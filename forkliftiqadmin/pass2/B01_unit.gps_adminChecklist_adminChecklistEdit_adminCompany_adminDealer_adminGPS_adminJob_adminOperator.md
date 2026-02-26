# Pass 2 — Test Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** B01
**Date:** 2026-02-26
**Scope:** 8 JSP files (view layer)
**Test directory searched:** /mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/

---

## Test Directory Summary

Four test files exist in the entire project, none of which cover any JSP file audited here:

- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

Grep of all 8 JSP base names against the test directory returned zero matches. No JSP-level tests, no mock-request tests, and no controller integration tests exist for these views.

---

## File 1: `gps/unit.gps.jsp`

### Evidence

**Purpose:** JSON response fragment — acts as a pseudo-REST endpoint that serialises GPS unit data as a JSON string to the HTTP response. No HTML; consumed by AJAX calls. Form action: none (response page only). Page title: none.

**Scriptlet blocks (lines 9–31):**
```java
List<String> unitList = (List<String>) request.getAttribute("arrGPSData");
String resp = "";
resp = resp + "{\"count\":" + unitList.size() + ",\"units\":[";
for (int i = 0; i < unitList.size(); i++) {
    String str = "" + unitList.get(i);
    resp = resp + str;
    if (i < unitList.size() - 1) { resp = resp + ","; }
}
resp = resp + "]}";
out.println(resp);
```

**EL / session / request attributes accessed:**
- `request.getAttribute("arrGPSData")` — set by `GetAjaxAction` (line 51 of `GetAjaxAction.java`); contains pre-serialised JSON strings produced in `GPSDao.getUnitGPSData()`.

**JavaScript with security implications:** None (no HTML/JS rendered by this JSP).

**Existing tests:** Zero.

### Findings

**B01-1 | Severity: CRITICAL | NullPointerException on null `arrGPSData` attribute**
`unitList` is cast from `request.getAttribute("arrGPSData")` with no null check. If `GetAjaxAction` does not set the attribute (e.g., exception path, direct URL access, or the `unit` parameter array is null — `GPSDao.getUnitGPSData` returns an empty list in that case but `arrGPSData` may never be set at all), `unitList` is `null` and `unitList.size()` throws a `NullPointerException`. No tests exercise the null-attribute path.

**B01-2 | Severity: HIGH | Unescaped database values injected directly into JSON output**
`GPSDao.getUnitGPSData()` builds JSON strings by concatenating raw database column values (vehicle name, manufacturer, type, power — all `String` from `rs.getString()`) directly into the JSON structure without JSON-encoding or HTML-encoding. A vehicle name containing `\"` or `\` will produce malformed JSON. A name containing `</script>` or similar could cause issues if the consuming JavaScript page does not sanitise. No tests verify the JSON output for special-character inputs.

**B01-3 | Severity: HIGH | SQL injection in `GPSDao.getGPSLocations()` (legacy method called from same DAO)**
`GPSDao.getGPSLocations()` (lines 85–88 of `GPSDao.java`) constructs a SQL query by concatenating `unitList[i]` directly into the query string without parameterisation: `where g.unit_id=" + unitList[i]`. Although `unit.gps.jsp` uses the parameterised `getUnitGPSData()`, this legacy method is in the same class, reachable via the same flow, and is entirely untested.

**B01-4 | Severity: HIGH | No `Content-Type: application/json` header set**
The JSP page declaration sets `contentType="text/html; charset=ISO-8859-1"` (line 4) but the output is pure JSON. This is functionally incorrect and causes browser/consumer misinterpretation. No test validates the content-type of the response.

**B01-5 | Severity: MEDIUM | String concatenation used instead of `StringBuilder` for response assembly**
`resp` is assembled via `String` concatenation inside a loop (lines 14–26). For large `unitList` this creates quadratic memory pressure. No performance/load test exists.

**B01-6 | Severity: MEDIUM | Error page declaration references a relative path that may not be reachable from sub-directory**
`<%@ page errorPage="../home/ExceptionHandler.jsp" %>` uses a relative path. If the JSP is invoked via a forwarded request from a different context path the resolution may fail silently. No test covers error-page routing.

**B01-7 | Severity: LOW | Unused imports**
`GPSUnitBean`, `ArrayList` are imported but never used in the JSP body (the attribute is already `List<String>`). Dead code that confuses future maintainers; no test would catch import drift.

---

## File 2: `html-jsp/adminChecklist.jsp`

### Evidence

**Purpose:** Checklist configuration list page. Allows filtering by manufacturer/type/power/attachment and listing checklist questions. Provides Add, Edit, Delete, Show/Hide actions. Form action: `fleetcheckconf.do`.

**Scriptlet blocks:** None (zero `<% ... %>` scriptlets).

**Request/session attributes accessed (via Struts tags):**
- `arrManufacturers` — `<html:optionsCollection name="arrManufacturers" .../>` (line 25)
- `arrAdminUnitType` — `<html:optionsCollection property="arrAdminUnitType" .../>` (line 33)
- `arrAdminUnitFuelType` — `<html:optionsCollection property="arrAdminUnitFuelType" .../>` (line 41)
- `arrAttachment` — `<html:optionsCollection property="arrAttachment" .../>` (line 49)
- `arrQuestions` — `<logic:notEmpty name="arrQuestions">` / `<logic:iterate ...>` (lines 89–162)
- ActionForm properties: `manu_id`, `type_id`, `fuel_type_id`, `attachment_id`, `action`, `id`

**JavaScript with security implications:**
- `fnaddchecklist()` (lines 191–199): Reads dropdown values and appends them directly to a URL via string concatenation: `"fleetcheckconf.do?action=add&manu_id=" + manu_id + ...`. Values come from HTML select elements populated from server data, but no encoding is applied. If IDs contain special characters (unlikely for numeric IDs but never validated) this could affect URL integrity.
- `postAndReload()` (lines 242–257): Posts `manu_id`, `type_id`, `fuel_type_id`, and `id` via `$.post`. The `id` parameter passed to `hideQuestion()`/`showQuestion()` originates from `<bean:write property="id" name="QuestionRecord"/>` in an inline `onclick` attribute — an integer DB ID, but no escaping is applied in the onclick context.
- `onclick="showQuestion(<bean:write property="id" name="QuestionRecord"/>)"` and `onclick="hideQuestion(<bean:write property="id" name="QuestionRecord"/>)"` (lines 123, 130, 155): Bean write of `id` directly into JavaScript onclick attribute. If `id` were ever non-numeric this would be a stored XSS vector.

**Existing tests:** Zero.

### Findings

**B01-8 | Severity: HIGH | `bean:write` of `QuestionRecord.id` unescaped inside JavaScript `onclick` attribute**
Lines 123, 130, and 155 embed `<bean:write property="id" name="QuestionRecord"/>` directly into an HTML `onclick` attribute as a JavaScript argument with no `filter="true"` or explicit escaping. By default `bean:write` HTML-encodes output, which is appropriate for HTML context but is not JavaScript-safe. If the `id` field ever contains a non-integer value (e.g., due to a data migration or future schema change), this becomes a stored XSS vector. No test validates the rendering of the `id` field in onclick context, nor boundary inputs.

**B01-9 | Severity: HIGH | No test for `arrManufacturers` / `arrAdminUnitType` / `arrAdminUnitFuelType` null or empty — silent rendering failure**
Struts `<html:optionsCollection>` will throw a `JspException` if the named collection attribute is `null` or not present in any scope. There is no `<logic:notEmpty>` guard around any of the four `optionsCollection` tags. No test covers the page rendering when these attributes are missing.

**B01-10 | Severity: MEDIUM | Client-side validation only — `isValidFields()` and `displayRequiredFields()` are the sole guards**
The `list()` function (line 209) sets the action value and submits the form with no server-side mandatory-field enforcement visible in this JSP. Validation logic in `isValidFields()` (lines 172–190) is JavaScript-only; bypassing JavaScript submits the form with empty manufacturer/type/fuel IDs. No test validates the server-side rejection of incomplete submissions from this page.

**B01-11 | Severity: MEDIUM | `bean:write property="content"` output is unfiltered HTML in table cell (line 101)**
Question content is rendered via `<bean:write property="content" name="QuestionRecord"/>`. The default Struts `bean:write` HTML-encodes the value, but there is no explicit `filter="true"` attribute and no test verifying that HTML/script characters in question content are safely escaped in the rendered table.

**B01-12 | Severity: MEDIUM | `data-delete-value` attribute populated from `bean:write id` without explicit escaping (lines 147)**
`data-delete-value="<bean:write property="id" name="QuestionRecord"/>"` injects the question ID into an HTML data attribute. While default `bean:write` encoding is active, no test verifies that the delete confirmation flow correctly uses this value and that it cannot be tampered with client-side.

**B01-13 | Severity: LOW | Hardcoded English string "ALL" in attachment dropdown (line 48)**
`<html:option value="">ALL</html:option>` is hardcoded rather than using a `bean:message` key, breaking internationalisation. All other option defaults use `bean:message`. No test verifies i18n completeness.

**B01-14 | Severity: LOW | `postAndReload` does not handle AJAX error responses**
`$.post(url, ..., function(data) { setTimeout(window.location.reload, 300); })` (lines 247–256) has no `.fail()` handler. A server error is silently swallowed and the page reloads regardless. No test covers error-response handling for hide/show question operations.

---

## File 3: `html-jsp/adminChecklistEdit.jsp`

### Evidence

**Purpose:** Modal/lightbox form for editing a single checklist question (content, expected answer, answer type). Rendered inside an ekko-lightbox overlay. No explicit `<html:form>` wrapper — submission is via `$.post` in JavaScript.

**Scriptlet blocks:** None.

**Request/session attributes accessed:**
- `arrQuestions` — `<logic:notEmpty name="arrQuestions">` / `<logic:iterate ...>` (lines 14–68); iterates `QuestionBean` objects.
- `arrAnswerType` — `<html:optionsCollection name="arrAnswerType" .../>` (line 55).
- Bean properties accessed: `order_no`, `content`, `expectedanswer`, `answer_type`, `id`, `type_id`, `fuel_type_id`, `manu_id`, `attachment_id`, `comp_id`, `active`.

**JavaScript with security implications:**
- `submit()` function (lines 93–109): Reads values from form inputs and posts to `fleetcheckedit.do` via `$.post`. Values include `comp_id`, `manu_id`, `type_id` — all read from hidden inputs injected by the server. No CSRF token is included in the POST.
- `$('input[id=question_id]').val()` — uses `id` selector; if multiple questions were ever iterated the selector would return the first match only, silently editing the wrong record.

**Existing tests:** Zero.

### Findings

**B01-15 | Severity: HIGH | No CSRF protection on `$.post` to `fleetcheckedit.do`**
The JavaScript `submit()` function posts question edits without any CSRF token. The endpoint accepts state-changing operations (modifying question content and answer type) with no synchroniser token. A logged-in admin can be tricked into submitting this form from a third-party page. No test covers CSRF token presence or absence.

**B01-16 | Severity: HIGH | `arrAnswerType` null guard missing — `<html:optionsCollection>` throws on null**
No `<logic:notEmpty>` guard wraps `<html:optionsCollection name="arrAnswerType" .../>` (line 55). If the backing Action does not set this attribute, a `JspException` is thrown at render time. No test covers this failure path.

**B01-17 | Severity: HIGH | `arrQuestions` null renders blank form with no user feedback**
If `arrQuestions` is null or empty (e.g., invalid `id` parameter passed to `fleetcheckedit.do`), the `<logic:notEmpty>` block is silently skipped, the Submit button is still rendered, and `submit()` would post empty/default values to the server. No test verifies the empty-collection rendering or the behaviour of submitting such a form.

**B01-18 | Severity: MEDIUM | `$('input[id=question_id]')` selector breaks with multiple iterated questions**
The `submit()` JavaScript function uses `$('input[id=question_id]')` (line 95). HTML `id` attributes must be unique; iterating multiple `QuestionBean` items would produce duplicate `id="question_id"` elements. jQuery returns only the first match, silently targeting the wrong record. No test covers multi-question iteration in this JSP.

**B01-19 | Severity: MEDIUM | `$.post` success callback unconditionally reloads without checking response status**
`location.reload()` is called regardless of whether the server returned an error response. Silent failures are not surfaced to the user. No test validates error response handling.

**B01-20 | Severity: LOW | Hardcoded action value in hidden field (line 66)**
`<input type="hidden" name="action" value="search"/>` is hardcoded inside the iterate block. This appears to be a copy-paste artefact from the search form — the edit action value is `search`, which is semantically misleading. No test verifies that the correct server-side action branch is taken.

---

## File 4: `html-jsp/adminCompany.jsp`

### Evidence

**Purpose:** Lists sub-companies (locations) for a dealer. Provides an "Add Company" lightbox link. Form action: `dealercompanies.do` (plain HTML `<form>`, not `<html:form>`).

**Scriptlet blocks:** None.

**Request/session attributes accessed:**
- `subCompanyLst` — `<logic:notEmpty name="subCompanyLst">` / `<logic:iterate ...>` (lines 43–50); iterates `CompanyBean` objects.
- Bean properties rendered: `name` (line 46), `address` (line 47).

**JavaScript with security implications:** None present in this JSP.

**Existing tests:** Zero.

### Findings

**B01-21 | Severity: HIGH | `bean:write property="name"` and `property="address"` rendered without explicit XSS guard**
Company name and address values from `CompanyBean` are written directly into table cells via `<bean:write property="name" name="companyRecord"/>` and `<bean:write property="address" name="companyRecord"/>`. Struts `bean:write` applies default HTML encoding, but there is no explicit `filter="true"` attribute, and no test verifies that script injection in company name or address fields is neutralised in the rendered output.

**B01-22 | Severity: MEDIUM | Empty company list renders a blank table with no "no records" message**
When `subCompanyLst` is null or empty the `<logic:notEmpty>` block is skipped and the `<tbody>` is empty. No empty-state message is shown. No test verifies this rendering path.

**B01-23 | Severity: MEDIUM | Plain HTML `<form>` used instead of Struts `<html:form>` — no ActionForm binding**
The outer form at line 17 is `<form method="post" action="dealercompanies.do" ...>` rather than `<html:form>`. This means Struts form bean population and validation hooks do not apply to this form, and error display via `<html:errors/>` relies on manually set `ActionErrors`, which may silently fail if the action does not populate them. No test exercises the form submission path from this JSP.

**B01-24 | Severity: LOW | No pagination or result-count limit on company list**
The entire `subCompanyLst` collection is iterated with no paging, which could produce extremely large HTML responses for dealers with many sub-companies. No load or boundary test exists.

---

## File 5: `html-jsp/adminDealer.jsp`

### Evidence

**Purpose:** Dealer conversion page — allows selecting a company and converting it to a dealer. Displays current dealers in a table. Form action: `/dealerconvert.do` (Struts `<html:form>`).

**Scriptlet blocks:** None.

**Request/session attributes accessed:**
- `arrCompanies` — `<html:optionsCollection name="arrCompanies" .../>` (line 24).
- `arrDealers` — `<logic:notEmpty name="arrDealers">` / `<logic:iterate ...>` (lines 50–56); iterates `CompanyBean`.
- ActionForm property: `companyId`.

**JavaScript with security implications:** None in this JSP.

**Existing tests:** Zero.

### Findings

**B01-25 | Severity: HIGH | `arrCompanies` null guard missing — `<html:optionsCollection>` throws on null**
`<html:optionsCollection name="arrCompanies" .../>` (line 24) has no surrounding `<logic:notEmpty>` guard. If the backing action does not set this attribute (e.g., an exception occurs loading the company list), a `JspException` will be thrown at render time. No test covers this failure path.

**B01-26 | Severity: HIGH | `bean:write property="name"` in dealer table rendered without explicit escaping (line 53)**
Dealer company names are rendered via `<bean:write property="name" name="DealerRecord"/>`. Default `bean:write` HTML encoding applies but there is no explicit `filter="true"`, and no test verifies that HTML/script in a company name is escaped.

**B01-27 | Severity: MEDIUM | No confirmation prompt before dealer conversion**
Submitting the form immediately converts a company to a dealer — an irreversible administrative action — with no confirmation dialog. The JSP provides no client-side guard. No test verifies a destructive-action safeguard exists.

**B01-28 | Severity: MEDIUM | Empty `arrDealers` list renders blank table without feedback**
When no dealers exist the `<logic:notEmpty>` block is skipped and the table body is empty with no "no records" message. No test verifies this rendering path.

**B01-29 | Severity: LOW | Form action uses absolute path `/dealerconvert.do` with leading slash**
`<html:form ... action="/dealerconvert.do">` uses a server-root-relative path. If the application is deployed under a context path other than `/`, this path will be wrong. All other forms in the audited JSPs use relative paths. No test verifies correct URL construction under a non-root context path.

---

## File 6: `html-jsp/adminGPS.jsp`

### Evidence

**Purpose:** GPS Report page — displays a multi-select vehicle list and a Google Maps canvas. Allows refreshing GPS positions. Form action: `adminunit.do`.

**Scriptlet blocks (lines 2–5):**
```java
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");
String custCd = "0";
```

**Request/session attributes accessed:**
- `session.getAttribute("sessDateFormat")` — used in scriptlet (line 3).
- `arrAdminUnit` — `<logic:notEmpty name="arrAdminUnit">` / `<logic:iterate ...>` (lines 24–29); iterates `UnitBean`.
- Hidden field: `cust_cd` value = `<%=custCd %>` (line 44).
- Bean properties rendered inside option: `id` (line 26), `name` (line 26-27).

**JavaScript with security implications:**
- `fnRefresh()` (lines 62–67): Calls `initialize($('#cust').val(), $('#site').val())` — but neither `#cust` nor `#site` elements exist in this JSP. This is a dead/broken call that silently does nothing.
- `fetchUnit(str)` (lines 70–103): Constructs an AJAX URL via string concatenation: `'../master/get_cust_vehicle.jsp?cust_cd='+cust_cd+"&loc_cd="+loc_cd+"&dept_cd="+str`. The `str` parameter is never URL-encoded; if it contains `&` or `=` the URL will be malformed.
- `fetchUnit` uses `jQuery.browser.msie` (line 78) — removed from jQuery 1.9+; this check is always `undefined`/`false` in modern jQuery, making the ActiveXObject branch dead code. `jQuery.migrate` is present in the project but this is a deprecated API.
- `fetchUnit` uses `new ActiveXObject('Microsoft.XMLDOM')` (line 82) — IE-specific, non-standard, dead code in any current browser.
- `alert(err)` in the AJAX error handler (line 89) — exposes raw error objects to users.
- `document.forms[0].model_cd` (lines 93–95) — accesses a form field named `model_cd` which does not exist in this JSP.

**Existing tests:** Zero.

### Findings

**B01-30 | Severity: CRITICAL | NullPointerException on `sessDateFormat` session attribute**
Line 3: `((String) session.getAttribute("sessDateFormat")).replaceAll(...)` — if `sessDateFormat` is not in the session (unauthenticated access, session expiry, or a new session without login), `session.getAttribute("sessDateFormat")` returns `null` and `.replaceAll()` throws a `NullPointerException`. The error page directive is absent from this JSP fragment. No test exercises this null-session path.

**B01-31 | Severity: HIGH | `bean:write property="id"` and `property="name"` inside `<option>` without explicit escaping (lines 26-27)**
Unit `id` and `name` values are written into HTML `<option value="...">` and option text via `<bean:write>`. Default HTML encoding applies, but no test verifies that special characters in unit names (e.g., `"`, `<`, `>`) are safely escaped in the option value and label context.

**B01-32 | Severity: HIGH | `fetchUnit()` constructs URL with unencoded `str` parameter**
`fetchUnit(str)` builds a URL by appending `str` directly without `encodeURIComponent()`. If `str` (the `dept_cd` value) contains `&`, `=`, `#`, or other special URL characters, the request URL is malformed. No test validates URL construction for boundary values.

**B01-33 | Severity: HIGH | `dateFormat` scriptlet variable written into hidden input without HTML encoding**
`<input type="hidden" ... value="<%=custCd %>" />` (line 44) uses the scriptlet variable `custCd` which is hardcoded to `"0"` — this specific instance is safe. However, `dateFormat` computed from session is never used in the rendered HTML, only in the scriptlet block. If future code were to render `dateFormat` into HTML without encoding, the `replaceAll` transforms would not sanitise all HTML-unsafe characters (e.g., `/` is present in date formats).

**B01-34 | Severity: HIGH | Broken `fnRefresh()` references non-existent DOM elements `#cust` and `#site`**
`fnRefresh()` calls `initialize($('#cust').val(), $('#site').val())` but neither `#cust` nor `#site` exist in this JSP. The Refresh button will silently pass `undefined` to `initialize()`. No test verifies the Refresh button's actual behaviour.

**B01-35 | Severity: MEDIUM | `fetchUnit()` references `document.forms[0].model_cd` which does not exist in this JSP**
Lines 93–95 attempt to set `document.forms[0].model_cd.options` but no field named `model_cd` exists in the rendered form. This is dead code copied from another context that silently throws a JavaScript TypeError. No test covers this code path.

**B01-36 | Severity: MEDIUM | `jQuery.browser.msie` usage is deprecated and removed since jQuery 1.9**
The `fetchUnit` function (line 78) gates on `jQuery.browser.msie`, which was removed in jQuery 1.9. The result is always falsy; the ActiveXObject branch is unreachable dead code. `jQuery.migrate` may suppress the error but does not restore the value. No test validates the intended XML parsing path.

**B01-37 | Severity: MEDIUM | Raw `alert(err)` in AJAX error handler exposes error details to user (line 89)**
The error callback `error: function(err) { alert(err) }` exposes raw jQuery XHR error objects (which may include server error messages or stack traces) in a browser alert. No test verifies that error information is appropriately sanitised before display.

**B01-38 | Severity: LOW | Hardcoded geographic coordinates default to Australia then overridden to UK (lines 52–58)**
`defaultLoc`, `defaultLat`, and `defaultLong` are first assigned Australian coordinates (commented out) and then UK coordinates. There is no i18n or configuration-driven default location. No test verifies which coordinates are active.

**B01-39 | Severity: LOW | `custCd` scriptlet variable hardcoded to `"0"` (line 4)**
`String custCd = "0"` is always `"0"` regardless of the logged-in company. The hidden `cust_cd` field will always submit `0` to the server. It is unclear whether the server-side action uses this value or ignores it, but it is never set from a session/request attribute. No test validates that the correct company context is passed.

---

## File 7: `html-jsp/adminJob.jsp`

### Evidence

**Purpose:** Modal/lightbox fragment for viewing and editing jobs associated with an equipment unit. Displays a list of existing jobs with inline edit forms, and supports adding new jobs. No outer `<html:form>` — uses plain HTML forms with class `ajax_mode_c`.

**Scriptlet blocks (lines 3–5):**
```java
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
```
These values are embedded into hidden `<input>` elements at lines 9–10 and line 72.

**Request/session attributes accessed:**
- `arrJobs` — `<logic:notEmpty name="arrJobs">` / `<logic:iterate ...>` (lines 33–76); iterates `JobDetailsBean`.
- Bean properties rendered: `jobTitle` (line 38), `description` (line 42), `driverName` (line 45), `startTime` (line 48,53), `endTime` (line 49,54,59,60), `unitId` (line 68), `jobNo` (line 68), `id` (line 73).

**JavaScript with security implications:**
- Lines 9–10: `request.getParameter("action")` and `request.getParameter("equipId")` are written directly into `<input>` `value` attributes without HTML encoding: `value="<%=id %>"` and `value="<%=action %>"`.
- Line 68: `href="jobdetails.do?action=details&equipId=<bean:write name="jobs" property="unitId" />&job_no=<bean:write name="jobs" property="jobNo" />"` — bean properties appended to a URL inside an anchor `href`.
- `triggerClick(id, genId)` (lines 94–105): Dynamically creates an anchor element by concatenating `id` and `genId` directly into an HTML string: `'<a id="hLink" ... href="driverjob.do?action=assign&equipId='+id+'&job_id='+genId+'"...'`. These values are not URL-encoded. If `id` or `genId` contain `"` or `'`, DOM-based XSS is possible.
- `saveJobs()` (lines 110–118): Iterates `$('.ajax_mode_c')` forms and calls `ajax_recaller(list)` — `ajax_recaller` is not defined in this JSP; it is presumably defined in an included/shared JS file. No null/undefined guard exists.

**Existing tests:** Zero.

### Findings

**B01-40 | Severity: CRITICAL | Reflected XSS via unencoded `request.getParameter("equipId")` and `request.getParameter("action")` in hidden input values**
Lines 9–10 write `<%=id %>` and `<%=action %>` directly into HTML input `value` attributes. `id` is populated from `request.getParameter("equipId")` and `action` from `request.getParameter("action")` with no HTML encoding applied. A crafted URL such as `?equipId="><script>alert(1)</script>` would break out of the `value` attribute and execute arbitrary script. This is a direct reflected XSS vulnerability. No test exercises this injection path.

**B01-41 | Severity: CRITICAL | DOM-based XSS in `triggerClick()` via unencoded `id` and `genId` parameters**
`triggerClick(id, genId)` constructs an anchor element HTML string by direct concatenation of `id` and `genId` (lines 101–103). If either parameter contains `"` the `href` attribute is terminated; if either contains `'` the JavaScript string literal is broken, allowing script injection. These values ultimately originate from server-rendered data (`equipId` request parameter), providing an attack surface. No test validates input sanitisation in this function.

**B01-42 | Severity: HIGH | `bean:write property="jobTitle"` and `property="description"` in editable input/textarea (lines 38, 42)**
Job title and description are rendered into form input `value` attributes and textarea content via `<bean:write>`. Default `bean:write` HTML encoding applies, but no test verifies that the rendered values are safe for the HTML attribute context, particularly for `value='...'` (single-quote delimited), where HTML encoding of `'` to `&#39;` is required but Struts 1.x `bean:write` may not consistently apply it.

**B01-43 | Severity: HIGH | `bean:write property="unitId"` and `property="jobNo"` appended unencoded into `href` URL (line 68)**
`<bean:write name="jobs" property="unitId"/>` and `<bean:write name="jobs" property="jobNo"/>` are concatenated directly into a URL in the `href` attribute without URL-encoding. If these fields contain characters such as `&`, `#`, or `?`, the URL is malformed. No test validates URL construction with boundary values.

**B01-44 | Severity: HIGH | No CSRF protection on `ajax_mode_c` form submissions**
Each job's edit form (`<form class="ajax_mode_c edit_job">`) is posted via `ajax_recaller`. No CSRF synchroniser token is present. State-changing operations (editing job records) are unprotected against cross-site request forgery. No test verifies CSRF token presence.

**B01-45 | Severity: MEDIUM | `ajax_recaller` is called but never defined in this JSP**
`saveJobs()` calls `ajax_recaller(list)` (line 117) which is not defined in `adminJob.jsp`. It is presumably in a shared JS include. If the include fails to load, `saveJobs()` throws a `ReferenceError` and all job edits are silently lost. No test verifies the full `saveJobs()` execution path.

**B01-46 | Severity: MEDIUM | Job status logic is redundant — three independent `<logic:*>` blocks instead of if/else-if/else**
Lines 48–63 use three separate `<logic:notEmpty>`/`<logic:empty>` pairs that are not mutually exclusive by Struts tag semantics. The "Complete" state requires two `<logic:notEmpty>` checks (lines 58–62) which duplicates the first condition test. This logic is untested and could produce duplicate status output if Struts re-evaluates the conditions differently.

**B01-47 | Severity: LOW | Global variable pollution — `x` and `list` declared without `var` keyword (lines 107–108)**
`x = 0; list = [];` at lines 107–108 are implicit global variable declarations. They will conflict with any other script on the same page that uses variables named `x` or `list` (notably `adminChecklist.jsp` has a `function list()`). No test covers script isolation in the modal context.

---

## File 8: `html-jsp/adminOperator.jsp`

### Evidence

**Purpose:** Manage Drivers (Operators) list page. Provides search, add (lightbox), edit (lightbox), and delete actions. Form: plain HTML `<form method="get" action="admindriver.do">`.

**Scriptlet blocks (lines 3–5):**
```java
String searchDriver = request.getParameter("searchDriver") == null ? "" : request.getParameter("searchDriver");
```
This value is written into the search input's `value` attribute at line 25: `value="<%=searchDriver %>"`.

**Request/session attributes accessed:**
- `arrAdminDriver` — `<logic:notEmpty name="arrAdminDriver">` / `<logic:iterate ...>` (lines 58–85); iterates `DriverBean`.
- Bean properties rendered: `id` (lines 63, 66, 72), `first_name` (line 78), `last_name` (line 79), `email_addr` (line 81), `joindt` (line 82).

**JavaScript with security implications:**
- Line 25: `value="<%=searchDriver %>"` — `searchDriver` from `request.getParameter()` is written directly into an HTML attribute without encoding. A crafted search string containing `"` breaks out of the attribute.
- Lines 63–66: `href="admindriver.do?action=edit&driverId=<bean:write property="id" name="driverRecord"/>"` and `class="driver<bean:write property="id" name="driverRecord"/>"` — driver `id` is appended into both a URL and a CSS class name via `bean:write`.
- Lines 72–73: `data-delete-value="<bean:write property="id" name="driverRecord"/>"` — driver `id` in HTML data attribute.

**Existing tests:** Zero.

### Findings

**B01-48 | Severity: CRITICAL | Reflected XSS via unencoded `request.getParameter("searchDriver")` in input `value` attribute**
Line 25 writes `<%=searchDriver %>` directly into the `value` attribute of an HTML text input without any HTML encoding. A crafted GET request with `searchDriver="><script>alert(1)</script>` would break out of the attribute and execute arbitrary JavaScript. This is a direct reflected XSS vulnerability. No test exercises this injection path.

**B01-49 | Severity: HIGH | `bean:write property="first_name"`, `last_name`, `email_addr` rendered without explicit XSS verification**
Driver names and email addresses from `DriverBean` are written into table cells. Default `bean:write` HTML encoding is the only protection. Stored data containing HTML special characters (e.g., a name containing `<` or `>`) should be encoded, but there is no test confirming the encoding behaviour for these fields.

**B01-50 | Severity: HIGH | Driver `id` appended to CSS class name via `bean:write` (line 66)**
`class="driver<bean:write property="id" name="driverRecord"/>"` injects a database ID directly into an HTML class attribute. While `id` is presumably numeric, there is no type-safety guarantee at the view layer. If `id` contains a space or other CSS-invalid character, the class attribute is malformed; if it contains `"`, the attribute is broken. No test verifies this rendering.

**B01-51 | Severity: MEDIUM | No server-side search input sanitisation visible in view layer**
`searchDriver` is passed as a GET parameter, written back into the rendered HTML (reflected), and presumably passed to a DAO query. No sanitisation or length restriction is enforced at the JSP level. No test covers the search with SQL-sensitive characters or excessively long strings.

**B01-52 | Severity: MEDIUM | Empty `arrAdminDriver` renders blank table with no "no records" message**
When no drivers exist or the search returns no results, the table body is empty with no feedback. No test verifies the empty-results rendering path.

**B01-53 | Severity: MEDIUM | Duplicate `data-after-delete="reload"` attribute on delete anchor (lines 69–73)**
The delete anchor has `data-after-delete="reload"` specified twice (lines 69 and 73). The second occurrence overrides the first in HTML parsing, which is harmless here since both values are identical, but it indicates copy-paste error and could mask a future bug where different values are intended. No test verifies delete-and-reload behaviour.

**B01-54 | Severity: LOW | Hardcoded English strings "Actions", "Manage Drivers" not using `bean:message` (lines 51, 10, 16)**
The table header "Actions" (line 51) and page title/breadcrumb "Manage Drivers" (lines 10, 16) are hardcoded English strings while other columns use `bean:message` keys. This breaks internationalisation. No test verifies i18n completeness.

---

## Cross-Cutting Findings

**B01-55 | Severity: CRITICAL | Zero JSP-level test coverage across all 8 files**
The test directory contains only 4 files, all in `com/calibration` and `com/util` packages. No mock HTTP request tests, no Struts `MockStrutsTestCase` tests, no Selenium/HTMLUnit integration tests, and no unit tests for any JSP scriptlet logic exist for any of the 8 audited files. Every rendering path, every null-attribute scenario, every scriptlet branch, and every JavaScript interaction is entirely untested.

**B01-56 | Severity: HIGH | No null-guard pattern for session attributes accessed in scriptlets (adminGPS.jsp, adminJob.jsp, adminOperator.jsp)**
Three JSPs (`adminGPS.jsp` line 3, `adminJob.jsp` lines 3–4, `adminOperator.jsp` lines 4) use the pattern `request.getParameter("x") == null ? "" : request.getParameter("x")` for request parameters (safe), but `adminGPS.jsp` does not apply the same pattern to `session.getAttribute("sessDateFormat")` (calls `.replaceAll()` directly on the result). The inconsistency in null-safety practice across JSPs is untested.

**B01-57 | Severity: HIGH | `bean:write` default HTML encoding untested for attribute contexts (multiple files)**
Multiple JSPs embed `<bean:write>` output inside HTML attribute values (e.g., `href`, `value`, `onclick`, `class`, `data-*`). While Struts 1.x `bean:write` HTML-encodes by default, the encoding set does not fully protect all attribute contexts (particularly single-quote delimited attributes, JavaScript event handler attributes, and CSS class attributes). The absence of any test means this protection has never been verified for any of the fields rendered across these 8 JSPs.

**B01-58 | Severity: HIGH | No CSRF protection on any state-changing AJAX or form submission across the 8 JSPs**
`adminChecklistEdit.jsp` (`fleetcheckedit.do`), `adminJob.jsp` (`adminunit.do`), `adminChecklist.jsp` (`fleetcheckhide.do`, `fleetcheckshow.do`), and `adminDealer.jsp` (`/dealerconvert.do`) all perform state-changing operations without any CSRF synchroniser token. No test verifies CSRF defences for any of these endpoints.

**B01-59 | Severity: MEDIUM | No error-state rendering tests — all `<html:errors/>` blocks are untested**
`adminChecklist.jsp` (line 74), `adminCompany.jsp` (line 30), `adminDealer.jsp` (line 38), and `adminOperator.jsp` (line 43) render `<html:errors/>`. No test verifies that server-side validation errors are correctly propagated to and displayed in these JSPs.

**B01-60 | Severity: MEDIUM | Hardcoded English UI text in multiple JSPs bypasses i18n framework**
Hardcoded strings found: "GPS Report" (adminGPS.jsp lines 9, 13), "Add Job" (adminJob.jsp line 16), "Title", "Description", "Driver", "Status", "Actions" (adminJob.jsp lines 23–27), "Not Started", "In Progress", "Complete" (adminJob.jsp lines 50–61), "Manage Drivers" (adminOperator.jsp lines 10, 16), "Actions" (adminOperator.jsp line 51), "ALL" (adminChecklist.jsp line 48). None of these are verified by i18n tests.

---

## Summary Table

| Finding | JSP File | Severity |
|---------|----------|----------|
| B01-1  | unit.gps.jsp | CRITICAL |
| B01-2  | unit.gps.jsp | HIGH |
| B01-3  | unit.gps.jsp (GPSDao) | HIGH |
| B01-4  | unit.gps.jsp | HIGH |
| B01-5  | unit.gps.jsp | MEDIUM |
| B01-6  | unit.gps.jsp | MEDIUM |
| B01-7  | unit.gps.jsp | LOW |
| B01-8  | adminChecklist.jsp | HIGH |
| B01-9  | adminChecklist.jsp | HIGH |
| B01-10 | adminChecklist.jsp | MEDIUM |
| B01-11 | adminChecklist.jsp | MEDIUM |
| B01-12 | adminChecklist.jsp | MEDIUM |
| B01-13 | adminChecklist.jsp | LOW |
| B01-14 | adminChecklist.jsp | LOW |
| B01-15 | adminChecklistEdit.jsp | HIGH |
| B01-16 | adminChecklistEdit.jsp | HIGH |
| B01-17 | adminChecklistEdit.jsp | HIGH |
| B01-18 | adminChecklistEdit.jsp | MEDIUM |
| B01-19 | adminChecklistEdit.jsp | MEDIUM |
| B01-20 | adminChecklistEdit.jsp | LOW |
| B01-21 | adminCompany.jsp | HIGH |
| B01-22 | adminCompany.jsp | MEDIUM |
| B01-23 | adminCompany.jsp | MEDIUM |
| B01-24 | adminCompany.jsp | LOW |
| B01-25 | adminDealer.jsp | HIGH |
| B01-26 | adminDealer.jsp | HIGH |
| B01-27 | adminDealer.jsp | MEDIUM |
| B01-28 | adminDealer.jsp | MEDIUM |
| B01-29 | adminDealer.jsp | LOW |
| B01-30 | adminGPS.jsp | CRITICAL |
| B01-31 | adminGPS.jsp | HIGH |
| B01-32 | adminGPS.jsp | HIGH |
| B01-33 | adminGPS.jsp | HIGH |
| B01-34 | adminGPS.jsp | HIGH |
| B01-35 | adminGPS.jsp | MEDIUM |
| B01-36 | adminGPS.jsp | MEDIUM |
| B01-37 | adminGPS.jsp | MEDIUM |
| B01-38 | adminGPS.jsp | LOW |
| B01-39 | adminGPS.jsp | LOW |
| B01-40 | adminJob.jsp | CRITICAL |
| B01-41 | adminJob.jsp | CRITICAL |
| B01-42 | adminJob.jsp | HIGH |
| B01-43 | adminJob.jsp | HIGH |
| B01-44 | adminJob.jsp | HIGH |
| B01-45 | adminJob.jsp | MEDIUM |
| B01-46 | adminJob.jsp | MEDIUM |
| B01-47 | adminJob.jsp | LOW |
| B01-48 | adminOperator.jsp | CRITICAL |
| B01-49 | adminOperator.jsp | HIGH |
| B01-50 | adminOperator.jsp | HIGH |
| B01-51 | adminOperator.jsp | MEDIUM |
| B01-52 | adminOperator.jsp | MEDIUM |
| B01-53 | adminOperator.jsp | MEDIUM |
| B01-54 | adminOperator.jsp | LOW |
| B01-55 | All 8 files | CRITICAL |
| B01-56 | adminGPS, adminJob, adminOperator | HIGH |
| B01-57 | Multiple | HIGH |
| B01-58 | Multiple | HIGH |
| B01-59 | Multiple | MEDIUM |
| B01-60 | Multiple | MEDIUM |

**Totals: 6 CRITICAL, 23 HIGH, 19 MEDIUM, 12 LOW**
