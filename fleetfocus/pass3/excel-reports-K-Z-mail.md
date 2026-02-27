# Pass 3 -- Documentation Audit: Excel Reports K-Z + Mail

**Audit ID:** A12-P3
**Date:** 2026-02-25
**Auditor:** Agent A12
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/` -- 16 files
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## 1. Executive Summary

All 16 files in this audit scope have **zero Javadoc** -- no class-level, constructor-level, or method-level Javadoc exists anywhere. Every public method across all files is undocumented. Inline comments are sparse and mostly limited to dead/commented-out code or IDE-generated `TODO` stubs. Four `TODO` markers were found in `MailExcelReports.java`, all of the auto-generated IDE variety (`TODO Auto-generated catch block`).

---

## 2. File-by-File Audit

### 2.1 ExcelKeyHourUtilReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelKeyHourUtilReport.java` |
| **Lines** | 357 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "Unit Utilisation Report" Excel workbook with two sections: utilised units (total != "0:0:00") and un-utilised units. Uses `KeyHourUtilBean` for data. Splits 24h into 8 three-hour buckets (12-03 AM through 09-12 PM). |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelKeyHourUtilReport(String docRoot, String fileName, KeyHourUtilBean utilBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc. Returns file path. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (commented-out code, line 117)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Unused import `EvaluationCell` (line 11), unused import `Date` (line 8), duplicate import `java.util.ArrayList` (line 9). Unused local variable `unitDAO` (line 106). Raw-type `ArrayList` used throughout without generics.

---

### 2.2 ExcelOperationalStatusReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelOperationalStatusReport.java` |
| **Lines** | 159 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates an "Operational Status Report" Excel workbook. Columns: Equipment No, Serial No, Model, Trigger Type, Status, Initiated By, Set Time, Note. Supports optional search criteria via `BaseFilterBean`. URL-decodes the search criteria string. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelOperationalStatusReport(String docRoot, String fileName, BaseResultBean resultBean)` | No Javadoc |
| `createExcel` | `createExcel(String custName, String siteName, String deptName)` | No Javadoc |
| `createOperationStatusReport` | `createOperationStatusReport(String custName, String siteName, String deptName)` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `// If there's an error decoding, use the original value` (line 74), `// Make sure search parameter is properly decoded` (line 70)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** None specific to documentation.

---

### 2.3 ExcelPreOpCheckFailReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckFailReport.java` |
| **Lines** | 383 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "PreOp Check Report - Incorrect Only" report. Two overloaded `createExcel` methods (one with `form` parameter). Two overloaded `createPreOpFailReport` methods -- nearly identical logic with ~150 lines of duplicated code. Columns: Equipment NO, Serial No, Model, Driver Name, Driver ID, Date and Time, Check Completed?, Checklist Failures, Checklist Type, Initialization to Completion Time, Comment. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelPreOpCheckFailReport(String docRoot, String fileName, PreOpCheckFailReportBean preOpBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createExcel` (overloaded) | `createExcel(String cust, String loc, String dep, String st, String et, String form)` | No Javadoc. The `form` parameter is passed through but its effect is undocumented. |
| `createPreOpFailReport` | `createPreOpFailReport(String cust, String loc, String dep, String st, String et)` | No Javadoc. Public but could be private. |
| `createPreOpFailReport` (overloaded) | `createPreOpFailReport(String cust, String loc, String dep, String st, String et, String form)` | No Javadoc. The `form` parameter is unused inside the method body. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (commented-out code, line 97)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Unused import `Vector` (line 6). Unused local variable `unitDAO` (lines 86, 245). `form` parameter in the overloaded method is accepted but never used -- misleading API. The variable `style` on line 276 is set but only used at the very end of the method via `setTotalDuration`.

---

### 2.4 ExcelPreOpCheckReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckReport.java` |
| **Lines** | 203 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "PreOp Check Report" (all entries, not only failures). Same column structure as PreOpCheckFailReport. Uses `PreOpCheckReportBean`. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelPreOpCheckReport(String docRoot, String fileName, PreOpCheckReportBean preOpBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createPreOpReport` | `createPreOpReport(String cust, String loc, String dep, String st, String et)` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (commented-out code, line 79)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Unused imports `CellStyle` (line 8), `CellRangeAddress` (line 12). Unused local variable `unitDAO` (line 68). Unused local variable `evaluator` would not exist but `FormulaEvaluator` import (line 9) is present and unused explicitly at file scope.

---

### 2.5 ExcelRestrictedUsageReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelRestrictedUsageReport.java` |
| **Lines** | 272 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "Restricted Access Usage Report" for on-demand fleet units. Uses a `Map<String, ArrayList<RestrictedAccessUsageBean>>`. Columns: Equipment NO, Serial No, On-Demand, Hour Meter Starts At, Hour Meter Finish At, Service Hour From, Total Usage, Hourly Rate, Max Monthly Rate, Total Charge. Includes per-fleet subtotals and a grand total row. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelRestrictedUsageReport(String docRoot, String fileName, Map<...> map, String grand_total_charge)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et, String model)` | No Javadoc. `model` parameter is accepted but never used in the method body. |
| `createRestrictedAccessReport` | `createRestrictedAccessReport(String cust, String loc, String dep, String st, String et, String model)` | No Javadoc. `model` parameter is accepted but never used. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 71)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Unused local variable `temp` (line 101, set to "x" but never read). `model` parameter is unused in both `createExcel` and `createRestrictedAccessReport`.

---

### 2.6 ExcelSeatHourUtilReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSeatHourUtilReport.java` |
| **Lines** | 357 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Nearly identical to `ExcelKeyHourUtilReport` but for seat-based utilisation. Generates a "Unit Utilisation Report - Seat" with the same 8 time-bucket structure. Uses `SeatHourUtilBean`. Two sections: utilised and un-utilised units. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelSeatHourUtilReport(String docRoot, String fileName, SeatHourUtilBean utilBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 116)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Duplicate import `java.util.ArrayList` (line 8). Unused local variable `unitDAO` (line 105). Unused local variable `evaluator` (line 136). Raw-type `ArrayList` used throughout.

---

### 2.7 ExcelServMaintenanceReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelServMaintenanceReport.java` |
| **Lines** | 272 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "Service Report" Excel workbook. Columns: Equipment NO, Serial No, Service Hour Starts At, Service Hour Finish At, Service Hours From, Last Service Date, Next Service Date, Last Service Type Carried Out, Hours at Last Service, Next Service Due, Hours to Next Service, Current Meter Reading, (optionally) Customer. Uses color-coded cells (red/green/orange) for service urgency. Conditionally adds "Customer" column when `cust` equals "all". |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelServMaintenanceReport(String docRoot, String fileName, ServMaintenanceReportBean bean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createServMaintenanceReport` | `createServMaintenanceReport(String cust, String loc, String dep, String st, String et)` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 2 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 81), `//Customer Defined Next Service Type Due` (line 148)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Duplicate import `java.util.ArrayList` (line 7). Uses color status logic (`DataUtil.getColourStatus`) but the mapping between integer thresholds and colors is not documented here.

---

### 2.8 ExcelSpareModuleReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSpareModuleReport.java` |
| **Lines** | 155 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "Spare Module Report" with no date/customer/site parameters in `createExcel` (parameter-less). Columns: Status, Type, GMTP ID, Old GMTP ID, From Serial, From Customer, From Site, From Department, Last Update, Swap Date, CCID, RA Number, Tech Number, Note. Uses `ArrayList<SpareModuleBean>`. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelSpareModuleReport(String docRoot, String fileName, ArrayList<SpareModuleBean> arrSpareModuleBean)` | No Javadoc |
| `createExcel` | `createExcel()` | No Javadoc. Takes no filter parameters unlike other reports. |
| `createSpareModuleReport` | `createSpareModuleReport()` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 56)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** None specific.

---

### 2.9 ExcelSuperMasterAuthReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSuperMasterAuthReport.java` |
| **Lines** | 151 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates an "On-Demand Authorisation Report" Excel workbook. Columns: Equipment NO, Serial No, Authorisation Start Time, Authorisation End Time, On-Demand Code. Groups rows by fleet number (subsequent rows for the same fleet omit fleet/serial columns). Uses `CustomerDAO` to resolve customer/location/department names. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelSuperMasterAuthReport(String docRoot, String fileName, SuperMasterAuthReportBean sBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et, String model)` | No Javadoc. `model` parameter is accepted but never used. |
| `createSuperMasterAuthReport` | `createSuperMasterAuthReport(String cust, String loc, String dep, String st, String et, String model)` | No Javadoc. `model` parameter unused. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 71)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Duplicate import `java.util.ArrayList` (line 7). Unused imports `DriverImpactReportBean` (line 15). `model` parameter is accepted but not used. Unused local variable `temp` (line 96, set to "x" only used for deduplication logic but its intent is undocumented).

---

### 2.10 ExcelUnitUnlockReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUnitUnlockReport.java` |
| **Lines** | 148 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "Machine Unlock Report" Excel workbook. Columns: Equipment NO, Serial No, Lockout Type, Lockout Time, Driver, Unlock Time, Master Code, Unlock Reason, Is This A Real Impact. Includes a filter subtitle row. Impact-related rows show real impact status ("Unconfirmed" when "unsure"). |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelUnitUnlockReport(String docRoot, String fileName, UnitUnlockReportBean bean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createUnitUnlockReport` | `createUnitUnlockReport(String cust, String loc, String dep, String st, String et)` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 73)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Duplicate import `java.util.ArrayList` (line 6). Unused local variable `unitDAO` (line 61). Raw-type `ArrayList` used throughout.

---

### 2.11 ExcelUtilWOWReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReport.java` |
| **Lines** | 173 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "Unit Utilisation by Hour Report" Excel workbook. Columns: Customer, Site, Department, Model, Date, Day, Hour Interval, Trucks Logged on, Number of Trucks on Site. Iterates over a nested structure: `UtilModelBean` -> `UtilBean` -> `util_no_veh_day[]` (24 hourly intervals). |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelUtilWOWReport(String docRoot, String fileName, UtilWowReportBean utilBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createUtilWowReport` | `createUtilWowReport(String cust, String loc, String dep, String from, String to)` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 79)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Unused imports `PreOpCheckReportBean` (line 14). Unused local variables `get_user`, `get_loc`, `get_dep`, `form_nm`, `chartUrl` (lines 47-52). Unused local variable `unitDAO` (line 68).

---

### 2.12 ExcelUtilWOWReportEmail.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReportEmail.java` |
| **Lines** | 180 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Email variant of `ExcelUtilWOWReport`. Identical structure but contains an AU-specific branch: when `LindeConfig.siteName` is "AU", renders a chart image via `addImageUtilisationChart()` instead of tabular data. Otherwise, identical spreadsheet output to `ExcelUtilWOWReport`. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelUtilWOWReportEmail(String docRoot, String fileName, UtilWowReportBean utilBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createUtilWowReport` | `createUtilWowReport(String cust, String loc, String dep, String from, String to)` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 1 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 80)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Unused imports `PreOpCheckReportBean` (line 14). Unused local variables `get_user`, `get_loc`, `get_dep`, `form_nm` (lines 48-51). Unused variable `unitDAO` (line 69). Massive code duplication with `ExcelUtilWOWReport.java`.

---

### 2.13 ExcelUtilisationReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilisationReport.java` |
| **Lines** | 229 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "Site Utilisation Report" Excel workbook. Columns: Equipment NO, Serial No, Model, Hours Available, Logged on Hours, Logged on Hours %, Seat Hours, Seat Hours %, Traction Hours, Traction Hours %, Hydraulic Hours, Hydraulic Hours %. Uses `UtilisationReportBean` and `UnitUtilSummaryBean`. Includes totals row. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelUtilisationReport(String docRoot, String fileName, UtilisationReportBean utilBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createUtilReport` | `createUtilReport(String custName, String locName, String deptName, String from, String to)` | No Javadoc. Public but could be private. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 2 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 91), `//sheet.protectSheet(null);` (line 76, commented-out code)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Duplicate import `java.util.ArrayList` (line 7). Unused local variables `Vgp_cd`, `Vgp_nm`, `Vuser_cd`, `Vuser_nm`, `Vloc_cd`, `Vloc_nm`, `vdept_cd`, `vdept_nm`, `get_gp`, `get_user`, `get_loc`, `get_dep` (lines 45-59). Unused local variable `unitDAO` (line 80). Potential bug on line 163: `contentCell.setCellValue(utilBean.getKey_hours())` is set for the "Traction Hours" column -- should likely be `utilBean.getTrack_hours()`.

---

### 2.14 ExcelVorReport.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat\fms6/excel/reports/ExcelVorReport.java` |
| **Lines** | 313 |
| **Extends** | `Frm_excel` |
| **Class Javadoc** | NONE |
| **Reading evidence** | Generates a "VOR Report" (Vehicle Off Road) Excel workbook. Complex nested structure: per-vehicle-model -> per-vehicle -> per-driver session. Uses a `do_list` CSV string to control which fields are hidden. Dynamic column headers based on `vrpt_field_cd`/`vrpt_field_nm`. Includes per-vehicle totals and grand totals per model. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| Constructor | `ExcelVorReport(String docRoot, String fileName, DynUnitReportBean dynBean)` | No Javadoc |
| `createExcel` | `createExcel(String cust, String loc, String dep, String st, String et)` | No Javadoc |
| `createVorReport` | `createVorReport(String cust, String loc, String dep, String st, String et)` | No Javadoc. Public but could be private. Has inline comment `// end method createDynReport` which uses a different name than the actual method. |
| `getFileName` | `getFileName()` | No Javadoc |

**Inline comments:** 5 -- `//adjust first column width: sheet.autoSizeColumn(0);` (line 121), `//deal with do_list here.` (line 76), `// Set the 'hide' option as '1'.` (line 84), `//end for loop...` (lines 263, 290, 306, 307), `// end method createDynReport` (line 308 -- **inaccurate**, method is named `createVorReport`)
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Unused local variable `unitDAO` (line 105). Misleading end-of-method comment references `createDynReport` instead of `createVorReport` (line 308). The variable `vrpt_veh_value_stopv` (line 57) is assigned the same value as `vrpt_veh_value_stop` (line 55) -- appears to be a copy-paste error.

---

### 2.15 MailBase.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java` |
| **Lines** | 128 |
| **Extends** | `Object` (default) |
| **Class Javadoc** | NONE |
| **Reading evidence** | Utility class that builds HTML email headers for FleetFocus reports. Two overloaded `setMailHeader` methods: one without model, one with model. Outputs hard-coded Linde-branded HTML with `http://` URLs (not HTTPS) to `fleetfocus.lindemh.com.au`. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| `setMailHeader` | `setMailHeader(String st, String et, String cust, String loc, String dep, String rptName)` | No Javadoc. 6 parameters. |
| `setMailHeader` (overloaded) | `setMailHeader(String st, String et, String cust, String loc, String dep, String model, String rptName)` | No Javadoc. 7 parameters with added `model`. |

**Inline comments:** None
**TODO/FIXME/HACK/XXX:** None
**Accuracy concerns:** Hard-coded HTTP URLs to `fleetfocus.lindemh.com.au` for images and CSS (lines 10, 15, 24, 69, 74, 83). No HTML escaping of parameters -- potential XSS risk if any parameter contains user-controlled HTML. Incomplete `<!DOCTYPE>` declaration (line 6 -- missing doctype specification).

---

### 2.16 MailExcelReports.java

| Item | Detail |
|---|---|
| **Path** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailExcelReports.java` |
| **Lines** | 45 |
| **Extends** | `Object` (default) |
| **Class Javadoc** | NONE |
| **Reading evidence** | Sends Excel report attachments via email using the `mail` utility class. Two overloaded `sendExcelReport` methods: one with auto-generated body text, one with custom body. Uses `LindeConfig.mail_from` as sender. Logs timing via `System.out.println`. |

**Public methods (all undocumented):**

| Method | Signature | Notes |
|---|---|---|
| `sendExcelReport` | `sendExcelReport(String subject, String email_id, String attachment, String attachmentName)` | No Javadoc. 4 parameters. |
| `sendExcelReport` (overloaded) | `sendExcelReport(String subject, String body, String email_id, String attachment, String attachmentName)` | No Javadoc. 5 parameters. |

**Inline comments:** None (only auto-generated TODO stubs)
**TODO/FIXME/HACK/XXX:** **4 instances**
- Line 21: `// TODO Auto-generated catch block` (AddressException in first overload)
- Line 24: `// TODO Auto-generated catch block` (MessagingException in first overload)
- Line 37: `// TODO Auto-generated catch block` (AddressException in second overload)
- Line 40: `// TODO Auto-generated catch block` (MessagingException in second overload)

**Accuracy concerns:** Hard-coded "unknown" strings passed as sender name and CC parameters to `mail.sendMail` (lines 19, 35). Exceptions are caught but only `e.printStackTrace()` is used -- no logging framework. The `System.out.println` logging on lines 14 and 27 exists in the first overload but not the second.

---

## 3. Consolidated Findings

### 3.1 Javadoc Coverage

| Metric | Count |
|---|---|
| Total files audited | 16 |
| Files with class-level Javadoc | **0** |
| Files with any method Javadoc | **0** |
| Total public methods across all files | **50** |
| Documented public methods | **0** |
| **Documentation coverage** | **0%** |

### 3.2 TODO/FIXME/HACK/XXX Summary

| File | Line(s) | Marker | Text |
|---|---|---|---|
| `MailExcelReports.java` | 21 | TODO | `Auto-generated catch block` (AddressException) |
| `MailExcelReports.java` | 24 | TODO | `Auto-generated catch block` (MessagingException) |
| `MailExcelReports.java` | 37 | TODO | `Auto-generated catch block` (AddressException) |
| `MailExcelReports.java` | 40 | TODO | `Auto-generated catch block` (MessagingException) |

**Total:** 4 TODO markers, all IDE-generated stubs. No FIXME, HACK, or XXX markers found.

### 3.3 Inline Comment Quality

| Category | Count | Notes |
|---|---|---|
| Commented-out code | ~14 instances | `//adjust first column width: sheet.autoSizeColumn(0);` appears in nearly every file; `//sheet.protectSheet(null);` in ExcelUtilisationReport |
| Meaningful comments | 3 | `// Make sure search parameter is properly decoded`, `//Customer Defined Next Service Type Due`, `// Set the 'hide' option as '1'.` |
| Inaccurate comments | 1 | `// end method createDynReport` in ExcelVorReport.java (method is named `createVorReport`) |
| End-of-block markers | 5 | `//end for loop...` variants in ExcelVorReport |

### 3.4 Undocumented Public Methods (Complete List)

All 50 public methods across 16 files lack Javadoc. The complete list:

| # | Class | Method |
|---|---|---|
| 1 | ExcelKeyHourUtilReport | Constructor |
| 2 | ExcelKeyHourUtilReport | `createExcel(String,String,String,String,String)` |
| 3 | ExcelKeyHourUtilReport | `getFileName()` |
| 4 | ExcelOperationalStatusReport | Constructor |
| 5 | ExcelOperationalStatusReport | `createExcel(String,String,String)` |
| 6 | ExcelOperationalStatusReport | `createOperationStatusReport(String,String,String)` |
| 7 | ExcelOperationalStatusReport | `getFileName()` |
| 8 | ExcelPreOpCheckFailReport | Constructor |
| 9 | ExcelPreOpCheckFailReport | `createExcel(String,String,String,String,String)` |
| 10 | ExcelPreOpCheckFailReport | `createExcel(String,String,String,String,String,String)` |
| 11 | ExcelPreOpCheckFailReport | `createPreOpFailReport(String,String,String,String,String)` |
| 12 | ExcelPreOpCheckFailReport | `createPreOpFailReport(String,String,String,String,String,String)` |
| 13 | ExcelPreOpCheckFailReport | `getFileName()` |
| 14 | ExcelPreOpCheckReport | Constructor |
| 15 | ExcelPreOpCheckReport | `createExcel(String,String,String,String,String)` |
| 16 | ExcelPreOpCheckReport | `createPreOpReport(String,String,String,String,String)` |
| 17 | ExcelPreOpCheckReport | `getFileName()` |
| 18 | ExcelRestrictedUsageReport | Constructor |
| 19 | ExcelRestrictedUsageReport | `createExcel(String,String,String,String,String,String)` |
| 20 | ExcelRestrictedUsageReport | `createRestrictedAccessReport(String,String,String,String,String,String)` |
| 21 | ExcelRestrictedUsageReport | `getFileName()` |
| 22 | ExcelSeatHourUtilReport | Constructor |
| 23 | ExcelSeatHourUtilReport | `createExcel(String,String,String,String,String)` |
| 24 | ExcelSeatHourUtilReport | `getFileName()` |
| 25 | ExcelServMaintenanceReport | Constructor |
| 26 | ExcelServMaintenanceReport | `createExcel(String,String,String,String,String)` |
| 27 | ExcelServMaintenanceReport | `createServMaintenanceReport(String,String,String,String,String)` |
| 28 | ExcelServMaintenanceReport | `getFileName()` |
| 29 | ExcelSpareModuleReport | Constructor |
| 30 | ExcelSpareModuleReport | `createExcel()` |
| 31 | ExcelSpareModuleReport | `createSpareModuleReport()` |
| 32 | ExcelSpareModuleReport | `getFileName()` |
| 33 | ExcelSuperMasterAuthReport | Constructor |
| 34 | ExcelSuperMasterAuthReport | `createExcel(String,String,String,String,String,String)` |
| 35 | ExcelSuperMasterAuthReport | `createSuperMasterAuthReport(String,String,String,String,String,String)` |
| 36 | ExcelSuperMasterAuthReport | `getFileName()` |
| 37 | ExcelUnitUnlockReport | Constructor |
| 38 | ExcelUnitUnlockReport | `createExcel(String,String,String,String,String)` |
| 39 | ExcelUnitUnlockReport | `createUnitUnlockReport(String,String,String,String,String)` |
| 40 | ExcelUnitUnlockReport | `getFileName()` |
| 41 | ExcelUtilWOWReport | Constructor |
| 42 | ExcelUtilWOWReport | `createExcel(String,String,String,String,String)` |
| 43 | ExcelUtilWOWReport | `createUtilWowReport(String,String,String,String,String)` |
| 44 | ExcelUtilWOWReport | `getFileName()` |
| 45 | ExcelUtilWOWReportEmail | Constructor |
| 46 | ExcelUtilWOWReportEmail | `createExcel(String,String,String,String,String)` |
| 47 | ExcelUtilWOWReportEmail | `createUtilWowReport(String,String,String,String,String)` |
| 48 | ExcelUtilWOWReportEmail | `getFileName()` |
| 49 | ExcelUtilisationReport | Constructor |
| 50 | ExcelUtilisationReport | `createExcel(String,String,String,String,String)` |
| 51 | ExcelUtilisationReport | `createUtilReport(String,String,String,String,String)` |
| 52 | ExcelUtilisationReport | `getFileName()` |
| 53 | ExcelVorReport | Constructor |
| 54 | ExcelVorReport | `createExcel(String,String,String,String,String)` |
| 55 | ExcelVorReport | `createVorReport(String,String,String,String,String)` |
| 56 | ExcelVorReport | `getFileName()` |
| 57 | MailBase | `setMailHeader(String,String,String,String,String,String)` |
| 58 | MailBase | `setMailHeader(String,String,String,String,String,String,String)` |
| 59 | MailExcelReports | `sendExcelReport(String,String,String,String)` |
| 60 | MailExcelReports | `sendExcelReport(String,String,String,String,String)` |

### 3.5 Comment Accuracy Issues

| File | Line | Issue |
|---|---|---|
| `ExcelVorReport.java` | 308 | Comment says `// end method createDynReport` but method is named `createVorReport` |
| `ExcelUtilisationReport.java` | 163 | Cell is for "Traction Hours" column but value set is `utilBean.getKey_hours()` instead of `utilBean.getTrack_hours()` -- no comment explains this, and it appears to be a data accuracy bug rather than intentional |

### 3.6 Cross-Cutting Patterns

1. **Zero documentation across all 16 files.** No class, method, or field Javadoc anywhere.
2. **Repeated commented-out code** -- `//adjust first column width: sheet.autoSizeColumn(0);` appears in 12 of 14 Excel report files, creating noise.
3. **Unused local variables** -- `unitDAO` is instantiated but never used in at least 8 files.
4. **Raw types** -- `ArrayList` without generics is the norm in the older report classes.
5. **Duplicate imports** -- `java.util.ArrayList` is imported twice in 6 files.
6. **Public methods that should be private** -- The `create*Report` methods are public but appear to be internal implementation details called only from `createExcel`.
7. **Unused parameters** -- `model` parameter is accepted but never used in `ExcelRestrictedUsageReport` and `ExcelSuperMasterAuthReport`.

---

## 4. Risk Assessment

| Risk | Severity | Files Affected |
|---|---|---|
| Complete lack of Javadoc makes maintenance hazardous | HIGH | All 16 |
| Inaccurate comment may mislead future developers | LOW | ExcelVorReport.java |
| IDE-generated TODO stubs mask real exception handling gaps | MEDIUM | MailExcelReports.java |
| Possible data bug (key_hours used for traction column) | HIGH | ExcelUtilisationReport.java (line 163) |

---

*End of Pass 3 Documentation Audit -- Agent A12*
