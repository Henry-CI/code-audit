# Pass 4 -- Code Quality: Misc Small Packages
**Audit Agent:** A04
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production

---

## Reading Evidence

### File 1: `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java` (148 lines)
- Servlet class annotated `@WebServlet`, `@MultipartConfig`.
- Single `doPost` method handling report generation and email dispatch.
- Imports `com.torrent.surat.fms6.util.mail` (lowercase class name).
- Instance field `message` (line 37) and `dHolder` (line 38) are mutable state on a servlet (not thread-safe).
- `getExportDir()` uses code-source URL manipulation with hard-coded relative path `/../../../../../../../excelrpt/` (line 113).
- Lines 106, 109, 114: commented-out `System.out.println` / alternative directory paths.
- Line 132: commented-out email recipient.
- `linderReportMailer` uses `System.out.print` (line 127-134) for logging instead of Log4j.
- Line 97-101: `catch(Exception e) { e.printStackTrace(); }` -- broad catch with stack trace to stdout.
- Line 135-139: `catch(Exception e) { System.out.println(...) }` -- another broad catch suppressing detail.
- Line 99: typo in user-facing message: `"Something went wong!"`.
- Line 43: log statement concatenates multiple `getParameter()` calls; no null-safety on `getSession()`.
- JSON response is hand-built string concatenation (lines 55, 60, 66, 85, 87, 92, 99) -- no JSON library.

### File 2: `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java` (1485 lines)
- God class: 1485 lines, 11+ fetch methods, each with its own JDBC Connection/Statement/ResultSet lifecycle.
- Instance fields include `HttpServletRequest request` (line 25), `Connection conn`, five Statements (`stmt` through `stmt4`), five ResultSets (`rset` through `rset4`) -- all package-private.
- `init()` opens class-level connection (line 62), then dispatches to opCode-specific method. Each fetch method **opens a second connection** via `DBUtil.getConnection()` (e.g., line 194, 319, 446), resulting in two concurrent connections per call.
- Every fetch method repeats the identical boilerplate: `conn=DBUtil.getConnection(); stmt=conn.createStatement(...)` ~11 times.
- Raw type `ArrayList` without generics used at lines 46, 47, 203, 251, 324, 377, 461, 512, 707, 773, 781, 887, 916-918, 1023, 1123, 1155-1157, 1254, 1270-1272.
- All SQL is built via string concatenation with user-controlled parameters (`customerCd`, `locationCd`, `st_dt`, `end_dt`) -- SQL injection risk throughout.
- Every catch block follows the pattern `catch(Exception e) { System.out.println(query); e.printStackTrace(); e.getMessage(); }` where `e.getMessage()` return value is discarded (lines 290-295, 417-422, 553-558, 606-611, 673-678, 746-751, 843-847, 979-984, 1079-1084, 1208-1213, 1319-1324).
- `fetchUtilImpact()` (line 180-303): N+1 pattern -- loops over drivers, then for each driver loops over units, executing 3 queries per unit.
- `fetchUtilImpactByUnit()` (line 305-430): Same N+1 pattern over units.
- `fetchUtilImpactByType()` (line 432-566): Same N+1 pattern over models then units.
- `fetchPreOPFail()` (line 858-992): Triple-nested loop -- models > units > drivers -- each issuing individual queries.
- `fetchPreOPFailByDriver()` (line 1223-1332): N+1 lookup for each driver name by individual query (line 1305).
- `fetchPreopStats()` (line 761-856): N+1 -- for each unit, executes 2 queries.
- Unused import: `HttpServletRequest` (line 12) is declared as a field (line 25) but never assigned or used in any method.
- Unused field: `request` (line 25) never referenced.
- Unused field: `methodName` assigned in every method but never consumed anywhere.
- `modelList` field (line 47) is never populated; only a getter exists (line 1481).
- `convert_time1` and `convert_time` utility methods duplicated here; also exist in `DataUtil`.
- `fetchTrackXHydr()` sets `methodName = "fetchExpiredLicense()"` (line 622) -- copy-paste bug.
- `fetchUtilImpactByUnit()` sets `methodName = "fetchUtilImpact()"` (line 306) -- copy-paste bug.
- Data interchange uses delimited strings (`#,#` or `,`) instead of typed objects.
- No transactions; each method opens its own connection with auto-commit.

### File 3: `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java` (1053 lines)
- 1053 lines with 12 private report-creation methods that repeat nearly identical boilerplate.
- Every method instantiates a new `BusinessInsightBean`, sets 5 properties, calls `init()`, then reads data -- tight coupling to bean internals.
- Every method instantiates `new UnitDAO()` and calls `getCustbyId` / `getLocById` independently (lines 101-103, 182-184, 281-283, 361-363, 479-481, 625-628, 703-706, 769-771, 849-851, 911-913, 976-978).
- `createPreopFail()` (line 767) is defined but never called from `createExcel()` -- dead code.
- Unused import: `java.sql.SQLException` is declared on method signatures but the methods delegate SQL work to `BusinessInsightBean`.
- Line 151: potential `ArithmeticException` from `duration / impact` when `impact == 0` -- the guard at line 153 is checked after the division.
- Same division-before-guard pattern at lines 240, 330.
- `FileOutputStream` at line 92 is never closed in a finally block; if `wb.write()` throws, the stream leaks.
- Variable `currDriver` assigned at line 160 but never read -- dead code.
- Unused import `java.io.IOException` -- methods declare it but IOException is only thrown from POI write operations handled in `createExcel`.

### File 4: `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/PreOpQuestions.java` (75 lines)
- Clean POJO / JSON binding class.
- No major issues found.
- `toString()` is manually constructed (verbose); could use standard library or annotation-based approach, but this is a style preference.

### File 5: `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/Question.java` (133 lines)
- Clean POJO / JSON binding class.
- Javadoc on constructor (line 13-22) lists parameter names but provides no descriptions -- minimal value.
- `toString()` is manually constructed (verbose), same pattern as `PreOpQuestions`.
- No significant issues.

### File 6: `WEB-INF/src/com/torrent/surat/fms6/linde/bean/SupervisorUnlockBean.java` (54 lines)
- Small bean with package-private fields (line 5-9) instead of `private` -- violates encapsulation convention.
- Line 12: `// TODO Auto-generated constructor stub` -- dead comment from IDE boilerplate.
- `getGrandTotal()` (line 51) is a derived computed property -- acceptable pattern.
- Field `grandTotal` (line 9) is declared but never set or read externally; `getGrandTotal()` computes from other fields, making the field dead code.

### File 7: `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java` (76 lines)
- All SQL built via string concatenation (lines 30-31, 54-55, 61-62) -- SQL injection vulnerability.
- `doClose()` method at line 67-75 uses `System.out.println` for error logging.
- `updateLanguageBy()` (line 54): Missing space between `Update` and table name: `"Update\"FMS_CHCKLIST_LANG_SETTING\""` -- potential SQL syntax error if driver is strict.
- No transaction management; assumes caller manages commit/rollback.
- Statement is passed in via constructor (line 21) but never validated for null.

### File 8: `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java` (127 lines)
- All SQL built via string concatenation with user-supplied parameters (`custCd`, `locCd`, `searchCrit`, `vehTypeCd`) -- SQL injection vulnerability (lines 24-25, 37-38, 50-51, 66-69, 76, 79-89).
- Pattern field `pattern` (line 16) provides partial input validation for `searchCrit` but the match result is only used to decide which WHERE clause to add -- it does not prevent injection for `custCd`, `locCd`, or `vehTypeCd`.
- Line 91: `ResultSet rset` is never closed explicitly; relies on `stmt.close()` cascading close.
- Lines 112-113: `catch(Exception e) { e.printStackTrace(); }` -- broad catch, no proper logging.
- Lines 120-122: nested `catch(SQLException e) { e.printStackTrace(); }` in finally block.
- Line 101-102: `map.get(rset.getString(1))` called twice in succession instead of using a local variable.
- Unbounded query: no `LIMIT` clause on the UNION ALL query (line 79-89); could return unlimited rows.
- No transaction management.

---

## Findings

### A04-1 [Severity: HIGH] -- God Class: BusinessInsightBean (1485 lines)
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 1-1485
**Category:** Architecture

`BusinessInsightBean` is a 1485-line class containing 11 fetch methods, each with identical boilerplate for connection management, result set processing, and error handling. Every method opens its own database connection (in addition to the connection opened by `init()`), manages multiple Statement/ResultSet pairs as local variables that shadow the instance fields, and performs all SQL construction via string concatenation. This class should be decomposed into separate DAO/service classes per report type with a shared connection management strategy.

---

### A04-2 [Severity: HIGH] -- SQL Injection via String Concatenation (Systemic)
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 206-210, 228-240, 253-255, 327-333, 355-367, 379-381, 463-469, 490-502, 514-516, 587-597, 642-650, 709-714, 729-735, 783-788, 804-807, 821-829, 889-895, 922-932, 954, 1026-1032, 1044-1054, 1127-1133, 1161-1171, 1256-1261, 1275-1285, 1305
**Category:** Error Handling / Security

All queries in `BusinessInsightBean` are built by concatenating user-supplied parameters (`customerCd`, `locationCd`, `st_dt`, `end_dt`) directly into SQL strings. No PreparedStatement or parameter binding is used. This pattern is also present in:
- `FmsChklistLangSettingRepo.java` (lines 30-31, 54-55, 61-62)
- `HireDehireService.java` (lines 24-25, 37-38, 50-51, 66-69, 76, 79-89)

---

### A04-3 [Severity: HIGH] -- N+1 Query Pattern in Multiple Fetch Methods
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 200-286 (`fetchUtilImpact`), 348-412 (`fetchUtilImpactByUnit`), 456-549 (`fetchUtilImpactByType`), 725-742 (`fetchLockoutStat`), 799-841 (`fetchPreopStats`), 882-977 (`fetchPreOPFail`), 1149-1202 (`fetchPreOPFailByUnit`), 1249-1317 (`fetchPreOPFailByDriver`)
**Category:** Performance

Nearly every fetch method in `BusinessInsightBean` follows an N+1 query pattern: an outer query fetches a list (drivers, units, or vehicle types), and then for each row, 1-3 additional queries are executed in a loop. `fetchPreOPFail` has a triple-nested loop (models > units > drivers), each level executing its own query. For large fleets this produces hundreds or thousands of individual SQL round trips.

---

### A04-4 [Severity: MEDIUM] -- Broad catch(Exception) with e.printStackTrace() Throughout
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java` (line 97-101)
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java` (lines 93-96, 290-295, 417-422, 553-558, 606-611, 673-678, 746-751, 843-847, 979-984, 1079-1084, 1208-1213, 1319-1324)
**File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java` (lines 112-113, 120-122)
**Category:** Error Handling

Every catch block in the audited files catches the broadest `Exception` type and calls `e.printStackTrace()`, which writes to stderr/stdout rather than the application log. In `BusinessInsightBean`, every catch block also calls `e.getMessage()` as a standalone statement whose return value is discarded (e.g., line 294). The servlet class (`BusinessInsight.java`) has a Log4j logger declared (line 35) but uses `e.printStackTrace()` and `System.out.print` instead of it.

---

### A04-5 [Severity: MEDIUM] -- Servlet Instance Fields Not Thread-Safe
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Lines:** 37-38
**Category:** Architecture

`BusinessInsight` is a servlet (single instance, shared across threads). The instance fields `message` (String, line 37) and `dHolder` (int, line 38) are written to in `doPost()` on every request. Under concurrent access, one thread's response could contain another thread's message string, causing incorrect data to be returned to users.

---

### A04-6 [Severity: MEDIUM] -- Duplicate Connection Opening in init() + fetch Methods
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 55-64 (init connection), 193-196 (fetchUtilImpact connection), 318-321, 445-448, 581-584, 634-637, 701-704, 776-779, 871-874, 1007-1010, 1107-1110, 1236-1239
**Category:** Performance / Architecture

`init()` opens a connection and creates statements at the class level (lines 62-65), then dispatches to a fetch method that opens a **second** connection via `DBUtil.getConnection()`. This means every report generation consumes two database connections simultaneously. The instance-level connection opened in `init()` is closed in the finally block but was never used by the fetch methods, which shadow the instance fields with local variables of the same name.

---

### A04-7 [Severity: MEDIUM] -- Dead Code: Unused Fields and Methods
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
- `request` field (line 25): declared but never assigned or read.
- `methodName` field (line 38): assigned in every fetch method but never consumed.
- `modelList` field (line 47): never populated; getter at line 1481 always returns empty list.
- `stmt2`, `stmt3`, `stmt4` fields (lines 29-31): declared but never used in `init()` or any method using instance-level fields.
- `rset2`, `rset3`, `rset4` fields (lines 34-36): same as above.
- `dHolder` field in `BusinessInsight.java` (line 38): never read.

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
- `createPreopFail()` method (line 767-845): defined but never called from `createExcel()`.
- `currDriver` variable (line 143/160): assigned but never read.

**File:** `WEB-INF/src/com/torrent/surat/fms6/linde/bean/SupervisorUnlockBean.java`
- `grandTotal` field (line 9): declared but never set or read; `getGrandTotal()` computes the value from other fields.

---

### A04-8 [Severity: MEDIUM] -- Commented-Out Code
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
- Line 106: `// System.out.println();`
- Line 109: `// String dir = this.getClass().getClassLoader().getResource(".").getPath();`
- Line 114: `// dir += "/../../excelrpt/";`
- Line 132: `// + "julius@collectiveintelligence.com.au"`
- Line 122: `// comment out for debug only`

**Category:** Dead Code

These commented-out lines include debug statements, alternative implementations, and a hard-coded developer email address. They add noise and should be removed or converted to configuration.

---

### A04-9 [Severity: MEDIUM] -- FileOutputStream Resource Leak in BusinessInsightExcel.createExcel()
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
**Lines:** 92-94
**Category:** Error Handling

```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
```

The `FileOutputStream` is not wrapped in a try-with-resources or try/finally block. If `wb.write(fileOut)` throws an exception, the stream will never be closed, leaking a file descriptor.

---

### A04-10 [Severity: MEDIUM] -- Division-Before-Guard Bug in BusinessInsightExcel
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
**Lines:** 151-155, 240-244, 330-332
**Category:** Error Handling

```java
double impXHour = duration / impact;  // line 151 -- ArithmeticException if impact==0
if (impact == 0 || duration == 0) {   // line 153 -- guard AFTER the division
    impXHour = 0;
}
```

The division `duration / impact` is performed unconditionally. The zero-check guard at line 153 executes after the division has already occurred. When `impact` is 0, this results in either `Infinity` or `NaN` for doubles, which may not throw but will produce incorrect spreadsheet values. The same pattern repeats at lines 240 and 330.

---

### A04-11 [Severity: MEDIUM] -- Massive Code Duplication in BusinessInsightExcel
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
**Lines:** 99-178, 180-276, 278-356, 358-474, 476-620, 623-688, 690-765, 767-845, 847-908, 910-971, 974-1035
**Category:** Architecture

The file contains 11 private `create*` methods that share approximately 80% identical code: instantiating `UnitDAO`, fetching customer/location, creating subtitles, instantiating `BusinessInsightBean` with the same 5 setters, creating header rows, and iterating over a bean list. Only the column headers and data parsing differ. This should be refactored to a template method or strategy pattern.

---

### A04-12 [Severity: MEDIUM] -- Copy-Paste Bugs in methodName Assignment
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 306, 433, 622, 762, 859, 995, 1095, 1224
**Category:** Style / Dead Code

Several fetch methods assign incorrect values to `methodName`:
- `fetchUtilImpactByUnit()` (line 306): sets `methodName = "fetchUtilImpact()"` (wrong method name).
- `fetchTrackXHydr()` (line 622): sets `methodName = "fetchExpiredLicense()"` (wrong method name).
- `fetchPreOPFailByType()` (line 995): sets `methodName = "fetchPreOPFail()"` (wrong method name).
- `fetchPreOPFailByUnit()` (line 1095): sets `methodName = "fetchPreOPFail()"` (wrong method name).
- `fetchPreOPFailByDriver()` (line 1224): sets `methodName = "fetchPreOPFail()"` (wrong method name).

Since `methodName` is never consumed, this is both dead code and a copy-paste indicator.

---

### A04-13 [Severity: MEDIUM] -- Raw Types / Missing Generics
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 46-47, 203, 251, 324, 377, 461, 512, 707, 773, 781, 887, 916-918, 1023, 1123, 1155-1157, 1254, 1270-1272
**Category:** Style

`ArrayList` is used without type parameters throughout the file. Examples:
- Line 46: `ArrayList<String> dataArray = new ArrayList();` -- missing diamond operator.
- Lines 916-917: `ArrayList res_id = new ArrayList(); ArrayList tmp_did = new ArrayList();` -- completely raw types.
- Line 1270-1272: `ArrayList res_id = new ArrayList(); ArrayList tmp_did = new ArrayList(); ArrayList tmpHireNo = new ArrayList();`

This suppresses compile-time type checking and produces unchecked warnings.

---

### A04-14 [Severity: MEDIUM] -- Unbounded Query Without LIMIT
**File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java`
**Lines:** 79-89
**Category:** Performance

The `UNION ALL` query in `getUnitsHireDehireTime()` has `ORDER BY` but no `LIMIT` clause. For customers with large vehicle histories, this query could return an unbounded number of rows, all loaded into an in-memory `LinkedHashMap`. There is no pagination or result-size guard.

---

### A04-15 [Severity: LOW] -- Package-Private Fields Instead of Private
**File:** `WEB-INF/src/com/torrent/surat/fms6/linde/bean/SupervisorUnlockBean.java`
**Lines:** 5-9
**Category:** Style

Fields `supervisorName`, `impactCount`, `surveyCount`, `criticalCount`, and `grandTotal` are declared with default (package-private) access instead of `private`. Since getters/setters exist, the fields should be `private` to enforce encapsulation.

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 25-48
All instance fields (`request`, `conn`, `stmt`-`stmt4`, `rset`-`rset4`, `query`, `methodName`, `opCode`, `customerCd`, `locationCd`, `st_dt`, `end_dt`, `dataArray`, `modelList`, `df`) are package-private.

---

### A04-16 [Severity: LOW] -- System.out.println Used Instead of Logger
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java` (lines 127-134, 137-138)
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java` (lines 95-96, 103, 109, 115, 121, 127, 133, 139, 145, 151, 157, 163, 167, 175, 292, 419, 555, 608, 675, 748, 981, 1081, 1210, 1321)
**File:** `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java` (line 72)
**File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java` (lines 113, 121)
**Category:** Style

`System.out.println` and `System.out.print` are used for logging throughout instead of the application's Log4j framework. `BusinessInsight.java` declares a Log4j logger (line 35) but only uses it once in the opening info log (line 43); all other output goes to stdout/stderr.

---

### A04-17 [Severity: LOW] -- Hand-Built JSON Responses
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Lines:** 55-56, 60-61, 66-67, 85, 87, 92-93, 99
**Category:** Style

JSON responses are built via string concatenation (e.g., `"{ \"status\":\"error\", \"message\": \"...\" }"`). This is fragile -- if message values contain quotes or special characters, the JSON will be malformed. A JSON serialization library should be used.

---

### A04-18 [Severity: LOW] -- Typo in User-Facing Error Message
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Line:** 99
**Category:** Style

```java
message = "{ \"status\":\"error\", \"message\": \"Sorry, Something went wong!\" }";
```

The word "wong" should be "wrong".

---

### A04-19 [Severity: LOW] -- IDE-Generated TODO Comments
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java` (line 32)
**File:** `WEB-INF/src/com/torrent/surat/fms6/linde/bean/SupervisorUnlockBean.java` (line 12)
**Category:** Dead Code

```java
// TODO Auto-generated constructor stub
```

These are default IDE-generated comments left in empty constructors. They provide no value and should be removed.

---

### A04-20 [Severity: LOW] -- Naming Convention Violation: Lowercase Class Name
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Line:** 18
**Category:** Style

```java
import com.torrent.surat.fms6.util.mail;
```

The class `mail` uses a lowercase name, violating Java naming conventions where class names should be PascalCase (e.g., `Mail`).

---

### A04-21 [Severity: LOW] -- Potential SQL Syntax Error in FmsChklistLangSettingRepo.updateLanguageBy()
**File:** `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java`
**Line:** 54
**Category:** Style

```java
String query = "Update\"FMS_CHCKLIST_LANG_SETTING\" set ...
```

There is no space between the `Update` keyword and the table name. While some database drivers may tolerate this, it is a formatting error that could fail on strict SQL parsers.

---

### A04-22 [Severity: LOW] -- Data Interchange via Delimited Strings Instead of Typed Objects
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java` (lines 285, 410, 549, 601, 666, 738, 835, 960, 1069, 1189, 1311)
**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java` (lines 147, 236, 326, 412, 538, 666, 737, 816, 889, 953, 1016)
**Category:** Architecture

`BusinessInsightBean` methods pack results into `ArrayList<String>` using delimited strings (e.g., `"Driver:John Smith#,#5#,#2.50"` or `"name:ABC,10,3.5,50,Forklift"`). `BusinessInsightExcel` then parses these back via `split("#,#")` or `split(",")`. This fragile data interchange using inconsistent delimiters (`#,#` vs `,`) throughout different methods is error-prone and should use typed DTOs.

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | 3     |
| MEDIUM   | 11    |
| LOW      | 8     |
| **Total**| **22**|

The most critical issues are concentrated in `BusinessInsightBean.java`, which is a 1485-line God class with pervasive SQL injection vulnerabilities, N+1 query patterns, duplicate connection management, and broad exception swallowing. `BusinessInsightExcel.java` compounds the problem with massive code duplication. `FmsChklistLangSettingRepo.java` and `HireDehireService.java` share the SQL injection pattern. The JSON binding POJOs (`PreOpQuestions.java`, `Question.java`) and the small bean (`SupervisorUnlockBean.java`) are relatively clean with only minor style issues.
