# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A95
**Date:** 2026-02-26

## Source Files Audited
1. `src/main/java/com/querybuilder/filters/UnitTypeFilter.java`
2. `src/main/java/com/querybuilder/filters/UnitTypeFilterHandler.java`
3. `src/main/java/com/querybuilder/impacts/ImpactsByCompanyIdQuery.java`

**Test directory searched:** `src/test/java/`

---

## Reading Evidence

### 1. UnitTypeFilter.java

**Class/Interface name:** `UnitTypeFilter` (interface)
**Package:** `com.querybuilder.filters`

| Element | Kind | Line |
|---------|------|------|
| `type()` | method (abstract) | 4 |

**Notes:** Marker interface with a single abstract method returning `Long`. Implemented by `ReportFilterBean` (and therefore `ImpactReportFilterBean`). No fields declared.

---

### 2. UnitTypeFilterHandler.java

**Class/Interface name:** `UnitTypeFilterHandler`
**Package:** `com.querybuilder.filters`
**Implements:** `FilterHandler`

| Element | Kind | Line |
|---------|------|------|
| `filter` | field (`private final UnitTypeFilter`) | 8 |
| `fieldName` | field (`private final String`) | 9 |
| `UnitTypeFilterHandler(UnitTypeFilter filter, String fieldName)` | constructor | 11 |
| `getQueryFilter()` | method (`@Override`) | 17 |
| `prepareStatement(StatementPreparer preparer)` | method (`@Override`) | 23 |
| `ignoreFilter()` | method (`private`) | 28 |

**Branching logic observed:**
- `ignoreFilter()`: returns `true` when `filter == null` OR `filter.type() == null`; returns `false` otherwise.
- `getQueryFilter()`: returns `""` when `ignoreFilter()` is `true`; returns `" AND %s = ? "` (formatted with `fieldName`) otherwise.
- `prepareStatement()`: is a no-op when `ignoreFilter()` is `true`; calls `preparer.addLong(filter.type())` otherwise.

---

### 3. ImpactsByCompanyIdQuery.java

**Class/Interface name:** `ImpactsByCompanyIdQuery`
**Package:** `com.querybuilder.impacts`

| Element | Kind | Line |
|---------|------|------|
| `BASE_QUERY` | field (`private static final String`) | 6 |
| `COUNT_QUERY` | field (`static final String`) | 13 |
| `REPORT_QUERY` | field (`static final String`) | 18 |
| `report(long companyId, ImpactReportFilterBean filter)` | method (`public static`) | 23 |
| `count(long companyId, String timezone)` | method (`public static`) | 27 |

**SQL constants observed:**
- `BASE_QUERY`: Joins `v_impacts`, `unit_company`, and `company`; WHERE clause filters by `vi.comp_id = ?` OR `uc.company_id = ?`, and enforces `unit_threshold != 0 AND impact_value >= unit_threshold`. Date-range join condition on `uc.start_date` / `uc.end_date` uses a potential whitespace defect (see findings).
- `COUNT_QUERY`: Prepends `SELECT COUNT(DISTINCT(impact_id))` to `BASE_QUERY`; appends a timezone-aware today-date filter.
- `REPORT_QUERY`: Prepends `SELECT vi.*, c.name AS assigned_company_name` to `BASE_QUERY`; includes a `%s` placeholder for dynamic `FilterHandler`-generated WHERE clauses; appends `ORDER BY impact_time DESC`.

**Delegation:**
- `report(...)` constructs `ImpactsReportByCompanyIdQuery`.
- `count(...)` constructs `ImpactsCountByCompanyIdQuery`.

---

## Test Coverage Search Results

| Class | Test files found |
|-------|-----------------|
| `UnitTypeFilter` | None |
| `UnitTypeFilterHandler` | None |
| `ImpactsByCompanyIdQuery` | None |

The entire test directory contains only four test files:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None reference any of the three audited classes.

---

## Findings

### UnitTypeFilter

**A95-1 | Severity: LOW | Interface `UnitTypeFilter` has no test for contract compliance**
`UnitTypeFilter` is a single-method interface (`type()` returning `Long`). There are no tests verifying that its implementing classes honour the contract — specifically that `type()` returns `null` when no unit type is selected and returns the stored `Long` when one is. The primary implementation is `ReportFilterBean.type()` which simply delegates to the `typeId` field; while trivial, a null-return path exists and is relied upon by `UnitTypeFilterHandler.ignoreFilter()`. Without tests, any future refactor of `ReportFilterBean` could silently break the null-semantics contract.

---

### UnitTypeFilterHandler

**A95-2 | Severity: CRITICAL | `UnitTypeFilterHandler` has zero test coverage**
`UnitTypeFilterHandler` is not referenced in any test file. The class contains non-trivial conditional logic (`ignoreFilter()`) that controls both SQL fragment generation and parameter binding. A defect in this class could silently omit or incorrectly append filter clauses to live queries, returning wrong result sets to the UI without any runtime exception.

**A95-3 | Severity: HIGH | No test for `getQueryFilter()` when filter is null**
The `ignoreFilter()` guard short-circuits when `filter == null`. The branch where the constructor receives a `null` `UnitTypeFilter` reference — causing `getQueryFilter()` to return `""` — is completely untested. If a caller mistakenly passes `null`, no filter is applied and all records matching the base criteria are returned.

**A95-4 | Severity: HIGH | No test for `getQueryFilter()` when `filter.type()` is null**
The branch where `filter` is non-null but `filter.type()` returns `null` is also untested. This is the normal "no unit-type selected" path that should produce no SQL fragment. A regression here could cause a `NullPointerException` inside `preparer.addLong(filter.type())` (auto-unboxing a null `Long`) if the guard is ever accidentally removed or misordered.

**A95-5 | Severity: HIGH | No test for `getQueryFilter()` when a valid type is present**
The active-filter branch — where `filter.type()` returns a non-null `Long` — is untested. This branch produces the SQL fragment `" AND %s = ? "` with `fieldName` substituted in. There is no test confirming that the returned string uses the correct format (leading/trailing spaces, exact `= ?` syntax) or that `fieldName` is embedded correctly.

**A95-6 | Severity: HIGH | No test for `prepareStatement()` parameter binding**
When `filter.type()` is non-null, `prepareStatement()` calls `preparer.addLong(filter.type())`. There is no test verifying that the correct `Long` value is bound to the preparer. A subtle mutation (e.g., passing the wrong value, binding twice, or not binding at all) would be undetected.

**A95-7 | Severity: MEDIUM | No test for `prepareStatement()` no-op branch**
When `ignoreFilter()` returns `true`, `prepareStatement()` is a no-op and must not advance the `StatementPreparer` index. There is no test asserting that calling `prepareStatement()` on an ignored filter leaves the preparer in an unchanged state, which is critical for the positional parameter ordering relied upon by callers.

**A95-8 | Severity: MEDIUM | `fieldName` is never validated — no test for empty or malformed field name**
The constructor accepts any `String` as `fieldName` without null or blank checks. If an empty string or a SQL-special string is passed, `getQueryFilter()` silently produces a malformed WHERE clause (e.g., `" AND  = ? "`). No test exercises this path.

---

### ImpactsByCompanyIdQuery

**A95-9 | Severity: CRITICAL | `ImpactsByCompanyIdQuery` has zero test coverage**
Neither the factory class nor its delegate classes (`ImpactsReportByCompanyIdQuery`, `ImpactsCountByCompanyIdQuery`) are referenced in any test. All SQL string constants and the factory methods are completely uncovered.

**A95-10 | Severity: CRITICAL | SQL string `BASE_QUERY` has a missing space causing a concatenation defect**
At line 7-8, `BASE_QUERY` is assembled as:
```java
"FROM v_impacts vi " +
"LEFT JOIN unit_company uc ON uc.unit_id = vi.unit_id AND" +
"  uc.start_date <= vi.impact_time AND ...
```
The string `"AND"` at the end of line 7 is immediately concatenated with `"  uc.start_date"` from line 8. The result is `"...vi.unit_id AND  uc.start_date..."` which, while functional due to the double space, is fragile. More critically, the `"AND"` keyword at the end of the join-condition line is not separated from `"LEFT JOIN"` by whitespace if ever restructured. No test validates the rendered SQL string, so this defect is invisible without manual inspection.

**A95-11 | Severity: HIGH | `COUNT_QUERY` string constant is untested**
`COUNT_QUERY` is a package-private constant that concatenates `BASE_QUERY` with a timezone-aware date comparison. No test asserts the correct final SQL text, the number of bind parameters (four: `companyId`, `companyId`, `timezone`, `timezone`), or the `COUNT(DISTINCT(impact_id))` projection.

**A95-12 | Severity: HIGH | `REPORT_QUERY` string constant is untested**
`REPORT_QUERY` is a package-private constant containing a `%s` placeholder that is filled at runtime by joining `FilterHandler.getQueryFilter()` outputs. No test validates the base SQL text, the correct number of mandatory bind parameters before the dynamic filters (two: `companyId`, `companyId`), or the `ORDER BY impact_time DESC` clause.

**A95-13 | Severity: HIGH | No test for `report()` factory method — filter chain composition untested**
`ImpactsByCompanyIdQuery.report(companyId, filter)` constructs an `ImpactsReportByCompanyIdQuery` with a hard-coded list of four `FilterHandler` instances, including `UnitTypeFilterHandler`. No test verifies that: (a) the correct handlers are registered, (b) they appear in the correct order (which determines bind-parameter position), or (c) the `UnitTypeFilterHandler` is bound to the `"type_id"` column.

**A95-14 | Severity: HIGH | No test for `count()` factory method**
`ImpactsByCompanyIdQuery.count(companyId, timezone)` constructs `ImpactsCountByCompanyIdQuery`. No test verifies the delegation or the parameter values passed to the delegate.

**A95-15 | Severity: HIGH | Duplicate `companyId` parameter binding in `COUNT_QUERY` is untested**
`COUNT_QUERY` requires `companyId` to be bound twice (positions 1 and 2) because `BASE_QUERY` contains `vi.comp_id = ? OR uc.company_id = ?`. `ImpactsCountByCompanyIdQuery.prepareStatement()` explicitly sets both `statement.setLong(1, companyId)` and `statement.setLong(2, companyId)`. There is no test confirming both bindings are correct and in the right positions.

**A95-16 | Severity: HIGH | Duplicate `timezone` parameter binding in `COUNT_QUERY` is untested**
`COUNT_QUERY` uses `timezone` twice (positions 3 and 4) in `timezone(?, now())` and `timezone(?, impact_time ...)`. `ImpactsCountByCompanyIdQuery.prepareStatement()` sets both `statement.setString(3, timezone)` and `statement.setString(4, timezone)`. No test verifies that both are bound or that their order matches the SQL.

**A95-17 | Severity: MEDIUM | No test for `report()` with a fully null filter (all fields null)**
When `ImpactReportFilterBean` has all optional fields null, each `FilterHandler` in the chain should return `""` from `getQueryFilter()` and skip parameter binding. No test verifies that `REPORT_QUERY` is rendered without any dynamic WHERE fragments in this scenario.

**A95-18 | Severity: MEDIUM | No test for `report()` with `typeId` populated — verifying `UnitTypeFilterHandler` integration**
When `ImpactReportFilterBean.typeId` is non-null, the `UnitTypeFilterHandler` (bound to `"type_id"`) must append `" AND type_id = ? "` to the query and bind the value. No integration-level test exercises this path through `ImpactsByCompanyIdQuery.report()`.

**A95-19 | Severity: MEDIUM | `BASE_QUERY` `unit_threshold != 0` condition is untested**
The hardcoded `AND unit_threshold != 0` in `BASE_QUERY` silently excludes units with a zero threshold. There is no test documenting or verifying this business-rule filter is intentional and correctly positioned in the WHERE clause.

**A95-20 | Severity: LOW | Package-private visibility of `COUNT_QUERY` and `REPORT_QUERY` limits testability**
`COUNT_QUERY` and `REPORT_QUERY` are package-private (`static final`, no explicit access modifier). While accessible to tests in the same package, no such tests exist. The constants should at minimum have their SQL text asserted in unit tests to catch accidental modification during maintenance.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 10 |
| MEDIUM | 5 |
| LOW | 2 |
| **Total** | **20** |

All three source files have **zero test coverage**. The most critical gaps are the complete absence of tests for `UnitTypeFilterHandler`'s conditional branching logic (which directly controls SQL generation and parameter binding) and `ImpactsByCompanyIdQuery`'s SQL string composition and factory delegation, including a structural SQL concatenation defect in `BASE_QUERY` that is only visible through string-level assertion tests.
