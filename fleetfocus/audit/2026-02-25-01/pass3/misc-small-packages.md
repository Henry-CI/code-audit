# Pass 3 -- Documentation Audit: Miscellaneous Small Packages

**Audit ID:** A04
**Pass:** 3 (Documentation)
**Date:** 2026-02-25
**Auditor:** Agent A04
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Repository:** `C:\Projects\cig-audit\repos\fleetfocus`

---

## Scope

| # | File | Package |
|---|------|---------|
| 1 | `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java` | businessinsight |
| 2 | `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java` | businessinsight |
| 3 | `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java` | businessinsight |
| 4 | `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/PreOpQuestions.java` | jsonbinding.preop |
| 5 | `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/Question.java` | jsonbinding.preop |
| 6 | `WEB-INF/src/com/torrent/surat/fms6/linde/bean/SupervisorUnlockBean.java` | linde.bean |
| 7 | `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java` | repository |
| 8 | `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java` | service |

---

## Reading Evidence

### File 1: `BusinessInsight.java`

- **Class:** `BusinessInsight extends HttpServlet` (line 23)
- **Class-level Javadoc:** NONE
- **Annotations:** `@WebServlet`, `@MultipartConfig` (lines 20-21)

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public BusinessInsight()` | 31 | NONE |
| 2 | `protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException` | 41 | NONE |
| 3 | `public static String now(String dateFormat)` | 142 | NONE |

**Private methods (for context):** `getExportDir()` (line 105), `linderReportMailer(...)` (line 118)

**TODO/FIXME/HACK/XXX comments found:**
- Line 32: `// TODO Auto-generated constructor stub`

**Commented-out code:**
- Line 106: `// System.out.println();`
- Lines 109, 113-114: commented-out alternative directory logic
- Line 132: `// "julius@collectiveintelligence.com.au"` -- hardcoded email in comment

**Other observations:**
- Line 51, inline comment on `init()`: `// Function called from the jsp page.` -- this comment is on `BusinessInsightBean`, not this file; noted for context.
- Line 99: Typo in user-facing error message: `"Something went wong!"` (should be "wrong")

---

### File 2: `BusinessInsightBean.java`

- **Class:** `BusinessInsightBean` (line 23)
- **Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public void init()` | 51 | NONE (has inline comment `// Function called from the jsp page.`) |
| 2 | `public void fetchUtilImpact() throws SQLException` | 180 | NONE |
| 3 | `public void fetchUtilImpactByUnit() throws SQLException` | 305 | NONE |
| 4 | `public void fetchUtilImpactByType() throws SQLException` | 432 | NONE |
| 5 | `public void fetchExpiredLicense() throws SQLException` | 568 | NONE |
| 6 | `public void fetchTrackXHydr() throws SQLException` | 621 | NONE |
| 7 | `public void fetchLockoutStat() throws SQLException` | 688 | NONE |
| 8 | `public void fetchPreopStats() throws SQLException` | 761 | NONE |
| 9 | `public void fetchPreOPFail() throws SQLException` | 858 | NONE |
| 10 | `public void fetchPreOPFailByType() throws SQLException` | 994 | NONE |
| 11 | `public void fetchPreOPFailByUnit() throws SQLException` | 1094 | NONE |
| 12 | `public void fetchPreOPFailByDriver() throws SQLException` | 1223 | NONE |
| 13 | `public static String convert_time(String msec)` | 1347 | NONE (has inline comment describing HH:MM:SS conversion, but the method comment refers to `msec` while the actual parameter comment says "Cento Seconds" on the private variant) |
| 14 | `public String getOpCode()` | 1434 | NONE |
| 15 | `public void setOpCode(String opCode)` | 1438 | NONE |
| 16 | `public ArrayList<String> getDataArray()` | 1442 | NONE |
| 17 | `public void setDataArray(ArrayList<String> impactDataArray)` | 1446 | NONE |
| 18 | `public String getCustomerCd()` | 1450 | NONE |
| 19 | `public String getLocationCd()` | 1454 | NONE |
| 20 | `public void setCustomerCd(String customerCd)` | 1458 | NONE |
| 21 | `public void setLocationCd(String locationCd)` | 1462 | NONE |
| 22 | `public String getSt_dt()` | 1465 | NONE |
| 23 | `public String getEnd_dt()` | 1469 | NONE |
| 24 | `public void setSt_dt(String st_dt)` | 1473 | NONE |
| 25 | `public void setEnd_dt(String end_dt)` | 1477 | NONE |
| 26 | `public ArrayList<String> getModelList()` | 1481 | NONE |

**Misleading comments found:**
- Line 95: Exception handler prints `"Exception in LindeReportsBean"` but this class is `BusinessInsightBean`
- Line 306: `methodName = "fetchUtilImpact()"` inside `fetchUtilImpactByUnit()` -- wrong method name
- Line 433: `methodName = "fetchUtilImpact()"` inside `fetchUtilImpactByType()` -- wrong method name
- Line 622: `methodName = "fetchExpiredLicense()"` inside `fetchTrackXHydr()` -- wrong method name
- Line 762: `methodName = "fetchNationalPreopCheckCompletionTime()"` inside `fetchPreopStats()` -- wrong method name (method does not exist in class)
- Line 859: `methodName = "fetchPreOPFail()"` inside `fetchPreOPFail()` -- correct
- Line 995: `methodName = "fetchPreOPFail()"` inside `fetchPreOPFailByType()` -- wrong method name
- Line 1095: `methodName = "fetchPreOPFail()"` inside `fetchPreOPFailByUnit()` -- wrong method name
- Line 1224: `methodName = "fetchPreOPFail()"` inside `fetchPreOPFailByDriver()` -- wrong method name

**Inline comment accuracy issues:**
- Line 1334-1337: `convert_time1` private method comment says "Calculates and returns the time (HH:MM:SS format)" but actually returns decimal hours (e.g., "1.50"), not HH:MM:SS
- Line 1347-1348: `convert_time` public method comment says "Calculates and returns the time" -- truncated / incomplete comment

---

### File 3: `BusinessInsightExcel.java`

- **Class:** `BusinessInsightExcel extends Frm_excel` (line 17)
- **Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public BusinessInsightExcel(String cust_cd, String loc_cd, String docRoot)` | 24 | NONE |
| 2 | `public String createExcel(String opCode) throws Exception` | 28 | NONE |
| 3 | `public String getSt_dt()` | 1037 | NONE |
| 4 | `public String getEnd_dt()` | 1041 | NONE |
| 5 | `public void setSt_dt(String st_dt)` | 1045 | NONE |
| 6 | `public void setEnd_dt(String end_dt)` | 1049 | NONE |

**Private methods (for context):** `createUtilImpact` (99), `createUtilImpactbyUnit` (180), `createUtilImpactbyType` (278), `createLockoutStatus` (358), `createPreopStat` (476), `createLicenseExpiredReport` (623), `creatTracXHydrReport` (690), `createPreopFail` (767), `createPreopFailByType` (847), `createPreopFailByUnit` (910), `createPreopFailByDriver` (974)

**TODO/FIXME/HACK/XXX comments found:** NONE

---

### File 4: `PreOpQuestions.java`

- **Class:** `PreOpQuestions` (line 5)
- **Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public PreOpQuestions(String utcTimestamp, boolean randomiseOrder, List<Question> questions)` | 17 | Partial -- has `@param` tags but all descriptions are empty |
| 2 | `public String getUtcTimestamp()` | 25 | NONE |
| 3 | `public void setUtcTimestamp(String utcTimestamp)` | 29 | NONE |
| 4 | `public boolean isRandomiseOrder()` | 33 | NONE |
| 5 | `public void setRandomiseOrder(boolean randomiseOrder)` | 37 | NONE |
| 6 | `public List<Question> getQuestions()` | 41 | NONE |
| 7 | `public void setQuestions(List<Question> questions)` | 45 | NONE |
| 8 | `public String toString()` | 50 | NONE (Override) |

**Existing Javadoc accuracy:** Constructor (lines 11-16) has a Javadoc block with `@param` tags but parameters are listed in wrong order (`utcTimestamp, questions, randomiseOrder`) vs actual signature order (`utcTimestamp, randomiseOrder, questions`), and all `@param` descriptions are empty.

---

### File 5: `Question.java`

- **Class:** `Question` (line 3)
- **Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public Question(long index, long id, String critical, boolean excludeRandom, String eng, String spa, String tha)` | 23 | Partial -- has `@param` tags but all descriptions are empty |
| 2 | `public long getIndex()` | 35 | NONE |
| 3 | `public void setIndex(long index)` | 39 | NONE |
| 4 | `public long getId()` | 43 | NONE |
| 5 | `public void setId(long id)` | 47 | NONE |
| 6 | `public String getCritical()` | 51 | NONE |
| 7 | `public void setCritical(String critical)` | 55 | NONE |
| 8 | `public boolean isExcludeRandom()` | 59 | NONE |
| 9 | `public void setExcludeRandom(boolean excludeRandom)` | 63 | NONE |
| 10 | `public String getEng()` | 67 | NONE |
| 11 | `public void setEng(String eng)` | 71 | NONE |
| 12 | `public String getSpa()` | 75 | NONE |
| 13 | `public void setSpa(String spa)` | 79 | NONE |
| 14 | `public String getTha()` | 83 | NONE |
| 15 | `public void setTha(String tha)` | 87 | NONE |
| 16 | `public String toString()` | 92 | NONE (Override) |

**Existing Javadoc accuracy:** Constructor (lines 13-22) has `@param` tags in incorrect order (`excludeRandom, critical, spa, index, id, tha, eng`) vs actual signature order (`index, id, critical, excludeRandom, eng, spa, tha`). All `@param` descriptions are empty.

---

### File 6: `SupervisorUnlockBean.java`

- **Class:** `SupervisorUnlockBean` (line 3)
- **Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public SupervisorUnlockBean()` | 11 | NONE |
| 2 | `public String getSupervisorName()` | 15 | NONE |
| 3 | `public int getImpactCount()` | 19 | NONE |
| 4 | `public int getSurveyCount()` | 23 | NONE |
| 5 | `public int getCriticalCount()` | 27 | NONE |
| 6 | `public void setSupervisorName(String supervisorName)` | 31 | NONE |
| 7 | `public void setImpactCount(int impactCount)` | 35 | NONE |
| 8 | `public void setSurveyCount(int surveyCount)` | 39 | NONE |
| 9 | `public void setCriticalCount(int criticalCount)` | 43 | NONE |
| 10 | `public String toString()` | 47 | NONE (Override) |
| 11 | `public int getGrandTotal()` | 51 | NONE |

**TODO/FIXME/HACK/XXX comments found:**
- Line 12: `// TODO Auto-generated constructor stub`

---

### File 7: `FmsChklistLangSettingRepo.java`

- **Class:** `FmsChklistLangSettingRepo` (line 14)
- **Class-level Javadoc:** YES -- `"Repository (CRUD operation) for Table FMS_CHCKLIST_LANG_SETTING"` (lines 10-13)

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public FmsChklistLangSettingRepo(Statement stmt)` | 21 | NONE (but there is a field-level Javadoc comment on `stmt` at lines 16-18) |
| 2 | `public List<String> queryLangConfigBy(String custCd, String locCd, String deptCd, String vehTypeCd) throws SQLException` | 26 | NONE |
| 3 | `public int updateLanguageBy(List<String> langChoice, String custCd, String locCd, String deptCd, String vehTypeCd) throws SQLException` | 45 | NONE |
| 4 | `public int insertBy(String custCd, String locCd, String deptCd, String vehTypeCd, String langChoice) throws SQLException` | 60 | NONE |

**Existing Javadoc accuracy:** Class-level Javadoc is accurate. Field-level comment on `stmt` (lines 16-18) is helpful and accurate.

---

### File 8: `HireDehireService.java`

- **Class:** `HireDehireService` (line 14)
- **Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public Map<String, List<DehireBean>> getUnitsHireDehireTime(Statement stmt, String custCd, String locCd, String deptCd, String searchCrit, String vehTypeCd)` | 18 | NONE |

**Inline comment:**
- Line 15: `// alphabets and spaces only` -- accurate description of the regex pattern on line 16.

---

## Findings

### A04-1 -- HIGH -- Misleading `methodName` assignments in `BusinessInsightBean`

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 306, 433, 622, 762, 995, 1095, 1224

Multiple methods set the `methodName` field to an incorrect value, pointing to a different method or a non-existent method. This would produce misleading diagnostic output if `methodName` were ever logged or displayed during debugging.

| Method | Line | `methodName` Set To | Correct Value |
|--------|------|---------------------|---------------|
| `fetchUtilImpactByUnit()` | 306 | `"fetchUtilImpact()"` | `"fetchUtilImpactByUnit()"` |
| `fetchUtilImpactByType()` | 433 | `"fetchUtilImpact()"` | `"fetchUtilImpactByType()"` |
| `fetchTrackXHydr()` | 622 | `"fetchExpiredLicense()"` | `"fetchTrackXHydr()"` |
| `fetchPreopStats()` | 762 | `"fetchNationalPreopCheckCompletionTime()"` | `"fetchPreopStats()"` |
| `fetchPreOPFailByType()` | 995 | `"fetchPreOPFail()"` | `"fetchPreOPFailByType()"` |
| `fetchPreOPFailByUnit()` | 1095 | `"fetchPreOPFail()"` | `"fetchPreOPFailByUnit()"` |
| `fetchPreOPFailByDriver()` | 1224 | `"fetchPreOPFail()"` | `"fetchPreOPFailByDriver()"` |

---

### A04-2 -- HIGH -- Misleading exception message references wrong class name

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Line:** 95

The `catch` block in `init()` prints `"Exception in LindeReportsBean"` but the class is `BusinessInsightBean`. This would mislead anyone investigating production exceptions.

---

### A04-3 -- HIGH -- Misleading inline comment on `convert_time1` (wrong format description)

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 1334-1337

The private method `convert_time1(String csec)` has an inline comment stating it "Calculates and returns the time (HH:MM:SS format)" but the method actually returns decimal hours (e.g., `"1.50"`) via `DecimalFormat("#0.00")`. The comment is factually incorrect and would mislead a developer trying to understand the return value format.

---

### A04-4 -- HIGH -- `@param` tags in wrong order in `PreOpQuestions` constructor Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/PreOpQuestions.java`
**Lines:** 11-16

The constructor Javadoc lists `@param` tags in order `utcTimestamp, questions, randomiseOrder`, but the actual constructor signature order is `utcTimestamp, randomiseOrder, questions`. Additionally, all `@param` descriptions are empty, making the Javadoc block useless.

---

### A04-5 -- HIGH -- `@param` tags in wrong order in `Question` constructor Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/Question.java`
**Lines:** 13-22

The constructor Javadoc lists `@param` tags in order `excludeRandom, critical, spa, index, id, tha, eng`, but the actual constructor signature order is `index, id, critical, excludeRandom, eng, spa, tha`. All `@param` descriptions are empty.

---

### A04-6 -- MEDIUM -- Missing Javadoc on all public methods in `BusinessInsightBean` (complex data-fetching logic)

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 51, 180, 305, 432, 568, 621, 688, 761, 858, 994, 1094, 1223, 1347

26 public methods have no Javadoc. The 12 `fetch*()` methods and `init()` contain complex SQL query construction and business logic. Without documentation, the purpose of each report type, its parameters, and the format of data written to `dataArray` are undiscoverable without full code reading. The public `convert_time(String msec)` utility method also lacks documentation.

**Undocumented complex public methods:**
- `init()` (line 51) -- dispatches to report fetchers based on opCode, manages DB connections
- `fetchUtilImpact()` (line 180) -- impact utilisation ratio by driver
- `fetchUtilImpactByUnit()` (line 305) -- impact utilisation ratio by unit
- `fetchUtilImpactByType()` (line 432) -- impact utilisation ratio by vehicle type
- `fetchExpiredLicense()` (line 568) -- expired license report
- `fetchTrackXHydr()` (line 621) -- traction vs hydraulic time report
- `fetchLockoutStat()` (line 688) -- lockout time statistics
- `fetchPreopStats()` (line 761) -- pre-op check completion time statistics
- `fetchPreOPFail()` (line 858) -- pre-op check failures by type/unit/driver
- `fetchPreOPFailByType()` (line 994) -- pre-op failures grouped by vehicle type
- `fetchPreOPFailByUnit()` (line 1094) -- pre-op failures grouped by unit
- `fetchPreOPFailByDriver()` (line 1223) -- pre-op failures grouped by driver
- `convert_time(String msec)` (line 1347) -- time conversion utility (public static)

---

### A04-7 -- MEDIUM -- Missing Javadoc on `BusinessInsight` servlet class and its `doPost` method

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Lines:** 23, 41

The servlet class has no class-level Javadoc explaining its URL mapping, purpose, or expected request parameters. The `doPost` method contains non-trivial validation and report-generation-then-email logic with no documentation of expected parameters (`email`, `customer`, `location`, `insight_report`, `st_dt`, `to_dt`) or response format (JSON).

---

### A04-8 -- MEDIUM -- Missing Javadoc on `BusinessInsightExcel.createExcel()` method

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
**Line:** 28

The `createExcel(String opCode)` method is the primary entry point for Excel report generation, dispatching to 10 different report types based on `opCode`. There is no documentation of valid `opCode` values, return value semantics, or thrown exceptions.

---

### A04-9 -- MEDIUM -- Missing Javadoc on all CRUD methods in `FmsChklistLangSettingRepo`

**File:** `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java`
**Lines:** 21, 26, 45, 60

Despite having a good class-level Javadoc, none of the four public methods (constructor, `queryLangConfigBy`, `updateLanguageBy`, `insertBy`) have method-level Javadoc. The `queryLangConfigBy` and `updateLanguageBy` methods have non-obvious behavior (e.g., defaulting to English, comma-separated string storage) that should be documented.

---

### A04-10 -- MEDIUM -- Missing Javadoc on `HireDehireService.getUnitsHireDehireTime()`

**File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java`
**Line:** 18

This is the sole public method in the service class and takes 6 parameters. It contains complex SQL with dynamic WHERE clause construction, a UNION ALL query across current and historical vehicle relationships, and returns a `Map<String, List<DehireBean>>`. There is no documentation of parameters, return value structure, or the fact that `"All"` is treated as a wildcard for filter parameters.

---

### A04-11 -- MEDIUM -- Missing class-level Javadoc on `BusinessInsight`, `BusinessInsightBean`, `BusinessInsightExcel`, `HireDehireService`

**Files:**
- `BusinessInsight.java` (line 23)
- `BusinessInsightBean.java` (line 23)
- `BusinessInsightExcel.java` (line 17)
- `HireDehireService.java` (line 14)

Four classes with significant business logic have no class-level Javadoc. These classes handle report generation, data fetching, and hire/dehire service operations that are central to the business insight module.

---

### A04-12 -- LOW -- Missing Javadoc on getter/setter methods across all files

**Files:** `BusinessInsightBean.java`, `BusinessInsightExcel.java`, `PreOpQuestions.java`, `Question.java`, `SupervisorUnlockBean.java`

Simple getter/setter methods across the audited files lack Javadoc. Total count:

| File | Undocumented Getter/Setters |
|------|-----------------------------|
| BusinessInsightBean.java | 12 (getOpCode, setOpCode, getDataArray, setDataArray, getCustomerCd, getLocationCd, setCustomerCd, setLocationCd, getSt_dt, getEnd_dt, setSt_dt, setEnd_dt, getModelList) |
| BusinessInsightExcel.java | 4 (getSt_dt, getEnd_dt, setSt_dt, setEnd_dt) |
| PreOpQuestions.java | 6 (getUtcTimestamp, setUtcTimestamp, isRandomiseOrder, setRandomiseOrder, getQuestions, setQuestions) |
| Question.java | 14 (getIndex, setIndex, getId, setId, getCritical, setCritical, isExcludeRandom, setExcludeRandom, getEng, setEng, getSpa, setSpa, getTha, setTha) |
| SupervisorUnlockBean.java | 9 (getSupervisorName, getImpactCount, getSurveyCount, getCriticalCount, setSupervisorName, setImpactCount, setSurveyCount, setCriticalCount, getGrandTotal) |

---

### A04-13 -- LOW -- Missing class-level Javadoc on POJO/bean classes

**Files:**
- `PreOpQuestions.java` (line 5)
- `Question.java` (line 3)
- `SupervisorUnlockBean.java` (line 3)

Three data-holding classes have no class-level Javadoc explaining their purpose or usage context (e.g., JSON serialization target, supervisor unlock tracking).

---

### A04-14 -- INFO -- TODO comments left from auto-generated code

**Files:**
- `BusinessInsight.java` line 32: `// TODO Auto-generated constructor stub`
- `SupervisorUnlockBean.java` line 12: `// TODO Auto-generated constructor stub`

IDE-generated TODO comments remain in production code. These are not actionable and should either be resolved or removed.

---

### A04-15 -- INFO -- Commented-out debug code in `BusinessInsight.java`

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Lines:** 106, 109, 113-114, 132

Multiple lines of commented-out code remain, including alternative directory computation logic and a hardcoded developer email address (`julius@collectiveintelligence.com.au`).

---

### A04-16 -- INFO -- `BusinessInsight.now()` public utility method undocumented

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Line:** 142

A public static utility method `now(String dateFormat)` has no Javadoc. It is simple (returns current time formatted with the given pattern), but its public static visibility means it could be called from anywhere.

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | 5     |
| MEDIUM   | 5     |
| LOW      | 2     |
| INFO     | 3     |
| **Total** | **15** |

**Key observations:**
1. The `businessinsight` package is the most poorly documented area, with zero Javadoc across all three classes and multiple misleading comments (wrong class names, wrong method names, incorrect format descriptions).
2. The `jsonbinding.preop` package has auto-generated Javadoc stubs with empty `@param` descriptions and incorrect parameter ordering -- worse than having no Javadoc at all.
3. `FmsChklistLangSettingRepo` is the only class with any class-level Javadoc, and it is accurate.
4. Seven out of eight files have zero method-level Javadoc.
5. The `BusinessInsightBean` class has the highest density of misleading comments (7 wrong `methodName` assignments, 1 wrong class name in exception message, 1 wrong format description in inline comment).
