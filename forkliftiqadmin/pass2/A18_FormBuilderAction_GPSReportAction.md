# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A18
**Files audited:**
- `src/main/java/com/action/FormBuilderAction.java`
- `src/main/java/com/action/GPSReportAction.java`

---

## 1. Reading-Evidence Blocks

### 1.1 FormBuilderAction

**File:** `src/main/java/com/action/FormBuilderAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

**Fields / Constants**

| Field | Type | Line | Notes |
|-------|------|------|-------|
| `log` | `static Logger` | 39 | `InfoLogger.getLogger("com.action.FormBuilderAction")` |

**Methods**

| Method | Signature | Lines | Notes |
|--------|-----------|-------|-------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 41–115 | Sole public entry point; contains all action logic |

**Imports / Dependencies used inside `execute`**

| Dependency | Usage |
|------------|-------|
| `HttpSession` | obtained via `request.getSession(false)` (line 44) |
| `ArrayList<DriverBean>` | cast from session attribute `"arrDriver"` (line 46) |
| `QuestionDAO` | instantiated inline (line 53); calls `getQuestionById(qid)` |
| `CompanyDAO` | singleton `getInstance()` (line 74); calls `getEntityByQuestion(qid, type)` |
| `FormBuilderDAO` | instantiated inline (line 88); calls `getLib(qid, type)` |
| `Util.sendMail` | called only inside `action == "save"` branch (line 80) |
| `BeanComparator` | used to sort form elements (line 97) |
| `Collections.sort` | sorts `arrFormEle` by position (line 98) |
| `DateUtil.GetDateNow` | embedded in HTML string (line 61) |
| `RuntimeConf.EMAIL_DIGANOSTICS_TITLE` / `RuntimeConf.emailFrom` | email configuration (line 80) |
| `ActionMessages` / `ActionMessage` | success message `"msg.form"` (lines 82–85) |
| `ActionErrors` / `ActionMessage` | error message for empty library (lines 103–106) |

---

### 1.2 GPSReportAction

**File:** `src/main/java/com/action/GPSReportAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

**Fields / Constants**

| Field | Type | Line | Notes |
|-------|------|------|-------|
| `reportService` | `ReportService` | 19 | `ReportService.getInstance()` — instance-level singleton reference |
| `manufactureDAO` | `ManufactureDAO` | 20 | `ManufactureDAO.getInstance()` — instance-level singleton reference |
| `unitDAO` | `UnitDAO` | 21 | `UnitDAO.getInstance()` — instance-level singleton reference |

**Methods**

| Method | Signature | Lines | Notes |
|--------|-----------|-------|-------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 24–44 | Sole public entry point; `@Override` |

**Commented-out code blocks (lines 35–36, 39, 41–42)**

| Line range | Commented content |
|------------|-------------------|
| 35–36 | `searchForm.setManufacturers(...)` / `searchForm.setUnitTypes(...)` |
| 39 | `ImpactReportBean impactReport = reportService.getImpactReport(...)` |
| 41–42 | `request.setAttribute("impactReport", impactReport)` |

**Imports / Dependencies used inside `execute`**

| Dependency | Usage |
|------------|-------|
| `HttpSession` | `request.getSession(false)` (line 25) |
| `sessCompId` | String session attribute cast (line 26) |
| `sessDateFormat` / `sessDateTimeFormat` / `sessTimezone` | read from session (lines 29–31); assigned but not used |
| `Long.valueOf(sessCompId)` | `compId` — assigned but not used in active code (line 32) |
| `GPSReportSearchForm` | cast from `form`; cast succeeds silently; `getGPSReportFilter()` never called in active code (line 34) |
| `UnitDAO.getAllUnitsByCompanyId` | static call with `Integer.parseInt(sessCompId)` (line 38) |

---

## 2. Test-Directory Coverage Confirmation

**Test files present in `src/test/java/` (all four):**

| Test File | Package | Classes Tested |
|-----------|---------|----------------|
| `UnitCalibrationImpactFilterTest.java` | `com.calibration` | `UnitCalibrationImpactFilter` |
| `UnitCalibrationTest.java` | `com.calibration` | `UnitCalibration` |
| `UnitCalibratorTest.java` | `com.calibration` | `UnitCalibrator` |
| `ImpactUtilTest.java` | `com.util` | `ImpactUtil` |

**Grep results for `FormBuilderAction` across test directory:** No matches found.
**Grep results for `GPSReportAction` across test directory:** No matches found.
**Grep results for `FormBuilderAction|GPSReportAction` (combined):** No matches found.

**Conclusion:** Zero test coverage — direct or indirect — exists for either action class.

---

## 3. Coverage Gaps and Findings

---

### FormBuilderAction — Findings

---

**A18-1 | Severity: CRITICAL | No test coverage for FormBuilderAction.execute — entire class is untested**

`FormBuilderAction.execute` is the sole method of the class. No test exercises it under any condition. All logic paths — normal flow, save branch, empty-library branch, and all error conditions — are completely uncovered.

---

**A18-2 | Severity: CRITICAL | Null session causes NullPointerException — no guard on getSession(false)**

Line 44: `HttpSession session = request.getSession(false);`
Line 46: `(ArrayList<DriverBean>) session.getAttribute("arrDriver");`

`getSession(false)` returns `null` when no session exists. The next line dereferences `session` without a null check, producing an unhandled `NullPointerException`. There is no test for an unauthenticated (session-less) request, and the method's `throws Exception` declaration means this propagates to the Struts error handler without a meaningful user-facing error.

---

**A18-3 | Severity: CRITICAL | NullPointerException when session attribute "arrDriver" is absent or empty**

Line 46–47: The session attribute `"arrDriver"` is cast to `ArrayList<DriverBean>` and immediately accessed at index 0 with no null check and no size check. If the attribute is missing (`null`) or the list is empty, the code throws either a `NullPointerException` or an `IndexOutOfBoundsException`. No test covers either case.

---

**A18-4 | Severity: CRITICAL | NullPointerException / IndexOutOfBoundsException when QuestionDAO returns empty or null result**

Line 54–55:
```java
ArrayList<QuestionBean> arrQues = questionDAO.getQuestionById(qid);
String qName = (arrQues.get(0)).getContent();
```
If `qid` does not match any question, `arrQues` is empty (or null depending on DAO implementation). `arrQues.get(0)` throws `IndexOutOfBoundsException`, and a null list throws `NullPointerException`. Neither error path has a null/empty guard, and no test covers an invalid or missing `qid`.

---

**A18-5 | Severity: CRITICAL | SQL Injection via unsanitised `qid` and `type` parameters in FormBuilderDAO.getLib**

Lines 49–51 accept `qid` and `type` directly from `request.getParameter(...)`. These raw strings are passed into `FormBuilderDAO.getLib(qid, type)`, which constructs the query using string concatenation (DAO line 37):
```java
String sql = "select id, form_object from form_library where question_id =" + questionId + " and type = '" + type + "'";
```
No input validation, type assertion, or parameterisation is applied in the action before the DAO call. No test validates that a malformed or adversarial `qid`/`type` value is rejected.

---

**A18-6 | Severity: HIGH | NullPointerException / IndexOutOfBoundsException when CompanyDAO returns empty entity list (save branch)**

Lines 75–77:
```java
ArrayList<EntityBean> arrEntity = companyDAO.getEntityByQuestion(qid, type);
EntityBean EntityBean = arrEntity.get(0);
String name = EntityBean.getName();
```
If no entity is associated with the given question/type, `arrEntity` is empty. `arrEntity.get(0)` throws `IndexOutOfBoundsException` inside the `save` branch. No guard exists and no test covers this path.

---

**A18-7 | Severity: HIGH | "save" branch is completely untested — email dispatch path has zero coverage**

Lines 57–86 are guarded by `action.equalsIgnoreCase("save")`. No test exercises this branch at all. The `Util.sendMail` call at line 80, the HTML assembly loop over request parameters (lines 63–72), and the success `ActionMessages` construction (lines 82–85) are all uncovered. A failure in `sendMail` (SMTP unavailable, invalid recipient) would propagate as an unhandled exception.

---

**A18-8 | Severity: HIGH | Reflected XSS: unsanitised request parameters written into HTML email body**

Lines 63–71 iterate `request.getParameterNames()` and embed raw parameter values directly into an HTML string:
```java
html += "<tr><td>" + ParameterNames + "</td><td>" + ParameterValues + "</td></tr>";
```
No HTML encoding is applied. Malicious parameter values containing `<script>` or other HTML can be injected into the email body. No test validates sanitisation behaviour.

---

**A18-9 | Severity: HIGH | Empty-library error branch tested for wrong condition — "action" variable used in error message instead of meaningful context**

Lines 103–108: When `arrLib` is null or empty, the error message is:
```java
new ActionMessage("errors.detail", "There is no " + action + " against this question.")
```
When `action` is an empty string (the default on line 49 when the parameter is absent), the message reads "There is no  against this question." — both misleading and untested for correctness. No test confirms what happens to the error message under valid or invalid `action` values in the non-save path.

---

**A18-10 | Severity: MEDIUM | `qid` defaults to "0" — no test for the zero/invalid-qid path**

Line 50: `String qid = request.getParameter("qid")==null?"0":request.getParameter("qid");`

When `qid` is absent, the value "0" is used. This propagates to `QuestionDAO.getQuestionById("0")` and `FormBuilderDAO.getLib("0", type)`. No test verifies the system's behaviour when `qid` is 0, negative, non-numeric, or null, including what the DAO returns and whether the downstream `.get(0)` calls crash.

---

**A18-11 | Severity: MEDIUM | Non-numeric `qid` causes NumberFormatException in DAO layer**

`FormBuilderDAO.getLib` concatenates `questionId` as a string directly into SQL (DAO line 37). A non-numeric `qid` (e.g. `"abc"`) would produce invalid SQL syntax. In `CompanyDAO.getEntityByQuestion` and `QuestionDAO.getQuestionById` the same unvalidated string is likely used. No test confirms that non-numeric `qid` values are rejected or handled gracefully.

---

**A18-12 | Severity: MEDIUM | `type` parameter accepted as empty string — untested behaviour when type is blank**

Line 51: `String type = request.getParameter("type")==null?"":request.getParameter("type");`

An empty `type` string propagates into `FormBuilderDAO.getLib` and `CompanyDAO.getEntityByQuestion`. The SQL query built in `getLib` embeds `type` in a quoted string literal, meaning blank type silently queries with `type = ''`. No test verifies what happens when `type` is empty, null, or an unrecognised value.

---

**A18-13 | Severity: MEDIUM | BeanComparator sort failure on null `getPosition` is untested**

Lines 97–98:
```java
BeanComparator bc = new BeanComparator(FormElementBean.class, "getPosition");
Collections.sort(arrFormEle, bc);
```
If any `FormElementBean` returns a null position, `BeanComparator` may throw a `NullPointerException` or `ClassCastException` during comparison. No test exercises sorting with null or out-of-order position values.

---

**A18-14 | Severity: LOW | Raw type warning on `Enumeration` suppressed implicitly — no test for empty parameter set**

Line 63: `for(Enumeration e = request.getParameterNames(); ...)` uses a raw `Enumeration`. No test confirms behaviour when the request has zero parameters with an underscore (i.e. the loop runs but produces no HTML rows).

---

**A18-15 | Severity: LOW | `@SuppressWarnings("unchecked")` on session cast is broad — no test for ClassCastException**

Line 45–46: The session attribute `"arrDriver"` is cast to `ArrayList<DriverBean>` with unchecked warning suppressed. If the attribute holds a different type at runtime, a `ClassCastException` is thrown. No test validates the cast.

---

### GPSReportAction — Findings

---

**A18-16 | Severity: CRITICAL | No test coverage for GPSReportAction.execute — entire class is untested**

`GPSReportAction.execute` is the sole method of the class. No test exercises it under any condition. All logic paths — normal flow, null session, null `sessCompId`, and the static `UnitDAO` call — are completely uncovered.

---

**A18-17 | Severity: CRITICAL | Null session causes NullPointerException — no guard on getSession(false)**

Line 25: `HttpSession session = request.getSession(false);`
Line 26: `String sessCompId = (String) session.getAttribute("sessCompId");`

If no session exists, `getSession(false)` returns `null` and line 26 throws `NullPointerException`. No test covers an unauthenticated request, and there is no null check before the attribute access.

---

**A18-18 | Severity: CRITICAL | RuntimeException thrown for null sessCompId — no test for the guard condition**

Line 27:
```java
if (sessCompId == null) throw new RuntimeException("Must have valid user logged in here");
```
This is the only active null guard in the class. No test confirms this guard fires, that the message is correct, or that the framework handles the unchecked `RuntimeException` appropriately. Throwing an unchecked exception from a Struts action is non-standard and may produce a generic 500 error rather than a proper redirect to an error or login page.

---

**A18-19 | Severity: HIGH | NumberFormatException if sessCompId is not parseable as Long or Integer**

Line 32: `Long compId = Long.valueOf(sessCompId);`
Line 38: `UnitDAO.getAllUnitsByCompanyId(Integer.parseInt(sessCompId));`

Both `Long.valueOf` and `Integer.parseInt` throw `NumberFormatException` if `sessCompId` is not a valid integer string (e.g. if session data is corrupted or truncated). No test covers this path.

---

**A18-20 | Severity: HIGH | Static `UnitDAO.getAllUnitsByCompanyId` call throws checked `SQLException` — propagated as unhandled exception**

Line 38: `request.setAttribute("arrAdminUnit", UnitDAO.getAllUnitsByCompanyId(Integer.parseInt(sessCompId)));`

`getAllUnitsByCompanyId` is declared to throw `SQLException`. The `execute` method signature declares `throws Exception`, so the exception propagates to the Struts exception handler uncaught. No test exercises what happens when the DAO call fails (database down, invalid company ID). No error forwarding is configured in the active code.

---

**A18-21 | Severity: HIGH | Three instance fields (reportService, manufactureDAO, unitDAO) are initialised but two are entirely unused in active code — dead code risk**

Lines 19–21:
```java
private ReportService reportService = ReportService.getInstance();
private ManufactureDAO manufactureDAO = ManufactureDAO.getInstance();
private UnitDAO unitDAO = UnitDAO.getInstance();
```
`reportService` and `manufactureDAO` are never referenced in active (non-commented) code. `unitDAO` is also not used directly — the active call is to the static method `UnitDAO.getAllUnitsByCompanyId`. These eager singleton initialisations execute at construction time, potentially acquiring database connections or other resources unnecessarily. No test verifies construction-time side effects or confirms that these fields are intentionally present.

---

**A18-22 | Severity: HIGH | Large blocks of commented-out code hide intended functionality — no test coverage of the removed logic**

Lines 35–36, 39, 41–42 contain commented-out calls to:
- `manufactureDAO.getAllManufactures(sessCompId)` — manufacturer dropdown population
- `unitDAO.getAllUnitType()` — unit type dropdown population
- `reportService.getImpactReport(compId, searchForm.getImpactReportFilter(dateFormat), dateTimeFormat, timezone)` — the core GPS impact report

The action currently sets only `"arrAdminUnit"` in the request. The view layer may still reference `"impactReport"` or manufacturer/unit-type attributes, causing silent null values in JSP rendering. No test verifies what the view receives or that commented-out code is intentionally disabled rather than accidentally omitted.

---

**A18-23 | Severity: MEDIUM | Session attributes sessDateFormat, sessDateTimeFormat, sessTimezone, and compId are read but never used in active code**

Lines 29–32 read four session attributes and assign them to local variables. None of these variables are referenced in the active (non-commented) execution path. If the commented-out report code is re-enabled without these variables being correctly populated, the report will use null format strings. No test validates that these values are correctly extracted or that their absence is tolerated.

---

**A18-24 | Severity: MEDIUM | GPSReportSearchForm is cast from ActionForm but getGPSReportFilter() is never called in active code**

Line 34: `GPSReportSearchForm searchForm = (GPSReportSearchForm) form;`

The form object is populated by Struts from request parameters but is then unused in active code. The cast itself can throw `ClassCastException` if Struts maps a different form type to this action. No test verifies the cast succeeds or that form field bindings work correctly.

---

**A18-25 | Severity: MEDIUM | No test for Integer.parseInt(sessCompId) overflow — company ID larger than Integer.MAX_VALUE**

Line 38: `Integer.parseInt(sessCompId)` — if `sessCompId` holds a value that fits in a `Long` but exceeds `Integer.MAX_VALUE` (2,147,483,647), `parseInt` throws `NumberFormatException`. Line 32 uses `Long.valueOf` suggesting large IDs may be anticipated. No test covers this discrepancy.

---

**A18-26 | Severity: LOW | GPSReportAction is not thread-safe — instance fields initialised at construction time in a shared Struts action singleton**

Struts 1.x actions are typically shared as singletons across requests. The three instance fields (`reportService`, `manufactureDAO`, `unitDAO`) are initialised once and shared. If any singleton DAO/service holds mutable state, concurrent requests can cause race conditions. No test exercises concurrent access.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A18-1 | CRITICAL | FormBuilderAction | No test coverage — entire class untested |
| A18-2 | CRITICAL | FormBuilderAction | Null session → NullPointerException, no guard |
| A18-3 | CRITICAL | FormBuilderAction | Null/empty "arrDriver" session attribute → NPE or IndexOutOfBoundsException |
| A18-4 | CRITICAL | FormBuilderAction | Empty QuestionDAO result → IndexOutOfBoundsException on .get(0) |
| A18-5 | CRITICAL | FormBuilderAction | SQL Injection via unsanitised qid and type parameters |
| A18-6 | HIGH | FormBuilderAction | Empty entity list in save branch → IndexOutOfBoundsException |
| A18-7 | HIGH | FormBuilderAction | Save branch entirely untested — email dispatch path uncovered |
| A18-8 | HIGH | FormBuilderAction | Reflected XSS: raw request parameters in HTML email body |
| A18-9 | HIGH | FormBuilderAction | Empty-library error message uses raw "action" variable — misleading and untested |
| A18-10 | MEDIUM | FormBuilderAction | qid default "0" path untested |
| A18-11 | MEDIUM | FormBuilderAction | Non-numeric qid causes NumberFormatException/SQL syntax error in DAO |
| A18-12 | MEDIUM | FormBuilderAction | Empty/blank type parameter propagated to DAO untested |
| A18-13 | MEDIUM | FormBuilderAction | BeanComparator sort with null position values untested |
| A18-14 | LOW | FormBuilderAction | Raw Enumeration; empty parameter set path untested |
| A18-15 | LOW | FormBuilderAction | Unchecked cast of session attribute — ClassCastException untested |
| A18-16 | CRITICAL | GPSReportAction | No test coverage — entire class untested |
| A18-17 | CRITICAL | GPSReportAction | Null session → NullPointerException, no guard |
| A18-18 | CRITICAL | GPSReportAction | RuntimeException for null sessCompId — guard untested, non-standard error handling |
| A18-19 | HIGH | GPSReportAction | NumberFormatException if sessCompId not numeric |
| A18-20 | HIGH | GPSReportAction | SQLException from UnitDAO propagates unhandled to Struts framework |
| A18-21 | HIGH | GPSReportAction | Two instance fields (reportService, manufactureDAO) unused in active code — dead code |
| A18-22 | HIGH | GPSReportAction | Large commented-out code blocks hide intended functionality — impact report never built |
| A18-23 | MEDIUM | GPSReportAction | Four session attributes read but unused in active code path |
| A18-24 | MEDIUM | GPSReportAction | GPSReportSearchForm cast but getGPSReportFilter() never called — ClassCastException risk |
| A18-25 | MEDIUM | GPSReportAction | Integer.parseInt vs Long.valueOf for sessCompId — potential overflow |
| A18-26 | LOW | GPSReportAction | Instance fields in Struts singleton action — thread-safety risk |

---

## 5. Statistics

| Metric | FormBuilderAction | GPSReportAction |
|--------|-------------------|-----------------|
| Total methods | 1 | 1 |
| Methods with any test | 0 | 0 |
| Method coverage | 0% | 0% |
| CRITICAL findings | 5 | 3 |
| HIGH findings | 4 | 4 |
| MEDIUM findings | 4 | 3 |
| LOW findings | 2 | 1 |
| Total findings | 15 | 11 |

**Grand total findings: 26**
**Overall action-class test coverage: 0%**
