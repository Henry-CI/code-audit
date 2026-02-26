# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A24
**Date:** 2026-02-26
**Files Audited:**
- `src/main/java/com/action/PreOpsReportAction.java`
- `src/main/java/com/action/PrintAction.java`

---

## 1. Reading-Evidence Blocks

### 1.1 PreOpsReportAction

**Full class name:** `com.action.PreOpsReportAction`
**Extends:** `org.apache.struts.action.Action`
**Annotations:** `@Slf4j` (Lombok)

**Fields / Constants (lines 20–22):**

| Line | Field | Type | Initialisation |
|------|-------|------|----------------|
| 20 | `reportService` | `ReportService` | `ReportService.getInstance()` |
| 21 | `manufactureDAO` | `ManufactureDAO` | `ManufactureDAO.getInstance()` |
| 22 | `unitDAO` | `UnitDAO` | `UnitDAO.getInstance()` |

**Methods:**

| Line | Signature |
|------|-----------|
| 25 | `public ActionForward execute(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception` |

**Internal logic inside `execute` (lines 27–46):**
- Line 27: `request.getSession(false)` — session may be null if no active session
- Line 28–31: reads `sessCompId` from session; throws `RuntimeException` if null
- Line 33: `Long.valueOf(sessCompId)` — throws `NumberFormatException` if non-numeric
- Line 34–36: reads `sessDateFormat`, `sessDateTimeFormat`, `sessTimezone` from session (none null-guarded)
- Line 38: casts `form` to `PreOpsReportSearchForm` — unchecked cast
- Line 39: `manufactureDAO.getAllManufactures(sessCompId)` — checked exception propagated
- Line 40: `unitDAO.getAllUnitType()` — checked exception propagated
- Line 41: `preOpsReportSearchForm.setTimezone(timezone)` — timezone may be null
- Line 43: `reportService.getPreOpsCheckReport(...)` with `getPreOpsReportFilter(dateFormat)` — dateFormat may be null
- Line 45: `mapping.findForward("success")` — returns null if forward not configured

---

### 1.2 PrintAction

**Full class name:** `com.action.PrintAction`
**Extends:** `org.apache.struts.action.Action`
**Logger:** `org.apache.log4j.Logger` via `InfoLogger.getLogger`

**Fields (lines 31–32):**

| Line | Field | Type | Initialisation |
|------|-------|------|----------------|
| 31 | `log` (static) | `Logger` | `InfoLogger.getLogger("com.action.PrintAction")` |
| 32 | `unitDAO` | `UnitDAO` | `UnitDAO.getInstance()` |

**Methods:**

| Line | Signature |
|------|-----------|
| 34 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

**Action dispatch branches inside `execute`:**

| Lines | Branch condition | Forward returned |
|-------|-----------------|-----------------|
| 53–97 | `action.equalsIgnoreCase("barcode")` | `"barcodeie"` (IE) or `"barcode"` (non-IE) |
| 98–112 | `action.equalsIgnoreCase("driverbarcode")` | `"driverie"` (IE) or `"driverbarcode"` (non-IE) |
| 113–168 | `action.equalsIgnoreCase("barcodeTime")` | `"barcodeTimeIE"` (IE) or `"barcodeTime"` (non-IE) |
| 170–176 | `else` (default) | `"success"` |

---

## 2. Test-Directory Coverage Confirmation

The project contains exactly four test files:

| File | Package | Classes under test |
|------|---------|-------------------|
| `UnitCalibrationImpactFilterTest.java` | `com.calibration` | `UnitCalibrationImpactFilter` |
| `UnitCalibrationTest.java` | `com.calibration` | `UnitCalibration` |
| `UnitCalibratorTest.java` | `com.calibration` | `UnitCalibrator` |
| `ImpactUtilTest.java` | `com.util` | `ImpactUtil` |

**Grep result for `PreOpsReportAction` across `src/test/java/`:** no matches found.
**Grep result for `PrintAction` across `src/test/java/`:** no matches found.

Neither class is referenced by any test, directly or indirectly.

---

## 3. Coverage Gaps and Findings

### PreOpsReportAction — Findings

---

**A24-1 | Severity: CRITICAL | PreOpsReportAction — zero test coverage on entire class**

`PreOpsReportAction.execute` is the sole method of the class and has no tests whatsoever. The class constitutes the primary pre-ops report entry point; a regression in any dependency would be entirely invisible.

---

**A24-2 | Severity: CRITICAL | Null session causes NullPointerException instead of safe redirect**

Line 27: `request.getSession(false)` deliberately avoids creating a new session and will return `null` when no session exists. The very next line (28) calls `session.getAttribute("sessCompId")` on that potentially-null reference, which throws an unhandled `NullPointerException`. There is no null-check on `session`. No test validates this path and no test confirms users with no session receive a safe error response rather than a 500 error.

```java
HttpSession session = request.getSession(false);          // may be null
String sessCompId = (String)session.getAttribute(...);    // NPE if session == null
```

---

**A24-3 | Severity: HIGH | NumberFormatException on non-numeric sessCompId not caught or tested**

Line 33: `Long.valueOf(sessCompId)` will throw `NumberFormatException` if `sessCompId` contains any non-numeric characters (e.g., empty string `""`, or a corrupt session value). The guard on line 29–31 only catches `null`; it does not catch empty or malformed strings. No test exercises this path.

---

**A24-4 | Severity: HIGH | Session attributes sessDateFormat, sessDateTimeFormat, sessTimezone not null-guarded**

Lines 34–36 read three additional session attributes without any null checks. If any attribute is missing from the session (e.g., after partial session initialisation or session attribute removal), `null` values flow silently into downstream calls:
- `dateFormat` → passed to `getPreOpsReportFilter(dateFormat)` → `DateUtil.stringToUTCDate` may throw
- `dateTimeFormat` → passed to `getPreOpsCheckReport` as a formatting parameter
- `timezone` → set on the form and passed to `getPreOpsCheckReport`

No tests cover any of these null-attribute scenarios.

---

**A24-5 | Severity: HIGH | ReportService singleton dependency not injectable — class is untestable without live infrastructure**

Line 20: `private ReportService reportService = ReportService.getInstance()` and similarly for lines 21–22 (`ManufactureDAO`, `UnitDAO`). All three singletons are concrete, hard-coded field initialisations with no constructor injection or setter injection. This makes the class structurally impossible to unit-test without a live database or extensive static-mocking infrastructure (e.g., PowerMock). No tests exist even with such infrastructure.

---

**A24-6 | Severity: MEDIUM | ActionForm unchecked cast not tested**

Line 38: `(PreOpsReportSearchForm) form` performs an unchecked cast. If the Struts framework routes an incorrect form type to this action (misconfiguration), a `ClassCastException` is thrown at runtime with no error handling. No test verifies the correct form type is always supplied or that the cast is safe.

---

**A24-7 | Severity: MEDIUM | findForward("success") null return not handled**

Line 45: if the Struts action mapping does not define a `"success"` forward, `mapping.findForward("success")` returns `null`. Struts will then throw an exception at the framework level. No test verifies the forward name matches the configuration.

---

**A24-8 | Severity: MEDIUM | No test for happy-path data propagation to request scope**

The single success path (line 43–45) sets `"preOpsReport"` as a request attribute. No test asserts that the attribute is non-null, is of the correct type, or reflects the correct data returned by `ReportService`.

---

### PrintAction — Findings

---

**A24-9 | Severity: CRITICAL | PrintAction — zero test coverage on entire class**

`PrintAction.execute` contains the entirety of the class's logic across four complex dispatch branches (barcode, driverbarcode, barcodeTime, default). None of these branches have any tests.

---

**A24-10 | Severity: CRITICAL | Null session causes NullPointerException — same pattern as PreOpsReportAction**

Line 37: `request.getSession(false)` may return `null`. Line 38 then chains `.getAttribute("sessCompId")` directly onto the result. Unlike `PreOpsReportAction`, `PrintAction` does not even check for null `sessCompId`; it defaults to `""` via the ternary. However the root NPE on `session` itself (before the ternary) is unhandled and untested.

```java
HttpSession session = request.getSession(false);
String sessCompId = (String) session.getAttribute("sessCompId") == null ? "" :
                    (String) session.getAttribute("sessCompId");   // NPE if session==null
```

---

**A24-11 | Severity: CRITICAL | ArrayIndexOutOfBoundsException when arrVeh is empty in "barcode" branch**

Line 86: `arrVeh.get(0).getFule_type_name()` and line 86–87 also access `arrVeh.get(0).getSerial_no()` (line 174 in the default branch). `unitDAO.getUnitById(veh_id)` returns a `List<UnitBean>`. If the vehicle ID does not exist in the database, the list is empty and `get(0)` throws `IndexOutOfBoundsException`. This pattern is repeated in:
- Line 86 (`barcode` branch)
- Line 173–174 (`else`/default branch)

No guard checks `arrVeh.isEmpty()` and no test covers an unknown `veh_id`.

---

**A24-12 | Severity: CRITICAL | NumberFormatException in "driverbarcode" branch when div_id is non-numeric**

Lines 104 and 109: `Integer.parseInt(div_id)` is called without any try/catch. `div_id` defaults to `""` (line 43) when the request parameter is absent. `Integer.parseInt("")` throws `NumberFormatException`. No test covers a missing or malformed `div_id`.

---

**A24-13 | Severity: CRITICAL | NullPointerException in "barcodeTime" branch when "time" parameter is absent**

Line 115: `String time = request.getParameter("time")` — this parameter has no null default unlike the others. Line 118 passes `time` to `Util.getBarcodeTimeLst(time)`, which immediately calls `time.split(" ")`, throwing `NullPointerException` if `time` is null. Additionally, `getBarcodeTimeLst` performs array indexing (`stringlst[0]`, `stringlst[1]`, `datelst[0]`...) assuming a very specific format (`DD/MM/YYYY HH:MM`); any other format causes `ArrayIndexOutOfBoundsException` or `StringIndexOutOfBoundsException`. No test covers null or malformed time input.

---

**A24-14 | Severity: HIGH | UnitDAO singleton and QuestionDAO instantiation make PrintAction untestable without live DB**

Line 32: `unitDAO = UnitDAO.getInstance()` is a hard-coded singleton. Line 46: `QuestionDAO quesionDao = new QuestionDAO()` is instantiated inline inside `execute`, making it impossible to substitute a test double. Both DAO calls execute real SQL. No mock infrastructure exists. The class has no constructor or setter injection points.

---

**A24-15 | Severity: HIGH | Empty arrQues list not handled in "barcode" branch loop**

Lines 57–73: the `for` loop over `arrQues` is safe for an empty list (no iterations). However line 86 (`arrVeh.get(0)`) executes unconditionally after the loop and will throw as described in A24-11. A secondary concern: if `arrQues` is empty, `arrBarCode` is empty, and the view receives an empty question list with no indication that the vehicle has no questions. No test covers this edge case.

---

**A24-16 | Severity: HIGH | No test for any of the six Struts forward names**

`PrintAction` returns six different forwards: `"barcodeie"`, `"barcode"`, `"driverie"`, `"driverbarcode"`, `"barcodeTimeIE"`, `"barcodeTime"`, and `"success"`. None are tested. A typo or misconfiguration in `struts-config.xml` for any of these would only be discovered at runtime.

---

**A24-17 | Severity: HIGH | BarCode file-system write path is not tested and uses a relative path derived from classloader location**

`BarCode.genBarCode` (called throughout `PrintAction`) writes PNG files to a path derived from `getClass().getProtectionDomain().getCodeSource().getLocation().getPath()` (BarCode.java line 124). This path is resolved relative to the deployed WAR structure. In a test environment this path does not exist, `FileOutputStream` will throw `FileNotFoundException`, the exception is silently swallowed in the `catch (Exception e)` block, and the method returns an empty string. No test verifies that barcode generation succeeds, that files are written, or that the silent failure does not corrupt the response sent to users.

---

**A24-18 | Severity: MEDIUM | Browser detection by string equality ("ie") is untested and case-sensitive in practice**

Lines 60, 75, 88, 102, 119 use `browser.equalsIgnoreCase("ie")`. The `browser` parameter defaults to `""` (line 44). No test verifies that every IE-vs-non-IE code path produces the correct forward and request attributes. The IE-specific paths generate barcode data differently (file writes vs. return value) and are particularly fragile.

---

**A24-19 | Severity: MEDIUM | Double call to session.getAttribute("sessCompId") in PrintAction**

Line 38: `session.getAttribute("sessCompId")` is called twice in a single ternary expression. If the session expires or is invalidated between the two calls (extremely unlikely but possible in a concurrent environment), results could be inconsistent. More practically, this is dead-code duplication that is never tested.

---

**A24-20 | Severity: MEDIUM | "barcodeTime" branch: arrTime empty list causes silent empty barcode sequence**

Line 118: `Util.getBarcodeTimeLst(time)` always returns a 10-element list for well-formed input, but if the time string is malformed (but not null), it may return fewer elements or throw. The loop on lines 129–134 and 153–157 does not validate list size. No test covers boundary input to `getBarcodeTimeLst` as invoked from `PrintAction`.

---

**A24-21 | Severity: MEDIUM | Typo in request attribute name "untiSerial" (line 174)**

Line 174: `request.setAttribute("untiSerial", ...)` — the attribute name `"untiSerial"` is a typo for `"unitSerial"`. If any JSP consumes `"unitSerial"`, it will receive `null`. No test exists to detect this kind of attribute-name mismatch between action and view.

---

**A24-22 | Severity: LOW | PrintAction uses org.apache.log4j.Logger while PreOpsReportAction uses Lombok @Slf4j — inconsistent logging strategy**

`PrintAction` (line 31) uses the legacy Log4j 1.x API directly via `InfoLogger.getLogger`. `PreOpsReportAction` uses the Lombok `@Slf4j` annotation (SLF4J facade). The inconsistency increases the surface area for logging misconfiguration and means the two classes cannot be uniformly controlled through a single logging abstraction. No test validates logging output from either class.

---

**A24-23 | Severity: LOW | QuestionDAO local variable is misspelled ("quesionDao")**

Line 46: `QuestionDAO quesionDao = new QuestionDAO()` — the variable name `quesionDao` omits the letter `t`. This is a cosmetic defect with no runtime impact, but it is indicative of code that has never been reviewed or tested.

---

**A24-24 | Severity: INFO | No integration or end-to-end tests exist for any Struts action class**

The entire `com.action` package (which includes at minimum `PreOpsReportAction` and `PrintAction`) has no corresponding test package. The four tests that exist cover only calibration utilities and impact utilities. The absence of even a basic Struts mock framework (StrutsTestCase, Spring MVC Test equivalent, or Mockito-based action unit tests) means that all routing, session handling, form binding, and forward resolution are verified only by manual QA.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A24-1 | CRITICAL | PreOpsReportAction | Zero test coverage on entire class |
| A24-2 | CRITICAL | PreOpsReportAction | Null session → NPE before any null check |
| A24-3 | HIGH | PreOpsReportAction | Non-numeric sessCompId → uncaught NumberFormatException |
| A24-4 | HIGH | PreOpsReportAction | Three session attributes used without null guards |
| A24-5 | HIGH | PreOpsReportAction | Singleton dependencies prevent unit testing |
| A24-6 | MEDIUM | PreOpsReportAction | Unchecked ActionForm cast not tested |
| A24-7 | MEDIUM | PreOpsReportAction | findForward("success") null return not handled or tested |
| A24-8 | MEDIUM | PreOpsReportAction | Happy-path request attribute not asserted in any test |
| A24-9 | CRITICAL | PrintAction | Zero test coverage on entire class |
| A24-10 | CRITICAL | PrintAction | Null session → NPE before ternary executes |
| A24-11 | CRITICAL | PrintAction | Empty arrVeh list → IndexOutOfBoundsException (multiple branches) |
| A24-12 | CRITICAL | PrintAction | Absent/non-numeric div_id → NumberFormatException |
| A24-13 | CRITICAL | PrintAction | Null or malformed "time" parameter → NPE / AIOOBE in barcodeTime branch |
| A24-14 | HIGH | PrintAction | Inline DAO instantiation and singleton prevent unit testing |
| A24-15 | HIGH | PrintAction | Empty question list not validated before arrVeh.get(0) |
| A24-16 | HIGH | PrintAction | All six Struts forward names untested |
| A24-17 | HIGH | PrintAction | BarCode filesystem write silently fails; failure untested |
| A24-18 | MEDIUM | PrintAction | IE browser detection branches entirely untested |
| A24-19 | MEDIUM | PrintAction | sessCompId read twice from session in single ternary |
| A24-20 | MEDIUM | PrintAction | barcodeTime branch does not validate arrTime contents |
| A24-21 | MEDIUM | PrintAction | Typo in request attribute name "untiSerial" undetectable without tests |
| A24-22 | LOW | Both | Inconsistent logging: Log4j direct vs. SLF4J/@Slf4j |
| A24-23 | LOW | PrintAction | Misspelled local variable "quesionDao" |
| A24-24 | INFO | Both | No integration/end-to-end tests for any Struts action in the project |

---

*End of report — Agent A24*
