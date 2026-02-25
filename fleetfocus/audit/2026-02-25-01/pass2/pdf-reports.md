# Pass 2 -- Test Coverage: pdf + reports packages
**Agent:** A16
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Criterion | Status |
|---|---|
| Test directory present | **NO** -- no `test/`, `src/test/`, or `__tests__` directory exists anywhere in the repository |
| Test framework configured | **NO** -- no JUnit, TestNG, Mockito, or any test library in build configuration |
| Test runner configured | **NO** -- no Maven Surefire, Gradle test task, or Ant test target detected |
| CI test stage | **NO** -- no evidence of automated test execution in CI |
| **Overall test coverage** | **0% -- ZERO tests exist for any of the 13 audited files** |

All 13 files in the `pdf` and `reports` packages have **no unit tests, no integration tests, and no test infrastructure of any kind**. Every public method, private method, error path, SQL query, and PDF generation flow is entirely untested.

---

## Reading Evidence

### 1. MonthlyPDFRpt.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java`
- **Lines:** 173
- **Class:** `MonthlyPDFRpt extends ReportPDF`
- **Public methods:**

| Line | Signature |
|---|---|
| 27 | `public MonthlyPDFRpt(String cust_cd, String loc_cd, String dept_cd, String set_month, String st_dt, String end_dt) throws Exception` |
| 35 | `public String createPdf() throws IOException, DocumentException, SQLException` |

- **Private methods:** `addContent()` (L47), `addTitlePage()` (L61), `fetch_chart()` (L90), `createTable()` (L101)
- **Key behaviors:** Generates PDF report with iText; calls `PreCheckDAO.getCheckSummary()` for table data; reads chart images from filesystem; builds 3-column table of fleet check summaries.

### 2. ReportPDF.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java`
- **Lines:** 236
- **Class:** `ReportPDF` (base class for PDF generation)
- **Public methods:**

| Line | Signature |
|---|---|
| 45 | `public ReportPDF(String cust_cd, String loc_cd, String dept_cd, String month, String st_dt, String end_dt) throws Exception` |
| 178 | `public String getPdfurl()` |
| 182 | `public void setPdfurl(String pdfurl)` |
| 187 | `public String getResult()` |
| 191 | `public void setResult(String result)` |
| 195 | `public String getTitle()` |
| 199 | `public void setTitle(String title)` |
| 203 | `public String getFrom()` |
| 207 | `public void setFrom(String from)` |
| 211 | `public String getTo()` |
| 215 | `public void setTo(String to)` |
| 219 | `public String getMonth()` |
| 223 | `public void setMonth(String month)` |
| 227 | `public Document getDocument()` |
| 231 | `public void setDocument(Document document)` |

- **Protected methods:** `createPdf()` (L61), `addMetaData()` (L102), `addFooter()` (L118), `createList()` (L131), `addEmptyLine()` (L139), `addImage()` (L147), `getExportDir()` (L166)
- **Key behaviors:** Base PDF class using iText library; `getExportDir()` uses fragile path traversal with `getProtectionDomain().getCodeSource().getLocation()` and 7 levels of `/../`; `addImage()` reads image from filesystem and scales.

### 3. Databean_cdisp.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java`
- **Lines:** 1,747
- **Class:** `Databean_cdisp`
- **Public methods:**

| Line | Signature |
|---|---|
| 120 | `public void clear_variables()` |
| 1264 | `public void init()` |
| 1447+ | ~60 getter/setter methods for fields (set_gmtp_id, get_user_fnm, etc.) |

- **Key behaviors:** JSP databean with `init()` as entry point; dispatches on `set_opcode` to call private methods: `Fetch_summary_data()`, `Fetch_summary_data_au()`, `Fetch_Data()`, `impact_data()`, `impact_data_au()`, `hire_veh_data()`, etc. All use string-concatenated SQL queries with JNDI data source.

### 4. Databean_dyn_reports.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java`
- **Lines:** 10,015
- **Class:** `Databean_dyn_reports`
- **Public methods:**

| Line | Signature |
|---|---|
| 201 | `public void clear_variables()` |
| 7767 | `public void init()` |
| 9521 | `public void fetchNames() throws SQLException` |
| 7512 | `public String getDept_prefix(String vcd) throws SQLException` |
| 8264+ | ~200 getter/setter methods |

- **Key behaviors:** Massive report databean; `init()` dispatches on `set_op_code` to dozens of private methods including `Fetch_data()`, `Fetch_data_au()`, `Fetch_curr_data_au()`, `fetchDriverLeagueDetails()`, `fetchVorReportData()`, `fetchExceptionSessionReportData()`, etc. All SQL is string-concatenated.

### 5. Databean_report.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java`
- **Lines:** 21,854 (largest file in assignment)
- **Class:** `Databean_report`
- **Public methods:**

| Line | Signature |
|---|---|
| 584 | `public void clear_variables()` |
| 1864 | `public String filterUnitDriverOptions()` |
| 1993 | `public String setTimePadding(String time)` |
| 12376 | `public String getDept_prefix(String vcd) throws SQLException` |
| 12941 | `public String getImageFromByte(InputStream in, String fname)` |
| 13906 | `public String getImageFromByte(byte[] convertObject, String fname)` |
| 14118 | `public ArrayList HourAdd(String simpledataformat, String oldDate, ...)` |
| 17582 | `public void addUtilModelBean(UtilModelBean putil)` |
| 18511 | `public void init()` |
| 1315 | `public String getDebuger()` |
| 2024+ | ~300 getter/setter methods |

- **Key behaviors:** Largest databean with ~22K lines; `init()` dispatches on `set_opcode` to dozens of report-fetching private methods including `Fetch_Data()`, `Fetch_operation_details()`, `Fetch_abuse_details()`, `Fetch_driver_licence()`, PDF generation (`MonthlyPDFRpt`), chart generation, email sending, etc. Contains image-from-byte conversion methods, date/time arithmetic, and extensive SQL queries.

### 6. Databean_report1.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java`
- **Lines:** 817
- **Class:** `Databean_report1`
- **Public methods:**

| Line | Signature |
|---|---|
| 100 | `public void clear_variables()` |
| 394 | `public void init()` |
| 453+ | ~30 getter/setter methods |

- **Key behaviors:** Simpler report databean; `init()` dispatches on `set_opcode` "report1" to fetch users and data; `Fetch_Data()` performs SQL queries with string concatenation including date filtering; `convert_time()` converts centiseconds to HH:MM:SS.

### 7. Databean_reports.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_reports.java`
- **Lines:** 127
- **Class:** `Databean_reports`
- **Public methods:**

| Line | Signature |
|---|---|
| 49 | `public void clearVectors()` (empty body) |

- **Key behaviors:** Appears to be a stub/placeholder class. The only non-trivial code is a commented-out `query()` method (lines 52-125). `clearVectors()` has an empty body.

### 8. LinderReportDatabean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/LinderReportDatabean.java`
- **Lines:** 1,935
- **Class:** `LinderReportDatabean`
- **Public methods:**

| Line | Signature |
|---|---|
| 59 | `public LinderReportDatabean()` |
| 63 | `public void init()` |
| 203 | `public void fetchUnitUtilisationReport() throws SQLException` |
| 326 | `public void fetchImpactReport() throws SQLException` |
| 415 | `public void fetchPreopCheckReport() throws SQLException` |
| 508 | `public void fetchSupervisorLockout() throws SQLException` |
| 554 | `public void fetchDriverLockout() throws SQLException` |
| 599 | `public ArrayList<ImpactBean> getImpacts(String cust_cd, String loc_cd) throws SQLException` |
| 679 | `public void fetchNationalPreopCheckReport() throws SQLException` |
| 780 | `public void fetchNationalPreopCheckCompleted() throws SQLException` |
| 911 | `public void fetchNationalPreopCheckCompletionTime() throws SQLException` |
| plus others (fetchUtilByDriverLogon, fetchNat2PreopChecks, fetchImpactByUnitWithUtil, fetchImpactByDriverWithUtil, fetchWorkHours) |

- **Key behaviors:** `init()` dispatches by `opCode` to various report methods; SQL queries use string concatenation; fetches from multiple data sources; heavy use of multiple Statement/ResultSet pairs.

### 9. RTLSHeatMapReport.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/RTLSHeatMapReport.java`
- **Lines:** 525
- **Class:** `RTLSHeatMapReport extends Reports`
- **Public methods:**

| Line | Signature |
|---|---|
| 33 | `public String getDensity()` |
| 37 | `public void setDensity(String density)` |
| 40 | `public ArrayList<Points> getArrPoints()` |
| 44 | `public void setArrPoints(ArrayList<Points> arrPoints)` |
| 504 | `public void init()` |
| 512 | `public void getPointsJson()` |

- **Private methods:** `getPoints()` (L49), `getSessionPoints()` (L127), `addWeight()` (L210), `getVehDuration()` (L255), `getVehSession()` (L279), `getOrigin()` (L384), `createJSON()` (L440)
- **Key behaviors:** RTLS heat map generation; connects to both PostgreSQL (via DBUtil.getConnection) and MySQL (via DBUtil.getMySqlConnection); builds GeoJSON output; uses PreparedStatement (better than most classes); grid clustering for point reduction.

### 10. RTLSImpactReport.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/RTLSImpactReport.java`
- **Lines:** 1,262
- **Class:** `RTLSImpactReport extends Reports`
- **Public methods:**

| Line | Signature |
|---|---|
| 38 | `public double getMaxSpeed()` |
| 44 | `public void setMaxSpeed(double maxSpeed)` |
| 897 | `public void getPointsJson()` |
| 920 | `public void generateSpeedList()` |
| 940 | `public void caculateImpactCacheTable()` |
| plus getters/setters for speedMap, speedMapwithFilter, shock_id, map_dt, veh_cd, geojson |

- **Private methods:** `get_impact_points()` (L53), `getVehName()` (L125), `check_location_exist()` (L183), `check_speed_exist()` (L246), `save_impact_points()` (L309), `update_impact_cached()` (L369), `saveSpeed()` (L427), `getPoints()` (L484), `getSpeed()` (L623), `caculatespeed()` (L686), `createJSON()` (L854), `getRedImpact()` (L967)
- **Key behaviors:** Impact location visualization; caches computed data in database; speed calculation with moving average filtering; writes GeoJSON; uses both MySQL and PostgreSQL data sources.

### 11. Reports.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Reports.java`
- **Lines:** 608
- **Class:** `Reports` (base class for RTLS reports)
- **Public methods:**

| Line | Signature |
|---|---|
| 49 | `public void Fetch_customers()` |
| 111 | `public void Fetch_cust_locations()` |
| 177 | `public void Fetch_cust_depts()` |
| 265 | `public void Fetch_cust_veh()` |
| 331 | `public int getVehTag(int veh_cd)` |
| 399+ | ~30 getter/setter methods |

- **Key behaviors:** Base class providing customer/location/department/vehicle fetching; all use `DBUtil.getConnection()` with Statement; SQL built via string concatenation with access control filtering; `getVehTag()` queries RTLS tag mapping.

### 12. UtilBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/UtilBean.java`
- **Lines:** 71
- **Class:** `UtilBean implements Comparable<UtilBean>`
- **Public methods:**

| Line | Signature |
|---|---|
| 11 | `public int[] getUtil_no_veh_day()` |
| 15 | `public void setUtil_no_veh_day(int[] util_no_veh_day)` |
| 19 | `public String getUtil_date()` |
| 23 | `public void setUtil_date(String util_date)` |
| 27 | `public String getUtil_day()` |
| 31 | `public void setUtil_day(String util_day)` |
| 36 | `public String[] getSiteOpen()` |
| 40 | `public void setSiteOpen(String[] siteOpen)` |
| 44 | `public int compareTo(UtilBean util1)` |
| 48 | `public int getDay_num()` |
| 52 | `public int setDayNum(String day)` |

- **Key behaviors:** Simple POJO/data-holder for utilisation data; `compareTo` sorts by day number; `setDayNum()` maps day names to integers (Monday=0, Tuesday=1, ..., Sunday=6). Note: Monday maps to default 0 (implicit fall-through).

### 13. UtilModelBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/UtilModelBean.java`
- **Lines:** 65
- **Class:** `UtilModelBean`
- **Public methods:**

| Line | Signature |
|---|---|
| 12 | `public int getAvatruck()` |
| 16 | `public void setAvatruck(int avatruck)` |
| 22 | `public void add(UtilBean item)` |
| 26 | `public String getCustomer()` |
| 30 | `public void setCustomer(String customer)` |
| 34 | `public String getSite()` |
| 38 | `public void setSite(String site)` |
| 42 | `public String getDepartment()` |
| 46 | `public void setDepartment(String department)` |
| 50 | `public String getModel()` |
| 54 | `public void setModel(String model)` |
| 58 | `public ArrayList getUb()` |
| 62 | `public void setUb(ArrayList ub)` |

- **Key behaviors:** Simple POJO/data-holder; wraps a list of UtilBeans with customer/site/department/model context. Uses raw `ArrayList` without type parameter.

---

## Findings

### A16-01 -- CRITICAL: Zero test coverage across 39,435 lines of code (all 13 files)
- **Severity:** CRITICAL
- **Files:** All 13 audited files
- **Detail:** The entire `pdf` and `reports` packages contain 39,435 lines of Java code with zero automated tests. There is no test framework, no test directory, no test runner, and no CI test stage. Every code path -- including PDF generation, SQL queries, data transformations, chart generation, GeoJSON construction, date calculations, and email sending -- is completely untested. This means:
  - Regressions are undetectable until runtime/production
  - Refactoring is extremely risky
  - SQL injection vulnerabilities cannot be verified as fixed
  - Edge cases in date/time conversions are unknown
  - PDF output correctness is unverifiable

### A16-02 -- CRITICAL: Pervasive SQL injection via string concatenation (all databean files)
- **Severity:** CRITICAL
- **Files:** `Databean_cdisp.java`, `Databean_dyn_reports.java`, `Databean_report.java`, `Databean_report1.java`, `LinderReportDatabean.java`, `Reports.java`
- **Detail:** Nearly every SQL query in these files is built via string concatenation with user-controlled parameters. Examples:
  - `Databean_report1.java` L154: `query="select \"USER_CD\" from \"FMS_USR_GRP_REL\" where \"GROUP_CD\"='"+set_gp_cd+"'"`
  - `Databean_report1.java` L242-246: Full SQL with `set_user_cd`, `st_dt`, `end_dt` concatenated directly
  - `Databean_dyn_reports.java` L266: `query = "select ... where \"FMS_VEHICLE_MST\".\"VEHICLE_CD\" = " + ucd`
  - `Databean_dyn_reports.java` L316: `sel_site = "and \"LOC_CD\" = '" + set_loc_cd + "'"`
  - `Reports.java` L63: `query += " where \"USER_CD\" = " + access_cust` (no quotes at all)
  - `Reports.java` L124: `" and \"LOC_CD\" = \"LOCATION_CD\" and \"USER_CD\" = "+set_cust_cd` (no quotes)
  - `LinderReportDatabean.java` L219: `query = "select \"NAME\" from \"FMS_LOC_MST\" where \"LOCATION_CD\"="+locArray[i]`
- **Impact without tests:** SQL injection attacks cannot be ruled out; no test can verify parameterized query migration correctness.
- **Needed tests:** Parameterized query tests, input validation tests, boundary tests for all SQL-executing methods.

### A16-03 -- HIGH: No tests for PDF generation correctness (MonthlyPDFRpt, ReportPDF)
- **Severity:** HIGH
- **Files:** `MonthlyPDFRpt.java`, `ReportPDF.java`
- **Detail:** PDF generation has zero test coverage. Critical untested areas:
  - `createPdf()` (L35-44 in MonthlyPDFRpt): Full PDF generation pipeline -- metadata, title page, content, footer, document close. No verification that output is valid PDF.
  - `addTitlePage()` (L61-88 in MonthlyPDFRpt): Makes DAO calls (`UnitDAO.getCustName()`, etc.) during PDF construction; SQL failures will leave document in corrupted state.
  - `createTable()` (L101-171 in MonthlyPDFRpt): Calls `PreCheckDAO.getCheckSummary()` for data. Exception catch block at L167 only calls `e.printStackTrace()`, then still adds table to document (potentially empty/malformed).
  - `getExportDir()` (L166-174 in ReportPDF): Uses fragile 7-level path traversal `"/../../../../../../../excelrpt/"` from code source location. No tests verify this resolves correctly on different deployments.
  - `addImage()` (L147-164 in ReportPDF): Silently skips if file does not exist. No error reporting if chart images are missing.
- **Needed tests:** PDF output validation, table data correctness, missing-image handling, path resolution, title page with empty/null date ranges.

### A16-04 -- HIGH: No tests for massive init() dispatcher methods
- **Severity:** HIGH
- **Files:** `Databean_report.java` (L18511), `Databean_dyn_reports.java` (L7767), `Databean_cdisp.java` (L1264), `LinderReportDatabean.java` (L63)
- **Detail:** Each databean has an `init()` method that is the primary entry point called from JSP pages. These methods:
  - Acquire JNDI data source connections
  - Dispatch on opcode strings to dozens of private methods
  - Execute multiple SQL queries in sequence
  - Databean_report.init() dispatches to ~30+ different opcodes in 300+ lines of if/else blocks
  - Databean_dyn_reports.init() dispatches to ~15+ opcodes
  - No test verifies that any opcode routing works correctly
  - No test verifies connection cleanup happens on all paths
- **Needed tests:** Opcode dispatch tests, connection lifecycle tests, invalid opcode handling tests.

### A16-05 -- HIGH: No tests for error handling paths -- silent exception swallowing
- **Severity:** HIGH
- **Files:** All databean files, `RTLSHeatMapReport.java`, `RTLSImpactReport.java`
- **Detail:** Error handling throughout uses bare `e.printStackTrace()` or `System.out.println()` with no recovery strategy. Examples:
  - `MonthlyPDFRpt.java` L167-169: `catch(Exception e){ e.printStackTrace(); }` -- swallows exception during table creation, continues to add potentially malformed table
  - `Databean_report1.java` L425-428: `System.out.println(" Exception in Databean_report1 In " + methodName ...)` -- prints query with potential sensitive data to stdout
  - `LinderReportDatabean.java` L116-119: `exception.printStackTrace(); System.out.println(...)` -- prints query to stdout
  - `RTLSImpactReport.java` L88-91 and dozens more: generic `catch (Exception exception) { exception.printStackTrace(); }` throughout all DB methods
  - All SQL resource cleanup in finally blocks also catches and prints exceptions individually
- **Needed tests:** Exception path tests verifying resource cleanup, error state verification, no data leakage in error messages.

### A16-06 -- HIGH: No tests for date/time conversion and calculation logic
- **Severity:** HIGH
- **Files:** `Databean_report1.java`, `Databean_dyn_reports.java`, `Databean_report.java`, `LinderReportDatabean.java`
- **Detail:** Multiple date/time conversion functions with no tests:
  - `Databean_report1.java` L318-392: `convert_time(String csec)` -- converts centiseconds to "HH:MM:SS". Hand-rolled math with nested if/else for zero-padding. Division by 100 for seconds, then modular arithmetic. Edge cases (negative input, zero, overflow) completely untested.
  - `Databean_dyn_reports.java` L866-884: `to_sec(String tm)` -- parses "HH:MM:SS" to seconds using StringTokenizer. Will fail on malformed input (empty string, missing colons).
  - `LinderReportDatabean.java` `convert_time1()` -- another time conversion with similar risks
  - `Databean_report.java` L14118: `HourAdd()` -- date arithmetic method
  - `MonthlyPDFRpt.java` L71-80: Calendar-based month handling with `cal.MONTH` (static field access via instance, returns 0-indexed month)
- **Needed tests:** Boundary tests (0 seconds, max int, negative values), format validation, timezone handling.

### A16-07 -- HIGH: No tests for RTLS GeoJSON generation and speed calculations
- **Severity:** HIGH
- **Files:** `RTLSHeatMapReport.java`, `RTLSImpactReport.java`
- **Detail:** Complex spatial calculations with no tests:
  - `RTLSHeatMapReport.createJSON()` (L440-500): Builds GeoJSON with coordinate transformations, standard deviation normalization, and grid clustering. Incorrect output would display wrong heatmap data.
  - `RTLSImpactReport.caculatespeed()` (L686-852): Speed calculation with micro-second interval handling, corrupted speed filtering (>20m/s), and interval bucketing. Complex math with many edge cases.
  - `RTLSImpactReport.calculateDistanceBetweenPoints()`: Distance calculation between spatial points.
  - `RTLSHeatMapReport.addWeight()` (L210-252): Calculates point weights based on time intervals between position records. Division by 1000 could produce unexpected results.
  - `LonLatConverter.computerThatLonLat()` called with reversed/negated coordinates: `lonlat.computerThatLonLat(entry.getKey().getY(), -entry.getKey().getX())` -- no test verifies this transform is correct.
- **Needed tests:** Coordinate transformation tests, speed calculation boundary tests, empty point array handling, GeoJSON schema validation.

### A16-08 -- MEDIUM: No tests for UtilBean.compareTo() and day mapping logic
- **Severity:** MEDIUM
- **Files:** `UtilBean.java`
- **Detail:** `compareTo()` at L44 compares day numbers as strings via `String.valueOf(day_num).compareTo(...)`. This means numeric comparison breaks for values >= 10 (string "10" < "2"). Currently safe because day values are 0-6, but fragile. Additionally, `setDayNum()` at L52-68 maps day names but has no explicit "Monday" case -- it falls through to the default returning 0. If the day name is "Monday", it correctly returns 0, but any unknown day name also returns 0, making Monday indistinguishable from invalid input.
- **Needed tests:** compareTo ordering verification, day name mapping for all 7 days, unknown day name handling.

### A16-09 -- MEDIUM: No tests for raw ArrayList usage and type safety
- **Severity:** MEDIUM
- **Files:** All databean files, `UtilModelBean.java`
- **Detail:** Pervasive use of raw `ArrayList` without generic type parameters throughout all databean classes. Examples:
  - `Databean_cdisp.java` L57: `ArrayList vgmtp_id = new ArrayList()`
  - `Databean_dyn_reports.java` L88-184: ~100 raw ArrayLists declared as fields
  - `Databean_report.java` L162-443: ~150+ raw ArrayLists
  - `UtilModelBean.java` L20: `private ArrayList ub = new ArrayList()`
  - Values are cast with `(String)` at runtime (e.g., `set_gp_cd=(String)group_cd.get(0)`) -- ClassCastException risk
- **Without tests:** Type safety cannot be verified; runtime ClassCastExceptions are possible.

### A16-10 -- MEDIUM: No tests for connection/resource lifecycle management
- **Severity:** MEDIUM
- **Files:** All databean files, `Reports.java`, `RTLSHeatMapReport.java`, `RTLSImpactReport.java`
- **Detail:** Every databean manually manages JDBC resources (Connection, Statement, ResultSet) in finally blocks. Pattern is error-prone:
  - Multiple Statement fields (stmt, stmt1, stmt2, stmt3, stmt4) used as instance variables -- not thread-safe
  - `Databean_report.java` creates 5 statements at init: L18524-18528
  - `RTLSImpactReport.java` opens and closes separate connections in every private method (e.g., L56-117, L128-176, L185-240, L253-303...) -- high connection overhead
  - `LinderReportDatabean.java` L122-200: Manually closes rset, rset1, rset2, rset3, rset4, stmt, stmt1, stmt2, stmt3, stmt4, conn in finally block
  - Some methods rely on class-level ResultSet being closed by other methods
- **Needed tests:** Connection leak tests, concurrent access tests, resource cleanup verification.

### A16-11 -- MEDIUM: No tests for Databean_reports.java (dead/incomplete code)
- **Severity:** MEDIUM
- **Files:** `Databean_reports.java`
- **Detail:** This 127-line class appears to be dead code or an incomplete implementation:
  - `clearVectors()` at L49 has an empty method body
  - The only substantial code is a commented-out `query()` method (L52-125)
  - The commented-out code references `rset2` and `stmt2` which are not declared as fields
  - No `init()` method exists
- **Impact:** Without tests, it is unclear whether this class is used anywhere or can be safely removed.

### A16-12 -- MEDIUM: No tests for access control filtering logic
- **Severity:** MEDIUM
- **Files:** `Databean_dyn_reports.java`, `Databean_report.java`, `Reports.java`
- **Detail:** Access control is implemented via SQL WHERE clauses built from `access_level`, `access_cust`, `access_site`, `access_dept` fields. Logic includes:
  - `Reports.java` L58: `int access_l = access_level.equalsIgnoreCase("")?1:Integer.parseInt(access_level)` -- empty string defaults to level 1; NumberFormatException if non-numeric
  - `Databean_dyn_reports.java` L360-371: Access level parsing with `Integer.parseInt(access_level)` -- no validation
  - Hierarchical access checks: level > 2 restricts to specific site, level > 3 restricts to specific department
  - `Reports.java` L62-64: `query += " where \"USER_CD\" = " + access_cust` -- no SQL quoting on access_cust
- **Needed tests:** Access level boundary tests (0, 1, 2, 3, 4, empty, non-numeric), unauthorized access prevention, access filter bypass tests.

### A16-13 -- LOW: No tests for getExportDir() path resolution
- **Severity:** LOW
- **Files:** `ReportPDF.java`
- **Detail:** `getExportDir()` at L166-174 uses a fragile path resolution mechanism:
  ```java
  String dir = this.getClass().getProtectionDomain().getCodeSource().getLocation().toString().substring(6);
  int charCount = dir.length() - dir.replaceAll("/", "").length();
  int index = DataUtil.nthOccurrence(dir, '/', charCount-1);
  dir = dir.substring(0,index);
  dir +="/../../../../../../../excelrpt/";
  ```
  This assumes a specific deployment directory structure with exactly 7 levels of parent traversal. Will break on:
  - Different application server deployments
  - Containerized environments
  - Path with spaces (substring(6) skips "file:/")
  - Windows vs. Linux path separators
- **Needed tests:** Path resolution tests on different environments.

### A16-14 -- LOW: No tests for LinderReportDatabean report dispatch correctness
- **Severity:** LOW
- **Files:** `LinderReportDatabean.java`
- **Detail:** `init()` at L63-201 dispatches on `opCode` to 15+ different report methods. Some opcodes map to the same method:
  - `"nat2_preop_check_by_driver"` calls `fetchNationalPreopCheckCompleted()` (L101)
  - `"nat2_util_driver_all_models"` also calls `fetchNationalPreopCheckCompleted()` (L103) -- likely a copy-paste error
  - `"util_all_models"` calls `fetchUtilByDriverLogon()` (L105)
  - No test verifies these mappings are intentional vs. erroneous
- **Needed tests:** Opcode-to-method mapping tests, regression tests for copy-paste errors.

---

## Priority Summary

| Severity | Count | Findings |
|---|---|---|
| CRITICAL | 2 | A16-01 (zero test coverage), A16-02 (SQL injection) |
| HIGH | 5 | A16-03 (PDF generation), A16-04 (init dispatchers), A16-05 (error handling), A16-06 (date/time logic), A16-07 (RTLS/GeoJSON) |
| MEDIUM | 5 | A16-08 (UtilBean compareTo), A16-09 (raw ArrayList), A16-10 (connection lifecycle), A16-11 (dead code), A16-12 (access control) |
| LOW | 2 | A16-13 (path resolution), A16-14 (dispatch copy-paste) |

## Recommended Test Priority (if tests were to be added)

1. **Highest priority:** Parameterized query migration tests for all SQL-executing methods (addresses A16-02)
2. **High priority:** Unit tests for `convert_time()`, `to_sec()`, `setDayNum()`, `HourAdd()`, and other pure logic methods that can be tested without DB (addresses A16-06, A16-08)
3. **High priority:** Integration tests for `init()` dispatcher methods with mock DataSource (addresses A16-04)
4. **High priority:** GeoJSON output validation and speed calculation tests (addresses A16-07)
5. **Medium priority:** PDF generation tests with mock DAOs (addresses A16-03)
6. **Medium priority:** Access control enforcement tests (addresses A16-12)
7. **Lower priority:** Resource lifecycle tests, dead code identification (addresses A16-10, A16-11)
