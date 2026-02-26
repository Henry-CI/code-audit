# Pass 2 Test Coverage Audit — Agent B06
**Audit Run:** 2026-02-26-01
**Agent:** B06
**Date:** 2026-02-26
**Scope:** JSP view test coverage, XSS risk, scriptlet logic, session attribute safety, untestable patterns, hardcoded values, missing authorization checks

---

## Test Directory Summary

**Directory audited:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Existing test files (4 total):**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep results for all JSP names and their action classes:**

All 9 JSP names were searched against the test directory. Pattern searched:
`success|search|add.alert|manufacturer|profile|settings|subscription|general`

Result: **No matches found in any test file.**

Additionally, the following action class names were searched:
`SearchAction|ManufacturerAction|AdminRegisterAction|AdminSettingsAction|AdminDriverAddAction|AdminDriverEditAction|AdminMenuAction|AdminAddAlertAction|AdminAlertAction`

Result: **No matches found in any test file.**

All 9 JSP files are completely untested. The only existing tests cover calibration utility classes and are entirely unrelated to view rendering, session management, or Struts action integration.

---

## JSP File Analyses (Reading Evidence)

---

### 1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/result/success.jsp`

**Purpose:** A Struts XML result configuration fragment, not a rendered HTML page. The file contains a single `<result>` element that configures an HTTP 200 empty-header response. It is referenced in the Struts action result chain rather than rendered as a user-facing view.

**Scriptlet blocks:** None.

**EL expressions / session/request attributes accessed:** None.

**Forms and action URLs:** None.

**Test grep results:** No test references found for `success`.

---

### 2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/search.jsp`

**Purpose:** Driver/vehicle search form. Renders a Struts HTML form with a typeahead text field (`fname`), two select dropdowns (unit `veh_id`, attachment `attachment`), and submit/print buttons. On page load, an AJAX call fetches driver XML data from `getXml.do` to populate typeahead suggestions. Print and barcode popups are triggered via `window.open()`.

**Scriptlet blocks:** None (no Java scriptlets in this file).

**EL expressions / request attribute accesses (via Struts tags):**
- `name="arrUnit"` — collection iterated via `<html:optionsCollection>` for vehicle select options (line 17).
- `property="arrAttachment"` — collection iterated for attachment select options (line 23).
- `property="fname"` — form bean property for driver name typeahead text field (line 11).
- `property="veh_id"` — form bean property for vehicle select (line 15).
- `property="attachment"` — form bean property for attachment select (line 21).

**Forms and action URLs:**
- `<html:form method="post" action="search.do">` (line 8) — submits to `SearchAction`.

**Notable JavaScript patterns:**
- Lines 51–69: AJAX call to `getXml.do?` uses `jQuery.browser.msie` (deprecated, removed in jQuery 1.9) to branch into an `ActiveXObject('Microsoft.XMLDOM')` code path for IE.
- Lines 83–90 (`fnprint()`): `dname` value taken from `document.searchActionForm.fname.value` and appended raw to a URL passed to `window.open()`.
- Lines 92–110 (`fnbarcode()`): Same raw `dname` concatenation into URL for barcode popup.
- Line 67: `error:function(err){alert(err)}` — raw XHR error object exposed via `alert()`.

**Test grep results:** No test references found for `search` or `SearchAction`.

---

### 3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/add-alert.jsp`

**Purpose:** Modal form fragment to subscribe an admin user to a named alert. Renders a single `<html:select>` drop-down populated from the `alertList` collection and submits to `adminAlertAdd.do`. A hidden `<input>` with `name="src"` is hardcoded to `value="alert"`.

**Scriptlet blocks:** None.

**EL expressions / request attribute accesses (via Struts tags):**
- `collection="alertList"` — `alert_id` and `alert_name` properties iterated for select options (line 11).
- `property="alert_id"` — form bean property bound to select (line 10).

**Forms and action URLs:**
- `<html:form method="post" action="adminAlertAdd.do" styleClass="ajax_mode_c">` (line 3).

**Notable structural issue:**
- Line 10: `<html:select ... style="adminalert.do?action=alerts" ...>` — a URL string has been placed in the `style` attribute. This has no CSS effect; the attribute value is a stray URL that likely belongs in a `data-url` attribute or similar.

**Test grep results:** No test references found for `add-alert`, `addAlert`, `AdminAddAlertAction`, or `AdminAlertAction`.

---

### 4. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`

**Purpose:** Manufacturer management page. Renders a table of manufacturers from the `arrManufacturers` request attribute. Each row has inline edit, save, and delete buttons wired to AJAX handlers. AJAX responses (JSON) are parsed and the table is re-rendered client-side via `prepareTable()` using string concatenation into jQuery's `.html()`.

**Scriptlet blocks (with line numbers):**
- Line 54: `value="<%= manufacturer.getName() %>"` — inline in HTML `<input>` attribute.
- Line 55: `id="manufacturer-edit-<%= manufacturer.getId() %>"` — inline in HTML `id` attribute.
- Line 59: `id="edit-<%= manufacturer.getId() %>"` — inline in `<button>` `id` attribute.
- Line 64: `id="save-<%= manufacturer.getId() %>"` — inline in `<button>` `id` attribute.

All four scriptlet expressions access `ManufactureBean.getName()` and `ManufactureBean.getId()` from the loop variable `manufacturer` declared by `<logic:iterate>`.

**EL expressions / request attribute accesses (via Struts tags and scriptlets):**
- `name="arrManufacturers"` — iterated via `<logic:iterate ... type="com.bean.ManufactureBean">` (lines 47–78).
- `<bean:write property="name" name="manufacturer"/>` — renders manufacturer name (line 52).
- `<bean:write property="id" name="manufacturer"/>` — renders manufacturer ID inline in `onclick` attributes (lines 60, 65, 70).
- `<logic:notEmpty property="company_id" name="manufacturer">` — conditionally renders edit/save/delete buttons (line 58).
- `manufacturer.getName()` via scriptlet — used as `<input>` value (line 54).
- `manufacturer.getId()` via scriptlet — used as element ID suffix (lines 55, 59, 64).

**Forms and action URLs:**
- `<html:form action="manufacturers.do" method="post">` (line 17) — initial page load form (unused for CRUD — all CRUD goes via AJAX to `manufacturers.do`).

**Notable JavaScript patterns:**
- Lines 144–175 `prepareTable()`: Server JSON is parsed and `elem.name` and `elem.id` are concatenated into raw HTML strings assigned to `table.html(html)`. No escaping applied to `elem.name`.
- Lines 95, 114, 124, 130: All AJAX calls post to `manufacturers.do` with `action` parameters.

**Test grep results:** No test references found for `manufacturers`, `manufacturersList`, or `AdminManufacturersAction`.

---

### 5. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturersList.jsp`

**Purpose:** JSON response emitter used as an AJAX result view. Declared `Content-Type: application/json`. Retrieves a `JSONObject` from the HTTP **session** (not request scope) under the key `"json"` and outputs it via scriptlet expression.

**Scriptlet blocks (with line numbers):**
- Lines 7–9:
  ```jsp
  <%
      JSONObject obj = (JSONObject)request.getSession().getAttribute("json");
  %>
  ```
- Line 11: `<%=obj%>` — outputs the JSONObject's `toString()` value as the response body.

**EL expressions / session attributes accessed:**
- `request.getSession().getAttribute("json")` — reads `JSONObject` from session scope (line 8). No null guard present before line 11.

**Forms and action URLs:** None.

**Test grep results:** No test references found for `manufacturersList`.

---

### 6. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/profile.jsp`

**Purpose:** Company profile and account info edit form. Renders company name, address, contact first/last name, email, mobile number, password, and confirm-password fields. Submits to `adminRegister.do`. Client-side validation in `fnsubmitAccount()` runs before form submission.

**Scriptlet blocks (with line numbers):**
- Line 110 (inside `<script>` block):
  ```jsp
  var smsUsrAlertExisting = <%=request.getAttribute("userSmsAlertExisting")%>;
  ```
  The request attribute `userSmsAlertExisting` (a Boolean set by `AdminMenuAction` at line 105 of that class) is injected directly into a JavaScript variable assignment without encoding or type coercion.

**EL expressions / request attribute accesses (via Struts tags):**
- `name="companyRecord"` — iterated via `<logic:iterate ... type="com.bean.CompanyBean">` (lines 22–38).
- `property="name"` / `name="company"` — company name text field (line 27).
- `property="address"` / `name="company"` — address textarea (line 33).
- `property="contact_fname"` / `name="company"` — contact first name (line 47).
- `property="contact_lname"` / `name="company"` — contact last name (line 53).
- `property="email"` / `name="company"` — email field (line 61).
- `property="mobile"` / `name="company"` — mobile field (line 67).
- `property="accountAction"` — hidden field hardcoded to `"update"` (line 96).
- `request.getAttribute("userSmsAlertExisting")` — via scriptlet (line 110).

**Forms and action URLs:**
- `<html:form action="adminRegister.do" method="post" styleClass="ajax_mode_c">` (line 14) — submits to `AdminRegisterAction`.

**Test grep results:** No test references found for `profile` or `AdminRegisterAction`.

---

### 7. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/settings.jsp`

**Purpose:** Company settings form. Manages date format, timezone, maximum session length, notification preference checkboxes (Red Impact Email, Red Impact SMS, Training Expiry Email Notification), and a Super Admin-only calibration job trigger button. Client-side `isValid()` validation runs on submit.

**Scriptlet blocks (with line numbers):**
- Lines 4–7 (top of file, Java declaration):
  ```jsp
  <%
      String dateFormat = (String) session.getAttribute("sessDateTimeFormat");
      String compTimezone = (String) session.getAttribute("timezoneId");
  %>
  ```
- Lines 171–174 (inside `<script>` block):
  ```jsp
  var dateFormat = "<%=dateFormat %>";
  ...
  $('#timezone').val("<%=compTimezone %>");
  ```
  Both session-sourced strings are injected directly into JavaScript string literals without escaping.

**EL expressions / session/request attributes accessed:**
- `session.getAttribute("sessDateTimeFormat")` — date format string from session (line 5).
- `session.getAttribute("timezoneId")` — timezone ID string from session (line 6).
- `name="dateFormats"` — iterated via `<logic:iterate ... type="com.bean.DateFormatBean">` (lines 30–37).
- `name="timezones"` — iterated via `<logic:iterate ... type="com.bean.TimezoneBean">` (lines 50–56).
- `name="isSuperAdmin"` — `<logic:equal value="true">` gate controlling calibration button visibility (line 71).
- `name="redImpactAlert"` — `<logic:notEmpty property="alert_id">` / `<logic:empty>` controls checkbox checked state (lines 90–95).
- `name="redImpactSMSAlert"` — same pattern (lines 102–107).
- `name="driverDenyAlert"` — same pattern (lines 113–118).
- `property="mobile"` / `name="company"` — hidden field (line 22).
- `property="maxSessionLength"` / `name="company"` — text input (line 66).

**Forms and action URLs:**
- `<html:form action="settings.do" method="post">` (line 16) — submits to `AdminSettingsAction`.

**Test grep results:** No test references found for `settings` or `AdminSettingsAction`.

---

### 8. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/subscription.jsp`

**Purpose:** Subscription management page. Displays two tables of existing alerts and reports for the current admin user (`alertList` and `reportList`). Links to add new alerts (`adminalert.do?action=alerts`) and reports (`adminalert.do?action=reports`) via lightbox modals. Both tables have a "Delete" column with static text labels (no actual delete functionality wired in the JSP).

**Scriptlet blocks (with line numbers):**
- Lines 5–12:
  ```jsp
  <%
      String op_code="alert_list";
      String message=request.getParameter("message")==null?"":request.getParameter("message");
      String user = (String)session.getAttribute("user_cd");
      String form_cd = request.getParameter("form_cd")==null?"":request.getParameter("form_cd");
      String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime());
  %>
  ```
  - `message` — read from request parameter, stored in local variable (never output to page).
  - `user` — read from session attribute `"user_cd"`, stored in local variable (never output to page).
  - `form_cd` — read from request parameter, stored in local variable (never output to page).
  - `timeStamp` — computed timestamp, stored in local variable (never output to page).

**EL expressions / session/request attributes accessed (via Struts tags and scriptlets):**
- `session.getAttribute("user_cd")` — reads user code from session (line 8). No null guard.
- `request.getParameter("message")` — reads URL parameter (line 7). Value stored but never rendered.
- `request.getParameter("form_cd")` — reads URL parameter (line 9). Value stored but never rendered.
- `name="alertList"` — iterated via `<logic:iterate id="companyAlert">` (lines 36–42); `alert_name` property rendered via `<bean:write>`.
- `name="reportList"` — iterated via `<logic:iterate id="companyReport">` (lines 70–76); `alert_name` and `frequency` rendered via `<bean:write>`.

**Forms and action URLs:**
- No HTML form present.
- Links: `adminalert.do?action=alerts` (line 47), `adminalert.do?action=reports` (line 82).

**Test grep results:** No test references found for `subscription`.

---

### 9. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`

**Purpose:** Add/edit user (non-operator driver) form. The page branches between "add user" and "edit user" modes based on the `action` URL parameter. Renders fields for first name, last name, mobile, email, password, and confirm password. Submits to either `admindriveradd.do` (`AdminDriverAddAction`) or `admindriveredit.do` (`AdminDriverEditAction`) depending on mode. A hidden `pass_hash` field is populated client-side with the MD5 hash of the password via `CryptoJS`.

**Scriptlet blocks (with line numbers):**
- Lines 4–28 (top-of-file business logic scriptlet):
  ```jsp
  <%
      String action = request.getParameter("action") == null ? "" : request.getParameter("action");
      String id = request.getParameter("driverId") == null ? "" : request.getParameter("driverId");
      String generalUrl;
      String subscriptionUrl = "";
      String op_code;
      String actionCode;

      if (action.equalsIgnoreCase("edituser")) {
          generalUrl = "admindriver.do?action=edituser&driverId=" + id;
          subscriptionUrl = "admindriver.do?action=subscription&driverId=" + id;
          op_code = "edit_general_user";
          actionCode = "admindriveredit.do";
      } else {
          generalUrl = "admindriver.do?action=adduser";
          op_code = "add_general_user";
          actionCode = "admindriveradd.do";
      }

      if (StringUtils.isBlank(id) && request.getAttribute("newDriverId") != null) {
          id = request.getAttribute("newDriverId").toString();
          request.removeAttribute("newDriverId");
      }
  %>
  ```
  - `action` — read from request parameter, used in conditional branch logic.
  - `id` — read from request parameter `driverId`, used to build navigation URLs and a hidden field value.
  - `op_code` — assigned based on action; controls server-side operation in action class.
  - `actionCode` — determines form submit target URL.
  - `newDriverId` — read from request attribute and falls back to it when `id` is blank.

- Line 33: `<a ... href="<%=generalUrl%>">General</a>` — scriptlet expression in `href` attribute.
- Line 34: `<a href="<%=subscriptionUrl%>">Notification</a>` — scriptlet expression in `href` attribute.
- Line 38: `action="<%=actionCode %>"` — scriptlet expression in `<html:form>` action attribute.
- Line 118: `<html:hidden property="id" value="<%=id %>" name="driver"/>` — scriptlet expression in hidden field value.
- Line 119: `<html:hidden property="op_code" value="<%=op_code %>" name="driver"/>` — scriptlet expression.
- Line 206: `var actUrl = "<%=actionCode %>";` — scriptlet expression injecting `actionCode` into JavaScript variable.

**EL expressions / session/request attributes accessed:**
- `request.getParameter("action")` — via scriptlet (line 5).
- `request.getParameter("driverId")` — via scriptlet (line 6).
- `request.getAttribute("newDriverId")` — via scriptlet (line 24).
- `name="driver"` — `<logic:notEmpty name="driver">` (line 50) gates all form field rendering; `<html:text>`, `<html:password>` tags bind properties from `driver` bean in session/request scope.

**Forms and action URLs:**
- `<html:form method="post" action="<%=actionCode %>" styleClass="ajax_mode_c driver_general_form" styleId="adminUserUpdateGeneral">` (line 38) — action URL determined at runtime by scriptlet. Submits to `AdminDriverAddAction` or `AdminDriverEditAction`.

**Test grep results:** No test references found for `users/general`, `AdminDriverAddAction`, or `AdminDriverEditAction`.

---

## Findings

### result/success.jsp

**B06-1 | Severity: INFO | success.jsp is a Struts result configuration fragment, not a rendered JSP view**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/result/success.jsp`

The file contains only a `<result name="empty" type="httpheader"><param name="status">200</param></result>` XML element. It is not a JSP page in the conventional sense. No test coverage is directly applicable. However, no integration test verifies that the action producing this result actually returns HTTP 200, or that the `httpheader` result type is correctly configured in the Struts action definition.

---

### search.jsp

**B06-2 | Severity: HIGH | Unencoded user-influenced value injected into URL in fnprint() and fnbarcode()**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/search.jsp`
Lines: 88, 102–106

In `fnprint()` (line 88) and `fnbarcode()` (lines 102–106), the value of `document.searchActionForm.fname.value` (the `dname` field, a driver name from the typeahead) is concatenated directly into the URL string passed to `window.open()`:

```javascript
var url = "print.do?veh_id="+veh_id+"&att_id="+att_id+"&dname="+dname+"&action=print";
```

No `encodeURIComponent()` or equivalent escaping is applied. A driver name containing `&`, `=`, `#`, or other special characters will corrupt the query string. If a driver name is adversarially crafted (e.g., `foo&action=barcode`), additional query parameters can be injected into the `print.do` or barcode request. This is a URL parameter injection vector. No test covers these code paths.

**B06-3 | Severity: HIGH | Use of removed jQuery.browser API indicates unpatched jQuery version in use**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/search.jsp`
Line: 55

`jQuery.browser.msie` was removed from jQuery core in version 1.9. In all supported jQuery versions this property evaluates to `undefined` (falsy). The conditional on line 55 (`if ( typeof xmlData == 'string')`) is the effective branch, not the `jQuery.browser.msie` check. The presence of this deprecated API is strong evidence that the project uses an unpatched, end-of-life jQuery version which is likely to carry known CVEs. The removed API cannot be detected by any existing test.

**B06-4 | Severity: MEDIUM | Raw XHR error object exposed to user via alert()**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/search.jsp`
Line: 67

```javascript
error:function(err){alert(err)}
```

The raw jQuery XHR object is passed to `alert()`. This leaks server-internal information (HTTP status codes, error text, potentially stack traces if the server returns them in the response body) to the end user. It also provides no structured error handling. No test covers the AJAX error path.

**B06-5 | Severity: MEDIUM | Dead IE ActiveXObject code path is permanently unreachable**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/search.jsp`
Lines: 59–62

The `ActiveXObject('Microsoft.XMLDOM')` block is entered only when `jQuery.browser.msie` is truthy (line 55). Since `jQuery.browser` was removed, this evaluates to `undefined` and the branch is never taken in any modern browser. The code is dead and untestable. Any security review of the IE XML parsing path is therefore permanently blocked.

**B06-6 | Severity: LOW | No test coverage for search.jsp form rendering or AJAX flow**

The `arrUnit` and `arrAttachment` collection rendering, typeahead population via `getXml.do`, print button visibility logic (`fnshowprint`), and the form submission to `search.do` are entirely untested.

---

### settings/add-alert.jsp

**B06-7 | Severity: HIGH | URL value placed in CSS style attribute — likely developer error creating a broken data coupling**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/add-alert.jsp`
Line: 10

```jsp
<html:select property="alert_id" styleClass="form-control add_alert_selector main_selector edit "
    style="adminalert.do?action=alerts" value="1">
```

The string `"adminalert.do?action=alerts"` has been placed in the `style` attribute of the `<html:select>` element. This is not valid CSS and has no effect on styling. If JavaScript elsewhere reads `element.style.cssText` or `element.getAttribute('style')` to discover the endpoint URL for dynamic AJAX behavior, this constitutes an undocumented, fragile, and non-standard coupling. No test exercises or documents the intended use of this value. It may be a misplaced `data-url` attribute.

**B06-8 | Severity: LOW | No test coverage for add-alert.jsp alertList rendering or form submission**

The `alertList` collection is not tested for null/empty states. The hidden `src` field hardcoded to `"alert"` has no test verifying this value is expected and processed correctly server-side by `AdminAddAlertAction`.

---

### settings/manufacturers.jsp

**B06-9 | Severity: CRITICAL | Stored XSS via unescaped manufacturer name in prepareTable() innerHTML construction**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`
Lines: 151–152

In `prepareTable()`, the server JSON response is parsed and `elem.name` is concatenated directly into an HTML string that is assigned to `table.html(html)`:

```javascript
html += '<tr><td><div id="manufacturer-name-' + elem.id + '">' + elem.name + '</div>'
    + ' <input type="text" style="display:none;" id="manufacturer-edit-' + elem.id + '" value="' + elem.name + '" /></td><td>';
```

`elem.name` is not escaped before insertion. A manufacturer name containing `<script>alert(1)</script>` or `"><img src=x onerror=alert(1)>` stored in the database will execute when any CRUD operation refreshes the table. This is a stored XSS vulnerability. The `value="' + elem.name + '"` on the same line will also break out of the attribute context if `elem.name` contains a single quote. No test covers this rendering path.

**B06-10 | Severity: CRITICAL | Unescaped scriptlet expression in HTML attribute value (XSS in initial render)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`
Line: 54

```jsp
<input type="text" style="display:none;" class="form-control"
    value="<%= manufacturer.getName() %>"
    id="manufacturer-edit-<%= manufacturer.getId() %>" class="manufacturer" />
```

`manufacturer.getName()` is written into an HTML attribute value using a raw scriptlet expression without HTML entity encoding. A manufacturer name containing `"` breaks out of the attribute context and allows injection of arbitrary HTML attributes or event handlers (e.g., `" onfocus="alert(1)`). The `<bean:write>` tag used elsewhere in the same file applies escaping by default, but this scriptlet expression bypasses that protection.

**B06-11 | Severity: HIGH | JavaScript injection risk via unvalidated ID in onclick attributes**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`
Lines: 59–70, 154–166

Both the server-rendered HTML (via `<bean:write property="id">` in `onclick` attributes) and the client-side `prepareTable()` function (via `elem.id` concatenated into onclick strings) embed the manufacturer ID directly into JavaScript event handler strings:

```jsp
onclick="edit_manufacturer(<bean:write property="id" name="manufacturer"/>)"
```

```javascript
' onclick="edit_manufacturer(' + elem.id + ')">'
```

If `id` is not strictly a positive integer (database corruption, type mismatch, or an injection via the edit flow), arbitrary JavaScript executes. No numeric type enforcement is applied in either location.

**B06-12 | Severity: HIGH | JSON.parse errors not handled in delete_manufacturer() and prepareTable()**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`
Lines: 126, 146

```javascript
if (JSON.parse(data).value == true) { ... }      // line 126
var arrManu = JSON.parse(data);                   // line 146
```

Neither call is wrapped in a try/catch block. A non-JSON server error response (Struts error page returning HTML, a 500 with a stack trace, a session timeout redirect) will cause an uncaught `SyntaxError` exception. The browser silently swallows this, the user receives no feedback, and the table is not updated. No test covers these error paths.

**B06-13 | Severity: MEDIUM | Duplicate class attribute on inline input element — second value silently dropped**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`
Lines: 54–55

The `<input>` element has `class="form-control"` set as an inline attribute and `class="manufacturer"` set as a second `class` attribute. HTML parsers ignore the second occurrence of the same attribute; the `manufacturer` class is silently dropped. If the `save_manufacturer` or any other JavaScript function selects by the `manufacturer` class, the selection will fail at runtime.

**B06-14 | Severity: LOW | No test coverage for manufacturers.jsp rendering or AJAX CRUD flows**

The `arrManufacturers` null/empty branch (`<logic:notEmpty>`), the `company_id` conditional display of action buttons, and all three AJAX functions (`add_manufacturer`, `edit_manufacturer`/`save_manufacturer`, `delete_manufacturer`) are entirely untested.

---

### settings/manufacturersList.jsp

**B06-15 | Severity: CRITICAL | NullPointerException when session attribute "json" is absent**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturersList.jsp`
Lines: 8–11

```jsp
<%
    JSONObject obj = (JSONObject)request.getSession().getAttribute("json");
%>
<%=obj%>
```

If the `json` session attribute has not been set (session expired, action failure, or a direct request to the URL), `obj` is `null`. The expression `<%=obj%>` calls `String.valueOf(null)` which produces the literal string `"null"` — technically valid JSON, but semantically incorrect. However, if `obj` is `null` and the JSP container calls `obj.toString()` through its own rendering mechanism, a `NullPointerException` is thrown, producing a 500 error response. No null guard exists before the expression. No test verifies this null path.

**B06-16 | Severity: HIGH | JSON data retrieved from session scope rather than request scope creates race condition**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturersList.jsp`
Line: 8

The `json` attribute is stored in the HTTP session (`request.getSession().getAttribute("json")`), not in request scope. Session attributes are shared across all concurrent requests within the same session (e.g., two browser tabs open on the same account). A race condition between two simultaneous manufacturer CRUD operations in the same session can cause one tab to receive the other tab's JSON response, corrupting the displayed manufacturer list. No test covers concurrent session state.

**B06-17 | Severity: LOW | No test coverage for manufacturersList.jsp null session attribute or response content**

No test verifies the JSON structure of the response, the null-session-attribute error path, or the `Content-Type: application/json` header declared at line 3.

---

### settings/profile.jsp

**B06-18 | Severity: HIGH | Unescaped request attribute injected into JavaScript variable assignment**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/profile.jsp`
Line: 110

```jsp
var smsUsrAlertExisting = <%=request.getAttribute("userSmsAlertExisting")%>;
```

The `userSmsAlertExisting` request attribute (a Boolean set by `AdminMenuAction`) is injected directly into JavaScript source without any encoding. If the attribute is `null` (not set because the page was accessed without going through the normal action flow), the output is `var smsUsrAlertExisting = null;` which is valid JavaScript but may cause the `else if(cmobile === '' && smsUsrAlertExisting)` check on line 138 to behave incorrectly. More critically, no type enforcement or escaping is applied; if an attacker were able to influence this attribute value through any upstream mechanism, arbitrary JavaScript could be injected into the page script block.

**B06-19 | Severity: MEDIUM | Client-side-only mobile number validation**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/profile.jsp`
Lines: 129–139

Mobile number validation (`isNaN(cmobile)` and `cmobile.startsWith("+")`) is implemented entirely in `fnsubmitAccount()`. This validation is bypassable by disabling JavaScript or by sending a direct HTTP POST to `adminRegister.do`. Examination of `AdminRegisterAction` shows no equivalent mobile format validation in the server-side action. Invalid mobile numbers can be stored.

**B06-20 | Severity: MEDIUM | Client-side-only password validation with bypassable minimum length check**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/profile.jsp`
Lines: 107–108, 124

Password match and minimum-length (6 characters) validation occur only in `fnsubmitAccount()`. These checks are bypassed by any direct POST to `adminRegister.do`. The server-side `AdminRegisterAction` accepts the `pin` field without visible minimum-length enforcement in the reviewed code. A zero-length password could be submitted and stored.

**B06-21 | Severity: LOW | Form save button is an anchor tag; form cannot be submitted without JavaScript**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/profile.jsp`
Line: 94

The Save control is `<a href="#" class="btn btn-lg btn-primary" onclick="fnsubmitAccount();">Save</a>`. When JavaScript is disabled, clicking this link navigates to `#` and the form is never submitted — a usability failure. Additionally, all client-side validation is bypassed by any direct POST, meaning the `fnsubmitAccount()` function provides no security guarantee.

**B06-22 | Severity: LOW | No test coverage for profile.jsp rendering or fnsubmitAccount validation logic**

The `companyRecord` null/empty branch, field binding from `CompanyBean`, and all validation paths in `fnsubmitAccount` are entirely untested.

---

### settings/settings.jsp

**B06-23 | Severity: HIGH | Session-sourced strings injected unescaped into JavaScript string literals**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/settings.jsp`
Lines: 171–174

```javascript
var dateFormat = "<%=dateFormat %>";
$('#timezone').val("<%=compTimezone %>");
```

`dateFormat` (from session attribute `sessDateTimeFormat`) and `compTimezone` (from session attribute `timezoneId`) are injected directly into JavaScript string literals delimited by double quotes. No escaping (e.g., `StringEscapeUtils.escapeEcmaScript()`) is applied. A date format string or timezone ID containing a `"`, `\`, or newline character — whether from a corrupted session, a malformed database value, or an adversarially crafted session — will produce a JavaScript syntax error or inject arbitrary script. No test verifies safe rendering of these values.

**B06-24 | Severity: HIGH | calibrate() AJAX success callback fires immediately on construction, not on request completion**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/settings.jsp`
Lines: 181–187

```javascript
$.ajax({
    type: 'POST',
    url: 'calibration.do',
    success: swal("Unit Calibration Job", "Successfully started unit calibration job")
});
```

The `success` property of the `$.ajax()` options object must be a function reference or `null`. Here, `swal(...)` is called immediately as the options object is constructed; its return value (`undefined`) is assigned to `success`. The "Successfully started" alert fires before the HTTP request is made and regardless of the server's response. If `calibration.do` returns an error, the user still sees the success message. This is a logic error that misrepresents the operation outcome.

**B06-25 | Severity: MEDIUM | maxSessionLength NaN bypass in isValid() client-side validation**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/settings.jsp`
Line: 147

```javascript
if (document.AdminSettingsActionForm.maxSessionLength.value < 15) {
```

When `maxSessionLength` contains a non-numeric string (e.g., `"abc"`), JavaScript computes `NaN < 15` which evaluates to `false`. The minimum-length check is silently bypassed and the form submits with an invalid `maxSessionLength` value. No test covers this edge case, and server-side coercion is not confirmed from this JSP.

**B06-26 | Severity: MEDIUM | Super Admin calibration function exposed to all authenticated users via page source**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/settings.jsp`
Lines: 71–81, 181–187

The calibration button is hidden behind `<logic:equal name="isSuperAdmin" value="true">` server-side. However, the `calibrate()` JavaScript function and the `calibration.do` endpoint URL are present in the page source for all users who can view the settings page. Any authenticated user can call `calibrate()` from the browser developer console. If `CalibrationAction` does not independently enforce super-admin authorization server-side, any authenticated settings-page user can trigger unit calibration.

**B06-27 | Severity: LOW | No test coverage for settings.jsp rendering, isValid() validation, or calibrate() behavior**

The `dateFormats` and `timezones` collection rendering, all three checkbox states (`redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`), the `isSuperAdmin` gate, the `isValid()` function, and the `calibrate()` function are entirely untested.

---

### settings/subscription.jsp

**B06-28 | Severity: HIGH | Scriptlet reads request parameters into local variables that are never used — dead code masking potential intent**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/subscription.jsp`
Lines: 7, 9, 11

```jsp
String message = request.getParameter("message") == null ? "" : request.getParameter("message");
String form_cd = request.getParameter("form_cd") == null ? "" : request.getParameter("form_cd");
String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime());
```

`message`, `form_cd`, and `timeStamp` are computed and assigned but never output or used anywhere in the file. The intent is unclear. If `message` was originally intended to be rendered as a user-facing success/error notice, the display logic was removed, silently hiding server feedback from the user. If `form_cd` was intended to control conditional behavior, that branching logic is also absent. This constitutes untestable dead code in the view layer — logic that cannot be exercised because it produces no observable output.

**B06-29 | Severity: HIGH | Session attribute "user_cd" accessed without null guard in subscription.jsp**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/subscription.jsp`
Line: 8

```jsp
String user = (String)session.getAttribute("user_cd");
```

`user` is assigned from `session.getAttribute("user_cd")` with no null check. If the session does not contain this attribute (session expired, attribute never set, or a direct unauthenticated request), `user` is `null`. While `user` is never subsequently rendered in this file, its retrieval without guard is a code smell indicating the scriptlet was copied or ported from another page where the value was used. The session attribute name `user_cd` differs from `sessUserId` used throughout the action classes, suggesting either a naming inconsistency or a stale reference to a deprecated attribute. No test covers this initialization path.

**B06-30 | Severity: MEDIUM | "Delete" column in both tables renders static text — unsubscribe functionality is not implemented**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/subscription.jsp`
Lines: 39, 76

Both the alert table and the report table have an "Unsubscribe" column header (lines 33, 67), but the data cells contain only the static text `Delete` with no button, form, or link wired to any action:

```jsp
<td>Delete</td>     <!-- line 39 and line 76 -->
```

The unsubscribe/delete functionality is not implemented in the view. Users cannot remove existing alerts or reports through this page. No test documents or verifies this incomplete state.

**B06-31 | Severity: MEDIUM | Scriptlet business logic (op_code, actionCode, timestamp generation) belongs in the Action class**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/subscription.jsp`
Lines: 5–12

The scriptlet block computes `op_code`, `form_cd`, `timeStamp`, `user`, and `message` directly in the JSP. Even though none are rendered, the presence of this logic in the view layer is an untestable pattern. Action routing decisions (`op_code`), timestamp generation, and session-to-local-variable assignments belong in the backing Action class where they can be unit tested. The JSP layer has no test infrastructure and these computations are permanently opaque to the test suite.

**B06-32 | Severity: LOW | No test coverage for subscription.jsp collection rendering or tab navigation**

The `alertList` and `reportList` null/empty branches, `<bean:write>` rendering for `alert_name` and `frequency`, and the lightbox modal links (`adminalert.do?action=alerts`, `adminalert.do?action=reports`) are entirely untested.

---

### users/general.jsp

**B06-33 | Severity: HIGH | Substantial business-logic scriptlet in view layer — untestable routing and URL construction**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`
Lines: 4–28

The top-of-file scriptlet performs action mode determination, URL construction, and operation code assignment:

```java
if (action.equalsIgnoreCase("edituser")) {
    generalUrl = "admindriver.do?action=edituser&driverId=" + id;
    subscriptionUrl = "admindriver.do?action=subscription&driverId=" + id;
    op_code = "edit_general_user";
    actionCode = "admindriveredit.do";
} else {
    generalUrl = "admindriver.do?action=adduser";
    op_code = "add_general_user";
    actionCode = "admindriveradd.do";
}
```

This conditional routing logic — which determines the form's submit URL, the tab navigation URLs, and the `op_code` sent to the server — resides in the JSP where it cannot be unit tested. The `op_code` value directly controls which server-side operation `AdminDriverAddAction` or `AdminDriverEditAction` executes. An error in this branching logic is invisible to the test suite. No test covers any path through this scriptlet.

**B06-34 | Severity: HIGH | driverId request parameter injected into navigation URLs without encoding**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`
Lines: 13–15, 33–34

The `id` variable is read from `request.getParameter("driverId")` (line 6) and then concatenated into navigation tab URLs:

```java
generalUrl = "admindriver.do?action=edituser&driverId=" + id;
subscriptionUrl = "admindriver.do?action=subscription&driverId=" + id;
```

These are then written into `href` attributes via scriptlet expressions (`<%=generalUrl%>`, `<%=subscriptionUrl%>`) on lines 33–34. The `id` value is not HTML-encoded or URL-encoded before concatenation. A crafted `driverId` parameter value containing `"` or `>` could break out of the `href` attribute and inject arbitrary HTML. A value containing `&` could inject additional query parameters.

**B06-35 | Severity: HIGH | MD5 used as password hashing mechanism — cryptographically broken**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`
Line: 190

```javascript
var password = '' + CryptoJS.MD5($('input[name="pass"]').val());
$('input[name=pass_hash]').val(password);
```

The password is hashed client-side with MD5 before being placed in the `pass_hash` hidden field and submitted to the server. MD5 is a cryptographically broken hash function with no salt. Client-side hashing without a server-side salt provides no meaningful security: an attacker who intercepts the network traffic (bypassing HTTPS) or who reads the `pass_hash` field from the DOM obtains a value that can be passed directly to the server to authenticate. Additionally, the clear-text `pass` field is also submitted in the POST body (it is not cleared before submission), meaning both the plaintext password and its MD5 hash are transmitted simultaneously. No test covers this hashing behavior.

**B06-36 | Severity: MEDIUM | actionCode value injected into JavaScript variable without encoding**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`
Line: 206

```jsp
var actUrl = "<%=actionCode %>";
```

`actionCode` is one of `"admindriveradd.do"` or `"admindriveredit.do"`, both hardcoded string literals. In this specific case the values are safe. However, the pattern — injecting a server-side scriptlet variable into a JavaScript string literal without encoding — is architecturally unsafe. If `actionCode` were ever derived from user input (e.g., from a request parameter) without escaping, this would become a script injection vector. No test documents that `actionCode` is always a safe, static value.

**B06-37 | Severity: MEDIUM | Password is submitted in plaintext alongside its MD5 hash**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`
Lines: 189–191

`validateFields()` sets `pass_hash` to the MD5 of the password but does not clear the `pass` and `cpass` fields before form submission. Both `pass` (plaintext) and `pass_hash` (MD5) are included in the POST body simultaneously. The server receives the plaintext password even when the intent appears to be to send only the hash. No test confirms which field the server actually uses for authentication or storage.

**B06-38 | Severity: MEDIUM | Password confirm-match check in validateFields() has a logic gap — mismatch not blocked on submit**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`
Lines: 168–196

`validateFields()` shows the `#password_not_match` div and sets `valid = false` on mismatch, but `$('input[name=submit]').prop('disabled', !valid)` is only called on line 195. If `validateFields()` is called with `valid = true` (the initial call from line 199 passes `displayRequiredFields()` result) and the passwords then don't match, the submit button may still be enabled depending on the evaluation order. More critically, the form also submits on the `btnSveDriverG` click bound to `setupConfirmationPopups()` (line 208) which does not call `validateFields()` — the confirmation popup flow may bypass the password match check entirely. No test covers this interaction.

**B06-39 | Severity: LOW | No test coverage for users/general.jsp rendering or scriptlet routing logic**

The add/edit mode branching scriptlet, all form field bindings from the `driver` bean, the `newDriverId` fallback path (lines 24–27), the `displayRequiredFields()` and `validateFields()` validation functions, and the `setupConfirmationPopups` integration are entirely untested.

---

## Summary Table

| ID     | JSP File                     | Severity | Category                                                     |
|--------|------------------------------|----------|--------------------------------------------------------------|
| B06-1  | result/success.jsp           | INFO     | Config fragment — no tests applicable                        |
| B06-2  | search.jsp                   | HIGH     | Unencoded user input injected into URL (param injection)     |
| B06-3  | search.jsp                   | HIGH     | Removed jQuery.browser API — outdated/vulnerable jQuery      |
| B06-4  | search.jsp                   | MEDIUM   | Raw XHR error object exposed to user via alert()             |
| B06-5  | search.jsp                   | MEDIUM   | Dead IE ActiveXObject code — permanently unreachable         |
| B06-6  | search.jsp                   | LOW      | No test coverage                                             |
| B06-7  | settings/add-alert.jsp       | HIGH     | URL placed in CSS style attribute — broken data coupling     |
| B06-8  | settings/add-alert.jsp       | LOW      | No test coverage                                             |
| B06-9  | settings/manufacturers.jsp   | CRITICAL | Stored XSS via unescaped name in innerHTML construction      |
| B06-10 | settings/manufacturers.jsp   | CRITICAL | Unescaped scriptlet in HTML attribute value (XSS)            |
| B06-11 | settings/manufacturers.jsp   | HIGH     | JS injection via unvalidated ID in onclick attributes        |
| B06-12 | settings/manufacturers.jsp   | HIGH     | Unhandled JSON.parse exceptions in AJAX callbacks            |
| B06-13 | settings/manufacturers.jsp   | MEDIUM   | Duplicate class attribute — second value silently dropped    |
| B06-14 | settings/manufacturers.jsp   | LOW      | No test coverage                                             |
| B06-15 | settings/manufacturersList.jsp | CRITICAL | NPE on null "json" session attribute                       |
| B06-16 | settings/manufacturersList.jsp | HIGH   | Session-scoped JSON creates race condition across tabs        |
| B06-17 | settings/manufacturersList.jsp | LOW    | No test coverage                                             |
| B06-18 | settings/profile.jsp         | HIGH     | Unescaped request attribute injected into JavaScript         |
| B06-19 | settings/profile.jsp         | MEDIUM   | Client-side-only mobile number validation                    |
| B06-20 | settings/profile.jsp         | MEDIUM   | Client-side-only password validation / bypassable min length |
| B06-21 | settings/profile.jsp         | LOW      | Form inaccessible without JavaScript                         |
| B06-22 | settings/profile.jsp         | LOW      | No test coverage                                             |
| B06-23 | settings/settings.jsp        | HIGH     | Session strings injected unescaped into JS string literals   |
| B06-24 | settings/settings.jsp        | HIGH     | calibrate() swal fires before AJAX request completes         |
| B06-25 | settings/settings.jsp        | MEDIUM   | NaN bypass in maxSessionLength isValid() check               |
| B06-26 | settings/settings.jsp        | MEDIUM   | Super admin JS function exposed to all authenticated users   |
| B06-27 | settings/settings.jsp        | LOW      | No test coverage                                             |
| B06-28 | settings/subscription.jsp    | HIGH     | Dead scriptlet variables — missing user feedback display     |
| B06-29 | settings/subscription.jsp    | HIGH     | Session attribute "user_cd" accessed without null guard      |
| B06-30 | settings/subscription.jsp    | MEDIUM   | Unsubscribe "Delete" column is static text — not implemented |
| B06-31 | settings/subscription.jsp    | MEDIUM   | Business-logic scriptlet in view layer (untestable)          |
| B06-32 | settings/subscription.jsp    | LOW      | No test coverage                                             |
| B06-33 | users/general.jsp            | HIGH     | Business-logic routing scriptlet in view layer (untestable)  |
| B06-34 | users/general.jsp            | HIGH     | driverId parameter injected into href without encoding       |
| B06-35 | users/general.jsp            | HIGH     | MD5 used for password hashing — cryptographically broken     |
| B06-36 | users/general.jsp            | MEDIUM   | actionCode injected into JS variable without encoding        |
| B06-37 | users/general.jsp            | MEDIUM   | Plaintext password submitted alongside MD5 hash              |
| B06-38 | users/general.jsp            | MEDIUM   | Password confirm-match check has logic gap — bypassable      |
| B06-39 | users/general.jsp            | LOW      | No test coverage                                             |

**Total findings: 39**

**CRITICAL: 3 | HIGH: 14 | MEDIUM: 9 | LOW: 12 | INFO: 1**

---

## Global Coverage Gap

Zero JSP test files exist in `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`. The test suite contains only 4 files, all covering calibration utility classes. There is no test infrastructure for:

- JSP rendering (Struts tag libraries, bean binding, logic iteration)
- Session or request attribute wiring between Action classes and JSP views
- Client-side JavaScript validation functions
- AJAX response handling and DOM mutation
- Scriptlet branching logic (add vs. edit mode, super-admin gates)
- Error and null-value rendering paths

All scriptlet logic, all conditional rendering branches, and all JavaScript validation functions across these 9 JSPs are permanently opaque to the test suite. Any regression in view-layer behavior — including the CRITICAL XSS vulnerabilities identified in `manufacturers.jsp` and `manufacturersList.jsp` — would not be detected by automated testing.
