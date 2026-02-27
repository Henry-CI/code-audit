# Pass 4 -- Code Quality Audit: excel/Frm_* (10 files)

**Auditor:** A09
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/excel/`

---

## 1. File Inventory

| # | File | Lines | Extends |
|---|------|------:|---------|
| 1 | `Frm_excel.java` | 1163 | -- (base class) |
| 2 | `Frm_Linde_Reports.java` | 2381 | `Frm_excel` |
| 3 | `Frm_MaxHourUsage.java` | 196 | `Frm_excel` |
| 4 | `Frm_inaUnit_rpt.java` | 227 | `Frm_excel` |
| 5 | `Frm_month_rpt.java` | 765 | `Frm_excel` |
| 6 | `Frm_national_rpt.java` | 1209 | `Frm_excel` |
| 7 | `Frm_nz_unitSummary_rpt.java` | 112 | `Frm_excel` |
| 8 | `Frm_quater_rpt.java` | 875 | `Frm_excel` |
| 9 | `Frm_simSwap_rpt.java` | 157 | `Frm_excel` |
| 10 | `Frm_unitSummary_rpt.java` | 257 | `Frm_excel` |

**Total:** 7,342 lines across 10 files.

---

## 2. Naming Conventions

### 2.1 Non-standard class names (underscore naming)

All 10 files use underscore-separated class names, which violates the standard Java PascalCase convention for class names.

| File | Class Name | Recommended PascalCase |
|------|-----------|------------------------|
| `Frm_excel.java` | `Frm_excel` | `FrmExcel` |
| `Frm_Linde_Reports.java` | `Frm_Linde_Reports` | `FrmLindeReports` |
| `Frm_MaxHourUsage.java` | `Frm_MaxHourUsage` | `FrmMaxHourUsage` |
| `Frm_inaUnit_rpt.java` | `Frm_inaUnit_rpt` | `FrmInactiveUnitReport` |
| `Frm_month_rpt.java` | `Frm_month_rpt` | `FrmMonthlyReport` |
| `Frm_national_rpt.java` | `Frm_national_rpt` | `FrmNationalReport` |
| `Frm_nz_unitSummary_rpt.java` | `Frm_nz_unitSummary_rpt` | `FrmNzUnitSummaryReport` |
| `Frm_quater_rpt.java` | `Frm_quater_rpt` | `FrmQuarterReport` |
| `Frm_simSwap_rpt.java` | `Frm_simSwap_rpt` | `FrmSimSwapReport` |
| `Frm_unitSummary_rpt.java` | `Frm_unitSummary_rpt` | `FrmUnitSummaryReport` |

**Severity:** LOW -- Consistent within the codebase but non-standard for Java.

### 2.2 Misspelled identifiers

| File | Location | Current | Expected |
|------|----------|---------|----------|
| `Frm_quater_rpt.java` | class name | `Frm_quater_rpt` | `Frm_quarter_rpt` |
| `Frm_excel.java` | line 80, `generateRadomName()` | `Radom` | `Random` |
| `Frm_excel.java` | line 903, parameter `dirctory` | `dirctory` | `directory` |
| `Frm_month_rpt.java` | line 500, title string | `"Unit Utilisation Reort"` | `"Unit Utilisation Report"` |
| `Frm_unitSummary_rpt.java` | line 125, header string | `"Moderm Version"` | `"Modem Version"` |

**Severity:** LOW (cosmetic) but the class name misspelling may cause confusion for future maintainers.

### 2.3 Field naming -- underscore style

Protected fields in `Frm_excel.java` (lines 50-68) use underscore naming: `cust_cd`, `loc_cd`, `dept_cd`, `cust_prefix`, `rpt_name`. This is the dominant convention in this codebase so is internally consistent, but is non-standard Java (which would use `custCd`, `locCd`, etc.).

---

## 3. God Class Analysis

### 3.1 Frm_Linde_Reports.java -- GOD CLASS

- **2,381 lines**, ~18 private methods plus a public `createExcel(String opCode)` router method.
- The `createExcel` method (lines 50-288) is a 238-line `if/else if` chain with 18 branches, each wiring up a different report type.
- Contains its own `generateChart` method that shells out to an external process via `Runtime.getRuntime().exec()` (line ~2335+).
- Mixes report construction, chart generation, and external process invocation in a single class.

**Severity:** HIGH -- This class should be decomposed into individual report strategy classes.

### 3.2 Frm_excel.java -- Large base class

- **1,163 lines** with 10 constructor overloads (lines 70-147), a 250-line `createStyles` method (lines 643-888), and 8 `addImage*` variant methods with heavy code duplication.
- Acts as both a utility class and a report base class.

**Severity:** MEDIUM

---

## 4. Commented-out Code

Significant amounts of commented-out code exist across the files. Total single-line comment count across all 10 files: **177 lines**.

| File | Lines | Key instances |
|------|-------|---------------|
| `Frm_excel.java` | 74 | Lines 504-510: commented-out `addImage2` alternatives; lines 536-537, 583, 589: commented-out closing braces; line 541: commented-out `System.out.println`; lines 837, 845: commented-out style format lines |
| `Frm_Linde_Reports.java` | 29 | Lines 307, 334, 365, 452: commented-out `File f` checks; lines 394, 396: commented-out `getDurationWeek` and params; lines 724-729: commented-out merge region; lines 1075-1076, 1226, 1432, 1566: commented-out `addImageLogo` calls |
| `Frm_quater_rpt.java` | 33 | Lines 676-679: commented-out test data; lines 686-688: commented-out DAO call; lines 715, 730, 748-749, 821: commented-out `System.out.println` debug statements |
| `Frm_national_rpt.java` | 20 | Lines 634-644: large block of commented-out work-days calculation logic |
| `Frm_month_rpt.java` | 9 | Lines 517-519, 555-557: commented-out testing data assignments |

**Severity:** MEDIUM -- Hinders readability and understanding of actual logic flow.

---

## 5. TODO / Auto-generated Comments

Residual IDE-generated `TODO` comments remain in 7 of 10 files:

| File | Line(s) | Comment |
|------|---------|---------|
| `Frm_Linde_Reports.java` | 47 | `// TODO Auto-generated constructor stub` |
| `Frm_MaxHourUsage.java` | 22, 28 | `// TODO Auto-generated constructor stub` |
| `Frm_MaxHourUsage.java` | 78, 156 | `// TODO needs to resize images` |
| `Frm_MaxHourUsage.java` | 85, 163 | `// TODO Auto-generated catch block` |
| `Frm_inaUnit_rpt.java` | 22, 30 | `// TODO Auto-generated constructor stub` |
| `Frm_month_rpt.java` | 31 | `// TODO Auto-generated constructor stub` |
| `Frm_national_rpt.java` | 34 | `// TODO Auto-generated constructor stub` |
| `Frm_nz_unitSummary_rpt.java` | 21 | `// TODO Auto-generated constructor stub` |
| `Frm_quater_rpt.java` | 36, 43 | `// TODO Auto-generated constructor stub` |
| `Frm_simSwap_rpt.java` | 20 | `// TODO Auto-generated constructor stub` |
| `Frm_unitSummary_rpt.java` | 21 | `// TODO Auto-generated constructor stub` |

**Severity:** LOW

---

## 6. Unused Imports

| File | Import | Evidence |
|------|--------|----------|
| `Frm_month_rpt.java` | `org.apache.poi.ss.usermodel.CellStyle` (line 14) | Never referenced directly; `styles` map from base class is used instead via `styles.get()` |
| `Frm_month_rpt.java` | `org.apache.poi.ss.usermodel.Workbook` (line 17) | Never referenced directly; `wb` is inherited |
| `Frm_month_rpt.java` | `java.util.Map` (line 10) | Not referenced in this file |
| `Frm_national_rpt.java` | `org.apache.poi.ss.usermodel.CellStyle` (line 12) | Never referenced directly |
| `Frm_national_rpt.java` | `org.apache.poi.ss.usermodel.Workbook` (line 15) | Never referenced directly |
| `Frm_quater_rpt.java` | `java.util.Arrays` (line 8) | Only appears in a commented-out line (749): `Arrays.deepToString` |
| `Frm_quater_rpt.java` | `org.apache.poi.ss.util.CellReference` (line 13) | Used only in `createImpactReport` and `createImpactByDriverReport`; valid usage |
| `Frm_excel.java` | `java.net.URL` (line 11) | Used in `addImage2`, `addImageUtilisationChart`, `addDashboardChart` |
| `Frm_excel.java` | `java.sql.SQLException` (line 12) | Used in method signatures |

**Confirmed unused:** `CellStyle` and `Workbook` in `Frm_month_rpt.java` and `Frm_national_rpt.java`; `java.util.Map` in `Frm_month_rpt.java`; `java.util.Arrays` in `Frm_quater_rpt.java`.

**Severity:** LOW

---

## 7. Exception Handling Issues

### 7.1 Broad catch (Exception) blocks

| File | Line(s) | Context |
|------|---------|---------|
| `Frm_excel.java` | 559 | `catch(Exception ex)` in `addImageFromUrl` -- catches all exceptions from SVG transcoding |
| `Frm_MaxHourUsage.java` | 84 | `catch(Exception e)` in `createUtilisationChart` |
| `Frm_MaxHourUsage.java` | 162 | `catch(Exception e)` in `createGroupUtilisationChart` |
| `Frm_quater_rpt.java` | 789 | `catch(Exception e)` in `createUtilisationChartByGroup` |

**Severity:** MEDIUM -- Broad catches obscure the actual exception type and mask potential bugs.

### 7.2 e.printStackTrace() usage

| File | Line(s) |
|------|---------|
| `Frm_excel.java` | 560 |
| `Frm_MaxHourUsage.java` | 86, 164 |
| `Frm_quater_rpt.java` | 790 |

All 4 occurrences use `e.printStackTrace()` which writes to stderr instead of a proper logging framework.

**Severity:** MEDIUM -- Production code should use a logger (e.g., `java.util.logging`, Log4j, SLF4J).

### 7.3 System.out.println in production code

| File | Line | Content |
|------|------|---------|
| `Frm_Linde_Reports.java` | 2369 | `System.out.println(line)` inside `generateChart` method |

**Severity:** LOW

---

## 8. Resource Leak Analysis

### 8.1 FileOutputStream not in try-with-resources

Every `createExcel()` method across all 10 files follows the same pattern:

```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
return result;
```

This occurs in:
- `Frm_excel.java` lines 203-206, 222-225, 233-236 (three methods)
- `Frm_Linde_Reports.java` lines 284-286
- `Frm_MaxHourUsage.java` lines 40-42
- `Frm_inaUnit_rpt.java` lines 45-47
- `Frm_month_rpt.java` lines 59-61
- `Frm_national_rpt.java` lines 89-91
- `Frm_nz_unitSummary_rpt.java` lines 41-43
- `Frm_quater_rpt.java` lines 87-89
- `Frm_simSwap_rpt.java` lines 32-34
- `Frm_unitSummary_rpt.java` lines 33-35

**Issues:**
1. If `wb.write(fileOut)` throws an exception, `fileOut.close()` is never called (no `finally` block, no try-with-resources).
2. The `Workbook wb` (field in `Frm_excel.java` line 63) is created in the constructor but never closed in any code path. `XSSFWorkbook` implements `Closeable` and holds temporary file resources.
3. No file is ever written using try-with-resources (zero occurrences confirmed by grep).

**Count:** 12 potential FileOutputStream leaks, 10 Workbook leaks.

**Severity:** HIGH -- Can lead to file descriptor exhaustion and locked files in production.

### 8.2 InputStream leaks in addImage* methods

In `Frm_excel.java`, the `addImage` variants (lines 400-590) open `FileInputStream` or `InputStream` from URL, and close them manually without `finally` blocks. If `IOUtils.toByteArray(is)` or `wb.addPicture()` throws, the stream is leaked.

Affected methods:
- `addImage(Sheet, String, int)` -- line 406
- `addImage(Sheet, String, int, boolean, int)` -- line 439
- `addImageLogo(Sheet, String, int, boolean, int, double)` -- line 474
- `addImage2(Sheet, String, int, boolean, int)` -- line 511
- `addImageFromUrl(Sheet, String, int, boolean, int)` -- line 547
- `addResizedImage(Sheet, String, int, boolean)` -- line 599
- `addImageUtilisationChart(Sheet, String, int, boolean, int)` -- line 948
- `addDashboardChart(Sheet, String, int, boolean, int)` -- line 986

**Severity:** MEDIUM

### 8.3 ByteArrayOutputStream leak in addImageFromUrl

In `Frm_excel.java` line 547-563: the `ByteArrayOutputStream ostream` is created in the try block but if the catch on line 559 fires, `ostream` may be null when accessed on line 563, causing a `NullPointerException`.

**Severity:** HIGH -- Potential NPE in the catch path.

---

## 9. Code Duplication

### 9.1 createExcel() boilerplate (FileOutputStream write pattern)

The exact same 3-line FileOutputStream pattern is duplicated in all 10 files (see Section 8.1). This should be extracted into the base class `Frm_excel`.

### 9.2 createSupervisorUnlockReport / createDriverLockoutReport duplication

In `Frm_Linde_Reports.java`, these two methods (lines 464-569 and 571-678) are structurally near-identical -- both:
- Query `LinderReportDatabean` with the same parameters
- Build the same 5-column table (Supervisor/Driver, Impact Lockout, Survey Timeout, Critical Question, Grand Total)
- Accumulate the same 4 running totals (`impTot`, `surTot`, `critTot`, `grantTot`)
- Write the same Grand Total footer row

The only differences are the title string and the first column header label.

**Severity:** MEDIUM

### 9.3 createUtilisationChart / createImpactChart / createPreOpChart duplication

In `Frm_Linde_Reports.java`, these three methods (lines 292-317, 319-344, 350-375) are nearly identical in structure -- each builds subtitles from `st_dt`, calls `createReptTitle`, `createReptSubTitle`, and `addImageFromUrl` with the same parameters. Only the title string differs.

**Severity:** MEDIUM

### 9.4 createUtilisationChart / createGroupUtilisationChart duplication in Frm_MaxHourUsage

`Frm_MaxHourUsage.java` lines 46-112 and 114-190 are near-identical methods. Both:
- Build the same title and date strings
- Query the same DAO (just different method: `getMaxUtil` vs `getMaxUtilGroup`)
- Iterate models identically, add images, catch exceptions
- Have identical `catch(Exception e) { e.printStackTrace(); }` blocks

**Severity:** MEDIUM

### 9.5 createUtilisationChart / createUtilisationChartByGroup duplication in Frm_quater_rpt

`Frm_quater_rpt.java` methods `createUtilisationChart` (lines 807-875) and `createUtilisationChartByGroup` (lines 672-795) share near-identical structure for chart layout with left/right side placement logic using `weekInt % 2`.

**Severity:** MEDIUM

### 9.6 On-Hire / Not-On-Hire table duplication in Frm_inaUnit_rpt

`Frm_inaUnit_rpt.java` lines 72-136 (On Hire) and lines 143-208 (Not On Hire) are structurally identical loops producing the same 6-column table, differing only in the boolean filter condition and the section title.

**Severity:** MEDIUM

### 9.7 setColumnWidth duplication across subclasses

Multiple subclasses override `setColumnWidth(Sheet)` with nearly identical patterns of `sheet.setColumnWidth(i, N*256)`:
- `Frm_simSwap_rpt.java` lines 39-56 (16 columns)
- `Frm_unitSummary_rpt.java` lines 40-51 (10 columns)
- `Frm_nz_unitSummary_rpt.java` lines 48-53 (4 columns)

The base class `Frm_excel.java` also has 5 different `setColumnWidth*` variants (lines 243-300). A parameterised utility method would eliminate this repetition.

**Severity:** LOW

---

## 10. Dead Methods

| File | Method | Line | Reason |
|------|--------|------|--------|
| `Frm_excel.java` | `init()` | 209 | Empty body, never overridden in any of the 9 subclasses |
| `Frm_excel.java` | `init2()` | 213 | Empty body, never overridden in any of the 9 subclasses |
| `Frm_excel.java` | `getBody()` | 239 | Returns empty string, never overridden |
| `Frm_excel.java` | `getCust_prefix(String)` | 1096 | Empty body, never overridden |
| `Frm_excel.java` | `createEmail()` | 217 | Identical to `createExcel()` and `createBody()` -- three methods with the same implementation |
| `Frm_excel.java` | `createBody()` | 228 | Identical to `createExcel()` and `createEmail()` |
| `Frm_excel.java` | `setFoot(Sheet)` | 304 | Annotated with own comment `//doesn't work` |
| `Frm_excel.java` | `createReport(Sheet)` | 309 | Contains hardcoded test data ("Person", "ID", "Mon"..., year 2011, "ALM", "VIC", "LAVERTON") -- appears to be development test code left in the base class |
| `Frm_excel.java` | `getImageHeight(String)` | 631 | Only called from `addResizedImage` but `width` variable (line 634) is assigned and never used |

**Severity:** MEDIUM -- Dead code bloats the base class and confuses maintainers. The `setFoot` method's own comment confirms it is non-functional.

---

## 11. Style Consistency

### 11.1 Indentation inconsistencies

`Frm_excel.java` uses **double-tab** indentation for class-level fields (lines 50-68, e.g., `\t\tprotected String result = "";`) while the rest of the methods use inconsistent mixes of tabs and spaces. Methods inside `Frm_excel.java` use 4-space indentation in some places (e.g., `createStyles` at line 643) and tab indentation in others.

Subclasses use a different mix: `Frm_quater_rpt.java` uses consistent tab-based indentation, while `Frm_inaUnit_rpt.java` uses spaces with irregular nesting.

### 11.2 Inconsistent brace style

All files use K&R style (opening brace on same line) for classes and methods, but `Frm_excel.java` inconsistently places closing braces, sometimes with extra blank lines (e.g., lines 346-347, 391-392).

### 11.3 Raw types

- `Frm_excel.java` line 60: `protected ArrayList deptCdArrayList = new ArrayList();` -- raw type, should be `ArrayList<String>`.
- `Frm_MaxHourUsage.java` line 26: `public Frm_MaxHourUsage(String cust_cd, String loc_cd, ArrayList deptCdArrayList, ...)` -- raw type parameter.
- `Frm_MaxHourUsage.java` line 135: `ArrayList<String> tabList = new ArrayList();` -- diamond operator missing on right side.
- `Frm_quater_rpt.java` line 40: `public Frm_quater_rpt(String cust_cd, String loc_cd, ArrayList deptCdArrayList, ...)` -- raw type parameter.

**Severity:** LOW

### 11.4 Deprecated API usage

`Frm_excel.java` line 544: `new File(image).toURL()` is deprecated since Java 1.7. Should use `new File(image).toURI().toURL()`.

**Severity:** LOW

---

## 12. Miscellaneous Observations

### 12.1 Double semicolons

`Frm_excel.java` line 120: `this.result = this.docroot+DataUtil.generateRadomName()+".xlsx";;` -- contains a stray double semicolon.

### 12.2 Hardcoded test data in base class

`Frm_excel.java` `createReport(Sheet)` method (lines 309-343) contains hardcoded values: `"year","2011"`, `"Pillar", "ALM"`, `"State", "VIC"`, `"Suburb", "LAVERTON"`. This is test/development stub code left in the production base class.

### 12.3 External process execution without error handling

`Frm_Linde_Reports.java` `generateChart` method (around line 2335) invokes `Runtime.getRuntime().exec()` and prints stdout via `System.out.println(line)` on line 2369. There is no error stream handling, no timeout, and no proper process lifecycle management.

### 12.4 Missing @Override annotations

None of the subclass `createExcel()` overrides use `@Override`. Zero `@Override` annotations exist across all 10 files.

---

## 13. Summary of Findings

| Category | Count | Severity |
|----------|------:|----------|
| Non-standard class naming (underscores) | 10 classes | LOW |
| Misspelled identifiers | 5 instances | LOW |
| God class (Frm_Linde_Reports) | 1 class, 2381 lines | HIGH |
| Commented-out code | ~177 lines across 10 files | MEDIUM |
| TODO / auto-generated comments | 16 instances | LOW |
| Unused imports | 4 confirmed unused | LOW |
| Broad catch (Exception) | 4 occurrences | MEDIUM |
| e.printStackTrace() | 4 occurrences | MEDIUM |
| System.out.println | 1 occurrence | LOW |
| FileOutputStream resource leaks | 12 sites (no try-with-resources anywhere) | HIGH |
| Workbook never closed | 10 classes | HIGH |
| InputStream leaks in addImage* | 8 methods | MEDIUM |
| Potential NPE in addImageFromUrl | 1 occurrence | HIGH |
| Duplicated code patterns | 7 distinct duplication clusters | MEDIUM |
| Dead / test methods in base class | 9 methods | MEDIUM |
| Raw types | 4 instances | LOW |
| Deprecated API (toURL) | 1 instance | LOW |
| Missing @Override | All 9 subclasses | LOW |
| Double semicolon | 1 instance | LOW |

### Critical Path Items (HIGH severity)

1. **Resource leaks:** FileOutputStream and Workbook are never managed with try-with-resources or finally blocks across all 10 files. If an exception occurs during `wb.write(fileOut)`, file descriptors leak.
2. **Potential NPE:** `addImageFromUrl` (Frm_excel.java line 563) dereferences `ostream` outside the try block; if the catch fires, `ostream` could be null.
3. **God class:** `Frm_Linde_Reports.java` at 2,381 lines with an 18-branch if/else router should be decomposed.

---

*End of Pass 4 audit for excel/Frm_ files. Report only -- no fixes applied.*
