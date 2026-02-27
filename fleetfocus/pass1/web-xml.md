# web-xml.md — Security Audit Pass 1
**Agent:** A01
**Audit run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Files audited:**
- `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web.xml`
- `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web - Copy.xml`

---

## SECTION 1 — READING EVIDENCE

### 1.1 web.xml

**XML declaration / schema:**
- `<?xml version="1.0" encoding="ISO-8859-1"?>`
- Schema: Servlet 3.0 (`web-app_3_0.xsd`)

---

**Servlets defined (name → class):**

| Servlet Name    | Servlet Class                                         |
|-----------------|-------------------------------------------------------|
| Frm_saveuser    | com.torrent.surat.fms6.master.Frm_saveuser            |
| Frm_security    | com.torrent.surat.fms6.security.Frm_security          |
| Frm_login       | com.torrent.surat.fms6.security.Frm_login             |
| Frm_upload      | com.torrent.surat.fms6.master.Frm_upload              |
| Frm_vehicle     | com.torrent.surat.fms6.security.Frm_vehicle           |
| Frm_customer    | com.torrent.surat.fms6.security.Frm_customer          |
| Import_Files    | com.torrent.surat.fms6.util.ImportFiles               |
| CustomUpload    | com.torrent.surat.fms6.util.CustomUpload              |
| BusinessInsight | com.torrent.surat.fms6.businessinsight.BusinessInsight|

---

**Servlet mappings (name → url-pattern):**

| Servlet Name    | URL Pattern                  |
|-----------------|------------------------------|
| Frm_saveuser    | /servlet/Frm_saveuser        |
| Frm_security    | /servlet/Frm_security        |
| Frm_login       | /servlet/Frm_login           |
| Frm_upload      | /servlet/Frm_upload          |
| Frm_vehicle     | /servlet/Frm_vehicle         |
| Frm_customer    | /servlet/Frm_customer        |
| Import_Files    | /servlet/Import_Files        |
| CustomUpload    | /servlet/CustomUpload        |
| BusinessInsight | /servlet/BusinessInsight     |

---

**Filters:** None defined.

**Filter mappings:** None defined.

**Listeners:** None defined.

---

**Security constraints:**

*Constraint 1 — HTTPSOnly (lines 136–144):*
```xml
<security-constraint>
    <web-resource-collection>
        <web-resource-name>HTTPSOnly</web-resource-name>
        <url-pattern>/pages/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```
- URL pattern: `/pages/*`
- Transport guarantee: `CONFIDENTIAL`
- Auth-constraint: none (no role restriction)

*Constraint 2 — HTTPorHTTPS (lines 146–165):*
```xml
<security-constraint>
    <web-resource-collection>
        <web-resource-name>HTTPorHTTPS</web-resource-name>
        <url-pattern>*.ico</url-pattern>
        <url-pattern>/img/*</url-pattern>
        <url-pattern>/js/*</url-pattern>
        <url-pattern>/css/*</url-pattern>
        <url-pattern>/skin/js/*</url-pattern>
        <url-pattern>/skin/css/*</url-pattern>
        <url-pattern>/gps/*</url-pattern>
        <url-pattern>/reports/*</url-pattern>
        <url-pattern>/dyn_report/*</url-pattern>
        <url-pattern>/linde_reports/*</url-pattern>
        <url-pattern>/includes/*</url-pattern>
        <url-pattern>/images/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>NONE</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```
- Multiple static-resource and sensitive path patterns
- Transport guarantee: `NONE`
- Auth-constraint: none

---

**Login config:** None defined (no `<login-config>` element).

**Security roles:** None defined (no `<security-role>` element).

---

**Session config (lines 131–133):**
```xml
<session-config>
    <session-timeout>30</session-timeout>
</session-config>
```
- Timeout: 30 minutes
- No `<cookie-config>` element

---

**Error pages:** None defined.

**Context params:** None defined.

**Environment entries (`<env-entry>`):** None defined.

**Resource references (`<resource-ref>`):** None defined.

**Welcome files:** None defined.

**JSP config (lines 168–173):**
```xml
<jsp-config>
    <jsp-property-group>
        <url-pattern>*.jsp</url-pattern>
        <page-encoding>ISO-8859-1</page-encoding>
    </jsp-property-group>
</jsp-config>
```

---

### 1.2 web - Copy.xml

**XML declaration / schema:**
- `<?xml version="1.0" encoding="ISO-8859-1"?>`
- DOCTYPE: Servlet 2.3 DTD (`web-app_2_3.dtd`) — older than web.xml's Servlet 3.0

---

**Filters defined (lines 7–14):**

| Filter Name | Filter Class                                  |
|-------------|-----------------------------------------------|
| monitoring  | net.bull.javamelody.MonitoringFilter          |

**Filter mappings:**

| Filter Name | URL Pattern |
|-------------|-------------|
| monitoring  | `/*`        |

---

**Listeners (lines 15–17):**

| Listener Class                              |
|---------------------------------------------|
| net.bull.javamelody.SessionListener         |

---

**Servlets defined (name → class):**

| Servlet Name | Servlet Class                                    |
|--------------|--------------------------------------------------|
| Frm_saveuser | com.torrent.surat.fms6.master.Frm_saveuser       |
| Frm_security | com.torrent.surat.fms6.security.Frm_security     |
| Frm_login    | com.torrent.surat.fms6.security.Frm_login        |
| Frm_upload   | com.torrent.surat.fms6.master.Frm_upload         |

Note: web - Copy.xml contains only 4 of the 9 servlets present in web.xml. Frm_vehicle, Frm_customer, Import_Files, CustomUpload, and BusinessInsight are absent.

---

**Servlet mappings:**

| Servlet Name | URL Pattern             |
|--------------|-------------------------|
| Frm_saveuser | /servlet/Frm_saveuser   |
| Frm_security | /servlet/Frm_security   |
| Frm_login    | /servlet/Frm_login      |
| Frm_upload   | /servlet/Frm_upload     |

---

**Security constraints:** None defined.

**Login config:** None defined.

**Security roles:** None defined.

**Session config (lines 78–80):**
```xml
<session-config>
    <session-timeout>30</session-timeout>
</session-config>
```

**Error pages:** None defined.

**Context params:** None defined.

**Environment entries:** None defined.

**Resource references:** None defined.

**Welcome files:** None defined.

**Taglib declarations (lines 82–89):**
```xml
<taglib>
    <taglib-uri>http://jakarta.apache.org/taglibs/mailer-1.1</taglib-uri>
    <taglib-location>/WEB-INF/taglibs-mailer.tld</taglib-location>
</taglib>
<taglib>
    <taglib-uri>http://jakarta.apache.org/taglibs/request-1.0</taglib-uri>
    <taglib-location>/WEB-INF/taglibs-request.tld</taglib-location>
</taglib>
```

---

## SECTION 2 — SECURITY REVIEW CHECKLIST

### Authentication & Authorization

**Is `<auth-method>` declared?**
RESULT: No `<login-config>` or `<auth-method>` element is present in either file. Container-managed authentication is entirely absent. All servlets under `/servlet/*` are unauthenticated at the web.xml level. See finding A01-1.

**Are all sensitive URL patterns protected?**
RESULT: No `<auth-constraint>` is present in any security constraint. The single `<security-constraint>` using `CONFIDENTIAL` on `/pages/*` enforces HTTPS only, not authentication. All servlet endpoints (`/servlet/*`) are completely unprotected. The `/gps/*`, `/reports/*`, `/dyn_report/*`, and `/linde_reports/*` paths are explicitly granted `NONE` transport and have no auth-constraint. See finding A01-2 and A01-4.

**Is the `<form-login-page>` using POST? Does the action URL look correct?**
RESULT: No `<login-config>` is defined; therefore no form login page is configured. Not applicable beyond the absence itself (covered under A01-1).

**Is there an admin role defined? Is admin functionality restricted to that role?**
RESULT: No `<security-role>` elements are defined. No role-based access control is configured anywhere in web.xml. See finding A01-2.

**Check for catch-all constraints vs specific path constraints — flag gaps.**
RESULT: No catch-all constraint exists. The `/servlet/*` path is entirely unconstrained. See finding A01-2.

---

### Session Management

**Is `<session-timeout>` set? Is it > 30 minutes?**
RESULT: Session timeout is set to exactly 30 minutes in both files. For a fleet management system handling GPS tracking and driver data, 30 minutes is acceptable per the checklist threshold (flag if > 30). PASS — timeout is at the boundary, not over it.

**Is `<cookie-config>` defined with `<http-only>true</http-only>` and `<secure>true</secure>`?**
RESULT: No `<cookie-config>` element is defined in either file. Session cookies are served without `HttpOnly` or `Secure` flags enforced at the deployment descriptor level. See finding A01-3.

**Are there URL rewriting configurations that could expose JSESSIONID in URLs?**
RESULT: No explicit URL rewriting configuration is present in web.xml. However, because the file uses Servlet 3.0 schema (`web-app_3_0.xsd`), URL rewriting is typically container-default behavior (enabled unless disabled). Without `<tracking-mode>COOKIE</tracking-mode>` declared in `<session-config>`, URL-based JSESSIONID rewriting may be active depending on the container. See finding A01-3.

---

### CSRF

**Is there any CSRF filter defined in web.xml?**
RESULT: No CSRF filter is defined in web.xml. No `<filter>` element referencing any CSRF protection mechanism (e.g., Spring Security CSRF, OWASP CSRFGuard, or a custom filter) exists. See finding A01-5.

---

### Error Pages

**Are `<error-page>` entries configured for 400, 403, 404, 500?**
RESULT: No `<error-page>` elements are defined in either file. The container will serve default error pages. See finding A01-6.

**Do the error page paths reveal internal structure?**
RESULT: No error pages defined; default container error pages will typically expose stack traces and container version information. See finding A01-6.

---

### Data Exposure

**Does the welcome-file expose anything sensitive?**
RESULT: No `<welcome-file-list>` is defined. The container default (typically `index.html`, `index.jsp`) applies. PASS — no explicitly sensitive welcome file configured, though absence of explicit configuration may allow directory listing depending on container settings. No additional finding raised beyond A01-6 for error exposure.

**Are any stack-trace-exposing default error handlers present?**
RESULT: No custom error handlers defined. Default container error pages are in effect; these commonly expose stack traces, class names, and container version strings. See finding A01-6.

---

### Transport Security

**Is there any HTTPS redirect filter or security constraint forcing SSL?**
RESULT: Partial. The constraint `HTTPSOnly` enforces `CONFIDENTIAL` on `/pages/*` only. The `/servlet/*` path — which hosts all application logic including `Frm_saveuser`, `Frm_login`, and `BusinessInsight` — has no transport guarantee. The `HTTPorHTTPS` constraint explicitly sets `NONE` on `/gps/*`, `/reports/*`, `/dyn_report/*`, and `/linde_reports/*`. See finding A01-4.

**Is `<transport-guarantee>CONFIDENTIAL</transport-guarantee>` set on security constraints?**
RESULT: Set only for `/pages/*`. Not set for `/servlet/*` or any other functional path. PARTIAL — see finding A01-4.

---

### web - Copy.xml Comparison

**Does web - Copy.xml differ from web.xml in security-relevant ways?**
RESULT: Yes, in multiple significant ways:
1. web - Copy.xml uses Servlet 2.3 DTD instead of Servlet 3.0 schema.
2. web - Copy.xml contains a JavaMelody monitoring filter (`net.bull.javamelody.MonitoringFilter`) mapped to `/*` — this is absent from the production web.xml.
3. web - Copy.xml contains no security constraints at all (no HTTPS enforcement).
4. web - Copy.xml is missing 5 of the 9 servlets present in web.xml.
5. web - Copy.xml retains legacy `<taglib>` declarations not present in web.xml.

See finding A01-7.

**Could a misconfigured server accidentally deploy web - Copy.xml instead of web.xml?**
RESULT: Possibly. Some servlet containers can be configured to load a non-default descriptor filename. If deployed, it would remove all transport security constraints and activate unauthenticated application-wide monitoring exposure. See finding A01-7.

---

### Secrets

**Check all `<env-entry>` and `<resource-ref>` elements for hardcoded credentials.**
RESULT: No `<env-entry>` or `<resource-ref>` elements exist in either file. PASS.

**Check all `<context-param>` values for credentials, API keys, or passwords.**
RESULT: No `<context-param>` elements exist in either file. PASS.

---

## SECTION 3 — FINDINGS

---

### A01-1 — No Authentication Mechanism Configured

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web.xml`
**Lines:** N/A (absence finding — no `<login-config>` element anywhere in file)
**Severity:** CRITICAL
**Category:** Authentication & Authorization

**Description:**
No `<login-config>` element is defined in web.xml. This means the Java EE container has no authentication mechanism configured at the deployment descriptor level. All application resources are accessible without any container-enforced authentication challenge. For a fleet management system handling GPS tracking, driver records, vehicle data, and business intelligence, the complete absence of container-managed authentication is a critical control gap. Application-level authentication (within `Frm_login`) may exist but is not enforced by the container and can be bypassed by direct URL access to any servlet or JSP.

**Evidence:**
No `<login-config>` block present anywhere in web.xml (175 lines). Closest reference to login is:
```xml
<servlet>
    <servlet-name>Frm_login</servlet-name>
    ...
    <servlet-class>com.torrent.surat.fms6.security.Frm_login</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>Frm_login</servlet-name>
    <url-pattern>/servlet/Frm_login</url-pattern>
</servlet-mapping>
```
This is an application servlet, not a container login configuration.

**Recommendation:**
Define a `<login-config>` element specifying an appropriate `<auth-method>`. For form-based authentication, add:
```xml
<login-config>
    <auth-method>FORM</auth-method>
    <realm-name>FleetFocus</realm-name>
    <form-login-config>
        <form-login-page>/pages/login.jsp</form-login-page>
        <form-error-page>/pages/login_error.jsp</form-error-page>
    </form-login-config>
</login-config>
```
Pair this with `<security-role>` declarations and `<auth-constraint>` blocks on all protected resources. If application-level authentication is intentionally used instead of container-managed auth, document this architectural decision, ensure all servlet endpoints are protected by a mandatory authentication filter mapped to `/*`, and validate that no endpoint is reachable without a valid session.

---

### A01-2 — No Role-Based Access Control; All Servlet Endpoints Unprotected

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web.xml`
**Lines:** 136–165 (security constraints), entire file (absence of `<auth-constraint>` and `<security-role>`)
**Severity:** HIGH
**Category:** Authentication & Authorization

**Description:**
Neither security constraint in web.xml contains an `<auth-constraint>` element. No `<security-role>` declarations exist. This means:
- The entire `/servlet/*` path (9 servlets including user management, file uploads, business intelligence, GPS, and customer data) is accessible without authentication or role checks at the container level.
- The `HTTPSOnly` constraint on `/pages/*` enforces transport encryption only; it does not require any authenticated role.
- The `HTTPorHTTPS` constraint on static assets and `/gps/*`, `/reports/*`, `/dyn_report/*`, `/linde_reports/*` is transport-only with `NONE` guarantee.
- Sensitive endpoints such as `/servlet/Frm_saveuser` (user creation/modification), `/servlet/Import_Files`, `/servlet/CustomUpload`, and `/servlet/BusinessInsight` are reachable by unauthenticated requests.

**Evidence:**
```xml
<!-- Constraint 1: no <auth-constraint>, transport only -->
<security-constraint>
    <web-resource-collection>
        <web-resource-name>HTTPSOnly</web-resource-name>
        <url-pattern>/pages/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>

<!-- Constraint 2: no <auth-constraint>, NONE transport -->
<security-constraint>
    <web-resource-collection>
        <web-resource-name>HTTPorHTTPS</web-resource-name>
        <url-pattern>*.ico</url-pattern>
        <url-pattern>/img/*</url-pattern>
        <url-pattern>/js/*</url-pattern>
        <url-pattern>/css/*</url-pattern>
        <url-pattern>/skin/js/*</url-pattern>
        <url-pattern>/skin/css/*</url-pattern>
        <url-pattern>/gps/*</url-pattern>
        <url-pattern>/reports/*</url-pattern>
        <url-pattern>/dyn_report/*</url-pattern>
        <url-pattern>/linde_reports/*</url-pattern>
        <url-pattern>/includes/*</url-pattern>
        <url-pattern>/images/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>NONE</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```
No `<security-role>` element present anywhere in the 175-line file.

**Recommendation:**
Define security roles and apply auth-constraints to all sensitive URL patterns. At minimum:
```xml
<security-role>
    <role-name>user</role-name>
</security-role>
<security-role>
    <role-name>admin</role-name>
</security-role>

<security-constraint>
    <web-resource-collection>
        <web-resource-name>AllServlets</web-resource-name>
        <url-pattern>/servlet/*</url-pattern>
    </web-resource-collection>
    <auth-constraint>
        <role-name>user</role-name>
    </auth-constraint>
</security-constraint>

<security-constraint>
    <web-resource-collection>
        <web-resource-name>AdminServlets</web-resource-name>
        <url-pattern>/servlet/Frm_saveuser</url-pattern>
        <url-pattern>/servlet/Import_Files</url-pattern>
        <url-pattern>/servlet/CustomUpload</url-pattern>
    </web-resource-collection>
    <auth-constraint>
        <role-name>admin</role-name>
    </auth-constraint>
</security-constraint>
```
Apply equivalent protection to `/pages/*`, `/gps/*`, `/reports/*`, `/dyn_report/*`, and `/linde_reports/*`.

---

### A01-3 — Session Cookie Not Configured with HttpOnly or Secure Flags; URL Rewriting Not Disabled

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web.xml`
**Lines:** 131–133 (`<session-config>` block)
**Severity:** HIGH
**Category:** Session Management

**Description:**
The `<session-config>` element defines only `<session-timeout>`. It does not include a `<cookie-config>` child element, meaning:
1. The session cookie (`JSESSIONID`) is not flagged `HttpOnly` at the deployment descriptor level. Without `HttpOnly`, client-side JavaScript can read the session cookie, enabling session hijacking via XSS.
2. The session cookie is not flagged `Secure`. Without `Secure`, the cookie will be transmitted over unencrypted HTTP connections, exposing the session token in cleartext on any network path not covered by the partial HTTPS constraint.
3. No `<tracking-mode>COOKIE</tracking-mode>` is declared. Under Servlet 3.0, the container default may include URL-based session tracking, which appends `JSESSIONID` as a URL parameter. This exposes session tokens in browser history, referrer headers, proxy logs, and server access logs.

**Evidence:**
```xml
<session-config>
    <session-timeout>30</session-timeout>    <!-- 30 minutes -->
</session-config>
```
No `<cookie-config>` child element. No `<tracking-mode>` element.

**Recommendation:**
Replace the `<session-config>` block with:
```xml
<session-config>
    <session-timeout>30</session-timeout>
    <cookie-config>
        <http-only>true</http-only>
        <secure>true</secure>
        <name>FFSESSIONID</name>
    </cookie-config>
    <tracking-mode>COOKIE</tracking-mode>
</session-config>
```
Renaming the cookie from the default `JSESSIONID` to `FFSESSIONID` additionally reduces fingerprinting of the application stack. Confirm the container (Tomcat/JBoss/etc.) honours these deployment descriptor settings and does not override them in `context.xml` or server configuration.

---

### A01-4 — Sensitive Path Groups Explicitly Permitted Over HTTP; /servlet/* Has No Transport Guarantee

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web.xml`
**Lines:** 146–165 (HTTPorHTTPS constraint), 17–124 (servlet mappings with no transport constraint)
**Severity:** HIGH
**Category:** Transport Security

**Description:**
Two distinct transport security deficiencies exist:

1. The `HTTPorHTTPS` security constraint explicitly sets `<transport-guarantee>NONE</transport-guarantee>` for a set of paths that includes operationally sensitive directories: `/gps/*`, `/reports/*`, `/dyn_report/*`, and `/linde_reports/*`. These paths are not static assets — they likely serve GPS telemetry, fleet reports, and dynamic report generation. Using `NONE` ensures that requests and responses on these paths are never upgraded to HTTPS by the container.

2. All nine servlet mappings under `/servlet/*` fall outside both security constraints. No constraint references `/servlet/*` or any specific servlet URL pattern. Therefore, these endpoints — including login (`/servlet/Frm_login`), user management (`/servlet/Frm_saveuser`), file import (`/servlet/Import_Files`), and business intelligence (`/servlet/BusinessInsight`) — have no transport guarantee whatsoever. Credentials and sensitive data submitted to these endpoints can transit in cleartext.

**Evidence:**
```xml
<!-- Sensitive paths explicitly set to no transport protection -->
<security-constraint>
    <web-resource-collection>
        <web-resource-name>HTTPorHTTPS</web-resource-name>
        <url-pattern>/gps/*</url-pattern>
        <url-pattern>/reports/*</url-pattern>
        <url-pattern>/dyn_report/*</url-pattern>
        <url-pattern>/linde_reports/*</url-pattern>
        <!-- ... other static patterns ... -->
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>NONE</transport-guarantee>
    </user-data-constraint>
</security-constraint>

<!-- No constraint covers /servlet/* at all -->
<servlet-mapping>
    <servlet-name>Frm_login</servlet-name>
    <url-pattern>/servlet/Frm_login</url-pattern>
</servlet-mapping>
<servlet-mapping>
    <servlet-name>Frm_saveuser</servlet-name>
    <url-pattern>/servlet/Frm_saveuser</url-pattern>
</servlet-mapping>
```

**Recommendation:**
Add `<transport-guarantee>CONFIDENTIAL</transport-guarantee>` to all functional paths. Remove `/gps/*`, `/reports/*`, `/dyn_report/*`, and `/linde_reports/*` from the `NONE` constraint (or eliminate that constraint entirely). Add a catch-all `CONFIDENTIAL` constraint and explicitly list only genuinely non-sensitive static resources with `NONE` if truly required. At minimum, add:
```xml
<security-constraint>
    <web-resource-collection>
        <web-resource-name>AllServletsHTTPS</web-resource-name>
        <url-pattern>/servlet/*</url-pattern>
        <url-pattern>/gps/*</url-pattern>
        <url-pattern>/reports/*</url-pattern>
        <url-pattern>/dyn_report/*</url-pattern>
        <url-pattern>/linde_reports/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```

---

### A01-5 — No CSRF Filter Defined

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web.xml`
**Lines:** N/A (absence finding — no `<filter>` element of any kind in file)
**Severity:** MEDIUM
**Category:** CSRF

**Description:**
No filter is defined in web.xml. In particular, there is no CSRF protection filter (such as Spring Security's `CsrfFilter`, OWASP CSRFGuard's `CsrfGuardFilter`, or any custom filter). This means state-changing servlet requests are not protected against cross-site request forgery at the deployment descriptor level. Given the application manages user accounts (`Frm_saveuser`), file uploads (`Frm_upload`, `CustomUpload`, `Import_Files`), and fleet/GPS data modifications (`Frm_vehicle`, `Frm_customer`), successful CSRF attacks could result in unauthorized data modification, user privilege escalation, or bulk data imports.

**Evidence:**
No `<filter>` or `<filter-mapping>` element present anywhere in web.xml (175 lines).

**Recommendation:**
Integrate a CSRF protection mechanism. If the application uses Spring MVC, enable Spring Security's CSRF protection. Alternatively, implement OWASP CSRFGuard and add:
```xml
<filter>
    <filter-name>CSRFGuard</filter-name>
    <filter-class>org.owasp.csrfguard.CsrfGuardFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>CSRFGuard</filter-name>
    <url-pattern>/servlet/*</url-pattern>
</filter-mapping>
```
Ensure CSRF tokens are validated on all state-changing HTTP methods (POST, PUT, DELETE). Document in code review whether CSRF protection is implemented at the application layer and verify coverage of all sensitive endpoints.

---

### A01-6 — No Custom Error Pages Configured; Default Container Error Pages Expose Internal Detail

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web.xml`
**Lines:** N/A (absence finding — no `<error-page>` element in file)
**Severity:** MEDIUM
**Category:** Data Exposure

**Description:**
No `<error-page>` elements are defined for HTTP error codes (400, 403, 404, 500) or Java exception types. The container default error pages (Tomcat/JBoss/etc.) typically display:
- Full Java stack traces including class names, method names, and line numbers
- Container version and build information
- Internal file system path fragments
- SQL error messages when database exceptions propagate

For a fleet management system, this information is directly useful to an attacker for mapping the application structure, identifying vulnerable components, and crafting targeted exploits.

**Evidence:**
No `<error-page>` block present anywhere in web.xml (175 lines).

**Recommendation:**
Add custom error pages for all standard error codes:
```xml
<error-page>
    <error-code>400</error-code>
    <location>/pages/error/400.jsp</location>
</error-page>
<error-page>
    <error-code>403</error-code>
    <location>/pages/error/403.jsp</location>
</error-page>
<error-page>
    <error-code>404</error-code>
    <location>/pages/error/404.jsp</location>
</error-page>
<error-page>
    <error-code>500</error-code>
    <location>/pages/error/500.jsp</location>
</error-page>
<error-page>
    <exception-type>java.lang.Exception</exception-type>
    <location>/pages/error/general.jsp</location>
</error-page>
```
Ensure that error pages do not themselves render stack trace information. Configure the container (e.g., Tomcat's `server.xml` or `context.xml`) to suppress `showReport` and `showServerInfo` in addition to web.xml error page declarations.

---

### A01-7 — Stale Backup Descriptor (web - Copy.xml) Present in WEB-INF; Contains Unauthenticated Monitoring Filter Mapped to All URLs

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\web - Copy.xml`
**Lines:** 7–17 (monitoring filter and listener), 1–6 (schema declaration), entire file
**Severity:** HIGH
**Category:** Data Exposure / Configuration Management

**Description:**
A stale backup of web.xml, named `web - Copy.xml`, exists in the `WEB-INF` directory. This file is security-relevant for three distinct reasons:

**Reason 1 — Presence of backup in deployment directory:**
Backup and copy files in `WEB-INF` represent a configuration management failure. If any mechanism causes this file to be loaded as the active deployment descriptor (misconfigured application server, automated deployment script error, manual deployment mistake), the production application would run with no security constraints at all and with an unauthenticated monitoring endpoint active.

**Reason 2 — JavaMelody monitoring filter mapped to `/*` with no authentication:**
`web - Copy.xml` contains a `net.bull.javamelody.MonitoringFilter` mapped to every URL (`/*`). JavaMelody exposes a monitoring dashboard (typically at `/monitoring`) that reveals heap dumps, thread states, SQL query details, HTTP request counts, session counts, active users, and system metrics. This filter is absent from `web.xml`. If this file were deployed, the monitoring endpoint would be accessible to unauthenticated users across all URLs.

**Reason 3 — Servlet 2.3 DTD vs Servlet 3.0 schema:**
`web - Copy.xml` declares the older Servlet 2.3 DTD. If deployed on a Servlet 3.0+ container, behaviour differences (particularly around session tracking modes and cookie security attributes) could produce unpredictable results compared to the production descriptor.

**Evidence:**
```xml
<!-- web - Copy.xml lines 3-5: older DTD -->
<!DOCTYPE web-app
    PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
    "http://java.sun.com/dtd/web-app_2_3.dtd">

<!-- web - Copy.xml lines 7-17: unauthenticated monitoring filter on all URLs -->
<filter>
    <filter-name>monitoring</filter-name>
    <filter-class>net.bull.javamelody.MonitoringFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>monitoring</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
<listener>
    <listener-class>net.bull.javamelody.SessionListener</listener-class>
</listener>
```
`web - Copy.xml` contains zero `<security-constraint>` elements (entire 92-line file reviewed).

**Recommendation:**
1. Delete `web - Copy.xml` from `WEB-INF` immediately. Backup files must not reside in any deployed application directory.
2. If JavaMelody monitoring is required in production, add it to the active `web.xml` with access restricted to an administrative role and HTTPS enforced:
```xml
<security-constraint>
    <web-resource-collection>
        <web-resource-name>MonitoringOnly</web-resource-name>
        <url-pattern>/monitoring</url-pattern>
    </web-resource-collection>
    <auth-constraint>
        <role-name>admin</role-name>
    </auth-constraint>
    <user-data-constraint>
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```
3. Audit the deployment pipeline to ensure only `web.xml` is loaded as the active descriptor and that no wildcard file selection can accidentally pick up backup files.

---

## SECTION 4 — FINDINGS SUMMARY

| ID     | Severity | Category                        | File                | Summary                                                              |
|--------|----------|---------------------------------|---------------------|----------------------------------------------------------------------|
| A01-1  | CRITICAL | Authentication & Authorization  | web.xml             | No `<login-config>` — no container-managed authentication defined    |
| A01-2  | HIGH     | Authentication & Authorization  | web.xml             | No `<auth-constraint>` or `<security-role>` — all endpoints open     |
| A01-3  | HIGH     | Session Management              | web.xml             | No `<cookie-config>` — JSESSIONID lacks HttpOnly, Secure, no COOKIE tracking-mode |
| A01-4  | HIGH     | Transport Security              | web.xml             | `/servlet/*` unconstrained; `/gps/*`, `/reports/*` etc. explicitly NONE |
| A01-5  | MEDIUM   | CSRF                            | web.xml             | No CSRF filter defined                                               |
| A01-6  | MEDIUM   | Data Exposure                   | web.xml             | No custom error pages — default pages expose stack traces            |
| A01-7  | HIGH     | Data Exposure / Config Mgmt     | web - Copy.xml      | Stale backup with unauthenticated JavaMelody monitoring filter on `/*` |

**Total findings: 7**
(1 CRITICAL, 4 HIGH, 2 MEDIUM, 0 LOW, 0 INFO)
