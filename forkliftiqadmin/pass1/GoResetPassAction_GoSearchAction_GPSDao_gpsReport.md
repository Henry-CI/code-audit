# Security Audit Report — Pass 1
**Application:** forkliftiqadmin (internal name: "pandora")
**Framework:** Apache Struts 1.3.10 on Tomcat
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated Security Review

**Files audited:**
- `src/main/java/com/action/GoResetPassAction.java`
- `src/main/java/com/action/GoSearchAction.java`
- `src/main/java/com/dao/GPSDao.java`
- `src/main/webapp/html-jsp/reports/gpsReport.jsp`

**Supporting files reviewed for context:**
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/java/com/action/GetAjaxAction.java`
- `src/main/java/com/action/GPSReportAction.java`
- `src/main/java/com/service/RestClientService.java`
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/WEB-INF/tiles-defs.xml`
- `src/main/webapp/gps/unit.gps.jsp`
- `src/main/java/com/dao/UnitDAO.java` (partial)

---

## Findings

---

### CRITICAL: SQL Injection via Statement + String Concatenation — getGPSLocations

**File:** `GPSDao.java` (lines 85–88)
**Description:**
The `getGPSLocations` method constructs a SQL query by directly concatenating attacker-controlled values from the `unitList` parameter array into a `Statement.executeQuery()` call. There is no input validation, type-checking, or use of `PreparedStatement`.

```java
String sql = "select u.id,u.name,g.longitude,g.latitude,g.gps_time,g.current_location from gps as g"
         + " inner join unit as u on u.id=g.unit_id"
         + " where g.unit_id=" + unitList[i] +""
         + " order by g.gps_time desc limit 1";

stmt = conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY);
rs = stmt.executeQuery(sql);
```

The values in `unitList` originate from request parameters (confirmed by tracing through `GetAjaxAction.java` line 45: `String[] unit = request.getParameterValues("unit")`). An attacker can supply a payload such as `1 UNION SELECT username,password,null,null,null,null FROM users-- ` to extract arbitrary data from any table the database user can access.

Additionally, the full constructed SQL string is written to the application log at `INFO` level (line 90: `log.info(sql)`), which means a successful injection attempt is fully logged and visible to anyone with log access, but also that the log can be used to confirm injection success.

**Risk:**
Complete database compromise. An authenticated attacker can read, and potentially write or drop, any data in the database. Given the multi-tenant nature of the application, this would expose data for all companies, not just the attacker's own tenant.

**Recommendation:**
Replace `Statement` with `PreparedStatement` using a `?` placeholder for `unit_id`. Validate that each element of `unitList` is a non-negative integer before use. Remove the `log.info(sql)` call, or at minimum ensure it never logs concatenated user input. Example fix:
```java
String sql = "select u.id,u.name,g.longitude,g.latitude,g.gps_time,g.current_location"
           + " from gps as g inner join unit as u on u.id=g.unit_id"
           + " where g.unit_id=? order by g.gps_time desc limit 1";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setInt(1, Integer.parseInt(unitList[i]));
```

---

### CRITICAL: SQL Injection via Statement + String Concatenation — getUnitById

**File:** `GPSDao.java` (lines 136–139)
**Description:**
The `getUnitById` method in `GPSDao` builds a SQL query by directly appending the `id` parameter string using a raw `Statement`, with no parameterisation:

```java
String sql = "select unit.id,unit.name,location,department,type_id,active,manu_id,size," +
             "fuel_type_id,hourmeter,serial_no,type.name,fuel_type.name,comp_id,unit.mac_address" +
             " from unit left outer join type on type.id = unit.type_id" +
             " left outer join fuel_type on fuel_type.id = unit.fuel_type_id" +
             " where unit.id=" + id;
log.info(sql);
rs = stmt.executeQuery(sql);
```

The `id` value is passed from callers (e.g., in the GPS and unit management flows). An injected `id` value such as `1 OR 1=1` or `1 UNION SELECT ...` allows arbitrary read access. The MAC address (`unit.mac_address`) is returned, which is a hardware identifier that could further aid device-level attacks. Again, the raw SQL is logged.

Note: `UnitDAO.getUnitById(String id)` (line 288–291) is a safer duplicate method that uses a parameterised query builder. This `GPSDao.getUnitById` is an older, vulnerable duplicate that should be removed entirely.

**Risk:**
Full SQL injection as per the previous finding. The response also leaks hardware identifiers (MAC addresses).

**Recommendation:**
Delete `GPSDao.getUnitById` entirely and route all callers to the safe `UnitDAO.getUnitById`. If `GPSDao.getUnitById` must remain, convert to `PreparedStatement`. Validate `id` as a positive integer before any SQL use.

---

### HIGH: Insecure Direct Object Reference (IDOR) — GPS Data Not Scoped to Authenticated Company

**File:** `GPSDao.java` (lines 35–72 and 74–120); `GetAjaxAction.java` (lines 44–51)
**Description:**
Both GPS data retrieval methods lack any ownership or tenancy check. In `getUnitGPSData`, the `compId` parameter passed to the method is accepted directly from the request (`request.getParameter("compId")` at `GetAjaxAction.java` line 46) rather than being sourced from the authenticated session:

```java
// GetAjaxAction.java line 46
String compId = request.getParameter("compId")==null?"0":request.getParameter("compId");
// ...
request.setAttribute("arrGPSData", GPSDao.getUnitGPSData(compId, unit, dateTimeFormat, timezone));
```

The `compId` value is never validated against `session.getAttribute("sessCompId")`. An authenticated user from Company A can supply `compId` belonging to Company B, and then supply `unit` IDs belonging to Company B, to retrieve real-time GPS location data for another tenant's vehicles. The `compId` parameter is also entirely unused inside `getUnitGPSData` itself — it is accepted as a parameter but the SQL query (`QUERY_UNIT_GPS`) performs no `AND comp_id = ?` filter whatsoever:

```java
private static final String QUERY_UNIT_GPS =
    "select u.name,g.longitude,g.latitude,g.gps_time,m.name as manufacturer, ..."
    + " where g.unit_id=? order by g.gps_time desc limit 1";
// compId is never used in this query
```

Similarly, `getGPSLocations` accepts a `unitList` and performs no company-scoping in its query. Any authenticated user who knows or guesses another company's unit IDs can retrieve their real-time GPS positions.

**Risk:**
Cross-tenant data leakage of real-time vehicle GPS coordinates, manufacturer, and type details. In a fleet management context this is a high-severity privacy and competitive intelligence breach.

**Recommendation:**
1. In `GetAjaxAction.java`, always read `compId` from the session (`session.getAttribute("sessCompId")`), never from the request parameter.
2. In `getUnitGPSData`, add a `WHERE comp_id = ?` join condition to the `QUERY_UNIT_GPS` constant, binding the session `compId`.
3. In `getGPSLocations`, add the same company filter.
4. Consider pre-validating that every `unitId` in the supplied array belongs to the authenticated company before executing any GPS query.

---

### HIGH: Insecure Direct Object Reference (IDOR) — getUnitById Exposes Cross-Tenant Unit Data

**File:** `GPSDao.java` (lines 122–175)
**Description:**
`GPSDao.getUnitById(String id)` retrieves a unit record including `comp_id` and `mac_address` without verifying that the requested unit belongs to the caller's company. The query is:

```java
String sql = "select unit.id,unit.name,location,department,type_id,active,manu_id,size," +
             "fuel_type_id,hourmeter,serial_no,type.name,fuel_type.name,comp_id,unit.mac_address" +
             " from unit ... where unit.id=" + id;
```

No `AND comp_id = [session value]` clause is present. Any authenticated user who knows or can guess a numeric unit ID can retrieve full details (including MAC address and serial number) for units belonging to any tenant.

**Risk:**
Cross-tenant equipment data exposure including hardware identifiers. Combined with the SQL injection in the same method, this is exploitable without even guessing valid IDs.

**Recommendation:**
Add `AND unit.comp_id = ?` to the query and bind it to `sessCompId` from the authenticated session. Validate that the returned `comp_id` matches the session value and return an error if it does not.

---

### HIGH: Authentication Bypass / Pre-Auth Password Reset — Username Accepted from Request Without Session Binding

**File:** `GoResetPassAction.java` (lines 23–35)
**Description:**
The `action=reset` branch accepts the `username` parameter directly from the HTTP request and passes it to the Cognito password reset API, without any validation that the `username` matches the currently authenticated session or any server-side ownership check:

```java
String username = request.getParameter("username") == null ? "" : request.getParameter("username");
String accessToken = session.getAttribute("accessToken") == null ? "" : (String) session.getAttribute("accessToken");
// ...
PasswordRequest passwordRequest = PasswordRequest.builder()
    .username(username)
    .accessToken(accessToken)
    .build();
PasswordResponse passwordResponse = restClientServce.resetPassword(passwordRequest);
```

The `goResetPass.do` endpoint is explicitly excluded from the `PreFlightActionServlet` authentication check (line 111 of `PreFlightActionServlet.java`: `else if(path.endsWith("goResetPass.do")) return false;`). This means this action is reachable without an authenticated session, i.e., unauthenticated. Furthermore `session.getAttribute("accessToken")` will be null (resolved to empty string `""`) for unauthenticated requests, so the `accessToken` field in the request to the Cognito back-end will be blank.

The security of this flow depends entirely on the downstream Cognito service at `http://localhost:9090/auth/ResetPassword` correctly rejecting a blank `accessToken` for an arbitrary `username`. If the Cognito service does not enforce this, any unauthenticated visitor can trigger a password reset for any username by calling `GET/POST /goResetPass.do?action=reset&username=victim@example.com`. There is no CSRF token, no rate limiting, and no confirmation step visible in this action.

**Risk:**
If the Cognito service accepts a blank `accessToken`, this constitutes unauthenticated account takeover for any user. Even if the Cognito service rejects the request, the flow constitutes user enumeration (different responses for valid vs. invalid usernames may be observable) and allows an attacker to spam password reset requests against any known username.

**Recommendation:**
1. Enforce that `goResetPass.do` requires an authenticated session (remove it from the `excludeFromFilter` whitelist, or add an explicit session check at the top of `execute()`).
2. If the reset flow is intended to be pre-authentication (self-service reset), `username` must come from the session or a previously issued signed token — never from a raw request parameter.
3. Validate that `accessToken` is non-empty before submitting to the Cognito API.
4. Add a synchronizer token (CSRF protection) to the reset form.
5. Implement rate limiting on reset requests per username.
6. Ensure the Cognito service returns identical responses for valid and invalid usernames to prevent enumeration.

---

### HIGH: No CSRF Protection on GPS Report Form and Password Reset Flow

**File:** `gpsReport.jsp` (line 23); `GoResetPassAction.java` (lines 31–42)
**Description:**
The GPS report form submits via HTTP POST to `gpsreport.do` with no synchronizer (anti-CSRF) token:

```jsp
<html:form action="gpsreport.do" method="POST" styleId="adminUnitEditForm" styleClass="checklist_from">
```

Struts 1.x does not provide built-in CSRF protection. No `<html:hidden property="org.apache.struts.taglib.html.TOKEN"/>` token tag or equivalent custom mechanism is present in `gpsReport.jsp`.

The password reset action (`GoResetPassAction.java`) also performs a state-changing operation (triggering a Cognito password reset) in response to a POST request without any CSRF token validation. As noted above, `goResetPass.do` is excluded from the authentication filter, making CSRF against this endpoint trivially exploitable — an attacker can cause any visiting user's browser to trigger a password reset for an arbitrary username by embedding a hidden form on a third-party page.

**Risk:**
For the GPS report: an attacker who can lure an authenticated admin into visiting a malicious page can cause actions to be submitted on their behalf. For the password reset: any visitor can be made to silently trigger password reset attempts against arbitrary accounts.

**Recommendation:**
Implement the Struts 1.x synchronizer token pattern: call `saveToken(request)` in any action that renders a form, and call `isTokenValid(request, true)` at the start of the form-processing action. For the password reset, ensure the endpoint requires authentication (see previous finding) and apply token validation consistently.

---

### MEDIUM: JSON Injection / Stored XSS via Unescaped Database Values in GPS JSON Strings

**File:** `GPSDao.java` (lines 64–65, lines 102–103)
**Description:**
Both GPS methods construct JSON strings by direct string concatenation of database-sourced values without any JSON encoding or HTML escaping:

```java
// getUnitGPSData (line 64–65)
String gps_str = "{\"name\":\"" + unitBean.getVehName()
    + "\",\"status\":1,\"lat\":" + unitBean.getLatitude()
    + ",\"lon\":" + unitBean.getLongitude()
    + ",\"manufacturer\":\"" + unitBean.getManufacturer()
    + "\",\"time\":\"" + DateUtil.formatDateTime(...)
    + "\",\"type\":\"" + unitBean.getType()
    + "\",\"power\":\"" + unitBean.getPower()
    + "\",\"ingeofence\":false,\"distance\":\"\",\"classColor\":\"\"}";

// getGPSLocations (line 102–103)
String gps_str = "{\"name\":\"" + vehName
    + "\",\"status\":1,\"lat\":" + df.format(Double.parseDouble(latitude))
    + ",\"lon\":" + df.format(Double.parseDouble(longitude))
    + ",\"model\":\"xxxx\",\"time\":\"" + timeStmp
    + "\",\"dept\":\"" + "\",\"statusindicator\":null,...}";
```

If any database field (e.g., a vehicle name or manufacturer name) contains a double-quote character or a JSON metacharacter, the JSON structure will be malformed or the value will "break out" of its field, allowing injection of arbitrary JSON keys. If the vehicle name contains HTML/JavaScript (e.g., entered by a user with unit-management access), and this JSON is subsequently rendered without escaping into a page (as it is in `unit.gps.jsp` via `out.println(resp)`), this constitutes a stored XSS vector. The `unit.gps.jsp` file (line 30) writes the raw JSON to the HTTP response with no encoding:

```jsp
out.println(resp);
```

This JSP sets `contentType="text/html"` (default), so the browser may parse embedded script in the response body if the response is rendered as HTML (e.g., via an iframe or an AJAX responseText misuse).

**Risk:**
JSON injection leading to corrupted GPS data display, or stored XSS executing in the context of the admin portal if vehicle names or other fields contain script payloads. A user with unit management rights who can rename a vehicle could plant a script that executes for all admins who view the GPS map.

**Recommendation:**
Use a proper JSON serialisation library (e.g., Jackson, Gson) to build JSON objects rather than manual string concatenation. Ensure `unit.gps.jsp` declares `contentType="application/json"` and is served with the `X-Content-Type-Options: nosniff` header. Sanitise or encode all string fields before output.

---

### MEDIUM: Unescaped Session Attribute Output in JSP — custCd Written Directly to HTML

**File:** `gpsReport.jsp` (line 51)
**Description:**
The `sessCompId` session attribute is written directly into a hidden HTML input field without HTML encoding:

```jsp
String custCd = (String) session.getAttribute("sessCompId");
// ...
<input type="hidden" name="cust" id="cust" value="<%=custCd %>" />
```

If `sessCompId` were to contain characters such as `"`, `>`, or `<`, they would break the HTML attribute context. While `sessCompId` is a numeric company identifier that should not contain such characters in practice, the lack of escaping is a defence-in-depth failure. A session fixation or session injection attack that places a crafted value into `sessCompId` would result in HTML injection at this point.

Additionally, the JavaScript block (lines 55–70) reads `$('#cust').val()` and passes it to the `initialize()` function, which likely constructs an AJAX URL. If the hidden field value is ever XSS-injectable, it flows into a JavaScript call without sanitisation.

**Risk:**
Low probability in normal operation, but if `sessCompId` can ever be set to a non-numeric value (e.g., via session poisoning, parameter injection in the login/switch-company flow, or a logic bug), HTML/script injection would result.

**Recommendation:**
Use JSTL `<c:out value="${sessionScope.sessCompId}" />` or explicitly `ESAPI.encoder().encodeForHTMLAttribute(custCd)` before writing any session attribute into HTML. Apply this pattern to all JSP scriptlet outputs.

---

### MEDIUM: Email / Username Enumeration via Password Reset Flow

**File:** `GoResetPassAction.java` (lines 31–42)
**Description:**
The `action=reset` branch forwards to `"reset"` if the Cognito API returns `HTTP_OK`, and to `"getcode"` otherwise. The distinct forward destinations (and their associated page content) make it possible for an attacker to determine whether a given username exists in the system:

```java
if(passwordResponse.getCode().equals(RuntimeConf.HTTP_OK)) {
    return mapping.findForward("reset");   // success → username exists
} else {
    return mapping.findForward("getcode"); // failure → username may not exist
}
```

Since this endpoint is publicly reachable (excluded from the auth filter), an attacker can enumerate valid usernames by observing whether the response redirects to `resetPassDefinition` or `getCodeDefinition`. Even if the page text is identical, the URL/tile path difference is detectable.

**Risk:**
Username / email address enumeration for all accounts in the system. This enables targeted phishing, credential stuffing preparation, and account lockout attacks.

**Recommendation:**
Return identical responses (same HTTP status, same destination page, same body) regardless of whether the username is valid. Log enumeration attempts server-side. Consider adding rate limiting (e.g., via a servlet filter or a token bucket per IP).

---

### MEDIUM: NullPointerException Risk in GoSearchAction — Session Used Without Null Check

**File:** `GoSearchAction.java` (lines 27–28)
**Description:**
The action retrieves a session with `getSession(false)` (which returns `null` if no session exists) and immediately calls `removeAttribute` on the result without any null check:

```java
HttpSession theSession = request.getSession(false);
theSession.removeAttribute("arrDriver");
return mapping.findForward("goSearch");
```

If the session does not exist (e.g., the request arrives after a session timeout, or the user is not authenticated), `theSession` will be `null` and `theSession.removeAttribute("arrDriver")` will throw a `NullPointerException`. This is caught by the Struts global exception handler, which forwards to `errorDefinition` (an `error.html` page). Depending on whether this page leaks a stack trace, this may expose internal class and path names.

The struts-config maps `/goSerach.do` (note the typo — `goSerach` not `goSearch`). This means the legitimately typed URL `/goSearch.do` would produce a 404, which may itself be an information disclosure issue and indicates the action was likely reached through hard-coded links only.

**Risk:**
Denial of service (unhandled exception) and potential stack trace disclosure for unauthenticated or post-timeout requests. The typo in the action path (`goSerach`) means the endpoint is not reachable under the expected URL and may indicate dead or untested code.

**Recommendation:**
Add a null check: `if (theSession != null) { theSession.removeAttribute("arrDriver"); }`. Additionally correct the action path typo from `/goSerach` to `/goSearch` in `struts-config.xml`. Ensure `error.html` does not contain stack traces in any environment.

---

### LOW: Sensitive Data Logged — SQL Queries with Potential User Input Written to Log at INFO Level

**File:** `GPSDao.java` (lines 90, 140)
**Description:**
Both `getGPSLocations` and `getUnitById` log the fully-constructed SQL query string at `INFO` level before execution:

```java
log.info(sql);  // line 90 in getGPSLocations — contains unitList[i] directly
log.info(sql);  // line 140 in getUnitById — contains id parameter directly
```

In the case of SQL injection, the injected payload is thereby recorded in log files. While this can aid forensic analysis, it also means that if log files are accessible to less privileged users (e.g., a developer log viewer), they can see exactly what injection attempts were made — or, in some threat models, logs are forwarded to a SIEM where the SQL content could trigger secondary injection into log management systems (log injection).

More practically, if an attacker gains read access to log files, they obtain a record of all IDs queried by all users, which constitutes a partial audit trail exposure.

**Risk:**
Log injection, inadvertent disclosure of query patterns and data access history to parties with log read access. Minimal additional risk beyond the SQL injection issues already noted.

**Recommendation:**
Remove `log.info(sql)` calls that embed user-controlled input. If query logging is needed for debugging, log only the static query template, not the interpolated string. Use `PreparedStatement` (which separates parameters from the query template) to make this distinction structural.

---

### LOW: Session Attribute Cast Without Type Check — Potential ClassCastException in gpsReport.jsp

**File:** `gpsReport.jsp` (lines 5–6)
**Description:**
Session attributes are cast to `String` without instanceof checks:

```jsp
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");
String custCd = (String) session.getAttribute("sessCompId");
```

If `sessDateFormat` is `null` (e.g., partially initialised session), the `.replaceAll()` call will throw a `NullPointerException`. If either attribute is set to a non-`String` object (possible via session manipulation), a `ClassCastException` results. Both conditions forward to the global error handler, which may expose internals.

**Risk:**
Application error / minor information disclosure. No direct security exploit in isolation.

**Recommendation:**
Add null checks before dereferencing session attributes. Use `Objects.toString(session.getAttribute("sessDateFormat"), "")` or equivalent defensive patterns.

---

### LOW: Hardcoded Internal Service Port — Information Disclosure

**File:** `RestClientService.java` (line 35)
**Description:**
The internal Cognito microservice URL is hardcoded with a fixed port and bound to `localhost`:

```java
private final String COGNITO_API_PORT = "9090";
// Used as: "http://localhost:9090/auth/ResetPassword"
```

This is not a remote-exploitable vulnerability in itself, but it discloses the internal service topology in source code. If the source code is exposed (e.g., via a path traversal, a public repository, or decompilation), an attacker with any form of SSRF or internal access would know exactly where to target the unauthenticated internal API.

**Risk:**
Facilitation of SSRF attacks and internal service discovery if source is exposed. The internal Cognito API at port 9090 must be assumed to have no external authentication beyond network isolation.

**Recommendation:**
Move service endpoint configuration to an external properties file (`application.properties` or environment variable). Ensure the internal Cognito service enforces mutual TLS or a shared secret even on localhost.

---

### INFO: GoSearchAction Contains Dead Code / Typo in Action Path Mapping

**File:** `GoSearchAction.java` (line 24); `struts-config.xml` (line 179)
**Description:**
The action is mapped in `struts-config.xml` as path `/goSerach` (misspelling of "Search"):

```xml
<action path="/goSerach" type="com.action.GoSearchAction">
```

The correct URL would therefore be `/goSerach.do`, not `/goSearch.do`. Any external links or bookmarks using the correctly-spelled URL would result in a 404 not found response. This suggests the action may be effectively dead or only reachable via specific hard-coded links within the application that also contain the typo.

**Risk:**
Informational. No direct security impact, but indicates untested code paths and potential discrepancy between documented and actual URLs.

**Recommendation:**
Correct the typo in `struts-config.xml` and ensure all links referencing this action are updated consistently.

---

### INFO: Raw SQL Logged at INFO Level Discloses Schema Details

**File:** `GPSDao.java` (line 90, line 140); `GoSearchAction.java` (general logging)
**Description:**
Full SQL query strings including table names (`gps`, `unit`, `type`, `fuel_type`), column names, join structure, and user-controlled input values are logged at `INFO` level by `log.info(sql)`. Log output at INFO level is typically written to application log files and may be visible in centralised log management systems or via the Tomcat manager interface.

**Risk:**
Schema information disclosure to parties with log read access. Assists attackers in crafting more targeted SQL injection payloads.

**Recommendation:**
Log only query identifiers or static template names at INFO level. Reserve full query logging for DEBUG level with appropriate log level controls in production.

---

## Summary

| # | Severity | Title |
|---|----------|-------|
| 1 | CRITICAL | SQL Injection — GPSDao.getGPSLocations (Statement + concatenation) |
| 2 | CRITICAL | SQL Injection — GPSDao.getUnitById (Statement + concatenation) |
| 3 | HIGH | IDOR — GPS Data Not Scoped to Authenticated Company (getUnitGPSData / getGPSLocations) |
| 4 | HIGH | IDOR — getUnitById Exposes Cross-Tenant Unit Data |
| 5 | HIGH | Auth Bypass / Pre-Auth Password Reset — Username from Request Parameter |
| 6 | HIGH | No CSRF Protection on GPS Report Form and Password Reset Flow |
| 7 | MEDIUM | JSON Injection / Stored XSS via Unescaped DB Values in GPS JSON |
| 8 | MEDIUM | Unescaped Session Attribute Written to HTML (gpsReport.jsp) |
| 9 | MEDIUM | Username Enumeration via Password Reset Response Difference |
| 10 | MEDIUM | NullPointerException Risk — Session Not Null-Checked in GoSearchAction |
| 11 | LOW | Sensitive SQL Queries Logged with User Input at INFO Level |
| 12 | LOW | Session Attribute Cast Without Null/Type Check in gpsReport.jsp |
| 13 | LOW | Hardcoded Internal Service Port in RestClientService |
| 14 | INFO | Dead Code / Typo in GoSearchAction Path Mapping (/goSerach) |
| 15 | INFO | Raw SQL Logged at INFO Level Discloses Database Schema |

**CRITICAL: 2 / HIGH: 4 / MEDIUM: 4 / LOW: 3 / INFO: 2**
