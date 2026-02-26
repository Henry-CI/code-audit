# Security Audit Report
## Files: GetAjaxAction.java, getcode.jsp, getDriverName.jsp, GetXmlAction.java
**Application:** forkliftiqadmin (internal name: pandora)
**Date:** 2026-02-26
**Auditor:** Pass 1 automated review
**Framework:** Apache Struts 1.3.10 / Tomcat
**Branch:** master

---

## Scope

| File | Path |
|------|------|
| GetAjaxAction.java | `src/main/java/com/action/GetAjaxAction.java` |
| getcode.jsp | `src/main/webapp/html-jsp/getcode.jsp` |
| getDriverName.jsp | `src/main/webapp/html-jsp/getDriverName.jsp` |
| GetXmlAction.java | `src/main/java/com/action/GetXmlAction.java` |

Supporting files reviewed for full call-chain analysis:
- `src/main/java/com/dao/UnitDAO.java` (methods `getType`, `getPower`)
- `src/main/java/com/dao/QuestionDAO.java` (method `getQuestionContentById`)
- `src/main/java/com/dao/GPSDao.java` (method `getUnitGPSData`)
- `src/main/java/com/dao/DriverDAO.java` (method `getAllDriver`)
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/WEB-INF/tiles-defs.xml`
- `src/main/webapp/gps/unit.gps.jsp`

---

## Findings

---

### CRITICAL: SQL Injection via unsanitized `manu_id` in UnitDAO.getType and UnitDAO.getPower

**File:** `src/main/java/com/dao/UnitDAO.java` (lines 625-628, 666-670) — called from `GetAjaxAction.java` (lines 31, 36)

**Description:**
`GetAjaxAction` passes the raw request parameters `manu_id` and `type_id` directly to `UnitDAO.getType()` and `UnitDAO.getPower()`. Both DAO methods concatenate these values into SQL statements executed via a `Statement` object — there is no parameterisation, no type validation, and no allowlist check before the values reach the database.

`GetAjaxAction.java` (lines 26, 35-36):
```java
String manu_id = request.getParameter("manu_id")==null?"0":request.getParameter("manu_id");
// ...
arrXml = unitDao.getType(manu_id);
// ...
String type_id = request.getParameter("type_id")==null?"0":request.getParameter("type_id");
arrXml = unitDao.getPower(manu_id, type_id);
```

`UnitDAO.java` (lines 625-628):
```java
String sql = "select distinct(type.id),name from manu_type_fuel_rel" +
        " left outer join type on type.id = manu_type_fuel_rel.type_id " +
        " where manu_id = " + manu_id +
        " order by name";
```

`UnitDAO.java` (lines 665-670):
```java
String sql = "select fuel_type.id,name from manu_type_fuel_rel" +
        " left outer join fuel_type on fuel_type.id = manu_type_fuel_rel.fuel_type_id " +
        " where manu_id = " + manu_id;
if (!type_id.equalsIgnoreCase("")) {
    sql += " and type_id= " + type_id;
}
```

An attacker with a valid session can send:
```
GET /getAjax.do?action=getType&manu_id=0 UNION SELECT table_name,table_schema FROM information_schema.tables--
```
This would enumerate all database tables. Because the application uses PostgreSQL and the DB user likely has broad permissions, this can escalate to reading arbitrary data from other tenants, extracting credentials, or (if `pg_read_file` / `COPY TO` is available) reading files from the server filesystem.

**Risk:** Full database compromise, cross-tenant data exfiltration, potential server-level file access.

**Recommendation:** Replace both `Statement` + string-concatenation patterns with `PreparedStatement` and integer-typed parameters. Validate that `manu_id` and `type_id` are non-negative integers before use. Example fix for `getType`:
```java
String sql = "select distinct(type.id),name from manu_type_fuel_rel" +
        " left outer join type on type.id = manu_type_fuel_rel.type_id" +
        " where manu_id = ? order by name";
// use PreparedStatement, ps.setInt(1, Integer.parseInt(manu_id))
```

---

### CRITICAL: SQL Injection via unsanitized `qus_id` and `lan_id` in QuestionDAO.getQuestionContentById

**File:** `src/main/java/com/dao/QuestionDAO.java` (lines 328-331) — called from `GetAjaxAction.java` (lines 40-43)

**Description:**
The `getQcontent` action branch reads `qus_id` and `lan_id` directly from the HTTP request and passes them without any validation or parameterisation to `QuestionDAO.getQuestionContentById()`, which builds two different SQL strings by concatenation:

`GetAjaxAction.java` (lines 40-43):
```java
String qus_id = request.getParameter("qus_id")==null?"0":request.getParameter("qus_id");
String lan_id = request.getParameter("lan_id")==null?"0":request.getParameter("lan_id");
QuestionDAO questionDAO = new QuestionDAO();
arrXml = questionDAO.getQuestionContentById(qus_id, lan_id);
```

`QuestionDAO.java` (lines 327-331):
```java
if (lanId.equalsIgnoreCase("1")) {
    sql = "select content from question where id = " + qId;
} else {
    sql = "select content from question_content where question_id = " + qId + " and lan_id = " + lanId;
}
```

Both branches are injectable. The `lan_id` branch is particularly straightforward since an attacker controls two concatenated parameters simultaneously. Example:
```
GET /getAjax.do?action=getQcontent&qus_id=1&lan_id=2 UNION SELECT session_token FROM driver LIMIT 1--
```

**Risk:** Full database read access, cross-tenant data exposure, credential theft.

**Recommendation:** Use `PreparedStatement` for both branches. Validate that `qus_id` and `lan_id` parse as positive integers before use; reject anything that does not.

---

### CRITICAL: IDOR — `last_gps` action accepts attacker-controlled `compId` bypassing multi-tenant isolation

**File:** `src/main/java/com/action/GetAjaxAction.java` (lines 44-51)

**Description:**
The `last_gps` branch of `GetAjaxAction` reads the `compId` value directly from the HTTP request parameter instead of reading it from the session (`sessCompId`). Any authenticated user from any company can supply a different company's ID and receive that company's GPS data:

```java
} else if(action.equals("last_gps")) {
    String[] unit = request.getParameterValues("unit");
    String compId = request.getParameter("compId")==null?"0":request.getParameter("compId");
    // ...
    request.setAttribute("arrGPSData", GPSDao.getUnitGPSData(compId, unit, dateTimeFormat, timezone));
}
```

`GPSDao.getUnitGPSData()` uses the caller-supplied `compId` (line 35 of GPSDao.java) as the data scope, but the underlying SQL query (`QUERY_UNIT_GPS`) does not filter by company at all — it only filters by the `unit_id` array values also supplied by the attacker:

```java
private static final String QUERY_UNIT_GPS =
    "select u.name,g.longitude,g.latitude,g.gps_time,m.name as manufacturer, ..." +
    " where g.unit_id=? order by g.gps_time desc limit 1";
```

The `compId` parameter is accepted by the signature but is not used in the SQL query itself, meaning any authenticated user can supply arbitrary unit IDs (from any company) and receive their live GPS coordinates, manufacturer, and type data without any cross-tenant ownership check. The `compId` parameter serves no access-control purpose in this code path.

**Risk:** Real-time GPS location leakage for all units across all tenants. This is a full IDOR enabling cross-company surveillance of physical equipment locations.

**Recommendation:** Remove the `compId` parameter from the HTTP request. Read the company identity exclusively from `session.getAttribute("sessCompId")`. Enforce the company scope inside `getUnitGPSData` by joining or checking that each requested `unit_id` belongs to the session company before querying GPS data.

---

### HIGH: SQL Injection via unsanitized `unit` array in GPSDao.getUnitGPSData (no integer validation)

**File:** `src/main/java/com/dao/GPSDao.java` (lines 45-54) — called from `GetAjaxAction.java` (line 51)

**Description:**
`GetAjaxAction` passes the raw `unit` parameter values array directly to `GPSDao.getUnitGPSData()`. Inside that method each element is passed as the argument to `Integer.parseInt(unitId)` before being bound to a `PreparedStatement`. The `parseInt` call provides some protection against classic string injection, but it throws a `NumberFormatException` (not caught specifically) on non-integer input, which propagates upward and may result in unhandled error responses leaking stack traces (see also the information-disclosure finding below).

However, the more significant concern is that the `unit` array is unbounded — no maximum number of elements is enforced. An attacker can submit thousands of unit IDs, causing the server to execute thousands of individual prepared queries in a single request, enabling a Denial-of-Service amplification attack:

```java
for( String unitId : unitIds ) {
    List<GPSUnitBean> list = DBUtil.queryForObjects(builder.toString(),
        stmt -> stmt.setInt(1, Integer.parseInt(unitId)), ...);
}
```

**Risk:** DoS via query amplification; potential for targeted enumeration of valid unit IDs across all tenants.

**Recommendation:** Enforce a hard maximum on the number of unit IDs accepted per request (e.g., 50). Validate each element as a positive integer. Scope the query to only return units belonging to `sessCompId` (see IDOR finding above).

---

### HIGH: JSON Injection in GPS response — unescaped database values embedded in hand-built JSON string

**File:** `src/main/java/com/dao/GPSDao.java` (lines 64-65) — response consumed by `src/main/webapp/gps/unit.gps.jsp`

**Description:**
The GPS response is assembled by manually concatenating database values into a JSON string literal with no escaping:

```java
String gps_str = "{\"name\":\"" + unitBean.getVehName()
    + "\",\"status\":1,\"lat\":" + unitBean.getLatitude()
    + ",\"lon\":" + unitBean.getLongitude()
    + ",\"manufacturer\":\"" + unitBean.getManufacturer()
    + "\",\"time\":\"" + DateUtil.formatDateTime(...)
    + "\",\"type\":\"" + unitBean.getType()
    + "\",\"power\":\"" + unitBean.getPower()
    + "\",\"ingeofence\":false,...}";
```

If a unit name, manufacturer name, or type name stored in the database contains a double-quote, backslash, or JSON control characters, the output JSON will be malformed or structurally manipulated. An attacker who can control unit name data (via a separate write endpoint) can inject arbitrary JSON keys/values into the response consumed by the GPS map page. This can be used to override trusted fields (e.g., set `"ingeofence":true`) or, if the client evaluates the JSON with `eval()`, to achieve stored XSS.

The `unit.gps.jsp` view also declares `contentType="text/html"` (line 4) despite returning JSON, which worsens the XSS surface.

**Risk:** Stored JSON injection; potential stored XSS if the client uses `eval()` or the Content-Type mismatch causes the browser to treat the response as HTML.

**Recommendation:** Use a JSON serialisation library (e.g., Jackson, Gson) to build all JSON responses. Never concatenate database-sourced strings into JSON manually. Fix the Content-Type declaration in `unit.gps.jsp` (see content-type finding below).

---

### HIGH: XML Injection in getDriverName.jsp — unescaped driver names embedded in XML response

**File:** `src/main/webapp/html-jsp/getDriverName.jsp` (lines 15)

**Description:**
Driver first and last names are concatenated directly into XML markup without any XML entity escaping:

```java
resp = resp + "<rec><name>"
    + (arrDriver.get(i)).getFirst_name()
    + " "
    + (arrDriver.get(i)).getLast_name()
    + "</name></rec>";
```

If a driver's name contains XML special characters (`<`, `>`, `&`, `"`, `'`), the output XML will be malformed or structurally manipulated. An attacker who can register a driver with a crafted name (e.g., `</name></rec><rec><name>injected`) can break the XML structure consumed by the calling JavaScript. If the client parses this with `innerHTML` or `eval`, this becomes a stored XSS vector.

A driver's name is a plausible injection point since it is typically editable by administrators or self-service registration flows.

**Risk:** Stored XML injection leading to malformed responses and potential stored XSS on any page that processes this XML and injects fragments into the DOM without sanitisation.

**Recommendation:** Escape all database-sourced values before embedding them in XML. Use `org.apache.commons.lang.StringEscapeUtils.escapeXml()` or equivalent. Consider using a proper XML/DOM builder rather than string concatenation.

---

### HIGH: XML Injection in getAjax.jsp — unescaped name values in XML response

**File:** `src/main/webapp/html-jsp/getAjax.jsp` (line 20)

**Description:**
The AJAX response view for `GetAjaxAction` (served for `getType`, `getPower`, and `getQcontent` actions) constructs XML by concatenating `XmlBean.name` and `XmlBean.id` values with no XML entity escaping:

```java
resp = resp + "<rec><code>" + id + "</code><name>" + name + "</name></rec>";
```

The `name` field is populated directly from database columns (`type.name`, `fuel_type.name`, `question.content`, `question_content.content`). The `getQcontent` action is particularly sensitive because the `name` field contains free-text question content that administrators enter. If this content includes `<`, `>`, or `&`, the XML response is malformed. If it includes `</name></rec><script>`, any page that injects the response into the DOM without sanitisation is vulnerable to stored XSS.

**Risk:** Stored XSS via crafted question/type content; malformed XML disrupting client-side functionality.

**Recommendation:** Apply XML entity escaping to all values before embedding in XML. Replace manual string concatenation with a DOM or SAX builder.

---

### HIGH: Missing Content-Type header on JSON GPS response

**File:** `src/main/webapp/gps/unit.gps.jsp` (line 4)

**Description:**
The GPS AJAX endpoint (`/getAjaxGPS.do`) forwards to `unit.gps.jsp`, which outputs a JSON body but declares `contentType="text/html; charset=ISO-8859-1"`:

```jsp
<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
```

The browser will receive JSON data under a `text/html` Content-Type. When combined with the JSON injection finding above, this Content-Type mismatch means a browser may attempt to parse the response as HTML, converting JSON injection into a direct XSS vector without requiring any unsafe `eval()` on the client side. Additionally, some older IE versions will MIME-sniff the response regardless of the declared type, increasing risk.

**Risk:** Escalates the JSON injection finding to a direct reflected/stored XSS depending on how the client handles the response.

**Recommendation:** Set `response.setContentType("application/json; charset=UTF-8")` at the top of the JSP (overriding the page directive) and remove the `text/html` declaration.

---

### HIGH: Missing Content-Type header on XML responses (getAjax.jsp and getDriverName.jsp declared but not enforced via response object)

**File:** `src/main/webapp/html-jsp/getAjax.jsp` (line 6), `src/main/webapp/html-jsp/getDriverName.jsp` (line 6)

**Description:**
Both `getAjax.jsp` and `getDriverName.jsp` call `response.setContentType("text/xml")` using the scriptlet API, which is the correct approach. However, neither JSP adds the `X-Content-Type-Options: nosniff` response header. Without this header, Internet Explorer and some Edge versions may MIME-sniff the body and reinterpret it as HTML if it contains HTML-like content (which is possible via the XML injection findings above). Combined with the XML injection vulnerabilities, this creates a direct XSS path in affected browsers.

Additionally, `getAjax.jsp` is also used for the `getQcontent` action which returns question text that could contain arbitrary Unicode characters, but the XML declaration does not specify an encoding, which can cause XML parser errors on the client.

**Risk:** MIME sniffing may allow XML injection to execute as HTML/script in Internet Explorer/Edge.

**Recommendation:** Add `response.setHeader("X-Content-Type-Options", "nosniff")` to both JSPs. Add an XML declaration with explicit encoding: `<?xml version="1.0" encoding="UTF-8"?>`.

---

### MEDIUM: CSRF — state-changing form in getcode.jsp has no synchronizer token

**File:** `src/main/webapp/html-jsp/getcode.jsp` (lines 12-26)

**Description:**
The password-reset request form submits to `goResetPass.do` via POST but contains no CSRF synchronizer token. Struts 1.x does not add tokens automatically; the application must opt in. There is no `<html:form>` tag (which would enable Struts token management), and no custom hidden token field is present:

```html
<form method="post" action="goResetPass.do" Class="login-fields" id="confirmationCodeFrom">
    <input type="text" name="username" value="" ...>
    <input type="hidden" name="action" value="reset"/>
</form>
```

The `goResetPass.do` action is excluded from the session check (`excludeFromFilter` returns `false` for this path), so the form is accessible to unauthenticated users. While the form's primary impact is initiating a password reset (which triggers a Cognito email), the absence of a CSRF token means:

1. Any page on any origin can silently POST to `goResetPass.do?action=reset&username=victim@example.com`, triggering unwanted password-reset emails for arbitrary users (email spam/harassment).
2. If the action is ever extended to perform more sensitive operations, CSRF protection will still be absent.

**Risk:** Unauthenticated CSRF enabling password-reset spam against arbitrary user accounts, potentially used to lock out users or as a phishing/social engineering vector.

**Recommendation:** Add a CSRF token. Since this form is pre-login, use a stateless HMAC-based token tied to the session ID or a time-limited value stored in a `HttpOnly` cookie, and validate it server-side in `GoResetPassAction`. Alternatively, implement the double-submit cookie pattern.

---

### MEDIUM: CSRF — no synchronizer token on GetXmlAction (state-exposing AJAX endpoint accessible to all authenticated users)

**File:** `src/main/java/com/action/GetXmlAction.java` — mapped to `/getXml.do`

**Description:**
`GetXmlAction` is a data-read (not data-write) endpoint, so CSRF is of lower severity here. However, because the response is served as `text/xml` with no `X-Content-Type-Options` header or CORS restriction, a malicious page on another origin can use a `<script src="...">` or `<link>` tag to trigger the request with the victim's credentials and read the response in older browsers that do not enforce the same-origin policy on cross-origin reads of non-script MIME types. More critically, if the Content-Type is ever changed or MIME-sniffed as JavaScript, the full cross-origin read attack becomes viable.

**Risk:** Cross-origin information disclosure of driver names in susceptible browsers; escalates if Content-Type controls are weakened.

**Recommendation:** Add the `X-Content-Type-Options: nosniff` response header. For all state-changing Struts actions, implement Struts 1.x token checking via `saveToken(request)` / `isTokenValid(request)`.

---

### MEDIUM: Information disclosure — driver PII (names) returned without company ownership verification in getDriverName.jsp (theoretical, mitigated by GetXmlAction)

**File:** `src/main/java/com/action/GetXmlAction.java` (lines 26-27), `src/main/webapp/html-jsp/getDriverName.jsp`

**Description:**
`GetXmlAction` correctly reads `sessCompId` from the session and passes it to `DriverDAO.getAllDriver()`, which scopes the query to the authenticated company via a parameterised `PreparedStatement`. This is the intended multi-tenant control and it works correctly at the DAO level:

```java
String sessCompId = (String) session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
List<DriverBean> arrDriver = driverDAO.getAllDriver(sessCompId, true);
```

However, if `sessCompId` is an empty string (which is the default when `session.getAttribute("sessCompId")` returns null), `Long.parseLong("")` inside `getAllDriver` will throw a `NumberFormatException`. This exception is not caught in `GetXmlAction`, meaning the action will throw, the container's error page (`/error/error.html`) will be served, and no data is returned. This constitutes a denial-of-service for any session where `sessCompId` is null but the session itself is still considered valid by the auth gate.

The more important note is that the auth gate (`PreFlightActionServlet`) checks `sessCompId != null` AND `!equals("")` before allowing access, so a truly null `sessCompId` should not reach this action. The vulnerability is the silent default of `""` rather than failing fast or throwing a meaningful error.

**Risk:** Unhandled exception causing 500 error page exposure; theoretical information disclosure if the auth gate check is ever relaxed or bypassed.

**Recommendation:** Remove the null-to-empty-string default. Instead, if `sessCompId` is null after authentication, throw an `AuthorizationException` or redirect to the session-expired page immediately. Do not allow an empty `compId` to propagate to DAO layer calls.

---

### MEDIUM: NullPointerException and unhandled exception risk in getDriverName.jsp

**File:** `src/main/webapp/html-jsp/getDriverName.jsp` (line 11)

**Description:**
The JSP dereferences `arrDriver` (cast from `request.getAttribute("arrDriverList")`) without a null check:

```java
ArrayList<DriverBean> arrDriver = (ArrayList<DriverBean>)request.getAttribute("arrDriverList");
if(arrDriver.size()>0)
```

If `GetXmlAction` throws an exception before setting `arrDriverList` on the request (as described in the finding above), or if the Struts forward is somehow invoked without passing through `GetXmlAction`, `arrDriver` will be `null` and line 11 will throw a `NullPointerException`. The JSP's error page is not configured (no `errorPage` directive), so the container's default error handler will take over, potentially exposing a stack trace containing class names, database information, and the Tomcat version.

**Risk:** Stack trace information disclosure; application may reveal internal architecture details to an attacker who can trigger the error condition.

**Recommendation:** Add a null check before dereferencing `arrDriver`. Add `<%@ page errorPage="../error/error.html" %>` directive. Log the error server-side and return a structured empty XML response rather than letting the exception propagate.

---

### MEDIUM: Sensitive session attributes accessed without null safety in GetAjaxAction (last_gps branch)

**File:** `src/main/java/com/action/GetAjaxAction.java` (lines 47-49)

**Description:**
The `last_gps` branch casts and dereferences session attributes without null-safety guards:

```java
String dateFormat = ((String) request.getSession().getAttribute("sessDateFormat"))
        .replaceAll("yyyy", "yy").replaceAll("M", "m");
String dateTimeFormat = (String) request.getSession().getAttribute("sessDateTimeFormat");
String timezone = (String) request.getSession().getAttribute("sessTimezone");
```

`sessDateFormat` is cast and immediately dereferenced with `.replaceAll(...)`. If this session attribute is null (e.g., partially initialised session, session replay after attribute expiry), the application will throw a `NullPointerException`. The resulting 500 response may expose internal stack trace information.

Furthermore, `dateTimeFormat` and `timezone` are used downstream in `GPSDao.getUnitGPSData()` and `DateUtil.formatDateTime()` without null checks, potentially causing further cascading errors.

**Risk:** Denial-of-service via crafted request to a valid session; information disclosure via stack traces.

**Recommendation:** Add null checks for all session attributes before use. Use a utility method that retrieves session attributes with a safe default and logs a warning if expected attributes are missing.

---

### LOW: getcode.jsp form uses a plain `<form>` tag instead of Struts `<html:form>` — CSRF token helper bypassed

**File:** `src/main/webapp/html-jsp/getcode.jsp` (line 12)

**Description:**
The form uses a plain HTML `<form>` tag rather than the Struts `<html:form>` tag:

```html
<form method="post" action="goResetPass.do" Class="login-fields" id="confirmationCodeFrom">
```

Struts 1.x provides built-in CSRF token support (via `html:form` + `saveToken`/`isTokenValid`) that is only available when `<html:form>` is used. The use of a raw HTML form tag means this path will be skipped even if the developer later adds token validation to the action, because `<html:form>` is what automatically injects the `org.apache.struts.taglib.html.TOKEN` hidden field. This is a defence-in-depth gap.

**Risk:** Reinforces the CSRF finding above; future developers may add server-side token validation without realising the form tag does not supply the token.

**Recommendation:** Replace `<form>` with `<html:form>` and integrate Struts token management, or use a framework-agnostic CSRF token approach (double-submit cookie or synchronizer token via hidden field populated server-side).

---

### LOW: Client-side email validation only — no server-side validation in GoResetPassAction

**File:** `src/main/webapp/html-jsp/getcode.jsp` (lines 33-52), `src/main/java/com/action/GoResetPassAction.java`

**Description:**
The `getcode.jsp` page performs email format validation in JavaScript before form submission:

```javascript
function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+...$/;
    return re.test(String(email).toLowerCase());
}
```

`GoResetPassAction` performs no corresponding server-side validation of the `username` parameter before passing it to `RestClientService.resetPassword()`. An attacker can bypass the JavaScript check entirely by submitting the form directly (e.g., via curl or Burp Suite) with a malformed or oversized email value. Depending on how the Cognito REST client handles malformed input, this could cause unexpected errors, log noise, or information disclosure through error messages.

**Risk:** Attackers can probe the Cognito integration with arbitrary username values; potential for account enumeration if different responses are returned for valid vs. invalid usernames.

**Recommendation:** Add server-side validation of the `username` parameter in `GoResetPassAction` before invoking the external service. Return a uniform response for both valid and invalid email addresses to prevent account enumeration.

---

### LOW: Timezone parameter from session used in SQL string without sanitisation (potential second-order injection)

**File:** `src/main/java/com/dao/DriverDAO.java` (line 358) — indirectly relevant context

**Description:**
While not directly in the audited files, `GetAjaxAction` (line 49) reads the `sessTimezone` session attribute and passes it to `GPSDao.getUnitGPSData()`. In a separate code path in `DriverDAO.getAllDriverSearch()` (line 358), a `timezone` value sourced from the session is interpolated directly into a SQL string:

```java
builder.append(" and timezone('"+timezone+"', p.updatedat)::DATE = current_date::DATE ");
```

If the `sessTimezone` session attribute is ever set from user-supplied input (e.g., a profile preference form) without sanitisation, this constitutes a second-order SQL injection. The timezone value set at login/profile-update time would not be injected until the search query is executed. While the `sessTimezone` origin is out of scope for this pass, the consumption of that value in a SQL concatenation is a significant risk that depends on how the attribute is populated.

**Risk:** Second-order SQL injection if `sessTimezone` is ever sourced from user-controlled input without validation.

**Recommendation:** Validate all session-stored values against an allowlist of valid IANA timezone identifiers before storing them in the session, and before using them in SQL queries. Use parameterised equivalents where the database supports them (PostgreSQL's `AT TIME ZONE` can accept a parameter).

---

### INFO: `getAjaxGPS.do` and `getXml.do` are protected by the session auth gate

**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java` (lines 98-115)

**Description:**
Confirmed that `/getAjaxGPS.do`, `/getAjax.do`, and `/getXml.do` are not listed in the `excludeFromFilter` method and therefore fall through to the `return true` catch-all. The auth gate will enforce `sessCompId != null && !equals("")` for all three endpoints. No authentication bypass exists via the path exclusion mechanism for these specific actions.

The `goResetPass.do` endpoint is correctly excluded from the session check since it serves the pre-login password-reset flow.

**Risk:** No authentication bypass via path exclusion for the AJAX/XML endpoints.

**Recommendation:** No action required for this specific point. Maintain the current exclusion list and periodically review it when new actions are added.

---

### INFO: DriverDAO.getAllDriver uses a PreparedStatement with correct company scoping

**File:** `src/main/java/com/dao/DriverDAO.java` (lines 76-77, 296-312)

**Description:**
The `QUERY_DRIVER_BY_COMP` constant correctly uses a parameterised placeholder for `comp_id`:

```java
private static final String QUERY_DRIVER_BY_COMP =
    "select d.id, d.first_name, d.last_name, d.active, d.licno, d.expirydt, ..." +
    "from driver d inner join permission p on d.id = p.driver_id where p.comp_id = ?";
```

The `getAllDriver` method binds the `compId` via `stmt.setLong(1, Long.parseLong(compId))`. The SQL used by `GetXmlAction` → `getDriverName.jsp` is therefore safe from SQL injection and correctly scoped to the session company.

**Risk:** None — this is a positive finding confirming correct implementation.

**Recommendation:** This pattern (constant SQL + PreparedStatement) should be used as the standard across all DAO methods in the codebase.

---

## Summary Table

| # | Severity | Title | File(s) |
|---|----------|-------|---------|
| 1 | CRITICAL | SQL injection via `manu_id`/`type_id` in getType/getPower | UnitDAO.java:625, 666 / GetAjaxAction.java:26,36 |
| 2 | CRITICAL | SQL injection via `qus_id`/`lan_id` in getQuestionContentById | QuestionDAO.java:328 / GetAjaxAction.java:40 |
| 3 | CRITICAL | IDOR — attacker-controlled `compId` in last_gps action | GetAjaxAction.java:46 |
| 4 | HIGH | DoS via unbounded unit array in GPS query loop | GPSDao.java:45 / GetAjaxAction.java:45 |
| 5 | HIGH | JSON injection in GPS response (unescaped DB values) | GPSDao.java:64 / unit.gps.jsp |
| 6 | HIGH | XML injection in getDriverName.jsp (unescaped driver names) | getDriverName.jsp:15 |
| 7 | HIGH | XML injection in getAjax.jsp (unescaped name/content values) | getAjax.jsp:20 |
| 8 | HIGH | Wrong Content-Type (text/html) on JSON GPS response | unit.gps.jsp:4 |
| 9 | HIGH | Missing X-Content-Type-Options on XML responses | getAjax.jsp, getDriverName.jsp |
| 10 | MEDIUM | CSRF on getcode.jsp password-reset form | getcode.jsp:12 |
| 11 | MEDIUM | CSRF — no token on GetXmlAction driver list endpoint | GetXmlAction.java |
| 12 | MEDIUM | Information disclosure via unhandled exception in GetXmlAction | GetXmlAction.java:26 |
| 13 | MEDIUM | NPE / stack trace disclosure in getDriverName.jsp | getDriverName.jsp:11 |
| 14 | MEDIUM | NPE on null session attributes in last_gps branch | GetAjaxAction.java:47 |
| 15 | LOW | Plain `<form>` tag bypasses Struts CSRF token helper | getcode.jsp:12 |
| 16 | LOW | No server-side email validation in GoResetPassAction | GoResetPassAction.java:24 |
| 17 | LOW | Second-order SQL injection risk via `sessTimezone` in SQL | DriverDAO.java:358 |
| 18 | INFO | AJAX/XML endpoints correctly protected by auth gate | PreFlightActionServlet.java |
| 19 | INFO | getAllDriver correctly parameterised and tenant-scoped | DriverDAO.java:76 |

---

**CRITICAL: 3 / HIGH: 6 / MEDIUM: 5 / LOW: 3 / INFO: 2**
