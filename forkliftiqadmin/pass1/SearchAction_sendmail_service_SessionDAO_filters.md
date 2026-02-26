# Security Audit Report — Pass 1
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Scope:** SearchAction flow, sendmail.jsp, service.jsp / AdminUnitServiceAction, SessionDAO / SessionsByCompanyIdQuery, SessionDriverFilter / SessionDriverFilterHandler, and supporting DAOs called by those paths (DriverDAO.getDriverByFullNm, QuestionDAO.getQuestionByUnitId)

---

## Findings

---

### CRITICAL: SQL Injection via unparameterized driver name in DriverDAO.getDriverByFullNm

**File:** `src/main/java/com/dao/DriverDAO.java` (line 264)

**Description:**
`SearchAction.execute` calls `driverDao.getDriverByFullNm(sessCompId, searchActionForm.getFname(), true)`. The `fname` field originates directly from the HTTP form parameter `searchActionForm.fname` submitted to `search.do`, with no sanitisation in `SearchActionForm` (the `validate` method only checks for empty string, not content). Inside `getDriverByFullNm` the value is spliced directly into a SQL string using `Statement`, not `PreparedStatement`:

```java
// DriverDAO.java line 263-264
// FIXME Use string constant to avoid to re-instantiating new string at every call.
// Also work with prepared statement to prevent SQL injection.
String sql = "select id,first_name,last_name,active,comp_id,licno from driver " +
    "where first_name||' '||last_name ilike '" + fullName + "' and comp_id = " + compId;
```

The comment in the code confirms the developers were aware of the problem. Because the database is PostgreSQL and the operator is `ilike`, an attacker can inject arbitrary SQL by submitting a crafted `fname` value such as:

```
' OR '1'='1
```

or (for data exfiltration via a UNION):

```
' UNION SELECT id,username,password,active,comp_id,licno FROM users--
```

Note also that `compId` is concatenated without quoting, which is a secondary injection point if `sessCompId` could ever be tampered with (it comes from the session, so direct exploitation requires session compromise, but the code pattern is still incorrect).

**Risk:** An authenticated attacker can read arbitrary data from the database, bypass row-level tenant scoping to access other companies' driver records, and potentially modify or delete data depending on the database account's privileges. This is the highest-severity finding in the audited scope.

**Recommendation:** Replace the `Statement` with a `PreparedStatement` and bind all user-controlled values as parameters:
```java
String sql = "select id,first_name,last_name,active,comp_id,licno from driver " +
    "where first_name||' '||last_name ilike ? and comp_id = ? and active = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, fullName);
ps.setInt(2, Integer.parseInt(compId));
ps.setBoolean(3, status);
```

---

### CRITICAL: SQL Injection via unparameterized unitId, attachmentId, compId, and lanId in QuestionDAO.getQuestionByUnitId

**File:** `src/main/java/com/dao/QuestionDAO.java` (lines 82–93)

**Description:**
`SearchAction.execute` calls `quesionDao.getQuestionByUnitId(searchActionForm.getVeh_id(), searchActionForm.getAttachment(), sessCompId, false)`. Both `veh_id` and `attachment` come from HTTP request parameters; `sessCompId` comes from the session. All three are concatenated directly into a SQL string that is executed via a raw `Statement`:

```java
// QuestionDAO.java lines 82-93
String sql = "select question.id,question.content,expectedanswer,order_no,answer_type,question_content.content " +
        "from question" +
        " left outer join question_content on question_content.question_id = question.id and lan_id = " + lanId +
        " left outer join unit on unit.type_id = question.type_id" +
        " where unit.id = " + unitId +
        " and unit.fuel_type_id = question.fule_type_id and unit.manu_id = question.manu_id" +
        " and (question.comp_id is null or question.comp_id = " + compId + ")";
if (attchId.equalsIgnoreCase("0")) {
    sql += " and attachment_id is null ";
} else {
    sql += " and (attachment_id is null or attachment_id = " + attchId + ")";
}
```

The `lanId` value is itself the result of `getQuesLanId(compId)` which also uses a raw concatenated Statement (line 42: `"select lan_id from company where id = " + compId`). Any of the four injection points (`unitId`, `attchId`, `compId`, `lanId`) allows arbitrary SQL.

`veh_id` and `attachment` receive no numeric validation in `SearchActionForm.validate` — only a check that `veh_id` is not empty; `attachment` is unchecked. An attacker can send `veh_id=1 UNION SELECT ...` to extract data.

**Risk:** Full SQL injection. Data from any table readable by the database account can be exfiltrated. Combined with the `getDriverByFullNm` finding, these two entry points make the `search.do` endpoint extremely high risk for any authenticated session.

**Recommendation:** Convert all four DAOs (`getQuesLanId`, `getQuestionByUnitId`, and any derived call) to `PreparedStatement`. Enforce numeric validation on `veh_id` and `attachment` in `SearchActionForm.validate` (reject non-integer values immediately):
```java
try { Integer.parseInt(veh_id); } catch (NumberFormatException e) { errors.add(...); }
```

---

### CRITICAL: SQL Injection in QuestionDAO.delQuestionById and QuestionDAO.getQuestionById

**File:** `src/main/java/com/dao/QuestionDAO.java` (lines 183, 275, 328, 330)

**Description:**
Although not directly called from the audited `SearchAction` path, these methods are called from admin-facing actions and share the same DAO file in scope. They use raw Statement concatenation:

```java
// line 183 — destructive write operation
String sql = "delete from question where id=" + id;

// line 275 — read
String sql = "select id,content,...,active from question where id = " + id;

// lines 328/330 — read (getQuestionContentById)
sql = "select content from question where id = " + qId;
sql = "select content from question_content where question_id = " + qId + " and lan_id = " + lanId;
```

`delQuestionById` in particular is a destructive operation where injection can cause bulk deletion of question rows.

**Risk:** Data destruction or exfiltration in the question bank. If called from any endpoint that accepts user input without strict integer validation the impact is critical.

**Recommendation:** All four statements must use `PreparedStatement`. For `id`, `qId`, and `lanId` values, validate that they are numeric integers before use.

---

### HIGH: IDOR — AdminUnitServiceAction accepts arbitrary unitId without company ownership check

**File:** `src/main/java/com/action/AdminUnitServiceAction.java` (lines 52, 61) and `src/main/webapp/html-jsp/vehicle/service.jsp` (line 181)

**Description:**
The `service.jsp` form embeds the raw request parameter `equipId` into a hidden field with no server-side binding to the session company:

```jsp
<!-- service.jsp line 181 -->
<input type="hidden" name="oldId" id="oldId" value="<%=id %>"/>
```

`id` is read directly from `request.getParameter("equipId")` at line 4 with no ownership verification. The form POSTs to `adminunitservice.do`, which calls `AdminUnitServiceAction.execute`. That action reads `serviceForm.getUnitId()` directly from form fields (populated by Struts from request parameters) and calls `UnitDAO.saveService(serviceBean)` — which writes service records for whatever `unitId` is submitted:

```java
// AdminUnitServiceAction.java line 52, 61
serviceBean.setUnitId(serviceForm.getUnitId());
...
UnitDAO.getInstance().saveService(serviceBean);
```

Neither `AdminUnitServiceAction` nor `saveService` validates that the submitted `unitId` belongs to `sessCompId`. An authenticated user of company A can therefore submit `unitId` belonging to company B and overwrite that unit's service data.

Additionally, the tab navigation links in `service.jsp` (lines 18, 27) use the raw `id` value without encoding in `href` attributes, which compounds the IDOR by allowing navigation to any unit's settings page.

**Risk:** Cross-tenant data modification. Any authenticated user can corrupt service records for vehicles belonging to any other company.

**Recommendation:** In `AdminUnitServiceAction`, after reading `serviceForm.getUnitId()`, query the database to confirm that the unit belongs to `sessCompId` before writing. For example:
```java
String sessCompId = (String) session.getAttribute("sessCompId");
if (!UnitDAO.getInstance().unitBelongsToCompany(serviceForm.getUnitId(), sessCompId)) {
    return mapping.findForward("accessDenied");
}
```
Apply the same check on the read path (when loading `service.jsp`).

---

### HIGH: IDOR — service.jsp tab links pass unvalidated equipId back into admin action URLs

**File:** `src/main/webapp/html-jsp/vehicle/service.jsp` (lines 8, 18, 19, 27, 28)

**Description:**
The JSP reads `equipId` from the request parameter without any ownership check and uses it to construct navigation URLs directly in the rendered HTML:

```java
// service.jsp lines 3-11
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String id     = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
...
if (!id.equalsIgnoreCase("")) {
    urlGeneral = "adminunit.do?action=edit&equipId=" + id;
} else {
    urlGeneral = "adminunit.do?action=add";
}
```

An attacker can pass any `equipId` and the page will render navigation links targeting that unit. The server never confirms that the session's company owns the requested `equipId`. This allows cross-tenant browsing, not just write access.

**Risk:** Tenant isolation broken at the read level. Combined with the write-side IDOR above, a full cross-tenant unit management attack is possible.

**Recommendation:** Before rendering the page, confirm that the unit identified by `equipId` belongs to `sessCompId`. Reject the request with an error or redirect if the check fails.

---

### HIGH: CSRF — All state-changing POST endpoints lack anti-CSRF tokens

**File:** `src/main/webapp/html-jsp/search.jsp` (line 8), `src/main/webapp/html-jsp/mod/sendmail.jsp` (line 15), `src/main/webapp/html-jsp/vehicle/service.jsp` (line 34)

**Description:**
None of the three forms include a CSRF synchronizer token. The Struts 1.3.10 framework does not add CSRF protection automatically. No evidence of a CSRF token was found in the struts-config.xml, the action forms (SearchActionForm, AdminSendMailActionForm, AdminUnitServiceForm), or their actions:

```jsp
<!-- search.jsp line 8 — no token -->
<html:form method="post" action="search.do">

<!-- sendmail.jsp line 15 — no token -->
<html:form method="post" action="sendMail.do" styleClass="ajax_mode_x">

<!-- service.jsp line 34 — no token -->
<html:form method="post" action="adminunitservice.do" styleClass="ajax_mode_c serv_form unit_sform">
```

An attacker who can lure an authenticated admin to a malicious page can silently trigger driver searches (which initiate the registration flow), send invitation emails to attacker-controlled addresses, or overwrite vehicle service data.

The `sendMail.do` endpoint is the most exploitable: a CSRF attack can cause the application to send email from `info@ciiquk.com` (the company's domain) to any address supplied by the attacker, enabling phishing abuse of the company's mail reputation.

**Risk:** Session riding. The most severe consequence is unsolicited email dispatch (phishing vector) and arbitrary vehicle service record mutation, all silently triggered from a third-party page.

**Recommendation:** Implement the synchronizer token pattern. In Struts 1.x, use `saveToken(request)` in each action's GET handler and `isTokenValid(request, true)` in the POST handler. Alternatively, adopt a servlet filter that checks `Origin` / `Referer` headers and adds a hidden `_csrf` field to all forms.

---

### HIGH: Reflected XSS via unencoded `dname` parameter in print.do URL constructed in JavaScript

**File:** `src/main/webapp/html-jsp/search.jsp` (lines 88, 102, 106)

**Description:**
The `fnprint()` and `fnbarcode()` JavaScript functions read the raw value of the `fname` form field and concatenate it unsanitised into a URL string opened in a popup window:

```javascript
// search.jsp lines 86-88
var dname = document.searchActionForm.fname.value;
var url = "print.do?veh_id="+veh_id+"&att_id="+att_id+"&dname="+dname+"&action=print";
window.open(url, "Report", "top=5,left=5,width=700,height=700,scrollbars=1");
```

The `dname` value is not URL-encoded before being appended. If the `print.do` action reflects the `dname` parameter back into HTML (which is the common behaviour for print/report pages), a value such as `"><img src=x onerror=alert(1)>` in the `fname` field would be reflected as XSS in the popup window. Even if `print.do` itself is safe, the lack of `encodeURIComponent` breaks URL correctness for names containing spaces, ampersands, or other special characters, and produces a URL-injection vector.

**Risk:** Stored or reflected XSS in the print popup. If `print.do` is audited and found to reflect the parameter unsanitised, this becomes an exploitable XSS chain. The `fname` typeahead field is visible to all authenticated operators.

**Recommendation:** URL-encode all user-supplied values before building URL strings:
```javascript
var url = "print.do?veh_id=" + encodeURIComponent(veh_id) +
          "&att_id=" + encodeURIComponent(att_id) +
          "&dname=" + encodeURIComponent(dname) + "&action=print";
```
The downstream `print.do` action must also HTML-escape the `dname` parameter before rendering.

---

### HIGH: Unvalidated `driverIdFieldName` injected into SQL fragment in SessionDriverFilterHandler

**File:** `src/main/java/com/querybuilder/filters/SessionDriverFilterHandler.java` (line 19)

**Description:**
`SessionDriverFilterHandler` uses `String.format` to embed `driverIdFieldName` (a caller-supplied column name) directly into a SQL fragment:

```java
// SessionDriverFilterHandler.java line 19
return String.format(" AND %s = ? ", driverIdFieldName);
```

The `driverIdFieldName` is supplied by the caller at construction time — currently always the hard-coded literal `"driver_id"` from `SessionsByCompanyIdQuery` (line 26). However, this design makes the class itself unsound: any future caller that supplies a non-literal, user-controlled or database-derived column name would introduce SQL injection through the column name position. SQL parameterization (`?`) does not cover identifiers such as column names, so injecting `driver_id = 1 OR 1=1 --` as the column name would corrupt the query.

The same pattern exists in `SessionUnitFilterHandler` and `DateBetweenFilterHandler` which also receive their field names as constructor arguments (not audited in detail here, but the same concern applies).

**Risk:** Currently not exploitable with the existing callers because the field name is a literal constant. However the design is fragile: a future refactoring that derives the field name from any external input would immediately create SQL injection. This is a latent high-severity vulnerability.

**Recommendation:** Enforce an allowlist of valid column name strings within `getQueryFilter()` (or in the constructor). If the supplied name is not in the allowlist, throw an `IllegalArgumentException`. Example:
```java
private static final Set<String> ALLOWED_COLUMN_NAMES =
    Collections.unmodifiableSet(new HashSet<>(Arrays.asList("driver_id", "unit_driver_id")));

public String getQueryFilter() {
    if (ignoreFilter()) return "";
    if (!ALLOWED_COLUMN_NAMES.contains(driverIdFieldName)) {
        throw new IllegalArgumentException("Invalid column name: " + driverIdFieldName);
    }
    return String.format(" AND %s = ? ", driverIdFieldName);
}
```

---

### MEDIUM: XSS — bean:write renders ServiceBean string fields without HTML escaping in service.jsp

**File:** `src/main/webapp/html-jsp/vehicle/service.jsp` (lines 50, 57)

**Description:**
`<bean:write>` in Struts 1.x HTML-escapes its output **only** when the `filter` attribute is explicitly set to `"true"`. Without that attribute the tag renders the raw bean property value. Both uses in `service.jsp` omit `filter`:

```jsp
<!-- service.jsp line 50 -->
<span><bean:write name="serviceBean" property="servStatus"/></span>

<!-- service.jsp line 57 -->
<bean:write name="serviceBean" property="hoursTillNextService"/>
```

`servStatus` is a `String` computed in `AdminUnitServiceAction` from arithmetic on integer form fields — its current values are hard-coded English sentences, so it is not directly exploitable today. `hoursTillNextService` is a `double` — numeric types are inherently safe. However, `servStatus` is set from free-form string logic, and if its derivation ever incorporates a user-controlled string (or if another property with free-form content is added without `filter="true"`), this becomes XSS. The pattern is consistently unsafe across the application.

**Risk:** Stored XSS if `servStatus` or any other string property rendered via unfiltered `<bean:write>` ever contains user-controlled content.

**Recommendation:** Add `filter="true"` to every `<bean:write>` tag that outputs a String property. For `hoursTillNextService` (a numeric double) the risk is negligible but the attribute should still be set consistently as a coding standard.

---

### MEDIUM: sendmail.jsp — email address value rendered in form without explicit escaping

**File:** `src/main/webapp/html-jsp/mod/sendmail.jsp` (line 22)

**Description:**
The email input is rendered via the Struts `<html:text>` tag. Struts `<html:text>` HTML-escapes its `value` attribute by default, so re-display of the submitted email after a validation failure is safe. The form body itself contains only static text; no request parameter is reflected in the modal content. No XSS vector was identified in this file in isolation.

However, the form provides no CSRF protection (covered in the CSRF finding), and the `body` of the invitation email sent by `AdminSendMailAction.sendMail` is the hard-coded literal `"Driver Invite body"` rather than being derived from user input, so email-injection via the body is not possible at this time.

The `isValidEmailAddress` regex in `AdminSendMailAction` (line 116) is evaluated but does not prevent all categories of abuse (e.g. it allows `+` which is valid but worth noting for abuse-rate-limiting purposes).

**Risk:** Low in isolation. The absence of CSRF (separate finding) means the send-mail action can be triggered cross-origin.

**Recommendation:** No code change needed for XSS on this file. Address the CSRF finding. Consider adding rate-limiting or a CAPTCHA to the invite email flow to prevent mail abuse.

---

### MEDIUM: IDOR risk in SessionDAO — driverId filter is not scoped to sessCompId

**File:** `src/main/java/com/dao/SessionDAO.java` (line 10–16) and `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java` (lines 42–44, 52–54)

**Description:**
`SessionDAO.getSessions` accepts a `companyId` (sourced from `sessCompId` in the calling action) and a `SessionFilterBean` that includes an optional `driverId`. The base query is correctly scoped to the company:

```java
// SessionsByCompanyIdQuery.java line 42
query.append("from v_sessions where (unit_owner_company_id = ? or unit_assigned_company_id = ?)");
```

The `driverId` filter appended by `SessionDriverFilterHandler` is:

```java
// SessionDriverFilterHandler.java line 19
return String.format(" AND %s = ? ", driverIdFieldName);
```

There is no explicit check that the `driverId` supplied in the filter belongs to `companyId`. In practice, the view `v_sessions` already joins unit ownership/assignment to the company constraint, which means the company scoping is applied first and the driver filter then further restricts rows already limited to that company. If the view definition is correct this provides implicit tenant scoping.

However, the security guarantee is entirely dependent on the view's `WHERE` clause. If the view is ever modified or if the query is reused with a different base table, the IDOR protection silently disappears. The DAO layer has no explicit assertion that `driverId` belongs to `companyId`.

**Risk:** Moderate. Currently mitigated by the view, but the design provides no explicit defence-in-depth. If the view definition is incorrect or changes, cross-tenant session data exposure would result.

**Recommendation:** Add an explicit check in the calling action or in `SessionDAO` that the requested `driverId` exists in the current company before passing it to the query builder. Alternatively, join the `driver` table in `SessionsByCompanyIdQuery` and add `AND driver.comp_id = ?` when a driver filter is active, eliminating the reliance on the view.

---

### MEDIUM: Information disclosure — raw SQL is logged at INFO level including user-supplied values

**File:** `src/main/java/com/dao/DriverDAO.java` (line 268), `src/main/java/com/dao/QuestionDAO.java` (lines 96, 182, 275, 329, 330)

**Description:**
The constructed SQL strings, which contain raw user-supplied values, are written to the INFO log before execution:

```java
// DriverDAO.java line 268
log.info(sql);

// QuestionDAO.java line 96
log.info(sql);
```

Any user-supplied value (driver name, unit ID, etc.) therefore appears in application log files. If logs are shipped to a centralised logging service or are accessible to lower-privileged users (e.g. support staff with log access but not DB access), sensitive data such as driver names and IDs are disclosed. More critically, a successful SQL injection payload would also be logged in plaintext, potentially alerting an attacker to what was and was not filtered.

**Risk:** PII (driver names) exposed in logs. SQL injection probes and payloads logged. If logs are long-retained and broadly accessible, this compounds the SQL injection findings.

**Recommendation:** Log the query template (without bound values) at DEBUG level and never at INFO. Once `PreparedStatement` is adopted (as recommended above), the log statement should only include the SQL skeleton with `?` placeholders — never the substituted values.

---

### LOW: Potential NullPointerException on null sessCompId results in 500 error with stack trace

**File:** `src/main/java/com/action/SearchAction.java` (line 41) and `src/main/java/com/actionform/SearchActionForm.java` (line 66)

**Description:**
`SearchAction` reads `sessCompId` with a null-safe guard:

```java
// SearchAction.java line 41
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
```

However, an empty `sessCompId` (which is the fallback value) is subsequently passed to DAO methods that will build invalid SQL (e.g. `comp_id = ` with no value). This could result in a SQL syntax error or uncaught exception propagating to a Tomcat 500 error page — potentially disclosing a stack trace containing the raw SQL with the empty comp_id.

Additionally, `SearchActionForm.validate` calls `fname.equalsIgnoreCase("")` and `veh_id.equalsIgnoreCase("")` without null checks. If `reset()` is called (it resets only `fname` to `""` but not `veh_id` or `attachment`) and the form is then resubmitted without those fields, `veh_id.equalsIgnoreCase("")` will throw a `NullPointerException`, resulting in an unhandled exception.

**Risk:** Low. Results in application errors and possible stack trace disclosure rather than direct data compromise. The auth gate (`PreFlightActionServlet`) should prevent an unauthenticated user from reaching this code, but a partially authenticated or session-expired user could reach `search.do`.

**Recommendation:** Add null checks in `SearchActionForm.validate` before calling `equalsIgnoreCase`. Validate that `sessCompId` is numeric and non-empty before constructing DAO calls; redirect to login if invalid.

---

### LOW: Unsafe AJAX error handler exposes internal error object via alert dialog

**File:** `src/main/webapp/html-jsp/search.jsp` (line 67)

**Description:**
The jQuery AJAX call to `getXml.do` uses a bare `alert(err)` in the error handler:

```javascript
// search.jsp line 67
error: function(err) { alert(err); }
```

`err` in a jQuery AJAX error callback is a `jqXHR` object. When stringified as `[object Object]` it is not directly harmful, but in some browsers the `responseText` property may surface in the alert, potentially exposing internal error details from the server response body. This also represents a poor user experience and exposes the existence of the `getXml.do` endpoint.

**Risk:** Minor information disclosure. Not directly exploitable but represents poor error handling practice.

**Recommendation:** Replace with a user-friendly error message:
```javascript
error: function() { console.error("Failed to load typeahead data."); }
```

---

### INFO: sendMail always returns true even on transport failure

**File:** `src/main/java/com/action/AdminSendMailAction.java` (lines 100–108)

**Description:**
The `Transport.send(message)` call is wrapped in its own try/catch that swallows the exception and only logs to `System.out`. The outer `sendMail` method then unconditionally returns `true`:

```java
// AdminSendMailAction.java lines 99-108
try {
    Transport.send(message);
} catch (Exception e) {
    System.out.println("Transport Exception :" + e);
}
// ...
return true;
```

This means `AdminSendMailAction.execute` will always return `mapping.findForward("success")` even if the email was never delivered. The user and any audit log will be told the invite succeeded when it did not.

**Risk:** No security impact. Operational integrity concern: failed email deliveries are silently masked.

**Recommendation:** Allow the `Transport.send` exception to propagate (or rethrow it), so the calling code can correctly signal failure to the user. Use a proper logger (`log.error(...)`) instead of `System.out.println`.

---

### INFO: Struts LTS version 1.3.10 — framework EOL

**File:** Application-level (pom.xml / struts-config.xml)

**Description:**
Apache Struts 1.x reached end-of-life in April 2013. Version 1.3.10 has multiple known CVEs including the widely exploited ClassLoader manipulation vulnerability (CVE-2014-0114 and related). Although many of these require specific configurations, running an EOL framework on an internet-facing application means no security patches will be released for newly discovered vulnerabilities.

**Risk:** Informational in isolation. Elevates overall attack surface significantly, particularly for deserialization and ClassLoader-based exploits.

**Recommendation:** Plan migration to a supported framework (Spring MVC, Jakarta EE, or Struts 2 with current patches). In the short term, ensure the Struts ClassLoader exploit mitigation is in place (filter on `class` parameter) and that Tomcat is kept current.

---

## Summary

| Severity | Count | Findings |
|----------|-------|---------|
| CRITICAL | 3 | SQL injection in DriverDAO.getDriverByFullNm; SQL injection in QuestionDAO.getQuestionByUnitId; SQL injection in QuestionDAO.delQuestionById / getQuestionById |
| HIGH | 4 | IDOR in AdminUnitServiceAction (cross-tenant unit write); IDOR in service.jsp (cross-tenant navigation); CSRF on search/sendmail/service forms; Reflected XSS via unencoded dname in print URL; latent SQL injection via unvalidated column name in SessionDriverFilterHandler |
| MEDIUM | 4 | XSS via unfiltered bean:write in service.jsp; sendmail.jsp IDOR/CSRF interaction; SessionDAO driverId not explicitly scoped to company; SQL values logged at INFO level |
| LOW | 2 | NullPointerException paths in SearchAction / SearchActionForm; AJAX error handler alert disclosure |
| INFO | 2 | sendMail silently returns true on failure; Struts 1.x EOL framework |

**CRITICAL: 3 / HIGH: 5 / MEDIUM: 4 / LOW: 2 / INFO: 2**
