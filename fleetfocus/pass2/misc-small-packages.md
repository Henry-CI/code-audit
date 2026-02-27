# Pass 2 -- Test Coverage: Miscellaneous Small Packages
**Agent:** A04
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|---|---|
| Test framework (JUnit / TestNG) | **ABSENT** -- no test dependencies found in project |
| Test source directory (`test/`, `src/test/`) | **ABSENT** -- no test directories exist |
| Test files matching `*Test.java` / `*Spec.java` | **ZERO** files found |
| Mocking framework (Mockito, EasyMock, etc.) | **ABSENT** |
| CI test execution configuration | **Not evident** |
| Code coverage tooling (JaCoCo, Cobertura) | **ABSENT** |

**Conclusion:** The entire repository has zero automated test coverage. Every class below has 0% line, branch, and method coverage. All findings below are predicated on this total absence.

---

## Reading Evidence

### 1. BusinessInsight.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
- **Class:** `BusinessInsight extends HttpServlet` (148 lines)
- **Annotations:** `@WebServlet(name = "BusinessInsight", urlPatterns = {"/servlet/BusinessInsight"})`, `@MultipartConfig`
- **Fields / Constants:**
  - `private static final long serialVersionUID = -7797674910705534506L` (line 28)
  - `private static Logger log` (line 35)
  - `private String message = ""` (line 37)
  - `int dHolder = 0` (line 38, package-private)
- **Public methods:**
  - `public BusinessInsight()` -- default constructor (line 31)
  - `public static String now(String dateFormat)` -- formats current date/time (line 142)
- **Protected methods:**
  - `protected void doPost(HttpServletRequest, HttpServletResponse) throws ServletException, IOException` (line 41)
- **Private methods:**
  - `private String getExportDir() throws Exception` (line 105)
  - `private void linderReportMailer(String, String, String, String)` (line 118)

---

### 2. BusinessInsightBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
- **Class:** `BusinessInsightBean` (1485 lines)
- **Fields (all package-private):**
  - `HttpServletRequest request` (line 25)
  - `Connection conn` (line 26)
  - `Statement stmt, stmt1, stmt2, stmt3, stmt4` (lines 27-31)
  - `ResultSet rset, rset1, rset2, rset3, rset4` (lines 32-36)
  - `String query, methodName, opCode, customerCd, locationCd, st_dt, end_dt` (lines 37-44)
  - `ArrayList<String> dataArray` (line 46)
  - `ArrayList<String> modelList` (line 47)
  - `DecimalFormat df` (line 49)
- **Public methods:**
  - `public void init()` -- JNDI lookup + dispatches by opCode (line 51)
  - `public void fetchUtilImpact() throws SQLException` (line 180)
  - `public void fetchUtilImpactByUnit() throws SQLException` (line 305)
  - `public void fetchUtilImpactByType() throws SQLException` (line 432)
  - `public void fetchExpiredLicense() throws SQLException` (line 568)
  - `public void fetchTrackXHydr() throws SQLException` (line 621)
  - `public void fetchLockoutStat() throws SQLException` (line 688)
  - `public void fetchPreopStats() throws SQLException` (line 761)
  - `public void fetchPreOPFail() throws SQLException` (line 858)
  - `public void fetchPreOPFailByType() throws SQLException` (line 994)
  - `public void fetchPreOPFailByUnit() throws SQLException` (line 1094)
  - `public void fetchPreOPFailByDriver() throws SQLException` (line 1223)
  - `public static String convert_time(String msec)` (line 1347)
  - Getters/Setters: `getOpCode()` (line 1434), `setOpCode(String)` (line 1438), `getDataArray()` (line 1442), `setDataArray(ArrayList<String>)` (line 1446), `getCustomerCd()` (line 1450), `getLocationCd()` (line 1454), `setCustomerCd(String)` (line 1458), `setLocationCd(String)` (line 1462), `getSt_dt()` (line 1465), `getEnd_dt()` (line 1469), `setSt_dt(String)` (line 1473), `setEnd_dt(String)` (line 1477), `getModelList()` (line 1481)
- **Private methods:**
  - `private String convert_time1(String csec)` (line 1334)
  - `private String ratio(int a, int b)` (line 1418)

---

### 3. BusinessInsightExcel.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
- **Class:** `BusinessInsightExcel extends Frm_excel` (1053 lines)
- **Fields:**
  - `String op_code = ""` (line 19, package-private)
  - `DecimalFormat df = new DecimalFormat("#0.00")` (line 20)
  - `String st_dt = ""` (line 21)
  - `String end_dt = ""` (line 22)
- **Public methods:**
  - `public BusinessInsightExcel(String cust_cd, String loc_cd, String docRoot)` -- constructor (line 24)
  - `public String createExcel(String opCode) throws Exception` -- master dispatch; creates Excel workbook (line 28)
  - `public String getSt_dt()` (line 1037)
  - `public String getEnd_dt()` (line 1041)
  - `public void setSt_dt(String)` (line 1045)
  - `public void setEnd_dt(String)` (line 1049)
- **Private methods (10 report generators):**
  - `createUtilImpact(Sheet)` (line 99)
  - `createUtilImpactbyUnit(Sheet)` (line 180)
  - `createUtilImpactbyType(Sheet)` (line 278)
  - `createLockoutStatus(Sheet)` (line 358)
  - `createPreopStat(Sheet)` (line 476)
  - `createLicenseExpiredReport(Sheet)` (line 623)
  - `creatTracXHydrReport(Sheet)` (line 690)
  - `createPreopFail(Sheet)` (line 767)
  - `createPreopFailByType(Sheet)` (line 847)
  - `createPreopFailByUnit(Sheet)` (line 910)
  - `createPreopFailByDriver(Sheet)` (line 974)

---

### 4. PreOpQuestions.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/PreOpQuestions.java`
- **Class:** `PreOpQuestions` (75 lines)
- **Fields (private):**
  - `String utcTimestamp` (line 7)
  - `boolean randomiseOrder` (line 8)
  - `List<Question> questions` (line 9)
- **Public methods:**
  - `public PreOpQuestions(String, boolean, List<Question>)` -- constructor (line 17)
  - `public String getUtcTimestamp()` (line 25)
  - `public void setUtcTimestamp(String)` (line 29)
  - `public boolean isRandomiseOrder()` (line 33)
  - `public void setRandomiseOrder(boolean)` (line 37)
  - `public List<Question> getQuestions()` (line 41)
  - `public void setQuestions(List<Question>)` (line 45)
  - `public String toString()` -- override (line 49)

---

### 5. Question.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/Question.java`
- **Class:** `Question` (133 lines)
- **Fields (private):**
  - `long index` (line 5)
  - `long id` (line 6)
  - `String critical` (line 7)
  - `boolean excludeRandom` (line 8)
  - `String eng` (line 9)
  - `String spa` (line 10)
  - `String tha` (line 11)
- **Public methods:**
  - `public Question(long, long, String, boolean, String, String, String)` -- constructor (line 23)
  - `public long getIndex()` (line 35)
  - `public void setIndex(long)` (line 39)
  - `public long getId()` (line 43)
  - `public void setId(long)` (line 47)
  - `public String getCritical()` (line 51)
  - `public void setCritical(String)` (line 55)
  - `public boolean isExcludeRandom()` (line 59)
  - `public void setExcludeRandom(boolean)` (line 63)
  - `public String getEng()` (line 67)
  - `public void setEng(String)` (line 71)
  - `public String getSpa()` (line 75)
  - `public void setSpa(String)` (line 79)
  - `public String getTha()` (line 83)
  - `public void setTha(String)` (line 87)
  - `public String toString()` -- override (line 92)

---

### 6. SupervisorUnlockBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/linde/bean/SupervisorUnlockBean.java`
- **Class:** `SupervisorUnlockBean` (54 lines)
- **Fields (package-private):**
  - `String supervisorName` (line 5)
  - `int impactCount` (line 6)
  - `int surveyCount` (line 7)
  - `int criticalCount` (line 8)
  - `int grandTotal` (line 9)
- **Public methods:**
  - `public SupervisorUnlockBean()` -- default constructor (line 11)
  - `public String getSupervisorName()` (line 15)
  - `public int getImpactCount()` (line 19)
  - `public int getSurveyCount()` (line 23)
  - `public int getCriticalCount()` (line 27)
  - `public void setSupervisorName(String)` (line 31)
  - `public void setImpactCount(int)` (line 35)
  - `public void setSurveyCount(int)` (line 39)
  - `public void setCriticalCount(int)` (line 43)
  - `public String toString()` -- override (line 47)
  - `public int getGrandTotal()` -- computed field: impactCount + surveyCount + criticalCount (line 51)

---

### 7. FmsChklistLangSettingRepo.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java`
- **Class:** `FmsChklistLangSettingRepo` (76 lines)
- **Fields:**
  - `private Statement stmt` (line 19)
- **Public methods:**
  - `public FmsChklistLangSettingRepo(Statement)` -- constructor (line 21)
  - `public List<String> queryLangConfigBy(String custCd, String locCd, String deptCd, String vehTypeCd) throws SQLException` (line 26)
  - `public int updateLanguageBy(List<String> langChoice, String custCd, String locCd, String deptCd, String vehTypeCd) throws SQLException` (line 45)
  - `public int insertBy(String custCd, String locCd, String deptCd, String vehTypeCd, String langChoice) throws SQLException` (line 60)
- **Private methods:**
  - `private void doClose(ResultSet)` (line 67)

---

### 8. HireDehireService.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java`
- **Class:** `HireDehireService` (127 lines)
- **Fields:**
  - `Pattern pattern = Pattern.compile("^[A-Za-z\\s]*$")` (line 16)
- **Public methods:**
  - `public Map<String, List<DehireBean>> getUnitsHireDehireTime(Statement stmt, String custCd, String locCd, String deptCd, String searchCrit, String vehTypeCd)` (line 18)

---

## Findings

### A04-01 -- Zero test coverage across all 8 files (systemic)
- **File:** All files in scope
- **Severity:** CRITICAL
- **Category:** Test Coverage -- Total Absence
- **Description:** None of the 8 files have any associated test classes. There are zero unit tests, zero integration tests, and zero coverage tooling in the entire repository. This means every public method, every error path, every edge case, and every SQL query is completely unverified by automated testing.
- **Evidence:** No `test/` or `src/test/` directory exists. No files matching `*Test.java`, `*Spec.java`, or `*IT.java` patterns found. No JUnit/TestNG/Mockito dependencies detected.
- **Recommendation:** Establish a test infrastructure (JUnit 5 + Mockito at minimum). Prioritize the files listed in A04-02 through A04-12 below, starting with the SQL-injection-vulnerable classes.

---

### A04-02 -- BusinessInsightBean: 12 public data-fetching methods with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage -- Business Logic
- **Description:** BusinessInsightBean contains 12 public fetch methods (`fetchUtilImpact`, `fetchUtilImpactByUnit`, `fetchUtilImpactByType`, `fetchExpiredLicense`, `fetchTrackXHydr`, `fetchLockoutStat`, `fetchPreopStats`, `fetchPreOPFail`, `fetchPreOPFailByType`, `fetchPreOPFailByUnit`, `fetchPreOPFailByDriver`, plus `init`) that each build and execute multiple raw SQL queries with string concatenation. These methods directly manipulate shared mutable state (`dataArray`, `rset`, `stmt` fields) and contain complex parsing logic (splitting strings by delimiters, integer parsing). None are tested.
- **Evidence:** All 12 methods concatenate `customerCd`, `locationCd`, `st_dt`, `end_dt` directly into SQL strings (e.g., lines 206-210, 327-333, 463-469, 587-597, 642-650, 709-714, 783-788). The `convert_time` (line 1347) and `convert_time1` (line 1334) utility methods perform arithmetic that is error-prone (integer division truncation at line 1341, negative time handling at line 1357). The `ratio` method (line 1418) has a potential division-by-zero if `min == 0` at line 1421.
- **Recommendation:** Create `BusinessInsightBeanTest.java` with tests for: (1) `convert_time` with values 0, negative, boundary values; (2) `convert_time1` with edge cases; (3) `ratio` with min=0, equal values, coprime values; (4) mock-based tests for each fetch method verifying correct data assembly into `dataArray`.

---

### A04-03 -- BusinessInsightBean: SQL injection via string concatenation in all fetch methods
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage -- Security
- **Description:** All 12 fetch methods build SQL queries by concatenating user-supplied parameters (`customerCd`, `locationCd`, `st_dt`, `end_dt`) directly into query strings without using PreparedStatement or any form of input sanitization. Without tests, there is no validation that these parameters are safe. A test suite should verify rejection of malicious input.
- **Evidence:** Line 209: `" r.\"USER_CD\" = " + customerCd`; Line 253-255: `"...\"utc_time\" >= '" + st_dt + "'::timestamp..."`. These patterns repeat in every fetch method (lines 332, 467-469, 594-596, 646-648, 713-714, 787-788, 893-895, 1030-1032, 1131-1133, 1259-1261). Parameters originate from `BusinessInsight.doPost()` which reads `request.getParameter()` without sanitization (lines 47-52).
- **Recommendation:** Tests should verify that SQL injection payloads in `customerCd`, `locationCd`, `st_dt`, `end_dt` are either rejected or safely handled. Long-term: migrate to PreparedStatement.

---

### A04-04 -- BusinessInsight servlet: doPost validation logic untested
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
- **Severity:** HIGH
- **Category:** Test Coverage -- Input Validation
- **Description:** The `doPost` method (line 41) contains multiple validation branches for empty dates, empty customer/location, and empty email. It also has exception handling (line 97) that silently swallows errors (printing stack trace only). None of these paths are tested.
- **Evidence:** Lines 54-58: date validation branch. Lines 59-63: customer/location validation. Lines 65-68: email validation. Line 72: insight_report dispatch. Line 97-101: catch-all exception handler with typo in message ("wong" instead of "wrong" at line 99). The `getExportDir()` method (line 105) uses fragile path manipulation (substring, counting slashes, hardcoded relative path traversal `/../../../../../../../excelrpt/`).
- **Recommendation:** Create servlet test with mocked `HttpServletRequest`/`HttpServletResponse` to verify each validation branch returns correct JSON error response, and test the `getExportDir()` path construction.

---

### A04-05 -- BusinessInsightExcel: createExcel dispatch and 10 report generators untested
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
- **Severity:** HIGH
- **Category:** Test Coverage -- Report Generation
- **Description:** `createExcel` (line 28) dispatches to 10 different private report-generation methods via an if-else chain on `opCode`. Each method parses delimited strings from `BusinessInsightBean.getDataArray()` using `split(",")` or `split("#,#")` and performs `Integer.parseInt` / `Double.parseDouble` without null/format checks. A malformed data string would cause `ArrayIndexOutOfBoundsException` or `NumberFormatException`. Additionally, there is a potential division-by-zero at line 151 (`double impXHour = duration / impact`) that is only guarded afterward (lines 153-155), and similarly at lines 240, 330, 470 (`totalAve/count * 10`), and line 581 (`avg/qCount * 10`).
- **Evidence:** Line 147: `String[] data = beanList.get(i).split("#,#")` followed by `data[0].split(":")[1]` -- no bounds check. Line 151: division `duration / impact` before check `if (impact == 0 || duration == 0)`. Line 470: integer division `totalAve/count * 10` uses integer arithmetic losing precision. Line 581: `avg/qCount * 10` will throw ArithmeticException if `qCount == 0`.
- **Recommendation:** Write unit tests with mocked `BusinessInsightBean` to verify: (1) correct opCode dispatch; (2) handling of empty data arrays; (3) malformed delimited strings; (4) zero-value edge cases for division; (5) generated Excel file structure.

---

### A04-06 -- FmsChklistLangSettingRepo: SQL injection in all three CRUD methods
- **File:** `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage -- Security / Data Integrity
- **Description:** All three public methods (`queryLangConfigBy`, `updateLanguageBy`, `insertBy`) build SQL via string concatenation with unsanitized parameters. The repository has zero tests to verify correct query assembly, correct result parsing, or behavior with malicious input.
- **Evidence:** Line 30-31: `"...where \"cust_cd\" = '" + custCd + "' and \"loc_cd\" = '" + locCd + "'..."`. Line 54-55: same pattern in UPDATE. Line 61-62: same pattern in INSERT. The `updateLanguageBy` method (line 45) also has a string manipulation bug risk: `langChoiceAsList.toString().replace("[", "").replace("]", "").replace(" ", "")` -- if any language code contains brackets or spaces, data corruption would result.
- **Recommendation:** Create `FmsChklistLangSettingRepoTest.java` with a mocked Statement to test: (1) `queryLangConfigBy` with null result set, empty result, valid result; (2) `updateLanguageBy` with empty list (English default behavior, line 51), list with nulls/blanks; (3) `insertBy` with special characters; (4) SQL injection payloads in all parameters.

---

### A04-07 -- FmsChklistLangSettingRepo: queryLangConfigBy edge cases unverified
- **File:** `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java`
- **Severity:** HIGH
- **Category:** Test Coverage -- Edge Cases
- **Description:** `queryLangConfigBy` (line 26) returns `Arrays.asList(rset.getString(1).split(","))` when a row is found, but the returned list from `Arrays.asList` is fixed-size (cannot add/remove elements). If callers attempt to modify the returned list, it will throw `UnsupportedOperationException`. Additionally, if the database value is a single empty string, `split(",")` returns `[""]` rather than an empty list.
- **Evidence:** Line 36: `Arrays.asList(rset.getString(1).split(","))` -- returns fixed-size list. The caller `updateLanguageBy` at line 46 wraps it in `new ArrayList<>(langChoice)` which is safe, but external callers may not.
- **Recommendation:** Test that callers can handle the fixed-size list. Test behavior when `lang_config` column value is empty string, null, single value, or comma-delimited values.

---

### A04-08 -- HireDehireService: complex SQL construction with multiple optional filters untested
- **File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage -- Business Logic / Security
- **Description:** `getUnitsHireDehireTime` (line 18) builds a complex UNION ALL SQL query with up to 4 optional WHERE clause conditions based on `locCd`, `deptCd`, `searchCrit`, and `vehTypeCd`. The method uses string concatenation for SQL (no PreparedStatement), has an early return for null/empty/All custCd, and silently swallows all exceptions via `e.printStackTrace()` (line 113). The search criteria filter applies a regex pattern check (line 55) but only adds a SQL condition for non-letter inputs (line 65-70), meaning pure letter-based search criteria are silently ignored -- a likely bug.
- **Evidence:** Lines 24-25: `"where fuvr.\"USER_CD\" = " + custCd` -- direct SQL concatenation. Lines 54-70: `searchCrit` is checked against a letters-only regex, but the `if (!searchCritLettersOnly)` block at line 65 means searches containing only letters are completely skipped with no filter applied. Lines 66-69: LIKE clauses use `searchCrit.trim().toLowerCase()` concatenated into SQL. Line 112: catch swallows all exceptions. Lines 116-122: Statement is closed in finally block but ResultSet `rset` is never explicitly closed.
- **Recommendation:** Create `HireDehireServiceTest.java` with mocked Statement to test: (1) null/empty/All custCd returns empty map; (2) various combinations of optional filters; (3) the letters-only searchCrit being silently dropped (confirm if this is intended behavior or bug); (4) SQL injection in searchCrit, custCd, locCd, deptCd, vehTypeCd; (5) exception handling path; (6) ResultSet to DehireBean mapping correctness.

---

### A04-09 -- HireDehireService: searchCrit letters-only search silently produces no filter (probable bug)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java`
- **Severity:** HIGH
- **Category:** Test Coverage -- Logic Defect
- **Description:** When `searchCrit` contains only alphabetic characters and spaces (matching the regex at line 16), the code enters the `if (searchCrit != null && !searchCrit.trim().isEmpty())` block (line 54) but the inner `if (!searchCritLettersOnly)` check (line 65) evaluates to false, causing no SQL filter to be added. The `and` conjunction was already appended to `relCond` and `relHistoryCond` (lines 58-63), which will result in a malformed SQL query ending in `and ` with no subsequent condition.
- **Evidence:** Lines 56-63 append `" and "` to relCond/relHistoryCond before the searchCritLettersOnly check. If `searchCritLettersOnly` is true, no condition follows the `and`, producing invalid SQL like `WHERE ... and `. This would cause a SQLException that is silently caught at line 112.
- **Recommendation:** A test with `searchCrit = "ABC"` would immediately reveal this SQL syntax error. Fix the logic to either support letter-based searches (e.g., by driver name) or avoid appending `and` when no condition will follow.

---

### A04-10 -- PreOpQuestions and Question POJOs: no equals/hashCode, no validation tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/PreOpQuestions.java`, `Question.java`
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Data Model
- **Description:** Both `PreOpQuestions` and `Question` are JSON binding POJOs used for pre-operation check question data. Neither class implements `equals()` or `hashCode()`, which means they cannot be reliably used in collections or compared in assertions. The `toString()` methods are custom implementations but never tested. `Question.critical` is typed as `String` rather than `boolean` or an enum, creating ambiguity about valid values.
- **Evidence:** `PreOpQuestions.java` lines 7-9: fields without validation. `Question.java` line 7: `String critical` -- presumably "Y"/"N" or "true"/"false" but not enforced. No `@JsonProperty` or `@NotNull` annotations present. No default constructor (only parameterized), which may cause issues with some JSON deserialization frameworks.
- **Recommendation:** Create basic POJO tests verifying: (1) constructor correctly sets all fields; (2) getters/setters round-trip; (3) toString produces expected output; (4) null handling in constructor arguments; (5) JSON serialization/deserialization if Jackson/Gson is used.

---

### A04-11 -- SupervisorUnlockBean: getGrandTotal computed field logic untested
- **File:** `WEB-INF/src/com/torrent/surat/fms6/linde/bean/SupervisorUnlockBean.java`
- **Severity:** LOW
- **Category:** Test Coverage -- Data Model
- **Description:** `SupervisorUnlockBean` is a simple POJO with a computed `getGrandTotal()` method (line 51) that returns `impactCount + surveyCount + criticalCount`. The declared but unused `int grandTotal` field (line 9) shadows the computed method, which could cause confusion. The `toString()` method is overridden but omits `surveyCount` label formatting and `grandTotal`. No tests validate the arithmetic or toString output.
- **Evidence:** Line 9: `int grandTotal` field declared but never assigned. Line 51: `getGrandTotal()` computes from three other fields. Line 47-48: `toString()` includes "Impact", "Critical", "Survey" but not the total.
- **Recommendation:** Create basic test verifying `getGrandTotal()` with known inputs, including zero values and Integer.MAX_VALUE overflow scenarios. Low priority given simplicity.

---

### A04-12 -- BusinessInsight servlet: hardcoded email sender and fragile path traversal untested
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Configuration / Error Handling
- **Description:** The `linderReportMailer` method (line 118) hardcodes the sender email as `"fleetfocus@lindemh.com.au"` (line 126) and passes `"unknown"` for the CC and sender name. The `getExportDir()` method (line 105) uses a fragile path traversal pattern (`/../../../../../../../excelrpt/`) based on counting slashes in the class's code source location URL. Neither method is tested, and the path traversal is extremely brittle across different deployment environments.
- **Evidence:** Line 107-108: `this.getClass().getProtectionDomain().getCodeSource().getLocation().toString().substring(6)` -- assumes URL format, hardcoded substring index. Line 113: `dir += "/../../../../../../../excelrpt/"` -- seven parent directory traversals. Line 123-126: hardcoded email addresses and `"unknown"` placeholders. Line 99: typo "wong" instead of "wrong" in error message.
- **Recommendation:** Test `getExportDir()` returns a valid path under known code source locations. Test `linderReportMailer()` with mocked mail utility. Fix the "wong" typo.

---

### A04-13 -- BusinessInsightExcel: division-by-zero risk in createUtilImpact and related methods
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java`
- **Severity:** HIGH
- **Category:** Test Coverage -- Arithmetic Error Paths
- **Description:** Multiple report generation methods compute `impXHour = duration / impact` (lines 151, 240, 330) before the guard check `if (impact == 0 || duration == 0)`. If `impact` is 0, the division occurs first, producing `Infinity` or `NaN` for doubles, or `ArithmeticException` for integers. The `createPreopStat` method has `avg/qCount * 10` (line 581) where integer division by zero will throw `ArithmeticException` if `qCount == 0`. Similarly, `createLockoutStatus` has `totalAve/count * 10` (line 470) with integer division.
- **Evidence:** Line 151: `double impXHour = duration / impact;` -- impact can be 0. Line 153: `if (impact == 0 || duration == 0) { impXHour = 0; }` -- guard comes too late for integer types. Line 470: `DataUtil.convert_time(totalAve/count * 10)` -- count is checked at line 448 but this is integer division, losing precision. Line 581: `DataUtil.convert_time(avg/qCount * 10)` -- qCount could be 0 if no questions found but `sum > 0`.
- **Recommendation:** Tests should supply data arrays with zero values for impact/duration/qCount/count to verify no runtime exceptions occur. The guard should be moved before the division.

---

### A04-14 -- BusinessInsightBean: exception handling swallows errors with only printStackTrace
- **File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Error Handling
- **Description:** Every fetch method in BusinessInsightBean catches `Exception` broadly and handles it with only `e.printStackTrace()` and `e.getMessage()` (the latter being a no-op since the result is not used). The `init()` method (line 93-96) also prints the raw query to stdout on failure, which could leak sensitive SQL content. Without tests, there is no verification that partial results or empty arrays are returned on failure rather than corrupted data.
- **Evidence:** Lines 290-295: `catch(Exception e) { System.out.println(query); e.printStackTrace(); e.getMessage(); }` -- `e.getMessage()` return value discarded. Same pattern at lines 553-558, 606-611, 673-678, 746-751, 843-847, 979-984, 1079-1084, 1208-1213, 1319-1324. Line 96: `System.out.println(" Exception in LindeReportsBean " + " \nquery " + query)` -- leaks SQL.
- **Recommendation:** Tests should verify that when database operations fail, the `dataArray` is in a consistent state (either empty or containing only valid entries). Test that partial failures mid-loop do not leave corrupted data.

---

## Priority Summary

| Priority | Finding IDs | Description |
|---|---|---|
| **CRITICAL** | A04-01, A04-02, A04-03, A04-06, A04-08 | Zero test infrastructure; SQL injection in BusinessInsightBean (12 methods), FmsChklistLangSettingRepo (3 methods), HireDehireService (1 method); untested business logic |
| **HIGH** | A04-04, A04-05, A04-07, A04-09, A04-13 | Servlet validation untested; Excel report generation with division-by-zero risks; silent search logic bug in HireDehireService; repo edge cases |
| **MEDIUM** | A04-10, A04-12, A04-14 | POJO model gaps; hardcoded config and fragile paths; swallowed exceptions |
| **LOW** | A04-11 | Simple bean computed field |

## Recommended Test Prioritization

1. **Immediate (CRITICAL):** `FmsChklistLangSettingRepoTest` -- smallest file, most testable, direct SQL injection risk
2. **Immediate (CRITICAL):** `HireDehireServiceTest` -- single complex method with SQL injection, silent bug, and testable with mocked Statement
3. **High Priority:** `BusinessInsightBeanTest` -- focus on `convert_time`, `convert_time1`, `ratio` utility methods first (pure functions, easily testable), then mock-based tests for fetch methods
4. **High Priority:** `BusinessInsightExcelTest` -- test `createExcel` dispatch and division-by-zero edge cases
5. **Medium Priority:** `BusinessInsightServletTest` -- mock request/response for validation branches
6. **Low Priority:** `PreOpQuestionsTest`, `QuestionTest`, `SupervisorUnlockBeanTest` -- simple POJOs
