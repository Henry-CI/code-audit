# Pass 4 -- Code Quality Audit: `chart` Package

**Auditor:** A05
**Date:** 2026-02-25
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/chart/` (12 files)
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## 1. File Inventory

| # | File | Lines | Extends Chart? | Notes |
|---|------|------:|:--------------:|-------|
| 1 | `BarChartCategory.java` | 131 | Yes | Google Charts bar chart for hourly usage |
| 2 | `BarChartImpactCategory.java` | 123 | Yes | Google Charts bar chart for impacts by day |
| 3 | `BarChartNational.java` | 106 | Yes | Google Charts bar chart for utilisation by driver |
| 4 | `BarChartR.java` | 97 | Yes | Google Charts stacked bar chart for drivers |
| 5 | `BarChartUtil.java` | 111 | Yes | Google Charts bar chart for 3-hour intervals |
| 6 | `BarChartUtil_bak.java` | 95 | Yes | **Dead code -- backup copy** |
| 7 | `Chart.java` | 84 | -- (base) | Base class for all charts4j chart types |
| 8 | `JfreeGroupStackChart.java` | 191 | No | JFreeChart grouped stacked bar -- demo data only |
| 9 | `LineChartR.java` | 82 | Yes | Google Charts line chart |
| 10 | `LineChartR_au.java` | 99 | Yes | Google Charts line chart with total line overlay |
| 11 | `PieChartR.java` | 77 | Yes | Google Charts pie chart |
| 12 | `StackedBarChart.java` | 319 | No | JFreeChart stacked bar chart with file I/O |

---

## 2. Reading Evidence Summary

Every file was read in full via the Read tool. Key structural observations:

- **Two charting libraries in use:** `com.googlecode.charts4j` (files 1-6, 9-11) and `org.jfree` (files 8, 12). The charts4j library wraps the **Google Chart Image API**, which was deprecated in 2012 and fully shut down in 2019.
- **Base class `Chart.java`** provides `caculateyAxis()` (misspelling of "calculate"), color palette, and a default empty `createChart()` return.
- **`BarChartUtil_bak.java`** is a near-identical copy of `BarChartNational.java`. Zero references exist outside of prior audit reports.
- **`JfreeGroupStackChart.java`** contains only hardcoded demo/sample data and is never referenced outside the package itself (only prior audit reports reference it).

---

## 3. Findings

### 3.1 Dead / Backup Files

| ID | Severity | File | Detail |
|----|----------|------|--------|
| CQ-01 | HIGH | `BarChartUtil_bak.java` | **`_bak` file committed to mainline.** Class name `BarChartUtil_bak` violates Java naming conventions (underscores are not standard in class names). Grep across the entire repository finds zero production references -- only prior audit markdown files mention it. This is dead code that should be removed. |
| CQ-02 | MEDIUM | `JfreeGroupStackChart.java` | Contains only hardcoded demo data ("Product 1 (US)", "Jan 04", etc.). Constructor creates a dataset and chart but discards both results. No callers found outside the file. Likely prototype/spike code that was never cleaned up. |

### 3.2 Deprecated / Sunset APIs

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-03 | CRITICAL | All `charts4j` files (1-6, 9-11) | **Google Chart Image API dependency.** `com.googlecode.charts4j` generates URLs for the Google Chart Image API (`chart.googleapis.com/chart`), which was deprecated April 2012 and shut down March 2019. Any `toURLString()` call produces a URL that no longer resolves. The entire charts4j-based charting subsystem is non-functional against the live Google service. |

### 3.3 Naming Conventions

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-04 | MEDIUM | `Chart.java:15` | Method `caculateyAxis()` is a misspelling of `calculateYAxis`. The typo propagates into every subclass call site (`BarChartCategory:55`, `BarChartImpactCategory:68`, `BarChartNational:53`, `BarChartR:42`, `BarChartUtil:65`, `BarChartUtil_bak:42`, `LineChartR:32`, `LineChartR_au:31`). |
| CQ-05 | LOW | `Chart.java:42,46` | Getter/setter `getyAxis()`/`setyAxis()` violate JavaBean conventions -- should be `getYAxis()`/`setYAxis()`. Same pattern in `BarChartCategory` (`getyAxisLabel`/`setyAxisLabel`), `BarChartImpactCategory`, `BarChartR`, `PieChartR`. |
| CQ-06 | LOW | `BarChartUtil_bak.java` | Class name contains underscore (`_bak`), violating standard Java class naming conventions. |
| CQ-07 | LOW | `LineChartR_au.java` | Class name contains underscore (`_au` suffix). Should follow standard CamelCase, e.g., `LineChartRAu` or a more descriptive name. |
| CQ-08 | LOW | `StackedBarChart.java:303,307` | Getters `getwFrom()`/`getwTo()` violate JavaBean conventions. Should be `getWFrom()`/`getWTo()`. |

### 3.4 Unused Imports

| ID | Severity | File | Line(s) | Import |
|----|----------|------|---------|--------|
| CQ-09 | LOW | `BarChartCategory.java` | 4 | `java.util.List` -- never used; only `ArrayList` is used directly. |
| CQ-10 | LOW | `BarChartCategory.java` | 6 | `com.googlecode.charts4j.*` -- wildcard import hides what is actually used. |
| CQ-11 | LOW | `BarChartR.java` | 6 | `com.googlecode.charts4j.*` -- wildcard import. |
| CQ-12 | LOW | `LineChartR.java` | 4 | `com.googlecode.charts4j.*` -- wildcard import. |
| CQ-13 | LOW | `LineChartR_au.java` | 3 | `com.googlecode.charts4j.*` -- wildcard import. |
| CQ-14 | LOW | `BarChartUtil_bak.java` | 8 | `com.googlecode.charts4j.*` -- wildcard import. |
| CQ-15 | LOW | `JfreeGroupStackChart.java` | 7-8,11,13,16,27,29 | Multiple unused imports: `ByteArrayInputStream`, `ByteArrayOutputStream`, `InputStream`, `ImageIO`, `ChartPanel`, `ApplicationFrame`, `RefineryUtilities` -- none are referenced in the class body. |
| CQ-16 | LOW | `StackedBarChart.java` | 27 | `org.jfree.ui.ApplicationFrame` -- imported but never used. |

### 3.5 Wildcard Imports

| ID | Severity | File | Line | Import |
|----|----------|------|------|--------|
| CQ-10 | LOW | `BarChartCategory.java` | 6 | `com.googlecode.charts4j.*` |
| CQ-11 | LOW | `BarChartR.java` | 6 | `com.googlecode.charts4j.*` |
| CQ-12 | LOW | `LineChartR.java` | 4 | `com.googlecode.charts4j.*` |
| CQ-13 | LOW | `LineChartR_au.java` | 3 | `com.googlecode.charts4j.*` |
| CQ-14 | LOW | `BarChartUtil_bak.java` | 8 | `com.googlecode.charts4j.*` |

These wildcard imports obscure the actual dependencies of each class and can cause ambiguous-type compilation errors if charts4j were ever updated.

### 3.6 Commented-Out Code

| ID | Severity | File | Line(s) | Content |
|----|----------|------|---------|---------|
| CQ-17 | MEDIUM | `BarChartCategory.java` | 53 | `//double max = com.torrent.surat.fms6.util.DataUtil.maxArrayValue(this.data);` |
| CQ-18 | LOW | `BarChartCategory.java` | 59 | `// EXAMPLE CODE START` boilerplate left from chart library examples. |
| CQ-19 | LOW | `BarChartCategory.java` | 102 | `//chart.addXAxisLabels(AxisLabelsFactory.newNumericRangeAxisLabels(0, 18,1));` |
| CQ-20 | LOW | `BarChartCategory.java` | 110 | `//  chart.setBarWidth(8);` |
| CQ-21 | LOW | `BarChartCategory.java` | 113 | `//  chart.setSpaceBetweenGroupsOfBars(15);` |
| CQ-22 | LOW | `BarChartCategory.java` | 116 | `//chart.setLegendPosition(LegendPosition.BOTTOM);` |
| CQ-23 | MEDIUM | `BarChartNational.java` | 51-52 | Two lines of commented-out alternative y-axis calculation logic. |
| CQ-24 | LOW | `BarChartR.java` | 55-58 | Commented-out `System.out.print` debug loop. |
| CQ-25 | LOW | `BarChartImpactCategory.java` | 100 | `// chart.addYAxisLabels(...)` |
| CQ-26 | LOW | `BarChartImpactCategory.java` | 105 | `// chart.setBarWidth(5);` |
| CQ-27 | LOW | `BarChartImpactCategory.java` | 112 | `// chart.setGrid(...)` |
| CQ-28 | LOW | `BarChartUtil.java` | 88 | `//   chart.addYAxisLabels(...)` |
| CQ-29 | LOW | `BarChartUtil.java` | 97 | `//  chart.setGrid(...)` |
| CQ-30 | MEDIUM | `BarChartUtil_bak.java` | 40-41 | Commented-out alternative y-axis calculation (same as BarChartNational). |
| CQ-31 | LOW | `StackedBarChart.java` | 64 | `// saveChart(chartDir);` -- constructor disabled the save call. |
| CQ-32 | LOW | `StackedBarChart.java` | 127 | `//renderer.setDrawBarOutline(true);` |
| CQ-33 | LOW | `StackedBarChart.java` | 161 | `// domainAxis.setCategoryLabelPositions(...)` |
| CQ-34 | LOW | `StackedBarChart.java` | 172 | `//chart.setDomainAxisLocation(AxisLocation.TOP_OR_RIGHT);` in JfreeGroupStackChart. |
| CQ-35 | LOW | `JfreeGroupStackChart.java` | 172 | `//plot.setDomainAxisLocation(AxisLocation.TOP_OR_RIGHT);` |

Across all 12 files there are **19+ distinct blocks** of commented-out code, indicating iterative development without cleanup.

### 3.7 Broad / Empty Exception Handling and `e.printStackTrace()`

| ID | Severity | File | Line(s) | Detail |
|----|----------|------|---------|--------|
| CQ-36 | HIGH | `StackedBarChart.java` | 179-181 | `catch (Exception e) { e.printStackTrace(); }` in `createChart()`. Broad catch of `Exception`, swallows the error, and uses `e.printStackTrace()` which writes to `System.err` (not application logs). Chart rendering failures will be silently lost. |
| CQ-37 | HIGH | `StackedBarChart.java` | 253-255 | `catch (Exception e) { e.printStackTrace(); }` in `createDataset()`. Same pattern -- data-parsing errors are swallowed. Partial datasets may be returned silently. |
| CQ-38 | MEDIUM | `StackedBarChart.java` | 295-297 | `catch (IOException e) { e.printStackTrace(); }` in `saveChart()`. I/O failure when writing chart PNG to disk is logged only to stderr and method continues to return a file path that may not exist on disk. |

### 3.8 Style Consistency Issues

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-39 | LOW | Package-wide | **Mixed indentation.** Tabs and spaces are intermixed. `BarChartNational.java` uses double-tab indentation for class body members while other files use single tab. |
| CQ-40 | LOW | Package-wide | **Mixed brace styles.** Some files place opening braces on the same line as the method signature (`BarChartImpactCategory`), others on the next line (`BarChartCategory` constructor at line 33, `LineChartR_au`). |
| CQ-41 | LOW | Package-wide | **Inconsistent spacing around operators.** `for(int i=0;i< data.size();i++)` in most files versus properly spaced `for (int i = 0; i < data.size(); i++)` in `BarChartImpactCategory`. |
| CQ-42 | LOW | `BarChartCategory.java`, `BarChartR.java` | `extends Chart{` -- missing space before opening brace. Same pattern in `BarChartUtil.java`, `BarChartNational.java`, `PieChartR.java`, `LineChartR.java`. |

### 3.9 Leaky Abstractions / Encapsulation

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-43 | MEDIUM | `BarChartCategory.java:9,11,13` | Fields `data`, `yAxisLabel`, and `total` have **package-private** (default) access instead of `private`. Same issue in `BarChartImpactCategory` (lines 23, 25), `BarChartNational` (line 22), `BarChartR` (lines 10, 12), `BarChartUtil` (lines 21-22, 33). Internal mutable state is exposed beyond the class. |
| CQ-44 | MEDIUM | `Chart.java:10-12` | Base class fields `report`, `yAxis`, `colors` are `protected` but mutable collections (`ArrayList<Color>`) are directly exposed to subclasses with no defensive copies. Any subclass can replace or corrupt the color list. |
| CQ-45 | LOW | Multiple files | Getter methods return mutable `ArrayList` references directly (e.g., `getData()` in `BarChartCategory`, `getColors()` in `Chart`). Callers can mutate internal state. |
| CQ-46 | MEDIUM | `StackedBarChart.java:52-57` | Fields `deptsKeys`, `deptsData`, `deptList`, `x[]`, `modelName`, `location` have **package-private** access. `deptsKeys` and `location` are never read or written after initialization (see 3.10 below). |

### 3.10 Unused Fields / Dead Fields

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-47 | MEDIUM | `StackedBarChart.java:42` | `serialVersionUID` is declared but the class does **not** implement `Serializable`. The field is completely meaningless without `Serializable`. |
| CQ-48 | MEDIUM | `StackedBarChart.java:52` | `private ArrayList deptsKeys = new ArrayList();` -- raw-type `ArrayList`, never read or populated after declaration. Dead field. |
| CQ-49 | LOW | `StackedBarChart.java:54` | `int[] x = { 1, 2, 3, 4, 5 };` -- package-private array, never referenced anywhere in the class. Dead field. |
| CQ-50 | LOW | `StackedBarChart.java:57` | `String location = "";` -- package-private field, never read or assigned beyond initialization. Dead field. |
| CQ-51 | MEDIUM | `StackedBarChart.java:43-44` | `wFrom` and `wTo` are declared with getters (`getwFrom()`, `getwTo()`) but **no setters exist** anywhere in the class. These fields will always be `null`. |
| CQ-52 | LOW | `LineChartR.java:14` | Constructor parameter `double yAxis` is accepted but never used -- the method body calls `this.setyAxis()` which recalculates from data. Misleading API. |

### 3.11 Raw Types / Missing Generics

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-53 | LOW | `StackedBarChart.java:52` | `private ArrayList deptsKeys = new ArrayList();` -- raw type `ArrayList` without generic parameter. |
| CQ-54 | LOW | `StackedBarChart.java:53,55` | `ArrayList<String> deptsData = new ArrayList();` and `ArrayList<String> deptList = new ArrayList();` -- diamond operator missing on right side (Java 7+ would warn). |

### 3.12 Potential `null` / Bounds Issues

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-55 | MEDIUM | `BarChartCategory.java:68` | `this.colors.get(i)` and `this.yAxisLabel.get(i)` are indexed by `data.size()`, but `addColors()` only adds 13 colors. If data has > 13 series, this throws `IndexOutOfBoundsException`. Same risk in `BarChartR.java:59`. |
| CQ-56 | LOW | `BarChartNational.java:70` | `datalist.getName().substring(0,18)` uses a hardcoded index `18` while `RuntimeConf.maxUnitName` is the comparison threshold. If `maxUnitName < 18`, the substring could still exceed intended length, or if length is between `maxUnitName` and 18, it would throw `StringIndexOutOfBoundsException`. |
| CQ-57 | MEDIUM | `StackedBarChart.java:124` | `colors[i]` is indexed by `i` which increments for each department. The `colors` array has 27 entries. If `deptList.size() > 27`, this throws `ArrayIndexOutOfBoundsException`. |
| CQ-58 | LOW | `Chart.java:50-52` | `createChart()` returns an empty string `""` as the default. Callers expecting a valid URL will silently get an empty string rather than a `null` or an exception signaling that chart creation was not implemented. |

### 3.13 Performance Concerns

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-59 | LOW | `StackedBarChart.java:226,229` | Inside a loop over `dataList`, a new `ArrayList<String> newModelUnitLst` is instantiated on every iteration (line 226), making the `contains` check on line 229 always operate on a fresh empty list. This is a logic bug that causes `totalUnits` to overcount. |
| CQ-60 | LOW | `StackedBarChart.java:238,245` | `dataToAdd.contains(...)` performs an O(n) scan on an `ArrayList` inside a nested loop. For large datasets, using a `HashSet` would be more efficient. |
| CQ-61 | LOW | `StackedBarChart.java:287` | `DataUtil.generateRadomName()` -- method name has a typo ("Radom" instead of "Random"), propagated from the utility class. |

### 3.14 God Classes / Responsibility

| ID | Severity | File | Detail |
|----|----------|------|--------|
| CQ-62 | MEDIUM | `StackedBarChart.java` | At 319 lines, this class handles dataset construction, chart rendering configuration, legend creation, file I/O (`saveChart`), and string-parsing of CSV data. It has the most responsibilities of any file in the package and would benefit from separating data parsing from chart rendering. |

### 3.15 Duplication

| ID | Severity | File(s) | Detail |
|----|----------|---------|--------|
| CQ-63 | MEDIUM | `BarChartUtil_bak.java` vs `BarChartNational.java` | These two files are nearly identical (95 vs 106 lines). `BarChartUtil_bak` is the dead backup. Even the commented-out code blocks are the same. |
| CQ-64 | LOW | `LineChartR.java` vs `LineChartR_au.java` | These two files share approximately 70% of their code (chart creation, axis styling, background fills). The `_au` variant adds a second "total" line. Could be consolidated. |
| CQ-65 | LOW | All `Chart` subclasses | Every subclass follows the same pattern: set data, set y-axis, add colors, create chart URL. The boilerplate `// EXAMPLE CODE START` / `// EXAMPLE CODE END` comments appear in 9 of the 10 chart-generating files, indicating code was copy-pasted from the charts4j library examples. |

---

## 4. Summary Counts

| Severity | Count |
|----------|------:|
| CRITICAL | 1 |
| HIGH | 3 |
| MEDIUM | 14 |
| LOW | 47 |
| **Total** | **65** |

---

## 5. Top Recommendations (Report Only -- No Fixes Applied)

1. **Remove `BarChartUtil_bak.java`** -- confirmed dead code with zero production references.
2. **Evaluate the charts4j dependency** -- the underlying Google Chart Image API has been non-functional since 2019. All 10 charts4j-based classes may be producing broken image URLs.
3. **Evaluate `JfreeGroupStackChart.java`** -- appears to be demo/spike code with hardcoded sample data and no callers.
4. **Replace all `e.printStackTrace()` calls** in `StackedBarChart.java` with proper logging (e.g., `log.error()`). Add meaningful error propagation instead of silently swallowing exceptions.
5. **Fix the `newModelUnitLst` scoping bug** in `StackedBarChart.java:226` -- the list is re-instantiated inside the loop, defeating the deduplication logic.
6. **Correct the `caculateyAxis` method name** to `calculateYAxis` across all files.
7. **Tighten field visibility** -- change package-private fields to `private` across all chart subclasses.
8. **Remove all commented-out code** (19+ blocks identified) and rely on version control history.
9. **Remove unused fields** in `StackedBarChart.java` (`deptsKeys`, `x[]`, `location`, `serialVersionUID`).
10. **Replace wildcard imports** with explicit imports in 5 files.

---

*End of Pass 4 audit for `chart` package.*
