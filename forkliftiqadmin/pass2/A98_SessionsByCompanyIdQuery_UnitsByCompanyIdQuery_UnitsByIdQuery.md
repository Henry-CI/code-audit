# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A98
**Report Date:** 2026-02-26
**Files Audited:**
1. `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java`
2. `src/main/java/com/querybuilder/unit/UnitsByCompanyIdQuery.java`
3. `src/main/java/com/querybuilder/unit/UnitsByIdQuery.java`

**Test Directory Searched:** `src/test/java/`

---

## Test Discovery Results

Grep of the test directory for each class name returned **no matches** for any of the three classes:

- `SessionsByCompanyIdQuery` — 0 test files found
- `UnitsByCompanyIdQuery` — 0 test files found
- `UnitsByIdQuery` — 0 test files found

Existing test files in the project (4 total, all unrelated):
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

---

## Reading Evidence

### 1. `SessionsByCompanyIdQuery`

**Class name:** `SessionsByCompanyIdQuery`
**Package:** `com.querybuilder.session`

**Fields:**

| Field | Type | Line |
|---|---|---|
| `companyId` | `int` | 18 |
| `filterHandlers` | `List<FilterHandler>` | 19 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `SessionsByCompanyIdQuery(int companyId, SessionFilterBean filter)` (constructor) | `private` | 21 |
| `query(String timezone, String dateFormat)` | `public` | 30 |
| `getQuery()` | `private` | 40 |
| `prepareStatement(PreparedStatement statement)` | `private` | 50 |
| `getResults(String timezone, String dateFormat, ResultSet rs)` | `private` | 57 |
| `report(int companyId, SessionFilterBean filter)` | `public static` | 69 |

**Filter handlers wired in constructor (line 23–27):**
- `DateBetweenFilterHandler` on column `session_start_time`
- `SessionUnitFilterHandler` on column `unit_id`
- `SessionDriverFilterHandler` on column `driver_id`

---

### 2. `UnitsByCompanyIdQuery`

**Class name:** `UnitsByCompanyIdQuery`
**Package:** `com.querybuilder.unit`

**Fields:**

| Field | Type | Line |
|---|---|---|
| `BASE_QUERY` | `private static final String` | 14 |
| `companyId` | `int` | 19 |
| `orderBy` | `String` (default `""`) | 20 |
| `activeUnitsOnly` | `String` (default `""`) | 21 |
| `filter` | `StringContainingFilterHandler` | 22 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `UnitsByCompanyIdQuery(int companyId)` (constructor) | `private` | 24 |
| `prepare(int companyId)` | `public static` | 29 |
| `orderBy(String orderBy)` | `public` | 33 |
| `activeUnitsOnly()` | `public` | 38 |
| `containing(String text)` | `public` | 43 |
| `query()` | `public` | 48 |
| `prepareStatement(PreparedStatement statement)` | `private` | 59 |
| `mapResult(ResultSet result)` | `private` | 67 |

---

### 3. `UnitsByIdQuery`

**Class name:** `UnitsByIdQuery`
**Package:** `com.querybuilder.unit`

**Fields:**

| Field | Type | Line |
|---|---|---|
| `query` | `private static final String` | 14 |
| `unitId` | `long` | 16 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `UnitsByIdQuery(long unitId)` (constructor) | `private` | 18 |
| `prepare(int unitId)` | `public static` | 22 |
| `query()` | `public` | 26 |
| `prepareStatement(PreparedStatement statement)` | `private` | 32 |
| `getResult(ResultSet result)` | `private` | 37 |

---

## Findings

---

### A — SessionsByCompanyIdQuery

**A98-1 | Severity: CRITICAL | No test class exists for SessionsByCompanyIdQuery**

There is zero test coverage for `SessionsByCompanyIdQuery`. No test file references the class name anywhere in the test source tree. Every method, branch, and SQL construction path is entirely untested.

---

**A98-2 | Severity: HIGH | `getQuery()` SQL construction not tested for any filter combination**

`getQuery()` (line 40) builds SQL dynamically by appending zero, one, two, or three filter clauses from `filterHandlers`. The combinations are:

- No filters active (date/unit/driver all null)
- Date filter only (start-only, end-only, or between-two-dates)
- Unit filter only
- Driver filter only
- All three filters simultaneously

None of these SQL shape variants are verified. A space is missing before `order by` (line 46; the prior filter clause may or may not end in a space, making the final SQL potentially malformed under certain filter combinations — e.g., when all filters are inactive the `WHERE` clause appends `order by` directly with no leading space after the closing parenthesis on line 42). This structural risk has no test coverage.

---

**A98-3 | Severity: HIGH | `prepareStatement()` parameter binding order not tested**

`prepareStatement()` (line 50) binds `companyId` twice (positions 1 and 2 via `addInteger`), then iterates filter handlers. The order of bind parameters must match the SQL placeholder positions precisely. No test verifies correct binding when filters are active or inactive, meaning a transposed or missing parameter would go undetected.

---

**A98-4 | Severity: HIGH | `getResults()` ResultSet mapping not tested — null timestamp handling**

`getResults()` (line 57) calls `DateUtil.utc2Local(rs.getTimestamp(...), timezone)` for both `session_finish_time` and `session_start_time`. `DateUtil.utc2Local(Timestamp, String)` (DateUtil line 228) will throw a `NullPointerException` if the timestamp is `null` (it calls `.toLocalDateTime()` on the returned timestamp directly without a null check). `session_finish_time` is a nullable column (sessions still in progress have no finish time), making NPE at runtime a real risk. No test covers this path.

---

**A98-5 | Severity: MEDIUM | `report()` factory method not tested**

The public API entry point `report(int companyId, SessionFilterBean filter)` (line 69) is never called in any test. While trivial in isolation, it is the only public construction path.

---

**A98-6 | Severity: MEDIUM | `query()` return value shape not tested**

`query(String timezone, String dateFormat)` (line 30) wraps results in a `SessionReportBean`. No test verifies that the bean is populated correctly (non-null sessions list, correct field mapping from `SessionBean.builder()`).

---

**A98-7 | Severity: MEDIUM | DateBetweenFilterHandler timezone injection not covered via SessionsByCompanyIdQuery**

When `SessionFilterBean` has a non-null timezone, `DateBetweenFilterHandler.prepareStatement()` prepends the timezone string as the first bind parameter (handler line 29), ahead of the date parameters. If timezone is null, no string is prepended. Because `SessionFilterBean.timezone()` can be null (field `timezone` has no `@NonNull` constraint), the binding order changes. No test validates either branch through the full query object.

---

### B — UnitsByCompanyIdQuery

**A98-8 | Severity: CRITICAL | No test class exists for UnitsByCompanyIdQuery**

There is zero test coverage for `UnitsByCompanyIdQuery`. No test file references the class name anywhere in the test source tree.

---

**A98-9 | Severity: HIGH | Builder method chaining and SQL composition not tested**

`UnitsByCompanyIdQuery` uses a fluent builder pattern (`prepare()`, `orderBy()`, `activeUnitsOnly()`, `containing()`). The `query()` method (line 48) appends `activeUnitsOnly` and optionally the `StringContainingFilterHandler` clause before `orderBy`. No test verifies any of the following SQL shape variants:

- Base query only (no modifiers)
- With `activeUnitsOnly()` only
- With `containing()` only
- With `orderBy()` only
- All three modifiers combined

---

**A98-10 | Severity: HIGH | `prepareStatement()` conditional filter binding not tested**

`prepareStatement()` (line 59) adds `companyId` twice as `Long` via `addLong()`, then conditionally calls `filter.prepareStatement(preparer)` only if `filter != null`. No test verifies correct parameter counts for the with-filter vs. without-filter cases.

---

**A98-11 | Severity: HIGH | `mapResult()` ResultSet column mapping not tested**

`mapResult()` (line 67) maps six columns: `id`, `name`, `serial_no`, `manu_name`, `type_name`, `hourmeter`. Note that `UnitsByCompanyIdQuery` does NOT map `type_nm` from the alias `type_name` — it uses `.type_nm(result.getString("type_name"))` (line 73). If the view `v_units` does not expose a column named `type_name` (it also uses `type_name` in `UnitsByIdQuery` at line 50), this is at least inconsistent across queries. No test exercises the mapping.

---

**A98-12 | Severity: MEDIUM | `orderBy()` accepts unsanitized SQL string**

`orderBy(String orderBy)` (line 33) directly concatenates the caller-supplied string into the SQL query (`" order by " + orderBy`). There is no input sanitization or whitelist validation. No test verifies that invalid or malicious input is rejected or handled safely. (SQL injection risk via untrusted `orderBy` values.)

---

**A98-13 | Severity: MEDIUM | `containing()` filter wraps text with `%` wildcards at construction time**

`StringContainingFilterHandler` (line 14 of that class) prepends and appends `%` to the search text at construction time, not at bind time. No test via `UnitsByCompanyIdQuery.containing()` verifies that the resulting ILIKE clause matches both `name` and `serial_no` columns simultaneously with the correct OR logic.

---

**A98-14 | Severity: MEDIUM | `prepare()` factory method not tested**

The sole public construction entry point `prepare(int companyId)` (line 29) is never exercised by any test.

---

### C — UnitsByIdQuery

**A98-15 | Severity: CRITICAL | No test class exists for UnitsByIdQuery**

There is zero test coverage for `UnitsByIdQuery`. No test file references the class name anywhere in the test source tree.

---

**A98-16 | Severity: CRITICAL | `getResult()` uses `KeypadReaderModel.valueOf()` without guarding against unrecognized enum values**

`getResult()` (line 59–60) calls `UnitBean.KeypadReaderModel.valueOf(result.getString("keypad_reader").trim())` when the column value is non-blank. `valueOf()` throws `IllegalArgumentException` for any string that does not exactly match one of the four enum constants (`ROSLARE`, `KERI`, `SMART`, `HID_ICLASS`). If the database column contains any other string (including legacy values, mixed case, or future additions), the application will throw an uncaught exception at runtime and fail to map the row. `StringUtils.isNotBlank()` guards against null/whitespace, but does not guard against unrecognized values. No test covers this path at all, let alone tests the failure case.

---

**A98-17 | Severity: HIGH | `getResult()` maps `session_finish_time` — `access_type` trim logic not tested**

`getResult()` (line 56–57) applies `.trim()` to the `access_type` column when non-blank. No test verifies that whitespace-padded values are trimmed, that null values are returned as null, or that blank-string values return null.

---

**A98-18 | Severity: HIGH | `getResult()` maps `keypad_reader` — null path not tested**

The null/blank path for `keypad_reader` (line 59) sets the field to `null` in the builder. No test confirms this branch is exercised correctly when the column is null or blank.

---

**A98-19 | Severity: HIGH | `getResult()` maps 16 columns — no column-level tests exist**

`getResult()` (lines 37–64) maps 16 columns from the `v_units` view: `id`, `name`, `location`, `department`, `type_id`, `active`, `manu_id`, `size`, `fuel_type_id`, `hourmeter`, `serial_no`, `type_name`, `fuel_type_name`, `manu_name`, `comp_id`, `mac_address`, `accessible`, `access_type`, `access_id`, `keypad_reader`, `facility_code`, `acc_hours`, `weight_unit`. A typo in any column name (e.g. `fuel_type_name` vs. `fule_type_name` in the field — line 51) would cause a `SQLException` at runtime. No test validates this mapping end-to-end.

---

**A98-20 | Severity: HIGH | `prepareStatement()` binds `unitId` as `Long` but `prepare()` accepts `int`**

`prepare(int unitId)` (line 22) accepts an `int` parameter and widens it to `long` in the `UnitsByIdQuery(long unitId)` constructor (line 18). `prepareStatement()` then binds it via `preparer.addLong(unitId)` (line 34), which calls `statement.setLong()`. No test verifies that widening from `int` to `long` preserves the value correctly, nor that `setLong()` is used where the database column type for `id` may be `INTEGER` (which could require `setInt()`).

---

**A98-21 | Severity: MEDIUM | `prepare()` and `query()` entry points not tested**

The public factory `prepare(int unitId)` (line 22) and `query()` (line 26) are entirely untested.

---

**A98-22 | Severity: MEDIUM | `getResult()` maps `accessible` via `getBoolean()` — no test for SQL NULL behavior**

`result.getBoolean("accessible")` (line 55) returns `false` when the SQL column is NULL (JDBC behavior). If the application logic requires distinguishing between an explicit `false` and a missing/null value, this silent coercion is a defect risk. No test covers this.

---

**A98-23 | Severity: LOW | `UnitsByIdQuery.query` field shadows `query()` method name**

The class has a `private static final String query` field (line 14) and a `public List<UnitBean> query()` method (line 26). Within the class, the field name `query` and method name `query()` are syntactically distinct but semantically confusing. No test documents expected behavior to distinguish intent.

---

## Summary Table

| Finding | Class | Severity | Category |
|---|---|---|---|
| A98-1 | SessionsByCompanyIdQuery | CRITICAL | No tests |
| A98-2 | SessionsByCompanyIdQuery | HIGH | SQL construction |
| A98-3 | SessionsByCompanyIdQuery | HIGH | Parameter binding |
| A98-4 | SessionsByCompanyIdQuery | HIGH | Null timestamp / NPE risk |
| A98-5 | SessionsByCompanyIdQuery | MEDIUM | Factory method |
| A98-6 | SessionsByCompanyIdQuery | MEDIUM | Return value shape |
| A98-7 | SessionsByCompanyIdQuery | MEDIUM | Timezone filter binding |
| A98-8 | UnitsByCompanyIdQuery | CRITICAL | No tests |
| A98-9 | UnitsByCompanyIdQuery | HIGH | SQL composition / fluent builder |
| A98-10 | UnitsByCompanyIdQuery | HIGH | Parameter binding |
| A98-11 | UnitsByCompanyIdQuery | HIGH | ResultSet column mapping |
| A98-12 | UnitsByCompanyIdQuery | MEDIUM | SQL injection via orderBy |
| A98-13 | UnitsByCompanyIdQuery | MEDIUM | ILIKE filter construction |
| A98-14 | UnitsByCompanyIdQuery | MEDIUM | Factory method |
| A98-15 | UnitsByIdQuery | CRITICAL | No tests |
| A98-16 | UnitsByIdQuery | CRITICAL | KeypadReaderModel.valueOf() unchecked |
| A98-17 | UnitsByIdQuery | HIGH | access_type trim logic |
| A98-18 | UnitsByIdQuery | HIGH | keypad_reader null path |
| A98-19 | UnitsByIdQuery | HIGH | 16-column ResultSet mapping |
| A98-20 | UnitsByIdQuery | HIGH | int-to-long widening / setLong vs setInt |
| A98-21 | UnitsByIdQuery | MEDIUM | Factory method / query entry point |
| A98-22 | UnitsByIdQuery | MEDIUM | getBoolean() NULL coercion |
| A98-23 | UnitsByIdQuery | LOW | Field/method name shadowing |

**Total findings: 23**
**CRITICAL: 4 | HIGH: 10 | MEDIUM: 8 | LOW: 1**
