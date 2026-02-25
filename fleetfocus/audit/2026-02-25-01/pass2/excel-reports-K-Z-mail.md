# Pass 2 — Test Coverage: excel/reports (Excel servlets K-Z + Mail)
**Agent:** A12
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|---|---|
| Test framework (JUnit/TestNG) | **Not present** -- zero JUnit or TestNG dependencies detected in project |
| Test source directories (`test/`, `src/test/`) | **Not present** -- no test source roots exist |
| Test files for audited classes | **Zero** -- 0 out of 16 files have any associated tests |
| Build-tool test configuration | No Maven/Gradle test lifecycle configuration found |
| CI test execution | No evidence of automated test runs |

`EncryptTest.java` exists in the codebase but is a decompiled utility class, not a test.

**Overall test coverage for all 16 audited files: 0%**

---

## Reading Evidence

All files reside under `WEB-INF/src/com/torrent/surat/fms6/excel/reports/`.

### 1. ExcelKeyHourUtilReport.java (357 lines)
- **Class:** `ExcelKeyHourUtilReport extends Frm_excel`
- **Public methods:**
  - `ExcelKeyHourUtilReport(String docRoot, String fileName, KeyHourUtilBean utilBean)` -- constructor, line 51
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 56
  - `String getFileName()` -- line 354
- **Private methods:**
  - `void createUtilReport(String cust, String loc, String dep, String st, String et, Sheet sheet)` -- line 103
- **Key concerns:** Uses raw `ArrayList` (no generics), creates `UnitDAO` at line 106 (unused), FileOutputStream not in try-with-resources, no input validation.

### 2. ExcelOperationalStatusReport.java (159 lines)
- **Class:** `ExcelOperationalStatusReport extends Frm_excel`
- **Public methods:**
  - `ExcelOperationalStatusReport(String docRoot, String fileName, BaseResultBean resultBean)` -- constructor, line 21
  - `String createExcel(String custName, String siteName, String deptName)` -- line 26
  - `void createOperationStatusReport(String custName, String siteName, String deptName)` -- line 44
  - `String getFileName()` -- line 156
- **Key concerns:** Unchecked cast of `resultBean` to `OperationalStatusReportResultBean` at line 23, URLDecoder usage silently swallows exceptions at line 73-74, FileOutputStream not in try-with-resources.

### 3. ExcelPreOpCheckFailReport.java (383 lines)
- **Class:** `ExcelPreOpCheckFailReport extends Frm_excel`
- **Public methods:**
  - `ExcelPreOpCheckFailReport(String docRoot, String fileName, PreOpCheckFailReportBean preOpBean)` -- constructor, line 21
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 26
  - `String createExcel(String cust, String loc, String dep, String st, String et, String form)` -- line 45 (overloaded)
  - `void createPreOpFailReport(String cust, String loc, String dep, String st, String et)` -- line 64
  - `void createPreOpFailReport(String cust, String loc, String dep, String st, String et, String form)` -- line 223 (overloaded)
  - `String getFileName()` -- line 380
- **Key concerns:** Two heavily duplicated `createPreOpFailReport` methods (~150 lines each nearly identical), creates unused `UnitDAO` at lines 86 and 245, raw `ArrayList` casts, FormulaEvaluator created but unused at line 116.

### 4. ExcelPreOpCheckReport.java (203 lines)
- **Class:** `ExcelPreOpCheckReport extends Frm_excel`
- **Public methods:**
  - `ExcelPreOpCheckReport(String docRoot, String fileName, PreOpCheckReportBean preOpBean)` -- constructor, line 22
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 27
  - `void createPreOpReport(String cust, String loc, String dep, String st, String et)` -- line 46
  - `String getFileName()` -- line 200
- **Key concerns:** Creates unused `UnitDAO` at line 68, raw `ArrayList` casts, FileOutputStream not in try-with-resources.

### 5. ExcelRestrictedUsageReport.java (272 lines)
- **Class:** `ExcelRestrictedUsageReport extends Frm_excel`
- **Public methods:**
  - `ExcelRestrictedUsageReport(String docRoot, String fileName, Map<String,ArrayList<RestrictedAccessUsageBean>> map, String grand_total_charge)` -- constructor, line 24
  - `String createExcel(String cust, String loc, String dep, String st, String et, String model)` -- line 31
  - `void createRestrictedAccessReport(String cust, String loc, String dep, String st, String et, String model)` -- line 50
  - `String getFileName()` -- line 269
- **Key concerns:** Instantiates `CustomerDAO` at line 59 to resolve names (live DB dependency in report generator), empty `if` block at line 110 (dead branch), FileOutputStream not in try-with-resources.

### 6. ExcelSeatHourUtilReport.java (357 lines)
- **Class:** `ExcelSeatHourUtilReport extends Frm_excel`
- **Public methods:**
  - `ExcelSeatHourUtilReport(String docRoot, String fileName, SeatHourUtilBean utilBean)` -- constructor, line 49
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 54
  - `String getFileName()` -- line 354
- **Private methods:**
  - `void createUtilReport(String cust, String loc, String dep, String st, String et, Sheet sheet)` -- line 102
- **Key concerns:** Nearly identical structure to `ExcelKeyHourUtilReport` (massive code duplication), unused `UnitDAO` at line 105, raw `ArrayList`, duplicate `import java.util.ArrayList` at line 8, FormulaEvaluator created but unused at line 136.

### 7. ExcelServMaintenanceReport.java (272 lines)
- **Class:** `ExcelServMaintenanceReport extends Frm_excel`
- **Public methods:**
  - `ExcelServMaintenanceReport(String docRoot, String fileName, ServMaintenanceReportBean bean)` -- constructor, line 21
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 26
  - `void createServMaintenanceReport(String cust, String loc, String dep, String st, String et)` -- line 45
  - `String getFileName()` -- line 269
- **Key concerns:** `Double.parseDouble()` at line 153 can throw `NumberFormatException` (uncaught), `DateUtil.compareDates` at line 165 can throw parse exceptions, color status logic at lines 185-193 uses string-contains on hex color codes, duplicate `import java.util.ArrayList` at line 7.

### 8. ExcelSpareModuleReport.java (155 lines)
- **Class:** `ExcelSpareModuleReport extends Frm_excel`
- **Public methods:**
  - `ExcelSpareModuleReport(String docRoot, String fileName, ArrayList<SpareModuleBean> arrSpareModuleBean)` -- constructor, line 19
  - `String createExcel()` -- line 24 (note: no parameters, unlike other report classes)
  - `void createSpareModuleReport()` -- line 43
  - `String getFileName()` -- line 150
- **Key concerns:** Different `createExcel()` signature (no filter params), FileOutputStream not in try-with-resources.

### 9. ExcelSuperMasterAuthReport.java (151 lines)
- **Class:** `ExcelSuperMasterAuthReport extends Frm_excel`
- **Public methods:**
  - `ExcelSuperMasterAuthReport(String docRoot, String fileName, SuperMasterAuthReportBean sBean)` -- constructor, line 24
  - `String createExcel(String cust, String loc, String dep, String st, String et, String model)` -- line 30
  - `void createSuperMasterAuthReport(String cust, String loc, String dep, String st, String et, String model)` -- line 49
  - `String getFileName()` -- line 148
- **Key concerns:** Instantiates `CustomerDAO` at line 59 (live DB call during report generation), empty cells created without value at lines 125-126, FileOutputStream not in try-with-resources.

### 10. ExcelUnitUnlockReport.java (148 lines)
- **Class:** `ExcelUnitUnlockReport extends Frm_excel`
- **Public methods:**
  - `ExcelUnitUnlockReport(String docRoot, String fileName, UnitUnlockReportBean bean)` -- constructor, line 19
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 24
  - `void createUnitUnlockReport(String cust, String loc, String dep, String st, String et)` -- line 43
  - `String getFileName()` -- line 145
- **Key concerns:** Creates unused `UnitDAO` at line 61, raw `ArrayList` casts, inconsistent indentation (lines 47-53).

### 11. ExcelUtilWOWReport.java (173 lines)
- **Class:** `ExcelUtilWOWReport extends Frm_excel`
- **Public methods:**
  - `ExcelUtilWOWReport(String docRoot, String fileName, UtilWowReportBean utilBean)` -- constructor, line 22
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 27
  - `void createUtilWowReport(String cust, String loc, String dep, String from, String to)` -- line 46
  - `String getFileName()` -- line 169
- **Key concerns:** Unused local variables `get_user`, `get_loc`, `get_dep`, `form_nm`, `chartUrl` at lines 47-52, creates unused `UnitDAO` at line 68, triple-nested loop (lines 104-165) generates potentially massive spreadsheets with no size guard.

### 12. ExcelUtilWOWReportEmail.java (180 lines)
- **Class:** `ExcelUtilWOWReportEmail extends Frm_excel`
- **Public methods:**
  - `ExcelUtilWOWReportEmail(String docRoot, String fileName, UtilWowReportBean utilBean)` -- constructor, line 23
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 28
  - `void createUtilWowReport(String cust, String loc, String dep, String from, String to)` -- line 47
  - `String getFileName()` -- line 176
- **Key concerns:** Near-complete code duplication of `ExcelUtilWOWReport` with added `LindeConfig.siteName` branch at line 94 (AU site gets chart image instead of data), unused local variables at lines 48-53, unused `UnitDAO` at line 69, static config access `LindeConfig.siteName` without null check.

### 13. ExcelUtilisationReport.java (229 lines)
- **Class:** `ExcelUtilisationReport extends Frm_excel`
- **Public methods:**
  - `ExcelUtilisationReport(String docRoot, String fileName, UtilisationReportBean utilBean)` -- constructor, line 20
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 25
  - `void createUtilReport(String custName, String locName, String deptName, String from, String to)` -- line 43
  - `String getFileName()` -- line 226
- **Key concerns:** Creates unused `UnitDAO` at line 80, many unused local variables (lines 45-59: `Vgp_cd`, `Vgp_nm`, `Vuser_cd`, etc.), line 163 bug -- sets traction hours cell value with `getKey_hours()` instead of `getTrack_hours()`, FileOutputStream not in try-with-resources.

### 14. ExcelVorReport.java (313 lines)
- **Class:** `ExcelVorReport extends Frm_excel`
- **Public methods:**
  - `ExcelVorReport(String docRoot, String fileName, DynUnitReportBean dynBean)` -- constructor, line 20
  - `String createExcel(String cust, String loc, String dep, String st, String et)` -- line 25
  - `void createVorReport(String cust, String loc, String dep, String st, String et)` -- line 44
  - `String getFileName()` -- line 310
- **Key concerns:** Most complex report -- quadruple-nested loops (lines 122-307), creates unused `UnitDAO` at line 105, raw `ArrayList` casts throughout, `StringTokenizer` at line 78 (legacy API), FileOutputStream not in try-with-resources.

### 15. MailBase.java (128 lines)
- **Class:** `MailBase` (standalone, no extends)
- **Public methods:**
  - `String setMailHeader(String st, String et, String cust, String loc, String dep, String rptName)` -- line 5
  - `String setMailHeader(String st, String et, String cust, String loc, String dep, String model, String rptName)` -- line 64 (overloaded, 7 params)
- **Key concerns:** Hardcoded external URLs to `fleetfocus.lindemh.com.au` at lines 10, 15-16, 24, 69, 74-75, 83 (HTTP not HTTPS -- potential mixed-content/security issue), HTML built via string concatenation (potential XSS if parameters contain user input), no HTML encoding/escaping of any parameters, heavy code duplication between the two overloads.

### 16. MailExcelReports.java (45 lines)
- **Class:** `MailExcelReports` (standalone, no extends)
- **Public methods:**
  - `boolean sendExcelReport(String subject, String email_id, String attachment, String attachmentName)` -- line 12
  - `boolean sendExcelReport(String subject, String body, String email_id, String attachment, String attachmentName)` -- line 31 (overloaded, 5 params)
- **Key concerns:** Hardcoded `"unknown"` passed for sender name and CC at lines 19, 35 (unclear purpose), exceptions caught but only `e.printStackTrace()` at lines 21-26 and 36-41 (no logging framework, no re-throw), `System.out.println` used for logging at lines 14, 27, `LindeConfig.mail_from` accessed statically without null check.

---

## Findings

### A12-01 — Zero test coverage across all 16 Excel report and mail classes
**Severity:** CRITICAL
**Files affected:** All 16 files
**Details:** None of the 16 audited files have any associated unit tests, integration tests, or any form of automated test coverage. The project has no test framework (JUnit, TestNG, etc.) configured, no test source directories, and no test build configuration. These classes handle Excel report generation, file I/O, database access (via DAO), and email dispatch -- all business-critical operations with zero verification.
**Risk:** Regressions in report output, data correctness, file handling, or email delivery would go entirely undetected until production.

### A12-02 — FileOutputStream resource leak in all Excel report generators (13 classes)
**Severity:** HIGH
**Files affected:** ExcelKeyHourUtilReport.java (line 96-98), ExcelOperationalStatusReport.java (line 37-39), ExcelPreOpCheckFailReport.java (lines 38-40, 57-59), ExcelPreOpCheckReport.java (line 39-41), ExcelRestrictedUsageReport.java (line 43-45), ExcelSeatHourUtilReport.java (line 95-97), ExcelServMaintenanceReport.java (line 38-40), ExcelSpareModuleReport.java (line 36-38), ExcelSuperMasterAuthReport.java (line 42-44), ExcelUnitUnlockReport.java (line 36-38), ExcelUtilWOWReport.java (line 39-41), ExcelUtilWOWReportEmail.java (line 40-42), ExcelUtilisationReport.java (line 36-38), ExcelVorReport.java (line 37-39)
**Details:** All `createExcel()` methods open a `FileOutputStream` without try-with-resources or a finally block. If `wb.write(fileOut)` throws an exception, the stream is never closed, causing a file-handle leak. No tests exist to verify correct resource cleanup under error conditions.
**Risk:** Accumulated file-handle leaks under error conditions could exhaust OS file descriptors.

### A12-03 — Potential data correctness bug in ExcelUtilisationReport: traction hours displays key hours
**Severity:** HIGH
**File:** ExcelUtilisationReport.java, line 163
**Details:** Line 163 reads:
```java
contentCell.setCellValue(utilBean.getKey_hours());
```
However, the cell is in the "Traction Hours" column (the formula on line 162 correctly uses `getTrack_hours()`). The display value should be `utilBean.getTrack_hours()` instead of `utilBean.getKey_hours()`. This means the traction hours column shows key hours data.
**Risk:** Incorrect report data delivered to customers. Without tests, this bug has no automated means of detection.

### A12-04 — Unused UnitDAO instantiations creating unnecessary database connections (9 classes)
**Severity:** MEDIUM
**Files affected:** ExcelKeyHourUtilReport.java (line 106), ExcelPreOpCheckFailReport.java (lines 86, 245), ExcelPreOpCheckReport.java (line 68), ExcelSeatHourUtilReport.java (line 105), ExcelUnitUnlockReport.java (line 61), ExcelUtilWOWReport.java (line 68), ExcelUtilWOWReportEmail.java (line 69), ExcelUtilisationReport.java (line 80), ExcelVorReport.java (line 105)
**Details:** A `UnitDAO unitDAO = new UnitDAO()` is instantiated but never used in at least 9 report classes. If the DAO constructor opens or pools a database connection, these are wasted resources.
**Risk:** Unnecessary database connection overhead on every report generation. No tests verify constructor side effects.

### A12-05 — Live database calls during report rendering (ExcelRestrictedUsageReport, ExcelSuperMasterAuthReport)
**Severity:** MEDIUM
**Files affected:** ExcelRestrictedUsageReport.java (lines 59, 65-67), ExcelSuperMasterAuthReport.java (lines 59, 65-67)
**Details:** Both classes instantiate `CustomerDAO` and call `getCustomerName()`, `getLocationName()`, and `getDepartmentName()` within the report-rendering methods. This mixes data retrieval with presentation, making the classes impossible to unit-test without a live database or mocking framework.
**Risk:** These classes cannot be tested in isolation. Database failures during report rendering will produce partial/corrupt Excel files.

### A12-06 — Massive code duplication between ExcelUtilWOWReport and ExcelUtilWOWReportEmail
**Severity:** MEDIUM
**Files affected:** ExcelUtilWOWReport.java (173 lines), ExcelUtilWOWReportEmail.java (180 lines)
**Details:** `ExcelUtilWOWReportEmail` is almost line-for-line identical to `ExcelUtilWOWReport`, with the sole difference being a `LindeConfig.siteName` check at line 94 that optionally embeds a chart image for the AU site. The remaining ~150 lines of data-rendering logic are duplicated verbatim.
**Risk:** Bug fixes or feature changes must be applied in both files. Without tests, divergence between the two copies is undetectable.

### A12-07 — Massive code duplication between ExcelKeyHourUtilReport and ExcelSeatHourUtilReport
**Severity:** MEDIUM
**Files affected:** ExcelKeyHourUtilReport.java (357 lines), ExcelSeatHourUtilReport.java (357 lines)
**Details:** These two classes are structurally identical (same field declarations, same rendering logic, same loop structures) differing only in the bean type (`KeyHourUtilBean` vs `SeatHourUtilBean`) and the report title. Both are 357 lines.
**Risk:** Same as A12-06 -- parallel maintenance burden with no tests to catch divergence.

### A12-08 — Heavy code duplication within ExcelPreOpCheckFailReport (two createPreOpFailReport overloads)
**Severity:** MEDIUM
**File:** ExcelPreOpCheckFailReport.java, lines 64-221 and 223-378
**Details:** The two overloaded `createPreOpFailReport` methods (with and without `String form` parameter) contain nearly identical logic spanning ~150 lines each. The `form` parameter is accepted but has no visible effect on the rendering, suggesting dead code or an incomplete feature.
**Risk:** Defects must be fixed in both copies. The `form` parameter's purpose is unclear and untested.

### A12-09 — XSS vulnerability in MailBase HTML generation
**Severity:** HIGH
**File:** MailBase.java, lines 5-127
**Details:** Both `setMailHeader` overloads build HTML via string concatenation, directly interpolating parameters (`st`, `et`, `cust`, `loc`, `dep`, `model`, `rptName`) into HTML without any encoding or escaping. If any parameter contains user-controlled data (e.g., customer name from a form), it could inject arbitrary HTML/JavaScript into the email body.
**Risk:** Stored XSS in email clients that render HTML. No tests validate output encoding.

### A12-10 — Hardcoded HTTP URLs in MailBase (insecure asset references)
**Severity:** MEDIUM
**File:** MailBase.java, lines 10, 15-16, 24, 69, 74-75, 83
**Details:** Image and CSS references use `http://fleetfocus.lindemh.com.au/fms/...` (plain HTTP, not HTTPS). These are hardcoded to a specific domain, making the code non-portable across deployments and sending asset requests over unencrypted connections.
**Risk:** Mixed-content warnings in email clients, broken images if domain changes, potential MitM for embedded resources.

### A12-11 — Exception handling in MailExcelReports uses only printStackTrace
**Severity:** MEDIUM
**File:** MailExcelReports.java, lines 20-26, 36-41
**Details:** Both `sendExcelReport` methods catch `AddressException` and `MessagingException` but only call `e.printStackTrace()` with a `// TODO Auto-generated catch block` comment. The method returns `false` (initial default) when an exception occurs but provides no diagnostic information to the caller, no structured logging, and no stack trace capture in production logging.
**Risk:** Mail delivery failures are silently swallowed; operators have no visibility into why emails are not being delivered. Without tests, the error-path behavior is entirely unverified.

### A12-12 — Raw ArrayList usage without generics across all Excel report classes
**Severity:** LOW
**Files affected:** ExcelKeyHourUtilReport.java, ExcelPreOpCheckFailReport.java, ExcelPreOpCheckReport.java, ExcelSeatHourUtilReport.java, ExcelServMaintenanceReport.java, ExcelUnitUnlockReport.java, ExcelUtilWOWReport.java, ExcelUtilWOWReportEmail.java, ExcelUtilisationReport.java, ExcelVorReport.java
**Details:** Extensive use of raw `ArrayList` (without type parameters) throughout these classes, followed by unchecked casts like `(String)veh_nm.get(i)`. This is a legacy Java pattern that bypasses compile-time type safety.
**Risk:** `ClassCastException` at runtime if bean data types change. Tests would catch type mismatches immediately.

### A12-13 — NumberFormatException risk in ExcelServMaintenanceReport
**Severity:** MEDIUM
**File:** ExcelServMaintenanceReport.java, line 153
**Details:** `Double.parseDouble(nsDue)` and `Double.parseDouble((String)currMeterReadingList.get(i))` are called without try-catch. If either value is non-numeric (e.g., "-" or empty string from database), the entire report generation will fail with an unhandled `NumberFormatException`.
**Risk:** Corrupt or failed report output for edge-case data. No tests verify behavior with non-numeric meter readings.

### A12-14 — Hardcoded "unknown" sender and CC in MailExcelReports
**Severity:** LOW
**File:** MailExcelReports.java, lines 19, 35
**Details:** The `mail.sendMail()` calls pass `"unknown"` as the sender name and CC address. This is semantically unclear and may cause email delivery issues with strict mail servers.
**Risk:** Emails may be flagged as spam or rejected by mail servers that validate sender names.

### A12-15 — System.out.println used for operational logging in MailExcelReports
**Severity:** LOW
**File:** MailExcelReports.java, lines 14, 27
**Details:** `System.out.println` is used to log email send start/completion times instead of a structured logging framework (Log4j, SLF4J, etc.). These messages include email addresses in clear text.
**Risk:** Log output goes to container stdout, not application logs; no log level control; email addresses exposed in plain text.

### A12-16 — Unused local variables and imports in multiple classes
**Severity:** LOW
**Files affected:**
- ExcelUtilWOWReport.java lines 47-52 (`get_user`, `get_loc`, `get_dep`, `form_nm`, `chartUrl` declared but unused)
- ExcelUtilWOWReportEmail.java lines 48-53 (same unused variables)
- ExcelUtilisationReport.java lines 45-59 (`Vgp_cd`, `Vgp_nm`, `Vuser_cd`, `Vuser_nm`, `Vloc_cd`, `Vloc_nm`, `vdept_cd`, `vdept_nm`, `get_gp`, `get_user`, `get_loc`, `get_dep` -- 12 unused variables)
- Multiple files have duplicate `import java.util.ArrayList` statements
**Details:** Significant number of declared-but-unused variables and duplicate imports across the codebase.
**Risk:** Code readability and maintainability impact; suggests incomplete refactoring.

---

## Summary Table

| ID | Title | Severity | Files |
|---|---|---|---|
| A12-01 | Zero test coverage across all 16 files | CRITICAL | All 16 |
| A12-02 | FileOutputStream resource leak (no try-with-resources) | HIGH | 13 Excel report classes |
| A12-03 | Data bug: traction hours shows key hours in ExcelUtilisationReport | HIGH | ExcelUtilisationReport.java |
| A12-04 | Unused UnitDAO instantiations | MEDIUM | 9 classes |
| A12-05 | Live DB calls during report rendering | MEDIUM | ExcelRestrictedUsageReport, ExcelSuperMasterAuthReport |
| A12-06 | Code duplication: ExcelUtilWOWReport vs ExcelUtilWOWReportEmail | MEDIUM | 2 files |
| A12-07 | Code duplication: ExcelKeyHourUtilReport vs ExcelSeatHourUtilReport | MEDIUM | 2 files |
| A12-08 | Code duplication within ExcelPreOpCheckFailReport | MEDIUM | ExcelPreOpCheckFailReport.java |
| A12-09 | XSS vulnerability in MailBase HTML generation | HIGH | MailBase.java |
| A12-10 | Hardcoded HTTP URLs in MailBase | MEDIUM | MailBase.java |
| A12-11 | Exception handling uses only printStackTrace | MEDIUM | MailExcelReports.java |
| A12-12 | Raw ArrayList usage without generics | LOW | 10 classes |
| A12-13 | NumberFormatException risk in service maintenance report | MEDIUM | ExcelServMaintenanceReport.java |
| A12-14 | Hardcoded "unknown" sender/CC in mail dispatch | LOW | MailExcelReports.java |
| A12-15 | System.out.println used for operational logging | LOW | MailExcelReports.java |
| A12-16 | Unused local variables and duplicate imports | LOW | Multiple files |
