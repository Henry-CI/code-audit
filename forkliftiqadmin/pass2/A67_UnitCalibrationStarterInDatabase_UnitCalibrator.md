# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A67
**Date:** 2026-02-26

**Source Files Audited:**
1. `src/main/java/com/calibration/UnitCalibrationStarterInDatabase.java`
2. `src/main/java/com/calibration/UnitCalibrator.java`

**Primary Test File:**
- `src/test/java/com/calibration/UnitCalibratorTest.java`

**Additional Test Files Consulted (indirect context):**
- `src/test/java/com/calibration/UnitCalibrationTest.java` (covers `UnitCalibration`, not the audited classes)
- `src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java` (covers `UnitCalibrationImpactFilter`, not the audited classes)

---

## Reading Evidence

### File 1: `UnitCalibrationStarterInDatabase.java`

**Class:** `UnitCalibrationStarterInDatabase` (line 7)
- Implements: `UnitCalibrationStarter` (interface, line 7)
- Package: `com.calibration`

**Fields:** None declared (no instance fields).

**Constants/Enums:** None.

**Methods:**

| Method | Line | Visibility | Signature |
|--------|------|------------|-----------|
| `startCalibration` | 9 | `public` (via `@Override`) | `void startCalibration(long unitId) throws SQLException` |

**SQL executed by `startCalibration`** (lines 10–14):
```sql
UPDATE unit
SET impact_threshold = 0,
    alert_enabled = FALSE,
    reset_calibration_date = NOW(),
    calibration_date = NULL
WHERE id = ?
```
The method delegates directly to `DBUtil.updateObject(query, statement -> statement.setLong(1, unitId))` with no branching logic beyond what happens inside `DBUtil`.

---

### File 2: `UnitCalibrator.java`

**Class:** `UnitCalibrator` (line 6)
- Package-private (`class`, not `public`)
- Package: `com.calibration`

**Fields:**

| Field | Line | Type | Visibility |
|-------|------|------|------------|
| `unitCalibrationGetter` | 7 | `UnitCalibrationGetter` | `private final` |
| `unitCalibrationEnder` | 8 | `UnitCalibrationEnder` | `private final` |

**Constants/Enums:** None.

**Methods:**

| Method | Line | Visibility | Signature |
|--------|------|------------|-----------|
| Constructor | 10–14 | package-private | `UnitCalibrator(UnitCalibrationGetter, UnitCalibrationEnder)` |
| `calibrateAllUnits` | 16–20 | package-private | `void calibrateAllUnits() throws SQLException` |
| `calibrateUnit` | 22–26 | `private` | `void calibrateUnit(UnitCalibration) throws SQLException` |

**Branch inventory for `calibrateUnit`** (line 23):
- Branch A: `calibrationPercentage() == 100` → calls `endCalibration`
- Branch B: `calibrationPercentage() != 100` → early return, no call

**Branch inventory for `calibrateAllUnits`** (lines 17–19):
- Branch A: list returned by `getUnitsToCalibrate()` is non-empty → iterates
- Branch B: list is empty → loop body never executes
- Branch C (implicit): `getUnitsToCalibrate()` throws `SQLException` → propagates

---

## Grep Results – Additional Indirect Coverage in Test Directory

```
Grep: "UnitCalibrationStarterInDatabase" in src/test/java → NO MATCHES
Grep: "startCalibration"               in src/test/java → NO MATCHES
Grep: "UnitCalibrator"                 in src/test/java → UnitCalibratorTest.java only (class declaration + constructor)
Grep: "calibrateAllUnits"              in src/test/java → UnitCalibratorTest.java lines 30, 40, 52 (all via public entry point)
Grep: "calibrateUnit"                  in src/test/java → NO MATCHES (private method; exercised only indirectly)
Grep: "UnitCalibrationStarter"         in src/test/java → NO MATCHES
Grep: "resetCalibration"               in src/test/java → UnitCalibrationTest.java only (field value in builder, unrelated class)
```

**Conclusion:** `UnitCalibrationStarterInDatabase` has **zero test coverage** anywhere in the test directory. `UnitCalibrator` is covered only by `UnitCalibratorTest.java`.

---

## Coverage Analysis

### UnitCalibratorTest – Test Inventory

| Test Method | Scenario Tested | Branch in `calibrateUnit` |
|-------------|----------------|--------------------------|
| `SetsThresholdOfUnitWithMoreThan100ValidImpacts` | Single unit, `calibrationPercentage == 100` (exactly 100 impacts) | Branch A |
| `DoesNotSetThresholdOfUnitWithLessThan100ValidImpacts` | Single unit, `calibrationPercentage == 99` (99 impacts) | Branch B |
| `SetsNewThresholdsWithMultipleUnits` | Three units: 100%, 80%, 120% impacts — mixed | Both A and B |

**Note on `calibrationPercentage` semantics:** The test helper `makeUnitToCalibrate` builds a `UnitCalibration` with only a `unitId` and an `impacts` list (no `resetCalibrationDate`, `calibrationDate`, or `threshold`). `UnitCalibration.calibrationPercentage()` returns 100 when `isCalibrated()` is true OR when `impacts.size() >= 100`. The test with `impactCount = 100` reaches exactly 100 impacts, so `calibrationPercentage()` returns 100 via `calibrationDone()`. The test with `impactCount = 120` also reaches 100%. The test named "MoreThan100ValidImpacts" actually uses exactly 100, which is a naming inaccuracy but not a gap being evaluated here.

---

## Findings

### UnitCalibrationStarterInDatabase

---

**A67-1 | Severity: CRITICAL | `UnitCalibrationStarterInDatabase` has no test coverage whatsoever**

`UnitCalibrationStarterInDatabase` implements `UnitCalibrationStarter` and executes a destructive `UPDATE` query against the `unit` table that zeroes `impact_threshold`, sets `alert_enabled = FALSE`, sets `reset_calibration_date = NOW()`, and nulls `calibration_date`. There is not a single test case for this class in the entire test directory. The only call site is `UnitDAO.resetCalibration()` (line 876), which is itself not tested at the unit level. The method has no conditional logic, so the only testable behaviour is the correct construction and execution of the SQL statement — but that path is never exercised in the test suite.

---

**A67-2 | Severity: HIGH | No test verifies the SQL UPDATE column set for `startCalibration`**

The `UPDATE` statement resets five columns: `impact_threshold = 0`, `alert_enabled = FALSE`, `reset_calibration_date = NOW()`, `calibration_date = NULL`, and the `WHERE id = ?` predicate. A regression that dropped or misordered any of those clauses would not be caught by any automated test. The absence of an integration or mocked-`DBUtil` test means the correctness of the SQL string is entirely untestable without manual inspection.

---

**A67-3 | Severity: HIGH | No test verifies that `startCalibration` propagates `SQLException` to callers**

`startCalibration` declares `throws SQLException`. `DBUtil.updateObject` can throw `SQLException` on connection failure or bad SQL. No test verifies that the exception is not swallowed and surfaces correctly to the caller (`UnitDAO.resetCalibration`, which does propagate it).

---

**A67-4 | Severity: MEDIUM | No test for `startCalibration` with a non-existent or invalid `unitId`**

The method accepts a `long unitId` and passes it as a bind parameter. No test verifies behaviour when `unitId` is 0, negative, or refers to a non-existent row. While the UPDATE would affect 0 rows silently in that case, there is no assertion that such silent no-ops are acceptable or detectable.

---

**A67-5 | Severity: LOW | `UnitCalibrationStarterInDatabase` is a concrete class instantiated with `new` at the call site (`UnitDAO` line 876), making it impossible to mock in tests of `UnitDAO`**

The class is not injected via the `UnitCalibrationStarter` interface; instead `UnitDAO.resetCalibration` calls `new UnitCalibrationStarterInDatabase()` directly. This tight coupling means that any future test of `UnitDAO.resetCalibration` will require a live database rather than being able to substitute a mock/stub of `UnitCalibrationStarter`.

---

### UnitCalibrator

---

**A67-6 | Severity: HIGH | Empty-list path for `calibrateAllUnits` is not tested**

When `unitCalibrationGetter.getUnitsToCalibrate()` returns an empty list, `calibrateAllUnits` performs no iteration and makes no calls to `unitCalibrationEnder`. No test covers this scenario (e.g., `when(unitCalibrationGetter.getUnitsToCalibrate()).thenReturn(Collections.emptyList())`). While the production consequence is benign (no-op), a test is needed to guard against regressions that might incorrectly short-circuit or throw on an empty list.

---

**A67-7 | Severity: HIGH | `SQLException` propagation from `getUnitsToCalibrate()` is not tested**

`calibrateAllUnits` declares `throws SQLException`. If `unitCalibrationGetter.getUnitsToCalibrate()` throws a `SQLException`, the exception should propagate to the caller. No test configures the mock to throw and then asserts that the exception surfaces. In `CalibrationJob.calibrateAllUnits()` (the production caller), this exception is silently swallowed via `e.printStackTrace()`, but the `UnitCalibrator` contract itself is untested for this path.

---

**A67-8 | Severity: HIGH | `SQLException` propagation from `endCalibration()` is not tested**

Similarly, if `unitCalibrationEnder.endCalibration()` throws a `SQLException` mid-loop (e.g., on the second of three units), no test verifies whether iteration halts for all remaining units or whether any partial state is acceptable. The exception would propagate out of `calibrateAllUnits`, abandoning uncalibrated units.

---

**A67-9 | Severity: MEDIUM | `calibrationPercentage() > 100` is tested only incidentally and the boundary at exactly 100 is not distinguished from above-100**

The test `SetsNewThresholdsWithMultipleUnits` includes a unit with 120 impacts (`calibrationPercentage` = 100 via the cap at line 68 of `UnitCalibration`). The test for "MoreThan100ValidImpacts" uses exactly 100 impacts, not more than 100. There is no dedicated test that passes a `UnitCalibration` where `calibrationPercentage()` returns exactly 100 due to the `> 100` cap path (`impacts.size() > 100 ? 100 : impacts.size()`). While the observable outcome is the same (endCalibration is called), the specific code path in `UnitCalibration.calibrationPercentage()` triggered by `> 100` vs. `== 100` is not isolated in `UnitCalibratorTest`.

---

**A67-10 | Severity: MEDIUM | `calibrateAllUnits` is not tested when `getUnitsToCalibrate()` returns null**

If `unitCalibrationGetter.getUnitsToCalibrate()` returns `null` (a legal value for a mock that is not configured), the enhanced `for` loop at line 18 will throw a `NullPointerException`. The production implementation (`UnitCalibrationGetterInDatabase`) returns a `List` from `DBUtil.queryForObjects` and would not return null, but the contract of `UnitCalibrationGetter` does not preclude null, and no null-guard exists in `UnitCalibrator`. This is not tested.

---

**A67-11 | Severity: MEDIUM | `calibrateUnit` is never tested in isolation; it is only exercised as a side effect of `calibrateAllUnits`**

`calibrateUnit` is `private`, so it cannot be tested directly, which is expected. However, there is no test that passes a `UnitCalibration` object that has been constructed with all its fields populated (i.e., with `resetCalibrationDate`, `calibrationDate`, and `threshold` all set) to verify that the `calibrationPercentage()` == 100 path works correctly for the fully-calibrated-via-date-and-threshold case. All `UnitCalibratorTest` tests use `makeUnitToCalibrate`, which only populates `unitId` and `impacts`.

---

**A67-12 | Severity: LOW | Test method name `SetsThresholdOfUnitWithMoreThan100ValidImpacts` is misleading**

The helper `makeUnitToCalibrate(1, 100)` creates exactly 100 impacts, not "more than 100". The method name asserts a scenario that does not match the data constructed. This makes the test intent ambiguous and may cause future maintainers to create a wrong assumption about boundary semantics (whether 100 is inclusive or exclusive). The actual boundary check in `UnitCalibration.calibrationPercentage()` uses `impacts.size() >= 100` (via `calibrationDone`), so 100 is indeed sufficient — but the test name says "more than 100".

---

**A67-13 | Severity: LOW | No test verifies the constructor argument assignment in `UnitCalibrator`**

The constructor assigns `unitCalibrationGetter` and `unitCalibrationEnder` to `private final` fields. If the assignments were accidentally reversed, the tests would fail with class-cast errors at runtime rather than clear assertion failures, since both are interfaces and the error would surface only indirectly. A dedicated test confirming that the correct collaborator is invoked for each role (getter vs. ender) is implicitly provided by the existing tests, but there is no explicit verification of constructor wiring.

---

**A67-14 | Severity: INFO | `UnitCalibrator` and `UnitCalibrationEnder` are package-private; this limits testability from outside the package**

`UnitCalibrator` has no `public` modifier (line 6) and `UnitCalibrationEnder` is also package-private (line 5 of `UnitCalibrationEnder.java`). The test class `UnitCalibratorTest` is in the same package (`com.calibration`), so this is workable, but the package-private visibility is a design choice that prevents third-party or integration tests from accessing these classes without being in the same package.

---

## Summary Table

| Finding | Severity | Class | Area |
|---------|----------|-------|------|
| A67-1 | CRITICAL | `UnitCalibrationStarterInDatabase` | Zero test coverage |
| A67-2 | HIGH | `UnitCalibrationStarterInDatabase` | SQL correctness unverified |
| A67-3 | HIGH | `UnitCalibrationStarterInDatabase` | `SQLException` propagation untested |
| A67-4 | MEDIUM | `UnitCalibrationStarterInDatabase` | Invalid/zero `unitId` not tested |
| A67-5 | LOW | `UnitCalibrationStarterInDatabase` | Hard-coded instantiation prevents mocking |
| A67-6 | HIGH | `UnitCalibrator` | Empty list path not tested |
| A67-7 | HIGH | `UnitCalibrator` | `SQLException` from getter not tested |
| A67-8 | HIGH | `UnitCalibrator` | `SQLException` from ender not tested |
| A67-9 | MEDIUM | `UnitCalibrator` | `calibrationPercentage > 100` cap path not isolated |
| A67-10 | MEDIUM | `UnitCalibrator` | Null return from getter causes NPE, not tested |
| A67-11 | MEDIUM | `UnitCalibrator` | `calibrateUnit` never tested with fully-populated `UnitCalibration` |
| A67-12 | LOW | `UnitCalibrator` | Misleading test method name |
| A67-13 | LOW | `UnitCalibrator` | Constructor wiring not explicitly verified |
| A67-14 | INFO | Both | Package-private visibility limits external testability |
