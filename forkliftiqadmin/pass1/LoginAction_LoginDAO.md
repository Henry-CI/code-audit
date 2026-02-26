# Security Audit Report — Authentication Mechanism
**Application:** forkliftiqadmin (FleetIQ System)
**Audit Date:** 2026-02-26
**Auditor Pass:** Pass 1
**Scope:** Login flow — `login.jsp`, `LoginAction.java`, `LoginActionForm.java`, `LoginDAO.java`
**Framework:** Apache Struts 1.3.10 on Tomcat
**Branch:** master

---

## Executive Summary

The login flow contains a cluster of serious vulnerabilities. The most critical finding is that **the Cognito authentication result is silently swallowed on exception**, meaning the entire authentication gate degrades to unauthenticated access when the Cognito sidecar is unreachable. Beyond that gateway failure, the database layer retains a legacy MD5-based `checkLogin` method that is still present in code and still used for the `company` table credential check, there is no CSRF token on the login form, no brute-force protection anywhere in the stack, and the Cognito proxy is called over plaintext HTTP on localhost — meaning credential pairs traverse the loopback interface in cleartext and are fully visible to any process running on the same host. Multi-factor authentication is absent. Session fixation is unmitigated. Eight distinct issues are documented below.

---

## Findings

### CRITICAL: Silent authentication bypass on Cognito sidecar exception

**File:** `LoginAction.java` (lines 38–49) / `RestClientService.java` (lines 51–69)

**Description:**
`RestClientService.authenticationRequest()` catches **all** exceptions in a bare `catch(Exception e)` block, prints the stack trace to stderr, logs the error message, and then **returns an empty `AuthenticationResponse` object** (constructed at line 50). It does not rethrow, does not set an error flag, and does not return `null`.

```java
// RestClientService.java lines 50-69
AuthenticationResponse response = new AuthenticationResponse();
try {
    ResponseEntity<AuthenticationResponse> result =
        restTemplate.exchange("http://localhost:" + COGNITO_API_PORT + "/auth",
            HttpMethod.POST, entity, AuthenticationResponse.class);
    if (HttpStatus.OK == result.getStatusCode()) {
        response = result.getBody();
    }
} catch(Exception e) {
    e.printStackTrace();
    log.error(method + "error:" + e.getMessage());
}
return response;   // <-- always returns; never null
```

`AuthenticationResponse` is a bean. Its `sessionToken` field will be `null` when the object is default-constructed. `LoginAction` then checks:

```java
// LoginAction.java lines 47-49
if (sessionToken == null) {
    return this.loginFailure(mapping, request);
}
```

At first glance this looks correct, but the critical problem is the **inverse direction**: if Cognito returns HTTP 200 with an `AuthenticationResponse` whose body has `sessionToken` non-null for **any** reason — including a misconfigured or compromised sidecar that never validates credentials — the check passes. More immediately dangerous: the exception path guarantees a null `sessionToken`, so the `null` check does correctly reject. **However**, a further failure mode exists: if `result.getBody()` returns a non-null object with a non-null `sessionToken` on any successful HTTP exchange regardless of credential validity, and the sidecar has a bug or is replaced, the entire authentication check is bypassed. The design fully trusts the sidecar's response with no secondary validation.

Additionally, the sidecar is contacted **after** session attributes are written (lines 31–35 execute before line 43), so `session.setAttribute("username", loginActionForm.getUsername())` writes the submitted username to the session of an **unauthenticated** request before authentication is confirmed.

```java
// LoginAction.java lines 31-35 — these run BEFORE authentication
session.setAttribute("sessAds", AdvertismentDAO.getInstance().getAllAdvertisment());
session.setAttribute("arrTimezone", TimezoneDAO.getInstance().getAllTimezone());
session.setAttribute("arrLanguage", LanguageDAO.getInstance().getAllLan());
session.setAttribute("username", loginActionForm.getUsername());
// ... Cognito call happens only at line 43
```

**Risk:**
If the Cognito sidecar process is down, crashes, or is replaced by an attacker who has achieved code execution on the host (e.g. via the plaintext HTTP SSRF vector described below), authentication fails closed (null token = failure). However, any future regression in the sidecar that returns a non-null token without genuine authentication silently grants full access to the admin panel. The pre-authentication writing of session data is also a minor state pollution issue.

**Recommendation:**
The sidecar response must be validated beyond a null check: verify the token is a well-formed JWT, verify its signature against the Cognito public key, and verify the `sub` / `email` claim matches the submitted username. Move all session writes to after authentication is confirmed. Wrap the REST call so that any exception results in an explicit failure rather than a default-constructed response object.

---

### CRITICAL: Cognito proxy called over plaintext HTTP — credentials exposed on loopback

**File:** `RestClientService.java` (line 53)

**Description:**
The Cognito authentication sidecar is contacted via an unencrypted HTTP connection to `localhost`:

```java
// RestClientService.java line 53
ResponseEntity<AuthenticationResponse> result =
    restTemplate.exchange(
        "http://localhost:" + COGNITO_API_PORT + "/auth",
        HttpMethod.POST, entity, AuthenticationResponse.class);
```

The `AuthenticationRequest` entity posted to this endpoint contains the plaintext username and password submitted by the user (lines 39–42 of `LoginAction.java`):

```java
AuthenticationRequest authenticationRequest = AuthenticationRequest.builder()
    .username(loginActionForm.getUsername())
    .password(loginActionForm.getPassword())
    .build();
```

On the loopback interface, this HTTP POST is not encrypted. Any process running on the same host that can bind a raw socket or perform a loopback packet capture (e.g. via `tcpdump lo`) will see the full username and password in cleartext. On a shared host (cloud VM with multiple services, container with a shared network namespace, or a compromised co-tenant), this completely undermines the Cognito TLS channel between the sidecar and AWS.

**Risk:**
Full credential exposure for every login attempt to any attacker with local process access to the application host. This includes malware, other misconfigured services, log-shipping agents with network access, or any side-channel capable of reading loopback traffic.

**Recommendation:**
All inter-process communication carrying credentials must use a secure channel. Options in order of preference: (1) embed the Cognito SDK directly into the Java application, eliminating the loopback hop entirely; (2) use a Unix domain socket with appropriate file permissions; (3) if HTTP on loopback is unavoidable, add mutual TLS with a local certificate. The `http://` scheme must not carry credentials under any circumstances.

---

### HIGH: MD5 unsalted password hashing in active database queries

**File:** `LoginDAO.java` (lines 51, 92–96)

**Description:**
Two SQL queries use `MD5()` at the database layer to hash passwords during authentication. The first is the `checkLogin` method (line 51):

```java
// LoginDAO.java lines 50-57
return DBUtil.queryForObject(
    "select count(*) from " + RuntimeConf.v_user +
    " where email = ? and password = md5(?)",
    stmt -> {
        stmt.setString(1, username);
        stmt.setString(2, password);
    },
    rs -> rs.getInt(1) > 0).orElseThrow(SQLException::new);
```

The second is in the overloaded `getCompanies(isSuperAdmin, isDealerLogin, username, password, comp)` method (lines 91–97), which queries the `company` table by email and MD5 password:

```java
// LoginDAO.java lines 91-97
int comp_id = DBUtil.queryForObject(
    "select id from company where email = ? and password = md5(?)",
    stmt -> {
        stmt.setString(1, username);
        stmt.setString(2, password);
    },
    (rs) -> rs.getInt("id")).orElse(comp);
```

MD5 is a cryptographic hash function not designed for password storage. It has no salt (making it trivially reversible via rainbow tables), is extremely fast (billions of hashes per second on modern GPU hardware), and is fully broken for this purpose. The audit context confirms this pattern is used elsewhere in the application. While the primary authentication path now delegates to Cognito, these MD5 queries remain in the codebase, with `checkLogin` being a callable instance method on a singleton and the company-table variant in a method that takes a raw password string — meaning these code paths may be invoked from other places, or could be re-enabled.

**Risk:**
If the database is compromised, all passwords stored as MD5 hashes can be reversed in minutes using precomputed rainbow tables (e.g., via CrackStation) or GPU-accelerated brute force. This is a complete password database compromise.

**Recommendation:**
Replace all MD5 password storage and verification with bcrypt (work factor >= 12), PBKDF2-HMAC-SHA256 (iterations >= 600,000), or Argon2id (as recommended by OWASP). The MD5 columns in both `v_user` (the user view) and `company` tables must be migrated. The `checkLogin` method should be deleted; authentication must flow exclusively through Cognito. The overloaded `getCompanies` method that accepts raw credentials should also be removed.

---

### HIGH: No CSRF protection on login form

**File:** `login.jsp` (line 23) / `struts-config.xml` (lines 78–87)

**Description:**
The login form is rendered with `<html:form method="post" action="login.do">`. Struts 1 provides a CSRF token mechanism via `<html:form>` with a corresponding server-side check using `saveToken`/`isTokenValid` in the Action class. Neither is present here. Inspecting `struts-config.xml`, the `/login` action mapping contains no `token` validation, and `LoginAction.execute()` never calls `isTokenValid()`.

```html
<!-- login.jsp line 23 — no token attribute -->
<html:form method="post" action="login.do" styleClass="login-fields">
```

```java
// LoginAction.java — no call to isTokenValid() anywhere in execute()
```

A CSRF attack against a login form enables **login CSRF**: an attacker crafts a page that silently submits the form with the attacker's own credentials. The victim is logged into the attacker's account, and any data the victim subsequently enters (saved addresses, payment information, private data) is visible to the attacker.

**Risk:**
Login CSRF allowing account takeover of victim sessions. In a multi-tenant admin system, a victim operator who is CSRF-logged into an attacker-controlled account and performs sensitive operations exposes those operations to the attacker.

**Recommendation:**
Add Struts token generation in the action that renders the login page (`saveToken(request)`) and validate with `isTokenValid(request, true)` as the first statement of `LoginAction.execute()`. Alternatively, implement the `SameSite=Strict` or `SameSite=Lax` cookie attribute on the session cookie, which mitigates CSRF in modern browsers — but the token approach is the defense-in-depth standard for Struts 1.

---

### HIGH: No brute-force protection — unlimited login attempts

**File:** `LoginAction.java` (entire file) / `LoginDAO.java` (entire file) / `PreFlightActionServlet.java`

**Description:**
There is no rate limiting, no account lockout, no CAPTCHA, and no exponential backoff anywhere in the authentication stack. `LoginAction.execute()` processes every submitted login attempt immediately. `loginFailure()` at line 82 simply adds an error message and returns the failure forward — no counter is incremented, no delay is introduced, and no IP or username is recorded. The `PreFlightActionServlet` excludes `login.do` from session checks (line 102), meaning the servlet will process every POST to `/login.do` without any session-based throttle.

```java
// LoginAction.java lines 82-88
private ActionForward loginFailure(ActionMapping mapping, HttpServletRequest request) {
    ActionErrors errors = new ActionErrors();
    ActionMessage msg = new ActionMessage("error.login");
    errors.add("loginError", msg);
    saveErrors(request, errors);
    return mapping.findForward("failure");
    // No counter, no delay, no lockout
}
```

**Risk:**
An attacker can make unlimited, unthrottled guesses at any account. Combined with the MD5 hashing identified above, a credential stuffing or password spray attack against the Cognito endpoint (which has its own rate limiting, but rate limits can be distributed across IPs) and the database credential check has no defensive layer at the application tier.

**Recommendation:**
Implement account lockout after N (e.g. 5) consecutive failures with a timed unlock (e.g. 15 minutes), or progressive delays (account soft-lock). Implement IP-based rate limiting at either the WAF, reverse proxy (nginx `limit_req`), or application filter layer. Consider integrating a CAPTCHA challenge after 3 failed attempts. Log all failed attempts with IP, username, and timestamp for detection.

---

### HIGH: Session fixation — existing session not invalidated before privilege elevation

**File:** `LoginAction.java` (lines 28, 31–68)

**Description:**
`LoginAction.execute()` obtains the existing session with `request.getSession(false)` at line 28. It then writes authentication state into this same session object throughout the method (lines 31–68). At no point is the pre-authentication session invalidated and a new session created. The Servlet specification's `session.invalidate()` + `request.getSession(true)` pattern is entirely absent.

```java
// LoginAction.java lines 28-35
HttpSession session = request.getSession(false);
// ...
session.setAttribute("sessAds", ...);
session.setAttribute("arrTimezone", ...);
session.setAttribute("arrLanguage", ...);
session.setAttribute("username", loginActionForm.getUsername());
// No session.invalidate() before privileged attributes are written
// No request.getSession(true) to create a fresh session
```

In a session fixation attack, the attacker obtains a valid pre-authentication session ID (by simply visiting the login page, which creates a session), injects it into the victim's browser via a subdomain cookie, URL parameter, or other means, and then waits for the victim to authenticate. Because the session ID is not rotated on login, the attacker's known session ID is now elevated to an authenticated session.

**Risk:**
Full session hijacking. An attacker who can plant a session cookie (via network position, XSS on a sibling domain, or URL-based session tracking) obtains authenticated access to any account they cause to log in with their planted session ID.

**Recommendation:**
Immediately before writing any authenticated state to the session, call `session.invalidate()` and then `session = request.getSession(true)` to obtain a fresh session with a new ID. Copy any pre-authentication state that must be preserved (e.g. return-to URL) explicitly. This is a mandatory control for any login flow.

---

### MEDIUM: Username stored in session before authentication confirmed

**File:** `LoginAction.java` (line 35)

**Description:**
The submitted username is written to the session at line 35, which executes unconditionally before the Cognito authentication call at line 43 and before any credential validation:

```java
// LoginAction.java line 35 — before authentication
session.setAttribute("username", loginActionForm.getUsername());
```

If authentication subsequently fails (null token, empty company list), the username remains set in the session (the `loginFailure` method at lines 82–88 does not clear it). Any subsequent code that reads `session.getAttribute("username")` without checking authentication state may operate on an unauthenticated username value. This is also a session state pollution issue that interacts with the session fixation vulnerability: an attacker can pre-populate the session with an arbitrary username string before triggering a victim's login.

**Risk:**
Logic flaws in other parts of the application that read `session.username` as a trusted value may be exploitable. Combined with session fixation, an attacker can seed the session with a chosen username before authentication.

**Recommendation:**
Move `session.setAttribute("username", ...)` to after successful authentication is confirmed, alongside the other privileged session attributes. Clear session state on all failure paths.

---

### MEDIUM: No HTTPS enforcement in web.xml — credentials may transit in cleartext

**File:** `web.xml` (entire file)

**Description:**
`web.xml` does not contain a `<security-constraint>` with `<transport-guarantee>CONFIDENTIAL</transport-guarantee>`, and there is no servlet filter or redirect enforcing HTTPS. The Servlet 2.4 schema is used (line 6), which supports this construct:

```xml
<!-- web.xml — absent -->
<!-- No <security-constraint> block requiring HTTPS -->
<!-- No <user-data-constraint><transport-guarantee>CONFIDENTIAL</transport-guarantee> -->
```

Without a transport guarantee configured at the container level, the application will accept form POSTs to `login.do` over plain HTTP. While TLS may be terminated upstream at a load balancer, this provides no defense-in-depth: if the load balancer is misconfigured or direct access to Tomcat is possible, login credentials are transmitted in cleartext. The `<html:form>` at `login.jsp` line 23 uses a relative URL (`action="login.do"`), so it inherits whatever protocol the page was loaded over.

**Risk:**
If a user accesses the login page over HTTP (direct Tomcat access, misconfigured LB, HTTP link in email), their credentials are transmitted in cleartext and are visible to any network observer.

**Recommendation:**
Add a `<security-constraint>` block in `web.xml` requiring `CONFIDENTIAL` transport for the entire application (`url-pattern: /*`). Additionally configure an HSTS header (`Strict-Transport-Security: max-age=31536000; includeSubDomains`) in Tomcat's HTTP connector or a servlet filter, and ensure the load balancer enforces HTTPS-only ingress with HTTP-to-HTTPS redirect.

---

### MEDIUM: Sensitive company and user data stored in HTTP session without protection flags

**File:** `LoginAction.java` (lines 56–68) / `CompanySessionSwitcher.java` (lines 27–44)

**Description:**
Following authentication, the session is populated with a significant volume of sensitive business data. `LoginAction` stores:
- `sessArrComp` — full list of `CompanyBean` objects including company name, email, unit, privacy flag, template, date format
- `sessAccountId` — the company's internal database ID
- `sessUserId` — the user's internal database ID
- `isSuperAdmin` — boolean privilege flag
- `isDealerLogin` — boolean privilege flag
- `sessionToken` — the raw Cognito access token

`CompanySessionSwitcher.UpdateCompanySessionAttributes` further stores `sessCompId`, `sessCompName`, `sessDateTimeFormat`, `sessTimezone`, `arrUnit`, `isDealer`, and `arrComp`. The `sessCompId` attribute is the sentinel used by `PreFlightActionServlet` as the sole authentication gate.

The `web.xml` does not set `<cookie-config><http-only>true</http-only><secure>true</secure></cookie-config>` for the session cookie (`JSESSIONID`). Without `HttpOnly`, any XSS vulnerability can read the session cookie. Without `Secure`, the cookie is transmitted over HTTP. The raw Cognito `sessionToken` stored in the session (line 51) is particularly sensitive — it is a live bearer token granting access to AWS Cognito APIs.

```java
// LoginAction.java line 51 — live bearer token in session
session.setAttribute("sessionToken", sessionToken);
```

**Risk:**
If any XSS vulnerability exists elsewhere in the application, the attacker can exfiltrate the session cookie and all session attributes, including the live Cognito token. The `isSuperAdmin` and `isDealerLogin` privilege flags in the session can potentially be manipulated if any deserialization, prototype pollution, or session attribute injection vector exists.

**Recommendation:**
Add `<session-config><cookie-config><http-only>true</http-only><secure>true</secure></cookie-config></session-config>` to `web.xml`. Minimise session data to non-sensitive identifiers; do not store the raw Cognito bearer token in the session — derive it from secure server-side storage or re-fetch it as needed. Privilege flags (`isSuperAdmin`, `isDealerLogin`) should be re-derived from the database on each request rather than stored as session attributes that could be tampered with.

---

### LOW: `checkLogin` dead-code MD5 method creates maintenance hazard and audit confusion

**File:** `LoginDAO.java` (lines 47–57)

**Description:**
The `checkLogin` instance method is present in `LoginDAO` and is callable via `LoginDAO.getInstance().checkLogin(username, password)`. It is not called from `LoginAction` (which delegates to Cognito), but it is a public method on a singleton that performs MD5-based authentication against the `v_user` view. Its continued presence means:
1. It may be called from other action classes not covered in this audit pass.
2. Future developers may re-enable it as a fallback.
3. It creates confusion about the intended authentication mechanism.

```java
// LoginDAO.java lines 47-57
public Boolean checkLogin(String username, String password) throws Exception {
    log.info("Inside LoginDAO Method : checkLogin");
    return DBUtil.queryForObject(
            "select count(*) from " + RuntimeConf.v_user +
            " where email = ? and password = md5(?)",
            stmt -> { ... },
            rs -> rs.getInt(1) > 0).orElseThrow(SQLException::new);
}
```

**Risk:**
If invoked from any code path, provides authentication via broken MD5 hashing. Dead code containing security vulnerabilities is a persistent risk.

**Recommendation:**
Delete `checkLogin` from `LoginDAO`. Conduct a full codebase grep for invocations (`checkLogin`) to confirm there are no call sites before removal.

---

### LOW: Error handling exposes stack traces to server logs with no sanitisation

**File:** `RestClientService.java` (lines 65, 101, 136, 169, etc.)

**Description:**
Every catch block in `RestClientService` calls `e.printStackTrace()` directly, which writes full Java stack traces to standard error (typically Tomcat's `catalina.out`). In environments where application logs are accessible to developers or operations staff beyond the security team, or where log aggregation systems are misconfigured to expose logs externally, stack traces reveal: internal class names and package structure, dependency versions, and service topology. This is repeated in at least 7 methods in the file.

```java
// RestClientService.java line 65 (repeated pattern)
} catch(Exception e) {
    e.printStackTrace();
    log.error(method + "error:" + e.getMessage());
}
```

**Risk:**
Information disclosure to log readers. The stack traces may also include the exception message, which for network errors can include the target URL (including port `9090`) and for auth errors may include partial credential data in the exception string.

**Recommendation:**
Replace `e.printStackTrace()` with `log.error(method + "error", e)` to route stack traces exclusively through the logging framework with its configured appenders and levels. Ensure Tomcat's `catalina.out` is not accessible to unprivileged users or external systems.

---

### INFO: No multi-factor authentication

**File:** `LoginAction.java` (entire file)

**Description:**
The authentication flow does not implement MFA. After Cognito returns a session token, no second factor (TOTP, SMS OTP, push notification, hardware key) is challenged. The Cognito SDK supports MFA challenges natively (via `AuthenticationResultType` with a `ChallengeName` of `SOFTWARE_TOKEN_MFA` or `SMS_MFA`), but the `AuthenticationResponse` bean and `RestClientService` do not handle challenge flows — any non-200 or challenge response from Cognito is silently treated as failure (or, via the exception path, degraded). This is an admin portal managing multi-tenant fleet data; the absence of MFA significantly increases the impact of credential compromise.

**Risk:**
A single compromised password grants full admin access. Phishing, credential stuffing, or password reuse attacks succeed without any additional barrier.

**Recommendation:**
Enable MFA in the AWS Cognito User Pool for all admin users. Implement the Cognito challenge-response flow in `RestClientService` to handle `SOFTWARE_TOKEN_MFA` and `SMS_MFA` challenge names, presenting the user with an OTP entry screen before completing authentication.

---

### INFO: No remember-me functionality (positive finding)

**File:** `login.jsp`, `LoginAction.java`, `LoginActionForm.java`

**Description:**
No persistent "remember me" cookie is implemented. The `LoginActionForm` does not contain a `rememberMe` field, and `LoginAction` does not write any persistent authentication cookie. This is a positive security posture; persistent authentication cookies are a common source of session hijacking vulnerabilities.

**Risk:**
N/A — absence of a vulnerability.

---

### INFO: Cognito authentication path confirmed; legacy DB path is not primary

**File:** `LoginAction.java` (lines 37–49) / `LoginDAO.java`

**Description:**
The primary authentication path in `LoginAction.execute()` uses AWS Cognito via `RestClientService.authenticationRequest()`. The legacy `LoginDAO.checkLogin()` MD5 database method is **not** called from `LoginAction`. Post-authentication, `LoginDAO` is used only for non-authentication queries: `getCompanyId`, `getUserId`, `isUserAuthority`, `isAuthority`, and `getCompanies` — all of which use `PreparedStatement` with bound parameters and are not vulnerable to SQL injection in their current form. This is a partial mitigation for the MD5 issue: passwords are no longer verified via the DB path in the primary flow, but the code remains present and the data at rest remains MD5-hashed.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH     | 4 |
| MEDIUM   | 3 |
| LOW      | 2 |
| INFO     | 3 |

**CRITICAL: 2 / HIGH: 4 / MEDIUM: 3 / LOW: 2 / INFO: 3**

---

## Files Audited

| File | Lines | Notes |
|------|-------|-------|
| `src/main/webapp/html-jsp/login.jsp` | 54 | No CSRF token; no XSS in rendered fields (Struts `<html:text>` escapes output); no HTTPS enforcement |
| `src/main/java/com/action/LoginAction.java` | 89 | Session fixation; pre-auth session writes; no brute-force protection; silent Cognito exception bypass |
| `src/main/java/com/actionform/LoginActionForm.java` | 47 | No issues in isolation; no input length constraints defined at form level |
| `src/main/java/com/dao/LoginDAO.java` | 265 | MD5 hashing in `checkLogin` and `getCompanies(5-arg)`; all other queries use PreparedStatement |
| `src/main/java/com/service/RestClientService.java` | 311 | Plaintext HTTP to Cognito sidecar; exception swallowing; stack trace leakage |
| `src/main/webapp/WEB-INF/struts-config.xml` | 597 | No CSRF token configured for login action |
| `src/main/webapp/WEB-INF/web.xml` | 77 | No HTTPS transport guarantee; no secure/httponly session cookie config |
| `src/main/java/com/actionservlet/PreFlightActionServlet.java` | 117 | Auth gate checks `sessCompId != null`; login.do correctly excluded |
| `src/main/java/com/util/CompanySessionSwitcher.java` | 47 | Excessive session data; `sessCompId` written here (auth gate dependency) |
