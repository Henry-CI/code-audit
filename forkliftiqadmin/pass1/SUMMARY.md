# Pass 1: Security Audit Summary — forkliftiqadmin
**Date:** 2026-02-26
**Run:** 01
**Branch audited:** master
**Audit framework:** AUDIT-FRAMEWORK_legacy.md
**Pass:** 1 — Source Code Security Review

---

## Executive Summary

The `forkliftiqadmin` application (internal name: **pandora**, Maven artifact: `pandoraAdmin`, Tomcat context: `/BHAG`) is a multi-tenant fleet safety management platform built on Apache Struts 1.3.10 and PostgreSQL. This pass reviewed the full application source — approximately 350 Java source files, 100+ JSP templates, and all configuration XML — across 35 primary audit agents covering every package.

**The application is in a critically insecure state.** Every major web application vulnerability category is present. The most severe findings are not isolated edge cases; they are architectural patterns replicated across the entire codebase. A determined attacker with a valid account (or in several cases no account at all) could:

- Extract the complete database of all tenants via SQL injection
- Execute arbitrary operating system commands via path traversal in the barcode upload endpoint
- Access fleet GPS locations, job records, and driver PII for any tenant (IDOR, no comp_id scoping)
- Recover all user and driver passwords (unsalted MD5, rainbow-table crackable)
- Send arbitrary emails from the platform to any address (unauthenticated `mailer.do`)
- Create new company accounts without authentication (`adminRegister.do` open to the Internet)
- Escalate privilege silently (MenuDAO privilege escalation, no RBAC in base Action class)

---

## Scope

| Item | Value |
|------|-------|
| Files audited | ~350 Java source files, ~100 JSPs, 5 config XMLs |
| Packages covered | All `com.*` packages plus WEB-INF config |
| Auth gate | `PreFlightActionServlet` extending Struts `ActionServlet` |
| Framework | Apache Struts 1.3.10 + Spring-web 4.0.2 (no Spring Security) |
| Database | PostgreSQL (via JDBC `Statement` / `PreparedStatement`) |
| Auth backend | AWS Cognito (sidecar at `http://localhost:9090`) |
| Report files | 100+ individual file-level report `.md` files in this directory |

---

## Finding Totals (from audited file reports)

Counts are drawn from the 35 batched-report files covering the highest-risk source files. Individual administrative JSP and ActionForm reports contribute additional findings not fully enumerated here.

| Severity | Count (known reports) | Notes |
|----------|----------------------|-------|
| **CRITICAL** | ~83 | Directly exploitable without chaining |
| **HIGH** | ~154 | Exploitable with session or minimal access |
| **MEDIUM** | ~152 | Exploitable under specific conditions |
| **LOW** | ~94 | Defence-in-depth or pattern concerns |
| **INFO** | ~80 | Informational / context notes |
| **TOTAL** | **~563** | Across 35 batched report files |

> Note: totals are additive across reports and may double-count instances of the same systemic pattern (e.g. the SQL injection pattern appears in ~30 DAOs and is counted per DAO rather than once).

---

## Critical Findings — Detail

### C-1 — Systemic SQL Injection via `Statement` + String Concatenation

**Severity:** CRITICAL
**Scope:** Entire DAO layer (~30+ affected methods identified)

The application's primary database access pattern uses `java.sql.Statement` with string concatenation rather than `PreparedStatement` with bind parameters. Affected DAOs confirmed during this audit include:

- `JobsDAO.getJobList`, `getJobListByJobId` — `equipId`, `jobNo` from request
- `ManufactureDAO.getManufactureById`, `checkManuByNm`, `getManu_type_fuel_rel` — manufacturer IDs from request
- `MenuDAO.getAllMenu`, `getRoleMenu` — language code and role list from request
- `MenuDAO.saveRoleMenu`, `delRoleMenu` — **role and menu IDs from request — privilege escalation via INSERT/DELETE**
- `QuestionDAO.delQuestionById`, `getQuestionById`, `getQuestionByUnitId`, `getQuestionContentById`
- `UnitDAO.getUnitBySerial`, `delUnitById`, `getType`, `getPower`, `getUnitNameByComp`, `getTotalUnitByID`
- `GPSDao.getGPSLocations` — unit IDs array from request (auth-excluded endpoint)
- `SubscriptionDAO.checkCompFleetAlert`, `getAllReport` — frequency and compId
- `DriverDAO.getDriverByNm`, `getDriverByFullNm`, `getAllDriverSearch` (second-order)
- `ResultDAO.saveResult`, `checkDuplicateResult`, `getChecklistResultInc`
- `FormBuilderDAO.getLib` — form library ID
- `ImpactReportDAO` — `%s`/`String.format` in REPORT_QUERY
- `LoginDAO.checkCompFleetAlert`, `saveDefualtSubscription`

Many of these methods are reachable from auth-excluded endpoints (see C-4 through C-8 below), making them unauthenticated SQL injection vulnerabilities. All confirmed via direct source read; no inference required.

**Exploit:** HTTP request parameter → `getParameter()` → string concatenation into SQL → `Statement.executeQuery()`. Blind/union/error-based injection depending on result handling.

---

### C-2 — Second-Order SQL Injection via Session-Stored Timezone

**Severity:** CRITICAL
**File:** `DriverDAO.java:358` (`getAllDriverSearch`), `DriverDAO.java:749` (`getTotalDriverByID`)

`TimezoneDAO` reads the `zone` column from the `timezone` table and stores it in `sessTimezone`. `DriverDAO` concatenates this session value directly into `timezone('...',...)` SQL function calls with no parameterisation or allow-list check. Any administrator with write access to the `timezone` table can inject SQL that fires on every authenticated search request.

---

### C-3 — Insecure Java Deserialization (`FormLibraryBean`)

**Severity:** CRITICAL
**File:** `FormLibraryBean.java`

Uses `ObjectInputStream.readObject()` with no class filter (no `ObjectInputFilter`, no allowlist). Deserialising attacker-controlled bytes allows arbitrary code execution on the JVM. The gadget chain depends on classpath contents (Spring, Commons Collections, etc. are present).

---

### C-4 — `mailer.do` — Unauthenticated Bulk Email + SQL Injection

**Severity:** CRITICAL
**Files:** `PreFlightActionServlet.java:105`, `MailerAction.java`, `SubscriptionDAO.java:38-43`

`mailer.do` is explicitly excluded from the auth gate. Any anonymous HTTP client can:
1. Trigger report generation and bulk email dispatch to all company subscribers.
2. Exploit SQL injection in `SubscriptionDAO.getAllReport()` — the `frequency` parameter is concatenated into a raw `Statement` query with no authentication required.

Additionally, `MailerAction` hardcodes admin credentials for the internal PDF API: `"admin_password":"ciiadmin","username":"hui"` (logged in plaintext on failure).

---

### C-5 — `adminRegister.do` — Unauthenticated Company Account Creation

**Severity:** CRITICAL
**Files:** `PreFlightActionServlet.java`, `AdminRegisterAction.java`, `struts-config.xml`

`adminRegister.do` is auth-excluded. Any anonymous user can POST to create a new company account in Cognito and the application database. No CAPTCHA, rate limit, or invitation token. The `validation.xml` form name mismatch (`adminRegisterActionForm` vs `adminRegActionForm`) means all field validation is silently skipped.

---

### C-6 — `loadbarcode.do` — Unauthenticated Fleet Record Write

**Severity:** CRITICAL
**Files:** `PreFlightActionServlet.java`, `BarCodeAction.java`, `struts-config.xml`

`loadbarcode.do` is auth-excluded. It accepts raw checklist data, resolves company/unit from a serial number, and writes inspection results to the database for any tenant. It also triggers alert emails. No form bean, no validation, no authentication.

---

### C-7 — `api.do` — Unauthenticated Mobile API (One Uncomment from Exploitation)

**Severity:** CRITICAL
**Files:** `AppAPIAction.java`, `struts-config.xml`, `PreFlightActionServlet.java`

`api.do` is excluded from the auth gate. The full mobile API body (login, enumerate all drivers, enumerate all vehicles, submit inspection results, generate PDFs) is currently commented out with `////` prefixes. The Struts route, action mapping, and XML view are all live. If the comment block is removed, all six API operations become immediately available to anonymous Internet users. Today the endpoint crashes with `NullPointerException` at `apiXml.jsp:13`.

---

### C-8 — `goResetPass.do` — Pre-Auth Password Reset Targeting Any Account

**Severity:** CRITICAL
**Files:** `GoResetPassAction.java`, `PreFlightActionServlet.java`

`goResetPass.do` is auth-excluded. Accepts a `username` parameter and dispatches a Cognito password reset for that account. No rate limit, no token binding, no CAPTCHA. Any anonymous caller can trigger a password reset for any known username, enabling account takeover via email interception or Cognito abuse.

---

### C-9 — `PreFlightActionServlet` Auth Gate Bypass via `endsWith()`

**Severity:** CRITICAL
**File:** `PreFlightActionServlet.java`

The auth exclusion check uses `path.endsWith("login.do")`, `path.endsWith("mailer.do")`, etc. The `endsWith()` check matches any path that terminates with the exclusion string. An attacker-controlled request to `/evil/fakelogin.do` passes the auth check and is forwarded to the actual `login.do` action. Depending on Struts routing behaviour, this can be used to reach auth-excluded actions via constructed paths that bypass WAF rules or IP allowlists targeting the literal excluded paths.

Additionally, the method is named `excludeFromFilter()` but returns `true` to *include* the path in the security check and `false` to exclude it — the semantics are inverted relative to the name, creating a maintenance hazard with safety-critical consequences.

---

### C-10 — RCE via Path Traversal in Barcode Filename

**Severity:** CRITICAL
**File:** `BarCode.java` (called from `BarCodeAction.java` / `PrintAction.java`)

`BarCode.java` constructs the output path using the raw `veh_id` parameter:
```
outputPath = baseDir + "../../../../images/barcode/" + veh_id + ".png"
```
No sanitisation of `veh_id` before path construction. An attacker can supply `../../../../WEB-INF/web.xml` (without `.png`) or a known writable path to overwrite arbitrary files within the Tomcat file system. Writing a JSP to the webroot yields remote code execution.

---

### C-11 — Silent Auth Bypass When Cognito Sidecar Throws Exception

**Severity:** CRITICAL
**File:** `LoginAction.java`

If the Cognito REST call throws any exception (network error, timeout, Cognito outage), `LoginAction` catches it and continues to the `success` forward — effectively granting authenticated access to anyone who submits a request while the Cognito sidecar is unavailable. The database-side MD5 hash check is the only gate that fires in the exception path.

---

### C-12 — No RBAC in `PandoraAction` Base Class

**Severity:** CRITICAL
**File:** `PandoraAction.java`

`PandoraAction` is the abstract base class for all action classes. Its `execute()` implementation checks only `sessCompId != null` — i.e., that a company session exists. There is no role check (`sessIsDealer`, `sessIsSuperAdmin`, etc.) in the base class. Every subclass inherits this minimal gate. Role checks exist in approximately a dozen actions but are absent from the majority. A regular operator user can reach administrative endpoints (dealer management, company creation, impact calibration, role-menu assignment) with no access control violation from the framework's perspective.

---

### C-13 — `MenuDAO.saveRoleMenu` / `delRoleMenu` — Privilege Escalation via SQL Injection

**Severity:** CRITICAL
**File:** `MenuDAO.java`

`saveRoleMenu(String roleId, String menuId)` and `delRoleMenu(String roleId, String menuId)` concatenate both parameters into `INSERT` and `DELETE` SQL statements. Any user who can reach `AdminMenuAction` (no role restriction in base class) can:
- Grant any role access to any menu item (INSERT arbitrary rows into `role_menu`)
- Delete all role-menu assignments for any role by injecting into the `DELETE WHERE` clause

---

### C-14 — Hardcoded API Bearer Token in Source Code

**Severity:** CRITICAL
**File:** `HttpDownloadUtility.java:105`

```java
connection.setRequestProperty("X-AUTH-TOKEN", "noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE");
```

This token is transmitted over plain HTTP (the `HttpsURLConnection` line is commented out). The same token also appears in `RegisterAction.java`. Anyone with read access to the repository or build artifacts has this credential.

---

### C-15 — UAT Tomcat Credentials in Committed `settings.xml`

**Severity:** CRITICAL** (also flagged in Pass 0 as P0-3)**
**File:** `settings.xml`

```
TomcatServerUat: username=maven, password=C!1admin
TomcatServerAzure: username=maven, password=pyx1s!96
```

Plaintext credentials committed to version history. Any repository read access yields live server credentials.

---

### C-16 — Unsalted MD5 Password Hashing

**Severity:** CRITICAL
**Files:** `LoginDAO.java`, `CompanyDAO.java`, `DriverDAO.java`, SQL queries throughout

All passwords, driver PINs, and admin PINs are stored using the PostgreSQL `md5()` function with no per-user salt. MD5 is cryptographically broken; modern GPU hardware can compute tens of billions of unsalted MD5 hashes per second; rainbow tables for common passwords are freely available. Any database exfiltration event means every credential is recoverable in minutes.

---

### C-17 — Cross-Tenant IDOR — No `comp_id` Scoping Throughout

**Severity:** CRITICAL (systemic)
**Scope:** ~20+ DAO methods and action classes

Essentially every resource in the application (units, drivers, questions, checklists, GPS records, training records, impact records, job records, subscription records) is identified only by a primary-key ID. DAO methods accept caller-supplied IDs without joining on `comp_id` or verifying ownership against the session's `sessCompId`. Affected classes include:

`UnitDAO` (6+ methods), `QuestionDAO` (all methods), `DriverDAO` (multiple), `ResultDAO` (4+ methods), `JobsDAO`, `TrainingDAO.deleteTraining`, `AdminUnitCalibrationAction`, `DriverJobDetailsAction`, `GPSDao.getGPSLocations`, `ImpactReportAction/DAO`, `FormBuilderDAO`, `LicenceBean write paths`, and more.

Impact: any authenticated user (from any tenant) can read, modify, or delete any other tenant's records by supplying a known primary key.

---

## Systemic Vulnerability Themes

### Theme 1: SQL Injection — Entire DAO Layer

The application was written exclusively using `java.sql.Statement` + string concatenation instead of `PreparedStatement` + bind parameters. While `DBUtil.queryForObject(String, Consumer<PreparedStatement>, ResultMapper)` (the 3-argument overload) does use parameterisation, many callers use the 2-argument overload that accepts a pre-built SQL string, bypassing parameterisation entirely. Every string-typed request parameter that flows to any DAO is a SQL injection point. Finding count: 30+ methods across 15+ DAOs.

**Remediation:** Replace all `Statement` usages with `PreparedStatement`. Enforce via Checkstyle rule `ForbiddenApiCheck` banning `java.sql.Connection#createStatement`.

---

### Theme 2: Authentication-Excluded Endpoints with Critical Functionality

`PreFlightActionServlet.excludeFromFilter()` excludes 8 endpoints from authentication. Of these:

| Endpoint | Risk |
|----------|------|
| `login.do` | Appropriate |
| `goResetPass.do` | CRITICAL — pre-auth account takeover |
| `adminRegister.do` | CRITICAL — unauthenticated tenant creation |
| `mailer.do` | CRITICAL — unauthenticated bulk email + SQLi |
| `loadbarcode.do` | CRITICAL — unauthenticated fleet record write |
| `uploadfile.do` | HIGH — no mapped action (latent risk) |
| `api.do` | CRITICAL — unauthenticated mobile API (commented out but live route) |
| `swithLanguage.do` | MEDIUM — cookie injection, NullPointerException DoS |

Only `login.do` should be excluded. All others require authentication.

---

### Theme 3: Zero Role-Based Access Control

`PandoraAction.execute()` checks `sessCompId != null`. This is the sole access control enforcement point for the entire application. There is no role check at the framework layer. Individual action classes perform ad-hoc `sessIsDealer` / `sessIsSuperAdmin` checks inconsistently. Many administrator-only functions (manufacturer management, menu/role management, unit calibration, driver access revocation) are reachable by any authenticated user of any tenant.

---

### Theme 4: Cross-Tenant IDOR — No Tenant Isolation

The multi-tenant architecture relies on `sessCompId` being present in the session. However, DAO methods generally accept caller-supplied IDs without joining on or verifying `comp_id`. An authenticated attacker from Tenant A can enumerate integer IDs and access Tenant B's data. This affects every major data model (drivers, units, GPS, checklists, training records, job records, impact data, subscription data).

---

### Theme 5: Broken Singleton Pattern (DCL Without `volatile`)

Over 10 DAO/service singletons use double-checked locking without declaring `theInstance` as `volatile`. Under the Java Memory Model, a racing thread may observe a partially-constructed instance. Affected classes include `UnitDAO`, `ManufactureDAO`, `FormBuilderDAO`, `TimezoneDAO`, `ReportService`, `IncidentReportDAO`, and others. This is a production correctness bug as well as a security concern (stale state may include cached credentials or connection objects).

---

### Theme 6: No CSRF Protection Anywhere

Struts 1.x does not add CSRF tokens automatically. The `saveToken()` / `isTokenValid()` API exists in Struts 1 but is never called anywhere in the codebase. Every state-modifying form — including login, logout, password change, role-menu assignment, driver creation, unit calibration, subscription management, company switch — is vulnerable to CSRF. An attacker who can get an authenticated user to visit a malicious page can perform any of these operations on their behalf.

---

### Theme 7: Credential and PII Leakage via Lombok `@Data`

Multiple beans annotated with Lombok `@Data` auto-generate `toString()` methods that include sensitive fields. Logging any of these beans (which happens extensively at DEBUG level) emits credentials and PII to log files:

- `PasswordRequest` — `password`, `oldPassword`, `accessToken`
- `DriverBean` — `pin`, `password`, `cognitoUsername`
- `CompanyBean` — `pass`, `cpass`
- `LicenceBean` — `securityNumber`
- `EmailSubscriptionBean` — 4 × `email_addr`

The `log4j.properties` file additionally sets `log4j.logger.jdbc.sqlonly=DEBUG`, logging all SQL with bound parameters substituted in — meaning MD5-hashed passwords appear in `sql.log`.

---

### Theme 8: Session Security

Multiple session-security defects are present:

1. **Session fixation:** `LoginAction` does not call `session.invalidate()` + `request.getSession(true)` before writing auth attributes. An attacker who can pre-set a session ID (via the cookie header) can fix the victim's session.
2. **Credentials written before auth confirmed:** `LoginAction` writes `sessUsername` to the session before Cognito returns a success response.
3. **Session not invalidated on company switch:** `SwitchCompanyAction` mutates session attributes in-place without creating a new session.
4. **Session re-created after logout:** `LogoutAction` calls `invalidate()` then immediately calls `request.getSession()` (create-if-absent) twice, leaving an active session object after logout.
5. **No `HttpOnly` or `Secure` on JSESSIONID:** `web.xml` uses Servlet 2.4 schema with no `<cookie-config>`; session cookies are readable by JavaScript and transmitted over plain HTTP.

---

### Theme 9: Hardcoded Secrets Throughout

| Secret | Location |
|--------|----------|
| Tomcat UAT password `C!1admin` | `settings.xml` (committed) |
| Tomcat Azure password `pyx1s!96` | `settings.xml` (committed) |
| API bearer token `noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE` | `HttpDownloadUtility.java:105`, `RegisterAction.java` |
| PDF API admin password `ciiadmin` | `MailerAction.java:102` |
| PDF API username `hui` | `MailerAction.java:102` |
| AWS EC2 production hostname | `RuntimeConf.java` |
| S3 bucket name | `RuntimeConf.java` |
| Secondary DB schema `fleeiq` | `RuntimeConf.java` |
| Production email addresses (personal) | `RuntimeConf.java` |

All constants in `RuntimeConf.java` are `public static` (non-final) and mutable at runtime.

---

### Theme 10: Unauthenticated / Plain-HTTP Internal Service Calls

- Cognito sidecar: `http://localhost:9090` — all Cognito credentials in cleartext HTTP on localhost. A compromised process on the same host intercepts credentials.
- Internal PDF/report API: `RuntimeConf.projectUrl` (plain HTTP, EC2 hostname) — all API tokens and report requests in cleartext.
- External API endpoint in `RuntimeConf`: plain HTTP.
- CSS/font fetch in `PreFlightReport` and `Util.getHTML()`: SSRF-capable, plain HTTP, no host validation, 15-minute timeout.

---

## Notable High-Severity Findings (non-Critical)

| ID | Finding | File |
|----|---------|------|
| H-1 | Session fixation on login | `LoginAction.java` |
| H-2 | No brute-force protection on login | `LoginAction.java`, `LoginDAO.java` |
| H-3 | SMTP header/recipient injection via lenient `InternetAddress.parse()` | `Util.java` |
| H-4 | Arbitrary file read via `attachment` path in `sendMail()` | `Util.java` |
| H-5 | Stored GPS data for any unit accessible without comp_id filter | `GPSDao.java`, `unit.gps.jsp` |
| H-6 | Any authenticated user can trigger system-wide calibration reset | `CalibrationAction.java` |
| H-7 | Quartz schedulers leak thread pools; `contextDestroyed()` is a no-op | `TrainingExpiry*Scheduler.java`, `CalibrationJobScheduler.java` |
| H-8 | Cognito errors reflected verbatim into HTML (XSS + info disclosure) | `MessageResources_en.properties`, `RestClientService.java` |
| H-9 | `genPass()` uses `java.util.Random` (predictable temporary passwords) | `Util.java` |
| H-10 | Stored XSS via GPS JSON emitted as `text/html` | `GPSDao.java`, `unit.gps.jsp` |
| H-11 | Calibration reset IDOR — any tenant's forklift safety threshold clearable | `AdminUnitImpactAction.java` |
| H-12 | HTML injection in email body (training expiry emails) | `TrainingDAO.java` |
| H-13 | `deleteUser` silently returns "Deleted" on Cognito failure (orphaned accounts) | `RestClientService.java` |
| H-14 | No CSRF on logout (forced logout DoS) | `LogoutAction.java` |
| H-15 | Reflected XSS in `resetpass.jsp` via unescaped `username` parameter | `resetpass.jsp:32` |

---

## End-to-End Attack Chains

### Chain 1: Unauthenticated Full Database Exfiltration

1. POST to `/mailer.do?frequency=1'+OR+'1'='1` — no auth required
2. `SubscriptionDAO.getAllReport()` executes injected SQL
3. Error response (or `StringIndexOutOfBoundsException` on `lastIndexOf("or")`) confirms injection
4. Union-based or blind SQLi to extract all tenant data

**Prerequisites:** None. No authentication. No special knowledge beyond the app URL.

---

### Chain 2: Unauthenticated Remote Code Execution

1. GET `/adminRegister.do` — create a new company account (no auth required)
2. POST login as the new account
3. POST to a barcode-generating endpoint with `veh_id=../../../../images/barcode/shell.jsp`
4. Write a JSP webshell to the webroot
5. GET `/BHAG/images/barcode/shell.jsp?cmd=id`

**Prerequisites:** None initially; account creation in step 1 is unauthenticated.

---

### Chain 3: Authenticated Cross-Tenant Data Exfiltration (IDOR)

1. Log in as any tenant user
2. Enumerate unit IDs: GET `/getAjax.do?action=gps&compId=<any_id>`
3. For each unit, request GPS history: POST `/gpsReport.do?unit=<unit_id>`
4. Access driver records: GET `/getDriverName.do?driverId=<driver_id>`
5. Access job records: GET `/view_job_details.do?equipId=<unit_id>&job_no=<job_no>`

**Prerequisites:** Any valid session (from any tenant).

---

### Chain 4: Password Recovery via MD5 Rainbow Table

1. Exploit Chain 1 or SQL injection in any authenticated endpoint to dump the `users` table
2. Submit all MD5 hashes to a rainbow table lookup service (e.g., `crackstation.net`)
3. Recover plaintext passwords for majority of user accounts (no salt, no iteration count)
4. Log in directly as recovered users

---

### Chain 5: Privilege Escalation via MenuDAO SQL Injection

1. Log in as any authenticated user (no admin role required)
2. POST to `/adminMenu.do` with injected `roleId`/`menuId` parameters
3. `MenuDAO.saveRoleMenu()` executes `INSERT INTO role_menu VALUES (<injected>)`
4. Inject a row granting the attacker's role access to super-admin menu items
5. Access dealer/super-admin functions in subsequent requests

---

## Remediation Priority

### Immediate (P0) — Fix Before Next Deployment

1. **Remove auth exclusions from `mailer.do`, `adminRegister.do`, `loadbarcode.do`, `api.do`, `goResetPass.do`** — add session and CSRF checks. `uploadfile.do` should be removed or mapped.
2. **Replace all `Statement` + concatenation with `PreparedStatement`** — prioritise all auth-excluded endpoints first, then IDOR-accessible DAOs.
3. **Add `comp_id` tenant scoping to all DAO methods** — all read/write/delete operations must join on or filter by `sessCompId` from the session (not the request).
4. **Remove `settings.xml` from the repository** — rotate all exposed credentials immediately.
5. **Rotate the hardcoded API bearer token** and remove it from source code.

### Short Term (P1) — Address Within One Sprint

6. **Implement CSRF tokens** — call `saveToken()` in forms and `isTokenValid()` in all state-modifying actions. Alternatively, adopt a filter-based CSRF middleware.
7. **Fix session lifecycle** — `session.invalidate()` + `request.getSession(true)` at login, company switch, and logout.
8. **Migrate password hashing to bcrypt** — minimum cost factor 10. Upgrade MD5 hashes on next login.
9. **Add RBAC to `PandoraAction`** — read role from session and enforce per-action access control via an annotation or forwarding table.
10. **Configure JSESSIONID cookie** — add `<cookie-config>` with `<http-only>true</http-only>` and `<secure>true</secure>` to `web.xml`.

### Medium Term (P2) — Address Within One Month

11. **Switch all internal API calls to HTTPS** — Cognito sidecar, PDF report API, external API.
12. **Fix broken DCL singletons** — add `volatile` to all `theInstance` fields.
13. **Replace `java.util.Random` with `SecureRandom`** in `Util.genPass()`.
14. **Remove or sanitise all Lombok `@Data` toString fields** — use `@ToString.Exclude` on password/token/PII fields.
15. **Neutralise deserialization in `FormLibraryBean`** — replace `ObjectInputStream` with a safe serialisation library (JSON/XML) or add an `ObjectInputFilter` allowlist.
16. **Sanitise `veh_id` in barcode path construction** — validate against `[A-Za-z0-9_-]` before use in file paths.
17. **Fix all SSRF vectors** — validate and restrict URLs in `Util.getHTML()`, `HttpDownloadUtility.downloadFile()`, and `PreFlightReport` CSS fetch to known safe hosts.
18. **Shut down Quartz schedulers on undeploy** — implement `contextDestroyed()` correctly in all four scheduler listeners.
19. **Add security response headers** — CSP, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security` — in a servlet filter applied to all responses.
20. **Fix `validation.xml` form-bean name mismatches** — align `adminRegisterActionForm` / `AdminDriverEditForm` case to match `struts-config.xml`.

---

## Configuration and Infrastructure Findings

| Finding | Location | Severity |
|---------|----------|----------|
| No HTTPS transport guarantee | `web.xml` — no `<security-constraint>CONFIDENTIAL` | CRITICAL |
| No HttpOnly/Secure on JSESSIONID | `web.xml` — Servlet 2.4, no `<cookie-config>` | CRITICAL |
| UAT active-by-default Maven profile | `pom.xml` — `<activeByDefault>true</activeByDefault>` | HIGH |
| CI pipeline uses UAT profile silently | `bitbucket-pipelines.yml` — `mvn -B verify`, no `-P` flag | HIGH |
| `log4j.logger.jdbc.sqlonly=DEBUG` logs SQL+params | `log4j.properties` | HIGH |
| `log4j.logger.jdbc.resultset=INFO` logs full rows | `log4j.properties` | HIGH |
| `log4j.debug=true` leaks internal paths | `log4j.properties` | MEDIUM |
| Error pages fall back to Tomcat default (stack trace exposure) | `web.xml` — only 1 error-page entry | MEDIUM |
| All `RuntimeConf` constants are mutable `public static` | `RuntimeConf.java` | MEDIUM |
| JDBC spy log files truncated on restart (forensic evidence destroyed) | `log4j.properties` — `Append=false` | LOW |

---

## Summary Statistics by Theme

| Theme | Critical | High | Notes |
|-------|----------|------|-------|
| SQL Injection | 20+ | 15+ | Entire DAO layer |
| Auth-excluded endpoints | 6 | 2 | 7 of 8 exclusions are inappropriate |
| IDOR / tenant isolation | 5 | 12+ | No comp_id scoping anywhere |
| Session security | 3 | 5 | Fixation, re-creation, cookie flags |
| Hardcoded secrets | 4 | 3 | Token, passwords, hostnames |
| RBAC gaps | 2 | 6 | Base class + individual actions |
| CSRF | 0 | 8+ | No CSRF protection anywhere |
| XSS | 1 | 6 | Stored, reflected, DOM |
| Path traversal / RCE | 2 | 2 | Barcode + import upload |
| Deserialization | 1 | 0 | FormLibraryBean |
| Cryptography | 2 | 2 | MD5, Random, plain HTTP |
| Broken DCL/singleton | 0 | 3 | Non-volatile, thread safety |
| Information disclosure | 0 | 5 | Lombok, error messages, logs |

---

*Pass 1 complete. Pass 2 (test coverage review) and Pass 3 (dependency/CVE review) are the recommended next steps.*
