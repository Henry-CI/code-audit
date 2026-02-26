# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A90
**Date:** 2026-02-26

---

## Source Files Audited

1. `src/main/java/com/querybuilder/StatementPreparer.java`
2. `src/main/java/com/querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`

**Test directory searched:** `src/test/java/`

**Test files present in repository:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep result for `StatementPreparer` in test directory:** No matches found.
**Grep result for `AssignmentByCompanyAndUnitIdQuery` in test directory:** No matches found.

---

## Reading Evidence

### File 1: `StatementPreparer.java`

**Class name:** `com.querybuilder.StatementPreparer`

**Fields:**

| Field Name  | Line | Type                  | Access  |
|-------------|------|-----------------------|---------|
| `statement` | 8    | `PreparedStatement`   | private |
| `index`     | 9    | `int`                 | private |

**Methods:**

| Method Name          | Line | Signature                                             |
|----------------------|------|-------------------------------------------------------|
| `StatementPreparer`  | 11   | `public StatementPreparer(PreparedStatement statement)` |
| `addDate`            | 16   | `public void addDate(Date value) throws SQLException`  |
| `addLong`            | 20   | `public void addLong(long value) throws SQLException`  |
| `addString`          | 24   | `public void addString(String value) throws SQLException` |
| `addInteger`         | 28   | `public void addInteger(int value) throws SQLException` |

**Behavioral notes:**
- `index` is initialised to `0` and pre-incremented (`++index`) before each `PreparedStatement` setter call. This means the first parameter bound is at index `1`, which is correct JDBC behaviour.
- No getter or reset method for `index` exists; once a `StatementPreparer` instance has advanced its index, there is no way to reuse it for a second round of bindings.

---

### File 2: `AssignmentByCompanyAndUnitIdQuery.java`

**Class name:** `com.querybuilder.assignment.AssignmentByCompanyAndUnitIdQuery`

**Fields:**

| Field Name  | Line | Type     | Access         |
|-------------|------|----------|----------------|
| `query`     | 14   | `String` | private static final |
| `companyId` | 20   | `long`   | private final  |
| `unitId`    | 21   | `long`   | private final  |

**SQL query (lines 14–18):**
```sql
SELECT id, company_name, start_date, end_date, is_current
FROM v_unit_assignments
WHERE unit_id = ? AND (company_id = ? OR parent_company_id = ?)
ORDER BY start_date DESC
```

**Methods:**

| Method Name          | Line | Signature                                                                          |
|----------------------|------|------------------------------------------------------------------------------------|
| `AssignmentByCompanyAndUnitIdQuery` | 23 | `public AssignmentByCompanyAndUnitIdQuery(long companyId, long unitId)` |
| `query`              | 28   | `public List<UnitAssignmentBean> query(String dateFormat) throws SQLException`      |
| `mapResults`         | 32   | `private UnitAssignmentBean mapResults(String dateFormat, ResultSet resultSet) throws SQLException` |
| `prepareStatement`   | 42   | `private void prepareStatement(PreparedStatement statement) throws SQLException`    |

**Parameter binding (lines 43–46):**
```
param 1 (index 1) -> unitId    (addLong)
param 2 (index 2) -> companyId (addLong)
param 3 (index 3) -> companyId (addLong)
```

**ResultSet column mapping (lines 33–39):**
- `"id"` -> `resultSet.getInt("id")` -> `UnitAssignmentBean.id`
- `"company_name"` -> `resultSet.getString("company_name")` -> `UnitAssignmentBean.company_name`
- `"start_date"` -> `resultSet.getDate("start_date")` via `DateUtil.formatDate` -> `UnitAssignmentBean.start`
- `"end_date"` -> `resultSet.getDate("end_date")` via `DateUtil.formatDate` -> `UnitAssignmentBean.end`
- `"is_current"` -> `resultSet.getBoolean("is_current")` -> `UnitAssignmentBean.isCurrent` (mapped to `"Yes"`/`"No"` string in bean)

---

## Findings

### StatementPreparer

---

**A90-1 | Severity: CRITICAL | No test class exists for StatementPreparer**

There is zero test coverage for `StatementPreparer`. No test file referencing `StatementPreparer` was found anywhere under `src/test/java/`. Every public method (`addDate`, `addLong`, `addString`, `addInteger`) and the constructor are completely untested.

---

**A90-2 | Severity: HIGH | addDate() — null input not handled; will throw NullPointerException**

`addDate(Date value)` calls `value.getTime()` unconditionally (line 17). If `null` is passed, a `NullPointerException` is thrown before the `PreparedStatement` setter is reached. There is no null guard and no test verifying this failure mode. `PreparedStatement.setNull()` or an explicit null check is required for nullable date columns but is absent.

---

**A90-3 | Severity: HIGH | addString() — no test for null input; JDBC null semantics unverified**

`addString(String value)` passes the value to `PreparedStatement.setString()` directly. JDBC drivers are permitted to accept `null` for `setString`, but this is driver-dependent. No test verifies either the null-accepted path or whether `setNull(index, Types.VARCHAR)` should be used instead. Callers in the codebase (e.g. date formatting producing `null` strings) could silently corrupt SQL parameters.

---

**A90-4 | Severity: HIGH | No test for sequential index advancement across multiple add* calls**

The correctness invariant of `StatementPreparer` is that `++index` produces the correct 1-based JDBC parameter index for each successive call. There is no test that constructs a `StatementPreparer` with a mock `PreparedStatement`, calls multiple `add*` methods in sequence, and asserts that each underlying `PreparedStatement.setXxx(n, ...)` was called with the expected index. A one-off error in the pre-increment would cause silent wrong-column binding.

---

**A90-5 | Severity: MEDIUM | addDate() — java.util.Date to java.sql.Date conversion: time component silently truncated; no test**

`addDate` constructs a `java.sql.Date` from a `java.util.Date` using `value.getTime()` (line 17). `java.sql.Date.getTime()` is millisecond-accurate but the SQL DATE type carries no time component; some JDBC drivers will silently discard the time portion. There is no test confirming that the time portion is intentionally discarded (or not) and that the resulting date value is correct.

---

**A90-6 | Severity: MEDIUM | addInteger() — no test for boundary values (Integer.MIN_VALUE, Integer.MAX_VALUE, negative values)**

`addInteger(int value)` delegates to `PreparedStatement.setInt`. No tests exist for boundary inputs such as `0`, `-1`, `Integer.MIN_VALUE`, or `Integer.MAX_VALUE` to ensure correct delegation and no sign/overflow issues.

---

**A90-7 | Severity: MEDIUM | addLong() — no test for boundary values**

Equivalent to A90-6 for `addLong`. Values such as `Long.MIN_VALUE`, `Long.MAX_VALUE`, and `0L` are untested. Given that `addLong` is used to bind database entity IDs in `AssignmentByCompanyAndUnitIdQuery`, an id of `0` (which could indicate an unset/default state) is a realistic edge case.

---

**A90-8 | Severity: LOW | No test for constructor — field initialisation not verified**

The constructor sets `index = 0` and assigns `statement`. No test verifies that a `null` `PreparedStatement` argument causes a predictable failure rather than a deferred NPE at the first `add*` call site.

---

### AssignmentByCompanyAndUnitIdQuery

---

**A90-9 | Severity: CRITICAL | No test class exists for AssignmentByCompanyAndUnitIdQuery**

There is zero test coverage for `AssignmentByCompanyAndUnitIdQuery`. No test file referencing this class was found anywhere under `src/test/java/`. The constructor, `query()`, `mapResults()`, and `prepareStatement()` are all untested.

---

**A90-10 | Severity: CRITICAL | Parameter binding order in prepareStatement() is inverted relative to the SQL WHERE clause**

The SQL WHERE clause (lines 16–17) is:
```sql
WHERE unit_id = ? AND (company_id = ? OR parent_company_id = ?)
```
The three placeholders map, in SQL order, to: `[1] unit_id`, `[2] company_id`, `[3] parent_company_id`.

`prepareStatement()` (lines 43–46) binds:
```java
preparer.addLong(unitId);    // index 1 -> unit_id     CORRECT
preparer.addLong(companyId); // index 2 -> company_id  CORRECT
preparer.addLong(companyId); // index 3 -> parent_company_id CORRECT (same value, intentional)
```
The binding is actually correct at runtime, but because parameters 2 and 3 receive the same value (`companyId`), this is a non-obvious pattern that is indistinguishable from an accidental duplication bug without tests. There is no test to confirm that `companyId` appearing twice is intentional design (to match both direct and inherited company relationships) versus a copy-paste defect where `parentCompanyId` was forgotten as a separate constructor parameter.

---

**A90-11 | Severity: HIGH | query() swallows SQLException silently — DBUtil.queryForObjects catches and only prints the exception**

`AssignmentByCompanyAndUnitIdQuery.query()` delegates to `DBUtil.queryForObjects()` (line 29), which internally catches `SQLException`, calls `e.printStackTrace()`, and returns an empty list (DBUtil lines 75–77). The caller sees an empty list rather than a thrown exception. No test validates this failure-masking behaviour, meaning callers cannot distinguish "no assignments found" from "database error occurred". This is a design defect in `DBUtil` but `AssignmentByCompanyAndUnitIdQuery` inherits it and provides no mitigation.

---

**A90-12 | Severity: HIGH | mapResults() — end_date is nullable; DateUtil.formatDate() returns null for null input; no test for open-ended assignments**

`resultSet.getDate("end_date")` (line 37) can return `null` for assignments without an end date (i.e., currently active assignments). `DateUtil.formatDate(Date date, String dateFormat)` returns `null` when `date` is null (DateUtil line 148). `UnitAssignmentBean.end` will therefore be `null`. No test verifies this path, and calling code that formats or displays `end` without a null check will throw a `NullPointerException`.

---

**A90-13 | Severity: HIGH | mapResults() — dateFormat parameter is not validated; a null or malformed format string will throw at runtime**

`DateUtil.formatDate(resultSet.getDate("start_date"), dateFormat)` and the equivalent for `end_date` use `dateFormat` directly in `new SimpleDateFormat(dateFormat)`. If `dateFormat` is `null` or malformed, a `NullPointerException` or `IllegalArgumentException` is thrown from inside the result-set mapper while iterating rows. Because `DBUtil.queryForObjects` only catches `SQLException`, this unchecked exception will propagate up the call stack unguarded. No test verifies invalid `dateFormat` handling.

---

**A90-14 | Severity: HIGH | No test for empty result set (zero matching rows)**

No test confirms that `query()` returns an empty `List` (not `null`) when the view returns no rows. Although `DBUtil` initialises `results` as an `ArrayList`, the silent catch block could theoretically return an empty list for the wrong reason (error vs. genuine empty result). A test with no matching rows is required to distinguish these cases.

---

**A90-15 | Severity: HIGH | No test for the query() method with a valid multi-row result set**

The happy-path scenario — multiple rows returned, all columns populated, correct `UnitAssignmentBean` objects produced — is entirely untested. Without an integration or mock-based test, the `mapResults` column-name bindings (`"id"`, `"company_name"`, `"start_date"`, `"end_date"`, `"is_current"`) have never been exercised against a real or simulated `ResultSet`.

---

**A90-16 | Severity: MEDIUM | isCurrent field: boolean from ResultSet converted to "Yes"/"No" String in bean; conversion is untested**

`mapResults` reads `resultSet.getBoolean("is_current")` and passes it as `isCurrent` to the Lombok builder (line 38). The `UnitAssignmentBean` builder constructor (UnitAssignmentBean line 26) converts `true` -> `"Yes"` and `false` -> `"No"` into the `current` String field. No test verifies both paths of this conversion. If the view returns `0`/`1` or a non-boolean type for `is_current`, `getBoolean` behaviour is driver-dependent.

---

**A90-17 | Severity: MEDIUM | Constructor: no validation for non-positive companyId or unitId**

`AssignmentByCompanyAndUnitIdQuery(long companyId, long unitId)` performs no validation. Values of `0` or negative longs are stored and bound to the SQL query without error. No test verifies that invalid entity IDs produce a predictable outcome (e.g., empty result set or exception). ID `0` is a plausible sentinel value that could produce misleading results from the view.

---

**A90-18 | Severity: MEDIUM | prepareStatement() is private and not independently testable; its correctness relies on integration test only**

`prepareStatement` (line 42) is the sole point where SQL parameter binding occurs. Because it is private, it can only be tested indirectly via `query()`. Without a mock-based test for `query()` that captures the `PreparedStatement` calls, there is no way to assert that `unitId` is bound to index 1 and `companyId` is bound to indices 2 and 3 without executing against a live database.

---

**A90-19 | Severity: MEDIUM | query(String dateFormat) — no test for null dateFormat explicitly**

Although A90-13 covers runtime behaviour, a dedicated test for `query(null)` as `dateFormat` is needed to document whether `null` is a supported input. `DateUtil.formatDate(date, null)` would call `new SimpleDateFormat(null)` which throws `NullPointerException`. There is no null guard in the call chain.

---

**A90-20 | Severity: LOW | Static query String is a compile-time constant; no test guards against accidental modification**

The SQL query string at lines 14–18 is a multi-line concatenation. The resulting string is correct, but there is no test that asserts the exact SQL string value. A future refactor that accidentally drops the `parent_company_id` clause or reorders predicates would not be caught without a coverage test.

---

**A90-21 | Severity: LOW | UnitAssignmentBean.id mapped via getInt("id") — potential truncation if DB id column exceeds Integer.MAX_VALUE**

`resultSet.getInt("id")` (line 34) will silently truncate values greater than `Integer.MAX_VALUE` (2,147,483,647) if the database `id` column is a `BIGINT`. The bean field `id` is typed as `int`. No test exercises a large-id scenario. If the view column is `BIGINT`, `getLong` should be used instead.

---

## Summary Table

| Finding | Severity | Area                        | Description (short)                                               |
|---------|----------|-----------------------------|-------------------------------------------------------------------|
| A90-1   | CRITICAL | StatementPreparer           | No test class exists                                              |
| A90-2   | HIGH     | StatementPreparer.addDate   | Null input causes NPE; no null guard and no test                  |
| A90-3   | HIGH     | StatementPreparer.addString | Null input JDBC semantics unverified; no test                     |
| A90-4   | HIGH     | StatementPreparer           | Sequential index advancement not tested with mock PreparedStatement |
| A90-5   | MEDIUM   | StatementPreparer.addDate   | Time component truncation behaviour untested                      |
| A90-6   | MEDIUM   | StatementPreparer.addInteger| Boundary values untested                                          |
| A90-7   | MEDIUM   | StatementPreparer.addLong   | Boundary values untested                                          |
| A90-8   | LOW      | StatementPreparer           | Constructor null-argument behaviour untested                      |
| A90-9   | CRITICAL | AssignmentByCompanyAndUnitIdQuery | No test class exists                                      |
| A90-10  | CRITICAL | prepareStatement()          | companyId bound twice; no test confirms intent vs. copy-paste bug |
| A90-11  | HIGH     | query()                     | DBUtil silently swallows SQLException; empty list is ambiguous    |
| A90-12  | HIGH     | mapResults()                | Null end_date not tested; UnitAssignmentBean.end will be null     |
| A90-13  | HIGH     | mapResults()                | Null or malformed dateFormat throws unchecked exception           |
| A90-14  | HIGH     | query()                     | Empty result set not tested                                       |
| A90-15  | HIGH     | query()                     | Happy-path multi-row mapping entirely untested                    |
| A90-16  | MEDIUM   | mapResults()                | boolean -> "Yes"/"No" conversion untested                         |
| A90-17  | MEDIUM   | Constructor                 | Non-positive/zero IDs not validated or tested                     |
| A90-18  | MEDIUM   | prepareStatement()          | Private method; parameter binding untestable without mock         |
| A90-19  | MEDIUM   | query()                     | Null dateFormat not explicitly tested                             |
| A90-20  | LOW      | query (SQL constant)        | No test guards the SQL string against accidental modification     |
| A90-21  | LOW      | mapResults()                | getInt("id") may silently truncate BIGINT ids                     |
