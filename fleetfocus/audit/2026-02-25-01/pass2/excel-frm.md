# Pass 2 -- Test Coverage: excel package (Frm_ servlets)
**Agent:** A09
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Item | Status |
|------|--------|
| Test framework (JUnit/TestNG) | **Not present** -- zero test dependencies found |
| Test source directories (`test/`, `src/test/`) | **Not present** |
| Test runner configuration (Maven Surefire, Gradle test, etc.) | **Not present** |
| CI/CD test stage | **Not observable** in repository |
| Code coverage tooling (JaCoCo, Cobertura) | **Not present** |
| Mock libraries (Mockito, EasyMock) | **Not present** |

**Conclusion:** The repository has **zero automated tests**. All 10 files in scope have **0% test coverage**. There is no test infrastructure of any kind in the repository.

---

## Reading Evidence

### 1. Frm_excel.java (Base Class)

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java`
- **Lines:** 1163
- **Class:** `public class Frm_excel` (no extends HttpServlet -- this is a POJO base class, NOT a servlet)
- **Servlet Annotations/Mappings:** None. Not registered in web.xml. No `@WebServlet` annotation.
- **Nature:** Base class for Excel report generation using Apache POI (XSSFWorkbook). All other Frm_ classes extend this.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_excel(String docRoot, String fileName) throws Exception` | 70 |
| public | `Frm_excel(String cust_cd, String loc_cd, String docRoot)` | 77 |
| public | `Frm_excel() throws Exception` | 85 |
| public | `Frm_excel(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 91 |
| public | `Frm_excel(String cust_cd, String loc_cd, ArrayList<String> deptCdArrayList, String from, String to, String docRoot)` | 102 |
| public | `Frm_excel(String cust_cd, String loc_cd, String dept_cd, String from, String to, String params[], String docRoot) throws Exception` | 113 |
| public | `Frm_excel(String cust_cd, String loc_cd, String dept_cd, String from, String to, String params[], String docRoot, String formName) throws Exception` | 125 |
| public | `Frm_excel(String[] params, String docRoot) throws Exception` | 138 |
| public | `Frm_excel(String docRoot)` | 143 |
| public | `void setParameters(boolean isConf) throws Exception` | 151 |
| public | `String getParam(String key)` | 174 |
| public | `String createExcel() throws IOException, SQLException` | 198 |
| public | `void init() throws SQLException` | 209 |
| public | `void init2() throws SQLException` | 213 |
| public | `String createEmail() throws IOException, SQLException` | 217 |
| public | `String createBody() throws IOException, SQLException` | 228 |
| public | `String getBody()` | 239 |
| public | `void setTotalDuration(String totalDuration, Cell contentCell, String style)` | 925 |
| public | `void getCust_prefix(String cust_cd)` | 1096 |
| public | `String getResult()` | 1100 |
| public | `void setResult(String result)` | 1104 |
| public | `String getTitle()` | 1108 |
| public | `void setTitle(String title)` | 1112 |
| public | `String getLoc_cd()` | 1116 |
| public | `void setLoc_cd(String loc_cd)` | 1120 |
| public | `String getCust_cd()` | 1123 |
| public | `void setCust_cd(String cust_cd)` | 1126 |
| public | `String getImageroot()` | 1130 |
| public | `void setImageroot(String imageroot)` | 1134 |
| public | `String getDocroot()` | 1138 |
| public | `void setDocroot(String docroot)` | 1142 |
| public | `String getDept_cd()` | 1146 |
| public | `void setDept_cd(String dept_cd)` | 1150 |
| public | `String getFileName()` | 1154 |
| public | `void setFileName(String fileName)` | 1158 |

**Key protected methods:** `createReptTitle`, `createReptSubTitle`, `addEmptyLine`, `addImage` (4 overloads), `addImageLogo`, `addImage2`, `addImageFromUrl`, `addResizedImage`, `addImageUtilisationChart`, `addDashboardChart`, `setPrint`, `setPrintA3`, `setColumnWidth`, `setColumnWidthWide`, `setColumnWidthNarrow`, `setColumnWidthOnePage`, `setColumnWidthWideDashboard`, `setColumnWidthTitle`, `setColumnWidthCustom`, `setFoot`, `createReport`, `getExportDir`, `createReptSubTitleNoLine` (2 overloads).

---

### 2. Frm_Linde_Reports.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_Linde_Reports.java`
- **Lines:** 2381
- **Class:** `public class Frm_Linde_Reports extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_Linde_Reports(String cust_cd, String loc_cd, String docRoot, String chart, String chart2, String st_dt, String end_dt)` | 41 |
| public | `String createExcel(String opCode) throws Exception` | 50 |
| public | `void setImageDir(String imageDir)` | 346 |
| public | `void generateChart(String rpt_name) throws Exception` | 2335 |
| public | `void setParams(String params)` | 2373 |
| public | `void setDataArray(String[] dataArray)` | 2377 |

**Private methods (16):** `createUtilisationChart` (L292), `createImpactChart` (L319), `createPreOpChart` (L350), `createUtilDriverLogonChart` (L379), `createNationalPreOpCheck` (L437), `createSupervisorUnlockReport` (L464), `createDriverLockoutReport` (L571), `createImpactReport` (L680), `createPreopChecksCompleted` (L1061), `createPreopChecksCompletionTime` (L1212), `createNat2PreopChecksbyModel` (L1420), `createNat2PreopChecksbyDriver` (L1555), `createUnitUnlockreport` (L1737), `createImpactByUnitUtil` (L1810), `createImpactByDriverUtil` (L2006).

---

### 3. Frm_MaxHourUsage.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_MaxHourUsage.java`
- **Lines:** 196
- **Class:** `public class Frm_MaxHourUsage extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_MaxHourUsage(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 20 |
| public | `Frm_MaxHourUsage(String cust_cd, String loc_cd, ArrayList deptCdArrayList, String from, String to, String docRoot)` | 26 |
| public | `String createExcel() throws IOException, SQLException` | 32 |

**Private methods:** `createUtilisationChart` (L46), `createGroupUtilisationChart` (L114).

---

### 4. Frm_inaUnit_rpt.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_inaUnit_rpt.java`
- **Lines:** 227
- **Class:** `public class Frm_inaUnit_rpt extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_inaUnit_rpt() throws Exception` | 21 |
| public | `Frm_inaUnit_rpt(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 26 |
| public | `String createExcel() throws IOException, SQLException` | 33 |
| public | `ArrayList<Integer> getDays()` | 215 |
| public | `void setDays(ArrayList<Integer> days)` | 219 |
| public | `void addDays(int days)` | 223 |

**Private methods:** `createInactiveUnitReport` (L53).

---

### 5. Frm_month_rpt.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_month_rpt.java`
- **Lines:** 765
- **Class:** `public class Frm_month_rpt extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_month_rpt(String cust_cd, String loc_cd, String docRoot)` | 29 |
| public | `String createExcel() throws IOException, SQLException` | 34 |

**Private methods:** `createCoverpage` (L65), `createImpactReport` (L139), `createImpactByDriverReport` (L313), `createUtilisationChart` (L499), `createUtilisationReport` (L551).

---

### 6. Frm_national_rpt.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_national_rpt.java`
- **Lines:** 1209
- **Class:** `public class Frm_national_rpt extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_national_rpt(String cust_cd, String loc_cd, String docRoot)` | 32 |
| public | `String createExcel() throws IOException, SQLException` | 38 |

**Private methods (7):** `createPreopByModelRpt` (L95), `createPreopByDriverRpt` (L204), `createImpactReport` (L327), `createUnitUnlockreport` (L549), `createUtilisationChart` (L621), `createImpactByUnitUtilreport` (L678), `createImpactByDriverUtilreport` (L884).

---

### 7. Frm_nz_unitSummary_rpt.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_nz_unitSummary_rpt.java`
- **Lines:** 112
- **Class:** `public class Frm_nz_unitSummary_rpt extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_nz_unitSummary_rpt() throws Exception` | 20 |
| public | `String createExcel() throws IOException, SQLException` | 25 |

**Private methods:** `createUnitSummaryReportNZ` (L57). Also overrides `setColumnWidth` (L48).

---

### 8. Frm_quater_rpt.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_quater_rpt.java`
- **Lines:** 875
- **Class:** `public class Frm_quater_rpt extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_quater_rpt(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 32 |
| public | `Frm_quater_rpt(String cust_cd, String loc_cd, ArrayList deptCdArrayList, String from, String to, String docRoot)` | 39 |
| public | `String createExcel() throws IOException, SQLException` | 46 |
| public | `String getExportDir() throws Exception` | 797 |

**Private methods (5):** `createPreopRpt` (L93), `createPreopByDriverRpt` (L178), `createImpactReport` (L313), `createImpactByDriverReport` (L428), `createUtilisationChart` (L807), `createUtilisationChartByGroup` (L672).

---

### 9. Frm_simSwap_rpt.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_simSwap_rpt.java`
- **Lines:** 157
- **Class:** `public class Frm_simSwap_rpt extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_simSwap_rpt() throws Exception` | 19 |
| public | `String createExcel() throws IOException, SQLException` | 24 |

**Private methods:** `createUnitSummaryReport` (L58). Also overrides `setColumnWidth` (L39).

---

### 10. Frm_unitSummary_rpt.java

- **File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_unitSummary_rpt.java`
- **Lines:** 257
- **Class:** `public class Frm_unitSummary_rpt extends Frm_excel`
- **Servlet Annotations/Mappings:** None.

| Visibility | Method Signature | Line |
|-----------|-----------------|------|
| public | `Frm_unitSummary_rpt() throws Exception` | 20 |
| public | `String createExcel() throws IOException, SQLException` | 25 |

**Private methods:** `createUnitSummaryReport` (L54). Also overrides `setColumnWidth` (L40).

---

## Architectural Note

Despite the task title referencing "Frm_ servlet classes," **none of these classes are servlets**. They are POJO report-generator classes that extend `Frm_excel`, which itself does not extend `HttpServlet` and has no servlet annotations. These classes are invoked programmatically from other parts of the application (likely from actual servlet or controller code) to generate `.xlsx` Excel files using Apache POI. They interact directly with DAO classes (`UnitDAO`, `ImpactDAO`, `LockOutDAO`, `PreCheckDAO`) and write output to the filesystem via `FileOutputStream`.

---

## Findings

### A09-001 -- Zero test coverage across all 10 files (7,342 total LOC)
**Severity:** CRITICAL
**Files:** All 10 files in scope
**Details:** None of the 10 files have any automated tests. There are no unit tests, integration tests, or any other form of automated verification. The combined codebase is 7,342 lines of code with approximately 55+ distinct methods containing significant business logic (report generation, data aggregation, formatting calculations). The complete absence of tests means:
- No regression safety net for any changes
- No verification that report output matches expected format or data
- No validation that DAO interactions produce correct results
- No confidence that edge cases (empty data sets, null values, boundary dates) are handled correctly

**Functions most urgently needing tests:**
1. `Frm_excel.getParam(String key)` (L174) -- parameter parsing logic, susceptible to index-out-of-bounds
2. `Frm_excel.setParameters(boolean isConf)` (L151) -- complex initialization with multiple DAO calls
3. `Frm_excel.setTotalDuration(String, Cell, String)` (L925) -- parsing/formatting logic with hour threshold
4. `Frm_excel.getExportDir(String)` (L903) -- path construction with site-specific branching (AU vs. other)
5. `Frm_Linde_Reports.createExcel(String opCode)` (L50) -- 16-branch dispatcher, core routing logic
6. `Frm_quater_rpt.createExcel()` (L46) -- multi-sheet report with conditional group/non-group logic

---

### A09-002 -- FileOutputStream resource leaks on exception in all createExcel() methods
**Severity:** HIGH
**Files:** All 10 files
**Details:** Every `createExcel()` method across all files follows the same pattern:
```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
return result;
```
This does NOT use try-with-resources or try/finally. If `wb.write(fileOut)` throws an exception, `fileOut.close()` is never called, leaking a file handle. This occurs in:
- `Frm_excel.java` lines 203-206, 222-225, 233-236
- `Frm_Linde_Reports.java` lines 284-288
- `Frm_MaxHourUsage.java` lines 40-43
- `Frm_inaUnit_rpt.java` lines 45-48
- `Frm_month_rpt.java` lines 59-62
- `Frm_national_rpt.java` lines 89-92
- `Frm_nz_unitSummary_rpt.java` lines 41-43
- `Frm_quater_rpt.java` lines 87-90
- `Frm_simSwap_rpt.java` lines 32-35
- `Frm_unitSummary_rpt.java` lines 33-36

**Tests needed:** Unit tests confirming output stream is properly closed even when `wb.write()` throws; tests verifying behavior when file path is invalid.

---

### A09-003 -- InputStream resource leaks in Frm_excel image-handling methods
**Severity:** HIGH
**File:** `Frm_excel.java`
**Details:** Multiple `addImage*` methods open `FileInputStream` or `URL.openStream()` without try-with-resources. If `IOUtils.toByteArray(is)` or `wb.addPicture()` throws, the stream is never closed. Affected methods:
- `addImage(Sheet, String, int)` -- L406-409
- `addImage(Sheet, String, int, boolean, int)` -- L439-444
- `addImageLogo(Sheet, String, int, boolean, int, double)` -- L474-479
- `addImage2(Sheet, String, int, boolean, int)` -- L511-516
- `addImageFromUrl(Sheet, String, int, boolean, int)` -- L548-569 (also leaks `ostream` on some paths)
- `addResizedImage(Sheet, String, int, boolean)` -- L599-603
- `addImageUtilisationChart(Sheet, String, int, boolean, int)` -- L948-953
- `addDashboardChart(Sheet, String, int, boolean, int)` -- L986-991

**Tests needed:** Tests with mock streams verifying proper cleanup; tests with non-existent or corrupt image files.

---

### A09-004 -- Swallowed exceptions with only e.printStackTrace() in catch blocks
**Severity:** HIGH
**Files:** `Frm_MaxHourUsage.java` (L84-87, L162-165), `Frm_quater_rpt.java` (L789-791), `Frm_excel.java` (L559-561)
**Details:** Multiple catch blocks catch `Exception` broadly and only call `e.printStackTrace()`:
```java
} catch (Exception e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
}
```
This silently swallows errors during image processing and chart generation. The report will be generated missing images/charts with no indication to the user or calling code that content was lost. The "TODO Auto-generated" comments in `Frm_MaxHourUsage` confirm these were never properly implemented.

**Tests needed:** Tests that inject failing image operations and verify that errors are either propagated or properly logged; tests verifying report completeness when image operations fail.

---

### A09-005 -- No input validation on constructor parameters and method arguments
**Severity:** HIGH
**Files:** All 10 files
**Details:** No file validates its constructor inputs. Parameters like `cust_cd`, `loc_cd`, `dept_cd`, `from`, `to`, `docRoot`, `opCode`, `chart`, `chart2`, `st_dt`, `end_dt` are accepted without any null checks, empty-string checks, format validation, or length limits. These values are passed directly to:
- DAO queries (potential SQL injection if DAOs don't use prepared statements)
- File path construction (potential path traversal via `docRoot`)
- `Integer.parseInt()` calls (will throw uncaught `NumberFormatException`)
- `String.split()` operations (will cause `ArrayIndexOutOfBoundsException` on malformed data)

Specific examples:
- `Frm_Linde_Reports.createExcel(String opCode)` L50: if opCode is null, `opCode.equals(...)` throws NPE
- `Frm_excel.getParam(String key)` L174-188: if `params` array is null, NPE at `params.length`
- `Frm_Linde_Reports` L296-298: `st_dt.split("/")` then `Integer.parseInt(datepart[1])` -- crashes on any non-dd/mm/yyyy format

**Tests needed:** Null parameter tests for all constructors; boundary/format tests for date strings; empty-collection tests for DAO return values.

---

### A09-006 -- Unsafe date string parsing with no format validation
**Severity:** HIGH
**Files:** `Frm_Linde_Reports.java` (lines 296-299, 323-326, 354-357)
**Details:** Date strings are parsed by naive `split("/")`:
```java
String[] datepart = st_dt.split("/");
String month = datepart[1];
String year = datepart[2];
String monRange = DataUtil.getMonthForInt(Integer.parseInt(month)-1)
    + " - " + DataUtil.getMonthForInt(Integer.parseInt(month)+4);
```
If `st_dt` is empty, null, or in an unexpected format (e.g., ISO `yyyy-MM-dd`), this will throw `ArrayIndexOutOfBoundsException` or `NumberFormatException`. The pattern is used in `createUtilisationChart`, `createImpactChart`, and `createPreOpChart`.

**Tests needed:** Tests with various date formats, empty strings, nulls, malformed strings like "abc", "2025-01-15", "//".

---

### A09-007 -- Potential ArrayIndexOutOfBoundsException in comma-delimited data parsing
**Severity:** HIGH
**File:** `Frm_Linde_Reports.java` (lines 1127-1132, 1278-1284, 1502-1505, 1633-1638)
**Details:** Multiple methods parse comma-delimited strings from `bean.getPreopDataArray()`:
```java
String[] data = beanList.get(i).split(",");
String model = data[0].split(":")[1];
String name = data[1];
int yesRpt = Integer.parseInt(data[2]);
int yes = Integer.parseInt(data[3]);
int no = Integer.parseInt(data[4]);
```
No length check on the `data` array before indexing. If the upstream data format changes, has missing fields, or contains fewer commas than expected, this will throw `ArrayIndexOutOfBoundsException`. The pattern is repeated in:
- `createPreopChecksCompleted` (L1127-1132)
- `createPreopChecksCompletionTime` (L1278-1284)
- `createNat2PreopChecksbyModel` (L1502-1505)
- `createNat2PreopChecksbyDriver` (L1633-1638)

**Tests needed:** Tests with malformed data arrays, missing fields, empty strings, data with colons but no commas, etc.

---

### A09-008 -- Division by zero risk in Frm_Linde_Reports
**Severity:** MEDIUM
**File:** `Frm_Linde_Reports.java`
**Details:** Two locations risk division by zero:
1. Line 1372: `avT = aveTot/countTot;` -- if `countTot` is 0 (no records after filtering), integer division by zero throws `ArithmeticException`. The guard `if(aveTot > 0)` does not protect against countTot being 0 independently.
2. Line 1923: `double impXHour = duration / gTotal;` -- if `gTotal` is 0 (both red and amber are 0), division by zero. While the data comes from a DAO, there is no guard.
3. Line 411: `DataUtil.convert_time_hhmm((int)(Double.parseDouble(totalHours+"")/Double.parseDouble(workDay+"")*60*60*10))` -- if `workDay` is 0, division by zero.

**Tests needed:** Tests with zero totals, zero counts, and zero work days to verify proper handling.

---

### A09-009 -- Hardcoded file system path construction with platform-specific separators
**Severity:** MEDIUM
**Files:** `Frm_excel.java` (L903-923), `Frm_nz_unitSummary_rpt.java` (L33-38), `Frm_quater_rpt.java` (L797-805)
**Details:** `getExportDir()` constructs paths using `getProtectionDomain().getCodeSource().getLocation()` and manipulates forward slashes. The path traversal differs by site:
```java
if(LindeConfig.siteName.equals("AU")) {
    dir += "/../../" + dirctory + "/";
} else {
    dir += "/../../../../../../../../" + dirctory + "/";
}
```
`Frm_nz_unitSummary_rpt.java` hardcodes its own path (`dir += "/../../" + RuntimeConf.docDir + "/"`), duplicating and diverging from the base class logic. `Frm_quater_rpt.java` has yet another variant (`dir += "/../../../../../../../"`). These are fragile, untestable, and non-portable.

**Tests needed:** Tests verifying correct path construction for both AU and non-AU configurations; tests with `getCodeSource()` returning different base paths.

---

### A09-010 -- Workbook (XSSFWorkbook) is never closed
**Severity:** MEDIUM
**Files:** All 10 files
**Details:** `Frm_excel` creates `protected Workbook wb = new XSSFWorkbook()` at field initialization (L63) but never closes it. `XSSFWorkbook` implements `Closeable` and holds significant memory (XML DOM in-memory). After `wb.write(fileOut)`, the workbook is never released. In a server environment generating many reports, this can lead to memory exhaustion. No `close()` call exists in any of the 10 files.

**Tests needed:** Tests confirming workbook is properly closed after use; memory profiling tests for large report generation.

---

### A09-011 -- Large method complexity in Frm_Linde_Reports.createExcel()
**Severity:** MEDIUM
**File:** `Frm_Linde_Reports.java` (lines 50-288)
**Details:** The `createExcel(String opCode)` method is a 238-line method with 18 if/else-if branches dispatching on opCode string values. Two special branches (`Linde_national_report_1` at L161, `Linde_national_report_2` at L226) aggregate multiple sub-reports by mutating `this.op_code` and calling multiple creation methods sequentially. This is extremely difficult to test because:
- The method mixes orchestration with side-effect-heavy operations
- It mutates instance state (`this.op_code`, `currentRow`) between method calls
- An unrecognized opCode silently produces an empty report with no error
- No default/else clause or error for unknown opCode values

**Tests needed:** Tests for each of the 18 opCode values; test for unknown/null opCode; tests verifying that national report consolidation calls are made in correct order.

---

### A09-012 -- DAO objects instantiated inline with no dependency injection
**Severity:** MEDIUM
**Files:** All 10 files
**Details:** Every file creates DAO instances inline with `new UnitDAO()`, `new ImpactDAO()`, `new PreCheckDAO()`, `new LockOutDAO()`. This makes testing impossible without a live database connection. There is no constructor injection, setter injection, or factory pattern that would allow substituting mock DAOs. Additionally, `Frm_excel` initializes `CustomerDAO dao = new CustomerDAO()` as a field-level member (L149), which means a DAO is created even if never used.

**Tests needed (if testable):** All DAO interactions would need mocking, requiring refactoring to inject DAO dependencies.

---

### A09-013 -- Raw ArrayList usage without generics (type safety)
**Severity:** LOW
**Files:** `Frm_MaxHourUsage.java` (L26), `Frm_quater_rpt.java` (L40), `Frm_excel.java` (L60)
**Details:** Several constructors accept or use raw `ArrayList` without generic type parameters:
- `Frm_MaxHourUsage(String cust_cd, String loc_cd, ArrayList deptCdArrayList, ...)` (L26)
- `Frm_quater_rpt(String cust_cd, String loc_cd, ArrayList deptCdArrayList, ...)` (L40)
- `Frm_excel` field: `protected ArrayList deptCdArrayList = new ArrayList()` (L60)
- `Frm_MaxHourUsage.createGroupUtilisationChart`: `ArrayList<String> tabList = new ArrayList()` (L135)

This bypasses Java's type safety and could lead to `ClassCastException` at runtime if incorrect types are added.

**Tests needed:** Type-safety tests ensuring only expected types are stored in collections.

---

### A09-014 -- Unreachable code and dead methods in Frm_excel
**Severity:** LOW
**File:** `Frm_excel.java`
**Details:**
- `getCust_prefix(String cust_cd)` (L1096-1098) has an empty body -- it is never implemented
- `init()` (L209-211) and `init2()` (L213-215) have empty bodies -- subclasses do not override them in the files in scope
- `createReport(Sheet)` (L309-343) contains hardcoded test data ("ALM", "VIC", "LAVERTON", year "2011") that appears to be a development placeholder
- `setFoot(Sheet)` (L304-307) has the comment "doesn't work"
- `getBody()` (L239-241) always returns empty string

**Tests needed:** Tests documenting which methods are intentionally empty vs. incomplete, and verifying base class placeholder behavior.

---

### A09-015 -- ProcessBuilder used to execute external chart generation with stdout/stderr not handled
**Severity:** MEDIUM
**File:** `Frm_Linde_Reports.java` (line 2335)
**Details:** The `generateChart(String rpt_name)` method (L2335) uses a `ProcessBuilder` or `Runtime.exec()` to execute an external process for chart generation. Line 2369 contains `System.out.println(line)` for reading process output. If the external process fails, hangs, or produces large output, this could block the thread or silently fail. There is no timeout mechanism and `System.out.println` is used for logging in a server context.

**Tests needed:** Tests for process execution failure, timeout scenarios, and stderr handling.

---

## Summary

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | A09-001 |
| HIGH | 6 | A09-002, A09-003, A09-004, A09-005, A09-006, A09-007 |
| MEDIUM | 5 | A09-008, A09-009, A09-010, A09-011, A09-012 |
| LOW | 3 | A09-013, A09-014, A09-015 |
| **Total** | **15** | |

### Priority Testing Recommendations

If test infrastructure were to be added, the highest-impact tests would be:

1. **Frm_excel.getParam()** and **setParameters()** -- small, self-contained methods with pure logic that can be tested without mocking. Covers input parsing edge cases.
2. **Frm_excel.setTotalDuration()** -- testable string parsing and formatting logic with clear boundary conditions (hour > 10000 threshold).
3. **Frm_Linde_Reports.createExcel(opCode)** -- dispatch logic that should be tested with each known opCode plus invalid values. Would require DAO mocking.
4. **FileOutputStream cleanup** across all `createExcel()` methods -- critical resource management that should be verified with integration tests.
5. **Date parsing in Frm_Linde_Reports** -- the split/parseInt chain is fragile and easily testable in isolation if extracted to a utility method.
