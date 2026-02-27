# Pass 4 -- Code Quality Audit: Excel Reports K-Z + Mail

**Audit Agent:** A12
**Date:** 2026-02-25
**Repository:** C:\Projects\cig-audit\repos\fleetfocus
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Pass:** 4 (Code Quality)
**Scope:** 16 files in `WEB-INF/src/com/torrent/surat/fms6/excel/reports/`

---

## Files Audited

| # | File | Lines |
|---|------|-------|
| 1 | ExcelKeyHourUtilReport.java | 358 |
| 2 | ExcelOperationalStatusReport.java | 160 |
| 3 | ExcelPreOpCheckFailReport.java | 384 |
| 4 | ExcelPreOpCheckReport.java | 204 |
| 5 | ExcelRestrictedUsageReport.java | 273 |
| 6 | ExcelSeatHourUtilReport.java | 358 |
| 7 | ExcelServMaintenanceReport.java | 273 |
| 8 | ExcelSpareModuleReport.java | 156 |
| 9 | ExcelSuperMasterAuthReport.java | 152 |
| 10 | ExcelUnitUnlockReport.java | 149 |
| 11 | ExcelUtilWOWReport.java | 174 |
| 12 | ExcelUtilWOWReportEmail.java | 181 |
| 13 | ExcelUtilisationReport.java | 230 |
| 14 | ExcelVorReport.java | 314 |
| 15 | MailBase.java | 129 |
| 16 | MailExcelReports.java | 46 |

---

## CQ-01: Code Duplication

### CQ-01.1 ExcelKeyHourUtilReport / ExcelSeatHourUtilReport -- Near-Identical Files

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| Files | `ExcelKeyHourUtilReport.java` (358 lines), `ExcelSeatHourUtilReport.java` (358 lines) |
| Evidence | Both files are structurally identical. They declare the same field lists (`veh_cd`, `veh_nm`, `veh_id`, `veh_typ_nm1`, `vutil1`..`vutil8`, `vutilt`, `vutilpt`, `util1`..`util8`, `utilt`), use the same `createExcel()` / `createUtilReport()` method structure, and differ only in the bean type (`KeyHourUtilBean` vs `SeatHourUtilBean`) and the tab title (`"Unit Utilisation Report"` vs `"Unit Utilisation Report - Seat"`). |

**ExcelKeyHourUtilReport.java lines 22-37:**
```java
public class ExcelKeyHourUtilReport extends Frm_excel{
    ArrayList veh_cd = new ArrayList();
    ArrayList veh_nm = new ArrayList();
    ArrayList veh_id = new ArrayList();
    ArrayList veh_typ_nm1 = new ArrayList();
    ArrayList vutil1 = new ArrayList();
    ...
```

**ExcelSeatHourUtilReport.java lines 20-35 (identical structure):**
```java
public class ExcelSeatHourUtilReport extends Frm_excel{
    ArrayList veh_cd = new ArrayList();
    ArrayList veh_nm = new ArrayList();
    ArrayList veh_id = new ArrayList();
    ArrayList veh_typ_nm1 = new ArrayList();
    ArrayList vutil1 = new ArrayList();
    ...
```

### CQ-01.2 ExcelUtilWOWReport / ExcelUtilWOWReportEmail -- Near-Identical Files

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| Files | `ExcelUtilWOWReport.java` (174 lines), `ExcelUtilWOWReportEmail.java` (181 lines) |
| Evidence | `ExcelUtilWOWReportEmail` is a copy of `ExcelUtilWOWReport` with the only addition being a `LindeConfig.siteName` check (line 94) that wraps the data loop in an AU-specific image branch vs the original table-based output. The entire data-loop body (lines 111-172 in Email version) is a verbatim copy of lines 104-165 in the non-Email version. |

**ExcelUtilWOWReport.java lines 104-115:**
```java
for (int i = 0; i < util.size(); i++) {
    utilmodelbean = (UtilModelBean) util.get(i);
    customer = utilmodelbean.getCustomer();
    location = utilmodelbean.getSite();
    ...
```

**ExcelUtilWOWReportEmail.java lines 111-126 (verbatim copy):**
```java
for (int i = 0; i < util.size(); i++) {
    utilmodelbean = (UtilModelBean) util.get(i);
    customer = utilmodelbean.getCustomer();
    location = utilmodelbean.getSite();
    ...
```

### CQ-01.3 ExcelPreOpCheckFailReport -- Internal Duplication Between Overloaded Methods

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| File | `ExcelPreOpCheckFailReport.java` |
| Lines | 64-221 vs 223-378 |
| Evidence | `createPreOpFailReport(cust,loc,dep,st,et)` (5-param) and `createPreOpFailReport(cust,loc,dep,st,et,form)` (6-param) are nearly identical -- both bodies contain the same 155+ lines of cell-population logic. The 6-param version differs only in minor style differences for a few cells. |

### CQ-01.4 createExcel() Boilerplate Across All 14 Excel Reports

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| Files | All 14 Excel report files |
| Evidence | Every file contains a nearly identical `createExcel()` method that follows this exact pattern: call the report builder, reset `currentRow`, create directory, open `FileOutputStream`, write workbook, close stream, return result. This 10-15 line pattern is duplicated across all 14 files and should be extracted to the base class `Frm_excel`. |

**Representative pattern (ExcelPreOpCheckReport.java lines 27-44):**
```java
public String createExcel(String cust, String loc, String dep, String st, String et) throws Exception{
    createPreOpReport(cust, loc, dep, st, et);
    currentRow =0;
    File docFile = new File(docroot);
    if( !docFile.exists() ){
        docFile.mkdirs();
    }
    FileOutputStream fileOut = new FileOutputStream(result);
    wb.write(fileOut);
    fileOut.close();
    return result;
}
```

### CQ-01.5 MailBase -- setMailHeader Overloads Duplicate HTML

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| File | `MailBase.java` |
| Lines | 5-62 vs 64-127 |
| Evidence | The two `setMailHeader()` overloads (6-param and 7-param) contain nearly identical HTML template strings. The 7-param version simply adds one additional `<tr>` for the "Model" field. The common HTML header/footer markup (~50 lines) is fully duplicated. |

---

## CQ-02: Naming Conventions

### CQ-02.1 Raw-Type ArrayList Field Names with Underscore/Abbreviation Style

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| Files | ExcelKeyHourUtilReport, ExcelSeatHourUtilReport, ExcelPreOpCheckReport, ExcelPreOpCheckFailReport, ExcelUnitUnlockReport, ExcelVorReport, ExcelUtilisationReport |
| Evidence | Field and variable names use inconsistent underscore-separated abbreviations that are not self-documenting: `veh_cd`, `veh_nm`, `veh_typ_nm1`, `vutil1`..`vutil8`, `vutilt`, `vutilpt`, `po_comp`, `sm_ser_st`, `sm_ser_ed2`, `vrpt_veh_typ_cd`, etc. |

**ExcelKeyHourUtilReport.java lines 23-37:**
```java
ArrayList veh_cd = new ArrayList();
ArrayList veh_nm = new ArrayList();
ArrayList veh_id = new ArrayList();
ArrayList veh_typ_nm1 = new ArrayList();
ArrayList vutil1 = new ArrayList();
...
ArrayList vutilpt= new ArrayList();
```

### CQ-02.2 Variable Names Starting with Uppercase

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| Files | ExcelVorReport.java (line 49), ExcelUtilisationReport.java (lines 45-51) |
| Evidence | Local variables begin with uppercase, violating Java naming conventions: `Vrpt_vor_count`, `Vgp_cd`, `Vgp_nm`, `Vuser_cd`, `Vuser_nm`, `Vloc_cd`, `Vloc_nm`, `StringTokenizer Tok`. |

**ExcelVorReport.java line 49:**
```java
ArrayList Vrpt_vor_count = dynBean.getVrpt_vor_count();
```

**ExcelUtilisationReport.java lines 45-51:**
```java
ArrayList Vgp_cd = utilBean.getGroup_cd();
ArrayList Vgp_nm = utilBean.getGroup_nm();
ArrayList Vuser_cd = utilBean.getUser_cd();
ArrayList Vuser_nm = utilBean.getUser_nm();
ArrayList Vloc_cd = utilBean.getLocation_cd();
ArrayList Vloc_nm = utilBean.getLocation_nm();
```

### CQ-02.3 Class Name `MailBase` Suggests Abstract but Is Concrete

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| File | `MailBase.java` |
| Evidence | The name `MailBase` implies it is a base class intended for inheritance, but it is a concrete class with only utility methods and no subclasses in this package. `MailExcelReports` does not extend `MailBase`. The parent class `Frm_excel` instantiates it as a utility object (`protected MailBase mb = new MailBase();` at line 62 of `Frm_excel.java`). |

---

## CQ-03: Commented-Out Code

### CQ-03.1 Commented autoSizeColumn Across Multiple Files

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| Files | ExcelKeyHourUtilReport (line 117), ExcelPreOpCheckFailReport (lines 97, 256), ExcelPreOpCheckReport (line 79), ExcelRestrictedUsageReport (line 71), ExcelSeatHourUtilReport (line 116), ExcelServMaintenanceReport (line 81), ExcelUnitUnlockReport (line 73), ExcelUtilWOWReport (line 79), ExcelUtilWOWReportEmail (line 80), ExcelUtilisationReport (line 91), ExcelVorReport (line 121) |
| Evidence | All files contain the same commented-out line: `//adjust first column width: sheet.autoSizeColumn(0);` |

### CQ-03.2 Commented protectSheet in ExcelUtilisationReport

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| File | `ExcelUtilisationReport.java` line 76 |
| Evidence | `//sheet.protectSheet(null);` |

---

## CQ-04: Unused Imports

### CQ-04.1 Duplicate Import of java.util.ArrayList

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| Files and Lines | ExcelKeyHourUtilReport (lines 7,9), ExcelSeatHourUtilReport (lines 7,8), ExcelServMaintenanceReport (lines 6,7), ExcelSuperMasterAuthReport (lines 6,7), ExcelUnitUnlockReport (lines 5,6), ExcelUtilisationReport (lines 5,6) |
| Evidence | `import java.util.ArrayList;` appears twice in each of these files. |

**ExcelKeyHourUtilReport.java lines 7,9:**
```java
import java.util.ArrayList;
import java.util.Date;
import java.util.ArrayList;
```

### CQ-04.2 Unused Imports

| File | Unused Import | Line |
|------|--------------|------|
| ExcelKeyHourUtilReport | `java.util.Date` | 8 |
| ExcelKeyHourUtilReport | `org.apache.poi.ss.formula.EvaluationCell` | 11 |
| ExcelKeyHourUtilReport | `org.apache.poi.ss.usermodel.FormulaEvaluator` | 13 |
| ExcelKeyHourUtilReport | `com.torrent.surat.fms6.excel.reports.beans.ImpactReportBean` | 19 |
| ExcelKeyHourUtilReport | `java.sql.SQLException` (declared but method signature covers it) | 6 |
| ExcelPreOpCheckFailReport | `java.util.Vector` | 6 |
| ExcelPreOpCheckFailReport | `org.apache.poi.ss.usermodel.FormulaEvaluator` (used only in 5-param overload) | 9 |
| ExcelPreOpCheckReport | `org.apache.poi.ss.usermodel.CellStyle` | 8 |
| ExcelPreOpCheckReport | `org.apache.poi.ss.usermodel.FormulaEvaluator` | 9 |
| ExcelPreOpCheckReport | `org.apache.poi.ss.util.CellRangeAddress` | 12 |
| ExcelSeatHourUtilReport | `org.apache.poi.ss.util.CellRangeAddress` | 14 |
| ExcelSuperMasterAuthReport | `com.torrent.surat.fms6.excel.reports.beans.DriverImpactReportBean` | 15 |
| ExcelUtilWOWReport | `com.torrent.surat.fms6.excel.reports.beans.PreOpCheckReportBean` | 14 |
| ExcelUtilWOWReportEmail | `com.torrent.surat.fms6.excel.reports.beans.PreOpCheckReportBean` | 14 |
| ExcelRestrictedUsageReport | `java.sql.SQLException` (declared in throws, but used) | 5 |
| MailExcelReports | `com.torrent.surat.fms6.util.RuntimeConf` | 7 |

---

## CQ-05: Empty / Broad Catch Blocks

### CQ-05.1 Empty Catch in ExcelOperationalStatusReport

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| File | `ExcelOperationalStatusReport.java` |
| Lines | 73-75 |
| Evidence | URLDecoder.decode exception is silently swallowed with no logging. |

```java
try {
    searchCrit = java.net.URLDecoder.decode(searchCrit, "UTF-8");
} catch (Exception e) {
    // If there's an error decoding, use the original value
}
```

### CQ-05.2 Broad `catch (Exception e)` in ExcelOperationalStatusReport

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| File | `ExcelOperationalStatusReport.java` |
| Line | 73 |
| Evidence | Catches generic `Exception` instead of the specific `UnsupportedEncodingException` that `URLDecoder.decode()` throws. |

---

## CQ-06: e.printStackTrace() Usage

### CQ-06.1 e.printStackTrace() in MailExcelReports

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| File | `MailExcelReports.java` |
| Lines | 22, 25, 38, 41 |
| Evidence | All four catch blocks use `e.printStackTrace()` with `// TODO Auto-generated catch block` comments, indicating they were never properly addressed. Both the `sendExcelReport` overloads exhibit this pattern. |

```java
} catch (AddressException e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
} catch (MessagingException e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
}
```

---

## CQ-07: Resource Leaks

### CQ-07.1 FileOutputStream Not in Try-with-Resources (All 14 Excel Reports)

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| Files | All 14 Excel report files |
| Evidence | Every `createExcel()` method opens a `FileOutputStream` without try-with-resources. If `wb.write(fileOut)` throws an exception, the stream is never closed. |

**Representative (ExcelKeyHourUtilReport.java lines 96-98):**
```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
```

The `Workbook wb` (XSSFWorkbook) is also never closed in any of the report classes.

### CQ-07.2 Workbook Never Closed

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| Files | All 14 Excel report files |
| Evidence | The `Workbook wb` field inherited from `Frm_excel` (an `XSSFWorkbook`) is never closed. `XSSFWorkbook` implements `Closeable` and holds memory-intensive resources. None of the 14 subclasses nor the base class call `wb.close()`. |

---

## CQ-08: God Methods

### CQ-08.1 ExcelVorReport.createVorReport() -- 264 Lines with 7 Nesting Levels

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| File | `ExcelVorReport.java` |
| Lines | 44-308 (264 lines) |
| Evidence | This method performs data extraction from the bean (20+ local variables), tokenizer-based `do_list` parsing, and a deeply nested loop structure (for model types > for vehicles > for drivers > for fields) to populate cells. Maximum nesting depth is 7 levels. |

### CQ-08.2 ExcelKeyHourUtilReport.createUtilReport() -- 249 Lines

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| File | `ExcelKeyHourUtilReport.java` |
| Lines | 103-352 (249 lines) |
| Evidence | Contains two large for-loops (utilized units and un-utilised units) with repetitive cell creation code. The same 8-column cell-creation pattern is duplicated twice within this single method. |

### CQ-08.3 ExcelSeatHourUtilReport.createUtilReport() -- 249 Lines

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| File | `ExcelSeatHourUtilReport.java` |
| Lines | 102-352 (249 lines) |
| Evidence | Near-identical god method to CQ-08.2; same structure and duplication. |

### CQ-08.4 ExcelServMaintenanceReport.createServMaintenanceReport() -- 222 Lines

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| File | `ExcelServMaintenanceReport.java` |
| Lines | 45-267 (222 lines) |
| Evidence | Performs complex business logic (service type calculation, date comparison, color status determination) interleaved with Excel cell creation. Business logic should be separated from presentation. |

### CQ-08.5 ExcelRestrictedUsageReport.createRestrictedAccessReport() -- 217 Lines

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| File | `ExcelRestrictedUsageReport.java` |
| Lines | 50-267 (217 lines) |
| Evidence | Large method with nested iterator and conditional branching for first/subsequent rows, plus a grand total section. |

---

## CQ-09: Dead Code / Unused Variables

### CQ-09.1 Unused UnitDAO Instantiations

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| Files and Lines | ExcelKeyHourUtilReport (line 106), ExcelPreOpCheckFailReport (lines 86, 245), ExcelPreOpCheckReport (line 68), ExcelSeatHourUtilReport (line 105), ExcelUnitUnlockReport (line 61), ExcelUtilWOWReport (line 68), ExcelUtilWOWReportEmail (line 69), ExcelUtilisationReport (line 80), ExcelVorReport (line 105) |
| Evidence | `UnitDAO unitDAO = new UnitDAO();` is instantiated but never used in any of these methods. This creates an unnecessary object and possibly an unnecessary database connection. |

**ExcelKeyHourUtilReport.java line 106:**
```java
UnitDAO unitDAO = new UnitDAO();
```

### CQ-09.2 Unused CustomerDAO Instantiation

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| File | `ExcelRestrictedUsageReport.java` line 59 |
| Evidence | `CustomerDAO customerDAO = new CustomerDAO();` is instantiated and used for name lookups, but `ExcelSuperMasterAuthReport.java` line 59 also creates one. In `ExcelRestrictedUsageReport`, the `customerDAO` is correctly used; in `ExcelSuperMasterAuthReport` it is also used. This is noted for consistency but not dead code. |

### CQ-09.3 Unused Local Variables

| File | Variable | Line | Evidence |
|------|----------|------|----------|
| ExcelPreOpCheckFailReport | `FormulaEvaluator evaluator` | 116 | Declared but never referenced |
| ExcelSeatHourUtilReport | `FormulaEvaluator evaluator` | 136 | Declared but never referenced |
| ExcelUtilWOWReport | `String get_user`, `get_loc`, `get_dep`, `form_nm`, `chartUrl` | 47-52 | All extracted from bean but never used |
| ExcelUtilWOWReportEmail | `String get_user`, `get_loc`, `get_dep`, `form_nm` | 48-51 | Extracted from bean but never used |
| ExcelUtilisationReport | `ArrayList Vgp_cd` through `ArrayList vdept_nm`, `String get_gp`, `get_user`, `get_loc`, `get_dep` | 45-59 | 10+ local variables extracted from bean and never referenced in the method |
| ExcelRestrictedUsageReport | `String temp` | 101 | Set to "x" and never used |
| ExcelSuperMasterAuthReport | `String temp` | 96 | Set to "x", later used only for comparison |
| ExcelVorReport | `ArrayList vrpt_veh_value_stopv` | 57 | Duplicates `vrpt_veh_value_stop` (calls same getter) and `vveh_value_stopv` local in the loop also shadows it |

**ExcelUtilWOWReport.java lines 47-52:**
```java
String get_user=utilBean.getGet_user();
String get_loc = utilBean.getGet_loc();
String get_dep = utilBean.getGet_dep();
String get_mod = utilBean.getGet_mod();
String form_nm = utilBean.getForm_nm();
String chartUrl = utilBean.getChartUrl();
```
Only `get_mod` is used (line 76 in subtitles). The rest are dead.

### CQ-09.4 System.out.println in MailExcelReports

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| File | `MailExcelReports.java` |
| Lines | 14, 27 |
| Evidence | Debug/logging via `System.out.println()` instead of a proper logging framework. |

```java
System.out.println(LindeConfig.now("yyyy.MM.dd G 'at' hh:mm:ss z") + " :Sending email: " + attachmentName);
System.out.println(LindeConfig.now("yyyy.MM.dd G 'at' hh:mm:ss z") + " :Email sent to: " + email_id +" ElapseTime: "+(System.currentTimeMillis() - startTime) + "(ms)");
```

---

## CQ-10: Raw Types / Missing Generics

### CQ-10.1 Raw ArrayList Usage Across All Excel Reports

| Attribute | Detail |
|-----------|--------|
| Severity | MEDIUM |
| Files | ExcelKeyHourUtilReport, ExcelSeatHourUtilReport, ExcelPreOpCheckReport, ExcelPreOpCheckFailReport, ExcelUnitUnlockReport, ExcelVorReport, ExcelUtilWOWReport, ExcelUtilWOWReportEmail, ExcelUtilisationReport, ExcelServMaintenanceReport |
| Evidence | Nearly all ArrayList declarations use raw types without generics, requiring unsafe casts throughout. |

**ExcelKeyHourUtilReport.java lines 23-36:**
```java
ArrayList veh_cd = new ArrayList();
ArrayList veh_nm = new ArrayList();
...
```

**ExcelVorReport.java lines 46-65 (20+ raw ArrayLists):**
```java
ArrayList vrpt_veh_typ_cd = dynBean.getVrpt_veh_typ_cd();
ArrayList vrpt_veh_typ = dynBean.getVrpt_veh_typ();
...
```

---

## CQ-11: Inheritance / Design Patterns

### CQ-11.1 MailBase Is Not Used as a Base Class

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| File | `MailBase.java` |
| Evidence | Despite the name suggesting it is a base class, `MailBase` is never extended. It is instantiated as a utility object by `Frm_excel` (`protected MailBase mb = new MailBase();` at line 62). `MailExcelReports` does not extend or reference `MailBase`. The class could be renamed to `MailHtmlHelper` or similar. |

### CQ-11.2 MailExcelReports Does Not Use MailBase

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| File | `MailExcelReports.java` |
| Evidence | `MailExcelReports` handles email sending but does not extend or compose `MailBase`. There is no relationship between the two "Mail" classes despite being in the same package. `MailExcelReports` delegates directly to `com.torrent.surat.fms6.util.mail`. |

### CQ-11.3 All 14 Excel Reports Extend Frm_excel but Override getFileName() Identically

| Attribute | Detail |
|-----------|--------|
| Severity | LOW |
| Files | All 14 Excel report files |
| Evidence | Every subclass overrides `getFileName()` with the identical body `return fileName;`, which is already the implementation in `Frm_excel` (line 1154). These overrides are redundant. |

---

## CQ-12: Potential Bug

### CQ-12.1 ExcelUtilisationReport -- Wrong Value for Traction Hours Cell

| Attribute | Detail |
|-----------|--------|
| Severity | HIGH |
| File | `ExcelUtilisationReport.java` |
| Lines | 161-163 |
| Evidence | The cell formula uses `getTrack_hours()` but the cell value is set to `getKey_hours()`, meaning the displayed fallback value is wrong. |

```java
contentCell.setCellFormula("VALUE(\""+utilBean.getTrack_hours()+"\")");
contentCell.setCellValue(utilBean.getKey_hours());  // BUG: should be getTrack_hours()
contentCell.setCellStyle(styles.get("cell_48hour_time"));
```

---

## Summary Table

| ID | Finding | Severity | Files Affected |
|----|---------|----------|---------------|
| CQ-01.1 | KeyHourUtil / SeatHourUtil near-identical files | HIGH | 2 |
| CQ-01.2 | UtilWOWReport / UtilWOWReportEmail near-identical files | HIGH | 2 |
| CQ-01.3 | PreOpCheckFailReport internal method duplication | HIGH | 1 |
| CQ-01.4 | createExcel() boilerplate across all reports | MEDIUM | 14 |
| CQ-01.5 | MailBase setMailHeader HTML duplication | MEDIUM | 1 |
| CQ-02.1 | Non-descriptive underscore/abbreviation field names | MEDIUM | 7 |
| CQ-02.2 | Uppercase local variable names | LOW | 2 |
| CQ-02.3 | MailBase name implies abstract base but is utility | LOW | 1 |
| CQ-03.1 | Commented-out autoSizeColumn across files | LOW | 11 |
| CQ-03.2 | Commented-out protectSheet | LOW | 1 |
| CQ-04.1 | Duplicate ArrayList import | LOW | 6 |
| CQ-04.2 | Various unused imports | LOW | 9 |
| CQ-05.1 | Empty catch in OperationalStatusReport | HIGH | 1 |
| CQ-05.2 | Broad Exception catch | MEDIUM | 1 |
| CQ-06.1 | e.printStackTrace() in MailExcelReports | HIGH | 1 |
| CQ-07.1 | FileOutputStream not in try-with-resources | HIGH | 14 |
| CQ-07.2 | Workbook never closed | MEDIUM | 14 |
| CQ-08.1 | VorReport.createVorReport() god method (264 lines) | HIGH | 1 |
| CQ-08.2 | KeyHourUtilReport.createUtilReport() god method | HIGH | 1 |
| CQ-08.3 | SeatHourUtilReport.createUtilReport() god method | HIGH | 1 |
| CQ-08.4 | ServMaintenanceReport god method | MEDIUM | 1 |
| CQ-08.5 | RestrictedUsageReport god method | MEDIUM | 1 |
| CQ-09.1 | Unused UnitDAO instantiations | MEDIUM | 9 |
| CQ-09.2 | Unused local variables | MEDIUM | 6 |
| CQ-09.3 | Duplicate/dead ArrayList (VorReport) | LOW | 1 |
| CQ-09.4 | System.out.println for logging | LOW | 1 |
| CQ-10.1 | Raw types (no generics) across all reports | MEDIUM | 10 |
| CQ-11.1 | MailBase misleading name / not a base class | LOW | 1 |
| CQ-11.2 | MailExcelReports unrelated to MailBase | LOW | 1 |
| CQ-11.3 | Redundant getFileName() overrides | LOW | 14 |
| CQ-12.1 | Wrong value for Traction Hours cell (bug) | HIGH | 1 |

---

## Severity Distribution

| Severity | Count |
|----------|-------|
| HIGH | 10 |
| MEDIUM | 12 |
| LOW | 10 |
| **Total** | **32** |

---

*End of Pass 4 audit for excel/reports K-Z + Mail files. Report only -- no fixes applied.*
