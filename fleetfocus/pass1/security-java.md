# Security Audit — Java Security Package
**Audit ID:** 2026-02-25-01
**Agent:** A03
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/security/`

---

## STEP 3 — FILE INVENTORY AND READING EVIDENCE

### File 1: `Frm_login.java`
**Fully qualified class name:** `com.torrent.surat.fms6.security.Frm_login`

**Imports (no wildcard imports):**
- `java.io.IOException`
- `java.sql.Connection`
- `java.sql.ResultSet`
- `java.sql.SQLException`
- `java.sql.Statement`
- `javax.naming.Context`
- `javax.naming.InitialContext`
- `javax.servlet.ServletException`
- `javax.servlet.http.HttpServlet`
- `javax.servlet.http.HttpServletRequest`
- `javax.servlet.http.HttpServletResponse`
- `javax.sql.DataSource`
- `org.apache.logging.log4j.Logger`
- `com.torrent.surat.fms6.util.RuntimeConf`

**Class annotations:** None (`@WebServlet` absent — mapped via web.xml or equivalent)

**Fields:**
- `private static final long serialVersionUID = 1L`
- `private static Logger log`

**Methods:**
| Return | Name | Parameter Types | Line |
|--------|------|----------------|------|
| `void` | `doPost` | `HttpServletRequest, HttpServletResponse` | 29 |
| `public static Connection` | `CreateConnection` | (none) | 144 |
| `public static void` | `closeConnection` | `Connection` | 157 |

**Method annotations:** None

---

### File 2: `GetGenericData.java`
**Fully qualified class name:** `com.torrent.surat.fms6.security.GetGenericData`

**Imports (no wildcard imports):**
- `java.io.IOException`
- `java.sql.Connection`, `ResultSet`, `SQLException`, `Statement`
- `javax.naming.Context`, `InitialContext`
- `javax.servlet.ServletException`
- `javax.servlet.http.HttpServlet`, `HttpServletRequest`, `HttpServletResponse`
- `javax.sql.DataSource`
- `com.torrent.surat.fms6.util.RuntimeConf`

**Class annotations:** None

**Fields (instance-level — shared across requests):**
- `String url`
- `String message`
- `Statement stmt`
- `ResultSet rset`
- `Connection dbcon`
- `private String queryString`

**Methods:**
| Return | Name | Parameter Types | Line |
|--------|------|----------------|------|
| (constructor) | `GetGenericData` | (none) | 28 |
| `void` | `doGet` | `HttpServletRequest, HttpServletResponse` | 32 |
| `private void` | `getWeigand` | (none) | 67 |
| `public static Connection` | `CreateConnection` | (none) | 75 |
| `public static void` | `closeConnection` | `Connection` | 87 |

---

### File 3: `Databean_security.java`
**Fully qualified class name:** `com.torrent.surat.fms6.security.Databean_security`

**Imports (no wildcard imports):**
- `java.sql.Connection`, `ResultSet`, `SQLException`, `Statement`
- `java.util.ArrayList`
- `javax.naming.Context`, `InitialContext`
- `javax.servlet.http.HttpServletRequest`
- `javax.sql.DataSource`
- `com.torrent.surat.fms6.bean.NotificationSettingsBean`
- `com.torrent.surat.fms6.util.LindeConfig`
- `com.torrent.surat.fms6.util.RuntimeConf`

**Class annotations:** None
**Note:** Not a servlet; data-access helper class.

**Fields (all package-private/default access):**
- `HttpServletRequest request`
- `Connection conn`
- `Statement stmt`, `stmt1`, `stmt2`
- `ResultSet rset`, `rset1`, `rset2`
- Multiple `String` fields (methodName, query, queryString, set_op_code, set_form_cd, set_module_cd, set_gp_cd, set_mail_grp_cd, set_user_cd, set_cust_cd, set_div_cd, set_loc_cd, set_dept_cd, etc.)
- Multiple `ArrayList` fields (raw, unparameterized)
- `String bms_user`, `String bms_pass`

**Notable:** Contains a field `String bms_pass` (BMS password, discussed in findings).

---

### File 4: `Frm_customer.java`
**Fully qualified class name:** `com.torrent.surat.fms6.security.Frm_customer`

**Imports (no wildcard imports):**
- `java.io.*`, `java.sql.*`, `java.text.*`, `java.util.*`
- `javax.mail.*`, `javax.naming.*`, `javax.servlet.*`, `javax.sql.*`
- `org.apache.logging.log4j.Logger`
- `org.mindrot.jbcrypt.BCrypt`
- `com.torrent.surat.fms6.*` (various beans and utilities)

**Class annotations:** `@MultipartConfig` is absent; `@SuppressWarnings("deprecation")` commented out

**Fields (instance-level — shared across requests due to lack of `SingleThreadModel`):**
- `private Connection dbcon`
- `private String queryString`
- `private Statement stmt`, `stmt1`
- `private ResultSet rset`, `rset1`
- `private String message`, `debug`
- `String VSite_Name`, `S_Access_level`, `S_Access_cust`, `S_Access_site`, `S_Access_dept`

**Methods (security-relevant):**
- `protected void doGet(HttpServletRequest, HttpServletResponse)` — line 75
- `private void Query_Customer_Relations(...)` — (internal)

---

### File 5: `Frm_security.java`
**Fully qualified class name:** `com.torrent.surat.fms6.security.Frm_security`

**Imports (no wildcard imports):**
- `java.io.IOException`, `java.net.URLEncoder`, `java.sql.*`, `java.text.*`, `java.util.*`
- `javax.mail.*`, `javax.naming.*`, `javax.servlet.*`, `javax.sql.*`
- `org.apache.commons.lang.RandomStringUtils`
- `org.apache.logging.log4j.Logger`
- `org.mindrot.jbcrypt.BCrypt`  ← PRESENT
- `org.owasp.esapi.ESAPI`  ← PRESENT
- Various internal beans and utilities

**Class annotations:** None (`@SuppressWarnings("deprecation")` commented out)

**Fields:**
- `private static final long serialVersionUID = 1L`
- `private static Logger log`
- `DecimalFormat df`

**Key methods (security-relevant):**
| Return | Name | Line |
|--------|------|------|
| `void` | `doPost` | 57 |
| `void` | `clearVectors` | 143 |
| `public static Connection` | `CreateConnection` | 147 |
| `public static void` | `closeConnection` | 159 |
| `private void` | `chk_login` | 1391 |
| `private void` | `reset_password` | 2176 |
| `private void` | `expire_password` | ~2260 |
| `private void` | `change_password` | 2335 |
| `private void` | `chg_bms_pass` | 2406 |
| `public String` | `generateRandomCharacters` | 2169 |
| `public static String` | `esapiNormalizeParam` | 4152 |
| `public static String` | `esapiNormalizeUserNameParam` | 4161 |

---

### File 6: `Frm_vehicle.java`
**Fully qualified class name:** `com.torrent.surat.fms6.security.Frm_vehicle`

**Imports (no wildcard imports):**
- `java.io.*`, `java.net.*`, `java.sql.*`, `java.text.*`, `java.time.*`, `java.util.*`
- `javax.naming.*`, `javax.servlet.*` (including `@MultipartConfig`), `javax.sql.*`
- `org.apache.logging.log4j.Logger`
- `com.google.gson.Gson`
- Internal beans and repositories

**Class annotations:** `@MultipartConfig` (line 56)

**Fields (instance-level — shared across requests):**
- `private Connection dbcon`
- `private String queryString`
- `private Statement stmt`, `stmt1`
- `private ResultSet rset`, `rset1`
- `private String message`
- `private FmsChklistLangSettingRepo fmsChklistLangSettingRepo`

**Methods:**
- `protected void doPost(HttpServletRequest, HttpServletResponse)` — line 79
- (Many private business-logic methods dispatched from `doPost`)

---

## STEP 4 — SECURITY REVIEW

### Authentication

- **`Frm_login.java` (legacy):** Login queries use raw string concatenation into SQL. Password is retrieved from DB in plaintext and compared with `password.equals(pass_word)`. No bcrypt. No session fixation protection. This class appears to be a legacy/unused servlet path.

- **`Frm_security.java` `chk_login` (primary path):** Uses `PreparedStatement` with `?` for the username count query and for the credential fetch. BCrypt is used via `BCrypt.checkpw(password, pass_word)` for non-AU/MLA sites. AU/MLA compares with `password.equals(esapiNormalizeParam(pass_word))` — plaintext comparison. Brute-force protection via `fms_user_actions` table (5-attempt lockout, 15-minute window). Session attributes are set but session is NOT invalidated/rotated prior to setting them. `request.getSession(true)` is called AFTER setting attributes (line 1946), which does not create a new session if one already exists — it returns the existing session.

---

## STEP 5 — FINDINGS

---

### A03-1
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java`
**Lines:** 58–59, 72–73
**Severity:** CRITICAL
**Category:** SQL Injection

**Description:**
The `doPost` method in `Frm_login.java` constructs both SQL queries by directly concatenating the `login` parameter (taken from the HTTP request with no sanitisation) into the query string. An attacker can inject arbitrary SQL, bypassing authentication or extracting data from the database.

**Evidence:**
```java
// Line 58-59
queryString = "select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '"
        + login + "'";

// Line 72-73
queryString = "select \"PASSWORD\",\"USER_CD\" from \"FMS_USR_MST\" where \"USER_NAME\" = '"
        + login + "'";
```

**Recommendation:**
Replace `Statement` with `PreparedStatement` and bind the `login` parameter with `ps.setString(1, login)` — exactly as is already done in `Frm_security.java:chk_login`. If `Frm_login.java` is no longer in active use, it should be deleted from the codebase rather than left as a reachable servlet. Confirm whether this servlet is mapped in `web.xml`.

---

### A03-2
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java`
**Lines:** 78–81
**Severity:** CRITICAL
**Category:** Plaintext Password Storage / Insufficient Hashing

**Description:**
The legacy `Frm_login.java` servlet retrieves the password from the database and compares it using a plain `.equals()` string comparison (`password.equals(pass_word)`). This implies either the database stores passwords in plaintext, or that the legacy servlet bypasses the bcrypt-hashed path used in `Frm_security.java`. In either case this path is not timing-safe and exposes plaintext or weakly-hashed credentials.

**Evidence:**
```java
// Line 78-81
pass_word = rset.getString(1);
user_cd = rset.getString(2);
...
if (password.equals(pass_word)) {
```

**Recommendation:**
If this servlet is still reachable, migrate it to use `BCrypt.checkpw()` as in `Frm_security.java`. If it is dead code, remove it entirely. Ensure the database does not store any passwords in plaintext.

---

### A03-3
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java`
**Lines:** 97–100
**Severity:** HIGH
**Category:** Sensitive Data Exposure via Logging

**Description:**
On a failed login, `Frm_login.java` logs both the submitted password and the password retrieved from the database in cleartext to the application log. Any party with access to log files (including log aggregation systems, support staff, or an attacker who has read access to logs) can harvest credentials.

**Evidence:**
```java
// Lines 97-100
log.info("login failed: login:" + login + " password:"
        + password + " database password:" + pass_word
        + ",ip:" + request.getRemoteAddr() + ",session:"
        + request.getSession().getId());
```

**Recommendation:**
Never log passwords or password hashes. Replace the log line with one that records only the username and failure reason, omitting both `password` and `pass_word`.

---

### A03-4
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Line:** 66
**Severity:** HIGH
**Category:** Sensitive Data Exposure via Logging

**Description:**
The `doPost` dispatcher in `Frm_security.java` unconditionally logs the raw value of the `password` request parameter at INFO level on every request, before any processing. This means every login attempt — whether successful or failed — writes the submitted plaintext password into the application log.

**Evidence:**
```java
// Line 66
log.info("New website requested op_code:" + req.getParameter("op_code")
    + ",form_cd:" + req.getParameter("form_cd")
    + ",ip:" + req.getRemoteAddr()
    + ",session:" + req.getSession().getId()
    + ",login:" + req.getParameter("login")
    + ";password:" + req.getParameter("password") + ";");
```

**Recommendation:**
Remove `;password:` and the associated `req.getParameter("password")` from this log statement. Audit all other log statements in the file for similar patterns.

---

### A03-5
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Line:** 2053
**Severity:** HIGH
**Category:** Sensitive Data Exposure via Logging

**Description:**
On a failed login, `Frm_security.java:chk_login` also logs both the submitted password and the database password hash/value in cleartext at INFO level.

**Evidence:**
```java
// Line 2053
log.info("login failed: login:" + login + " password:" + password
    + " database password:" + pass_word
    + ",ip:" + request.getRemoteAddr()
    + ",session:" + request.getSession().getId());
```

**Recommendation:**
Remove `password` and `pass_word` from this log statement. Log only the username, failure event type, IP, and session ID.

---

### A03-6
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 1167–1175, 1890–1898, 1946
**Severity:** HIGH
**Category:** Session Fixation

**Description:**
After a successful login, session attributes (including `user_cd`, `access_level`, permission matrices) are set on the **pre-existing** session object obtained by `request.getSession()`. The call to `request.getSession(true)` on line 1946 occurs **after** the attributes have already been written to the session, and `getSession(true)` only creates a new session if one does not already exist — if a session already exists, it returns the existing one unchanged. This means the session ID is never invalidated and re-issued on privilege escalation, leaving the application vulnerable to session fixation attacks: an attacker can plant a known session ID (e.g., via a network intercept) and after the victim authenticates, the attacker inherits the authenticated session.

**Evidence:**
```java
// Lines 1167–1175 (change_pass == true branch)
request.getSession().setAttribute("user_cd", user_cd);
request.getSession().setAttribute("access_level", access_level);
request.getSession().setAttribute("access_cust", DataUtil.removeDuplicateCds(access_cust));
// ...
request.getSession(true);  // line 1192 — too late; does not invalidate existing session

// Lines 1890–1898 (normal login branch)
request.getSession().setAttribute("user_cd", user_cd);
// ...
request.getSession(true);  // line 1946 — same problem
```

**Recommendation:**
Implement proper session fixation protection. Before setting any session attributes after successful authentication:
1. Copy any required pre-auth session values.
2. Call `request.getSession().invalidate()` to destroy the existing session.
3. Call `request.getSession(true)` to create a brand-new session with a new session ID.
4. Set all attributes on the new session.

---

### A03-7
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 1496–1505
**Severity:** HIGH
**Category:** SQL Injection (in temporary password lookup during login)

**Description:**
Inside `chk_login`, after the user record is fetched using a safe `PreparedStatement`, there is a fallback query to `user_reset_password` that concatenates `user_cd` (a string sourced from the database result set) directly into the SQL. Although `user_cd` originates from the database rather than directly from user input, the value ultimately traces back to the authenticated username lookup and should still be bound via a prepared statement to prevent second-order injection. More critically, this pattern is inconsistent and introduces risk if the data-origin assumption ever changes.

**Evidence:**
```java
// Lines 1496–1497
queryString = "select temp_pass from user_reset_password where user_id =  "
    + user_cd + " and active is true";
rset = stmt.executeQuery(queryString);
```

**Recommendation:**
Use a `PreparedStatement` with `ps.setInt(1, Integer.parseInt(user_cd))` — consistent with the surrounding code which already uses this pattern for the same `user_cd` value.

---

### A03-8
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 2196–2199
**Severity:** HIGH
**Category:** SQL Injection (in reset_password)

**Description:**
The `reset_password` method builds the user-lookup query by concatenating the `username` request parameter directly into the SQL string. Although the AU branch only concatenates the email, the non-AU branch concatenates both `username` and the email into the query without parameterisation.

**Evidence:**
```java
// Lines 2196–2199
if(LindeConfig.siteName.equalsIgnoreCase("AU")) {
    queryString = "select \"USER_CD\",\"EMAIL_ADDR\",\"USER_NAME\" from \"FMS_USR_MST\" "
        + "where upper(\"EMAIL_ADDR\") = upper('" + username + "') ...";
} else {
    queryString = "select \"USER_CD\",\"EMAIL_ADDR\",\"USER_NAME\" from \"FMS_USR_MST\" "
        + "where (\"USER_NAME\" = '" + username + "' or upper(\"EMAIL_ADDR\") = upper('"
        + username + "')) ...";
}
rset = stmt.executeQuery(queryString);
```

**Recommendation:**
Convert to `PreparedStatement` with bound parameters for both `USER_NAME` and `EMAIL_ADDR` predicates.

---

### A03-9
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 2226–2231
**Severity:** HIGH
**Category:** SQL Injection (in reset_password — temp password insert/update)

**Description:**
The `reset_password` method inserts and updates the `user_reset_password` table by concatenating `userId` (an integer, lower risk but still incorrect practice) and `pass` (a randomly generated temporary password string) directly into SQL strings. While `pass` is generated internally, the insert/update is not parameterised, making the code fragile and potentially injectable if the generation logic changes.

**Evidence:**
```java
// Lines 2226–2231
queryString = "insert into user_reset_password (user_id, temp_pass, active, update_time) "
    + "values (" + userId + ",'" + pass + "', TRUE, now())";
stmt.executeUpdate(queryString);
// and:
queryString = "update user_reset_password set temp_pass = '" + pass
    + "', active = TRUE, update_time = now() where user_id = " + userId;
stmt.executeUpdate(queryString);
```

**Recommendation:**
Use `PreparedStatement` with bound parameters for all insert/update operations.

---

### A03-10
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 2359–2378
**Severity:** HIGH
**Category:** SQL Injection + Insecure Password Storage (change_password for AU/MLA)

**Description:**
The `change_password` method retrieves the stored password with `USER_CD` concatenated directly into SQL, and updates the password using string concatenation with only a quote-doubling escape (`npass.replace("'", "''")`). This is not a parameterised query. Quote-doubling is not a reliable SQL injection defence (it is bypassable in some encoding scenarios), and no bcrypt hashing is applied — the new password is stored in plaintext. Additionally, `user_cd` is taken from the HTTP request parameter, meaning an authenticated user could supply a different `user_cd` to change another user's password.

**Evidence:**
```java
// Lines 2359–2360
queryString = "select \"PASSWORD\" from \"FMS_USR_MST\" where \"USER_CD\" = '" + user_cd + "'";
rset = stmt.executeQuery(queryString);

// Lines 2375–2378
String normalizePswd = npass.replace("'", "''");
queryString = "update \"FMS_USR_MST\" set \"PASSWORD\" = '" + normalizePswd
    + "', \"CHANGEPASSWORD\" = TRUE where \"USER_CD\" = '" + user_cd + "'";
stmt.executeUpdate(queryString);
```

**Recommendation:**
(1) Use `PreparedStatement` for all queries. (2) Hash the new password with BCrypt before storage — as the rest of the non-AU/MLA code does. (3) Source `user_cd` from the authenticated session (`request.getSession().getAttribute("user_cd")`) rather than from the request parameter to prevent horizontal privilege escalation.

---

### A03-11
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 2435–2458
**Severity:** HIGH
**Category:** SQL Injection + MD5 Password Hashing (chg_bms_pass)

**Description:**
`chg_bms_pass` uses MD5 (via the PostgreSQL `md5()` function called inside a concatenated SQL string) to hash the BMS password. MD5 is cryptographically broken and unsuitable for password storage. Additionally, `user_cd` and `cpass` are concatenated directly into the SQL string, creating SQL injection vectors. `bmsuser` is also concatenated into the UPDATE statement.

**Evidence:**
```java
// Lines 2435–2437
queryString = "select \"BMS_PASSWORD\",md5('" + cpass + "') "
    + "from \"FMS_USR_MST\" "
    + "where \"USER_CD\" = '" + user_cd + "'";

// Lines 2455–2459
queryString = "update \"FMS_USR_MST\" "
    + "set \"BMS_PASSWORD\" = '" + md5_password + "',"
    + "\"BMS_USERNAME\" = '" + bmsuser + "' "
    + "where \"USER_CD\" = '" + user_cd + "'";
```

**Recommendation:**
(1) Replace MD5 with BCrypt for BMS password hashing. (2) Use `PreparedStatement` for all queries. (3) Source `user_cd` from the session, not the request.

---

### A03-12
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 1583–1586
**Severity:** HIGH
**Category:** Plaintext Password Comparison (AU/MLA sites)

**Description:**
For Linde AU and MLA deployments, the password check in `chk_login` uses a plain `.equals()` comparison after ESAPI HTML-encoding of both the submitted password and the stored password. This implies AU/MLA passwords are stored in plaintext (or encoded but not hashed) in the database. There is no timing-safe comparison and no bcrypt.

**Evidence:**
```java
// Lines 1583–1586
} else {
    // Apply ESAPI for Linde AU password check
    matched = password.equals(esapiNormalizeParam(pass_word));
}
```

**Recommendation:**
Migrate AU/MLA password storage to BCrypt. Run a one-time migration to hash existing passwords, and update the comparison to `BCrypt.checkpw()`. ESAPI HTML-encoding is not a substitute for password hashing.

---

### A03-13
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 1600, 1974, 1203
**Severity:** MEDIUM
**Category:** Sensitive Data Exposure — `user_cd` in URL

**Description:**
After a successful login where a password change is required, the server responds with a redirect URL that includes the numeric `user_cd` as a plain query parameter (e.g., `../pages/changepass.jsp?user_cd=42`). This exposes the internal user ID in browser history, server access logs, and HTTP `Referer` headers.

**Evidence:**
```java
// Line 1600
message = "{ \"status\" : \"success_popup\", \"message\" : \"Sucessfully Login!\", "
    + "\"value\" :\"../pages/changepass.jsp?user_cd=" + user_cd
    + "&force_change=Y&lastUpdate=..." + "\" }";

// Line 1974
String url = "../pages/changepass.jsp?user_cd=" + user_cd + "&reset_pass=" + reset_pass;

// Line 1203
message = "{ ... \"value\" :\"../pages/changepass.jsp?user_cd=" + user_cd + "\" }";
```

**Recommendation:**
Store `user_cd` in the session after the authentication check and have `changepass.jsp` retrieve it from the session. Do not pass `user_cd` as a URL parameter.

---

### A03-14
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 2347, 2420, 2520
**Severity:** MEDIUM
**Category:** Broken Access Control — `user_cd` Taken from Request in Password Change

**Description:**
`change_password`, `chg_bms_pass`, and `chg_pass` all accept `user_cd` as an HTTP request parameter and use it directly to identify which user's password to change. An authenticated user can pass a different `user_cd` to change another user's password without further authorisation checks.

**Evidence:**
```java
// Line 2347 (change_password)
String user_cd = request.getParameter("user_cd") == null ? "" : request.getParameter("user_cd");

// Line 2420 (chg_bms_pass)
String user_cd = request.getParameter("user_cd") == null ? "" : request.getParameter("user_cd");
```

**Recommendation:**
Source `user_cd` from `request.getSession().getAttribute("user_cd")` rather than from the request parameter. Alternatively, verify that the supplied `user_cd` matches the session user before performing the update.

---

### A03-15
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/GetGenericData.java`
**Lines:** 21–26
**Severity:** MEDIUM
**Category:** Instance-Variable State Shared Across Concurrent Requests (Thread Safety)

**Description:**
`GetGenericData` extends `HttpServlet` but declares `Connection`, `Statement`, `ResultSet`, and other state as instance fields (not local variables). The servlet container creates one servlet instance shared across all concurrent requests. This means concurrent requests race on the same `dbcon`, `stmt`, `rset`, and `queryString` fields, causing potential data leakage between users and unpredictable query behaviour. The same pattern exists in `Frm_customer.java` and `Frm_vehicle.java`.

**Evidence:**
```java
// Lines 21–26 (GetGenericData.java)
String url = "";
String message = "";
Statement stmt = null;
ResultSet rset = null;
Connection dbcon = null;
private String queryString = "";
```

**Recommendation:**
Declare all `Connection`, `Statement`, `ResultSet`, and query-state variables as local variables within the handler methods, not as instance fields. This is the pattern already used correctly in `Frm_security.java:chk_login`.

---

### A03-16
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java`
**Lines:** 29–141 (entire `doPost`)
**Severity:** MEDIUM
**Category:** No Session Fixation Protection; No Brute-Force Protection; No CSRF

**Description:**
`Frm_login.java` has no session fixation protection, no failed-attempt tracking, no account lockout, and no CSRF token validation. The primary login path (`Frm_security.java:chk_login`) has all of these, but if `Frm_login.java` is reachable, attackers can use it as an alternative unauthenticated endpoint that bypasses all those controls.

**Evidence:**
```java
// After successful login in Frm_login.java — lines 82–83
request.getSession().setAttribute("sessionUsrCd", login);
message = "Login Successful";
// No invalidate(), no getSession(true), no fail counter, no CSRF check
```

**Recommendation:**
If `Frm_login.java` is not in use, remove its servlet mapping from `web.xml` and delete the file. If it is still used, apply the same protections as `Frm_security.java:chk_login`.

---

### A03-17
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 1417–1421
**Severity:** LOW
**Category:** ESAPI HTML-Encoding Applied to Password Before BCrypt

**Description:**
The submitted `password` parameter is passed through `esapiNormalizeParam()`, which applies `ESAPI.encoder().encodeForHTML()` (HTML-entity encoding), before being passed to `BCrypt.checkpw()`. This means that if a user's password contains HTML-special characters (e.g., `<`, `>`, `&`, `"`), the encoded form (e.g., `&lt;`) is what gets bcrypt-compared against the stored hash. This is inconsistent: if the password was stored using the raw value, authentication will fail for such users. If the password was stored using the encoded form, this is an artificial restriction on password character space that weakens security marginally.

**Evidence:**
```java
// Lines 1420–1421
String password = request.getParameter("password") == null ? "" : request.getParameter("password");
password = esapiNormalizeParam(password);
```

**Recommendation:**
Do not apply HTML encoding to passwords before hashing or comparison. Passwords are opaque binary credentials; encoding transforms them in a context-specific way that has no place in authentication. Pass the raw password directly to `BCrypt.checkpw()`.

---

### A03-18
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Lines:** 57–141 (entire `doPost`)
**Severity:** LOW
**Category:** No CSRF Protection on Login Endpoint

**Description:**
The `doPost` dispatcher handles the `login` operation without any CSRF token validation. Login CSRF is a real vulnerability (an attacker can log a victim into the attacker's account, then observe the victim's sensitive actions). None of the other POST operations in `Frm_security.java` appear to validate a CSRF token either.

**Recommendation:**
Implement CSRF token validation for all state-changing POST requests. For the login form specifically, issue a synchroniser token in the login page and verify it server-side before processing credentials. Consider adopting a framework-level CSRF filter (e.g., OWASP CSRFGuard or Spring Security's CSRF support).

---

### A03-19
**File:** `WEB-INF/src/com/torrent/surat/fms6/security/Databean_security.java`
**Lines:** 158–179 (Fetch_report_nm), and many other methods
**Severity:** MEDIUM
**Category:** SQL Injection (Databean query methods)

**Description:**
`Databean_security` contains multiple query methods that concatenate class-field values (`set_form_cd`, `set_ucd`, `gcd`, `set_cust_cd`, etc.) directly into SQL strings via `Statement.executeQuery()`. These field values are ultimately sourced from HTTP request parameters (set by the calling servlet). Representative examples are shown below.

**Evidence:**
```java
// Lines 158–159 (Fetch_report_nm)
query = "select \"FORM_NAME\" from " + RuntimeConf.form_table
    + " where \"FORM_CD\"='" + set_form_cd + "' ";
rset = stmt.executeQuery(query);

// Lines 171–172
query = "select \"GROUP_CD\" from \"FMS_USR_GRP_REL\" where \"USER_CD\" = '"
    + set_ucd + "' ";
rset = stmt.executeQuery(query);

// Lines 178–180
query = "select \"EDIT\",\"DELETE\",\"PRINT\" from " + RuntimeConf.access_rights_table
    + " where \"FORM_CD\"='" + set_form_cd + "' and \"GROUP_CD\" = '" + gcd + "'";
```

**Recommendation:**
Convert all query methods in `Databean_security` to use `PreparedStatement` with bound parameters. As this is a widely-used helper class, the remediation scope is broad; prioritise methods that accept values with direct user-input provenance.

---

## Summary Table

| ID | File | Lines | Severity | Category |
|----|------|-------|----------|----------|
| A03-1 | Frm_login.java | 58–59, 72–73 | CRITICAL | SQL Injection (login) |
| A03-2 | Frm_login.java | 78–81 | CRITICAL | Plaintext Password Comparison |
| A03-3 | Frm_login.java | 97–100 | HIGH | Password Logged in Cleartext |
| A03-4 | Frm_security.java | 66 | HIGH | Password Logged in Cleartext (dispatcher) |
| A03-5 | Frm_security.java | 2053 | HIGH | Password Logged in Cleartext (chk_login) |
| A03-6 | Frm_security.java | 1167–1175, 1890–1898, 1946 | HIGH | Session Fixation |
| A03-7 | Frm_security.java | 1496–1497 | HIGH | SQL Injection (temp password lookup) |
| A03-8 | Frm_security.java | 2196–2199 | HIGH | SQL Injection (reset_password) |
| A03-9 | Frm_security.java | 2226–2231 | HIGH | SQL Injection (reset_password insert/update) |
| A03-10 | Frm_security.java | 2359–2378 | HIGH | SQL Injection + Plaintext Password Storage (change_password) |
| A03-11 | Frm_security.java | 2435–2458 | HIGH | SQL Injection + MD5 Hashing (chg_bms_pass) |
| A03-12 | Frm_security.java | 1583–1586 | HIGH | Plaintext Password Comparison (AU/MLA) |
| A03-13 | Frm_security.java | 1600, 1974, 1203 | MEDIUM | user_cd Exposed in URL |
| A03-14 | Frm_security.java | 2347, 2420, 2520 | MEDIUM | Broken Access Control (user_cd from request) |
| A03-15 | GetGenericData.java | 21–26 | MEDIUM | Thread-Safety / Instance State Sharing |
| A03-16 | Frm_login.java | 29–141 | MEDIUM | No Session Fixation / Brute-Force / CSRF Protection |
| A03-17 | Frm_security.java | 1420–1421 | LOW | ESAPI Encoding Applied Before BCrypt |
| A03-18 | Frm_security.java | 57–141 | LOW | No CSRF Protection on Login |
| A03-19 | Databean_security.java | 158–179+ | MEDIUM | SQL Injection (Databean query methods) |

**Total findings: 19**
**CRITICAL: 2 | HIGH: 9 | MEDIUM: 6 | LOW: 2**
