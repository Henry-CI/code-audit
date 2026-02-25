# Security Audit — Bean Java Files
**Audit ID:** A07
**Run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/bean/` (51 files), `linde/bean/` (1 file), `excel/reports/beans/` (28 files)

---

## STEP 3 — File Inventory Summary

### Package: `com.torrent.surat.fms6.bean`

| File | Class | Serializable | Notable Fields |
|------|-------|-------------|----------------|
| UserBean.java | `UserBean` | No | id, username, firstname, lastname, email, lastUpdate |
| DriverBean.java | `DriverBean` | Yes | id, user_cd, weigand, veh_type |
| CustomerBean.java | `CustomerBean` | No | id, passwordPolicy, active |
| UnitBean.java | `UnitBean` | Yes | veh_cd, gmtp_id, cust_nm, ccid, sim_provider, serial_no |
| SuperMasterAuthBean.java | `SuperMasterAuthBean` | No | fleetNo, serialNo, authStart, authEnd, **superMasterCode**, custName |
| SFTPSettings.java | `SFTPSettings` | No | customerCd, sftpAddress, sftpUser, **sftpPass**, sftpDir |
| NetworkSettingBean.java | `NetworkSettingBean` | Yes | index, country, ssid, **password** |
| VehNetworkSettingsBean.java | `VehNetworkSettingsBean` | No | index, country, ssid, **password** |
| LockOutBean.java | `LockOutBean` | Yes | id, fleetno, type, lockouttime, driver, unlocktime, **master_code** |
| SiteConfigurationBean.java | `SiteConfigurationBean` | Yes | id, module_type, reader_type, sim_supplier, contact_nm, contact_no, contact_email, **facility_code**, **super_card** |
| UserFormBean.java | `UserFormBean` | No | id, userFomrCd, userFomrName, userFormMenuView, userFormMenuEdit, userFormDelete, userFormMenuPrint |
| SpecialAccessBean.java | `SpecialAccessBean` | No | id, user_cd, cust_cd, loc_cd, dept_cd, custName, userName, module_cd, enabled |
| UserDriverBean.java | `UserDriverBean` | No | id, user_cd, weigand, veh_type, firstName, lastName |
| DriverImportBean.java | `DriverImportBean` | Yes | id, first_name, last_name, **licno**, phone, location, card_no, facility_code, access_level, access_cust, access_site, access_dept |
| ServiceDueFlagBean.java | `ServiceDueFlagBean` | No | Contains embedded SQL via `java.sql.*`, HttpServletRequest, opCode, set_cust_cd, is_user_admin, access_cust — builds SQL queries by string concatenation |
| LicenseBlackListBean.java | `LicenseBlackListBean` | No | vehicleType, custCd, locCd, deptCd, driverCd, access_level, access_cust, access_site, access_dept |
| SubscriptionBean.java | `SubscriptionBean` | Yes | id, cust_cd, loc_cd, dept_cd, month, email |
| MymessagesUsersBean.java | `MymessagesUsersBean` | Yes | id, cust_cd, loc_cd, dept_cd, threshold, user_id, user_email |
| NotificationSettingsBean.java | `NotificationSettingsBean` | No | notification_id, header, title, content, signature, enabled |
| BroadcastmsgBean.java | `BroadcastmsgBean` | Yes | text, type, driver, unit, veh_id |
| FleetCheckBean.java | `FleetCheckBean` | No | unitName, avg_completion_time |
| PreCheckBean.java | `PreCheckBean` | Yes | id, name, complete, incomplete, total, dept_id |
| PreCheckDriverBean.java | `PreCheckDriverBean` | Yes | total, driver_cd, driver_name |
| PreCheckSummaryBean.java | `PreCheckSummaryBean` | Yes | loc_cd, loc_name |
| QuestionBean.java | `QuestionBean` | No | user_cd, loc_cd, dept_cd, veh_typ_cd, question, exp_ans, crit_ans, custCd, access_level |
| EntityBean.java | `EntityBean` | Yes | id, name, totalno, attribute, locs, depts |
| MenuBean.java | `MenuBean` | No | Menus_Cd, Menus_Name, Form_Cd, Form_Name, Form_Path, ReskinPath |
| ImpactBean.java | `ImpactBean` | Yes | cust_cd, loc_cd, dept_cd, driver_cd, driver_name, unit_cd |
| ImpactDeptBean.java | `ImpactDeptBean` | Yes | dept_cd, dept_name |
| ImpactLocBean.java | `ImpactLocBean` | Yes | loc_cd, loc_name |
| ImpactSummaryBean.java | `ImpactSummaryBean` | Yes | loc_cd, loc_name, driver_cd, driver_name |
| DriverLeagueBean.java | `DriverLeagueBean` | No | id, driverName, department, truckType, redImpact, preOp |
| DailyUsageDeptDataBean.java | `DailyUsageDeptDataBean` | Yes | dept_id, dept_name, modelName |
| DailyUsageHourBean.java | `DailyUsageHourBean` | Yes | (aggregation bean) |
| DayhoursBean.java | `DayhoursBean` | Yes | id, total_hours, break_hours |
| MaxHourUsageBean.java | `MaxHourUsageBean` | Yes | model_name, model_img |
| UnitutilBean.java | `UnitutilBean` | Yes | veh_cd, vmachine_nm, dept_cd, loc_cd |
| UnitUtilSummaryBean.java | `UnitUtilSummaryBean` | Yes | hire_no, serial_no, model_nm, total_hours |
| UnitBean.java | `UnitBean` | Yes | veh_cd, gmtp_id, cust_nm, loc_nm, ccid, old_ccid, sim_provider, serial_no |
| UnitVersionInfoBean.java | `UnitVersionInfoBean` | No | gmtpId, char100MaxSupported |
| UnusedUnitBean.java | `UnusedUnitBean` | Yes | cust_name, site_name, fleet_no, serial_no, gmtp_id, ccid |
| VehDiagnostic.java | `VehDiagnostic` | No | vehicleCd, ccid, apn, firmwareVer, ccid, shockThreshold |
| VehicleImportBean.java | `VehicleImportBean` | No | gmtp_id, serial_no, custCd, canRule |
| RestrictedAccessUsageBean.java | `RestrictedAccessUsageBean` | No | fleetNo, serialNo, hourlyRate, maxMonthlyRate, totalCharge |
| SpareModuleBean.java | `SpareModuleBean` | No | gmtp_id, ccid, ra_number, from_serial, tech_number |
| CanruleBean.java | `CanruleBean` | No | gmtp_id, custCd, access_level, access_cust, access_site, access_dept |
| BatteryBean.java | `BatteryBean` | Yes | batteryId, unit_cd, bef_dri_nm, aft_dri_nm |
| DehireBean.java | `DehireBean` | No | vehCd, hire_time, dehire_time |
| CustLocDeptBean.java | `CustLocDeptBean` | No | custCd, locCd, deptCd |
| DetailedReportUtil.java | `DetailedReportUtil` | No | (report aggregation, raw ArrayList, debug System.out.println) |
| ServiceDueFlagBean.java | `ServiceDueFlagBean` | No | *see SQL injection findings* |

### Package: `com.torrent.surat.fms6.linde.bean`

| File | Class | Serializable | Notable Fields |
|------|-------|-------------|----------------|
| SupervisorUnlockBean.java | `SupervisorUnlockBean` | No | supervisorName, impactCount, surveyCount, criticalCount |

### Package: `com.torrent.surat.fms6.excel.reports.beans` (28 files — data-holder beans, no SQL)

All are plain data-holder beans; no embedded SQL was found in this package.

---

## STEP 4 — Security Review Notes (Pre-Finding)

**UserBean — password/tenant scoping:**
`UserBean` stores `id`, `username`, `firstname`, `lastname`, `email`, `lastUpdate`. It does NOT store a password field and does NOT store a `customer_id`/tenant scoping field. There is no session-level tenant boundary encoded in this bean. A separate mechanism must provide tenant scoping; this is architecturally risky (see A07-5).

**Password/credential fields in beans:**
- `SFTPSettings.sftpPass` — plain string, getter `getSftpPass()` returns raw value. No indication of encryption.
- `NetworkSettingBean.password` and `VehNetworkSettingsBean.password` — WiFi PSKs in plain strings with public getters. `NetworkSettingBean` also implements `Serializable`.
- `LockOutBean.master_code` — override/master code stored in a `Serializable` bean.
- `SiteConfigurationBean.super_card` and `facility_code` — access-control secrets in a `Serializable` bean.
- `SuperMasterAuthBean.superMasterCode` — privileged bypass code, full getter/setter pair, no protection.

**SQL injection in ServiceDueFlagBean:**
This bean contains `java.sql.*` imports, a `Connection`, `Statement`, and `ResultSet` directly, and builds query strings via string concatenation using externally-supplied values (`form_cd`, `set_ucd`, `veh_cd`, `set_cust_cd`, `st_dt`, `end_dt`, `end_dt`, `vehicle_cd`, `ucd_str`). No `PreparedStatement` is used anywhere in the file.

**Serializable beans with sensitive state:**
`NetworkSettingBean` implements `Serializable` and stores a WiFi `password` in a plain string. If this bean is placed in an HTTP session, the password will appear in any session serialization store (file, database, replicated cluster).

**PII in driver beans:**
`DriverImportBean` (Serializable) stores `first_name`, `last_name`, `licno` (licence number), `phone`, `card_no`, `facility_code`. Full getter/setter for every field.
`UserDriverBean` stores `firstName`, `lastName`, `weigand` (physical access card code).

**Mass assignment — no input filtering:**
Every bean has a complete set of public setters for every field, including fields that control authorisation scope (`access_level`, `access_cust`, `access_site`, `access_dept`, `enabled`, `is_user_admin`). There is no whitelist or input-binding restriction layer visible in the beans.

**ServiceDueFlagBean.is_user_admin:**
A public mutable `Boolean is_user_admin` flag stored directly in the bean with a full public setter `setIs_user_admin(Boolean)`. If this bean is bound from HTTP request parameters, an attacker could POST `is_user_admin=true`.

**Debug output:**
`DetailedReportUtil` (constructor) calls `System.out.println` with field counts, which logs to the application server stdout/logs — minor information leakage to server logs.

---

## STEP 5 — Findings

---

### A07-1 — SFTP Password Stored and Exposed in Plaintext

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SFTPSettings.java`
**Lines:** 8, 26
**Severity:** High
**Category:** A02:2021 Cryptographic Failures / Sensitive Data Exposure

**Description:**
The `SFTPSettings` bean stores an SFTP password in a plain `String` field with a public getter that returns the raw value. There is no indication that the password is encrypted at rest in the database, obfuscated in memory, or scrubbed after use. If this bean is logged, serialized, or rendered into a view context, the credential is exposed.

**Evidence:**
```java
// SFTPSettings.java line 8
private String sftpPass = "";

// SFTPSettings.java line 25-27
public String getSftpPass() {
    return sftpPass;
}
```

**Recommendation:**
Store SFTP credentials encrypted in the database (e.g., AES-256-GCM with a server-side key). Do not expose the raw credential via a getter in a bean that is passed to view templates. If the bean is used in JSPs/EL expressions, the password will be rendered. Consider a separate credential-fetch path that never materialises the secret in the bean.

---

### A07-2 — WiFi PSK Stored in Serializable Bean with Public Getter

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/NetworkSettingBean.java`
**Lines:** 3–5, 10, 30–34
**Severity:** High
**Category:** A02:2021 Cryptographic Failures / Sensitive Data Exposure

**Description:**
`NetworkSettingBean` implements `java.io.Serializable` and stores a WiFi pre-shared key (`password`) as a plain String. Because the bean is `Serializable`, any session persistence mechanism (Tomcat file/JDBC session store, cluster replication) will write the password to disk or a database in plaintext. The password is also returned verbatim by `getPassword()`.

The non-Serializable sibling `VehNetworkSettingsBean` has the same password exposure but without the serialization risk.

**Evidence:**
```java
// NetworkSettingBean.java line 3-5
public class NetworkSettingBean implements Serializable{
    ...
    private String password = "";

// line 30-34
public String getPassword() {
    return password;
}
public void setPassword(String password) {
    this.password = password;
}
```

**Recommendation:**
Do not store network credentials in beans that are placed in the HTTP session or serialized. If the PSK must be held transiently, do not implement `Serializable`, clear the field after use, and avoid passing the bean to view-layer templates.

---

### A07-3 — Master/Override Codes Stored in Serializable Beans

**Files:**
- `WEB-INF/src/com/torrent/surat/fms6/bean/LockOutBean.java` lines 17, 49–53
- `WEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java` lines 5, 31–33
- `WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java` lines 30–31, 148–153

**Severity:** High
**Category:** A02:2021 Cryptographic Failures / Sensitive Data Exposure

**Description:**
Three beans store privileged override codes in plain string fields with full getter/setter pairs:

1. `LockOutBean.master_code` — the override code used to unlock a locked-out vehicle. The bean implements `Serializable`.
2. `SuperMasterAuthBean.superMasterCode` — a super-master bypass code with date-bounded authorisation window. Not Serializable, but has a full getter.
3. `SiteConfigurationBean.super_card` and `facility_code` — physical access control card values stored in a `Serializable` bean.

Any of these appearing in session serialization, application logs, or report output would expose the override mechanism to attackers.

**Evidence:**
```java
// LockOutBean.java line 17
String master_code = "";

// LockOutBean.java line 49-53
public String getMaster_code() {
    return master_code;
}

// SuperMasterAuthBean.java line 5
private String fleetNo,serialNo,authStart,authEnd,servHourFrom,superMasterCode,custName;

// SuperMasterAuthBean.java line 31-33
public String getSuperMasterCode() {
    return superMasterCode;
}

// SiteConfigurationBean.java line 30-31
String facility_code = "";
String super_card = "";
```

**Recommendation:**
Override codes should not be placed in beans that are passed to view layers or serialized in sessions. Treat them as short-lived secrets: fetch them only when needed, clear after use, and never log them. For the `SuperMasterAuthBean` — the report bean `SuperMasterAuthReportBean` exposes a full list of these codes via its getter; confirm that the report is only accessible to administrators, and redact the code value in rendered output.

---

### A07-4 — SQL Injection in ServiceDueFlagBean via String Concatenation

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`
**Lines:** 557, 568–570, 580–592, 638–640, 647, 660, 691, 713–715, 745, 767, 783–790, 855, 895–897, 902–904, 946–948, 980
**Severity:** Critical
**Category:** A03:2021 Injection — SQL Injection

**Description:**
`ServiceDueFlagBean` is a bean-class that also contains full database access logic using `java.sql.Statement` (not `PreparedStatement`). Every query in the file is built by direct string concatenation of field values that are externally supplied. Affected parameters include: `form_cd`, `set_ucd`, `veh_cd`, `set_cust_cd`, `st_dt`, `end_dt`, `tmp_veh_cd`, `ucd_str` (extracted from `access_cust`), and `vehicle_cd` (passed to `getHrAtLastServ()`).

Several of the most dangerous cases:

1. **`form_cd` injected into access-rights query (lines 568–592):** `form_cd` comes from an externally-settable field. It is concatenated into a query that reads the user's edit/delete/print permissions. An attacker who can control `form_cd` can read or manipulate these checks.

2. **`veh_cd` inserted bare into queries (lines 638–640, 647, 660, 691):** `veh_cd` is concatenated directly into SQL with no quoting or type enforcement.

3. **`ucd_str` from `access_cust` (lines 742–744):** The code builds an IN-clause by substring-slicing `access_cust` and embedding it directly: `"where \"USER_CD\"in (" + ucd_str + ")"`. If `access_cust` can be influenced by user input, this is a direct injection point.

4. **`st_dt` / `end_dt` date parameters (lines 783–794):** Date strings from the bean are injected directly into `select '"+st_dt+"'::timestamp`.

5. **`testQueries` method (line 557):** A test method remains in production code that builds and executes raw queries using `hex` and `dateS` parameters.

**Evidence:**
```java
// ServiceDueFlagBean.java line 568-570
query = "select \"FORM_NAME\"  from \"FMS_FORM_MST\" where \"FORM_CD\"='"
    + form_cd + "' ";

// line 580-583
query = "select  \"GROUP_CD\" from \"FMS_USR_GRP_REL\" where \"USER_CD\" = '"
    + set_ucd + "' ";

// line 587-592
query = "select \"EDIT\",\"DELETE\",\"PRINT\"  from \"FMS_GROUP_ACCESS_RIGHT\" where \"FORM_CD\"='"
    + form_cd
    + "' and "
    + " \"GROUP_CD\" = '"
    + gcd
    + "'";

// line 638-640
query = " select \"HIRE_NO\" from \"FMS_SERV_MST\",\"FMS_USR_VEHICLE_REL\",\"FMS_VEHICLE_MST\" "
    + " where   \"FMS_VEHICLE_MST\".\"VEHICLE_CD\" = \"FMS_SERV_MST\".\"VEHICLE_CD\" and \"FMS_SERV_MST\".\"VEHICLE_CD\" = "
    + veh_cd;

// line 742-745 (ucd_str injected into IN clause)
String ucd_str = access_cust.substring(2, access_cust.length());
query = "select \"USER_CD\",\"USER_NAME\" "
    + "  from \"FMS_CUST_MST\" where \"USER_CD\"in (" + ucd_str
    + ") and \"ACTIVE\" is true order by \"USER_NAME\" ";

// line 783-784
query = "select '"+ st_dt + "'::timestamp";

// line 895-897
query = "select hm from fms_hm_history_mst where veh_cd = "
    + vehicle_cd + " and utc_time <='"+end_dt
    +"'::timestamp order by utc_time desc limit 1";
```

**Recommendation:**
Replace all `Statement` usage in `ServiceDueFlagBean` with `PreparedStatement` with parameterised binds. Validate and type-cast integer IDs (`veh_cd`, `set_cust_cd`) to integers before use. The `testQueries` method must be removed from production code. Consider refactoring this god-class: database logic does not belong in a bean.

---

### A07-5 — UserBean Has No Tenant (customer_id) Scoping Field

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java`
**Lines:** 3–51
**Severity:** Medium
**Category:** A01:2021 Broken Access Control — Missing Tenant Context

**Description:**
`UserBean` stores only `id`, `username`, `firstname`, `lastname`, `email`, and `lastUpdate`. It does not include any `customer_id`/`cust_cd` field that binds the user to a tenant. In a multi-tenant SaaS context, the absence of a tenant-binding field in the primary user bean means that the application must rely entirely on separate session attributes or service-layer checks to enforce data isolation.

If `UserBean` is the primary user context object stored in the HTTP session, any code path that queries data using only the user's `id` without re-fetching the tenant binding is at risk of cross-tenant data leakage. The review cannot confirm whether a separate session attribute carries `cust_cd`, but the bean itself provides no tenant guardrail.

**Evidence:**
```java
// UserBean.java — complete field list
int id;
String username;
String firstname;
String lastname;
String email;
String lastUpdate;
// No cust_cd, customer_id, or tenant_id field.
```

**Recommendation:**
Add a `custCd` (or `tenantId`) field to `UserBean` and populate it from the database at login. Enforce in all data-access paths that the customer code is sourced from the authenticated session `UserBean`, not from request parameters. This ensures the user's tenant scope cannot be overridden by a manipulated request.

---

### A07-6 — DriverImportBean (Serializable) Stores PII Without Data-Minimisation Controls

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverImportBean.java`
**Lines:** 5–31
**Severity:** Medium
**Category:** A02:2021 Cryptographic Failures / PII Data Exposure

**Description:**
`DriverImportBean` implements `Serializable` and stores the following PII and access-control data together in a single flat bean: `first_name`, `last_name`, `licno` (driver licence number), `phone`, `card_no` (physical access card), `facility_code`, `access_level`, `access_cust`, `access_site`, `access_dept`. Every field has a public getter and setter.

Because the bean is `Serializable`, placing it in the HTTP session or passing it through a session-replicated cluster will cause all PII fields, including the licence number and card number, to be written to disk or replicated storage in plaintext. There are no transient annotations, no scrubbing, and no data-minimisation — all PII travels with the bean even in contexts where only the `custCd` or `access_level` is needed.

**Evidence:**
```java
// DriverImportBean.java lines 5-31
public class DriverImportBean implements Serializable {
    private static final long serialVersionUID = -6234180688512824118L;
    private String first_name = null;
    private String last_name = null;
    private String licno = null;       // driver licence number
    private String phone = null;
    private String card_no = null;     // physical card number
    private String facility_code = null;
    private String access_level = null;
    private String access_cust = null;
    private String access_site = null;
    private String access_dept = null;
    ...
}
```

**Recommendation:**
Mark PII fields (`licno`, `phone`, `card_no`) as `transient` so they are excluded from Java serialization. Separate the access-control fields (`access_level`, `access_cust`, `access_site`, `access_dept`) into a distinct security-context class. Do not store driver PII in session-scoped beans; fetch only what is needed for the current operation.

---

### A07-7 — Mass Assignment Risk: is_user_admin Flag Has Public Setter

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`
**Lines:** 86, 527–532
**Severity:** High
**Category:** A01:2021 Broken Access Control — Mass Assignment / Privilege Escalation

**Description:**
`ServiceDueFlagBean` contains a `Boolean is_user_admin` flag with a public setter `setIs_user_admin(Boolean)`. This flag controls which customer list is fetched in `Fetch_serv_mnt_data()`: when `is_user_admin` is `true` and `set_cust_cd` is `"all"`, the query returns all active customer records. If the web layer uses Java bean population frameworks (e.g., Apache Commons BeanUtils, Spring MVC, or JSP `useBean` with `setProperty="*"`) to populate this bean from HTTP request parameters, an attacker could POST `is_user_admin=true` to gain admin-level data access.

**Evidence:**
```java
// ServiceDueFlagBean.java line 86
Boolean is_user_admin = false;

// line 527-532
public Boolean getIs_user_admin() {
    return is_user_admin;
}
public void setIs_user_admin(Boolean is_user_admin) {
    this.is_user_admin = is_user_admin;
}

// line 734-738 (consequence)
if(is_user_admin && set_cust_cd.equalsIgnoreCase("all")){
    query = "select \"USER_CD\" from \"FMS_CUST_MST\" where \"ACTIVE\" is true and \"USER_CD\"!=103 order by \"USER_NAME\" ";
```

**Recommendation:**
Remove the public setter for `is_user_admin`. This flag must be derived exclusively from the authenticated session user's role, never from HTTP input. Consider replacing the flag with a method that reads the role from the session at the point of use, or pass it via a constructor parameter from a trusted source only.

---

### A07-8 — Hardcoded Customer Exclusion (USER_CD != 103) in Service Query

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`
**Line:** 735
**Severity:** Low
**Category:** A05:2021 Security Misconfiguration — Hardcoded Business Logic

**Description:**
The admin-level customer list query contains a hardcoded exclusion: `"USER_CD\"!=103"`. This silently excludes customer 103 from admin-visible data. The intent is unknown from context, but hardcoded IDs in security-sensitive queries are a maintenance and auditability risk. If customer 103 is a test/internal account, its exclusion from admin queries could mask activity. If it is a live customer, this may represent undocumented privileged treatment.

**Evidence:**
```java
// ServiceDueFlagBean.java line 735
query = "select \"USER_CD\" from \"FMS_CUST_MST\" where \"ACTIVE\" is true and \"USER_CD\"!=103 order by \"USER_NAME\" ";
```

**Recommendation:**
Replace the hardcoded customer ID with a configurable exclusion list, a flag in the `FMS_CUST_MST` table (e.g., `EXCLUDE_FROM_ADMIN_VIEW`), or document the business reason in a code comment and a corresponding entry in the audit trail. Remove hardcoded IDs from query strings.

---

### A07-9 — Test/Debug Method Left in Production Bean

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`
**Lines:** 543–561
**Severity:** Medium
**Category:** A05:2021 Security Misconfiguration — Dead Code / Debug Artefacts

**Description:**
A `testQueries(int count)` method is present in the production bean. It is reachable via the `init()` method when `opCode.equalsIgnoreCase("test_queries")` (line 123). The method builds and executes a `sp_eos_message` stored procedure call using `hex` and `dateS` fields that are both settable via public setters. The `opCode` value controls which code path runs in `init()`, and `opCode` is set via a public setter, raising the possibility that the test mode can be triggered in production by an attacker who can invoke the bean's `init()` method.

**Evidence:**
```java
// ServiceDueFlagBean.java line 118-126
if(opCode.equals("vehicle_serv_new")){
    Fetch_service_status_veh();
}else if( opCode.equals("service_flag_new")){
    Fetch_serv_mnt_data();
    Fetch_service_reminder();
}else if(opCode.equalsIgnoreCase("test_queries")){
    testQueries(count);   // test method invocable via opCode setter
}

// line 557
query = "select sp_eos_message( '"+dateS+"', '2002f5b,"+hex+"', 'foc_0003282007', ...
```

**Recommendation:**
Remove the `testQueries` method entirely. Remove the `test_queries` branch from the `init()` dispatch. If functional testing of stored procedures is needed, use a dedicated test harness outside the production code path.

---

### A07-10 — Debug println Leaks Internal Data to Server Logs

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`
**Lines:** 39–41
**Severity:** Low
**Category:** A09:2021 Security Logging and Monitoring Failures — Information Leakage

**Description:**
The `DetailedReportUtil` constructor calls `System.out.println` with dataset sizes. While not directly sensitive, this indicates a pattern of debug logging to stdout throughout the codebase. Server stdout is often captured by application server logs that may be accessible to more personnel than intended. The same logging pattern appears in `ServiceDueFlagBean` (lines 131–133) which logs the failing SQL query string, potentially including user-controlled input and internal schema details.

**Evidence:**
```java
// DetailedReportUtil.java lines 39-41
System.out.println("vrpt_field_cd: " + vrpt_field_cd.size());
System.out.println("vrpt_field_nm: " + vrpt_field_nm.size());
System.out.println("vrpt_veh_value_stop: " + vrpt_veh_value_stop.size());

// ServiceDueFlagBean.java lines 131-133
System.out.println(" Exception in Databean_getuser In "
    + methodName + " \nquery " + query + " \nException :"
    + exception);
```

**Recommendation:**
Replace all `System.out.println` calls with a structured logging framework (e.g., SLF4J/Logback). Set appropriate log levels; debug/trace output must not emit at INFO or above in production. Critically, never log the full SQL query string to application logs as it may contain user-supplied input and sensitive values.

---

### A07-11 — LockOutBean Serializable with master_code Field

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/LockOutBean.java`
**Lines:** 5, 17, 49–54
**Severity:** Medium
**Category:** A02:2021 Cryptographic Failures — Sensitive Data in Serialized Session State

**Description:**
`LockOutBean` implements `Serializable` and stores `master_code` — the code used to unlock a locked-out vehicle — as a plain String field. If this bean is stored in the HTTP session or replicated across a cluster, the master code will be written to the session store in cleartext. An attacker with read access to the session storage (e.g., a compromised Tomcat session database, heap dump, or network intercept of session replication) could extract override codes for fleet vehicles.

**Evidence:**
```java
// LockOutBean.java
public class LockOutBean implements Serializable{
    private static final long serialVersionUID = 7995241917485082877L;
    String master_code = "";

    public String getMaster_code() {
        return master_code;
    }
```

**Recommendation:**
Mark `master_code` as `transient` to exclude it from serialization. If the master code must be held in session state, encrypt it with a session-specific key. Preferably, do not store override codes in session beans at all — retrieve them on demand from a secure store and clear immediately after use.

---

### A07-12 — SiteConfigurationBean Serializable with Facility Code and Super Card

**File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java`
**Lines:** 5, 29–31, 142–153
**Severity:** Medium
**Category:** A02:2021 Cryptographic Failures — Sensitive Data in Serialized Session State

**Description:**
`SiteConfigurationBean` implements `Serializable` and stores `facility_code` (physical access control facility code) and `super_card` (superuser access card value). These are physical security credentials used by the on-vehicle card reader system. Serializing them to session storage exposes them to any session-level compromise.

**Evidence:**
```java
// SiteConfigurationBean.java
public class SiteConfigurationBean implements Serializable{
    ...
    String facility_code = "";
    String super_card = "";

    public String getFacility_code() { return facility_code; }
    public String getSuper_card() { return super_card; }
```

**Recommendation:**
Mark `facility_code` and `super_card` as `transient`. These fields should not participate in Java serialization. If they must appear in a bean that is passed to a JSP, ensure they are not rendered in HTML output visible to the browser.

---

## Summary Table

| Finding ID | File | Line(s) | Severity | Category |
|------------|------|---------|----------|----------|
| A07-1 | SFTPSettings.java | 8, 26 | High | Plaintext credential exposure |
| A07-2 | NetworkSettingBean.java | 3–5, 10, 30–34 | High | WiFi PSK in Serializable bean |
| A07-3 | LockOutBean.java, SuperMasterAuthBean.java, SiteConfigurationBean.java | multiple | High | Override/bypass codes in beans |
| A07-4 | ServiceDueFlagBean.java | 557, 568–592, 638–660, 691–715, 742–794, 855, 895–904, 946–948, 980 | Critical | SQL Injection |
| A07-5 | UserBean.java | 3–51 | Medium | No tenant scoping field |
| A07-6 | DriverImportBean.java | 5–31 | Medium | PII in Serializable bean |
| A07-7 | ServiceDueFlagBean.java | 86, 527–532, 734 | High | Mass assignment — admin flag |
| A07-8 | ServiceDueFlagBean.java | 735 | Low | Hardcoded customer ID exclusion |
| A07-9 | ServiceDueFlagBean.java | 118–126, 543–561 | Medium | Test method in production code |
| A07-10 | DetailedReportUtil.java, ServiceDueFlagBean.java | 39–41, 131–133 | Low | SQL query and debug data logged to stdout |
| A07-11 | LockOutBean.java | 5, 17, 49–54 | Medium | master_code in Serializable bean |
| A07-12 | SiteConfigurationBean.java | 5, 29–31, 142–153 | Medium | Physical access codes in Serializable bean |

**Total findings: 12**

---

## Notes for Downstream Passes

- `ServiceDueFlagBean` requires a dedicated SQL-injection pass (it is a bean that contains full DAO logic, an anti-pattern that may be replicated in other bean classes).
- The session management architecture needs a dedicated pass to confirm whether `UserBean` is the primary session object and what mechanism carries the `cust_cd` tenant scope.
- All `Serializable` beans should be re-reviewed against the session storage configuration (file store vs. JDBC store vs. in-memory) to confirm the attack surface for the serialization findings.
- `SuperMasterAuthReportBean` (excel/reports/beans) exposes a list of `SuperMasterAuthBean` objects — the `superMasterCode` field value will appear in any Excel export. Confirm the report is access-controlled.
