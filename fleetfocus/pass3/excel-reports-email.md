# Pass 3 -- Documentation Audit: excel/reports Email Classes

**Audit agent:** A10
**Date:** 2026-02-25
**Scope:** 28 Email*Report classes under `WEB-INF/src/com/torrent/surat/fms6/excel/reports/`
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## 1. Summary

All 28 files were read in full. Every file follows a nearly identical pattern:

- Extends `Frm_excel` (Apache POI-based Excel report superclass).
- Provides one or more constructors that accept customer/location/department/date-range/params/dir and call `super(...)` then `setTitle(...)`.
- Exposes a `createExcel()` method that delegates to a report-builder, writes the workbook to `FileOutputStream`, and returns the file path.
- Exposes a report-builder method (e.g., `createBatteryReport()`, `createBroadcastMsgReport()`) that queries a `Databean_report` or `Databean_dyn_reports`, populates an Excel sheet with subtitles, headers, and data rows.

**No class-level Javadoc exists on any of the 28 files.**
**No method-level Javadoc exists on any public or private method in any of the 28 files.**
**No TODO, FIXME, HACK, or XXX markers found in any of the 28 files.**

---

## 2. Per-File Audit

### 2.1 EmailBatteryReport.java (153 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBatteryReport.java` |
| **Lines** | 153 |
| **Class Javadoc** | NONE |
| **Superclass** | `Frm_excel` |
| **Constructors** | 2 (7-param, 8-param with `formName`) -- both undocumented |
| **Public methods** | `createExcel()`, `createBatteryReport()`, `getFileName()` -- all undocumented |
| **Method Javadoc** | NONE on any method |
| **Inline comments** | 1 -- line 101: `//adjust first column width: sheet.autoSizeColumn(0);` (commented-out code) |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Battery State of Charge Report". Uses `Databean_dyn_reports` with op_code `rpt_battery`. Headers: Equipment NO, Serial No, Driver, Time, Battery Level(%). Uses `CustomerDAO.getModelName()` for model. |
| **Duplicate import** | `java.util.ArrayList` imported twice (lines 6-7) |
| **Documentation accuracy** | N/A (no documentation exists) |

### 2.2 EmailBroadcastMsgReport.java (149 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBroadcastMsgReport.java` |
| **Lines** | 149 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createBroadcastMsgReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Inline comments** | 1 -- line 79: commented-out autoSizeColumn |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title set as "Machine Unlock Report" in constructor but tab/sheet title is "Broadcast Message Report" -- **potential title mismatch**. Uses `Databean_report` with `rpt_broadcast`. Uses `BroadcastmsgBean`. Headers: Equipment NO, Serial No, Driver, Type, Message Text, Response, Sent Time, Response Time, Display Time. `UnitDAO unitDAO` instantiated on line 68 but never used. |
| **Deviation from pattern** | Title in constructor ("Machine Unlock Report") differs from tab title ("Broadcast Message Report"). |

### 2.3 EmailCimplicityShockReport.java (167 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityShockReport.java` |
| **Lines** | 167 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (7-param, 8-param) -- undocumented |
| **Public methods** | `createExcel()`, `createCimplicityShockReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Inline comments** | 1 -- commented-out autoSizeColumn |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **Reading evidence** | Title = "Cimplicity Shock Report". Uses `Databean_report` with `d_simp_shock`. Shows top 5 best/worst drivers and vehicles. `UnitDAO unitDAO` instantiated but never used. |

**Same documentation pattern as EmailBatteryReport -- no Javadoc at any level.**

### 2.4 EmailCimplicityUtilReport.java (166 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityUtilReport.java` |
| **Lines** | 166 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (7-param, 8-param) -- undocumented |
| **Public methods** | `createExcel()`, `createCimplicityUtilisationReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Cimplicity Utilisation Report". Uses `Databean_report` with `d_simp_sum`. `UnitDAO unitDAO` instantiated but never used. |

**Same documentation pattern as EmailBatteryReport.**

### 2.5 EmailCurrDrivReport.java (143 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrDrivReport.java` |
| **Lines** | 143 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (7-param, 8-param) -- undocumented |
| **Public methods** | `createExcel()`, `createCurrDrivReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Current Status Report by Driver". Uses `Databean_dyn_reports` with `curr_driv_report`. Commented-out code at lines 99-101 (conditional Dept column). `UnitDAO unitDAO` instantiated but never used. |

**Same documentation pattern as EmailBatteryReport.**

### 2.6 EmailCurrUnitReport.java (149 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrUnitReport.java` |
| **Lines** | 149 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (7-param, 8-param) -- undocumented |
| **Public methods** | `createExcel()`, `createCurrUnitReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Current Status Report by Unit". Uses `Databean_dyn_reports` with `curr_unit_report`. Conditionally adds "Dept." column when `deptName == "all"`. `UnitDAO unitDAO` instantiated but never used. |

**Same documentation pattern as EmailCurrDrivReport (near-identical counterpart by Unit rather than by Driver).**

### 2.7 EmailDailyVehSummaryReport.java (331 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDailyVehSummaryReport.java` |
| **Lines** | 331 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createDSumReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Summary Report". Uses `Databean_report` with either `d_veh_sum` or `d_driv_sum` based on `isVeh` flag. Conditionally adds columns based on `cust_type` (`RuntimeConf.cust_leader`, `cust_cimp`, `cust_combine`). More complex than simpler reports. Contains total row with `setTotalDuration`. `UnitDAO unitDAO` instantiated but never used. |
| **Deviation** | Longer and more complex than the basic pattern; has conditional column rendering based on customer type. Total row rendering does not check `cust_type` gating -- always renders all totals including leader-only columns (potential bug outside documentation scope). |

### 2.8 EmailDriverAccessAbuseReport.java (356 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverAccessAbuseReport.java` |
| **Lines** | 356 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (standard 7-param; `String[] args, String dir`) -- undocumented |
| **Public methods** | `init()`, `init2()`, `createExcel()`, `createEmail()`, `createAbuseReport()`, `createBody()`, `getFileName()`, `getBody()` -- **8 public methods, ALL undocumented** |
| **Method Javadoc** | NONE except a brief inline comment on `createEmail()` line 154: `//Generates Email with report body and excel attachment` |
| **Inline comments** | Line 83: commented-out ArrayList; Line 154: method purpose inline comment; Line 181: commented-out autoSizeColumn |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **Reading evidence** | Title = "Driver Access Abuse Report". Uses `Databean_report` with `access_abuse_au`. Has instance-level `Databean_report`, `StringBuilder body`, `CustomerDAO`. Has two initialization methods `init()` and `init2()` that are largely duplicated -- `init()` reads filters from `params[]` array, `init2()` reads them via `getParam()`. `createExcel()` calls `init2()` then `createAbuseReport()`. `createEmail()` calls `createBody()` then `createAbuseReport()` but **does not call init() or init2()** -- relies on caller to have invoked `init()` first. `createBody()` generates HTML email body. |
| **Deviation from pattern** | Significant: has dual initialization, HTML email body generation via `createBody()`, separate `createEmail()` flow. More complex lifecycle than standard Email reports. Instance fields store intermediate data between init and report phases. |

### 2.9 EmailDriverImpactReport.java (179 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverImpactReport.java` |
| **Lines** | 179 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param with `params` as 6th arg) -- undocumented |
| **Public methods** | `createExcel()`, `createDrivImpReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Driver Impact Report". Uses `Databean_report` with `impact_driver_rep`. Contains commented-out block (lines 69-79) referencing `filter` variable that was replaced by `dbreport`. Uses `CustomerDAO.getModelName()`. `FormulaEvaluator` imported and instantiated but never used for evaluation. |

**Same documentation pattern as EmailBatteryReport.**

### 2.10 EmailDriverLicenceExpiry.java (116 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverLicenceExpiry.java` |
| **Lines** | 116 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createLicenceExpiryReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Driver LIcence Expiry Report" (note: **typo "LIcence"** -- uppercase I -- appears 3 times: lines 22, 68, 72). Uses `Databean_report` with `driver_licence_detail`. `UnitDAO unitDAO` instantiated but never used. |
| **Deviation** | Naming inconsistency: class name says `Licence` (British) but title has typo `LIcence`. |

### 2.11 EmailDynDriverReport.java (315 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynDriverReport.java` |
| **Lines** | 315 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createDynDriverReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Detailed Report by Driver". Uses `Databean_dyn_reports` with `dyn_driver_report`. Uses `StringTokenizer` to parse `do_list` for field hiding. Multi-level nested loops (vehicle type > driver > vehicle > field). Complex nested ArrayList structures. `UnitDAO unitDAO` instantiated but never used. Commented-out `dbreport.setSet_form_cd(form_cd)` at line 71. |

**Same documentation pattern as EmailBatteryReport. Complex nested structure but zero documentation.**

### 2.12 EmailDynSeenReport.java (244 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynSeenReport.java` |
| **Lines** | 244 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createDynUnitReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Pedestrian Detection Report". Uses `Databean_dyn_reports` with `seen_iris_pedestrian`. Method named `createDynUnitReport()` but report is about pedestrian detection -- **naming mismatch**. `UnitDAO unitDAO` instantiated but never used. `vor_flag` variable declared but only used if params length > 3 (no apparent usage within report). `FormulaEvaluator` imported but never used. |
| **Deviation** | Method name `createDynUnitReport()` does not match report purpose (Pedestrian Detection). |

### 2.13 EmailDynUnitReport.java (352 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynUnitReport.java` |
| **Lines** | 352 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createDynUnitReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Detailed Report by Unit". Uses `Databean_dyn_reports` with `dyn_unit_report`. Nearly identical structure to EmailDynDriverReport but organized by vehicle model. Extensive commented-out code (lines 281-283, 323-326, 344-346) referencing old `TIME()` formula approach replaced by `VALUE()`. `UnitDAO unitDAO` instantiated but never used. Uses `excluded_veh_cd` list to conditionally skip vehicles. |

**Same documentation pattern as EmailDynDriverReport. Unit-counterpart to the driver version.**

### 2.14 EmailHireDehireReport.java (134 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailHireDehireReport.java` |
| **Lines** | 134 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (`String docRoot, String fileName, HireDehireReportBean`) -- **different constructor signature from all other Email reports** |
| **Public methods** | `createExcel(String st, String et, String sc)`, `createHireDehireReport(String st, String et, String search_crit)`, `getFileName()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Hire Dehire Report". Uses `HireDehireReportBean` (passed in constructor, not queried from DB here). Constructor takes `docRoot` and `fileName` instead of the standard cust/loc/dep/st/et/params/dir pattern. `createExcel()` takes parameters `st, et, sc` rather than reading from instance fields. Creates output directory if not exists. No `Databean_report` usage. |
| **Deviation from pattern** | Significant: different constructor signature (`docRoot, fileName, bean`), different `createExcel()` signature (takes `st, et, sc` parameters), data comes from injected bean rather than querying `Databean_report` directly. Does not follow the standard initialization pattern. |

### 2.15 EmailImpactMeterReport.java (230 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactMeterReport.java` |
| **Lines** | 230 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (no-arg, 7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createImpactReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Impact Report". Uses `Databean_report` with `impact_photo_rep`. Includes image embedding (`addImage2`). Hardcoded URL on line 204: `http://fleetfocus.lindemh.com.au/fms/...` references `RuntimeConf.impactDir`. Color-coded severity levels (Red/Amber/Blue). Includes meter percentage data via `DataUtil.convertToImpPerc()`. Differs from EmailImpactReport by including "Impact Data" column and meter details in severity display. `DecimalFormat` imported but never used. `UnitDAO unitDAO` instantiated but never used. |
| **Deviation** | Has a no-arg constructor (unique among most reports). Includes "Impact Data" column that EmailImpactReport lacks. |

### 2.16 EmailImpactReport.java (223 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactReport.java` |
| **Lines** | 223 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (no-arg, 7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createImpactReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Nearly identical to EmailImpactMeterReport. Title = "Impact Report". Same `impact_photo_rep` op code. Same hardcoded URL (`http://fleetfocus.lindemh.com.au/fms/`). Differs by not having the "Impact Data" column and showing severity level without meter percentage. `DecimalFormat` imported but never used. `UnitDAO unitDAO` instantiated but never used. |

**Same documentation pattern as EmailImpactMeterReport. Very similar code -- candidate for consolidation.**

### 2.17 EmailKeyHourUtilReport.java (346 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailKeyHourUtilReport.java` |
| **Lines** | 346 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (no-arg, 7-param) -- undocumented |
| **Public methods** | `createExcel()` -- undocumented |
| **Private methods** | `createUtilReport()` -- undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Unit Utilisation Report". Uses `Databean_report` with `key_hour`. Shows 8 time periods (3-hour blocks across 24h). Has "Un Utilised Units" section after utilized units. **Subtitle labels appear swapped**: line 112-114 sets Customer=locName, Site=deptName, Dept=custName. `FormulaEvaluator` instantiated but never used for evaluation. Note: total row is missing the "Model" column (only 2 empty cells before totals instead of 3). |
| **Deviation** | Subtitle label swap (Customer/Site/Dept values misassigned). `createUtilReport()` is private, not public. Has no-arg constructor. |

### 2.18 EmailPreOpChkFailReport.java (225 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkFailReport.java` |
| **Lines** | 225 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createPreOpFailReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "PreOp Check Report - Incorrect Only". Uses `Databean_report` with `preop_chk`. Filters to show only failed checks (`fail1 != "-"`). Includes: Equipment NO, Serial No, Model, Driver Name/ID, Date, Check Completed, Failures, Checklist Type (maps codes 1/2/3 to Optional/Prompt), Initialization to Completion Time, Comment. Extra wide Comment column (40*256). Average completion time total row. `UnitDAO unitDAO` instantiated but never used. `FormulaEvaluator` instantiated but never used. `Vector` imported but never used. |

**Same documentation pattern as EmailBatteryReport.**

### 2.19 EmailPreOpChkReport.java (232 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkReport.java` |
| **Lines** | 232 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createPreOpReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Inline comments** | Lines 41-56: helpful comments explaining URL parameter construction from different JSP pages |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "PreOp Check Report". Uses `Databean_report` with `preop_chk`. Shows ALL records (not just failures). Has conditional parameter parsing logic based on `params.length == 4` vs other cases, with inline comments explaining the two calling JSP pages. Same columns as FailReport. `UnitDAO unitDAO` instantiated but never used. `Vector` imported but never used. |

**Same documentation pattern as EmailPreOpChkFailReport. Counterpart that shows all results rather than failures only.**

### 2.20 EmailRestictedAccessUsageReport.java (190 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailRestictedAccessUsageReport.java` |
| **Lines** | 190 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (7-param, `String[] args, String dir`) -- undocumented |
| **Public methods** | `createExcel()`, `createRestrictedAccessReport()`, `getFileName()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Restricted Access Usage Report". **Class name has typo: "Resticted" should be "Restricted"**. Uses `Databean_report` with `restricted_access_usage`. Uses `RestrictedAccessUsageBean`. Uses `CustomerDAO`. Headers: Equipment NO, Serial No, Hour Meter Starts/Finish, Service Hour From, Total Usage. |
| **Deviation** | Class name typo. Has alternate constructor with `String[] args`. |

### 2.21 EmailSeatHourUtilReport.java (345 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java` |
| **Lines** | 345 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (no-arg, 7-param) -- undocumented |
| **Public methods** | `createExcel()` -- undocumented |
| **Private methods** | `createUtilReport()` -- undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Unit Utilisation Report". Uses `Databean_report` with `seat_hour`. Nearly identical to EmailKeyHourUtilReport. **Same subtitle label swap bug**: Customer=locName, Site=deptName, Dept=custName (lines 104-106). **Copy-paste bug**: lines 165-196 set cell values all to `vutil1.get(i)` instead of `vutil2`, `vutil3`, etc. -- only the formula references the correct `vutilN` while the displayed string value is always `vutil1`. `Vector` imported but never used. `FormulaEvaluator` instantiated but never used. |
| **Deviation** | Same subtitle swap bug as EmailKeyHourUtilReport. Copy-paste bug on cell values. `createUtilReport()` is private. |

### 2.22 EmailServMaintenanceReport.java (438 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReport.java` |
| **Lines** | 438 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (7-param, `String[] args, String dir`) -- undocumented |
| **Public methods** | `init()`, `init2()`, `createExcel()`, `createEmail()`, `createServMaintenanceReport()`, `createBody()`, `getFileName()`, `getBody()` -- **8 public methods, ALL undocumented** |
| **Method Javadoc** | NONE except line 158: `//Generates Email with report body and excel attachment` |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **Reading evidence** | Title = "Service Report". Uses `Databean_report` with `serv_hour`/`serv_hour_new` and `ServiceDueFlagBean` with `service_flag_new`. Has dual init (init uses `serv_hour`, init2 uses `serv_hour_new`). Has `createEmail()` flow with HTML body and `createBody()` that generates service report email with color-coded legend. Extensive service calculation logic using `DataUtil` methods (`addMonthToDate`, `calculateLastServTypeCO`, `calculateNextServTypeDue`, `getColourStatus`). Instance-level fields for intermediate data. Color-coded "Hours to Next Service" cells (red/green/orange). `UnitDAO unitDAO` instantiated but never used. |
| **Deviation from pattern** | Most complex file in the set: dual init, HTML email body generation, service calculation logic, color-coded status, legend in email body. Same lifecycle pattern as EmailDriverAccessAbuseReport. |

### 2.23 EmailServMaintenanceReportNew.java (256 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReportNew.java` |
| **Lines** | 256 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createServMaintenanceReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Service Report". Uses `Databean_report` with `serv_hour` and `ServiceDueFlagBean` with `service_flag` (not `service_flag_new` -- naming contradiction given the "New" class name). Simpler than EmailServMaintenanceReport: no dual init, no HTML email body. All logic in `createServMaintenanceReport()`. Same color-coded service status. Missing "Serial No" header compared to the original report. `UnitDAO unitDAO` instantiated but never used. |
| **Deviation** | Simpler version of EmailServMaintenanceReport. Uses `service_flag` (not `_new`) despite the class being named "New". |

### 2.24 EmailSuperMasterAuthReport.java (211 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSuperMasterAuthReport.java` |
| **Lines** | 211 |
| **Class Javadoc** | NONE |
| **Constructors** | 2 (7-param, `String[] args, String dir`) -- undocumented |
| **Public methods** | `createExcel()`, `createSuperMasterAuthReport()`, `getFileName()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "On-Demand Authentication Report" (rptTitle), but sheet tab = "On-Demand Authorisation Report " (with trailing space, and UK spelling vs US). Uses `Databean_report` with `super_master_auth`. Uses `SuperMasterAuthReportBean` and `SuperMasterAuthBean`. `CustomerDAO` instantiated to get model name. Groups rows by fleet number, only showing fleet/serial on first occurrence. |
| **Deviation** | Title inconsistency: "Authentication" (rptTitle) vs "Authorisation" (sheet tab, line 112). Has alternate constructor. |

### 2.25 EmailUnitUnlockReport.java (191 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUnitUnlockReport.java` |
| **Lines** | 191 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createBroadcastMsgReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Machine Unlock Report". Uses `Databean_report` with `rpt_unlock`. Method named `createBroadcastMsgReport()` but actually creates an unlock report -- **naming mismatch** (likely copy-paste from EmailBroadcastMsgReport). Has lockout type filter mapping (codes 251-254 to descriptive names). Has optional filter for unconfirmed impacts and missing reasons. Shows "Is This A Real Impact" column conditionally. |
| **Deviation** | Method name `createBroadcastMsgReport()` is misleading for an unlock report. |

### 2.26 EmailUtilisationReport.java (256 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java` |
| **Lines** | 256 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createUtilReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Site Utilisation Report". Uses `Databean_report` with `util_rpt`. Uses `UnitUtilSummaryBean`. Shows Hours Available, Logged on Hours (+ %), Seat Hours (+ %), Traction Hours (+ %), Hydraulic Hours (+ %). Total row with `setTotalDuration`. Commented-out `System.out.println` debug lines (57, 62). `Date` and `SimpleDateFormat` imported but never used. `UnitDAO unitDAO` instantiated but never used. |

**Same documentation pattern as EmailBatteryReport.**

### 2.27 EmailUtilWowReport.java (133 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilWowReport.java` |
| **Lines** | 133 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createCurrReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title = "Unit Utilisation by Hour Report". Uses `Databean_report` with two op codes: `util_wow_dtl` (first init) and `email_util_wow` (second init). Embeds a utilisation chart image via `addImageUtilisationChart()`. Multiple unused local variables: `customer`, `location`, `department`, `model`, `avatruck`, `utilmodelbean`. `UnitDAO unitDAO` instantiated but never used. Method named `createCurrReport()` but report is about utilisation -- naming unclear. |
| **Deviation** | Generates chart-based report (unique among the 28). Multiple unused variables. Two-phase `Databean_report` initialization. |

### 2.28 EmailVorReport.java (335 lines)

| Item | Detail |
|---|---|
| **File** | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailVorReport.java` |
| **Lines** | 335 |
| **Class Javadoc** | NONE |
| **Constructors** | 1 (7-param) -- undocumented |
| **Public methods** | `createExcel()`, `createVorReport()` -- all undocumented |
| **Method Javadoc** | NONE |
| **Duplicate import** | `java.util.ArrayList` imported twice |
| **TODO/FIXME/HACK/XXX** | NONE |
| **Reading evidence** | Title set as "Detailed Report by Unit" in constructor (line 24) but sheet tab = "Vor Report" (line 131) -- **title mismatch**. Uses `Databean_dyn_reports` with `vor_report`. Uses `vor_flag = "1"` hardcoded. Nearly identical structure to EmailDynUnitReport but includes "Times Enabled" column and Start/End Time columns use `VALUE()` formula. `UnitDAO unitDAO` instantiated but never used. `FormulaEvaluator` imported but never used. |
| **Deviation** | Title mismatch. Very similar to EmailDynUnitReport with VOR-specific additions. |

---

## 3. Consolidated Findings

### 3.1 Documentation Deficit -- All 28 Files

| Metric | Count |
|---|---|
| **Files with class-level Javadoc** | 0 / 28 |
| **Files with ANY method-level Javadoc** | 0 / 28 |
| **Total public methods across all files** | ~75 |
| **Documented public methods** | 0 / ~75 |
| **Files with TODO/FIXME/HACK/XXX** | 0 / 28 |
| **Files with duplicate `ArrayList` import** | 19 / 28 |
| **Files with unused `UnitDAO` instantiation** | 21 / 28 |

### 3.2 Undocumented Public Methods (Complete List by File)

All 28 files have zero Javadoc. The following lists all public methods:

| File | Undocumented Public Methods |
|---|---|
| EmailBatteryReport | `createExcel()`, `createBatteryReport()`, `getFileName()` |
| EmailBroadcastMsgReport | `createExcel()`, `createBroadcastMsgReport()` |
| EmailCimplicityShockReport | `createExcel()`, `createCimplicityShockReport()` |
| EmailCimplicityUtilReport | `createExcel()`, `createCimplicityUtilisationReport()` |
| EmailCurrDrivReport | `createExcel()`, `createCurrDrivReport()` |
| EmailCurrUnitReport | `createExcel()`, `createCurrUnitReport()` |
| EmailDailyVehSummaryReport | `createExcel()`, `createDSumReport()` |
| EmailDriverAccessAbuseReport | `init()`, `init2()`, `createExcel()`, `createEmail()`, `createAbuseReport()`, `createBody()`, `getFileName()`, `getBody()` |
| EmailDriverImpactReport | `createExcel()`, `createDrivImpReport()` |
| EmailDriverLicenceExpiry | `createExcel()`, `createLicenceExpiryReport()` |
| EmailDynDriverReport | `createExcel()`, `createDynDriverReport()` |
| EmailDynSeenReport | `createExcel()`, `createDynUnitReport()` |
| EmailDynUnitReport | `createExcel()`, `createDynUnitReport()` |
| EmailHireDehireReport | `createExcel(String,String,String)`, `createHireDehireReport(String,String,String)`, `getFileName()` |
| EmailImpactMeterReport | `createExcel()`, `createImpactReport()` |
| EmailImpactReport | `createExcel()`, `createImpactReport()` |
| EmailKeyHourUtilReport | `createExcel()` |
| EmailPreOpChkFailReport | `createExcel()`, `createPreOpFailReport()` |
| EmailPreOpChkReport | `createExcel()`, `createPreOpReport()` |
| EmailRestictedAccessUsageReport | `createExcel()`, `createRestrictedAccessReport()`, `getFileName()` |
| EmailSeatHourUtilReport | `createExcel()` |
| EmailServMaintenanceReport | `init()`, `init2()`, `createExcel()`, `createEmail()`, `createServMaintenanceReport()`, `createBody()`, `getFileName()`, `getBody()` |
| EmailServMaintenanceReportNew | `createExcel()`, `createServMaintenanceReport()` |
| EmailSuperMasterAuthReport | `createExcel()`, `createSuperMasterAuthReport()`, `getFileName()` |
| EmailUnitUnlockReport | `createExcel()`, `createBroadcastMsgReport()` |
| EmailUtilisationReport | `createExcel()`, `createUtilReport()` |
| EmailUtilWowReport | `createExcel()`, `createCurrReport()` |
| EmailVorReport | `createExcel()`, `createVorReport()` |

### 3.3 Naming / Accuracy Issues Found

| File | Issue |
|---|---|
| EmailBroadcastMsgReport | Constructor title "Machine Unlock Report" does not match report content "Broadcast Message Report" |
| EmailDriverLicenceExpiry | Typo "LIcence" (uppercase I) repeated 3 times in title strings |
| EmailDynSeenReport | Method `createDynUnitReport()` does not match report purpose (Pedestrian Detection) |
| EmailUnitUnlockReport | Method `createBroadcastMsgReport()` does not match report purpose (Machine Unlock) |
| EmailRestictedAccessUsageReport | Class name typo: "Resticted" should be "Restricted" |
| EmailSuperMasterAuthReport | Title inconsistency: "Authentication" (rptTitle) vs "Authorisation" (sheet tab) |
| EmailVorReport | Constructor title "Detailed Report by Unit" does not match sheet tab "Vor Report" |
| EmailUtilWowReport | Method `createCurrReport()` does not reflect utilisation report purpose |
| EmailKeyHourUtilReport | Subtitle labels swapped: Customer=locName, Site=deptName, Dept=custName |
| EmailSeatHourUtilReport | Same subtitle label swap bug as EmailKeyHourUtilReport |
| EmailSeatHourUtilReport | Copy-paste bug: all cell string values reference `vutil1` instead of `vutil2..vutil8` |

### 3.4 Structural Deviations from Standard Pattern

| File | Deviation |
|---|---|
| EmailDriverAccessAbuseReport | Dual init methods, HTML email body via `createBody()`, `createEmail()` flow |
| EmailServMaintenanceReport | Dual init methods, HTML email body via `createBody()`, `createEmail()` flow, color-coded service status |
| EmailHireDehireReport | Completely different constructor (`docRoot, fileName, bean`), different `createExcel()` signature |
| EmailUtilWowReport | Chart-based report, two-phase Databean init, multiple unused variables |
| EmailImpactMeterReport / EmailImpactReport | Include image embedding from external URL |

---

## 4. Commented-Out Code Inventory

| File | Lines | Content |
|---|---|---|
| EmailBatteryReport | 101 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| EmailCurrDrivReport | 99-101 | Conditional dept header (commented out) |
| EmailDynDriverReport | 71 | `//dbreport.setSet_form_cd(form_cd);` |
| EmailDynUnitReport | 76, 281-283, 323-326, 344-346 | Old `TIME()` formula approach |
| EmailDriverImpactReport | 64, 69-79 | Old `filter` variable references |
| EmailDriverAccessAbuseReport | 83 | Old `ArrayList a_driv_id = filter.getA_driv_id();` |
| EmailUtilisationReport | 57, 62 | `System.out.println` debug lines |
| Multiple files | various | `//adjust first column width: sheet.autoSizeColumn(0);` (boilerplate) |

---

## 5. Unused Import / Instantiation Summary

| Pattern | Affected Files (count) |
|---|---|
| `java.util.ArrayList` imported twice | 19 files |
| `UnitDAO unitDAO` instantiated but never used | 21 files |
| `FormulaEvaluator` imported/instantiated, never used for evaluation | 5 files |
| `Vector` imported but never used | 2 files (PreOpChkReport, PreOpChkFailReport) |
| `DecimalFormat` imported but never used | 2 files (ImpactReport, ImpactMeterReport) |
| `java.sql.Date`, `SimpleDateFormat` imported but never used | 1 file (EmailUtilisationReport) |
| `java.util.Arrays` imported but never used | 3 files |

---

*End of Pass 3 documentation audit for excel/reports Email classes.*
