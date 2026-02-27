# Pass 4 -- Code Quality Audit: DAO Package

**Auditor:** A07
**Date:** 2026-02-25
**Batch:** 2026-02-25-01
**Pass:** 4 (Code Quality)
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/dao/` -- 10 files

---

## 1. File Inventory

| # | File | Lines | Methods | Notes |
|---|------|------:|--------:|-------|
| 1 | BatteryDAO.java | 420 | 6 | Battery charge/change tracking |
| 2 | DriverDAO.java | 569 | 8 | Driver queries + licence expiry |
| 3 | DriverImportDAO.java | 1208 | 17 | Driver CRUD + licence blacklist import |
| 4 | ImpactDAO.java | 1353 | 11 | Impact report queries |
| 5 | ImportDAO.java | 4881 | 16 | Vehicle/driver/question import -- **God class** |
| 6 | LockOutDAO.java | 145 | 2 | Unit lock-out data |
| 7 | MessageDao.java | 113 | 6 | Outgoing message queries |
| 8 | PreCheckDAO.java | 578 | 6 | Pre-operational check reports |
| 9 | RegisterDAO.java | 535 | 3 | Customer self-registration |
| 10 | UnitDAO.java | 2731 | 33 | Unit/location/dept/utilisation -- **God class** |
| | **TOTAL** | **12,533** | | |

---

## 2. Naming Conventions

### 2.1 Class Name Inconsistency (SEV-2)

| Finding | Detail |
|---------|--------|
| **MessageDao** uses camelCase "Dao" | All other 9 files use UPPERCASE "DAO" (BatteryDAO, DriverDAO, etc.) |
| Recommendation | Rename to `MessageDAO` for consistency |

### 2.2 Method Naming Issues (SEV-3)

| File | Method | Issue |
|------|--------|-------|
| BatteryDAO | `getDept_prefix()` | snake_case mixed with camelCase |
| UnitDAO | `getArryModel()` | Typo: "Arry" should be "Array" (used consistently, so not a bug, but unclear) |
| UnitDAO | `getArryModelImpact()` | Same typo pattern |
| UnitDAO | `getArryModelImpactByDriver()` | Same typo pattern |
| UnitDAO | `getArryModelLinde()` | Same typo pattern |
| UnitDAO | `getArryModelLindeGroup()` | Same typo pattern |
| UnitDAO | `Fetch_maxUsage_Chart()` | PascalCase + snake_case; violates Java convention |
| UnitDAO | `getTotalTime()` comment says "muniutes" | Typo in comment (minor) |

### 2.3 Variable Naming (SEV-3)

Local variables across all DAOs consistently use `snake_case` (e.g., `cust_cd`, `loc_cd`, `dept_cd`, `unit_name`) rather than Java-standard `camelCase`. This is a codebase-wide convention rather than isolated deviation.

Parameter `DriverImportBean DriverImportBean` in DriverImportDAO (lines 148, 203, 258, etc.) shadows the class name with the local variable -- used in at least 8 methods.

---

## 3. God Classes (SEV-1)

### 3.1 ImportDAO.java -- 4,881 lines, 16 methods

- Combines unrelated responsibilities: question management, driver import, vehicle import, CAN-rule sending, service settings.
- Single method `saveVehicleInfo()` (starting at line 2632) and `sendCanUnit()` (starting at line 3487) are each hundreds of lines long.
- Contains transaction management (`setAutoCommit(false)`, `commit()`, `rollback()`) only in `sendCanUnit()` -- no other multi-statement write methods use transactions.

### 3.2 UnitDAO.java -- 2,731 lines, 33 methods

- Combines unit queries, location queries, department queries, model queries, utilisation reports, chart generation (`Fetch_maxUsage_Chart`), file I/O (`getExportDir`), and unit summary reports.
- At least 5 distinct responsibility areas that should be separate DAOs (LocationDAO, DepartmentDAO, ModelDAO, UtilisationDAO, UnitReportDAO).
- Raw `ArrayList` (without generic type parameter) used in `getMaxUtilGroup()` and `getArryModelLindeGroup()` signatures.

---

## 4. SQL Injection Vulnerabilities (SEV-0 -- CRITICAL)

Every file in this package constructs SQL via string concatenation with user-supplied parameters. Only 3 of 10 files use `PreparedStatement` at all, and even those mix prepared statements with concatenated queries.

### 4.1 Files Using Only String Concatenation (No PreparedStatement)

| File | Concatenated Query Count |
|------|------------------------:|
| BatteryDAO.java | 6 |
| DriverDAO.java | 10 |
| ImpactDAO.java | 11 |
| LockOutDAO.java | 2 |
| MessageDao.java | 2 |
| PreCheckDAO.java | 6+ |
| UnitDAO.java | 38+ |

### 4.2 Files With Mixed PreparedStatement and Concatenation

| File | PreparedStatement Uses | Concatenated Uses |
|------|----------------------:|------------------:|
| ImportDAO.java | 16 | 22+ |
| DriverImportDAO.java | 4 | 18+ |
| RegisterDAO.java | 2 | 3 |

### 4.3 Representative Examples

- **BatteryDAO.java:42** -- `" and d1.utc_time >= '"+from+"'::timestamp"` -- date parameter concatenated directly.
- **DriverDAO.java:35** -- `extra += " and \"FMS_USER_DEPT_REL\".\"CUST_CD\" = " + cust_cd;` -- ID concatenated directly.
- **DriverDAO.java:159** -- `" and v.\"VEHICLE_TYPE_CD\" = "+ vehtype +" and ur.\"USER_CD\" = " + usercd;` -- multiple params concatenated.
- **DriverImportDAO.java:29-30** -- `"trim ( both ' ' from '" + fname + "')"` -- first/last name directly in SQL.
- **RegisterDAO.java:474** -- `"ilike '"+cname.trim()+"'"` -- company name concatenated.
- **MessageDao.java:62** -- `"select * from mnt_msg where \"FORM_CD\"="+fid;` -- form ID concatenated.
- **LockOutDAO.java:103** -- `"'"+st_dt+"'::timestamp and unlocked_utc_time < '"+end_dt+"'::timestamp"` -- dates concatenated.

---

## 5. e.printStackTrace() and Broad Catches (SEV-2)

### 5.1 e.printStackTrace() Count by File

| File | Count |
|------|------:|
| BatteryDAO.java | 6 |
| DriverDAO.java | 9 |
| DriverImportDAO.java | 2 |
| ImpactDAO.java | 11 |
| ImportDAO.java | 5 |
| LockOutDAO.java | 2 |
| MessageDao.java | 1 (+ 3 raw `System.out.println` in finally) |
| PreCheckDAO.java | 6 |
| RegisterDAO.java | 3 |
| UnitDAO.java | 38 |
| **TOTAL** | **83** |

None of these use a logging framework (except ImportDAO which has `log4j` but still uses `e.printStackTrace()` in some catch blocks and `System.out.println` in 93 places).

### 5.2 Broad `catch(Exception e)` Count by File

| File | Count |
|------|------:|
| BatteryDAO.java | 9 (including inner catches at lines 213, 231) |
| DriverDAO.java | 9 |
| DriverImportDAO.java | 19 |
| ImpactDAO.java | 11 |
| ImportDAO.java | 16 |
| LockOutDAO.java | 2 |
| MessageDao.java | 1 |
| PreCheckDAO.java | 6 |
| RegisterDAO.java | 3 |
| UnitDAO.java | 38 |
| **TOTAL** | **114** |

Every catch block in the package catches `Exception` rather than `SQLException` or a more specific type.

### 5.3 Orphaned `e.getMessage()` Statements (SEV-3)

75 occurrences across 7 files where `e.getMessage()` is called as a bare statement (return value discarded). Pattern:
```java
catch(Exception e) {
    e.printStackTrace();
    e.getMessage();     // <-- return value unused; serves no purpose
}
```

Found in: BatteryDAO (6), DriverDAO (9), ImpactDAO (11), LockOutDAO (2), PreCheckDAO (6), RegisterDAO (3), UnitDAO (38).

---

## 6. Resource Management / Connection Leaks (SEV-1)

### 6.1 No try-with-resources

None of the 10 files use Java 7+ `try-with-resources`. All use manual `try/finally` cleanup.

### 6.2 Unsafe finally Blocks

The standard cleanup pattern across most files is:
```java
finally {
    if(null != rs) {rs.close();}
    if(null != stmt) {stmt.close();}
    DBUtil.closeConnection(conn);
}
```

**Problem:** If `rs.close()` throws, `stmt` and `conn` are leaked. Only MessageDao.java wraps each close in its own try/catch (lines 79-100), but this approach has its own issues (see 6.3).

### 6.3 MessageDao -- Instance-Level JDBC Fields (SEV-1)

MessageDao (lines 15-21) stores Connection, Statement, and ResultSet as **instance fields**:
```java
public class MessageDao {
    Connection conn;
    Statement stmt;
    ResultSet rset;
    String queryString = "";
    ...
```

This makes the class **not thread-safe** and risks leaking resources if the same instance is used concurrently. The `init()` method acquires a connection via JNDI lookup (unlike all other DAOs which use `DBUtil.getConnection()`), demonstrating an inconsistent connection strategy.

### 6.4 DriverImportDAO.saveDriverInfo() / updateDriverInfo() -- Conditional Close (SEV-2)

Lines 549-553 and 963-967:
```java
finally {
    if (null != ps) {
        ps.close();
        DBUtil.closeConnection(conn);  // only runs if ps != null
    }
}
```
If `ps` is never assigned (e.g., exception before `conn.prepareStatement()`), the connection is **never closed**.

### 6.5 DriverImportDAO.saveLicenseExpiryBlackListInfo() -- Commented-Out Cleanup (SEV-1)

Lines 893-917: The entire finally block's resource cleanup code is **commented out**, leaving only `DBUtil.closeConnection(conn)`. Multiple `Statement` and `ResultSet` objects created within the method (`stmt1`, `rs`, `rset`, `ps`) are not reliably closed.

### 6.6 BatteryDAO.getDept_prefix() / getDuration() -- Connection Per Call in Loop (SEV-1)

`getDept_prefix()` (line 386) and `getDuration()` (line 351) each acquire their own database connection. They are called from within `while(rs.next())` loops in `calculateBatteryChange()` and `calculateBatteryCharge()`, creating a **new connection per row** processed. This can exhaust the connection pool.

---

## 7. N+1 Query Problems (SEV-1)

### 7.1 BatteryDAO -- getDept_prefix() in Result Loop

`calculateBatteryChange()` (line 223) and `calculateBatteryCharge()` (lines 313, 332) call `getDept_prefix()` for each row. Each call opens a new connection and executes a query.

### 7.2 BatteryDAO -- getDuration() in Result Loop

`calculateBatteryChange()` (line 210) calls `getDuration()` inside the row-processing loop. Each call opens a new connection to compute a timestamp difference that could be done in the original query or in Java.

### 7.3 PreCheckDAO.getCheckSummary() -- Per-Unit Queries

Lines 209-253: For each unit in `arrUnit`, two separate queries are executed (average completion time + failed questions). With N units, this generates 2N+1 queries.

### 7.4 PreCheckDAO.getChecks(6-param) -- Per-ID Query

Lines 78-93: After fetching all checklist result IDs, iterates over each ID and executes a separate query per ID to count failed answers. With N results, this is N+1 queries.

### 7.5 PreCheckDAO.getChecksByDriver() -- Nested DAO Calls + Per-Driver Query

Line 538: Inside a loop iterating over `preCheckMap` entries, calls `driverDAO.getDriverNameById(driver_cd)` which opens a new connection and executes a query for each driver.

### 7.6 UnitDAO.getUnusedUnit() -- Per-Unit Follow-Up Query

Lines 836-850: After fetching unused units, iterates over each and executes a separate query to get last report time. N+1 pattern.

### 7.7 UnitDAO.getUtil() -- Triple-Nested Loop Queries

Lines 596-625: For each model, for each day in duration, executes a query. With M models and D days, this generates M*D queries.

### 7.8 UnitDAO.getMaxUtilGroup() -- Quadruple-Nested Loop Queries

Lines 1485-1523: For each model, for each location, for each department, for each day, for each hour (24), executes a query. This is O(M * L * D * Days * 24) queries -- potentially thousands.

---

## 8. Missing Transactions (SEV-1)

### 8.1 RegisterDAO.register() -- Multi-Table Inserts Without Transaction

Lines 29-456: The `register()` method performs approximately 15-20 sequential INSERT statements across 8+ tables (FMS_CUST_MST, FMS_CUST_GRP_REL, FMS_LOC_MST, FMS_DEPT_MST, FMS_CUST_DEPT_REL, FMS_USR_CUST_REL, FMS_GRP_MST, FMS_VEHICLE_MST, FMS_USR_VEHICLE_REL, FMS_USR_MST, FMS_USR_GRP_REL, FMS_USER_DEPT_REL, FMS_OPCHK_QUEST_MST). There is **no transaction management** -- a failure partway through leaves the database in an inconsistent state. The method returns `null` on individual failures but does not roll back prior inserts.

### 8.2 DriverDAO.sendIDDENY() -- Multi-Table Writes Without Transaction

Lines 141-246: Inserts into `outgoing`, `outgoing_stat`, and `FMS_VEHICLE_OVERRIDE`, plus `driver_licence_expiry_status` without any transaction boundary.

### 8.3 DriverDAO.checkValidLicence() -- Mixed Read/Write Without Transaction

Lines 402-487: Reads data, then performs inserts into `outgoing` and `outgoing_stat` in a loop without transaction management.

### 8.4 DriverImportDAO.saveLicenseExpiryBlackListInfo() -- Multi-Table Writes

Lines 559-922: Performs deletes, inserts, and updates across `FMS_DRIVER_BLKLST`, `driver_licence_expiry_mst`, `fms_vehicle_access_mapper` without transaction management.

### 8.5 ImportDAO -- Partial Transaction Usage

Only `sendCanUnit()` (around line 2649) uses `setAutoCommit(false)` / `commit()` / `rollback()`. All other write methods in ImportDAO (saveQuestions, saveDriverInfo, saveVehicleInfo, etc.) perform multiple writes without transactions.

---

## 9. Unbounded Queries (SEV-2)

### 9.1 No LIMIT Clauses on Data Queries

The following queries return unbounded result sets with no pagination or row limits:

| File | Method | Query Description |
|------|--------|-------------------|
| UnitDAO | `getUnitSummary()` | Fetches ALL vehicles across ALL customers |
| UnitDAO | `getUnitSummaryNZ()` | Fetches all NZ vehicles |
| UnitDAO | `getSimSwapSummary()` | Fetches all sim swap records |
| UnitDAO | `getUnusedUnit()` | Fetches all unused units |
| ImpactDAO | Multiple methods | Fetch all impacts for a time period |
| PreCheckDAO | `getCheckSummary()` | Fetches all units then queries each |
| DriverDAO | `checkExpiry()` | Fetches all expired driver licences |
| BatteryDAO | All methods | Fetch all battery events in date range |

---

## 10. Unused Imports (SEV-3)

| File | Import | Status |
|------|--------|--------|
| DriverDAO.java | `java.sql.Array` | **Unused** -- no `Array` type referenced in code |
| DriverDAO.java | `java.util.HashMap` | Used only in `sendIDDENY` parameter -- valid |
| DriverDAO.java | `java.util.Iterator` | **Unused** -- never referenced |
| DriverDAO.java | `java.util.Map.Entry` | **Unused** -- never referenced |
| ImpactDAO.java | `org.apache.xmlbeans.XmlBeans` | **Unused** -- never referenced |
| ImpactDAO.java | `org.apache.xmlbeans.impl.tool.XMLBean` | **Unused** -- never referenced |
| UnitDAO.java | `org.apache.xmlbeans.impl.tool.XMLBean` | **Unused** -- never referenced |
| MessageDao.java | `java.util.ArrayList` | **Unused** -- never referenced (no ArrayList in file) |
| ImportDAO.java | `java.util.List` | **Unused** -- not referenced outside import |
| ImportDAO.java | `FmsChklistLangSettingRepo` | Declared as field, never assigned or invoked |

---

## 11. Commented-Out Code (SEV-3)

### 11.1 DriverImportDAO.saveLicenseExpiryBlackListInfo()

- **Lines 610, 628, 648, 736, 748, 750, 766**: Commented-out `System.out.println` debug statements.
- **Lines 650-652**: Commented-out alternative SQL query.
- **Lines 893-917**: Large block of commented-out finally cleanup code (25 lines).

### 11.2 ImportDAO.java

126 comment-block occurrences detected. ImportDAO contains extensive commented-out `System.out.println` debug lines throughout (93 `System.out.println` active, many more commented out).

### 11.3 PreCheckDAO.java

- Lines 148-149, 158-159, 291: Commented-out `RuntimeConf.start_time`/`end_time` references.

### 11.4 UnitDAO.java

- Line 594: Commented-out alternative method call.
- Line 603: Commented-out alternative method call.
- Line 656: Commented-out alternative SQL query.
- Line 902: Commented-out RuntimeConf time filter.

### 11.5 LockOutDAO.java

- Lines 38-39: Commented-out time filter query fragment.

---

## 12. Code Duplication (SEV-2)

### 12.1 BatteryDAO -- Near-Identical Query Methods

`getBatteryCharge()` (lines 16-72) and `getBatteryChange()` (lines 74-130) are structurally identical with minor SQL differences. They share the same:
- Connection/Statement/ResultSet setup
- UnitDAO instantiation for unit list
- try/catch/finally pattern
- Error handling

Similarly, `calculateBatteryChange()` and `calculateBatteryCharge()` share about 70% of their structure.

### 12.2 LockOutDAO -- Near-Identical Methods

`getLockOutData()` (lines 15-78) and `getLockOutDataNtlRpt()` (lines 80-142) are nearly identical, differing only in the date filter clause. **Additionally, there is a logic inconsistency:** in `getLockOutData()` line 57, the "else" case maps to `"Other"`, but in `getLockOutDataNtlRpt()` line 122, the same "else" case maps to `"Question"` -- likely a copy-paste bug.

### 12.3 DriverDAO -- Filter Construction Duplication

The filter-construction pattern (`extra += " and ... = " + param`) is duplicated across `getArrayDriver()`, `getDriverlst()`, `getDriverFulllst()`, `getArrayDriverImpact()`, and `getDriverImpactLst()`.

### 12.4 DriverImportDAO -- Repeated Result Mapping

The pattern of reading 9 columns from the `driver` table and mapping them to `DriverImportBean` fields is duplicated verbatim in `getAllDriver()`, `getAllDriverLinde(compId, boolean)`, `getDriverLicence()`, and `getDriverById()`.

### 12.5 UnitDAO -- Duplicated Utility Methods

`getUnitLstByModel()` (line 159) and `getUnitLstByModelLinde()` (line 1738) are nearly identical with minor filter differences. `getArryModel()` and `getArryModelLinde()` follow the same duplication pattern.

`getUnitSummary()` and `getSimSwapSummary()` have extensive structural duplication (similar SELECT, same joins, same result mapping pattern).

`getTotalTime()` and `getWorkDays()` (lines 927-1078) share approximately 80% of their logic.

### 12.6 PreCheckDAO -- Overloaded getChecks() Methods

Three `getChecks()` overloads share similar structure but are not factored into a common private method.

---

## 13. MessageDao -- Architectural Concerns (SEV-1)

### 13.1 Inconsistent Connection Strategy

MessageDao uses JNDI lookup (`InitialContext` / `DataSource`) while all other 9 DAOs use `DBUtil.getConnection()`. This suggests MessageDao was written separately or at a different time and was never aligned.

### 13.2 opCode-Driven Dispatch in init()

The `init()` method (lines 48-102) uses `opCode` string comparison to dispatch behavior:
```java
if(opCode.equalsIgnoreCase("get_msg")) { ... }
else if(opCode.equalsIgnoreCase("testing")) { selectMesssage(); }
```
This is a non-standard pattern for a DAO. The method name `init()` is misleading -- it actually executes queries.

### 13.3 Method Name Typo

`selectMesssage()` (line 105) has triple 's' -- likely typo of `selectMessage()`.

### 13.4 Debug Code Left In

`selectMesssage()` contains `System.out.println("result: " + rset.getString(1))` -- debug output in production code.

---

## 14. Additional Style Issues

### 14.1 System.out.println / System.err.println Usage (SEV-2)

| File | System.out Count | System.err Count |
|------|-----------------:|-----------------:|
| DriverDAO.java | 2 | 0 |
| DriverImportDAO.java | 7 (commented) | 5 |
| ImportDAO.java | 93 | 0 |
| MessageDao.java | 5 | 0 |
| PreCheckDAO.java | 2 (commented) | 0 |
| UnitDAO.java | 5 | 0 |

ImportDAO.java has **93 active `System.out.println` statements** despite having a log4j `Logger` field declared. This is the most egregious case of inconsistent logging.

### 14.2 TYPE_SCROLL_SENSITIVE Everywhere (SEV-3)

Every `createStatement()` call across all 10 files uses `ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY`. Most queries only iterate forward with `rs.next()` and never use scrolling. `TYPE_FORWARD_ONLY` would be more efficient and is the default.

### 14.3 Raw Types (SEV-3)

- UnitDAO.java `getMaxUtilGroup()` line 1392: `ArrayList locdeptList` parameter -- raw type.
- UnitDAO.java `getArryModelLindeGroup()` line 1560: `ArrayList locDeptLst` parameter -- raw type.
- UnitDAO.java line 1573: `new ArrayList()` -- raw type.

### 14.4 UnitDAO Blank Lines (SEV-3)

UnitDAO.java lines 13-31 contain 19 consecutive blank lines between the last import and the first class-level import, suggesting deleted or reorganized code.

---

## 15. Summary of Findings by Severity

| Severity | Count | Category |
|----------|------:|----------|
| SEV-0 (Critical) | 1 | SQL injection via string concatenation across all 10 files (96+ concatenation points) |
| SEV-1 (High) | 8 | God classes (2), connection leaks (3), N+1 queries (8 patterns), missing transactions (5 methods), MessageDao architecture |
| SEV-2 (Medium) | 6 | e.printStackTrace (83 instances), broad catches (114), code duplication (6 patterns), naming inconsistency (MessageDao), unbounded queries, System.out.println (114) |
| SEV-3 (Low) | 6 | Unused imports (10), commented-out code (multiple blocks), method naming typos, orphaned e.getMessage() (75), raw types, TYPE_SCROLL_SENSITIVE overuse |

---

## 16. Priority Remediation Recommendations

1. **SQL Injection (SEV-0):** Convert all string-concatenated queries to `PreparedStatement` with parameterized bindings. This is the single highest-risk issue.
2. **Missing Transactions (SEV-1):** Wrap multi-statement write methods (`RegisterDAO.register()`, `DriverDAO.sendIDDENY()`, `DriverImportDAO.saveLicenseExpiryBlackListInfo()`, all ImportDAO write methods) in explicit transactions with rollback on failure.
3. **Connection Leaks (SEV-1):** Adopt try-with-resources; fix DriverImportDAO conditional-close bug; refactor MessageDao to use DBUtil.
4. **N+1 Queries (SEV-1):** Refactor `getDept_prefix()` and `getDuration()` into the parent query via JOINs or subqueries; batch PreCheckDAO per-ID queries; refactor UnitDAO nested loops into aggregate queries.
5. **God Classes (SEV-1):** Split ImportDAO into QuestionImportDAO, DriverImportDAO (merge with existing), VehicleImportDAO, CanRuleDAO, ServiceSettingsDAO. Split UnitDAO into LocationDAO, DepartmentDAO, ModelDAO, UtilisationDAO, UnitReportDAO.
6. **Logging (SEV-2):** Replace all `e.printStackTrace()` and `System.out.println` with structured logging via log4j (already available in ImportDAO). Remove orphaned `e.getMessage()` calls.

---

*Report generated by audit agent A07. Report only -- no code modifications made.*
