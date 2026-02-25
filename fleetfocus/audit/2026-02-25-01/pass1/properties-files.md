# Security Audit: Properties Files
**Audit Run:** 2026-02-25-01
**Agent:** A02
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25

---

## STEP 1 — BRANCH CHECK

Read `C:\Projects\cig-audit\repos\fleetfocus\.git\HEAD`:

```
ref: refs/heads/release/UAT_RELEASE_FLEETFOCUS_Production
```

Branch confirmed. Proceeding.

---

## STEP 2 — FILES READ

| # | File | Lines |
|---|------|-------|
| 1 | `WEB-INF/src/ESAPI.properties` | 554 |
| 2 | `WEB-INF/src/esapi-java-logging.properties` | 7 |
| 3 | `WEB-INF/src/log4j.properties` | 29 |
| 4 | `WEB-INF/src/log4j2.properties` | 24 |
| 5 | `WEB-INF/src/validation.properties` | 29 |

---

## STEP 3 — READING EVIDENCE

### 3.1 ESAPI.properties (554 lines)

| Property | Value | Flag? |
|----------|-------|-------|
| `ESAPI.printProperties` | `true` | Potential info leak |
| `ESAPI.AccessControl` | `org.owasp.esapi.reference.DefaultAccessController` | - |
| `ESAPI.Authenticator` | `org.owasp.esapi.reference.FileBasedAuthenticator` | - |
| `ESAPI.Encoder` | `org.owasp.esapi.reference.DefaultEncoder` | - |
| `ESAPI.Encryptor` | `org.owasp.esapi.reference.crypto.JavaEncryptor` | - |
| `ESAPI.Executor` | `org.owasp.esapi.reference.DefaultExecutor` | - |
| `ESAPI.HTTPUtilities` | `org.owasp.esapi.reference.DefaultHTTPUtilities` | - |
| `ESAPI.IntrusionDetector` | `org.owasp.esapi.reference.DefaultIntrusionDetector` | - |
| `ESAPI.Logger` | `org.owasp.esapi.logging.java.JavaLogFactory` | - |
| `ESAPI.Randomizer` | `org.owasp.esapi.reference.DefaultRandomizer` | - |
| `ESAPI.Validator` | `org.owasp.esapi.reference.DefaultValidator` | - |
| `Authenticator.AllowedLoginAttempts` | `3` | - |
| `Authenticator.MaxOldPasswordHashes` | `13` | - |
| `Authenticator.UsernameParameterName` | `username` | - |
| `Authenticator.PasswordParameterName` | `password` | - |
| `Authenticator.RememberTokenDuration` | `14` (days) | - |
| `Authenticator.IdleTimeoutDuration` | `20` (minutes) | - |
| `Authenticator.AbsoluteTimeoutDuration` | `120` (minutes) | - |
| `Encoder.AllowMultipleEncoding` | `false` | - |
| `Encoder.AllowMixedEncoding` | `false` | - |
| `Encoder.DefaultCodecList` | `HTMLEntityCodec,PercentCodec,JavaScriptCodec` | - |
| `Encryptor.MasterKey` | **COMMENTED OUT** (line 130: `#Encryptor.MasterKey=`) | FLAG — key absent/missing |
| `Encryptor.MasterSalt` | **COMMENTED OUT** (line 131: `#Encryptor.MasterSalt=`) | FLAG — salt absent/missing |
| `Encryptor.PreferredJCEProvider` | _(empty)_ | - |
| `Encryptor.EncryptionAlgorithm` | `AES` | - |
| `Encryptor.CipherTransformation` | `AES/CBC/PKCS5Padding` | - |
| `Encryptor.cipher_modes.combined_modes` | `GCM,CCM,IAPM,EAX,OCB,CWC` | - |
| `Encryptor.cipher_modes.additional_allowed` | `CBC` | - |
| `Encryptor.EncryptionKeyLength` | `128` | - |
| `Encryptor.MinEncryptionKeyLength` | `128` | - |
| `Encryptor.ChooseIVMethod` | `random` | - |
| `Encryptor.CipherText.useMAC` | `true` | - |
| `Encryptor.PlainText.overwrite` | `true` | - |
| `Encryptor.HashAlgorithm` | `SHA-512` | - |
| `Encryptor.HashIterations` | `1024` | - |
| `Encryptor.DigitalSignatureAlgorithm` | `SHA256withDSA` | - |
| `Encryptor.DigitalSignatureKeyLength` | `2048` | - |
| `Encryptor.RandomAlgorithm` | `SHA1PRNG` | - |
| `Encryptor.CharacterEncoding` | `UTF-8` | - |
| `Encryptor.KDF.PRF` | `HmacSHA256` | - |
| `HttpUtilities.UploadDir` | `C:\\ESAPI\\testUpload` | FLAG — development/test path in production config |
| `HttpUtilities.UploadTempDir` | `C:\\temp` | FLAG — generic temp path |
| `HttpUtilities.ForceHttpOnlySession` | `false` | FLAG — session cookies not HttpOnly |
| `HttpUtilities.ForceSecureSession` | `false` | FLAG — session cookies not Secure |
| `HttpUtilities.ForceHttpOnlyCookies` | `true` | - |
| `HttpUtilities.ForceSecureCookies` | `true` | - |
| `HttpUtilities.MaxHeaderNameSize` | `256` | - |
| `HttpUtilities.MaxHeaderValueSize` | `4096` | - |
| `HttpUtilities.HTTPJSESSIONIDLENGTH` | `50` | - |
| `HttpUtilities.URILENGTH` | `2000` | - |
| `HttpUtilities.maxRedirectLength` | `512` | - |
| `HttpUtilities.HTTPSCHEMELENGTH` | `10` | - |
| `HttpUtilities.HTTPHOSTLENGTH` | `100` | - |
| `HttpUtilities.HTTPPATHLENGTH` | `150` | - |
| `HttpUtilities.contextPathLength` | `150` | - |
| `HttpUtilities.HTTPSERVLETPATHLENGTH` | `100` | - |
| `HttpUtilities.httpQueryParamNameLength` | `100` | - |
| `HttpUtilities.httpQueryParamValueLength` | `500` | - |
| `HttpUtilities.ApprovedUploadExtensions` | `.pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.rtf,.txt,.jpg,.png` | - |
| `HttpUtilities.MaxUploadFileBytes` | `500000000` (500 MB) | FLAG — very large; DoS risk |
| `HttpUtilities.MaxUploadFileCount` | `20` | - |
| `HttpUtilities.FileUploadAllowAnonymousUser` | `true` | FLAG — anonymous uploads permitted |
| `HttpUtilities.ResponseContentType` | `text/html; charset=UTF-8` | - |
| `HttpUtilities.HttpSessionIdName` | `JSESSIONID` | - |
| `HttpUtilities.OverwriteStatusCodes` | `true` | - |
| `HttpUtilities.CharacterEncoding` | `UTF-8` | - |
| `Executor.WorkingDirectory` | _(empty)_ | - |
| `Executor.ApprovedExecutables` | _(empty)_ | - |
| `Logger.ApplicationName` | `ExampleApplication` | FLAG — default/placeholder application name |
| `Logger.LogEncodingRequired` | `false` | FLAG — log encoding disabled |
| `Logger.LogApplicationName` | `true` | - |
| `Logger.LogServerIP` | `true` | - |
| `Logger.UserInfo` | `true` | - |
| `Logger.ClientInfo` | `true` | - |
| `IntrusionDetector.Disable` | `false` | - |
| `IntrusionDetector.event.test.count` | `2` | - |
| `IntrusionDetector.event.test.interval` | `10` | - |
| `IntrusionDetector.event.test.actions` | `disable,log` | - |
| `IntrusionDetector.org.owasp.esapi.errors.IntrusionException.count` | `1` | - |
| `IntrusionDetector.org.owasp.esapi.errors.IntrusionException.interval` | `1` | - |
| `IntrusionDetector.org.owasp.esapi.errors.IntrusionException.actions` | `log,disable,logout` | - |
| `IntrusionDetector.org.owasp.esapi.errors.IntegrityException.count` | `10` | - |
| `IntrusionDetector.org.owasp.esapi.errors.IntegrityException.interval` | `5` | - |
| `IntrusionDetector.org.owasp.esapi.errors.IntegrityException.actions` | `log,disable,logout` | - |
| `IntrusionDetector.org.owasp.esapi.errors.AuthenticationHostException.count` | `2` | - |
| `IntrusionDetector.org.owasp.esapi.errors.AuthenticationHostException.interval` | `10` | - |
| `IntrusionDetector.org.owasp.esapi.errors.AuthenticationHostException.actions` | `log,logout` | - |
| `Validator.ConfigurationFile` | `validation.properties` | - |
| `Validator.AccountName` | `^[a-zA-Z0-9]{3,20}$` | - |
| `Validator.SystemCommand` | `^[a-zA-Z\\-\\/]{1,64}$` | - |
| `Validator.RoleName` | `^[a-z]{1,20}$` | - |
| `Validator.Redirect` | `^\\/test.*$` | FLAG — redirect validator anchored to `/test` path |
| `Validator.HTTPScheme` | `^(http|https)$` | - |
| `Validator.HTTPServerName` | `^[a-zA-Z0-9_.\\-]*$` | - |
| `Validator.HTTPCookieName` | `^[a-zA-Z0-9\\-_]{1,32}$` | - |
| `Validator.HTTPCookieValue` | `^[a-zA-Z0-9\\-\\/+=_ ]{0,1024}$` | - |
| `Validator.HTTPHeaderName` | `^[a-zA-Z0-9\\-_]{1,256}$` | - |
| `Validator.HTTPHeaderValue` | `^[a-zA-Z0-9()\\-=\\*\\.\\?;,+\\/:&_ ]*$` | - |
| `Validator.HTTPServletPath` | `^[a-zA-Z0-9.\\-\\/_]*$` | - |
| `Validator.HTTPPath` | `^[a-zA-Z0-9.\\-_]*$` | - |
| `Validator.HTTPURL` | `^.*$` | FLAG — accepts any URL |
| `Validator.HTTPJSESSIONID` | `^[A-Z0-9]{10,32}$` | - |
| `Validator.HTTPParameterName` | `^[a-zA-Z0-9_\\-]{1,32}$` | - |
| `Validator.HTTPParameterValue` | `^[-\\p{L}\\p{N}./+=_ !$*?@]{0,1000}$` | - |
| `Validator.HTTPContextPath` | `^/[a-zA-Z0-9.\\-_]*$` | - |
| `Validator.HTTPQueryString` | `^([a-zA-Z0-9_\\-]{1,32}=[\\p{L}\\p{N}.\\-/+=_ !$*?@%]*&?)*$` | - |
| `Validator.HTTPURI` | `^/([a-zA-Z0-9.\\-_]*/?)*$` | - |
| `Validator.FileName` | `^[a-zA-Z0-9!@#$%^&{}\\[\\]()_+\\-=,.~'\` ]{1,255}$` | - |
| `Validator.DirectoryName` | `^[a-zA-Z0-9:/\\\\!@#$%^&{}\\[\\]()_+\\-=,.~'\` ]{1,255}$` | - |
| `Validator.AcceptLenientDates` | `false` | - |
| `Validator.HtmlValidationAction` | `throw` | - |

### 3.2 esapi-java-logging.properties (7 lines)

| Property | Value | Flag? |
|----------|-------|-------|
| `handlers` | `java.util.logging.ConsoleHandler` | - |
| `.level` | `INFO` | - |
| `java.util.logging.ConsoleHandler.level` | `INFO` | - |
| `java.util.logging.ConsoleHandler.formatter` | `java.util.logging.SimpleFormatter` | - |
| `java.util.logging.SimpleFormatter.format` | `[%1$tF %1$tT] [%3$-7s] %5$s %n` | - |

No credential-like values present.

### 3.3 log4j.properties (29 lines)

| Property | Value | Flag? |
|----------|-------|-------|
| `log4j.rootLogger` | `INFO, file` | - |
| `log4j.appender.file` | `org.apache.log4j.RollingFileAppender` | - |
| `log4j.appender.file.File` | `/home/gmtp/logs/linde.log` | FLAG — Linux home-dir path in a Windows application; dev/wrong-env path |
| `log4j.appender.file.MaxFileSize` | `10MB` | - |
| `log4j.appender.file.MaxBackupIndex` | `100` | - |
| `log4j.appender.file.layout` | `org.apache.log4j.PatternLayout` | - |
| `log4j.appender.file.layout.ConversionPattern` | `%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1}:%L - %m%n` | - |

No credential-like values. No remote appender configured.

### 3.4 log4j2.properties (24 lines)

| Property | Value | Flag? |
|----------|-------|-------|
| `name` | `PropertiesConfig` | - |
| `property.filename` | `logs` | - |
| `appenders` | `console, file` | - |
| `appender.console.type` | `Console` | - |
| `appender.console.name` | `STDOUT` | - |
| `appender.console.layout.type` | `PatternLayout` | - |
| `appender.console.layout.pattern` | `[%-5level] %d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %c{1} - %msg%n` | - |
| `appender.file.type` | `File` | - |
| `appender.file.name` | `LOGFILE` | - |
| `appender.file.fileName` | `/home/gmtp/logs/linde.log` | FLAG — Linux home-dir path; dev/wrong-env path |
| `appender.file.layout.type` | `PatternLayout` | - |
| `appender.file.layout.pattern` | `[%-5level] %d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %c{1} - %msg%n` | - |
| `loggers` | `file` | - |
| `logger.file.name` | `log4j2properties` | - |
| `logger.file.level` | `info,debug` | FLAG — debug level enabled in logger |
| `logger.file.appenderRefs` | `file` | - |
| `logger.file.appenderRef.file.ref` | `LOGFILE` | - |
| `rootLogger.level` | `debug` | FLAG — root logger at DEBUG in production |
| `rootLogger.appenderRefs` | `file` | - |
| `rootLogger.appenderRef.stdout.ref` | `LOGFILE` | - |
| _(absent)_ | `log4j2.formatMsgNoLookups` | FLAG — not set; JNDI lookup protection not explicitly configured |

No credential-like values. No remote appender (SocketAppender, JMSAppender, SMTPAppender) configured.

### 3.5 validation.properties (29 lines)

| Property | Value | Flag? |
|----------|-------|-------|
| `Validator.SafeString` | `^[.\\p{Alnum}\\p{Space}]{0,1024}$` | - |
| `Validator.Email` | `^[A-Za-z0-9._%'-]+@[A-Za-z0-9.-]+\\.[a-zA-Z]{2,4}$` | - |
| `Validator.IPAddress` | `^(?:(?:25[0-5]\|2[0-4][0-9]\|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]\|2[0-4][0-9]\|[01]?[0-9][0-9]?)$` | - |
| `Validator.URL` | Long RFC-like regex | - |
| `Validator.CreditCard` | `^(\\d{4}[- ]?){3}\\d{4}$` | FLAG — credit card regex present; PCI scope indicator |
| `Validator.SSN` | `^(?!000)([0-6]\\d{2}\|7([0-6]\\d\|7[012]))([ -]?)(?!00)\\d\\d\\3(?!0000)\\d{4}$` | FLAG — SSN regex present; PII scope indicator |

No credential-like values.

---

## STEP 4 — SECURITY REVIEW SUMMARY

### Secrets & Credentials

- **Encryptor.MasterKey / Encryptor.MasterSalt:** Both are commented out (lines 130–131 of ESAPI.properties). ESAPI will fall back to its compiled-in default values, which are publicly known. **FAIL** — see A02-1.
- **Hardcoded passwords / API keys / SMTP passwords:** None found in any file. **PASS**
- **External credential store reference:** No external vault or credential store referenced; inline configuration only. **PASS (no secrets present, but no external store either)**
- **Remote log appenders (SocketAppender, JMSAppender, SMTPAppender):** Not present in log4j.properties or log4j2.properties. **PASS**
- **Log4Shell / JNDI lookups:** The project classpath contains log4j 2.x. The `log4j2.properties` file does not set `log4j2.formatMsgNoLookups=true`. Whether the runtime JVM property is set is outside the scope of these files; within these files the protection is absent. **FAIL** — see A02-2.
- **Path exposure (server directory structure):** `HttpUtilities.UploadDir=C:\\ESAPI\\testUpload`, `log4j.appender.file.File=/home/gmtp/logs/linde.log`, `appender.file.fileName=/home/gmtp/logs/linde.log` all expose server paths and appear to be development/wrong-environment values. **FAIL** — see A02-3.
- **Validator.HTTPURL overly permissive:** `^.*$` accepts any URL string. **FAIL** — see A02-4.
- **Validator.Redirect placeholder:** `^\\/test.*$` — only allows redirects beginning with `/test`. If used in production this will break legitimate redirect flows AND is clearly a placeholder value. **FAIL** — see A02-5.

### Data Exposure Through Logging

- **rootLogger.level = debug** in log4j2.properties — root logger set to DEBUG in production. **FAIL** — see A02-6.
- **Log file paths appear to be development paths** (`/home/gmtp/logs/linde.log` is a Linux user home-directory path, inconsistent with a production Windows deployment). **FAIL** — see A02-3 (covered).
- **Logger.LogEncodingRequired=false** — log output encoding disabled, creating potential log injection/forging risk. **FAIL** — see A02-7.

### ESAPI Configuration Correctness

- **ESAPI.printProperties=true** — prints all ESAPI properties to output on startup; in a production environment this leaks configuration to logs/console. **FAIL** — see A02-8.
- **HttpUtilities.ForceHttpOnlySession=false** — session cookie not forced HttpOnly. **FAIL** — see A02-9.
- **HttpUtilities.ForceSecureSession=false** — session cookie not forced Secure (TLS-only). **FAIL** — see A02-9.
- **HttpUtilities.FileUploadAllowAnonymousUser=true** — anonymous file uploads allowed. **FAIL** — see A02-10.
- **HttpUtilities.MaxUploadFileBytes=500000000** (500 MB) — extremely large per-file upload limit; DoS risk. **FAIL** — see A02-11.
- **Logger.ApplicationName=ExampleApplication** — default placeholder name not customised for this application. **FAIL** — see A02-12.
- **IntrusionDetector:** Active (`Disable=false`), thresholds configured. **PASS**
- **Encoder.DefaultCodecList:** `HTMLEntityCodec,PercentCodec,JavaScriptCodec` — reasonable defaults. **PASS**
- **Validator.HtmlValidationAction=throw** — correct secure setting. **PASS**
- **Validator.CreditCard / Validator.SSN present** — implies PCI/PII data scope; review whether logging of validated fields could expose this data. **INFORMATIONAL** — see A02-13.
- **ValidationException intrusion detection rule is commented out** (lines 448–450 of ESAPI.properties) — rapid validation errors (scan/attack indicator) will not trigger detection. **FAIL** — see A02-14.

---

## STEP 5 — FINDINGS

---

### A02-1 — ESAPI Master Key and Salt Not Configured (CRITICAL)

**File:** `WEB-INF/src/ESAPI.properties`, lines 130–131
**Severity:** Critical
**Category:** Cryptographic — Missing / Default Encryption Keys

**Description:**
Both `Encryptor.MasterKey` and `Encryptor.MasterSalt` are commented out. ESAPI's `JavaEncryptor` requires these values to derive encryption and MAC keys. When they are absent, ESAPI falls back to compiled-in default values that are published in the ESAPI source code and widely known. Any data encrypted by the application (encrypted state, CSRF tokens, remember-me tokens) is trivially decryptable by an attacker who knows the defaults, which breaks confidentiality and integrity guarantees of all ESAPI-encrypted data.

**Evidence:**
```
#Encryptor.MasterKey=
#Encryptor.MasterSalt=
```
(Lines 130–131, both commented out — no application-specific values set.)

**Recommendation:**
Generate application-specific values using `java -classpath esapi.jar org.owasp.esapi.reference.crypto.JavaEncryptor`, uncomment and set `Encryptor.MasterKey` and `Encryptor.MasterSalt` to the generated values. Store these values in a secrets manager or environment variable rather than in a properties file committed to source control. Rotate any data that may have been encrypted under the default keys.

---

### A02-2 — Log4j2 JNDI Protection Not Explicitly Configured (HIGH)

**File:** `WEB-INF/src/log4j2.properties`, all lines
**Severity:** High
**Category:** Log4Shell / JNDI Injection Mitigation (CVE-2021-44228)

**Description:**
The audit has confirmed that log4j 2.x is present in the application classpath. The `log4j2.properties` file does not contain `log4j2.formatMsgNoLookups=true` (or its equivalent `log4j2.formatMsgNoLookups = true`), which is one of the recommended mitigations for Log4Shell (CVE-2021-44228). While the full mitigation for modern log4j versions (2.17.0+) is achieved by removing the JndiLookup class or upgrading, the absence of this property means no defence-in-depth guard is present at the configuration layer. If the application is running on log4j 2.17.0 the default behaviour disables JNDI lookups, but this is not enforced through configuration and therefore cannot be audited or validated without runtime inspection.

**Evidence:**
```
# log4j2.formatMsgNoLookups is NOT present anywhere in log4j2.properties
rootLogger.level = debug
```

**Recommendation:**
Add `log4j2.formatMsgNoLookups=true` to `log4j2.properties`. Verify the deployed log4j version is 2.17.1 or later (or 2.12.4 / 2.3.2 for earlier release trains). Consider removing the JndiLookup class from the log4j JAR as an additional hardening measure: `zip -q -d log4j-core-*.jar org/apache/logging/log4j/core/lookup/JndiLookup.class`.

---

### A02-3 — Development / Wrong-Environment File Paths in Production Configuration (HIGH)

**Files:**
- `WEB-INF/src/ESAPI.properties`, line 311: `HttpUtilities.UploadDir=C:\\ESAPI\\testUpload`
- `WEB-INF/src/log4j.properties`, line 25: `log4j.appender.file.File=/home/gmtp/logs/linde.log`
- `WEB-INF/src/log4j2.properties`, line 12: `appender.file.fileName=/home/gmtp/logs/linde.log`

**Severity:** High
**Category:** Configuration Management — Environment Mismatch / Path Disclosure

**Description:**
Three files contain file-system paths that are clearly development or wrong-environment values:

1. `C:\\ESAPI\\testUpload` — the path name contains "test", suggesting a developer workstation or test environment path, not a controlled production upload directory.
2. `/home/gmtp/logs/linde.log` — a Linux home-directory path (user `gmtp`, product name `linde`) referenced in both `log4j.properties` and `log4j2.properties`. The application is deployed on Windows (as evidenced by the Windows path in ESAPI.properties). This path cannot resolve correctly on Windows, meaning the file appender will likely fail silently or fall back to console output, creating a gap in production log capture. Additionally, the path leaks developer username (`gmtp`) and a product/customer name (`linde`) in committed source code.

**Evidence:**
```
HttpUtilities.UploadDir=C:\\ESAPI\\testUpload
log4j.appender.file.File=/home/gmtp/logs/linde.log
appender.file.fileName=/home/gmtp/logs/linde.log
```

**Recommendation:**
Replace all environment-specific paths with environment-variable references or deployment-time substitution tokens (e.g., `${LOG_DIR}/application.log`, `${UPLOAD_DIR}`). Ensure production configuration management (CI/CD pipeline or secrets manager) injects correct paths per environment. Audit git history to confirm no credentials or sensitive data were committed alongside these paths.

---

### A02-4 — Validator.HTTPURL Accepts Any Value (HIGH)

**File:** `WEB-INF/src/ESAPI.properties`, line 493
**Severity:** High
**Category:** Input Validation — Overly Permissive Regex

**Description:**
The `Validator.HTTPURL` rule is set to `^.*$`, which matches any string of any length and content. This effectively disables URL validation for any code path that calls `ESAPI.validator().getValidInput(..., "HTTPURL", ...)`. An attacker can supply arbitrary URLs including `javascript:` URIs, `data:` URIs, internal SSRF targets, or malformed values that downstream code may mishandle.

**Evidence:**
```
Validator.HTTPURL=^.*$
```

**Recommendation:**
Replace with a restrictive URL pattern, such as the pattern defined in `validation.properties` (`Validator.URL`) or a scheme-restricted pattern:
`^(https?://)[a-zA-Z0-9][a-zA-Z0-9\\-.]+(:[0-9]+)?(/[a-zA-Z0-9\\-._~:/?#\\[\\]@!$&'()*+,;=%]*)?$`
At minimum restrict to `http` and `https` schemes and reject `javascript:`, `data:`, and `vbscript:`.

---

### A02-5 — Validator.Redirect Contains Placeholder Test Value (MEDIUM)

**File:** `WEB-INF/src/ESAPI.properties`, line 480
**Severity:** Medium
**Category:** Configuration Management — Placeholder Value in Production

**Description:**
The redirect validator pattern is `^\\/test.*$`, which only permits redirects to paths beginning with `/test`. The inline comment above this line reads: "the word TEST below should be changed to your application name — only relative URL's are supported." This is an unmodified default/placeholder value. Depending on how open redirect protection is implemented, this may mean that either (a) all production redirect operations are rejected because they do not start with `/test`, or (b) the validator is not being used for redirect validation, leaving open-redirect protection absent entirely.

**Evidence:**
```
#the word TEST below should be changed to your application
#name - only relative URL's are supported
Validator.Redirect=^\\/test.*$
```

**Recommendation:**
Replace `test` with the actual application context path or permitted redirect root (e.g., `^\\/fleetfocus.*$`). Verify that ESAPI redirect validation is actively applied at every redirect point in the application code.

---

### A02-6 — Root Logger Set to DEBUG Level in Production (HIGH)

**File:** `WEB-INF/src/log4j2.properties`, line 22
**Severity:** High
**Category:** Data Exposure — Excessive Logging Verbosity

**Description:**
The `log4j2.properties` file sets `rootLogger.level = debug`. DEBUG-level logging routinely outputs SQL queries (including parameter values), HTTP request/response bodies, session identifiers, internal stack traces, and in some frameworks credential material. In a production environment this configuration can expose PII, credentials, and internal architecture details through log files, log aggregators, or console output. Additionally, `logger.file.level = info,debug` also shows debug enabled at the named logger level.

**Evidence:**
```
logger.file.level = info,debug
rootLogger.level = debug
```

**Recommendation:**
Set `rootLogger.level = warn` or `rootLogger.level = error` for production deployments. Use `info` for application-specific named loggers only where necessary. Ensure log levels are controlled per-environment via deployment configuration rather than being hardcoded in committed properties files.

---

### A02-7 — Log Encoding Disabled (MEDIUM)

**File:** `WEB-INF/src/ESAPI.properties`, line 400
**Severity:** Medium
**Category:** Log Injection / Log Forging

**Description:**
`Logger.LogEncodingRequired=false` disables ESAPI's HTML encoding of log messages before they are written. If an attacker can influence logged values (e.g., user-supplied input in error messages, usernames, HTTP header values), they can inject newline characters, ANSI escape codes, or HTML/script tags into log entries. This enables log forging (fabricating false log records) and, in environments where logs are viewed in a browser or log-management UI without output encoding, could enable stored XSS.

**Evidence:**
```
Logger.LogEncodingRequired=false
```

**Recommendation:**
Set `Logger.LogEncodingRequired=true`. This causes ESAPI to HTML-encode log data before writing, preventing log injection. Verify that any downstream log viewer correctly renders or strips HTML entities.

---

### A02-8 — ESAPI Prints All Properties on Startup (LOW)

**File:** `WEB-INF/src/ESAPI.properties`, line 43
**Severity:** Low
**Category:** Information Disclosure — Configuration Exposure

**Description:**
`ESAPI.printProperties=true` causes ESAPI to print all loaded property values to the log output at application startup. This includes any sensitive configuration values that may be present. In this case, master key and salt are absent, but if they were ever set, they would be logged in plaintext at startup. This also exposes the full security configuration to anyone with access to application logs or startup output.

**Evidence:**
```
ESAPI.printProperties=true
```

**Recommendation:**
Set `ESAPI.printProperties=false` in the production configuration. Leave it enabled only in test/development environments for troubleshooting.

---

### A02-9 — Session Cookie Security Flags Not Enforced (HIGH)

**File:** `WEB-INF/src/ESAPI.properties`, lines 314–315
**Severity:** High
**Category:** Session Management — Insecure Cookie Configuration

**Description:**
Both `HttpUtilities.ForceHttpOnlySession=false` and `HttpUtilities.ForceSecureSession=false` are set. When these flags are false, ESAPI does not enforce the `HttpOnly` and `Secure` attributes on the session cookie (`JSESSIONID`). Without `HttpOnly`, the session cookie is accessible to JavaScript, making it vulnerable to session theft via XSS. Without `Secure`, the session cookie may be transmitted over unencrypted HTTP connections, allowing session hijacking via network interception. Note that general cookies do have `ForceHttpOnlyCookies=true` and `ForceSecureCookies=true` — the gap is specifically for the session cookie.

**Evidence:**
```
HttpUtilities.ForceHttpOnlySession=false
HttpUtilities.ForceSecureSession=false
```

**Recommendation:**
Set both `HttpUtilities.ForceHttpOnlySession=true` and `HttpUtilities.ForceSecureSession=true`. If HTTPS-only access is enforced by infrastructure (load balancer / reverse proxy), enabling `ForceSecureSession` will have no adverse effect on accessibility but adds the defence-in-depth attribute to session cookies.

---

### A02-10 — Anonymous File Uploads Permitted (MEDIUM)

**File:** `WEB-INF/src/ESAPI.properties`, line 367
**Severity:** Medium
**Category:** Access Control — Unauthenticated File Upload

**Description:**
`HttpUtilities.FileUploadAllowAnonymousUser=true` permits unauthenticated users to upload files. Combined with the 500 MB file size limit (A02-11) and 20 files per request, this creates a Denial-of-Service vector: an unauthenticated attacker can saturate server disk space and I/O by repeatedly uploading large files. It may also be an unintended access control gap if file upload functionality is intended to be authenticated-only.

**Evidence:**
```
HttpUtilities.FileUploadAllowAnonymousUser=true
```

**Recommendation:**
Set `HttpUtilities.FileUploadAllowAnonymousUser=false` unless anonymous upload is a deliberate, documented functional requirement with additional rate-limiting and quota controls in place. If anonymous upload is required, implement IP-based rate limiting and total quota enforcement outside ESAPI.

---

### A02-11 — Upload File Size Limit Excessively Large (MEDIUM)

**File:** `WEB-INF/src/ESAPI.properties`, line 344
**Severity:** Medium
**Category:** Denial of Service — Resource Exhaustion

**Description:**
`HttpUtilities.MaxUploadFileBytes=500000000` sets a 500 MB per-file upload limit. For a fleet management application where approved extensions are documents, spreadsheets, and images (`.pdf`, `.doc`, `.jpg`, `.png`, etc.), a 500 MB limit per file is disproportionately large. Combined with `MaxUploadFileCount=20` and anonymous uploads (A02-10), an attacker could attempt to upload 10 GB of data per request, exhausting disk space and degrading service availability.

**Evidence:**
```
HttpUtilities.MaxUploadFileBytes=500000000
HttpUtilities.MaxUploadFileCount=20
```

**Recommendation:**
Reduce `MaxUploadFileBytes` to a value appropriate for the approved file types (e.g., 10–25 MB for documents and images). Review whether 20 files per request is operationally necessary; if not, reduce this value. Implement server-side quotas (per user/session) and rate limiting independently of ESAPI configuration.

---

### A02-12 — Logger Application Name Is Default Placeholder (LOW)

**File:** `WEB-INF/src/ESAPI.properties`, line 398
**Severity:** Low
**Category:** Configuration Management — Placeholder Value

**Description:**
`Logger.ApplicationName=ExampleApplication` is the default value shipped with the ESAPI distribution and has not been changed. In a multi-application logging environment (SIEM, log aggregator), all ESAPI log events from this application will be tagged as `ExampleApplication`, making it impossible to correlate or filter log events to the correct application and potentially masking security events from analysts.

**Evidence:**
```
Logger.ApplicationName=ExampleApplication
```

**Recommendation:**
Set `Logger.ApplicationName` to the correct application identifier (e.g., `FleetFocus` or the deployment-specific name).

---

### A02-13 — Credit Card and SSN Validation Rules Present — PCI/PII Scope (INFORMATIONAL)

**File:** `WEB-INF/src/validation.properties`, lines 27–28
**Severity:** Informational
**Category:** Data Classification — PCI DSS / PII Scope

**Description:**
The presence of `Validator.CreditCard` and `Validator.SSN` regex rules indicates that the application may process, validate, or store payment card numbers and US Social Security Numbers. This places the application in scope for PCI DSS (if credit card data is processed) and relevant US state PII protection regulations. This finding is informational — the presence of validation rules does not confirm live use, but it warrants verification.

**Evidence:**
```
Validator.CreditCard=^(\\d{4}[- ]?){3}\\d{4}$
Validator.SSN=^(?!000)([0-6]\\d{2}|7([0-6]\\d|7[012]))([ -]?)(?!00)\\d\\d\\3(?!0000)\\d{4}$
```

**Recommendation:**
Confirm with the development team whether these validators are actively invoked. If credit card or SSN data is processed or stored, ensure PCI DSS and applicable PII regulations are addressed, including tokenisation, encryption at rest, and audit logging of access to this data. If the validators are unused legacy code, remove them to reduce audit scope.

---

### A02-14 — ValidationException Intrusion Detection Rule Commented Out (MEDIUM)

**File:** `WEB-INF/src/ESAPI.properties`, lines 448–450
**Severity:** Medium
**Category:** Intrusion Detection — Scan/Attack Detection Gap

**Description:**
The intrusion detection rule for `org.owasp.esapi.errors.ValidationException` is commented out. This rule is intended to detect rapid sequences of validation failures, which are characteristic of automated scanning tools, fuzzing, and parameter tampering attacks. Without this rule, the IntrusionDetector does not react to high volumes of input validation failures, reducing the application's ability to detect and respond to active attacks.

**Evidence:**
```
# rapid validation errors indicate scans or attacks in progress
# org.owasp.esapi.errors.ValidationException.count=10
# org.owasp.esapi.errors.ValidationException.interval=10
# org.owasp.esapi.errors.ValidationException.actions=log,logout
```

**Recommendation:**
Uncomment and activate the `ValidationException` intrusion detection rule. Tune the count and interval thresholds based on normal application traffic patterns to minimise false positives. Consider setting the action to `log,logout` initially, with `disable` added after the rule has been observed in production.

---

## Summary Table

| Finding | File | Line(s) | Severity | Category |
|---------|------|---------|----------|----------|
| A02-1 | ESAPI.properties | 130–131 | **Critical** | Cryptographic — Missing Encryption Keys |
| A02-2 | log4j2.properties | (absent) | **High** | Log4Shell / JNDI Mitigation Absent |
| A02-3 | ESAPI.properties, log4j.properties, log4j2.properties | 311, 25, 12 | **High** | Config Mgmt — Dev Paths in Production |
| A02-4 | ESAPI.properties | 493 | **High** | Input Validation — Permissive URL Regex |
| A02-5 | ESAPI.properties | 480 | **Medium** | Config Mgmt — Placeholder Redirect Validator |
| A02-6 | log4j2.properties | 18, 22 | **High** | Data Exposure — DEBUG Log Level in Production |
| A02-7 | ESAPI.properties | 400 | **Medium** | Log Injection / Log Forging |
| A02-8 | ESAPI.properties | 43 | **Low** | Information Disclosure — Config Print on Startup |
| A02-9 | ESAPI.properties | 314–315 | **High** | Session Mgmt — Session Cookie Missing HttpOnly/Secure |
| A02-10 | ESAPI.properties | 367 | **Medium** | Access Control — Anonymous File Upload |
| A02-11 | ESAPI.properties | 344 | **Medium** | DoS — Excessive Upload Size Limit |
| A02-12 | ESAPI.properties | 398 | **Low** | Config Mgmt — Default App Name Placeholder |
| A02-13 | validation.properties | 27–28 | **Informational** | Data Classification — PCI/PII Scope |
| A02-14 | ESAPI.properties | 448–450 | **Medium** | Intrusion Detection — Scan Detection Gap |

**Total findings: 14** (1 Critical, 4 High, 5 Medium, 2 Low, 1 Informational — excluding informational: 13 actionable)

---

*End of report — Agent A02 — 2026-02-25*
