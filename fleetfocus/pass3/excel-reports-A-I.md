# Pass 3 -- Documentation Audit: Excel Report Servlets A-I

**Audit agent:** A11
**Date:** 2026-02-25
**Pass:** 3 (Documentation)
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/` -- 18 files (ExcelBatteryReport through ExcelImpactReport)
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## 1. Reading Evidence

All 18 files were read in full. Line counts per file:

| # | File | Lines | Read in full |
|---|------|------:|:------------:|
| 1 | ExcelBatteryReport.java | 121 | Yes |
| 2 | ExcelBroadcastMsgReport.java | 137 | Yes |
| 3 | ExcelCimplicityShockReport.java | 145 | Yes |
| 4 | ExcelCimplicityUtilReport.java | 141 | Yes |
| 5 | ExcelCurrDrivReport.java | 126 | Yes |
| 6 | ExcelCurrUnitReport.java | 132 | Yes |
| 7 | ExcelDailyVehSummaryReport.java | 277 | Yes |
| 8 | ExcelDriverAccessAbuseReport.java | 198 | Yes |
| 9 | ExcelDriverImpactReport.java | 146 | Yes |
| 10 | ExcelDriverLicenceExpiry.java | 102 | Yes |
| 11 | ExcelDynDriverReport.java | 307 | Yes |
| 12 | ExcelDynSeenReport.java | 214 | Yes |
| 13 | ExcelDynTransportDriverReport.java | 228 | Yes |
| 14 | ExcelDynUnitReport.java | 328 | Yes |
| 15 | ExcelExceptionSessionReport.java | 354 | Yes |
| 16 | ExcelHireDehireReport.java | 135 | Yes |
| 17 | ExcelImpactMeterReport.java | 198 | Yes |
| 18 | ExcelImpactReport.java | 254 | Yes |

---

## 2. Class-Level Javadoc

| # | File | Has Class Javadoc | Notes |
|---|------|:-----------------:|-------|
| 1 | ExcelBatteryReport.java | NO | No class-level documentation of any kind |
| 2 | ExcelBroadcastMsgReport.java | NO | No class-level documentation of any kind |
| 3 | ExcelCimplicityShockReport.java | NO | No class-level documentation of any kind |
| 4 | ExcelCimplicityUtilReport.java | NO | No class-level documentation of any kind |
| 5 | ExcelCurrDrivReport.java | NO | No class-level documentation of any kind |
| 6 | ExcelCurrUnitReport.java | NO | No class-level documentation of any kind |
| 7 | ExcelDailyVehSummaryReport.java | NO | No class-level documentation of any kind |
| 8 | ExcelDriverAccessAbuseReport.java | NO | No class-level documentation of any kind |
| 9 | ExcelDriverImpactReport.java | NO | No class-level documentation of any kind |
| 10 | ExcelDriverLicenceExpiry.java | NO | No class-level documentation of any kind |
| 11 | ExcelDynDriverReport.java | NO | No class-level documentation of any kind |
| 12 | ExcelDynSeenReport.java | NO | No class-level documentation of any kind |
| 13 | ExcelDynTransportDriverReport.java | NO | No class-level documentation of any kind |
| 14 | ExcelDynUnitReport.java | NO | No class-level documentation of any kind |
| 15 | ExcelExceptionSessionReport.java | NO | No class-level documentation of any kind |
| 16 | ExcelHireDehireReport.java | NO | No class-level documentation of any kind |
| 17 | ExcelImpactMeterReport.java | NO | No class-level documentation of any kind |
| 18 | ExcelImpactReport.java | NO | No class-level documentation of any kind |

**Result: 0 / 18 classes have any Javadoc.**

---

## 3. Method-Level Javadoc

No method in any of the 18 files has any Javadoc comment (/** ... */) whatsoever. The only inline comments found are short operational remarks such as `//adjust first column width: sheet.autoSizeColumn(0);` (present in most files), `// Set the 'hide' option as '1'.`, `// Tokenizing the string to get the elements of the do_list stack.`, and end-of-block markers like `// end method createDynReport`.

**Result: 0 methods across all 18 files have Javadoc.**

---

## 4. Undocumented Public Methods (per file)

Every public method listed below lacks Javadoc entirely.

### 4.1 ExcelBatteryReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelBatteryReport(String docRoot, String fileName, BatteryReportBean bean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createBatteryReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.2 ExcelBroadcastMsgReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelBroadcastMsgReport(String docRoot, String fileName, ArrayList<BroadcastmsgBean> arrBroadCastMsgBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createUnitUnlockReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.3 ExcelCimplicityShockReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelCimplicityShockReport(String docRoot, String fileName, CimplicityShockReportBean cimpBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createCimplicityShockReport(String cust, String loc, String dep, String from, String to)` | NO |
| `String getFileName()` | NO |

### 4.4 ExcelCimplicityUtilReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelCimplicityUtilReport(String docRoot, String fileName, CimplicityUtilReportBean cimpBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createCimplicityUtilReport(String cust, String loc, String dep, String from, String to)` | NO |
| `String getFileName()` | NO |

### 4.5 ExcelCurrDrivReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelCurrDrivReport(String docRoot, String fileName, CurrDrivReportBean currBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createCurrDrivReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.6 ExcelCurrUnitReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelCurrUnitReport(String docRoot, String fileName, CurrUnitReportBean currBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createCurrUnitReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.7 ExcelDailyVehSummaryReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDailyVehSummaryReport(String docRoot, String fileName, DailyVehSummaryReportBean dsumBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createDSumReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.8 ExcelDriverAccessAbuseReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDriverAccessAbuseReport(String docRoot, String fileName, DriverAccessAbuseBean abuseBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createDriverAccessAbuseReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.9 ExcelDriverImpactReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDriverImpactReport(String docRoot, String fileName, DriverImpactReportBean dImpactBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et, String model)` | NO |
| `void createDrivImpReport(String cust, String loc, String dep, String st, String et, String model)` | NO |
| `String getFileName()` | NO |

### 4.10 ExcelDriverLicenceExpiry.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDriverLicenceExpiry(String docRoot, String fileName, DriverLicenceExpiryBean bean)` | NO |
| `String createExcel(String cust_cd, String loc_cd, String dept_cd)` | NO |
| `void createLicenceExpiryReport(String cust_cd, String loc_cd, String dept_cd)` | NO |
| `String getFileName()` | NO |

### 4.11 ExcelDynDriverReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDynDriverReport(String docRoot, String fileName, DynDriverReportBean dynBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.12 ExcelDynSeenReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDynSeenReport(String docRoot, String fileName, DynSeenReportBean dynBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.13 ExcelDynTransportDriverReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDynTransportDriverReport(String docRoot, String fileName, DynDriverReportBean dynBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.14 ExcelDynUnitReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelDynUnitReport(String docRoot, String fileName, DynUnitReportBean dynBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createDynUnitReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.15 ExcelExceptionSessionReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelExceptionSessionReport(String docRoot, String fileName, DynUnitReportBean dynBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `void createExceptionSessionReport(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

### 4.16 ExcelHireDehireReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelHireDehireReport(String docRoot, String fileName, HireDehireReportBean hireDehireBean)` | NO |
| `String createExcel(String st, String et, String sc)` | NO |
| `void createHireDehireReport(String st, String et, String search_crit)` | NO |
| `String getFileName()` | NO |

### 4.17 ExcelImpactMeterReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelImpactMeterReport(String docRoot, String fileName, ImpactReportBean impBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

Note: `createImpactReport(...)` is private, not public.

### 4.18 ExcelImpactReport.java
| Method Signature | Javadoc |
|------------------|:-------:|
| `ExcelImpactReport(String docRoot, String fileName, ImpactReportBean impBean)` | NO |
| `String createExcel(String cust, String loc, String dep, String st, String et)` | NO |
| `String getFileName()` | NO |

Note: `createImpactReport(...)` is private, not public.

---

## 5. Documentation Accuracy Check

Since there is no documentation to evaluate for accuracy, this section documents naming/semantic inconsistencies that would be confusing to maintainers in the absence of documentation:

| # | File | Observation |
|---|------|-------------|
| 1 | ExcelBroadcastMsgReport.java | Internal report-building method is named `createUnitUnlockReport` (line 42), but the class and report title are "Broadcast Message Report". Method name is misleading -- likely copy-paste residue. |
| 2 | ExcelDynDriverReport.java | Report-building method is named `createDynUnitReport` (line 46), but the class represents a "Detailed Report by Driver". Name suggests a unit-based report. |
| 3 | ExcelDynSeenReport.java | Report-building method is named `createDynUnitReport` (line 46), but the class represents a "Pedestrian Detection Report". Name is misleading. |
| 4 | ExcelDynTransportDriverReport.java | Report-building method is named `createDynUnitReport` (line 41), but the class represents a "Detailed Report by Transport Driver". Name is misleading. |
| 5 | ExcelDriverLicenceExpiry.java | Tab title string contains a typo: `"Driver LIcence Expiry Report"` (line 53) -- uppercase 'I' in "LIcence". |
| 6 | ExcelCimplicityShockReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 54) but never uses it -- dead code. |
| 7 | ExcelCimplicityUtilReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 62) but never uses it -- dead code. |
| 8 | ExcelCurrDrivReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 61) but never uses it -- dead code. |
| 9 | ExcelCurrUnitReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 62) but never uses it -- dead code. |
| 10 | ExcelDailyVehSummaryReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 93) but never uses it -- dead code. |
| 11 | ExcelDynDriverReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 107) but never uses it -- dead code. |
| 12 | ExcelDynSeenReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 99) but never uses it -- dead code. |
| 13 | ExcelImpactMeterReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 77) but never uses it -- dead code. |
| 14 | ExcelImpactReport.java | Instantiates `UnitDAO unitDAO = new UnitDAO()` (line 79) but never uses it -- dead code. |
| 15 | ExcelImpactReport.java | Line 221 contains misspelling `"longtitue"` -- should be `"longitude"`. |

---

## 6. TODO / FIXME / HACK / XXX Markers

| # | File | Line | Marker | Text |
|---|------|-----:|--------|------|
| 1 | ExcelImpactReport.java | 234 | TODO | `// TODO Auto-generated catch block` -- JSONException is caught and only `e.printStackTrace()` is called. No logging or re-throw. |

**Total markers found: 1**

---

## 7. Inline Comment Inventory

Beyond the TODO above, the only recurring inline comments across files are:

- `//adjust first column width: sheet.autoSizeColumn(0);` -- appears in 16 of 18 files. This is a commented-out code line, not a documentation comment. It serves no explanatory purpose and constitutes dead commented-out code.
- `// Tokenizing the string to get the elements of the do_list stack.` -- appears in ExcelDynDriverReport, ExcelDynSeenReport, ExcelDynTransportDriverReport, ExcelDynUnitReport, ExcelExceptionSessionReport.
- `// Set the 'hide' option as '1'.` -- same files as above.
- `//deal with do_list here.` -- same files as above.
- End-of-block markers: `// end method createDynReport`, `//end for loop vdriv_cd`, `//end for loop details`, `//end for loop per vehicle model`, `//end loop total`, `//end loop grand total` -- present in ExcelDynDriverReport, ExcelDynSeenReport, ExcelDynTransportDriverReport, ExcelDynUnitReport, ExcelExceptionSessionReport.

---

## 8. Summary Statistics

| Metric | Count |
|--------|------:|
| Files audited | 18 |
| Total lines of code | 3,543 |
| Classes with Javadoc | 0 / 18 (0%) |
| Public methods total | 69 |
| Public methods with Javadoc | 0 / 69 (0%) |
| Method-name accuracy issues | 4 (misleading names from copy-paste) |
| Dead code instances (unused DAO) | 9 |
| TODO/FIXME/HACK/XXX markers | 1 |
| String typos found | 2 ("LIcence", "longtitue") |
| Commented-out code patterns | 1 pattern across 16 files |

---

## 9. Findings by Severity

### Critical
- None.

### High
- **H-1:** Zero documentation across all 18 files. No class Javadoc, no method Javadoc, no @param/@return/@throws on any of the 69 public methods. This represents a complete absence of API documentation for the Excel report generation layer.

### Medium
- **M-1:** Four classes have misleadingly named public methods (ExcelBroadcastMsgReport.createUnitUnlockReport, ExcelDynDriverReport.createDynUnitReport, ExcelDynSeenReport.createDynUnitReport, ExcelDynTransportDriverReport.createDynUnitReport). Without documentation, the only way to understand what these methods actually do is to read through their full implementation.
- **M-2:** Nine files instantiate `UnitDAO` objects that are never referenced, adding unnecessary resource allocation without any comment explaining why.
- **M-3:** Single TODO marker in ExcelImpactReport.java (line 234) with bare `e.printStackTrace()` -- the auto-generated catch block was never properly implemented with logging or error handling.

### Low
- **L-1:** Typo in ExcelDriverLicenceExpiry.java tab title: `"Driver LIcence Expiry Report"` (line 53).
- **L-2:** Typo in ExcelImpactReport.java: `"longtitue"` should be `"longitude"` (line 221).
- **L-3:** Commented-out code `//adjust first column width: sheet.autoSizeColumn(0);` appears in 16 of 18 files as stale dead code.

---

*End of Pass 3 documentation audit for excel/reports A-I.*
