# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** B03
**Date:** 2026-02-26

## JSP Files Audited

1. `html-jsp/dealer/preOpsReport.jsp`
2. `html-jsp/dealer/sessionReport.jsp`
3. `html-jsp/driver/general.jsp`
4. `html-jsp/driver/licence.jsp`
5. `html-jsp/driver/subscription.jsp`
6. `html-jsp/driver/training.jsp`
7. `html-jsp/driver/vehicle.jsp`
8. `html-jsp/error.jsp`
9. `html-jsp/expiringTrainings.jsp`

## Test Directory Survey

**Test directory:** `src/test/java/`

Only four test files exist in the entire test suite. None of them relate to any JSP under audit:

| File | Subject |
|---|---|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | UnitCalibrationImpactFilter utility |
| `com/calibration/UnitCalibrationTest.java` | UnitCalibration domain model |
| `com/calibration/UnitCalibratorTest.java` | UnitCalibrator algorithm |
| `com/util/ImpactUtilTest.java` | ImpactUtil helper |

Grep results for each JSP name in the test directory: **zero matches** for all nine files (`preOpsReport`, `sessionReport`, `general`, `licence`, `subscription`, `training`, `vehicle`, `error`, `expiringTrainings`).

---

## File-by-File Evidence and Findings

---

### 1. `html-jsp/dealer/preOpsReport.jsp`

**Purpose:** Dealer-facing report view listing pre-operation checks completed within a date range, filterable by manufacturer and unit type. Renders a filterable HTML table with equipment, driver, datetime, failures, duration, and comment columns. Also initialises jQuery date-picker widgets.

**Scriptlet blocks:**

- Lines 4-6: Reads `sessDateFormat` from session, performs two `replaceAll` transformations to derive a JS-compatible date format string:
  ```java
  String dateFormat = ((String) session.getAttribute("sessDateFormat"))
      .replaceAll("yyyy", "yy").replaceAll("M", "m");
  ```
  No null-check before the `replaceAll` call; a `NullPointerException` is thrown if `sessDateFormat` is absent from the session.

- Lines 109-111: Reads `start_date` request parameter, passes it directly to `DateUtil.stringToIsoNoTimezone()`, and emits the result into a JavaScript string literal without escaping:
  ```java
  if (request.getParameter("start_date") != null) { %>
  start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
      request.getParameter("start_date"),
      (String) session.getAttribute("sessDateFormat")) %>");
  <% } %>
  ```

- Lines 113-115: Same pattern for `end_date`.

- Lines 117-118: The derived `dateFormat` string is emitted directly into JS:
  ```java
  setupDatePicker('#start_date', '<%= dateFormat %>', start_date);
  setupDatePicker('#end_date', '<%= dateFormat %>', end_date);
  ```

**EL / Struts tag output (unescaped by default in Struts 1.x unless `filter="true"`):**

- `<bean:write name="preOpsEntry" property="unitName"/>` — line 81
- `<bean:write name="preOpsEntry" property="manufacture"/>` — line 82
- `<bean:write name="preOpsEntry" property="companyName"/>` — line 83
- `<bean:write name="preOpsEntry" property="driverName"/>` — line 84
- `<bean:write name="preOpsEntry" property="checkDateTime"/>` — line 85
- `<bean:write name="failure"/>` (nested iteration over failure strings) — line 90
- `<bean:write name="preOpsEntry" property="duration"/>` — line 94
- `<bean:write name="preOpsEntry" property="comment"/>` — line 95

None of the `<bean:write>` tags specify `filter="true"`.

**JavaScript with security implications:**

- Request parameters `start_date` and `end_date` are processed by `DateUtil.stringToIsoNoTimezone()` and the result is spliced into a JS `new Date("...")` constructor. If `stringToIsoNoTimezone` returns null (e.g., because it cannot parse the date), an unhandled `NullPointerException` is thrown server-side and partial or broken content is emitted to the browser. Additionally, if the date parsing fallback in `DateUtil.stringToDate` produces a result that still contains attacker-controlled characters (e.g., due to a crafted format), the unescaped emission inside a JS string literal is an injection vector.
- The session-derived `dateFormat` string is emitted into a JS string literal without escaping. A compromised or unexpected session value could inject arbitrary JS.

---

### 2. `html-jsp/dealer/sessionReport.jsp`

**Purpose:** Dealer-facing session report showing vehicle, driver, start time, and finish time entries, filterable by vehicle, driver, and date range.

**Scriptlet blocks:**

- Lines 4-6: Identical `sessDateFormat` extraction pattern as `preOpsReport.jsp`. Same NPE risk if session attribute is absent.

- Lines 99-105: Reads `start_date` request parameter and emits into JS string literal without HTML/JS escaping:
  ```java
  if (request.getParameter("start_date") != null) { %>
  start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
      request.getParameter("start_date"),
      (String) session.getAttribute("sessDateFormat")) %>")
  <% } %>
  ```

- Lines 107-113: Same pattern for `end_date`.

- Lines 114-115: `dateFormat` emitted into JS string literal:
  ```java
  setupDatePicker('#start_date', '<%= dateFormat %>', start_date);
  setupDatePicker('#end_date', '<%= dateFormat %>', end_date);
  ```

**EL / Struts tag output:**

- `<bean:write property="unitName" name="sessionEntry"/>` — line 81
- `<bean:write property="driverName" name="sessionEntry"/>` — line 82
- `<bean:write property="startTime" name="sessionEntry"/>` — line 83
- `<bean:write property="finishTime" name="sessionEntry"/>` — line 84

None specify `filter="true"`.

**JavaScript with security implications:**

- Same injection pattern as `preOpsReport.jsp`: `start_date` and `end_date` request parameters are passed through `DateUtil.stringToIsoNoTimezone()` and spliced into JS string literals without escaping.

---

### 3. `html-jsp/driver/general.jsp`

**Purpose:** Driver add/edit modal tab — General tab. Displays and accepts first name, last name, mobile, email (username), and PIN (password) fields. Handles both add and edit modes based on the `action` request parameter.

**Scriptlet blocks:**

- Lines 4-38: Large initialization block. Reads `action` and `driverId` from request parameters with null-coalescing defaults. Constructs URL strings by direct string concatenation of the raw `id` value. Reads `sessTimezone` from session to conditionally label the Training/Licence tab:
  ```java
  String action = request.getParameter("action") == null ? "" : request.getParameter("action");
  String id = request.getParameter("driverId") == null ? "" : request.getParameter("driverId");
  // ...URL construction with id appended directly...
  String timezone = (String) session.getAttribute("sessTimezone");
  // NPE if sessTimezone is null:
  if(!timezone.contains("US/")&&!timezone.contains("Canada/")) { ... }
  ```
  No null-check on `timezone` before calling `.contains()`.

- Lines 28-31: Conditional read of `newDriverId` request attribute with `toString()` cast:
  ```java
  if (StringUtils.isBlank(id) && request.getAttribute("newDriverId") != null) {
      id = request.getAttribute("newDriverId").toString();
      request.removeAttribute("newDriverId");
  }
  ```

**Direct scriptlet output into HTML (unescaped):**

- Line 43: `href="<%=generalUrl%>"` — generalUrl contains the raw `id` value from request parameter.
- Line 44: `href="<%=trainingUrl%>"` and `<%=trainingtab%>` — trainingUrl likewise.
- Line 45: `href="<%=vehicleUrl%>"`.
- Line 135: `<html:hidden property="id" value="<%=id %>" name="driver"/>` — raw `id` from request parameter emitted as hidden field value.
- Line 136: `<html:hidden property="op_code" value="<%=op_code %>" name="driver"/>`.
- Line 256: `var actUrl = "<%=actionCode %>";` — actionCode is a hardcoded constant, not a risk in itself.

**EL / Struts tags (no filter):**

- `<bean:write name="errfirst_name"/>` — line 68
- `<bean:write name="last_name"/>` — line 79
- `<bean:write name="mobile"/>` — line 91

**JavaScript with security implications:**

- MD5 is used as the PIN hashing algorithm (line 205):
  ```javascript
  var password = '' + CryptoJS.MD5($('input[name="pass"]').val());
  $('input[name=pass_hash]').val(password);
  ```
  MD5 is cryptographically broken. Hashing is performed client-side before transmission; the server may be accepting an MD5 hash rather than verifying the plain PIN, meaning the hash itself is the credential. There are no tests for this hashing behavior.

- `console.log("valid:"+valid)` on line 210 leaks internal validation state to the browser console in production.

- Client-side-only PIN validation: numeric-only check and 4–8 digit length check are performed exclusively in JavaScript. These controls can be trivially bypassed.

- `history.back(-1)` is used in error.jsp; the negative integer argument is non-standard (the standard is `history.back()` or `history.go(-1)`).

---

### 4. `html-jsp/driver/licence.jsp`

**Purpose:** Unknown — file exists on disk but is completely empty (0 bytes).

**Scriptlet blocks:** None (empty file).

**EL expressions:** None.

**JavaScript:** None.

---

### 5. `html-jsp/driver/subscription.jsp`

**Purpose:** Driver edit modal tab — Subscription tab. Displays email subscription fields (up to four addresses) for driver alert notifications.

**Scriptlet blocks:**

- Lines 3-15: Reads `driverId` request parameter and constructs navigation URLs. No null-check on `sessTimezone` before calling `.contains()`:
  ```java
  Long id = request.getParameter("driverId") == null ? null : Long.valueOf(request.getParameter("driverId"));
  // ...
  String timezone = (String) session.getAttribute("sessTimezone");
  if(!timezone.contains("US/")&&!timezone.contains("Canada/")) { ... }
  ```
  If `driverId` is non-null but not a valid long, `Long.valueOf()` throws `NumberFormatException` with no try/catch around the conversion.
  If `sessTimezone` is absent from session, NPE is thrown.

**Direct scriptlet output into HTML:**

- Line 19: `href="<%=generalUrl%>"`.
- Line 20: `href="<%=trainingUrl%>"` and `<%=trainingtab%>`.
- Line 21: `href="<%=vehicleUrl%>"`.

**EL / Struts tags:** None that render unescaped user data directly; fields are populated from `arrAdminDriverEmails` bean via `html:text` tags (which encode for HTML attribute context).

**JavaScript:** No significant security implications beyond the general lack of server-side validation.

---

### 6. `html-jsp/driver/training.jsp`

**Purpose:** Driver edit modal tab — Training/Licence tab. Displays existing driver training records (manufacturer, type, fuel type, training date, expiration date) in a table, and provides an inline form to add new training records via AJAX. Delete is also available via AJAX.

**Scriptlet blocks:**

- Lines 3-16: Same `driverId` → `Long.valueOf()` pattern without null-check on `sessTimezone`:
  ```java
  Long id = request.getParameter("driverId") == null ? null : Long.valueOf(request.getParameter("driverId"));
  // ...
  String dateFormat = ((String) session.getAttribute("sessDateFormat"))
      .replaceAll("yyyy", "yy").replaceAll("M", "m");
  String timezone = (String) session.getAttribute("sessTimezone");
  if(!timezone.contains("US/")&&!timezone.contains("Canada/")) { ... }
  ```
  NPE if either `sessDateFormat` or `sessTimezone` is absent.
  `NumberFormatException` if `driverId` is non-numeric.

- Lines 134-138: `dateFormat` is emitted into JS string literals:
  ```java
  setupDatePicker('#new-training-date', '<%=dateFormat%>', today);
  setupDatePicker('#new-expiration-date', '<%=dateFormat%>', nextYear);
  ```

**Direct scriptlet output into HTML:**

- Line 21: `href="<%=trainingUrl%>"` and `<%=trainingtab%>`.
- Line 32: `<%=trainingtab%>` rendered as visible heading text.

**EL / Struts tags (no filter specified):**

- `<bean:write name="training" property="manufacture_name"/>` — line 52
- `<bean:write name="training" property="type_name"/>` — line 53
- `<bean:write name="training" property="fuel_type_name"/>` — line 54
- `<bean:write name="training" property="training_date"/>` — line 55
- `<bean:write name="training" property="expiration_date"/>` — line 56
- `<bean:write name="training" property="id"/>` — line 60-61, emitted inside an `onclick` attribute:
  ```html
  onclick="deleteTraining(event, <bean:write name="training" property="id"/>)"
  ```
  This is an integer ID so the immediate XSS risk is low, but the absence of `filter="true"` is still a gap.
- `<bean:write name="manufacturer" property="id"/>` — line 74, emitted as `<option value="...">`.
- `<bean:write name="manufacturer" property="name"/>` — line 75.
- `<bean:write name="type" property="id"/>` — line 83.
- `<bean:write name="type" property="name"/>` — line 84.
- `<bean:write name="fuelType" property="id"/>` — line 93.
- `<bean:write name="fuelType" property="name"/>` — line 94.
- `<bean:write name="driverId"/>` — line 112, emitted as hidden input value.

**JavaScript with security implications:**

- `addTraining()` posts to `trainings.do` via `$.post()` passing values from the DOM. No CSRF token is present in the AJAX request.
- `deleteTraining()` makes a `$.get()` to `trainings.do` with the training ID. Using GET for a state-changing delete operation violates HTTP semantics and is vulnerable to CSRF via image tags or prefetch.
- The `setupConfirmationPopups` call on line 127 references `'#adminDriverUpdateTraining'` but the form's `styleId` is `"adminDriverUpdateVehicle"` (line 25). This selector mismatch means the confirmation popup logic will silently fail to bind.

---

### 7. `html-jsp/driver/vehicle.jsp`

**Purpose:** Driver edit modal tab — Vehicles tab. Shows all vehicles with assigned/trained/hours status; allows changing vehicle assignments via checkboxes.

**Scriptlet blocks:**

- Lines 3-15: Same `driverId` → `Long.valueOf()` without validation; same NPE risk on `sessTimezone`:
  ```java
  Long id = request.getParameter("driverId") == null ? null : Long.valueOf(request.getParameter("driverId"));
  // ...
  String timezone = (String) session.getAttribute("sessTimezone");
  if(!timezone.contains("US/")&&!timezone.contains("Canada/")) { ... }
  ```

**Direct scriptlet output into HTML:**

- Line 19: `href="<%=generalUrl%>"`.
- Line 20: `href="<%=trainingUrl%>"` and `<%=trainingtab%>`.
- Line 21: `href="<%=vehicleUrl%>"`.

**EL / Struts tags (no filter):**

- `<bean:write name="vehicle" property="name"/>` — line 51
- `<bean:write name="vehicle" property="location"/>` — line 52
- `<bean:write name="vehicle" property="department"/>` — line 53
- `<bean:write name="vehicle" property="trained"/>` — line 58-59
- `<bean:write name="vehicle" property="hours"/>` — line 60-61

**JavaScript:** No security-significant patterns beyond `setupConfirmationPopups`.

---

### 8. `html-jsp/error.jsp`

**Purpose:** Generic error page fragment. Renders Struts errors and provides a "Previous" button that calls `history.back(-1)`.

**Scriptlet blocks:**

- Lines 4-6: Obtains a logger instance (`InfoLogger.getLogger`).
- Lines 17-23: Catches `Exception`, logs it, and re-throws with `e.getMessage()`. The re-throw wraps the original exception message in a new `Exception`, potentially losing the original stack trace and exception type:
  ```java
  catch(Exception e) {
      InfoLogger.logException(log, e);
      throw new Exception(e.getMessage());
  }
  ```

**EL / Struts tags:**

- `<html:errors/>` — renders all Struts action errors. In Struts 1.x, `html:errors` escapes the error messages by default only if the message resource strings do not contain HTML. If action code places raw HTML or user-supplied content into error messages, this could render unsanitized content.

**JavaScript with security implications:**

- `history.back(-1)`: the integer argument `-1` is non-standard. The HTML specification for `history.back()` takes no argument; `history.go(-1)` is the correct call for "go back one page." While browsers handle this gracefully in practice, it is technically incorrect.
- No CSP headers are set within the JSP.

---

### 9. `html-jsp/expiringTrainings.jsp`

**Purpose:** Dashboard panel showing drivers whose training or licence is expired or expiring soon. Iterates over `arrExpiringTrainings` (a list of `DriverTrainingBean`) to display name, email, vehicle name, training date, and expiration date.

**Scriptlet blocks:**

- Lines 3-9: Reads `sessTimezone` from session with no null-check before calling `.contains()`:
  ```java
  String timezone = (String) session.getAttribute("sessTimezone");
  if(!timezone.contains("US/")&&!timezone.contains("Canada/")) { ... }
  ```

- Line 19: The derived `trainingtab` string is emitted directly into HTML:
  ```java
  <div>Drivers with <%=trainingtab %> expired or expiring soon</div>
  ```
  `trainingtab` is derived from the session attribute, not user input, so XSS risk is low, but the pattern is present.

**EL / Struts tags (no filter):**

- `<bean:write property="first_name" name="training"/>` — line 40
- `<bean:write property="last_name" name="training"/>` — line 40
- `<bean:write property="email" name="training"/>` — line 43
- `<bean:write property="unit_name" name="training"/>` — line 46
- `<bean:write property="training_date" name="training"/>` — line 50
- `<bean:write property="expiration_date" name="training"/>` — line 58

No `filter="true"` on any tag. Driver first name, last name, email, and vehicle name are all user-originated data that could contain `<script>` or other HTML if stored without sanitization.

**JavaScript:** None.

---

## Findings

### Summary Table

| ID | Severity | File(s) | Description |
|---|---|---|---|
| B03-1 | CRITICAL | All 9 JSPs | Zero test coverage: no unit, integration, or view tests exist for any of the nine audited JSPs |
| B03-2 | CRITICAL | general.jsp | MD5 used client-side for PIN hashing; MD5 is cryptographically broken and the hash itself becomes the credential |
| B03-3 | HIGH | preOpsReport.jsp, sessionReport.jsp | Request parameters `start_date` / `end_date` are passed through `DateUtil.stringToIsoNoTimezone()` and emitted unescaped into a JavaScript string literal; partial JS injection is possible if the date parsing fallback does not fully consume the input |
| B03-4 | HIGH | preOpsReport.jsp, sessionReport.jsp, training.jsp | Session attribute `sessDateFormat` is dereferenced without a null-check; absent attribute causes `NullPointerException` and a 500 error visible to the user |
| B03-5 | HIGH | general.jsp, subscription.jsp, training.jsp, vehicle.jsp, expiringTrainings.jsp | Session attribute `sessTimezone` is dereferenced without a null-check; absent attribute causes `NullPointerException` |
| B03-6 | HIGH | subscription.jsp, training.jsp, vehicle.jsp | `Long.valueOf(request.getParameter("driverId"))` is called without a try/catch; a non-numeric `driverId` parameter throws `NumberFormatException` |
| B03-7 | HIGH | training.jsp | `deleteTraining()` uses HTTP GET for a state-changing operation, making it trivially exploitable via CSRF (e.g., `<img src="trainings.do?action=delete&training=N">`) |
| B03-8 | HIGH | training.jsp, subscription.jsp, vehicle.jsp | AJAX form submissions do not include a CSRF token |
| B03-9 | HIGH | preOpsReport.jsp, sessionReport.jsp, training.jsp, expiringTrainings.jsp, vehicle.jsp, general.jsp | `<bean:write>` tags render user-originated data (names, comments, failure strings, email addresses) without `filter="true"`; Struts 1.x `bean:write` does not HTML-escape by default, creating stored XSS risk |
| B03-10 | MEDIUM | licence.jsp | File is completely empty (0 bytes); the JSP is referenced in navigation links from general.jsp, subscription.jsp, training.jsp, and vehicle.jsp but serves no content |
| B03-11 | MEDIUM | training.jsp | `setupConfirmationPopups` call references selector `'#adminDriverUpdateTraining'` but the actual form `styleId` is `"adminDriverUpdateVehicle"`; the confirmation popup silently fails to bind to the form |
| B03-12 | MEDIUM | error.jsp | Exception is re-thrown as `new Exception(e.getMessage())`, discarding the original exception type and stack trace; makes diagnosing server errors harder |
| B03-13 | MEDIUM | general.jsp | Client-side-only PIN validation (numeric check, 4–8 digit length); entirely bypassable by crafting a direct POST request to `admindriveredit.do`; no evidence of equivalent server-side validation tested |
| B03-14 | MEDIUM | preOpsReport.jsp, sessionReport.jsp | Session-derived `dateFormat` is emitted unescaped into a JavaScript string literal; a malformed or compromised session value could inject arbitrary JavaScript |
| B03-15 | MEDIUM | general.jsp | `console.log("valid:"+valid)` statement leaks internal validation state to the browser console in production |
| B03-16 | MEDIUM | preOpsReport.jsp, sessionReport.jsp | `DateUtil.stringToIsoNoTimezone()` can throw `NullPointerException` if the date string cannot be parsed (returns null from `stringToDate`); no null-check before calling `df.format(dateObj)` |
| B03-17 | LOW | sessionReport.jsp | URL in breadcrumb has a trailing space: `href="dealerSessionReport.do "` (line 11); cosmetic but indicates lack of review |
| B03-18 | LOW | error.jsp | `history.back(-1)` uses a non-standard integer argument; correct idiom is `history.go(-1)` or `history.back()` |
| B03-19 | LOW | preOpsReport.jsp, sessionReport.jsp, training.jsp | `DateUtil.stringToDate()` has a silent fallback: if the primary format fails to parse, it retries with hardcoded `"dd/MM/yyyy"` and swallows the second `ParseException` via `System.out.println`; no test covers this fallback path |
| B03-20 | INFO | All 9 JSPs | No JSP-level unit tests exist anywhere in the project; the four existing tests cover only impact/calibration utilities unrelated to any of these views |

---

## Detailed Finding Descriptions

**B03-1 | Severity: CRITICAL | Zero test coverage across all nine JSPs**
The test directory contains only four Java test files, none of which reference or exercise any of the nine JSPs under audit, their backing Struts actions, or the form beans they depend upon. There are no mock-request tests, no integration tests, and no automated rendering tests. All scriptlet logic, conditional branches, and output paths are completely untested.

**B03-2 | Severity: CRITICAL | MD5 client-side PIN hashing in general.jsp**
`driver/general.jsp` lines 205-206 compute `CryptoJS.MD5(pin)` in the browser and submit the hash via a hidden field `pass_hash`. MD5 is cryptographically broken (preimage attacks, collision attacks). Performing the hash client-side means the MD5 digest is the credential transmitted over the wire; capturing it is sufficient to replay it. There are no tests confirming the server rejects replayed hashes or that it enforces a stronger algorithm.

**B03-3 | Severity: HIGH | Unescaped request parameter in JavaScript string literal (preOpsReport.jsp, sessionReport.jsp)**
`request.getParameter("start_date")` and `request.getParameter("end_date")` are passed to `DateUtil.stringToIsoNoTimezone()` whose output is embedded verbatim inside `new Date("...")`. If the date parsing fallback in `DateUtil.stringToDate()` processes the input in a way that leaves attacker-controlled characters in the output, this becomes a JavaScript injection point. No encoding (e.g., `StringEscapeUtils.escapeEcmaScript`) is applied.

**B03-4 | Severity: HIGH | NPE on null sessDateFormat (preOpsReport.jsp, sessionReport.jsp, training.jsp)**
Line 5 of `preOpsReport.jsp` and `sessionReport.jsp`, line 9 of `training.jsp`: `((String) session.getAttribute("sessDateFormat")).replaceAll(...)` — if the session attribute is absent (expired session, session fixation, or a code path that omits setting it), `getAttribute` returns null and `replaceAll` throws a `NullPointerException`. No defensive null-check exists, and no test covers the missing-attribute path.

**B03-5 | Severity: HIGH | NPE on null sessTimezone (general.jsp, subscription.jsp, training.jsp, vehicle.jsp, expiringTrainings.jsp)**
All five files call `timezone.contains(...)` without first checking that `timezone != null`. A null session attribute causes an NPE. This pattern is repeated identically in five separate files.

**B03-6 | Severity: HIGH | NumberFormatException on non-numeric driverId (subscription.jsp, training.jsp, vehicle.jsp)**
`Long.valueOf(request.getParameter("driverId"))` in lines 4 of subscription.jsp, training.jsp, and vehicle.jsp has no try/catch. A request with `driverId=abc` or `driverId=` (when the null-check was already done, confirming it is non-null) causes an unhandled `NumberFormatException` that propagates to the container and produces a 500 error.

**B03-7 | Severity: HIGH | HTTP GET for delete operation in training.jsp**
`deleteTraining()` (line 162) makes a `$.get('trainings.do', {action: 'delete', training: id})`. Using GET for a state-changing delete is a REST anti-pattern and violates the HTTP specification. Any hyperlink, `<img>` tag, or browser prefetch to the URL `trainings.do?action=delete&training=N` would silently delete a training record. No CSRF protection is feasible with GET-based mutations.

**B03-8 | Severity: HIGH | Missing CSRF tokens in AJAX submissions (training.jsp, subscription.jsp, vehicle.jsp)**
The `addTraining()` AJAX POST and the form submissions driven by `setupConfirmationPopups` do not include any CSRF token. A malicious page loaded in the same browser session can forge these requests against an authenticated user.

**B03-9 | Severity: HIGH | Stored XSS via unfiltered bean:write output (multiple JSPs)**
Struts 1.x `<bean:write>` does NOT HTML-encode output unless `filter="true"` is explicitly set. None of the `<bean:write>` tags across the nine JSPs set this attribute. User-controlled fields — driver first name, last name, email, mobile, vehicle name, company name, unit name, pre-ops failure strings, and pre-ops comments — are rendered directly into the HTML response. If any of these fields contain `<script>alert(1)</script>` or similar payloads (stored via an insufficiently validated data entry path), the stored XSS fires on every page load.

**B03-10 | Severity: MEDIUM | licence.jsp is an empty file**
`driver/licence.jsp` has 0 bytes. Navigation tabs in `general.jsp`, `subscription.jsp`, `training.jsp`, and `vehicle.jsp` generate links pointing to `admindriver.do?action=training&driverId=...` which presumably renders this file. An empty JSP renders a blank modal panel with no content, error message, or fallback. It is unclear whether this is intentional (feature stub) or an accidental deletion.

**B03-11 | Severity: MEDIUM | Mismatched form ID in training.jsp setupConfirmationPopups call**
`training.jsp` line 127 calls `setupConfirmationPopups('#adminDriverUpdateTraining', ...)` but the HTML form on line 25 has `styleId="adminDriverUpdateVehicle"`. The jQuery selector `#adminDriverUpdateTraining` will find no element, so the confirmation popup event handler is never bound. Form submissions from the training tab will either silently bypass the confirmation dialog or behave unexpectedly. No test catches this.

**B03-12 | Severity: MEDIUM | Exception re-wrapping loses original type and stack trace in error.jsp**
`error.jsp` lines 19-23 catch `Exception e` and throw `new Exception(e.getMessage())`. This discards the original exception class and full stack trace, replacing them with a plain `Exception` carrying only the message string. Downstream error handlers receive a stripped exception that is harder to diagnose. The `InfoLogger.logException` call does log the original exception, but the propagated exception loses fidelity.

**B03-13 | Severity: MEDIUM | Client-side-only PIN validation in general.jsp**
The numeric-only check and 4–8 digit length check for the driver PIN are implemented exclusively in JavaScript (`validateFields()` function). Any attacker can submit a direct POST to `admindriveredit.do` with a PIN that violates these rules (e.g., non-numeric characters, length outside 4–8). No test verifies that server-side validation rejects invalid PIN values.

**B03-14 | Severity: MEDIUM | Session-derived dateFormat emitted unescaped into JS (preOpsReport.jsp, sessionReport.jsp)**
`<%= dateFormat %>` is placed inside a single-quoted JS string: `setupDatePicker('#start_date', '<%= dateFormat %>', ...)`. If the session value for `sessDateFormat` contains a single quote or other JS metacharacter, the string literal breaks and arbitrary JavaScript can execute. Although session data is generally trusted, it originates from database configuration and is not tested for JS-safety.

**B03-15 | Severity: MEDIUM | Debug console.log in production code (general.jsp)**
Line 210 of `general.jsp`: `console.log("valid:"+valid)` — logs internal form validation state to the browser developer console. This is a development artifact present in production code. No test or linting rule prevents this from shipping.

**B03-16 | Severity: MEDIUM | Potential NPE in DateUtil.stringToIsoNoTimezone (preOpsReport.jsp, sessionReport.jsp)**
`DateUtil.stringToIsoNoTimezone()` calls `stringToDate()` which can return null if both parse attempts fail (second `ParseException` is swallowed). The result is then passed to `df.format(dateObj)` without a null-check, which throws `NullPointerException`. The JSP emits partial content up to the scriptlet that throws, producing a malformed response. No test covers parse-failure scenarios.

**B03-17 | Severity: LOW | Trailing space in breadcrumb URL (sessionReport.jsp)**
`sessionReport.jsp` line 11: `<a href="dealerSessionReport.do ">` contains a trailing space in the href attribute. Most browsers handle this gracefully, but it is an indication of lack of automated linting or review.

**B03-18 | Severity: LOW | Non-standard history.back(-1) call (error.jsp)**
`error.jsp` line 28: `history.back(-1)`. The DOM `history.back()` method takes no arguments; `history.go(-1)` is the correct call for navigating back one step. The argument is ignored by all current browsers but is incorrect per specification.

**B03-19 | Severity: LOW | Silent date parsing fallback with System.out in DateUtil (preOpsReport.jsp, sessionReport.jsp, training.jsp)**
`DateUtil.stringToDate()` retries with a hardcoded `"dd/MM/yyyy"` format if the primary format fails, and swallows the secondary `ParseException` with a `System.out.println`. This fallback is invisible in logs (uses stdout, not the logging framework), alters behavior silently based on an undocumented secondary format, and has no test coverage for the fallback path.

**B03-20 | Severity: INFO | No JSP-level test infrastructure exists in the project**
The project has no test framework (e.g., Mockito with MockHttpServletRequest, Cactus, Selenium, or similar) configured to exercise JSP rendering paths. The four existing tests cover only standalone utility/domain classes. Achieving meaningful JSP coverage would require introducing a testing framework capable of exercising Struts 1.x action+view pipelines.
