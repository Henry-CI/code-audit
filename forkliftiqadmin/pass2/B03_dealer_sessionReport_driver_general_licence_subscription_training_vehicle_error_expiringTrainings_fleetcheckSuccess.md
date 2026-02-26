# Pass 2 — Test Coverage Audit: JSP View Layer
**Audit Run:** 2026-02-26-01
**Agent ID:** B03
**Date:** 2026-02-26
**Scope:** View-layer audit of 9 JSP files; no automated test coverage exists for any JSP in this project.

---

## 1. Reading Evidence

### 1.1 `dealer/sessionReport.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/sessionReport.jsp`
**Purpose:** Session report filter/results page for dealer users. Renders a search form and a table of session entries (vehicle, driver, start/end time) populated by `DealerSessionReportAction`.

**Key scriptlets and line numbers:**

| Lines | Content |
|-------|---------|
| 4–6   | Reads `session.getAttribute("sessDateFormat")`, calls `.replaceAll(...)` on the result without null-check, assigns to `dateFormat`. |
| 99–105 | Checks `request.getParameter("start_date") != null`; if present, calls `DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), ...)` and emits the result directly into JavaScript via `<%= ... %>`. |
| 107–113 | Same pattern for `request.getParameter("end_date")`. |
| 114–115 | Emits `<%= dateFormat %>` and `<%= dateFormat %>` unescaped into a JavaScript `setupDatePicker(...)` call. |

**Key EL expressions / session attributes accessed:**
- `session.getAttribute("sessDateFormat")` — lines 5, 102, 110
- `request.getParameter("start_date")` — lines 100, 102
- `request.getParameter("end_date")` — lines 108, 110

**Forms and action URLs:**
- `<html:form action="dealerSessionReport.do" method="POST">` — search filter form (line 21)

**Request attribute / bean usage:**
- `name="vehicles"` — `<html:optionsCollection>` (line 27)
- `name="drivers"` — `<html:optionsCollection>` (line 35)
- `name="sessionReport" property="sessions" id="sessionEntry" type="com.bean.SessionBean"` — `<logic:iterate>` (line 78–87)
- `<bean:write>` used for `unitName`, `driverName`, `startTime`, `finishTime` — all HTML-escaped by default via Struts `bean:write`

---

### 1.2 `driver/general.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/general.jsp`
**Purpose:** General driver information form (add/edit). Part of a tabbed modal. Handles both add and edit modes based on the `action` query parameter. Submitted to `admindriveradd.do` or `admindriveredit.do`.

**Key scriptlets and line numbers:**

| Lines | Content |
|-------|---------|
| 4–6   | Reads `action` and `id` from `request.getParameter(...)` with null-guards. |
| 14–26 | Branch on `action.equalsIgnoreCase("edit")` to set URL variables and op_code — business routing logic in view. |
| 28–31 | Checks `request.getAttribute("newDriverId")`, falls back for add-mode. |
| 33    | `session.getAttribute("sessTimezone")` — no null-check. |
| 35–38 | Business logic: determines tab label ("Training" vs "Licence") based on timezone. |
| 43–45 | Emits `<%=generalUrl%>`, `<%=trainingUrl%>`, `<%=vehicleUrl%>` directly into `href` attributes. |
| 48    | Emits `<%=actionCode %>` into `html:form action` attribute. |
| 135–137 | Hidden fields: `id`, `op_code`, `pass_hash` written into form. |
| 190–212 | JavaScript: client-side PIN validation; uses `CryptoJS.MD5(...)` to hash PIN and place it in `pass_hash` hidden field (line 205). |
| 210   | `console.log("valid:"+valid)` — debug statement left in production code. |
| 256   | `var actUrl = "<%=actionCode %>"` emitted unescaped into JavaScript. |

**Key EL expressions / session attributes accessed:**
- `session.getAttribute("sessTimezone")` — line 33

**Forms and action URLs:**
- `<html:form method="post" action="<%=actionCode %>"...>` — dynamically set to `admindriveradd.do` or `admindriveredit.do` (line 48)

---

### 1.3 `driver/licence.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/licence.jsp`
**Purpose:** The file exists on disk but is **completely empty** (0 bytes, 0 lines). It is referenced in the tab navigation of sibling driver JSPs when the timezone is non-US/Canada. It has no content whatsoever.

**Scriptlets:** None.
**EL expressions:** None.
**Forms:** None.

---

### 1.4 `driver/subscription.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/subscription.jsp`
**Purpose:** Driver alert subscription management tab. Displays four email address fields for alert notifications. Submitted to `admindriveredit.do` with `op_code=edit_subscription`.

**Key scriptlets and line numbers:**

| Lines | Content |
|-------|---------|
| 4     | `Long.valueOf(request.getParameter("driverId"))` — no null guard handled by ternary (null remains null), but non-numeric input throws `NumberFormatException`. |
| 5–8   | URL construction for tab navigation using `id` (which may be `null`). `trainingUrl`, `subscriptionUrl`, `vehicleUrl` will contain literal `"null"` strings if `id` is null. |
| 9     | `session.getAttribute("sessTimezone")` cast to `String` — no null-check. |
| 11–14 | Tab label business logic (Training vs Licence). |
| 19–21 | Emits `<%=generalUrl%>`, `<%=trainingUrl%>`, `<%=vehicleUrl%>` unescaped into `href` attributes. |

**Key EL expressions / session attributes accessed:**
- `session.getAttribute("sessTimezone")` — line 9
- `request.getParameter("driverId")` — line 4

**Forms and action URLs:**
- `<html:form method="post" action="admindriveredit.do"...>` — hardcoded (line 24)
- Hidden fields: `op_code` (value `edit_subscription`), `driver_id`

---

### 1.5 `driver/training.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/training.jsp`
**Purpose:** Driver training records tab. Lists existing trainings and allows adding/deleting them via AJAX calls to `trainings.do`.

**Key scriptlets and line numbers:**

| Lines | Content |
|-------|---------|
| 4     | `Long.valueOf(request.getParameter("driverId"))` — throws `NumberFormatException` on non-numeric input. |
| 5–8   | Tab URL construction; `id` may produce `"null"` in URLs. |
| 9     | `(String) session.getAttribute("sessDateFormat")).replaceAll(...)` — NPE if `sessDateFormat` is null. |
| 10    | `session.getAttribute("sessTimezone")` — no null-check. |
| 11–15 | Tab label business logic. |
| 21    | `<%=trainingUrl%>` in href. |
| 32    | `<%=trainingtab %>` emitted as panel heading text. |
| 112   | `<input type="hidden" id="driver-id" value="<bean:write name="driverId"/>"/>` — `driverId` bean written into an HTML attribute value. |
| 134, 138 | `<%=dateFormat%>` emitted into JavaScript `setupDatePicker(...)` call. |
| 141–158 | JavaScript `addTraining()` issues `$.post('trainings.do', ...)` — no CSRF token. |
| 162–168 | JavaScript `deleteTraining()` issues `$.get('trainings.do', ...)` using HTTP GET for a destructive operation. |

**Key EL expressions / session attributes accessed:**
- `session.getAttribute("sessDateFormat")` — line 9
- `session.getAttribute("sessTimezone")` — line 10

**Request attribute / bean usage:**
- `name="trainings"` — iterates `com.bean.DriverTrainingBean`
- `name="manufacturers"`, `name="types"`, `name="fuelTypes"` — select option data
- `name="driverId"` — used in hidden field at line 112

**Forms and action URLs:**
- `<html:form method="post" action="admindriveredit.do"...>` (line 25)
- AJAX: `$.post('trainings.do', ...)` and `$.get('trainings.do', ...)`

---

### 1.6 `driver/vehicle.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/vehicle.jsp`
**Purpose:** Driver vehicle assignment tab. Lists all vehicles for the company with checkboxes indicating whether each is assigned to this driver. Submitted to `admindriveredit.do` with `op_code=edit_vehicle`.

**Key scriptlets and line numbers:**

| Lines | Content |
|-------|---------|
| 4     | `Long.valueOf(request.getParameter("driverId"))` — same pattern as subscription/training. |
| 5–8   | Tab URL construction with potential `"null"` in URLs. |
| 9     | `session.getAttribute("sessTimezone")` — no null-check. |
| 11–14 | Tab label business logic. |
| 19–21 | Emits `<%=generalUrl%>`, `<%=trainingUrl%>`, `<%=vehicleUrl%>` into href. |

**Key EL expressions / session attributes accessed:**
- `session.getAttribute("sessTimezone")` — line 9
- `request.getParameter("driverId")` — line 4

**Request attribute / bean usage:**
- `name="driverVehicle" property="driverUnits" id="vehicle" type="com.bean.DriverUnitBean"` — iterate (line 48)
- `<bean:write>` for `name`, `location`, `department`, `trained`, `hours`

**Forms and action URLs:**
- `<html:form method="post" action="admindriveredit.do"...>` (line 24)
- Hidden fields: `op_code` (value `edit_vehicle`), `id`

---

### 1.7 `error.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/error.jsp`
**Purpose:** Generic error page fragment. Displays Struts action errors and a "Back" button that calls `history.back(-1)`.

**Key scriptlets and line numbers:**

| Lines | Content |
|-------|---------|
| 4     | Obtains a `Logger` instance via `InfoLogger.getLogger("com.error.html")`. |
| 5, 17–23 | Wraps the entire body in a try/catch that logs exceptions and re-throws as `new Exception(e.getMessage())` — wrapping discards original stack trace type. |

**Key EL expressions / session attributes accessed:** None.

**Forms and action URLs:** None (button triggers `history.back(-1)` via JavaScript).

---

### 1.8 `expiringTrainings.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/expiringTrainings.jsp`
**Purpose:** Dashboard widget showing drivers with trainings that are expired or expiring soon. Read-only display table.

**Key scriptlets and line numbers:**

| Lines | Content |
|-------|---------|
| 3     | `(String) session.getAttribute("sessTimezone")` — no null-check; NPE if attribute absent. |
| 5–8   | Tab label logic ("training" vs "licence"). |
| 19    | `<%=trainingtab %>` emitted directly into HTML text inside a `<div>`. |

**Key EL expressions / session attributes accessed:**
- `session.getAttribute("sessTimezone")` — line 3

**Request attribute / bean usage:**
- `name="arrExpiringTrainings" id="training" type="com.bean.DriverTrainingBean"` — iterated (line 36)
- `<bean:write>` for `first_name`, `last_name`, `email`, `unit_name`, `training_date`, `expiration_date`

**Forms and action URLs:** None. Read-only widget.

---

### 1.9 `fleetcheckSuccess.jsp`

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/fleetcheckSuccess.jsp`
**Purpose:** Success/completion page displayed after a fleetcheck is submitted. Shows a countdown timer (10 seconds) and then auto-redirects by submitting a hidden form targeting `goSerach.do`. Also provides a manual logout button.

**Key scriptlets and line numbers:** None.

**Key EL expressions / session attributes accessed:** None.

**Forms and action URLs:**
- `<form action="goSerach.do" method="post" name="searchForm">` — auto-submitted after countdown (line 9). Note: `goSerach` is a typo for `goSearch`; confirmed present in struts-config.xml at path `/goSerach`.
- `<form action="logout.do" method="post" name="logoutForm">` — manual logout (line 11)

**JavaScript:**
- Lines 21–45: Countdown timer using `setInterval`; calls `document.searchForm.submit()` when timer reaches 0.
- `document.onload = init()` — incorrect syntax; `init()` is called immediately at parse time rather than on the `load` event.

---

## 2. Test Coverage Grep Results

**Test directory:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

The test directory contains exactly four test files:
1. `com/calibration/UnitCalibrationImpactFilterTest.java`
2. `com/calibration/UnitCalibrationTest.java`
3. `com/calibration/UnitCalibratorTest.java`
4. `com/util/ImpactUtilTest.java`

Grep searches were performed for all of the following patterns across the test directory:

| Search Pattern | Result |
|----------------|--------|
| `sessionReport`, `dealerSessionReport`, `SessionReport` | No matches |
| `admindriver`, `AdminDriver`, `admindriveredit`, `admindriveradd` | No matches |
| `error.jsp`, `expiringTrainings`, `fleetcheckSuccess` | No matches |
| `trainings.do`, `TrainingsAction`, `ExpiringTraining` | No matches |
| `general`, `licence`, `subscription`, `training`, `vehicle`, `fleetcheck` | No matches |

**Conclusion:** Zero test coverage exists for any of the nine audited JSP files, their associated action classes (`DealerSessionReportAction`, `AdminDriverAddAction`, `AdminDriverEditAction`, `AdminTrainingsAction`), or the view-layer logic they contain. The four existing tests cover only calibration and impact utilities.

---

## 3. Findings

---

### B03-1
**Severity:** CRITICAL
**File:** `dealer/sessionReport.jsp`, lines 99–113
**Title:** Reflected XSS via `start_date` and `end_date` parameters injected into JavaScript

**Description:**
User-supplied query parameters `start_date` and `end_date` are passed through `DateUtil.stringToIsoNoTimezone(...)` and emitted without any HTML or JavaScript escaping directly inside a `<script>` block:

```java
// line 102
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>")
// line 110
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>")
```

`DateUtil.stringToIsoNoTimezone` returns `df.format(dateObj)` where `dateObj` may be `null` if parsing fails. When the date cannot be parsed, `df.format(null)` throws a `NullPointerException`, crashing the page. When the date is valid, the formatted string is inserted unescaped. An attacker crafting input that parses successfully yet contains JavaScript-special characters (or by influencing the format string path) can break out of the string literal. More critically, because parsing silently falls back to a fixed format and may return garbage strings, the degree of control depends on date-format handling. Even if direct script injection is constrained by the format, the output is **never escaped** before HTML emission into a `<script>` context. This is a textbook DOM/reflected XSS injection point.

The issue is untestable at the unit level because the logic is embedded in the view.

---

### B03-2
**Severity:** HIGH
**File:** `dealer/sessionReport.jsp`, line 5
**Title:** Unguarded `session.getAttribute("sessDateFormat")` — guaranteed NPE on session expiry or missing attribute

**Description:**
```java
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```
The cast result is immediately chained with `.replaceAll(...)` without a null check. If the session attribute `sessDateFormat` is absent (e.g., session has expired mid-flight, was never set, or was invalidated), a `NullPointerException` is thrown during JSP rendering, leaking a stack trace to the error page rather than a clean timeout redirect. The same attribute is read again at lines 102 and 110 within the inline scriptlet.

---

### B03-3
**Severity:** HIGH
**File:** `driver/general.jsp`, lines 205–206
**Title:** Client-side MD5 used as password hash before transmission

**Description:**
```javascript
var password = '' + CryptoJS.MD5($('input[name="pass"]').val());
$('input[name=pass_hash]').val(password);
```
The driver's PIN is MD5-hashed in the browser before form submission. MD5 is a broken cryptographic hash with no salt. This pattern provides no effective security:
1. An attacker with network access (or browser DevTools) sees the MD5 hash in the POST body; the hash *is* the credential.
2. MD5 hashes of 4–8 digit PINs are trivially reversed via rainbow tables or brute force.
3. The actual plaintext is also submitted in the `pass` field (both fields are present in the form), so the hash is redundant.

This is an untestable security concern because it lives entirely in client-side JavaScript within the JSP.

---

### B03-4
**Severity:** HIGH
**File:** `driver/training.jsp`, line 162
**Title:** Training deletion performed via HTTP GET — CSRF and idempotency violation

**Description:**
```javascript
function deleteTraining(event, id) {
    event.preventDefault();
    $.get('trainings.do', {action: 'delete', training: id})
```
Deleting a training record is a state-changing (destructive) operation but is issued as an HTTP GET request. HTTP GET must be idempotent and side-effect free (RFC 7231). Using GET for mutation:
1. Makes the delete operation susceptible to Cross-Site Request Forgery (CSRF) via `<img src="trainings.do?action=delete&training=X">` or similar, because browsers and proxies will follow GET URLs without user consent.
2. Allows deletion to be triggered by browser pre-fetch, link-crawlers, or history pre-loading.
3. No anti-CSRF token is present in either the GET or the POST AJAX calls (`addTraining`).

The application has no CSRF filter in `web.xml`.

---

### B03-5
**Severity:** HIGH
**File:** `driver/subscription.jsp` line 4, `driver/training.jsp` line 4, `driver/vehicle.jsp` line 4
**Title:** Unguarded `Long.valueOf()` on user-supplied `driverId` — denial-of-service via `NumberFormatException`

**Description:**
All three files contain:
```java
Long id = request.getParameter("driverId") == null ? null : Long.valueOf(request.getParameter("driverId"));
```
A null check guards against a missing parameter but not against a non-numeric value. Supplying `driverId=abc` causes `Long.valueOf("abc")` to throw `NumberFormatException` during JSP execution. Struts catches this and renders the generic error page, but it is an unhandled server-side exception observable from the browser. An unauthenticated attacker who reaches these pages (or a malicious authenticated user) can trivially trigger 500-series responses in a loop, constituting a denial-of-service vector against error-page rendering infrastructure.

---

### B03-6
**Severity:** HIGH
**File:** `driver/general.jsp`, lines 14–26, 33–38; `driver/subscription.jsp`, lines 9–14; `driver/training.jsp`, lines 9–15; `driver/vehicle.jsp`, lines 9–14; `expiringTrainings.jsp`, lines 3–8
**Title:** Business routing and locale-detection logic embedded in view scriptlets — untestable

**Description:**
Multiple JSPs contain non-trivial business logic that belongs in the Action class:

- **general.jsp (lines 14–26):** Determines `generalUrl`, `trainingUrl`, `subscriptionUrl`, `vehicleUrl`, `op_code`, and `actionCode` based on the `action` parameter. This is routing logic that duplicates what the action class should decide.
- **general.jsp / subscription.jsp / training.jsp / vehicle.jsp / expiringTrainings.jsp:** All independently implement the same timezone-to-tab-label mapping (`"Training"` vs `"Licence"` based on `US/` or `Canada/` timezone prefix) via copy-pasted scriptlet code. If the business rule changes, it must be updated in five places.

This logic cannot be unit-tested. It is only exercisable via integration tests that render the full JSP, which do not exist in this project.

---

### B03-7
**Severity:** MEDIUM
**File:** `driver/general.jsp`, line 33; `driver/subscription.jsp`, line 9; `driver/training.jsp`, line 10; `driver/vehicle.jsp`, line 9; `expiringTrainings.jsp`, line 3
**Title:** `session.getAttribute("sessTimezone")` cast without null-check in five files

**Description:**
All five files perform:
```java
String timezone = (String) session.getAttribute("sessTimezone");
// immediately followed by:
if(!timezone.contains("US/")&&!timezone.contains("Canada/"))
```
If `sessTimezone` is absent from the session (session expiry, misconfigured setup, or attribute removal), the cast succeeds but `timezone` is `null`, and the subsequent `.contains(...)` call throws a `NullPointerException`. This will produce an uncaught exception in the JSP rendering pipeline, resulting in an error page with potential stack trace leakage.

`DealerSessionReportAction` (the associated action class) correctly guards `sessCompId` with a null-check and throws a `RuntimeException` with a meaningful message; the JSPs do not apply the same discipline.

---

### B03-8
**Severity:** MEDIUM
**File:** `driver/training.jsp`, line 9
**Title:** Chained method call on unchecked `session.getAttribute("sessDateFormat")` — NPE risk

**Description:**
```java
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```
Identical to the pattern in `dealer/sessionReport.jsp` (B03-2). If `sessDateFormat` is null, a `NullPointerException` is thrown immediately during JSP compilation of the scriptlet. This silently breaks the entire training tab rendering.

---

### B03-9
**Severity:** MEDIUM
**File:** `driver/subscription.jsp`, lines 5–8; `driver/training.jsp`, lines 5–8; `driver/vehicle.jsp`, lines 5–8
**Title:** Tab navigation URLs contain literal `"null"` string when `driverId` is absent

**Description:**
When `request.getParameter("driverId")` is null, the variable `id` is set to `null` (Java `Long`). URL construction then produces:
```java
String trainingUrl = "admindriver.do?action=training&driverId=" + id;
// results in: "admindriver.do?action=training&driverId=null"
```
This emits `driverId=null` as a string into href attributes. Clicking these tabs will cause `Long.valueOf("null")` to throw `NumberFormatException` in the target JSP, crashing the next request. This constitutes a broken user interface for add-mode navigation.

---

### B03-10
**Severity:** MEDIUM
**File:** `driver/general.jsp`, lines 43–45, 48, 256; `driver/subscription.jsp`, lines 19–21; `driver/training.jsp`, lines 20–21; `driver/vehicle.jsp`, lines 19–21
**Title:** URL variables and action codes emitted from scriptlets without HTML encoding

**Description:**
Multiple JSPs emit URL strings constructed from request parameters directly into HTML attributes and JavaScript via `<%= %>`:

```html
<!-- general.jsp line 43 -->
<li class="active"><a class="triggerThis" href="<%=generalUrl%>">General</a></li>

<!-- general.jsp line 256 -->
var actUrl = "<%=actionCode %>";
```

The variables `generalUrl`, `trainingUrl`, `vehicleUrl`, and `actionCode` are built from `request.getParameter("action")` and `request.getParameter("driverId")`. While `id` is validated as Long and `action` is only used to branch (not output directly), the URL strings themselves are emitted without `fn:escapeXml()` or equivalent. If the parameter values are not restricted by the action class before the JSP is rendered (e.g., in cases where JSPs are rendered after a form validation failure and the original parameters are re-echoed), this creates a secondary XSS path via malformed href injection.

---

### B03-11
**Severity:** MEDIUM
**File:** `error.jsp`, lines 17–23
**Title:** Exception re-thrown as bare `new Exception(e.getMessage())` — stack trace information lost

**Description:**
```java
catch(Exception e) {
    InfoLogger.logException(log, e);
    throw new Exception(e.getMessage());
}
```
Re-wrapping with `new Exception(e.getMessage())` discards the original exception's type, cause chain, and stack trace. Downstream error handlers receive only the message string. This makes production incident diagnosis significantly harder and prevents proper exception-type-based routing in a Struts exception handler. While not a direct security issue, it is an untestable anti-pattern embedded in the view.

---

### B03-12
**Severity:** MEDIUM
**File:** `fleetcheckSuccess.jsp`, lines 9, 44
**Title:** Auto-redirect form targets `goSerach.do` — hardcoded typo in action URL

**Description:**
```html
<form action="goSerach.do" method="post" name="searchForm">
```
```javascript
function redirect() {
    document.searchForm.submit();
}
```
The action URL `goSerach.do` is a known typo for `goSearch.do`. While this mapping exists in `struts-config.xml` at path `/goSerach`, it is a typo-dependent hardcoded URL. If the path is ever corrected without updating both `struts-config.xml` and this JSP, the auto-redirect silently breaks. Since the form is submitted programmatically via JavaScript after a timer, the user has no visible indication of the failure. There are no tests that verify the redirect succeeds.

---

### B03-13
**Severity:** MEDIUM
**File:** `fleetcheckSuccess.jsp`, line 23
**Title:** `document.onload` misuse — `init()` executes immediately at parse time

**Description:**
```javascript
document.onload = init();
```
This is incorrect JavaScript. `document.onload` is not a standard event handler (the correct property is `window.onload`); even if it were, the `= init()` syntax calls `init()` immediately and assigns its return value (`undefined`) to the property rather than registering it as a callback. As a result, `setInterval(countDown, 1000)` is called at parse time, which is the intended behaviour in this case, but only by accident. The countdown will start correctly, but the pattern is fragile: if `init()` is refactored to return early when the DOM is not ready, the behaviour changes silently. This is untestable.

---

### B03-14
**Severity:** LOW
**File:** `driver/general.jsp`, line 210
**Title:** `console.log` debug statement left in production code

**Description:**
```javascript
console.log("valid:"+valid);
```
A `console.log` debug statement is present inside the PIN validation function. In production this outputs the current validation state on every input change event to the browser console, which is visible to any user opening DevTools. While the `valid` value itself is not sensitive, debug logging in production is undesirable from a security hygiene and professional code quality standpoint.

---

### B03-15
**Severity:** LOW
**File:** `driver/licence.jsp`
**Title:** File is empty — tab navigation broken for non-US/Canada timezones

**Description:**
`licence.jsp` is a zero-byte empty file. The tab navigation in `driver/general.jsp` (line 44), `driver/subscription.jsp` (line 20), `driver/training.jsp` (line 21), and `driver/vehicle.jsp` (line 20) renders a tab labelled "Licence" (instead of "Training") for users whose `sessTimezone` does not contain `"US/"` or `"Canada/"`. Clicking that tab will request `admindriver.do?action=training&driverId=...`, which would forward to this empty JSP, rendering a blank modal panel with no content. There is no test to catch this regression.

---

### B03-16
**Severity:** LOW
**File:** All driver tab JSPs (`general.jsp`, `subscription.jsp`, `training.jsp`, `vehicle.jsp`, `expiringTrainings.jsp`)
**Title:** Timezone business rule copy-pasted in five JSP files — no single source of truth

**Description:**
The following logic appears verbatim five times across these files:
```java
String trainingtab = "Training";
if(!timezone.contains("US/")&&!timezone.contains("Canada/"))
{
    trainingtab = "Licence";
}
```
This is a maintenance hazard and an untestable pattern. Any change to which timezones use "Licence" vs "Training" must be replicated manually in all five files. Since there are no tests, a partial update would introduce a subtle inconsistency visible to international users.

---

### B03-17
**Severity:** INFO
**File:** All 9 audited JSP files
**Title:** Zero test coverage for all view files and their backing action classes

**Description:**
The project test suite contains only 4 test classes, all covering calibration mathematics and impact utilities. There are:
- No JSP rendering/integration tests
- No Selenium or browser-based UI tests
- No mock-servlet unit tests for action classes
- No tests for `DealerSessionReportAction`, `AdminDriverEditAction`, `AdminDriverAddAction`, or `AdminTrainingsAction`

The view-layer logic identified in findings B03-1 through B03-16 is entirely exercised only by manual testing. Regression detection for XSS, null-pointer crashes, broken tab navigation, and routing decisions depends entirely on manual QA.

---

### B03-18
**Severity:** INFO
**File:** All driver tab JSPs
**Title:** No view-layer authorization check — relies entirely on action servlet

**Description:**
None of the audited JSPs perform any session-based authorization check (e.g., verifying `sessRole` or `sessCompId`). Authorization is delegated to `PreFlightActionServlet`, which checks `sessCompId` is non-null for all protected `.do` requests. This is the correct architecture (auth in the servlet layer, not the view), but it means:
1. If the JSP is ever exposed directly (e.g., via a misconfigured tiles definition or a direct `/html-jsp/...` URL without the Struts filter), it will render without any authentication gate.
2. The authorization boundary is not tested.

---

## 4. Summary Table

| ID     | Severity | File(s)                         | Title |
|--------|----------|---------------------------------|-------|
| B03-1  | CRITICAL | `dealer/sessionReport.jsp`      | Reflected XSS via date parameters injected into JavaScript |
| B03-2  | HIGH     | `dealer/sessionReport.jsp`      | NPE on `sessDateFormat` null — guaranteed crash on session expiry |
| B03-3  | HIGH     | `driver/general.jsp`            | Client-side MD5 used as password hash before transmission |
| B03-4  | HIGH     | `driver/training.jsp`           | Training deletion via HTTP GET — CSRF and idempotency violation |
| B03-5  | HIGH     | `subscription.jsp`, `training.jsp`, `vehicle.jsp` | Unguarded `Long.valueOf()` on user input — DoS via NumberFormatException |
| B03-6  | HIGH     | `general.jsp`, `subscription.jsp`, `training.jsp`, `vehicle.jsp`, `expiringTrainings.jsp` | Business routing and locale-detection logic in view scriptlets — untestable |
| B03-7  | MEDIUM   | `general.jsp`, `subscription.jsp`, `training.jsp`, `vehicle.jsp`, `expiringTrainings.jsp` | `sessTimezone` used without null-check — NPE on session expiry |
| B03-8  | MEDIUM   | `driver/training.jsp`           | Chained `sessDateFormat` method call without null-check — NPE risk |
| B03-9  | MEDIUM   | `subscription.jsp`, `training.jsp`, `vehicle.jsp` | Tab navigation URLs contain literal `"null"` string when driverId absent |
| B03-10 | MEDIUM   | Multiple driver tab JSPs        | URL variables emitted without HTML encoding into attributes and JavaScript |
| B03-11 | MEDIUM   | `error.jsp`                     | Exception re-thrown as bare `new Exception` — stack trace lost |
| B03-12 | MEDIUM   | `fleetcheckSuccess.jsp`         | Auto-redirect targets hardcoded typo URL `goSerach.do` |
| B03-13 | MEDIUM   | `fleetcheckSuccess.jsp`         | `document.onload = init()` — incorrect event registration pattern |
| B03-14 | LOW      | `driver/general.jsp`            | `console.log` debug statement left in production code |
| B03-15 | LOW      | `driver/licence.jsp`            | File is completely empty — tab broken for non-US/Canada timezones |
| B03-16 | LOW      | 5 driver/expiring JSPs          | Timezone business rule copy-pasted 5 times — no single source of truth |
| B03-17 | INFO     | All 9 audited JSPs              | Zero test coverage for all view files and their backing action classes |
| B03-18 | INFO     | All driver tab JSPs             | No view-layer authorization check — relies entirely on action servlet |
