# Pass 3 Documentation Audit — A65
**Audit run:** 2026-02-26-01
**Agent:** A65
**Files audited:**
- `calibration/UnitCalibrationGetter.java`
- `calibration/UnitCalibrationGetterInDatabase.java`

---

## 1. Reading Evidence

### 1.1 UnitCalibrationGetter.java

| Element | Kind | Line |
|---------|------|------|
| `UnitCalibrationGetter` | interface | 6 |
| `getUnitsToCalibrate()` | public method (interface) | 7 |
| `getUnitCalibration(long unitId)` | public method (interface) | 8 |

Fields: none (interface).

### 1.2 UnitCalibrationGetterInDatabase.java

| Element | Kind | Line |
|---------|------|------|
| `UnitCalibrationGetterInDatabase` | class | 11 |
| `filter` | field — `UnitCalibrationImpactFilter` (private final) | 12 |
| `UnitCalibrationGetterInDatabase()` (constructor) | public | 14 |
| `getUnitsToCalibrate()` | public method (@Override) | 19 |
| `getUnitCalibration(long unitId)` | public method (@Override) | 32 |
| `makeUnit(ResultSet result)` | private method | 41 |
| `getImpactsForUnit(long unitId, Timestamp resetCalibrationDate)` | private method | 53 |

---

## 2. Findings

### A65-1 — UnitCalibrationGetter: no class-level Javadoc
**Severity:** LOW
**Location:** `UnitCalibrationGetter.java`, line 6
**Detail:** The `UnitCalibrationGetter` interface has no class-level (`/** ... */`) Javadoc comment. There is no description of the interface's purpose, the strategy it abstracts (fetching calibration data for units), or any notes on checked exceptions.

---

### A65-2 — UnitCalibrationGetter: `getUnitsToCalibrate()` undocumented
**Severity:** MEDIUM
**Location:** `UnitCalibrationGetter.java`, line 7
**Detail:** The public interface method `getUnitsToCalibrate()` has no Javadoc. This is a non-trivial method — it implies a filtered database query with specific business rules (e.g. only units where `impact_threshold = 0`, `alert_enabled IS FALSE`, and `reset_calibration_date IS NOT NULL`, as revealed by the implementation). None of this contract is described. Missing `@return` and `@throws SQLException`.

---

### A65-3 — UnitCalibrationGetter: `getUnitCalibration(long unitId)` undocumented
**Severity:** MEDIUM
**Location:** `UnitCalibrationGetter.java`, line 8
**Detail:** The public interface method `getUnitCalibration(long unitId)` has no Javadoc. Notably, the implementation in `UnitCalibrationGetterInDatabase` returns `null` when no record is found (via `.orElse(null)`), which is a non-obvious null-return contract callers must know about. Missing `@param unitId`, `@return` (including the null case), and `@throws SQLException`.

---

### A65-4 — UnitCalibrationGetterInDatabase: no class-level Javadoc
**Severity:** LOW
**Location:** `UnitCalibrationGetterInDatabase.java`, line 11
**Detail:** The class `UnitCalibrationGetterInDatabase` has no class-level Javadoc. There is no description that this is the database-backed implementation of `UnitCalibrationGetter`, no mention of its dependency on `UnitCalibrationImpactFilter`, and no notes about threading or lifecycle.

---

### A65-5 — UnitCalibrationGetterInDatabase: constructor undocumented
**Severity:** LOW
**Location:** `UnitCalibrationGetterInDatabase.java`, line 14
**Detail:** The public no-arg constructor has no Javadoc. While the constructor body is trivial (initialises `filter`), a brief note confirming that this constructor creates the internal filter instance would be consistent with the documentation standard. Classified LOW as trivial.

---

### A65-6 — UnitCalibrationGetterInDatabase: `getUnitsToCalibrate()` undocumented
**Severity:** MEDIUM
**Location:** `UnitCalibrationGetterInDatabase.java`, lines 18-29
**Detail:** The `@Override` of `getUnitsToCalibrate()` has no Javadoc. Per Javadoc norms, `@Override` implementations may inherit interface Javadoc, but because the interface itself has none (A65-2), there is no effective documentation anywhere in the hierarchy. The SQL query embeds significant business logic (filters on `impact_threshold = 0`, `alert_enabled IS FALSE`, `reset_calibration_date IS NOT NULL`) that is completely undocumented. Missing `@return` and `@throws SQLException`.

---

### A65-7 — UnitCalibrationGetterInDatabase: `getUnitCalibration(long unitId)` undocumented
**Severity:** MEDIUM
**Location:** `UnitCalibrationGetterInDatabase.java`, lines 31-39
**Detail:** The `@Override` of `getUnitCalibration(long unitId)` has no Javadoc. As noted in A65-3, the null-return contract (`.orElse(null)` on line 38) is particularly important and goes entirely undocumented. Missing `@param unitId`, `@return` (including null when not found), and `@throws SQLException`.

---

## 3. Summary Table

| ID | File | Location | Severity | Description |
|----|------|----------|----------|-------------|
| A65-1 | UnitCalibrationGetter.java | line 6 | LOW | No class-level Javadoc on interface |
| A65-2 | UnitCalibrationGetter.java | line 7 | MEDIUM | `getUnitsToCalibrate()` undocumented (non-trivial, no @return/@throws) |
| A65-3 | UnitCalibrationGetter.java | line 8 | MEDIUM | `getUnitCalibration()` undocumented; null-return contract not stated (no @param/@return/@throws) |
| A65-4 | UnitCalibrationGetterInDatabase.java | line 11 | LOW | No class-level Javadoc on implementing class |
| A65-5 | UnitCalibrationGetterInDatabase.java | line 14 | LOW | Public constructor undocumented (trivial) |
| A65-6 | UnitCalibrationGetterInDatabase.java | lines 18-29 | MEDIUM | `getUnitsToCalibrate()` override undocumented; no inherited Javadoc to fall back on |
| A65-7 | UnitCalibrationGetterInDatabase.java | lines 31-39 | MEDIUM | `getUnitCalibration()` override undocumented; null-return contract entirely absent |

Total findings: 7 (4 MEDIUM, 3 LOW, 0 HIGH)
