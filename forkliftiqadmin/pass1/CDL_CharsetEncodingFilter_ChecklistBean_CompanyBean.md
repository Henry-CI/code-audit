# Pass 1 Audit — CDL / CharsetEncodingFilter / ChecklistBean / CompanyBean

**Files:**
- `src/main/java/com/json/CDL.java`
- `src/main/java/com/util/CharsetEncodingFilter.java`
- `src/main/java/com/bean/ChecklistBean.java`
- `src/main/java/com/bean/CompanyBean.java`

**Date:** 2026-02-26

---

## Summary

These four files span three distinct concerns: a vendored JSON utility, a servlet filter, and two data-transfer beans.

**CDL.java** is a vendored copy of the `org.json` CSV-to-JSON library (copyright JSON.org, version 2010-12-24, package renamed to `com.json`). It contains no application logic and no direct I/O. Risks here are limited to the age of the vendored copy and one character-stripping behaviour in the output path that could produce misleading CSV content.

**CharsetEncodingFilter.java** is a minimalist servlet filter that sets the request character encoding to UTF-8 (or a value from `web.xml`). The filter is mapped to `/*` in `web.xml` and runs before the Struts dispatcher. It applies only to the request, not the response, and performs no security checks. The gap it leaves — no response encoding header — is a minor hardening concern.

**ChecklistBean.java** is a plain Java bean with two fields (`equipId`, `driverBased`). It carries no credentials, no Lombok annotations, and implements no serialization. Risk is low.

**CompanyBean.java** is the highest-risk file in this batch. It is annotated `@Data` (Lombok), which auto-generates `toString()` including every field. The class stores `password` and `pin` in plain `String` fields, implements `Serializable` without marking sensitive fields `transient`, and is stored as a full `List<CompanyBean>` in the HTTP session attribute `sessArrComp` after login. Each `CompanyBean` in that list is populated directly from database rows that include the `password` and `pin` columns. Separate evidence in `CompanyDAO.java` confirms that passwords are stored as MD5 hashes (`md5(?)`) and that `pin` also stores a user-visible access PIN that may be in plaintext. The combination of `@Data`-generated `toString()`, session storage of full objects including credential fields, and `Serializable` without `transient` creates multiple credential-exposure paths.

**Overall risk level: HIGH** (driven primarily by CompanyBean credential handling).

---

## Findings

### HIGH: Lombok @Data Generates toString() That Includes password and pin Fields

**File:** `CompanyBean.java` (lines 11, 24–25)

**Description:**
The class is annotated with `@Data`, which causes Lombok to auto-generate `toString()`, `equals()`, and `hashCode()` methods that include every non-static field. The fields `password` (line 24) and `pin` (line 25) are plain `String` members. Any logging statement, debug output, or framework-level exception handler that calls `toString()` on a `CompanyBean` instance — including a `List<CompanyBean>` dump — will emit the password hash and PIN in cleartext. Struts 1.x and servlet containers commonly log request attributes and session objects during error conditions (e.g., in `<error-page>` handlers or via MDC). The project uses SLF4J/MDC, and `CompanyDAO.java` already contains `log.info(...)` statements throughout the DAO layer, making accidental future logging of a bean highly likely.

**Risk:**
Any log aggregation pipeline (application logs, access logs, container stdout) that captures a `CompanyBean.toString()` will capture password hashes and PINs. If those logs are shipped to a third-party SIEM or stored insecurely, credential data is exposed. The PIN field in particular appears to be stored in plaintext in the database in some flows (see `QUERY_SUBCOMPANYLST_BY_ID` and the Cognito flow in `CompanyDAO.java` line 615).

**Recommendation:**
Override `toString()` explicitly and exclude `password`, `pin`, `answer` (security question answer), and any other credential or secret field. Either use `@ToString.Exclude` on those fields (Lombok annotation), or replace `@Data` with `@Getter @Setter @EqualsAndHashCode` and write a manual `toString()`. At minimum, annotate:
```java
@ToString.Exclude
private String password;

@ToString.Exclude
private String pin;

@ToString.Exclude
private String answer;
```

---

### HIGH: CompanyBean Implements Serializable With Non-transient Credential Fields

**File:** `CompanyBean.java` (lines 7, 13, 24–25)

**Description:**
`CompanyBean` implements `java.io.Serializable` (line 13) and declares a `serialVersionUID` (line 15). The `password` and `pin` fields are not marked `transient`. `CompanyBean` instances are stored in the HTTP session attribute `sessArrComp` as an `ArrayList<CompanyBean>` (confirmed in `LoginAction.java` line 61 and `AdminRegisterAction.java` lines 206 and 260). Java EE servlet containers serialize HTTP sessions to disk for persistence or clustering (session passivation). If session passivation is enabled or the container crashes, the serialized session file on disk will contain the password hashes and PINs of every company visible to the logged-in user.

Additionally, if session data is transmitted to a remote node (e.g., in a clustered deployment), the credential values travel over whatever transport the cluster uses. The `web.xml` does not configure any session persistence provider, so the risk depends on deployment configuration, but the object itself provides no protection.

**Risk:**
Credential exposure in session storage files, cluster replication traffic, or any deserialization endpoint.

**Recommendation:**
Mark credential and sensitive fields `transient`:
```java
private transient String password;
private transient String pin;
private transient String answer;
```
Additionally, review whether the full `CompanyBean` (with credentials) needs to be in the session at all, or whether a projection bean containing only the fields actually used at runtime (timezone, dateFormat, template, email, etc.) should be stored instead.

---

### HIGH: password and pin Columns Fetched Into CompanyBean From Database Unnecessarily

**File:** `CompanyBean.java` (lines 24–25) — evidenced by `CompanyDAO.java` lines 75–79, 81–85, 187–188, 498–499, 533–534

**Description:**
Multiple SQL queries in `CompanyDAO` (`QUERY_SUBCOMPANYLST_BY_ID`, `QUERY_COMPANY_BY_ID`) SELECT the `password` and `pin` columns and map them directly into `CompanyBean.password` and `CompanyBean.pin`. The resulting beans are placed into session and passed to JSP views. While these queries use parameterised statements (no SQL injection risk), the architectural choice to hydrate credential fields into the view/session bean is the root cause of the `@Data`/`Serializable` exposure findings above.

At line 615 of `CompanyDAO.java`, the `pin` field's value is used directly as a Cognito password without any transformation check beyond a blank-string guard — meaning whatever is stored in `pin` is sent to AWS Cognito as an authentication credential, further elevating the sensitivity of this field.

**Risk:**
Credentials flow through multiple layers (DAO → bean → session → JSP template rendering context → `sessArrComp` attribute) where any intermediate logging, serialization, or accidental inclusion in a response body can expose them.

**Recommendation:**
Introduce a separate DAO projection that omits `password` and `pin` for all non-authentication use cases. Use the full credential-bearing query only in the narrow authentication code paths, and discard the credential fields immediately after use rather than retaining them in a session-scoped object.

---

### MEDIUM: MD5 Used for Password Hashing

**File:** `CompanyBean.java` (line 24) — evidenced by `CompanyDAO.java` lines 61, 95, 443 and `LoginDAO.java` lines 51, 92

**Description:**
The application stores user and company passwords using the SQL expression `md5(?)` (plain MD5, no salt). MD5 is a cryptographic hash function deprecated for password storage since at least 2004. It is vulnerable to rainbow-table attacks and can be brute-forced on commodity hardware at billions of hashes per second. There is no evidence of a pepper or application-side salt. The `CompanyBean.password` field therefore holds a raw unsalted MD5 digest.

**Risk:**
If the database is compromised, all passwords are recoverable in minutes to hours using pre-computed tables or GPU cracking. This is a systemic credential-security weakness; the bean design compounds it by propagating these hashes into session and potentially into logs.

**Recommendation:**
Migrate password hashing to bcrypt, scrypt, or Argon2 with appropriate cost factors. The `UPDATE_USR_PIN` query (`update users set password = md5(?) where id = ?`) and all login verification queries must be updated. The migration should include a re-hashing strategy for existing users on next login.

---

### MEDIUM: CompanyBean Contains Security-Question Answer as Plain String

**File:** `CompanyBean.java` (lines 30–31)

**Description:**
The fields `question` and `answer` hold the user's security question and answer. Security question answers are effectively secondary passwords. They are stored in `CompanyBean` as plain `String` values and are subject to the same `@Data`-generated `toString()` exposure and `Serializable` leakage as `password` and `pin`.

**Risk:**
Security question answers exposed via logging or session serialization can be used for account recovery attacks. Even if the application later replaces security questions with a better MFA mechanism, these values remain in the database and in serialized sessions.

**Recommendation:**
Apply `@ToString.Exclude` and `transient` to the `answer` field. If security questions are still in active use, hash the answers at rest rather than storing plaintext.

---

### MEDIUM: CharsetEncodingFilter Does Not Set Response Character Encoding or Content-Type

**File:** `CharsetEncodingFilter.java` (lines 19–24)

**Description:**
The filter correctly sets the request character encoding (`srequest.setCharacterEncoding(defaultEncode)`), which prevents mis-decoding of multi-byte input. However, it does not set the response character encoding (`response.setCharacterEncoding(...)`) or a default `Content-Type` header. If downstream JSPs or actions omit an explicit `Content-Type: text/html; charset=UTF-8` declaration, browsers may apply charset sniffing, which is a known XSS vector (older IE and some mobile browsers). The Struts 1.x JSP pages in this application are the primary surface for this risk.

**Risk:**
Without an authoritative `charset` in the response `Content-Type`, a browser that sniffs the content encoding may interpret UTF-7 or other alternate-encoding payloads as XSS. The risk is elevated in Struts 1.x applications that do not consistently set `Content-Type` in every JSP.

**Recommendation:**
Extend `doFilter` to also set the response encoding:
```java
response.setCharacterEncoding(defaultEncode);
```
Additionally, verify that all JSPs include `<%@ page contentType="text/html; charset=UTF-8" %>` and that the `X-Content-Type-Options: nosniff` response header is set (ideally in this same filter).

---

### LOW: CharsetEncodingFilter Charset Is Configurable From web.xml Without Validation

**File:** `CharsetEncodingFilter.java` (lines 12–14)

**Description:**
The `init` method reads the `Charset` init-parameter from `web.xml` and assigns it to `defaultEncode` without validating that it is a recognised charset name. If an invalid value is configured, `setCharacterEncoding` will throw an `UnsupportedEncodingException` at runtime for every request, causing a full denial of service. In the current `web.xml` no `Charset` init-parameter is defined, so the default of `"UTF-8"` applies, but the risk remains latent for future deployments.

**Risk:**
Misconfiguration in `web.xml` can cause a complete application outage without any code change. Low likelihood in a controlled deployment, but the lack of validation is a defensive-programming gap.

**Recommendation:**
Validate the configured charset in `init()`:
```java
if (config.getInitParameter("Charset") != null) {
    String cs = config.getInitParameter("Charset");
    if (Charset.isSupported(cs)) {
        defaultEncode = cs;
    } else {
        throw new ServletException("Unsupported charset: " + cs);
    }
}
```
Failing fast in `init` is preferable to failing on every request.

---

### LOW: CDL.java Is a Vendored Copy of org.json (Version 2010-12-24) — No Upstream Patches Applied

**File:** `CDL.java` (lines 3–25, 44)

**Description:**
This file is a vendored (inlined) copy of the `org.json` `CDL` class, version-dated 2010-12-24, repackaged under `com.json`. Vendoring a library inside application source means the application does not receive upstream bug fixes or security patches through normal dependency management (e.g., Maven). The `org.json` library has had CVEs reported against it (notably CVE-2022-45688, a stack-overflow/DoS via deeply nested JSON, and earlier parsing issues). Whether those CVEs affect the vendored `CDL.java` specifically depends on which other `com.json.*` classes are also vendored; `CDL` itself delegates to `JSONTokener` and `JSONArray`, which are likely also vendored copies.

**Risk:**
Low for `CDL.java` in isolation — the CSV-parsing logic here does not perform network I/O and is not directly exposed to untrusted input in a web request path. However, the vendoring pattern across the entire `com.json` package may leave the application exposed to unpatched `org.json` vulnerabilities in other classes.

**Recommendation:**
Replace the entire `com.json` vendored package with a Maven/Gradle dependency on a current, maintained version of `org.json` (or switch to Jackson or Gson, which have better CVE track records). This allows automated dependency scanning tools (OWASP Dependency-Check, Snyk, etc.) to flag future vulnerabilities.

---

### LOW: CDL.rowToString() Silently Strips Characters Below ASCII 32 and Double-Quotes From Cell Values

**File:** `CDL.java` (lines 158–163)

**Description:**
In `rowToString`, when a cell value requires quoting (contains a comma, newline, carriage return, null byte, or starts with a double-quote), the method iterates the string and silently drops any character below ASCII 32 (`c >= ' '` check) and any double-quote character (`c != '"'` check) rather than escaping them. This means the serialized CSV output is not a lossless representation of the original data: control characters and embedded double-quotes are silently discarded.

If CSV output produced by `CDL.toString()` is later used as input to `CDL.toJSONArray()`, the round-trip is not faithful. If the CSV is consumed by a downstream system that expects complete data, silent data loss could produce incorrect results or, in an adversarial input scenario, allow a value that would otherwise trigger a parse error to be quietly cleaned into a valid-looking but incorrect value.

**Risk:**
Data integrity issue rather than a direct security vulnerability. Low severity in isolation. Could become a medium-severity concern if CSV output is used in a security-relevant context (e.g., audit logs, compliance exports) where silent data modification is unacceptable.

**Recommendation:**
Use proper RFC 4180 CSV escaping: double-quotes inside a quoted field should be escaped as `""` rather than dropped. Replace the inner loop with standard escaping logic.

---

### INFO: ChecklistBean Has No Security-Relevant Content

**File:** `ChecklistBean.java` (lines 1–22)

**Description:**
`ChecklistBean` is a minimal two-field POJO (`equipId: int`, `driverBased: boolean`) with standard getter/setter pairs. It carries no credentials, no PII, no Lombok annotations, and does not implement `Serializable`. No security concerns were identified.

**Risk:** None.

**Recommendation:** No action required. Note for completeness that `equipId` is an `int` — callers that set this value from a user-supplied request parameter should validate the range server-side (cannot be negative, should correspond to an equipment record accessible to the current session company), but that validation belongs in the Action layer, not in the bean itself.

---

### INFO: CharsetEncodingFilter Stores FilterConfig Reference Unnecessarily

**File:** `CharsetEncodingFilter.java` (lines 7, 11, 17)

**Description:**
The `config` field stores the `FilterConfig` reference across the filter's lifecycle, but `config` is never used after `init()` completes. The only value consumed from it is `getInitParameter("Charset")`, which is read once and stored in `defaultEncode`. Holding a reference to `FilterConfig` for the entire filter lifetime is a minor memory and code-cleanliness issue; it also means the filter holds a reference to a container-managed object longer than necessary.

**Risk:** None — this is an informational note.

**Recommendation:** Remove the `private FilterConfig config` field and the assignment in `init()`. The `destroy()` method already sets it to `null`, which implicitly acknowledges it is not needed after init, but it is cleaner to not retain it at all.

---

## Finding Count

- CRITICAL: 0
- HIGH: 3
- MEDIUM: 2
- LOW: 3
- INFO: 2
