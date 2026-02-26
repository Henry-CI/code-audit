# Security Audit Report — Pass 1
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Date:** 2026-02-26
**Auditor:** Automated pass via Claude Code
**Scope:** RegisterAction, RegisterActionForm, register.jsp, ReportAPI, ResetPasswordAction, ResetPassActionForm, resetpass.jsp, GoResetPassAction, DriverDAO (methods called by in-scope actions), PreFlightActionServlet, HttpDownloadUtility, RuntimeConf

---

## Findings

---

### CRITICAL: SQL Injection via `getDriverByNm` — user-controlled name values interpolated into raw SQL

**File:** `src/main/java/com/dao/DriverDAO.java` (lines 226–228)

**Description:**
`RegisterAction.execute()` calls `driverDao.getDriverByNm(sessCompId, registerActionForm.getFirstName(), registerActionForm.getLastName(), true)` at line 66 of `RegisterAction.java` after a successful driver save. Inside `DriverDAO.getDriverByNm`, `firstName` and `lastName` (raw user input from the form) are concatenated directly into a SQL string using a plain `Statement`, not a `PreparedStatement`:

```java
// DriverDAO.java line 226-228
String sql = "select id,first_name,last_name,active,comp_id from driver " +
    "where trim(both ' ' from first_name) ilike trim(both ' ' from '" + firstName + "')  " +
    " and trim(both ' ' from last_name) ilike trim(both ' ' from '" + lastName + "')" +
    " and comp_id = " + compId;
```

The source FIXME comment at line 225 explicitly acknowledges this: *"Also work with prepared statement to prevent SQL injection."* The same pattern is repeated in `getDriverByFullNm` at line 264:

```java
String sql = "select id,first_name,last_name,active,comp_id,licno from driver " +
    "where first_name||' '||last_name ilike '" + fullName + "' and comp_id = " + compId;
```

A user who submits `firstName` as `' OR '1'='1` or a time-based payload like `' OR pg_sleep(5)--` will cause the query to behave unexpectedly. The `ilike` wildcard context allows UNION-based extraction as well because the `ILIKE` expression can be escaped with `%27` and the SQL can be terminated and new queries injected.

Additionally `compId` is concatenated (not parameterised) in the `comp_id = " + compId` fragment. While `compId` originates from the session in this code path, in `getDriverByFullNm` it also travels through callers that may not sanitise it.

**Risk:**
Full SQL injection in a PostgreSQL database. Impact includes: arbitrary data exfiltration from all tables accessible to the application DB user, authentication bypass in other contexts where these methods are reused, and potentially OS-level command execution via PostgreSQL `COPY TO/FROM PROGRAM` if the DB user has sufficient privilege.

**Recommendation:**
Replace `Statement` with `PreparedStatement` for all dynamic queries. The existing `DBUtil.queryForObject` helper (which takes a `PreparedStatementHandler` lambda) is already used correctly elsewhere in the same class; apply the same pattern here:

```java
// Correct pattern already used in checkDriverByNm (lines 185-193)
Optional<Long> count = DBUtil.queryForObject(QUERY_DRIVER_BY_NAME, (stmt) -> {
    stmt.setString(1, firstName);
    stmt.setString(2, lastName);
    stmt.setLong(3, Long.parseLong(compId));
}, (rs) -> rs.getLong(1));
```

---

### CRITICAL: Hardcoded API Authentication Token in Source Code

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (line 105)

**Description:**
A static `X-AUTH-TOKEN` value is hardcoded directly in the source:

```java
con.setRequestProperty("X-AUTH-TOKEN", "noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE");
```

This token authenticates outbound API calls to the report-generation backend at `http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/` (RuntimeConf.java line 60). Any developer with read access to the repository — including build pipeline workers, any future contractor, or an attacker who gains read access to the repository — immediately has a valid credential for that external API endpoint.

**Risk:**
Exposure of a long-lived credential that authenticates calls to an AWS-hosted backend. If the backend API can be called directly (it lacks its own network-level restriction), an attacker can generate arbitrary PDF reports for any company, potentially exfiltrating sensitive operational data. The hardcoded token also cannot be rotated without a code change and redeployment.

**Recommendation:**
Move the token to an environment variable or a secrets store (e.g., AWS Secrets Manager, Vault, or a properties file that is excluded from version control). Read it at startup:

```java
con.setRequestProperty("X-AUTH-TOKEN", System.getenv("REPORT_API_TOKEN"));
```

Rotate the token immediately now that it is known to be committed to version history.

---

### CRITICAL: Plain HTTP Used for External API Communication — Credential and Data in Transit Exposed

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 91–99) and `src/main/java/com/util/RuntimeConf.java` (line 60)

**Description:**
The report API endpoint is configured as a plain HTTP URL:

```java
// RuntimeConf.java line 60
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/";
```

And `HttpDownloadUtility.sendPost` opens a plain `HttpURLConnection`, with commented-out code showing HTTPS was considered but intentionally bypassed:

```java
// HttpDownloadUtility.java lines 98-99
//  Secure connection
//  HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
HttpURLConnection con = (HttpURLConnection)obj.openConnection();
```

The `X-AUTH-TOKEN` header and the full JSON POST body (which includes company ID, date filters, and report data) are transmitted in cleartext. Any network device between the Tomcat server and the AWS endpoint (corporate proxy, cloud transit) can intercept both the credential and the returned PDF content.

**Risk:**
Man-in-the-middle interception of the auth token (enabling replay attacks), interception of exported report data (confidentiality breach), and potential injection of crafted PDF responses that are then emailed to users.

**Recommendation:**
Restore the `HttpsURLConnection` path, enforce certificate validation (do not disable trust managers), and update `RuntimeConf.APIURL` to use `https://`. Additionally enforce TLS 1.2 or higher via `SSLContext`.

---

### HIGH: Missing CSRF Protection on Password Reset Form

**File:** `src/main/webapp/html-jsp/resetpass.jsp` (lines 16–33) and `src/main/java/com/action/ResetPasswordAction.java`

**Description:**
The password reset form uses a plain HTML `<form>` (not Struts `<html:form>`) with no CSRF token:

```html
<!-- resetpass.jsp line 16 -->
<form method="post" action="resetpass.do" id="resetpassForm">
    <input name="code" type="text" class="input" />
    <input name="npass" type="password" class="input" />
    <input name="rnpass" type="password" class="input" />
    <input type="hidden" name="username" value="<%=username%>">
</form>
```

`ResetPasswordAction` (which is on the `excludeFromFilter` whitelist — line 110 of PreFlightActionServlet — and therefore accessible pre-authentication) reads all parameters directly from `request.getParameter()` without any token check:

```java
// ResetPasswordAction.java lines 30-32
String username = request.getParameter("username") == null ? "" : request.getParameter("username");
String password = request.getParameter("npass") == null ? "" : request.getParameter("npass");
String code     = request.getParameter("code") == null ? "" : request.getParameter("code");
```

Struts 1.3.x has no built-in CSRF protection. There is no synchroniser token, no `SameSite` cookie attribute check, and no `Origin`/`Referer` validation in this action. An attacker who knows (or can guess/obtain) a valid verification code and target username can craft a cross-site request from any origin to reset the victim's password.

**Risk:**
A malicious page visited by any user who has recently requested a password reset verification code can silently submit the reset form. Combined with the username-in-hidden-field pattern described below, the attacker controls the target account.

**Recommendation:**
Generate a per-session CSRF synchroniser token (e.g., via `TokenProcessor.getInstance().generateToken(request)`) before rendering the page and validate it in `ResetPasswordAction` with `TokenProcessor.getInstance().isTokenValid(request, true)`. Alternatively, implement a CSP `Origin` header check. In Struts 1.x the recommended approach is to use `html:form` with a token stored in the session.

---

### HIGH: Username Reflected Unescaped into Hidden Field — Reflected XSS

**File:** `src/main/webapp/html-jsp/resetpass.jsp` (line 32)

**Description:**
The `username` URL parameter is read and immediately reflected into a hidden form field with no encoding:

```jsp
<%  String username = request.getParameter("username") == null ? "" : request.getParameter("username"); %>
...
<input type="hidden" name="username" value="<%=username%>">
```

A request to `resetpass.do?username="><script>alert(1)</script>` would inject the script tag into the rendered page. Because this endpoint is pre-auth accessible (it is on the `excludeFromFilter` exclusion list at PreFlightActionServlet line 110), no session is required to trigger this — it can be sent as a link to any user (including unauthenticated users).

**Risk:**
Reflected XSS allowing an attacker to execute arbitrary JavaScript in the victim's browser on the application's origin. Exploitable via phishing: send a victim the URL `https://app/resetpass.do?username=<payload>` and their session cookies, localStorage tokens, and page content are accessible to the attacker's script. On a pre-auth page this also means it can be used without any prior account access.

**Recommendation:**
Encode output before insertion into HTML. Use `ESAPI.encoder().encodeForHTMLAttribute(username)` or, as the simplest fix within the JSP, use the JSTL `<c:out>` tag or wrap with `fn:escapeXml()`:

```jsp
<input type="hidden" name="username" value="<c:out value='${param.username}'/>">
```

Avoid scriptlet-style `<%= %>` output in JSPs entirely; use EL with auto-escaping or explicit encoding.

---

### HIGH: Username Enumeration via Distinct Error Messages / Cognito Response Leakage

**File:** `src/main/java/com/action/ResetPasswordAction.java` (lines 46–53) and `src/main/java/com/action/GoResetPassAction.java`

**Description:**
`ResetPasswordAction` passes the raw Cognito error message directly to the user as an action error:

```java
// ResetPasswordAction.java lines 48-52
String errormsg = passwordResponse.getMessage();
ActionErrors errors = new ActionErrors();
ActionMessage msg = new ActionMessage("error.incorrect.reset.cognito", errormsg);
errors.add("infoerror", msg);
saveErrors(request, errors);
```

AWS Cognito returns distinct error messages that differ based on whether a username exists: `UserNotFoundException` for unknown users vs. `CodeMismatchException` or `ExpiredCodeException` for known users. By surfacing the raw Cognito `message` field directly, an attacker can determine whether a given username is a registered account by submitting a dummy verification code and observing the error:

- Unknown user: `"Username/client id combination not found."` (Cognito `UserNotFoundException`)
- Known user with wrong code: `"Invalid verification code provided, please try again."` (Cognito `CodeMismatchException`)

`GoResetPassAction` also accepts a `username` parameter from user input (line 24) with no rate limiting and calls `restClientServce.resetPassword(passwordRequest)`, triggering a password reset email send for any supplied username. The response branching (line 36-42) then implicitly confirms whether the account exists.

**Risk:**
An attacker can enumerate all valid usernames by scripting requests to `resetpass.do` or `goResetPass.do?action=reset&username=<candidate>`. This list can be used for credential stuffing or targeted phishing.

**Recommendation:**
Map all Cognito error types to a single generic message such as `"If an account with that username exists, a reset code has been sent."` Never expose raw Cognito error text to the user. Implement rate limiting on both `goResetPass.do` and `resetpass.do` (e.g., via a Servlet filter tracking IP-based request rate).

---

### HIGH: `register.do` is NOT Pre-Auth Excluded — but RegisterAction Directly Dereferences Session Without Null Check

**File:** `src/main/java/com/action/RegisterAction.java` (lines 30–34) and `src/main/java/com/actionservlet/PreFlightActionServlet.java` (lines 98–114)

**Description:**
`register.do` is NOT present in the `excludeFromFilter` list in `PreFlightActionServlet`. The exclusion list includes `adminRegister.do` and `switchRegister.do` but not `register.do`. This means the auth gate (`sessCompId != null`) does apply to `register.do`.

However, `RegisterAction.execute()` calls `request.getSession()` (creates-if-absent, not `getSession(false)`) on line 32 while simultaneously calling `getSession(false)` on line 30:

```java
// RegisterAction.java lines 30-34
HttpSession session = request.getSession(false);           // may return null
RegisterActionForm registerActionForm = (RegisterActionForm) actionForm;
String sessCompId = (String) request.getSession().getAttribute("sessCompId"); // creates new session if null
ArrayList<CompanyBean> sessArrComp = (ArrayList<CompanyBean>) session.getAttribute("sessArrComp"); // NPE if session was null
String template = (String) sessArrComp.get(0).getTemplate(); // NPE if sessArrComp is null
```

If a request somehow reaches `RegisterAction` with no active session (e.g., a race condition during session expiry or a direct URL hit that bypasses the filter), `session` on line 30 is `null`. The code then calls `session.getAttribute("sessArrComp")` on line 33, throwing a `NullPointerException`. More critically, `sessArrComp.get(0)` at line 34 will throw `NullPointerException` or `IndexOutOfBoundsException` if the session attribute was not populated correctly, causing an unhandled exception that may reveal stack traces.

Additionally there is a logic inconsistency: line 47 sets `driverbean.setComp_id(sessCompId)` where `sessCompId` was fetched via `request.getSession()` (a new empty session), not from the validated `session` object, so in an edge-case bypass `sessCompId` would be an empty string and the driver would be inserted with a null/empty `comp_id`.

**Risk:**
NullPointerException leading to an HTTP 500 error and potential stack trace disclosure. In a bypass edge-case, a driver record could be inserted with no company association, corrupting data integrity.

**Recommendation:**
Consistently use `request.getSession(false)` for all session accesses and add an explicit null-guard at the top of `execute()`:

```java
HttpSession session = request.getSession(false);
if (session == null || session.getAttribute("sessCompId") == null) {
    return mapping.findForward("sessionExpired");
}
```

---

### HIGH: Unparameterised `compId` and `timezone` Concatenation in DriverDAO — SQL Injection via Session Value

**File:** `src/main/java/com/dao/DriverDAO.java` (lines 749, 783)

**Description:**
Two additional methods concatenate values directly into SQL strings. `getTotalDriverByID` (line 749):

```java
String sql = "select count(p.id) from permission as p inner join driver as d on p.driver_id = d.id "
    + "where p.comp_id = " + id + " and timezone('" + timezone + "', p.updatedat)::DATE = current_date::DATE ";
```

`getDriverName` (line 783):

```java
String sql = "select first_name||' '||last_name as name from driver where id=" + id;
```

While `id` and `timezone` originate from session/database values in most current callers, they are method parameters and their data-flow should not be trusted. If any caller passes user-controlled or partially-user-controlled data (e.g., via a timezone preference stored by the user), these become injection vectors. The `timezone` parameter in particular is a string and is concatenated inside single-quote delimiters in a PostgreSQL `timezone()` call; a value of `Australia/Sydney') OR 1=1--` would alter query semantics.

**Risk:**
SQL injection. Though currently the callers pass session-sourced values, the unparameterised pattern is fragile and a single refactor adding a user-controlled timezone setting would introduce an exploitable injection.

**Recommendation:**
Use parameterised queries throughout `DriverDAO`. Replace all `Statement.createStatement` / string concatenation patterns with `PreparedStatement` and `setString`/`setLong`.

---

### MEDIUM: No Rate Limiting or Account Lockout on Password Reset Initiation

**File:** `src/main/java/com/action/GoResetPassAction.java` (lines 27–46) and `src/main/java/com/actionservlet/PreFlightActionServlet.java` (line 111)

**Description:**
`goResetPass.do` is excluded from the auth filter and accepts a `username` and `action=reset` parameter combination. It calls `restClientServce.resetPassword(passwordRequest)` unconditionally with the supplied `username` with no rate limiting, no CAPTCHA, and no request throttling in the application layer:

```java
// GoResetPassAction.java lines 33-42
RestClientService restClientServce = new RestClientService();
PasswordRequest passwordRequest = PasswordRequest.builder()
    .username(username).accessToken(accessToken).build();
PasswordResponse passwordResponse = restClientServce.resetPassword(passwordRequest);
if (passwordResponse.getCode().equals(RuntimeConf.HTTP_OK)) {
    return mapping.findForward("reset");
} else {
    return mapping.findForward("getcode");
}
```

An attacker can send thousands of reset requests per second for a valid username, flooding the target user's inbox with reset code emails (email bombing / denial-of-service against the user). If Cognito enforces its own rate limits the application does not surface this gracefully.

**Risk:**
Email-based denial of service against targeted users. Harassment and account disruption.

**Recommendation:**
Implement a Servlet filter that rate-limits password reset requests per IP address (e.g., maximum 5 requests per 10 minutes per IP). Consider adding a CAPTCHA to the reset initiation page. Return a consistent response whether or not the account exists.

---

### MEDIUM: No Input Validation on `expirydt` — Potential Date Injection / Malformed Data

**File:** `src/main/java/com/actionform/RegisterActionForm.java` (lines 79–101) and `src/main/java/com/dao/DriverDAO.java` (lines 562–565)

**Description:**
The `validate()` method in `RegisterActionForm` checks only for blank/null values on `firstName`, `lastName`, `licence_no`, and `expirydt`. It does not validate the format or content of `expirydt`:

```java
// RegisterActionForm.java lines 94-97
if (expirydt == null) {
    ActionMessage message = new ActionMessage("error.expDate");
    errors.add("expirydt", message);
}
```

The string is passed directly to `DateUtil.stringToSQLDate(driverbean.getExpirydt(), dateFormat)` inside a prepared-statement binding (safe from SQL injection), but an invalid date string will throw a `ParseException` or `IllegalArgumentException` that propagates up to `RegisterAction.execute()`. The `execute()` method does not catch this exception; the Struts global exception handler maps `java.lang.Exception` to an `errorDefinition` tile, which may expose an application error page. `licence_no` and `veh_id` / `attachment` are also unrestricted strings with no length or format checks.

**Risk:**
Unhandled exception leading to a 500 error page with stack trace disclosure. Malformed data persisted to the database if the exception is swallowed somewhere in the chain. Potential for oversized inputs to cause out-of-memory issues or database column overflow errors.

**Recommendation:**
Validate the `expirydt` field format (e.g., `dd/MM/yyyy`) in `RegisterActionForm.validate()` using a try/catch around `DateFormat.parse()`. Validate `licence_no` for maximum length and acceptable character set. Validate `veh_id` and `attachment` as numeric identifiers only.

---

### MEDIUM: `saveDriverInfo` Prepared Statement Parameter Count Mismatch — Incorrect `id` Binding

**File:** `src/main/java/com/dao/DriverDAO.java` (lines 57–58, 547–556)

**Description:**
`INSERT_DRIVER_INFO_SQL` declares 9 columns and 9 placeholders:

```java
private static final String INSERT_DRIVER_INFO_SQL =
    "insert into driver (id, first_name,last_name,licno,expirydt,phone,location,department,comp_id) values (?,?,?,?,?,?,?,?,?)";
```

But the lambda binding in `saveDriverInfo` (for the `driverbean.getId() == null` branch) sets only parameters 1–8:

```java
rowUpdated = DBUtil.updateObject(INSERT_DRIVER_INFO_SQL, (ps) -> {
    ps.setString(1, driverbean.getFirst_name());   // binds to 'id' column — WRONG
    ps.setString(2, driverbean.getLast_name());    // binds to 'first_name'
    ps.setNull(3, Types.VARCHAR);                  // binds to 'last_name'
    ps.setNull(4, Types.DATE);                     // binds to 'licno'
    ps.setString(5, driverbean.getPhone());        // binds to 'expirydt'
    ps.setString(6, driverbean.getLocation());     // binds to 'phone'
    ps.setString(7, driverbean.getDepartment());   // binds to 'location'
    ps.setString(8, driverbean.getComp_id());      // binds to 'department'
    // parameter 9 (comp_id) is NEVER SET
});
```

There is a complete column/parameter alignment error: `first_name` is bound to the `id` placeholder, and `comp_id` (9th column) has no binding. At runtime JDBC will throw a `SQLException: No value specified for parameter 9` unless the driver supplies a default — meaning either every new driver insertion fails silently (the `catch` in `DBUtil.updateObject` calls `e.printStackTrace()` only and returns `-1`) or, if the database `id` column is a sequence/SERIAL, the statement itself is structurally wrong with all values shifted.

The actual insert that does use correctly parameterised statements is a different code block (lines 511–519) that inserts into different columns. This `saveDriverInfo` path is what `RegisterAction` calls.

**Risk:**
Silent insert failure: new driver registrations through the kiosk flow may fail without returning an error to the user if `DBUtil.updateObject` returns `-1` but `RegisterAction` only checks the boolean return of `saveDriverInfo > 0`. Data integrity issue: driver records may be inserted with incorrect field values if the database supplies a default for the missing parameter.

**Recommendation:**
Fix the parameter binding to match the SQL column order exactly:

```java
ps.setLong(1, /* generated or next-val id */);
ps.setString(2, driverbean.getFirst_name());
ps.setString(3, driverbean.getLast_name());
ps.setString(4, driverbean.getLicno());
// ... etc.
ps.setString(9, driverbean.getComp_id());
```

Alternatively, remove `id` from the INSERT column list if it is a `SERIAL`/auto-increment column and shift all bindings accordingly.

---

### MEDIUM: Verification Code Transmitted in GET Parameter — Logged and Cached

**File:** `src/main/webapp/html-jsp/resetpass.jsp` (line 18)

**Description:**
The "Resend verification code" link navigates to `goResetPass.do?action=getcode` with no `username` parameter. However, the overall password-reset flow involves the `username` being passed as a URL query parameter throughout (visible in the hidden field `value="<%=username%>"` which is populated from `request.getParameter("username")`). This means the username value is exposed in:

1. Browser history
2. Server access logs
3. HTTP `Referer` headers on any subsequent navigation to a third-party resource loaded by the page

While the verification code itself is POSTed, the `username` value is persistently exposed in URLs throughout the flow.

**Risk:**
Username disclosure via server access logs and browser history. Facilitates account enumeration by log analysis.

**Recommendation:**
Carry the username in the session rather than as a URL parameter. Set it during the `getcode` step and retrieve it from the session in `ResetPasswordAction`, removing it from the request parameter entirely.

---

### MEDIUM: No Validation of `npass` Complexity — Any Password Accepted by Application Layer

**File:** `src/main/webapp/html-jsp/resetpass.jsp` (lines 43–67)

**Description:**
The client-side `fnSubmit()` function only checks that `npass` is non-empty and matches `rnpass`. There is no server-side password complexity validation in `ResetPasswordAction`:

```javascript
// resetpass.jsp lines 48-66
if (npass == "") {
    swal("Error", "New Password is required", "error");
} else if (rnpass == "") {
    swal("Error", "Please Re-type New Password", "error");
} else if (npass != rnpass) {
    swal("Error", "Password is not matched", "error");
} else {
    $('#resetpassForm').submit();
}
```

`ResetPasswordAction.execute()` passes `password` directly to Cognito without any application-layer complexity check. If Cognito's password policy is misconfigured or changed, single-character or common passwords would be accepted.

**Risk:**
Users may reset to weak passwords (e.g., a single character), degrading account security. Client-side-only validation is trivially bypassed by sending a direct POST to `resetpass.do`.

**Recommendation:**
Add server-side password complexity validation in `ResetPasswordAction` before calling Cognito — enforce minimum length (12+ characters recommended), mixed character classes, and a check against a common-password list. Do not rely solely on client-side JavaScript or Cognito's default policy.

---

### MEDIUM: `register.jsp` Uses Unescaped `<bean:write>` for `veh_id` and `attachment` — Potential Stored XSS

**File:** `src/main/webapp/html-jsp/register.jsp` (lines 9–13)

**Description:**
The JSP renders two hidden fields using `<bean:write>` with request-scope attributes:

```jsp
<input type="hidden" name="veh_id"
    value='<bean:write name="veh_id"></bean:write>'></input>
<input type="hidden" name="attachment"
    value='<bean:write name="attachment"></bean:write>'></input>
```

`<bean:write>` does NOT HTML-encode output by default in Struts 1.x unless `filter="true"` is explicitly set. These attributes are populated from `request.setAttribute("veh_id", registerActionForm.getVeh_id())` and `request.setAttribute("attachment", registerActionForm.getAttachment())` which come directly from the form POST without sanitisation (see `RegisterActionForm`, `RegisterAction` lines 54–55). If a prior action in the workflow (e.g., `SearchAction`) sets `veh_id` from a database value that itself contains unescaped HTML characters, the content would be reflected into the page.

While the primary data flow appears to originate from the application database (not directly from user text input), any stored XSS vector in the `veh_id` or `attachment` columns would flow into this page unescaped.

**Risk:**
Stored XSS if `veh_id` or `attachment` values in the database contain HTML/JavaScript characters. Session hijacking, credential theft.

**Recommendation:**
Add `filter="true"` to all `<bean:write>` tags:

```jsp
<bean:write name="veh_id" filter="true"/>
```

Apply this consistently to all `<bean:write>` usages across the application.

---

### LOW: `ResetPassActionForm.validate()` Will Throw `NullPointerException` if Fields Are Null

**File:** `src/main/java/com/actionform/ResetPassActionForm.java` (lines 49–58)

**Description:**
The `validate()` method calls `name.equalsIgnoreCase("")` and `email.equalsIgnoreCase("")` without null-checking the fields first:

```java
if (name.equalsIgnoreCase("")) {   // throws NPE if name == null
    ...
}
if (email.equalsIgnoreCase(""))  { // throws NPE if email == null
    ...
}
```

The fields `name` and `email` are initialised to `null` (lines 13–14). If the form is submitted with missing `name` or `email` parameters (e.g., a partial form submission or an automated request), the `validate()` method throws `NullPointerException` instead of returning a validation error, which will propagate through Struts and result in a 500 error with potential stack trace exposure.

Note: This form (`resetPassActionForm`) is mapped in `struts-config.xml` but no action uses it as the `name` attribute — the `goResetPass` and `resetpass` action mappings have no `name` attribute — so in practice this `validate()` method may never be called. However this is itself a symptom of dead/disconnected code that represents technical debt.

**Risk:**
NullPointerException resulting in HTTP 500 and possible stack trace disclosure if the form is ever wired to an action. Dead validation code provides false confidence that the form is protected.

**Recommendation:**
Use `"".equalsIgnoreCase(name)` (reversing the operand) or add an explicit null check first: `if (name == null || name.equalsIgnoreCase(""))`. Wire the form bean to its action in `struts-config.xml` or delete the form class if it is not in use.

---

### LOW: Same Error Key Used Twice in `RegisterActionForm.validate()` — Validation Error Silently Dropped

**File:** `src/main/java/com/actionform/RegisterActionForm.java` (lines 86–93)

**Description:**
Both the `lastName` validation and the `licence_no` validation add errors under the key `"lastName"`:

```java
// RegisterActionForm.java lines 86-93
if (lastName.equalsIgnoreCase("")) {
    errors.add("lastName", message);   // key: "lastName"
}
if (licence_no.equalsIgnoreCase("")) {
    errors.add("lastName", message);   // ALSO key: "lastName" — should be "licence_no"
}
```

In Struts 1.x `ActionErrors`, adding two messages under the same key is valid and both will be displayed, but it means that `<html:errors property="licence_no"/>` in a JSP will never render the licence error since the key is wrong. This is a functional bug but also a security concern: if client-side validation is bypassed and the licence field is blank, the user might not see the correct error message, potentially confusing the UI state in a way an attacker could exploit.

**Risk:**
Licence validation error appears under the wrong field label, potentially hiding the error from the user. Low severity security impact.

**Recommendation:**
Change the key for the licence validation to `"licence_no"`:

```java
errors.add("licence_no", message);
```

---

### LOW: `ResetPassActionForm` Contains Dead Security-Question Fields Never Used by the Cognito Flow

**File:** `src/main/java/com/actionform/ResetPassActionForm.java` (lines 12–45)

**Description:**
`ResetPassActionForm` declares `question` and `answer` fields:

```java
private String question = null;
private String answer   = null;
```

These suggest a legacy password-reset mechanism based on security questions (knowledge-based authentication), which is now superseded by the Cognito verification-code flow. The fields are not used by any current action. If this code were ever re-activated or wired in, it would represent a weak authentication mechanism (security questions are generally considered broken).

**Risk:**
Dead code that, if resurrected, would introduce a weak authentication mechanism. The presence of these fields may mislead developers into thinking a KBA flow is available.

**Recommendation:**
Remove the `question` and `answer` fields and their getters/setters from `ResetPassActionForm`. If historical KBA data exists in the database, consider whether it should be purged.

---

### INFO: Hardcoded Internal Credentials and URLs in `RuntimeConf.java`

**File:** `src/main/java/com/util/RuntimeConf.java` (lines 8, 16, 58, 60)

**Description:**
`RuntimeConf.java` contains several hardcoded values that should be externalised:

- `url = "http://prestart.collectiveintelligence.com.au/"` — internal service URL over plain HTTP
- `RECEIVER_EMAIL = "hui@ciifm.com"` — hardcoded email address (personally identifiable, potential target)
- `debugEmailRecipet = "hui@collectiveintelligence.com.au"` — debug email address committed to source
- `APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"` — direct EC2 IP/hostname over HTTP
- `cloudImageURL = "https://s3.amazonaws.com/forkliftiq360/image/"` — S3 bucket name disclosed

The S3 bucket name `forkliftiq360` is directly exposed, making it trivial to enumerate public objects in that bucket.

**Risk:**
Information disclosure. These values expose internal infrastructure topology, email addresses, and service endpoints. The S3 bucket name can be used to attempt public object enumeration. The EC2 hostname may be used to directly probe the report API.

**Recommendation:**
Move all environment-specific configuration to an externally managed properties file (loaded at startup, excluded from version control) or to environment variables. Implement a secrets management solution for any credentials. Immediately check the S3 bucket `forkliftiq360` for public access settings and restrict accordingly.

---

### INFO: `HttpDownloadUtility.saveFilePath` is a Static Field — Race Condition in Concurrent Requests

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 27, 160, 186–192)

**Description:**
`saveFilePath` is a `private static String` that is written by `sendPost()` and read by `getSaveFilePath()`:

```java
private static String saveFilePath = "";
...
saveFilePath = saveDir + fileName + RuntimeConf.file_type;
...
public static String getSaveFilePath() {
    return saveFilePath;
}
```

In a multithreaded Tomcat environment, concurrent report generation requests will overwrite this shared static field, causing one request to read the file path written by another request. The caller (`ReportAPI.downloadPDF()`) calls `sendPost()` and then immediately calls `getSaveFilePath()`, but under concurrent load these two calls can be interleaved with another thread's `sendPost()` call.

**Risk:**
Under concurrent usage: users may receive another user's report PDF, leading to confidentiality breach (one company's report emailed to another company's users). This is a data leakage vulnerability under load.

**Recommendation:**
Return the `saveFilePath` directly from `sendPost()` rather than storing it as a static field. Alternatively use a thread-local variable. The `downloadPDF()` and `sendPost()` methods should be instance methods (not static), and the path should be an instance field of `ReportAPI`.

---

## Summary

| Severity | Count | Findings |
|----------|-------|----------|
| CRITICAL | 3     | SQL injection in `getDriverByNm`/`getDriverByFullNm`; Hardcoded API auth token; Plain HTTP for external API with token in transit |
| HIGH     | 4     | No CSRF on password reset form; Reflected XSS in `resetpass.jsp`; Username enumeration via Cognito error passthrough; NullPointerException / auth bypass edge-case in `RegisterAction` |
| MEDIUM   | 5     | No rate limiting on reset initiation; No server-side password complexity validation; Unescaped `<bean:write>` XSS in `register.jsp`; `saveDriverInfo` parameter/column alignment bug; Username in URL throughout reset flow |
| LOW      | 3     | `ResetPassActionForm.validate()` NPE on null fields; Wrong error key for licence validation; Dead security-question fields in `ResetPassActionForm` |
| INFO     | 2     | Hardcoded infrastructure details in `RuntimeConf.java`; Static `saveFilePath` race condition in `HttpDownloadUtility` |

**CRITICAL: 3 / HIGH: 4 / MEDIUM: 5 / LOW: 3 / INFO: 2**
