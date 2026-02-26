# Pass 3 Documentation Audit — A67
**Audit run:** 2026-02-26-01
**Files:**
- `calibration/UnitCalibrationStarterInDatabase.java`
- `calibration/UnitCalibrator.java`

---

## 1. Reading Evidence

### 1.1 `UnitCalibrationStarterInDatabase.java`

| Element | Kind | Line |
|---|---|---|
| `UnitCalibrationStarterInDatabase` | class (public, implements `UnitCalibrationStarter`) | 7 |
| `startCalibration(long unitId)` | method — public, `@Override`, throws `SQLException` | 9 |

**Fields:** none declared.

---

### 1.2 `UnitCalibrator.java`

| Element | Kind | Line |
|---|---|---|
| `UnitCalibrator` | class (package-private) | 6 |
| `unitCalibrationGetter` | field — `private final UnitCalibrationGetter` | 7 |
| `unitCalibrationEnder` | field — `private final UnitCalibrationEnder` | 8 |
| `UnitCalibrator(UnitCalibrationGetter, UnitCalibrationEnder)` | constructor — package-private | 10–13 |
| `calibrateAllUnits()` | method — package-private, throws `SQLException` | 16 |
| `calibrateUnit(UnitCalibration)` | method — private, throws `SQLException` | 22 |

---

## 2. Findings

### A67-1 — LOW — No class-level Javadoc: `UnitCalibrationStarterInDatabase`

**File:** `calibration/UnitCalibrationStarterInDatabase.java`, line 7

No class-level Javadoc comment is present above the class declaration. The class implements the `UnitCalibrationStarter` interface via a database-backed approach, performing a SQL `UPDATE` that resets calibration fields. That purpose is not documented.

```java
// No Javadoc here
public class UnitCalibrationStarterInDatabase implements UnitCalibrationStarter {
```

**Recommendation:** Add a class-level `/** ... */` comment describing that this is the database-backed implementation of `UnitCalibrationStarter` and what the `startCalibration` operation does at a high level.

---

### A67-2 — MEDIUM — Undocumented non-trivial public method: `startCalibration`

**File:** `calibration/UnitCalibrationStarterInDatabase.java`, lines 8–16

The method `startCalibration(long unitId)` is public (by virtue of implementing a public interface) and performs a non-trivial database side-effect: it resets `impact_threshold` to `0`, disables alerts (`alert_enabled = FALSE`), sets `reset_calibration_date` to `NOW()`, and nulls `calibration_date` for the given unit. None of this behaviour is documented.

```java
@Override
public void startCalibration(long unitId) throws SQLException {
    String query = "UPDATE unit SET impact_threshold = 0, " +
            "alert_enabled = FALSE, " +
            "reset_calibration_date = NOW(), " +
            "calibration_date = NULL " +
            "WHERE id = ?";
    DBUtil.updateObject(query, statement -> statement.setLong(1, unitId));
}
```

No `/** ... */` block is present. Missing `@param unitId` and `@throws SQLException` tags are also absent.

**Recommendation:** Add a Javadoc block describing the side-effects (fields reset, rationale), plus `@param unitId` and `@throws SQLException`.

---

### A67-3 — LOW — No class-level Javadoc: `UnitCalibrator`

**File:** `calibration/UnitCalibrator.java`, line 6

No class-level Javadoc comment is present above the `UnitCalibrator` class declaration. The class coordinates fetching units ready for calibration and completing them when `calibrationPercentage` reaches 100, which is non-obvious behaviour worth documenting.

```java
// No Javadoc here
class UnitCalibrator {
```

**Recommendation:** Add a class-level `/** ... */` comment explaining the calibration-completion orchestration role of this class.

---

### A67-4 — MEDIUM — Undocumented non-trivial package-private method: `calibrateAllUnits`

**File:** `calibration/UnitCalibrator.java`, lines 16–20

`calibrateAllUnits()` fetches all units awaiting calibration and iterates them, delegating to `calibrateUnit`. Although package-private, this is the primary entry-point for the calibration workflow and is non-trivial. No Javadoc is present.

```java
void calibrateAllUnits() throws SQLException {
    List<UnitCalibration> unitsToCalibrate = unitCalibrationGetter.getUnitsToCalibrate();
    for (UnitCalibration unitCalibration : unitsToCalibrate)
        calibrateUnit(unitCalibration);
}
```

**Recommendation:** Add a Javadoc block describing what "calibrate all units" means, including the threshold for completion, and a `@throws SQLException` tag.

---

### A67-5 — LOW — Undocumented package-private constructor: `UnitCalibrator`

**File:** `calibration/UnitCalibrator.java`, lines 10–13

The constructor accepts two collaborators via dependency injection. No Javadoc is present to describe the expected implementations or the role of each dependency.

```java
UnitCalibrator(UnitCalibrationGetter unitCalibrationGetter,
               UnitCalibrationEnder unitCalibrationEnder) {
```

This is rated LOW because it is a straightforward constructor, but the dependency semantics are worth noting.

**Recommendation:** Add a brief `/** ... */` block with `@param` tags for both parameters.

---

## 3. Summary

| ID | Severity | File | Element | Issue |
|---|---|---|---|---|
| A67-1 | LOW | `UnitCalibrationStarterInDatabase.java` | Class | No class-level Javadoc |
| A67-2 | MEDIUM | `UnitCalibrationStarterInDatabase.java` | `startCalibration(long)` | No Javadoc; missing `@param`, `@throws` |
| A67-3 | LOW | `UnitCalibrator.java` | Class | No class-level Javadoc |
| A67-4 | MEDIUM | `UnitCalibrator.java` | `calibrateAllUnits()` | No Javadoc; missing `@throws` |
| A67-5 | LOW | `UnitCalibrator.java` | Constructor | No Javadoc; missing `@param` tags |

**No inaccurate or dangerously wrong comments were found** (there are no existing comments to be inaccurate). All findings are omission-based.
