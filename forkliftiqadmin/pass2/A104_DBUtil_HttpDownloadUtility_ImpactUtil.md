# Test Coverage Audit Report
**Audit Run:** 2026-02-26-01
**Pass:** 2 (Test Coverage Audit)
**Agent ID:** A104
**Date:** 2026-02-26

**Source Files Audited:**
- `src/main/java/com/util/DBUtil.java`
- `src/main/java/com/util/HttpDownloadUtility.java`
- `src/main/java/com/util/ImpactUtil.java`

**Test File Reviewed:**
- `src/test/java/com/util/ImpactUtilTest.java`

---

## Section 1: Reading Evidence

### 1.1 DBUtil.java

**Class name:** `DBUtil`
**Package:** `com.util`

**Fields:**

| Field Name | Line | Type | Visibility |
|---|---|---|---|
| `databaseName` | 22 | `static String` | `private static` |

**Methods:**

| Method Signature | Line |
|---|---|
| `public static Connection getConnection()` | 24 |
| `public static Connection getConnection(boolean autoCommit)` | 28 |
| `private static void ensureDatabaseNameIsSet()` | 43 |
| `public static void closeConnection(Connection conn)` | 57 (`@Deprecated`) |
| `public static <T> List<T> queryForObjects(String, PreparedStatementHandler, ResultMapper<T>)` | 61 |
| `public static <T> List<T> queryForObjectsWithRowHandler(String, PreparedStatementHandler, RowHandler<T>)` | 84 |
| `public static <T> List<T> queryForObjects(Connection, String, PreparedStatementHandler, ResultMapper<T>)` | 107 |
| `public static <T> Optional<T> queryForObject(String, ResultMapper<T>)` | 128 |
| `public static <T> Optional<T> queryForObject(String, PreparedStatementHandler, ResultMapper<T>)` | 148 |
| `public static <T> Optional<T> queryForObject(Connection, String, PreparedStatementHandler, ResultMapper<T>)` | 172 |
| `public static int updateObject(Connection, String, PreparedStatementHandler)` | 195 |
| `public static int updateObject(String, PreparedStatementHandler)` | 211 |
| `public static void executeStatementWithRollback(String, PreparedStatementHandler)` | 228 |

**Inner interfaces:**

| Interface Name | Line |
|---|---|
| `PreparedStatementHandler` | 247 |
| `ResultMapper<T>` | 251 |
| `RowHandler<T>` | 255 |

---

### 1.2 HttpDownloadUtility.java

**Class name:** `HttpDownloadUtility`
**Package:** `com.util`

**Fields:**

| Field Name | Line | Type | Visibility |
|---|---|---|---|
| `log` | 23 | `static Logger` | `private static` |
| `BUFFER_SIZE` | 25 | `static final int` | `private static` |
| `saveFilePath` | 26 | `static String` | `private static` |

**Methods:**

| Method Signature | Line |
|---|---|
| `public static void downloadFile(String fileName, String fileURL, String saveDir)` | 35 |
| `public static int sendPost(String fileName, String input, String saveDir)` | 88 |
| `public static String getSaveFilePath()` | 186 |
| `public static void setSaveFilePath(String saveFilePath)` | 190 |

---

### 1.3 ImpactUtil.java

**Class name:** `ImpactUtil`
**Package:** `com.util`

**Fields:**

| Field Name | Line | Type | Visibility |
|---|---|---|---|
| `G_FORCE_COEFFICIENT` | 6 | `static final double` | `private static final` |
| `BLUE_IMPACT_COEFFICIENT` | 7 | `static final double` | `private static final` |
| `AMBER_IMPACT_COEFFICIENT` | 8 | `static final double` | `private static final` |
| `RED_IMPACT_COEFFICIENT` | 9 | `static final double` | `private static final` |

**Methods:**

| Method Signature | Line |
|---|---|
| `public static double calculateGForceOfImpact(long impactValue)` | 11 |
| `public static double calculateGForceRequiredForImpact(double impactThreshold, ImpactLevel impactLevel)` | 15 |
| `private static double getImpactLevelCoefficient(ImpactLevel impactLevel)` | 19 |
| `public static String getCSSColor(ImpactLevel impactLevel)` | 32 |
| `public static ImpactLevel calculateImpactLevel(int impactValue, int impactThreshold)` | 45 |

**Inner class:**

| Class Name | Line |
|---|---|
| `UnhandledImpactLevelException` (extends `IllegalArgumentException`) | 52 |
| `UnhandledImpactLevelException(ImpactLevel)` constructor | 53 |

---

## Section 2: Indirect Coverage Search Results

Grep of the entire test directory (`src/test/java/`) for each class name:

- **DBUtil**: No matches found in any test file.
- **HttpDownloadUtility**: No matches found in any test file.
- **ImpactUtil**: Referenced only in `ImpactUtilTest.java`.

The test directory contains exactly four test files total:
- `src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java`
- `src/test/java/com/calibration/UnitCalibrationTest.java`
- `src/test/java/com/calibration/UnitCalibratorTest.java`
- `src/test/java/com/util/ImpactUtilTest.java`

None of the calibration tests reference `DBUtil` or `HttpDownloadUtility`. No indirect coverage of those two classes exists anywhere in the test suite.

---

## Section 3: Findings

---

### DBUtil.java Findings

**A104-1 | Severity: CRITICAL | DBUtil has zero test coverage — no test class exists**

`DBUtil` is the sole database access layer for the entire application. There is no test file for `DBUtil` anywhere in the test directory. All 13 methods (including all `queryForObjects`, `queryForObject`, `updateObject`, and `executeStatementWithRollback` overloads) are completely untested.

---

**A104-2 | Severity: CRITICAL | SQLException silently swallowed in six query/update methods — errors are invisible to callers**

In six methods — `queryForObjects(String,...)` (line 75), `queryForObjectsWithRowHandler` (line 98), `queryForObjects(Connection,...)` (line 119), `queryForObject(String, ResultMapper)` (line 140), `queryForObject(String, PreparedStatementHandler, ResultMapper)` (line 164), `queryForObject(Connection,...)` (line 186), `updateObject(Connection,...)` (line 203), and `updateObject(String,...)` (line 220) — `SQLException` is caught and only printed to stderr via `e.printStackTrace()`, then execution continues. The methods all declare `throws SQLException` in their signatures but never actually propagate the exception. Callers receive empty lists or empty `Optional` results that are indistinguishable from legitimate "no rows found" results. This silent failure makes defect diagnosis extremely difficult and cannot be detected without tests that inject SQL failures. No such tests exist.

---

**A104-3 | Severity: CRITICAL | queryForObject(String, ResultMapper) — connection opened before try block, never closed on getConnection() failure path**

In `queryForObject(String query, ResultMapper<T> mapper)` (line 128–146), `conn = getConnection()` is called at line 131, outside the try/catch/finally block. If `getConnection()` succeeds but an exception occurs before the `finally` block executes, cleanup still occurs. However, if `getConnection()` itself throws, no `finally` runs and no connection leak occurs. More critically: the `conn` variable is declared at line 129, `getConnection()` is called at line 131, and the `finally` block at line 142 calls `DbUtils.closeQuietly(conn, stmt, rs)`. This asymmetry with all other overloads (which initialise `conn = null` inside try) is an inconsistent pattern. More critically, if `conn.prepareStatement(query)` throws and is caught at line 140, the caught block only calls `e.printStackTrace()` — it does not re-throw — so the `finally` still runs and the connection is closed. No test covers the exception path of this particular overload.

---

**A104-4 | Severity: HIGH | executeStatementWithRollback — rollback itself can throw and mask the original exception**

In `executeStatementWithRollback` (line 228–244), the catch block at line 238 calls `conn.rollback()` (line 239) without a try/catch. If `conn.rollback()` itself throws a `SQLException`, that new exception propagates and completely masks the original exception that caused the rollback. The original failure context is lost. No test exercises this failure path.

---

**A104-5 | Severity: HIGH | ensureDatabaseNameIsSet — logic relies on JVM arguments that cannot be set in unit tests; databaseName is mutable static state shared across all tests**

`databaseName` (line 22) is a `private static` field that is never reset. In a test environment, `ManagementFactory.getRuntimeMXBean().getInputArguments()` will not contain `-Ddb=...` unless explicitly passed at JVM startup, so `databaseName` will always fall through to `RuntimeConf.database` (line 53). There is no mechanism to inject a test database name without either modifying `RuntimeConf.database` (a public mutable static) or passing JVM arguments. Because the field is `static` and non-resettable, test isolation is impossible without reflection. No tests exist to verify this resolution logic.

---

**A104-6 | Severity: HIGH | updateObject(Connection, ...) returns -1 on SQLException instead of propagating the exception**

`updateObject(Connection conn, String query, PreparedStatementHandler handler)` at line 195 catches `SQLException` and returns `-1` (line 208). Callers that receive `-1` have no way to distinguish "zero rows affected" (a valid outcome for some queries) from "exception occurred". The method signature declares `throws SQLException` but the exception is never thrown. No test covers this negative return path.

---

**A104-7 | Severity: HIGH | updateObject(String, ...) returns -1 on SQLException instead of propagating the exception**

Same issue as A104-6 but for the `updateObject(String query, PreparedStatementHandler handler)` overload at line 211. The `catch` at line 220 swallows the exception and returns `-1` at line 225. No test covers this path.

---

**A104-8 | Severity: MEDIUM | getConnection() zero-argument overload — no test for autoCommit=true delegation**

`getConnection()` (line 24) delegates to `getConnection(true)`. No test verifies this delegation. Integration tests would require a live JNDI context.

---

**A104-9 | Severity: MEDIUM | NamingException converted to SQLException — error message quality untested**

In `getConnection(boolean autoCommit)` (line 38–40), `NamingException` is wrapped in a `SQLException` with the message `"Unable to get datasource for " + databaseName`. If `databaseName` is `null` at this point (e.g., before `ensureDatabaseNameIsSet()` runs, which is impossible given the code order, but illustrative), the message would read `"Unable to get datasource for null"`. No test verifies the wrapping or the resulting message content.

---

**A104-10 | Severity: MEDIUM | queryForObjects(Connection,...) closes stmt and rs separately instead of using the three-argument closeQuietly — inconsistent resource cleanup**

In `queryForObjects(Connection conn, String query, ...)` (lines 122–124), the `finally` block calls `DbUtils.closeQuietly(stmt)` and then separately `DbUtils.closeQuietly(rs)`. All other methods use the three-argument form `DbUtils.closeQuietly(conn, stmt, rs)`. While functionally equivalent, the separate calls are inconsistent and, more importantly, if closing `stmt` throws an unchecked exception, `rs` would not be closed — a resource leak. No test exercises this close sequence.

---

**A104-11 | Severity: MEDIUM | closeConnection is @Deprecated with no replacement documented and still publicly accessible**

`closeConnection(Connection conn)` (line 57) is annotated `@Deprecated` but no Javadoc explains what callers should use instead. It remains public and callable. No test validates its behaviour or confirms it properly delegates to `DbUtils.closeQuietly`.

---

**A104-12 | Severity: LOW | queryForObject — "unique result expected" branch untested (rs.isLast() check)**

In both `queryForObject` overloads that check `rs.isLast()` (lines 137 and 161), the branch that throws `new SQLException("Unique result expected, got more than one")` is executed only when the ResultSet has more than one row. No test exercises this guard; the exception-throwing branch has zero coverage.

---

### HttpDownloadUtility.java Findings

**A104-13 | Severity: CRITICAL | HttpDownloadUtility has zero test coverage — no test class exists**

There is no test file for `HttpDownloadUtility` anywhere in the test directory. All four methods (`downloadFile`, `sendPost`, `getSaveFilePath`, `setSaveFilePath`) are completely untested.

---

**A104-14 | Severity: CRITICAL | Hardcoded API authentication token in sendPost at line 105**

`sendPost` (line 105) sets the request header `X-AUTH-TOKEN` to the literal value `"noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE"`. This token is committed in plain text in source code. Any test that exercises this method would also expose the credential. No test exists, but the credential exposure is a security finding independent of test coverage.

---

**A104-15 | Severity: CRITICAL | sendPost ignores fileName parameter — silently overwrites it with a hardcoded value**

`sendPost(String fileName, String input, String saveDir)` (line 88) immediately reassigns `fileName = "pandora-usage-dashboard"` at line 90, discarding the caller-supplied argument entirely. This makes the public method signature misleading and unverifiable. No test documents or asserts this behaviour.

---

**A104-16 | Severity: CRITICAL | sendPost swallows OutputStream write exception — partial POST body sent without error**

In `sendPost` (lines 110–118), the try/catch around `os.write(input.getBytes("UTF-8"))` catches `Exception` and only calls `e.printStackTrace()`. If the write fails (e.g., connection reset), execution continues to `con.getResponseCode()` at line 120 — which may block, succeed with a partial body, or throw — and the caller is never notified of the write failure. No test exercises this path.

---

**A104-17 | Severity: CRITICAL | downloadFile and sendPost: InputStream and FileOutputStream not closed in a finally block — resource leak on exception**

In `downloadFile` (lines 60–77) and `sendPost` (lines 157–175), `InputStream` and `FileOutputStream` are opened and closed via explicit calls at the end of the try block. If an exception occurs during `inputStream.read()` or `outputStream.write()`, the streams are not closed because the close statements are at the end of the try body and the catch only calls `e.printStackTrace()`. Both streams leak on any I/O error. No test exercises these failure paths.

---

**A104-18 | Severity: HIGH | downloadFile — non-HTTP_OK response path only logs; caller receives no indication of failure**

`downloadFile` (lines 80–82) logs `"No file to download. Server replied HTTP code: " + responseCode` when `responseCode != HTTP_OK` but does not throw an exception. The method's return type is `void`, so callers have no programmatic way to detect that the download failed. No test asserts behaviour on non-200 responses.

---

**A104-19 | Severity: HIGH | sendPost — non-HTTP_OK response path only logs; caller receives the raw response code but error body is discarded**

`sendPost` (lines 178–180) logs a message on non-HTTP_OK response but does not read the error stream from `con.getErrorStream()` (the code to do so is commented out at lines 138–150). The error body is inaccessible to the caller. No test verifies error handling on non-200 responses.

---

**A104-20 | Severity: HIGH | saveFilePath is a mutable static field — concurrent calls to downloadFile/sendPost cause race conditions**

`saveFilePath` (line 26) is `private static String`. Both `downloadFile` (line 63) and `sendPost` (line 160) write to it. In a multi-threaded environment (e.g., servlet container handling concurrent requests), simultaneous downloads overwrite each other's path. `getSaveFilePath()` will return whichever thread wrote last. No test exercises concurrent access or validates thread safety.

---

**A104-21 | Severity: HIGH | downloadFile — Content-Disposition parsing uses fixed offset (+10) without validating the index value**

In `downloadFile` (line 50), when a `Content-Disposition` header is found with `filename=`, the code extracts the filename via `disposition.substring(index + 10, disposition.length() - 1)`. The magic offset `10` accounts for `filename="` (9 chars + the leading quote). If the header value is malformed (e.g., `filename=` without quotes, or with extra whitespace), `substring` will either return wrong data or throw `StringIndexOutOfBoundsException`. No test exercises header parsing.

---

**A104-22 | Severity: MEDIUM | sendPost — URL constructed by string concatenation of RuntimeConf.APIURL and a hardcoded filename; APIURL points to an AWS EC2 IP address**

`sendPost` constructs `url = RuntimeConf.APIURL + fileName` (line 91), where `RuntimeConf.APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"`. The URL uses plain HTTP (not HTTPS), and the destination is a hardcoded external IP. The `HttpsURLConnection` import (line 17) and commented-out HTTPS usage (line 98) indicate a deliberate downgrade to HTTP. No test verifies URL construction or the HTTP-vs-HTTPS choice.

---

**A104-23 | Severity: MEDIUM | downloadFile and sendPost: Exception caught instead of IOException — overly broad catch masks programming errors**

Both `downloadFile` (line 74) and `sendPost` (lines 115 and 172) catch `Exception` rather than `IOException`. This broad catch masks `RuntimeException`, `NullPointerException`, and other programming errors as if they were normal I/O exceptions, making defect diagnosis harder. No tests cover any of these catch paths.

---

**A104-24 | Severity: LOW | getSaveFilePath and setSaveFilePath are untested**

`getSaveFilePath()` (line 186) and `setSaveFilePath(String)` (line 190) are simple accessor methods for the shared static field. No tests verify their behaviour, including the interaction between `setSaveFilePath` and subsequent calls to `downloadFile` or `sendPost`.

---

### ImpactUtil.java Findings

**A104-25 | Severity: HIGH | calculateImpactLevel returns null when impactValue is at or below threshold — null return undocumented and untested**

`calculateImpactLevel(int impactValue, int impactThreshold)` (line 45–50) returns `null` when `impactValue <= impactThreshold * BLUE_IMPACT_COEFFICIENT` (i.e., the impact does not exceed even the lowest threshold). The `ImpactUtilTest.ReturnsImpactLevelOfImpact` test only asserts the three non-null cases (BLUE, AMBER, RED). The null-return branch is never tested. Callers that receive `null` and pass it to `getCSSColor` or `calculateGForceRequiredForImpact` will trigger `UnhandledImpactLevelException` or a `NullPointerException`, respectively.

---

**A104-26 | Severity: HIGH | calculateImpactLevel boundary values are untested — off-by-one errors in threshold comparisons not detected**

`calculateImpactLevel` uses strict greater-than (`>`) comparisons:
- `impactValue > impactThreshold * RED_IMPACT_COEFFICIENT` (line 46)
- `impactValue > impactThreshold * AMBER_IMPACT_COEFFICIENT` (line 47)
- `impactValue > impactThreshold * BLUE_IMPACT_COEFFICIENT` (line 48)

The test at line 16–18 of `ImpactUtilTest` uses values that are well inside each range (e.g., 678901 vs threshold 500000 * 1 = 500000 for BLUE). None of the following boundary cases are tested:
- `impactValue == impactThreshold * 1` (should return null, not BLUE)
- `impactValue == impactThreshold * 1 + 1` (first value that returns BLUE)
- `impactValue == impactThreshold * 5` (should return BLUE, not AMBER)
- `impactValue == impactThreshold * 5 + 1` (first value that returns AMBER)
- `impactValue == impactThreshold * 10` (should return AMBER, not RED)
- `impactValue == impactThreshold * 10 + 1` (first value that returns RED)

---

**A104-27 | Severity: HIGH | UnhandledImpactLevelException — default branches in getImpactLevelCoefficient and getCSSColor are untested**

The `default` case in `getImpactLevelCoefficient` (line 27) and `getCSSColor` (line 41) both throw `UnhandledImpactLevelException`. Because `ImpactLevel` is a three-value enum (`BLUE`, `AMBER`, `RED`) with all three cases handled, these branches can only be reached if a new enum constant is added without updating `ImpactUtil`. No test exercises the `default` branch or verifies that `UnhandledImpactLevelException` is thrown with the correct message. The exception constructor at line 53–55 is also completely uncovered.

---

**A104-28 | Severity: MEDIUM | calculateGForceOfImpact — only one positive value tested; zero, negative, and large values not covered**

`calculateGForceOfImpact(long impactValue)` at line 11 is tested with a single positive value (500000) in `ReturnsGForceForImpact`. The following cases are not tested:
- `impactValue = 0` (should return 0.0)
- `impactValue < 0` (Math.sqrt of a negative long produces NaN; this is likely unintentional behaviour)
- Very large values approaching `Long.MAX_VALUE` (potential floating-point precision loss)

---

**A104-29 | Severity: MEDIUM | calculateGForceRequiredForImpact — negative or zero impactThreshold not tested**

`calculateGForceRequiredForImpact(double impactThreshold, ImpactLevel impactLevel)` is tested with a positive threshold only. A zero threshold returns 0.0 for all levels. A negative threshold produces NaN via `Math.sqrt` of a negative product. Neither case is documented or tested.

---

**A104-30 | Severity: MEDIUM | getCSSColor — return values are not validated against a specification; color strings are tested by equality only with hardcoded expectations**

The test `ReturnsCSSColorForImpactLevel` (line 29–33) correctly asserts all three enum cases. However, the amber value `"#FFBF00"` (line 37) is a hex colour code while BLUE and RED return CSS named colours (`"blue"`, `"red"`). There is no test that would detect if this inconsistency causes rendering issues (e.g., if a consumer expects a uniform format). This is an INFO-level observation about test intent rather than missing branch coverage, but it is noted here as a test quality gap.

---

**A104-31 | Severity: LOW | ImpactUtil has no test for getImpactLevelCoefficient indirectly through calculateGForceRequiredForImpact with an invalid ImpactLevel**

`getImpactLevelCoefficient` is `private` and is only reachable through `calculateGForceRequiredForImpact`. While all three valid enum values are tested via `ReturnsGForceRequiredForDifferentImpactLevels`, the exception path (default branch) is unreachable with the current enum but represents a future regression risk. See also A104-27.

---

**A104-32 | Severity: INFO | ImpactUtilTest uses JUnit 4 style (@Test from org.junit.Test) — no test runner or suite configuration found**

`ImpactUtilTest` imports `org.junit.Test` (JUnit 4). No `@RunWith` annotation, test suite, or Maven Surefire configuration was examined as part of this audit. This does not affect coverage but may affect CI/CD integration if the project is migrating to JUnit 5.

---

## Summary Table

| Finding ID | Severity | Class | Description |
|---|---|---|---|
| A104-1 | CRITICAL | DBUtil | Zero test coverage — no test class exists |
| A104-2 | CRITICAL | DBUtil | SQLException swallowed in 6+ methods; callers receive false empty results |
| A104-3 | CRITICAL | DBUtil | queryForObject(String, ResultMapper) opens connection outside try block — inconsistent cleanup pattern |
| A104-4 | HIGH | DBUtil | rollback in executeStatementWithRollback can throw and mask original exception |
| A104-5 | HIGH | DBUtil | Static databaseName field prevents test isolation; ensureDatabaseNameIsSet untestable without JVM args |
| A104-6 | HIGH | DBUtil | updateObject(Connection,...) returns -1 on SQLException instead of propagating |
| A104-7 | HIGH | DBUtil | updateObject(String,...) returns -1 on SQLException instead of propagating |
| A104-8 | MEDIUM | DBUtil | getConnection() no-arg overload delegation untested |
| A104-9 | MEDIUM | DBUtil | NamingException-to-SQLException wrapping and error message not tested |
| A104-10 | MEDIUM | DBUtil | queryForObjects(Connection,...) uses separate closeQuietly calls — inconsistent, rs leak on stmt close exception |
| A104-11 | MEDIUM | DBUtil | @Deprecated closeConnection has no documented replacement; untested |
| A104-12 | LOW | DBUtil | "Unique result expected" exception branch never exercised by any test |
| A104-13 | CRITICAL | HttpDownloadUtility | Zero test coverage — no test class exists |
| A104-14 | CRITICAL | HttpDownloadUtility | Hardcoded API authentication token in source code |
| A104-15 | CRITICAL | HttpDownloadUtility | sendPost silently discards caller-supplied fileName parameter |
| A104-16 | CRITICAL | HttpDownloadUtility | sendPost swallows OutputStream write exception — partial POST body undetectable |
| A104-17 | CRITICAL | HttpDownloadUtility | Streams not closed in finally — resource leak on any I/O exception |
| A104-18 | HIGH | HttpDownloadUtility | downloadFile non-200 path only logs; caller has no programmatic failure signal |
| A104-19 | HIGH | HttpDownloadUtility | sendPost non-200 path only logs; error stream is discarded |
| A104-20 | HIGH | HttpDownloadUtility | Static saveFilePath causes race condition in concurrent usage |
| A104-21 | HIGH | HttpDownloadUtility | Content-Disposition filename parsing uses magic offset without bounds validation |
| A104-22 | MEDIUM | HttpDownloadUtility | API URL uses plain HTTP despite HttpsURLConnection import; hardcoded external EC2 address |
| A104-23 | MEDIUM | HttpDownloadUtility | Catches Exception instead of IOException — masks programming errors |
| A104-24 | LOW | HttpDownloadUtility | getSaveFilePath and setSaveFilePath completely untested |
| A104-25 | HIGH | ImpactUtil | calculateImpactLevel returns null for below-threshold values — undocumented and untested |
| A104-26 | HIGH | ImpactUtil | Boundary values for calculateImpactLevel not tested — off-by-one errors undetectable |
| A104-27 | HIGH | ImpactUtil | UnhandledImpactLevelException default branch untested in both switch statements |
| A104-28 | MEDIUM | ImpactUtil | calculateGForceOfImpact tested with one value only; zero/negative/overflow not covered |
| A104-29 | MEDIUM | ImpactUtil | calculateGForceRequiredForImpact not tested with zero or negative threshold |
| A104-30 | MEDIUM | ImpactUtil | getCSSColor return values mix hex codes and CSS named colours — no format consistency test |
| A104-31 | LOW | ImpactUtil | getImpactLevelCoefficient exception path unreachable with current enum but untested for future safety |
| A104-32 | INFO | ImpactUtil | ImpactUtilTest uses JUnit 4 annotations — no suite/runner configuration verified |

---

*End of report. Agent A104. Audit run 2026-02-26-01.*
