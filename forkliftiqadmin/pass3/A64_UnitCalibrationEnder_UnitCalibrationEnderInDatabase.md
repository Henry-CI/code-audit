# Pass 3 Documentation Audit — A64
**Audit run:** 2026-02-26-01
**Agent:** A64
**Files:**
- `calibration/UnitCalibrationEnder.java`
- `calibration/UnitCalibrationEnderInDatabase.java`

---

## Reading Evidence

### File 1: `UnitCalibrationEnder.java`

| Element | Kind | Line |
|---|---|---|
| `UnitCalibrationEnder` | interface | 5 |
| `endCalibration(long unitId, int newThreshold)` | method (public, abstract) | 6 |

**Fields:** none

---

### File 2: `UnitCalibrationEnderInDatabase.java`

| Element | Kind | Line |
|---|---|---|
| `UnitCalibrationEnderInDatabase` | class (public) | 7 |
| `endCalibration(long unitId, int newThreshold)` | method (public, @Override) | 9 |

**Fields:** none

**Method body summary (`endCalibration`):**
- Constructs a SQL `UPDATE` statement that sets `impact_threshold`, `alert_enabled = TRUE`, and `calibration_date = NOW()` on the `unit` row matching the given `id`.
- Delegates execution to `DBUtil.updateObject(query, statementSetter)`.

---

## Findings

### A64-1 — LOW: No class-level Javadoc on interface `UnitCalibrationEnder`

**File:** `calibration/UnitCalibrationEnder.java`, line 5

The `UnitCalibrationEnder` interface has no `/** ... */` block above its declaration. A brief description of what "ending a calibration" means (persisting the final threshold, re-enabling alerts, recording the calibration date) would aid maintainers.

---

### A64-2 — MEDIUM: Undocumented non-trivial public method `endCalibration` on interface `UnitCalibrationEnder`

**File:** `calibration/UnitCalibrationEnder.java`, line 6

```java
void endCalibration(long unitId, int newThreshold) throws SQLException;
```

No Javadoc is present. The method is non-trivial: it commits the result of a calibration session by updating the unit record in the database. Both parameters and the checked exception need description. Missing tags: `@param unitId`, `@param newThreshold`, `@throws SQLException`.

---

### A64-3 — LOW: No class-level Javadoc on `UnitCalibrationEnderInDatabase`

**File:** `calibration/UnitCalibrationEnderInDatabase.java`, line 7

The public class `UnitCalibrationEnderInDatabase` has no `/** ... */` block above its declaration. A sentence noting that this is the database-backed implementation of `UnitCalibrationEnder`, and which table it writes to (`unit`), would clarify its role.

---

### A64-4 — MEDIUM: Undocumented non-trivial public method `endCalibration` on `UnitCalibrationEnderInDatabase`

**File:** `calibration/UnitCalibrationEnderInDatabase.java`, lines 9–18

```java
@Override
public void endCalibration(long unitId, int newThreshold) throws SQLException {
    String query = "UPDATE unit SET impact_threshold = ?, " +
            "alert_enabled = TRUE, " +
            "calibration_date = NOW() " +
            "WHERE id = ?";
    DBUtil.updateObject(query, statement -> {
        statement.setInt(1, newThreshold);
        statement.setLong(2, unitId);
    });
}
```

No Javadoc is present on the concrete implementation. The method performs three distinct side-effects: persisting the new threshold, re-enabling alerts, and stamping the calibration date. These are not obvious from the method signature alone. Missing tags: `@param unitId`, `@param newThreshold`, `@throws SQLException`.

---

## Summary Table

| ID | Severity | File | Line | Description |
|---|---|---|---|---|
| A64-1 | LOW | `UnitCalibrationEnder.java` | 5 | No class-level Javadoc on interface |
| A64-2 | MEDIUM | `UnitCalibrationEnder.java` | 6 | No Javadoc on non-trivial public method `endCalibration` (interface declaration) |
| A64-3 | LOW | `UnitCalibrationEnderInDatabase.java` | 7 | No class-level Javadoc on implementation class |
| A64-4 | MEDIUM | `UnitCalibrationEnderInDatabase.java` | 9 | No Javadoc on non-trivial public method `endCalibration` (concrete implementation) |
