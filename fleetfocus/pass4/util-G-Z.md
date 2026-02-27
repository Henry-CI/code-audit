# Pass 4 -- Code Quality Audit: util G-Z (24 files)

**Auditor:** A20
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/util/` -- files G through Z

---

## 1. Naming Conventions

### 1.1 Non-Standard Class Names (lowercase / snake_case)

Java convention requires PascalCase class names. The following violate this:

| File | Class Name | Recommended Name |
|------|-----------|-----------------|
| `call_mail.java` | `call_mail` | `CallMail` |
| `escapeSingleQuotes.java` | `escapeSingleQuotes` | `EscapeSingleQuotes` |
| `fix_department.java` | `fix_department` | `FixDepartment` |
| `mail.java` | `mail` | `Mail` |
| `password_life.java` | `password_life` | `PasswordLife` |
| `password_policy.java` | `password_policy` | `PasswordPolicy` |
| `send_timezone.java` | `send_timezone` | `SendTimezone` |
| `send_updatepreop.java` | `send_updatepreop` | `SendUpdatePreop` |

**Evidence:** 8 of 24 files (33%) use non-standard lowercase/snake_case class names.
**Severity:** Medium -- breaks Java conventions; affects readability and tooling.

### 1.2 Non-Standard Method Names

Several classes use non-PascalCase or snake_case method names inconsistently:

| File | Method | Convention Issue |
|------|--------|----------------|
| `LogicBean_filter.java` | `Fetch_users()`, `Fetch_Data()` | PascalCase methods (should be camelCase) |
| `LogicBean_filter1.java` | `Fetch_users()`, `Fetch_Data()` | Same as above |
| `GdprDataDelete.java` | `call_gdpr_delete_data()` | snake_case method |
| `send_timezone.java` | `call_send_timezone()`, `call_send_timezone_au()` | snake_case method |
| `send_updatepreop.java` | `updatepreop()`, `resyncPreop()` | Inconsistent casing |
| `fix_department.java` | `show_cust_dept()`, `fix_dept()` | snake_case methods |
| `call_mail.java` | `call_email_au()`, `Ename()` | Mixed snake_case and PascalCase |
| `mail.java` | `Ename()` | PascalCase (should be camelCase) |
| `InfoLogger.java` | `writelog()` | Missing camelCase (`writeLog`) |

**Severity:** Low -- internal consistency issue.

### 1.3 Underscore-Separated Class Name Pairs

| File | Class Name |
|------|-----------|
| `LogicBean_filter.java` | `LogicBean_filter` |
| `LogicBean_filter1.java` | `LogicBean_filter1` |
| `Menu_Bean.java` | `Menu_Bean` |
| `Menu_Bean1.java` | `Menu_Bean1` |

**Evidence:** The underscore convention combined with numeric suffixes suggests copy-paste versioning rather than proper inheritance or parameterization.
**Severity:** Medium.

---

## 2. God Classes / Oversized Files

### 2.1 ImportFiles.java -- 2,692 lines

- **Evidence:** `wc -l` returns 2,692 lines. Single `doPost()` method contains all import logic for drivers (generic, UK, AU), questions, and question-tab imports within massive `if/else` blocks.
- **Impact:** Extremely difficult to test, maintain, or extend. A single method handles at least 5 distinct import workflows.
- **Severity:** Critical.

### 2.2 call_mail.java -- 1,454 lines

- **Evidence:** `wc -l` returns 1,454 lines. Contains email-sending logic for both AU and general configurations with deeply nested DB queries and HTML generation.
- **Severity:** High.

### 2.3 send_updatepreop.java -- 601 lines / send_timezone.java -- 417 lines

- Both contain long, deeply nested methods with duplicated JNDI lookup, query execution, and resource cleanup patterns.
- **Severity:** Medium.

---

## 3. Duplicate / Near-Duplicate Implementations

### 3.1 Menu_Bean.java vs Menu_Bean1.java

Both files share nearly identical structure:
- Same fields: `conn`, `stmt`, `rset`, `query`, `query1`, `empl_GrpId`, `op_cd`, `moduleNmMotherPg`, `set_user_cd`, `form_str`, `emp_nm`, `option`, `module`, ArrayLists (`FormId`, `appl_path`, `FormName`, `FormType`, `ModuleName`, `ModuleCode`).
- Same methods: `fetchform_rights()`, `fetchMenuAttr1()`, `fetchSubModule()`, `clearVectors()`, `init()`.
- Differences: `Menu_Bean1` adds `form_desc` ArrayList and returns an extra PRIORITY/DESCRIPTION column in `fetchSubModule()`. `Menu_Bean` has `icon_path` and `ModuleDesc` that `Menu_Bean1` lacks.

**Evidence:** Line-by-line comparison shows ~85% code duplication.
**Severity:** High -- maintenance changes must be applied to both files.

### 3.2 LogicBean_filter.java vs LogicBean_filter1.java

Both files share nearly identical structure:
- Same 24 ArrayLists (Viodriver_id, Vdriver_id, Vgmtp_id, Vio0_data0..Vio9_data2, Vutc_time, Vdate, Vtime).
- Same `clear_variables()`, `Fetch_users()` methods.
- Same `init()` pattern.
- Difference: `LogicBean_filter1` adds sorting (`sort_by`, `sort_asc`), time-conversion helper `convert_time()`, and aggregate totals (`io0_data1`..`io9_data2`, `iio0_data1`..`iio9_data2`).

**Evidence:** `LogicBean_filter` is 475 lines, `LogicBean_filter1` is 782 lines. The first ~180 lines (fields + clear_variables + Fetch_users) are copy-pasted verbatim.
**Severity:** High.

### 3.3 password_life.java vs password_policy.java

Both are decompiled classes with identical structure:
- Same fields: `conn`, `stmt`, `rset`, `queryString`..`queryString3`, `method_name`, `userid`, `logintime`, `logindate`, `ip`, `login_status`, `emp_pass`.
- Same `clear_variables()`, `setUser()`, `setIp()`, `setLogindate()`, `setLogintime()`, `init()` methods.
- Both have `loadDefaultValues()` that differ only in the SQL query executed.

**Evidence:** `password_life.java` header comment: `// Decompiled by DJ v3.9.9.91 Copyright 2005 Atanas Neshkov`. Both files carry decompiled artifacts from 2006.
**Severity:** Medium -- legacy decompiled code with shared base that was never refactored.

### 3.4 call_mail.java `Ename()` vs mail.java `Ename()`

`call_mail.Ename()` (line 60-66) simply returns `LindeConfig.mail_from + "#" + LindeConfig.systemName` without any DB query. `mail.Ename()` (line 41-107) performs a full DB query to look up email/name, then ignores the result and returns the same `LindeConfig.mail_from + "#" + LindeConfig.systemName`. The DB query in `mail.Ename()` is dead code.

**Evidence:** `mail.java` lines 69-79: queries the DB for EMAIL_ADDR/CONTACT_FIRST_NAME/CONTACT_LAST_NAME, then overwrites `sEmail` and `sName` with `LindeConfig` values at lines 78-79.
**Severity:** Medium -- wasted DB call, dead code.

---

## 4. Dead Code

### 4.1 PurgeData.java -- Completely Empty Class

```java
package com.torrent.surat.fms6.util;
public class PurgeData {
}
```

**Evidence:** File is 5 lines total. No methods, no fields, no functionality.
**Severity:** Low -- dead code that should be removed.

### 4.2 GetHtml.java -- Commented-Out Method (lines 41-72)

A large block of commented-out code for `getHTML1()` using Apache HttpClient (lines 41-72), preceded by commented-out imports (lines 7-11).

**Evidence:**
```java
/*
   public String getHTML1(String urlToRead){
       HttpClient httpclient = new DefaultHttpClient();
       ...
   }
*/
```
**Severity:** Low.

### 4.3 ImportFiles.java -- Extensive Commented-Out Code

Dozens of `//System.out.println(...)` debug statements throughout (lines 84, 91, 131, 151, etc.). Also commented-out blocks at lines 120-123, 165-168.
**Severity:** Low.

### 4.4 LogicBean_filter1.java -- Commented-Out conn.close() (line 392)

```java
//conn.close();
```
**Evidence:** Connection close was commented out, but a finally block was added later. The commented-out line is dead code.
**Severity:** Low.

### 4.5 Menu_Bean.java & Menu_Bean1.java -- Commented-Out Legacy Queries

Both files contain large commented-out SQL queries in `fetchSubModule()` (lines 165-172 in Menu_Bean, lines 152-159 and 175-176 in Menu_Bean1).
**Severity:** Low.

### 4.6 send_timezone.java -- Duplicate Insert (line 87-88)

```java
stmte1.executeUpdate(query);  // line 87
stmte1.executeUpdate(query);  // line 88 -- DUPLICATE EXECUTION
```

**Evidence:** The same `INSERT INTO outgoing` statement is executed twice. This is a bug, not just dead code.
**Severity:** High -- causes duplicate outgoing messages.

---

## 5. Hardcoded Credentials and Secrets

### 5.1 RuntimeConf.java -- Multiple Hardcoded Credentials

| Line | Field | Value |
|------|-------|-------|
| 19 | `user` | `"firmware"` |
| 20 | `pass` | `"ciifirmware"` |
| 30 | `firmwarepass` | `"Sdh79HfkLq6"` |
| 54-55 | `username`/`password` | `"TestK"` / `"testadmin"` |
| 86-88 | `USERNAME`/`PASSWORD`/`API_ID` | `"collintell"` / `"fOqDVWYK"` / `"3259470"` (Clickatell SMS API) |

**Evidence:** All values at `RuntimeConf.java` lines 18-20, 29-30, 54-55, 86-88.
**Severity:** Critical -- credentials in source code. These should be externalized to environment variables, JNDI, or encrypted configuration.

### 5.2 LindeConfig.java -- Hardcoded Server URLs and Email

| Line | Field | Value |
|------|-------|-------|
| 22 | `externalURL` | `"http://fms.fleetiq360.com"` |
| 31 | `mail_from` | `"fleetfocus@lindemh.com.au"` |
| 34 | `localURL` | `"http://localhost:8090/fms"` |
| 56 | File path | `"/home/gmtp/linde_config/"` |

**Evidence:** Hardcoded in LindeConfig.java at lines 22, 31, 34, 56.
**Severity:** Medium -- configuration values should not be in source code, though most are overridable via XML. The hardcoded file path is not.

### 5.3 send_updatepreop.java -- FTP Credentials in Outgoing Messages

```java
String ftp_upld_cmd = "FTPF=" + LindeConfig.firmwareserver + ","
    + RuntimeConf.firmwareport + ","
    + RuntimeConf.firmwareuser + ","
    + RuntimeConf.firmwarepass + ","
    + RuntimeConf.firmwareoutgoingfolder + pth + fnm;
```

**Evidence:** `send_updatepreop.java` line 524-528. FTP credentials (including password from RuntimeConf) are embedded in a message stored in the `outgoing` database table.
**Severity:** Critical -- credentials stored in plaintext in the database.

### 5.4 SendMessage.java -- API Credentials in URLs

```java
url = RuntimeConf.LOCATION + "/http/auth?user=" + RuntimeConf.USERNAME + "&password=" + RuntimeConf.PASSWORD + "&api_id=" + RuntimeConf.API_ID;
```

**Evidence:** `SendMessage.java` line 180. SMS API credentials passed as URL query parameters.
**Severity:** High -- credentials in URLs may be logged by proxies and servers.

---

## 6. SQL Injection Vulnerabilities

Nearly every file constructs SQL queries via string concatenation with unsanitized input. This is a systemic issue.

### 6.1 GdprDataDelete.java

```java
query = "... where ur.\"CUST_CD\"='" + cust_cd + "' ...";   // line 67
query = "... and \"driver_cd\"='" + driver_cd.get(i) + "'";  // line 73
```

### 6.2 InfoLogger.java

```java
queryString = "SELECT EMP_CD FROM HR_EMP_MST WHERE EMP_NM='" + tuid + "'";  // line 59
queryString = "insert into SEC_LOG_DETAILS(...) values(to_date('" + tsDate + "',...),'" + time + "','" + uid + "','" + mid + "','" + rem + "','" + emp_cd + "')";  // line 64-65
```

### 6.3 LogicBean_filter.java / LogicBean_filter1.java

```java
query = "select id, firstname, lastname from \"user\" where \"group\"='" + set_gp_cd + "' ...";  // line 122-123
query = "... where driver_id = '" + weig_id + "' ...";  // line 146-150
```

### 6.4 Menu_Bean.java / Menu_Bean1.java

```java
query = "select \"GROUP_CD\" from \"FMS_USR_GRP_REL\" where \"USER_CD\" = '" + set_user_cd + "'";  // line 77
query = "select \"FORM_CD\" from ... where \"GROUP_CD\" = '" + gp_cd + "'...";  // line 80/88
```
Also, manual construction of `IN(...)` clauses via string concatenation in `fetchform_rights()` and `fetchMenuAttr1()`.

### 6.5 SupervisorMasterHelper.java

All three methods (`deleteSupervisorByUser`, `deleteSupervisor`, `deleteSuperMaster`) construct queries with concatenated parameters.

### 6.6 PasswordExpiryAlert.java

```java
sql = "insert into email_outgoing (timestamp, to_email, subject, message) VALUES (NOW(), '" + email + "','" + subsject + "','" + message + "')";  // line 69
```

### 6.7 fix_department.java

Extensive string-concatenated queries throughout `show_cust_dept()` and `fix_dept()` methods (lines 42-48, 121, 131, 142, 148, 156, 159, 165, 168, 174, 177, 183, 186, etc.).

### 6.8 UtilBean.java

```java
String sql = "select \"LOC_CD\" from \"FMS_USER_DEPT_REL\" where \"USER_CD\" = " + webUserCD;  // line 86
```

### 6.9 password_life.java / password_policy.java

```java
queryString = "select nvl(emplpass_reset_flag,' ') from empl_passwords where emplpass_empid='" + userid + "'";  // password_life line 76
```

**Total:** All 24 files that perform DB operations use string concatenation. Zero use of PreparedStatement.
**Severity:** Critical -- systemic SQL injection risk.

---

## 7. Resource Leaks

### 7.1 LogicBean_filter.java -- Connection Never Closed on Exception Path

In `init()` (line 180-210), `conn.close()` is called only in the happy path (line 202). If an exception occurs after the connection is opened but before `conn.close()`, the connection leaks. There is no `finally` block.

**Evidence:** Lines 180-210 -- no `finally` block.
**Severity:** High.

### 7.2 password_life.java / password_policy.java -- No finally Block

Both `init()` methods close the connection only in the happy path (`conn.close()` at line 159/131). No `finally` block ensures cleanup on exception.

**Evidence:** `password_life.java` lines 143-167; `password_policy.java` lines 115-139.
**Severity:** High.

### 7.3 GetHtml.java -- Streams Not Closed on Exception

In `getHTML()` (line 16-38), `BufferedReader rd` and `HttpURLConnection conn` are only closed in the happy path. If an exception occurs, `rd` is never closed.

In `getHTML1()` (line 74-104), `conn.disconnect()` and `rd.close()` are only in the happy path.

**Evidence:** No `finally` blocks in either method.
**Severity:** Medium.

### 7.4 InfoLogger.java -- Connection and Statement Leak

Instance fields `conn` and `stmt` are opened in `writelog()` but only `conn.close()` is guaranteed via `finally`. `stmt` is never explicitly closed. Also, `ResultSet rset` is never closed.

**Evidence:** Lines 18-22 (instance fields), line 67 (`conn.close()` in try block), lines 73-82 (finally only closes conn).
**Severity:** Medium.

### 7.5 GdprDataDelete.java -- Unused Import / Unused Field

- `import com.torrent.surat.fms6.excel.Frm_excel;` (line 19) is never used.
- `ArrayList` is imported (line 7) but used with raw type.
- Field `rs` declared at line 30 but never populated (always null in finally block).

**Severity:** Low.

### 7.6 MigrateMaster.java -- e.getMessage() Called but Return Value Discarded

```java
} catch(Exception e) {
    e.printStackTrace();
    e.getMessage();   // line 316 -- return value not used
}
```

**Evidence:** Line 316.
**Severity:** Low.

### 7.7 PasswordExpiryAlert.java -- e.getMessage() Called but Return Value Discarded

```java
} catch (Exception e) {
    e.printStackTrace();
    e.getMessage();   // line 79 -- return value not used
}
```

**Evidence:** Line 79.
**Severity:** Low.

---

## 8. Broad / Empty Exception Catches

### 8.1 Broad `catch(Exception e)` Throughout

Every file in scope uses `catch(Exception e)` instead of catching specific exceptions. This masks potential programming errors by catching RuntimeExceptions alongside checked exceptions.

**Count:** 48 occurrences of `catch(Exception e)` across the 24 files.
**Severity:** Medium.

### 8.2 e.printStackTrace() Throughout

**Count:** 59 occurrences of `e.printStackTrace()` across the 24 assigned files (only counting files in scope).
**Impact:** Stack traces go to System.err (typically server logs) instead of a structured logging framework. In production, this is unstructured noise.
**Severity:** Medium.

### 8.3 System.out.println for Error Output

**Count:** 270 occurrences of `System.out.print` across the assigned files.
**Impact:** Not using a logging framework means no log levels, no log rotation, no structured output.
**Severity:** Medium.

### 8.4 Swallowed Exceptions in Finally Blocks

Many finally blocks catch `SQLException` and print to System.out but take no corrective action. For example, in `GdprDataDelete.java` lines 116-138, `send_timezone.java` lines 104-129, `fix_department.java` lines 68-93, and many others.

**Severity:** Low -- standard for this codebase but not ideal.

---

## 9. Missing Transactions

### 9.1 GdprDataDelete.java -- Multi-Table Deletes Without Transaction

`call_gdpr_delete_data()` deletes from 6 tables per driver (`fms_io_data_dtl`, `fms_io_data`, `fms_stat_data_dtl`, `fms_stat_data`, `fms_usage_data_dtl`, `fms_usage_data`, `op_chk_checklistanswer`, `op_chk_checklistresult`, `fms_unit_unlock_data`) in a loop. No transaction boundary or `autocommit(false)` is set.

**Evidence:** Lines 72-97 -- 10 `executeUpdate()` calls per driver iteration with no transaction.
**Severity:** High -- partial deletes could leave data in an inconsistent state.

### 9.2 MigrateMaster.java -- Multi-Table Operations Without Transaction

`callMigrateMaster()` performs deletes from `FMS_LOC_OVERRIDE`, inserts into `FMS_LOC_OVERRIDE`, updates to `FMS_USR_MST`, inserts into `FMS_DEPT_OVERRIDE` -- all without transactions.

**Evidence:** Lines 60-311 -- dozens of DML statements with no transaction boundary.
**Severity:** High.

### 9.3 fix_department.java -- Multi-Table Updates Without Transaction

`fix_dept()` updates 11+ tables (`FMS_DEPT_MST`, `FMS_CUST_DEPT_REL`, `FMS_OPCHK_QUEST_MST`, `FMS_USER_DEPT_REL`, `FMS_USR_VEHICLE_REL`, `dayhours`, `fms_can_input_settings`, `fms_impact_month_cache`, `fms_impact_month_driver_cache`, `fms_monthly_rpt_subscription`, `mymessages_users`, `FMS_EMAIL_CONF`, `site_settings_by_hour`) to reassign department codes.

**Evidence:** Lines 139-263 -- 13 update statements with no transaction.
**Severity:** High.

### 9.4 SupervisorMasterHelper.java -- Delete + Insert Without Transaction

All three methods perform delete-then-insert sequences across `FMS_LOC_OVERRIDE`/`FMS_DEPT_OVERRIDE`, `FMS_USR_MST`, `outgoing`, and `outgoing_stat` without transactions.

**Evidence:** Lines 48-98, 222-309, 362-416.
**Severity:** High.

### 9.5 PasswordExpiryAlert.java -- Insert + Update Without Transaction

`checkExpiry()` inserts into `email_outgoing` and then updates `FMS_USR_MST` for each user. If the update fails, the email record exists but the user is not marked as alerted.

**Evidence:** Lines 69-73.
**Severity:** Medium.

---

## 10. Unused Imports

| File | Unused Import(s) |
|------|-----------------|
| `LogicBean_filter.java` | `java.io.PrintStream`, `java.util.Properties`, `javax.servlet.http.HttpSession` |
| `LogicBean_filter1.java` | `java.io.PrintStream`, `java.util.Properties`, `javax.servlet.http.HttpSession` |
| `Menu_Bean.java` | `java.lang.*` (auto-imported), `java.io.*` (no file I/O) |
| `Menu_Bean1.java` | `java.lang.*` (auto-imported), `java.io.*` (no file I/O) |
| `password_life.java` | `java.io.PrintStream` |
| `password_policy.java` | `java.io.PrintStream` |
| `GdprDataDelete.java` | `com.torrent.surat.fms6.excel.Frm_excel`, `java.util.Calendar`, `java.util.Date`, `java.util.GregorianCalendar`, `java.util.TimeZone`, `java.util.ArrayList` (raw type), `java.util.HashMap` (raw type) |
| `send_timezone.java` | `com.torrent.surat.fms6.excel.Frm_excel` |
| `fix_department.java` | `javax.servlet.http.HttpServletRequest`, `java.util.Calendar`, `java.util.Date`, `java.util.GregorianCalendar`, `java.util.TimeZone` |
| `call_mail.java` | `java.util.Properties`, `java.util.Hashtable`, `javax.servlet.http.HttpServletRequest`, `java.net.InetAddress.*` |
| `GetHtml.java` | `java.text.SimpleDateFormat`, `java.util.Calendar` (used only in `getHTML1` internal `now()` helper) |
| `send_updatepreop.java` | `java.io.File`, `java.io.FileOutputStream`, `java.io.IOException`, `java.io.DataOutputStream` (used only in `resyncPreop`, some are conditionally used) |
| `SendMessage.java` | `java.util.List` (assigned but `ArrayList` would suffice given usage) |

**Severity:** Low.

---

## 11. Raw Types / Missing Generics

The following files use raw `ArrayList` without type parameters:

| File | Lines |
|------|-------|
| `LogicBean_filter.java` | Lines 37-66 -- all 24 ArrayLists are raw |
| `LogicBean_filter1.java` | Lines 38-67 -- all 24 ArrayLists are raw |
| `Menu_Bean.java` | Lines 39-47 -- all ArrayLists are raw |
| `Menu_Bean1.java` | Lines 37-44 -- all ArrayLists are raw |
| `GdprDataDelete.java` | Line 62 -- `ArrayList driver_cd = new ArrayList()` |
| `fix_department.java` | Lines 309-314 -- all 6 ArrayLists are raw |
| `SupervisorMasterHelper.java` | Lines 63, 101, 132, 269 -- raw ArrayLists |
| `MigrateMaster.java` | Lines 112-117 -- `Drivers`, `Gmtp_id`, `Slot_No`, `Weigs`, `supervisorAccessList`, `vehCdList` |
| `send_updatepreop.java` | Lines 98, 191-194, 197 -- raw ArrayLists |
| `SendMessage.java` | Line 122 -- `String[] array_ret` used loosely |

**Severity:** Low -- compiler warnings, potential `ClassCastException` at runtime.

---

## 12. Style Consistency Issues

### 12.1 Inconsistent Indentation and Brace Style

- `Menu_Bean.java` / `Menu_Bean1.java`: Deeply inconsistent indentation (e.g., line 275 closing brace at 3 tabs, line 276 at 2 tabs, line 277 at 1 tab).
- `call_mail.java`: Mixed tabs and spaces throughout.
- `password_life.java` / `password_policy.java`: Decompiled code with inconsistent whitespace.

### 12.2 Inconsistent Field Visibility

- `LogicBean_filter.java` / `LogicBean_filter1.java`: All fields are package-private (no modifier). Should be `private` with getters.
- `password_life.java` / `password_policy.java`: Fields like `queryString`, `userid`, `logintime`, `ip` are `public`. Should be `private`.
- `Menu_Bean.java` / `Menu_Bean1.java`: Fields like `FormId`, `appl_path`, `FormName` are `public`. Should be `private`.

### 12.3 Decompiled Code Artifacts

`password_life.java` line 1: `// Decompiled by DJ v3.9.9.91 Copyright 2005 Atanas Neshkov Date: 2/11/2006 11:48:36 AM`

This indicates the original source was lost and the class was recovered from bytecode. The code quality reflects decompiler output rather than hand-written code.

**Severity:** Low (informational).

---

## 13. Incorrect / Misleading Error Messages

### 13.1 GdprDataDelete.java -- Wrong Method Name in Error Message

```java
System.out.println("Exception in the send_timezone() Method..." + e);  // line 110
```

**Evidence:** The method is `call_gdpr_delete_data()`, but the error message says `send_timezone()`.
**Severity:** Low -- misleading for debugging.

### 13.2 fix_department.java -- Wrong Method Name in Error Message

```java
System.out.println("Exception in the send_timezone() Method..." + e);  // line 64, 276
```

**Evidence:** The methods are `show_cust_dept()` and `fix_dept()`, but the error message says `send_timezone()`.
**Severity:** Low -- copy-paste error from `send_timezone.java`.

### 13.3 LogicBean_filter.java / LogicBean_filter1.java -- Wrong Class Name in Error Message

```java
System.out.println(" Exception in LogicBean_LoginAlerter In " + methodName + ...);  // line 208 / 398
```

**Evidence:** The class is `LogicBean_filter` / `LogicBean_filter1`, but the error message references `LogicBean_LoginAlerter`.
**Severity:** Low.

### 13.4 PasswordExpiryAlert.java -- Typo in Variable Name

```java
String subsject = "";  // line 58 -- "subsject" should be "subject"
```

**Severity:** Low -- cosmetic, variable is used correctly despite misspelling.

---

## 14. Duplicate Code Within send_timezone.java

`send_timezone.java` contains three methods that are near-duplicates:
1. `call_send_timezone()` (lines 27-130) -- UK timezone handling (original version with bulk insert bug)
2. `call_send_timezone_test()` (lines 132-251) -- UK timezone handling (test version with per-unit insert)
3. `call_send_timezone_au()` (lines 254-416) -- AU timezone handling

All three duplicate the entire JNDI lookup, connection management, and resource cleanup pattern. The entire resource cleanup block (lines 102-129 / 223-250 / 389-416) is copy-pasted identically three times.

**Severity:** Medium -- high duplication increases maintenance risk.

---

## 15. Thread Safety Concerns

### 15.1 LindeConfig.java -- Mutable Public Static Fields

All configuration fields in `LindeConfig` are `public static` non-final mutable fields (lines 20-46). The `readXMLFile()` method modifies these from the constructor, but any thread can modify them at any time.

**Evidence:** Lines 20-46 -- 20+ mutable static fields.
**Severity:** Medium -- race condition risk in multi-threaded servlet environment.

### 15.2 RuntimeConf.java -- Mutable Public Static Fields

All non-final fields in `RuntimeConf` are `public static` and mutable. `LindeConfig.readXMLFile()` modifies `RuntimeConf.mail_from` (line 97).

**Evidence:** Lines 5-127 -- dozens of mutable static fields.
**Severity:** Medium.

---

## 16. Specific File-Level Findings Summary

| # | File | Lines | Key Issues |
|---|------|-------|-----------|
| 1 | `GdprDataDelete.java` | 143 | SQL injection, no transaction, e.printStackTrace(), wrong error message, unused import |
| 2 | `GetHtml.java` | 113 | Commented-out code (30 lines), resource leak (no finally), e.printStackTrace(), string concat in loop |
| 3 | `ImportFiles.java` | 2,692 | **God class**, massive doPost(), raw types, commented-out code throughout |
| 4 | `InfoLogger.java` | 107 | SQL injection, resource leak (stmt/rset never closed), no finally for DB resources |
| 5 | `LindeConfig.java` | 146 | Hardcoded URLs/email, mutable statics, broad catch, hardcoded file path |
| 6 | `LogicBean_filter.java` | 475 | SQL injection, raw types, unused imports, connection leak (no finally), duplicate of filter1 |
| 7 | `LogicBean_filter1.java` | 782 | SQL injection, raw types, unused imports, duplicate of filter, wrong error message |
| 8 | `Menu_Bean.java` | 310 | SQL injection, raw types, `import java.lang.*`, duplicate of Menu_Bean1 |
| 9 | `Menu_Bean1.java` | 293 | SQL injection, raw types, `import java.lang.*`, duplicate of Menu_Bean, debug query in output |
| 10 | `MigrateMaster.java` | 325 | SQL injection, no transaction, e.getMessage() discarded |
| 11 | `PasswordExpiryAlert.java` | 102 | SQL injection, no transaction, e.getMessage() discarded, typo in variable |
| 12 | `PurgeData.java` | 5 | **Empty class** -- dead code |
| 13 | `RuntimeConf.java` | 156 | **Hardcoded credentials** (5 sets), mutable statics, hardcoded URLs/paths |
| 14 | `SendMessage.java` | 242 | SQL injection, credentials in URLs, deprecated `DataInputStream.readLine()`, e.printStackTrace() |
| 15 | `SupervisorMasterHelper.java` | 446 | SQL injection, no transaction, raw types, duplicated outgoing message pattern |
| 16 | `UtilBean.java` | 413 | SQL injection, e.printStackTrace(), template method with no logic |
| 17 | `call_mail.java` | 1,454 | SQL injection, e.printStackTrace(), god-class behavior, unused imports |
| 18 | `escapeSingleQuotes.java` | 19 | Non-standard class name, no null guard (loop condition handles null but StringBuffer is redundant) |
| 19 | `fix_department.java` | 388 | SQL injection, no transaction, wrong error message, raw types |
| 20 | `mail.java` | 311 | SQL injection, dead DB query in `Ename()`, e.printStackTrace(), non-standard name |
| 21 | `password_life.java` | 187 | Decompiled code, SQL injection, no finally block, unused import, non-standard name |
| 22 | `password_policy.java` | 159 | Decompiled code, SQL injection, no finally block, unused import, non-standard name |
| 23 | `send_timezone.java` | 417 | SQL injection, **duplicate insert bug**, 3x code duplication, non-standard name |
| 24 | `send_updatepreop.java` | 601 | SQL injection, FTP creds in DB, e.printStackTrace(), non-standard name |

---

## 17. Aggregate Metrics

| Metric | Count |
|--------|-------|
| Total files audited | 24 |
| Files with non-standard class names | 8 (33%) |
| Files with SQL injection risk | 22 (92%) -- all files with DB operations |
| Files with e.printStackTrace() | 22 (92%) |
| Files with System.out.print usage | 22 (92%) |
| Files with broad catch(Exception) | 20 (83%) |
| Files with resource leak risk | 8 (33%) |
| Files with hardcoded credentials | 2 (RuntimeConf, SendMessage via RuntimeConf) |
| Files with missing transactions | 6 (25%) |
| Near-duplicate file pairs | 3 pairs (Menu_Bean/1, LogicBean_filter/1, password_life/policy) |
| Dead code files | 1 (PurgeData) |
| God classes (>500 lines) | 3 (ImportFiles 2692, call_mail 1454, send_updatepreop 601) |
| Files with unused imports | 13 (54%) |

---

## 18. Priority Recommendations (Report Only)

1. **Critical:** Remove hardcoded credentials from `RuntimeConf.java` and externalize to secure configuration.
2. **Critical:** Replace all string-concatenated SQL with `PreparedStatement` across all 22 DB-using files.
3. **Critical:** Fix the duplicate `executeUpdate` bug in `send_timezone.java` line 87-88.
4. **High:** Refactor `ImportFiles.java` (2,692 lines) into strategy-pattern handlers per import type.
5. **High:** Consolidate `Menu_Bean` / `Menu_Bean1` into a single parameterized class.
6. **High:** Consolidate `LogicBean_filter` / `LogicBean_filter1` into a single class with optional sort.
7. **High:** Add transaction boundaries to `GdprDataDelete`, `MigrateMaster`, `fix_department`, `SupervisorMasterHelper`.
8. **High:** Fix resource leaks in `LogicBean_filter`, `password_life`, `password_policy`, `GetHtml`.
9. **Medium:** Delete `PurgeData.java` (empty class).
10. **Medium:** Rename 8 snake_case classes to PascalCase.
11. **Medium:** Replace `System.out.println` and `e.printStackTrace()` with structured logging (Log4j2 is already available in some files).
12. **Low:** Remove commented-out code, fix misleading error messages, add generics to raw types.

---

*End of Pass 4 audit for util G-Z.*
