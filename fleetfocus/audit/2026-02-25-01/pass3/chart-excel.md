# Pass 3 -- Documentation: chart/excel package
**Agent:** A06
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Reading Evidence

### BatteryChargeBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.BatteryChargeBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `String getDeptName()` (line 7) -- Javadoc: Absent
  - `int getCount()` (line 10) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 13) -- Javadoc: Absent
  - `void setCount(int count)` (line 16) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### BatteryChargeChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.BatteryChargeChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 31) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 35) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 39) -- Javadoc: Absent
  - `BatteryChargeChart(ArrayList<double[]> data)` (line 43) -- Javadoc: Absent
  - `void addColors()` (line 52) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 56) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 60) -- Javadoc: Absent
  - `void setyAxis()` (line 64) -- Javadoc: Absent
  - `String createChart(List<String> axisLabels)` (line 70) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:** "EXAMPLE CODE START" (line 71), "EXAMPLE CODE END" (line 127) -- misleading, this is production code not example code

### ChartDashboard.java
- **Class:** `com.torrent.surat.fms6.chart.excel.ChartDashboard`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ChartDashboard()` (line 5) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### ChartDashboardUtil.java
- **Class:** `com.torrent.surat.fms6.chart.excel.ChartDashboardUtil` extends `Frm_excel`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ChartDashboardUtil(String docRoot, String fileName)` (line 38) -- Javadoc: Absent
  - `String createExcel()` (line 42) -- Javadoc: Absent
  - `void createTestChart(int ch)` (line 70) -- Javadoc: Absent
  - `static String now(String dateFormat)` (line 688) -- Javadoc: Absent
  - `void createBarChart()` (line 695) -- Javadoc: Absent
  - `String getImpactChartUrl(ArrayList<ImpactBean> bean)` (line 1036) -- Javadoc: Absent
  - `String getImpactChartUrl(ArrayList<ImpactBean> bean, String dept)` (line 1058) -- Javadoc: Absent
  - `String getMachineUnlock(ArrayList<UnlockBean> bean)` (line 1083) -- Javadoc: Absent
  - `String getMachineUnlock(ArrayList<UnlockBean> bean, String dept)` (line 1105) -- Javadoc: Absent
  - `String getUnitUtil(ArrayList<UnitUtilBean> bean)` (line 1127) -- Javadoc: Absent
  - `String getUnitUtil(ArrayList<UnitUtilBean> bean, String dept)` (line 1150) -- Javadoc: Absent
  - `String getPreOpFail(ArrayList<PreopFailBean> bean)` (line 1176) -- Javadoc: Absent
  - `String getPreOpFail(ArrayList<PreopFailBean> bean, String dept)` (line 1190) -- Javadoc: Absent
  - `String getAccessAbuse(ArrayList<DriverAccessAbuseBean> bean)` (line 1208) -- Javadoc: Absent
  - `String getAccessAbuse(ArrayList<DriverAccessAbuseBean> bean, String dept)` (line 1226) -- Javadoc: Absent
  - `String getBatteryCharge(ArrayList<BatteryChargeBean> bean)` (line 1246) -- Javadoc: Absent
  - `String getBatteryCharge(ArrayList<BatteryChargeBean> bean, String dept)` (line 1267) -- Javadoc: Absent
  - `String getExpiry(ArrayList<ExpiryBean> bean)` (line 1291) -- Javadoc: Absent
  - `String getExpiry(ArrayList<ExpiryBean> bean, String dept)` (line 1314) -- Javadoc: Absent
  - `String getUtilWow()` (line 1340) -- Javadoc: Absent
  - `String getUtilWow(String depCd)` (line 1358) -- Javadoc: Absent
  - `String getUserLogin(ArrayList<UserLoginBean> bean)` (line 1376) -- Javadoc: Absent
  - `String getUserLogin(ArrayList<UserLoginBean> bean, String dept)` (line 1397) -- Javadoc: Absent
  - `String getDriverActivity(ArrayList<DriverActivityBean> bean)` (line 1420) -- Javadoc: Absent
  - `String getDriverActivity(ArrayList<DriverActivityBean> bean, String dept)` (line 1448) -- Javadoc: Absent
  - `void setDeptSize(int deptSize)` (line 1478) -- Javadoc: Absent
  - `void setReportType(int reportType)` (line 1482) -- Javadoc: Absent
  - `ArrayList<ChartMailListBean> getChartMailBeanList()` (line 1486) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:**
  - `//FOR TESTING ONLY` (line 92) -- test code retained in production
  - `//END TESTING=` (line 680) -- marks end of test block
  - `//for testing purposes only` (line 735) -- test code retained in production

### ChartMailListBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.ChartMailListBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `int getCustCd()` (line 10) -- Javadoc: Absent
  - `String getLocCd()` (line 13) -- Javadoc: Absent
  - `int getUserCd()` (line 16) -- Javadoc: Absent
  - `String getEmailId()` (line 19) -- Javadoc: Absent
  - `void setCustCd(int custCd)` (line 22) -- Javadoc: Absent
  - `void setLocCd(String locCd)` (line 25) -- Javadoc: Absent
  - `void setUserCd(int userCd)` (line 28) -- Javadoc: Absent
  - `void setEmailId(String emailId)` (line 31) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### ChartsExcelDao.java
- **Class:** `com.torrent.surat.fms6.chart.excel.ChartsExcelDao`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ChartsExcelDao()` (line 20) -- Javadoc: Absent
  - `String getFromDate()` (line 24) -- Javadoc: Absent
  - `ArrayList<ChartMailListBean> getEmailList(String custCd, String locCd)` (line 58) -- Javadoc: Absent
  - `ArrayList<CustLocBean> getCustLoc()` (line 97) -- Javadoc: Absent
  - `String getAllLocations(String custCd)` (line 133) -- Javadoc: Absent
  - `String getCurrDate()` (line 172) -- Javadoc: Absent
  - `ArrayList<UnlockBean> getMachineUnlock(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` (line 207) -- Javadoc: Absent
  - `ArrayList<ImpactBean> getImpacts(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept)` (line 329) -- Javadoc: Absent
  - `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` (line 404) -- Javadoc: Absent
  - `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, String st_dt, String end_dt)` (line 552) -- Javadoc: Absent
  - `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, String dept_cd, String st_dt, String end_dt)` (line 693) -- Javadoc: Absent
  - `ArrayList<PreopFailBean> getPreopFail(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` (line 849) -- Javadoc: Absent
  - `ArrayList<DriverAccessAbuseBean> getAccessAbuse(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` (line 970) -- Javadoc: Absent
  - `ArrayList<BatteryChargeBean> getBatteryCharge(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String from, String to)` (line 1258) -- Javadoc: Absent
  - `ArrayList<ExpiryBean> getExpiry(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept)` (line 1344) -- Javadoc: Absent
  - `ArrayList<UserLoginBean> getUserLogin(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` (line 1432) -- Javadoc: Absent
  - `ArrayList<DriverActivityBean> getDriverActivity(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` (line 1494) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### CustLocBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.CustLocBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `String getCustCd()` (line 8) -- Javadoc: Absent
  - `String getLocCd()` (line 11) -- Javadoc: Absent
  - `void setCustCd(String custCd)` (line 14) -- Javadoc: Absent
  - `void setLocCd(String locCd)` (line 17) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### DriverAccessAbuseBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.DriverAccessAbuseBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `String getDeptName()` (line 7) -- Javadoc: Absent
  - `int getCount()` (line 10) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 13) -- Javadoc: Absent
  - `void setCount(int count)` (line 16) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### DriverAccessAbuseChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.DriverAccessAbuseChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 31) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 35) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 39) -- Javadoc: Absent
  - `DriverAccessAbuseChart(ArrayList<double[]> data)` (line 43) -- Javadoc: Absent
  - `void addColors()` (line 52) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 56) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 60) -- Javadoc: Absent
  - `void setyAxis()` (line 64) -- Javadoc: Absent
  - `String createChart(List<String> axisLabels)` (line 70) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:** "EXAMPLE CODE START" (line 71), "EXAMPLE CODE END" (line 127)

### DriverActivityBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.DriverActivityBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `String getDeptName()` (line 11) -- Javadoc: Absent
  - `int getDur()` (line 14) -- Javadoc: Absent
  - `int getHydr()` (line 17) -- Javadoc: Absent
  - `int getSeat()` (line 20) -- Javadoc: Absent
  - `int getTraction()` (line 23) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 26) -- Javadoc: Absent
  - `void setDur(int dur)` (line 29) -- Javadoc: Absent
  - `void setHydr(int hydr)` (line 32) -- Javadoc: Absent
  - `void setSeat(int seat)` (line 35) -- Javadoc: Absent
  - `void setTraction(int traction)` (line 38) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### DriverActivityChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.DriverActivityChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 29) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 33) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 37) -- Javadoc: Absent
  - `DriverActivityChart(ArrayList<double[]> data)` (line 41) -- Javadoc: Absent
  - `void addColors()` (line 50) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 54) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 58) -- Javadoc: Absent
  - `void setyAxis()` (line 62) -- Javadoc: Absent
  - `String createChart()` (line 68) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:** "EXAMPLE CODE START" (line 69), "EXAMPLE CODE END" (line 113)

### ExpiryBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.ExpiryBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `String getDeptName()` (line 10) -- Javadoc: Absent
  - `int getExpired()` (line 13) -- Javadoc: Absent
  - `int getOneWeek()` (line 16) -- Javadoc: Absent
  - `int getOneMonth()` (line 19) -- Javadoc: Absent
  - `int getThreeMonths()` (line 22) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 25) -- Javadoc: Absent
  - `void setExpired(int expired)` (line 28) -- Javadoc: Absent
  - `void setOneWeek(int oneWeek)` (line 31) -- Javadoc: Absent
  - `void setOneMonth(int oneMonth)` (line 34) -- Javadoc: Absent
  - `void setThreeMonths(int threeMonths)` (line 37) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### ExpiryChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.ExpiryChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 29) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 33) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 37) -- Javadoc: Absent
  - `ExpiryChart(ArrayList<double[]> data)` (line 41) -- Javadoc: Absent
  - `void addColors()` (line 50) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 54) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 58) -- Javadoc: Absent
  - `void setyAxis()` (line 62) -- Javadoc: Absent
  - `String createChart()` (line 68) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:** "EXAMPLE CODE START" (line 69), "EXAMPLE CODE END" (line 113)

### ImpactChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.ImpactChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 29) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 33) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 37) -- Javadoc: Absent
  - `ImpactChart(ArrayList<double[]> data)` (line 41) -- Javadoc: Absent
  - `void addColors()` (line 50) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 54) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 58) -- Javadoc: Absent
  - `void setyAxis()` (line 62) -- Javadoc: Absent
  - `String createChart()` (line 68) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:** "EXAMPLE CODE START" (line 69), "EXAMPLE CODE END" (line 113)

### MachineUnlockChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.MachineUnlockChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 29) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 33) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 37) -- Javadoc: Absent
  - `MachineUnlockChart(ArrayList<double[]> data)` (line 41) -- Javadoc: Absent
  - `void addColors()` (line 50) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 54) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 58) -- Javadoc: Absent
  - `void setyAxis()` (line 62) -- Javadoc: Absent
  - `String createChart()` (line 68) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:** "EXAMPLE CODE START" (line 69), "EXAMPLE CODE END" (line 113)

### PreopFailBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.PreopFailBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `PreopFailBean()` (line 8) -- Javadoc: Absent
  - `int getIncorrect()` (line 12) -- Javadoc: Absent
  - `void setIncorrect(int incorrect)` (line 17) -- Javadoc: Absent
  - `String getDeptName()` (line 21) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 25) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:**
  - Line 9: `// TODO Auto-generated constructor stub`

### PreopFailChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.PreopFailChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 29) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 33) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 37) -- Javadoc: Absent
  - `PreopFailChart(ArrayList<double[]> data)` (line 41) -- Javadoc: Absent
  - `void addColors()` (line 50) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 54) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 58) -- Javadoc: Absent
  - `void setyAxis()` (line 62) -- Javadoc: Absent
  - `String createChart()` (line 68) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:**
  - "EXAMPLE CODE START" (line 69), "EXAMPLE CODE END" (line 113)
  - Legend label says "Unlocks" (line 78) but chart is for Pre-op Fail -- misleading

### UnitUtilBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.UnitUtilBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `UnitUtilBean()` (line 8) -- Javadoc: Absent
  - `String getDeptName()` (line 12) -- Javadoc: Absent
  - `double[] getUtilNo()` (line 16) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 20) -- Javadoc: Absent
  - `void setUtilNo(double[] utilNo)` (line 24) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:**
  - Line 9: `// TODO Auto-generated constructor stub`

### UnlockBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.UnlockBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `UnlockBean()` (line 8) -- Javadoc: Absent
  - `String getDeptName()` (line 12) -- Javadoc: Absent
  - `String getReason()` (line 16) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 20) -- Javadoc: Absent
  - `void setReason(String reason)` (line 24) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:**
  - Line 9: `// TODO Auto-generated constructor stub`

### UserLoginBean.java
- **Class:** `com.torrent.surat.fms6.chart.excel.UserLoginBean`
- **Class Javadoc:** Absent
- **Public methods:**
  - `String getDeptName()` (line 8) -- Javadoc: Absent
  - `int getLoginCount()` (line 11) -- Javadoc: Absent
  - `void setDeptName(String deptName)` (line 14) -- Javadoc: Absent
  - `void setLoginCount(int loginCount)` (line 17) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

### UserLoginChart.java
- **Class:** `com.torrent.surat.fms6.chart.excel.UserLoginChart` extends `Chart`
- **Class Javadoc:** Absent
- **Public methods:**
  - `ArrayList<String> getyAxisLabel()` (line 31) -- Javadoc: Absent
  - `void setyAxisLabel(ArrayList<String> yAxisLabel)` (line 35) -- Javadoc: Absent
  - `void addyAxisLabel(String yAxisLabel)` (line 39) -- Javadoc: Absent
  - `UserLoginChart(ArrayList<double[]> data)` (line 43) -- Javadoc: Absent
  - `void addColors()` (line 52) -- Javadoc: Absent
  - `ArrayList<double[]> getData()` (line 56) -- Javadoc: Absent
  - `void setData(ArrayList<double[]> data)` (line 60) -- Javadoc: Absent
  - `void setyAxis()` (line 64) -- Javadoc: Absent
  - `String createChart(List<String> axisLabels)` (line 70) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Inline comments of note:** "EXAMPLE CODE START" (line 71), "EXAMPLE CODE END" (line 127)

---

## Findings

### A06-01 -- No Javadoc on any class in the entire package (20 files)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/*.java`
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Class Javadoc
- **Description:** Not a single file in the chart/excel package has a class-level Javadoc comment. There are 20 classes and zero class-level documentation.
- **Evidence:** Every `public class` declaration is preceded only by the `package` statement and `import` blocks with no `/** ... */` Javadoc.
- **Recommendation:** Add class-level Javadoc to all 20 files explaining purpose, usage context, and relationship to the chart dashboard feature. Prioritize the complex classes: `ChartDashboardUtil`, `ChartsExcelDao`, and the Chart subclasses.

### A06-02 -- No Javadoc on any public method in the entire package (176+ methods)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/*.java`
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Method Javadoc
- **Description:** Across all 20 files, there are approximately 176 public methods (including constructors, getters, setters, and business methods). Not a single one has a Javadoc comment with `@param`, `@return`, or `@throws` tags.
- **Evidence:** Exhaustive review of every file confirms zero Javadoc method comments.
- **Recommendation:** Prioritize Javadoc on non-trivial business methods. Bean getters/setters are lower priority.

### A06-03 -- Missing docs on complex DAO methods in ChartsExcelDao (17 methods)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Method Javadoc
- **Description:** ChartsExcelDao contains 17 public methods ranging from 30 to 350 lines each, many with complex SQL queries, multiple database calls, and intricate business logic. None have any documentation explaining parameters, return values, query semantics, or thrown exceptions.
- **Evidence:** Methods such as:
  - `getUnitUtilisationByHour` (3 overloads, lines 404, 552, 693) -- each ~150 lines with nested loops and multiple SQL calls
  - `getAccessAbuse` (line 970) -- 155 lines of complex clash-detection logic
  - `getDriverActivity` (line 1494) -- 345 lines with firmware version checks and dynamic IO field resolution
  - `getMachineUnlock` (line 207) -- 120 lines with reason mapping logic
  - `getPreopFail` (line 849) -- 120 lines with checklist answer comparison
- **Recommendation:** Each DAO method needs Javadoc documenting: what data it retrieves, the meaning of each parameter, the structure of the returned list, and that it throws `SQLException`.

### A06-04 -- Missing docs on complex ChartDashboardUtil methods (29 methods)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java`
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Method Javadoc
- **Description:** ChartDashboardUtil is a 1490-line class with 29 public methods, none documented. `createTestChart(int ch)` alone is 616 lines with a switch statement mapping integer codes to chart types. `createBarChart()` is 335 lines. The 9 chart types are undocumented.
- **Evidence:**
  - `createTestChart(int ch)` (line 70): The `int ch` parameter maps 1-9 to different chart types but this mapping is documented only as inline comments within the switch cases, not in the method signature.
  - `createBarChart()` (line 695): Orchestrates all 9 chart types per location but has no documentation.
- **Recommendation:** Add Javadoc to at minimum `createTestChart`, `createExcel`, and `createBarChart`. Document the chart type integer mapping (1=Impact, 2=Machine Unlock, 3=Preop, 4=Access Abuse, 5=Battery, 6=Expiry, 7=User Login, 8=Driver Activity, 9=Unit Utilisation).

### A06-05 -- Misleading "EXAMPLE CODE" comments in all Chart subclasses
- **File:** Multiple files (see below)
- **Severity:** HIGH
- **Category:** Documentation > Misleading Inline Comments
- **Description:** Eight chart classes contain `// EXAMPLE CODE START` and `// EXAMPLE CODE END. Use this url string in your web or Internet application.` bracketing the body of their `createChart()` methods. This is production code, not example code. These comments appear to be leftovers from a charts4j library tutorial that were copy-pasted and never cleaned up.
- **Evidence:**
  - `BatteryChargeChart.java` lines 71, 127
  - `DriverAccessAbuseChart.java` lines 71, 127
  - `DriverActivityChart.java` lines 69, 113
  - `ExpiryChart.java` lines 69, 113
  - `ImpactChart.java` lines 69, 113
  - `MachineUnlockChart.java` lines 69, 113
  - `PreopFailChart.java` lines 69, 113
  - `UserLoginChart.java` lines 71, 127
- **Recommendation:** Remove `// EXAMPLE CODE START`, `// EXAMPLE CODE END`, and `Use this url string in your web or Internet application` comments from all 8 files. These are misleading -- this is not example code.

### A06-06 -- Misleading legend label "Unlocks" in PreopFailChart
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailChart.java`:78
- **Severity:** HIGH
- **Category:** Documentation > Misleading Inline Comment / Incorrect Label
- **Description:** The `PreopFailChart.createChart()` method creates a bar chart plot with the legend label "Unlocks" (line 78: `Plots.newBarChartPlot(..., "Unlocks")`), but this chart is for "Incorrect Pre-op Checks" (as set in the constructor on line 43). The axis labels also say "Question" and "Impact" (line 86) which are unlock categories, not pre-op check categories. This chart appears to have been copy-pasted from `MachineUnlockChart` without updating the labels.
- **Evidence:**
  - Line 43: `this.setReport("Incorrect Pre-op Checks");` -- the chart title is correct
  - Line 78: `this.colors.get(i), "Unlocks");` -- legend says "Unlocks" (incorrect)
  - Line 86: `AxisLabelsFactory.newAxisLabels("Question","Impact");` -- axis labels from MachineUnlockChart (incorrect)
  - Line 89: `AxisLabelsFactory.newAxisLabels("Incorrect", 100.0);` -- Y-axis label is correct
  - Compare to `MachineUnlockChart.java` line 78: `"Unlocks"` and line 86: `"Question","Impact"` -- identical
- **Recommendation:** Change the legend label to "Incorrect" or "Pre-op Failures" and update axis labels to reflect pre-op check categories rather than machine unlock categories.

### A06-07 -- Test/debug code markers in production ChartDashboardUtil
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java`
- **Severity:** MEDIUM
- **Category:** Documentation > Misleading Inline Comments
- **Description:** ChartDashboardUtil contains inline comments marking sections as test-only code, but these code paths are part of the production build and actively used based on configuration (non-empty `dept_cd`). The comments are misleading because they suggest the code should not be in production.
- **Evidence:**
  - Line 92: `//FOR TESTING ONLY`
  - Line 680: `//END TESTING=`
  - Line 735: `//for testing purposes only`
- **Recommendation:** Either remove the test code paths if they are truly not needed in production, or update the comments to accurately describe the conditional behavior (e.g., "single-department mode for targeted reporting").

### A06-08 -- TODO Auto-generated constructor stubs in 3 bean classes
- **File:** Multiple bean files
- **Severity:** INFO
- **Category:** Documentation > Stale TODO Comments
- **Description:** Three bean classes retain IDE-generated `// TODO Auto-generated constructor stub` comments in empty constructors. These TODOs serve no purpose and add noise.
- **Evidence:**
  - `PreopFailBean.java` line 9
  - `UnitUtilBean.java` line 9
  - `UnlockBean.java` line 9
- **Recommendation:** Remove the `// TODO Auto-generated constructor stub` comments since the constructors intentionally have no body (default construction is the intended behavior for these beans).

### A06-09 -- Extensive commented-out System.out.println and code throughout ChartDashboardUtil
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java`
- **Severity:** LOW
- **Category:** Documentation > Stale/Dead Comments
- **Description:** ChartDashboardUtil contains numerous commented-out `System.out.println` statements and commented-out code blocks that add noise and obscure the actual logic.
- **Evidence:**
  - Line 89: `//System.out.println("FROM: " + from + " | TO: " + to);`
  - Line 853: `//System.out.println(chartUrl);`
  - Lines 864, 875, 885, 895, 905, 915, 925, 936: More commented-out System.out.println calls
  - Line 358: `//chartUrl = getUtilWow();` -- commented-out method call
  - Line 649: `//chartUrl = getUtilWow();` -- duplicate
  - Line 1045-1046: `//blue += b.getBlueimpact();` -- commented-out logic in getImpactChartUrl
  - Line 1068: `//blue += b.getBlueimpact();` -- same in overload
- **Recommendation:** Remove all commented-out `System.out.println` statements and dead code. Use a proper logging framework instead of commented-out print statements.

### A06-10 -- Undocumented method `getAllLocations` misleading name vs implementation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`:133
- **Severity:** HIGH
- **Category:** Documentation > Misleading Method Name / Missing Docs
- **Description:** The method `getAllLocations(String custCd)` is named to suggest it fetches locations by customer code, but the SQL query uses `custCd` as a `USER_CD` in the `FMS_USR_CUST_REL` table (line 145: `"select \"LOC_CD\" from \"FMS_USR_CUST_REL\" where \"USER_CD\"=" + custCd`). Without documentation, the parameter name `custCd` is misleading -- it actually represents a user code. Additionally, the dead-code check on line 164 (`if( locCd.trim().length() < 0)`) will never be true since `String.length()` is always >= 0, so the trailing comma is never trimmed.
- **Evidence:**
  - Line 145: SQL uses `"USER_CD"` not customer code
  - Line 164: `locCd.trim().length() < 0` is an impossible condition
- **Recommendation:** Add Javadoc clarifying the actual parameter semantics. Fix the bug on line 164 (should be `> 0` not `< 0`). Consider renaming the parameter.

### A06-11 -- Unused local variable `arrDept` in getFromDate and getCurrDate
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`
- **Severity:** INFO
- **Category:** Documentation > Misleading Dead Code
- **Description:** Both `getFromDate()` (line 32) and `getCurrDate()` (line 180) declare `ArrayList<EntityBean> arrDept = new ArrayList<EntityBean>()` but never use it. This creates a misleading impression that department data is involved in these date-fetching methods.
- **Evidence:**
  - Line 32 in `getFromDate()`: `ArrayList<EntityBean> arrDept = new ArrayList<EntityBean>();` -- unused
  - Line 180 in `getCurrDate()`: `ArrayList<EntityBean> arrDept = new ArrayList<EntityBean>();` -- unused
- **Recommendation:** Remove the unused `arrDept` variable declarations from both methods.

### A06-12 -- Unused local variable `arrImpactData` in getUnitUtilisationByHour overloads
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`
- **Severity:** INFO
- **Category:** Documentation > Misleading Dead Code
- **Description:** All three overloads of `getUnitUtilisationByHour` declare `ArrayList<ImpactBean> arrImpactData = new ArrayList<ImpactBean>()` but never use it. This misleadingly suggests impact data is part of utilisation computation.
- **Evidence:**
  - Line 412 (5-param overload)
  - Line 560 (4-param overload)
  - Line 701 (5-param with dept_cd overload)
- **Recommendation:** Remove the unused `arrImpactData` variable from all three overloads.

### A06-13 -- ChartDashboard.java is an empty class with no documentation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboard.java`
- **Severity:** LOW
- **Category:** Documentation > Missing Class Javadoc
- **Description:** `ChartDashboard` is a completely empty class (only an empty constructor). There is no documentation explaining whether this is a placeholder, deprecated, or intended for future use.
- **Evidence:** The entire file is 9 lines with only `public class ChartDashboard { public ChartDashboard() { } }`.
- **Recommendation:** Either document the intended purpose of this class or remove it if it is unused.

### A06-14 -- ImpactChart axis labels say "Amber","Red" but getImpactChartUrl overload includes blue
- **File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ImpactChart.java`:86 and `ChartDashboardUtil.java`:1074
- **Severity:** HIGH
- **Category:** Documentation > Misleading Code-Comment Inconsistency
- **Description:** `ImpactChart.createChart()` defines X-axis labels as `"Amber","Red"` (line 86), and the no-dept overload of `getImpactChartUrl` in ChartDashboardUtil correctly passes only `{amber, red}` data (line 1049). However, the dept-filtered overload on line 1074 passes `{blue, amber, red}` -- a 3-element array -- to a chart that only has 2 axis labels. The `blue` variable is always 0 because line 1068 (`//blue += b.getBlueimpact();`) is commented out, but the data array mismatch between 2 labels and 3 data points is undocumented and potentially produces an incorrect chart.
- **Evidence:**
  - `ImpactChart.java` line 86: `AxisLabelsFactory.newAxisLabels("Amber","Red")` -- 2 labels
  - `ChartDashboardUtil.java` line 1049: `double[] dou = { amber,red };` -- 2 values (correct)
  - `ChartDashboardUtil.java` line 1074: `double[] dou = {blue,amber,red };` -- 3 values (inconsistent)
  - `ChartDashboardUtil.java` line 1068: `//blue += b.getBlueimpact();` -- blue always 0, commented out
- **Recommendation:** Fix the dept-filtered overload to match the no-dept overload by removing the `blue` element from the data array, or if blue impacts should be shown, uncomment the accumulation and add a third axis label.

---

## Summary Statistics

| Metric | Count |
|---|---|
| Files reviewed | 20 |
| Total public methods catalogued | ~176 |
| Classes with Javadoc | 0 / 20 |
| Methods with Javadoc | 0 / ~176 |
| Findings total | 14 |
| HIGH severity | 4 |
| MEDIUM severity | 4 |
| LOW severity | 2 |
| INFO severity | 4 |

### Severity Breakdown
- **HIGH (4):** A06-05 (misleading "EXAMPLE CODE" comments in 8 files), A06-06 (wrong legend/axis labels in PreopFailChart copied from MachineUnlockChart), A06-10 (misleading method name and parameter in getAllLocations), A06-14 (data/label count mismatch in ImpactChart dept overload)
- **MEDIUM (4):** A06-01 (no class Javadoc on any file), A06-02 (no method Javadoc on any method), A06-03 (missing docs on complex DAO methods), A06-04 (missing docs on complex ChartDashboardUtil methods), A06-07 (test-code markers in production)
- **LOW (2):** A06-09 (commented-out debug code), A06-13 (empty undocumented class)
- **INFO (4):** A06-08 (stale TODO stubs), A06-11 (unused arrDept variable), A06-12 (unused arrImpactData variable)
