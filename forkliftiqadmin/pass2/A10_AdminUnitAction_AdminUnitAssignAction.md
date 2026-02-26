# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A10
**Files Audited:**
- `src/main/java/com/action/AdminUnitAction.java`
- `src/main/java/com/action/AdminUnitAssignAction.java`

---

## 1. Reading-Evidence Blocks

### 1.1 AdminUnitAction

**Class:** `com.action.AdminUnitAction extends org.apache.struts.action.Action`
**File:** `src/main/java/com/action/AdminUnitAction.java`

**Fields / Constants**

| Name | Type | Line | Notes |
|------|------|------|-------|
| `unitDAO` | `UnitDAO` | 25 | Singleton, eagerly initialised at field declaration |

**Methods**

| Method | Signature | Lines | Return |
|--------|-----------|-------|--------|
| `execute` | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 27–219 | `ActionForward` |

`execute` is the sole method. It reads request/session parameters and dispatches on the `action` parameter via a chain of `if / else if` blocks. Logical branches (each internally may have further sub-branches):

| Branch (action value) | Lines | Forwards returned |
|-----------------------|-------|-------------------|
| `"edit"` | 44–47 | `"unitedit"` |
| `"add"` | 48–56 | `"unitadd"` |
| `"delete"` | 57–61 | `"unitlist"` |
| `"job"` | 62–68 | `"joblist"` |
| `"add_job"` success | 69–81 | `"joblist"` |
| `"add_job"` failure | 82–84 | `"globalfailure"` |
| `"edit_job"` success | 85–98 | `"joblist"` |
| `"edit_job"` failure | 97–99 | `"globalfailure"` |
| `"service"` + equipId non-empty + arrServ non-empty | 100–127 | `"unitservice"` |
| `"service"` + equipId non-empty + arrServ empty | 128–147 | `"unitservice"` |
| `"service"` + equipId empty | 148–163 | `"unitservice"` |
| `"impact"` + equipId empty | 165–169 | `"unitimpact"` |
| `"impact"` + equipId non-empty | 170–183 | `"unitimpact"` |
| `"assignment"` | 184–187 | `"unitassignment"` |
| `"checklist"` + equipId non-empty + chkLst non-empty | 188–195 | `"unitchecklist"` |
| `"checklist"` + equipId non-empty + chkLst empty | 196–199 | `"unitchecklist"` |
| `"checklist"` + equipId empty | 200–205 | `"unitchecklist"` |
| default (list / search) — searchUnit empty | 208–218 | `"unitlist"` |
| default (list / search) — searchUnit non-empty | 208–218 | `"unitlist"` |

---

### 1.2 AdminUnitAssignAction

**Class:** `com.action.AdminUnitAssignAction extends com.action.PandoraAction`
**File:** `src/main/java/com/action/AdminUnitAssignAction.java`

**Fields / Constants**
None declared (fields are inherited from `PandoraAction`).

**Methods**

| Method | Signature | Lines | Return |
|--------|-----------|-------|--------|
| `execute` | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 20–63 | `ActionForward` |
| `writeJsonResponse` | `writeJsonResponse(HttpServletResponse, String)` | 65–68 | `void` (private) |

`execute` dispatches on the `action` parameter via a `switch`:

| Case | Lines | Outcome |
|------|-------|---------|
| `"validate"` — start null | 30–35 | writes JSON error, returns null |
| `"validate"` — start non-null, end non-null, start > end | 37–40 | writes JSON error, returns null |
| `"validate"` — overlapping | 44–47 | writes JSON error, returns null |
| `"validate"` — valid, no overlap | 49–50 | writes `"true"`, returns null |
| `"delete"` | 51–53 | calls `UnitDAO.deleteAssignment`, falls through to list |
| `"add"` | 54–56 | calls `UnitDAO.addAssignment`, falls through to list |
| default (unmatched action) | — | falls through to list |
| post-switch list | 59–62 | sets `arrAdminUnit`, forwards `"success"` |

**Supporting form:** `com.actionform.AdminUnitAssignForm` (Lombok `@Data @NoArgsConstructor`)
Fields: `id`, `unit_id`, `company_id`, `start`, `end` — all `String`.

---

## 2. Test-Coverage Confirmation

**Grep target:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`
**Pattern searched:** `AdminUnitAction|AdminUnitAssignAction`
**Result:** No matches found.

**Existing test files (all 4):**

| File | Subject |
|------|---------|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | `UnitCalibrationImpactFilter` |
| `com/calibration/UnitCalibrationTest.java` | `UnitCalibration` |
| `com/calibration/UnitCalibratorTest.java` | `UnitCalibrator` |
| `com/util/ImpactUtilTest.java` | `ImpactUtil` |

Neither `AdminUnitAction` nor `AdminUnitAssignAction` — nor their parent `PandoraAction` — appears in any test file. Coverage for all three classes is **0 %**.

---

## 3. Coverage Gaps and Findings

### 3.1 AdminUnitAction — Untested Branches and Defects

---

**A10-1 | Severity: CRITICAL | NullPointerException when session is null**

Line 30: `request.getSession(false)` returns `null` if no session exists. Every subsequent `session.getAttribute(...)` call (lines 31–32) and `session.setAttribute(...)` call (line 185–186) will throw `NullPointerException`. No null-check is performed on the session object anywhere in the method. This is an unhandled runtime error that crashes the request.

Affected lines: 30–32, 185–186.

---

**A10-2 | Severity: CRITICAL | NullPointerException on `Double.parseDouble` of `bean.getHrsTilNext()` when equipId is empty**

Lines 148–162 (the `"service"` branch, `equipId` is empty): A new `ServiceBean` is constructed (line 149). `ServiceBean.hrsTilNext` initialises to `null`. Line 150 calls `Double.parseDouble(bean.getHrsTilNext())` unconditionally without a null-check. This guarantees a `NullPointerException` at runtime when this code path is reached.

The analogous empty-list branch at lines 128–147 correctly guards with `if (bean.getHrsTilNext() != null)` (line 132). The empty-equipId branch does not apply the same guard, making this an inconsistency as well as a defect.

Affected lines: 149–150.

---

**A10-3 | Severity: CRITICAL | NumberFormatException on `Integer.parseInt(sessCompId)` when sessCompId is empty or non-numeric**

Line 40: `int companyId = Integer.parseInt(sessCompId)` is executed unconditionally at the top of every request path, before any action dispatch. If the session attribute `sessCompId` is absent (line 31 defaults it to `""`) or contains a non-integer string, `Integer.parseInt` throws `NumberFormatException`. No try-catch or pre-validation exists.

Affected line: 40.

---

**A10-4 | Severity: HIGH | NumberFormatException on `Integer.parseInt(equipId)` — action "add_job"**

Line 70: `int unitId = Integer.parseInt(equipId)` is called without first validating that `equipId` is a non-empty numeric string. If `equipId` is empty (its default, line 34) or contains non-numeric data, this throws `NumberFormatException`. No guard exists.

Affected line: 70.

---

**A10-5 | Severity: HIGH | NumberFormatException on `Integer.parseInt(job_id)` — action "edit_job"**

Line 86: `int jobId = Integer.parseInt(job_id)` is called without validating that `job_id` is a non-empty numeric string. `job_id` defaults to `""` (line 38). Empty or non-numeric input throws `NumberFormatException`.

Affected line: 86.

---

**A10-6 | Severity: HIGH | No null-check on `sessDateFormat` before it is passed to downstream methods**

Line 32: `dateFormat` is obtained by a direct cast of `session.getAttribute("sessDateFormat")` with no null-check. `dateFormat` is passed to `UnitDAO.getAssignments` (line 186). If the session attribute is absent, `dateFormat` is `null`. Whether downstream code handles a null format string is not tested and is a latent defect.

Affected lines: 32, 186.

---

**A10-7 | Severity: HIGH | "service" branch — empty equipId path parses `equipId` without guard**

Line 142: `bean.setUnitId(Integer.parseInt(equipId))` is inside the `arrServ.size() == 0` sub-branch where `equipId` has already been confirmed non-empty (outer if at line 101). This is not an immediate defect, but the logic relies on an implicit ordering guarantee that is fragile and untested.

Additionally, within the empty-list sub-branch (line 133), `bean.getHrsTilNext()` is null (new `ServiceBean()`), and the guard `if (bean.getHrsTilNext() != null)` prevents the parse. The variable `servRemain` therefore stays `0.0` and the immediately following `if (servRemain < 0)` block (lines 136–138) is permanently dead code. This dead code path has no test coverage.

Affected lines: 129–147.

---

**A10-8 | Severity: HIGH | `Long.valueOf(equipId)` — action "impact" — throws NumberFormatException for non-numeric equipId**

Line 173: `Long.valueOf(equipId)` is called with no pre-validation. `equipId` defaults to `""`. If `equipId` is empty or non-numeric, `Long.valueOf` throws `NumberFormatException`.

Affected line: 173.

---

**A10-9 | Severity: HIGH | All 19 action branches are completely untested**

The entire `execute` method — including every action branch (`edit`, `add`, `delete`, `job`, `add_job`, `edit_job`, `service`, `impact`, `assignment`, `checklist`, default) — has no corresponding unit or integration test. This means zero coverage of the primary controller entry point for admin unit management.

---

**A10-10 | Severity: MEDIUM | "add_job" success / failure paths both untested**

Lines 80–84: the conditional `if (jobsDAO.addJob(jobdetails))` produces two different forwards (`"joblist"` vs `"globalfailure"`). No test exercises either path or verifies that the correct forward is chosen based on DAO success/failure.

---

**A10-11 | Severity: MEDIUM | "edit_job" success / failure paths both untested**

Lines 95–99: same pattern as A10-10. Both the success and failure paths from `jobsDAO.editJob(jobdetails)` are untested.

---

**A10-12 | Severity: MEDIUM | Service status threshold boundary logic is untested**

Lines 113–119: the service status string is determined by comparing `servRemain` against thresholds of 5 and 25 hours. Three distinct branches exist. None of the boundary conditions (servRemain == 5.0, servRemain == 4.999, servRemain == 24.999, servRemain == 25.0, servRemain > 25.0, servRemain < 0) are tested.

---

**A10-13 | Severity: MEDIUM | "impact" branch — `sessDateTimeFormat` attribute may be null**

Line 172: `(String) session.getAttribute("sessDateTimeFormat")` is retrieved and assigned to `dateTimeFormat` without a null-check. It is passed to `DateUtil.sqlTimestampToString` (lines 177–178). `DateUtil.sqlTimestampToString` passes it directly to `new SimpleDateFormat(dateTimeFormat)`, which throws `NullPointerException` or `IllegalArgumentException` if `dateTimeFormat` is null.

Affected line: 172.

---

**A10-14 | Severity: MEDIUM | `UnitCalibrationGetterInDatabase` database failure is unhandled**

Line 173: `new UnitCalibrationGetterInDatabase().getUnitCalibration(Long.valueOf(equipId))` may throw checked or unchecked exceptions if the database is unavailable or if no calibration record exists for the given unit. The calling code neither catches exceptions nor validates that a calibration record was found before accessing its fields (lines 175–180).

---

**A10-15 | Severity: MEDIUM | Default branch — search behaviour not tested for either path**

Lines 209–213: two sub-branches exist (`searchUnit` empty: list all units; non-empty: search). Neither is covered by any test.

---

**A10-16 | Severity: LOW | `ManufactureDAO.getAllManufactures(sessCompId)` called unconditionally for all actions**

Line 42: `ManufactureDAO.getAllManufactures(sessCompId)` runs on every request, including actions like `"validate"` in `AdminUnitAssignAction` (though that class does not call this line). Within `AdminUnitAction`, this is always invoked even when the result is not used (e.g., the `"add_job"` and `"edit_job"` paths do not include `arrManufacturers` in their JSP forwards). This is an untested unnecessary DAO call.

---

**A10-17 | Severity: LOW | UnitDAO field is a mutable singleton reference — not validated in tests**

Line 25: `private UnitDAO unitDAO = UnitDAO.getInstance()` is initialised at field declaration. No test verifies that the singleton is correctly initialised or that substituting a mock DAO is possible. The lack of dependency injection prevents unit testing without reflection or a test framework supporting field injection.

---

### 3.2 AdminUnitAssignAction — Untested Branches and Defects

---

**A10-18 | Severity: CRITICAL | NullPointerException when session is null**

Line 21: `request.getSession(false)` may return `null`. Lines 22–23 call `session.getAttribute(...)` unconditionally. No null-check on `session`. This is the same structural defect as A10-1 and is untested.

Affected lines: 21–23.

---

**A10-19 | Severity: CRITICAL | NumberFormatException on `Integer.parseInt(sessCompId)` when sessCompId is empty or non-numeric**

Line 26: `int companyId = Integer.parseInt(sessCompId)` — identical vulnerability to A10-3. `sessCompId` is read from the session with no numeric validation. Throws `NumberFormatException` for absent or non-numeric values.

Affected line: 26.

---

**A10-20 | Severity: CRITICAL | ClassCastException if `actionForm` is not `AdminUnitAssignForm`**

Line 27: `AdminUnitAssignForm form = (AdminUnitAssignForm) actionForm` performs an unchecked cast. If Struts binds a different form type, this throws `ClassCastException`. No `instanceof` guard exists. Not tested.

Affected line: 27.

---

**A10-21 | Severity: HIGH | All execute branches completely untested**

The entire `execute` method — all `switch` cases (`validate`, `delete`, `add`) and the default fall-through — has no test coverage.

---

**A10-22 | Severity: HIGH | "validate" case — `form.getStart()` null not handled correctly**

Line 32: `DateUtil.stringToUTCDate(form.getStart(), dateFormat)` is called. `DateUtil.stringToUTCDate` returns `null` if `str_date == null` (line 56 of `DateUtil`). Line 33 checks `if (start == null)` and writes an error. However, if `dateFormat` (from session) is null, `DateUtil.stringToDate` constructs `new SimpleDateFormat(null)` which throws `NullPointerException` — this error path is unguarded and untested.

Affected lines: 22, 32–35.

---

**A10-23 | Severity: HIGH | "validate" case — `end` null is not treated as an error**

Line 37–40: if `form.getEnd()` parses to `null` (empty or null input), `end == null` and the start/end comparison block is skipped. The overlap check at line 44 is then called with `end == null`. Whether `UnitDAO.isAssignmentOverlapping` correctly handles a null end date (representing an open-ended assignment) is unverified by any test.

Affected lines: 37–47.

---

**A10-24 | Severity: HIGH | "validate" — `start.compareTo(end) > 0` does not catch equal dates**

Line 38: the validation rejects only `start > end`, not `start == end`. An assignment with identical start and end timestamps passes validation. Whether this is the intended business rule is not documented and not tested.

Affected lines: 38–40.

---

**A10-25 | Severity: HIGH | "add" case — no validation of form fields before DAO call**

Line 55: `UnitDAO.addAssignment(form.getCompany_id(), form.getUnit_id(), form.getStart(), form.getEnd(), dateFormat)` is called with raw, unvalidated strings from the form. If `company_id` or `unit_id` are null, empty, or non-numeric, the DAO or downstream SQL conversion may throw. No pre-validation or test coverage exists.

Affected line: 55.

---

**A10-26 | Severity: HIGH | "delete" case — `id` is not validated before DAO call**

Line 52: `UnitDAO.deleteAssignment(id)` is called where `id` defaults to `""` (line 25). Passing an empty string to the DAO may result in a SQL error or silent no-op. No validation or test coverage exists.

Affected lines: 25, 52.

---

**A10-27 | Severity: MEDIUM | `writeJsonResponse` — no Content-Type header set**

Lines 65–68: the private `writeJsonResponse` method writes a string directly to the response writer without setting `Content-Type: application/json`. This can cause browsers or API clients to mis-parse the response. No test verifies the response content type or body content.

Affected lines: 65–68.

---

**A10-28 | Severity: MEDIUM | Default switch case (unrecognised action) silently succeeds**

No `default` case is present in the switch statement (lines 29–57). An unrecognised `action` value silently falls through to the post-switch code, fetches the full unit list, and forwards to `"success"`. This may be unintentional and is completely untested.

Affected lines: 29–62.

---

**A10-29 | Severity: MEDIUM | `writeJsonResponse` called twice per validation response — potential double-flush**

Lines 66–67: `response.getWriter()` is called twice per invocation. `getWriter()` returns the same `PrintWriter` instance in a standard servlet container, so this is not a direct defect, but double-flushing the same writer object without checking `isCommitted()` can cause issues in some containers. Not tested.

Affected lines: 65–68.

---

**A10-30 | Severity: MEDIUM | `PandoraAction` utility methods completely untested**

`PandoraAction` (parent of `AdminUnitAssignAction`) provides `getLongRequestParam`, `getRequestParam` (Long overload), `getRequestParam` (String overload), `getSessionAttribute`, `getLongSessionAttribute`, and `getCompId`. None of these utility methods have test coverage. `AdminUnitAssignAction.execute` uses `getRequestParam` at lines 24–25; the behaviour for null parameters, "undefined" strings, and blank strings is untested.

Affected file: `src/main/java/com/action/PandoraAction.java`, lines 13–43.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A10-1 | CRITICAL | AdminUnitAction | NPE: `request.getSession(false)` result used without null-check |
| A10-2 | CRITICAL | AdminUnitAction | NPE: `Double.parseDouble(bean.getHrsTilNext())` when equipId empty and bean is freshly constructed (hrsTilNext is null) |
| A10-3 | CRITICAL | AdminUnitAction | NumberFormatException: `Integer.parseInt(sessCompId)` — no numeric validation |
| A10-4 | HIGH | AdminUnitAction | NumberFormatException: `Integer.parseInt(equipId)` in "add_job" branch |
| A10-5 | HIGH | AdminUnitAction | NumberFormatException: `Integer.parseInt(job_id)` in "edit_job" branch |
| A10-6 | HIGH | AdminUnitAction | Null `sessDateFormat` passed unchecked to downstream DAO call |
| A10-7 | HIGH | AdminUnitAction | Dead code path in service/empty-list branch; implicit ordering fragility |
| A10-8 | HIGH | AdminUnitAction | NumberFormatException: `Long.valueOf(equipId)` in "impact" branch |
| A10-9 | HIGH | AdminUnitAction | 0% coverage: all 19 action branches untested |
| A10-10 | MEDIUM | AdminUnitAction | "add_job" success/failure forward selection untested |
| A10-11 | MEDIUM | AdminUnitAction | "edit_job" success/failure forward selection untested |
| A10-12 | MEDIUM | AdminUnitAction | Service status threshold boundary conditions untested |
| A10-13 | MEDIUM | AdminUnitAction | Null `sessDateTimeFormat` may cause NPE in "impact" branch |
| A10-14 | MEDIUM | AdminUnitAction | Database failure from `UnitCalibrationGetterInDatabase` unhandled |
| A10-15 | MEDIUM | AdminUnitAction | Default branch search sub-paths (empty vs non-empty searchUnit) untested |
| A10-16 | LOW | AdminUnitAction | Unconditional `ManufactureDAO` call on every request regardless of action |
| A10-17 | LOW | AdminUnitAction | Singleton `UnitDAO` field precludes unit testing without reflection |
| A10-18 | CRITICAL | AdminUnitAssignAction | NPE: `request.getSession(false)` result used without null-check |
| A10-19 | CRITICAL | AdminUnitAssignAction | NumberFormatException: `Integer.parseInt(sessCompId)` — no numeric validation |
| A10-20 | CRITICAL | AdminUnitAssignAction | ClassCastException: unchecked cast of `actionForm` to `AdminUnitAssignForm` |
| A10-21 | HIGH | AdminUnitAssignAction | 0% coverage: all switch cases and default fall-through untested |
| A10-22 | HIGH | AdminUnitAssignAction | Null `dateFormat` causes NPE inside `DateUtil.stringToUTCDate` |
| A10-23 | HIGH | AdminUnitAssignAction | Null `end` passed to overlap check — open-ended assignment behaviour untested |
| A10-24 | HIGH | AdminUnitAssignAction | Equal start/end dates pass validation — business rule undocumented and untested |
| A10-25 | HIGH | AdminUnitAssignAction | "add" case: unvalidated form fields passed directly to DAO |
| A10-26 | HIGH | AdminUnitAssignAction | "delete" case: empty `id` passed to DAO without validation |
| A10-27 | MEDIUM | AdminUnitAssignAction | `writeJsonResponse` does not set `Content-Type: application/json` |
| A10-28 | MEDIUM | AdminUnitAssignAction | Unrecognised action silently falls through to success path |
| A10-29 | MEDIUM | AdminUnitAssignAction | Double call to `response.getWriter()` per write — potential double-flush |
| A10-30 | MEDIUM | PandoraAction | All utility methods in parent class untested |

**Total findings: 30**
**CRITICAL: 6 | HIGH: 12 | MEDIUM: 9 | LOW: 3**
