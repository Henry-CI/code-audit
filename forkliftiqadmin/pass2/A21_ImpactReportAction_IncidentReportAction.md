# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A21
**Date:** 2026-02-26
**Files Audited:**
- `src/main/java/com/action/ImpactReportAction.java`
- `src/main/java/com/action/IncidentReportAction.java`

---

## 1. Reading Evidence

### 1.1 ImpactReportAction

**File:** `src/main/java/com/action/ImpactReportAction.java`
**Class:** `ImpactReportAction extends Action` (line 17)
**Package:** `com.action`

**Fields / Constants (instance-level):**

| Name | Type | Initialiser | Line |
|---|---|---|---|
| `reportService` | `ReportService` | `ReportService.getInstance()` | 19 |
| `manufactureDAO` | `ManufactureDAO` | `ManufactureDAO.getInstance()` | 20 |
| `unitDAO` | `UnitDAO` | `UnitDAO.getInstance()` | 21 |

**Methods:**

| Method | Signature | Lines |
|---|---|---|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 24–44 |

**execute() control flow (annotated):**

```
24  execute(mapping, form, request, response)
25    session = request.getSession(false)          // may return null -> NPE
26    sessCompId = session.getAttribute("sessCompId")
27    if sessCompId == null -> throw RuntimeException
29    dateFormat    = session.getAttribute("sessDateFormat")
30    dateTimeFormat= session.getAttribute("sessDateTimeFormat")
31    timezone      = session.getAttribute("sessTimezone")
32    compId        = Long.valueOf(sessCompId)      // may throw NumberFormatException
34    searchForm    = (ImpactReportSearchForm) form // unchecked cast
35    searchForm.setManufacturers(manufactureDAO.getAllManufactures(sessCompId))
36    searchForm.setUnitTypes(unitDAO.getAllUnitType())
37    searchForm.setTimezone(timezone)
39    impactReport  = reportService.getImpactReport(compId, searchForm.getImpactReportFilter(dateFormat), dateTimeFormat, timezone)
41    request.setAttribute("impactReport", impactReport)
43    return mapping.findForward("success")
```

---

### 1.2 IncidentReportAction

**File:** `src/main/java/com/action/IncidentReportAction.java`
**Class:** `IncidentReportAction extends Action` (line 17)
**Package:** `com.action`

**Fields / Constants:** None declared (no instance fields; all dependencies accessed via static methods or local singletons inline).

**Methods:**

| Method | Signature | Lines |
|---|---|---|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 20–47 |

**execute() control flow (annotated):**

```
20  execute(mapping, form, request, response)
22    session = request.getSession(false)              // may return null -> NPE
23    sessCompId = session.getAttribute("sessCompId")
24-26  if sessCompId == null -> throw RuntimeException
28    dateFormat    = session.getAttribute("sessDateFormat")
29    dateTimeFormat= session.getAttribute("sessDateTimeFormat")
30    timezone      = session.getAttribute("sessTimezone")
31    compId        = Integer.parseInt(sessCompId)     // may throw NumberFormatException
33    incidentReportSearchForm = (IncidentReportSearchForm) form  // unchecked cast
34    incidentReportSearchForm.setManufacturers(ManufactureDAO.getAllManufactures(sessCompId))
35    incidentReportSearchForm.setUnitTypes(UnitDAO.getAllUnitType())
36    incidentReportSearchForm.setTimezone(timezone)
38-44  request.setAttribute("incidentReport",
          ReportService.getInstance().getIncidentReport(compId, ..., dateTimeFormat, timezone))
46    return mapping.findForward("success")
```

---

## 2. Test-Directory Coverage Confirmation

**Test files found in** `src/test/java/`:

| File | Scope |
|---|---|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | Tests `UnitCalibrationImpactFilter` only |
| `com/calibration/UnitCalibrationTest.java` | Tests calibration logic only |
| `com/calibration/UnitCalibratorTest.java` | Tests calibration logic only |
| `com/util/ImpactUtilTest.java` | Tests `ImpactUtil` utility methods only |

**Grep results for `ImpactReportAction` in test directory:** 0 matches
**Grep results for `IncidentReportAction` in test directory:** 0 matches
**Grep results for `ReportService`, `getImpactReport`, `getIncidentReport` in test directory:** 0 matches

**Conclusion:** Zero direct or indirect test coverage exists for either action class or for the `ReportService` methods they invoke.

---

## 3. Coverage Gaps — All Untested Methods, Error Paths, and Edge Cases

### A21-1 | Severity: CRITICAL | ImpactReportAction.execute — zero test coverage

The entire `execute` method of `ImpactReportAction` (lines 24–44) has no test of any kind. This is the class's only behaviour. No unit test, no integration test, and no mock-based controller test exists. No execution path through the class has ever been exercised in an automated harness.

---

### A21-2 | Severity: CRITICAL | IncidentReportAction.execute — zero test coverage

The entire `execute` method of `IncidentReportAction` (lines 20–47) has no test of any kind. This is the class's only behaviour. The same complete absence of coverage applies as for A21-1.

---

### A21-3 | Severity: CRITICAL | Null session causes unhandled NullPointerException in both actions

Both actions call `request.getSession(false)` (line 25 in ImpactReportAction; line 22 in IncidentReportAction). `getSession(false)` returns `null` when no session exists. The return value is used immediately on the very next line without a null-check:

```java
// ImpactReportAction line 26
String sessCompId = (String) session.getAttribute("sessCompId");
```

If `session` is null, this throws an unhandled `NullPointerException`, which propagates as an uncaught exception rather than a controlled redirect to a login page or error forward. No test covers this path. This is a security boundary: unauthenticated or session-expired requests should be handled gracefully.

---

### A21-4 | Severity: HIGH | sessCompId null guard throws RuntimeException with no error forward

Both actions throw a bare `RuntimeException` when `sessCompId` is null (ImpactReportAction line 27; IncidentReportAction lines 24–26):

```java
throw new RuntimeException("Must have valid user logged in here");
```

A Struts action should map unauthenticated states to a named forward (e.g., `"login"` or `"error"`) rather than propagating a raw `RuntimeException` up to the container, which will result in a 500 error page. No test validates this authentication-failure path, nor verifies whether an error forward should be returned instead.

---

### A21-5 | Severity: HIGH | NumberFormatException not handled for sessCompId parsing in both actions

`ImpactReportAction` (line 32) calls `Long.valueOf(sessCompId)` and `IncidentReportAction` (line 31) calls `Integer.parseInt(sessCompId)`. If `sessCompId` contains a non-numeric value (e.g., due to session tampering, corruption, or a migration that changed the ID format), a `NumberFormatException` is thrown and propagates uncaught. No test exercises a malformed `sessCompId`.

Note additionally that ImpactReportAction uses `Long` while IncidentReportAction uses `int` / `Integer.parseInt` for the same conceptual field (`compId`), representing a type-consistency defect between two structurally equivalent classes.

---

### A21-6 | Severity: HIGH | Inconsistent compId type between ImpactReportAction (Long) and IncidentReportAction (int)

`ImpactReportAction` stores `compId` as `Long` (line 32: `Long.valueOf(sessCompId)`) and passes it to `ReportService.getImpactReport(Long compId, ...)`. `IncidentReportAction` stores `compId` as `int` (line 31: `Integer.parseInt(sessCompId)`) and passes it to `ReportService.getIncidentReport(int compId, ...)`. These two action classes are structurally parallel, yet they use different primitive representations of the same session attribute. If company IDs exceed `Integer.MAX_VALUE` (2,147,483,647), `IncidentReportAction` will silently truncate or throw. No test covers boundary values or verifies behavioural parity between the two actions.

---

### A21-7 | Severity: HIGH | ImpactReportAction holds singleton DAOs as instance fields — untestable without framework support

`ImpactReportAction` initialises `reportService`, `manufactureDAO`, and `unitDAO` eagerly at field-declaration time (lines 19–21) using singleton getter calls. There is no constructor injection, setter injection, or any seam for substituting test doubles. As a result, any test of `ImpactReportAction` would require a live database or extensive use of PowerMock / static-mock frameworks. `IncidentReportAction` has the same structural problem but accesses all dependencies inline via static calls (lines 34–35, 39), making it equally untestable without invasive tooling. No test exists that acknowledges this design constraint.

---

### A21-8 | Severity: HIGH | ReportService.getImpactReport and getIncidentReport — SQLException / ReportServiceException paths untested

Both actions delegate to `ReportService` methods that can throw `ReportServiceException` (wrapping a `SQLException`). Neither action catches this exception; it propagates directly to the Struts framework and will produce a 500 response. No test verifies:
- That a `ReportServiceException` from the service layer causes an appropriate container-level or forward-based error response.
- That the exception message or cause is logged before propagation.

---

### A21-9 | Severity: HIGH | ManufactureDAO.getAllManufactures and UnitDAO.getAllUnitType exceptions propagate uncaught in both actions

Both actions call `ManufactureDAO.getAllManufactures(sessCompId)` (ImpactReportAction line 35; IncidentReportAction line 34) and `UnitDAO.getAllUnitType()` (ImpactReportAction line 36; IncidentReportAction line 35). Both DAO methods declare `throws Exception`. A database failure during lookup of manufacturers or unit types will throw an uncaught exception, crashing the request with a 500 error rather than rendering the form with an empty dropdown and an informational message. No test exercises these failure paths.

---

### A21-10 | Severity: MEDIUM | Unchecked cast of ActionForm to concrete search form type in both actions

`ImpactReportAction` line 34 casts `form` to `ImpactReportSearchForm`; `IncidentReportAction` line 33 casts `form` to `IncidentReportSearchForm`. These are unchecked casts with no instanceof guard. A Struts misconfiguration that wires the wrong form bean to the action path would produce a `ClassCastException` at runtime. No test verifies correct form-type binding or exercises the cast-failure scenario.

---

### A21-11 | Severity: MEDIUM | Session attributes dateFormat, dateTimeFormat, and timezone may be null with no guard in both actions

Both actions retrieve `sessDateFormat` (lines 29/28), `sessDateTimeFormat` (lines 30/29), and `sessTimezone` (lines 31/30) from the session without null-checks. These values are subsequently passed into:
- `searchForm.getImpactReportFilter(dateFormat)` / `incidentReportSearchForm.getIncidentReportFilter(dateFormat)` — internally used by `DateUtil.stringToUTCDate` which may throw on a null format pattern.
- `reportService.getImpactReport(..., dateTimeFormat, timezone)` / `ReportService.getInstance().getIncidentReport(..., dateTimeFormat, timezone)` — null timezone could cause incorrect data rendering or a downstream NullPointerException.

No test verifies behaviour when any of these session attributes is absent.

---

### A21-12 | Severity: MEDIUM | mapping.findForward("success") return value is never validated in both actions

Both actions return `mapping.findForward("success")` as their only forward (ImpactReportAction line 43; IncidentReportAction line 46). If the Struts action mapping does not define a `"success"` forward, `findForward` returns `null`. Struts will then throw a `NullPointerException` at dispatch time. No test verifies that the correct forward name is configured and returned.

---

### A21-13 | Severity: MEDIUM | ImpactReportAction.execute() sets form data (manufacturers, unitTypes, timezone) before calling the service — order-dependence untested

The form is mutated (lines 35–37) before the service call (line 39). If `setManufacturers` or `setUnitTypes` throw, the service is never called and no report is generated. If the service throws, the form is already partially populated. No test verifies the intermediate form state, the order-dependence of these operations, or that the request attribute `"impactReport"` is set correctly (or not set at all) when an error occurs mid-method.

---

### A21-14 | Severity: MEDIUM | IncidentReportAction uses static ManufactureDAO.getAllManufactures call but ImpactReportAction uses instance field — structural inconsistency untested

`IncidentReportAction` calls `ManufactureDAO.getAllManufactures(sessCompId)` as a static method (line 34) and `UnitDAO.getAllUnitType()` as a static method (line 35). `ImpactReportAction` calls the same methods through instance-field singleton references (`this.manufactureDAO.getAllManufactures(...)` line 35; `unitDAO.getAllUnitType()` line 36). No test verifies that both classes obtain identical data from the same DAO, nor that the singleton lifecycle and thread-safety of `ManufactureDAO.getInstance()` / `UnitDAO.getInstance()` behave correctly under concurrent requests.

---

### A21-15 | Severity: MEDIUM | ReportService singleton is not thread-safe — getInstance() has a race condition

`ReportService.getInstance()` (ReportService lines 20–27) checks `theInstance == null` before entering a `synchronized` block, but does not re-check inside the block (classic broken double-checked locking without `volatile`). Under concurrent first access, two threads may both pass the outer null check, and although only one will win the `synchronized` block, the absence of `volatile` on `theInstance` means the second thread may cache a partially-constructed object. Neither action class is tested under concurrency. This is a design defect in a shared dependency that both audited classes depend on.

---

### A21-16 | Severity: LOW | No happy-path test for ImpactReportAction.execute verifying request attribute is set

There is no test that:
1. Provides a valid session with all required attributes.
2. Mocks or stubs `ReportService.getImpactReport` to return a known `ImpactReportBean`.
3. Asserts that `request.getAttribute("impactReport")` returns the expected bean.
4. Asserts that the `ActionForward` returned maps to `"success"`.

---

### A21-17 | Severity: LOW | No happy-path test for IncidentReportAction.execute verifying request attribute is set

Identical gap to A21-16 but for `IncidentReportAction`: no test verifies that `request.getAttribute("incidentReport")` is set to the result of `getIncidentReport`, or that the `"success"` forward is returned under normal conditions.

---

### A21-18 | Severity: LOW | ImpactReportAction filter construction edge cases untested

`ImpactReportSearchForm.getImpactReportFilter(dateFormat)` (called at line 39) contains multiple conditional branches:
- `manu_id == null || manu_id == 0` -> passes null to filter
- `type_id == null || type_id == 0` -> passes null to filter
- Blank `start_date` / `end_date` -> passes null
- Blank `impact_level` -> passes null; non-blank -> calls `ImpactLevel.valueOf(impact_level)` which throws `IllegalArgumentException` on an invalid enum name

None of these branches are exercised through the action layer. In particular the `ImpactLevel.valueOf` failure would propagate as an uncaught `IllegalArgumentException` from inside `execute`.

---

### A21-19 | Severity: LOW | IncidentReportAction filter construction edge cases untested

`IncidentReportSearchForm.getIncidentReportFilter(dateFormat)` contains the same null / blank guards for `manu_id`, `type_id`, `start_date`, `end_date`, and `timezone`. No test exercises these branches through the action.

---

## 4. Summary Table

| Finding | Severity | Description |
|---|---|---|
| A21-1 | CRITICAL | `ImpactReportAction.execute` — zero test coverage |
| A21-2 | CRITICAL | `IncidentReportAction.execute` — zero test coverage |
| A21-3 | CRITICAL | Null session causes unhandled `NullPointerException` in both actions |
| A21-4 | HIGH | Null `sessCompId` throws bare `RuntimeException` instead of error forward |
| A21-5 | HIGH | `NumberFormatException` unhandled for malformed `sessCompId` in both actions |
| A21-6 | HIGH | Inconsistent `compId` type: `Long` in ImpactReportAction vs `int` in IncidentReportAction |
| A21-7 | HIGH | Singleton dependencies injected at field-declaration time — no testability seam in either class |
| A21-8 | HIGH | `ReportServiceException` / `SQLException` paths not handled or tested in either action |
| A21-9 | HIGH | DAO exceptions from `getAllManufactures` / `getAllUnitType` propagate uncaught in both actions |
| A21-10 | MEDIUM | Unchecked `ActionForm` cast with no `instanceof` guard in both actions |
| A21-11 | MEDIUM | Session attributes `dateFormat`, `dateTimeFormat`, `timezone` may be null with no guard |
| A21-12 | MEDIUM | `mapping.findForward("success")` result not validated; returns null on misconfiguration |
| A21-13 | MEDIUM | Form mutation before service call — order-dependence and partial-state on error untested |
| A21-14 | MEDIUM | Structural inconsistency: static vs instance DAO access between the two parallel action classes |
| A21-15 | MEDIUM | `ReportService.getInstance()` uses broken double-checked locking without `volatile` |
| A21-16 | LOW | No happy-path test confirming `"impactReport"` request attribute and `"success"` forward for ImpactReportAction |
| A21-17 | LOW | No happy-path test confirming `"incidentReport"` request attribute and `"success"` forward for IncidentReportAction |
| A21-18 | LOW | `ImpactReportSearchForm.getImpactReportFilter` branches (including `ImpactLevel.valueOf` failure) untested via action |
| A21-19 | LOW | `IncidentReportSearchForm.getIncidentReportFilter` filter-construction branches untested via action |

**Total findings: 19**
CRITICAL: 3 | HIGH: 6 | MEDIUM: 6 | LOW: 4
