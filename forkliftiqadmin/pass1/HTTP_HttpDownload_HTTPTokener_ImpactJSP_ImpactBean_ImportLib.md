# Security Audit Report
## Batch: HTTP.java, HttpDownloadUtility.java, HTTPTokener.java, impact.jsp, ImpactBean.java, ImpactLevel.java, importLib.jsp
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Application:** forkliftiqadmin — Apache Struts 1.3.10 / Tomcat
**Branch:** master

---

## Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/json/HTTP.java` |
| 2 | `src/main/java/com/util/HttpDownloadUtility.java` |
| 3 | `src/main/java/com/json/HTTPTokener.java` |
| 4 | `src/main/webapp/html-jsp/vehicle/impact.jsp` |
| 5 | `src/main/java/com/bean/ImpactBean.java` |
| 6 | `src/main/java/com/bean/ImpactLevel.java` |
| 7 | `src/main/webapp/includes/importLib.jsp` |

---

## Findings

---

### CRITICAL: Hardcoded API Authentication Token in Source Code

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (line 105)

**Description:**
A static, hardcoded bearer/token credential is set directly as a request property on every outbound POST connection to the Pandora reporting API:

```java
con.setRequestProperty("X-AUTH-TOKEN", "noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE");
```

This token is committed to version control in plain text. Anyone with read access to the repository — including all developers, CI/CD pipelines, contractors, and anyone who has ever cloned the repository — now permanently possesses this credential. The token cannot be revoked without a code change and redeployment. Git history retains the value even after a future removal.

**Risk:**
An attacker who obtains the source code (insider, leaked repo, compromised developer machine, or public GitHub exposure) can use this token to call the Pandora API directly, bypassing all application-layer access controls. Depending on the API's capabilities this could expose all tenant reports, allow data exfiltration, or allow data manipulation across every company in the system.

**Recommendation:**
Remove the token from source immediately. Rotate the credential at the API provider. Store secrets in environment variables, a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault), or an externalized properties file that is excluded from version control via `.gitignore`. Inject the value at runtime via JNDI, system properties, or a configuration service.

---

### CRITICAL: HTTP Used for API Communication — Token Transmitted in Plaintext

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 91–99)

**Description:**
The `sendPost` method constructs the target URL from `RuntimeConf.APIURL`, which is defined as a plain HTTP endpoint:

```java
// RuntimeConf.java line 60
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/";
```

The connection object is typed as `HttpURLConnection` (not `HttpsURLConnection`), and the commented-out HTTPS alternative is never used:

```java
// Secure connection
// HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
```

The hardcoded `X-AUTH-TOKEN` header and any POST body content (which may contain tenant `company_id`, date ranges, and credentials) are transmitted in cleartext over this HTTP connection. The application server communicates with an EC2 instance using a raw IP-based DNS hostname over the public internet, with no TLS.

**Risk:**
Network-level attackers (on-path, rogue cloud routing, compromised ISP transit) can intercept the `X-AUTH-TOKEN` credential and all request/response bodies. The EC2 instance is addressed by a public hostname, making this traffic internet-routable without encryption. Additionally, data in transit may include PII (driver names, company data, operational hours) violating data-protection obligations.

**Recommendation:**
Change `RuntimeConf.APIURL` to an `https://` endpoint. Activate the commented-out `HttpsURLConnection` code path. Validate the server certificate (do not disable hostname verification). Consider placing the API call within a VPC or private network if both services run in AWS.

---

### CRITICAL: SSRF via Unvalidated User-Supplied URL in `downloadFile`

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 35–38)

**Description:**
The `downloadFile` method accepts a `fileURL` parameter and passes it directly to `new URL(...)` and `url.openConnection()` without any validation, allow-listing, or scheme checking:

```java
public static void downloadFile(String fileName, String fileURL, String saveDir)
        throws IOException {
    URL url = new URL(fileURL);
    HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
```

If any calling code path exposes `fileURL` to user-controlled input, the server can be made to issue HTTP requests to arbitrary internal or external targets. The cast to `HttpURLConnection` would reject `file://` or `ftp://` schemes with a ClassCastException, but `http://` and `https://` to internal targets remain fully exploitable. Currently `downloadFile` appears to have no callers in the audited codebase other than its declaration, so exploitability depends on whether it is called from an action that accepts a request parameter. This risk must be treated as critical because the method signature is designed for external data and provides zero guard rails.

**Risk:**
SSRF enabling the application server to make GET requests to internal AWS metadata service (`http://169.254.169.254/`), internal databases, adjacent microservices, or other intranet hosts not reachable from the public internet. Could lead to credential theft (AWS IAM role credentials from IMDS), internal service enumeration, or data exfiltration.

**Recommendation:**
Implement a strict allow-list of permitted URL prefixes (scheme + host). Reject any URL that does not match. If the download URL is fully controlled by the server (not user-supplied), remove the parameter from the public API surface and hardcode the base URL. Use a dedicated HTTP client library that supports SSRF mitigation features.

---

### HIGH: Path Traversal via Server-Controlled `Content-Disposition` Filename

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 44–63)

**Description:**
When the HTTP response includes a `Content-Disposition` header, the code extracts a filename from it and uses that filename directly when constructing the local file save path:

```java
String disposition = httpConn.getHeaderField("Content-Disposition");
if (disposition != null) {
    int index = disposition.indexOf("filename=");
    if (index > 0) {
        fileName = disposition.substring(index + 10, disposition.length() - 1);
    }
}
// ...
saveFilePath = saveDir + File.separator + fileName;
FileOutputStream outputStream = new FileOutputStream(saveFilePath);
```

If the remote server (or an attacker who has performed MitM due to the HTTP-only connection noted above) returns a `Content-Disposition` such as `attachment; filename=../../conf/server.xml`, the resulting `saveFilePath` will escape the intended `saveDir`. Because there is no call to `getCanonicalPath()` and no check that the resolved path remains within `saveDir`, this constitutes a path traversal write vulnerability.

The same risk applies when the URL-derived filename (lines 55–57) contains `..` sequences, though that is slightly harder to exploit because the URL is currently server-controlled.

**Risk:**
An attacker controlling the remote server (or performing MitM against the unencrypted HTTP connection) can cause the application to overwrite arbitrary files writable by the Tomcat process: web application files, configuration files, JSP pages (enabling RCE via JSP shell upload), or OS-level files.

**Recommendation:**
After constructing `saveFilePath`, verify it using `File.getCanonicalPath()` and assert that it starts with the canonical path of `saveDir`. Sanitize the extracted filename by stripping all directory separators and `..` components before use. Consider using only a server-generated UUID as the filename and ignoring the `Content-Disposition` header entirely.

---

### HIGH: Static Mutable Field `saveFilePath` — Race Condition / Cross-Request Data Leakage

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 26–27, 63, 160, 186–192)

**Description:**
`saveFilePath` is declared as a `private static String` field and is written by both `downloadFile` (line 63) and `sendPost` (line 160). Its value is then read back by callers via `getSaveFilePath()`:

```java
private static String saveFilePath = "";

// In downloadFile:
saveFilePath = saveDir + File.separator + fileName;

// In sendPost:
saveFilePath = saveDir + fileName + RuntimeConf.file_type;
```

In a multi-threaded servlet container (Tomcat handles every HTTP request on a separate thread), two concurrent report-generation requests will race to write and then read this single static field. Thread A may write its path, then Thread B overwrites it before Thread A reads it back, causing Thread A to retrieve Thread B's file path. In a multi-tenant system this means one company's generated report could be sent to a different company's user.

**Risk:**
Cross-tenant data leakage: a user belonging to Company A receives a PDF report containing Company B's operational data. This is a confidentiality breach that violates the multi-tenant isolation model of the application.

**Recommendation:**
Remove the `static` keyword from `saveFilePath` or, since the methods are currently `static`, refactor them to return the computed file path directly from the method instead of storing it in a shared field. Alternatively, use a `ThreadLocal<String>` if the static design must be kept.

---

### HIGH: Unescaped Request Parameter `id` Reflected into HTML Attributes (XSS)

**File:** `src/main/webapp/html-jsp/vehicle/impact.jsp` (lines 7–8, 41–45, 85)

**Description:**
The `equipId` request parameter is read and concatenated directly into HTML without any encoding:

```java
// Line 7-8
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String urlGeneral = id.isEmpty() ? "adminunit.do?action=add" : "adminunit.do?action=edit&equipId=" + id;
```

`id` and `urlGeneral` are then embedded in HTML:

```jsp
<!-- Line 40 -->
<ul class="modal-content-tab admin_unit clearfix <%= isDealer ? "five" : "four" %>">
<!-- Line 41 -->
<li><a href="<%=urlGeneral %>" class="general_u_tab">General</a></li>
<!-- Line 42 -->
<li><a href="adminunit.do?action=service&equipId=<%=id %>" id="service_tab">Service</a></li>
<!-- Line 43 -->
<li><a href="adminunitaccess.do?id=<%=id %>" id="access_tab">Access</a></li>
<!-- Line 44 -->
<li class="active"><a href="adminunit.do?action=impact&equipId=<%=id %>" id="impact_tab">Impact</a></li>
<!-- Line 85 -->
<input type="hidden" name=equipId value="<%=id %>">
```

A crafted `equipId` value such as `"><script>alert(1)</script>` or `" onmouseover="alert(1)` will break out of the attribute context and inject arbitrary JavaScript. Although the application requires authentication (`sessCompId` check), stored/reflected XSS from authenticated users can still be used to steal session cookies, perform CSRF escalation within an active session, or execute actions on behalf of other users including administrators.

**Risk:**
Reflected XSS. An attacker who tricks an authenticated user into clicking a crafted link can hijack their session, exfiltrate session cookies, or perform actions in the application on behalf of the victim. In a multi-tenant admin application this could allow cross-tenant privilege escalation.

**Recommendation:**
Encode all user-supplied values before placing them in HTML. Use JSTL `<c:out value="${param.equipId}"/>` or the OWASP Java Encoder library: `Encode.forHtmlAttribute(id)` for attribute contexts and `Encode.forUriComponent(id)` when building URL query strings. Never use raw `<%= %>` scriptlets with unvalidated request parameters.

---

### HIGH: NullPointerException / Authentication Logic Flaw — Unguarded `session.getAttribute` Call

**File:** `src/main/webapp/html-jsp/vehicle/impact.jsp` (line 9)

**Description:**
The JSP calls `.equals("true")` directly on the return value of `session.getAttribute("isDealer")` without a null check:

```java
boolean isDealer = session.getAttribute("isDealer").equals("true");
```

If `isDealer` has not been placed in the session (e.g., for a freshly created session, a session after partial logout, or a session that bypassed the normal authentication flow), this line will throw a `NullPointerException`. Depending on how Tomcat/Struts handles the resulting `500` error page, this could:

1. Reveal a full stack trace including internal class names, server paths, and framework versions.
2. Be exploited to probe the authentication state — a `500` response versus a redirect indicates whether the session attribute was set.

More critically, if a bypass or timing attack allows the page to render without `isDealer` in the session, the NPE provides confirmation of the anomaly.

**Risk:**
Information disclosure via stack trace exposure and potential DoS for legitimate users arriving at this page with an incomplete session state.

**Recommendation:**
Use a null-safe pattern: `"true".equals(session.getAttribute("isDealer"))`. Ensure the application's global error handler suppresses stack traces in production responses. Validate the attribute presence at the action layer before forwarding to the JSP.

---

### MEDIUM: Plaintext Internal Application URL Exposed in Source Configuration

**File:** `src/main/java/com/util/RuntimeConf.java` (line 8)

**Description:**
A publicly routable URL to the application's own deployment endpoint is hardcoded in source:

```java
public static String url = "http://prestart.collectiveintelligence.com.au/";
```

This is served over HTTP (no TLS), and the hostname reveals the live production deployment domain. Combined with other fields in `RuntimeConf`, this file provides a map of the production infrastructure: the S3 bucket name (`forkliftiq360`), the EC2 hostname and IP (`ec2-52-5-205-104.compute-1.amazonaws.com`), email addresses for staff (`hui@ciifm.com`, `hui@collectiveintelligence.com.au`), the JNDI database name (`jdbc/PreStartDB`), internal folder paths (`/doc/`, `/temp/`), and the Linde-branded database name (`fleeiq`).

**Risk:**
Infrastructure reconnaissance. An attacker who reads the source code gains a complete map of production hostnames, S3 bucket names, email addresses, and internal path conventions. The S3 bucket name is particularly sensitive: it may be enumerable if its ACL is misconfigured. The email addresses constitute targeted social-engineering targets.

**Recommendation:**
Move all environment-specific configuration out of source code into externalized configuration (environment variables, JNDI, a properties file excluded from version control). Apply the Twelve-Factor App principle: code ships with no environment-specific data. At a minimum, audit the S3 bucket ACL, rotate exposed email aliases, and consider rotating the EC2 instance.

---

### MEDIUM: Unescaped `bean:write` Tag Output in CSS `content` Property (Potential XSS)

**File:** `src/main/webapp/html-jsp/vehicle/impact.jsp` (lines 27–35)

**Description:**
The Struts `<bean:write>` tag is used to inject the `percentage` property of `impactBean` into a CSS `content` pseudo-element defined inline in a `<style>` block:

```jsp
<style>
    .progress:after {
        content: "<bean:write name="impactBean" property="percentage" />%";
        ...
    }
</style>
```

By default, `<bean:write>` does not HTML-encode its output (unlike `<c:out>`). If `percentage` is derived from any attacker-influenced source (e.g., a database field set by a malicious operator-level user), it could contain a closing `</style>` sequence followed by a `<script>` block or event handler. Even if `percentage` is a `double` field in the Java bean (which would limit injection to numeric values), the reliance on the data type alone — rather than explicit output encoding — is a fragile control that could break if the field type changes or if the value is mapped through a different code path.

Furthermore, the same tag is used at line 96 in an HTML `style` attribute:
```jsp
style="width: <bean:write name="impactBean" property="percentage"/>%"
```

Injection here into a CSS property value within an attribute could also serve as an XSS vector if the value is not strictly numeric.

**Risk:**
If `percentage` is ever populated from user-controlled input without server-side type enforcement, this constitutes a stored XSS vector injected via a CSS context, which can be used to steal sessions or perform phishing.

**Recommendation:**
Use `<bean:write name="impactBean" property="percentage" filter="true"/>` (which HTML-encodes output) or replace with JSTL `<c:out>`. For numeric fields, add server-side validation that rejects non-numeric values before they are stored. Do not rely solely on a Java field type as a sanitization control.

---

### MEDIUM: `downloadFile` Accepts Arbitrary URL Schemes — SSRF via `file://` Bypass Risk

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 37–38)

**Description:**
While the method casts to `HttpURLConnection`, passing a `file://` URL would cause a `ClassCastException` rather than a clean rejection. However, `jar:http://...!/` and `jar:https://...!/` URLs can open HTTP connections to external resources and may not cast cleanly to `HttpURLConnection`, depending on JVM version. More subtly, if the JVM follows HTTP redirects internally (which `HttpURLConnection` does not by default, but may be enabled in some configurations), a target server could redirect the client to `http://169.254.169.254/`. No redirect policy is set on the connection:

```java
HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
// No: httpConn.setInstanceFollowRedirects(false);
```

**Risk:**
Redirect-based SSRF: if the remote server returns a `3xx` redirect to an internal resource, the JVM will follow it (default `followRedirects` is `true` at the class level for `HttpURLConnection`). This could expose AWS IMDS or other internal services.

**Recommendation:**
Explicitly call `httpConn.setInstanceFollowRedirects(false)` before issuing the request. Validate that the resolved target URL remains within the allow-listed hosts. After following or rejecting redirects, re-validate the final URL.

---

### MEDIUM: Commented-Out Debug Code Contains Hardcoded Credentials

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 93–94)

**Description:**
A commented-out test block contains what appears to be a plaintext admin credential:

```java
// url = "http://httpbin.org/post";
// input = "{\"admin_password\":\"adminadmin\",\"username\":\"admin\",\"filters\":[...]}";
```

While this is commented out and therefore not executed, it reveals: (1) that `admin`/`adminadmin` was used as test credentials, which may still be active on a development or staging instance; (2) the JSON structure of the API authentication payload, which assists an attacker in crafting valid API requests; (3) a historical record that a test external service (`httpbin.org`) was used, which means outbound connectivity to arbitrary internet hosts was tested and may still be possible.

**Risk:**
If `admin`/`adminadmin` credentials are still active on any environment (development, staging, or production API), they enable full API access. The payload structure disclosure reduces the effort required to attack the API directly.

**Recommendation:**
Remove all commented-out debug code before committing to version control. Never commit credentials in any form — even in comments. Rotate the `admin`/`adminadmin` API credentials immediately and audit whether they are still active. Use a pre-commit hook or secret-scanning tool (e.g., `git-secrets`, `trufflehog`) to prevent future occurrences.

---

### MEDIUM: No SSL/TLS Certificate Validation Configuration — Vulnerable to MitM

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 97–99)

**Description:**
The code comments out the HTTPS connection type and uses plain `HttpURLConnection`. Even if HTTPS were used, no `SSLContext` or `HostnameVerifier` is configured, which means the default JVM trust store and hostname verification would apply. In environments where the JVM trust store has been modified (a common misconfiguration in enterprise deployments), this could silently trust malicious certificates. The real issue is that the code has an explicit comment noting this as a "Secure connection" and then opts not to use it:

```java
//  Secure connection
//  HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
HttpURLConnection con = (HttpURLConnection)obj.openConnection();
```

The presence of the comment suggests the developer was aware of the security requirement and made a deliberate choice to skip it, likely for expediency during development, but this was never reversed.

**Risk:**
All data transmitted to the EC2 API endpoint is susceptible to interception and tampering by any network-level attacker with access to the path between the Tomcat server and the EC2 instance.

**Recommendation:**
Enable TLS. If self-signed certificates are used internally, pin the certificate or add it to a dedicated trust store — never disable certificate validation globally.

---

### LOW: `ImpactBean` Lombok `@Data` Exposes All Fields in `toString()` — Potential Log Leakage

**File:** `src/main/java/com/bean/ImpactBean.java` (line 10)

**Description:**
The `@Data` annotation from Lombok auto-generates a `toString()` method that includes all fields:

```java
@Data
@NoArgsConstructor
public class ImpactBean implements Serializable {
    private int equipId;
    private double accHours;
    private double sessHours;
    private double impact_threshold;
    private boolean alert_enabled;
    private double percentage;
    private String reset_calibration_date;
    private String calibration_date;
```

The auto-generated `toString()` will produce output such as:
```
ImpactBean(equipId=1234, accHours=150.5, sessHours=12.3, impact_threshold=2.5, alert_enabled=true, percentage=100.0, reset_calibration_date=2024-01-15, calibration_date=2024-01-10)
```

If an `ImpactBean` instance is logged (e.g., passed to `log.debug(impact)` or included in an exception message), all calibration parameters including `impact_threshold` (the g-force calibration value, which is operationally sensitive) and `alert_enabled` status are written to log files. In this case there are no passwords or cryptographic secrets in the bean fields, so the severity is lower than a bean containing credentials, but operational sensor data in logs can still be a compliance concern depending on the applicable standards.

**Risk:**
Operational data leakage into log files. Calibration thresholds and alert status for individual forklifts could be read by anyone with log file access, including operators who are not authorised to view calibration data.

**Recommendation:**
Override `toString()` in `ImpactBean` to exclude or redact sensitive fields, or add `@ToString.Exclude` on specific fields. Consider removing `@Data` and generating only the necessary methods to maintain explicit control over what is included in `toString()`.

---

### LOW: `ImpactLevel` Enum Lacks Access Control Annotation — Potential Information Disclosure in API Responses

**File:** `src/main/java/com/bean/ImpactLevel.java` (lines 1–7)

**Description:**
`ImpactLevel` is a plain public enum with no serialization exclusion annotations:

```java
public enum ImpactLevel {
    BLUE,
    AMBER,
    RED
}
```

This is low risk on its own, but when used in serialized API responses (e.g., if `ImpactBean` is serialized to JSON and the impact level is embedded), the enum values are exposed to the client. More importantly, `impact.jsp` iterates over `ImpactLevel.values()` and calls `ImpactUtil.calculateGForceRequiredForImpact()` for each value (line 71), rendering the g-force thresholds for all levels directly in the page HTML. This means any authenticated user who can access the impact tab sees the exact calibration thresholds. Depending on business context, calibration values may be commercially sensitive or safety-critical information that should require elevated privileges to view.

**Risk:**
Low-severity information disclosure of operational calibration thresholds to any authenticated user regardless of role.

**Recommendation:**
Review whether all authenticated users should be able to see calibration thresholds or only privileged roles (e.g., site admins). If restricted, add a role check before rendering the calibration table in `impact.jsp`.

---

### LOW: No Timeout Set on HTTP Connections — Denial of Service Risk

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 37–39, 96–99)

**Description:**
Both `downloadFile` and `sendPost` open HTTP connections without setting connect or read timeouts:

```java
URL url = new URL(fileURL);
HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
int responseCode = httpConn.getResponseCode(); // can block indefinitely
```

If the remote server is slow, unreachable, or deliberately stalls, the Tomcat thread handling the request will block indefinitely. In a Struts 1.x application running on a fixed-size thread pool, a small number of such blocked requests can exhaust all available threads and render the entire application unresponsive.

**Risk:**
Denial of service: an attacker who can cause the server to make HTTP requests to a slow target (via the SSRF vector in `downloadFile`, or by disrupting the EC2 endpoint for `sendPost`) can exhaust the Tomcat thread pool.

**Recommendation:**
Set explicit timeouts on all HTTP connections:
```java
httpConn.setConnectTimeout(10_000); // 10 seconds
httpConn.setReadTimeout(30_000);    // 30 seconds
```

---

### LOW: `HTTP.java` Uses Raw `Iterator` (Unchecked Generics) — Minor Code Quality Risk

**File:** `src/main/java/com/json/HTTP.java` (line 128)

**Description:**
The `toString(JSONObject jo)` method uses a raw `Iterator` without a generic type parameter:

```java
Iterator keys = jo.keys();
// ...
string = keys.next().toString();
```

While this does not constitute a direct security vulnerability, reliance on raw types suppresses compiler warnings and can mask `ClassCastException` scenarios at runtime. If a `JSONObject` were constructed with non-String keys through a deserialization path, the cast to `String` via `.toString()` could produce unexpected output that gets written into the HTTP header string produced by this method.

**Risk:**
Low. If `HTTP.toString()` output is used to construct HTTP requests sent to internal systems, malformed header values could cause header injection. Actual exploitability depends on call sites.

**Recommendation:**
Replace raw `Iterator` with `Iterator<String>`. This is a JSON.org library copy-paste; consider replacing the entire vendored copy with the current official `org.json` library dependency.

---

### INFO: `importLib.jsp` Contains No Client-Side Asset Imports — Clean

**File:** `src/main/webapp/includes/importLib.jsp` (lines 1–18)

**Description:**
The file contains only server-side JSP imports and Struts taglib declarations. It does not load any JavaScript, CSS, or other client-side resources over HTTP or CDN:

```jsp
<%@ page import="org.apache.struts.action.Action" %>
<%@ page import="com.action.SwitchLanguageAction" %>
<%@ taglib uri="/tags/struts-html" prefix="html" %>
<%@ taglib uri="/tags/struts-bean" prefix="bean" %>
<%@ taglib uri="/tags/struts-logic" prefix="logic" %>
```

No CDN URLs, no `<script src>` or `<link href>` tags. There are no findings in this file from a CDN-over-HTTP or XSS-via-import perspective. The Struts taglib declarations are appropriate for this framework version.

**Risk:** None identified.

**Recommendation:** No action required for this file. Continue auditing all JSPs that `<%@ include file="../../includes/importLib.jsp" %>` this file to ensure the consuming JSPs do not introduce client-side resource loading over HTTP.

---

### INFO: `HTTPTokener.java` Is a Vendored Copy of `org.json` Library Code — No Custom Logic

**File:** `src/main/java/com/json/HTTPTokener.java` (lines 1–77)

**Description:**
`HTTPTokener.java` is a verbatim copy of the `org.json` 2010-12-24 version of `HTTPTokener`. It extends `JSONTokener` and implements `nextToken()` to parse HTTP header token strings. The logic performs no external calls, no file I/O, and no user data persistence. The security exposure of this class is limited to:

1. Its age (2010 release) — it predates Java 8 and has not benefited from 15 years of library maintenance.
2. The `nextToken()` method has a quoted-string branch that does not check for CRLF injection within the quoted string body; however, this is a parsing utility, not a HTTP request constructor, so direct injection risk is low.

There are no SSRF, path traversal, credential, or XSS concerns in this file in isolation.

**Risk:** Informational. Vendored ancient library code represents a maintenance and supply-chain risk but no immediate exploitable vulnerability in isolation.

**Recommendation:** Replace the vendored `com.json` package (which includes `HTTP.java`, `HTTPTokener.java`, and the implied `JSONTokener.java`/`JSONObject.java`) with the current official `org.json:json` Maven dependency. This eliminates version skew and ensures future security patches are applied via dependency management.

---

## Summary

| Severity | Count | Findings |
|----------|-------|----------|
| CRITICAL | 3 | Hardcoded API auth token; HTTP-only API communication with token in plaintext; SSRF via unvalidated URL in `downloadFile` |
| HIGH | 4 | Path traversal via `Content-Disposition` filename; static field race condition / cross-tenant data leakage; reflected XSS via unencoded `equipId`; NPE / auth logic flaw in session attribute access |
| MEDIUM | 4 | No redirect policy (SSRF via redirect); commented-out hardcoded credentials; no TLS certificate validation configuration; unescaped `bean:write` in CSS context |
| LOW | 4 | `@Data` toString operational data leakage to logs; `ImpactLevel` calibration threshold exposure to all users; no HTTP connection timeouts; raw Iterator in HTTP.java |
| INFO | 2 | `importLib.jsp` is clean; `HTTPTokener.java` is vendored ancient library code |

**CRITICAL: 3 / HIGH: 4 / MEDIUM: 4 / LOW: 4 / INFO: 2**
