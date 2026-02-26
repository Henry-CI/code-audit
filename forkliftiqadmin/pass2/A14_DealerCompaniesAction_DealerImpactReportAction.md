# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A14
**Date:** 2026-02-26
**Scope:** DealerCompaniesAction, DealerImpactReportAction

---

## 1. Reading Evidence

### 1.1 DealerCompaniesAction
**File:** `src/main/java/com/action/DealerCompaniesAction.java`
**Class:** `com.action.DealerCompaniesAction extends org.apache.struts.action.Action`

**Fields / Constants defined:** None (no instance fields, no static constants).

**Methods:**

| # | Method | Line | Signature |
|---|--------|------|-----------|
| 1 | `execute` | 20 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

**Imports used at runtime:**
- `org.apache.struts.action.{Action, ActionForm, ActionForward, ActionMapping}`
- `com.bean.CompanyBean`
- `com.dao.CompanyDAO` (static method `getSubCompanies`)
- `javax.servlet.http.{HttpServletRequest, HttpServletResponse, HttpSession}`
- `java.util.{ArrayList, List}`

**Logic summary of `execute` (lines 20–39):**
1. Obtains `HttpSession` via `request.getSession(false)`.
2. Reads request parameter `"action"` — defaults to `""` if null (ternary on line 25).
3. Reads `session.getAttribute("sessCompId")` and calls `.toString()` on the result — no null guard (line 26).
4. Branch A (`action.equalsIgnoreCase("add")`, line 28):
   - Creates a new `ArrayList<CompanyBean>`, adds one empty `CompanyBean`, sets it as request attribute `"companyRecord"`, returns forward `"add"`.
5. Branch B (else, line 33):
   - Sets request attribute `"isDealer"` from session attribute `"isDealer"`.
   - Calls `CompanyDAO.getSubCompanies(companyId)` and sets result as `"subCompanyLst"`.
   - Returns forward `"list"`.

---

### 1.2 DealerImpactReportAction
**File:** `src/main/java/com/action/DealerImpactReportAction.java`
**Class:** `com.action.DealerImpactReportAction extends org.apache.struts.action.Action`

**Fields / Constants defined:** None (no instance fields, no static constants).

**Methods:**

| # | Method | Line | Signature |
|---|--------|------|-----------|
| 1 | `execute` | 19 | `public ActionForward execute(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception` |

**Imports used at runtime:**
- `com.actionform.ImpactReportSearchForm`
- `com.bean.ImpactReportBean`
- `com.dao.ManufactureDAO` (static method `getAllManufactures`)
- `com.dao.UnitDAO` (singleton via `getInstance()`, then `getAllUnitType()`)
- `com.service.ReportService` (singleton via `getInstance()`, then `getImpactReport()`)
- `org.apache.struts.action.{Action, ActionForm, ActionForward, ActionMapping}`
- `javax.servlet.http.{HttpServletRequest, HttpServletResponse, HttpSession}`

**Logic summary of `execute` (lines 19–44):**
1. Obtains `HttpSession` via `request.getSession(false)`.
2. Reads `session.getAttribute("sessCompId")` cast to `String` (line 24).
3. Explicit null check: if `sessCompId == null` throws `RuntimeException("Must have valid user logged in here")` (line 25).
4. Reads three further session attributes: `"sessDateFormat"`, `"sessDateTimeFormat"`, `"sessTimezone"` — no null guards on any of them (lines 27–29).
5. Converts `sessCompId` to `Long` via `Long.valueOf(sessCompId)` — will throw `NumberFormatException` if non-numeric (line 30).
6. Casts `form` to `ImpactReportSearchForm` — unchecked cast, will throw `ClassCastException` if wrong form type (line 32).
7. Calls `ManufactureDAO.getAllManufactures(sessCompId)` and `UnitDAO.getInstance().getAllUnitType()` to populate the search form (lines 33–34).
8. Calls `ReportService.getInstance().getImpactReport(compId, searchForm.getImpactReportFilter(dateFormat), dateTimeFormat, timezone)` (lines 36–39).
9. Sets result as request attribute `"impactReport"` and returns forward `"report"` (lines 41–43).

---

## 2. Test Directory Grep Results

**Test files found (4 total):**
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

**Grep for target class names and all directly invoked dependencies across all 4 test files:**

Pattern searched: `DealerCompaniesAction|DealerImpactReportAction|CompanyDAO|ManufactureDAO|UnitDAO|ReportService|ImpactReportSearchForm|CompanyBean`

**Result: No matches found.**

No test file references either action class, either action class's DAO/service dependencies, or any of the related bean/form types that would imply indirect coverage. Both classes have **zero test coverage**.

---

## 3. Coverage Gap Analysis

### 3.1 DealerCompaniesAction — All Gaps

#### 3.1.1 Null Session Object
`request.getSession(false)` can return `null` when no session exists. Every subsequent access via `session.getAttribute(...)` or `session.getAttribute(...).toString()` will then throw a `NullPointerException`. There is no null check on the returned session object. This is the first operation in `execute` and its failure is completely untested.

#### 3.1.2 Null `sessCompId` Session Attribute
On line 26, `session.getAttribute("sessCompId").toString()` is called without any null guard. If the session exists but `"sessCompId"` has not been set (e.g., partial session state, session attribute cleared), a `NullPointerException` is thrown at `.toString()`. Unlike `DealerImpactReportAction`, there is no explicit null check here. This path is untested.

#### 3.1.3 "add" Branch — Happy Path
The entire `action.equalsIgnoreCase("add")` branch (lines 28–32) is untested. A test should verify:
- The forward name returned is `"add"`.
- The request attribute `"companyRecord"` is set.
- The list contains exactly one element.
- The element is an empty (default-constructed) `CompanyBean`.

#### 3.1.4 "add" Branch — Forward Resolution Failure
`mapping.findForward("add")` can return `null` if the forward is not configured in `struts-config.xml`. This return value is never null-checked. The path where the forward is missing is untested.

#### 3.1.5 Default (List) Branch — Happy Path
The entire else branch (lines 33–38) is untested. A test should verify:
- The forward name returned is `"list"`.
- `"isDealer"` is set from the session attribute.
- `"subCompanyLst"` is set with the result of `CompanyDAO.getSubCompanies(companyId)`.

#### 3.1.6 Default Branch — `CompanyDAO.getSubCompanies` Throws Exception
`CompanyDAO.getSubCompanies(companyId)` declares `throws Exception` (ultimately wraps `SQLException`). If the database call fails, the exception propagates out of `execute`. No try/catch is present; the caller (Struts framework) receives the raw exception. This error path is untested.

#### 3.1.7 Default Branch — `"isDealer"` Session Attribute Absent
`session.getAttribute("isDealer")` may return `null` if the attribute was never set. The code sets `null` as the `"isDealer"` request attribute. Downstream JSP behaviour when this is `null` is unvalidated and untested.

#### 3.1.8 Default Branch — Forward `"list"` Resolution Failure
`mapping.findForward("list")` can return `null` if misconfigured. Not null-checked and untested.

#### 3.1.9 Non-"add" / Non-empty Action Parameter Values
The parameter `action` defaults to `""` when null. Any non-null, non-"add" value (e.g., `"edit"`, `"delete"`) silently falls through to the list branch. No validation or rejection of unexpected action values is implemented or tested.

#### 3.1.10 `companyId` Non-Numeric Value
`CompanyDAO.getSubCompanies(companyId)` calls `Long.parseLong(companyId)` internally. If `sessCompId` is set to a non-numeric string in the session, a `NumberFormatException` is thrown inside the DAO and propagates through `execute`. This path is untested.

---

### 3.2 DealerImpactReportAction — All Gaps

#### 3.2.1 Null Session Object
Identical structural issue to DealerCompaniesAction: `request.getSession(false)` can return `null`. All subsequent session attribute reads would throw `NullPointerException`. The explicit null check on line 25 guards only `sessCompId`, not the session itself. The case where session is `null` is untested.

#### 3.2.2 `sessCompId` Null Path — RuntimeException Throw
Line 25 explicitly throws `new RuntimeException("Must have valid user logged in here")` when `sessCompId` is `null`. While the guard exists, this exceptional path is never tested. A test should assert this `RuntimeException` (or a subtype) is thrown with the expected message when `sessCompId` is absent.

#### 3.2.3 `sessDateFormat` Null — No Guard
`session.getAttribute("sessDateFormat")` is cast to `String` with no null check (line 27). If null, it is passed into `searchForm.getImpactReportFilter(dateFormat)` and then into `DateUtil.stringToUTCDate(this.start_date, dateFormat)` within `ImpactReportSearchForm.getImpactReportFilter()`. Depending on `DateUtil`'s tolerance of a null format string, this can produce a `NullPointerException` or silently wrong behaviour. This path is entirely untested.

#### 3.2.4 `sessDateTimeFormat` Null — No Guard
`session.getAttribute("sessDateTimeFormat")` is cast to `String` with no null check (line 28). A null `dateTimeFormat` is passed directly to `ReportService.getImpactReport()` and downstream to `ImpactReportDAO`. Null tolerance is not guaranteed. Untested.

#### 3.2.5 `sessTimezone` Null — No Guard
`session.getAttribute("sessTimezone")` is cast to `String` with no null check (line 29). A null `timezone` is passed to `ReportService.getImpactReport()`. Impact is downstream-dependent and untested.

#### 3.2.6 `sessCompId` Non-Numeric — NumberFormatException
Line 30: `Long.valueOf(sessCompId)` will throw `NumberFormatException` if `sessCompId` is a non-numeric string. No try/catch surrounds this call. This path is untested.

#### 3.2.7 Form Cast to `ImpactReportSearchForm` — ClassCastException
Line 32: `(ImpactReportSearchForm) form` is an unchecked downcast from `ActionForm`. If Struts routes a different form type to this action (misconfiguration), a `ClassCastException` is thrown at runtime. No defensive check or meaningful error message is produced. This path is untested.

#### 3.2.8 `ManufactureDAO.getAllManufactures` Throws Exception
Line 33: `ManufactureDAO.getAllManufactures(sessCompId)` declares `throws Exception` (wraps `SQLException`). A database failure propagates uncaught out of `execute`. This error path is untested.

#### 3.2.9 `UnitDAO.getInstance().getAllUnitType()` Throws Exception
Line 34: `UnitDAO.getInstance().getAllUnitType()` declares `throws Exception` (wraps `SQLException`). A database failure propagates uncaught. `UnitDAO.getInstance()` itself is a singleton that may be in a broken state if the database was unavailable at first access. Both failure paths are untested.

#### 3.2.10 `ReportService.getImpactReport` Throws `ReportServiceException`
Lines 36–39: `ReportService.getInstance().getImpactReport(...)` throws `ReportServiceException` (a `RuntimeException`) when the underlying `ImpactReportDAO` call fails with `SQLException`. This exception propagates out of `execute` uncaught. The error path is untested.

#### 3.2.11 `ReportService` Singleton Race Condition (Double-Checked Locking Defect)
In `ReportService.getInstance()` (lines 20–27 of ReportService.java), the instance is checked outside the synchronized block without the `volatile` keyword on `theInstance`. This is a broken double-checked locking pattern: a partially constructed `ReportService` object can be published to another thread before its constructor completes. While not directly a coverage gap in the action, the action triggers this code path on every request and it is completely untested, including concurrent access scenarios.

#### 3.2.12 `getImpactReportFilter` with Null `dateFormat` Propagating to `DateUtil`
Within `ImpactReportSearchForm.getImpactReportFilter(dateFormat)` (line 36–37 of `ImpactReportSearchForm.java`): when `start_date` or `end_date` are non-blank but `dateFormat` is `null` (gap A14-3.2.3 above), `DateUtil.stringToUTCDate(start_date, null)` is called. The result — exception or silent wrong value — is entirely untested via the action layer.

#### 3.2.13 Forward `"report"` Resolution Failure
`mapping.findForward("report")` on line 43 can return `null` if the forward is not configured. Not null-checked and untested.

#### 3.2.14 Happy Path — No Test
The entire normal execution path (valid session, valid compId, successful DAO/service calls, forward `"report"` returned) has no test. Basic positive-path coverage for this action is completely absent.

---

## 4. Findings

### DealerCompaniesAction

| ID | Severity | Description |
|----|----------|-------------|
| A14-1 | CRITICAL | `execute`: `request.getSession(false)` can return `null`; no null guard before `session.getAttribute(...)` calls — `NullPointerException` on all code paths when no session exists. Zero test coverage for this scenario. |
| A14-2 | CRITICAL | `execute` line 26: `session.getAttribute("sessCompId").toString()` has no null guard on the attribute value — `NullPointerException` if `"sessCompId"` is absent from an existing session. Contrasts with `DealerImpactReportAction` which explicitly guards this. Zero test coverage. |
| A14-3 | HIGH | `execute` "add" branch (lines 28–32): entire positive path is untested — forward name, request attribute `"companyRecord"`, list size, and `CompanyBean` default state are never asserted. |
| A14-4 | HIGH | `execute` else branch (lines 33–38): entire positive path is untested — forward name `"list"`, `"isDealer"` attribute propagation, and `"subCompanyLst"` population are never asserted. |
| A14-5 | HIGH | `execute` else branch: `CompanyDAO.getSubCompanies(companyId)` can throw `Exception` (wraps `SQLException`) on database failure; exception propagates uncaught from `execute`. Error path is untested. |
| A14-6 | MEDIUM | `execute`: any non-null, non-`"add"` value for the `action` parameter (e.g., `"delete"`, `"update"`) silently routes to the list branch with no validation. No test verifies this fallback behaviour or rejects unexpected values. |
| A14-7 | MEDIUM | `execute`: `session.getAttribute("isDealer")` may be `null` if attribute was never set; null is propagated to the request attribute and consumed by JSP. Downstream null-tolerance is unvalidated and untested. |
| A14-8 | MEDIUM | `execute` line 26: `sessCompId` converted via `.toString()` and passed to `CompanyDAO.getSubCompanies()` which internally calls `Long.parseLong(companyId)`; a non-numeric session value produces `NumberFormatException`. Untested. |
| A14-9 | LOW | `mapping.findForward("add")` and `mapping.findForward("list")` can each return `null` on misconfiguration; neither return value is null-checked. Untested. |

---

### DealerImpactReportAction

| ID | Severity | Description |
|----|----------|-------------|
| A14-10 | CRITICAL | `execute`: `request.getSession(false)` can return `null`; there is no null guard on the session object before attribute reads — `NullPointerException` on all code paths when no session exists. Zero test coverage. |
| A14-11 | CRITICAL | `execute` line 32: `(ImpactReportSearchForm) form` is an unchecked cast; a misconfigured Struts mapping supplying the wrong `ActionForm` subtype throws `ClassCastException` at runtime with no defensive handling. Zero test coverage. |
| A14-12 | HIGH | `execute` line 25: `RuntimeException("Must have valid user logged in here")` is thrown when `sessCompId` is `null`; this explicit guard exists but the path is never exercised by any test. |
| A14-13 | HIGH | `execute` line 30: `Long.valueOf(sessCompId)` throws `NumberFormatException` if `sessCompId` is non-numeric (e.g., corrupted session data); no try/catch present and path is untested. |
| A14-14 | HIGH | `execute` lines 33–34: `ManufactureDAO.getAllManufactures()` and `UnitDAO.getInstance().getAllUnitType()` both declare `throws Exception`; database failures propagate uncaught from `execute`. Neither error path is tested. |
| A14-15 | HIGH | `execute` lines 36–39: `ReportService.getInstance().getImpactReport()` throws `ReportServiceException` (unchecked) on DAO failure; exception propagates out of `execute` uncaught. Error path is untested. |
| A14-16 | HIGH | `execute`: the complete happy path (valid session with all required attributes, successful DAO/service calls, forward `"report"` returned) has no test — no positive-case coverage whatsoever. |
| A14-17 | MEDIUM | `execute` lines 27–29: `sessDateFormat`, `sessDateTimeFormat`, and `sessTimezone` are all retrieved without null guards; null values are silently forwarded to downstream DAO/service calls where null-tolerance is not guaranteed. Untested. |
| A14-18 | MEDIUM | `execute` line 36–37: when `dateFormat` is `null` and `start_date`/`end_date` are non-blank, `ImpactReportSearchForm.getImpactReportFilter()` calls `DateUtil.stringToUTCDate(date, null)`; the resulting exception or silent wrong value is untested at the action layer. |
| A14-19 | MEDIUM | `ReportService.getInstance()`: the `theInstance` field is not declared `volatile`, breaking the double-checked locking pattern; a partially constructed instance can be published to concurrent threads. This code path is exercised by every action invocation and is completely untested including under concurrent load. |
| A14-20 | LOW | `mapping.findForward("report")` can return `null` on Struts misconfiguration; not null-checked and untested. |

---

## 5. Summary Statistics

| Class | Methods | Methods with any test coverage | Coverage % |
|-------|---------|-------------------------------|------------|
| `DealerCompaniesAction` | 1 (`execute`) | 0 | 0% |
| `DealerImpactReportAction` | 1 (`execute`) | 0 | 0% |

**Total findings:** 20
**CRITICAL:** 4 (A14-1, A14-2, A14-10, A14-11)
**HIGH:** 9 (A14-3, A14-4, A14-5, A14-12, A14-13, A14-14, A14-15, A14-16)
**MEDIUM:** 6 (A14-6, A14-7, A14-8, A14-17, A14-18, A14-19)
**LOW:** 2 (A14-9, A14-20)

Both classes share a project-wide pattern: the entire `src/test/java` tree (4 files) covers only calibration utilities and an impact utility — no action class, no DAO used by action classes, and no service layer receives any test coverage. Introducing testability for these action classes will require either a Struts mock framework (e.g., `StrutsMock`, Spring MVC Test, or Mockito with manual wiring) or extracting business logic from `execute` into separately testable service/command objects.
