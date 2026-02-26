# Security Audit: Deployment Descriptors
**Application:** forkliftiqadmin (FleetIQ System)
**Audit Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Branch:** master
**Files Audited:**
- `src/main/webapp/WEB-INF/web.xml`
- `src/main/webapp/WEB-INF/validation.xml`
- `src/main/webapp/WEB-INF/validator-rules.xml`
- `src/main/webapp/WEB-INF/tiles-defs.xml`
- `src/main/webapp/WEB-INF/struts-config.xml` (cross-reference)
- `src/main/java/com/actionservlet/PreFlightActionServlet.java` (cross-reference)

---

## Findings

---

### CRITICAL: No HTTPS Transport Guarantee (Missing `<security-constraint>`)
**File:** `web.xml` (entire file)
**Description:** There is no `<security-constraint>` element anywhere in `web.xml`. Without a `<transport-guarantee>CONFIDENTIAL</transport-guarantee>` constraint, the container (Tomcat) will not enforce HTTPS for any URL pattern. The application handles authentication credentials (username/password) via the `/login.do` endpoint, as well as session tokens and sensitive fleet/operator data on all other endpoints. Any of this traffic can be transmitted in plaintext over HTTP if the deployment does not independently enforce HTTPS at a load balancer or Tomcat connector level — and there is no defence-in-depth fallback in the application itself.
**Risk:** Full credential and session token interception via network eavesdropping (man-in-the-middle). An attacker on the same network segment can harvest passwords and session cookies without any cryptographic barrier enforced by the application.
**Recommendation:** Add a `<security-constraint>` block enforcing `CONFIDENTIAL` transport over all URL patterns:
```xml
<security-constraint>
  <web-resource-collection>
    <web-resource-name>Entire Application</web-resource-name>
    <url-pattern>/*</url-pattern>
  </web-resource-collection>
  <user-data-constraint>
    <transport-guarantee>CONFIDENTIAL</transport-guarantee>
  </user-data-constraint>
</security-constraint>
```
Additionally configure the Tomcat `<Connector>` with `redirectPort` and ensure an HTTPS connector is active.

---

### CRITICAL: No `HttpOnly` or `Secure` Flags on Session Cookie
**File:** `web.xml` (lines 45–47)
**Description:** The `<session-config>` block contains only a timeout value and no `<cookie-config>` child element. This means:
1. The `JSESSIONID` session cookie is issued **without the `HttpOnly` flag**, making it readable by any JavaScript executing in the browser. Combined with any XSS vulnerability (client-side or reflected), an attacker can trivially exfiltrate the session cookie via `document.cookie`.
2. The session cookie is issued **without the `Secure` flag**, meaning it will be transmitted over plain HTTP connections. Even if HTTPS is enforced at a load balancer, any downgrade scenario or mixed-content request can leak the cookie.

Current configuration:
```xml
<session-config>
    <session-timeout>30</session-timeout>
</session-config>
```
**Risk:** Session hijacking via XSS cookie theft (missing `HttpOnly`). Session cookie leakage over unencrypted channels (missing `Secure`). Both are baseline mitigations expected in any production web application handling authenticated sessions.
**Recommendation:** Add a `<cookie-config>` block:
```xml
<session-config>
    <session-timeout>30</session-timeout>
    <cookie-config>
        <http-only>true</http-only>
        <secure>true</secure>
    </cookie-config>
</session-config>
```
Note: `<cookie-config>` requires Servlet 3.0 (Tomcat 7+). The application currently declares `version="2.4"` in its `<web-app>` schema — this must be upgraded to `version="3.0"` or higher for the `<cookie-config>` element to be recognised. If upgrading the schema is not immediately feasible, configure `useHttpOnly="true"` on the Tomcat `<Context>` element and enforce `Secure` at the Tomcat `<Connector>` or load balancer.

---

### CRITICAL: `uploadfile.do` Excluded from Authentication — Not Mapped in struts-config.xml
**File:** `PreFlightActionServlet.java` (line 113), `struts-config.xml` (entire action-mappings section)
**Description:** `uploadfile.do` is unconditionally excluded from the authentication gate in `PreFlightActionServlet.excludeFromFilter()`. Any request whose path ends with `uploadfile.do` bypasses the session validity check entirely. However, there is **no corresponding `<action>` mapping for `/uploadfile` in `struts-config.xml`**. This means:
- The exclusion entry is either dead code referencing a removed action, OR
- The action is mapped elsewhere (e.g., in a second struts-config file not referenced in `web.xml`, or handled by a different servlet).

If this endpoint existed previously and handled file uploads without authentication, or if it is re-introduced in future development, it will be exposed to unauthenticated access immediately, since the auth-gate bypass is permanently in place. Furthermore, if there is any ambiguity about whether the action is reachable via another path alias, file upload without authentication represents a critical attack surface (arbitrary file upload, server-side file write).
**Risk:** If the endpoint is or becomes active, unauthenticated arbitrary file upload leading to remote code execution or server compromise. The orphaned exclusion also creates confusion for future developers who may inadvertently re-enable a dangerous endpoint.
**Recommendation:** Remove `uploadfile.do` from the exclusion list in `PreFlightActionServlet` immediately, or document and justify the exclusion with a confirmed mapping. Audit all struts-config files and servlet mappings to determine whether this action is currently reachable. If a public file upload endpoint is genuinely required, implement strict authentication, file-type whitelisting, size limits, and storage outside the web root.

---

### HIGH: `mailer.do` and `api.do` Excluded from Authentication — No Input Validation on Actions
**File:** `PreFlightActionServlet.java` (lines 105–106), `struts-config.xml` (lines 440–451)
**Description:** Both `mailer.do` (`/mailer` action, `com.action.MailerAction`) and `api.do` (`/api` action, `com.action.AppAPIAction`) are explicitly excluded from session authentication in `PreFlightActionServlet`. These endpoints are reachable by any unauthenticated HTTP client. The `mailer.do` action (confirmed reachable, mapped in struts-config) can be abused as an **open mail relay** — any unauthenticated caller may be able to trigger outbound email from the server. The `api.do` action exposes the application API endpoint (`AppAPIAction` forwarding to `/html-jsp/apiXml.jsp`) without any session gate. Neither action has validator-framework validation rules defined in `validation.xml`.
**Risk:** `mailer.do` - open mail relay abuse, spam origination, phishing via the application's mail server, potential resource exhaustion. `api.do` - unauthenticated access to application data or functionality exposed by the API; attack surface for injection, enumeration, and data exfiltration without leaving an authenticated audit trail.
**Recommendation:** Evaluate whether these endpoints truly require unauthenticated access. For `mailer.do`, implement at minimum a CAPTCHA or shared-secret token for inbound calls, and enforce rate limiting. For `api.do`, implement token-based authentication (API key or OAuth). Move authentication logic inside the respective `Action` classes if the servlet-level gate cannot be applied, rather than relying on a blanket exclusion.

---

### HIGH: `adminRegister.do` Excluded from Authentication — Self-Registration Endpoint Publicly Accessible
**File:** `PreFlightActionServlet.java` (line 107), `struts-config.xml` (lines 145–157)
**Description:** `adminRegister.do` is excluded from authentication, meaning any unauthenticated user can submit registration data. The action (`AdminRegisterAction`) handles three code paths: new company registration (`successregister`), adding a sub-company via a dealer (`successadd`), and updating an existing company record (`successupdate`). The registration path (creating a new admin company account) being publicly accessible is by design, but the **update** code path (`successupdate` forwarding to `/adminmenu.do?action=home`) potentially allows modification of existing company records without prior authentication, depending solely on form field values supplied by the caller. Validation rules for `adminRegisterActionForm` require only `name` (minlength 3), `contact_name` (required), `email` (required, email format), and `password` (minlength 4). There is no CSRF protection, no rate limiting, and no account enumeration defence.
**Risk:** Unauthenticated account creation allowing spam registrations and resource exhaustion. Potential for unauthenticated modification of existing company records if the action's update path does not independently enforce authorization. Weak password policy (minlength 4) for admin accounts.
**Recommendation:** Require a pre-shared invite token or CAPTCHA for public registration. The update/add sub-company code paths should require an authenticated session — remove `adminRegister.do` from the exclusion list and handle the distinction between public self-registration and authenticated admin operations in separate action paths. Increase password minimum length to at least 8 characters and add complexity rules.

---

### HIGH: `loadbarcode.do` Excluded from Authentication — Unauthenticated Barcode/Data Endpoint
**File:** `PreFlightActionServlet.java` (line 112), `struts-config.xml` (lines 458–461)
**Description:** `loadbarcode.do` is excluded from authentication and maps to `com.action.BarCodeAction`, which forwards to `/html-jsp/apiXml.jsp` on success (the same JSP used by the `api.do` endpoint). This means barcode lookup or data retrieval functionality is available to unauthenticated callers. Depending on what `BarCodeAction` does (likely a device-facing lookup), it may expose asset/fleet data without any access control. There are no validation rules for the form used by this action.
**Risk:** Unauthenticated enumeration of asset/equipment barcode data. Information disclosure of internal asset identifiers, fleet composition, or equipment status to any caller who can reach the server.
**Recommendation:** Implement token-based authentication for device-facing endpoints rather than removing them from the auth gate entirely. If barcode lookups must be public, ensure the data returned is minimal and does not expose internal identifiers or sensitive fleet details.

---

### HIGH: Servlet API Version 2.4 — Missing Security Features
**File:** `web.xml` (lines 3–6)
**Description:** The `<web-app>` element declares `version="2.4"` against the J2EE 2.4 schema. Servlet 2.4 predates numerous security features introduced in later versions:
- `<cookie-config>` (including `<http-only>` and `<secure>`) requires Servlet 3.0.
- `<session-config><tracking-mode>` (to restrict session tracking to cookies only, disabling URL rewriting and thus session ID exposure in URLs) requires Servlet 3.0.
- `<deny-uncovered-http-methods>` requires Servlet 3.1.

Using `version="2.4"` prevents declarative use of these security controls. The application is running on Tomcat which supports modern Servlet APIs, so there is no technical barrier to upgrading.
**Risk:** Inability to enforce cookie security flags declaratively. URL-based session tracking (URL rewriting) may be active by default, exposing `JSESSIONID` in server logs, browser history, and `Referer` headers. Cannot use `<deny-uncovered-http-methods>` to restrict HTTP verb abuse.
**Recommendation:** Upgrade the `<web-app>` declaration to Servlet 3.1 (or 4.0 if Tomcat 9+):
```xml
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
             http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
```
Then add `<cookie-config>` and `<tracking-mode>COOKIE</tracking-mode>` as described in other findings.

---

### HIGH: No Security-Relevant HTTP Response Headers (No CORS, CSP, XSS, or Clickjacking Filter)
**File:** `web.xml` (lines 8–15)
**Description:** The only filter configured in `web.xml` is `CharsetEncodingFilter`, which sets the request character encoding to UTF-8. There are no filters or servlet-level mechanisms to set any of the following security response headers:
- `Content-Security-Policy` (CSP) — mitigates XSS and data injection
- `X-Frame-Options` or `frame-ancestors` CSP directive — mitigates clickjacking
- `X-Content-Type-Options: nosniff` — mitigates MIME-type sniffing attacks
- `Strict-Transport-Security` (HSTS) — enforces HTTPS at the browser level
- `X-XSS-Protection` — legacy XSS filter for older browsers
- `Referrer-Policy` — prevents leakage of internal URLs in the `Referer` header
- `Permissions-Policy` — restricts browser feature access

None of the JSP templates or Struts actions were observed to set these headers programmatically either (based on the tile/include structure).
**Risk:** The absence of CSP significantly increases the impact of any XSS vulnerability. Without `X-Frame-Options`, the application is vulnerable to clickjacking attacks where it is embedded in a malicious iframe. Without HSTS, browsers will not remember to enforce HTTPS, increasing exposure to SSL-stripping attacks.
**Recommendation:** Add a servlet filter (e.g., a `SecurityHeadersFilter`) mapped to `/*` that sets all required security headers on every response. At minimum:
```
Content-Security-Policy: default-src 'self'; script-src 'self'; ...
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
```

---

### HIGH: Weak Password Minimum Length (4 Characters) for Admin Registration
**File:** `validation.xml` (lines 50–57)
**Description:** The `adminRegisterActionForm` defines a `minlength` of 4 characters for the `password` field. This is the password for a new company administrator account — the highest-privilege user in the application. A 4-character minimum password can be exhaustively brute-forced in seconds, even against a rate-limited endpoint, and trivially against any offline attack on a leaked password hash. There is no `maxlength` validator on the password field either.
**Risk:** Trivial brute-force or dictionary attack on admin accounts. Admin compromise gives full control over all operators, equipment, reports, and fleet data for a company.
**Recommendation:** Enforce a minimum password length of at least 12 characters for administrator accounts. Add complexity requirements (uppercase, lowercase, digit, symbol) via a custom `mask` validator or a custom server-side validator. Also add a `maxlength` validator (e.g., 128 characters) to prevent DoS via excessively long password hashing inputs.

---

### MEDIUM: No `maxlength` Validators on Any Form Field — Potential DoS via Oversized Input
**File:** `validation.xml` (lines 23–67)
**Description:** None of the three forms defined in `validation.xml` (`loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm`) specifies a `maxlength` constraint on any field. The `validator-rules.xml` includes a `maxlength` validator implementation that is fully available for use. Without `maxlength` enforcement, an attacker can submit arbitrarily large strings to:
- `username` and `password` fields on the login form (potentially triggering expensive hashing or database operations)
- `name`, `contact_name`, `email`, `contact_no`, `password` fields on admin registration
- `first_name`, `last_name` on the driver edit form

Additionally, the `contact_no` field on `adminRegisterActionForm` is validated only as `integer` — there is no range or length constraint, allowing arbitrarily large integer strings.
**Risk:** Application-layer denial of service through memory pressure, slow hashing of large password inputs (if using bcrypt/scrypt — less of an issue with fast hashes but still applicable), or database varchar overflow errors that may expose stack traces. Combined with the unauthenticated `adminRegister.do` endpoint, this is directly exploitable without authentication.
**Recommendation:** Add `maxlength` validators to all text fields in all three forms. Recommended limits: username/email: 254 characters (RFC 5321 limit), password: 128 characters, names: 100 characters, phone numbers: 20 characters. Example:
```xml
<field property="username" depends="required,maxlength">
    <arg1 key="${var:maxlength}" resource="false"/>
    <var><var-name>maxlength</var-name><var-value>254</var-value></var>
</field>
```

---

### MEDIUM: Only 3 of ~30 Action Forms Have Validation Rules Defined
**File:** `validation.xml` (lines 21–69); cross-referenced with `struts-config.xml` (lines 6–41)
**Description:** `struts-config.xml` declares **30 form-beans**. The `validation.xml` defines rules for only **3** of them:
- `loginActionForm` — username and password required
- `adminRegisterActionForm` — name, contact_name, email, contact_no, password
- `AdminDriverEditForm` (note: case mismatch with the declared bean `adminDriverEditForm`) — first_name, last_name required only

The following form-beans that have `validate="true"` in their action mappings but **no corresponding rules in validation.xml** will pass through the Struts ValidatorPlugIn silently (the validator finds no rules and performs no checks):

| Form Bean | Action Path | validate= |
|---|---|---|
| `switchCompanyActionForm` | `/switchCompany` | true |
| `searchActionForm` | `/search` | true |
| `registerActionForm` | `/register` | true |
| `adminDriverAddForm` | `/admindriveredit` | true |
| `adminUnitEditForm` | `/adminunitedit` | true |
| `adminUnitAssignForm` | `/adminunitassign` | true |
| `adminFleetcheckEditActionForm` | `/fleetcheckedit` | true |
| `adminFleetcheckActionForm` | `/fleetcheckconf` | true |
| `adminFleetcheckShowActionForm` | `/fleetcheckshow` | true |
| `adminFleetcheckHideActionForm` | `/fleetcheckhide` | true |
| `adminFleetcheckDeleteActionForm` | `/fleetcheckdelete` | true |
| `adminDealerActionForm` | `/dealerconvert` | true |
| `sendMailForm` | `/sendMail` | true |
| `adminAlertActionForm` | `/adminAlertAdd` | true |
| `driverJobDetailsActionForm` | `/driverjobreq` | true |
| `adminUnitServiceForm` | `/adminunitservice` | true |
| `adminUnitImpactForm` | `/adminunitimpact` | true |
| `adminUnitAccessForm` | `/adminunitaccess` | true |
| `dealerCompanyForm` | `/dealercompanies` | true |

This means all field-level validation for these forms — required checks, format checks, length checks, type checks — is entirely absent. User input to these forms is passed directly to the action classes without any framework-level sanitisation gate.
**Risk:** Injection attacks (SQL injection, stored XSS, command injection) via unvalidated fields on authenticated but unvalidated forms. Missing required-field checks allow unexpected null or empty inputs to reach DAO and business logic layers, potentially causing unhandled exceptions. Missing format checks allow type confusion attacks.
**Recommendation:** Define validation rules in `validation.xml` for all form-beans that use `validate="true"`. At minimum, add `required` checks on mandatory fields and `maxlength` on all string fields. For numeric fields (IDs, quantities, impact levels) use `integer` or `intRange` validators. Prioritise the `sendMailForm` (email injection risk), `adminUnitEditForm` (equipment data), and `adminDriverAddForm` (operator data) as highest-priority additions.

---

### MEDIUM: Case Mismatch Between `AdminDriverEditForm` in validation.xml and `adminDriverEditForm` in struts-config.xml
**File:** `validation.xml` (line 60); `struts-config.xml` (line 14)
**Description:** The validation rule in `validation.xml` defines a form named `AdminDriverEditForm` (capital 'A', capital 'D', capital 'E'). The form-bean declaration in `struts-config.xml` names it `adminDriverEditForm` (all lowercase initial letters). The Struts 1 validator framework performs case-sensitive form name lookups. This means the validation rules for `AdminDriverEditForm` in `validation.xml` will **never be applied** to the `adminDriverEditForm` action form used by `/admindriveredit` and `/admindriverlicencevalidateexist`. The first_name and last_name required checks are effectively dead.
**Risk:** The `adminDriverEditForm` form operates with zero framework-level validation. Fields `first_name` and `last_name` (intended to be required) can be submitted as empty or null, potentially causing unexpected application behaviour, null pointer exceptions, or malformed database records. Any additional validation rules added to this form in future under the wrong name will also be silently ignored.
**Recommendation:** Correct the form name in `validation.xml` line 60 from `AdminDriverEditForm` to `adminDriverEditForm` to match the struts-config.xml declaration exactly. Verify at runtime that the corrected validator triggers as expected.

---

### MEDIUM: `swithLanguage.do` Typo in Auth Exclusion List — Future Maintenance Risk
**File:** `PreFlightActionServlet.java` (line 109)
**Description:** The auth exclusion list contains `swithLanguage.do` (missing the 'c' — should be `switchLanguage.do`). The struts-config.xml maps the action as `/swithLanguage` (the typo is consistent in both places, so it currently works). However, this is a latent maintenance defect: if the action is ever renamed to fix the typo (`switchLanguage`), the exclusion list will silently fail to exclude it, causing the language-switch action to require an authenticated session — a potentially confusing regression. Conversely, someone might add a correctly spelled `switchLanguage.do` endpoint in future, and it would not be excluded.
**Risk:** Low immediate risk; medium maintenance risk. If the typo is fixed in struts-config without updating the exclusion list, language switching breaks for unauthenticated users. If a new correctly-spelled endpoint is introduced, it may inadvertently require authentication or bypass it unexpectedly.
**Recommendation:** Standardise the spelling to `switchLanguage` in both `struts-config.xml` and `PreFlightActionServlet`, and update the exclusion list entry accordingly.

---

### MEDIUM: Single Error Page Covers Only `java.lang.Exception` — HTTP Error Codes Not Handled
**File:** `web.xml` (lines 51–54)
**Description:** The `<error-page>` configuration handles only `java.lang.Exception` and maps it to `/error/error.html`. There are no HTTP status code error pages configured. This means:
- `404 Not Found` — Tomcat's default error page is served, which may expose the Tomcat version, server path information, and the requested URI.
- `403 Forbidden` — Tomcat default page exposes server information.
- `400 Bad Request`, `405 Method Not Allowed`, `500 Internal Server Error` — all served by Tomcat's default handler, which in non-production configurations typically includes exception class names and stack traces.

Additionally, the single exception-type handler only catches `java.lang.Exception`. Errors (i.e., `java.lang.Error` subclasses such as `OutOfMemoryError`, `StackOverflowError`) will not be caught and will cause Tomcat to render its default error output including stack traces.
**Risk:** Information disclosure via Tomcat default error pages: server version, Java version, internal file paths, class names, and stack traces visible to attackers. Stack trace exposure on `OutOfMemoryError` and similar JVM errors.
**Recommendation:** Add HTTP status code error pages for at minimum 400, 403, 404, and 500, all pointing to generic error pages that reveal no technical detail:
```xml
<error-page><error-code>400</error-code><location>/error/error.html</location></error-page>
<error-page><error-code>403</error-code><location>/error/error.html</location></error-page>
<error-page><error-code>404</error-code><location>/error/error.html</location></error-page>
<error-page><error-code>500</error-code><location>/error/error.html</location></error-page>
```
Also add a handler for `java.lang.Throwable` in addition to `java.lang.Exception` to catch `Error` subclasses.

---

### MEDIUM: `goSerach.do` Typo in struts-config.xml — Not in Auth Exclusion (Low Impact but Indicative)
**File:** `struts-config.xml` (line 179)
**Description:** The action path `/goSerach` is mapped (should be `/goSearch`). This is a cosmetic defect but indicative of general code quality. The action is not in the auth exclusion list (correct — it requires authentication to use the search navigation). No direct security impact from this specific finding, but the overall presence of typos in both the exclusion list (`swithLanguage`) and action paths (`goSerach`) suggests the codebase was not reviewed thoroughly, increasing the probability that other configuration errors exist.
**Risk:** Low direct security risk. Indicative of insufficient review processes.
**Recommendation:** Correct the action path to `/goSearch` in `struts-config.xml` and update any links or references to `goSerach.do` in JSP files. Adopt a code review checklist that includes configuration file spell-checking.

---

### MEDIUM: `errorDefinition` Tile Defined as a Static `.html` File
**File:** `tiles-defs.xml` (line 7)
**Description:** The `errorDefinition` tile is defined as:
```xml
<definition name="errorDefinition" path="/error/error.html"/>
```
This static HTML error page at `/error/error.html` is a direct path mapping to a file within the web root. The file itself contains no stack trace or sensitive information (confirmed by review), which is good. However:
1. The file is accessible **directly by URL** (`/error/error.html`) without any authentication gate, since it does not go through the Struts `*.do` filter. This is expected for an error page but should be noted.
2. The `global-exceptions` in `struts-config.xml` (lines 42–55) maps `java.sql.SQLException`, `java.io.IOException`, and `javax.servlet.ServletException` to `errorDefinition` — which means SQL exceptions are swallowed and a generic page shown. This is positive from an information-disclosure perspective, but means SQL errors are silently hidden, making it harder to detect injection attacks in logs (though they should be logged server-side).
3. The `<error-page>` in `web.xml` also maps `java.lang.Exception` to `/error/error.html`. The same path is used for both, providing consistent UX.
**Risk:** Low direct risk from the tile definition itself. Indirect risk: if the static file path is changed or the error page is replaced with a JSP that renders exception details, it could expose sensitive information.
**Recommendation:** Consider converting the error page to a JSP under `/WEB-INF/` (served only through Struts forwarding, not directly accessible by URL) to prevent direct access. Ensure server-side logging of all exceptions caught by `global-exceptions` is in place so that SQL errors and IO errors are not silently swallowed without audit trail.

---

### LOW: Directory Listing Status Unknown — `DefaultServlet` Not Explicitly Configured
**File:** `web.xml` (entire file)
**Description:** The `web.xml` does not include an explicit declaration of Tomcat's `DefaultServlet` with `<listing>false</listing>`. Directory listing behaviour is therefore controlled entirely by Tomcat's global `conf/web.xml`. In Tomcat's default configuration (`DefaultServlet` init-param `listings` defaults to `false`), directory listing is disabled. However, this relies on the Tomcat server configuration being correctly set and not overridden. Since the application's own `web.xml` does not explicitly disable listings, a misconfigured Tomcat installation could expose directory contents.
**Risk:** Low if Tomcat defaults are preserved. Medium if Tomcat is misconfigured. Directory listing of static asset directories could expose internal path structure, JavaScript file names, and resource inventory to attackers.
**Recommendation:** Explicitly override the `DefaultServlet` in the application's `web.xml` to ensure directory listing is always disabled regardless of server configuration:
```xml
<servlet>
    <servlet-name>default</servlet-name>
    <servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
    <init-param>
        <param-name>listings</param-name>
        <param-value>false</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>
```

---

### LOW: No `<url-pattern>` Restrictions on Sensitive File Extensions
**File:** `web.xml` (lines 29–32)
**Description:** The only servlet mapping is `*.do` for the `PreFlightActionServlet`. There are no mappings or security constraints blocking direct HTTP access to `.properties`, `.java`, `.class`, `.xml`, or `.bak` files. While `.java` source files are not typically deployed to the web root, `.properties` files (such as `MessageResources.properties`) may be present in locations accessible via the classpath but not the web root. The `WEB-INF/` directory is protected by the Servlet specification (containers must deny direct access to `WEB-INF/`), but files placed outside of `WEB-INF/` (e.g., in the webapp root) are accessible. Additionally, the `*.tld` tag library files inside `WEB-INF/` are protected by the container, but any accidentally misplaced configuration files in the web root are not.
**Risk:** Low if file deployment discipline is maintained. Medium if any configuration or source file is accidentally placed in the web root.
**Recommendation:** Add explicit `<security-constraint>` blocks with an empty `<auth-constraint/>` (deny all) for patterns such as `*.properties`, `*.bak`, `*.xml` at the root level as a defence-in-depth measure. Audit the deployed WAR/directory for any sensitive files outside of `WEB-INF/`.

---

### LOW: `<error-page>` Uses Absolute URL Reference for Static Assets
**File:** `src/main/webapp/error/error.html` (lines 10–16)
**Description:** The `/error/error.html` page loads CSS (`../skin/css/bootstrap.min.css`), JavaScript (`../skin/js/jquery.min.js`), and other static assets using relative paths that resolve relative to the `/error/` directory. If the error page is ever moved or referenced from a different context, these relative paths will break. More significantly, one external resource is loaded over HTTP (not HTTPS):
```html
<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,600,700' rel='stylesheet' type='text/css'/>
```
This triggers a mixed-content warning if the page is served over HTTPS and loads an external font over HTTP. In modern browsers this request will be blocked, breaking the font rendering on the error page. Additionally, loading external resources from Google on an error page creates a dependency on external availability and leaks the fact that a user encountered an error to Google's servers.
**Risk:** Low functional impact. Mixed-content violation breaks font loading on HTTPS. External resource dependency introduces availability risk and minor privacy leakage (error event visible to Google via font request).
**Recommendation:** Change the Google Fonts `<link>` to use HTTPS (`https://fonts.googleapis.com/...`) or self-host the font to eliminate the external dependency and mixed-content issue.

---

### LOW: DTD External Resolution in XML Configuration Files
**File:** `validation.xml` (line 3), `validator-rules.xml` (lines 2–4), `tiles-defs.xml` (lines 3–5), `struts-config.xml` (lines 2–4)
**Description:** All four XML configuration files declare `<!DOCTYPE ...>` with a `SYSTEM` or `PUBLIC` identifier pointing to external DTD URLs on `jakarta.apache.org` or `struts.apache.org`. For example:
```xml
<!DOCTYPE form-validation PUBLIC "-//Apache Software Foundation//DTD Commons Validator Rules Configuration 1.1//EN"
  "http://jakarta.apache.org/commons/dtds/validator_1_1.dtd">
```
At application startup, the XML parser may attempt to resolve these external DTDs over the network. If the server has outbound HTTP access and the parser does not cache DTDs, this creates:
1. A startup-time network dependency — if `jakarta.apache.org` is unreachable, parsing may fail or be delayed.
2. A minor information leakage (the server's external IP and application type are visible to the DTD host).
3. A theoretical XML External Entity (XXE) concern if the DTD definitions themselves were ever tampered with, though this is unlikely with well-known Apache DTDs.

In practice, Struts 1.3 bundles its own DTD copies and the parser typically resolves them locally via catalog entries, mitigating startup-time failures. However, this is configuration-dependent.
**Risk:** Low. Primarily a startup reliability and minor information-disclosure concern rather than an active vulnerability.
**Recommendation:** Configure the XML parser to use a local entity catalog (`xml:catalog`) or disable external DTD resolution where the DTDs are already bundled with the Struts JARs. Verify that Tomcat/Struts resolves these DTDs locally at startup without outbound network calls.

---

### INFO: Session Timeout Set to 30 Minutes
**File:** `web.xml` (lines 45–47)
**Description:** The session timeout is configured as 30 minutes. This is a standard value for a web application. For an admin-only fleet management system, a shorter timeout (15 minutes) would be more appropriate given the sensitivity of the data. There is no mechanism observed (in `web.xml` or tiles) for idle-session warnings to the user before timeout.
**Risk:** Informational. Unattended admin sessions remain valid for up to 30 minutes after the last request, increasing the window for session hijacking in a physical access or shared-browser scenario.
**Recommendation:** Consider reducing the session timeout to 15 minutes for this admin application. Implement a JavaScript-based idle warning modal (e.g., at 12 minutes) that prompts the user to extend the session or logs them out gracefully.

---

### INFO: `jsonResultDefinition` Tile Exposes Internal JSP Path
**File:** `tiles-defs.xml` (lines 173–175)
**Description:** The `jsonResultDefinition` tile is defined without extending any parent layout:
```xml
<definition name="jsonResultDefinition" path="/html-jsp/result/json_result.jsp">
    <put name="content" value="/html-jsp/result/json_result.jsp"/>
</definition>
```
The content is specified twice (as both the `path` and a `put` attribute), which is redundant. The JSP path `/html-jsp/result/json_result.jsp` is exposed in the tiles configuration. While `tiles-defs.xml` is not directly accessible via HTTP (it is under `WEB-INF/`), this path is used by the `/sendMail` action (success and failure both forward to `jsonResultDefinition`). If the JSON result JSP improperly outputs exception details or debugging information, it could expose internal state via the AJAX response path.
**Risk:** Informational. Internal path exposure in a server-side config file is low risk. The redundant attribute is a configuration quality issue.
**Recommendation:** Remove the redundant `<put name="content">` attribute from `jsonResultDefinition`. Review `json_result.jsp` to ensure it outputs only controlled JSON responses and never includes exception stack traces or server-side error details.

---

### INFO: `fleetcheckDefinition` Uses a Non-Standard Navigation Include (`menu_loginInfo.inc.jsp`)
**File:** `tiles-defs.xml` (lines 131–136, 137–142)
**Description:** The `fleetcheckDefinition` and `fleetcheckDashboardDefinition` tiles use `menu_loginInfo.inc.jsp` as the navigation include, while all other authenticated tiles under `adminDefinition` use `menu.inc.jsp`. This suggests that fleetcheck-related pages have a different (possibly reduced) navigation context. If `menu_loginInfo.inc.jsp` lacks proper session validation or displays session-related information in its output, it may behave differently from the main admin navigation and present an inconsistent access control surface.
**Risk:** Informational. The navigation difference may be intentional (fleetcheck is a separate public-facing feature) but should be confirmed.
**Recommendation:** Confirm that `menu_loginInfo.inc.jsp` does not expose session identifiers or admin navigation links to unauthenticated or lower-privilege users. Document the intended audience for fleetcheck pages versus admin pages.

---

### INFO: `mailerDefinition` Tile Extends `adminDefinition` — Inconsistency with Unauthenticated Endpoint
**File:** `tiles-defs.xml` (line 158–160)
**Description:** The `mailerDefinition` tile extends `adminDefinition`, which includes the standard admin header, navigation menu, and footer:
```xml
<definition name="mailerDefinition" extends="adminDefinition">
    <put name="content" value="/html-jsp/mailSuccuess.jsp"/>
</definition>
```
However, `mailer.do` is excluded from authentication in `PreFlightActionServlet`, meaning unauthenticated callers can reach this endpoint. If the admin navigation (`menu.inc.jsp`) renders user-specific session data, links to authenticated admin features, or CSRF tokens derived from session attributes, rendering it in an unauthenticated context could produce errors, expose session-dependent data, or behave unexpectedly. Additionally, the target file is named `mailSuccuess.jsp` (note the double 'c' — `Succuess` instead of `Success`), indicating a typographic error in a file name.
**Risk:** Informational / Low. Potential for null pointer exceptions if `menu.inc.jsp` accesses session attributes not present in an unauthenticated request. Typo in filename is a cosmetic defect.
**Recommendation:** Either move `mailerDefinition` to extend `loginDefinition` (which uses a simpler header without the full admin navigation), or ensure `menu.inc.jsp` gracefully handles null session attributes. Rename `mailSuccuess.jsp` to `mailSuccess.jsp`.

---

## Summary of Findings

| # | Severity | Title | File |
|---|---|---|---|
| 1 | CRITICAL | No HTTPS Transport Guarantee | web.xml |
| 2 | CRITICAL | No HttpOnly or Secure Flags on Session Cookie | web.xml |
| 3 | CRITICAL | `uploadfile.do` Excluded from Auth — No Action Mapping | PreFlightActionServlet.java / struts-config.xml |
| 4 | HIGH | `mailer.do` and `api.do` Excluded from Auth | PreFlightActionServlet.java |
| 5 | HIGH | `adminRegister.do` Publicly Accessible with Update Code Path | PreFlightActionServlet.java |
| 6 | HIGH | `loadbarcode.do` Unauthenticated Barcode/Data Endpoint | PreFlightActionServlet.java |
| 7 | HIGH | Servlet API Version 2.4 Blocks Security Cookie Features | web.xml |
| 8 | HIGH | No Security Response Headers Filter (CSP, HSTS, X-Frame-Options, etc.) | web.xml |
| 9 | HIGH | Weak Password Minimum Length (4 chars) for Admin Accounts | validation.xml |
| 10 | MEDIUM | No `maxlength` Validators on Any Field — DoS Risk | validation.xml |
| 11 | MEDIUM | Only 3 of ~30 Action Forms Have Validation Rules | validation.xml / struts-config.xml |
| 12 | MEDIUM | Case Mismatch: `AdminDriverEditForm` vs `adminDriverEditForm` — Validation Never Applied | validation.xml |
| 13 | MEDIUM | `swithLanguage.do` Typo in Exclusion List — Maintenance Risk | PreFlightActionServlet.java |
| 14 | MEDIUM | HTTP Error Codes (404, 403, 500) Not Handled — Default Tomcat Error Pages | web.xml |
| 15 | MEDIUM | `goSerach.do` Typo in struts-config.xml | struts-config.xml |
| 16 | MEDIUM | `errorDefinition` Tile as Static HTML — Stack Traces Hidden but Not Logged Confirmably | tiles-defs.xml |
| 17 | LOW | Directory Listing Not Explicitly Disabled | web.xml |
| 18 | LOW | No Restrictions on Sensitive File Extensions | web.xml |
| 19 | LOW | Mixed-Content HTTP Resource in error.html | error/error.html |
| 20 | LOW | DTD External Resolution in XML Configuration Files | validation.xml / tiles-defs.xml / struts-config.xml |
| 21 | INFO | Session Timeout 30 Minutes — Consider Reduction | web.xml |
| 22 | INFO | Redundant Attribute in `jsonResultDefinition` Tile | tiles-defs.xml |
| 23 | INFO | `fleetcheckDefinition` Uses Non-Standard Navigation Include | tiles-defs.xml |
| 24 | INFO | `mailerDefinition` Extends `adminDefinition` for Unauthenticated Endpoint | tiles-defs.xml |

---

**CRITICAL: 3 / HIGH: 6 / MEDIUM: 7 / LOW: 4 / INFO: 4**
