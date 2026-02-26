# FleetFocus (ff-new) Audit Action Plan

**Audit Date**: 2026-02-25
**Run**: 01
**Branch**: release/UAT_RELEASE_FLEETFOCUS_Production
**Generated**: 2026-02-26

## Summary (to be filled after all passes)

| Severity | Count |
|----------|-------|
| CRITICAL | — |
| HIGH     | — |
| MEDIUM   | — |
| LOW      | — |
| INFO     | — |
| **Total**| — |

---

## Pass 1: Security Findings

### ff-new-inventory
No findings. (Repository inventory file -- informational only.)

### web-xml

[A01-1] CRITICAL | File: WEB-INF/web.xml | Line: N/A (absence)
Description: No <login-config> element defined -- no container-managed authentication; all resources accessible without auth challenge.
Fix: Add <login-config> with FORM auth-method, pair with <security-role> and <auth-constraint> on all protected resources.

[A01-2] HIGH | File: WEB-INF/web.xml | Line: 136-165
Description: No <auth-constraint> or <security-role> defined -- all servlet endpoints (/servlet/*) are accessible without authentication or role checks.
Fix: Define security roles (user, admin) and apply auth-constraints to /servlet/*, /pages/*, /gps/*, /reports/*, /dyn_report/*, /linde_reports/*.

[A01-3] HIGH | File: WEB-INF/web.xml | Line: 131-133
Description: No <cookie-config> in <session-config> -- JSESSIONID lacks HttpOnly and Secure flags; no COOKIE tracking-mode set, allowing URL-based session ID exposure.
Fix: Add <cookie-config> with <http-only>true</http-only> and <secure>true</secure>; add <tracking-mode>COOKIE</tracking-mode>.

[A01-4] HIGH | File: WEB-INF/web.xml | Line: 146-165
Description: /gps/*, /reports/*, /dyn_report/*, /linde_reports/* explicitly set to transport-guarantee NONE; /servlet/* has no transport constraint at all -- credentials and data can transit in cleartext.
Fix: Add <transport-guarantee>CONFIDENTIAL</transport-guarantee> to all functional paths; remove sensitive paths from the NONE constraint.

[A01-5] MEDIUM | File: WEB-INF/web.xml | Line: N/A (absence)
Description: No CSRF filter defined -- state-changing servlets (user mgmt, file uploads, fleet data) are unprotected against cross-site request forgery.
Fix: Integrate OWASP CSRFGuard or equivalent CSRF filter mapped to /servlet/*.

[A01-6] MEDIUM | File: WEB-INF/web.xml | Line: N/A (absence)
Description: No custom error pages configured -- default container error pages expose stack traces, class names, and container version info.
Fix: Add <error-page> elements for 400, 403, 404, 500 and java.lang.Exception with safe custom pages.

[A01-7] HIGH | File: WEB-INF/web - Copy.xml | Line: 7-17
Description: Stale backup descriptor in WEB-INF contains unauthenticated JavaMelody monitoring filter mapped to /* with zero security constraints; uses older Servlet 2.3 DTD.
Fix: Delete web - Copy.xml immediately; if JavaMelody needed, add to active web.xml with admin role restriction and HTTPS enforcement.

### properties-files

[A02-1] CRITICAL | File: WEB-INF/src/ESAPI.properties | Line: 130-131
Description: Encryptor.MasterKey and Encryptor.MasterSalt are commented out -- ESAPI falls back to publicly known default values, breaking all encryption guarantees.
Fix: Generate application-specific key/salt via ESAPI tool, store in secrets manager, rotate any data encrypted with defaults.

[A02-2] HIGH | File: WEB-INF/src/log4j2.properties | Line: N/A (absent property)
Description: log4j2.formatMsgNoLookups=true not set -- no defence-in-depth against Log4Shell (CVE-2021-44228) at configuration layer.
Fix: Add log4j2.formatMsgNoLookups=true; verify deployed log4j version is 2.17.1+; consider removing JndiLookup class from JAR.

[A02-3] HIGH | File: WEB-INF/src/ESAPI.properties | Line: 311; WEB-INF/src/log4j.properties | Line: 25; WEB-INF/src/log4j2.properties | Line: 12
Description: Development/wrong-environment paths hardcoded (C:\ESAPI\testUpload, /home/gmtp/logs/linde.log) -- expose server structure and likely fail on production OS.
Fix: Replace with environment-variable references or deployment-time substitution tokens; externalize per-environment config.

[A02-4] HIGH | File: WEB-INF/src/ESAPI.properties | Line: 493
Description: Validator.HTTPURL regex is ^.*$ -- accepts any URL string, effectively disabling URL validation (SSRF, javascript: URI risk).
Fix: Replace with restrictive pattern allowing only http/https schemes.

[A02-5] MEDIUM | File: WEB-INF/src/ESAPI.properties | Line: 480
Description: Validator.Redirect is ^\/test.*$ -- unmodified placeholder value that only permits /test paths, indicating open-redirect validation not properly configured.
Fix: Replace test with actual application context path; verify redirect validation is applied at every redirect point.

[A02-6] HIGH | File: WEB-INF/src/log4j2.properties | Line: 22
Description: rootLogger.level set to debug in production -- DEBUG logging exposes SQL queries, session IDs, internal details, and PII.
Fix: Set rootLogger.level to warn or error for production; use info only for specific named loggers.

[A02-7] MEDIUM | File: WEB-INF/src/ESAPI.properties | Line: 400
Description: Logger.LogEncodingRequired=false -- log output encoding disabled, enabling log injection/forging attacks.
Fix: Set Logger.LogEncodingRequired=true.

[A02-8] LOW | File: WEB-INF/src/ESAPI.properties | Line: 43
Description: ESAPI.printProperties=true -- prints all ESAPI configuration to logs on startup, leaking security config.
Fix: Set ESAPI.printProperties=false in production.

[A02-9] HIGH | File: WEB-INF/src/ESAPI.properties | Line: 314-315
Description: ForceHttpOnlySession=false and ForceSecureSession=false -- session cookie lacks HttpOnly and Secure attributes, vulnerable to XSS theft and network interception.
Fix: Set both HttpUtilities.ForceHttpOnlySession=true and HttpUtilities.ForceSecureSession=true.

[A02-10] MEDIUM | File: WEB-INF/src/ESAPI.properties | Line: 367
Description: FileUploadAllowAnonymousUser=true -- unauthenticated users can upload files, creating DoS and access control gaps.
Fix: Set to false unless anonymous upload is a documented requirement with rate-limiting controls.

[A02-11] MEDIUM | File: WEB-INF/src/ESAPI.properties | Line: 344
Description: MaxUploadFileBytes=500000000 (500MB) -- excessively large for document/image uploads; combined with anonymous uploads enables 10GB/request DoS.
Fix: Reduce to 10-25MB; implement per-user quotas and rate limiting.

[A02-12] LOW | File: WEB-INF/src/ESAPI.properties | Line: 398
Description: Logger.ApplicationName=ExampleApplication -- default placeholder not customized, preventing proper log correlation in SIEM.
Fix: Set to FleetFocus or deployment-specific name.

[A02-13] INFO | File: WEB-INF/src/validation.properties | Line: 27-28
Description: CreditCard and SSN validation regex rules present -- indicates potential PCI DSS and PII regulatory scope.
Fix: Confirm whether validators are actively used; if credit card/SSN data is processed, ensure PCI/PII compliance; remove if unused.

[A02-14] MEDIUM | File: WEB-INF/src/ESAPI.properties | Line: 448-450
Description: ValidationException intrusion detection rule commented out -- rapid validation failures (scans/attacks) will not trigger detection.
Fix: Uncomment and activate the ValidationException rule; tune thresholds based on traffic patterns.

### security-java

[A03-1] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 58-59, 72-73
Description: SQL queries in doPost concatenate the login parameter directly into SQL strings with no sanitisation -- full SQL injection on authentication endpoint.
Fix: Replace Statement with PreparedStatement and bind login parameter; or delete Frm_login.java if unused and remove its web.xml mapping.

[A03-2] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 78-81
Description: Password retrieved from DB and compared with plain .equals() -- implies plaintext password storage; no bcrypt, not timing-safe.
Fix: Migrate to BCrypt.checkpw() as in Frm_security.java; ensure DB stores bcrypt hashes not plaintext.

[A03-3] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 97-100
Description: Failed login logs both submitted password and database password in cleartext to application log.
Fix: Remove password and pass_word from log statement; log only username, failure type, IP, session ID.

[A03-4] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 66
Description: doPost dispatcher unconditionally logs raw password request parameter at INFO level on every request.
Fix: Remove password parameter from the log statement.

[A03-5] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 2053
Description: chk_login logs both submitted password and database password in cleartext on failed login.
Fix: Remove password and pass_word from log statement.

[A03-6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 1167-1175, 1890-1898, 1946
Description: Session ID not invalidated/rotated after successful authentication -- session fixation vulnerability.
Fix: Call request.getSession().invalidate() then request.getSession(true) before setting any post-auth session attributes.

[A03-7] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 1496-1497
Description: Fallback query to user_reset_password concatenates user_cd directly into SQL string (second-order injection risk).
Fix: Use PreparedStatement with bound parameter for user_cd.

[A03-8] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 2196-2199
Description: reset_password concatenates username request parameter directly into SQL -- SQL injection on password reset endpoint.
Fix: Convert to PreparedStatement with bound parameters for USER_NAME and EMAIL_ADDR.

[A03-9] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 2226-2231
Description: reset_password insert/update concatenates userId and temp password into SQL strings.
Fix: Use PreparedStatement with bound parameters for all insert/update operations.

[A03-10] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 2359-2378
Description: change_password concatenates user_cd (from request param) and password into SQL; uses quote-doubling instead of parameterization; stores password in plaintext for AU/MLA.
Fix: Use PreparedStatement; hash with BCrypt; source user_cd from session not request parameter.

[A03-11] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 2435-2458
Description: chg_bms_pass uses MD5 for BMS password hashing via SQL concatenation; user_cd and cpass concatenated into SQL.
Fix: Replace MD5 with BCrypt; use PreparedStatement; source user_cd from session.

[A03-12] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 1583-1586
Description: AU/MLA password check uses plain .equals() with ESAPI encoding -- implies plaintext password storage for these sites.
Fix: Migrate AU/MLA passwords to BCrypt; run one-time hash migration; use BCrypt.checkpw().

[A03-13] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 1600, 1974, 1203
Description: user_cd exposed as plain query parameter in redirect URLs after login -- leaks internal user ID in browser history and Referer headers.
Fix: Store user_cd in session; have changepass.jsp retrieve it from session instead of URL parameter.

[A03-14] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 2347, 2420, 2520
Description: change_password and chg_bms_pass accept user_cd from request parameter -- allows authenticated user to change another user's password (IDOR).
Fix: Source user_cd from session attribute instead of request parameter; verify match before update.

[A03-15] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/security/GetGenericData.java | Line: 21-26
Description: Connection, Statement, ResultSet declared as servlet instance fields -- shared across concurrent requests causing thread-safety / data leakage issues.
Fix: Declare all DB state as local variables within handler methods.

[A03-16] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java | Line: 29-141
Description: Frm_login.java has no session fixation protection, no brute-force protection, no CSRF validation -- bypasses all controls in Frm_security.java.
Fix: Remove Frm_login servlet mapping from web.xml and delete the file; or apply same protections as Frm_security.

[A03-17] LOW | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 1420-1421
Description: ESAPI HTML-encoding applied to password before BCrypt comparison -- transforms special characters, potentially causing auth failures or weakening password space.
Fix: Pass raw password directly to BCrypt.checkpw() without HTML encoding.

[A03-18] LOW | File: WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java | Line: 57-141
Description: No CSRF token validation on login endpoint -- enables login CSRF attacks.
Fix: Implement CSRF synchronizer token on login form; consider framework-level CSRF filter.

[A03-19] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/security/Databean_security.java | Line: 158-179+
Description: Multiple query methods concatenate field values (sourced from HTTP request params) directly into SQL strings.
Fix: Convert all query methods to PreparedStatement with bound parameters.

### gps-jsps

[A11-1] CRITICAL | File: gps/unit.gps.jsp | Line: 1-6
Description: GPS location JSON endpoint has no session authentication check -- any unauthenticated request can retrieve real-time vehicle GPS data for any customer.
Fix: Add Expire.jsp include; validate ccd parameter against session access_cust.

[A11-2] CRITICAL | File: gps/gpsZonesData.jsp | Line: 1-5
Description: GPS zone boundary data endpoint has no session authentication -- unauthenticated requests can retrieve zone configurations for any customer.
Fix: Add Expire.jsp include; validate ccd against session access_cust.

[A11-3] CRITICAL | File: gps/setGpsZones.jsp | Line: 1-36
Description: GPS zone write endpoint has no authentication and no CSRF token -- unauthenticated POST can create/modify geofence zones for any customer.
Fix: Add Expire.jsp include; validate ccd against session; implement CSRF token.

[A11-4] HIGH | File: gps/Copy of gpsZonesData.jsp | Line: entire file
Description: Stale backup file (Windows "Copy of" naming) deployed to production with identical vulnerabilities to gpsZonesData.jsp -- expands attack surface.
Fix: Delete from production; add build check to reject Copy of * patterns.

[A11-5] HIGH | File: gps/speedZones_back.jsp | Line: entire file
Description: Backup copy of speedZones.jsp deployed to production (uses old Google Maps API) -- unnecessary attack surface.
Fix: Delete from production; use version control for history.

[A11-6] HIGH | File: gps/gpsWhereIAm.jsp | Line: 290; gps/speedZones.jsp | Line: 276
Description: Authenticated users can manipulate user_cd parameter to access GPS data for other customers -- no cross-customer validation at JSP level.
Fix: Assert user_cd matches session access_cust before calling filter.init().

[A11-7] MEDIUM | File: gps/gpsWhereIAm.jsp | Line: 452; gps/speedZones.jsp | Line: 431
Description: Request parameter form_cd echoed to hidden HTML field without encoding -- reflected XSS.
Fix: HTML-encode form_cd with ESAPI.encoder().encodeForHTML() before output.

[A11-8] MEDIUM | File: gps/gpsWhereIAm.jsp | Line: 403, 412, 427, 437; gps/speedZones.jsp | Line: 390-425
Description: DB-sourced strings (customer names, vehicle names, etc.) output unescaped to HTML option elements -- stored XSS risk.
Fix: Wrap all <%= %> DB-sourced outputs with HTML encoding utility.

[A11-9] MEDIUM | File: gps/gpsWhereIAm.jsp | Line: 638-641; gps/ajaxSendStore.js | Line: 849-858
Description: DB values (unit.name, unit.model, unit.time) interpolated unescaped into HTML strings in JavaScript InfoWindow -- DOM-based XSS.
Fix: HTML-encode DB values before JS interpolation; use DOM methods instead of string concatenation.

[A11-10] MEDIUM | File: gps/gpsZonesData.jsp | Line: 41, 45-47
Description: Zone names and IDs from DB embedded unescaped into XML attribute values -- XML injection risk.
Fix: Apply XML attribute encoding; validate lat/lon are numeric; use XML library instead of string concat.

[A11-11] MEDIUM | File: gps/gpsWhereIAm.jsp | Line: 16-18; gps/speedZones.jsp | Line: 16-22
Description: External JS/CSS libraries loaded over HTTP (not HTTPS) including outdated jQuery UI 1.8.21 and Leaflet 0.7.3 -- MITM and known CVE risk.
Fix: Switch to HTTPS; upgrade to current versions; bundle locally with SRI hashes.

[A11-12] LOW | File: gps/gpsWhereIAm.jsp | Line: 17; gps/speedZones.jsp | Line: 17
Description: Google Maps API key (AIzaSyCOyV9n_Yz5bcNNJfvvbAgZc016ThnFhFM) present in commented-out source code.
Fix: Remove key from source; rotate in Google Cloud Console; manage via environment variables.

### dao

[A05-1] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/BatteryDAO.java | Line: 32-44, 365, 400
Description: All 5 methods concatenate from/to date strings, unitList, and vcd into SQL via Statement -- full SQL injection across battery reports.
Fix: Replace all Statement/concatenation with PreparedStatement; bind timestamps, validate unitList is numeric.

[A05-2] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java | Line: 35-550
Description: 7+ methods concatenate cust_cd, loc_cd, dept_cd, userId, usercd, vehtype into SQL -- SQL injection across driver operations.
Fix: Use PreparedStatement throughout with typed bindings (setInt, setString, setTimestamp).

[A05-3] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java | Line: 29-1186
Description: 10+ methods concatenate fname, lname, licence, compId, id, url into SQL -- SQL injection on free-text name fields, file URLs, and IDs.
Fix: Use PreparedStatement for all queries; setString for text, setInt for IDs.

[A05-4] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/ImpactDAO.java | Line: 71-1058
Description: All methods concatenate cust_cd, loc_cd, dept_cd, date strings, and unitlst into SQL -- SQL injection across all impact report queries.
Fix: Use PreparedStatement; bind timestamps as java.sql.Timestamp; validate unitlst elements are numeric.

[A05-5] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java | Line: 108-1650
Description: saveQuestions, saveQuestionsTab, saveDriverInfo concatenate free-text fields (question text, names, codes) into INSERT/UPDATE SQL.
Fix: Use PreparedStatement with individual setString/setInt bindings for all columns.

[A05-6] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java | Line: 62-63
Description: init() concatenates fid directly into SQL with no sanitization -- SQL injection via form code parameter.
Fix: Use PreparedStatement; bind fid; replace SELECT * with explicit column names.

[A05-7] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java | Line: 45-293
Description: getChecks and getCheckSummary concatenate date strings and entity IDs into SQL -- SQL injection on pre-check report endpoints.
Fix: Use PreparedStatement; validate from/to date formats; parse entity IDs as integers.

[A05-8] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java | Line: 474, 284, 294
Description: checkDupComp concatenates company name into ILIKE SQL; register concatenates user_nm into SELECT -- SQL injection on self-registration.
Fix: Use PreparedStatement with ? placeholder for ILIKE and SELECT queries.

[A05-9] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java | Line: 68-558
Description: All methods concatenate filter parameters (cust_cd, loc_cd, dept_cd, model_cd) into SQL -- high-leverage injection point used as building block by other DAOs.
Fix: Validate all filter params as numeric integers; rewrite with PreparedStatement and array-type IN clauses.

[A05-10] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java | Line: 32-181
Description: 5 lookup methods concatenate ID parameters directly into SQL; form_cd injectable via single-quote.
Fix: Use PreparedStatement; validate RuntimeConf.form_table against allowlist.

[A05-11] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java | Line: 31-62
Description: All 3 query methods concatenate custCd, locCd, deptCd, vehTypeCd, langChoice into SQL.
Fix: Use PreparedStatement; accept Connection instead of Statement to create own PreparedStatement objects.

[A05-12] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java | Line: 472
Description: getDriverById fetches driver record by bare ID with no customer/tenant filter -- cross-tenant data access.
Fix: Add AND comp_id = ? with session customer ID as bound parameter.

[A05-13] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java | Line: 1069, 1111
Description: getDriverName and getDriverNameLinde look up any user by ID with no tenant check -- cross-tenant enumeration.
Fix: Add comp_id/cust_cd filter parameter; join through FMS_USER_DEPT_REL for Linde variant.

[A05-14] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java | Line: 62
Description: init() queries mnt_msg by FORM_CD with no customer filter -- potential cross-tenant message disclosure.
Fix: Add customer filter if table is per-customer; use PreparedStatement; replace SELECT * with explicit columns.

[A05-15] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java | Line: 550
Description: getDriverNameById returns any user's full name with no tenant scoping -- violates data isolation.
Fix: Add cust_cd filter via join to FMS_USER_DEPT_REL.

[A05-16] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java | Line: 511-518
Description: checkAuthority embeds RuntimeConf.username and RuntimeConf.password in SQL string; uses MD5; credentials appear in query logs on exception.
Fix: Compare credentials in application code with constant-time comparison and modern hash; remove SQL-based MD5 pattern.

[A05-17] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java | Line: 885-918
Description: Finally block entirely commented out -- Statement and ResultSet objects never closed; will exhaust DB cursors under load.
Fix: Restore finally block; use try-with-resources for all DB resources.

[A05-18] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java | Line: 162-196
Description: Unused PreparedStatement ps declared but never assigned (dead code); ResultSets closed inline without finally guard.
Fix: Consolidate cleanup into finally blocks or use try-with-resources; remove unused ps.

[A05-19] LOW | File: Multiple DAO files | Line: various
Description: Full SQL query strings (containing user data and schema) printed to stdout/stderr on exception via e.printStackTrace() and System.out.println.
Fix: Replace with structured logging; do not log SQL strings in production; fix no-op e.getMessage() calls.

### master-java

[A06-1] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 54; WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java | Line: 69
Description: Neither servlet verifies authenticated session before processing -- unauthenticated access to all user/customer/vehicle CRUD operations and file uploads.
Fix: Add session authentication guard at start of doPost; consider servlet filter for all protected URLs.

[A06-2] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 4138, 4279-4281
Description: Access level for new users taken directly from HTTP parameter "al" -- any user can create admin accounts via privilege escalation.
Fix: Cap assignable access level to caller's own level from session; never trust access level from client input.

[A06-3] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 4135, 5016, 10788
Description: Customer/tenant scope for all write operations set from request parameters, not session -- cross-tenant data modification possible.
Fix: Validate request cust_cd against session access_cust before executing any tenant-scoped write.

[A06-4] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: multiple; Databean_customer.java | Line: multiple
Description: Every SQL statement built by string concatenation of request parameters -- pervasive SQL injection across all CRUD operations.
Fix: Replace all SQL concatenation with PreparedStatement and bound parameters.

[A06-5] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java | Line: 115-137
Description: File upload has no type/extension validation, writes to web root (/images/pics/), no size limit, no auth -- enables remote code execution via JSP upload.
Fix: Move upload dir outside web root; validate MIME type with Tika; enforce extension whitelist; set size limit; add auth.

[A06-6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java | Line: 131-136
Description: Uploaded filename only stripped of backslash paths; forward-slash traversal (../../) can write files to arbitrary server locations.
Fix: Use Paths.get(name).getFileName(); verify canonical path starts with upload directory.

[A06-7] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 54; Frm_upload.java | Line: 69
Description: No CSRF token validation on any of 40+ state-changing operations -- all vulnerable to cross-site request forgery.
Fix: Implement synchronizer token pattern; generate per-session CSRF token; validate in every doPost.

[A06-8] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 4119, 4199, 4268, 5022
Description: Passwords received as plaintext HTTP params and stored directly in DB with no hashing -- only single-quote escaping for SQL syntax.
Fix: Hash all passwords with BCrypt before storage; never store or log plaintext passwords.

[A06-9] LOW | File: Multiple master package files | Line: various
Description: Wildcard imports (java.sql.*, java.util.*, java.lang.reflect.*, etc.) obscure class scope and complicate security review.
Fix: Replace wildcard imports with explicit named imports.

[A06-10] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 35
Description: Deprecated SingleThreadModel serialises all requests; instance-level fields for per-request state cause performance bottleneck and potential race conditions.
Fix: Move per-request state to local variables; remove SingleThreadModel.

### bean-java

[A07-1] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/bean/SFTPSettings.java | Line: 8, 26
Description: SFTP password stored as plain String with public getter -- no encryption at rest or in memory; exposed if bean is logged/serialized/rendered.
Fix: Store encrypted in DB; do not expose raw credential via getter; use separate credential-fetch path.

[A07-2] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/bean/NetworkSettingBean.java | Line: 3-5, 30-34
Description: WiFi pre-shared key stored in Serializable bean with public getter -- will be written to disk in plaintext if session is persisted/replicated.
Fix: Mark password field as transient; do not implement Serializable for beans with credentials; clear after use.

[A07-3] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/bean/LockOutBean.java, SuperMasterAuthBean.java, SiteConfigurationBean.java | Line: multiple
Description: Master override codes, super-master bypass codes, and physical access card values stored in plain String fields with full getters in Serializable beans.
Fix: Mark sensitive fields as transient; fetch on demand from secure store; never log or render in views.

[A07-4] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 557-980
Description: Bean contains full DAO logic with all queries built by string concatenation -- SQL injection via form_cd, veh_cd, set_cust_cd, date strings, and access_cust.
Fix: Replace all Statement usage with PreparedStatement; extract DB logic from bean into proper DAO layer.

[A07-5] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java | Line: 3-51
Description: Primary user bean has no customer_id/tenant scoping field -- application relies on separate mechanisms for tenant isolation, increasing cross-tenant risk.
Fix: Add custCd field; populate from DB at login; enforce as authoritative tenant source in all data access.

[A07-6] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DriverImportBean.java | Line: 5-31
Description: Serializable bean stores PII (licence number, phone, card number) alongside access-control fields without transient marking or data minimisation.
Fix: Mark PII fields as transient; separate access-control fields into distinct class; avoid session-scoped PII storage.

[A07-7] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 86, 527-532
Description: Public setter for is_user_admin Boolean flag -- if bean is populated from HTTP params, attacker can POST is_user_admin=true for admin-level data access.
Fix: Remove public setter; derive admin flag from authenticated session role only.

[A07-8] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 735
Description: Hardcoded customer exclusion (USER_CD!=103) in admin query -- undocumented privileged treatment.
Fix: Replace with configurable exclusion list or table flag; document business reason.

[A07-9] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 118-126, 543-561
Description: testQueries method left in production code, invocable via opCode="test_queries" -- executes raw stored procedure calls.
Fix: Remove testQueries method and its dispatch branch from production code.

[A07-10] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 39-41; ServiceDueFlagBean.java | Line: 131-133
Description: Debug System.out.println leaks SQL queries and internal data to server stdout/logs.
Fix: Replace with structured logging; never log full SQL in production.

[A07-11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/LockOutBean.java | Line: 5, 17, 49-54
Description: Serializable bean stores master_code (vehicle unlock override) in plain String -- exposed in session serialization.
Fix: Mark master_code as transient; encrypt if session storage needed; prefer on-demand retrieval.

[A07-12] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java | Line: 5, 29-31
Description: Serializable bean stores facility_code and super_card (physical access credentials) -- exposed in session serialization.
Fix: Mark both fields as transient; ensure they are not rendered in browser-visible HTML output.

### excel-pdf-java

[A09-1] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java | Line: 32, 70, 107, 144, 180-181
Description: 5 lookup methods concatenate user-supplied parameters directly into Statement queries -- SQL injection on all report lookups.
Fix: Replace all Statement with PreparedStatement and bind parameters.

[A09-2] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java | Line: 71, 145, 229-250, 437-512, 583-810
Description: 10+ queries in chart DAO use Statement with string concatenation of custCd, locCd, dates, and derived values -- SQL injection throughout chart generation.
Fix: Migrate all queries to PreparedStatement with ? placeholders; validate IN-clause elements.

[A09-3] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java | Line: 91-100; all report classes
Description: No customer isolation check in report export layer -- cust_cd accepted from caller without session validation; cross-tenant data export via IDOR.
Fix: Read cust_cd from session only; verify requested cust_cd/loc_cd/dept_cd against user's access rights before SQL.

[A09-4] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java | Line: 159-162
Description: Output file path derived from form_cd parameter via SQL-injectable getFormName() -- path traversal can write files to arbitrary locations.
Fix: Fix SQL injection in getFormName(); validate rpt_name to alphanumeric only; canonicalize output path.

[A09-5] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java | Line: 27-33, 49
Description: cust_cd and loc_cd embedded directly in chart file path without sanitisation -- path traversal possible.
Fix: Sanitise cust_cd/loc_cd to alphanumeric only; enforce canonical path check within chart directory.

[A09-6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java | Line: 26-60, 95-127
Description: Customer/location/department names from DB embedded in HTML email body without encoding -- HTML injection/XSS in emails.
Fix: HTML-encode all dynamic values before embedding in HTML email bodies.

[A09-7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java | Line: 925-935
Description: Duration string embedded in setCellFormula() without validation -- formula injection risk if value contains formula characters.
Fix: Validate totalDuration against strict HH:MM:SS regex before formula construction; fallback to setCellValue().

[A09-8] MEDIUM | File: All 70+ report classes in excel/ | Line: various
Description: XSSFWorkbook never closed after write across all report generators -- memory and file descriptor leak under load.
Fix: Add wb.close() in finally block or use try-with-resources.

[A09-9] INFO | File: ReportPDF.java, MonthlyPDFRpt.java | Line: N/A
Description: No external process invocation found in PDF generation -- command injection check clear.
Fix: No action required.

[A09-10] INFO | File: chart/*.java | Line: N/A
Description: No external process invocation found in chart generation -- command injection check clear.
Fix: No action required.

[A09-11] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/DriverAccessAbuseDAO.java | Line: 7, 11
Description: Duplicate import statement -- low code hygiene indicator.
Fix: Remove duplicate import.

[A09-12] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java | Line: 13-25; ExcelImpactReport.java | Line: 191
Description: Hardcoded HTTP (not HTTPS) production URL in source -- MITM risk for email recipients and environment portability issue.
Fix: Move hostnames to configuration property; use https:// for all URLs.

### security-jsps

[A10-1] CRITICAL | File: pages/index.jsp | Line: 18-20
Description: Arbitrary file inclusion via request parameter -- page parameter used in jsp:include without validation, enabling path traversal to include any JSP/file on the server.
Fix: Validate page parameter against a whitelist of allowed JSP paths; reject any value containing ../ or absolute paths.

[A10-2] CRITICAL | File: security/output.jsp | Line: 87-110
Description: SQL injection -- lines from D:/reset.csv file concatenated directly into SQL UPDATE/INSERT statements without parameterisation.
Fix: Remove or gate these operational scripts; use parameterised queries exclusively.

[A10-3] CRITICAL | File: security/threshold_par.jsp | Line: 97-127
Description: SQL injection -- same pattern as output.jsp; lines from D:/PAR_messages.log concatenated into SQL statements.
Fix: Remove or gate; use parameterised queries.

[A10-4] CRITICAL | File: security/output.jsp, security/threshold_par.jsp | Line: 16-165
Description: No session check or authentication -- unauthenticated access to destructive database operations (UPDATE, INSERT on vehicle/messaging tables).
Fix: Remove from web-accessible directory or add strong authentication and authorisation checks.

[A10-5] CRITICAL | File: pages/checker.jsp | Line: 9, 24-30
Description: Authentication bypass -- accepts user_cd from request parameter and directly sets session attributes (user_cd, access_level, access_cust), enabling session hijacking without password.
Fix: Never accept user_cd from request params for session setup; only set auth attributes after credential verification; invalidate/regenerate session.

[A10-6] HIGH | File: pages/login.jsp | Line: 641
Description: XSS in JavaScript context -- value parameter HTML-encoded via ESAPI but embedded in JS string literal where single quotes and backslashes are not encoded.
Fix: Use encodeForJavaScript() instead of encodeForHTML() for JS string context.

[A10-7] HIGH | File: pages/login.jsp | Line: 403
Description: Stored XSS -- database status message from MessageDao output unescaped on login page visible to all users.
Fix: Escape msg with encoder.encodeForHTML() before rendering.

[A10-8] HIGH | File: security/auto_change_pass.jsp | Line: 154
Description: Reflected XSS -- message request parameter echoed directly into HTML without escaping.
Fix: HTML-encode message before output.

[A10-9] HIGH | File: security/frm_change_pass.jsp | Line: 157
Description: Reflected XSS -- message parameter reflected without escaping into password change page.
Fix: HTML-encode message before output.

[A10-10] HIGH | File: security/frm_access_rights.jsp | Line: 277, 444-445
Description: Reflected XSS -- cust_cd and gp_cd from request params embedded unescaped in JS onLoad; message reflected unescaped in HTML.
Fix: Use encodeForJavaScript() for JS context; encodeForHTML() for HTML context.

[A10-11] HIGH | File: security/frm_add_mail_group.jsp | Line: 129
Description: Stored XSS -- DB group codes/names embedded unescaped in JavaScript onclick handler.
Fix: Apply encodeForJavaScript() to values in JS string arguments.

[A10-12] HIGH | File: security/frm_add_mail_group_pop.jsp | Line: 122
Description: Stored XSS -- DB group name, code, customer code unescaped in JS onclick handler.
Fix: Apply encodeForJavaScript() to all JS context values.

[A10-13] HIGH | File: security/frm_edit_mail_list.jsp | Line: 224
Description: Stored XSS -- email addresses from DB embedded in JS onclick handler; single quotes in emails break JS context.
Fix: Apply encodeForJavaScript() to values in JS function calls.

[A10-14] HIGH | File: security/frm_form_priority.jsp | Line: 314, 318
Description: Stored XSS -- form codes from DB embedded unescaped in JS onclick handlers.
Fix: Apply encodeForJavaScript() or validate form codes are strictly numeric.

[A10-15] HIGH | File: pages/changepass.jsp | Line: 17
Description: Reflected XSS -- lastUpdate request parameter rendered unescaped into HTML.
Fix: HTML-encode lastUpdate before rendering; validate date format server-side.

[A10-16] HIGH | File: All security/frm_*.jsp files and pages/changepass.jsp | Line: multiple
Description: No CSRF tokens on any state-changing form -- password change, access rights, mail groups, modules all vulnerable to CSRF.
Fix: Implement synchroniser token pattern across all forms.

[A10-17] HIGH | File: security/get_form_data.jsp, get_mail_data.jsp, get_module_data.jsp | Line: all
Description: AJAX data endpoints have no authentication -- unauthenticated enumeration of forms, email addresses, and modules.
Fix: Add Expire.jsp session check to all three endpoints.

[A10-18] MEDIUM | File: pages/login.jsp | Line: 85-95
Description: No session regeneration on login -- session ID not invalidated before setting auth attributes; session fixation risk.
Fix: Call session.invalidate() then getSession(true) before setting authentication attributes.

[A10-19] MEDIUM | File: pages/login.jsp | Line: 101-123
Description: Password stored in browser cookie -- password cookie persists on client, transmitted with every request, vulnerable to XSS/network interception.
Fix: Remove password cookie; implement remember-me with cryptographically random single-use token.

[A10-20] MEDIUM | File: security/output.jsp, security/threshold_par.jsp | Line: 46
Description: Hardcoded absolute filesystem paths (D:/reset.csv, D:/PAR_messages.log) -- server path disclosure and operational dependency.
Fix: Remove operational scripts from web-accessible directory.

[A10-21] MEDIUM | File: sess/Expire.jsp | Line: 20
Description: Weak session guard -- NullPointerException risk if session null after forward; only checks user_cd attribute, not verified auth flag.
Fix: Add return after forward; supplement with explicit authentication flag check.

[A10-22] MEDIUM | File: pages/changepass.jsp | Line: 56-74
Description: Password policy enforced client-side only via JavaScript -- trivially bypassable.
Fix: Enforce all password policy rules server-side independently of client validation.

[A10-23] MEDIUM | File: pages/checker.jsp | Line: 32-41
Description: Open redirect -- message parameter concatenated unescaped into redirect URL.
Fix: URL-encode message parameter; validate redirect targets within application domain.

### dashboard

[A17-1] HIGH | File: dashboard/jsp/summary.jsp | Line: 254-256
Description: Request parameters cust_cd, loc_cd, dept_cd interpolated into JavaScript block without type-checking or encoding -- reflected XSS via DOM.
Fix: Enforce Integer.parseInt() server-side; emit only numeric result; or use encodeForJavaScript().

[A17-2] MEDIUM | File: dashboard/jsp/header_filter.jsp | Line: 3-4; dashboard/jsp/header_vor_status.jsp | Line: 3-4
Description: Request parameters mnm and sub reflected into HTML input value attributes without encoding -- reflected XSS.
Fix: Use ESAPI encodeForHTMLAttribute() or JSTL c:out.

[A17-3] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Summary.java, Config.java, CriticalBattery.java, Impacts.java, Licence.java, Preop.java, TableServlet.java, Utilisation.java | Line: multiple
Description: Every SQL query in dashboard package built by string concatenation of unsanitised request parameters -- pervasive SQL injection.
Fix: Replace all Statement with PreparedStatement; bind all filter params as typed parameters.

[A17-4] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java | Line: 29, 59, 75-91
Description: Static cusList field shared across all threads -- race condition causes one user's customer list to overwrite another's, exposing cross-tenant data.
Fix: Remove static shared field; execute session-scoped queries per request; store per-session.

[A17-5] HIGH | File: dashboard/jsp/summary.jsp | Line: 5-7; Summary.java all methods
Description: cust_cd accepted from request parameter with no session-scope verification -- authenticated user can access any tenant's data.
Fix: Verify cust_cd is in authenticated user's permitted customer set before executing queries.

[A17-6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java | Line: 168
Description: Session attribute user_cd concatenated directly into SQL without parameterization.
Fix: Use PreparedStatement with ? placeholder; parse user_cd as integer.

[A17-7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Licence.java | Line: 47-53
Description: init() pre-loads ALL customers, sites, and departments with no access-level restriction -- full cross-tenant topology loaded eagerly.
Fix: Remove init() pre-load or scope to per-request queries using authenticated user's permissions.

[A17-8] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/TableServlet.java | Line: 37; Utilisation.java | Line: 49-52
Description: Instance-level mutable fields (rsList, vehicles, oneDay) shared across concurrent requests -- race condition and cross-user data leakage.
Fix: Move to local method variables; never store per-request data in servlet instance fields.

[A17-9] LOW | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/SessionCleanupListener.java | Line: 21-29
Description: Session cleanup only calls Impacts.cleanupSession; CriticalBattery, Preop, Utilisation, Licence maps never cleaned -- memory leak.
Fix: Add missing cleanupSession() calls for all four servlet classes.

[A17-10] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Licence.java | Line: 198-233
Description: SQL injection + broken authorization + PII exposure -- cust_cd from request concatenated into queries returning driver names, emails, phone numbers, licence data.
Fix: Use PreparedStatement; validate cust_cd against session; restrict PII columns returned.

### util-database

[A04-01] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 19-20, 30, 54-55, 87-89
Description: Eight plaintext credentials hardcoded in source: FTP passwords (firmware/ciifirmware, Sdh79HfkLq6), test account (TestK/testadmin), Clickatell SMS API (collintell/fOqDVWYK/3259470).
Fix: Remove all credential literals; load from env vars or secrets manager; rotate all exposed credentials immediately.

[A04-02] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 219
Description: FTP connection string with password Sdh79HfkLq6 hardcoded as string literal and stored in DB in plaintext.
Fix: Remove hardcoded credential; read from secrets store; rotate FTP password.

[A04-03] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: 86, 196, 251, 305
Description: Four public methods concatenate userCd, webUserCD, custCd into SQL -- SQL injection in utility class used throughout application.
Fix: Replace all with PreparedStatement using ? placeholders.

[A04-04] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: 67, 73-94
Description: DELETE statements concatenate cust_cd and driver_cd; gdpr_data from DB used in interval expression -- second-order injection on destructive operations.
Fix: Use PreparedStatement; validate gdpr_data as integer in expected range; use make_interval() function.

[A04-05] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java | Line: 76, 104, 108
Description: Client IP address, logindate, logintime, userid concatenated into UPDATE SQL -- fires on every login; X-Forwarded-For is attacker-controlled.
Fix: Use PreparedStatement; validate IP format; never trust X-Forwarded-For without proxy config.

[A04-06] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java | Line: 39-40, 49-50, 54-55, 65-66, 107
Description: All public methods concatenate user, loc_cd, cust_cd, dept_cd, access_user into SQL including INSERT to message queue.
Fix: Use PreparedStatement for all queries; validate access_user against session.

[A04-07] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java | Line: 42-100
Description: callMigrateMaster iterates over lists concatenating customer/location/department/user codes into SELECT, DELETE, INSERT, UPDATE.
Fix: Use PreparedStatement; validate all codes are numeric.

[A04-08] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: 121-177
Description: fix_dept concatenates user_cd, loc_cd, dept_cd into 10+ queries affecting department tables -- injection corrupts relational data.
Fix: Use PreparedStatement; validate all parameters are numeric.

[A04-09] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java | Line: 59, 64-65
Description: Security audit log writelog() parses msg string and concatenates components into SELECT/INSERT -- corrupting the audit log itself.
Fix: Use PreparedStatement; validate each component; restructure to accept typed parameters.

[A04-10] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/mail.java | Line: 63
Description: Ename() concatenates userid directly into SQL to resolve email addresses -- SQL injection on notification path.
Fix: Use PreparedStatement; validate userid is numeric.

[A04-11] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java | Line: 73, 77
Description: fetchform_rights/fetchSubModule concatenate set_user_cd and module into SQL.
Fix: Use PreparedStatement; validate set_user_cd as numeric; whitelist module codes.

[A04-12] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean1.java | Line: 69, 73
Description: Same SQL injection as Menu_Bean.java in the variant class.
Fix: Use PreparedStatement; validate inputs.

[A04-13] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: multiple
Description: Background alert dispatcher concatenates veh_cd, gmtp_id, rec_no, freq into queries -- executes in privileged server context.
Fix: Audit each query in call_mail.java individually and replace all with PreparedStatement; ensure the background job's database user has only minimum required privileges (SELECT/UPDATE on specific tables, no DDL).

[A04-14] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Line: 45, 79, 85, 115, 124, 147, 207, 248
Description: checkDueDate/getAlertlist concatenate cust, site, vehicle/inspection values into SQL; email INSERT concatenates email, subsject, message -- second-order injection.
Fix: Use PreparedStatement for all queries; parameterise email INSERT bindings for email, subsject, message.

[A04-15] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Line: 43-50, 81-85, 144
Description: checkExpiry() builds dynamic extra filter by concatenating cust_cd, loc_cd, dept_cd; email INSERT also concatenates without parameterisation.
Fix: Replace dynamic extra filter with parameterised conditions using conditional setString() calls; parameterise email INSERT.

[A04-16] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Line: 64-70, 125, 143, 161
Description: Same extra filter pattern as A04-15 for cust_cd, loc_cd, dept_cd; email INSERTs at lines 125, 143, 161 concatenate email, subsject, message.
Fix: Same as A04-15.

[A04-17] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java | Line: 206-212
Description: resyncPreop splits vehTCds by | to extract vehType, customer, location, department -- all concatenated into query strings without validation.
Fix: Use PreparedStatement; validate customer, location, department as numeric and vehType against expected pattern.

[A04-18] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Line: 84, 100, 229
Description: checkFirmware concatenates gmtp_id, vt_cd, cust_cd, site_cd, dept_cd into SELECTs; FTP command at line 229 embeds hardcoded RuntimeConf.firmwarepass.
Fix: Use PreparedStatement for all queries; remove hardcoded firmware password from FTP command string (see A04-01).

[A04-19] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java | Line: 24, 83
Description: getHTML/getHTML1 concatenate urlToRead and param to form URL and open HTTP connection -- SSRF if callers pass user-controlled values.
Fix: Validate urlToRead against an allowlist of permitted hosts and schemes; reject file://, ftp://, and non-approved hosts.

[A04-20] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 329-343, 919, 937
Description: saveImage opens new URL(imageUrl) directly (SSRF); uploadLicenceFile constructs path from filename without canonicalisation; uploadDocumentFile uses cust_loc in path allowing traversal.
Fix: Validate imageUrl against allowlist; after constructing File, call getCanonicalPath() and assert result starts with expected base directory; reject filename/cust_loc containing .. or path separators.

[A04-21] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java | Line: 85
Description: doPost extracts fileName from Content-Disposition header without path traversal validation -- attacker can write to arbitrary server paths.
Fix: Strip directory component using new File(fileName).getName(); verify getCanonicalPath() is within upload directory; reject filenames containing /, \, or ..

[A04-22] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 77
Description: Same path traversal as A04-21 -- fileName from multipart header written to path without sanitisation.
Fix: Same as A04-21: use new File(fileName).getName() and validate canonical output path.

[A04-23] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java | Line: N/A (entire class)
Description: Trivial character-substitution cipher with no key, no salt, no computational cost -- deterministic and reversible; used by password_life.java to "encrypt" passwords.
Fix: Replace with bcrypt, Argon2, or PBKDF2 (min 100k iterations, random per-user salt); force password reset for all users after migration since substitution output can be decoded to recover plaintext.

[A04-24] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java | Line: 69-70
Description: Email INSERT concatenates email, subsject, message read from FMS_USR_MST -- second-order injection if stored values contain SQL metacharacters.
Fix: Use PreparedStatement for the INSERT; migrate UPDATE at line 72 to PreparedStatement for consistency.

[A04-25] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java | Line: 225
Description: ORDER BY built by concatenating sort_str and sort_ord -- currently safe (switch-controlled) but fragile pattern.
Fix: Document intent; ensure sort columns always resolved through switch; consider enum-based approach; migrate surrounding query to PreparedStatement.

[A04-26] LOW | File: Multiple (UtilBean.java, mail.java, InfoLogger.java, GdprDataDelete.java, GetHtml.java, others)
Description: Wildcard imports (java.sql.*, javax.sql.*, etc.) obscure which SQL classes are in use and increase class-name collision risk.
Fix: Replace wildcard imports with explicit imports; serves as forcing function to identify all SQL class usage during A04-03 through A04-18 remediation.

### pages-jsps

[A15-1] HIGH | File: pages/login.jsp | Line: 403
Description: DB-sourced notification message (msg) rendered without HTML encoding on login page -- stored XSS if attacker can set message content.
Fix: Replace <%=msg %> with <%=ESAPI.encoder().encodeForHTML(msg) %>; ESAPI already imported on this page.

[A15-2] MEDIUM | File: pages/login.jsp | Line: 641
Description: Request parameter val is ESAPI HTML-encoded then placed in JS string literal -- HTML encoding insufficient for JS context.
Fix: Use encoder.encodeForJavaScript(value) instead of encodeForHTML; alternatively whitelist-validate value as only "0", "1", or "logout".

[A15-3] HIGH | File: pages/manage_form.jsp, pages/admin/SpecialAdminRights.jsp | Line: manage_form.jsp:1, SpecialAdminRights.jsp:2
Description: Only session existence checked (Expire.jsp) -- no admin access_level check; any authenticated user can access form management and special admin rights pages.
Fix: Add explicit role check after session guard: if (!access_level.equalsIgnoreCase("1")) redirect to access_denied.jsp.

[A15-4] HIGH | File: Multiple admin pages (customer/view.jsp, user/edit-general.jsp, edit-website-access.jsp, my_profile.jsp, manage_form.jsp, menu-new.jsp, menu.jsp, others)
Description: DB-sourced values (names, emails, addresses, form names, module names) rendered via <%= %> with no HTML encoding across all admin pages -- stored XSS.
Fix: Apply ESAPI.encoder().encodeForHTML() to all DB-sourced expressions; for HTML attributes use encodeForHTMLAttribute(); consider global find-and-replace pass on all JSPs.

[A15-5] HIGH | File: All state-changing forms (manage_form.jsp, add-general.jsp, edit-general.jsp, edit-website-access.jsp, edit-general.jsp, my_profile.jsp, change_password.jsp, SpecialAdminRights.jsp)
Description: Zero CSRF tokens found across all JSP forms -- every state-changing POST (user create/edit, password change, customer edit, form management, special admin rights) is vulnerable.
Fix: Implement Synchronizer Token Pattern: generate random token at session creation, include as hidden field in every POST form, validate server-side; consider OWASP CSRFGuard.

[A15-6] HIGH | File: pages/admin.jsp | Line: 119-145
Description: mnm and sub request parameters concatenated directly into file path for jsp:include -- no whitelist, no path canonicalization, no .. rejection.
Fix: Whitelist permitted mnm/sub values; alternatively resolve from DB-registered page list; add canonical path check ensuring result starts with /pages/admin/.

[A15-7] MEDIUM | File: pages/admin.jsp | Line: 144
Description: Permission check short-circuits when form_cd parameter is null -- any authenticated user can access any admin sub-page by omitting form_cd.
Fix: Reverse logic to deny by default: require form__cd != null AND permission check passes; reject when form_cd is absent.

[A15-8] HIGH | File: pages/admin.jsp | Line: 55, 159-172
Description: form_cd request parameter injected into JS variable without encoding (line 55); message parameter rendered raw into swal() call (lines 159-172) -- reflected XSS.
Fix: Use ESAPI.encoder().encodeForJavaScript() for both values; validate form_cd as numeric integer.

[A15-9] MEDIUM | File: layout/header.jsp | Line: 169
Description: Session user_fnm/user_lnm rendered in top nav without HTML encoding -- stored XSS if name contains HTML characters; also in change_password.jsp line 25.
Fix: Apply ESAPI.encoder().encodeForHTML(fnm+" "+lnm) in header.jsp; same for change_password.jsp.

[A15-10] LOW | File: pages/admin/customer/view.jsp | Line: 66
Description: filter.getDebug() output rendered to browser -- may expose SQL queries, exceptions, or implementation details.
Fix: Remove debug output line from production JSP; write debug info to server-side logs only.

[A15-11] MEDIUM | File: pages/manage_form.jsp | Line: 7-30, 61-113
Description: Complete list of all modules, form paths, form codes exposed to any authenticated user (no admin check) -- aids attacker reconnaissance and path traversal.
Fix: Add admin access check (see A15-3); consider whether form paths need browser exposure or can be referenced by opaque IDs.

[A15-12] HIGH | File: pages/admin/reports/mod/mail_report.jsp | Line: 2-5, 20
Description: url request parameter appended to LindeConfig.emailurl and fetched server-side via GetHtml.getHTML1() -- SSRF to internal network resources.
Fix: Validate url against strict whitelist of permitted report page paths (alphanumeric only, no slashes/dots); use numeric ID resolved server-side to pre-approved path list.

### reports-dashboard-java

[A08-1] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/reports/Reports.java | Line: 63, 124, 127, 191, 200, 276-285
Description: Base class Fetch_customers/Fetch_cust_locations/Fetch_cust_depts/Fetch_cust_veh concatenate session/request values into SQL via Statement -- pattern propagates to all report subclasses.
Fix: Replace all Statement usage with PreparedStatement and bind parameters; applies to all four methods and every subclass.

[A08-2] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java | Line: throughout (21,854 lines)
Description: Hundreds of stmt.executeQuery(query) calls concatenating set_cust_cd, set_loc_cd, set_dept_cd, st_dt, to_dt, set_sc, access_dept into SQL; zero PreparedStatement usage.
Fix: Full refactor to PreparedStatement; bind dates as Timestamp objects, not SQL string literals.

[A08-3] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java | Line: 154, 173-174, 188, 245-246
Description: Fetch_users/Fetch_Data concatenate set_gp_cd, set_user_cd, st_dt, end_dt into SQL; no customer scope enforcement -- any user can query any driver's data.
Fix: Use PreparedStatement; enforce set_user_cd belongs to authenticated session's customer.

[A08-4] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java | Line: throughout (10,015 lines)
Description: set_dept_cd, set_loc_cd, set_cust_cd, set_sc, dynamic field codes concatenated into SQL via Statement throughout entire file.
Fix: Full refactor to PreparedStatement; validate dynamic field codes against whitelist before interpolation.

[A08-5] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java | Line: 155-164, 168, 210, 235-244, 296-302, 814, 866, 908-909
Description: access_cust, access_site, access_dept, set_cust_cd, set_gmtp_id concatenated into SQL; GPS data query at 908-909 particularly dangerous (cross-customer location data exposure).
Fix: Use PreparedStatement; prioritise GPS query at lines 908-909.

[A08-6] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/reports/LinderReportDatabean.java | Line: 216-217, 338-339, 426-427, 524, 570, 633, 715-717, 818-820
Description: customerCd, locationCd (split on - and each part concatenated), st_dt, end_dt embedded directly into PostgreSQL timestamp expressions.
Fix: Use PreparedStatement with setTimestamp() for dates; parameterise customerCd and locationCd.

[A08-7] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java | Line: 41-44, 168
Description: Shared utility reads cust, site, dept from req.getParameter() and concatenates unquoted into SQL condition used by ALL dashboard servlets; saveasList() executes any raw SQL.
Fix: Refactor Config to return parameterised query fragment with ? placeholders and bound value list; validate integer parameters.

[A08-8] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Summary.java | Line: 100-101, 196
Description: Multiple handlers concatenate cust_cd, loc_cd, dept_cd, st_dt, to_dt from request into SQL; dates in PostgreSQL timestamp literals.
Fix: Use PreparedStatement; bind integers via setInt(), dates via setTimestamp().

[A08-9] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Impacts.java | Line: 111, 171-172, 187-199
Description: cust, startTime, endTime from request concatenated into SQL; dates also in generate_series() expressions enabling interval manipulation.
Fix: Use PreparedStatement with setTimestamp(); validate cust as integer.

[A08-10] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/TableServlet.java | Line: 109, 304-309, 374-375, 380-395
Description: search in ILIKE without escaping; DB-returned field_cd/name interpolated back into second query (second-order injection); startTime, endTime, drivers concatenated.
Fix: Use PreparedStatement with setString() for ILIKE (prepend/append % in Java); validate field_cd as integer whitelist; sanitise column alias names to alphanumeric.

[A08-11] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/CriticalBattery.java, Licence.java, Preop.java, Utilisation.java
Description: All four dashboard servlets concatenate cust, site, dept, startTime, endTime from request into SQL -- identical pattern to Summary/Impacts.
Fix: Same as A08-8/A08-9; refactor shared Config.java parameterised builder to eliminate duplication.

[A08-12] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java | Line: 24-25, 37-38, 50-51, 66-69, 75-77
Description: UNION ALL query concatenates custCd, locCd, deptCd, searchCrit, vehTypeCd; Pattern check on searchCrit is incomplete mitigation.
Fix: Use PreparedStatement for entire query; remove partial pattern-check; bind each parameter properly.

[A08-13] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java | Line: 209-211, 332-334, 467-470, 524, 570
Description: customerCd, locationCd, st_dt, end_dt from request concatenated into SQL; locationCd split on - and each fragment separately concatenated.
Fix: Refactor to PreparedStatement; validate cust_cd matches authenticated session's customer in BusinessInsight.java.

[A08-14] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/Config.java + all dashboard servlets
Description: cust_cd, loc_cd, dept_cd read directly from request with no verification against session's authorised scope -- any user can query any customer's data by supplying another customer code.
Fix: Validate request parameters against session's authorised customer/site/dept list on every request; reject mismatched scope.

[A08-15] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/RTLSImpactReport.java | Line: 981-986
Description: getRTLSVehLst() returns vehicles without customer scope filter -- getRedImpact() then fetches impact data for unscoped vehicle list exposing cross-customer data.
Fix: Add customer scope filter (AND "USER_CD" = ?) to getRTLSVehLst() and all impact queries.

[A08-16] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dashboard/SessionCleanupListener.java
Description: Only Impacts.cleanupSession() called on session destroy; CriticalBattery, Licence, Preop, Utilisation session-cached data not cleaned -- memory leak and potential data exposure.
Fix: Add cleanup calls for all session-caching servlets; or use HttpSession.setAttribute() for per-session data so container handles cleanup.

[A08-17] LOW | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java, Databean_cdisp.java
Description: Wildcard imports (java.sql.*, java.util.*) obscure Statement vs PreparedStatement usage during code review.
Fix: Replace with explicit imports during SQL injection remediation.

[A08-18] LOW | File: All reports/dashboard/service/businessinsight files
Description: Every file uses e.printStackTrace() as sole error handling -- may expose stack traces with class names, schema details, file paths.
Fix: Replace with log.error("message", e) using existing log4j Logger; configure servlet container to suppress raw stack traces in HTTP responses.

### dependencies

[A18-1] CRITICAL | File: WEB-INF/lib/commons-collections-3.1.jar | CVE: CVE-2015-6420, CVE-2015-7501
Description: Deserialization gadget chain (InvokerTransformer/ChainedTransformer) enables RCE via any endpoint that deserializes untrusted data.
Fix: Upgrade to commons-collections 3.2.2 or 4.4; audit all Java deserialization points; deploy ObjectInputFilter (jep290).

[A18-2] CRITICAL | File: WEB-INF/lib/commons-fileupload-1.1.jar | CVE: CVE-2014-0050, CVE-2016-1000031
Description: DoS via multipart boundary headers (CVE-2014-0050); RCE via DiskFileItem deserialization writing arbitrary files (CVE-2016-1000031). Actively used by Frm_upload and CustomUpload servlets.
Fix: Upgrade to commons-fileupload 1.5+; also upgrade commons-io-1.1.jar to 2.11.0+.

[A18-3] HIGH | File: WEB-INF/lib/poi-3.9-*.jar (3 JARs) | CVE: CVE-2014-9527, CVE-2017-5644, CVE-2019-12415
Description: XXE in OOXML processing (attacker-supplied Office documents read server files); DoS via HSSf records. Import_Files servlet accepts uploaded documents.
Fix: Upgrade all three POI JARs to 5.2.5+; apply XMLInputFactory external entity protections; validate file content type on upload.

[A18-4] HIGH | File: WEB-INF/lib/httpclient-4.2.3.jar, httpcore-4.2.2.jar | CVE: CVE-2014-3577, CVE-2020-13956
Description: SSL hostname verification bypass (MITM on outbound HTTPS); request URI miscategorization enabling SSRF.
Fix: Upgrade to HttpClient 4.5.14 or 5.3; upgrade HttpCore together.

[A18-5] HIGH | File: WEB-INF/lib/dom4j-1.6.1.jar | CVE: CVE-2018-1000632, CVE-2020-10683
Description: XML injection via Element text (CVE-2018-1000632); XXE by default when parsing attacker-supplied XML (CVE-2020-10683).
Fix: Upgrade to dom4j 2.1.4+; as interim disable external entity resolution on SAXReader.

[A18-6] HIGH | File: WEB-INF/lib/itextpdf-5.4.2.jar | CVE: CVE-2017-7386, CVE-2018-10036
Description: SSRF via XMLWorker (crafted XML triggers outbound requests); DoS via malformed PDF; AGPL-3.0 license compliance risk.
Fix: Upgrade to iText 7.x (commercial) or migrate to Apache PDFBox 3.x (Apache 2.0); minimum safe is iText 5.5.13.3.

[A18-7] HIGH | File: WEB-INF/lib/batik-*.jar (4 JARs) | CVE: CVE-2019-17566, CVE-2022-38648, CVE-2022-40146, CVE-2022-44729, CVE-2022-44730
Description: Multiple SSRF vulnerabilities via crafted SVG files exploiting image href, jar: URL scheme, and data: URIs.
Fix: Upgrade all four Batik JARs to 1.17+; sanitize SVG content from untrusted sources before transcoding.

[A18-8] MEDIUM | File: WEB-INF/lib/gson-2.8.5.jar | CVE: CVE-2022-25647
Description: Stack overflow DoS via deeply nested JSON objects in JsonElement.deepCopy() and TypeAdapter deserialization.
Fix: Upgrade to Gson 2.10.1+.

[A18-9] MEDIUM | File: WEB-INF/lib/commons-logging.jar + commons-logging-1.1.1.jar
Description: Duplicate JARs (v1.1 and v1.1.1); Eclipse compiles against 1.1 but Tomcat may load 1.1.1 -- classpath split between build and runtime.
Fix: Remove commons-logging.jar (v1.1); retain only commons-logging-1.1.1.jar; consider upgrading to 1.3.x.

[A18-10] MEDIUM | File: WEB-INF/lib/commons-net-1.4.1.jar + commons-net-2.0.jar
Description: Duplicate JARs; Eclipse compiles against 2.0 but Tomcat loads 1.4.1 (alphabetical) -- API breaking changes between versions cause potential NoSuchMethodError at runtime.
Fix: Remove both; replace with single commons-net 3.9.0.

[A18-11] MEDIUM | File: N/A (build system absent)
Description: No pom.xml, build.gradle, or build.xml -- IDE-only build prevents automated CVE scanning, version pinning, transitive dependency management, reproducible builds.
Fix: Migrate to Maven or Gradle; immediately run OWASP Dependency-Check standalone against WEB-INF/lib/.

[A18-12] MEDIUM | File: WEB-INF/lib/junit-3.8.1.jar
Description: Test framework JAR in production WEB-INF/lib/ -- increases attack surface, exposes test infrastructure classes.
Fix: Remove junit-3.8.1.jar from WEB-INF/lib/ immediately.

[A18-13] HIGH | File: N/A (Tomcat container -- version unknown)
Description: web.xml declares Servlet 3.0 (min Tomcat 7.0); Tomcat 7/8.0/8.5 all EOL; if deployed on these, unpatched CVEs including GhostCat (CVE-2020-1938, CVSS 9.8).
Fix: Determine Tomcat version via catalina.sh version; upgrade to Tomcat 10.1.x or at minimum 9.0.99+.

[A18-14] HIGH | File: WEB-INF/lib/xmlbeans-2.3.0.jar | CVE: CVE-2021-23926
Description: XXE injection (CVSS 9.1) -- XMLBeans before 3.0.0 does not disable external entity resolution; used by poi-ooxml internally.
Fix: Upgrade to XMLBeans 5.1.1+; coordinate with POI upgrade (A18-3).

[A18-15] HIGH | File: WEB-INF/lib/postgresql-8.3-603.jdbc4.jar | CVE: CVE-2022-21724
Description: EOL driver (2013); no modern TLS support; class injection via loggerLevel/loggerFile connection properties (CVSS 9.8).
Fix: Upgrade to PostgreSQL JDBC 42.7.x -- drop-in replacement for standard JDBC4 code.

[A18-16] MEDIUM | File: WEB-INF/lib/charts4j-1.3.jar
Description: Sends fleet operational data (metrics, driver activity, vehicle data) to Google Charts API (deprecated March 2019) -- outbound data leakage to third-party.
Fix: Replace with JFreeChart (already present) or Chart.js; remove charts4j-1.3.jar; keep all chart data server-side.

[A18-17] LOW | File: WEB-INF/lib/javamelody.jar
Description: Monitoring endpoint exposes request stats, SQL queries, JVM state, session data; not in active web.xml but JAR loaded by classloader -- risk if inadvertently activated.
Fix: Remove javamelody.jar if not needed; if needed add authentication via allowed-addr-pattern; remove stale web - Copy.xml.

[A18-18] LOW | File: WEB-INF/lib/jsoup-1.12.1.jar | CVE: CVE-2021-37714, CVE-2022-36033
Description: XSS sanitizer bypass via Unicode characters (CVE-2021-37714) and crafted HTML (CVE-2022-36033).
Fix: Upgrade to Jsoup 1.17.2+.

[A18-19] INFO | File: WEB-INF/lib/log4j-api-2.17.0.jar, log4j-core-2.17.0.jar | CVE: CVE-2021-44832 (low risk)
Description: Log4Shell patched (2.17.0 fixes CVE-2021-44228/45046/45105); CVE-2021-44832 requires attacker config write access (low practical risk). log4j.properties suggests possible Log4j 1.x config.
Fix: Upgrade to Log4j 2.24.x; audit log4j.properties to confirm Log4j 1.x not active.

### executables-sql-misc

[A19-1] HIGH | File: executables/gmtp_outgoing_queue/gmtp_outgoing_queue.sh | Line: 26, 31
Description: Hardcoded GMTP management interface credentials (username: gmtp, password: gmtp!telnet) in plaintext in version control.
Fix: Rotate password immediately; move credentials to environment variable or secrets manager; purge from git history via git filter-repo or BFG.

[A19-2] LOW | File: executables/gmtp_outgoing_queue/gmtp_outgoing_queue.sh | Line: 9-11
Description: Three internal staff email addresses hardcoded in monitoring script.
Fix: Move alert recipients to environment variable or external config file excluded from version control.

[A19-3] MEDIUM | File: sql/fleetfocus-schema-apr02-2025-dump.sql, sql/fleetfocus-schema-apr02-2025-update.sql
Description: Full production PostgreSQL schema dumps committed to repo -- exposes all table definitions, function bodies, sequences, constraints, plperlu extensions, db owner username.
Fix: Remove schema dumps from repo and git history; maintain sanitized DDL migration scripts instead; audit whether plperlu (untrusted PL/Perl) is required.

[A19-4] LOW | File: sql/adhoctask/April232024/UnwantedCustomerSitesDeletionWoolworths.sql
Description: Ad-hoc script names real customer (Woolworths), internal customer code (233), site IDs and names in comments -- data minimisation concern.
Fix: Anonymise customer identifiers in comments; evaluate moving adhoctask/ to separate access-controlled operations repo.

[A19-5] LOW | File: work/org/apache/jsp/pages/admin/setting/*.class, *.java
Description: Tomcat-compiled JSP class files and generated Java sources tracked by git despite /work/ in .gitignore (committed at initial import).
Fix: Run git rm --cached on all work/ files; verify with git ls-files work/.

[A19-6] INFO | File: WEB-INF/vssver2.scc (and ~19 others across repo)
Description: Visual SourceSafe binary metadata files committed at initial import -- expose legacy VSS project path structure.
Fix: Remove all vssver2.scc files via git rm; add vssver2.scc to .gitignore.

[A19-7] INFO | File: .gitattributes
Description: ~700-line file with per-file -text entries from VSS/SVN migration; confirms committed .class files and Excel reports; non-standard but no security-suppressive attributes found.
Fix: Replace per-file entries with generic type-based rules (*.class -text, *.jar -text); remove committed binary artifacts via git filter-repo.

### exporter-dyn-jsps

[A13-1] CRITICAL | File: linde_reports/linde_reports_subscription.jsp | Line: 58-73
Description: OS command injection -- rpt_name, email, cust_cd, loc_cd, st_dt, end_dt concatenated into ProcessBuilder /bin/sh -c command; shell metacharacters trivially exploitable; page has no authentication.
Fix: Authenticate endpoint; validate rpt_name against fixed allowlist of known report names; validate all params for format; replace shell invocation with direct Java API.

[A13-2] CRITICAL | File: linde_reports/linde_reports_subscription.jsp, red_impact.jsp, unit_utilisation.jsp; au_email/xlsx_daily_veh_summary_report_mail.jsp; dyn_report/email_dyn_unit_report_exc.jsp
Description: Five pages entirely missing Expire.jsp authentication guard -- unauthenticated access to data, OS commands, and email sending; email_dyn_unit_report_exc.jsp has session reads explicitly commented out.
Fix: Add <%@include file="../sess/Expire.jsp" %> as first statement on all pages; review all linde_reports/ and au_email/ for missing guards.

[A13-3] CRITICAL | File: dyn_report/email_vor_status_report.jsp, email_dyn_driver_report.jsp, email_dyn_seen_report.jsp, email_dyn_unit_report.jsp, email_dyn_unit_report_exc.jsp, email_vor_report.jsp
Description: Six email report pages hardcode access_level="1" and access_cust/site/dept="" instead of reading session -- any user gets admin-level cross-tenant data access.
Fix: Replace hardcoded values with session.getAttribute() reads as in correctly implemented export pages; audit backend queries for independent scope enforcement.

[A13-4] HIGH | File: dyn_report/excel_driver_league.jsp, email_driver_league.jsp, print_driver_league.jsp
Description: Three Driver League report pages don't read access_level/access_cust from session or call filter.setAccess_*() -- data scoping depends entirely on backend defaults.
Fix: Add session access control reads and filter.setAccess_*() calls matching correctly scoped pages; confirm backend enforcement.

[A13-5] HIGH | File: dyn_report/mail_report.jsp | Line: 19-70
Description: mail_id and subject from request passed to sendMail() without sanitisation (email header injection via newlines); url from request prepended to base URL (SSRF).
Fix: Validate mail_id against RFC 5322 format rejecting \r\n; strip newlines from subject; validate url against allowlist of known report JSP names.

[A13-6] HIGH | File: au_email/xlsx_daily_veh_summary_report_mail.jsp | Line: 85-136
Description: No authentication guard; mail_id from request passed to sendExcelReport() (email injection); mail_id reflected in HTML unescaped.
Fix: Add Expire.jsp; validate mail_id as valid email; strip \r\n before use.

[A13-7] HIGH | File: dyn_report/mail_conf.jsp | Line: 127, 242, 309, 314-319
Description: message parameter reflected unescaped in HTML; url, hour, min, st_time, to_time reflected in hidden input values without encoding -- reflected XSS.
Fix: HTML-encode all request parameters with ESAPI.encoder().encodeForHTML(); use encodeForHTMLAttribute() for attribute contexts.

[A13-8] HIGH | File: dyn_report/rpt_dyn_driver_report.jsp, rpt_dyn_seen_report.jsp, rpt_dyn_unit_report.jsp
Description: Request params (do_list, undo_list, sort_by, sort_asc, field_cd, field_nm, refresh_page_url) concatenated unescaped into JS onclick handler strings -- JS injection.
Fix: Apply encodeForHTMLAttribute() + encodeForJavaScript() for values in JS strings inside HTML attributes; or use data attributes read by JS.

[A13-9] HIGH | File: 8 linde_reports/ chart pages (red_impact.jsp, impact_by_unit_with_util.jsp, preop_complete.jsp, unit_utilisation.jsp, util_driver_all_models.jsp, util_driver_logon.jsp, national_preop_checks.jsp, nat2_util_driver_all_models.jsp)
Description: DB-sourced site names, model names, unit names concatenated unescaped into Highcharts JS config objects -- stored XSS if name contains JS metacharacters.
Fix: JavaScript-encode all DB-sourced strings with ESAPI.encoder().encodeForJavaScript(); or pass data as JSON via separate API call.

[A13-10] MEDIUM | File: dyn_report/mail_first.jsp, au_email/xlsx_daily_veh_summary_input_mail.jsp
Description: Request parameters (url, loc_nm, dept_nm, cust) reflected unescaped in hidden input value attributes -- reflected XSS via attribute breakout.
Fix: Encode all reflected values with encodeForHTMLAttribute().

[A13-11] MEDIUM | File: 7 email/print report pages (email_vor_status_report.jsp, email_dyn_driver_report.jsp, email_dyn_seen_report.jsp, email_dyn_unit_report.jsp, email_driver_league.jsp, print_driver_league.jsp, email_vor_report.jsp)
Description: DB-sourced strings (serial numbers, vehicle/driver names, notes, model names) inserted into HTML table cells via <%= %> without encoding -- stored XSS.
Fix: HTML-encode all DB-sourced values with ESAPI.encoder().encodeForHTML().

[A13-12] MEDIUM | File: dyn_report/get_dept.jsp, get_site.jsp | Line: 45
Description: DB department/site codes and names concatenated into XML string without XML-escaping -- XML injection if values contain <, >, &.
Fix: XML-encode DB values with StringEscapeUtils.escapeXml11() or use XMLOutputFactory API.

[A13-13] MEDIUM | File: dyn_report/mail_conf.jsp, mail_first.jsp, includes/report_nevigation.jsp, report_nevigation_keyword.jsp, report_nevigation_todate.jsp
Description: POST forms lack CSRF tokens -- attacker can trigger report subscriptions, email config changes, report generation via victim's session.
Fix: Implement synchroniser token pattern with per-session random token; validate server-side before processing.

[A13-14] MEDIUM | File: sess/Expire.jsp | Line: 10-29
Description: When session expired, forwards to login without calling session.invalidate() -- server-side session remains active; stolen session ID usable until container timeout.
Fix: Call session.invalidate() before jsp:forward; add return; after forward; consider replacing with response.sendRedirect().

[A13-15] MEDIUM | File: exporter/users.jsp, exporter/vehicles.jsp
Description: customer parameter from request passed to filter alongside session access controls -- if backend uses request customer as primary filter, cross-tenant export possible.
Fix: Validate requested customer matches access_cust when access_level doesn't grant cross-customer access; review DAO-layer queries.

[A13-16] LOW | File: linde_reports/linde_reports_subscription.jsp | Line: 92
Description: Date validation checks st_dt twice instead of st_dt and end_dt (copy-paste bug) -- malformed end_dt passes validation.
Fix: Correct second condition to check end_dt; secondary to A13-1 command injection fix.

[A13-17] INFO | File: linde_reports/linde_reports_subscription.jsp | Line: 62-65
Description: Windows code path hardcodes internal IP 192.168.10.47:8090 -- reveals internal network topology.
Fix: Move URL to RuntimeConf.emailurl configuration property; remove hardcoded IP from source.

### au-excel-print-jsps

[A16-1] CRITICAL | File: au_excel/xlsx_curr_unit_report.jsp | Line: 29-57
Description: Entire access-control block commented out (op_code, session reads, all filter.setAccess_* calls) -- filter.init() runs with no data-scope constraint; any authenticated user gets full cross-customer unit dataset.
Fix: Uncomment access-control block immediately; review git history for when/why it was commented out; verify filter output is scoped to session's access_cust.

[A16-2] HIGH | File: au_print/print_hire_dehire_report.jsp | Line: 93
Description: search_crit request parameter output unescaped into HTML <td>; file also has no session-expiry include.
Fix: HTML-encode search_crit; add standard authentication include.

[A16-3] HIGH | File: au_print/print_dyn_driver_report.jsp | Line: 156
Description: do_list, undo_list, sort_by, sort_asc from request injected unescaped into JS onclick attribute string -- JS injection.
Fix: JavaScript-encode values with escapeEcmaScript(); or use data attributes read by separate script block.

[A16-4] HIGH | File: All 29 au_print/ JSP files
Description: Pervasive unescaped DB-sourced output (vehicle names, driver names, model names, broadcast text, pre-op comments) via <%= %> across all print pages -- stored XSS.
Fix: Apply StringEscapeUtils.escapeHtml4() or JSTL <c:out> to all DB-sourced expressions; prioritise broadcast message text and pre-op comments.

[A16-5] HIGH | File: au_print/print_broadcastmsg.jsp
Description: Device/operator-submitted broadcast message text output directly into HTML without encoding -- highest-risk stored XSS input (field-operator-controlled content).
Fix: HTML-encode all broadcastmsgBean fields; validate/sanitise broadcast text at ingestion layer.

[A16-6] LOW | File: xlsx_driver_impact_report.jsp, xlsx_hire_dehire_report.jsp, xlsx_impact_meter_report.jsp, xlsx_impact_report.jsp, excel_hourmeter_exception.jsp
Description: Double Content-Type assignment; use of non-standard application/x-download MIME type; HTML served as application/vnd.ms-excel.
Fix: Set Content-Type once using correct MIME type; add X-Content-Type-Options: nosniff header.

[A16-7] MEDIUM | File: au_excel/excel_hourmeter_exception.jsp
Description: HTML-as-Excel export with unescaped DB values; accessible as HTML in browser creating stored XSS surface; form_cd request param in attribute unescaped.
Fix: Convert to genuine XLSX using POI; or HTML-encode all outputs and form_cd attribute value.

[A16-8] LOW | File: excel_hourmeter_exception.jsp, print_curr_driv_report.jsp, print_curr_unit_report.jsp, print_util_wow.jsp
Description: form_cd request parameter echoed unescaped in hidden input value attribute -- attribute breakout XSS.
Fix: Encode with escapeHtml4(form_cd) in attribute context.

[A16-9] MEDIUM | File: All 62 au_excel/ and au_print/ JSP files
Description: No JSP-layer check that caller-supplied user_cd/cust_cd matches session access_cust -- enforcement delegated entirely to filter bean SQL.
Fix: Add explicit check before filter.init(): if non-admin access_level and cust_cd != access_cust, return 403; or enforce in filter bean init().

[A16-10] MEDIUM | File: All au_excel/au_print/ files; critical in print_hire_dehire_report.jsp
Description: session.getAttribute("access_level") not null-checked before .equalsIgnoreCase() -- NPE on expired session; print_hire_dehire_report.jsp has no session-expiry include at all.
Fix: Add null check (if access_level == null, redirect to login); add Expire.jsp to print_hire_dehire_report.jsp; consider centralised servlet filter.

[A16-11] LOW | File: au_excel/xlsx_cimplicity_shock_report.jsp | Line: 85
Description: Content-Disposition filename from xlsxReport.getTitle() without sanitisation -- header injection if title contains newlines.
Fix: Sanitise filename to alphanumeric/hyphen/underscore/dot; wrap in double quotes per RFC 6266.

[A16-12] INFO | File: au_excel/xlsx_preop_chk_report_orig_no_fitler.jsp
Description: Debug/backup JSP with misspelled filename present in web root -- additional endpoint with potentially stale access controls.
Fix: Remove from web root; preserve in VCS only; exclude from deployed artifact.

[A16-13] LOW | File: au_excel/xlsx_util_wow_report.jsp
Description: filter.init() called twice on same bean with different op_codes in one request -- fragile state management.
Fix: Use distinct bean instances or refactor to support named result sets.

### reports-jsps

[A14-1] HIGH | File: All rpt_* display pages (26+ files in reports/)
Description: Pervasive unescaped DB output via <%= %> across all report pages -- no encoding mechanism found anywhere in reports/ directory; stored XSS via any configurable DB field.
Fix: Apply JSTL <c:out escapeXml="true"/> or StringEscapeUtils.escapeHtml4() to every <%= %> expression rendering DB data.

[A14-2] HIGH | File: rpt_unit_unlock.jsp, rpt_unit_unlock_impact.jsp, rpt_unit_unlock_question.jsp, rpt_imp_set_lst.jsp, rpt_override_code_lst.jsp, rpt_email_configuration_report.jsp, rpt_messages_status.jsp, mail_conf.jsp
Description: message request parameter reflected unescaped into HTML -- reflected XSS via crafted URL.
Fix: HTML-encode message before output; consider server-side flash message mechanism.

[A14-3] MEDIUM | File: rpt_impact_report.jsp, rpt_impact_photo_report.jsp
Description: search_crit request parameter reflected into input value attribute without encoding -- attribute breakout XSS.
Fix: HTML-encode search_crit in attribute context.

[A14-4] HIGH | File: rpt_user_summary.jsp | Line: 113-128
Description: sort_flg request parameter reflected directly into JS onclick handler -- JS injection via sort_flg=');alert(1);//.
Fix: Whitelist-validate sort_flg to "asc" or "desc" only; reject other values.

[A14-5] MEDIUM | File: rpt_impact_report.jsp, rpt_driver_util.jsp, rpt_impact_photo_report.jsp
Description: Request parameters (user_cd, loc_cd, dept_cd, sev) interpolated as bare strings into JS onload body attribute.
Fix: Apply escapeEcmaScript() before interpolation; validate params match expected numeric/alphanumeric patterns.

[A14-6] MEDIUM | File: rpt_driver_licence_expiry.jsp | Line: 446-449
Description: user_cd, loc_cd, dept_cd, form_cd interpolated into JS var declarations in script block -- JS metacharacter injection.
Fix: Apply escapeEcmaScript() or JSON encoding; validate as numeric/alphanumeric.

[A14-7] HIGH | File: rpt_serv_maintenance.jsp, rpt_hour_counter.jsp, rpt_messages_status.jsp
Description: DB-sourced color values (sm_color, msg_col) injected directly into HTML <td> attributes -- attribute injection allowing event handler insertion.
Fix: Validate color values as hex #RRGGBB or named colors server-side; encode with escapeXml; prefer CSS class names.

[A14-8] HIGH | File: rpt_messages_status.jsp | Line: 546
Description: DB-sourced message code, message content, vehicle hire number interpolated into JS onclick handler -- stored XSS via single-quote breakout.
Fix: Apply escapeEcmaScript() to all values; or use data-* attributes with external JS event listeners.

[A14-9] MEDIUM | File: rpt_impact_photo_report.jsp | Line: 593
Description: Image path from DB concatenated into javascript:popImage() href -- stored XSS if filename contains JS metacharacters.
Fix: Apply escapeEcmaScript(); validate/sanitise image filenames at ingestion to safe characters only.

[A14-10] MEDIUM | File: rpt_blacklist_driv.jsp, rpt_blacklist_driv_au.jsp
Description: scr (search) parameter injected into JS AJAX URL string and hidden field values without encoding -- reflected XSS.
Fix: Apply escapeEcmaScript() for JS context; HTML-encode for attribute context; validate to safe character set.

[A14-11] MEDIUM | File: reports/mail_first.jsp, mail_conf.jsp
Description: url request parameter reflected into hidden field value attribute without encoding -- attribute breakout XSS.
Fix: HTML-encode url in attribute; validate as expected relative path pattern.

[A14-12] HIGH | File: reports/mail_report.jsp | Line: 24-25, 44
Description: mail_id and subject from request passed directly to sendMail() without sanitisation -- email injection/open relay; mail_id also reflected unescaped in HTML.
Fix: Validate mail_id against strict email regex rejecting \r\n; strip newlines from subject; restrict to session user's addresses; require CSRF token.

[A14-13] HIGH | File: reports/mail_report.jsp | Line: 15-19
Description: url parameter appended to server-side base URL and fetched to construct email body -- SSRF to internal network resources.
Fix: Validate url against strict allowlist of permitted report page names; reject .., ://, unexpected characters.

[A14-14] CRITICAL | File: reports/file_dl.jsp | Line: 4-16
Description: customer, location, department, vehicle_cd, fileName parameters concatenated into filesystem path without validation -- arbitrary file read via ../ traversal; no authentication check.
Fix: Add session auth; canonicalise path with File.getCanonicalPath() and verify starts with base directory; validate each param to alphanumeric/hyphen/underscore only.

[A14-15] HIGH | File: reports/file_dl_url.jsp | Line: 2-14
Description: filename parameter concatenated to fixed base path /home/gmtp/fms_files/licence/ -- path traversal arbitrary file read; no authentication check.
Fix: Same as A14-14: canonicalise and verify within base; validate filename; add authentication.

[A14-16] MEDIUM | File: reports/xlsx_report.jsp | Line: 17-21
Description: rpt_name and params request parameters passed unvalidated to ExcelUtil.getExcel() -- potential path traversal or unexpected behaviour depending on implementation.
Fix: Validate rpt_name against strict allowlist of known report identifiers; review ExcelUtil implementation.

[A14-17] HIGH | File: rpt_impact_avg_driver_rpt.jsp, rpt_impact_avg_hours_rpt.jsp
Description: No setAccess_level/setAccess_cust/setAccess_site/setAccess_dept calls before filter.init() -- all customers' impact data may be returned.
Fix: Add standard access control block reading session attributes and setting on filter before init().

[A14-18] MEDIUM | File: rpt_unit_unlock.jsp, rpt_unit_unlock_impact.jsp, rpt_unit_unlock_question.jsp
Description: State-modifying Save form writes unlock reason to DB with no CSRF token.
Fix: Implement synchroniser token pattern; validate token server-side before processing save.

[A14-19] MEDIUM | File: All excel_* export pages (~30 files in reports/)
Description: DB values output directly as HTML table cells with Content-Type application/vnd.ms-excel -- formula injection if values start with =, +, -, @.
Fix: Prefix formula-triggering characters with single quote; or use Apache POI for proper cell typing.

[A14-20] HIGH | File: rpt_driver_licence_expiry_detail.jsp
Description: No setAccess_level/session-scoping calls before filter.init() -- arbitrary cust_cd from request may retrieve other customers' licence data.
Fix: Add standard access scoping block consistent with other report pages.

[A14-21] MEDIUM | File: reports/display_report.jsp | Line: 396-406, 498-539
Description: do_list, undo_list, sort_by, sort_asc reflected into JS onclick handlers; DB data values output unescaped.
Fix: Validate list params to digits/commas only; apply escapeEcmaScript(); HTML-encode DB data.

[A14-22] MEDIUM | File: rpt_imp_set_lst.jsp, rpt_override_code_lst.jsp
Description: get_cust, get_loc, get_dep display names from DB output unescaped in page heading -- stored XSS.
Fix: HTML-encode with escapeXml before output.

[A14-23] MEDIUM | File: reports/rpt_call_mail.jsp (also rpt_call_alertmail.jsp, rpt_cal_impact.jsp)
Description: Batch mail trigger endpoint with no authentication check; accepts debug and email parameters -- unauthenticated batch email triggering and info disclosure.
Fix: Add session authentication; restrict to admin access_level; remove debug/email params from public-facing JSPs; trigger via scheduler only.

### master-jsps-vehicles

[A12v-1] HIGH | File: existing_alert_lst.jsp:172, existing_alert_lst_admin.jsp:466, frm_alert_add.jsp:533, frm_alert_add1.jsp:540 | Line: 172, 466, 533, 540
Description: The `message` request parameter is read directly and output unescaped into HTML via `<%= message %>` in all four files -- classic reflected XSS via crafted URL.
Fix: HTML-encode `message` before output; replace all `<%=message %>` with `<%=StringEscapeUtils.escapeHtml(message) %>` or equivalent.

[A12v-2] HIGH | File: existing_vehicle_lst.jsp:349, existing_cust_vehicle_lst.jsp:558 | Line: 349, 558
Description: Request parameters `veh_typ_cd`, `loc_cd`, `cust_cd`, `dept_cd` written directly into HTML `body onload` attribute JavaScript call -- JS injection via single quote or closing parenthesis.
Fix: JavaScript-encode all values with `StringEscapeUtils.escapeEcmaScript()`; enforce numeric format for integer/code values server-side.

[A12v-3] HIGH | File: existing_alert_lst_admin.jsp:372, frm_alert_add1.jsp:436, frm_alert_add.jsp:419 | Line: 372, 436, 419
Description: Multiple DB-sourced and request param-sourced values injected unescaped into multi-argument JavaScript `set(...)` call in `body onload` -- JS string context breakout.
Fix: Apply `StringEscapeUtils.escapeEcmaScript()` to every value embedded in JS string literal; validate ID/code parameters match expected alphanumeric pattern.

[A12v-4] MEDIUM | File: existing_vehicle_lst.jsp:492,494,498, existing_cust_vehicle_lst.jsp:714,727,731 | Line: 492, 494, 498, 714, 727, 731
Description: Vehicle code, GMTP ID, and hire/fleet number rendered directly into `onClick` JavaScript handler string arguments without HTML/JS escaping -- stored XSS if DB values contain single quote or backslash.
Fix: JS-encode values in JS string literals with `escapeEcmaScript()`; HTML-encode values used as visible text with `escapeHtml()`.

[A12v-5] HIGH | File: existing_cust_vehicle_lst.jsp:471,501,503 | Line: 471, 501, 503
Description: Page reads `cust_cd` from request parameter and passes directly to filter bean with no check against `session.getAttribute("access_cust")` -- IDOR allowing cross-customer vehicle list access.
Fix: Enforce that requested `cust_cd` equals or is a permitted child of `session.getAttribute("access_cust")`; for `access_level >= 3` fix customer scope to session value.

[A12v-6] HIGH | File: existing_alert_lst_admin.jsp:291-329 | Line: 291-329
Description: Admin alert management page reads `access_level` from session but performs no conditional block halting rendering for non-admin users -- relies only on `Expire.jsp` (session existence) and filter bean scoping; authenticated non-admin can access admin UI directly.
Fix: Add explicit access level guard at top of scriptlet block (e.g., `if(al > 2) { response.sendRedirect("../error/access_denied.jsp"); return; }`).

[A12v-7] HIGH | File: frm_alert_add1.jsp:370,394,568 | Line: 370, 394, 568
Description: Admin alert form takes `user` variable from `request.getParameter("user_cd")` not session -- any authenticated user can specify arbitrary `user_cd` to create/edit alerts on behalf of another user; cross-tenant data manipulation.
Fix: Enforce admin-level check before accepting `user_cd` from request; validate target `user_cd` against admin's permitted customer scope; force user code from session for own-alert editing.

[A12v-8] MEDIUM | File: existing_alert_lst.jsp:164, existing_alert_lst_admin.jsp:412, frm_alert_add.jsp:420, frm_alert_add1.jsp:437 | Line: 164, 412, 420, 437
Description: All alert mutation forms POST to `../servlet/Frm_saveuser` with no CSRF synchroniser token -- attacker can auto-submit POST from victim's authenticated browser to silently add/edit/delete alert subscriptions.
Fix: Generate per-session CSRF token, store in HTTP session, include as hidden field in all state-changing forms, validate in `Frm_saveuser` before processing.

[A12v-9] LOW | File: existing_cust_vehicle_lst.jsp:739, frm_alert_add.jsp:551, existing_alert_lst_admin.jsp:560 | Line: 739, 551, 560
Description: Session-sourced `access_level` value written into hidden HTML form input -- exposes privilege model to attacker; potential privilege escalation if downstream servlet trusts submitted `alevel` value.
Fix: Remove `alevel` hidden field; `Frm_saveuser` servlet should read `access_level` directly from server-side session.

[A12v-10] MEDIUM | File: existing_vehicle_lst.jsp:436,446, existing_cust_vehicle_lst.jsp:652,674 | Line: 436, 446, 652, 674
Description: `search_crit` parameter rendered directly into input `value` attribute and table heading cell without escaping -- HTML attribute injection via `"` allows arbitrary HTML/JS injection.
Fix: HTML-encode `search_crit` with `escapeHtml()` in both input value and inline text context; limit permitted character set server-side.

### master-jsps-users

[A12u-1] CRITICAL | File: master/existing_user_lst.jsp | Line: 436, 579, 609, 611
Description: DB-sourced and request-parameter values interpolated directly into JavaScript event handler strings and `onload` attributes without any escaping -- stored and reflected XSS; `onload` on line 436 interpolates four request parameters directly into JS function call.
Fix: JavaScript-escape all values in JS contexts with `escapeEcmaScript()`; HTML-escape values in HTML contexts with `encodeForHTML()`.

[A12u-2] HIGH | File: master/existing_user_lst.jsp | Line: 540, 544-545
Description: `message` request parameter (line 540) and `search_crit` request parameter (line 545) output raw into HTML -- reflected XSS via crafted link.
Fix: HTML-encode all request parameters before rendering with `encodeForHTML()`.

[A12u-3] HIGH | File: master/existing_user_lst.jsp | Line: 435, 583, 585, 587, 590, 596, 599
Description: User list exposes access level, accessible customers list, mobile phone numbers, and Wiegand card IDs (physical access credentials) in plaintext; bare `<%=access_cust%>` on line 435 leaks session data (debug artefact with trailing "asd" on line 590).
Fix: Remove bare `<%=access_cust%>` and debug artefacts; restrict Wiegand ID display to admin-only edit form; HTML-encode all remaining outputs.

[A12u-4] HIGH | File: master/existing_user_lst.jsp | Line: 476, 620-621
Description: Form posts to `../servlet/Frm_saveuser` with `op_code=user_delete` or `user_active` to delete/recover user accounts with no CSRF token -- forged POST can silently delete arbitrary user accounts.
Fix: Implement Synchronizer Token Pattern with per-session CSRF token.

[A12u-5] CRITICAL | File: master/existing_driver_lst.jsp | Line: 599, 601, 603, 607, 611, 615, 618, 627, 635, 637
Description: Driver names, user ID, card prefix, card/PIN value, mobile number, and Wiegand driver ID all interpolated into HTML and JavaScript onclick handlers without escaping -- stored XSS via card/PIN or driver name fields; `onload` on line 452 uses four request params.
Fix: Apply JavaScript escaping for JS event handlers; HTML encoding for HTML content; remove or restrict display of card/PIN and Wiegand values.

[A12u-6] HIGH | File: master/existing_driver_lst.jsp | Line: 492, 646-647
Description: Driver form posts to `../servlet/Frm_saveuser` with no CSRF token -- delete and recover operations (`driver_delete`, `driver_active`) can be forged.
Fix: Implement Synchronizer Token Pattern.

[A12u-7] HIGH | File: master/existing_driver_lst.jsp | Line: 607-618
Description: Driver list renders card prefix (site code), full card/PIN number, and Wiegand ID for every driver in plaintext -- physical access credentials exposed enabling card cloning or unauthorised vehicle access.
Fix: Mask card/PIN and Wiegand ID in list view (show only last 4 characters); full values only in admin edit form over HTTPS with audit logging.

[A12u-8] MEDIUM | File: master/existing_customer_lst.jsp | Line: 382
Description: Customer list form has no `method` or `action` attribute; navigation relies on JavaScript `location.replace()` only; "Add/Edit Site" passes customer code as URL parameter enabling IDOR.
Fix: Explicitly declare `method="get"` or `method="post"` with CSRF token; do not rely on JS-only navigation for security.

[A12u-9] HIGH | File: master/existing_customer_lst.jsp | Line: 469, 471, 479
Description: Customer company name, account prefix, contact email, phone number rendered raw -- free-text fields enable stored XSS; JS onclick interpolates customer code and name without escaping.
Fix: HTML-encode all values in HTML context; JavaScript-escape values in JS string literals within event handlers.

[A12u-10] CRITICAL | File: master/frm_access_customer.jsp | Line: 136, 159
Description: `user_cd` parameter read from HTTP request and passed directly to filter to load that user's customer access rights -- no verification requesting user is permitted to view/modify target user's access rights; any authenticated user can view or overwrite any other user's customer access permissions.
Fix: Validate server-side that requesting session's user is same user or has access level permitting managing target user; verify target user's customer scope against `access_cust`.

[A12u-11] HIGH | File: master/frm_access_customer.jsp | Line: 222, 273
Description: Form saving customer access rights has no CSRF token -- combined with A12u-10 IDOR, attacker can craft cross-site request to grant or revoke any user's access to any customer.
Fix: Implement Synchronizer Token Pattern; fix A12u-10 IDOR first.

[A12u-12] HIGH | File: master/frm_access_customer.jsp | Line: 235, 253, 268
Description: User first/last names, customer names, and `message` parameter output without HTML encoding on privilege-management page -- stored XSS on admin session enables privilege escalation.
Fix: HTML-encode all DB-sourced values; especially critical on access-management page.

[A12u-13] HIGH | File: master/frm_blacklist_driv.jsp | Line: 776
Description: `message` request parameter rendered directly into `<tr>` element without HTML encoding -- reflected XSS.
Fix: HTML-encode `message` parameter before output.

[A12u-14] HIGH | File: master/frm_blacklist_driv.jsp | Line: 714, 946
Description: Blacklist form (restricts drivers from operating specific vehicle types/vehicles) has no CSRF token -- forged request can blacklist/unblacklist any driver.
Fix: Implement Synchronizer Token Pattern.

[A12u-15] HIGH | File: master/frm_blacklist_driv.jsp | Line: 795-817
Description: Driver first and last names rendered into table cells without HTML encoding -- stored XSS via malicious driver name.
Fix: HTML-encode `Vuser_fnm.get(i)` and `Vuser_lnm.get(i)` before rendering.

[A12u-16] HIGH | File: master/existing_opchk_lst.jsp | Line: 578, 631
Description: Operational checklist question text (`vquest.get(i)`) rendered raw -- stored XSS via crafted question; `message` parameter also reflected raw.
Fix: HTML-encode `vquest.get(i)` and `message` parameter.

[A12u-17] HIGH | File: master/existing_opchk_lst.jsp | Line: 557, 562, 574, 611, 621
Description: Check codes and customer name interpolated into JavaScript `onclick` handlers without escaping -- customer name with single quote breaks JS string allowing injection.
Fix: JavaScript-escape all values in JS string contexts with `escapeEcmaScript()`.

[A12u-18] HIGH | File: master/existing_opchk_lst.jsp | Line: 457, 637, 319
Description: Operational checklist form (deletes/reorders safety questions) posts to `../servlet/Frm_saveuser` with no CSRF token -- forged request can delete or reorder safety questions undermining safety check workflow.
Fix: Implement Synchronizer Token Pattern.

[A12u-19] MEDIUM | File: All six JSPs | Line: 626, 652, 954, 644
Description: Access level from session controls UI element visibility but `access_level` value also written to hidden form field `alevel` -- user can modify with dev tools to bypass client-side controls; potential privilege escalation if servlet relies on posted value.
Fix: Verify `Frm_saveuser` reads access level exclusively from `session.getAttribute("access_level")` never from `request.getParameter("alevel")`; audit as priority follow-on.

[A12u-20] MEDIUM | File: master/existing_user_lst.jsp + 3 others | Line: 350-355, 368-371, 593-596, 333-336
Description: `cust_cd`, `loc_cd`, `dept_cd` read from request parameters; unclear whether Databean enforces session-scope limits when `cust_cd` supplied directly -- potential cross-customer user listing.
Fix: Audit `Databean_getuser` to confirm session-scope enforcement; reject request-supplied `cust_cd` not belonging to session's `access_cust`.

### master-jsps-misc

[A12m-1] CRITICAL | File: master/chk_dup_acode.jsp, master/chk_dup_card.jsp | Line: entire file
Description: Both AJAX endpoints accept user input and query DB with no session authentication check (no `../sess/Expire.jsp`) -- unauthenticated enumeration of account codes and card numbers.
Fix: Add `<%@ include file="../sess/Expire.jsp" %>` as first directive in both files; ensure servlet/DAO layer also enforces session authentication.

[A12m-2] CRITICAL | File: master/chk_dup_acode.jsp, master/chk_dup_card.jsp | Line: 8-18, 8-30
Description: Multiple request parameters passed with no validation to Databean_getuser setters on unauthenticated endpoint -- if DAO uses string concatenation (confirmed pattern), parameters are SQL-injectable.
Fix: Verify DAO queries use parameterised PreparedStatement; apply whitelist input validation (numeric/alphanumeric bounded length); enforce authentication (A12m-1).

[A12m-3] HIGH | File: master/edit_dept_name.jsp, edit_site_address.jsp, edit_site_name.jsp, frm_new_customer.jsp, frm_new_department.jsp, frm_customer_rel.jsp, frm_customer_vehicle_rel.jsp, frm_customer_vehicle_reset.jsp, frm_mastercode.jsp, frm_hourcount_config.jsp | Line: various
Description: Every file uses raw `<%= %>` to embed values into HTML output (table cells, input values, textarea, onclick attributes, img src) with no encoding -- reflected XSS via URL parameters, stored XSS via DB values, and JS context XSS via event handlers.
Fix: Replace `<%= value %>` with JSTL `<c:out escapeXml="true"/>` or `ESAPI.encoder().encodeForHTML()`; use `encodeForJavaScript()` for JS handler attributes; use `encodeForHTMLAttribute()` for value attributes.

[A12m-4] HIGH | File: master/frm_customer_rel.jsp, frm_customer_vehicle_rel.jsp, frm_customer_vehicle_reset.jsp, frm_mastercode.jsp, frm_hourcount_config.jsp | Line: various
Description: Customer identifier (`user_cd`/`cust_cd`) read from URL parameter and passed directly to data access layer -- IDOR allowing cross-tenant data access (sites, departments, vehicles, hour count configs, master codes).
Fix: Derive customer identifier from `session.getAttribute("access_cust")` for single-customer users; for admin users validate requested `user_cd` against permitted customer set server-side.

[A12m-5] HIGH | File: master/frm_customer_vehicle_reset.jsp | Line: 319-320, 496, 558
Description: "Reclaim Vehicle" operation specifies vehicle and customer entirely via request parameters with no server-side permission check -- authenticated user can reclaim vehicles from unrelated customers; hardcoded `res_gmtp="Y"` forces GMTP prefix reset unconditionally.
Fix: Validate server-side in `Frm_saveuser` that vehicle belongs to customer the authenticated session is authorised to manage; verify vehicle-customer relationship against session's `access_cust`.

[A12m-6] HIGH | File: master/frm_mastercode.jsp | Line: 352-387, 579-580
Description: Master override code generation uses customer and site from request parameters not session; only UI-level access restriction (hiding "All" dropdown option) -- lower-privileged user can manually submit `site_cd=all` or arbitrary `user_cd` to generate unauthorised master codes providing physical-layer device access bypass.
Fix: Implement server-side access level gate; re-validate session's `access_cust` against requested `user_cd` in `frm_mastercode_step2.jsp`.

[A12m-7] HIGH | File: master/frm_hourcount_config.jsp | Line: 201, 234-235
Description: Hour count (contracted hours per year) is billing-sensitive; `cust_cd` taken from request parameter -- attacker changing `cust_cd` in URL can view/modify contracted hour settings for other customers' vehicles.
Fix: Derive `cust_cd` from session's `access_cust`; for multi-customer admin validate requested `cust_cd` is within permitted set.

[A12m-8] MEDIUM | File: All 10 master/misc form JSPs | Line: various
Description: No state-changing form includes CSRF token -- operations include creating customers, editing department/site names, assigning/reclaiming vehicles, updating hour configs; master code form uses `method='get'` (bookmarkable/embeddable in `<img src>`).
Fix: Implement synchroniser token pattern; change master code form to `method="post"`.

[A12m-9] MEDIUM | File: master/frm_customer_rel.jsp | Line: 321-330
Description: jQuery `$(document).ready` block intercepts all form submissions, displays serialised form data in browser `alert()`, then prevents submission (`e.preventDefault(); return false;`) -- debug artefact breaks form functionality and exposes field names/values.
Fix: Remove debug block entirely; implement pre-commit hook to detect and block debug output statements.

[A12m-10] LOW | File: master/frm_customer_vehicle_rel.jsp, frm_customer_vehicle_reset.jsp, frm_customer_rel.jsp, edit_dept_name.jsp, edit_site_address.jsp, edit_site_name.jsp, frm_new_customer.jsp | Line: various
Description: Request parameters injected directly into JavaScript event handler attribute strings without JS encoding (separate encoding context from HTML body/attribute) -- single quote breaks out of JS string literal.
Fix: Apply `encodeForJavaScript()` for values in JS string literals within HTML event handlers; consider moving to data-* attributes with external JS.

[A12m-11] LOW | File: master/chk_dup_acode.jsp, master/chk_dup_card.jsp | Line: 20-25
Description: AJAX endpoints return count revealing whether account code or card number exists in DB -- with no authentication (A12m-1), enables automated enumeration of account codes and card identifiers.
Fix: Add authentication (A12m-1); implement rate limiting to prevent automated enumeration even by authenticated users.

### master-jsps-config

[A12c-1] CRITICAL | File: master/frm_conf_firmware_upg.jsp | Line: 519-538
Description: No session authentication guard; access control variables hard-coded (`access_level="1"`, `access_cust="0"`, etc.) -- any unauthenticated HTTP request can load page and submit firmware dispatch form.
Fix: Re-add `<%@ include file="../sess/Expire.jsp" %>` as first line; remove all hard-coded access values; restore reading from `session.getAttribute(...)`.

[A12c-2] CRITICAL | File: master/frm_conf_firmware_display.jsp | Line: 72-91
Description: No session guard; identical hard-coded access values -- displays live firmware version matrix (fleet numbers, GMTP device IDs, firmware versions, upgrade dates) to unauthenticated parties.
Fix: Add `<%@ include file="../sess/Expire.jsp" %>` at line 1; restore session-driven access level reading.

[A12c-3] CRITICAL | File: master/frm_conf_firmware_upg.jsp, Frm_saveuser.java | Line: 605 (JSP); 54-80, 177-181 (Servlet)
Description: `Frm_saveuser` servlet's `doPost()` performs no session authentication check before dispatching to any operation handler -- unauthenticated POST with `op_code=conf_firmware_upg` dispatches firmware upgrade commands to fleet devices.
Fix: Add session authentication guard at top of `doPost()`: verify `req.getSession(false) != null` and `user_cd` attribute exists; send 401 or redirect to login.

[A12c-4] CRITICAL | File: Frm_saveuser.java | Line: 10204, 10211, 10220-10241, 10264-10280
Description: `cust_cd` for firmware dispatch taken entirely from HTTP request parameters with no comparison to session's `access_cust` -- any user (or unauthenticated given A12c-1/A12c-3) can push FTPF firmware-upgrade commands to any customer's fleet devices via `outgoing` table polled by telematics gateway.
Fix: Compare submitted `cust_cd` to `session.getAttribute("access_cust")`; reject mismatched requests; apply equivalent checks for `loc_cd` and `dept_cd`.

[A12c-5] HIGH | File: Frm_saveuser.java | Line: 10211, 10343-10376, 10386, 10220-10241, 10264-10280, 10292-10304
Description: Both `conf_firmware_upg` and `conf_firmware_upg_bean` build every SQL query using raw string concatenation with unvalidated request parameters (`veh_cd[]`, `mod_cd[]`, `cust_cd`, `loc_cd`, `dep`, `message`) -- SQL injection; no session required (A12c-3).
Fix: Replace string-concatenated queries with `PreparedStatement` parameterised placeholders; validate `message` (firmware version) against DB set of known valid versions.

[A12c-6] HIGH | File: frm_conf_firmware_upg.jsp, frm_conf_firmware_upg_bean.jsp, frm_conf_firmware_display.jsp, frm_conf_driv_setting.jsp, frm_impact_setting.jsp | Line: various
Description: All five JSPs emit request parameters and DB-sourced values directly using `<%= %>` with no HTML encoding -- `message`, `search_crit`, vehicle hire numbers, GMTP device IDs, firmware version strings, location/department/customer names all produce stored or reflected XSS.
Fix: Wrap every `<%= %>` expression outputting user-supplied or DB-sourced data through HTML-encoding utility.

[A12c-7] HIGH | File: master/frm_conf_driv_setting.jsp | Line: 622-625, 631, 662-663
Description: `cust_cd`, `loc_cd`, `dept_cd` filter values taken from request parameters without cross-referencing session's `access_cust` -- authenticated user can alter `cust_cd` to issue IDAUTH/IDDENY/IDCLEAR/IDMAST driver memory commands to another customer's fleet devices.
Fix: Compare requested `cust_cd` against `session.getAttribute("access_cust")` when `access_level > 1`; enforce in both JSP and servlet.

[A12c-8] HIGH | File: All five config JSPs | Line: 605, 606, 163, 731, 698
Description: All forms POST to `../servlet/Frm_saveuser` with no CSRF token -- firmware upgrade dispatch, driver memory management, and impact calibration commands can be triggered via cross-site request forgery.
Fix: Generate cryptographically random per-session CSRF token; embed as hidden field in every form; validate in `Frm_saveuser.doPost()`.

[A12c-9] MEDIUM | File: master/frm_conf_driv_setting.jsp, frm_impact_setting.jsp, frm_conf_firmware_upg_bean.jsp | Line: 627, 586, 537
Description: `access_level.equalsIgnoreCase("")` called without null guard -- if `access_level` never written to session, `NullPointerException` surfaces as HTTP 500 exposing stack trace with internal class names and server paths.
Fix: Change to `if(access_level == null || access_level.equalsIgnoreCase(""))` in all affected pages.

[A12c-10] MEDIUM | File: master/frm_conf_firmware_upg.jsp, frm_conf_firmware_upg_bean.jsp | Line: 671-675, 678-682
Description: Firmware version string (`message` parameter) taken from request and concatenated into FTPF command path without validation against legitimate versions -- path traversal or attacker-controlled path on firmware FTP server; commands sent to physical devices using unvalidated input.
Fix: Server-side query to confirm `message` value exists in firmware version table before constructing FTPF string; reject values not in approved list.

[A12c-11] MEDIUM | File: master/frm_impact_setting.jsp | Line: 453-467
Description: Impact slider calibration settings sent via inline `$.ajax()` POST to `../servlet/Frm_saveuser` with `op_code=set_fssxmulti` -- no CSRF token; AJAX uses standard form-encoded content vulnerable to cross-origin form attack; attacker can silently re-calibrate impact detection thresholds.
Fix: Include session CSRF token in AJAX `data` parameter; validate in servlet before processing `set_fssxmulti`.

[A12c-12] LOW | File: master/frm_conf_driv_setting.jsp | Line: 1014
Description: Session's `access_level` written to hidden form field `alevel` and used by client-side JS to decide "All" dropdown options -- trivially bypassable by setting `alevel=1` in browser dev tools.
Fix: Remove `alevel` hidden field; embed access level as JS constant from session at render time rather than submittable form field; enforce server-side only.

[A12c-13] MEDIUM | File: Frm_saveuser.java | Line: 34-36
Description: `Frm_saveuser` implements deprecated `javax.servlet.SingleThreadModel` with mutable instance fields (`dbcon`, `queryString`, `message`, `url`, `stmt`, `rset`) -- under load, concurrent requests can corrupt state, leaking one user's firmware dispatch response to another or producing incorrect SQL.
Fix: Remove `SingleThreadModel`; move all mutable state to local variables within `doPost()` and handler methods; use try-with-resources for DB connections.

### master-jsps-b

[A12b-1] HIGH | File: master/frm_customer_rel.jsp | Line: 453
Description: `message` parameter taken directly from `request.getParameter("message")` and rendered into HTML without encoding -- reflected XSS via crafted redirect URL.
Fix: HTML-encode all user-controlled values before rendering with `encodeForHTML()`.

[A12b-2] HIGH | File: All form JSPs (35+ files in master/) | Line: various
Description: Every form page reflects the `message` request parameter raw into HTML -- widespread reflected XSS across 35+ files.
Fix: Apply `encodeForHTML()` to all `message` parameter outputs; global search-and-replace of `<%=message %>` pattern.

[A12b-3] HIGH | File: master/frm_customer_rel.jsp | Line: 493-501
Description: Site names, addresses, and status codes from DB interpolated directly into `onclick` attribute strings without JavaScript encoding -- stored XSS if DB values contain JS metacharacters.
Fix: Encode DB values for JS string context using `encodeForJavaScript()`; consider unobtrusive event handling patterns.

[A12b-4] HIGH | File: master/frm_new_driver.jsp, master/frm_new_user.jsp | Line: 695, 767
Description: Multiple DB-sourced values (user group, status, driver flag, customer code, site code, department code, access level, ID type, expiry) interpolated raw into `<body onload="set(...)">` -- stored XSS via single quote or JS special character in any value.
Fix: Apply `encodeForJavaScript()` to every value in JS string literals in event handler attributes; or write values to JSON object in page head.

[A12b-5] MEDIUM | File: master/frm_new_customer.jsp | Line: 310
Description: DB-sourced filename (`mach_pic`) written directly into `<img src>` attribute without encoding -- attribute breakout via `"` or `>`; potential path traversal via `../`.
Fix: Validate `mach_pic` against allowlist of safe filename characters; HTML-encode on output with `encodeForHTMLAttribute()`.

[A12b-6] CRITICAL | File: master/frm_new_user.jsp | Line: 942, 946
Description: User's password fetched from DB and pre-populated into password and confirm password fields as plaintext value attributes -- passwords stored in recoverable form (plaintext or reversibly-encrypted) in database.
Fix: Hash passwords with bcrypt/scrypt/Argon2; never read back or display; leave password fields empty on edit; only update hash if admin enters new value.

[A12b-7] HIGH | File: master/frm_new_driver.jsp, master/frm_new_user.jsp | Line: 14, 14
Description: jQuery UI loaded from external CDN over plain HTTP (not HTTPS) -- MITM can replace library with malicious JS; jQuery UI 1.8.21 is from 2012 with known vulnerabilities.
Fix: Bundle jQuery UI locally; serve over HTTPS; upgrade to current supported version.

[A12b-8] LOW | File: master/frm_customer_rel.jsp | Line: 325
Description: jQuery debug `alert()` statement serializes and displays all form data in production code.
Fix: Remove all debug `alert()` calls from production code.

[A12b-9] HIGH | File: All state-changing form JSPs (38+ files in master/) | Line: N/A
Description: Every form POSTing to `../servlet/Frm_saveuser` contains no anti-CSRF token -- attacker can silently submit any form using victim's active session causing unauthorized state changes.
Fix: Implement Synchronizer Token Pattern: per-session cryptographically random CSRF token as hidden field validated in `Frm_saveuser` before processing.

[A12b-10] HIGH | File: All get_*.jsp AJAX data endpoints (15 files in master/) | Line: N/A
Description: All AJAX data-fetching endpoints lack session enforcement include (`../sess/Expire.jsp`) -- return sensitive organizational data to unauthenticated HTTP clients.
Fix: Add `<%@ include file="../sess/Expire.jsp" %>` as first line in every `get_*.jsp` file.

[A12b-11] CRITICAL | File: master/register.jsp | Line: N/A
Description: Publicly accessible JSP web API accepts username/password credentials in plain HTTP parameters and creates full company registrations -- no session check, no CSRF protection; `email` input placed directly into XML response causing XML injection.
Fix: Implement proper API authentication (OAuth 2.0 or HMAC-signed over HTTPS); XML-entity-encode all user-supplied data; consider restricting from public internet.

[A12b-12] HIGH | File: master/update_all_user_weigand.jsp | Line: N/A
Description: State-changing form updating all user Wiegand codes does not include `../sess/Expire.jsp` -- unauthenticated user can load page and trigger Wiegand update operation.
Fix: Add `<%@ include file="../sess/Expire.jsp" %>` as first line; add CSRF token.

[A12b-13] HIGH | File: master/frm_group_loc_rel.jsp | Line: N/A
Description: Group Site Authorization form does not include `../sess/Expire.jsp` -- despite reading session attributes, no explicit authentication gate; unauthenticated access possible.
Fix: Add `<%@ include file="../sess/Expire.jsp" %>` as first line.

[A12b-14] HIGH | File: master/frm_new_customer.jsp, frm_new_driver.jsp, frm_new_user.jsp, frm_new_question.jsp, frm_new_vehicle.jsp, frm_new_vehicle1.jsp, frm_new_vehicle_short.jsp, frm_repl_vehiclemod.jsp, frm_service_status.jsp, frm_setup_driver.jsp, frm_send_canbus_rules.jsp, frm_vehicle_prod.jsp | Line: N/A
Description: Edit forms accept record identifier from request parameter and modify record with no check that record belongs to logged-in user's customer scope -- cross-tenant record editing (IDOR).
Fix: After fetching record by primary key, verify record's customer/tenant identifier matches `access_cust` from session; reject mismatches and log attempted access.

[A12b-15] HIGH | File: master/pic_upload_logo.jsp | Line: 27-32
Description: Logo upload validates file extension only in client-side JavaScript (trivially bypassed) -- if server-side handler does not validate, arbitrary file types including JSP webshells can be uploaded.
Fix: Server-side validation in `Frm_upload`: check extension against allowlist, validate MIME type via magic bytes, store outside web root or disable JSP execution in upload directory, rename to random UUID.

[A12b-16] MEDIUM | File: master/frm_upload_questions.jsp | Line: 170
Description: `cust_nm` parameter taken from request and reflected directly into page body without HTML encoding -- reflected XSS.
Fix: Apply `encodeForHTML(cust_nm)` before output.

[A12b-17] MEDIUM | File: master/frm_fc_vehicle_lst.jsp | Line: 481
Description: `search_crit` request parameter reflected raw into page body within `<b>` tag -- reflected XSS via crafted URL.
Fix: Apply `encodeForHTML(search_crit)` before output.

[A12b-18] HIGH | File: master/frm_new_branch.jsp, frm_new_branch_old.jsp, frm_new_department.jsp, frm_new_department_win.jsp, frm_new_division.jsp, frm_new_location.jsp, frm_new_group.jsp | Line: various
Description: Location names, addresses, group names, descriptions, timezone values from DB interpolated directly into `onclick="set_editvalues('...')"` without JavaScript encoding -- stored XSS.
Fix: Apply `encodeForJavaScript()` to all values in JS string contexts within HTML event attributes.

[A12b-19] MEDIUM | File: All XML-producing get_*.jsp endpoints (15 files + register.jsp) | Line: N/A
Description: All `get_*.jsp` construct XML responses by string concatenation without XML-encoding DB values -- malformed XML if values contain `<`, `>`, `&`, `"`, `'`; enables client-side injection.
Fix: Use `javax.xml.stream.XMLStreamWriter` or apply all five XML entity replacements to every value.

[A12b-20] MEDIUM | File: master/frm_new_customer.jsp, frm_new_driver.jsp, frm_new_user.jsp, frm_new_vehicle.jsp, frm_new_vehicle1.jsp | Line: multiple
Description: DB-sourced values (names, addresses, phone numbers, emails, serial numbers, hire numbers, comments) written raw into `<input value="...">` and `<textarea>` -- stored XSS via attribute breakout with `"`, `<`, or `>`.
Fix: Apply `encodeForHTMLAttribute()` for attribute contexts; `encodeForHTML()` for element content.

[A12b-21] HIGH | File: master/frm_io_setting.jsp | Line: 321
Description: I/O violation number and level values from DB interpolated raw into `onclick` attribute string -- stored XSS.
Fix: Apply `encodeForJavaScript()` to `vio_no` and `vio_level`.

[A12b-22] MEDIUM | File: master/frm_mastercode_step2.jsp | Line: 305, 315, 321
Description: DB-sourced display names rendered raw in H2 heading; driver code and slot number arrays echoed into hidden input fields without encoding.
Fix: Apply `encodeForHTML()` to heading content; `encodeForHTMLAttribute()` to hidden field values.

[A12b-23] MEDIUM | File: master/frm_override_codes.jsp | Line: 449
Description: Several request parameters (`veh_typ_cd`, `veh_cd`, `cust_cd`, `loc_cd`, `dept_cd`) interpolated directly into `<body onload="set(...)">` without JS encoding.
Fix: Apply `encodeForJavaScript()` to all values in onload handler.

[A12b-24] MEDIUM | File: master/frm_service_flag.jsp | Line: 399, 403, 453, 455-469
Description: Service reminder hour values, service IDs, vehicle hire numbers, accumulated hours, service dates rendered raw in table and onclick handler; `vserv_color` interpolated into `<td>` attribute creating injection point.
Fix: Apply `encodeForHTML()` to cell content; `encodeForJavaScript()` to onclick parameters; validate `vserv_color` against strict CSS class allowlist.

[A12b-25] MEDIUM | File: master/frm_send_canbus_rules.jsp | Line: 57, 71, 83, 97, 105, 115, 121-123
Description: Vehicle hire number, serial number, GMTP ID, vehicle type from DB rendered raw in table cells; `veh_cd`, `gmtp_id`, `form_cd` request parameters echoed into hidden input values without encoding.
Fix: Encode all DB values and request parameters before output.

[A12b-26] MEDIUM | File: master/frm_customer_vehicle_rel.jsp, frm_customer_vehicle_reset.jsp | Line: 324, 391
Description: Multiple request parameters interpolated directly into `<body onload="set(...)">` call without JS encoding.
Fix: Apply `encodeForJavaScript()` to all values in onload handler.

[A12b-27] MEDIUM | File: master/frm_impact_setting.jsp | Line: 658
Description: Vehicle type, vehicle code, customer code, site code, department code, and boolean flag interpolated raw into `<body onload>` JS call.
Fix: Apply `encodeForJavaScript()` to all values in onload handler.

[A12b-28] MEDIUM | File: master/frm_hourcount_config.jsp | Line: 362-363, 380, 383, 387, 395
Description: Customer, site, department display names from DB rendered raw in heading; vehicle hire numbers and contracted hours raw in table cells; vehicle code in onclick handler.
Fix: Encode all DB values with `encodeForHTML()` for HTML contexts; `encodeForJavaScript()` for JS contexts.

[A12b-29] MEDIUM | File: master/rpt_preop_unsync_qustion.jsp | Line: 478, 485-488
Description: Vehicle hire numbers, question order numbers, question text, expected answers, critical-answer flags from DB rendered raw in table cells; `bgcol` variable interpolated into `bgcolor` attribute.
Fix: Encode all DB values before output; validate `bgcol` and `col` against strict allowlist.

[A12b-30] MEDIUM | File: master/frm_site_hours.jsp | Line: 361
Description: Four filter parameters (`cust_cd`, `loc_cd`, `dep_cd`, `type_cd`) interpolated raw into `<body onload="set(...)">` call.
Fix: Apply `encodeForJavaScript()` to all values.

[A12b-31] MEDIUM | File: master/frm_service_flag.jsp | Line: 291, 403
Description: Three filter parameters in `<body onload="set(...)">` call; service ID in `deleteReminder()` onclick handler -- JS injection.
Fix: Apply `encodeForJavaScript()` to all values in JS event handler contexts.

[A12b-32] MEDIUM | File: master/frm_new_vehicle.jsp, frm_new_vehicle1.jsp, frm_repl_vehiclemod.jsp | Line: 261, 295-296, 115-116
Description: Filter parameters (`veh_typ_cd`, `loc_cd`, `st_dt`, `end_dt`, `search_crit`, `form_cd`, `cust_cd`, `dept_cd`) passed as GET parameters echoed raw into `onclick="closeform(...)"` -- JS injection.
Fix: Apply `encodeForJavaScript()` to all request parameters embedded in inline JS event handlers.

## Pass 2: Test Coverage

### config

[A01-1] CRITICAL | File: WEB-INF/web.xml, Frm_login.java | Line: 58-66, 72-73
Description: `Frm_login` concatenates `login` parameter directly into SQL authentication query without PreparedStatement -- SQL injection in most sensitive path; zero test coverage for credential validation or session establishment.
Fix: Write `testFrmLoginSqlInjectionPrevented()` using MockHttpServletRequest/Response; inject `' OR '1'='1` as login parameter; assert redirect to error page and no session attribute set.

[A01-2] CRITICAL | File: WEB-INF/web.xml, Frm_security.java
Description: `Frm_security` is central POST dispatcher for all access-controlled operations via `op_code` parameter using ESAPI, BCrypt, JNDI -- no test verifies op_code routing, unauthenticated request rejection, or BCrypt verification.
Fix: Write `testFrmSecurityDispatchRequiresSession()` asserting POST without valid session is rejected; write `testFrmSecurityOpCodeRouting()` to mock each known op_code and verify correct handler invoked.

[A01-3] CRITICAL | File: WEB-INF/web.xml
Description: `<security-constraint>` declaring CONFIDENTIAL transport for `/pages/*` is sole mechanism forcing HTTPS -- no integration test verifies HTTP requests are redirected or static assets correctly receive NONE treatment.
Fix: Write `testPagesRequireHttps()` using embedded Tomcat; issue HTTP GET to `/pages/login.jsp`; assert 301/302 redirect to `https://` URL.

[A01-4] CRITICAL | File: WEB-INF/src/ESAPI.properties
Description: Both `Encryptor.MasterKey` and `Encryptor.MasterSalt` are commented out -- ESAPI's JavaEncryptor will throw ConfigurationException at first use, silently disabling all encryption; no test verifies ESAPI initialisation.
Fix: Write `testEsapiEncryptorInitialises()` calling `ESAPI.encryptor()` asserting no ConfigurationException; write `testEsapiEncryptRoundTrip()` for key and cipher consistency.

[A01-5] CRITICAL | File: WEB-INF/src/ESAPI.properties
Description: `HttpUtilities.ForceHttpOnlySession` and `ForceSecureSession` both `false` -- ESAPI will not add HttpOnly or Secure flags to JSESSIONID cookie; enables session hijacking via XSS or network sniffing.
Fix: Write `testSessionCookieIsHttpOnly()` and `testSessionCookieIsSecure()` using MockHttpServletResponse; run login flow; assert presence of HttpOnly and Secure directives in Set-Cookie header.

[A01-6] HIGH | File: WEB-INF/web.xml, ESAPI.properties
Description: Three upload servlets accept multipart uploads; ESAPI allows anonymous uploads (`FileUploadAllowAnonymousUser=true`); 500MB max size and extension whitelist untested; upload directory is Windows path failing on production Linux server.
Fix: Write `testUploadRejectedForDisallowedExtension()` POSTing `.jsp` file and asserting rejection; write `testUploadRejectedWhenUnauthenticated()` and `testUploadDirectoryIsWritable()`.

[A01-7] HIGH | File: WEB-INF/web.xml
Description: `Frm_vehicle` and `Frm_customer` perform vehicle/customer master-data operations using BCrypt and JNDI -- no test coverage for authorization checks, data integrity, or BCrypt password path.
Fix: Write `testFrmVehicleRequiresAdminRole()` asserting non-admin session results in redirect or 403; write `testFrmCustomerSavePersistedCorrectly()` mocking datasource.

[A01-8] HIGH | File: WEB-INF/web.xml, Frm_saveuser.java
Description: `Frm_saveuser` implements deprecated `SingleThreadModel` (removed in Servlet 6.0) serializing all requests -- no tests for user-creation logic, password hashing, concurrent-request serialization, or duplicate username rejection.
Fix: Write `testSaveUserCreatesCorrectRecord()` mocking datasource; write `testSaveUserRejectsDuplicateUsername()` simulating collision and asserting error response.

[A01-9] HIGH | File: WEB-INF/web.xml, BusinessInsight.java
Description: `BusinessInsight` is `@MultipartConfig` servlet also declared in web.xml creating dual registration -- no test verifies load, multipart handling, email path, or which registration wins at runtime.
Fix: Write `testBusinessInsightLoadsWithoutError()` invoking `init()` asserting no exception; write `testBusinessInsightDualRegistrationWinner()` deploying to embedded container.

[A01-10] HIGH | File: WEB-INF/src/log4j2.properties
Description: Two silent misconfigurations: `logger.file.level=info,debug` unparseable by Log4j 2 causing silent fallback to ERROR; `rootLogger.appenderRef.stdout.ref=LOGFILE` broken name reference dropping output -- no startup test verifies log messages reach log file.
Fix: Write `testLog4j2ConfigurationIsValid()` using `LogManager.getContext(false).getConfiguration()` asserting at least one appender attached to root logger and level is not ERROR.

[A01-11] HIGH | File: WEB-INF/src/ESAPI.properties
Description: Intrusion detection thresholds configured as live security controls -- misconfiguration would silently remove brute-force and session-hijacking defences; no test triggers test intrusion event.
Fix: Write `testIntrusionDetectorFiresOnThreshold()` calling `IntrusionDetector.getInstance().addEvent("test")` twice within 10s and asserting account becomes disabled.

[A01-12] MEDIUM | File: WEB-INF/src/validation.properties, ESAPI.properties
Description: Six named validation patterns untested; `Validator.Redirect` set to `^\/test.*$` (placeholder restricting all redirects to `/test*`); `Validator.HTTPParameterValue` excludes common printable characters that may silently fail legitimate forms.
Fix: Write `testRedirectValidatorAllowsProductionPaths()` calling `ESAPI.validator().isValidRedirectLocation(...)` with production paths; write `testEmailValidatorAcceptsValidRejectsInvalid()`.

[A01-13] MEDIUM | File: WEB-INF/web.xml, ESAPI.properties
Description: Three inconsistent session timeout values: web.xml 30 min, ESAPI idle 20 min, ESAPI absolute 120 min -- no test verifies which timeout wins or whether sessions are invalidated after inactivity.
Fix: Write `testSessionExpiresAfterIdleTimeout()` creating session, advancing mock clock 31 min, asserting new-session redirect.

[A01-14] MEDIUM | File: WEB-INF/web.xml, ESAPI.properties
Description: Three-way encoding mismatch: JSP page-encoding ISO-8859-1, ESAPI ResponseContentType UTF-8, Frm_security sets response encoding UTF-8 -- no test for multi-byte or non-ASCII input round-trip.
Fix: Write `testNonAsciiInputRoundTrip()` POSTing non-ASCII characters and asserting response body correctly encoded.

[A01-15] MEDIUM | File: WEB-INF/src/ESAPI.properties
Description: `Logger.ApplicationName` set to `ExampleApplication` (ESAPI default template) -- all ESAPI log entries tagged with placeholder making log aggregation unreliable.
Fix: Write `testEsapiApplicationNameIsCorrect()` asserting `ESAPI.securityConfiguration().getApplicationName()` equals correct production identifier.

[A01-16] LOW | File: WEB-INF/src/log4j.properties, log4j2.properties
Description: Both log configs hard-code output path to `/home/gmtp/logs/linde.log` -- if directory does not exist or not writable, Log4j silently fails with no error.
Fix: Write `testLogDirectoryIsAccessibleAtStartup()` asserting `/home/gmtp/logs` is a directory and writable.

[A01-17] LOW | File: WEB-INF/src/log4j.properties
Description: `log4j.properties` uses Log4j 1.x namespace but servlets import Log4j 2.x -- Log4j 2 does not read `log4j.properties` by default making file silently inert dead configuration.
Fix: Write `testActiveLoggingFrameworkIsLog4j2()` asserting `LogManager.getContext().getClass().getName()` contains `log4j2`.

[A01-18] INFO | File: WEB-INF/src/ESAPI.properties
Description: `ESAPI.printProperties=true` prints entire configuration (algorithm names, key lengths, timeouts) to stdout at startup -- information disclosure in production.
Fix: Write `testEsapiPrintPropertiesIsFalseInProduction()` asserting `ESAPI.printProperties` equals `"false"`.

### security

[A18-01] CRITICAL | File: All 6 files in com.torrent.surat.fms6.security
Description: Security package (authentication, authorization, password management, session management, user CRUD, vehicle management) across 6 files and ~35,000+ lines has zero automated tests.
Fix: Implement comprehensive test suites covering authentication, authorization, SQL injection prevention, password hashing, session management, account lockout, and input validation.

[A18-02] CRITICAL | File: Frm_login.java, Frm_security.java | Line: 97-99, 66, 2053
Description: User-entered passwords AND database-stored passwords logged in plaintext via `log.info()` -- Frm_security line 66 logs every doPost request's password regardless of operation.
Fix: Remove all password logging; sanitize log messages so sensitive fields are never written to log output.

[A18-03] CRITICAL | File: Frm_login.java | Line: 58-59, 72-73
Description: Login parameter concatenated directly into SQL authentication queries without sanitization or parameterization -- full authentication bypass via SQL injection.
Fix: Replace string concatenation with PreparedStatement parameterized queries for all authentication SQL.

[A18-04] CRITICAL | File: Frm_login.java | Line: 81
Description: Passwords stored and compared in plaintext using `password.equals(pass_word)` with no hashing in this older login servlet.
Fix: Implement BCrypt or equivalent password hashing for storage and comparison; ensure no plaintext passwords stored in database.

[A18-05] CRITICAL | File: Frm_security.java | Line: 2196-2198
Description: Username parameter in password reset flow concatenated directly into SQL -- attacker can exfiltrate data or reset any user's password.
Fix: Use PreparedStatement parameterized queries; add rate limiting on password reset requests.

[A18-06] CRITICAL | File: Frm_security.java | Line: 2227-2231
Description: Temporary passwords stored in plaintext in `user_reset_password` table; SQL injection also possible through userId parameter.
Fix: Hash temporary passwords before storage; verify temp password expiry and invalidation after use; use parameterized queries.

[A18-07] CRITICAL | File: Frm_security.java | Line: 2435, 2448
Description: BMS passwords hashed with MD5 (broken algorithm) via SQL string concatenation embedding raw password values directly in SQL -- cryptographic weakness and SQL injection.
Fix: Replace MD5 with strong hashing (BCrypt, Argon2) in application code; use parameterized queries.

[A18-08] CRITICAL | File: Frm_security.java, Frm_customer.java | Line: 1569-1586, 2367-2378, 3586-3596, 3631-3633
Description: AU and MLA sites store/compare passwords in plaintext while other sites use BCrypt; BCrypt IllegalArgumentException fallback silently degrades to plaintext comparison.
Fix: Enforce BCrypt hashing for all sites including AU/MLA; remove plaintext fallback; implement migration path from plaintext to hashed passwords.

[A18-09] CRITICAL | File: Frm_customer.java, Frm_vehicle.java | Line: 49-57, 59-66
Description: Connection, Statement, ResultSet, and message are instance fields on singleton servlets -- concurrent requests corrupt each other's database state, potentially leaking data or creating authentication bypass.
Fix: Move all Connection, Statement, ResultSet, and message variables to local scope within each method for thread isolation.

[A18-10] CRITICAL | File: Frm_security.java
Description: Nearly every data-modification method (save_form, save_module, save_mail_group, save_mail_lst, saveDashboardSubscription, save_perm, change_password, chg_pass, reloadPermissions, saveShift, 20+ others) builds SQL through string concatenation with user-supplied input.
Fix: Convert all SQL operations to PreparedStatement with parameterized queries.

[A18-11] CRITICAL | File: Frm_customer.java
Description: Multiple methods (GetCanSettingsByVehicle, GetCanbusByVehicle, lock_unlock_start, add_user, get_username, Query_Customer_Relations, save_mastercodes, etc.) use string-concatenated SQL with user-supplied input.
Fix: Convert all SQL operations to PreparedStatement with parameterized queries.

[A18-12] CRITICAL | File: Frm_vehicle.java
Description: Nearly every private method (diagSyncThreshold, resetUnitMemory, broadcast, reboot, locker, 40+ others) uses string concatenation for SQL with user-supplied vehicle parameters.
Fix: Convert all SQL operations to PreparedStatement with parameterized queries.

[A18-13] HIGH | File: Frm_customer.java | Line: 8672-8673
Description: New users created with hardcoded plaintext password "password" with no forced password change requirement.
Fix: Generate random initial password; hash before storage; enforce mandatory password change on first login.

[A18-14] HIGH | File: Frm_security.java, Frm_customer.java, Frm_vehicle.java | Line: 57, 75, 1372, 79
Description: doPost() dispatchers invoke security-critical operations (save_perm, change_password, delete_user, reset_password, reboot, etc.) without verifying caller has valid authenticated session or appropriate access level.
Fix: Add session validation and access-level authorization checks before any operation dispatch in all servlet doPost/doGet methods.

[A18-15] HIGH | File: GetGenericData.java | Line: 67-73
Description: `getWeigand()` method contains syntactically invalid SQL (missing WHERE predicate); never called from doGet(); doGet() creates connection but performs no operations -- dead/abandoned code.
Fix: Remove class entirely if unused; verify servlet is not mapped or reachable.

[A18-16] HIGH | File: Frm_security.java | Line: 4045-4081
Description: `sendMail()` catches all exceptions (including Throwable) and always returns true regardless of email send success -- impossible to detect failed password reset email delivery.
Fix: Propagate or return actual send success/failure status; do not silently swallow exceptions.

[A18-17] MEDIUM | File: Databean_security.java
Description: All Fetch_* methods use string-concatenated SQL with values from setter fields populated from JSP parameters -- SQL injection possible if JSP pages pass unsanitized input.
Fix: Convert to parameterized queries; add input sanitization at JSP/bean boundary.

[A18-18] MEDIUM | File: GetGenericData.java | Line: 22-26
Description: Instance-level Connection, Statement, ResultSet, and queryString fields create same thread-safety concurrency issue as Frm_customer and Frm_vehicle.
Fix: Move all mutable state to local method scope for thread-safe servlet operation.

### dao

[A07-01] CRITICAL | File: All 10 DAO files
Description: Entire repository lacks any test framework, test directories, or test files -- all 10 DAO files have 0% code coverage with 128+ public methods executing SQL directly against production database.
Fix: Add JUnit 5 and Mockito to build dependencies; create `src/test/java` directory; prioritize DAO testing using embedded H2 or Mockito-based mocking of `DBUtil.getConnection()`.

[A07-02] CRITICAL | File: BatteryDAO.java | Line: 42, 100, 163, 365, 400
Description: All 6 methods construct SQL via string concatenation with user-supplied parameters; `getDuration()` and `getDept_prefix()` directly concatenate timestamp strings and `vcd` into SQL.
Fix: Convert to PreparedStatements; write parameterized-query tests and negative tests with SQL injection payloads.

[A07-03] CRITICAL | File: DriverDAO.java | Line: 35, 87, 159, 165, 178, 420, 550
Description: All 9 methods use string-concatenated SQL; `sendIDDENY` performs INSERT operations sending commands to physical vehicle hardware (IDDENY/IDAUTH messages); `checkValidLicence` concatenates `userId` and `newRevewDate`.
Fix: Test `sendIDDENY` and `checkValidLicence` thoroughly (physical vehicle access control); convert to PreparedStatements; write injection boundary tests.

[A07-04] CRITICAL | File: DriverImportDAO.java | Line: 29-30, 83, 738, 749, 893-917, 984, 1152, 1185
Description: 18 public methods; `checkDriverByNm` and `checkDriverByLic` concatenate names/licence into SQL; `saveLicenseExpiryBlackListInfo` (~360 lines) mixes PreparedStatements with raw concatenation and has commented-out `finally` cleanup.
Fix: Write tests for all 18 methods; `saveLicenseExpiryBlackListInfo` needs attention for nested logic, mixed statement types, and commented-out cleanup.

[A07-05] HIGH | File: All 10 DAO files
Description: Pervasive anti-pattern: exceptions caught with `catch(Exception e)` followed by `e.printStackTrace()` and no-op `e.getMessage()` whose return value is never used -- all database failures silently swallowed.
Fix: Write tests mocking `DBUtil.getConnection()` to throw `SQLException` and verify correct propagation; methods should log via proper logger and either throw or return sentinel value.

[A07-06] HIGH | File: DriverImportDAO.java | Line: 559-922, 893-917, 576, 688, 751
Description: `saveLicenseExpiryBlackListInfo` has deliberately commented-out `finally` block for closing ResultSets/PreparedStatements/Statements -- any mid-method exception causes resource leaks.
Fix: Write resource-leak tests using mock connections; verify all JDBC resources closed in all paths; consider try-with-resources refactoring.

[A07-07] HIGH | File: DriverImportDAO.java | Line: 511, 520, 540, 547-554, 924, 961-968
Description: In `saveDriverInfo` and `updateDriverInfo`, connection only closed inside conditional `if (null != ps)` block in `finally` -- if `ps` never assigned (null DriverImportBean), acquired connection never closed, causing pool leak.
Fix: Write tests with null DriverImportBean triggering early-return path; verify connection still closed; move `DBUtil.closeConnection(conn)` outside `if (null != ps)` block.

[A07-08] HIGH | File: MessageDao.java | Line: 15-18, 54-56, 62, 105
Description: Unlike other DAOs, `MessageDao` stores Connection, Statement, ResultSet, queryString as instance fields -- concurrent requests corrupt each other's database state; `fid` concatenated into SQL.
Fix: Write concurrent access tests demonstrating race condition; refactor to method-local JDBC resources; add SQL injection tests for `fid`.

[A07-09] CRITICAL | File: ImportDAO.java | Line: 166-167, 334, 569, 680, 698, 851-852
Description: ImportDAO (~4900+ lines, 16 public methods) performs INSERT/UPDATE/DELETE with string-concatenated SQL; `saveQuestions` concatenates question text into INSERTs; `removePreviousChecklist` concatenates check codes into DELETEs.
Fix: Write injection tests focusing on `saveQuestions` with SQL metacharacters; convert all DML to PreparedStatements; test `removePreviousChecklist` with manipulated `chkList` values.

[A07-10] CRITICAL | File: RegisterDAO.java | Line: 17-458, 75, 85, 284, 294, 373, 446-450
Description: `register` method (~440 lines) performs 15+ sequential INSERTs across 10+ tables without transaction management (`setAutoCommit(false)`/`commit()`/`rollback()`) -- mid-method failure leaves partially-created state with orphaned records; line 284 has SQL injection in username check.
Fix: Write integration tests covering successful registration and failure at each INSERT point; add transaction management with commit/rollback; test `checkAuthority` for timing-safe comparison.

[A07-11] HIGH | File: LockOutDAO.java, PreCheckDAO.java | Line: 103, 45, 50, 335, 453, 57-59, 120-123
Description: Both DAOs concatenate date parameters directly into SQL timestamp casts; LockOutDAO has logic bug where unrecognized lockout reason codes map to "Question" (line 122) instead of "Other".
Fix: Write tests with injection payloads in date parameters; test LockOutDAO reason code mapping to detect logic bug; convert date parameters to PreparedStatement parameters.

[A07-12] HIGH | File: ImpactDAO.java | Line: 52-83, 117-162, 357-425, 388, 203-243
Description: 11 methods with complex nested loops generating O(departments x models x months) individual SQL queries per invocation; `getRedImpactCacheByDriver` creates O(depts x drivers x models x months) queries; impact severity uses inconsistent casing (`Blue_LEVEL` vs `RED_LEVEL`).
Fix: Write performance tests measuring query count per invocation; extract RED/AMBER/BLUE classification into testable pure function; test edge cases including zero departments, zero models, year boundary crossings.

[A07-13] CRITICAL | File: UnitDAO.java | Line: 68, 172, 176, 181, 186, 195, 282, 450, 485, 521
Description: UnitDAO is most-referenced DAO (used by 5+ other DAOs) with 36+ methods all using string-concatenated SQL; `getUnitLstByModel` returns comma-separated vehicle codes embedded directly into IN clauses by calling DAOs -- second-order SQL injection.
Fix: Test `getUnitLstByModel` first (foundational query method); verify generated ID list format with empty, single, and large result sets; convert to PreparedStatements with IN-clause array binding.

[A07-14] HIGH | File: RegisterDAO.java | Line: 498, 511, 515
Description: `checkAuthority` sends `RuntimeConf.username` and `RuntimeConf.password` to DB to compute MD5 hashes via SQL then compares with `equalsIgnoreCase` (not timing-safe) -- sends plaintext credentials over JDBC, uses weak MD5, concatenates RuntimeConf values into SQL.
Fix: Write authentication tests for valid/invalid credentials, SQL injection in RuntimeConf values, and case sensitivity; replace MD5 with bcrypt/scrypt; move hash to application layer; use constant-time comparison.

[A07-15] HIGH | File: PreCheckDAO.java | Line: 78-94, 209-253, 376-405, 485-553
Description: `getChecks` retrieves all checklist result IDs then loops individually executing separate query per ID to count failed answers -- thousands of queries for large deployments; `getChecksByDriver` has quadruple nested structure.
Fix: Write load tests measuring query count and response time; refactor N+1 patterns to batch queries or JOINs; test with realistic data volumes.

### util-java

[A03-1] CRITICAL | File: RuntimeConf.java | Line: 18-30
Description: Plaintext passwords committed to version control (`pass="ciifirmware"`, `firmwarepass="Sdh79HfkLq6"`, `username="TestK"`, `password="testadmin"`, Clickatell `PASSWORD="fOqDVWYK"`); all fields `public static` mutable.
Fix: Write configuration-validation test asserting no credential field matches any known committed default/test value and no field is null or empty.

[A03-2] CRITICAL | File: EncryptTest.java | Line: 16, 97
Description: Algorithm is trivially reversible; empty string input to `encrypt()` returns 10-character prefix with no encrypted content; `decrypt()` on strings shorter than 10 characters throws `StringIndexOutOfBoundsException`; null input causes NPE.
Fix: Write round-trip tests, null input tests, empty string tests, too-short decrypt tests, and weakness demonstration tests.

[A03-3] CRITICAL | File: GdprDataDelete.java | Line: 67-95
Description: `gdpr_data` and `driver_cd.get(i)` interpolated directly into DELETE statements across nine tables -- malformed value could execute arbitrary SQL permanently destroying data; no test confirms customer scoping.
Fix: Write tests for customer isolation, GDPR interval boundary, and SQL injection resistance; requires parameterised query rewrite.

[A03-4] CRITICAL | File: CustomUpload.java | Line: 45-299
Description: Filename from multipart Content-Disposition header used with no extension check, type whitelist, or path separator sanitisation -- `../../WEB-INF/web.xml` writes to arbitrary paths; firmware action embeds hardcoded password in FTP command.
Fix: Write tests to reject non-CSV extensions, detect path traversal filenames, handle null parts, and verify large file behaviour.

[A03-5] CRITICAL | File: DataUtil.java | Line: 918-958
Description: `uploadLicenceFile()` writes to path where `filename` is caller-supplied with no sanitisation; `uploadDocumentFile()` constructs paths using `cust_loc` with no traversal check; `escapeSpecialCharacter()` does NOT strip `/` leaving `../` traversal possible.
Fix: Add `canonicalPath()` containment checks; write tests for path traversal via filename and `cust_loc`.

[A03-6] CRITICAL | File: ImportFiles.java | Line: 49-end
Description: Uploaded file written to disk with original filename before validation; `driversUK` handler calls `dataLst.get(5).size()` throwing `IndexOutOfBoundsException` if CSV has fewer than 6 rows; no file extension restriction; CSV content not sanitised.
Fix: Write tests for insufficient CSV rows, non-CSV file rejection, CSV injection blocking, and rollback on partial import failure.

[A03-7] HIGH | File: GdprDataDelete.java | Line: 59-101
Description: Queries all customers with `gdpr_data != 0` then deletes data for inactive drivers -- if `CUST_CD` join condition incorrect or `inactive_date` logic has off-by-one, wrong customer's data deleted; no test asserts customer isolation.
Fix: Write integration test with two customers and overlapping driver sets; assert isolation post-deletion.

[A03-8] HIGH | File: UtilBean.java | Line: 86, 196, 251, 305
Description: Four `public static` methods concatenate String parameters directly into SQL queries; called from JSP pages where parameters may originate from session or request attributes.
Fix: Write SQL injection tests passing `"1 OR 1=1"` for each method and null input tests; refactor to PreparedStatement.

[A03-9] HIGH | File: InfoLogger.java | Line: 59-66
Description: `writelog()` parses `msg` by character position to extract fields then interpolates all three into INSERT into `SEC_LOG_DETAILS` -- attacker controlling log message format could inject SQL into security audit table.
Fix: Write tests for SQL injection in uid position and malformed messages without `/` delimiters.

[A03-10] HIGH | File: FleetCheckFTP.java | Line: 229-244
Description: `gmtp_id` from `ftp_outgoing` table directly concatenated into INSERT and SELECT statements; FTP command embeds `RuntimeConf.firmwarepass` in plaintext in outgoing message table.
Fix: Write tests to verify SQL injection in `gmtp_id` is blocked and outgoing message does not contain literal firmware password.

[A03-11] HIGH | File: SendMessage.java | Line: 174-180
Description: Clickatell API credentials passed as plaintext HTTP query parameters; DELETE SQL at line 132 interpolates `id` directly; exception mid-loop may cause re-sent messages.
Fix: Write tests for null `unit_name` handling and SQL injection resistance in `id` parameter of DELETE.

[A03-12] HIGH | File: LindeConfig.java | Line: 52-136
Description: `DocumentBuilderFactory.newInstance()` uses default settings allowing external entity expansion (XXE) -- if config XML writable by attacker, XXE payloads read arbitrary server files.
Fix: Write tests for XXE prevention with malicious XML payload and for missing required configuration keys.

[A03-13] HIGH | File: DataUtil.java | Line: 600-604
Description: `escapeSpecialCharacter()` regex does NOT strip `/` or `..` -- name like `../../../etc` survives and produces traversal path under `RuntimeConf.firmwarefolder`.
Fix: Write tests asserting slashes stripped from output and null input returns null or empty without NPE.

[A03-14] HIGH | File: DateUtil.java | Line: 45-71
Description: Date format detection logic broken -- dates like `10/06/2024` (10th June) parsed as 6th October due to inverted conditional branches; ambiguous dates default to `MM/dd/yyyy` producing incorrect SQL dates silently.
Fix: Write tests for unambiguous dates (`"15/06/2024"` must parse to 15 June), ambiguous dates, and null input; fix broken format detection.

[A03-15] HIGH | File: Dt_Checker.java | Line: 141-150
Description: Leap year algorithm returns `true` for `y % 1000 == 0` (incorrect) and `false` for `y % 400 == 0` (inverted) -- year 2000 treated as NOT leap year; `days_Betn()` and `daysIn()` return wrong counts around 28 Feb.
Fix: Write tests for years 2000 (leap), 1900 (not leap), 3000 (not leap); test `days_Betn` across leap day boundaries; fix inverted logic.

[A03-16] HIGH | File: password_life.java:71, password_policy.java:69
Description: Both classes call `EncryptTest().encrypt(userid)` assigning result to `s`, but `s` is never used -- implies either authentication bypass (removed security check) or dead code where query uses raw `userid` (SQL injection risk).
Fix: Write tests to verify SQL query uses encrypted form of userid; add static analysis assertions that `s` is referenced post-assignment.

[A03-17] HIGH | File: ExcelUtil.java | Line: 37-39
Description: `Class.forName()` loads classes using unsanitised `rpt_name` parameter -- if user-controlled, attacker could load unintended classes; `getExportDir()` constructs path with `../../../../../../../../excelrpt/` which may resolve outside intended directory.
Fix: Write tests to verify unknown report names produce controlled exceptions and export directory resolves within expected web root.

[A03-18] MEDIUM | File: BeanComparator.java | Line: 33-172
Description: Reflection-based comparison does not restrict which methods can be invoked; if `methodName` caller-supplied, any public getter could be invoked including those with side effects; `compare()` catches Exception broadly masking real failures.
Fix: Write tests for ascending/descending string ordering, null value sorting, and invalid method names asserting `IllegalArgumentException`.

[A03-19] MEDIUM | File: DataUtil.java | Line: 776-798
Description: `removeDuplicateCds()` would crash on empty string input with `StringIndexOutOfBoundsException` due to `substring(0, length-1)` on empty result; `"0,0"` special case fails on `"0, 0"` (with space).
Fix: Write tests for empty string input, single value input, and duplicate removal correctness.

[A03-20] MEDIUM | File: DataUtil.java | Line: 862-899
Description: `calculateTime()` returns -1 on parse exception or invalid type; callers use `if(days <= 0)` so -1 error return triggers overdue alert branch, causing spurious "overdue" emails to all customers.
Fix: Write tests for known date pairs, invalid type strings, and null date inputs; consider throwing instead of returning -1.

[A03-21] MEDIUM | File: UtilBean.java | Line: 58-68
Description: `getDays()` accesses `noofdays[month - 1]` with no bounds check -- month 0 causes `ArrayIndexOutOfBoundsException` at index -1; month > 12 also out-of-bounds.
Fix: Write tests for all valid months, invalid month values (0, 13), and leap year February handling.

[A03-22] MEDIUM | File: LindeConfig.java | Line: 20-45
Description: All configuration fields (`siteName`, `externalURL`, `firmwareserver`, etc.) are `public static` non-final -- any class can overwrite at runtime; `RuntimeConf.mail_from` mutated inside `readXMLFile()`.
Fix: Write tests for UK and AU site configurations asserting expected field values; verify config fields immutable after initial load.

[A03-23] MEDIUM | File: escapeSingleQuotes.java | Line: 4-17
Description: Only doubles single quotes; does not escape backslash, comment sequences (`--`, `/*`), or semicolons -- callers relying on this for SQL injection protection are still vulnerable.
Fix: Write tests for quote doubling, null safety; document limitation that it does not provide complete SQL injection protection.

[A03-24] MEDIUM | File: SupervisorMasterHelper.java | Line: 18
Description: `user`, `loc_cd`, `cust_cd` concatenated directly into UPDATE, DELETE, and SELECT statements -- if session state compromised, injected SQL would delete arbitrary supervisor slot data.
Fix: Write tests passing SQL injection payloads like `"' OR '1'='1"` as user and assert no unintended rows modified.

[A03-25] LOW | File: CustomComparator.java | Line: 10-13
Description: `compare()` method has `// TODO Auto-generated method stub` comment never removed; implementation is single line (descending name sort) with no verified sort direction or null-safety.
Fix: Write test asserting descending order correct; remove TODO stub comment.

[A03-26] LOW | File: PurgeData.java | Line: 3-5
Description: Empty class with no methods or fields -- either planned functionality never implemented or purge logic living elsewhere; if data purge intended and omitted, data retention obligations may be unmet.
Fix: Document intent; if placeholder remove class or add comment confirming intentionally empty.

[A03-27] LOW | File: DataUtil.java | Line: 240-248
Description: Typo in method name (`generateRadomName` instead of `generateRandomName`); combines timestamp and UUID untested for format or uniqueness under rapid concurrent calls.
Fix: Write test asserting result matches expected `yyyyMMddHHmmss-<uuid>` pattern; fix method name typo.

[A03-28] LOW | File: DBUtil.java | Line: 20-57
Description: `getConnection()` throws generic `Exception`; no test verifies `closeConnection(null)` is safe; no test for behaviour when JNDI datasource unavailable.
Fix: Write test asserting `closeConnection(null)` does not throw.

### util-A-F

[A19-01] CRITICAL | File: ALL (repository-wide)
Description: Repository contains no test framework dependencies, no test directories, no test runner configuration, and no test files -- every public method across all 13 files has 0% automated test coverage.
Fix: Establish JUnit 5 test infrastructure with at minimum unit tests for pure-logic utility methods (DataUtil, DateUtil, Dt_Checker, BeanComparator, EncryptTest).

[A19-02] CRITICAL | File: DBUtil.java | Line: 20, 35, 51
Description: DBUtil is central connection factory used by all DB-dependent classes -- no tests for connection acquisition failure handling, closeConnection() on already-closed connections, or connection leak detection.
Fix: Add tests for JNDI lookup failure, pool exhaustion, already-closed connection handling; replace raw Exception throws with specific exception types.

[A19-03] CRITICAL | File: CftsAlert.java, DriverExpiryAlert.java, DriverMedicalAlert.java, FleetCheckFTP.java | Line: various
Description: All four classes build SQL via string concatenation with variables from database result sets -- values like cust, site, email, message, gmtp_id concatenated directly into SQL.
Fix: Convert all string-concatenated queries to PreparedStatement with parameterized queries; add tests for query correctness and injection resistance.

[A19-04] CRITICAL | File: EncryptTest.java | Line: 16, 97
Description: Encryption class uses simple character-shift cipher (trivial obfuscation, not real encryption) -- no round-trip tests, no edge-case tests for empty strings, nulls, or Unicode.
Fix: Add round-trip correctness tests, edge-case tests; evaluate replacing algorithm with proper encryption standard (AES).

[A19-05] HIGH | File: Dt_Checker.java | Line: 141
Description: `isleap()` uses `y%1000` instead of `y%100` and returns false for `y%400` instead of true -- year 1900 incorrectly identified as leap; year 2400 incorrectly non-leap.
Fix: Replace with correct algorithm (divisible by 4, except centuries unless also divisible by 400); add parameterized tests.

[A19-06] HIGH | File: Dt_Checker.java | Line: 6-7
Description: Static mutable fields (date1, dd, mm, yy) written by `first()` and `last()` -- in multi-threaded Tomcat concurrent calls corrupt shared state.
Fix: Replace static fields with local variables within each method; add concurrent test cases.

[A19-07] HIGH | File: DateUtil.java | Line: 45
Description: `stringToSQLDate()` auto-detects dd/MM/yyyy vs MM/dd/yyyy by checking if values exceed 12 -- ambiguous dates like 05/06/2024 silently pick dd/MM/yyyy with no way to distinguish 5th June from May 6th.
Fix: Add tests for ambiguous date inputs; consider requiring single consistent format or accepting format as parameter.

[A19-08] HIGH | File: DataUtil.java
Description: 40+ pure-logic static methods (1087 lines) with zero tests -- `maxValue(double[])` crashes on empty array, `convert_time(int)` infinite loops on extremely negative values, `formatStringDate` throws on short strings, `getRandomString` has off-by-one, `checkDateFormat` has incorrect regex.
Fix: Add unit tests for all pure static methods focusing on empty/null inputs, boundary values, and specific bugs identified.

[A19-09] HIGH | File: DataUtil.java, CustomUpload.java | Line: 918, 936, 45, 307
Description: `uploadLicenceFile()`, `uploadDocumentFile()`, and `CustomUpload.doPost()` do not validate file paths stay within intended directories -- `../` sequences could write files to arbitrary server locations.
Fix: Add path traversal validation (canonicalize and verify resolved path starts with intended base directory); add tests with malicious filenames.

[A19-10] HIGH | File: CustomUpload.java | Line: 45, 55, 108, 219, 221, 327
Description: Hardcoded email recipient, hardcoded file path causing concurrent request conflicts, hardcoded FTP credentials in source, SQL injection via string concatenation, no authentication in doPost(), unclosed BufferedReader.
Fix: Externalize credentials/configuration; use PreparedStatement; add authentication checks; use try-with-resources; add servlet integration tests.

[A19-11] HIGH | File: BeanComparator.java | Line: 106
Description: Reflection-based `compare()` untested for IllegalAccessException, InvocationTargetException, non-Comparable return types, null arguments causing NPE; uses raw Comparator type with no generic safety.
Fix: Add unit tests covering reflection failure cases, null arguments, non-Comparable types; add generic type parameters.

[A19-12] HIGH | File: ExcelUtil.java | Line: 34, 61, 84, 107
Description: `getExcel()`, `getEmail()`, `getPrintBody()` use `Class.forName()` with unsanitized `rpt_name` enabling arbitrary class instantiation; `downloadExcel()` reads files byte-by-byte without buffering.
Fix: Validate `rpt_name` against allowlist of known report classes; use buffered I/O; add tests for valid and malicious class name inputs.

[A19-13] HIGH | File: FleetCheckFTP.java | Line: 24
Description: 250-line monolithic `upload_quest_ftp()` combines DB queries, filesystem directory creation, binary file writing, FTP command insertion, and record deletion -- all with string-concatenated SQL and no testable decomposition.
Fix: Decompose into smaller testable methods; convert to PreparedStatement; add integration tests with DB and filesystem mocking.

[A19-14] MEDIUM | File: DriverMedicalAlert.java | Line: 16
Description: Shared static SimpleDateFormat instance not thread-safe -- concurrent Tomcat requests produce corrupted date strings or NumberFormatException.
Fix: Replace with thread-local SimpleDateFormat, DateTimeFormatter (Java 8+), or local instances; add concurrent tests.

[A19-15] MEDIUM | File: CustomComparator.java | Line: 10
Description: `compare()` calls `getDriverName().compareTo()` without null checks -- null bean or null getDriverName() throws NPE.
Fix: Add null-safety checks for both bean arguments and driver name values; add unit tests including null cases.

[A19-16] MEDIUM | File: CftsAlert.java, DriverExpiryAlert.java, DriverMedicalAlert.java | Line: various
Description: All three alert classes catch Exception, call `e.printStackTrace()` and `e.getMessage()` (return value discarded), then silently continue -- partial alert processing failures ignored.
Fix: Replace with proper logging; propagate or record errors for monitoring; remove no-op `e.getMessage()` calls.

[A19-17] MEDIUM | File: DateUtil.java | Line: 16, 189, 208
Description: `stringToDate()`, `stringToTimestamp()`, `stringToTimestampHM()` catch ParseException, print to stdout, return null -- callers not checking for null get NPE at a distance.
Fix: Either throw checked exception or return Optional; document null-return contract; add tests for unparseable input.

[A19-18] MEDIUM | File: DataUtil.java | Line: 329, 936
Description: `saveImage()` closes streams sequentially without try-with-resources -- if `os.close()` throws, `is` remains open; `uploadDocumentFile()` never closes outStream causing resource leak.
Fix: Use try-with-resources for all stream handling; add tests for proper resource cleanup.

[A19-19] LOW | File: DataUtil.java | Line: 528
Description: `getRandomString()` loop uses `i <= length` generating length+1 characters -- `getRandomString(8)` returns 9-character string.
Fix: Change loop condition to `i < length`; add test asserting returned string length equals requested length.

[A19-20] LOW | File: DataUtil.java | Line: 754
Description: `checkDateFormat()` year regex `[20]{2}` is character class matching any combination of '2' and '0' (matches "00xx", "02xx", "22xx") not literal prefix "20" -- invalid dates like "01/01/0099" match.
Fix: Replace `[20]{2}` with literal `20` in regex; add tests with valid and invalid year prefixes.

### util-G-Z

[A20-01] CRITICAL | File: GdprDataDelete.java | Line: 29-140
Description: `call_gdpr_delete_data()` performs irreversible DELETE operations across 6+ tables for GDPR compliance with no unit tests, no transaction management (partial deletes possible), and SQL injection via string concatenation of `cust_cd`, `driver_cd`, `gdpr_data`.
Fix: Add unit tests for deletion scope, 30-day threshold logic, partial failure/rollback, and invalid `gdpr_data` values; use prepared statements and wrap in transaction.

[A20-02] CRITICAL | File: password_life.java, password_policy.java, PasswordExpiryAlert.java | Line: various
Description: Three files governing password security (expiry, policy enforcement, alert emails) have zero test coverage -- risks include silent expiry bypass on exception, hardcoded 3-month/7-day windows, email SQL injection, and Oracle-specific SQL that may fail on PostgreSQL.
Fix: Add tests for password expiry calculation, boundary edge cases, empty table behavior, email validation, and alert idempotency; parameterize SQL and externalize expiry configuration.

[A20-03] CRITICAL | File: RuntimeConf.java | Line: 20, 30, 54-55, 87-88
Description: Multiple production credentials hardcoded in source (FTP firmware password `"Sdh79HfkLq6"`, legacy `"ciifirmware"`, test credentials `"TestK"/"testadmin"`, SMS API credentials `"fOqDVWYK"` / API ID `"3259470"`) all committed to version control.
Fix: Move all credentials to secure external configuration (environment variables, vault); add tests ensuring RuntimeConf values overridden by external config.

[A20-04] HIGH | File: All 24 files except PurgeData.java, escapeSingleQuotes.java, RuntimeConf.java
Description: Every file executing SQL uses string concatenation instead of prepared statements; `escapeSingleQuotes` utility provides only single-quote doubling which is insufficient.
Fix: Replace all string concatenation with parameterized prepared statements; add tests with adversarial input including `'; DROP TABLE --`, Unicode bypasses, and null byte injection.

[A20-05] HIGH | File: mail.java, call_mail.java | Line: 109-145, 147-203, 205-259
Description: All `sendMail` variants return `true` regardless of whether email was sent, catching `Throwable` and still returning success -- callers cannot detect delivery failures for password resets, alerts, or reports.
Fix: Return `false` on exception; add tests verifying correct return values on success, transport failure, and invalid recipient.

[A20-06] HIGH | File: ImportFiles.java | Line: 49-2300
Description: `ImportFiles` servlet handles file uploads and DB modifications (~2700 lines) with no authentication checks, no file-type/size validation, path construction via concatenation (path traversal), and complex CSV parsing with zero test coverage.
Fix: Add authentication, file-type allowlisting, size limits, path traversal protection; write tests for CSV parsing with malformed input, path traversal, oversized files.

[A20-07] HIGH | File: MigrateMaster.java | Line: 18-323
Description: `callMigrateMaster()` performs complex multi-table data migration (deletes, inserts, updates `supervisor_access`) for all active customers in single 325-line method with no transaction boundaries -- database inconsistent on mid-migration failure.
Fix: Wrap migration in transaction with rollback; add tests for single-customer migration, empty vehicle lists, mid-migration errors.

[A20-08] HIGH | File: fix_department.java | Line: 97-306
Description: `fix_dept()` cascades department code changes across 12 database tables without transaction wrapping -- failure at any point breaks referential integrity; SQL injection via `user_cd`, `loc_cd`, `dept_cd` concatenation.
Fix: Wrap 12-table cascade in transaction with rollback; use prepared statements; add tests for duplicate detection, full cascade completion, rollback on failure.

[A20-09] HIGH | File: send_timezone.java | Line: 86-88
Description: In `call_send_timezone()`, INSERT query executed twice on lines 86 and 88 causing every vehicle to receive duplicate timezone messages on DST transition days.
Fix: Remove duplicate `executeUpdate()` call; add tests verifying single message per vehicle per DST transition.

[A20-10] MEDIUM | File: InfoLogger.java | Line: 28-83
Description: `writelog()` parses `msg` using `indexOf('/')` and `indexOf(']')` without bounds checking causing `StringIndexOutOfBoundsException` if format deviates; extracted values directly inserted into SQL via concatenation.
Fix: Add bounds/null checking before `substring()` calls; use prepared statements; add tests for expected format, missing delimiters, and SQL injection payloads.

[A20-11] MEDIUM | File: LindeConfig.java | Line: 63-65
Description: `DocumentBuilderFactory` used without disabling external entities -- XXE attacks could read local files or perform SSRF if XML configuration file tampered with.
Fix: Configure `DocumentBuilderFactory` to disable DTDs and external entities; add tests for valid XML, missing/malformed XML, and XXE payload rejection.

[A20-12] MEDIUM | File: Menu_Bean1.java | Line: 192-197
Description: In `fetchSubModule()`, raw SQL query string appended to `FormName` ArrayList, exposing database schema information to JSP page rendering the menu.
Fix: Remove debug line adding query to `FormName`; add tests verifying `FormName` contains only valid form names.

[A20-13] MEDIUM | File: GetHtml.java | Line: 16-38
Description: `getHTML(urlToRead, param)` constructs URL by simple concatenation without validation or allow-listing -- SSRF to access internal resources if either parameter user-controlled.
Fix: Add URL validation and allowlisting; add tests for internal/private IP addresses, non-HTTP protocols, timeout handling.

[A20-14] MEDIUM | File: escapeSingleQuotes.java | Line: 4-16
Description: `replaceSingleQuotes()` only doubles single quotes; does not handle backslash escaping, null byte injection, Unicode bypass, or other SQL metacharacters -- primary SQL escaping utility used inconsistently.
Fix: Replace usage with prepared statements throughout; add tests for escaping, backslash, null/empty input, Unicode, multi-byte sequences.

[A20-15] MEDIUM | File: UtilBean.java | Line: 29, 178-233, 235-288
Description: `static CustomerBean customer` field shared across all threads; both `getCustomerSettingByUser()` and `getCustomerSetting()` write to and return this field -- concurrent requests overwrite each other's results.
Fix: Remove static shared field; return new `CustomerBean` from each call; add concurrent access tests.

[A20-16] MEDIUM | File: send_updatepreop.java | Line: 106-116
Description: In `updatepreop()`, UPDATE query for correcting pre-op question text is built but `executeUpdate()` never called -- question text correction silently non-functional.
Fix: Add missing `executeUpdate()` call; add tests verifying mismatched questions actually updated.

[A20-17] LOW | File: PurgeData.java | Line: 1-5
Description: `PurgeData` class completely empty with no methods or fields -- dead code or unfinished implementation; if data purging required beyond `GdprDataDelete`, represents missing feature.
Fix: Implement intended purge functionality or remove dead class.

[A20-18] LOW | File: SendMessage.java | Line: 177, 236
Description: `URLEncoder.encode(message)` uses deprecated single-arg method (platform-default encoding); `DataInputStream.readLine()` deprecated since Java 1.1 -- encoding issues with special characters.
Fix: Use `URLEncoder.encode(message, "UTF-8")`; replace `DataInputStream.readLine()` with `BufferedReader.readLine()`.

### bean-A-D

[A01-1] CRITICAL | File: (repository-wide)
Description: Entire FleetFocus repository contains zero test files, no test directories, no JUnit/TestNG dependencies, and no test runner configuration -- every class has 0% test coverage.
Fix: Establish test framework (JUnit 5 + Maven/Gradle) with `src/test/java` directory and configure CI to run tests on every commit.

[A01-2] HIGH | File: DailyUsageHourBean.java | Line: 39
Description: `arrangeData(String modelName)` contains nested iteration, shared state mutation, comma-delimited string construction, and potential NPE if `this.week` is null at line 49.
Fix: Write unit tests covering normal matching, null `this.week`, empty deptDataList, multiple departments with same model, edge-case doubles (NaN, Infinity).

[A01-3] HIGH | File: DailyUsageHourBean.java | Line: 27
Description: `getModelList()` is getter with side effects that modifies `modelList` on every call, iterates `deptDataList` to extract unique model names, and wastes allocation with unnecessary `new DailyUsageDeptDataBean()`.
Fix: Write tests for empty deptDataList, duplicate model name deduplication, and idempotency across multiple calls.

[A01-4] HIGH | File: DailyUsageHourBean.java | Line: 101
Description: `getWeekList(String model)` has getter-with-side-effects anti-pattern; uses `equalsIgnoreCase` for model comparison but exact equality for week deduplication.
Fix: Test with multiple weeks for same model, same week for different models, case sensitivity on model name, repeated calls not duplicating entries.

[A01-5] MEDIUM | File: DetailedReportUtil.java | Line: 44
Description: `analyzeAndCombine()` iterates `vrpt_field_nm` checking for "Hydraulic"/"HYDR"/"HYDL" strings but conditional block body is completely empty -- dead code or incomplete implementation.
Fix: Write tests verifying method does not throw on empty lists or matching field names; investigate whether dead code or unfinished feature.

[A01-6] MEDIUM | File: DetailedReportUtil.java | Line: 34
Description: Parameterized constructor writes debug output via `System.out.println` exposing internal data sizes -- leaks information in production and pollutes logs.
Fix: Write tests verifying construction with various ArrayList sizes and null ArrayLists; mark `System.out.println` for removal.

[A01-7] HIGH | File: CustomerBean.java | Line: 6
Description: `passwordPolicy` boolean defaults to false -- if false means enforcement disabled, new instances silently skip password complexity enforcement.
Fix: Write tests verifying default values of `passwordPolicy` and `active`; document whether false default is intentional.

[A01-8] HIGH | File: CanruleBean.java | Line: 14
Description: Four access control fields (access_level, access_cust, access_site, access_dept) all default to null; bean does not implement Serializable risking session replication issues.
Fix: Write tests verifying access fields default to null and getter/setter round-trips; integration tests for null access field handling.

[A01-9] HIGH | File: DriverImportBean.java | Line: 26
Description: Safety-critical `denyOnExp` boolean defaults to false (expired-license drivers not denied access by default); `expirydt` stored as String with no format validation.
Fix: Write tests verifying `denyOnExp` defaults to false; document whether this is safe default; verify all 24 fields round-trip correctly.

[A01-10] LOW | File: BatteryBean.java | Line: 5
Description: Pure getter/setter bean with 22 fields tracking battery swap events -- incorrect serialization or field mapping could cause battery tracking data loss.
Fix: Write basic tests verifying default field values, getter/setter round-trips for all 22 fields.

[A01-11] LOW | File: BroadcastmsgBean.java | Line: 5
Description: Serializable DTO carrying broadcast message data (text, type, timestamps, driver, unit, vehicle ID) with 10 String fields all defaulting to null.
Fix: Write basic getter/setter and serialization round-trip tests.

[A01-12] LOW | File: CustLocDeptBean.java | Line: 3
Description: Minimal 3-field bean (custCd, locCd, deptCd as ints) for customer-location-department hierarchy mapping with no Serializable implementation.
Fix: Write basic getter/setter tests; consider adding Serializable for consistency.

[A01-13] LOW | File: DailyUsageDeptDataBean.java | Line: 6
Description: Serializable DTO with 10 fields for daily usage reporting; `data` field (`ArrayList<double[]>`) is mutable and could be externally modified after construction.
Fix: Write tests for parameterized constructor setting all fields; verify data ArrayList mutability understood.

[A01-14] LOW | File: DashboarSubscriptionBean.java | Line: 3
Description: Class name typo ("Dashboar" vs "Dashboard"); carries `emailId` (PII) with no validation; does not implement Serializable.
Fix: Write getter/setter tests; consider adding Serializable; document class name typo.

[A01-15] LOW | File: DayhoursBean.java | Line: 5
Description: Serializable DTO with 7 fields tracking work hours; `avail_hours` defaults to "00:00:00".
Fix: Write basic getter/setter and serialization tests; verify `avail_hours` format consistency.

[A01-16] LOW | File: DehireBean.java | Line: 5
Description: Minimal 3-field bean using `java.sql.Timestamp` directly (JDBC type coupling); does not implement Serializable.
Fix: Write basic getter/setter tests; consider adding Serializable.

[A01-17] LOW | File: DriverBean.java | Line: 5
Description: Serializable DTO with 4 fields including `weigand` (Wiegand access card number -- physical access credential); all fields default to empty string.
Fix: Write getter/setter and serialization tests; note weigand stores credential-adjacent value.

[A01-18] LOW | File: DriverLeagueBean.java | Line: 3
Description: Driver performance data with 9 fields including redImpact, preOp, keyHour stored as Strings rather than numeric types -- sorting/comparison issues possible; does not implement Serializable.
Fix: Write basic getter/setter tests.

### bean-E-P

[A02-1] CRITICAL | File: NetworkSettingBean.java | Line: 10
Description: WiFi credentials (ssid and password) stored as plaintext Strings with no encryption, masking, or access control; `getPassword()` returns raw password; missing serialVersionUID despite implementing Serializable.
Fix: Write tests verifying serialization round-trip; add serialVersionUID; consider encrypting password at rest.

[A02-2] CRITICAL | File: LockOutBean.java | Line: 17
Description: `master_code` field (lockout bypass/master unlock code for fleet vehicles) exposed as plain string via `getMaster_code()` with zero tests for secure handling or accidental serialization to logs.
Fix: Write tests for master_code getter/setter contract and serialization behavior; consider redacting from serialized output.

[A02-3] CRITICAL | File: LicenseBlackListBean.java | Line: 13-16
Description: Access-level authorization fields (access_level, access_cust, access_site, access_dept) initialized to null (not empty string); `vehicleCds` getter returns null unless set risking NPE.
Fix: Write tests verifying null defaults for access fields vs empty-string defaults for other fields; test vehicleCds null safety.

[A02-4] HIGH | File: ImpactBean.java | Line: 47
Description: `addImactMap(int, int)` mutates internal HashMap plus fixed-size arrays (int[8], int[8][3]) for impact monitoring -- zero tests for insertion/overwrite, array bounds, or aggregated totals; method name typo ("Imact").
Fix: Write tests for addImactMap (add, overwrite, boundary month values), default array sizes, serialization with populated arrays.

[A02-5] HIGH | File: PreCheckBean.java | Line: 29
Description: `addCheckMap(String, int)` aggregates pre-check completion data by driver name into HashMap plus complete/incomplete/total counts -- zero tests for mutation, consistency of complete + incomplete = total, duplicate driver name, null key.
Fix: Write tests for addCheckMap with null key, duplicate keys, empty string keys; verify complete/incomplete/total arithmetic.

[A02-6] HIGH | File: MymessagesUsersBean.java | Line: 16-17
Description: Stores user identity info (user_id, user_email) and notification threshold (String not numeric); field name typo "descrption" (missing 'i').
Fix: Write tests for getter/setter round-trip; verify threshold String parseable by downstream consumers.

[A02-7] MEDIUM | File: ImpactLocBean.java | Line: 50
Description: Three beans form hierarchy (ImpactLocBean -> ImpactDeptBean -> ImpactSummaryBean -> ImpactBean) with convenience add methods and total fields -- zero tests for add methods, total consistency, or hierarchical integrity; ImpactSummaryBean missing serialVersionUID.
Fix: Write integration tests building full hierarchy; verify add methods and totals reconcile at each level.

[A02-8] MEDIUM | File: PreCheckSummaryBean.java | Line: 34
Description: Aggregates PreCheckBean instances by location with `addArrPrecheck()`; PreCheckDriverBean's `checks` int[] defaults to null -- zero tests for list building, total consistency, or null checks array.
Fix: Write tests for addArrPrecheck with null argument, null checks array access, serialization.

[A02-9] MEDIUM | File: MaxHourUsageBean.java | Line: 36
Description: Aggregates unit utilization data with `addArrUnitUtil()`; FleetCheckBean exposes `frequent_failed_question` as mutable ArrayList allowing callers to modify internal state.
Fix: Write tests for addArrUnitUtil with null argument; test mutable list exposure.

[A02-10] MEDIUM | File: MenuBean.java | Line: 11
Description: Stores menu navigation config including `Form_Path` and `ReskinPath` (URL/path values) -- malformed or manipulated values could lead to open redirect or path traversal.
Fix: Write tests verifying getter/setter contracts; document expected path format.

[A02-11] LOW | File: EntityBean.java
Description: Simple Serializable data bean with 6 fields and only getter/setter methods (55 lines, no business logic); zero tests.
Fix: Low priority; write basic round-trip getter/setter and serialization tests.

[A02-12] LOW | File: NotificationSettingsBean.java
Description: Simple data bean with notification template fields and enabled boolean (51 lines, no complex logic); zero tests.
Fix: Low priority; write basic getter/setter tests; verify boolean default (false).

### bean-Q-Z

[A03-001] CRITICAL | File: All 20 bean files (Q-Z range)
Description: None of the 20 bean files have any unit tests; repository has no test framework, test directories, test runner, or build tool.
Fix: Introduce JUnit 4/5 and build tool (Maven/Gradle); prioritize tests for ServiceDueFlagBean.java; generate basic getter/setter round-trip tests for remaining 19 POJOs.

[A03-002] CRITICAL | File: ServiceDueFlagBean.java | Line: 104-165
Description: `init()` performs JNDI context lookup, obtains DB connection, dispatches to different private methods based on opCode -- no tests for correct dispatch, error handling on null context, or cleanup in finally block.
Fix: Write integration tests with embedded database or mocked DataSource; test each opCode branch independently; verify resource cleanup in all paths.

[A03-003] CRITICAL | File: ServiceDueFlagBean.java | Line: 557, 568-592, 637-660, 735-807, 895-904, 947, 980
Description: Multiple methods construct SQL via string concatenation with user-controlled values -- no tests validate input sanitization occurs upstream.
Fix: Create parameterized query tests verifying SQL injection prevented; refactor to PreparedStatement.

[A03-004] HIGH | File: ServiceDueFlagBean.java | Line: 956-963
Description: `convertServiceHourAvg()` divides by `(36000 * days)` -- if days is 0, causes ArithmeticException or Infinity/NaN; no tests validate edge case.
Fix: Add tests for days=0, days=1, negative days, normal values; add guard clause for zero days.

[A03-005] HIGH | File: ServiceDueFlagBean.java | Line: 609-617
Description: `convertServiceHour()` divides milliseconds by 36000 to produce hours assuming 1/10th-second units rather than actual milliseconds -- no tests verify correctness; cast to float may lose precision for large values.
Fix: Write tests verifying conversion factor and precision; test boundary values (0, Long.MAX_VALUE, negative).

[A03-006] HIGH | File: ServiceDueFlagBean.java | Line: 619-632
Description: `getColourStatus()` returns HTML style strings based on hour thresholds (>=25 green, 6-24 orange, <=5 red) -- no tests verify boundary values or returned HTML styles.
Fix: Write tests for boundary values: 0, 5, 6, 24, 25, 26, and negative hours.

[A03-007] HIGH | File: ServiceDueFlagBean.java | Line: 543-561
Description: `testQueries()` public method executes SQL in a loop `count` times with no upper bound, incrementing hex values and timestamps via string concatenation -- could be used for denial-of-service.
Fix: Add tests for count=0, count=1, invalid hex values; add upper bound on count parameter.

[A03-008] MEDIUM | File: ServiceDueFlagBean.java | Line: 44-62
Description: All 17 ArrayList fields use raw types without generics allowing any object type insertion -- potential ClassCastException at runtime.
Fix: Add generics to all ArrayList declarations; write tests verifying type safety.

[A03-009] MEDIUM | File: ServiceDueFlagBean.java | Line: 278-524
Description: All ArrayList getter methods return direct references to internal mutable lists; `getStmt()`/`getStmt1()` expose raw JDBC Statement objects -- external mutation corrupts internal state.
Fix: Write tests demonstrating external mutation; return defensive copies; remove Statement getters/setters.

[A03-010] HIGH | File: ServiceDueFlagBean.java | Line: 742
Description: When `is_user_lmh` true and `set_cust_cd` is "all", `access_cust.substring(2, access_cust.length())` called without null-checking -- risks NPE or StringIndexOutOfBoundsException.
Fix: Add tests for null access_cust, empty string, single-character string; add null/length checks.

[A03-011] HIGH | File: SFTPSettings.java | Line: 8
Description: `sftpPass` stores SFTP credentials as plain-text String with no encryption or masking.
Fix: Create tests verifying passwords encrypted before storage; consider using char[] or encryption wrapper.

[A03-012] HIGH | File: VehNetworkSettingsBean.java | Line: 31
Description: `password` field stores network password as plain-text String with no tests verifying secure handling.
Fix: Encrypt password storage; add tests verifying encryption.

[A03-013] MEDIUM | File: RestrictedAccessUsageBean.java | Line: 5
Description: Fields `hourlyRate`, `maxMonthlyRate`, `totalCharge` represent monetary values but stored as Strings -- no verification of numeric validity, precision, or calculation correctness.
Fix: Write tests verifying financial values parse correctly; consider BigDecimal for financial fields.

[A03-014] MEDIUM | File: UnitutilBean.java | Line: 78-79
Description: `setUtil(int i, int util)` directly indexes into fixed-size array of 8 without bounds checking -- index < 0 or >= 8 throws ArrayIndexOutOfBoundsException.
Fix: Write tests for i=-1, i=0, i=7, i=8; add bounds checking.

[A03-015] MEDIUM | File: UnitUtilSummaryBean.java | Line: 15-25
Description: All hour and percentage fields stored as Strings initialized to "0" -- no verification they parse safely as numbers by consuming code.
Fix: Write tests verifying round-trip numeric consistency; consider numeric types.

[A03-016] LOW | File: UserFormBean.java | Line: 9-10
Description: Fields `userFomrCd` and `userFomrName` contain typo "Fomr" instead of "Form" with corresponding getters/setters; renaming without tests has unknown blast radius.
Fix: Add tests and search for all callers before fixing typo; use IDE refactoring.

[A03-017] INFO | File: UserFormBean.java | Line: 3
Description: `import java.util.ArrayList` declared but never used.
Fix: Remove unused import.

[A03-018] MEDIUM | File: 12 of 20 beans (SiteConfigurationBean.java, SpecialAccessBean.java, SubscriptionBean.java, UnitBean.java, UnitUtilSummaryBean.java, UnitutilBean.java, UnusedUnitBean.java, UserBean.java, UserDriverBean.java, UserFormBean.java, VehDiagnostic.java, VehNetworkSettingsBean.java)
Description: 12 beans declare fields with default (package-private) access instead of private -- any class in same package can bypass getters/setters and directly modify fields.
Fix: Change all fields to private; write tests to verify getter/setter contracts; search for direct field access before changing visibility.

[A03-019] MEDIUM | File: ServiceDueFlagBean.java | Line: 129-133, 912-916
Description: Exception handling uses `System.out.println` and `printStackTrace()` instead of proper logging; errors swallowed silently with no notification to callers.
Fix: Add tests verifying error propagation; replace `System.out` with logging framework.

[A03-020] HIGH | File: ServiceDueFlagBean.java | Line: 545
Description: SimpleDateFormat uses pattern `"yyyy-MM-dd hh:mm:ss.ms"` where `hh` is 12-hour format (should be `HH`) and `ms` is invalid (should be `SSS` for milliseconds) -- produces incorrect date parsing results.
Fix: Write tests verifying date parsing; fix pattern to `"yyyy-MM-dd HH:mm:ss.SSS"`.

### master

[A15-01] CRITICAL | File: Databean_customer.java | Line: 331-534, 547-2989
Description: `query(String op_code)` and every `Query_*` sub-method construct SQL by concatenating instance field values (`Param_User`, `Param_Customer`, `Param_Site`, `Param_Search`, `access_user`) without parameterized queries or input sanitization.
Fix: Replace all string-concatenated SQL with parameterized prepared statements; add input sanitization on every `setParam_*` setter.

[A15-02] CRITICAL | File: Frm_saveuser.java | Line: 4108-4380
Description: `save_user` method and virtually all other handler methods construct INSERT/UPDATE/DELETE SQL by concatenating `request.getParameter()` values directly -- no prepared statements anywhere across 70+ operations.
Fix: Replace all concatenated SQL with prepared statements; validate every request parameter; ensure transaction integrity for multi-statement operations.

[A15-03] CRITICAL | File: Databean_getuser.java | Line: 5383-5395 (pervasive, 10,675 lines)
Description: All query methods use string concatenation with setter-injected values (`set_cust_cd`, `set_loc_cd`, `set_dept_cd`, `Param_User`) directly interpolated into SQL including unquoted numeric injections.
Fix: Convert all ~40+ private query methods to parameterized queries; add input validation for all setter-injected values.

[A15-04] CRITICAL | File: Frm_upload.java | Line: 109-156
Description: `loadData` accepts file uploads with no validation of file type/extension, file size, or filename; files written to web-accessible `/images/pics/` with only weak random prefix (0-999); filename not sanitized against path traversal.
Fix: Add file type allowlist, enforce size limits, sanitize filenames, increase random prefix entropy, store outside web-accessible directory.

[A15-05] CRITICAL | File: Frm_saveuser.java, Databean_customer.java | Line: 4119, 4199, 4268, 4298, 4310, 1535, 1612, 2838
Description: Passwords read from HTTP request as plaintext, only escaped for single quotes (no hashing), stored directly in DB as plaintext, and retrieved/exposed through getter.
Fix: Implement password hashing (bcrypt) before storage; remove plaintext password retrieval; add password strength validation and constant-time comparison.

[A15-06] HIGH | File: Databean_customer.java | Line: 1814
Description: Line 1814 has guaranteed NPE: `if(Param_Search == null && Param_Search.equalsIgnoreCase(""))` -- if null, first condition true then `.equalsIgnoreCase("")` called on null; same bug at line 1854.
Fix: Change `&&` to `||` or rewrite as `if(Param_Search == null || Param_Search.isEmpty())`; apply same fix at line 1854.

[A15-07] HIGH | File: FirmwareverBean.java | Line: 38-49, 89-177, 179-209, 211-243
Description: `setCurr_ver(String version)` calls `Long.parseLong(version, 16)` throwing NFE for non-hex input; `version.equalsIgnoreCase(null)` always returns false instead of null check; cascading substring/re-parse can throw further exceptions.
Fix: Replace `version.equalsIgnoreCase(null)` with `version == null`; add try-catch for NFE in `convert32bit`; guard `substring(1)` against empty/single-character strings.

[A15-08] HIGH | File: Frm_upload.java | Line: 46-67, 69-100
Description: `init()` acquires DB connection and creates statements as instance fields that are never closed; `doPost()` acquires another connection leaking first; `stmt1` referenced in `doPost()` only created in `init()` and may be null; no try-with-resources or finally block.
Fix: Use try-with-resources; eliminate instance-level connection/statement fields; ensure cleanup in finally blocks.

[A15-09] HIGH | File: Frm_saveuser.java | Line: 35
Description: Implements deprecated `SingleThreadModel` (deprecated since Servlet 2.4) and stores request-scoped data (`dbcon`, `stmt`, `rset`, `op_code`, `form_cd`, `url`, `message`) in instance fields -- unsafe for concurrent requests.
Fix: Remove `SingleThreadModel`; move all request-scoped data to local variables within `doPost()`; use connection pooling.

[A15-10] HIGH | File: Frm_saveuser.java | Line: 4108-4380
Description: `save_user()` reads ~25+ HTTP request parameters passed directly into SQL with no validation -- no email format, phone format, length checks, character restrictions, or numeric validation; `user_lnm.substring(0,3)` at line 4223 throws SIOOBE for names under 3 characters.
Fix: Add comprehensive input validation for every parameter; fix substring guard to check `length() >= 3`.

[A15-11] MEDIUM | File: Databean_customer.java | Line: 1296-1306
Description: Line 1303 has hardcoded customer name check `if (!cust_name.equalsIgnoreCase("James Hardie Australia"))` controlling `unauthorised_driver` alert type -- brittle business logic dependency on specific string.
Fix: Replace hardcoded customer name with configurable database flag or feature toggle.

[A15-12] MEDIUM | File: Frm_saveuser.java | Line: 5199-5205
Description: Email validation regex has unescaped dot after domain part matching any character instead of literal dot -- allows invalid emails like `user@hostXcom` to pass.
Fix: Escape dot in regex as `\\.`; alternatively consolidate on `InternetAddress.validate()` method existing elsewhere.

[A15-13] LOW | File: Databean_user.java | Line: 1-45
Description: Class declares 10 fields and imports 15 packages but has zero methods -- dead code or incomplete refactoring artifact.
Fix: Determine if referenced anywhere; if unused remove entirely.

[A15-14] MEDIUM | File: Frm_upload.java | Line: 26-44
Description: Stores all operational state (`dbcon`, `stmt`, `rset`, `message`, `url`, `op_code`) as instance fields without any thread safety mechanism (not even `SingleThreadModel`) -- concurrent requests corrupt each other's state.
Fix: Move all operational state to local variables within `doPost()`; use request-scoped connections.

[A15-15] MEDIUM | File: All files
Description: Error handling exposes internal details: exception messages in JSON (Frm_upload.java line 153), full exceptions with query details to stdout (Databean_customer.java line 479), `e.printStackTrace()` (Frm_saveuser.java line 406), no structured logging.
Fix: Replace `System.out.println` and `printStackTrace` with structured logging; return generic error messages; ensure output contains no SQL, stack traces, or PII.

[A15-16] MEDIUM | File: FirmwareverBean.java | Line: 211-243
Description: In `getType(String version)`, when `Long.parseLong(version, 16)` throws NFE, code does `version.substring(1)` and retries -- single character input produces empty string causing uncaught NFE.
Fix: Add length check before `substring(1)`; wrap retry parse in try-catch or return default.

### dashboard

[A08-01] CRITICAL | File: Config.java | Line: 32-70
Description: Request parameters `cust_cd`, `loc_cd`, `dept_cd` and session attribute `user_cd` concatenated directly into SQL without parameterization -- textbook SQL injection.
Fix: Use PreparedStatement with parameterized queries for all SQL in `getCustomers()`.

[A08-02] CRITICAL | File: CriticalBattery.java, Impacts.java, Licence.java, Preop.java, Summary.java, TableServlet.java, Utilisation.java | Line: various
Description: Every servlet constructs SQL by concatenating unsanitized HTTP request parameters (`cust_cd`, `loc_cd`, `dept_cd`, `start_time`, `end_time`, `st_dt`, `to_dt`, `search_crit`) -- no PreparedStatement used anywhere.
Fix: Replace all string-concatenated SQL with PreparedStatement parameterized queries across all 7 servlets.

[A08-03] HIGH | File: All 7 dashboard servlets | Line: various
Description: Every servlet reads `req.getParameter("part")` without null-checking -- absent `part` parameter causes `switch(part)` to throw NPE, resulting in unhandled 500 error.
Fix: Add null check on `part` parameter before switch; return 400 error response if missing.

[A08-04] HIGH | File: Impacts.java, CriticalBattery.java, Preop.java, Summary.java, Utilisation.java | Line: various
Description: Parameters `mode`, `start_time`, `end_time`, `cust_cd`, `loc_cd`, `dept_cd` never null-checked -- NPEs on `.equals()` calls and null date dereferences when date parsing fails.
Fix: Validate all required parameters for null/empty; return 400 error response for missing parameters.

[A08-05] HIGH | File: TableServlet.java | Line: 36-40
Description: `rsList` is instance field on shared servlet instance -- concurrent requests read/write same list (`rsList.clear()` at lines 131, 231, 397, 548) causing race conditions, data corruption, cross-user data leakage.
Fix: Refactor `rsList` to session-keyed ConcurrentHashMap pattern consistent with other servlets or use local variables.

[A08-06] HIGH | File: Utilisation.java | Line: 49-52
Description: Instance fields `vehicles`, `thresholdLow`, `thresholdHigh`, `oneDay` are shared mutable state on single servlet instance -- concurrent requests corrupt each other's state.
Fix: Convert instance fields to local variables passed between methods or session-keyed maps.

[A08-07] MEDIUM | File: SessionCleanupListener.java | Line: 21-29
Description: Only `Impacts.cleanupSession()` called on session destruction -- `CriticalBattery`, `Preop`, `Utilisation`, and `Licence` all have session data in static ConcurrentHashMaps never cleaned up, causing memory leaks.
Fix: Add calls to `CriticalBattery.cleanupSession()`, `Preop.cleanupSession()`, `Utilisation.cleanupSession()`, `Licence.cleanupSession()` in `sessionDestroyed()`.

[A08-08] HIGH | File: Config.java | Line: 29
Description: `cusList` is static field written by `getCustomers()` and read by `getSites()`/`getDepartments()` -- when one user calls `getCustomers()` it overwrites list, causing cross-user data leakage; not synchronized or thread-safe.
Fix: Replace static shared list with per-request or per-session data.

[A08-09] HIGH | File: All 9 dashboard files
Description: No input validation (length checks, type checks, allowlist matching) on any request parameter -- `substring()` throws SIOOBE for short strings, `Integer.parseInt()` throws NFE for non-numeric, `SimpleDateFormat` failures leave null dates.
Fix: Add input validation for all parameters including type checking, length validation, allowlist matching with appropriate error responses.

[A08-10] MEDIUM | File: All 9 dashboard files
Description: Every catch block prints exceptions to stdout/stderr but never writes error response -- client receives empty 200 OK or unhandled 500 with no meaningful error message.
Fix: Set appropriate HTTP error status codes (400, 500); return structured error responses in catch blocks.

[A08-11] HIGH | File: Licence.java | Line: 175-238
Description: `category` from `req.getParameter("category")` can be null (ternary preserves null) causing NPE on `.equals()`; `entry.get("status").replace(...)` NPEs if status DB field is null.
Fix: Add null checks for `category` before `.equals()` and for map values before string methods.

[A08-12] MEDIUM | File: CriticalBattery.java, Preop.java, Impacts.java | Line: various
Description: `entry1.get("id")`, `entry1.get("series")`, `entry1.get("shock_id")`, `entry1.get("level")` called without null checks -- null DB values cause NPE on `.equals()`.
Fix: Add null checks on map values or use `Objects.equals()` for null-safe comparison.

[A08-13] MEDIUM | File: Impacts.java | Line: 358-389
Description: `getAverage()` references map keys `"cd"` and `"percentage"` that do not exist in Impacts query result set -- dead/broken code copied from another servlet.
Fix: Correct key names to match actual SQL columns or remove dead code.

[A08-14] MEDIUM | File: Config.java | Line: 42
Description: `cust == LindeConfig.customerLinde` uses reference equality (`==`) instead of `.equals()` for string comparison -- condition almost never true since `cust` from `req.getParameter()` is a new String.
Fix: Replace `==` with `.equals()`.

[A08-15] HIGH | File: All servlet classes
Description: No servlet checks whether user is authenticated -- `Config.getCustomers()` reads session attribute but does not gate access; `Config.getPermision()` queries permissions but only returns them without enforcing.
Fix: Add authentication and authorization checks at beginning of each `doGet()` or implement servlet filter enforcing authentication.

[A08-16] MEDIUM | File: Licence.java | Line: 47-54
Description: `init()` loads all customers from DB into instance-level `cusList` at startup -- data never refreshed (stale after changes), shared across all users without filtering.
Fix: Remove stale shared list; load customer data per-request or per-session.

[A08-17] CRITICAL | File: TableServlet.java | Line: 103-111, 200-212, 303-309, 469-472
Description: `search_crit` parameter injected directly into SQL LIKE clauses without sanitization -- `%'); DROP TABLE --` breaks out of LIKE and injects arbitrary SQL.
Fix: Use PreparedStatement with parameterized LIKE queries.

[A08-18] LOW | File: All 8 dashboard files
Description: All DB operations use manual try/finally instead of try-with-resources -- `rs` reassigned multiple times inside try block means only last reference closed in finally, risking resource leaks.
Fix: Refactor to try-with-resources for all JDBC Connection, Statement, ResultSet.

### chart

[A05-001] HIGH | File: All 12 chart files
Description: Chart package has 12 Java files with ~70+ public methods, zero tests, and no test framework -- every code path entirely untested.
Fix: Introduce JUnit 4/5; prioritize testing `Chart.caculateyAxis()`, `StackedBarChart.createDataset()`, `StackedBarChart.saveChart()`.

[A05-002] HIGH | File: Chart.java | Line: 15
Description: `caculateyAxis(double yAxis)` is central axis-scaling algorithm inherited by 10 classes with 5 branches -- untested exactly-10 boundary falls through all conditions returning unscaled.
Fix: Create parameterized tests covering: 0.0, 0.5, 5.0, 10.0 (boundary), 10.1, 50.0, 100.0, 100.1, 999.0, and negative values.

[A05-003] MEDIUM | File: BarChartCategory.java, BarChartR.java, BarChartImpactCategory.java | Line: 68, 59, 80-82
Description: Multiple `createChart()` methods access `this.colors.get(i)` and `this.yAxisLabel.get(i)` without bounds checking -- parent provides only 13 colors so >13 data series causes IOOBE.
Fix: Write tests verifying 1-13 data series, 0 data series, and >13 data series handling.

[A05-004] MEDIUM | File: BarChartNational.java, BarChartUtil_bak.java | Line: 91-92, 80-81
Description: Both compute `500/unit.length` and `470/unit.length` -- empty `data` list means `unit.length` is 0 causing ArithmeticException (division by zero).
Fix: Write tests with empty list input; add guard clause for empty data.

[A05-005] HIGH | File: StackedBarChart.java | Line: 218-258
Description: `createDataset()` parses comma-separated strings accessing array indices 0, 1, 2, 5, 6+ without validation -- malformed input causes AIOOBE, NFE, or silent data corruption.
Fix: Write tests for well-formed CSV, fewer than 7 fields, non-numeric values, empty string, null elements.

[A05-006] MEDIUM | File: StackedBarChart.java | Line: 286-300
Description: `saveChart()` writes PNG swallowing IOException -- returns intended file path as though succeeded even when write fails.
Fix: Write tests for file creation, invalid/nonexistent `chartDir`, read-only path, return value on IOException.

[A05-007] MEDIUM | File: StackedBarChart.java | Line: 268
Description: `createDataset2()` mutates instance field `totalUnits` via `totalUnits = totalUnits/5` -- called multiple times produces repeatedly divided incorrect values.
Fix: Write test calling `saveChart()` twice verifying `totalUnits` consistency; use local variable instead.

[A05-008] MEDIUM | File: PieChartR.java | Line: 19-26, 48-65
Description: Constructor hardcodes 3 labels and 3 colors but `createChart()` iterates `data.size()` -- fewer or more than 3 elements causes missed slices or IOOBE.
Fix: Write tests with 0, 1, 3 (happy path), and 5 elements.

[A05-009] LOW | File: LineChartR.java | Line: 14
Description: Constructor accepts `yAxis` parameter but immediately calls `this.setyAxis()` which recalculates from data, discarding caller-provided value.
Fix: Write test verifying whether provided or calculated value takes effect; remove parameter if intentionally ignored.

[A05-010] LOW | File: BarChartUtil_bak.java
Description: `_bak` suffix indicates backup copy; functionally identical to `BarChartNational` with minor differences -- likely unused dead code.
Fix: Search for references; if unreferenced remove it.

[A05-011] LOW | File: JfreeGroupStackChart.java
Description: Contains entirely hardcoded demo data with no parameterization; constructor creates chart and discards it -- appears to be sample/demo code never adapted for production.
Fix: If unused remove; if used refactor to accept dynamic data.

[A05-012] MEDIUM | File: StackedBarChart.java | Line: 179, 253, 295
Description: Three locations use `catch (Exception e) { e.printStackTrace(); }` swallowing all exceptions -- impossible to verify error conditions handled correctly.
Fix: Write tests triggering each exception path; verify exception logged properly and application state remains consistent.

[A05-013] MEDIUM | File: BarChartNational.java | Line: 68-73
Description: Name truncation checks `if(name.length() > RuntimeConf.maxUnitName)` then hardcodes `substring(0,18)` -- throws SIOOBE if name passes condition but shorter than 18 characters.
Fix: Write parameterized tests with names of varying lengths (0, 1, 17, 18, 19, 50); verify correct truncation.

### chart-excel

[A06-01] CRITICAL | File: ChartsExcelDao.java | Line: 58-95, 133-169, 207-327, 329-1838
Description: Every database method uses raw string concatenation to build SQL with user-supplied parameters (cust_cd, loc_cd, dept_cd, st_dt, end_dt) -- SQL injection in all 12+ public query methods with zero test coverage.
Fix: Convert all SQL to PreparedStatement with parameterized queries; add tests with mock DB connections and SQL injection payloads.

[A06-02] CRITICAL | File: ChartsExcelDao.java | Line: various (16 catch blocks)
Description: Every catch block calls `e.getMessage()` as no-op (result discarded), prints to stdout/stderr but never re-throws or logs properly -- methods return partial/empty results without failure indication.
Fix: Re-throw exceptions or return proper error indicators; add tests for exception propagation, empty ResultSets, and resource cleanup.

[A06-03] CRITICAL | File: ChartDashboardUtil.java | Line: 70-686, 695-1030
Description: `createTestChart()` (616 lines, 9-case switch) and `createBarChart()` (335 lines) interact with DB, generate Excel via Apache POI, build chart URLs via charts4j, and perform file I/O -- all with zero coverage.
Fix: Add tests for each of 9 switch cases, varying departments/locations/data sizes, empty department lists, null data.

[A06-04] HIGH | File: ChartsExcelDao.java | Line: 164-166
Description: Condition `locCd.trim().length() < 0` always false (length never negative) -- dead code; trailing comma from while loop never stripped so `getAllLocations()` always returns string with trailing comma.
Fix: Change condition to `locCd.trim().length() > 0`; add tests for single location, multiple locations, empty result sets.

[A06-05] HIGH | File: BatteryChargeChart.java, DriverAccessAbuseChart.java, UserLoginChart.java | Line: 27, 75-79
Description: `chldLetters` array has exactly 26 entries (A-Z) -- if `axisLabels.size()` exceeds 26, AIOOBE thrown accessing `chldLetters[i]` in createChart loop.
Fix: Add bounds check or cap loop at `Math.min(axisLabels.size(), chldLetters.length)`; test with 0, 1, 26, and 27+ labels.

[A06-06] HIGH | File: ChartDashboardUtil.java | Line: 1036-1476
Description: All chart-generation methods iterate input bean lists without null checks; department name filtering calls `equalsIgnoreCase` on potentially null `getDept_name()` return -- NullPointerExceptions.
Fix: Add null checks for input lists and bean field values; test with null/empty lists and beans with null department names.

[A06-07] HIGH | File: ChartsExcelDao.java | Line: 404-550, 552-691, 693-847
Description: `getUnitUtilisationByHour` methods execute queries in deeply nested loops (days x hours x vehicles) using single Statement -- each `executeQuery()` implicitly closes previous ResultSet; large `days_btn` values create extreme DB load.
Fix: Refactor to batch queries; add performance tests with varying `days_btn` values; test resource cleanup on exception.

[A06-08] HIGH | File: ChartsExcelDao.java | Line: 1046-1106, 1128-1183, 1185-1255
Description: `getAccessAbuse()` contains time-overlap detection using private helpers `sub_tm()`, `clash()`, `to_sec()`, `convert_time()` performing manual time parsing and complex nested conditionals -- all purely computational with zero coverage.
Fix: Extract time-calculation helpers into testable utility; add tests for `sub_tm()` midnight boundary, `clash()` overlapping/non-overlapping, `to_sec()` various formats, `convert_time()` zero/negative values.

[A06-09] MEDIUM | File: All 8 chart classes
Description: All 8 chart classes follow identical pattern building Google Charts URLs via charts4j with inherited `caculateyAxis()` (typo "caculate") -- no URL generation or axis calculation tested.
Fix: Add tests verifying chart URLs well-formed, y-axis calculation with various ranges (0, single value, large), behavior when `maxArrayValue()` returns 0.

[A06-10] MEDIUM | File: PreopFailChart.java | Line: 78
Description: Chart legend label is "Unlocks" but chart represents "Incorrect Pre-op Checks" -- copy-paste error from MachineUnlockChart.
Fix: Change legend from "Unlocks" to "Incorrect" or "Pre-op Failures"; add test verifying legend matches report.

[A06-11] MEDIUM | File: ChartDashboard.java | Line: 1-9
Description: Class contains only empty default constructor with no fields or methods -- unused dead code or unimplemented placeholder.
Fix: Verify if referenced; if not, remove as dead code.

[A06-12] MEDIUM | File: All 10 bean classes
Description: None implement `equals()`/`hashCode()`/`toString()`; none validate setter inputs for null; UnitUtilBean.`getUtilNo()` returns mutable `double[]` reference without defensive copy.
Fix: Add equals/hashCode/toString, null validation, defensive array copying; add tests for round-trips and null handling.

[A06-13] MEDIUM | File: ChartsExcelDao.java | Line: 351-362, 366-378
Description: Impact categorization depends on `RuntimeConf.Blue_LEVEL`, `RED_LEVEL`, `AMBER_LEVEL` for business-critical severity classification -- no tests at boundary values.
Fix: Add tests with shock values at exactly each threshold, just below and above; verify correct categorization counts.

[A06-14] LOW | File: ChartDashboardUtil.java | Line: 1049, 1074
Description: No-department overload creates 2-element array {amber, red} matching ImpactChart's 2 axis labels; department-filtered overload creates 3-element array {blue, amber, red} -- may produce misaligned chart.
Fix: Align both overloads to same array structure; add tests comparing output of both overloads.

[A06-15] LOW | File: ChartDashboardUtil.java | Line: 1214
Description: Access abuse count multiplied by 2 (`bean.get(i).getCount() * 2`) without documentation -- unclear if intentional business logic (counting both sides of clash) or bug.
Fix: Document business reason or remove if bug; add tests verifying multiplied value against expected output.

### excel-frm

[A09-001] CRITICAL | File: All 10 excel-frm files
Description: Zero test coverage across all 10 files (7,342 total LOC) -- no unit tests, integration tests, or automated verification for ~55+ methods containing report generation, data aggregation, and formatting calculations.
Fix: Add test infrastructure; prioritize tests for `Frm_excel.getParam()`, `setParameters()`, `setTotalDuration()`, `Frm_Linde_Reports.createExcel(opCode)`.

[A09-002] HIGH | File: All 10 files | Line: various
Description: Every `createExcel()` method uses `FileOutputStream` without try-with-resources or try/finally -- if `wb.write(fileOut)` throws, `fileOut.close()` never called, leaking file handle.
Fix: Wrap `FileOutputStream` in try-with-resources.

[A09-003] HIGH | File: Frm_excel.java | Line: 406-409, 439-444, 474-479, 511-516, 548-569, 599-603, 948-953, 986-991
Description: Multiple `addImage*` methods open `FileInputStream` or `URL.openStream()` without try-with-resources -- if `IOUtils.toByteArray(is)` throws, stream never closed.
Fix: Wrap all InputStream usages in try-with-resources.

[A09-004] HIGH | File: Frm_MaxHourUsage.java, Frm_quater_rpt.java, Frm_excel.java | Line: various
Description: Multiple catch blocks catch Exception broadly and only call `e.printStackTrace()` -- reports generated with missing content and no failure indication.
Fix: Replace `printStackTrace()` with proper logging; propagate exception or set flag indicating partial generation.

[A09-005] HIGH | File: All 10 files
Description: No input validation on constructor parameters or method arguments -- `cust_cd`, `loc_cd`, `docRoot`, `opCode`, date strings used directly in DAO queries, file paths, `Integer.parseInt()`, `String.split()` without null/format checks.
Fix: Add null checks, empty-string validation, format validation for all parameters before path construction, parsing, DAO calls.

[A09-006] HIGH | File: Frm_Linde_Reports.java | Line: 296-299, 323-326, 354-357
Description: Date strings parsed by naive `split("/")` without format validation -- null, empty, or unexpected format (ISO `yyyy-MM-dd`) throws AIOOBE or NFE.
Fix: Validate date format before parsing or use `SimpleDateFormat`/`DateTimeFormatter`.

[A09-007] HIGH | File: Frm_Linde_Reports.java | Line: 1127-1132, 1278-1284, 1502-1505, 1633-1638
Description: Multiple methods parse comma-delimited strings by splitting on commas and indexing into array without length checks -- AIOOBE if data has missing fields.
Fix: Add array length validation after `split(",")` before accessing indexed elements.

[A09-008] MEDIUM | File: Frm_Linde_Reports.java | Line: 1372, 1923, 411
Description: Three locations risk division by zero: `aveTot/countTot`, `duration/gTotal`, `totalHours/workDay` when divisors are 0.
Fix: Add zero-value guards before each division; handle zero case with default value or skip calculation.

[A09-009] MEDIUM | File: Frm_excel.java, Frm_nz_unitSummary_rpt.java, Frm_quater_rpt.java | Line: various
Description: File paths constructed using `getProtectionDomain().getCodeSource().getLocation()` with hardcoded relative traversals (e.g., `"/../../"` vs `"/../../../../../../../../"`) differing by site and duplicated across subclasses.
Fix: Centralize path construction in base class using configurable root directory; remove duplicated path logic.

[A09-010] MEDIUM | File: All 10 files | Line: Frm_excel.java:63
Description: `XSSFWorkbook` created at field initialization but never closed -- holds XML DOM in memory; can lead to memory exhaustion in server environment generating many reports.
Fix: Add `close()` or `dispose()` method to `Frm_excel` that closes workbook; call in finally block after report generation.

[A09-011] MEDIUM | File: Frm_Linde_Reports.java | Line: 50-288
Description: `createExcel(String opCode)` is 238-line method with 18 if/else-if branches dispatching on opCode -- silently produces empty report for unrecognized opCodes with no error.
Fix: Refactor using strategy pattern or map-based dispatch; add default/else throwing exception for unknown opCodes.

[A09-012] MEDIUM | File: All 10 files
Description: DAO objects instantiated inline with `new` -- unit testing impossible without live database since no dependency injection or factory pattern.
Fix: Refactor to accept DAO instances via constructor/setter injection for mock substitution during testing.

[A09-013] LOW | File: Frm_MaxHourUsage.java, Frm_quater_rpt.java, Frm_excel.java | Line: various
Description: Several constructors and fields use raw `ArrayList` without generic type parameters -- bypasses type safety risking ClassCastException.
Fix: Add proper generic type parameters to all ArrayList declarations.

[A09-014] LOW | File: Frm_excel.java | Line: 1096-1098, 209-211, 213-215, 309-343, 304-307, 239-241
Description: Multiple dead or placeholder methods: `getCust_prefix()` has empty body, `init()`/`init2()` empty and never overridden, `createReport()` has hardcoded 2011 test data, `setFoot()` commented "doesn't work", `getBody()` always returns empty string.
Fix: Remove dead code or implement properly; document intentionally empty template methods.

[A09-015] MEDIUM | File: Frm_Linde_Reports.java | Line: 2335
Description: `generateChart(String rpt_name)` uses `ProcessBuilder`/`Runtime.exec()` for chart generation with no timeout, `System.out.println` for logging, no proper stderr handling -- process could hang or silently fail.
Fix: Add timeout to process execution; capture and log both stdout and stderr; throw on failure.

### misc-small-packages

[A04-01] CRITICAL | File: All 8 misc-small-packages files
Description: None of the 8 files have any test classes -- zero unit/integration tests and zero coverage tooling in entire repository; every public method completely unverified.
Fix: Establish test infrastructure (JUnit 5 + Mockito); prioritize SQL-injection-vulnerable classes.

[A04-02] CRITICAL | File: BusinessInsightBean.java | Line: 180-1481
Description: 12 public fetch methods each build multiple raw SQL queries with string concatenation, manipulate shared mutable state, and contain error-prone arithmetic including potential division-by-zero in `ratio` when `min == 0`.
Fix: Create tests for `convert_time` boundaries, `ratio` with min=0, and mock-based tests for each fetch method verifying data assembly.

[A04-03] CRITICAL | File: BusinessInsightBean.java | Line: 209, 253-255, 332, 467-469, 594-596, 646-648, 713-714, 787-788, 893-895, 1030-1032, 1131-1133, 1259-1261
Description: All 12 fetch methods concatenate user-supplied parameters (`customerCd`, `locationCd`, `st_dt`, `end_dt`) directly into SQL without PreparedStatement -- parameters originate from `request.getParameter()`.
Fix: Tests should verify SQL injection payloads in all parameters are rejected or safely handled; migrate to PreparedStatement.

[A04-04] HIGH | File: BusinessInsight.java | Line: 41, 54-68, 97-101, 105
Description: `doPost` has untested validation branches for empty dates/customer/location/email plus exception handling silently swallowing errors; `getExportDir()` uses fragile path manipulation with hardcoded relative traversal; typo "wong" instead of "wrong".
Fix: Create servlet test with mocked request/response verifying each validation branch; test `getExportDir()` path construction.

[A04-05] HIGH | File: BusinessInsightExcel.java | Line: 28, 147, 151, 240, 330, 470, 581
Description: `createExcel` dispatches to 10 methods via if-else on `opCode`; each parses delimited strings with `parseInt`/`parseDouble` without null/format checks; division-by-zero at line 151 occurs before guard check; integer arithmetic precision loss at lines 470, 581.
Fix: Write tests with mocked bean verifying opCode dispatch, empty data arrays, malformed strings, zero-value edge cases.

[A04-06] CRITICAL | File: FmsChklistLangSettingRepo.java | Line: 26-62
Description: All three public methods build SQL via string concatenation with unsanitized parameters; `updateLanguageBy` has string manipulation bug risk where `langChoiceAsList.toString().replace(...)` could corrupt data.
Fix: Create tests with mocked Statement for null/empty/valid results, empty list default, special characters, SQL injection payloads.

[A04-07] HIGH | File: FmsChklistLangSettingRepo.java | Line: 36
Description: `queryLangConfigBy` returns `Arrays.asList(rset.getString(1).split(","))` -- fixed-size list throws UnsupportedOperationException if callers modify; empty string DB value causes `split(",")` to return `[""]` not empty list.
Fix: Test callers handle fixed-size list; test empty string, null, single value, comma-delimited values.

[A04-08] CRITICAL | File: HireDehireService.java | Line: 18-122
Description: `getUnitsHireDehireTime` builds complex UNION ALL SQL with string concatenation (no PreparedStatement), early returns for null/empty/All custCd, silently swallows all exceptions, and search regex filter silently ignores pure letter-based searches.
Fix: Create tests with mocked Statement for null/empty/All custCd, filter combinations, letters-only searchCrit being dropped, SQL injection, ResultSet-to-DehireBean mapping.

[A04-09] HIGH | File: HireDehireService.java | Line: 54-70
Description: When `searchCrit` contains only alphabetic characters, code appends `" and "` to SQL but skips adding filter condition -- produces malformed SQL ending in `and ` with no subsequent condition, causing silently-caught SQLException.
Fix: Test with `searchCrit = "ABC"` to reveal SQL syntax error; fix logic to either support letter searches or avoid appending `and`.

[A04-10] MEDIUM | File: PreOpQuestions.java, Question.java | Line: 5-11, 7-9
Description: Neither implements `equals()`/`hashCode()` preventing reliable collection use; `Question.critical` typed as String rather than boolean/enum; no default constructor may cause JSON deserialization issues.
Fix: Write POJO tests for constructor, round-trips, toString, null handling, and JSON serialization/deserialization.

[A04-11] LOW | File: SupervisorUnlockBean.java | Line: 9, 47-51
Description: `getGrandTotal()` computes `impactCount + surveyCount + criticalCount` but declared `int grandTotal` field never assigned and shadows computed method; `toString()` omits total.
Fix: Write test verifying `getGrandTotal()` with known inputs including zero values and overflow.

[A04-12] MEDIUM | File: BusinessInsight.java | Line: 105-113, 118-126, 99
Description: `linderReportMailer` hardcodes sender email as `"fleetfocus@lindemh.com.au"` and passes `"unknown"` for CC; `getExportDir()` uses fragile seven-level parent directory traversal; typo "wong" at line 99.
Fix: Test `getExportDir()` returns valid path; test `linderReportMailer()` with mocked mail utility; fix "wong" typo.

[A04-13] HIGH | File: BusinessInsightExcel.java | Line: 151, 240, 330, 470, 581
Description: Multiple report methods compute `impXHour = duration / impact` before guard check `if (impact == 0)` -- produces Infinity/NaN for doubles or ArithmeticException for integers; integer division-by-zero risk at lines 470, 581.
Fix: Tests should supply data with zero values for impact/duration/qCount/count to verify no runtime exceptions; move guard before division.

[A04-14] MEDIUM | File: BusinessInsightBean.java | Line: 93-96, 290-295, 553-558, 606-611, 673-678, 746-751, 843-847, 979-984, 1079-1084, 1208-1213, 1319-1324
Description: Every fetch method catches Exception broadly with only `e.printStackTrace()` and discarded `e.getMessage()`; `init()` prints raw query to stdout on failure, leaking sensitive SQL.
Fix: Tests should verify dataArray in consistent state after DB failure; verify partial failures mid-loop don't leave corrupted data.

### excel-reports-A-I

[A11-01] CRITICAL | File: All 18 excel report files (A-I range)
Description: Zero automated tests for any of the 18 Excel report generation classes -- no unit tests, integration tests, or test framework in the repository.
Fix: Add unit tests for each `createExcel()` verifying output file creation, column layout, conditional logic paths, boundary tests for empty/null inputs.

[A11-02] HIGH | File: All 18 files
Description: Every `createExcel()` creates FileOutputStream without try-with-resources or try/finally -- if `wb.write(fileOut)` throws, stream leaks file handle.
Fix: Wrap FileOutputStream in try-with-resources in all 18 files.

[A11-03] HIGH | File: ExcelCimplicityUtilReport.java, ExcelDailyVehSummaryReport.java, ExcelDriverAccessAbuseReport.java, ExcelDriverImpactReport.java, ExcelDynDriverReport.java, ExcelDynTransportDriverReport.java, ExcelDynUnitReport.java, ExcelExceptionSessionReport.java | Line: various
Description: Multiple files call `setCellFormula("VALUE(\""+variable+"\")")` where variable from bean/DB/user input risks malformed formulas or Excel formula injection with special characters.
Fix: Sanitize values before embedding in formulas; escape double-quote characters and formula-triggering prefixes; or use `setCellValue` instead.

[A11-04] MEDIUM | File: 10 excel report files | Line: various
Description: `new UnitDAO()` instantiated inside report methods but never referenced in 10+ files -- wastes allocation and potentially triggers unnecessary DB connection (copy-paste artifact).
Fix: Remove unused `UnitDAO` instantiation from all affected files.

[A11-05] MEDIUM | File: ExcelDriverImpactReport.java, ExcelDriverLicenceExpiry.java | Line: various
Description: Files create `CustomerDAO` and call DB methods during Excel generation -- mixes data retrieval with presentation making code untestable without live database.
Fix: Move DB lookups into bean/service layer before report generation.

[A11-06] MEDIUM | File: ExcelBroadcastMsgReport.java, ExcelDynDriverReport.java, ExcelDynSeenReport.java, ExcelDynTransportDriverReport.java | Line: various
Description: Method names don't match report produced (e.g., `createUnitUnlockReport` in BroadcastMsgReport) -- copy-paste artifacts.
Fix: Rename methods to match actual report type.

[A11-07] HIGH | File: All 18 files
Description: No null checks on constructor parameters, bean getter return values, or ArrayList elements before casting -- `dep.equalsIgnoreCase("all")` throws NPE if `dep` is null.
Fix: Add null-guard checks on constructor parameters and bean data; use `"all".equalsIgnoreCase(dep)` pattern.

[A11-08] MEDIUM | File: All 18 files
Description: Nearly every file uses unparameterized `ArrayList` with unchecked casts like `(String)vunit_name.get(i)` -- runtime ClassCastException risk; Dyn* reports use 3+ levels of nested raw ArrayList.
Fix: Add generic type parameters to all ArrayList declarations; eliminate unchecked casts.

[A11-09] MEDIUM | File: ExcelImpactMeterReport.java, ExcelImpactReport.java | Line: 176, 191
Description: Both hardcode production URL `http://fleetfocus.lindemh.com.au/fms/` (HTTP not HTTPS) -- non-portable and unencrypted.
Fix: Move base URL to externalized config; use HTTPS.

[A11-10] HIGH | File: ExcelExceptionSessionReport.java, ExcelImpactReport.java | Line: 137-139, 233-236
Description: ExcelExceptionSessionReport silently ignores URL decoding failures; ExcelImpactReport catches JSONException with only `e.printStackTrace()` -- RTLS location/speed data silently disappears.
Fix: Log meaningful errors; propagate exceptions or provide safe fallback values making data gap visible.

[A11-11] HIGH | File: ExcelExceptionSessionReport.java | Line: 300-312
Description: When `vdriv_cd.size() == 0`, line 311 writes `veh_id` into "Operational Mode" column instead of correct value -- duplicate vehicle ID in wrong cell.
Fix: Write correct operational mode value or empty string at line 311 instead of `veh_id`.

[A11-12] LOW | File: ExcelImpactReport.java | Line: 221
Description: GeoJSON location string uses misspelling "longtitue" instead of "longitude" -- appears in Excel output visible to users.
Fix: Change `"longtitue"` to `"longitude"`.

[A11-13] LOW | File: ExcelDriverImpactReport.java, ExcelDriverLicenceExpiry.java, ExcelHireDehireReport.java + 12 others
Description: `createExcel()` has 4 different signatures across 18 files (5-param, 6-param, 3-param variants) preventing common interface or polymorphic usage.
Fix: Define common interface or abstract method using parameter object or builder pattern.

[A11-14] MEDIUM | File: ExcelImpactReport.java | Line: 32, 77
Description: Instance field `vimp_rtlsjson` shadowed by local variable with same name at line 77 -- instance field remains null; maintenance trap.
Fix: Remove instance field or rename local variable.

[A11-15] LOW | File: 11 of 18 files
Description: 11 files contain `import java.util.ArrayList` twice -- copy-paste development without IDE cleanup.
Fix: Remove duplicate import statements.

### excel-reports-K-Z-mail

[A12-01] CRITICAL | File: All 16 excel report and mail files
Description: None of the 16 audited files have any unit tests, integration tests, or automated coverage -- no test framework configured, no test source directories, no test build configuration.
Fix: Introduce test framework (JUnit/TestNG); create test source directories; add unit/integration tests for all 16 classes.

[A12-02] HIGH | File: All 14 Excel report files | Line: various
Description: All `createExcel()` methods open FileOutputStream without try-with-resources or finally -- if `wb.write(fileOut)` throws, stream leaks file handle.
Fix: Wrap FileOutputStream in try-with-resources in all 13 Excel report classes.

[A12-03] HIGH | File: ExcelUtilisationReport.java | Line: 163
Description: Line 163 sets "Traction Hours" cell using `utilBean.getKey_hours()` instead of `utilBean.getTrack_hours()` -- traction hours column displays key hours data.
Fix: Change to `utilBean.getTrack_hours()`.

[A12-04] MEDIUM | File: 9 report files | Line: various
Description: UnitDAO instantiated but never referenced in at least 9 classes -- wasted resources if DAO constructor opens DB connection.
Fix: Remove unused UnitDAO instantiations.

[A12-05] MEDIUM | File: ExcelRestrictedUsageReport.java, ExcelSuperMasterAuthReport.java | Line: 59/65-67
Description: Both instantiate CustomerDAO and call getCustomerName/getLocationName/getDepartmentName during report rendering -- mixes data retrieval with presentation.
Fix: Move data retrieval out; pass resolved names as constructor/method parameters.

[A12-06] MEDIUM | File: ExcelUtilWOWReport.java, ExcelUtilWOWReportEmail.java | Line: 1-173, 1-180
Description: ExcelUtilWOWReportEmail is near line-for-line identical to ExcelUtilWOWReport (~150 lines duplicated) differing only by LindeConfig.siteName check.
Fix: Extract shared rendering logic into common base class or method.

[A12-07] MEDIUM | File: ExcelKeyHourUtilReport.java, ExcelSeatHourUtilReport.java | Line: 1-357
Description: Two 357-line classes are structurally identical, differing only in bean type (KeyHourUtilBean vs SeatHourUtilBean) and report title.
Fix: Refactor into single generic/parameterized class or common base class.

[A12-08] MEDIUM | File: ExcelPreOpCheckFailReport.java | Line: 64-221, 223-378
Description: Two overloaded `createPreOpFailReport` methods contain ~150 lines of near-identical logic; `form` parameter in second overload has no visible effect -- dead code or incomplete feature.
Fix: Consolidate into one method; determine if `form` parameter serves purpose.

[A12-09] HIGH | File: MailBase.java | Line: 5-127
Description: Both `setMailHeader` overloads build HTML via string concatenation directly interpolating parameters into HTML without encoding -- XSS if parameters contain user-controlled data.
Fix: Apply HTML encoding to all interpolated parameters before embedding in HTML string.

[A12-10] MEDIUM | File: MailBase.java | Line: 10, 15-16, 24, 69, 74-75, 83
Description: Image and CSS references use hardcoded `http://fleetfocus.lindemh.com.au/fms/` URLs (HTTP not HTTPS) -- non-portable and unencrypted.
Fix: Replace with HTTPS; externalize base URL to configuration property.

[A12-11] MEDIUM | File: MailExcelReports.java | Line: 20-26, 36-41
Description: Both `sendExcelReport` methods catch AddressException/MessagingException with only `e.printStackTrace()` and TODO comment -- returns false with no diagnostics, no structured logging, no re-throw.
Fix: Replace `printStackTrace()` with structured logging; consider propagating or wrapping exception.

[A12-12] LOW | File: 10 report files
Description: Extensive use of raw ArrayList without type parameters followed by unchecked casts -- runtime ClassCastException risk.
Fix: Add generic type parameters; remove unchecked casts.

[A12-13] MEDIUM | File: ExcelServMaintenanceReport.java | Line: 153
Description: `Double.parseDouble(nsDue)` called without try-catch -- non-numeric values (e.g., "-" or empty) cause unhandled NumberFormatException failing entire report.
Fix: Wrap in try-catch with safe default value (0.0) or skip row on parse failure.

[A12-14] LOW | File: MailExcelReports.java | Line: 19, 35
Description: `mail.sendMail()` passes literal string "unknown" as sender name and CC address -- semantically unclear; may cause delivery issues.
Fix: Replace with meaningful configured value; source sender name from configuration.

[A12-15] LOW | File: MailExcelReports.java | Line: 14, 27
Description: `System.out.println` used to log email send times with email addresses in clear text instead of structured logging.
Fix: Replace with structured logging framework; redact/mask email addresses.

[A12-16] LOW | File: ExcelUtilWOWReport.java, ExcelUtilWOWReportEmail.java, ExcelUtilisationReport.java, multiple files
Description: Significant unused variables (up to 12 in ExcelUtilisationReport) and duplicate imports -- incomplete refactoring.
Fix: Remove all unused declarations and duplicate imports.

### excel-reports-beans-A-D

[A13-01] HIGH | File: All 15 bean files (A-D range)
Description: Zero test coverage across all 15 bean classes -- no test framework, no build system, no test directories; all 398 public getter/setter methods completely untested.
Fix: Introduce test framework; create basic getter/setter round-trip, default value verification, and null-handling tests.

[A13-02] MEDIUM | File: All 15 files (every setter method)
Description: No setter performs null validation -- calling with null overwrites safely-initialized defaults (`new ArrayList()`, `""`) with null causing downstream NPEs; applies to ~180 ArrayList setters and 20 String setters.
Fix: Add null-argument tests for every setter; implement null guards.

[A13-03] MEDIUM | File: All files except BaseFilterBean.java, BaseResultBean.java, BaseItemResultBean.java
Description: All ArrayList fields use raw types without generics allowing any object type insertion with no compile-time safety.
Fix: Add type verification tests; parameterize all ArrayList declarations.

[A13-04] LOW | File: CurrDrivReportBean.java, CurrUnitReportBean.java
Description: Two 118-line classes are line-for-line identical duplicates differing only in class name.
Fix: Refactor so one extends the other or both extend common base class.

[A13-05] LOW | File: BaseItemResultBean.java | Line: 3
Description: Completely empty class with zero fields and zero methods -- marker/placeholder type only.
Fix: Add instantiation tests or remove if unnecessary.

[A13-06] LOW | File: 14 of 15 bean files
Description: All fields use package-private (default) visibility instead of private -- any same-package class can bypass setters and directly mutate state.
Fix: Change fields to private; add encapsulation verification tests.

[A13-07] LOW | File: BaseFilterBean.java | Line: 8-9
Description: `startTime` and `endTime` stored as plain Strings with no format validation, date parsing, or timezone handling.
Fix: Add valid date format acceptance tests and invalid format handling tests.

[A13-08] INFO | File: DriverAccessAbuseBean.java | Line: 3-4
Description: `java.util.ArrayList` import appears twice.
Fix: Remove duplicate import.

[A13-09] INFO | File: Multiple bean files
Description: Inconsistent field naming: some uppercase (`Vrpt_veh_typ_cd`), some lowercase (`dsum_veh_cd`), some camelCase (`searchCrit`), varying prefixes (`V`, `a_`, `dir_`, `dsum_`).
Fix: Standardize naming conventions; add reflection-based tests.

[A13-10] LOW | File: All 15 files
Description: None override `equals()`, `hashCode()`, or `toString()` -- equality uses reference identity; collections using these as keys behave incorrectly.
Fix: Implement overrides; add equality/identity tests.

[A13-11] LOW | File: All 15 files
Description: None implement `java.io.Serializable` -- beans in HTTP sessions will fail during session replication.
Fix: Implement Serializable on session-scoped beans; add serialization round-trip tests.

[A13-12] INFO | File: BaseResultBean.java, BaseFilterBean.java, all report beans
Description: None of 12 concrete report beans extend BaseResultBean or BaseFilterBean despite those being intended base classes -- report beans duplicate filter-like fields instead of inheriting.
Fix: Verify inheritance contracts; determine whether report beans should extend base classes.

### excel-reports-beans-H-Z-dao

[A14-01] CRITICAL | File: All 15 files (H-Z range)
Description: Repository contains no test framework dependency, no test source directory, no test runner configuration -- all 15 files have exactly 0% automated test coverage.
Fix: Introduce test framework (JUnit); create test source directory; add test runner configuration.

[A14-02] HIGH | File: CustomerDAO.java | Line: 32, 70, 107, 144, 180-181
Description: All five public methods build SQL via string concatenation with caller-supplied parameters -- SQL injection attacks possible.
Fix: Replace all string-concatenated SQL with PreparedStatement and parameterized queries.

[A14-03] HIGH | File: CustomerDAO.java | Line: 41-44, 78-81, 115-118, 152-155, 190-193
Description: All five methods catch Exception, call `e.printStackTrace()` and discard `e.getMessage()`, return default value -- impossible to distinguish "no data found" from "database error."
Fix: Replace silent exception swallowing with proper error propagation and structured logging.

[A14-04] HIGH | File: CustomerDAO.java | Line: 177
Description: `getFormName()` checks local variable `formName` instead of input parameter `form_cd` for empty/zero/all guards -- calls with "0" or "all" incorrectly execute query; copy-paste bug.
Fix: Change guard condition to check `form_cd` instead of `formName`.

[A14-05] HIGH | File: DriverAccessAbuseDAO.java | Line: 33-63
Description: `getAbuseBean()` delegates to `Databean_report.init()` with no try/catch, no null-validation of 7 string parameters, no error checking; has 13 unused instance-level ArrayList fields (dead code).
Fix: Add null-checks for all parameters; wrap delegation in error handling; remove 13 dead instance fields.

[A14-06] MEDIUM | File: HireDehireReportBean.java | Line: 6-13
Description: All 8 ArrayList fields declared private but never initialized (default null) unlike other beans which use `new ArrayList()` -- any getter before setter throws NPE.
Fix: Initialize all ArrayList fields at declaration.

[A14-07] MEDIUM | File: ImpactReportBean.java | Line: 7-21
Description: Seven ArrayList fields default to null while four initialized to `new ArrayList()`; String `fileName` also null -- inconsistent null/non-null behavior.
Fix: Initialize all ArrayList fields and fileName at declaration.

[A14-08] MEDIUM | File: PreOpCheckReportBean.java, PreOpCheckFailReportBean.java
Description: Two classes are line-for-line identical duplicates with same fields, signatures, implementations -- bug fix in one must be manually replicated.
Fix: Extract shared base class or single parameterized class.

[A14-09] MEDIUM | File: KeyHourUtilBean.java, SeatHourUtilBean.java
Description: Two classes have identical field structures (14 ArrayList + 9 String fields), identical signatures and implementations -- same duplication risk.
Fix: Extract shared base class or single parameterized class.

[A14-10] LOW | File: All 13 bean files
Description: Nearly all ArrayList fields use raw types instead of generics -- runtime ClassCastException risk.
Fix: Add generic type parameters to all ArrayList declarations.

[A14-11] LOW | File: CustomerDAO.java | Line: 28, 66, 103, 140, 174
Description: All five methods use `conn.createStatement` with TYPE_SCROLL_SENSITIVE and CONCUR_READ_ONLY instead of PreparedStatement; scroll capability never used (only `rs.next()`).
Fix: Replace Statement with PreparedStatement; change to TYPE_FORWARD_ONLY.

[A14-12] LOW | File: DriverAccessAbuseDAO.java | Line: 18-31
Description: DAO declares 13 ArrayList instance fields never read or written by any method -- remnants of previous implementation.
Fix: Remove 13 dead instance fields.

[A14-13] LOW | File: OperationalStatusReportResultBean.java | Line: 11
Description: When `itemResultBeanList` is null, each `getItemResultBeanList()` returns new empty ArrayList -- callers adding items lose them since backing field remains null.
Fix: Change null guard to assign new list back to field (lazy initialization).

### excel-reports-email

[A10-001] CRITICAL | File: All 28 Email*Report.java files
Description: Zero test coverage across all 28 email report classes -- no test infrastructure, unit tests, integration tests, or test harness for DB queries, Excel generation, file I/O, HTML email bodies, or business logic.
Fix: Add unit tests for each `create*Report()` with mocked Databeans, Excel output validation, empty/null edge cases, and I/O failure handling.

[A10-002] HIGH | File: All 28 Email*Report.java files
Description: Every `createExcel()` uses FileOutputStream without try-with-resources or try-catch-finally -- if `wb.write()` throws, stream never closed causing resource leak.
Fix: Wrap FileOutputStream in try-with-resources or add finally block.

[A10-003] HIGH | File: All 28 Email*Report.java files
Description: All files use raw-type ArrayList from Databeans with unchecked `(String)` casts -- null elements or type mismatches cause ClassCastException/NPE with no meaningful error.
Fix: Add null checks before casting; use generics; handle exceptions from unexpected types.

[A10-004] HIGH | File: EmailKeyHourUtilReport.java, EmailSeatHourUtilReport.java | Line: 112-114, 104-106
Description: Subtitle labels mapped to wrong values -- Customer shows `locName`, Site shows `deptName`, Dept shows `custName` -- incorrect metadata in exported Excel.
Fix: Correct to `{"Customer", custName}`, `{"Site", locName}`, `{"Dept", deptName}`.

[A10-005] HIGH | File: EmailSeatHourUtilReport.java | Line: 159-196, 291-330
Description: Every time-slot column's `setCellValue()` uses `vutil1.get(i)` instead of corresponding `vutil2` through `vutil8` -- all columns display 12-03 AM value when formulas can't evaluate.
Fix: Change each `setCellValue()` to use matching variable (`vutil2` through `vutil8`).

[A10-006] HIGH | File: EmailDriverAccessAbuseReport.java, EmailServMaintenanceReport.java | Line: 283-346, 347-428
Description: `createBody()` methods build HTML by concatenating user/DB data into HTML tags without escaping -- HTML injection and XSS in email clients.
Fix: HTML-escape all dynamic values with `StringEscapeUtils.escapeHtml4()` or equivalent.

[A10-007] MEDIUM | File: EmailImpactMeterReport.java, EmailImpactReport.java | Line: 204, 197
Description: Both hardcode production domain with HTTP in URL embedded in report output.
Fix: Move base URL to config; use HTTPS.

[A10-008] MEDIUM | File: EmailUnitUnlockReport.java, EmailDynSeenReport.java | Line: 32, 38
Description: Method names don't match class purpose due to copy-paste -- `createBroadcastMsgReport()` in EmailUnitUnlockReport and `createDynUnitReport()` in EmailDynSeenReport.
Fix: Rename to `createUnitUnlockReport()` and `createDynSeenReport()`.

[A10-009] MEDIUM | File: EmailPreOpChkFailReport.java, EmailPreOpChkReport.java | Line: 38, 55
Description: Direct `params[1]` access without length checks -- AIOOBE if params array has fewer than 2 elements.
Fix: Add `params.length > 1` guard before accessing `params[1]`.

[A10-010] MEDIUM | File: EmailServMaintenanceReport.java, EmailServMaintenanceReportNew.java | Line: 250/390, 159
Description: `Double.parseDouble()` on meter readings without try-catch -- non-numeric values like `"-"` or empty strings throw unhandled NFE crashing entire report.
Fix: Wrap in try-catch with fallback default value; validate string is numeric before parsing.

[A10-011] LOW | File: Majority of 28 files
Description: Duplicate `import java.util.ArrayList` in 11+ files; `UnitDAO` instantiated but unused in ~18 files (unnecessary DB overhead); `FormulaEvaluator` unused in 4+ files; multiple unused variables.
Fix: Remove duplicate imports and all unused declarations.

[A10-012] MEDIUM | File: EmailDriverAccessAbuseReport.java | Line: 154
Description: `createEmail()` does not call `init()` or `init2()` before using instance ArrayLists defaulting to null -- NPE if called without prior external initialization.
Fix: Add `init2()` call at start of `createEmail()` or add null-guard initialization.

[A10-013] MEDIUM | File: EmailServMaintenanceReport.java | Line: 103-144
Description: `init2()` does not set `vsNo` field (unlike `init()` at line 93) -- `createExcel()` calling `init2()` encounters NPE when `vsNo.get(i)` accessed.
Fix: Add `vsNo = servBean.getVs_no()` to `init2()`.

[A10-014] MEDIUM | File: EmailDailyVehSummaryReport.java | Line: 294-327
Description: Total row always outputs all columns including leader-specific and cimp-specific columns regardless of `cust_type` -- misaligned columns when data rows were conditionally built.
Fix: Apply same `cust_type` conditional logic to total row generation.

[A10-015] LOW | File: EmailDriverLicenceExpiry.java, EmailRestictedAccessUsageReport.java | Line: 21, 68, 72
Description: User-facing typos: title reads `"Driver LIcence Expiry Report"` (capital I); class name misspells "Restricted" as "Resticted".
Fix: Correct title string; rename class/file from `EmailRestictedAccessUsageReport` to `EmailRestrictedAccessUsageReport`.

[A10-016] LOW | File: EmailUtilisationReport.java, EmailKeyHourUtilReport.java | Line: 59-60, 99-106
Description: Inherited fields `from` and `to` truncated via `substring(0,10)` mutating parent state (affects reuse); throws SIOOBE if string shorter than 10 characters.
Fix: Use local variables for truncated values; add length check before `substring()`.

[A10-017] MEDIUM | File: All 28 Email*Report.java files
Description: Same boilerplate pattern duplicated across all 28 files with no shared template -- cross-cutting fixes impossible to apply in one place.
Fix: Refactor common logic into Template Method pattern in parent `Frm_excel` class.

### pdf-reports

[A16-01] CRITICAL | File: All 13 pdf and reports package files
Description: 39,435 lines of Java code with zero automated tests -- no test framework, no test directory, no test runner, no CI test stage; every code path (PDF generation, SQL queries, data transformations, charts, GeoJSON, date calculations, email) completely untested.
Fix: Establish test infrastructure (JUnit/Mockito, Maven Surefire, CI stage); add unit and integration tests starting with highest-risk areas (SQL injection, date/time logic, init dispatchers).

[A16-02] CRITICAL | File: Databean_cdisp.java, Databean_dyn_reports.java, Databean_report.java, Databean_report1.java, LinderReportDatabean.java, Reports.java | Line: various
Description: Nearly every SQL query built via string concatenation with user-controlled parameters (Reports.java L63 concatenates access_cust without quotes, Databean_dyn_reports L266 concatenates ucd directly, Databean_report1 L154 concatenates set_gp_cd) -- pervasive SQL injection across all databean files.
Fix: Migrate all SQL to PreparedStatement with parameterized queries; add input validation tests and boundary tests for all SQL-executing methods.

[A16-03] HIGH | File: MonthlyPDFRpt.java, ReportPDF.java | Line: various
Description: PDF generation has zero test coverage -- createPdf() pipeline, DAO calls during title page that can leave documents corrupted on SQL failure, exception swallowing in createTable(), fragile 7-level path traversal in getExportDir(), silent missing-image skipping in addImage().
Fix: Add PDF output validation tests, table data correctness tests, missing-image handling, path resolution tests, title page tests with empty/null dates using mock DAOs.

[A16-04] HIGH | File: Databean_report.java, Databean_dyn_reports.java, Databean_cdisp.java, LinderReportDatabean.java | Line: various
Description: Each databean has init() as primary JSP entry point acquiring JNDI connections and dispatching on opcode strings to dozens of methods via large if/else blocks (Databean_report.init() dispatches to 30+ opcodes in 300+ lines) -- no tests for opcode routing or connection cleanup.
Fix: Add opcode dispatch tests, connection lifecycle tests, invalid opcode handling tests using mock DataSource injection.

[A16-05] HIGH | File: All databean files, RTLSHeatMapReport.java, RTLSImpactReport.java
Description: Error handling uses bare `e.printStackTrace()` or `System.out.println()` with no recovery -- MonthlyPDFRpt swallows exceptions during table creation continuing with malformed tables, Databean_report1 prints queries with sensitive data to stdout.
Fix: Add exception path tests verifying resource cleanup and no data leakage; replace `printStackTrace()` with proper logging.

[A16-06] HIGH | File: Databean_report1.java, Databean_dyn_reports.java, Databean_report.java, LinderReportDatabean.java | Line: various
Description: Multiple date/time conversion functions untested -- `convert_time()` uses hand-rolled centisecond-to-HH:MM:SS math, `to_sec()` parses HH:MM:SS via StringTokenizer failing on malformed input, MonthlyPDFRpt accesses Calendar.MONTH as instance field.
Fix: Add boundary tests (0 seconds, max int, negative values), format validation tests, timezone handling tests for all date/time methods.

[A16-07] HIGH | File: RTLSHeatMapReport.java, RTLSImpactReport.java | Line: various
Description: Complex spatial calculations lack any tests -- createJSON() builds GeoJSON with coordinate transformations and standard deviation normalization, caculatespeed() performs speed calculation with micro-second intervals, LonLatConverter called with reversed/negated coordinates.
Fix: Add coordinate transformation tests, speed calculation boundary tests, empty point array handling, GeoJSON schema validation.

[A16-08] MEDIUM | File: UtilBean.java | Line: 44, 52-68
Description: `compareTo()` compares day numbers as strings via `String.valueOf()` (breaks for values >= 10); `setDayNum()` has no explicit "Monday" case falling through to default returning 0 (indistinguishable from invalid input).
Fix: Add compareTo ordering verification for all 7 days, day name mapping tests, unknown day name handling; change compareTo to integer comparison.

[A16-09] MEDIUM | File: All databean files, UtilModelBean.java
Description: Pervasive raw ArrayList without generic type parameters (~100 raw ArrayLists in Databean_dyn_reports, ~150+ in Databean_report, UtilModelBean.java) with runtime String casts risking ClassCastException.
Fix: Add type safety verification; migrate raw ArrayLists to proper generic type parameters.

[A16-10] MEDIUM | File: All databean files, Reports.java, RTLSHeatMapReport.java, RTLSImpactReport.java
Description: Every databean manually manages JDBC resources in finally blocks using multiple Statement instance variables (stmt, stmt1, stmt2, etc.) not thread-safe -- Databean_report creates 5 statements at init, RTLSImpactReport opens/closes separate connections in every private method.
Fix: Add connection leak and concurrent access tests; migrate to try-with-resources or connection pooling.

[A16-11] MEDIUM | File: Databean_reports.java
Description: 127-line class appears dead code -- `clearVectors()` has empty body, only substantial code is commented-out `query()` referencing undeclared fields, no `init()` method.
Fix: Determine if referenced; if unused remove to reduce maintenance burden.

[A16-12] MEDIUM | File: Databean_dyn_reports.java, Databean_report.java, Reports.java | Line: various
Description: Access control via SQL WHERE clauses built from access_level fields -- Reports.java L58 defaults empty string to level 1 and throws NFE on non-numeric; concatenates access_cust into SQL without quoting.
Fix: Add access level boundary tests (0-4, empty, non-numeric), unauthorized access prevention tests, access filter bypass tests; validate all access control inputs.

[A16-13] LOW | File: ReportPDF.java | Line: 166-174
Description: `getExportDir()` uses fragile path resolution stripping "file:/" via substring(6), counting slashes, appending 7 levels of parent traversal -- breaks on different deployments, containers, spaces in paths, Windows vs Linux.
Fix: Add path resolution tests; replace fragile traversal with configurable property or JNDI resource.

[A16-14] LOW | File: LinderReportDatabean.java | Line: 63-201
Description: init() dispatches on opCode to 15+ methods but some opcodes map to same method incorrectly -- "nat2_preop_check_by_driver" (L101) and "nat2_util_driver_all_models" (L103) both call fetchNationalPreopCheckCompleted(), likely copy-paste error.
Fix: Add opcode-to-method mapping tests and regression tests to detect copy-paste errors.

### rtls

[A17-01] CRITICAL | File: GridCluster.java | Line: 31
Description: `density` parameter is String parsed at runtime -- "0" causes division by zero producing Infinity/NaN; null or empty strings cause NFE/NPE; no input validation.
Fix: Validate density before use; reject null, empty, and zero; parse once outside loop; guard against zero with explicit check.

[A17-02] CRITICAL | File: GridCluster.java | Line: 62, 68
Description: When `hashPoints` is empty, `length == 0` causes division by zero at line 62; single entry means `length - 1 == 0` causes division by zero at line 68; both produce NaN propagating into returned threshold string.
Fix: Guard against empty and single-entry maps; return early or require minimum two entries before computing standard deviation.

[A17-03] HIGH | File: GridCluster.java | Line: 15-16
Description: `(int)` cast truncates toward zero rather than toward negative infinity causing negative coordinates to snap to wrong grid cell (e.g., `x = -0.3, mod = 1.0` yields `x = 0.5` instead of correct `-0.5`).
Fix: Replace `(int)(points.getX()/mod)` with `Math.floor(points.getX()/mod)`.

[A17-04] CRITICAL | File: LonLatConverter.java | Line: 80-88
Description: Vincenty direct formula iteration has no maximum iteration count -- pathological inputs (near-antipodal points, extreme distances, NaN/Infinity from upstream) could cause infinite loop.
Fix: Add maximum iteration cap (100-200) and handle non-convergence gracefully.

[A17-05] HIGH | File: LonLatConverter.java | Line: 115-117
Description: Bearing calculation adds 90 degrees to `Math.atan2(y,x)` but does not normalize result to `[0, 360)` -- certain x/y combinations produce negative or out-of-range bearings fed into Vincenty formula.
Fix: Normalize to `[0, 360)` using modulo arithmetic; handle degenerate case x=0, y=0.

[A17-06] MEDIUM | File: LonLatConverter.java | Line: 13-14
Description: Origin coordinates hard-coded to Sydney, Australia as public mutable fields -- latitude 90 (pole) causes `Math.tan(rad(90))` to approach infinity causing numerical instability or infinite loop.
Fix: Make fields private; validate longitude `[-180, 180]` and latitude `[-90, 90]`; reject pole values causing singularities.

[A17-07] HIGH | File: MovingAverage.java | Line: 16-23
Description: Window allows `_size + 1` elements before eviction (post-increment comparison) causing first `_size` results to be expanding-window averages; no guard against `_size <= 0` producing degenerate behavior.
Fix: Validate `_size > 0` in constructor; adjust eviction condition for consistent fixed-window.

[A17-08] MEDIUM | File: MovingAverage.java | Line: 17, 20
Description: Running sum maintained by incremental add/subtract -- over thousands of calls on long-running RTLS data streams, floating-point rounding errors accumulate and average drifts from true value.
Fix: Use compensated summation (Kahan algorithm) or periodically recompute sum from queue contents.

[A17-09] HIGH | File: Points.java | Line: 61-86
Description: Points used as HashMap keys in `GridCluster.reducePoints()` use exact bitwise double comparison via `Double.doubleToLongBits()` -- floating-point arithmetic may not produce bit-identical results for logically equivalent grid cells causing duplicate map entries.
Fix: Use epsilon-based comparison or ensure all coordinates canonicalized through consistent rounding before use as map keys.

[A17-10] LOW | File: Points.java | Line: 61-86
Description: `hashCode` and `equals` only consider x and y, ignoring weight, timestamp, and centralpoints flag -- two Points with same coordinates but different weights considered equal.
Fix: Document intentional design choice or expand equals/hashCode to include all semantically significant fields.

[A17-11] LOW | File: SessionBean.java, ShockBean.java, SpeedBean.java, Tags.java
Description: Four Serializable DTOs do not override `equals()` or `hashCode()` -- identity-based comparison used instead of value-based if placed in collections.
Fix: Override equals/hashCode based on meaningful fields; add serialization round-trip tests.

[A17-12] LOW | File: ShockBean.java | Line: 12-16, 29
Description: All fields use default (package-private) access rather than private -- same-package classes can bypass getters/setters and directly mutate fields.
Fix: Change all field access to `private`.

[A17-13] MEDIUM | File: GridCluster.java | Line: 31
Description: `density` parsed via `Double.parseDouble(density)` inside loop body on every iteration rather than once; malformed input causes unhandled NFE.
Fix: Change method signature to accept `double` or parse once outside loop with error handling.

[A17-14] CRITICAL | File: LonLatConverter.java | Line: 56-104
Description: `computerThatLonLat` implements Vincenty direct formula with ~30 intermediate variables and multiple trig operations but zero unit tests against known geodetic reference values -- no assurance formula correctly transcribed or longitude wrap-around handled.
Fix: Add tests using published Vincenty test vectors (Vincenty 1975 Table 2, NGS geodetic toolkit); verify at short/long distances, near poles, equator, date line.

[A17-15] LOW | File: LonLatConverter.java | Line: 119-121
Description: For very large x or y values, `x*x` could overflow to Infinity before `Math.sqrt` applied producing incorrect distance results.
Fix: Replace `Math.sqrt(x*x + y*y)` with `Math.hypot(x, y)` (overflow-safe alternative).

## Pass 3: Documentation

### security

[P3-SEC-001] HIGH | File: Databean_security.java | Line: 22
Description: No class-level Javadoc on security data bean that orchestrates access rights loading, login data fetching, and form permissions
Fix: Add class-level Javadoc describing the data bean's role in the security subsystem and its JSP consumers
[P3-SEC-002] HIGH | File: Databean_security.java | Line: 950
Description: init() -- security-critical initialization method that loads access rights, login data, mail config, and BMS credentials -- has no Javadoc
Fix: Add Javadoc to init() documenting the security-critical data loading orchestration and calling context
[P3-SEC-003] HIGH | File: Databean_security.java | Line: 1287-1315
Description: getAccess_level(), getAccess_cust(), getAccess_site(), getAccess_dept() and their setters -- authorization-level accessors with no Javadoc documenting valid values or authorization model
Fix: Add Javadoc with @param/@return tags documenting valid values and the authorization model for each accessor
[P3-SEC-004] HIGH | File: Databean_security.java | Line: 1534-1546
Description: getBms_user(), setBms_user(), getBms_pass(), setBms_pass() -- BMS credential accessors with no Javadoc; security-critical credential handling is completely undocumented
Fix: Add Javadoc documenting BMS credential handling, storage expectations, and security considerations
[P3-SEC-005] MEDIUM | File: Databean_security.java | Line: all
Description: 78 remaining public getter/setter methods have no Javadoc (non-security-critical data accessors)
Fix: Add Javadoc with @param/@return tags to all public getter/setter methods
[P3-SEC-006] HIGH | File: Frm_customer.java | Line: 47
Description: No class-level Javadoc on a 12,943-line servlet that handles user management, driver allocation, master codes, and Wiegand card operations
Fix: Add class-level Javadoc describing the servlet's responsibilities, supported operations, and session requirements
[P3-SEC-007] HIGH | File: Frm_customer.java | Line: 75
Description: doGet() -- 1,295-line method handling 15+ distinct operations with session-based access control -- has no Javadoc
Fix: Add Javadoc documenting the dispatched GET operations, parameter routing, and access control requirements
[P3-SEC-008] HIGH | File: Frm_customer.java | Line: 1372
Description: doPost() -- handles user creation, deletion, password changes, master code programming, vehicle allocation -- has no Javadoc
Fix: Add Javadoc documenting the dispatched POST operations, method parameter routing, and authorization model
[P3-SEC-009] HIGH | File: Frm_customer.java | Line: 2240
Description: checkWeigand() -- Wiegand card ID validation for physical access control -- has no Javadoc documenting validation logic, return semantics, or card format support
Fix: Add Javadoc with @param/@return/@throws documenting validation logic, return semantics, and supported card formats
[P3-SEC-010] MEDIUM | File: Frm_customer.java | Line: 8614
Description: isValidEmailAddress(String email) -- no Javadoc documenting the regex pattern or edge cases
Fix: Add Javadoc with @param/@return documenting the validation regex pattern and edge cases
[P3-SEC-011] MEDIUM | File: Frm_customer.java | Line: 12006, 12018
Description: CreateConnection() and closeConnection() -- no Javadoc
Fix: Add Javadoc documenting the JNDI connection factory and connection lifecycle
[P3-SEC-012] LOW | File: Frm_customer.java | Line: 1291
Description: // TODO Auto-generated catch block -- unfinished error handling
Fix: Implement proper error handling or add documentation justifying the empty catch block
[P3-SEC-013] HIGH | File: Frm_login.java | Line: 21
Description: No class-level Javadoc on the primary login authentication servlet
Fix: Add class-level Javadoc describing the authentication flow, session management, and security considerations
[P3-SEC-014] HIGH | File: Frm_login.java | Line: 29
Description: doPost() -- the entire authentication flow (credential lookup, plaintext password comparison, session creation, redirect) has no Javadoc documenting the auth protocol, session attributes set, or failure modes
Fix: Add Javadoc documenting the authentication protocol, session attributes, failure modes, and redirect behavior
[P3-SEC-015] MEDIUM | File: Frm_login.java | Line: 144, 157
Description: CreateConnection() and closeConnection() -- no Javadoc
Fix: Add Javadoc documenting the JNDI connection factory and connection lifecycle
[P3-SEC-016] MEDIUM | File: Frm_login.java | Line: 111
Description: Misleading error message: System.out.println("Frm_security-->: " + e) -- references wrong class name (Frm_security instead of Frm_login)
Fix: Correct the error message to reference Frm_login and replace System.out.println with proper logging
[P3-SEC-017] HIGH | File: Frm_security.java | Line: 47
Description: No class-level Javadoc on the primary security operations controller (authentication, password management, access rights, mail config)
Fix: Add class-level Javadoc describing the servlet's security responsibilities and supported operations
[P3-SEC-018] HIGH | File: Frm_security.java | Line: 57
Description: doPost() -- central security dispatcher for ~30 operations including login, password reset/change/expire, access rights -- has no Javadoc
Fix: Add Javadoc documenting the op_code routing, supported operations, authorization model, and session requirements
[P3-SEC-019] HIGH | File: Frm_security.java | Line: 2169
Description: generateRandomCharacters(int length) -- generates temporary passwords for password reset flow -- has no Javadoc documenting character set, entropy, or usage
Fix: Add Javadoc with @param/@return documenting character set, entropy guarantees, and password reset usage context
[P3-SEC-020] HIGH | File: Frm_security.java | Line: 4152
Description: esapiNormalizeParam(String) -- ESAPI HTML encoding for input sanitization -- has no Javadoc; this is a security-critical sanitization method
Fix: Add Javadoc documenting what is normalized, the encoding strategy, and when to use this vs esapiNormalizeUserNameParam
[P3-SEC-021] HIGH | File: Frm_security.java | Line: 4161
Description: esapiNormalizeUserNameParam(String) -- ESAPI encoding variant for usernames -- has no Javadoc explaining difference from esapiNormalizeParam or the @ re-encoding behavior
Fix: Add Javadoc documenting the @ re-encoding behavior and when to use this instead of esapiNormalizeParam
[P3-SEC-022] MEDIUM | File: Frm_security.java | Line: 4045
Description: sendMail(...) -- email sending utility used for password resets -- has no Javadoc
Fix: Add Javadoc with @param/@return/@throws documenting parameters, failure modes, and security considerations
[P3-SEC-023] LOW | File: Frm_security.java | Line: 143
Description: clearVectors() -- empty method body, no Javadoc explaining why it is a no-op
Fix: Add Javadoc explaining why the method body is empty or implement the expected behavior
[P3-SEC-024] MEDIUM | File: Frm_security.java | Line: 258, 335
Description: saveDashboardSubscription() and deleteSubscription() -- public methods with no Javadoc
Fix: Add Javadoc with @param/@throws documenting subscription management operations
[P3-SEC-025] MEDIUM | File: Frm_security.java | Line: 147, 159
Description: CreateConnection() and closeConnection() -- no Javadoc
Fix: Add Javadoc documenting the JNDI connection factory and connection lifecycle
[P3-SEC-026] HIGH | File: Frm_security.java | Line: 66
Description: Plaintext password logged in doPost entry point: log.info(... + ";password:" + req.getParameter("password") + ";") -- no Javadoc or inline warning about this security-critical logging behavior
Fix: Remove plaintext password logging and add Javadoc warning about sensitive parameter handling
[P3-SEC-027] MEDIUM | File: Frm_security.java | Line: 2526
Description: Misleading log: log.info("Method: chg_bms_pass()...") appears inside chg_pass() method, not chg_bms_pass()
Fix: Correct the log message to reference chg_pass() instead of chg_bms_pass()
[P3-SEC-028] LOW | File: Frm_security.java | Line: 3392
Description: // TODO Auto-generated catch block -- unfinished error handling in mail_conf_dyn
Fix: Implement proper error handling or add documentation justifying the empty catch block
[P3-SEC-029] HIGH | File: Frm_vehicle.java | Line: 57
Description: No class-level Javadoc on 16,269-line vehicle management servlet handling firmware updates, remote commands, network settings, diagnostic sync
Fix: Add class-level Javadoc describing the servlet's responsibilities and supported vehicle operations
[P3-SEC-030] HIGH | File: Frm_vehicle.java | Line: 79
Description: doPost() -- dispatches ~35 operations including firmware sync, broadcast, reboot, remote access, spare swap -- has no Javadoc
Fix: Add Javadoc documenting the method parameter routing, supported operations, and authorization requirements
[P3-SEC-031] MEDIUM | File: Frm_vehicle.java | Line: 15476, 15488
Description: CreateConnection() and closeConnection() -- no Javadoc
Fix: Add Javadoc documenting the JNDI connection factory and connection lifecycle
[P3-SEC-032] LOW | File: Frm_vehicle.java | Line: 15492
Description: intToByteArray(int a) -- no Javadoc on utility method
Fix: Add Javadoc documenting byte order (big-endian), usage context, and purpose
[P3-SEC-033] LOW | File: Frm_vehicle.java | Line: 2724, 2728
Description: getVs_status()/setVs_status() -- no Javadoc
Fix: Add Javadoc documenting valid VOR status values and their semantics
[P3-SEC-034] LOW | File: Frm_vehicle.java | Line: 14976
Description: clearVectors() -- empty method body with no Javadoc
Fix: Add Javadoc explaining why the method body is empty or implement the expected behavior
[P3-SEC-035] INFO | File: Frm_vehicle.java | Line: 14723
Description: //TODO: Do we sync the VOR setting until we found the VOR is enalbed? -- open design question with typo "enalbed"
Fix: Resolve the design question, fix the typo "enalbed" to "enabled", and document the decision
[P3-SEC-036] INFO | File: Frm_vehicle.java | Line: 14789
Description: //TODO: Do we sync the full lock out settings until we found the full lockout enabled? -- open design question
Fix: Resolve the design question and document the synchronization decision
[P3-SEC-037] MEDIUM | File: GetGenericData.java | Line: 19
Description: No class-level Javadoc; purpose of this servlet is unclear from the code alone
Fix: Add class-level Javadoc explaining the servlet's purpose or mark as deprecated if it is unused stub code
[P3-SEC-038] MEDIUM | File: GetGenericData.java | Line: 32
Description: doGet() -- acquires DB connection but performs no operations; appears to be stub code -- has no Javadoc explaining if this is intentional
Fix: Add Javadoc explaining the stub status or complete the implementation; consider removing if unused
[P3-SEC-039] LOW | File: GetGenericData.java | Line: 75, 87
Description: CreateConnection() and closeConnection() -- no Javadoc
Fix: Add Javadoc documenting the JNDI connection factory and connection lifecycle
[P3-SEC-040] INFO | File: GetGenericData.java | Line: 29
Description: // TODO Auto-generated constructor stub -- IDE placeholder
Fix: Remove the TODO comment and implement the constructor or leave empty with documentation

### dao

[A07-1] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/BatteryDAO.java | Line: 16, 74, 134, 250, 351, 386
Description: All 6 public methods lack Javadoc documenting parameters, return semantics, or SQL operations performed
Fix: Add Javadoc with @param, @return, and @throws to all 6 public methods and add class-level Javadoc
[A07-2] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java | Line: 20, 76, 141, 249, 298, 352, 402, 489, 538
Description: All 9 public methods lack Javadoc; critical methods with side effects (IDDENY messages, licence expiry updates) are undocumented
Fix: Add Javadoc with @param, @return, and @throws to all 9 public methods, especially documenting side effects, and add class-level Javadoc
[A07-3] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java | Line: 17, 71, 122, 179, 235, 293, 342, 401, 460, 511, 559, 924, 973, 1009, 1055, 1098, 1141, 1174
Description: All 18 public methods lack Javadoc; saveLicenseExpiryBlackListInfo (364-line method) has undocumented parameter expectations and error return semantics
Fix: Add Javadoc with @param, @return, and @throws to all 18 public methods and add class-level Javadoc
[A07-4] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/ImpactDAO.java | Line: 33, 98, 178, 258, 342, 428, 605, 689, 826, 1042, 1162
Description: All 11 public methods lack Javadoc; heavily overloaded methods (getImpacts, getImpactsByUnit, getImpactsByDriver) are indistinguishable without reading implementation
Fix: Add Javadoc with @param, @return, and @throws to all 11 public methods, clearly distinguishing overloads, and add class-level Javadoc
[A07-5] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java | Line: 30, 199, 376, 443, 541, 608, 907, 1389, 1789, 2109, 2440, 2481, 2632, 3487, 4728, 4805
Description: All 16 public methods in 4850+ line file lack Javadoc; confusing naming variants (saveDriverInfo/saveDriverInfo1/saveDriverInfoAU/saveDriverInfoAu) are undifferentiated
Fix: Add Javadoc with @param, @return, and @throws to all 16 public methods clarifying naming variants, and add class-level Javadoc
[A07-6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java | Line: 381
Description: Log statement in getCurrentCheckCd incorrectly reads "Inside ImportDAO Method : saveQuestionsTab" due to copy-paste error
Fix: Change log message at line 381 to reference the correct method name getCurrentCheckCd
[A07-7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/LockOutDAO.java | Line: 15, 80
Description: Both public methods (getLockOutData, getLockOutDataNtlRpt) lack Javadoc
Fix: Add Javadoc with @param, @return, and @throws to both public methods and add class-level Javadoc
[A07-8] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dao/LockOutDAO.java | Line: 56-58, 120-123
Description: getLockOutData maps unknown reason codes to "Other" but getLockOutDataNtlRpt maps them to "Question" with no comment explaining the discrepancy
Fix: Investigate whether the differing default values are intentional; add documenting comment or fix the likely copy-paste bug
[A07-9] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java | Line: 48, 105
Description: DB-access methods init() and selectMesssage() lack Javadoc; selectMesssage has a typo in method name (triple 's')
Fix: Add Javadoc to init() and selectMesssage(), and consider renaming selectMesssage to selectMessage
[A07-10] LOW | File: WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java | Line: 23, 26, 30, 34, 39, 44
Description: Six simple getter/setter methods lack Javadoc
Fix: Add minimal Javadoc to getter/setter methods
[A07-11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java | Line: 26, 127, 181, 267, 316, 433
Description: All 6 public methods lack Javadoc; overloaded getChecks (3 overloads) and getChecksByDriver (2 overloads) have different return types with inadequate inline annotation
Fix: Add Javadoc with @param, @return, and @throws to all 6 public methods distinguishing each overload, and add class-level Javadoc
[A07-12] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java | Line: 17, 460, 498
Description: All 3 public methods lack Javadoc; register() is a 440-line method with 9 parameters performing multi-table inserts entirely undocumented
Fix: Add Javadoc with @param, @return, and @throws to all 3 public methods, especially documenting register()'s complex transaction, and add class-level Javadoc
[A07-13] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java | Line: 53, 102, 159, 211, 267, 321, 376, 437, 472, 507, 543, 581, 644, 680, 717, 749, 782, 865, 927, 997, 1080, 1226, 1287, 1392, 1559, 1628, 1677, 1738, 1801, 1811, 1962, 2015, 2079, 2115, 2152, 2368, 2590, 2645, 2681
Description: All 39 public methods in 2730+ line file lack Javadoc; Linde-specific variant methods have no documentation explaining the Linde vs non-Linde distinction
Fix: Add Javadoc with @param, @return, and @throws to all 39 public methods, document Linde-specific variants, and add class-level Javadoc
[A07-14] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java | Line: 996
Description: Comment "get working hours total in muniutes" precedes getWorkDays which returns work days not hours; copy-pasted from line 926 and actively misleading
Fix: Replace the comment at line 996 with an accurate description such as "get work days array" for the getWorkDays method
[A07-15] INFO | File: All 10 files in WEB-INF/src/com/torrent/surat/fms6/dao/ | Line: N/A
Description: No class-level Javadoc on any of the 10 DAO classes describing purpose, tables, or role in the application
Fix: Add class-level Javadoc to all 10 DAO classes documenting primary tables and data domain
[A07-16] INFO | File: WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java | Line: 4351
Description: The only Javadoc in the entire 10-file DAO package is on a private method (normalizeTimeFormat); 0 of 120 public methods have Javadoc
Fix: Prioritize adding Javadoc to all 120 public methods across the DAO package

### util-A-F

[DOC-BEAN-01] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/BeanComparator.java | Line: 30-104
Description: All method comments use `/* */` style instead of Javadoc `/** */`; these will not appear in generated Javadoc.
Fix: Convert all `/* */` method comments to `/** */` Javadoc comments.
[DOC-BEAN-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/BeanComparator.java | Line: 104
Description: Comment says "Implement the Comparable interface" but the class implements `Comparator`, not `Comparable`.
Fix: Change comment to "Implement the Comparator interface".
[DOC-CFTS-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Line: 11
Description: Missing class-level Javadoc explaining that this alert checks CFTS inspection due dates and sends email notifications.
Fix: Add class-level Javadoc describing CFTS inspection due date checking and email notification behavior.
[DOC-CFTS-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Line: 14
Description: Public method `checkDueDate()` has no Javadoc documenting its behavior, side-effects (sends emails, updates alert_status), or thrown SQLException.
Fix: Add Javadoc to `checkDueDate()` describing its email-sending and alert_status-updating side-effects.
[DOC-CFTS-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Line: 279
Description: Public method `getCustGroupList()` has no Javadoc documenting the returned customer/site group data structure.
Fix: Add Javadoc to `getCustGroupList()` describing return type and data structure.
[DOC-CCOMP-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomComparator.java | Line: 7
Description: Missing class-level Javadoc explaining that this comparator sorts `DriverLeagueBean` by driver name in descending order.
Fix: Add class-level Javadoc documenting the descending driver name sort behavior.
[DOC-CCOMP-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomComparator.java | Line: 10-12
Description: Public method `compare()` has no Javadoc; the descending sort order is undocumented and could surprise callers.
Fix: Add Javadoc to `compare()` noting the descending sort order.
[DOC-CCOMP-03] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomComparator.java | Line: 11
Description: Residual IDE-generated `TODO Auto-generated method stub` comment left in production code.
Fix: Remove the IDE-generated TODO comment.
[DOC-CUPL-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 38
Description: Missing class-level Javadoc explaining this servlet handles CSV uploads for GMTP ID lookups and firmware push operations.
Fix: Add class-level Javadoc documenting the two action modes ("gmtp" and "firmware") and servlet purpose.
[DOC-CUPL-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 45
Description: Public method `doPost()` has no Javadoc documenting its multi-action logic, expected request parameters, or JSON response format.
Fix: Add Javadoc to `doPost()` documenting expected parameters (`src`, `customer`, `action`, `email`, `file`) and response format.
[DOC-CUPL-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 322
Description: Public method `read(String)` has no Javadoc documenting its CSV parsing contract, delimiter handling, or character sanitization.
Fix: Add Javadoc to `read()` describing CSV parsing behavior, delimiter, and sanitization rules.
[DOC-CUPL-04] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 294
Description: Residual IDE-generated `TODO Auto-generated catch block` left in production code.
Fix: Remove the IDE-generated TODO comment and add proper error handling or logging.
[DOC-DBUT-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DBUtil.java | Line: 10
Description: Missing class-level Javadoc explaining its role as the central JNDI-based connection factory.
Fix: Add class-level Javadoc describing the JNDI connection factory purpose.
[DOC-DBUT-02] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DBUtil.java | Line: 14-19, 29-34
Description: Javadoc declares `@exception SQLException` but methods throw `Exception`; `@param void` is non-standard; `getMySqlConnection` Javadoc is identical to `getConnection` and does not mention MySQL vs PostgreSQL difference.
Fix: Update `@exception` to `Exception`, remove `@param void`, and differentiate `getMySqlConnection` Javadoc to mention MySQL.
[DOC-DUTIL-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 39
Description: Missing class-level Javadoc on the largest utility class in the package (1087 lines, 50+ methods) with zero documentation of scope or organization.
Fix: Add class-level Javadoc summarizing the utility categories (HTML helpers, formatting, date ops, math, file handling, etc.).
[DOC-DUTIL-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: all
Description: Every public method (50+) lacks Javadoc; key methods with non-obvious contracts include `calculateTime`, `convert_time`, `caculateImpPercentage`, and `isVehichleDurationHired`.
Fix: Add Javadoc to all public methods, prioritizing those with non-obvious contracts.
[DOC-DUTIL-03] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 346-413, 415-482
Description: `convert_time(int msec)` parameter says "msec" (milliseconds) but divides by 10, implying deciseconds; inline comment does not clarify input unit.
Fix: Rename parameter to `deciseconds` or add Javadoc clarifying the input unit is deciseconds (1/10th second).
[DOC-DUTIL-04] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 1052-1082
Description: `getLocationFilter` hard-codes Visy-specific customer ID ("26") and user ID ("166207") with hard-coded location codes; inline comment says "quick impl" but no TODO or Javadoc exists.
Fix: Add Javadoc documenting the hard-coded Visy-specific behavior and add a TODO to externalize the configuration.
[DOC-DUTIL-05] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 509
Description: Method names `caculatePercentage`, `caculateImpPercentage`, and `generateRadomName` are misspelled with no Javadoc to clarify.
Fix: Add Javadoc noting correct spelling and consider creating correctly-spelled aliases that delegate to the originals.
[DOC-DTUT-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java | Line: 14
Description: Missing class-level Javadoc on a central date utility class with 22 public methods and no documentation of date format conventions or thread-safety.
Fix: Add class-level Javadoc documenting expected date format conventions and thread-safety considerations.
[DOC-DTUT-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java | Line: all
Description: All 22 public methods lack Javadoc; naming differences like `isValidDate` (yyyy/MM/dd HH:mm:ss) vs `isValidDates` (dd/MM/yyyy) are confusing without documentation.
Fix: Add Javadoc to all public methods specifying expected date format strings and return value semantics.
[DOC-DTUT-03] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java | Line: 45-71
Description: `stringToSQLDate` contains an undocumented heuristic that swaps dd/MM/yyyy and MM/dd/yyyy based on whether day or month exceeds 12; ambiguous for dates where both are <= 12.
Fix: Add Javadoc documenting the date-format heuristic and its ambiguity limitations for dates where both day and month are <= 12.
[DOC-DEXP-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Line: 12
Description: Class has an inline `//` comment instead of proper Javadoc `/** */`; will not appear in generated documentation.
Fix: Convert the `//` comment to a `/** */` Javadoc class comment.
[DOC-DEXP-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Line: 15
Description: Public method `checkExpiry()` has no Javadoc documenting its database queries, email-sending side-effects, or alert threshold logic.
Fix: Add Javadoc to `checkExpiry()` describing alert thresholds (expired, 1-week, 1-month, 3-month, 6-month) and side-effects.
[DOC-DMED-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Line: 14
Description: Missing class-level Javadoc explaining that this alert checks driver medical certificate dates and sends email notifications for today, one-week, and one-month windows.
Fix: Add class-level Javadoc describing medical certificate expiry alert behavior and notification windows.
[DOC-DMED-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Line: 18
Description: Public method `checkInterval()` has no Javadoc documenting its database queries, date comparisons, and email insertion behavior.
Fix: Add Javadoc to `checkInterval()` describing its database query, date comparison, and email insertion workflow.
[DOC-DTCK-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 4
Description: Missing class-level Javadoc explaining this is a legacy date checker, its expected dd/mm/yyyy format, or thread-safety issues with static mutable fields.
Fix: Add class-level Javadoc documenting expected date format, legacy status, and thread-safety warning.
[DOC-DTCK-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 11, 53
Description: `greaterThan` and `equalTo` have non-obvious parameter ordering; `greaterThan(dt2, dt1)` returns true if dt2 > dt1 but parameter names reverse natural reading order.
Fix: Add Javadoc clarifying parameter semantics and comparison direction.
[DOC-DTCK-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 84, 109
Description: `first(String)` returns first day of next month and `last(String)` returns last day of month after next; names are entirely misleading without Javadoc.
Fix: Add Javadoc explaining actual return values or rename methods to `firstOfNextMonth` and `lastOfMonthAfterNext`.
[DOC-DTCK-04] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 141-150
Description: `isleap(int)` contains a bug (`y%1000` should be `y%100` for century check) and has no Javadoc; absence of docs makes it impossible to know if the bug is intentional.
Fix: Fix the bug (`y%1000` to `y%100`) and add Javadoc documenting the standard leap year algorithm.
[DOC-DTCK-05] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 153-175
Description: `between` and `conflict` have complex date range overlap logic with 3 and 4 string parameters respectively; parameter order and semantics are unknowable without Javadoc.
Fix: Add Javadoc documenting parameter order (start date, end date) and range overlap semantics.
[DOC-ENCT-01] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java | Line: 9
Description: Class name `EncryptTest` is misleading; it is a production encryption utility (not a test) using a character-shift cipher with length-based prefix, confirmed decompiled code.
Fix: Add class-level Javadoc clarifying this is a production utility, not a test, and document the algorithm; consider renaming.
[DOC-ENCT-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java | Line: 16, 97
Description: `encrypt(String)` and `decrypt(String)` have no Javadoc documenting the encryption algorithm, 10-character prefix convention, or input constraints.
Fix: Add Javadoc to both methods documenting the character-shift algorithm, prefix convention, and minimum input length for decrypt.
[DOC-ENCT-03] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java | Line: 1-4
Description: Decompiler header comment from 2006 is still present; not functional documentation and potentially confusing as provenance metadata.
Fix: Remove or relocate the decompiler header to a version-control note.
[DOC-EXUT-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Line: 13
Description: Missing class-level Javadoc explaining the reflection-based report generation pattern and relationship to `Frm_excel` and `MailExcelReports`.
Fix: Add class-level Javadoc describing the reflection-based report loading pattern and class dependencies.
[DOC-EXUT-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Line: 34, 61, 84, 107, 129, 134
Description: All 6 public methods lack Javadoc; `getExcel` dynamically loads classes by name (security implications), `params` is comma-delimited, `getExportDir` uses fragile relative path traversal.
Fix: Add Javadoc to all methods documenting parameter formats, security considerations, and path traversal logic.
[DOC-EXUT-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Line: 134-144
Description: `getExportDir()` computes directory path by navigating 8 levels up (`../../../../../../../../excelrpt/`) with no documentation of why this depth is needed.
Fix: Add Javadoc explaining the directory traversal rationale and target directory; consider externalizing the path to configuration.
[DOC-FCFTP-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Line: 17
Description: Missing class-level Javadoc; informational block comment (lines 18-23) about this class being potentially dead code uses `/* */` instead of Javadoc.
Fix: Convert the `/* */` block comment to a `/** */` Javadoc comment so the dead-code warning appears in generated docs.
[DOC-FCFTP-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Line: 24
Description: Public method `upload_quest_ftp()` has no Javadoc documenting its complex workflow (query FTP queue, look up hierarchy, generate binary PREOP.TXT, insert FTP commands, clean up).
Fix: Add Javadoc to `upload_quest_ftp()` describing the full FTP upload workflow and database interactions.

### util-G-Z

[P3-UGZ-001] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: class level
Description: No class-level Javadoc on GDPR deletion class; must document what personal data is deleted, retention period logic, eligibility criteria, and 6 master/detail table pairs affected
Fix: Add class-level Javadoc documenting deleted data tables, retention period source (FMS_CUST_MST.gdpr_data), and inactive-driver eligibility criteria (inactive > 30 days)
[P3-UGZ-002] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: call_gdpr_delete_data()
Description: No method Javadoc on security-critical method performing irreversible deletion of personal data across 9 tables
Fix: Add Javadoc documenting deletion order (detail before master), retention period source, and inactive-driver filter
[P3-UGZ-003] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: 110
Description: Exception message references send_timezone() which is misleading; this is GdprDataDelete -- copy-paste error in error message string
Fix: Correct the exception message to reference GdprDataDelete and call_gdpr_delete_data()
[P3-UGZ-004] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java | Line: class level
Description: No class-level Javadoc; should document purpose as HTTP GET utility for report generation
Fix: Add class-level Javadoc describing HTTP GET utility purpose
[P3-UGZ-005] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java | Line: getHTML(String, String)
Description: No Javadoc; should document parameters (URL base and parameter suffix), 10-minute read timeout, and return value
Fix: Add method Javadoc with @param and @return tags documenting URL parameters and timeout
[P3-UGZ-006] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java | Line: getHTML1(String)
Description: No Javadoc; should document difference from getHTML (single URL parameter, 15-minute timeout, timing logs)
Fix: Add method Javadoc documenting single-URL variant with 15-minute timeout
[P3-UGZ-007] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java | Line: now(String)
Description: No Javadoc on simple date formatting utility
Fix: Add Javadoc with @param for format string and @return for formatted date
[P3-UGZ-008] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java | Line: class level
Description: No class-level Javadoc; should document servlet purpose, supported import types (drivers, driversUK, driversAU, questions, questions-tab, vehicles), and CSV format expectations
Fix: Add class-level Javadoc documenting supported import types and CSV format expectations
[P3-UGZ-009] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java | Line: doPost(...)
Description: No Javadoc on main servlet entry point; should document required request parameters (src, customer, location, department, access_level, access_cust, access_site, access_dept, file)
Fix: Add method Javadoc listing all required request parameters
[P3-UGZ-010] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java | Line: private methods
Description: Numerous private validation methods (validateCSV, validateCSVIndividualD, validateCSVIndividual, validateCSVIndividualTab, etc.) are undocumented
Fix: Add brief Javadoc to each private validation method describing its validation rules
[P3-UGZ-011] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java | Line: class level
Description: No class-level Javadoc; should document dual logging to file and database
Fix: Add class-level Javadoc documenting file logging (InfoLogs/fms.{date}.log) and database logging (SEC_LOG_DETAILS)
[P3-UGZ-012] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java | Line: writelog(String)
Description: No Javadoc; should document expected message format ([uid/machineId] remarks) and synchronized write behavior
Fix: Add method Javadoc documenting message format parsing and synchronization
[P3-UGZ-013] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java | Line: class level
Description: No class-level Javadoc; should document site-specific configuration loader, XML file location, and supported site names (UK, AU, hiremech, westexe, MLA)
Fix: Add class-level Javadoc documenting XML config source and supported sites
[P3-UGZ-014] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java | Line: readXMLFile()
Description: No Javadoc; should document XML structure expected, file path fallback logic, and static fields populated
Fix: Add method Javadoc documenting XML structure, fallback from settings.xml to setting_au.xml, and populated fields
[P3-UGZ-015] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java | Line: now(String)
Description: No Javadoc on simple date formatting utility (duplicate of GetHtml.now)
Fix: Add Javadoc and consider consolidating with GetHtml.now
[P3-UGZ-016] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java | Line: class level
Description: Existing block comment is minimal; does not describe which report, the data source (penom_database), or the IO data fields
Fix: Expand block comment to Javadoc documenting report identity, data source, and field descriptions
[P3-UGZ-017] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java | Line: init()
Description: Inline comment exists but is not Javadoc; should be converted to Javadoc documenting DB connection and data fetch lifecycle
Fix: Convert inline comment to proper Javadoc
[P3-UGZ-018] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java | Line: clear_variables()
Description: Has inline comment but no Javadoc
Fix: Convert inline comment to Javadoc
[P3-UGZ-019] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java | Line: getters/setters
Description: 25+ public getters undocumented; low severity as they are simple bean accessors
Fix: Add brief Javadoc to public getters describing the data field returned
[P3-UGZ-020] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java | Line: class level
Description: Existing block comment is minimal, same issue as LogicBean_filter
Fix: Expand block comment to Javadoc documenting report identity, sorting, and time conversion
[P3-UGZ-021] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java | Line: init(), clear_variables()
Description: Inline comments present but not Javadoc
Fix: Convert inline comments to proper Javadoc
[P3-UGZ-022] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java | Line: getters/setters
Description: 35+ public accessors undocumented; low severity as simple bean properties
Fix: Add brief Javadoc to public getters
[P3-UGZ-023] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java | Line: class level
Description: No class-level Javadoc; should document that this bean provides menu/navigation data based on user group access rights
Fix: Add class-level Javadoc documenting menu data retrieval and access rights integration
[P3-UGZ-024] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java | Line: fetchform_rights()
Description: No Javadoc on security-relevant method that queries user group and form access rights
Fix: Add Javadoc documenting user group query and access rights returned
[P3-UGZ-025] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java | Line: fetchMenuAttr1()
Description: No Javadoc; should document module fetching logic
Fix: Add Javadoc documenting module attribute retrieval
[P3-UGZ-026] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java | Line: fetchSubModule()
Description: No Javadoc; should document sub-module form fetching
Fix: Add Javadoc documenting sub-module form retrieval
[P3-UGZ-027] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java | Line: init()
Description: No Javadoc on entry point that dispatches to MOD or SUBMOD logic
Fix: Add Javadoc documenting dispatch logic
[P3-UGZ-028] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean1.java | Line: class level
Description: No class-level Javadoc; should document difference from Menu_Bean (priority ordering, form description)
Fix: Add class-level Javadoc distinguishing from Menu_Bean and documenting priority ordering
[P3-UGZ-029] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean1.java | Line: fetchform_rights(), fetchMenuAttr1(), fetchSubModule()
Description: No Javadoc on any of these public methods; same security-relevance as Menu_Bean
Fix: Add Javadoc to all three public methods documenting access rights queries
[P3-UGZ-030] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean1.java | Line: 192
Description: Debug code appends raw SQL query string as a form name entry via FormName.add(query1); undocumented and surprising
Fix: Document the debug behavior or remove the debug code
[P3-UGZ-031] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java | Line: class level
Description: No class-level Javadoc on migration utility; must document source/target schemas/tables, two migration modes (SITE vs DEPT level), and data flow direction
Fix: Add class-level Javadoc documenting migration modes, source tables, and target tables
[P3-UGZ-032] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java | Line: callMigrateMaster()
Description: No method Javadoc; must document processing of all active customers, SITE mode (copies to FMS_LOC_OVERRIDE), DEPT mode (populates FMS_DEPT_OVERRIDE), max 40 supervisors per department, and supervisor_access value '1&2&4'
Fix: Add comprehensive Javadoc documenting both migration modes, table operations, and constraints
[P3-UGZ-033] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java | Line: 202-230
Description: Large block of commented-out code for outgoing message insertion; should be documented or removed
Fix: Remove commented-out code or add comment explaining why it is retained
[P3-UGZ-034] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java | Line: class level
Description: No class-level Javadoc on password/security class; must document 3-month password lifetime, 7-day advance warning, customer-level pword_restriction toggle, and one-time alert flag
Fix: Add class-level Javadoc documenting all password expiry rules and alert behavior
[P3-UGZ-035] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java | Line: checkExpiry()
Description: No method Javadoc; must document 3-month expiry interval, 7-day warning window, email insertion to email_outgoing table, and pword_alert_sent flag update
Fix: Add method Javadoc documenting expiry logic, email dispatch, and duplicate prevention flag
[P3-UGZ-036] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/PurgeData.java | Line: class level
Description: Empty class with no Javadoc; should document whether this is a placeholder, deprecated, or pending implementation
Fix: Add Javadoc indicating status (placeholder/deprecated/pending) or remove the empty class
[P3-UGZ-037] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: class level
Description: No class-level Javadoc; should document central runtime configuration with JNDI datasource names, firmware server settings, SMS API config, and feature constants
Fix: Add class-level Javadoc documenting configuration categories and usage
[P3-UGZ-038] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: fields
Description: No Javadoc on ~80+ public static fields; especially important for security-sensitive fields like PASSWORD, firmwarepass, USERNAME, API_ID
Fix: Add Javadoc to all public static fields, especially security-sensitive ones
[P3-UGZ-039] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java | Line: class level
Description: No class-level Javadoc; should document SMS sending via Clickatell API from sms_outgoing table
Fix: Add class-level Javadoc documenting Clickatell API integration and sms_outgoing processing
[P3-UGZ-040] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java | Line: init()
Description: No Javadoc on public entry point; should document DB connection and pending SMS dispatch
Fix: Add method Javadoc documenting initialization and SMS dispatch flow
[P3-UGZ-041] INFO | File: WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java | Line: send_sms_message(...) (private)
Description: Has Javadoc but uses PHP-style @param integer $id instead of Java-style @param id; inaccurate documentation style
Fix: Convert to standard Java @param syntax
[P3-UGZ-042] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java | Line: class level
Description: No class-level Javadoc; should document supervisor override deletion and vehicle communication management
Fix: Add class-level Javadoc documenting supervisor master list management
[P3-UGZ-043] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java | Line: deleteSupervisorByUser(String, String, String, String, String)
Description: No Javadoc; should document 5 parameters, site vs dept level deletion, supervisor_access reset to '0&0&0', and IDMAST messaging
Fix: Add method Javadoc with @param tags and deletion behavior documentation
[P3-UGZ-044] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java | Line: deleteSupervisor(String, String, String, String, String)
Description: No Javadoc; should document slot-based deletion, master_code_level lookup, and difference from deleteSupervisorByUser
Fix: Add method Javadoc documenting slot-based deletion and comparison with deleteSupervisorByUser
[P3-UGZ-045] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java | Line: deleteSuperMaster(int, String)
Description: No Javadoc; should document super_master_override table deletion and IDSMAST command difference from IDMAST
Fix: Add method Javadoc documenting super master deletion and IDSMAST command
[P3-UGZ-046] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: class level
Description: Existing block comment is incomplete; does not mention customer settings, local time conversion, or CLD lookup
Fix: Expand block comment to Javadoc covering all utility functions provided
[P3-UGZ-047] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: getLocalTime(String, String)
Description: No Javadoc; should document timezone conversion via time_zone_impl DB function
Fix: Add method Javadoc documenting timezone conversion parameters and DB function call
[P3-UGZ-048] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: getCustomerSettingByUser(String)
Description: No Javadoc; should document retrieval of password policy settings for a user's customer
Fix: Add method Javadoc documenting user-based customer setting retrieval
[P3-UGZ-049] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: getCustomerSetting(String)
Description: No Javadoc; should document retrieval of password policy directly by customer code
Fix: Add method Javadoc documenting customer-code-based setting retrieval
[P3-UGZ-050] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: getDays(int, int)
Description: Has inline comment but no Javadoc
Fix: Convert inline comment to Javadoc with @param and @return
[P3-UGZ-051] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: template()
Description: Has inline comment '//TEMPLATE FOR DB UTILS' but no Javadoc explaining this is a code template, not functional code
Fix: Add Javadoc clarifying this is a non-functional code template
[P3-UGZ-052] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: class level
Description: No class-level Javadoc; should document email dispatch system, supported email types (scheduled reports, alerts), and email_outgoing table processing
Fix: Add class-level Javadoc documenting email dispatch system and supported types
[P3-UGZ-053] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: call_email_au(), call_email()
Description: No Javadoc; should document scheduled email report generation and dispatch
Fix: Add method Javadoc documenting scheduled report email generation
[P3-UGZ-054] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: call_alertemail()
Description: No Javadoc; should document alert email processing
Fix: Add method Javadoc documenting alert email processing
[P3-UGZ-055] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: calibrate_impact()
Description: No Javadoc; name is misleading for a method in an email class -- should document its actual purpose
Fix: Add Javadoc explaining actual purpose and consider renaming the method
[P3-UGZ-056] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: sendMail(...), sendMail1(...)
Description: No Javadoc; should document the SMTP sending mechanism
Fix: Add method Javadoc documenting SMTP sending parameters and behavior
[P3-UGZ-057] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: callLindeReports()
Description: No Javadoc; should document Linde-specific report generation
Fix: Add method Javadoc documenting Linde-specific report generation
[P3-UGZ-058] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/escapeSingleQuotes.java | Line: class level
Description: No Javadoc; simple utility class; class name violates Java naming conventions (lowercase)
Fix: Add class-level Javadoc and consider renaming to EscapeSingleQuotes
[P3-UGZ-059] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/escapeSingleQuotes.java | Line: replaceSingleQuotes(String)
Description: No Javadoc; should document that it escapes single quotes by doubling them for SQL injection prevention
Fix: Add method Javadoc documenting SQL quote escaping behavior
[P3-UGZ-060] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: class level
Description: No class-level Javadoc; should document this is a data repair utility for fixing shared/duplicate department codes across multiple customers
Fix: Add class-level Javadoc documenting data repair purpose and scope
[P3-UGZ-061] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: fix_dept(String, String, String)
Description: No Javadoc; should document the 12 tables updated during department fix operation
Fix: Add method Javadoc listing all 12 affected tables and the fix procedure
[P3-UGZ-062] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: show_cust_dept()
Description: No Javadoc; should document that it populates the department listing for display
Fix: Add method Javadoc documenting department listing population
[P3-UGZ-063] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/mail.java | Line: class level
Description: No class-level Javadoc; should document email sending utility and supported modes (plain, with attachment, auto-CSV-from-HTML)
Fix: Add class-level Javadoc documenting email modes
[P3-UGZ-064] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/mail.java | Line: sendMail(...) (instance)
Description: No Javadoc; should document JNDI mail session lookup and plain HTML email sending
Fix: Add method Javadoc documenting JNDI session and HTML email sending
[P3-UGZ-065] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/mail.java | Line: sendMail(...) (static, 8 params)
Description: No Javadoc; should document the file attachment variant
Fix: Add method Javadoc documenting attachment support and 8 parameters
[P3-UGZ-066] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/mail.java | Line: sendMailAttachment(...)
Description: No Javadoc; should document HTML-table-to-CSV auto-attachment feature using Jsoup parsing
Fix: Add method Javadoc documenting HTML-to-CSV conversion and attachment behavior
[P3-UGZ-067] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java | Line: class level
Description: No class-level Javadoc; password security class should document Oracle-specific password lifecycle checking, fms_password_life configuration table, and expiry/reminder calculation logic
Fix: Add class-level Javadoc documenting password lifecycle rules and Oracle dependency
[P3-UGZ-068] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java | Line: loadDefaultValues()
Description: No Javadoc; should document password reset flag check, lifetime retrieval from fms_password_life, expiry date calculation, and login status recording
Fix: Add method Javadoc documenting password lifecycle checks and login recording
[P3-UGZ-069] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java | Line: getters
Description: getCount(), getDiff(), getRem(), getCount1() have no Javadoc; names are cryptic -- getCount returns expiry status, getDiff returns days until expiry, getRem returns reminder threshold, getCount1 returns reset flag
Fix: Add Javadoc to each getter explaining the actual meaning of the returned value
[P3-UGZ-070] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/password_policy.java | Line: class level
Description: No class-level Javadoc on password policy class; must document rules enforced: username length min/max, password length min/max, source table (fms_password_life), and effective-date lookup logic
Fix: Add class-level Javadoc documenting all password policy rules and source table
[P3-UGZ-071] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/password_policy.java | Line: loadDefaultValues()
Description: No Javadoc; should document effective-date-based policy lookup and 4 policy fields retrieved (userid_min, userid_max, password_min, password_max)
Fix: Add method Javadoc documenting date-based lookup and the four policy fields
[P3-UGZ-072] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/password_policy.java | Line: getUmin(), getUmax(), getPmin(), getPmax()
Description: No Javadoc; names are abbreviated and unclear without documentation
Fix: Add Javadoc to each getter clarifying what U/P min/max represent
[P3-UGZ-073] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java | Line: class level
Description: No class-level Javadoc; should document DST timezone synchronization for vehicle fleet units
Fix: Add class-level Javadoc documenting DST sync purpose and supported regions
[P3-UGZ-074] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java | Line: call_send_timezone()
Description: No Javadoc; should document UK DST transitions, TZONE message format, England-only vehicle targeting, and FMS_STATE_MST.DST update
Fix: Add method Javadoc documenting UK DST logic and TZONE messaging
[P3-UGZ-075] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java | Line: call_send_timezone_au()
Description: No Javadoc; should document AU DST transitions for AEDT (NSW/VIC/ACT/TAS) and ACDT (SA) zones and state-based vehicle filtering
Fix: Add method Javadoc documenting AU DST zones and state filtering
[P3-UGZ-076] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java | Line: call_send_timezone_test()
Description: No Javadoc; appears to be test/debug variant of call_send_timezone() with relaxed conditions
Fix: Add Javadoc documenting test/debug purpose and how it differs from production method
[P3-UGZ-077] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java | Line: class level
Description: No class-level Javadoc; should document pre-op checklist file generation, binary format specification, and firmware version-dependent file selection
Fix: Add class-level Javadoc documenting PREOP file generation and binary format
[P3-UGZ-078] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java | Line: updatepreop()
Description: No Javadoc; should document historical checklist answer correction from 2019-04-01 onward and question matching logic
Fix: Add method Javadoc documenting historical correction and matching logic
[P3-UGZ-079] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java | Line: resyncPreop(List<String>)
Description: No Javadoc; should document vehTCds list format (vehicleType,customer,location,department), FTP upload command generation, and three file format variants (PREOP.TXT, PREOP100.TXT, PREOP150.TXT)
Fix: Add method Javadoc documenting list format, FTP commands, and three firmware-dependent file variants
[P3-UGZ-080] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java | Line: intToByteArray(int)
Description: No Javadoc; should document little-endian byte conversion for the binary file format
Fix: Add method Javadoc documenting little-endian conversion purpose
[P3-UGZ-A1] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: 110
Description: Exception message says "Exception in the send_timezone() Method..." but this is the GDPR delete class; misleading copy-paste error
Fix: Correct exception message to reference GdprDataDelete class and method
[P3-UGZ-A2] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: 64, 276
Description: Exception message says "Exception in the send_timezone() Method..." but this is the fix_department class; same copy-paste error
Fix: Correct exception messages to reference fix_department class and methods
[P3-UGZ-A3] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java | Line: 208
Description: Exception message references "LogicBean_LoginAlerter" but this is LogicBean_filter
Fix: Correct exception message to reference LogicBean_filter
[P3-UGZ-A4] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java | Line: 398
Description: Exception message references "LogicBean_LoginAlerter" but this is LogicBean_filter1
Fix: Correct exception message to reference LogicBean_filter1
[P3-UGZ-A5] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/password_policy.java | Line: 94
Description: Error message says "Exception in the loadDefaultvalues() Method of password_life..." but this is password_policy
Fix: Correct error message to reference password_policy class
[P3-UGZ-A6] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/password_policy.java | Line: 137
Description: Error message says "password_life in..." but this is password_policy.init()
Fix: Correct error message to reference password_policy.init()
[P3-UGZ-A7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java | Line: 100-110
Description: Private method send_sms_message has Javadoc describing it as "sending out email" when it actually sends SMS
Fix: Correct Javadoc to say "sending out SMS" instead of "sending out email"

### bean-A-D

[A01-P3-001] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java, BroadcastmsgBean.java, CanruleBean.java, CustLocDeptBean.java, CustomerBean.java, DailyUsageDeptDataBean.java, DailyUsageHourBean.java, DashboarSubscriptionBean.java, DayhoursBean.java, DehireBean.java, DetailedReportUtil.java, DriverBean.java, DriverImportBean.java, DriverLeagueBean.java | Line: 5,5,3,3,3,6,8,3,5,5,5,5,5,3
Description: None of the 14 bean classes has a class-level Javadoc comment describing its purpose, domain context, or usage.
Fix: Add a Javadoc comment to each class explaining its domain purpose, what entity/report it maps to, and any key usage constraints.
[A01-P3-002] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 27,39,101
Description: Three public methods (getModelList, arrangeData, getWeekList) contain significant business logic but have no Javadoc.
Fix: Add Javadoc with @param and @return descriptions; document the comma-delimited format returned by arrangeData() and non-idempotent behavior of getModelList/getWeekList.
[A01-P3-003] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 44
Description: analyzeAndCombine() method loops over fields checking for Hydraulic strings but the if-block body is empty (no-op), with no documentation of intent.
Fix: Add Javadoc or inline comment clarifying whether this is intentionally a no-op, dead code to be removed, or an unfinished implementation.
[A01-P3-004] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 39-41
Description: Parameterized constructor contains three System.out.println debug statements printing list sizes with no associated comment.
Fix: Remove the debug output or replace with proper logging (e.g., Logger.debug()).
[A01-P3-005] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 57-59
Description: Commented-out System.out.println debug statements within arrangeData() provide no documentation value and clutter the code.
Fix: Remove the commented-out debug statements; if output format needs documenting, do so in method Javadoc instead.
[A01-P3-006] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java | Line: 3
Description: Class named DashboarSubscriptionBean is missing the letter 'd' and should be DashboardSubscriptionBean, misleading developers and propagating the typo to all callers.
Fix: Rename the class to DashboardSubscriptionBean and update all references; at minimum add a class Javadoc noting the intended name if renaming is deferred.
[A01-P3-007] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java, BroadcastmsgBean.java, CanruleBean.java, CustLocDeptBean.java, CustomerBean.java, DailyUsageDeptDataBean.java, DailyUsageHourBean.java, DashboarSubscriptionBean.java, DayhoursBean.java, DehireBean.java, DetailedReportUtil.java, DriverBean.java, DriverImportBean.java, DriverLeagueBean.java | Line: all files
Description: Not a single getter or setter method (approximately 260+) in any of the 14 files has a Javadoc comment; many use cryptic abbreviations.
Fix: Add Javadoc to getters/setters with non-obvious names; prioritize BatteryBean, DetailedReportUtil, CanruleBean, and DriverBean.
[A01-P3-008] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java, DetailedReportUtil.java, CanruleBean.java, DriverBean.java | Line: 11-33,8-28,5-17,8
Description: Multiple files use heavily abbreviated field names (bef_soc, aft_hm, vrpt_veh_*, gmtp_id, src_holder, weigand) with no inline comments or Javadoc explaining their meaning.
Fix: Add field-level Javadoc or inline comments defining each abbreviation; at minimum document BatteryBean before/after semantics, DetailedReportUtil vrpt_* prefix, and DriverBean weigand field.
[A01-P3-009] INFO | File: WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java, BroadcastmsgBean.java, DayhoursBean.java | Line: 7-9,7-9,7-9
Description: Three files contain auto-generated empty Javadoc blocks above serialVersionUID that provide no useful information.
Fix: Either remove the empty Javadoc blocks or add meaningful content noting the serialization contract.
[A01-P3-010] INFO | File: All 14 files in scope | Line: all files
Description: None of the 14 classes has @author or @since tags, making ownership and version history unclear in a legacy codebase.
Fix: Add @author and @since tags to class-level Javadoc when class Javadoc is added per A01-P3-001.
[A01-P3-011] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 27
Description: getModelList() follows getter naming but performs computation, mutates modelList, and is not idempotent; same issue with getWeekList() at line 101.
Fix: Rename to buildModelList()/computeModelList() to signal computation, or add Javadoc explicitly stating non-getter behavior and side effects.
[A01-P3-012] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 34-42
Description: Parameterized constructor takes three raw ArrayList parameters with no documentation of contents, expected ordering, relationship, or null handling.
Fix: Add constructor Javadoc with @param tags explaining what each ArrayList contains (field codes, field names, stop values) and their expected sizes/relationship.

### bean-E-P

[A02-1] MEDIUM | File: EntityBean.java | Line: 5
Description: No class-level Javadoc; purpose of this DTO (entity with id, name, totalno, attribute, locs, depts) is unclear without documentation.
Fix: Add class-level Javadoc describing the bean's purpose and field semantics.
[A02-2] MEDIUM | File: FleetCheckBean.java | Line: 5
Description: No class-level Javadoc; bean carries fleet check data (unit name, avg completion time, frequent failed questions) but purpose and usage context are undocumented.
Fix: Add class-level Javadoc describing the bean's purpose and usage context.
[A02-3] MEDIUM | File: ImpactBean.java | Line: 6
Description: No class-level Javadoc; large bean (57 public methods, ~30 fields) representing impact/shock data with multiple field groups having no explanation of domain meaning.
Fix: Add class-level Javadoc explaining the bean's domain context and field group semantics (blue/amber/red shock, shift variants, monthly report arrays).
[A02-4] MEDIUM | File: ImpactDeptBean.java | Line: 6
Description: No class-level Javadoc; aggregation bean grouping ImpactSummaryBeans by department with undocumented relationship hierarchy.
Fix: Add class-level Javadoc describing the department aggregation hierarchy.
[A02-5] MEDIUM | File: ImpactLocBean.java | Line: 6
Description: No class-level Javadoc; aggregation bean grouping ImpactDeptBeans by location with undocumented relationship hierarchy.
Fix: Add class-level Javadoc describing the location aggregation hierarchy.
[A02-6] MEDIUM | File: ImpactSummaryBean.java | Line: 6
Description: No class-level Javadoc; summary bean aggregating ImpactBeans with location and driver info; relationship to ImpactLocBean/ImpactDeptBean hierarchy is undocumented.
Fix: Add class-level Javadoc describing the summary aggregation and its relationship to ImpactLocBean/ImpactDeptBean.
[A02-7] MEDIUM | File: LicenseBlackListBean.java | Line: 5
Description: No class-level Javadoc; bean carries license blacklist filter criteria including access-level fields with undocumented business rules for blacklisting.
Fix: Add class-level Javadoc documenting blacklist filter criteria and access-level business rules.
[A02-8] MEDIUM | File: LockOutBean.java | Line: 5
Description: No class-level Javadoc; bean represents a fleet lockout event with lockout/unlock times and master code; domain context is undocumented.
Fix: Add class-level Javadoc describing the lockout event domain context.
[A02-9] MEDIUM | File: MaxHourUsageBean.java | Line: 6
Description: No class-level Javadoc; bean groups UnitutilBeans by model for max-hour usage reporting; purpose undocumented.
Fix: Add class-level Javadoc describing the max-hour usage reporting purpose.
[A02-10] MEDIUM | File: MenuBean.java | Line: 5
Description: No class-level Javadoc; bean represents a menu item with form paths and reskin paths; navigation model is undocumented.
Fix: Add class-level Javadoc describing the menu item navigation model.
[A02-11] MEDIUM | File: MymessagesUsersBean.java | Line: 5
Description: No class-level Javadoc; bean carries user messaging subscription data (threshold, email, description); domain purpose is undocumented.
Fix: Add class-level Javadoc describing the messaging subscription domain purpose.
[A02-12] MEDIUM | File: NetworkSettingBean.java | Line: 5
Description: No class-level Javadoc; bean stores WiFi network settings (country, SSID, password); deployment context is undocumented.
Fix: Add class-level Javadoc describing the WiFi network settings deployment context.
[A02-13] MEDIUM | File: NotificationSettingsBean.java | Line: 3
Description: No class-level Javadoc; bean represents notification template settings (header, title, content, signature, enabled flag); purpose undocumented.
Fix: Add class-level Javadoc describing the notification template settings purpose.
[A02-14] MEDIUM | File: PreCheckBean.java | Line: 8
Description: No class-level Javadoc; bean tracks pre-check completion counts by driver with monthly report arrays; relationship to PreCheckDriverBean is undocumented.
Fix: Add class-level Javadoc describing the pre-check tracking and relationship to PreCheckDriverBean.
[A02-15] MEDIUM | File: PreCheckDriverBean.java | Line: 5
Description: No class-level Javadoc; bean holds per-driver pre-check data with monthly check arrays; purpose undocumented.
Fix: Add class-level Javadoc describing the per-driver pre-check data purpose.
[A02-16] MEDIUM | File: PreCheckSummaryBean.java | Line: 6
Description: No class-level Javadoc; summary bean grouping PreCheckBeans by location; hierarchy undocumented.
Fix: Add class-level Javadoc describing the location-grouped pre-check summary hierarchy.
[A02-17] MEDIUM | File: ImpactBean.java | Line: 47
Description: Business logic method addImactMap(int, int) with no Javadoc; method name contains typo ("Imact" instead of "Impact"); lacks @param documentation.
Fix: Add Javadoc with @param tags for month and impact_no parameters.
[A02-18] MEDIUM | File: ImpactLocBean.java | Line: 50
Description: Mutator addArrImpactDeptBean(ImpactDeptBean) appends to internal list (not a simple setter) with no Javadoc.
Fix: Add Javadoc describing the list-append behavior and @param tag.
[A02-19] MEDIUM | File: ImpactSummaryBean.java | Line: 40
Description: Mutator addArrImpact(ImpactBean) appends to internal list (not a simple setter) with no Javadoc.
Fix: Add Javadoc describing the list-append behavior and @param tag.
[A02-20] MEDIUM | File: MaxHourUsageBean.java | Line: 36
Description: Mutator addArrUnitUtil(UnitutilBean) appends to internal list (not a simple setter) with no Javadoc.
Fix: Add Javadoc describing the list-append behavior and @param tag.
[A02-21] MEDIUM | File: PreCheckBean.java | Line: 29
Description: Business logic method addCheckMap(String, int) with no Javadoc; lacks @param documentation for driver name and total.
Fix: Add Javadoc with @param tags for drivername and total parameters.
[A02-22] MEDIUM | File: PreCheckSummaryBean.java | Line: 34
Description: Mutator addArrPrecheck(PreCheckBean) appends to internal list (not a simple setter) with no Javadoc.
Fix: Add Javadoc describing the list-append behavior and @param tag.
[A02-23] LOW | File: EntityBean.java | Line: 19-52
Description: All 12 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 12 getter/setter methods.
[A02-24] LOW | File: FleetCheckBean.java | Line: 11-28
Description: All 6 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 6 getter/setter methods.
[A02-25] LOW | File: ImpactBean.java | Line: 52-252
Description: All 56 getter/setter methods lack Javadoc; fields like blueshock[8], ambershock[8], redshock[8], blueshockShift[8][3] and iotime have non-obvious semantics.
Fix: Add Javadoc to all 56 getter/setter methods, especially those with non-obvious field semantics.
[A02-26] LOW | File: ImpactDeptBean.java | Line: 18-40
Description: All 8 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 8 getter/setter methods.
[A02-27] LOW | File: ImpactLocBean.java | Line: 19-46
Description: All 10 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 10 getter/setter methods.
[A02-28] LOW | File: ImpactSummaryBean.java | Line: 16-58
Description: All 14 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 14 getter/setter methods.
[A02-29] LOW | File: LicenseBlackListBean.java | Line: 19-82
Description: All 22 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 22 getter/setter methods.
[A02-30] LOW | File: LockOutBean.java | Line: 19-58
Description: All 14 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 14 getter/setter methods.
[A02-31] LOW | File: MaxHourUsageBean.java | Line: 17-32
Description: All 6 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 6 getter/setter methods.
[A02-32] LOW | File: MenuBean.java | Line: 13-46
Description: All 12 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 12 getter/setter methods.
[A02-33] LOW | File: MymessagesUsersBean.java | Line: 22-67
Description: All 16 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 16 getter/setter methods.
[A02-34] LOW | File: NetworkSettingBean.java | Line: 12-33
Description: All 8 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 8 getter/setter methods.
[A02-35] LOW | File: NotificationSettingsBean.java | Line: 12-45
Description: All 12 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 12 getter/setter methods.
[A02-36] LOW | File: PreCheckBean.java | Line: 40-91
Description: All 20 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 20 getter/setter methods.
[A02-37] LOW | File: PreCheckDriverBean.java | Line: 17-38
Description: All 8 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 8 getter/setter methods.
[A02-38] LOW | File: PreCheckSummaryBean.java | Line: 15-46
Description: All 10 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 10 getter/setter methods.
[A02-39] HIGH | File: ImpactBean.java | Line: 47
Description: Method addImactMap is misspelled (should be addImpactMap); misleading public API identifier that could cause confusion or bugs in callers searching for "Impact" by name.
Fix: Rename method from addImactMap to addImpactMap and update all callers.
[A02-40] INFO | File: MymessagesUsersBean.java | Line: 17,58,61
Description: Field descrption and accessors getDescrption()/setDescrption() are misspelled (missing 'i'; should be "description").
Fix: Rename field and accessors from descrption to description and update all callers.
[A02-41] INFO | File: ImpactDeptBean.java | Line: 14,30,33
Description: Field and accessor arrImpactSummryBean/getArrImpactSummryBean()/setArrImpactSummryBean() are misspelled (should be "Summary" not "Summry").
Fix: Rename field and accessors from Summry to Summary and update all callers.
[A02-42] INFO | File: EntityBean.java | Line: 7-9
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-43] INFO | File: ImpactBean.java | Line: 7-9
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-44] INFO | File: ImpactDeptBean.java | Line: 7-9
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-45] INFO | File: ImpactLocBean.java | Line: 8-10
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-46] INFO | File: LockOutBean.java | Line: 7-9
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-47] INFO | File: MaxHourUsageBean.java | Line: 8-10
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-48] INFO | File: MymessagesUsersBean.java | Line: 7-9
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-49] INFO | File: PreCheckBean.java | Line: 10-12
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-50] INFO | File: PreCheckDriverBean.java | Line: 7-9
Description: Empty block comment above serialVersionUID (IDE-generated placeholder) provides no value.
Fix: Remove the empty block comment or replace with meaningful documentation.
[A02-51] INFO | File: ImpactBean.java | Line: 25
Description: Terse inline comment "//monthly national report" provides minimal context; does not explain what the following arrays represent or their index semantics.
Fix: Expand the comment to describe array purpose and index semantics.
[A02-52] INFO | File: ImpactBean.java | Line: 40-43
Description: Terse section markers "//new monthly report" and "//end" with no explanation of what changed or why a new report format was added.
Fix: Expand the comments to explain the new report format and rationale.
[A02-53] INFO | File: PreCheckBean.java | Line: 22
Description: Terse inline comment "//new Monthly Report" with no explanation of the new fields that follow.
Fix: Expand the comment to describe the new fields and their purpose.

### bean-Q-Z

[QB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/QuestionBean.java | Line: 3
Description: No class-level Javadoc. Purpose of bean (pre-op question configuration?) is unclear from class name alone.
Fix: Add class-level Javadoc explaining the bean represents pre-op question configuration data.
[QB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/QuestionBean.java | Line: 22-125
Description: All 34 getter/setter methods lack Javadoc. Abbreviated field names (exp_ans, crit_ans, questionSpa, questionTha) have no documentation explaining their meaning.
Fix: Add Javadoc to all 34 methods, especially clarifying abbreviations exp_ans, crit_ans, questionSpa, questionTha.
[RAUB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java | Line: 3
Description: No class-level Javadoc. Bean purpose (restricted-access usage tracking/billing) not documented.
Fix: Add class-level Javadoc documenting the bean's role in restricted-access usage tracking and billing.
[RAUB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java | Line: 7-97
Description: All 23 public methods lack Javadoc.
Fix: Add Javadoc to all 23 public methods.
[RAUB-03] INFO | File: WEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java | Line: 8
Description: Stale TODO Auto-generated constructor stub left from IDE scaffolding. Constructor body is empty.
Fix: Remove the stale `// TODO Auto-generated constructor stub` comment.
[SFTP-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SFTPSettings.java | Line: 3
Description: No class-level Javadoc. Bean holds SFTP connection credentials; purpose/usage context not documented.
Fix: Add class-level Javadoc documenting the bean holds SFTP connection credentials and its usage context.
[SFTP-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SFTPSettings.java | Line: 16-57
Description: All 14 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 14 getter/setter methods.
[SDFB-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 29
Description: No class-level Javadoc on a 1003-line class that mixes data-bean responsibilities with database access (JNDI lookup, SQL queries). This is the most complex class in the batch and desperately needs architectural documentation.
Fix: Add comprehensive class-level Javadoc documenting the mixed bean/DAO architecture, JNDI usage, and SQL query responsibilities.
[SDFB-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 104-165
Description: init() -- complex 60-line lifecycle method that performs JNDI lookup, obtains a DB connection, branches on opCode, and handles resource cleanup. Completely undocumented.
Fix: Add Javadoc to init() documenting JNDI lookup, DB connection, opCode branching logic, and resource cleanup.
[SDFB-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 543-561
Description: testQueries(int count) -- public method that runs raw SQL in a loop using hex-incrementing IDs and hardcoded message parameters. No Javadoc explaining purpose, expected inputs, or why test code is in a production bean.
Fix: Add Javadoc explaining purpose and inputs, or remove test code from the production bean.
[SDFB-04] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 886-942
Description: getHrAtLastServ(String, String) -- 56-line public method that opens its own DB connection (separate from init()), runs queries, and converts results. No Javadoc.
Fix: Add Javadoc documenting parameters, return value, and the independent DB connection lifecycle.
[SDFB-05] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 966-999
Description: getDept_prefix(String vcd) -- public method that opens its own DB connection to look up department prefix. No Javadoc.
Fix: Add Javadoc documenting the parameter, return value, and independent DB connection usage.
[SDFB-06] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 106
Description: Comment "// Try connecting the database" is misleading -- init() does far more than just connect; it dispatches to Fetch_service_status_veh(), Fetch_serv_mnt_data(), or testQueries() depending on opCode. The comment obscures this critical branching logic.
Fix: Replace misleading comment with accurate description of the JNDI lookup, connection, opCode dispatch, and cleanup logic.
[SDFB-07] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 90-539
Description: All 93 getter/setter methods (including getStmt()/setStmt() that expose raw Statement objects) lack Javadoc.
Fix: Add Javadoc to all 93 getter/setter methods, especially noting Statement exposure implications.
[SDFB-08] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java | Line: 168-192
Description: clearVariables() has no Javadoc. Clears 17 ArrayLists; purpose and expected lifecycle call-point not documented.
Fix: Add Javadoc documenting purpose, the 17 ArrayLists cleared, and expected lifecycle call-point.
[SCB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java | Line: 5
Description: No class-level Javadoc. Bean likely configures hardware site setup (module type, reader, SIM, timeslots, idle/survey timers) but this is not documented.
Fix: Add class-level Javadoc documenting hardware site configuration purpose and field semantics.
[SCB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java | Line: 32-153
Description: All 40 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 40 getter/setter methods.
[SMB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SpareModuleBean.java | Line: 3
Description: No class-level Javadoc. Bean tracks spare hardware module inventory (swap dates, RA numbers, CCID).
Fix: Add class-level Javadoc documenting spare hardware module inventory tracking purpose.
[SMB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SpareModuleBean.java | Line: 21-116
Description: All 32 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 32 getter/setter methods.
[SAB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SpecialAccessBean.java | Line: 3
Description: No class-level Javadoc. Bean represents special access permissions per user/customer/module but no documentation exists.
Fix: Add class-level Javadoc documenting special access permission mapping per user/customer/module.
[SAB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SpecialAccessBean.java | Line: 14-67
Description: All 18 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 18 getter/setter methods.
[SUB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SubscriptionBean.java | Line: 7
Description: No class-level Javadoc. Bean likely represents email subscription configuration per customer/location/department but this is undocumented.
Fix: Add class-level Javadoc documenting email subscription configuration purpose.
[SUB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SubscriptionBean.java | Line: 21-50
Description: All 10 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 10 getter/setter methods.
[SMAB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java | Line: 3
Description: No class-level Javadoc. Bean relates to super-master authorization (access card auth time windows?) but purpose is undocumented.
Fix: Add class-level Javadoc documenting super-master authorization and access card time window purpose.
[SMAB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java | Line: 7-65
Description: All 15 public methods lack Javadoc.
Fix: Add Javadoc to all 15 public methods.
[SMAB-03] INFO | File: WEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java | Line: 8
Description: Stale TODO Auto-generated constructor stub left from IDE scaffolding. Constructor body is empty.
Fix: Remove the stale `// TODO Auto-generated constructor stub` comment.
[UB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitBean.java | Line: 6
Description: No class-level Javadoc. Core unit/vehicle bean with extensive fields (GMTP ID, CCID, versions, service hours) but no documentation.
Fix: Add class-level Javadoc documenting the core unit/vehicle data model and field semantics.
[UB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitBean.java | Line: 35-162
Description: All 42 getter/setter methods lack Javadoc. Field moderm_version appears to be a typo for "modem_version" but no documentation clarifies intent.
Fix: Add Javadoc to all 42 methods and correct or document the moderm_version typo.
[UUSB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitUtilSummaryBean.java | Line: 5
Description: No class-level Javadoc. Bean summarizes unit utilization (key, seat, track, hydraulic hours with percentages) but no documentation.
Fix: Add class-level Javadoc documenting unit utilization summary purpose and metric types.
[UUSB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitUtilSummaryBean.java | Line: 27-110
Description: All 28 getter/setter methods lack Javadoc. Abbreviation "hydl" (hydraulic?) is not documented.
Fix: Add Javadoc to all 28 methods, clarifying the "hydl" abbreviation.
[UVIB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitVersionInfoBean.java | Line: 3
Description: No class-level Javadoc. Bean tracks firmware/protocol version capabilities (char100Max, char150Max, char150MaxMulti) but meaning of these capability flags is undocumented.
Fix: Add class-level Javadoc documenting firmware version capability flags and their meanings.
[UVIB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitVersionInfoBean.java | Line: 9-32
Description: All 8 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 8 getter/setter methods.
[UUB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java | Line: 7
Description: No class-level Javadoc. Bean holds unit utilization data with complex nested maps (utilMap, impactMap, arrUtil) but data model is completely undocumented.
Fix: Add class-level Javadoc documenting the nested map data model (utilMap, impactMap, arrUtil).
[UUB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java | Line: 35-188
Description: All 38 public methods lack Javadoc. setUtil(int, int) is a non-standard indexed setter with no documentation of the index semantics (the int[8] array maps to 8 unnamed slots).
Fix: Add Javadoc to all 38 methods, especially documenting setUtil(int, int) index semantics for the 8-slot array.
[UUB-03] INFO | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java | Line: 34
Description: Comment "//construction" is trivially obvious, adds no value.
Fix: Remove the trivial `//construction` comment or replace with meaningful constructor documentation.
[UUnitB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnusedUnitBean.java | Line: 5
Description: No class-level Javadoc. Bean represents units identified as unused/inactive but purpose and criteria not documented.
Fix: Add class-level Javadoc documenting unused/inactive unit identification criteria.
[UUnitB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UnusedUnitBean.java | Line: 24-89
Description: All 22 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 22 getter/setter methods.
[UserB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java | Line: 3
Description: No class-level Javadoc. Simple user profile bean.
Fix: Add class-level Javadoc documenting the user profile bean.
[UserB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java | Line: 12-47
Description: All 12 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 12 getter/setter methods.
[UDB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UserDriverBean.java | Line: 3
Description: No class-level Javadoc. Bean links users to drivers, including Wiegand card number (field weigand -- likely misspelled "Wiegand"). Purpose not documented.
Fix: Add class-level Javadoc documenting user-driver linkage and correct or document the "weigand" spelling.
[UDB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UserDriverBean.java | Line: 11-46
Description: All 12 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 12 getter/setter methods.
[UFB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java | Line: 5
Description: No class-level Javadoc. Bean maps user form access rights (view, edit, delete, print) but undocumented. Fields userFomrCd and userFomrName contain typo "Fomr" (should be "Form").
Fix: Add class-level Javadoc and correct or document the "Fomr" typo in field names.
[UFB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java | Line: 15-56
Description: All 14 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 14 getter/setter methods.
[VD-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/VehDiagnostic.java | Line: 3
Description: No class-level Javadoc on a substantial diagnostic bean (46 methods). Contains both "reported" values (from device) and "current" values (from DB config) plus sync flags, but the dual-value/sync-check pattern is not documented anywhere.
Fix: Add class-level Javadoc documenting the dual reported/current value pattern and sync flag semantics.
[VD-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/VehDiagnostic.java | Line: 33-215
Description: All 46 getter/setter methods lack Javadoc. Abbreviations "FSSX", "CRC", "APN" are domain-specific and unexplained.
Fix: Add Javadoc to all 46 methods, defining FSSX, CRC, and APN abbreviations.
[VNSB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/VehNetworkSettingsBean.java | Line: 3
Description: No class-level Javadoc. Bean holds WiFi network settings (SSID, password, country) for vehicle modules but purpose undocumented.
Fix: Add class-level Javadoc documenting WiFi network settings purpose for vehicle modules.
[VNSB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/VehNetworkSettingsBean.java | Line: 5-28
Description: All 8 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 8 getter/setter methods.
[VIB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/VehicleImportBean.java | Line: 3
Description: No class-level Javadoc. Bean used for bulk vehicle import (maps spreadsheet columns to vehicle properties?) but process and expected data format not documented.
Fix: Add class-level Javadoc documenting the bulk vehicle import process and expected data format.
[VIB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/VehicleImportBean.java | Line: 25-139
Description: All 38 getter/setter methods lack Javadoc.
Fix: Add Javadoc to all 38 getter/setter methods.

### master

[DC-DOC-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 30
Description: Missing class Javadoc on Databean_customer, a large data-access bean (~3,009 lines) with no class-level documentation
Fix: Add class-level Javadoc describing purpose, usage, and responsibility of the bean
[DC-DOC-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 331
Description: Missing Javadoc on query(String op_code), the primary entry-point method dispatching to ~25 query methods with no documented valid op_code values
Fix: Add Javadoc listing valid op_code values, side effects, expected state, and @param/@throws tags
[DC-DOC-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 547, 578, 600, 634, 725
Description: Missing Javadoc on public Query methods (Query_Viewable_Battery, Query_Viewable_Settings, Query_Viewable_Reports, Query_Viewable_Menu, Query_User_Form_Menu) that execute complex SQL
Fix: Add Javadoc with @param/@throws tags documenting SQL contracts and populated ArrayLists
[DC-DOC-04] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 804, 871, 957
Description: Missing Javadoc on public data-access methods (queryBlacklist, querySupervisorList, Query_User_Access_Restriction) with access-level branching logic
Fix: Add Javadoc documenting access-level behavior, SQL queries, and side effects
[DC-DOC-05] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 1029, 1163
Description: Missing Javadoc on Query_All_Models_By_Cus_Loc_Dept() and Query_All_Models_By_Cus_Loc_Dept_va() with no documentation explaining difference between variants
Fix: Add Javadoc explaining purpose and distinction between the two variant methods
[DC-DOC-06] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 1246, 1289, 1387, 1430, 1472, 1696, 1713, 1745, 1763, 1792, 1835, 1871, 1937, 1967, 1992, 2028, 2049, 2078, 2327, 2567, 2600, 2960
Description: All 22 remaining public Query/data-access methods lack Javadoc with no @param, @throws, or contract descriptions
Fix: Add Javadoc to each method documenting parameters, SQL operations, populated state, and exceptions
[DC-DOC-07] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 2715-2998
Description: ~80 public getter/setter methods lack Javadoc
Fix: Add minimal Javadoc or use @return/@param tags on each accessor
[DC-DOC-08] INFO | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java | Line: 27
Description: Inline comment "Added by Leslie 11-07-2014" used instead of @author tag
Fix: Replace inline comment with proper @author Javadoc tag in class-level Javadoc
[DG-DOC-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java | Line: 41
Description: Missing class Javadoc on Databean_getter, a large data-access bean (~5,469 lines) with no class-level documentation
Fix: Add class-level Javadoc describing purpose, usage, and responsibility of the bean
[DG-DOC-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java | Line: 474
Description: Missing Javadoc on query(String op_code), the primary entry point (~400 lines) dispatching to 30+ private query methods with no documented operation codes
Fix: Add Javadoc listing valid op_code values, required pre-state, and exceptions
[DG-DOC-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java | Line: 872, 3865, 3948
Description: Missing Javadoc on public Query methods (Query_Vehicle_Diagnostic, Query_Customers_Locations, Query_Departments) with complex SQL and access-level filtering
Fix: Add Javadoc with @param/@throws documenting SQL contracts and filtering logic
[DG-DOC-04] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java | Line: various
Description: ~140 public getter/setter methods lack Javadoc
Fix: Add minimal Javadoc or use @return/@param tags on each accessor
[DG-DOC-05] INFO | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java | Line: 4071, 4080, 4089
Description: Three identical "TODO Auto-generated catch block" comments in empty catch blocks indicate unfinished error handling
Fix: Implement proper error handling or logging in each catch block and remove TODO comments
[DG-DOC-06] INFO | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java | Line: 812
Description: Incorrect error message "Exception in Databean_getuser" in class named Databean_getter -- misleading copy-paste error
Fix: Correct the error message string to reference "Databean_getter" instead of "Databean_getuser"
[DGU-DOC-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java | Line: 28
Description: Missing class Javadoc on Databean_getuser, the largest file in the package (~10,675 lines) with no class-level documentation
Fix: Add class-level Javadoc describing purpose, usage, and responsibility of the bean
[DGU-DOC-02] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java | Line: 461-464
Description: Empty/misleading Javadoc "/** */" on clear_variables() with no description, @param, or @throws; inline comment after signature provides more info than the Javadoc
Fix: Move inline comment content into the Javadoc block and add proper @param/@throws tags
[DGU-DOC-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java | Line: 7880
Description: Missing Javadoc on init(), a critical lifecycle method that sets up database connections and dispatches based on operation codes
Fix: Add Javadoc documenting expected configuration, valid op_codes, and side effects
[DGU-DOC-04] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java | Line: 5383
Description: Missing Javadoc on Query_Current_User(), a complex SQL query method that populates user state
Fix: Add Javadoc documenting SQL operations, populated state fields, and exceptions
[DGU-DOC-05] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java | Line: 5971, 6014, 6026, 9018
Description: Missing Javadoc on public data-access methods (Query_User_Form_Menu, Query_Permits, QueryUnlkSettings, QuerySFTPSettings)
Fix: Add Javadoc with @param/@throws documenting SQL contracts and side effects
[DGU-DOC-06] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java | Line: 3447
Description: Missing Javadoc on convertToArrayString(Object[]), a static utility method with no documented contract
Fix: Add Javadoc with @param/@return tags documenting input expectations and return value
[DGU-DOC-07] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java | Line: various
Description: ~250 public getter/setter methods lack Javadoc
Fix: Add minimal Javadoc or use @return/@param tags on each accessor
[DU-DOC-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_user.java | Line: 29
Description: Missing class Javadoc on Databean_user, an empty/unused shell class (45 lines, no methods) with no documentation explaining its purpose
Fix: Add class-level Javadoc explaining whether the class is intentionally empty or deprecated
[DU-DOC-02] INFO | File: WEB-INF/src/com/torrent/surat/fms6/master/Databean_user.java | Line: 24
Description: Inline comment "Added by Leslie 11-07-2014" used instead of @author tag
Fix: Replace inline comment with proper @author Javadoc tag in class-level Javadoc
[FVB-DOC-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java | Line: 3
Description: Missing class Javadoc on FirmwareverBean, a data bean for firmware version conversion (32-bit and 64-bit hex parsing) with no class documentation
Fix: Add class-level Javadoc describing firmware version parsing purpose and hex format expectations
[FVB-DOC-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java | Line: 38
Description: Missing Javadoc on setCurr_ver(String version) which contains business logic parsing hex firmware versions via convert64bit/convert32bit based on string length
Fix: Add Javadoc documenting hex format expectations, parsing logic, and @param/@throws tags
[FVB-DOC-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java | Line: 211
Description: Missing Javadoc on getType(String version), an overloaded method that parses hex version strings and returns type codes with substring fallback on NumberFormatException
Fix: Add Javadoc documenting hex input format, return value meaning, and exception handling behavior
[FVB-DOC-04] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java | Line: 51, 56
Description: Missing Javadoc on setCurr_ver_edit(String) and setCurr_ver() (no-arg) which bypass parsing logic with undocumented distinction from setCurr_ver(String)
Fix: Add Javadoc explaining how these setters differ from the parsing variant setCurr_ver(String)
[FVB-DOC-05] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java | Line: 14-85, 245-251
Description: 13 simple getter/setter methods lack Javadoc
Fix: Add minimal Javadoc or use @return/@param tags on each accessor
[FSU-DOC-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 35
Description: Missing class Javadoc on Frm_saveuser, the largest servlet in the package (~10,930 lines) implementing SingleThreadModel with no documented purpose or URL mapping
Fix: Add class-level Javadoc describing servlet purpose, URL mapping, and supported op_code values
[FSU-DOC-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 54
Description: Missing Javadoc on doPost(HttpServletRequest, HttpServletResponse), a 393-line method dispatching to ~70 save operations with no documented op_code values
Fix: Add Javadoc listing valid op_code parameter values and @param/@throws tags
[FSU-DOC-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 5199
Description: Missing Javadoc on isValidEmailAddress(String email), a utility method validating email via regex
Fix: Add Javadoc with @param/@return tags documenting validation rules and return value
[FSU-DOC-04] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java | Line: 449
Description: Missing Javadoc on clearVectors() which has an empty method body with no documentation on why it exists
Fix: Add Javadoc explaining whether this is intentionally a no-op or pending implementation
[FU-DOC-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java | Line: 26
Description: Missing class Javadoc on Frm_upload, a file-upload servlet with no documentation on what it uploads, security considerations, or file-size limits
Fix: Add class-level Javadoc describing upload purpose, accepted file types, size limits, and security
[FU-DOC-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java | Line: 46
Description: Missing Javadoc on init(), a servlet lifecycle method that establishes database connections
Fix: Add Javadoc with @throws documenting database connection setup and failure modes
[FU-DOC-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java | Line: 69
Description: Missing Javadoc on doPost(HttpServletRequest, HttpServletResponse) which handles multipart file upload and database operations
Fix: Add Javadoc with @param/@throws documenting multipart handling, file storage, and DB operations
[FU-DOC-04] LOW | File: WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java | Line: 102
Description: Missing Javadoc on clearVectors() which has an empty method body with no documentation
Fix: Add Javadoc explaining whether this is intentionally a no-op or pending implementation

### dashboard

[1] MEDIUM | File: Config.java | Line: Class level
Description: No class-level Javadoc for shared utility class serving dashboard servlets; role, thread-safety of static cusList, and servlet relationship undocumented
Fix: Add class-level Javadoc describing purpose, thread-safety considerations, and relationship to dashboard servlets
[2] MEDIUM | File: Config.java | Line: getCustomers()
Description: Public method getCustomers(HttpServletRequest, HttpServletResponse) undocumented; no @param, @return, @throws tags
Fix: Add Javadoc with @param, @return, @throws documenting customer master data query, JSON response, and session attributes used
[3] MEDIUM | File: Config.java | Line: getSites()
Description: Public method getSites() undocumented; filters cached cusList by cust_cd parameter, returns JSON list of sites
Fix: Add Javadoc with @param and @return documenting site filtering and JSON response
[4] MEDIUM | File: Config.java | Line: getDepartments()
Description: Public method getDepartments() undocumented; filters cached cusList by loc_cd parameter, returns JSON list of departments
Fix: Add Javadoc with @param and @return documenting department filtering and JSON response
[5] MEDIUM | File: Config.java | Line: saveasList()
Description: Public method saveasList(String) undocumented; executes arbitrary SQL via JNDI lookup with no documentation on query format or error handling
Fix: Add Javadoc with @param, @return, @throws documenting SQL execution, JNDI lookup, and expected query format
[6] MEDIUM | File: Config.java | Line: getPermision()
Description: Public method getPermision() undocumented; queries form permissions for current user session, returns JSON array of form names
Fix: Add Javadoc with @param and @return documenting session-based permission query and JSON response format
[7] LOW | File: Config.java | Line: addSeries() (2-param overload)
Description: Public utility method addSeries(List, String, List) undocumented; builds chart series data structures
Fix: Add Javadoc with @param tags documenting series building parameters
[8] LOW | File: Config.java | Line: addSeries() (3-param overload)
Description: Public utility method addSeries(List, String, String, List) undocumented; overload with color parameter
Fix: Add Javadoc with @param tags documenting series building parameters including color
[9] MEDIUM | File: CriticalBattery.java | Line: Class level
Description: No class-level Javadoc for servlet handling critical battery level data; URL, purpose, parameter contract, and response format undocumented
Fix: Add class-level Javadoc documenting servlet URL /Servlet/CriticalBatteryServlet, part parameter values, and JSON response format
[10] MEDIUM | File: CriticalBattery.java | Line: doGet()
Description: No Javadoc on doGet(); dispatches on part parameter to multiple sub-handlers with no documentation of valid part values
Fix: Add Javadoc documenting part parameter values (dates, table, update, cust, site, dept, permision) and response contract
[11] MEDIUM | File: CriticalBattery.java | Line: cleanupSession()
Description: Public static method cleanupSession(String) undocumented; clears session-specific ConcurrentHashMap entries to prevent memory leaks
Fix: Add Javadoc with @param documenting session ID parameter and cleanup behavior
[12] MEDIUM | File: Impacts.java | Line: Class level
Description: No meaningful class-level Javadoc; empty /** * */ block on serialVersionUID field, not the class; servlet purpose undocumented
Fix: Add class-level Javadoc documenting servlet URL /Servlet/ImpactsServlet, impact/shock data purpose, and parameter contract
[13] MEDIUM | File: Impacts.java | Line: doGet()
Description: No Javadoc on doGet(); dispatches on part parameter with 9 different values including pie and average, none documented
Fix: Add Javadoc documenting all 9 part parameter values and their response formats
[14] MEDIUM | File: Impacts.java | Line: cleanupSession()
Description: Public static method cleanupSession(String) undocumented
Fix: Add Javadoc with @param documenting session ID parameter and cleanup behavior
[15] MEDIUM | File: Licence.java | Line: Class level
Description: No class-level Javadoc; servlet manages driver licence expiry dashboard data with AU-specific logic via LindeConfig.siteName branching
Fix: Add class-level Javadoc documenting servlet URL /Servlet/LicenceServlet, purpose, parameters, and AU vs non-AU behavior
[16] MEDIUM | File: Licence.java | Line: init()
Description: Overridden servlet lifecycle method init() undocumented; loads customer-department-location data into cusList at startup
Fix: Add Javadoc documenting initialization of cusList data and startup behavior
[17] MEDIUM | File: Licence.java | Line: doGet()
Description: No Javadoc on doGet(); dispatches on part parameter with 3 possible values
Fix: Add Javadoc documenting part parameter values (chart, table, update) and response contract
[18] MEDIUM | File: Licence.java | Line: cleanupSession()
Description: Public static method cleanupSession(String) undocumented
Fix: Add Javadoc with @param documenting session ID parameter and cleanup behavior
[19] MEDIUM | File: Preop.java | Line: Class level
Description: No class-level Javadoc; servlet handles pre-operation check data (checklists, pass/fail/incomplete) with no documentation
Fix: Add class-level Javadoc documenting servlet URL /Servlet/PreopServlet, purpose, and parameter contract
[20] MEDIUM | File: Preop.java | Line: doGet()
Description: No Javadoc on doGet(); dispatches on part parameter with 7 possible values
Fix: Add Javadoc documenting part parameter values (dates, table, update, cust, site, dept, permision) and response contract
[21] MEDIUM | File: Preop.java | Line: cleanupSession()
Description: Public static method cleanupSession(String) undocumented
Fix: Add Javadoc with @param documenting session ID parameter and cleanup behavior
[22] LOW | File: SessionCleanupListener.java | Line: Class-level Javadoc
Description: Minimal one-line class Javadoc missing @author tag and does not document which servlets it cleans up or registration mechanism
Fix: Expand class Javadoc to include @author, list of servlets cleaned up, and @WebListener registration details
[23] HIGH | File: SessionCleanupListener.java | Line: sessionDestroyed() line 26
Description: Misleading documentation by omission; only calls Impacts.cleanupSession() but not CriticalBattery, Preop, Utilisation, or Licence cleanup methods, masking a memory leak
Fix: Add cleanupSession() calls for CriticalBattery, Preop, Utilisation, and Licence in sessionDestroyed(), and update comments to reflect all servlets
[24] LOW | File: SessionCleanupListener.java | Line: sessionCreated()
Description: Inline comment says "Nothing needed here" which is adequate for a no-op but minimal
Fix: No action required; adequate for a no-op method
[25] MEDIUM | File: Summary.java | Line: Class level
Description: No class-level Javadoc; main summary/overview dashboard servlet with 11 part values and most complex dispatch in the package
Fix: Add class-level Javadoc documenting servlet URL /Servlet/SummaryServlet, purpose, all 11 part values, and aggregated sub-views
[26] MEDIUM | File: Summary.java | Line: doGet()
Description: No Javadoc on doGet(); complex dispatch with 11 cases covering drivers, units, impacts, licences, utilisation, preop, and battery
Fix: Add Javadoc documenting all 11 part parameter values and their response formats
[27] MEDIUM | File: Summary.java | Line: getBattery()
Description: Private but complex business logic method undocumented; queries voltage data over 12 hourly intervals with cust_cd, loc_cd, dept_cd, to_dt parameters
Fix: Add Javadoc documenting request parameters, 12-interval query logic, and JSON response structure with categories and series
[28] MEDIUM | File: Summary.java | Line: getImpact()
Description: Private but complex business logic method undocumented; runs 4 separate queries for red impacts (today, yesterday, 7-day, 28-day)
Fix: Add Javadoc documenting the 4 query periods and response structure
[29] MEDIUM | File: Summary.java | Line: getUnit()
Description: Private but complex method undocumented; queries units, inactive-72h, active, VOR, abuse counts with realtime parameter branching
Fix: Add Javadoc documenting unit count queries, realtime parameter behavior, and response structure
[30] MEDIUM | File: Summary.java | Line: getDriver()
Description: Private but complex method undocumented; queries driver counts, expired licences, no-licence, inactive drivers with AU-specific branching
Fix: Add Javadoc documenting driver queries, AU-specific logic, and response structure
[31] INFO | File: Summary.java | Line: 633
Description: TODO marker "//to-do: only for demo" with placeholder code that sets abuse to "0" in both branches of a conditional, never implemented
Fix: Implement actual abuse count logic or remove the dead conditional and TODO marker
[32] MEDIUM | File: TableServlet.java | Line: Class level
Description: No class-level Javadoc; servlet provides detailed table data for units, drivers, preop checklists, and VOR status
Fix: Add class-level Javadoc documenting servlet URL /Servlet/TableServlet, purpose, parameters, and response format
[33] MEDIUM | File: TableServlet.java | Line: doGet()
Description: No Javadoc on doGet(); dispatches on part parameter with 7 possible values
Fix: Add Javadoc documenting part parameter values (detail_unit, detail_driver, preop, vor_status, cust, site, dept) and response contract
[34] MEDIUM | File: TableServlet.java | Line: saveasList()
Description: Public static method saveasList(String, String) undocumented; similar to Config.saveasList() but with servlet name parameter for error logging
Fix: Add Javadoc with @param and @return documenting SQL execution, servlet parameter for logging, and return type
[35] INFO | File: TableServlet.java | Line: 38
Description: Instance field servlet set to "/Servlet/UtilisationServlet" is a copy-paste artifact; actual servlet is /Servlet/TableServlet, causing misleading error logs
Fix: Change servlet field value to "/Servlet/TableServlet" to match the actual servlet mapping
[36] MEDIUM | File: Utilisation.java | Line: Class level
Description: No class-level Javadoc; most complex servlet with 18 part values covering model/date/location views, tables, charts, pie, and averages; threshold logic undocumented
Fix: Add class-level Javadoc documenting servlet URL /Servlet/UtilisationServlet, all 18 part values, and thresholdLow/thresholdHigh band meanings
[37] LOW | File: Utilisation.java | Line: cleanupSession()
Description: Public static method cleanupSession(String) undocumented; same pattern as other servlets
Fix: Add Javadoc with @param documenting session ID parameter and cleanup behavior
[38] LOW | File: Utilisation.java | Line: serialVersionUID
Description: Field serialVersionUID is static final but package-private visibility instead of private; minor documentation/style note
Fix: Change serialVersionUID access modifier to private

### chart

[1] MEDIUM | File: BarChartCategory.java | Line: 8
Description: Missing class-level Javadoc on non-trivial chart class
Fix: Add class-level Javadoc describing daily usage bar chart generation by hour period
[2] LOW | File: BarChartCategory.java | Line: 32-41
Description: Missing Javadoc on constructor
Fix: Add Javadoc to constructor documenting data, y-axis labels, and total parameters
[3] MEDIUM | File: BarChartCategory.java | Line: 58-128
Description: Missing Javadoc on complex createChart() method (70 lines, markers, scaling)
Fix: Add Javadoc documenting return value semantics, side effects, and chart URL generation logic
[4] LOW | File: BarChartCategory.java | Line: 16-30
Description: Missing Javadoc on getters/setters (getTotal, setTotal, getyAxisLabel, setyAxisLabel)
Fix: Add Javadoc to getTotal(), setTotal(int), getyAxisLabel(), setyAxisLabel(ArrayList)
[5] LOW | File: BarChartCategory.java | Line: 43-56
Description: Missing Javadoc on getData, setData, setyAxis
Fix: Add Javadoc to getData(), setData(ArrayList), and setyAxis() methods
[6] MEDIUM | File: BarChartImpactCategory.java | Line: 20
Description: Missing class-level Javadoc; Blue/Amber/Red categorization undocumented
Fix: Add class-level Javadoc explaining impact breakdown chart and Blue/Amber/Red categories
[7] LOW | File: BarChartImpactCategory.java | Line: 40-49
Description: Missing Javadoc on constructor
Fix: Add Javadoc to constructor documenting data parameter
[8] MEDIUM | File: BarChartImpactCategory.java | Line: 71-120
Description: Missing Javadoc on createChart() with non-obvious blue-skip filtering
Fix: Add Javadoc documenting the blue category filtering logic at line 79
[9] INFO | File: BarChartImpactCategory.java | Line: 51-55
Description: Missing Javadoc on addColors() override
Fix: Add Javadoc explaining override behavior with Blue/Orange/Red colors
[10] LOW | File: BarChartNational.java | Line: 21
Description: Missing class-level Javadoc
Fix: Add class-level Javadoc describing national utilisation bar chart
[11] LOW | File: BarChartNational.java | Line: 33-39
Description: Missing Javadoc on constructor
Fix: Add Javadoc to constructor documenting EntityBean list parameter
[12] LOW | File: BarChartNational.java | Line: 56-103
Description: Missing Javadoc on createChart()
Fix: Add Javadoc to createChart() method
[13] LOW | File: BarChartR.java | Line: 8
Description: Missing class-level Javadoc
Fix: Add class-level Javadoc describing stacked bar chart for driver data over time
[14] LOW | File: BarChartR.java | Line: 23-29
Description: Missing Javadoc on constructor (does not set report title)
Fix: Add Javadoc noting constructor does not set report title, defaults to "Unknown Report"
[15] LOW | File: BarChartR.java | Line: 46-94
Description: Missing Javadoc on createChart()
Fix: Add Javadoc to createChart() method
[16] LOW | File: BarChartUtil.java | Line: 19
Description: Missing class-level Javadoc
Fix: Add class-level Javadoc describing usage bar chart by 3-hour intervals
[17] INFO | File: BarChartUtil.java | Line: 36-52
Description: Missing Javadoc on two overloaded constructors
Fix: Add Javadoc to both constructor overloads documenting their parameters
[18] INFO | File: BarChartUtil.java | Line: 69-108
Description: Missing Javadoc on createChart()
Fix: Add Javadoc to createChart() method
[19] INFO | File: BarChartUtil_bak.java | Line: 10
Description: Missing class-level Javadoc; _bak file status (deprecated?) undocumented
Fix: Add class-level Javadoc indicating backup/deprecated status and relationship to BarChartNational
[20] MEDIUM | File: Chart.java | Line: 8
Description: Missing class-level Javadoc on base class of entire chart hierarchy
Fix: Add class-level Javadoc documenting role, subclassing pattern, and charts4j dependency
[21] HIGH | File: Chart.java | Line: 15-39
Description: Missing Javadoc on core algorithm caculateyAxis(double) used by 7+ subclasses; name misspelled; parameter shadows field
Fix: Add Javadoc documenting rounding algorithm, edge cases, parameter/return semantics; note misspelled name
[22] INFO | File: Chart.java | Line: 50-53
Description: Missing Javadoc on base createChart() (override contract undocumented)
Fix: Add Javadoc documenting that subclasses are expected to override this method
[23] INFO | File: Chart.java | Line: 63-77
Description: Missing Javadoc on addColors() (override contract undocumented)
Fix: Add Javadoc documenting default 13-color palette and that subclasses may override
[24] INFO | File: JfreeGroupStackChart.java | Line: 32
Description: Missing class-level Javadoc on apparent demo/prototype class
Fix: Add class-level Javadoc indicating demo/prototype status and whether class is in active use
[25] HIGH | File: JfreeGroupStackChart.java | Line: 34-38
Description: Misleading Javadoc: documents @param title but constructor takes no parameters
Fix: Remove or correct the @param title tag to match the no-arg constructor signature
[26] INFO | File: JfreeGroupStackChart.java | Line: 185-188
Description: Javadoc on createLegendItems() says "subset" but returns empty collection
Fix: Correct Javadoc to reflect that the method returns an empty legend item collection
[27] HIGH | File: StackedBarChart.java | Line: 31-36
Description: Misleading class-level Javadoc: says "dummy data not real data" but class processes production data
Fix: Update class-level Javadoc to reflect that class processes real production data from constructor parameter
[28] INFO | File: StackedBarChart.java | Line: 47-51
Description: Orphaned/misplaced constructor Javadoc with misspelled @param titel; separated from actual constructor by field declarations
Fix: Move Javadoc block to directly precede constructor at line 59; fix @param titel to @param title; document all 4 parameters
[29] INFO | File: StackedBarChart.java | Line: 212-217
Description: createDataset() Javadoc says "database with JDBC" but data comes from in-memory ArrayList
Fix: Update Javadoc to state data comes from in-memory ArrayList passed to constructor
[30] MEDIUM | File: StackedBarChart.java | Line: 286-300
Description: Missing Javadoc on public saveChart(String) which performs file I/O
Fix: Add Javadoc documenting file I/O side effects, directory expectations, and return value (absolute path)

### chart-excel

[A06-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/*.java | Line: all classes
Description: Not a single file in the chart/excel package (20 classes) has a class-level Javadoc comment
Fix: Add class-level Javadoc to all 20 files, prioritizing ChartDashboardUtil, ChartsExcelDao, and Chart subclasses
[A06-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/*.java | Line: all methods
Description: All ~176 public methods across 20 files lack Javadoc comments with @param, @return, or @throws tags
Fix: Add Javadoc to all non-trivial business methods; bean getters/setters are lower priority
[A06-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java | Line: 404,552,693,970,1494,207,849
Description: 17 public DAO methods (30-350 lines each) with complex SQL and business logic have zero documentation
Fix: Add Javadoc documenting retrieved data, parameter meanings, returned list structure, and SQLException
[A06-04] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java | Line: 70,695
Description: 1490-line class with 29 public methods, none documented; createTestChart is 616 lines with undocumented int-to-chart mapping
Fix: Add Javadoc to createTestChart, createExcel, createBarChart; document chart type integer mapping (1-9)
[A06-05] HIGH | File: BatteryChargeChart.java:71,127; DriverAccessAbuseChart.java:71,127; DriverActivityChart.java:69,113; ExpiryChart.java:69,113; ImpactChart.java:69,113; MachineUnlockChart.java:69,113; PreopFailChart.java:69,113; UserLoginChart.java:71,127 | Line: see files
Description: Eight chart classes contain "EXAMPLE CODE START/END" comments bracketing production createChart() methods, copy-pasted from charts4j tutorial
Fix: Remove all "EXAMPLE CODE START", "EXAMPLE CODE END", and "Use this url string" comments from all 8 files
[A06-06] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/PreopFailChart.java | Line: 78,86
Description: PreopFailChart legend says "Unlocks" and axis labels say "Question","Impact" -- copy-pasted from MachineUnlockChart without updating
Fix: Change legend label to "Incorrect" or "Pre-op Failures" and update axis labels to reflect pre-op check categories
[A06-07] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java | Line: 92,680,735
Description: Production code paths marked with "FOR TESTING ONLY" and "for testing purposes only" comments are misleading
Fix: Remove test code paths if unused in production, or update comments to describe conditional behavior accurately
[A06-08] INFO | File: PreopFailBean.java:9; UnitUtilBean.java:9; UnlockBean.java:9 | Line: 9
Description: Three bean classes retain IDE-generated "TODO Auto-generated constructor stub" comments in empty constructors
Fix: Remove the "// TODO Auto-generated constructor stub" comments from all three files
[A06-09] LOW | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboardUtil.java | Line: 89,853,864,875,885,895,905,915,925,936,358,649,1045-1046,1068
Description: Numerous commented-out System.out.println statements and dead code blocks obscure actual logic
Fix: Remove all commented-out System.out.println statements and dead code; use a proper logging framework
[A06-10] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java | Line: 133,145,164
Description: getAllLocations(String custCd) uses custCd as USER_CD in SQL; line 164 has impossible condition (length < 0)
Fix: Add Javadoc clarifying parameter semantics, fix bug on line 164 (should be > 0 not < 0), consider renaming parameter
[A06-11] INFO | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java | Line: 32,180
Description: getFromDate() and getCurrDate() declare unused ArrayList<EntityBean> arrDept, misleadingly suggesting department involvement
Fix: Remove the unused arrDept variable declarations from both methods
[A06-12] INFO | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java | Line: 412,560,701
Description: All three getUnitUtilisationByHour overloads declare unused ArrayList<ImpactBean> arrImpactData
Fix: Remove the unused arrImpactData variable from all three overloads
[A06-13] LOW | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartDashboard.java | Line: 5
Description: Completely empty class (only empty constructor) with no documentation explaining if placeholder, deprecated, or future use
Fix: Document the intended purpose of this class or remove it if unused
[A06-14] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/chart/excel/ImpactChart.java:86; ChartDashboardUtil.java:1074 | Line: 86,1049,1074,1068
Description: ImpactChart has 2 axis labels ("Amber","Red") but dept-filtered overload passes 3-element array {blue,amber,red} with blue always 0
Fix: Remove blue element from dept-filtered overload data array, or uncomment blue accumulation and add third axis label

### excel-frm

[DOC-001] HIGH | File: Frm_excel.java | Line: 191-197
Description: Misleading Javadoc on createExcel() reads "Creates a PDF with information about the movies" with wrong @param and @throws -- method actually creates an Excel workbook, has no filename parameter, and never throws DocumentException
Fix: Replace Javadoc with accurate description of Excel workbook creation, correct parameters, and actual exceptions thrown
[DOC-002] HIGH | File: Frm_Linde_Reports.java | Line: 1415
Description: Misleading inline legend text states "Green: Average Time is less than 00:00:45" but code logic at lines 1336-1342 applies green when ave >= 45 (greater than or equal to, not less than)
Fix: Change legend text to "Green: Average Time is greater than or equal to 00:00:45" to match actual code logic
[DOC-003] MEDIUM | File: Frm_excel.java | Line: 303
Description: Inaccurate inline comment "//doesn't work" on setFoot() with no explanation of why it fails, whether it is dead code, or intended behavior
Fix: Either remove dead code or replace comment with explanation of the known issue and intended fix
[DOC-004] MEDIUM | File: Frm_excel.java | Line: 49
Description: No class-level Javadoc on the base class that is the foundation of the entire Excel report hierarchy with 9 subclasses
Fix: Add class-level Javadoc describing purpose, field semantics, lifecycle, and extension contract
[DOC-005] MEDIUM | File: Frm_Linde_Reports.java | Line: 26
Description: No class-level Javadoc on complex 2381-line class generating 15+ different Linde/Americold report types via opCode dispatch
Fix: Add class-level Javadoc documenting supported report types, opCode dispatch pattern, and usage
[DOC-006] MEDIUM | File: Frm_national_rpt.java | Line: 30
Description: No class-level Javadoc on 1210-line class producing national-level multi-tab report (preop, impact, unlock, utilisation)
Fix: Add class-level Javadoc describing report structure and data dependencies
[DOC-007] MEDIUM | File: Frm_quater_rpt.java | Line: 30
Description: No class-level Javadoc on 876-line class producing quarterly/monthly report; class name is also misspelled ("quater" vs "quarter")
Fix: Add class-level Javadoc and consider renaming class to Frm_quarter_rpt
[DOC-008] MEDIUM | File: Frm_month_rpt.java | Line: 27
Description: No class-level Javadoc on 765-line class producing monthly cover page, impact, and utilisation reports
Fix: Add class-level Javadoc describing report tabs and generation workflow
[DOC-009] LOW | File: Frm_MaxHourUsage.java | Line: 18
Description: No class-level Javadoc
Fix: Add class-level Javadoc describing purpose and usage
[DOC-010] LOW | File: Frm_inaUnit_rpt.java | Line: 17
Description: No class-level Javadoc
Fix: Add class-level Javadoc describing purpose and usage
[DOC-011] LOW | File: Frm_unitSummary_rpt.java | Line: 16
Description: No class-level Javadoc
Fix: Add class-level Javadoc describing purpose and usage
[DOC-012] LOW | File: Frm_simSwap_rpt.java | Line: 15
Description: No class-level Javadoc
Fix: Add class-level Javadoc describing purpose and usage
[DOC-013] LOW | File: Frm_nz_unitSummary_rpt.java | Line: 16
Description: No class-level Javadoc
Fix: Add class-level Javadoc describing purpose and usage
[DOC-014] MEDIUM | File: Frm_Linde_Reports.java | Line: 50
Description: Massive 240-line dispatcher method createExcel(String opCode) handling 18 distinct opCode values with no documentation of accepted opCodes, return semantics, or side effects
Fix: Add Javadoc listing all valid opCode values, return value semantics, and side effects
[DOC-015] MEDIUM | File: Frm_Linde_Reports.java | Line: 2335
Description: generateChart(String rpt_name) spawns an external PhantomJS process with hardcoded OS-specific paths and no documentation of expected environment, file output locations, or failure modes
Fix: Add Javadoc documenting PhantomJS dependency, expected environment setup, output file locations, and error handling
[DOC-016] MEDIUM | File: Frm_excel.java | Line: 151
Description: setParameters(boolean isConf) parses params array and initializes UtilBean but parameter isConf is accepted and never used in the method body
Fix: Add Javadoc explaining method purpose and either document or remove the unused isConf parameter
[DOC-017] MEDIUM | File: Frm_excel.java | Line: 198
Description: Base createExcel() implementation creating a single "Monthly Report" sheet, overridden in every subclass, with existing Javadoc that is misleading (see DOC-001)
Fix: Replace misleading Javadoc with accurate description of base behavior and override contract
[DOC-018] MEDIUM | File: Frm_excel.java | Line: 217
Description: createEmail() has identical implementation to createExcel() with no documentation explaining why two identical methods exist or how they should differ
Fix: Add Javadoc explaining the distinct purpose of createEmail() vs createExcel() or consolidate if truly redundant
[DOC-019] MEDIUM | File: Frm_excel.java | Line: 228
Description: createBody() has identical implementation to createExcel() and createEmail() with no documentation of purpose
Fix: Add Javadoc explaining the distinct purpose of createBody() or consolidate if truly redundant
[DOC-020] MEDIUM | File: Frm_national_rpt.java | Line: 38
Description: createExcel() generates 7 Excel tabs with no documentation of report structure or data dependencies
Fix: Add Javadoc listing generated tabs, data sources, and dependencies
[DOC-021] MEDIUM | File: Frm_quater_rpt.java | Line: 46
Description: createExcel() generates 5 tabs (preop, impact, utilisation) with no documentation
Fix: Add Javadoc listing generated tabs and report structure
[DOC-022] MEDIUM | File: Frm_month_rpt.java | Line: 34
Description: createExcel() generates 5 tabs (cover, impacts, utilisation) with no documentation
Fix: Add Javadoc listing generated tabs and report structure
[DOC-023] MEDIUM | File: Frm_MaxHourUsage.java | Line: 32
Description: createExcel() dispatches between single-dept and group utilisation with no documentation
Fix: Add Javadoc explaining dispatch logic and report output
[DOC-024] MEDIUM | File: Frm_inaUnit_rpt.java | Line: 33
Description: createExcel() generates inactive unit report with configurable day thresholds and no documentation
Fix: Add Javadoc explaining day threshold configuration and report output
[DOC-025] MEDIUM | File: Frm_excel.java | Line: 174
Description: getParam(String key) searches a string array for key=value pairs with non-obvious format contract and no documentation
Fix: Add Javadoc documenting expected key=value format, search behavior, and return value when key is not found
[DOC-026] MEDIUM | File: Frm_excel.java | Line: 925
Description: setTotalDuration() has a 10000-hour threshold that silently changes behavior (skips formula for large values) with no documentation of this edge case
Fix: Add Javadoc documenting the 10000-hour threshold behavior and rationale
[DOC-027] LOW | File: Frm_excel.java | Line: 70-147
Description: None of the 9 overloaded constructors have Javadoc explaining which parameters are for which use case
Fix: Add Javadoc to each constructor explaining its specific use case and parameter semantics
[DOC-028] LOW | File: Frm_excel.java | Line: 209, 213
Description: init() and init2() are empty hook methods with no documentation of intended override purpose
Fix: Add Javadoc explaining these are template method hooks and when subclasses should override them
[DOC-029] LOW | File: Frm_excel.java | Line: 239
Description: getBody() returns empty string with no explanation of purpose or override expectation
Fix: Add Javadoc explaining purpose and expected override behavior
[DOC-030] LOW | File: Frm_excel.java | Line: 1096
Description: getCust_prefix(String cust_cd) has empty method body and appears to be dead code with no documentation
Fix: Remove dead code or add Javadoc explaining intended purpose and implement the method
[DOC-031] LOW | File: Frm_excel.java | Line: 1100-1160
Description: 16 getter/setter methods with no Javadoc
Fix: Add Javadoc to each accessor describing the field purpose
[DOC-032] LOW | File: Frm_Linde_Reports.java | Line: 346, 2373, 2377
Description: setImageDir(), setParams(), setDataArray() simple setters with no Javadoc
Fix: Add Javadoc describing expected values and usage context
[DOC-033] LOW | File: Frm_inaUnit_rpt.java | Line: 215, 219, 223
Description: getDays(), setDays(), addDays() simple accessors with no Javadoc
Fix: Add Javadoc describing the days collection purpose and semantics
[DOC-034] LOW | File: Frm_quater_rpt.java | Line: 797
Description: getExportDir() computes export directory path with hardcoded path traversal and no documentation
Fix: Add Javadoc documenting the computed path structure and dependencies
[DOC-035] LOW | File: Frm_nz_unitSummary_rpt.java | Line: 25
Description: createExcel() generates NZ unit summary report with no documentation
Fix: Add Javadoc describing report output and data sources
[DOC-036] LOW | File: Frm_simSwap_rpt.java | Line: 24
Description: createExcel() generates SIM swap report with no documentation
Fix: Add Javadoc describing report output and data sources
[DOC-037] LOW | File: Frm_unitSummary_rpt.java | Line: 25
Description: createExcel() generates unit summary report with no documentation
Fix: Add Javadoc describing report output and data sources
[DOC-038] INFO | File: Frm_Linde_Reports.java | Line: 47
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up
Fix: Remove the auto-generated TODO comment
[DOC-039] INFO | File: Frm_MaxHourUsage.java | Line: 22, 28
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up (2 occurrences)
Fix: Remove the auto-generated TODO comments
[DOC-040] MEDIUM | File: Frm_MaxHourUsage.java | Line: 78, 156
Description: TODO "needs to resize images" indicates known incomplete feature -- images may render incorrectly in output, present in both createUtilisationChart() and createGroupUtilisationChart()
Fix: Implement image resizing or document the limitation and create a tracking ticket
[DOC-041] INFO | File: Frm_MaxHourUsage.java | Line: 85, 163
Description: "// TODO Auto-generated catch block" with exception silently swallowed via e.printStackTrace() only, present in both private methods
Fix: Replace with proper exception handling or logging and remove TODO comment
[DOC-042] INFO | File: Frm_inaUnit_rpt.java | Line: 22, 30
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up (2 occurrences)
Fix: Remove the auto-generated TODO comments
[DOC-043] INFO | File: Frm_month_rpt.java | Line: 31
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up
Fix: Remove the auto-generated TODO comment
[DOC-044] INFO | File: Frm_national_rpt.java | Line: 34
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up
Fix: Remove the auto-generated TODO comment
[DOC-045] INFO | File: Frm_quater_rpt.java | Line: 36, 43
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up (2 occurrences)
Fix: Remove the auto-generated TODO comments
[DOC-046] INFO | File: Frm_simSwap_rpt.java | Line: 20
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up
Fix: Remove the auto-generated TODO comment
[DOC-047] INFO | File: Frm_unitSummary_rpt.java | Line: 21
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up
Fix: Remove the auto-generated TODO comment
[DOC-048] INFO | File: Frm_nz_unitSummary_rpt.java | Line: 21
Description: IDE-generated placeholder "// TODO Auto-generated constructor stub" not cleaned up
Fix: Remove the auto-generated TODO comment
[DOC-049] MEDIUM | File: Frm_month_rpt.java | Line: 500
Description: Typo in report title string "Unit Utilisation Reort" should be "Unit Utilisation Report" -- visible to end users in generated Excel output
Fix: Change "Reort" to "Report" in the title string
[DOC-050] LOW | File: Frm_unitSummary_rpt.java | Line: 124
Description: Typo in column header "Moderm Version" should be "Modem Version" -- visible to end users in generated Excel output
Fix: Change "Moderm" to "Modem" in the column header string
[DOC-051] INFO | File: Frm_quater_rpt.java | Line: 30
Description: Class name Frm_quater_rpt is misspelled -- should be "quarter", propagates into filenames and all references
Fix: Rename class to Frm_quarter_rpt and update all references

### misc-small-packages

[A04-1] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java | Line: 306, 433, 622, 762, 995, 1095, 1224
Description: Misleading `methodName` assignments in multiple methods point to wrong or non-existent method names, producing incorrect diagnostic output
Fix: Update each `methodName` assignment to match the containing method name (e.g., line 306 change to `"fetchUtilImpactByUnit()"`, line 433 to `"fetchUtilImpactByType()"`, etc.)
[A04-2] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java | Line: 95
Description: Exception handler prints `"Exception in LindeReportsBean"` but the class is `BusinessInsightBean`, misleading production debugging
Fix: Change the exception message from `"Exception in LindeReportsBean"` to `"Exception in BusinessInsightBean"`
[A04-3] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java | Line: 1334-1337
Description: Inline comment on `convert_time1` states it returns "HH:MM:SS format" but method actually returns decimal hours (e.g., `"1.50"`)
Fix: Update the comment to state it returns decimal hours formatted as `#0.00`
[A04-4] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/PreOpQuestions.java | Line: 11-16
Description: Constructor Javadoc `@param` tags are in wrong order (`utcTimestamp, questions, randomiseOrder`) vs actual signature order, and all descriptions are empty
Fix: Reorder `@param` tags to match signature (`utcTimestamp, randomiseOrder, questions`) and add meaningful descriptions
[A04-5] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/jsonbinding/preop/Question.java | Line: 13-22
Description: Constructor Javadoc `@param` tags are in wrong order (`excludeRandom, critical, spa, index, id, tha, eng`) vs actual signature order, and all descriptions are empty
Fix: Reorder `@param` tags to match signature (`index, id, critical, excludeRandom, eng, spa, tha`) and add meaningful descriptions
[A04-6] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightBean.java | Line: 51, 180, 305, 432, 568, 621, 688, 761, 858, 994, 1094, 1223, 1347
Description: 26 public methods have no Javadoc; the 12 `fetch*()` methods and `init()` contain complex SQL and business logic with undocumented purpose, parameters, and data formats
Fix: Add Javadoc to each public method documenting its report type, parameters, data written to `dataArray`, and any SQL logic
[A04-7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java | Line: 23, 41
Description: Servlet class and `doPost` method lack Javadoc explaining URL mapping, expected request parameters (`email`, `customer`, `location`, etc.), or JSON response format
Fix: Add class-level Javadoc with URL mapping and purpose, and method-level Javadoc to `doPost` documenting request parameters and response format
[A04-8] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsightExcel.java | Line: 28
Description: `createExcel(String opCode)` dispatches to 10 report types but has no documentation of valid `opCode` values, return value semantics, or exceptions
Fix: Add Javadoc documenting valid `opCode` values, return value (file path), and thrown exceptions
[A04-9] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java | Line: 21, 26, 45, 60
Description: Four public methods lack Javadoc despite non-obvious behavior such as defaulting to English and comma-separated string storage
Fix: Add method-level Javadoc to constructor, `queryLangConfigBy`, `updateLanguageBy`, and `insertBy` documenting parameters, return values, and default behaviors
[A04-10] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/service/HireDehireService.java | Line: 18
Description: Sole public method takes 6 parameters with complex SQL, UNION ALL query, and `"All"` wildcard behavior, all undocumented
Fix: Add Javadoc documenting all parameters, wildcard behavior for `"All"`, return value `Map<String, List<DehireBean>>` structure, and SQL logic
[A04-11] MEDIUM | File: BusinessInsight.java (line 23), BusinessInsightBean.java (line 23), BusinessInsightExcel.java (line 17), HireDehireService.java (line 14)
Description: Four classes with significant business logic (report generation, data fetching, hire/dehire service) have no class-level Javadoc
Fix: Add class-level Javadoc to each class describing its responsibility, usage context, and relationship to the business insight module
[A04-12] LOW | File: BusinessInsightBean.java, BusinessInsightExcel.java, PreOpQuestions.java, Question.java, SupervisorUnlockBean.java
Description: 45 simple getter/setter methods across five files lack Javadoc
Fix: Add Javadoc to getter/setter methods, at minimum for those with non-obvious field semantics
[A04-13] LOW | File: PreOpQuestions.java (line 5), Question.java (line 3), SupervisorUnlockBean.java (line 3)
Description: Three POJO/bean classes have no class-level Javadoc explaining their purpose or usage context (JSON serialization, supervisor unlock tracking)
Fix: Add class-level Javadoc to each class describing its purpose, serialization format, and usage context
[A04-14] INFO | File: BusinessInsight.java (line 32), SupervisorUnlockBean.java (line 12)
Description: IDE-generated `// TODO Auto-generated constructor stub` comments remain in production code and are not actionable
Fix: Remove the auto-generated TODO comments or replace with meaningful constructor documentation
[A04-15] INFO | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java | Line: 106, 109, 113-114, 132
Description: Commented-out debug code remains including alternative directory logic and a hardcoded developer email address (`julius@collectiveintelligence.com.au`)
Fix: Remove all commented-out code lines; if the logic may be needed later, track it in version control instead
[A04-16] INFO | File: WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java | Line: 142
Description: Public static utility method `now(String dateFormat)` has no Javadoc despite being callable from anywhere
Fix: Add Javadoc documenting the `dateFormat` parameter (SimpleDateFormat pattern) and return value (formatted current timestamp string)

### excel-reports-A-I

[H-1] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ (all 18 files) | Line: all
Description: Zero documentation across all 18 files -- no class Javadoc, no method Javadoc, no @param/@return/@throws on any of the 69 public methods.
Fix: Add class-level and method-level Javadoc with @param/@return/@throws to all 69 public methods across all 18 files.
[M-1] MEDIUM | File: ExcelBroadcastMsgReport.java, ExcelDynDriverReport.java, ExcelDynSeenReport.java, ExcelDynTransportDriverReport.java | Line: 42, 46, 46, 41
Description: Four classes have misleadingly named public methods (createUnitUnlockReport, createDynUnitReport) that do not match the class purpose -- copy-paste residue.
Fix: Rename methods to match their actual report type (e.g., createBroadcastMsgReport, createDynDriverReport, createDynSeenReport, createDynTransportDriverReport).
[M-2] MEDIUM | File: ExcelCimplicityShockReport.java, ExcelCimplicityUtilReport.java, ExcelCurrDrivReport.java, ExcelCurrUnitReport.java, ExcelDailyVehSummaryReport.java, ExcelDynDriverReport.java, ExcelDynSeenReport.java, ExcelImpactMeterReport.java, ExcelImpactReport.java | Line: 54, 62, 61, 62, 93, 107, 99, 77, 79
Description: Nine files instantiate UnitDAO objects that are never referenced, adding unnecessary resource allocation.
Fix: Remove the unused `UnitDAO unitDAO = new UnitDAO()` instantiation from each of the nine files.
[M-3] MEDIUM | File: ExcelImpactReport.java | Line: 234
Description: Auto-generated TODO catch block with bare e.printStackTrace() for JSONException -- never properly implemented with logging or error handling.
Fix: Replace e.printStackTrace() with proper logging (e.g., logger.error()) and appropriate error handling or re-throw.
[L-1] LOW | File: ExcelDriverLicenceExpiry.java | Line: 53
Description: Typo in tab title string: "Driver LIcence Expiry Report" -- uppercase 'I' in "LIcence".
Fix: Change `"Driver LIcence Expiry Report"` to `"Driver Licence Expiry Report"`.
[L-2] LOW | File: ExcelImpactReport.java | Line: 221
Description: Misspelling "longtitue" should be "longitude".
Fix: Change `"longtitue"` to `"longitude"`.
[L-3] LOW | File: 16 of 18 files in excel/reports/ | Line: varies
Description: Commented-out code `//adjust first column width: sheet.autoSizeColumn(0);` appears in 16 files as stale dead code.
Fix: Remove the commented-out code line from all 16 files, or uncomment it if the functionality is actually needed.

### excel-reports-K-Z-mail

[A12-P3-001] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ (all 16 files) | Line: N/A
Description: Complete lack of Javadoc across all 16 files -- 0% documentation coverage on 60 public methods
Fix: Add class-level and method-level Javadoc to all 60 public methods across all 16 files
[A12-P3-002] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilisationReport.java | Line: 163
Description: Possible data bug -- key_hours getter used for "Traction Hours" column instead of likely-correct track_hours
Fix: Verify business logic and replace utilBean.getKey_hours() with utilBean.getTrack_hours() if confirmed as bug
[A12-P3-003] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailExcelReports.java | Line: 21,24,37,40
Description: Four IDE-generated TODO catch blocks swallow AddressException and MessagingException with only printStackTrace
Fix: Replace printStackTrace with proper logging framework calls and appropriate error handling/re-throwing
[A12-P3-004] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelVorReport.java | Line: 308
Description: Inaccurate end-of-method comment says "createDynReport" but method is actually named "createVorReport"
Fix: Change comment from "// end method createDynReport" to "// end method createVorReport"
[A12-P3-005] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java | Line: 10,15,24,69,74,83
Description: Hard-coded HTTP URLs to fleetfocus.lindemh.com.au for images and CSS -- insecure and not environment-agnostic
Fix: Replace hard-coded HTTP URLs with HTTPS and externalize domain to configuration
[A12-P3-006] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java | Line: 6
Description: Incomplete DOCTYPE declaration missing doctype specification in HTML email header
Fix: Add proper DOCTYPE specification (e.g., <!DOCTYPE html>)
[A12-P3-007] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java | Line: N/A
Description: No HTML escaping of parameters in email header methods -- potential XSS risk if parameters contain user-controlled HTML
Fix: Apply HTML entity escaping to all string parameters before embedding in HTML output
[A12-P3-008] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelKeyHourUtilReport.java | Line: 11,8,9,106
Description: Unused imports (EvaluationCell, Date, duplicate ArrayList) and unused local variable unitDAO
Fix: Remove unused imports and the unused unitDAO variable declaration
[A12-P3-009] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckFailReport.java | Line: 6,86,245
Description: Unused import Vector, unused unitDAO variables, and form parameter accepted but never used in overloaded method
Fix: Remove unused import and variables; either use the form parameter or remove it from the method signature
[A12-P3-010] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckReport.java | Line: 8,12,9,68
Description: Unused imports (CellStyle, CellRangeAddress, FormulaEvaluator) and unused local variable unitDAO
Fix: Remove unused imports and the unused unitDAO variable declaration
[A12-P3-011] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelRestrictedUsageReport.java | Line: 71,101
Description: Unused local variable temp set to "x" but never read; model parameter unused in both createExcel and createRestrictedAccessReport
Fix: Remove unused temp variable and either use or remove model parameter from method signatures
[A12-P3-012] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSeatHourUtilReport.java | Line: 8,105,136
Description: Duplicate ArrayList import, unused local variables unitDAO and evaluator, raw-type ArrayList usage throughout
Fix: Remove duplicate import and unused variables; add generics to ArrayList declarations
[A12-P3-013] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelServMaintenanceReport.java | Line: 7
Description: Duplicate import java.util.ArrayList
Fix: Remove duplicate import statement
[A12-P3-014] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelSuperMasterAuthReport.java | Line: 7,15,96
Description: Duplicate ArrayList import, unused DriverImpactReportBean import, model parameter accepted but unused
Fix: Remove duplicate/unused imports and either use or remove model parameter from method signatures
[A12-P3-015] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUnitUnlockReport.java | Line: 6,61
Description: Duplicate ArrayList import and unused local variable unitDAO, raw-type ArrayList usage
Fix: Remove duplicate import and unused variable; add generics to ArrayList declarations
[A12-P3-016] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReport.java | Line: 14,47-52,68
Description: Unused import PreOpCheckReportBean, unused local variables get_user/get_loc/get_dep/form_nm/chartUrl/unitDAO
Fix: Remove unused import and all unused local variable declarations
[A12-P3-017] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilWOWReportEmail.java | Line: 14,48-51,69
Description: Unused import PreOpCheckReportBean, unused local variables get_user/get_loc/get_dep/form_nm/unitDAO; massive code duplication with ExcelUtilWOWReport.java
Fix: Remove unused import and variables; refactor to extract shared logic with ExcelUtilWOWReport into a common base
[A12-P3-018] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelUtilisationReport.java | Line: 7,45-59,80
Description: Duplicate ArrayList import, 12 unused local variables (Vgp_cd through get_dep), unused unitDAO
Fix: Remove duplicate import and all unused local variable declarations
[A12-P3-019] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelVorReport.java | Line: 105,57
Description: Unused local variable unitDAO; vrpt_veh_value_stopv assigned same value as vrpt_veh_value_stop (copy-paste error)
Fix: Remove unused unitDAO; verify vrpt_veh_value_stopv assignment is correct or fix the copy-paste error
[A12-P3-020] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelPreOpCheckFailReport.java | Line: 86-245
Description: Two overloaded createPreOpFailReport methods contain ~150 lines of nearly identical duplicated code
Fix: Extract shared logic into a single private method and have both overloads delegate to it
[A12-P3-021] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ (12 files) | Line: various
Description: Repeated commented-out code "//adjust first column width: sheet.autoSizeColumn(0);" appears in 12 of 14 Excel report files
Fix: Either remove the commented-out code or uncomment and use it if the functionality is desired
[A12-P3-022] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ (8+ files) | Line: various
Description: unitDAO instantiated but never used in at least 8 files -- unnecessary object creation
Fix: Remove unused unitDAO instantiations across all affected files
[A12-P3-023] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/ (multiple files) | Line: various
Description: Public create*Report methods appear to be internal implementation called only from createExcel but are exposed as public API
Fix: Reduce visibility of create*Report methods from public to private
[A12-P3-024] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailExcelReports.java | Line: 19,35
Description: Hard-coded "unknown" strings passed as sender name and CC parameters to mail.sendMail
Fix: Replace hard-coded "unknown" with proper configuration values or meaningful defaults
[A12-P3-025] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailExcelReports.java | Line: 14,27
Description: System.out.println used for timing logging instead of a logging framework; inconsistent between overloads
Fix: Replace System.out.println with proper logging framework calls and apply consistently to both overloads

### excel-reports-beans-A-D

[P3-ERBA-001] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BaseFilterBean.java | Line: 1-55
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose as a filter parameter holder with its 7 String fields
[P3-ERBA-002] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BaseItemResultBean.java | Line: 1-5
Description: No class-level Javadoc documentation exists on completely empty class
Fix: Add class-level Javadoc explaining whether this is a marker type or planned base class, or remove if unused
[P3-ERBA-003] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BaseResultBean.java | Line: 1-15
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's role as a base result holder with its appliedFilterBean field
[P3-ERBA-004] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BatteryReportBean.java | Line: 1-51
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for battery report data
[P3-ERBA-005] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityShockReportBean.java | Line: 1-26
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for Cimplicity shock report data
[P3-ERBA-006] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityUtilReportBean.java | Line: 1-59
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for Cimplicity utilization report data
[P3-ERBA-007] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrDrivReportBean.java | Line: 1-118
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for current driver report data and how it differs from CurrUnitReportBean
[P3-ERBA-008] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrUnitReportBean.java | Line: 1-118
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for current unit report data and how it differs from CurrDrivReportBean
[P3-ERBA-009] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DailyVehSummaryReportBean.java | Line: 1-207
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for daily vehicle summary metrics
[P3-ERBA-010] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverAccessAbuseBean.java | Line: 1-107
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for driver access/abuse data
[P3-ERBA-011] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverImpactReportBean.java | Line: 1-78
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for driver impact report data
[P3-ERBA-012] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverLicenceExpiryBean.java | Line: 1-23
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for driver licence expiry data
[P3-ERBA-013] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynDriverReportBean.java | Line: 1-178
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for dynamic driver report data
[P3-ERBA-014] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynSeenReportBean.java | Line: 1-102
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for dynamic "seen" report data
[P3-ERBA-015] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynUnitReportBean.java | Line: 1-200
Description: No class-level Javadoc documentation exists
Fix: Add class-level Javadoc describing the bean's purpose for dynamic unit report data
[P3-ERBA-016] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/*.java | Line: all
Description: Zero method-level Javadoc across all 15 files; 330 public methods are completely undocumented
Fix: Add Javadoc to all public getter/setter methods describing the field semantics and expected value domains
[P3-ERBA-017] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverAccessAbuseBean.java | Line: 3-4
Description: Duplicate import -- `import java.util.ArrayList;` appears on both line 3 and line 4
Fix: Remove the duplicate import on line 4
[P3-ERBA-018] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrDrivReportBean.java, CurrUnitReportBean.java | Line: 1-118
Description: Near-duplicate classes -- structurally identical (same 15 fields, names, types, getters/setters, 118 lines each) with no documentation explaining their distinction
Fix: Document the intended difference between current driver report and current unit report beans, or refactor to eliminate duplication
[P3-ERBA-019] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BatteryReportBean.java, CimplicityShockReportBean.java, CimplicityUtilReportBean.java, CurrDrivReportBean.java, CurrUnitReportBean.java, DailyVehSummaryReportBean.java, DriverAccessAbuseBean.java, DriverImpactReportBean.java, DriverLicenceExpiryBean.java, DynDriverReportBean.java, DynSeenReportBean.java, DynUnitReportBean.java | Line: all
Description: Raw ArrayList types used without generics across 12 files (only partial generics in DriverAccessAbuseBean for 2 of 14 fields)
Fix: Add generic type parameters to all ArrayList declarations (e.g., `ArrayList<String>`) for type safety
[P3-ERBA-020] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityUtilReportBean.java, CurrDrivReportBean.java, CurrUnitReportBean.java, DynDriverReportBean.java, DynSeenReportBean.java, DynUnitReportBean.java | Line: all
Description: Non-standard uppercase-initial field naming (e.g., `Vrpt_veh_typ_cd`) violates Java naming conventions and creates ambiguity with class references
Fix: Rename fields to use standard Java camelCase naming convention (e.g., `vrptVehTypCd`)
[P3-ERBA-021] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/*.java | Line: all
Description: Fields declared at package-private (default) visibility instead of private despite having public getters/setters; inconsistent in DriverAccessAbuseBean (3 private, 11 package-private)
Fix: Declare all fields as private to enforce encapsulation consistently
[P3-ERBA-022] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BaseItemResultBean.java | Line: 1-5
Description: Completely empty class with no fields, methods, or comments; purpose is unknown
Fix: Document the class purpose or remove it if unused; if it is a marker type, add Javadoc stating so
[P3-ERBA-023] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/*.java | Line: all
Description: All beans use database-column-style underscore naming (e.g., `dsum_veh_typ_nm`) instead of Java camelCase with no documentation mapping fields to their database columns or domain meanings
Fix: Add field-level Javadoc mapping each field to its database column and documenting its domain meaning

### excel-reports-beans-H-Z-dao

[OBS-1] HIGH | File: beans/HireDehireReportBean.java, beans/ImpactReportBean.java, beans/KeyHourUtilBean.java, beans/OperationalStatusReportItemResultBean.java, beans/OperationalStatusReportResultBean.java, beans/PreOpCheckFailReportBean.java, beans/PreOpCheckReportBean.java, beans/SeatHourUtilBean.java, beans/ServMaintenanceReportBean.java, beans/SuperMasterAuthReportBean.java, beans/UnitUnlockReportBean.java, beans/UtilWowReportBean.java, beans/UtilisationReportBean.java, dao/CustomerDAO.java, dao/DriverAccessAbuseDAO.java | Line: all
Description: Zero documentation across all 15 files -- no class-level Javadoc, method-level Javadoc, or inline explanatory comments exist in any audited file (0 of 324 public methods documented)
Fix: Add class-level Javadoc to all 15 files explaining each class's purpose, and method-level Javadoc to DAO methods with non-trivial logic
[OBS-2] LOW | File: beans/*.java (files 1-13) | Line: all
Description: Bean classes are pure POJOs with only fields and getter/setter pairs; class-level Javadoc explaining the report each bean supports and its abbreviated field names is critically missing
Fix: Add class-level Javadoc to each bean describing the report it backs and a field glossary for abbreviated names
[OBS-3] MEDIUM | File: beans/PreOpCheckReportBean.java, beans/PreOpCheckFailReportBean.java, beans/KeyHourUtilBean.java, beans/SeatHourUtilBean.java | Line: all
Description: Duplicate/near-duplicate class pairs detected -- PreOpCheckReportBean and PreOpCheckFailReportBean are structurally identical, as are KeyHourUtilBean and SeatHourUtilBean, with no documentation explaining their intended distinction
Fix: Document the intended distinction between each duplicate pair or refactor into a single parameterised class with a discriminator
[OBS-4] HIGH | File: dao/CustomerDAO.java | Line: 17, 55, 92, 129, 165
Description: Most logic-bearing file in scope has 5 public SQL-querying methods with zero Javadoc; methods have non-trivial parameters and database table dependencies undocumented
Fix: Add method-level Javadoc to all 5 methods documenting parameters, queried tables, return semantics, and default-value behavior
[OBS-5] MEDIUM | File: dao/DriverAccessAbuseDAO.java | Line: 7-30
Description: Declares 13 instance-level ArrayList fields and multiple unused imports (Connection, ResultSet, SQLException, Statement, Collections, StringTokenizer) that appear to serve no purpose
Fix: Remove unused instance fields and unused imports, or document their intended purpose if they are needed for a future use case
[OBS-6] MEDIUM | File: beans/*.java (all 15 files) | Line: all
Description: Cryptic abbreviated field names throughout (po_dnm, vutil1, sm_ser_ed2, vunit_lotm, a_driv_cd, etc.) with no documentation; meaning can only be inferred from database column names
Fix: Add inline comments or Javadoc on each field mapping abbreviated names to their full meaning and source database column

### excel-reports-email

[EXC-RPT-001] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBatteryReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import on line 7
[EXC-RPT-002] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBatteryReport.java | Line: 101
Description: Commented-out code for autoSizeColumn left in source
Fix: Remove the commented-out line or restore the autoSizeColumn call if needed
[EXC-RPT-003] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBroadcastMsgReport.java | Line: 22
Description: Constructor title "Machine Unlock Report" does not match report content "Broadcast Message Report"
Fix: Change the constructor title string to "Broadcast Message Report" to match the actual report
[EXC-RPT-004] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBroadcastMsgReport.java | Line: 68
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-005] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityShockReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-006] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityShockReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-007] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityUtilReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-008] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityUtilReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-009] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrDrivReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-010] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrDrivReport.java | Line: 99-101
Description: Commented-out conditional dept header code left in source
Fix: Remove the commented-out code block or restore if the logic is needed
[EXC-RPT-011] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrDrivReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-012] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrUnitReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-013] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCurrUnitReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-014] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDailyVehSummaryReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-015] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDailyVehSummaryReport.java | Line: N/A
Description: Total row renders all totals including leader-only columns regardless of cust_type gating (potential data bug)
Fix: Add cust_type conditional checks to the total row rendering to match the column rendering logic
[EXC-RPT-016] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDailyVehSummaryReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-017] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverAccessAbuseReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-018] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverAccessAbuseReport.java | Line: 83
Description: Commented-out ArrayList declaration left in source
Fix: Remove the commented-out line
[EXC-RPT-019] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverAccessAbuseReport.java | Line: N/A
Description: Dual initialization methods init() and init2() contain largely duplicated logic
Fix: Refactor to a single parameterized init method that handles both calling patterns
[EXC-RPT-020] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverImpactReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-021] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverImpactReport.java | Line: 64, 69-79
Description: Commented-out code referencing old filter variable left in source
Fix: Remove the commented-out code block
[EXC-RPT-022] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverImpactReport.java | Line: N/A
Description: FormulaEvaluator instantiated but never used for evaluation
Fix: Remove the unused FormulaEvaluator instantiation
[EXC-RPT-023] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverLicenceExpiry.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-024] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverLicenceExpiry.java | Line: 22, 68, 72
Description: Typo "LIcence" (uppercase I) repeated 3 times in title strings
Fix: Change "LIcence" to "Licence" in all three occurrences
[EXC-RPT-025] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDriverLicenceExpiry.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-026] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynDriverReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-027] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynDriverReport.java | Line: 71
Description: Commented-out dbreport.setSet_form_cd(form_cd) left in source
Fix: Remove the commented-out line
[EXC-RPT-028] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynDriverReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-029] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynSeenReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-030] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynSeenReport.java | Line: N/A
Description: Method named createDynUnitReport() does not match report purpose (Pedestrian Detection Report)
Fix: Rename method to createPedestrianDetectionReport() or similar to reflect actual purpose
[EXC-RPT-031] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynSeenReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-032] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynSeenReport.java | Line: N/A
Description: FormulaEvaluator imported but never used
Fix: Remove the unused FormulaEvaluator import
[EXC-RPT-033] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynUnitReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-034] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynUnitReport.java | Line: 76, 281-283, 323-326, 344-346
Description: Extensive commented-out code referencing old TIME() formula approach
Fix: Remove the commented-out code blocks
[EXC-RPT-035] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailDynUnitReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-036] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailRestictedAccessUsageReport.java | Line: 1
Description: Class name typo "Resticted" should be "Restricted"
Fix: Rename class to EmailRestrictedAccessUsageReport and update all references
[EXC-RPT-037] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSuperMasterAuthReport.java | Line: 112
Description: Title inconsistency between "Authentication" (rptTitle) and "Authorisation" (sheet tab with trailing space)
Fix: Align both title strings to use the same spelling and remove the trailing space
[EXC-RPT-038] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUnitUnlockReport.java | Line: N/A
Description: Method named createBroadcastMsgReport() does not match report purpose (Machine Unlock Report)
Fix: Rename method to createUnitUnlockReport() to reflect actual purpose
[EXC-RPT-039] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailVorReport.java | Line: 24, 131
Description: Constructor title "Detailed Report by Unit" does not match sheet tab "Vor Report"
Fix: Change the constructor title to "VOR Report" to match the sheet tab
[EXC-RPT-040] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailVorReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-041] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailVorReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-042] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailVorReport.java | Line: N/A
Description: FormulaEvaluator imported but never used
Fix: Remove the unused FormulaEvaluator import
[EXC-RPT-043] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailKeyHourUtilReport.java | Line: 112-114
Description: Subtitle labels swapped: Customer=locName, Site=deptName, Dept=custName
Fix: Correct the label-to-value mapping so Customer=custName, Site=locName, Dept=deptName
[EXC-RPT-044] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailKeyHourUtilReport.java | Line: N/A
Description: FormulaEvaluator instantiated but never used for evaluation
Fix: Remove the unused FormulaEvaluator instantiation
[EXC-RPT-045] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java | Line: 104-106
Description: Subtitle labels swapped: Customer=locName, Site=deptName, Dept=custName (same as KeyHourUtilReport)
Fix: Correct the label-to-value mapping so Customer=custName, Site=locName, Dept=deptName
[EXC-RPT-046] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java | Line: 165-196
Description: Copy-paste bug: all cell string values reference vutil1 instead of vutil2..vutil8, displaying wrong data
Fix: Update each cell value to reference the correct vutilN variable matching its time period
[EXC-RPT-047] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java | Line: N/A
Description: Vector imported but never used
Fix: Remove the unused Vector import
[EXC-RPT-048] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailSeatHourUtilReport.java | Line: N/A
Description: FormulaEvaluator instantiated but never used for evaluation
Fix: Remove the unused FormulaEvaluator instantiation
[EXC-RPT-049] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-050] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReport.java | Line: N/A
Description: Dual initialization methods init() and init2() contain largely duplicated logic
Fix: Refactor to a single parameterized init method that handles both calling patterns
[EXC-RPT-051] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-052] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReportNew.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-053] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReportNew.java | Line: N/A
Description: Class named "New" but uses service_flag (not service_flag_new) creating a naming contradiction
Fix: Align the op code to service_flag_new or rename the class to remove the misleading "New" suffix
[EXC-RPT-054] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailServMaintenanceReportNew.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-055] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkFailReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-056] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkFailReport.java | Line: N/A
Description: FormulaEvaluator instantiated but never used
Fix: Remove the unused FormulaEvaluator instantiation
[EXC-RPT-057] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkFailReport.java | Line: N/A
Description: Vector imported but never used
Fix: Remove the unused Vector import
[EXC-RPT-058] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-059] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailPreOpChkReport.java | Line: N/A
Description: Vector imported but never used
Fix: Remove the unused Vector import
[EXC-RPT-060] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilWowReport.java | Line: N/A
Description: Method named createCurrReport() does not reflect utilisation report purpose; multiple unused local variables
Fix: Rename method to createUtilWowReport() and remove unused local variables
[EXC-RPT-061] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilWowReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-062] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java | Line: 6-7
Description: Duplicate import of java.util.ArrayList
Fix: Remove the duplicate ArrayList import
[EXC-RPT-063] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java | Line: 57, 62
Description: Commented-out System.out.println debug lines left in source
Fix: Remove the commented-out debug print statements
[EXC-RPT-064] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java | Line: N/A
Description: Date and SimpleDateFormat imported but never used
Fix: Remove the unused Date and SimpleDateFormat imports
[EXC-RPT-065] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailUtilisationReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-066] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactMeterReport.java | Line: N/A
Description: DecimalFormat imported but never used
Fix: Remove the unused DecimalFormat import
[EXC-RPT-067] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactMeterReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-068] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactReport.java | Line: N/A
Description: DecimalFormat imported but never used
Fix: Remove the unused DecimalFormat import
[EXC-RPT-069] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactReport.java | Line: N/A
Description: UnitDAO unitDAO instantiated but never used
Fix: Remove the unused UnitDAO instantiation
[EXC-RPT-070] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactMeterReport.java | Line: 204
Description: Hardcoded URL http://fleetfocus.lindemh.com.au/fms/ instead of using configuration
Fix: Replace the hardcoded URL with a configurable property from RuntimeConf
[EXC-RPT-071] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailImpactReport.java | Line: N/A
Description: Hardcoded URL http://fleetfocus.lindemh.com.au/fms/ instead of using configuration
Fix: Replace the hardcoded URL with a configurable property from RuntimeConf
[EXC-RPT-072] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailBroadcastMsgReport.java | Line: 79
Description: Commented-out autoSizeColumn code left in source
Fix: Remove the commented-out line
[EXC-RPT-073] LOW | File: WEB-INF/src/com/torrent/surat/fms6/excel/reports/EmailCimplicityShockReport.java | Line: N/A
Description: Commented-out autoSizeColumn code left in source
Fix: Remove the commented-out line

### pdf-reports

[1] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java | Line: 96
Description: createTable() Javadoc declares @return on a void method, copy-pasted from ReportPDF
Fix: Remove the inaccurate @return tag and rewrite Javadoc to reflect that the method returns void
[2] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java | Line: 55
Description: createPdf() Javadoc references "movies" from iText tutorial and documents a @param filename that does not exist in the method signature
Fix: Replace tutorial-derived Javadoc with accurate description of fleet report PDF generation and remove the phantom @param filename tag
[3] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java | Line: 96
Description: createTable() Javadoc declares @return on a void method; method body contains hard-coded placeholder content suggesting dead scaffold code
Fix: Remove inaccurate @return tag, document actual behavior, and evaluate whether scaffold content should be removed
[4] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java | Line: 1-1747
Description: 1,747-line file with zero Javadoc comments at class or method level; 60+ public getters/setters with opaque field names undocumented
Fix: Add class-level Javadoc and document all public methods, especially non-trivial fields like no_units, max_impact, no_uncal, no_dislockout
[5] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java | Line: 1-10015
Description: 10,015-line file with zero Javadoc comments; 100+ public getters/setters with opaque names like Vrpt_veh_driv_is_technician completely undocumented
Fix: Add class-level and method-level Javadoc, prioritizing the public API methods init(), clear_variables(), getDept_prefix(), and fetchNames()
[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java | Line: 1-21854
Description: 21,854-line file (largest in scope) with zero Javadoc; 300+ public getters/setters and 10+ public methods entirely undocumented
Fix: Add class-level Javadoc and document all public methods, prioritizing init(), filterUnitDriverOptions(), getImageFromByte(), and HourAdd()
[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java | Line: 2396
Description: TODO Auto-generated catch block in ParseException handler that only calls e.printStackTrace()
Fix: Replace e.printStackTrace() with proper logging and error handling
[8] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java | Line: 15100
Description: TODO Auto-generated catch block in AddressException handler that only calls e.printStackTrace()
Fix: Replace e.printStackTrace() with proper logging and error handling
[9] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java | Line: 15103
Description: TODO Auto-generated catch block in MessagingException handler that only calls e.printStackTrace()
Fix: Replace e.printStackTrace() with proper logging and error handling
[10] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report1.java | Line: 1-817
Description: 817-line file with zero Javadoc; ~50 public getters/setters with opaque names like Vio0_data0 through Vio9_data2 completely undocumented
Fix: Add class-level Javadoc and document all public methods and the semantics of the Vio/iio field naming scheme
[11] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_reports.java | Line: 1-127
Description: Effectively dead class; only active method clearVectors() has empty body, and entire query() method (lines 52-125) is commented out with references to wrong class Databean_getuser
Fix: Evaluate whether this class can be deleted entirely; if retained, remove commented-out dead code and document the class purpose
[12] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/LinderReportDatabean.java | Line: 1-1935
Description: 1,935-line file with zero Javadoc; 15 non-getter/setter public methods all undocumented including critical report-fetching methods
Fix: Add class-level Javadoc and document all 15 public report methods including fetchUnitUtilisationReport(), fetchImpactReport(), etc.
[13] LOW | File: WEB-INF/src/com/torrent/surat/fms6/reports/LinderReportDatabean.java | Line: 60
Description: TODO Auto-generated constructor stub in empty default constructor
Fix: Either add meaningful initialization logic or remove the TODO and document that the default constructor is intentionally empty
[14] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/RTLSHeatMapReport.java | Line: 1-525
Description: Zero Javadoc in entire file; core public method getPointsJson() for generating heat map GeoJSON is undocumented
Fix: Add class-level Javadoc and document getPointsJson(), init(), and the density/arrPoints fields
[15] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/RTLSHeatMapReport.java | Line: 99,108,117,182,191,200,356,365,374,412,421,430,495
Description: 13 TODO Auto-generated catch block stubs across getPoints(), getSessionPoints(), getVehSession(), getOrigin(), and createJSON() methods
Fix: Replace all e.printStackTrace() calls with proper logging framework usage and meaningful error handling
[16] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/RTLSImpactReport.java | Line: 1-1262
Description: Zero Javadoc in entire file; misspelled method name caculateImpactCacheTable() (should be calculate); 4 public methods undocumented
Fix: Add class-level Javadoc, document all public methods, and rename caculateImpactCacheTable() to calculateImpactCacheTable()
[17] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/RTLSImpactReport.java | Line: 690
Description: Actionable TODO indicating untuned algorithmic parameter min_dist=0.01 with comment "find a suitable minimum distance. Default is 0.3"
Fix: Research and set an appropriate min_dist value based on RTLS hardware specs and testing, then remove the TODO
[18] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/RTLSImpactReport.java | Line: 96,105,114,154,163,172,218,227,236,281,290,299,343,352,361,401,410,419,458,467,476,595,604,613,659,668,677,888,1012,1021,1030,1073,1082,1091,1137,1146,1155
Description: 37 TODO Auto-generated catch block stubs across all private methods in finally blocks
Fix: Replace all e.printStackTrace() calls with proper logging framework usage and meaningful error handling
[19] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Reports.java | Line: 1-608
Description: Zero Javadoc in entire file; 5 public Fetch_* methods with inconsistent naming convention (capitalized prefix) all undocumented
Fix: Add class-level Javadoc, document all public methods, and standardize method naming to camelCase (e.g., fetchCustomers())
[20] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/Reports.java | Line: 84,93,102,151,160,169,239,248,257,305,314,323,370,379,388
Description: 15 TODO Auto-generated catch block stubs across all Fetch_* and getVehTag() method finally blocks
Fix: Replace all e.printStackTrace() calls with proper logging framework usage and meaningful error handling
[21] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/UtilBean.java | Line: 1-71
Description: Zero Javadoc; compareTo() sorting semantics undocumented; setDayNum() uses unconventional Monday=0 week start with no documentation
Fix: Add class-level Javadoc and document compareTo() sorting contract and setDayNum() day-mapping convention
[22] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/reports/UtilModelBean.java | Line: 1-65
Description: Zero Javadoc; unclear field name "avatruck" with no documentation; raw type ArrayList used in getUb()/setUb()
Fix: Add class-level Javadoc, document the meaning of "avatruck", parameterize the raw ArrayList type, and document all public methods
[23] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java | Line: 1-173
Description: Zero class-level Javadoc; 6-parameter constructor and core createPdf() method completely undocumented
Fix: Add class-level Javadoc explaining report purpose and document the constructor parameters and createPdf() method
[24] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java | Line: 1-236
Description: Zero class-level Javadoc; dead scaffold code in createTable() and createList() with hard-coded placeholder content ("Cell with colspan 3", "First point")
Fix: Add class-level Javadoc, remove or replace dead scaffold code, and document all protected methods that form the template method pattern
[25] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_report.java | Line: 18511
Description: init() method spanning ~400 lines dispatches to 30+ private methods based on opcode strings with no documentation of valid opcodes or their effects
Fix: Document all valid opcode strings and their corresponding behaviors; consider refactoring to a strategy or command pattern
[26] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_dyn_reports.java | Line: 7767
Description: init() method serves as undocumented dispatch hub based on opcode strings with no documentation of valid opcodes
Fix: Document all valid opcode strings and their corresponding behaviors in method-level Javadoc
[27] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/reports/Databean_cdisp.java | Line: 1264
Description: init() method serves as undocumented dispatch hub based on opcode strings with no documentation of valid opcodes
Fix: Document all valid opcode strings and their corresponding behaviors in method-level Javadoc

### rtls

[GC-01] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/rtls/GridCluster.java | Line: 21-44
Description: `reducePoints()` has no Javadoc; implements grid-based spatial clustering with undocumented `density` parameter units, range, and meaning
Fix: Add Javadoc explaining grid-based clustering algorithm, `density` parameter (parsed as percentage), return value semantics, and grid cell behavior
[GC-02] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/rtls/GridCluster.java | Line: 47-74
Description: `calculateStdev()` has no Javadoc; computes sample standard deviation and returns mean+stdev threshold as string with undocumented statistical purpose
Fix: Add Javadoc documenting the outlier-detection threshold computation, why it returns a string, and the statistical meaning of mean+stdev
[GC-03] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/rtls/GridCluster.java | Line: 13-19
Description: `simplePoints()` (private) performs grid-snapping via integer-division and re-centering with no inline comments explaining the math
Fix: Add inline comments explaining the grid-snap algorithm (integer-divide by modulus, re-center to cell midpoint)
[GC-04] INFO | File: WEB-INF/src/com/torrent/surat/fms6/rtls/GridCluster.java | Line: 53
Description: Variable `treshold` is misspelled; should be `threshold`
Fix: Rename variable from `treshold` to `threshold`
[GC-05] INFO | File: WEB-INF/src/com/torrent/surat/fms6/rtls/GridCluster.java | Line: 10
Description: No class-level Javadoc; class purpose (grid-based spatial clustering for RTLS point data) is undocumented
Fix: Add class-level Javadoc describing grid-based spatial clustering purpose and usage
[LLC-01] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 56-104
Description: `computerThatLonLat()` implements Vincenty's direct formula for WGS-84 with only skeleton `@param` tags providing zero information; no algorithm reference, no unit docs, no `@throws`
Fix: Add full Javadoc documenting Vincenty's direct formula, parameter units (x,y in meters as local Cartesian offsets), return behavior, and algorithm source reference
[LLC-01a] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 13-14
Description: Hardcoded origin coordinates (Sydney, Australia area: 150.95866, -33.92217) are undocumented magic numbers
Fix: Add comments documenting what geographic location the origin coordinates represent and why they are hardcoded
[LLC-02] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 9-11
Description: WGS-84 ellipsoid constants `a`, `b`, `f` are private instance fields with no documentation; should be `static final`
Fix: Add Javadoc identifying constants as WGS-84 semi-major axis, semi-minor axis, and flattening; declare as `static final`
[LLC-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 115-117
Description: `getBrng()` has no Javadoc; inline comment is terse and does not explain the +90 degree offset or coordinate system convention; return units unstated
Fix: Add Javadoc documenting bearing computation, coordinate system convention (math angle to compass bearing), and return value in degrees
[LLC-04] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 119-121
Description: `getDistance()` has no Javadoc; computes Euclidean distance with undocumented units (meters assumed)
Fix: Add Javadoc with `@param` and `@return` specifying units in meters
[LLC-05] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 19-21
Description: `getOringin_lat()` has no Javadoc
Fix: Add Javadoc for getter documenting origin latitude in degrees
[LLC-06] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 23-25
Description: `setOringin_lat()` has no Javadoc
Fix: Add Javadoc for setter documenting origin latitude parameter in degrees
[LLC-07] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 27-29
Description: `getOringin_lon()` has no Javadoc
Fix: Add Javadoc for getter documenting origin longitude in degrees
[LLC-08] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 31-33
Description: `setOringin_lon()` has no Javadoc
Fix: Add Javadoc for setter documenting origin longitude parameter in degrees
[LLC-09] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 35-37
Description: `getLon()` has no Javadoc
Fix: Add Javadoc for getter documenting computed longitude
[LLC-10] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 39-41
Description: `setLon()` has no Javadoc
Fix: Add Javadoc for setter documenting longitude parameter
[LLC-11] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 43-45
Description: `getLat()` has no Javadoc
Fix: Add Javadoc for getter documenting computed latitude
[LLC-12] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 47-49
Description: `setLat()` has no Javadoc
Fix: Add Javadoc for setter documenting latitude parameter
[LLC-13] INFO | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 5
Description: No class-level Javadoc; class implements geodetic coordinate conversion (local Cartesian to WGS-84 via Vincenty's direct formula)
Fix: Add class-level Javadoc describing geodetic conversion purpose and algorithm reference
[LLC-14] INFO | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 13-14
Description: Field names `oringin_lon` and `oringin_lat` contain typo "oringin" (should be "origin"), propagating to getter/setter names
Fix: Rename fields and accessors from `oringin` to `origin`
[MA-01] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/rtls/MovingAverage.java | Line: 6-24
Description: No class-level Javadoc; class implements simple moving average (SMA) with sliding window backed by Queue but algorithm type and window semantics are undocumented
Fix: Add class-level Javadoc specifying SMA algorithm type, sliding window behavior, and Queue-based implementation
[MA-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/rtls/MovingAverage.java | Line: 12-14
Description: Constructor `MovingAverage(int size)` has no Javadoc; `size` parameter meaning (sliding window width) is undocumented
Fix: Add Javadoc with `@param size` documenting sliding window width
[MA-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/rtls/MovingAverage.java | Line: 16-23
Description: `next(double val)` has no Javadoc; adds value to window, evicts oldest if full, returns current average with no `@param` or `@return`
Fix: Add Javadoc with `@param val` and `@return` documenting value insertion and running average return
[PT-01] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/rtls/Points.java | Line: 5
Description: No class-level Javadoc; core data class coordinate system (local Cartesian? lat/lon?) and weight meaning (count? signal strength?) are undocumented
Fix: Add class-level Javadoc specifying coordinate system, weight semantics, and role in RTLS spatial operations
[PT-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/Points.java | Line: 12-56
Description: All 14 getter/setter methods and 2 constructors lack Javadoc
Fix: Add Javadoc to all public methods documenting parameter and return semantics
[SB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/SessionBean.java | Line: 7
Description: No class-level Javadoc; bean holds vehicle code, date range, and array of points for an RTLS session
Fix: Add class-level Javadoc describing RTLS session DTO purpose
[SB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/SessionBean.java | Line: 17-45
Description: All 8 getter/setter methods lack Javadoc; abbreviated names st_dt and to_dt are unclear
Fix: Add Javadoc to all methods clarifying st_dt=start date and to_dt=end date
[SK-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/ShockBean.java | Line: 6
Description: No class-level Javadoc; bean represents a shock/impact event for a vehicle with undocumented "shock" concept
Fix: Add class-level Javadoc describing shock/impact sensor event DTO
[SK-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/ShockBean.java | Line: 17-48
Description: All 11 getter/setter methods lack Javadoc
Fix: Add Javadoc to all public methods
[SPB-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/SpeedBean.java | Line: 6
Description: No class-level Javadoc; bean stores speed measurement with undocumented units for `speed` (m/s? km/h?) and `interval` (seconds? ms?)
Fix: Add class-level Javadoc specifying speed and interval units
[SPB-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/SpeedBean.java | Line: 17-32
Description: All 6 getter/setter methods lack Javadoc; units unknown
Fix: Add Javadoc to all methods specifying units
[TG-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/Tags.java | Line: 5
Description: No class-level Javadoc; bean represents an RTLS tag (tracking device) with undocumented "tag" concept
Fix: Add class-level Javadoc describing RTLS tracking tag/device DTO
[TG-02] LOW | File: WEB-INF/src/com/torrent/surat/fms6/rtls/Tags.java | Line: 13-22
Description: All 4 getter/setter methods lack Javadoc
Fix: Add Javadoc to all public methods
[ACC-01] INFO | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 52-55
Description: Skeleton Javadoc on `computerThatLonLat()` has bare `@param x` and `@param y` with no descriptions, giving false appearance of documentation
Fix: Either fill in meaningful `@param` descriptions or remove the skeleton tags and write complete Javadoc
[ACC-02] INFO | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 116
Description: Inline comment "the angle to y up direction" is partially misleading; does not explain math-angle-to-compass-bearing conversion with +90 offset
Fix: Rewrite comment to explain conversion from standard math angle (CCW from x-axis) to bearing (CW from north/y-axis)
[ACC-03] INFO | File: WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java | Line: 56
Description: Method name `computerThatLonLat` is a misnomer; "computer" is a noun, "That" adds no clarity; should be `computeLonLat` or `calculateLonLat`
Fix: Rename method to `computeLonLat` or `calculateLonLat` and update all call sites

## Pass 4: Code Quality


### util-A-F

[1a] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 4
Description: Class name uses underscore separator (Dt_Checker) instead of standard Java PascalCase.
Fix: Rename class to DateChecker or DtChecker following PascalCase convention.

[1b] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java | Lines: 1, 9
Description: Class named EncryptTest suggests a unit test but is a production encryption utility; also contains decompiled code.
Fix: Rename to EncryptUtil or CipherHelper and replace decompiled source with clean implementation.

[1c] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 240, 509, 636
Description: Misspelled method names generateRadomName and caculatePercentage/caculateImpPercentage.
Fix: Rename to generateRandomName, calculatePercentage, and calculateImpPercentage.

[1c] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java | Lines: 250, 257, 298
Description: Methods GetDateNow(), GetDate(), GetCalendar() use PascalCase instead of camelCase.
Fix: Rename to getDateNow(), getDate(), getCalendar().

[1c] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 178
Description: Method days_Betn uses underscore and abbreviation violating naming conventions.
Fix: Rename to daysBetween using camelCase.

[2] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Line: N/A
Description: Mixed brace placement (K&R and Allman) with inconsistent indentation.
Fix: Apply uniform brace style and indentation using a code formatter.

[2] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: N/A
Description: Mixed brace styles with tabs and spaces mixed.
Fix: Apply uniform brace style and convert all indentation to consistent tabs or spaces.

[2] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 346-413
Description: Extremely inconsistent indentation in convert_time() with zero indentation inside nested blocks.
Fix: Reformat convert_time() method with consistent indentation.

[2] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: N/A
Description: Minimal indentation, no blank lines between methods, archaic style.
Fix: Reformat with proper indentation and blank line separators between methods.

[2] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java | Line: N/A
Description: Decompiled code style with no meaningful variable names (s, s1, c).
Fix: Replace with clean implementation using descriptive variable names.

[2] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Line: N/A
Description: Deeply nested code (5+ levels) with inconsistent spacing.
Fix: Reduce nesting via early returns/guard clauses and apply consistent formatting.

[2] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Lines: 20-25
Description: Missing access modifiers on fields (package-private by default).
Fix: Add explicit private access modifiers to all fields.

[3a] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: N/A
Description: God class with 1087 lines and 40+ methods spanning date formatting, HTML helpers, math, file I/O, image downloading, and more.
Fix: Decompose into domain-specific utilities (HtmlFormUtil, MathUtil, FileUploadUtil, TimeConversionUtil).

[3b] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 38-517
Description: Single servlet containing HTTP handling, CSV parsing, validation, file upload, email sending, database operations, and firmware push.
Fix: Extract CSV validation, email, and firmware logic into separate service classes.

[4] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 76, 83, 117, 168, 385-386, 395, 938
Description: Multiple blocks of commented-out debug System.out.println statements and dead code.
Fix: Remove all commented-out code.

[4] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 836-837
Description: Dead unreachable block left after return statement inside convertToImpPerc.
Fix: Remove the unreachable code after the return statement.

[4] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Lines: 18-23
Description: Comment block states class is not called by the stored procedure, suggesting the entire class may be dead code.
Fix: Verify the class is unused and remove it, or update the comment if it is in use.

[5] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 37
Description: Duplicate import java.util.ArrayList (already imported at line 17).
Fix: Remove the duplicate import on line 37.

[5] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Line: 2
Description: Unnecessary import java.lang.* which is always implicitly imported.
Fix: Remove the import java.lang.* statement.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Lines: 217-221, 264-268, 307-311
Description: Three catch(Exception e) blocks catch all exceptions, call e.getMessage() as no-op standalone statement.
Fix: Catch specific exceptions, log with Log4j2, and remove the standalone e.getMessage() calls.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 252-257, 294
Description: Broad catch(Exception e) with System.out.println and a TODO marker left in catch(SQLException e).
Fix: Catch specific exceptions, log properly with Log4j2, and remove the TODO stub.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Lines: 150-154, 195-199
Description: Two catch(Exception e) blocks with e.printStackTrace() and no-op e.getMessage().
Fix: Catch specific exceptions and log with Log4j2.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Lines: 166-169, 215-219
Description: Two catch(Exception e) blocks with e.printStackTrace() and no-op e.getMessage().
Fix: Catch specific exceptions and log with Log4j2.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Lines: 252-254
Description: Broad catch(Exception e) with e.printStackTrace() and no-op e.getMessage().
Fix: Catch specific exceptions and log with Log4j2.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Lines: 56-58, 79-81, 100-102, 123-126
Description: Four separate catch(Exception e){ e.printStackTrace(); } blocks swallowing all exceptions.
Fix: Catch specific exceptions and log with Log4j2.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 747-749, 893-895
Description: Broad catches with only e.printStackTrace() and no recovery.
Fix: Catch specific exceptions, log with Log4j2, and handle or rethrow appropriately.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java | Lines: 25, 64, 200, 219, 241, 313, 353
Description: Multiple exception catches logged only via System.out.println then swallowed.
Fix: Replace System.out.println with Log4j2 logging and handle exceptions properly.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Lines: 220, 267, 310
Description: e.getMessage() called as standalone statement with return value discarded (no-op).
Fix: Remove the standalone e.getMessage() calls or capture for logging.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Lines: 153, 198
Description: e.getMessage() called as standalone statement with return value discarded (no-op).
Fix: Remove the standalone e.getMessage() calls or capture for logging.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Lines: 169, 218
Description: e.getMessage() called as standalone statement with return value discarded (no-op).
Fix: Remove the standalone e.getMessage() calls or capture for logging.

[6] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Line: 254
Description: e.getMessage() called as standalone statement with return value discarded (no-op).
Fix: Remove the standalone e.getMessage() call or capture for logging.

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Lines: 219, 266, 309
Description: Three e.printStackTrace() calls writing to stderr instead of application logging framework.
Fix: Replace with log.error() using Log4j2.

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 171-174, 254, 295
Description: Three instances of e.printStackTrace() or System.out.println exception logging despite Log4j2 being imported.
Fix: Replace with log.error() using the existing Log4j2 logger.

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 748, 894
Description: Two e.printStackTrace() calls writing to stderr instead of using a logging framework.
Fix: Add Log4j2 logger and replace with log.error().

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java | Lines: 25, 354
Description: Exception handling via System.out.println and e.printStackTrace() instead of proper logging.
Fix: Add Log4j2 logger and replace all exception output with log.error().

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Lines: 152, 197
Description: Two e.printStackTrace() calls writing to stderr.
Fix: Add Log4j2 logger and replace with log.error().

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Lines: 168, 217
Description: Two e.printStackTrace() calls writing to stderr.
Fix: Add Log4j2 logger and replace with log.error().

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Lines: 57, 80, 101, 125
Description: Four e.printStackTrace() calls writing to stderr.
Fix: Add Log4j2 logger and replace with log.error().

[7] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Lines: 214, 222, 253
Description: Three e.printStackTrace() calls writing to stderr.
Fix: Add Log4j2 logger and replace with log.error().

[8] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Line: 16
Description: Static SimpleDateFormat instance shared across threads is not thread-safe.
Fix: Replace with ThreadLocal or use java.time.format.DateTimeFormatter which is thread-safe.

[9a] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 329-344
Description: InputStream and OutputStream in saveImage() not wrapped in try-with-resources; both leak if exception occurs.
Fix: Wrap both streams in try-with-resources block.

[9b] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 918-934
Description: InputStream from filePart.getInputStream() never closed; OutputStream not closed on exception.
Fix: Wrap both streams in try-with-resources block.

[9c] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 936-959
Description: OutputStream never closed at all and InputStream never closed in uploadDocumentFile().
Fix: Wrap both streams in try-with-resources block.

[9d] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 322-353
Description: BufferedReader in read() method is never closed; no try-with-resources or finally block.
Fix: Wrap BufferedReader in try-with-resources block.

[9e] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Lines: 107-127
Description: FileInputStream in downloadExcel() not closed if exception occurs during read loop.
Fix: Wrap FileInputStream in try-with-resources block.

[10a] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 355, 378, 407, 445, 465, 484
Description: Six private validation methods are never called.
Fix: Remove all six unused private methods.

[10b] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Lines: 18-23
Description: Entire class is potentially dead code per comment stating stored procedure does not call it.
Fix: Verify with database team and remove class if confirmed unused.

[10c] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Lines: 6-7, 234
Description: Static mutable fields are thread-unsafe, field beanName appears unused, and init() method is empty.
Fix: Remove unused field beanName and empty init() method; refactor static fields to local variables.

[10d] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 309, 311
Description: Local variable partHeader assigned but never used.
Fix: Remove the unused partHeader variable.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Lines: 77, 83, 95, 154
Description: Magic numbers 0, 1, 2, 7, 13 used for alert status codes and day/length thresholds with no named constants.
Fix: Extract to named constants.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 349
Description: Division by 10 to convert "milliseconds" to seconds is suspicious (should be 1000).
Fix: Verify and correct the divisor to 1000.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 354
Description: Magic number 86400 (seconds in a day) used without a named constant.
Fix: Extract to a named constant SECONDS_PER_DAY = 86400.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 696-706
Description: Magic numbers 25, 5, 6 used as hour thresholds for colour status.
Fix: Extract to named constants describing the threshold meaning.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 815-833
Description: Magic numbers 100, 150, 50, 67, 33 used in impact percentage calculations.
Fix: Extract to named constants.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 1056
Description: Hardcoded customer ID "26" and user ID "166207" for Visy-specific filtering.
Fix: Move IDs to configuration or database lookup.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Line: 141
Description: Hardcoded relative path traversal "../../../../../../../../excelrpt/" with magic depth.
Fix: Replace with configurable base path resolved from application context.

[11] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Lines: 113, 204
Description: Magic numbers 3 and 50 for substring length and padding length.
Fix: Extract to named constants with descriptive names.

[12a] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 55, 108, 163, 219
Description: Hardcoded FTP hostname, port, username, password in plain text, plus hardcoded email addresses and absolute file path.
Fix: Move all credentials and paths to externalized configuration and remove from source code.

[12b] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Line: 229
Description: FTP credentials loaded from config but assembled into plain-text command string sent to device outgoing queue.
Fix: Encrypt or secure the credential transmission channel.

[12c] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 919, 937, 1056, 1073-1077, 1085
Description: Hardcoded Linux paths and customer/user IDs with comment "hard-coded for the meantime".
Fix: Move all paths to externalized configuration and IDs to database-driven lookup.

[13] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Lines: 41-45, 54-67, 79, 85, 106, 115, 124, 147, 165, 174, 184, 207, 244-248, 291-295
Description: All SQL built via string concatenation with Statement in checkDueDate(), getAlertlist(), getCustGroupList().
Fix: Replace all with PreparedStatement using parameterized queries.

[13] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Lines: 70-86, 105-106, 114, 123, 134, 144, 175-179
Description: All SQL built via string concatenation with Statement.
Fix: Replace all with PreparedStatement using parameterized queries.

[13] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java | Lines: 37, 74-80, 125, 143, 161, 195-199
Description: All SQL built via string concatenation with Statement.
Fix: Replace all with PreparedStatement using parameterized queries.

[13] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Lines: 77-84, 99-101, 230-231, 235-236, 242-243, 246
Description: All SQL built via string concatenation with Statement.
Fix: Replace all with PreparedStatement using parameterized queries.

[13] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 219-234
Description: Uses PreparedStatement for SELECT but string concatenation for INSERT statements.
Fix: Replace all concatenated INSERT statements with PreparedStatement.

[13] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java, DriverExpiryAlert.java, DriverMedicalAlert.java | Lines: Multiple
Description: Email content concatenated directly into INSERT SQL for email_outgoing table; single quotes in content break SQL or enable injection.
Fix: Use PreparedStatement with parameterized queries for all email INSERT operations.

[14] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/BeanComparator.java | Lines: 19, 69
Description: Raw type Comparator and Class without generic parameters.
Fix: Add generics: implements Comparator<Object> and Class<?>.

[14] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 60, 104
Description: Raw type ArrayList used as method parameter without generic type.
Fix: Add generics: ArrayList<String> or appropriate parameterized type.

[14] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java | Lines: 43-44, 58-61
Description: Six raw ArrayList declarations.
Fix: Add appropriate generic type parameters.

[14] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java | Lines: 27, 37, 65, 87
Description: Raw types Class[] and Class without generic wildcards.
Fix: Change to Class<?>[] and Class<?>.

[14] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Line: 106
Description: Diamond operator missing on right side.
Fix: Add diamond operator: new ArrayList<>().

[15] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java | Lines: 142, 203
Description: Variable subsject misspelled (should be subject).
Fix: Rename subsject to subject.

[15] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java | Lines: 40, 141, 144
Description: Variable subsject misspelled (should be subject).
Fix: Rename subsject to subject.

[15] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Line: 240
Description: Method generateRadomName misspelled.
Fix: Rename to generateRandomName and update all callers.

[15] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java | Lines: 509, 636
Description: Methods caculatePercentage and caculateImpPercentage misspelled.
Fix: Rename to calculatePercentage and calculateImpPercentage.

[15] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java | Lines: 445, 465
Description: Methods validateQuestionLenght and validateQuestionLenghtTab misspelled.
Fix: Rename to validateQuestionLength and validateQuestionLengthTab.

[15] LOW | File: WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java | Line: 300
Description: Variable arrCanlendar misspelled (should be arrCalendar).
Fix: Rename to arrCalendar.

[16] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Lines: 141-150
Description: Leap-year logic uses y%1000 instead of y%100, and returns are inverted -- years like 1900 wrongly treated as leap, 2000 wrongly treated as non-leap.
Fix: Replace with correct logic or use java.time.Year.isLeap().

[16] HIGH | File: WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java | Lines: 6-7
Description: Static mutable fields written by first() and last() methods cause thread-safety corruption under concurrent access.
Fix: Refactor static fields to local variables or method return values.

[17] CRITICAL | File: WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java | Line: entire file
Description: Home-rolled trivial character-shift cipher with no key, IV, or standard algorithm; decompiled from 2006 third-party tool; provides no real cryptographic protection.
Fix: Replace with standard javax.crypto AES encryption and audit all callers.

### util-G-Z

[1.1] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java, escapeSingleQuotes.java, fix_department.java, mail.java, password_life.java, password_policy.java, send_timezone.java, send_updatepreop.java | Line: N/A
Description: 8 of 24 files (33%) use non-standard lowercase/snake_case class names instead of PascalCase.
Fix: Rename classes to PascalCase (e.g., call_mail -> CallMail, fix_department -> FixDepartment).

[1.2] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java, LogicBean_filter1.java, GdprDataDelete.java, send_timezone.java, send_updatepreop.java, fix_department.java, call_mail.java, mail.java, InfoLogger.java | Line: various
Description: Multiple classes use non-camelCase method names (PascalCase, snake_case, or inconsistent casing).
Fix: Rename methods to camelCase.

[1.3] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java, LogicBean_filter1.java, Menu_Bean.java, Menu_Bean1.java | Line: N/A
Description: Underscore-separated class names with numeric suffixes suggest copy-paste versioning rather than proper inheritance.
Fix: Refactor into properly named classes using inheritance or parameterization.

[2.1] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java | Line: 1-2692
Description: God class at 2,692 lines with single doPost() method containing all import logic for 5+ distinct workflows in massive if/else blocks.
Fix: Refactor into strategy-pattern handlers per import type.

[2.2] High | File: WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java | Line: 1-1454
Description: God class at 1,454 lines with deeply nested DB queries and HTML generation for email sending.
Fix: Decompose into smaller classes separating DB access, HTML generation, and email dispatch.

[2.3] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java, send_timezone.java | Line: 1-601, 1-417
Description: Both contain long, deeply nested methods with duplicated JNDI lookup, query execution, and resource cleanup patterns.
Fix: Extract common JNDI lookup and resource cleanup into shared utility methods.

[3.1] High | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java, Menu_Bean1.java | Line: all
Description: ~85% code duplication between Menu_Bean and Menu_Bean1.
Fix: Consolidate into a single parameterized class.

[3.2] High | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java, LogicBean_filter1.java | Line: 1-180
Description: First ~180 lines are copy-pasted verbatim between filter and filter1.
Fix: Consolidate into a single class with optional sort/aggregate functionality.

[3.3] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java, password_policy.java | Line: all
Description: Decompiled classes from 2006 with identical structure differing only in the SQL query.
Fix: Merge into a single class with parameterized query or use inheritance.

[3.4] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/mail.java | Line: 41-107
Description: mail.Ename() performs a full DB query then ignores the result, returning the same LindeConfig values -- DB query is dead code.
Fix: Remove the dead DB query or consolidate both Ename() methods.

[4.1] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/PurgeData.java | Line: 1-5
Description: Completely empty class with no methods, fields, or functionality.
Fix: Delete PurgeData.java.

[4.2] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java | Line: 7-11, 41-72
Description: Large block of commented-out code for getHTML1() using Apache HttpClient plus commented-out imports.
Fix: Remove all commented-out code and unused imports.

[4.3] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java | Line: 84, 91, 120-123, 131, 151, 165-168
Description: Dozens of commented-out System.out.println debug statements and commented-out blocks.
Fix: Remove all commented-out debug statements and dead code blocks.

[4.4] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java | Line: 392
Description: Commented-out conn.close() is dead code since a finally block was added later.
Fix: Remove the commented-out conn.close() line.

[4.5] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java, Menu_Bean1.java | Line: 165-172, 152-159
Description: Both files contain large commented-out SQL queries in fetchSubModule().
Fix: Remove all commented-out legacy SQL queries.

[4.6] High | File: WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java | Line: 87-88
Description: Same INSERT INTO outgoing statement is executed twice consecutively, causing duplicate outgoing messages (bug).
Fix: Remove the duplicate stmte1.executeUpdate(query) call on line 88.

[5.1] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 18-20, 29-30, 54-55, 86-88
Description: Multiple hardcoded credentials including DB user/pass, firmware password, test credentials, and Clickatell SMS API credentials in source code.
Fix: Externalize all credentials to environment variables, JNDI, or encrypted configuration store.

[5.2] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java | Line: 22, 31, 34, 56
Description: Hardcoded server URLs, email addresses, and file paths in source code.
Fix: Externalize all configuration values to XML or environment configuration.

[5.3] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java | Line: 524-528
Description: FTP credentials embedded in a message string stored in plaintext in the outgoing database table.
Fix: Use secure credential retrieval at FTP execution time instead of embedding credentials in database records.

[5.4] High | File: WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java | Line: 180
Description: SMS API credentials passed as URL query parameters which may be logged by proxies and servers.
Fix: Use HTTP POST body or authorization headers instead of query parameters.

[6.1] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: 67, 73
Description: SQL queries constructed via string concatenation with unsanitized cust_cd and driver_cd values.
Fix: Replace with PreparedStatement parameterized queries.

[6.2] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java | Line: 59, 64-65
Description: SQL queries for SELECT and INSERT constructed via string concatenation with unsanitized values.
Fix: Replace with PreparedStatement parameterized queries.

[6.3] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java, LogicBean_filter1.java | Line: 122-123, 146-150
Description: SQL queries constructed via string concatenation with unsanitized set_gp_cd and weig_id values.
Fix: Replace with PreparedStatement parameterized queries.

[6.4] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java, Menu_Bean1.java | Line: 77, 80, 88
Description: SQL queries and manual IN() clause construction via string concatenation.
Fix: Replace with PreparedStatement parameterized queries.

[6.5] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java | Line: various
Description: All three methods construct queries with concatenated parameters.
Fix: Replace with PreparedStatement parameterized queries.

[6.6] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java | Line: 69
Description: INSERT into email_outgoing constructed via string concatenation with unsanitized email, subject, and message values.
Fix: Replace with PreparedStatement parameterized queries.

[6.7] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: 42-48, 121, 131, 142, 148, 156, 159, 165, 168, 174, 177, 183, 186
Description: Extensive string-concatenated queries throughout show_cust_dept() and fix_dept() methods.
Fix: Replace with PreparedStatement parameterized queries.

[6.8] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java | Line: 86
Description: SQL query constructed via string concatenation with unsanitized webUserCD value.
Fix: Replace with PreparedStatement parameterized queries.

[6.9] Critical | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java, password_policy.java | Line: 76
Description: SQL queries constructed via string concatenation with unsanitized userid value.
Fix: Replace with PreparedStatement parameterized queries.

[7.1] High | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java | Line: 180-210
Description: Connection never closed on exception path in init() -- conn.close() only in happy path with no finally block.
Fix: Add a finally block to ensure conn.close() is called regardless of exception.

[7.2] High | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java, password_policy.java | Line: 143-167, 115-139
Description: Both init() methods close connection only in happy path with no finally block.
Fix: Add finally blocks to ensure connection close on all code paths.

[7.3] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java | Line: 16-38, 74-104
Description: BufferedReader and HttpURLConnection only closed in happy path; exception path leaks resources.
Fix: Add finally blocks or use try-with-resources.

[7.4] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java | Line: 18-22, 67, 73-82
Description: Instance fields conn and stmt opened in writelog() but stmt is never explicitly closed and ResultSet rset is never closed.
Fix: Close stmt and rset explicitly in a finally block or use try-with-resources.

[7.5] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: 7, 19, 30
Description: Unused import (Frm_excel), raw ArrayList type, and field rs declared but never populated.
Fix: Remove unused import, add generic type parameter, and remove or populate the rs field.

[7.6] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java | Line: 316
Description: e.getMessage() called but return value discarded in catch block.
Fix: Remove the unused e.getMessage() call or assign for logging.

[7.7] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java | Line: 79
Description: e.getMessage() called but return value discarded in catch block.
Fix: Remove the unused e.getMessage() call or assign for logging.

[8.1] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/ (all 24 files) | Line: various
Description: 48 occurrences of catch(Exception e) across all files instead of catching specific exceptions.
Fix: Replace broad catches with specific exception types.

[8.2] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/ (22 of 24 files) | Line: various
Description: 59 occurrences of e.printStackTrace() sending unstructured stack traces to System.err.
Fix: Replace e.printStackTrace() with structured logging using Log4j2 or SLF4J.

[8.3] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/ (22 of 24 files) | Line: various
Description: 270 occurrences of System.out.print across files with no log levels, rotation, or structured output.
Fix: Replace System.out.println with a structured logging framework.

[8.4] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java, send_timezone.java, fix_department.java | Line: various
Description: Finally blocks catch SQLException and print to System.out but take no corrective action.
Fix: Log swallowed exceptions at appropriate level using a logging framework.

[9.1] High | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: 72-97
Description: Multi-table deletes from 9+ tables per driver in a loop with no transaction boundary.
Fix: Wrap all delete operations in a transaction with conn.setAutoCommit(false), commit on success, rollback on failure.

[9.2] High | File: WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java | Line: 60-311
Description: Multi-table operations without transaction boundaries.
Fix: Wrap all DML statements in a transaction.

[9.3] High | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: 139-263
Description: Updates to 11+ tables to reassign department codes with no transaction boundary (13 update statements).
Fix: Wrap all update operations in a transaction.

[9.4] High | File: WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java | Line: 48-98, 222-309, 362-416
Description: Delete-then-insert sequences across multiple tables without transactions in all three methods.
Fix: Wrap each method's DML operations in a transaction.

[9.5] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java | Line: 69-73
Description: Insert into email_outgoing then update FMS_USR_MST without transaction; failed update leaves orphaned email record.
Fix: Wrap insert and update in a transaction.

[10] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/ (13 of 24 files) | Line: various
Description: 13 files contain unused imports including java.lang.*, java.io.*, PrintStream, HttpSession, Properties, Frm_excel, etc.
Fix: Remove all unused imports using IDE auto-cleanup.

[11] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/ (10 files) | Line: various
Description: Raw ArrayList usage without type parameters across 10 files causing compiler warnings.
Fix: Add generic type parameters to all ArrayList declarations.

[12.1] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java, Menu_Bean1.java, call_mail.java, password_life.java, password_policy.java | Line: various
Description: Deeply inconsistent indentation and brace style including mixed tabs and spaces and decompiled code whitespace.
Fix: Apply consistent formatting using an IDE auto-formatter.

[12.2] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java, LogicBean_filter1.java, password_life.java, password_policy.java, Menu_Bean.java, Menu_Bean1.java | Line: various
Description: Inconsistent field visibility -- package-private fields that should be private.
Fix: Make all fields private and add getter/setter methods where access is needed.

[12.3] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/password_life.java | Line: 1
Description: Decompiled code artifact header from DJ v3.9.9.91 (2006) indicating original source was lost.
Fix: Remove decompiler header comments and consider rewriting these classes from scratch.

[13.1] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java | Line: 110
Description: Error message references "send_timezone() Method" but actual method is call_gdpr_delete_data().
Fix: Correct error message to reference the actual method name.

[13.2] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java | Line: 64, 276
Description: Error messages reference "send_timezone() Method" but actual methods are show_cust_dept() and fix_dept() (copy-paste error).
Fix: Correct error messages to reference the actual method names.

[13.3] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java, LogicBean_filter1.java | Line: 208, 398
Description: Error message references "LogicBean_LoginAlerter" but actual class is LogicBean_filter.
Fix: Correct error messages to reference the actual class name.

[13.4] Low | File: WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java | Line: 58
Description: Variable name "subsject" is a typo of "subject".
Fix: Rename variable from "subsject" to "subject".

[14] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java | Line: 27-130, 132-251, 254-416
Description: Three near-duplicate methods with identical JNDI lookup, connection management, and resource cleanup blocks copy-pasted three times.
Fix: Extract common JNDI lookup and resource cleanup into a shared template method.

[15.1] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java | Line: 20-46
Description: 20+ mutable public static non-final fields modifiable by any thread creating race condition risk.
Fix: Make fields private with synchronized accessors, or use an immutable configuration object.

[15.2] Medium | File: WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java | Line: 5-127
Description: Dozens of mutable public static fields modifiable by any thread.
Fix: Make fields private with synchronized accessors, or use an immutable configuration object.

### bean-A-D

[A01-01] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java | Line: all (also BroadcastmsgBean, CanruleBean, DailyUsageDeptDataBean, DayhoursBean, DehireBean, DetailedReportUtil, DriverBean, DriverImportBean)
Description: Pervasive snake_case naming in getter/setter methods across 9 of 14 audited bean files violates Java Bean camelCase conventions.
Fix: Adopt camelCase naming for new code; retrofitting existing code requires coordinated changes with all consumers.

[A01-02] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java | Line: 11-33 (also DayhoursBean, DriverBean, DetailedReportUtil, CustomerBean, CustLocDeptBean)
Description: Fields declared with package-private (default) visibility instead of private, allowing any same-package class to bypass getters/setters.
Fix: Change all bean fields to private to properly encapsulate internal state.

[A01-03] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 8-29
Description: All 20 ArrayList fields and constructor parameters use raw types without generics.
Fix: Add appropriate type parameters to all collections and their associated method signatures.

[A01-04] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 11-15
Description: Five ArrayList fields use raw-type constructors (diamond operator missing).
Fix: Use the diamond operator: new ArrayList<>().

[A01-05] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 39-41
Description: Parameterized constructor prints debug information to stdout using System.out.println().
Fix: Remove debug statements or replace with proper logging.

[A01-06] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 44-53
Description: The analyzeAndCombine() method iterates over field names checking for substrings but the if-block body is completely empty -- dead code or abandoned stub.
Fix: Either implement the intended logic or remove the method entirely.

[A01-07] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 57-59
Description: Three lines of commented-out System.out.println debug statements in arrangeData().
Fix: Remove the commented-out code.

[A01-08] INFO | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 5
Description: The java.util.Arrays import appeared potentially unused but is actually used on line 61.
Fix: WITHDRAWN -- the import is in active use; no action required.

[A01-09] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 29-30, 43-44, 103-104
Description: DailyUsageDeptDataBean objects are instantiated then immediately overwritten by assignment from a list.
Fix: Replace with direct assignment from the list.

[A01-10] LOW | File: CanruleBean, CustLocDeptBean, CustomerBean, DashboarSubscriptionBean, DehireBean, DetailedReportUtil, DriverLeagueBean | Line: class declarations
Description: Seven beans do not implement Serializable while seven others do, creating an inconsistent pattern.
Fix: Establish a consistent policy; all session-eligible beans should implement Serializable with serialVersionUID.

[A01-11] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java | Line: 3
Description: Class name DashboarSubscriptionBean is missing the letter 'd' -- should be DashboardSubscriptionBean.
Fix: Rename class and file to DashboardSubscriptionBean, updating all references.

[A01-12] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DriverBean.java | Line: 5
Description: DriverBean implements Serializable but does not declare a serialVersionUID.
Fix: Add private static final long serialVersionUID.

[A01-13] LOW | File: Multiple files across the bean package | Line: various
Description: Inconsistent String field initialization defaults -- some use "" (empty string), some use null, some use implicit null.
Fix: Adopt a consistent default initialization strategy for String fields across all beans.

[A01-14] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 27-36, 101-111
Description: getModelList() and getWeekList() are named as getters but mutate internal fields by appending entries without clearing.
Fix: Rename to buildModelList()/buildWeekList() or refactor to return a new list without modifying internal state.

[A01-15] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java | Line: 39-67
Description: DailyUsageHourBean contains significant business logic in arrangeData(), mixing data representation with processing.
Fix: Extract arrangeData(), getModelList(), and getWeekList() logic into a separate service or utility class.

[A01-16] MEDIUM | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: all
Description: DetailedReportUtil has 20 parallel ArrayList fields with 40 getters/setters plus constructors and business methods (43 public members total), constituting a God class.
Fix: Refactor parallel arrays into a typed collection of a structured inner class.

[A01-17] LOW | File: WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java | Line: 57-164 (also DailyUsageDeptDataBean, DailyUsageHourBean)
Description: Multiple beans return direct references to internal mutable ArrayList fields via getters.
Fix: Return unmodifiable views or defensive copies from getters.

[A01-18] INFO | File: WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageDeptDataBean.java | Line: 55-60 (also DailyUsageHourBean, DetailedReportUtil)
Description: All collection-typed method parameters and return types use concrete ArrayList class rather than the List interface.
Fix: Use List interface in method signatures.
