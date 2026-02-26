# Pass 2 Test Coverage Audit — Agent B06
**Audit Run:** 2026-02-26-01
**Agent:** B06
**Scope:** JSP view test coverage, XSS risk, scriptlet logic, missing error handling, hardcoded values

---

## Test Directory Summary

**Directory audited:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Existing test files (4 total):**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep results for all 8 JSP names (json_result, success, search, add-alert, manufacturers, manufacturersList, profile, settings):** No matches found in any test file.

All 8 JSP files are completely untested. The only existing tests cover calibration utilities and are entirely unrelated to view rendering.

---

## JSP File Analyses

---

### 1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/result/json_result.jsp`

**Purpose:** A JSON result dispatcher used as a Struts action result view. Reads a `result` request attribute, matches it against the string "success", and emits a hand-crafted JSON literal as the response body. The page has no `Content-Type` declaration.

**Scriptlet blocks:**
```jsp
<%
String message = "";
String result = request.getAttribute("result") ==  null ? "" :  request.getAttribute("result").toString();

if( result.equalsIgnoreCase("success")){
    message = "{ \"status\":\"success_close\", \"message\":\"Mail has been sent\" }";
}else{
    message = "{ \"status\":\"error\", \"message\":\"Sending Failed.\" }";
}
%>
<%=message %>
```

**EL expressions / request attribute accesses:**
- `request.getAttribute("result")` — read via scriptlet, not EL.

**JavaScript with security implications:** None in this file.

**Test grep results:** No test references found for `json_result`.

---

### 2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/result/success.jsp`

**Purpose:** A Struts XML result configuration fragment (not a rendered HTML page). It returns an HTTP 200 response with an `empty` result type using the `httpheader` result type.

**Scriptlet blocks:** None.

**EL expressions / request attribute accesses:** None.

**JavaScript with security implications:** None.

**Test grep results:** No test references found for `success`.

---

### 3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/search.jsp`

**Purpose:** Driver/vehicle search form. Renders a Struts HTML form with a typeahead text field, two select dropdowns (unit, attachment), and submit/print buttons. Fetches driver XML data via AJAX on page load to populate typeahead suggestions. Includes print and barcode popup functionality.

**Scriptlet blocks:** None (no Java scriptlets).

**EL expressions / request attribute accesses (via Struts tags):**
- `name="arrUnit"` — collection iterated for vehicle select options.
- `property="arrAttachment"` — collection iterated for attachment select options.
- `property="fname"` — form bean property (driver name text field).
- `property="veh_id"` — form bean property (vehicle select).
- `property="attachment"` — form bean property (attachment select).

**JavaScript with security implications:**
- Line 52–69: AJAX call to `getXml.do?` using `jQuery.browser.msie` (deprecated API, removed in jQuery 1.9+). Falls back to ActiveX `Microsoft.XMLDOM` for IE — legacy Internet Explorer-only code path with no CSP consideration.
- Lines 88, 102–106: `fnprint()` and `fnbarcode()` build a URL string using raw DOM field values (`veh_id`, `att_id`, `dname`) and pass them to `window.open()`. The `dname` value (driver name, user-influenced via typeahead) is injected into the URL without encoding.
- Line 67: `error:function(err){alert(err)}` — exposes raw XHR error objects to the user via `alert()`.
- Line 55: `jQuery.browser` usage — this property was removed from jQuery core and its presence indicates an unpatched legacy jQuery version is in use.
- Line 59: `ActiveXObject('Microsoft.XMLDOM')` — IE-specific instantiation, present in production code with no browser version gating except the removed `jQuery.browser.msie` flag.

**Test grep results:** No test references found for `search`.

---

### 4. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/add-alert.jsp`

**Purpose:** A modal form to associate an alert with an admin entity. Renders a single `<html:select>` populated from a `alertList` collection and submits to `adminAlertAdd.do`. Contains a hidden `src` field hardcoded to `"alert"`.

**Scriptlet blocks:** None.

**EL expressions / request attribute accesses (via Struts tags):**
- `collection="alertList"` — `alert_id` and `alert_name` properties iterated for the select options.
- `property="alert_id"` — form bean property bound to select.

**JavaScript with security implications:** None in-page.

**Notable structural issue:**
- Line 10: `<html:select>` has a `style` attribute set to `"adminalert.do?action=alerts"` — a URL has been placed in a CSS `style` attribute. This appears to be either a misplaced attribute (should be `data-url` or similar) or a developer error. It has no functional CSS effect and is confusing.

**Test grep results:** No test references found for `add-alert` or `addAlert`.

---

### 5. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`

**Purpose:** Manufacturer management page. Renders a table of manufacturers from the `arrManufacturers` session/request attribute. Each row has inline edit, save, and delete buttons wired to AJAX handlers. AJAX responses are parsed as JSON and the table is re-rendered via `prepareTable()` using string concatenation into `innerHTML`.

**Scriptlet blocks:**
```jsp
value="<%= manufacturer.getName() %>"
id="manufacturer-edit-<%= manufacturer.getId() %>"
id="edit-<%= manufacturer.getId() %>"
id="save-<%= manufacturer.getId() %>"
```
Four scriptlet expressions inline in HTML attribute values, accessing `ManufactureBean.getName()` and `ManufactureBean.getId()`.

**EL expressions / request attribute accesses (via Struts tags and scriptlets):**
- `name="arrManufacturers"` — iterated via `<logic:iterate>`, type `com.bean.ManufactureBean`.
- `<bean:write property="name" name="manufacturer"/>` — renders manufacturer name.
- `<bean:write property="id" name="manufacturer"/>` — renders manufacturer ID inline in `onclick` attributes.
- `<logic:notEmpty property="company_id" name="manufacturer">` — conditionally renders edit/save/delete buttons.
- `manufacturer.getName()` via scriptlet — used as an `input` value attribute.
- `manufacturer.getId()` via scriptlet — used as element `id` suffix.

**JavaScript with security implications:**
- Lines 151–152, `prepareTable()`: Server JSON response is parsed and `elem.name` and `elem.id` are concatenated directly into HTML strings that are assigned to `table.html(html)`. If `elem.name` contains HTML special characters (e.g., `<`, `>`, `"`, `'`), this constitutes a stored XSS vector. No escaping is applied.
- Lines 155–168: Button `onclick` attribute values in the dynamically built HTML string embed `elem.id` without validation. If `elem.id` is not a pure integer (attacker-controlled or server bug), JavaScript injection is possible in the `onclick` handler.
- Line 54: The server-side `input` tag uses `value="<%= manufacturer.getName() %>"` without HTML-encoding. A manufacturer name containing `"` or `>` would break out of the attribute and could inject attributes or script.
- Lines 60, 65, 70: `<bean:write property="id" name="manufacturer"/>` is embedded inside HTML `onclick="edit_manufacturer(...)"` — if the id is non-numeric, JavaScript injection results.
- `delete_manufacturer` (line 123–142): Issues a GET to `isVehicleAssigned` passing `manufacturerId` from a JS variable populated by the unescaped `elem.id`. The response is parsed with `JSON.parse(data).value` without guarding for parse errors.

**Test grep results:** No test references found for `manufacturers` or `manufacturersList`.

---

### 6. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturersList.jsp`

**Purpose:** Emits a JSON representation of the manufacturer list. Sets `Content-Type: application/json`. Retrieves a `JSONObject` directly from the HTTP **session** (not request) and outputs it via `<%=obj%>`.

**Scriptlet blocks:**
```jsp
<%@ page import="com.json.JSONObject"%>
<%
    JSONObject obj = (JSONObject)request.getSession().getAttribute("json");
%>
<%=obj%>
```

**EL expressions / request attribute accesses:**
- `request.getSession().getAttribute("json")` — reads a `JSONObject` from session scope.

**JavaScript with security implications:** None in-page.

**Test grep results:** No test references found for `manufacturersList`.

---

### 7. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/profile.jsp`

**Purpose:** Company profile edit form. Renders company name, address, contact first/last name, email, mobile, password, and confirm-password fields. Submits to `adminRegister.do`. Includes client-side validation in `fnsubmitAccount()` before form submission.

**Scriptlet blocks:**
```jsp
var smsUsrAlertExisting = <%=request.getAttribute("userSmsAlertExisting")%>;
```
Single scriptlet expression inside a JavaScript `<script>` block. The value of `userSmsAlertExisting` is injected directly into JavaScript source.

**EL expressions / request attribute accesses (via Struts tags):**
- `name="companyRecord"` — iterated via `<logic:iterate>`, type `com.bean.CompanyBean`.
- `property="name"` / `name="company"` — company name field.
- `property="address"` / `name="company"` — address textarea.
- `property="contact_fname"` / `name="company"` — contact first name.
- `property="contact_lname"` / `name="company"` — contact last name.
- `property="email"` / `name="company"` — email.
- `property="mobile"` / `name="company"` — mobile number.
- `request.getAttribute("userSmsAlertExisting")` — via scriptlet, embedded in JS.
- `property="accountAction"` — hidden field hardcoded to `"update"`.

**JavaScript with security implications:**
- Line 110: `var smsUsrAlertExisting = <%=request.getAttribute("userSmsAlertExisting")%>;` — If `userSmsAlertExisting` is `null` (attribute not set), the rendered output is `var smsUsrAlertExisting = null;` which is valid JavaScript. However, if an attacker can influence this attribute value (e.g., through a crafted request or data injection upstream), arbitrary JavaScript could be injected into the page. There is no escaping or type coercion applied.
- Line 133: `cmobile.startsWith("+")` — client-side only validation. No indication of server-side enforcement.
- Lines 131–136: Mobile number validation (`isNaN`, `startsWith`) is JavaScript-only; bypassing is trivial.
- Line 94: `onclick="fnsubmitAccount();"` on an anchor tag (`<a href="#">`) — the form relies entirely on JS for submission control. With JS disabled the form submits unconditionally.

**Test grep results:** No test references found for `profile`.

---

### 8. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/settings.jsp`

**Purpose:** Company settings form. Manages date format, timezone, max session length, notification checkboxes (Red Impact Email, Red Impact SMS, Training Expiry Email), and a Super Admin-only calibration trigger button. Client-side `isValid()` validation runs before form submit.

**Scriptlet blocks:**
```jsp
<%
    String dateFormat = (String) session.getAttribute("sessDateTimeFormat");
    String compTimezone = (String) session.getAttribute("timezoneId");
%>
```
And in the script block:
```jsp
var dateFormat = "<%=dateFormat %>";
...
$('#timezone').val("<%=compTimezone %>");
```
Two scriptlet declarations reading session attributes, then two scriptlet expressions injecting those values unescaped into JavaScript string literals.

**EL expressions / request attribute accesses (via Struts tags and scriptlets):**
- `session.getAttribute("sessDateTimeFormat")` — date format string from session.
- `session.getAttribute("timezoneId")` — timezone ID string from session.
- `name="dateFormats"` — iterated via `<logic:iterate>`, type `com.bean.DateFormatBean`.
- `name="timezones"` — iterated via `<logic:iterate>`, type `com.bean.TimezoneBean`.
- `name="isSuperAdmin"` — `<logic:equal>` gate controlling calibration button visibility.
- `name="redImpactAlert"` — `<logic:notEmpty>/<logic:empty>` controls checkbox checked state.
- `name="redImpactSMSAlert"` — same pattern.
- `name="driverDenyAlert"` — same pattern.
- `property="mobile"` / `name="company"` — hidden field for mobile.
- `property="maxSessionLength"` / `name="company"` — session length text input.

**JavaScript with security implications:**
- Lines 171–174:
  ```javascript
  var dateFormat = "<%=dateFormat %>";
  $('#timezone').val("<%=compTimezone %>");
  ```
  Both `dateFormat` and `compTimezone` are session-sourced strings injected directly into JavaScript string literals without escaping. If either contains a double-quote or backslash (e.g., timezone names in some locales or a corrupted session value), this breaks the JS string and could be exploited for script injection.
- Line 147: `document.AdminSettingsActionForm.maxSessionLength.value < 15` — numeric comparison against a string value retrieved from a DOM input. JavaScript type coercion makes this work normally but it is not explicit; an empty string coerces to `0` (which is `< 15` and would trigger the error), but `"abc"` coerces to `NaN` which is not `< 15` and bypasses the check.
- Line 181–187, `calibrate()`: The AJAX `success` callback is `swal(...)` called immediately (not as a function reference). The `swal` call fires when the `$.ajax()` is constructed, not when the request completes, regardless of actual success or failure of the server call.
- Line 75: The "Run Unit Calibration Job" button is hidden behind `<logic:equal name="isSuperAdmin" value="true">` server-side, but the `calibrate()` JS function itself is always present in the page source and can be called from the browser console by any authenticated user who can view the page source. There is no server-side authorization check visible in this JSP.

**Test grep results:** No test references found for `settings`.

---

## Findings

### json_result.jsp

**B06-1 | Severity: HIGH | No Content-Type header declared in json_result.jsp**
The JSP emits a JSON body but has no `<%@ page contentType="application/json"%>` directive. The server will serve this as `text/html` by default. Consumers expecting `application/json` may misparse the response; browsers may apply HTML rendering rules to the body, and XSS filters may not engage correctly.

**B06-2 | Severity: MEDIUM | Binary success/error classification loses error detail in json_result.jsp**
The scriptlet maps every non-"success" value of the `result` attribute to a generic `"Sending Failed."` error message regardless of the actual failure cause (network error, auth failure, invalid recipient, etc.). No test covers the range of possible `result` values or verifies that partial-failure states produce meaningful feedback.

**B06-3 | Severity: LOW | No test coverage for json_result.jsp scriptlet logic**
The `result` attribute null-handling and case-insensitive string comparison (`equalsIgnoreCase("success")`) are untested. A null `result` attribute silently falls to the error branch with no indication this occurred; there is no test verifying this behavior.

---

### success.jsp

**B06-4 | Severity: INFO | success.jsp is a Struts result configuration fragment, not a rendered view**
The file contains only a `<result>` XML element. It is not a JSP page in the usual sense. No test coverage is applicable or expected for this file directly; however, no integration test verifies that the action producing this result actually returns HTTP 200.

---

### search.jsp

**B06-5 | Severity: HIGH | Unencoded driver name injected into URL in fnprint() and fnbarcode()**
In `fnprint()` (line 88) and `fnbarcode()` (lines 102–106), the value of `document.searchActionForm.fname.value` (the `dname` field) is concatenated directly into a URL string passed to `window.open()`. The driver name field is populated from a typeahead backed by server XML data; any name containing `&`, `=`, `#`, or other special characters will corrupt the URL. If the server does not encode the XML data, a crafted name could inject additional query parameters into the `print.do` or barcode request.

**B06-6 | Severity: HIGH | Use of removed jQuery.browser API indicates unpatched jQuery**
Line 55 uses `jQuery.browser.msie`, which was removed in jQuery 1.9. This API always evaluates to `undefined` (falsy) in modern jQuery. The result is that the `ActiveXObject` branch is never taken via this check, and the IE-specific XML parsing path is permanently dead. This also confirms the application is using a jQuery version old enough to have retained this API, which likely contains known security vulnerabilities.

**B06-7 | Severity: MEDIUM | Raw XHR error object exposed to user via alert()**
Line 67: `error:function(err){alert(err)}` passes the raw jQuery XHR error object to `alert()`. This leaks internal server information (status codes, error messages) to the end user and provides no structured error handling. No test covers error path behavior.

**B06-8 | Severity: MEDIUM | ActiveXObject IE fallback is dead code and cannot be tested**
The `ActiveXObject('Microsoft.XMLDOM')` block (lines 59–62) is unreachable in any modern browser because `jQuery.browser.msie` is always falsy. It is also untestable in a JVM test environment. This block should be audited for removal.

**B06-9 | Severity: LOW | No test coverage for search.jsp form rendering or AJAX data loading**
`arrUnit` and `arrAttachment` collection rendering, the typeahead population flow, and the print button visibility logic (`fnshowprint`) are entirely untested.

---

### add-alert.jsp

**B06-10 | Severity: HIGH | URL placed in CSS style attribute — likely misrouted data attribute**
Line 10: `style="adminalert.do?action=alerts"` on the `<html:select>` element. A URL has been placed in the `style` attribute. This is either a developer error (intended as a `data-url` attribute) or an attempt to wire a dynamic URL via CSS that will not work. If a JavaScript framework reads `element.style` to discover the endpoint URL, this is an undocumented and fragile coupling. No test verifies the intended behavior.

**B06-11 | Severity: LOW | No test coverage for add-alert.jsp alertList rendering or form submission**
The `alertList` collection is not tested for null/empty states. The hidden `src` field hardcoded to `"alert"` has no test verifying this value is expected and processed correctly server-side.

---

### manufacturers.jsp

**B06-12 | Severity: CRITICAL | Stored XSS via unescaped manufacturer name in prepareTable() innerHTML construction**
In `prepareTable()` (lines 151–152), `elem.name` from the parsed JSON response is concatenated directly into an HTML string that is assigned to `table.html(html)`. A manufacturer name stored in the database containing `<script>alert(1)</script>` or `"><img src=x onerror=alert(1)>` will execute when the table is re-rendered after any CRUD operation. This is a stored XSS vulnerability. The `value="' + elem.name + '"` pattern on line 152 also breaks out of the attribute context if `elem.name` contains a single quote.

**B06-13 | Severity: CRITICAL | Unescaped manufacturer name in server-side input value attribute (XSS)**
Line 54: `value="<%= manufacturer.getName() %>"` — The manufacturer name is inserted into an HTML attribute value without HTML entity encoding. A name containing `"` breaks out of the attribute; a name containing `>` or additional attributes could inject arbitrary HTML or event handlers. The `<bean:write>` tag used elsewhere applies escaping by default, but this scriptlet expression bypasses that protection.

**B06-14 | Severity: HIGH | JavaScript injection risk via unvalidated ID in onclick attributes**
Lines 59–70 embed `<bean:write property="id" name="manufacturer"/>` directly inside `onclick="edit_manufacturer(...)"`, `onclick="save_manufacturer(...)"`, and `onclick="delete_manufacturer(...)"`. If `id` is not strictly numeric (database corruption, type mismatch, or injection via the edit flow), arbitrary JavaScript executes. The same risk exists in `prepareTable()` lines 154–166 where `elem.id` is concatenated into onclick strings.

**B06-15 | Severity: HIGH | JSON parse error not handled in delete_manufacturer and prepareTable**
`JSON.parse(data)` in `delete_manufacturer` (line 126) and `prepareTable` (line 146) are not wrapped in try/catch. A non-JSON server error response (e.g., a Struts error page returning HTML, a 500 with a stack trace) will throw an uncaught exception, silently failing with no user feedback.

**B06-16 | Severity: MEDIUM | Duplicate class attribute on input element**
Line 54–55: The `<input>` element has `class="form-control"` set both inline (`class="form-control"`) and again as a second `class` attribute (`class="manufacturer"`). Only the first `class` attribute is recognized by browsers; the `manufacturer` class is silently dropped. The `save_manufacturer` function may depend on the `manufacturer` class for selection logic.

**B06-17 | Severity: LOW | No test coverage for manufacturers.jsp rendering or AJAX CRUD flows**
The `arrManufacturers` null/empty branch (`<logic:notEmpty>`), the `company_id` conditional display of action buttons, and all three AJAX functions are untested.

---

### manufacturersList.jsp

**B06-18 | Severity: CRITICAL | NullPointerException when session attribute "json" is absent**
Line 8–10: `JSONObject obj = (JSONObject)request.getSession().getAttribute("json");` followed by `<%=obj%>`. If the `json` session attribute has not been set (session expired, first request, or action failure), `obj` is `null` and `<%=obj%>` renders the string `"null"` which is technically valid JSON. However, if `obj.toString()` is called (which `<%=obj%>` does implicitly), a `NullPointerException` will be thrown at runtime, producing a 500 error response. The rendered output would be an empty or error page where a JSON array is expected. No null guard exists.

**B06-19 | Severity: HIGH | JSON data retrieved from session scope, not request scope**
The `json` attribute is stored in the HTTP **session** (`request.getSession().getAttribute("json")`). Session-scoped JSON responses are shared across concurrent requests in the same session (e.g., two browser tabs). A race condition between two simultaneous manufacturer operations in the same session can cause one tab to receive the other tab's response data, corrupting the displayed manufacturer list.

**B06-20 | Severity: LOW | No test coverage for manufacturersList.jsp null session attribute or response content**
No test verifies the JSON structure of the response, the null-session-attribute error path, or the content-type header (`application/json` declared at line 3).

---

### profile.jsp

**B06-21 | Severity: HIGH | Unescaped request attribute injected into JavaScript in profile.jsp**
Line 110: `var smsUsrAlertExisting = <%=request.getAttribute("userSmsAlertExisting")%>;`
The `userSmsAlertExisting` request attribute is injected directly into a JavaScript variable assignment without any encoding or type enforcement. If this attribute is `null` (not set by the action), the output is `var smsUsrAlertExisting = null;` — valid but unintended. If an attacker can manipulate this attribute (e.g., via a crafted upstream data source or a future code path), arbitrary JavaScript can be injected. No escaping via `StringEscapeUtils.escapeEcmaScript()` or equivalent is applied.

**B06-22 | Severity: MEDIUM | Client-side-only mobile number validation in profile.jsp**
Lines 131–136 validate that the mobile number is numeric and starts with `"+"` using JavaScript only. This validation is bypassable by any user who disables JavaScript or sends a direct HTTP POST to `adminRegister.do`. No server-side validation evidence is visible in this JSP.

**B06-23 | Severity: MEDIUM | Password transmitted and compared client-side before POST**
Lines 107–108: `var pass = $('[name="pin"]').val(); var cpassword = $('[name="cpassword"]').val();` — password match validation occurs client-side. The actual password value is transmitted in plaintext POST body. While HTTPS would protect the transport, the client-side match check is bypassable and the minimum-length check (line 124) can also be bypassed. No indication of server-side minimum-length enforcement.

**B06-24 | Severity: LOW | Form submits unconditionally when JavaScript is disabled**
Line 94: The Save button is an `<a>` tag with `onclick="fnsubmitAccount();"`. When JavaScript is disabled, clicking this link navigates to `#` and the form is never submitted. This is a usability gap. Separately, if a malicious actor crafts a direct POST, all client-side validation (including the mobile number format check and password match check) is bypassed entirely.

**B06-25 | Severity: LOW | No test coverage for profile.jsp rendering or fnsubmitAccount validation logic**
The `companyRecord` null/empty branch, field binding from `CompanyBean`, and all `fnsubmitAccount` validation paths are untested.

---

### settings.jsp

**B06-26 | Severity: HIGH | Session-sourced strings injected unescaped into JavaScript string literals**
Lines 171–174:
```javascript
var dateFormat = "<%=dateFormat %>";
$('#timezone').val("<%=compTimezone %>");
```
`dateFormat` and `compTimezone` are read from session attributes `sessDateTimeFormat` and `timezoneId` respectively, then injected directly into JavaScript string literals delimited by double quotes. If either value contains a `"` character, a `\`, a newline, or other characters with special meaning in JavaScript string literals, the script block will be malformed. A compromised or corrupted session, or a timezone/format value stored with a double-quote in the database, would produce broken or injectable JavaScript. No escaping (e.g., `StringEscapeUtils.escapeEcmaScript`) is applied.

**B06-27 | Severity: HIGH | calibrate() AJAX success callback fires immediately, not on request completion**
Lines 181–187:
```javascript
$.ajax({
    type: 'POST',
    url: 'calibration.do',
    success: swal("Unit Calibration Job", "Successfully started unit calibration job")
});
```
The `success` property is set to the return value of `swal(...)` (which is `undefined`), not a function reference. The `swal` alert fires synchronously when `$.ajax()` is called, before the HTTP request is made. This means the "Successfully started" message always appears regardless of whether the calibration job actually started, failed, or the request was rejected by the server. This is a logic error that cannot be caught by testing without integration tests.

**B06-28 | Severity: MEDIUM | maxSessionLength NaN bypass in isValid() client-side validation**
Line 147: `document.AdminSettingsActionForm.maxSessionLength.value < 15` — When the field value is a non-numeric string (e.g., `"abc"`), JavaScript's `NaN < 15` evaluates to `false`, silently bypassing the minimum-length check. The form submits with an invalid `maxSessionLength`. No test verifies this edge case, and no server-side coercion is visible in this JSP.

**B06-29 | Severity: MEDIUM | Super Admin calibration endpoint accessible via browser console by any authenticated user**
The `calibrate()` function and the `calibration.do` endpoint are compiled into the page source for all users who can view the settings page. The `<logic:equal name="isSuperAdmin" value="true">` Struts tag hides the button visually, but the JavaScript function is always present and callable. If `calibration.do` does not enforce its own server-side super-admin authorization check, any authenticated user with settings page access can trigger unit calibration by calling `calibrate()` from the browser developer console.

**B06-30 | Severity: LOW | No test coverage for settings.jsp rendering, isValid() validation, or calibrate() behavior**
The `dateFormats` and `timezones` collection rendering, all three checkbox states (`redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`), the `isSuperAdmin` gate, and all `isValid()` validation paths are entirely untested.

---

## Summary Table

| ID     | JSP File              | Severity | Category                                |
|--------|-----------------------|----------|-----------------------------------------|
| B06-1  | json_result.jsp       | HIGH     | Missing Content-Type header             |
| B06-2  | json_result.jsp       | MEDIUM   | Loss of error detail in binary branch   |
| B06-3  | json_result.jsp       | LOW      | No test coverage                        |
| B06-4  | success.jsp           | INFO     | Config fragment, no tests applicable    |
| B06-5  | search.jsp            | HIGH     | Unencoded user input in URL (open redirect / param injection) |
| B06-6  | search.jsp            | HIGH     | Removed jQuery.browser API / outdated jQuery |
| B06-7  | search.jsp            | MEDIUM   | Raw XHR error exposed to user           |
| B06-8  | search.jsp            | MEDIUM   | Dead IE ActiveXObject code              |
| B06-9  | search.jsp            | LOW      | No test coverage                        |
| B06-10 | add-alert.jsp         | HIGH     | URL in style attribute (misrouted data) |
| B06-11 | add-alert.jsp         | LOW      | No test coverage                        |
| B06-12 | manufacturers.jsp     | CRITICAL | Stored XSS via innerHTML string concat  |
| B06-13 | manufacturers.jsp     | CRITICAL | Unescaped scriptlet in HTML attribute (XSS) |
| B06-14 | manufacturers.jsp     | HIGH     | JS injection via unvalidated ID in onclick |
| B06-15 | manufacturers.jsp     | HIGH     | Unhandled JSON.parse exceptions         |
| B06-16 | manufacturers.jsp     | MEDIUM   | Duplicate class attribute, silently dropped |
| B06-17 | manufacturers.jsp     | LOW      | No test coverage                        |
| B06-18 | manufacturersList.jsp | CRITICAL | NPE on null session attribute           |
| B06-19 | manufacturersList.jsp | HIGH     | Race condition: session-scoped JSON     |
| B06-20 | manufacturersList.jsp | LOW      | No test coverage                        |
| B06-21 | profile.jsp           | HIGH     | Unescaped request attribute into JS     |
| B06-22 | profile.jsp           | MEDIUM   | Client-side-only mobile validation      |
| B06-23 | profile.jsp           | MEDIUM   | Client-side-only password validation    |
| B06-24 | profile.jsp           | LOW      | Form inaccessible without JS            |
| B06-25 | profile.jsp           | LOW      | No test coverage                        |
| B06-26 | settings.jsp          | HIGH     | Session strings injected into JS literals unescaped |
| B06-27 | settings.jsp          | HIGH     | calibrate() swal fires before AJAX completes |
| B06-28 | settings.jsp          | MEDIUM   | NaN bypass in maxSessionLength validation |
| B06-29 | settings.jsp          | MEDIUM   | Super admin JS function exposed to all users |
| B06-30 | settings.jsp          | LOW      | No test coverage                        |

**Total findings: 30**
**CRITICAL: 3 | HIGH: 10 | MEDIUM: 8 | LOW: 8 | INFO: 1**

---

## Global Coverage Gap

Zero JSP test files exist. The test suite contains only 4 files, all covering calibration utility classes. There is no test infrastructure for JSP rendering, Struts action integration, session/request attribute wiring, or client-side JavaScript behavior. All scriptlet logic, all conditional rendering branches, and all JavaScript validation functions across these 8 JSPs are entirely untested.
