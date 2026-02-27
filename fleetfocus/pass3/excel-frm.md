# Pass 3 -- Documentation Audit: Excel Package (Frm_ Classes)

**Audit ID:** 2026-02-25-01-P3-excel-frm
**Agent:** A09
**Date:** 2026-02-25
**Repository:** fleetfocus
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `com.torrent.surat.fms6.excel`
**Scope:** Frm_Linde_Reports, Frm_MaxHourUsage, Frm_excel, Frm_inaUnit_rpt, Frm_month_rpt, Frm_national_rpt, Frm_nz_unitSummary_rpt, Frm_quater_rpt, Frm_simSwap_rpt, Frm_unitSummary_rpt

---

## 1. File-by-File Reading Evidence

### 1.1 Frm_excel.java (Base Class)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java`
**Lines:** 1--1164
**Class:** `public class Frm_excel`
**Class-level Javadoc:** NONE
**Extends:** Nothing (root of hierarchy)

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_excel(String docRoot, String fileName) throws Exception` | 70 | None |
| 2 | `public Frm_excel(String cust_cd, String loc_cd, String docRoot)` | 77 | None |
| 3 | `public Frm_excel() throws Exception` | 85 | None |
| 4 | `public Frm_excel(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 91 | None |
| 5 | `public Frm_excel(String cust_cd, String loc_cd, ArrayList<String> deptCdArrayList, String from, String to, String docRoot)` | 102 | None |
| 6 | `public Frm_excel(String cust_cd, String loc_cd, String dept_cd, String from, String to, String[] params, String docRoot) throws Exception` | 113 | None |
| 7 | `public Frm_excel(String cust_cd, String loc_cd, String dept_cd, String from, String to, String[] params, String docRoot, String formName) throws Exception` | 125 | None |
| 8 | `public Frm_excel(String[] params, String docRoot) throws Exception` | 138 | None |
| 9 | `public Frm_excel(String docRoot)` | 143 | None |
| 10 | `public void setParameters(boolean isConf) throws Exception` | 151 | None |
| 11 | `public String getParam(String key)` | 174 | None |
| 12 | `public String createExcel() throws IOException, SQLException` | 198 | **YES -- MISLEADING** (see findings) |
| 13 | `public void init() throws SQLException` | 209 | None |
| 14 | `public void init2() throws SQLException` | 213 | None |
| 15 | `public String createEmail() throws IOException, SQLException` | 217 | None |
| 16 | `public String createBody() throws IOException, SQLException` | 228 | None |
| 17 | `public String getBody()` | 239 | None |
| 18 | `public void setTotalDuration(String totalDuration, Cell contentCell, String style)` | 925 | None |
| 19 | `public void getCust_prefix(String cust_cd)` | 1096 | None |
| 20 | `public String getResult()` | 1100 | None |
| 21 | `public void setResult(String result)` | 1104 | None |
| 22 | `public String getTitle()` | 1108 | None |
| 23 | `public void setTitle(String title)` | 1112 | None |
| 24 | `public String getLoc_cd()` | 1116 | None |
| 25 | `public void setLoc_cd(String loc_cd)` | 1120 | None |
| 26 | `public String getCust_cd()` | 1123 | None |
| 27 | `public void setCust_cd(String cust_cd)` | 1126 | None |
| 28 | `public String getImageroot()` | 1130 | None |
| 29 | `public void setImageroot(String imageroot)` | 1134 | None |
| 30 | `public String getDocroot()` | 1138 | None |
| 31 | `public void setDocroot(String docroot)` | 1142 | None |
| 32 | `public String getDept_cd()` | 1146 | None |
| 33 | `public void setDept_cd(String dept_cd)` | 1150 | None |
| 34 | `public String getFileName()` | 1154 | None |
| 35 | `public void setFileName(String fileName)` | 1158 | None |

---

### 1.2 Frm_Linde_Reports.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_Linde_Reports.java`
**Lines:** 1--2381
**Class:** `public class Frm_Linde_Reports extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_Linde_Reports(String cust_cd, String loc_cd, String docRoot, String chart, String chart2, String st_dt, String end_dt)` | 41 | None |
| 2 | `public String createExcel(String opCode) throws Exception` | 50 | None |
| 3 | `public void setImageDir(String imageDir)` | 346 | None |
| 4 | `public void generateChart(String rpt_name) throws Exception` | 2335 | None |
| 5 | `public void setParams(String params)` | 2373 | None |
| 6 | `public void setDataArray(String[] dataArray)` | 2377 | None |

---

### 1.3 Frm_MaxHourUsage.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_MaxHourUsage.java`
**Lines:** 1--196
**Class:** `public class Frm_MaxHourUsage extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_MaxHourUsage(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 20 | None |
| 2 | `public Frm_MaxHourUsage(String cust_cd, String loc_cd, ArrayList deptCdArrayList, String from, String to, String docRoot)` | 26 | None |
| 3 | `public String createExcel() throws IOException, SQLException` | 32 | None |

---

### 1.4 Frm_inaUnit_rpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_inaUnit_rpt.java`
**Lines:** 1--227
**Class:** `public class Frm_inaUnit_rpt extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_inaUnit_rpt() throws Exception` | 21 | None |
| 2 | `public Frm_inaUnit_rpt(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 26 | None |
| 3 | `public String createExcel() throws IOException, SQLException` | 33 | None |
| 4 | `public ArrayList<Integer> getDays()` | 215 | None |
| 5 | `public void setDays(ArrayList<Integer> days)` | 219 | None |
| 6 | `public void addDays(int days)` | 223 | None |

---

### 1.5 Frm_month_rpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_month_rpt.java`
**Lines:** 1--765
**Class:** `public class Frm_month_rpt extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_month_rpt(String cust_cd, String loc_cd, String docRoot)` | 29 | None |
| 2 | `public String createExcel() throws IOException, SQLException` | 34 | None |

---

### 1.6 Frm_national_rpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_national_rpt.java`
**Lines:** 1--1210
**Class:** `public class Frm_national_rpt extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_national_rpt(String cust_cd, String loc_cd, String docRoot)` | 32 | None |
| 2 | `public String createExcel() throws IOException, SQLException` | 38 | None |

---

### 1.7 Frm_nz_unitSummary_rpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_nz_unitSummary_rpt.java`
**Lines:** 1--113
**Class:** `public class Frm_nz_unitSummary_rpt extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_nz_unitSummary_rpt() throws Exception` | 20 | None |
| 2 | `public String createExcel() throws IOException, SQLException` | 25 | None |

---

### 1.8 Frm_quater_rpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_quater_rpt.java`
**Lines:** 1--876
**Class:** `public class Frm_quater_rpt extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_quater_rpt(String cust_cd, String loc_cd, String dept_cd, String from, String to, String docRoot)` | 32 | None |
| 2 | `public Frm_quater_rpt(String cust_cd, String loc_cd, ArrayList deptCdArrayList, String from, String to, String docRoot)` | 39 | None |
| 3 | `public String createExcel() throws IOException, SQLException` | 46 | None |
| 4 | `public String getExportDir() throws Exception` | 797 | None |

---

### 1.9 Frm_simSwap_rpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_simSwap_rpt.java`
**Lines:** 1--157
**Class:** `public class Frm_simSwap_rpt extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_simSwap_rpt() throws Exception` | 19 | None |
| 2 | `public String createExcel() throws IOException, SQLException` | 24 | None |

---

### 1.10 Frm_unitSummary_rpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_unitSummary_rpt.java`
**Lines:** 1--258
**Class:** `public class Frm_unitSummary_rpt extends Frm_excel`
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `public Frm_unitSummary_rpt() throws Exception` | 20 | None |
| 2 | `public String createExcel() throws IOException, SQLException` | 25 | None |

---

## 2. Findings

### 2.1 Misleading / Inaccurate Documentation

| ID | Severity | File | Line(s) | Description |
|----|----------|------|---------|-------------|
| DOC-001 | **HIGH** | Frm_excel.java | 191--197 | **Misleading Javadoc on `createExcel()`**: The only Javadoc in the entire 10-file package reads _"Creates a PDF with information about the movies"_ with `@param filename` and `@throws DocumentException`. This method actually creates an Excel (.xlsx) workbook, not a PDF. It has no `filename` parameter, and the `DocumentException` referenced in `@throws` is never thrown. Every aspect of this Javadoc is wrong. |
| DOC-002 | **HIGH** | Frm_Linde_Reports.java | 1415 | **Misleading inline legend text**: The green legend note in `createPreopChecksCompletionTime()` states _"Green: Average Time is less than 00:00:45"_. According to the code logic at lines 1336--1342, green is applied when `ave >= 45` (i.e., 45 seconds or more), amber when `ave >= 35`, and red below 35. The green label should read _"greater than or equal to"_, not _"less than"_. This will confuse report consumers. |
| DOC-003 | **MEDIUM** | Frm_excel.java | 303 | **Inaccurate inline comment on `setFoot()`**: Comment says `//doesn't work` on a protected method that is still present in the codebase. No explanation of why it does not work, whether it is dead code, or what the intended behavior should be. |

---

### 2.2 Missing Class-Level Javadoc

| ID | Severity | File | Line | Description |
|----|----------|------|------|-------------|
| DOC-004 | **MEDIUM** | Frm_excel.java | 49 | No class-level Javadoc on the base class. This is the foundation of the entire Excel report hierarchy (9 subclasses). Lacks description of purpose, field semantics, lifecycle, and extension contract. |
| DOC-005 | **MEDIUM** | Frm_Linde_Reports.java | 26 | No class-level Javadoc. Complex 2381-line class generating 15+ different Linde/Americold report types via opCode dispatch. |
| DOC-006 | **MEDIUM** | Frm_national_rpt.java | 30 | No class-level Javadoc. 1210-line class producing national-level multi-tab report (preop, impact, unlock, utilisation). |
| DOC-007 | **MEDIUM** | Frm_quater_rpt.java | 30 | No class-level Javadoc. 876-line class producing quarterly/monthly report (preop, impact, daily usage). Class name is also misspelled ("quater" vs "quarter"). |
| DOC-008 | **MEDIUM** | Frm_month_rpt.java | 27 | No class-level Javadoc. 765-line class producing monthly cover page, impact, and utilisation reports. |
| DOC-009 | **LOW** | Frm_MaxHourUsage.java | 18 | No class-level Javadoc. |
| DOC-010 | **LOW** | Frm_inaUnit_rpt.java | 17 | No class-level Javadoc. |
| DOC-011 | **LOW** | Frm_unitSummary_rpt.java | 16 | No class-level Javadoc. |
| DOC-012 | **LOW** | Frm_simSwap_rpt.java | 15 | No class-level Javadoc. |
| DOC-013 | **LOW** | Frm_nz_unitSummary_rpt.java | 16 | No class-level Javadoc. |

---

### 2.3 Missing Method-Level Javadoc -- Complex Report Methods

| ID | Severity | File | Method | Line | Description |
|----|----------|------|--------|------|-------------|
| DOC-014 | **MEDIUM** | Frm_Linde_Reports.java | `createExcel(String opCode)` | 50 | Massive 240-line dispatcher method handling 18 distinct opCode values. No documentation of accepted opCodes, return semantics, or side effects. |
| DOC-015 | **MEDIUM** | Frm_Linde_Reports.java | `generateChart(String rpt_name)` | 2335 | Spawns an external PhantomJS process with hardcoded OS-specific paths. No documentation of expected environment, file output locations, or failure modes. |
| DOC-016 | **MEDIUM** | Frm_excel.java | `setParameters(boolean isConf)` | 151 | Parses params array, initializes UtilBean, sets multiple fields. Parameter `isConf` is accepted but never used in the method body. |
| DOC-017 | **MEDIUM** | Frm_excel.java | `createExcel()` | 198 | Base implementation creating a single "Monthly Report" sheet. Override in every subclass. Existing Javadoc is misleading (see DOC-001). |
| DOC-018 | **MEDIUM** | Frm_excel.java | `createEmail()` | 217 | Identical implementation to `createExcel()`. No documentation explaining why two identical methods exist or how they should differ. |
| DOC-019 | **MEDIUM** | Frm_excel.java | `createBody()` | 228 | Identical implementation to `createExcel()` and `createEmail()`. No documentation of purpose. |
| DOC-020 | **MEDIUM** | Frm_national_rpt.java | `createExcel()` | 38 | Generates 7 Excel tabs. No documentation of report structure or data dependencies. |
| DOC-021 | **MEDIUM** | Frm_quater_rpt.java | `createExcel()` | 46 | Generates 5 tabs (preop, impact, utilisation). No documentation. |
| DOC-022 | **MEDIUM** | Frm_month_rpt.java | `createExcel()` | 34 | Generates 5 tabs (cover, impacts, utilisation). No documentation. |
| DOC-023 | **MEDIUM** | Frm_MaxHourUsage.java | `createExcel()` | 32 | Dispatches between single-dept and group utilisation. No documentation. |
| DOC-024 | **MEDIUM** | Frm_inaUnit_rpt.java | `createExcel()` | 33 | Generates inactive unit report with configurable day thresholds. No documentation. |
| DOC-025 | **MEDIUM** | Frm_excel.java | `getParam(String key)` | 174 | Searches a string array for key=value pairs. Non-obvious format contract. No documentation. |
| DOC-026 | **MEDIUM** | Frm_excel.java | `setTotalDuration(String totalDuration, Cell contentCell, String style)` | 925 | Has a 10000-hour threshold that silently changes behavior (skips formula for large values). No documentation of this edge case. |

---

### 2.4 Missing Method-Level Javadoc -- Simple / Getter-Setter Methods

| ID | Severity | File | Methods | Lines | Description |
|----|----------|------|---------|-------|-------------|
| DOC-027 | **LOW** | Frm_excel.java | 9 constructors | 70--147 | None of the 9 overloaded constructors have Javadoc explaining which parameters are for which use case. |
| DOC-028 | **LOW** | Frm_excel.java | `init()`, `init2()` | 209, 213 | Empty hook methods with no documentation of intended override purpose. |
| DOC-029 | **LOW** | Frm_excel.java | `getBody()` | 239 | Returns empty string. No explanation of purpose or override expectation. |
| DOC-030 | **LOW** | Frm_excel.java | `getCust_prefix(String cust_cd)` | 1096 | Empty method body -- appears to be dead code. No documentation. |
| DOC-031 | **LOW** | Frm_excel.java | 16 getter/setter methods | 1100--1160 | Standard accessors with no Javadoc. |
| DOC-032 | **LOW** | Frm_Linde_Reports.java | `setImageDir()`, `setParams()`, `setDataArray()` | 346, 2373, 2377 | Simple setters, no Javadoc. |
| DOC-033 | **LOW** | Frm_inaUnit_rpt.java | `getDays()`, `setDays()`, `addDays()` | 215, 219, 223 | Simple accessors, no Javadoc. |
| DOC-034 | **LOW** | Frm_quater_rpt.java | `getExportDir()` | 797 | Computes export directory path with hardcoded path traversal. No documentation. |
| DOC-035 | **LOW** | Frm_nz_unitSummary_rpt.java | `createExcel()` | 25 | Generates NZ unit summary report. No documentation. |
| DOC-036 | **LOW** | Frm_simSwap_rpt.java | `createExcel()` | 24 | Generates SIM swap report. No documentation. |
| DOC-037 | **LOW** | Frm_unitSummary_rpt.java | `createExcel()` | 25 | Generates unit summary report. No documentation. |

---

### 2.5 TODO / FIXME Markers

| ID | Severity | File | Line(s) | Text | Description |
|----|----------|------|---------|------|-------------|
| DOC-038 | **INFO** | Frm_Linde_Reports.java | 47 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up. |
| DOC-039 | **INFO** | Frm_MaxHourUsage.java | 22, 28 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up (2 occurrences). |
| DOC-040 | **MEDIUM** | Frm_MaxHourUsage.java | 78, 156 | `// TODO needs to resize images` | Indicates known incomplete feature -- images may render incorrectly in output. Present in both `createUtilisationChart()` and `createGroupUtilisationChart()`. |
| DOC-041 | **INFO** | Frm_MaxHourUsage.java | 85, 163 | `// TODO Auto-generated catch block` | Exception silently swallowed with `e.printStackTrace()` only. Present in both private methods. |
| DOC-042 | **INFO** | Frm_inaUnit_rpt.java | 22, 30 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up (2 occurrences). |
| DOC-043 | **INFO** | Frm_month_rpt.java | 31 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up. |
| DOC-044 | **INFO** | Frm_national_rpt.java | 34 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up. |
| DOC-045 | **INFO** | Frm_quater_rpt.java | 36, 43 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up (2 occurrences). |
| DOC-046 | **INFO** | Frm_simSwap_rpt.java | 20 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up. |
| DOC-047 | **INFO** | Frm_unitSummary_rpt.java | 21 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up. |
| DOC-048 | **INFO** | Frm_nz_unitSummary_rpt.java | 21 | `// TODO Auto-generated constructor stub` | IDE-generated placeholder not cleaned up. |

---

### 2.6 Accuracy / Typo Issues in Displayed Report Labels

| ID | Severity | File | Line | Description |
|----|----------|------|------|-------------|
| DOC-049 | **MEDIUM** | Frm_month_rpt.java | 500 | Typo in report title string: `"Unit Utilisation Reort"` should be `"Unit Utilisation Report"`. This misspelling appears in the generated Excel output visible to end users. |
| DOC-050 | **LOW** | Frm_unitSummary_rpt.java | 124 | Typo in column header: `"Moderm Version"` should be `"Modem Version"`. Appears in generated Excel output. |
| DOC-051 | **INFO** | Frm_quater_rpt.java | 30 | Class name `Frm_quater_rpt` is misspelled -- should be `quarter`. This propagates into filenames and any references. |

---

## 3. Summary

| Severity | Count |
|----------|-------|
| HIGH     | 2     |
| MEDIUM   | 20    |
| LOW      | 13    |
| INFO     | 16    |
| **Total**| **51**|

### Key Observations

1. **Zero legitimate Javadoc across all 10 files.** The only Javadoc block in the entire package (on `Frm_excel.createExcel()` at line 191) is actively misleading -- it describes creating a PDF about movies, when the method creates an Excel workbook for fleet management reports.

2. **The base class `Frm_excel` is the critical documentation gap.** At 1164 lines with 9 constructors, 35 public methods, and no class-level or method-level documentation, maintainers have no way to understand the extension contract, field lifecycle, or the purpose of identically-implemented methods (`createExcel()`, `createEmail()`, `createBody()`).

3. **Complex report generation logic is entirely undocumented.** The `createExcel(String opCode)` method in `Frm_Linde_Reports` is a 240-line dispatcher handling 18 different report types with no documentation of valid opCodes. The `generateChart()` method spawns external PhantomJS processes with OS-specific hardcoded paths and no documentation of prerequisites.

4. **Two HIGH-severity misleading comments exist**: the fake PDF/movies Javadoc (DOC-001) and the incorrect green threshold legend that contradicts the actual code logic (DOC-002). Both could lead maintainers or report consumers to incorrect conclusions.

5. **16 residual IDE-generated TODO stubs** litter the codebase, plus 2 meaningful TODOs indicating known incomplete image-resize functionality in `Frm_MaxHourUsage`.

---

*End of Pass 3 audit for excel-frm scope.*
