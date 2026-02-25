# Security Audit — master Java Package
**Audit ID:** 2026-02-25-01
**Pass:** 1
**Auditor agent:** A06
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `com.torrent.surat.fms6.master`

---

## Step 2 — Files Reviewed

| File | Fully Qualified Class Name |
|------|---------------------------|
| `Databean_user.java` | `com.torrent.surat.fms6.master.Databean_user` |
| `Frm_upload.java` | `com.torrent.surat.fms6.master.Frm_upload` |
| `Databean_customer.java` | `com.torrent.surat.fms6.master.Databean_customer` |
| `Databean_getter.java` | `com.torrent.surat.fms6.master.Databean_getter` |
| `Databean_getuser.java` | `com.torrent.surat.fms6.master.Databean_getuser` |
| `FirmwareverBean.java` | `com.torrent.surat.fms6.master.FirmwareverBean` |
| `Frm_saveuser.java` | `com.torrent.surat.fms6.master.Frm_saveuser` |

---

## Step 3 — Reading Evidence

### Databean_user.java

**Imports (notable):**
- `java.sql.*` — wildcard (FLAG)
- `java.util.*` — wildcard (FLAG)
- `java.lang.reflect.*` — wildcard (FLAG)
- Duplicate `import java.util.ArrayList;` at lines 8 and 9

**Annotations:** None
**Class:** Plain data bean, no servlet.
**Public methods:** None (only private fields, no public methods defined).

---

### Frm_upload.java

**Annotations:** None (@WebServlet, @MultipartConfig absent)
**Extends:** `HttpServlet`
**Imports (notable):**
- `java.io.*` — wildcard (FLAG)
- `java.sql.*` — wildcard (FLAG)
- `javax.servlet.*` — wildcard (FLAG)
- `javax.naming.*` — wildcard (FLAG)
- `javax.sql.*` — wildcard (FLAG)

**Fields:**
- `public Connection dbcon` — public, should be private
- `public String op_code` — public
- `public String date`, `public String url` — public
- `String veh_typ_cd` — package-private (no modifier)

**Public methods:**
- `void init()` — line 46
- `protected void doPost(HttpServletRequest req, HttpServletResponse res)` — line 69
- `public void clearVectors()` — line 102

**Private methods:**
- `private void loadData(HttpServletRequest request)` — line 109

---

### Databean_customer.java

**Imports (notable):**
- `java.sql.*` — wildcard (FLAG)
- `java.util.*` — wildcard (FLAG)
- Duplicate `import java.util.ArrayList;` at lines 8 and 10

**Annotations:** None
**Class:** Data bean (JSP-backing). Not a servlet.
**Key public methods (selection):**
- `public void query(String op_code)` — line 331
- `public void Query_Viewable_Battery() throws SQLException` — line 547
- `public void Query_Viewable_Settings() throws SQLException` — line 578
- `public void Query_Viewable_Reports() throws SQLException` — line 600
- `public void Query_Viewable_Menu() throws SQLException` — line 634
- `public void Query_User_Form_Menu() throws SQLException` — line 725
- `public void queryBlacklist() throws SQLException` — line 804
- `public void querySupervisorList() throws SQLException` — line 871
- `public void Query_User_Access_Restriction() throws SQLException` — line 957
- `public void Query_Current_Alert() throws SQLException` — line 1246
- `public void Query_Alerts() throws SQLException` — line 1289
- `public void Query_Groups_By_Cust() throws SQLException` — line 1387
- `public void Query_Access_Groups() throws SQLException` — line 1430
- `public void Query_Current_User() throws SQLException` — line 1472
- `public void Query_All_Models_By_Cus_Loc_Dept() throws SQLException` — line 1029
- `public void Query_All_Models_By_Cus_Loc_Dept_va() throws SQLException` — line 1163

---

### Databean_getter.java

**Imports (notable):**
- Explicit named imports (no wildcards for java.sql)
- `org.apache.commons.net.ftp.*` — FTP client use

**Annotations:** None
**Class:** Data bean. Not a servlet.
**Key public methods (selection):**
- `public void query(String op_code)` — line 474 (dispatches based on op_code string)
- Numerous getters/setters for vehicle, FTP, model data

---

### Databean_getuser.java

**Imports (notable):**
- `java.sql.*` — wildcard (FLAG)
- `java.util.*` — wildcard (FLAG)
- `com.torrent.surat.fms6.bean.*` — wildcard (FLAG)

**Annotations:** None
**Class:** Data bean. Not a servlet.

---

### FirmwareverBean.java

**Imports:** None (no imports — uses only primitive types and java.lang)
**Annotations:** None
**Class:** Simple value object / bean.
**Public methods:**
- `public String getVeh_id()` / `setVeh_id(String)` — lines 14–20
- `public String getGmtp_id()` / `setGmtp_id(String)` — lines 22–28
- `public String getFirm_vers()` / `setFirm_vers(String)` — lines 30–36
- `public void setCurr_ver(String version)` — line 38
- `public void setCurr_ver_edit(String version)` — line 51
- `public void setCurr_ver()` — line 56
- `public String getRep_time()` / `setRep_time(String)` — lines 61–67
- `public String getHire_no()` / `setHire_no(String)` — lines 69–75
- `public String getType()` / `setType(String)` — lines 77–83
- `public String getCurr_ver()` — line 85

---

### Frm_saveuser.java

**Annotations:** `@SuppressWarnings("deprecation")` — line 34
**Implements:** `HttpServlet`, `SingleThreadModel` (deprecated interface)
**Imports (notable):**
- `javax.servlet.SingleThreadModel` — deprecated, serialises request handling

**Fields (all private):**
- `private Connection dbcon`
- `private String queryString`, `op_code`, `form_cd`, `message`, `url`, `veh_typ_cd`
- `private Statement stmt`, `stmt1`
- `private ResultSet rset`, `rset1`
- `private static Logger log`

**Public methods:**
- `protected void doPost(HttpServletRequest req, HttpServletResponse res)` — line 54

**Private methods (selection — over 80 internal handlers dispatched from doPost):**
- `save_group`, `save_group_rel`, `save_division`, `save_department`
- `save_loc`, `save_branch`, `save_user`, `del_user`, `active_user`
- `save_driver`, `del_driver`, `active_driver`, `driver_setup`
- `conf_driv_setting_ftp`, `conf_mach_setting`, `delete_reminder`, `delete_file`
- `vehicle_serv`, `add_reminder`, `update_hours`, `site_config`
- `save_customer_new`, `save_vehicle`, `save_new_vehicle`
- `setAccessCustomers`, `save_spare_new`, `save_spare_edit`, `save_spare_discard`
- `update_contracthour`, `update_battery`, `update_service`
- (and many more)

---

## Step 4 — Security Review

### Authentication / Authorization

**No authentication guard in doPost (Frm_saveuser, Frm_upload):**
Neither `Frm_saveuser.doPost` (line 54) nor `Frm_upload.doPost` (line 69) contains any check that the caller has an authenticated session. There is no `session.getAttribute("sessionUsrCd") != null` guard or equivalent before processing begins. Session attributes are read only in log statements — they are never validated.

**Access level sourced from HTTP request parameter in save_user (IDOR / privilege escalation):**
In `save_user` (line 4138), the access level written for a newly created user is read directly from the HTTP parameter `"al"`:
```java
String access_cd = request.getParameter("al")==null?"1":request.getParameter("al");
```
This value is then written directly into `FMS_USER_DEPT_REL."ACCESS_LEVEL"` (line 4280). Any authenticated user who can reach the `user_add` op_code can submit `al=1` (or whatever value represents administrator) to create a user with arbitrary privilege.

**Customer ID sourced from HTTP request parameter (IDOR):**
In `save_user` (line 4135), `save_customer_new` (line 5016), and many other handlers, the `user_cd`/`cust_cd` that scopes the write operation comes from `request.getParameter("user_cd")` / `request.getParameter("cust")`. There is no check that the authenticated user's `access_cust` session attribute matches the supplied customer ID. Any authenticated user can supply a different customer's `user_cd` and modify that tenant's data.

**setAccessCustomers — IDOR on user permission assignment:**
In `setAccessCustomers` (line 10788), `user_cd` comes from `request.getParameter("user")` and is used directly in a DELETE + INSERT loop against `FMS_WEBUSER_CUSTOMER_REL`. No check that the caller has permission to modify access for that user.

### SQL Injection

Throughout `Frm_saveuser.java` and the Databean classes, user-controlled strings are concatenated directly into SQL without parameterisation. No `PreparedStatement` is used anywhere in this package. All SQL execution uses `Statement.executeUpdate(queryString)` or `Statement.executeQuery(query)`.

Representative examples:

- `save_group` (line 1312–1318): `group_nm`, `group_desc`, `cust_cd` from `request.getParameter` concatenated into INSERT/UPDATE.
- `save_user` (lines 4265–4270, 4298–4305): ALL user fields concatenated into INSERT/UPDATE on `FMS_USR_MST`. The password field does apply a single-quote doubling (`normalizePswd`) but this is not parameterisation.
- `save_customer_new` (lines 5100–5117): ALL customer fields concatenated into INSERT/UPDATE on `FMS_CUST_MST`.
- `delete_file` (line 3624): `fileName` and `veh_cd` from request parameters concatenated into DELETE.
- `update_contracthour` (line 3651): `setHour` and `veh_cd` from request parameters concatenated into UPDATE.
- `update_battery` (line 3673): `set_fleetno` and `p_id` from request parameters concatenated into UPDATE.
- `setAccessCustomers` (lines 10797–10804): `user_cd`, `cust_ids[i]`, `loc_ids[i]` from request parameters concatenated into DELETE/INSERT.
- `Databean_customer.Query_Viewable_Battery/Settings/Reports/Menu` (lines 551, 582, 604, 666): `Param_User` and `Param_Module` (set from JSP) concatenated directly into SELECT.
- `Databean_customer.queryBlacklist` (lines 806, 813): `Param_User` concatenated into SELECT.
- `Databean_customer.Query_User_Access_Restriction` (lines 959, 966, 973, 980): `Param_User` concatenated into SELECT.

### File Upload (Frm_upload)

1. No content-type validation — `getContentType()` is never called on the `FileItem`.
2. No file extension whitelist check anywhere in `loadData`.
3. Upload directory is INSIDE the web root: `base = this.getServletContext().getRealPath("/")` followed by `path = base+"/images/pics/"` (lines 115–116). Uploaded files are directly web-accessible and, on Tomcat, any `.jsp` file written there would be executed by the server.
4. No file size limit — `DiskFileItemFactory` is instantiated with no `setSizeThreshold` and `ServletFileUpload` has no `setSizeMax`.
5. The filename is only partially randomised: a random integer 0–999 is prepended but the original filename (after last `\`) is appended verbatim. A filename like `../../evil.jsp` with no backslash would result in `<rand>_../../evil.jsp` which, when used in `new File(path + fileName)`, could traverse directories (path traversal risk).
6. No authentication check in `doPost` before `loadData` is called.

### Command Injection

No `Runtime.getRuntime().exec()` or `ProcessBuilder` found in this package. Not applicable.

### SSRF

No HTTP client calls (`HttpURLConnection`, `HttpClient`, `URL.openConnection`) found in this package. Not applicable.

### CSRF

No CSRF token validation exists anywhere in `Frm_saveuser.doPost` or `Frm_upload.doPost`. No token is checked in any handler method. All state-changing operations are vulnerable to cross-site request forgery.

### Multi-tenancy

`Frm_saveuser` relies entirely on user-supplied request parameters (`cust`, `user_cd`, `cust_cd`, etc.) to scope writes to a tenant. Session attributes `access_cust`, `access_site`, `access_dept` are logged but never enforced. This means an authenticated user of any tenant can target another tenant's data by supplying a different `cust_cd`.

---

## Step 5 — Findings

---

### A06-1 — No Authentication Guard on Frm_saveuser and Frm_upload

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`, line 54
`WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java`, line 69
**Severity:** Critical
**Category:** Authentication / Authorization (Section 2)

**Description:**
Neither servlet verifies that the caller holds a valid authenticated session before processing any operation. The `doPost` entry point proceeds directly to database connection and operation dispatch. Session attributes (`sessionUsrCd`, `access_level`, `access_cust`) are referenced only in log statements and are never checked against a null/empty guard.

**Evidence:**
```java
// Frm_saveuser.java line 54–82
protected void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
    res.setContentType("text/plain");
    try {
        // ... JNDI connection setup ...
        op_code = req.getParameter("op_code")==null?"":req.getParameter("op_code");
        // No session authentication check before here or before dispatch
        if(req.getParameter("op_code").equalsIgnoreCase("group_add")) {
            save_group(req);
        }
        // ... 40+ additional operation branches ...
    }
}
```

**Recommendation:**
Add an authentication guard at the start of each `doPost` method, before any other processing:
```java
HttpSession session = req.getSession(false);
if (session == null || session.getAttribute("sessionUsrCd") == null) {
    res.sendError(HttpServletResponse.SC_UNAUTHORIZED);
    return;
}
```
Consider using a servlet filter applied to all protected URLs rather than duplicating this check.

---

### A06-2 — User Access Level Set from HTTP Request Parameter (Privilege Escalation)

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`, lines 4138, 4279–4281
**Severity:** Critical
**Category:** Authentication / Authorization (Section 2)

**Description:**
The access level (`ACCESS_LEVEL`) assigned to a new or updated user account is read directly from the HTTP POST parameter `"al"`. Any authenticated user who can reach the `user_add` or `user_edit` operation can submit an arbitrary access level value — including the highest privilege — to create or promote an admin account without any server-side permission check.

**Evidence:**
```java
// line 4138
String access_cd = request.getParameter("al")==null?"1":request.getParameter("al");

// line 4279-4281
queryString = "Insert into \"FMS_USER_DEPT_REL\" (\"USER_CD\",\"CUST_CD\",\"LOC_CD\",\"DEPT_CD\",\"ACCESS_LEVEL\") " +
    "values ('"+user_cd+"','"+cust_cd+"','"+site_cd+"','"+dept_cd+"','"+access_cd+"')";
stmt.executeUpdate(queryString);
```

**Recommendation:**
The maximum access level that a creating user may assign must be capped to at most their own access level, read from the server-side session:
```java
int callerLevel = Integer.parseInt(
    (String) request.getSession().getAttribute("access_level"));
int requestedLevel = Integer.parseInt(request.getParameter("al"));
if (requestedLevel < callerLevel) {
    // reject: user is trying to grant a level higher than their own
    return;
}
```
Never trust access level values from client-controlled input.

---

### A06-3 — Insecure Direct Object Reference (IDOR) — Cross-Tenant Data Modification

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`, lines 4135, 5016, 10788, and throughout
**Severity:** Critical
**Category:** Multi-tenancy / Authorization (Section 2)

**Description:**
Customer/tenant scope for all write operations (create, update, delete users, vehicles, customers, alerts, access permissions) is determined entirely by user-supplied request parameters (`cust`, `user_cd`, `cust_cd`, etc.). Session attributes containing the authenticated user's customer scope (`access_cust`, `access_site`, `access_dept`) are populated but never validated against the incoming request parameters. Any authenticated user can modify data belonging to a different tenant by supplying another tenant's `user_cd` or `cust_cd`.

**Evidence:**
```java
// save_user line 4135
String cust_cd = request.getParameter("cust")==null?"0":request.getParameter("cust");

// save_customer_new line 5016
String user_cd = request.getParameter("user_cd")==null?"":request.getParameter("user_cd");

// setAccessCustomers line 10788
String user_cd = request.getParameter("user")==null?"":request.getParameter("user");
// line 10797
queryString = "delete from \"FMS_WEBUSER_CUSTOMER_REL\" where \"USER_CD\" = "+user_cd;
```
Session attribute `access_cust` is read only for logging (lines 73, 78, 79, 402) and is never compared to the supplied `cust_cd`.

**Recommendation:**
Before executing any tenant-scoped write, verify that the customer/user being acted upon belongs to the authenticated user's scope:
```java
String sessionCustCd = (String) request.getSession().getAttribute("access_cust");
if (!sessionCustCd.equals(cust_cd)) {
    res.sendError(HttpServletResponse.SC_FORBIDDEN);
    return;
}
```

---

### A06-4 — Pervasive SQL Injection via String Concatenation

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`, multiple methods
`WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java`, multiple methods
**Severity:** Critical
**Category:** SQL Injection (Section 3)

**Description:**
Every SQL statement in this package is built by string concatenation of user-controlled request parameters. No `PreparedStatement` is used anywhere. This creates SQL injection vulnerabilities across all read and write operations. An attacker can supply crafted values to extract, modify, or delete arbitrary database data, bypass authentication, or (depending on PostgreSQL configuration) escalate to OS-level access.

**Evidence (selection):**
```java
// Frm_saveuser.java save_group, lines 1312-1313
queryString = "Insert into \"FMS_GRP_MST\" (\"GROUP_CD\",\"GROUP_NAME\",\"GROUP_DESC\",\"CUST_CD\") " +
    "values ('"+group_cd+"','"+group_nm+"','"+group_desc+"','"+cust_cd+"')";

// Frm_saveuser.java delete_file, line 3624
queryString = "delete from fms_inspection_files where veh_id = "+veh_cd
    +" and file_name='"+fileName+"'";

// Frm_saveuser.java update_contracthour, line 3651
queryString = "update \"FMS_VEHICLE_MST\" set \"COUNT_HOUR\" = "+setHour
    +" where \"VEHICLE_CD\" = " + veh_cd;

// Frm_saveuser.java save_user, lines 4265-4270
queryString = "Insert into \"FMS_USR_MST\" (...) " +
    "values ('"+user_cd+"','"+user_nm+"','"+user_desc+"','"+normalizePswd+"','"+active+"',...)"

// Databean_customer.java queryBlacklist, line 806
query = "select count(*) from \"FMS_DRIVER_BLKLST\" where \"USER_CD\" = " + Param_User;

// Databean_customer.java Query_Viewable_Reports, line 604
query = "... AND \"FMS_USR_MST\".\"USER_CD\" ='"+Param_User+"' AND "
    + RuntimeConf.form_table + ".\"MODULE_CD\" = 4 ...";
```
Note: The password field uses `password.replace("'", "''")` (line 4199, 5110) as mitigation, but this is not parameterisation and does not protect against all injection vectors.

**Recommendation:**
Replace all SQL string concatenation with `PreparedStatement` and bind parameters:
```java
PreparedStatement ps = dbcon.prepareStatement(
    "INSERT INTO \"FMS_GRP_MST\" (\"GROUP_NAME\",\"GROUP_DESC\",\"CUST_CD\") VALUES (?,?,?)");
ps.setString(1, group_nm);
ps.setString(2, group_desc);
ps.setString(3, cust_cd);
ps.executeUpdate();
```
This must be applied to every query in every method across this package.

---

### A06-5 — Unrestricted File Upload Inside Web Root (Remote Code Execution Risk)

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java`, lines 115–137
**Severity:** Critical
**Category:** File Upload (Section 3)

**Description:**
The `Frm_upload` servlet writes uploaded files into the web application's own directory tree (`/images/pics/` relative to the application root). There is no validation of the uploaded file's MIME type or content type, no file extension whitelist, and no restriction on size. Combined with the lack of authentication (A06-1), any unauthenticated attacker can upload a JSP file to this directory. Because the directory is inside the web root, the server will execute the uploaded JSP on the next HTTP request, giving the attacker a web shell with full application-server privileges.

**Evidence:**
```java
// lines 114-137
base = this.getServletContext().getRealPath("/");   // Web root
path = base+"/images/pics/";                        // Inside web root

Random ran = new Random();
fileName = "" + ran.nextInt(1000) + "_"
    + fitem.getName().substring(fitem.getName().lastIndexOf('\\') + 1);
// No content-type check, no extension whitelist, no size limit
File f = new File(path + fileName);
fitem.write(f);                                    // File written unconditionally
```

Five concurrent issues:
1. Upload directory is inside the web root — uploaded files are web-accessible and JSP files will be executed.
2. No content type validation (`fitem.getContentType()` is never called).
3. No file extension whitelist.
4. No file size limit (`DiskFileItemFactory`/`ServletFileUpload` size properties not set).
5. No authentication check before upload processing.

**Recommendation:**
1. Move the upload directory outside the web root (e.g. a dedicated directory on the filesystem with no HTTP mapping).
2. Validate the MIME type using a library such as Apache Tika against the actual file content (not the `Content-Type` header).
3. Enforce a strict extension whitelist (e.g. `jpg`, `png`, `gif` only for this logo-upload use case).
4. Set a maximum file size: `upload.setSizeMax(5 * 1024 * 1024)`.
5. Sanitise the filename: strip path separators, reject files whose resolved path escapes the target directory.
6. Add authentication guard (see A06-1).

---

### A06-6 — Path Traversal in Uploaded Filename

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java`, lines 131–137
**Severity:** High
**Category:** File Upload / Path Traversal (Section 3)

**Description:**
The uploaded filename is taken from `fitem.getName()` and only stripped of characters up to the last backslash (`\\`). On a Linux/Mac server (where the path separator is `/`) a filename containing `/` characters (e.g. `../../WEB-INF/web.xml`) would not be stripped, allowing the attacker to write files to arbitrary locations on the server.

**Evidence:**
```java
// lines 131-136
fileName = "" + ran.nextInt(1000) + "_"
    + fitem.getName().substring(
        fitem.getName().lastIndexOf('\\') + 1);  // Only strips backslash paths
File f = new File(path + fileName);
fitem.write(f);
```
If `fitem.getName()` returns `../../conf/evil.conf`, `lastIndexOf('\\')` returns -1, `substring(0)` returns the full string, and `path + fileName` becomes `…/images/pics/../../conf/evil.conf`.

**Recommendation:**
Extract only the bare filename using `Paths.get(fitem.getName()).getFileName().toString()` (Java NIO), then verify the canonical resolved path starts with the intended upload directory:
```java
Path uploadDir = Paths.get(path).toRealPath();
Path target = uploadDir.resolve(Paths.get(fitem.getName()).getFileName()).normalize();
if (!target.startsWith(uploadDir)) {
    throw new SecurityException("Path traversal detected");
}
```

---

### A06-7 — No CSRF Protection on Any State-Changing Operation

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`, line 54 (doPost)
`WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java`, line 69 (doPost)
**Severity:** High
**Category:** CSRF (Section 4)

**Description:**
Neither servlet checks for a CSRF token. The search for `csrf`, `CSRF`, `token`, or `_token` in `Frm_saveuser.java` returned no matches. Every state-changing operation (user creation and deletion, customer creation and modification, vehicle assignment, access control changes, file upload, etc.) can be triggered by a cross-origin request from a page loaded in any browser tab where the user is authenticated. An attacker who tricks a logged-in administrator into visiting a malicious page can create admin accounts, delete data, or exfiltrate configuration.

**Evidence:**
```java
// Frm_saveuser.java line 54 — no CSRF check before or inside doPost
protected void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
    // No token validation. Dispatches to 40+ state-changing operations.
}
```
Grep result for CSRF/token: `No matches found`.

**Recommendation:**
Implement the synchronizer token pattern. Generate a per-session CSRF token at login, store it in the session, embed it as a hidden field in every form, and validate it at the start of every `doPost`:
```java
String sessionToken = (String) req.getSession().getAttribute("csrfToken");
String requestToken = req.getParameter("csrfToken");
if (sessionToken == null || !sessionToken.equals(requestToken)) {
    res.sendError(HttpServletResponse.SC_FORBIDDEN, "CSRF validation failed");
    return;
}
```

---

### A06-8 — Cleartext Password Storage and Transmission

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`, lines 4119, 4199, 4268, 5022, 5103–5117
**Severity:** High
**Category:** Credential Handling (Section 2)

**Description:**
User and customer passwords are received as plaintext HTTP parameters (`request.getParameter("pass")`), stored directly in the database (`FMS_USR_MST."PASSWORD"`, `FMS_CUST_MST."PASSWORD"`), and retrieved from the database in `Query_Current_User` (line 1480: `"FMS_USR_MST"."PASSWORD"` is column 3 in the SELECT result). For the non-AU code path in `save_user` the password undergoes no processing at all. For the AU path a single-quote doubling is applied (`password.replace("'", "''")`) which is entirely for SQL syntax, not security. Passwords are not hashed with a modern algorithm (BCrypt, Argon2, or PBKDF2).

**Evidence:**
```java
// save_user line 4119
String password = request.getParameter("pass")==null?"":request.getParameter("pass");

// line 4199
String normalizePswd = password.replace("'", "''");  // Not hashing — just escaping

// line 4268
"values ('"+user_cd+"','"+user_nm+"','"+user_desc+"','"+normalizePswd+"','"+active+"',...)"

// save_customer_new line 5022
String password = request.getParameter("pass")==null?"":request.getParameter("pass");
// line 5103
"values ('"+user_cd+"','"+user_nm+"','"+user_desc+"','"+password+"','"+active+"',...)"
```

**Recommendation:**
Hash all passwords using BCrypt (or Argon2 where FIPS compliance is not required) before storage:
```java
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);
String hashedPassword = encoder.encode(password);
```
Never store or log plaintext passwords. Never return the password column in query results used by JSP pages.

---

### A06-9 — Wildcard Imports Across Multiple Classes

**Files:**
`Databean_user.java` lines 4, 16, 28
`Frm_upload.java` lines 2, 3, 7, 9, 10
`Databean_customer.java` lines 4, 17
`Databean_getuser.java` lines 4, 14, 16
**Severity:** Low
**Category:** Code Quality / Defence-in-Depth

**Description:**
Wildcard imports (`java.sql.*`, `java.util.*`, `java.lang.reflect.*`, `javax.servlet.*`, `javax.naming.*`, `javax.sql.*`, `com.torrent.surat.fms6.bean.*`) are used across the package. While not directly exploitable, wildcard imports obscure which classes are actually in scope, complicate security review, and in rare cases allow class name shadowing if a malicious JAR is placed on the classpath.

**Evidence:**
```java
// Databean_user.java lines 4, 16, 28
import java.sql.*;
import java.util.*;
import java.lang.reflect.*;

// Frm_upload.java lines 2, 7, 9, 10
import java.io.*;
import javax.servlet.*;
import javax.naming.*;
import javax.sql.*;
```

**Recommendation:**
Replace all wildcard imports with explicit named imports. Most IDEs can perform this refactoring automatically (Eclipse: `Source > Organize Imports`; IntelliJ: `Code > Optimize Imports`).

---

### A06-10 — Use of Deprecated SingleThreadModel in Frm_saveuser

**File:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`, line 35
**Severity:** Medium
**Category:** Concurrency / Architecture

**Description:**
`Frm_saveuser` implements the deprecated `javax.servlet.SingleThreadModel` interface. This interface was deprecated in the Servlet 2.4 specification (2003) and removed in later versions. Its purpose was to serialise servlet invocations to prevent concurrent access, but this approach causes a severe performance bottleneck (one request at a time) and does not reliably prevent shared-state race conditions when connection pools or EJBs are used. The use of instance-level fields (`dbcon`, `stmt`, `rset`, `queryString`, `message`, `url`, `op_code`) for per-request state — the underlying reason `SingleThreadModel` was added — is an architectural defect.

**Evidence:**
```java
// line 35
public class Frm_saveuser extends HttpServlet implements SingleThreadModel {
// line 38-49 — instance fields for per-request state
private Connection dbcon = null;
private String queryString = "";
private String message = "";
private String op_code = "";
private Statement stmt = null;
private ResultSet rset = null;
```

**Recommendation:**
Move all per-request state (connection, statement, resultset, queryString, message, url, op_code) to local variables inside `doPost` and its called methods. Remove `implements SingleThreadModel`. The servlet can then safely serve concurrent requests and the bottleneck is eliminated.

---

## Summary Table

| ID | Severity | Category | File | Description |
|----|----------|----------|------|-------------|
| A06-1 | Critical | Authentication | `Frm_saveuser.java:54`, `Frm_upload.java:69` | No authentication guard in doPost — unauthenticated access to all operations |
| A06-2 | Critical | Privilege Escalation | `Frm_saveuser.java:4138` | Access level for new users taken from HTTP parameter `"al"` |
| A06-3 | Critical | IDOR / Multi-tenancy | `Frm_saveuser.java:4135, 5016, 10788` | Customer/tenant scope set from request parameters, not session |
| A06-4 | Critical | SQL Injection | `Frm_saveuser.java` (all methods), `Databean_customer.java` (all query methods) | All SQL built by string concatenation; no PreparedStatement used |
| A06-5 | Critical | File Upload / RCE | `Frm_upload.java:115-137` | No type/extension check, upload inside web root, no size limit, no auth |
| A06-6 | High | Path Traversal | `Frm_upload.java:131-136` | Filename stripped of backslash only; forward-slash traversal possible |
| A06-7 | High | CSRF | `Frm_saveuser.java:54`, `Frm_upload.java:69` | No CSRF token on any state-changing operation |
| A06-8 | High | Credential Handling | `Frm_saveuser.java:4119, 5022` | Passwords stored in plaintext; no hashing applied |
| A06-9 | Low | Code Quality | Multiple files | Wildcard imports throughout the package |
| A06-10 | Medium | Concurrency / Architecture | `Frm_saveuser.java:35` | Deprecated SingleThreadModel serialises all requests; instance-level per-request state |

**Total findings: 10**
