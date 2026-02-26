# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A91
**Date:** 2026-02-26

## Source Files Audited

1. `src/main/java/com/querybuilder/filters/FilterHandler.java`
2. `src/main/java/com/querybuilder/filters/DateBetweenFilter.java`
3. `src/main/java/com/querybuilder/filters/DateBetweenFilterHandler.java`

## Test Directory Searched

`src/test/java/`

Test files present in the project (all files):
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

Grep results for `FilterHandler`, `DateBetweenFilter`, `DateBetweenFilterHandler` across all test files: **No matches found.**

---

## Reading Evidence

### 1. FilterHandler.java

**Type:** Interface
**Package:** `com.querybuilder.filters`
**Full path:** `src/main/java/com/querybuilder/filters/FilterHandler.java`

**Fields:** None declared.

**Methods:**

| Method | Line | Notes |
|--------|------|-------|
| `getQueryFilter()` | 8 | Returns `String`; no parameters. |
| `prepareStatement(StatementPreparer preparer)` | 10 | Returns `void`; throws `SQLException`. |

**Imports:**
- `com.querybuilder.StatementPreparer` (line 3)
- `java.sql.SQLException` (line 5)

**Known implementors (from main source grep):**
`DateBetweenFilterHandler`, `UnitTypeFilterHandler`, `UnitManufactureFilterHandler`, `StringContainingFilterHandler`, `SessionUnitFilterHandler`, `SessionDriverFilterHandler`, `ImpactLevelFilterHandler`.

---

### 2. DateBetweenFilter.java

**Type:** Interface
**Package:** `com.querybuilder.filters`
**Full path:** `src/main/java/com/querybuilder/filters/DateBetweenFilter.java`

**Fields:** None declared.

**Methods:**

| Method | Line | Notes |
|--------|------|-------|
| `start()` | 6 | Returns `java.util.Date`. |
| `end()` | 7 | Returns `java.util.Date`. |
| `timezone()` | 8 | Returns `String`. |

**Imports:**
- `java.util.Date` (line 3)

**Known implementors (from main source grep):**
`SessionFilterBean` (line 14), `ReportFilterBean` (line 14).

---

### 3. DateBetweenFilterHandler.java

**Type:** Class (concrete), implements `FilterHandler`
**Package:** `com.querybuilder.filters`
**Full path:** `src/main/java/com/querybuilder/filters/DateBetweenFilterHandler.java`

**Fields:**

| Field | Line | Modifiers |
|-------|------|-----------|
| `filter` | 8 | `private final DateBetweenFilter` |
| `fieldName` | 9 | `private final String` |

**Methods (public):**

| Method | Line | Notes |
|--------|------|-------|
| `DateBetweenFilterHandler(DateBetweenFilter filter, String fieldName)` | 11 | Constructor. |
| `getQueryFilter()` | 17 | `@Override`; delegates to private helpers; returns SQL fragment string or `""`. |
| `prepareStatement(StatementPreparer preparer)` | 27 | `@Override`; throws `SQLException`; calls `preparer.addString()` and `preparer.addDate()` conditionally. |

**Methods (private):**

| Method | Line | Notes |
|--------|------|-------|
| `ignoreFilter()` | 34 | Returns `true` if `filter == null`. |
| `filterStartOnly()` | 38 | Returns `true` if `start != null && end == null`. |
| `filterEndOnly()` | 42 | Returns `true` if `start == null && end != null`. |
| `filterBetweenTwoDates()` | 46 | Returns `true` if `start != null && end != null`. |

**Notable implementation details:**
- Line 21 contains a commented-out alternative SQL fragment (`%s::DATE BETWEEN ? AND ?`). The active line 22 uses a timezone-aware variant: `timezone(?, %s at time zone 'UTC')::DATE BETWEEN ? AND ?`.
- `prepareStatement` adds the timezone string first (line 29), then start date (line 30), then end date (line 31). This ordering is tightly coupled to the positional parameter order in the SQL string produced by `getQueryFilter()`. Any mismatch would produce incorrect SQL binding silently.
- When `filterStartOnly()` or `filterEndOnly()` returns true, the SQL fragment uses `>= ?` or `<= ?` respectively, but `prepareStatement` at line 29 unconditionally adds `timezone` if non-null, regardless of which branch was taken. This means the number of `?` placeholders in the SQL and the number of parameters bound by `prepareStatement` may diverge in the start-only or end-only branches when a timezone is present.

---

## Findings

### A91-1 | Severity: CRITICAL | No test class exists for DateBetweenFilterHandler

There is no test file anywhere under `src/test/java/` that references `DateBetweenFilterHandler`. The class contains non-trivial conditional logic across six methods (`getQueryFilter`, `prepareStatement`, and four private predicate methods) and is used in production query builders for session, incident, impact, and pre-ops reports. Zero test coverage exists for any code path in this class.

---

### A91-2 | Severity: CRITICAL | Parameter-count mismatch between getQueryFilter() and prepareStatement() for start-only and end-only cases when timezone is non-null

In `getQueryFilter()` (lines 19-20):
- `filterStartOnly()` returns `" AND %s >= ?"` — **one placeholder**
- `filterEndOnly()` returns `" AND %s <= ?"` — **one placeholder**

In `prepareStatement()` (lines 29-31):
```java
if(filter.timezone() != null) preparer.addString(filter.timezone()); // always adds timezone if present
if (filter.start() != null) preparer.addDate(filter.start());
if (filter.end() != null) preparer.addDate(filter.end());
```

When `filterStartOnly()` is active and `filter.timezone()` is non-null, `prepareStatement` will bind **two parameters** (timezone string + start date) to a SQL fragment that only has **one `?`**. Likewise for `filterEndOnly()`. The timezone parameter is only consumed by the `BETWEEN` variant on line 22. This mismatch would cause a `SQLException` at runtime or silently bind wrong values depending on the JDBC driver. This is a latent production defect that tests would have caught. No test covers these branches.

---

### A91-3 | Severity: HIGH | getQueryFilter() returns empty string for null filter but prepareStatement() also short-circuits — interaction untested

`ignoreFilter()` (line 34-36) returns `true` only when `filter == null`. Both `getQueryFilter()` and `prepareStatement()` return early in this case. The constructor accepts `null` as a valid `DateBetweenFilter` argument with no null guard. While both methods handle null consistently, the null-filter code path (and the interaction between the two methods across that path) is entirely untested.

---

### A91-4 | Severity: HIGH | No tests for getQueryFilter() SQL string correctness across all four branches

`getQueryFilter()` has four distinct return paths:
1. `ignoreFilter()` true — returns `""`
2. `filterStartOnly()` true — returns `" AND %s >= ?"`
3. `filterEndOnly()` true — returns `" AND %s <= ?"`
4. `filterBetweenTwoDates()` true — returns the timezone-aware BETWEEN fragment
5. All conditions false (impossible in current logic, but the method returns `""`) — fallthrough

No test verifies that the correct SQL fragment is returned for any of these branches, nor that `fieldName` is correctly interpolated into the format string.

---

### A91-5 | Severity: HIGH | No tests for prepareStatement() parameter binding order

`prepareStatement()` binds parameters in the order: timezone (if non-null), start date (if non-null), end date (if non-null). This ordering is a contract with the SQL produced by `getQueryFilter()`. No test verifies that `StatementPreparer` methods are called in the correct order or the correct number of times for any scenario.

---

### A91-6 | Severity: HIGH | Commented-out alternative SQL path creates maintenance risk with no regression protection

Line 21 contains a commented-out SQL variant:
```java
// if (filterBetweenTwoDates()) return String.format(" AND %s::DATE BETWEEN ? AND ?", fieldName);
```
The active line 22 uses a different timezone-aware form. There is no test to confirm the active variant is correct or to prevent silent reactivation of the commented code. This commented code suggests the implementation changed but the reason was not documented in tests.

---

### A91-7 | Severity: MEDIUM | No tests for FilterHandler interface contract

`FilterHandler` is a two-method interface (`getQueryFilter()`, `prepareStatement()`) used by at least seven concrete implementations and consumed by four query builder classes. There are no contract tests (e.g., a shared abstract test class or parameterized test suite) verifying that all implementations satisfy the expected behavioral contract (e.g., `getQueryFilter()` returns empty string when filter is inactive; `prepareStatement()` binds zero parameters when filter is inactive).

---

### A91-8 | Severity: MEDIUM | No tests for DateBetweenFilter interface

`DateBetweenFilter` is a three-method interface (`start()`, `end()`, `timezone()`). Its concrete implementations (`SessionFilterBean`, `ReportFilterBean`) are not tested in the context of this interface. No test verifies that the interface methods return expected values for any implementing class in a filter-handler integration scenario.

---

### A91-9 | Severity: MEDIUM | filterBetweenTwoDates() is always reachable only after filterStartOnly() and filterEndOnly() checks — no test confirms mutual exclusivity of predicate logic

The four private predicates (`ignoreFilter`, `filterStartOnly`, `filterEndOnly`, `filterBetweenTwoDates`) form a logical partition of states, but nothing is tested to confirm they are mutually exclusive and collectively exhaustive. Specifically, the case where both `start` and `end` are null and `filter` is non-null falls through all conditions in `getQueryFilter()` and returns `""` silently — this "all-null-non-null-filter" case is a fifth implicit state that is not named, not documented, and not tested.

---

### A91-10 | Severity: LOW | No edge-case tests for fieldName injection (empty string, SQL-special characters, null)

The `fieldName` parameter is injected directly into the SQL fragment via `String.format()` with no validation or escaping. No test verifies behavior when `fieldName` is empty, null, or contains SQL-special characters. A null `fieldName` would produce a `NullPointerException` inside `String.format()` at runtime.

---

### A91-11 | Severity: LOW | No integration test verifying DateBetweenFilterHandler within a query builder (e.g., SessionsByCompanyIdQuery)

`DateBetweenFilterHandler` is instantiated inside at least four query builder classes. No test exercises it through any of those callers, so end-to-end SQL assembly and parameter binding are entirely unverified.

---

## Summary Table

| ID | Severity | Description |
|----|----------|-------------|
| A91-1 | CRITICAL | No test class exists for DateBetweenFilterHandler |
| A91-2 | CRITICAL | Parameter-count mismatch in start-only/end-only cases when timezone is non-null |
| A91-3 | HIGH | Null-filter code path and method interaction untested |
| A91-4 | HIGH | No tests for getQueryFilter() SQL string correctness across all branches |
| A91-5 | HIGH | No tests for prepareStatement() parameter binding order |
| A91-6 | HIGH | Commented-out alternative SQL path creates maintenance risk with no regression protection |
| A91-7 | MEDIUM | No contract tests for FilterHandler interface |
| A91-8 | MEDIUM | No tests for DateBetweenFilter interface implementations |
| A91-9 | MEDIUM | No tests confirming mutual exclusivity of predicate logic |
| A91-10 | LOW | No edge-case tests for fieldName (null, empty, special characters) |
| A91-11 | LOW | No integration test through any query builder caller |

**Total findings: 11**
**Files with zero test coverage: 3 of 3 (100%)**
