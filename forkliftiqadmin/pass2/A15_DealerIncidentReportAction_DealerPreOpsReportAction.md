# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A15
**Files audited:**
- `src/main/java/com/action/DealerIncidentReportAction.java`
- `src/main/java/com/action/DealerPreOpsReportAction.java`

---

## 1. Reading Evidence

### 1.1 DealerIncidentReportAction
**File:** `src/main/java/com/action/DealerIncidentReportAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

**Fields / Constants defined:** none (no instance fields, no static constants declared in this class)

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 19 |

**Execution path inside `execute` (line-by-line logic):**
- L23: `request.getSession(false)` — returns `null` if no session exists
- L24: `session.getAttribute("sessCompId")` — cast to `String`
- L25: Guard: throws `RuntimeException` if `sessCompId == null`
- L27-29: Reads `sessDateFormat`, `sessDateTimeFormat`, `sessTimezone` from session — no null guard on any of these three
- L30: `Integer.parseInt(sessCompId)` — can throw `NumberFormatException`
- L32: Downcasts `form` to `IncidentReportSearchForm` — can throw `ClassCastException`
- L33: `ManufactureDAO.getAllManufactures(sessCompId)` — static call, throws `Exception`
- L34: `UnitDAO.getAllUnitType()` — static call, throws `Exception`
- L36: `ReportService.getInstance().getIncidentReport(...)` — singleton call, throws `ReportServiceException`
- L37: `request.setAttribute("incidentReport", incidentReport)`
- L38: `mapping.findForward("report")`

---

### 1.2 DealerPreOpsReportAction
**File:** `src/main/java/com/action/DealerPreOpsReportAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

**Fields / Constants defined:** none (no instance fields, no static constants declared in this class)

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 19 |

**Execution path inside `execute` (line-by-line logic):**
- L23: `request.getSession(false)` — returns `null` if no session exists
- L24: `session.getAttribute("sessCompId")` — cast to `String`
- L25: Guard: throws `RuntimeException` if `sessCompId == null`
- L27: `Long.valueOf(sessCompId)` — can throw `NumberFormatException`
- L28-30: Reads `sessDateFormat`, `sessDateTimeFormat`, `sessTimezone` from session — no null guard on any of these three
- L32: Downcasts `form` to `PreOpsReportSearchForm` — can throw `ClassCastException`
- L33: `ManufactureDAO.getAllManufactures(sessCompId)` — static call, throws `Exception`
- L34: `UnitDAO.getAllUnitType()` — static call, throws `Exception`
- L36-39: `ReportService.getInstance().getPreOpsCheckReport(...)` — singleton call, throws `ReportServiceException`
- L40: `request.setAttribute("preOpsReport", preOpsReportBean)`
- L42: `return mapping.findForward("report")`

---

## 2. Test Coverage Confirmation

**Test files present in `src/test/java/` (all 4):**
```
com/calibration/UnitCalibrationImpactFilterTest.java
com/calibration/UnitCalibrationTest.java
com/calibration/UnitCalibratorTest.java
com/util/ImpactUtilTest.java
```

**Grep results for any reference to audited classes or their dependencies:**

| Search term | Matches in test directory |
|---|---|
| `DealerIncidentReportAction` | 0 |
| `DealerPreOpsReportAction` | 0 |
| `IncidentReportSearchForm` | 0 |
| `PreOpsReportSearchForm` | 0 |
| `ReportService` | 0 |
| `getIncidentReport` | 0 |
| `getPreOpsCheckReport` | 0 |
| `incidentReport` | 0 |
| `preOpsReport` | 0 |

**Conclusion:** Zero direct or indirect test coverage exists for either action class.

---

## 3. Coverage Gaps — All Findings

---

### DealerIncidentReportAction

**A15-1 | Severity: CRITICAL | No test coverage for DealerIncidentReportAction.execute — happy path**
The `execute` method (L19-39) has zero test coverage. The entire happy-path execution — session attribute extraction, DAO population of the search form, service call, and forward resolution — is completely untested. Any regression in this method would be undetected by the test suite.

---

**A15-2 | Severity: CRITICAL | Null session not guarded — NullPointerException on getSession(false)**
At L23, `request.getSession(false)` returns `null` when no HTTP session exists (e.g., session expired, request made without prior authentication). The return value is stored directly in `session` and immediately dereferenced at L24 without a null check. This throws an unhandled `NullPointerException` rather than a controlled error response. No test verifies this failure mode, and the code provides no safe fallback. This is distinct from the `sessCompId == null` guard at L25 which only fires if the session object itself exists.

---

**A15-3 | Severity: CRITICAL | Null session not guarded — NullPointerException on getSession(false) (DealerPreOpsReportAction — see A15-12 for counterpart; this entry covers DealerIncidentReportAction)**
*(Cross-reference: the same defect exists in DealerPreOpsReportAction; see A15-12.)*

---

**A15-4 | Severity: HIGH | NumberFormatException from Integer.parseInt(sessCompId) not tested**
At L30, `Integer.parseInt(sessCompId)` will throw `NumberFormatException` if the session attribute `sessCompId` contains a non-numeric string (e.g., due to session corruption or injection). The guard at L25 only catches `null`; a non-numeric non-null value is uncaught. No test covers this edge case.

---

**A15-5 | Severity: HIGH | Null session attributes sessDateFormat, sessDateTimeFormat, sessTimezone — not guarded and not tested**
At L27-29, three session attributes (`sessDateFormat`, `sessDateTimeFormat`, `sessTimezone`) are read without null checks. If any of these are absent from the session (partially initialized session, attribute cleared elsewhere), the value is silently `null`. These nulls are then passed downstream to `getIncidentReportFilter(dateFormat)` and `getIncidentReport(..., dateTimeFormat, timezone)`. The behavior of the downstream service with null format/timezone arguments is untested and may cause `NullPointerException`, incorrect SQL, or malformed date parsing. No test covers any of these null attribute scenarios.

---

**A15-6 | Severity: HIGH | ClassCastException from ActionForm downcast not tested**
At L32, `form` is blindly cast to `IncidentReportSearchForm`. If the Struts framework supplies a different `ActionForm` subtype (misconfiguration, routing error), a `ClassCastException` is thrown. No test verifies that the action handles or propagates this gracefully.

---

**A15-7 | Severity: HIGH | ManufactureDAO.getAllManufactures exception path not tested**
At L33, `ManufactureDAO.getAllManufactures(sessCompId)` is a static call declared to throw `Exception`. If the database is unavailable or the query fails, the exception propagates unhandled through `execute`. No test mocks this failure or verifies the resulting error behavior.

---

**A15-8 | Severity: HIGH | UnitDAO.getAllUnitType exception path not tested**
At L34, `UnitDAO.getAllUnitType()` is a static call declared to throw `Exception`. Database failures here propagate unhandled. No test covers this failure path.

---

**A15-9 | Severity: HIGH | ReportService.getIncidentReport ReportServiceException not tested**
At L36, `ReportService.getInstance().getIncidentReport(...)` throws `ReportServiceException` (wrapping `SQLException`) if the underlying DAO query fails. This exception propagates out of `execute` uncaught. No test verifies the service failure scenario or its user-visible impact.

---

**A15-10 | Severity: MEDIUM | ReportService singleton initialization not tested under concurrent access**
`ReportService.getInstance()` (ReportService.java L20-27) uses a non-double-checked locking pattern: the null check is outside `synchronized` but instance assignment is inside. Under race conditions on first initialization, two threads can observe `theInstance == null` simultaneously, with one overwriting the other's newly-created instance. No test exercises concurrent initialization. While not strictly a gap in action testing, the action's direct dependency on this pattern is untested.

---

**A15-11 | Severity: MEDIUM | mapping.findForward("report") return value not tested**
At L38, `mapping.findForward("report")` may return `null` if the "report" forward is not configured in struts-config.xml. No test verifies that the correct forward name is returned or that a null forward is handled appropriately.

---

### DealerPreOpsReportAction

**A15-12 | Severity: CRITICAL | No test coverage for DealerPreOpsReportAction.execute — happy path**
The `execute` method (L19-43) has zero test coverage. The entire happy-path — session attribute extraction, `Long.valueOf` conversion, DAO population of the search form, service call, and forward resolution — is completely untested.

---

**A15-13 | Severity: CRITICAL | Null session not guarded — NullPointerException on getSession(false)**
Identical defect to A15-2. At L23, `request.getSession(false)` returns `null` for expired or non-existent sessions. The result is immediately dereferenced at L24 with no null check, producing an uncontrolled `NullPointerException`. No test covers this scenario.

---

**A15-14 | Severity: HIGH | NumberFormatException from Long.valueOf(sessCompId) not tested**
At L27, `Long.valueOf(sessCompId)` will throw `NumberFormatException` for non-numeric values of `sessCompId`. Unlike `DealerIncidentReportAction` which uses `Integer.parseInt`, this action uses `Long.valueOf`, but the failure mode is identical. No test covers this edge case.

---

**A15-15 | Severity: HIGH | Null session attributes sessDateFormat, sessDateTimeFormat, sessTimezone — not guarded and not tested**
At L28-30, three session attributes are read without null checks — identical to A15-5. These nulls flow into `getPreOpsReportFilter(dateFormat)` and `getPreOpsCheckReport(..., dateTimeFormat, timezone)`. No test covers null attribute scenarios.

---

**A15-16 | Severity: HIGH | ClassCastException from ActionForm downcast not tested**
At L32, `form` is blindly cast to `PreOpsReportSearchForm`. A Struts misconfiguration or routing error supplying a different form type throws `ClassCastException`. No test covers this.

---

**A15-17 | Severity: HIGH | ManufactureDAO.getAllManufactures exception path not tested**
At L33, same static DAO call as in `DealerIncidentReportAction`. Database failures throw an unhandled `Exception`. No test covers this failure path.

---

**A15-18 | Severity: HIGH | UnitDAO.getAllUnitType exception path not tested**
At L34, same static DAO call as in `DealerIncidentReportAction`. Database failures throw an unhandled `Exception`. No test covers this failure path.

---

**A15-19 | Severity: HIGH | ReportService.getPreOpsCheckReport ReportServiceException not tested**
At L36-39, `ReportService.getInstance().getPreOpsCheckReport(...)` throws `ReportServiceException` (wrapping `SQLException`) on DAO failure. This propagates unhandled. No test covers this.

---

**A15-20 | Severity: MEDIUM | mapping.findForward("report") return value not tested**
At L42, same issue as A15-11. `mapping.findForward("report")` may return `null`. No test verifies the forward name or handles a null return.

---

### Cross-Cutting Findings (both classes)

**A15-21 | Severity: HIGH | Both actions share identical structural defects with no shared base class or tested utility**
`DealerIncidentReportAction` and `DealerPreOpsReportAction` contain essentially duplicate session-handling and DAO-loading logic with no shared superclass or utility method to centralize the pattern. The duplicated untested code doubles the surface area for defects. No test exists for either implementation.

---

**A15-22 | Severity: HIGH | Type mismatch between companyId representations — int vs Long — not tested**
`DealerIncidentReportAction` parses `sessCompId` as `int` (L30: `Integer.parseInt`) and passes it to `ReportService.getIncidentReport(int compId, ...)`. `DealerPreOpsReportAction` parses `sessCompId` as `Long` (L27: `Long.valueOf`) and passes it to `ReportService.getPreOpsCheckReport(Long compId, ...)`. No test validates that the same session attribute value is consistently safe at both narrowing (int) and widening (Long) conversions, particularly for company IDs exceeding `Integer.MAX_VALUE`.

---

**A15-23 | Severity: MEDIUM | ReportService is a non-resettable singleton — untestable in isolation without reflection or test framework support**
Both actions call `ReportService.getInstance()` which stores a singleton in a static field (`theInstance`) with no reset mechanism. This design prevents proper unit testing with mock services unless Mockito's `mockStatic`, PowerMock, or reflection-based field reset is used. No test infrastructure of this kind is present in the project. The singleton pattern makes the actions inherently difficult to unit test as written.

---

**A15-24 | Severity: MEDIUM | Static DAO methods ManufactureDAO.getAllManufactures and UnitDAO.getAllUnitType cannot be mocked without PowerMock or equivalent**
Both actions call static methods on `ManufactureDAO` and `UnitDAO`. Standard Mockito cannot mock static methods, meaning these database-hitting calls cannot be isolated in unit tests without additional tooling (e.g., PowerMock, Mockito-inline, or refactoring to instance methods). No such tooling is configured in the project, and no tests attempt to isolate these calls.

---

**A15-25 | Severity: LOW | No test verifies that "incidentReport" and "preOpsReport" request attributes are set correctly**
Both actions set a report bean on the request (`request.setAttribute("incidentReport", ...)` at L37 of `DealerIncidentReportAction`; `request.setAttribute("preOpsReport", ...)` at L40 of `DealerPreOpsReportAction`). No test verifies that the correct attribute name is used, that the bean is non-null on success, or that the JSP-expected attribute name matches the key set in the action.

---

**A15-26 | Severity: LOW | No integration test or smoke test exists for either Struts action mapping**
There is no test — unit, integration, or functional — confirming that these action classes are correctly wired in `struts-config.xml` with the appropriate form bean, input path, and forward declarations. A misconfigured action mapping would cause a runtime 500 error invisible to the current test suite.

---

## 4. Summary Table

| Finding | Severity | Class(es) | Description |
|---------|----------|-----------|-------------|
| A15-1 | CRITICAL | DealerIncidentReportAction | No test coverage — happy path |
| A15-2 | CRITICAL | DealerIncidentReportAction | NPE: null session from getSession(false) |
| A15-4 | HIGH | DealerIncidentReportAction | NumberFormatException from Integer.parseInt(sessCompId) |
| A15-5 | HIGH | DealerIncidentReportAction | Null sessDateFormat/sessDateTimeFormat/sessTimezone not guarded |
| A15-6 | HIGH | DealerIncidentReportAction | ClassCastException from ActionForm downcast |
| A15-7 | HIGH | DealerIncidentReportAction | ManufactureDAO.getAllManufactures exception path untested |
| A15-8 | HIGH | DealerIncidentReportAction | UnitDAO.getAllUnitType exception path untested |
| A15-9 | HIGH | DealerIncidentReportAction | ReportService.getIncidentReport ReportServiceException untested |
| A15-10 | MEDIUM | DealerIncidentReportAction | ReportService singleton race condition untested |
| A15-11 | MEDIUM | DealerIncidentReportAction | mapping.findForward("report") null return untested |
| A15-12 | CRITICAL | DealerPreOpsReportAction | No test coverage — happy path |
| A15-13 | CRITICAL | DealerPreOpsReportAction | NPE: null session from getSession(false) |
| A15-14 | HIGH | DealerPreOpsReportAction | NumberFormatException from Long.valueOf(sessCompId) |
| A15-15 | HIGH | DealerPreOpsReportAction | Null sessDateFormat/sessDateTimeFormat/sessTimezone not guarded |
| A15-16 | HIGH | DealerPreOpsReportAction | ClassCastException from ActionForm downcast |
| A15-17 | HIGH | DealerPreOpsReportAction | ManufactureDAO.getAllManufactures exception path untested |
| A15-18 | HIGH | DealerPreOpsReportAction | UnitDAO.getAllUnitType exception path untested |
| A15-19 | HIGH | DealerPreOpsReportAction | ReportService.getPreOpsCheckReport ReportServiceException untested |
| A15-20 | MEDIUM | DealerPreOpsReportAction | mapping.findForward("report") null return untested |
| A15-21 | HIGH | Both | Duplicated session-handling logic doubles untested defect surface |
| A15-22 | HIGH | Both | int vs Long companyId type mismatch untested |
| A15-23 | MEDIUM | Both | ReportService non-resettable singleton prevents unit testing |
| A15-24 | MEDIUM | Both | Static DAO methods cannot be mocked with standard Mockito |
| A15-25 | LOW | Both | Request attribute name correctness not verified by any test |
| A15-26 | LOW | Both | No test for Struts action mapping wiring |

**Totals:** 4 CRITICAL, 12 HIGH, 5 MEDIUM, 2 LOW — 23 distinct findings across 2 classes.
