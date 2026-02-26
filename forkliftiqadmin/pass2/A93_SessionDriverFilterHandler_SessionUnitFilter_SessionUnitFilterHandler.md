# Pass 2 – Test Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A93
**Files audited:**
1. `src/main/java/com/querybuilder/filters/SessionDriverFilterHandler.java`
2. `src/main/java/com/querybuilder/filters/SessionUnitFilter.java`
3. `src/main/java/com/querybuilder/filters/SessionUnitFilterHandler.java`

---

## 1. Source File Evidence

### 1.1 SessionDriverFilterHandler.java

**Class:** `SessionDriverFilterHandler` (implements `FilterHandler`)
**Package:** `com.querybuilder.filters`

| Element | Kind | Line |
|---------|------|------|
| `filter` | field (`SessionDriverFilter`) | 8 |
| `driverIdFieldName` | field (`String`) | 9 |
| `SessionDriverFilterHandler(SessionDriverFilter, String)` | constructor | 11 |
| `getQueryFilter()` | method (`String`) | 17 |
| `prepareStatement(StatementPreparer)` | method (`void`, throws `SQLException`) | 23 |
| `ignoreFilter()` | method (`boolean`, private) | 28 |

**Behaviour notes:**
- `ignoreFilter()` returns `true` when `filter == null` OR `filter.driverId() == null`.
- `getQueryFilter()` returns `""` when `ignoreFilter()` is true; otherwise returns ` AND <driverIdFieldName> = ? `.
- `prepareStatement()` is a no-op when `ignoreFilter()` is true; otherwise calls `preparer.addLong(filter.driverId())`.

---

### 1.2 SessionUnitFilter.java

**Type:** interface
**Package:** `com.querybuilder.filters`

| Element | Kind | Line |
|---------|------|------|
| `unitId()` | abstract method (`Long`) | 4 |

**Behaviour notes:**
- Single-method interface (functional interface).
- Implemented by `SessionFilterBean` (maps `vehicleId` → `unitId()`).

---

### 1.3 SessionUnitFilterHandler.java

**Class:** `SessionUnitFilterHandler` (implements `FilterHandler`)
**Package:** `com.querybuilder.filters`

| Element | Kind | Line |
|---------|------|------|
| `filter` | field (`SessionUnitFilter`) | 8 |
| `unitIdFieldName` | field (`String`) | 9 |
| `SessionUnitFilterHandler(SessionUnitFilter, String)` | constructor | 11 |
| `getQueryFilter()` | method (`String`) | 17 |
| `prepareStatement(StatementPreparer)` | method (`void`, throws `SQLException`) | 23 |
| `ignoreFilter()` | method (`boolean`, private) | 28 |

**Behaviour notes:**
- `ignoreFilter()` returns `true` when `filter == null` OR `filter.unitId() == null`.
- `getQueryFilter()` returns `""` when `ignoreFilter()` is true; otherwise returns ` AND <unitIdFieldName> = ? `.
- `prepareStatement()` is a no-op when `ignoreFilter()` is true; otherwise calls `preparer.addLong(filter.unitId())`.

---

## 2. Test Discovery

**Grep target:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`
**Pattern searched:** `SessionDriverFilterHandler`, `SessionUnitFilter`, `SessionUnitFilterHandler`
**Result:** No matching files found.

The test directory contains only four test files, none related to the `com.querybuilder.filters` package:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

---

## 3. Coverage Gaps & Findings

### SessionDriverFilterHandler

**A93-1 | Severity: CRITICAL | No test class exists for SessionDriverFilterHandler**
`SessionDriverFilterHandler` has zero test coverage. No test class exists anywhere in the test source tree for this class or its package (`com.querybuilder.filters`). All logic paths are untested.

**A93-2 | Severity: HIGH | getQueryFilter() — "filter is null" branch not tested**
When `filter == null`, `ignoreFilter()` returns `true` and `getQueryFilter()` must return `""`. This null-filter guard is not covered by any test.

**A93-3 | Severity: HIGH | getQueryFilter() — "driverId is null" branch not tested**
When `filter` is non-null but `filter.driverId()` returns `null`, `ignoreFilter()` returns `true` and `getQueryFilter()` must return `""`. This is a distinct short-circuit path that is not covered.

**A93-4 | Severity: HIGH | getQueryFilter() — active-filter (non-null driverId) branch not tested**
When `filter.driverId()` is non-null, `getQueryFilter()` must return ` AND <driverIdFieldName> = ? `. The correctness of the format string (including surrounding spaces) is not verified by any test.

**A93-5 | Severity: HIGH | prepareStatement() — "filter is null" branch not tested**
When `filter == null`, `prepareStatement()` must be a no-op (no call to `preparer.addLong()`). Not tested.

**A93-6 | Severity: HIGH | prepareStatement() — "driverId is null" branch not tested**
When `filter.driverId()` returns `null`, `prepareStatement()` must be a no-op. Not tested. Note: `StatementPreparer.addLong` accepts a primitive `long`; if the `null` guard in `ignoreFilter()` ever fails, an `NPE` would occur at unboxing.

**A93-7 | Severity: HIGH | prepareStatement() — active-filter (non-null driverId) branch not tested**
When `filter.driverId()` is non-null, `preparer.addLong()` must be called exactly once with the correct value. This is not verified.

**A93-8 | Severity: MEDIUM | Constructor field assignment not verified**
There is no test asserting that the injected `filter` and `driverIdFieldName` values are correctly stored and subsequently used in query generation.

---

### SessionUnitFilter

**A93-9 | Severity: LOW | Interface SessionUnitFilter has no contract test**
`SessionUnitFilter` is a single-method interface. No test verifies that its sole contract method (`unitId()`) is correctly implemented by any concrete class (e.g., `SessionFilterBean`). While interface-level testing is optional, the mapping in `SessionFilterBean` (`vehicleId` → `unitId()`) represents a non-obvious field rename that warrants explicit coverage.

---

### SessionUnitFilterHandler

**A93-10 | Severity: CRITICAL | No test class exists for SessionUnitFilterHandler**
`SessionUnitFilterHandler` has zero test coverage. No test class exists anywhere in the test source tree for this class. All logic paths are untested.

**A93-11 | Severity: HIGH | getQueryFilter() — "filter is null" branch not tested**
When `filter == null`, `ignoreFilter()` returns `true` and `getQueryFilter()` must return `""`. Not tested.

**A93-12 | Severity: HIGH | getQueryFilter() — "unitId is null" branch not tested**
When `filter` is non-null but `filter.unitId()` returns `null`, `ignoreFilter()` returns `true` and `getQueryFilter()` must return `""`. Not tested.

**A93-13 | Severity: HIGH | getQueryFilter() — active-filter (non-null unitId) branch not tested**
When `filter.unitId()` is non-null, `getQueryFilter()` must return ` AND <unitIdFieldName> = ? `. The correctness of the format string is not verified.

**A93-14 | Severity: HIGH | prepareStatement() — "filter is null" branch not tested**
When `filter == null`, `prepareStatement()` must be a no-op. Not tested.

**A93-15 | Severity: HIGH | prepareStatement() — "unitId is null" branch not tested**
When `filter.unitId()` returns `null`, `prepareStatement()` must be a no-op. Not tested. As with the driver handler, a guard failure would produce an NPE at unboxing into primitive `long`.

**A93-16 | Severity: HIGH | prepareStatement() — active-filter (non-null unitId) branch not tested**
When `filter.unitId()` is non-null, `preparer.addLong()` must be called exactly once with the correct value. Not tested.

**A93-17 | Severity: MEDIUM | Constructor field assignment not verified**
No test confirms that injected `filter` and `unitIdFieldName` values are correctly stored and used.

---

### Cross-Cutting Concerns

**A93-18 | Severity: HIGH | NPE risk on unboxing not guarded by type system**
Both handlers call `preparer.addLong(filter.driverId())` / `preparer.addLong(filter.unitId())`, where the argument is a `Long` (boxed) being unboxed to primitive `long`. The `ignoreFilter()` null check prevents NPE at runtime, but the guard and the call site are separated — a future refactor removing or loosening the guard would silently introduce an NPE. No test validates this boundary.

**A93-19 | Severity: MEDIUM | Structural duplication between SessionDriverFilterHandler and SessionUnitFilterHandler is untested**
The two handler classes are structurally identical except for the injected interface and field name. There are no tests that would catch a regression if the logic between them diverged unintentionally.

**A93-20 | Severity: INFO | com.querybuilder.filters package has no test coverage whatsoever**
The entire `com.querybuilder.filters` package (which also includes `DateBetweenFilterHandler`, `ImpactLevelFilterHandler`, `StringContainingFilterHandler`, `UnitManufactureFilterHandler`, `UnitTypeFilterHandler`) has no test coverage. The three files under audit are consistent with a broader gap across the package.

---

## 4. Summary Table

| Finding | Severity | Class |
|---------|----------|-------|
| A93-1 | CRITICAL | SessionDriverFilterHandler |
| A93-2 | HIGH | SessionDriverFilterHandler |
| A93-3 | HIGH | SessionDriverFilterHandler |
| A93-4 | HIGH | SessionDriverFilterHandler |
| A93-5 | HIGH | SessionDriverFilterHandler |
| A93-6 | HIGH | SessionDriverFilterHandler |
| A93-7 | HIGH | SessionDriverFilterHandler |
| A93-8 | MEDIUM | SessionDriverFilterHandler |
| A93-9 | LOW | SessionUnitFilter |
| A93-10 | CRITICAL | SessionUnitFilterHandler |
| A93-11 | HIGH | SessionUnitFilterHandler |
| A93-12 | HIGH | SessionUnitFilterHandler |
| A93-13 | HIGH | SessionUnitFilterHandler |
| A93-14 | HIGH | SessionUnitFilterHandler |
| A93-15 | HIGH | SessionUnitFilterHandler |
| A93-16 | HIGH | SessionUnitFilterHandler |
| A93-17 | MEDIUM | SessionUnitFilterHandler |
| A93-18 | HIGH | Both handlers |
| A93-19 | MEDIUM | Both handlers |
| A93-20 | INFO | Package-wide |

**Totals:** 2 CRITICAL, 12 HIGH, 4 MEDIUM, 1 LOW, 1 INFO
