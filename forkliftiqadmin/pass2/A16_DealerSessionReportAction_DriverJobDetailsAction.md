# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A16
**Date:** 2026-02-26
**Auditor:** Claude Sonnet 4.6 (claude-sonnet-4-6)

## Source Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/action/DealerSessionReportAction.java` |
| 2 | `src/main/java/com/action/DriverJobDetailsAction.java` |

---

## Section 1: Reading-Evidence Blocks

### 1.1 DealerSessionReportAction

**Class:** `com.action.DealerSessionReportAction`
**Superclass:** `org.apache.struts.action.Action`
**File:** `src/main/java/com/action/DealerSessionReportAction.java`
**Lines:** 1–41

**Fields / Constants defined:**
_(none — no instance fields or static constants are declared in this class)_

**Methods:**

| Method | Signature | Lines | Visibility |
|--------|-----------|-------|------------|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 19–40 | `public` (override) |

**Imports / Static dependencies called inside `execute`:**

| Call site | Line | Type |
|-----------|------|------|
| `request.getSession(false)` | 23 | Instance |
| `session.getAttribute("sessCompId")` | 24 | Instance |
| `session.getAttribute("sessDateFormat")` | 27 | Instance |
| `session.getAttribute("sessDateTimeFormat")` | 28 | Instance |
| `session.getAttribute("sessTimezone")` | 29 | Instance |
| `Integer.parseInt(sessCompId)` | 30 | Static |
| `(SessionReportSearchForm) form` cast | 32 | Cast |
| `UnitDAO.getAllUnitsByCompanyId(companyId)` | 34 | Static |
| `DriverDAO.getAllDriver(sessCompId, true)` | 35 | Static |
| `ReportService.getInstance().getSessionReport(companyId, …)` | 37 | Singleton |
| `sessionReportSearchForm.getSessionReportFilter(dateFormat)` | 37 | Instance |
| `request.setAttribute("vehicles", …)` | 34 | Instance |
| `request.setAttribute("drivers", …)` | 35 | Instance |
| `request.setAttribute("sessionReport", …)` | 38 | Instance |
| `mapping.findForward("report")` | 39 | Instance |

**Struts mapping (from `struts-config.xml` lines 575–581):**

```xml
<action path="/dealerSessionReport"
        name="sessionReportSearchForm"
        type="com.action.DealerSessionReportAction"
        scope="request"
        validate="false">
    <forward name="report" path="dealerSessionReportDefinition"/>
</action>
```

Only one forward defined: `"report"`. No `"failure"`, `"error"`, or exception forward exists within the action mapping itself; exception handling falls through to `global-exceptions`.

---

### 1.2 DriverJobDetailsAction

**Class:** `com.action.DriverJobDetailsAction`
**Superclass:** `org.apache.struts.action.Action`
**File:** `src/main/java/com/action/DriverJobDetailsAction.java`
**Lines:** 1–73

**Fields / Constants defined:**

| Field | Type | Line | Modifier |
|-------|------|------|----------|
| `log` | `org.apache.log4j.Logger` | 26 | `private static` |
| `unitDao` | `UnitDAO` | 28 | `private` (instance) |
| `driverDao` | `DriverDAO` | 29 | `private` (instance) |

**Methods:**

| Method | Signature | Lines | Visibility |
|--------|-----------|-------|------------|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 31–70 | `public` |

**Struts mappings (from `struts-config.xml` lines 463–489):**

Three distinct Struts action paths are mapped to this single class:

| Path | Form | Forwards declared |
|------|------|-------------------|
| `/driverjob` | _(none)_ | `assign_driver`, `joblist`, `error` |
| `/jobdetails` | _(none)_ | `details`, `joblist`, `error` |
| `/driverjobreq` | `driverJobDetailsActionForm` | `successupdate`, `assign_driver`, `joblist`, `error`, `success`, `failure` |

**Branch map inside `execute`:**

| Condition | Line(s) | Forward returned |
|-----------|---------|-----------------|
| `session` is `null` (implicit NPE if `getSession(false)` returns null) | 34–35 | _(NullPointerException uncaught)_ |
| `action == null \|\| action == ""` (reference equality — dead branch) | 41–43 | falls through to form fallback |
| `action == null` after form fallback | 45–47 | `"error"` |
| `action.equalsIgnoreCase("details")` | 49–55 | `"details"` |
| `action.equalsIgnoreCase("assign")` | 56–60 | `"assign_driver"` |
| `action.equalsIgnoreCase("assign_driver")` | 61–66 | `"successupdate"` |
| default (else) | 67–68 | `"error"` |

---

## Section 2: Coverage Confirmation in Test Directory

**Test files present (entire project):**

```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

**Grep result — pattern `DealerSessionReportAction|DriverJobDetailsAction` across all test sources:**

> No matches found.

**Conclusion:** Zero direct or indirect test coverage exists for either audited class. Neither class name appears in any test file. The four existing tests cover only `com.calibration` and `com.util` packages. No action class in the project has any test coverage.

---

## Section 3: Coverage Gap Findings

---

### A16-1 | Severity: CRITICAL | DealerSessionReportAction — Zero test coverage (class entirely untested)

`DealerSessionReportAction` has no unit tests, integration tests, or any indirect test coverage whatsoever. The entire `execute` method — the only entry point of the class — is untested. Every line, branch, and error path described below is uncovered.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`
**Method:** `execute` (lines 19–40)

---

### A16-2 | Severity: CRITICAL | DealerSessionReportAction — Null session causes unguarded NullPointerException

`request.getSession(false)` at line 23 can return `null` when no session exists (the `false` argument explicitly prevents session creation). The return value is assigned directly to `session` and immediately dereferenced at line 24 (`session.getAttribute("sessCompId")`). If a user's session has expired or was never established, this produces a `NullPointerException` rather than the guarded `RuntimeException` thrown for `sessCompId == null` at line 25.

The `global-exceptions` handler in `struts-config.xml` catches only `java.sql.SQLException`, `java.io.IOException`, and `javax.servlet.ServletException` — not `NullPointerException` or `RuntimeException`. An expired-session hit on `/dealerSessionReport` would result in an unhandled server error (HTTP 500) with a raw stack trace visible to the browser.

No test verifies behaviour when `getSession(false)` returns `null`.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, line 23–24

---

### A16-3 | Severity: CRITICAL | DealerSessionReportAction — sessCompId null check throws RuntimeException not caught by any handler

Line 25 throws `new RuntimeException("Must have valid user logged in here")` when `sessCompId` is `null`. `RuntimeException` is not listed in `global-exceptions` and there is no `"error"` or `"failure"` forward in the `/dealerSessionReport` action mapping. This exception propagates to the container and produces an unformatted HTTP 500 response.

No test verifies this guard path fires correctly, nor that an appropriate user-visible error page is shown.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, line 25

---

### A16-4 | Severity: CRITICAL | DealerSessionReportAction — Integer.parseInt(sessCompId) throws NumberFormatException on malformed session value

Line 30 calls `Integer.parseInt(sessCompId)` without any format validation. If the session attribute `sessCompId` is present but contains a non-numeric value (data corruption, session hijack with crafted cookie, etc.), a `NumberFormatException` is thrown. `NumberFormatException` extends `IllegalArgumentException` → `RuntimeException` and is not handled by `global-exceptions`. No test covers this path.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, line 30

---

### A16-5 | Severity: HIGH | DealerSessionReportAction — ClassCastException on form cast is untested

Line 32 casts `form` to `SessionReportSearchForm` without an `instanceof` check. If the Struts framework delivers an unexpected form type (misconfiguration, multi-mapped path), a `ClassCastException` is thrown and is unhandled. No test exercises this path.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, line 32

---

### A16-6 | Severity: HIGH | DealerSessionReportAction — UnitDAO.getAllUnitsByCompanyId failure path untested

`UnitDAO.getAllUnitsByCompanyId(companyId)` at line 34 declares `throws SQLException`. A database connectivity failure propagates upward through `execute`'s `throws Exception` declaration. The `global-exceptions` handler does list `java.sql.SQLException`, which would redirect to `errorDefinition`, but this path is never exercised in any test. Correct mapping of the exception to the error tile is unverified.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, line 34

---

### A16-7 | Severity: HIGH | DealerSessionReportAction — DriverDAO.getAllDriver failure path untested

`DriverDAO.getAllDriver(sessCompId, true)` at line 35 may throw exceptions. Same reasoning as A16-6 applies. No test covers database failure during driver list retrieval.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, line 35

---

### A16-8 | Severity: HIGH | DealerSessionReportAction — ReportService.getSessionReport failure path untested

`ReportService.getInstance().getSessionReport(...)` at line 37 wraps a `SQLException` into a `ReportServiceException` (which extends `RuntimeException`). `ReportServiceException` is not caught by `global-exceptions`. If session data retrieval fails, an unhandled `ReportServiceException` propagates to the container with no user-visible error forward. No test exercises this path.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, lines 37–38
**Related:** `src/main/java/com/service/ReportService.java`, lines 90–99

---

### A16-9 | Severity: HIGH | DealerSessionReportAction — Null session attributes for dateFormat/dateTimeFormat/timezone are silently passed downstream

Lines 27–29 retrieve `sessDateFormat`, `sessDateTimeFormat`, and `sessTimezone` from the session with no null guard. These values are passed directly to `getSessionReport(...)` and `getSessionReportFilter(dateFormat)`. If any of these session keys are absent, null is forwarded into `SessionFilterBean.builder()` and `SessionDAO.getSessions(...)`. The downstream impact (NullPointerException vs. silent empty-string treatment) depends on `DateUtil.stringToUTCDate` and `StringUtils.isBlank` — the latter handles null safely, but `DateUtil.stringToUTCDate(null, null)` is not audited here and the path is untested.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, lines 27–29, 37

---

### A16-10 | Severity: HIGH | DealerSessionReportAction — Happy-path (normal report render) untested

The primary success path — valid session with `sessCompId`, valid `dateFormat`/`dateTimeFormat`/`timezone`, successful DAO calls, `"report"` forward returned — is completely untested. No test verifies that `request` attributes `"vehicles"`, `"drivers"`, and `"sessionReport"` are set with the correct values, or that `mapping.findForward("report")` is invoked.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, lines 19–40

---

### A16-11 | Severity: CRITICAL | DriverJobDetailsAction — Zero test coverage (class entirely untested)

`DriverJobDetailsAction` has no unit tests, integration tests, or any indirect coverage. The class is reused across three Struts action paths (`/driverjob`, `/jobdetails`, `/driverjobreq`). The entirety of the `execute` method is uncovered.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`
**Method:** `execute` (lines 31–70)

---

### A16-12 | Severity: CRITICAL | DriverJobDetailsAction — Null session causes NullPointerException (same pattern as A16-2)

Line 34 calls `request.getSession(false)`, which can return `null`. The result is used in a ternary on line 35 (`session.getAttribute("sessCompId") == null ? "" : ...`) which will throw `NullPointerException` if `session` is `null`. This is unguarded, identical in nature to the defect in `DealerSessionReportAction`, and untested.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 34–35

---

### A16-13 | Severity: CRITICAL | DriverJobDetailsAction — Dead branch: reference equality check `action == ""` is always false

Lines 41–43:
```java
if (action == null || action == "") {
    action = form.getAction();
}
```
The left side of the `||` can never be true because `action` was assigned on line 36 via:
```java
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
```
The ternary ensures `action` is never null; it is either a non-null String from the request or the string literal `""`. The comparison `action == ""` is a reference-equality check, not `.equals()`. In Java, `request.getParameter(...)` returns a new `String` object; that object is not the same reference as the literal `""`. Therefore, `action == ""` is always `false` even when the parameter is the empty string.

**Consequences:**
1. `form.getAction()` is never called regardless of the parameter value — dead code.
2. The subsequent null check `if (action == null)` at line 45 is also always false (action was set non-null on line 36), so the `return mapping.findForward("error")` at line 46 is permanently unreachable dead code.
3. When `action` is an empty string from the request, execution falls through to the `else` branch at line 67 which returns `"error"` — the intended logic is circuitous and misleading.

No test covers this broken guard or verifies what happens when `action` is empty.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 41–47

---

### A16-14 | Severity: HIGH | DriverJobDetailsAction — "details" branch: getJobListByJobId with empty equipId/jobNo untested

Lines 49–55: when `action.equalsIgnoreCase("details")` is true, `jobsDAO.getJobListByJobId(equipId, jobNo)` is called. Both `equipId` and `jobNo` default to `""` (empty string) when the request parameters are absent. `getJobListByJobId` in `JobsDAO` builds a raw SQL string that concatenates these values directly (line 123 of `JobsDAO.java`):

```java
"... and j.unit_id = " + equipId + " and j.job_no = '" + jobNo + "'"
```

If `equipId` is `""`, the SQL becomes `... and j.unit_id =` which is a syntax error and will throw `SQLException`. If `jobNo` is `""`, the query executes but returns an empty result set. Neither the empty-parameter path nor the SQL error path is tested.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 49–55
**Related:** `src/main/java/com/dao/JobsDAO.java`, line 123

---

### A16-15 | Severity: CRITICAL | DriverJobDetailsAction / JobsDAO — SQL Injection via unparameterised equipId and jobNo

`JobsDAO.getJobListByJobId` (lines 108–170) constructs its SQL by direct string concatenation of `equipId` and `jobNo`:

```java
String sql = "select ... where j.unit_id = " + equipId
           + " and j.job_no = '" + jobNo + "' order by js.start_time";
```

Both values originate from `request.getParameter(...)` in `DriverJobDetailsAction` lines 37–38 with no sanitisation. An attacker who can reach `/jobdetails` (or `/driverjob`, `/driverjobreq`) with crafted `equipId` or `job_no` parameters can inject arbitrary SQL. This is an unauthenticated code path if session guard is absent (see A16-12). The absence of any test means this injection vector has never been exercised or detected.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 37–38, 49–52
**Related:** `src/main/java/com/dao/JobsDAO.java`, lines 123, 52 (same pattern in `getJobList`)

---

### A16-16 | Severity: HIGH | DriverJobDetailsAction — "assign" branch: driverDao.getAllDriver failure path untested

Lines 56–60: the `"assign"` branch calls `driverDao.getAllDriver(sessCompId, true)`. If the database is unreachable, the exception propagates through `execute`'s `throws Exception`. The `global-exceptions` handler would catch `SQLException`, but the forward mapping for `/driverjob` does not include a `"failure"` forward — only `"assign_driver"`, `"joblist"`, and `"error"`. Exception propagation to the container is unverified. No test exercises this path.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 56–60

---

### A16-17 | Severity: HIGH | DriverJobDetailsAction — "assign_driver" branch: System.out.println diagnostic left in production code

Line 62:
```java
System.out.println(form.getJobTitle());
```
This is production debug output writing to stdout (Tomcat's `catalina.out`). `form.getJobTitle()` will throw `NullPointerException` if `form` is null — which is possible when the action is invoked via `/driverjob` or `/jobdetails` which have no named form bean and Struts may pass a default empty `ActionForm`. No test verifies that `form` is non-null in the `"assign_driver"` path, and the debug print itself is a data exposure risk (job titles written to server logs).

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, line 62

---

### A16-18 | Severity: HIGH | DriverJobDetailsAction — "assign_driver" branch success path ("successupdate" forward) untested

Lines 61–66 handle `action.equalsIgnoreCase("assign_driver")`. This branch fetches all drivers and returns `mapping.findForward("successupdate")`. The forward `"successupdate"` is only declared in the `/driverjobreq` mapping; it does not exist in `/driverjob` or `/jobdetails`. If `"assign_driver"` is triggered via those paths, `mapping.findForward("successupdate")` returns `null`, and Struts will throw `NullPointerException` or deliver a blank response. No test covers any variant of this branch.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 61–66
**Related:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 463–475 (missing `successupdate` forward in `/driverjob` and `/jobdetails`)

---

### A16-19 | Severity: HIGH | DriverJobDetailsAction — "details" forward ("details") only declared in /jobdetails, not /driverjob or /driverjobreq

The `"details"` forward is declared only for `/jobdetails` (struts-config line 472). The `/driverjob` and `/driverjobreq` mappings have no `"details"` forward. If `action.equalsIgnoreCase("details")` is triggered via those paths, `mapping.findForward("details")` returns `null`, causing a `NullPointerException` or blank response. No test validates the forward-to-path mapping for any of the three Struts paths that share this action class.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, line 55
**Related:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 463–489

---

### A16-20 | Severity: MEDIUM | DriverJobDetailsAction — unitDao field (line 28) is instantiated but never used

`private UnitDAO unitDao = UnitDAO.getInstance();` at line 28 creates a `UnitDAO` singleton instance that is never referenced anywhere in `execute`. This is dead initialisation — the DAO instance is created eagerly on every action instantiation (Struts 1 creates a new action instance or reuses a single instance depending on configuration) and discarded. No test would catch a regression if `UnitDAO.getInstance()` were to fail during initialisation (e.g., due to missing configuration), because no test ever constructs `DriverJobDetailsAction`.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, line 28

---

### A16-21 | Severity: MEDIUM | DriverJobDetailsAction — sessCompId defaulting to empty string silently restricts driver list

Line 35 defaults `sessCompId` to `""` when the session attribute is absent or the session is null. The `driverDao.getAllDriver("", true)` call with an empty company ID may return all drivers across all companies (depending on DAO query logic), return zero results, or throw an exception. None of these outcomes are tested. The silent fallback to `""` masks the absence of a real session and may expose cross-tenant data.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 35, 57, 63

---

### A16-22 | Severity: MEDIUM | DealerSessionReportAction — ReportService singleton uses double-checked locking without volatile

`ReportService.getInstance()` (ReportService.java lines 20–27) uses double-checked locking with `synchronized` but the field `theInstance` is not declared `volatile`. Without `volatile`, in Java's memory model, a partially-constructed `ReportService` object could be observed by a second thread. This is a pre-Java-5 concurrency defect. No test exercises concurrent initialisation of `ReportService`.

**File:** `src/main/java/com/service/ReportService.java`, lines 18–27
_(Indirectly relevant to DealerSessionReportAction line 37)_

---

### A16-23 | Severity: LOW | DealerSessionReportAction — No test verifies "report" forward name string constant

The forward name `"report"` at line 39 must match the Struts configuration. The configuration at struts-config.xml line 580 confirms the match. However, since no test exists, a future rename of either the Java literal or the XML forward would go silently undetected until a runtime 404 or blank response.

**File:** `src/main/java/com/action/DealerSessionReportAction.java`, line 39

---

### A16-24 | Severity: LOW | DriverJobDetailsAction — Commented-out code left in production file

Lines 59, 65:
```java
//   request.setAttribute("driverList", form.getDriverList());
```
This commented-out code appears in two branches. It suggests incomplete feature implementation or a removed feature. Its presence creates ambiguity about intent and may indicate a missing `"driverList"` attribute that downstream JSPs or JavaScript expect. No test would detect a view-level breakage caused by the missing attribute.

**File:** `src/main/java/com/action/DriverJobDetailsAction.java`, lines 59, 65

---

### A16-25 | Severity: INFO | Both classes — No test infrastructure for Struts action testing exists in the project

The project contains no Struts mock testing framework setup (e.g., StrutsTestCase, MockStrutsTestCase, or Spring MVC Test equivalents). All four existing tests are pure unit tests of utility and calibration logic. There is no test infrastructure for testing `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `ActionMapping`, or `ActionForm` in isolation. Adding coverage to these action classes would require either introducing a mocking library (Mockito is already present in the calibration tests) or a Struts-specific test harness.

---

## Section 4: Coverage Gap Summary

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A16-1 | CRITICAL | DealerSessionReportAction | Class entirely untested — zero coverage |
| A16-2 | CRITICAL | DealerSessionReportAction | Null session (`getSession(false)`) causes unguarded NPE |
| A16-3 | CRITICAL | DealerSessionReportAction | Null `sessCompId` throws `RuntimeException` uncaught by any handler |
| A16-4 | CRITICAL | DealerSessionReportAction | `Integer.parseInt(sessCompId)` throws `NumberFormatException` on malformed input |
| A16-5 | HIGH | DealerSessionReportAction | `ClassCastException` on `ActionForm` cast untested |
| A16-6 | HIGH | DealerSessionReportAction | `UnitDAO.getAllUnitsByCompanyId` failure path untested |
| A16-7 | HIGH | DealerSessionReportAction | `DriverDAO.getAllDriver` failure path untested |
| A16-8 | HIGH | DealerSessionReportAction | `ReportService.getSessionReport` throws `ReportServiceException` uncaught by global handler |
| A16-9 | HIGH | DealerSessionReportAction | Null `dateFormat`/`dateTimeFormat`/`timezone` session attributes passed downstream without guard |
| A16-10 | HIGH | DealerSessionReportAction | Happy-path (successful report render) entirely untested |
| A16-11 | CRITICAL | DriverJobDetailsAction | Class entirely untested — zero coverage |
| A16-12 | CRITICAL | DriverJobDetailsAction | Null session causes NPE on line 35 |
| A16-13 | CRITICAL | DriverJobDetailsAction | Dead branch: `action == ""` reference equality always false; null guard at line 45 unreachable |
| A16-14 | HIGH | DriverJobDetailsAction | `"details"` branch: empty `equipId`/`jobNo` causes SQL syntax error in `getJobListByJobId` |
| A16-15 | CRITICAL | DriverJobDetailsAction / JobsDAO | SQL Injection via unparameterised `equipId` and `jobNo` concatenated into raw SQL |
| A16-16 | HIGH | DriverJobDetailsAction | `"assign"` branch DAO failure path untested; missing failure forward in `/driverjob` |
| A16-17 | HIGH | DriverJobDetailsAction | `System.out.println(form.getJobTitle())` in production code; potential NPE and data exposure |
| A16-18 | HIGH | DriverJobDetailsAction | `"assign_driver"` branch returns `"successupdate"` forward absent from `/driverjob` and `/jobdetails` |
| A16-19 | HIGH | DriverJobDetailsAction | `"details"` forward absent from `/driverjob` and `/driverjobreq` mappings |
| A16-20 | MEDIUM | DriverJobDetailsAction | `unitDao` field instantiated but never used in `execute` |
| A16-21 | MEDIUM | DriverJobDetailsAction | `sessCompId` defaults to `""` silently; potential cross-tenant data exposure |
| A16-22 | MEDIUM | DealerSessionReportAction | `ReportService` singleton uses double-checked locking without `volatile` field |
| A16-23 | LOW | DealerSessionReportAction | No test verifies `"report"` forward name matches Struts config |
| A16-24 | LOW | DriverJobDetailsAction | Commented-out `request.setAttribute("driverList", ...)` code in two branches |
| A16-25 | INFO | Both | No Struts action test infrastructure exists in the project |

---

## Section 5: Metrics

| Metric | DealerSessionReportAction | DriverJobDetailsAction |
|--------|--------------------------|----------------------|
| Total methods | 1 | 1 |
| Methods with any test coverage | 0 | 0 |
| Execution branches in `execute` | 3 (null check, DAO calls, forward) | 7 (null checks x2, dead branch, 3 action branches, default) |
| Branches with any test coverage | 0 | 0 |
| Distinct error paths identified | 7 | 10 |
| Error paths tested | 0 | 0 |
| Security findings | 0 | 2 (A16-13 logic error, A16-15 SQL injection) |

**Overall line coverage for audited classes: 0%**
**Overall branch coverage for audited classes: 0%**

---

*End of report — A16 — 2026-02-26-01*
