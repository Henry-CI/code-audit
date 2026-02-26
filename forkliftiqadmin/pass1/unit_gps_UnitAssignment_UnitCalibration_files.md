# Security Audit Report
## Files: unit.gps.jsp, UnitAssignmentBean, UnitCalibration* Classes
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master
**Date:** 2026-02-26
**Pass:** 1

---

## Scope

Files audited in this pass:

1. `src/main/webapp/gps/unit.gps.jsp`
2. `src/main/java/com/bean/UnitAssignmentBean.java`
3. `src/main/java/com/calibration/UnitCalibration.java`
4. `src/main/java/com/calibration/UnitCalibrationEnder.java`
5. `src/main/java/com/calibration/UnitCalibrationEnderInDatabase.java`
6. `src/main/java/com/calibration/UnitCalibrationGetter.java`
7. `src/main/java/com/calibration/UnitCalibrationGetterInDatabase.java`
8. `src/main/java/com/calibration/UnitCalibrationImpactFilter.java`
9. `src/main/java/com/calibration/UnitCalibrationStarter.java`
10. `src/main/java/com/calibration/UnitCalibrationStarterInDatabase.java`
11. `src/main/java/com/calibration/UnitCalibrator.java`

Supporting context files also examined during analysis:

- `src/main/java/com/action/CalibrationAction.java`
- `src/main/java/com/action/AdminUnitImpactAction.java`
- `src/main/java/com/action/AdminUnitAction.java`
- `src/main/java/com/action/GetAjaxAction.java`
- `src/main/java/com/calibration/CalibrationJob.java`
- `src/main/java/com/calibration/CalibrationJobScheduler.java`
- `src/main/java/com/dao/GPSDao.java`
- `src/main/java/com/dao/UnitDAO.java`
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/WEB-INF/web.xml`

---

## Findings

---

### CRITICAL: XSS via Unescaped Database Strings Injected into JSON/JavaScript in GPS Response

**File:** `src/main/java/com/dao/GPSDao.java` (line 64–65); rendered by `src/main/webapp/gps/unit.gps.jsp` (line 30)

**Description:**

`GPSDao.getUnitGPSData()` builds a raw JSON string by directly concatenating database-sourced string values — `vehName`, `manufacturer`, `type`, and `power` — with no HTML or JavaScript escaping applied:

```java
// GPSDao.java lines 64-65
String gps_str = "{\"name\":\"" + unitBean.getVehName()
    + "\",\"status\":1,\"lat\":" + unitBean.getLatitude()
    + ",\"lon\":" + unitBean.getLongitude()
    + ",\"manufacturer\":\"" + unitBean.getManufacturer()
    + "\",\"time\":\"" + DateUtil.formatDateTime(...)
    + "\",\"type\":\"" + unitBean.getType()
    + "\",\"power\":\"" + unitBean.getPower()
    + "\",\"ingeofence\":false,\"distance\":\"\",\"classColor\":\"\"}";
```

This string is placed into the request attribute `arrGPSData` and then output verbatim by `unit.gps.jsp`:

```jsp
// unit.gps.jsp lines 19-30
String str = ""+unitList.get(i);
resp = resp+str;
...
out.println(resp);
```

The JSP writes the concatenated result directly to the HTTP response body with no escaping. The response is consumed by JavaScript on the GPS map page. If any of the four unescaped fields — unit name, manufacturer name, unit type, or power/fuel type — contains a string such as:

```
","name":"x","__proto__":{"polluted":true}
```

or:

```
\u0022}];alert(document.cookie);//
```

then the JSON is malformed in a way that the client-side JavaScript parser may execute attacker-controlled code. Because these values originate from the database (populated via unit registration forms elsewhere in the application), a user with unit-editing privileges can store a payload and have it execute in every GPS viewer's browser session — a stored XSS.

The `latitude` and `longitude` fields are also injected unquoted (as numeric values). If stored as non-numeric strings (e.g., from an API ingestion path), they could also break the JSON structure and inject script context.

A legacy method `GPSDao.getGPSLocations()` at line 87 contains an additional raw string injection into the same JSON shape using `unitList[i]` directly in a `Statement`-based SQL concatenation (separate SQL injection finding below), amplifying the attack surface.

**Risk:** An attacker with write access to unit records (or via a separate SQLi vector) can store a JavaScript payload in a unit name, manufacturer, type, or power field. Every authenticated user who loads the GPS dashboard then executes the payload in their browser session, potentially stealing session cookies, performing CSRF-equivalent actions, or exfiltrating data from other tenants.

**Recommendation:**
1. Use a proper JSON serialisation library (e.g., Jackson, Gson) to construct the GPS JSON object from `GPSUnitBean` fields. Never build JSON by string concatenation.
2. If string concatenation is retained as an interim measure, apply `StringEscapeUtils.escapeJson()` (Apache Commons Lang) to every string field before embedding it in the JSON literal.
3. Ensure the response `Content-Type` is set to `application/json` (not `text/html`) so browsers do not attempt to parse the response as HTML.

---

### CRITICAL: IDOR — Calibration Reset Not Scoped to Authenticated Company

**File:** `src/main/java/com/action/AdminUnitImpactAction.java` (lines 21–33); `src/main/java/com/dao/UnitDAO.java` (line 876); `src/main/java/com/calibration/UnitCalibrationStarterInDatabase.java` (lines 9–16)

**Description:**

`AdminUnitImpactAction.execute()` accepts `equipId` directly from the HTTP request parameter and passes it to `UnitDAO.resetCalibration()` with no verification that the unit belongs to the authenticated user's company (`sessCompId`):

```java
// AdminUnitImpactAction.java lines 21-33
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
...
if (action.equalsIgnoreCase("reset_calibration")) {
    int equip = Integer.parseInt(equipId);
    UnitDAO.getInstance().resetCalibration(equip);   // no tenant check
    ...
}
```

```java
// UnitDAO.java line 876
public void resetCalibration(int equipId) throws SQLException {
    new UnitCalibrationStarterInDatabase().startCalibration(equipId);
}
```

```java
// UnitCalibrationStarterInDatabase.java lines 9-16
public void startCalibration(long unitId) throws SQLException {
    String query = "UPDATE unit SET impact_threshold = 0, "
        + "alert_enabled = FALSE, "
        + "reset_calibration_date = NOW(), "
        + "calibration_date = NULL "
        + "WHERE id = ?";
    DBUtil.updateObject(query, statement -> statement.setLong(1, unitId));
}
```

The `UPDATE` statement is parameterised (no SQL injection), but its `WHERE` clause filters only on `id`. There is no `AND comp_id = <sessCompId>` constraint. Any authenticated user from any tenant can submit `equipId=<any_unit_id>` and reset the impact-threshold calibration state of a unit belonging to a completely different company. Because `alert_enabled` is set to `FALSE` and `impact_threshold` is zeroed out, the targeted forklift will stop triggering impact alerts until a new calibration cycle completes — which can take hundreds of operating hours.

The same absence of tenant scoping is present in `AdminUnitAction` at line 173 where `getUnitCalibration(Long.valueOf(equipId))` is called with a user-supplied `equipId` and no company ownership check.

**Risk:** Cross-tenant sabotage of safety-critical calibration state. An authenticated attacker can silently disable impact alerting on competitor or other-tenant forklifts. In a warehouse environment this constitutes a direct safety risk: impacts that would normally trigger a safety alert will go unreported, potentially leading to unreported equipment damage or operator injury events.

**Recommendation:**
1. Add `AND comp_id = ?` to the `UPDATE` statement in `UnitCalibrationStarterInDatabase.startCalibration()` and pass `sessCompId` from the action layer through the DAO to the SQL.
2. Before calling `resetCalibration`, verify ownership by loading the unit record and asserting its `comp_id` matches `sessCompId`.
3. Apply the same ownership check to `getUnitCalibration` in `AdminUnitAction` (impact view path).

---

### CRITICAL: Authorization Bypass — Any Authenticated User Can Trigger Global Calibration Run

**File:** `src/main/java/com/action/CalibrationAction.java` (lines 12–22); `src/main/webapp/WEB-INF/struts-config.xml` (line 582)

**Description:**

`CalibrationAction` is a Struts action mapped to the path `/calibration` with no role constraint and no forward declaration:

```xml
<!-- struts-config.xml line 582 -->
<action path="/calibration" type="com.action.CalibrationAction">
</action>
```

```java
// CalibrationAction.java lines 12-22
public class CalibrationAction extends Action {
    @Override
    public ActionForward execute(ActionMapping mapping, ActionForm form,
                                 HttpServletRequest request, HttpServletResponse response)
            throws Exception {
        CalibrationJob job = new CalibrationJob();
        job.calibrateAllUnits();           // runs across ALL tenants/units
        return super.execute(mapping, form, request, response);
    }
}
```

`CalibrationJob.calibrateAllUnits()` calls `UnitCalibrationGetterInDatabase.getUnitsToCalibrate()` which queries the `unit` table with no `comp_id` filter — it retrieves every unit in the database that has a pending calibration, across all tenants. Any user who is authenticated (i.e., has a valid `sessCompId` in session, regardless of role) can issue a `GET /calibration.do` request and immediately finalize calibration for every pending unit system-wide, committing calculated impact thresholds to the database.

The `PreFlightActionServlet` only checks that `sessCompId` is non-null — it performs no role-based access check. There is no role guard inside `CalibrationAction` itself.

**Risk:** Any low-privilege operator-level account can force-commit safety-threshold values across all tenants at an arbitrary time, potentially before sufficient calibration data has been collected. If abused in combination with the impact-filter manipulation below, this could set abnormally low or high thresholds across an entire fleet. This is a direct safety risk.

**Recommendation:**
1. Restrict `/calibration.do` to an administrator or system role. Check `sessRole` (or equivalent) inside `CalibrationAction` and throw an `UnauthorizedException` or redirect to an error page if the caller is not a system administrator.
2. Remove the HTTP-accessible calibration trigger entirely; rely solely on the scheduled Quartz job (`CalibrationJobScheduler`). If a manual trigger is required, it should be accessible only from an internal/admin interface with role enforcement.
3. Add a `comp_id` filter to `UnitCalibrationGetterInDatabase.getUnitsToCalibrate()` so that even if the endpoint is accessed, the scope is limited to the caller's own tenant.

---

### HIGH: IDOR — GPS Unit IDs Not Validated Against Authenticated Company

**File:** `src/main/java/com/action/GetAjaxAction.java` (lines 44–51); `src/main/java/com/dao/GPSDao.java` (lines 35–58)

**Description:**

The `last_gps` branch of `GetAjaxAction` accepts an array of unit IDs from the request parameter `unit[]` and a `compId` from the request parameter `compId`, then passes them directly to `GPSDao.getUnitGPSData()`:

```java
// GetAjaxAction.java lines 44-51
} else if (action.equals("last_gps")) {
    String[] unit = request.getParameterValues("unit");
    String compId = request.getParameter("compId")==null?"0":request.getParameter("compId");
    ...
    request.setAttribute("arrGPSData",
        GPSDao.getUnitGPSData(compId, unit, dateTimeFormat, timezone));
}
```

Two distinct problems exist:

1. **`compId` is taken from the request, not from the session.** An attacker can supply any `compId` value. The `compId` parameter is passed to `getUnitGPSData` but is never actually used inside that method — it has no effect on the query. The GPS query (`QUERY_UNIT_GPS`) filters only on `unit_id`, so the `compId` parameter is purely cosmetic and provides no access control.

2. **The individual `unit` IDs in the array are not verified to belong to the authenticated user's company.** `GPSDao` queries `gps JOIN unit WHERE g.unit_id = ?` for each element of the `unit` array without checking `unit.comp_id = sessCompId`. An attacker can enumerate arbitrary unit IDs and obtain GPS location data (latitude, longitude, timestamp, unit name, manufacturer, type) for units belonging to other tenants.

**Risk:** Full GPS location history leakage across tenants. A tenant can track the physical location of competitor or other-tenant forklifts in real time, which is a serious privacy and competitive intelligence breach.

**Recommendation:**
1. Remove `compId` from the request parameters entirely. Read the company ID exclusively from `session.getAttribute("sessCompId")`.
2. Add `AND u.comp_id = ?` to `QUERY_UNIT_GPS` in `GPSDao` and bind it to `sessCompId`.
3. Alternatively, validate each requested `unitId` against the company's unit list before querying GPS data.

---

### HIGH: UnitDAO Singleton Uses Broken Double-Checked Locking (Non-Volatile Field)

**File:** `src/main/java/com/dao/UnitDAO.java` (lines 24–35)

**Description:**

`UnitDAO` implements a singleton using the double-checked locking (DCL) pattern, but the shared field `theInstance` is not declared `volatile`:

```java
// UnitDAO.java lines 24-34
private static UnitDAO theInstance;   // NOT volatile

public static UnitDAO getInstance() {
    if (theInstance == null) {                    // first check (no lock)
        synchronized (UnitDAO.class) {
            if (theInstance == null) {            // second check (under lock)
                theInstance = new UnitDAO();
            }
        }
    }
    return theInstance;
}
```

Without `volatile`, the Java Memory Model does not guarantee that the write to `theInstance` inside the `synchronized` block is visible to threads performing the first unsynchronized null-check. A thread can observe a non-null but partially constructed `UnitDAO` instance due to instruction reordering. Calling methods on a partially constructed instance can yield `NullPointerException` or corrupt internal state.

`UnitDAO.getInstance()` is called from `AdminUnitAction`, `AdminUnitImpactAction`, and `GetAjaxAction` — all of which are hit under concurrent load in a multi-threaded Tomcat container.

Note: The previously flagged non-volatile singletons in `UnitCalibrationEnderInDatabase` and `UnitCalibrationStarterInDatabase` are **not** singletons in the current codebase — both classes are instantiated with `new` directly (e.g., `UnitDAO.resetCalibration()` at line 876, `CalibrationJob.calibrateAllUnits()` at lines 17–18). No singleton pattern was found in those two classes in the current code. The broken DCL pattern is confirmed only in `UnitDAO`.

**Risk:** Under concurrent request load, two threads may simultaneously initialise `UnitDAO`, or a thread may receive a partially initialised instance, resulting in runtime exceptions or inconsistent DAO state. In a production Tomcat server with a thread pool this is a plausible race condition that can manifest as intermittent `NullPointerException`s.

**Recommendation:**
Declare `theInstance` as `volatile`:
```java
private static volatile UnitDAO theInstance;
```
Alternatively, use the initialization-on-demand holder idiom to avoid the need for `volatile`:
```java
private static class Holder {
    static final UnitDAO INSTANCE = new UnitDAO();
}
public static UnitDAO getInstance() { return Holder.INSTANCE; }
```

---

### HIGH: SQL Injection via String Concatenation in `UnitDAO.getUnitBySerial()`

**File:** `src/main/java/com/dao/UnitDAO.java` (lines 212–217)

**Description:**

`getUnitBySerial()` constructs a SQL query by concatenating the `serial_no` parameter directly into the query string using a `Statement`, not a `PreparedStatement`:

```java
// UnitDAO.java lines 211-217
if (!serial_no.equalsIgnoreCase("")) {
    String sql = "select id,comp_id from unit where serial_no = '" + serial_no + "'";
    if (activeStatus) {
        sql += " and active = true";
    }
    rs = stmt.executeQuery(sql);
```

A `serial_no` value of `' OR '1'='1` would return all units. A value of `'; DROP TABLE unit; --` (on a database configuration that permits stacked queries) could cause data loss. More practically on PostgreSQL, a `UNION SELECT` injection could exfiltrate data from any table accessible to the database user.

**Risk:** SQL injection leading to cross-tenant data exfiltration, authentication bypass (if serial-number lookup is used in an auth path), or data manipulation.

**Recommendation:** Replace with a `PreparedStatement`:
```java
String sql = "SELECT id, comp_id FROM unit WHERE serial_no = ?";
// ... use ps.setString(1, serial_no)
```

---

### HIGH: SQL Injection via String Concatenation in `UnitDAO.delUnitById()`

**File:** `src/main/java/com/dao/UnitDAO.java` (line 349)

**Description:**

`delUnitById()` concatenates the `id` parameter directly into a SQL `UPDATE` statement without parameterisation:

```java
// UnitDAO.java line 349
String sql = "update unit set active = false where id=" + id;
stmt.executeUpdate(sql);
```

The `id` value comes from `request.getParameter("equipId")` in `AdminUnitAction`. Although it is expected to be numeric, no type-validation or sanitisation is enforced before this call. A value such as `0 OR 1=1` would soft-delete every unit in the table.

**Risk:** Mass data corruption. An authenticated attacker can soft-delete all units in the database or, with more targeted input, selectively deactivate units belonging to other tenants.

**Recommendation:** Replace with a parameterised `PreparedStatement`. Also add a tenant-scoping `AND comp_id = ?` clause.

---

### HIGH: SQL Injection via String Concatenation in `UnitDAO.getUnitNameByComp()` and `getTotalUnitByID()`

**File:** `src/main/java/com/dao/UnitDAO.java` (line 311, line 548)

**Description:**

Both methods construct SQL by inserting a `compLst` string (a comma-separated list of company IDs) directly into an `IN (...)` clause:

```java
// UnitDAO.java line 311
String sql = "select id,name from unit where comp_id in (" + compLst + ")";

// UnitDAO.java line 548
String sql = "select count(id) from unit where comp_id in (" + compLst + ")";
```

`compLst` is produced by `CompanyDAO.getSubCompanyLst(compId)`, which itself constructs a string from database-sourced company IDs. If an administrator can control company names or IDs in a way that allows commas or SQL metacharacters to be embedded in `getSubCompanyLst()` output, this becomes a second-order SQL injection. Even without that, the pattern is architecturally unsafe — `IN (?)` with JDBC does not support variable-length lists, but the correct approach is to use an allowlist or a `JOIN`-based construction with parameterised IDs.

**Risk:** Second-order SQL injection if company IDs can be manipulated. Even without exploitation, the pattern represents a structural vulnerability that widens if the source of `compLst` ever changes.

**Recommendation:** Use a parameterised approach with a dynamically constructed placeholder list `IN (?, ?, ?)`, binding each company ID individually, or join against a subquery with a properly parameterised parent company check.

---

### HIGH: SQL Injection via String Concatenation in `UnitDAO.getType()` and `getPower()`

**File:** `src/main/java/com/dao/UnitDAO.java` (line 627, lines 666–670)

**Description:**

`getType()` concatenates `manu_id` directly into the SQL `WHERE` clause using `Statement.executeQuery()`:

```java
// UnitDAO.java line 627
String sql = "select distinct(type.id),name from manu_type_fuel_rel"
    + " left outer join type on type.id = manu_type_fuel_rel.type_id "
    + " where manu_id = " + manu_id
    + " order by name";
```

`getPower()` does the same for both `manu_id` and `type_id`:

```java
// UnitDAO.java lines 666-670
String sql = "select fuel_type.id,name from manu_type_fuel_rel"
    + " left outer join fuel_type on fuel_type.id = manu_type_fuel_rel.fuel_type_id "
    + " where manu_id = " + manu_id;
if (!type_id.equalsIgnoreCase("")) {
    sql += " and type_id= " + type_id;
}
```

Both parameters originate from `request.getParameter()` in `GetAjaxAction` (lines 26, 35). Although they are expected to be integers, no validation is performed.

**Risk:** SQL injection via the AJAX endpoint. An attacker can submit `manu_id=0 UNION SELECT username, password FROM users--` to extract credential data from the database.

**Recommendation:** Replace `Statement` with `PreparedStatement` and bind `manu_id` and `type_id` as typed integer parameters.

---

### HIGH: SQL Injection via String Concatenation in Legacy `GPSDao.getGPSLocations()`

**File:** `src/main/java/com/dao/GPSDao.java` (lines 87–88)

**Description:**

The legacy `getGPSLocations()` method concatenates individual unit IDs from an externally supplied array directly into a SQL string:

```java
// GPSDao.java lines 85-88
String sql = "select u.id,u.name,g.longitude,g.latitude,g.gps_time,g.current_location from gps as g"
    + " inner join unit as u on u.id=g.unit_id"
    + " where g.unit_id=" + unitList[i]
    + " order by g.gps_time desc limit 1";
```

Although `getGPSLocations()` does not appear to be called from any currently active action path (the active path uses `getUnitGPSData()`), it remains compiled into the application and could be wired up through a future action or reached indirectly.

**Risk:** SQL injection if this method is ever called with untrusted input. Even as dead code it represents a maintenance hazard.

**Recommendation:** Replace with a `PreparedStatement`. If the method is no longer needed, remove it entirely.

---

### HIGH: SQL Injection via String Concatenation in `GPSDao.getUnitById()`

**File:** `src/main/java/com/dao/GPSDao.java` (line 139)

**Description:**

`GPSDao.getUnitById()` concatenates the `id` parameter directly into the SQL `WHERE` clause:

```java
// GPSDao.java line 139
String sql = "select unit.id,unit.name,...,comp_id,unit.mac_address from unit"
    + " left outer join type on type.id = unit.type_id "
    + " left outer join fuel_type on fuel_type.id = unit.fuel_type_id"
    + " where unit.id=" + id;
```

**Risk:** SQL injection leading to data exfiltration or manipulation.

**Recommendation:** Replace with a parameterised `PreparedStatement`.

---

### MEDIUM: CalibrationAction Exposes Unauthenticated Path if `excludeFromFilter` Condition is Misunderstood

**File:** `src/main/webapp/WEB-INF/struts-config.xml` (line 582); `src/main/java/com/actionservlet/PreFlightActionServlet.java` (lines 98–115)

**Description:**

`PreFlightActionServlet.excludeFromFilter()` returns `false` for explicitly listed public paths (welcome, login, logout, etc.) and `true` for all other paths. The session check is applied only when `excludeFromFilter()` returns `true`. This logic is inverted from the conventional name: returning `true` means "apply the session filter", returning `false` means "allow without session check". The naming is misleading and increases the risk of a future developer accidentally adding `/calibration.do` (or any other sensitive path) to the exclusion list under the mistaken belief that `false` means "include in filter". The current code is functionally correct, but the inverted boolean naming is a maintenance risk for a safety-critical function.

Additionally, `PreFlightActionServlet` only checks `doGet`, which calls `doPost`. There is no `doPut` or `doDelete` override. Depending on the Tomcat connector configuration, non-standard HTTP methods routed to the `ActionServlet` might bypass the session check. Struts 1 typically only handles GET/POST, but this is worth verifying.

**Risk:** No active bypass in the current code; risk is to future maintainers introducing a regression that exposes sensitive actions.

**Recommendation:**
1. Rename `excludeFromFilter` to `requiresAuthentication` and invert the return values for clarity.
2. Document the logic explicitly with a comment.
3. Consider using a proper Servlet Filter (e.g., `javax.servlet.Filter`) for authentication enforcement, which provides more reliable interception across all HTTP methods and is easier to reason about.

---

### MEDIUM: `CalibrationJob.calibrateAllUnits()` Silently Swallows `SQLException` on Safety-Critical Operation

**File:** `src/main/java/com/calibration/CalibrationJob.java` (lines 15–24)

**Description:**

The `calibrateAllUnits()` method catches `SQLException` and only prints a stack trace, with no logging to a persistent log system, no alerting mechanism, and no retry logic:

```java
// CalibrationJob.java lines 15-24
public void calibrateAllUnits() {
    try {
        UnitCalibrationGetter getter = new UnitCalibrationGetterInDatabase();
        UnitCalibrationEnder ender = new UnitCalibrationEnderInDatabase();
        UnitCalibrator calibrator = new UnitCalibrator(getter, ender);
        calibrator.calibrateAllUnits();
    } catch (SQLException e) {
        e.printStackTrace();    // stack trace only — no log4j, no alerting
    }
}
```

Furthermore, `execute()` calls `calibrateAllUnits()` via `Executors.newSingleThreadExecutor().execute(this::calibrateAllUnits)`, which means any unchecked exception thrown inside the runnable would also be silently swallowed by the executor's default uncaught exception handler. If the database is unreachable or a calibration commit fails, the system will continue operating with stale or incomplete calibration data and no operator notification.

This is particularly dangerous because `UnitCalibrator.calibrateUnit()` does not catch exceptions from `endCalibration()` — if that call throws, the entire `calibrateAllUnits()` loop terminates mid-run, leaving some units calibrated and others not, with no record of which units were processed.

**Risk:** Silent calibration failure. Forklifts remain in an uncalibrated state (`alert_enabled = FALSE`, `impact_threshold = 0`) indefinitely with no notification to administrators. Impact alerts remain disabled on safety-critical equipment.

**Recommendation:**
1. Replace `e.printStackTrace()` with a proper `log.error("Calibration job failed", e)` call using the existing Log4j infrastructure.
2. Add a monitoring/alerting hook (e.g., write a failure record to a `calibration_errors` table, send an admin email).
3. Consider per-unit exception handling inside `UnitCalibrator.calibrateAllUnits()` so a failure on one unit does not abort calibration of all subsequent units.
4. Add an `UncaughtExceptionHandler` to the executor thread to capture any unchecked exceptions.

---

### MEDIUM: `CalibrationJobScheduler.contextDestroyed()` Creates and Discards a `ServletException` — No Scheduler Shutdown

**File:** `src/main/java/com/calibration/CalibrationJobScheduler.java` (lines 35–38)

**Description:**

The `contextDestroyed` lifecycle callback, called when the servlet context is being shut down, does not actually stop the Quartz scheduler. Instead it instantiates a `ServletException` and calls `printStackTrace()` on it — creating and immediately discarding an exception object to produce a stack trace as a log message:

```java
// CalibrationJobScheduler.java lines 36-38
@Override
public void contextDestroyed(ServletContextEvent servletContextEvent) {
    new ServletException("Application Stopped").printStackTrace();
}
```

The Quartz `Scheduler` that was started in `contextInitialized()` is never stored as an instance field and is never shut down. This has two consequences:

1. The Quartz scheduler thread pool may keep the JVM alive after the web application is undeployed, causing classloader leaks in Tomcat hot-redeploys.
2. The scheduler may continue to fire after the application context is destroyed, potentially executing calibration logic against a partially torn-down application.

**Risk:** Classloader leak on application redeploy; potential calibration job execution against a partially destroyed application context, which could corrupt calibration data or cause unhandled exceptions.

**Recommendation:**
1. Store the `Scheduler` as an instance field of `CalibrationJobScheduler`.
2. In `contextDestroyed()`, call `scheduler.shutdown(true)` to gracefully stop the scheduler and wait for running jobs to complete.
3. Replace the misuse of `new ServletException(...).printStackTrace()` with a proper `log.info("Application context destroyed, stopping calibration scheduler")` statement.

---

### MEDIUM: `UnitCalibrationImpactFilter` — Identity Comparison Used Instead of `equals()` for Timestamp

**File:** `src/main/java/com/calibration/UnitCalibrationImpactFilter.java` (line 46)

**Description:**

The `compareImpacts` method uses the `!=` reference-equality operator to compare two `Timestamp` objects:

```java
// UnitCalibrationImpactFilter.java line 46
private int compareImpacts(CalibrationImpact i1, CalibrationImpact i2) {
    if (i1.sessionStart != i2.sessionStart) return i1.sessionStart.compareTo(i2.sessionStart);
    return i1.time.compareTo(i2.time);
}
```

`Timestamp` is a reference type. Two distinct `Timestamp` objects representing the same instant in time will always satisfy `i1.sessionStart != i2.sessionStart` (they are different object references), so the secondary sort by `i1.time` will never be reached for any two impacts that share a session start time — unless they happen to be the exact same object reference in memory (which can only occur if the same `Timestamp` instance is reused, which `ResultSet.getTimestamp()` does not guarantee).

The practical consequence is that the 15-minute sectioning in `splitImpactsBy15MinutesOfSession` will misclassify impacts: it checks `impact.sessionStart.compareTo(sessionStart) != 0` using `.compareTo()` (value-based, correct), but `compareImpacts` uses `!=` (reference-based, incorrect), meaning the sort order can be wrong for same-session impacts. This leads to incorrect 15-minute bucket boundaries, which distorts the impact average and standard deviation used to calculate the final safety threshold.

**Risk:** Incorrect calibration threshold calculation. If the impact filter produces incorrect output due to the reference comparison bug, the computed `impact_threshold` written by `UnitCalibrationEnderInDatabase.endCalibration()` may be higher or lower than the statistically correct value. A threshold that is too low will trigger excessive false-positive impact alerts; a threshold that is too high will suppress genuine high-impact events, which is a safety risk.

**Recommendation:** Replace `!=` with `!i1.sessionStart.equals(i2.sessionStart)`:
```java
if (!i1.sessionStart.equals(i2.sessionStart))
    return i1.sessionStart.compareTo(i2.sessionStart);
```

---

### MEDIUM: `UnitCalibration.isCalibrated()` Logic Allows Zero-Impact Calibration

**File:** `src/main/java/com/calibration/UnitCalibration.java` (lines 36–38)

**Description:**

The `unitCalibrationNeverReset()` branch of `isCalibrated()` returns `true` if `resetCalibrationDate == null` AND `calibrationDate == null` AND `threshold != 0`:

```java
// UnitCalibration.java lines 36-38
private boolean unitCalibrationNeverReset() {
    return resetCalibrationDate == null && calibrationDate == null && threshold != 0;
}
```

This means a unit that was manually assigned a non-zero `impact_threshold` directly in the database (with both date fields null) is considered "calibrated" and will not go through the impact-data-driven calibration process. If the manually assigned threshold is incorrect (e.g., set to an arbitrary value by a database administrator or via a SQL injection), the unit will never be re-calibrated automatically. The `calibrationPercentage()` method will return `100` for such a unit, which will prevent `UnitCalibrator` from recalibrating it.

**Risk:** A unit with a manually set or attacker-modified threshold bypasses the statistical calibration process entirely. Combined with a SQL injection or direct database access, an attacker could set any threshold value and have it persist indefinitely.

**Recommendation:** Document this design decision explicitly. If intentional, add an audit log entry whenever a threshold is applied through this path. If unintentional, require at least one of the date fields to be set for a unit to be considered calibrated.

---

### LOW: `UnitAssignmentBean` Has Inconsistent Use of Lombok `@Builder` and `@NoArgsConstructor`

**File:** `src/main/java/com/bean/UnitAssignmentBean.java` (lines 9–28)

**Description:**

`UnitAssignmentBean` is annotated with both `@NoArgsConstructor` (which generates a public no-argument constructor) and `@Builder` (which is applied to a private constructor). The class also has a public `@Data`-generated setter for each field. This means the bean can be constructed in two ways: via the builder (which enforces the `isCurrent` boolean logic) or via the no-args constructor plus setters (which allows setting `current` to an arbitrary string, bypassing the `"Yes"/"No"` normalisation in the builder constructor).

```java
// UnitAssignmentBean.java lines 21-27
@Builder
private UnitAssignmentBean(int id, String company_name, String start, String end, boolean isCurrent) {
    ...
    this.current = isCurrent ? "Yes" : "No";   // normalised only in builder path
}
```

While this is not a directly exploitable security vulnerability, it is a data-integrity weakness: any code path that uses `new UnitAssignmentBean()` + `setCurrent("arbitrary")` will store an un-normalised value. If `current` is later used in a security-relevant display or access-control decision, this inconsistency could be leveraged.

**Risk:** Low. Data integrity weakness; potential for inconsistent `current` field values if the no-args + setter path is used.

**Recommendation:** Make the no-args constructor `private` or remove it if it is not required by the serialisation framework, so all construction goes through the builder.

---

### LOW: `unit.gps.jsp` Has No `Content-Type: application/json` Header

**File:** `src/main/webapp/gps/unit.gps.jsp` (line 4)

**Description:**

The JSP declares `contentType="text/html"` but outputs a raw JSON payload:

```jsp
<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
```

Sending JSON with a `text/html` content type causes browsers to treat the response as HTML, which means the XSS finding (CRITICAL-1 above) is compounded: the browser may attempt to parse the JSON payload as HTML and execute any `<script>` tags or inline event handlers embedded within it.

**Risk:** Amplifies the XSS severity: content-type mismatch means even data that would be harmless in a JSON context can be executed as HTML.

**Recommendation:** Change the content type to `application/json; charset=UTF-8`.

---

### LOW: `UnitCalibration.average()` Divides by Zero if `impacts` List Is Empty

**File:** `src/main/java/com/calibration/UnitCalibration.java` (lines 53–56)

**Description:**

`average()` divides by `impacts.size()` without a guard for the empty-list case:

```java
// UnitCalibration.java lines 53-56
private double average() {
    double sum = 0;
    for (int impact : impacts) sum += impact;
    return sum / impacts.size();   // ArithmeticException if size == 0
}
```

`getCalculatedThreshold()` calls `average()` and `standardDeviation(average)`. It is invoked from `UnitCalibrator.calibrateUnit()` after a `calibrationPercentage() == 100` check. `calibrationPercentage()` returns `100` when `isCalibrated()` is true. `calibrationDone()` returns `true` when `impacts.size() >= 100`, so in the normal automated flow the list is always non-empty when `getCalculatedThreshold()` is called. However, the `unitCalibrationNeverReset()` or `unitCalibrationDateAndThresholdSet()` paths in `isCalibrated()` do not guarantee a non-null or non-empty `impacts` list. If either of those paths returns `true`, a subsequent call to `getCalculatedThreshold()` will throw `ArithmeticException` (integer division by zero) or produce `NaN` (floating-point), depending on the list state.

**Risk:** Low in practice due to flow guarding, but represents a latent defect. An unexpected code path or future refactoring could trigger a division-by-zero during safety-threshold calculation, resulting in an exception that aborts calibration silently (see MEDIUM-1 exception swallowing).

**Recommendation:** Add a guard:
```java
private double average() {
    if (impacts == null || impacts.isEmpty()) return 0.0;
    double sum = 0;
    for (int impact : impacts) sum += impact;
    return sum / impacts.size();
}
```

---

### INFO: `UnitCalibrationGetterInDatabase.getUnitsToCalibrate()` Queries Global (Cross-Tenant) Unit Table

**File:** `src/main/java/com/calibration/UnitCalibrationGetterInDatabase.java` (lines 19–28)

**Description:**

The scheduled `CalibrationJob` uses `getUnitsToCalibrate()`, which retrieves calibration candidates from the `unit` table with no `comp_id` filter:

```java
// UnitCalibrationGetterInDatabase.java lines 20-24
String query = "SELECT id, reset_calibration_date, calibration_date, impact_threshold "
    + "FROM unit "
    + "WHERE impact_threshold = 0 "
    + "AND alert_enabled IS FALSE "
    + "AND reset_calibration_date IS NOT NULL";
```

This is the intended behaviour for the background Quartz job (it should process all tenants). However, because the same `UnitCalibrationGetterInDatabase` class is also used when constructing a `UnitCalibrator` in response to the unauthenticated `CalibrationAction` endpoint (CRITICAL-3), the lack of a tenant scope in this query directly enables the cross-tenant calibration abuse described in that finding.

**Risk:** Informational in isolation; elevated to CRITICAL when combined with `CalibrationAction` finding.

**Recommendation:** Provide a scoped variant of `getUnitsToCalibrate(long companyId)` for use in the web-layer action, and keep the unscoped version only for the internal scheduler.

---

### INFO: `UnitCalibrationEnderInDatabase` and `UnitCalibrationStarterInDatabase` — No Singleton Pattern Found (Confirming Prior Note)

**File:** `src/main/java/com/calibration/UnitCalibrationEnderInDatabase.java`; `src/main/java/com/calibration/UnitCalibrationStarterInDatabase.java`

**Description:**

The audit brief noted that `UnitCalibrationEnderInDatabase` and `UnitCalibrationStarterInDatabase` were previously identified as having broken double-checked locking with non-volatile `theInstance` fields. In the current codebase (branch: master), neither class contains any singleton pattern. Both are instantiated with `new` at each call site:

- `UnitDAO.java` line 876: `new UnitCalibrationStarterInDatabase().startCalibration(equipId)`
- `CalibrationJob.java` lines 17–18: `new UnitCalibrationGetterInDatabase()` / `new UnitCalibrationEnderInDatabase()`

The non-volatile singleton pattern that was previously flagged has either been removed or was present in a different branch. The broken DCL pattern is confirmed only in `UnitDAO` (see HIGH finding above).

**Risk:** None from DCL in these classes. The `UnitDAO` broken DCL remains a risk.

**Recommendation:** No action required for these two classes with respect to DCL. Confirm that the fix was intentional and that no singleton references to these classes exist in other branches.

---

## Summary

| Severity | Count | Findings |
|----------|-------|---------|
| CRITICAL | 3 | XSS via unescaped GPS JSON; IDOR on calibration reset; Authorization bypass on global calibration trigger |
| HIGH | 7 | GPS IDOR (unit IDs not scoped to tenant); Broken DCL in UnitDAO; SQLi in getUnitBySerial; SQLi in delUnitById; SQLi in getUnitNameByComp/getTotalUnitByID; SQLi in getType/getPower; SQLi in legacy GPSDao methods |
| MEDIUM | 5 | CalibrationAction auth bypass naming risk; Exception swallowing in CalibrationJob; CalibrationJobScheduler no-shutdown on destroy; Reference-equality Timestamp bug in ImpactFilter; Zero-impact calibration bypass in isCalibrated |
| LOW | 3 | UnitAssignmentBean no-args constructor bypass; unit.gps.jsp wrong Content-Type; Division-by-zero in average() |
| INFO | 2 | getUnitsToCalibrate cross-tenant scope note; DCL confirmation for EnderInDatabase/StarterInDatabase |

**CRITICAL: 3 / HIGH: 7 / MEDIUM: 5 / LOW: 3 / INFO: 2**
