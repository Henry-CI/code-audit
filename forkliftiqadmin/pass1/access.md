# A01 — access.jsp
**Path:** src/main/webapp/html-jsp/vehicle/access.jsp
**Auditor:** A01
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### File path
`src/main/webapp/html-jsp/vehicle/access.jsp`

### HTML form tags
None — no plain `<form>` HTML tags present.

### Struts form tags (`<html:form>`)
| Tag | action | method |
|-----|--------|--------|
| `<html:form>` (line 35) | `adminunitaccess.do` | `post` |

### Scriptlet blocks (`<% ... %>`)
**Lines 3–12** — Reads `request.getParameter("id")`. If `id` is non-empty, builds URL string `urlGeneral = "adminunit.do?action=edit&equipId=" + id`. If empty, sets `urlGeneral = "adminunit.do?action=add"`. The value is not sanitised or encoded before being used in expression outputs on lines 18 and 27.

### Expression outputs (`<%= ... %>` and `${...}`)
| Line | Expression | Context | Notes |
|------|-----------|---------|-------|
| 18 | `<%=urlGeneral %>` | Inside `href="..."` attribute of `<a>` tag | Derived from unescaped `request.getParameter("id")` — XSS sink in href |
| 19 | `<%=id %>` | Inside `href="..."` attribute of `<a>` tag | Directly from unescaped `request.getParameter("id")` — XSS sink in href |
| 20 | `<%=id %>` | Inside `href="..."` attribute of `<a>` tag | Same as above |
| 21 | `<%=id %>` | Inside `href="..."` attribute of `<a>` tag | Same as above |
| 22 | `<%=id %>` | Inside `href="..."` attribute of `<a>` tag | Same as above |
| 27 | `<%=urlGeneral %>` | Inside `href="..."` attribute of `<a>` tag | Derived from unescaped `request.getParameter("id")` — XSS sink in href |
| 28 | `<%=id %>` | Inside `href="..."` attribute of `<a>` tag | Same as above |
| 29 | `<%=id %>` | Inside `href="..."` attribute of `<a>` tag | Same as above |
| 30 | `<%=id %>` | Inside `href="..."` attribute of `<a>` tag | Same as above |

### `<%@ include %>` / `<jsp:include>` / `<c:import>`
| Directive | Path |
|-----------|------|
| `<%@ include file="../../includes/importLib.jsp" %>` (line 1) | `/includes/importLib.jsp` — imports Struts tag libraries and Java classes; no authentication logic. |

The page is rendered inside the `UnitAccessDefinition` Tiles definition (`tiles-defs.xml` line 105–108), which uses `loginDefinition` as its base template and `header_pop.inc.jsp` as its header. The header file contains only CSS styling — it performs no session check.

### `request.getParameter()` / `request.getAttribute()` / session access in scriptlets
| Line | Call | Notes |
|------|------|-------|
| 4 | `request.getParameter("id")` | Not validated, not encoded. Used to build navigation URLs and output raw into href attributes. |

### Struts bean / logic tags that read request/session scope
| Line | Tag | Attribute | Notes |
|------|-----|-----------|-------|
| 16 | `<logic:equal value="true" name="isDealer">` | `name="isDealer"` | Reads a session/request bean named `isDealer`; controls whether a fifth tab (Assignment) is shown. |

### URLs constructed or output to the page
- Line 8: `"adminunit.do?action=edit&equipId=" + id` — `id` is unescaped user input appended to a URL.
- Line 10: `"adminunit.do?action=add"` — static, no issue.
- Lines 18, 27: `<%=urlGeneral %>` — the constructed URL containing raw `id` is written into `href` attributes.
- Lines 19–22, 28–30: `<%=id %>` — raw `id` is written into `href` attributes.

### Form fields rendered by Struts HTML tags (lines 49–101)
All form fields (`html:checkbox`, `html:select`, `html:text`, `html:hidden`) are rendered by Struts 1.x HTML tags, which HTML-encode their output by default. No `bean:write filter="false"` usage found.

---

## Findings

### FINDING 1 — REFLECTED XSS VIA UNENCODED `id` PARAMETER IN HREF ATTRIBUTES
**Severity:** HIGH

**Description:**
The JSP reads `request.getParameter("id")` at line 4 and stores the raw value in local variables `id` and `urlGeneral` without HTML-encoding or URL-encoding. These are then written directly into multiple `href` attribute values at lines 18–22 and 27–30 using `<%= %>` scriptlet expressions.

A value such as `"><script>alert(1)</script>` or `javascript:alert(1)` supplied as the `id` query parameter will be written verbatim into the rendered HTML, allowing JavaScript execution in the victim's browser. Because this page is reached via `adminunitaccess.do?id=<value>`, an attacker can craft a link and trick an authenticated admin into clicking it.

**File and lines:**
`src/main/webapp/html-jsp/vehicle/access.jsp` — lines 4, 8, 18, 19, 20, 21, 22, 27, 28, 29, 30

**Evidence:**
```jsp
// Line 4
String id = request.getParameter("id") == null ? "" : request.getParameter("id");

// Line 8
urlGeneral = "adminunit.do?action=edit&equipId=" + id;

// Line 18 — raw urlGeneral written into href
<li><a href="<%=urlGeneral %>" class="general_u_tab">General</a></li>

// Line 19 — raw id written into href
<li><a href="adminunit.do?action=service&equipId=<%=id %>" id="service_tab">Service</a></li>

// Lines 20–22 (repeated pattern)
<li class="active"><a href="adminunitaccess.do?id=<%=id %>" id="access_tab">Access</a></li>
<li><a href="adminunit.do?action=impact&equipId=<%=id %>" id="impact_tab">Impact</a></li>
<li><a href="adminunit.do?action=assignment&equipId=<%=id %>" id="assignment_tab">Assignment</a></li>
```

**Recommendation:**
Encode all user-supplied values before outputting them into HTML. For URL query-parameter context, apply `java.net.URLEncoder.encode(id, "UTF-8")`. For HTML attribute context, apply OWASP Java Encoder `Encode.forHtmlAttribute(id)` or use `<c:out value="${param.id}"/>` (JSTL). Replace all nine raw `<%= id %>` and `<%= urlGeneral %>` occurrences with properly encoded equivalents. The `id` value should also be validated as a numeric integer (it is a database primary key) and rejected with an error response if it is not.

---

### FINDING 2 — INSECURE DIRECT OBJECT REFERENCE (IDOR): UNIT DATA FETCHED WITHOUT OWNERSHIP CHECK
**Severity:** HIGH

**Description:**
When the `adminunitaccess.do` action is invoked without `action=save`, the handler in `AdminUnitAccessAction.java` (line 29) calls `UnitDAO.getUnitById(accessForm.getId())`. This fetches a unit record from the database using only the `id` form field, with no verification that the unit belongs to the authenticated user's company.

The session company ID (`sessCompId`) is present in the action and is used only to load the full unit list for display (`UnitDAO.getAllUnitsByCompanyId(companyId)` at line 33). It is never used to scope the `getUnitById` lookup.

Similarly, the `save` path at line 26 calls `accessForm.getUnit(sessCompId)`, which passes `sessCompId` to `UnitBean`, but `UnitDAO.saveUnitAccessInfo()` issues `UPDATE unit SET ... WHERE id = ?` with only the unit primary key from the form field — there is no `AND comp_id = ?` predicate. An authenticated user of company A can therefore update access control settings (card type, PIN mode, access ID, facility code, keypad reader) for a unit belonging to company B by manipulating the `id` hidden field in the form.

**Files and lines:**
- `src/main/webapp/html-jsp/vehicle/access.jsp` line 100: `<html:hidden property="id"/>` — `id` comes from the form bean, which is populated from the request.
- `src/main/java/com/action/AdminUnitAccessAction.java` lines 19, 26, 29: session company ID is not used to scope the unit lookup or the save.
- `src/main/java/com/dao/UnitDAO.java` line 514–527: `UPDATE_UNIT_ACCESS` has no `comp_id` predicate.
- `src/main/java/com/querybuilder/unit/UnitsByIdQuery.java` line 14: `SELECT * FROM v_units WHERE id = ?` has no `comp_id` predicate.

**Evidence:**
```java
// AdminUnitAccessAction.java lines 19, 26, 29
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
...
if ("save".equalsIgnoreCase(action)) {
    UnitBean unitBean = accessForm.getUnit(sessCompId); // sessCompId passed to bean but not used in WHERE clause
    UnitDAO.saveUnitAccessInfo(unitBean);               // UPDATE uses only id, no comp_id check
} else {
    UnitBean unitBean = UnitDAO.getUnitById(accessForm.getId()).get(0); // no company scope
    accessForm.setUnit(unitBean);
}

// UnitDAO.java lines 513–527
private static final String UPDATE_UNIT_ACCESS =
    "update unit set accessible = ?, access_type = ?, access_id = ?, keypad_reader = ?, facility_code = ? " +
    "where id= ?";   // <-- no AND comp_id = ? predicate

// UnitsByIdQuery.java line 14
private static final String query = "SELECT * FROM v_units WHERE id = ?"; // no comp_id constraint
```

**Recommendation:**
Add `AND comp_id = ?` to both the `SELECT` (in `UnitsByIdQuery`) and the `UPDATE_UNIT_ACCESS` statement in `UnitDAO`. In `AdminUnitAccessAction`, pass `companyId` as a parameter to `UnitDAO.getUnitById()` and `UnitDAO.saveUnitAccessInfo()`. Verify the result set is non-empty after filtering by company before proceeding; return an authorisation error if the unit does not belong to the session company.

---

### FINDING 3 — NO CSRF PROTECTION ON STATE-CHANGING FORM
**Severity:** MEDIUM

**Description:**
The `<html:form>` submits a POST to `adminunitaccess.do` and modifies access control settings (card/PIN configuration, access ID, facility code) for a forklift unit. There is no CSRF token in the form and no CSRF mitigation evident anywhere in the application — `web.xml` defines no CSRF filter, `struts-config.xml` includes no CSRF plug-in, and Struts 1.x does not provide CSRF protection by default.

An attacker who can cause an authenticated admin to load a malicious page can forge a cross-site POST to `adminunitaccess.do` with an arbitrary `id` and access control values, silently altering forklift access settings.

**Files and lines:**
`src/main/webapp/html-jsp/vehicle/access.jsp` lines 35–102; `src/main/webapp/WEB-INF/web.xml` (no CSRF filter defined).

**Evidence:**
```jsp
<html:form method="post" action="adminunitaccess.do" styleClass="ajax_mode_c"
           styleId="adminUnitEditFormAccess">
    ...
    <!-- No CSRF token field -->
    <html:hidden property="id"/>
    <html:hidden property="action" value="save"/>
</html:form>
```

**Recommendation:**
Implement a synchroniser token pattern. Generate a cryptographically random token per session (or per form render), store it in the session, include it as a hidden field in the form, and validate it server-side in `AdminUnitAccessAction` before processing any state-changing operation. Alternatively, adopt a CSRF filter library (e.g., OWASP CSRFGuard) applied at the servlet filter layer.

---

### FINDING 4 — AUTHENTICATION CHECK APPLIES TO GET ONLY; NO ROLE AUTHORISATION
**Severity:** MEDIUM

**Description:**
Authentication is enforced by `PreFlightActionServlet.doGet()`, which checks for a non-null, non-empty `sessCompId` session attribute before delegating to the Struts action. However, this check is in `doGet()` and `doPost()` calls `doGet()` in turn, so the session check does apply to both verbs.

The key concern is that the check confirms only that some `sessCompId` is set — it does not verify the user's role. `forkliftiqadmin` is an admin application. There is no check anywhere in the `adminunitaccess.do` flow (in the action, the form, or the JSP) that the authenticated session belongs to an admin-level user rather than a lower-privileged user who happens to have a session. If any authenticated session is sufficient to reach this endpoint, then a low-privileged authenticated user could update forklift access control settings.

**Files and lines:**
`src/main/java/com/actionservlet/PreFlightActionServlet.java` lines 56–60; `src/main/java/com/action/AdminUnitAccessAction.java` lines 17–37 (no role check).

**Evidence:**
```java
// PreFlightActionServlet.java
else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
// No role check — any user with a sessCompId can reach any *.do action.

// AdminUnitAccessAction.java — no role check present
public ActionForward execute(...) throws Exception {
    HttpSession session = request.getSession(false);
    String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
    // ... directly proceeds to data access
}
```

**Recommendation:**
Implement role-based authorisation. Determine the authenticated user's role from the session (e.g., a `sessRole` or `sessIsAdmin` attribute set at login), and explicitly check that the role is sufficient to modify unit access settings before proceeding. Reject with an HTTP 403 or redirect to an error page if the check fails.

---

### FINDING 5 — SESSION ESTABLISHED WITH `request.getSession(false)`; NPE RISK IF SESSION IS NULL
**Severity:** LOW

**Description:**
`AdminUnitAccessAction.execute()` calls `request.getSession(false)` (line 18), which returns `null` if no session exists. The very next line immediately dereferences the returned value with `session.getAttribute("sessCompId")`. If a request somehow reaches this action without a session — for example, if the `excludeFromFilter` logic in `PreFlightActionServlet` had a matching edge case, or if the session expired between the filter check and action execution — a `NullPointerException` would be thrown, caught by the global exception handler, and the user would be forwarded to the error page. This is low severity given the session filter guard, but the pattern is fragile.

**File and line:**
`src/main/java/com/action/AdminUnitAccessAction.java` lines 18–19.

**Evidence:**
```java
HttpSession session = request.getSession(false);  // can return null
String sessCompId = session.getAttribute("sessCompId") == null ? "" : ...;  // NPE if session is null
```

**Recommendation:**
Add a null check on `session` and redirect to the login/expire page explicitly if it is null, rather than relying on the exception handler.

---

### FINDING 6 — `isDealer` SESSION ATTRIBUTE CONTROLS TAB RENDERING WITHOUT AUTHORISATION ENFORCEMENT
**Severity:** LOW

**Description:**
The JSP uses `<logic:equal value="true" name="isDealer">` (lines 16 and 25) to decide whether to render the "Assignment" tab, which links to `adminunit.do?action=assignment`. This flag controls a UI element only. It does not constitute an authorisation check — a user who manually navigates to `adminunit.do?action=assignment&equipId=<id>` will reach the assignment functionality regardless of the `isDealer` flag, assuming the session is valid. While this specific JSP is not itself the vulnerability, it highlights a pattern of UI-based access control that may be relied upon elsewhere.

**File and lines:**
`src/main/webapp/html-jsp/vehicle/access.jsp` lines 16–24.

**Evidence:**
```jsp
<logic:equal value="true" name="isDealer">
    <ul class="modal-content-tab admin_unit clearfix five">
        ...
        <li><a href="adminunit.do?action=assignment&equipId=<%=id %>" id="assignment_tab">Assignment</a></li>
    </ul>
</logic:equal>
```

**Recommendation:**
Verify that the `adminunit.do?action=assignment` endpoint enforces the dealer-role check server-side in its action class, independently of whether the tab is visible in the UI.

---

## Checklist Coverage

### 1. Secrets and Configuration
Not applicable to this JSP. The file contains no hardcoded credentials, API keys, database URLs, or internal service paths. The only string literals are static UI label values and fixed Struts action paths.

### 2. Authentication and Authorization
**Issues found.**
- FINDING 3 (MEDIUM): Authentication is enforced by `PreFlightActionServlet` checking for a non-null `sessCompId`. The `adminunitaccess.do` action is not in the `excludeFromFilter` exemption list, so it is covered by the session check.
- FINDING 4 (MEDIUM): No role-based authorisation check is performed. Any authenticated session can invoke this action.
- FINDING 2 (HIGH): IDOR — the unit looked up and modified is not verified to belong to the authenticated session's company.

### 3. Input Validation and Injection
**Issues found.**
- FINDING 1 (HIGH): Reflected XSS — `request.getParameter("id")` is output unencoded into nine `href` attributes.
- SQL injection: Not present in the access-specific query path. `UnitsByIdQuery` (used on load) uses a parameterised `PreparedStatement` with a `?` placeholder. `UPDATE_UNIT_ACCESS` (used on save) is a fully parameterised prepared statement. No string concatenation of user input into SQL is present in the direct access flow. Note: other methods in `UnitDAO` (e.g., `getUnitBySerial`, `delUnitById`, `getType`, `getPower`) use string concatenation and are vulnerable to SQL injection, but they are not invoked by the `adminunitaccess.do` flow.
- No command injection, path traversal, XXE, or SSRF identified in this file or its direct action/DAO path.

### 4. Session and CSRF
**Issues found.**
- FINDING 3 (MEDIUM): No CSRF token on the state-changing POST form.
- Session fixation, cookie flags (`Secure`, `HttpOnly`, `SameSite`), and `X-Frame-Options`/`X-Content-Type-Options` headers are not set in `web.xml` and no evidence of them in the JSP. This is a broader application-level concern not unique to this file; flagged for awareness.

### 5. Data Exposure
**Issue found (FINDING 2).**
The load path fetches and populates the form with unit access settings (access type, access ID, facility code, keypad reader model) for any unit ID without scoping to the authenticated company. An attacker could read access control configuration for units belonging to other organisations.

No stack traces or SQL error messages are rendered in this JSP itself; the global exception handler forwards to `/error/error.html`.

### 6. Dependencies
Not applicable to this JSP file. Dependency review must be performed against `pom.xml`.

### 7. Build and CI
Not applicable to this JSP file.
