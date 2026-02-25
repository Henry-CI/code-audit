# Audit A08 — reports / dashboard / service / businessinsight / jsonbinding packages
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Auditor:** Agent A08
**Scope:** All .java files under the following packages:
- `WEB-INF/src/com/torrent/surat/fms6/reports/`
- `WEB-INF/src/com/torrent/surat/fms6/dashboard/`
- `WEB-INF/src/com/torrent/surat/fms6/rtls/` (none found)
- `WEB-INF/src/com/torrent/surat/fms6/service/`
- `WEB-INF/src/com/torrent/surat/fms6/businessinsight/`
- `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/`
- `WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/`

**Total findings: 18**

---

## Files Catalogued

| File | Lines | Notes |
|------|-------|-------|
| reports/Reports.java | 608 | Base class; Statement-based SQL throughout |
| reports/Databean_report.java | 21,854 | Too large to read in full; grepped for patterns |
| reports/Databean_report1.java | 817 | Fully read |
| reports/Databean_reports.java | 127 | Fully read; stub/empty class |
| reports/Databean_dyn_reports.java | 10,015 | Too large to read in full; grepped for patterns |
| reports/Databean_cdisp.java | 1,747 | Too large to read in full; grepped for patterns |
| reports/LinderReportDatabean.java | 1,935 | Too large to read in full; grepped for patterns |
| reports/RTLSHeatMapReport.java | 525 | Fully read; PreparedStatement used correctly |
| reports/RTLSImpactReport.java | 1,262 | Fully read; mostly PreparedStatement |
| reports/UtilBean.java | 71 | Fully read; POJO only |
| reports/UtilModelBean.java | 65 | Fully read; POJO only |
| dashboard/Config.java | — | Fully read |
| dashboard/Summary.java | — | Fully read |
| dashboard/Impacts.java | — | Fully read |
| dashboard/TableServlet.java | — | Fully read |
| dashboard/CriticalBattery.java | — | Fully read |
| dashboard/Licence.java | — | Fully read |
| dashboard/Preop.java | — | Fully read |
| dashboard/Utilisation.java | — | Fully read |
| dashboard/SessionCleanupListener.java | — | Fully read |
| service/HireDehireService.java | 127 | Fully read |
| businessinsight/BusinessInsight.java | — | Fully read |
| businessinsight/BusinessInsightBean.java | ~53.5 KB | Too large to read in full; grepped for patterns |
| businessinsight/BusinessInsightExcel.java | — | Fully read |
| jsonbinding/preop/PreOpQuestions.java | — | Fully read; POJO only |
| jsonbinding/preop/Question.java | — | Fully read; POJO only |

---

## Findings

---

### A08-1 — SQL Injection in Reports.java (Base Class)

**File:** `WEB-INF/src/com/torrent/surat/fms6/reports/Reports.java`
**Lines:** 63, 124, 127, 191, 200, 276–285
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
The base class `Reports` contains four methods — `Fetch_customers()`, `Fetch_cust_locations()`, `Fetch_cust_depts()`, and `Fetch_cust_veh()` — that construct SQL queries by directly concatenating session and request-derived values into SQL strings using `java.sql.Statement`. No parameterisation is used in any of these methods. Because `Reports` is the base class extended by all report databean classes, this pattern propagates throughout the entire reports subsystem.

**Evidence:**
```java
// Fetch_customers() — Line 63
query += " where \"USER_CD\" = " + access_cust;

// Fetch_cust_locations() — Line 124
+ " where \"USER_CD\" = "+set_cust_cd;
// Line 127
query += " and \"LOCATION_CD\" = " + access_site;

// Fetch_cust_depts() — Line 191
dep_lst = " and \"FMS_CUST_DEPT_REL\".\"DEPT_CD\" in ("+access_dept+") ";
// Line 200
cond_cust="  \"FMS_CUST_DEPT_REL\".\"USER_CD\" = '"+set_cust_cd+"'";

// Fetch_cust_veh() — Lines 276–285
" where \"USER_CD\" = '"+set_cust_cd+"'";
query += " and \"LOC_CD\" = '"+set_loc_cd+"'";
query += " and \"DEPT_CD\" = '"+set_dept_cd+"'";
```

The only method in `Reports.java` that correctly uses a `PreparedStatement` is `getVehTag()` (line 349–353).

**Recommendation:**
Replace all `Statement` usage with `PreparedStatement` and bind each parameter with the appropriate `setString()` / `setInt()` call. This applies to all four affected methods and to every subclass that inherits the same pattern.

---

### A08-2 — SQL Injection in Databean_report.java (Pervasive)

**File:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java`
**Lines:** Widespread throughout 21,854-line file
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`Databean_report.java` is the largest file in the codebase (21,854 lines). Grep analysis confirms hundreds of `stmt.executeQuery(query)` calls where `query` is assembled by concatenating `set_cust_cd`, `set_loc_cd`, `set_dept_cd`, `st_dt`, `to_dt`, `end_dt`, `set_sc`, and `access_dept` directly into SQL strings via `java.sql.Statement`. No `PreparedStatement` usage was found for any of these parameterised queries. The file extends `Reports` and therefore inherits the same base-class patterns identified in A08-1.

**Evidence (representative grep hits):**
```java
// Typical pattern repeated throughout:
stmt = conn.createStatement();
query = "select ... where \"USER_CD\" = '" + set_cust_cd + "' ...";
rset = stmt.executeQuery(query);

// Date parameters embedded in SQL literals:
"where \"DATE_TIME\" >= timestamp '" + st_dt + "' and \"DATE_TIME\" <= timestamp '" + to_dt + "'"

// access_dept in IN clause:
" and \"DEPT_CD\" in (" + access_dept + ")"

// Search criteria (set_sc) in ILIKE:
" and (\"HIRE_NO\" ilike '%" + set_sc + "%' or \"SERIAL_NO\" ilike '%" + set_sc + "%')"
```

**Recommendation:**
Refactor all query construction in this class to use `PreparedStatement`. Date parameters must be bound as `Timestamp` objects, not embedded in SQL string literals.

---

### A08-3 — SQL Injection in Databean_report1.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java`
**Lines:** 154, 173–174, 188, 245–246
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`Databean_report1.java` constructs SQL queries by concatenating request-derived parameters directly into SQL strings. The `Fetch_users()` method concatenates `set_gp_cd` and `set_user_cd` from HTTP request parameters into WHERE clauses. The `Fetch_Data()` method concatenates `set_user_cd`, `st_dt`, and `end_dt` into a date-range query. A multi-step flow builds an `IN` clause by first querying group members and then embedding those values unvalidated into a second query.

**Evidence:**
```java
// Line 154 — set_gp_cd from request, concatenated unquoted
query = "select \"USER_CD\" from \"FMS_USR_GRP_REL\" where \"GROUP_CD\"='"+set_gp_cd+"'";

// Lines 173–174 — user_cd list built from prior results, concatenated into IN clause
query = "select \"USER_CD\", \"CONTACT_FIRST_NAME\", \"CONTACT_LAST_NAME\", \"EMAIL\" "
      + "from \"FMS_USR_MST\" where \"USER_CD\" in ("+ucd_str+")";

// Line 188 — set_user_cd from request
query = "select ... from \"FMS_USR_MST\" where \"USER_CD\"='"+set_user_cd+"'";

// Lines 245–246 — st_dt, end_dt, set_user_cd concatenated into date-range query
"where \"DRIVER_CD\" = '"+set_user_cd+"' and to_date(to_char(\"DATE_TIME\"...), '"+st_dt+"'..."
```

There is no customer/tenant scope enforcement — any authenticated user can query any driver's data by manipulating `set_user_cd`.

**Recommendation:**
Use `PreparedStatement` for all queries. Enforce that the requested `set_user_cd` belongs to the authenticated session's customer before executing the query.

---

### A08-4 — SQL Injection in Databean_dyn_reports.java (Pervasive)

**File:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java`
**Lines:** Widespread throughout 10,015-line file
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`Databean_dyn_reports.java` contains extensive SQL injection across its 10,015 lines. Grep analysis identified numerous instances where `set_dept_cd`, `set_loc_cd`, `set_cust_cd`, `set_sc`, and dynamic field codes are concatenated into SQL queries executed via `java.sql.Statement`.

**Evidence (representative grep hits):**
```java
// Line 578 — set_dept_cd unquoted (integer-style injection)
query = "select \"DEPT_NAME\" from \"FMS_DEPT_MST\" where \"DEPT_CD\"="+set_dept_cd;

// Line 3111 — set_loc_cd unquoted in geofence query
query += " and gf.site_cd = " + set_loc_cd;

// Lines 3692, 3705, 4734, 4747 — set_cust_cd unquoted
"AND uv.\"CUST_CD\" = " + set_cust_cd + " "

// Lines 2239, 2303, 2373 — field_cd from loop variable concatenated
String queryExt = " and field_cd = '" + tmp_fnm + "' ";
queryExt = " and field_cd in (" + tmp_fnm + ") ";

// Lines 1968–1969 — set_sc (search criteria) in ILIKE
cond_sc = " and (\"HIRE_NO\" ilike '%" + set_sc + "%' or \"SERIAL_NO\" ilike '%" + set_sc + "%')";
```

**Recommendation:**
Full refactor to `PreparedStatement` is required. Dynamic field code loops must validate field codes against a whitelist before interpolation.

---

### A08-5 — SQL Injection in Databean_cdisp.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java`
**Lines:** 155–164, 168, 210, 235–244, 296–302, 814, 866, 908–909
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`Databean_cdisp.java` concatenates `access_cust`, `access_site`, `access_dept`, `set_cust_cd`, and `set_gmtp_id` directly into SQL strings executed via `java.sql.Statement`. All queries in this file use `Statement`; no `PreparedStatement` usage was found. The `set_gmtp_id` parameter is particularly dangerous as it is used to construct queries against the `FMS_GPSE_DATA` table (GPS/telematics data), meaning an injection here could expose or manipulate location tracking records across all customers.

**Evidence:**
```java
// Lines 155–164 — access_cust, access_site, access_dept concatenated into IN clauses
cond_relation = " AND \"USER_CD\" in ("+ access_cust +")";
cond_relation += " AND \"LOC_CD\" in ("+access_site+") ";
cond_relation += " AND \"DEPT_CD\" in ("+access_dept+") ";

// Line 168 — set_cust_cd quoted but still injectable
query = "select \"VEHICLE_CD\" from \"FMS_USR_VEHICLE_REL\" where \"USER_CD\" ='" + set_cust_cd + "' " + cond_relation;

// Lines 908–909 — set_gmtp_id in GPS data query
"where \"VEHICLE_CD\"='"+set_gmtp_id+"' and \"UNIXTIME\" in"
+"(select max(\"UNIXTIME\") from \"FMS_GPSE_DATA\" where \"VEHICLE_CD\" = '"+set_gmtp_id+"' )";
```

**Recommendation:**
Use `PreparedStatement` for all queries. The GPS query at lines 908–909 is particularly high-risk and should be prioritised.

---

### A08-6 — SQL Injection in LinderReportDatabean.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/reports/LinderReportDatabean.java`
**Lines:** 216–217, 338–339, 426–427, 524, 570, 633, 715–717, 818–820
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`LinderReportDatabean.java` concatenates `customerCd`, `locationCd`, `st_dt`, and `end_dt` directly into SQL strings executed via `java.sql.Statement`. The `locationCd` value is split on `-` and each component is then concatenated into separate queries per loop iteration — bypassing any potential validation of the original combined value. Date parameters `st_dt` and `end_dt` are embedded directly into PostgreSQL `timestamp` cast expressions.

**Evidence:**
```java
// Lines 216–217 — customerCd and locationCd concatenated (customer-scoped but unparameterised)
cond_cust = " \"USER_CD\" = '"+customerCd+"'";
cond_site = " and \"LOC_CD\" = '" + locArray[i] + "'";

// Lines 524, 570 — st_dt and end_dt in timestamp literals
+ " and unlocked_utc_time >= '"+st_dt+"'::timestamp and unlocked_utc_time < '"+end_dt+"'::timestamp + interval '1 day' "

// Lines 715–717, 818–820 — date range in more complex queries
+ " '"+st_dt+"'::timestamp "
+ " '"+end_dt+"'::timestamp + interval '1 day' "
```

**Recommendation:**
Use `PreparedStatement` with `setTimestamp()` for all date parameters. Replace all string concatenation for `customerCd` and `locationCd` with parameterised placeholders.

---

### A08-7 — SQL Injection in dashboard/Config.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java`
**Lines:** 41–44, 168
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`Config.java` is a static utility class used by all dashboard servlets to build the shared customer/site/department filter condition. The `cust`, `site`, and `dept` parameters are read directly from `req.getParameter()` and concatenated unquoted into an SQL condition string that is then appended to every dashboard query. Because this class is shared, a single injection point here affects every dashboard servlet (`Summary`, `Impacts`, `TableServlet`, `CriticalBattery`, `Licence`, `Preop`, `Utilisation`). The `saveasList(String query)` utility method (used internally) executes any raw SQL string passed to it via `Statement`, amplifying the impact.

**Evidence:**
```java
// Lines 41–44 — cust, site, dept from req.getParameter(), concatenated unquoted
if (level > 1 && !cust.equals("all"))
    condition = " where c.\"USER_CD\" in (" + cust +" ) ";
if (user != null && cust == LindeConfig.customerLinde)
    condition += "or c.\"USER_CD\" in (select ... where \"USER_CD\" = " + user + ")";
if (level > 2 && !site.equals("all"))
    condition += " and \"LOC_CD\" = " + site;
if (level > 3 && !dept.equals("all"))
    condition += " and d.\"DEPT_CD\" = " + dept;

// Line 168 — user (from session) still concatenated
"AND userrel.\"USER_CD\" = '" + user + "'"
```

**Recommendation:**
Refactor `Config` to return a parameterised query fragment (e.g., a record containing the SQL skeleton with `?` placeholders and a list of bound values). All dashboard servlets must then bind those values through `PreparedStatement`. Integer parameters such as `USER_CD`, `LOC_CD`, and `DEPT_CD` should be validated as integers before any use.

---

### A08-8 — SQL Injection in dashboard/Summary.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Summary.java`
**Lines:** 100–101, 196
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`Summary.java` (`@WebServlet("/Servlet/SummaryServlet")`) contains multiple handler methods (`getBattery`, `getPreop`, `getImpactChart`, `getUtilisation`, `getLicence`, `getImpact`, `getUnit`, `getDriver`) each of which reads `cust_cd`, `loc_cd`, `dept_cd`, `st_dt`, and `to_dt` from HTTP request parameters and concatenates them directly into SQL queries. Date values `st_dt` and `to_dt` are embedded in PostgreSQL `timestamp` literals, enabling SQL injection via date-format manipulation.

**Evidence:**
```java
// Line 100 — cust from request, unquoted integer injection
+ "where \"IS_UNIT\" is true and lowutil = FALSE and \"USER_CD\" = " + cust;

// Line 101 — site and dept from request
+ " and \"LOC_CD\" = " + site + " and \"DEPT_CD\" = " + dept;

// Line 196 — st_dt, to_dt from request in timestamp literals
"where starttimestamp >= timestamp '" + st_dt + "' and starttimestamp <= timestamp '" + to_dt + "'"
```

**Recommendation:**
Use `PreparedStatement` for all queries. Bind `cust_cd`, `loc_cd`, `dept_cd` as integers; bind `st_dt` and `to_dt` as `Timestamp` objects via `setTimestamp()`.

---

### A08-9 — SQL Injection in dashboard/Impacts.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Impacts.java`
**Lines:** 111, 171–172, 187–199
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`Impacts.java` (`@WebServlet("/Servlet/ImpactsServlet")`) reads `cust`, `startTime`, and `endTime` from HTTP request parameters and concatenates them into SQL queries. The `startTime` and `endTime` values are embedded directly into PostgreSQL `timestamp` literals, and also into `generate_series()` expressions used for time-bucketing — a more complex injection context that could manipulate interval arithmetic.

**Evidence:**
```java
// Line 111 — cust from request, unquoted
String vehiclesQuery = "select \"VEHICLE_CD\" from \"FMS_USR_VEHICLE_REL\" where \"USER_CD\" = " + cust;

// Lines 171–172 — startTime, endTime from request in timestamp literals
"where \"DATE_TIME\" >= timestamp ' " + startTime + "' and \"DATE_TIME\" <= timestamp '" + endTime + "'"

// Lines 187–199 — startTime, endTime in generate_series()
"generate_series(timestamp '" + startTime + "', timestamp '" + endTime + "', '1 hour'::interval)"
```

**Recommendation:**
Use `PreparedStatement` and `setTimestamp()` for all temporal parameters. Validate that `cust` is an integer before use.

---

### A08-10 — SQL Injection in dashboard/TableServlet.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/TableServlet.java`
**Lines:** 109, 304–309, 374–375, 380–395
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`TableServlet.java` (`@WebServlet("/Servlet/TableServlet")`) concatenates `search`, `cust`, `site`, `dept`, `startTime`, `endTime`, and `drivers` from HTTP request parameters into SQL queries. The `search` parameter is inserted into `ILIKE` patterns without escaping. A particularly dangerous secondary injection exists at lines 374–375: values returned from a preliminary database query (`rs.getString(1)` containing `field_cd` and `name` containing field descriptions) are directly interpolated back into a second SQL query, creating a second-order SQL injection vulnerability if the `FMS_VEHICLE_FIELD_DEF` table is compromised or if `field_cd` values are attacker-controlled.

**Evidence:**
```java
// Line 109 — search from request in ILIKE (no escaping of %, _, \)
vehiclesQuery += " and (lower(\"HIRE_NO\") like lower('%" + search + "%') ...)";

// Lines 304–309 — search from request in ILIKE on driver table
driversQuery += " and (\"CONTACT_LAST_NAME\" ilike '%" + search + "%' ...)";

// Lines 374–375 — DB-returned field_cd and name interpolated into SQL (second-order injection)
fields += ", sum(case when field_cd = " + rs.getString(1) + " then data_stop else 0 end) as \"" + name + "\"";
columns += ", to_char((\"" + name + "\"/10||'s')::interval, 'HH24:mi:ss') as \"" + name + "\"";

// Lines 393–395 — startTime, endTime, drivers from request
"where starttimestamp >= timestamp '" + startTime + "' and starttimestamp <= timestamp '" + endTime + "'"
+ " and \"DRIVER_CD\" in (" + drivers + ")"
```

**Recommendation:**
Use `PreparedStatement` for all user-controlled parameters. For the ILIKE patterns, use `setString()` with `%` prepended/appended in Java (not in SQL). For the dynamic column construction from DB-returned values, validate `field_cd` values against an integer whitelist and sanitise column alias names to alphanumeric characters only before embedding in SQL.

---

### A08-11 — SQL Injection in dashboard/CriticalBattery.java, Licence.java, Preop.java, Utilisation.java

**Files:**
- `WEB-INF/src/com/torrent/surat/fms6/dashboard/CriticalBattery.java` (lines 104–106, 129, 148)
- `WEB-INF/src/com/torrent/surat/fms6/dashboard/Licence.java` (lines 95–100, 201–212)
- `WEB-INF/src/com/torrent/surat/fms6/dashboard/Preop.java` (lines 103–105, 129)
- `WEB-INF/src/com/torrent/surat/fms6/dashboard/Utilisation.java` (lines 138–143, 177–190)

**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
All four remaining dashboard servlets follow the identical pattern as `Summary.java` and `Impacts.java`: HTTP request parameters `cust`, `site`, `dept`, `startTime`, and `endTime` are concatenated directly into SQL queries without parameterisation. Each servlet independently builds its own vehicle/driver filter subqueries and date-range conditions using string concatenation.

**Evidence (representative from each file):**
```java
// CriticalBattery.java — Lines 104–106
String vehiclesQuery = "... where \"USER_CD\" = " + cust;
vehiclesQuery += " and \"LOC_CD\" = " + site;
vehiclesQuery += " and \"DEPT_CD\" = " + dept;
// Lines 129, 148
"where ... >= timestamp '" + startTime + "' and ... <= timestamp '" + endTime + "'"

// Licence.java — Lines 95–100
String driversQuery = "... where \"USER_CD\" = " + cust;
driversQuery += " and \"LOC_CD\" = " + site;
driversQuery += " and \"DEPT_CD\" = " + dept;

// Preop.java — Lines 103–105 (same cust/site/dept pattern)
// Utilisation.java — Lines 138–143 (same cust/site/dept pattern, complex date range at 177–190)
```

**Recommendation:**
Same as A08-8 and A08-9. A shared parameterised query builder (refactoring `Config.java`) should be used consistently across all dashboard servlets, eliminating this class of vulnerability at the root.

---

### A08-12 — SQL Injection in service/HireDehireService.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java`
**Lines:** 24–25, 37–38, 50–51, 66–69, 75–77
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`HireDehireService.getUnitsHireDehireTime()` constructs a `UNION ALL` query by concatenating `custCd`, `locCd`, `deptCd`, `searchCrit`, and `vehTypeCd` directly into SQL strings. All five parameters are unparameterised. A `Pattern`-based check at line 55 gates the `searchCrit` injection only for the letters-only case — when `searchCrit` contains digits or special characters (e.g., a hire number), it is still concatenated directly. The pattern check is therefore an incomplete mitigation, not a fix.

**Evidence:**
```java
// Lines 24–25 — custCd concatenated unquoted (integer injection)
String relCond = " where fuvr.\"USER_CD\" = " + custCd;
String relHistoryCond = " where fuvrh.\"USER_CD\" = " + custCd;

// Lines 37–38 — locCd unquoted
relCond += " fuvr.\"LOC_CD\" = " + locCd;
relHistoryCond += " fuvrh.\"LOC_CD\" = " + locCd;

// Lines 50–51 — deptCd unquoted
relCond += " fuvr.\"DEPT_CD\" = " + deptCd;
relHistoryCond += " fuvrh.\"DEPT_CD\" = " + deptCd;

// Lines 66–69 — searchCrit concatenated when non-alpha (partial mitigation only)
relCond += " (lower(fvm.\"HIRE_NO\") like lower('%" + searchCrit.trim().toLowerCase() + "%') ...)";

// Lines 75–77 — vehTypeCd unquoted
vehTypeMstrJoinCond = " inner join \"FMS_VEHICLE_TYPE_MST\" as fvtm on fvtm.\"VEHICLE_TYPE_CD\" = fvm.\"VEHICLE_TYPE_CD\" "
                    + "and fvtm.\"VEHICLE_TYPE_CD\" = " + vehTypeCd;
```

**Recommendation:**
Use `PreparedStatement` for the entire query. The `UNION ALL` structure can still be parameterised — bind each clause's parameters separately. Remove the partial pattern-check mitigation and replace it with proper parameterisation.

---

### A08-13 — SQL Injection in businessinsight/BusinessInsightBean.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java`
**Lines:** 209–211, 332–334, 467–470, 524, 570
**Severity:** Critical
**Category:** SQL Injection (CWE-89)

**Description:**
`BusinessInsightBean.java` concatenates `customerCd`, `locationCd`, `st_dt`, and `end_dt` — all sourced from HTTP request parameters via `BusinessInsight.java` — directly into SQL queries executed via `java.sql.Statement`. Multiple query methods (for utilisation, pre-op, impact, and model reports) share this pattern. The `locationCd` field is split on `-` and each fragment is separately concatenated, bypassing any format assumption about the original value.

**Evidence:**
```java
// Lines 209–211 — customerCd and locationCd concatenated unquoted
+ " r.\"USER_CD\" = " + customerCd
+ "  and r.\"LOC_CD\" = " + locationCd;

// Lines 332–334 — same pattern in second query method
+ " r.\"USER_CD\" = " + customerCd
+ "  and r.\"LOC_CD\" = " + locationCd + " order by t.\"VEHICLE_TYPE\" ";

// Lines 253–254 — st_dt and end_dt in timestamp literals
query = "select rec_no from \"fms_io_data\" where \"vehicle_cd\"="+uBean.getVeh_cd()
      + " and \"utc_time\" >= '" + st_dt + "'::timestamp and \"utc_time\" < '" + end_dt + "'::timestamp";
```

**Recommendation:**
Refactor all data access in this class to use `PreparedStatement`. `BusinessInsight.java` must validate that `cust_cd` from the request matches the authenticated session's authorised customer before passing to `BusinessInsightBean`.

---

### A08-14 — Missing Customer-Scope Enforcement in Dashboard Servlets (Broken Object-Level Authorization)

**Files:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java`, `Summary.java`, `Impacts.java`, `TableServlet.java`, `CriticalBattery.java`, `Licence.java`, `Preop.java`, `Utilisation.java`
**Lines:** Config.java lines 41–44; all dashboard servlet doGet/doPost handlers
**Severity:** High
**Category:** Broken Object-Level Authorization (CWE-639)

**Description:**
All dashboard servlets read `cust_cd` (customer code), `loc_cd` (location code), and `dept_cd` (department code) directly from HTTP request parameters and use them as the primary data-access scope. There is no verification that the requested `cust_cd` matches the authenticated session user's authorised customers. A low-privilege user who knows or can guess another customer's code can supply it as a request parameter and receive data belonging to that other customer. The `access_level` / `access_cust` session variables set in `Config.java` are used to restrict query results, but only when `level > 1` — if `access_level` is not set or defaults to `1`, no restriction is applied.

**Evidence:**
```java
// Config.java — Lines 41–44: cust, site, dept from request; restriction only when level > 1
String cust = req.getParameter("cust_cd");
String site = req.getParameter("loc_cd");
String dept = req.getParameter("dept_cd");
if (level > 1 && !cust.equals("all"))
    condition = " where c.\"USER_CD\" in (" + cust +" ) ";
// No else branch: if level == 1 (default), no WHERE clause is added → all customers returned
```

**Recommendation:**
Validate request parameters `cust_cd`, `loc_cd`, and `dept_cd` against the authenticated session's authorised scope on every request. Reject requests where the supplied `cust_cd` does not appear in the session's authorised customer list. Never use client-supplied scope parameters as the sole access control gate.

---

### A08-15 — Customer-Scope Not Enforced in RTLSImpactReport.getRedImpact()

**File:** `WEB-INF/src/com/torrent/surat/fms6/reports/RTLSImpactReport.java`
**Lines:** 981–986
**Severity:** High
**Category:** Broken Object-Level Authorization (CWE-639)

**Description:**
`RTLSImpactReport.getRedImpact()` builds a vehicle list via `getRTLSVehLst()` and then constructs an `IN` clause from all returned vehicles. The grep and read analysis shows that `getRTLSVehLst()` queries RTLS-enabled vehicles without filtering by the currently authenticated customer. The outer `getRedImpact()` query then fetches impact records (`FMS_FORCE_MSG`) for that unscoped vehicle list. An attacker who can invoke this report may receive impact data for vehicles belonging to other customers.

Note: All individual database queries within `RTLSImpactReport` correctly use `PreparedStatement` for their parameterised portions — the scope issue is at the vehicle-list construction level rather than injection.

**Evidence:**
```java
// Lines 981–986 — unitLst from getRTLSVehLst() (no customer scope filter), used in IN clause
String query = "select shock_id,location_cached,speed_cached, \"VEHICLE_CD\",..."
    + " from \"FMS_FORCE_MSG\""
    + " where \"VEHICLE_CD\" in ("+unitLst+")"
    + " and \"SEVERITY\" = 'Red' ...";
```

**Recommendation:**
Ensure `getRTLSVehLst()` filters by the authenticated session's `access_cust` value. Add an explicit `AND "USER_CD" = ?` (or equivalent customer scope join) to all impact queries in this class.

---

### A08-16 — Incomplete Session Cleanup Listener

**File:** `WEB-INF/src/com/torrent/surat/fms6/dashboard/SessionCleanupListener.java`
**Lines:** Full class
**Severity:** Medium
**Category:** Resource Management / Session Data Leakage (CWE-404)

**Description:**
`SessionCleanupListener` implements `HttpSessionListener` and calls `Impacts.cleanupSession(sessionId)` on session destruction. However, `CriticalBattery`, `Licence`, `Preop`, and `Utilisation` all use session-scoped `ConcurrentHashMap` data structures to cache query results (per evidence of session-keyed storage in those servlets), but none of their cleanup methods are called from the listener. When a user session expires, cached data belonging to that session remains in memory indefinitely in those four servlets, causing both a memory leak and a potential data exposure if a new session reuses the same session ID.

**Evidence:**
```java
// SessionCleanupListener.java — only Impacts is cleaned up
@Override
public void sessionDestroyed(HttpSessionEvent se) {
    String sessionId = se.getSession().getId();
    Impacts.cleanupSession(sessionId);
    // CriticalBattery.cleanupSession(), Licence.cleanupSession(),
    // Preop.cleanupSession(), Utilisation.cleanupSession() — NOT CALLED
}
```

**Recommendation:**
Add cleanup calls for all session-caching servlets in `sessionDestroyed()`. Alternatively, use the standard `HttpSession.setAttribute()` / `HttpSession.removeAttribute()` mechanism to store per-session data so the servlet container handles cleanup automatically on session destruction.

---

### A08-17 — Wildcard Imports in SQL-Heavy Classes

**Files:**
- `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java` (lines 1–4: `import java.sql.*;`, `import java.util.*;`)
- `WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java` (lines 6–7: `import java.sql.*;`, `import java.util.*;`)

**Severity:** Low
**Category:** Code Quality / Import Hygiene

**Description:**
Both `Databean_report1.java` and `Databean_cdisp.java` use wildcard imports for `java.sql.*` and `java.util.*`. In the context of SQL injection mitigation, wildcard imports for `java.sql.*` can obscure whether `Statement` or `PreparedStatement` is being used, making code reviews and security audits harder. Explicit imports make the use of `Statement` (the insecure choice) immediately visible in the import list.

**Evidence:**
```java
// Databean_report1.java — Lines 1–4
import java.sql.*;
import java.util.*;

// Databean_cdisp.java — Lines 6–7
import java.sql.*;
import java.util.*;
```

**Recommendation:**
Replace with explicit imports. During the SQL injection remediation effort (A08-1 through A08-6), replace `import java.sql.*` with specific imports for `java.sql.Connection`, `java.sql.PreparedStatement`, `java.sql.ResultSet`, `java.sql.SQLException`, and `java.sql.Timestamp` (removing `java.sql.Statement` entirely).

---

### A08-18 — Stack Trace Leakage via System Output

**Files:** All files in scope
**Severity:** Low
**Category:** Information Disclosure (CWE-209)

**Description:**
Every file in scope uses `exception.printStackTrace()` or `e.printStackTrace()` as the sole error-handling mechanism in catch blocks. In a production environment (`release/UAT_RELEASE_FLEETFOCUS_Production` branch), stack traces written to standard output or standard error may appear in server logs, in HTTP responses (if the servlet container maps stderr to the response), or in monitoring systems accessible to operators. Stack traces can reveal internal class names, method signatures, database schema details, and file paths — all of which aid an attacker in understanding the application's internals.

**Evidence (representative — pattern appears in every file):**
```java
// Reports.java — Line 77
} catch (Exception exception) {
    exception.printStackTrace();
}

// HireDehireService.java — Lines 113, 121
} catch (Exception e) {
    e.printStackTrace();
} catch (SQLException e) {
    e.printStackTrace();
}

// Config.java, Summary.java, Impacts.java, TableServlet.java,
// CriticalBattery.java, Licence.java, Preop.java, Utilisation.java,
// Databean_report1.java, BusinessInsightBean.java — same pattern throughout
```

**Recommendation:**
Replace `e.printStackTrace()` with structured logging via the existing `org.apache.logging.log4j.Logger` (already imported in `Reports.java` as `log`). Use `log.error("Descriptive message", e)` to capture the exception in logs without exposing it to end-users or uncontrolled output streams. Configure the servlet container to suppress raw stack traces in HTTP error responses.

---

## Summary Table

| ID | File(s) | Severity | Category |
|----|---------|----------|----------|
| A08-1 | reports/Reports.java | Critical | SQL Injection |
| A08-2 | reports/Databean_report.java | Critical | SQL Injection |
| A08-3 | reports/Databean_report1.java | Critical | SQL Injection |
| A08-4 | reports/Databean_dyn_reports.java | Critical | SQL Injection |
| A08-5 | reports/Databean_cdisp.java | Critical | SQL Injection |
| A08-6 | reports/LinderReportDatabean.java | Critical | SQL Injection |
| A08-7 | dashboard/Config.java | Critical | SQL Injection |
| A08-8 | dashboard/Summary.java | Critical | SQL Injection |
| A08-9 | dashboard/Impacts.java | Critical | SQL Injection |
| A08-10 | dashboard/TableServlet.java | Critical | SQL Injection (incl. second-order) |
| A08-11 | dashboard/CriticalBattery.java, Licence.java, Preop.java, Utilisation.java | Critical | SQL Injection |
| A08-12 | service/HireDehireService.java | Critical | SQL Injection |
| A08-13 | businessinsight/BusinessInsightBean.java | Critical | SQL Injection |
| A08-14 | dashboard/* (all servlets) | High | Broken Object-Level Authorization |
| A08-15 | reports/RTLSImpactReport.java | High | Broken Object-Level Authorization |
| A08-16 | dashboard/SessionCleanupListener.java | Medium | Resource Management / Session Leakage |
| A08-17 | reports/Databean_report1.java, Databean_cdisp.java | Low | Code Quality (Wildcard Imports) |
| A08-18 | All files in scope | Low | Information Disclosure (Stack Traces) |

## Areas with No Findings

- **reports/RTLSHeatMapReport.java** — All database queries use `PreparedStatement` correctly. No injection found.
- **reports/RTLSImpactReport.java** — All parameterised queries use `PreparedStatement`. One authorization scope issue noted (A08-15).
- **reports/UtilBean.java**, **reports/UtilModelBean.java** — Pure POJOs, no database access.
- **reports/Databean_reports.java** — Stub/empty class with no active queries.
- **jsonbinding/preop/PreOpQuestions.java**, **jsonbinding/preop/Question.java** — Pure POJOs used for JSON deserialization. No dynamic typing annotations (`@JsonTypeInfo`, etc.) found. No security issues.
- **businessinsight/BusinessInsight.java** — Servlet entry point only; no direct SQL. Passes unvalidated parameters to `BusinessInsightBean` (risk addressed in A08-13 and A08-14).
- **businessinsight/BusinessInsightExcel.java** — Apache POI Excel generation; no SQL. File path derived from class location, not user input.
- **No command injection found** — No `Runtime.getRuntime().exec()`, `ProcessBuilder`, or `ScriptEngine` usage detected in any in-scope file.
- **No SSRF found** — RTLS classes connect only to databases via `DBUtil`; no user-controlled URLs used in HTTP connections.
- **No unsafe JSON deserialization found** — Gson used without polymorphic type handling; `org.json` used for RTLS JSON construction.
