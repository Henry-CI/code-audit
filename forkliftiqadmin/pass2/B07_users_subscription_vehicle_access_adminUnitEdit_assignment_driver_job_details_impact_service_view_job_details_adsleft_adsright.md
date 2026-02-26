# B07 Pass 2 Audit — JSP View-Layer Test Coverage
**Audit Agent:** B07
**Date:** 2026-02-26
**Scope:** JSP view files (users + vehicle subdirectories, includes)
**Test directory:** `src/test/java/`

---

## 1. Reading Evidence

### 1.1 `users/subscription.jsp`

**Purpose:** Driver notification-subscription management modal. Renders three toggle checkboxes (Red Impact Email, Red Impact SMS, Training Expiry Email) and submits to `admindriveredit.do`.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 3–7 | Reads `driverId` request parameter; builds `generalUrl` and `subscriptionUrl` strings by concatenating the raw parameter directly into URLs. `Long.valueOf(request.getParameter("driverId"))` — if `driverId` is present but non-numeric this throws `NumberFormatException`. |

**EL / Struts bean expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:notEmpty name="redImpactAlert" property="alert_id">` | request-scoped `redImpactAlert` bean | populated by action |
| `<logic:notEmpty name="redImpactSMSAlert" …>` | request-scoped `redImpactSMSAlert` bean | |
| `<logic:notEmpty name="driverDenyAlert" …>` | request-scoped `driverDenyAlert` bean | |
| `<html:hidden property="id" name="driver"/>` | `driver` bean, `id` property | |
| `<html:hidden property="mobile" name="driver"/>` | `driver` bean, `mobile` property | |

**Forms:**

| Form / Element | Action URL | Method |
|----------------|-----------|--------|
| `html:form` id=`adminDriverUpdateSubscription` | `admindriveredit.do` | POST |

**No EL `${}` expressions present.** Uses Struts 1 custom tags only.

---

### 1.2 `vehicle/access.jsp`

**Purpose:** Vehicle (unit) access-control settings tab. Allows editing of `accessible`, `access_type`, `access_id`, `keypad_reader`, and `facility_code` fields. Tab strip includes dealer-only "Assignment" tab guarded by `isDealer` session attribute.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 3–12 | Reads `id` from request parameter; builds `urlGeneral` by string concatenation of the raw `id` value into the URL. No encoding. |

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:equal value="true" name="isDealer">` | session-scoped `isDealer` | controls tab count display |
| `<html:checkbox … property="accessible">` | `adminUnitAccessForm` | bound to Struts form |
| `<html:select … property="access_type">` | `adminUnitAccessForm` | |
| `<html:text … property="access_id">` | `adminUnitAccessForm` | |
| `<html:select … property="keypad_reader">` | `adminUnitAccessForm` | |
| `<html:text … property="facility_code">` | `adminUnitAccessForm` | |

**Forms:**

| Form / Element | Action URL | Method |
|----------------|-----------|--------|
| `html:form` id=`adminUnitEditFormAccess` | `adminunitaccess.do` | POST |

---

### 1.3 `vehicle/adminUnitEdit.jsp`

**Purpose:** Vehicle general information editor (General tab). Edits name, serial number, manufacturer, type, power/fuel type, capacity, expansion module, and MAC address. Contains inline JavaScript real-time AJAX validation for duplicate name/serial/MAC via three separate `.do` endpoints.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 2–25 | Reads `action` and `equipId` request parameters; builds tab-strip URLs by concatenating raw `id` value. Reads `request.getAttribute("newId")` with a cast to `Integer`. |
| 170–172 | Three `<input type="hidden">` tags emit `id`, `newId`, and `actionUnit` values directly via `<%=id %>`, `<%=newUnitId %>`, `<%=action %>` without HTML encoding. |

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:equal value="true" name="isDealer">` | session-scoped `isDealer` | tab-count guard |
| `<logic:notEmpty name="arrAdminUnit">` | request-scoped list | |
| `<logic:iterate name="arrAdminUnit" id="unitRecord" type="com.bean.UnitBean">` | | |
| `<html:text property="name" name="unitRecord">` | UnitBean | |
| `<html:text property="serial_no" name="unitRecord">` | UnitBean | |
| `<html:select property="manu_id" name="unitRecord">` | UnitBean | |
| `<html:select property="type_id" name="unitRecord">` | UnitBean | |
| `<html:select property="fuel_type_id" name="unitRecord">` | UnitBean | |
| `<html:text property="mac_address" name="unitRecord">` | UnitBean | |
| `<html:hidden property="id" name="unitRecord">` | UnitBean | |

**Forms:**

| Form / Element | Action URL | Method |
|----------------|-----------|--------|
| `html:form` id=`adminUnitEditFormGeneral` | `adminunitedit.do` | POST |

**JavaScript AJAX validation (lines 253–291):**
- `unitnameexists.do?op_code=unitnameexists&name=` + raw field value (no encoding)
- `serialnoexists.do?op_code=serialnoexists&serial_no=` + raw field value (no encoding)
- `macaddressexists.do?op_code=macaddressexists&mac_address=` + raw field value (no encoding)
- All three use `async: false` (synchronous XHR — deprecated API)

---

### 1.4 `vehicle/assignment.jsp`

**Purpose:** Vehicle-to-company assignment management tab. Allows selecting a company and date range to assign a vehicle, and displays existing assignments in a table with delete controls.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 4–7 | Reads `sessDateFormat` from session **without null check**; calls `.replaceAll()` on the result. Reads `equipId` request parameter; builds `urlGeneral` by string concatenation. |
| 72–73 | Two `<input type="hidden">` tags emit `unit_id` and `action` directly via `<%=id %>`. |
| 132–134 | JavaScript AJAX URL built from `$('input[name=unit_id]').val()` plus datepicker values — query string constructed client-side. |

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<html:optionsCollection name="arrCompanies" value="id" label="name">` | request-scoped `arrCompanies` | |
| `<logic:notEmpty name="arrAssignments">` | request-scoped `arrAssignments` | |
| `<logic:iterate name="arrAssignments" id="assignment" type="com.bean.UnitAssignmentBean">` | | |
| `<bean:write property="company_name" name="assignment">` | UnitAssignmentBean | default filter=true (HTML-escaped) |
| `<bean:write property="start" name="assignment">` | UnitAssignmentBean | |
| `<bean:write property="end" name="assignment">` | UnitAssignmentBean | |
| `<bean:write property="current" name="assignment">` | UnitAssignmentBean | |
| `<bean:write property="id" name="assignment">` | UnitAssignmentBean | emitted in data-attribute |

**Forms:**

| Form / Element | Action URL | Method |
|----------------|-----------|--------|
| `html:form` id=`adminUnitAssignForm` | `adminunitassign.do` | POST |

---

### 1.5 `vehicle/driver_job_details.jsp`

**Purpose:** Driver-job assignment dialog. Lets an admin select a driver from a dropdown, set start/end times, and write instructions; submits to `driverjobreq.do`. Rendered inside a Bootstrap modal.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 2–6 | Reads `action`, `equipId`, `job_id` from request parameters (unused in HTML body beyond hidden fields). |
| 47–53 | Four `<html:hidden>` tags; `jobId` and `equipId` are set from `<%=jobId %>` / `<%=id %>` via scriptlet. |

**EL / Struts tag expressions:**

| Tag / Element | Bean / Attribute | Notes |
|---------------|-----------------|-------|
| `<html:select property="driverId" …>` | `driverJobDetailsActionForm` | |
| `<html:options collection="arrDrivers" property="id" labelProperty="first_last">` | request-scoped `arrDrivers` | |
| `<html:text property="startTime" …>` | | |
| `<html:text property="endTime" …>` | | |
| `<html:textarea property="instruct" …>` | | |

**Forms:**

| Form / Element | Action URL | Method |
|----------------|-----------|--------|
| Unnamed Struts form | `driverjobreq.do` | POST (class `assign_driver`) |

**Dead code present:** `fnsubmitAccount()` function (lines 85–106) references `adminRegActionForm` — a completely different form — and is never called from this page. Fields `fromTime`, `toTime` are in commented-out HTML.

---

### 1.6 `vehicle/impact.jsp`

**Purpose:** Vehicle sensor calibration display tab. Shows G-force thresholds table when calibration is at 100%, or a progress bar during calibration. Allows resetting calibration via a form.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 1–3 | Imports `ImpactBean`, `ImpactUtil`, `ImpactLevel` from application packages. |
| 7–11 | Reads `equipId` request parameter; reads `isDealer` from session **without null check** — calls `.equals("true")` directly, which will throw `NullPointerException` if session attribute is absent. Casts `request.getAttribute("impactBean")` to `ImpactBean` without null guard. |
| 39 | Emits `isDealer ? "five" : "four"` inline in class attribute — computed at scriptlet level. |
| 71 | `impact.calculateGForceRequiredForImpact(impactLevel)` — `impact` will be null if `impactBean` was not set by action, causing NPE at render time. |
| 85 | `<input type="hidden" name=equipId value="<%=id %>">` — missing quotes around attribute name `equipId` and missing HTML encoding on value. |

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:equal value="true" name="isDealer">` | session-scoped `isDealer` | |
| `<bean:write name="impactBean" property="percentage"/>` | request-scoped `impactBean` | used inline in CSS `content:` property and progress bar `style` |
| `<logic:equal name="impactBean" property="percentage" value="100.0">` | | |
| `<logic:iterate id="impactLevel" collection="<%= ImpactLevel.values() %>" …>` | static enum | scriptlet inside tag attribute |

**Forms:**

| Form / Element | Action URL | Method |
|----------------|-----------|--------|
| `html:form` id=`adminUnitEditImpact` | `adminunitimpact.do` | POST |

---

### 1.7 `vehicle/service.jsp`

**Purpose:** Vehicle service schedule settings tab. Displays service status (read-only), allows setting accumulated hours, service type (By Set Hours / By Interval), last service, next service due, and interval duration.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 3–12 | Reads `action` and `equipId` request parameters; builds `urlGeneral` by string concatenation of raw `id`. |
| 181 | `<input type="hidden" name="oldId" id="oldId" value="<%=id %>">` — raw parameter value emitted without HTML encoding. |

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:equal value="true" name="isDealer">` | session-scoped `isDealer` | tab-count guard |
| `<bean:write name="serviceBean" property="servStatus"/>` | request-scoped `serviceBean` | default filter=true (HTML-escaped) |
| `<bean:write name="serviceBean" property="hoursTillNextService"/>` | serviceBean | |
| `<html:text property="accHours" name="serviceBean"/>` | serviceBean | |
| `<html:text property="servLast" name="serviceBean"/>` | serviceBean | |
| `<html:text property="servNext" name="serviceBean"/>` | serviceBean | |
| `<html:text property="servDuration" name="serviceBean"/>` | serviceBean | |

**Forms:**

| Form / Element | Action URL | Method |
|----------------|-----------|--------|
| `html:form` id=`adminUnitEditFormService` | `adminunitservice.do` | POST |

---

### 1.8 `vehicle/view_job_details.jsp`

**Purpose:** Read-only job details list view rendered in a modal panel. Iterates over `arrJobDetails` and displays driver name, job number, status (1=Start, 2=Complete, 3=Pause), start/end times, and duration.

**Key scriptlets and line numbers:**

None. This file contains no scriptlet (`<% %>`) blocks.

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:notEmpty name="arrJobDetails">` | request-scoped `arrJobDetails` | |
| `<logic:iterate name="arrJobDetails" id="jobDetails" type="com.bean.JobDetailsBean">` | | |
| `<bean:write name="jobDetails" property="driverName"/>` | JobDetailsBean | default filter=true |
| `<bean:write name="jobDetails" property="jobNo"/>` | JobDetailsBean | |
| `<bean:write name="jobDetails" property="status"/>` | JobDetailsBean | |
| `<bean:write name="jobDetails" property="startTime"/>` | JobDetailsBean | |
| `<bean:write name="jobDetails" property="endTime"/>` | JobDetailsBean | |
| `<bean:write name="jobDetails" property="duration"/>` | JobDetailsBean | |

**Forms:** None.

---

### 1.9 `includes/adsleft.inc.jsp`

**Purpose:** Left-sidebar advertisement include fragment. Iterates the first three records from the session-scoped `sessAds` list and renders each ad image and text.

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 11 | `<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord"/>">` — image `src` is a mix of a compiled-in constant (`"images/"`) and a bean-written `pic` value. The `bean:write` tag uses default `filter=true`, but a relative path is used for `RuntimeConf.IMG_SRC`. |

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:notEmpty name="sessAds">` | session-scoped `sessAds` | |
| `<logic:iterate name="sessAds" id="adsRecord" type="com.bean.AdvertisementBean" length="3">` | | first 3 ads |
| `<bean:write property="pic" name="adsRecord"/>` | AdvertisementBean | default filter=true |
| `<bean:write property="text" name="adsRecord"/>` | AdvertisementBean | default filter=true |

**Forms:** None.

---

### 1.10 `includes/adsright.inc.jsp`

**Purpose:** Right-sidebar advertisement include fragment. Identical in structure to `adsleft.inc.jsp` but iterates records 4–6 (`offset="3"`).

**Key scriptlets and line numbers:**

| Lines | Code |
|-------|------|
| 10 | Same `<%=RuntimeConf.IMG_SRC%>` + `<bean:write property="pic" …>` pattern as adsleft. |

**EL / Struts tag expressions:**

| Tag | Bean / Attribute | Notes |
|-----|-----------------|-------|
| `<logic:notEmpty name="sessAds">` | session-scoped `sessAds` | |
| `<logic:iterate name="sessAds" id="adsRecord" … length="3" offset="3">` | | records 4–6 |
| `<bean:write property="pic" name="adsRecord"/>` | AdvertisementBean | default filter=true |
| `<bean:write property="text" name="adsRecord"/>` | AdvertisementBean | default filter=true |

**Forms:** None.

---

## 2. Test Directory Search Results

**Test directory:** `src/test/java/`

Files present in the test directory:

```
com/calibration/UnitCalibrationImpactFilterTest.java
com/calibration/UnitCalibrationTest.java
com/calibration/UnitCalibratorTest.java
com/util/ImpactUtilTest.java
```

Search results for JSP names and their backing action classes:

| Search term | Match in test directory |
|-------------|------------------------|
| `subscription` | None |
| `admindriveredit` / `AdminDriverEdit` | None |
| `adminunitaccess` / `AdminUnitAccess` | None |
| `adminunitedit` / `AdminUnitEdit` | None |
| `adminunitassign` / `AdminUnitAssign` | None |
| `driverjobreq` / `DriverJobDetails` | None |
| `adminunitimpact` / `AdminUnitImpact` | None (only ImpactUtil utility-class tests present) |
| `adminunitservice` / `AdminUnitService` | None |
| `view_job_details` / `ViewJobDetails` | None |
| `adsleft` / `adsright` / `Advertisement` | None |

**Conclusion:** Zero test coverage exists for all ten JSP files and their backing Action classes. The four existing tests cover utility/calibration classes only.

---

## 3. Findings

---

### B07-1
**Severity:** CRITICAL
**File:** `vehicle/impact.jsp`, line 9
**Title:** Unguarded session attribute dereference — guaranteed NullPointerException

```java
boolean isDealer = session.getAttribute("isDealer").equals("true");
```

`session.getAttribute("isDealer")` returns `null` if the attribute is not set (expired session, partial login, or direct URL access). Calling `.equals()` on `null` throws `NullPointerException`, causing a 500 error and a potential information-disclosure stack trace. Because the only session guard in `PreFlightActionServlet` checks `sessCompId` — not `isDealer` — a user with a valid but stripped session can trigger this reliably.

---

### B07-2
**Severity:** CRITICAL
**File:** `vehicle/impact.jsp`, line 71
**Title:** Null dereference on unguarded `impactBean` cast — server crash

```java
ImpactBean impact = (ImpactBean) request.getAttribute("impactBean");
// ...
<%= String.format("%.1fg", impact.calculateGForceRequiredForImpact(impactLevel)) %>
```

`impact` is assigned from `request.getAttribute("impactBean")` without a null check. The dereference `impact.calculateGForceRequiredForImpact(...)` at line 71 is reached only when `impactBean.percentage == 100.0` (line 56 logic branch), but if the action failed to set the attribute the cast itself succeeds (returning null) and the subsequent method call throws `NullPointerException`. An attacker who can reach this page without a valid unit or in an error state can trigger repeated 500 responses.

---

### B07-3
**Severity:** HIGH
**File:** `vehicle/assignment.jsp`, line 4
**Title:** Unguarded session attribute dereference — NullPointerException on `sessDateFormat`

```java
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```

`session.getAttribute("sessDateFormat")` is dereferenced without a null check. If the attribute has not been populated (e.g., session attribute was never set, or the session was partially initialised), this will throw `NullPointerException` at page render time before any HTML is output. Unlike `isDealer`, there is no Struts-logic tag that could absorb the error.

---

### B07-4
**Severity:** HIGH
**File:** `vehicle/adminUnitEdit.jsp`, lines 253–268
**Title:** Unencoded user input in client-side AJAX URLs — reflected XSS vector

```javascript
isSerialExists = wsValidation('serialnoexists.do?op_code=serialnoexists&serial_no=' + $('input[name=serial_no]').val(), 'serial_no_already_exists');
isNameExists = wsValidation('unitnameexists.do?op_code=unitnameexists&name=' + $('input[name=name]').val(), 'name_already_exists');
isMacAddrExists = wsValidation('macaddressexists.do?op_code=macaddressexists&mac_address=' + $('input[name=mac_address]').val(), 'mac_address_already_exists');
```

The raw text-field value is concatenated directly into AJAX URL strings without `encodeURIComponent()`. If a server-side validation endpoint returns the submitted value inside an HTML response (or if JavaScript string concatenation is used to inject content), this creates a reflected-XSS pathway. At minimum, an attacker who can influence the field value can inject arbitrary query parameters into these requests.

---

### B07-5
**Severity:** HIGH
**File:** `vehicle/impact.jsp`, line 85
**Title:** Missing quotes on HTML attribute and unencoded `equipId` parameter value

```html
<input type="hidden" name=equipId value="<%=id %>">
```

The `name` attribute is unquoted (`name=equipId`), which is non-conformant HTML and may be misinterpreted by some parsers. More critically, `<%=id %>` is the raw value of the `equipId` request parameter concatenated directly into the HTML attribute value without `ESAPI.encodeForHTMLAttribute()` or equivalent encoding. A crafted `equipId` such as `1" onmouseover="alert(1)` would inject a DOM event handler attribute, constituting a stored/reflected XSS.

---

### B07-6
**Severity:** HIGH
**File:** `users/subscription.jsp`, lines 4–6
**Title:** Request parameter concatenated into navigation URLs without encoding — reflected XSS

```java
Long id = request.getParameter("driverId") == null ? 0 : Long.valueOf(request.getParameter("driverId"));
String generalUrl = "admindriver.do?action=" + (id == null ? "adduser" : "edituser&driverId=" + id);
String subscriptionUrl = "admindriver.do?action=subscription&driverId=" + id;
```

`id` is a `Long` cast from the raw `driverId` parameter. Because `Long.valueOf()` throws `NumberFormatException` on non-numeric input rather than returning null, the ternary `id == null ? "adduser" : "edituser&driverId=" + id` will always evaluate the non-null branch — but only if the parse succeeded. If the parameter is engineered to bypass this (e.g., via a numeric value that contains XSS when rendered), the resulting URL string is inserted directly into two anchor `href` attributes (lines 11–12):

```jsp
<li><a class="triggerThis" href="<%=generalUrl%>">General</a></li>
<li><a class="active" href="<%=subscriptionUrl%>">Notification</a></li>
```

The `Long` parse does prevent the most obvious `javascript:` injection, but the URL is emitted without HTML-attribute encoding, making it vulnerable to attribute-level HTML injection if `Long.toString()` is somehow bypassed (e.g., a future refactor that loosens the type).

---

### B07-7
**Severity:** HIGH
**File:** `vehicle/access.jsp`, `vehicle/service.jsp`, `vehicle/adminUnitEdit.jsp`, `vehicle/assignment.jsp`, `vehicle/impact.jsp`
**Title:** Raw request parameter `id`/`equipId` emitted into HTML attributes and hidden fields without encoding — reflected XSS

Multiple files emit the raw `id` or `equipId` request parameter directly into HTML `href` attributes and `<input type="hidden" value="...">` fields using scriptlet output (`<%=id %>`), with no call to `ESAPI.encodeForHTMLAttribute()`, `StringEscapeUtils.escapeHtml()`, or equivalent:

- `access.jsp` lines 18–22, 27–31: `<%=id %>` in anchor `href`s
- `service.jsp` lines 17–21, 25–29, 181: `<%=id %>` in anchor `href`s and hidden input
- `adminUnitEdit.jsp` lines 29–43, 170–172: `<%=id %>`, `<%=action %>`, `<%=newUnitId %>` in hrefs and hidden inputs
- `assignment.jsp` lines 14–19, 72: `<%=id %>` in anchor `href`s and hidden input
- `impact.jsp` lines 40–46, 85: `<%=id %>` in anchor `href`s and hidden input

An attacker who can control these parameters (e.g., via a malicious link) can inject arbitrary HTML attributes or close the tag and inject script.

---

### B07-8
**Severity:** HIGH
**File:** `vehicle/driver_job_details.jsp`, lines 85–106
**Title:** Dead code contains password-handling logic from a different form

```javascript
function fnsubmitAccount() {
    var pass = document.adminRegActionForm.pin.value;
    var cpassword = document.adminRegActionForm.cpassword.value;
    // ...
}
```

This function references `adminRegActionForm` — a completely different form that does not exist in this page. It performs client-side password comparison before calling `document.adminRegActionForm.submit()`. This is dead code that was copied from a registration page and never cleaned up. Its presence:

1. Confuses code readers about the actual authorization boundaries of this page.
2. If `adminRegActionForm` were ever added to the same page (e.g., during a future refactor), the function would silently submit a registration form from a job-details modal, bypassing expected controls.
3. Represents untestable logic stranded in a view file.

---

### B07-9
**Severity:** HIGH
**File:** `vehicle/impact.jsp`, lines 27–28 (CSS `content` property)
**Title:** Unencoded bean property emitted inside CSS `content:` pseudo-element — CSS injection

```jsp
.progress:after {
    content: "<bean:write name="impactBean" property="percentage" />%";
```

`bean:write` with default `filter=true` applies HTML entity encoding, which replaces `<`, `>`, `"`, `&`. However, CSS string context requires CSS encoding, not HTML encoding. Characters such as `\`, `;`, `}`, and Unicode escape sequences (`\A`) are not filtered by the default Struts `bean:write` tag. If the `percentage` value originates from user-supplied or device-supplied data, a value such as `\A}body{background:url(//evil.com/)}` would break out of the CSS string and inject arbitrary CSS rules. The `percentage` property is a float derived from sensor data (calibration), so exploitation is constrained but not impossible.

---

### B07-10
**Severity:** MEDIUM
**File:** `vehicle/driver_job_details.jsp`, line 112
**Title:** DOM manipulation reads from potentially wrong selector — data integrity defect

```javascript
$("#drivrId").val($("#name option:selected").val());
```

The element ID is `drivrId` (missing the letter 'e'), but the hidden input is declared as `styleId="driverId"` (line 53). This means the JavaScript `fnAssign()` function silently fails to populate the driver ID hidden field before form submission. The server would receive an empty or stale `driverId` value, causing incorrect assignment without any error feedback. This is an untestable view-layer logic defect — no unit test in the current test suite can detect it.

---

### B07-11
**Severity:** MEDIUM
**File:** `vehicle/adminUnitEdit.jsp`, lines 276–291
**Title:** Synchronous XHR (`async: false`) in three validation functions

```javascript
jQuery.ajax({ url: url, success: function(result) { ... }, async: false });
```

All three AJAX validation calls (`wsValidation`) use `async: false`, which blocks the browser's UI thread. This is deprecated in all modern browsers and will generate console warnings. More importantly from a quality perspective, this pattern is inherently untestable with standard JavaScript testing frameworks and cannot be mocked without special handling. It also creates a denial-of-service vector: if the validation endpoints are slow or unresponsive, the entire browser tab freezes for all users concurrently editing.

---

### B07-12
**Severity:** MEDIUM
**File:** `vehicle/assignment.jsp`, lines 131–147
**Title:** Server error message echoed into DOM unencoded — potential reflected XSS

```javascript
success: function (result) {
    if (result != "true") {
        errorOutput.text(result);
```

The AJAX response from `assigndatesvalid.do` is placed into the DOM via jQuery's `.text()` method, which safely HTML-encodes content. This is not currently exploitable for XSS because `.text()` is used rather than `.html()`. However, if the endpoint returns data in any other format or a future change switches this to `.html()`, it becomes immediately exploitable. The concern is that there is no test verifying this boundary, and the server-side response is fully trust-implicit.

---

### B07-13
**Severity:** MEDIUM
**File:** `includes/adsleft.inc.jsp` and `includes/adsright.inc.jsp`, lines 11 and 10 respectively
**Title:** Ad image `src` constructed from database-sourced path using relative `RuntimeConf.IMG_SRC`

```jsp
<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord"/>" alt=""/>
```

`RuntimeConf.IMG_SRC` is the literal string `"images/"` (relative path). The `pic` property is HTML-encoded by `bean:write` (default filter=true), which prevents `<script>` injection but does not prevent path traversal in the URL path portion (e.g., `../admin/sensitive`). An attacker with access to insert advertisement records could supply a `pic` value like `../../WEB-INF/web.xml` or a `javascript:` scheme. While most browsers do not execute `javascript:` in `img src`, the path traversal could expose internal resources or cause unexpected cross-origin requests.

---

### B07-14
**Severity:** MEDIUM
**File:** `vehicle/driver_job_details.jsp`
**Title:** Form submits without CSRF token

The `assign_driver` form posts to `driverjobreq.do` with no anti-CSRF token field. The session auth check in `PreFlightActionServlet` verifies `sessCompId` is present but does not validate a synchronizer token. An attacker who can trick an authenticated admin into visiting a malicious page can submit a forged driver assignment for any `job_id` and `equipId` visible in a URL.

---

### B07-15
**Severity:** MEDIUM
**File:** All vehicle/*.jsp and users/subscription.jsp
**Title:** No CSRF protection on any of the POST forms

None of the six POST forms across the audited files contain a CSRF synchronizer token:
- `admindriveredit.do` (subscription.jsp)
- `adminunitaccess.do` (access.jsp)
- `adminunitedit.do` (adminUnitEdit.jsp)
- `adminunitassign.do` (assignment.jsp)
- `adminunitservice.do` (service.jsp)
- `adminunitimpact.do` (impact.jsp)

`web.xml` declares no CSRF filter. `PreFlightActionServlet` does not implement token validation. Cross-site request forgery is possible against all these admin endpoints for any authenticated session.

---

### B07-16
**Severity:** MEDIUM
**File:** `users/subscription.jsp`, line 4
**Title:** `NumberFormatException` on non-numeric `driverId` parameter

```java
Long id = request.getParameter("driverId") == null ? 0 : Long.valueOf(request.getParameter("driverId"));
```

When `driverId` is present but not numeric (e.g., `?driverId=abc`), `Long.valueOf()` throws an uncaught `NumberFormatException`. The global exception handler in `web.xml` redirects to `/error/error.html`, but this is a recoverable input validation error that should be handled gracefully rather than surfaced as a 500. The absence of input validation here is also untestable at the view layer.

---

### B07-17
**Severity:** LOW
**File:** `vehicle/driver_job_details.jsp`, lines 66–70
**Title:** JavaScript placeholder assignment references undefined element IDs

```javascript
$("#fromTime").attr('placeholder', 'From Time')
$("#toTime").attr('placeholder', 'To Time')
```

The corresponding `fromTime` and `toTime` form fields are commented out in the HTML (lines 29–35). The jQuery selectors silently no-op because the elements do not exist. This is harmless but indicative of dead code that was not cleaned up when features were disabled.

---

### B07-18
**Severity:** LOW
**File:** `includes/adsleft.inc.jsp` and `includes/adsright.inc.jsp`
**Title:** Advertisement text rendered with `bean:write` default filter — HTML entities displayed literally in raw-HTML-intended fields

`<bean:write property="text" name="adsRecord" />` with default `filter=true` HTML-encodes the output. If ad text is intended to include formatting HTML (e.g., `<b>Sale</b>`), those tags will be displayed as literal text. If the text is plain-text only, this is correct. There is no documentation or enforcement of this constraint, and no test that verifies ad text is stored/retrieved as plain text.

---

### B07-19
**Severity:** INFO
**File:** All ten files
**Title:** Zero test coverage — no JSP rendering tests, no action integration tests

The test directory contains four files, all of which test calibration/utility classes. No test covers:
- Action classes backing these JSPs (`AdminDriverEditAction`, `AdminUnitAccessAction`, `AdminUnitEditAction`, `AdminUnitAssignAction`, `DriverJobDetailsAction`, `AdminUnitImpactAction`, `AdminUnitServiceAction`)
- Form validation logic in corresponding `ActionForm` classes
- Session/request attribute population paths that JSPs depend on
- JavaScript behaviour (AJAX validation, date-picker, modal interaction)

Because all business logic in JSP scriptlets is interleaved with rendering, it is structurally untestable with JUnit alone.

---

### B07-20
**Severity:** INFO
**File:** `vehicle/impact.jsp`, lines 67–79
**Title:** Business logic (G-force threshold calculation) performed in JSP scriptlet

```jsp
<%= String.format("%.1fg", impact.calculateGForceRequiredForImpact(impactLevel)) %>
```

The display formatting logic (which level triggers what G-force) is computed in a scriptlet loop inside the view, not in the Action or a display-bean. This makes the presentation logic untestable without a running servlet container, and couples the view to the `ImpactBean` API directly.

---

### B07-21
**Severity:** INFO
**File:** `vehicle/adminUnitEdit.jsp`, lines 127–136
**Title:** Conditional field rendering based on property value comparison done in view

```jsp
<logic:equal name="unitRecord" property="size" value="0.0">
    <html:text property="size" … value="" …/>
</logic:equal>
<logic:notEqual name="unitRecord" property="size" value="0.0">
    <html:text property="size" …/>
</logic:notEqual>
```

The decision to blank the `size` field when it equals 0.0 is presentation logic embedded in the JSP. It cannot be unit-tested and could be inadvertently broken by a change to the default value in `UnitBean`.

---

## 4. Summary Table

| ID | Severity | File | Title |
|----|----------|------|-------|
| B07-1 | CRITICAL | `vehicle/impact.jsp:9` | Unguarded `isDealer` session attribute dereference — NPE |
| B07-2 | CRITICAL | `vehicle/impact.jsp:71` | Null dereference on `impactBean` — NPE at render |
| B07-3 | HIGH | `vehicle/assignment.jsp:4` | Unguarded `sessDateFormat` session attribute — NPE |
| B07-4 | HIGH | `vehicle/adminUnitEdit.jsp:253–268` | Unencoded user input in client-side AJAX URLs — XSS vector |
| B07-5 | HIGH | `vehicle/impact.jsp:85` | Unquoted attribute and unencoded `equipId` — XSS |
| B07-6 | HIGH | `users/subscription.jsp:4–12` | Request parameter concatenated into hrefs without encoding |
| B07-7 | HIGH | Multiple vehicle JSPs | Raw `id`/`equipId` emitted into HTML attributes without encoding — reflected XSS |
| B07-8 | HIGH | `vehicle/driver_job_details.jsp:85–106` | Dead code contains password-handling logic from different form |
| B07-9 | HIGH | `vehicle/impact.jsp:27–28` | Unencoded `percentage` in CSS `content:` — CSS injection |
| B07-10 | MEDIUM | `vehicle/driver_job_details.jsp:112` | Typo in element ID (`drivrId`) silently drops driver ID on submit |
| B07-11 | MEDIUM | `vehicle/adminUnitEdit.jsp:276–291` | Synchronous XHR (`async: false`) — untestable, browser freeze risk |
| B07-12 | MEDIUM | `vehicle/assignment.jsp:131–147` | Server error echoed into DOM — trust-implicit, `.text()` currently safe |
| B07-13 | MEDIUM | `includes/adsleft.inc.jsp`, `adsright.inc.jsp` | Ad image `src` path from DB — path traversal risk |
| B07-14 | MEDIUM | `vehicle/driver_job_details.jsp` | No CSRF token on assign form |
| B07-15 | MEDIUM | All six POST forms | No CSRF protection on any admin POST endpoint |
| B07-16 | MEDIUM | `users/subscription.jsp:4` | `NumberFormatException` on non-numeric `driverId` |
| B07-17 | LOW | `vehicle/driver_job_details.jsp:66–70` | JavaScript references commented-out element IDs |
| B07-18 | LOW | `includes/adsleft.inc.jsp`, `adsright.inc.jsp` | Ad text HTML-encoded — formatting intent undocumented |
| B07-19 | INFO | All ten files | Zero test coverage for all JSPs and backing actions |
| B07-20 | INFO | `vehicle/impact.jsp:67–79` | Business logic in JSP scriptlet — untestable |
| B07-21 | INFO | `vehicle/adminUnitEdit.jsp:127–136` | Conditional rendering logic in view — untestable |
