# Pass 2 — Test Coverage Audit: Configuration Layer
**Agent:** A01
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Repo root:** C:\Projects\cig-audit\repos\fleetfocus

---

## Reading Evidence

### File: WEB-INF/web.xml
- **Line count:** 174
- **Configurable elements defined:**

| # | Type | Name | Class / Pattern |
|---|------|------|-----------------|
| 1 | servlet | `Frm_saveuser` | `com.torrent.surat.fms6.master.Frm_saveuser` → `/servlet/Frm_saveuser` |
| 2 | servlet | `Frm_security` | `com.torrent.surat.fms6.security.Frm_security` → `/servlet/Frm_security` |
| 3 | servlet | `Frm_login` | `com.torrent.surat.fms6.security.Frm_login` → `/servlet/Frm_login` |
| 4 | servlet | `Frm_upload` | `com.torrent.surat.fms6.master.Frm_upload` → `/servlet/Frm_upload` |
| 5 | servlet | `Frm_vehicle` | `com.torrent.surat.fms6.security.Frm_vehicle` → `/servlet/Frm_vehicle` |
| 6 | servlet | `Frm_customer` | `com.torrent.surat.fms6.security.Frm_customer` → `/servlet/Frm_customer` |
| 7 | servlet | `Import_Files` | `com.torrent.surat.fms6.util.ImportFiles` → `/servlet/Import_Files` |
| 8 | servlet | `CustomUpload` | `com.torrent.surat.fms6.util.CustomUpload` → `/servlet/CustomUpload` |
| 9 | servlet | `BusinessInsight` | `com.torrent.surat.fms6.businessinsight.BusinessInsight` → `/servlet/BusinessInsight` |
| 10 | session-config | session-timeout | 30 minutes |
| 11 | security-constraint | `HTTPSOnly` | `/pages/*` → CONFIDENTIAL (HTTPS enforced) |
| 12 | security-constraint | `HTTPorHTTPS` | `*.ico`, `/img/*`, `/js/*`, `/css/*`, `/skin/js/*`, `/skin/css/*`, `/gps/*`, `/reports/*`, `/dyn_report/*`, `/linde_reports/*`, `/includes/*`, `/images/*` → NONE |
| 13 | jsp-config | jsp-property-group | `*.jsp` → page-encoding ISO-8859-1 |

No filters, no listeners, no error-page declarations are present in web.xml.

Note: `ImportFiles` and `CustomUpload` and `BusinessInsight` are also annotated with `@WebServlet` in their Java source, creating a dual-registration that overrides web.xml for those three servlets at runtime. This configuration ambiguity is itself untested.

---

### File: WEB-INF/src/log4j.properties
- **Line count:** 29
- **Property keys defined:**

| Key | Value |
|-----|-------|
| `log4j.rootLogger` | `INFO, file` |
| `log4j.appender.file` | `org.apache.log4j.RollingFileAppender` |
| `log4j.appender.file.File` | `/home/gmtp/logs/linde.log` |
| `log4j.appender.file.MaxFileSize` | `10MB` |
| `log4j.appender.file.MaxBackupIndex` | `100` |
| `log4j.appender.file.layout` | `org.apache.log4j.PatternLayout` |
| `log4j.appender.file.layout.ConversionPattern` | `%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1}:%L - %m%n` |

Notes: References `org.apache.log4j` (Log4j 1.x). The codebase actually imports `org.apache.logging.log4j` (Log4j 2.x). The `log4j.properties` file is therefore dead configuration that would be silently ignored at runtime.

---

### File: WEB-INF/src/log4j2.properties
- **Line count:** 24
- **Property keys defined:**

| Key | Value |
|-----|-------|
| `name` | `PropertiesConfig` |
| `property.filename` | `logs` |
| `appenders` | `console, file` |
| `appender.console.type` | `Console` |
| `appender.console.name` | `STDOUT` |
| `appender.console.layout.type` | `PatternLayout` |
| `appender.console.layout.pattern` | `[%-5level] %d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %c{1} - %msg%n` |
| `appender.file.type` | `File` |
| `appender.file.name` | `LOGFILE` |
| `appender.file.fileName` | `/home/gmtp/logs/linde.log` |
| `appender.file.layout.type` | `PatternLayout` |
| `appender.file.layout.pattern` | `[%-5level] %d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %c{1} - %msg%n` |
| `loggers` | `file` |
| `logger.file.name` | `log4j2properties` |
| `logger.file.level` | `info,debug` (invalid compound value — should be a single level) |
| `logger.file.appenderRefs` | `file` |
| `logger.file.appenderRef.file.ref` | `LOGFILE` |
| `rootLogger.level` | `debug` |
| `rootLogger.appenderRefs` | `file` |
| `rootLogger.appenderRef.stdout.ref` | `LOGFILE` (ref name is "stdout" but target is "LOGFILE") |

Notes: The root logger level is `debug` in this file but `INFO` in log4j.properties. The `logger.file.level` value `info,debug` is syntactically invalid in Log4j 2 properties format; only one level token is accepted. The appenderRef name mismatch (`stdout` vs `LOGFILE`) is a silent misconfiguration that goes undetected without a startup test.

---

### File: WEB-INF/src/ESAPI.properties
- **Line count:** 554 (read in full)
- **Significant property keys defined (security-relevant subset):**

| Key | Value / Relevance |
|-----|-------------------|
| `ESAPI.printProperties` | `true` — dumps all ESAPI config to stdout at boot |
| `ESAPI.AccessControl` | `DefaultAccessController` |
| `ESAPI.Authenticator` | `FileBasedAuthenticator` |
| `ESAPI.Encoder` | `DefaultEncoder` |
| `ESAPI.Encryptor` | `JavaEncryptor` |
| `ESAPI.IntrusionDetector` | `DefaultIntrusionDetector` |
| `ESAPI.Logger` | `JavaLogFactory` |
| `Authenticator.AllowedLoginAttempts` | `3` |
| `Authenticator.MaxOldPasswordHashes` | `13` |
| `Authenticator.IdleTimeoutDuration` | `20` minutes |
| `Authenticator.AbsoluteTimeoutDuration` | `120` minutes |
| `Encoder.AllowMultipleEncoding` | `false` |
| `Encoder.AllowMixedEncoding` | `false` |
| `Encryptor.MasterKey` | **COMMENTED OUT / BLANK** — encryption non-functional |
| `Encryptor.MasterSalt` | **COMMENTED OUT / BLANK** — encryption non-functional |
| `Encryptor.CipherTransformation` | `AES/CBC/PKCS5Padding` |
| `Encryptor.EncryptionKeyLength` | `128` |
| `Encryptor.CipherText.useMAC` | `true` |
| `Encryptor.HashAlgorithm` | `SHA-512` |
| `Encryptor.HashIterations` | `1024` |
| `HttpUtilities.ForceHttpOnlySession` | **`false`** — session cookie HttpOnly NOT enforced |
| `HttpUtilities.ForceSecureSession` | **`false`** — session cookie Secure NOT enforced |
| `HttpUtilities.ForceHttpOnlyCookies` | `true` |
| `HttpUtilities.ForceSecureCookies` | `true` |
| `HttpUtilities.UploadDir` | `C:\\ESAPI\\testUpload` — Windows path on a Linux server |
| `HttpUtilities.ApprovedUploadExtensions` | `.pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.rtf,.txt,.jpg,.png` |
| `HttpUtilities.MaxUploadFileBytes` | `500000000` (500 MB) |
| `HttpUtilities.FileUploadAllowAnonymousUser` | **`true`** — unauthenticated upload permitted |
| `HttpUtilities.OverwriteStatusCodes` | `true` — all responses rewritten to HTTP 200 |
| `Logger.ApplicationName` | `ExampleApplication` — placeholder value, not customised |
| `IntrusionDetector.Disable` | `false` |
| `Validator.Redirect` | `^\\/test.*$` — redirect whitelist still says "test" |
| `Validator.HtmlValidationAction` | `throw` |
| `Validator.ConfigurationFile` | `validation.properties` |

---

### File: WEB-INF/src/esapi-java-logging.properties
- **Line count:** 6
- **Property keys defined:**

| Key | Value |
|-----|-------|
| `handlers` | `java.util.logging.ConsoleHandler` |
| `.level` | `INFO` |
| `java.util.logging.ConsoleHandler.level` | `INFO` |
| `java.util.logging.ConsoleHandler.formatter` | `java.util.logging.SimpleFormatter` |
| `java.util.logging.SimpleFormatter.format` | `[%1$tF %1$tT] [%3$-7s] %5$s %n` |

---

### File: WEB-INF/src/validation.properties
- **Line count:** 29
- **Property keys defined:**

| Key | Regex value |
|-----|-------------|
| `Validator.SafeString` | `^[.\\p{Alnum}\\p{Space}]{0,1024}$` |
| `Validator.Email` | `^[A-Za-z0-9._%'-]+@[A-Za-z0-9.-]+\\.[a-zA-Z]{2,4}$` |
| `Validator.IPAddress` | full IPv4 octet regex |
| `Validator.URL` | URL regex |
| `Validator.CreditCard` | `^(\\d{4}[- ]?){3}\\d{4}$` |
| `Validator.SSN` | SSN regex |

---

## Search Evidence — Test Files

The following grep searches were executed. **All returned zero test files.**

| Search term | Files with matches (test files only) |
|-------------|--------------------------------------|
| `web\.xml` | 0 test files |
| `esapi` (case-insensitive) | 0 test files |
| `log4j` (case-insensitive) | 0 test files |
| `RuntimeConf` | 0 test files |
| `@Test` | 0 files in entire codebase |
| `TestCase` | 0 files in entire codebase |
| `junit\.framework` | 0 files in entire codebase |
| Directories named `test` or `tests` | None found |

Matches found in `web.xml`, `ESAPI` etc. are all in production source files and prior audit markdown notes, not test code.

---

## Findings

### A01-1 — CRITICAL — No test coverage — login servlet (SQL injection + credential exposure)
**File:** `WEB-INF/web.xml` (servlet: `Frm_login` → `/servlet/Frm_login`), `WEB-INF/src/com/torrent/surat/fms6/security/Frm_login.java`
**Severity:** CRITICAL
**Category:** No test coverage — authentication servlet
**Detail:** `Frm_login` is the application's primary authentication entry point, registered at `/servlet/Frm_login`. Inspection of the servlet source confirms the `login` parameter is concatenated directly into a SQL `SELECT` query string without using a `PreparedStatement` (lines 58–66 and 72–73 of `Frm_login.java`). This is a classical SQL injection vector in the most sensitive path of the application. There is no test of any kind — no unit test to verify correct credential validation, no negative test for injection strings, no test that verifies session is established only on valid credentials, and no integration test that starts the container and exercises this mapping. The authentication outcome for boundary conditions (empty username, Unicode input, SQL metacharacters) is completely unverified.
**Recommended test:** `testFrmLoginSqlInjectionPrevented()` — use MockHttpServletRequest/MockHttpServletResponse (Spring Mock or Mockito), inject a login parameter of `' OR '1'='1`, assert HTTP response redirects to the error page and no session attribute is set. Pair with `testFrmLoginValidCredentials()` and `testFrmLoginInvalidCredentials()`.

---

### A01-2 — CRITICAL — No test coverage — security servlet (access control dispatcher)
**File:** `WEB-INF/web.xml` (servlet: `Frm_security` → `/servlet/Frm_security`), `WEB-INF/src/com/torrent/surat/fms6/security/Frm_security.java`
**Severity:** CRITICAL
**Category:** No test coverage — access control dispatcher
**Detail:** `Frm_security` is the central POST dispatcher for all access-controlled operations (form saving, module management, mail group operations, and others selected by the `op_code` parameter). It uses ESAPI and BCrypt and drives JNDI database operations. No test verifies that: (a) the op_code dispatch table routes to the correct handler; (b) an unauthenticated request is rejected; (c) ESAPI encoder/validator are invoked correctly; (d) BCrypt verification is called on the submitted password. A regression or misconfiguration in this servlet would be completely silent.
**Recommended test:** `testFrmSecurityDispatchRequiresSession()` — assert that a POST to the servlet without a valid session attribute results in rejection (redirect to login). `testFrmSecurityOpCodeRouting()` — mock the request with each known `op_code` value and verify the correct handler method is invoked (via spy or argument capture).

---

### A01-3 — CRITICAL — No test coverage — HTTPS enforcement security-constraint
**File:** `WEB-INF/web.xml` (security-constraint: `HTTPSOnly`, url-pattern `/pages/*`)
**Severity:** CRITICAL
**Category:** No test coverage — transport security enforcement
**Detail:** The `<security-constraint>` element declaring `CONFIDENTIAL` transport for `/pages/*` is the sole declarative mechanism that forces all authenticated page traffic over HTTPS. This constraint is entirely enforced by the container at deployment time; if the wrong `web.xml` is deployed, or if a container configuration ignores it, all authenticated pages silently revert to HTTP. There is no integration test that starts a Tomcat instance and verifies that an HTTP request to `/pages/somePage.jsp` is redirected to HTTPS. There is equally no test for the inverse: that the static-asset patterns (`/js/*`, `/css/*`, `/images/*`, etc.) correctly receive `NONE` treatment and are not broken by accidental over-restriction.
**Recommended test:** `testPagesRequireHttps()` — embed Tomcat (or use Arquillian), deploy the application, issue an HTTP GET to `/pages/login.jsp`, assert response code is 301/302 to an `https://` URL. `testStaticAssetsAllowHttp()` — assert HTTP GET to `/js/app.js` returns 200 without redirect.

---

### A01-4 — CRITICAL — No test coverage — ESAPI encryption key absent
**File:** `WEB-INF/src/ESAPI.properties` (keys: `Encryptor.MasterKey`, `Encryptor.MasterSalt`)
**Severity:** CRITICAL
**Category:** No test coverage — encryption configuration
**Detail:** Both `Encryptor.MasterKey` and `Encryptor.MasterSalt` are commented out in `ESAPI.properties`. ESAPI's `JavaEncryptor` will throw a `ConfigurationException` at first use if these keys are absent, silently disabling any encryption call that relies on them. There is no test that verifies ESAPI can be initialised with the supplied configuration, no smoke test that calls `ESAPI.encryptor()` and confirms it does not throw, and no test that encrypts and decrypts a known value end-to-end. This means the encryption failure mode has never been observed or documented.
**Recommended test:** `testEsapiEncryptorInitialises()` — call `ESAPI.encryptor()` and assert no `ConfigurationException` is thrown. `testEsapiEncryptRoundTrip()` — encrypt a plaintext string and decrypt it back, asserting equality, to verify the key and cipher configuration is self-consistent.

---

### A01-5 — CRITICAL — No test coverage — session cookie security flags disabled
**File:** `WEB-INF/src/ESAPI.properties` (keys: `HttpUtilities.ForceHttpOnlySession=false`, `HttpUtilities.ForceSecureSession=false`)
**Severity:** CRITICAL
**Category:** No test coverage — session cookie hardening
**Detail:** `HttpUtilities.ForceHttpOnlySession` and `HttpUtilities.ForceSecureSession` are both set to `false`. This means ESAPI's `HTTPUtilities.setCurrentHTTP()` will not add the `HttpOnly` or `Secure` flags to the `JSESSIONID` cookie. Combined with the session timeout of 30 minutes in `web.xml`, this configuration directly enables session hijacking via XSS or network sniffing. There is no test that instantiates an ESAPI-managed response, calls the session establishment path, and asserts the JSESSIONID cookie carries both `HttpOnly` and `Secure` attributes.
**Recommended test:** `testSessionCookieIsHttpOnly()` and `testSessionCookieIsSecure()` — use `MockHttpServletResponse`, run the login flow, extract the `Set-Cookie` header for `JSESSIONID`, assert presence of `HttpOnly` and `Secure` directives.

---

### A01-6 — HIGH — No test coverage — file upload servlets (unauthenticated upload permitted)
**File:** `WEB-INF/web.xml` (servlets: `Frm_upload` → `/servlet/Frm_upload`, `Import_Files` → `/servlet/Import_Files`, `CustomUpload` → `/servlet/CustomUpload`); `WEB-INF/src/ESAPI.properties` (key: `HttpUtilities.FileUploadAllowAnonymousUser=true`)
**Severity:** HIGH
**Category:** No test coverage — file upload security
**Detail:** Three servlets accept multipart file uploads. `ESAPI.properties` explicitly sets `HttpUtilities.FileUploadAllowAnonymousUser=true`, meaning ESAPI will not reject unauthenticated upload requests. The approved extension list (`.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, `.rtf`, `.txt`, `.jpg`, `.png`) and 500 MB maximum file size (`HttpUtilities.MaxUploadFileBytes=500000000`) are both configured in ESAPI.properties but neither is tested. There is no test that verifies upload of a disallowed extension (e.g., `.jsp`, `.war`, `.exe`) is rejected, no test for the 500 MB boundary, and no test that verifies an unauthenticated upload is rejected at the application layer. The `HttpUtilities.UploadDir` is set to `C:\\ESAPI\\testUpload` — a Windows path that will fail silently on the production Linux server.
**Recommended test:** `testUploadRejectedForDisallowedExtension()` — POST a multipart request with a `.jsp` file and assert a 400 or error response. `testUploadRejectedWhenUnauthenticated()` — POST without a valid session and assert rejection. `testUploadDirectoryIsWritable()` — at application startup, verify the configured upload directory exists and is writable.

---

### A01-7 — HIGH — No test coverage — vehicle and customer administration servlets
**File:** `WEB-INF/web.xml` (servlets: `Frm_vehicle` → `/servlet/Frm_vehicle`, `Frm_customer` → `/servlet/Frm_customer`)
**Severity:** HIGH
**Category:** No test coverage — privileged administration operations
**Detail:** `Frm_vehicle` and `Frm_customer` are security-package servlets that perform vehicle and customer master-data operations. Both use BCrypt for password checks and RuntimeConf for database JNDI lookup. Neither has any test coverage. Changes to vehicle or customer records are irreversible in many cases (e.g., vehicle deletion, customer deactivation), so regressions here carry direct operational risk. There is no test for authorisation (only admins should access these), no test for data integrity (correct records updated), and no test for the BCrypt path.
**Recommended test:** `testFrmVehicleRequiresAdminRole()` — assert that a non-admin session results in a redirect or 403. `testFrmCustomerSavePersistedCorrectly()` — mock the datasource, invoke the save path, assert correct SQL was executed via a capture of the PreparedStatement.

---

### A01-8 — HIGH — No test coverage — user save servlet (SingleThreadModel, deprecated)
**File:** `WEB-INF/web.xml` (servlet: `Frm_saveuser` → `/servlet/Frm_saveuser`), `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`
**Severity:** HIGH
**Category:** No test coverage — user management with deprecated concurrency model
**Detail:** `Frm_saveuser` implements the deprecated `SingleThreadModel` interface, which was removed in Servlet 6.0 and causes Tomcat to serialise all requests through a single instance. This has severe concurrency implications in production. There is no test that verifies user-creation logic, no test for the password hashing path, no concurrent-request test to expose the serialisation bottleneck, and no test that a user with a duplicate username is correctly rejected.
**Recommended test:** `testSaveUserCreatesCorrectRecord()` — mock the datasource, POST a new-user request, assert the expected INSERT SQL is executed. `testSaveUserRejectsDuplicateUsername()` — simulate a username collision and assert the correct error response.

---

### A01-9 — HIGH — No test coverage — BusinessInsight servlet
**File:** `WEB-INF/web.xml` (servlet: `BusinessInsight` → `/servlet/BusinessInsight`), `WEB-INF/src/com/torrent/surat/fms6/businessinsight/BusinessInsight.java`
**Severity:** HIGH
**Category:** No test coverage — reporting / data-export servlet
**Detail:** `BusinessInsight` is a `@MultipartConfig` servlet also declared in `web.xml`. It uses Log4j 2 and the `mail` utility. No test verifies its load, its multipart handling, its email path, or any of its data output. The dual registration via both `@WebServlet` and `web.xml` is also untested and the runtime resolution order between the two declarations is container-specific.
**Recommended test:** `testBusinessInsightLoadsWithoutError()` — create an instance and invoke `init()`, asserting no exception. `testBusinessInsightDualRegistrationWinner()` — deploy to an embedded container and confirm only one servlet mapping responds to `/servlet/BusinessInsight`.

---

### A01-10 — HIGH — No test coverage — Log4j 2 configuration validity
**File:** `WEB-INF/src/log4j2.properties`
**Severity:** HIGH
**Category:** No test coverage — logging configuration correctness
**Detail:** `log4j2.properties` contains two silent misconfigurations: (1) `logger.file.level = info,debug` — Log4j 2 accepts only a single level token; `info,debug` will cause the logger level to be silently set to the default (`ERROR`) because the value is unparseable. This means INFO-level log statements (used extensively across all servlets) will produce no output. (2) `rootLogger.appenderRef.stdout.ref = LOGFILE` — the appender reference name is `stdout` but the target appender name is `LOGFILE`; this broken reference means the root logger output will be silently dropped. There is no startup test that verifies log messages actually reach the log file. On top of this, `log4j.properties` (Log4j 1.x format) is present alongside `log4j2.properties`, adding further ambiguity about which configuration is active.
**Recommended test:** `testLog4j2ConfigurationIsValid()` — use `LogManager.getContext(false).getConfiguration()` to obtain the live configuration, assert that at least one appender is attached to the root logger, and assert root logger level is not ERROR.

---

### A01-11 — HIGH — No test coverage — ESAPI intrusion detection thresholds
**File:** `WEB-INF/src/ESAPI.properties` (keys: `IntrusionDetector.*`)
**Severity:** HIGH
**Category:** No test coverage — intrusion detection configuration
**Detail:** Intrusion detection thresholds are configured for `IntrusionException` (count=1, actions=log,disable,logout) and `AuthenticationHostException` (count=2, interval=10, actions=log,logout). These thresholds are live security controls: a misconfiguration (e.g., accidentally setting count=0 or disabling the detector) would silently remove the brute-force and session-hijacking defences. There is no test that triggers a test intrusion event and asserts the detector fires the configured actions.
**Recommended test:** `testIntrusionDetectorFiresOnThreshold()` — call `IntrusionDetector.getInstance().addEvent("test")` twice within 10 seconds, assert that the account becomes disabled per the `event.test.actions=disable,log` configuration.

---

### A01-12 — MEDIUM — No test coverage — ESAPI validator regex correctness
**File:** `WEB-INF/src/validation.properties`, `WEB-INF/src/ESAPI.properties` (Validator.* keys)
**Severity:** MEDIUM
**Category:** No test coverage — input validation regex
**Detail:** `validation.properties` defines six named validation patterns (`SafeString`, `Email`, `IPAddress`, `URL`, `CreditCard`, `SSN`) and `ESAPI.properties` adds HTTP-specific patterns (`HTTPCookieName`, `HTTPParameterValue`, `HTTPJSESSIONID`, `Validator.Redirect`, etc.). None of these regexes have a corresponding positive or negative test. Notable concerns: `Validator.Redirect` is set to `^\\/test.*$`, a placeholder value that restricts all redirects to URLs starting with `/test`. This is almost certainly wrong for production and means any redirect target outside `/test*` will be rejected by ESAPI. `Validator.HTTPParameterValue` allows `\p{L}` (Unicode letters) but excludes several common printable characters, which may cause legitimate form submissions to fail. Without tests, these silent rejections cannot be distinguished from application bugs.
**Recommended test:** `testRedirectValidatorAllowsProductionPaths()` — call `ESAPI.validator().isValidRedirectLocation(...)` with known valid production paths (e.g., `/pages/dashboard.jsp`) and assert `true`. `testEmailValidatorAcceptsValidRejectsInvalid()` — test a matrix of valid and invalid email strings against the configured pattern.

---

### A01-13 — MEDIUM — No test coverage — session timeout configuration
**File:** `WEB-INF/web.xml` (element: `<session-timeout>30</session-timeout>`)
**Severity:** MEDIUM
**Category:** No test coverage — session lifecycle
**Detail:** The `web.xml` declares a 30-minute session timeout. `ESAPI.properties` separately declares `Authenticator.IdleTimeoutDuration=20` and `Authenticator.AbsoluteTimeoutDuration=120`. These three values are inconsistent (20 min ESAPI idle vs 30 min container timeout vs 120 min ESAPI absolute). There is no test that verifies which timeout wins, no test that verifies a session is invalidated after inactivity, and no test that confirms the container session timeout is honoured.
**Recommended test:** `testSessionExpiresAfterIdleTimeout()` — create a session, advance a mock clock by 31 minutes, assert that subsequent access results in a new-session redirect to the login page.

---

### A01-14 — MEDIUM — No test coverage — JSP character encoding
**File:** `WEB-INF/web.xml` (jsp-config: `*.jsp` → page-encoding `ISO-8859-1`)
**Severity:** MEDIUM
**Category:** No test coverage — character encoding consistency
**Detail:** All JSPs are declared as ISO-8859-1. `ESAPI.properties` sets `HttpUtilities.ResponseContentType=text/html; charset=UTF-8` and `HttpUtilities.CharacterEncoding=UTF-8`. `Frm_security.java` calls `res.setCharacterEncoding("UTF-8")`. The result is a three-way encoding mismatch: JSP page-encoding ISO-8859-1, ESAPI response UTF-8, servlet response UTF-8. There is no test that submits multi-byte or non-ASCII input and verifies round-trip encoding correctness.
**Recommended test:** `testNonAsciiInputRoundTrip()` — POST a request containing non-ASCII characters (e.g., accented letters), process through the servlet, and assert the response body contains the correctly encoded characters.

---

### A01-15 — MEDIUM — No test coverage — ESAPI logger application name placeholder
**File:** `WEB-INF/src/ESAPI.properties` (key: `Logger.ApplicationName=ExampleApplication`)
**Severity:** MEDIUM
**Category:** No test coverage — logging identity / operational configuration
**Detail:** `Logger.ApplicationName` is set to `ExampleApplication`, which is the ESAPI default template value. All ESAPI log entries will be tagged with `ExampleApplication` in production, making log aggregation and alerting based on application name unreliable. There is no test that reads this property and asserts it matches the expected production application name.
**Recommended test:** `testEsapiApplicationNameIsCorrect()` — load ESAPI configuration and assert `ESAPI.securityConfiguration().getApplicationName()` equals `"FleetFocus"` (or the correct production identifier).

---

### A01-16 — LOW — No test coverage — log file path hard-coded to Linux home directory
**File:** `WEB-INF/src/log4j.properties` (key: `log4j.appender.file.File=/home/gmtp/logs/linde.log`), `WEB-INF/src/log4j2.properties` (key: `appender.file.fileName=/home/gmtp/logs/linde.log`)
**Severity:** LOW
**Category:** No test coverage — operational path configuration
**Detail:** Both log configuration files hard-code the log output path to `/home/gmtp/logs/linde.log`. If this directory does not exist or is not writable, Log4j silently fails to write logs with no error to the operator. No startup test verifies the log directory exists and is writable before the application begins handling requests.
**Recommended test:** `testLogDirectoryIsAccessibleAtStartup()` — at application init, assert `new File("/home/gmtp/logs").isDirectory()` and `canWrite()`. Alternatively, configure a test-scoped appender and assert a known log message appears after servlet init.

---

### A01-17 — LOW — No test coverage — dead log4j 1.x configuration
**File:** `WEB-INF/src/log4j.properties`
**Severity:** LOW
**Category:** No test coverage — dead configuration / version mismatch
**Detail:** `log4j.properties` uses the Log4j 1.x property namespace (`log4j.rootLogger`, `log4j.appender.*`). All servlet source files import `org.apache.logging.log4j` (Log4j 2.x). Log4j 2 does not read `log4j.properties` files by default; it looks for `log4j2.properties`, `log4j2.xml`, or `log4j2.json`. This file is therefore silently inert. There is no test that confirms the active logging framework version, and no test that asserts `log4j.properties` is not the active configuration.
**Recommended test:** `testActiveLoggingFrameworkIsLog4j2()` — assert `LogManager.getContext().getClass().getName()` contains `log4j2` and does not contain `log4j` version 1.x.

---

### A01-18 — INFO — No test coverage — ESAPI print properties at startup
**File:** `WEB-INF/src/ESAPI.properties` (key: `ESAPI.printProperties=true`)
**Severity:** INFO
**Category:** No test coverage — information disclosure at startup
**Detail:** `ESAPI.printProperties=true` causes ESAPI to print its entire configuration to standard output at startup. In a production environment this means all ESAPI settings (including algorithm names, key lengths, and timeout values) appear in application server logs. The ESAPI project documentation explicitly notes this should be `false` in production (the property comment references "src/test/resources/.esapi version" as the place it should be false). There is no test that asserts this is set to `false` for production builds.
**Recommended test:** `testEsapiPrintPropertiesIsFalseInProduction()` — load the production `ESAPI.properties` resource and assert `ESAPI.printProperties` equals `"false"`.

---

## Checklist

| Question | Answer |
|----------|--------|
| Is there any test that verifies a filter/servlet/listener loads correctly? | No. No tests exist at all. |
| Is there any test that verifies properties are read with correct defaults? | No. |
| Is there any integration test that starts the Tomcat container? | No. |
| Is there any test for the security filter (login, session, access control)? | No. |
| Is there any test for error pages / exception handling? | No. web.xml has no error-page declarations and no tests for exception behaviour exist. |
| Is there any test for the HTTPS transport constraint? | No. |
| Is there any test for file upload extension restriction? | No. |
| Is there any test for ESAPI intrusion detection thresholds? | No. |
| Is there any test for the session timeout (web.xml vs ESAPI vs servlet)? | No. |
| Is there any test for Log4j 2 configuration correctness? | No. |

---

## Summary

| File | Key Elements Count | Test Coverage |
|------|--------------------|---------------|
| `WEB-INF/web.xml` | 9 servlets, 1 session-config, 2 security-constraints, 1 jsp-config | None |
| `WEB-INF/src/log4j.properties` | 7 property keys (Log4j 1.x — dead config) | None |
| `WEB-INF/src/log4j2.properties` | 19 property keys (2 silent misconfigurations) | None |
| `WEB-INF/src/ESAPI.properties` | ~55 active property keys (security-critical) | None |
| `WEB-INF/src/esapi-java-logging.properties` | 5 property keys | None |
| `WEB-INF/src/validation.properties` | 6 validator regex keys | None |
| **Total** | **~97 configurable elements across 6 files** | **0% — None** |

---

## Recommended Test Strategy

Ordered by risk (highest first):

1. **[CRITICAL] Integration smoke test — container startup**
   Write a single Arquillian or embedded-Tomcat test that deploys the WAR and asserts the container starts without errors. This one test would immediately surface the broken Log4j 2 appender reference, the ESAPI missing master key, the Windows upload path on a Linux host, and the `ExampleApplication` logger name. Estimated effort: 1 day. Test method: `testApplicationDeploysWithoutErrors()`.

2. **[CRITICAL] Authentication servlet tests — Frm_login**
   Mock-servlet tests for the login path: valid credentials, invalid credentials, SQL injection input, empty parameters, brute-force threshold (ties to intrusion detector). This is the single highest-risk untested path. Estimated effort: 1 day. Key methods: `testLoginValidCredentials()`, `testLoginInvalidCredentials()`, `testLoginSqlInjectionBlocked()`.

3. **[CRITICAL] HTTPS transport constraint verification**
   Embedded-Tomcat integration test asserting that HTTP requests to `/pages/*` receive a redirect to HTTPS and that static assets under `/js/*`, `/css/*`, `/images/*` do not. Estimated effort: half day.

4. **[CRITICAL] ESAPI encryptor and cookie-flag tests**
   Unit tests for ESAPI initialisation (confirms master key is present or handles absence), and for session/cookie flag assertions. Estimated effort: half day.

5. **[HIGH] File upload restriction tests**
   Mock-multipart tests for each upload servlet: disallowed extensions, oversized files, unauthenticated requests, upload directory writability. Estimated effort: 1 day.

6. **[HIGH] Log4j 2 configuration correctness test**
   Programmatic Log4j 2 configuration inspection at test time: assert appender is attached, level is not ERROR, appenderRef names resolve. Estimated effort: 2 hours.

7. **[HIGH] Access-control servlets — Frm_security, Frm_vehicle, Frm_customer**
   Mock-servlet tests for session presence check, op_code dispatch, and BCrypt path. Estimated effort: 2 days.

8. **[MEDIUM] Input validation regex tests**
   Parameterised tests covering valid and invalid inputs against every named validator in `validation.properties` and the HTTP validators in `ESAPI.properties`. Pay particular attention to `Validator.Redirect` (currently `^\\/test.*$` placeholder). Estimated effort: half day.

9. **[MEDIUM] Session timeout consistency test**
   Verify the 30-minute container timeout, 20-minute ESAPI idle timeout, and 120-minute ESAPI absolute timeout are mutually understood and the lowest value (20 min) governs. Estimated effort: 2 hours.

10. **[LOW / INFO] Operational configuration assertions**
    Properties-file assertion tests: `ESAPI.printProperties=false` in production, `Logger.ApplicationName` is not `ExampleApplication`, log directory exists and is writable. These are cheap to write (< 1 hour) and prevent silent operational failures at deployment.
