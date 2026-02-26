# Pass 3 Documentation Audit — Agent A95

**Audit run:** 2026-02-26-01
**Agent:** A95
**Files audited:**
- `querybuilder/filters/UnitTypeFilterHandler.java`
- `querybuilder/impacts/ImpactsByCompanyIdQuery.java`
- `querybuilder/impacts/ImpactsCountByCompanyIdQuery.java`

---

## File 1: `UnitTypeFilterHandler.java`

**Full path:** `src/main/java/com/querybuilder/filters/UnitTypeFilterHandler.java`

### Reading Evidence

| Element | Kind | Line |
|---------|------|------|
| `UnitTypeFilterHandler` | class | 7 |
| `filter` | field — `final UnitTypeFilter` | 8 |
| `fieldName` | field — `final String` | 9 |
| `UnitTypeFilterHandler(UnitTypeFilter, String)` | constructor (public) | 11 |
| `getQueryFilter()` | method (public, `@Override`) | 17 |
| `prepareStatement(StatementPreparer)` | method (public, `@Override`) | 23 |
| `ignoreFilter()` | method (private) | 28 |

### Javadoc Analysis

**Class-level Javadoc:** None.

**Method-level Javadoc:**

| Method | Has Javadoc |
|--------|-------------|
| `UnitTypeFilterHandler(UnitTypeFilter, String)` | No |
| `getQueryFilter()` | No |
| `prepareStatement(StatementPreparer)` | No |
| `ignoreFilter()` | No (private — not required) |

### Findings

**A95-1** [LOW] `UnitTypeFilterHandler` (line 7) has no class-level Javadoc. There is no description of the class's purpose: implementing `FilterHandler` to constrain queries by unit type, producing an SQL fragment `AND <fieldName> = ?` and binding the corresponding long parameter.

**A95-2** [MEDIUM] `getQueryFilter()` (line 17) is a public, non-trivial method with no Javadoc. It conditionally returns an empty string when the filter should be ignored, or a parameterised SQL fragment `AND <fieldName> = ?`. The conditional logic and the side-effect on parameter binding order are important contracts that callers need to understand.

**A95-3** [MEDIUM] `prepareStatement(StatementPreparer preparer)` (line 23) is a public, non-trivial method with no Javadoc. It conditionally binds `filter.type()` as a `Long` via `preparer.addLong()`, and silently does nothing when the filter is to be ignored. The coupling between `getQueryFilter()` and `prepareStatement()` (both must agree on whether to act) is a non-obvious contract that warrants documentation.

**A95-4** [LOW] Constructor `UnitTypeFilterHandler(UnitTypeFilter, String)` (line 11) has no Javadoc. As a public constructor, a minimal description of the `filter` and `fieldName` parameters would be appropriate (e.g. explaining that `fieldName` is the SQL column name to filter on).

---

## File 2: `ImpactsByCompanyIdQuery.java`

**Full path:** `src/main/java/com/querybuilder/impacts/ImpactsByCompanyIdQuery.java`

### Reading Evidence

| Element | Kind | Line |
|---------|------|------|
| `ImpactsByCompanyIdQuery` | class | 5 |
| `BASE_QUERY` | field — `static final String` | 6 |
| `COUNT_QUERY` | field — `static final String` | 13 |
| `REPORT_QUERY` | field — `static final String` | 18 |
| `report(long, ImpactReportFilterBean)` | method (public static) | 23 |
| `count(long, String)` | method (public static) | 27 |

### Javadoc Analysis

**Class-level Javadoc:** None.

**Method-level Javadoc:**

| Method | Has Javadoc |
|--------|-------------|
| `report(long, ImpactReportFilterBean)` | No |
| `count(long, String)` | No |

### Findings

**A95-5** [LOW] `ImpactsByCompanyIdQuery` (line 5) has no class-level Javadoc. The class acts as a factory/namespace for two query-building entry points (`report` and `count`) and centralises the shared SQL base query for impacts filtered by company ID. This structural role is not documented anywhere.

**A95-6** [MEDIUM] `report(long companyId, ImpactReportFilterBean filter)` (line 23) is a public static factory method with no Javadoc. It is non-trivial: it creates an `ImpactsReportByCompanyIdQuery` that uses `REPORT_QUERY` (which includes a `%s` placeholder for additional filters and an `ORDER BY impact_time DESC` clause). No `@param` tags for `companyId` or `filter`, and no `@return` tag explaining the returned query object.

**A95-7** [MEDIUM] `count(long companyId, String timezone)` (line 27) is a public static factory method with no Javadoc. It creates an `ImpactsCountByCompanyIdQuery` that counts distinct impacts for today in the specified timezone. The `timezone` parameter's role — driving timezone-based date comparison in the SQL — is non-obvious and undocumented. No `@param` or `@return` tags.

**A95-8** [LOW] Package-private fields `COUNT_QUERY` (line 13) and `REPORT_QUERY` (line 18) are used by sibling classes (`ImpactsCountByCompanyIdQuery`, `ImpactsReportByCompanyIdQuery`). They have no comments explaining the structure of each query, particularly the `%s` format placeholder in `REPORT_QUERY` (line 20) which represents injected filter clauses. This is not a public API concern but represents a maintenance risk.

---

## File 3: `ImpactsCountByCompanyIdQuery.java`

**Full path:** `src/main/java/com/querybuilder/impacts/ImpactsCountByCompanyIdQuery.java`

### Reading Evidence

| Element | Kind | Line |
|---------|------|------|
| `ImpactsCountByCompanyIdQuery` | class | 8 |
| `companyId` | field — `final long` | 9 |
| `timezone` | field — `final String` | 10 |
| `ImpactsCountByCompanyIdQuery(long, String)` | constructor (package-private) | 12 |
| `query()` | method (public) | 17 |
| `prepareStatement(PreparedStatement)` | method (private) | 23 |

### Javadoc Analysis

**Class-level Javadoc:** None.

**Method-level Javadoc:**

| Method | Has Javadoc |
|--------|-------------|
| `ImpactsCountByCompanyIdQuery(long, String)` | No (package-private — lower priority) |
| `query()` | No |
| `prepareStatement(PreparedStatement)` | No (private — not required) |

### Findings

**A95-9** [LOW] `ImpactsCountByCompanyIdQuery` (line 8) has no class-level Javadoc. The class is package-private in construction but exposes a public `query()` method. Its purpose — executing a count of distinct impacts for a company on the current day in a given timezone — is entirely undocumented.

**A95-10** [MEDIUM] `query()` (line 17) is a public, non-trivial method with no Javadoc. It executes `COUNT_QUERY` (defined in `ImpactsByCompanyIdQuery`) and returns the integer count, defaulting to `0` via `orElse(0)` if no result is returned. The `throws SQLException` declaration and the default-zero behaviour are important contracts for callers that are entirely undocumented. Missing `@return` and `@throws` tags.

**A95-11** [LOW] `prepareStatement(PreparedStatement)` (line 23) binds `companyId` twice (positions 1 and 2) and `timezone` twice (positions 3 and 4), mirroring the four `?` placeholders in `COUNT_QUERY`. This repetition is a consequence of the SQL structure in `ImpactsByCompanyIdQuery` (company ID appears in both `vi.comp_id = ?` and `uc.company_id = ?`; timezone appears for both the impact timestamp and `now()`). While private, an inline comment explaining this binding pattern would reduce maintenance risk and is currently absent.

---

## Summary Table

| ID | File | Element | Line | Severity | Description |
|----|------|---------|------|----------|-------------|
| A95-1 | UnitTypeFilterHandler.java | class `UnitTypeFilterHandler` | 7 | LOW | No class-level Javadoc |
| A95-2 | UnitTypeFilterHandler.java | `getQueryFilter()` | 17 | MEDIUM | Undocumented non-trivial public method |
| A95-3 | UnitTypeFilterHandler.java | `prepareStatement(StatementPreparer)` | 23 | MEDIUM | Undocumented non-trivial public method; implicit coupling with `getQueryFilter()` undocumented |
| A95-4 | UnitTypeFilterHandler.java | constructor | 11 | LOW | Undocumented public constructor; no @param tags |
| A95-5 | ImpactsByCompanyIdQuery.java | class `ImpactsByCompanyIdQuery` | 5 | LOW | No class-level Javadoc |
| A95-6 | ImpactsByCompanyIdQuery.java | `report(long, ImpactReportFilterBean)` | 23 | MEDIUM | Undocumented non-trivial public static factory method; no @param/@return |
| A95-7 | ImpactsByCompanyIdQuery.java | `count(long, String)` | 27 | MEDIUM | Undocumented non-trivial public static factory method; timezone role not described; no @param/@return |
| A95-8 | ImpactsByCompanyIdQuery.java | `COUNT_QUERY`, `REPORT_QUERY` fields | 13, 18 | LOW | No comments on package-private SQL constants; `%s` placeholder in `REPORT_QUERY` unexplained |
| A95-9 | ImpactsCountByCompanyIdQuery.java | class `ImpactsCountByCompanyIdQuery` | 8 | LOW | No class-level Javadoc |
| A95-10 | ImpactsCountByCompanyIdQuery.java | `query()` | 17 | MEDIUM | Undocumented non-trivial public method; default-zero behaviour and `throws SQLException` undocumented; no @return/@throws |
| A95-11 | ImpactsCountByCompanyIdQuery.java | `prepareStatement(PreparedStatement)` | 23 | LOW | Private method; duplicate parameter binding unexplained via inline comment |

**Totals:** 5 MEDIUM, 6 LOW, 0 HIGH
