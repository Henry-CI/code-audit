# Pass 3 -- Documentation Audit: pdf + reports Packages

**Audit agent:** A16
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Scope:** 13 files across two packages

---

## 1. MonthlyPDFRpt.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java`
**Lines:** 173

### Class-level Javadoc
None. No class-level documentation exists.

### Method-level Javadoc
| Method | Visibility | Javadoc? | Notes |
|---|---|---|---|
| `MonthlyPDFRpt(...)` | public | No | Constructor -- no documentation of 6 string parameters |
| `createPdf()` | public | No | Core method, undocumented |
| `addContent()` | private | No | -- |
| `addTitlePage()` | private | No | -- |
| `fetch_chart(String)` | private | No | -- |
| `createTable()` | private | **Yes** | Javadoc at line 96 reads "Creates our first table / @return our first table" -- **inaccurate**: method returns `void`, not a table object. Copy-pasted from `ReportPDF`. |

### Undocumented Public Methods
- `MonthlyPDFRpt(String, String, String, String, String, String)`
- `createPdf()`

### Javadoc Accuracy Issues
- `createTable()` Javadoc declares `@return our first table` but method is `void`.

### TODO / FIXME / HACK / XXX
None found.

---

## 2. ReportPDF.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java`
**Lines:** 236

### Class-level Javadoc
None.

### Method-level Javadoc
| Method | Visibility | Javadoc? | Notes |
|---|---|---|---|
| `ReportPDF(...)` | public | No | 6-param constructor |
| `createPdf()` | protected | **Yes** | Javadoc at line 55: "Creates a PDF with information about the movies" -- **inaccurate**: this is a fleet report system, not a movie system. Appears copy-pasted from an iText tutorial. `@param filename` documented but method takes no `filename` parameter. |
| `addContent()` | private | No | -- |
| `createTable()` | private | **Yes** | "Creates our first table / @return our first table" -- **inaccurate**: returns `void`. The table itself is hard-coded placeholder content ("Cell with colspan 3", "row 1; cell 1") suggesting dead/scaffold code. |
| `addMetaData()` | protected | No | -- |
| `addTitlePage()` | private | No | -- |
| `addFooter()` | protected | No | -- |
| `createList(Section)` | protected | No | Appears to be dead scaffold code with hard-coded "First point" etc. |
| `addEmptyLine(Paragraph, int)` | protected | No | -- |
| `addImage(String)` | protected | No | -- |
| `getExportDir()` | protected | No | Complex path manipulation, no documentation |
| Getters/setters (8 methods) | public | No | Standard bean pattern |

### Undocumented Public Methods
- `ReportPDF(String, String, String, String, String, String)`
- `getPdfurl()`, `setPdfurl(String)`
- `getResult()`, `setResult(String)`
- `getTitle()`, `setTitle(String)`
- `getFrom()`, `setFrom(String)`
- `getTo()`, `setTo(String)`
- `getMonth()`, `setMonth(String)`
- `getDocument()`, `setDocument(Document)`

### Javadoc Accuracy Issues
- `createPdf()`: Describes "movies" -- leftover from iText tutorial. `@param filename` does not match method signature.
- `createTable()`: `@return` tag on a void method.

### TODO / FIXME / HACK / XXX
None found.

---

## 3. Databean_cdisp.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java`
**Lines:** 1,747

### Class-level Javadoc
None.

### Method-level Javadoc
None whatsoever. Only inline `//` comments exist (e.g., `// Clears all the vectors to avoid previous junk data.`).

### Undocumented Public Methods (non-getter/setter)
- `clear_variables()` -- only has a trailing inline comment
- `init()` -- only has trailing inline comment "Function called from the jsp page."

### Undocumented Public Getter/Setter Methods
Approximately 60+ public getters/setters with no documentation. Key non-trivial fields (e.g., `no_units`, `max_impact`, `no_uncal`, `no_dislockout`) have no explanation of their semantics.

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 4. Databean_dyn_reports.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java`
**Lines:** 10,015

### Class-level Javadoc
None.

### Method-level Javadoc
None. Zero Javadoc comments in 10,015 lines. Only trailing inline comments.

### Undocumented Public Methods (non-getter/setter)
- `clear_variables()` -- inline comment only
- `getDept_prefix(String)` (line 7512)
- `init()` (line 7767) -- inline comment only
- `fetchNames()` (line 9521)

### Undocumented Public Getter/Setter Methods
Over 100 public getters/setters spanning lines 8264-9665, all undocumented. Includes semantically opaque field names (e.g., `Vrpt_veh_driv_is_technician`, `Vrpt_veh_shutdown_type`, `vorStatusNote`).

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 5. Databean_report.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java`
**Lines:** 21,854 (largest file in audit scope)

### Class-level Javadoc
None.

### Method-level Javadoc
None. Zero Javadoc comments across the entire 21,854 lines. The only documentation is occasional trailing inline comments (e.g., `// Clears all the ArrayLists to avoid previous junk data.`, `// Function called from the jsp page.`).

### Undocumented Public Methods (non-getter/setter)
- `clear_variables()` (line 584)
- `filterUnitDriverOptions()` (line 1864) -- has a block comment but not Javadoc format
- `setTimePadding(String)` (line 1993)
- `isReport_filter()` / `setReport_filter(boolean)` (lines 2024/2029)
- `getDept_prefix(String)` (line 12376)
- `getImageFromByte(InputStream, String)` (line 12941)
- `getImageFromByte(byte[], String)` (line 13906) -- overloaded variant
- `HourAdd(String, String, int, int)` (line 14118)
- `addUtilModelBean(UtilModelBean)` (line 17582)
- `init()` (line 18511)

### Undocumented Public Getter/Setter Methods
Hundreds of public getters/setters (estimated 300+) covering fields with opaque naming conventions (e.g., `Vio0_data0`, `Vio9_data2`, `sm_hour_meter`, `dsum_sb_hr`, `po_comp`).

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
| Line | Marker | Content |
|---|---|---|
| 2396 | TODO | `// TODO Auto-generated catch block` in `ParseException` handler |
| 15100 | TODO | `// TODO Auto-generated catch block` in `AddressException` handler |
| 15103 | TODO | `// TODO Auto-generated catch block` in `MessagingException` handler |

All three are auto-generated catch blocks that only call `e.printStackTrace()`.

---

## 6. Databean_report1.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java`
**Lines:** 817

### Class-level Javadoc
None.

### Method-level Javadoc
None. Only inline `//` comments on methods.

### Undocumented Public Methods (non-getter/setter)
- `clear_variables()` (line 100) -- inline comment: "Clears all the vectors to avoid previous junk data."
- `init()` (line 394) -- inline comment: "Function called from the jsp page."

### Undocumented Public Getter/Setter Methods
Approximately 50 public getters/setters, all undocumented. Opaque field names include `Vio0_data0` through `Vio9_data2`, `Viodriver_id`, `iio0_data1` etc.

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 7. Databean_reports.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_reports.java`
**Lines:** 127

### Class-level Javadoc
None.

### Method-level Javadoc
None.

### Undocumented Public Methods
- `clearVectors()` (line 49) -- empty method body, no documentation

### Special Notes
- The entire active code of this class consists of field declarations and a single empty method.
- A large `query()` method is commented out (lines 52-125), constituting approximately 60% of the file. This commented-out code block contains references to non-existent variables (`rset2`, `stmt2`) suggesting it was abandoned mid-development.

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
None found (the commented-out code references `Databean_getuser` in its error message, suggesting it may have been copied from another class).

---

## 8. LinderReportDatabean.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/LinderReportDatabean.java`
**Lines:** 1,935

### Class-level Javadoc
None.

### Method-level Javadoc
None. Zero Javadoc in the entire file.

### Undocumented Public Methods (non-getter/setter)
- `LinderReportDatabean()` (line 59) -- constructor
- `init()` (line 63) -- inline comment only
- `fetchUnitUtilisationReport()` (line 203)
- `fetchImpactReport()` (line 326)
- `fetchPreopCheckReport()` (line 415)
- `fetchSupervisorLockout()` (line 508)
- `fetchDriverLockout()` (line 554)
- `fetchNationalPreopCheckReport()` (line 679)
- `fetchNationalPreopCheckCompleted()` (line 780)
- `fetchNationalPreopCheckCompletionTime()` (line 911)
- `fetchNat2PreopChecks()` (line 1019)
- `fetchUtilByDriverLogon()` (line 1120)
- `fetchImpactByUnitWithUtil()` (line 1284)
- `fetchImpactByDriverWithUtil()` (line 1432)
- `fetchWorkHours()` (line 1708)

15 non-getter/setter public methods, all undocumented.

### Undocumented Public Getter/Setter Methods
Approximately 20 getters/setters (lines 1840-1935), all undocumented.

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
| Line | Marker | Content |
|---|---|---|
| 60 | TODO | `// TODO Auto-generated constructor stub` in empty default constructor |

---

## 9. RTLSHeatMapReport.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/RTLSHeatMapReport.java`
**Lines:** 525

### Class-level Javadoc
None.

### Method-level Javadoc
None.

### Undocumented Public Methods (non-getter/setter)
- `init()` (line 504) -- calls inherited Fetch_* methods
- `getPointsJson()` (line 512) -- core public method for generating heat map GeoJSON

### Undocumented Public Getter/Setter Methods
- `getDensity()`, `setDensity(String)`
- `getArrPoints()`, `setArrPoints(ArrayList<Points>)`

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
| Line(s) | Marker | Content |
|---|---|---|
| 99, 108, 117 | TODO | `// TODO Auto-generated catch block` -- `getPoints()` finally block |
| 182, 191, 200 | TODO | `// TODO Auto-generated catch block` -- `getSessionPoints()` finally block |
| 356, 365, 374 | TODO | `// TODO Auto-generated catch block` -- `getVehSession()` finally block |
| 412, 421, 430 | TODO | `// TODO Auto-generated catch block` -- `getOrigin()` finally block |
| 495 | TODO | `// TODO Auto-generated catch block` -- `createJSON()` catch block |

**Total: 13 TODO markers**, all auto-generated catch block stubs.

---

## 10. RTLSImpactReport.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/RTLSImpactReport.java`
**Lines:** 1,262

### Class-level Javadoc
None.

### Method-level Javadoc
None.

### Undocumented Public Methods (non-getter/setter)
- `getPointsJson()` (line 897) -- generates impact location + speed GeoJSON
- `generateSpeedList()` (line 920) -- populates speed map with filter
- `caculateImpactCacheTable()` (line 940) -- note misspelling: "caculate" instead of "calculate"
- `checkRTLSCustomer(String)` (line 1101) -- checks if customer is RTLS-enabled

### Undocumented Public Getter/Setter Methods
- `getMaxSpeed()`, `setMaxSpeed(double)`
- `getShock_id()`, `setShock_id(int)`
- `getMap_dt()`, `setMap_dt(String)`
- `getSpeedMap()`, `setSpeedMap(...)`
- `getSpeedMapwithFilter()`, `setSpeedMapwithFilter(...)`

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
| Line(s) | Marker | Content |
|---|---|---|
| 96, 105, 114, 154, 163, 172, 218, 227, 236, 281, 290, 299, 343, 352, 361, 401, 410, 419, 458, 467, 476, 595, 604, 613, 659, 668, 677, 888, 1012, 1021, 1030, 1073, 1082, 1091, 1137, 1146, 1155 | TODO | `// TODO Auto-generated catch block` -- boilerplate in finally blocks across all private methods |
| 690 | TODO | `//TODO find a suitable minimum distance. Default is 0.3` -- **actionable TODO**: indicates an untuned algorithmic parameter (`min_dist = 0.01`) |

**Total: 38 TODO markers.** 37 are auto-generated catch block stubs; 1 is an actionable technical debt item regarding an untuned `min_dist` parameter in the `caculatespeed()` method.

---

## 11. Reports.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/Reports.java`
**Lines:** 608

### Class-level Javadoc
None.

### Method-level Javadoc
None.

### Undocumented Public Methods (non-getter/setter)
- `Fetch_customers()` (line 49) -- naming convention inconsistency (capitalized prefix)
- `Fetch_cust_locations()` (line 111)
- `Fetch_cust_depts()` (line 177)
- `Fetch_cust_veh()` (line 265)
- `getVehTag(int)` (line 331)

### Undocumented Public Getter/Setter Methods
Approximately 40 getters/setters spanning lines 399-608, all undocumented.

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
| Line(s) | Marker | Content |
|---|---|---|
| 84, 93, 102 | TODO | `// TODO Auto-generated catch block` -- `Fetch_customers()` finally block |
| 151, 160, 169 | TODO | `// TODO Auto-generated catch block` -- `Fetch_cust_locations()` finally block |
| 239, 248, 257 | TODO | `// TODO Auto-generated catch block` -- `Fetch_cust_depts()` finally block |
| 305, 314, 323 | TODO | `// TODO Auto-generated catch block` -- `Fetch_cust_veh()` finally block |
| 370, 379, 388 | TODO | `// TODO Auto-generated catch block` -- `getVehTag(int)` finally block |

**Total: 15 TODO markers**, all auto-generated catch block stubs.

---

## 12. UtilBean.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/UtilBean.java`
**Lines:** 71

### Class-level Javadoc
None.

### Method-level Javadoc
None.

### Undocumented Public Methods
- `getUtil_no_veh_day()`, `setUtil_no_veh_day(int[])`
- `getUtil_date()`, `setUtil_date(String)`
- `getUtil_day()`, `setUtil_day(String)`
- `getSiteOpen()`, `setSiteOpen(String[])`
- `compareTo(UtilBean)` -- implements `Comparable<UtilBean>`, undocumented sorting semantics
- `getDay_num()`
- `setDayNum(String)` -- public method that converts day name to numeric; Monday maps to 0, starts week from Monday (unconventional)

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 13. UtilModelBean.java

**Path:** `WEB-INF/src/com/torrent/surat/fms6/reports/UtilModelBean.java`
**Lines:** 65

### Class-level Javadoc
None.

### Method-level Javadoc
None.

### Undocumented Public Methods
- `getAvatruck()`, `setAvatruck(int)` -- unclear what "avatruck" means
- `add(UtilBean)` -- adds to internal list, undocumented
- `getCustomer()`, `setCustomer(String)`
- `getSite()`, `setSite(String)`
- `getDepartment()`, `setDepartment(String)`
- `getModel()`, `setModel(String)`
- `getUb()`, `setUb(ArrayList)` -- raw type ArrayList, undocumented

### Javadoc Accuracy Issues
N/A -- no Javadoc exists.

### TODO / FIXME / HACK / XXX
None found.

---

## Summary

### Documentation Coverage

| File | Lines | Class Javadoc | Any Method Javadoc | Javadoc Accuracy Issues |
|---|---|---|---|---|
| MonthlyPDFRpt.java | 173 | No | 1 (private, inaccurate) | `@return` on void |
| ReportPDF.java | 236 | No | 2 (inaccurate) | "movies" reference; `@param` mismatch; `@return` on void |
| Databean_cdisp.java | 1,747 | No | 0 | N/A |
| Databean_dyn_reports.java | 10,015 | No | 0 | N/A |
| Databean_report.java | 21,854 | No | 0 | N/A |
| Databean_report1.java | 817 | No | 0 | N/A |
| Databean_reports.java | 127 | No | 0 | N/A |
| LinderReportDatabean.java | 1,935 | No | 0 | N/A |
| RTLSHeatMapReport.java | 525 | No | 0 | N/A |
| RTLSImpactReport.java | 1,262 | No | 0 | N/A |
| Reports.java | 608 | No | 0 | N/A |
| UtilBean.java | 71 | No | 0 | N/A |
| UtilModelBean.java | 65 | No | 0 | N/A |
| **TOTAL** | **39,435** | **0/13** | **3 methods (all inaccurate)** | **3 issues** |

### TODO/FIXME/HACK/XXX Summary

| File | Count | Type |
|---|---|---|
| RTLSImpactReport.java | 38 | 37 auto-generated catch stubs + 1 actionable (min_dist tuning) |
| Reports.java | 15 | All auto-generated catch stubs |
| RTLSHeatMapReport.java | 13 | All auto-generated catch stubs |
| Databean_report.java | 3 | All auto-generated catch stubs |
| LinderReportDatabean.java | 1 | Auto-generated constructor stub |
| **TOTAL** | **70** | **69 auto-generated stubs + 1 actionable** |

### Key Findings

1. **Near-total absence of documentation.** Across 39,435 lines of code, there are exactly 0 class-level Javadoc comments and only 3 method-level Javadoc comments (all inaccurate).

2. **All existing Javadoc is copy-pasted from iText tutorials.** The `createPdf()` Javadoc references "movies" and a `filename` parameter that does not exist. The `createTable()` Javadoc declares `@return` on void methods. These were clearly pasted from the iText library's sample code and never corrected.

3. **70 TODO markers across 5 files**, of which 69 are boilerplate `// TODO Auto-generated catch block` stubs from IDE code generation. One actionable TODO exists at `RTLSImpactReport.java:690` regarding an untuned `min_dist` parameter.

4. **Opaque field naming throughout.** Fields like `Vio0_data0`, `Vio9_data2`, `sm_hour_meter`, `dsum_sb_hr`, `po_comp`, and `Vrpt_veh_driv_is_technician` appear across multiple Databean classes with zero documentation. Their meaning can only be inferred by tracing SQL queries to database columns.

5. **Massive `init()` methods serve as undocumented dispatch hubs.** `Databean_report.init()` (line 18511, spanning ~400 lines) dispatches to 30+ private methods based on opcode strings, with no documentation of valid opcodes or their effects. `Databean_dyn_reports.init()` (line 7767) and `Databean_cdisp.init()` (line 1264) follow the same pattern.

6. **Databean_reports.java is effectively dead.** Its only active method `clearVectors()` has an empty body, and the entire `query()` method is commented out with references to an unrelated class (`Databean_getuser`).
