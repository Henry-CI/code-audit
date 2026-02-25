# Pass 3 -- Documentation Audit: `dashboard` Package

**Audit ID:** 2026-02-25-01-P3-dashboard
**Auditor:** A08
**Date:** 2026-02-25
**Package:** `com.torrent.surat.fms6.dashboard`
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/`
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## Summary

| Metric | Count |
|---|---|
| Files audited | 9 |
| Total findings | 36 |
| HIGH | 1 |
| MEDIUM | 27 |
| LOW | 6 |
| INFO | 2 |

The dashboard package has **virtually no Javadoc documentation** across all 9 files. None of the 6 servlet classes have class-level Javadoc describing purpose, servlet mapping, request parameters, or response format. There are zero `@param`, `@return`, or `@throws` tags in the entire package. The only Javadoc-style comment in the entire package is a minimal class-level comment on `SessionCleanupListener` (one sentence, no tags). Every public method across all files lacks documentation.

---

## File-by-File Analysis

---

### 1. Config.java (218 lines)

**Reading evidence:** Utility/helper class (not a servlet). Contains static fields `siteHours`, `cusList`, `gson`. Public static methods: `getCustomers()`, `getSites()`, `getDepartments()`, `saveasList()`, `getPermision()`, `addSeries()` (two overloads). No class-level or method-level Javadoc anywhere.

**Class role:** Shared configuration and utility methods used by all dashboard servlets. Provides customer/site/department lookup, SQL query execution, and chart series building.

| # | Severity | Location | Finding |
|---|---|---|---|
| 1 | MEDIUM | Class level | No class-level Javadoc. Class serves as a shared utility for dashboard servlets -- its role, thread-safety implications of static `cusList`, and relationship to servlets are entirely undocumented. |
| 2 | MEDIUM | `getCustomers(HttpServletRequest, HttpServletResponse)` | Public method undocumented. No Javadoc, no `@param`, no `@return`, no `@throws`. This is business logic that queries customer master data filtered by user access level, writes JSON to response. Request parameters: `cust_cd`, `loc_cd`, `dept_cd`; reads session attributes `user_cd`, `access_level`. |
| 3 | MEDIUM | `getSites(HttpServletRequest, HttpServletResponse)` | Public method undocumented. Filters cached `cusList` by `cust_cd` parameter, returns JSON list of sites. |
| 4 | MEDIUM | `getDepartments(HttpServletRequest, HttpServletResponse)` | Public method undocumented. Filters cached `cusList` by `loc_cd` parameter, returns JSON list of departments. |
| 5 | MEDIUM | `saveasList(String)` | Public method undocumented. Core database utility that executes arbitrary SQL and returns results as `LinkedList<HashMap<String, String>>`. No documentation on expected query format, JNDI lookup, or error handling. |
| 6 | MEDIUM | `getPermision(HttpServletRequest, HttpServletResponse)` | Public method undocumented. Queries form permissions for current user session. Response format is JSON array of form names. |
| 7 | LOW | `addSeries(List, String, List)` | Public utility method undocumented. Two overloads (with/without color parameter) for building chart series data structures. |
| 8 | LOW | `addSeries(List, String, String, List)` | Public utility method undocumented. Overload of above with color parameter. |

---

### 2. CriticalBattery.java (351 lines)

**Reading evidence:** Servlet class annotated `@WebServlet("/Servlet/CriticalBatteryServlet")`. Extends `HttpServlet`. Overrides `doGet()`. Uses `ConcurrentHashMap` for session-specific data. Private methods: `getDates()`, `getTable()`, `updateTable()`, `mapValue()`, `mapKey()`. Public static: `cleanupSession()`. No class-level or method-level Javadoc.

**Servlet mapping:** `/Servlet/CriticalBatteryServlet` (annotation-based)
**HTTP method:** GET only
**Request parameter `part`:** `dates`, `table`, `update`, `cust`, `site`, `dept`, `permision`
**Response format:** `application/json` (UTF-8)

| # | Severity | Location | Finding |
|---|---|---|---|
| 9 | MEDIUM | Class level | No class-level Javadoc. This is a servlet handling critical battery level data for the dashboard. Servlet URL, purpose, parameter contract, and response format are undocumented. |
| 10 | MEDIUM | `doGet()` | No Javadoc. Dispatches on `part` parameter to multiple sub-handlers. No documentation of valid `part` values or the overall request/response contract. |
| 11 | MEDIUM | `cleanupSession(String)` | Public static method undocumented. Called by `SessionCleanupListener` to prevent memory leaks by clearing session-specific `ConcurrentHashMap` entries. |

Additional `part=dates` parameters: `mode` (hour/date), `start_time`, `end_time`, `cust_cd`, `loc_cd`, `dept_cd` -- all undocumented.

---

### 3. Impacts.java (469 lines)

**Reading evidence:** Servlet class annotated `@WebServlet("/Servlet/ImpactsServlet")`. Extends `HttpServlet`. Has empty Javadoc block on `serialVersionUID` field (lines 38-40: `/** * */`). Overrides `doGet()`. Uses `ConcurrentHashMap` for session-specific data. Private methods: `getDates()`, `getTable()`, `updateTable()`, `getPie()`, `getAverage()`, `saveasList()`, `mapValue()`, `mapKey()`, `addSeries()`. Public static: `cleanupSession()`. No meaningful Javadoc.

**Servlet mapping:** `/Servlet/ImpactsServlet` (annotation-based)
**HTTP method:** GET only
**Request parameter `part`:** `dates`, `table`, `update`, `cust`, `site`, `dept`, `pie`, `average`, `permision`
**Response format:** `application/json` (UTF-8)

| # | Severity | Location | Finding |
|---|---|---|---|
| 12 | MEDIUM | Class level | No meaningful class-level Javadoc. The empty `/** * */` block (lines 38-40) is on the `serialVersionUID` field, not the class. Servlet purpose (impact/shock data dashboard), URL mapping, and parameter contract are undocumented. |
| 13 | MEDIUM | `doGet()` | No Javadoc. Dispatches on `part` parameter. Supports 9 different `part` values including `pie` and `average` which are unique to this servlet. None documented. |
| 14 | MEDIUM | `cleanupSession(String)` | Public static method undocumented. |

Additional `part=dates` parameters: `mode`, `start_time`, `end_time`, `cust_cd`, `loc_cd`, `dept_cd` -- all undocumented.

---

### 4. Licence.java (315 lines)

**Reading evidence:** Servlet class annotated `@WebServlet("/Servlet/LicenceServlet")`. Extends `HttpServlet`. Overrides `init()` and `doGet()`. Uses `ConcurrentHashMap` for session-specific data. Private methods: `getChart()`, `updateTable()`, `getTable()`, `saveasList()`. Public static: `cleanupSession()`. No Javadoc.

**Servlet mapping:** `/Servlet/LicenceServlet` (annotation-based)
**HTTP method:** GET only
**Request parameter `part`:** `chart`, `table`, `update`
**Response format:** `application/json` (UTF-8)

| # | Severity | Location | Finding |
|---|---|---|---|
| 15 | MEDIUM | Class level | No class-level Javadoc. Servlet manages driver licence expiry dashboard data. Supports AU-specific logic via `LindeConfig.siteName` branching. No documentation of URL, parameters, or AU vs non-AU behavior. |
| 16 | MEDIUM | `init()` | Overridden servlet lifecycle method undocumented. Loads customer-department-location data into `cusList` at startup. |
| 17 | MEDIUM | `doGet()` | No Javadoc. Dispatches on `part` parameter with 3 possible values. |
| 18 | MEDIUM | `cleanupSession(String)` | Public static method undocumented. |

Additional `part=chart` parameters: `cust_cd`, `loc_cd`, `dept_cd`. `part=update` parameters: `category`, `cust_cd`, `loc_cd`, `dept_cd` -- all undocumented.

---

### 5. Preop.java (347 lines)

**Reading evidence:** Servlet class annotated `@WebServlet("/Servlet/PreopServlet")`. Extends `HttpServlet`. Overrides `doGet()`. Uses `ConcurrentHashMap` for session-specific data. Private methods: `getDates()`, `getTable()`, `updateTable()`, `mapValue()`, `mapKey()`. Public static: `cleanupSession()`. No Javadoc.

**Servlet mapping:** `/Servlet/PreopServlet` (annotation-based)
**HTTP method:** GET only
**Request parameter `part`:** `dates`, `table`, `update`, `cust`, `site`, `dept`, `permision`
**Response format:** `application/json` (UTF-8)

| # | Severity | Location | Finding |
|---|---|---|---|
| 19 | MEDIUM | Class level | No class-level Javadoc. Servlet handles pre-operation check data (checklists, pass/fail/incomplete). No documentation of purpose, URL, or parameter contract. |
| 20 | MEDIUM | `doGet()` | No Javadoc. Dispatches on `part` parameter with 7 possible values. |
| 21 | MEDIUM | `cleanupSession(String)` | Public static method undocumented. |

Additional `part=dates` parameters: `mode`, `start_time`, `end_time`, `cust_cd`, `loc_cd`, `dept_cd` -- all undocumented.

---

### 6. SessionCleanupListener.java (30 lines)

**Reading evidence:** Annotated `@WebListener`. Implements `HttpSessionListener`. Has class-level Javadoc: `"Session listener to clean up session-specific resources"`. Two methods: `sessionCreated()` (no-op) and `sessionDestroyed()` (calls cleanup on Impacts only). Import of `com.torrent.surat.fms6.dashboard.*` is present.

| # | Severity | Location | Finding |
|---|---|---|---|
| 22 | LOW | Class-level Javadoc | Has a one-line class Javadoc (`"Session listener to clean up session-specific resources"`) -- the only Javadoc in the entire package. However, it lacks `@author`, and does not document which servlets it cleans up or the registration mechanism. |
| 23 | HIGH | `sessionDestroyed()` line 26 | **Misleading by omission.** The inline comment says `"Clean up session-specific resources"` and `"Add other cleanup calls for other servlets as needed"` (line 28), but the method body only calls `Impacts.cleanupSession(sessionId)`. It does **not** call cleanup for `CriticalBattery`, `Preop`, `Utilisation`, or `Licence` -- all of which have `cleanupSession()` static methods and use `ConcurrentHashMap` session storage. The comment implies this is extensible/complete, but the implementation is incomplete. This is misleading documentation that could mask a memory leak. |
| 24 | LOW | `sessionCreated()` | Minor: inline comment says `"Nothing needed here"` which is adequate for a no-op. |

---

### 7. Summary.java (767 lines)

**Reading evidence:** Servlet class annotated `@WebServlet("/Servlet/SummaryServlet")`. Extends `HttpServlet`. Overrides `doGet()`. The largest file in the package. Private methods: `getBattery()`, `getPreop()`, `getImpactChart()`, `getUtilisation()`, `getLicence()`, `getImpact()`, `getUnit()`, `getDriver()`. No Javadoc anywhere.

**Servlet mapping:** `/Servlet/SummaryServlet` (annotation-based)
**HTTP method:** GET only
**Request parameter `part`:** `cust`, `site`, `dept`, `driver`, `unit`, `impact`, `licence`, `utilisation`, `impact_chart`, `preop`, `battery`
**Response format:** `application/json` (UTF-8)

| # | Severity | Location | Finding |
|---|---|---|---|
| 25 | MEDIUM | Class level | No class-level Javadoc. This is the main summary/overview dashboard servlet with 11 `part` values, the most complex dispatch in the package. No documentation of purpose, URL, or which sub-views it aggregates. |
| 26 | MEDIUM | `doGet()` | No Javadoc. Complex dispatch with 11 cases covering drivers, units, impacts, licences, utilisation, preop, and battery. None documented. |
| 27 | MEDIUM | `getBattery()` | Private but complex business logic method. Queries voltage data over 12 hourly intervals. Request parameters: `cust_cd`, `loc_cd`, `dept_cd`, `to_dt`. Response: JSON with `categories` and `series`. Undocumented. |
| 28 | MEDIUM | `getImpact()` | Private but complex business logic. Runs 4 separate queries for red impacts (today, yesterday, 7-day, 28-day). Undocumented. |
| 29 | MEDIUM | `getUnit()` | Private but complex method. Queries units, inactive-72h, active, VOR, abuse counts. Has `realtime` parameter branching. Undocumented. |
| 30 | MEDIUM | `getDriver()` | Private but complex method. Queries driver counts, expired licences, no-licence, inactive drivers. Has AU-specific branching. Undocumented. |
| 31 | INFO | Line 633 | **TODO marker:** `//to-do: only for demo` -- the associated code sets `abuse` to `"0"` in both branches of a conditional, suggesting this is placeholder/demo code that was never finished. |

---

### 8. TableServlet.java (640 lines)

**Reading evidence:** Servlet class annotated `@WebServlet("/Servlet/TableServlet")`. Extends `HttpServlet`. Overrides `doGet()`. Instance field `servlet` is set to `"/Servlet/UtilisationServlet"` (line 38) which is incorrect -- this is TableServlet, not UtilisationServlet. Private methods: `getVORStatus()`, `getPreop()`, `getDetailDriver()`, `getDetailUnit()`. Public static: `saveasList(String, String)`. No Javadoc.

**Servlet mapping:** `/Servlet/TableServlet` (annotation-based)
**HTTP method:** GET only
**Request parameter `part`:** `detail_unit`, `detail_driver`, `preop`, `vor_status`, `cust`, `site`, `dept`
**Response format:** `application/json` (UTF-8)

| # | Severity | Location | Finding |
|---|---|---|---|
| 32 | MEDIUM | Class level | No class-level Javadoc. Servlet provides detailed table data for units, drivers, preop checklists, and VOR status. No documentation of purpose, URL, parameters, or response format. |
| 33 | MEDIUM | `doGet()` | No Javadoc. Dispatches on `part` parameter with 7 possible values. |
| 34 | MEDIUM | `saveasList(String, String)` | Public static method undocumented. Similar to `Config.saveasList()` but takes a `servlet` name parameter for error logging. No `@param` or `@return` tags. |
| 35 | INFO | Line 38 | Instance field `servlet = "/Servlet/UtilisationServlet"` appears to be a copy-paste artifact. The actual servlet is `/Servlet/TableServlet`. While not strictly a documentation issue, it causes misleading error log messages. |

---

### 9. Utilisation.java (996 lines)

**Reading evidence:** Servlet class annotated `@WebServlet("/Servlet/UtilisationServlet")`. Extends `HttpServlet`. The second-largest file in the package. Overrides `doGet()`. Uses `ConcurrentHashMap` for session-specific data. Instance fields include `thresholdLow=25`, `thresholdHigh=50`, `oneDay` flag. Private methods: `procedure()`, `getDateData()`, `getModelData()`, `getSiteData()`, `updateModelChart()`, `updateSiteChart()`, `updateDateChart()`, `getTable()`, `updateTable()`, `updateDateTable()`, `getPie()`, `getModelAverage()`, `getSiteAverage()`, `getDateAverage()`, `saveasList()`, `mapValue()`, `mapKey()`, `addSeries()`. Public static: `cleanupSession()`. No Javadoc.

**Servlet mapping:** `/Servlet/UtilisationServlet` (annotation-based)
**HTTP method:** GET only
**Request parameter `part`:** `model`, `date`, `location`, `table`, `tb_model`, `tb_date`, `tb_location`, `ct_model`, `ct_date`, `ct_location`, `cust`, `site`, `dept`, `pie`, `av_model`, `av_date`, `av_site`, `permision`
**Response format:** `application/json` (UTF-8)

| # | Severity | Location | Finding |
|---|---|---|---|
| 36 | MEDIUM | Class level | No class-level Javadoc. Most complex servlet in the package with 18 `part` values covering model/date/location views, tables, charts, pie, and averages. The entire parameter contract, threshold logic (`thresholdLow`/`thresholdHigh`), and the meaning of the three utilisation bands (Low/Middle/High) are undocumented. |
| 37 | LOW | `cleanupSession(String)` | Public static method undocumented. Same pattern as other servlets. |
| 38 | LOW | `serialVersionUID` visibility | Field is `static final` but package-private (not `private`). Minor documentation/style note. |

---

## Cross-Cutting Findings

### Servlet Mapping Summary

All servlet mappings use `@WebServlet` annotations (no web.xml entries found for this package):

| Servlet Class | URL Pattern | `part` Values |
|---|---|---|
| CriticalBattery | `/Servlet/CriticalBatteryServlet` | dates, table, update, cust, site, dept, permision |
| Impacts | `/Servlet/ImpactsServlet` | dates, table, update, cust, site, dept, pie, average, permision |
| Licence | `/Servlet/LicenceServlet` | chart, table, update |
| Preop | `/Servlet/PreopServlet` | dates, table, update, cust, site, dept, permision |
| Summary | `/Servlet/SummaryServlet` | cust, site, dept, driver, unit, impact, licence, utilisation, impact_chart, preop, battery |
| TableServlet | `/Servlet/TableServlet` | detail_unit, detail_driver, preop, vor_status, cust, site, dept |
| Utilisation | `/Servlet/UtilisationServlet` | model, date, location, table, tb_model, tb_date, tb_location, ct_model, ct_date, ct_location, cust, site, dept, pie, av_model, av_date, av_site, permision |

### Common Undocumented Request Parameters

These parameters are used across multiple servlets but never documented:
- `cust_cd` -- customer code
- `loc_cd` -- location/site code
- `dept_cd` -- department code
- `start_time` / `st_dt` -- start date/time (format: `dd/MM/yyyy HH:mm`)
- `end_time` / `to_dt` -- end date/time (format: `dd/MM/yyyy HH:mm`)
- `mode` -- `"hour"` or date aggregation mode
- `category` -- chart category for drill-down
- `series` -- chart series for drill-down
- `realtime` -- `"1"` for live data, else historical
- `search_crit` -- text search filter
- `high` / `low` -- utilisation threshold percentages

### TODO/FIXME/HACK/XXX Markers

| File | Line | Marker | Content |
|---|---|---|---|
| Summary.java | 633 | `//to-do` | `//to-do: only for demo` -- Placeholder code that sets `abuse` to `"0"` regardless of condition. Never implemented. |

### Documentation Statistics

| Metric | Value |
|---|---|
| Total public methods (all files) | 14 |
| Public methods with Javadoc | 0 |
| Public methods with `@param` | 0 |
| Public methods with `@return` | 0 |
| Public methods with `@throws` | 0 |
| Classes with Javadoc | 1 (SessionCleanupListener, minimal) |
| Classes without Javadoc | 8 |
| Servlet classes without Javadoc | 6 (all) |
| Inline comments (code-level) | Sparse; mostly session-related cleanup comments added during concurrency refactoring |

---

## Findings Index (sorted by severity)

| # | Severity | File | Summary |
|---|---|---|---|
| 23 | HIGH | SessionCleanupListener.java | Misleading: only cleans up Impacts session data; CriticalBattery, Preop, Utilisation, Licence cleanup methods exist but are never called |
| 1 | MEDIUM | Config.java | No class-level Javadoc |
| 2 | MEDIUM | Config.java | `getCustomers()` undocumented |
| 3 | MEDIUM | Config.java | `getSites()` undocumented |
| 4 | MEDIUM | Config.java | `getDepartments()` undocumented |
| 5 | MEDIUM | Config.java | `saveasList()` undocumented |
| 6 | MEDIUM | Config.java | `getPermision()` undocumented |
| 9 | MEDIUM | CriticalBattery.java | No class/servlet Javadoc |
| 10 | MEDIUM | CriticalBattery.java | `doGet()` undocumented |
| 11 | MEDIUM | CriticalBattery.java | `cleanupSession()` undocumented |
| 12 | MEDIUM | Impacts.java | No class/servlet Javadoc |
| 13 | MEDIUM | Impacts.java | `doGet()` undocumented |
| 14 | MEDIUM | Impacts.java | `cleanupSession()` undocumented |
| 15 | MEDIUM | Licence.java | No class/servlet Javadoc |
| 16 | MEDIUM | Licence.java | `init()` undocumented |
| 17 | MEDIUM | Licence.java | `doGet()` undocumented |
| 18 | MEDIUM | Licence.java | `cleanupSession()` undocumented |
| 19 | MEDIUM | Preop.java | No class/servlet Javadoc |
| 20 | MEDIUM | Preop.java | `doGet()` undocumented |
| 21 | MEDIUM | Preop.java | `cleanupSession()` undocumented |
| 25 | MEDIUM | Summary.java | No class/servlet Javadoc |
| 26 | MEDIUM | Summary.java | `doGet()` undocumented (11 dispatch cases) |
| 27 | MEDIUM | Summary.java | `getBattery()` complex business logic undocumented |
| 28 | MEDIUM | Summary.java | `getImpact()` complex business logic undocumented |
| 29 | MEDIUM | Summary.java | `getUnit()` complex business logic undocumented |
| 30 | MEDIUM | Summary.java | `getDriver()` complex business logic undocumented |
| 32 | MEDIUM | TableServlet.java | No class/servlet Javadoc |
| 33 | MEDIUM | TableServlet.java | `doGet()` undocumented |
| 34 | MEDIUM | TableServlet.java | `saveasList(String, String)` undocumented |
| 36 | MEDIUM | Utilisation.java | No class/servlet Javadoc (18 dispatch cases) |
| 7 | LOW | Config.java | `addSeries()` (2-param overload) undocumented |
| 8 | LOW | Config.java | `addSeries()` (3-param overload) undocumented |
| 22 | LOW | SessionCleanupListener.java | Minimal class Javadoc, missing `@author` and servlet inventory |
| 24 | LOW | SessionCleanupListener.java | `sessionCreated()` trivial, minor |
| 37 | LOW | Utilisation.java | `cleanupSession()` undocumented |
| 38 | LOW | Utilisation.java | `serialVersionUID` package-private visibility |
| 31 | INFO | Summary.java | TODO marker: `//to-do: only for demo` (line 633) |
| 35 | INFO | TableServlet.java | Misleading `servlet` field value `/Servlet/UtilisationServlet` (copy-paste artifact) |

---

*End of Pass 3 Documentation Audit for `dashboard` package.*
*Auditor: A08 | Generated: 2026-02-25*
