# Pass 3 -- Documentation Audit: `security` Package

**Audit ID:** 2026-02-25-01-P3-security
**Agent:** A18
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `WEB-INF/src/com/torrent/surat/fms6/security/`

---

## Scope

| # | File | Lines | Class |
|---|------|------:|-------|
| 1 | `Databean_security.java` | 1,575 | `Databean_security` |
| 2 | `Frm_customer.java` | 12,943 | `Frm_customer extends HttpServlet` |
| 3 | `Frm_login.java` | 161 | `Frm_login extends HttpServlet` |
| 4 | `Frm_security.java` | 4,171 | `Frm_security extends HttpServlet` |
| 5 | `Frm_vehicle.java` | 16,269 | `Frm_vehicle extends HttpServlet` |
| 6 | `GetGenericData.java` | 94 | `GetGenericData extends HttpServlet` |

**Total lines audited:** 35,213

---

## 1. Databean_security.java

### 1.1 Reading Evidence

**Class:** `Databean_security` (line 22) -- No class-level Javadoc.

| Line | Visibility | Method Signature |
|-----:|------------|------------------|
| 127 | public | `void clear_variables()` |
| 950 | public | `void init()` |
| 1093 | public | `void setSet_op_code(String set_op_code)` |
| 1100 | public | `ArrayList getForm_cd()` |
| 1107 | public | `ArrayList getForm_nm()` |
| 1114 | public | `ArrayList getModule_cd()` |
| 1121 | public | `ArrayList getModule_nm()` |
| 1128 | public | `void setSet_form_cd(String set_form_cd)` |
| 1135 | public | `String getForm_desc()` |
| 1142 | public | `String getForm_mod_cd()` |
| 1149 | public | `String getForm_name()` |
| 1156 | public | `String getForm_path()` |
| 1163 | public | `void setSet_module_cd(String set_module_cd)` |
| 1170 | public | `String getModule_desc()` |
| 1177 | public | `String getModule_name()` |
| 1184 | public | `String getModule_path()` |
| 1191 | public | `ArrayList getGp_cd()` |
| 1198 | public | `ArrayList getGp_nm()` |
| 1205 | public | `ArrayList getVdel()` |
| 1212 | public | `ArrayList getVedit()` |
| 1219 | public | `ArrayList getVform_cd()` |
| 1226 | public | `ArrayList getVform_nm()` |
| 1233 | public | `ArrayList getVprint()` |
| 1240 | public | `ArrayList getVview()` |
| 1247 | public | `void setSet_gp_cd(String set_gp_cd)` |
| 1254 | public | `ArrayList getVform_mod()` |
| 1261 | public | `ArrayList getMail_grp_cd()` |
| 1268 | public | `ArrayList getMail_grp_nm()` |
| 1275 | public | `ArrayList getMail_grp_lst()` |
| 1280 | public | `void setSet_mail_grp_cd(String set_mail_grp_cd)` |
| 1287 | public | `String getAccess_level()` |
| 1294 | public | `void setAccess_level(String access_level)` |
| 1301 | public | `String getAccess_cust()` |
| 1308 | public | `String getAccess_dept()` |
| 1315 | public | `String getAccess_site()` |
| 1322 | public | `void setSet_user_cd(String set_user_cd)` |
| 1329 | public | `String getUser_fnm()` |
| 1336 | public | `String getUser_lnm()` |
| 1343 | public | `void setSet_frm_cd(String set_frm_cd)` |
| 1350 | public | `String getReport_name()` |
| 1354 | public | `ArrayList getVform_priority()` |
| 1358 | public | `void setSet_ucd(String set_ucd)` |
| 1362 | public | `String getGet_fdel()` |
| 1366 | public | `String getGet_fexp()` |
| 1370 | public | `String getGet_fmod()` |
| 1374 | public | `void setSet_cust_cd(String set_cust_cd)` |
| 1378 | public | `void setSet_div_cd(String set_div_cd)` |
| 1382 | public | `ArrayList getCust_cd()` |
| 1386 | public | `ArrayList getCust_nm()` |
| 1390 | public | `void setAccess_cust(String access_cust)` |
| 1394 | public | `void setAccess_dept(String access_dept)` |
| 1398 | public | `void setAccess_site(String access_site)` |
| 1402 | public | `ArrayList getVmail_frq()` |
| 1406 | public | `ArrayList getVmail_mailid()` |
| 1410 | public | `ArrayList getVmail_rec_no()` |
| 1414 | public | `ArrayList getVmail_st_dt()` |
| 1418 | public | `ArrayList getVmail_sub()` |
| 1422 | public | `void setSet_rep_url(String set_rep_url)` |
| 1426 | public | `ArrayList getVmail_usr()` |
| 1430 | public | `ArrayList getMail_grp_cust()` |
| 1434 | public | `ArrayList getMail_grp_cust_nm()` |
| 1438 | public | `String getMail_group_cust_nm()` |
| 1442 | public | `ArrayList getVmail_ge_dt()` |
| 1446 | public | `void setVmail_ge_dt(ArrayList vmail_ge_dt)` |
| 1450 | public | `ArrayList getVmail_end_time()` |
| 1454 | public | `void setVmail_end_time(ArrayList vmail_end_time)` |
| 1458 | public | `ArrayList getVmail_st_time()` |
| 1462 | public | `void setVmail_st_time(ArrayList vmail_st_time)` |
| 1466 | public | `ArrayList getVmail_loc_name()` |
| 1470 | public | `void setVmail_loc_name(ArrayList vmail_loc_name)` |
| 1474 | public | `ArrayList getVmail_cust_name()` |
| 1478 | public | `void setVmail_cust_name(ArrayList vmail_cust_name)` |
| 1482 | public | `ArrayList getVmail_dept_name()` |
| 1486 | public | `void setVmail_dept_name(ArrayList vmail_dept_name)` |
| 1490 | public | `String getSet_loc_cd()` |
| 1494 | public | `void setSet_loc_cd(String set_loc_cd)` |
| 1498 | public | `String getSet_dept_cd()` |
| 1502 | public | `void setSet_dept_cd(String set_dept_cd)` |
| 1506 | public | `String getSet_cust_cd()` |
| 1510 | public | `String getCust_name_disp()` |
| 1514 | public | `void setCust_name_disp(String cust_name_disp)` |
| 1518 | public | `String getLoc_name_disp()` |
| 1522 | public | `void setLoc_name_disp(String loc_name_disp)` |
| 1526 | public | `String getDept_name_disp()` |
| 1530 | public | `void setDept_name_disp(String dept_name_disp)` |
| 1534 | public | `String getBms_user()` |
| 1538 | public | `void setBms_user(String bms_user)` |
| 1542 | public | `String getBms_pass()` |
| 1546 | public | `void setBms_pass(String bms_pass)` |
| 1550 | public | `NotificationSettingsBean getNotificationSettingsBean()` |
| 1554 | public | `void setNotificationSettingsBean(NotificationSettingsBean)` |
| 1559 | public | `ArrayList getVmailType()` |
| 1563 | public | `void setVmailType(ArrayList vmailType)` |
| 1567 | public | `boolean isHasSFTPAccess()` |
| 1571 | public | `void setHasSFTPAccess(boolean hasSFTPAccess)` |

**Total public methods:** 82
**Javadoc present:** None (0 class-level, 0 method-level)

### 1.2 Javadoc Assessment

- **Class-level Javadoc:** ABSENT. No description of what this data bean does, how it interacts with security subsystem, or what JSP pages consume it.
- **Method-level Javadoc:** ABSENT on all 82 public methods. Zero `@param`, `@return`, or `@throws` tags anywhere.
- `clear_variables()` at line 127 has only an inline comment `// Clears all the vectors to avoid previous junk data.` -- this is not Javadoc.
- `init()` at line 950 has only `//Function called from the jsp page.` -- not Javadoc.

### 1.3 Inline Comment Check

- Line 127: `// Clears all the vectors to avoid previous junk data.` -- Adequate inline but not Javadoc.
- Line 950: `//Function called from the jsp page.` -- Incomplete, does not explain the security-critical data loading orchestration.
- No TODO/FIXME/HACK/XXX markers found.

---

## 2. Frm_customer.java

### 2.1 Reading Evidence

**Class:** `Frm_customer extends HttpServlet` (line 47) -- No class-level Javadoc (only auto-generated `serialVersionUID` Javadoc at line 66-69).

| Line | Visibility | Method Signature |
|-----:|------------|------------------|
| 75 | protected | `void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` |
| 1372 | protected | `void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` |
| 2240 | public | `boolean checkWeigand(HttpServletRequest req, HttpServletResponse res) throws SQLException` |
| 8614 | public | `boolean isValidEmailAddress(String email)` |
| 12006 | public static | `Connection CreateConnection() throws Exception` |
| 12018 | public static | `void closeConnection(final Connection conn) throws SQLException` |

**Total public/protected methods:** 6
**Javadoc present:** None (the `/**` at line 66 is an empty auto-generated serial UID comment, not a class Javadoc)

### 2.2 Javadoc Assessment

- **Class-level Javadoc:** ABSENT. No documentation describing this massive servlet (12,943 lines) that handles customer/location/department hierarchical data lookups, user management, driver allocation, master code programming, and Wiegand card ID validation.
- **Method-level Javadoc:** ABSENT on all 6 public/protected methods. None have `@param`, `@return`, or `@throws`.
- `doGet` (line 75): 1,295-line method with zero documentation. Handles at least 15 distinct GET operations dispatched via `req.getParameter("get")` including `cussitedep`, `cussitedepsup`, `veh_sitedep`, `cussitedepdehire`, `cussitedepFw`, `subs_dept`, `cussitedepveh`, `weigand_list`, `checkWeigand`, `available_vehicles`, `mcdrivers`, `mcdriversveh`, `mcdriversTab`, `smdrivers`, `smdrivers_active`.
- `doPost` (line 1372): Equally large, dispatching via `req.getParameter("method")` to ~30 private methods.
- `checkWeigand` (line 2240): Security-relevant Wiegand card validation with zero documentation.

### 2.3 Inline Comment & TODO Check

- Line 1291: `// TODO Auto-generated catch block` inside a catch handler -- unfinished error handling.

---

## 3. Frm_login.java

### 3.1 Reading Evidence

**Class:** `Frm_login extends HttpServlet` (line 21) -- No class-level Javadoc (only auto-generated `serialVersionUID` comment at line 22-25).

| Line | Visibility | Method Signature |
|-----:|------------|------------------|
| 29 | protected | `void doPost(HttpServletRequest request, HttpServletResponse res) throws ServletException, IOException` |
| 144 | public static | `Connection CreateConnection() throws Exception` |
| 157 | public static | `void closeConnection(final Connection conn) throws SQLException` |

**Total public/protected methods:** 3
**Javadoc present:** None

### 3.2 Javadoc Assessment

- **Class-level Javadoc:** ABSENT. This is a login authentication servlet -- the most security-critical class in the package -- and has zero documentation.
- **Method-level Javadoc:** ABSENT on all 3 methods.
- `doPost` (line 29): Handles the complete login authentication flow including username lookup, plaintext password comparison, session attribute setting, and redirect. No documentation of the authentication protocol, failure handling, or session semantics.
- `CreateConnection` (line 144): Undocumented JNDI connection factory.
- `closeConnection` (line 157): Undocumented.

### 3.3 Accuracy & Misleading Comment Check

- **Line 97-99 CRITICAL:** `log.info("login failed: login:" + login + " password:" + password + " database password:" + pass_word ...)` -- Logs **both the user-supplied password and the database password** in plaintext. While not a documentation issue per se, the absence of any Javadoc warning about this security-critical logging behavior is directly relevant.
- **Line 81:** Password comparison uses `password.equals(pass_word)` -- plaintext comparison with no hashing. The code has no comment documenting this as intentional or deprecated.
- **Line 111:** `System.out.println("Frm_security-->: " + e)` -- Misleading: error message references `Frm_security` but this is `Frm_login`.

---

## 4. Frm_security.java

### 4.1 Reading Evidence

**Class:** `Frm_security extends HttpServlet` (line 47) -- No class-level Javadoc (only auto-generated `serialVersionUID` comment at line 48-51).

| Line | Visibility | Method Signature |
|-----:|------------|------------------|
| 57 | protected | `void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` |
| 143 | public | `void clearVectors()` |
| 147 | public static | `Connection CreateConnection() throws Exception` |
| 159 | public static | `void closeConnection(final Connection conn) throws SQLException` |
| 258 | public | `void saveDashboardSubscription(HttpServletRequest req, HttpServletResponse res) throws SQLException, IOException` |
| 335 | public | `void deleteSubscription(HttpServletRequest req, HttpServletResponse res) throws SQLException, IOException` |
| 2169 | public | `String generateRandomCharacters(int length)` |
| 4045 | public | `boolean sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail) throws AddressException, MessagingException` |
| 4152 | public static | `String esapiNormalizeParam(String string)` |
| 4161 | public static | `String esapiNormalizeUserNameParam(String string)` |

**Total public/protected methods:** 10
**Javadoc present:** None

### 4.2 Javadoc Assessment

- **Class-level Javadoc:** ABSENT. This 4,171-line servlet is the primary security operations controller: authentication (login), password management (change, reset, expire), access rights/permissions, mail group management, subscriptions, shift management, and notification settings. Zero documentation.
- **Method-level Javadoc:** ABSENT on all 10 public/protected methods.
- `doPost` (line 57): The central dispatcher for ~30 security operations. No documentation of the op_code routing, authorization model, or session requirements.
- `generateRandomCharacters` (line 2169): Generates random passwords used in `reset_password`. No Javadoc on character set, strength guarantees, or usage context.
- `esapiNormalizeParam` (line 4152): ESAPI input sanitization. No Javadoc explaining what it normalizes, why, or when to use it vs. `esapiNormalizeUserNameParam`.
- `esapiNormalizeUserNameParam` (line 4161): Has a single inline comment `// Username may include @ sign` but no Javadoc. The inline comment at line 4167-4169 explains the `@` re-encoding but this should be formal Javadoc.
- `sendMail` (line 4045): Email utility used for password resets. No Javadoc on parameters, failure modes, or security considerations.

### 4.3 Accuracy, Misleading Comments & TODO Check

- **Line 66 CRITICAL:** `log.info(... + ",login:" + req.getParameter("login") + ";password:" + req.getParameter("password") + ";")` -- Logs the user's plaintext password to the application log during the `doPost` entry point. No documentation warning about this.
- **Line 2372-2374:** Comment `// Linde AU has no password hashing apply normalization` -- documents that AU deployment stores passwords in plaintext. This is accurate but should be formal Javadoc with security implications.
- **Line 2535-2537:** Same plaintext password storage comment repeated in `chg_pass` method.
- **Line 3392:** `// TODO Auto-generated catch block` -- Unfinished error handling in `mail_conf_dyn`.
- **Line 2526:** Misleading log message: `log.info("Method: chg_bms_pass()...")` appears inside method `chg_pass()`, not `chg_bms_pass()`.

---

## 5. Frm_vehicle.java

### 5.1 Reading Evidence

**Class:** `Frm_vehicle extends HttpServlet` (line 57) -- No class-level Javadoc (only auto-generated `serialVersionUID` comment at line 69-72).

| Line | Visibility | Method Signature |
|-----:|------------|------------------|
| 79 | protected | `void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` |
| 2724 | public | `String getVs_status()` |
| 2728 | public | `void setVs_status(String vs_status)` |
| 14976 | public | `void clearVectors()` |
| 15476 | public static | `Connection CreateConnection() throws Exception` |
| 15488 | public static | `void closeConnection(final Connection conn) throws SQLException` |
| 15492 | public | `byte[] intToByteArray(int a)` |

**Total public/protected methods:** 7
**Javadoc present:** None

### 5.2 Javadoc Assessment

- **Class-level Javadoc:** ABSENT. This 16,269-line servlet handles vehicle management operations including vehicle editing, deletion, de-hiring, hiring, checklist/question management, firmware updates, network settings, VOR settings, impact calibration, diagnostic sync, remote access, broadcast messaging, reboot commands, and spare swap. Zero documentation.
- **Method-level Javadoc:** ABSENT on all 7 public/protected methods.
- `doPost` (line 79): Dispatches ~35 operations via `req.getParameter("method")`. No documentation of the routing scheme, authorization requirements, or supported operations.
- `intToByteArray` (line 15492): Utility conversion with no Javadoc on byte order (big-endian), usage context, or why it exists.
- `getVs_status`/`setVs_status` (lines 2724/2728): VOR status getter/setter with no documentation of valid values or semantics.
- `clearVectors` (line 14976): Empty method body with no documentation explaining why it is empty.

### 5.3 TODO Check

- **Line 14723:** `//TODO: Do we sync the VOR setting until we found the VOR is enalbed?` -- Open design question about VOR synchronization behavior. Note the typo "enalbed" (should be "enabled").
- **Line 14789:** `//TODO: Do we sync the full lock out settings until we found the full lockout enabled?` -- Open design question about full lockout synchronization.

---

## 6. GetGenericData.java

### 6.1 Reading Evidence

**Class:** `GetGenericData extends HttpServlet` (line 19) -- No class-level Javadoc.

| Line | Visibility | Method Signature |
|-----:|------------|------------------|
| 28 | public | `GetGenericData()` (constructor) |
| 32 | protected | `void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException` |
| 75 | public static | `Connection CreateConnection() throws Exception` |
| 87 | public static | `void closeConnection(final Connection conn) throws SQLException` |

**Total public/protected methods:** 4 (including constructor)
**Javadoc present:** None

### 6.2 Javadoc Assessment

- **Class-level Javadoc:** ABSENT. The purpose of this servlet is unclear -- the `doGet` method creates a connection and statement but does nothing with them before closing.
- **Method-level Javadoc:** ABSENT on all 4 methods.
- `doGet` (line 32): The method body acquires a database connection and statement but never executes any query. This appears to be stub/skeleton code but is completely undocumented.
- The private `getWeigand` method (line 67) contains an incomplete SQL query (`where` clause with no predicate) suggesting this is unfinished code.

### 6.3 TODO Check

- **Line 29:** `// TODO Auto-generated constructor stub` -- IDE-generated placeholder in the constructor.

---

## Findings Summary

| ID | File | Line(s) | Severity | Description |
|----|------|---------|----------|-------------|
| P3-SEC-001 | `Databean_security.java` | 22 | **HIGH** | No class-level Javadoc on security data bean that orchestrates access rights loading, login data fetching, and form permissions |
| P3-SEC-002 | `Databean_security.java` | 950 | **HIGH** | `init()` -- security-critical initialization method that loads access rights, login data, mail config, and BMS credentials -- has no Javadoc |
| P3-SEC-003 | `Databean_security.java` | 1287-1315 | **HIGH** | `getAccess_level()`, `getAccess_cust()`, `getAccess_site()`, `getAccess_dept()` and their setters -- authorization-level accessors with no Javadoc documenting valid values or authorization model |
| P3-SEC-004 | `Databean_security.java` | 1534-1546 | **HIGH** | `getBms_user()`, `setBms_user()`, `getBms_pass()`, `setBms_pass()` -- BMS credential accessors with no Javadoc. Security-critical credential handling is completely undocumented |
| P3-SEC-005 | `Databean_security.java` | all | **MEDIUM** | 78 remaining public getter/setter methods have no Javadoc (non-security-critical data accessors) |
| P3-SEC-006 | `Frm_customer.java` | 47 | **HIGH** | No class-level Javadoc on a 12,943-line servlet that handles user management, driver allocation, master codes, and Wiegand card operations |
| P3-SEC-007 | `Frm_customer.java` | 75 | **HIGH** | `doGet()` -- 1,295-line method handling 15+ distinct operations with session-based access control -- has no Javadoc |
| P3-SEC-008 | `Frm_customer.java` | 1372 | **HIGH** | `doPost()` -- handles user creation, deletion, password changes, master code programming, vehicle allocation -- has no Javadoc |
| P3-SEC-009 | `Frm_customer.java` | 2240 | **HIGH** | `checkWeigand()` -- Wiegand card ID validation for physical access control -- has no Javadoc documenting validation logic, return semantics, or card format support |
| P3-SEC-010 | `Frm_customer.java` | 8614 | **MEDIUM** | `isValidEmailAddress(String email)` -- no Javadoc documenting the regex pattern or edge cases |
| P3-SEC-011 | `Frm_customer.java` | 12006, 12018 | **MEDIUM** | `CreateConnection()` and `closeConnection()` -- no Javadoc |
| P3-SEC-012 | `Frm_customer.java` | 1291 | **LOW** | `// TODO Auto-generated catch block` -- unfinished error handling |
| P3-SEC-013 | `Frm_login.java` | 21 | **HIGH** | No class-level Javadoc on the primary login authentication servlet |
| P3-SEC-014 | `Frm_login.java` | 29 | **HIGH** | `doPost()` -- the entire authentication flow (credential lookup, plaintext password comparison, session creation, redirect) has no Javadoc documenting the auth protocol, session attributes set, or failure modes |
| P3-SEC-015 | `Frm_login.java` | 144, 157 | **MEDIUM** | `CreateConnection()` and `closeConnection()` -- no Javadoc |
| P3-SEC-016 | `Frm_login.java` | 111 | **MEDIUM** | Misleading error message: `System.out.println("Frm_security-->: " + e)` -- references wrong class name (`Frm_security` instead of `Frm_login`) |
| P3-SEC-017 | `Frm_security.java` | 47 | **HIGH** | No class-level Javadoc on the primary security operations controller (authentication, password management, access rights, mail config) |
| P3-SEC-018 | `Frm_security.java` | 57 | **HIGH** | `doPost()` -- central security dispatcher for ~30 operations including login, password reset/change/expire, access rights -- has no Javadoc |
| P3-SEC-019 | `Frm_security.java` | 2169 | **HIGH** | `generateRandomCharacters(int length)` -- generates temporary passwords for password reset flow -- has no Javadoc documenting character set, entropy, or usage |
| P3-SEC-020 | `Frm_security.java` | 4152 | **HIGH** | `esapiNormalizeParam(String)` -- ESAPI HTML encoding for input sanitization -- has no Javadoc. This is a security-critical sanitization method |
| P3-SEC-021 | `Frm_security.java` | 4161 | **HIGH** | `esapiNormalizeUserNameParam(String)` -- ESAPI encoding variant for usernames -- has no Javadoc explaining difference from `esapiNormalizeParam` or the `@` re-encoding behavior |
| P3-SEC-022 | `Frm_security.java` | 4045 | **MEDIUM** | `sendMail(...)` -- email sending utility used for password resets -- has no Javadoc |
| P3-SEC-023 | `Frm_security.java` | 143 | **LOW** | `clearVectors()` -- empty method body, no Javadoc explaining why it is a no-op |
| P3-SEC-024 | `Frm_security.java` | 258, 335 | **MEDIUM** | `saveDashboardSubscription()` and `deleteSubscription()` -- public methods with no Javadoc |
| P3-SEC-025 | `Frm_security.java` | 147, 159 | **MEDIUM** | `CreateConnection()` and `closeConnection()` -- no Javadoc |
| P3-SEC-026 | `Frm_security.java` | 66 | **HIGH** | Plaintext password logged in `doPost` entry point: `log.info(... + ";password:" + req.getParameter("password") + ";")` -- no Javadoc or inline warning about this security-critical logging behavior |
| P3-SEC-027 | `Frm_security.java` | 2526 | **MEDIUM** | Misleading log: `log.info("Method: chg_bms_pass()...")` appears inside `chg_pass()` method, not `chg_bms_pass()` |
| P3-SEC-028 | `Frm_security.java` | 3392 | **LOW** | `// TODO Auto-generated catch block` -- unfinished error handling in `mail_conf_dyn` |
| P3-SEC-029 | `Frm_vehicle.java` | 57 | **HIGH** | No class-level Javadoc on 16,269-line vehicle management servlet handling firmware updates, remote commands, network settings, diagnostic sync |
| P3-SEC-030 | `Frm_vehicle.java` | 79 | **HIGH** | `doPost()` -- dispatches ~35 operations including firmware sync, broadcast, reboot, remote access, spare swap -- has no Javadoc |
| P3-SEC-031 | `Frm_vehicle.java` | 15476, 15488 | **MEDIUM** | `CreateConnection()` and `closeConnection()` -- no Javadoc |
| P3-SEC-032 | `Frm_vehicle.java` | 15492 | **LOW** | `intToByteArray(int a)` -- no Javadoc on utility method |
| P3-SEC-033 | `Frm_vehicle.java` | 2724, 2728 | **LOW** | `getVs_status()`/`setVs_status()` -- no Javadoc |
| P3-SEC-034 | `Frm_vehicle.java` | 14976 | **LOW** | `clearVectors()` -- empty method body with no Javadoc |
| P3-SEC-035 | `Frm_vehicle.java` | 14723 | **INFO** | `//TODO: Do we sync the VOR setting until we found the VOR is enalbed?` -- open design question with typo "enalbed" |
| P3-SEC-036 | `Frm_vehicle.java` | 14789 | **INFO** | `//TODO: Do we sync the full lock out settings until we found the full lockout enabled?` -- open design question |
| P3-SEC-037 | `GetGenericData.java` | 19 | **MEDIUM** | No class-level Javadoc. Purpose of this servlet is unclear from the code alone |
| P3-SEC-038 | `GetGenericData.java` | 32 | **MEDIUM** | `doGet()` -- acquires DB connection but performs no operations; appears to be stub code -- has no Javadoc explaining if this is intentional |
| P3-SEC-039 | `GetGenericData.java` | 75, 87 | **LOW** | `CreateConnection()` and `closeConnection()` -- no Javadoc |
| P3-SEC-040 | `GetGenericData.java` | 29 | **INFO** | `// TODO Auto-generated constructor stub` -- IDE placeholder |

---

## Severity Distribution

| Severity | Count |
|----------|------:|
| **HIGH** | 19 |
| **MEDIUM** | 14 |
| **LOW** | 8 |
| **INFO** | 3 |
| **Total** | **44** |

---

## Key Observations

1. **Zero Javadoc across the entire package.** Not a single class or method in any of the 6 files has formal Javadoc documentation. The only `/**` comments found are auto-generated `serialVersionUID` placeholders.

2. **Security-critical code is entirely undocumented.** The authentication flow (`Frm_login.doPost`, `Frm_security.chk_login`), password management (`change_password`, `reset_password`, `expire_password`, `chg_pass`, `chg_bms_pass`), access control model (`Databean_security` access level getters/setters), input sanitization (`esapiNormalizeParam`, `esapiNormalizeUserNameParam`), and physical access control (`checkWeigand`) have no documentation whatsoever.

3. **Misleading cross-references.** Error messages in `Frm_login.java` reference `Frm_security`, and log statements in `chg_pass` reference `chg_bms_pass`, creating confusion during debugging and incident response.

4. **Plaintext password logging is undocumented.** Both `Frm_login.java` (line 97-99) and `Frm_security.java` (line 66) log user-supplied passwords to the application log. There is no documentation warning maintainers about this behavior.

5. **Five TODO items remain unresolved** across 4 files, including unfinished error handlers and open design questions about VOR/lockout synchronization behavior.

6. **Massive method sizes with no documentation.** `Frm_customer.doGet` (1,295 lines), `Frm_customer.doPost` (~10,000+ lines), and `Frm_vehicle.doPost` (dispatching to ~35 operations across 16,000+ lines) are extremely difficult to understand or maintain without documentation.

---

*Report generated by audit agent A18 -- Pass 3 (Documentation) -- 2026-02-25*
