# Pass 2 -- Test Coverage: chart/excel package
**Agent:** A06
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|--------|--------|
| Test framework (JUnit/TestNG) | **Not present** -- no JUnit or TestNG dependency found in project |
| Test source root (`src/test/`, `test/`) | **Does not exist** |
| Test files for this package | **Zero** -- 0 out of 20 files have any associated test |
| CI test execution | **None observed** -- no test runner configuration found |
| Coverage tooling (JaCoCo, Cobertura) | **Not present** |
| Mocking framework (Mockito, EasyMock) | **Not present** |

**Effective line coverage for `com.torrent.surat.fms6.chart.excel`: 0%**

The entire repository contains zero automated tests. No test infrastructure, no test dependencies, no test configurations. Every class in this package is completely untested.

---

## Reading Evidence

### 1. BatteryChargeBean.java (21 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/BatteryChargeBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 7 | `String getDeptName()` | public |
| 10 | `int getCount()` | public |
| 13 | `void setDeptName(String deptName)` | public |
| 16 | `void setCount(int count)` | public |

Simple POJO bean with two fields: `deptName` (String) and `count` (int). No validation logic.

---

### 2. BatteryChargeChart.java (131 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/BatteryChargeChart.java`
**Extends:** `Chart` (from `com.torrent.surat.fms6.chart`)

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 31 | `ArrayList<String> getyAxisLabel()` | public |
| 35 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 39 | `void addyAxisLabel(String yAxisLabel)` | public |
| 43 | `BatteryChargeChart(ArrayList<double[]> data)` | public (constructor) |
| 52 | `void addColors()` | public |
| 56 | `ArrayList<double[]> getData()` | public |
| 60 | `void setData(ArrayList<double[]> data)` | public |
| 64 | `void setyAxis()` | public |
| 70 | `String createChart(List<String> axisLabels) throws UnsupportedEncodingException` | public |

Builds a Google Charts bar chart URL using `charts4j`. The `chldLetters` array (line 27) is limited to 26 entries (A-Z). `createChart` takes axis labels and URL-encodes them.

---

### 3. ChartDashboard.java (9 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboard.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 5 | `ChartDashboard()` | public (constructor) |

Empty class with only a default constructor. No methods, no fields.

---

### 4. ChartDashboardUtil.java (1490 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java`
**Extends:** `Frm_excel`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 38 | `ChartDashboardUtil(String docRoot, String fileName) throws Exception` | public (constructor) |
| 42 | `String createExcel() throws IOException` | public |
| 70 | `void createTestChart(int ch) throws Exception` | public |
| 688 | `static String now(String dateFormat)` | public static |
| 695 | `void createBarChart() throws IOException` | public |
| 1036 | `String getImpactChartUrl(ArrayList<ImpactBean> bean) throws SQLException` | public |
| 1058 | `String getImpactChartUrl(ArrayList<ImpactBean> bean, String dept) throws SQLException` | public |
| 1083 | `String getMachineUnlock(ArrayList<UnlockBean> bean) throws SQLException` | public |
| 1105 | `String getMachineUnlock(ArrayList<UnlockBean> bean, String dept) throws SQLException` | public |
| 1127 | `String getUnitUtil(ArrayList<UnitUtilBean> bean) throws SQLException` | public |
| 1150 | `String getUnitUtil(ArrayList<UnitUtilBean> bean, String dept) throws SQLException` | public |
| 1176 | `String getPreOpFail(ArrayList<PreopFailBean> bean) throws SQLException` | public |
| 1190 | `String getPreOpFail(ArrayList<PreopFailBean> bean, String dept) throws SQLException` | public |
| 1208 | `String getAccessAbuse(ArrayList<DriverAccessAbuseBean> bean) throws SQLException, UnsupportedEncodingException` | public |
| 1226 | `String getAccessAbuse(ArrayList<DriverAccessAbuseBean> bean, String dept) throws SQLException, UnsupportedEncodingException` | public |
| 1246 | `String getBatteryCharge(ArrayList<BatteryChargeBean> bean) throws SQLException, UnsupportedEncodingException` | public |
| 1267 | `String getBatteryCharge(ArrayList<BatteryChargeBean> bean, String dept) throws SQLException, UnsupportedEncodingException` | public |
| 1291 | `String getExpiry(ArrayList<ExpiryBean> bean) throws SQLException, UnsupportedEncodingException` | public |
| 1314 | `String getExpiry(ArrayList<ExpiryBean> bean, String dept) throws SQLException, UnsupportedEncodingException` | public |
| 1340 | `String getUtilWow()` | public |
| 1358 | `String getUtilWow(String depCd)` | public |
| 1376 | `String getUserLogin(ArrayList<UserLoginBean> bean) throws SQLException, UnsupportedEncodingException` | public |
| 1397 | `String getUserLogin(ArrayList<UserLoginBean> bean, String dept) throws SQLException, UnsupportedEncodingException` | public |
| 1420 | `String getDriverActivity(ArrayList<DriverActivityBean> bean) throws SQLException, UnsupportedEncodingException` | public |
| 1448 | `String getDriverActivity(ArrayList<DriverActivityBean> bean, String dept) throws SQLException, UnsupportedEncodingException` | public |
| 1478 | `void setDeptSize(int deptSize)` | public |
| 1482 | `void setReportType(int reportType)` | public |
| 1486 | `ArrayList<ChartMailListBean> getChartMailBeanList()` | public |

This is the central orchestration class. It creates Excel workbooks with chart dashboards. `createBarChart()` is ~335 lines and calls into `ChartsExcelDao` for data, then generates 9 different chart types. `createTestChart(int ch)` dispatches on chart type via a switch statement (cases 1-9). Both methods contain deeply nested logic, database calls, file I/O, and exception handling.

---

### 5. ChartMailListBean.java (37 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartMailListBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 10 | `int getCustCd()` | public |
| 13 | `String getLocCd()` | public |
| 16 | `int getUserCd()` | public |
| 19 | `String getEmailId()` | public |
| 22 | `void setCustCd(int custCd)` | public |
| 25 | `void setLocCd(String locCd)` | public |
| 28 | `void setUserCd(int userCd)` | public |
| 31 | `void setEmailId(String emailId)` | public |

Simple POJO bean with four fields. No validation logic.

---

### 6. ChartsExcelDao.java (1841 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 20 | `ChartsExcelDao()` | public (constructor) |
| 24 | `String getFromDate() throws SQLException` | public |
| 58 | `ArrayList<ChartMailListBean> getEmailList(String custCd, String locCd) throws SQLException` | public |
| 97 | `ArrayList<CustLocBean> getCustLoc() throws SQLException` | public |
| 133 | `String getAllLocations(String custCd) throws SQLException` | public |
| 172 | `String getCurrDate() throws SQLException` | public |
| 207 | `ArrayList<UnlockBean> getMachineUnlock(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt) throws SQLException` | public |
| 329 | `ArrayList<ImpactBean> getImpacts(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept) throws SQLException` | public |
| 404 | `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt) throws SQLException` | public |
| 552 | `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, String st_dt, String end_dt) throws SQLException` | public |
| 693 | `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, String dept_cd, String st_dt, String end_dt) throws SQLException` | public |
| 849 | `ArrayList<PreopFailBean> getPreopFail(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt) throws SQLException` | public |
| 970 | `ArrayList<DriverAccessAbuseBean> getAccessAbuse(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt) throws SQLException` | public |
| 1128 | `private String sub_tm(String tm, int secs)` | private |
| 1152 | `private boolean clash(String stm, String etm, String chk_tm)` | private |
| 1165 | `private int to_sec(String tm)` | private |
| 1185 | `private String convert_time(String csec)` | private |
| 1258 | `ArrayList<BatteryChargeBean> getBatteryCharge(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String from, String to) throws SQLException` | public |
| 1344 | `ArrayList<ExpiryBean> getExpiry(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept) throws SQLException` | public |
| 1432 | `ArrayList<UserLoginBean> getUserLogin(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt) throws SQLException` | public |
| 1494 | `ArrayList<DriverActivityBean> getDriverActivity(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt) throws SQLException` | public |

This is the primary data-access class. Every public method opens a raw JDBC connection, builds SQL via string concatenation, executes queries, and returns bean lists. Contains 4 private helper methods for time calculations.

---

### 7. CustLocBean.java (22 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/CustLocBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 8 | `String getCustCd()` | public |
| 11 | `String getLocCd()` | public |
| 14 | `void setCustCd(String custCd)` | public |
| 17 | `void setLocCd(String locCd)` | public |

Simple POJO bean. No validation.

---

### 8. DriverAccessAbuseBean.java (21 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverAccessAbuseBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 7 | `String getDeptName()` | public |
| 10 | `int getCount()` | public |
| 13 | `void setDeptName(String deptName)` | public |
| 16 | `void setCount(int count)` | public |

Simple POJO bean. Identical structure to `BatteryChargeBean`.

---

### 9. DriverAccessAbuseChart.java (131 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverAccessAbuseChart.java`
**Extends:** `Chart`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 31 | `ArrayList<String> getyAxisLabel()` | public |
| 35 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 39 | `void addyAxisLabel(String yAxisLabel)` | public |
| 43 | `DriverAccessAbuseChart(ArrayList<double[]> data)` | public (constructor) |
| 52 | `void addColors()` | public |
| 56 | `ArrayList<double[]> getData()` | public |
| 60 | `void setData(ArrayList<double[]> data)` | public |
| 64 | `void setyAxis()` | public |
| 70 | `String createChart(List<String> axisLabels) throws UnsupportedEncodingException` | public |

Structurally identical to `BatteryChargeChart`. Uses `chldLetters` array limited to 26 entries.

---

### 10. DriverActivityBean.java (43 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverActivityBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 11 | `String getDeptName()` | public |
| 14 | `int getDur()` | public |
| 17 | `int getHydr()` | public |
| 20 | `int getSeat()` | public |
| 23 | `int getTraction()` | public |
| 26 | `void setDeptName(String deptName)` | public |
| 29 | `void setDur(int dur)` | public |
| 32 | `void setHydr(int hydr)` | public |
| 35 | `void setSeat(int seat)` | public |
| 38 | `void setTraction(int traction)` | public |

POJO bean with five fields. No validation.

---

### 11. DriverActivityChart.java (117 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/DriverActivityChart.java`
**Extends:** `Chart`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 29 | `ArrayList<String> getyAxisLabel()` | public |
| 33 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 37 | `void addyAxisLabel(String yAxisLabel)` | public |
| 41 | `DriverActivityChart(ArrayList<double[]> data)` | public (constructor) |
| 50 | `void addColors()` | public |
| 54 | `ArrayList<double[]> getData()` | public |
| 58 | `void setData(ArrayList<double[]> data)` | public |
| 62 | `void setyAxis()` | public |
| 68 | `String createChart()` | public |

Fixed axis labels: "Duration", "Hydraulics", "Seat", "Traction". No URL encoding needed (no dynamic labels).

---

### 12. ExpiryBean.java (42 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ExpiryBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 10 | `String getDeptName()` | public |
| 13 | `int getExpired()` | public |
| 16 | `int getOneWeek()` | public |
| 19 | `int getOneMonth()` | public |
| 22 | `int getThreeMonths()` | public |
| 25 | `void setDeptName(String deptName)` | public |
| 28 | `void setExpired(int expired)` | public |
| 31 | `void setOneWeek(int oneWeek)` | public |
| 34 | `void setOneMonth(int oneMonth)` | public |
| 37 | `void setThreeMonths(int threeMonths)` | public |

POJO bean with five fields. No validation.

---

### 13. ExpiryChart.java (117 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ExpiryChart.java`
**Extends:** `Chart`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 29 | `ArrayList<String> getyAxisLabel()` | public |
| 33 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 37 | `void addyAxisLabel(String yAxisLabel)` | public |
| 41 | `ExpiryChart(ArrayList<double[]> data)` | public (constructor) |
| 50 | `void addColors()` | public |
| 54 | `ArrayList<double[]> getData()` | public |
| 58 | `void setData(ArrayList<double[]> data)` | public |
| 62 | `void setyAxis()` | public |
| 68 | `String createChart()` | public |

Fixed axis labels: "Expired", "1 Week", "1 Month", "Three Months".

---

### 14. ImpactChart.java (117 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ImpactChart.java`
**Extends:** `Chart`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 29 | `ArrayList<String> getyAxisLabel()` | public |
| 33 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 37 | `void addyAxisLabel(String yAxisLabel)` | public |
| 41 | `ImpactChart(ArrayList<double[]> data)` | public (constructor) |
| 50 | `void addColors()` | public |
| 54 | `ArrayList<double[]> getData()` | public |
| 58 | `void setData(ArrayList<double[]> data)` | public |
| 62 | `void setyAxis()` | public |
| 68 | `String createChart()` | public |

Fixed axis labels: "Amber", "Red". Y-axis label says "Impacts".

---

### 15. MachineUnlockChart.java (117 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/MachineUnlockChart.java`
**Extends:** `Chart`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 29 | `ArrayList<String> getyAxisLabel()` | public |
| 33 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 37 | `void addyAxisLabel(String yAxisLabel)` | public |
| 41 | `MachineUnlockChart(ArrayList<double[]> data)` | public (constructor) |
| 50 | `void addColors()` | public |
| 54 | `ArrayList<double[]> getData()` | public |
| 58 | `void setData(ArrayList<double[]> data)` | public |
| 62 | `void setyAxis()` | public |
| 68 | `String createChart()` | public |

Fixed axis labels: "Question", "Impact". Y-axis label says "Unlocks".

---

### 16. PreopFailBean.java (31 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 8 | `PreopFailBean()` | public (constructor) |
| 12 | `int getIncorrect()` | public |
| 17 | `void setIncorrect(int incorrect)` | public |
| 21 | `String getDeptName()` | public |
| 25 | `void setDeptName(String deptName)` | public |

POJO bean with two fields. No validation.

---

### 17. PreopFailChart.java (117 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailChart.java`
**Extends:** `Chart`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 29 | `ArrayList<String> getyAxisLabel()` | public |
| 33 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 37 | `void addyAxisLabel(String yAxisLabel)` | public |
| 41 | `PreopFailChart(ArrayList<double[]> data)` | public (constructor) |
| 50 | `void addColors()` | public |
| 54 | `ArrayList<double[]> getData()` | public |
| 58 | `void setData(ArrayList<double[]> data)` | public |
| 62 | `void setyAxis()` | public |
| 68 | `String createChart()` | public |

Fixed axis labels: "Question", "Impact". Legend label says "Unlocks" -- likely a copy-paste from MachineUnlockChart (the legend should say "Incorrect" to match the Y-axis label).

---

### 18. UnitUtilBean.java (30 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/UnitUtilBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 8 | `UnitUtilBean()` | public (constructor) |
| 12 | `String getDeptName()` | public |
| 16 | `double[] getUtilNo()` | public |
| 20 | `void setDeptName(String deptName)` | public |
| 24 | `void setUtilNo(double[] utilNo)` | public |

POJO bean with two fields. The `utilNo` field is a raw array (no defensive copy).

---

### 19. UnlockBean.java (30 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/UnlockBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 8 | `UnlockBean()` | public (constructor) |
| 12 | `String getDeptName()` | public |
| 16 | `String getReason()` | public |
| 20 | `void setDeptName(String deptName)` | public |
| 24 | `void setReason(String reason)` | public |

POJO bean with two fields. No validation.

---

### 20. UserLoginBean.java (23 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/UserLoginBean.java`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 8 | `String getDeptName()` | public |
| 11 | `int getLoginCount()` | public |
| 14 | `void setDeptName(String deptName)` | public |
| 17 | `void setLoginCount(int loginCount)` | public |

Simple POJO bean. No validation.

---

### 21. UserLoginChart.java (131 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/UserLoginChart.java`
**Extends:** `Chart`

| Line | Method Signature | Visibility |
|------|-----------------|------------|
| 31 | `ArrayList<String> getyAxisLabel()` | public |
| 35 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | public |
| 39 | `void addyAxisLabel(String yAxisLabel)` | public |
| 43 | `UserLoginChart(ArrayList<double[]> data)` | public (constructor) |
| 52 | `void addColors()` | public |
| 56 | `ArrayList<double[]> getData()` | public |
| 60 | `void setData(ArrayList<double[]> data)` | public |
| 64 | `void setyAxis()` | public |
| 70 | `String createChart(List<String> axisLabels) throws UnsupportedEncodingException` | public |

Same structure as `BatteryChargeChart` and `DriverAccessAbuseChart`. Uses `chldLetters` array.

---

## Findings

### A06-01 -- CRITICAL: ChartsExcelDao has SQL injection vulnerabilities in all 12 public query methods, with zero test coverage

**Severity:** CRITICAL
**File:** `ChartsExcelDao.java`
**Lines:** 58-95 (getEmailList), 133-169 (getAllLocations), 207-327 (getMachineUnlock), 329-402 (getImpacts), 404-550 (getUnitUtilisationByHour 3-param), 552-691 (getUnitUtilisationByHour 4-param), 693-847 (getUnitUtilisationByHour 5-param), 849-968 (getPreopFail), 970-1126 (getAccessAbuse), 1258-1342 (getBatteryCharge), 1344-1430 (getExpiry), 1432-1492 (getUserLogin), 1494-1838 (getDriverActivity)

Every database method in `ChartsExcelDao` uses raw string concatenation to build SQL queries with user-supplied parameters (`cust_cd`, `loc_cd`, `dept_cd`, `st_dt`, `end_dt`). No parameterized queries (PreparedStatement) are used. Examples:

- Line 71: `"where cust_cd="+custCd + " and loc_cd='" + locCd +"';"` -- direct concatenation of `custCd` and `locCd`
- Line 145: `"where \"USER_CD\"=" + custCd` -- direct concatenation
- Line 250: `"where " + cond_cust + cond_site + cond_dept` -- conditions built from parameters
- Lines 271-274: timestamp parameters injected directly into SQL

**Tests needed:**
- Unit tests with mock database connections verifying parameterized queries are used
- Integration tests with SQL injection payloads to verify input sanitization
- Tests for each of the 12+ query methods with boundary/null inputs

---

### A06-02 -- CRITICAL: ChartsExcelDao error handling silently swallows exceptions, no tests verify error propagation

**Severity:** CRITICAL
**File:** `ChartsExcelDao.java`
**Lines:** 45-49, 84-88, 120-124, 153-157, 193-197, 316-320, 391-395, 538-542, 679-683, 835-839, 956-960, 1113-1117, 1330-1334, 1418-1422, 1480-1484, 1826-1830

Every catch block in `ChartsExcelDao` follows this pattern:
```java
catch(Exception e) {
    e.printStackTrace();
    e.getMessage();
}
```
The `e.getMessage()` call on line 48 (and all similar instances) is a no-op -- it evaluates the string but discards the result. Exceptions are printed to stdout/stderr but never re-thrown or logged properly. The methods then return partial/empty results without any indication of failure.

**Tests needed:**
- Tests that verify exception propagation (or proper error indication) when DB connections fail
- Tests that verify behavior when ResultSet is empty
- Tests that verify resource cleanup in finally blocks when exceptions occur during nested operations

---

### A06-03 -- CRITICAL: ChartDashboardUtil.createBarChart() and createTestChart() are 335+ line methods with zero test coverage

**Severity:** CRITICAL
**File:** `ChartDashboardUtil.java`
**Lines:** 70-686 (createTestChart), 695-1030 (createBarChart)

These are the two most complex methods in the package. `createTestChart()` contains a 9-case switch statement (lines 113-387) that dispatches to different chart-generation paths. `createBarChart()` contains deeply nested loops generating Excel sheets with 9 different chart types per site. Both methods:
- Interact with the database (via `ChartsExcelDao`)
- Generate Excel workbooks (via Apache POI)
- Generate chart URLs (via charts4j)
- Perform file I/O (via `FileOutputStream`)
- Handle multiple departments and locations in nested loops

**Tests needed:**
- Unit tests for each of the 9 switch cases in `createTestChart()`
- Tests for `createBarChart()` with varying numbers of departments, locations, and data sizes
- Tests for the Excel output format correctness
- Tests for file creation and cleanup
- Edge case tests: empty department list, null data, single vs. multiple locations

---

### A06-04 -- HIGH: ChartsExcelDao.getAllLocations() has a dead-code bug at line 164

**Severity:** HIGH
**File:** `ChartsExcelDao.java`
**Lines:** 164-166

```java
if( locCd.trim().length() < 0){
    locCd = locCd.substring(0,locCd.length() - 1);
}
```

`String.length()` can never return a value less than 0. This condition is always false, meaning the trailing comma from the `while` loop on line 151 (`locCd += rs.getString(1) + ","`) is never stripped. This means `getAllLocations()` always returns a string with a trailing comma (e.g., `"loc1,loc2,"`), which could cause downstream SQL issues.

**Tests needed:**
- Unit test verifying trailing comma is properly stripped
- Test with single location result
- Test with empty result set

---

### A06-05 -- HIGH: Chart classes have unbounded array index risk in createChart() methods with >26 axis labels

**Severity:** HIGH
**Files:** `BatteryChargeChart.java` (line 78), `DriverAccessAbuseChart.java` (line 78), `UserLoginChart.java` (line 78)
**Lines:** 27 (chldLetters declaration), 75-79 (loop accessing chldLetters[i])

The `chldLetters` array has exactly 26 entries (A-Z). If `axisLabels.size() > 26`, an `ArrayIndexOutOfBoundsException` will be thrown at runtime:
```java
for( int i=0; i < axisLabels.size(); i++){
    ...
    chdlL.add(chldLetters[i]);  // BOOM if i >= 26
```

**Tests needed:**
- Test with 0 labels (empty list)
- Test with 1 label
- Test with exactly 26 labels (boundary)
- Test with 27+ labels (should handle gracefully or throw documented exception)

---

### A06-06 -- HIGH: ChartDashboardUtil chart URL methods lack null-safety, no tests for empty input

**Severity:** HIGH
**File:** `ChartDashboardUtil.java`
**Lines:** 1036-1476 (all getXxxChartUrl/getXxx methods)

All chart-generation methods (e.g., `getImpactChartUrl`, `getMachineUnlock`, `getAccessAbuse`, etc.) iterate over the input bean list without checking for null. If any bean list is null, a `NullPointerException` will occur. Additionally, when filtering by department name (e.g., line 1067: `b.getDept_name().equalsIgnoreCase(dept)`), if `getDept_name()` returns null, this will throw NPE.

**Tests needed:**
- Tests with null input lists
- Tests with empty input lists
- Tests with beans containing null department names
- Tests for each overloaded variant (with and without dept filter)

---

### A06-07 -- HIGH: ChartsExcelDao resource leak risk in getUnitUtilisationByHour() -- reuses ResultSet variable across nested queries

**Severity:** HIGH
**File:** `ChartsExcelDao.java`
**Lines:** 404-550, 552-691, 693-847

The `getUnitUtilisationByHour` methods execute multiple queries in deeply nested loops (days x hours x vehicles) using a single `Statement` object. Each `stmt.executeQuery()` call returns a new `ResultSet` that implicitly closes the previous one. Within the nested `for(i) -> for(j)` loop, up to `days_btn * 24 * 3` queries are executed per department. If `days_btn` is large, this creates extreme database load.

**Tests needed:**
- Performance tests with varying `days_btn` values
- Tests verifying correct behavior with large date ranges
- Tests for proper resource cleanup on exception

---

### A06-08 -- HIGH: ChartsExcelDao.getAccessAbuse() contains complex time-clash detection logic (lines 1046-1106) with no unit tests

**Severity:** HIGH
**File:** `ChartsExcelDao.java`
**Lines:** 1046-1106 (clash detection), 1128-1150 (sub_tm), 1152-1163 (clash), 1165-1183 (to_sec), 1185-1255 (convert_time)

The `getAccessAbuse()` method contains intricate time-overlap detection logic using private helper methods `sub_tm()`, `clash()`, `to_sec()`, and `convert_time()`. These are purely computational methods that could be trivially unit-tested in isolation, but have zero coverage. The `sub_tm()` method (line 1128) performs time subtraction via manual parsing, and `convert_time()` (line 1185) uses complex nested conditionals for time formatting. Both are error-prone.

**Tests needed:**
- Unit tests for `sub_tm()` with normal times, midnight boundary, negative results
- Unit tests for `clash()` with overlapping, non-overlapping, and boundary times
- Unit tests for `to_sec()` with various time formats
- Unit tests for `convert_time()` with zero, small, large, and negative centisecond values
- Integration tests for the full clash-detection algorithm

---

### A06-09 -- MEDIUM: All 8 Chart classes have identical structure with no tests verifying chart URL generation

**Severity:** MEDIUM
**Files:** `BatteryChargeChart.java`, `DriverAccessAbuseChart.java`, `DriverActivityChart.java`, `ExpiryChart.java`, `ImpactChart.java`, `MachineUnlockChart.java`, `PreopFailChart.java`, `UserLoginChart.java`

All chart classes follow the same pattern: constructor sets data, colors, and y-axis; `createChart()` builds a Google Charts URL. The chart URL generation depends on third-party library `charts4j` and the inherited `caculateyAxis()` method (note: typo in method name -- "caculate" instead of "calculate"). None of this is tested.

**Tests needed:**
- Tests verifying chart URL is well-formed (starts with expected prefix, contains required parameters)
- Tests verifying y-axis calculation with various data ranges (0, single value, large values)
- Tests for empty data arrays
- Tests for `setyAxis()` when `maxArrayValue()` returns 0 (potential division by zero in `caculateyAxis()`)

---

### A06-10 -- MEDIUM: PreopFailChart has misleading legend label "Unlocks" instead of "Incorrect"

**Severity:** MEDIUM
**File:** `PreopFailChart.java`
**Line:** 78

```java
BarChartPlot plot = Plots.newBarChartPlot(
    DataUtil.scaleWithinRange(0, this.yAxis, datalist),
    this.colors.get(i), "Unlocks");  // Should be "Incorrect" or "Pre-op Failures"
```

The legend label is "Unlocks" but this chart represents "Incorrect Pre-op Checks" (line 43). This is a copy-paste error from `MachineUnlockChart`. A test comparing chart metadata to the report title would catch this.

**Tests needed:**
- Test verifying the chart legend matches the report subject matter

---

### A06-11 -- MEDIUM: ChartDashboard.java is an empty class with no functionality

**Severity:** MEDIUM
**File:** `ChartDashboard.java`
**Lines:** 1-9

The class has only an empty default constructor. It appears to be unused dead code or a placeholder that was never implemented. All actual dashboard logic lives in `ChartDashboardUtil`.

**Tests needed:**
- Verify whether this class is referenced anywhere; if not, it should be removed

---

### A06-12 -- MEDIUM: 8 POJO beans have no equals/hashCode/toString, no null validation on setters

**Severity:** MEDIUM
**Files:** `BatteryChargeBean.java`, `ChartMailListBean.java`, `CustLocBean.java`, `DriverAccessAbuseBean.java`, `DriverActivityBean.java`, `ExpiryBean.java`, `PreopFailBean.java`, `UnlockBean.java`, `UnitUtilBean.java`, `UserLoginBean.java`

None of the bean classes implement `equals()`, `hashCode()`, or `toString()`. None validate their setter inputs. While these are simple data holders, the lack of `equals`/`hashCode` means they cannot be reliably used in Sets or as Map keys. The `UnitUtilBean.getUtilNo()` (line 16) returns a mutable `double[]` reference with no defensive copy.

**Tests needed:**
- Tests for getter/setter round-trip correctness
- Tests for null input handling on setters
- Tests for `UnitUtilBean` array mutability
- Tests for serialization if beans are ever transmitted

---

### A06-13 -- MEDIUM: ChartsExcelDao.getImpacts() uses hardcoded threshold configuration from RuntimeConf without tests

**Severity:** MEDIUM
**File:** `ChartsExcelDao.java`
**Lines:** 351-362, 366-378

The impact categorization logic depends on `RuntimeConf.Blue_LEVEL`, `RuntimeConf.RED_LEVEL`, and `RuntimeConf.AMBER_LEVEL` for threshold classification. These are static configuration values that affect business-critical impact severity categorization. There are no tests verifying the classification logic works correctly at boundary values.

**Tests needed:**
- Tests with shock values at exactly the RED, AMBER, and BLUE thresholds
- Tests with shock values just below and just above each threshold
- Tests verifying correct categorization counts

---

### A06-14 -- LOW: ChartDashboardUtil.getImpactChartUrl() overloads have inconsistent array construction

**Severity:** LOW
**File:** `ChartDashboardUtil.java`
**Lines:** 1049 vs. 1074

The no-department overload creates: `double[] dou = { amber, red }` (2 elements)
The department-filtered overload creates: `double[] dou = { blue, amber, red }` (3 elements)

The first overload includes only amber and red (matching the "Amber"/"Red" axis labels in `ImpactChart`), while the second includes blue as well. Since `ImpactChart` only has 2 axis labels, the 3-element array in the department variant may produce a misaligned chart.

**Tests needed:**
- Tests comparing output of both overloads with identical input data
- Tests verifying chart data alignment with axis labels

---

### A06-15 -- LOW: ChartDashboardUtil.getAccessAbuse() multiplies count by 2 without documentation

**Severity:** LOW
**File:** `ChartDashboardUtil.java`
**Line:** 1214

```java
dou[i] = bean.get(i).getCount() * 2;
```

The access abuse count is multiplied by 2 in the no-department overload but this factor is not documented. It is unclear whether this is intentional business logic (e.g., counting both sides of a clash) or a bug.

**Tests needed:**
- Test verifying the multiplier is correct for the business domain
- Test comparing the multiplied value against expected output from known clash scenarios

---

## Summary

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 3 | SQL injection in all DAO methods (A06-01), silent exception swallowing (A06-02), massive untested orchestration methods (A06-03) |
| HIGH | 5 | Dead-code bug in getAllLocations (A06-04), ArrayIndexOutOfBounds risk (A06-05), null-safety gaps (A06-06), resource leak risk (A06-07), untested time-clash logic (A06-08) |
| MEDIUM | 5 | Chart URL generation untested (A06-09), copy-paste legend error (A06-10), empty class (A06-11), beans lack equals/hashCode (A06-12), threshold logic untested (A06-13) |
| LOW | 2 | Inconsistent array construction (A06-14), undocumented multiplier (A06-15) |
| **TOTAL** | **15** | |

### Priority Test Recommendations

1. **Immediate (CRITICAL):** Add parameterized query tests and fix SQL injection in `ChartsExcelDao` -- all 12+ public methods
2. **Immediate (CRITICAL):** Add tests for exception handling and resource cleanup in all DAO methods
3. **High priority:** Extract and unit-test the private time-calculation helpers (`sub_tm`, `clash`, `to_sec`, `convert_time`) from `ChartsExcelDao`
4. **High priority:** Add boundary tests for chart classes with >26 axis labels
5. **Medium priority:** Add chart URL validation tests for all 8 chart classes
6. **Medium priority:** Add integration tests for `ChartDashboardUtil.createExcel()` verifying file output

### Test Infrastructure Prerequisites

Before any tests can be written for this package, the project needs:
1. JUnit 4 or 5 dependency added to the build
2. A test source directory (`src/test/java/`)
3. Mockito or similar for mocking `DBUtil.getConnection()`, `UnitDAO`, etc.
4. An in-memory database (H2) or test database configuration for integration tests
5. A build tool configuration (Maven/Gradle) to execute tests
