# Pass 3 – Documentation Audit
**Agent:** B02
**Date:** 2026-02-26
**Scope:** adminReports.jsp, adminSubscription.jsp, adminUnit.jsp, adminUser.jsp, apiXml.jsp, dealer/adminSubcompanyEdit.jsp, dealer/impactReport.jsp, dealer/incidentReport.jsp, dealer/preOpsReport.jsp

---

## Reading Evidence

---

### 1. adminReports.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminReports.jsp`

**Purpose:** Reports landing/hub page. Displays links to the Incident Report, Session Report, and GPS Report. Dynamically selects the correct URL for Incident Report and Session Report based on whether the current user is a dealer.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 3–6: Reads `isDealer` session attribute; sets `incidentReportUrl` and `sessionReportUrl` to dealer-specific or standard action URLs.

**JSP Expression blocks (`<%= %>`):**
- Line 26: `<%= incidentReportUrl %>` — renders the Incident Report href.
- Line 29: `<%= incidentReportUrl %>` — renders the Incident Report anchor image href.
- Line 38: `<%= sessionReportUrl %>` — renders the Session Report anchor image href.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:** None (no `<form>` element present).

**Session attribute accesses:**
- Line 4: `session.getAttribute("isDealer")` — used to branch between dealer and standard report URLs.
- Line 5: `session.getAttribute("isDealer")` — same attribute, second use for session report URL.

**Significant JavaScript functions defined:** None.

---

### 2. adminSubscription.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminSubscription.jsp`

**Purpose:** Subscription management page. Displays a list of available subscription options (from `arrSubscription`) with checkboxes, allowing the user to select subscriptions to assign to a company. Submits to `adminsubscription.do`.

**JSP Scriptlet blocks (`<% %>`):** None.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`

**HTML form `action` attributes:**
- Line 7: `action="adminsubscription.do"` (Struts `<html:form>`).

**Session attribute accesses:** None directly in this file (session may be accessed via included importLib.jsp).

**Significant JavaScript functions defined:** None.

---

### 3. adminUnit.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminUnit.jsp`

**Purpose:** Manage Vehicles (forklift units) list page. Provides a search field to filter vehicles, a button to add a new vehicle (via lightbox modal), and a table listing existing vehicles with edit and delete action buttons.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 3–5: Reads `searchUnit` request parameter; defaults to empty string if null.

**JSP Expression blocks (`<%= %>`):**
- Line 23: `<%=searchUnit %>` — populates the search input field value.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 18: `action="adminunit.do"` (plain HTML `<form>`).

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions defined:** None.

---

### 4. adminUser.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminUser.jsp`

**Purpose:** Manage Users (drivers) list page. Provides a search field to filter users, a button to add a new user (via lightbox modal), and a table listing existing users with edit and delete action buttons. Note: form action and backend action names reference "driver" though the visible UI label says "Users".

**JSP Scriptlet blocks (`<% %>`):**
- Lines 3–5: Reads `searchDriver` request parameter; defaults to empty string if null.

**JSP Expression blocks (`<%= %>`):**
- Line 25: `<%=searchDriver %>` — populates the search input field value.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 20: `action="admindriver.do"` (plain HTML `<form>`, method GET).

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions defined:** None.

---

### 5. apiXml.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/apiXml.jsp`

**Purpose:** Mobile/API XML response renderer. Sets content type to `text/xml` and generates an XML body by branching on the `method` request attribute. Handles response types for: login (compKey), vehicle list, driver list, attachment list, question list (with XML entity escaping), result status, and PDF report email status.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 6–103: Single large scriptlet covering the entire file logic:
  - Line 7: Sets content type to `text/xml`.
  - Lines 8–9: Initialises `resp` string and opens `<body>` tag.
  - Lines 11–12: Reads `method` and `error` request attributes.
  - Lines 13–16: Branch `API_LOGIN` — appends `compKey` record.
  - Lines 18–25: Branch `API_VEHICLE` — iterates `arrUnit`, appends id/name records.
  - Lines 27–35: Branch `API_DRIVER` — iterates `arrDriver`, appends id/name records.
  - Lines 36–45: Branch `API_ATTACHMENT` — iterates `arrAtt`, appends id/name records.
  - Lines 46–73: Branch `API_QUESTION` — iterates `arrQues`, applies XML entity escaping to question content, appends id/name/value records.
  - Lines 75–81: Branch `API_RESULT` (first occurrence) — appends resultstatus and emailstatus records.
  - Lines 82–88: Branch `API_RESULT` (second, duplicate occurrence — dead/unreachable code) — identical to the block above.
  - Lines 89–93: Branch `API_PDFRPT` — appends emailstatus record.
  - Lines 95–98: Appends error record if error is non-empty.
  - Lines 100–102: Closes `</body>` tag and writes to output.

**JSP Expression blocks (`<%= %>`):** None (all output via `out.println` inside scriptlet).

**`<%@ include %>` / `<jsp:include>` directives:** None (uses `<%@ page %>` directives only).

**HTML form `action` attributes:** None.

**Session attribute accesses:** None directly (operates on request attributes only).

**Significant JavaScript functions defined:** None.

---

### 6. dealer/adminSubcompanyEdit.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`

**Purpose:** Dealer sub-company edit/add form (rendered in a modal). Displays a two-column form with Company Info (name, timezone, address) and User Info (first name, last name, phone, email, password, confirm password) fields. A hidden field `accountAction` is hard-coded to `"add"`, implying this form only supports adding (not editing) despite being named "Edit". Client-side validation is performed in JavaScript before form submission.

**JSP Scriptlet blocks (`<% %>`):** None.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 4: `action="adminRegister"` (Struts `<html:form>`).

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions defined:**
- `fnsubmitAccount()` (lines 138–169): Reads form values for company name, email, password, confirm password, and timezone. Displays SweetAlert error dialogs for missing/mismatched fields. If validation passes, submits `#adminCompActionForm`.
- Anonymous `jQuery(document).ready` handler (lines 171–174): Initialises `#pword` password strength plugin — however note the input's `id` attribute is not set to `pword` in the HTML (the `<input>` for password at line 102 has no `id` attribute and uses `name="pin"`), making this initialisation call non-functional.

---

### 7. dealer/impactReport.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/impactReport.jsp`

**Purpose:** Dealer Impact Report page. Displays a filter form (manufacturer, type, impact level, date range) and a grouped table of impact events across all dealer sub-companies. Rows are grouped by unit (manufacturer + unit name span multiple rows via `rowspan`). A colour swatch and g-force value are rendered for the impact level column. Date pickers are initialised via JavaScript.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 4–6: Reads `sessDateFormat` session attribute; converts Java date format to jQuery datepicker format (replaces `yyyy`→`yy` and `M`→`m`).
- Lines 117–119: In the script block — conditional: if `start_date` request parameter is not null, emits a JavaScript assignment parsing the date using `DateUtil.stringToIsoNoTimezone`.
- Lines 121–123: In the script block — conditional: if `end_date` request parameter is not null, emits a JavaScript assignment.

**JSP Expression blocks (`<%= %>`):**
- Line 88: `<%= impactGroup.getEntries().size() %>` — `rowspan` value for manufacturer cell.
- Line 91: `<%= impactGroup.getEntries().size() %>` — `rowspan` value for unit name cell.
- Line 99: `<%= impactEntry.getImpactLevelCSSColor() %>` — background colour for impact level swatch.
- Line 102: `<%= String.format(" (%.1fg)", impactEntry.getGForce()) %>` — formatted g-force value.
- Line 118: `<%= DateUtil.stringToIsoNoTimezone(...) %>` — ISO date string for JS date constructor.
- Line 122: `<%= DateUtil.stringToIsoNoTimezone(...) %>` — ISO date string for JS date constructor.
- Line 125: `<%= dateFormat %>` — jQuery datepicker format string.
- Line 126: `<%= dateFormat %>` — jQuery datepicker format string.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`
- Line 2: `<%@ page import="com.util.DateUtil" %>`

**HTML form `action` attributes:**
- Line 22: `action="dealerImpactReport.do"` (Struts `<html:form>`).

**Session attribute accesses:**
- Line 5: `session.getAttribute("sessDateFormat")` — retrieves the user/company date format for datepicker configuration.
- Line 118: `(String) session.getAttribute("sessDateFormat")` — used in `DateUtil.stringToIsoNoTimezone` call to parse submitted start date.
- Line 122: `(String) session.getAttribute("sessDateFormat")` — same, for end date.

**Significant JavaScript functions defined:**
- Anonymous `$(function(){...})` (lines 113–127): Initialises `start_date` and `end_date` JS variables from request parameters (if present), then calls `setupDatePicker` for both date fields.

---

### 8. dealer/incidentReport.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/incidentReport.jsp`

**Purpose:** Dealer Incident Report page. Displays a filter form (manufacturer, type, date range with calendar buttons) and a detailed table of incident events across all dealer sub-companies, including fields for near-miss, incident, injury flags (rendered via a helper method), injury type, location, witness, and links to signature and image lightboxes.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 4–6: Reads `sessDateFormat` session attribute; converts format for jQuery datepicker.
- Lines 148–150: Conditional JS assignment for `start_date` if request parameter present.
- Lines 152–154: Conditional JS assignment for `end_date` if request parameter present.

**JSP Declaration blocks (`<%! %>`):**
- Lines 7–10: Declares helper method `getYesNoMessageKey(boolean value)` — returns message key `"clst.answerY"` or `"clst.answerN"` based on boolean value, used inline in bean:message tags.

**JSP Expression blocks (`<%= %>`):**
- Line 107: `<%= getYesNoMessageKey(incidentEntry.getNear_miss()) %>` — message key for near-miss column.
- Line 108: `<%= getYesNoMessageKey(incidentEntry.getIncident()) %>` — message key for incident column.
- Line 109: `<%= getYesNoMessageKey(incidentEntry.getInjury()) %>` — message key for injury column.
- Line 149: `<%= DateUtil.stringToIsoNoTimezone(...) %>` — ISO date string for start date JS.
- Line 153: `<%= DateUtil.stringToIsoNoTimezone(...) %>` — ISO date string for end date JS.
- Line 156: `<%= dateFormat %>` — datepicker format.
- Line 157: `<%= dateFormat %>` — datepicker format.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`
- Line 2: `<%@ page import="com.util.DateUtil" %>`

**HTML form `action` attributes:**
- Line 27: `action="dealerIncidentReport.do"` (Struts `<html:form>`).

**Session attribute accesses:**
- Line 5: `session.getAttribute("sessDateFormat")` — date format for datepicker.
- Line 149: `(String) session.getAttribute("sessDateFormat")` — for start date parse.
- Line 153: `(String) session.getAttribute("sessDateFormat")` — for end date parse.

**Significant JavaScript functions defined:**
- Anonymous `$(function(){...})` (lines 144–162): Initialises date picker fields with current or submitted dates. Also disables keyboard input on datepicker text boxes via `keydown` handler returning `false`.

---

### 9. dealer/preOpsReport.jsp
**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/preOpsReport.jsp`

**Purpose:** Dealer Pre-Ops (pre-operational safety check) Report page. Displays a filter form (manufacturer, type, date range) with search and print buttons, and a table listing pre-ops check details per vehicle per company, including a nested list of failure items per entry.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 4–6: Reads `sessDateFormat` session attribute; converts to jQuery datepicker format.
- Lines 109–111: Conditional JS assignment for `start_date` from request parameter.
- Lines 113–115: Conditional JS assignment for `end_date` from request parameter.

**JSP Expression blocks (`<%= %>`):**
- Line 110: `<%= DateUtil.stringToIsoNoTimezone(...) %>` — ISO start date for JS.
- Line 114: `<%= DateUtil.stringToIsoNoTimezone(...) %>` — ISO end date for JS.
- Line 117: `<%= dateFormat %>` — datepicker format.
- Line 118: `<%= dateFormat %>` — datepicker format.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`
- Line 2: `<%@ page import="com.util.DateUtil" %>`

**HTML form `action` attributes:**
- Line 22: `action="dealerPreOpsReport.do"` (Struts `<html:form>`).

**Session attribute accesses:**
- Line 5: `session.getAttribute("sessDateFormat")` — date format for datepicker.
- Line 110: `(String) session.getAttribute("sessDateFormat")` — start date parse.
- Line 114: `(String) session.getAttribute("sessDateFormat")` — end date parse.

**Significant JavaScript functions defined:**
- Anonymous `$(function(){...})` (lines 105–119): Initialises date pickers with current or submitted dates by calling `setupDatePicker`.

---

## Findings

---

### B02-1 | LOW | adminReports.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose at the top of the file. The first line is an include directive followed immediately by a scriptlet. A reader must infer that this is the reports hub/landing page entirely from the heading HTML further down.

---

### B02-2 | MEDIUM | adminReports.jsp:3-6 | Complex conditional scriptlet without comment

The scriptlet at lines 3–6 silently branches report destination URLs based on the session attribute `"isDealer"`. There is no comment explaining why two different action endpoints exist, what constitutes a "dealer" context, or what the fallback (non-dealer) endpoints are for. A future developer modifying this logic has no guidance on the intent or the expected values.

```jsp
<%
    String incidentReportUrl = session.getAttribute("isDealer").equals("true") ? "dealerIncidentReport.do" : "incidentreport.do";
    String sessionReportUrl = session.getAttribute("isDealer").equals("true") ? "dealerSessionReport.do" : "sessionreport.do";
%>
```

---

### B02-3 | LOW | adminReports.jsp:4-5 | Non-obvious session attribute key "isDealer" undocumented

The session key `"isDealer"` is read twice with no comment explaining what values it holds (`"true"` as a String), when it is set, or where. The string comparison `.equals("true")` (comparing to a literal string rather than a Boolean) is a non-obvious pattern that warrants documentation.

---

### B02-4 | LOW | adminReports.jsp:36 | Hard-coded URL inconsistency with no comment

At line 36, the Session Report card's heading anchor href is hard-coded to `"sessionreport.do"` (non-dealer URL), while the image link on line 38 correctly uses `<%= sessionReportUrl %>`. This means dealer users clicking the heading link will be routed to the wrong endpoint. Even if intentional (which seems unlikely), there is no comment explaining the discrepancy.

```html
<h3><a href="sessionreport.do">Session Report</a></h3>
...
<a href="<%= sessionReportUrl %>" class="box-a">...
```

---

### B02-5 | LOW | adminSubscription.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose. The file begins directly with an include directive and layout markup.

---

### B02-6 | LOW | adminSubscription.jsp:38 | Stray `<!-- /container -->` comment is misleading

The comment `<!-- /container -->` at line 38 appears to reference a container element that is not explicitly present in this file fragment (the file renders into a larger layout). The comment does not describe the page purpose and could mislead a developer into thinking a full container is being closed here, when the actual outer layout structure is defined elsewhere.

---

### B02-7 | LOW | adminUnit.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose at the top of the file.

---

### B02-8 | LOW | adminUnit.jsp:3-5 | Undocumented null-coalescing pattern for request parameter

The scriptlet at lines 3–5 silently defaults the `searchUnit` parameter to an empty string with no comment. While the logic is short, the pattern is idiomatic boilerplate that is repeated identically in adminUser.jsp; a single comment in either file (explaining that null prevents a NullPointerException in the input value attribute) would improve maintainability.

---

### B02-9 | LOW | adminUser.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose at the top of the file.

---

### B02-10 | LOW | adminUser.jsp:20 | Form action name mismatch with no comment

The form at line 20 submits to `admindriver.do`, while the page's visible heading and breadcrumb are labelled "Manage Users". The underlying action name and Struts bean name `arrAdminDriver` use "driver" terminology throughout the page, but the UI calls them "Users". No comment explains the naming discrepancy or legacy reason for the different terminology.

---

### B02-11 | LOW | adminUser.jsp:3-5 | Undocumented null-coalescing pattern for request parameter

Same pattern as B02-8 for `searchDriver`; no comment on null-safety rationale.

---

### B02-12 | HIGH | apiXml.jsp:6 | Entire file logic is one uncommented scriptlet with no page-level description

The entire 98-line scriptlet (lines 6–103) has no explanatory comments whatsoever. This file is the sole XML API response serialiser for the mobile client and handles login, vehicle, driver, attachment, question, and result payloads. The complete absence of comments means:
- The branching logic (which `RuntimeConf` constants map to which response format) is opaque.
- The XML entity escaping block for `API_QUESTION` (lines 47–73) uses `else if` chains instead of sequential replacements, meaning only the first matching character type is escaped per string — a subtle logic defect with no comment to indicate whether it is intentional.
- The duplicate `API_RESULT` branch (lines 82–88) is dead/unreachable code with no comment explaining its presence.

Given that this file is the interface contract for a mobile API, the total lack of documentation is a high-severity documentation gap.

---

### B02-13 | MEDIUM | apiXml.jsp:46-73 | XML entity escaping uses else-if chain — logic defect, no comment

The question content escaping block at lines 46–73 uses a chain of `else if` conditions: only the first matching special character type (`&`, `'`, `"`, `<`, `>`) is replaced. If a question string contains both `&` and `<`, only the `&` is escaped. No comment documents this limitation or indicates it is intentional. This is likely a defect masquerading as logic. The absence of any comment makes it impossible to determine intent.

```java
if(content.contains("&"))      { content = content.replace("&","&amp;"); }
else if(content.contains("'")) { content = content.replace("'","&apos;"); }
else if(content.contains("\"")){ content = content.replace("\"","&quot;"); }
else if(content.contains("<")) { content = content.replace("<","&lt;"); }
else if(content.contains(">")) { content = content.replace("<","&gt;"); }  // also: replaces "<" not ">"
```

Additionally, line 70 has a copy-paste bug: `content.replace("<","&gt;")` replaces `<` with `&gt;` instead of replacing `>` with `&gt;`. No comment is present to flag or explain this.

---

### B02-14 | MEDIUM | apiXml.jsp:82-88 | Dead code — duplicate API_RESULT branch, no comment

Lines 82–88 are an exact duplicate of lines 75–81, both branching on `method.equalsIgnoreCase(RuntimeConf.API_RESULT)`. The second `else if` can never be reached. No comment explains why this block exists, whether it was intended to handle a different method constant, or whether it is safe to remove.

```java
else if(method.equalsIgnoreCase(RuntimeConf.API_RESULT))  // line 75 - executed
{ ... }
else if(method.equalsIgnoreCase(RuntimeConf.API_RESULT))  // line 82 - unreachable
{ ... }
```

---

### B02-15 | LOW | dealer/adminSubcompanyEdit.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose at the top of the file.

---

### B02-16 | MEDIUM | dealer/adminSubcompanyEdit.jsp:133 | Hidden field "accountAction" hard-coded to "add" despite file being named "Edit"

Line 133 contains:
```jsp
<html:hidden property="accountAction" value="add" />
```
The file is named `adminSubcompanyEdit.jsp`, strongly suggesting it should support editing an existing sub-company record. However, `accountAction` is unconditionally set to `"add"`, meaning this form always creates a new account regardless of whether a company record is being edited. No comment explains whether the "Edit" in the filename is wrong, whether this is intentional (always re-register), or whether this is a defect. This is at minimum a misleading lack of documentation; it may represent a functional bug.

---

### B02-17 | LOW | dealer/adminSubcompanyEdit.jsp:171-174 | Password strength plugin targets non-existent element ID

The `jQuery(document).ready` block at lines 171–174 calls `$('#pword').strength()` but no element in the file has `id="pword"`. The password input at lines 102–108 has no `id` attribute set. The strength meter plugin call is silently non-functional with no comment explaining the intended wiring.

---

### B02-18 | LOW | dealer/impactReport.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose at the top of the file.

---

### B02-19 | LOW | dealer/impactReport.jsp:4-6 | Non-obvious date format conversion lacks comment

The format conversion `.replaceAll("yyyy", "yy").replaceAll("M", "m")` translates a Java SimpleDateFormat pattern to a jQuery UI datepicker format. There is no comment explaining why this translation is needed, what the source format attribute contains, or what the expected output format is. The `replaceAll("M", "m")` call is especially non-obvious as it also replaces the `M` within `MM` and `MMM` patterns.

---

### B02-20 | LOW | dealer/impactReport.jsp:44-47 | Hard-coded impact level values without comment

The impact level dropdown hard-codes the string values `"BLUE"`, `"AMBER"`, and `"RED"` at lines 44–47 with no comment linking them to the constants or enum values defined elsewhere in the codebase (e.g., `ImpactLevel`). If the valid values change in the backend, the JSP will silently send stale values.

---

### B02-21 | LOW | dealer/incidentReport.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose at the top of the file.

---

### B02-22 | LOW | dealer/incidentReport.jsp:4-6 | Non-obvious date format conversion lacks comment

Same pattern as B02-19. No comment on the Java-to-jQuery format translation.

---

### B02-23 | LOW | dealer/incidentReport.jsp:159-161 | Keyboard input disabled on datepicker fields with no comment

The `keydown` handler at lines 159–161 returns `false` to prevent any keyboard input in datepicker text boxes. This is a UX constraint that may surprise maintenance developers and has no comment explaining the rationale (presumably to force users to use the date picker widget rather than type freeform dates, which could break the expected date format).

```js
$('.datepicker_textbox').on('keydown', function() {
    return false;
});
```

---

### B02-24 | LOW | dealer/preOpsReport.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose at the top of the file.

---

### B02-25 | LOW | dealer/preOpsReport.jsp:4-6 | Non-obvious date format conversion lacks comment

Same pattern as B02-19 and B02-22. No comment on the Java-to-jQuery format translation.

---

### B02-26 | LOW | dealer/preOpsReport.jsp:54-57 | Print button uses inline onclick with no comment

The print button at lines 54–57 uses `onclick="window.print(); return false;"`. The `return false` prevents default form submission but this is not commented. A developer unfamiliar with the context might remove `return false` expecting no side effects, causing the form to submit on print.

---

## Summary Table

| ID     | Severity | File:Line                                      | Description                                                                                         |
|--------|----------|------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| B02-1  | LOW      | adminReports.jsp:1                             | Missing page-level comment                                                                          |
| B02-2  | MEDIUM   | adminReports.jsp:3-6                           | Dealer/non-dealer URL branching scriptlet has no comment explaining the routing logic               |
| B02-3  | LOW      | adminReports.jsp:4-5                           | Session key "isDealer" is undocumented; string "true" comparison pattern unexplained                |
| B02-4  | LOW      | adminReports.jsp:36                            | Session Report heading link hard-coded to non-dealer URL while image link uses dynamic URL — no comment |
| B02-5  | LOW      | adminSubscription.jsp:1                        | Missing page-level comment                                                                          |
| B02-6  | LOW      | adminSubscription.jsp:38                       | Stray `<!-- /container -->` comment is misleading — no container is present in this fragment        |
| B02-7  | LOW      | adminUnit.jsp:1                                | Missing page-level comment                                                                          |
| B02-8  | LOW      | adminUnit.jsp:3-5                              | Null-coalescing request parameter default has no comment                                            |
| B02-9  | LOW      | adminUser.jsp:1                                | Missing page-level comment                                                                          |
| B02-10 | LOW      | adminUser.jsp:20                               | Form submits to "admindriver.do" but UI labels say "Users" — mismatch undocumented                 |
| B02-11 | LOW      | adminUser.jsp:3-5                              | Null-coalescing request parameter default has no comment                                            |
| B02-12 | HIGH     | apiXml.jsp:6                                   | Entire 98-line API serialiser scriptlet has zero comments; no page-level description                |
| B02-13 | MEDIUM   | apiXml.jsp:46-73                               | XML entity escaping uses else-if chain (only first match escapes); line 70 has copy-paste bug replacing `<` instead of `>`; no comment |
| B02-14 | MEDIUM   | apiXml.jsp:82-88                               | Dead code: duplicate else-if branch for API_RESULT is unreachable; no comment                      |
| B02-15 | LOW      | dealer/adminSubcompanyEdit.jsp:1               | Missing page-level comment                                                                          |
| B02-16 | MEDIUM   | dealer/adminSubcompanyEdit.jsp:133             | Hidden field "accountAction" hard-coded to "add" in a file named "Edit"; no comment                |
| B02-17 | LOW      | dealer/adminSubcompanyEdit.jsp:171-174         | Password strength plugin targets `#pword` which has no matching element in the file                 |
| B02-18 | LOW      | dealer/impactReport.jsp:1                      | Missing page-level comment                                                                          |
| B02-19 | LOW      | dealer/impactReport.jsp:4-6                    | Java-to-jQuery date format conversion has no comment                                                |
| B02-20 | LOW      | dealer/impactReport.jsp:44-47                  | Impact level values "BLUE"/"AMBER"/"RED" hard-coded with no link to backend constants               |
| B02-21 | LOW      | dealer/incidentReport.jsp:1                    | Missing page-level comment                                                                          |
| B02-22 | LOW      | dealer/incidentReport.jsp:4-6                  | Java-to-jQuery date format conversion has no comment                                                |
| B02-23 | LOW      | dealer/incidentReport.jsp:159-161              | Keyboard input suppressed on datepicker fields with no comment explaining rationale                 |
| B02-24 | LOW      | dealer/preOpsReport.jsp:1                      | Missing page-level comment                                                                          |
| B02-25 | LOW      | dealer/preOpsReport.jsp:4-6                    | Java-to-jQuery date format conversion has no comment                                                |
| B02-26 | LOW      | dealer/preOpsReport.jsp:54-57                  | Print button inline onclick with `return false` has no comment explaining why form submission is suppressed |

**Total findings: 26**
- HIGH: 1 (B02-12)
- MEDIUM: 4 (B02-2, B02-13, B02-14, B02-16)
- LOW: 21
