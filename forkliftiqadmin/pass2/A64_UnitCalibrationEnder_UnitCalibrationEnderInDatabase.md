# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A64
**Source files audited:**
- `src/main/java/com/calibration/UnitCalibrationEnder.java`
- `src/main/java/com/calibration/UnitCalibrationEnderInDatabase.java`

---

## 1. Reading Evidence

### UnitCalibrationEnder.java

**Type:** Interface
**Package:** `com.calibration`
**File:** `src/main/java/com/calibration/UnitCalibrationEnder.java`

| Element | Kind | Lines |
|---------|------|-------|
| `UnitCalibrationEnder` | interface declaration | 5 |
| `endCalibration(long unitId, int newThreshold)` | abstract method | 6 |

**Fields:** None
**Imports:** `java.sql.SQLException`
**Checked exceptions declared:** `SQLException`

---

### UnitCalibrationEnderInDatabase.java

**Type:** Class (implements `UnitCalibrationEnder`)
**Package:** `com.calibration`
**File:** `src/main/java/com/calibration/UnitCalibrationEnderInDatabase.java`

| Element | Kind | Lines |
|---------|------|-------|
| `UnitCalibrationEnderInDatabase` | class declaration | 7 |
| `endCalibration(long unitId, int newThreshold)` | `@Override` public method | 9–18 |
| SQL UPDATE string construction | inline logic | 10–13 |
| `DBUtil.updateObject(query, lambda)` call | statement execution | 14 |
| `statement.setInt(1, newThreshold)` | parameter binding | 15 |
| `statement.setLong(2, unitId)` | parameter binding | 16 |

**Fields:** None (stateless class)
**Imports:** `com.util.DBUtil`, `java.sql.SQLException`
**Checked exceptions declared:** `SQLException`

**SQL produced at runtime:**
```sql
UPDATE unit
SET impact_threshold = ?,
    alert_enabled    = TRUE,
    calibration_date = NOW()
WHERE id = ?
```
Parameter binding order: `?1 = newThreshold (INT)`, `?2 = unitId (LONG)`.

---

## 2. Test Directory Grep Results

**Search term:** `UnitCalibrationEnder`
**Search term:** `UnitCalibrationEnderInDatabase`
**Search path:** `src/test/java/`

### Matches for `UnitCalibrationEnder`

```
src/test/java/com/calibration/UnitCalibratorTest.java:15:
    private UnitCalibrationEnder unitCalibrationEnder;

src/test/java/com/calibration/UnitCalibratorTest.java:20:
    unitCalibrationEnder = mock(UnitCalibrationEnder.class);
```

### Matches for `UnitCalibrationEnderInDatabase`

**No matches found.**

---

## 3. Indirect Coverage via UnitCalibratorTest.java

`UnitCalibratorTest` was read in full (69 lines). Summary of relevant behaviour:

| Test method | What it exercises regarding `UnitCalibrationEnder` |
|-------------|-----------------------------------------------------|
| `SetsThresholdOfUnitWithMoreThan100ValidImpacts` | Verifies `endCalibration` is called once when `impactCount >= 100` |
| `DoesNotSetThresholdOfUnitWithLessThan100ValidImpacts` | Verifies `endCalibration` is NOT called when `impactCount < 100` |
| `SetsNewThresholdsWithMultipleUnits` | Verifies `endCalibration` called for qualifying units and not called for non-qualifying units in a mixed list |

**Key observation:** In all three tests, `unitCalibrationEnder` is created with `mock(UnitCalibrationEnder.class)` — a Mockito mock of the interface.  The concrete implementation `UnitCalibrationEnderInDatabase` is **never instantiated** in any test.  The tests validate the `UnitCalibrator` orchestration logic only; the real SQL path is bypassed entirely.

---

## 4. Coverage Findings

### A64-1 | Severity: CRITICAL | UnitCalibrationEnderInDatabase has zero test coverage

`UnitCalibrationEnderInDatabase` is never referenced in any test file.  No test instantiates it, injects it, or calls its `endCalibration` method with real or mocked database resources.  The only test file that references `UnitCalibrationEnder` (the interface) uses `mock(UnitCalibrationEnder.class)`, which never exercises the concrete class.  Line coverage for `UnitCalibrationEnderInDatabase` is 0%.

### A64-2 | Severity: CRITICAL | endCalibration SQL logic is completely untested

The UPDATE statement built inside `UnitCalibrationEnderInDatabase.endCalibration` (lines 10–13) is never executed under test.  There is no integration test, repository test, or use of an in-memory database (e.g., H2) that would verify the SQL is syntactically correct, that `impact_threshold` and `id` columns map to the correct parameters, or that `alert_enabled` and `calibration_date` are set as intended.

### A64-3 | Severity: HIGH | Parameter binding order is untested and carries silent-corruption risk

The lambda at lines 14–17 binds `newThreshold` to `?1` (INT) and `unitId` to `?2` (LONG).  If the order were reversed the query would execute silently (both are numeric) but corrupt data.  No test verifies the binding order against actual column semantics.

### A64-4 | Severity: HIGH | SQLException propagation from endCalibration is untested

`endCalibration` declares `throws SQLException`.  `DBUtil.updateObject` (the no-connection overload, lines 211–226 of DBUtil.java) catches `SQLException` internally, prints a stack trace, and returns `-1` — meaning a real SQL failure is swallowed and never propagated to the caller.  This diverges from the declared contract.  No test exercises this failure path or asserts on the return value / exception behaviour.

### A64-5 | Severity: MEDIUM | No test verifies the UPDATE affects exactly one row

`DBUtil.updateObject` returns the row-count from `executeUpdate()` but `UnitCalibrationEnderInDatabase.endCalibration` discards the return value (void method, return value of `DBUtil.updateObject` is ignored).  There is no assertion — even in a hypothetical integration test — that exactly one row was updated, or that an update affecting zero rows (unknown `unitId`) is detected and handled.

### A64-6 | Severity: MEDIUM | UnitCalibrationEnder interface contract is only tested through a mock

The interface `UnitCalibrationEnder` itself has no dedicated contract test.  `UnitCalibratorTest` tests `UnitCalibrator`'s use of the interface via a mock, which is correct practice for unit testing the orchestrator.  However, no test verifies that the interface's single concrete implementor (`UnitCalibrationEnderInDatabase`) satisfies the expected behaviour, leaving the interface-to-implementation contract unverified.

### A64-7 | Severity: LOW | calibration_date = NOW() is a server-side timestamp with no testability

The UPDATE hardcodes `calibration_date = NOW()` (MySQL server time).  No test verifies that the calibration date is set at all, or that it is approximately equal to the time of the call.  This is low severity because the logic is trivial, but it represents untested observable side-effect state.

### A64-8 | Severity: INFO | alert_enabled = TRUE hardcoding is untested

The column `alert_enabled` is unconditionally set to `TRUE` on every calibration end.  No test verifies this column's value after a calibration, nor that the intent (re-enabling alerts post-calibration) is preserved if the SQL is refactored.

---

## 5. Summary Table

| Finding | Severity | Area |
|---------|----------|------|
| A64-1 | CRITICAL | `UnitCalibrationEnderInDatabase` — zero test coverage |
| A64-2 | CRITICAL | SQL UPDATE logic — never executed under test |
| A64-3 | HIGH | Parameter binding order — silent corruption risk, untested |
| A64-4 | HIGH | `SQLException` swallowed by `DBUtil` — contract divergence, untested |
| A64-5 | MEDIUM | Row-count return value discarded — zero-row update undetected |
| A64-6 | MEDIUM | Interface-to-implementation contract — only mocked, never verified |
| A64-7 | LOW | `calibration_date = NOW()` — server-side timestamp, unasserted |
| A64-8 | INFO | `alert_enabled = TRUE` hardcoding — side-effect unverified |

---

## 6. Test Files Examined

| File | Role |
|------|------|
| `src/test/java/com/calibration/UnitCalibratorTest.java` | Tests `UnitCalibrator` orchestration using a mock of `UnitCalibrationEnder`; does NOT cover `UnitCalibrationEnderInDatabase` |
| `src/test/java/com/calibration/UnitCalibrationTest.java` | Unrelated (tests `UnitCalibration` model) |
| `src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java` | Unrelated (tests impact filter logic) |
| `src/test/java/com/util/ImpactUtilTest.java` | Unrelated (tests `ImpactUtil`) |
