# A04 — Security Audit: `util` Package (Database / Credential / Injection Layer)

**Auditor agent:** A04
**Run:** 2026-02-25-01
**Branch confirmed:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Package audited:** `com.torrent.surat.fms6.util`
**Package path:** `WEB-INF/src/com/torrent/surat/fms6/util/`
**Files reviewed:** 37 Java source files
**Total findings:** 26

---

## Finding Index

| ID | File | Category | Severity |
|----|------|----------|----------|
| A04-01 | RuntimeConf.java | Hardcoded Credentials | CRITICAL |
| A04-02 | CustomUpload.java | Hardcoded Credentials | CRITICAL |
| A04-03 | UtilBean.java | SQL Injection | CRITICAL |
| A04-04 | GdprDataDelete.java | SQL Injection | CRITICAL |
| A04-05 | password_life.java | SQL Injection | CRITICAL |
| A04-06 | SupervisorMasterHelper.java | SQL Injection | CRITICAL |
| A04-07 | MigrateMaster.java | SQL Injection | HIGH |
| A04-08 | fix_department.java | SQL Injection | HIGH |
| A04-09 | InfoLogger.java | SQL Injection | HIGH |
| A04-10 | mail.java | SQL Injection | HIGH |
| A04-11 | Menu_Bean.java | SQL Injection | HIGH |
| A04-12 | Menu_Bean1.java | SQL Injection | HIGH |
| A04-13 | call_mail.java | SQL Injection | HIGH |
| A04-14 | CftsAlert.java | SQL Injection | HIGH |
| A04-15 | DriverExpiryAlert.java | SQL Injection | HIGH |
| A04-16 | DriverMedicalAlert.java | SQL Injection | HIGH |
| A04-17 | send_updatepreop.java | SQL Injection | HIGH |
| A04-18 | FleetCheckFTP.java | SQL Injection | HIGH |
| A04-19 | GetHtml.java | SSRF | HIGH |
| A04-20 | DataUtil.java | SSRF / File Path Traversal | HIGH |
| A04-21 | ImportFiles.java | File Path Traversal | HIGH |
| A04-22 | CustomUpload.java | File Path Traversal | HIGH |
| A04-23 | EncryptTest.java | Weak Cryptography | HIGH |
| A04-24 | PasswordExpiryAlert.java | SQL Injection (Second-order) | MEDIUM |
| A04-25 | LogicBean_filter1.java | SQL Injection (ORDER BY) | LOW |
| A04-26 | Multiple files | Wildcard SQL Imports | LOW |

---

## Findings

---

### A04-01 — Hardcoded Credentials in RuntimeConf.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java`
**Lines:** 19, 20, 30, 54, 55, 87, 88, 89
**Severity:** CRITICAL
**Category:** Hardcoded Credentials / Secrets in Source

**Description:**
`RuntimeConf` is a public static configuration class whose fields are committed to source control. It contains eight plaintext credential values spanning FTP access, a legacy JDBC connection, a test account, and a third-party SMS gateway (Clickatell). Any developer with read access to the repository — or any attacker who reads a compiled `.class` file — has immediate access to all of these credentials. Several are referenced by other classes throughout the application (see A04-02, A04-18).

**Evidence:**
```java
// Lines 19-20 — FTP / firmware server credentials
public static String user     = "firmware";
public static String pass     = "ciifirmware";

// Line 30 — firmware FTP server password (also hardcoded in CustomUpload.java line 219)
public static String firmwarepass = "Sdh79HfkLq6";

// Lines 54-55 — test account credentials
public static String username = "TestK";
public static String password = "testadmin";

// Lines 87-89 — Clickatell SMS API credentials
public static String USERNAME = "collintell";
public static String PASSWORD = "fOqDVWYK";
public static String API_ID   = "3259470";
```

**Recommendation:**
Remove all credential literals from source code. Load secrets at runtime from environment variables, a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault), or an encrypted properties file that is excluded from version control. Rotate all exposed credentials immediately. For the Clickatell API, regenerate the API key.

---

### A04-02 — Hardcoded FTP Credentials in CustomUpload.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java`
**Line:** 219
**Severity:** CRITICAL
**Category:** Hardcoded Credentials / Secrets in Source

**Description:**
A complete FTP connection string including server hostname, port, username, and password is embedded as a string literal and then inserted into the `outgoing_stat` database table. The password `Sdh79HfkLq6` matches `RuntimeConf.firmwarepass`, confirming the same credential appears in at least two separate source files. Additionally, the connection string is stored in the database in plaintext, further broadening its exposure.

**Evidence:**
```java
// Line 219
String message = "FTPF=fms.fleetiq360.com,211,firmware,Sdh79HfkLq6,"
    + "/firmware/FW_LMII_2_10_59_GEN2_DISPLAY_AUTO_CAM/FleetMS.bin";
```

**Recommendation:**
Remove the hardcoded credential. Read the FTP password from an environment variable or secrets store at runtime. Do not store raw credentials in the database. Rotate the `firmware` / `Sdh79HfkLq6` FTP credential.

---

### A04-03 — SQL Injection in UtilBean.java (Multiple Methods)

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java`
**Lines:** 86, 196, 251, 305
**Severity:** CRITICAL
**Category:** SQL Injection

**Description:**
Four public methods in `UtilBean` build SQL queries by string-concatenating `String` parameters received from callers. None use `PreparedStatement`. Because `UtilBean` is a utility class invoked throughout the application, the `userCd`, `webUserCD`, and `custCd` values ultimately derive from session state or HTTP request parameters, giving an authenticated attacker full control over these queries.

**Evidence:**
```java
// Line 86 — getLocalTime(String currentTime, String webUserCD)
String sql = "select \"LOC_CD\" from \"FMS_USER_DEPT_REL\" where \"USER_CD\" = " + webUserCD;
rst = stmt.executeQuery(sql);

// Line 196 — getCustomerSettingByUser(String userCd)
String sql = " select cust.\"USER_CD\", cust.pword_restriction, cust.cust_timezone, "
    + "cust.cust_locale, cust.date_format, usr.dashboard_type "
    + " from \"FMS_CUST_MST\" cust, \"FMS_USR_MST\" usr "
    + " where usr.\"USER_CD\"=" + userCd;
rst = stmt.executeQuery(sql);

// Line 251 — getCustomerSetting(String custCd)
String sql = " select \"USER_CD\", pword_restriction FROM \"FMS_CUST_MST\" "
    + " where \"USER_CD\"=" + custCd;

// Line 305 — getCustLocDeptBeanByUser(String userCD)
String sql = "select rel.\"CUST_CD\", rel.\"LOC_CD\", rel.\"DEPT_CD\" "
    + " from \"FMS_USER_DEPT_REL\" rel "
    + " where rel.\"USER_CD\"=" + userCD;
```

**Recommendation:**
Replace all four queries with `PreparedStatement` using `?` placeholders and `setString()`/`setInt()` parameter binding. Example:
```java
String sql = "select \"LOC_CD\" from \"FMS_USER_DEPT_REL\" where \"USER_CD\" = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, webUserCD);
ResultSet rst = ps.executeQuery();
```

---

### A04-04 — SQL Injection in GdprDataDelete.java (DELETE Statements)

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java`
**Lines:** 67, 73–94
**Severity:** CRITICAL
**Category:** SQL Injection / Second-Order SQL Injection

**Description:**
`call_gdpr_delete_data()` issues multiple destructive `DELETE` statements whose WHERE clauses are built by concatenating `cust_cd`, `driver_cd.get(i)`, and `gdpr_data` directly into the query string. `gdpr_data` is read from the `FMS_CUST_MST` table and then injected into an `interval` expression, constituting a second-order injection: a malicious value stored in the database executes arbitrary SQL when this method runs. Because these are `DELETE` statements, exploitation can result in complete data loss.

**Evidence:**
```java
// Line 67
query = "select ur.\"USER_CD\" from \"FMS_USER_DEPT_REL\" as ur ..."
      + " where ur.\"CUST_CD\"='" + cust_cd + "' and ur.\"USER_CD\" != 2 ...";

// Lines 73-80 — loop body, i iterates over driver_cd list
query = "delete from \"fms_io_data_dtl\" where ... and \"driver_cd\"='" + driver_cd.get(i) + "')";
query = "delete from \"fms_io_data\" where ... and \"driver_cd\"= '" + driver_cd.get(i) + "'";

// gdpr_data used as PostgreSQL interval value (second-order injection)
query = "delete from \"fms_io_data\" where timestamp < NOW() - interval '" + gdpr_data + " years' ...";
```

**Recommendation:**
Use `PreparedStatement` for all queries. For the `interval` expression, cast `gdpr_data` to an integer before use and validate it is within an expected range (e.g., 1–10 years) before constructing the SQL, since PostgreSQL does not support `?` placeholders in `interval` literals directly — use `interval '1 year' * ?` or the `make_interval` function with a parameterised integer.

---

### A04-05 — SQL Injection in password_life.java (IP Address Injection)

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/password_life.java`
**Lines:** 76, 104, 108
**Severity:** CRITICAL
**Category:** SQL Injection

**Description:**
`loadDefaultValues()` concatenates the client IP address (`ip`), `logindate`, and `logintime` into an `UPDATE` statement. The IP address is typically obtained from `HttpServletRequest.getRemoteAddr()`, but in environments behind load balancers or proxies, it may be sourced from the `X-Forwarded-For` header, which an attacker can freely set. This provides a reliable SQL injection vector that fires on every login event. The `userid` parameter is also concatenated in the SELECT and UPDATE queries.

**Evidence:**
```java
// Line 76
queryString = "select nvl(emplpass_reset_flag,' ') from empl_passwords "
    + "where emplpass_empid='" + userid + "'";

// Line 108 — UPDATE with IP, date, time all concatenated
queryString = "update empl_passwords set emplpass_login_status='"
    + ip + "'||' on '||to_char(to_date('"
    + logindate + "','dd/mm/yy'),'Dy , Monthdd , yyyy ')||'"
    + logintime + "' where emplpass_empid='" + userid + "'";
```

**Recommendation:**
Use `PreparedStatement` for all queries. Validate that `ip` conforms to IPv4/IPv6 format before use. Never trust `X-Forwarded-For` without explicit proxy trust configuration.

---

### A04-06 — SQL Injection in SupervisorMasterHelper.java (INSERT into outgoing_stat)

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java`
**Lines:** 39–40, 49–50, 54–55, 65–66, 107
**Severity:** CRITICAL
**Category:** SQL Injection

**Description:**
All three public methods (`deleteSupervisorByUser`, `deleteSupervisor`, `deleteSuperMaster`) construct SQL by string-concatenating method parameters: `user`, `loc_cd`, `cust_cd`, `dept_cd`, `slot`, and `access_user`. The `access_user` parameter represents the session user and is inserted into the `outgoing_stat` messaging table. Because this affects both query logic (SELECT/UPDATE/DELETE) and data insertion (INSERT), exploitation can both extract data and inject malicious records into the message queue.

**Evidence:**
```java
// Lines 39-40
queryString = "select \"SLOT_NO\" from \"FMS_LOC_OVERRIDE\" "
    + "where \"USER_CD\"='" + user + "' and \"LOC_CD\"='" + loc_cd + "'";

// Lines 49-50
queryString = "Update \"FMS_USR_MST\" set \"supervisor_access\" = '0&0&0' "
    + "where \"USER_CD\" ='" + user + "'";

// Line 107 — INSERT with access_user from session
queryString = "insert into \"outgoing_stat\" (sno, gmtp_id, message, tm, sent, user_cd) "
    + "values('" + sno + "','" + gmtpid + "','" + msg + "','" + tm + "','f','" + access_user + "')";
```

**Recommendation:**
Replace all Statement usage with `PreparedStatement`. The `access_user` value must be validated against the authenticated session identity and not accepted as a raw string parameter.

---

### A04-07 — SQL Injection in MigrateMaster.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java`
**Lines:** 42, 53, 60, 71, 86, 95, 100
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`callMigrateMaster()` iterates over lists of customer codes, location codes, department codes, and user codes, concatenating each into SELECT, DELETE, INSERT, and UPDATE statements. The `cust_cd` parameter and list contents (`locations.get(i)`, `users.get(j)`, `departments.get(w)`) are all string-typed with no sanitisation.

**Evidence:**
```java
// Line 42
sql = "SELECT \"master_code_level\" from \"FMS_CUST_MST\" where \"USER_CD\"='" + cust_cd + "'";

// Line 53
sql = "delete from \"FMS_LOC_OVERRIDE\" where \"LOC_CD\"='" + locations.get(i) + "'";

// Line 60
sql = "insert into \"FMS_LOC_OVERRIDE\" (\"LOC_CD\",\"SLOT_NO\",\"USER_CD\") "
    + "values ('" + locations.get(i) + "','" + tmp_slots.get(j) + "','" + tmp_user_cd.get(j) + "')";

// Line 95
sql = "Update \"FMS_USR_MST\" set \"supervisor_access\" = '1&2&4' "
    + "where \"USER_CD\" ='" + tmp_user_cd.get(j) + "'";
```

**Recommendation:**
Use `PreparedStatement` for all queries. Validate that customer, location, department, and user codes match expected numeric or alphanumeric patterns before use.

---

### A04-08 — SQL Injection in fix_department.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java`
**Lines:** 121, 131, 142, 148, 156, 159, 165, 168, 177
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`fix_dept(String user_cd, String loc_cd, String dept_cd)` concatenates all three `String` parameters directly into more than ten queries affecting `FMS_CUST_DEPT_REL`, `FMS_DEPT_MST`, `FMS_USER_DEPT_REL`, and related tables. The method modifies and reassigns department codes, meaning injection can silently corrupt relational data across the fleet management schema.

**Evidence:**
```java
// Line 121
query = "select count(\"DEPT_CD\") from \"FMS_CUST_DEPT_REL\" "
    + "where \"DEPT_CD\"=" + dept_cd;

// Line 142
query = "update \"FMS_CUST_DEPT_REL\" set \"DEPT_CD\" = " + newDeptCd
    + " where \"USER_CD\"=" + user_cd
    + " AND \"LOC_CD\"=" + loc_cd
    + " AND \"DEPT_CD\"=" + dept_cd;

// Line 165
query = "update \"FMS_USER_DEPT_REL\" set \"DEPT_CD\"=" + newDeptCd
    + " where \"DEPT_CD\"=" + dept_cd
    + " and \"LOC_CD\"=" + loc_cd
    + " and \"USER_CD\"=" + user_cd;
```

**Recommendation:**
Use `PreparedStatement` throughout. Validate that `user_cd`, `loc_cd`, and `dept_cd` are numeric before use in any query.

---

### A04-09 — SQL Injection in InfoLogger.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java`
**Lines:** 59, 64–65
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`writelog(String msg)` parses the `msg` parameter by splitting on `#` to extract `tsDate`, `time`, `uid`, `mid`, `rem`, and `tuid`. All extracted values are concatenated into a SELECT and then an INSERT to `SEC_LOG_DETAILS`. Because `msg` is a single string parameter whose format is caller-controlled, any component of it can carry SQL injection payload. This is the application's security audit log, so corrupting it is particularly impactful.

**Evidence:**
```java
// Line 59
queryString = "SELECT EMP_CD FROM HR_EMP_MST WHERE EMP_NM='" + tuid + "'";

// Lines 64-65
queryString = "insert into SEC_LOG_DETAILS(LOG_DT, LOG_TIME, LOG_UID, LOG_MACH_ID, REMARKS, EMP_CD) "
    + "values(to_date('" + tsDate + "','yyyy-mm-dd'),'"
    + time + "','" + uid + "','" + mid + "','" + rem + "','" + emp_cd + "')";
```

**Recommendation:**
Use `PreparedStatement`. Validate each component of `msg` after splitting: `tsDate` must match a date pattern, `uid` must be numeric, `mid` must be alphanumeric, etc. Consider restructuring `writelog` to accept typed parameters rather than a single delimited string.

---

### A04-10 — SQL Injection in mail.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/mail.java`
**Line:** 63
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`Ename(String userid)` queries `FMS_USR_MST` with `userid` concatenated directly. This method is called to resolve a user's email address before sending notifications — any code path that passes user-controlled input as `userid` is exploitable.

**Evidence:**
```java
// Line 63
query = "select \"EMAIL_ADDR\",\"CONTACT_FIRST_NAME\",\"CONTACT_LAST_NAME\" "
    + "from \"FMS_USR_MST\" where \"USER_CD\"='" + userid + "'";
rs = stmt.executeQuery(query);
```

**Recommendation:**
Replace with `PreparedStatement`. Validate that `userid` is numeric before use.

---

### A04-11 — SQL Injection in Menu_Bean.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java`
**Lines:** 73, 77
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`fetchform_rights()` and `fetchSubModule()` build SELECT queries by concatenating `set_user_cd` and `module` string fields. These fields are set via the `setUser_cd()` and `setModule()` setters, which accept arbitrary string input from callers.

**Evidence:**
```java
// Line 73
sql = "select \"FORM_CD\",\"MODULE_CD\",\"FORM_NM\",\"FORM_URL\" "
    + "from \"FMS_FORM_MST\" where \"MODULE_CD\"='" + module + "' order by \"FORM_NM\"";

// Line 77
sql = "select \"FORM_CD\",\"FORM_URL\" from \"FMS_FORM_RIGHTS\" "
    + "where \"USER_CD\"=" + set_user_cd + " and \"FORM_CD\" in (...)";
```

**Recommendation:**
Use `PreparedStatement` for both queries. Validate `set_user_cd` as numeric and `module` against a whitelist of known module codes.

---

### A04-12 — SQL Injection in Menu_Bean1.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean1.java`
**Lines:** 69, 73
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
Same structural vulnerability as A04-11 in the `Menu_Bean1` variant. `fetchform_rights()` concatenates `set_user_cd` and `module` into SQL queries.

**Evidence:**
```java
// Line 69
sql = "select \"FORM_CD\",\"MODULE_CD\",\"FORM_NM\",\"FORM_URL\" "
    + "from \"FMS_FORM_MST\" where \"MODULE_CD\"='" + module + "'";

// Line 73
sql = "select \"FORM_CD\",\"FORM_URL\" from \"FMS_FORM_RIGHTS\" "
    + "where \"USER_CD\"=" + set_user_cd + " ...";
```

**Recommendation:**
Same as A04-11: use `PreparedStatement` and validate inputs.

---

### A04-13 — SQL Injection in call_mail.java (Multiple Methods)

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java`
**Lines:** Throughout (confirmed via static analysis grep)
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`call_mail.java` contains multiple `executeQuery()` and `executeUpdate()` calls using bare `Statement` objects. Variables including `rec_no`, `veh_cd`, `gmtp_id`, `id`, and `freq` are concatenated into query strings. The file is a background alert/notification dispatcher invoked by a scheduler, so injected payloads would execute in a privileged, non-interactive server context without per-request authentication checks.

**Evidence (grep output confirms):**
```
stmt.executeUpdate(query)   — multiple occurrences
stmt.executeQuery(query)    — multiple occurrences
query = "... where ... = '" + veh_cd + "'"
query = "... where gmtp_id = '" + gmtp_id + "'"
query = "... where rec_no = " + rec_no
```

**Recommendation:**
Audit each query in `call_mail.java` individually and replace all with `PreparedStatement`. Since this runs as a background job, ensure the database user account used has only the minimum required privileges (SELECT/UPDATE on specific tables, no DDL).

---

### A04-14 — SQL Injection in CftsAlert.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java`
**Lines:** 45, 79, 85, 115, 124, 147, 207, 248
**Severity:** HIGH
**Category:** SQL Injection / Second-Order SQL Injection

**Description:**
`checkDueDate()` and `getAlertlist()` concatenate `cust`, `site`, and vehicle/inspection values read from the database into subsequent SQL statements. The email INSERT (lines 147, 207) concatenates `email`, `subsject`, and `message` content directly into the `email_outgoing` table. Values sourced from the database that are then re-used in SQL without parameterisation constitute second-order injection.

**Evidence:**
```java
// Line 45
sql = "select b.\"VEHICLE_CD\", b.\"VEHICLE_ID\", b.\"NEXT_INSPECTION_DT\", "
    + "b.\"LOC_CD\", a.\"EMAIL_ADDR\" "
    + "from \"FMS_VEHICLE_MST\" b, \"FMS_USR_MST\" a "
    + "where b.\"USER_CD\"=" + cust + " and b.\"LOC_CD\"=" + site;

// Line 85
sql = "update fms_inspection_config set alert_status=2 "
    + "where vehicle_cd=" + rs.getString(2);

// Line 147
sql = "insert into email_outgoing (timestamp, to_email, subject, message) "
    + "VALUES (NOW(), '" + email + "','" + subsject + "','" + message + "')";
```

**Recommendation:**
Use `PreparedStatement` for all queries. For the email INSERT, use parameterised binding for `email`, `subsject`, and `message` to prevent stored second-order injection from email content.

---

### A04-15 — SQL Injection in DriverExpiryAlert.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java`
**Lines:** 43–50, 81–85, 144
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`checkExpiry()` builds a dynamic `extra` filter string by concatenating `cust_cd`, `loc_cd`, and `dept_cd` values read from `FMS_CUST_MST` / `FMS_LOC_MST`. This `extra` string is appended directly to the main query. The email INSERT (line 144) also concatenates `email`, `subsject`, and `message` without parameterisation.

**Evidence:**
```java
// Lines 43-50
String extra = "";
if (!cust_cd.equals("")) extra += " and \"CUST_CD\" = '" + cust_cd + "'";
if (!loc_cd.equals(""))  extra += " and \"LOC_CD\" = '"  + loc_cd  + "'";
if (!dept_cd.equals("")) extra += " and \"DEPT_CD\" = '" + dept_cd + "'";
sql = "select ... from driver_masters where ... " + extra + " order by ...";

// Line 144
sql = "insert into email_outgoing (timestamp, to_email, subject, message) "
    + "VALUES (NOW(), '" + email + "','" + subsject + "','" + message + "')";
```

**Recommendation:**
Replace the dynamic `extra` filter with parameterised conditions. Use `PreparedStatement` with conditional `setString()` calls for optional filter values. Parameterise the email INSERT.

---

### A04-16 — SQL Injection in DriverMedicalAlert.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java`
**Lines:** 64–70, 125, 143, 161
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
Same `extra` filter pattern as A04-15 applied to `cust_cd`, `loc_cd`, `dept_cd`. Email INSERTs at lines 125, 143, and 161 also concatenate `email`, `subsject`, and `message` values.

**Evidence:**
```java
// Lines 64-70
String extra = "";
if (!cust_cd.equals("")) extra += " and \"CUST_CD\" = '" + cust_cd + "'";
// ... same pattern
sql = "select ... from driver_masters where ... " + extra;

// Line 125
sql = "insert into email_outgoing ... VALUES (NOW(), '"
    + email + "','" + subsject + "','" + message + "')";
```

**Recommendation:**
Same as A04-15.

---

### A04-17 — SQL Injection in send_updatepreop.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java`
**Lines:** 206–212
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`resyncPreop(List<String> vehTCds)` splits each element of `vehTCds` by `|` to extract `vehType`, `customer`, `location`, `department`. These four values are then concatenated into query strings. The `vehTCds` list originates from a caller-supplied parameter, and its elements are not validated before being embedded in SQL.

**Evidence:**
```java
// Lines 206-212
String[] parts = vehTCds.get(i).split("\\|");
String vehType   = parts[0];
String customer  = parts[1];
String location  = parts[2];
String department = parts[3];
query = "select ... from \"FMS_VEHICLE_MST\" "
    + "where \"USER_CD\"='" + customer + "' and \"LOC_CD\"='" + location
    + "' and \"DEPT_CD\"='" + department + "' and \"VEH_TYPE\"='" + vehType + "'";
```

**Recommendation:**
Use `PreparedStatement`. Validate that `customer`, `location`, `department` are numeric and `vehType` matches an expected pattern before use.

---

### A04-18 — SQL Injection in FleetCheckFTP.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java`
**Lines:** 84, 100, 229
**Severity:** HIGH
**Category:** SQL Injection

**Description:**
`checkFirmware()` (or equivalent entry point) concatenates database-sourced values `gmtp_id`, `vt_cd`, `cust_cd`, `site_cd`, `dept_cd` into SELECT queries and then into an INSERT that records an FTP upload command. The FTP command string at line 229 also embeds `RuntimeConf.firmwarepass` (`Sdh79HfkLq6`) — see A04-01 and A04-02.

**Evidence:**
```java
// Line 84
sql = "select ... from \"FMS_VEHICLE_MST\" v "
    + "where v.\"VEHICLE_ID\" = '" + gmtp_id + "'";

// Line 100
sql = "select ... where \"USER_CD\"='" + cust_cd + "' and \"LOC_CD\" = '"
    + site_cd + "' and \"DEPT_CD\" = '" + dept_cd + "'";

// Line 229 — FTP command with hardcoded password stored to DB
sql = "insert into \"outgoing\" ... values ('" + ftp_upld_cmd + "')";
// ftp_upld_cmd contains RuntimeConf.firmwarepass
```

**Recommendation:**
Use `PreparedStatement` for all queries. Remove the hardcoded firmware password from the FTP command string (see A04-01).

---

### A04-19 — SSRF in GetHtml.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java`
**Lines:** 24, 83
**Severity:** HIGH
**Category:** Server-Side Request Forgery (SSRF)

**Description:**
`getHTML(String urlToRead, String param)` concatenates `urlToRead` and `param` to form a URL and opens an HTTP connection to it. `getHTML1(String urlToRead)` does the same with a single parameter. If callers pass user-controlled values — e.g., from HTTP request parameters — an attacker can direct the server to make requests to internal network addresses (`http://169.254.169.254/`, `http://localhost:8080/manager/`, other microservices) or exfiltrate data to external hosts.

**Evidence:**
```java
// Line 24 — getHTML(String urlToRead, String param)
URL url = new URL(urlToRead + param);
HttpURLConnection con = (HttpURLConnection) url.openConnection();

// Line 83 — getHTML1(String urlToRead)
URL url = new URL(urlToRead);
HttpURLConnection con = (HttpURLConnection) url.openConnection();
```

**Recommendation:**
Validate `urlToRead` against an allowlist of permitted hosts and schemes before constructing the URL. Reject `file://`, `ftp://`, and any host not in the approved list. If this method is only ever called with internally-constructed URLs (not user-supplied), document this assumption and add assertions to enforce it.

---

### A04-20 — SSRF and File Path Traversal in DataUtil.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java`
**Lines:** 329–343, 919, 937
**Severity:** HIGH
**Category:** SSRF / File Path Traversal

**Description:**
`saveImage(String imageUrl, ...)` (line 329) opens `new URL(imageUrl)` directly — SSRF if `imageUrl` is caller-supplied. `uploadLicenceFile()` (line 919) constructs a file path from a `filename` parameter appended to a fixed base path without canonicalisation. `uploadDocumentFile()` (line 937) uses `cust_loc` in the path: `"/home/gmtp/fms_files/CFTS/" + cust_loc + "/"` — if `cust_loc` contains `../`, the file is written outside the intended directory.

**Evidence:**
```java
// Lines 329-343
URL url = new URL(imageUrl);
HttpURLConnection connection = (HttpURLConnection) url.openConnection();
// ... writes to destinationFile

// Line 919
File f = new File(base + filename);
FileOutputStream fos = new FileOutputStream(f);

// Line 937
String base = "/home/gmtp/fms_files/CFTS/" + cust_loc + "/";
```

**Recommendation:**
For SSRF: validate `imageUrl` against an allowlist. For file path traversal: after constructing the `File` object, call `getCanonicalPath()` and assert the result starts with the expected base directory before writing. Reject any `filename` or `cust_loc` containing `..` or path separators.

---

### A04-21 — File Path Traversal in ImportFiles.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java`
**Line:** 85
**Severity:** HIGH
**Category:** File Path Traversal

**Description:**
`doPost()` extracts `fileName` from the `Content-Disposition` header of a multipart upload request. The extracted name is stripped of surrounding quotes but is not validated for path traversal sequences. The file is written to `appPath + RuntimeConf.UPLOAD_FOLDER + File.separator + fileName`. An attacker can submit a filename such as `../../WEB-INF/web.xml` or `../../etc/cron.d/pwn` to overwrite arbitrary server-side files.

**Evidence:**
```java
// Line 77-85
String fileName = header.substring(header.indexOf("filename=\"") + 10, header.lastIndexOf("\""));
// No path sanitisation
File uploadFile = new File(path + File.separator + fileName);
out = new FileOutputStream(uploadFile);
```

**Recommendation:**
After extracting `fileName`, strip any directory component using `new File(fileName).getName()` (returns only the leaf name, discarding any path prefix). Then construct the output path and verify with `getCanonicalPath()` that the resolved path is within the upload directory. Reject filenames containing `/`, `\`, or `..`.

---

### A04-22 — File Path Traversal in CustomUpload.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java`
**Line:** 77
**Severity:** HIGH
**Category:** File Path Traversal

**Description:**
Same vulnerability as A04-21. `CustomUpload.doPost()` extracts `fileName` from the multipart `Content-Disposition` header and writes to `path + File.separator + fileName` without sanitisation.

**Evidence:**
```java
// Line 77
String fileName = header.substring(header.indexOf("filename=\"") + 10, header.lastIndexOf("\""));
File uploadFile = new File(path + File.separator + fileName);
out = new FileOutputStream(uploadFile);
```

**Recommendation:**
Same as A04-21: use `new File(fileName).getName()` and validate the canonical output path.

---

### A04-23 — Weak Cryptography in EncryptTest.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java`
**Severity:** HIGH
**Category:** Weak Cryptography / Broken Encryption

**Description:**
`EncryptTest` implements a trivial character-substitution cipher — each character is mapped to a different character from a static lookup string. This provides no meaningful confidentiality: the transformation is deterministic, there is no key, no salt, and no computational cost. Any attacker with access to two known plaintext/ciphertext pairs (e.g., any known password) can derive the full substitution table and decrypt all stored values. `password_life.java` calls this class to "encrypt" passwords before storage.

**Evidence (representative logic):**
```java
// Character substitution — maps each char to a fixed offset in a lookup table
// No key, no salt, trivially reversible
public static String encrypt(String plainText) {
    // ... character substitution loop
}
```

**Recommendation:**
Replace with a proper password hashing algorithm: `bcrypt`, `Argon2`, or `PBKDF2` with a minimum of 100,000 iterations and a cryptographically random per-user salt. Do not use reversible "encryption" for passwords — passwords should be stored as one-way hashes. Consider a forced password reset for all existing users after migrating to a secure hash algorithm, since the substitution cipher output can be decoded to recover plaintext credentials.

---

### A04-24 — SQL Injection (Second-Order) in PasswordExpiryAlert.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java`
**Lines:** 69–70
**Severity:** MEDIUM
**Category:** SQL Injection (Second-Order)

**Description:**
The email INSERT at lines 69–70 concatenates `email`, `subsject`, and `message` strings read from `FMS_USR_MST` into the `email_outgoing` INSERT. If any of these values in the database contain SQL metacharacters (e.g., a stored email address with a single quote), the INSERT will fail or be exploitable. The UPDATE at line 72 uses `userBean.getId()` which returns `int` — that portion is safe.

**Evidence:**
```java
// Lines 69-70
sql = "insert into email_outgoing (timestamp, to_email, subject, message) "
    + "VALUES (NOW(), '" + email + "','" + subsject + "','" + message + "')";
stmt.executeUpdate(sql);

// Line 72 — safe (int)
sql = "update \"FMS_USR_MST\" set pword_alert_sent='t' where \"USER_CD\"=" + userBean.getId();
```

**Recommendation:**
Use `PreparedStatement` for the INSERT. The UPDATE at line 72 is safe as-is but should also be migrated to `PreparedStatement` for consistency.

---

### A04-25 — Dynamic ORDER BY in LogicBean_filter1.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java`
**Line:** 225
**Severity:** LOW
**Category:** SQL Injection (ORDER BY — Mitigated)

**Description:**
The ORDER BY clause is built by concatenating `sort_str` and `sort_ord`. `sort_str` is set via a `switch` statement on a parsed integer (safe — column name is controlled by the switch), and `sort_ord` is set to either `" asc"` or `" desc"` (safe — controlled by a binary check). The current implementation is not directly exploitable, but the pattern is fragile: any future modification that passes `sort_str` from a non-switch source would immediately create a vulnerability. The code also does not use `PreparedStatement`.

**Evidence:**
```java
// Line 225
sql = sql + " order by " + sort_str + sort_ord;
```

**Recommendation:**
Document the intent clearly. If additional sort columns are added in future, ensure they are always resolved through the switch statement. Consider converting to an enum-based approach. Migrate the surrounding query to `PreparedStatement` even if ORDER BY must remain dynamic.

---

### A04-26 — Wildcard SQL and Naming Imports Across Package

**Files:** Multiple (UtilBean.java, mail.java, InfoLogger.java, GdprDataDelete.java, GetHtml.java, and others)
**Severity:** LOW
**Category:** Code Quality / Import Hygiene

**Description:**
Multiple files use wildcard imports (`java.sql.*`, `javax.sql.*`, `javax.naming.*`, `java.net.*`, `java.io.*`). While not a direct vulnerability, wildcard imports increase the risk of accidental class name collisions (e.g., a class named `Statement` from a malicious dependency shadowing `java.sql.Statement`), obscure which SQL classes are in use during code review, and prevent static analysis tools from easily identifying whether `PreparedStatement` or `Statement` is being used.

**Evidence:**
```java
// UtilBean.java
import java.sql.*;
import javax.sql.*;
import javax.naming.*;

// mail.java, InfoLogger.java, GdprDataDelete.java
import java.sql.*;
import javax.naming.*;
```

**Recommendation:**
Replace wildcard imports with explicit imports. This also serves as a forcing function to identify all SQL class usage during the remediation of A04-03 through A04-18.

---

## Summary

The `util` package exhibits systemic SQL injection vulnerabilities. Of the 37 files reviewed, **at least 18 contain SQL queries built by string concatenation** with no use of `PreparedStatement`. The root cause is a package-wide coding pattern that predates parameterised queries being standard practice. The following priorities are recommended:

**Immediate (before next production release):**
1. Rotate all credentials exposed in `RuntimeConf.java` and `CustomUpload.java` (A04-01, A04-02) — these are in version control and must be treated as fully compromised.
2. Remediate SQL injection in `GdprDataDelete.java` (A04-04) — this has `DELETE` statements and second-order injection, making it the highest-consequence injection point.
3. Remediate SQL injection in `password_life.java` (A04-05) — IP address injection fires on every login.
4. Remediate file upload path traversal in `ImportFiles.java` and `CustomUpload.java` (A04-21, A04-22) — arbitrary file write on the server.
5. Replace the character-substitution cipher in `EncryptTest.java` with bcrypt or Argon2 (A04-23).

**Short-term (within current sprint):**
6. Remediate SQL injection across all remaining files (A04-03, A04-06 through A04-18, A04-24).
7. Validate and restrict SSRF vectors in `GetHtml.java` and `DataUtil.java` (A04-19, A04-20).

**Ongoing:**
8. Enforce a code review rule that `java.sql.Statement` may not be used for queries with variable inputs — only `PreparedStatement`.
9. Note: `escapeSingleQuotes.java` exists in the package but is not used by any of the SQL-executing classes reviewed. Its presence suggests an earlier partial attempt at SQL escaping that was never adopted. This approach (escaping) is inferior to parameterised queries and should not be used as a remediation strategy.
