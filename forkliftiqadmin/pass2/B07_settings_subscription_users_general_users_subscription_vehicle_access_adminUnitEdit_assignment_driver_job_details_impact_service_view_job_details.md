# Pass 2 - Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** B07
**Date:** 2026-02-26

## Scope

| # | JSP File |
|---|----------|
| 1 | `src/main/webapp/html-jsp/settings/subscription.jsp` |
| 2 | `src/main/webapp/html-jsp/users/general.jsp` |
| 3 | `src/main/webapp/html-jsp/users/subscription.jsp` |
| 4 | `src/main/webapp/html-jsp/vehicle/access.jsp` |
| 5 | `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp` |
| 6 | `src/main/webapp/html-jsp/vehicle/assignment.jsp` |
| 7 | `src/main/webapp/html-jsp/vehicle/driver_job_details.jsp` |
| 8 | `src/main/webapp/html-jsp/vehicle/impact.jsp` |
| 9 | `src/main/webapp/html-jsp/vehicle/service.jsp` |
| 10 | `src/main/webapp/html-jsp/vehicle/view_job_details.jsp` |

**Test directory searched:** `src/test/java/`

**Existing tests found (total in project):** 4 files
- `com/util/ImpactUtilTest.java`
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`

**Result of test search for all 10 JSP filenames (without extension):** Zero matches. No test file references `subscription`, `general`, `access`, `adminUnitEdit`, `assignment`, `driver_job_details`, `impact`, `service`, or `view_job_details` in any test class name, method name, or string literal.

---

## JSP-by-JSP Evidence and Findings

---

### 1. `settings/subscription.jsp`

**Purpose:** Displays the admin user's active alert subscriptions (email alerts) and report subscriptions in two tables. Provides links to add new alerts/reports. Rendered as a modal panel under the "My Subscription" tab of the settings area. The backing action is `AdminMenuAction` with `action=subscription` (noted as "Not used" in a comment in that action class).

**Scriptlet blocks:**
```java
// Lines 5-12
String op_code = "alert_list";
String message = request.getParameter("message") == null ? "" : request.getParameter("message");
String user = (String) session.getAttribute("user_cd");
String form_cd = request.getParameter("form_cd") == null ? "" : request.getParameter("form_cd");
String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime());
```

**EL / Struts tag attribute access:**
- `name="alertList"` — request attribute, iterated with `<logic:iterate>`; bean property `alert_name` written via `<bean:write>`
- `name="reportList"` — request attribute, iterated; properties `alert_name`, `frequency` written via `<bean:write>`

**JavaScript with security implications:** None (no JavaScript block in this file).

**Findings:**

B07-1 | Severity: HIGH | `message` parameter (line 7) is read from `request.getParameter("message")` into a Java variable but is never rendered in the JSP output. However, the variable is declared and retained, creating dead code that could be repurposed unsafely in future edits. No sanitisation is applied. If the variable were ever output without escaping, it would be a stored/reflected XSS vector.

B07-2 | Severity: MEDIUM | `user_cd` is pulled from session (line 8) into a local variable `user` but is never used in the JSP. The variable constitutes dead code — untested and semantically unclear. No test verifies whether the correct session value is present when this view is rendered.

B07-3 | Severity: MEDIUM | `form_cd` is read from a request parameter (line 9) into a Java variable but is never rendered or used. Same dead-code risk as B07-1/B07-2.

B07-4 | Severity: MEDIUM | `op_code` is hardcoded to `"alert_list"` (line 6) but is never used within the JSP. The comment in `AdminMenuAction.java` explicitly marks the `subscription` action as "Not used," meaning the entire view may be orphaned dead code with no tested path.

B07-5 | Severity: HIGH | `<bean:write>` for `alert_name` (line 38) and `frequency` (line 73) in both table iterations renders request-attribute values directly to HTML with no explicit escaping strategy documented. `<bean:write>` does not HTML-encode by default unless `filter="true"` is explicitly set. If `alert_name` or `frequency` values contain `<`, `>`, `"`, or `&` characters, XSS is possible.

B07-6 | Severity: LOW | The "Delete" links (lines 39, 74) in the Unsubscribe column are plain text strings — not actual functional links or buttons. There is no form action or JavaScript handler attached. This is dead UI that would confuse security testing and indicates incomplete implementation. No test covers the empty or null `alertList`/`reportList` case.

B07-7 | Severity: INFO | Zero test coverage: no unit, integration, or JSP render test exists for this view. The `AdminMenuAction` subscription branch is confirmed untested.

---

### 2. `users/general.jsp`

**Purpose:** Form for adding or editing a user (driver/admin). Supports two modes controlled by the `action` request parameter (`edituser` vs. add). Renders user fields: first name, last name, mobile, email, password, confirm password. Submits to `admindriveredit.do` or `admindriveradd.do`. Backed by `AdminDriverEditAction` / `AdminDriverAddAction`.

**Scriptlet blocks:**
```java
// Lines 4-28
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
```

**EL / Struts tag attribute access:**
- `name="driver"` — used as the ActionForm/bean name throughout; `first_name`, `last_name`, `mobile`, `email_addr`, `pass`, `cpass`, `id`, `op_code`, `pass_hash` properties bound via `<html:text>`, `<html:password>`, `<html:hidden>`
- `request.getAttribute("newDriverId")` — consumed and removed in scriptlet

**JavaScript with security implications:**
- Lines 126-216: Client-side validation of `first_name`, `last_name`, `email_addr`, `pass`, `cpass` fields.
- Line 154: Password length validation uses `< 6` threshold — checks that password is more than 6 characters but the swal message (line 179) says "more than 6 characters" while the check is `< 6` (i.e., passes at exactly 6). Off-by-one: a 6-character password is accepted by the swal branch but rejected by `displayRequiredFields` at line 154.
- Lines 183-192: The `validateFields` function's `else if` block for mobile validation is only reached when `pass` AND `cpass` are both empty. If only one is empty, neither branch fires. If both are empty, mobile validation runs — this is a logical error that means mobile is only validated when no password is entered.
- Line 190: MD5 is used to hash the password client-side before submission: `CryptoJS.MD5($('input[name="pass"]').val())`. MD5 is cryptographically broken and unsuitable for password hashing; this provides no meaningful security. The plaintext password is also present in the DOM while the page is active.
- Line 190: MD5 hash is only computed in the `else` branch of `validateFields`, i.e., only when both `pass` and `cpass` are empty. The `pass_hash` hidden field is therefore never populated when the user actually enters a password.
- Line 206: `<%=actionCode %>` is injected directly into a JavaScript string literal with no JS escaping. If `actionCode` were somehow tainted (it is constructed from a hardcoded string here, but the pattern is dangerous), it would be a DOM-based XSS vector.

**Findings:**

B07-8 | Severity: CRITICAL | MD5 is used as the client-side password hashing algorithm (line 190). MD5 is cryptographically broken, not a key-derivation function, and trivially reversible via rainbow tables. The server-side handling of `pass_hash` is not examined here, but using MD5 for any part of the password pipeline is a critical security defect. No test validates the hashing scheme.

B07-9 | Severity: HIGH | The `pass_hash` field is only populated in the `else` branch of `validateFields` (line 190), which is reached only when both `pass` and `cpass` are empty. When the user enters a password, the MD5 hash is never computed and `pass_hash` is submitted empty. This means password changes may silently fail or submit an empty hash. No test covers this logic path.

B07-10 | Severity: HIGH | `id` is taken from `request.getParameter("driverId")` (line 6) without validation and directly embedded into URL strings `generalUrl` and `subscriptionUrl` (lines 14-15). These URLs are rendered into `<a href="...">` tag content at lines 33-34. If `id` contains special characters including quotes or angle brackets, HTML injection or URL manipulation is possible. No sanitisation is applied.

B07-11 | Severity: HIGH | `actionCode` (constructed from a hardcoded constant, but the scriptlet pattern allows it to vary) is injected unescaped into a JavaScript string at line 206: `var actUrl = "<%=actionCode %>";`. The established pattern is dangerous: if `actionCode` ever contains a double-quote or a newline, JavaScript injection results. No test validates the output of this scriptlet variable in a JavaScript context.

B07-12 | Severity: MEDIUM | The password validation logic in `validateFields` (lines 173-193) has a structural defect: mobile-number validation is in an `else if` that is only reached when both `pass` and `cpass` are empty. A user with a password can supply an invalid mobile number without triggering the mobile validation. No test covers this combined case.

B07-13 | Severity: MEDIUM | The password minimum-length check is inconsistent between `displayRequiredFields` (line 154: `length < 6` rejects, so exactly 6 is accepted) and the swal error message (line 179: "more than 6 characters"). The actual threshold applied is >= 6 characters, not > 6. No test validates the boundary condition.

B07-14 | Severity: MEDIUM | `request.removeAttribute("newDriverId")` at line 26 mutates request state as a side effect of rendering the view. This is an unusual pattern that prevents retries (e.g., on browser refresh the `newDriverId` attribute will be gone). No test verifies this state-mutation behaviour.

B07-15 | Severity: INFO | Zero test coverage for this JSP and its scriptlet logic. No test exercises the add vs. edit mode branching, the newDriverId fallback, or any of the client-side validation paths.

---

### 3. `users/subscription.jsp`

**Purpose:** Notification preferences tab for a specific driver/user. Displays three checkboxes: Red Impact Email, Red Impact SMS, and Training Expiry Email Notification. Checked state is driven by three request attributes (`redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`). Submits to `admindriveredit.do` with `op_code=edit_subscription`.

**Scriptlet blocks:**
```java
// Lines 3-7
Long id = request.getParameter("driverId") == null ? 0 : Long.valueOf(request.getParameter("driverId"));
String generalUrl = "admindriver.do?action=" + (id == null ? "adduser" : "edituser&driverId=" + id);
String subscriptionUrl = "admindriver.do?action=subscription&driverId=" + id;
```

**EL / Struts tag attribute access:**
- `name="redImpactAlert"` — request attribute; `property="alert_id"` tested for notEmpty/empty to set checkbox checked state
- `name="redImpactSMSAlert"` — request attribute; same pattern
- `name="driverDenyAlert"` — request attribute; same pattern
- `name="driver"` — used for `<html:hidden property="id">` and `<html:hidden property="mobile">`

**JavaScript with security implications:**
- Lines 80-95: `isValid()` reads `document.adminDriverEditForm.mobile.value` to check if SMS checkbox is checked without a mobile number. The form's `styleId` is `adminDriverUpdateSubscription` but the JavaScript references `document.adminDriverEditForm`, which is a different form name. This mismatch means `isValid()` will throw a JavaScript error or always return `true` (invalid reference), making the mobile-required validation non-functional.

**Findings:**

B07-16 | Severity: HIGH | `isValid()` at line 82 references `document.adminDriverEditForm.mobile.value` but the form `styleId` is `adminDriverUpdateSubscription` and the Struts form name would be derived from the ActionForm bean name. The reference `document.adminDriverEditForm` will be `undefined` at runtime, causing a JavaScript TypeError. The SMS alert checkbox can therefore be saved without a mobile number being present, bypassing the intended validation. No test covers this scenario.

B07-17 | Severity: HIGH | `Long.valueOf(request.getParameter("driverId"))` at line 4 will throw `NumberFormatException` if the parameter is present but non-numeric (e.g., `driverId=abc`). No try/catch block exists. This results in an unhandled exception bubbling up to the Struts error handler, potentially exposing a stack trace. No test covers non-numeric or malformed `driverId` input.

B07-18 | Severity: MEDIUM | The `id == null` check in `generalUrl` construction (line 5) is dead code: `id` is assigned `Long.valueOf(...)` or `0` (a non-null primitive autoboxed value). The condition `id == null` will never be true, so the `"adduser"` branch is unreachable. No test validates the URL construction logic.

B07-19 | Severity: MEDIUM | `id` is embedded directly into HTML anchor `href` attributes at lines 11-12 (rendered as `<%=generalUrl%>` and `<%=subscriptionUrl%>`). While `id` is a `Long`, the pattern is fragile: any future change from `Long` to `String` would re-introduce URL injection risk with no sanitisation in place.

B07-20 | Severity: INFO | The typo "Notifcation" (line 102, JavaScript string) in the success message `'Notifcation information successfully updated.'` is not a security issue but indicates the view is not tested end-to-end.

B07-21 | Severity: INFO | Zero test coverage: no test exercises the subscription JSP rendering, checkbox state logic, or form submission flow.

---

### 4. `vehicle/access.jsp`

**Purpose:** Access control configuration tab for a vehicle unit. Renders fields: accessible (checkbox), access type (card/PIN), access ID, keypad reader (dropdown with hardware vendor values), and facility code. Submits to `adminunitaccess.do`. Tab navigation includes conditional dealer-specific tabs via `<logic:equal name="isDealer">`.

**Scriptlet blocks:**
```java
// Lines 3-12
String id = request.getParameter("id") == null ? "" : request.getParameter("id");
String urlGeneral;
if (!id.equalsIgnoreCase("")) {
    urlGeneral = "adminunit.do?action=edit&equipId=" + id;
} else {
    urlGeneral = "adminunit.do?action=add";
}
```

**EL / Struts tag attribute access:**
- `name="isDealer"` — session/request attribute tested via `<logic:equal>` and `<logic:notEqual>` to control tab visibility
- ActionForm properties bound: `accessible`, `access_type`, `access_id`, `keypad_reader`, `facility_code`, `id`, `action`

**JavaScript with security implications:**
- Lines 107-114: `setupConfirmationPopups` called with hardcoded action URL `'adminunitaccess.do'`. No variable injection.

**Findings:**

B07-22 | Severity: HIGH | `id` is taken from `request.getParameter("id")` (line 4) without validation or sanitisation and is concatenated into `urlGeneral` and several navigation tab `href` values (lines 18-20, 28-30). These are output directly into HTML anchor tags. No HTML encoding is applied. A crafted `id` value containing `"` or `>` could break out of the `href` attribute context and inject arbitrary HTML or JavaScript.

B07-23 | Severity: HIGH | `id` is also embedded verbatim in multiple Struts navigation tab hrefs at lines 19, 20, 28, 29 (e.g., `href="adminunit.do?action=service&equipId=<%=id %>"`). The same injection risk applies across all five tab URLs. None of these outputs are tested.

B07-24 | Severity: MEDIUM | The `isDealer` attribute is read from the request/session scope as a raw string `"true"` and compared using `<logic:equal value="true">`. There is no test that verifies what happens when `isDealer` is absent (null) from the session, which would cause the `<logic:notEqual>` branch to render the four-tab layout — this is a silent degradation not a crash, but the semantic correctness is unverified.

B07-25 | Severity: LOW | The hardcoded access type values `"card"` and `"pin"` (lines 58-59) and keypad reader values `"ROSLARE"`, `"KERI"`, `"SMART"`, `"HID_ICLASS"` (lines 77-80) are defined only in the JSP with no backing enumeration or constant class. No test verifies that these values are valid against the database schema or the hardware abstraction layer.

B07-26 | Severity: INFO | Zero test coverage: no test exercises the access JSP rendering, the dealer/non-dealer tab branching, or the form submission for any access control field.

---

### 5. `vehicle/adminUnitEdit.jsp`

**Purpose:** General tab of the vehicle (unit) add/edit form. Renders fields: unit name, serial number, manufacturer (dropdown), type (dropdown), power/fuel type (dropdown), capacity (weight unit + size), expansion module checkbox, and MAC address (conditionally visible). Submits to `adminunitedit.do`. Includes async AJAX validation calls for uniqueness of name, serial number, and MAC address.

**Scriptlet blocks:**
```java
// Lines 3-25
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String urlGeneral = "adminunit.do?action=add";
String urlService = "";
String urlImpact = "";
String urlAccess = "";
String urlAssignment = "";
if (action.equalsIgnoreCase("edit")) {
    urlGeneral = "adminunit.do?action=edit&equipId=" + id;
    urlService = "adminunit.do?action=service&equipId=" + id;
    urlAccess = "adminunitaccess.do?id=" + id;
    urlImpact = "adminunit.do?action=impact&equipId=" + id;
    urlAssignment = "adminunit.do?action=assignment&equipId=" + id;
}
int newUnitId = 0;
if (request.getAttribute("newId") != null) {
    newUnitId = (Integer) request.getAttribute("newId");
}
```

**EL / Struts tag attribute access:**
- `name="isDealer"` — request attribute tested via `<logic:equal>` for tab layout
- `name="arrAdminUnit"` — iterated; `type="com.bean.UnitBean"` properties: `name`, `serial_no`, `manu_id`, `type_id`, `fuel_type_id`, `weight_unit`, `size`, `exp_mod`, `mac_address`, `id`
- `name="arrManufacturers"` — request attribute used as options collection
- `name="unitRecord"` — loop variable referencing collection properties `arrAdminUnitType`, `arrAdminUnitFuelType`

**JavaScript with security implications:**
- Lines 253-268: AJAX uniqueness validation functions `validateNameField`, `validateSerialNoField`, `validateMacAddressField` call `wsValidation(url, divId)` with user-entered field values concatenated directly into GET request URLs. Values from `input[name=name]`, `input[name=serial_no]`, and `input[name=mac_address]` are appended to query strings without any URL encoding. Special characters in these fields could manipulate the server-side query string or cause SSRF-like parameter injection.
- Lines 170-172: Three hidden fields (`oldId`, `newId`, `actionUnit`) are set with scriptlet values (`<%=id %>`, `<%=newUnitId %>`, `<%=action %>`). `action` is a string from a request parameter. While the current `action` values are only `"edit"` or `""`, the raw injection pattern is dangerous.
- Lines 277-291: `wsValidation` uses synchronous AJAX (`async: false`), which blocks the UI thread and is deprecated in modern browsers.

**Findings:**

B07-27 | Severity: HIGH | `id` from `request.getParameter("equipId")` (line 4) is concatenated into five tab navigation URLs (lines 13-17) and into three hidden `<input>` values (lines 170-172) without any HTML encoding. An attacker with control of the URL parameter could inject HTML attributes or script content.

B07-28 | Severity: HIGH | In `validateNameField`, `validateSerialNoField`, and `validateMacAddressField` (lines 253-268), user-entered field values are concatenated directly into AJAX URL strings without `encodeURIComponent()`. Input containing `&`, `=`, `#`, or space characters will corrupt or manipulate the query string sent to the validation endpoints. No test validates URL encoding behaviour.

B07-29 | Severity: HIGH | `action` from `request.getParameter("action")` (line 3) is injected verbatim into a hidden input value at line 172: `value="<%=action %>"`. No HTML encoding is applied. If `action` contains `"` or `>`, the HTML attribute is broken.

B07-30 | Severity: MEDIUM | The `wsValidation` function (lines 275-291) uses synchronous AJAX (`async: false`), which is deprecated and will hang the UI thread. No test validates the behaviour when the validation endpoint is slow or unavailable, including whether the submit button correctly remains disabled.

B07-31 | Severity: MEDIUM | The `checkIdValue` function (lines 183-188) fires an `alert()` instead of an application-styled notification when the service tab href is empty. This is inconsistent with the rest of the application (which uses `swal`) and untested.

B07-32 | Severity: MEDIUM | `newUnitId` is cast directly from `request.getAttribute("newId")` as `(Integer)` (line 23). If the attribute is set to a non-Integer type, a `ClassCastException` will occur. No test verifies attribute type correctness.

B07-33 | Severity: LOW | The `<logic:equal name="unitRecord" property="size" value="0.0">` branch (line 127) renders the size field with `value=""` when size is 0.0, effectively hiding zero values. This UI behaviour is untested and could mask legitimately zero-capacity vehicles.

B07-34 | Severity: INFO | Zero test coverage: no test exercises the add vs. edit mode branching, URL construction, AJAX validation calls, or form submission for the vehicle general edit form.

---

### 6. `vehicle/assignment.jsp`

**Purpose:** Assignment tab for a vehicle unit. Allows assigning a vehicle to a company for a date range. Renders a company dropdown and two date pickers (start/end). Lists existing assignments in a table. Delete action is via data attributes handled by a global JavaScript handler. Submits to `adminunitassign.do`.

**Scriptlet blocks:**
```java
// Lines 3-7
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String urlGeneral = id.isEmpty() ? "adminunit.do?action=add" : "adminunit.do?action=edit&equipId=" + id;
```

**EL / Struts tag attribute access:**
- `name="arrCompanies"` — request attribute used as options collection (value=`id`, label=`name`)
- `name="arrAssignments"` — request attribute iterated; `type="com.bean.UnitAssignmentBean"`; properties: `id`, `company_name`, `start`, `end`, `current`

**JavaScript with security implications:**
- Lines 122-174: `validateFields()` makes a synchronous AJAX call to `assigndatesvalid.do` with `unit_id`, `start`, and `end` values from form inputs without URL encoding.
- Line 138: Server response is written directly to `errorOutput.text(result)` — uses `.text()` which is safe (text node, not innerHTML).
- Lines 122-123: `dateFormat` from session is injected into JavaScript: `setupDatePicker('#start_date', '<%= dateFormat %>', null)`. If the session date format string contains a single quote or backslash, JavaScript string literal injection occurs.

**Findings:**

B07-35 | Severity: CRITICAL | `session.getAttribute("sessDateFormat")` at line 4 is called without a null check, immediately invoking `.replaceAll(...)` on the result. If `sessDateFormat` is absent from the session (e.g., session expiry or misconfiguration), a `NullPointerException` is thrown, resulting in a 500 error. No test verifies null-session-attribute resilience.

B07-36 | Severity: HIGH | `dateFormat` (derived from the session attribute) is injected into a JavaScript string literal at lines 122-123: `'<%= dateFormat %>'`. No JavaScript string escaping is applied. If the date format string contains a single quote character (e.g., `d 'of' MMMM`), JavaScript string literal injection occurs, potentially breaking the page or allowing script execution depending on value origin. No test validates this injection point.

B07-37 | Severity: HIGH | `id` from `request.getParameter("equipId")` (line 5) is embedded directly into multiple HTML tab navigation `href` attributes (lines 15-19) and into a hidden input `value` (line 72) without HTML encoding. HTML injection is possible with a crafted `id` parameter.

B07-38 | Severity: MEDIUM | The AJAX date validation call (lines 131-147) concatenates `$('input[name=unit_id]').val()`, `$('#start_date').val()`, and `$('#end_date').val()` into a URL string without `encodeURIComponent()`. Dates from the datepicker and the unit_id value are not validated or encoded before use. No test covers invalid or malformed date input.

B07-39 | Severity: MEDIUM | `<bean:write property="company_name" name="assignment"/>` (line 99) renders the company name to HTML without a documented encoding guarantee. `<bean:write>` without `filter="true"` does not HTML-encode output. If `company_name` contains HTML special characters, XSS is possible.

B07-40 | Severity: INFO | Zero test coverage: no test exercises the date format session attribute handling, company assignment creation, table rendering, or delete flow.

---

### 7. `vehicle/driver_job_details.jsp`

**Purpose:** Form for assigning a driver to a job. Renders a driver select dropdown, start/end time inputs, and an instruction textarea. Submits to `driverjobreq.do`. Contains hidden fields for `jobId`, `equipId`, and `action`. The form is presented inside a modal dialog. The file contains a substantial dead-code block (`fnsubmitAccount`) that appears to be copied from an account registration form.

**Scriptlet blocks:**
```java
// Lines 3-6
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String jobId = request.getParameter("job_id") == null ? "" : request.getParameter("job_id");
```

**EL / Struts tag attribute access:**
- `collection="arrDrivers"` — used with `<html:options>` for the driver select (property=`id`, labelProperty=`first_last`)
- `value="<%=jobId %>"` and `value="<%=id %>"` — scriptlet values injected into hidden input values

**JavaScript with security implications:**
- Lines 85-106: `fnsubmitAccount()` function is entirely dead code referencing `document.adminRegActionForm` — a form that does not exist on this page. It reads `pin`, `cpassword`, `name`, `email` fields that are not present. This is copy-pasted code from the registration form that was never cleaned up.
- Lines 108-118: `fnAssign()` reads values from the parent modal DOM using `$('.modal:nth-last-child(2) [name="name"]').val()` and `$('.modal:nth-last-child(2) [name="description"]').val()`. These are set via jQuery `.val()` into hidden fields `#jobTitle` and `#description`. The values are then submitted as form fields — no sanitisation is applied to content coming from a parent modal's input fields.
- Line 112: `$("#drivrId")` — note the typo (`drivrId` vs. `driverId`). The element with id `driverId` exists at line 53 as `styleId="driverId"`. This means `driverId` is never correctly populated by `fnAssign()` and the driver selection is not submitted with the intended form field name.

**Findings:**

B07-41 | Severity: HIGH | `jobId` and `id` (lines 4-5) are injected into hidden `<html:hidden>` field values at lines 48-49 (`value="<%=jobId %>"`, `value="<%=id %>"`). These values are taken from request parameters without validation or HTML encoding. While `<html:hidden>` generates `<input type="hidden">` tags, attribute injection is still possible if values contain `"` or `>`.

B07-42 | Severity: HIGH | In `fnAssign()` (line 112), `$("#drivrId")` references a non-existent element (the actual element ID is `driverId` at line 53). The `driverId` hidden field is therefore never populated via `fnAssign()`. The selected driver's ID is not submitted to `driverjobreq.do`, meaning driver assignment is silently broken. No test verifies the form submission payload.

B07-43 | Severity: HIGH | Dead code block `fnsubmitAccount()` (lines 85-106) references `document.adminRegActionForm` which does not exist on this page. While currently inert, this function could be accidentally invoked by a future code change or by an attacker discovering a way to call it. The presence of password comparison logic (`pin` vs. `cpassword`) in a driver-job context is a code hygiene issue that complicates security review. No test would flag this dead path.

B07-44 | Severity: MEDIUM | Values extracted from the parent modal DOM in `fnAssign()` (lines 110-111) — specifically `[name="name"]` and `[name="description"]` — are passed unsanitised as form field values. If these fields contain HTML or script content that gets stored and re-rendered, a stored XSS scenario is possible.

B07-45 | Severity: MEDIUM | The `action` request parameter (line 3) is read but never used in the JSP rendering or form submission. Its presence as an unused variable is dead code and an unclear API surface.

B07-46 | Severity: LOW | Date/time inputs `startTime` and `endTime` are rendered with placeholder text set via JavaScript (`$("#startTime").attr('placeholder', 'Start Time')`). There is no server-side validation of the date format noted in the JSP — time values are sent as freeform strings. No test validates accepted date formats.

B07-47 | Severity: INFO | Zero test coverage: no test exercises this JSP, its driver selection, form submission, or the broken `fnAssign()` logic.

---

### 8. `vehicle/impact.jsp`

**Purpose:** Impact sensor calibration tab for a vehicle. Displays a calibration progress bar when calibration is incomplete (percentage != 100.0), or a G-force threshold table when fully calibrated. Provides a "RESET Calibration" button when calibrated. Tab layout is conditional on `isDealer` session attribute. Backed by `AdminUnitImpactAction`.

**Scriptlet blocks:**
```java
// Lines 6-11
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String urlGeneral = id.isEmpty() ? "adminunit.do?action=add" : "adminunit.do?action=edit&equipId=" + id;
boolean isDealer = session.getAttribute("isDealer").equals("true");
ImpactBean impact = (ImpactBean) request.getAttribute("impactBean");
```

**EL / Struts tag attribute access:**
- `name="impactBean"` — request attribute; property `percentage` used in `<logic:equal>`, `<logic:notEqual>`, `<bean:write>` and inside a CSS `content:` pseudo-element value
- `name="isDealer"` — session attribute used for tab count class selection and `<logic:equal>`

**JavaScript with security implications:**
- Lines 109-133: `$('#calibration_slider').trigger('change')` is called on an element that does not exist in this JSP. Dead code / potential error.
- Lines 112-123: Slider JavaScript references `$("#FSSX_multiplicator").val()` — this element also does not appear in the JSP markup. The slider is initialised but its value basis is undefined (will be `undefined`, causing `NaN` arithmetic). Dead/broken JavaScript.

**Findings:**

B07-48 | Severity: CRITICAL | `session.getAttribute("isDealer").equals("true")` at line 9 will throw a `NullPointerException` if `isDealer` is not present in the session (session timeout, new session, or misconfiguration). There is no null check. This would result in a 500 error on every impact page load for any session that lacks `isDealer`. No test exercises this null path.

B07-49 | Severity: HIGH | `(ImpactBean) request.getAttribute("impactBean")` at line 10 is cast without null checking. If `impactBean` is absent from the request (e.g., when the action did not set it), any subsequent use of `impact.calculateGForceRequiredForImpact(...)` at line 71 will throw a `NullPointerException`. No test verifies that the action always populates this attribute.

B07-50 | Severity: HIGH | `id` from `request.getParameter("equipId")` (line 7) is embedded without HTML encoding into multiple tab navigation `href` attributes (lines 40-46) and into a hidden input `value` (line 85: `value="<%=id %>"`). HTML injection is possible with a crafted parameter.

B07-51 | Severity: HIGH | The `<bean:write name="impactBean" property="percentage"/>` expression at line 27 is rendered inside a CSS `content:` pseudo-element value within a `<style>` block. If `percentage` contains `"`, `\`, or `}` characters, CSS injection could close the rule block and inject arbitrary CSS. Although percentage values are expected to be numeric, the lack of type enforcement at the JSP layer is a defect.

B07-52 | Severity: MEDIUM | `isDealer` is injected into a JSP scriptlet expression at line 39: `<%= isDealer ? "five" : "four" %>`. This determines the CSS class for the tab list. The boolean is derived from a string comparison at line 9 and is safe here, but the pattern of deriving rendering logic from unchecked session state is fragile.

B07-53 | Severity: MEDIUM | `String.format("%.1fg", impact.calculateGForceRequiredForImpact(impactLevel))` at line 71 is executed inside a `<logic:iterate>` over `ImpactLevel.values()`. If `impact` is null (see B07-49), all iterations throw NPE. If `calculateGForceRequiredForImpact` throws, the error is unhandled. No test covers iteration failure modes.

B07-54 | Severity: LOW | The slider JavaScript (lines 109-133) references DOM elements (`#calibration_slider`, `#FSSX_multiplicator`) that do not exist in this JSP. This indicates removed or never-connected UI components. The slider is initialised with an undefined value, producing `NaN` for `calValue`. This dead JavaScript generates browser console errors. No test detects this regression.

B07-55 | Severity: INFO | The existing `ImpactUtilTest.java` and calibration tests cover the utility/calibration logic but have zero coverage of the JSP rendering logic, null-attribute paths, or CSS injection surface.

---

### 9. `vehicle/service.jsp`

**Purpose:** Service configuration tab for a vehicle unit. Displays service status (status, hours till next service, accumulated hours) and service settings (service type: by set hours or by interval, with relevant input fields). Submits to `adminunitservice.do`. Tab layout is conditional on `isDealer`.

**Scriptlet blocks:**
```java
// Lines 3-12
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String urlGeneral;
if (!id.equalsIgnoreCase("")) {
    urlGeneral = "adminunit.do?action=edit&equipId=" + id;
} else {
    urlGeneral = "adminunit.do?action=add";
}
```

**EL / Struts tag attribute access:**
- `name="isDealer"` — session/request attribute tested via `<logic:equal>` and `<logic:notEqual>` for tab layout
- `name="serviceBean"` — request attribute; properties: `servStatus`, `hoursTillNextService`, `accHours`, `servType`, `servLast`, `servNext`, `servDuration`, `unitId`

**JavaScript with security implications:**
- Lines 201-208: `setupConfirmationPopups` is called with a hardcoded action URL. No variable injection.

**Findings:**

B07-56 | Severity: HIGH | `id` from `request.getParameter("equipId")` (line 4) is embedded unencoded into multiple tab navigation `href` attributes (lines 17-29) and into a hidden input `value` at line 181 (`value="<%=id %>"`). No HTML encoding is applied. HTML injection is possible with a crafted `equipId` parameter.

B07-57 | Severity: HIGH | `<bean:write name="serviceBean" property="servStatus"/>` at line 50 renders the service status string directly to HTML without `filter="true"`. If `servStatus` is sourced from user-controlled or device-supplied data, XSS is possible.

B07-58 | Severity: HIGH | `<bean:write name="serviceBean" property="hoursTillNextService"/>` at line 57 and other numeric `<bean:write>` outputs (lines 57, 64 via `accHours`) have no explicit HTML encoding. Although these are expected to be numeric, the JSP imposes no type constraint. Malicious database content would render unescaped.

B07-59 | Severity: MEDIUM | The `action` parameter (line 3) is read and stored in a local variable but is never used within the JSP rendering logic. It is dead code that widens the request parameter attack surface unnecessarily.

B07-60 | Severity: MEDIUM | The service type rendering logic uses mirrored `<logic:equal>`/`<logic:notEqual>` pairs to conditionally show/hide divs using inline `style="display:none"`. This approach duplicates HTML structure and makes the view logic difficult to reason about correctly. Two divs at lines 159-163 carry duplicate `data-serv-type` attributes (both `data-serv-type="interval"` and `data-serv-type="setHrs"` — line 160 has both on the same element), which appears to be a copy-paste error. No test verifies the correct rendering state for each service type.

B07-61 | Severity: INFO | Zero test coverage: no test exercises service JSP rendering for either service type, the tab layout, or form submission.

---

### 10. `vehicle/view_job_details.jsp`

**Purpose:** Read-only list view of job details for a vehicle. Displays driver name, job number, status (mapped from integer codes 1/2/3 to labels Start/Complete/Pause), start time, end time, and duration. Data comes from the `arrJobDetails` request attribute. No forms, no JavaScript.

**Scriptlet blocks:** None.

**EL / Struts tag attribute access:**
- `name="arrJobDetails"` — request attribute; iterated; `type="com.bean.JobDetailsBean"`; properties rendered: `driverName`, `jobNo`, `status`, `startTime`, `endTime`, `duration`

**JavaScript with security implications:** None (no JavaScript in this file).

**Findings:**

B07-62 | Severity: HIGH | `<bean:write name="jobDetails" property="driverName"/>` (line 24), `<bean:write ... property="jobNo"/>` (line 27), `<bean:write ... property="startTime"/>` (line 41), `<bean:write ... property="endTime"/>` (line 45), `<bean:write ... property="duration"/>` (line 48) all render request-attribute bean properties directly to HTML. None use `filter="true"`. Driver names in particular are user-entered strings. If any of these properties contain HTML special characters, unescaped output results in XSS. This is a stored XSS risk as the data originates from the database.

B07-63 | Severity: MEDIUM | Job status codes 1, 2, and 3 are mapped to human-readable labels (`Start`, `Complete`, `Pause`) using three separate `<logic:equal>` comparisons. Status code `0` or any value outside 1-3 silently produces no output — the cell is rendered blank with no fallback or error indicator. This edge case is untested and could confuse users or indicate unexpected data states.

B07-64 | Severity: MEDIUM | The `<body>` tag at line 3 is an anomaly: this JSP is included as a fragment inside a larger page layout (modal), but it declares its own `<body>` tag, which creates invalid nested `<body>` elements in the rendered HTML. The same issue is present in `driver_job_details.jsp` (line 8). No test detects malformed HTML structure.

B07-65 | Severity: LOW | If `arrJobDetails` is null (rather than empty), `<logic:notEmpty>` suppresses rendering and the table body is empty — but the enclosing panel with its header row is still rendered, producing a visually empty panel with no "no data" message. User experience is degraded and no test verifies the empty-state rendering.

B07-66 | Severity: INFO | Zero test coverage: no test exercises this JSP's rendering with any data state (populated, empty, or null collection).

---

## Summary Table

| Finding ID | JSP File | Severity | Category |
|------------|----------|----------|----------|
| B07-1 | settings/subscription.jsp | HIGH | Dead code / potential XSS vector |
| B07-2 | settings/subscription.jsp | MEDIUM | Dead code — unused session attribute |
| B07-3 | settings/subscription.jsp | MEDIUM | Dead code — unused request parameter |
| B07-4 | settings/subscription.jsp | MEDIUM | Dead code — orphaned/unused view |
| B07-5 | settings/subscription.jsp | HIGH | XSS — unencoded bean:write output |
| B07-6 | settings/subscription.jsp | LOW | Incomplete implementation — non-functional delete UI |
| B07-7 | settings/subscription.jsp | INFO | Zero test coverage |
| B07-8 | users/general.jsp | CRITICAL | Broken cryptography — MD5 password hashing |
| B07-9 | users/general.jsp | HIGH | Logic error — pass_hash never populated on password entry |
| B07-10 | users/general.jsp | HIGH | HTML injection — unencoded driverId in href |
| B07-11 | users/general.jsp | HIGH | JS injection — unescaped scriptlet in JS string literal |
| B07-12 | users/general.jsp | MEDIUM | Validation logic defect — mobile validation unreachable |
| B07-13 | users/general.jsp | MEDIUM | Off-by-one in password length validation |
| B07-14 | users/general.jsp | MEDIUM | Side-effect request mutation in view layer |
| B07-15 | users/general.jsp | INFO | Zero test coverage |
| B07-16 | users/subscription.jsp | HIGH | JS runtime error — wrong form name reference, validation bypassed |
| B07-17 | users/subscription.jsp | HIGH | NumberFormatException — unguarded Long.valueOf on request param |
| B07-18 | users/subscription.jsp | MEDIUM | Dead code — unreachable null check on Long |
| B07-19 | users/subscription.jsp | MEDIUM | HTML injection — id embedded in href |
| B07-20 | users/subscription.jsp | INFO | Typo in user-visible success message |
| B07-21 | users/subscription.jsp | INFO | Zero test coverage |
| B07-22 | vehicle/access.jsp | HIGH | HTML injection — unencoded id in href attributes |
| B07-23 | vehicle/access.jsp | HIGH | HTML injection — id in multiple tab href attributes |
| B07-24 | vehicle/access.jsp | MEDIUM | Null session attribute — isDealer not null-checked |
| B07-25 | vehicle/access.jsp | LOW | Hardcoded access type / keypad values without enumeration |
| B07-26 | vehicle/access.jsp | INFO | Zero test coverage |
| B07-27 | vehicle/adminUnitEdit.jsp | HIGH | HTML injection — unencoded equipId in hrefs and hidden inputs |
| B07-28 | vehicle/adminUnitEdit.jsp | HIGH | URL parameter injection — field values not encoded in AJAX URLs |
| B07-29 | vehicle/adminUnitEdit.jsp | HIGH | HTML injection — unencoded action param in hidden input |
| B07-30 | vehicle/adminUnitEdit.jsp | MEDIUM | Deprecated synchronous AJAX — UI blocking |
| B07-31 | vehicle/adminUnitEdit.jsp | MEDIUM | Inconsistent notification — native alert() vs. swal |
| B07-32 | vehicle/adminUnitEdit.jsp | MEDIUM | ClassCastException risk — unguarded attribute cast |
| B07-33 | vehicle/adminUnitEdit.jsp | LOW | Zero-size field hidden — UX defect, untested |
| B07-34 | vehicle/adminUnitEdit.jsp | INFO | Zero test coverage |
| B07-35 | vehicle/assignment.jsp | CRITICAL | NullPointerException — sessDateFormat not null-checked |
| B07-36 | vehicle/assignment.jsp | HIGH | JS string injection — dateFormat injected into JS literal |
| B07-37 | vehicle/assignment.jsp | HIGH | HTML injection — unencoded equipId in hrefs and hidden input |
| B07-38 | vehicle/assignment.jsp | MEDIUM | URL parameter injection — dates not encoded in AJAX URL |
| B07-39 | vehicle/assignment.jsp | MEDIUM | XSS — company_name rendered without filter="true" |
| B07-40 | vehicle/assignment.jsp | INFO | Zero test coverage |
| B07-41 | vehicle/driver_job_details.jsp | HIGH | HTML injection — jobId and equipId in hidden input values |
| B07-42 | vehicle/driver_job_details.jsp | HIGH | Functional defect — driverId never submitted due to JS typo |
| B07-43 | vehicle/driver_job_details.jsp | HIGH | Dead code — fnsubmitAccount() referencing wrong form |
| B07-44 | vehicle/driver_job_details.jsp | MEDIUM | Stored XSS risk — unsanitised values from parent modal |
| B07-45 | vehicle/driver_job_details.jsp | MEDIUM | Dead code — action parameter unused |
| B07-46 | vehicle/driver_job_details.jsp | LOW | No server-side date format validation for time inputs |
| B07-47 | vehicle/driver_job_details.jsp | INFO | Zero test coverage |
| B07-48 | vehicle/impact.jsp | CRITICAL | NullPointerException — isDealer session attribute not null-checked |
| B07-49 | vehicle/impact.jsp | HIGH | NullPointerException — impactBean request attribute not null-checked |
| B07-50 | vehicle/impact.jsp | HIGH | HTML injection — unencoded equipId in hrefs and hidden input |
| B07-51 | vehicle/impact.jsp | HIGH | CSS injection — bean:write output inside CSS content: property |
| B07-52 | vehicle/impact.jsp | MEDIUM | Fragile rendering logic — boolean from unchecked session string |
| B07-53 | vehicle/impact.jsp | MEDIUM | Unhandled exception — ImpactBean method call inside iterate |
| B07-54 | vehicle/impact.jsp | LOW | Dead JavaScript — missing DOM elements for slider |
| B07-55 | vehicle/impact.jsp | INFO | Existing tests cover utility only; zero JSP coverage |
| B07-56 | vehicle/service.jsp | HIGH | HTML injection — unencoded equipId in hrefs and hidden input |
| B07-57 | vehicle/service.jsp | HIGH | XSS — servStatus rendered without filter="true" |
| B07-58 | vehicle/service.jsp | HIGH | XSS — numeric bean:write outputs lack explicit encoding |
| B07-59 | vehicle/service.jsp | MEDIUM | Dead code — action parameter unused |
| B07-60 | vehicle/service.jsp | MEDIUM | Duplicate data attributes — copy-paste error in service type rendering |
| B07-61 | vehicle/service.jsp | INFO | Zero test coverage |
| B07-62 | vehicle/view_job_details.jsp | HIGH | Stored XSS — multiple bean:write outputs lack filter="true" |
| B07-63 | vehicle/view_job_details.jsp | MEDIUM | Missing fallback for unknown job status codes |
| B07-64 | vehicle/view_job_details.jsp | MEDIUM | Invalid HTML — nested body tag in JSP fragment |
| B07-65 | vehicle/view_job_details.jsp | LOW | No empty-state message when arrJobDetails is null/empty |
| B07-66 | vehicle/view_job_details.jsp | INFO | Zero test coverage |

---

## Cross-Cutting Issues

**CC-1 | Severity: CRITICAL | Systemic absence of JSP test coverage.** Zero test files exist for any of the 10 audited JSPs or any other JSP in the project. The 4 existing test files cover only back-end calibration and utility logic. All view-layer scriptlet logic, conditional rendering, URL construction, and JavaScript behaviour is completely untested.

**CC-2 | Severity: HIGH | Systemic bean:write XSS risk.** The `<bean:write>` Struts tag does not HTML-encode output unless `filter="true"` is explicitly specified. Across all 10 JSPs, properties from request-attribute beans (`driverName`, `company_name`, `servStatus`, `alert_name`, `frequency`, `jobNo`, `startTime`, `endTime`, `duration`) are rendered without `filter="true"`. Any of these properties sourced from user input or external data is a stored XSS vector.

**CC-3 | Severity: HIGH | Systemic unencoded request parameter injection into URLs.** Across 8 of the 10 JSPs, the `equipId`, `id`, `driverId`, or `action` request parameter is concatenated without encoding into HTML `href` attributes and/or hidden `<input value>` attributes. The same vulnerability pattern is replicated in every vehicle tab JSP (access, adminUnitEdit, assignment, impact, service).

**CC-4 | Severity: MEDIUM | Systemic absence of null-checks on session and request attributes.** The pattern `session.getAttribute("x").equals(...)` (without null check) appears in `impact.jsp` (line 9) and the pattern of reading session attributes without null checks appears throughout. A session timeout or cold start can cause NullPointerExceptions across multiple views.

**CC-5 | Severity: MEDIUM | Systemic synchronous AJAX.** `async: false` is used in `adminUnitEdit.jsp` (line 289) and `assignment.jsp` (line 147). This is deprecated in all modern browsers and causes UI thread blocking. No test validates degraded or error states for these calls.
