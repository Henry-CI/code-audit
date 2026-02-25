# Security Audit — Dashboard Module
**Audit ID:** A17
**Run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Auditor:** Agent A17
**Date:** 2026-02-25

---

## STEP 3 — READING EVIDENCE

### JSP Files

#### `dashboard/jsp/header_filter.jsp`
- No `<%@ page import %>` directives.
- No `<%@ include %>` or `<jsp:include>` directives.
- **Scriptlet blocks:**
  - Lines 65–67: Permission check `permision[form_cd][3].equalsIgnoreCase("t")` — controls Print button rendering.
  - Lines 68–70: Permission check `permision[form_cd][2].equalsIgnoreCase("t")` — controls Email/Subscribe button rendering.
  - Lines 72–74: Permission check `permision[form_cd][1].equalsIgnoreCase("t")` — controls Export button rendering.
- **Expression outputs (`<%= ... %>`):**
  - Line 3: `<%=request.getParameter("mnm").toString()%>` — raw user-supplied request parameter output into an HTML `value` attribute. Not escaped.
  - Line 4: `<%=request.getParameter("sub").toString()%>` — same pattern. Not escaped.
  - Line 5: `<%=form_cd%>` — sourced from a scriptlet variable (origin unclear without parent context; likely from session/DB).

#### `dashboard/jsp/header_vor_status.jsp`
- Identical in structure to `header_filter.jsp` (same pattern for lines 3–5, 65–74).
- Same unescaped `<%=request.getParameter("mnm").toString()%>` and `<%=request.getParameter("sub").toString()%>` at lines 3–4.
- No `<%@ page import %>` or include directives.

#### `dashboard/jsp/summary.jsp`
- **Directives:**
  - Line 1: `<%@ include file="../../sess/Expire.jsp" %>` — session expiry guard included.
  - Line 2: `<%@ page import="java.util.*,com.torrent.surat.fms6.util.LindeConfig"%>`
- **Scriptlet blocks (lines 3–12):**
  - `cust_cd`, `loc_cd`, `dept_cd` sourced from request parameter if present, otherwise from session attributes `access_cust`, `access_site`, `access_dept` (with `.substring(2)` stripping).
  - `access_level` and `access_user` read from session.
  - Line 11: If `access_l == 3`, `dept_cd` is forced to `"0"` (overriding user input for this access level).
- **Expression outputs (`<%= ... %>`) in JavaScript block (lines 254–260):**
  - Line 254: `var cust_cd = <%=cust_cd%>;` — server-side value interpolated into JavaScript. `cust_cd` comes from `request.getParameter("cust_cd")` with no sanitisation.
  - Line 255: `var loc_cd = <%=loc_cd%>;` — same pattern, from `request.getParameter("loc_cd")`.
  - Line 256: `var dept_cd = <%=dept_cd%>;` — same pattern, from `request.getParameter("dept_cd")`.
  - Line 257: `var isForVisyLimitingLocations = <%=com.torrent.surat.fms6.util.DataUtil.isForVisyLimitingLocations(cust_cd, access_user)%>` — DB-sourced boolean; low risk but unquoted.
  - Line 258: `if (cust_cd == 9999 || cust_cd == 0) cust_cd = <%=LindeConfig.customerLinde%>;` — static config value, low risk.
- No `<jsp:include>` directives.

---

### Java Files

#### `com.torrent.surat.fms6.dashboard.Config`
- **Fully qualified class name:** `com.torrent.surat.fms6.dashboard.Config`
- **Imports:** `java.io.IOException`, `java.sql.*`, `java.util.*`, `javax.naming.*`, `javax.servlet.http.*`, `javax.sql.DataSource`, `com.google.gson.Gson`, `com.torrent.surat.fms6.util.DataUtil`, `com.torrent.surat.fms6.util.LindeConfig`, `com.torrent.surat.fms6.util.RuntimeConf`
- **Fields:**
  - `public static float siteHours = 24`
  - `static LinkedList<HashMap<String, String>> cusList`
  - `static Gson gson`
- **Public methods:**
  - `public static void getCustomers(HttpServletRequest req, HttpServletResponse res) throws IOException` — line 32
  - `public static void getSites(HttpServletRequest req, HttpServletResponse res) throws IOException` — line 72
  - `public static void getDepartments(HttpServletRequest req, HttpServletResponse res) throws IOException` — line 88
  - `public static LinkedList<HashMap<String, String>> saveasList(String query)` — line 104
  - `public static void getPermision(HttpServletRequest req, HttpServletResponse res)` — line 153
  - `public static void addSeries(List<Map<String, Object>> mplist, String name, List<Integer> list)` — line 204
  - `public static void addSeries(List<Map<String, Object>> mplist, String name, String color, List<Integer> list)` — line 211

#### `com.torrent.surat.fms6.dashboard.Summary` (servlet: `/Servlet/SummaryServlet`)
- **Imports:** Standard Java SQL/util, `javax.servlet.*`, `com.google.gson.Gson`, `com.torrent.surat.fms6.util.LindeConfig`, `com.torrent.surat.fms6.util.RuntimeConf`
- **Fields:** `serialVersionUID`, `cusList`, `gson`
- **Methods (all private except doGet):**
  - `protected void doGet(HttpServletRequest req, HttpServletResponse res)` — line 39
  - `private void getBattery(HttpServletRequest req, HttpServletResponse res)` — line 82
  - `private void getPreop(HttpServletRequest req, HttpServletResponse res)` — line 165
  - `private void getImpactChart(HttpServletRequest req, HttpServletResponse res)` — line 238
  - `private void getUtilisation(HttpServletRequest req, HttpServletResponse res)` — line 312
  - `private void getLicence(HttpServletRequest req, HttpServletResponse res)` — line 394
  - `private void getImpact(HttpServletRequest req, HttpServletResponse res)` — line 479
  - `private void getUnit(HttpServletRequest req, HttpServletResponse res)` — line 573
  - `private void getDriver(HttpServletRequest req, HttpServletResponse res)` — line 673

#### `com.torrent.surat.fms6.dashboard.CriticalBattery` (servlet: `/Servlet/CriticalBatteryServlet`)
- Session-keyed `ConcurrentHashMap` for `sessionRsListMap` and `sessionDateListMap`.
- `getDates`, `getTable`, `updateTable` methods; delegates customer/site/dept to `Config`.

#### `com.torrent.surat.fms6.dashboard.Impacts` (servlet: `/Servlet/ImpactsServlet`)
- Session-keyed maps; `getDates`, `getTable`, `updateTable`, `getPie`, `getAverage`.

#### `com.torrent.surat.fms6.dashboard.Licence` (servlet: `/Servlet/LicenceServlet`)
- `init()` method (line 47) executes a query loading ALL customers at startup with no access filtering.
- `getChart`, `getTable`, `updateTable` methods.

#### `com.torrent.surat.fms6.dashboard.Preop` (servlet: `/Servlet/PreopServlet`)
- Session-keyed maps; `getDates`, `getTable`, `updateTable`.

#### `com.torrent.surat.fms6.dashboard.TableServlet` (servlet: `/Servlet/TableServlet`)
- Instance-level (non-session-isolated) `rsList` field — shared across concurrent requests.
- `getDetailUnit`, `getDetailDriver`, `getPreop`, `getVORStatus` methods; delegates cust/site/dept to `Config`.

#### `com.torrent.surat.fms6.dashboard.Utilisation` (servlet: `/Servlet/UtilisationServlet`)
- Instance-level `vehicles` and `oneDay` fields — shared across concurrent requests.
- `procedure`, `getDateData`, `getModelData`, `getSiteData`, `updateTable`, etc.

#### `com.torrent.surat.fms6.dashboard.SessionCleanupListener`
- Implements `HttpSessionListener`; `sessionDestroyed` calls `Impacts.cleanupSession()` only — does NOT clean up `CriticalBattery`, `Preop`, `Utilisation`, or `Licence` servlet maps.

---

## STEP 4 — SECURITY REVIEW

### Authorization (Section 2)
- `summary.jsp` reads `cust_cd`, `loc_cd`, `dept_cd` from request parameters first, falling back to session. This means a user can override their session-scoped customer by supplying a different `cust_cd` in the URL. The dashboard form action passes these values on to all subsequent AJAX calls to `SummaryServlet`. The `SummaryServlet` performs no server-side re-validation that the supplied `cust_cd` belongs to the authenticated user.
- `Config.getCustomers()` (line 41) does apply an access-level guard: `if (level > 1 && !cust.equals("all")) condition = " where c.\"USER_CD\" in (" + cust + " )"`. However, a level-1 (super-admin) user gets no restriction. For level > 1, the filter only operates if the user supplies a non-"all" value. If the user supplies an arbitrary integer as `cust_cd`, the filter accepts it as long as it's a valid customer code.
- `header_filter.jsp` and `header_vor_status.jsp` contain a `cust_cd` select whose options are populated via JavaScript/AJAX. There is no server-side check in the form processing that the submitted `cust_cd` is actually one the user is permitted to see.
- `Config.cusList` is a **static shared field**. It is overwritten on every call to `getCustomers()`. Between a write and subsequent reads by `getSites()` or `getDepartments()`, a concurrent user's call can replace it. This is a race condition that can expose one user's customer list to another user's site/dept queries.

### SQL Injection (Section 3)
- Throughout `Summary.java`, `Config.java`, `CriticalBattery.java`, `Impacts.java`, `Licence.java`, `Preop.java`, `TableServlet.java`, and `Utilisation.java`, all SQL queries are built via string concatenation. Parameters sourced directly from `req.getParameter(...)` are inserted without any parameterized query (`PreparedStatement`) or escaping. Affected parameters include: `cust_cd`, `loc_cd`, `dept_cd`, `st_dt`/`start_time`, `to_dt`/`end_time`, `search_crit`, `mode`, `category`, `series`, `high`, `low`.
- `Config.getPermision()` (line 168) concatenates `user` (read from session's `user_cd`) directly into SQL. While session values are generally less attacker-controlled than request parameters, if `user_cd` is ever user-supplied during login and stored unsanitised, this is exploitable.
- `TableServlet.getDetailDriver()` (lines 304–309) concatenates `search` (from `request.getParameter("search_crit")`) into an `ilike` pattern: `"%" + search + "%"`. No escaping of SQL metacharacters (`%`, `_`, `'`, `;`).
- `TableServlet.getDetailUnit()` (lines 469–471) similarly concatenates `search` into `ilike '%" + search + "%'`. Same problem.
- `TableServlet.getVORStatus()` (lines 107–110) applies a regex check `^[A-Za-z\\s]*$` before concatenating into a `like` clause, but the regex only covers the `nameCon` branch; the `vehiclesQuery` branch at line 109 concatenates `search` without the guard.

### XSS (Section 3)
- `header_filter.jsp` lines 3–4: `<%=request.getParameter("mnm").toString()%>` and `<%=request.getParameter("sub").toString()%>` are written into HTML `input value` attributes without HTML encoding. An attacker can craft a URL with `mnm="><script>alert(1)</script>` or a similar payload to inject into the page if the value is not already attribute-escaped by the browser in reflected context.
- `header_vor_status.jsp` lines 3–4: Same pattern, same vulnerability.
- `summary.jsp` lines 254–256: `cust_cd`, `loc_cd`, and `dept_cd` are interpolated directly into a JavaScript block as unquoted values:
  ```javascript
  var cust_cd = <%=cust_cd%>;
  var loc_cd = <%=loc_cd%>;
  var dept_cd = <%=dept_cd%>;
  ```
  Because the values come from `request.getParameter(...)` with only a null check and `substring(2)` applied (no type enforcement), an attacker can inject arbitrary JavaScript. For example, `cust_cd=0;alert(document.cookie)//` would produce `var cust_cd = 0;alert(document.cookie)//;`.
- No HTML escaping (e.g., JSTL `<c:out>`, `StringEscapeUtils`, or `ESAPI`) is applied anywhere in the dashboard JSPs.

### SSRF (Section 3)
- No HTTP client calls to external URLs were found in the dashboard package. The dashboard data is sourced entirely from the internal database via JNDI datasource. No SSRF surface identified.

### Sensitive Data in Dashboard (Section 5)
- `Summary.getDriver()` (lines 690–698) returns counts and lists of driver user codes. These are returned as JSON to the browser with no explicit tenant scope check beyond the `cust_cd` parameter (which, as noted, is caller-supplied).
- `Summary.getUnit()` returns vehicle counts and activity metrics filtered only by the caller-supplied `cust_cd`.
- `CriticalBattery.getDates()` returns driver names (`CONTACT_FIRST_NAME`, `CONTACT_LAST_NAME`), card IDs (`CARD_ID`), vehicle serial numbers, and battery telemetry data. This constitutes PII and operational data.
- `Impacts.getDates()` returns driver names, card IDs, impact force values, and vehicle information — all scoped only by the caller-supplied `cust_cd`.
- `Licence.getChart()` returns driver names, email addresses (`EMAIL_ADDR`), phone numbers (`PHONE_NUMBER`), and licence expiry dates — significant PII exposure.
- GPS coordinates are not directly returned in dashboard API responses reviewed, but location-derived data (site name, department, GPS zone names via `fms_gps_zone_mst`) is included in `TableServlet.getDetailDriver()`.

---

## STEP 5 — FINDINGS

---

### A17-1
**File:** `C:\Projects\cig-audit\repos\fleetfocus\dashboard\jsp\summary.jsp`, lines 254–256
**Severity:** High
**Category:** XSS — JavaScript Injection
**Description:** Request parameters `cust_cd`, `loc_cd`, and `dept_cd` are interpolated directly into a JavaScript block without type-checking or output encoding. An attacker supplying a crafted value for any of these parameters can inject and execute arbitrary JavaScript in the victim's browser (reflected XSS via DOM).

**Evidence:**
```java
// summary.jsp lines 5-7 (server-side value construction from request param):
String cust_cd = request.getParameter("cust_cd") == null ?
    ((String)session.getAttribute("access_cust")).substring(2) :
    request.getParameter("cust_cd");

// summary.jsp lines 254-256 (injection point):
var cust_cd = <%=cust_cd%>;
var loc_cd = <%=loc_cd%>;
var dept_cd = <%=dept_cd%>;
```

**Recommendation:** Enforce integer parsing server-side before use. Replace the raw interpolation with explicit integer-cast outputs, e.g., use `Integer.parseInt(cust_cd)` in the scriptlet and emit only the numeric result. Alternatively, wrap in `"` quotes and apply JavaScript string escaping (`StringEscapeUtils.escapeEcmaScript()`). Never emit unvalidated string request parameters into a JavaScript context.

---

### A17-2
**File:** `C:\Projects\cig-audit\repos\fleetfocus\dashboard\jsp\header_filter.jsp`, lines 3–4; `C:\Projects\cig-audit\repos\fleetfocus\dashboard\jsp\header_vor_status.jsp`, lines 3–4
**Severity:** Medium
**Category:** XSS — Reflected HTML Attribute Injection
**Description:** The request parameters `mnm` and `sub` are reflected into HTML `input` element `value` attributes without HTML encoding. A crafted URL can break out of the attribute context and inject HTML/script.

**Evidence:**
```jsp
<!-- header_filter.jsp line 3 -->
<input type="hidden" value="<%=request.getParameter("mnm").toString()%>" name="mnm">
<!-- header_filter.jsp line 4 -->
<input type="hidden" value="<%=request.getParameter("sub").toString()%>" name="sub">
```

**Recommendation:** Use `ESAPI.encoder().encodeForHTMLAttribute(request.getParameter("mnm"))` or the JSTL `<c:out value="${param.mnm}" escapeXml="true"/>` pattern. Never reflect raw request parameters into HTML attributes.

---

### A17-3
**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\Summary.java`, multiple methods; `Config.java`; `CriticalBattery.java`; `Impacts.java`; `Licence.java`; `Preop.java`; `TableServlet.java`; `Utilisation.java`
**Severity:** Critical
**Category:** SQL Injection
**Description:** Every SQL query in the dashboard package is constructed by string concatenation of unsanitised request parameters. `Statement.executeQuery()` (not `PreparedStatement`) is used throughout. All filter parameters — `cust_cd`, `loc_cd`, `dept_cd`, `st_dt`, `to_dt`, `start_time`, `end_time`, `search_crit`, `mode`, `category`, `series`, `high`, `low` — flow directly from `req.getParameter()` into SQL strings with no type validation, no quoting, and no parameterization.

**Evidence (representative samples):**
```java
// Summary.java line 100 (getBattery):
String vehiclesQuery = "select v.\"VEHICLE_CD\" from \"FMS_VEHICLE_MST\" v join \"FMS_USR_VEHICLE_REL\" r on v.\"VEHICLE_CD\" = r.\"VEHICLE_CD\" "
    + "where \"IS_UNIT\" is true and lowutil = FALSE and \"USER_CD\" = " + cust;

// Summary.java lines 117-118 (getBattery inner query):
query = queryheader + " and utc_time between date_trunc('hour', timestamp '" + to_dt + "') and timestamp '" + to_dt + "'...";

// Summary.java lines 196-197 (getPreop):
String query = "select sum(...) from ... where starttimestamp >= timestamp '" + st_dt + "' and starttimestamp <= timestamp '" + to_dt + "' "
    + "and r.driver_id!= '0' and vehicle_cd in " + vehicles + " group by r.id) a";

// Config.java lines 41-44 (getCustomers):
if (level > 1 && !cust.equals("all")) condition = " where c.\"USER_CD\" in (" + cust +" ) ";
if (level > 2 && !site.equals("all")) condition += " and \"LOC_CD\" = " + site;
if (level > 3 && !dept.equals("all")) condition += " and d.\"DEPT_CD\" = " + dept;

// TableServlet.java lines 304-309 (getDetailDriver — search_crit):
if (!search.equals("")) {
    driversQuery += " and (\"CONTACT_LAST_NAME\" ilike '%" + search
        + "%' or \"CONTACT_FIRST_NAME\" ilike '%" + search + "%' ...";
}
```

**Recommendation:** Replace all `Statement` usage with `PreparedStatement`. Bind every filter parameter as a typed parameter (integer, timestamp, string). For parameters that must be integers (IDs), parse them with `Integer.parseInt()` immediately upon receipt and throw an exception on failure before they reach any SQL context. For date parameters, parse through `SimpleDateFormat` first and pass as `java.sql.Timestamp`. For free-text search fields, use `PreparedStatement` with `?` placeholders.

---

### A17-4
**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\Config.java`, field `cusList` (line 29); method `getCustomers` (line 59), `getSites` (line 75), `getDepartments` (line 91)
**Severity:** High
**Category:** Authorization / Race Condition — Cross-Tenant Data Exposure
**Description:** `cusList` is a `static` field shared across all threads and all user sessions. `getCustomers()` overwrites it with one user's customer scope (line 59: `cusList = Config.saveasList(query)`). `getSites()` and `getDepartments()` then read from `cusList` without re-querying, scoped only by what the last `getCustomers()` call wrote. Under concurrent load, User A's call to `getSites()` or `getDepartments()` can read User B's customer list, exposing cross-tenant site and department names to the wrong user. This is a Tenant Isolation failure.

**Evidence:**
```java
// Config.java line 29:
static LinkedList<HashMap<String, String>> cusList = new LinkedList<HashMap<String, String>>();

// Config.java line 59 (getCustomers overwrites shared field):
cusList = Config.saveasList(query);

// Config.java lines 75-85 (getSites reads shared field without re-scoping):
public static void getSites(HttpServletRequest req, HttpServletResponse res) throws IOException {
    String cust = req.getParameter("cust_cd") == null ? "all" : req.getParameter("cust_cd");
    LinkedList<HashMap<String, String>> list = new LinkedList<HashMap<String, String>>();
    for (Map<String, String> entry : cusList) {
        if (cust.equals(entry.get("USER_CD")) || cust.equalsIgnoreCase("all")) {
            ...
        }
    }
}
```

**Recommendation:** Remove `cusList` as a static shared field. Execute fresh, session-scoped queries in each of `getSites()` and `getDepartments()`, joining against the requesting user's session-derived customer scope. Alternatively, make `cusList` a local variable within a single request scope and pass it explicitly, or store per-session in `HttpSession`.

---

### A17-5
**File:** `C:\Projects\cig-audit\repos\fleetfocus\dashboard\jsp\summary.jsp`, lines 5–7; `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\Summary.java`, all data-retrieval methods
**Severity:** High
**Category:** Authorization — Missing Tenant Scope Enforcement
**Description:** `summary.jsp` accepts `cust_cd`, `loc_cd`, and `dept_cd` from the request parameter first, using session values only when the parameter is absent. The servlet `SummaryServlet` uses these caller-supplied values to filter all data queries without verifying that the authenticated user is permitted to access the requested customer. An authenticated user can substitute any `cust_cd` value in API calls to `/Servlet/SummaryServlet?part=driver&cust_cd=<target>` and retrieve driver, vehicle, impact, and licence data for an arbitrary tenant.

**Evidence:**
```java
// summary.jsp lines 5-7:
String cust_cd = request.getParameter("cust_cd") == null ?
    ((String)session.getAttribute("access_cust")).substring(2) :
    request.getParameter("cust_cd");

// Summary.java line 691 (getDriver — no ownership check):
String driversQuery = "select u.\"USER_CD\" from \"FMS_USER_DEPT_REL\" r join \"FMS_USR_MST\" u on r.\"USER_CD\" = u.\"USER_CD\" " +
    "where \"ACTIVE\" is true and \"ISDRIVER\" is true and \"CUST_CD\" = " + cust;
// 'cust' is directly from req.getParameter("cust_cd") — no session cross-check.
```

**Recommendation:** In each servlet handler, after reading `cust_cd` from the request, verify that it is in the set of customer codes permitted for the authenticated session user (by querying the `FMS_WEBUSER_CUSTOMER_REL` table or an equivalent access-control table, keyed on `session.getAttribute("user_cd")`). Reject requests where the supplied `cust_cd` is not in the user's permitted set with HTTP 403.

---

### A17-6
**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\Config.java`, `getPermision()` method, line 168
**Severity:** High
**Category:** SQL Injection — Session Attribute Concatenation
**Description:** The `user_cd` value is read from the session and concatenated directly into a SQL query string without parameterization. While session attributes are less directly attacker-controlled than request parameters, if the login process ever stored a user-supplied value without sanitisation, or if the session is compromised, this constitutes a SQL injection vector. The pattern is also structurally unsafe.

**Evidence:**
```java
// Config.java lines 154 and 168:
String user = (String) req.getSession().getAttribute("user_cd");
...
String query = "SELECT distinct form.\"FORM_NAME\", form.\"FORM_CD\", form.\"PRIORITY\" " +
    "FROM " + RuntimeConf.form_table + " as form " +
    "LEFT JOIN " + RuntimeConf.access_rights_table + " as rights ON form.\"FORM_CD\" = rights.\"FORM_CD\" " +
    "LEFT JOIN \"FMS_USR_GRP_REL\" as userrel ON userrel.\"GROUP_CD\" = rights.\"GROUP_CD\" " +
    "WHERE rights.\"VIEW\" is true and rights.\"EDIT\" is true and form.\"PRIORITY\" = '9' and is_reskin='t' AND form.\"MODULE_CD\" = 5 AND userrel.\"USER_CD\" = '" + user + "' ORDER BY form.\"PRIORITY\" ASC";
```

**Recommendation:** Use a `PreparedStatement` with a `?` placeholder for `user_cd`. Parse `user_cd` as an integer before use; if it is not numeric, throw an exception and do not execute the query.

---

### A17-7
**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\Licence.java`, `init()` method, lines 47–53
**Severity:** Medium
**Category:** Authorization — Unrestricted Data Pre-load
**Description:** The `Licence` servlet's `init()` method executes a query that loads ALL customers, sites, and departments from the database at servlet startup — with no access-level restriction. This data is stored in the instance-level `cusList` field. Although `cusList` is not directly served to users in `LicenceServlet` (it references the parent `Config.cusList` for customer/site/dept filtering), the pattern demonstrates a design where full cross-tenant customer topology is loaded eagerly without scoping.

**Evidence:**
```java
// Licence.java lines 47-53:
public void init() {
    String query = "select c.\"USER_CD\", \"USER_NAME\", \"LOC_CD\", \"NAME\", d.\"DEPT_CD\", \"DEPT_NAME\"\r\n"
        + "from \"FMS_CUST_MST\" c right join \"FMS_CUST_DEPT_REL\" r on c.\"USER_CD\" = r.\"USER_CD\" \r\n"
        + "join \"FMS_LOC_MST\" s on r.\"LOC_CD\" = s.\"LOCATION_CD\"\r\n"
        + "join \"FMS_DEPT_MST\" d on r.\"DEPT_CD\" = d.\"DEPT_CD\"\r\n"
        + "order by \"USER_NAME\", \"LOC_CD\", \"DEPT_NAME\"";
    cusList = saveasList(query);
}
```

**Recommendation:** Remove the `init()` pre-load or scope the query to a specific customer. Customer/site/dept enumeration should always be performed at request time, scoped to the authenticated user's permitted customer set.

---

### A17-8
**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\TableServlet.java`, fields `rsList` (line 37) and `Utilisation.java` fields `vehicles` (line 49), `oneDay` (line 52)
**Severity:** Medium
**Category:** Race Condition — Shared Mutable State / Cross-Request Data Leakage
**Description:** `TableServlet` stores the result set `rsList` as an instance variable. Servlet instances are reused across concurrent requests. Under concurrent load, one user's request can overwrite `rsList` while another user's request is iterating it, resulting in either exceptions or one user's query results being returned to another user. `Utilisation.java` has the same problem with `vehicles` and `oneDay` instance fields. This is a data integrity and potential cross-tenant data leakage issue.

**Evidence:**
```java
// TableServlet.java line 37:
LinkedList<HashMap<String, String>> rsList = new LinkedList<HashMap<String, String>>();

// TableServlet.java line 131 (getVORStatus — instance field overwritten per request):
rsList.clear();
rsList = saveasList(query, servlet);

// Utilisation.java lines 49-52:
String vehicles = "";
int thresholdLow = 25, thresholdHigh = 50;
Gson gson = new Gson();
boolean oneDay = false;
```

**Recommendation:** Move `rsList`, `vehicles`, `oneDay`, `thresholdLow`, and `thresholdHigh` to local method variables rather than instance fields. Never store per-request data in servlet instance fields.

---

### A17-9
**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\SessionCleanupListener.java`, `sessionDestroyed()` method, lines 21–29
**Severity:** Low
**Category:** Memory Leak / Incomplete Session Cleanup
**Description:** The `SessionCleanupListener` only calls `Impacts.cleanupSession(sessionId)` on session destruction. The other servlets that use session-keyed `ConcurrentHashMap` stores — `CriticalBattery`, `Preop`, `Utilisation`, and `Licence` — are never cleaned up. Over time, session data for all users who have visited these dashboard pages accumulates in the static maps, leading to a memory leak that grows proportionally with the number of user sessions.

**Evidence:**
```java
// SessionCleanupListener.java lines 22-29:
public void sessionDestroyed(HttpSessionEvent se) {
    String sessionId = se.getSession().getId();
    // Clean up Impacts servlet resources
    Impacts.cleanupSession(sessionId);
    // Add other cleanup calls for other servlets as needed
}
```
Missing calls: `CriticalBattery.cleanupSession(sessionId)`, `Preop.cleanupSession(sessionId)`, `Utilisation.cleanupSession(sessionId)`, `Licence.cleanupSession(sessionId)`.

**Recommendation:** Add the missing `cleanupSession()` invocations for all four affected servlet classes in `sessionDestroyed()`. All four already have `cleanupSession()` static methods implemented; they simply need to be called from the listener.

---

### A17-10
**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\dashboard\Licence.java`, `updateTable()`, lines 198–233; and `getChart()`, lines 80–172
**Severity:** High
**Category:** SQL Injection + Authorization — PII Data Exposure
**Description:** `LicenceServlet.updateTable()` accepts `cust_cd`, `loc_cd`, and `dept_cd` from request parameters at the time of the `update` call (lines 198–200), separate from the initial `chart` call. These are concatenated into `driversQuery` without parameterization or session-scope verification. This allows an authenticated user to supply a different `cust_cd` in the `update` call than in the `chart` call, retrieving driver PII (names, email addresses, phone numbers, licence expiry dates) scoped to a different tenant. This combines SQL injection, broken authorization, and PII exposure.

**Evidence:**
```java
// Licence.java lines 198-222 (updateTable, "without" category branch):
String cust = req.getParameter("cust_cd") == null ? "all" : req.getParameter("cust_cd");
String site = req.getParameter("loc_cd") == null ? "all" : req.getParameter("loc_cd");
String dept = req.getParameter("dept_cd") == null ? "all" : req.getParameter("dept_cd");
String driversQuery = "select u.\"USER_CD\" from \"FMS_USR_MST\" u join \"FMS_USER_DEPT_REL\" r on u.\"USER_CD\" = r.\"USER_CD\" "
    + "where \"ACTIVE\" is true and \"ISDRIVER\" is true and \"CUST_CD\" = " + cust;
// ... concatenation continues for site and dept ...
query = "select 'No expiry date' as expiry_date, concat('Driver ', u.\"USER_CD\") as name, '' as \"VEHICLE_TYPE\", \"EMAIL_ADDR\", \"PHONE_NUMBER\", ..."
    + " from \"FMS_USR_MST\" u join ... where u.\"USER_CD\" in (" + driversQuery + ") ...";
```

**Recommendation:** Apply `PreparedStatement` parameterization to all queries. Validate `cust_cd` against the authenticated session user's permitted customer set before executing any query. Do not accept `cust_cd` as a freely-mutable request parameter in stateful follow-up calls (use the session-stored value instead).

---

## Summary Table

| ID    | Severity | Category                                    | File(s)                              |
|-------|----------|---------------------------------------------|--------------------------------------|
| A17-1 | High     | XSS — JavaScript Injection                  | summary.jsp:254-256                  |
| A17-2 | Medium   | XSS — HTML Attribute Injection              | header_filter.jsp:3-4, header_vor_status.jsp:3-4 |
| A17-3 | Critical | SQL Injection (pervasive)                   | Summary.java, Config.java, CriticalBattery.java, Impacts.java, Licence.java, Preop.java, TableServlet.java, Utilisation.java |
| A17-4 | High     | Race Condition / Cross-Tenant Data Exposure | Config.java:29,59,75-91             |
| A17-5 | High     | Authorization — Missing Tenant Enforcement  | summary.jsp:5-7, Summary.java (all methods) |
| A17-6 | High     | SQL Injection — Session Attribute           | Config.java:168                      |
| A17-7 | Medium   | Authorization — Unrestricted Data Pre-load  | Licence.java:47-53                   |
| A17-8 | Medium   | Race Condition — Instance-Level Mutable State | TableServlet.java:37, Utilisation.java:49-52 |
| A17-9 | Low      | Memory Leak / Incomplete Session Cleanup    | SessionCleanupListener.java:21-29    |
| A17-10| High     | SQL Injection + Authorization + PII Exposure | Licence.java:198-233                |

**Total findings: 10**
