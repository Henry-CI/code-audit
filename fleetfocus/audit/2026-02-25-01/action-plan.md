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
