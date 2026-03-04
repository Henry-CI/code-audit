# Common Critical Findings — FleetIQ & FleetFocus

**Total matched findings:** 32  
**Files affected:** 10  

---

## WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java

### [P1-J55-F01] / [P1-A04-01]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19-20, 30, 54-55, 87-89  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18, 28, 54, 86, 87, 88  

Description: `RuntimeConf.java` contains multiple plaintext credentials committed directly to source control. This includes firmware server passwords, an FTP account password, a generic test/admin password, and full Clickatell SMS API credentials (username, password, API ID). Any developer with read access to the repository has these credentials. If the repository is ever leaked or cloned by an unauthorised party, all of these accounts are immediately compromised.

Fix: // RuntimeConf.java public static String pass="ciifirmware"; //old firmware password        // line 18 public static String firmwarepass = "Sdh79HfkLq6";                      // line 28 public static String password = "testadmin";                             // line 54 public static String PASSWORD = "fOqDVWYK";   // Clickatell SMS API     // line 87 public static String USERNAME = "collintell";  // Clickatell SMS API     // line 86 public static String API_ID = "3259470";       // Clickatell SMS API     // line 88

---

### [P1-J55-F01] / [P2-A20-03]

**FleetFocus:** File: RuntimeConf.java | Line: 20, 30, 54-55, 87-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18, 28, 54, 86, 87, 88  

Description: `RuntimeConf.java` contains multiple plaintext credentials committed directly to source control. This includes firmware server passwords, an FTP account password, a generic test/admin password, and full Clickatell SMS API credentials (username, password, API ID). Any developer with read access to the repository has these credentials. If the repository is ever leaked or cloned by an unauthorised party, all of these accounts are immediately compromised.

Fix: // RuntimeConf.java public static String pass="ciifirmware"; //old firmware password        // line 18 public static String firmwarepass = "Sdh79HfkLq6";                      // line 28 public static String password = "testadmin";                             // line 54 public static String PASSWORD = "fOqDVWYK";   // Clickatell SMS API     // line 87 public static String USERNAME = "collintell";  // Clickatell SMS API     // line 86 public static String API_ID = "3259470";       // Clickatell SMS API     // line 88

---

### [P1-J73-F02] / [P2-A20-03]

**FleetFocus:** File: RuntimeConf.java | Line: 20, 30, 54-55, 87-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 17–19, 27–28, 53–54, 86–88  

Description: `RuntimeConf.java` contains multiple hardcoded credentials committed to the repository: (1) an FTP username/password pair for an old firmware server (`user="firmware"`, `pass="ciifirmware"`, lines 18–19); (2) the firmware FTP password `firmwarepass = "Sdh79HfkLq6"` (line 28); (3) a Clickatell SMS API password `PASSWORD = "fOqDVWYK"` (line 87) and API ID `API_ID = "3259470"` (line 88); (4) a generic `username = "TestK"` and `password = "testadmin"` (lines 53–54). These are all checked in to version control and visible to anyone with repository access.

Fix: // RuntimeConf.java lines 17–19 public static String server="fms2.ciifm.com";//old firmware server public static String user="firmware"; //old firmware user name public static String pass="ciifirmware"; //old firmware password // RuntimeConf.java lines 27–28 public static String firmwareuser = "firmware"; public static String firmwarepass = "Sdh79HfkLq6"; // RuntimeConf.java lines 86–88 public static String USERNAME = "collintell"; public static String PASSWORD = "fOqDVWYK"; public static String API_ID = "3259470"; // RuntimeConf.java lines 53–54 public static String username = "TestK"; public static String password = "testadmin";

---

### [P1-J73-F02] / [P4-UTLGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 17–19, 27–28, 53–54, 86–88  

Description: `RuntimeConf.java` contains multiple hardcoded credentials committed to the repository: (1) an FTP username/password pair for an old firmware server (`user="firmware"`, `pass="ciifirmware"`, lines 18–19); (2) the firmware FTP password `firmwarepass = "Sdh79HfkLq6"` (line 28); (3) a Clickatell SMS API password `PASSWORD = "fOqDVWYK"` (line 87) and API ID `API_ID = "3259470"` (line 88); (4) a generic `username = "TestK"` and `password = "testadmin"` (lines 53–54). These are all checked in to version control and visible to anyone with repository access.

Fix: // RuntimeConf.java lines 17–19 public static String server="fms2.ciifm.com";//old firmware server public static String user="firmware"; //old firmware user name public static String pass="ciifirmware"; //old firmware password // RuntimeConf.java lines 27–28 public static String firmwareuser = "firmware"; public static String firmwarepass = "Sdh79HfkLq6"; // RuntimeConf.java lines 86–88 public static String USERNAME = "collintell"; public static String PASSWORD = "fOqDVWYK"; public static String API_ID = "3259470"; // RuntimeConf.java lines 53–54 public static String username = "TestK"; public static String password = "testadmin";

---

### [P1-J73-F02] / [P4-UTILGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 17–19, 27–28, 53–54, 86–88  

Description: `RuntimeConf.java` contains multiple hardcoded credentials committed to the repository: (1) an FTP username/password pair for an old firmware server (`user="firmware"`, `pass="ciifirmware"`, lines 18–19); (2) the firmware FTP password `firmwarepass = "Sdh79HfkLq6"` (line 28); (3) a Clickatell SMS API password `PASSWORD = "fOqDVWYK"` (line 87) and API ID `API_ID = "3259470"` (line 88); (4) a generic `username = "TestK"` and `password = "testadmin"` (lines 53–54). These are all checked in to version control and visible to anyone with repository access.

Fix: // RuntimeConf.java lines 17–19 public static String server="fms2.ciifm.com";//old firmware server public static String user="firmware"; //old firmware user name public static String pass="ciifirmware"; //old firmware password // RuntimeConf.java lines 27–28 public static String firmwareuser = "firmware"; public static String firmwarepass = "Sdh79HfkLq6"; // RuntimeConf.java lines 86–88 public static String USERNAME = "collintell"; public static String PASSWORD = "fOqDVWYK"; public static String API_ID = "3259470"; // RuntimeConf.java lines 53–54 public static String username = "TestK"; public static String password = "testadmin";

---

### [P1-J81-F01] / [P1-A04-01]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19-20, 30, 54-55, 87-89  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 17–19, 27–29, 53–54  

Description: `RuntimeConf.java` contains at least three distinct sets of hardcoded plaintext passwords committed directly to source control. These include a firmware server password (`ciifirmware`), a secondary firmware/FTP password (`Sdh79HfkLq6`), and an application-level test credential (`testadmin`). All are stored as `public static` fields, making them globally accessible throughout the application at runtime with no access control whatsoever. The field `pass` is annotated in a comment as "old firmware password" and `user` as "old firmware user name," suggesting these may be deprecated — but they remain live in source code and are committed to the repository. There is also a separate `firmwarepass` field with a different value, indicating multiple credential sets exist simultaneously. Any developer with repository access, or any attacker who achieves source disclosure, obtains all credentials immediately.

Fix: // RuntimeConf.java lines 17–19 public static String server="fms2.ciifm.com";//old firmware server public static String user="firmware"; //old firmware user name public static String pass="ciifirmware"; //old firmware password // RuntimeConf.java lines 27–29 public static String firmwareuser = "firmware"; public static String firmwarepass = "Sdh79HfkLq6"; public static String firmwarepassmask = "******"; // RuntimeConf.java lines 53–54 public static String username = "TestK"; public static String password = "testadmin";

---

### [P2-J81-F27] / [P1-A04-01]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19-20, 30, 54-55, 87-89  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 28  

Description: RuntimeConf contains hardcoded FTP password "Sdh79HfkLq6" on line 28. This is a security violation. No test validates that credentials are not committed to source control or that they can be externalized.

Fix: Move credentials to external configuration (environment variables, encrypted properties files, secret management system). Add test validating credentials are not hardcoded and are loaded from secure external source.

---

### [P2-J81-F27] / [P2-A20-03]

**FleetFocus:** File: RuntimeConf.java | Line: 20, 30, 54-55, 87-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 28  

Description: RuntimeConf contains hardcoded FTP password "Sdh79HfkLq6" on line 28. This is a security violation. No test validates that credentials are not committed to source control or that they can be externalized.

Fix: Move credentials to external configuration (environment variables, encrypted properties files, secret management system). Add test validating credentials are not hardcoded and are loaded from secure external source.

---

### [P2-J81-F27] / [P4-UTLGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 28  

Description: RuntimeConf contains hardcoded FTP password "Sdh79HfkLq6" on line 28. This is a security violation. No test validates that credentials are not committed to source control or that they can be externalized.

Fix: Move credentials to external configuration (environment variables, encrypted properties files, secret management system). Add test validating credentials are not hardcoded and are loaded from secure external source.

---

### [P2-J81-F27] / [P4-UTILGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 28  

Description: RuntimeConf contains hardcoded FTP password "Sdh79HfkLq6" on line 28. This is a security violation. No test validates that credentials are not committed to source control or that they can be externalized.

Fix: Move credentials to external configuration (environment variables, encrypted properties files, secret management system). Add test validating credentials are not hardcoded and are loaded from secure external source.

---

### [P2-J81-F28] / [P1-A04-01]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19-20, 30, 54-55, 87-89  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19, 54, 87  

Description: RuntimeConf contains multiple hardcoded credentials: firmware password "ciifirmware" (line 19), SMS API password "fOqDVWYK" (line 87), test credentials "testadmin" (line 54). No test validates secure credential management.

Fix: Externalize all credentials to secure configuration management. Add tests verifying: (1) credentials are loaded from secure sources, (2) credentials are not logged, (3) masked passwords are used for display.

---

### [P2-J81-F28] / [P2-A20-03]

**FleetFocus:** File: RuntimeConf.java | Line: 20, 30, 54-55, 87-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19, 54, 87  

Description: RuntimeConf contains multiple hardcoded credentials: firmware password "ciifirmware" (line 19), SMS API password "fOqDVWYK" (line 87), test credentials "testadmin" (line 54). No test validates secure credential management.

Fix: Externalize all credentials to secure configuration management. Add tests verifying: (1) credentials are loaded from secure sources, (2) credentials are not logged, (3) masked passwords are used for display.

---

### [P2-J81-F28] / [P4-UTLGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19, 54, 87  

Description: RuntimeConf contains multiple hardcoded credentials: firmware password "ciifirmware" (line 19), SMS API password "fOqDVWYK" (line 87), test credentials "testadmin" (line 54). No test validates secure credential management.

Fix: Externalize all credentials to secure configuration management. Add tests verifying: (1) credentials are loaded from secure sources, (2) credentials are not logged, (3) masked passwords are used for display.

---

### [P2-J81-F28] / [P4-UTILGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19, 54, 87  

Description: RuntimeConf contains multiple hardcoded credentials: firmware password "ciifirmware" (line 19), SMS API password "fOqDVWYK" (line 87), test credentials "testadmin" (line 54). No test validates secure credential management.

Fix: Externalize all credentials to secure configuration management. Add tests verifying: (1) credentials are loaded from secure sources, (2) credentials are not logged, (3) masked passwords are used for display.

---

### [P2-J81-F34] / [P4-UTLGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 86-88  

Description: RuntimeConf contains hardcoded Clickatell SMS API credentials (USERNAME="collintell", PASSWORD="fOqDVWYK", API_ID="3259470" on lines 86-88). These are third-party API credentials that should never be in source code. No test validates secure credential management.

Fix: Immediately rotate exposed API credentials. Move all API credentials to secure secret management (environment variables, vault, encrypted config). Add tests verifying: (1) API credentials load from secure source, (2) credentials are not logged or exposed, (3) invalid credentials are handled gracefully.

---

### [P2-J81-F34] / [P4-UTILGZ-5.1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 86-88  

Description: RuntimeConf contains hardcoded Clickatell SMS API credentials (USERNAME="collintell", PASSWORD="fOqDVWYK", API_ID="3259470" on lines 86-88). These are third-party API credentials that should never be in source code. No test validates secure credential management.

Fix: Immediately rotate exposed API credentials. Move all API credentials to secure secret management (environment variables, vault, encrypted config). Add tests verifying: (1) API credentials load from secure source, (2) credentials are not logged or exposed, (3) invalid credentials are handled gracefully.

---

## WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java

### [P2-J70-F02] / [P1-A03-1]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 58-59, 72-73  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 58-59, 72-73  

Description: Lines 58-59 and 72-73 construct SQL queries using direct string concatenation of user-supplied login parameter without any sanitization or prepared statements: `"select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '" + login + "'"`. This allows trivial SQL injection attacks. No tests verify that injection attempts are blocked or that prepared statements are used. Attackers can bypass authentication, extract database contents, or modify data.

Fix: (1) Implement prepared statements with parameterized queries immediately, (2) Create security test suite that attempts common SQL injection patterns: `admin'--`, `' OR '1'='1'--`, `'; DROP TABLE "FMS_USR_MST";--`, union-based injections, blind SQL injection, time-based attacks, (3) Verify input validation rejects malicious input, (4) Test that error messages don't leak database structure information.

---

### [P2-J70-F02] / [P2-A18-03]

**FleetFocus:** File: Frm_login.java | Line: 58-59, 72-73  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 58-59, 72-73  

Description: Lines 58-59 and 72-73 construct SQL queries using direct string concatenation of user-supplied login parameter without any sanitization or prepared statements: `"select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '" + login + "'"`. This allows trivial SQL injection attacks. No tests verify that injection attempts are blocked or that prepared statements are used. Attackers can bypass authentication, extract database contents, or modify data.

Fix: (1) Implement prepared statements with parameterized queries immediately, (2) Create security test suite that attempts common SQL injection patterns: `admin'--`, `' OR '1'='1'--`, `'; DROP TABLE "FMS_USR_MST";--`, union-based injections, blind SQL injection, time-based attacks, (3) Verify input validation rejects malicious input, (4) Test that error messages don't leak database structure information.

---

### [P4-J70-F11] / [P2-A18-02]

**FleetFocus:** File: Frm_login.java | Line: 97-99, 66, 2053  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 71-81  

Description: Passwords are retrieved from the database and compared directly as plaintext strings (line 81). This indicates passwords are stored in plaintext in the database, which is a severe security vulnerability. If the database is compromised, all user passwords are immediately exposed.

Fix: Implement proper password hashing using a strong algorithm like BCrypt, Argon2, or PBKDF2. Store only password hashes in the database. During authentication, hash the provided password and compare hashes (not plaintext). Note: This requires database schema changes and password migration.

---

### [P4-J70-F11] / [P2-A18-04]

**FleetFocus:** File: Frm_login.java | Line: 81  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 71-81  

Description: Passwords are retrieved from the database and compared directly as plaintext strings (line 81). This indicates passwords are stored in plaintext in the database, which is a severe security vulnerability. If the database is compromised, all user passwords are immediately exposed.

Fix: Implement proper password hashing using a strong algorithm like BCrypt, Argon2, or PBKDF2. Store only password hashes in the database. During authentication, hash the provided password and compare hashes (not plaintext). Note: This requires database schema changes and password migration.

---

### [P4-J70-F12] / [P2-A18-02]

**FleetFocus:** File: Frm_login.java | Line: 97-99, 66, 2053  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 97-100  

Description: Lines 97-100 log failed login attempts including the plaintext user password and database password to the log file. This exposes sensitive credentials in log files, which may be accessible to unauthorized personnel or inadvertently included in log aggregation systems.

Fix: Remove password logging completely. Log only non-sensitive information like username, timestamp, and IP address. Never log passwords, tokens, or other credentials.

---

## WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java

### [P2-J31-F20] / [P4-SMS-01]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java | Line: 29  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java | Line: 39, 87, 105, 121  

Description: The static `cusList` variable (line 39) is populated in `getCustomers` (line 87) and then read by `getSites` and `getDepartments`. In a multi-user environment, concurrent requests will cause race conditions where User A's call to getCustomers overwrites the cusList that User B is reading in getSites, causing data leakage. No tests verify thread-safety.

Fix: Create concurrent load tests simulating multiple users with different permissions calling these methods simultaneously. Verify each user only sees their authorized data. Refactor to use session-scoped or request-scoped storage instead of static fields.

---

### [P4-J31-F02] / [P4-TS-02]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java | Line: 29  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java | Line: 41, 44, 196  

Description: Config.java stores HttpServletRequest in a static field (line 41), making it shared across all concurrent requests. The field is assigned in getCustomers() and later accessed in getTime(). This creates a severe thread-safety issue where concurrent requests will overwrite each other's request objects, leading to data corruption and potential security issues (users accessing wrong sessions).

Fix: Pass HttpServletRequest as a parameter to getTime() instead of storing it in a static field. Remove the static request field entirely.

---

## WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java

### [P2-J83-F08] / [P4-UTLGZ-6.8]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: 86  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: 257-326  

Description: The `getLocalTime` method constructs SQL queries by concatenating `webUserCD` directly into the query string at line 288 without parameterization. This is a critical SQL injection vulnerability in time conversion code that processes user credentials. An attacker could inject malicious SQL to bypass authentication or extract sensitive data. Additionally, the method performs complex dealer date format logic (lines 276-298) with multiple conditional branches that are completely untested.

Fix: Add comprehensive test suite: (1) Test SQL injection attempts with malicious `webUserCD` values; (2) Test super admin path (SessionVar.isSuperAdmin = true) separately from normal user path; (3) Test with null/empty webUserCD; (4) Test when dealer date format is null or empty; (5) Test the fallback date format logic; (6) Mock database responses for various scenarios; (7) CRITICAL: Refactor to use PreparedStatement with bind parameters.

---

### [P2-J83-F08] / [P4-UTILGZ-6.8]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: 86  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: 257-326  

Description: The `getLocalTime` method constructs SQL queries by concatenating `webUserCD` directly into the query string at line 288 without parameterization. This is a critical SQL injection vulnerability in time conversion code that processes user credentials. An attacker could inject malicious SQL to bypass authentication or extract sensitive data. Additionally, the method performs complex dealer date format logic (lines 276-298) with multiple conditional branches that are completely untested.

Fix: Add comprehensive test suite: (1) Test SQL injection attempts with malicious `webUserCD` values; (2) Test super admin path (SessionVar.isSuperAdmin = true) separately from normal user path; (3) Test with null/empty webUserCD; (4) Test when dealer date format is null or empty; (5) Test the fallback date format logic; (6) Mock database responses for various scenarios; (7) CRITICAL: Refactor to use PreparedStatement with bind parameters.

---

## au_excel/xlsx_curr_unit_report.jsp

### [P1-P02-F01] / [P1-A16-1]

**FleetFocus:** File: au_excel/xlsx_curr_unit_report.jsp | Line: 29-57  
**FleetIQ:**    File: au_excel/xlsx_curr_unit_report.jsp | Line: 31–57  

Description: The entire session-based access level control block in `xlsx_curr_unit_report.jsp` is commented out (lines 31–57). This means any authenticated user can download the Current Unit Report Excel file for any customer, bypassing tenant isolation. The `access_level`, `access_cust`, `access_site`, and `access_dept` session attributes are never applied to the data query.

Fix: // Lines 31-57 — entire access control block commented out: // 	String access_level = (String)session.getAttribute("access_level"); // 	String access_cust=(String)session.getAttribute("access_cust"); // 	String access_site=(String)session.getAttribute("access_site"); // 	String access_dept=(String)session.getAttribute("access_dept"); // 	if(access_level.equalsIgnoreCase("")) // 	{ // 		access_level = "5"; // 	} // 	int al = Integer.parseInt(access_level); // 	filter.setAccess_level(access_level); // 	filter.setAccess_cust(access_cust); // 	filter.setAccess_site(access_site); // 	filter.setAccess_dept(access_dept);

---

### [P2-P02-F14] / [P1-A16-1]

**FleetFocus:** File: au_excel/xlsx_curr_unit_report.jsp | Line: 29-57  
**FleetIQ:**    File: au_excel/xlsx_curr_unit_report.jsp | Line: 28-57  

Description: All session-based access control code is commented out (lines 28-57). The JSP generates reports with NO authorization checks, allowing any authenticated user to view all customer data regardless of their access level. This is a severe security vulnerability enabling unauthorized data access.

Fix: IMMEDIATELY uncomment and enable the access control code (lines 28-57). Create comprehensive tests that: (1) verify unauthorized users cannot access the report, (2) validate filter configuration properly restricts data by customer/site/department, (3) test that access_level enforcement works correctly, (4) add regression tests to prevent this code from being disabled again. This requires urgent remediation.

---

## (repository-wide)

### [P2-P17-F07] / [P2-A01-1a]

**FleetFocus:** File: (repository-wide) | Line:   
**FleetIQ:**    File: (Repository-wide) | Line: N/A  

Description: Repository-wide search revealed zero test infrastructure. No JUnit, TestNG, Selenium, or any other testing framework is present. No test directories exist. This means the entire application has zero automated test coverage, making it impossible to catch regressions, verify security fixes, or ensure code quality through CI/CD.

Fix: Establish comprehensive testing infrastructure: (1) Add JUnit or TestNG for Java unit tests, (2) Add Selenium WebDriver or similar for JSP/web integration tests, (3) Create test directory structure (e.g., src/test/java/), (4) Configure build tool (Maven/Gradle) for test execution, (5) Implement CI/CD pipeline with mandatory test execution, (6) Set code coverage targets and enforce them. Start with critical paths (authentication, authorization, data access) and expand coverage systematically.

---

## WEB-INF/src/com/torrent/surat/fms6/bean/LicenseBlackListBean.java

### [P2-J08-F01] / [P2-A02-3]

**FleetFocus:** File: LicenseBlackListBean.java | Line: 13-16  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/bean/LicenseBlackListBean.java | Line: 1-85 (entire class)  

Description: The `LicenseBlackListBean` class contains security-critical access control fields (`access_level`, `access_cust`, `access_site`, `access_dept`) and is used for driver license blacklist management, but has zero test coverage. This bean is used by `DriverImportDAO` to control access permissions and blacklist enforcement. Without tests, there is no verification that access control data is properly initialized (all fields default to `null`), validated, or protected from manipulation. The `vehicleCds` ArrayList could also be set to null, causing NullPointerExceptions in consuming code.

Fix: Create comprehensive unit tests covering: 1. Bean initialization with null defaults for access control fields 2. Getter/setter validation for all security-sensitive fields 3. Null safety tests for the `vehicleCds` ArrayList 4. Serialization/deserialization if the bean is persisted or transmitted 5. Boundary tests for date format in `expiryDate` field 6. Integration tests with `DriverImportDAO` to verify access control enforcement

---

## WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java

### [P1-J66-F03] / [P2-A15-05]

**FleetFocus:** File: Frm_saveuser.java | Line: 4119, 4199, 4268, 4298, 4310, 1535, 1612, 2838  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line:   

Description: User passwords are received from the HTTP request as plaintext strings and stored directly into the database column `PASSWORD` in `FMS_USR_MST` and `FMS_CUST_MST` with no hashing, salting, or encryption applied. There is no call to any digest, hash, or encoding function. This affects `save_user`, `save_driver`, `save_customer`, `save_customer_new`, and `saveDealer`. String password=request.getParameter("pass")==null?"":request.getParameter("pass"); // ... queryString="Insert into \"FMS_USR_MST\" (\"USER_CD\",\"USER_NAME\",\"USER_DESC\",\"PASSWORD\",...) " + "values ('"+user_cd+"','"+user_nm+"','"+user_desc+"','"+password+"',..."; stmt.executeUpdate(queryString); String password=request.getParameter("pass")==null?"":request.getParameter("pass"); // ... queryString="Insert into \"FMS_USR_MST\" (...,\"PASSWORD\",...) " + "values (...,'"+password+"',..."; stmt.executeUpdate(queryString);

Fix: Implement password hashing (bcrypt) before storage; remove plaintext password retrieval; add password strength validation and constant-time comparison.

---

## WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java

### [P1-J73-F01] / [P1-A04-02]

**FleetFocus:** File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 219  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 220  

Description: A plaintext FTP password is hardcoded directly in the Java source at line 220 inside the `firmware` action branch. The string `"FTPF=fms.fleetiq360.com,211,firmware,Sdh79HfkLq6,/firmware/FW_LMII_2_10_59_GEN2_DISPLAY_AUTO_CAM/FleetMS.bin"` is assigned to a local variable named `message` and then written to the database `outgoing` table to be transmitted to devices. The password `Sdh79HfkLq6` is committed to version control in plain text. This same password appears in `RuntimeConf.java` at line 28 (`public static String firmwarepass = "Sdh79HfkLq6";`) confirming it is a real operational FTP credential.

Fix: // CustomUpload.java line 220 String message = "FTPF=fms.fleetiq360.com,211,firmware,Sdh79HfkLq6,/firmware/FW_LMII_2_10_59_GEN2_DISPLAY_AUTO_CAM/FleetMS.bin"; // RuntimeConf.java line 28 (corroborating evidence) public static String firmwarepass = "Sdh79HfkLq6";

---

## WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java

### [P1-J78-F03] / [P2-A20-06]

**FleetFocus:** File: ImportFiles.java | Line: 49-2300  
**FleetIQ:**    File: WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java | Line: 47–65  

Description: The `ImportFiles` servlet (`/servlet/Import_Files`) handles driver, vehicle, question, canrule, service, and licence file imports. There is no authentication check anywhere in `doPost`. The servlet does not verify that `request.getSession()` contains a valid, authenticated user before processing the import. Any unauthenticated HTTP client that can reach the servlet URL can import or overwrite driver and vehicle records.

Fix: // ImportFiles.java line 47-65 — doPost begins, no session auth check protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException { log.info("requested src:" + request.getParameter("src") ...); response.setContentType("text/html;charset=UTF-8"); Part filePart       = request.getPart("file"); String fileName     = getFileName(filePart); String appPath      = request.getServletContext().getRealPath(""); String src          = request.getParameter("src")==null?"":request.getParameter("src"); String customer     = request.getParameter("customer")==null?"":request.getParameter("customer"); // No: request.getSession(false) null-check, no session attribute lookup, no role check

---

