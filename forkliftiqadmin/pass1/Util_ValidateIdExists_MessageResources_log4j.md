# Security Audit Report — Pass 1
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated static analysis (Claude Code)
**Scope:** Util.java, ValidateIdExistsAbstractActionForm.java, MessageResources.properties, MessageResources_en.properties, log4j.properties

---

## Table of Contents
1. [CRITICAL — Unsalted MD5 used for password hashing (database layer)](#finding-1)
2. [HIGH — SMTP header injection via unsanitised subject and recipient fields](#finding-2)
3. [HIGH — Arbitrary file read via `attachment` path in sendMail() overload](#finding-3)
4. [HIGH — Cognito / external API error messages reflected verbatim to end users](#finding-4)
5. [MEDIUM — SSRF via `getHTML()` with partially user-influenced URL](#finding-5)
6. [MEDIUM — `genPass()` uses `java.util.Random` (PRNG) seeded from `MD5`](#finding-6)
7. [MEDIUM — JDBC SQL logging at DEBUG level in production configuration](#finding-7)
8. [MEDIUM — `log4j.debug=true` in production — internal log4j state exposed](#finding-8)
9. [MEDIUM — `ValidateIdExistsAbstractActionForm` validation silently discarded when `validate="false"` is set in struts-config](#finding-9)
10. [LOW — `generateRadomName()` name is misleading; actual randomness relies on UUID but timestamp prefix is predictable](#finding-10)
11. [LOW — Stack traces written to `System.out` / `e.printStackTrace()` in mail-send error paths](#finding-11)
12. [LOW — Log file path controlled by unvalidated `${logDir}` system property](#finding-12)
13. [LOW — JDBC and SQL log files configured with `Append=false` (log truncation on restart)](#finding-13)
14. [INFO — Hardcoded internal email addresses and AWS endpoint in RuntimeConf.java](#finding-14)
15. [INFO — MessageResources property `error.cognito` / `error.incorrect.reset.cognito` acts as a passthrough message sink](#finding-15)

---

<a name="finding-1"></a>
### CRITICAL: Unsalted MD5 used for password hashing (database layer)

**File:** `src/main/java/com/dao/LoginDAO.java` (line 51, 92), `src/main/java/com/dao/DriverDAO.java` (line 512), `src/main/java/com/dao/CompanyDAO.java` (lines 61, 95, 443) — called throughout from `Util.java` infrastructure

**Description:**
All user passwords, driver PINs, and company admin PINs are stored using the database-side `md5()` function with no salt. This is confirmed in multiple SQL statements found in the DAO layer — which form the verification counterpart to `Util.genPass()` (which also uses MD5 internally):

```java
// LoginDAO.java line 51
"select count(*) from " + RuntimeConf.v_user + " where email = ? and password = md5(?)"

// LoginDAO.java line 92
"select id from company where email = ? and password = md5(?)"

// CompanyDAO.java line 61
"INSERT INTO users (id, email, password, ...) values (?,?,md5(?),?,?,?)"

// CompanyDAO.java line 95
"update users set password = md5(?) where id = ?"

// CompanyDAO.java line 443
"update company set password = md5(?) where id = ?"
```

MD5 is a cryptographic hash function that is entirely unsuitable for password storage. Without a unique per-user salt, all users with the same password produce the same hash, enabling:
- Pre-computed rainbow-table attacks — multi-billion-entry MD5 tables for common passwords exist publicly and free of charge.
- Bulk cracking — if the database is exfiltrated, all hashes can be submitted to online lookup services (e.g. crackstation.net) simultaneously.
- GPU-accelerated brute force — modern consumer GPUs can compute tens of billions of unsalted MD5 hashes per second.

**Risk:** If the `users` or `company` table is exfiltrated via SQL injection or a database breach, every password in the system can realistically be recovered within minutes to hours. This directly leads to full account takeover for all users, drivers, and administrators.

**Recommendation:** Replace all `md5()` calls in SQL with server-side password hashing using a memory-hard algorithm such as bcrypt, scrypt, or Argon2 (via Spring Security's `BCryptPasswordEncoder` or the `jBCrypt` library). A per-user salt must be generated with `SecureRandom` and stored alongside the hash. Migration requires a forced password-reset flow for existing accounts.

---

<a name="finding-2"></a>
### HIGH: SMTP header injection via unsanitised subject and recipient fields in `sendMail()`

**File:** `src/main/java/com/util/Util.java` (lines 32–71, 73–131)

**Description:**
Both overloads of `sendMail()` accept `subject` and `rEmail` parameters and pass them directly to the JavaMail API without sanitisation:

```java
// Util.java lines 47-53
message.setRecipients(Message.RecipientType.TO,
        InternetAddress.parse(rEmail, false));  // strict=false
...
message.setSubject(subject);
```

The second argument to `InternetAddress.parse()` is `false`, which means the parser operates in **lenient mode** and will accept a comma-separated list of addresses without enforcing RFC 2822 strictness. An attacker who can influence `rEmail` (e.g. via the subscription email field, driver email registration, or the "send mail" admin form) can inject additional `To:`, `Cc:`, or `Bcc:` addresses by supplying values such as:

```
victim@example.com, attacker@evil.com
```

Because `InternetAddress.parse(..., false)` splits on commas and does not validate each resulting address rigorously, this enables **email list injection** (spamming arbitrary recipients through the application's mail relay).

For the `subject` field, JavaMail's `setSubject()` does not strip embedded CRLF sequences on all versions. If `subject` originates from user input (e.g. `FormBuilderAction` passes the diagnostics title from `RuntimeConf`, but other callers such as `TrainingDAO` concatenate user-controlled training type strings), an attacker could inject newline characters (`\r\n`) to add arbitrary headers to the outgoing message.

Compounding this: the `sEmail` (From) parameter is accepted without validation in both overloads:
```java
if (sEmail != null) {
    message.setFrom(new InternetAddress(sEmail));
}
```
A non-empty `sEmail` value is set directly on the message without checking it is a legitimate address, enabling From-header spoofing.

**Risk:** An attacker can abuse the application's mail relay to send spam or phishing emails to arbitrary third parties, potentially causing the application's sending domain to be blacklisted. From-header spoofing enables impersonation of legitimate senders (e.g. `info@forkliftiq360.com`).

**Recommendation:**
- Change `InternetAddress.parse(rEmail, false)` to `InternetAddress.parse(rEmail, true)` (strict mode) to enforce RFC 2822 compliance.
- Validate `rEmail` against a whitelist or strict single-address regex before passing to JavaMail; reject addresses containing commas, angle brackets, or CRLF characters.
- Strip or encode `\r` and `\n` from `subject` before calling `setSubject()`.
- Validate `sEmail` against an allowlist of known sender addresses rather than accepting any caller-supplied value.

---

<a name="finding-3"></a>
### HIGH: Arbitrary local file read via unsanitised `attachment` path in sendMail() overload

**File:** `src/main/java/com/util/Util.java` (lines 108–114); caller at `src/main/java/com/action/MailerAction.java` (lines 113–129)

**Description:**
The second `sendMail()` overload accepts an `attachment` parameter which is a filesystem path and opens it directly using `FileDataSource`:

```java
// Util.java lines 110-114
if (!attachment.equalsIgnoreCase("")) {
    messageBodyPart = new MimeBodyPart();
    FileDataSource source = new FileDataSource(attachment);        // raw path
    messageBodyPart.setDataHandler(new DataHandler(source));
    messageBodyPart.setFileName(attachmentName);
    multipart.addBodyPart(messageBodyPart);
}
```

In `MailerAction.java`, the `attachment` value is obtained from `reportAPI.downloadPDF()`, which itself constructs a path using `generateRadomName()` under the `RuntimeConf.PDF_FOLDER` (`/temp/`) directory. While in the normal flow this path is server-generated, the critical question is whether an attacker can influence `reportAPI` state or if the path is derived from any user-controlled input. If an API parameter or intercepted request can substitute a path such as:

```
/WEB-INF/web.xml
/etc/passwd
../../WEB-INF/classes/com/util/RuntimeConf.class
```

…then `FileDataSource` will silently open and attach that file to the outgoing email, sending it to whatever address is passed as `rEmail`. There is no canonicalisation, no confinement check, and no extension or path prefix validation anywhere in this code path.

Even in the current flow, the path is logged at INFO level before sending:
```java
log.info("file genrated = " + attachment);
```
This means the full server-side path of every generated PDF is written to `info.log`.

**Risk:** If path traversal to the `attachment` parameter is achievable (via the API layer that calls `MailerAction`), an attacker can cause the server to email arbitrary files from the filesystem to a chosen recipient. Combined with the email injection finding above, an attacker could exfiltrate configuration files, credentials, or class files to an external address.

**Recommendation:**
- Validate `attachment` against a strict allowlist of permitted directories (e.g. only paths under the configured `PDF_FOLDER`).
- Canonicalise the path using `File.getCanonicalPath()` and assert it begins with the expected base directory before passing it to `FileDataSource`.
- Do not expose raw filesystem paths in log messages at INFO level.

---

<a name="finding-4"></a>
### HIGH: Cognito / external API error messages reflected verbatim to the user

**File:** `src/main/resources/properties/MessageResources.properties` (lines 117, 507); used by `src/main/java/com/action/AdminDriverEditAction.java` (line 100), `AdminDriverAddAction.java` (line 76), `AdminRegisterAction.java` (lines 136, 152, 282), `ResetPasswordAction.java` (line 50)

**Description:**
Two message keys act as raw passthrough placeholders that render whatever string the external service returns, directly into the HTML page presented to the user:

```properties
# MessageResources.properties line 117
error.incorrect.reset.cognito = {0}

# MessageResources.properties line 507
error.cognito = {0}
```

In the calling actions, the raw `getMessage()` value from the external API response is substituted directly for `{0}`:

```java
// AdminDriverEditAction.java lines 99-100
String errormsg = userUpdateResponse.getMessage();
ActionMessage msg = new ActionMessage("error.cognito", errormsg);

// ResetPasswordAction.java lines 48-50
String errormsg = passwordResponse.getMessage();
ActionMessage msg = new ActionMessage("error.incorrect.reset.cognito", errormsg);
```

AWS Cognito error messages can contain:
- Internal service ARNs or resource identifiers (information disclosure)
- The user's email address or username (privacy violation)
- Technical stack details (e.g. "PreTokenGeneration failed with error...")
- Potentially attacker-crafted content if the input that triggered the error is reflected back by Cognito (second-order injection risk)

Because the Struts `<html:errors>` tag renders `ActionMessage` parameters as HTML without encoding by default in Struts 1.x, and because the `errors.prefix`/`errors.suffix` in `MessageResources.properties` wraps output in `<li><b>...</b></li>`, an attacker who can cause Cognito to echo back a payload-containing string (e.g. by registering a username containing HTML) may achieve **stored cross-site scripting** through this pathway.

**Risk:** Information disclosure of internal AWS infrastructure details to all users who trigger these error conditions. Potential XSS if Cognito reflects user-supplied input in error messages.

**Recommendation:**
- Define explicit, user-friendly error messages for all known Cognito error codes rather than forwarding raw service messages.
- HTML-encode all user-visible strings at the point of rendering; do not rely on Struts 1 defaults.
- Log the full Cognito error message server-side (at WARN or ERROR level) instead of displaying it to the user.

---

<a name="finding-5"></a>
### MEDIUM: SSRF via `getHTML()` with `RuntimeConf.projectTitle` interpolated into URL

**File:** `src/main/java/com/util/Util.java` (lines 134–155); callers at `src/main/java/com/report/PreFlightReport.java` (lines 68, 79), `src/main/java/com/report/FleetCheckAlert.java` (line 60)

**Description:**
`getHTML()` performs an outbound HTTP GET to a caller-supplied URL with no validation whatsoever:

```java
// Util.java lines 141-149
url = new URL(urlToRead);
conn = (HttpURLConnection) url.openConnection();
conn.setReadTimeout(900000);   // 15-minute timeout
conn.setRequestMethod("GET");
rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
while ((line = rd.readLine()) != null) {
    result += line + "\n";
}
```

The known callers construct the URL by concatenating `RuntimeConf.projectTitle` into the path:

```java
// PreFlightReport.java lines 68, 79
Util.getHTML("http://localhost:8090/" + RuntimeConf.projectTitle + "/css/bootstrap_table.css")
```

`RuntimeConf.projectTitle` is a `public static String` field (currently `"PreStart"`). Although it is not a direct request parameter, it is a publicly accessible static field with no `final` modifier. If any other code path can write to `RuntimeConf.projectTitle` (e.g. via an admin configuration action, or through Java reflection in a future feature), an attacker could redirect this request to an arbitrary internal host and port.

More immediately, `getHTML()` accepts any `String urlToRead` argument. It supports any protocol accepted by `java.net.URL`, including `file://`, `ftp://`, and custom URL handlers registered in the JVM. If `getHTML()` is ever called with a URL derived from user input (which the current design pattern — a public static utility method — makes easy to do accidentally), it becomes a full SSRF vector that can:
- Probe internal network services (port scanning via timing)
- Read local files via `file:///etc/passwd`
- Interact with cloud metadata services (e.g. `http://169.254.169.254/latest/meta-data/`)

The 15-minute read timeout (`900000 ms`) means each injected request will hold a server thread for up to 15 minutes, creating a denial-of-service amplification risk.

**Risk:** Internal port scanning, cloud metadata exfiltration, and potential local file read if user input ever reaches this method. The excessively long timeout compounds DoS risk.

**Recommendation:**
- Restrict `getHTML()` to an explicit allowlist of permitted host:port combinations.
- Validate that the scheme is `http` or `https` and the host matches the allowlist before opening the connection.
- Do not interpolate any mutable string (including configuration values) into the URL without validation.
- Reduce the read timeout to a value appropriate for fetching a CSS file (e.g. 5–10 seconds).
- If the sole purpose is fetching a local CSS file for inclusion in HTML email, consider reading it from the classpath or the filesystem using a `ClassLoader.getResourceAsStream()` call instead, eliminating the network round-trip entirely.

---

<a name="finding-6"></a>
### MEDIUM: `genPass()` uses `java.util.Random` (non-cryptographic PRNG) seeded with system time

**File:** `src/main/java/com/util/Util.java` (lines 159–175)

**Description:**
`genPass()` is used to generate temporary passwords. It uses `java.util.Random`, which is a **linear congruential generator (LCG)** — a non-cryptographically-secure PRNG whose internal state can be reconstructed from a small number of observed outputs:

```java
// Util.java lines 160-174
Random r = new Random();          // seeded from System.nanoTime() — predictable
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] entropy = new byte[1024];
r.nextBytes(entropy);             // LCG output — not cryptographically random
md.update(entropy, 0, 1024);
return new BigInteger(1, md.digest()).toString(16).substring(0, chars);
```

MD5 is applied on top of the PRNG output, but this does not add entropy — it only obscures the LCG state. MD5 is deterministic: identical `entropy` arrays produce identical digests. An attacker who knows (or can estimate) the approximate time the server was started can enumerate a feasible range of `Random` seeds and reproduce the full sequence of `genPass()` outputs.

The generated password is returned as a hexadecimal substring of the MD5 digest, limiting its alphabet to `[0-9a-f]` — 16 characters — which significantly reduces brute-force complexity even for longer outputs.

If `genPass()` is used to generate password reset tokens, temporary access credentials, or one-time passwords, an attacker can predict or reproduce these values.

**Risk:** Predictable temporary passwords enable account takeover for any user who requests a password reset while the attacker can estimate the server start time or observe a small number of generated values.

**Recommendation:**
- Replace `java.util.Random` with `java.security.SecureRandom` for any security-sensitive token generation.
- Replace MD5 with `SHA-256` or higher, or use `SecureRandom.nextBytes()` directly and encode with Base64 for adequate entropy without the hexadecimal alphabet restriction.
- A simpler and more correct approach: `SecureRandom.getInstance("SHA1PRNG").generateSeed(32)` encoded as Base64 or hex.

---

<a name="finding-7"></a>
### MEDIUM: JDBC SQL logging at DEBUG level logs full SQL statements and query results

**File:** `src/main/resources/properties/log4j.properties` (lines 56–61, 69–94)

**Description:**
The log4j configuration activates JDBC spy appenders at `DEBUG` level, writing full SQL statement text to `sql.log` and query timing to `sqltiming.log`:

```properties
# log4j.properties lines 56-57
log4j.logger.jdbc.sqlonly=DEBUG,sql
log4j.additivity.jdbc.sqlonly=false

# log4j.properties lines 60-61
log4j.logger.jdbc.sqltiming=DEBUG,sqltiming
log4j.additivity.jdbc.sqltiming=false

# log4j.properties lines 52-53
log4j.logger.jdbc.audit=INFO,jdbc
log4j.logger.jdbc.resultset=INFO,jdbc
```

The `jdbc.resultset=INFO` level logs **ResultSet contents** — i.e. data returned from database queries — including password hashes, email addresses, personal data, and session tokens, to `jdbc.log`. Combined with `jdbc.sqlonly` at DEBUG, every parameterised query is logged with its bound parameter values substituted in, meaning plaintext passwords passed to `md5()` database functions may appear in `sql.log`.

For example, an INSERT such as:
```sql
INSERT INTO users (id, email, password, ...) values (?,?,md5(?),?,?,?)
```
will be logged with the actual password value substituted for the third `?` in `sql.log`.

The log files use `Append=false`, meaning they are truncated on every server restart. While this limits the persistence of sensitive data, it also means evidence of attacks is destroyed on restart (see Finding 13).

**Risk:** Log files containing plaintext credentials, PII (email addresses, names), session data, and full SQL queries are written to disk. If the server is compromised, log files are a high-value target for credential harvesting. In cloud or shared hosting environments, log file access controls may be insufficiently restrictive.

**Recommendation:**
- Set `log4j.logger.jdbc.sqlonly=OFF` and `log4j.logger.jdbc.resultset=OFF` in production.
- If SQL logging is required for debugging, enable it only in a non-production environment with a separate properties file, and ensure log files are stored with restrictive OS permissions (readable only by the application service account).
- Never log ResultSet contents in production.

---

<a name="finding-8"></a>
### MEDIUM: `log4j.debug=true` enables internal log4j diagnostic output to console

**File:** `src/main/resources/properties/log4j.properties` (line 39)

**Description:**
The configuration file contains:

```properties
log4j.debug=true
```

When set, log4j writes verbose internal diagnostic messages about its own initialisation, appender loading, and configuration parsing to `System.out` (standard output / Tomcat's `catalina.out`). These messages disclose:
- The full filesystem path to the `log4j.properties` file being loaded
- The full path of each log file being opened
- The names and configuration of all appenders and loggers
- JVM classpath and class loading details

This information is directly useful to an attacker who has access to Tomcat's standard output (e.g. via a misconfigured Tomcat Manager, a log injection vulnerability, or access to container logs in a cloud deployment).

**Risk:** Disclosure of internal deployment paths, log file locations, and configuration structure to any party with access to Tomcat console output.

**Recommendation:**
- Set `log4j.debug=false` (or remove the line entirely, as `false` is the default) in the production configuration file.

---

<a name="finding-9"></a>
### MEDIUM: `ValidateIdExistsAbstractActionForm` validation bypassed when `validate="false"` in struts-config

**File:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java` (lines 18–27); `src/main/webapp/WEB-INF/struts-config.xml` (lines 267, 278, 288, 357, 364, 371, 378, 524, 530, 550, 556, 560, 565, 572, 579)

**Description:**
`ValidateIdExistsAbstractActionForm` provides a `validate()` implementation that checks the `id` field is non-empty before allowing the action to proceed:

```java
// ValidateIdExistsAbstractActionForm.java lines 19-27
@Override
public ActionErrors validate(ActionMapping mapping, HttpServletRequest request) {
    ActionErrors errors = new ActionErrors();
    if (StringUtils.isEmpty(this.id)) {
        ActionMessage message = new ActionMessage("error.id");
        errors.add("id", message);
    }
    return errors;
}
```

In Struts 1, the `validate()` method on an `ActionForm` is **only called when the corresponding `<action>` element in struts-config.xml has `validate="true"`**. An audit of `struts-config.xml` found at least 14 action mappings with `validate="false"`, including several that use form beans extending `ValidateIdExistsAbstractActionForm` or its subclasses (e.g. the `/settings` action at line 267, and several report and unit actions).

When `validate="false"` is set, Struts completely skips the `ActionForm.validate()` call, meaning the `id` field is never checked. The action's `execute()` method receives an `ActionForm` where `id` may be `null` or an empty string, and any downstream SQL queries using that `id` will either return an empty result set, throw a `NullPointerException`, or — if the DAO layer does not guard against null — execute a query with an unintended predicate (e.g. `WHERE id = NULL`), which in some databases returns all rows.

This is an architectural vulnerability: the validation logic is placed in the form class, but struts-config.xml can silently neutralise it with a single attribute.

**Risk:** For actions where `id` is used as a database key to scope queries to a specific company or user record, a missing `id` could cause data leakage across tenants (returning all rows) or a server error that reveals stack trace information. The validation bypass is invisible to a developer reading only the Java source.

**Recommendation:**
- Audit every `<action>` that uses a form extending `ValidateIdExistsAbstractActionForm` or its subclasses; set `validate="true"` where the `id` field is mandatory.
- Add a null/empty guard at the start of each action's `execute()` method for the `id` parameter as a defence-in-depth measure, independent of the form validation setting.
- Add an integration test that verifies the action rejects requests with a missing `id` parameter.

---

<a name="finding-10"></a>
### LOW: `generateRadomName()` prefixes UUID with predictable timestamp

**File:** `src/main/java/com/util/Util.java` (lines 258–266); caller at `src/main/java/com/pdf/FleetCheckPDF.java` (line 37)

**Description:**
`generateRadomName()` is used to generate PDF filenames stored in the server's `/temp/` directory:

```java
// Util.java lines 260-265
Calendar currentDate = Calendar.getInstance();
SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMddHHmmss");
String dateNow = formatter.format(currentDate.getTime());
String uuid = UUID.randomUUID().toString();
return dateNow + "-" + uuid;
```

The UUID component (`UUID.randomUUID()`) uses the JVM's `SecureRandom` source and provides 122 bits of cryptographic randomness — sufficient to make the filename unpredictable. However:

1. The method name is `generateRadomName` (a typo for `generateRandomName`), which indicates its purpose is not clearly defined. If it is repurposed for generating security tokens (session IDs, one-time tokens, CSRF nonces), the timestamp prefix leaks the exact second of token creation, reducing the effective search space for a brute-force attack by approximately 32 bits.

2. The generated PDF filename is logged at INFO level before being emailed (`log.info("file genrated = " + attachment)`), exposing the full server path and filename in `info.log`.

**Risk:** If `generateRadomName()` is used as a security token rather than only as a filename, the timestamp prefix reduces entropy. As a filename the UUID suffix is sufficient, but the combination could be misused.

**Recommendation:**
- Rename the method to `generateRandomName()` and add a Javadoc comment clarifying that it is intended for filename generation only and must not be used as a security token.
- For security tokens, use only `UUID.randomUUID().toString()` or `SecureRandom`-derived bytes without a predictable prefix.
- Remove the server-side file path from INFO-level log statements.

---

<a name="finding-11"></a>
### LOW: Stack traces printed to `System.out` via `e.printStackTrace()` in mail-send error paths

**File:** `src/main/java/com/util/Util.java` (lines 63, 124); `src/main/java/com/action/MailerAction.java` (lines 124, 131); `src/main/java/com/action/AdminSendMailAction.java` (line 106)

**Description:**
Multiple catch blocks in the mail-sending code fall through to `e.printStackTrace()` or `System.out.println()`:

```java
// Util.java lines 62-64 (sendMail overload 1 — Transport.send failure)
} catch (Exception e) {
    e.printStackTrace();
    return false;
}

// Util.java lines 123-125 (sendMail overload 2 — Transport.send failure)
} catch (Exception e) {
    e.printStackTrace();
}

// Util.java lines 67-69 (outer catch)
} catch (Throwable t) {
    t.printStackTrace();
}
```

`printStackTrace()` writes to `System.err`, which on Tomcat is typically directed to `catalina.out`. This output includes:
- Full Java stack traces with class names, method names, and line numbers
- Exception messages that may include SMTP server hostname, port, authentication failure details, or TLS certificate errors
- In the outer `catch (Throwable t)` block in both `sendMail` overloads, even `OutOfMemoryError` and similar JVM errors are silently swallowed after printing

The `sendMail()` method at line 130 in the attachment overload returns `true` regardless of whether `Transport.send()` succeeded, because the exception is swallowed in the inner try/catch but the method's outer `return true` is always reached. This means callers have no reliable way to detect mail delivery failure.

**Risk:** Stack traces in server logs disclose internal class structure, library versions, and server configuration to anyone with access to `catalina.out`. The silent `return true` on mail failure means administrators are not alerted to delivery problems.

**Recommendation:**
- Replace all `e.printStackTrace()` calls with `log.error("...", e)` using the application's configured log4j logger.
- Fix the second `sendMail()` overload to return `false` (or throw) when `Transport.send()` fails, rather than silently returning `true`.
- Replace `catch (Throwable t)` with `catch (Exception e)` to allow `Error`-class JVM failures to propagate normally.

---

<a name="finding-12"></a>
### LOW: Log file path controlled by unvalidated `${logDir}` JVM system property

**File:** `src/main/resources/properties/log4j.properties` (lines 22, 70, 77, 83, 90)

**Description:**
All log file paths are constructed from the `${logDir}` system property:

```properties
log4j.appender.rollingFile.File=${logDir}/info.log
log4j.appender.sql.File=${logDir}/sql.log
log4j.appender.sqltiming.File=${logDir}/sqltiming.log
log4j.appender.jdbc.File=${logDir}/jdbc.log
log4j.appender.connection.File=${logDir}/connection.log
```

If `${logDir}` is not set at JVM startup, log4j will use the literal string `${logDir}` as the directory name, creating log files in the current working directory (Tomcat's `bin/` or `root/` directory, depending on startup configuration). More importantly, if an attacker can influence JVM system properties — for example, through a JNDI injection vulnerability (relevant given this is a Struts 1 application with the historical Struts OGNL/ClassLoader issues), or through a misconfigured admin interface — they could redirect log output to an attacker-controlled path or overwrite sensitive files.

**Risk:** Missing `${logDir}` causes logs to be written to an unintended location, potentially the web-accessible document root. An attacker able to set system properties could redirect log output.

**Recommendation:**
- Set `${logDir}` to an absolute, non-web-accessible path in the Tomcat startup configuration (e.g. `JAVA_OPTS="-DlogDir=/var/log/forkliftiqadmin"`).
- Add a startup check that validates `${logDir}` is set and points to a writable, non-web-accessible directory before the application accepts requests.

---

<a name="finding-13"></a>
### LOW: SQL and JDBC log files use `Append=false` — evidence of attacks destroyed on restart

**File:** `src/main/resources/properties/log4j.properties` (lines 71, 78, 85, 92)

**Description:**
The `sql`, `sqltiming`, `jdbc`, and `connection` file appenders are all configured with:

```properties
log4j.appender.sql.Append=false
log4j.appender.sqltiming.Append=false
log4j.appender.jdbc.Append=false
log4j.appender.connection.Append=false
```

`Append=false` causes log4j to **truncate** (overwrite) the log file on every application startup. This means:
- SQL injection attack attempts are erased when the server is restarted.
- Security forensics is impossible if an incident is discovered after a server restart.
- A rolling restart (e.g. during a deployment) destroys recent log history.

By contrast, the main `rollingFile` appender (for `info.log`) does not set `Append=false` and uses `RollingFileAppender`, so general application logs are preserved. The inconsistency suggests the SQL log configuration was copied from a debugging template and not reviewed for production use.

**Risk:** Loss of forensic evidence for SQL injection and database access auditing. An attacker who can trigger a server restart (e.g. through a resource exhaustion attack) can erase their tracks.

**Recommendation:**
- Set `Append=true` on all production log file appenders, or use `RollingFileAppender` with `MaxBackupIndex` to maintain a rolling history.
- If these SQL logs are considered debug-only, disable them entirely in production (see Finding 7).

---

<a name="finding-14"></a>
### INFO: Hardcoded internal email addresses, AWS EC2 endpoint, and debug recipient in RuntimeConf.java

**File:** `src/main/java/com/util/RuntimeConf.java` (lines 16, 58, 60)

**Description:**
`RuntimeConf.java` contains hardcoded values that should be externalised to environment-specific configuration:

```java
public static String RECEIVER_EMAIL = "hui@ciifm.com";              // line 16 — labelled "live"
public static String debugEmailRecipet = "hui@collectiveintelligence.com.au"; // line 58
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"; // line 60
```

Of particular note:
- `RECEIVER_EMAIL` is labelled with the comment `//live`, indicating it was copied from a production configuration and was never replaced with an environment-specific placeholder.
- `debugEmailRecipet` receives a copy of every report email when the `debug` parameter equals `"t"`. A developer left a debug mode with a hardcoded personal email address in the production codebase.
- `APIURL` is a hardcoded HTTP (not HTTPS) URL to an AWS EC2 public IP address. Traffic to this endpoint is unencrypted and the IP address is publicly committed to the source code.

**Risk:** Developer email addresses are exposed in source code (privacy/policy concern). The unencrypted AWS API endpoint exposes PDF report content to network interception. Hardcoded debug mode addresses mean reports could be misdirected if the debug flag is accidentally enabled in production.

**Recommendation:**
- Externalise all environment-specific values (`RECEIVER_EMAIL`, `debugEmailRecipet`, `APIURL`, `emailFrom`) to a properties file loaded at runtime or environment variables.
- Change the API URL to HTTPS.
- Remove the `debug` email-routing logic from production code entirely, or gate it behind an environment variable that defaults to `false` in production.

---

<a name="finding-15"></a>
### INFO: `error.cognito` message key acts as unconstrained passthrough for external error strings

**File:** `src/main/resources/properties/MessageResources.properties` (line 507); `MessageResources_en.properties` (not present in `_en` file — only in the base file)

**Description:**
The base `MessageResources.properties` defines two keys that are simply `{0}` — a single argument placeholder with no surrounding text:

```properties
error.cognito={0}
error.incorrect.reset.cognito = {0}
```

These keys exist in the base (default-language) file but are absent from `MessageResources_en.properties`. This means for English-locale users, Struts will fall back to the base file, and the raw external API message is displayed. The absence of these keys from the `_en` file also means that if someone adds a localised message for these keys in the `_en` file in the future, the passthrough behaviour will be silently broken for the default locale but fixed for English — an inconsistency that could lead to confusion.

This is a design smell rather than an acute vulnerability, but it amplifies Finding 4 above.

**Risk:** Reinforces the information disclosure and potential XSS risk described in Finding 4.

**Recommendation:**
- Replace `{0}` with a fixed user-friendly message for each key (e.g. `error.cognito=An authentication error occurred. Please try again.`).
- Add corresponding entries to `MessageResources_en.properties` to maintain consistency across all locale files.
- Log the raw Cognito message server-side and display only a reference number or generic message to the user.

---

## Summary

| Severity | Count | Findings |
|----------|-------|----------|
| CRITICAL | 1 | Unsalted MD5 password hashing |
| HIGH | 3 | SMTP header/recipient injection; arbitrary file read via attachment path; Cognito error passthrough with XSS risk |
| MEDIUM | 5 | SSRF in getHTML(); weak PRNG in genPass(); JDBC DEBUG logging; log4j.debug=true; validate="false" bypass |
| LOW | 4 | generateRadomName() predictable prefix; e.printStackTrace() information disclosure; unvalidated ${logDir}; Append=false destroys forensic evidence |
| INFO | 2 | Hardcoded email/AWS addresses in RuntimeConf; error.cognito passthrough design |

**CRITICAL: 1 / HIGH: 3 / MEDIUM: 5 / LOW: 4 / INFO: 2**
