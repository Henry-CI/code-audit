# Pass 2 Audit Report — B01
## JSP View Files: GPS and Admin Views

**Auditor:** B01
**Date:** 2026-02-26
**Audit pass:** 2 (Test-coverage + view-layer security)
**Test directory:** `src/test/java/`

---

## 1. Reading Evidence

### 1.1 `gps/unit.gps.jsp`

**File:** `src/main/webapp/gps/unit.gps.jsp`
**Purpose:** JSON response generator for GPS unit data. Reached via the `/getAjaxGPS.do` Struts action (`GetAjaxAction`). Renders a bare JSON payload (no HTML wrapper) containing GPS coordinates and vehicle metadata for one or more units.

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 9–31 | Single large scriptlet that casts `request.getAttribute("arrGPSData")` to `List<String>`, iterates the list, concatenates each pre-built JSON string, and calls `out.println(resp)` — no HTML or JSP output outside this scriptlet. |
| 11 | `List<String> unitList = (List<String>)request.getAttribute("arrGPSData");` — unchecked cast, no null guard. |
| 14 | `resp = resp+"{\"count\":"+unitList.size()+","` — NPE if `arrGPSData` was not set (i.e., action parameter was not `last_gps`). |
| 30 | `out.println(resp)` — raw print of constructed JSON string. |

**EL expressions:** None.

**Session variables accessed:** None directly in the JSP; session access occurs in the backing `GetAjaxAction`.

**Forms / action URLs:** None; this is a response-only view.

**Error page directive:** `<%@ page errorPage="../home/ExceptionHandler.jsp" %>` (line 6).

**Backing action:** `GetAjaxAction` (`/getAjaxGPS.do`)
- Line 46: `String compId = request.getParameter("compId")==null?"0":request.getParameter("compId");` — compId taken from request, not session.
- Line 47: `((String) request.getSession().getAttribute("sessDateFormat")).replaceAll(...)` — chained call with no null check on the cast result.
- Line 51: `GPSDao.getUnitGPSData(compId, unit, dateTimeFormat, timezone)` — compId accepted but `QUERY_UNIT_GPS` SQL does not include a `comp_id` filter; query filters only by `unit_id`.

**JSON construction in `GPSDao.getUnitGPSData` (lines 64–65):**
```java
String gps_str = "{\"name\":\""+unitBean.getVehName()+"\",\"status\":1,\"lat\":"+unitBean.getLatitude()
    +",\"lon\":"+unitBean.getLongitude()+"\",\"manufacturer\":\""+unitBean.getManufacturer()
    +"\",...}";
```
Fields (`vehName`, `manufacturer`, `type`, `power`) are DB-sourced strings inserted directly into JSON by string concatenation — no JSON serialiser is used.

---

### 1.2 `html-jsp/adminChecklist.jsp`

**File:** `src/main/webapp/html-jsp/adminChecklist.jsp`
**Purpose:** Admin checklist management view. Lists pre-operation checklist questions filtered by manufacturer, unit type, and fuel type. Allows adding, editing, hiding, showing, and deleting questions. Backed by `/fleetcheckconf.do` (`AdminFleetcheckAction`). Reached via `adminChecklistDefinition` tile which extends `adminDefinition` (authenticated layout).

**Key scriptlets:** None (uses Struts tags throughout).

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<html:optionsCollection name="arrManufacturers" .../>` | Line 25 | Request-scoped bean |
| `<logic:iterate name="arrQuestions" id="QuestionRecord" type="com.bean.QuestionBean">` | Line 90 | Iterates request attribute |
| `<bean:write property="order_no" name="QuestionRecord"/>` | Line 98 | Numeric order field |
| `<bean:write property="content" name="QuestionRecord"/>` | Line 101 | Question text — user-supplied content |
| `<bean:write property="id" name="QuestionRecord"/>` | Lines 123, 130, 138, 147, 155 | Used inside `onclick=` JS calls and `href=` URL |
| `<html:hidden property="action" styleClass="chkact" value=""/>` | Line 70 | Hidden field with empty value, set by JS |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `fleetcheckconf.do` | POST | Main filter/list form |
| `./fleetcheckhide.do` (AJAX POST via JS) | POST | `postAndReload()` function, lines 235–256 |
| `./fleetcheckshow.do` (AJAX POST via JS) | POST | Same function |
| `fleetcheckconf.do?action=add&manu_id=...` (lightbox link built in JS) | GET | `fnaddchecklist()`, line 195 |

**JavaScript:**  Lines 172–272 contain inline client-side validation (`isValidFields()`), AJAX post helpers (`postAndReload()`), and form submission logic (`list()`).

---

### 1.3 `html-jsp/adminChecklistEdit.jsp`

**File:** `src/main/webapp/html-jsp/adminChecklistEdit.jsp`
**Purpose:** Modal edit form for a single checklist question. Loaded in a lightbox via `/fleetcheckedit.do` (`AdminFleetcheckEditAction`). Allows editing question text, expected answer, and answer type. Backed by `adminChecklistEditDefinition` tile which extends `loginDefinition` (header-only, unauthenticated-style layout — popup context).

**Key scriptlets:** None (uses Struts tags throughout).

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<logic:iterate name="arrQuestions" id="question" type="com.bean.QuestionBean">` | Line 15 | Iterates single question bean |
| `<html:textarea property="content" name="question"/>` | Lines 25–29 | Editable question text |
| `<html:hidden property="id" name="question" styleId="question_id"/>` | Line 59 | Question ID in hidden input |
| `<html:hidden property="comp_id" name="question"/>` | Line 64 | Company ID passed through form — client-side |
| `<html:hidden property="active" name="question"/>` | Line 65 | Active flag in hidden input |
| `<input type="hidden" name="action" value="search"/>` | Line 66 | Hardcoded hidden action field |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `fleetcheckedit.do` (AJAX POST via JS `submit()`, line 94) | POST | Client-side JS reads all hidden fields and posts |

**JavaScript:** Lines 82–114 contain `fntoogleDiv()` (show/hide answer type section) and `submit()` (jQuery AJAX POST with all form fields).

---

### 1.4 `html-jsp/adminCompany.jsp`

**File:** `src/main/webapp/html-jsp/adminCompany.jsp`
**Purpose:** Sub-company (location) listing view. Displays companies associated with a dealer account. Backed by `/dealercompanies.do` (`DealerCompaniesAction`). Layout: `dealerCompaniesDefinition` (extends `adminDefinition` — authenticated layout).

**Key scriptlets:** None.

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<logic:iterate name="subCompanyLst" id="companyRecord" type="com.bean.CompanyBean">` | Line 44 | Iterates request attribute |
| `<bean:write property="name" name="companyRecord"/>` | Line 46 | Company name — user-supplied string |
| `<bean:write property="address" name="companyRecord"/>` | Line 47 | Address — user-supplied string |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `dealercompanies.do` | POST | Plain `<form>` (not `<html:form>`), no hidden action field visible |
| `dealercompanies.do?action=add` (lightbox link) | GET | Add company anchor |

---

### 1.5 `html-jsp/adminDealer.jsp`

**File:** `src/main/webapp/html-jsp/adminDealer.jsp`
**Purpose:** Dealer company conversion view. Displays existing dealer companies and allows converting a regular company to a dealer account. Backed by `/dealerconvert.do` (`AdminDealerAction`). Layout: `adminDealerDefinition` (extends `adminDefinition` — authenticated layout).

**Key scriptlets:** None.

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<html:optionsCollection name="arrCompanies" value="id" label="name"/>` | Line 24 | Companies dropdown, request-scoped |
| `<logic:iterate name="arrDealers" id="DealerRecord" type="com.bean.CompanyBean">` | Line 51 | Iterates dealers |
| `<bean:write property="name" name="DealerRecord"/>` | Line 53 | Company name — user-supplied string |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `/dealerconvert.do` | POST | Note absolute path with leading slash |

---

### 1.6 `html-jsp/adminGPS.jsp`

**File:** `src/main/webapp/html-jsp/adminGPS.jsp`
**Purpose:** GPS map report view. Displays a multi-select list of units and an embedded map canvas (`#map_canvas`). Loads GPS data via AJAX to `getAjaxGPS.do`. Backed by `/gpsreport.do` (`GPSReportAction`). Layout: `gpsReportDefinition` extends `adminDefinition` (authenticated).

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 3 | `String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");` — session attribute fetched and immediately chained without null guard. |
| 4 | `String custCd = "0";` — hardcoded to "0", never set from session or DB. |

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<logic:iterate name="arrAdminUnit" id="unitRecord" type="com.bean.UnitBean">` | Lines 25–29 | Iterates units |
| `<bean:write property="id" name="unitRecord"/>` | Line 26 | Unit ID in `<option value="">` |
| `<bean:write property="name" name="unitRecord"/>` | Line 27 | Unit name as option text |
| `<%=custCd %>` | Line 44 | Hidden input value — always "0" |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `adminunit.do` | POST | Main form (unused in actual GPS flow — actual GPS data loaded via AJAX) |

**JavaScript (inline, lines 50–103):**
- `var defaultLoc = "-24.2761156,133.5912902"; //UK- 55.378051, -3.435973` — commented-out Australia coordinates alongside live UK coordinates (lines 52–58).
- `fetchUnit()` (lines 70–103): constructs AJAX URL `../master/get_cust_vehicle.jsp?cust_cd=...` with `#cust` DOM value — references a JSP outside the admin module, uses `ActiveXObject` (IE-only) XML parsing pattern.
- `fnRefresh()` (lines 62–68): calls `initialize()` and `application.getGotToZonesControl()` — undefined functions in this file.

---

### 1.7 `html-jsp/adminJob.jsp`

**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Purpose:** Job management modal. Displays a list of jobs for a given equipment unit, allowing add/edit. Loaded as a lightbox popup via `/adminunit.do` (`AdminUnitAction`). Layout: `adminJobDefinition` extends `loginDefinition` (popup/header-only layout).

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 3–4 | `String action = request.getParameter("action") == null ? "" : request.getParameter("action");` |
| 4 | `String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");` |

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<%=id %>` | Lines 9, 72 | Raw `equipId` request parameter into `<input>` value attributes |
| `<%=action %>` | Line 10 | Raw `action` request parameter into `<input>` value attribute |
| `<bean:write name="jobs" property="jobTitle"/>` | Line 38 | Job title in `<input value='...'>` (single-quote delimited) |
| `<bean:write name="jobs" property="description"/>` | Line 42 | Job description inside `<textarea>` |
| `<bean:write name="jobs" property="driverName"/>` | Line 45 | Driver name in `<label>` |
| `<bean:write name="jobs" property="unitId"/>` | Line 68 | Unit ID in `href` attribute |
| `<bean:write name="jobs" property="jobNo"/>` | Line 68 | Job number in `href` attribute |
| `<bean:write name="jobs" property="id"/>` | Line 73 | Job ID in hidden input |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `adminunit.do` | POST | Per-job inline form with class `ajax_mode_c edit_job`, submitted via `saveJobs()` AJAX batch |

---

### 1.8 `html-jsp/adminOperator.jsp`

**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Purpose:** Driver (operator) management list view. Allows searching, adding, editing, and deleting drivers. Backed by `/admindriver.do` (`AdminOperatorAction`). Layout: `adminOperatorDefinition` extends `adminDefinition` (authenticated).

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 4 | `String searchDriver = request.getParameter("searchDriver") == null ? "" : request.getParameter("searchDriver");` |

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<%=searchDriver %>` | Line 25 | Raw request parameter into `<input value="...">` (double-quote delimited) |
| `<logic:iterate name="arrAdminDriver" id="driverRecord" type="com.bean.DriverBean">` | Line 59 | Iterates drivers |
| `<bean:write property="id" name="driverRecord"/>` | Lines 63, 66, 72 | Driver ID in `href`, CSS class name, and data attribute |
| `<bean:write property="first_name" name="driverRecord"/>` | Line 78 | Driver first name |
| `<bean:write property="last_name" name="driverRecord"/>` | Line 79 | Driver last name |
| `<bean:write property="email_addr" name="driverRecord"/>` | Line 81 | Email address |
| `<bean:write property="joindt" name="driverRecord"/>` | Line 82 | Join date |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `admindriver.do` | GET | Search form; search term reflected in `value` attribute |

---

### 1.9 `html-jsp/adminRegister.jsp`

**File:** `src/main/webapp/html-jsp/adminRegister.jsp`
**Purpose:** New company/user registration form. Collects company name, timezone, address, contact name, phone, email, password, and confirm password. Backed by `/adminRegister.do` (`AdminRegisterAction`). Layout: `adminRegiserDefinition` extends `loginDefinition` (unauthenticated header-only layout — accessible without a valid session).

**Key scriptlets:** None.

**Key EL expressions / Struts tags:**

| Tag / Expression | Location | Notes |
|-----------------|----------|-------|
| `<html:form action="adminRegister.do" ...>` | Line 12 | Main registration form |
| `<html:text property="name" .../>` | Lines 30–35 | Company name field |
| `<select name="timezone" ...>` | Lines 38–48 | Timezone dropdown (plain `<select>`, not `<html:select>`) |
| `<logic:iterate name="arrTimezone" id="timezone" type="com.bean.TimezoneBean">` | Lines 41–47 | Timezone options |
| `<bean:write name="timezone" property="id"/>` | Line 43 | Timezone ID in `<option value='...' >` — raw single-quoted |
| `<bean:write name="timezone" property="name"/>` | Line 44 | Timezone display name |
| `<html:textarea property="address" .../>` | Lines 52–57 | Address field |
| `<input type="password" name="pin" ...>` | Lines 102–109 | Password field (plain `<input>`, not `<html:password>`) |
| `<input type="password" name="cpassword" ...>` | Lines 111–118 | Confirm password (plain `<input>`) |
| `<html:hidden property="accountAction" value="register"/>` | Line 139 | Controls action branch in server-side handler |

**Forms:**
| Form action | Method | Notes |
|-------------|--------|-------|
| `adminRegister.do` | POST | Registration form; `accountAction=register` triggers unauthenticated account creation path |

**JavaScript (lines 150–187):** Client-only validation (`fnsubmitAccount()`) checks company name, email, password, confirm password match, and timezone. `fnGoBackHome()` redirects to `index.jsp` via `location.replace`.

---

## 2. Test Coverage Search

**Test directory:** `src/test/java/`
**Files present:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep results for all audited file names, action paths, and backing action class names:**

| Search term | Matches in test directory |
|-------------|--------------------------|
| `unit.gps` | 0 |
| `adminChecklist` | 0 |
| `adminChecklistEdit` | 0 |
| `adminCompany` | 0 |
| `adminDealer` | 0 |
| `adminGPS` / `GPSReport` / `GetAjax` | 0 |
| `adminJob` | 0 |
| `adminOperator` | 0 |
| `adminRegister` | 0 |
| `fleetcheckconf` / `fleetcheckedit` | 0 |
| `dealercompanies` / `dealerconvert` | 0 |
| `adminunit` / `admindriver` | 0 |
| `AdminRegisterAction` | 0 |
| `AdminFleetcheckAction` / `AdminFleetcheckEditAction` | 0 |
| `AdminDealerAction` / `DealerCompaniesAction` | 0 |
| `AdminUnitAction` / `AdminOperatorAction` | 0 |
| `GPSReportAction` / `GetAjaxAction` | 0 |
| `GPSUnitBean` | 0 |

**Conclusion:** Zero test coverage exists for any of the nine audited JSP files or their associated action classes and backing DAOs.

---

## 3. Findings

---

### B01-1
**Severity:** HIGH
**File:** `html-jsp/adminOperator.jsp`, line 25
**Title:** Reflected XSS via unescaped `searchDriver` request parameter in HTML attribute

**Evidence:**
```jsp
<%
    String searchDriver = request.getParameter("searchDriver") == null ? "" : request.getParameter("searchDriver");
%>
...
<input type="text" name="searchDriver" class="form-control input-lg" placeholder="Search"
       value="<%=searchDriver %>"/>
```
`request.getParameter("searchDriver")` is assigned to a Java String and then emitted directly into an HTML attribute value using `<%=...%>` (JSP expression syntax, equivalent to `out.print()`). JSP expression output is **not** HTML-encoded. The attribute is double-quote delimited (`value="..."`). An attacker can submit `searchDriver="onmouseover=alert(1)` to break out of the attribute and inject arbitrary HTML event handlers, or submit `searchDriver="><script>...` to inject a script element. This is a reflected XSS because the form uses `method="get"`, making the payload fully URL-encodable and shareable as a crafted link.

**Untestable pattern:** The JSP scriptlet performs the parameter read and output directly — this logic is entirely in the view layer and cannot be unit-tested without a live servlet container.

---

### B01-2
**Severity:** HIGH
**File:** `html-jsp/adminJob.jsp`, lines 9–10 and 72
**Title:** Reflected XSS via unescaped `action` and `equipId` request parameters in hidden input values

**Evidence:**
```jsp
<%
    String action = request.getParameter("action") ==  null ? "" :  request.getParameter("action");
    String id = request.getParameter("equipId") ==  null ? "" :  request.getParameter("equipId");
%>
<input type="hidden" name="equip_id" value="<%=id %>" />
<input type="hidden" name="action" value="<%=action %>" />
...
<input type="hidden" name="equipId" value="<%=id %>" />
```
Both `action` and `equipId` are taken from the raw request and emitted via `<%=...%>` into double-quote-delimited HTML attribute values without encoding. A request such as `equipId="><script>alert(1)</script>` will break out of the attribute and inject arbitrary JavaScript. The `action` parameter is similarly exposed. Because these are inside a lightbox popup loaded by AJAX, an attacker who can construct a URL that is loaded in the popup context can achieve XSS.

**Untestable pattern:** Scriptlet-level parameter reading and raw output in the view — no unit-testable layer exists.

---

### B01-3
**Severity:** HIGH
**File:** `html-jsp/adminGPS.jsp`, line 3
**Title:** Null-pointer dereference on missing `sessDateFormat` session attribute — server-side exception disclosure

**Evidence:**
```jsp
<%
    String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
%>
```
`session.getAttribute("sessDateFormat")` returns `null` if the attribute has not been set (e.g., expired session, direct navigation without prior login flow). The result is immediately cast to `String` and `.replaceAll()` is called on it without a null guard. This produces a `NullPointerException` at page-render time. Depending on the error handler, this may expose a stack trace. The same pattern exists in the backing `GetAjaxAction` at line 47:
```java
String dateFormat = ((String) request.getSession().getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```
Both the JSP and its backing action share this defect. The JSP-level scriptlet is untestable without a servlet container.

---

### B01-4
**Severity:** HIGH
**File:** `gps/unit.gps.jsp`, lines 11–14
**Title:** NullPointerException on `arrGPSData` attribute when action is not `last_gps`

**Evidence:**
```jsp
List<String> unitList = (List<String>)request.getAttribute("arrGPSData");
String resp = "";
resp = resp+"{\"count\":"+unitList.size()+",\"units\":[";
```
`GetAjaxAction` only sets `arrGPSData` when the `action` request parameter equals `"last_gps"` (line 44 of `GetAjaxAction`):
```java
} else if (action.equals("last_gps")) {
    ...
    request.setAttribute("arrGPSData", GPSDao.getUnitGPSData(...));
}
```
For any other action value (including an absent parameter, since the action defaults to `""`), `arrGPSData` is never set and remains `null`. Line 14 of `unit.gps.jsp` then dereferences the null list (`unitList.size()`), producing an unguarded NPE. The `errorPage` directive redirects to `ExceptionHandler.jsp`, which may itself expose error details.

---

### B01-5
**Severity:** HIGH
**File:** `html-jsp/adminRegister.jsp` / `com/action/AdminRegisterAction.java`
**Title:** Unauthenticated new-company account creation — registration endpoint reachable without login

**Evidence:**

`tiles-defs.xml`:
```xml
<definition name="adminRegiserDefinition" extends="loginDefinition">
    <put name="header" value="/includes/header_register.inc.jsp"/>
    <put name="content" value="/html-jsp/adminRegister.jsp"/>
</definition>
```
`loginDefinition` uses `tilesTemplateHeader.jsp`, which contains no session or authentication check:
```jsp
<tiles:insert attribute="header"/>
<tiles:insert attribute="content"/>
```
`web.xml` defines only a `CharsetEncodingFilter` — no security constraint, no login-config block.

`AdminRegisterAction.java` lines 76 and 166–170:
```java
if (accountAction.equalsIgnoreCase("register") || accountAction.equalsIgnoreCase("add")) {
    ...
    if (accountAction.equalsIgnoreCase("register")) {
        compId = compDao.saveCompInfo(companybean, RuntimeConf.ROLE_COMP);
```
When `accountAction=register`, the action calls `compDao.saveCompInfo()` to create a new company row. Session variables (`sessCompId`, `sessUserId`) are initialised to empty string / 0 when the session attributes are absent — they are not checked before the register branch is taken. This means any unauthenticated visitor can POST to `/adminRegister.do` with `accountAction=register` and create a new company and admin user account in the system.

The JSP `adminRegister.jsp` line 139 hardcodes the hidden field:
```jsp
<html:hidden property="accountAction" value="register" />
```

---

### B01-6
**Severity:** HIGH
**File:** `gps/unit.gps.jsp` (output) / `com/dao/GPSDao.java` (data source)
**Title:** Insecure Direct Object Reference (IDOR) — GPS unit data returned without tenant isolation

**Evidence:**

`GetAjaxAction.java`:
```java
String compId = request.getParameter("compId")==null?"0":request.getParameter("compId");
String[] unit = request.getParameterValues("unit");
request.setAttribute("arrGPSData", GPSDao.getUnitGPSData(compId, unit, dateTimeFormat, timezone));
```
`GPSDao.QUERY_UNIT_GPS`:
```java
private static final String QUERY_UNIT_GPS =
    "select u.name,g.longitude,g.latitude,g.gps_time,m.name as manufacturer, t.name as type, f.name as power "
    + "from gps as g inner join unit as u on u.id=g.unit_id"
    + " ... where g.unit_id=? order by g.gps_time desc limit 1";
```
`compId` is taken from the HTTP request parameter, not from the session. More critically, the SQL query has **no `comp_id` filter** — it retrieves GPS records for any `unit_id` without verifying that the unit belongs to the requesting user's company. An authenticated user from company A can request GPS data for unit IDs belonging to company B by submitting arbitrary `unit[]` values. The `compId` parameter is entirely unused in the parameterised query path (it is passed to the method but not applied to `QUERY_UNIT_GPS`).

---

### B01-7
**Severity:** MEDIUM
**File:** `html-jsp/adminChecklistEdit.jsp`, line 64
**Title:** `comp_id` passed as client-side hidden field — tenant identifier forgeable

**Evidence:**
```jsp
<html:hidden property="comp_id" name="question" />
```
The company ID that scopes the checklist question is round-tripped through a hidden form input. A browser-side modification of this field before form submission (via developer tools or a proxy) could associate the question update with a different company ID. Server-side trust of this value in `AdminFleetcheckEditAction` would allow cross-tenant data manipulation.

---

### B01-8
**Severity:** MEDIUM
**File:** `html-jsp/adminChecklist.jsp`, lines 123, 130, 155
**Title:** `bean:write` of String `id` field used inside `onclick` JavaScript call — potential stored XSS if ID is not numeric

**Evidence:**
```jsp
onclick="showQuestion(<bean:write property="id" name="QuestionRecord"/>)"
onclick="hideQuestion(<bean:write property="id" name="QuestionRecord"/>)"
```
`QuestionBean.id` is declared as `String` (not a primitive `int`). Although `bean:write` uses `filter=true` by default (HTML-encoding `<`, `>`, `&`, `"`), HTML-encoding does not neutralise JavaScript context. If a non-numeric value or a value containing single quotes or parentheses were stored in the `id` column (e.g., via direct DB manipulation or a SQL injection attack elsewhere), it would break out of the JavaScript argument context and execute arbitrary code in the browser. The risk is mitigated if the DB column is typed as a numeric primary key, but the Java model does not enforce this.

---

### B01-9
**Severity:** MEDIUM
**File:** `html-jsp/adminGPS.jsp`, lines 52–58
**Title:** Dead commented-out geographic coordinates reveal previous deployment location; live coordinates hardcoded

**Evidence:**
```javascript
var defaultLoc = "-24.2761156,133.5912902"; //UK- 55.378051, -3.435973
// var defaultLat = "-24.2761156"; //AU
// var defaultLong = "133.5912902";
var defaultLat = "55.378051"; //UK- 55.378051, -3.435973
var defaultLong = "-3.435973"
```
Commented-out Australian coordinates (`-24.2761156, 133.5912902`) remain visible in the shipped source. The active UK coordinates are hardcoded literals. These coordinates are delivered to every browser that loads this page, regardless of user role, and expose operational deployment geography. Hardcoded coordinates also mean the map will centre incorrectly for deployments in other regions without a source code change.

---

### B01-10
**Severity:** MEDIUM
**File:** `html-jsp/adminGPS.jsp`, lines 70–103
**Title:** Dead `fetchUnit()` function references unauthenticated external JSP and contains IE-only `ActiveXObject` code

**Evidence:**
```javascript
function fetchUnit(str) {
    var cust_cd = $('#cust').val();
    ...
    $.ajax({
        url:'../master/get_cust_vehicle.jsp?cust_cd='+cust_cd+"&loc_cd="+loc_cd+"&dept_cd="+str,
        ...
        success: function(xmlData) {
            if ( typeof xmlData == 'string') {
                xmllist = new ActiveXObject( 'Microsoft.XMLDOM');
```
`fetchUnit()` is defined but never called in this file. It references `../master/get_cust_vehicle.jsp`, a path pointing to a JSP outside the admin module that may not exist in the current codebase (the file was not located in the repository). The `ActiveXObject` usage is IE-only and broken on all modern browsers. The function reads `$('#cust').val()` — a DOM element that is not present in this file, so `cust_cd` will always be `undefined`. The dead code adds confusion and may represent a legacy integration path that was never removed.

---

### B01-11
**Severity:** MEDIUM
**File:** `html-jsp/adminRegister.jsp`, lines 102–118
**Title:** Password fields implemented as plain `<input>` elements — not using Struts `<html:password>` tag; confirm-password field never cleared on redisplay

**Evidence:**
```html
<input class="form-control" placeholder="Password" name="pin" type="password" value="" autocomplete="off" tabindex="5">
<input class="form-control" placeholder="Confirm Password" name="cpassword" type="password" value="" autocomplete="off" tabindex="6">
```
The password and confirm-password fields use raw HTML `<input>` elements rather than `<html:password>`. The `<html:password>` tag intentionally suppresses pre-population on redisplay (validation failure returns to form). With raw `<input>` the Struts ActionForm's `pin` property value could be re-rendered in the `value` attribute on validation failure, although the current markup has `value=""` hardcoded. The `cpassword` field is not a Struts-bound property and exists only for client-side JS validation — password confirmation is not enforced server-side.

---

### B01-12
**Severity:** MEDIUM
**File:** All nine audited JSPs
**Title:** No CSRF protection on any state-mutating form

**Evidence:**
Grep across the entire `src/main/webapp` tree finds zero occurrences of `csrf`, `CSRF`, `syncToken`, or `synchronizer`. `web.xml` contains no CSRF filter. None of the audited forms include a synchronizer token. Affected state-mutating endpoints include:
- `fleetcheckconf.do` (adminChecklist — hide/show/add question)
- `fleetcheckedit.do` (adminChecklistEdit — edit question)
- `dealerconvert.do` (adminDealer — convert company to dealer)
- `adminRegister.do` (adminRegister — create account)
- `admindriver.do` (adminOperator — delete driver)
- `adminunit.do` (adminJob — save jobs)

An attacker can craft a page that silently submits these forms from any origin when a logged-in user visits it.

---

### B01-13
**Severity:** MEDIUM
**File:** `html-jsp/adminJob.jsp`, line 38
**Title:** `bean:write` in single-quote-delimited HTML attribute — HTML encoding does not neutralise single-quote breakout

**Evidence:**
```jsp
<input name="title" ... value='<bean:write name="jobs" property="jobTitle" />' class="form-control fader" />
```
The attribute delimiter is a single quote (`value='...'`). Struts `bean:write` with `filter=true` (default) encodes `<`, `>`, `&`, and `"` — but **not single quotes**. If `jobTitle` contains a single quote, the attribute value is broken and subsequent content is parsed as additional HTML attributes or tag content. If a user-controlled job title contains `' onmouseover='alert(1)`, the browser will execute the event handler. Job titles are entered by authenticated users, making this a stored XSS vector within the authenticated session scope.

---

### B01-14
**Severity:** LOW
**File:** `html-jsp/adminDealer.jsp`, line 16
**Title:** Absolute path used in form action — potential routing issue in non-root deployments

**Evidence:**
```jsp
<html:form method="post" action="/dealerconvert.do" styleId="adminDealerForm">
```
The action path begins with `/`, making it an absolute path from the web server root. All other forms in the codebase use relative paths (e.g., `fleetcheckconf.do`). If the application is deployed under a context path (e.g., `/forkliftiq`), this form will POST to `/dealerconvert.do` (root) instead of `/forkliftiq/dealerconvert.do`, resulting in a 404 or routing to a different application entirely.

---

### B01-15
**Severity:** LOW
**File:** `html-jsp/adminChecklistEdit.jsp`, line 66
**Title:** Hardcoded hidden action field `value="search"` in edit form

**Evidence:**
```html
<input type="hidden" name="action" value="search"/>
```
This hidden field sets `action=search` unconditionally in an edit/submit modal. The client-side `submit()` JS function (line 94) posts directly to `fleetcheckedit.do` via jQuery AJAX and does not include this hidden field in its payload. The hardcoded field is therefore not submitted and serves no function, but it creates confusion about the intended action and could mislead future maintainers into believing the form submits a search action.

---

### B01-16
**Severity:** LOW
**File:** `gps/unit.gps.jsp`, line 1
**Title:** Imported `GPSUnitBean` is never used in the JSP

**Evidence:**
```jsp
<%@page import="com.bean.GPSUnitBean"%>
```
`GPSUnitBean` is imported at line 1 but is never referenced in the scriptlet. The JSP works with `List<String>` (pre-serialised JSON strings) not `GPSUnitBean` objects. The unused import is a code-smell and may confuse developers into thinking the JSP processes `GPSUnitBean` objects directly.

---

### B01-17
**Severity:** INFO
**File:** `html-jsp/adminGPS.jsp`, line 4
**Title:** Scriptlet business logic in view — `custCd` initialised to hardcoded "0" rather than session value

**Evidence:**
```jsp
<%
    String dateFormat = ((String) session.getAttribute("sessDateFormat"))...;
    String custCd = "0";
%>
...
<input type="hidden" name="cust_cd" id="cust_cd" value="<%=custCd %>" />
```
`custCd` is hardcoded to `"0"` in the scriptlet and served in a hidden input. The JavaScript variable `custCd` is separately initialised to `""` in the inline script. The determination of the actual customer code value belongs in the backing action (`GPSReportAction`), not as a scriptlet in the view. This pattern — scriptlets setting view-layer state that should come from the model — is untestable without a servlet container and conflates view and controller responsibilities.

---

### B01-18
**Severity:** INFO
**File:** All nine audited JSPs
**Title:** Zero unit-test coverage — entire view layer is untestable without integration test infrastructure

**Evidence:**
The test directory (`src/test/java/`) contains exactly four test classes, none of which reference any of the nine audited JSP files, their backing action classes (`GetAjaxAction`, `AdminFleetcheckAction`, `AdminFleetcheckEditAction`, `AdminDealerAction`, `DealerCompaniesAction`, `GPSReportAction`, `AdminUnitAction`, `AdminOperatorAction`, `AdminRegisterAction`), or the DAOs invoked by those actions.

JSP files containing scriptlets (`<% %>`) and expression elements (`<%= %>`) embed business logic directly in the view layer where it cannot be exercised by JUnit tests. Specific untestable patterns identified:
- `unit.gps.jsp`: JSON serialisation loop in scriptlet (lines 9–31)
- `adminGPS.jsp`: Session attribute read and date format transformation (line 3)
- `adminOperator.jsp`: Search parameter reflection (line 4, 25)
- `adminJob.jsp`: Request parameter extraction (lines 3–4, 9–10, 72)

Recommendation (for tracking only — no fix in scope for this report): Extract scriptlet logic into action classes or tag libraries; cover action classes with JUnit + MockHttpServletRequest.

---

## 4. Summary Table

| ID | Severity | File | Title |
|----|----------|------|-------|
| B01-1 | HIGH | adminOperator.jsp:25 | Reflected XSS via unescaped `searchDriver` parameter |
| B01-2 | HIGH | adminJob.jsp:9–10,72 | Reflected XSS via unescaped `action` and `equipId` parameters |
| B01-3 | HIGH | adminGPS.jsp:3 | NPE on null `sessDateFormat` session attribute |
| B01-4 | HIGH | unit.gps.jsp:11–14 | NPE on null `arrGPSData` when action != `last_gps` |
| B01-5 | HIGH | adminRegister.jsp | Unauthenticated new-company account creation |
| B01-6 | HIGH | unit.gps.jsp / GetAjaxAction | IDOR — GPS data returned without tenant isolation |
| B01-7 | MEDIUM | adminChecklistEdit.jsp:64 | `comp_id` as forgeable hidden field |
| B01-8 | MEDIUM | adminChecklist.jsp:123,130,155 | `bean:write String id` in `onclick` — JS-context XSS risk |
| B01-9 | MEDIUM | adminGPS.jsp:52–58 | Hardcoded geographic coordinates expose deployment geography |
| B01-10 | MEDIUM | adminGPS.jsp:70–103 | Dead function referencing missing JSP with IE-only ActiveXObject |
| B01-11 | MEDIUM | adminRegister.jsp:102–118 | Plain `<input>` password fields; server-side confirm-password not validated |
| B01-12 | MEDIUM | All 9 JSPs | No CSRF protection on any state-mutating form |
| B01-13 | MEDIUM | adminJob.jsp:38 | `bean:write` in single-quote attribute — stored XSS via job title |
| B01-14 | LOW | adminDealer.jsp:16 | Absolute action path breaks context-path deployments |
| B01-15 | LOW | adminChecklistEdit.jsp:66 | Hardcoded `action=search` hidden field unused and misleading |
| B01-16 | LOW | unit.gps.jsp:1 | Unused `GPSUnitBean` import |
| B01-17 | INFO | adminGPS.jsp:4 | Scriptlet business logic — `custCd` hardcoded in view |
| B01-18 | INFO | All 9 JSPs | Zero unit-test coverage across entire view layer |
