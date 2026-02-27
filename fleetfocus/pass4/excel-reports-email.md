# Pass 4 -- Code Quality: excel/reports Email*.java (28 files)

**Auditor:** A10
**Date:** 2026-02-25
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/Email*.java` (28 files)
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## 1. Structural Overview

All 28 files follow a copy-paste pattern. Each class extends `Frm_excel` and implements the same boilerplate:

1. Constructor(s) calling `super(...)` and `setTitle(...)`.
2. `createExcel()` method that calls a report-specific builder, writes `wb` to a `FileOutputStream`, and returns the result path.
3. A `create<ReportName>Report()` method that sets up the `Databean`, builds subtitle arrays, creates headers, and iterates over data to populate cells.

There is **no shared abstract template or strategy pattern**. All 28 files duplicate the same structural skeleton with only the databean opcode, column headers, and cell-population logic varying. This is the single most severe code-quality finding across this file set.

---

## 2. Systemic Issues (Present Across All or Nearly All 28 Files)

### 2.1 Massive Copy-Paste Duplication (CRITICAL)

Every file duplicates:
- The `createExcel()` method (FileOutputStream open/write/close pattern) -- identical in all 28 files.
- The `cust_cd`/`loc_cd`/`dept_cd` normalization block (`"0"` to `""` or `"all"`) -- identical in all 28 files.
- Subtitle array construction (`"FleetFocus Reporting System"`, start/end time, customer, site, dept, report title) -- structurally identical in all 28.
- Header row creation loop (`for (int i = 0; i < headerLst.size()...`) -- identical in all 28.
- Row declaration and blank-row creation pattern (`row = sheet.createRow(currentRow); currentRow++; row = sheet.createRow(currentRow++);`) -- identical in all 28.
- Cell population pattern (`contentCell = row.createCell(m++); contentCell.setCellValue(...); contentCell.setCellStyle(...)`) -- structurally identical across all.

**Evidence:** Compare any two files, e.g., `EmailBatteryReport.java` lines 33-42 vs. `EmailBroadcastMsgReport.java` lines 24-33 -- the `createExcel()` body is character-for-character identical.

### 2.2 Resource Leak in `createExcel()` (HIGH -- All 28 Files)

Every `createExcel()` method opens a `FileOutputStream` without a try-with-resources or try/finally block:

```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
```

If `wb.write(fileOut)` throws an exception, the `FileOutputStream` is never closed. This pattern exists in all 28 files.

**Affected files:** All 28.

### 2.3 Raw-Type `ArrayList` Usage (HIGH -- All 28 Files)

Nearly every file uses raw `ArrayList` without generics for data retrieved from `Databean_report` or `Databean_dyn_reports`:

```java
ArrayList vunit_name = dbreport.getVunit_name();
ArrayList vunit_battery = dbreport.getVunit_battery();
```

These are then cast with `(String)` at usage sites, producing unchecked cast warnings and no type safety.

**Affected files:** All 28 except `EmailHireDehireReport` (which still uses raw `ArrayList` for its bean fields).

### 2.4 Unused Local Variable: `UnitDAO unitDAO` (HIGH -- 19 Files)

A `UnitDAO unitDAO = new UnitDAO()` is instantiated but never used in 19 of 28 files. This creates an unnecessary object and is dead code.

**Affected files:**
- EmailBroadcastMsgReport
- EmailCimplicityShockReport
- EmailCimplicityUtilReport
- EmailCurrDrivReport
- EmailCurrUnitReport
- EmailDailyVehSummaryReport
- EmailDriverLicenceExpiry
- EmailDynDriverReport
- EmailDynSeenReport
- EmailDynUnitReport
- EmailImpactMeterReport
- EmailImpactReport
- EmailKeyHourUtilReport
- EmailPreOpChkFailReport
- EmailPreOpChkReport
- EmailServMaintenanceReport
- EmailServMaintenanceReportNew
- EmailUtilisationReport
- EmailUtilWowReport

### 2.5 Duplicate Import: `import java.util.ArrayList;` Appears Twice (MEDIUM -- 16 Files)

The import `java.util.ArrayList` is listed twice in the import block.

**Affected files:**
- EmailBatteryReport
- EmailCimplicityShockReport
- EmailCimplicityUtilReport
- EmailCurrDrivReport
- EmailCurrUnitReport
- EmailDailyVehSummaryReport
- EmailDriverAccessAbuseReport
- EmailDriverImpactReport
- EmailDriverLicenceExpiry
- EmailDynDriverReport
- EmailDynSeenReport
- EmailDynUnitReport
- EmailServMaintenanceReport
- EmailServMaintenanceReportNew
- EmailUtilisationReport
- EmailVorReport

### 2.6 Commented-Out Code: `//adjust first column width: sheet.autoSizeColumn(0);` (LOW -- 24 Files)

This identical commented-out line appears in 24 of 28 files, indicating dead code that was mass-copied and never cleaned up.

**Additional commented-out code blocks:**
- `EmailCurrDrivReport` lines 99-101: commented-out conditional dept column logic.
- `EmailDriverImpactReport` line 64: `//dbreport.setSet_form_cd(form_cd);`
- `EmailDriverImpactReport` lines 69-79: large block of commented-out old filter references.
- `EmailDynDriverReport` line 71: `//dbreport.setSet_form_cd(form_cd);`
- `EmailDynSeenReport` line 75: `//dbreport.setSet_form_cd(form_cd);`
- `EmailDynUnitReport` line 76: `//dbreport.setSet_form_cd(form_cd);`
- `EmailDynUnitReport` lines 281-283, 323-325, 344-346: three blocks of commented-out evaluator/formula code.
- `EmailUtilisationReport` lines 57, 62: commented-out `System.out.println` debug statements.
- `EmailImpactReport` line 218: stray `//` comment.
- `EmailImpactMeterReport` line 225: stray `//` comment.
- `EmailDriverAccessAbuseReport` lines 83, 128: commented-out `// ArrayList a_driv_id = filter.getA_driv_id();` (duplicated in both `init()` and `init2()`).

---

## 3. Per-File Deviations and Specific Issues

### 3.1 EmailBatteryReport.java (152 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | `CustomerDAO customerDao` instantiated at line 70, used only for `getModelName()` at line 80; could be a static utility call | LOW | Line 70 |
| 2 | Title variable `static String t` -- poor naming, non-final | LOW | Line 20 |
| 3 | Title `t` is `static` but set via `setTitle(t)` -- mutable shared state risk | MEDIUM | Line 20 |

### 3.2 EmailBroadcastMsgReport.java (148 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Title set as `"Machine Unlock Report"` at line 21, but tab title is `"Broadcast Message Report"` at line 63 -- title mismatch (potential bug) | HIGH | Lines 21 vs 63 |

### 3.3 EmailCimplicityShockReport.java (167 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | `static String rptTitle` -- non-final mutable static | LOW | Line 19 |
| 2 | Two constructors (1-arg formName, 2-arg) -- second ignores `formName` param | LOW | Lines 25-28 |

### 3.4 EmailCimplicityUtilReport.java (165 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Local variable `String style = "cell_b_normal_time"` declared at line 45 but not used until line 163 | LOW | Line 45 |
| 2 | Loop at lines 136-138 iterates fields but overwrites `temp` each iteration, only keeping the last value -- likely logic bug | HIGH | Lines 136-138 |

### 3.5 EmailCurrDrivReport.java (142 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused local variables: `vveh_cd`, `vveh_id`, `vveh_typ_cd` (declared lines 63-66, never read) | MEDIUM | Lines 63-66 |
| 2 | Commented-out dept column logic at lines 99-101 | LOW | Lines 99-101 |

### 3.6 EmailCurrUnitReport.java (148 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused local variables: `vveh_cd`, `vveh_id`, `vveh_typ_cd` (declared lines 64-67, never read) | MEDIUM | Lines 64-67 |

### 3.7 EmailDailyVehSummaryReport.java (330 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Longest file at 330 lines; single monolithic method `createDSumReport()` is 295 lines | HIGH | Lines 35-328 |
| 2 | Total row at lines 294-327 unconditionally writes 8 columns including seat/traction/hydraulic, but header columns are conditional on `cust_type` -- potential column misalignment | HIGH | Lines 294-327 vs 139-153 |
| 3 | Import `RuntimeConf` used for customer type checks -- tightly coupled to runtime configuration | LOW | Line 16 |

### 3.8 EmailDriverAccessAbuseReport.java (355 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Two nearly identical methods: `init()` and `init2()` -- lines 49-95 vs 97-140. Massive internal duplication | HIGH | Lines 49-140 |
| 2 | Field `dbreport` declared as instance variable at line 21 but shadowed by local `dbreport` in both `init()` line 59 and `init2()` line 104 | MEDIUM | Lines 21, 59, 104 |
| 3 | Field `customerDao` declared at line 23 but never used | MEDIUM | Line 23 |
| 4 | `createBody()` method builds HTML using string concatenation with `body.append("<td>"+tmp+"</td>")` -- XSS vulnerability (no HTML escaping of data values) | HIGH | Lines 283-345 |
| 5 | Unused import: second `ArrayList` import (duplicate) | LOW | Line 8 |

### 3.9 EmailDriverImpactReport.java (178 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused import: `java.util.Arrays` | LOW | Line 7 |
| 2 | Unused local: `FormulaEvaluator evaluator` declared at line 129, never used | MEDIUM | Line 129 |
| 3 | Large block of commented-out code at lines 69-79 | LOW | Lines 69-79 |

### 3.10 EmailDriverLicenceExpiry.java (115 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | **Typo in title:** `"Driver LIcence Expiry Report"` (uppercase I in "LIcence") -- appears 3 times at lines 21, 68, 72 | MEDIUM | Lines 21, 68, 72 |
| 2 | Class name does not end in "Report" unlike all other 27 files -- naming inconsistency | LOW | Line 17 |

### 3.11 EmailDynDriverReport.java (314 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused import: `java.util.Arrays` | LOW | Line 7 |
| 2 | Nearly identical StringTokenizer field-hide logic as `EmailDynUnitReport` and `EmailVorReport` -- triplicated code | HIGH | Lines 106-126 |
| 3 | Variable `vrpt_veh_value_stopv` at line 84 is an exact duplicate of `vrpt_veh_value_stop` at line 82 (same getter called twice) | MEDIUM | Lines 82, 84 |

### 3.12 EmailDynSeenReport.java (243 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused import: `java.util.Arrays` | LOW | Line 7 |
| 2 | Unused local: `vfld_hide` ArrayList declared at line 94, never read | MEDIUM | Line 94 |
| 3 | Unused local: `String vor_flag` declared at line 41, never used | LOW | Line 41 |
| 4 | `fld_hide[]` array is populated but never actually checked in the cell-writing loop (lines 229-235 always write all fields) | HIGH | Lines 96-101 vs 229-235 |
| 5 | Unused import: `FormulaEvaluator` | LOW | Line 12 |

### 3.13 EmailDynUnitReport.java (351 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused import: `java.util.Arrays` | LOW | Line 7 |
| 2 | Large blocks of commented-out evaluator code at lines 281-283, 323-325, 344-346 | LOW | Multiple |
| 3 | Duplicate variable `vrpt_veh_value_stopv` at line 89 (same getter as line 87) | MEDIUM | Lines 87, 89 |
| 4 | Unused import: `FormulaEvaluator` (evaluator code is commented out) | LOW | Line 12 |

### 3.14 EmailHireDehireReport.java (133 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Different constructor signature from all other 27 files -- takes `(String docRoot, String fileName, HireDehireReportBean)` instead of standard 7-param pattern | LOW | Line 18 |
| 2 | `createExcel()` takes parameters `(String st, String et, String sc)` unlike all other files | LOW | Line 23 |
| 3 | Title set with `.xlsx` extension appended: `setTitle(tabTitle+".xlsx")` at line 58 -- unique inconsistency | LOW | Line 58 |
| 4 | `import java.io.File` used at line 3 for `new File(docroot).mkdirs()` at line 30 -- only file that does directory creation | LOW | Lines 3, 28-32 |

### 3.15 EmailImpactMeterReport.java (229 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | **Near-complete duplication of `EmailImpactReport.java`** -- the two files differ only in: (a) an extra "Impact Data" column, (b) meter percentage display in severity text. Lines 42-224 are ~95% identical to `EmailImpactReport` lines 42-220 | CRITICAL | Entire file |
| 2 | Unused import: `DecimalFormat` | LOW | Line 6 |
| 3 | Hardcoded URL: `"http://fleetfocus.lindemh.com.au/fms/"+ RuntimeConf.impactDir` at line 204 | MEDIUM | Line 204 |
| 4 | Unused locals: `veh_cd`, `veh_nm`, `veh_typ_nm1` (declared lines 80-82, never read) | MEDIUM | Lines 80-82 |
| 5 | Double semicolon: `dbreport.setReport_filter(rpt_filter);;` at line 77 | LOW | Line 77 |

### 3.16 EmailImpactReport.java (222 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused import: `DecimalFormat` | LOW | Line 6 |
| 2 | Hardcoded URL: `"http://fleetfocus.lindemh.com.au/fms/"+ RuntimeConf.impactDir` at line 197 | MEDIUM | Line 197 |
| 3 | Unused locals: `veh_cd`, `veh_nm`, `veh_typ_nm1` (declared lines 80-82, never read) | MEDIUM | Lines 80-82 |
| 4 | Double semicolon: `dbreport.setReport_filter(rpt_filter);;` at line 77 | LOW | Line 77 |

### 3.17 EmailKeyHourUtilReport.java (345 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | **Near-complete duplication of `EmailSeatHourUtilReport.java`** -- same structure, same column layout, only opcode differs (`key_hour` vs `seat_hour`) | CRITICAL | Entire file |
| 2 | Subtitle fields swapped: `{"Customer", locName}`, `{"Site", deptName}`, `{"Dept", custName}` at lines 112-114 -- **values are in wrong positions (bug)** | CRITICAL | Lines 112-114 |
| 3 | Unused local: `FormulaEvaluator evaluator` declared at line 40, never used | MEDIUM | Line 40 |
| 4 | Total row at lines 213-258 is missing the "Serial No" column compared to data rows (data rows have 3 text columns, total row only has 2 before times) -- potential column misalignment | HIGH | Lines 213-258 |

### 3.18 EmailPreOpChkFailReport.java (224 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused import: `java.util.Arrays` | LOW | Line 7 |
| 2 | Unused import: `java.util.Vector` | LOW | Line 8 |
| 3 | Unused local: `FormulaEvaluator evaluator` declared at line 117, never used | MEDIUM | Line 117 |
| 4 | Heavy duplication with `EmailPreOpChkReport.java` -- same column structure, differs only in the filtering condition (`fail1 != "-"` guard) | HIGH | Entire file |

### 3.19 EmailPreOpChkReport.java (231 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused import: `java.util.Vector` | LOW | Line 7 |
| 2 | Redundant `if (params.length == 4)` outer check at line 40 contains inner checks `if (params.length > 1)`, `if (params.length > 2)`, `if (params.length > 3)` which are always true when outer is true | LOW | Lines 40-51 |

### 3.20 EmailRestictedAccessUsageReport.java (189 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | **Class name misspelling:** `EmailRestictedAccessUsageReport` -- missing 'r' in "Restricted" | MEDIUM | Line 19 |
| 2 | Unused local variable `temp` declared at line 150, never read | LOW | Line 150 |
| 3 | Unused locals: `get_user`, `form_nm` (declared lines 95, 99) | MEDIUM | Lines 95, 99 |
| 4 | Unused import: `java.io.File` | LOW | Line 3 |

### 3.21 EmailSeatHourUtilReport.java (344 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | **Copy-paste bug:** Lines 165, 170, 175, 180, 185, 190, 195 all write `vutil1.get(i).toString()` as the cell *value* (the formula uses the correct `vutil2`..`vutil8`, but the display value is always `vutil1`) | CRITICAL | Lines 165-196 |
| 2 | Same bug repeats in the un-utilised section at lines 298-330 | CRITICAL | Lines 298-330 |
| 3 | Subtitle fields swapped same as EmailKeyHourUtilReport: `{"Customer", locName}`, `{"Site", deptName}`, `{"Dept", custName}` at lines 104-106 -- **values in wrong positions (bug)** | CRITICAL | Lines 104-106 |
| 4 | Unused import: `java.util.Vector` | LOW | Line 7 |
| 5 | Unused local: `FormulaEvaluator evaluator` declared at line 130, never used | MEDIUM | Line 130 |

### 3.22 EmailServMaintenanceReport.java (438 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Longest file at 438 lines. Two near-identical `init()`/`init2()` methods (lines 56-101 vs 103-144) | HIGH | Lines 56-144 |
| 2 | Instance field `customerDao` declared at line 26, never used | MEDIUM | Line 26 |
| 3 | `createBody()` builds HTML with no escaping of data values -- XSS risk | HIGH | Lines 347-428 |
| 4 | Heavy duplication with `EmailServMaintenanceReportNew.java` | HIGH | Entire report generation logic |
| 5 | Multiple instance-level `ArrayList` fields at lines 28-42 -- unusual; other files use locals | LOW | Lines 28-42 |

### 3.23 EmailServMaintenanceReportNew.java (255 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Near-complete duplication of `EmailServMaintenanceReport.java`'s report creation method | HIGH | Entire file |
| 2 | Uses `"service_flag"` opcode at line 68 vs `"service_flag_new"` in the older file -- the "New" suffix in the class name is the only differentiator | LOW | Line 68 |
| 3 | Total row at lines 205-253 writes 10 empty cells individually instead of using a loop | LOW | Lines 205-253 |

### 3.24 EmailSuperMasterAuthReport.java (210 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Title mismatch: `rptTitle` = `"On-Demand Authentication Report"` but `tabTitle` = `"On-Demand Authorisation Report "` (trailing space, and "Authentication" vs "Authorisation") | MEDIUM | Lines 21 vs 112 |
| 2 | Unused locals: `get_user`, `get_loc`, `get_dep`, `form_nm` (declared lines 101-105) | MEDIUM | Lines 101-105 |
| 3 | `CustomerDAO customerDAO` instantiated at line 117 but never used (model name retrieved from `get_mod` which comes from `dbreport`) | MEDIUM | Line 117 |

### 3.25 EmailUnitUnlockReport.java (190 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Method name `createBroadcastMsgReport()` at line 32 -- misleading; this is the Unlock report, not Broadcast | HIGH | Line 32 |
| 2 | Missing `else` before last `if` at line 103: `} if (rptFilter.equalsIgnoreCase("both")){` -- functionally a fall-through bug where `optFilter` can be overwritten | HIGH | Line 103 |

### 3.26 EmailUtilisationReport.java (255 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused imports: `java.sql.Date`, `java.text.ParseException`, `java.text.SimpleDateFormat` | LOW | Lines 6-8 |
| 2 | Unused local: `FormulaEvaluator evaluator` | MEDIUM | (implicit from import) |
| 3 | Commented-out `System.out.println` debug lines at lines 57, 62 | LOW | Lines 57, 62 |
| 4 | Mutates inherited field `from` and `to` via `substring(0,10)` at lines 59-60 -- side effect that could affect callers | MEDIUM | Lines 59-60 |

### 3.27 EmailUtilWowReport.java (132 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Unused locals: `utilmodelbean`, `customer`, `location`, `department`, `model`, `avatruck` (declared lines 105-110, never used) | MEDIUM | Lines 105-110 |
| 2 | Unused import from `UtilModelBean` (line 14) only used for dead local | LOW | Line 14 |
| 3 | Calls `dbreport.init()` twice (lines 78 and 101) with different opcodes on the same bean instance -- relies on re-initialization behavior | MEDIUM | Lines 78, 101 |

### 3.28 EmailVorReport.java (334 lines)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | Structurally near-identical to `EmailDynUnitReport.java` -- same StringTokenizer/fld_hide pattern, same nested loop structure, adds only "Times Enabled" and "VOR count" columns | HIGH | Entire file |
| 2 | Duplicate variable `vrpt_veh_value_stopv` at line 86 (same getter as line 84) | MEDIUM | Lines 84, 86 |
| 3 | Unused import: `java.util.Arrays` | LOW | Line 7 |

---

## 4. Summary of Unused Import Audit

| Import | Files Where Unused |
|--------|-------------------|
| `java.util.ArrayList` (duplicate) | 16 files (see section 2.5) |
| `java.util.Arrays` | EmailDriverImpactReport, EmailDynDriverReport, EmailDynSeenReport, EmailDynUnitReport, EmailPreOpChkFailReport, EmailVorReport |
| `java.util.Vector` | EmailPreOpChkFailReport, EmailPreOpChkReport, EmailSeatHourUtilReport |
| `java.text.DecimalFormat` | EmailImpactMeterReport, EmailImpactReport |
| `java.sql.Date` | EmailUtilisationReport |
| `java.text.ParseException` | EmailUtilisationReport |
| `java.text.SimpleDateFormat` | EmailUtilisationReport |
| `java.io.File` | EmailRestictedAccessUsageReport |
| `o.a.p.ss.usermodel.FormulaEvaluator` | EmailDynSeenReport (evaluator code absent), EmailDynUnitReport (evaluator code commented out) |
| `com.torrent...dao.UnitDAO` | 19 files (instantiated but never used -- see section 2.4) |
| `com.torrent...dao.CustomerDAO` | EmailDriverAccessAbuseReport (field never used), EmailSuperMasterAuthReport (local never used) |
| `com.torrent...UtilModelBean` | EmailUtilWowReport (used only for dead local) |

---

## 5. Summary of Confirmed or Likely Bugs

| # | File | Bug | Severity |
|---|------|-----|----------|
| 1 | EmailSeatHourUtilReport | Cell values always display `vutil1` instead of `vutil2`-`vutil8` (copy-paste error) | CRITICAL |
| 2 | EmailKeyHourUtilReport | Subtitle labels Customer/Site/Dept have swapped values (locName, deptName, custName in wrong order) | CRITICAL |
| 3 | EmailSeatHourUtilReport | Same subtitle label swap as EmailKeyHourUtilReport | CRITICAL |
| 4 | EmailCimplicityUtilReport | Loop at lines 136-138 overwrites `temp` each iteration, only keeps last field value | HIGH |
| 5 | EmailBroadcastMsgReport | Constructor title "Machine Unlock Report" vs tab title "Broadcast Message Report" | HIGH |
| 6 | EmailUnitUnlockReport | Missing `else` before `if` at line 103 causes fall-through logic error | HIGH |
| 7 | EmailDynSeenReport | `fld_hide` array is populated but never checked in cell-writing loop (all fields always displayed) | HIGH |
| 8 | EmailSuperMasterAuthReport | Title string mismatch: "Authentication" vs "Authorisation" + trailing space | MEDIUM |
| 9 | EmailDriverLicenceExpiry | Typo: "LIcence" (uppercase I) in report title | MEDIUM |
| 10 | EmailRestictedAccessUsageReport | Class name misspelling: "Resticted" (missing 'r') | MEDIUM |

---

## 6. Duplication Clusters

The following groups of files are near-clones of each other and could be collapsed into parameterized implementations:

1. **EmailImpactReport + EmailImpactMeterReport** -- ~95% identical, differ only in one extra column and meter percentage display.
2. **EmailKeyHourUtilReport + EmailSeatHourUtilReport** -- ~90% identical, differ only in opcode (`key_hour` vs `seat_hour`) and tab title.
3. **EmailServMaintenanceReport + EmailServMaintenanceReportNew** -- same report creation logic, differ in opcode (`serv_hour` vs `serv_hour_new`) and whether email body is supported.
4. **EmailDynUnitReport + EmailVorReport** -- ~85% identical, VOR adds "Times Enabled" column and hardcodes `vor_flag`.
5. **EmailPreOpChkReport + EmailPreOpChkFailReport** -- same structure, Fail version adds a filter condition.
6. **EmailCurrDrivReport + EmailCurrUnitReport** -- same structure with different column order and opcode.

---

## 7. Hardcoded Values

| File | Value | Location |
|------|-------|----------|
| EmailImpactReport | `http://fleetfocus.lindemh.com.au/fms/` | Line 197 |
| EmailImpactMeterReport | `http://fleetfocus.lindemh.com.au/fms/` | Line 204 |
| All 28 files | `"FleetFocus Reporting System"` | Subtitle array |
| All 28 files | `"0"` as sentinel for "all" customer/location/dept | Parameter normalization block |

---

## 8. Aggregate Statistics

| Metric | Value |
|--------|-------|
| Total files | 28 |
| Total approximate lines | ~6,200 |
| Files with duplicate ArrayList import | 16 (57%) |
| Files with unused UnitDAO instantiation | 19 (68%) |
| Files with resource leak in createExcel() | 28 (100%) |
| Files with raw-type ArrayList usage | 28 (100%) |
| Files with commented-out code | 24 (86%) |
| Confirmed/likely bugs | 10 |
| Near-clone file pairs | 6 clusters |
| Unused imports (distinct types) | 12 different imports across the set |
