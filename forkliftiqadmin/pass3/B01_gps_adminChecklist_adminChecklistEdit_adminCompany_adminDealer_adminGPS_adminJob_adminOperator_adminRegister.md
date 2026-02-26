# Pass 3 Documentation Audit — Agent B01
**Date:** 2026-02-26
**Auditor:** B01
**Scope:** gps/unit.gps.jsp, html-jsp/adminChecklist.jsp, html-jsp/adminChecklistEdit.jsp, html-jsp/adminCompany.jsp, html-jsp/adminDealer.jsp, html-jsp/adminGPS.jsp, html-jsp/adminJob.jsp, html-jsp/adminOperator.jsp, html-jsp/adminRegister.jsp

---

## Reading Evidence

---

### File 1: `gps/unit.gps.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/gps/unit.gps.jsp`

**Purpose:** A JSON-fragment producer. Reads a `List<String>` from the request attribute `arrGPSData` and writes a raw JSON object (with `count` and `units` array) directly to the response output. This is not a display page — it functions as a data endpoint returning GPS unit data.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 9–31: Main scriptlet — casts `request.getAttribute("arrGPSData")` to `List<String>`, iterates over the list to build a JSON string, and calls `out.println(resp)` to emit the response.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:** None (no importLib include).

**HTML form `action` attributes:** None (no HTML form).

**Session attribute accesses:** None.

**Significant JavaScript functions:** None (no JavaScript block).

**Commented-out code:**
- Line 5: `<%-- <%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%> --%>` — commented-out import directive.
- Line 7: `<%-- <jsp:useBean class="com.torrent.surat.fms6.beans.Databean_report" id="filter" scope="request"/> --%>` — commented-out `useBean`.
- Line 28: `// resp = "{\"count\":95,\"units\":[{...}]}";` — a large inline JSON sample string commented out inline within the active scriptlet.

---

### File 2: `html-jsp/adminChecklist.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminChecklist.jsp`

**Purpose:** Checklist configuration list page. Allows an admin to filter checklist questions by manufacturer, type, fuel/power type, and attachment, then list or add questions. Renders a results table with per-row show/hide/edit/delete actions.

**JSP Scriptlet blocks (`<% %>`):** None.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 15: `action="fleetcheckconf.do"` (Struts `html:form`)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions (lines 171–273):**
- `isValidFields()` (line 172): Validates that manufacturer, type, and fuel_type_id dropdowns are non-empty; shows SweetAlert on failure.
- `fnaddchecklist()` (line 191): Reads the three filter dropdowns, builds a URL for `fleetcheckconf.do?action=add`, sets it on the hidden `#AddCheckList` anchor, then triggers a click.
- `checklistAdd()` (line 201): Calls `isValidFields()`; if valid, triggers `ekkoLightbox()` on `#AddCheckList`.
- `list()` (line 209): Sets the hidden `chkact` field to `'search'` and submits the form.
- `displayRequiredFields()` (line 214): Applies red border styling to empty required dropdowns; clears borders when values are present.
- `hideQuestion(id)` (line 234): Calls `postAndReload` with `fleetcheckhide.do`.
- `showQuestion(id)` (line 238): Calls `postAndReload` with `fleetcheckshow.do`.
- `postAndReload(url, id)` (line 242): POSTs current filter values plus the question `id` to the given URL, then reloads the page after a 300 ms timeout.

**Commented-out code:** None.

---

### File 3: `html-jsp/adminChecklistEdit.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminChecklistEdit.jsp`

**Purpose:** Modal form for editing a single checklist question. Displayed inside a lightbox. Renders fields for question content, expected answer (YES/NO), and answer type. Submits via an AJAX POST to `fleetcheckedit.do` and reloads on success.

**JSP Scriptlet blocks (`<% %>`):** None.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:** None — the form submission is done exclusively via `$.post('fleetcheckedit.do', ...)` in JavaScript; there is no `<form>` element with an `action` attribute.

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions (lines 82–115):**
- `fntoogleDiv(type)` (line 83): Shows or hides the `.expectAns` section depending on whether `type == "1"` (Y/N answer type). Comment `//type 1, y/n` is present.
- `submit()` (line 93): Collects all hidden and visible field values and POSTs them to `fleetcheckedit.do`; on success calls `location.reload()`.

**Commented-out code:** None.

---

### File 4: `html-jsp/adminCompany.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminCompany.jsp`

**Purpose:** Company/locations management list page. Displays a table of sub-companies (name and address) associated with the current dealer. Provides an "Add Company" button that opens a lightbox modal.

**JSP Scriptlet blocks (`<% %>`):** None.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 17: `action="dealercompanies.do"` (plain HTML `<form>`)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions:** None defined in this file.

**Commented-out code:** None.

---

### File 5: `html-jsp/adminDealer.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminDealer.jsp`

**Purpose:** Dealer management page. Allows selection of a company from a dropdown and submission to convert that company to a dealer account. Displays the current list of dealers in a table.

**JSP Scriptlet blocks (`<% %>`):** None.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 16: `action="/dealerconvert.do"` (Struts `html:form`)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions:** None defined in this file.

**Commented-out code:** None.

---

### File 6: `html-jsp/adminGPS.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminGPS.jsp`

**Purpose:** GPS Report view page. Renders a map canvas (`#map_canvas`) and a multi-select list of units. Retrieves the session's date format and a hardcoded `custCd` value. Provides a Refresh button and defines GPS map initialisation/unit-fetch functions.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 2–5: Reads `sessDateFormat` from the session and reformats it for a JavaScript date-picker pattern; initialises `custCd` to `"0"`.

**JSP Expression blocks (`<%= %>`):**
- Line 44: `<%=custCd %>` — outputs the `custCd` Java variable into the hidden `cust_cd` input value.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 17: `action="adminunit.do"` (plain HTML `<form>`)

**Session attribute accesses:**
- Line 3: `session.getAttribute("sessDateFormat")` — reads the user's date format preference from the HTTP session.

**Significant JavaScript functions (lines 48–103):**
- `fnRefresh()` (line 62): Calls `initialize()` passing values from `#cust` and `#site` inputs (neither input is defined in this file); conditionally calls `application.getGotToZonesControl()`.
- `fetchUnit(str)` (line 70): Reads `#cust` and `#site` values; performs a synchronous AJAX call to `../master/get_cust_vehicle.jsp`; parses the XML response (with an IE-specific ActiveXObject branch); populates `model_cd` options in the form.

**Commented-out code (lines 54–56):**
```javascript
// 	    var defaultLat = "-24.2761156"; //AU
// 	   	var defaultLong = "133.5912902";
```
Australian default coordinates commented out in favour of the UK coordinates on lines 57–58.

---

### File 7: `html-jsp/adminJob.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminJob.jsp`

**Purpose:** Job management modal. Displays a list of jobs for a given equipment/unit (identified by `equipId` request parameter). Each job row shows title, description, driver, status (derived from `startTime`/`endTime` nullity), and action icons. Provides an Add Job button and a Save button that submits all job forms via sequential AJAX.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 2–5: Reads `action` and `equipId` from request parameters, defaulting to empty string if null.

**JSP Expression blocks (`<%= %>`):**
- Line 9: `<%=id %>` — outputs `equipId` into a hidden `equip_id` input.
- Line 10: `<%=action %>` — outputs `action` into a hidden `action` input.
- Line 72: `<%=id %>` — outputs `equipId` into a per-job hidden `equipId` input inside the iterate loop.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`

**HTML form `action` attributes:**
- Line 35: `action="adminunit.do"` (plain HTML `<form>` inside a `logic:iterate` loop — one form per job row)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions (lines 93–119):**
- `triggerClick(id, genId)` (line 94): Locates a job row by `genId`, validates the job title, then dynamically creates and clicks an anchor pointing to `driverjob.do?action=assign` to open the driver allocation lightbox.
- `saveJobs()` (line 110): Iterates over all `.ajax_mode_c` forms, collects them into an array `list[]`, then calls `ajax_recaller(list)` (defined externally).

**Commented-out code:**
- Line 18: `<!-- <input type="text" id="driver_name" ...> -->` — commented-out driver name input.
- Lines 83–84: `<%-- <html:submit ... /> --%>` (JSP comment) and `<!-- <input type="submit" ... /> -->` (HTML comment) — two alternative submit button implementations commented out, replaced by the `<a>` element on line 85.

---

### File 8: `html-jsp/adminOperator.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminOperator.jsp`

**Purpose:** Operator/driver management list page. Provides a search box to filter drivers by name, an Add Driver button, and a table listing drivers with edit and delete actions.

**JSP Scriptlet blocks (`<% %>`):**
- Lines 3–5: Reads `searchDriver` request parameter, defaulting to empty string if null.

**JSP Expression blocks (`<%= %>`):**
- Line 25: `<%=searchDriver %>` — outputs the search term into the search input's `value` attribute to preserve it across form submissions.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 20: `action="admindriver.do"` with `method="get"` (plain HTML `<form>`)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions:** None defined in this file.

**Commented-out code:** None.

---

### File 9: `html-jsp/adminRegister.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminRegister.jsp`

**Purpose:** New company/user registration form. Collects company name, timezone, address, contact first/last name, phone number, email, password, and confirm-password. Performs client-side validation and submits to `adminRegister.do`. Also contains a Back button that redirects to `index.jsp`.

**JSP Scriptlet blocks (`<% %>`):** None.

**JSP Expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`

**HTML form `action` attributes:**
- Line 12: `action="adminRegister.do"` (Struts `html:form`)

**Session attribute accesses:** None directly in this file.

**Significant JavaScript functions (lines 149–187):**
- `fnsubmitAccount()` (line 150): Validates that company name, email, password, confirm-password (match), and timezone are all provided and consistent; on success submits `#adminRegActionForm`. Password field is read from the input named `pin`.
- `fnGoBackHome()` (line 184): Redirects to `index.jsp` via `location.replace()`.

**Commented-out code:**
- Line 123: `<!-- Change this to a button or input when using this as a form -->` — developer note left in the markup.

---

## Findings

### B01-1 | LOW | gps/unit.gps.jsp:1 | Missing page-level comment

No HTML or JSP comment near the top of the file describes its purpose. This file behaves as a JSON data endpoint, which is non-obvious from the file name alone. A page-level comment stating its role (e.g., "Returns GPS unit data as a JSON object for map display") would aid maintenance.

---

### B01-2 | LOW | gps/unit.gps.jsp:5,7 | Dead commented-out imports with no explanation

Lines 5 and 7 contain `<%-- --%>` commented-out directives referencing `com.torrent.surat.fms6` — a package that does not appear to match the current application package (`com.bean`). No comment explains why these were disabled or whether they belong to a superseded integration. This is dead code of unknown provenance.

---

### B01-3 | LOW | gps/unit.gps.jsp:28 | Large commented-out magic JSON sample with no explanation

Line 28 contains a hardcoded JSON sample response string commented out with `//`. It includes a specific date (`2019-11-08`) and geographic coordinates, suggesting it was a debug stub. No comment explains its purpose, whether it is safe to remove, or what it was used for.

---

### B01-4 | MEDIUM | gps/unit.gps.jsp:9–31 | Complex scriptlet with no explanatory comment

The main scriptlet (lines 9–31) builds a raw JSON string by string concatenation — a non-trivial and fragile serialisation pattern. There is only a single terse inline comment (`//prepare the response here.` at line 16 and `//end of response preparation` at line 29). No comment explains: (a) why manual string concatenation is used instead of a JSON library, (b) the expected structure of the `arrGPSData` list elements (each element is written directly with `""+unitList.get(i)`, implying the list already holds pre-serialised JSON fragments — this is not obvious), or (c) the output contract (content-type, encoding).

---

### B01-5 | LOW | html-jsp/adminChecklist.jsp:1 | Missing page-level comment

No HTML or JSP comment near the top of the file describes the page's purpose, the required request attributes (`arrManufacturers`, `arrAdminUnitType`, `arrAdminUnitFuelType`, `arrAttachment`, `arrQuestions`), or the Struts action it posts to.

---

### B01-6 | LOW | html-jsp/adminChecklist.jsp:146–148 | Magic action strings without comment

The delete anchor (lines 144–149) uses `data-delete-action="question"` and `data-method-action="delete_questions"` — hard-coded action strings consumed by a shared JavaScript delete handler. No comment explains the convention or valid values for these attributes.

---

### B01-7 | LOW | html-jsp/adminChecklistEdit.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose, the expected `arrQuestions` / `arrAnswerType` request attributes, or the fact that this is a modal fragment rather than a standalone page.

---

### B01-8 | LOW | html-jsp/adminChecklistEdit.jsp:66 | Hard-coded hidden `action` value without comment

Line 66: `<input type="hidden" name="action" value="search"/>`. This element is inside the question-edit modal but its value is `"search"` — a non-obvious choice for an edit form. No comment explains why the action value is `"search"` (it may be a leftover or used to trigger a post-edit refresh query).

---

### B01-9 | LOW | html-jsp/adminCompany.jsp:1 | Missing page-level comment

No HTML or JSP comment near the top of the file describes the page's purpose or the required request attribute `subCompanyLst`.

---

### B01-10 | LOW | html-jsp/adminDealer.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose (converting a company to a dealer) or the required request attribute `arrCompanies` / `arrDealers`.

---

### B01-11 | LOW | html-jsp/adminDealer.jsp:16 | Absolute-path action attribute without comment

Line 16: `action="/dealerconvert.do"`. This uses an absolute path (leading `/`) unlike all other forms in the codebase that use relative paths (e.g., `action="fleetcheckconf.do"`). No comment explains the reason for the different path style, which could cause routing errors if the application is deployed to a non-root context path.

---

### B01-12 | LOW | html-jsp/adminGPS.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose, its dependency on a Google Maps / mapping library (`initialize()` is called but not defined in this file), or the meaning of the session attribute being read.

---

### B01-13 | LOW | html-jsp/adminGPS.jsp:3 | Non-obvious session attribute key `sessDateFormat`

Line 3: `session.getAttribute("sessDateFormat")`. The key `sessDateFormat` is not documented anywhere in this file. Its origin (set during login/session initialisation), its expected format string pattern (e.g., `"dd/MM/yyyy"`), and the transformation applied (`replaceAll("yyyy","yy").replaceAll("M","m")`) are all without explanation. The transformation is also lossy (single `M` replacement will also match `MM`).

---

### B01-14 | MEDIUM | html-jsp/adminGPS.jsp:3 | Scriptlet date-format transformation has undocumented lossy regex

Line 3:
```java
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy")
    .replaceAll("M", "m");
```
The second `replaceAll("M", "m")` will match both `M` (month) and the `m` in any other letter sequence if the format contains lowercase characters. More critically, it will transform both `M` and `MM` patterns identically. The variable `dateFormat` is computed but never actually used in the page body (it is not referenced in any `<%= %>` or JavaScript assignment visible in this file), making this dead computation. Neither the intent nor the outcome is documented.

---

### B01-15 | LOW | html-jsp/adminGPS.jsp:4 | Magic hardcoded `custCd = "0"` without comment

Line 4: `String custCd = "0";`. The value `"0"` is hardcoded with no comment explaining what customer code `0` represents, why it is hardcoded rather than read from the session or a request attribute, and how it affects the GPS data query.

---

### B01-16 | LOW | html-jsp/adminGPS.jsp:52 | Hardcoded default geographic coordinates without adequate comment

Line 52: `var defaultLoc = "-24.2761156,133.5912902"; //UK- 55.378051, -3.435973`

The inline comment says `//UK-` but the coordinates (`-24.2761156, 133.5912902`) are in Australia (near Alice Springs), not the UK. Lines 57–58 define `defaultLat`/`defaultLong` with the actual UK coordinates. The comment on line 52 is misleading — it appears to be a copy-paste remnant from when the UK coordinates were being noted for reference. The variable `defaultLoc` is set to AU coordinates but never used in any visible code in this file.

---

### B01-17 | HIGH | html-jsp/adminGPS.jsp:52 | Comment label "UK" attached to Australian coordinates

Line 52: `var defaultLoc = "-24.2761156,133.5912902"; //UK- 55.378051, -3.435973`

The variable value is the geographic centre of Australia. The comment reads `//UK-`. This is a dangerously inaccurate comment: any developer reading this line would believe `defaultLoc` holds UK coordinates. If `defaultLoc` were to be used as the fallback map centre, the map would open over Australia while the comment states it is the UK. This constitutes an inaccurate comment on a geographic value that could silently produce incorrect behaviour.

---

### B01-18 | LOW | html-jsp/adminGPS.jsp:54–55 | Commented-out coordinate variables with no explanation

Lines 54–55:
```javascript
// 	    var defaultLat = "-24.2761156"; //AU
// 	   	var defaultLong = "133.5912902";
```
These are commented out without explanation of when or why they were disabled, or whether the currently active lines 57–58 (UK coordinates) are the permanent replacement.

---

### B01-19 | MEDIUM | html-jsp/adminGPS.jsp:70–103 | Complex `fetchUnit` function with no comment and IE-specific dead branch

The `fetchUnit(str)` function (lines 70–103) contains a synchronous AJAX call (`async:false`) and an Internet Explorer ActiveXObject XML parsing branch (`jQuery.browser.msie` / `Microsoft.XMLDOM`). No comment explains: (a) the synchronous nature and its blocking implications, (b) that the IE branch is likely dead code given `jQuery.browser` was removed in jQuery 1.9, (c) the expected XML structure of the response, or (d) how `str` (the department code) is expected to be supplied. The function also references `document.forms[0].model_cd` — an implicit form index that is fragile and undocumented.

---

### B01-20 | LOW | html-jsp/adminJob.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose, the required request attribute `arrJobs`, or the fact that this is a modal fragment.

---

### B01-21 | LOW | html-jsp/adminJob.jsp:18,83–84 | Dead commented-out UI elements with no explanation

Line 18: `<!-- <input type="text" id="driver_name" ...> -->`
Lines 83–84: `<%-- <html:submit ... /> --%>` and `<!-- <input type="submit" ...> -->`

Three distinct UI elements (a driver name input and two alternative submit button implementations) are commented out with no explanation of why they were removed, whether they will be restored, or whether the replacement `<a>` element on line 85 is the intended permanent solution.

---

### B01-22 | LOW | html-jsp/adminJob.jsp:107–108 | Global variable declarations without comment

Lines 107–108:
```javascript
x = 0;
list = [];
```
These are implicit globals (no `var`/`let`/`const`). No comment explains their purpose or scope. `x` is a generic counter and `list` accumulates form references for `ajax_recaller`. The function `ajax_recaller` is called on line 117 but is not defined in this file — no comment identifies where it is defined.

---

### B01-23 | LOW | html-jsp/adminOperator.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose or the required request attribute `arrAdminDriver`.

---

### B01-24 | LOW | html-jsp/adminRegister.jsp:1 | Missing page-level comment

No HTML or JSP comment describes the page's purpose (new company self-registration), who can access it (it appears to be public/unauthenticated given it is the first registration step and redirects to `index.jsp` on back), or what `adminRegister.do` does upon submission.

---

### B01-25 | LOW | html-jsp/adminRegister.jsp:105 | Password field named `pin` without comment

Lines 102–110: The password `<input>` uses `name="pin"` rather than a conventional name like `password`. The `fnsubmitAccount()` JavaScript (line 154) reads it as `$('[name="pin"]').val()`. No comment explains why the field is named `pin` (historical naming convention, PIN-based auth, API contract requirement, etc.).

---

### B01-26 | LOW | html-jsp/adminRegister.jsp:123 | Stale developer note left in production markup

Line 123: `<!-- Change this to a button or input when using this as a form -->`

This is a developer TODO/note that was apparently not acted on and not removed. The surrounding element is a `<div>` containing `<html:button>` and `<a>` elements — the form already uses button and anchor elements. The comment is now inaccurate and misleading as stale guidance.

---

## Summary Table

| ID     | Severity | File:Line                        | Description                                                                 |
|--------|----------|----------------------------------|-----------------------------------------------------------------------------|
| B01-1  | LOW      | unit.gps.jsp:1                   | Missing page-level comment                                                  |
| B01-2  | LOW      | unit.gps.jsp:5,7                 | Dead commented-out imports (foreign package) with no explanation            |
| B01-3  | LOW      | unit.gps.jsp:28                  | Large commented-out magic JSON sample with no explanation                   |
| B01-4  | MEDIUM   | unit.gps.jsp:9–31                | Complex JSON-building scriptlet with insufficient commentary                |
| B01-5  | LOW      | adminChecklist.jsp:1             | Missing page-level comment                                                  |
| B01-6  | LOW      | adminChecklist.jsp:146–148       | Magic data-delete-action / data-method-action strings without comment       |
| B01-7  | LOW      | adminChecklistEdit.jsp:1         | Missing page-level comment                                                  |
| B01-8  | LOW      | adminChecklistEdit.jsp:66        | Hard-coded hidden action value "search" on an edit modal without comment    |
| B01-9  | LOW      | adminCompany.jsp:1               | Missing page-level comment                                                  |
| B01-10 | LOW      | adminDealer.jsp:1                | Missing page-level comment                                                  |
| B01-11 | LOW      | adminDealer.jsp:16               | Absolute-path action attribute without explanation                          |
| B01-12 | LOW      | adminGPS.jsp:1                   | Missing page-level comment                                                  |
| B01-13 | LOW      | adminGPS.jsp:3                   | Non-obvious session attribute key `sessDateFormat` not documented           |
| B01-14 | MEDIUM   | adminGPS.jsp:3                   | Lossy date-format regex transformation applied to unused variable           |
| B01-15 | LOW      | adminGPS.jsp:4                   | Magic hardcoded `custCd = "0"` without explanation                          |
| B01-16 | LOW      | adminGPS.jsp:52                  | `defaultLoc` set to AU coordinates; inline comment misleadingly labels them |
| B01-17 | HIGH     | adminGPS.jsp:52                  | Comment says "UK" but variable holds Australian coordinates                 |
| B01-18 | LOW      | adminGPS.jsp:54–55               | Commented-out AU coordinate variables with no explanation                   |
| B01-19 | MEDIUM   | adminGPS.jsp:70–103              | Complex fetchUnit function: synchronous AJAX, dead IE branch, undocumented  |
| B01-20 | LOW      | adminJob.jsp:1                   | Missing page-level comment                                                  |
| B01-21 | LOW      | adminJob.jsp:18,83–84            | Three dead commented-out UI elements with no explanation                    |
| B01-22 | LOW      | adminJob.jsp:107–108             | Implicit global variables; external dependency `ajax_recaller` undocumented |
| B01-23 | LOW      | adminOperator.jsp:1              | Missing page-level comment                                                  |
| B01-24 | LOW      | adminRegister.jsp:1              | Missing page-level comment                                                  |
| B01-25 | LOW      | adminRegister.jsp:105            | Password field named `pin` without explanation                              |
| B01-26 | LOW      | adminRegister.jsp:123            | Stale developer TODO comment left in production markup                      |

**Total findings: 26**
- HIGH: 1 (B01-17)
- MEDIUM: 3 (B01-4, B01-14, B01-19)
- LOW: 22
