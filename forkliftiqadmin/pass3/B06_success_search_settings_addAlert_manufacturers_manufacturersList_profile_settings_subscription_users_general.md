# Pass 3 Documentation Audit — Agent B06
**Date:** 2026-02-26
**Auditor:** B06
**Scope:** 9 JSP files covering result/success, search, settings (add-alert, manufacturers, manufacturersList, profile, settings, subscription), and users/general

---

## Reading Evidence

---

### File 1: `html-jsp/result/success.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/result/success.jsp`

**Purpose:** Returns an HTTP 200 result stub. The file contains only a pseudo-XML result element with a status of 200 — no HTML, no JSP scriptlet logic, no form, no JavaScript. It appears to be a static success-response fragment used as a server-side include or a stand-alone response target to signal an HTTP 200 OK to an AJAX caller.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:** None.

**HTML form `action` attributes:** None.

**Session attribute accesses:** None.

**Significant JavaScript functions:** None.

---

### File 2: `html-jsp/search.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/search.jsp`

**Purpose:** Driver/vehicle search form. Allows the user to search by driver name (with typeahead), select a vehicle unit, and select an attachment. Provides submit and print buttons. The print button is hidden until a vehicle is selected.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`

**HTML form `action` attributes:**
- Line 8: `action="search.do"` (Struts `<html:form>`)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions defined:**
- `fnprint()` (lines 83–90): Reads form field values and opens a print report URL in a new popup window.
- `fnbarcode()` (lines 92–110): Reads form field values, detects IE vs non-IE browser, and opens a barcode print URL in a new popup window.
- `fnshowprint(veh)` (lines 113–123): Shows or hides the print button depending on whether a vehicle is selected.
- Anonymous `$(document).ready` (lines 48–77): Fetches XML driver list via AJAX and populates the typeahead array; also initializes the Bootstrap Typeahead plugin (lines 79–81, outside the ready block).

**Commented-out code:**
- Lines 28–31: An HTML comment block wrapping `<div class='printbtn clearfix'>` and two JSP comments wrapping `<html:button>` elements for print and barcode. These appear to be an earlier incarnation of the print/barcode buttons that were replaced by the live buttons at lines 36 and (the now-dead `fnbarcode`) still referenced in `fnbarcode()`.

---

### File 3: `html-jsp/settings/add-alert.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/add-alert.jsp`

**Purpose:** Modal/embedded form that allows an admin to subscribe to an alert by selecting from a pre-populated list of available alerts. Submits via AJAX (class `ajax_mode_c`) to `adminAlertAdd.do`.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp"%>`

**HTML form `action` attributes:**
- Line 3: `action="adminAlertAdd.do"` (Struts `<html:form>`)

**Session attribute accesses:** None.

**Significant JavaScript functions defined:** None.

---

### File 4: `html-jsp/settings/manufacturers.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturers.jsp`

**Purpose:** Settings tab page for managing forklift manufacturers. Displays a table of existing manufacturers with Edit/Save/Delete buttons, and provides a text input + Add button to create new manufacturers. All CRUD operations use AJAX (jQuery `.post`/`.get`) against `manufacturers.do` with an `action` parameter. The `delete_manufacturer` function first checks if the manufacturer is assigned to any vehicle before permitting deletion. A `logic:notEmpty` guard on `company_id` controls which rows show Edit/Delete buttons.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):**
- Line 54: `<%= manufacturer.getName() %>` — populates the hidden edit input's value.
- Line 55: `<%= manufacturer.getId() %>` — populates the edit input's `id` attribute.
- Line 59: `<%= manufacturer.getId() %>` — populates the edit button's `id` attribute.
- Line 64: `<%= manufacturer.getId() %>` — populates the save button's `id` attribute.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 17: `action="manufacturers.do"` (Struts `<html:form>`)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions defined:**
- `add_manufacturer()` (lines 92–103): POSTs `action=add` with the entered manufacturer name; on success calls `prepareTable(data)`.
- `edit_manufacturer(id)` (lines 105–110): Toggles display to show the edit input and save button, hide the display div and edit button.
- `save_manufacturer(id)` (lines 112–121): POSTs `action=edit` with the new manufacturer name; on success calls `prepareTable(data)`.
- `delete_manufacturer(id)` (lines 123–142): GETs `action=isVehicleAssigned`; if not assigned, POSTs `action=delete`; on success calls `prepareTable(data)`.
- `prepareTable(data)` (lines 144–175): Parses JSON response and rebuilds the `#tableManu` tbody HTML. Contains a single inline comment at line 145.

---

### File 5: `html-jsp/settings/manufacturersList.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/manufacturersList.jsp`

**Purpose:** A minimal JSP that retrieves a JSON object from the session attribute `"json"` and writes it directly to the HTTP response as `application/json`. This is a JSON data-serving fragment (not a visual page) used to return manufacturer list data to AJAX callers.

**JSP scriptlet blocks (`<% %>`):**
- Lines 7–9: Retrieves the `JSONObject` stored under session attribute key `"json"` and assigns it to the local variable `obj`.

**JSP expression blocks (`<%= %>`):**
- Line 11: `<%=obj%>` — outputs the JSON object as the entire response body.

**`<%@ include %>` / `<jsp:include>` directives:** None (uses `<%@ page import=...>` only).

**HTML form `action` attributes:** None.

**Session attribute accesses:**
- Line 8: `request.getSession().getAttribute("json")` — session key `"json"`.

**Significant JavaScript functions defined:** None.

---

### File 6: `html-jsp/settings/profile.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/profile.jsp`

**Purpose:** Admin company profile and account info edit page. Allows the admin to update the company name, address, and their own contact details (first/last name, email, mobile, password). Client-side validation is performed before form submission.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):**
- Line 110: `<%=request.getAttribute("userSmsAlertExisting")%>` — injects the `userSmsAlertExisting` request attribute value into the JavaScript variable `smsUsrAlertExisting`.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp"%>`

**HTML form `action` attributes:**
- Line 14: `action="adminRegister.do"` (Struts `<html:form>`)

**Session attribute accesses:** None directly in this file (request attribute only at line 110).

**Significant JavaScript functions defined:**
- `fnsubmitAccount()` (lines 103–145): Validates company name, email, password match, password length, and mobile number format (must be numeric, must start with `+`). If `cmobile` is empty and `smsUsrAlertExisting` is truthy, blocks submission. Otherwise submits the form.
- Anonymous `jQuery(document).ready` (lines 147–150): Invokes `$('#pword').strength()` for password strength display; note `#pword` does not appear in the HTML above — likely targets an element in an included layout or is a dead selector.

---

### File 7: `html-jsp/settings/settings.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/settings.jsp`

**Purpose:** Company settings configuration page. Allows the admin to set the date format, timezone, and maximum session length. Also conditionally displays a "Run Unit Calibration Job" button for super-admins only. Includes notification checkboxes for Red Impact Email, Red Impact SMS, and Training Expiry Email alerts.

**JSP scriptlet blocks (`<% %>`):**
- Lines 4–7: Reads `sessDateTimeFormat` and `timezoneId` from the HTTP session and assigns to local String variables `dateFormat` and `compTimezone`.

**JSP expression blocks (`<%= %>`):**
- Line 171: `<%=dateFormat %>` — injects the current date format into JavaScript to pre-select the dropdown.
- Line 174: `<%=compTimezone %>` — injects the current timezone ID into JavaScript to pre-select the dropdown.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 2: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 16: `action="settings.do"` (Struts `<html:form>`)

**Session attribute accesses:**
- Line 5: `session.getAttribute("sessDateTimeFormat")` — session key `"sessDateTimeFormat"`.
- Line 6: `session.getAttribute("timezoneId")` — session key `"timezoneId"`.

**Significant JavaScript functions defined:**
- `isValid()` (lines 136–161): Validates that dateFormat, maxSessionLength (>= 15), mobile (required when SMS alert checked), and timezone are all populated.
- `send()` (lines 163–167): Calls `isValid()` and displays a SweetAlert error if invalid.
- Anonymous IIFE (lines 169–179): Pre-selects the dateFormat and timezone dropdowns from JSP-injected values, and wires `form.onsubmit` to call `isValid()`.
- `calibrate()` (lines 181–187): Sends an AJAX POST to `calibration.do` to trigger the unit calibration job.

---

### File 8: `html-jsp/settings/subscription.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/settings/subscription.jsp`

**Purpose:** Subscription management page showing two tables: existing alert subscriptions and existing report subscriptions. Each row has a "Delete" placeholder (non-functional — no click handler). Buttons to add a new alert or report open a lightbox modal linking to `adminalert.do?action=alerts` and `adminalert.do?action=reports` respectively.

**JSP scriptlet blocks (`<% %>`):**
- Lines 5–12: Reads `op_code`, `message`, `user_cd` session attribute, `form_cd` request parameter, and computes a timestamp string. Variables `op_code`, `message`, `form_cd`, and `timeStamp` are declared and assigned but **none of them are used anywhere in the rest of the file**.

**JSP expression blocks (`<%= %>`):** None (scriptlet variables are never output).

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 3: `<%@ include file="../../includes/importLib.jsp"%>`

**HTML form `action` attributes:** None (no `<html:form>` or `<form>` elements).

**Session attribute accesses:**
- Line 8: `session.getAttribute("user_cd")` — session key `"user_cd"`.

**Significant JavaScript functions defined:** None.

---

### File 9: `html-jsp/users/general.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/users/general.jsp`

**Purpose:** Add/Edit user (driver) general information form. Detects whether the page is in "add" or "edit" mode based on the `action` request parameter. In edit mode it pre-populates form fields from the `driver` bean. Fields include first/last name, mobile, email, password, and confirm password. Client-side validation enforces required fields and password constraints before submission.

**JSP scriptlet blocks (`<% %>`):**
- Lines 4–28: Reads `action` and `driverId` request parameters, sets URLs, `op_code`, and `actionCode` based on whether action is `"edituser"`. Also resolves `id` from `newDriverId` request attribute if the parameter is blank and the attribute is present.

**JSP expression blocks (`<%= %>`):**
- Line 33: `<%=generalUrl%>` — injects the General tab URL.
- Line 34: `<%=subscriptionUrl%>` — injects the Notification/Subscription tab URL.
- Line 38: `<%=actionCode %>` — form action URL.
- Line 118: `<%=id %>` — hidden field value for driver ID.
- Line 119: `<%=op_code %>` — hidden field value for operation code.
- Line 206: `<%=actionCode %>` — JavaScript variable for AJAX confirmation popup URL.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 2: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 38: `action="<%=actionCode %>"` (Struts `<html:form>`) — resolves to `admindriveredit.do` (edit) or `admindriveradd.do` (add).

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions defined:**
- `displayRequiredFields()` (lines 127–166): Highlights required fields with a red border if empty; disables the submit button if validation fails.
- `validateFields(valid)` (lines 168–196): Checks password match, password length (< 6 chars), mobile number format, and computes MD5 hash of the password into the `pass_hash` hidden field.
- Anonymous `$(document).ready` (lines 198–213): Calls `validateFields(displayRequiredFields())` on load; wires `change` events on all inputs; calls `setupConfirmationPopups` with the form element, action URL, and success/error messages.

---

## Findings

---

**B06-1 | LOW | result/success.jsp:1 | Missing page-level comment**

`success.jsp` has no HTML or JSP comment explaining its purpose. The file contains only a pseudo-XML result stub (`<result name="empty" ...>`). Without a comment, a developer cannot easily determine whether this is a Struts result forwarding target, an AJAX response fragment, or an error. A one-line description would suffice.

---

**B06-2 | LOW | search.jsp:1 | Missing page-level comment**

`search.jsp` has no page-level HTML or JSP comment describing its purpose (driver/vehicle search form), its dependencies (Struts bean collections `arrUnit`, `arrAttachment`), or its expected session state.

---

**B06-3 | LOW | search.jsp:28-31 | Dead commented-out code with no explanation**

Lines 28–31 contain a block of commented-out HTML and JSP markup:

```
<!-- <div class='printbtn clearfix' style='display:none'> -->
<%-- <html:button property="print" ...>...</html:button> --%>
<%-- <html:button property="barcode" ...>...</html:button> --%>
<!-- </div> -->
```

These are the original print/barcode buttons. No comment explains why they were commented out, or whether they are safe to delete. The `fnbarcode()` function (lines 92–110) is still defined and still referenced nowhere in the live markup, suggesting related dead code.

---

**B06-4 | LOW | search.jsp:92-110 | Dead JavaScript function with no comment**

`fnbarcode()` (lines 92–110) is a fully implemented function but is never called from any live HTML element (the only `onclick="fnbarcode()"` button was commented out at lines 29–30). No comment explains whether this function is retained intentionally for future use or is safe to remove.

---

**B06-5 | MEDIUM | search.jsp:48-77 | Complex AJAX scriptlet block without comment**

The `$(document).ready` block (lines 48–77) performs a synchronous AJAX call (`async:false`) to `getXml.do`, then applies a browser-specific IE code path using `ActiveXObject` to parse XML for the typeahead data source. There is no comment explaining:
- Why `async:false` is used (a deprecated and blocking pattern).
- Why a separate IE/non-IE branch is required.
- What the expected XML structure is (the `<rec><name>` element structure is implicit).

This is non-trivial logic that warrants at minimum a short explanatory comment.

---

**B06-6 | LOW | add-alert.jsp:1 | Missing page-level comment**

`add-alert.jsp` has no page-level comment describing its purpose (modal form for subscribing to an alert), required request-scoped data (`alertList` collection), or the AJAX submission pattern (`ajax_mode_c` style class).

---

**B06-7 | LOW | add-alert.jsp:10 | Magic `style` attribute used as data attribute**

Line 10: `style="adminalert.do?action=alerts"` is set on the `<html:select>` element. This is plainly not a CSS style value — it appears to be a data value (a URL) masquerading as a `style` attribute, likely consumed by JavaScript to dynamically load alert options. There is no comment explaining this unconventional usage.

---

**B06-8 | LOW | manufacturers.jsp:1 | Missing page-level comment**

`manufacturers.jsp` has no page-level comment describing its purpose, required backing beans (`arrManufacturers`), or its AJAX-based CRUD pattern.

---

**B06-9 | LOW | manufacturers.jsp:153 | Undocumented `company_id` guard logic**

Line 153 (inside `prepareTable`) and lines 58/74 (in the Struts iterate block) gate the Edit/Delete buttons on `typeof elem.company_id !== 'undefined'` / `<logic:notEmpty property="company_id">`. There is no comment explaining the business rule: presumably manufacturers without a `company_id` are global/system-level records that should not be editable by a company admin. This is a non-obvious access-control implication with no documentation.

---

**B06-10 | LOW | manufacturersList.jsp:1 | Missing page-level comment**

`manufacturersList.jsp` has no page-level comment. The file's purpose — to emit a JSON response from a session attribute — is completely non-obvious from the file name alone (which implies a visual list page). A comment is especially important here because the file is not a display page.

---

**B06-11 | MEDIUM | manufacturersList.jsp:8 | Cryptic session attribute key `"json"` with no documentation**

Line 8: `request.getSession().getAttribute("json")` uses the key `"json"`. This is highly ambiguous: it says nothing about what JSON is stored, who stores it, or when. If another action accidentally stores a different object under `"json"`, this page will either crash or emit wrong data. No comment documents the expected producer or content of this session attribute.

---

**B06-12 | LOW | profile.jsp:1 | Missing page-level comment**

`profile.jsp` has no page-level comment describing its purpose (admin company profile + account info editor), required backing bean (`companyRecord`), or the `ajax_mode_c` form submission pattern.

---

**B06-13 | LOW | profile.jsp:110 | Undocumented `userSmsAlertExisting` request attribute**

Line 110: `<%=request.getAttribute("userSmsAlertExisting")%>` injects a request attribute into JavaScript. The attribute name `userSmsAlertExisting` is reasonably named but its type (Boolean? String?) and its producer (which Action sets this attribute?) are undocumented. The injected value is used in a boolean conditional at line 138, where truthiness matters — if the attribute is null this evaluates to the literal string `"null"` in JavaScript, which is truthy, potentially causing a spurious validation error.

---

**B06-14 | MEDIUM | profile.jsp:147-150 | Dead/incorrect selector `#pword` in jQuery ready block**

Lines 147–150:
```javascript
jQuery(document).ready(function($) {
    $('#pword').strength();
});
```
There is no element with `id="pword"` anywhere in `profile.jsp`. The password input at line 75 has `name="pin"` and no `id` attribute. The `$('#pword').strength()` call silently does nothing. No comment documents whether this is intentionally disabled, a vestigial call from a renamed element, or a genuine bug.

---

**B06-15 | LOW | settings.jsp:1 | Missing page-level comment**

`settings.jsp` has no page-level comment describing its purpose, required session attributes, backing beans (`dateFormats`, `timezones`, `redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`, `isSuperAdmin`), or the form's action.

---

**B06-16 | LOW | settings.jsp:5-6 | Undocumented session attribute keys `"sessDateTimeFormat"` and `"timezoneId"`**

Lines 5–6 read two session attributes with non-self-documenting keys. `"sessDateTimeFormat"` uses a `sess` prefix that is inconsistent with other session keys such as `"user_cd"` and `"timezoneId"`. No comment describes the expected format of these values or which component writes them.

---

**B06-17 | LOW | settings.jsp:71 | Undocumented `isSuperAdmin` bean with no comment**

Line 71: `<logic:equal name="isSuperAdmin" value="true">` gates the calibration button. The bean name `isSuperAdmin` is set by an upstream action, but there is no comment explaining this access-control gate, what distinguishes a super-admin from a regular admin, or why calibration is super-admin-only.

---

**B06-18 | LOW | subscription.jsp:1 | Missing page-level comment**

`subscription.jsp` has no page-level comment describing its purpose (display and manage alert/report subscriptions for a company), required backing beans (`alertList`, `reportList`), or the lightbox-based add flows.

---

**B06-19 | MEDIUM | subscription.jsp:5-12 | Non-trivial scriptlet with entirely unused variables**

Lines 5–12 declare and populate five local variables (`op_code`, `message`, `user`, `form_cd`, `timeStamp`):

```java
String op_code="alert_list";
String message=request.getParameter("message")==null?"":request.getParameter("message");
String user = (String)session.getAttribute("user_cd");
String form_cd = request.getParameter("form_cd")==null?"":request.getParameter("form_cd");
String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime());
```

None of these variables are used anywhere in the rest of the file (no `<%= ... %>` expressions and no scriptlet references below line 12). There is no comment explaining why this block exists or whether it is dead code from a prior implementation. The `Calendar`/`SimpleDateFormat` imports at lines 1–2 exist solely to support `timeStamp`, compounding the confusion. This should either be explained with a comment or removed.

---

**B06-20 | LOW | subscription.jsp:39 | Non-functional "Delete" placeholder with no comment**

Lines 39 and 76 contain the literal text `Delete` as a table cell value with no `onclick`, no link, no form, and no JavaScript:
```html
<td>Delete</td>
```
There is no comment indicating whether this is a future placeholder, a UI regression, or intentionally inactive. A developer reading the code would not know if this is broken functionality.

---

**B06-21 | LOW | users/general.jsp:1 | Missing page-level comment**

`general.jsp` has no page-level comment describing its dual-mode nature (add vs. edit user), the role of the `action` request parameter in switching modes, or the expected backing beans (`driver`).

---

**B06-22 | MEDIUM | users/general.jsp:4-28 | Multi-branch scriptlet with no comment**

Lines 4–28 contain a 24-line scriptlet that:
1. Reads `action` and `driverId` parameters.
2. Branches on `action.equalsIgnoreCase("edituser")` to set URLs and operation codes.
3. Handles a special case where `id` is blank but `newDriverId` is set as a request attribute, then removes that attribute.

No comment explains the `newDriverId` request attribute, why it must be removed after being read (presumably to avoid reuse across redirects), or what `op_code` values (`"edit_general_user"`, `"add_general_user"`) mean downstream. This is the most complex scriptlet in the file and it has no documentation at all.

---

**B06-23 | LOW | users/general.jsp:190 | MD5 password hashing without comment**

Lines 190–191:
```javascript
var password = '' + CryptoJS.MD5($('input[name="pass"]').val());
$('input[name=pass_hash]').val(password);
```
The plain-text password is hashed client-side with MD5 before submission. MD5 is a cryptographically broken algorithm for password hashing. There is no comment explaining this design choice, whether server-side hashing also occurs, or that this is a known legacy pattern. The absence of documentation makes it impossible to assess the full security posture from this file alone.

---

## Summary Table

| ID     | Severity | File:Line                                      | Description                                                                          |
|--------|----------|------------------------------------------------|--------------------------------------------------------------------------------------|
| B06-1  | LOW      | result/success.jsp:1                           | Missing page-level comment                                                           |
| B06-2  | LOW      | search.jsp:1                                   | Missing page-level comment                                                           |
| B06-3  | LOW      | search.jsp:28-31                               | Dead commented-out print/barcode button block with no explanation                    |
| B06-4  | LOW      | search.jsp:92-110                              | Dead `fnbarcode()` function — never called, no comment                               |
| B06-5  | MEDIUM   | search.jsp:48-77                               | Complex synchronous AJAX + IE/non-IE XML parse with no explanatory comment           |
| B06-6  | LOW      | add-alert.jsp:1                                | Missing page-level comment                                                           |
| B06-7  | LOW      | add-alert.jsp:10                               | `style` attribute used as URL data value — magic string with no documentation        |
| B06-8  | LOW      | manufacturers.jsp:1                            | Missing page-level comment                                                           |
| B06-9  | LOW      | manufacturers.jsp:58/153                       | Undocumented `company_id` guard for access-control on edit/delete buttons            |
| B06-10 | LOW      | manufacturersList.jsp:1                        | Missing page-level comment on a non-obvious JSON response fragment                   |
| B06-11 | MEDIUM   | manufacturersList.jsp:8                        | Cryptic session attribute key `"json"` with no documentation of producer or content  |
| B06-12 | LOW      | profile.jsp:1                                  | Missing page-level comment                                                           |
| B06-13 | LOW      | profile.jsp:110                                | Undocumented `userSmsAlertExisting` request attribute; null emits as truthy string   |
| B06-14 | MEDIUM   | profile.jsp:147-150                            | `$('#pword').strength()` targets non-existent element — silent no-op, no comment     |
| B06-15 | LOW      | settings.jsp:1                                 | Missing page-level comment                                                           |
| B06-16 | LOW      | settings.jsp:5-6                               | Undocumented session attribute keys `"sessDateTimeFormat"` and `"timezoneId"`        |
| B06-17 | LOW      | settings.jsp:71                                | Undocumented `isSuperAdmin` access-control gate — no comment on the role distinction |
| B06-18 | LOW      | subscription.jsp:1                             | Missing page-level comment                                                           |
| B06-19 | MEDIUM   | subscription.jsp:5-12                          | Scriptlet declares 5 variables (including Calendar/timestamp) all of which go unused |
| B06-20 | LOW      | subscription.jsp:39,76                         | Non-functional "Delete" text placeholders with no comment or click handler           |
| B06-21 | LOW      | users/general.jsp:1                            | Missing page-level comment                                                           |
| B06-22 | MEDIUM   | users/general.jsp:4-28                         | Multi-branch scriptlet with `newDriverId` attribute removal — no explanatory comment |
| B06-23 | LOW      | users/general.jsp:190-191                      | Client-side MD5 password hashing with no comment on design rationale or security     |
