# Pass 2 -- Test Coverage: excel/reports (Email classes)
**Agent:** A10
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

## Test Infrastructure Assessment

- **Test files found:** 0 (zero). No JUnit, TestNG, or any test framework present in the repository.
- **Build system:** No `pom.xml` or `build.xml` found. No Maven/Gradle/Ant build configuration.
- **Test directories:** No `test/` or `src/test/` directories exist.
- **Test dependencies:** No test framework JARs observed.
- **EncryptTest.java** in `util/` is a decompiled class (DJ decompiler, 2006), NOT an actual test.
- **Current test coverage for all 28 Email report classes: 0%**

## Common Pattern Summary

All 28 files extend `Frm_excel` (in `com.torrent.surat.fms6.excel`) and follow a highly consistent pattern:

1. **Constructor(s):** Accept customer/location/department/start-time/end-time/params/dir strings, delegate to `super()`, call `this.setTitle(...)`.
2. **`createExcel()`:** Public method that calls a report-specific builder method, then writes the workbook to a `FileOutputStream` and returns the file path.
3. **Report builder method** (e.g., `createBatteryReport()`, `createBroadcastMsgReport()`, etc.): Initializes a `Databean_report` or `Databean_dyn_reports`, sets op-code and filter parameters, calls `init()`, retrieves data from ArrayLists, creates an Excel sheet with headers and rows using Apache POI.
4. **Optional:** `getFileName()`, `getBody()`, `createBody()`, `createEmail()`, `init()`, `init2()`.

### Key risk areas common to all files:
- **No null checks on ArrayList data:** Unchecked casts `(String)arrayList.get(i)` throughout.
- **No try-catch around file I/O in `createExcel()`:** FileOutputStream is not in a try-with-resources or finally block -- resource leak on exception.
- **No validation of constructor parameters or `params[]` array:** ArrayIndexOutOfBoundsException possible.
- **Raw type ArrayLists everywhere:** No generics, relying on unchecked casts.
- **Hardcoded magic strings** for op-codes, style keys, and report titles.
- **Unused DAO instantiations:** `UnitDAO unitDAO = new UnitDAO()` created but never used in many files.

---

## Reading Evidence

### 1. EmailBatteryReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBatteryReport.java`
**Lines:** 152
**Class:** `EmailBatteryReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailBatteryReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 22 |
| Constructor (8-arg) | `public EmailBatteryReport(String cust, String loc, String dep, String st, String et, String params[], String dir, String formName) throws Exception` | 27 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 33 |
| createBatteryReport | `public void createBatteryReport() throws SQLException` | 44 |
| getFileName | `public String getFileName()` | 149 |

**Notes:**
- Uses `Databean_dyn_reports` with op_code `"rpt_battery"`.
- Duplicate import: `import java.util.ArrayList;` appears twice (line 6, 7).
- `CustomerDAO` instantiated at line 70 and used at line 80 for `getModelName()`.
- `params[1]` accessed with length check (`params.length>1`) -- correct.
- No error handling around data retrieval or Excel generation.

### 2. EmailBroadcastMsgReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBroadcastMsgReport.java`
**Lines:** 149
**Class:** `EmailBroadcastMsgReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailBroadcastMsgReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 19 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 24 |
| createBroadcastMsgReport | `public void createBroadcastMsgReport()` | 35 |

**Notes:**
- Only single constructor (no 8-arg variant).
- Uses `Databean_report` with op_code `"rpt_broadcast"`.
- Uses `BroadcastmsgBean` typed ArrayList. `UnitDAO unitDAO` instantiated at line 68 but never used.

### 3. EmailCimplicityShockReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityShockReport.java`
**Lines:** 167
**Class:** `EmailCimplicityShockReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailCimplicityShockReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 20 |
| Constructor (8-arg) | `public EmailCimplicityShockReport(String cust, String loc, String dep, String st, String et, String params[], String dir, String formName) throws Exception` | 25 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 30 |
| createCimplicityShockReport | `public void createCimplicityShockReport()` | 42 |

**Notes:**
- Complex index arithmetic for "best/worst" driver/vehicle display (lines 115-163).
- Potential `IndexOutOfBoundsException` if `usize` or `vsize` between 6-10 at lines 133-138 and 153-158.
- `UnitDAO unitDAO` instantiated but unused (line 80).
- Duplicate ArrayList import.

### 4. EmailCimplicityUtilReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityUtilReport.java`
**Lines:** 166
**Class:** `EmailCimplicityUtilReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailCimplicityUtilReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 20 |
| Constructor (8-arg) | `public EmailCimplicityUtilReport(String cust, String loc, String dep, String st, String et, String params[], String dir, String formName) throws Exception` | 25 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 31 |
| createCimplicityUtilisationReport | `public void createCimplicityUtilisationReport()` | 43 |

**Notes:**
- Follows same pattern as #3. `UnitDAO unitDAO` unused (line 91).
- Loop at line 136 iterates but only keeps last value of `temp` -- potential logic bug: all field values overwritten, only last displayed.
- Uses `setCellFormula("VALUE(\""+temp+"\")")` alongside `setCellValue(temp)` -- formula and value conflict.

### 5. EmailCurrDrivReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrDrivReport.java`
**Lines:** 143
**Class:** `EmailCurrDrivReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailCurrDrivReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 20 |
| Constructor (8-arg) | `public EmailCurrDrivReport(String cust, String loc, String dep, String st, String et, String params[], String dir, String formName) throws Exception` | 25 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 30 |
| createCurrDrivReport | `public void createCurrDrivReport()` | 41 |

**Notes:**
- Standard pattern. Uses `Databean_dyn_reports` with `"curr_driv_report"`. `UnitDAO unitDAO` unused.

### 6. EmailCurrUnitReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrUnitReport.java`
**Lines:** 149
**Class:** `EmailCurrUnitReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailCurrUnitReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 20 |
| Constructor (8-arg) | `public EmailCurrUnitReport(String cust, String loc, String dep, String st, String et, String params[], String dir, String formName) throws Exception` | 25 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 31 |
| createCurrUnitReport | `public void createCurrUnitReport()` | 42 |

**Notes:**
- Conditional column "Dept." added when `deptName.equalsIgnoreCase("all")` (line 100).
- `UnitDAO unitDAO` unused.

### 7. EmailDailyVehSummaryReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDailyVehSummaryReport.java`
**Lines:** 331
**Class:** `EmailDailyVehSummaryReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailDailyVehSummaryReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 19 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 24 |
| createDSumReport | `public void createDSumReport()` | 35 |

**Notes:**
- Most complex among the basic pattern files at 331 lines.
- Branching on `isVeh` (vehicle vs driver summary) and `cust_type` (leader/cimp/combine).
- References `RuntimeConf.cust_leader`, `RuntimeConf.cust_combine`, `RuntimeConf.cust_cimp`.
- **Bug risk (lines 294-327):** Total row always outputs all columns including leader columns regardless of `cust_type` -- may produce misaligned totals for non-leader customers.
- `UnitDAO unitDAO` unused.

### 8. EmailDriverAccessAbuseReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverAccessAbuseReport.java`
**Lines:** 355
**Class:** `EmailDriverAccessAbuseReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailDriverAccessAbuseReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 39 |
| Constructor (args-based) | `public EmailDriverAccessAbuseReport(String[] args, String dir) throws Exception` | 45 |
| init | `public void init()` | 49 |
| init2 | `public void init2()` | 97 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 142 |
| createEmail | `public String createEmail() throws IOException, SQLException` | 154 |
| createAbuseReport | `public void createAbuseReport()` | 165 |
| createBody | `public String createBody()` | 283 |
| getFileName | `public String getFileName()` | 348 |
| getBody | `public String getBody()` | 352 |

**Notes:**
- **DEVIATION:** This class has both `createExcel()` and `createEmail()` methods, plus `createBody()` for HTML email content.
- Has `init()` and `init2()` -- two different initialization paths. `init2()` uses `getParam()` method (from parent), `init()` reads from `params[]` array.
- `createExcel()` calls `init2()` then `createAbuseReport()`, but `createEmail()` calls `createBody()` then `createAbuseReport()` -- **`createEmail()` does NOT call `init()` or `init2()`, relying on pre-initialized state** which could lead to NPE if called without prior init.
- `createBody()` builds raw HTML with **XSS-vulnerable string concatenation** (user data directly in `<td>` tags, lines 309-340).
- Instance field `Databean_report dbreport` at line 21 is shadowed by local var in `init()` at line 59 and `init2()` at line 104.

### 9. EmailDriverImpactReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverImpactReport.java`
**Lines:** 179
**Class:** `EmailDriverImpactReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailDriverImpactReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 21 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 26 |
| createDrivImpReport | `public void createDrivImpReport() throws SQLException` | 37 |

**Notes:**
- Uses `CustomerDAO` at line 101 for `getModelName()`.
- `FormulaEvaluator evaluator` created at line 129 but never used.
- Duplicate ArrayList import.

### 10. EmailDriverLicenceExpiry.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverLicenceExpiry.java`
**Lines:** 116
**Class:** `EmailDriverLicenceExpiry extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailDriverLicenceExpiry(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 19 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 24 |
| createLicenceExpiryReport | `public void createLicenceExpiryReport()` | 33 |

**Notes:**
- Typo in title: `"Driver LIcence Expiry Report"` (capital I in "LIcence") -- lines 21, 68, 72.
- `UnitDAO unitDAO` unused (line 73).
- Simplest of the classes (only 2 data columns).

### 11. EmailDynDriverReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynDriverReport.java`
**Lines:** 314
**Class:** `EmailDynDriverReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailDynDriverReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 22 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 27 |
| createDynDriverReport | `public void createDynDriverReport()` | 38 |

**Notes:**
- Complex nested loops (4 levels deep). Uses `StringTokenizer` for `do_list` field hiding.
- `UnitDAO unitDAO` unused (line 134).
- Deeply nested ArrayList casts without null/size checks.

### 12. EmailDynSeenReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynSeenReport.java`
**Lines:** 243
**Class:** `EmailDynSeenReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailDynSeenReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 22 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 27 |
| createDynUnitReport | `public void createDynUnitReport()` | 38 |

**Notes:**
- Method named `createDynUnitReport` despite class being "Seen" report -- possible copy-paste naming inconsistency.
- Uses op_code `"seen_iris_pedestrian"` -- Pedestrian Detection Report.
- `vfld_hide` ArrayList allocated (line 94) but never used (uses `fld_hide[]` array instead).
- `UnitDAO unitDAO` unused.

### 13. EmailDynUnitReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynUnitReport.java`
**Lines:** 352
**Class:** `EmailDynUnitReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailDynUnitReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 22 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 27 |
| createDynUnitReport | `public void createDynUnitReport()` | 38 |

**Notes:**
- Most complex of the "Dyn" reports at 352 lines with 5 levels of nested loops.
- Handles `excluded_veh_cd` list for VOR-filtered vehicles (line 97, 246, 296, 307).
- `vfld_hide` ArrayList allocated but never used.
- `UnitDAO unitDAO` unused.

### 14. EmailHireDehireReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailHireDehireReport.java`
**Lines:** 134
**Class:** `EmailHireDehireReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailHireDehireReport(String docRoot, String fileName, HireDehireReportBean hireDehireBean) throws Exception` | 18 |
| createExcel | `public String createExcel(String st, String et, String sc) throws Exception` | 23 |
| createHireDehireReport | `public void createHireDehireReport(String st, String et, String search_crit)` | 41 |
| getFileName | `public String getFileName()` | 130 |

**Notes:**
- **DEVIATION:** Different constructor signature (docRoot, fileName, bean) -- uses `super(docRoot, fileName)`.
- `createExcel()` takes parameters (st, et, sc) -- deviates from standard pattern.
- Creates output directory if not existing (line 30-31) -- only file to do this.
- Uses `HireDehireReportBean` instead of Databean.

### 15. EmailImpactMeterReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactMeterReport.java`
**Lines:** 229
**Class:** `EmailImpactMeterReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (no-arg) | `public EmailImpactMeterReport() throws Exception` | 21 |
| Constructor (7-arg) | `public EmailImpactMeterReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 26 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 31 |
| createImpactReport | `public void createImpactReport() throws SQLException, IOException` | 42 |

**Notes:**
- Has a no-arg constructor (line 21) -- unusual among these classes.
- **Hardcoded URL at line 204:** `"http://fleetfocus.lindemh.com.au/fms/"+ RuntimeConf.impactDir+"/"+img_link.get(j)` -- HTTP, not HTTPS.
- Complex photo handling with image embedding (`addImage2`).
- Includes "Impact Data" column not present in EmailImpactReport -- differentiator.
- Uses `DataUtil.convertToImpPerc()` for percentage display.

### 16. EmailImpactReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactReport.java`
**Lines:** 222
**Class:** `EmailImpactReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (no-arg) | `public EmailImpactReport() throws Exception` | 21 |
| Constructor (7-arg) | `public EmailImpactReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 26 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 31 |
| createImpactReport | `public void createImpactReport() throws SQLException, IOException` | 42 |

**Notes:**
- Very similar to EmailImpactMeterReport but without "Impact Data" column.
- Same **hardcoded HTTP URL** at line 197.
- Same no-arg constructor.
- Double semicolons at line 77: `dbreport.setReport_filter(rpt_filter);;` -- harmless but sloppy.

### 17. EmailKeyHourUtilReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailKeyHourUtilReport.java`
**Lines:** 345
**Class:** `EmailKeyHourUtilReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (no-arg) | `public EmailKeyHourUtilReport() throws Exception` | 17 |
| Constructor (7-arg) | `public EmailKeyHourUtilReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 22 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 27 |
| createUtilReport (private) | `private void createUtilReport() throws SQLException, IOException` | 38 |

**Notes:**
- **Bug at lines 112-114:** Subtitle labels are wrong -- `{"Customer", locName}`, `{"Site", deptName}`, `{"Dept", custName}` -- Customer/Site/Dept values are swapped!
- `createUtilReport` is `private` -- only file with private report builder method.
- Modifies inherited `from` and `to` fields (substring truncation, lines 99-106) -- side effect.
- "Un Utilised Units" section follows utilized units section.
- `FormulaEvaluator evaluator` created but unused (line 40).

### 18. EmailPreOpChkFailReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkFailReport.java`
**Lines:** 225
**Class:** `EmailPreOpChkFailReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailPreOpChkFailReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 21 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 26 |
| createPreOpFailReport | `public void createPreOpFailReport()` | 37 |

**Notes:**
- **Direct `params[1]` access at line 38 without length check** -- will throw `ArrayIndexOutOfBoundsException` if params has only 1 element.
- Uses `FormulaEvaluator evaluator` -- unused (line 117).
- Imports `java.util.Vector` but does not use it.
- Correctly includes Comment column with wider width (line 84).

### 19. EmailPreOpChkReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkReport.java`
**Lines:** 232
**Class:** `EmailPreOpChkReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailPreOpChkReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 19 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 24 |
| createPreOpReport | `public void createPreOpReport()` | 35 |

**Notes:**
- More sophisticated parameter parsing: handles both 4-param and 2-param URLs (lines 40-56).
- **Direct `params[1]` access at line 55 in else branch** without null check (only checks for `params.length == 4` first).
- Imports `java.util.Vector` but does not use it.
- Very similar to EmailPreOpChkFailReport but shows ALL checks (not just failures).

### 20. EmailRestictedAccessUsageReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailRestictedAccessUsageReport.java`
**Lines:** 189
**Class:** `EmailRestictedAccessUsageReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailRestictedAccessUsageReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 23 |
| Constructor (args-based) | `public EmailRestictedAccessUsageReport(String[] args, String dir) throws Exception` | 29 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 35 |
| createRestrictedAccessReport | `public void createRestrictedAccessReport() throws SQLException` | 47 |
| getFileName | `public String getFileName()` | 186 |

**Notes:**
- **Typo in class name:** "Resticted" instead of "Restricted" -- throughout file name and class declaration.
- Uses `RestrictedAccessUsageBean` typed ArrayList.
- Has `CustomerDAO customerDAO` (line 111) instantiated but never used.
- Imports `java.io.File` but does not use it.

### 21. EmailSeatHourUtilReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java`
**Lines:** 345
**Class:** `EmailSeatHourUtilReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (no-arg) | `public EmailSeatHourUtilReport() throws Exception` | 19 |
| Constructor (7-arg) | `public EmailSeatHourUtilReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 24 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 29 |
| createUtilReport (private) | `private void createUtilReport() throws SQLException, IOException` | 40 |

**Notes:**
- **CRITICAL BUG (lines 104-106):** Same as EmailKeyHourUtilReport -- Customer/Site/Dept subtitle values are swapped: `{"Customer", locName}`, `{"Site", deptName}`, `{"Dept", custName}`.
- **CRITICAL BUG (lines 159-196):** All `setCellValue()` calls use `vutil1.get(i)` instead of the corresponding `vutil2` through `vutil8` -- **every time slot column displays the 12-03 AM value**. The formula uses the correct value but the displayed cell value is wrong.
- Same bug repeated in the "Un Utilised Units" section (lines 291-330).
- `FormulaEvaluator evaluator` created but unused.
- `createUtilReport` is `private`.

### 22. EmailServMaintenanceReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReport.java`
**Lines:** 438
**Class:** `EmailServMaintenanceReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailServMaintenanceReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 47 |
| Constructor (args-based) | `public EmailServMaintenanceReport(String[] args, String dir) throws Exception` | 52 |
| init | `public void init()` | 56 |
| init2 | `public void init2()` | 103 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 146 |
| createEmail | `public String createEmail() throws IOException, SQLException` | 158 |
| createServMaintenanceReport | `public void createServMaintenanceReport()` | 169 |
| createBody | `public String createBody()` | 347 |
| getFileName | `public String getFileName()` | 431 |
| getBody | `public String getBody()` | 435 |

**Notes:**
- **DEVIATION:** Like EmailDriverAccessAbuseReport, has `createEmail()`, `createBody()`, `init()`/`init2()`.
- Uses `ServiceDueFlagBean` alongside `Databean_report` for dual data source.
- `createBody()` builds HTML with XSS-vulnerable string concatenation.
- `Double.parseDouble()` at lines 250, 390 could throw `NumberFormatException` -- no error handling.
- `init()` uses op_code `"serv_hour"`, `init2()` uses `"serv_hour_new"` -- different ops.
- `init2()` does NOT set `vsNo` field -- potential NPE when `createServMaintenanceReport()` accesses it (line 222). Note: `init()` does set it (line 93).
- Color-coded "Hours to Next Service" column with red/green/orange styles.

### 23. EmailServMaintenanceReportNew.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReportNew.java`
**Lines:** 256
**Class:** `EmailServMaintenanceReportNew extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailServMaintenanceReportNew(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 21 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 26 |
| createServMaintenanceReport | `public void createServMaintenanceReport()` | 37 |

**Notes:**
- Simpler version of EmailServMaintenanceReport -- no `createEmail()`/`createBody()`.
- Uses `"serv_hour"` (not `"serv_hour_new"`).
- Same `Double.parseDouble()` risk at line 159.
- `UnitDAO unitDAO` unused.

### 24. EmailSuperMasterAuthReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSuperMasterAuthReport.java`
**Lines:** 211
**Class:** `EmailSuperMasterAuthReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor (7-arg) | `public EmailSuperMasterAuthReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 24 |
| Constructor (args-based) | `public EmailSuperMasterAuthReport(String[] args, String dir) throws Exception` | 30 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 35 |
| createSuperMasterAuthReport | `public void createSuperMasterAuthReport() throws SQLException` | 51 |
| getFileName | `public String getFileName()` | 207 |

**Notes:**
- Uses `SuperMasterAuthBean` and `SuperMasterAuthReportBean`.
- Has deduplication logic for fleet number grouping (lines 155-198).
- `CustomerDAO customerDAO` instantiated (line 117) but never used.
- Variables `get_user`, `get_loc`, `get_dep`, `get_mod`, `form_nm` retrieved (lines 101-105) but mostly unused.

### 25. EmailUnitUnlockReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUnitUnlockReport.java`
**Lines:** 191
**Class:** `EmailUnitUnlockReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailUnitUnlockReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 16 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 21 |
| createBroadcastMsgReport | `public void createBroadcastMsgReport()` | 32 |

**Notes:**
- **Misleading method name:** `createBroadcastMsgReport()` in an unlock report class -- clearly copy-pasted from EmailBroadcastMsgReport.
- Complex lockout type filter handling (lines 82-105).
- Logic bug at line 103: `if` without `else` after previous `else if` -- `rptFilter "both"` check is a standalone `if`, not chained.

### 26. EmailUtilWowReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilWowReport.java`
**Lines:** 133
**Class:** `EmailUtilWowReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailUtilWowReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 20 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 25 |
| createCurrReport | `public void createCurrReport() throws IOException` | 36 |

**Notes:**
- Unique: calls `dbreport.init()` TWICE with different op_codes (`"util_wow_dtl"` then `"email_util_wow"`).
- Embeds a chart image via `addImageUtilisationChart()` -- no tabular data rows.
- Variables `utilmodelbean`, `customer`, `location`, `department`, `model`, `avatruck` declared (lines 105-110) but never used.
- `UnitDAO unitDAO` unused.

### 27. EmailUtilisationReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java`
**Lines:** 256
**Class:** `EmailUtilisationReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailUtilisationReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 25 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 30 |
| createUtilReport | `public void createUtilReport()` | 41 |

**Notes:**
- Truncates `from` field: `from = from.substring(0,10)` at line 59 -- side effect on inherited field, could affect other uses.
- Uses `UnitUtilSummaryBean` typed ArrayList -- cleaner bean-based approach.
- Comprehensive utilisation metrics (key, seat, traction, hydraulic hours with percentages).
- Several variables fetched but unused: `Vgp_cd`, `Vuser_cd`, `Vloc_cd`, `vdept_cd`, etc.
- `UnitDAO unitDAO` unused.

### 28. EmailVorReport.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailVorReport.java`
**Lines:** 335
**Class:** `EmailVorReport extends Frm_excel`

| Method | Signature | Line |
|--------|-----------|------|
| Constructor | `public EmailVorReport(String cust, String loc, String dep, String st, String et, String params[], String dir) throws Exception` | 22 |
| createExcel | `public String createExcel() throws IOException, SQLException` | 27 |
| createVorReport | `public void createVorReport()` | 38 |

**Notes:**
- Structurally similar to EmailDynUnitReport but uses `vor_flag = "1"` and `"vor_report"` op_code.
- Has "Times Enabled" column and VOR count tracking.
- Same `StringTokenizer` pattern for field hiding.
- `UnitDAO unitDAO` unused. `vfld_hide` ArrayList allocated but never used.

---

## Findings

### A10-001 -- Zero Test Coverage for All 28 Email Report Classes
**Severity:** CRITICAL
**Files:** All 28 `Email*Report.java` files
**Details:** No test infrastructure exists. None of the 28 classes have any unit tests, integration tests, or even a test harness. These classes perform:
- Database queries via Databean initialization (untested SQL paths)
- Excel file generation via Apache POI (untested output correctness)
- File system writes (untested I/O error handling)
- HTML email body generation (untested in 3 classes)
- Complex business logic (date calculations, service due calculations, time formatting)

**Recommended tests:**
- Unit tests for each `create*Report()` method with mocked Databeans
- Excel output validation tests (header correctness, row count, cell values)
- Edge case tests: empty data sets, null values in ArrayLists, missing params
- Error handling tests: IOException during file write, invalid date formats

### A10-002 -- No Error Handling or Resource Management in createExcel()
**Severity:** HIGH
**Files:** All 28 files
**Details:** Every `createExcel()` method follows this pattern:
```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
```
No try-with-resources, no try-catch-finally. If `wb.write()` throws an exception, the FileOutputStream is never closed, causing a resource leak. Additionally, the `result` path could be invalid/unwritable with no graceful handling.

**Tests needed:**
- Verify FileOutputStream is properly closed on success and failure
- Verify behavior when output path is invalid
- Verify behavior when disk is full / write permission denied

### A10-003 -- Unchecked Array Casts and No Null Safety on ArrayList Data
**Severity:** HIGH
**Files:** All 28 files
**Details:** All files use raw-type `ArrayList` from Databeans and perform unchecked `(String)` casts like `(String)vunit_name.get(i)`. If the Databean returns null elements or mismatched types, `ClassCastException` or `NullPointerException` will occur at runtime with no meaningful error message.

**Tests needed:**
- Test with null elements in data arrays
- Test with empty data arrays
- Test with type-mismatched data

### A10-004 -- Critical Bug: Swapped Subtitle Labels in KeyHour and SeatHour Util Reports
**Severity:** HIGH
**Files:**
- `EmailKeyHourUtilReport.java` (lines 112-114)
- `EmailSeatHourUtilReport.java` (lines 104-106)

**Details:** The subtitle section maps labels to wrong values:
```java
{"Customer", locName},   // Should be custName
{"Site", deptName},      // Should be locName
{"Dept", custName},      // Should be deptName
```
This means the exported Excel report displays incorrect metadata -- Customer shows location name, Site shows department name, Dept shows customer name.

**Tests needed:**
- Subtitle label-to-value mapping validation

### A10-005 -- Critical Bug: SeatHourUtilReport Displays Wrong Cell Values
**Severity:** HIGH
**File:** `EmailSeatHourUtilReport.java` (lines 159-196 and 291-330)
**Details:** Every time-slot column's `setCellValue()` call uses `vutil1.get(i)` instead of the corresponding variable:
```java
contentCell.setCellFormula("VALUE(\""+vutil2.get(i).toString()+"\")");  // Formula correct
contentCell.setCellValue(vutil1.get(i).toString());                     // Value WRONG - always vutil1
```
This repeats for vutil2 through vutil8. When the formula cannot be evaluated (e.g., in non-Excel viewers), every column shows the 12-03 AM value.

**Tests needed:**
- Cell value correctness tests for each time slot column
- Formula vs display value consistency test

### A10-006 -- XSS Vulnerability in HTML Email Body Generation
**Severity:** HIGH
**Files:**
- `EmailDriverAccessAbuseReport.java` -- `createBody()` (lines 283-346)
- `EmailServMaintenanceReport.java` -- `createBody()` (lines 347-428)

**Details:** These methods build HTML email content by directly concatenating user/database data into HTML tags without escaping:
```java
body.append("<td>"+tmp+"</td>");
body.append("<td>"+fleetNameList.get(i)+"</td>");
```
If any data contains HTML special characters (`<`, `>`, `"`, `&`), the email content will be corrupted. If data is attacker-controlled, this enables HTML injection / XSS in email clients.

**Tests needed:**
- HTML escaping verification with special characters in data
- Email body structure correctness tests

### A10-007 -- Hardcoded HTTP URLs for Impact Photos
**Severity:** MEDIUM
**Files:**
- `EmailImpactMeterReport.java` (line 204)
- `EmailImpactReport.java` (line 197)

**Details:** Both files contain:
```java
String tmp = "http://fleetfocus.lindemh.com.au/fms/"+ RuntimeConf.impactDir+"/"+img_link.get(j);
```
This hardcodes a production domain and uses HTTP (not HTTPS). The domain is directly embedded in report output files.

**Tests needed:**
- URL construction validation
- Protocol/domain configuration verification

### A10-008 -- Misleading Method Names from Copy-Paste
**Severity:** MEDIUM
**Files:**
- `EmailUnitUnlockReport.java` -- method `createBroadcastMsgReport()` at line 32
- `EmailDynSeenReport.java` -- method `createDynUnitReport()` at line 38

**Details:** Method names do not match the class purpose. `EmailUnitUnlockReport` has a method named `createBroadcastMsgReport()` (clearly copied from `EmailBroadcastMsgReport`). `EmailDynSeenReport` has `createDynUnitReport()` instead of `createDynSeenReport()`.

**Tests needed:**
- Method behavior should match expected report output regardless of name

### A10-009 -- Potential ArrayIndexOutOfBoundsException on params Array
**Severity:** MEDIUM
**Files:**
- `EmailPreOpChkFailReport.java` (line 38): `String form_cd = params[1];` -- no length check
- `EmailPreOpChkReport.java` (line 55): `form_cd = params[1]` in else branch -- assumes length >= 2

**Details:** If `params` array has fewer elements than expected, these direct accesses will throw `ArrayIndexOutOfBoundsException`. Most other files properly check `params.length > N` before accessing `params[N]`.

**Tests needed:**
- Constructor/method calls with minimal params arrays
- Boundary testing on params length

### A10-010 -- NumberFormatException Risk in Service Reports
**Severity:** MEDIUM
**Files:**
- `EmailServMaintenanceReport.java` (lines 250, 390)
- `EmailServMaintenanceReportNew.java` (line 159)

**Details:** `Double.parseDouble(nsDue)` and `Double.parseDouble((String)currMeterReadingList.get(i))` are called without try-catch. If either value is non-numeric (e.g., "-", empty string, or a text value), a `NumberFormatException` will crash the entire report generation.

**Tests needed:**
- Service report generation with non-numeric meter readings
- Service report generation with "-" placeholder values

### A10-011 -- Duplicate and Unused Imports/Variables Throughout
**Severity:** LOW
**Files:** Majority of the 28 files
**Details:**
- Duplicate `import java.util.ArrayList;` in 11+ files
- `UnitDAO unitDAO = new UnitDAO()` instantiated but never used in ~18 files (unnecessary object creation, potential DB connection overhead)
- `FormulaEvaluator evaluator` created but unused in 4+ files
- `CustomerDAO customerDAO` created but unused in 3+ files
- Multiple unused variables in EmailUtilWowReport (lines 105-110), EmailUtilisationReport, EmailSuperMasterAuthReport

**Tests needed:**
- Static analysis / lint would catch these; no runtime test needed

### A10-012 -- EmailDriverAccessAbuseReport.createEmail() Missing Initialization Guard
**Severity:** MEDIUM
**File:** `EmailDriverAccessAbuseReport.java` (line 154)
**Details:** `createEmail()` calls `createBody()` then `createAbuseReport()` but does NOT call `init()` or `init2()`. The data fields (`a_driv_cd`, `a_driv_nm`, etc.) are instance-level ArrayLists that default to null. If `createEmail()` is called without a prior `init()`/`init2()` call, `NullPointerException` will occur in both `createBody()` and `createAbuseReport()`.

In contrast, `createExcel()` correctly calls `init2()` first (line 144).

**Tests needed:**
- Call `createEmail()` without prior initialization -- verify graceful failure
- Call `createEmail()` after `init()` vs `init2()` -- verify correct behavior for both paths

### A10-013 -- EmailServMaintenanceReport.init2() Missing vsNo Assignment
**Severity:** MEDIUM
**File:** `EmailServMaintenanceReport.java` (lines 103-144)
**Details:** `init()` sets `vsNo = servBean.getVs_no()` at line 93, but `init2()` does not. If `createExcel()` (which calls `init2()` then `createServMaintenanceReport()`) is used, the `vsNo` field will be null, causing NPE at line 222 in the report generation loop where `vsNo.get(i)` is accessed.

**Tests needed:**
- Report generation via `createExcel()` path -- should populate Serial No column
- Compare init() vs init2() field population

### A10-014 -- EmailDailyVehSummaryReport Total Row Misalignment
**Severity:** MEDIUM
**File:** `EmailDailyVehSummaryReport.java` (lines 294-327)
**Details:** The total row always outputs all columns (including leader-specific and cimp-specific columns) regardless of the `cust_type` check that was used when building data rows (lines 139-151, 204-284). This means for non-leader customers, the total row will have more cells than data rows, creating misaligned columns in the Excel output.

**Tests needed:**
- Total row alignment for each customer type (leader, cimp, combine, default)
- Column count consistency between header, data rows, and total row

### A10-015 -- Typos in Report Titles and Class Names
**Severity:** LOW
**Files:**
- `EmailDriverLicenceExpiry.java`: Title is `"Driver LIcence Expiry Report"` (capital I in LIcence)
- `EmailRestictedAccessUsageReport.java`: Class name misspells "Restricted" as "Resticted"

**Details:** These typos appear in user-facing report titles and affect file naming/class discovery. The licence expiry typo appears in lines 21, 68, and 72.

**Tests needed:**
- Report title string validation

### A10-016 -- Side Effects on Inherited Fields
**Severity:** LOW
**Files:**
- `EmailUtilisationReport.java` (lines 59-60): `from = from.substring(0,10)` and `to = to.substring(0,10)` -- truncates inherited fields
- `EmailKeyHourUtilReport.java` (lines 99-106): Same pattern
- Multiple files modify `cust_cd`, `loc_cd`, `dept_cd` (e.g., setting to `""` or `"all"`)

**Details:** These modifications to inherited fields could cause issues if the object is reused or if parent class methods depend on the original values. The substring truncation at line 59 could also throw `StringIndexOutOfBoundsException` if `from` is shorter than 10 characters.

**Tests needed:**
- Report generation with `from`/`to` strings shorter than 10 characters
- Object reuse after first report generation

### A10-017 -- Massive Code Duplication Across 28 Files
**Severity:** MEDIUM (maintainability/testability impact)
**Files:** All 28 files
**Details:** The common pattern (constructor delegation, cust/loc/dept normalization, createExcel with FileOutputStream, subtitle generation, header/data loop) is duplicated across all 28 files with no shared template method or base report class. This makes it nearly impossible to fix cross-cutting issues (like the FileOutputStream resource leak) in one place. A Template Method pattern in the parent `Frm_excel` class would dramatically reduce duplication and improve testability.

**Tests needed:**
- If refactored: single test for the template, per-report tests only for unique logic
- Current state: each of the 28 files requires independent testing of the same boilerplate
