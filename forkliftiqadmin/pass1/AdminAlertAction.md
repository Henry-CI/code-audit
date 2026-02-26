# A05 — AdminAlertAction.java
**Path:** src/main/java/com/action/AdminAlertAction.java
**Auditor:** A05
**Date:** 2026-02-26
**Branch:** master

## Reading Evidence

### Fully Qualified Class Name
`com.action.AdminAlertAction`

### Class Hierarchy
| Line | Declaration |
|------|-------------|
| 15   | `public class AdminAlertAction extends org.apache.struts.action.Action` |

Note: `AdminAlertAction` does NOT extend `PandoraAction`. It extends the raw Struts `Action` directly. `PandoraAction` (which provides `getCompId()` and session-attribute helpers) is not used by this class.

### Fields
None declared. No instance fields.

### Annotations
None. No class-level or method-level annotations.

### Public Methods
| Return Type | Method | Parameters | Line |
|-------------|--------|------------|------|
| `ActionForward` | `execute` | `ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response` | 18–36 |

### Imports / Dependencies
- `javax.servlet.http.HttpServletRequest` (line 3)
- `javax.servlet.http.HttpServletResponse` (line 4)
- `org.apache.struts.action.*` (lines 6–11)
- `com.dao.CompanyDAO` (line 13)

### Struts Action Mapping (from struts-config.xml, lines 257–261)
```xml
<action
        path="/adminalert"
        type="com.action.AdminAlertAction">
    <forward name="adminalerts" path="AdminAlertDefinition"/>
</action>
```

Key observations on the mapping:
- **No `name` attribute** — no ActionForm is bound; Struts passes `null` for `actionForm`.
- **No `validate` attribute** — form validation is not invoked (consistent with no form binding).
- **No `roles` attribute** — Struts 1.x `roles` attribute is absent; there is no declarative role enforcement in the mapping.
- **No `scope` attribute** — defaults to `session` scope, but this is moot since no form is bound.
- One forward: `adminalerts` → `AdminAlertDefinition`.
- There is also a related mapping `/adminAlertAdd` (lines 294–300) for `com.action.AdminAddAlertAction` with form `adminAlertActionForm` and `validate="true"`.

### DAO Methods Called
`CompanyDAO.getAlertList()` (line 25) — static method, no parameters.
`CompanyDAO.getReportList()` (line 28) — static method, no parameters.

Both methods execute fixed, parameterless queries against the `subscription` table (lines 42–44 of CompanyDAO.java):
```java
private static final String QUERY_ALERT_LST = " select * from subscription where type ilike 'alert' " ;
private static final String QUERY_REPORT_LST = "select * from subscription where LOWER(type) = 'report'";
```

### Branching Logic (execute method)
```java
String action = request.getParameter("action")==null?"":request.getParameter("action");

if(action.equalsIgnoreCase("alerts")) {
    request.setAttribute("alertList", CompanyDAO.getAlertList());
    return mapping.findForward("adminalerts");
} else if(action.equalsIgnoreCase("reports")) {
    request.setAttribute("alertList", CompanyDAO.getReportList());
    return mapping.findForward("adminalerts");
} else {
    ActionErrors errors = new ActionErrors();
    errors.add(ActionErrors.GLOBAL_MESSAGE, new ActionMessage("errors.global"));
    saveErrors(request, errors);
    return mapping.findForward("globalfailure");
}
```

---

## Findings

### FINDING 1
**Severity:** HIGH
**Title:** No authentication session check inside the Action — relies solely on PreFlightActionServlet gate

**Description:**
`AdminAlertAction.execute()` performs no verification of session attributes (`sessCompId`, `sessUserId`) before serving data. Authentication depends entirely on `PreFlightActionServlet.excludeFromFilter()`. However, `excludeFromFilter` has a logic inversion: it returns `true` for paths that SHOULD be checked and `false` for paths excluded from checking. The session guard only executes when `excludeFromFilter(path)` returns `true`. Since `adminalert.do` is not in the exclusion list, the filter does enforce the session check for GET/POST to `/adminalert.do`, and that is correct at runtime.

The risk is that the Action itself has zero defence-in-depth. If the PreFlightActionServlet is bypassed, misconfigured, or the URL pattern is altered (e.g., a direct `RequestDispatcher.forward()` from another servlet, or a future mapping that routes differently), there is no fallback check inside the Action. This is an architectural weakness consistent with the risk profile of an admin application.

**File + Line:**
- `src/main/java/com/action/AdminAlertAction.java`, lines 18–36 (entire execute method — no session check)
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`, lines 48–61 (sole authentication gate)

**Code Evidence:**
```java
// AdminAlertAction.execute() — no session check whatsoever
public ActionForward execute(ActionMapping mapping,
       ActionForm actionForm, HttpServletRequest request, HttpServletResponse response)
       throws Exception {
    String action = request.getParameter("action")==null?"":request.getParameter("action");
    if(action.equalsIgnoreCase("alerts")) {
        request.setAttribute("alertList", CompanyDAO.getAlertList());
        ...
```

**Recommendation:**
Add an explicit session validation at the top of `execute()` — check that `request.getSession(false)` is non-null and that `sessCompId` and `sessUserId` are present and non-empty. Forward to the expire/login page if either check fails. This is consistent with defence-in-depth for an admin application.

---

### FINDING 2
**Severity:** HIGH
**Title:** No role-based authorisation — any authenticated user can access the admin alert management screen

**Description:**
The `/adminalert` action mapping has no `roles` attribute (struts-config.xml line 257–261). `AdminAlertAction` itself performs no role check. Any user who has a valid `sessCompId` session attribute — regardless of role (operator, site admin, dealer, or super-admin) — can reach the alert and report subscription lists by calling `/adminalert.do?action=alerts` or `/adminalert.do?action=reports`.

This is particularly significant because this is `forkliftiqadmin`, described as an admin application. The checklist explicitly calls out that admin-only functionality must be protected by an admin role check, not just authentication.

**File + Line:**
- `src/main/webapp/WEB-INF/struts-config.xml`, lines 257–261 (no `roles` attribute)
- `src/main/java/com/action/AdminAlertAction.java`, lines 18–36 (no role check in execute)

**Code Evidence:**
```xml
<!-- struts-config.xml lines 257-261: no roles attribute -->
<action
        path="/adminalert"
        type="com.action.AdminAlertAction">
    <forward name="adminalerts" path="AdminAlertDefinition"/>
</action>
```

**Recommendation:**
Add a `roles` attribute to the action mapping (e.g., `roles="ROLE_ADMIN,ROLE_SUPERADMIN"`) to restrict access via the Struts `RequestProcessor` role check, AND add an in-action role check using the session role attribute for defence-in-depth.

---

### FINDING 3
**Severity:** MEDIUM
**Title:** No CSRF protection on state-reading action (CSRF token absent from the entire framework)

**Description:**
Struts 1.x has no built-in CSRF protection. There is no manual CSRF token implementation anywhere in `AdminAlertAction` or in the `PreFlightActionServlet`. The `/adminalert.do?action=alerts` and `/adminalert.do?action=reports` endpoints are GET-accessible (the `doPost` in `PreFlightActionServlet` simply delegates to `doGet`), so an authenticated admin can be tricked into loading these endpoints via a cross-origin request.

Although the actions in this file are read-only (they only call `getAlertList()` and `getReportList()`), the data returned (subscription/alert list) is placed on the request scope and rendered in the response, meaning a CSRF-triggered request would not mutate state but could assist in information gathering via same-origin cached data. More critically, the companion `/adminAlertAdd.do` endpoint (same form) would be vulnerable to CSRF for state-changing operations. The absence of any token mechanism at the framework level is noted here as it affects this Action's threat surface.

**File + Line:**
- `src/main/java/com/action/AdminAlertAction.java`, lines 18–36 (no CSRF token validation)
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`, lines 94–96 (doPost calls doGet without any token check)

**Code Evidence:**
```java
// PreFlightActionServlet.java lines 94-96
public void doPost(final HttpServletRequest req, final HttpServletResponse res) throws ServletException, IOException {
    doGet(req,res);
}
```
No token is read, validated, or compared anywhere.

**Recommendation:**
Implement a synchroniser token pattern: generate a per-session CSRF token at login, embed it as a hidden field in all forms and as a parameter in AJAX calls, and validate it in the `PreFlightActionServlet` (or in a Struts `RequestProcessor` subclass) for all non-GET state-changing requests.

---

### FINDING 4
**Severity:** MEDIUM
**Title:** Unscoped alert/report list — data not filtered by company or role

**Description:**
`CompanyDAO.getAlertList()` and `CompanyDAO.getReportList()` execute queries against the entire `subscription` table with no `WHERE` clause filtering by company, user, or role:

```java
private static final String QUERY_ALERT_LST = " select * from subscription where type ilike 'alert' " ;
private static final String QUERY_REPORT_LST = "select * from subscription where LOWER(type) = 'report'";
```

Every authenticated user reaching `/adminalert.do` receives the full platform-wide list of alert and report subscription types. If the `subscription` table contains entries specific to particular companies, entities, or tiers, this constitutes a data exposure issue. Even if the table is intentionally global, the `SELECT *` pattern means any future columns added (e.g., internal pricing, tier flags, configuration details) would be automatically exposed.

**File + Line:**
- `src/main/java/com/action/AdminAlertAction.java`, lines 25 and 28 (calls to DAO)
- `src/main/java/com/dao/CompanyDAO.java`, lines 42–44 (unscoped queries)

**Code Evidence:**
```java
// AdminAlertAction.java line 25
request.setAttribute("alertList", CompanyDAO.getAlertList());

// CompanyDAO.java line 42-44
private static final String QUERY_ALERT_LST = " select * from subscription where type ilike 'alert' " ;
private static final String QUERY_REPORT_LST = "select * from subscription where LOWER(type) = 'report'";
```

**Recommendation:**
Review whether the `subscription` table contains any company-scoped or tier-scoped rows. If so, add a `WHERE` clause to scope results to the authenticated user's context. Replace `SELECT *` with explicit column selection to prevent inadvertent future data exposure.

---

### FINDING 5
**Severity:** LOW
**Title:** `action` parameter accepted but not validated — silent fallthrough on unknown values

**Description:**
The `action` request parameter (line 22) is read directly with no whitelist validation and no logging of unknown/invalid values. Any value other than `"alerts"` or `"reports"` silently routes to `globalfailure`. While this does not expose data, the absence of input validation and logging means unexpected or probe-style inputs (e.g., `action=<script>`, `action=../../../`) are silently discarded without alerting operators to potential enumeration or probing attempts.

**File + Line:**
- `src/main/java/com/action/AdminAlertAction.java`, line 22

**Code Evidence:**
```java
String action = request.getParameter("action")==null?"":request.getParameter("action");
```

**Recommendation:**
Validate the `action` parameter against an explicit whitelist (`"alerts"`, `"reports"`). Log unexpected values at WARN level to aid in detection of probing. This is consistent with the application's admin context.

---

### FINDING 6
**Severity:** LOW
**Title:** `mailer.do` and `api.do` excluded from authentication in PreFlightActionServlet

**Description:**
While not directly in `AdminAlertAction`, review of the authentication gate in `PreFlightActionServlet` (lines 105–106) shows that `mailer.do` and `api.do` are explicitly excluded from session checks:
```java
else if (path.endsWith("mailer.do")) return false;
else if (path.endsWith("api.do")) return false;
```
These exclusions mean unauthenticated access to those endpoints is possible. This is noted here for completeness because the same PreFlightActionServlet is the sole authentication gate protecting `AdminAlertAction`. The security of `AdminAlertAction` depends on this gate being correctly maintained.

**File + Line:**
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`, lines 105–106

**Code Evidence:**
```java
else if (path.endsWith("mailer.do")) return false;
else if (path.endsWith("api.do")) return false;
```

**Recommendation:**
Review whether `mailer.do` and `api.do` genuinely require unauthenticated access and document the justification. If they process any sensitive data, add authentication checks. This also highlights the fragility of the exclusion-list approach — any new path added incorrectly could accidentally bypass authentication for all admin actions.

---

### FINDING 7
**Severity:** INFO
**Title:** AdminAlertAction does not extend PandoraAction

**Description:**
Unlike other actions in the application (which extend `PandoraAction` for consistent session-attribute access via `getCompId()`, `getLongSessionAttribute()`, etc.), `AdminAlertAction` extends raw `org.apache.struts.action.Action` directly. The DAO methods it calls (`getAlertList()`, `getReportList()`) require no company context, but this architectural inconsistency means the common helper methods are unavailable if the Action is later extended to perform company-scoped operations.

**File + Line:**
- `src/main/java/com/action/AdminAlertAction.java`, line 15

**Code Evidence:**
```java
public class AdminAlertAction extends Action {
```

**Recommendation:**
Consider extending `PandoraAction` for consistency with the rest of the codebase, particularly if future development may add company-scoped queries to this Action.

---

## Checklist Coverage

### 1. Secrets and Configuration
**NOT APPLICABLE to this file.** `AdminAlertAction.java` contains no hardcoded credentials, database URLs, API keys, or secrets. The DAO layer (`CompanyDAO`) uses `DBUtil` for connection management with no credentials visible in this action. No `.properties` or config files are referenced in this file. — **PASS (file scope)**

### 2. Authentication and Authorization
**FAIL — two issues found.**
- Authentication: `AdminAlertAction` performs no in-action session check. Authentication is delegated entirely to `PreFlightActionServlet` (FINDING 1 — HIGH).
- Authorization: No role check in the action mapping (no `roles` attribute) and no in-action role verification. Any authenticated user can access admin alert/report listings (FINDING 2 — HIGH).
- The `sessCompId` session attribute pattern is present in `PreFlightActionServlet` but not used in this Action.

### 3. Input Validation and Injection
**PARTIAL FAIL.**
- The `action` parameter is read without explicit whitelist validation (FINDING 5 — LOW). No injection risk exists in this specific Action since the parameter is only used in `equalsIgnoreCase` comparisons and never passed to a query.
- The DAO queries called by this Action (`getAlertList`, `getReportList`) use fixed SQL with no user input — no SQL injection risk in this code path.
- No file access, no command execution, no XML parsing, no deserialization in this Action.
- **PASS on injection; LOW finding on input validation.**

### 4. Session and CSRF
**FAIL.**
- No CSRF token mechanism exists anywhere in the framework (FINDING 3 — MEDIUM). Struts 1.x has no built-in CSRF protection and none has been implemented manually.
- `doPost` in `PreFlightActionServlet` simply calls `doGet` with no distinction, meaning the endpoint accepts both GET and POST without token validation.
- No `X-Frame-Options`, `X-Content-Type-Options`, or `Strict-Transport-Security` headers are set by this Action or by any filter visible in web.xml (only `CharsetEncodingFilter` is registered).
- Session timeout is set to 30 minutes in web.xml (line 46) — adequate.
- Cookie security flags (`Secure`, `HttpOnly`, `SameSite`) are not configured in web.xml — not explicitly checked in this file's scope.

### 5. Data Exposure
**FAIL — one issue found.**
- `getAlertList()` and `getReportList()` return the full platform-wide subscription list with `SELECT *` and no company scoping (FINDING 4 — MEDIUM).
- No stack traces are returned to the client; the `else` branch uses `ActionErrors` / `globalfailure` forward, and web.xml maps `java.lang.Exception` to `/error/error.html`.
- No PII or sensitive data appears to be directly logged in this Action (log statements are only in the DAO).

### 6. Dependencies
**NOT APPLICABLE to this file.** Dependency version analysis is a `pom.xml`-level concern, not scoped to this action class. The action uses standard Struts 1.x classes and `CompanyDAO` — no direct third-party dependencies are introduced.

### 7. Build and CI
**NOT APPLICABLE to this file.** Build and CI pipeline analysis is outside the scope of this action class file.
