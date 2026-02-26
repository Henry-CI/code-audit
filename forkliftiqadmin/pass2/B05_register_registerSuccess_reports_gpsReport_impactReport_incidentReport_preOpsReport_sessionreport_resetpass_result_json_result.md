# Pass 2 Test-Coverage Audit: JSP View Layer
**Audit ID:** B05
**Date:** 2026-02-26
**Auditor:** Agent B05
**Scope:** JSP view files — test-coverage gaps, view-layer security issues, untestable patterns

---

## Files Audited

1. `src/main/webapp/html-jsp/register.jsp`
2. `src/main/webapp/html-jsp/registerSuccess.jsp`
3. `src/main/webapp/html-jsp/reports/gpsReport.jsp`
4. `src/main/webapp/html-jsp/reports/impactReport.jsp`
5. `src/main/webapp/html-jsp/reports/incidentReport.jsp`
6. `src/main/webapp/html-jsp/reports/preOpsReport.jsp`
7. `src/main/webapp/html-jsp/reports/sessionreport.jsp`
8. `src/main/webapp/html-jsp/resetpass.jsp`
9. `src/main/webapp/html-jsp/result/json_result.jsp`

**Test directory:** `src/test/java/`

---

## Section 1: Reading Evidence

### 1.1 `register.jsp`

**Purpose:** New driver registration form. Collects `firstName`, `lastName`, `licence_no`, `expirydt`. Submits to `register.do` via POST. Used within the `fleetcheckDefinition` Tiles layout (tablet/kiosk flow, not the admin portal).

**Scriptlets (`<% %>`): none.** No raw Java scriptlets present.

**EL / Tag expressions:**
- Line 6: `<html:form action="register.do">` — Struts HTML form posting to `register.do`
- Line 8: `<bean:define id="veh_id" name="veh_id">` — reads request attribute `veh_id` into page scope
- Line 10: `<bean:write name="veh_id">` — writes `veh_id` into hidden input value attribute
- Line 11: `<bean:define id="attachment" name="attachment">` — reads request attribute `attachment` into page scope
- Line 13: `<bean:write name="attachment">` — writes `attachment` into hidden input value attribute
- Line 14: `<html:errors>` — renders action errors
- Lines 17–27: `<html:text>` fields for firstName, lastName, licence_no, expirydt — bound to `registerActionForm`

**Forms:** One form, `POST register.do`.

**JavaScript:**
- Lines 39–43: jQuery datepicker initialisation for `#datepicker` (expirydt field), format `dd/mm/yy`.

**Test directory search results:** No test file references `register.jsp`, `register.do`, `RegisterAction`, or `RegisterActionForm`.

---

### 1.2 `registerSuccess.jsp`

**Purpose:** Registration success/confirmation page. Shows a message that a verification link was sent. Counts down 10 seconds and redirects to `index.jsp`. Most original markup is commented out. Extends `loginDefinition` via Tiles (from `successRegisterDefinition`).

**Scriptlets:** None.

**EL / Tag expressions:**
- Line 32: `<html:form action="login.do">` — wraps the success message body in an (essentially no-op) form pointing to `login.do`
- Line 34: `<bean:message key="regsiter.create">` — i18n key (note typo in key name: `regsiter`)
- Line 38: `<bean:message key="register.info">` — i18n key
- Line 43: `<input type="button" onclick="redirect()">` — calls JavaScript redirect

**Forms:** One form, `POST login.do`. The form is decorative; no submit button is active (only a disabled download button and a JS-onclick home button).

**JavaScript (lines 52–75):**
- `document.onload = init()` — calls `init()` immediately (incorrect usage; should be `window.onload = init` without parentheses — the assignment will always execute init once at parse time)
- `setInterval(countDown, 1000)` — starts countdown
- `redirect()` navigates to hardcoded `"index.jsp"` (line 73)

**Test directory search results:** No test file references `registerSuccess.jsp` or `successRegisterDefinition`.

---

### 1.3 `reports/gpsReport.jsp`

**Purpose:** GPS live-map report page for admin portal. Renders a vehicle multi-select dropdown and a Google Maps canvas. Submits to `gpsreport.do`. Extends `adminDefinition` (requires authenticated session).

**Scriptlets:**
- Lines 4–7: Reads `sessDateFormat` from session and reformats it; reads `sessCompId` from session.

```
Line 5:  String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy","yy").replaceAll("M","m");
Line 6:  String custCd = (String) session.getAttribute("sessCompId");
```

**EL / Tag expressions:**
- Line 23: `<html:form action="gpsreport.do">` — POST form
- Lines 29–34: `<logic:notEmpty name="arrAdminUnit">` / `<logic:iterate name="arrAdminUnit">` — iterates vehicle list set by action
- Lines 31–32: `<bean:write property="id" name="unitRecord">` and `<bean:write property="name" name="unitRecord">` — renders unit id and name into option element

**Hidden input:**
- Line 51: `<input type="hidden" name="cust" id="cust" value="<%=custCd %>">` — emits `custCd` from session directly into HTML

**JavaScript (lines 54–72):**
- `custCd` is declared as empty string at the JS level (line 56), but the hidden input containing the real value is used by `fnRefresh()`.
- Hardcoded default coordinates: `-24.2761156,133.5912902` (Australian lat/long).
- `fnRefresh()` calls `initialize($('#cust').val(), $('#site').val())` — `$('#site')` is not defined anywhere in this file.

**Test directory search results:** No test file references `gpsReport.jsp`, `gpsreport.do`, or `GPSReportAction`.

---

### 1.4 `reports/impactReport.jsp`

**Purpose:** Impact event report page. Displays a filterable table of impact events grouped by unit/manufacturer. Submits to `impactreport.do`. Extends `adminDefinition`.

**Scriptlets:**
- Line 5: `String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll(...)` — no null guard
- Lines 87, 90: `<%= impactGroup.getEntries().size() %>` — direct scriptlet output into `rowspan` attribute
- Line 97: `<span style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;">` — scriptlet output into inline CSS
- Line 100: `<%= String.format(" (%.1fg)", impactEntry.getGForce()) %>` — scriptlet output into table cell
- Lines 115–116: Request parameter `start_date` passed to `DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), ...)` and output inside `new Date("...")` JS constructor
- Lines 119–120: Same pattern for `end_date`
- Line 123: `'<%= dateFormat %>'` — session-derived date format string output into JavaScript string

**EL / Tag expressions:**
- Lines 26–29: `<html:select property="manu_id">`, `<html:optionsCollection property="manufacturers">` — from action form
- Lines 33–36: `<html:select property="type_id">`, `<html:optionsCollection property="unitTypes">`
- Lines 42–47: `<html:select property="impact_level">` with hardcoded BLUE/AMBER/RED option values
- Lines 80–105: `<logic:iterate name="impactReport" property="groups">` and nested `<logic:iterate name="impactGroup" property="entries">` with `<bean:write>` for manufacturer, unitName, driverName, impactDateTime

**Forms:** One form, `POST impactreport.do`.

**Test directory search results:** No test file references `impactReport.jsp`, `impactreport.do`, or `ImpactReportAction`.

---

### 1.5 `reports/incidentReport.jsp`

**Purpose:** Incident report page. Displays a filterable table of incident entries with links to signature and image files. Submits to `incidentreport.do`. Extends `adminDefinition`.

**Scriptlets:**
- Line 5: `String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll(...)` — no null guard
- Lines 162–165: `request.getParameter("start_date")` passed to `DateUtil.stringToIsoNoTimezone(...)` and emitted as JS `new Date(...)` argument
- Lines 170–174: Same for `end_date`
- Line 176: `'<%= dateFormat %>'` into JavaScript

**EL / Tag expressions:**
- Lines 96–149: `<logic:iterate name="incidentReport" property="entries">` with `<bean:write>` for unitName, manufacture, driverName, description, event_time, injureType, location, witness
- Lines 132–137: `href="<bean:write property="signature" name="incidentEntry"/>"` — signature URL written directly into href attribute
- Lines 140–145: `href="<bean:write property="image" name="incidentEntry"/>"` — image URL written directly into href attribute

**Forms:** One form, `POST incidentreport.do`.

**Note:** The breadcrumb link at line 11 has a trailing space in the URL: `href="incidentreport.do "`.

**Test directory search results:** No test file references `incidentReport.jsp`, `incidentreport.do`, or `IncidentReportAction`.

---

### 1.6 `reports/preOpsReport.jsp`

**Purpose:** Pre-operations checklist completion report. Displays filterable table of pre-ops entries including failures list, duration, and comments. Submits to `preopsreport.do`. Extends `adminDefinition`.

**Scriptlets:**
- Line 5: `String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll(...)` — no null guard
- Lines 107–111: `request.getParameter("start_date")` passed to `DateUtil.stringToIsoNoTimezone(...)` and emitted as JS `new Date(...)` argument
- Lines 115–119: Same for `end_date`
- Lines 121–122: `'<%= dateFormat %>'` into JavaScript

**EL / Tag expressions:**
- Lines 78–95: `<logic:iterate name="preOpsReport" property="entries">` with `<bean:write>` for unitName, manufacture, driverName, checkDateTime, duration, comment
- Lines 86–88: Nested `<logic:iterate id="failure" name="preOpsEntry" property="failures">` with `<bean:write name="failure">` — failure strings rendered into list items

**Forms:** One form, `POST preopsreport.do`. Includes a `window.print()` button (line 55).

**Note:** The breadcrumb link at line 11 has a trailing space in the URL: `href="preopsreport.do "`.

**Test directory search results:** No test file references `preOpsReport.jsp`, `preopsreport.do`, or `PreOpsReportAction`.

---

### 1.7 `reports/sessionreport.jsp`

**Purpose:** Driver session report. Displays a filterable table of forklift sessions with vehicle, driver, start time, and finish time. Submits to `sessionreport.do`. Extends `adminDefinition`.

**Scriptlets:**
- Line 5: `String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll(...)` — no null guard
- Lines 100–104: `request.getParameter("start_date")` passed to `DateUtil.stringToIsoNoTimezone(...)` and emitted as JS `new Date(...)` argument
- Lines 108–112: Same for `end_date`
- Lines 114–115: `'<%= dateFormat %>'` into JavaScript

**EL / Tag expressions:**
- Lines 25–28: `<html:select property="vehicle_id">` with `<html:optionsCollection name="vehicles">` — uses named bean, not form property
- Lines 33–36: `<html:select property="driver_id">` with `<html:optionsCollection name="drivers">` — uses named bean
- Lines 78–88: `<logic:iterate name="sessionReport" property="sessions">` with `<bean:write>` for unitName, driverName, startTime, finishTime

**Forms:** One form, `POST sessionreport.do`.

**Note:** The breadcrumb link at line 11 has a trailing space in the URL: `href="sessionreport.do "`.

**Test directory search results:** No test file references `sessionreport.jsp`, `sessionreport.do`, or `SessionReportAction`.

---

### 1.8 `resetpass.jsp`

**Purpose:** Password reset form. Accepts a verification code, new password, and confirm password. Submits to `resetpass.do` via POST. Uses `resetPassDefinition` Tiles layout (extends `loginDefinition` — no session required). This page is intentionally pre-authentication.

**Scriptlets:**
- Line 2: `String username = request.getParameter("username") == null ? "" : request.getParameter("username");` — reads `username` from query parameter
- Line 32: `value="<%=username%>"` — emits the username directly into a hidden input value

**EL / Tag expressions:**
- Line 14: `<html:errors>` — renders action errors
- Line 16: `<form action="resetpass.do" method="post">` — plain HTML form (not `html:form`)

**Forms:** One plain HTML form, `POST resetpass.do`.

**JavaScript (lines 42–68):**
- Client-side validation: checks `npass`, `rnpass`, `code` for empty; checks `npass == rnpass`. Uses `swal()` (SweetAlert) for error dialogs.
- No server-side equivalent of password length/complexity validation observable in the view.

**`resetpass.do` excluded from auth filter:** Confirmed in `PreFlightActionServlet.excludeFromFilter()` — `resetpass.do` returns `false` meaning it is **excluded from** session checks, which is correct for a pre-auth reset flow.

**Test directory search results:** No test file references `resetpass.jsp`, `resetpass.do`, or `ResetPasswordAction`.

---

### 1.9 `result/json_result.jsp`

**Purpose:** JSON response fragment for the `sendMail` action (`/sendMail.do` → `AdminSendMailAction`). Reads a `result` request attribute and outputs a hardcoded JSON string. Used via Tiles `jsonResultDefinition` (direct path, not extending another definition).

**Scriptlets (entire file is scriptlet + output):**
- Lines 1–11: Reads `request.getAttribute("result")`, compares case-insensitively to `"success"`, branches on two hardcoded JSON string literals.
- Line 12: `<%=message %>` — raw output of the constructed JSON string

**EL / Tag expressions:** None.

**Forms:** None.

**No `<%@ page contentType="application/json" %>` declaration** — the response MIME type defaults to `text/html`.

**Test directory search results:** No test file references `json_result.jsp`, `jsonResultDefinition`, or `AdminSendMailAction`.

---

## Section 2: Test Coverage Summary

```
File                             | Action Class              | Test File Found
---------------------------------|---------------------------|----------------
register.jsp                     | RegisterAction            | NONE
registerSuccess.jsp              | (forward from register)   | NONE
reports/gpsReport.jsp            | GPSReportAction           | NONE
reports/impactReport.jsp         | ImpactReportAction        | NONE
reports/incidentReport.jsp       | IncidentReportAction      | NONE
reports/preOpsReport.jsp         | PreOpsReportAction        | NONE
reports/sessionreport.jsp        | SessionReportAction       | NONE
resetpass.jsp                    | ResetPasswordAction       | NONE
result/json_result.jsp           | AdminSendMailAction       | NONE
```

All 9 JSP files and their corresponding action classes have **zero test coverage** in the test directory. The test directory contains only 4 files, all focused on the calibration/impact utility layer.

---

## Section 3: Findings

---

### B05-1
**Severity:** CRITICAL
**File:** `reports/impactReport.jsp`, `reports/incidentReport.jsp`, `reports/preOpsReport.jsp`, `reports/sessionreport.jsp`
**Lines:** impactReport.jsp:116, 120; incidentReport.jsp:164, 172; preOpsReport.jsp:109, 117; sessionreport.jsp:102, 110
**Title:** Reflected XSS — unescaped request parameters injected into JavaScript string context

**Evidence:**
In all four report JSPs the `start_date` and `end_date` request parameters are read and passed directly into `DateUtil.stringToIsoNoTimezone()`, then the return value is emitted into a JavaScript `new Date("...")` constructor without any HTML or JavaScript escaping:

```jsp
// impactReport.jsp line 116
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>");
```

`DateUtil.stringToIsoNoTimezone()` calls `DateUtil.stringToDate()`. When parsing fails (malformed input), `stringToDate()` catches `ParseException`, sets `date = null`, and returns `null`. `stringToIsoNoTimezone()` then calls `df.format(null)`, which throws `NullPointerException`. However, if the method were to be modified, or if any other path returns without throwing, the raw parameter string could reach the output. More critically: if `start_date` is a string like `"); alert(1); //`, the JSP emits:

```js
start_date = new Date(""); alert(1); //");
```

Because the parameter is placed inside a JavaScript string literal delimited by `"`, an attacker who can inject `"` can break out of the string and execute arbitrary JavaScript. While the current implementation would throw a NullPointerException (500 error) for non-date values and thus may not render the page, this pattern is fragile. A future refactor that makes `stringToIsoNoTimezone` return a safe default on bad input, or any path that passes a date-like string containing `"`, would be directly exploitable. The structural XSS sink is present and must be treated as CRITICAL.

These pages are under `adminDefinition` (authenticated users only), but XSS in authenticated-only pages is still exploitable for session hijacking, CSRF bypass, and admin credential theft.

---

### B05-2
**Severity:** HIGH
**File:** `resetpass.jsp`
**Line:** 2, 32
**Title:** Reflected XSS — unescaped `username` request parameter in hidden input value

**Evidence:**
```jsp
Line 2:  String username = request.getParameter("username") == null ? "" : request.getParameter("username");
Line 32: <input type="hidden" name="username" value="<%=username%>">
```

The `username` parameter from the query string is read without sanitisation and written directly into an HTML attribute value without HTML-encoding. An attacker who constructs a link such as:

```
/resetpass.do?username="><script>alert(document.cookie)</script>
```

can inject arbitrary HTML and JavaScript into the page. Because `resetpass.do` is intentionally excluded from the session authentication filter (pre-auth flow), this endpoint is reachable by unauthenticated users, making the attack surface unrestricted. A phishing email containing such a link could be used to steal credentials or install malware on victim browsers.

---

### B05-3
**Severity:** HIGH
**File:** `reports/gpsReport.jsp`, `reports/impactReport.jsp`, `reports/incidentReport.jsp`, `reports/preOpsReport.jsp`, `reports/sessionreport.jsp`
**Line:** gpsReport.jsp:5; impactReport.jsp:5; incidentReport.jsp:5; preOpsReport.jsp:5; sessionreport.jsp:5
**Title:** NullPointerException on null `sessDateFormat` session attribute — no null guard

**Evidence:**
All five report JSPs execute the following pattern at the top of the file:
```jsp
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```

`session.getAttribute("sessDateFormat")` returns `null` if the session exists but the attribute was never set (e.g., if the user session was partially initialised, or after an application restart with sticky sessions). Calling `.replaceAll(...)` on `null` throws a `NullPointerException`. This will result in a 500 error and an unhandled exception reaching the user.

`sessDateFormat` is only set in two places: `AdminSettingsAction.java:57` and `CompanySessionSwitcher.java:32`. The `CompanySessionSwitcher` is called from `LoginAction`, so a correctly logged-in user will have it set. However there is no defensive null check at the point of use in the view, making this a single point of failure with no graceful fallback.

---

### B05-4
**Severity:** HIGH
**File:** `reports/gpsReport.jsp`
**Line:** 5–6, 51
**Title:** Session attribute `sessCompId` unguarded and emitted directly into HTML

**Evidence:**
```jsp
Line 6:  String custCd = (String) session.getAttribute("sessCompId");
Line 51: <input type="hidden" name="cust" id="cust" value="<%=custCd %>">
```

`sessCompId` is cast and immediately used without a null check. If the session attribute is null, `custCd` is `null` and line 51 renders `value="null"` in the HTML. More importantly, this value is a company identifier placed in a hidden form field that is subsequently sent to the server-side GPS initialisation function and used in AJAX calls. There is no server-side revalidation visible in this view that the `cust` value matches the logged-in session's actual company — a user who manipulates this hidden field could potentially query GPS data for other companies.

---

### B05-5
**Severity:** HIGH
**File:** `reports/impactReport.jsp`
**Lines:** 87, 90, 97, 100
**Title:** Untestable business logic in scriptlets — inline Java in view layer

**Evidence:**
```jsp
Line 87:  <td rowspan="<%= impactGroup.getEntries().size() %>">
Line 90:  <td rowspan="<%= impactGroup.getEntries().size() %>">
Line 97:  <span style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;">
Line 100: <%= String.format(" (%.1fg)", impactEntry.getGForce()) %>
```

These scriptlets call bean methods directly in the view. The `rowspan` calculation (`getEntries().size()`), the CSS colour derivation (`getImpactLevelCSSColor()`), and the g-force formatting (`String.format("%.1fg", getGForce())`) are all business/presentation logic embedded in the view. None of this can be covered by unit tests targeting the JSP. The logic can only be exercised by integration tests with a running container. Given the project has no integration test infrastructure evident in the test directory, this logic is effectively untestable.

---

### B05-6
**Severity:** MEDIUM
**File:** `result/json_result.jsp`
**Lines:** 1–12
**Title:** Missing `Content-Type: application/json` declaration — MIME-type sniffing risk

**Evidence:**
```jsp
<%
String result = request.getAttribute("result") == null ? "" : request.getAttribute("result").toString();
if (result.equalsIgnoreCase("success")) {
    message = "{ \"status\":\"success_close\", \"message\":\"Mail has been sent\" }";
} else {
    message = "{ \"status\":\"error\", \"message\":\"Sending Failed.\" }";
}
%>
<%=message %>
```

There is no `<%@ page contentType="application/json" %>` directive. The response will be served as `text/html` (the JSP default). Clients consuming this endpoint as JSON rely on the data format rather than the declared content type. Browsers may MIME-sniff the response. Additionally, callers cannot rely on content-type negotiation. Internet Explorer and older Edge perform MIME sniffing for `text/html` responses that look like scripts, which could be a vector if the message content were user-controlled.

The message content is currently hardcoded (not user-controlled), so XSS is not present here, but the missing content-type is a structural defect.

---

### B05-7
**Severity:** MEDIUM
**File:** `register.jsp`
**Lines:** 8–13
**Title:** `<bean:define>` / `<bean:write>` of request-scoped attributes without null guard — potential JspException

**Evidence:**
```jsp
Line 8:  <bean:define id="veh_id" name="veh_id"></bean:define>
Line 10: value='<bean:write name="veh_id"></bean:write>'
Line 11: <bean:define id="attachment" name="attachment"></bean:define>
Line 13: value='<bean:write name="attachment"></bean:write>'
```

`<bean:define name="veh_id">` resolves the bean named `veh_id` from page/request/session/application scope in that order. If the `RegisterAction` does not place `veh_id` in request scope (e.g., initial GET navigation to the register page without a prior action invocation), Struts will throw a `JspException: Cannot find bean veh_id in any scope`. This results in a 500 error rather than a graceful form with an empty hidden field. The action code confirms `veh_id` and `attachment` are only set on the failure forward path (`request.setAttribute("veh_id", ...)`) but not on an initial GET.

---

### B05-8
**Severity:** MEDIUM
**File:** `resetpass.jsp`
**Lines:** 42–68
**Title:** Password validation logic is view-only (client-side only) — untestable and bypassable

**Evidence:**
```javascript
if (npass == "") { swal("Error", "New Password is required", "error"); }
else if (rnpass == "") { swal("Error", "Please Re-type New Password", "error"); }
else if (code == "") { swal("Error", "Confirmation Code", "error"); }
else if (npass != rnpass) { swal("Error", "Password is not matched", "error"); }
else { $('#resetpassForm').submit(); }
```

All field validation (required checks, password match) is implemented exclusively in JavaScript in the view. There is no server-side equivalent validation in `ResetPasswordAction` or `ResetPassActionForm` for these constraints visible in the codebase. An attacker can bypass all validation by submitting the form directly (e.g., `curl` or a crafted POST), sending empty passwords or mismatched passwords directly to `resetpass.do`. Since this endpoint is pre-auth (excluded from the session filter), it is reachable without logging in. This is untestable as a JSP and has no corresponding unit test.

---

### B05-9
**Severity:** MEDIUM
**File:** `registerSuccess.jsp`
**Line:** 73
**Title:** Hardcoded redirect URL — inflexible and potentially misdirected

**Evidence:**
```javascript
function redirect() {
    var url = "index.jsp";
    location.replace(url);
}
```

The redirect destination after registration success is hardcoded as `"index.jsp"` — a relative URL. This bypasses any server-side routing configuration (Struts action mappings, Tiles definitions). If the deployment context changes, or if the application is deployed under a non-root context path, this relative redirect may land on the wrong page. Additionally, the redirect is purely client-side (JavaScript) with no server-side redirect fallback for users with JavaScript disabled.

---

### B05-10
**Severity:** MEDIUM
**File:** `reports/gpsReport.jsp`
**Lines:** 57–60
**Title:** Hardcoded geographic coordinates (Australia) — misconfiguration risk for non-AU deployments

**Evidence:**
```javascript
var defaultLoc = "-24.2761156,133.5912902"; //UK- 55.378051, -3.435973
var defaultLat = "-24.2761156"; //AU
var defaultLong = "133.5912902";
```

The default map centre is hardcoded to the centre of Australia. A commented-out UK coordinate set exists but is not active. For non-Australian customers, the GPS map will open centered on Australia, providing a degraded user experience and suggesting this is not configurable per-tenant. This is not a security finding but is a significant functional gap that cannot be tested via unit tests.

---

### B05-11
**Severity:** MEDIUM
**File:** `reports/incidentReport.jsp`
**Lines:** 132–145
**Title:** Unvalidated URL written to `href` attributes — potential open redirect or javascript: URI injection

**Evidence:**
```jsp
Line 133: href="<bean:write property="signature" name="incidentEntry"/>"
Line 141: href="<bean:write property="image" name="incidentEntry"/>"
```

The `signature` and `image` properties of `IncidentReportEntryBean` are written directly into `href` attributes without validation or sanitisation. If these values originate from user-uploaded data or a compromised data source, they could contain `javascript:` URIs (which would execute JavaScript on click) or external URLs (open redirect). `<bean:write>` performs HTML escaping of `<`, `>`, `&`, and `"` by default in Struts, which neutralises most HTML injection. However, `<bean:write>` does **not** validate URL scheme — a `javascript:alert(1)` value would pass through HTML-escaped as a valid `href`, and clicking it would execute the script in the user's browser. This is a stored XSS vector if the data source is attacker-influenced.

---

### B05-12
**Severity:** LOW
**File:** `registerSuccess.jsp`
**Line:** 54
**Title:** `document.onload` assignment pattern executes `init()` immediately — countdown always starts twice

**Evidence:**
```javascript
document.onload = init();
```

`init()` is called immediately (the `()` executes the function and assigns its return value, `undefined`, to `document.onload`). The `setInterval` inside `init()` starts immediately at page parse time. `document.onload` is also not a standard event — the intended pattern is `window.onload = init` (without parentheses) or `window.addEventListener('load', init)`. The practical effect is that the countdown starts before the DOM is ready, which is usually harmless but is incorrect and untestable.

---

### B05-13
**Severity:** LOW
**File:** `reports/incidentReport.jsp`, `reports/preOpsReport.jsp`, `reports/sessionreport.jsp`
**Lines:** incidentReport.jsp:11; preOpsReport.jsp:11; sessionreport.jsp:11
**Title:** Trailing whitespace in breadcrumb `href` attributes

**Evidence:**
```jsp
// incidentReport.jsp
<a href="incidentreport.do ">Incident Report</a>
// preOpsReport.jsp
<a href="preopsreport.do ">Pre-ops Completed Today</a>
// sessionreport.jsp
<a href="sessionreport.do ">Session Report</a>
```

All three breadcrumb links have a trailing space in the URL. Most browsers will trim the space before requesting, but it is technically non-conforming and may cause failures in strict URL processing environments or automated tests.

---

### B05-14
**Severity:** LOW
**File:** `reports/gpsReport.jsp`
**Line:** 66
**Title:** Reference to undefined jQuery selector `$('#site')` in `fnRefresh()`

**Evidence:**
```javascript
function fnRefresh() {
    initialize($('#cust').val(), $('#site').val());
    ...
}
```

`$('#site')` refers to an element with id `site` which does not exist anywhere in `gpsReport.jsp` or its includes. This will silently pass `undefined` (or an empty string from `.val()`) as the `site` parameter to `initialize()`. This untested dead-code/broken-reference indicates the GPS filter functionality is incomplete.

---

### B05-15
**Severity:** INFO
**File:** All 9 files
**Title:** No test coverage exists for any audited JSP or its corresponding action class

**Evidence:**
The test directory contains exactly 4 files:
- `UnitCalibrationImpactFilterTest.java`
- `UnitCalibrationTest.java`
- `UnitCalibratorTest.java`
- `ImpactUtilTest.java`

A grep across the entire test directory for the names `register`, `gpsReport`, `impactReport`, `incidentReport`, `preOpsReport`, `sessionreport`, `resetpass`, `json_result`, `RegisterAction`, `GPSReportAction`, `ImpactReportAction`, `IncidentReportAction`, `PreOpsReportAction`, `SessionReportAction`, `ResetPasswordAction`, `AdminSendMailAction`, `register.do`, `gpsreport.do`, `impactreport.do`, `incidentreport.do`, `preopsreport.do`, `sessionreport.do`, `resetpass.do` returns no results.

JSPs are inherently difficult to unit-test. However the corresponding action classes, DAO interactions, and bean transformation logic are all equally untested.

---

### B05-16
**Severity:** INFO
**File:** `registerSuccess.jsp`
**Line:** 34
**Title:** Typo in i18n message key `regsiter.create`

**Evidence:**
```jsp
<h2>&nbsp;<bean:message key="regsiter.create"></bean:message></h2>
```

The key `regsiter.create` is a misspelling of `register.create`. If the properties file uses the correct spelling, this key lookup will silently fall back to the key name itself or throw a missing-resource error depending on Struts configuration. This is a display defect.

---

## Section 4: Summary Table

| ID     | Severity | File(s)                                              | Title                                                                          |
|--------|----------|------------------------------------------------------|--------------------------------------------------------------------------------|
| B05-1  | CRITICAL | impactReport, incidentReport, preOpsReport, sessionreport | Reflected XSS — unescaped request params in JS string context             |
| B05-2  | HIGH     | resetpass.jsp                                        | Reflected XSS — unescaped `username` param in hidden input value               |
| B05-3  | HIGH     | gpsReport, impactReport, incidentReport, preOpsReport, sessionreport | NPE on null `sessDateFormat` — no null guard                    |
| B05-4  | HIGH     | gpsReport.jsp                                        | `sessCompId` unguarded; emitted to HTML; no server-side revalidation           |
| B05-5  | HIGH     | impactReport.jsp                                     | Untestable business logic in scriptlets (rowspan, CSS color, g-force format)   |
| B05-6  | MEDIUM   | result/json_result.jsp                               | Missing `Content-Type: application/json` declaration                           |
| B05-7  | MEDIUM   | register.jsp                                         | `bean:define` on unguarded request attributes — JspException on initial GET    |
| B05-8  | MEDIUM   | resetpass.jsp                                        | Password validation is client-side only — bypassable and untestable            |
| B05-9  | MEDIUM   | registerSuccess.jsp                                  | Hardcoded redirect URL `index.jsp`                                             |
| B05-10 | MEDIUM   | gpsReport.jsp                                        | Hardcoded Australian coordinates — non-configurable per tenant                 |
| B05-11 | MEDIUM   | incidentReport.jsp                                   | Unvalidated DB-sourced URLs in `href` — stored XSS risk via `javascript:` URI  |
| B05-12 | LOW      | registerSuccess.jsp                                  | `document.onload = init()` — incorrect event assignment, always executes early |
| B05-13 | LOW      | incidentReport, preOpsReport, sessionreport          | Trailing whitespace in breadcrumb `href` attributes                            |
| B05-14 | LOW      | gpsReport.jsp                                        | Reference to undefined jQuery selector `$('#site')` in `fnRefresh()`           |
| B05-15 | INFO     | All 9 files                                          | Zero test coverage for all JSPs and corresponding action classes               |
| B05-16 | INFO     | registerSuccess.jsp                                  | Typo in i18n key `regsiter.create`                                             |
