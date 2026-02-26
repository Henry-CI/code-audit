# Security Audit Report — Pass 1
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Audit Date:** 2026-02-26
**Files Audited:**
- `src/main/java/com/querybuilder/StatementPreparer.java`
- `src/main/java/com/querybuilder/filters/StringContainingFilterHandler.java`
- `src/main/webapp/html-jsp/settings/settings.jsp`
- `src/main/java/com/dao/SubscriptionDAO.java`
- `src/main/java/com/bean/SubscriptionBean.java`
- `src/main/java/com/actionform/SubscriptionActionForm.java`
- `src/main/webapp/html-jsp/driver/subscription.jsp`
- `src/main/webapp/html-jsp/settings/subscription.jsp`
- `src/main/webapp/html-jsp/users/subscription.jsp`
- `src/main/webapp/html-jsp/result/success.jsp`
- `src/main/java/com/action/SwitchCompanyAction.java`
- `src/main/java/com/actionform/SwitchCompanyActionForm.java`
- `src/main/java/com/action/SwitchLanguageAction.java`
- `src/main/java/com/action/SwitchRegisterAction.java`

**Auditor:** Automated security audit (Claude)

---

## Findings

---

### CRITICAL: SQL Injection in SubscriptionDAO.checkCompFleetAlert via Direct String Concatenation

**File:** `src/main/java/com/dao/SubscriptionDAO.java` (line 99)

**Description:**
The method `checkCompFleetAlert(String comId)` concatenates the caller-supplied `comId` parameter directly into a SQL query string without any sanitisation or parameterised binding. A `java.sql.Statement` (not `PreparedStatement`) is used to execute the result.

```java
String sql = "select name from company_subscription as c,subscription as s "
           + "where c.subscription_id = s.id "
           + "and s.file_name = 'FleetcheckAlert' "
           + "and c.comp_id ='" + comId + "'";
log.info(sql);
rs = stmt.executeQuery(sql);
```

The call site in `FleetcheckAction.java` (line 165) passes `sessCompId` directly from the HTTP session:

```java
String sessCompId = (String)(session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
...
String name = subscriptionDAO.checkCompFleetAlert(sessCompId);
```

`sessCompId` is set either at login or — critically — via `SwitchCompanyAction` / `CompanySessionSwitcher.UpdateCompanySessionAttributes()`. Although the session value is not directly user-supplied in the request body at query time, any path that allows a controlled value into `sessCompId` (including the IDOR in `SwitchCompanyAction` described below, a future regression, or a session-fixation attack) creates a direct SQLi vector. Additionally, the raw SQL is logged via `log.info(sql)`, which means injected payloads appear in log files and could be used for blind-injection timing attacks.

The SQL query also uses an implicit cross join (old comma-style) rather than explicit JOIN syntax, which obscures the attack surface during code review.

**Risk:**
Full SQL injection. Depending on database configuration and permissions, this could lead to: unauthorised cross-tenant data read (SELECT on any table), data destruction (if the DB user has DELETE/UPDATE rights), or server-side command execution (via database functions such as PostgreSQL's `COPY TO/FROM`, `pg_read_file`, etc.). The query runs against the production database connection pool.

**Recommendation:**
Replace the `Statement` with a `PreparedStatement` and bind `comId` as a typed parameter:

```java
String sql = "SELECT name FROM company_subscription AS c "
           + "JOIN subscription AS s ON c.subscription_id = s.id "
           + "WHERE s.file_name = 'FleetcheckAlert' AND c.comp_id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, comId);
rs = ps.executeQuery();
```

Remove the `log.info(sql)` call that dumps the assembled query with user-controlled data.

---

### CRITICAL: SQL Injection in SubscriptionDAO.getAllReport via Frequency List Concatenation

**File:** `src/main/java/com/dao/SubscriptionDAO.java` (lines 38–51)

**Description:**
The method `getAllReport(ArrayList<String> frequencies)` builds a SQL `WHERE` clause by iterating over the supplied `frequencies` list and appending each value directly into the query string using string concatenation. A raw `Statement` is used to execute it.

```java
String extra = "";
for (int i = 0; i < frequencies.size(); i++) {
    extra += " frequency = '" + frequencies.get(i) + "' or";
}
if (extra.length() > 0) {
    extra = extra.substring(0, extra.lastIndexOf("or") - 1);
    extra = " and (" + extra + ")";
}

String sql = "select company.email, comp_id,sp.name, sp.file_name,frequency "
           + " from company_subscription as s "
           + " left outer join company on company.id = s.comp_id  "
           + " left outer join subscription as sp on sp.id = s.subscription_id"
           + "  where type ilike 'Report'" + extra + " limit 1";
```

The caller in `MailerAction.java` (line 88) populates the list from hard-coded strings (`"Weekly"`, `"Daily"`, `"Monthy"`), so this particular call site is not currently exploitable. However, the method signature accepts any `ArrayList<String>`, has no input validation, and the pattern is hazardous. If the method is ever called with attacker-influenced data (e.g., via an administrative scheduling endpoint), full SQL injection results.

Additionally, the off-by-one in the `substring`/`lastIndexOf` logic (`extra.lastIndexOf("or") - 1`) will throw a `StringIndexOutOfBoundsException` if a frequency value itself contains the substring `"or"`, creating a denial-of-service path.

**Risk:**
SQL injection if any future caller passes user-controlled frequency values. Denial-of-service via malformed frequency strings containing `"or"`.

**Recommendation:**
Use a `PreparedStatement` with placeholders, constructing the `IN (?, ?, ...)` clause dynamically by counting list elements, then binding each value with `ps.setString()`. Remove the manual string concatenation entirely.

---

### HIGH: Insecure Direct Object Reference (IDOR) — SwitchCompanyAction Does Not Validate Company Ownership

**File:** `src/main/java/com/action/SwitchCompanyAction.java` (lines 31–38)

**Description:**
`SwitchCompanyAction` allows an authenticated user who is either a `isSuperAdmin` or `isDealerLogin` to switch the active company stored in their session. The validation consists solely of checking these two boolean flags. The action then calls `LoginDAO.getCompanies(isSuperAdmin, isDealerLogin, loggedInCompanyId)` to obtain the list of permitted companies and iterates over the result:

```java
if (!isSuperAdmin && !isDealerLogin) {
    return mapping.findForward("failure");
}

List<CompanyBean> companies = LoginDAO.getCompanies(isSuperAdmin, isDealerLogin, loggedInCompanyId);
for (CompanyBean company : companies)
    if (company.getId().equals(loginActionForm.getCurrentCompany()))
        CompanySessionSwitcher.UpdateCompanySessionAttributes(company, request, session);
```

At first glance this appears safe: the list of companies is fetched server-side, and the form's `currentCompany` value is only accepted if it exists in that server-derived list. However, several problems remain:

1. **Silent no-op on mismatch**: If `currentCompany` does not match any company in the list, the code silently falls through the loop and still returns `"successAdmin"`. The session is left in its previous state with no error, and the response gives no indication that the switch was rejected. This is not an access control bypass in isolation, but masks the boundary condition and could lead to confused state.

2. **Super-admin bypass**: When `isSuperAdmin == true`, `LoginDAO.getCompanies` calls `getSuperAdminCompanies()` which returns **all companies in the database**. A super-admin can therefore switch `sessCompId` to any company ID whatsoever, including companies belonging to other tenants. While this may be intentional for a super-admin role, there is no secondary confirmation, audit log, or rate-limiting on this action, making it trivially scriptable for bulk data harvesting.

3. **`sessAccountId` vs `sessCompId` divergence after switch**: After `CompanySessionSwitcher.UpdateCompanySessionAttributes()` runs, `sessCompId` is updated to the new company, but `sessAccountId` (set at login to the original company ID) is **not** updated. Downstream code that uses `sessAccountId` (e.g., `SwitchCompanyAction` line 29 re-reads it for the `getCompanies` call) will observe the original value. If a dealer performs a company switch, the next call to `SwitchCompanyAction` recomputes the permitted list based on the **original** `sessAccountId`, which could produce an inconsistent allowed-company list.

**Risk:**
A dealer or super-admin account can access data from any company they are authorised to see simply by submitting a `currentCompany` POST parameter. A compromised super-admin or dealer account therefore becomes a pivot point for full cross-tenant data access. The silent success on an invalid switch could mask exploitation attempts in logs.

**Recommendation:**
- Add an explicit `else` branch after the loop that returns a proper access-denied forward when no matching company was found, and log the attempted company ID.
- After a successful switch, update `sessAccountId` to match the new `sessCompId`, or redesign the session model to clearly separate the "originating account" from the "currently viewed company."
- Add an audit log entry for every company switch that includes the original company, target company, timestamp, and user ID.
- For super-admin access, consider requiring re-authentication or MFA confirmation before switching to a non-owned company.

---

### HIGH: No Session Invalidation / Regeneration on Company Switch

**File:** `src/main/java/com/action/SwitchCompanyAction.java` (lines 25–42) and `src/main/java/com/util/CompanySessionSwitcher.java` (lines 17–46)

**Description:**
When a user switches the active company context, neither `SwitchCompanyAction` nor `CompanySessionSwitcher` calls `session.invalidate()` followed by `request.getSession(true)`. The same session ID remains in use before and after the company switch. The session object is mutated in place:

```java
session.setAttribute("sessCompId", comp_id);
session.setAttribute("currentCompany", comp_id);
session.setAttribute("sessCompName", company.getName());
// ... other attributes set on the same session ...
```

This means:
- A session fixation attack targeting the period between login and company switch retains full access to the new company context without re-authentication.
- Any browser tab or concurrent request that read the old `sessCompId` between the attribute-writes and the response completion can observe a partially-updated session (race condition on session attributes in a multi-threaded servlet container).
- Cached session state from the old company (e.g., `arrUnit`, `arrComp`, `arrExpiringTrainings`) may persist in the session for a window until `UpdateCompanySessionAttributes` completes, and any concurrent request processed in that window will observe inconsistent tenant data.

`CompanySessionSwitcher` does not update all tenant-scoped session attributes either — for example, `sessArrComp`, `sessUserId`, `isSuperAdmin`, and `isDealerLogin` are set at login but not touched on a company switch.

**Risk:**
Session fixation / session riding allowing a passive attacker with access to the session ID (e.g., via network sniffing on HTTP, or via log exposure) to follow a session across company boundaries. Race conditions may briefly expose one tenant's data to another tenant's requests in high-concurrency scenarios.

**Recommendation:**
On any security context change (login, company switch, privilege elevation), invalidate the existing session, create a new one, and migrate only the necessary attributes:

```java
HttpSession oldSession = request.getSession(false);
// copy required attributes
Map<String, Object> toMigrate = collectRequiredAttributes(oldSession);
oldSession.invalidate();
HttpSession newSession = request.getSession(true);
toMigrate.forEach(newSession::setAttribute);
```

Alternatively, use a session migration helper that atomically replaces the session ID while preserving content (available in Spring Security; must be implemented manually for Struts 1.x).

---

### HIGH: No CSRF Protection on Company Switch or Settings Forms

**File:** `src/main/webapp/includes/menu.inc.jsp` (line 24), `src/main/webapp/html-jsp/settings/settings.jsp` (line 16), `src/main/java/com/action/SwitchCompanyAction.java`, `src/main/webapp/WEB-INF/struts-config.xml`

**Description:**
The company-switch form is a plain HTML form that submits via POST to `switchCompany.do`:

```jsp
<html:form method="post" action="switchCompany.do">
    <html:select styleId="currentCompany" property="currentCompany"
                 styleClass="form-control"
                 onchange="this.form.submit()">
```

The settings form similarly submits via POST to `settings.do`:

```jsp
<html:form action="settings.do" method="post">
```

No CSRF token is present in either form, in any hidden field, or in the action handler. The Struts validator in `validation.xml` does not configure a CSRF rule for `switchCompanyActionForm` or `AdminSettingsActionForm`. Struts 1.x does not add CSRF tokens automatically.

An attacker who can trick an authenticated admin or dealer into visiting a malicious page can craft a cross-origin form POST that silently switches the victim's active company context, or saves arbitrary settings (date format, timezone, session length, notification preferences) on the victim's account. The `onchange="this.form.submit()"` trigger on the company-switch dropdown makes the attack window very narrow for a UX-driven navigation, but a hidden auto-submitting form on an attacker-controlled page bypasses this entirely.

**Risk:**
Cross-Site Request Forgery allowing an unauthenticated attacker to:
- Switch an authenticated admin/dealer's active company context to one they control, potentially causing subsequent administrative actions to be applied to the wrong tenant.
- Modify company settings (session timeout, notification alerts, timezone) without the victim's knowledge.

**Recommendation:**
Implement the Synchronizer Token Pattern for all state-changing POST endpoints:
1. Generate a cryptographically random token per session (or per form) at render time and store it in the session.
2. Embed the token in all forms as a hidden field.
3. Validate the token server-side in the action handler before processing the request, rejecting requests with missing or mismatched tokens.

For Struts 1.x, this must be implemented manually (e.g., a custom `RequestProcessor` subclass) or via a framework such as OWASP CSRFGuard.

---

### HIGH: CSRF on Subscription Notification Preference Forms

**File:** `src/main/webapp/html-jsp/users/subscription.jsp` (lines 15, 70–75), `src/main/webapp/html-jsp/driver/subscription.jsp` (lines 24–81), `src/main/webapp/WEB-INF/struts-config.xml`

**Description:**
Both subscription JSPs render POST forms that modify notification subscription settings (red impact email/SMS alerts, training expiry notifications). Neither form contains a CSRF token:

```jsp
<!-- users/subscription.jsp -->
<html:form method="post" action="admindriveredit.do" styleClass="ajax_mode_c"
           styleId="adminDriverUpdateSubscription">
    ...
    <html:hidden property="op_code" value="edit_subscription"/>
    <!-- No CSRF token -->
```

```jsp
<!-- driver/subscription.jsp -->
<html:form method="post" action="admindriveredit.do" styleClass="ajax_mode_c driver_edit_form"
           styleId="adminDriverUpdateSubscription">
    ...
    <html:hidden property="op_code" value="edit_subscription" name="driverEmails"/>
    <!-- No CSRF token -->
```

The `admindriveredit.do` endpoint accepts `op_code=edit_subscription` to identify the operation, and the driver ID is taken from the session-bound bean. An attacker can forge a subscription-update request for any driver the victim has access to.

**Risk:**
Forged POST requests can silently enable or disable alert notifications for drivers within a company, e.g., disabling red-impact email alerts to suppress notifications of dangerous forklift impacts.

**Recommendation:**
Apply the same Synchronizer Token Pattern as described for the company-switch form to all state-changing forms, including `admindriveredit.do`.

---

### MEDIUM: Reflected XSS via Unescaped Session Attribute in settings.jsp JavaScript Block

**File:** `src/main/webapp/html-jsp/settings/settings.jsp` (lines 171–174)

**Description:**
Two session attributes are read in a JSP scriptlet block and interpolated directly into a `<script>` block without any escaping:

```jsp
<%
    String dateFormat = (String) session.getAttribute("sessDateTimeFormat");
    String compTimezone = (String) session.getAttribute("timezoneId");
%>
...
<script>
    var dateFormat = "<%=dateFormat %>";
    ...
    $('#dateFormat').val(dateFormat);
    $('#timezone').val("<%=compTimezone %>");
</script>
```

`sessDateTimeFormat` is ultimately sourced from the `company.date_format` database column, which is set when a company is registered or when settings are saved. `timezoneId` comes from the `timezone` table. If either of these values contains a double-quote, a backslash, or JavaScript-meaningful characters, the generated script will be syntactically broken or executable. More critically, if an attacker can influence these values (e.g., via the settings-save form, which itself lacks CSRF protection, or via a super-admin company-switch), they can inject arbitrary JavaScript into the settings page for all users of that company.

For example, a `dateFormat` value of `"; alert(document.cookie); var x = "` would produce:

```javascript
var dateFormat = ""; alert(document.cookie); var x = "";
```

**Risk:**
Stored XSS (via database) or second-order XSS. A malicious super-admin or an attacker who exploits the CSRF on the settings form can inject JavaScript that runs in the browser of any user who opens the settings panel, enabling session hijacking or credential theft.

**Recommendation:**
Never interpolate server-side values directly into JavaScript string literals. Use a JSON encoder:

```jsp
var dateFormat = <%= com.fasterxml.jackson.databind.ObjectMapper.default().writeValueAsString(dateFormat) %>;
```

Or pass the values to JavaScript via `data-` attributes on the HTML element and read them with `$.data()` or `dataset`, then ensure the HTML attribute context uses proper HTML encoding (`<c:out>` or `fn:escapeXml`).

---

### MEDIUM: Unescaped Session Attribute Injected into JavaScript in menu.inc.jsp

**File:** `src/main/webapp/includes/menu.inc.jsp` (lines 41–42)

**Description:**
The session attribute `sessCompId` is written directly into a `<script>` block without encoding:

```jsp
<script>
    $('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');
</script>
```

`sessCompId` is a numeric company ID (an integer stored as a String), which is low-risk in practice because it originates from a controlled integer column. However, the pattern is fragile: if the type ever changes, or if the value is influenced by data that passes through user-editable fields, it becomes an XSS vector. There is also no explicit validation that `sessCompId` is a numeric string before interpolation.

**Risk:**
Low-impact in current form (numeric ID), but establishes a dangerous pattern. If `sessCompId` were ever set to a non-numeric value via the IDOR/company-switch path or session manipulation, the injected value would execute as JavaScript.

**Recommendation:**
Use `fn:escapeXml` or pass the value through a JSON encoder before embedding in a script context. Even for ostensibly numeric values, defensive encoding should be applied:

```jsp
$('select[name="currentCompany"]').val(<%= Integer.parseInt((String) session.getAttribute("sessCompId")) %>);
```

Or better, use a `data-` attribute on the `<select>` element set via proper JSP HTML encoding, and read it in JavaScript with `element.dataset`.

---

### MEDIUM: SQL Injection Pattern in SubscriptionDAO.saveDefualtSubscription via Integer Concatenation

**File:** `src/main/java/com/dao/SubscriptionDAO.java` (line 133)

**Description:**
The `saveDefualtSubscription(int compId)` method inserts default subscriptions for a new company by concatenating the `compId` integer directly into a SQL string:

```java
String sql = "insert into company_subscription (comp_id,subscription_id) "
           + "select " + compId + ", id from subscription where frequency is not null";
stmt.execute(sql);
```

Because `compId` is declared as a Java primitive `int`, direct SQL injection via this parameter is not possible (the compiler guarantees it cannot be a non-integer). However, the approach violates the parameterised query principle and creates several secondary concerns:

- The method uses `Statement.execute()` rather than `executeUpdate()`, which means the JDBC driver may process additional result sets or output parameters in some database configurations.
- The `ResultSet rs` variable is declared and initialised to `null` at the top of the method (line 124), but `rs` is never assigned in this method — the `finally` block calls `rs.close()` conditionally, which is a dead code path. This masking of resource-management intent makes the method harder to audit.
- If a future refactor changes `compId` to `String` (as seen in `checkCompFleetAlert`), the method immediately becomes injectable.

**Risk:**
Currently not directly exploitable due to Java's type system. Low risk in isolation, but the inconsistent pattern (some methods use concatenation for integers, others for strings) increases the probability of a copy-paste error introducing a genuine SQLi.

**Recommendation:**
Use `PreparedStatement` consistently:

```java
String sql = "INSERT INTO company_subscription (comp_id, subscription_id) "
           + "SELECT ?, id FROM subscription WHERE frequency IS NOT NULL";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setInt(1, compId);
ps.executeUpdate();
```

Remove the unused `rs` variable and dead `rs.close()` call.

---

### MEDIUM: SQL Injection in getAllReport — Off-by-One DoS via Frequency Value Containing "or"

**File:** `src/main/java/com/dao/SubscriptionDAO.java` (lines 42–43)

**Description:**
Already covered as part of Finding 2 (getAllReport SQL injection), but the denial-of-service aspect warrants its own severity entry for triage purposes. The logic that trims the trailing `" or"` from the constructed `extra` string is:

```java
extra = extra.substring(0, extra.lastIndexOf("or") - 1);
```

If a frequency string such as `"Bimonthly"` or `"Bi-Weekly Reorder"` (any value containing the substring `"or"`) were passed, `lastIndexOf("or")` would match inside the frequency value itself rather than the trailing ` or` separator, producing a negative or incorrect index and throwing `StringIndexOutOfBoundsException`. This exception propagates as a `SQLException` to the caller and could crash the mailer batch job or any future interactive endpoint.

**Risk:**
Denial of service against the mailer batch job if frequency strings containing `"or"` are introduced. Low probability given current hard-coded call site, but significant if the method is ever exposed to variable input.

**Recommendation:**
Replace the manual trailing-`or` trim with a proper collection join:

```java
String placeholders = String.join(",", Collections.nCopies(frequencies.size(), "?"));
String sql = "... WHERE type ILIKE 'Report' AND frequency IN (" + placeholders + ")";
PreparedStatement ps = conn.prepareStatement(sql);
for (int i = 0; i < frequencies.size(); i++) {
    ps.setString(i + 1, frequencies.get(i));
}
```

---

### MEDIUM: Language Cookie Stored Without HttpOnly or Secure Flags

**File:** `src/main/java/com/action/SwitchLanguageAction.java` (lines 61–63)

**Description:**
The language-preference cookie `ckLanguage` is created and managed without setting the `HttpOnly` or `Secure` flags:

```java
cookie = new Cookie("ckLanguage", language);
cookie.setMaxAge(24 * 60 * 60);
response.addCookie(cookie);
```

Without `HttpOnly`, any JavaScript running in the page (including injected scripts from the XSS vulnerabilities above) can read this cookie via `document.cookie`. Without `Secure`, the cookie is sent over unencrypted HTTP connections, exposing it to network interception.

While the `ckLanguage` cookie itself is low-sensitivity, the same cookie-security omission pattern exists in the application generally (the `web.xml` does not configure `<session-config><cookie-config><http-only>true</http-only></cookie-config></session-config>`, meaning the JSESSIONID cookie may also lack HttpOnly in some Tomcat configurations).

**Risk:**
The `ckLanguage` cookie value can be read by injected JavaScript. The missing `Secure` flag means the cookie is sent over HTTP, exposable to man-in-the-middle attacks. More critically, if the JSESSIONID session cookie lacks HttpOnly (check Tomcat context.xml), the XSS vulnerabilities identified in this report become session-hijacking vulnerabilities.

**Recommendation:**
Set both flags on all cookies created by the application:

```java
cookie.setHttpOnly(true);
cookie.setSecure(true); // only if the application is served exclusively over HTTPS
```

Also add the following to `web.xml` to apply `HttpOnly` and `Secure` to the JSESSIONID session cookie:

```xml
<session-config>
    <session-timeout>30</session-timeout>
    <cookie-config>
        <http-only>true</http-only>
        <secure>true</secure>
    </cookie-config>
</session-config>
```

---

### MEDIUM: SwitchLanguageAction Accessible Without Authentication

**File:** `src/main/java/com/action/SwitchLanguageAction.java` (lines 22–68) and `src/main/java/com/actionservlet/PreFlightActionServlet.java` (line 109)

**Description:**
`PreFlightActionServlet.excludeFromFilter()` explicitly excludes `swithLanguage.do` from the authentication check (note the typo "swithLanguage" in both the servlet and struts-config.xml path):

```java
else if (path.endsWith("swithLanguage.do")) return false;
```

This means any unauthenticated user can POST to `swithLanguage.do` to set the Struts `LOCALE_KEY` session attribute (`Globals.LOCALE_KEY`) on their session. This is functionally acceptable for a locale-switching endpoint, but the implementation has two concerns:

1. The `language` parameter is taken directly from the request and used to set a cookie with user-controlled content:
   ```java
   String language = request.getParameter("language") == null ? "" : request.getParameter("language");
   cookie.setValue(language);
   ```
   `Cookie.setValue()` in the Java Servlet API does not accept all characters (specifically semicolons, commas, whitespace, and other special characters are disallowed by RFC 6265 and throw `IllegalArgumentException` in some servlet containers). Passing a malformed `language` value may cause an unhandled exception or, in lenient containers, inject additional cookie attributes (cookie header injection).

2. There is no whitelist of valid language codes. An attacker can set the locale to an arbitrary string, which is then stored in the session and used by Struts for i18n lookups. Invalid locale values could cause `NullPointerException` in downstream code that calls `SwitchLanguageAction.getLocale()` (returns `null` for unknown codes) and then uses the result without null-checking.

**Risk:**
Cookie header injection (low severity). Potential `NullPointerException` if the `null` locale returned for unknown language codes is used without null-checking. Unauthenticated manipulation of session locale state.

**Recommendation:**
Validate `language` against the explicit allowed set `{"0", "1", "2", "3", "4"}` before processing. Return a `400 Bad Request` for values outside this set. Apply `Pattern.matches("[0-4]", language)` before use.

---

### MEDIUM: SwitchRegisterAction Accessible Without Authentication and Sets Sensitive Session Attributes

**File:** `src/main/java/com/action/SwitchRegisterAction.java` (lines 20–31) and `src/main/java/com/actionservlet/PreFlightActionServlet.java` (line 108)

**Description:**
`switchRegister.do` is excluded from the authentication filter:

```java
else if (path.endsWith("switchRegister.do")) return false;
```

The action sets session attributes `arrTimezone` and `arrLanguage` from DAO calls, and sets `accountAction = "register"`:

```java
session.setAttribute("arrTimezone", TimezoneDAO.getInstance().getAllTimezone());
session.setAttribute("arrLanguage", LanguageDAO.getInstance().getAllLan());
session.setAttribute("accountAction", "register");
```

The `request.getSession(false)` call on line 23 will return `null` if there is no existing session — for an unauthenticated visitor, this is the expected case, yet `session.setAttribute(...)` is called unconditionally, causing a `NullPointerException` crash if no session exists. This is a reliable denial-of-service against this endpoint for clients without a session cookie.

Additionally, setting `accountAction = "register"` on an authenticated user's session (if they navigate to this URL) could interfere with their session state in an unexpected way.

**Risk:**
`NullPointerException` when called by a client without a session (unauthenticated, no prior request). This causes an unhandled exception that propagates to the global error page, potentially leaking stack trace information. Authenticated users who visit the URL have their `accountAction` session attribute overwritten.

**Recommendation:**
Replace `request.getSession(false)` with `request.getSession(true)` (create session if absent) for this registration-flow endpoint, or add a null-check before setAttribute calls. Restrict the endpoint to only pre-registration flows and not to authenticated sessions.

---

### LOW: Struts Synchronizer Token Not Used for Any State-Changing Action

**File:** `src/main/webapp/WEB-INF/struts-config.xml` (all action mappings), `src/main/webapp/WEB-INF/validation.xml`

**Description:**
Struts 1.x ships with a built-in Synchronizer Token mechanism (`Action.saveToken(request)` / `Action.isTokenValid(request)`) that provides a simple per-session CSRF defence. No action in `struts-config.xml` makes use of this mechanism. The `validation.xml` file only validates field presence and format; it has no CSRF rule definitions.

This is a systemic gap rather than a per-endpoint finding: every POST action in the application that changes state is potentially vulnerable to CSRF.

**Risk:**
Systemic absence of CSRF protection across all state-changing actions (company switch, settings save, subscription management, driver management, unit management, alert configuration, etc.).

**Recommendation:**
Audit all POST action handlers and apply Struts Synchronizer Token or a framework-level CSRF filter (OWASP CSRFGuard, custom `RequestProcessor`) to every state-changing endpoint. Prioritise the high-value endpoints: `switchCompany.do`, `settings.do`, `admindriveredit.do`, `adminunitservice.do`.

---

### LOW: Sensitive Data Logged in Plain Text (SQL Queries with Identifiers)

**File:** `src/main/java/com/dao/SubscriptionDAO.java` (lines 53, 100, 134)

**Description:**
All three SQL methods in `SubscriptionDAO` log the assembled SQL string via `log.info(sql)`:

```java
log.info(sql);   // line 53 — getAllReport, query includes frequency values
log.info(sql);   // line 100 — checkCompFleetAlert, query includes comId
log.info(sql);   // line 134 — saveDefualtSubscription, query includes compId
```

For `checkCompFleetAlert`, this logs the raw `comId` value injected into the query string. In an attack scenario, the injected SQL payload appears verbatim in application logs. If log files are accessible to developers or are shipped to a log-aggregation service, they expose both the payload and potentially the attacker's intent.

More broadly, logging SQL queries at INFO level in production creates a significant data-leakage surface if logs are compromised.

**Risk:**
Log injection: an attacker crafting a SQL injection payload in `comId` can write attacker-controlled text into the application logs (log forgery). Sensitive query patterns visible in log aggregation systems.

**Recommendation:**
Remove or downgrade SQL query logging to DEBUG level, and only enable it in non-production environments. Use parameterised logging with placeholders (`log.debug("checkCompFleetAlert comId={}", comId)`) rather than logging the assembled SQL string.

---

### LOW: StatementPreparer Does Not Validate Input or Enforce Maximum Parameter Count

**File:** `src/main/java/com/querybuilder/StatementPreparer.java` (lines 11–31)

**Description:**
`StatementPreparer` is a well-structured wrapper around `PreparedStatement` that correctly uses typed setter methods (`setDate`, `setLong`, `setString`, `setInt`). This design is sound and does not introduce SQL injection directly. However, the class has no bounds checking: `index` starts at 0 and increments on every `add*()` call without verifying that the number of parameters added does not exceed the number of `?` placeholders in the underlying prepared statement.

If a caller adds more parameters than the statement has placeholders, the JDBC driver will throw an `SQLException` at execution time rather than at the `add*()` call site, making errors harder to diagnose.

There is no mechanism to detect that callers have forgotten to add a required parameter, which could result in silent use of `null` for unset parameters in some JDBC drivers.

**Risk:**
Low. This is a code quality and defensive programming concern rather than a direct security vulnerability. Incorrect parameter counts cause runtime exceptions rather than security bypass.

**Recommendation:**
Consider adding a constructor parameter `int expectedParamCount` and asserting at construction time that the prepared statement has the expected number of parameters, or validate at the first `add*()` call that `index < expectedParamCount`. This improves fail-fast behaviour and reduces the chance of logic errors that could have security implications (e.g., a missing parameter causing a query to return broader results than intended).

---

### LOW: StringContainingFilterHandler Column Names Are Not Validated Against an Allowlist

**File:** `src/main/java/com/querybuilder/filters/StringContainingFilterHandler.java` (lines 21–28)

**Description:**
`StringContainingFilterHandler` correctly parameterises the **search value** (the `searchText` is bound via `preparer.addString(searchText)`). However, the **column names** (`fieldNames`) are interpolated directly into the SQL fragment:

```java
return String.format(" AND %s ILIKE ? ", fieldNames.get(0));
// and:
filter.append(fieldName).append(" ILIKE ? OR ");
```

Column names cannot be parameterised in standard SQL; they must be embedded in the query string. This is architecturally correct. However, if the `fieldNames` supplied to the constructor are ever derived from user input (e.g., a configurable sort/search field in an admin list page), an attacker could inject arbitrary SQL through the column-name position.

A review of the codebase for callers of `StringContainingFilterHandler` would be needed to determine whether any call site passes user-controlled column names (out of scope for this file-set batch). The concern is flagged here as a design-level risk.

**Risk:**
SQL injection via column-name injection if any caller passes user-controlled strings as `fieldNames`. Currently rated LOW pending caller analysis; escalate to HIGH if user-controlled column names are found in callers.

**Recommendation:**
Implement a compile-time or runtime allowlist of valid column names for each entity. Validate each `fieldName` against this allowlist in the constructor and throw `IllegalArgumentException` for unrecognised names. This is a defence-in-depth measure regardless of whether current callers are safe.

---

### LOW: bean:write XSS Risk in settings/subscription.jsp and users/subscription.jsp (Potential Stored XSS via Alert/Report Names)

**File:** `src/main/webapp/html-jsp/settings/subscription.jsp` (lines 38, 72–73), `src/main/webapp/html-jsp/users/subscription.jsp` (lines 31–32, 70–73)

**Description:**
Both subscription JSPs use `<bean:write>` to render `alert_name` and `frequency` values from the `alertList` and `reportList` request attributes:

```jsp
<td><bean:write property="alert_name" name="companyAlert"></bean:write></td>
<td><bean:write property="alert_name" name="companyReport"></bean:write></td>
<td><bean:write property="frequency" name="companyReport"></bean:write></td>
```

The Struts `<bean:write>` tag does **not** HTML-encode output by default (unlike JSTL `<c:out>`). If `alert_name` or `frequency` values stored in the database contain HTML metacharacters (e.g., `<script>alert(1)</script>`), they will be rendered unescaped in the browser.

A malicious administrator with access to the alert/report configuration pages could store a crafted name that executes JavaScript in the browser of any user who views the subscription list.

**Risk:**
Stored XSS via alert/report names. If an administrator (or a user who exploits the CSRF vulnerability on the alert-add form) stores a crafted `alert_name`, all users of the company who view the subscription page are attacked.

**Recommendation:**
Replace `<bean:write>` with `<bean:write filter="true">` (which HTML-encodes the output) or migrate to JSTL `<c:out value="${...}" escapeXml="true"/>`. Audit all `<bean:write>` tags in the application for missing `filter="true"`.

---

### INFO: StatementPreparer and StringContainingFilterHandler Architecture Is Sound

**File:** `src/main/java/com/querybuilder/StatementPreparer.java`, `src/main/java/com/querybuilder/filters/StringContainingFilterHandler.java`

**Description:**
The `StatementPreparer` helper class wraps `PreparedStatement` and exposes typed setter methods, consistently using JDBC parameterised binding. `StringContainingFilterHandler` correctly parameterises the search value (wrapping it in `%...%` and binding it via `StatementPreparer.addString()`), while column names are statically embedded in the query fragment. This is the correct pattern for user-value parameterisation.

`getSubscriptionByName` in `SubscriptionDAO` (line 162) also uses the parameterised `DBUtil.queryForObject` utility correctly:

```java
DBUtil.queryForObject("select id from subscription where file_name = ? ",
    stmt -> stmt.setString(1, name), rs -> SubscriptionBean.builder().id(rs.getString(1)).build());
```

These demonstrate that parameterised query infrastructure exists in the codebase. The security failures in `getAllReport`, `checkCompFleetAlert`, and `saveDefualtSubscription` are regressions from this established pattern, not a systemic absence of the capability.

**Risk:** None (informational).

**Recommendation:** Enforce the parameterised pattern for all new DAO code via code review checklist. Consider a static analysis rule (SpotBugs SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE) to prevent future regressions.

---

### INFO: SubscriptionBean Has No Input Validation or Constraints

**File:** `src/main/java/com/bean/SubscriptionBean.java`

**Description:**
`SubscriptionBean` is a plain data holder with `@Data` and `@NoArgsConstructor` from Lombok. All fields default to empty strings. There are no JSR-303/JSR-380 validation annotations (`@NotNull`, `@Size`, `@Pattern`) on any field, and no validation logic in setters. The `file_name` field in particular is used as a SQL query parameter (in `getSubscriptionByName`) and as an email file-path reference, but accepts any string.

**Risk:** Informational. No direct exploitability from the bean class in isolation.

**Recommendation:** Add Bean Validation annotations to enforce expected field formats. At minimum, `file_name` and `id` should be validated for length and character set.

---

### INFO: success.jsp Returns Only an HTTP 200 with No Body — Potential Information Leakage if Misconfigured

**File:** `src/main/webapp/html-jsp/result/success.jsp` (lines 1–3)

**Description:**
The file contains only:

```xml
<result name="empty" type="httpheader">
    <param name="status">200</param>
</result>
```

This appears to be a Struts 2 result configuration fragment accidentally placed in a JSP file (Struts 2 syntax in a Struts 1.x application). It will be sent as literal text body in an HTTP 200 response if this JSP is ever forwarded to. Browsers will render it as text, which is harmless, but it suggests a copy-paste error from a Struts 2 project. If the intent was to return an empty 200 response, this JSP does not achieve it — it returns the XML text as a body.

**Risk:** Low. The XML body is not sensitive. The misconfiguration suggests incomplete migration or copy-paste from a different codebase.

**Recommendation:** Replace with a proper empty JSP (`<%-- empty --%>`) or remove the file if it is unused. Search for other Struts 2 syntax fragments that may have been incorrectly included.

---

## Summary

| # | Severity | Title | File |
|---|----------|-------|------|
| 1 | CRITICAL | SQL Injection — `checkCompFleetAlert` direct string concat | `SubscriptionDAO.java:99` |
| 2 | CRITICAL | SQL Injection — `getAllReport` frequency list concat | `SubscriptionDAO.java:38-51` |
| 3 | HIGH | IDOR — `SwitchCompanyAction` no ownership check, silent no-op on invalid switch | `SwitchCompanyAction.java:31-38` |
| 4 | HIGH | No session invalidation/regeneration on company switch | `SwitchCompanyAction.java`, `CompanySessionSwitcher.java` |
| 5 | HIGH | No CSRF protection on company switch form | `menu.inc.jsp:24`, `SwitchCompanyAction.java` |
| 6 | HIGH | No CSRF protection on settings form | `settings/settings.jsp:16` |
| 7 | HIGH | No CSRF protection on subscription notification forms | `users/subscription.jsp`, `driver/subscription.jsp` |
| 8 | MEDIUM | Reflected/Stored XSS — session attributes interpolated into JS in settings.jsp | `settings/settings.jsp:171-174` |
| 9 | MEDIUM | Unescaped session attribute in JS — menu.inc.jsp | `menu.inc.jsp:41-42` |
| 10 | MEDIUM | SQL Injection pattern (type-safe today, fragile) — `saveDefualtSubscription` | `SubscriptionDAO.java:133` |
| 11 | MEDIUM | DoS via off-by-one in `getAllReport` frequency string trim | `SubscriptionDAO.java:42-43` |
| 12 | MEDIUM | Language cookie missing HttpOnly and Secure flags | `SwitchLanguageAction.java:61-63` |
| 13 | MEDIUM | `swithLanguage.do` bypasses auth; cookie header injection; null locale | `SwitchLanguageAction.java` |
| 14 | MEDIUM | `switchRegister.do` bypasses auth; NPE if no session | `SwitchRegisterAction.java:23` |
| 15 | LOW | Struts Synchronizer Token not used for any action | `struts-config.xml` (systemic) |
| 16 | LOW | SQL query with user data logged at INFO level | `SubscriptionDAO.java:53,100,134` |
| 17 | LOW | `StatementPreparer` lacks parameter-count bounds checking | `StatementPreparer.java` |
| 18 | LOW | `StringContainingFilterHandler` column names not allowlisted | `StringContainingFilterHandler.java:21-28` |
| 19 | LOW | `<bean:write>` without `filter="true"` — stored XSS via alert names | `settings/subscription.jsp`, `users/subscription.jsp` |
| 20 | INFO | `StatementPreparer` / `StringContainingFilterHandler` architecture is sound | — |
| 21 | INFO | `SubscriptionBean` lacks validation annotations | `SubscriptionBean.java` |
| 22 | INFO | `success.jsp` contains Struts 2 XML fragment — likely copy-paste error | `result/success.jsp` |

---

**CRITICAL: 2 / HIGH: 5 / MEDIUM: 7 / LOW: 5 / INFO: 3**
