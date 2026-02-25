# Pass 2 — Test Coverage: dashboard package
**Agent:** A08
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Criteria | Status |
|---|---|
| Test directory exists | NO -- no `test/`, `src/test/`, or any test directory found in the repository |
| Test framework on classpath | NO -- no JUnit, TestNG, Mockito, or any test dependency declared |
| Test files for this package | **ZERO** -- 0 of 9 files have any corresponding test |
| CI test execution | No evidence of automated test execution |
| Code coverage tooling | None detected (no JaCoCo, Cobertura, etc.) |

**Effective test coverage for the dashboard package: 0%**

All 9 classes in this package handle HTTP requests and/or direct database access with zero automated test coverage. This is a CRITICAL gap for a production codebase.

---

## Reading Evidence

### 1. Config.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java` (218 lines)
- **Class:** `Config` (plain utility class, not a servlet)
- **Servlet mapping:** None (called statically by other servlets)
- **Public fields:**
  - `public static float siteHours = 24` (line 28)
  - `static LinkedList<HashMap<String, String>> cusList` (line 29, package-private)
  - `static Gson gson` (line 30, package-private)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| getCustomers | `public static void getCustomers(HttpServletRequest req, HttpServletResponse res) throws IOException` | 32 |
| getSites | `public static void getSites(HttpServletRequest req, HttpServletResponse res) throws IOException` | 72 |
| getDepartments | `public static void getDepartments(HttpServletRequest req, HttpServletResponse res) throws IOException` | 88 |
| saveasList | `public static LinkedList<HashMap<String, String>> saveasList(String query)` | 104 |
| getPermision | `public static void getPermision(HttpServletRequest req, HttpServletResponse res)` | 153 |
| addSeries (2-arg) | `public static void addSeries(List<Map<String, Object>> mplist, String name, List<Integer> list)` | 204 |
| addSeries (3-arg) | `public static void addSeries(List<Map<String, Object>> mplist, String name, String color, List<Integer> list)` | 211 |

---

### 2. CriticalBattery.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/CriticalBattery.java` (351 lines)
- **Class:** `CriticalBattery extends HttpServlet`
- **Servlet mapping:** `@WebServlet("/Servlet/CriticalBatteryServlet")` (line 35)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| doGet | `protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 50 |
| cleanupSession | `public static void cleanupSession(String sessionId)` | 347 |

- **Private methods:** `getDates` (line 85), `getTable` (line 252), `updateTable` (line 283), `mapValue` (line 330), `mapKey` (line 338)
- **Session maps:** `sessionRsListMap`, `sessionDateListMap` (static ConcurrentHashMap)

---

### 3. Impacts.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Impacts.java` (469 lines)
- **Class:** `Impacts extends HttpServlet`
- **Servlet mapping:** `@WebServlet("/Servlet/ImpactsServlet")` (line 36)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| doGet | `protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 53 |
| cleanupSession | `public static void cleanupSession(String sessionId)` | 465 |

- **Private methods:** `getDates` (line 94), `getTable` (line 268), `updateTable` (line 294), `getPie` (line 332), `getAverage` (line 358), `saveasList` (line 392), `mapValue` (line 441), `mapKey` (line 449), `addSeries` (line 457)
- **Session maps:** `sessionRsListMap`, `sessionDateListMap` (static ConcurrentHashMap)

---

### 4. Licence.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Licence.java` (315 lines)
- **Class:** `Licence extends HttpServlet`
- **Servlet mapping:** `@WebServlet("/Servlet/LicenceServlet")` (line 33)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| init | `public void init()` (override) | 47 |
| doGet | `protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 56 |
| cleanupSession | `public static void cleanupSession(String sessionId)` | 312 |

- **Private methods:** `getChart` (line 80), `updateTable` (line 175), `getTable` (line 241), `saveasList` (line 262)
- **Session maps:** `sessionRsListMap` (static ConcurrentHashMap)

---

### 5. Preop.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Preop.java` (347 lines)
- **Class:** `Preop extends HttpServlet`
- **Servlet mapping:** `@WebServlet("/Servlet/PreopServlet")` (line 34)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| doGet | `protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 49 |
| cleanupSession | `public static void cleanupSession(String sessionId)` | 343 |

- **Private methods:** `getDates` (line 84), `getTable` (line 246), `updateTable` (line 278), `mapValue` (line 326), `mapKey` (line 334)
- **Session maps:** `sessionRsListMap`, `sessionDateListMap` (static ConcurrentHashMap)

---

### 6. SessionCleanupListener.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/SessionCleanupListener.java` (30 lines)
- **Class:** `SessionCleanupListener implements HttpSessionListener`
- **Annotation:** `@WebListener` (line 12)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| sessionCreated | `public void sessionCreated(HttpSessionEvent se)` (override) | 16 |
| sessionDestroyed | `public void sessionDestroyed(HttpSessionEvent se)` (override) | 21 |

---

### 7. Summary.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Summary.java` (767 lines)
- **Class:** `Summary extends HttpServlet`
- **Servlet mapping:** `@WebServlet("/Servlet/SummaryServlet")` (line 32)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| doGet | `protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 39 |

- **Private methods:** `getBattery` (line 82), `getPreop` (line 165), `getImpactChart` (line 238), `getUtilisation` (line 312), `getLicence` (line 394), `getImpact` (line 479), `getUnit` (line 573), `getDriver` (line 673)

---

### 8. TableServlet.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/TableServlet.java` (640 lines)
- **Class:** `TableServlet extends HttpServlet`
- **Servlet mapping:** `@WebServlet("/Servlet/TableServlet")` (line 32)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| doGet | `protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 42 |
| saveasList | `public static LinkedList<HashMap<String, String>> saveasList(String query, String servlet)` | 591 |

- **Private methods:** `getVORStatus` (line 73), `getPreop` (line 174), `getDetailDriver` (line 273), `getDetailUnit` (line 440)
- **Instance fields:** `rsList` (line 37, shared mutable state -- NOT session-safe)

---

### 9. Utilisation.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Utilisation.java` (996 lines)
- **Class:** `Utilisation extends HttpServlet`
- **Servlet mapping:** `@WebServlet("/Servlet/UtilisationServlet")` (line 39)
- **Public methods:**

| Method | Signature | Line |
|---|---|---|
| doGet | `protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 54 |
| cleanupSession | `public static void cleanupSession(String sessionId)` | 992 |

- **Private methods:** `procedure` (line 123), `getDateData` (line 197), `getModelData` (line 309), `getSiteData` (line 367), `updateModelChart` (line 425), `updateSiteChart` (line 478), `updateDateChart` (line 531), `getTable` (line 611), `updateTable` (line 642), `updateDateTable` (line 695), `getPie` (line 784), `getModelAverage` (line 809), `getSiteAverage` (line 840), `getDateAverage` (line 871), `saveasList` (line 919), `mapValue` (line 968), `mapKey` (line 976), `addSeries` (line 984)
- **Session maps:** `sessionRsListMap`, `sessionDateListMap` (static ConcurrentHashMap)
- **Instance fields:** `vehicles` (line 49), `thresholdLow`/`thresholdHigh` (line 50), `oneDay` (line 52) -- mutable shared instance state

---

## Findings

### A08-01 — SQL Injection in Config.getCustomers via Unvalidated Request Parameters
**Severity:** CRITICAL
**File:** `Config.java`, lines 32-70
**Details:**
Request parameters `cust_cd`, `loc_cd`, `dept_cd`, and session attribute `user_cd` are concatenated directly into SQL strings without any parameterization or sanitization (lines 41-44). For example:
```java
if (level > 1 && !cust.equals("all")) condition = " where c.\"USER_CD\" in (" + cust +" ) ";
if (level > 2 && !site.equals("all")) condition += " and \"LOC_CD\" = " + site;
```
This is a textbook SQL injection vector. Tests needed:
- Injection via `cust_cd` parameter with SQL metacharacters (e.g., `1); DROP TABLE --`)
- Injection via `loc_cd` and `dept_cd` parameters
- Injection via `user_cd` session attribute (less likely from external attackers but still risky)
- Boundary: `access_level` empty string path (line 35) and `NumberFormatException` from `Integer.parseInt` (line 36)

---

### A08-02 — SQL Injection Across All Servlet doGet Handlers
**Severity:** CRITICAL
**Files:** `CriticalBattery.java` (lines 103-106, 123-148), `Impacts.java` (lines 111-117, 160-173), `Licence.java` (lines 94-101, 111-118), `Preop.java` (lines 102-105, 122-135), `Summary.java` (lines 99-102, 268-270, 496-498, etc.), `TableServlet.java` (lines 92, 107-109, 120-130, 193, 208-210, 303-309, 461-471), `Utilisation.java` (lines 138-143, 177-190)
**Details:**
Every servlet in this package constructs SQL queries by concatenating unsanitized HTTP request parameters (`cust_cd`, `loc_cd`, `dept_cd`, `start_time`, `end_time`, `st_dt`, `to_dt`, `search_crit`). No `PreparedStatement` is used anywhere. Every `saveasList()` variant and inline query block is vulnerable. Tests needed:
- Parameterized injection test for each of the 7 servlets
- Timestamp injection via `start_time`/`end_time` (e.g., `' OR 1=1 --`)
- Search criteria injection in `TableServlet.getDetailDriver` (lines 303-309) and `getDetailUnit` (lines 469-471)

---

### A08-03 — NullPointerException Paths in doGet Switch Dispatchers
**Severity:** HIGH
**Files:** All servlet classes (`CriticalBattery.java` line 51, `Impacts.java` line 54, `Licence.java` line 58, `Preop.java` line 50, `Summary.java` line 40, `TableServlet.java` line 46, `Utilisation.java` line 56)
**Details:**
Every servlet reads `req.getParameter("part")` without null-checking. If the `part` parameter is absent, `switch(part)` throws `NullPointerException`. The exception is unhandled and would result in a 500 error with no meaningful response. Tests needed:
- Request with no `part` parameter
- Request with empty-string `part` parameter
- Request with unrecognized `part` value (hits empty `default:` -- returns no response body)

---

### A08-04 — NullPointerException in Impacts.getDates When Parameters Are Null
**Severity:** HIGH
**File:** `Impacts.java`, lines 94-100, 112-116, 158
**Details:**
Parameters `mode`, `start_time`, `end_time`, `cust_cd`, `loc_cd`, `dept_cd` are read with `req.getParameter()` but never null-checked. Line 112: `site.equals("all")` will throw NPE if `site` is null. Line 158: `endDate.getTime() - startDate.getTime()` will throw NPE if date parsing fails (startDate/endDate remain null). Line 183: `mode.equals("hour")` will throw NPE if mode is null. This same pattern exists in:
- `CriticalBattery.getDates` (lines 86-91, 105-106, 123)
- `Preop.getDates` (lines 85-90, 104-105, 120-121, 143)
- `Summary` -- all private methods read parameters without null checks
- `Utilisation.procedure` (lines 124-128, 139-143)

Tests needed:
- Each servlet endpoint with missing required parameters
- Date parsing with malformed date strings
- `mode` parameter as null or invalid value

---

### A08-05 — Shared Mutable Instance State in TableServlet (Thread-Safety)
**Severity:** HIGH
**File:** `TableServlet.java`, lines 36-40
**Details:**
```java
LinkedList<HashMap<String, String>> rsList = new LinkedList<HashMap<String, String>>();  // line 37
String servlet = "/Servlet/UtilisationServlet";  // line 38 (wrong servlet name)
int defaultCust = 249;  // line 39
```
`rsList` is an instance field on a shared servlet instance. Multiple concurrent requests will read/write the same list (e.g., `rsList.clear()` at line 131, 231, 397, 548). This causes race conditions, data corruption, and cross-user data leakage. Unlike `CriticalBattery`, `Impacts`, `Preop`, and `Utilisation` which were refactored to use `ConcurrentHashMap<sessionId, ...>`, `TableServlet` was NOT refactored.
Tests needed:
- Concurrent request simulation showing data race on `rsList`
- Verify `rsList.clear()` followed by `rsList = saveasList(...)` can interleave with another request's read

---

### A08-06 — Shared Mutable Instance State in Utilisation (Thread-Safety)
**Severity:** HIGH
**File:** `Utilisation.java`, lines 49-52
**Details:**
```java
String vehicles = "";          // line 49
int thresholdLow = 25, thresholdHigh = 50;  // line 50
boolean oneDay = false;        // line 52
```
These are instance-level fields on a shared servlet. `vehicles` is written in `procedure()` (line 146) and read in `getDateData()` (line 227). `thresholdLow`/`thresholdHigh` are written from request parameters in multiple methods. `oneDay` is written in `getDateData()` (line 210) and read in `updateDateChart()` (line 563) and `updateDateTable()` (line 729). Concurrent requests will corrupt each other's state.
Tests needed:
- Concurrent requests with different `cust_cd` values showing `vehicles` contamination
- Concurrent requests with different `high`/`low` threshold values
- The `oneDay` flag being read by one request after another request sets it

---

### A08-07 — SessionCleanupListener Only Cleans Up Impacts (Incomplete Cleanup)
**Severity:** MEDIUM
**File:** `SessionCleanupListener.java`, lines 21-29
**Details:**
```java
public void sessionDestroyed(HttpSessionEvent se) {
    String sessionId = se.getSession().getId();
    Impacts.cleanupSession(sessionId);
    // Add other cleanup calls for other servlets as needed  <-- NOT DONE
}
```
Only `Impacts.cleanupSession()` is called. The following servlets also have session-specific data in static ConcurrentHashMaps that are NOT cleaned up:
- `CriticalBattery.cleanupSession()` -- NOT called
- `Preop.cleanupSession()` -- NOT called
- `Utilisation.cleanupSession()` -- NOT called
- `Licence.cleanupSession()` -- NOT called

This causes memory leaks as session data accumulates without being freed.
Tests needed:
- Session destruction should trigger cleanup for all 5 servlets
- Memory leak test over many session create/destroy cycles

---

### A08-08 — Config.cusList is Shared Static Mutable State Across All Sessions
**Severity:** HIGH
**File:** `Config.java`, line 29
**Details:**
```java
static LinkedList<HashMap<String, String>> cusList = new LinkedList<HashMap<String, String>>();
```
`cusList` is a static field written by `getCustomers()` (line 59) and read by `getSites()` (line 75) and `getDepartments()` (line 91). When User A calls `getCustomers()`, it overwrites `cusList`. If User B then calls `getSites()`, User B sees User A's customer list. This is a cross-user data leakage vulnerability.
Tests needed:
- Two different users calling `getCustomers()` then `getSites()` in sequence, verifying data isolation
- Concurrent access to `cusList` showing race conditions (not synchronized, not thread-safe)

---

### A08-09 — No Input Validation or Sanitization on Any Request Parameter
**Severity:** HIGH
**Files:** All 9 files
**Details:**
No file in this package performs any input validation (length checks, type checks, allowlist matching, encoding, etc.) on any request parameter. Examples:
- `to_dt.substring(11, 13)` in `Summary.java` line 87 and line 317 -- will throw `StringIndexOutOfBoundsException` if `to_dt` is shorter than 13 characters or null
- `Integer.parseInt(access_level)` in `Config.java` line 36 -- `NumberFormatException` if not numeric
- `Integer.parseInt(req.getParameter("high"))` in `Utilisation.java` line 220 -- `NumberFormatException` if not numeric
- Date parsing with `SimpleDateFormat("dd/MM/yyyy HH:mm")` swallows `ParseException` and then tries to dereference null date objects
Tests needed:
- Malformed date strings
- Non-numeric values for numeric parameters (`cust_cd`, `loc_cd`, `dept_cd`, `high`, `low`)
- `to_dt` parameter with fewer than 13 characters
- Empty strings for all parameters

---

### A08-10 — Error Responses Not Sent to Client; Exceptions Logged to stdout Only
**Severity:** MEDIUM
**Files:** All 9 files
**Details:**
Every catch block in the package follows this pattern:
```java
} catch (Exception e) {
    System.out.println(servlet + ": " + e);
    e.printStackTrace();
}
```
The exception is printed to stdout/stderr, but no error response is written to `HttpServletResponse`. The client receives an empty 200 OK response or a 500 if the exception propagates. No HTTP error status codes (400, 500) are set. No structured error JSON is returned.
Tests needed:
- Database connection failure -- verify response status and body
- SQL execution error -- verify response status and body
- Verify `res.sendError()` or equivalent is used

---

### A08-11 — Licence.updateTable NPE When category Is "without" and Null Check Bypassed
**Severity:** HIGH
**File:** `Licence.java`, lines 175-238
**Details:**
At line 183, `category` can be null (from `req.getParameter("category")`). At line 188, `category` is used in a conditional but may be null. At line 197, `category.equals("without")` will throw NPE if `category` is null. This is reachable because the null ternary on line 183 preserves null:
```java
String category = req.getParameter("category") == null ? null : req.getParameter("category");
```
Additionally, line 187: `entry.get("status").replace("due in ", "<")` will NPE if `status` is null.
Tests needed:
- `updateTable` with `category=null`
- `updateTable` with `category=without` and all parameter combinations
- Result set where `status` field is null in the database

---

### A08-12 — CriticalBattery.updateTable and Preop.updateTable NPE on Null Map Entries
**Severity:** MEDIUM
**File:** `CriticalBattery.java`, lines 283-328; `Preop.java`, lines 278-324
**Details:**
In both files, `entry1.get("id")` and `entry1.get("series")` are called without null checks at lines 304 and 299 respectively. If the database row has null values for these columns, the `.equals()` call throws NPE. Similarly in `Impacts.updateTable` (line 306): `entry1.get("shock_id").equals(id)` and `entry1.get("level").equalsIgnoreCase(series)`.
Tests needed:
- Null `id`/`shock_id` in result set rows
- Null `series`/`level` in result set rows
- Empty `dateList` or `rsList` scenarios

---

### A08-13 — Impacts.getAverage References Non-Existent Map Keys
**Severity:** MEDIUM
**File:** `Impacts.java`, lines 358-389
**Details:**
At line 369, `cd.equals(entry1.get("cd"))` references key `"cd"`, but the `rsList` is populated from a query whose columns include `"shock_id"`, `"level"`, `"time"`, etc. -- there is no column named `"cd"`. Similarly, line 370 references `entry1.get("percentage")` but no `"percentage"` column exists in the Impacts query. This method appears to be dead/broken code copied from another servlet.
Tests needed:
- Call the `average` endpoint and verify it produces correct output
- Verify key names match the actual SQL column names

---

### A08-14 — Config.getCustomers Uses Reference Equality (==) for String Comparison
**Severity:** MEDIUM
**File:** `Config.java`, line 42
**Details:**
```java
if (user != null && cust == LindeConfig.customerLinde)
```
The `==` operator compares object references, not string content. This condition will almost never be true because `cust` comes from `req.getParameter()` (a new String object each time). Should be `.equals()`.
Tests needed:
- Verify the `LindeConfig.customerLinde` code path is reachable
- Test with `cust` value matching `LindeConfig.customerLinde` string content

---

### A08-15 — No Authentication or Authorization Checks in Any Servlet
**Severity:** HIGH
**Files:** All servlet classes
**Details:**
No servlet in this package checks whether the user is authenticated before processing the request. `Config.getCustomers()` reads `req.getSession().getAttribute("user_cd")` (line 33) and would throw NPE if the attribute is missing (unauthenticated session), but this is not a proper auth check. None of the other methods verify session validity. `Config.getPermision()` queries permissions but the result is just returned to the client -- it does not gate access.
Tests needed:
- Requests with no session
- Requests with session but no `user_cd` attribute
- Requests with session but insufficient permissions
- Direct URL access bypassing any login flow

---

### A08-16 — Licence.init() Loads All Customers Into Instance-Level List Without Filtering
**Severity:** MEDIUM
**File:** `Licence.java`, lines 47-54
**Details:**
The `init()` method loads ALL customers from the database into `cusList` (an instance field) at servlet startup. This data is:
1. Never refreshed (stale after any customer changes)
2. Shared across all users of the servlet (no per-user filtering)
3. Not used by the session-aware methods (which use their own `sessionRsListMap`)
Tests needed:
- Verify `cusList` contains expected data
- Verify stale data after customer table changes
- Verify thread-safety of `cusList` access

---

### A08-17 — TableServlet Search Parameter Allows SQL Injection via LIKE Pattern
**Severity:** CRITICAL
**File:** `TableServlet.java`, lines 103-111, 200-212, 303-309, 469-472
**Details:**
The `search_crit` parameter is used in SQL LIKE clauses with only an alphabetic regex check to decide query path, but:
1. The regex check at line 104 (`contains_number = m.matches()`) is testing if the string is ALL letters/spaces. If it is, the string goes into a name search. If not (i.e., it contains numbers or special chars), it goes directly into a vehicle search -- with NO sanitization:
```java
vehiclesQuery += " and (lower(\"HIRE_NO\") like lower('%" + search + "%') or lower(\"SERIAL_NO\") like lower('%" + search + "%'))";
```
2. In `getDetailDriver` (line 303-309), the search parameter is injected into ILIKE clauses:
```java
driversQuery += " and (\"CONTACT_LAST_NAME\" ilike '%" + search + "%' ..."
```
A search value like `%'); DROP TABLE -- ` would break out of the LIKE and inject arbitrary SQL.
Tests needed:
- SQL injection via `search_crit` with SQL metacharacters
- LIKE wildcard injection (`%`, `_`)
- Both the alphabetic and non-alphabetic code paths

---

### A08-18 — JDBC Resource Management Relies on Manual Finally Blocks
**Severity:** LOW
**Files:** All files with database access (Config.java, CriticalBattery.java, Impacts.java, Licence.java, Preop.java, Summary.java, TableServlet.java, Utilisation.java)
**Details:**
Every database operation uses manual try/finally blocks to close Connection, Statement, and ResultSet instead of try-with-resources. While the finally blocks are present and generally correct, there are cases where ResultSet is reused (e.g., `Summary.java` lines 102-119 where `rs` is reassigned multiple times inside the try block -- if a later `executeQuery` fails, only the last `rs` reference is closed in finally).
Tests needed:
- Connection pool exhaustion under error conditions
- Verify all resources are closed when exceptions occur mid-method
- `Summary.getImpact()` (lines 479-571) executes 4 sequential queries reusing `rs` -- verify all get closed

---

## Summary of Coverage Gaps

| ID | Title | Severity | Files Affected |
|---|---|---|---|
| A08-01 | SQL Injection in Config.getCustomers | CRITICAL | Config.java |
| A08-02 | SQL Injection Across All Servlet doGet Handlers | CRITICAL | All 7 servlet classes |
| A08-03 | NPE on Null `part` Parameter in doGet Dispatchers | HIGH | All 7 servlet classes |
| A08-04 | NPE When Required Parameters Are Null | HIGH | CriticalBattery, Impacts, Preop, Summary, Utilisation |
| A08-05 | Shared Mutable rsList in TableServlet (Thread-Safety) | HIGH | TableServlet.java |
| A08-06 | Shared Mutable Instance State in Utilisation | HIGH | Utilisation.java |
| A08-07 | SessionCleanupListener Only Cleans Impacts | MEDIUM | SessionCleanupListener.java |
| A08-08 | Static cusList Cross-User Data Leakage | HIGH | Config.java |
| A08-09 | No Input Validation on Any Parameter | HIGH | All 9 files |
| A08-10 | Exceptions Not Returned to Client | MEDIUM | All 9 files |
| A08-11 | Licence.updateTable NPE on Null category | HIGH | Licence.java |
| A08-12 | NPE on Null Map Entries in updateTable | MEDIUM | CriticalBattery, Preop, Impacts |
| A08-13 | Impacts.getAverage References Wrong Keys | MEDIUM | Impacts.java |
| A08-14 | String Reference Equality (==) in Config | MEDIUM | Config.java |
| A08-15 | No Authentication/Authorization Checks | HIGH | All servlet classes |
| A08-16 | Licence.init() Stale Shared Data | MEDIUM | Licence.java |
| A08-17 | SQL Injection via search_crit LIKE | CRITICAL | TableServlet.java |
| A08-18 | Manual JDBC Resource Management | LOW | All 8 DB-accessing files |

**Total findings: 18**
- CRITICAL: 3
- HIGH: 8
- MEDIUM: 6
- LOW: 1

### Recommended Test Priorities (Highest First)
1. **SQL injection tests** for all servlets (A08-01, A08-02, A08-17) -- requires parameterized queries as the fix
2. **Null parameter handling** for all doGet dispatchers (A08-03, A08-04, A08-11)
3. **Thread-safety tests** for TableServlet and Utilisation shared state (A08-05, A08-06, A08-08)
4. **Authentication/authorization gate tests** (A08-15)
5. **Session cleanup completeness** (A08-07)
6. **Error response behavior** (A08-10)
