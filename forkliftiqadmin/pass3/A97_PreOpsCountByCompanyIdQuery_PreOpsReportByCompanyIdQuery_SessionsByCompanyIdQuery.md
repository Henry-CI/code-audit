# Pass 3 Documentation Audit — Agent A97

**Audit Run:** 2026-02-26-01
**Files Audited:**
- `querybuilder/preops/PreOpsCountByCompanyIdQuery.java`
- `querybuilder/preops/PreOpsReportByCompanyIdQuery.java`
- `querybuilder/session/SessionsByCompanyIdQuery.java`

---

## File 1: PreOpsCountByCompanyIdQuery.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/preops/PreOpsCountByCompanyIdQuery.java`

### Reading Evidence

| Element | Type / Kind | Line |
|---------|-------------|------|
| `PreOpsCountByCompanyIdQuery` | class | 9 |
| `companyId` | field — `final long` | 10 |
| `timezone` | field — `final String` | 11 |
| `PreOpsCountByCompanyIdQuery(long companyId, String timezone)` | constructor (package-private) | 13 |
| `query()` | method — `public Integer throws SQLException` | 18 |
| `prepareStatement(PreparedStatement statement)` | method — `private void throws SQLException` | 24 |

### Javadoc Analysis

**Class-level Javadoc:** None present.

**Constructor `PreOpsCountByCompanyIdQuery(long, String)` (line 13):** Package-private; no Javadoc present.

**`query()` (line 18) — public, non-trivial:**
- No Javadoc present.
- Executes a COUNT query against `PreOpsByCompanyIdQuery.COUNT_QUERY`, binding `companyId` three times and `timezone` once, then returns the first column as an `Integer`, defaulting to `0` if no row is returned.

**`prepareStatement(PreparedStatement)` (line 24) — private:** Not subject to public-method Javadoc requirement.

### Findings

| ID | Severity | Location | Description |
|----|----------|----------|-------------|
| A97-1 | LOW | `PreOpsCountByCompanyIdQuery`, line 9 | No class-level Javadoc. The class purpose (counting pre-ops check records for a given company, scoped by timezone) is not documented. |
| A97-2 | MEDIUM | `query()`, line 18 | No Javadoc on public non-trivial method. The method executes a database COUNT query and returns a result; callers have no documentation about what is counted, what `0` means as a default, or that `SQLException` may be thrown. Missing `@return` and `@throws` tags. |

---

## File 2: PreOpsReportByCompanyIdQuery.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/preops/PreOpsReportByCompanyIdQuery.java`

### Reading Evidence

| Element | Type / Kind | Line |
|---------|-------------|------|
| `PreOpsReportByCompanyIdQuery` | class | 22 |
| `companyId` | field — `final long` | 23 |
| `filterHandlers` | field — `List<FilterHandler>` | 24 |
| `PreOpsReportByCompanyIdQuery(long companyId, PreOpsReportFilterBean filter)` | constructor (package-private) | 26 |
| `query(String timezone, String dateFormat)` | method — `public PreOpsReportBean throws SQLException` | 35 |
| `getQuery()` | method — `private String` | 41 |
| `prepareStatement(PreparedStatement statement)` | method — `private void throws SQLException` | 47 |
| `getResults(String timezone, String dateFormat, ResultSet rs)` | method — `private List<PreOpsReportEntryBean> throws SQLException` | 55 |

### Javadoc Analysis

**Class-level Javadoc:** None present.

**Constructor `PreOpsReportByCompanyIdQuery(long, PreOpsReportFilterBean)` (line 26):** Package-private; no Javadoc present.

**`query(String timezone, String dateFormat)` (line 35) — public, non-trivial:**
- No Javadoc present.
- Executes a dynamically filtered SQL report query, maps each result-set row into `PreOpsReportEntryBean` objects (grouping rows by `result_id` to accumulate failure answers), and returns the aggregated collection wrapped in a `PreOpsReportBean`.

**`getQuery()`, `prepareStatement()`, `getResults()` — private:** Not subject to public-method Javadoc requirement.

### Findings

| ID | Severity | Location | Description |
|----|----------|----------|-------------|
| A97-3 | LOW | `PreOpsReportByCompanyIdQuery`, line 22 | No class-level Javadoc. The class purpose (building and executing a filtered pre-ops report query for a specific company) is not documented. |
| A97-4 | MEDIUM | `query(String, String)`, line 35 | No Javadoc on public non-trivial method. The method applies dynamic filters, executes a database query, performs grouped result-set mapping, and returns a `PreOpsReportBean`. Callers have no documentation on parameter semantics, expected `timezone` or `dateFormat` values, the structure of the returned bean, or the declared `SQLException`. Missing `@param`, `@return`, and `@throws` tags. |

---

## File 3: SessionsByCompanyIdQuery.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java`

### Reading Evidence

| Element | Type / Kind | Line |
|---------|-------------|------|
| `SessionsByCompanyIdQuery` | class | 17 |
| `companyId` | field — `int` | 18 |
| `filterHandlers` | field — `List<FilterHandler>` | 19 |
| `SessionsByCompanyIdQuery(int companyId, SessionFilterBean filter)` | constructor (private) | 21 |
| `query(String timezone, String dateFormat)` | method — `public SessionReportBean throws SQLException` | 30 |
| `getQuery()` | method — `private String` | 40 |
| `prepareStatement(PreparedStatement statement)` | method — `private void throws SQLException` | 50 |
| `getResults(String timezone, String dateFormat, ResultSet rs)` | method — `private SessionBean throws SQLException` | 57 |
| `report(int companyId, SessionFilterBean filter)` | method — `public static SessionsByCompanyIdQuery` | 69 |

### Javadoc Analysis

**Class-level Javadoc:** None present.

**Constructor `SessionsByCompanyIdQuery(int, SessionFilterBean)` (line 21):** Private; not subject to public-method Javadoc requirement.

**`query(String timezone, String dateFormat)` (line 30) — public, non-trivial:**
- No Javadoc present.
- Executes a session report query against `v_sessions` with dynamic filters applied, maps each row to a `SessionBean` (with times converted from UTC to the specified timezone and formatted), and returns the list wrapped in a `SessionReportBean`.

**`report(int companyId, SessionFilterBean filter)` (line 69) — public static, factory method:**
- No Javadoc present.
- Acts as the sole public factory method for instantiating `SessionsByCompanyIdQuery`. Without documentation, callers cannot determine the intent of `report` vs. a hypothetical alternative constructor usage.

**`getQuery()`, `prepareStatement()`, `getResults()` — private:** Not subject to public-method Javadoc requirement.

### Findings

| ID | Severity | Location | Description |
|----|----------|----------|-------------|
| A97-5 | LOW | `SessionsByCompanyIdQuery`, line 17 | No class-level Javadoc. The class purpose (querying session records for a given company with optional filters) is not documented. |
| A97-6 | MEDIUM | `query(String, String)`, line 30 | No Javadoc on public non-trivial method. The method executes a filtered database query and maps rows to session beans with UTC-to-local timezone conversion. Missing `@param`, `@return`, and `@throws` tags. |
| A97-7 | MEDIUM | `report(int, SessionFilterBean)`, line 69 | No Javadoc on public static factory method. This is the only entry point for constructing instances; its purpose, parameters, and return value are undocumented. Missing `@param` tags for `companyId` and `filter`, and a `@return` tag. |

---

## Summary Table

| ID | File | Line | Severity | Description |
|----|------|------|----------|-------------|
| A97-1 | `PreOpsCountByCompanyIdQuery.java` | 9 | LOW | No class-level Javadoc |
| A97-2 | `PreOpsCountByCompanyIdQuery.java` | 18 | MEDIUM | Undocumented public non-trivial method `query()`; missing `@return`, `@throws` |
| A97-3 | `PreOpsReportByCompanyIdQuery.java` | 22 | LOW | No class-level Javadoc |
| A97-4 | `PreOpsReportByCompanyIdQuery.java` | 35 | MEDIUM | Undocumented public non-trivial method `query(String, String)`; missing `@param`, `@return`, `@throws` |
| A97-5 | `SessionsByCompanyIdQuery.java` | 17 | LOW | No class-level Javadoc |
| A97-6 | `SessionsByCompanyIdQuery.java` | 30 | MEDIUM | Undocumented public non-trivial method `query(String, String)`; missing `@param`, `@return`, `@throws` |
| A97-7 | `SessionsByCompanyIdQuery.java` | 69 | MEDIUM | Undocumented public static factory method `report(int, SessionFilterBean)`; missing `@param`, `@return` |

**Total findings: 7** (3 LOW, 4 MEDIUM, 0 HIGH)
