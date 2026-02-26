# Audit Report A92 — Pass 2: Test Coverage
**Audit ID:** A92
**Date:** 2026-02-26
**Auditor:** Agent A92
**Pass:** 2 (Test Coverage)

## Scope

| # | Source File |
|---|-------------|
| 1 | `src/main/java/com/querybuilder/filters/ImpactLevelFilter.java` |
| 2 | `src/main/java/com/querybuilder/filters/ImpactLevelFilterHandler.java` |
| 3 | `src/main/java/com/querybuilder/filters/SessionDriverFilter.java` |

**Test directory searched:** `src/test/java/`

---

## Section 1 — Reading Evidence

### 1.1 ImpactLevelFilter.java

**Full path:** `src/main/java/com/querybuilder/filters/ImpactLevelFilter.java`
**Type:** `public interface`
**Package:** `com.querybuilder.filters`

**Imports:**
- `com.bean.ImpactLevel`

**Methods:**

| Line | Signature | Notes |
|------|-----------|-------|
| 6 | `ImpactLevel impactLevel()` | Single abstract method; no parameters; returns `ImpactLevel` enum value |

**Fields / Constants:** None (interface).

**Known implementors (production code):**
- `com.bean.ImpactReportFilterBean` — stores `private ImpactLevel impactLevel` field; implements `impactLevel()` by returning it directly.

---

### 1.2 ImpactLevelFilterHandler.java

**Full path:** `src/main/java/com/querybuilder/filters/ImpactLevelFilterHandler.java`
**Type:** `public class implements FilterHandler`
**Package:** `com.querybuilder.filters`

**Imports:**
- `com.querybuilder.StatementPreparer`

**Fields / Constants:**

| Line | Name | Type | Modifier |
|------|------|------|----------|
| 6 | `filter` | `ImpactLevelFilter` | `private final` |
| 7 | `impactFieldName` | `String` | `private final` |
| 8 | `thresholdFieldName` | `String` | `private final` |

**Methods:**

| Line | Signature | Visibility | Notes |
|------|-----------|------------|-------|
| 10 | `ImpactLevelFilterHandler(ImpactLevelFilter filter, String impactFieldName, String thresholdFieldName)` | `public` | Constructor; assigns all three fields with no null-guards |
| 17 | `String getQueryFilter()` | `public` (`@Override`) | Branches on `ignoreFilter()`, then switch on `filter.impactLevel()` |
| 32 | `void prepareStatement(StatementPreparer preparer)` | `public` (`@Override`) | Body is entirely empty — no parameters are ever bound |
| 36 | `boolean ignoreFilter()` | `private` | Returns `true` when `filter == null` OR `filter.impactLevel() == null` |

**`getQueryFilter()` branch detail (lines 17–29):**

| Condition | Returned value |
|-----------|----------------|
| `ignoreFilter()` true (filter null or level null) | `" AND <impactFieldName> > <thresholdFieldName> "` |
| `ImpactLevel.RED` | `" AND <impactFieldName> > (<thresholdFieldName> * 10) "` |
| `ImpactLevel.AMBER` | `" AND <impactFieldName> BETWEEN (<thresholdFieldName> * 5 + 1) AND (<thresholdFieldName> * 10) "` |
| `ImpactLevel.BLUE` | `" AND <impactFieldName> BETWEEN <thresholdFieldName> AND (<thresholdFieldName> * 5) "` |
| `default` (any future enum value) | `""` — silently drops the filter clause |

**`ignoreFilter()` logic (lines 36–38):**
- `filter == null` → `true`
- `filter.impactLevel() == null` → `true`
- Both non-null → `false`

**`prepareStatement()` (lines 32–34):** empty method body; no-op.

**`FilterHandler` interface contract** (`FilterHandler.java` line 10): `prepareStatement` is declared `throws SQLException`. `ImpactLevelFilterHandler` overrides without re-declaring `throws`.

**Known callers (production code):**
- `ImpactsReportByCompanyIdQuery.java` line 27: `new ImpactLevelFilterHandler(filter, "impact_value", "unit_threshold")`.

---

### 1.3 SessionDriverFilter.java

**Full path:** `src/main/java/com/querybuilder/filters/SessionDriverFilter.java`
**Type:** `public interface`
**Package:** `com.querybuilder.filters`

**Imports:** None.

**Methods:**

| Line | Signature | Notes |
|------|-----------|-------|
| 4 | `Long driverId()` | Single abstract method; no parameters; returns boxed `Long` (nullable by design) |

**Fields / Constants:** None (interface).

**Known implementors (production code):**
- `com.bean.SessionFilterBean` — stores `private Long driverId` field; implements `driverId()` by returning it directly.

**Known handler (closely related):**
- `SessionDriverFilterHandler` — consumes `SessionDriverFilter`; guards with `ignoreFilter()` (`filter == null || filter.driverId() == null`); calls `preparer.addLong(filter.driverId())` when active.

---

## Section 2 — Test Coverage Search Results

**Search terms used against `src/test/java/`:**
- `ImpactLevelFilter`
- `ImpactLevelFilterHandler`
- `SessionDriverFilter`
- `impactLevel`
- `ignoreFilter`
- `getQueryFilter`
- `prepareStatement`
- `driverId`

**Result for all terms:** No matches found in any test file.

**Test files present in `src/test/java/`:**

| Test class | Package | Subject |
|------------|---------|---------|
| `UnitCalibrationImpactFilterTest` | `com.calibration` | `UnitCalibrationImpactFilter` — unrelated calibration logic |
| `UnitCalibrationTest` | `com.calibration` | `UnitCalibration` — unrelated calibration logic |
| `UnitCalibratorTest` | `com.calibration` | `UnitCalibrator` — unrelated calibration logic |
| `ImpactUtilTest` | `com.util` | `ImpactUtil` — exercises `ImpactLevel` enum values but never touches any filter class |

**Conclusion:** Zero direct or indirect test coverage exists for any of the three audited source files or for the SQL-generation logic of `ImpactLevelFilterHandler`.

---

## Section 3 — Findings

---

### A92-1

**Severity:** CRITICAL
**File:** `ImpactLevelFilterHandler.java`
**Subject:** No test coverage whatsoever for `ImpactLevelFilterHandler`

`ImpactLevelFilterHandler` has zero test coverage. The class contains five distinct branching paths in `getQueryFilter()` that emit raw SQL fragments concatenated directly into database queries used by `ImpactsReportByCompanyIdQuery`. None of its public or private methods appear in any test file. Because the output of `getQueryFilter()` is interpolated into SQL via `String.format`, an incorrect SQL fragment silently corrupts every impact-report query without any test to detect the regression.

**Evidence:**
- Grep for `ImpactLevelFilterHandler` in `src/test/java/`: no matches.
- `ImpactsReportByCompanyIdQuery.java` line 27: `new ImpactLevelFilterHandler(filter, "impact_value", "unit_threshold")`.

---

### A92-2

**Severity:** CRITICAL
**File:** `ImpactLevelFilterHandler.java`, `getQueryFilter()` line 18
**Subject:** `ignoreFilter()` fallback emits an active SQL filter instead of a no-op

When `filter` is `null` or `filter.impactLevel()` returns `null`, `getQueryFilter()` returns:

```
" AND impact_value > unit_threshold "
```

This is not a neutral no-op. It applies a "greater-than-threshold" constraint that narrows the result set. A caller passing `null` as the filter to mean "show all impacts regardless of level" will silently receive only above-threshold impacts. This semantic mismatch is entirely untested and undocumented.

**Comparison:** The analogous `SessionDriverFilterHandler.ignoreFilter()` correctly returns an empty string (true no-op) when the filter is null/empty. `ImpactLevelFilterHandler` deviates from that pattern without any test to document or pin the behaviour.

**Evidence:**
- `ImpactLevelFilterHandler.java` lines 18 and 36–38.
- `SessionDriverFilterHandler.java` line 18: `if (ignoreFilter()) return "";`

---

### A92-3

**Severity:** CRITICAL
**File:** `ImpactLevelFilterHandler.java`, `getQueryFilter()` lines 20–28
**Subject:** All three enum-value branches (RED, AMBER, BLUE) and the default branch are untested

The switch statement has four reachable outcomes. None are covered by any test. Specific risks per branch:

- **RED (line 21):** `> (threshold * 10)` — multiplier correctness unverified.
- **AMBER (line 23):** `BETWEEN (threshold * 5 + 1) AND (threshold * 10)` — `thresholdFieldName` referenced twice; the `+ 1` lower-bound offset preventing BLUE/AMBER overlap is unverified.
- **BLUE (line 25):** `BETWEEN threshold AND (threshold * 5)` — boundary alignment with AMBER unverified.
- **default (line 27):** Returns `""`, silently dropping the filter for any future enum value added to `ImpactLevel`. There is no test that would catch such a regression.

**Evidence:**
- `ImpactLevelFilterHandler.java` lines 19–28.
- `ImpactLevel.java` lines 3–7: current enum values `BLUE`, `AMBER`, `RED`.

---

### A92-4

**Severity:** HIGH
**File:** `ImpactLevelFilterHandler.java`, `prepareStatement()` lines 32–34
**Subject:** Empty `prepareStatement` body is unverified; JDBC index consistency risk for the handler chain

`prepareStatement(StatementPreparer preparer)` overrides the `FilterHandler` contract with an entirely empty body. This is intentional because the SQL fragments use column references rather than `?` placeholders, so no JDBC parameter binding is needed. However:

1. There is no test confirming that `prepareStatement` correctly does nothing (does not advance the `StatementPreparer` index). Every other `FilterHandler` in the query's chain that does bind parameters relies on the index counter staying consistent. A future maintainer who adds a `?` placeholder to any `getQueryFilter()` branch without also updating `prepareStatement` will silently produce off-by-one JDBC parameter mismatches for all subsequent handlers.
2. `FilterHandler.prepareStatement` is declared `throws SQLException` (`FilterHandler.java` line 10). `ImpactLevelFilterHandler` overrides it without the `throws` clause — a subtle inconsistency that signals the method was never reviewed through tests.

**Evidence:**
- `ImpactLevelFilterHandler.java` lines 32–34.
- `FilterHandler.java` line 10: `void prepareStatement(StatementPreparer preparer) throws SQLException;`

---

### A92-5

**Severity:** HIGH
**File:** `ImpactLevelFilterHandler.java`, constructor lines 10–14
**Subject:** Constructor accepts null `impactFieldName` / `thresholdFieldName`; `String.format` silently embeds the literal string `"null"` in SQL

The constructor assigns `impactFieldName` and `thresholdFieldName` with no null-guards:

```java
public ImpactLevelFilterHandler(ImpactLevelFilter filter, String impactFieldName, String thresholdFieldName) {
    this.filter = filter;
    this.impactFieldName = impactFieldName;
    this.thresholdFieldName = thresholdFieldName;
}
```

If either string is `null`, every branch of `getQueryFilter()` calls `String.format(...)` and silently embeds the four-character string `"null"` into the SQL fragment (Java's `String.format` converts a null `%s` argument to `"null"`). This produces syntactically valid but semantically broken SQL such as `AND null > null` or `AND impact_value > null`. The database may return no rows or throw an error, both silently from the application's perspective. No test covers this path.

**Evidence:**
- `ImpactLevelFilterHandler.java` lines 10–14 and lines 18, 21, 23, 25: all `String.format` calls use `impactFieldName` and `thresholdFieldName` without null checks.

---

### A92-6

**Severity:** MEDIUM
**File:** `ImpactLevelFilter.java`
**Subject:** No test verifies the `impactLevel()` contract through any implementing class, including the null case

`ImpactReportFilterBean` is the sole production implementor of `ImpactLevelFilter`. There is no test:

1. Verifying that a bean constructed with a given `ImpactLevel` value returns that same value from `impactLevel()`.
2. Verifying the null case — that when `impactLevel` is not set, `impactLevel()` returns `null` — which is the signal `ImpactLevelFilterHandler.ignoreFilter()` depends on to suppress the level-specific filter.

Any Lombok-generated code change on `ImpactReportFilterBean` (e.g., to `@Data` or `@EqualsAndHashCode` annotations) that inadvertently breaks the `impactLevel()` accessor would not be caught by any test.

**Evidence:**
- `ImpactLevelFilter.java` line 6.
- `ImpactReportFilterBean.java` lines 13 and 22–24.
- Grep for `ImpactLevelFilter` in `src/test/java/`: no matches.

---

### A92-7

**Severity:** MEDIUM
**File:** `SessionDriverFilter.java`
**Subject:** No test verifies the `driverId()` contract through any implementing class, including the null case

`SessionFilterBean` is the sole production implementor of `SessionDriverFilter`. There is no test:

1. Verifying that a `SessionFilterBean` built with a non-null `driverId` returns that value from `driverId()`.
2. Verifying the null case — that when `driverId` is not set, `driverId()` returns `null` — which is the signal `SessionDriverFilterHandler.ignoreFilter()` uses to omit the `AND driver_id = ?` clause from session queries. A regression causing `driverId()` to return a non-null value when not set would cause all session queries to filter by an unintended driver ID.

**Evidence:**
- `SessionDriverFilter.java` line 4.
- `SessionFilterBean.java` lines 17 and 33: `private Long driverId;` / `public Long driverId() { return driverId; }`.
- `SessionDriverFilterHandler.java` line 28: `filter.driverId() == null` null guard.
- Grep for `SessionDriverFilter` in `src/test/java/`: no matches.

---

### A92-8

**Severity:** MEDIUM
**File:** `ImpactLevelFilterHandler.java`, `getQueryFilter()` lines 23–25
**Subject:** AMBER/BLUE boundary arithmetic is untested; off-by-one risk

The AMBER and BLUE SQL ranges are:

- BLUE: `impact_value BETWEEN threshold AND (threshold * 5)`
- AMBER: `impact_value BETWEEN (threshold * 5 + 1) AND (threshold * 10)`

The `+ 1` in the AMBER lower bound is the sole mechanism preventing double-counting of the exact value `threshold * 5`. No test confirms:

1. A value exactly equal to `threshold * 5` is captured by BLUE, not AMBER.
2. A value exactly equal to `threshold * 5 + 1` is captured by AMBER, not BLUE.
3. A value exactly equal to `threshold * 10` is captured by AMBER, not RED.
4. A value exactly equal to `threshold * 10 + 1` is captured by RED.

These boundary conditions are precisely the arithmetic errors unit tests are designed to detect.

**Evidence:**
- `ImpactLevelFilterHandler.java` lines 21, 23, 25.

---

### A92-9

**Severity:** LOW
**File:** `ImpactLevelFilterHandler.java`, `getQueryFilter()` / `ignoreFilter()` lines 19 and 37
**Subject:** `filter.impactLevel()` is called twice per invocation; no test for idempotency contract

`ignoreFilter()` (line 37) calls `filter.impactLevel()` to check for null, and then `getQueryFilter()` (line 19) calls it again in the switch. If an implementor of `ImpactLevelFilter` has a side-effectful or expensive `impactLevel()` implementation (e.g., lazy loading from a data store), the two invocations could return different results, causing `ignoreFilter()` to return `false` while the switch subsequently evaluates a null value and falls to `default`. Neither the idempotency expectation nor this double-call pattern is documented in the interface or tested.

**Evidence:**
- `ImpactLevelFilterHandler.java` lines 19 and 37.
- `ImpactLevelFilter.java`: no contract annotation or Javadoc.

---

### A92-10

**Severity:** INFO
**File:** `ImpactLevelFilter.java`, `SessionDriverFilter.java`
**Subject:** Neither interface documents the null-return contract for its single method

Neither interface has Javadoc or annotations describing:

- Whether `impactLevel()` / `driverId()` may return `null` and what that signals to callers.
- Thread-safety or idempotency expectations.

The null-tolerant contract is implied only by reading the handler implementations (`ImpactLevelFilterHandler.ignoreFilter()`, `SessionDriverFilterHandler.ignoreFilter()`), not the interface declarations. No test documents this expected behaviour as executable specification.

**Evidence:**
- `ImpactLevelFilter.java` lines 1–7: no Javadoc.
- `SessionDriverFilter.java` lines 1–5: no Javadoc.

---

## Summary Table

| ID | Severity | File | Subject |
|----|----------|------|---------|
| A92-1 | CRITICAL | `ImpactLevelFilterHandler.java` | Zero test coverage for entire class |
| A92-2 | CRITICAL | `ImpactLevelFilterHandler.java` line 18 | `ignoreFilter()` fallback emits an active SQL filter, not a no-op |
| A92-3 | CRITICAL | `ImpactLevelFilterHandler.java` lines 20–28 | All switch branches (RED, AMBER, BLUE, default) untested |
| A92-4 | HIGH | `ImpactLevelFilterHandler.java` lines 32–34 | Empty `prepareStatement` unverified; JDBC index consistency risk |
| A92-5 | HIGH | `ImpactLevelFilterHandler.java` lines 10–14 | Constructor null field names silently produce `"null"` in SQL |
| A92-6 | MEDIUM | `ImpactLevelFilter.java` | No test for implementor `impactLevel()` contract including null case |
| A92-7 | MEDIUM | `SessionDriverFilter.java` | No test for implementor `driverId()` contract including null case |
| A92-8 | MEDIUM | `ImpactLevelFilterHandler.java` lines 23–25 | AMBER/BLUE boundary arithmetic untested; off-by-one risk |
| A92-9 | LOW | `ImpactLevelFilterHandler.java` lines 19 and 37 | `filter.impactLevel()` called twice; idempotency not documented or tested |
| A92-10 | INFO | `ImpactLevelFilter.java`, `SessionDriverFilter.java` | No interface contract documentation for null-return semantics |

**Total findings: 10**
**CRITICAL: 3 | HIGH: 2 | MEDIUM: 3 | LOW: 1 | INFO: 1**
