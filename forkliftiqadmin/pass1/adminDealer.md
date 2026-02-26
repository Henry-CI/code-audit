# A10 — adminDealer.jsp

**Path:** src/main/webapp/html-jsp/adminDealer.jsp
**Auditor:** A10 (Claude Sonnet 4.6)
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### File: adminDealer.jsp
**Full path:** src/main/webapp/html-jsp/adminDealer.jsp
**Lines:** 65 (file ends after closing `</div>` at line 65; no closing `</html:form>` tag issue — tag is present at line 63)

#### Includes
- Line 1: `<%@ include file="../includes/importLib.jsp" %>` — static include of tag library declarations and Java imports (importLib.jsp imports Struts tag libs, log4j, Cookie, ArrayList, RuntimeConf, InfoLogger, Calendar).

#### Form Tags
| Line | Tag | action | method |
|------|-----|--------|--------|
| 16 | `<html:form>` | `/dealerconvert.do` | `post` |

No `<html:hidden>` CSRF token field present anywhere in the form.

#### Scriptlets
None. The JSP contains no `<% ... %>` scriptlet blocks.

#### Expression Outputs (`<%= %>`, `${...}`, `<bean:write>`)
| Line | Type | Expression | Escaped? |
|------|------|-----------|---------|
| 53 | `<bean:write>` | `property="name" name="DealerRecord"` | Default `filter="true"` — HTML-escaped by Struts `bean:write` |

No raw `<%= %>` or `${...}` EL expressions present in this JSP.

#### `<html:select>` / `<html:optionsCollection>`
| Line | Tag | Binding |
|------|-----|---------|
| 22–25 | `<html:select property="companyId">` with `<html:optionsCollection name="arrCompanies" value="id" label="name"/>` | Renders company `id` as option value, company `name` as option label. Both sourced from request attribute `arrCompanies` (ArrayList of CompanyBean). Option values are numeric DB IDs; labels are HTML-escaped by the Struts html tag library. |

#### Hidden Fields
None.

#### URL Construction
- Breadcrumb link at line 5: `href="adminmenu.do?action=home"` — static, no user input.
- Breadcrumb link at line 6: `href="adminmenu.do?action=configDealer"` — static, no user input.
- Form action at line 16: `/dealerconvert.do` — static.

#### request.getParameter / session access (in backing Action classes)
**AdminMenuAction.java (configDealer branch, line 60–62):**
- `request.getParameter("action")` — used for routing only; not reflected into output.
- `session.getAttribute("sessCompId")` — used for company context.
- `session.getAttribute("isSuperAdmin")` — gating call to `AdminDealerAction.prepareDealerRequest()`.

**AdminDealerAction.java:**
- `session.getAttribute("isSuperAdmin")` — checked via `.equals(false)` early return at line 33.
- `adminDealerForm.getCompanyId()` — form field; passed directly to `CompanyDAO.convertCompanyToDealer(String)` at line 24 without further server-side validation beyond `StringUtils.isNotBlank()`.

#### Request Attributes Set by Action
| Attribute | Value | Set in |
|-----------|-------|--------|
| `arrCompanies` | `ArrayList<CompanyBean>` of non-dealer companies (all companies system-wide) | `AdminDealerAction.prepareDealerRequest()` line 51 |
| `arrDealers` | `ArrayList<CompanyBean>` of dealer companies | `AdminDealerAction.prepareDealerRequest()` line 52 |

#### struts-config.xml: dealerconvert action
```xml
<action
    path="/dealerconvert"
    name="adminDealerActionForm"
    scope="session"
    validate="true"
    type="com.action.AdminDealerAction"
    input="adminDealerDefinition">
    <forward name="success" path="adminDealerDefinition"/>
    <forward name="failure" path="adminDealerDefinition"/>
</action>
```
Key: `scope="session"` — the form bean is stored in the HTTP session, not the request.

#### validation.xml
No entry for `adminDealerActionForm` exists in validation.xml. The `validate="true"` attribute in struts-config.xml will invoke the `validate()` method on `AdminDealerActionForm`, which inherits the default no-op `validate()` from `ActionForm` (Struts returns no errors). No field-level constraints are declared.

#### AdminDealerActionForm.java
Single field: `private String companyId = null;` — no JSR-303 annotations, no override of `validate()`.

#### CompanyDAO.convertCompanyToDealer (line 830–845)
Accepts `String companyId`, calls `Integer.parseInt(companyId)` inside a PreparedStatement lambda — uses parameterised queries. The companyId value originates entirely from the submitted form field.

#### CompanyDAO.getAllCompany (line 770–811)
Returns every company in the database. No scoping by the authenticated user's company. Fetches: id, name, address, postcode, email, unit, timezone, lan_id.

#### PreFlightActionServlet (session check)
`dealerconvert.do` is NOT in the exclusion list — the servlet's `excludeFromFilter()` returns `true` for this path, so it IS checked. The check validates that a session exists and `sessCompId` is not null/empty. It does NOT check role or authority — any authenticated user with a valid session can POST to `/dealerconvert.do`.

---

## Findings

### FINDING 1 — CRITICAL: No CSRF Protection on Dealer Conversion Form
**File:** adminDealer.jsp line 16; struts-config.xml lines 430–438
**Category:** CSRF (Checklist §4)

The `<html:form>` posts to `/dealerconvert.do` via HTTP POST with no CSRF token. Struts 1.x has no built-in CSRF protection. No synchroniser token is generated or verified anywhere in the request/response cycle for this action. `scope="session"` for the form bean does not constitute CSRF protection — it only means the form bean persists across requests in the same session.

An attacker who tricks an authenticated super-admin into visiting a malicious page can silently submit a cross-origin POST to `/dealerconvert.do?companyId=<target_id>`, promoting any arbitrary company to dealer status. This is a privilege-escalation primitive — "dealer" role grants access to dealer-scoped report actions (`DealerImpactReportAction`, `DealerPreOpsReportAction`, `DealerSessionReportAction`, etc.).

**Evidence:**
- No `<html:hidden property="org.apache.struts.taglib.html.TOKEN"/>` or equivalent in the JSP.
- No call to `saveToken(request)` in `AdminDealerAction.execute()` or `AdminMenuAction` configDealer branch.
- No call to `isTokenValid(request)` in `AdminDealerAction.execute()`.

---

### FINDING 2 — HIGH: Broken Access Control — Role Check Only on Data Population, Not on Action Execution
**File:** AdminDealerAction.java lines 23–29
**Category:** Authentication and Authorization (Checklist §2)

`AdminDealerAction.execute()` checks `isSuperAdmin` only when calling `prepareDealerRequest()` (data population), but the actual state-changing operation — `CompanyDAO.convertCompanyToDealer(adminDealerForm.getCompanyId())` — executes unconditionally at line 24 for any non-blank `companyId`, before the super-admin check at line 33 (which is inside `prepareDealerRequest()`).

The logic is:
```java
// Line 23-25: ALWAYS executes if companyId is non-blank
if (StringUtils.isNotBlank(adminDealerForm.getCompanyId())) {
    CompanyDAO.getInstance().convertCompanyToDealer(adminDealerForm.getCompanyId());
}

// Line 27: prepareDealerRequest contains the isSuperAdmin check
AdminDealerAction.prepareDealerRequest(request, session);
// Inside prepareDealerRequest (line 33):
// if (session.getAttribute("isSuperAdmin").equals(false)) return;
```

Any authenticated non-super-admin user (e.g., a site admin or dealer admin) who can reach `/dealerconvert.do` — which only requires `sessCompId` to be set — can convert any company to dealer status. The `PreFlightActionServlet` only checks for session existence and a non-null `sessCompId`; it does not enforce role. The super-admin gate is applied too late (post-mutation) and only affects data returned to the page, not the mutation itself.

**Impact:** A dealer or site admin can escalate any company to dealer status, expanding their own or others' data-access scope.

---

### FINDING 3 — HIGH: IDOR on companyId — No Ownership Validation
**File:** AdminDealerAction.java line 24; AdminDealerActionForm.java
**Category:** IDOR / Authorization (Checklist §2)

`companyId` is a raw string submitted by the client. It is passed directly to `CompanyDAO.convertCompanyToDealer()` after only a blank-check (`StringUtils.isNotBlank`). There is no validation that:
1. The submitted ID corresponds to an existing company.
2. The submitting user has any relationship to the target company.
3. The value is a valid integer (a non-numeric value will cause `Integer.parseInt` to throw inside the DAO, but this is caught by the global exception handler and results in a silent redirect — no security enforcement).

Even if FINDING 2 were fixed (super-admin check moved before the mutation), a super-admin could still be manipulated via CSRF (FINDING 1) to promote an arbitrary companyId. There is no secondary confirmation step for this irreversible privilege change.

---

### FINDING 4 — HIGH: Form Bean Scope is "session" — Token/State Fixation Risk
**File:** struts-config.xml line 432
**Category:** Session / CSRF (Checklist §4)

The `adminDealerActionForm` is declared with `scope="session"`. In Struts 1.x, session-scoped form beans persist between requests. This means:

1. A companyId submitted in a previous request remains in the session form bean. A subsequent GET to the dealer page will re-populate the form with the previous companyId value, and a subsequent POST (e.g., triggered by CSRF) will resubmit the stale companyId.
2. In multi-tab scenarios, concurrent form submissions will share state, potentially causing one tab's submission to be overwritten by another.
3. The stale session bean compounds the CSRF risk: if an attacker can predict or enumerate company IDs (they are sequential integers), a single CSRF hit with a carefully chosen ID will be effective even if the victim never actively uses the form.

---

### FINDING 5 — MEDIUM: No Input Validation on companyId Field
**File:** AdminDealerActionForm.java; validation.xml (absent entry)
**Category:** Input Validation (Checklist §3)

`adminDealerActionForm` has `validate="true"` in struts-config.xml, but no corresponding entry in validation.xml and no override of `ActionForm.validate()`. The `companyId` field is therefore never validated for:
- Type (must be a positive integer).
- Range (must correspond to an existing, non-dealer company).
- Whitelist (only IDs from the `arrCompanies` dropdown should be accepted).

Although the DAO uses `PreparedStatement` (parameterised), a non-integer companyId will propagate to `Integer.parseInt()` inside the DAO lambda, resulting in an unhandled `NumberFormatException` that surfaces as a generic error page. This also means the `companyId` parameter can be tampered with (see FINDING 3) without triggering any application-level validation error.

---

### FINDING 6 — MEDIUM: Null Dereference Risk on isSuperAdmin Session Attribute
**File:** AdminDealerAction.java line 33
**Category:** Robustness / Authorization (Checklist §2)

```java
if (session.getAttribute("isSuperAdmin").equals(false)) return;
```

If `isSuperAdmin` is not present in the session (e.g., due to partial session initialisation, session manipulation, or a code path that does not set this attribute), `session.getAttribute("isSuperAdmin")` returns `null` and the `.equals(false)` call throws a `NullPointerException`. The global exception handler catches `java.lang.Exception` and redirects to the error page — which means the data-population logic silently fails but the mutation at line 24 has already executed (see FINDING 2). Additionally, if session state is manipulated to remove this attribute, the guard can be bypassed by inducing NPE.

---

### FINDING 7 — MEDIUM: getAllCompany Returns All Companies Cross-Tenant Without Scoping
**File:** CompanyDAO.java lines 770–811; AdminDealerAction.java line 35
**Category:** Data Exposure / Multi-tenancy (Checklist §5)

`CompanyDAO.getAllCompany()` executes:
```sql
select id,name,address,postcode,email,unit,timezone,lan_id from company order by name
```

This returns every company in the system with no filter. The results (including company email addresses and postcodes) are placed in the `arrCompanies` and `arrDealers` request attributes and rendered in the JSP. While the intent is that only super-admins reach this page, FINDING 2 shows the gate is broken. Even if the gate were correct, returning the full company list (including email, address, postcode) to the admin page rather than a minimised projection (id, name only) increases the blast radius of any XSS or data-exposure vulnerability elsewhere in the page or its tile template.

---

### FINDING 8 — LOW: bean:write Default Escaping Confirmed — No XSS at This Output Point
**File:** adminDealer.jsp line 53
**Category:** XSS (Checklist §3)

`<bean:write property="name" name="DealerRecord"/>` uses the default `filter="true"` behaviour, which HTML-encodes the output. No raw `filter="false"` is present. This output point is not vulnerable to reflected or stored XSS as written. Noted for completeness.

---

### FINDING 9 — INFORMATIONAL: Struts 1.x EOL — Framework-Level Risk
**File:** pom.xml / web.xml (struts 1.3)
**Category:** Dependencies (Checklist §6)

The application uses Apache Struts 1.x, which reached end-of-life in 2013. Struts 1.x has no built-in CSRF protection, no expression-language injection protection comparable to modern frameworks, and receives no security patches. All findings above are made worse by the absence of framework-level mitigations that would exist in a maintained framework (Spring Security CSRF tokens, Thymeleaf automatic escaping, etc.).

---

## Checklist Coverage

| # | Area | Items Checked | Findings |
|---|------|---------------|---------|
| 1 | Secrets and Configuration | No secrets in JSP; web.xml contains no credentials; no DB URLs in scope | None for this file |
| 2 | Authentication and Authorization | PreFlightActionServlet session check; isSuperAdmin gate placement; role enforcement on mutation; IDOR on companyId | FINDING 2 (HIGH), FINDING 3 (HIGH), FINDING 6 (MEDIUM) |
| 3 | Input Validation and Injection | companyId validation; bean:write escaping; SQL injection in DAO | FINDING 5 (MEDIUM), FINDING 8 (LOW — no issue) |
| 4 | Session and CSRF | CSRF token presence; form bean scope; session attribute risks | FINDING 1 (CRITICAL), FINDING 4 (HIGH) |
| 5 | Data Exposure | getAllCompany scope; fields returned; cross-tenant data | FINDING 7 (MEDIUM) |
| 6 | Dependencies | Struts 1.x EOL status | FINDING 9 (INFO) |
| 7 | Build and CI | Not in scope for this JSP-level audit | Not assessed |

### Summary of Findings by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | F1 |
| HIGH | 3 | F2, F3, F4 |
| MEDIUM | 3 | F5, F6, F7 |
| LOW | 1 | F8 (no vulnerability) |
| INFO | 1 | F9 |
