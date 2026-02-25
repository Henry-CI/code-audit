# Pass 4 -- Code Quality Audit: excel/reports Excel* A-I

**Audit ID:** A11-P4
**Date:** 2026-02-25
**Auditor:** Agent A11
**Scope:** 18 files in `WEB-INF/src/com/torrent/surat/fms6/excel/reports/` (ExcelBatteryReport through ExcelImpactReport)
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## Summary

| Check                        | Files Affected | Severity |
|------------------------------|:--------------:|:--------:|
| Code Duplication             | 18/18          | HIGH     |
| Naming Conventions           | 14/18          | MEDIUM   |
| Commented-Out Code           | 15/18          | LOW      |
| Unused Imports               | 12/18          | MEDIUM   |
| Empty / Broad Catches        | 1/18           | HIGH     |
| `e.printStackTrace()`        | 1/18           | HIGH     |
| Resource Leaks (FOS/Workbook)| 18/18          | HIGH     |
| God Methods                  | 6/18           | HIGH     |
| Dead Code                    | 4/18           | MEDIUM   |

---

## 1. Code Duplication

**Severity: HIGH**
**Files Affected: ALL 18 files**

Every file in this set follows an almost identical structural pattern. The `createExcel()` method is copy-pasted across all 18 files with only trivial variation (which inner report-building method is called). The boilerplate consists of:

```java
// Identical in all 18 files:
File docFile = new File(docroot);
if( !docFile.exists() ){
    docFile.mkdirs();
}
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
return result;
```

Additionally, the subtitle/header construction pattern is duplicated across every report builder method:

```java
String[][] subtitles1 = {
    {"FleetFocus Reporting System"},
    {"Start Time", st},
    {"End Time", et},
    {"Customer", cust},
    {"Site", loc},
    {"Dept", dep},
    {"Report:", tabTitle}
};
```

The cell-writing pattern (create cell, set value, set style) is repeated hundreds of times with no helper method:

```java
contentCell = row.createCell(m++);
contentCell.setCellValue((String)someList.get(i));
contentCell.setCellStyle(styles.get("cell_report_centered"));
```

The do_list/fld_hide tokenization block is copy-pasted identically in 5 files (ExcelDynDriverReport, ExcelDynSeenReport, ExcelDynTransportDriverReport, ExcelDynUnitReport, ExcelExceptionSessionReport):

```java
String delims=",";
StringTokenizer Tok = new StringTokenizer(do_list,delims);
if(Tok!=null) { ... }
```

### Specific Duplication Pairs

| File A | File B | Duplicated Region |
|--------|--------|-------------------|
| ExcelCurrDrivReport | ExcelCurrUnitReport | ~80% structural overlap; both extract the same bean arrays and write cells identically |
| ExcelDynDriverReport | ExcelDynUnitReport | ~70% overlap; field-hide logic, header construction, total/grand-total rendering |
| ExcelDynUnitReport | ExcelExceptionSessionReport | ~75% overlap; entire report loop structure nearly identical |
| ExcelImpactReport | ExcelImpactMeterReport | ~85% overlap; the core impact-rendering loop, severity color logic, photo handling |

---

## 2. Naming Conventions

**Severity: MEDIUM**
**Files Affected: 14/18**

### 2a. Raw-type ArrayList (no generics)

All 18 files use raw `ArrayList` without type parameters, but the following files are the worst offenders with numerous raw-typed local variables:

| File | Line(s) | Example |
|------|---------|---------|
| ExcelBatteryReport.java | 45-49 | `ArrayList vunit_name = bean.getVunit_name()` |
| ExcelCimplicityShockReport.java | 46-47 | `ArrayList vmachine_nm`, `ArrayList vuser_nm` |
| ExcelCimplicityUtilReport.java | 47-55 | 7 raw ArrayLists |
| ExcelCurrDrivReport.java | 46-53 | 8 raw ArrayLists |
| ExcelCurrUnitReport.java | 46-54 | 9 raw ArrayLists |
| ExcelDailyVehSummaryReport.java | 47-81 | 18+ raw ArrayLists |
| ExcelDriverAccessAbuseReport.java | 21-29 | 10 raw ArrayList fields |
| ExcelDriverImpactReport.java | 49-57 | 9 raw ArrayLists |
| ExcelDriverLicenceExpiry.java | 47-48 | 2 raw ArrayLists |
| ExcelDynDriverReport.java | 48-66 | 19 raw ArrayLists |
| ExcelDynSeenReport.java | 49-58 | 10 raw ArrayLists |
| ExcelDynTransportDriverReport.java | 43-57 | 15 raw ArrayLists |
| ExcelDynUnitReport.java | 49-69 | 20+ raw ArrayLists |
| ExcelExceptionSessionReport.java | 43-62 | 20+ raw ArrayLists |
| ExcelImpactMeterReport.java | 22-29 | 8 raw ArrayList fields |
| ExcelImpactReport.java | 24-32 | 8 raw ArrayList fields |

### 2b. Non-standard variable naming

| File | Line | Variable | Issue |
|------|------|----------|-------|
| ExcelDynDriverReport.java | 80 | `Tok` | Capital first letter for local variable |
| ExcelDynSeenReport.java | 72 | `Tok` | Same |
| ExcelDynTransportDriverReport.java | 71 | `Tok` | Same |
| ExcelDynUnitReport.java | 82 | `Tok` | Same |
| ExcelExceptionSessionReport.java | 78 | `Tok` | Same |
| ExcelImpactMeterReport.java | 22-29 | `Vhire_no`, `Vveh_id`, `Vmodel_no`, `Vdriver`, `Vcard_no`, `Vimp_tm`, `Vimp_ene`, `Vtmp_imp_data` | Capital V prefix on instance fields |
| ExcelImpactReport.java | 24-30 | `Vhire_no`, `Vveh_id`, `Vmodel_no`, `Vdriver`, `Vcard_no`, `Vimp_tm`, `Vimp_ene` | Same |
| ExcelImpactMeterReport.java | 71 | `Vimp_img` | Capital V prefix on local variable |
| ExcelImpactReport.java | 73 | `Vimp_img` | Same |

### 2c. Misleading method names

| File | Line | Method | Issue |
|------|------|--------|-------|
| ExcelBroadcastMsgReport.java | 42 | `createUnitUnlockReport()` | Method named "UnitUnlock" but creates a Broadcast Message report -- clear copy-paste naming error |
| ExcelDynDriverReport.java | 46 | `createDynUnitReport()` | Named "Unit" but creates Driver report |
| ExcelDynSeenReport.java | 46 | `createDynUnitReport()` | Named "Unit" but creates Pedestrian Detection report |
| ExcelDynTransportDriverReport.java | 41 | `createDynUnitReport()` | Named "Unit" but creates Transport Driver report |

### 2d. Typo in string literal

| File | Line | Value | Issue |
|------|------|-------|-------|
| ExcelDriverLicenceExpiry.java | 53 | `"Driver LIcence Expiry Report"` | Uppercase "I" in "LIcence" |

---

## 3. Commented-Out Code

**Severity: LOW**
**Files Affected: 15/18**

| File | Line(s) | Content |
|------|---------|---------|
| ExcelBatteryReport.java | 69 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelBroadcastMsgReport.java | 60 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelCimplicityShockReport.java | 64 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelCimplicityUtilReport.java | 72 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelCurrDrivReport.java | 72 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelCurrDrivReport.java | 79-81 | Commented-out dept header logic block |
| ExcelCurrUnitReport.java | 73 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDailyVehSummaryReport.java | 104 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDriverAccessAbuseReport.java | 92 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDriverImpactReport.java | 78 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDriverLicenceExpiry.java | 65 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDynDriverReport.java | 123 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDynSeenReport.java | 115 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDynTransportDriverReport.java | 108 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelDynUnitReport.java | 122 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelExceptionSessionReport.java | 157 | `//adjust first column width: sheet.autoSizeColumn(0);` |
| ExcelImpactMeterReport.java | 88, 187 | `//adjust first column width...` and `//` stray comment |
| ExcelImpactReport.java | 94 | `//adjust first column width: sheet.autoSizeColumn(0);` |

The `//adjust first column width` comment appears in 15 of 18 files -- clearly a mass copy-paste artifact.

---

## 4. Unused Imports

**Severity: MEDIUM**
**Files Affected: 12/18**

| File | Line(s) | Unused Import(s) |
|------|---------|-------------------|
| ExcelBatteryReport.java | 6 | `java.util.Vector` |
| ExcelBatteryReport.java | 12 | `com.torrent.surat.fms6.dao.UnitDAO` |
| ExcelCimplicityShockReport.java | 5 | `java.io.IOException` (only thrown, not caught) -- however, method declares `throws IOException`, so the import is used. **Duplicate import on line 7**: `java.util.ArrayList` imported twice |
| ExcelCimplicityShockReport.java | 7 | Duplicate `java.util.ArrayList` |
| ExcelCimplicityShockReport.java | 13 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 54 but never used further |
| ExcelCimplicityUtilReport.java | 7 | Duplicate `java.util.ArrayList` |
| ExcelCimplicityUtilReport.java | 13 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 62 but result never used |
| ExcelCurrDrivReport.java | 6 | Duplicate `java.util.ArrayList` |
| ExcelCurrDrivReport.java | 12 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 61 but never used |
| ExcelCurrUnitReport.java | 6 | Duplicate `java.util.ArrayList` |
| ExcelCurrUnitReport.java | 12 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 62 but never used |
| ExcelDailyVehSummaryReport.java | 7 | Duplicate `java.util.ArrayList` |
| ExcelDailyVehSummaryReport.java | 13 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 93 but never used |
| ExcelDriverAccessAbuseReport.java | 8 | Duplicate `java.util.ArrayList` |
| ExcelDriverAccessAbuseReport.java | 14 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 81 but never used |
| ExcelDriverImpactReport.java | 7 | Duplicate `java.util.ArrayList` |
| ExcelDriverLicenceExpiry.java | 8 | `java.util.Vector` -- never used |
| ExcelDynDriverReport.java | 7 | Duplicate `java.util.ArrayList` |
| ExcelDynDriverReport.java | 14 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 107 but never used |
| ExcelDynSeenReport.java | 7 | Duplicate `java.util.ArrayList` |
| ExcelDynSeenReport.java | 14 | `com.torrent.surat.fms6.dao.UnitDAO` -- instantiated on line 99 but never used |
| ExcelDynUnitReport.java | 5 | `java.sql.SQLException` -- never thrown or caught |
| ExcelDynUnitReport.java | 8 | Duplicate `java.util.ArrayList` |
| ExcelDynUnitReport.java | 15 | `com.torrent.surat.fms6.dao.UnitDAO` -- not instantiated in this file |
| ExcelImpactMeterReport.java | 16 | `com.torrent.surat.fms6.util.DataUtil` -- never referenced |

### Summary of duplicate `java.util.ArrayList` imports

Files with `import java.util.ArrayList;` appearing twice: ExcelCimplicityShockReport, ExcelCimplicityUtilReport, ExcelCurrDrivReport, ExcelCurrUnitReport, ExcelDailyVehSummaryReport, ExcelDriverAccessAbuseReport, ExcelDriverImpactReport, ExcelDynDriverReport, ExcelDynSeenReport, ExcelDynUnitReport (10 files).

### Unused UnitDAO instantiation (object created, result discarded)

In 8 files, a `UnitDAO unitDAO = new UnitDAO()` is created but the variable is never referenced afterward. This represents wasted object creation and a potential database connection leak if the DAO constructor acquires resources:

- ExcelCimplicityShockReport.java:54
- ExcelCimplicityUtilReport.java:62
- ExcelCurrDrivReport.java:61
- ExcelCurrUnitReport.java:62
- ExcelDailyVehSummaryReport.java:93
- ExcelDriverAccessAbuseReport.java:81
- ExcelDynDriverReport.java:107
- ExcelDynSeenReport.java:99
- ExcelImpactMeterReport.java:77
- ExcelImpactReport.java:79

---

## 5. Empty / Broad Catches

**Severity: HIGH**
**Files Affected: 1/18**

| File | Line(s) | Issue |
|------|---------|-------|
| ExcelExceptionSessionReport.java | 136-139 | `catch (Exception e) { }` -- broad `Exception` catch with empty body silently swallows URL decoding errors. The comment says "use the original value" but no logging or alternative handling occurs. |

```java
try {
    searchCrit = java.net.URLDecoder.decode(searchCrit, "UTF-8");
} catch (Exception e) {
    // If there's an error decoding, use the original value
}
```

---

## 6. `e.printStackTrace()`

**Severity: HIGH**
**Files Affected: 1/18**

| File | Line(s) | Context |
|------|---------|---------|
| ExcelImpactReport.java | 233-235 | Inside `createImpactReport` method, a `JSONException` catch block calls `e.printStackTrace()`. In a server-side Tomcat application this writes to stdout/stderr rather than the application log, and no recovery or re-throw occurs. |

```java
} catch (JSONException e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
}
```

Note: The `// TODO Auto-generated catch block` comment indicates IDE-generated code that was never properly implemented.

---

## 7. Resource Leaks

**Severity: HIGH**
**Files Affected: ALL 18 files**

### 7a. FileOutputStream not in try-with-resources

Every file creates a `FileOutputStream` without try-with-resources or a finally block. If `wb.write(fileOut)` throws an exception, the stream is never closed:

```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
```

**Affected files (all 18):**
- ExcelBatteryReport.java:36-38
- ExcelBroadcastMsgReport.java:35-37
- ExcelCimplicityShockReport.java:38-40
- ExcelCimplicityUtilReport.java:38-40
- ExcelCurrDrivReport.java:37-39
- ExcelCurrUnitReport.java:37-39
- ExcelDailyVehSummaryReport.java:40-42
- ExcelDriverAccessAbuseReport.java:67-69
- ExcelDriverImpactReport.java:40-42
- ExcelDriverLicenceExpiry.java:38-40
- ExcelDynDriverReport.java:39-41
- ExcelDynSeenReport.java:39-41
- ExcelDynTransportDriverReport.java:34-36
- ExcelDynUnitReport.java:40-42
- ExcelExceptionSessionReport.java:34-36
- ExcelHireDehireReport.java:34-36
- ExcelImpactMeterReport.java:52-54
- ExcelImpactReport.java:55-57

### 7b. XSSFWorkbook (`wb`) never explicitly closed

The `wb` workbook (inherited from `Frm_excel` superclass) is never closed in any of these 18 files. `XSSFWorkbook` implements `Closeable` and holds significant heap memory (XML DOM). Not closing it creates a memory leak, especially under concurrent report generation.

---

## 8. God Methods

**Severity: HIGH**
**Files Affected: 6/18**

Methods exceeding reasonable size (~50 lines) with deep nesting and multiple responsibilities:

| File | Method | Lines | Nesting Depth | Description |
|------|--------|:-----:|:-------------:|-------------|
| ExcelDynDriverReport.java | `createDynUnitReport()` | ~255 (L46-L301) | 6 | Parses field visibility, iterates vehicle types, iterates drivers, iterates vehicles, writes cells, computes totals and grand totals |
| ExcelDynUnitReport.java | `createDynUnitReport()` | ~275 (L47-L322) | 7 | Same structural pattern; includes excluded-vehicle filtering |
| ExcelExceptionSessionReport.java | `createExceptionSessionReport()` | ~305 (L41-L348) | 6 | Builds subtitles conditionally, same loop-of-loops pattern with operational mode handling |
| ExcelDynTransportDriverReport.java | `createDynUnitReport()` | ~180 (L41-L222) | 6 | Same nested loop pattern |
| ExcelDynSeenReport.java | `createDynUnitReport()` | ~160 (L46-L208) | 5 | Nested iteration with field-hide logic |
| ExcelDailyVehSummaryReport.java | `createDSumReport()` | ~225 (L46-L270) | 4 | Multiple customer-type conditional branches combined with cell-writing loops |

---

## 9. Dead Code

**Severity: MEDIUM**
**Files Affected: 4/18**

| File | Line(s) | Dead Code | Reason |
|------|---------|-----------|--------|
| ExcelBatteryReport.java | 50 | `String model_name = bean.getModel_name()` | Variable `model_name` is assigned but the subtitles array on line 65 references the variable only in the subtitle. However the value IS used in the subtitle. **Not dead.** |
| ExcelCurrDrivReport.java | 47-50 | `ArrayList vveh_id`, `ArrayList vveh_typ_cd` | Variables extracted from bean but never referenced in cell-writing loop |
| ExcelCurrUnitReport.java | 47, 49 | `ArrayList vveh_id`, `ArrayList vveh_typ_cd` | Same as above -- extracted but never used |
| ExcelDynDriverReport.java | 58 | `ArrayList vrpt_veh_value_stopv` | Assigned identical value as `vrpt_veh_value_stop` on line 56, never referenced afterward |
| ExcelDynDriverReport.java | 69, 144 | `ArrayList vfld_hide`, `ArrayList<String> headerLst1` | Declared, never used |
| ExcelDynDriverReport.java | 149 | `FormulaEvaluator evaluator` | Created but never used |
| ExcelDynSeenReport.java | 61, 133 | `ArrayList vfld_hide`, `String field_cd` | Declared but never referenced |
| ExcelDynTransportDriverReport.java | 60, 123 | `ArrayList vfld_hide`, `ArrayList<String> headerLst1` declared but `headerLst1` is used. `vfld_hide` is never used. |
| ExcelDynUnitReport.java | 59, 71, 143-144 | `ArrayList vrpt_veh_value_stopv`, `ArrayList vfld_hide`, `ArrayList<String> headerLst1` | `vrpt_veh_value_stopv` is a duplicate fetch; `vfld_hide` is never populated or read; `headerLst1` is used for model header row though |
| ExcelExceptionSessionReport.java | 67 | `ArrayList vfld_hide` | Declared, never populated or read |
| ExcelImpactMeterReport.java | 16-17 | `import DataUtil; import RuntimeConf` | `DataUtil` imported but never used. `RuntimeConf` is also imported but not referenced in this file (no hardcoded URL like in ExcelImpactReport). **Correction**: `RuntimeConf` is not referenced. `DataUtil` is not referenced. |
| ExcelDriverAccessAbuseReport.java | 31, 116 | `String a_time_filter = ""`, `String x = ""` | Both assigned but never read |

---

## 10. Additional Observations

### 10a. Potential NullPointerException risks

In ExcelDynSeenReport.java line 72, `if(Tok!=null)` -- `StringTokenizer` constructor never returns null, making this check meaningless. Same pattern in ExcelDynDriverReport (L81), ExcelDynTransportDriverReport (L73), ExcelDynUnitReport (L83), ExcelExceptionSessionReport (L79).

### 10b. Hardcoded URL

| File | Line | Value |
|------|------|-------|
| ExcelImpactMeterReport.java | 176 | `"http://fleetfocus.lindemh.com.au/fms/"+ RuntimeConf.impactDir+"/"+img_link.get(j)` |
| ExcelImpactReport.java | 191 | Same hardcoded HTTP URL |

Both files hardcode the base URL `http://fleetfocus.lindemh.com.au/fms/` rather than using a configuration property. This also uses plain HTTP, not HTTPS.

### 10c. Spelling error in variable name

| File | Line | Variable | Issue |
|------|------|----------|-------|
| ExcelDriverLicenceExpiry.java | 48 | `vreveiw_date` | Should be `vreview_date` |

### 10d. Inconsistent `createExcel` signatures

The `createExcel` method has different signatures across files, preventing polymorphic use:
- 5-param `(cust, loc, dep, st, et)` -- most files
- 6-param `(cust, loc, dep, st, et, model)` -- ExcelDriverImpactReport
- 3-param `(cust_cd, loc_cd, dept_cd)` -- ExcelDriverLicenceExpiry
- 3-param `(st, et, sc)` -- ExcelHireDehireReport

---

## File-by-File Summary

| # | File | Dup | Naming | Comments | Unused Imports | Empty Catch | printStackTrace | Resource Leak | God Method | Dead Code |
|---|------|:---:|:------:|:--------:|:--------------:|:-----------:|:---------------:|:-------------:|:----------:|:---------:|
| 1 | ExcelBatteryReport.java | Y | Y | Y | Y (Vector, UnitDAO) | - | - | Y | - | - |
| 2 | ExcelBroadcastMsgReport.java | Y | Y | Y | - | - | - | Y | - | - |
| 3 | ExcelCimplicityShockReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | - | - |
| 4 | ExcelCimplicityUtilReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | - | - |
| 5 | ExcelCurrDrivReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | - | Y |
| 6 | ExcelCurrUnitReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | - | Y |
| 7 | ExcelDailyVehSummaryReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | Y | - |
| 8 | ExcelDriverAccessAbuseReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | - | Y |
| 9 | ExcelDriverImpactReport.java | Y | Y | Y | Y (dup ArrayList) | - | - | Y | - | - |
| 10 | ExcelDriverLicenceExpiry.java | Y | Y | Y | Y (Vector) | - | - | Y | - | - |
| 11 | ExcelDynDriverReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | Y | Y |
| 12 | ExcelDynSeenReport.java | Y | Y | Y | Y (dup ArrayList, UnitDAO unused) | - | - | Y | Y | Y |
| 13 | ExcelDynTransportDriverReport.java | Y | Y | - | - | - | - | Y | Y | - |
| 14 | ExcelDynUnitReport.java | Y | Y | Y | Y (dup ArrayList, SQLException) | - | - | Y | Y | Y |
| 15 | ExcelExceptionSessionReport.java | Y | Y | Y | - | Y | - | Y | Y | Y |
| 16 | ExcelHireDehireReport.java | Y | - | Y | - | - | - | Y | - | - |
| 17 | ExcelImpactMeterReport.java | Y | Y | Y | Y (DataUtil) | - | - | Y | - | - |
| 18 | ExcelImpactReport.java | Y | Y | Y | - | - | Y | Y | - | - |

---

## Recommendations (Report Only -- No Fixes Applied)

1. **Extract a base-class `createExcel` template method** in `Frm_excel` that handles directory creation, file output stream management (with try-with-resources), and workbook close. Each subclass would only override the report-building step.

2. **Create a cell-writing helper method** (e.g., `writeCell(Row row, int col, String value, String styleName)`) to eliminate the repetitive 3-line cell-creation pattern.

3. **Extract the do_list/fld_hide tokenization logic** into a shared utility method to eliminate the identical block duplicated across 5 files.

4. **Replace all raw `ArrayList` usage** with parameterized types (`ArrayList<String>`, etc.) to improve type safety and readability.

5. **Fix misleading method names** -- especially `createUnitUnlockReport` in ExcelBroadcastMsgReport and `createDynUnitReport` in ExcelDynDriverReport, ExcelDynSeenReport, and ExcelDynTransportDriverReport.

6. **Replace `e.printStackTrace()`** in ExcelImpactReport with proper logging (e.g., `logger.error()`).

7. **Fix the empty catch** in ExcelExceptionSessionReport to at least log the exception.

8. **Wrap FileOutputStream in try-with-resources** and ensure `wb.close()` is called in all files.

9. **Remove all unused imports**, duplicate imports, and unused local variables/fields.

10. **Externalize the hardcoded URL** in ExcelImpactReport and ExcelImpactMeterReport to a configuration property, and use HTTPS.

---

*End of Pass 4 audit for excel/reports Excel* A-I.*
