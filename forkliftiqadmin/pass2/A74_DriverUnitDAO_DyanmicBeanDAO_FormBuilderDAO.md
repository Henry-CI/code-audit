# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A74
**Files Audited:**
1. `src/main/java/com/dao/DriverUnitDAO.java`
2. `src/main/java/com/dao/DyanmicBeanDAO.java`
3. `src/main/java/com/dao/FormBuilderDAO.java`

---

## Test Directory Search Results

Grep of `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/` for each class name:

| Class Name | Matches Found |
|---|---|
| `DriverUnitDAO` | **0** |
| `DyanmicBeanDAO` | **0** |
| `FormBuilderDAO` | **0** |

Existing test files in the test directory (for context on project testing patterns):
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of the three audited DAO classes have any test coverage whatsoever.

---

## Reading Evidence

### 1. DriverUnitDAO.java

**Class name:** `DriverUnitDAO`
**File:** `src/main/java/com/dao/DriverUnitDAO.java`

**Fields:**

| Field Name | Line | Notes |
|---|---|---|
| `QUERY_DRIVER_UNITS_BY_DRIVER_ID` | 12 | `private static final String` – SQL constant |
| `QUERY_UNITS_ASSIGNED` | 13 | `private static final String` – SQL constant with `FOR UPDATE` lock |
| `UNASSIGN_DRIVER_UNIT` | 14 | `private static final String` – SQL constant |
| `ASSIGN_DRIVER_UNIT` | 15 | `private static final String` – SQL constant |
| `instance` | 17 | `private static DriverUnitDAO` – singleton holder |

**Methods:**

| Method Name | Line | Signature |
|---|---|---|
| `getInstance` | 19 | `public static DriverUnitDAO getInstance()` |
| `DriverUnitDAO` (constructor) | 30 | `private DriverUnitDAO()` |
| `getDriverUnitsByCompAndDriver` | 33 | `public static List<DriverUnitBean> getDriverUnitsByCompAndDriver(Long compId, Long driverId) throws SQLException` |
| `saveDriverVehicle` | 49 | `public void saveDriverVehicle(DriverVehicleBean driverVehicle) throws SQLException` |

---

### 2. DyanmicBeanDAO.java

**Class name:** `DyanmicBeanDAO`
**File:** `src/main/java/com/dao/DyanmicBeanDAO.java`

**Fields:**

| Field Name | Line | Notes |
|---|---|---|
| `log` | 18 | `private static Logger` – Log4j logger |

**Methods:**

| Method Name | Line | Signature |
|---|---|---|
| `getDynamicBean` | 20 | `public ArrayList<DynamicBean> getDynamicBean() throws Exception` |

---

### 3. FormBuilderDAO.java

**Class name:** `FormBuilderDAO`
**File:** `src/main/java/com/dao/FormBuilderDAO.java`

**Fields:**

| Field Name | Line | Notes |
|---|---|---|
| `log` | 22 | `private static Logger` – Log4j logger |

**Methods:**

| Method Name | Line | Signature |
|---|---|---|
| `getLib` | 24 | `public ArrayList<FormLibraryBean> getLib(String questionId, String type) throws SQLException` |
| `saveLib` | 63 | `public boolean saveLib(String entityId, String questionId, String type, FormBuilderBean formBuilderBean) throws SQLException` |
| `saveAnswerForm` | 138 | `public boolean saveAnswerForm(String questionId, String type, FormBuilderBean formBuilderBean) throws SQLException` |

---

## Findings

### DriverUnitDAO.java

**A74-1 | Severity: CRITICAL | DriverUnitDAO – zero test coverage: no test class exists**
The class `DriverUnitDAO` is completely untested. No test file references this class in the test source tree. All methods, fields, and behavioral branches are unexercised by automated tests.

**A74-2 | Severity: CRITICAL | DriverUnitDAO.getInstance() – singleton double-checked locking is untested**
`getInstance()` (line 19) implements a double-checked locking singleton pattern. There are no tests verifying: (a) that the first call returns a non-null instance, (b) that repeated calls return the same instance, or (c) thread-safety behavior under concurrent access.

**A74-3 | Severity: CRITICAL | DriverUnitDAO.getDriverUnitsByCompAndDriver() – happy-path entirely untested**
The static method at line 33 queries the `v_driver_units` view and maps all result columns into a `DriverUnitBean`. No test verifies the correct mapping of `comp_id`, `driver_id`, `unit_id`, `name`, `location`, `department`, `assigned`, `hours`, and `trained` columns.

**A74-4 | Severity: HIGH | DriverUnitDAO.getDriverUnitsByCompAndDriver() – null parameter behavior untested**
There is no null-guard on `compId` or `driverId` before they are passed to `stmt.setLong()`. No test covers what happens when either parameter is `null` (a `NullPointerException` would be unboxed at runtime). The result of passing `null` is not verified.

**A74-5 | Severity: HIGH | DriverUnitDAO.getDriverUnitsByCompAndDriver() – empty result set untested**
No test verifies that when the query returns zero rows the method returns an empty `List` rather than `null` or throwing an exception.

**A74-6 | Severity: CRITICAL | DriverUnitDAO.saveDriverVehicle() – happy-path entirely untested**
The method at line 49 performs a transactional read-modify-write sequence: it locks assigned unit rows with `FOR UPDATE`, computes set-differences, issues DELETE and INSERT statements, and commits. None of this logic is covered by any test.

**A74-7 | Severity: HIGH | DriverUnitDAO.saveDriverVehicle() – unassign branch untested**
The stream filter at line 59 selects units that are not assigned in the bean but are present in the database, then deletes them. No test exercises this path or confirms that the correct `unit_id` values are deleted.

**A74-8 | Severity: HIGH | DriverUnitDAO.saveDriverVehicle() – assign branch untested**
The stream filter at line 75 selects units that are assigned in the bean but absent from the database, then inserts them. No test exercises this path or confirms that the correct `unit_id` values are inserted.

**A74-9 | Severity: HIGH | DriverUnitDAO.saveDriverVehicle() – no-op case (empty driverUnits list) untested**
When `driverVehicle.getDriverUnits()` returns an empty list both streams produce no side-effects and `commit()` is still called. No test verifies this degenerate case.

**A74-10 | Severity: HIGH | DriverUnitDAO.saveDriverVehicle() – SQLException on DELETE triggers rollback then RuntimeException; rollback swallows inner SQLException**
Lines 65-71: a `SQLException` during DELETE causes a `connection.rollback()` call inside a nested try/catch that silently discards any rollback failure. No test verifies that (a) `rollback()` is called on a DELETE failure, (b) the outer `RuntimeException` is properly propagated, or (c) a rollback `SQLException` is silently swallowed.

**A74-11 | Severity: HIGH | DriverUnitDAO.saveDriverVehicle() – SQLException on INSERT triggers rollback then RuntimeException; rollback swallows inner SQLException**
Lines 81-88: identical silent-swallow pattern as A74-10 but for the INSERT path. No test covers this branch.

**A74-12 | Severity: HIGH | DriverUnitDAO.saveDriverVehicle() – Java assertion on null driverVehicle not tested**
Lines 51-52 use `assert` statements (disabled at runtime by default in JVM unless `-ea` flag is passed). No test verifies the intended null-protection behavior, and no test validates the edge case where assertions are disabled and a `null` argument is passed, which would cause a `NullPointerException` later.

**A74-13 | Severity: MEDIUM | DriverUnitDAO.getDriverUnitsByCompAndDriver() – SQLException propagation untested**
No test verifies that a `SQLException` thrown by `DBUtil.queryForObjects()` propagates correctly to the caller.

**A74-14 | Severity: MEDIUM | DriverUnitDAO.saveDriverVehicle() – connection commit failure untested**
If `connection.commit()` at line 91 throws a `SQLException`, no test verifies what exception the caller receives or what state the database is left in.

---

### DyanmicBeanDAO.java

**A74-15 | Severity: CRITICAL | DyanmicBeanDAO – zero test coverage: no test class exists**
The class `DyanmicBeanDAO` is completely untested. No test file references this class anywhere in the test source tree.

**A74-16 | Severity: CRITICAL | DyanmicBeanDAO.getDynamicBean() – happy-path entirely untested**
The method at line 20 queries the `dynamicbean` table and maps `name`, `type`, and `value` columns into `DynamicBean` objects. No test verifies correct column-to-field mapping or that the returned `ArrayList` contains the expected number of entries.

**A74-17 | Severity: HIGH | DyanmicBeanDAO.getDynamicBean() – empty result set untested**
No test verifies that when the `dynamicbean` table returns zero rows the method returns an empty `ArrayList` rather than `null`.

**A74-18 | Severity: HIGH | DyanmicBeanDAO.getDynamicBean() – exception handling and rethrow untested**
Lines 46-50: any `Exception` (including a `SQLException` from the database) is caught, logged via `InfoLogger.logException()`, wrapped in a new `SQLException`, and rethrown. No test verifies that: (a) the original exception message is preserved in the rethrown `SQLException`, (b) `InfoLogger.logException()` is invoked, or (c) the caller receives a `SQLException`.

**A74-19 | Severity: HIGH | DyanmicBeanDAO.getDynamicBean() – finally-block resource cleanup exception untested**
Lines 51-55: `rs.close()`, `stmt.close()`, and `DBUtil.closeConnection(conn)` are called in a `finally` block. No test verifies behavior when one of these close calls itself throws a `SQLException` (which would mask the original exception).

**A74-20 | Severity: MEDIUM | DyanmicBeanDAO.getDynamicBean() – multiple rows mapped correctly is untested**
No test verifies that all rows returned by the query (not just the first) are added to the result list; a regression that processes only one row would go undetected.

**A74-21 | Severity: INFO | DyanmicBeanDAO – class name is a typo ("Dyanmic" instead of "Dynamic")**
The class is named `DyanmicBeanDAO` (line 16) rather than the correct spelling `DynamicBeanDAO`. This is not a test coverage gap per se, but it increases the chance that future callers searching for `DynamicBeanDAO` will not find this class, and any test file would need to repeat the typo to reference it.

---

### FormBuilderDAO.java

**A74-22 | Severity: CRITICAL | FormBuilderDAO – zero test coverage: no test class exists**
The class `FormBuilderDAO` is completely untested. No test file references this class anywhere in the test source tree.

**A74-23 | Severity: CRITICAL | FormBuilderDAO.getLib() – happy-path entirely untested**
The method at line 24 constructs a SQL string by direct string concatenation of `questionId` and `type` (SQL injection risk, see A74-35), queries `form_library`, and maps `id` and `form_object` (blob) columns into a `FormLibraryBean`. No test verifies correct mapping of either column.

**A74-24 | Severity: HIGH | FormBuilderDAO.getLib() – no-results case untested**
The method uses `if(rs.next())` at line 40 rather than `while(rs.next())`, meaning only the first matching row is ever added to `arrLib`. No test verifies: (a) that a query with zero results returns an empty list, or (b) that when multiple rows match only the first is returned (this may be a logic bug — the method is named `getLib` and returns `ArrayList`, implying multiple results are expected).

**A74-25 | Severity: HIGH | FormBuilderDAO.getLib() – exception handling and rethrow untested**
Lines 50-54: any `Exception` is caught, logged, and rethrown as `SQLException`. No test verifies that the original message is preserved, that logging occurs, or that the caller receives a `SQLException`.

**A74-26 | Severity: HIGH | FormBuilderDAO.getLib() – finally-block resource cleanup exception untested**
Lines 55-59: no test covers behavior when `rs.close()`, `stmt.close()`, or `DBUtil.closeConnection()` throws an exception in the finally block.

**A74-27 | Severity: CRITICAL | FormBuilderDAO.saveLib() – happy-path (insert branch, count == 0) entirely untested**
Lines 91-103: when no existing record is found (`count == 0`) an INSERT is performed. No test verifies the INSERT SQL is correctly parameterized, that `formBuilderBean` is serialized to bytes correctly, or that the method returns `true` on success.

**A74-28 | Severity: CRITICAL | FormBuilderDAO.saveLib() – happy-path (update branch, count > 0) entirely untested**
Lines 105-119: when an existing record is found (`count > 0`) an UPDATE is performed. No test verifies correct parameterization, correct byte serialization of `formBuilderBean`, or that the method returns `true` on success.

**A74-29 | Severity: HIGH | FormBuilderDAO.saveLib() – returns false when executeUpdate() != 1 is untested**
Lines 100-103 and 115-118: both the INSERT and UPDATE paths return `false` if `executeUpdate()` does not return exactly 1. No test exercises these failure branches.

**A74-30 | Severity: HIGH | FormBuilderDAO.saveLib() – null formBuilderBean causes method to silently return true**
Line 77: `if(formBuilderBean!=null)` gates all database activity. When `formBuilderBean` is `null` the method skips all SQL operations and falls through to return `true` at line 134. No test verifies this behavior; callers could interpret the `true` return value as a successful save when in fact nothing was persisted.

**A74-31 | Severity: HIGH | FormBuilderDAO.saveLib() – NumberFormatException on non-numeric questionId or entityId untested**
Lines 84, 96, 98, 113: `Integer.parseInt(questionId)` and `Integer.parseInt(entityId)` are called without validation. A non-numeric string argument throws an unchecked `NumberFormatException` which is caught by the outer `catch(Exception e)` block and rethrown as `SQLException`. No test verifies this error path.

**A74-32 | Severity: CRITICAL | FormBuilderDAO.saveAnswerForm() – happy-path (insert branch) entirely untested**
Lines 166-177: no test verifies the INSERT path for `saveAnswerForm`. Note that `saveAnswerForm` does NOT include `lock_entity_id` in the INSERT (unlike `saveLib`), making the two methods structurally distinct. No test covers this difference.

**A74-33 | Severity: CRITICAL | FormBuilderDAO.saveAnswerForm() – happy-path (update branch) entirely untested**
Lines 179-193: no test verifies the UPDATE path for `saveAnswerForm`. The UPDATE SQL (line 182) uses only `form_object`, `type`, and `question_id` — it does not update `lock_entity_id`. No test covers or validates this intentional difference from `saveLib`.

**A74-34 | Severity: HIGH | FormBuilderDAO.saveAnswerForm() – null formBuilderBean silently returns true, identical to saveLib gap**
Line 152: same silent-no-op-returns-true pattern as A74-30. No test covers the null `formBuilderBean` path.

**A74-35 | Severity: HIGH | FormBuilderDAO.getLib() – SQL injection via string concatenation is untested (and unmitigated)**
Line 37: the SQL string is constructed by direct concatenation of the caller-supplied `questionId` and `type` parameters:
```java
String sql = "select id, form_object from form_library where question_id ="+questionId+" and type = '"+type+"'";
```
No test exercises a malformed or adversarial `questionId` or `type` value. Unlike `saveLib` and `saveAnswerForm` which use `PreparedStatement`, `getLib` uses a raw `Statement`, making it exploitable. There is no test confirming safe or unsafe behavior.

**A74-36 | Severity: MEDIUM | FormBuilderDAO.saveLib() – finally block closes stmt before ps; if stmt.close() throws, ps.close() is skipped**
Lines 127-132: `stmt.close()` is called before `ps.close()`. If `stmt.close()` throws a `SQLException` the `finally` block exits without closing `ps`, leaking a `PreparedStatement`. No test covers this resource-leak path.

**A74-37 | Severity: MEDIUM | FormBuilderDAO.saveAnswerForm() – identical finally-block resource-leak risk as A74-36**
Lines 200-205: same ordering issue as A74-36 with the same untested risk.

**A74-38 | Severity: MEDIUM | FormBuilderDAO.saveLib() and saveAnswerForm() – NumberFormatException on non-numeric questionId untested**
Lines 159, 171, 186: `Integer.parseInt(questionId)` is called without validation in `saveAnswerForm` as well. No test verifies the error path.

**A74-39 | Severity: LOW | FormBuilderDAO.saveLib() – log message says "saveLib" but method is saveLib; saveAnswerForm at line 146 also says "saveLib"**
Line 146 in `saveAnswerForm` logs `"Inside LoginDAO Method : saveLib"` — both the class name (`LoginDAO` should be `FormBuilderDAO`) and the method name (`saveLib` should be `saveAnswerForm`) are wrong. No test verifies correct log output, and this misleading log message would hamper production diagnosis. Same issue exists at line 71 in `saveLib` (class name wrong: `LoginDAO`).

**A74-40 | Severity: LOW | DyanmicBeanDAO.getDynamicBean() – log message references "LoginDAO" instead of "DyanmicBeanDAO"**
Line 26: `log.info("Inside LoginDAO Method : getDynamicBean")` uses the wrong class name. No test validates log output.

---

## Summary Table

| Finding | Severity | Class | Area |
|---|---|---|---|
| A74-1 | CRITICAL | DriverUnitDAO | No test class |
| A74-2 | CRITICAL | DriverUnitDAO | getInstance() untested |
| A74-3 | CRITICAL | DriverUnitDAO | getDriverUnitsByCompAndDriver() happy path |
| A74-4 | HIGH | DriverUnitDAO | getDriverUnitsByCompAndDriver() null params |
| A74-5 | HIGH | DriverUnitDAO | getDriverUnitsByCompAndDriver() empty result set |
| A74-6 | CRITICAL | DriverUnitDAO | saveDriverVehicle() happy path |
| A74-7 | HIGH | DriverUnitDAO | saveDriverVehicle() unassign branch |
| A74-8 | HIGH | DriverUnitDAO | saveDriverVehicle() assign branch |
| A74-9 | HIGH | DriverUnitDAO | saveDriverVehicle() empty driverUnits list |
| A74-10 | HIGH | DriverUnitDAO | saveDriverVehicle() DELETE failure rollback |
| A74-11 | HIGH | DriverUnitDAO | saveDriverVehicle() INSERT failure rollback |
| A74-12 | HIGH | DriverUnitDAO | saveDriverVehicle() assert null-guard not tested |
| A74-13 | MEDIUM | DriverUnitDAO | getDriverUnitsByCompAndDriver() SQLException propagation |
| A74-14 | MEDIUM | DriverUnitDAO | saveDriverVehicle() commit failure |
| A74-15 | CRITICAL | DyanmicBeanDAO | No test class |
| A74-16 | CRITICAL | DyanmicBeanDAO | getDynamicBean() happy path |
| A74-17 | HIGH | DyanmicBeanDAO | getDynamicBean() empty result set |
| A74-18 | HIGH | DyanmicBeanDAO | getDynamicBean() exception rethrow |
| A74-19 | HIGH | DyanmicBeanDAO | getDynamicBean() finally-block close exceptions |
| A74-20 | MEDIUM | DyanmicBeanDAO | getDynamicBean() multiple-row mapping |
| A74-21 | INFO | DyanmicBeanDAO | Class name typo |
| A74-22 | CRITICAL | FormBuilderDAO | No test class |
| A74-23 | CRITICAL | FormBuilderDAO | getLib() happy path |
| A74-24 | HIGH | FormBuilderDAO | getLib() no-results / single-row-only logic |
| A74-25 | HIGH | FormBuilderDAO | getLib() exception rethrow |
| A74-26 | HIGH | FormBuilderDAO | getLib() finally-block close exceptions |
| A74-27 | CRITICAL | FormBuilderDAO | saveLib() insert branch |
| A74-28 | CRITICAL | FormBuilderDAO | saveLib() update branch |
| A74-29 | HIGH | FormBuilderDAO | saveLib() returns-false branches |
| A74-30 | HIGH | FormBuilderDAO | saveLib() null formBuilderBean silently returns true |
| A74-31 | HIGH | FormBuilderDAO | saveLib() NumberFormatException on non-numeric input |
| A74-32 | CRITICAL | FormBuilderDAO | saveAnswerForm() insert branch |
| A74-33 | CRITICAL | FormBuilderDAO | saveAnswerForm() update branch |
| A74-34 | HIGH | FormBuilderDAO | saveAnswerForm() null formBuilderBean silently returns true |
| A74-35 | HIGH | FormBuilderDAO | getLib() SQL injection via string concatenation |
| A74-36 | MEDIUM | FormBuilderDAO | saveLib() finally-block resource leak ordering |
| A74-37 | MEDIUM | FormBuilderDAO | saveAnswerForm() finally-block resource leak ordering |
| A74-38 | MEDIUM | FormBuilderDAO | saveAnswerForm() NumberFormatException on non-numeric input |
| A74-39 | LOW | FormBuilderDAO | Incorrect log messages in saveLib/saveAnswerForm |
| A74-40 | LOW | DyanmicBeanDAO | Incorrect log message in getDynamicBean |

**Total findings: 40**
- CRITICAL: 11
- HIGH: 19
- MEDIUM: 6
- LOW: 2
- INFO: 1
- INFO: 1
