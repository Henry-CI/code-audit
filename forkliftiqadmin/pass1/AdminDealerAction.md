# A11 — AdminDealerAction.java

**Path:** `src/main/java/com/action/AdminDealerAction.java`
**Auditor:** A11
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### Fully Qualified Class Name
`com.action.AdminDealerAction`

### Class Hierarchy
| Relationship | Class/Interface | Line |
|---|---|---|
| extends | `org.apache.struts.action.Action` | 16 |

Note: `AdminDealerAction` does NOT extend `PandoraAction`. It extends the raw Struts 1.x `Action` directly. `PandoraAction` (which extends `Action` and adds session/param helpers) is not in the hierarchy here.

### Fields
None declared. No instance fields.

### Methods

| Modifier | Return Type | Name | Parameters | Line |
|---|---|---|---|---|
| `public` (override) | `ActionForward` | `execute` | `ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response` | 18 |
| `public static` | `void` | `prepareDealerRequest` | `HttpServletRequest request, HttpSession session` | 32 |

### Annotations
None on class or methods. This is a plain Struts 1.x action with no Java annotations of any kind.

### Imports
- `com.actionform.AdminDealerActionForm`
- `com.bean.CompanyBean`
- `com.bean.RoleBean`
- `com.dao.CompanyDAO`
- `org.apache.commons.lang.StringUtils`
- `org.apache.struts.action.*`
- `javax.servlet.http.HttpServletRequest`
- `javax.servlet.http.HttpServletResponse`
- `javax.servlet.http.HttpSession`
- `java.sql.SQLException`
- `java.util.ArrayList`

### ActionForm: AdminDealerActionForm
**FQCN:** `com.actionform.AdminDealerActionForm`
Extends: `org.apache.struts.action.ActionForm`
Annotations: `@Getter`, `@Setter`, `@NoArgsConstructor` (Lombok)
Fields:
- `private String companyId = null` (Lombok-generated getter/setter)

### Struts-Config Action Mapping (`/dealerconvert`)

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

Key mapping properties:
- `scope="session"` — the form bean is stored in **session scope**, not request scope
- `validate="true"` — Struts validator is invoked (delegates to validation.xml)
- No `roles` attribute (Struts 1.x does not enforce roles natively via this attribute in config)
- Both success and failure forward to `adminDealerDefinition`

### DAO Called: CompanyDAO (singleton)

Methods called from `AdminDealerAction`:
- `CompanyDAO.getInstance().convertCompanyToDealer(String companyId)` — line 24
- `CompanyDAO.getInstance().getAllCompany()` — line 35

**`convertCompanyToDealer` internals** (CompanyDAO.java, line 830–845):
- Calls `LoginDAO.isAuthority(companyId, RuntimeConf.ROLE_COMP)` — parameterised query, safe
- If authority matches: executes `UPDATE_COMPANY_ROLE` prepared statement — parameterised, safe
- Else: executes `SAVE_COMPANY_DEALER_ROLE` prepared statement — parameterised, safe

**`getAllCompany` internals** (CompanyDAO.java, line 770–811):
- Static SQL string, no user input, fetches ALL companies from the `company` table

### Session Filter: PreFlightActionServlet
The custom action servlet (`com.actionservlet.PreFlightActionServlet`) performs a pre-flight check in `doGet`:
- For paths NOT in the exclusion list (i.e., all protected paths including `/dealerconvert.do`), it checks that `session != null` and `session.getAttribute("sessCompId")` is non-null/non-empty.
- If this check fails it redirects to the expire/login page.
- `/dealerconvert.do` is NOT in the exclusion list, so this basic session check applies.
- No role-level check is performed by the servlet filter.

---

## Findings

### FINDING 1 — Authentication Guard in `execute()` Runs AFTER the State-Changing DAO Call [CRITICAL]

**Severity:** Critical
**Category:** Authentication / Authorization Order of Operations

**Description:**
In `execute()` (lines 18–30), the `isSuperAdmin` role check is entirely absent before the state-changing call. The sequence is:

```java
// Line 23–25: state-changing DAO call — NO auth check before this
if (StringUtils.isNotBlank(adminDealerForm.getCompanyId())) {
    CompanyDAO.getInstance().convertCompanyToDealer(adminDealerForm.getCompanyId());
}

// Line 27: only THEN is prepareDealerRequest called, which contains the superadmin check
AdminDealerAction.prepareDealerRequest(request, session);
```

`prepareDealerRequest` (line 33) does check `isSuperAdmin`:

```java
if (session.getAttribute("isSuperAdmin").equals(false)) return;
```

However, this check guards only the data-population logic (loading all companies into request attributes for the view). It does NOT guard `convertCompanyToDealer`. Any authenticated session (i.e., any user who has passed the `PreFlightActionServlet` `sessCompId` check) can submit a `companyId` to `/dealerconvert.do` and promote any company to dealer status, regardless of whether they hold the `ROLE_SYS_ADMIN` role.

**Impact:** Any authenticated user — including site admins (`ROLE_SITE_ADMIN`) and dealer-level users — can elevate any arbitrary company to dealer status by posting a valid `companyId`. This is a privilege escalation vulnerability allowing horizontal and vertical privilege abuse.

---

### FINDING 2 — `isSuperAdmin` NullPointerException Risk [HIGH]

**Severity:** High
**Category:** Error Handling / Robustness / Implicit Auth Bypass

**Description:**
In `prepareDealerRequest` (line 33):

```java
if (session.getAttribute("isSuperAdmin").equals(false)) return;
```

`session.getAttribute("isSuperAdmin")` returns `null` if the attribute was never set (e.g., a coding defect in the login flow, or a session that was partially established). Calling `.equals(false)` on `null` throws a `NullPointerException`.

The `global-exceptions` handler in `struts-config.xml` catches `java.sql.SQLException`, `java.io.IOException`, and `javax.servlet.ServletException`, but `NullPointerException` is none of these — it propagates as an unhandled `java.lang.RuntimeException`. The `web.xml` does configure a fallback `<error-page>` for `java.lang.Exception` pointing to `/error/error.html`, which prevents a raw stack trace to the client from this path. However, the exception surfaces before the role check completes.

A secondary risk: if the attribute is present but not a `Boolean` object (e.g., stored as a `String`), `equals(false)` compares a `String` to a `Boolean` and returns `false`, meaning the condition is never true and the method silently proceeds as if the user IS a superadmin, populating the request with all company data. This depends on how `isSuperAdmin` is set during login.

**Impact:** Depending on the type used when setting `isSuperAdmin` in the session at login, the role check may silently pass for all authenticated users, exposing the full company/dealer list to any logged-in user.

---

### FINDING 3 — IDOR: No Ownership Validation on `companyId` Parameter [CRITICAL]

**Severity:** Critical
**Category:** Insecure Direct Object Reference (IDOR)

**Description:**
The `companyId` parameter submitted via `AdminDealerActionForm` is passed directly to `CompanyDAO.getInstance().convertCompanyToDealer(adminDealerForm.getCompanyId())` (line 24) with no verification that the company ID belongs to the authenticated user's organisation, nor that the requesting user has any relationship to the target company.

Even if the superadmin check were correctly placed before the DAO call (see Finding 1), a superadmin could still promote any company in the system, including companies belonging to other entities and dealers. While that may be intentional for a superadmin, the combined absence of any pre-call auth check means the IDOR surface is reachable by all authenticated users.

**Impact:** Any authenticated user can submit an arbitrary integer as `companyId` and, if Finding 1 is not remediated, change the role of any company in the entire database.

---

### FINDING 4 — Form Bean in Session Scope: CSRF and Stale-Data Risk [HIGH]

**Severity:** High
**Category:** CSRF / Session Pollution

**Description:**
The `struts-config.xml` mapping at line 430–438 declares:

```xml
scope="session"
```

For the `adminDealerActionForm`. In Struts 1.x, `scope="session"` means the form bean persists in the HTTP session across requests. This creates two related risks:

1. **CSRF amplification:** Struts 1.x has no built-in CSRF token mechanism, and this application has no Spring Security CSRF filter (it is a pure Struts 1.x application with no Spring Security). A forged cross-site request to `/dealerconvert.do` can carry a valid session cookie and no additional token is required. The session-scoped form means that if an attacker can induce a superadmin to visit a malicious page while logged in, the stored `companyId` value in the session form bean from a previous legitimate request could be used, or a new value can be injected via query string.

2. **Stale data / replay:** If a superadmin submits the form once with a `companyId`, that value remains in the session-scoped form bean. A subsequent navigation to `/dealerconvert.do` with an empty `companyId` in the request will not clear the session-scoped form (Struts repopulates it from the session, so if the new request has no `companyId` parameter, the old value may persist and trigger a repeat conversion).

**Impact:** CSRF is a structural gap for all state-changing endpoints in this application. The session scope amplifies it for this specific action.

---

### FINDING 5 — `getAllCompany()` Returns All Companies to Any Authenticated User [MEDIUM]

**Severity:** Medium
**Category:** Data Exposure / Missing Data Scoping

**Description:**
`prepareDealerRequest` calls `CompanyDAO.getInstance().getAllCompany()` (line 35), which executes an unfiltered `SELECT * FROM company ORDER BY name` returning every company record in the database. The result is placed into request attributes `arrCompanies` and `arrDealers` (lines 51–52).

Although `prepareDealerRequest` has the `isSuperAdmin` early-return guard, the robustness of that guard is in question (see Finding 2). If the guard is bypassed or misconfigured, all company names, addresses, postcodes, email addresses, timezone info, and company IDs are exposed to the requesting user in the view layer.

Even when operating correctly (superadmin only), returning the entirety of the company table on every page load is unnecessarily broad. If the `isSuperAdmin` session attribute is unreliable, this amounts to an information disclosure of the full customer list.

**Impact:** Full customer list disclosure to non-superadmin users if the `isSuperAdmin` guard is bypassed.

---

### FINDING 6 — No Input Validation on `companyId` Before Numeric Conversion [MEDIUM]

**Severity:** Medium
**Category:** Input Validation / Error Handling

**Description:**
`AdminDealerActionForm.companyId` is a `String`. In `convertCompanyToDealer` (CompanyDAO.java, line 835):

```java
ps.setInt(2, Integer.parseInt(companyId));
```

and line 841:

```java
ps.setInt(1, Integer.parseInt(companyId));
```

`Integer.parseInt` throws `NumberFormatException` (a `RuntimeException`) if `companyId` contains non-numeric characters. The `struts-config.xml` global exception handlers do not catch `NumberFormatException`. The `web.xml` `<error-page>` for `java.lang.Exception` should catch it at the container level and redirect to the static error page — preventing a stack trace to the client — but the exception is unhandled within the action/DAO layer itself and will produce an unhandled exception log event.

`StringUtils.isNotBlank` (line 23) only prevents a blank/null string; it does not validate that the value is a valid positive integer. A non-numeric or negative `companyId` will cause an unhandled exception.

**Impact:** Malformed `companyId` values cause unhandled exceptions. Combined with the missing auth guard (Finding 1), an unauthenticated CSRF or post-auth attacker can cause repeated unhandled exceptions.

---

### FINDING 7 — `prepareDealerRequest` Is `public static`: Uncontrolled Reuse Surface [LOW]

**Severity:** Low
**Category:** Design / Encapsulation

**Description:**
`prepareDealerRequest` (line 32) is declared `public static`. This means any other action class in the application can call it without going through the access-control logic of `execute()`. If another action calls `prepareDealerRequest` from a context where `isSuperAdmin` is not set correctly in the session, the full company/dealer list will be exposed.

A search of the codebase would be needed to confirm whether other callers exist, but the exposure is structural — the method's visibility and mutability of its output (writing to request attributes) means the guard can be trivially bypassed at the call site.

**Impact:** Potential reuse of company-list population without the intended access control context.

---

### FINDING 8 — CompanyDAO Contains SQL Injection in Other Methods (Contextual Note) [HIGH]

**Severity:** High (in CompanyDAO, not AdminDealerAction directly)
**Category:** SQL Injection

**Description:**
While not directly exploited by `AdminDealerAction`, the audited DAO (`CompanyDAO`) contains confirmed SQL injection vulnerabilities in methods reachable from other actions in the same application. These are noted here for completeness and cross-reference:

- **`checkExist`** (CompanyDAO.java, line 367): `"select id from company where " + dbField + " ='" + name + "'"` — both `dbField` and `name` are concatenated directly.
- **`checkUserExit`** (CompanyDAO.java, line 385): `"select id from users where " + dbField + " ='" + name + "'"` — same pattern.
- **`checkCompExist`** (CompanyDAO.java, line 408): `name`, `email`, `question`, `answer` fields of `CompanyBean` concatenated into SQL.
- **`getCompLogo`** (CompanyDAO.java, line 471): `"select logo from company where id = " + compId` — `compId` is a String concatenated directly.
- **`getEntityComp`** (CompanyDAO.java, line 669): `entityId` concatenated into SQL when not `"1"`.
- **`getEntityByQuestion`** (CompanyDAO.java, line 702): `qId` and `type` both concatenated.
- **`getAllEntity`** (CompanyDAO.java, line 745): entity ID from `rs.getString(1)` used in a second query within the same loop — not user-controlled, but the pattern is indicative.

These are not called by `AdminDealerAction` itself, but they are in the same singleton DAO and represent significant risk in the wider application.

---

## Checklist Coverage

| # | Checklist Item | Result | Notes |
|---|---|---|---|
| 2.1 | Admin-only functionality protected by admin role check | FAIL | `convertCompanyToDealer` executes before any role check |
| 2.2 | Session-based auth: session check present | PARTIAL | `PreFlightActionServlet` checks `sessCompId` exists; no role enforcement at servlet level |
| 2.3 | IDOR: object belongs to authenticated user's org | FAIL | No ownership check on submitted `companyId`; any integer is accepted |
| 2.4 | Correct role verified (not just authentication) | FAIL | Role check (`isSuperAdmin`) is post-mutation and guards only the view-population path |
| 3.1 | SQL injection: parameterised queries for this action's DAO calls | PASS | `convertCompanyToDealer` and `getAllCompany` use prepared statements |
| 3.2 | Input validation on form parameters | FAIL | `companyId` not validated as positive integer before `Integer.parseInt` |
| 4.1 | CSRF protection present | FAIL | Structural gap — no CSRF token mechanism in Struts 1.x application; session-scoped form amplifies risk |
| 4.2 | Session scope appropriate for form bean | FAIL | `scope="session"` on `adminDealerActionForm`; request scope is appropriate for a one-shot conversion action |
| 5.1 | Error responses do not return stack traces to client | PASS (partial) | `web.xml` error page redirects to static HTML; however unhandled NPE/NFE in action layer is imprecise |
| 5.2 | Data scoped to authenticated user's organisation | FAIL | `getAllCompany()` returns all companies system-wide; relies solely on `isSuperAdmin` guard which has robustness defects |
| 5.3 | `isSuperAdmin` guard: null-safe comparison | FAIL | `session.getAttribute("isSuperAdmin").equals(false)` will NPE if attribute absent |
| 1.x | Secrets / credentials in this file | PASS | No hardcoded credentials in `AdminDealerAction.java` |
| 6.x | Dependencies (not in scope for this file) | N/A | — |
| 7.x | Build / CI (not in scope for this file) | N/A | — |
