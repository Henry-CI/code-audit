# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A65
**Files Audited:**
1. `src/main/java/com/calibration/UnitCalibrationGetter.java`
2. `src/main/java/com/calibration/UnitCalibrationGetterInDatabase.java`

---

## Source File Evidence

### File 1: UnitCalibrationGetter.java

**Class/Interface name:** `UnitCalibrationGetter` (interface)
**Package:** `com.calibration`

**Methods (with line numbers):**

| Method | Line |
|--------|------|
| `getUnitsToCalibrate()` | 7 |
| `getUnitCalibration(long unitId)` | 8 |

**Fields:** None

**Constants/Enums:** None

**Imports:**
- `java.sql.SQLException` (line 3)
- `java.util.List` (line 4)

---

### File 2: UnitCalibrationGetterInDatabase.java

**Class/Interface name:** `UnitCalibrationGetterInDatabase` (implements `UnitCalibrationGetter`)
**Package:** `com.calibration`

**Fields (with line numbers):**

| Field | Type | Line |
|-------|------|------|
| `filter` | `UnitCalibrationImpactFilter` (private final) | 12 |

**Methods (with line numbers):**

| Method | Visibility | Line |
|--------|------------|------|
| `UnitCalibrationGetterInDatabase()` (constructor) | public | 14 |
| `getUnitsToCalibrate()` | public (Override) | 19 |
| `getUnitCalibration(long unitId)` | public (Override) | 32 |
| `makeUnit(ResultSet result)` | private | 41 |
| `getImpactsForUnit(long unitId, Timestamp resetCalibrationDate)` | private | 53 |

**Constants/Enums:** None

**Imports:**
- `com.util.DBUtil` (line 3)
- `java.sql.Date` (line 5) — imported but unused
- `java.sql.ResultSet` (line 6)
- `java.sql.SQLException` (line 7)
- `java.sql.Timestamp` (line 8)
- `java.util.List` (line 9)

---

## Test Coverage Search Results

**Test directory searched:** `src/test/java/`

**Grep for `UnitCalibrationGetter`:**
- Matched in: `src/test/java/com/calibration/UnitCalibratorTest.java`
  - `UnitCalibrationGetter` is used only as a **Mockito mock** (`mock(UnitCalibrationGetter.class)`). The interface contract is stubbed; the concrete implementation `UnitCalibrationGetterInDatabase` is never instantiated or exercised.

**Grep for `UnitCalibrationGetterInDatabase`:**
- **No matches found** in the entire test directory.

**Conclusion:** `UnitCalibrationGetterInDatabase` has **zero test coverage**. The interface `UnitCalibrationGetter` is only ever interacted with via a mock. No integration tests, no unit tests with a test database or in-memory DB, and no mocking of `DBUtil` are present anywhere in the test suite.

---

## Findings

### A65-1 | Severity: HIGH | UnitCalibrationGetterInDatabase has zero test coverage

The class `UnitCalibrationGetterInDatabase` — the sole concrete implementation of the `UnitCalibrationGetter` interface — has no test coverage whatsoever. No test file references it, instantiates it, or exercises any of its methods (`getUnitsToCalibrate`, `getUnitCalibration`, `makeUnit`, `getImpactsForUnit`). All tests in `UnitCalibratorTest` mock the interface, meaning bugs in the real database implementation are entirely invisible to the test suite. Any regression in query construction, parameter binding, or result mapping would go undetected until runtime.

---

### A65-2 | Severity: HIGH | getUnitCalibration silently returns null when no row is found; null return is not tested

At line 38, `getUnitCalibration` calls `DBUtil.queryForObject(...).orElse(null)`, meaning the method returns `null` when no unit with the given `unitId` exists in the database. No test verifies that callers handle this null return. Any caller that dereferences the result without a null check will throw a `NullPointerException`. This is compounded by the fact that `DBUtil.queryForObject` swallows `SQLException` internally (prints stack trace, returns `Optional.empty()`), meaning the null could also be caused silently by a database error rather than a missing row, and the caller has no way to distinguish the two cases.

---

### A65-3 | Severity: HIGH | SQLException silently swallowed in DBUtil; methods declare throws SQLException but exceptions are never propagated

Both `getUnitsToCalibrate` (line 19) and `getUnitCalibration` (line 32) declare `throws SQLException` in their signatures, but the underlying `DBUtil.queryForObjects` and `DBUtil.queryForObject` methods (DBUtil.java lines 75-77, 164-166) catch all `SQLException` instances internally, print the stack trace, and return an empty result. This means:
- Database connection failures return empty lists or `Optional.empty()` silently.
- Callers cannot distinguish between "no data exists" and "query failed."
- The `throws SQLException` declaration on `getUnitsToCalibrate` and `getUnitCalibration` is misleading — in practice these methods never throw; they fail silently.
- There are no tests covering the failure path, not even via the mock layer.

---

### A65-4 | Severity: MEDIUM | getImpactsForUnit is not tested for null resetCalibrationDate

At line 59, `getImpactsForUnit` binds `resetCalibrationDate` directly to a PreparedStatement parameter via `statement.setTimestamp(2, resetCalibrationDate)`. If `resetCalibrationDate` is `null` (which is permitted by the schema — `reset_calibration_date IS NOT NULL` is only a filter in `getUnitsToCalibrate`, not in `getUnitCalibration`), then `setTimestamp(2, null)` is called. While JDBC may tolerate this and pass SQL NULL to the query, the resulting behaviour — returning impacts regardless of session start time — would be logically incorrect. There is no null guard and no test covering this path. This situation arises when `getUnitCalibration` is called directly with a unit whose `reset_calibration_date` is NULL.

---

### A65-5 | Severity: MEDIUM | makeUnit is not tested for missing or unexpected ResultSet columns

The private method `makeUnit` (lines 41-51) accesses four ResultSet columns by name: `id`, `reset_calibration_date`, `calibration_date`, and `impact_threshold`. No test verifies that a `ResultSet` missing one of these columns produces a meaningful error, nor that incorrect column types cause a detectable failure. Because `DBUtil` swallows `SQLException`, a mapping failure would silently result in default/zero values being propagated into a `UnitCalibration` object (e.g., `unitId = 0`, `threshold = 0`), which could cause incorrect calibration decisions downstream.

---

### A65-6 | Severity: MEDIUM | getUnitsToCalibrate not tested for empty result set

There is no test verifying behaviour when `getUnitsToCalibrate` returns an empty list (i.e., no units currently require calibration). While the method itself would simply return an empty `ArrayList`, no test confirms that callers handle this gracefully and that the calibration job does not error or produce unexpected side effects in the zero-unit case.

---

### A65-7 | Severity: MEDIUM | getUnitCalibration not tested for any scenario

The method `getUnitCalibration(long unitId)` (line 32) is entirely untested. Missing test scenarios include:
- Unit exists with a valid `reset_calibration_date`.
- Unit exists with a null `reset_calibration_date`.
- Unit does not exist (returns null).
- `unitId` is zero or negative (boundary values).
- `unitId` is `Long.MAX_VALUE` (boundary value).
- Multiple rows returned for a single unit (would trigger the "Unique result expected" path in `DBUtil`, but that exception is also swallowed).

---

### A65-8 | Severity: MEDIUM | UnitCalibrationGetter interface is only used as a mock; contract is not verified against its implementation

`UnitCalibratorTest` mocks `UnitCalibrationGetter` and stubs `getUnitsToCalibrate()` to return controlled data. This approach tests `UnitCalibrator` in isolation but provides no guarantee that `UnitCalibrationGetterInDatabase` satisfies the interface contract at runtime. There are no contract tests (e.g., using Mockito's `@Spy` on a partial real implementation, or a test double backed by an in-memory database) to bridge this gap.

---

### A65-9 | Severity: LOW | Unused import of java.sql.Date in UnitCalibrationGetterInDatabase

Line 5 of `UnitCalibrationGetterInDatabase.java` imports `java.sql.Date`, which is not used anywhere in the class. This is dead code in the import section. No test would catch this, but it is a code quality indicator that the class has not been subjected to even basic static analysis or compiler-warning checks.

---

### A65-10 | Severity: LOW | Constructor UnitCalibrationGetterInDatabase() not tested independently

The no-argument constructor (line 14) instantiates a `UnitCalibrationImpactFilter` and assigns it to the `filter` field. There is no test confirming that the constructor succeeds, that the correct `UnitCalibrationImpactFilter` instance is created, or that the field is non-null when subsequently used by `getImpactsForUnit`. Although this is low-risk given the simplicity of the constructor, the complete absence of any test for the class means even constructor-level failures would go undetected.

---

### A65-11 | Severity: LOW | getImpactsForUnit not tested for large impact datasets or performance boundaries

`getImpactsForUnit` (line 53) queries the `v_impacts` view, which may return an unbounded number of rows. There is no test confirming behaviour with very large result sets (e.g., thousands of impacts for a unit with a long calibration window). The full result set is loaded into a `List<CalibrationImpact>` in memory before filtering, which could cause memory pressure in production for heavily-used units. No test exercises this boundary condition.

---

### A65-12 | Severity: INFO | UnitCalibrationGetter interface has no Javadoc describing contract for null returns or exception semantics

The `UnitCalibrationGetter` interface declares both methods as `throws SQLException`, but as noted in A65-3 the concrete implementation never actually throws. There is no Javadoc on either interface method describing the expected return value when no data is found, the conditions under which `null` may be returned by `getUnitCalibration`, or the exception semantics. This ambiguity increases the risk of incorrect caller implementations or test stubs.

---

## Summary Table

| Finding | Severity | Topic |
|---------|----------|-------|
| A65-1 | HIGH | Zero test coverage for UnitCalibrationGetterInDatabase |
| A65-2 | HIGH | Null return from getUnitCalibration untested; caller null-safety unverified |
| A65-3 | HIGH | SQLException silently swallowed; throws declaration misleading; no failure path tests |
| A65-4 | MEDIUM | null resetCalibrationDate passed to JDBC setTimestamp untested |
| A65-5 | MEDIUM | makeUnit not tested for missing/mistyped ResultSet columns |
| A65-6 | MEDIUM | getUnitsToCalibrate empty result not tested |
| A65-7 | MEDIUM | getUnitCalibration untested for all scenarios including boundaries |
| A65-8 | MEDIUM | Interface contract not verified against concrete implementation |
| A65-9 | LOW | Unused import java.sql.Date |
| A65-10 | LOW | Constructor not tested independently |
| A65-11 | LOW | No boundary/performance test for large impact datasets |
| A65-12 | INFO | Interface missing Javadoc for null return and exception semantics |
