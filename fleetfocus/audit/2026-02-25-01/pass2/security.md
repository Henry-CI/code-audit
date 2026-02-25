# Pass 2 -- Test Coverage: security package
**Agent:** A18
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Criteria | Status |
|---|---|
| Test directory present (`test/`, `src/test/`) | **NO** -- none found in entire repository |
| Test framework dependency (JUnit, TestNG) | **NO** -- no test framework dependencies |
| Test runner configuration (Maven Surefire, Gradle) | **NO** -- no build tool test configuration |
| Any `@Test` annotations in codebase | **NO** -- zero instances across all Java files |
| Mockito / mock framework | **NO** -- not present |
| Integration test infrastructure | **NO** -- not present |
| CI/CD test execution | **NO** -- not evident |

**Conclusion:** The repository has **ZERO automated tests** of any kind. Every class, method, code path, and error condition in the security package is **completely untested**. This is the highest-risk package in the application (authentication, authorization, password management, session management) and has zero coverage.

---

## Reading Evidence

### File 1: Databean_security.java

- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/security/Databean_security.java`
- **Class:** `public class Databean_security` (line 22) -- NOT a servlet; a data-access JavaBean used from JSP pages
- **No servlet mapping** -- instantiated directly from JSP via `<jsp:useBean>`
- **Fields:** `HttpServletRequest request`, `Connection conn`, `Statement stmt/stmt1/stmt2`, `ResultSet rset/rset1/rset2`, multiple String fields for codes, ArrayList fields for forms/modules (lines 24-67)
- **Lines:** ~1575

**Public methods (with signatures and line numbers):**

| Line | Signature |
|---|---|
| 127 | `public void clear_variables()` |
| 150 | `private void Fetch_report_nm()` |
| 198 | `private void Fetch_forms()` |
| 213 | `private void Fetch_modules()` |
| 228 | `private void Fetch_mail_groups()` |
| 281 | `private void Fetch_mail_conf()` |
| 377 | `private void Fetch_customer_info() throws SQLException` |
| 418 | `private void Fetch_monthly_mail_conf()` |
| 457 | `private String getClassURL(String emailurl)` |
| 469 | `private String getLoc_cd(String emailurl, String enity)` |
| 492 | `private void Fetch_mail_conf_rpt()` |
| 540 | `private void Fetch_mail_list()` |
| 557 | `private void Fetch_mail_cust()` |
| 570 | `private void Fetch_form_data()` |
| 587 | `private void Fetch_module_data()` |
| 603 | `private void Fetch_access_rights() throws SQLException` |
| 677 | `private void Fetch_notification_settings() throws SQLException` |
| 696 | `private void Fetch_groups()` |
| 714 | `private void Fetch_groups1() throws SQLException` |
| 760 | `private void fetchAccessRightsTemplate() throws SQLException` |
| 786 | `private void Fetch_group_customers1()` |
| 843 | `private void Fetch_login()` |
| 935 | `private void Fetch_BMS_login() throws SQLException` |
| 950 | `public void init()` -- **main entry point called from JSP** |
| 1093+ | ~50 public getters/setters for bean properties |

**Key observation (line 950):** `init()` is the main orchestrator called from JSP. It reads `set_op_code` and dispatches to various `Fetch_*` methods. The `Fetch_login()` (line 843) and `Fetch_BMS_login()` (line 935) methods deal with login/session data retrieval. `Fetch_access_rights()` (line 603) reads access permissions. All use string-concatenated SQL.

---

### File 2: Frm_login.java

- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java`
- **Class:** `public class Frm_login extends HttpServlet` (line 21)
- **Servlet mapping:** `/servlet/Frm_login` (web.xml line 44-45)
- **Lines:** 161

**Public/protected methods:**

| Line | Signature |
|---|---|
| 29 | `protected void doPost(HttpServletRequest request, HttpServletResponse res) throws ServletException, IOException` |
| 144 | `public static Connection CreateConnection() throws Exception` |
| 157 | `public static void closeConnection(final Connection conn) throws SQLException` |

**Security-critical code in doPost (lines 29-142):**
- Reads `login` and `password` from request parameters (lines 49-52)
- **SQL INJECTION:** Builds SQL by concatenating `login` directly: `"select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '" + login + "'"` (line 58-59)
- **SQL INJECTION:** Second query also concatenates `login`: `"select \"PASSWORD\",\"USER_CD\" from \"FMS_USR_MST\" where \"USER_NAME\" = '" + login + "'"` (lines 72-73)
- **PLAINTEXT PASSWORD COMPARISON:** `password.equals(pass_word)` (line 81) -- no hashing
- **PASSWORD LOGGING:** `log.info("login failed: login:" + login + " password:" + password + " database password:" + pass_word ...)` (lines 97-100) -- logs both user-entered and database-stored passwords in plaintext
- **USER_CD IN URL:** Passes `user_cd` in redirect URL query parameter (line 91)
- **NO SESSION VALIDATION:** No CSRF token, no rate limiting, no account lockout
- **SENSITIVE DATA LOGGING:** Logs the full query including username (line 60)

---

### File 3: Frm_security.java

- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
- **Class:** `public class Frm_security extends HttpServlet` (line 47)
- **Servlet mapping:** `/servlet/Frm_security` (web.xml line 31-32)
- **Lines:** ~4171
- **Imports:** BCrypt, ESAPI, RandomStringUtils (lines 29-32)

**All methods (with signatures and line numbers):**

| Line | Signature | Security Relevance |
|---|---|---|
| 57 | `protected void doPost(HttpServletRequest req, HttpServletResponse res)` | Main dispatcher -- 30+ operations |
| 66 | (within doPost) **LOGS PASSWORD IN PLAINTEXT** | `log.info(... +";password:"+req.getParameter("password")+";")` |
| 143 | `public void clearVectors()` | Empty method |
| 147 | `public static Connection CreateConnection() throws Exception` | DB connection factory |
| 159 | `public static void closeConnection(final Connection conn)` | |
| 164 | `private void save_form(...)` | SQL injection in form_nm, module_cd, path, desc |
| 258 | `public void saveDashboardSubscription(...)` | SQL injection in userCd, custCd, locCd |
| 335 | `public void deleteSubscription(...)` | SQL injection in subsId |
| 399 | `private void rrsubscribe(...)` | |
| 456 | `private void save_module(...)` | SQL injection |
| 547 | `private void sendAUEmail(...)` | |
| 570 | `private void mail_group_add(...)` | |
| 627 | `private void save_mail_group(...)` | SQL injection in grp_nm |
| 711 | `private void save_mail_group_pop(...)` | SQL injection |
| 793 | `private void save_mail_lst(...)` | SQL injection in mail_id, grp_cd |
| 857 | `private void del_mail_lst(...)` | SQL injection |
| 923 | `private void new_login(...)` | **AUTH**: Uses PreparedStatement, session management |
| 1244 | `private void reloadPermissions(...)` | Permission reload -- SQL injection in group_cd |
| 1391 | `private void chk_login(...)` | **PRIMARY AUTH**: BCrypt (non-AU), ESAPI normalization, lockout logic |
| 2169 | `public String generateRandomCharacters(int length)` | Password generation |
| 2176 | `private void reset_password(...)` | **SQL INJECTION in username** (lines 2196-2198), temp password emailed |
| 2283 | `private void expire_password(...)` | Expires temp passwords |
| 2335 | `private void change_password(...)` | **PLAINTEXT COMPARE for AU** (line 2367), SQL injection in user_cd (line 2359) |
| 2406 | `private void chg_bms_pass(...)` | **MD5 hashing via SQL** (line 2435), SQL injection in user_cd, cpass, npass |
| 2508 | `private void chg_pass(...)` | Plaintext password in SQL for AU (line 2547-2548) |
| 2639 | `private void save_perm(...)` | **AUTHORIZATION**: SQL injection in gp_cd, vform_cd, v_perm, etc. |
| 2723 | `private void save_notification_settings(...)` | |
| 2793 | `private void save_mail_conf(...)` | |
| 3003 | `private void del_mail_conf(...)` | |
| 3060 | `private void del_mail_conf_rpt(...)` | |
| 3116 | `private void mail_conf_dyn(...)` | |
| 3401 | `private void save_mail_conf_dyn(...)` | |
| 3583 | `private void del_mail_conf_dyn(...)` | |
| 3651 | `private void del_mail_monthly_conf(...)` | |
| 3703 | `private void save_mail_monthly_conf(...)` | |
| 3779 | `private void save_re_order_form(...)` | |
| 3851 | `private void del_subscription(...)` | |
| 3905 | `private void save_subscription(...)` | |
| 3958 | `private void save_national_subscription(...)` | |
| 4010 | `private String getLoc_cd(...)` | |
| 4032 | `private String getClassURL(...)` | |
| 4045 | `public boolean sendMail(...)` | Always returns true regardless of errors |
| 4083 | `private void saveShift(...)` | SQL injection in cust_cd |
| 4152 | `public static String esapiNormalizeParam(String string)` | Input sanitization |
| 4161 | `public static String esapiNormalizeUserNameParam(String string)` | Username sanitization |

**Key `chk_login` flow (lines 1391-2167):**
1. Reads `login` and `password` from request (lines 1417-1421)
2. ESAPI normalization applied (lines 1418, 1421)
3. Uses PreparedStatement for user lookup (line 1432-1433)
4. For non-AU sites: BCrypt password verification (line 1571)
5. For AU sites: plaintext comparison with ESAPI normalization (line 1585)
6. Account lockout after 5 failed attempts with 15-minute cooldown (lines 1525-1548)
7. Session attributes set: user_cd, access_level, access_cust, access_site, access_dept, permissions (lines 1890-1898)
8. **Still logs passwords on failed attempts** (line 2053)

---

### File 4: Frm_customer.java

- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_customer.java`
- **Class:** `public class Frm_customer extends HttpServlet` (line 47)
- **Servlet mapping:** `/servlet/Frm_customer` (web.xml line 83-84)
- **Lines:** ~12850+ (extremely large file, 511KB)
- **Instance fields (NOT thread-safe):** `private Connection dbcon`, `private Statement stmt`, `private ResultSet rset`, `private String message` (lines 49-57)

**Key methods (security-relevant):**

| Line | Signature | Security Relevance |
|---|---|---|
| 75 | `protected void doGet(...)` | 15+ dispatch operations, session-based access control |
| 1372 | `protected void doPost(...)` | 30+ dispatch operations |
| 1516 | `private String GetCanSettingsByVehicle(...)` | SQL injection in all params |
| 1536 | `private boolean GetCanbusByVehicle(String veh_cd)` | SQL injection |
| 2240 | `public boolean checkWeigand(...)` | |
| 2469 | `private void lock_unlock_start(...)` | SQL injection in veh_cd, lockout |
| 2508 | `private void add_new_user(...)` | User creation with many unsanitized params |
| 3560 | `private void change_password(...)` | BCrypt for non-AU, plaintext for AU, SQL injection in user_cd |
| 5162 | `private void copy_user(...)` | User copy |
| 6321 | `private void update_user(...)` | User update |
| 8163 | `private void delete_user(...)` | User deletion |
| 8394 | `private void recover_user(...)` | User recovery |
| 8599 | `private boolean isEmailValid(String email)` | Email validation |
| 8614 | `public boolean isValidEmailAddress(String email)` | Regex email validation |
| 8622 | `private void add_user(...)` | **HARDCODED PASSWORD "password"** (line 8672-8673) |
| 8687 | `private String get_username(String username)` | SQL injection in username |
| 8718 | `private void save_mastercodes(...)` | |
| 12006 | `public static Connection CreateConnection() throws Exception` | |
| 12018 | `public static void closeConnection(final Connection conn)` | |

**Thread-safety concern:** Connection, Statement, ResultSet, and message are all instance fields (lines 49-57). Since servlets are shared across threads, concurrent requests will corrupt these shared resources. This is a critical concurrency bug.

---

### File 5: Frm_vehicle.java

- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_vehicle.java`
- **Class:** `@MultipartConfig public class Frm_vehicle extends HttpServlet` (lines 56-57)
- **Servlet mapping:** `/servlet/Frm_vehicle` (web.xml line 70-71)
- **Lines:** ~16229+ (extremely large file, 615KB)
- **Instance fields (NOT thread-safe):** `private Connection dbcon`, `private Statement stmt`, `private ResultSet rset`, `private String message` (lines 59-66)

**Key methods:**

| Line | Signature | Security Relevance |
|---|---|---|
| 79 | `protected void doPost(...)` | 30+ dispatch operations |
| 237 | `private long parseServiceHour(String val)` | |
| 265 | `private void diagSyncThreshold(...)` | SQL injection in vehicle, threshold |
| 396 | `private void resetUnitMemory(...)` | SQL injection in vehicle |
| 492 | `private void spareSwap(...)` | |
| 710 | `private void locker(...)` | |
| 934 | `private void broadcast(...)` | |
| 1032 | `private void reboot(...)` | Device reboot command |
| 1111 | `private void save_idle_timer(...)` | |
| 1240 | `private void save_network_settings(...)` | |
| 3695 | `private void sendSMRemoteAccess(...)` | Supermaster remote access |
| 9296 | `private void saveSiteSetupConfig(...)` | |
| 9474 | `private void saveAccessRightsTemplate(...)` | |
| 10158 | `private void save_impact(...)` | |
| 13109 | `private void delete_vehicle(...)` | |
| 13161 | `private void dehire_vehicle(...)` | |
| 15147 | `private void save_firmware(...)` | Firmware upload |
| 15476 | `public static Connection CreateConnection() throws Exception` | |
| 15488 | `public static void closeConnection(final Connection conn)` | |

**Same thread-safety issue** as Frm_customer.java -- instance-level Connection/Statement/ResultSet fields.

---

### File 6: GetGenericData.java

- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/security/GetGenericData.java`
- **Class:** `public class GetGenericData extends HttpServlet` (line 19)
- **No servlet mapping found in web.xml** (may be unused or mapped elsewhere)
- **Lines:** 94
- **Instance fields (NOT thread-safe):** `Statement stmt`, `ResultSet rset`, `Connection dbcon`, `String queryString` (lines 22-26)

**Methods:**

| Line | Signature |
|---|---|
| 28 | `public GetGenericData()` -- empty constructor |
| 32 | `protected void doGet(...)` -- creates connection but does nothing with it |
| 67 | `private void getWeigand() throws SQLException` -- **INCOMPLETE SQL** (missing WHERE clause predicate, line 68) |
| 75 | `public static Connection CreateConnection() throws Exception` |
| 87 | `public static void closeConnection(final Connection conn)` |

**Observation:** This class appears to be a stub/incomplete implementation. The `getWeigand()` method is never called from `doGet()` and contains a broken SQL query (`select "CARD_ID" from "FMS_USR_MST" where` -- no condition).

---

## Findings

### A18-01 -- CRITICAL: Zero test coverage for entire security package (6 files, ~35,000+ lines)

**Severity:** CRITICAL
**Files:** All 6 files in `com.torrent.surat.fms6.security`
**Impact:** The security package handles authentication, authorization, password management, session management, user CRUD, vehicle management, and access control for the entire FleetFocus application. There are zero automated tests of any kind -- no unit tests, no integration tests, no security tests. This means:

- No regression safety net for any security-critical code changes
- No validation that authentication logic works correctly
- No verification that authorization checks prevent unauthorized access
- No tests for SQL injection prevention
- No tests for password hashing correctness
- No tests for session management
- No tests for account lockout behavior
- No tests for input validation

**Test cases that MUST exist:**

For **Frm_login.java** (161 lines, 0% coverage):
1. Successful login with valid credentials
2. Failed login with wrong password
3. Failed login with nonexistent user
4. SQL injection attempt in login field
5. Null/empty login parameter handling
6. Null/empty password parameter handling
7. Connection failure handling
8. Redirect URL correctness for success and failure paths

For **Frm_security.chk_login()** (~776 lines, 0% coverage):
1. Successful BCrypt password verification (non-AU)
2. Successful plaintext password verification (AU)
3. Account lockout after 5 failed attempts
4. Account lockout 15-minute expiry/reset
5. Forced password change (expired password policy)
6. Change password required (first login)
7. Reset password flow
8. Deactivated customer login denial
9. Access level 5 (no-access) denial
10. HAS_WEB_ACCESS=false denial
11. Session attribute population correctness
12. Permission matrix loading
13. Privacy policy acceptance flow
14. Release notes acceptance flow
15. ESAPI normalization of login/password inputs
16. BCrypt IllegalArgumentException fallback to plaintext comparison

For **Frm_security.change_password()** (lines 2335-2404):
1. Password change with correct current password
2. Password change with wrong current password
3. New password same as old password rejection
4. New password/confirm password mismatch
5. Empty user_cd handling
6. SQL injection in user_cd parameter

For **Frm_security.reset_password()** (lines 2176-2280):
1. Valid username reset
2. Valid email reset
3. Invalid/nonexistent username
4. Empty username
5. Temporary password generation and storage
6. Email sending on reset
7. SQL injection in username parameter

For **Frm_security.save_perm()** (lines 2639-2721):
1. Permission save with valid inputs
2. Permission delete/re-insert atomicity
3. Unauthorized permission modification attempt
4. SQL injection in group code, form codes, permission arrays

For **Frm_customer.change_password()** (lines 3560-3696):
1. BCrypt password change (non-AU)
2. Plaintext password change (AU)
3. Password history check (prevents reuse)
4. Reset password flow
5. Wrong current password
6. Password mismatch

For **Frm_customer.add_new_user()** (lines 2508-2668+):
1. Successful user creation with all fields
2. Missing required fields validation
3. Duplicate user handling
4. SQL injection in all input parameters
5. Card ID / Pin ID validation

For **Frm_customer.add_user()** (lines 8622-8685):
1. User creation with hardcoded "password"
2. Username generation collision handling
3. Input validation for customer/location/department

For **Frm_vehicle.doPost()** and all dispatch methods:
1. Each of 30+ operations needs basic happy path test
2. Authorization checks for each operation
3. SQL injection in vehicle parameters

For **Databean_security.init()** (line 950):
1. Each op_code dispatch path
2. Data retrieval for login, access rights, groups
3. SQL injection in op_code-derived parameters

For **GetGenericData.doGet()** (line 32):
1. Basic invocation
2. Broken getWeigand() SQL handling

---

### A18-02 -- CRITICAL: Password logging in plaintext (Frm_login.java line 97-99, Frm_security.java line 66, line 2053)

**Severity:** CRITICAL
**Files:**
- `Frm_login.java` line 97-99: `log.info("login failed: login:" + login + " password:" + password + " database password:" + pass_word ...)`
- `Frm_security.java` line 66: `log.info(... + ";password:" + req.getParameter("password") + ";")` -- logs every request's password
- `Frm_security.java` line 2053: `log.info("login failed: login:" + login + " password:" + password + " database password:" + pass_word ...)`

**Impact:** User-entered passwords AND database-stored passwords are written to application log files in cleartext. Anyone with log access can harvest all credentials. The line 66 occurrence in Frm_security.java logs EVERY doPost request's password regardless of the operation.

**Required tests:**
1. Verify that no passwords appear in log output after login attempts
2. Verify that log messages are sanitized for sensitive fields
3. Verify that database passwords are never included in any log output

---

### A18-03 -- CRITICAL: SQL injection in Frm_login.java authentication queries (lines 58-59, 72-73)

**Severity:** CRITICAL
**File:** `Frm_login.java`
**Lines:** 58-59, 72-73

**Code:**
```java
queryString = "select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '" + login + "'";
// and
queryString = "select \"PASSWORD\",\"USER_CD\" from \"FMS_USR_MST\" where \"USER_NAME\" = '" + login + "'";
```

**Impact:** The login parameter is concatenated directly into SQL without any sanitization or parameterization. An attacker can bypass authentication entirely with a payload like `' OR '1'='1' --`.

**Required tests:**
1. SQL injection payloads in login field are rejected or safely handled
2. Parameterized queries are used instead of string concatenation
3. Special characters in username do not cause SQL errors

---

### A18-04 -- CRITICAL: Plaintext password comparison in Frm_login.java (line 81)

**Severity:** CRITICAL
**File:** `Frm_login.java` line 81
**Code:** `if (password.equals(pass_word))`

**Impact:** Passwords are stored and compared in plaintext. This is the older login servlet; while `Frm_security.chk_login()` uses BCrypt for non-AU sites, this servlet performs no hashing at all.

**Required tests:**
1. Verify passwords are hashed before storage
2. Verify password comparison uses BCrypt or equivalent
3. Verify plaintext passwords are never stored in the database

---

### A18-05 -- CRITICAL: SQL injection in reset_password (Frm_security.java lines 2196-2198)

**Severity:** CRITICAL
**File:** `Frm_security.java` lines 2196-2198

**Code:**
```java
queryString = "select \"USER_CD\",\"EMAIL_ADDR\",\"USER_NAME\" from \"FMS_USR_MST\" where (\"USER_NAME\" = '" + username + "' or upper(\"EMAIL_ADDR\") = upper('"+username+"')) and ...";
```

**Impact:** The username parameter in password reset is concatenated directly into SQL. An attacker can exfiltrate data or modify the query to reset any user's password.

**Required tests:**
1. SQL injection payloads in username field for reset flow
2. Parameterized query usage verification
3. Rate limiting on reset requests (currently absent)

---

### A18-06 -- CRITICAL: Temporary password stored in plaintext (Frm_security.java lines 2227-2231)

**Severity:** CRITICAL
**File:** `Frm_security.java` lines 2227-2231

**Code:**
```java
queryString = "insert into user_reset_password (user_id, temp_pass, active, update_time) values ("+userId+",'" + pass + "', TRUE, now())";
// or
queryString = "update user_reset_password set temp_pass = '" + pass + "', active = TRUE, update_time = now() where user_id = "+ userId;
```

**Impact:** Temporary passwords are stored in plaintext in the `user_reset_password` table. SQL injection is also possible through `userId` (though it comes from DB, not user input directly).

**Required tests:**
1. Verify temp passwords are hashed before storage
2. Verify temp password expiry works correctly (2-hour window)
3. Verify temp password is invalidated after use

---

### A18-07 -- CRITICAL: MD5 hashing for BMS passwords via SQL (Frm_security.java lines 2435, 2448)

**Severity:** CRITICAL
**File:** `Frm_security.java` lines 2435, 2448

**Code:**
```java
queryString = "select \"BMS_PASSWORD\",md5('" + cpass + "') from \"FMS_USR_MST\" where \"USER_CD\" = '" + user_cd + "'";
queryString = "select md5('" + npass + "')";
```

**Impact:** BMS passwords are hashed with MD5 (weak/broken hash algorithm) and the hashing is done via SQL string concatenation, creating both a cryptographic weakness and SQL injection vulnerability. The raw password values (`cpass`, `npass`) are embedded in the SQL string.

**Required tests:**
1. Verify BMS passwords use a strong hashing algorithm (BCrypt, Argon2)
2. SQL injection in cpass, npass, user_cd, bmsuser parameters
3. Password comparison correctness

---

### A18-08 -- CRITICAL: Inconsistent password hashing (AU plaintext vs. non-AU BCrypt)

**Severity:** CRITICAL
**Files:** `Frm_security.java` (lines 1569-1586, 2367-2378), `Frm_customer.java` (lines 3586-3596, 3631-3633)

**Impact:** For AU and MLA sites, passwords are stored and compared in plaintext (with only single-quote escaping). For other sites, BCrypt is used. This means AU/MLA deployments have no password hashing protection. Additionally, the BCrypt `IllegalArgumentException` fallback (line 1572-1573) silently degrades to plaintext comparison, which could be exploited.

**Required tests:**
1. BCrypt verification for all non-AU logins
2. Behavior when BCrypt throws IllegalArgumentException
3. Password storage format verification per site configuration
4. Migration path from plaintext to hashed passwords for AU

---

### A18-09 -- CRITICAL: Thread-safety violations in Frm_customer.java and Frm_vehicle.java

**Severity:** CRITICAL
**Files:** `Frm_customer.java` (lines 49-57), `Frm_vehicle.java` (lines 59-66)

**Code (Frm_customer.java):**
```java
private Connection dbcon;
private String queryString;
private Statement stmt;
private ResultSet rset;
private Statement stmt1;
private ResultSet rset1;
private String message;
```

**Impact:** Servlets are singletons shared across all requests. Using instance fields for Connection, Statement, ResultSet, and message means concurrent requests will corrupt each other's database state, potentially returning one user's data to another user, causing data corruption, or creating authentication bypass scenarios.

**Required tests:**
1. Concurrent request handling (multiple threads calling doPost simultaneously)
2. Verify no cross-request data leakage
3. Verify connection/statement isolation between requests

---

### A18-10 -- CRITICAL: SQL injection pervasive across Frm_security.java (30+ methods)

**Severity:** CRITICAL
**File:** `Frm_security.java`

**Affected methods (non-exhaustive list with string-concatenated SQL):**
- `save_form()` -- form_nm, module_cd, path, desc (lines 201-213, 216-220)
- `save_module()` -- module_nm, path, desc (lines 493-500, 502-510)
- `save_mail_group()` -- grp_nm (lines 661-662, 665-666)
- `save_mail_group_pop()` -- grp_nm, usr (lines 743-750, 753-755)
- `save_mail_lst()` -- grp_cd, mail_id (lines 809-810, 818-819)
- `del_mail_lst()` -- grp_cd, mail_id (lines 873-874, 880-881)
- `saveDashboardSubscription()` -- userCd, custCd, locCd (lines 281, 291, 297)
- `deleteSubscription()` -- subsId (line 362)
- `save_perm()` -- gp_cd, vform_cd[], v_perm[], e_perm[], d_perm[], p_perm[], user_cd (lines 2665-2683)
- `saveShift()` -- cust_cd, shift values (lines 4108, 4115, 4117)
- `change_password()` -- user_cd (line 2359, 2377)
- `chg_pass()` -- user_cd, normalizePswd (lines 2528, 2547-2548, 2589-2590)
- `reloadPermissions()` -- group_cd in string concatenation (line 1307)

**Impact:** Nearly every data-modification method builds SQL through string concatenation with user-supplied input. This creates widespread SQL injection vulnerabilities throughout the security administration interface.

**Required tests:** Each method needs SQL injection tests for every user-supplied parameter.

---

### A18-11 -- CRITICAL: SQL injection pervasive across Frm_customer.java

**Severity:** CRITICAL
**File:** `Frm_customer.java`

**Affected methods (examples):**
- `GetCanSettingsByVehicle()` -- veh_type_cd, cust_cd, loc_cd, dep_cd (line 1525)
- `GetCanbusByVehicle()` -- veh_cd (line 1540)
- `lock_unlock_start()` -- veh_cd, lockout (lines 2478, 2487, 2493)
- `add_user()` -- fname, lname, customer, location, department, User_Name (lines 8672-8673, 8676-8677, 8679-8681)
- `get_username()` -- username (line 8691, 8701)
- `Query_Customer_Relations()` -- Group concatenated into SQL (line 1645)
- `save_mastercodes()` -- vehicle_cd, user_cd[] (lines 8740, 8745)

**Required tests:** Each method needs SQL injection tests for every user-supplied parameter.

---

### A18-12 -- CRITICAL: SQL injection pervasive across Frm_vehicle.java

**Severity:** CRITICAL
**File:** `Frm_vehicle.java`

**Affected methods (examples):**
- `diagSyncThreshold()` -- vehicle, threshold (lines 291, 345-346)
- `resetUnitMemory()` -- vehicle (line 407, 415)
- All `broadcast()`, `reboot()`, `locker()` methods -- vehicle parameters
- Nearly every private method uses string concatenation for SQL

**Required tests:** Each of the 40+ methods needs SQL injection testing.

---

### A18-13 -- HIGH: Hardcoded default password "password" in add_user (Frm_customer.java line 8672-8673)

**Severity:** HIGH
**File:** `Frm_customer.java` line 8672-8673

**Code:**
```java
queryString="Insert into \"FMS_USR_MST\" (\"USER_CD\",\"USER_NAME\",\"ACTIVE\",\"CONTACT_FIRST_NAME\",\"CONTACT_LAST_NAME\",\"PASSWORD\") " +
    "values ('"+User_Cd+"','"+User_Name+"',"+status+",'"+fname+"','"+lname+"','password')";
```

**Impact:** New users are created with the plaintext password "password". There is no forced password change requirement visible in this method. Combined with the plaintext storage issue, this means all new users have a known, guessable password.

**Required tests:**
1. Verify new users must change password on first login
2. Verify default password is not used in production
3. Verify password is hashed before storage

---

### A18-14 -- HIGH: No authorization checks in doPost dispatchers

**Severity:** HIGH
**Files:** `Frm_security.java` (line 57), `Frm_customer.java` (lines 75, 1372), `Frm_vehicle.java` (line 79)

**Impact:** The `doPost()` methods dispatch to security-critical operations (save_perm, change_password, delete_user, reset_password, reboot, etc.) without first verifying that the caller has a valid authenticated session or the appropriate access level. Any unauthenticated request can invoke any operation by crafting the appropriate `op_code` or `method` parameter.

**Required tests:**
1. Unauthenticated access to each operation is denied
2. Users without admin access level cannot invoke admin-only operations
3. Session validation occurs before any operation dispatch

---

### A18-15 -- HIGH: Broken/incomplete GetGenericData.java (line 67-68)

**Severity:** HIGH
**File:** `GetGenericData.java` lines 67-73

**Code:**
```java
private void getWeigand() throws SQLException{
    queryString = "select \"CARD_ID\" from \"FMS_USR_MST\" where";
    rset = stmt.executeQuery(queryString);
```

**Impact:** The SQL query is syntactically invalid (no WHERE predicate). The method is never called from `doGet()`, and `doGet()` creates a connection but performs no operations. This appears to be dead/abandoned code that should be removed. If ever activated, the broken SQL would cause runtime errors, and the lack of a WHERE clause would return ALL card IDs.

**Required tests:**
1. Verify this class is not mapped/reachable
2. If reachable, verify doGet returns appropriate response
3. Verify getWeigand has valid SQL if ever used

---

### A18-16 -- HIGH: sendMail always returns true (Frm_security.java lines 4045-4081)

**Severity:** HIGH
**File:** `Frm_security.java` lines 4045-4081

**Impact:** The `sendMail()` method catches all exceptions internally (including `Throwable`) and always returns `true`, regardless of whether the email was actually sent. This means callers cannot distinguish between successful and failed email delivery, which is critical for password reset notifications.

**Required tests:**
1. Verify return value reflects actual send success/failure
2. Verify exception handling does not silently swallow errors
3. Verify password reset email delivery is confirmed

---

### A18-17 -- MEDIUM: Databean_security uses string-concatenated SQL throughout

**Severity:** MEDIUM (lower because bean is not directly internet-facing, but still exploitable via JSP parameter injection)
**File:** `Databean_security.java`

**Impact:** All `Fetch_*` methods use string concatenation with values derived from `set_*` fields that are populated from JSP page parameters. While not directly a servlet, if JSP pages pass unsanitized user input to the bean's setter methods, SQL injection is possible.

**Required tests:**
1. Each Fetch method with malicious input values
2. Input sanitization at the JSP/bean boundary

---

### A18-18 -- MEDIUM: Instance-level thread-safety issue in GetGenericData.java

**Severity:** MEDIUM
**File:** `GetGenericData.java` lines 22-26

**Impact:** Same pattern as Frm_customer and Frm_vehicle -- instance-level Connection, Statement, ResultSet, and queryString fields in a servlet. Although the servlet currently does nothing meaningful, if it is ever completed, this would be a concurrency issue.

**Required tests:**
1. Concurrent access to doGet
2. Verify no shared mutable state

---

## Summary

| Severity | Count | Description |
|---|---|---|
| CRITICAL | 12 | Zero test coverage, password logging, SQL injection (authentication, reset, password change, pervasive across 3 servlets), plaintext passwords, thread-safety, MD5 hashing, inconsistent hashing |
| HIGH | 4 | Hardcoded password, no authorization checks, broken code, silent email failure |
| MEDIUM | 2 | Bean SQL injection, GetGenericData thread-safety |
| **Total** | **18** | |

**Overall assessment:** The security package is the most critical code in the FleetFocus application and has absolutely zero test coverage. The code contains numerous severe security vulnerabilities (SQL injection, plaintext password storage, credential logging) that would be detectable by even basic security-focused tests. The complete absence of tests means these vulnerabilities have never been systematically validated or caught through automated means. This represents the highest possible risk level for a production security codebase.
