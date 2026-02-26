# Pass 3 Documentation Audit — Agent B05
**Date:** 2026-02-26
**Auditor:** B05
**Files Audited:** register.jsp, registerSuccess.jsp, reports/gpsReport.jsp, reports/impactReport.jsp, reports/incidentReport.jsp, reports/preOpsReport.jsp, reports/sessionreport.jsp, resetpass.jsp, result/json_result.jsp

---

## Reading Evidence

---

### 1. register.jsp
**Path:** `src/main/webapp/html-jsp/register.jsp`
**Purpose:** New driver registration form. Collects first name, last name, licence number, and expiry date for a new driver. Submits to `register.do`. Hidden fields pass `veh_id` and `attachment` from bean scope.

**JSP Scriptlet Blocks (`<% %>`):**
- None present.

**JSP Expression Blocks (`<%= %>`):**
- None present.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`

**HTML Form `action` Attributes:**
- Line 6: `action="register.do"` (method="post")

**Session Attribute Accesses:**
- None directly in this file (session access delegated to included lib or action).

**Significant JavaScript Functions Defined:**
- Lines 39–43: Anonymous jQuery document-ready function initialising `#datepicker` with `dateFormat: 'dd/mm/yy'`.
- (References `fnback()` via onclick at line 29, but that function is not defined in this file — presumably defined in the included lib.)

---

### 2. registerSuccess.jsp
**Path:** `src/main/webapp/html-jsp/registerSuccess.jsp`
**Purpose:** Post-registration success page. Informs the user that a verification link was sent to their email, displays a 10-second countdown, then redirects to `index.jsp`. Renders a login-style layout with disabled download button and active home button.

**JSP Scriptlet Blocks (`<% %>`):**
- None present (no scriptlet code).

**JSP Expression Blocks (`<%= %>`):**
- None present.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`

**HTML Form `action` Attributes:**
- Line 32: `action="login.do"` (method="post") — form wraps the success message content; no actual login submission occurs on this page.

**Session Attribute Accesses:**
- None.

**Significant JavaScript Functions Defined:**
- Lines 56–58: `init()` — calls `setInterval(countDown, 1000)` to start the countdown.
- Lines 60–68: `countDown()` — decrements `time` each second, updates `#timer` element, calls `redirect()` when reaches 0.
- Lines 71–75: `redirect()` — replaces current location with `index.jsp`.

**Commented-out Code:**
- Lines 2–20: Large block of HTML and JSP comments enclosing an entire earlier layout (div structure with `span8`, `containerL`, `login-form`). Includes commented-out `<bean:message>` calls and button elements. No explanation for why they were retained.

---

### 3. reports/gpsReport.jsp
**Path:** `src/main/webapp/html-jsp/reports/gpsReport.jsp`
**Purpose:** GPS Report page. Displays a map canvas (`#map_canvas`) allowing the admin to select one or more vehicles and view their GPS positions. Reads customer ID and date format from session; passes customer code to the map initialisation function.

**JSP Scriptlet Blocks (`<% %>`):**
- Lines 4–7: Reads `sessDateFormat` from session and reformats it (replaces `yyyy`→`yy`, `M`→`m`); reads `sessCompId` from session into `custCd`.

**JSP Expression Blocks (`<%= %>`):**
- Line 51: `<%=custCd %>` — renders the customer code into a hidden input's `value` attribute.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**`<%@ page import %>` Directives:**
- Line 2: `<%@ page import="com.util.DateUtil" %>` (imported but `DateUtil` is not used anywhere in this file).

**HTML Form `action` Attributes:**
- Line 23: `action="gpsreport.do"` (method="POST")

**Session Attribute Accesses:**
- Line 5: `session.getAttribute("sessDateFormat")`
- Line 6: `session.getAttribute("sessCompId")`

**Significant JavaScript Functions Defined:**
- Lines 64–70: `fnRefresh()` — calls `initialize()` with customer and site values; conditionally calls `application.getGotToZonesControl()`.

**JavaScript Variables / Notable Values:**
- Line 57: `var defaultLoc = "-24.2761156,133.5912902"` — hard-coded default map coordinates with inline comment `//UK- 55.378051, -3.435973`.
- Lines 58–59: `var defaultLat` and `var defaultLong` — same coordinates, commented as `//AU`.

---

### 4. reports/impactReport.jsp
**Path:** `src/main/webapp/html-jsp/reports/impactReport.jsp`
**Purpose:** Impact Report page. Displays a filterable table of forklift impact events grouped by manufacturer/unit, with driver name, timestamp, and a colour-coded g-force severity indicator (BLUE/AMBER/RED). Includes date range pickers and dropdowns for manufacturer, unit type, and impact level.

**JSP Scriptlet Blocks (`<% %>`):**
- Lines 4–6: Reads `sessDateFormat` from session and reformats it.
- Lines 115–117: Conditional — if `start_date` request parameter is not null, emits JS to set `start_date` variable.
- Lines 119–121: Conditional — if `end_date` request parameter is not null, emits JS to set `end_date` variable.

**JSP Expression Blocks (`<%= %>`):**
- Line 87: `<%= impactGroup.getEntries().size() %>` — `rowspan` for manufacturer cell.
- Line 90: `<%= impactGroup.getEntries().size() %>` — `rowspan` for unit name cell.
- Line 97: `<%= impactEntry.getImpactLevelCSSColor() %>` — CSS background colour for impact level indicator.
- Line 100: `<%= String.format(" (%.1fg)", impactEntry.getGForce()) %>` — formatted g-force display value.
- Line 116: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>` — converts date string for JS Date constructor.
- Line 120: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>` — same for end date.
- Line 123: `<%= dateFormat %>` — emits reformatted date format string into JS.
- Line 124: `<%= dateFormat %>` — same.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML Form `action` Attributes:**
- Line 22: `action="impactreport.do"` (method="POST")

**Session Attribute Accesses:**
- Line 5: `session.getAttribute("sessDateFormat")`
- Line 116: `(String) session.getAttribute("sessDateFormat")` (inside expression, within scriptlet block)
- Line 120: `(String) session.getAttribute("sessDateFormat")` (same pattern)

**Significant JavaScript Functions Defined:**
- None explicitly named. One anonymous jQuery document-ready function (lines 111–125) initialises date pickers.

---

### 5. reports/incidentReport.jsp
**Path:** `src/main/webapp/html-jsp/reports/incidentReport.jsp`
**Purpose:** Incident Report page. Displays a filterable table of incident records with fields for unit, manufacturer, driver, description, time, near-miss flag, incident flag, injury flag, injury type, location, witness, signature (lightbox), and image (lightbox). Date range and manufacturer/type dropdowns for filtering.

**JSP Scriptlet Blocks (`<% %>`):**
- Lines 4–6: Reads `sessDateFormat` from session and reformats it.
- Lines 161–167: Conditional — if `start_date` not null, emits JS to set `start_date`.
- Lines 169–175: Conditional — if `end_date` not null, emits JS to set `end_date`.

**JSP Expression Blocks (`<%= %>`):**
- Line 164: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>` — converts start date for JS.
- Line 172: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>` — converts end date for JS.
- Line 176: `<%= dateFormat %>` — emits date format into JS.
- Line 177: `<%= dateFormat %>` — same.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML Form `action` Attributes:**
- Line 22: `action="incidentreport.do"` (method="POST")

**Session Attribute Accesses:**
- Line 5: `session.getAttribute("sessDateFormat")`
- Line 164: `(String) session.getAttribute("sessDateFormat")`
- Line 172: `(String) session.getAttribute("sessDateFormat")`

**Significant JavaScript Functions Defined:**
- None explicitly named. One anonymous jQuery document-ready function (lines 157–182) sets up date pickers and disables keyboard input on datepicker text fields via `keydown` handler returning false.

---

### 6. reports/preOpsReport.jsp
**Path:** `src/main/webapp/html-jsp/reports/preOpsReport.jsp`
**Purpose:** Pre-Operations (pre-ops) Report page. Displays a filterable table of pre-shift inspection completions, including unit name, manufacturer, driver, check date/time, list of failed questions, duration, and comments. Includes a print button.

**JSP Scriptlet Blocks (`<% %>`):**
- Lines 4–6: Reads `sessDateFormat` from session and reformats it.
- Lines 106–112: Conditional — if `start_date` not null, emits JS to set `start_date`.
- Lines 114–120: Conditional — if `end_date` not null, emits JS to set `end_date`.

**JSP Expression Blocks (`<%= %>`):**
- Line 109: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>` — converts start date for JS.
- Line 117: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>` — converts end date for JS.
- Line 121: `<%= dateFormat %>` — emits date format.
- Line 122: `<%= dateFormat %>` — same.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML Form `action` Attributes:**
- Line 22: `action="preopsreport.do"` (method="POST")

**Session Attribute Accesses:**
- Line 5: `session.getAttribute("sessDateFormat")`
- Line 109: `(String) session.getAttribute("sessDateFormat")`
- Line 117: `(String) session.getAttribute("sessDateFormat")`

**Significant JavaScript Functions Defined:**
- None explicitly named. One anonymous jQuery document-ready function (lines 102–123) initialises date pickers.

---

### 7. reports/sessionreport.jsp
**Path:** `src/main/webapp/html-jsp/reports/sessionreport.jsp`
**Purpose:** Session Report page. Lists forklift operator sessions (vehicle, driver, start time, finish time) with filtering by vehicle, driver, and date range.

**JSP Scriptlet Blocks (`<% %>`):**
- Lines 4–6: Reads `sessDateFormat` from session and reformats it.
- Lines 99–105: Conditional — if `start_date` not null, emits JS to set `start_date`.
- Lines 107–113: Conditional — if `end_date` not null, emits JS to set `end_date`.

**JSP Expression Blocks (`<%= %>`):**
- Line 102: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>` — converts start date.
- Line 110: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>` — converts end date.
- Line 114: `<%= dateFormat %>` — emits date format.
- Line 115: `<%= dateFormat %>` — same.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML Form `action` Attributes:**
- Line 21: `action="sessionreport.do"` (method="POST")

**Session Attribute Accesses:**
- Line 5: `session.getAttribute("sessDateFormat")`
- Line 102: `(String) session.getAttribute("sessDateFormat")`
- Line 110: `(String) session.getAttribute("sessDateFormat")`

**Significant JavaScript Functions Defined:**
- None explicitly named. One anonymous jQuery document-ready function (lines 95–116) sets up date pickers.

---

### 8. resetpass.jsp
**Path:** `src/main/webapp/html-jsp/resetpass.jsp`
**Purpose:** Password reset confirmation form. Accepts a verification code, new password, and confirm password from the user. Validates inputs client-side using SweetAlert (`swal`) and submits to `resetpass.do`. The username is carried forward as a hidden field from the query string.

**JSP Scriptlet Blocks (`<% %>`):**
- Line 2: `<%  String username = request.getParameter("username") == null ? "" : request.getParameter("username"); %>`

**JSP Expression Blocks (`<%= %>`):**
- Line 32: `<%=username%>` — emits the username into the hidden input value.

**`<%@ include %>` / `<jsp:include>` Directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML Form `action` Attributes:**
- Line 16: `action="resetpass.do"` (method="post")

**Session Attribute Accesses:**
- None.

**Significant JavaScript Functions Defined:**
- Lines 42–67: `fnSubmit()` — validates that `npass`, `rnpass`, and `code` are non-empty and that the two passwords match; shows `swal` alerts for each error condition; submits `#resetpassForm` if all valid.

---

### 9. result/json_result.jsp
**Path:** `src/main/webapp/html-jsp/result/json_result.jsp`
**Purpose:** JSON response fragment. Reads a `result` request attribute set by the action layer. If the result equals "success" (case-insensitive), outputs a JSON payload with status `success_close` and a mail-sent message; otherwise outputs an error JSON payload. Used as an AJAX response endpoint, likely for a mail-sending operation.

**JSP Scriptlet Blocks (`<% %>`):**
- Lines 1–10: Entire logic block — declares `message` and `result` strings; applies case-insensitive check on `result`; assigns one of two JSON string literals to `message`.

**JSP Expression Blocks (`<%= %>`):**
- Line 12: `<%=message %>` — outputs the constructed JSON string as the response body.

**`<%@ include %>` / `<jsp:include>` Directives:**
- None.

**HTML Form `action` Attributes:**
- None.

**Session Attribute Accesses:**
- None (uses `request.getAttribute("result")`).

**Significant JavaScript Functions Defined:**
- None (server-side output only).

---

## Findings

### B05-1 | LOW | register.jsp:1 | Missing page-level comment
There is no HTML (`<!-- -->`) or JSP (`<%-- --%>`) comment at or near the top of the file describing its purpose. The first line is the include directive and the second is a structural `<div>`. A reader must infer the page's role from the form heading "New Driver" and the action target `register.do`.

---

### B05-2 | LOW | registerSuccess.jsp:1 | Missing page-level comment
No page-level comment describing the purpose of the page. The file begins immediately with an include directive followed by large commented-out blocks. The actual content and purpose (post-registration success with countdown redirect) must be inferred from reading the body.

---

### B05-3 | LOW | registerSuccess.jsp:2-20 | Dead commented-out layout block with no explanation
Lines 2–20 contain the entire original layout of the page (div structure, `<h2>`, `<h3>`, buttons) commented out using both HTML and JSP comment syntax. There is no accompanying note explaining why this code was replaced, whether it is safe to remove, or what changed. This creates maintenance confusion.

---

### B05-4 | LOW | registerSuccess.jsp:32 | Undocumented form action on a non-interactive page
The `<html:form>` at line 32 targets `action="login.do"`, but this page is purely informational — it auto-redirects and the user never interacts with the form. No comment explains why a login form wrapper is used here, or whether this is intentional scaffolding or a copy-paste artefact.

---

### B05-5 | LOW | reports/gpsReport.jsp:1 | Missing page-level comment
No comment at the top of the file describes its purpose. The file opens directly with include and import directives.

---

### B05-6 | LOW | reports/gpsReport.jsp:2 | Unused import with no comment
Line 2 imports `com.util.DateUtil` via `<%@ page import %>`, but `DateUtil` is never referenced anywhere in the file. There is no comment explaining the import or indicating it is reserved for future use. This is a dead import that may confuse maintainers.

---

### B05-7 | MEDIUM | reports/gpsReport.jsp:57-59 | Misleading / contradictory comment on magic coordinate values
Line 57 declares:
```javascript
var defaultLoc = "-24.2761156,133.5912902"; //UK- 55.378051, -3.435973
```
Lines 58–59:
```javascript
var defaultLat = "-24.2761156"; //AU
var defaultLong = "133.5912902";
```
The active coordinate values (`-24.2761156, 133.5912902`) are central Australia. The inline comment on `defaultLoc` labels them as "UK" and then provides different UK coordinates (`55.378051, -3.435973`) as if they were the active values. The `//AU` comment on the separate variables correctly identifies the coordinates as Australian. This inconsistency means the comment on `defaultLoc` is factually wrong about which country's coordinates are in use, and may cause a developer to believe the system is configured for the UK when it is actually configured for Australia.

---

### B05-8 | LOW | reports/gpsReport.jsp:4-7 | Non-obvious session key `sessCompId` undocumented
The key `"sessCompId"` (line 6) is a cryptic abbreviation. No comment explains what entity it identifies (company/customer ID), what type it holds, or where it is set. The related key `"sessDateFormat"` (line 5) is similarly undocumented but is at least readable. Both are used across multiple report files without documentation.

---

### B05-9 | LOW | reports/impactReport.jsp:1 | Missing page-level comment
No comment at the top of the file describes its purpose.

---

### B05-10 | LOW | reports/impactReport.jsp:44-46 | Magic string impact level values without comment
Lines 44–46 hard-code impact level option values as `"BLUE"`, `"AMBER"`, and `"RED"`. There is no comment explaining what these strings represent (severity thresholds), how they map to sensor readings, or where they are defined in the backend domain. Readers must search elsewhere to understand the severity scale.

---

### B05-11 | MEDIUM | reports/impactReport.jsp:115-121 | Date conversion scriptlet block without comment
The scriptlet at lines 115–121 conditionally converts the request's `start_date` and `end_date` parameters through `DateUtil.stringToIsoNoTimezone()` and emits the result into JavaScript. The conversion method name suggests timezone handling, but there is no comment explaining why ISO format without timezone is needed here, what the source format is, or what the JavaScript `Date()` constructor will receive. The same pattern is repeated without comment in incidentReport.jsp, preOpsReport.jsp, and sessionreport.jsp.

---

### B05-12 | LOW | reports/incidentReport.jsp:1 | Missing page-level comment
No comment at the top of the file describes its purpose.

---

### B05-13 | LOW | reports/incidentReport.jsp:77 | Mismatched table ID
The table at line 77 is given `id="preops_entries"` — the same ID used in preOpsReport.jsp. This appears to be a copy-paste leftover. While not strictly a documentation finding, the absence of any comment compounds the confusion; a reader cannot tell whether this is intentional or an error.

---

### B05-14 | LOW | reports/preOpsReport.jsp:1 | Missing page-level comment
No comment at the top of the file describes its purpose.

---

### B05-15 | LOW | reports/sessionreport.jsp:1 | Missing page-level comment
No comment at the top of the file describes its purpose.

---

### B05-16 | LOW | reports/sessionreport.jsp:4-6 | Session key `sessDateFormat` undocumented (repeated pattern)
As in all other report files, `session.getAttribute("sessDateFormat")` (line 5) is used without any comment explaining the key's meaning, its format, or where it is set. This pattern is present in gpsReport.jsp, impactReport.jsp, incidentReport.jsp, preOpsReport.jsp, and sessionreport.jsp — none have any documentation on this key.

---

### B05-17 | LOW | resetpass.jsp:1 | Missing page-level comment
No comment at the top of the file describes its purpose or the expected flow (user arrives here after requesting a password reset and receiving a verification code by email).

---

### B05-18 | MEDIUM | resetpass.jsp:55-57 | Incomplete error message for missing verification code
The `fnSubmit()` function at line 55–57 shows a SweetAlert for a missing verification code:
```javascript
swal("Error", "Confirmation Code", "error");
```
The message is "Confirmation Code" — a noun phrase with no verb, unlike the other error messages ("New Password is required", "Please Re-type New Password", "Password is not matched"). This appears to be a truncated or unfinished message. There is no comment indicating whether this is intentional or a known defect. A user would see an unhelpful alert.

---

### B05-19 | LOW | resetpass.jsp:2 | Undocumented username pass-through via query string
Line 2 reads the `username` parameter from the query string and places it in a hidden form field (line 32). There is no comment explaining that the username is passed forward from the preceding password-reset request step (presumably `goResetPass.do`), or warning that this value originates from untrusted URL input. While the server-side action should validate it, the absence of a comment obscures the trust boundary.

---

### B05-20 | LOW | result/json_result.jsp:1 | Missing page-level comment
No comment at the top of the file describes its purpose, the calling context, or the structure of the JSON responses it produces.

---

### B05-21 | MEDIUM | result/json_result.jsp:6 | Hard-coded JSON status string `success_close` without comment
Line 6 uses the status value `"success_close"`:
```java
message = "{ \"status\":\"success_close\", \"message\":\"Mail has been sent\" }";
```
The string `success_close` is a non-obvious protocol token. It implies special behaviour in the calling JavaScript (presumably closing a modal or dialog on success), but there is no comment explaining what this value means, what client-side code consumes it, or why it differs from a plain `"success"`. A developer reading only this file has no way to understand the contract.

---

### B05-22 | LOW | result/json_result.jsp:6-8 | Hard-coded English message strings in JSON response
Lines 6 and 8 contain hard-coded English strings `"Mail has been sent"` and `"Sending Failed."` embedded directly in the JSON output. The rest of the application uses `bean:message` keys for internationalisation. There is no comment explaining why these messages are not externalised or whether internationalisation is not required for this response path.

---

## Summary Table

| Finding | Severity | File | Line | Issue |
|---------|----------|------|------|-------|
| B05-1   | LOW      | register.jsp | 1 | Missing page-level comment |
| B05-2   | LOW      | registerSuccess.jsp | 1 | Missing page-level comment |
| B05-3   | LOW      | registerSuccess.jsp | 2–20 | Dead commented-out layout block, no explanation |
| B05-4   | LOW      | registerSuccess.jsp | 32 | Undocumented form action on non-interactive page |
| B05-5   | LOW      | reports/gpsReport.jsp | 1 | Missing page-level comment |
| B05-6   | LOW      | reports/gpsReport.jsp | 2 | Unused import `DateUtil` with no comment |
| B05-7   | MEDIUM   | reports/gpsReport.jsp | 57–59 | Misleading comment — `defaultLoc` comment says "UK" but value is Australian coordinates |
| B05-8   | LOW      | reports/gpsReport.jsp | 6 | Non-obvious session key `sessCompId` undocumented |
| B05-9   | LOW      | reports/impactReport.jsp | 1 | Missing page-level comment |
| B05-10  | LOW      | reports/impactReport.jsp | 44–46 | Magic string impact level values (BLUE/AMBER/RED) without comment |
| B05-11  | MEDIUM   | reports/impactReport.jsp | 115–121 | Date conversion scriptlet without explanatory comment |
| B05-12  | LOW      | reports/incidentReport.jsp | 1 | Missing page-level comment |
| B05-13  | LOW      | reports/incidentReport.jsp | 77 | Mismatched table ID `preops_entries` with no comment |
| B05-14  | LOW      | reports/preOpsReport.jsp | 1 | Missing page-level comment |
| B05-15  | LOW      | reports/sessionreport.jsp | 1 | Missing page-level comment |
| B05-16  | LOW      | reports/sessionreport.jsp | 5 | Session key `sessDateFormat` undocumented (cross-file pattern) |
| B05-17  | LOW      | resetpass.jsp | 1 | Missing page-level comment |
| B05-18  | MEDIUM   | resetpass.jsp | 55–57 | Incomplete/truncated error message for missing verification code |
| B05-19  | LOW      | resetpass.jsp | 2 | Undocumented username pass-through from untrusted query string |
| B05-20  | LOW      | result/json_result.jsp | 1 | Missing page-level comment |
| B05-21  | MEDIUM   | result/json_result.jsp | 6 | Undocumented protocol token `success_close` in JSON status |
| B05-22  | LOW      | result/json_result.jsp | 6–8 | Hard-coded English message strings not internationalised, no comment |

**Total findings: 22**
- HIGH: 0
- MEDIUM: 4 (B05-7, B05-11, B05-18, B05-21)
- LOW: 18
