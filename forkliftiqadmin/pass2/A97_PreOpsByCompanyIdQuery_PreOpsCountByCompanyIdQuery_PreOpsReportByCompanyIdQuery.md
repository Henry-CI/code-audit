# Pass 2 — Test Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A97
**Files audited:**
1. `src/main/java/com/querybuilder/preops/PreOpsByCompanyIdQuery.java`
2. `src/main/java/com/querybuilder/preops/PreOpsCountByCompanyIdQuery.java`
3. `src/main/java/com/querybuilder/preops/PreOpsReportByCompanyIdQuery.java`

---

## Section 1 — Reading Evidence

### 1.1 PreOpsByCompanyIdQuery

**Class name:** `PreOpsByCompanyIdQuery`
**Package:** `com.querybuilder.preops`

**Fields:**

| Field | Modifier | Type | Line |
|---|---|---|---|
| `BASE_QUERY` | `private static final` | `String` | 6–7 |
| `COUNT_QUERY` | `static final` | `String` | 9–11 |
| `REPORT_QUERY` | `static final` | `String` | 13–14 |

**Methods:**

| Method | Signature | Line |
|---|---|---|
| `report` | `public static PreOpsReportByCompanyIdQuery report(long companyId, PreOpsReportFilterBean filter)` | 16–18 |
| `count` | `public static PreOpsCountByCompanyIdQuery count(long companyId, String timezone)` | 20–22 |

**SQL constants (verbatim):**

- `BASE_QUERY` (line 6–7):
  ```sql
  FROM v_preops_report WHERE (comp_id = ? OR assigned_company_id = ? OR unit_company_id = ?)
  ```
- `COUNT_QUERY` (line 9–11):
  ```sql
  SELECT COUNT(DISTINCT(result_id)) FROM v_preops_report WHERE (comp_id = ? OR assigned_company_id = ? OR unit_company_id = ?)
  AND timezone(?, check_date_time at time zone 'UTC')::DATE = current_date::DATE
  ```
- `REPORT_QUERY` (line 13–14):
  ```sql
  SELECT * FROM v_preops_report WHERE (comp_id = ? OR assigned_company_id = ? OR unit_company_id = ?) %s ORDER BY result_id
  ```
  (`%s` is a `String.format` placeholder for dynamic filter clauses.)

---

### 1.2 PreOpsCountByCompanyIdQuery

**Class name:** `PreOpsCountByCompanyIdQuery`
**Package:** `com.querybuilder.preops`

**Fields:**

| Field | Modifier | Type | Line |
|---|---|---|---|
| `companyId` | `private final` | `long` | 10 |
| `timezone` | `private final` | `String` | 11 |

**Methods:**

| Method | Modifier | Signature | Line |
|---|---|---|---|
| `PreOpsCountByCompanyIdQuery` (constructor) | package-private | `PreOpsCountByCompanyIdQuery(long companyId, String timezone)` | 13–16 |
| `query` | `public` | `Integer query() throws SQLException` | 18–22 |
| `prepareStatement` | `private` | `void prepareStatement(PreparedStatement statement) throws SQLException` | 24–30 |

**Parameter binding in `prepareStatement` (lines 25–29):**
- Parameter 1: `companyId` (Long) — binds to `comp_id = ?`
- Parameter 2: `companyId` (Long) — binds to `assigned_company_id = ?`
- Parameter 3: `companyId` (Long) — binds to `unit_company_id = ?`
- Parameter 4: `timezone` (String) — binds to the `timezone(?, ...)` function call

---

### 1.3 PreOpsReportByCompanyIdQuery

**Class name:** `PreOpsReportByCompanyIdQuery`
**Package:** `com.querybuilder.preops`

**Fields:**

| Field | Modifier | Type | Line |
|---|---|---|---|
| `companyId` | `private final` | `long` | 23 |
| `filterHandlers` | `private` | `List<FilterHandler>` | 24 |

**Methods:**

| Method | Modifier | Signature | Line |
|---|---|---|---|
| `PreOpsReportByCompanyIdQuery` (constructor) | package-private | `PreOpsReportByCompanyIdQuery(long companyId, PreOpsReportFilterBean filter)` | 26–33 |
| `query` | `public` | `PreOpsReportBean query(String timezone, String dateFormat) throws SQLException` | 35–39 |
| `getQuery` | `private` | `String getQuery()` | 41–45 |
| `prepareStatement` | `private` | `void prepareStatement(PreparedStatement statement) throws SQLException` | 47–53 |
| `getResults` | `private` | `List<PreOpsReportEntryBean> getResults(String timezone, String dateFormat, ResultSet rs) throws SQLException` | 55–85 |

**Filter handlers initialised in constructor (lines 28–32):**
- `DateBetweenFilterHandler(filter, "check_date_time")`
- `UnitManufactureFilterHandler(filter, "manu_id")`
- `UnitTypeFilterHandler(filter, "type_id")`

**`getResults` row-assembly logic (lines 55–85):**
- Groups rows by `result_id`; when a new `result_id` is encountered, finalises the previous `PreOpsReportEntryBean` and begins a new one.
- Columns read from `ResultSet`: `result_id`, `unit_name`, `manufacture`, `assigned_company_name`, `driver_name`, `check_date_time`, `duration`, `comment`, `answer`.
- `duration` is read with `rs.getTime("duration").toLocalTime()` — no null check.
- `check_date_time` is converted via `DateUtil.utc2Local` then `DateUtil.formatDateTime`.
- `answer` is added to a `failures` list per entry.
- After the loop, the last entry is appended (lines 80–82).
- `Objects.requireNonNull(entry)` is used on line 77 (potential `NullPointerException` path if `entry` is null after the first row — logically impossible given the if-branch on line 62, but not provably safe for an empty result set entering the inner block).

---

## Section 2 — Test Coverage Search Results

**Search target:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

| Class searched | Files matched |
|---|---|
| `PreOpsByCompanyIdQuery` | **None** |
| `PreOpsCountByCompanyIdQuery` | **None** |
| `PreOpsReportByCompanyIdQuery` | **None** |
| `preops` (case-insensitive broad sweep) | **None** |
| `FilterHandler`, `DateBetweenFilterHandler`, `UnitManufactureFilterHandler`, `UnitTypeFilterHandler` | **None** |

The test suite contains only four test files:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these are related to the PreOps query builder classes.

---

## Section 3 — Findings

### A97-1 | Severity: CRITICAL | PreOpsByCompanyIdQuery — zero test coverage for factory class

`PreOpsByCompanyIdQuery` has no test class. The two static factory methods `report()` and `count()` are completely untested. These are the only public entry points into the entire PreOps query-builder subsystem. No test verifies that `report()` returns a correctly constructed `PreOpsReportByCompanyIdQuery` or that `count()` returns a correctly constructed `PreOpsCountByCompanyIdQuery`.

---

### A97-2 | Severity: CRITICAL | PreOpsCountByCompanyIdQuery — zero test coverage

`PreOpsCountByCompanyIdQuery` has no test class. The `query()` method, which executes a live database call via `DBUtil.queryForObject`, and the `prepareStatement()` parameter-binding logic are completely untested.

---

### A97-3 | Severity: CRITICAL | PreOpsReportByCompanyIdQuery — zero test coverage

`PreOpsReportByCompanyIdQuery` has no test class. The `query()` method, `getQuery()` SQL construction, `prepareStatement()` parameter binding, and `getResults()` result-set mapping are all completely untested.

---

### A97-4 | Severity: CRITICAL | COUNT_QUERY SQL constant — not tested

`PreOpsByCompanyIdQuery.COUNT_QUERY` (lines 9–11) is a package-private constant that concatenates `BASE_QUERY` with a timezone date filter. There is no test that verifies the assembled SQL string is syntactically correct, that the parameter count matches the binding calls in `PreOpsCountByCompanyIdQuery.prepareStatement()` (4 parameters: 3 × companyId + 1 × timezone), or that `current_date` comparison semantics behave correctly for the intended timezone conversion.

---

### A97-5 | Severity: CRITICAL | REPORT_QUERY SQL constant — dynamic `%s` placeholder is untested

`PreOpsByCompanyIdQuery.REPORT_QUERY` (lines 13–14) contains a `%s` format placeholder injected by `PreOpsReportByCompanyIdQuery.getQuery()`. No test verifies that the `String.format` substitution produces a valid SQL fragment under any combination of filter conditions (all filters active, no filters active, partial filters), that the parameter count produced by `getQuery()` matches what `prepareStatement()` binds, or that the resulting SQL is syntactically valid.

---

### A97-6 | Severity: HIGH | Filter composition in `getQuery()` — untested for all filter permutations

`PreOpsReportByCompanyIdQuery.getQuery()` (lines 41–45) iterates `filterHandlers` and appends each handler's `getQueryFilter()` output. No test covers: (a) the case where no filters are active and `%s` resolves to an empty string, (b) all three filters active simultaneously, (c) each individual filter active in isolation. An incorrect filter fragment could silently corrupt the SQL without being caught.

---

### A97-7 | Severity: HIGH | `prepareStatement()` parameter binding — untested for correctness

`PreOpsReportByCompanyIdQuery.prepareStatement()` (lines 47–53) binds `companyId` three times, then delegates to each `FilterHandler.prepareStatement()`. No test verifies that the parameter count and order produced by this method exactly matches the SQL placeholders in the dynamically assembled `REPORT_QUERY`. A mismatch would cause a `SQLException` at runtime that would be silent until exercised on a live path.

---

### A97-8 | Severity: HIGH | `PreOpsCountByCompanyIdQuery.prepareStatement()` parameter order — untested

`PreOpsCountByCompanyIdQuery.prepareStatement()` (lines 24–30) binds `companyId` three times then `timezone` once. No test verifies the order matches the `COUNT_QUERY` placeholder positions. If the order were ever changed in `COUNT_QUERY` without updating `prepareStatement()`, the bug would not be caught.

---

### A97-9 | Severity: HIGH | `getResults()` result-set grouping logic — untested

`PreOpsReportByCompanyIdQuery.getResults()` (lines 55–85) implements a multi-row grouping algorithm: rows sharing the same `result_id` are merged into one `PreOpsReportEntryBean`, with each row's `answer` appended to the `failures` list. Critical paths with no test coverage:
- Single result row (one `result_id`, one `answer`).
- Multiple rows for the same `result_id` (grouping merge fires correctly).
- Multiple distinct `result_id` groups in sequence.
- Empty `ResultSet` (loop body never entered; final `if (entry != null)` must not add anything).
- The last group being correctly appended after the loop ends (lines 80–82).

---

### A97-10 | Severity: HIGH | `rs.getTime("duration").toLocalTime()` — no null guard, untested

Line 73 calls `rs.getTime("duration").toLocalTime()` without a null check. If the `duration` column is `NULL` in the database, `rs.getTime()` returns `null` and the chained `.toLocalTime()` throws a `NullPointerException`. No test exercises this code path with a null duration value.

---

### A97-11 | Severity: MEDIUM | `Objects.requireNonNull(entry)` on line 77 — defensive check masks a logic assumption

`Objects.requireNonNull(entry)` on line 77 is reached every time `rs.next()` returns `true`. The only way `entry` can be `null` at that point is if the `if (prevResultId != resultId)` branch (line 62) did not execute on the very first row — which is impossible since `prevResultId` is initialised to `0` and `result_id` is expected to be a positive database ID. No test documents this invariant or verifies that a `result_id` of `0` (edge case) would not silently break grouping by colliding with the initial sentinel value.

---

### A97-12 | Severity: MEDIUM | `DateUtil.utc2Local` and `DateUtil.formatDateTime` — timezone/format conversion untested in this context

Line 72 applies `DateUtil.utc2Local(rs.getTimestamp("check_date_time"), timezone)` and then `DateUtil.formatDateTime(..., dateFormat)`. No test verifies that this chain produces the expected localised string for representative timezone and format combinations when called through `PreOpsReportByCompanyIdQuery.query()`.

---

### A97-13 | Severity: MEDIUM | `BASE_QUERY` uses OR-triple company-ID predicate — multi-identity scoping untested

`BASE_QUERY` matches rows where `comp_id = ?`, `assigned_company_id = ?`, or `unit_company_id = ?` all bound to the same `companyId` value. No test verifies that all three columns are correctly targeted, that there is no inadvertent duplication of results (the report query uses `SELECT *` without `DISTINCT`, while the count query uses `COUNT(DISTINCT(result_id))`), or that the intended data-scoping semantics are preserved.

---

### A97-14 | Severity: MEDIUM | `COUNT_QUERY` vs `REPORT_QUERY` DISTINCT semantics mismatch — untested

`COUNT_QUERY` uses `COUNT(DISTINCT(result_id))` (line 10), but `REPORT_QUERY` uses `SELECT *` (line 13) without `DISTINCT`. If a `result_id` can appear across multiple `comp_id`/`assigned_company_id`/`unit_company_id` matches, the report result set may contain duplicate rows while the count reflects deduplicated numbers. No test verifies that the count and report row-count are consistent with each other.

---

### A97-15 | Severity: LOW | Package-private constructor accessibility — untested as a design constraint

Both `PreOpsCountByCompanyIdQuery` (line 13) and `PreOpsReportByCompanyIdQuery` (line 26) have package-private constructors, enforcing that only `PreOpsByCompanyIdQuery.count()` and `PreOpsByCompanyIdQuery.report()` are used as entry points. No test documents or enforces this intended API contract (e.g., a test confirming that direct construction from outside the package is not intended).

---

### A97-16 | Severity: LOW | `query()` returns `Integer` (boxed) with `.orElse(0)` — untested zero-result behaviour

`PreOpsCountByCompanyIdQuery.query()` (line 18–22) wraps the result in an `Optional` via `DBUtil.queryForObject` and falls back to `0` via `.orElse(0)`. No test verifies the `orElse(0)` branch (i.e., when the database returns no row), nor verifies that the method signature returning boxed `Integer` rather than primitive `int` does not create unexpected null-boxing issues in calling code.

---

## Summary Table

| Finding | Severity | Category |
|---|---|---|
| A97-1 | CRITICAL | Zero test coverage — `PreOpsByCompanyIdQuery` |
| A97-2 | CRITICAL | Zero test coverage — `PreOpsCountByCompanyIdQuery` |
| A97-3 | CRITICAL | Zero test coverage — `PreOpsReportByCompanyIdQuery` |
| A97-4 | CRITICAL | SQL constant `COUNT_QUERY` not tested |
| A97-5 | CRITICAL | Dynamic SQL `REPORT_QUERY` `%s` placeholder not tested |
| A97-6 | HIGH | Filter composition permutations untested |
| A97-7 | HIGH | `prepareStatement()` parameter binding untested (report) |
| A97-8 | HIGH | `prepareStatement()` parameter order untested (count) |
| A97-9 | HIGH | `getResults()` grouping algorithm untested |
| A97-10 | HIGH | Null `duration` causes NPE — no null guard, untested |
| A97-11 | MEDIUM | `Objects.requireNonNull(entry)` sentinel-value assumption undocumented |
| A97-12 | MEDIUM | Timezone/date format conversion untested in this context |
| A97-13 | MEDIUM | OR-triple company-ID predicate scoping untested |
| A97-14 | MEDIUM | `DISTINCT` vs non-`DISTINCT` count/report mismatch untested |
| A97-15 | LOW | Package-private constructor access contract undocumented by tests |
| A97-16 | LOW | `orElse(0)` zero-result fallback untested |

**Total findings: 16**
**CRITICAL: 5 | HIGH: 5 | MEDIUM: 4 | LOW: 2**
