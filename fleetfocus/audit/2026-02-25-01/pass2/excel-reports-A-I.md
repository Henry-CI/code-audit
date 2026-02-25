# Pass 2 — Test Coverage: excel/reports (Excel servlets A-I)
**Agent:** A11
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|---|---|
| Test framework (JUnit/TestNG) | **Not present** -- zero dependencies on any test framework |
| Test directories (`src/test/`, `test/`) | **Not present** |
| Build tool with test phase (Maven/Gradle) | **Not present** -- no `pom.xml`, no `build.xml`, no `build.gradle` |
| Mocking libraries (Mockito, EasyMock) | **Not present** |
| Test files matching `*Test*.java` | One file found: `EncryptTest.java` -- this is a utility class (encrypt/decrypt), **not** a test. It contains no assertions or test annotations. |
| Integration/E2E test harness | **Not present** |

**Conclusion:** The repository has **zero automated tests** of any kind. There is no test infrastructure, no test runner configuration, and no CI test pipeline. All 18 files audited below have **0% test coverage**.

---

## Reading Evidence

All files reside under:
`WEB-INF/src/com/torrent/surat/fms6/excel/reports/`

All classes extend `Frm_excel` (the shared base class for Excel report generation using Apache POI).

### 1. ExcelBatteryReport.java (121 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelBatteryReport(String docRoot, String fileName, BatteryReportBean bean) throws Exception` | 19 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 24 |
| 3 | `public void createBatteryReport(String cust, String loc, String dep, String st, String et)` | 43 |
| 4 | `public String getFileName()` | 117 |

**Notes:** Uses raw `ArrayList` (unparameterized). FileOutputStream not in try-with-resources. No input validation.

### 2. ExcelBroadcastMsgReport.java (137 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelBroadcastMsgReport(String docRoot, String fileName, ArrayList<BroadcastmsgBean> arrBroadCastMsgBean) throws Exception` | 18 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 23 |
| 3 | `public void createUnitUnlockReport(String cust, String loc, String dep, String st, String et)` | 42 |
| 4 | `public String getFileName()` | 131 |

**Notes:** Method name `createUnitUnlockReport` is misleading for a Broadcast Message report (copy-paste artifact). FileOutputStream not in try-with-resources.

### 3. ExcelCimplicityShockReport.java (144 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelCimplicityShockReport(String docRoot, String fileName, CimplicityShockReportBean cimpBean) throws Exception` | 22 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 27 |
| 3 | `public void createCimplicityShockReport(String cust, String loc, String dep, String from, String to) throws IOException` | 45 |
| 4 | `public String getFileName()` | 140 |

**Notes:** Instantiates `UnitDAO` (line 54) but never uses it. Duplicate import of `java.util.ArrayList`. Raw ArrayList casts. Complex index arithmetic for "best/worst" top/bottom 5 logic susceptible to off-by-one errors.

### 4. ExcelCimplicityUtilReport.java (141 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelCimplicityUtilReport(String docRoot, String fileName, CimplicityUtilReportBean cimpBean) throws Exception` | 22 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 27 |
| 3 | `public void createCimplicityUtilReport(String cust, String loc, String dep, String from, String to) throws IOException` | 45 |
| 4 | `public String getFileName()` | 137 |

**Notes:** Instantiates `UnitDAO` (line 62) but never uses it. Duplicate import. `setCellFormula` and `setCellValue` both called on same cell (lines 111-112) -- only the last write wins. Total calculation loop (lines 130-132) only retains the last element.

### 5. ExcelCurrDrivReport.java (126 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelCurrDrivReport(String docRoot, String fileName, CurrDrivReportBean currBean) throws Exception` | 20 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 25 |
| 3 | `public void createCurrDrivReport(String cust, String loc, String dep, String st, String et)` | 44 |
| 4 | `public String getFileName()` | 122 |

**Notes:** Instantiates `UnitDAO` (line 61) but never uses it. Duplicate import. Raw ArrayList. No null checks on bean data lists.

### 6. ExcelCurrUnitReport.java (132 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelCurrUnitReport(String docRoot, String fileName, CurrUnitReportBean currBean) throws Exception` | 20 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 25 |
| 3 | `public void createCurrUnitReport(String cust, String loc, String dep, String st, String et)` | 44 |
| 4 | `public String getFileName()` | 128 |

**Notes:** Instantiates `UnitDAO` (line 62) but never uses it. Potential NPE if `dep` is null (line 80 calls `.equalsIgnoreCase("all")`). Conditional column logic for "Dept" column only applies when `dep` == "all".

### 7. ExcelDailyVehSummaryReport.java (277 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDailyVehSummaryReport(String docRoot, String fileName, DailyVehSummaryReportBean dsumBean) throws Exception` | 22 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 28 |
| 3 | `public void createDSumReport(String cust, String loc, String dep, String st, String et)` | 46 |
| 4 | `public String getFileName()` | 272 |

**Notes:** Most complex of the simpler reports. References `RuntimeConf.cust_leader`, `RuntimeConf.cust_cimp`, `RuntimeConf.cust_combine` for conditional columns. Instantiates unused `UnitDAO`. Multiple conditional branches for customer type affect column layout -- high risk for column misalignment bugs without tests. `FormulaEvaluator` instantiated (line 85) but never used.

### 8. ExcelDriverAccessAbuseReport.java (198 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDriverAccessAbuseReport(String docRoot, String fileName, DriverAccessAbuseBean abuseBean) throws Exception` | 37 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws IOException, SQLException` | 42 |
| 3 | `public void createDriverAccessAbuseReport(String cust, String loc, String dep, String st, String et)` | 74 |
| 4 | `public String getFileName()` | 194 |

**Notes:** Declares instance-level raw ArrayLists as fields (lines 20-29) and then reassigns them in `createExcel`. Instantiates unused `UnitDAO` (line 81). Unused field `a_time_filter` (line 31). Uses `setCellFormula("VALUE(\""+tmp+"\")")` with user-derived content -- formula injection risk if `tmp` contains quotes or special characters.

### 9. ExcelDriverImpactReport.java (146 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDriverImpactReport(String docRoot, String fileName, DriverImpactReportBean dImpactBean) throws Exception` | 22 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et, String model) throws Exception` | 28 |
| 3 | `public void createDrivImpReport(String cust, String loc, String dep, String st, String et, String model) throws SQLException` | 47 |
| 4 | `public String getFileName()` | 142 |

**Notes:** Creates a `CustomerDAO` (line 65) and calls database methods (`getCustomerName`, `getLocationName`, `getDepartmentName`, `getModelName`) directly during Excel generation -- mixing I/O concerns. Throws `SQLException` from report builder method. `createExcel` has 6 parameters (different signature from other reports).

### 10. ExcelDriverLicenceExpiry.java (102 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDriverLicenceExpiry(String docRoot, String fileName, DriverLicenceExpiryBean bean) throws Exception` | 22 |
| 2 | `public String createExcel(String cust_cd, String loc_cd, String dept_cd) throws IOException, SQLException` | 27 |
| 3 | `public void createLicenceExpiryReport(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 45 |
| 4 | `public String getFileName()` | 98 |

**Notes:** `createExcel` signature differs from all other reports (3 params instead of 5, no date range). Creates `CustomerDAO` (line 50) and calls DB during report generation. Typo in title: "Driver LIcence Expiry Report" (capital I in "LIcence"). Typo in variable name: `vreveiw_date` (should be `vreview_date`).

### 11. ExcelDynDriverReport.java (307 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDynDriverReport(String docRoot, String fileName, DynDriverReportBean dynBean) throws Exception` | 22 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 27 |
| 3 | `public void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | 46 |
| 4 | `public String getFileName()` | 303 |

**Notes:** Method name `createDynUnitReport` is misleading -- this is a *driver* report. 4 levels of nested loops. Uses `StringTokenizer` for `do_list` parsing. `FormulaEvaluator` instantiated (line 149) but never used. Deeply nested ArrayList-of-ArrayList-of-ArrayList data structures with raw casts -- high risk for ClassCastException. Formula injection via `setCellFormula("VALUE(\""+stop+"\")")`.

### 12. ExcelDynSeenReport.java (214 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDynSeenReport(String docRoot, String fileName, DynSeenReportBean dynBean) throws Exception` | 22 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 27 |
| 3 | `public void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | 46 |
| 4 | `public String getFileName()` | 210 |

**Notes:** Method named `createDynUnitReport` but generates "Pedestrian Detection Report". `UnitDAO` instantiated (line 99) but never used. Duplicate import. Complex nested ArrayList structures with raw casts. `fld_hide` array created but never actually used in the output filtering (all fields always written at line 196-201).

### 13. ExcelDynTransportDriverReport.java (228 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDynTransportDriverReport(String docRoot, String fileName, DynDriverReportBean dynBean) throws Exception` | 17 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 22 |
| 3 | `public void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | 41 |
| 4 | `public String getFileName()` | 224 |

**Notes:** Method named `createDynUnitReport` but generates "Detailed Report by Transport Driver". Formula injection via `setCellFormula`. Deep nesting (4 levels). `vfld_hide` ArrayList declared (line 60) but never populated -- only the local `fld_hide` array is used.

### 14. ExcelDynUnitReport.java (328 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelDynUnitReport(String docRoot, String fileName, DynUnitReportBean dynBean) throws Exception` | 23 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 28 |
| 3 | `public void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | 47 |
| 4 | `public String getFileName()` | 324 |

**Notes:** Largest of the Dyn reports. Complex excluded vehicle logic (line 217, 268, 279). Formula injection via `setCellFormula`. Deep nesting (4 levels). `vfld_hide` ArrayList declared but never used. Duplicate variable `vrpt_veh_value_stopv` (line 59, same data as line 58).

### 15. ExcelExceptionSessionReport.java (354 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelExceptionSessionReport(String docRoot, String fileName, DynUnitReportBean dynBean) throws Exception` | 17 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception` | 22 |
| 3 | `public void createExceptionSessionReport(String cust, String loc, String dep, String st, String et)` | 41 |
| 4 | `public String getFileName()` | 350 |

**Notes:** Most feature-rich of the group. Handles `includeZLinde`, `opMode` (DT/MM/VOR), and `searchCrit` with URL decoding (line 136). URL decoding with empty catch block (lines 137-139). Bug at line 311: writes `veh_id` in the "Operational Mode" cell position when `vdriv_cd.size() == 0`. Formula injection via `setCellFormula`. Deep nesting. `vfld_hide` declared but unused.

### 16. ExcelHireDehireReport.java (135 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelHireDehireReport(String docRoot, String fileName, HireDehireReportBean hireDehireBean) throws Exception` | 18 |
| 2 | `public String createExcel(String st, String et, String sc) throws Exception` | 23 |
| 3 | `public void createHireDehireReport(String st, String et, String search_crit)` | 41 |
| 4 | `public String getFileName()` | 130 |

**Notes:** Different `createExcel` signature (3 params: st, et, sc). No customer/location/department parameters. Simple linear data layout.

### 17. ExcelImpactMeterReport.java (198 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelImpactMeterReport(String docRoot, String fileName, ImpactReportBean impBean) throws Exception` | 31 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws IOException, SQLException` | 36 |
| 3 | `private void createImpactReport(String cust, String loc, String dep, String st, String et, Sheet sheet) throws SQLException, IOException` | 60 |
| 4 | `public String getFileName()` | 190 |

**Notes:** `createImpactReport` is `private` (only private report-builder in this group). Instance-level raw ArrayList fields for report data (lines 22-29). Hardcoded URL `http://fleetfocus.lindemh.com.au/fms/` (line 176) -- environment-specific, not configurable. Instantiates unused `UnitDAO` (line 77). Complex photo embedding logic with row skipping.

### 18. ExcelImpactReport.java (254 lines)

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ExcelImpactReport(String docRoot, String fileName, ImpactReportBean impBean) throws Exception` | 34 |
| 2 | `public String createExcel(String cust, String loc, String dep, String st, String et) throws IOException, SQLException` | 39 |
| 3 | `private void createImpactReport(String cust, String loc, String dep, String st, String et, Sheet sheet) throws SQLException, IOException` | 63 |
| 4 | `public String getFileName()` | 246 |

**Notes:** Private report builder. Handles RTLS (Real-Time Location System) data with GeoJSON parsing (lines 212-236). JSON parsing in catch block does `e.printStackTrace()` only (line 235) -- swallows exception silently. Hardcoded URL `http://fleetfocus.lindemh.com.au/fms/` (line 191). Typo in GeoJSON output: "longtitue" should be "longitude" (line 221). Instance-level `vimp_rtlsjson` field shadowed by local variable at line 77. Instantiates unused `UnitDAO` (line 79).

---

## Findings

### A11-01 -- Zero Test Coverage Across All 18 Excel Report Classes
**Severity:** CRITICAL
**Files:** All 18 files in scope
**Details:** There are zero automated tests for any of the 18 Excel report generation classes. No unit tests, no integration tests, no test framework is present in the repository. Every public method is untested. This means:
- No verification that correct columns appear in correct order
- No verification that data is placed in correct cells
- No verification of conditional column logic (e.g., customer type branching in DailyVehSummaryReport)
- No verification of edge cases (empty data lists, null values, zero-length arrays)
- No regression protection for any bug fix or feature change

**Recommended tests:**
- Unit tests for each `createExcel()` method verifying output file creation and column layout
- Unit tests for conditional logic paths (customer type, department "all", excluded vehicles, etc.)
- Boundary tests for empty input data, null parameters
- Integration tests verifying end-to-end Excel file validity

---

### A11-02 -- FileOutputStream Resource Leak in All 18 Files
**Severity:** HIGH
**Files:** All 18 files
**Details:** Every `createExcel()` method follows this pattern:
```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
```
The `FileOutputStream` is not wrapped in a try-with-resources or try/finally block. If `wb.write(fileOut)` throws an exception, the stream will not be closed, resulting in a file handle leak. This pattern is identical across all 18 files.

**Testing gap:** No tests verify behavior under write-failure conditions.

---

### A11-03 -- Excel Formula Injection via setCellFormula with Unsanitized Input
**Severity:** HIGH
**Files:** ExcelCimplicityUtilReport.java (line 111), ExcelDailyVehSummaryReport.java (lines 171, 185, 195, 207, 222), ExcelDriverAccessAbuseReport.java (lines 162, 173, 185), ExcelDriverImpactReport.java (line 130), ExcelDynDriverReport.java (line 244), ExcelDynTransportDriverReport.java (line 210), ExcelDynUnitReport.java (line 255), ExcelExceptionSessionReport.java (lines 274, 279, 293)
**Details:** Multiple files call `setCellFormula("VALUE(\""+variable+"\")")` where the variable content originates from bean data (ultimately from database/user input). If the variable contains a double-quote character or formula syntax, this can produce:
1. Malformed Excel formulas causing file corruption
2. Potential Excel formula injection if values contain `=`, `+`, `-`, or `@` prefixes

**Testing gap:** No tests validate formula generation with special characters or adversarial input.

---

### A11-04 -- Unused UnitDAO Instantiation Across 10+ Files
**Severity:** MEDIUM
**Files:** ExcelCimplicityShockReport.java (line 54), ExcelCimplicityUtilReport.java (line 62), ExcelCurrDrivReport.java (line 61), ExcelCurrUnitReport.java (line 62), ExcelDailyVehSummaryReport.java (line 93), ExcelDriverAccessAbuseReport.java (line 81), ExcelDynDriverReport.java (line 107), ExcelDynSeenReport.java (line 99), ExcelImpactMeterReport.java (line 77), ExcelImpactReport.java (line 79)
**Details:** `UnitDAO unitDAO = new UnitDAO()` is instantiated inside the report creation methods but never referenced. This is wasted object allocation and potentially an unwanted database connection initialization (depending on the DAO constructor). This appears to be a copy-paste artifact across the codebase.

**Testing gap:** No tests would catch dead code or unnecessary object instantiation.

---

### A11-05 -- Database Calls During Excel Generation (ExcelDriverImpactReport, ExcelDriverLicenceExpiry)
**Severity:** MEDIUM
**Files:** ExcelDriverImpactReport.java (lines 71-74), ExcelDriverLicenceExpiry.java (lines 50, 60-63)
**Details:** These two files create `CustomerDAO` and call database methods (`getCustomerName()`, `getLocationName()`, `getDepartmentName()`, `getModelName()`) during the Excel report building phase. This mixes data retrieval with presentation, making the code:
- Untestable without a live database
- Prone to `SQLException` during report generation
- Impossible to unit-test in isolation

**Testing gap:** No tests; would require database mocking to achieve unit test coverage.

---

### A11-06 -- Misleading Method Names (Copy-Paste Artifacts)
**Severity:** MEDIUM
**Files:**
- ExcelBroadcastMsgReport.java: method `createUnitUnlockReport()` (line 42) -- should be `createBroadcastMsgReport()`
- ExcelDynDriverReport.java: method `createDynUnitReport()` (line 46) -- should be `createDynDriverReport()`
- ExcelDynSeenReport.java: method `createDynUnitReport()` (line 46) -- should be `createDynSeenReport()`
- ExcelDynTransportDriverReport.java: method `createDynUnitReport()` (line 41) -- should be `createDynTransportDriverReport()`

**Details:** These method names do not match the actual report they produce. This is evidence of copy-paste development where the original method name was not updated. Without tests, there is no executable documentation confirming correct behavior.

---

### A11-07 -- NullPointerException Risk with Unvalidated Bean Data
**Severity:** HIGH
**Files:** All 18 files
**Details:** No file performs null checks on:
- Constructor parameters (docRoot, fileName, bean)
- Bean getter return values (ArrayList fields)
- Individual ArrayList elements before casting

For example, in ExcelCurrUnitReport.java (line 80): `dep.equalsIgnoreCase("all")` will throw NPE if `dep` is null. Similar patterns exist in ExcelDailyVehSummaryReport.java where `cust_type.equalsIgnoreCase()` is called without null guard.

**Testing gap:** No tests verify behavior with null or empty inputs.

---

### A11-08 -- Raw Type ArrayList Usage Across All Files
**Severity:** MEDIUM
**Files:** All 18 files
**Details:** Nearly every file uses unparameterized `ArrayList` with unchecked casts like `(String)vunit_name.get(i)`. This creates runtime `ClassCastException` risk if the bean data contains unexpected types. The Dyn* reports are particularly dangerous, using ArrayList-of-ArrayList-of-ArrayList structures (3+ levels deep) with raw type casts at each level.

**Testing gap:** No type-safety tests exist. Generics would eliminate the need for such tests, but the raw types remain.

---

### A11-09 -- Hardcoded Production URL in Impact Reports
**Severity:** MEDIUM
**Files:** ExcelImpactMeterReport.java (line 176), ExcelImpactReport.java (line 191)
**Details:** Both files contain:
```java
String tmp = "http://fleetfocus.lindemh.com.au/fms/" + RuntimeConf.impactDir + "/" + img_link.get(j);
```
This hardcodes the production domain (`http://fleetfocus.lindemh.com.au`) in the source code. The URL is HTTP (not HTTPS). This would break in any non-production environment and constitutes a security concern (HTTP for potentially sensitive fleet data).

**Testing gap:** No tests verify URL construction or environment-specific configuration.

---

### A11-10 -- Swallowed Exceptions in ExcelExceptionSessionReport and ExcelImpactReport
**Severity:** HIGH
**Files:** ExcelExceptionSessionReport.java (lines 137-139), ExcelImpactReport.java (lines 233-236)
**Details:**
- ExcelExceptionSessionReport: URL decoding failure is caught and silently ignored:
  ```java
  try { searchCrit = java.net.URLDecoder.decode(searchCrit, "UTF-8"); }
  catch (Exception e) { // If there's an error decoding, use the original value }
  ```
- ExcelImpactReport: JSON parsing failure results in only `e.printStackTrace()` with no error propagation:
  ```java
  catch (JSONException e) { e.printStackTrace(); }
  ```
  This means RTLS location/speed data silently disappears from the report if JSON is malformed, and the cells for that row are never created.

**Testing gap:** No tests verify error handling paths or confirm correct behavior when parsing fails.

---

### A11-11 -- Bug: Duplicate Data Written to Wrong Cell in ExcelExceptionSessionReport
**Severity:** HIGH
**File:** ExcelExceptionSessionReport.java (lines 300-312)
**Details:** When `vdriv_cd.size() == 0` (no driver data), the code writes:
```java
contentCell = row.createCell(m++); // cell 0: veh_nm
contentCell.setCellValue(veh_nm);
contentCell = row.createCell(m++); // cell 1: veh_id
contentCell.setCellValue(veh_id);
contentCell = row.createCell(m++); // cell 2: veh_id AGAIN (should be operational mode or empty)
contentCell.setCellValue(veh_id);
```
Line 311 writes `veh_id` into the "Operational Mode" column position. This is a likely bug.

**Testing gap:** A test with empty driver data would catch this immediately.

---

### A11-12 -- GeoJSON Output Typo in ExcelImpactReport
**Severity:** LOW
**File:** ExcelImpactReport.java (line 221)
**Details:** The location string is constructed as:
```java
location += "[longtitue:" + coordinates.getString(0) + ...
```
"longtitue" should be "longitude". This typo appears in the Excel output visible to end users.

**Testing gap:** A simple string assertion test would catch this.

---

### A11-13 -- Inconsistent createExcel() Method Signatures
**Severity:** LOW
**Files:** Multiple
**Details:** The `createExcel()` method has at least 4 different signatures across the 18 files:
1. `createExcel(String cust, String loc, String dep, String st, String et)` -- 12 files
2. `createExcel(String cust, String loc, String dep, String st, String et, String model)` -- ExcelDriverImpactReport
3. `createExcel(String cust_cd, String loc_cd, String dept_cd)` -- ExcelDriverLicenceExpiry
4. `createExcel(String st, String et, String sc)` -- ExcelHireDehireReport

This prevents a common interface or polymorphic usage pattern. Without tests or an interface contract, it is unclear whether these variations are intentional or accidental.

---

### A11-14 -- Variable Shadowing in ExcelImpactReport
**Severity:** MEDIUM
**File:** ExcelImpactReport.java (lines 32 vs 77)
**Details:** Instance field `vimp_rtlsjson` (line 32) is shadowed by a local variable with the same name at line 77:
```java
ArrayList vimp_rtlsjson = impBean.getVimp_rtlsjson(); // local, shadows field
```
The local variable is used at line 139 but the instance field at line 32 remains null. If any code path referenced the instance field, it would get null. This is a maintenance trap.

**Testing gap:** No tests exercise RTLS-enabled vs disabled paths.

---

### A11-15 -- Duplicate Import Statements
**Severity:** LOW
**Files:** ExcelCimplicityShockReport.java, ExcelCimplicityUtilReport.java, ExcelCurrDrivReport.java, ExcelCurrUnitReport.java, ExcelDailyVehSummaryReport.java, ExcelDriverAccessAbuseReport.java, ExcelDriverImpactReport.java, ExcelDynDriverReport.java, ExcelDynSeenReport.java, ExcelDynUnitReport.java, ExcelExceptionSessionReport.java
**Details:** 11 of 18 files contain `import java.util.ArrayList;` twice. While this is a compiler warning rather than an error, it is a quality indicator suggesting copy-paste development without IDE cleanup.

---

## Summary Table

| Finding | Severity | Files Affected | Category |
|---|---|---|---|
| A11-01: Zero test coverage | CRITICAL | 18/18 | Test Infrastructure |
| A11-02: FileOutputStream resource leak | HIGH | 18/18 | Resource Management |
| A11-03: Formula injection risk | HIGH | 12/18 | Security |
| A11-04: Unused UnitDAO instantiation | MEDIUM | 10/18 | Dead Code |
| A11-05: DB calls during Excel generation | MEDIUM | 2/18 | Architecture |
| A11-06: Misleading method names | MEDIUM | 4/18 | Maintainability |
| A11-07: NPE risk from unvalidated data | HIGH | 18/18 | Robustness |
| A11-08: Raw type ArrayList usage | MEDIUM | 18/18 | Type Safety |
| A11-09: Hardcoded production URL | MEDIUM | 2/18 | Configuration |
| A11-10: Swallowed exceptions | HIGH | 2/18 | Error Handling |
| A11-11: Bug: wrong cell data | HIGH | 1/18 | Correctness |
| A11-12: GeoJSON typo "longtitue" | LOW | 1/18 | Correctness |
| A11-13: Inconsistent method signatures | LOW | 4/18 | API Design |
| A11-14: Variable shadowing | MEDIUM | 1/18 | Maintainability |
| A11-15: Duplicate imports | LOW | 11/18 | Code Quality |

**Total findings:** 15
- CRITICAL: 1
- HIGH: 5
- MEDIUM: 6
- LOW: 3
