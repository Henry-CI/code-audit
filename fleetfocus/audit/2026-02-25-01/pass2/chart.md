# Pass 2 -- Test Coverage: chart package
**Agent:** A05
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Criterion | Status |
|---|---|
| Test directory (`test/`, `src/test/`) | **Not present** |
| Test framework dependency (JUnit, TestNG) | **Not present** in any build config |
| Test files (`*Test.java`, `*Tests.java`, `*Spec.java`) | **None found** -- one file `EncryptTest.java` exists but is a decompiled utility class, not a test |
| Test runner configuration (Maven Surefire, Gradle Test) | **Not present** |
| CI/CD test stage | **Not evident** in repository |
| Code coverage tooling (JaCoCo, Cobertura) | **Not present** |
| Mocking libraries (Mockito, EasyMock) | **Not present** |

**Conclusion:** The repository has **zero test infrastructure**. There are no unit tests, no integration tests, and no test framework dependencies anywhere in the codebase. Every public method in the chart package has **0% test coverage**.

---

## Reading Evidence

### Chart.java (base class)
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/Chart.java`
- **Class:** `Chart` (lines 8-84)
- **Extends:** none (root base class for chart hierarchy)
- **Fields:** `report` (String, protected, line 10), `yAxis` (double, protected, line 11), `colors` (ArrayList\<Color\>, protected, line 12)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `double caculateyAxis(double yAxis)` | 15 | public |
| 2 | `double getyAxis()` | 42 | public |
| 3 | `void setyAxis(double yAxis)` | 46 | public |
| 4 | `String createChart()` | 50 | public |
| 5 | `String getReport()` | 55 | public |
| 6 | `void setReport(String report)` | 59 | public |
| 7 | `void addColors()` | 63 | public |
| 8 | `ArrayList<Color> getColors()` | 79 | public |

**Notes:**
- `caculateyAxis` (line 15) is a typo for "calculateYAxis" -- this is the central axis-scaling algorithm used by all subclasses.
- Contains branching logic for yAxis values at thresholds: 0, <10, >100, >10 (lines 18-35).
- `createChart()` returns empty string -- serves as an overridable base method (lines 50-53).
- `addColors()` hardcodes exactly 13 colors (lines 63-77); subclasses that need >13 series will get `IndexOutOfBoundsException`.

---

### BarChartCategory.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/BarChartCategory.java`
- **Class:** `BarChartCategory extends Chart` (lines 8-130)
- **Fields:** `data` (ArrayList\<double[]\>, line 9), `yAxisLabel` (ArrayList\<String\>, line 11), `total` (int, line 13)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `int getTotal()` | 16 | public |
| 2 | `void setTotal(int total)` | 20 | public |
| 3 | `ArrayList<String> getyAxisLabel()` | 24 | public |
| 4 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | 28 | public |
| 5 | `BarChartCategory(ArrayList<double[]>, ArrayList<String>, int)` | 32 | public (constructor) |
| 6 | `ArrayList<double[]> getData()` | 43 | public |
| 7 | `void setData(ArrayList<double[]> data)` | 47 | public |
| 8 | `void setyAxis()` | 51 | public |
| 9 | `String createChart()` | 58 | public |

**Notes:**
- Constructor (line 32) calls `this.setyAxis()` then `this.addColors()` from parent.
- `createChart()` (line 58): iterates `data` and accesses `this.colors.get(i)` and `this.yAxisLabel.get(i)` -- will throw `IndexOutOfBoundsException` if `data.size() > colors.size()` (13) or `data.size() > yAxisLabel.size()`.
- Division `100*total/this.yAxis` (line 79): potential division by zero if `yAxis == 0`.
- Marker loop `while(i<=100)` (line 77) with `i = i+7` -- iterates approximately 15 times; hardcoded logic.

---

### BarChartImpactCategory.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/BarChartImpactCategory.java`
- **Class:** `BarChartImpactCategory extends Chart` (lines 20-122)
- **Fields:** `data` (ArrayList\<double[]\>, line 23), `yAxisLabel` (ArrayList\<String\>, line 25)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `ArrayList<String> getyAxisLabel()` | 28 | public |
| 2 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | 32 | public |
| 3 | `void addyAxisLabel(String yAxisLabel)` | 36 | public |
| 4 | `BarChartImpactCategory(ArrayList<double[]> data)` | 40 | public (constructor) |
| 5 | `void addColors()` | 51 | public (override) |
| 6 | `ArrayList<double[]> getData()` | 57 | public |
| 7 | `void setData(ArrayList<double[]> data)` | 61 | public |
| 8 | `void setyAxis()` | 65 | public |
| 9 | `String createChart()` | 71 | public |

**Notes:**
- `addColors()` (line 51) overrides parent but only adds 3 colors (Blue, Orange, Red), while parent adds 13. Correct for this specific chart but fragile.
- Constructor (line 40) calls `this.addColors()` from parent `Chart.addColors()` context -- but since `addColors()` is overridden here, polymorphic dispatch correctly calls the local 3-color version. However, the constructor also calls parent `addColors()` through `this.addColors()` which means the parent's colors list is populated with 3 items.
- `setyAxis()` (line 65) calls `DataUtil.maxArrayValue()` -- external dependency not testable without integration.
- `createChart()` (line 71): loop skips "blue" entries (line 79 `equalsIgnoreCase("blue")`) -- hardcoded business logic filtering.

---

### BarChartNational.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/BarChartNational.java`
- **Class:** `BarChartNational extends Chart` (lines 21-105)
- **Fields:** `data` (List\<EntityBean\>, line 22)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `List<EntityBean> getData()` | 24 | public |
| 2 | `void setData(List<EntityBean> data)` | 28 | public |
| 3 | `BarChartNational(List<EntityBean> arrUtil_unit)` | 33 | public (constructor) |
| 4 | `void setyAxis()` | 42 | public |
| 5 | `String createChart()` | 56 | public |

**Notes:**
- `setyAxis()` (line 42): iterates data to extract percentage values but then hardcodes `this.yAxis = 100` (line 53), with the percentage extraction logic effectively dead code (lines 44-49 are computed but never used).
- `createChart()` (line 56): `datalist.getName().substring(0,18)` (line 70) will throw `StringIndexOutOfBoundsException` if name length is between `RuntimeConf.maxUnitName+1` and 17 (the check is `>RuntimeConf.maxUnitName` but hardcodes substring to 18).
- `unit.length` used as divisor for `setBarWidth(500/unit.length)` (line 91) and `setSpaceBetweenGroupsOfBars(470/unit.length)` (line 92) -- will cause `ArithmeticException` (division by zero) if `data` is empty.

---

### BarChartR.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/BarChartR.java`
- **Class:** `BarChartR extends Chart` (lines 8-96)
- **Fields:** `data` (ArrayList\<double[]\>, line 10), `yAxisLabel` (ArrayList\<String\>, line 12)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `ArrayList<String> getyAxisLabel()` | 15 | public |
| 2 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | 19 | public |
| 3 | `BarChartR(ArrayList<double[]>, ArrayList<String>)` | 23 | public (constructor) |
| 4 | `ArrayList<double[]> getData()` | 31 | public |
| 5 | `void setData(ArrayList<double[]> data)` | 35 | public |
| 6 | `void setyAxis()` | 39 | public |
| 7 | `String createChart()` | 46 | public |

**Notes:**
- `setyAxis()` (line 39) calls `DataUtil.maxTotalValue()` -- different from other chart classes which call `maxArrayValue()` or `maxValue()`.
- `createChart()` (line 46): same `IndexOutOfBoundsException` risk with `this.colors.get(i)` and `this.yAxisLabel.get(i)` if data size exceeds array bounds.
- Constructor does not call `setReport()`, so the chart title will be the parent's default `"Unknown Report"` (line 10 of Chart.java).

---

### BarChartUtil.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/BarChartUtil.java`
- **Class:** `BarChartUtil extends Chart` (lines 19-110)
- **Fields:** `data` (double[8], line 21), `total` (int, line 22), `yAxisLabel` (ArrayList\<String\>, line 33)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `int getTotal()` | 24 | public |
| 2 | `void setTotal(int total)` | 28 | public |
| 3 | `BarChartUtil(double[] data)` | 36 | public (constructor) |
| 4 | `BarChartUtil(double[] data, int total, String title)` | 45 | public (constructor) |
| 5 | `double[] getData()` | 54 | public |
| 6 | `void setData(double[] data)` | 58 | public |
| 7 | `void setyAxis()` | 62 | public |
| 8 | `String createChart()` | 69 | public |

**Notes:**
- Two constructors: single-arg (line 36) and three-arg (line 45). The single-arg constructor hardcodes the title; the three-arg allows a custom title.
- `data` field initialized to `new double[8]` (line 21) but `setData()` can replace it with any size array. The chart labels assume exactly 8 intervals (line 80: "12-03 AM" through "09-12 PM"), so data arrays of size != 8 will produce misaligned charts.
- `setyAxis()` (line 62) calls `DataUtil.maxValue(this.data)` -- uses the simple `double[]` overload.
- `yAxisLabel` field (line 33) is declared but never populated or used.

---

### BarChartUtil_bak.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/BarChartUtil_bak.java`
- **Class:** `BarChartUtil_bak extends Chart` (lines 10-94)
- **Fields:** `data` (List\<EntityBean\>, line 11)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `List<EntityBean> getData()` | 13 | public |
| 2 | `void setData(List<EntityBean> data)` | 17 | public |
| 3 | `BarChartUtil_bak(List<EntityBean> arrUtil_unit)` | 22 | public (constructor) |
| 4 | `void setyAxis()` | 31 | public |
| 5 | `String createChart()` | 45 | public |

**Notes:**
- This is a backup/legacy copy of what appears to be the predecessor of `BarChartNational.java`. Code is nearly identical.
- Same `substring(0,18)` risk (line 59) and same division-by-zero risk with `unit.length` (lines 80-81).
- Dead code: `setyAxis()` computes percentage list (lines 33-38) but never uses it, hardcoding `this.yAxis = 100` (line 42).
- The `_bak` suffix indicates this file should likely have been removed from the codebase.

---

### JfreeGroupStackChart.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/JfreeGroupStackChart.java`
- **Class:** `JfreeGroupStackChart` (lines 32-190) -- does NOT extend `Chart`
- **Fields:** none (all data is hardcoded in methods)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `JfreeGroupStackChart()` | 39 | public (constructor) |
| 2 | `CategoryDataset createDataset()` | 50 | private |
| 3 | `JFreeChart createChart(CategoryDataset dataset)` | 103 | private |
| 4 | `LegendItemCollection createLegendItems()` | 185 | private |

**Notes:**
- All methods except the constructor are private -- extremely low surface area for direct testing.
- Constructor (line 39) creates a dataset and chart but discards both results (lines 40-42). The chart object is never assigned to a field or returned.
- `createDataset()` (line 50) contains entirely hardcoded demo data ("Product 1 (US)", "Jan 04", etc.) -- appears to be sample/demo code, not production logic.
- `createLegendItems()` (line 185) returns an empty `LegendItemCollection` -- dead/placeholder code.
- Imports `ApplicationFrame` and `RefineryUtilities` (lines 27, 29) but never uses them -- unused imports.
- Does not extend `Chart` base class unlike all other chart files.

---

### LineChartR.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/LineChartR.java`
- **Class:** `LineChartR extends Chart` (lines 7-81)
- **Fields:** `data` (double[], private, line 11)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `LineChartR(double yAxis, double[] data)` | 14 | public (constructor) |
| 2 | `double[] getData()` | 20 | public |
| 3 | `void setData(double[] data)` | 25 | public |
| 4 | `void setyAxis()` | 29 | public |
| 5 | `String createChart()` | 36 | public |

**Notes:**
- Constructor (line 14) accepts `yAxis` parameter but ignores it -- `setyAxis()` recalculates from data (lines 29-33). Misleading API.
- `setyAxis()` (line 29) calls `DataUtil.maxValue(this.data)` then `caculateyAxis()`.
- `createChart()` (line 36) uses hardcoded numeric range 0-24 for X axis (line 54), assuming 24-hour data. No validation that `data.length == 25`.

---

### LineChartR_au.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/LineChartR_au.java`
- **Class:** `LineChartR_au extends Chart` (lines 5-99)
- **Fields:** `data` (double[], private, line 10), `total` (double[], private, line 11)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `LineChartR_au(double total, double[] data)` | 13 | public (constructor) |
| 2 | `double[] getData()` | 20 | public |
| 3 | `void setData(double[] data)` | 25 | public |
| 4 | `void setyAxis(double total)` | 30 | public |
| 5 | `void setTotal(double total)` | 34 | public |
| 6 | `double[] getTotal()` | 46 | public |
| 7 | `String createChart()` | 51 | public |

**Notes:**
- `setTotal(double total)` (line 34) creates a 25-element array filled with the same value -- used as horizontal reference line on chart.
- `setyAxis(double total)` (line 30) calls `caculateyAxis(total + 1)` -- adds 1 to prevent the reference line from sitting exactly at the top.
- `createChart()` (line 51) renders two lines: data and total reference line. Same hardcoded 0-24 X axis.
- The `_au` suffix suggests this is an Australia-specific variant of `LineChartR` -- code duplication rather than parameterization.

---

### PieChartR.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/PieChartR.java`
- **Class:** `PieChartR extends Chart` (lines 13-76)
- **Fields:** `data` (ArrayList\<Integer\>, line 15), `yAxisLabel` (ArrayList\<String\>, line 16)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `PieChartR(ArrayList<Integer> data)` | 19 | public (constructor) |
| 2 | `ArrayList<Integer> getData()` | 28 | public |
| 3 | `void setData(ArrayList<Integer> data)` | 32 | public |
| 4 | `ArrayList<String> getyAxisLabel()` | 36 | public |
| 5 | `void setyAxisLabel(ArrayList<String> yAxisLabel)` | 40 | public |
| 6 | `void addyAxisLabel(String yAxisLabel)` | 44 | public |
| 7 | `String createChart()` | 48 | public |
| 8 | `void addColors()` | 67 | public (override) |

**Notes:**
- Constructor (line 19) hardcodes exactly 3 labels: "Completed", "Incomplete", "Failed" (lines 22-24). If `data` has != 3 elements, `createChart()` will either skip elements or throw `IndexOutOfBoundsException`.
- `addColors()` (line 67) overrides parent with 3 custom hex colors. Calls `this.addColors()` in constructor after parent also calls it -- results in only the overridden 3 colors.
- `createChart()` (line 48) concatenates `data.get(i)+"%"` (line 54) to create slice labels -- relies on `data` containing valid percentage integers that sum to 100.
- No validation that data values sum to 100 or are non-negative.

---

### StackedBarChart.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/chart/StackedBarChart.java`
- **Class:** `StackedBarChart` (lines 37-318) -- does NOT extend `Chart`
- **Fields:** `wFrom` (String, line 43), `wTo` (String, line 44), `week` (String, line 45), `totalUnits` (int, line 46), `deptsKeys` (ArrayList, raw, line 52), `deptsData` (ArrayList\<String\>, line 53), `x` (int[5], line 54), `deptList` (ArrayList\<String\>, line 55), `modelName` (String, line 56), `location` (String, line 57), `colors` (Color[27], line 192), `serialVersionUID` (long, line 42)

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `StackedBarChart(String, ArrayList<String>, ArrayList<String>, String, String)` | 59 | public (constructor) |
| 2 | `ArrayList<String> getDataArrayList()` | 67 | public |
| 3 | `JFreeChart createChart(CategoryDataset dataset)` | 77 | private |
| 4 | `LegendItemCollection createLegendItems()` | 204 | private |
| 5 | `CategoryDataset createDataset()` | 218 | private |
| 6 | `CategoryDataset createDataset2()` | 260 | private |
| 7 | `String saveChart(String chartDir)` | 286 | public |
| 8 | `String getwFrom()` | 303 | public |
| 9 | `String getwTo()` | 307 | public |
| 10 | `String getWeek()` | 311 | public |
| 11 | `void setWeek(String week)` | 315 | public |

**Notes:**
- Most complex file in the package (318 lines). Does NOT extend `Chart` base class.
- `serialVersionUID` (line 42) declared but class is not `Serializable` -- dead field.
- `createDataset()` (line 218): parses CSV-like strings via `s.split(",")` with no validation of field count. Accesses `data[0]`, `data[1]`, `data[2]`, `data[5]`, and `data[i]` for i>=6 -- will throw `ArrayIndexOutOfBoundsException` if any string has fewer than 7 comma-separated values.
- `createDataset()` (line 231): `Integer.parseInt(data[5])` -- will throw `NumberFormatException` on non-numeric input.
- `createDataset()` (line 242): `Double.parseDouble(data[i])` -- same `NumberFormatException` risk.
- `createDataset2()` (line 260): mutates `totalUnits` field via `totalUnits = totalUnits/5` (line 268) -- side effect in a dataset creation method, meaning calling `createDataset2()` multiple times would keep dividing.
- `saveChart()` (line 286): writes to filesystem using `chartDir` path with `%20` space replacement. No path traversal validation. `IOException` is caught but only `printStackTrace()` is called -- the method still returns `file.getAbsoluteFile().toString()` even if save failed.
- `colors` array (line 192) has 27 entries -- if `deptList.size() > 27`, the renderer loop (lines 119-126) will throw `ArrayIndexOutOfBoundsException`.
- `deptsKeys` (line 52) uses raw `ArrayList` (no generic type) -- potential `ClassCastException`.
- `x` field (line 54) and `location` field (line 57) are declared but never used -- dead fields.
- Exception handling in `createChart()` (line 179) and `createDataset()` (line 253) uses broad `catch (Exception e)` with only `e.printStackTrace()`.

---

## Findings

### A05-001 -- Zero Test Coverage Across Entire chart Package
- **File:** All 12 files in `com.torrent.surat.fms6.chart`
- **Severity:** HIGH
- **Category:** Test Coverage Gap
- **Description:** The chart package contains 12 Java source files with a combined total of approximately 70+ public methods and constructors. There are zero unit tests, zero integration tests, and no test framework present in the repository. Every code path -- including critical business logic in `caculateyAxis()`, data parsing in `StackedBarChart.createDataset()`, and file I/O in `StackedBarChart.saveChart()` -- is entirely untested.
- **Evidence:** Repository-wide search for `@Test`, `import org.junit`, `import org.testng` returns zero results in production code. No `test/` or `src/test/` directories exist. No test dependencies in build configuration.
- **Recommendation:** Introduce JUnit 4/5 with a Maven or Gradle build configuration. Prioritize testing in order: (1) `Chart.caculateyAxis()` -- pure logic with clear boundary conditions, (2) `StackedBarChart.createDataset()` -- complex CSV parsing, (3) `StackedBarChart.saveChart()` -- file I/O with error paths.

---

### A05-002 -- Chart.caculateyAxis() Has Untested Boundary Conditions
- **File:** `Chart.java`, line 15
- **Severity:** HIGH
- **Category:** Test Coverage Gap -- Critical Logic
- **Description:** The `caculateyAxis(double yAxis)` method is the central axis-scaling algorithm inherited by 10 of 12 classes in the package. It contains 5 branches (yAxis == 0, <10, >100, >10, and the implicit exactly-10 case). The exactly-10 boundary falls through all conditions and returns unscaled, which may not be intentional. None of these branches are tested.
- **Evidence:** Lines 18-38 of `Chart.java`. When `yAxis == 10.0`, the conditions `yAxis == 0.0` (false), `yAxis < 10` (false), `yAxis > 100` (false), `yAxis > 10` (false) all fail, returning 10.0 unmodified. This is correct but undocumented and untested.
- **Recommendation:** Create parameterized unit tests covering: `0.0` (should return 10), `0.5` (should return 2), `5.0` (should return 7), `10.0` (boundary -- returns 10), `10.1` (should return 20), `50.0` (should return 60), `100.0` (should return 110), `100.1` (should return 200), `999.0` (should return 1000), negative values (currently unhandled).

---

### A05-003 -- IndexOutOfBoundsException Risk in createChart() Loops
- **File:** `BarChartCategory.java` (line 68), `BarChartR.java` (line 59), `BarChartImpactCategory.java` (line 80-82)
- **Severity:** MEDIUM
- **Category:** Test Coverage Gap -- Error Path
- **Description:** Multiple `createChart()` methods iterate over `data` and access `this.colors.get(i)` and `this.yAxisLabel.get(i)` without bounds checking. The parent `addColors()` provides 13 colors; if any chart is constructed with more than 13 data series, a runtime `IndexOutOfBoundsException` will occur. No test exists to validate that data size constraints are enforced.
- **Evidence:** `BarChartCategory.java` line 68: `this.colors.get(i)` where `i` ranges from 0 to `data.size()-1`. `Chart.addColors()` adds exactly 13 colors (lines 63-77 of `Chart.java`).
- **Recommendation:** Write tests that: (1) verify normal operation with 1-13 data series, (2) verify behavior with 0 data series (empty chart), (3) assert that >13 data series either throws a clear exception or is handled gracefully.

---

### A05-004 -- Division by Zero in BarChartNational and BarChartUtil_bak
- **File:** `BarChartNational.java` (lines 91-92), `BarChartUtil_bak.java` (lines 80-81)
- **Severity:** MEDIUM
- **Category:** Test Coverage Gap -- Edge Case
- **Description:** Both files compute `500/unit.length` and `470/unit.length` for chart bar width and spacing. When `data` is an empty list, `unit.length` is 0, causing an `ArithmeticException` (integer division by zero). No test validates the empty-data edge case.
- **Evidence:** `BarChartNational.java` line 91: `chart.setBarWidth(500/unit.length)` where `unit = new String[data.size()]`.
- **Recommendation:** Write unit tests with empty `List<EntityBean>` input and verify either graceful handling or a descriptive exception. Add guard clause for empty data.

---

### A05-005 -- StackedBarChart.createDataset() CSV Parsing Untested
- **File:** `StackedBarChart.java`, lines 218-258
- **Severity:** HIGH
- **Category:** Test Coverage Gap -- Data Processing
- **Description:** `createDataset()` parses comma-separated strings from `deptsData` and accesses array indices 0, 1, 2, 5, and 6+ without validation. This is the most complex data transformation in the chart package and has zero test coverage. Malformed input will cause `ArrayIndexOutOfBoundsException`, `NumberFormatException`, or silent data corruption.
- **Evidence:** Line 225: `String[] data = s.split(",")` with subsequent unguarded access `data[0]`, `data[1]`, `data[2]`, `data[5]`. Line 231: `Integer.parseInt(data[5])`. Line 242: `Double.parseDouble(data[i])`.
- **Recommendation:** Write tests covering: (1) well-formed CSV strings with expected field count, (2) strings with fewer than 7 fields, (3) non-numeric values in numeric fields, (4) empty string input, (5) null elements in `deptsData` list.

---

### A05-006 -- StackedBarChart.saveChart() File I/O Untested
- **File:** `StackedBarChart.java`, lines 286-300
- **Severity:** MEDIUM
- **Category:** Test Coverage Gap -- I/O and Error Handling
- **Description:** `saveChart()` writes a PNG file to a filesystem path constructed from user-provided `chartDir`. The method uses `%20` replacement for spaces (line 287), generates a random filename via `DataUtil.generateRadomName()`, and swallows `IOException` (line 296). If the write fails, the method still returns the intended file path as though it succeeded. None of this behavior is tested.
- **Evidence:** Lines 286-300: `File file = new File(chartDir.replace("%20", " ") + "/chart_img/" + DataUtil.generateRadomName() + ".png")`. The `catch (IOException e) { e.printStackTrace(); }` on line 295-297 does not re-throw or return a failure indicator.
- **Recommendation:** Write tests that: (1) verify file is created at expected path, (2) verify behavior with invalid/nonexistent `chartDir`, (3) verify behavior when disk is full or path is read-only, (4) verify `%20` replacement works correctly, (5) verify return value when IOException occurs.

---

### A05-007 -- StackedBarChart.createDataset2() Side Effect on totalUnits
- **File:** `StackedBarChart.java`, line 268
- **Severity:** MEDIUM
- **Category:** Test Coverage Gap -- Stateful Bug
- **Description:** `createDataset2()` mutates the instance field `totalUnits` via `totalUnits = totalUnits/5` (line 268). This method is called from within `createChart()` (line 149), meaning `totalUnits` is permanently altered after chart creation. If `saveChart()` is called multiple times (or `createDataset2()` is invoked again), `totalUnits` will be repeatedly divided by 5, producing incorrect values. No test validates this side effect.
- **Evidence:** Line 268: `totalUnits = totalUnits/5;`. This is called at line 149: `final CategoryDataset dataset2 = createDataset2();`.
- **Recommendation:** Write a test that calls `saveChart()` twice and verifies that `totalUnits` and chart output remain consistent. The fix would be to use a local variable instead of mutating the field.

---

### A05-008 -- PieChartR Assumes Exactly 3 Data Elements
- **File:** `PieChartR.java`, lines 19-26, 48-65
- **Severity:** MEDIUM
- **Category:** Test Coverage Gap -- Contract Violation
- **Description:** The constructor hardcodes 3 labels ("Completed", "Incomplete", "Failed") and 3 colors. The `createChart()` method iterates over `data.size()` and accesses `this.colors.get(i)` and `yAxisLabel.get(i)`. If `data` has fewer or more than 3 elements, the chart will either miss slices or throw `IndexOutOfBoundsException`. No test validates this implicit contract.
- **Evidence:** Constructor lines 22-24 add exactly 3 labels. `addColors()` override (lines 67-74) adds exactly 3 colors. `createChart()` loop (line 52) iterates `data.size()`.
- **Recommendation:** Write tests with: (1) exactly 3 data elements (happy path), (2) 0 elements, (3) 1 element, (4) 5 elements. Consider adding a constructor validation that `data.size() == 3`.

---

### A05-009 -- LineChartR Constructor Ignores yAxis Parameter
- **File:** `LineChartR.java`, line 14
- **Severity:** LOW
- **Category:** Test Coverage Gap -- API Contract
- **Description:** The constructor `LineChartR(double yAxis, double[] data)` accepts a `yAxis` parameter but immediately calls `this.setyAxis()` which recalculates from data, discarding the caller-provided value. No test verifies this behavior or documents whether it is intentional.
- **Evidence:** Line 14: `public LineChartR(double yAxis,double[] data)`. Line 17: `this.setyAxis()` which at line 31 computes `double max = DataUtil.maxValue(this.data)`.
- **Recommendation:** Write a test that constructs a `LineChartR` with a specific `yAxis` value and verifies whether the provided value or the calculated value takes effect. If the parameter is intentionally ignored, remove it from the constructor signature.

---

### A05-010 -- BarChartUtil_bak.java is Dead Code Without Tests
- **File:** `BarChartUtil_bak.java` (entire file, 94 lines)
- **Severity:** LOW
- **Category:** Test Coverage Gap -- Dead Code
- **Description:** The `_bak` suffix indicates this is a backup copy. The class `BarChartUtil_bak` is functionally identical to `BarChartNational` with minor differences. It is included in the compiled codebase but is likely unused. No tests exist to verify whether it is referenced or can be safely removed.
- **Evidence:** File path includes `_bak` suffix. Class content is nearly identical to `BarChartNational.java`. Both share the same dead code in `setyAxis()` and same `substring(0,18)` logic.
- **Recommendation:** Search for references to `BarChartUtil_bak` across the codebase. If unreferenced, remove it. If referenced, write tests equivalent to `BarChartNational` tests. Either way, add a test to document the decision.

---

### A05-011 -- JfreeGroupStackChart Contains Only Hardcoded Demo Data
- **File:** `JfreeGroupStackChart.java` (entire file, 190 lines)
- **Severity:** LOW
- **Category:** Test Coverage Gap -- Dead/Demo Code
- **Description:** The class contains entirely hardcoded demo data ("Product 1 (US)", "Jan 04") with no parameterization. The constructor creates a chart and discards it. All data-producing methods are private. This appears to be sample/demo code that was never adapted for production use. No tests exist to confirm it is unused or to validate its output.
- **Evidence:** `createDataset()` (lines 50-93) contains only hardcoded `result.addValue()` calls. Constructor (lines 39-43) creates objects but discards them. `createLegendItems()` (line 185) returns empty collection.
- **Recommendation:** Determine if this class is referenced anywhere in the application. If unused, remove it. If used, refactor to accept dynamic data and write corresponding tests.

---

### A05-012 -- Broad Exception Handling in StackedBarChart Swallows Errors
- **File:** `StackedBarChart.java`, lines 179, 253, 295
- **Severity:** MEDIUM
- **Category:** Test Coverage Gap -- Error Path
- **Description:** Three locations use `catch (Exception e) { e.printStackTrace(); }` which swallows all exceptions including unexpected `RuntimeException` types. Since no tests exist, it is impossible to verify that error conditions are handled correctly or that the calling code can detect failures.
- **Evidence:** Line 179: `catch (Exception e) { e.printStackTrace(); }` in `createChart()`. Line 253: same pattern in `createDataset()`. Line 295: `catch (IOException e) { e.printStackTrace(); }` in `saveChart()`.
- **Recommendation:** Write tests that trigger each exception path and verify that: (1) the exception is logged properly, (2) the calling method returns a meaningful result or re-throws, (3) the application state remains consistent after the error.

---

### A05-013 -- String Truncation Bug Risk in BarChartNational.createChart()
- **File:** `BarChartNational.java`, lines 68-73
- **Severity:** MEDIUM
- **Category:** Test Coverage Gap -- Edge Case
- **Description:** The name truncation logic checks `if(datalist.getName().length() > RuntimeConf.maxUnitName)` then hardcodes `substring(0,18)`. If `RuntimeConf.maxUnitName` is a value less than 18 (e.g., 15), and a name is 16 characters long, the condition is true but `substring(0,18)` will throw `StringIndexOutOfBoundsException`. If `maxUnitName` is greater than 18, names between 19 and `maxUnitName` length will be truncated unnecessarily. No test validates the interaction between `RuntimeConf.maxUnitName` and the hardcoded `18`.
- **Evidence:** Line 68: `if(datalist.getName().length()>RuntimeConf.maxUnitName)`. Line 70: `unit[i] = datalist.getName().substring(0,18)+"..."`.
- **Recommendation:** Write parameterized tests with names of varying lengths (0, 1, 17, 18, 19, 50 characters) and different values of `RuntimeConf.maxUnitName` to verify correct truncation behavior.

---

## Summary

| Severity | Count |
|---|---|
| HIGH | 3 |
| MEDIUM | 7 |
| LOW | 3 |
| **Total** | **13** |

### Priority Test Implementation Order

1. **Chart.caculateyAxis()** -- Pure function, easy to unit test, used by 10 subclasses (A05-002)
2. **StackedBarChart.createDataset()** -- Complex CSV parsing with multiple failure modes (A05-005)
3. **StackedBarChart.saveChart()** -- File I/O with swallowed exceptions (A05-006)
4. **PieChartR constructor + createChart()** -- Implicit 3-element contract (A05-008)
5. **BarChartNational.createChart()** -- Division by zero and string truncation risks (A05-004, A05-013)
6. **createChart() methods across all BarChart* classes** -- IndexOutOfBounds risks (A05-003)
7. **StackedBarChart.createDataset2()** -- Stateful mutation bug (A05-007)

### Estimated Test Count Needed
A minimum of **45-55 unit tests** would be required to achieve basic coverage of the public API and critical error paths in this package.
