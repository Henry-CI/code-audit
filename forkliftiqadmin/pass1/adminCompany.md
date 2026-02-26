# A09 — adminCompany.jsp

**Path:** src/main/webapp/html-jsp/adminCompany.jsp
**Auditor:** A09
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### File: src/main/webapp/html-jsp/adminCompany.jsp

**Includes / imports (line 1):**
- `<%@ include file="../includes/importLib.jsp" %>` — static include that pulls in Struts tag libraries (`struts-html`, `struts-bean`, `struts-logic`) and Java imports (`Iterator`, `ArrayList`, `RuntimeConf`, `InfoLogger`, `Calendar`, `Cookie`, `Logger`).

**Form tags:**

| Line | Action | Method | Name / ID |
|------|--------|--------|-----------|
| 17 | `dealercompanies.do` | `post` | `adminRegActionForm` / `adminRegActionForm` |

The form has no hidden CSRF token field and carries no `action` parameter; it submits to the `dealercompanies.do` mapping.

**Scriptlets:** None. The JSP contains no `<% ... %>` scriptlet blocks.

**Expression outputs `<%= %>` / `${...}`:** None.

**`<bean:write>` outputs (unescaped by default in Struts 1.x when `filter` attribute is omitted):**

| Line | Bean name | Property | `filter` attribute present? |
|------|-----------|----------|---------------------------|
| 46 | `companyRecord` | `name` | No |
| 47 | `companyRecord` | `address` | No |

In Struts 1.x the `<bean:write>` tag defaults to `filter="true"`, which encodes `<`, `>`, `"`, `&`, and `'` as HTML entities. Neither instance explicitly sets `filter="false"`, so the default HTML-encoding path is taken. However, because `filter` is not explicitly declared, this is a read-evidence item requiring verification of the Struts version TLD behaviour in deployment.

**`<logic:iterate>` / `<logic:notEmpty>`:**

| Line | Attribute name | Scope | Type |
|------|----------------|-------|------|
| 43 | `subCompanyLst` | implicit (request) | — |
| 44 | `subCompanyLst` | — | `com.bean.CompanyBean` |

**URL built in JSP:**
- Line 20: `dealercompanies.do?action=add` — hardcoded, no user input.
- Line 5: `adminmenu.do?action=home` — hardcoded.
- Line 6: `dealercompanies.do` — hardcoded.

**Hidden fields:** None.

**`request.getParameter` / session access in JSP:** None directly. Data arrives via request attributes set by the Action class.

---

### Action class: com.action.DealerCompaniesAction

**File:** src/main/java/com/action/DealerCompaniesAction.java
**Extends:** `org.apache.struts.action.Action`
**Method:** `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)`

**Session reads:**
- `session.getAttribute("sessCompId")` — line 26, used directly as the company ID parameter passed to `CompanyDAO.getSubCompanies(companyId)`.
- `session.getAttribute("isDealer")` — line 34, echoed as a request attribute.

**Request parameter reads:**
- `request.getParameter("action")` — line 25, controls branch: `"add"` vs list.

**Request attributes set:**
- `"subCompanyLst"` — set to `CompanyDAO.getSubCompanies(companyId)` (line 35), a `List<CompanyBean>` whose `name` and `address` are rendered in the JSP.
- `"isDealer"` — set from session attribute (line 34).
- `"companyRecord"` — on the `add` branch, a single empty `CompanyBean` (line 31).

**No explicit null-check before `.toString()` call:** Line 26 calls `session.getAttribute("sessCompId").toString()` with no null guard. If `sessCompId` is somehow absent the action throws a `NullPointerException`. The `PreFlightActionServlet` is intended to prevent this but the in-action guard is absent.

---

### Supporting class: com.dao.CompanyDAO

**Relevant method: `getSubCompanies(String companyId)` (line 177)**

```java
private static final String QUERY_SUBCOMPANYLST_BY_ID =
    "select c.id, c.name, c.address, ... from company as c " +
    " left outer join company_rel as r on r.company_id = c.id " +
    " where r.parent_company_id = ?";

return DBUtil.queryForObjects(QUERY_SUBCOMPANYLST_BY_ID,
    stmt -> stmt.setLong(1, Long.parseLong(companyId)),
    ...);
```

Uses a parameterised prepared statement. The `companyId` value comes from the session (`sessCompId`), not from user-supplied request input. SQL injection is not present in this method.

**SQL injection present elsewhere in CompanyDAO (in scope because the same DAO backs this page's data layer):**

- `checkExist` (line 357): string concatenation — `"select id from company where " + dbField + " ='" + name + "'"`. Both `name` and `dbField` are caller-controlled strings. `checkExist` is not called on the list path of this page, but its presence in the same DAO class is a systemic risk.
- `checkUserExit` (line 382): same pattern.
- `checkCompExist` (line 396): `name` and `email` from `CompanyBean` are directly concatenated into SQL.
- `getCompLogo` (line 461): `"select logo from company where id = " + compId + ""` — companyId concatenated directly.
- `getEntityComp` (line 655): `entityId` concatenated when not equal to `"1"`.
- `getEntityByQuestion` (line 690): `qId` and `type` both concatenated.
- `getAllEntity` (line 722): entity `id` from first result set is concatenated into second query on line 745.

These are not triggered directly by the adminCompany.jsp list flow, but are noted because they are in the same DAO that services the company management subsystem.

---

### Session and auth gate: com.actionservlet.PreFlightActionServlet

- `doPost` delegates to `doGet` (line 95).
- `doGet` calls `excludeFromFilter(path)` (line 98–115).
- `dealercompanies.do` is not in the exclusion list, so `excludeFromFilter` returns `true`.
- When `excludeFromFilter` returns `true`, the servlet checks: (a) session is null, or (b) `sessCompId` is null or empty — if either, forward to `EXPIRE_PAGE`.
- No role check is performed. Any authenticated user with a valid `sessCompId` — regardless of authority — can reach this page.

**Role constants (RuntimeConf):**
- `ROLE_SYSADMIN = "ROLE_SYS_ADMIN"`
- `ROLE_DEALER = "ROLE_DEALER"`
- `ROLE_COMP = "ROLE_COMPANY_GROUP"`
- `ROLE_SUBCOMP = "ROLE_SUBCOMP"`
- `ROLE_SITEADMIN = "ROLE_SITE_ADMIN"`

---

### Tiles definition

`dealerCompaniesDefinition` extends `adminDefinition` (tiles-defs.xml line 176–178), meaning the page renders within the standard admin chrome (header, navigation, footer). The `dealerCompaniesAddDefinition` uses the popup/lightbox template.

---

### web.xml observations

- Session timeout: 30 minutes (line 46).
- No `<security-constraint>` elements present — declarative Java EE container security is not used.
- No `secure` or `HttpOnly` cookie configuration in web.xml (Servlet 2.4 schema does not have `<cookie-config>`).
- Error page maps `java.lang.Exception` to `/error/error.html` (line 52–54) — a static HTML page, which limits stack trace leakage at the container level.
- Servlet class is `com.actionservlet.PreFlightActionServlet`, which extends Struts `ActionServlet` and adds the session/`sessCompId` pre-flight check only.

---

## Findings

### FINDING-01: No CSRF token on the POST form (MEDIUM)

**Location:** adminCompany.jsp line 17; struts-config.xml `/dealercompanies` action.

The form at line 17 submits via HTTP POST to `dealercompanies.do`. There is no CSRF token — no hidden field, no Struts token check, no SynchronizerToken pattern. Struts 1.x has a built-in token mechanism (`saveToken` / `isTokenValid`) but it is not used here or in `DealerCompaniesAction`.

The form body as rendered is an empty POST — clicking the form submit button has no visible effect on the list view (the list action simply re-queries and renders). However, the same `dealercompanies.do` endpoint is also the target for the inline `adminRegRegisterAction` form name (`adminRegActionForm`), and the `adminRegister.do` mapping (which accepts POST to create/update companies) also uses the same `adminRegActionForm` form name. An adversary who can induce an admin user to click a crafted link could trigger state-changing requests against the company management endpoints.

More critically: the `/adminRegister` action (struts-config.xml line 145–157) which creates and updates company records also lacks CSRF protection and is reached via POST from various forms sharing this form-bean name.

**Risk:** A CSRF attack could cause an authenticated dealer or site-admin user to unknowingly create or modify sub-company records.

---

### FINDING-02: No role-based access control on the company list endpoint (HIGH)

**Location:** com.actionservlet.PreFlightActionServlet lines 48–65; com.action.DealerCompaniesAction lines 23–38.

The `PreFlightActionServlet` gate checks only that (a) a session exists and (b) `sessCompId` is not null/empty. It does not verify the authority (`ROLE_DEALER`, `ROLE_SYS_ADMIN`, etc.) of the authenticated company or user.

`DealerCompaniesAction.execute()` performs no role check of its own. Any authenticated session holder — including a `ROLE_SUBCOMP` (sub-company) user or a `ROLE_SITE_ADMIN` — can GET `dealercompanies.do` and receive the sub-company list for whatever `sessCompId` is in their session.

The page is described by the navigation as the "Locations" / Dealer Companies view, implying it is intended for dealer-level or super-admin users only. There is no `LoginDAO.isAuthority` or equivalent guard in the action.

**Risk:** A site-admin user whose company has sub-companies can enumerate all sub-company names and addresses. A ROLE_SUBCOMP user whose `sessCompId` happens to be set to a parent company ID can enumerate sibling companies.

---

### FINDING-03: Implicit XSS risk — `bean:write` `filter` attribute not explicitly set (LOW / informational)

**Location:** adminCompany.jsp lines 46–47.

```jsp
<bean:write property="name" name="companyRecord"/>
<bean:write property="address" name="companyRecord"/>
```

The `filter` attribute is not specified. In Struts 1.x the default value of `filter` is `true`, which causes the tag to HTML-encode the output (replacing `<`, `>`, `"`, `&`). Provided the deployed Struts 1.3 TLD preserves this default, stored XSS from company `name` or `address` fields is prevented.

However, this is a passive defence relying on framework default behaviour that is not explicitly declared. If a future developer adds `filter="false"` for formatting purposes, or if the tag library version changes the default, stored XSS would be introduced. Company `name` and `address` are admin-entered strings that could contain `<script>` content stored in the database.

**Risk (current):** Likely not exploitable given the default. Risk becomes HIGH if `filter="false"` is ever added.

**Recommendation (report only):** Add `filter="true"` explicitly to both `<bean:write>` tags as a defence-in-depth declaration.

---

### FINDING-04: NullPointerException risk — unguarded `.toString()` on session attribute (LOW)

**Location:** com.action.DealerCompaniesAction line 26.

```java
String companyId = session.getAttribute("sessCompId").toString();
```

`session.getAttribute("sessCompId")` can return `null` if the session attribute was never set or was invalidated between the pre-flight check and the action execution (a race condition or programmatic session manipulation). Calling `.toString()` on a null reference throws a `NullPointerException`.

The `PreFlightActionServlet` attempts to prevent this by checking `sessCompId == null` before forwarding to the action, but the check is in `doGet`/`doPost` of the servlet, not in the action itself. If `session.getAttribute("sessCompId")` returns null, the global exception handler forwards to `/error/error.html`, which leaks no stack trace to the browser, but the unhandled NPE still propagates through the Struts exception handler as a `java.lang.NullPointerException` and is logged.

---

### FINDING-05: SQL injection in CompanyDAO methods callable from company-management flows (HIGH — DAO level)

**Location:** com.dao.CompanyDAO

While the `getSubCompanies` method used by the list path of this page is safe (parameterised), the same DAO class contains multiple SQL-injection-vulnerable methods:

- `checkExist` (line 357–379): `dbField` and `name` concatenated.
- `checkUserExit` (line 382–393): `dbField` and `name` concatenated.
- `checkCompExist` (line 396–433): `name`, `email`, `question`, `answer` from `CompanyBean` concatenated.
- `getCompLogo` (line 461–486): `compId` concatenated into `WHERE id = ` without a prepared statement.
- `getEntityComp` (line 655–688): `entityId` concatenated when not `"1"`.
- `getEntityByQuestion` (line 690–719): `qId` and `type` concatenated.
- `getAllEntity` (line 722–768): a value from the first result set is concatenated into a second query (second-order injection risk).

These methods are invoked from other action flows in the company management subsystem (e.g., `AdminRegisterAction`, registration validation). They are noted here because they share the same DAO and data scope as the adminCompany.jsp page.

---

### FINDING-06: Data scoping relies solely on session `sessCompId` with no server-side verification (MEDIUM — IDOR)

**Location:** com.action.DealerCompaniesAction line 26–35; com.dao.CompanyDAO.getSubCompanies.

The company ID used to query sub-companies is read directly from the session attribute `sessCompId`. There is no verification that the company identified by `sessCompId` is actually authorised to view the sub-company list (e.g., that it holds `ROLE_DEALER`). The data scoping is: "show all companies whose `parent_company_id` = `sessCompId`".

If an attacker can manipulate `sessCompId` (e.g., via a session fixation attack, or if `sessCompId` is set from a request parameter elsewhere), they can enumerate sub-companies for any parent company ID.

Additionally, the `SwitchCompanyAction` allows an authenticated user to switch to a different `sessCompId` from the `sessArrComp` list set at login. If the list of switchable companies is not tightly scoped at login time, a user could switch to an unintended parent company and retrieve its sub-company list.

---

### FINDING-07: No security headers set at application level (MEDIUM)

**Location:** web.xml; PreFlightActionServlet.

The `web.xml` declares no `<security-constraint>`, no filter that sets `X-Frame-Options`, `X-Content-Type-Options`, or `Strict-Transport-Security` response headers. The `PreFlightActionServlet` does not set these headers either. This exposes all pages in the admin application — including adminCompany.jsp — to clickjacking and MIME-sniffing attacks.

---

### FINDING-08: Session cookie configuration not hardened (MEDIUM)

**Location:** web.xml.

The `web.xml` uses the Servlet 2.4 schema, which does not support `<cookie-config>` (introduced in Servlet 3.0). There is no programmatic `HttpOnly` or `Secure` flag set on the session cookie anywhere in the codebase visible from this file's call chain. Without `HttpOnly`, the session cookie is accessible to JavaScript, making it vulnerable to exfiltration via XSS. Without `Secure`, the cookie may be transmitted over plain HTTP.

---

## Checklist Coverage

| # | Checklist item | Status | Notes |
|---|---------------|--------|-------|
| 1 | Secrets / hardcoded credentials in config files | Not applicable to this JSP | See pass0 for secrets audit |
| 2a | Authentication required for this endpoint | Pass (with caveat) | PreFlightActionServlet checks sessCompId; session-timeout is 30 min |
| 2b | Admin role enforced for this endpoint | FAIL | No role check in servlet or action (Finding-02) |
| 2c | IDOR: company ID verified against authenticated user's org | FAIL | sessCompId is trusted directly; no ownership verification (Finding-06) |
| 2d | Admin-only functionality protected by admin role | FAIL | Any authenticated user can reach dealer company list (Finding-02) |
| 3a | SQL injection in data path for this page | Pass | getSubCompanies uses prepared statement |
| 3b | SQL injection in supporting DAO methods | FAIL | Multiple methods in CompanyDAO use string concatenation (Finding-05) |
| 3c | Input validation on form fields | N/A | Form on this page submits no user data fields (list-only view) |
| 4a | CSRF protection on POST form | FAIL | No token (Finding-01) |
| 4b | Security response headers | FAIL | X-Frame-Options, X-Content-Type-Options, HSTS absent (Finding-07) |
| 4c | Session cookie HttpOnly / Secure flags | FAIL | Not set at application level (Finding-08) |
| 5a | XSS via unescaped output | Pass (with caveat) | bean:write defaults to filter=true but not explicit (Finding-03) |
| 5b | Error pages do not leak stack traces | Pass | web.xml maps Exception to static HTML |
| 5c | Operator/company data scoped to authenticated org | FAIL | Scoping relies on session attribute with no role gate (Finding-06) |
| 6 | Dependency versions (Struts 1.x) | Informational | Struts 1.x is EOL; no security patches available upstream |
| 7 | Build / CI | Not in scope for this JSP audit |  |
