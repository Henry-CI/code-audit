# Pass 3 -- Documentation Audit: `chart` Package

**Audit ID:** 2026-02-25-01
**Agent:** A05
**Pass:** 3 (Documentation)
**Date:** 2026-02-25
**Package:** `com.torrent.surat.fms6.chart`
**Source path:** `WEB-INF/src/com/torrent/surat/fms6/chart/`
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## Summary

| Metric | Value |
|---|---|
| Files audited | 12 |
| Classes with class-level Javadoc | 1 (StackedBarChart) |
| Classes missing class-level Javadoc | 11 |
| Methods with method-level Javadoc | 5 |
| Undocumented public methods (total) | 63 |
| Accuracy issues found | 4 |
| TODO/FIXME/HACK/XXX markers | 0 |
| Findings (total) | 30 |
| HIGH | 3 |
| MEDIUM | 5 |
| LOW | 11 |
| INFO | 11 |

---

## File-by-File Findings

---

### 1. BarChartCategory.java (131 lines)

**Reading evidence:** Public class extending `Chart`. Uses `charts4j` Google Charts API. Contains constructor accepting data, y-axis labels, and total; generates a grouped bar chart URL showing "Daily Usage for Hour Period" with diamond markers for "Units Available" reference line. 6 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 1 | 8 | MEDIUM | **Missing class-level Javadoc.** Class generates a category-based bar chart for daily usage by hour period; the chart rendering logic is non-trivial and warrants a class description. |
| 2 | 32-41 | LOW | **Missing Javadoc on constructor** `BarChartCategory(ArrayList<double[]>, ArrayList<String>, int)`. Constructor sets report title, data, total, y-axis, and colors -- purpose not documented. |
| 3 | 58-128 | MEDIUM | **Missing Javadoc on `createChart()`.** Complex method (70 lines) builds a Google Charts URL with data scaling, reference markers, axis labels, layout parameters. No documentation of return value semantics or side effects. |
| 4 | 16-22 | LOW | **Missing Javadoc on getters/setters** `getTotal()`, `setTotal(int)`. |
| 5 | 24-30 | LOW | **Missing Javadoc on getters/setters** `getyAxisLabel()`, `setyAxisLabel(ArrayList<String>)`. |
| 6 | 43-49 | LOW | **Missing Javadoc on getters/setters** `getData()`, `setData(ArrayList<double[]>)`. |
| 7 | 51-56 | LOW | **Missing Javadoc on `setyAxis()`.** Calculates and sets the y-axis maximum from the total count. |

**Undocumented public methods:** `getTotal()`, `setTotal(int)`, `getyAxisLabel()`, `setyAxisLabel(ArrayList<String>)`, `getData()`, `setData(ArrayList<double[]>)`, `setyAxis()`, `createChart()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 2. BarChartImpactCategory.java (123 lines)

**Reading evidence:** Public class extending `Chart`. Generates a bar chart showing "Impacts - Breakdown by Day" using `charts4j`. Hardcodes days of the week (Sun-Sat) on X axis, categorizes data into Blue/Amber/Red impact levels, but skips "blue" data during plot construction. 7 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 8 | 20 | MEDIUM | **Missing class-level Javadoc.** Class renders an impact breakdown chart by day-of-week; the Blue/Amber/Red categorization and the filtering of "blue" from chart output deserves explanation. |
| 9 | 40-49 | LOW | **Missing Javadoc on constructor** `BarChartImpactCategory(ArrayList<double[]>)`. |
| 10 | 71-120 | MEDIUM | **Missing Javadoc on `createChart()`.** Contains non-obvious filtering logic (skips "blue" category at line 79) that should be documented. |
| 11 | 51-55 | INFO | **Missing Javadoc on `addColors()`.** Overrides parent's `addColors()` with Blue/Orange/Red. Simple override but overriding behavior is not explained. |

**Undocumented public methods:** `getyAxisLabel()`, `setyAxisLabel(ArrayList<String>)`, `addyAxisLabel(String)`, `addColors()`, `getData()`, `setData(ArrayList<double[]>)`, `setyAxis()`, `createChart()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 3. BarChartNational.java (106 lines)

**Reading evidence:** Public class extending `Chart`. Generates a bar chart showing "% Utilisation by Driver logon/available hours". Consumes `EntityBean` data, truncates long unit names to 18 characters. Y-axis is hardcoded to 100. Uses `RuntimeConf.maxUnitName` for the truncation threshold but hardcodes `substring(0,18)` which may not match `maxUnitName`. 5 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 12 | 21 | LOW | **Missing class-level Javadoc.** Class generates a national utilisation bar chart. |
| 13 | 33-39 | LOW | **Missing Javadoc on constructor** `BarChartNational(List<EntityBean>)`. |
| 14 | 56-103 | LOW | **Missing Javadoc on `createChart()`.** |

**Undocumented public methods:** `getData()`, `setData(List<EntityBean>)`, `setyAxis()`, `createChart()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 4. BarChartR.java (97 lines)

**Reading evidence:** Public class extending `Chart`. Generates a stacked bar chart (time-based, 0-24 hours) with y-axis label "Drivers" and x-axis label "Time". Uses `DataUtil.maxTotalValue()` for y-axis scaling. 6 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 15 | 8 | LOW | **Missing class-level Javadoc.** Class generates a stacked bar chart for driver data over time. |
| 16 | 23-29 | LOW | **Missing Javadoc on constructor** `BarChartR(ArrayList<double[]>, ArrayList<String>)`. Does not set a report title (unlike siblings), so `report` defaults to "Unknown Report" from parent. |
| 17 | 46-94 | LOW | **Missing Javadoc on `createChart()`.** |

**Undocumented public methods:** `getyAxisLabel()`, `setyAxisLabel(ArrayList<String>)`, `getData()`, `setData(ArrayList<double[]>)`, `setyAxis()`, `createChart()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 5. BarChartUtil.java (111 lines)

**Reading evidence:** Public class extending `Chart`. Generates a bar chart for "Usage - Breakdown by 3 hour intervals" with 8 time slots (12-03 AM through 09-12 PM). Has two constructors: one simple (data only), one accepting total and title. 7 public methods + 2 constructors, 0 documented.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 18 | 19 | LOW | **Missing class-level Javadoc.** Class generates a usage bar chart by 3-hour intervals. |
| 19 | 36-52 | INFO | **Missing Javadoc on constructors.** Two overloaded constructors with different signatures. |
| 20 | 69-108 | INFO | **Missing Javadoc on `createChart()`.** |

**Undocumented public methods:** `getTotal()`, `setTotal(int)`, `getData()`, `setData(double[])`, `setyAxis()`, `createChart()` (two constructors also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 6. BarChartUtil_bak.java (95 lines)

**Reading evidence:** Public class extending `Chart`. Near-identical clone of `BarChartNational.java`. The `_bak` suffix suggests this is a backup/deprecated version. Generates "% Utilisation by Driver logon/available hours" chart from `EntityBean` data, same truncation logic, same hardcoded y-axis of 100. 5 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 21 | 10 | INFO | **Missing class-level Javadoc.** File is a backup copy (`_bak` suffix) that appears to be a near-duplicate of `BarChartNational.java`. No documentation indicates whether this is deprecated, retained for rollback, or still in active use. |

**Undocumented public methods:** `getData()`, `setData(List<EntityBean>)`, `setyAxis()`, `createChart()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 7. Chart.java (85 lines)

**Reading evidence:** Abstract-like base class (not declared abstract) for all chart types. Defines `report`, `yAxis`, `colors` fields. Provides `caculateyAxis(double)` (note: misspelling of "calculate"), `createChart()` (returns empty string -- base implementation), `addColors()` (adds 13 default colors), and standard getters/setters. 7 public methods, 0 documented.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 22 | 8 | MEDIUM | **Missing class-level Javadoc.** This is the base class for the entire chart hierarchy. It defines shared state (`report`, `yAxis`, `colors`) and shared algorithms (`caculateyAxis`). A class-level Javadoc documenting its role, intended subclassing pattern, and the `charts4j` dependency is essential. |
| 23 | 15-39 | HIGH | **Missing Javadoc on `caculateyAxis(double)`.** This is a core algorithm used by 7+ subclasses. It rounds up y-axis maximums into "nice" values (0->10, <10->ceil+1, 10-100->next multiple of 10, >100->next multiple of 100). The parameter shadows the field name `yAxis` which is confusing. No Javadoc explains the rounding algorithm, edge cases, or parameter/return semantics. Also, the method name is misspelled ("caculate" instead of "calculate"). |
| 24 | 50-53 | INFO | **Missing Javadoc on `createChart()`.** Base implementation returns empty string. Should document that subclasses are expected to override. |
| 25 | 63-77 | INFO | **Missing Javadoc on `addColors()`.** Populates the shared color palette with 13 colors. Subclasses may override (e.g., `BarChartImpactCategory`, `PieChartR`). |

**Undocumented public methods:** `caculateyAxis(double)`, `getyAxis()`, `setyAxis(double)`, `createChart()`, `getReport()`, `setReport(String)`, `addColors()`, `getColors()`.

**TODO/FIXME/HACK/XXX:** None.

---

### 8. JfreeGroupStackChart.java (191 lines)

**Reading evidence:** Public class (not extending `Chart`). Uses JFreeChart library (not charts4j). Contains hardcoded sample data for "Product 1/2/3" across "US/Europe/Asia/Middle East" regions. Constructor creates a chart but does not store or return it. All non-constructor methods are private. Appears to be demo/prototype code.

**Class-level Javadoc:** MISSING

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| 26 | 32 | INFO | **Missing class-level Javadoc.** The class appears to be demo/prototype code (hardcoded product data, unused chart result in constructor). No documentation explains purpose or whether it is in active use. |
| 27 | 34-38 | HIGH | **Misleading Javadoc on constructor.** The existing Javadoc says `"Creates a new demo."` and documents a `@param title` parameter (`"the frame title"`), but the constructor `JfreeGroupStackChart()` takes **no parameters**. The Javadoc was likely copied from a JFreeChart `ApplicationFrame` example and never updated. |
| 28 | 46-49 | INFO | **Javadoc present on `createDataset()`.** States "Creates a sample dataset" -- accurate for this demo-style class. |
| 29 | 96-102 | INFO | **Javadoc present on `createChart(CategoryDataset)`.** States "Creates a sample chart" -- accurate. |
| 30 | 179-184 | INFO | **Javadoc present on `createLegendItems()`.** Accurate but returns an empty collection; the Javadoc says items are set manually "for a subset" but the subset is actually empty. Minor accuracy gap. |

**Undocumented public methods:** (Constructor only; all other methods are private.)

**TODO/FIXME/HACK/XXX:** None.

---

### 9. LineChartR.java (82 lines)

**Reading evidence:** Public class extending `Chart`. Generates a line chart URL via `charts4j` with time (0-24) on X axis and "Units" on Y axis. Uses circle shape markers. Constructor takes `yAxis` and `data` but ignores the `yAxis` parameter (recalculates from data). 4 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

**Accuracy issue:** Constructor parameter `yAxis` is accepted but never used -- the value is immediately overwritten by `setyAxis()` which recalculates from data.

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| -- | -- | -- | No new finding IDs needed; covered by global table. Constructor at line 14 accepts `double yAxis` which is silently discarded. This is a code issue, not a doc issue per se, but if Javadoc existed it would need to note this. |

**Undocumented public methods:** `getData()`, `setData(double[])`, `setyAxis()`, `createChart()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 10. LineChartR_au.java (99 lines)

**Reading evidence:** Public class extending `Chart`. Variant of `LineChartR` that adds a horizontal "Total Units" reference line alongside the main data line. Constructor takes `total` (a double) and `data` array. The `total` field is `double[]` but `setTotal(double)` creates a 25-element array filled with the single value. 5 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

**Undocumented public methods:** `getData()`, `setData(double[])`, `setyAxis(double)`, `setTotal(double)`, `getTotal()`, `createChart()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 11. PieChartR.java (77 lines)

**Reading evidence:** Public class extending `Chart`. Generates a 3D pie chart URL via `charts4j` showing "Pre-op Check Status" with slices for Completed/Incomplete/Failed. Overrides `addColors()` with custom blue/amber/red hex colors. 7 public methods + 1 constructor, 0 documented.

**Class-level Javadoc:** MISSING

**Undocumented public methods:** `getData()`, `setData(ArrayList<Integer>)`, `getyAxisLabel()`, `setyAxisLabel(ArrayList<String>)`, `addyAxisLabel(String)`, `createChart()`, `addColors()` (constructor also undocumented).

**TODO/FIXME/HACK/XXX:** None.

---

### 12. StackedBarChart.java (319 lines)

**Reading evidence:** Public class (does not extend `Chart`). Uses JFreeChart library. Generates a stacked/grouped bar chart for "Daily Usage for Hour Period" with department-based data grouping across weekdays (M/T/W/Th/F). Saves chart as PNG file. Contains `serialVersionUID` field suggesting it once extended `ApplicationFrame` (no longer does). Has class-level and several method-level Javadoc comments.

**Class-level Javadoc:** PRESENT (line 31-36). States: "Stacked Bar Example, the data display on chart is dummy data not real data". Author: `putukus`.

| # | Line(s) | Severity | Finding |
|---|---------|----------|---------|
| -- | 31-36 | HIGH | **Misleading class-level Javadoc.** States "the data display on chart is dummy data not real data", but the `createDataset()` method (line 218) processes actual `deptsData` from the constructor parameter -- this is production data, not dummy data. The Javadoc appears to be a leftover from when the class was a demo. This is actively misleading for maintainers. |
| -- | 47-51 | INFO | **Orphaned Javadoc block.** Lines 47-51 contain `/** Constructor * @param titel */` but this block is separated from the actual constructor (line 59) by field declarations (lines 52-57). The `@param titel` is also misspelled ("titel" instead of "title") and the actual constructor takes 4 parameters, not 1. |
| -- | 71-76 | INFO | **Javadoc on `createChart(CategoryDataset)`.** Present but `@return` description is missing. |
| -- | 212-217 | INFO | **Javadoc on `createDataset()`.** States "usually get data from database with JDBC or collection" which is inaccurate -- data comes from an in-memory `ArrayList<String>` passed to the constructor. |
| -- | 286-300 | MEDIUM | **Missing Javadoc on `saveChart(String chartDir)`.** Public method that writes a PNG file to disk and returns the absolute path. File I/O side effects and directory expectations should be documented. |
| -- | 59-65 | INFO | **Constructor Javadoc misplaced.** See orphaned block above. |
| -- | 260-283 | INFO | **Missing Javadoc on `createDataset2()`.** Private method, so out-of-scope for public-method audit, but the inline comment says "row keys..." / "column keys..." which are remnants of example code. |

**Undocumented public methods:** `getDataArrayList()`, `saveChart(String)`, `getwFrom()`, `getwTo()`, `getWeek()`, `setWeek(String)` (constructor effectively undocumented due to orphaned Javadoc).

**TODO/FIXME/HACK/XXX:** None.

---

## Cross-Cutting Observations

### 1. Method name typo: `caculateyAxis` (Chart.java, line 15)

The base class defines `caculateyAxis(double)` -- a misspelling of "calculateYAxis". This method is called from 7 of the 12 files (`BarChartCategory`, `BarChartImpactCategory`, `BarChartR`, `BarChartUtil`, `LineChartR`, `LineChartR_au`, and referenced in commented-out code in `BarChartNational` and `BarChartUtil_bak`). While this is a code-level naming issue rather than strictly a documentation issue, any future Javadoc must reference this misspelled name, perpetuating confusion. Noted as INFO.

### 2. Two charting libraries in use

The package uses **two different** charting libraries without any documentation explaining the split:
- `charts4j` (Google Charts API wrapper): used by `Chart.java` and all its subclasses (10 files)
- `JFreeChart`: used by `JfreeGroupStackChart.java` and `StackedBarChart.java` (2 files)

No package-level or class-level documentation explains why two libraries coexist or which should be preferred.

### 3. Backup file in production codebase

`BarChartUtil_bak.java` is a near-identical clone of `BarChartNational.java` with no documentation indicating its status (deprecated, retained for rollback, historical reference, etc.).

### 4. Demo/prototype code

`JfreeGroupStackChart.java` contains entirely hardcoded sample data and an unused chart object in its constructor. No documentation marks it as demo, test, or prototype code.

---

## Consolidated Findings Table

| # | File | Line(s) | Severity | Description |
|---|------|---------|----------|-------------|
| 1 | BarChartCategory.java | 8 | MEDIUM | Missing class-level Javadoc on non-trivial chart class |
| 2 | BarChartCategory.java | 32-41 | LOW | Missing Javadoc on constructor |
| 3 | BarChartCategory.java | 58-128 | MEDIUM | Missing Javadoc on complex `createChart()` method (70 lines, markers, scaling) |
| 4 | BarChartCategory.java | 16-30 | LOW | Missing Javadoc on getters/setters (`getTotal`, `setTotal`, `getyAxisLabel`, `setyAxisLabel`) |
| 5 | BarChartCategory.java | 43-56 | LOW | Missing Javadoc on `getData`, `setData`, `setyAxis` |
| 6 | BarChartImpactCategory.java | 20 | MEDIUM | Missing class-level Javadoc; Blue/Amber/Red categorization undocumented |
| 7 | BarChartImpactCategory.java | 40-49 | LOW | Missing Javadoc on constructor |
| 8 | BarChartImpactCategory.java | 71-120 | MEDIUM | Missing Javadoc on `createChart()` with non-obvious blue-skip filtering |
| 9 | BarChartImpactCategory.java | 51-55 | INFO | Missing Javadoc on `addColors()` override |
| 10 | BarChartNational.java | 21 | LOW | Missing class-level Javadoc |
| 11 | BarChartNational.java | 33-39 | LOW | Missing Javadoc on constructor |
| 12 | BarChartNational.java | 56-103 | LOW | Missing Javadoc on `createChart()` |
| 13 | BarChartR.java | 8 | LOW | Missing class-level Javadoc |
| 14 | BarChartR.java | 23-29 | LOW | Missing Javadoc on constructor (does not set report title) |
| 15 | BarChartR.java | 46-94 | LOW | Missing Javadoc on `createChart()` |
| 16 | BarChartUtil.java | 19 | LOW | Missing class-level Javadoc |
| 17 | BarChartUtil.java | 36-52 | INFO | Missing Javadoc on two overloaded constructors |
| 18 | BarChartUtil.java | 69-108 | INFO | Missing Javadoc on `createChart()` |
| 19 | BarChartUtil_bak.java | 10 | INFO | Missing class-level Javadoc; `_bak` file status (deprecated?) undocumented |
| 20 | Chart.java | 8 | MEDIUM | Missing class-level Javadoc on base class of entire chart hierarchy |
| 21 | Chart.java | 15-39 | HIGH | Missing Javadoc on core algorithm `caculateyAxis(double)` used by 7+ subclasses; name misspelled; parameter shadows field |
| 22 | Chart.java | 50-53 | INFO | Missing Javadoc on base `createChart()` (override contract undocumented) |
| 23 | Chart.java | 63-77 | INFO | Missing Javadoc on `addColors()` (override contract undocumented) |
| 24 | JfreeGroupStackChart.java | 32 | INFO | Missing class-level Javadoc on apparent demo/prototype class |
| 25 | JfreeGroupStackChart.java | 34-38 | HIGH | Misleading Javadoc: documents `@param title` but constructor takes no parameters |
| 26 | JfreeGroupStackChart.java | 185-188 | INFO | Javadoc on `createLegendItems()` says "subset" but returns empty collection |
| 27 | StackedBarChart.java | 31-36 | HIGH | Misleading class-level Javadoc: says "dummy data not real data" but class processes production data |
| 28 | StackedBarChart.java | 47-51 | INFO | Orphaned/misplaced constructor Javadoc with misspelled `@param titel`; separated from actual constructor by field declarations |
| 29 | StackedBarChart.java | 212-217 | INFO | `createDataset()` Javadoc says "database with JDBC" but data comes from in-memory ArrayList |
| 30 | StackedBarChart.java | 286-300 | MEDIUM | Missing Javadoc on public `saveChart(String)` which performs file I/O |

---

## Severity Distribution

- **HIGH (3):** Misleading Javadoc on `JfreeGroupStackChart` constructor (#25), misleading "dummy data" claim on `StackedBarChart` (#27), missing Javadoc on core algorithm `caculateyAxis` in `Chart.java` (#21)
- **MEDIUM (5):** Missing class-level Javadoc on `Chart.java` base class (#20), `BarChartCategory` (#1), `BarChartImpactCategory` (#6); missing method Javadoc on complex `createChart()` methods (#3, #8); missing Javadoc on `saveChart()` with I/O (#30)
- **LOW (11):** Missing Javadoc on simpler classes, constructors, and straightforward public methods (#2, #4, #5, #7, #10, #11, #12, #13, #14, #15, #16)
- **INFO (11):** Missing Javadoc on trivial getters/setters, minor accuracy gaps in existing Javadoc, backup file status (#9, #17, #18, #19, #22, #23, #24, #26, #28, #29)

---

*End of Pass 3 audit for chart package. Report only -- no fixes applied.*
