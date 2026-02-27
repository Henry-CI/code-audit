# Pass 4 -- Code Quality Audit: bean package (Q-Z)

**Auditor:** A03
**Date:** 2026-02-25
**Repository:** C:\Projects\cig-audit\repos\fleetfocus
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `com.torrent.surat.fms6.bean` (files Q through Z)

---

## Scope

20 files audited in `WEB-INF/src/com/torrent/surat/fms6/bean/`:

| # | File | Lines | Methods | Findings |
|---|------|------:|--------:|---------:|
| 1 | QuestionBean.java | 126 | 20 | 2 |
| 2 | RestrictedAccessUsageBean.java | 101 | 23 | 2 |
| 3 | SFTPSettings.java | 61 | 14 | 2 |
| 4 | ServiceDueFlagBean.java | 1003 | 53 | 19 |
| 5 | SiteConfigurationBean.java | 157 | 34 | 1 |
| 6 | SpareModuleBean.java | 120 | 30 | 1 |
| 7 | SpecialAccessBean.java | 70 | 16 | 1 |
| 8 | SubscriptionBean.java | 51 | 10 | 1 |
| 9 | SuperMasterAuthBean.java | 69 | 15 | 1 |
| 10 | UnitBean.java | 166 | 34 | 1 |
| 11 | UnitUtilSummaryBean.java | 113 | 26 | 1 |
| 12 | UnitVersionInfoBean.java | 33 | 6 | 0 |
| 13 | UnitutilBean.java | 189 | 30 | 1 |
| 14 | UnusedUnitBean.java | 90 | 22 | 1 |
| 15 | UserBean.java | 51 | 12 | 1 |
| 16 | UserDriverBean.java | 50 | 12 | 1 |
| 17 | UserFormBean.java | 59 | 14 | 2 |
| 18 | VehDiagnostic.java | 218 | 34 | 1 |
| 19 | VehNetworkSettingsBean.java | 35 | 6 | 2 |
| 20 | VehicleImportBean.java | 140 | 28 | 1 |

**Total distinct findings: 42**

---

## Summary of Findings by Category

| Category | Count | Severity |
|----------|------:|----------|
| God class (1000+ lines / 20+ methods) | 2 | HIGH |
| DB access in bean (layering violation) | 1 | HIGH |
| SQL injection risk (string concatenation) | 1 | HIGH |
| e.printStackTrace() | 3 | MEDIUM |
| Broad catch (Exception) | 3 | MEDIUM |
| Commented-out code | 2 | MEDIUM |
| Raw types (missing generics) | 2 | MEDIUM |
| Naming convention violations | 10 | LOW |
| Package-private fields (missing access modifier) | 9 | LOW |
| Unused imports | 2 | LOW |
| TODO / auto-generated stubs | 2 | LOW |
| Sensitive data in plain-text fields | 2 | LOW |
| Inconsistent style / formatting | 3 | LOW |

---

## Detailed Findings

### 1. QuestionBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/QuestionBean.java`
**Lines:** 126 | **Methods:** 20 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q01-01 | 4-17 | LOW | Naming | Field names use snake_case (`user_cd`, `loc_cd`, `dept_cd`, `ans_type`, `exp_ans`, `crit_ans`, `access_level`, `access_cust`, `access_site`, `access_dept`, `question_id`). Getter/setter names propagate underscore convention (`getUser_cd`, `setAns_type`, etc.) which violates JavaBean camelCase convention. |
| Q01-02 | 12-16 | LOW | Inconsistency | Fields `custCd` (line 12) through `questionSpa`/`questionTha` (lines 18-19) use camelCase while all other fields use snake_case. Inconsistent naming within same class. |

**Reading evidence:** Pure POJO, 126 lines, no imports, no logic, no DB access. All fields are String or boolean with getters/setters only.

---

### 2. RestrictedAccessUsageBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java`
**Lines:** 101 | **Methods:** 23 (1 constructor + 22 getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q02-01 | 5 | LOW | Style | Multiple field declarations on a single line separated by commas. Reduces readability and makes diffs harder to review. |
| Q02-02 | 8 | LOW | TODO stub | Constructor contains only `// TODO Auto-generated constructor stub`. Dead comment that should be removed or the constructor should be removed entirely since it is a no-op. |

**Reading evidence:** Pure POJO, 101 lines. No imports, no business logic, no DB access.

---

### 3. SFTPSettings.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/SFTPSettings.java`
**Lines:** 61 | **Methods:** 14 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q03-01 | 3 | LOW | Naming | Class name `SFTPSettings` does not follow the project's `*Bean` suffix convention for bean classes. |
| Q03-02 | 7-8 | LOW | Sensitive data | Fields `sftpUser` and `sftpPass` store SFTP credentials as plain-text Strings. No indication of encryption or secure handling. Credentials stored in bean may be serialized or logged. |

**Reading evidence:** Pure POJO, 61 lines, no imports beyond package declaration, no business logic.

---

### 4. ServiceDueFlagBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`
**Lines:** 1003 | **Methods:** ~53

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q04-01 | 1-1003 | HIGH | God class | 1003 lines with ~53 methods. This class combines data holding (bean fields), database connection management, and business logic (service due calculation). Exceeds both the 1000-line and 20-method thresholds. |
| Q04-02 | 104-165, 543-561, 564-606, 634-726, 728-883, 886-942, 944-954, 956-964, 966-999 | HIGH | DB access in bean / Layering violation | Bean class directly performs JNDI lookups (line 107), opens JDBC connections (line 114), creates Statements (line 116), and executes raw SQL queries throughout. This is a severe layering violation -- a bean should not contain data access logic. Methods `init()`, `testQueries()`, `Fetch_report_nm()`, `Fetch_service_status_veh()`, `Fetch_serv_mnt_data()`, `getHrAtLastServ()`, `Fetch_service_reminder()`, `getDept_prefix()` all perform direct DB access. |
| Q04-03 | 557, 568-569, 580-581, 587-592, 637-639, 647, 656-660, 691, 735, 743-744, 767, 783, 790, 798-806, 855, 895-897, 902-904, 947, 980 | HIGH | SQL injection | All SQL queries built via string concatenation with user-controllable variables (`veh_cd`, `set_cust_cd`, `set_loc_cd`, `form_cd`, `set_ucd`, `st_dt`, `end_dt`, `vehicle_cd`, `hex`, `dateS`, `count`). No use of PreparedStatement. |
| Q04-04 | 129-130 | MEDIUM | e.printStackTrace() | `exception.printStackTrace()` in `init()` method catch block. |
| Q04-05 | 912-913 | MEDIUM | e.printStackTrace() | `exception.printStackTrace()` in `getHrAtLastServ()` method catch block. |
| Q04-06 | 990 | MEDIUM | e.printStackTrace() | `e.printStackTrace()` in `getDept_prefix()` method catch block. |
| Q04-07 | 129 | MEDIUM | Broad catch | `catch (Exception exception)` in `init()` -- catches all exceptions including unchecked ones. |
| Q04-08 | 912 | MEDIUM | Broad catch | `catch (Exception exception)` in `getHrAtLastServ()`. |
| Q04-09 | 988 | MEDIUM | Broad catch | `catch(Exception e)` in `getDept_prefix()`. |
| Q04-10 | 697-712 | MEDIUM | Commented-out code | Large block of commented-out SQL query logic (approximately 15 lines). Multiple alternative query strategies left commented out. |
| Q04-11 | 797-806 | MEDIUM | Commented-out code | Multiple lines of commented-out join clauses and conditions in `Fetch_serv_mnt_data()` (lines 800, 803-805, 845). |
| Q04-12 | 44-62, 74-75 | MEDIUM | Raw types | All `ArrayList` declarations use raw types without generic parameters (e.g., `private ArrayList lastServDateList = new ArrayList()`). There are approximately 20 raw-type ArrayList fields. |
| Q04-13 | 564, 634, 728, 944 | LOW | Naming | Private methods use PascalCase: `Fetch_report_nm()`, `Fetch_service_status_veh()`, `Fetch_serv_mnt_data()`, `Fetch_service_reminder()`. Java convention requires camelCase for method names. |
| Q04-14 | 63, 74-75, 86-88 | LOW | Package-private fields | Fields `t_sm_hm_s`, `vmachine_cd`, `vs_no`, `is_user_admin`, `is_user_lmh`, `access_cust` declared without access modifier (package-private). Inconsistent with other fields that are declared `private`. |
| Q04-15 | 65-66, 68 | LOW | Leaky abstraction | Bean exposes `Connection`, `Statement`, and `ResultSet` fields with public getters/setters (`getStmt()`, `setStmt()`, `getStmt1()`, `setStmt1()`). JDBC implementation details should not leak through a bean's public API. |
| Q04-16 | 846-879 | MEDIUM | N+1 query | The loop at line 846 iterates over `vmachine_cd` and executes a query per vehicle (line 856) and potentially another via `getHrAtLastServ()` (line 878) which itself opens a new connection and executes 1-2 queries. This is an N+1 (or N+2) query pattern. |
| Q04-17 | 8-11 | LOW | Unused imports | `java.text.ParseException` imported at line 11 but only thrown by `testQueries()` (declared in signature). `javax.servlet.http.HttpServletRequest` imported at line 21 but field `request` (line 65) is never read/used in any method. |
| Q04-18 | 991 | LOW | Dead code | `e.getMessage()` called at line 991 but return value is discarded -- has no effect. |
| Q04-19 | 7, 9 | LOW | Unused imports | `java.sql.Timestamp` is used. `java.text.ParseException` usage is limited to method signature declaration only. `javax.servlet.http.HttpServletRequest` import at line 21 -- field `request` at line 65 is never used by any method in the class. |

**Reading evidence:** 1003 lines. Contains JNDI lookup in `init()`, raw SQL via `stmt.executeQuery(query)`, `conn.createStatement()`, `DBUtil.getConnection()`, and direct `ResultSet` iteration. Mixes data-holding (50+ fields with getters/setters) with data-access (8+ methods executing SQL) and business logic (service due calculation, color status). Heavy class carrying multiple responsibilities.

---

### 5. SiteConfigurationBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java`
**Lines:** 157 | **Methods:** 34 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q05-01 | 11-30 | LOW | Package-private fields | All fields (17 fields including `id`, `module_type`, `reader_type`, `sim_supplier`, `sim_type`, `driver_base`, `time_base`, `timeslot1-4`, `idle_timer`, `survey_timer`, `contact_nm`, `contact_no`, `contact_email`, `comments`, `idtype`, `facility_code`, `super_card`) are declared package-private (no access modifier). Should be `private`. |

**Reading evidence:** Pure POJO implementing `Serializable`, 157 lines. No business logic, no DB access.

---

### 6. SpareModuleBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/SpareModuleBean.java`
**Lines:** 120 | **Methods:** 30 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q06-01 | 5-20 | LOW | Naming | Field names use snake_case (`spare_modules_cd`, `spare_status_cd`, `spare_status`, `from_serial`, `last_updated`, `swap_date`, `ra_number`, `from_gmtp_id`, `tech_number`). Inconsistent -- some fields are camelCase-adjacent (`gmtp_id`, `ccid`). |

**Reading evidence:** Pure POJO, 120 lines. No imports, no business logic, no DB access.

---

### 7. SpecialAccessBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/SpecialAccessBean.java`
**Lines:** 70 | **Methods:** 16 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q07-01 | 5-13 | LOW | Package-private fields | All fields (`id`, `user_cd`, `cust_cd`, `loc_cd`, `dept_cd`, `custName`, `userName`, `module_cd`, `enabled`) are declared package-private. Should be `private`. |

**Reading evidence:** Pure POJO, 70 lines. No imports, no business logic, no DB access.

---

### 8. SubscriptionBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/SubscriptionBean.java`
**Lines:** 51 | **Methods:** 10 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q08-01 | 14-19 | LOW | Package-private fields | Fields `id`, `cust_cd`, `loc_cd`, `dept_cd`, `month`, `email` are declared package-private despite class implementing `Serializable`. Should be `private`. |

**Reading evidence:** Pure POJO implementing `Serializable`, 51 lines. Unused import: `java.util.ArrayList` imported on line 4 but never used.

> Note: `java.util.ArrayList` import at line 4 is unused.

---

### 9. SuperMasterAuthBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java`
**Lines:** 69 | **Methods:** 15 (1 constructor + 14 getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q09-01 | 8 | LOW | TODO stub | Constructor contains only `// TODO Auto-generated constructor stub`. Dead auto-generated comment. |

**Reading evidence:** Pure POJO, 69 lines. Multiple fields declared on a single line (line 5). No business logic, no DB access.

---

### 10. UnitBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitBean.java`
**Lines:** 166 | **Methods:** 34 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q10-01 | 13-33 | LOW | Package-private fields | All 18 fields (`veh_cd`, `gmtp_id`, `cust_nm`, `loc_nm`, `dept_nm`, `model`, `state`, `hire_no`, `serial_no`, `active_date`, `cur_version`, `sim_provider`, `ccid`, `old_ccid`, `ccid_rpt_time`, `moderm_version`, `old_gmtpid`, `last_session`, `service_from`, `service_hour`, `threshold`) are declared package-private despite class being `Serializable`. |

**Reading evidence:** Pure POJO implementing `Serializable`, 166 lines. Import of `java.util.Date` is used for `active_date` field. No business logic, no DB access. Typo in field name: `moderm_version` (should be `modem_version`).

---

### 11. UnitUtilSummaryBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitUtilSummaryBean.java`
**Lines:** 113 | **Methods:** 26 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q11-01 | 12-25 | LOW | Package-private fields | All 13 fields are declared package-private. Should be `private`. |

**Reading evidence:** Pure POJO implementing `Serializable`, 113 lines. No business logic, no DB access.

---

### 12. UnitVersionInfoBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitVersionInfoBean.java`
**Lines:** 33 | **Methods:** 6 (getters/setters)

No findings. Clean, small POJO. All fields are properly declared `private`. Follows camelCase convention. No DB access, no business logic.

**Reading evidence:** 33 lines, 3 private boolean fields and 1 private String field with corresponding getters/setters.

---

### 13. UnitutilBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java`
**Lines:** 189 | **Methods:** 30 (1 constructor + 29 getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q13-01 | 14-32 | LOW | Package-private fields | All fields are declared package-private. Fields include complex types (`HashMap`, `ArrayList`, `int[]`) that should ideally be encapsulated behind `private` access. |

**Reading evidence:** POJO implementing `Serializable`, 189 lines. Uses `HashMap` and `ArrayList` with proper generics. Constructor initializes `util` array. No DB access, no business logic beyond initialization.

---

### 14. UnusedUnitBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnusedUnitBean.java`
**Lines:** 90 | **Methods:** 22 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q14-01 | 11-21 | LOW | Package-private fields | All fields are declared package-private despite class being `Serializable`. |

**Reading evidence:** Pure POJO implementing `Serializable`, 90 lines. No business logic, no DB access.

---

### 15. UserBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java`
**Lines:** 51 | **Methods:** 12 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q15-01 | 5-10 | LOW | Package-private fields | All fields (`id`, `username`, `firstname`, `lastname`, `email`, `lastUpdate`) are declared package-private. |

**Reading evidence:** Pure POJO, 51 lines. No imports, no business logic, no DB access.

---

### 16. UserDriverBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserDriverBean.java`
**Lines:** 50 | **Methods:** 12 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q16-01 | 5-10 | LOW | Package-private fields / Naming | All fields are package-private. Mixed naming convention: `user_cd`, `veh_type` use snake_case while `firstName`, `lastName` use camelCase. |

**Reading evidence:** Pure POJO, 50 lines. No imports, no business logic, no DB access.

---

### 17. UserFormBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java`
**Lines:** 59 | **Methods:** 14 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q17-01 | 9-14 | LOW | Package-private fields | Fields `userFomrCd`, `userFomrName`, `userFormMenuView`, `userFormMenuEdit`, `userFormDelete`, `userFormMenuPrint` are package-private. |
| Q17-02 | 4 | LOW | Unused import | `java.util.ArrayList` is imported but never used in the class. |

**Reading evidence:** Pure POJO, 59 lines. Typo in field names: `userFomrCd` and `userFomrName` (should be `userFormCd` and `userFormName`).

---

### 18. VehDiagnostic.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/VehDiagnostic.java`
**Lines:** 218 | **Methods:** 34 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q18-01 | 5-30 | LOW | Package-private fields | All fields are declared package-private. 19 fields total including mixed primitive and String types. |

**Reading evidence:** Pure POJO, 218 lines. No imports, no business logic, no DB access. Class name does not use `Bean` suffix (naming inconsistency with rest of package).

---

### 19. VehNetworkSettingsBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/VehNetworkSettingsBean.java`
**Lines:** 35 | **Methods:** 6 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q19-01 | 4, 29-31 | LOW | Package-private fields / Style | Fields `index`, `country`, `ssid`, `password` declared package-private. Additionally, field declarations are placed after the getter/setter methods (lines 29-31), which is unconventional. The field `index` is declared at the top (line 4) but the remaining fields are declared at the bottom (lines 29-31). |
| Q19-02 | 31 | LOW | Sensitive data | Field `password` stores network password as a plain-text String with a public getter. No indication of encryption or secure handling. |

**Reading evidence:** Pure POJO, 35 lines. No imports, no business logic, no DB access.

---

### 20. VehicleImportBean.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/VehicleImportBean.java`
**Lines:** 140 | **Methods:** 28 (getters/setters)

| ID | Line(s) | Severity | Category | Description |
|----|---------|----------|----------|-------------|
| Q20-01 | 5-23 | LOW | Naming | Mixed naming: snake_case fields (`site_name`, `department_name`, `gmtp_id`, `serial_no`, `surv_to`, `question_sched`, `seat_idle`) alongside camelCase fields (`equipNo`, `canRule`, `custCd`, `servHrsInterval`, `dateInterval`, `lastServDate`, `canUnit`). |

**Reading evidence:** Pure POJO, 140 lines. No imports beyond package, no business logic, no DB access. Opening brace on new line (line 4) deviates from the K&R style used by most other files.

---

## Critical File: ServiceDueFlagBean.java -- Detailed Breakdown

This file is the only file in the audited set that contains significant logic and carries the vast majority of findings. A summary of its structural issues:

1. **Responsibilities mixed into one class:**
   - Data holding (50+ fields with getters/setters)
   - JNDI connection management (`init()`)
   - SQL query execution (8+ methods)
   - Business logic (service interval calculation, color coding)
   - Utility conversion (`convertServiceHour`, `convertServiceHourAvg`)

2. **SQL injection vectors:** Every SQL query is built via string concatenation. Variables `veh_cd`, `set_cust_cd`, `form_cd`, `set_ucd`, `st_dt`, `end_dt`, `vehicle_cd`, `hex`, `dateS` are all concatenated directly into SQL strings without parameterization.

3. **Resource management pattern:** Manual try/finally cleanup of `Connection`, `Statement`, `ResultSet` in multiple places. Method `getHrAtLastServ()` opens its own connection via `DBUtil.getConnection()` while the enclosing class already holds a connection as a field -- creating parallel connection management paths.

4. **N+1 query in `Fetch_serv_mnt_data()`:** Lines 846-880 loop through vehicles, executing 1 query per vehicle for service settings (line 856), and calling `getHrAtLastServ()` which opens a new connection and executes 1-2 more queries per vehicle.

---

## Cross-Cutting Observations

### Pervasive Package-Private Fields
15 of the 20 files declare fields without an access modifier (package-private). Only `QuestionBean`, `ServiceDueFlagBean` (partially), `SFTPSettings`, `SpareModuleBean`, and `VehicleImportBean` use `private` for fields. This is a systemic pattern across the bean package.

### Naming Inconsistency
The codebase uses a mixture of snake_case and camelCase for field names, even within single classes. Getter/setter names then propagate the underscore-based names (e.g., `getUser_cd()`), creating a non-standard JavaBean API surface.

### Missing Bean Suffix
Two files (`SFTPSettings.java`, `VehDiagnostic.java`) do not follow the `*Bean` naming convention used by the rest of the package.

### Typos in Field Names
- `moderm_version` in `UnitBean.java` (should be `modem_version`)
- `userFomrCd` and `userFomrName` in `UserFormBean.java` (should be `userFormCd` and `userFormName`)
- `dateInteval` in `ServiceDueFlagBean.java` (should be `dateInterval`)

---

## Risk Summary

| Risk Level | Count | Key Concern |
|------------|------:|-------------|
| HIGH | 3 | ServiceDueFlagBean: God class, layering violation, SQL injection |
| MEDIUM | 10 | e.printStackTrace(), broad catches, commented-out code, raw types, N+1 queries |
| LOW | 29 | Naming conventions, package-private fields, unused imports, TODO stubs, sensitive plaintext data |

**Overall assessment:** 19 of 20 files are clean POJOs with only minor style/convention issues. `ServiceDueFlagBean.java` is the critical outlier, concentrating all HIGH-severity findings. It should be refactored to extract data access into a DAO/service layer, use PreparedStatements, and eliminate the God class anti-pattern.

---

*End of report -- Pass 4, bean package Q-Z*
