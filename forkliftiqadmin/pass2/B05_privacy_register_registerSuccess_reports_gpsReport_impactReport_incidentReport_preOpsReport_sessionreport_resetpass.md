# Pass 2 Test Coverage Audit — Agent B05
**Audit Run:** 2026-02-26-01
**Agent:** B05
**Date:** 2026-02-26
**Scope:** JSP view files — privacy, register, registerSuccess, reports/gpsReport, reports/impactReport, reports/incidentReport, reports/preOpsReport, reports/sessionreport, resetpass
**Test directory:** /mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/

---

## Preamble — Test Directory State

The test directory contains exactly four test files, none of which relate to any JSP under audit:

- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

A grep of the test directory for each JSP filename (privacy, register, registerSuccess, gpsReport, gpsreport, impactReport, impactreport, incidentReport, incidentreport, preOpsReport, preopsreport, sessionreport, resetpass) returned **no matches**. There are zero JSP-level tests of any kind in this project.

---

## JSP 1 — privacy.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/privacy.jsp`

### Evidence

**Purpose:** Presents a privacy policy text (pulled from `privacyText.jsp` include) inside a read-only textarea. The user must check a checkbox to enable a Submit button before proceeding. The form POSTs to `privacy.do`.

**Scriptlet blocks:** None. The file contains no `<% %>` scriptlet code.

**EL / Struts tag expressions accessing request/session attributes:**
- `<bean:message key="privacy.accept">` — resolves message bundle key, not a user-supplied value.
- `<bean:message key="button.submit">` — resolves message bundle key.
- `<%@ include file="../includes/privacyText.jsp"%>` — static include of the privacy text fragment.

**JavaScript with security implications:**
```javascript
function enableSubmit() {
    if (document.privacyForm.privacy.checked) {
        document.getElementById("submitBtn").disabled = false;
    } else {
        document.getElementById("submitBtn").disabled = true;
    }
}
```
The `disabled` attribute on the submit button is enforced only client-side. There is no server-side guard preventing a direct POST to `privacy.do` without the checkbox being checked.

**Existing tests for this JSP:** None found.

### Findings

**B05-1 | Severity: MEDIUM | privacy.jsp — Client-side-only enforcement of privacy checkbox acceptance**
The submit button is disabled via JavaScript (`enableSubmit()`), but this is a purely client-side control. An attacker or automated client can POST directly to `privacy.do` without ever accepting the privacy policy. There is no test verifying that the server-side action (`PrivacyAction`) rejects requests where the checkbox value is absent/false.

**B05-2 | Severity: LOW | privacy.jsp — Zero test coverage**
No unit or integration test exists for this JSP or its backing `PrivacyAction`. The rendering path (include of `privacyText.jsp`, Struts tag resolution) is entirely untested.

---

## JSP 2 — register.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/register.jsp`

### Evidence

**Purpose:** New Driver registration form. Collects firstName, lastName, licence_no, and expirydt. Hidden fields carry `veh_id` and `attachment` values seeded from request-scoped bean attributes. POSTs to `register.do`.

**Scriptlet blocks:** None.

**EL / Struts tag expressions accessing request/session attributes:**
- `<bean:define id="veh_id" name="veh_id">` — reads the `veh_id` attribute from the default scope (request/session). If missing, this tag throws a `JspException`; there is no fallback.
- `<bean:write name="veh_id">` — writes the resolved value into an `<input type="hidden">` without HTML encoding. The `bean:write` tag by default does NOT encode HTML entities unless `filter="true"` is explicitly set.
- `<bean:define id="attachment" name="attachment">` — same pattern; reads `attachment` attribute with no null-safety.
- `<bean:write name="attachment">` — writes unencoded into a hidden `<input>` value attribute.
- `<html:errors>` — renders Struts action errors.
- `<html:text property="firstName" ...>`, `<html:text property="lastName" ...>`, `<html:text property="licence_no" ...>`, `<html:text property="expirydt" ...>` — form fields backed by the ActionForm.

**JavaScript with security implications:**
```javascript
$(function() {
    $("#datepicker").datepicker({ dateFormat: 'dd/mm/yy' });
});
```
The `fnback()` function referenced by the Back button's `onclick` handler is not defined in this file. It is presumably defined in an included file (`importLib.jsp` does not define it). If the function is absent, the Back button silently fails.

**Existing tests for this JSP:** None found.

### Findings

**B05-3 | Severity: HIGH | register.jsp — Unencoded output of `veh_id` and `attachment` in hidden input values (XSS risk)**
`<bean:write name="veh_id">` and `<bean:write name="attachment">` emit values into HTML `input value` attributes without the `filter="true"` attribute. If either session/request attribute contains characters such as `"`, `>`, or `<`, the output can break out of the attribute context and inject arbitrary HTML or script. The default `bean:write` behavior in Struts 1.x is to NOT HTML-encode output unless `filter="true"` is explicitly specified.

**B05-4 | Severity: HIGH | register.jsp — NullPointerException / JspException if `veh_id` or `attachment` attributes are absent**
`<bean:define id="veh_id" name="veh_id">` will throw a `JspException` if the named attribute does not exist in any scope. There is no `<logic:present>` guard or try/catch, meaning a missing attribute produces a raw error page. No test covers the absent-attribute path.

**B05-5 | Severity: MEDIUM | register.jsp — `fnback()` JavaScript function referenced but not defined in this file**
The Back button calls `onclick="fnback();"` but `fnback` is not defined anywhere in register.jsp. If the function is absent from the global scope at runtime, clicking Back will throw a JavaScript `ReferenceError` and silently fail to navigate. No test verifies navigation behavior.

**B05-6 | Severity: LOW | register.jsp — Zero test coverage**
No unit or integration test exists for this JSP or `RegisterAction` / `AdminRegisterAction`.

---

## JSP 3 — registerSuccess.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/registerSuccess.jsp`

### Evidence

**Purpose:** Post-registration success page. Displays a confirmation message and redirects the user to `index.jsp` after a 10-second countdown. POSTs to `login.do` (the embedded form, though the user is redirected before they can interact with it).

**Scriptlet blocks:** None (all `<% %>` blocks are commented out).

**EL / Struts tag expressions accessing request/session attributes:**
- `<bean:message key="regsiter.create">` — note: the key name contains a typo (`regsiter` instead of `register`). If the key is absent from the message bundle, Struts renders the raw key name.
- `<bean:message key="register.info">` — message bundle lookup.
- `<bean:message key="button.download">` — message bundle lookup; the download button is `disabled`.
- `<bean:message key="button.home">` — message bundle lookup for the Home button that calls `redirect()`.

**JavaScript with security implications:**
```javascript
var time = 10;
document.onload = init();  // BUG: should be window.onload, not document.onload

function init() {
    setInterval(countDown, 1000);
}

function countDown() {
    if (time > 0) {
        time--;
        document.getElementById("timer").innerHTML = time;
        if (time == 0) { redirect(); }
    }
}

function redirect() {
    var url = "index.jsp";
    location.replace(url);
}
```
The redirect target `"index.jsp"` is a hardcoded relative path.

`document.onload = init()` immediately invokes `init()` at assignment time (because of the `()`) and assigns its return value (`undefined`) to `document.onload`. The net effect is that `init()` runs once synchronously during page parse, which starts the `setInterval`. This is a latent bug but the timer still functions because `setInterval` is called synchronously.

The file also contains both `</html>` and `<body>` tags in incorrect positions — `</html>` appears at line 50 before the `<script>` block, producing malformed HTML.

**Existing tests for this JSP:** None found.

### Findings

**B05-7 | Severity: MEDIUM | registerSuccess.jsp — `document.onload` used instead of `window.onload` (broken event handler pattern)**
`document.onload = init()` does not register `init` as a load event handler; it calls `init()` immediately and assigns the return value (`undefined`) to a non-standard property. While the countdown accidentally works due to the immediate invocation, this is an unintentional behavior and breaks in strict environments. No test covers the countdown/redirect behavior.

**B05-8 | Severity: MEDIUM | registerSuccess.jsp — Malformed HTML: `</html>` tag appears before the `<script>` block**
The closing `</html>` tag (line 50) appears before the `<script>` block (lines 52–76), producing invalid HTML. Browsers may parse the script block anyway, but behavior is undefined. The file also has a lone `<body>` open tag with no enclosing document structure from this fragment.

**B05-9 | Severity: LOW | registerSuccess.jsp — Typo in message key `regsiter.create`**
The key `regsiter.create` is a misspelling of `register.create`. If the properties file does not contain the misspelled key, Struts renders the raw key string. No test validates that all message keys used in this JSP resolve correctly.

**B05-10 | Severity: LOW | registerSuccess.jsp — Hardcoded redirect target `index.jsp`**
The `redirect()` function navigates to the literal string `"index.jsp"`. This cannot be configured or tested in isolation and creates a fragile dependency on the deployment context root.

**B05-11 | Severity: LOW | registerSuccess.jsp — Zero test coverage**
No unit or integration test exists for this JSP or any backing action directing to it.

---

## JSP 4 — reports/gpsReport.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/reports/gpsReport.jsp`

### Evidence

**Purpose:** GPS tracking report page. Displays a map canvas and a multi-select vehicle dropdown populated from `arrAdminUnit`. Provides a Refresh button that calls `initialize()` to load GPS data onto the map.

**Scriptlet blocks:**
```java
// Lines 4-7
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");
String custCd = (String) session.getAttribute("sessCompId");
```
Both statements perform unchecked casts. If `sessDateFormat` is null, a `NullPointerException` is thrown before the cast. If `sessCompId` is null, `custCd` is null (acceptable for the hidden field but not logged or handled).

**EL / Struts tag expressions accessing request/session attributes:**
- `session.getAttribute("sessDateFormat")` — direct scriptlet access, no null guard.
- `session.getAttribute("sessCompId")` — direct scriptlet access.
- `<logic:notEmpty name="arrAdminUnit">` — guarded iteration over the unit list.
- `<logic:iterate name="arrAdminUnit" id="unitRecord" type="com.bean.UnitBean">` — iterates `arrAdminUnit`.
- `<bean:write property="id" name="unitRecord">` / `<bean:write property="name" name="unitRecord">` — writes unit id and name into `<option>` value/label without `filter="true"`.
- `<%= custCd %>` — emits the customer code into a hidden `<input>` value attribute.

**JavaScript with security implications:**
```javascript
var GPS = true;
var custCd = "";  // JavaScript variable never populated from server-side custCd
var defaultLoc = "-24.2761156,133.5912902"; // hardcoded AU coordinates, comment says UK
var defaultLat = "-24.2761156";
var defaultLong = "133.5912902";

function fnRefresh() {
    initialize($('#cust').val(), $('#site').val());
    if ($('#gotoZoneControl').length > 0) {
        application.getGotToZonesControl('#gotoZoneControl');
    }
}
```
The JavaScript `custCd` variable is declared but never assigned the server-side `custCd` value; the hidden input `#cust` is used instead. The `$('#site').val()` reference targets an element (`#site`) that does not exist in this JSP, so `undefined` is passed to `initialize()`.

**Existing tests for this JSP:** None found.

### Findings

**B05-12 | Severity: CRITICAL | gpsReport.jsp — NullPointerException if `sessDateFormat` session attribute is null**
`((String) session.getAttribute("sessDateFormat")).replaceAll(...)` dereferences the result without any null check. If the session attribute is absent (expired session, unauthenticated request that bypasses the filter, or misconfiguration), the page throws a `NullPointerException` and the full stack trace may be exposed to the client. No test covers this path.

**B05-13 | Severity: HIGH | gpsReport.jsp — `<bean:write>` outputs unit id and name without HTML encoding (XSS risk)**
`<bean:write property="id" name="unitRecord">` and `<bean:write property="name" name="unitRecord">` write values into `<option value="...">` and option label content without `filter="true"`. If a unit name or id from the database contains `<`, `>`, `"`, or `'`, the output is unescaped and can inject HTML or script into the page.

**B05-14 | Severity: HIGH | gpsReport.jsp — `$('#site').val()` references a non-existent DOM element**
`fnRefresh()` calls `initialize($('#cust').val(), $('#site').val())`. The `#site` element is not present in this JSP, so `$('#site').val()` returns `undefined`. The behavior of `initialize()` when passed `undefined` as the site parameter is unknown and untested.

**B05-15 | Severity: MEDIUM | gpsReport.jsp — Hardcoded default coordinates are contradictory (comment says UK, values are Australian)**
`defaultLoc = "-24.2761156,133.5912902"` is a point in central Australia. The inline comment reads `//UK- 55.378051, -3.435973`. The mismatch indicates copy-paste error. No test validates that the correct default region is used.

**B05-16 | Severity: MEDIUM | gpsReport.jsp — `custCd` JavaScript variable never populated**
The JavaScript declares `var custCd = ""` but the server-side `custCd` value is only placed in the hidden `<input id="cust">`. Any JavaScript that references `custCd` directly (rather than reading `$('#cust').val()`) will use an empty string. This inconsistency is untested.

**B05-17 | Severity: LOW | gpsReport.jsp — `dateFormat` is computed but never used in this JSP**
The scriptlet computes `dateFormat` from `sessDateFormat` and manipulates the format string, but the variable is never referenced again in gpsReport.jsp. This is dead code that nevertheless carries an NPE risk (finding B05-12).

**B05-18 | Severity: LOW | gpsReport.jsp — Zero test coverage**
No unit or integration test exists for this JSP or `GPSReportAction`.

---

## JSP 5 — reports/impactReport.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/reports/impactReport.jsp`

### Evidence

**Purpose:** Impact report page. Displays a filterable table of impact events grouped by manufacturer/unit. Filters include manufacturer, unit type, impact level (BLUE/AMBER/RED), and a date range. Data is populated from the `impactReport` request attribute.

**Scriptlet blocks:**
```java
// Lines 4-6 — top of file
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");

// Lines 86-93 — inside logic:iterate, in table cell
<td rowspan="<%= impactGroup.getEntries().size() %>">
<td rowspan="<%= impactGroup.getEntries().size() %>">

// Lines 97, 100
<span style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;">
<%= String.format(" (%.1fg)", impactEntry.getGForce()) %>

// Lines 115-124 — JavaScript date picker initialization
<% if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("start_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
<% if (request.getParameter("end_date") != null) { %>
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("end_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
```

**EL / Struts tag expressions accessing request/session attributes:**
- `session.getAttribute("sessDateFormat")` — unchecked, no null guard.
- `<logic:iterate id="impactGroup" name="impactReport" property="groups" ...>` — iterates `impactReport` bean.
- `<bean:write property="manufacturer" name="impactGroup">` — no `filter="true"`.
- `<bean:write property="unitName" name="impactGroup">` — no `filter="true"`.
- `<bean:write property="driverName" name="impactEntry">` — no `filter="true"`.
- `<bean:write property="impactDateTime" name="impactEntry">` — no `filter="true"`.
- `request.getParameter("start_date")` — user-supplied parameter fed directly into `DateUtil.stringToIsoNoTimezone()` and emitted into a JavaScript `new Date("...")` expression.
- `request.getParameter("end_date")` — same.

**JavaScript with security implications:**
```javascript
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("start_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
```
The user-controlled `start_date` and `end_date` request parameters are passed through `DateUtil.stringToIsoNoTimezone()` and emitted directly into a JavaScript string literal. If `stringToIsoNoTimezone()` returns a value containing `"` or other JavaScript metacharacters (e.g., due to a parse failure returning a malformed string), this constitutes a JavaScript injection vector. `DateUtil.stringToIsoNoTimezone()` calls `df.format(dateObj)` where `dateObj` could be `null` if parsing fails, causing a `NullPointerException` in `df.format(null)`.

**Existing tests for this JSP:** None found (ImpactUtilTest exists but tests the utility class, not the JSP).

### Findings

**B05-19 | Severity: CRITICAL | impactReport.jsp — NullPointerException if `sessDateFormat` session attribute is null**
Same pattern as B05-12. `((String) session.getAttribute("sessDateFormat")).replaceAll(...)` throws NPE if the attribute is absent.

**B05-20 | Severity: CRITICAL | impactReport.jsp — NullPointerException in `DateUtil.stringToIsoNoTimezone()` when date parameter fails to parse**
`DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), ...)` calls `stringToDate()` which returns `null` on parse failure (silently catches `ParseException`). The result is then passed to `df.format(dateObj)` where `dateObj` is null, throwing an uncaught `NullPointerException` that propagates to the JSP rendering thread and exposes a stack trace to the client.

**B05-21 | Severity: HIGH | impactReport.jsp — JavaScript injection via unvalidated `start_date`/`end_date` request parameters**
User-supplied `start_date` and `end_date` parameters are embedded directly into a JavaScript `new Date("...")` string literal after processing by `DateUtil.stringToIsoNoTimezone()`. If the date parse fails or the utility returns unexpected characters, arbitrary JavaScript can be injected. The `filter="true"` analog for scriptlet output (`ESAPI.encodeForJavaScript()` or equivalent) is not applied. No test exercises malformed date inputs.

**B05-22 | Severity: HIGH | impactReport.jsp — `<bean:write>` renders manufacturer, unitName, driverName, impactDateTime without HTML encoding (XSS)**
None of the `<bean:write>` tags in the table use `filter="true"`. Database-sourced values (manufacturer name, unit name, driver name) rendered unencoded into HTML table cells can inject arbitrary markup if the data contains special characters.

**B05-23 | Severity: MEDIUM | impactReport.jsp — `impactEntry.getImpactLevelCSSColor()` output emitted into inline style without sanitization**
`<span style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;">` emits a CSS color value from the bean. If `getImpactLevelCSSColor()` can return a value derived from attacker-influenced data (e.g., a stored impact level), a CSS injection is possible. No test validates the set of possible CSS color values returned by `ImpactUtil.getCSSColor()`.

**B05-24 | Severity: LOW | impactReport.jsp — Zero test coverage of JSP rendering**
ImpactUtilTest covers utility logic only. No test covers the JSP rendering, the date parameter handling path, or the table output. The session attribute access and all `<bean:write>` outputs are untested at the view layer.

---

## JSP 6 — reports/incidentReport.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/reports/incidentReport.jsp`

### Evidence

**Purpose:** Incident report table showing unit, manufacturer, driver, description, timestamps, and boolean flags (near_miss, incident, injury). Includes lightbox links for signature and image fields.

**Scriptlet blocks:**
```java
// Lines 4-6
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");

// Lines 162-175 — JavaScript date initialization
if (request.getParameter("start_date") != null) { ... }
if (request.getParameter("end_date") != null) { ... }
// Both embed DateUtil.stringToIsoNoTimezone output into JavaScript string literals
```

**EL / Struts tag expressions accessing request/session attributes:**
- `session.getAttribute("sessDateFormat")` — no null check.
- `<logic:iterate name="incidentReport" property="entries" id="incidentEntry" type="com.bean.IncidentReportEntryBean">` — iterates `incidentReport`.
- `<bean:write property="unitName" name="incidentEntry">` — no `filter="true"`.
- `<bean:write property="manufacture" name="incidentEntry">` — no `filter="true"`.
- `<bean:write property="driverName" name="incidentEntry">` — no `filter="true"`.
- `<bean:write property="description" name="incidentEntry">` — no `filter="true"`. This field represents free-text user input and is the highest-risk unencoded output.
- `<bean:write property="event_time" name="incidentEntry">` — no `filter="true"`.
- `<bean:write property="injureType" name="incidentEntry">` — no `filter="true"`.
- `<bean:write property="location" name="incidentEntry">` — no `filter="true"`.
- `<bean:write property="witness" name="incidentEntry">` — no `filter="true"`.
- `<bean:write property="signature" name="incidentEntry">` — emitted into an `href` attribute without encoding.
- `<bean:write property="image" name="incidentEntry">` — emitted into an `href` attribute without encoding.
- `request.getParameter("start_date")` / `request.getParameter("end_date")` — same JavaScript injection risk as impactReport.jsp.

**JavaScript with security implications:**
Same `new Date("<%= DateUtil.stringToIsoNoTimezone(...) %>")` pattern as impactReport.jsp. Additionally, the `description`, `location`, and `witness` fields are free-text user-entered data rendered unencoded in the HTML table.

The `signature` and `image` fields are rendered as `href` values. If these contain `javascript:` URIs or other data that bypasses URL validation, clicking the lightbox link could execute script.

**Existing tests for this JSP:** None found.

### Findings

**B05-25 | Severity: CRITICAL | incidentReport.jsp — NullPointerException if `sessDateFormat` session attribute is null**
Same pattern as B05-12 and B05-19. No null guard.

**B05-26 | Severity: CRITICAL | incidentReport.jsp — NullPointerException in `DateUtil.stringToIsoNoTimezone()` on parse failure**
Same pattern as B05-20. Applies to both `start_date` and `end_date` parameters.

**B05-27 | Severity: HIGH | incidentReport.jsp — Stored XSS via unencoded `description`, `location`, `witness` fields**
`<bean:write property="description" name="incidentEntry">`, `<bean:write property="location" name="incidentEntry">`, and `<bean:write property="witness" name="incidentEntry">` output free-text user-supplied data (originally entered on mobile devices during incident logging) directly into HTML table cells without HTML encoding. This is a stored XSS vector: malicious script stored in the database is rendered to any admin who views the incident report.

**B05-28 | Severity: HIGH | incidentReport.jsp — `signature` and `image` URLs rendered unencoded into `href` attributes**
`<bean:write property="signature" name="incidentEntry">` and `<bean:write property="image" name="incidentEntry">` produce raw URL strings inside `href="..."` attributes without encoding or protocol validation. A `javascript:` URI stored as the signature or image path would execute when the lightbox anchor is clicked.

**B05-29 | Severity: HIGH | incidentReport.jsp — JavaScript injection via unvalidated `start_date`/`end_date` request parameters**
Same pattern as B05-21.

**B05-30 | Severity: HIGH | incidentReport.jsp — Multiple `<bean:write>` outputs lack `filter="true"` (XSS risk)**
`unitName`, `manufacture`, `driverName`, `event_time`, `injureType` are all output without HTML encoding. Combined with B05-27 and B05-28, the entire incident table row is an unencoded output surface.

**B05-31 | Severity: LOW | incidentReport.jsp — Zero test coverage**
No test exists for this JSP, `IncidentReportAction`, or `IncidentReportDAO` rendering paths.

---

## JSP 7 — reports/preOpsReport.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/reports/preOpsReport.jsp`

### Evidence

**Purpose:** Pre-ops inspection report. Displays a table of pre-operation checks with unit name, manufacturer, driver, datetime, a list of failed checklist items, duration, and comment. Includes a Print Report button.

**Scriptlet blocks:**
```java
// Lines 4-6
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");

// Lines 107-120 — JavaScript date initialization
if (request.getParameter("start_date") != null) { ... }
if (request.getParameter("end_date") != null) { ... }
// Both embed DateUtil.stringToIsoNoTimezone output into JavaScript string literals
```

**EL / Struts tag expressions accessing request/session attributes:**
- `session.getAttribute("sessDateFormat")` — no null check.
- `<logic:iterate name="preOpsReport" property="entries" id="preOpsEntry" type="com.bean.PreOpsReportEntryBean">` — iterates `preOpsReport`.
- `<bean:write property="unitName" name="preOpsEntry">` — no `filter="true"`.
- `<bean:write property="manufacture" name="preOpsEntry">` — no `filter="true"`.
- `<bean:write property="driverName" name="preOpsEntry">` — no `filter="true"`.
- `<bean:write property="checkDateTime" name="preOpsEntry">` — no `filter="true"`.
- `<logic:iterate id="failure" name="preOpsEntry" property="failures" type="java.lang.String">` — iterates the `failures` list.
- `<bean:write name="failure">` — no `filter="true"`. The `failure` string represents a checklist item label, potentially user-defined.
- `<bean:write property="duration" name="preOpsEntry">` — no `filter="true"`. The `duration` field is typed as `java.time.LocalTime` in the bean, and `bean:write` calls `toString()` on it.
- `<bean:write property="comment" name="preOpsEntry">` — no `filter="true"`. The `comment` field is free-text user input.
- `request.getParameter("start_date")` / `request.getParameter("end_date")` — same JavaScript injection risk.

**JavaScript with security implications:**
Same `new Date("<%= DateUtil.stringToIsoNoTimezone(...) %>")` pattern. The `comment` field is free-text user input rendered directly in the HTML table.

**Existing tests for this JSP:** None found.

### Findings

**B05-32 | Severity: CRITICAL | preOpsReport.jsp — NullPointerException if `sessDateFormat` session attribute is null**
Same pattern as B05-12, B05-19, B05-25. No null check before `.replaceAll()`.

**B05-33 | Severity: CRITICAL | preOpsReport.jsp — NullPointerException in `DateUtil.stringToIsoNoTimezone()` on parse failure**
Same pattern as B05-20 and B05-26. Applies to both `start_date` and `end_date` parameters.

**B05-34 | Severity: HIGH | preOpsReport.jsp — Stored XSS via unencoded `comment` field**
`<bean:write property="comment" name="preOpsEntry">` outputs free-text comments entered by drivers without HTML encoding. Malicious script stored in the comment field is rendered to any admin viewing the pre-ops report.

**B05-35 | Severity: HIGH | preOpsReport.jsp — Stored XSS via unencoded `failure` checklist items**
`<bean:write name="failure">` outputs checklist failure labels without HTML encoding. If these labels are user-configurable (e.g., custom checklist questions), this is a stored XSS vector.

**B05-36 | Severity: HIGH | preOpsReport.jsp — JavaScript injection via unvalidated `start_date`/`end_date` request parameters**
Same pattern as B05-21, B05-29.

**B05-37 | Severity: HIGH | preOpsReport.jsp — `<bean:write>` for `unitName`, `manufacture`, `driverName`, `checkDateTime` lack HTML encoding**
Same pattern as B05-22, B05-30.

**B05-38 | Severity: MEDIUM | preOpsReport.jsp — `duration` field rendered via `LocalTime.toString()` without format specification**
`bean:write property="duration"` calls `toString()` on a `java.time.LocalTime` object. The format produced depends on the JVM's `LocalTime.toString()` implementation (ISO-8601 partial, e.g., `HH:mm` or `HH:mm:ss`). If the value is null, `bean:write` renders the string `"null"` visibly in the table. No test validates the rendered format.

**B05-39 | Severity: LOW | preOpsReport.jsp — Zero test coverage**
No test exists for this JSP or `PreOpsReportAction`.

---

## JSP 8 — reports/sessionreport.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/reports/sessionreport.jsp`

### Evidence

**Purpose:** Session report showing vehicle-driver session records with start and end times. Filterable by vehicle, driver, and date range. Data comes from `sessionReport` and filter options from `vehicles` and `drivers` attributes.

**Scriptlet blocks:**
```java
// Lines 4-6
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");

// Lines 99-113 — JavaScript date initialization
if (request.getParameter("start_date") != null) { ... }
if (request.getParameter("end_date") != null) { ... }
// Both embed DateUtil.stringToIsoNoTimezone output into JavaScript string literals
```

**EL / Struts tag expressions accessing request/session attributes:**
- `session.getAttribute("sessDateFormat")` — no null check.
- `<html:optionsCollection name="vehicles" value="id" label="name">` — reads `vehicles` request/session attribute.
- `<html:optionsCollection name="drivers" value="id" label="name">` — reads `drivers` request/session attribute.
- `<logic:iterate name="sessionReport" property="sessions" id="sessionEntry" type="com.bean.SessionBean">` — iterates `sessionReport`.
- `<bean:write property="unitName" name="sessionEntry">` — no `filter="true"`.
- `<bean:write property="driverName" name="sessionEntry">` — no `filter="true"`.
- `<bean:write property="startTime" name="sessionEntry">` — no `filter="true"`.
- `<bean:write property="finishTime" name="sessionEntry">` — no `filter="true"`.
- `request.getParameter("start_date")` / `request.getParameter("end_date")` — same JavaScript injection risk.

**JavaScript with security implications:**
Same `new Date("<%= DateUtil.stringToIsoNoTimezone(...) %>")` pattern as other report JSPs.

**Existing tests for this JSP:** None found.

### Findings

**B05-40 | Severity: CRITICAL | sessionreport.jsp — NullPointerException if `sessDateFormat` session attribute is null**
Same pattern as B05-12, B05-19, B05-25, B05-32. No null check before `.replaceAll()`.

**B05-41 | Severity: CRITICAL | sessionreport.jsp — NullPointerException in `DateUtil.stringToIsoNoTimezone()` on parse failure**
Same pattern as B05-20, B05-26, B05-33. Applies to both `start_date` and `end_date` parameters.

**B05-42 | Severity: HIGH | sessionreport.jsp — JavaScript injection via unvalidated `start_date`/`end_date` request parameters**
Same pattern as B05-21, B05-29, B05-36.

**B05-43 | Severity: HIGH | sessionreport.jsp — `<bean:write>` for `unitName`, `driverName`, `startTime`, `finishTime` lack HTML encoding (XSS)**
Same pattern as B05-22, B05-30, B05-37. All four session table columns are rendered without HTML encoding.

**B05-44 | Severity: MEDIUM | sessionreport.jsp — `vehicles` and `drivers` option collections rendered without encoding**
`<html:optionsCollection name="vehicles" value="id" label="name">` and the `drivers` equivalent render dropdown option labels from data objects. The Struts `html:optionsCollection` tag does apply HTML encoding to option labels by default, but the `value` attribute (the `id` field) encoding behavior depends on the Struts version and configuration. This should be verified; no test validates the rendered option markup.

**B05-45 | Severity: LOW | sessionreport.jsp — Zero test coverage**
No test exists for this JSP or `SessionReportAction`.

---

## JSP 9 — resetpass.jsp

**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/resetpass.jsp`

### Evidence

**Purpose:** Password reset page. Prompts the user for a verification code, new password, and confirmation password. Includes a hidden field carrying the `username` parameter from the request query string. Client-side validation is performed in JavaScript before form submission to `resetpass.do`.

**Scriptlet blocks:**
```java
// Line 2
String username = request.getParameter("username") == null ? "" : request.getParameter("username");
```
The `username` parameter is read from the HTTP request and stored in a local variable with an empty-string fallback for null. It is then emitted into the page at line 32:
```html
<input type="hidden" name="username" value="<%=username%>">
```

**EL / Struts tag expressions accessing request/session attributes:**
- `<html:errors>` — renders Struts action errors.
- `request.getParameter("username")` — direct query parameter access; the value is emitted unencoded into an HTML attribute.

**JavaScript with security implications:**
```javascript
function fnSubmit() {
    var npass = $('[name="npass"]').val();
    var rnpass = $('[name="rnpass"]').val();
    var code = $('[name="code"]').val();

    if (npass == "") {
        swal("Error", "New Password is required", "error");
    } else if (rnpass == "") {
        swal("Error", "Please Re-type New Password", "error");
    } else if (code == "") {
        swal("Error", "Confirmation Code", "error");   // BUG: message says "Confirmation Code" not "Verification Code is required"
    } else if (npass != rnpass) {
        swal("Error", "Password is not matched", "error");
    } else {
        $('#resetpassForm').submit();
    }
}
```
The "Update Password" button is an `<a href="#">` element with `onclick="fnSubmit();"`, not an `<input type="submit">`. This means the form is only submitted via JavaScript. If JavaScript is disabled, the page cannot function at all.

No password complexity or minimum length is enforced client-side or server-side (only presence is checked via `npass == ""`).

**Existing tests for this JSP:** None found.

### Findings

**B05-46 | Severity: CRITICAL | resetpass.jsp — Reflected XSS via unencoded `username` request parameter in hidden input**
`<input type="hidden" name="username" value="<%=username%>">` emits the raw `username` query parameter value into an HTML attribute without any HTML encoding. An attacker can craft a URL such as:
```
/resetpass.jsp?username="><script>alert(1)</script>
```
The injected value breaks out of the attribute and injects arbitrary script. This is a textbook reflected XSS vulnerability. No HTML-encoding (e.g., `ESAPI.encodeForHTML()`, `StringEscapeUtils.escapeHtml()`, or the Struts `<bean:write filter="true">` equivalent) is applied.

**B05-47 | Severity: HIGH | resetpass.jsp — No server-side password complexity enforcement**
Client-side validation in `fnSubmit()` only checks that `npass` and `rnpass` are non-empty and equal. There is no minimum length requirement, no complexity rule (uppercase, digits, special chars), and no check that the new password differs from the old one. Since the submit button is client-side (`<a onclick>`), these checks can be bypassed entirely by submitting the form programmatically. No test verifies that the server-side `ResetPasswordAction` enforces password policy.

**B05-48 | Severity: HIGH | resetpass.jsp — Form only submittable via JavaScript; no graceful degradation**
The "Update Password" element is `<a href="#" onclick="fnSubmit();">`, not a standard form submit button. With JavaScript disabled, there is no way to submit the form. There is also no `<noscript>` fallback. This is a usability and accessibility issue with security implications: if a browser security policy blocks inline scripts, password reset is completely broken.

**B05-49 | Severity: MEDIUM | resetpass.jsp — Verification code error message is misleading**
The error branch `else if (code == "")` displays `swal("Error", "Confirmation Code", "error")` — the message body reads only "Confirmation Code" (not "Verification Code is required" or equivalent), which provides no actionable guidance. This is a UX defect that could confuse users during the security-sensitive password reset flow.

**B05-50 | Severity: MEDIUM | resetpass.jsp — Verification code validated only for presence, not format**
`fnSubmit()` checks only `code == ""`. No format validation (e.g., numeric, fixed length) is performed client-side. Server-side format validation is untested.

**B05-51 | Severity: MEDIUM | resetpass.jsp — `username` is transported as a plain query parameter and hidden form field**
The username is passed in the URL query string (`goResetPass.do?action=getcode` links back to the page) and also in a hidden form field. Both are visible in browser history and server logs. In a password-reset flow the username exposure is a minor information leak but should be noted.

**B05-52 | Severity: LOW | resetpass.jsp — Resend link sends user to `goResetPass.do?action=getcode` with no CSRF protection**
The "Click Here to Resend" link is an `<a>` tag navigating via GET to `goResetPass.do?action=getcode`. This can be triggered by an image tag on a third-party page (CSRF). No CSRF token is present.

**B05-53 | Severity: LOW | resetpass.jsp — Zero test coverage**
No test exists for this JSP, `ResetPasswordAction`, or `GoResetPassAction` behavior.

---

## Cross-Cutting Findings

**B05-54 | Severity: CRITICAL | ALL report JSPs — Repeated `sessDateFormat` null-dereference pattern with no shared mitigation**
The identical unchecked `session.getAttribute("sessDateFormat").replaceAll(...)` scriptlet appears in gpsReport.jsp, impactReport.jsp, incidentReport.jsp, preOpsReport.jsp, and sessionreport.jsp. There is no shared utility method or include file that centralizes and null-guards this operation. A session expiry or misconfiguration affects all five report pages simultaneously. No test covers session-attribute absence for any of these pages.

**B05-55 | Severity: CRITICAL | ALL report JSPs — Repeated JavaScript injection pattern via `DateUtil.stringToIsoNoTimezone()` with no shared mitigation**
The pattern of embedding `DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), ...)` into JavaScript string literals appears in impactReport.jsp, incidentReport.jsp, preOpsReport.jsp, and sessionreport.jsp. The utility's parse-failure NPE risk and the absence of JavaScript-context encoding are systemic. No test exercises invalid date inputs against any of these pages.

**B05-56 | Severity: HIGH | ALL JSPs — Project-wide absence of JSP view-layer tests**
Zero test files in the test directory target any JSP file, any view rendering, or any request-attribute/session-attribute population. The four existing tests cover only calibration logic and ImpactUtil. The entire view layer — including all XSS-risk outputs, NPE-risk scriptlets, and client-side JavaScript behavior — is completely untested.

**B05-57 | Severity: HIGH | MULTIPLE JSPs — `<bean:write>` used without `filter="true"` throughout the codebase**
Across register.jsp, gpsReport.jsp, impactReport.jsp, incidentReport.jsp, preOpsReport.jsp, and sessionreport.jsp, `<bean:write>` tags consistently omit the `filter="true"` attribute. Struts 1.x `bean:write` does NOT HTML-encode output by default. This is a systemic pattern rather than an isolated oversight.

---

## Finding Summary Table

| ID | Severity | JSP | Description |
|----|----------|-----|-------------|
| B05-1 | MEDIUM | privacy.jsp | Client-side-only enforcement of privacy checkbox |
| B05-2 | LOW | privacy.jsp | Zero test coverage |
| B05-3 | HIGH | register.jsp | Unencoded `veh_id`/`attachment` in hidden inputs (XSS) |
| B05-4 | HIGH | register.jsp | NPE/JspException if `veh_id` or `attachment` attributes absent |
| B05-5 | MEDIUM | register.jsp | `fnback()` referenced but not defined in JSP |
| B05-6 | LOW | register.jsp | Zero test coverage |
| B05-7 | MEDIUM | registerSuccess.jsp | `document.onload` misuse; broken event handler pattern |
| B05-8 | MEDIUM | registerSuccess.jsp | Malformed HTML: `</html>` before `<script>` block |
| B05-9 | LOW | registerSuccess.jsp | Typo in message key `regsiter.create` |
| B05-10 | LOW | registerSuccess.jsp | Hardcoded redirect target `index.jsp` |
| B05-11 | LOW | registerSuccess.jsp | Zero test coverage |
| B05-12 | CRITICAL | gpsReport.jsp | NPE on `sessDateFormat` null |
| B05-13 | HIGH | gpsReport.jsp | `bean:write` unit id/name unencoded (XSS) |
| B05-14 | HIGH | gpsReport.jsp | `$('#site').val()` references non-existent element |
| B05-15 | MEDIUM | gpsReport.jsp | Hardcoded coordinates contradict comment (AU vs UK) |
| B05-16 | MEDIUM | gpsReport.jsp | JavaScript `custCd` variable never populated |
| B05-17 | LOW | gpsReport.jsp | `dateFormat` computed but never used |
| B05-18 | LOW | gpsReport.jsp | Zero test coverage |
| B05-19 | CRITICAL | impactReport.jsp | NPE on `sessDateFormat` null |
| B05-20 | CRITICAL | impactReport.jsp | NPE in `DateUtil.stringToIsoNoTimezone()` on parse failure |
| B05-21 | HIGH | impactReport.jsp | JavaScript injection via `start_date`/`end_date` parameters |
| B05-22 | HIGH | impactReport.jsp | `bean:write` manufacturer/unitName/driverName unencoded (XSS) |
| B05-23 | MEDIUM | impactReport.jsp | CSS injection via `getImpactLevelCSSColor()` |
| B05-24 | LOW | impactReport.jsp | Zero test coverage of JSP rendering |
| B05-25 | CRITICAL | incidentReport.jsp | NPE on `sessDateFormat` null |
| B05-26 | CRITICAL | incidentReport.jsp | NPE in `DateUtil.stringToIsoNoTimezone()` on parse failure |
| B05-27 | HIGH | incidentReport.jsp | Stored XSS via unencoded `description`/`location`/`witness` |
| B05-28 | HIGH | incidentReport.jsp | `signature`/`image` URLs in `href` unencoded (possible `javascript:` URI) |
| B05-29 | HIGH | incidentReport.jsp | JavaScript injection via `start_date`/`end_date` parameters |
| B05-30 | HIGH | incidentReport.jsp | Multiple `bean:write` outputs lack `filter="true"` |
| B05-31 | LOW | incidentReport.jsp | Zero test coverage |
| B05-32 | CRITICAL | preOpsReport.jsp | NPE on `sessDateFormat` null |
| B05-33 | CRITICAL | preOpsReport.jsp | NPE in `DateUtil.stringToIsoNoTimezone()` on parse failure |
| B05-34 | HIGH | preOpsReport.jsp | Stored XSS via unencoded `comment` field |
| B05-35 | HIGH | preOpsReport.jsp | Stored XSS via unencoded `failure` checklist items |
| B05-36 | HIGH | preOpsReport.jsp | JavaScript injection via `start_date`/`end_date` parameters |
| B05-37 | HIGH | preOpsReport.jsp | Multiple `bean:write` outputs lack `filter="true"` |
| B05-38 | MEDIUM | preOpsReport.jsp | `duration` rendered via `LocalTime.toString()`; null renders as "null" |
| B05-39 | LOW | preOpsReport.jsp | Zero test coverage |
| B05-40 | CRITICAL | sessionreport.jsp | NPE on `sessDateFormat` null |
| B05-41 | CRITICAL | sessionreport.jsp | NPE in `DateUtil.stringToIsoNoTimezone()` on parse failure |
| B05-42 | HIGH | sessionreport.jsp | JavaScript injection via `start_date`/`end_date` parameters |
| B05-43 | HIGH | sessionreport.jsp | `bean:write` session fields unencoded (XSS) |
| B05-44 | MEDIUM | sessionreport.jsp | `vehicles`/`drivers` option collection encoding not verified |
| B05-45 | LOW | sessionreport.jsp | Zero test coverage |
| B05-46 | CRITICAL | resetpass.jsp | Reflected XSS via unencoded `username` query parameter |
| B05-47 | HIGH | resetpass.jsp | No server-side password complexity enforcement |
| B05-48 | HIGH | resetpass.jsp | Form only submittable via JavaScript; no fallback |
| B05-49 | MEDIUM | resetpass.jsp | Misleading verification code error message |
| B05-50 | MEDIUM | resetpass.jsp | Verification code not format-validated |
| B05-51 | MEDIUM | resetpass.jsp | `username` exposed in URL and hidden field |
| B05-52 | LOW | resetpass.jsp | Resend link lacks CSRF protection |
| B05-53 | LOW | resetpass.jsp | Zero test coverage |
| B05-54 | CRITICAL | ALL reports | Repeated `sessDateFormat` null-dereference; no shared mitigation |
| B05-55 | CRITICAL | ALL reports | Repeated JavaScript injection pattern; no shared mitigation |
| B05-56 | HIGH | ALL JSPs | Project-wide absence of JSP view-layer tests |
| B05-57 | HIGH | MULTIPLE | `bean:write` without `filter="true"` is a systemic pattern |

---

*End of B05 Pass 2 Report — 57 findings across 9 JSP files.*
