# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A75
**Date:** 2026-02-26
**Source Files Audited:**
- `src/main/java/com/dao/GPSDao.java`
- `src/main/java/com/dao/ImpactReportDAO.java`

**Test Directory Searched:** `src/test/java/`

---

## Test Suite Inventory

The following four test files exist in the test directory. Neither audited class is referenced in any of them.

| Test File | Covers |
|---|---|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | `UnitCalibrationImpactFilter` |
| `com/calibration/UnitCalibrationTest.java` | `UnitCalibration` |
| `com/calibration/UnitCalibratorTest.java` | `UnitCalibrator` |
| `com/util/ImpactUtilTest.java` | `ImpactUtil` |

Grep result for `GPSDao` in `src/test/java/`: **no matches**
Grep result for `ImpactReportDAO` in `src/test/java/`: **no matches**

---

## File 1: GPSDao.java

### Reading Evidence

**Class name:** `GPSDao`
**Package:** `com.dao`

**Fields:**

| Field Name | Line | Type | Notes |
|---|---|---|---|
| `log` | 22 | `static Logger` | Raw `Logger` from `InfoLogger.getLogger` |
| `vgps_string` | 25 | `ArrayList` (raw) | Instance field, mutable, unparameterized |
| `Vveh_cd` | 26 | `ArrayList` (raw) | Instance field, mutable, unparameterized; non-standard capitalization |
| `QUERY_UNIT_GPS` | 28–33 | `static final String` | Parameterized SQL string used by `getUnitGPSData` |

**Methods:**

| Method Name | Line | Visibility | Notes |
|---|---|---|---|
| `getUnitGPSData(String compId, String[] unitIds, String dateFormat, String timezone)` | 35 | `public static` | Returns `List<String>` |
| `getGPSLocations(String[] unitList)` | 74 | `public` | Returns `void`; mutates instance fields |
| `getUnitById(String id)` | 122 | `public` | Returns `ArrayList<UnitBean>` |
| `getVgps_string()` | 177 | `public` | Getter for `vgps_string` |
| `getVveh_cd()` | 181 | `public` | Getter for `Vveh_cd` |
| `setVgps_string(ArrayList)` | 185 | `public` | Setter for `vgps_string` |
| `setVveh_cd(ArrayList)` | 189 | `public` | Setter for `Vveh_cd` |

---

## File 2: ImpactReportDAO.java

### Reading Evidence

**Class name:** `ImpactReportDAO`
**Package:** `com.dao`

**Fields:**

| Field Name | Line | Type | Notes |
|---|---|---|---|
| `theInstance` | 12 | `static ImpactReportDAO` | Singleton instance; not volatile |

**Methods:**

| Method Name | Line | Visibility | Notes |
|---|---|---|---|
| `getInstance()` | 14 | `public static` | Double-checked locking singleton factory |
| `ImpactReportDAO()` | 26 | `private` | Constructor |
| `countImpactsToday(Long compId, String timezone)` | 29 | `public` | Delegates to `ImpactsByCompanyIdQuery.count(...).query()` |
| `getImpactReport(Long compId, ImpactReportFilterBean filter, String format, String timezone)` | 33 | `public` | Delegates to `ImpactsByCompanyIdQuery.report(...).query(timezone, format)` |

---

## Findings

### GPSDao.java

---

**A75-1 | Severity: CRITICAL | No test class exists for GPSDao**

There is no test file anywhere under `src/test/java/` that references `GPSDao`. The class has zero test coverage. All methods, branches, and error paths are untested.

---

**A75-2 | Severity: CRITICAL | getGPSLocations — SQL injection via unsanitized string concatenation**

`getGPSLocations` (line 85–88) builds a SQL query by directly concatenating elements of the caller-supplied `unitList` array into the query string without using a `PreparedStatement`. There is no test verifying rejection or sanitization of malicious input such as `1; DROP TABLE unit` or `1 OR 1=1`. This is a security-critical code path that must have both positive and negative test coverage.

---

**A75-3 | Severity: CRITICAL | getUnitById — SQL injection via unsanitized string concatenation**

`getUnitById` (line 136–139) constructs SQL by directly concatenating the caller-supplied `id` parameter. No `PreparedStatement` is used. There is no test covering injection input. This is the same class of vulnerability as A75-2 and represents a security-critical untested path.

---

**A75-4 | Severity: HIGH | getUnitGPSData — null unitIds guard branch not tested**

`getUnitGPSData` (line 42–44) returns an empty list early when `unitIds == null`. No test verifies this branch. Additionally the `compId` parameter is accepted but never used in the method body; no test captures that the parameter is silently ignored.

---

**A75-5 | Severity: HIGH | getUnitGPSData — empty unitIds array not tested**

When `unitIds` is a non-null but zero-length array the loop at line 45 is skipped and an empty list is returned. This edge case is not tested.

---

**A75-6 | Severity: HIGH | getUnitGPSData — Integer.parseInt throws NumberFormatException on non-numeric unitId**

Line 47 calls `Integer.parseInt(unitId)` on each element of `unitIds` with no try/catch. A non-numeric string causes an unhandled `NumberFormatException`. There is no test covering this path.

---

**A75-7 | Severity: HIGH | getUnitGPSData — DBUtil.queryForObjects silently swallows SQLException**

`DBUtil.queryForObjects` (DBUtil.java line 75–77) catches `SQLException`, prints the stack trace, and returns an empty list rather than rethrowing. `getUnitGPSData` therefore silently returns incomplete results when a database error occurs. No test verifies the silent-failure behavior or that the caller receives a partial-empty list on database error.

---

**A75-8 | Severity: HIGH | getGPSLocations — instance field state contamination across calls**

`getGPSLocations` appends to the instance-level `vgps_string` and `Vveh_cd` lists (lines 94, 105) without clearing them first. A second call accumulates results on top of the first call's results. No test verifies or challenges this stateful accumulation behavior. The lack of reset makes the class non-reusable per instance without manual setter calls.

---

**A75-9 | Severity: HIGH | getGPSLocations — Double.parseDouble throws NumberFormatException on bad latitude/longitude**

Line 102 calls `Double.parseDouble(latitude)` and `Double.parseDouble(longitude)` on raw `ResultSet` string values. If the database column is null or contains a non-numeric value, an unhandled `NumberFormatException` is thrown inside the try block, which is caught by the `catch(Exception e)` at line 108 and rethrown as `SQLException`. No test covers this path.

---

**A75-10 | Severity: HIGH | getUnitById — no test for unit not found (empty ResultSet)**

`getUnitById` returns an empty `ArrayList` when `rs.next()` returns false (no row for the given id). This is not tested.

---

**A75-11 | Severity: HIGH | getUnitById — no test for invalid (non-numeric) id**

The `id` parameter is typed as `String` but concatenated directly into SQL. If the value is null or non-numeric the database will return a syntax error, which is caught and rethrown as `SQLException`. No test covers null id or non-numeric id input.

---

**A75-12 | Severity: MEDIUM | getUnitGPSData — JSON output not tested for special characters in field values**

The JSON string at lines 64–65 is assembled by direct string concatenation. If `vehName`, `manufacturer`, `type`, or `power` contains a double-quote, backslash, or newline character, the resulting JSON is malformed. No test covers field values containing characters that require JSON escaping.

---

**A75-13 | Severity: MEDIUM | getUnitGPSData — null timestamp from ResultSet causes NullPointerException**

`GPSUnitBean.timeStmp` is populated from `rs.getTimestamp("gps_time")`. If the database column is NULL, `getTimestamp` returns null. `DateUtil.formatDateTime(DateUtil.utc2Local(null, timezone), dateFormat)` at line 64 is likely to throw a `NullPointerException`. No test covers a null GPS timestamp.

---

**A75-14 | Severity: MEDIUM | getUnitGPSData — null or invalid timezone not tested**

The `timezone` parameter is passed to `DateUtil.utc2Local`. No test verifies behavior when `timezone` is null, empty, or an unrecognized timezone identifier.

---

**A75-15 | Severity: MEDIUM | getUnitGPSData — null or invalid dateFormat not tested**

The `dateFormat` parameter is passed to `DateUtil.formatDateTime`. No test verifies behavior when `dateFormat` is null or an invalid pattern string.

---

**A75-16 | Severity: MEDIUM | getGPSLocations — null unitList array causes NullPointerException**

`getGPSLocations` (line 84) calls `unitList.length` without a null guard. Passing null throws a `NullPointerException` which propagates through the `catch(Exception e)` block and is rethrown as `SQLException`. No test covers a null `unitList`.

---

**A75-17 | Severity: MEDIUM | getGPSLocations — empty unitList array not tested**

When `unitList` is empty the loop body never executes, `vgps_string` and `Vveh_cd` remain in whatever state they were in before the call, and no exception is thrown. No test verifies this behavior.

---

**A75-18 | Severity: MEDIUM | getGPSLocations — result data not accessible via return value; accessor methods not tested**

Results of `getGPSLocations` are stored in instance fields `vgps_string` and `Vveh_cd` and retrieved via `getVgps_string()` and `getVveh_cd()`. No test verifies that after a successful call the accessor methods return the expected data.

---

**A75-19 | Severity: MEDIUM | Getter/setter methods not tested**

`getVgps_string()`, `getVveh_cd()`, `setVgps_string(ArrayList)`, and `setVveh_cd(ArrayList)` (lines 177–191) have no test coverage whatsoever.

---

**A75-20 | Severity: LOW | getUnitGPSData — compId parameter is accepted but never used**

The parameter `compId` at line 35 is declared and logged indirectly (the log message says "getUnitGPSData") but is never referenced in any query or logic. This silent dead parameter could mask a requirement gap. No test asserts its effect on results.

---

**A75-21 | Severity: LOW | Raw ArrayList types used for instance fields and getters/setters**

Fields `vgps_string` (line 25) and `Vveh_cd` (line 26), and their corresponding getters and setters, use raw `ArrayList` rather than parameterized types. This is a type-safety gap. No test exercises storing or retrieving typed content through these fields.

---

### ImpactReportDAO.java

---

**A75-22 | Severity: CRITICAL | No test class exists for ImpactReportDAO**

There is no test file anywhere under `src/test/java/` that references `ImpactReportDAO`. The class has zero test coverage. All methods and branches are untested.

---

**A75-23 | Severity: HIGH | getInstance — singleton theInstance field is not volatile; double-checked locking is broken under Java memory model without volatile**

`theInstance` (line 12) is declared as `private static ImpactReportDAO theInstance` without the `volatile` keyword. Under the Java Memory Model, without `volatile`, the double-checked locking pattern at lines 15–23 is not guaranteed to be thread-safe: a second thread may observe a non-null but incompletely constructed object. No test exercises concurrent calls to `getInstance()` or verifies that the same instance is always returned.

---

**A75-24 | Severity: HIGH | countImpactsToday — no test for null compId**

`countImpactsToday` (line 29) passes `compId` directly to `ImpactsByCompanyIdQuery.count`. If `compId` is null, behavior depends on the query builder implementation. No test covers a null `compId`.

---

**A75-25 | Severity: HIGH | countImpactsToday — no test for null timezone**

The `timezone` parameter is passed to the query builder without null-checking. No test covers a null or empty timezone string.

---

**A75-26 | Severity: HIGH | getImpactReport — no test for null compId, null filter, null format, or null timezone**

`getImpactReport` (line 33–38) passes all four parameters directly to `ImpactsByCompanyIdQuery.report` and `.query` without any null checks. No test covers null or missing values for any of these parameters.

---

**A75-27 | Severity: HIGH | getImpactReport — no test for SQLException propagation**

`getImpactReport` declares `throws SQLException` and propagates any exception thrown by the query execution chain. No test verifies that an underlying `SQLException` is correctly propagated to callers (e.g., via a mock of the query builder).

---

**A75-28 | Severity: HIGH | countImpactsToday — no test for SQLException propagation**

Same as A75-27: `countImpactsToday` declares `throws SQLException` but no test verifies propagation behavior on database failure.

---

**A75-29 | Severity: MEDIUM | getInstance — no test verifying singleton contract**

No test verifies that multiple calls to `getInstance()` return the same object reference. No test verifies that the singleton cannot be bypassed.

---

**A75-30 | Severity: MEDIUM | getInstance — no test for thread-safety**

Related to A75-23: beyond the volatile gap, no concurrent stress test validates that `getInstance()` is safe when called simultaneously from multiple threads.

---

**A75-31 | Severity: MEDIUM | countImpactsToday — return value not tested for expected range**

No test verifies that `countImpactsToday` returns a non-negative integer, or handles the case where the query returns zero impacts vs. a positive count.

---

**A75-32 | Severity: MEDIUM | getImpactReport — returned ImpactReportBean content not tested**

No test verifies the structure or content of the `ImpactReportBean` returned by `getImpactReport`. Empty filter, date-bounded filter, and format-specific output variations are all untested.

---

**A75-33 | Severity: LOW | Private constructor not tested**

The private constructor at line 26 is trivially empty but its existence (and the enforcement that it cannot be instantiated externally) is not verified by any test using reflection or other means.

---

## Summary Table

| ID | Severity | Class | Finding |
|---|---|---|---|
| A75-1 | CRITICAL | GPSDao | No test class exists |
| A75-2 | CRITICAL | GPSDao | SQL injection in getGPSLocations via string concatenation |
| A75-3 | CRITICAL | GPSDao | SQL injection in getUnitById via string concatenation |
| A75-4 | HIGH | GPSDao | getUnitGPSData null unitIds branch not tested |
| A75-5 | HIGH | GPSDao | getUnitGPSData empty unitIds array not tested |
| A75-6 | HIGH | GPSDao | getUnitGPSData NumberFormatException on non-numeric unitId |
| A75-7 | HIGH | GPSDao | DBUtil.queryForObjects silently swallows SQLException |
| A75-8 | HIGH | GPSDao | getGPSLocations instance field state contamination across calls |
| A75-9 | HIGH | GPSDao | getGPSLocations NumberFormatException on bad lat/lon |
| A75-10 | HIGH | GPSDao | getUnitById no test for empty ResultSet |
| A75-11 | HIGH | GPSDao | getUnitById no test for null/non-numeric id |
| A75-12 | MEDIUM | GPSDao | getUnitGPSData JSON injection via special characters in field values |
| A75-13 | MEDIUM | GPSDao | getUnitGPSData null GPS timestamp causes NullPointerException |
| A75-14 | MEDIUM | GPSDao | getUnitGPSData null/invalid timezone not tested |
| A75-15 | MEDIUM | GPSDao | getUnitGPSData null/invalid dateFormat not tested |
| A75-16 | MEDIUM | GPSDao | getGPSLocations null unitList causes NullPointerException |
| A75-17 | MEDIUM | GPSDao | getGPSLocations empty unitList not tested |
| A75-18 | MEDIUM | GPSDao | getGPSLocations results only accessible via accessor methods; not tested |
| A75-19 | MEDIUM | GPSDao | Getter/setter methods not tested |
| A75-20 | LOW | GPSDao | getUnitGPSData compId parameter silently unused |
| A75-21 | LOW | GPSDao | Raw ArrayList types on instance fields and accessors |
| A75-22 | CRITICAL | ImpactReportDAO | No test class exists |
| A75-23 | HIGH | ImpactReportDAO | theInstance not volatile; double-checked locking broken |
| A75-24 | HIGH | ImpactReportDAO | countImpactsToday null compId not tested |
| A75-25 | HIGH | ImpactReportDAO | countImpactsToday null timezone not tested |
| A75-26 | HIGH | ImpactReportDAO | getImpactReport null parameter inputs not tested |
| A75-27 | HIGH | ImpactReportDAO | getImpactReport SQLException propagation not tested |
| A75-28 | HIGH | ImpactReportDAO | countImpactsToday SQLException propagation not tested |
| A75-29 | MEDIUM | ImpactReportDAO | getInstance singleton contract not verified by test |
| A75-30 | MEDIUM | ImpactReportDAO | getInstance thread-safety not tested |
| A75-31 | MEDIUM | ImpactReportDAO | countImpactsToday return value range not tested |
| A75-32 | MEDIUM | ImpactReportDAO | getImpactReport returned bean content not tested |
| A75-33 | LOW | ImpactReportDAO | Private constructor not tested |

---

**Total findings: 33**
CRITICAL: 4 | HIGH: 16 | MEDIUM: 10 | LOW: 3
