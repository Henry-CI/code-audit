# Security Audit Report: LogoutAction, MailerAction, mailSuccuess.jsp

**Application:** forkliftiqadmin (FleetIQ / ForkliftIQ Admin Portal)
**Framework:** Apache Struts 1.3.10 on Apache Tomcat
**Audit Date:** 2026-02-26
**Pass:** 1
**Auditor:** Automated static analysis (CIG Audit)
**Files Audited:**
- `src/main/java/com/action/LogoutAction.java`
- `src/main/java/com/action/MailerAction.java`
- `src/main/webapp/html-jsp/mailSuccuess.jsp`

**Supporting files examined:**
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/java/com/dao/SubscriptionDAO.java`
- `src/main/java/com/util/Util.java`
- `src/main/java/com/util/RuntimeConf.java`
- `src/main/java/com/report/ReportAPI.java`
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/WEB-INF/tiles-defs.xml`
- `src/main/webapp/WEB-INF/web.xml`

---

## Executive Summary

This pass identified **7 findings** across the three audited files. The most severe is an unauthenticated trigger of the bulk email dispatch pipeline (`MailerAction` exposed without authentication), which directly combines with a SQL injection vulnerability in `SubscriptionDAO`. The logout implementation contains a session re-creation flaw that leaves a new unauthenticated session live after invalidation, and no CSRF protection guards the logout endpoint. The `mailSuccuess.jsp` file is currently empty (zero bytes), removing one potential XSS surface but raising a separate concern about unhandled error disclosure.

---

## Findings

---

### CRITICAL: Unauthenticated Access to Email Dispatch Endpoint (Authentication Bypass)

**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java` (line 105) / `src/main/java/com/action/MailerAction.java` (all)

**Description:**
`PreFlightActionServlet.excludeFromFilter()` returns `false` for `mailer.do`, meaning the auth gate is completely bypassed for this path:

```java
// PreFlightActionServlet.java line 105
else if (path.endsWith("mailer.do")) return false;
```

The logic in `excludeFromFilter` is inverted relative to its name: returning `false` means "do NOT apply the filter" (i.e., skip the `sessCompId` check). Any unauthenticated HTTP request to `/mailer.do` — including a cron-style URL with no session — will reach `MailerAction.execute()` without challenge.

`MailerAction` does the following on every invocation:
1. Reads `date` and `frequency` directly from request parameters (no sanitization, no auth check).
2. Passes `frequency` into `SubscriptionDAO.getAllReport()` which embeds it into a raw SQL string (see SQL injection finding below).
3. Downloads a PDF from an internal API endpoint using hardcoded admin credentials (`ciiadmin` / `hui`).
4. Dispatches emails with PDF attachments to all matching subscribers pulled from the database.

An anonymous internet user can force the mailer pipeline to run at will, consuming SMTP resources, triggering PDF generation against the internal API, and potentially causing email spam to all subscribed customers.

**Risk:**
- Any unauthenticated attacker can trigger mass email dispatch to all company subscribers.
- Repeated calls constitute a denial-of-service against the SMTP relay and internal PDF API.
- Combined with the SQL injection in `SubscriptionDAO` (see below), the attacker can manipulate which records are processed.
- No rate limiting, no IP allowlist, no secret token is present.

**Recommendation:**
- Remove `mailer.do` from the exclusion list entirely if it is not intended for public access.
- If it must be cron-invocable, protect it with a shared secret (HMAC token in the request, validated server-side) or restrict access to `localhost` / a private subnet at the Tomcat/firewall level.
- As an interim measure, add an explicit IP allowlist check at the top of `MailerAction.execute()`.

---

### CRITICAL: SQL Injection in SubscriptionDAO.getAllReport() via User-Controlled `frequency` Parameter

**File:** `src/main/java/com/dao/SubscriptionDAO.java` (lines 38-43) and `src/main/java/com/action/MailerAction.java` (lines 47-48, 76-78)

**Description:**
`MailerAction` reads the `frequency` request parameter without any sanitisation:

```java
// MailerAction.java lines 47-48
String frequency = request.getParameter("frequency") == null ? ""
        : request.getParameter("frequency");
```

It then adds this raw string to an `ArrayList<String>` and passes it to `SubscriptionDAO.getAllReport()`:

```java
// MailerAction.java lines 76-78
if (!frequency.equalsIgnoreCase("")) {
    frequencies.add(frequency);
}
```

Inside `getAllReport`, each element of `frequencies` is concatenated directly into a SQL string:

```java
// SubscriptionDAO.java lines 38-43
for (int i = 0; i < frequencies.size(); i++) {
    extra += " frequency = '" + frequencies.get(i) + "' or";
}
```

This produces a query fragment such as:

```sql
... and ( frequency = 'Daily' or frequency = 'INJECTED_VALUE' or)
```

Because `mailer.do` is unauthenticated, an anonymous attacker can send:

```
GET /mailer.do?frequency=Daily'+OR+'1'='1
```

This collapses the `WHERE` clause and causes all subscription records — across all tenants — to be processed and emailed, regardless of frequency or company. More destructive payloads (stacked queries on PostgreSQL, `UNION SELECT`, `DROP TABLE`) are also possible depending on the database driver's configuration.

The inner query in `getAllReport` uses a raw `Statement` (not `PreparedStatement`), confirming no parameterisation is present anywhere in this code path.

**Risk:**
- Full database read/write/delete by an unauthenticated attacker via a publicly accessible URL.
- Cross-tenant data exfiltration (all company subscription records, email addresses).
- Potential for destructive queries.

**Recommendation:**
- Replace the raw string-building loop with a parameterised `PreparedStatement` using `IN (?, ?, ...)` or equivalent.
- Apply input validation: `frequency` must be one of a fixed set of known values (`Daily`, `Weekly`, `Monthly`); reject anything else with HTTP 400 before it reaches the DAO layer.

---

### HIGH: Hardcoded Admin Credentials in Source Code

**File:** `src/main/java/com/action/MailerAction.java` (line 102)

**Description:**
The JSON payload sent to the internal PDF generation API contains hardcoded administrator credentials in plaintext:

```java
// MailerAction.java line 102
String input = "{\"admin_password\":\"ciiadmin\",\"username\": \"hui\",\"filters\":[...]}";
```

The username `hui` and password `ciiadmin` are embedded directly in source code. These credentials are also referenced in `RuntimeConf.debugEmailRecipet` (`hui@collectiveintelligence.com.au`) suggesting `hui` is a real administrative account. Anyone with access to the compiled `.class` files, the source repository, or log output (since `input` is logged at `log.info` level on line 137 on failure) can obtain these credentials.

Furthermore, the `company_id` is hardcoded to `1` in the same string, meaning the PDF API is always invoked in the context of company 1 regardless of which company is actually being reported on — a potential cross-tenant data issue.

**Risk:**
- Credential exposure through source code, build artifacts, log files, or decompilation.
- If the PDF API endpoint (`http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/`) is accessible externally, any attacker who discovers these credentials can invoke it directly.
- Hardcoded `company_id=1` means report data may be scoped to the wrong tenant.

**Recommendation:**
- Move credentials to environment variables or an encrypted secrets store (e.g., Tomcat `context.xml` with `<Resource>`, AWS Secrets Manager, or Vault).
- Remove credentials from log statements.
- Parameterise `company_id` from the subscription record rather than hardcoding it.

---

### HIGH: Session Re-Creation After Invalidation (Session Fixation Risk Post-Logout)

**File:** `src/main/java/com/action/LogoutAction.java` (lines 36-48)

**Description:**
`LogoutAction` correctly invalidates the existing session on line 39:

```java
theSession.invalidate();
```

However, immediately after invalidation, the code calls `request.getSession()` (without `false`) twice — once on line 44 and once on line 47:

```java
// LogoutAction.java lines 44-47
request.getSession().setAttribute(Globals.LOCALE_KEY, locale);
// ...
request.getSession().setAttribute("sessAds", AdvertismentDAO.getInstance().getAllAdvertisement());
```

`request.getSession()` with no argument (equivalent to `getSession(true)`) **creates a new session** if one does not exist. Because this new session is created during the same request lifecycle that just processed the user's logout, Tomcat will issue the **same JSESSIONID cookie value** (in some configurations) or, more critically, will establish a new live session object. This new session:

- Has no `sessCompId` attribute, so the auth gate will redirect requests to the expire page — but the session object itself exists in server memory.
- In certain Tomcat versions or with a sticky load balancer, the old JSESSIONID token may map to this new session, giving a prior session token unexpected post-logout validity.
- The `sessAds` attribute populated in this new session contains advertisement data retrieved from the database, confirming the session is genuinely live.

Additionally, the JSESSIONID cookie is never explicitly expired in the HTTP response. There is no call to:
```java
Cookie jsessionCookie = new Cookie("JSESSIONID", "");
jsessionCookie.setMaxAge(0);
response.addCookie(jsessionCookie);
```

The browser will continue to hold the old JSESSIONID cookie until the browser is closed, and the server will have a new session associated with it populated with advertisement data.

**Risk:**
- Session token not cleared from browser; an attacker who captured the JSESSIONID (e.g., via shoulder surfing, shared device, network sniffing) can continue to make requests with it after logout.
- The new post-logout session slightly expands the attack surface (live session object in container memory, advertisement data loaded unnecessarily).

**Recommendation:**
- Do not call `request.getSession()` (create-if-absent) after `invalidate()`. Use `request.getSession(false)` and check for null, or obtain a new session only once and store the reference.
- Explicitly expire the JSESSIONID cookie in the response immediately after `invalidate()`.
- If locale and advertisement data are needed for the login page, pass them as request attributes rather than session attributes on the logout response.

---

### HIGH: No CSRF Protection on Logout Endpoint

**File:** `src/main/java/com/action/LogoutAction.java` (all) / `src/main/webapp/WEB-INF/struts-config.xml` (lines 199-202)

**Description:**
The `logout.do` action accepts both GET and POST requests (Struts 1.x actions are reachable via both methods by default; `PreFlightActionServlet.doPost` delegates to `doGet`). There is no CSRF token validation anywhere in `LogoutAction` or in a surrounding filter.

A malicious page on any origin can force a victim's browser to submit a logout request:

```html
<!-- On attacker-controlled page -->
<img src="https://target.example.com/logout.do" />
```

or via JavaScript:

```javascript
fetch("https://target.example.com/logout.do", { method: "POST", credentials: "include" });
```

This allows an attacker to remotely log out any authenticated user who visits the attacker's page, constituting a denial-of-availability attack against the session.

While logout CSRF is generally lower severity than login CSRF, in industrial/fleet management contexts where operators rely on uninterrupted access to manage safety-critical equipment, forced logouts represent a meaningful operational risk.

**Risk:**
- Any authenticated user can be silently logged out by a third-party page they visit.
- In safety-critical operational scenarios (forklift management, fleet monitoring), forced logout may cause an operator to lose context at a critical moment.

**Recommendation:**
- Require a valid CSRF token (Synchronizer Token Pattern) on the logout request, validated in a Struts filter or in `LogoutAction` itself.
- As a minimum mitigation, verify that `Referer` or `Origin` headers match the application's own origin before processing logout.
- Alternatively, only accept POST requests for logout and include a hidden anti-CSRF token in the logout form.

---

### MEDIUM: Insecure Direct Use of User-Controlled `date` Parameter Without Strict Validation

**File:** `src/main/java/com/action/MailerAction.java` (lines 45-46, 53-57)

**Description:**
The `date` request parameter is read directly and passed to `DateUtil.parseDate()` with no length limit, character whitelist, or exception-specific handling:

```java
// MailerAction.java lines 45-46
String sDate = request.getParameter("date") == null ? "" : request.getParameter("date");

// lines 53-56
if (!sDate.equalsIgnoreCase("")) {
    dDate = DateUtil.parseDate(sDate);
    currentDate.setTime(dDate);
}
```

If `DateUtil.parseDate()` throws an exception on a malformed date string, the exception propagates upward and is either swallowed by the Struts exception handler (potentially leaking a stack trace to the client via the Struts error page) or causes the action to abort mid-processing. The value is also embedded into the JSON string sent to the internal API (line 102), providing a secondary injection vector into that API's input if `DateUtil.formatDate()` does not fully sanitise the parsed result.

Additionally, because `mailer.do` is unauthenticated, an attacker can supply arbitrary `date` values to probe the internal PDF API's behaviour across arbitrary date ranges, generating unwanted reports.

**Risk:**
- Possible information disclosure via exception/stack trace in error responses.
- Ability for unauthenticated users to generate reports for arbitrary historical date ranges.
- Secondary injection risk into the internal PDF generation API's JSON input.

**Recommendation:**
- Validate `date` against a strict regex (e.g., `\d{2}/\d{2}/\d{4}`) before parsing.
- Restrict allowable date range (e.g., within the last N days) to prevent arbitrary historical report generation.
- Wrap `DateUtil.parseDate()` in a try/catch and return HTTP 400 with a generic error message on invalid input.

---

### MEDIUM: JSESSIONID Cookie Missing HttpOnly and Secure Flags

**File:** `src/main/webapp/WEB-INF/web.xml` (lines 45-47)

**Description:**
The `<session-config>` block in `web.xml` specifies only a timeout and does not configure the JSESSIONID cookie's security attributes:

```xml
<session-config>
    <session-timeout>30</session-timeout>
</session-config>
```

There is no `<cookie-config>` element setting `<http-only>true</http-only>` or `<secure>true</secure>`. The web.xml uses the Servlet 2.4 schema (`web-app_2_4.xsd`), which predates the `<cookie-config>` element (introduced in Servlet 3.0). This means:

- **HttpOnly is not set:** The JSESSIONID is accessible to JavaScript. Any XSS vulnerability elsewhere in the application (of which several are known) can be used to steal the session cookie via `document.cookie`.
- **Secure is not set:** The JSESSIONID will be transmitted over plain HTTP connections. Given that `RuntimeConf.url` references `http://` (not `https://`), the application may be deployed without TLS, making session tokens trivially sniffable.

In `LogoutAction.java`, the code demonstrates awareness of cookies (it reads a `ckLanguage` cookie) but makes no attempt to set security flags on the JSESSIONID.

**Risk:**
- Session hijacking via XSS (HttpOnly not set) or network sniffing (Secure not set).
- Compounds the impact of any other XSS finding in the application.

**Recommendation:**
- Upgrade the `web.xml` to Servlet 3.0+ schema and add:
  ```xml
  <session-config>
      <session-timeout>30</session-timeout>
      <cookie-config>
          <http-only>true</http-only>
          <secure>true</secure>
      </cookie-config>
      <tracking-mode>COOKIE</tracking-mode>
  </session-config>
  ```
- Ensure the application is deployed behind TLS and enforce HTTPS redirects.
- As an interim measure for Tomcat, configure `useHttpOnly="true"` and `secure="true"` on the `<Context>` element in `context.xml`.

---

### INFO: mailSuccuess.jsp is Empty — No XSS Surface, But Response May Be Blank or Malformed

**File:** `src/main/webapp/html-jsp/mailSuccuess.jsp` (0 bytes)

**Description:**
The file `mailSuccuess.jsp` exists on disk but contains zero bytes. It is referenced by the `mailerDefinition` Tiles layout as the content fragment:

```xml
<!-- tiles-defs.xml line 158-160 -->
<definition name="mailerDefinition" extends="adminDefinition">
    <put name="content" value="/html-jsp/mailSuccuess.jsp"/>
</definition>
```

`mailerDefinition` extends `adminDefinition`, which uses the full admin template (`/includes/tilesTemplate.jsp`) including header, navigation, and footer. When `MailerAction` forwards to `success`, the Tiles engine will render the outer template with an empty content body. This means:

- There is currently **no XSS risk** from this file (no user-controlled data is rendered).
- However, the response delivered to the client after a successful mailer run is a full admin page shell with a blank content area, which may expose internal navigation structure (menu items, application name, version) to an unauthenticated caller (since `mailer.do` has no auth gate).
- The blank JSP may also indicate this page is unfinished and may be populated with dynamic content in future without being re-assessed for XSS.

**Risk:**
- Low immediate risk. Minor information disclosure (admin navigation structure visible to unauthenticated callers).
- Future risk if content is added without XSS review.

**Recommendation:**
- Either populate the JSP with a static success message containing no user-controlled data, or redirect to a non-admin page after the mailer action completes.
- If the mailer is restricted to server-side invocation (cron), consider returning a plain-text or JSON response rather than rendering an HTML admin template.
- Flag this file for re-audit if content is added in future.

---

## Summary of Findings

| # | Severity | Title | File |
|---|----------|-------|------|
| 1 | CRITICAL | Unauthenticated Access to Email Dispatch Endpoint | `PreFlightActionServlet.java:105`, `MailerAction.java` |
| 2 | CRITICAL | SQL Injection via User-Controlled `frequency` Parameter | `SubscriptionDAO.java:38-43`, `MailerAction.java:47-48` |
| 3 | HIGH | Hardcoded Admin Credentials in Source Code | `MailerAction.java:102` |
| 4 | HIGH | Session Re-Creation After Invalidation (Post-Logout Session) | `LogoutAction.java:44,47` |
| 5 | HIGH | No CSRF Protection on Logout Endpoint | `LogoutAction.java`, `struts-config.xml:199` |
| 6 | MEDIUM | Unvalidated User-Controlled `date` Parameter | `MailerAction.java:45-57` |
| 7 | MEDIUM | JSESSIONID Cookie Missing HttpOnly and Secure Flags | `web.xml:45-47` |
| 8 | INFO | mailSuccuess.jsp is Empty — Blank Response to Unauthenticated Caller | `mailSuccuess.jsp` |

---

`CRITICAL: 2 / HIGH: 3 / MEDIUM: 2 / LOW: 0 / INFO: 1`
