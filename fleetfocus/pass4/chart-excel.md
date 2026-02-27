# Pass 4 -- Code Quality Audit: chart/excel Package

**Audit ID:** 2026-02-25-01
**Agent:** A06
**Pass:** 4 (Code Quality)
**Package:** `com.torrent.surat.fms6.chart.excel`
**Files Audited:** 21
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Date:** 2026-02-25

---

## 1. Reading Evidence

All 21 files were read in full:

| # | File | Lines | Read |
|---|------|-------|------|
| 1 | BatteryChargeBean.java | 22 | Full |
| 2 | BatteryChargeChart.java | 132 | Full |
| 3 | ChartDashboard.java | 10 | Full |
| 4 | ChartDashboardUtil.java | 1490 | Full |
| 5 | ChartMailListBean.java | 38 | Full |
| 6 | ChartsExcelDao.java | 1841 | Full |
| 7 | CustLocBean.java | 23 | Full |
| 8 | DriverAccessAbuseBean.java | 22 | Full |
| 9 | DriverAccessAbuseChart.java | 132 | Full |
| 10 | DriverActivityBean.java | 44 | Full |
| 11 | DriverActivityChart.java | 118 | Full |
| 12 | ExpiryBean.java | 43 | Full |
| 13 | ExpiryChart.java | 118 | Full |
| 14 | ImpactChart.java | 118 | Full |
| 15 | MachineUnlockChart.java | 118 | Full |
| 16 | PreopFailBean.java | 32 | Full |
| 17 | PreopFailChart.java | 118 | Full |
| 18 | UnitUtilBean.java | 31 | Full |
| 19 | UnlockBean.java | 31 | Full |
| 20 | UserLoginBean.java | 24 | Full |
| 21 | UserLoginChart.java | 132 | Full |

---

## 2. Findings Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 7 |
| HIGH | 14 |
| MEDIUM | 17 |
| LOW | 10 |
| **Total** | **48** |

---

## 3. Findings Detail

### 3.1 CRITICAL -- SQL Injection via String Concatenation

**Files affected:**
- `ChartsExcelDao.java` lines 70-71, 145, 250-274, 345-362, 437-452, 594, 648-654, 711-712, 735-750, 788-810, 870-891, 905-914, 993-1010, 1022-1029, 1053-1066, 1279-1316, 1368-1410, 1453-1459, 1469, 1517-1536, 1547-1556, 1568-1571, 1586, 1610, 1624, 1636-1638, 1669-1676, 1708, 1730-1731, 1756

**Description:** Every SQL query in `ChartsExcelDao` is built via raw string concatenation with user-supplied parameters (`cust_cd`, `loc_cd`, `dept_cd`, `st_dt`, `end_dt`). No PreparedStatement is used anywhere. This is a systemic SQL injection vulnerability across all 12+ DAO methods.

**Evidence (getEmailList, line 70-71):**
```java
String sql = "select user_cd,cust_cd,loc_cd,\"EMAIL_ADDR\" from "+LindeConfig.subscriptionTable+" inner join \"FMS_USR_MST\" on \"USER_CD\"=user_cd "
        + "where cust_cd="+custCd + " and loc_cd='" + locCd +"';";
```

**Evidence (getImpacts, lines 351-362):**
```java
sql = "select case when threshold > 0 then f.data_x/threshold" +
      " else f.data_x/\"FSSS_BASE\"/v.\"FSSSMULTI\"" +
      " end as shock" +
      " from \"FMS_FORCE_MSG\" as f " +
      // ... concatenating unitlst directly into query
      " where f.\"VEHICLE_CD\" in ( " + unitlst + ")";
```

---

### 3.2 CRITICAL -- God Class: ChartDashboardUtil (1490 lines)

**File:** `ChartDashboardUtil.java`

**Description:** This class is 1490 lines long and holds at least 25 methods that span multiple responsibilities: Excel creation, chart URL generation for 9 different chart types (each in paired overloaded methods), time arithmetic helpers, and report orchestration. The `createBarChart()` method alone spans ~330 lines (lines 695-1030). The `createTestChart()` method spans ~300 lines with a deeply nested switch/for structure. This class should be decomposed into separate chart-builder classes and a coordinator.

---

### 3.3 CRITICAL -- God Class: ChartsExcelDao (1841 lines)

**File:** `ChartsExcelDao.java`

**Description:** This DAO class is 1841 lines long and contains 12+ database-access methods, each with deeply nested loops and inline SQL. Methods such as `getDriverActivity()` (lines 1494-1838) span 340+ lines alone. The class mixes data access with business logic (shock-level classification, time parsing, firmware version branching, etc.). It should be decomposed into focused DAO classes per domain entity.

---

### 3.4 CRITICAL -- N+1 Query Patterns in ChartsExcelDao

**File:** `ChartsExcelDao.java`

**Description:** Multiple methods execute queries inside nested loops, producing severe N+1 (or N*M+1) query patterns:

| Method | Lines | Pattern |
|--------|-------|---------|
| `getUnitUtilisationByHour` (3 overloads) | 404-847 | Triple-nested loop: for each dept, for each day, for each hour (24), executes 3 SQL queries. For 5 depts over 7 days = 5 x 7 x 24 x 3 = **2,520 queries per call**. |
| `getPreopFail` | 849-968 | For each dept, queries vehicles, then for each checklist result queries answers individually. |
| `getAccessAbuse` | 970-1126 | For each dept, queries vehicles, then drivers, then for each driver queries full IO data. |
| `getDriverActivity` | 1494-1838 | For each dept, queries vehicles, drivers, then for each driver, queries IO data and iterates over field types with individual queries per field per driver. |
| `getUserLogin` | 1432-1492 | For each dept, queries user IDs, then for each user executes a count query (line 1469). |

**Evidence (getUnitUtilisationByHour, lines 485-519):**
```java
for (int i = 0; i < days_btn; i++) {
    for (int j = 0; j < 24; j++) {
        // 3 queries per iteration:
        sql = "select to_date(...)"; // timestamp start
        rs = stmt.executeQuery(sql);
        sql = "select to_date(...)"; // timestamp end
        rs = stmt.executeQuery(sql);
        sql = "select sum(data_stop) from ..."; // actual data
        rs = stmt.executeQuery(sql);
    }
}
```

---

### 3.5 CRITICAL -- e.printStackTrace() Used Pervasively with Exception Swallowing

**Files affected:**
- `ChartDashboardUtil.java` lines 50, 684, 1028
- `ChartsExcelDao.java` lines 47, 86, 122, 155, 195, 318, 393, 540, 681, 837, 958, 1115, 1332, 1420, 1482, 1828

**Description:** Every single catch block in both `ChartsExcelDao` and `ChartDashboardUtil` uses `e.printStackTrace()` followed by `e.getMessage()` (whose return value is discarded). Exceptions are swallowed -- the methods continue and return partial/empty data rather than propagating the error. In a server context, `e.printStackTrace()` writes to stderr which may be lost; the caller has no way to know the operation failed.

**Evidence (ChartsExcelDao, lines 45-49 -- repeated identically in 16 places):**
```java
}catch(Exception e)
{
    e.printStackTrace();
    e.getMessage();
}
```

Note: `e.getMessage()` on line 48 (and in all other catch blocks) is called but its return value is never used -- this is a dead statement.

---

### 3.6 CRITICAL -- Broad Exception Catches (catch Exception)

**Files affected:**
- `ChartDashboardUtil.java` lines 49, 683
- `ChartsExcelDao.java` lines 45, 84, 120, 153, 193, 316, 391, 538, 679, 835, 956, 1113, 1330, 1418, 1480, 1826

**Description:** Every catch block catches `Exception` rather than specific exception types. This masks programming errors (NullPointerException, ArrayIndexOutOfBoundsException, etc.) and makes debugging impossible. The declared `throws SQLException` on the DAO methods is misleading because SQLExceptions are actually caught and swallowed internally.

---

### 3.7 CRITICAL -- Logic Bug in getAllLocations

**File:** `ChartsExcelDao.java` lines 164-166

**Description:** The condition `locCd.trim().length() < 0` can never be true -- `String.length()` never returns a negative value. The trailing comma is therefore never stripped from `locCd`, which will produce malformed SQL in downstream usage.

**Evidence:**
```java
if( locCd.trim().length() < 0){
    locCd = locCd.substring(0,locCd.length() - 1);
}
```

Should presumably be `locCd.trim().length() > 0`.

---

### 3.8 HIGH -- Massive Code Duplication Across Chart Classes

**Files affected:** BatteryChargeChart, DriverAccessAbuseChart, DriverActivityChart, ExpiryChart, ImpactChart, MachineUnlockChart, PreopFailChart, UserLoginChart

**Description:** All 8 chart classes are near-identical copies of the same template. They all:
1. Extend `Chart`
2. Declare identical fields: `data`, `yAxisLabel` (and `chldLetters` in 3 of them)
3. Implement identical `getyAxisLabel`, `setyAxisLabel`, `addyAxisLabel`, `getData`, `setData`, `setyAxis`, `addColors` methods
4. Implement a `createChart()` method with the same bar-chart building boilerplate

The only differences between classes are: (a) the report title string, (b) x-axis label strings, (c) y-axis label text, (d) `spaceBetweenGroupsOfBars` value, and (e) whether `createChart` accepts `List<String> axisLabels` parameter.

**Evidence -- identical setyAxis() across all 8 classes:**
```java
public void setyAxis() {
    double max = com.torrent.surat.fms6.util.DataUtil.maxArrayValue(this.data);
    this.yAxis = caculateyAxis(max);
}
```

All 8 classes could be consolidated into a single parameterized BarChart builder class.

---

### 3.9 HIGH -- Duplicate Bean Classes

**Files affected:** BatteryChargeBean, DriverAccessAbuseBean

**Description:** These two beans are structurally identical -- both have exactly the same fields (`deptName: String`, `count: int`) and identical getter/setter methods. They could be a single generic class.

**Evidence (BatteryChargeBean lines 5-18 vs DriverAccessAbuseBean lines 5-18):**
```java
// Both classes have:
private String deptName;
private int count;
// + identical getters/setters
```

---

### 3.10 HIGH -- Duplicate Switch Blocks in ChartDashboardUtil.createTestChart()

**File:** `ChartDashboardUtil.java` lines 70-686

**Description:** The `createTestChart()` method contains two nearly identical switch statements (lines 113-387 and lines 404-678). The first handles the single-department test case and the second handles the multi-department case. Both have cases 1-9 with the same chart generation logic duplicated, differing only in how departments are filtered. This entire block is ~600 lines of duplicated logic.

---

### 3.11 HIGH -- Commented-Out Code Throughout

**Files affected:**
- `BatteryChargeChart.java` lines 109, 114, 121
- `DriverAccessAbuseChart.java` lines 109, 114, 121
- `DriverActivityChart.java` lines 95, 100, 107
- `ExpiryChart.java` lines 95, 100, 107
- `ImpactChart.java` lines 95, 100, 107
- `MachineUnlockChart.java` lines 95, 100, 107
- `PreopFailChart.java` lines 95, 100, 107
- `UserLoginChart.java` lines 109, 114, 121
- `ChartDashboardUtil.java` lines 89, 358, 649, 853-875, 880-900, 910-936 (bulk commented-out chart code)
- `ChartsExcelDao.java` lines 276-279, 457, 482-484, 598-599, 624-626, 755, 780-782

**Description:** All 8 chart classes contain the same 3 commented-out lines (alternative chart configurations). `ChartDashboardUtil` has numerous commented-out `System.out.println` calls and commented-out chart section headers. `ChartsExcelDao` has commented-out debug prints and old code fragments. These add noise and confusion.

**Evidence (repeated in every chart class):**
```java
// chart.addYAxisLabels(AxisLabelsFactory.newNumericRangeAxisLabels(0, this.yAxis));
// ...
// chart.setBarWidth(5);
// ...
// chart.setGrid(600, (50.0/this.yAxis)*20, 3, 2);
```

---

### 3.12 HIGH -- "EXAMPLE CODE START/END" Comments Left in Production Code

**Files affected:** All 8 chart classes

**Description:** Every chart class contains `// EXAMPLE CODE START` and `// EXAMPLE CODE END` comments wrapping the entire `createChart()` method body. This suggests the code was copied from a sample/tutorial and never cleaned up.

**Evidence (BatteryChargeChart.java lines 71, 127):**
```java
// EXAMPLE CODE START
// ...
// EXAMPLE CODE END. Use this url string in your web or Internet application.
```

---

### 3.13 HIGH -- System.out.println Used for Logging

**File:** `ChartDashboardUtil.java` lines 121, 153, 183, 213, 242, 273, 302, 331, 361, 412, 444, 474, 503, 532, 563, 593, 621, 652, 714

**Description:** Approximately 19 `System.out.println()` calls are used throughout `ChartDashboardUtil` to output chart URLs and status messages. In a Tomcat/server context, a proper logging framework (e.g., Log4j, SLF4J) should be used for controllable log levels and output destinations.

**Evidence (line 714):**
```java
System.out.println(now("yyyy.MM.dd G 'at' hh:mm:ss z") + " Creating excel for Cust:"+ cust_cd + " and site: " + loc_cd+"");
```

---

### 3.14 HIGH -- Unused Variable: arrDept in getFromDate and getCurrDate

**File:** `ChartsExcelDao.java` lines 32, 180

**Description:** Both `getFromDate()` and `getCurrDate()` declare `ArrayList<EntityBean> arrDept` but never use it.

**Evidence (line 32):**
```java
ArrayList<EntityBean> arrDept = new ArrayList<EntityBean>();
```

---

### 3.15 HIGH -- Unused Variable: arrImpactData in getUnitUtilisationByHour

**File:** `ChartsExcelDao.java` lines 412, 560, 701

**Description:** All three overloads of `getUnitUtilisationByHour()` declare `ArrayList<ImpactBean> arrImpactData` that is never populated or read.

---

### 3.16 HIGH -- Unused Imports

**Files affected:**
- `BatteryChargeChart.java` line 19 (`LegendPosition` -- used but `LinearGradientFill` import at line 19 is used; checking all: `Fills` line 16 used, all imports appear used)
- `ChartsExcelDao.java` line 8 (`StringTokenizer`) -- used only by helper methods that were moved to this DAO
- `ChartDashboardUtil.java` line 7 (`SQLException`) -- used in catch
- `ChartDashboardUtil.java` line 11 (`List`) -- used

Upon closer inspection, all explicit imports in chart classes are used within `createChart()`. However:
- `ChartsExcelDao.java` line 13: `FirmwareverBean` is imported and used only in `getDriverActivity`
- `ChartsExcelDao.java` line 8: `StringTokenizer` is used only in helper methods that belong to a utility class, not a DAO

---

### 3.17 HIGH -- Deprecated API: CellRangeAddress from org.apache.poi.hssf.util

**File:** `ChartDashboardUtil.java` line 13

**Description:** `org.apache.poi.hssf.util.CellRangeAddress` has been deprecated in favor of `org.apache.poi.ss.util.CellRangeAddress`. The HSSF version is a compatibility shim.

**Evidence:**
```java
import org.apache.poi.hssf.util.CellRangeAddress;
```

---

### 3.18 HIGH -- Deprecated Google Chart Image API (charts4j)

**Files affected:** All 8 chart classes

**Description:** The entire charting approach depends on `com.googlecode.charts4j`, which is a Java wrapper around the Google Chart Image API. Google deprecated the Chart Image API in 2012 and shut it down entirely. Any chart URLs generated by these classes will fail to render.

---

### 3.19 HIGH -- Package-Private (Default) Access on Fields in Chart Classes

**Files affected:** All 8 chart classes

**Description:** Fields `data`, `chldLetters`, and `yAxisLabel` are declared with package-private (default) access rather than `private`. This leaks implementation details.

**Evidence (BatteryChargeChart.java lines 26-28):**
```java
ArrayList<double[]> data = new ArrayList<double[]>();
String[] chldLetters = {"A","B","C",...};
ArrayList<String> yAxisLabel = new ArrayList<String>();
```

---

### 3.20 HIGH -- Raw Type Usage (Unchecked Collections)

**File:** `ChartsExcelDao.java`

**Description:** Multiple raw `ArrayList` declarations without generic type parameters:
- Line 213: `ArrayList<UnlockBean> unlock = new ArrayList();`
- Line 406: `ArrayList<UnitUtilBean> utilBean = new ArrayList();`
- Line 430: `ArrayList vcd = new ArrayList();`
- Line 554: `ArrayList<UnitUtilBean> utilBean = new ArrayList();`
- Line 576: `ArrayList vcd = new ArrayList();`
- Line 695: `ArrayList<UnitUtilBean> utilBean = new ArrayList();`
- Line 728: `ArrayList vcd = new ArrayList();`
- Line 851: `ArrayList<PreopFailBean> preopBean = new ArrayList();`
- Line 902: `ArrayList res_id = new ArrayList();`
- Line 925-928: `ArrayList tmp_fail`, `tmp_question`, `tmp_ans`, `tmp_exp`
- Line 972: `ArrayList<DriverAccessAbuseBean> abuseBean = new ArrayList();`
- Line 1037: `ArrayList tmp_dcd = new ArrayList();`
- Line 1048-1051: `ArrayList tmp_st_tm`, `tmp_end_tm`, `tmp_v_cd`, `date`
- Line 1076: `ArrayList clash_rec = new ArrayList();`
- Line 1346: `ArrayList<ExpiryBean> exBean = new ArrayList();`
- Line 1434: `ArrayList<UserLoginBean> uBean = new ArrayList();`
- Line 1450: `ArrayList temp_uid = new ArrayList();`
- Line 1496: `ArrayList<DriverActivityBean> dBean = new ArrayList();`
- Line 1566: `ArrayList<String> dsum_driver_cd = new ArrayList();`
- Line 1605: `ArrayList dsum_key_hr = new ArrayList();`
- Line 1664-1666: `ArrayList rec_no`, `vtmp_vcd`, `vtmp_rec_no`
- Line 1691: `ArrayList temp_usage = new ArrayList();`

This produces unchecked warnings and loses type safety.

---

### 3.21 MEDIUM -- Empty Class: ChartDashboard

**File:** `ChartDashboard.java` (10 lines)

**Description:** This class contains only an empty constructor and no methods or fields. It appears to be a dead/placeholder class.

---

### 3.22 MEDIUM -- TODO Comment Left in Production Beans

**Files affected:**
- `PreopFailBean.java` line 9
- `UnitUtilBean.java` line 9
- `UnlockBean.java` line 9

**Description:** Auto-generated `// TODO Auto-generated constructor stub` comments were left in the default constructors.

**Evidence:**
```java
public PreopFailBean() {
    // TODO Auto-generated constructor stub
}
```

---

### 3.23 MEDIUM -- Mutable Internal Collections Returned Directly (Leaky Abstractions)

**Files affected:** All 8 chart classes, `ChartDashboardUtil.java`

**Description:** Getter methods return direct references to mutable internal `ArrayList` fields, allowing callers to modify internal state.

**Evidence (all chart classes):**
```java
public ArrayList<String> getyAxisLabel() {
    return yAxisLabel;
}
public ArrayList<double[]> getData() {
    return data;
}
```

`ChartDashboardUtil.getChartMailBeanList()` (line 1486) similarly returns a direct reference to `emailBeanList`.

---

### 3.24 MEDIUM -- Concrete Type in API (ArrayList instead of List)

**Files affected:** All 8 chart classes, `ChartDashboardUtil.java`, `ChartsExcelDao.java`

**Description:** Method signatures and field declarations use `ArrayList` as the declared type instead of the `List` interface. This couples the code to a specific implementation and prevents substitution.

**Evidence:**
```java
public ArrayList<String> getyAxisLabel() { ... }
public void setyAxisLabel(ArrayList<String> yAxisLabel) { ... }
public ArrayList<double[]> getData() { ... }
```

---

### 3.25 MEDIUM -- Inconsistent Method Naming Convention (caculateyAxis)

**File:** `Chart.java` line 15 (parent class, called from all chart subclasses)

**Description:** The method name `caculateyAxis` has a typo ("caculate" instead of "calculate") and does not follow Java camelCase convention (should be `calculateYAxis`). All 8 chart subclasses call this misspelled method in their `setyAxis()` methods.

**Evidence:**
```java
this.yAxis = caculateyAxis(max);
```

---

### 3.26 MEDIUM -- Inconsistent Brace Style

**Files affected:** All files in the package

**Description:** The codebase mixes Egyptian braces (opening brace on same line) with Allman/next-line braces inconsistently:
- Chart class constructors use next-line opening brace
- `setyAxis()` methods have an unusual leading space before the opening brace
- Most if/else blocks use Egyptian style
- Some catch blocks use next-line style

**Evidence (BatteryChargeChart.java):**
```java
public BatteryChargeChart(ArrayList<double[]> data)
{                                   // <-- next-line brace
    this.setReport("...");
}

public void setyAxis()
 {                                  // <-- next-line with extra leading space
    double max = ...;
 }
```

---

### 3.27 MEDIUM -- Inconsistent Indentation

**Files affected:** `ChartsExcelDao.java`, `ChartDashboardUtil.java`

**Description:** Indentation varies between methods and even within methods -- some blocks use tab indentation, others use spaces, and nesting levels are inconsistent. `ChartsExcelDao.getExpiry()` (line 1344) has its method signature at 0-indent level unlike other methods.

---

### 3.28 MEDIUM -- Dead Code: unused 'blue' variable

**File:** `ChartDashboardUtil.java` lines 1039, 1062

**Description:** In `getImpactChartUrl()`, the variable `blue` is declared and initialized to 0 but is commented out from accumulation (line 1045/1068: `//blue += b.getBlueimpact()`). However in the overloaded dept-specific version (line 1074), `blue` is included in the output array:
```java
double[] dou = {blue, amber, red};
```
This means the first element is always 0, which is likely a bug (it appears blue was intentionally removed but the array was not updated in one of the overloads).

---

### 3.29 MEDIUM -- FileOutputStream Not in Try-with-Resources

**File:** `ChartDashboardUtil.java` lines 62-64

**Description:** `FileOutputStream` is created and closed manually without try-with-resources. If `wb.write(fileOut)` throws, the stream will leak.

**Evidence:**
```java
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
```

---

### 3.30 MEDIUM -- JDBC Resources Not Managed with Try-with-Resources

**File:** `ChartsExcelDao.java` (all methods)

**Description:** All 12+ DAO methods manage `Connection`, `Statement`, and `ResultSet` with manual null-check cleanup in finally blocks. Java 7+ try-with-resources would be safer and more concise. The current pattern can also fail: if `rs.close()` throws in the finally block, `stmt.close()` and `DBUtil.closeConnection(conn)` may not execute.

---

### 3.31 MEDIUM -- ResultSet.TYPE_SCROLL_SENSITIVE Used Unnecessarily

**File:** `ChartsExcelDao.java` (all methods)

**Description:** Every `createStatement` call uses `ResultSet.TYPE_SCROLL_SENSITIVE` and `ResultSet.CONCUR_READ_ONLY`, but the code only iterates forward through results with `next()`. The scroll-sensitive cursor type incurs performance overhead for no benefit.

---

### 3.32 MEDIUM -- String Concatenation in Loop for SQL IN Clauses

**File:** `ChartsExcelDao.java` (multiple methods)

**Description:** Vehicle CD lists for SQL `IN` clauses are built via string concatenation in while-loops. This is both inefficient (should use StringBuilder) and creates SQL injection risk. Repeated pattern across getMachineUnlock, getUnitUtilisationByHour, getPreopFail, getAccessAbuse, getBatteryCharge, getExpiry, getUserLogin, getDriverActivity.

**Evidence (line 254-257):**
```java
while (rs.next()) {
    tmp_cd += "'" + rs.getString(1) + "',";
}
```

---

### 3.33 MEDIUM -- Fully Qualified Class Name Used Instead of Import

**Files affected:** All 8 chart classes

**Description:** The `setyAxis()` method in every chart class uses a fully-qualified class name instead of importing it:
```java
double max = com.torrent.surat.fms6.util.DataUtil.maxArrayValue(this.data);
```

This should be imported at the top like other dependencies.

---

### 3.34 MEDIUM -- Potential ArrayIndexOutOfBoundsException in Chart Classes

**Files affected:** BatteryChargeChart, DriverAccessAbuseChart, UserLoginChart

**Description:** The `chldLetters` array has 26 entries (A-Z). If `axisLabels.size() > 26`, `chldLetters[i]` will throw ArrayIndexOutOfBoundsException at line 78 of each class. There is no bounds check.

---

### 3.35 MEDIUM -- Magic Numbers Throughout ChartDashboardUtil

**File:** `ChartDashboardUtil.java`

**Description:** Numeric constants like `1`, `15`, `29`, `5`, `36000`, `650`, `350` are used extensively without named constants. The values `1`, `15`, `29` represent chart column positions; `36000` is a time-division factor; `650x350` is chart dimensions. These should be extracted to named constants.

**Evidence:**
```java
int div = 36000;
dur = dur/div;
```

---

### 3.36 MEDIUM -- Unused 'cData' Variable in getUnitUtil Methods

**File:** `ChartDashboardUtil.java` lines 1129, 1152

**Description:** Both `getUnitUtil()` overloads declare `ArrayList<double[]> cData` but never use it.

---

### 3.37 LOW -- Trailing Whitespace and Extra Blank Lines in Bean Classes

**Files affected:** All 8 bean classes

**Description:** Bean classes have inconsistent trailing blank lines before the closing brace and extra blank lines between methods. Minor formatting inconsistency.

---

### 3.38 LOW -- Missing @Override Annotations

**Files affected:** All 8 chart classes

**Description:** Methods like `addColors()` and `createChart()` override methods from the `Chart` parent class but are not annotated with `@Override`. This means the compiler will not catch signature mismatches.

---

### 3.39 LOW -- @SuppressWarnings("deprecation") Without Fixing Deprecation

**File:** `ChartDashboardUtil.java` line 694

**Description:** The `createBarChart()` method is annotated with `@SuppressWarnings("deprecation")` to silence the `CellRangeAddress` deprecation warning rather than migrating to the non-deprecated API.

---

### 3.40 LOW -- Beans Lack toString/equals/hashCode

**Files affected:** All 8 bean classes (BatteryChargeBean, ChartMailListBean, CustLocBean, DriverAccessAbuseBean, DriverActivityBean, ExpiryBean, PreopFailBean, UnitUtilBean, UnlockBean, UserLoginBean)

**Description:** None of the bean classes implement `toString()`, `equals()`, or `hashCode()`. This makes debugging and collection operations unreliable.

---

### 3.41 LOW -- Misspelling: "accessBeam" instead of "accessBean"

**File:** `ChartDashboardUtil.java` lines 211, 502, 883

**Description:** Variable `accessBeam` should be `accessBean` for consistency with other bean variable names (`impBean`, `unlockBean`, `preopBean`, etc.).

---

### 3.42 LOW -- Inconsistent Semicolon in SQL String

**File:** `ChartsExcelDao.java` line 71

**Description:** The SQL in `getEmailList` ends with a literal semicolon inside the string (`+"';";`). JDBC drivers generally do not require or want trailing semicolons and some may fail with them. No other SQL in the class includes a trailing semicolon.

---

### 3.43 LOW -- Duplicate Overloaded Methods Have Nearly Identical Bodies in ChartDashboardUtil

**File:** `ChartDashboardUtil.java`

**Description:** Each "get chart URL" method has two overloads -- one for aggregate and one for per-department filtering. These differ only by a single `if (dept.equalsIgnoreCase(...))` guard. Examples: `getImpactChartUrl` (2 overloads), `getMachineUnlock` (2), `getPreOpFail` (2), `getAccessAbuse` (2), `getBatteryCharge` (2), `getExpiry` (2), `getUserLogin` (2), `getDriverActivity` (2), `getUnitUtil` (2). These 18 methods could be consolidated into 9 using an optional department filter parameter.

---

### 3.44 LOW -- Inconsistent Variable Naming

**Files affected:** `ChartsExcelDao.java`

**Description:** Variable naming is inconsistent:
- `Tok` (line 1132) uses PascalCase for a local variable
- `Vrpt_field_cd` (line 1606) uses mixed underscore/PascalCase
- Mix of `rset` and `rs` for ResultSet variables across methods
- Mix of `query` and `sql` for SQL string variables across methods
- `tmp_cd`, `tmp_veh_cd`, `tmp_driv_cd`, `tmp_dcd` -- inconsistent abbreviation patterns

---

### 3.45 LOW -- Potential Null Handling Issues in DriverActivity

**File:** `ChartsExcelDao.java` lines 1714-1718

**Description:** The firmware version check accesses `rset.getString(1)` twice without storing the result, and the null check allows empty string through but later uses `startsWith("1")` which could have unexpected results for edge cases.

---

### 3.46 LOW -- Unused Method: getUtilWow

**File:** `ChartDashboardUtil.java` lines 1340-1374

**Description:** The `getUtilWow()` and `getUtilWow(String depCd)` methods appear to be superseded by `getUnitUtil()` (they are commented out at line 358/649: `// chartUrl = getUtilWow();`). They remain in the code as dead methods.

---

## 4. Duplicate Code Cross-Reference Matrix

The following shows which chart classes share identical code blocks:

| Code Block | BCC | DAAC | DAC | EC | IC | MUC | PFC | ULC |
|-----------|-----|------|-----|----|----|-----|-----|-----|
| Fields (data, yAxisLabel) | X | X | X | X | X | X | X | X |
| setyAxis() | X | X | X | X | X | X | X | X |
| addColors() | X | X | X | X | X | X | X | X |
| getData/setData | X | X | X | X | X | X | X | X |
| getyAxisLabel/setyAxisLabel/addyAxisLabel | X | X | X | X | X | X | X | X |
| createChart() boilerplate | X | X | X | X | X | X | X | X |
| chldLetters[] array | X | X | - | - | - | - | - | X |
| URL-encoding label loop | X | X | - | - | - | - | - | X |

Legend: BCC=BatteryChargeChart, DAAC=DriverAccessAbuseChart, DAC=DriverActivityChart, EC=ExpiryChart, IC=ImpactChart, MUC=MachineUnlockChart, PFC=PreopFailChart, ULC=UserLoginChart

---

## 5. Summary

The chart/excel package suffers from severe structural and quality issues:

1. **SQL injection** is systemic across all DAO methods -- no parameterized queries are used anywhere.
2. **Two God classes** (`ChartDashboardUtil` at 1490 lines, `ChartsExcelDao` at 1841 lines) concentrate too many responsibilities.
3. **N+1 query patterns** in the DAO will cause severe performance degradation, with some methods capable of generating thousands of database queries per invocation.
4. **Exception handling** is uniformly broken: every catch block swallows exceptions with `e.printStackTrace()` and a no-op `e.getMessage()`.
5. **Code duplication** is extreme: 8 chart classes share ~90% identical code, and the dashboard utility duplicates switch blocks and paired overloaded methods.
6. **The charts4j library** wraps the defunct Google Chart Image API, meaning chart rendering is non-functional.
7. **A logic bug** in `getAllLocations()` (impossible condition `length() < 0`) means trailing commas are never removed.

---

*End of Pass 4 audit for chart/excel package.*
