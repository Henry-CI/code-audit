# Pass 2 Test Coverage Audit — UnitDAO
**Audit run:** 2026-02-26-01
**Agent ID:** A81
**Source file:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/dao/UnitDAO.java`
**Test directory:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

---

## Reading Evidence

### Class Name
- `UnitDAO` (line 22) — singleton, package `com.dao`

### Fields (static constants and instance fields)

| Line | Field Name | Type |
|------|-----------|------|
| 23 | `log` | `static Logger` |
| 24 | `theInstance` | `static UnitDAO` |
| 48–50 | `INSERT_UNIT_ASSIGNMENT` | `static final String` |
| 78 | `DELETE_UNIT_ASSIGNMENT` | `static final String` |
| 91–96 | `QUERY_ASSIGN_DATE_OVERLAP_CHECK` | `static final String` |
| 116–117 | `QUERY_COUNT_UNIT_BY_NAME` | `static final String` |
| 146–147 | `QUERY_COUNT_UNIT_BY_SERIAL_NO` | `static final String` |
| 179–180 | `QUERY_COUNT_UNIT_BY_MAC_ADDRESS` | `static final String` |
| 438–440 | `INSERT_UNIT_INFO` | `static final String` |
| 467–470 | `UPDATE_UNIT` | `static final String` |
| 513–515 | `UPDATE_UNIT_ACCESS` | `static final String` |
| 817–820 | `QUERY_IMPACT_BY_UNIT` | `static final String` |

### Methods

| Line | Method Name | Visibility | Static? |
|------|------------|-----------|---------|
| 26 | `getInstance()` | public | static |
| 37 | `UnitDAO()` (constructor) | private | — |
| 40 | `getAssignments(String, String, String)` | public | static |
| 52 | `addAssignment(String, String, String, String, String)` | public | static |
| 80 | `deleteAssignment(String)` | public | static |
| 98 | `isAssignmentOverlapping(String, Date, Date)` | public | static |
| 119 | `checkUnitByNm(String, String, String, boolean)` | public | instance |
| 149 | `checkUnitBySerial(String, String, boolean, String)` | public | instance |
| 182 | `checkUnitByMacAddr(String, String)` | public | instance |
| 199 | `getUnitBySerial(String, Boolean)` | public | instance |
| 242 | `getAllUnitsByCompanyId(int)` | public | static |
| 252 | `getUnitMaxId()` | public | instance |
| 288 | `getUnitById(String)` | public | static |
| 293 | `getUnitNameByComp(String, Boolean)` | public | instance |
| 340 | `delUnitById(String)` | public | instance |
| 364 | `getAllUnitType()` | public | static |
| 401 | `getAllUnitFuelType()` | public | instance |
| 442 | `saveUnitInfo(UnitBean)` | public | instance |
| 472 | `updateUnitInfo(UnitBean)` | private | instance |
| 517 | `saveUnitAccessInfo(UnitBean)` | public | static |
| 530 | `getTotalUnitByID(String, Boolean)` | public | static |
| 573 | `getAllUnitAttachment()` | public | instance |
| 610 | `getType(String)` | public | instance |
| 653 | `getPower(String, String)` | public | instance |
| 699 | `saveService(ServiceBean)` | public | instance |
| 761 | `getServiceByUnitId(String)` | public | instance |
| 822 | `getImpactByUnitId(Long)` | public | instance |
| 833 | `getChecklistSettings(String)` | public | instance |
| 875 | `resetCalibration(int)` | public | instance |
| 879 | `updateChecklistSettings(ChecklistBean)` | public | instance |
| 909 | `getSessionHoursCalilbration(String, String)` | public | instance |
| 958 | `getAllUnitSearch(String, Boolean, String)` | public | instance |

---

## Test Coverage Search Results

Grep for `UnitDAO` across all files under
`/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`:

**Result: No matches found.**

Existing test files in the test directory:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these files reference `UnitDAO` in any capacity. There is **zero test coverage** for this class.

---

## Findings

### Complete Absence of Tests

A81-1 | Severity: CRITICAL | The class `UnitDAO` has no test class and no test methods whatsoever. All 31 public/private methods, every SQL branch, and every error path are entirely untested.

---

### Singleton / Lifecycle

A81-2 | Severity: HIGH | `getInstance()` (line 26) uses a double-checked locking pattern but the `theInstance` field (line 24) is not declared `volatile`. Under the Java Memory Model this can cause a partially-constructed object to be returned by a second thread. No test verifies thread-safe singleton construction or that repeated calls return the same instance.

A81-3 | Severity: LOW | There is no test verifying that the private constructor (line 37) prevents direct instantiation (e.g., via reflection).

---

### `getAssignments` (line 40)

A81-4 | Severity: HIGH | No test covers the happy path (valid companyId and equipId producing a non-empty assignment list).

A81-5 | Severity: HIGH | No test covers the case where `AssignmentByCompanyAndUnitIdQuery.query()` throws `SQLException`.

A81-6 | Severity: MEDIUM | No test covers non-numeric `sessCompId` or `equipId` strings (will throw `NumberFormatException` before any SQL is issued — unhandled and undeclared).

---

### `addAssignment` (line 52)

A81-7 | Severity: HIGH | No test covers the happy path: all four parameters non-null and non-empty.

A81-8 | Severity: HIGH | No test verifies the `startDate == null || startDate.equals("")` branch (line 61–63) that sets `Types.DATE` null on parameter 3.

A81-9 | Severity: HIGH | No test verifies the `endDate == null || endDate.equals("")` branch (line 65–68) that sets `Types.DATE` null on parameter 4.

A81-10 | Severity: HIGH | No test verifies that a `SQLException` from `DBUtil.updateObject` is caught, logged, and re-thrown.

A81-11 | Severity: MEDIUM | No test covers non-numeric `unitId` or `subCompanyId` triggering `NumberFormatException` (unhandled, not declared).

---

### `deleteAssignment` (line 80)

A81-12 | Severity: HIGH | No test covers the happy path (valid numeric id).

A81-13 | Severity: HIGH | No test verifies `SQLException` propagation after logging.

A81-14 | Severity: MEDIUM | No test covers a non-numeric `id` string causing `NumberFormatException`.

---

### `isAssignmentOverlapping` (line 98)

A81-15 | Severity: HIGH | No test covers the case where `endDate` is non-null (parameters 2 and 3 set to actual dates).

A81-16 | Severity: HIGH | No test covers the case where `endDate` is null (parameters 2 and 3 set to `Types.DATE` null).

A81-17 | Severity: HIGH | No test covers the case where `startDate` is null — `Objects.requireNonNull` (line 100) throws `NullPointerException` at runtime; this exception is not declared and not caught.

A81-18 | Severity: HIGH | No test verifies that a count > 0 returns `true` and a count of 0 returns `false`.

A81-19 | Severity: MEDIUM | The `orElse(0)` fallback (line 111) when the `Optional` is empty is never tested.

---

### `checkUnitByNm` (line 119)

A81-20 | Severity: HIGH | No test covers the branch where `id != null` (appends `" and id != ?"` and binds the third parameter).

A81-21 | Severity: HIGH | No test covers the branch where `id == null`.

A81-22 | Severity: HIGH | No test covers the branch where `activeStatus == true` (appends `" and active = true"`).

A81-23 | Severity: HIGH | No test covers the branch where `activeStatus == false`.

A81-24 | Severity: MEDIUM | The `assert compId != null` and `assert StringUtils.isNotBlank(name)` guards (lines 122–123) are never exercised; assertions are disabled by default in production JVMs.

A81-25 | Severity: MEDIUM | No test verifies that a count > 0 returns `true` and a count of 0 returns `false`.

---

### `checkUnitBySerial` (line 149)

A81-26 | Severity: HIGH | No test covers the 2^3 = 8 combinations of `id`/`activeStatus`/`compId` that control dynamic SQL construction (lines 153–163).

A81-27 | Severity: MEDIUM | No test covers `serialNo` being blank (assert guard at line 150, disabled by default).

A81-28 | Severity: MEDIUM | No test verifies count-to-boolean mapping.

---

### `checkUnitByMacAddr` (line 182)

A81-29 | Severity: HIGH | No test covers the branch where `id != null` vs `id == null`.

A81-30 | Severity: MEDIUM | `macAddr` being null is never tested; `stmt.setString` with a null value may behave differently across JDBC drivers.

---

### `getUnitBySerial` (line 199)

A81-31 | Severity: HIGH | No test covers the happy path where the ResultSet contains exactly one row.

A81-32 | Severity: HIGH | No test covers the branch where `serial_no` is empty string — the method short-circuits and returns an empty list (line 211).

A81-33 | Severity: HIGH | No test covers the case where the query returns zero rows (empty ResultSet after the `if (rs.next())` check).

A81-34 | Severity: HIGH | No test verifies that a caught `Exception` is wrapped in `SQLException` and re-thrown.

A81-35 | Severity: CRITICAL | This method builds SQL by direct string concatenation of `serial_no` (line 212): `"select id,comp_id from unit where serial_no = '" + serial_no + "'"`. This is a SQL injection vulnerability. No test (positive or negative) exercises any input sanitization or demonstrates safe handling of adversarial input.

A81-36 | Severity: MEDIUM | The `activeStatus` toggle branch (lines 213–215) has no test for both `true` and `false` values.

---

### `getAllUnitsByCompanyId` (line 242)

A81-37 | Severity: HIGH | No test covers the happy path or an empty result from `UnitsByCompanyIdQuery`.

A81-38 | Severity: HIGH | No test covers `SQLException` propagation.

---

### `getUnitMaxId` (line 252)

A81-39 | Severity: HIGH | No test covers the happy path where `max(id)` returns a non-null value and `count` is set to `rs.getInt(1) + 1`.

A81-40 | Severity: HIGH | No test covers the edge case where the `unit` table is empty — `SELECT max(id)` returns a NULL, and `rs.getInt(1)` returns `0`; the method would return `1`. This behaviour is undocumented and untested.

A81-41 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

---

### `getUnitById` (line 288)

A81-42 | Severity: HIGH | No test covers the happy path or empty result.

A81-43 | Severity: MEDIUM | No test covers a non-numeric `id` string causing `NumberFormatException` (unhandled, not declared).

---

### `getUnitNameByComp` (line 293)

A81-44 | Severity: HIGH | No test covers the dealer-role branch (line 307–309) that expands `compLst` to a sub-company list.

A81-45 | Severity: HIGH | No test covers the non-dealer branch where `compLst` equals the original `compId`.

A81-46 | Severity: HIGH | No test covers the `activeStatus == true` SQL filter branch (line 312–314).

A81-47 | Severity: HIGH | No test covers the case where the ResultSet is empty (returns empty list).

A81-48 | Severity: CRITICAL | SQL is constructed via string concatenation of `compLst` (line 311): `"select id,name from unit where comp_id in (" + compLst + ")"`. If `compLst` originates from user input, this is a SQL injection vector. No test exercises this path with adversarial input.

---

### `delUnitById` (line 340)

A81-49 | Severity: HIGH | No test verifies the soft-delete (`update unit set active = false where id=<id>`) executes.

A81-50 | Severity: CRITICAL | SQL is constructed via string concatenation of `id` (line 349): `"update unit set active = false where id=" + id`. No validation or sanitization is applied. No test exercises this with adversarial input.

A81-51 | Severity: HIGH | No test verifies that a caught `Exception` is re-thrown as `SQLException`.

---

### `getAllUnitType` (line 364)

A81-52 | Severity: HIGH | No test covers a non-empty result (list of `UnitTypeBean`).

A81-53 | Severity: HIGH | No test covers an empty result set.

A81-54 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

---

### `getAllUnitFuelType` (line 401)

A81-55 | Severity: HIGH | No test covers a non-empty result (list of `UnitFuelTypeBean`).

A81-56 | Severity: HIGH | No test covers an empty result set.

A81-57 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

---

### `saveUnitInfo` (line 442)

A81-58 | Severity: HIGH | No test covers the insert branch (`unitbean.getId() == null`, lines 446–461).

A81-59 | Severity: HIGH | No test covers the update branch (`unitbean.getId() != null`, delegates to `updateUnitInfo`, line 463).

A81-60 | Severity: HIGH | No test verifies that `rowUpdate > 0` returns `true` and `rowUpdate == 0` returns `false`.

A81-61 | Severity: MEDIUM | No test covers a null `UnitBean` argument (will throw `NullPointerException` at line 445).

---

### `updateUnitInfo` (line 472) — private

A81-62 | Severity: HIGH | No test (even indirect via `saveUnitInfo`) verifies the SQL update executes and returns `true`.

A81-63 | Severity: HIGH | No test covers the branch where `ps.executeUpdate() != 1` (line 497), which returns `false`.

A81-64 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

A81-65 | Severity: MEDIUM | The `assert unitbean != null` guard (line 473) is disabled by default; never exercised.

A81-66 | Severity: MEDIUM | `finally` block only closes the PreparedStatement if it is non-null, but the `Connection` (`conn`) is only closed inside that same `if` block (line 507). If `conn.prepareStatement` throws before `ps` is assigned, the connection leaks. No test exercises this resource-leak path.

---

### `saveUnitAccessInfo` (line 517)

A81-67 | Severity: HIGH | No test covers the happy path for any combination of `accessible`, `access_type`, `access_id`, `keypad_reader`, and `facility_code`.

A81-68 | Severity: HIGH | No test covers `keypad_reader == null` vs non-null (the ternary on line 524).

A81-69 | Severity: HIGH | No test covers `SQLException` propagation (method declares `throws Exception` but has no try/catch; any SQL error propagates uncaught).

A81-70 | Severity: MEDIUM | The `assert unitbean != null` guard (line 518) is disabled by default; never exercised.

---

### `getTotalUnitByID` (line 530)

A81-71 | Severity: HIGH | No test covers the dealer-role expansion path (line 544–546).

A81-72 | Severity: HIGH | No test covers the `activeStatus == true` SQL filter branch (line 549–551).

A81-73 | Severity: HIGH | No test covers the case where `rs.next()` returns false (empty table) — method returns empty string `""` which callers may parse as an integer, causing `NumberFormatException`.

A81-74 | Severity: CRITICAL | SQL constructed by string concatenation of `compLst` (line 548): `"select count(id) from unit where comp_id in (" + compLst + ")"`. SQL injection risk identical to `getUnitNameByComp`. No test covers adversarial input.

---

### `getAllUnitAttachment` (line 573)

A81-75 | Severity: HIGH | No test covers a non-empty result or empty result.

A81-76 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

---

### `getType` (line 610)

A81-77 | Severity: HIGH | No test covers the `manu_id.equalsIgnoreCase("")` branch that substitutes `"0"` (line 622–624).

A81-78 | Severity: HIGH | No test covers a non-empty or empty result set.

A81-79 | Severity: CRITICAL | SQL uses string concatenation of `manu_id` (line 627): `" where manu_id = " + manu_id`. SQL injection risk. No test exercises adversarial input.

A81-80 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

---

### `getPower` (line 653)

A81-81 | Severity: HIGH | No test covers the branch where `type_id` is non-empty (line 669–671), which appends an additional `and type_id=` filter.

A81-82 | Severity: HIGH | No test covers the branch where `type_id` is empty.

A81-83 | Severity: CRITICAL | SQL uses string concatenation of both `manu_id` (line 667) and `type_id` (line 670). SQL injection risk. No test covers adversarial input.

A81-84 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

---

### `saveService` (line 699)

A81-85 | Severity: HIGH | No test covers the insert path (count <= 0, lines 720–731).

A81-86 | Severity: HIGH | No test covers the update path (count > 0, lines 733–744).

A81-87 | Severity: HIGH | No test verifies that the count query correctly determines insert vs update by checking `rset.next()`.

A81-88 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

A81-89 | Severity: MEDIUM | The same `PreparedStatement` variable `ps` is reused for two different SQL statements (lines 712 and 720/733). If closing the first statement before reassigning fails, the second statement may leave a resource unclosed. No test exercises the resource cleanup path.

---

### `getServiceByUnitId` (line 761)

A81-90 | Severity: HIGH | No test covers the happy path where rows are returned.

A81-91 | Severity: HIGH | No test covers the `service_type` value `"setDur"` being remapped to `"setIntval"` (lines 789–791).

A81-92 | Severity: HIGH | No test covers an empty result set (returns empty list).

A81-93 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

A81-94 | Severity: MEDIUM | No test covers a non-numeric `unitId` string causing `NumberFormatException` at line 776.

---

### `getImpactByUnitId` (line 822)

A81-95 | Severity: HIGH | No test covers the happy path (non-empty result list with all ImpactBean fields mapped).

A81-96 | Severity: HIGH | No test covers an empty result set (no `unit_service` row joined).

A81-97 | Severity: HIGH | No test covers `Exception`/`SQLException` propagation.

---

### `getChecklistSettings` (line 833)

A81-98 | Severity: HIGH | No test covers the happy path where `driver_based` is `true` vs `false`.

A81-99 | Severity: HIGH | No test covers an empty result set (no matching unit id).

A81-100 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

A81-101 | Severity: MEDIUM | No test covers a non-numeric `unitId` string causing `NumberFormatException` at line 850.

---

### `resetCalibration` (line 875)

A81-102 | Severity: HIGH | No test verifies that `UnitCalibrationStarterInDatabase.startCalibration(equipId)` is invoked with the correct argument.

A81-103 | Severity: HIGH | No test covers `SQLException` propagation from the delegate call.

---

### `updateChecklistSettings` (line 879)

A81-104 | Severity: HIGH | No test verifies the SQL update executes with the correct `driver_based` and `equipId` values.

A81-105 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

A81-106 | Severity: MEDIUM | No test covers a `ChecklistBean` with a zero or negative `equipId`.

---

### `getSessionHoursCalilbration` (line 909)

A81-107 | Severity: HIGH | No test covers the happy path where sessions are returned and hours are summed.

A81-108 | Severity: HIGH | No test covers the empty result set (method returns `0.0`).

A81-109 | Severity: HIGH | No test covers the case where `DateUtil.parseDateTime` returns null or throws for a malformed timestamp string — would throw `NullPointerException` at `parseStart.getTime()` (line 934).

A81-110 | Severity: HIGH | No test covers `Exception` wrapping in `SQLException`.

A81-111 | Severity: MEDIUM | No test covers a non-numeric `equipId` string causing `NumberFormatException` at line 928.

A81-112 | Severity: LOW | The method name `getSessionHoursCalilbration` contains a typo (`Calilbration` instead of `Calibration`). No test documents or guards against this naming inconsistency.

---

### `getAllUnitSearch` (line 958)

A81-113 | Severity: HIGH | No test covers the happy path with matching units returned.

A81-114 | Severity: HIGH | No test covers the `activeStatus == true` branch (line 962) that calls `activeUnitsOnly()`.

A81-115 | Severity: HIGH | No test covers the `searchUnit.isEmpty()` short-circuit that skips `query.containing(searchUnit)` (line 963).

A81-116 | Severity: HIGH | No test covers an empty `searchUnit` returning all units vs a non-empty `searchUnit` filtering results.

A81-117 | Severity: HIGH | No test covers `Exception`/`SQLException` propagation from `query.query()`.

A81-118 | Severity: MEDIUM | No test covers a non-numeric `compId` causing `NumberFormatException` at `Integer.valueOf(compId)` (line 961).

---

### Cross-Cutting / Structural

A81-119 | Severity: CRITICAL | Multiple methods construct SQL strings via direct concatenation of unsanitized caller-supplied values: `getUnitBySerial` (line 212), `getUnitNameByComp` (line 311), `delUnitById` (line 349), `getTotalUnitByID` (line 548), `getType` (line 627), and `getPower` (lines 667, 670). No tests exercise these paths with adversarial input to document or guard against SQL injection.

A81-120 | Severity: HIGH | None of the raw-JDBC methods (`getUnitBySerial`, `getUnitMaxId`, `getUnitNameByComp`, `delUnitById`, `getAllUnitType`, `getAllUnitFuelType`, `getAllUnitAttachment`, `getType`, `getPower`, `saveService`, `getServiceByUnitId`, `getChecklistSettings`, `updateChecklistSettings`, `getSessionHoursCalilbration`) have tests that verify JDBC resource cleanup (Connection, Statement, ResultSet) occurs correctly in both success and exception scenarios.

A81-121 | Severity: HIGH | No negative tests exist for any method to verify that all declared `throws SQLException` / `throws Exception` signatures actually propagate exceptions as documented.

A81-122 | Severity: MEDIUM | Several methods accept `String` arguments that are parsed to `int`/`long`/`double` without prior validation (e.g., `getAssignments`, `addAssignment`, `deleteAssignment`, `getUnitById`, `getUnitNameByComp`, `delUnitById`, `getServiceByUnitId`, `getChecklistSettings`, `getSessionHoursCalilbration`, `getAllUnitSearch`). No test exercises the `NumberFormatException` path for any of them.

A81-123 | Severity: LOW | The log message in `getUnitMaxId` (line 256) and several other methods incorrectly reads `"Inside LoginDAO Method : ..."` instead of `"Inside UnitDAO Method : ..."`. No test verifies correct log output.
