# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A96
**Date:** 2026-02-26

## Source Files Audited

1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/impacts/ImpactsCountByCompanyIdQuery.java`
2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/impacts/ImpactsReportByCompanyIdQuery.java`
3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/incidents/IncidentReportByCompanyIdQuery.java`

**Test directory searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

---

## Reading Evidence

### 1. ImpactsCountByCompanyIdQuery

**Class name:** `ImpactsCountByCompanyIdQuery`
**Package:** `com.querybuilder.impacts`

**Fields:**

| Field | Line |
|-------|------|
| `private final long companyId` | 9 |
| `private final String timezone` | 10 |

**Methods:**

| Method | Line |
|--------|------|
| `ImpactsCountByCompanyIdQuery(long companyId, String timezone)` (package-private constructor) | 12 |
| `public Integer query() throws SQLException` | 17 |
| `private void prepareStatement(PreparedStatement statement) throws SQLException` | 23 |

**SQL used (from `ImpactsByCompanyIdQuery.COUNT_QUERY`):**
```
SELECT COUNT(DISTINCT(impact_id))
FROM v_impacts vi
LEFT JOIN unit_company uc ON uc.unit_id = vi.unit_id AND
  uc.start_date <= vi.impact_time AND (uc.end_date IS NULL OR uc.end_date >= vi.impact_time)
LEFT JOIN company c ON c.id = uc.company_id
WHERE (vi.comp_id = ? OR uc.company_id = ?)
AND unit_threshold != 0 AND impact_value >= unit_threshold
AND timezone(?, impact_time at time zone 'UTC')::DATE = timezone(?, now())::DATE
```
Parameters: `companyId (pos 1)`, `companyId (pos 2)`, `timezone (pos 3)`, `timezone (pos 4)`

---

### 2. ImpactsReportByCompanyIdQuery

**Class name:** `ImpactsReportByCompanyIdQuery`
**Package:** `com.querybuilder.impacts`

**Fields:**

| Field | Line |
|-------|------|
| `private final long companyId` | 18 |
| `private List<FilterHandler> filterHandlers` | 19 |

**Methods:**

| Method | Line |
|--------|------|
| `ImpactsReportByCompanyIdQuery(long companyId, ImpactReportFilterBean filter)` (package-private constructor) | 21 |
| `public ImpactReportBean query(String timezone, String dateFormat) throws SQLException` | 31 |
| `private String getQuery()` | 39 |
| `private void prepareStatement(PreparedStatement statement) throws SQLException` | 45 |
| `private List<ImpactReportGroupBean> getResults(String timezone, String dateFormat, ResultSet rs) throws SQLException` | 52 |

**SQL used (from `ImpactsByCompanyIdQuery.REPORT_QUERY`):**
```
SELECT vi.*, c.name AS assigned_company_name
FROM v_impacts vi
LEFT JOIN unit_company uc ON uc.unit_id = vi.unit_id AND
  uc.start_date <= vi.impact_time AND (uc.end_date IS NULL OR uc.end_date >= vi.impact_time)
LEFT JOIN company c ON c.id = uc.company_id
WHERE (vi.comp_id = ? OR uc.company_id = ?)
AND unit_threshold != 0 AND impact_value >= unit_threshold
 %s
ORDER BY impact_time DESC
```
Dynamic filter segment `%s` is built by concatenating `filterHandler.getQueryFilter()` results for:
- `DateBetweenFilterHandler` on `impact_time`
- `UnitManufactureFilterHandler` on `manufacture_id`
- `UnitTypeFilterHandler` on `type_id`
- `ImpactLevelFilterHandler` on `impact_value`/`unit_threshold`

ResultSet columns consumed in `getResults`: `unit_id`, `unit_name`, `manufacture_name`, `impact_id`, `unit_threshold`, `impact_time`, `impact_value`, `driver_name`, `assigned_company_name`

---

### 3. IncidentReportByCompanyIdQuery

**Class name:** `IncidentReportByCompanyIdQuery`
**Package:** `com.querybuilder.incidents`

**Fields:**

| Field | Line |
|-------|------|
| `private static final String BASE_QUERY` | 22 |
| `private final int companyId` | 29 |
| `private List<FilterHandler> filterHandlers` | 30 |

**Methods:**

| Method | Line |
|--------|------|
| `public IncidentReportByCompanyIdQuery(int companyId, IncidentReportFilterBean filter)` | 32 |
| `public IncidentReportBean query(String timezone, String dateFormat) throws SQLException` | 41 |
| `private String getQuery()` | 47 |
| `private void prepareStatement(PreparedStatement statement) throws SQLException` | 54 |
| `private IncidentReportEntryBean mapResult(String timezone, String dateFormat, ResultSet result) throws SQLException` | 61 |

**SQL used (BASE_QUERY + dynamic filters + ORDER BY):**
```
SELECT vir.*, c.name AS assigned_company_name
FROM v_incidents_report vir
LEFT JOIN unit_company uc ON uc.unit_id = vir.unit_id
  AND uc.start_date <= vir.event_time AND (uc.end_date IS NULL OR uc.end_date >= vir.event_time)
LEFT JOIN company c ON c.id = uc.company_id
WHERE (vir.comp_id = ? OR uc.company_id = ?)
<dynamic filters appended>
ORDER BY event_time DESC
```
Dynamic filters built by:
- `DateBetweenFilterHandler` on `event_time`
- `UnitManufactureFilterHandler` on `manufacture_id`
- `UnitTypeFilterHandler` on `type_id`

ResultSet columns consumed in `mapResult`: `unit_name`, `manufacture_name`, `assigned_company_name`, `driver_name`, `incidents_description`, `event_time`, `near_miss`, `incident`, `injury`, `injury_type`, `incidents_location`, `witness`, `signature`, `image`

---

## Test Coverage Search Results

Grep of test directory for `ImpactsCountByCompanyIdQuery`: **No matches found**
Grep of test directory for `ImpactsReportByCompanyIdQuery`: **No matches found**
Grep of test directory for `IncidentReportByCompanyIdQuery`: **No matches found**
Grep of test directory for `ImpactsByCompanyIdQuery`: **No matches found**

Existing test files in the test directory:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Conclusion:** Zero test coverage exists for all three classes under audit.

---

## Findings

### ImpactsCountByCompanyIdQuery

**A96-1 | Severity: CRITICAL | No test class exists for ImpactsCountByCompanyIdQuery**
There are no tests at all for `ImpactsCountByCompanyIdQuery`. The class performs a live database COUNT query via `DBUtil.queryForObject`. No unit or integration test exists to verify any of its behavior.

**A96-2 | Severity: CRITICAL | COUNT_QUERY parameter binding is entirely untested**
`prepareStatement` sets four parameters: `companyId` at positions 1 and 2, and `timezone` at positions 3 and 4. The fact that `companyId` must appear twice (to satisfy the `vi.comp_id = ? OR uc.company_id = ?` clause) and `timezone` must appear twice (for both `timezone()` function calls in the `WHERE` date equality check) is non-obvious and error-prone. There is no test confirming the parameter count, positions, or types are correct.

**A96-3 | Severity: HIGH | No test for the zero-result (orElse(0)) default path**
`query()` returns `rs.getInt(1)` wrapped with `.orElse(0)`. There is no test verifying that a query returning no rows (e.g., for a companyId with no impacts today) correctly yields `0` rather than `null` or an exception.

**A96-4 | Severity: HIGH | Package-private constructor prevents straightforward unit testing**
The constructor `ImpactsCountByCompanyIdQuery(long companyId, String timezone)` has package-private (default) visibility. Only `ImpactsByCompanyIdQuery.count()` is the intended factory entry point, also package-private. This design makes instantiation for testing without reflection or being in the same package impossible from external test classes, creating a structural barrier to unit testing.

**A96-5 | Severity: MEDIUM | No test for invalid or null timezone argument**
`timezone` is stored as a plain `String` and passed directly to the SQL timezone function via `statement.setString`. There is no test for a `null` timezone, an invalid timezone name, or an empty string, all of which would cause database-side errors that would be swallowed by `DBUtil` (which only calls `e.printStackTrace()` and returns `Optional.empty()`).

**A96-6 | Severity: MEDIUM | Error swallowing in DBUtil is untested**
`DBUtil.queryForObject` catches `SQLException`, prints the stack trace, and returns `Optional.empty()`, meaning `query()` would silently return `0` on any database error. There is no test asserting that a database failure is surfaced or distinguishable from a legitimate zero count.

---

### ImpactsReportByCompanyIdQuery

**A96-7 | Severity: CRITICAL | No test class exists for ImpactsReportByCompanyIdQuery**
There are no tests at all for `ImpactsReportByCompanyIdQuery`. The class performs a live database SELECT query, constructs dynamic SQL, maps a complex result set into a grouped bean structure, and sorts results. None of this is tested.

**A96-8 | Severity: CRITICAL | Dynamic SQL construction via getQuery() is entirely untested**
`getQuery()` appends filter fragments from four `FilterHandler` instances using `String.format` with a `%s` placeholder from `REPORT_QUERY`. No test verifies the constructed SQL string for any combination of active or inactive filters. Incorrect whitespace, duplicate AND keywords, or missing clauses would go undetected.

**A96-9 | Severity: CRITICAL | ResultSet grouping logic in getResults() is entirely untested**
`getResults()` uses a `HashMap<Long, ImpactReportGroupBean>` keyed on `unit_id` to aggregate multiple rows per unit into groups. No test confirms that: (a) multiple rows for the same unit are correctly grouped under one bean, (b) rows for different units produce separate group beans, (c) a single-row result produces exactly one group with one entry, or (d) an empty result set produces an empty list.

**A96-10 | Severity: CRITICAL | ImpactLevelFilterHandler SQL injection-style logic is untested through ImpactsReportByCompanyIdQuery**
`ImpactLevelFilterHandler.getQueryFilter()` inlines field names (`impact_value`, `unit_threshold`) directly into SQL strings using `String.format` with no parameterization (e.g., `AND impact_value > (unit_threshold * 10)`). The correctness of each branch (RED, AMBER, BLUE, null/default) as triggered through `ImpactsReportByCompanyIdQuery` is untested.

**A96-11 | Severity: HIGH | No test for filter combination correctness in prepareStatement**
`prepareStatement` first adds `companyId` twice via `StatementPreparer`, then delegates to each filter handler. The filter handlers add parameters only when their filter is active. No test verifies that the parameter binding order (companyId x2, then filter params in handler order) matches the corresponding SQL placeholder order produced by `getQuery()`, across all filter activation combinations.

**A96-12 | Severity: HIGH | No test for result sorting in query()**
`query()` calls `Collections.sort(impactReportGroups)` on the result. `ImpactReportGroupBean.compareTo()` returns `this.manufacturer.compareTo(o.manufacturer) + this.unitName.compareTo(o.unitName)`, which is mathematically incorrect as a comparator (the sum of two `compareTo` calls does not produce a consistent total ordering). No test exposes or validates this sort behavior.

**A96-13 | Severity: HIGH | No test for null or missing ResultSet columns**
`getResults()` calls `rs.getString("unit_name")`, `rs.getString("manufacture_name")`, `rs.getString("driver_name")`, `rs.getString("assigned_company_name")` without null checks. If any of these columns return null (e.g., no driver assigned, no company assignment), the behavior is untested. In particular, `manufacturer` being `null` would cause a `NullPointerException` in `ImpactReportGroupBean.compareTo()` during sorting.

**A96-14 | Severity: HIGH | No test for DateBetweenFilterHandler start-only and end-only paths within this query**
`DateBetweenFilterHandler.getQueryFilter()` has three active branches: start-only (`>= ?`), end-only (`<= ?`), and between two dates (with timezone). The between branch generates `timezone(?, impact_time at time zone 'UTC')::DATE BETWEEN ? AND ?` with three parameters (timezone, start, end); the start-only and end-only branches generate a single parameter each but do NOT prepend the timezone. The `prepareStatement` in `DateBetweenFilterHandler` conditionally adds the timezone first. No test verifies the consistency of parameter count between SQL and binding for any of these branches.

**A96-15 | Severity: MEDIUM | Package-private constructor prevents straightforward unit testing**
As with `ImpactsCountByCompanyIdQuery`, the constructor is package-private. External tests must use the `ImpactsByCompanyIdQuery.report()` factory, but that factory also resides in the same package and is itself untested. This creates a circular dependency that makes isolation-level unit testing structurally difficult.

**A96-16 | Severity: MEDIUM | No test for timezone/dateFormat interaction in result mapping**
`getResults()` calls `DateUtil.utc2Local(rs.getTimestamp("impact_time"), timezone)` followed by `DateUtil.formatDateTime(..., dateFormat)`. No test verifies that timezone conversion and date formatting produce the expected output string for a given UTC timestamp, timezone identifier, and date format pattern. A null `impact_time` timestamp would return an empty string from `formatDateTime` without exception, but this is also unverified.

**A96-17 | Severity: MEDIUM | No test for ImpactReportBean construction from empty group list**
No test covers the case where no impacts exist (empty result set), verifying that `query()` returns an `ImpactReportBean` with an empty `groups` list rather than null or throwing.

---

### IncidentReportByCompanyIdQuery

**A96-18 | Severity: CRITICAL | No test class exists for IncidentReportByCompanyIdQuery**
There are no tests at all for `IncidentReportByCompanyIdQuery`. The class builds dynamic SQL, binds parameters, and maps a fourteen-column result set to a bean with URL concatenation for two fields. None of this is tested.

**A96-19 | Severity: CRITICAL | Dynamic SQL construction via getQuery() is entirely untested**
`getQuery()` appends string fragments from three `FilterHandler` instances to a `StringBuilder` then appends a fixed `ORDER BY event_time DESC`. No test verifies the final query string under any filter combination (all inactive, all active, partial).

**A96-20 | Severity: CRITICAL | Result mapping in mapResult() is entirely untested**
`mapResult()` reads fourteen columns from the result set and passes two of them through `RuntimeConf.cloudImageURL + result.getString("signature")` and `RuntimeConf.cloudImageURL + result.getString("image")`. No test verifies: (a) all columns are read with the correct column labels, (b) the URL prefix concatenation is correct, (c) null column values are handled without NullPointerException (e.g., `signature` or `image` being null would produce a string like `"https://...null"`).

**A96-21 | Severity: CRITICAL | Null image/signature columns produce corrupt URL values without test guard**
In `mapResult()` (line 76-77):
```java
.signature(RuntimeConf.cloudImageURL + result.getString("signature"))
.image(RuntimeConf.cloudImageURL + result.getString("image"))
```
If `result.getString("signature")` or `result.getString("image")` returns `null`, Java string concatenation produces `"https://s3.amazonaws.com/forkliftiq360/image/null"`. This is a data corruption defect with no test to detect it.

**A96-22 | Severity: HIGH | companyId field type mismatch between class and StatementPreparer call is untested**
`companyId` is declared as `int` at line 29, but `preparer.addLong(companyId)` is called at lines 56-57. This causes implicit widening of `int` to `long`. While widening is safe in Java, the field is typed inconsistently with the equivalent field in `ImpactsCountByCompanyIdQuery` (which uses `long`). No test verifies that `int`-range boundary values (e.g., `Integer.MAX_VALUE`) are passed to the database without loss or misinterpretation.

**A96-23 | Severity: HIGH | No test for parameter binding order consistency**
As with the impacts queries, no test verifies that the order of SQL placeholders in the final query string matches the order in which `prepareStatement` adds parameters (companyId x2, then filter parameters in handler-list order). Any discrepancy would bind wrong values to wrong parameters silently.

**A96-24 | Severity: HIGH | No test for ORDER BY correctness or filter interaction**
The `ORDER BY event_time DESC` clause is appended unconditionally. No test verifies the final query structure when zero, one, two, or three filters are active, or that the ORDER BY is always the final clause and not interleaved with filter fragments.

**A96-25 | Severity: HIGH | No test for boolean column mapping (near_miss, incident, injury)**
`mapResult()` calls `result.getBoolean("near_miss")`, `result.getBoolean("incident")`, and `result.getBoolean("injury")`. The behavior when these columns are SQL `NULL` (which returns `false` in JDBC with no indication of null) is untested and may produce misleading false negatives in the output bean.

**A96-26 | Severity: MEDIUM | No test for DateBetweenFilterHandler paths in IncidentReportByCompanyIdQuery**
The same filter branch correctness concern documented in A96-14 applies here for `event_time`. The start-only, end-only, and between-two-dates paths each produce different SQL and different parameter counts. No test validates any of these paths in the context of this class.

**A96-27 | Severity: MEDIUM | No test for timezone/dateFormat handling in mapResult()**
`mapResult()` calls `DateUtil.utc2Local(result.getTimestamp("event_time"), timezone)` and `DateUtil.formatDateTime(..., dateFormat)`. A null `event_time` timestamp returns an empty string silently. An invalid timezone identifier passed to `TimeZone.getTimeZone()` silently falls back to GMT. No test covers these degraded-input paths.

**A96-28 | Severity: MEDIUM | Error swallowing in DBUtil.queryForObjects is untested**
`DBUtil.queryForObjects` catches `SQLException`, prints the stack trace, and returns an empty list. `IncidentReportByCompanyIdQuery.query()` would then return an `IncidentReportBean` with an empty entry list on any database failure, with no distinction from a legitimate zero-result query. No test covers this failure path.

**A96-29 | Severity: LOW | No test for IncidentReportBean wrapping of empty result list**
No test confirms that when the query produces zero rows, `query()` returns a non-null `IncidentReportBean` containing an empty (not null) `entries` list.

**A96-30 | Severity: LOW | Constructor is public but ImpactsCountByCompanyIdQuery/ImpactsReportByCompanyIdQuery constructors are package-private**
`IncidentReportByCompanyIdQuery` has a `public` constructor (line 32), unlike the two impacts query classes which use package-private constructors and factory methods in `ImpactsByCompanyIdQuery`. The inconsistency means this class can be instantiated directly in tests but no test does so. The impacts classes require using the `ImpactsByCompanyIdQuery` factory methods, creating an access asymmetry with no documented rationale and no test coverage to validate the factory path.

---

## Summary Table

| Finding | Class | Severity | Category |
|---------|-------|----------|----------|
| A96-1 | ImpactsCountByCompanyIdQuery | CRITICAL | No test class |
| A96-2 | ImpactsCountByCompanyIdQuery | CRITICAL | Parameter binding |
| A96-3 | ImpactsCountByCompanyIdQuery | HIGH | Default value path |
| A96-4 | ImpactsCountByCompanyIdQuery | HIGH | Structural test barrier |
| A96-5 | ImpactsCountByCompanyIdQuery | MEDIUM | Null/invalid timezone |
| A96-6 | ImpactsCountByCompanyIdQuery | MEDIUM | Error swallowing |
| A96-7 | ImpactsReportByCompanyIdQuery | CRITICAL | No test class |
| A96-8 | ImpactsReportByCompanyIdQuery | CRITICAL | Dynamic SQL construction |
| A96-9 | ImpactsReportByCompanyIdQuery | CRITICAL | ResultSet grouping logic |
| A96-10 | ImpactsReportByCompanyIdQuery | CRITICAL | ImpactLevel filter SQL branches |
| A96-11 | ImpactsReportByCompanyIdQuery | HIGH | Filter combo parameter binding |
| A96-12 | ImpactsReportByCompanyIdQuery | HIGH | Incorrect comparator / sort |
| A96-13 | ImpactsReportByCompanyIdQuery | HIGH | Null ResultSet columns |
| A96-14 | ImpactsReportByCompanyIdQuery | HIGH | DateBetweenFilter branches |
| A96-15 | ImpactsReportByCompanyIdQuery | MEDIUM | Structural test barrier |
| A96-16 | ImpactsReportByCompanyIdQuery | MEDIUM | Timezone/dateFormat in mapping |
| A96-17 | ImpactsReportByCompanyIdQuery | MEDIUM | Empty result set |
| A96-18 | IncidentReportByCompanyIdQuery | CRITICAL | No test class |
| A96-19 | IncidentReportByCompanyIdQuery | CRITICAL | Dynamic SQL construction |
| A96-20 | IncidentReportByCompanyIdQuery | CRITICAL | Result mapping untested |
| A96-21 | IncidentReportByCompanyIdQuery | CRITICAL | Null image/signature URL corruption |
| A96-22 | IncidentReportByCompanyIdQuery | HIGH | companyId int/long type mismatch |
| A96-23 | IncidentReportByCompanyIdQuery | HIGH | Parameter binding order |
| A96-24 | IncidentReportByCompanyIdQuery | HIGH | ORDER BY clause correctness |
| A96-25 | IncidentReportByCompanyIdQuery | HIGH | Boolean null column mapping |
| A96-26 | IncidentReportByCompanyIdQuery | MEDIUM | DateBetweenFilter branches |
| A96-27 | IncidentReportByCompanyIdQuery | MEDIUM | Timezone/dateFormat handling |
| A96-28 | IncidentReportByCompanyIdQuery | MEDIUM | Error swallowing |
| A96-29 | IncidentReportByCompanyIdQuery | LOW | Empty result wrapping |
| A96-30 | IncidentReportByCompanyIdQuery | LOW | Constructor visibility inconsistency |

**Total findings: 30**
- CRITICAL: 10
- HIGH: 10
- MEDIUM: 7
- LOW: 3
