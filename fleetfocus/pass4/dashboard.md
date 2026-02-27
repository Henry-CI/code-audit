# Pass 4 -- Code Quality Audit: `dashboard` Package

**Audit Agent:** A08
**Date:** 2026-02-25
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Package:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/`

---

## Files Audited (9)

| # | File | Lines | Read in Full |
|---|------|------:|:------------:|
| 1 | Config.java | 219 | Yes |
| 2 | CriticalBattery.java | 351 | Yes |
| 3 | Impacts.java | 469 | Yes |
| 4 | Licence.java | 315 | Yes |
| 5 | Preop.java | 347 | Yes |
| 6 | SessionCleanupListener.java | 30 | Yes |
| 7 | Summary.java | 768 | Yes |
| 8 | TableServlet.java | 641 | Yes |
| 9 | Utilisation.java | 997 | Yes |

---

## 1. Style Consistency

| ID | File | Line(s) | Finding |
|----|------|---------|---------|
| STY-01 | Config.java | throughout | Mixed indentation -- tabs and spaces are interleaved inconsistently (e.g., line 29 uses spaces, line 30 uses tab). This pattern is inconsistent with the rest of the package, which predominantly uses spaces with 4-space indentation. |
| STY-02 | Summary.java | throughout | Uses tab indentation throughout, whereas CriticalBattery, Impacts, Preop, and Utilisation use 4-space indentation. |
| STY-03 | TableServlet.java | throughout | Uses tab indentation, inconsistent with the space-indented servlets. |
| STY-04 | Multiple files | -- | Closing brace placement is inconsistent: `getCustomers()` in Config.java (line 70) has the closing brace indented at a different level than other methods. |
| STY-05 | Licence.java | 97 | Double semicolons: `driversQuery += " and \"LOC_CD\" = " + site;;` |
| STY-06 | Licence.java | 195, 233, 234 | Unnecessary semicolons after closing braces of for-each loops (`;` after `}`). |
| STY-07 | Summary.java | 639 | Unnecessary semicolon after closing brace: `};` at line 639. |
| STY-08 | Config.java | 153 | Typo in method name: `getPermision` (should be `getPermission`). This typo propagates to all callers in every servlet. |
| STY-09 | Preop.java | 123 | Typo in SQL literal: `'incompelte'` should be `'incomplete'`. |

---

## 2. God Classes

| ID | File | Line Count | Method Count | Finding |
|----|------|-----------|-------------|---------|
| GOD-01 | Summary.java | 768 | 10 methods | This class handles 10 distinct endpoint operations (driver, unit, impact, licence, utilisation, impact_chart, preop, battery, plus cust/site/dept delegation). Each method independently opens DB connections, builds SQL, and serializes JSON. Strong candidate for decomposition. |
| GOD-02 | Utilisation.java | 997 | 19 methods | The largest file in the package. Handles model, date, site chart data plus table views, pie charts, and averages. Significant duplication of chart-building logic across `getModelData`, `getSiteData`, `updateModelChart`, `updateSiteChart`, and `updateDateChart`. |
| GOD-03 | TableServlet.java | 641 | 6 methods | `getDetailUnit` (150 lines) and `getDetailDriver` (165 lines) are excessively long methods with duplicated logic for building dynamic column queries. |

---

## 3. Servlet Architecture -- Thread Safety of Instance Variables

| ID | File | Line(s) | Field | Severity | Finding |
|----|------|---------|-------|----------|---------|
| TS-01 | Config.java | 28 | `siteHours` | HIGH | `public static float siteHours = 24` -- mutable static field shared across all requests. If any code path modifies this, it creates a race condition. |
| TS-02 | Config.java | 29 | `cusList` | CRITICAL | `static LinkedList<HashMap<String, String>> cusList` -- shared mutable static collection written in `getCustomers()` (line 59) and read in `getSites()` / `getDepartments()`. Concurrent requests will corrupt this list. No synchronization. |
| TS-03 | Config.java | 30 | `gson` | LOW | `static Gson gson` -- Gson instances are thread-safe, but declaring it static non-final is unconventional. |
| TS-04 | CriticalBattery.java | 45 | `cusList` | HIGH | Non-static instance variable `LinkedList<HashMap<String, String>> cusList` on a servlet (single instance shared across threads). Written and read without synchronization. |
| TS-05 | CriticalBattery.java | 47 | `servlet` | MEDIUM | Instance-level `String servlet` field -- immutable value but should be `private static final`. |
| TS-06 | CriticalBattery.java | 48 | `gson` | LOW | Instance-level Gson -- safe but should be `private static final`. |
| TS-07 | Impacts.java | 48 | `cusList` | HIGH | Same pattern as TS-04. Instance-level mutable list on a shared servlet instance. |
| TS-08 | Impacts.java | 50-51 | `servlet`, `gson` | MEDIUM | Instance-level fields that should be constants. |
| TS-09 | Licence.java | 42 | `cusList` | HIGH | Mutable instance-level list on a shared servlet. Written in `init()` (line 53) and never updated again, but no `volatile` or synchronization to guarantee visibility to request-handling threads. |
| TS-10 | Licence.java | 44 | `gson` | LOW | Instance-level Gson. |
| TS-11 | Preop.java | 44 | `cusList` | HIGH | Mutable instance-level list on a shared servlet (unused -- never read after declaration). |
| TS-12 | Preop.java | 46-47 | `servlet`, `gson` | MEDIUM | Instance-level fields that should be constants. |
| TS-13 | Summary.java | 36 | `cusList` | HIGH | Instance-level mutable list on a shared servlet. |
| TS-14 | Summary.java | 37 | `gson` | LOW | Instance-level Gson. |
| TS-15 | TableServlet.java | 36-40 | `cusList`, `rsList`, `servlet`, `defaultCust`, `gson` | CRITICAL | Multiple mutable instance variables on a shared servlet. `rsList` is written in `getVORStatus()` (line 131-132), `getPreop()` (line 231-232), `getDetailDriver()` (line 397-398), and `getDetailUnit()` (line 548-549). Concurrent requests will corrupt results across users. |
| TS-16 | Utilisation.java | 48-52 | `cusList`, `vehicles`, `thresholdLow`, `thresholdHigh`, `oneDay` | CRITICAL | Multiple mutable instance variables on a shared servlet. `vehicles` is written in `procedure()` (line 146). `thresholdLow` and `thresholdHigh` are written in multiple methods. `oneDay` is written in `getDateData()` (line 210) and read in `updateDateChart()` / `updateDateTable()`. Concurrent requests from different users will corrupt each other's state. |
| TS-17 | Utilisation.java | 51 | `gson` | LOW | Instance-level Gson. |

---

## 4. Commented-Out Code

| ID | File | Line(s) | Finding |
|----|------|---------|---------|
| COM-01 | Summary.java | 274 | `// impactList.add(rs.getInt(3));` -- commented-out logic that alters result content. |
| COM-02 | Summary.java | 349 | `// System.out.println(query);` -- debug print left commented. |
| COM-03 | Summary.java | 605 | `// System.out.println(query);` -- debug print left commented. |
| COM-04 | Summary.java | 633-639 | `//to-do: only for demo` block with dead conditional code that always puts `"0"` for abuse regardless of the condition. |
| COM-05 | TableServlet.java | 230 | `// System.out.println(query);` -- debug print left commented. |
| COM-06 | TableServlet.java | 294 | Entire line commented out: `// String vehiclesQuery = ...` |
| COM-07 | TableServlet.java | 319-332 | 14 lines of commented-out date calculation and suffix logic. |
| COM-08 | TableServlet.java | 347 | `// System.out.println(query);` -- debug print left commented. |
| COM-09 | TableServlet.java | 396 | `// System.out.println(query);` -- debug print left commented. |
| COM-10 | TableServlet.java | 497 | `// System.out.println(query);` -- debug print left commented. |
| COM-11 | TableServlet.java | 547 | `// System.out.println(query);` -- debug print left commented. |

---

## 5. Unused Imports

| ID | File | Line(s) | Import |
|----|------|---------|--------|
| UI-01 | Config.java | 13 | `java.util.Map` -- used only in for-each loop parameter; however technically used. No truly unused imports in Config. |
| UI-02 | CriticalBattery.java | 11 | `java.util.Arrays` -- never referenced in the file. |
| UI-03 | SessionCleanupListener.java | 7 | `com.torrent.surat.fms6.dashboard.*` -- wildcard import of own package is redundant (classes are in the same package). |
| UI-04 | Summary.java | 11 | `java.util.Arrays` -- never referenced. |
| UI-05 | Summary.java | 12 | `java.util.Calendar` -- never referenced. |
| UI-06 | Summary.java | 13 | `java.util.Date` -- never referenced. |
| UI-07 | Summary.java | 8 | `java.text.SimpleDateFormat` -- never referenced. |
| UI-08 | TableServlet.java | 11 | `java.util.Arrays` -- used in `getDetailDriver` and `getDetailUnit` for `Arrays.asList()`, so actually used. Retracted. |
| UI-09 | Utilisation.java | 21 | `java.util.concurrent.TimeUnit` -- never referenced. |

---

## 6. Empty / Broad Catch Blocks

| ID | File | Line(s) | Finding |
|----|------|---------|---------|
| BC-01 | Config.java | 124 | `catch (Exception e)` -- broad catch in `saveasList()`. Catches all exceptions including unchecked ones (NPE, ClassCast, etc.) which masks bugs. |
| BC-02 | Config.java | 175 | `catch (Exception e)` -- broad catch in `getPermision()`. |
| BC-03 | CriticalBattery.java | 224 | `catch (Exception e)` -- broad catch in `getDates()`. |
| BC-04 | Impacts.java | 124 | `catch (Exception e)` -- broad catch in `getDates()` first try block. |
| BC-05 | Impacts.java | 412 | `catch (Exception e)` -- broad catch in `saveasList()`. |
| BC-06 | Licence.java | 146 | `catch (Exception e)` -- broad catch in `getChart()`. |
| BC-07 | Licence.java | 282 | `catch (Exception e)` -- broad catch in `saveasList()`. |
| BC-08 | Preop.java | 218 | `catch (Exception e)` -- broad catch in `getDates()`. |
| BC-09 | Summary.java | 137, 210, 283, 365, 450, 544, 644, 739 | Eight instances of `catch (Exception e)` -- every method in this class uses broad catch. |
| BC-10 | TableServlet.java | 145, 245, 412, 563, 611 | Five instances of `catch (Exception e)` across all methods. |
| BC-11 | Utilisation.java | 151, 939 | Two instances of `catch (Exception e)`. |

Total: **24 broad catch blocks** across the package. None of the catch blocks perform meaningful error recovery. All follow the same pattern of printing to stdout and the stack trace.

---

## 7. `e.printStackTrace()` Usage

| ID | File | Line(s) |
|----|------|---------|
| EPT-01 | Config.java | 126, 177 |
| EPT-02 | CriticalBattery.java | 119, 226 |
| EPT-03 | Impacts.java | 126, 156, 414 |
| EPT-04 | Licence.java | 148, 284 |
| EPT-05 | Preop.java | 118, 220 |
| EPT-06 | Summary.java | 139, 212, 285, 367, 452, 546, 646, 741 |
| EPT-07 | TableServlet.java | 147, 247, 414, 565, 613 |
| EPT-08 | Utilisation.java | 153, 207, 941 |

**Total: 26 instances** across the package. All write directly to `System.err` rather than using a logging framework. Additionally, many are paired with `System.out.println(e)` which duplicates the error output to `System.out`.

---

## 8. Shared Mutable State (Beyond Instance Variables)

| ID | File | Line(s) | Finding |
|----|------|---------|---------|
| SMS-01 | Config.java | 29 | `static cusList` is written by `getCustomers()` and read by `getSites()` and `getDepartments()`. These are called from different HTTP requests potentially on different threads. No synchronization. A request from User A calling `getCustomers()` will overwrite the list while User B is iterating it in `getSites()`. |
| SMS-02 | Config.java | 28 | `public static float siteHours = 24` is read by Utilisation.java (line 187-190). If anything writes to it, it is a cross-request race. |
| SMS-03 | CriticalBattery.java | 41-42 | `static final ConcurrentHashMap` for session data -- properly concurrent, but entries are never cleaned up if `SessionCleanupListener` does not call `CriticalBattery.cleanupSession()`. The listener only calls `Impacts.cleanupSession()` (SessionCleanupListener.java line 26). This is a **memory leak**. |
| SMS-04 | Preop.java | 40-41 | `static final ConcurrentHashMap` for session data -- never cleaned up by SessionCleanupListener. Memory leak. |
| SMS-05 | Licence.java | 39 | `static final ConcurrentHashMap` for session data -- never cleaned up by SessionCleanupListener. Memory leak. |
| SMS-06 | Utilisation.java | 45-46 | `static final ConcurrentHashMap` for session data -- never cleaned up by SessionCleanupListener. Memory leak. |
| SMS-07 | SessionCleanupListener.java | 21-28 | Only calls `Impacts.cleanupSession()`. Missing cleanup calls for CriticalBattery, Preop, Licence, and Utilisation, despite all four having `cleanupSession()` methods. Comment on line 28 says "Add other cleanup calls for other servlets as needed" -- they were never added. |

---

## 9. N+1 Query Patterns

| ID | File | Line(s) | Finding |
|----|------|---------|---------|
| NQ-01 | Summary.java | 508-539 (`getImpact`) | Four sequential SQL queries are executed to fetch impact counts for different time ranges (today, yesterday, last 7 days, last 28 days). These share the same base query structure and could be consolidated into a single query with conditional aggregation. |
| NQ-02 | Summary.java | 602-613 (`getUnit`) | Four sequential SQL queries are executed for unit counts (total, inactive72, active, vor). These are independent counts that could be consolidated. |
| NQ-03 | Summary.java | 690-734 (`getDriver`) | Four sequential SQL queries for driver statistics (total, expired, no_licence, not_active). Same consolidation opportunity. |
| NQ-04 | Summary.java | 115-129 (`getBattery`) | Loop executes 12 SQL queries (one per hour) inside a for-loop. Each query differs only by the hour offset. This is a classic N+1 -- could be a single query with `date_trunc` grouping. |
| NQ-05 | Summary.java | 344-360 (`getUtilisation`) | Loop executes 12 SQL queries (one per hour) inside a for-loop. Same pattern as NQ-04. |
| NQ-06 | CriticalBattery.java | 190 / Impacts.java | 218 / Preop.java | 173 | Nested iteration: for each entry in `dateList`, iterates entire `rsList` to find a match. This is O(n*m) in-memory join that could be replaced with a HashMap lookup or a single joined SQL query. |

---

## 10. String Equality (`==` vs `.equals()`)

| ID | File | Line | Finding |
|----|------|------|---------|
| SE-01 | Config.java | 42 | `cust == LindeConfig.customerLinde` -- uses `==` for String comparison. This compares object references, not values. Will only work if both reference the same interned String constant. Should be `.equals()`. |

---

## 11. Resource Management

| ID | File | Line(s) | Finding |
|----|------|---------|---------|
| RM-01 | All files | -- | All database access uses manual try/finally for Connection, Statement, and ResultSet cleanup. None use try-with-resources (Java 7+). While the finally blocks do close resources, they are verbose (20+ lines of boilerplate per method) and error-prone if a developer forgets one resource. |
| RM-02 | Config.java | 104-151 | `saveasList()` -- proper cleanup in finally block, but the method accepts arbitrary SQL strings, making it an open conduit for SQL injection if user input reaches it. |
| RM-03 | Summary.java | 265, 506, 600 | Several methods call `rs.close()` mid-method before executing a new query on the same `stmt` (e.g., line 265 and 506). If the subsequent `stmt.executeQuery()` throws, the `rs` reference in the finally block points to the new (failed) `rs`, and the previously closed one is fine -- but this pattern is fragile. |
| RM-04 | Config.java | 69 | `res.getWriter()` -- writer obtained but never flushed or closed. Same pattern in every servlet method that writes JSON. The container should handle this, but explicit flush is best practice. |
| RM-05 | Impacts.java | 392-439 | Duplicated `saveasList()` method -- Impacts has its own copy identical to Config's version. Code should reuse `Config.saveasList()`. |
| RM-06 | Licence.java | 262-309 | Duplicated `saveasList()` method -- another copy of the same logic. |
| RM-07 | Utilisation.java | 919-966 | Duplicated `saveasList()` method -- another copy. |
| RM-08 | TableServlet.java | 591-638 | Duplicated `saveasList()` (with extra `servlet` parameter for logging). |

---

## 12. SQL Injection

| ID | File | Line(s) | Finding |
|----|------|---------|---------|
| SQLI-01 | Config.java | 41-44 | User-controlled parameters `cust`, `site`, `dept` are concatenated directly into SQL: `" where c.\"USER_CD\" in (" + cust + " )"`. No parameterized queries or input sanitization. |
| SQLI-02 | Config.java | 42 | `user` from session attribute concatenated directly into SQL. |
| SQLI-03 | Config.java | 164-168 | `user` concatenated into SQL in `getPermision()`. |
| SQLI-04 | CriticalBattery.java | 103-106 | `cust`, `site`, `dept` concatenated into vehicle query. |
| SQLI-05 | CriticalBattery.java | 129 | `startTime` and `endTime` from request parameters concatenated into SQL timestamp literals. |
| SQLI-06 | Impacts.java | 111-117 | Same pattern with `cust`, `site`, `dept`. |
| SQLI-07 | Impacts.java | 171 | `startTime`, `endTime` concatenated into SQL. |
| SQLI-08 | Licence.java | 94-101 | `cust`, `site`, `dept` concatenated into SQL. |
| SQLI-09 | Preop.java | 102-105 | `cust`, `site`, `dept` concatenated into SQL. |
| SQLI-10 | Summary.java | all methods | Every method in Summary concatenates request parameters directly into SQL. |
| SQLI-11 | TableServlet.java | 92-99, 107-109 | `cust`, `site`, `dept`, and `search` concatenated into SQL. The `search` parameter is partially filtered by a regex test but the non-name branch still concatenates directly. |
| SQLI-12 | Utilisation.java | 138-150, 177-190 | `cust`, `site`, `dept`, `startTime`, `endTime` all concatenated. |

**All 9 files in this package construct SQL via string concatenation with user-supplied input.** No file uses `PreparedStatement`. This is a systemic SQL injection vulnerability across the entire dashboard package.

---

## 13. Additional Findings

| ID | File | Line(s) | Category | Finding |
|----|------|---------|----------|---------|
| ADD-01 | Preop.java | 44 | Dead code | `cusList` instance variable is declared and initialized but never read or written to by any method (unlike other servlets where `cusList` is at least referenced). |
| ADD-02 | CriticalBattery.java | 45 | Dead code | `cusList` instance variable declared but never used -- the class delegates customer queries to `Config.getCustomers()`. |
| ADD-03 | Impacts.java | 48 | Dead code | Same as ADD-02 -- `cusList` declared but unused. |
| ADD-04 | Summary.java | 36 | Dead code | Same pattern -- `cusList` declared but unused. |
| ADD-05 | Impacts.java | 369 | Logic error | `getAverage()` looks for key `"cd"` and `"percentage"` in `rsList` entries, but the `getDates()` query populates `rsList` with columns named `"shock_id"` and `"level"` (not `"cd"` or `"percentage"`). This method will always produce empty results. |
| ADD-06 | Utilisation.java | 42 | Visibility | `serialVersionUID` uses default (package-private) visibility: `static final long serialVersionUID`. Should be `private static final long`. |
| ADD-07 | TableServlet.java | 38 | Misleading | Instance variable `servlet` is set to `"/Servlet/UtilisationServlet"` but this is the `TableServlet` class. The wrong servlet path will appear in error log messages. |
| ADD-08 | CriticalBattery.java | 221 | Minor | Double semicolons: `Config.addSeries(series, "20%-30%", yellowList);;` |
| ADD-09 | Multiple | -- | Pattern | Massive code duplication of `saveasList()`, resource cleanup blocks, and vehicle-query construction across all servlets. The same 20-line finally-block pattern is copy-pasted at least 25 times across the package. |
| ADD-10 | Impacts.java | 158 | NPE risk | `endDate.getTime() - startDate.getTime()` -- if date parsing fails (line 155-157 catches ParseException with only `e.printStackTrace()`), then `endDate` or `startDate` remain null and this line throws NullPointerException. |
| ADD-11 | Preop.java | 120-121 | NPE risk | Same pattern: if `startDate` or `endDate` parsing fails, `endDate.getTime()` at line 120 will NPE. |

---

## Summary Statistics

| Category | Count |
|----------|------:|
| Style consistency issues | 9 |
| God class indicators | 3 |
| Thread-safety violations | 17 |
| Commented-out code blocks | 11 |
| Unused imports | 6 |
| Broad catch blocks | 24 |
| `e.printStackTrace()` calls | 26 |
| Shared mutable state issues | 7 |
| N+1 / excessive query patterns | 6 |
| String equality (`==`) issues | 1 |
| Resource management issues | 8 |
| SQL injection vectors | 12 |
| Additional findings | 11 |
| **Total findings** | **141** |

---

## Risk Assessment

| Risk | Files Affected | Summary |
|------|---------------|---------|
| **CRITICAL -- SQL Injection** | All 9 files | Every file constructs SQL via string concatenation with user-supplied request parameters. No use of `PreparedStatement` anywhere in the package. |
| **CRITICAL -- Thread Safety** | Config, TableServlet, Utilisation | Mutable instance/static variables on shared servlet instances are written and read by concurrent request threads with no synchronization. Config.cusList is the worst case: written on one request, read on subsequent requests from any user. |
| **HIGH -- Memory Leaks** | SessionCleanupListener | Only cleans up Impacts sessions. CriticalBattery, Preop, Licence, and Utilisation session maps grow without bound as sessions expire. |
| **HIGH -- God Classes** | Summary (768L), Utilisation (997L) | Excessive method counts and line counts with massive duplication. |
| **MEDIUM -- Error Handling** | All 9 files | 24 broad catches + 26 printStackTrace() calls. No logging framework. Errors are swallowed with no recovery and no notification to callers. |
| **LOW -- Code Hygiene** | Multiple | 11 commented-out blocks, 6 unused imports, dead code fields, typos in method/SQL names. |
