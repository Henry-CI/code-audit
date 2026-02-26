# A04 — AdminAddAlertAction.java
**Path:** src/main/java/com/action/AdminAddAlertAction.java
**Auditor:** A04
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### Fully Qualified Class Name
`com.action.AdminAddAlertAction`

### Class Hierarchy
| Line | Declaration |
|------|-------------|
| 17 | `public class AdminAddAlertAction extends Action` |

The class extends `org.apache.struts.action.Action` directly. It does **not** extend `PandoraAction` (which is `com.action.PandoraAction extends Action`). Therefore no helper methods from `PandoraAction` are inherited.

### Class-Level Annotations
None.

### Fields
None declared in this class (no instance fields).

### Public Methods
| Return Type | Name | Parameters | Line |
|-------------|------|------------|------|
| `ActionForward` | `execute` | `ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response` | 20 |

### Method-Level Annotations
| Line | Annotation | Method |
|------|------------|--------|
| 19 | `@Override` | `execute` |

### Action Mapping (from struts-config.xml, lines 293–301)
```xml
<action
    path="/adminAlertAdd"
    name="adminAlertActionForm"
    scope="request"
    type="com.action.AdminAddAlertAction"
    validate="true"
    input="adminDefinition">
    <forward name="adminalerts" path="AdminAlertDefinition"/>
</action>
```

| Attribute | Value |
|-----------|-------|
| Path | `/adminAlertAdd` (maps to URL `/adminAlertAdd.do`) |
| Form bean | `adminAlertActionForm` → `com.actionform.AdminAlertActionForm` |
| Scope | `request` |
| Validate | `true` |
| Input (on validation failure) | `adminDefinition` |
| Roles attribute | **Not present** — no `roles` attribute on this action mapping |
| Forward | `adminalerts` → `AdminAlertDefinition` |

Note: No `roles` attribute is configured on this action mapping. The Struts `roles` attribute is the declarative way to restrict actions to specific roles in Struts 1.x; its absence means Struts does not enforce any role restriction on this action.

### ActionForm: AdminAlertActionForm (src/main/java/com/actionform/AdminAlertActionForm.java)
Fields:
- `private int alertId` (line 9)
- `private String alertDesc` (line 10)
- `private String alertCode` (line 11)
- `private ArrayList arrVehicles` (line 12, raw type)
- `private String action` (line 13)
- `private String[] unitIds` (line 14)
- `private String alert_id = null` (line 15) — **this is the field used by AdminAddAlertAction**
- `private int impactLevel` (line 18)
- `private boolean isActive` (line 19)

The `alert_id` field is populated from the HTTP form/request parameter `alert_id` via Struts binding. No validation rules for `adminAlertActionForm` are defined in `validation.xml` (the file only defines rules for `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`). Despite `validate="true"` in struts-config.xml, there are no corresponding rules in validation.xml for this form, so Struts validation is a no-op for this action.

### DAOs and Services Called Within execute()
| DAO / Method | Location | Line in Action |
|--------------|----------|---------------|
| `CompanyDAO.addUserSubscription(String userId, String alertId)` | `com.dao.CompanyDAO`, line 862 | 28, 31 |
| `CompanyDAO.getAlertList()` | `com.dao.CompanyDAO`, line 813 | 29 |
| `CompanyDAO.getReportList()` | `com.dao.CompanyDAO`, line 847 | 32 |

### CompanyDAO.addUserSubscription (lines 862–869 of CompanyDAO.java)
```java
public static void addUserSubscription(String userId, String alertId) throws Exception {
    log.info("Inside LoginDAO Method : addUserSubscription");
    DBUtil.updateObject("insert into user_subscription(user_id, subscription_id) values(?, ?)", stmt -> {
        stmt.setInt(1, Integer.parseInt(userId));
        stmt.setInt(2, Integer.parseInt(alertId));
    });
}
```
Both `userId` and `alertId` are passed as `?` bind parameters — the SQL itself is parameterised.

### PreFlightActionServlet Session Check
`web.xml` registers `com.actionservlet.PreFlightActionServlet` as the Struts action servlet. Its `doGet` method (lines 36–86):
- Calls `excludeFromFilter(path)`: `/adminAlertAdd.do` is **not** in the exclusion list, so it returns `true`.
- For paths not excluded, it checks: `session == null` or `session.getAttribute("sessCompId") == null || equals("")`. If either condition is true it forwards to the expire page.
- This means a session with a non-null, non-empty `sessCompId` is required before `execute()` is reached.

However, the servlet only checks for `sessCompId` presence; it does **not** check for an admin role or any privilege level.

---

## Findings

### FINDING 1 — HIGH: No Admin Role Enforcement; Any Authenticated User Can Add Alert Subscriptions

**Severity:** HIGH

**Description:**
`AdminAddAlertAction` is in the `Admin` package and is registered under the path `/adminAlertAdd.do` in the admin application. It writes a `user_subscription` row on behalf of the session user. Neither the action mapping in struts-config.xml nor the `execute()` method enforces that the caller holds an admin-level role.

The only gate is the `PreFlightActionServlet` session check, which verifies that `sessCompId` is set in the session. Any authenticated session — regardless of role — satisfies this check. There is no call to a role-check method, no inspection of `sessRole` or equivalent session attribute, and no Struts `roles` attribute on the action mapping.

**Evidence:**

struts-config.xml lines 293–301 — no `roles` attribute:
```xml
<action
    path="/adminAlertAdd"
    name="adminAlertActionForm"
    scope="request"
    type="com.action.AdminAddAlertAction"
    validate="true"
    input="adminDefinition">
```

AdminAddAlertAction.java lines 20–39 — no role check in execute():
```java
public ActionForward execute(ActionMapping mapping, ActionForm actionForm,
        HttpServletRequest request, HttpServletResponse response) throws Exception {
    HttpSession session = request.getSession(false);
    String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
    String src = request.getParameter("src") == null ? "" : request.getParameter("src");
    int sessUserId = session.getAttribute("sessUserId") == null ? 0 : (Integer) session.getAttribute("sessUserId");
    AdminAlertActionForm alertAction = (AdminAlertActionForm) actionForm;

    if (src.equalsIgnoreCase("alert")) {
        CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
        ...
    }
```

**Recommendation:**
Add a Struts `roles` attribute to the action mapping (e.g., `roles="ROLE_ADMIN,ROLE_SITEADMIN"`), and/or add an explicit role check at the start of `execute()` by reading a role attribute from the session and comparing it against an allowlist of admin roles. Reject the request and redirect to the login or error page if the role is insufficient.

---

### FINDING 2 — HIGH: IDOR — User Can Subscribe Any User to Any Alert by Manipulating `alert_id`

**Severity:** HIGH

**Description:**
The action subscribes the currently logged-in user (`sessUserId` from session) to an alert identified by `alert_id` from the ActionForm (which originates from the HTTP request parameter `alert_id`). The `alert_id` value is passed directly to `CompanyDAO.addUserSubscription()` with no verification that the `alert_id` is a valid, existing subscription record, and no verification that it is appropriate for the logged-in user's company or organisation.

Although `sessUserId` is taken from the trusted session and cannot be spoofed by the client, the subscription_id (`alert_id`) is fully client-controlled. An attacker can iterate over integer `alert_id` values to subscribe themselves to arbitrary subscription types they are not entitled to. Because `addUserSubscription` uses parameterised SQL and performs no existence or authorisation check on the `subscription_id`, the insert will succeed for any integer value that corresponds to a row in the `subscription` table.

**Evidence:**

AdminAddAlertAction.java lines 25–32:
```java
AdminAlertActionForm alertAction = (AdminAlertActionForm) actionForm;

if (src.equalsIgnoreCase("alert")) {
    CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
    request.setAttribute("alertList", CompanyDAO.getAlertList());
} else if (src.equalsIgnoreCase("report")) {
    CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
    request.setAttribute("alertList", CompanyDAO.getReportList());
}
```

CompanyDAO.java lines 862–869:
```java
public static void addUserSubscription(String userId, String alertId) throws Exception {
    log.info("Inside LoginDAO Method : addUserSubscription");
    DBUtil.updateObject("insert into user_subscription(user_id, subscription_id) values(?, ?)", stmt -> {
        stmt.setInt(1, Integer.parseInt(userId));
        stmt.setInt(2, Integer.parseInt(alertId));
    });
}
```

There is no lookup to confirm that `alertId` belongs to the subscription catalogue appropriate for the user's company, and no check for duplicate subscriptions.

**Recommendation:**
Before inserting, validate that the `alert_id` value exists in the `subscription` table and corresponds to a type consistent with the `src` parameter (e.g., type = 'alert' when `src` is "alert"). Consider fetching the list of valid alert/report IDs server-side and rejecting any `alert_id` not in that set.

---

### FINDING 3 — HIGH: No CSRF Protection

**Severity:** HIGH

**Description:**
`AdminAddAlertAction` is a state-changing action (it inserts a row into `user_subscription`). Struts 1.x provides no built-in CSRF protection. The action performs no manual CSRF token check. The `web.xml` defines no CSRF filter. The `struts-config.xml` mapping for this action does not reference any CSRF mechanism.

Any page on the internet can submit a cross-site POST (or GET) to `/adminAlertAdd.do` with an attacker-chosen `alert_id` and `src` parameter. If the victim's browser holds a valid session cookie, the subscription insertion will execute on their behalf.

**Evidence:**

No CSRF token field or check appears anywhere in AdminAddAlertAction.java. No CSRF filter is declared in web.xml. The only filter in web.xml (lines 8–15) is a character encoding filter:
```xml
<filter>
    <filter-name>Character Encoding</filter-name>
    <filter-class>com.util.CharsetEncodingFilter</filter-class>
</filter>
```

AdminAlertActionForm.java contains no CSRF token field.

**Recommendation:**
Implement a synchroniser token pattern: generate a random per-session token, store it in the session, embed it as a hidden field in all forms that submit to state-changing actions, and verify the submitted token against the session value at the start of `execute()`. Alternatively, introduce a servlet filter that enforces CSRF tokens for all non-excluded `.do` paths.

---

### FINDING 4 — MEDIUM: Null Session Dereference — No Null Guard on `request.getSession(false)`

**Severity:** MEDIUM

**Description:**
Line 21 calls `request.getSession(false)`, which returns `null` if no session exists. Line 22 immediately dereferences `session` without a null check:

```java
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
```

If `session` is `null`, this throws a `NullPointerException`. While `PreFlightActionServlet` is supposed to intercept requests with no session before they reach `execute()`, that guard is in a servlet that can be subverted (e.g., through direct dispatcher forwarding, or if the session expires between the servlet check and the action execution). The absence of a local null guard means that the failure mode is an unhandled exception rather than a controlled redirect.

**Evidence:**

AdminAddAlertAction.java lines 21–22:
```java
HttpSession session = request.getSession(false);
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
```

**Recommendation:**
Add a null check immediately after line 21:
```java
if (session == null) {
    return mapping.findForward("failure"); // or redirect to login
}
```

---

### FINDING 5 — MEDIUM: `alert_id` Form Field Is Unvalidated — No Type or Bounds Check Before Integer Parsing

**Severity:** MEDIUM

**Description:**
`alertAction.getAlert_id()` returns a raw `String` value bound directly from the HTTP request parameter `alert_id`. This value is passed to `CompanyDAO.addUserSubscription()`, which calls `Integer.parseInt(alertId)` at line 867. There is no validation rule for `adminAlertActionForm` in `validation.xml` (the form has no entry at all). Despite `validate="true"` on the action mapping, the Struts validator framework has no rules to apply and performs no validation.

If `alert_id` is `null`, non-numeric, or an out-of-range integer, `Integer.parseInt` will throw a `NumberFormatException`. This exception propagates up through `execute()` and is caught by the global Struts exception handler (struts-config.xml lines 43–55), which maps `java.sql.SQLException` to an error page but does not list `NumberFormatException`. The result is an unhandled exception, potentially exposing a stack trace.

**Evidence:**

validation.xml — no entry for `adminAlertActionForm`:
```xml
<formset>
    <form name="loginActionForm"> ... </form>
    <form name="adminRegisterActionForm"> ... </form>
    <form name="AdminDriverEditForm"> ... </form>
</formset>
```

AdminAlertActionForm.java line 15 (alert_id is a String, default null):
```java
private String alert_id = null;
```

CompanyDAO.java line 867:
```java
stmt.setInt(2, Integer.parseInt(alertId));
```

struts-config.xml global exception handler (lines 42–55) — no entry for `NumberFormatException`:
```xml
<global-exceptions>
    <exception key="errors.global" type="java.sql.SQLException" path="errorDefinition"/>
    <exception key="errors.global" type="java.io.IOException" path="errorDefinition"/>
    <exception key="errors.global" type="javax.servlet.ServletException" path="errorDefinition"/>
</global-exceptions>
```

**Recommendation:**
Add a validation rule for `adminAlertActionForm` in `validation.xml` to require `alert_id` to be an integer. Also add a `NumberFormatException` entry to the global exception handler, and/or validate the `alert_id` string as a non-null, parseable positive integer before calling the DAO.

---

### FINDING 6 — LOW: `sessCompId` Is Read from Session but Never Used

**Severity:** LOW (defensive code quality issue with potential security implication)

**Description:**
Line 22 reads `sessCompId` from the session but this variable is never used in the rest of `execute()`. The action uses `sessUserId` for the database write. The `sessCompId` is the natural authorisation anchor to scope subscriptions to the correct organisation, but it is not used. This suggests that a company-scoping check was either never implemented or was removed, and is consistent with the IDOR finding (Finding 2). It is also dead code that may mislead future maintainers into believing a company-scope check is present.

**Evidence:**

AdminAddAlertAction.java line 22:
```java
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
```

`sessCompId` does not appear on any subsequent line in the file.

**Recommendation:**
Either use `sessCompId` to scope the alert list or subscription check to the user's company, or remove the variable if it has no purpose. Resolving the IDOR (Finding 2) would naturally make use of this value.

---

### FINDING 7 — INFO: `src` Parameter Is Read Directly from HTTP Request (Not from Form)

**Severity:** INFO

**Description:**
The `src` parameter (line 23) is read from the raw HTTP request via `request.getParameter("src")` rather than from the `AdminAlertActionForm`. This is an architectural inconsistency — other form values come through the ActionForm binding mechanism, but `src` bypasses it. The `src` value is only compared with `equalsIgnoreCase`, which is safe from injection, but this pattern means `src` is not subject to any form-level validation that might be added in future.

**Evidence:**

AdminAddAlertAction.java line 23:
```java
String src = request.getParameter("src") == null ? "" : request.getParameter("src");
```

**Recommendation:**
Move the `src` field into `AdminAlertActionForm` so that it is subject to the same validation lifecycle as other form fields.

---

### FINDING 8 — INFO: Duplicate Subscription Inserts Not Prevented

**Severity:** INFO

**Description:**
`CompanyDAO.addUserSubscription` performs an unconditional `INSERT INTO user_subscription`. There is no `WHERE NOT EXISTS` guard, no unique constraint check at the application level, and no check for a pre-existing subscription before inserting. Repeated submissions of the same `alert_id` by the same user will insert duplicate rows unless the database schema enforces a unique constraint on `(user_id, subscription_id)`. If no such constraint exists in the database, a user could accumulate duplicate notification subscriptions. This is a data-integrity issue that also has a minor security implication (potential spam/notification abuse).

**Evidence:**

CompanyDAO.java lines 865–868:
```java
DBUtil.updateObject("insert into user_subscription(user_id, subscription_id) values(?, ?)", stmt -> {
    stmt.setInt(1, Integer.parseInt(userId));
    stmt.setInt(2, Integer.parseInt(alertId));
});
```

No duplicate check appears in `AdminAddAlertAction.execute()` or in `addUserSubscription`.

**Recommendation:**
Add an application-level check (or use `INSERT ... ON CONFLICT DO NOTHING` if the database supports it) to prevent duplicate subscriptions. Verify that the `user_subscription` table has a unique index on `(user_id, subscription_id)`.

---

## Checklist Coverage

### 1. Secrets and Configuration
**Result: No findings for this file.**
No hardcoded credentials, API keys, database URLs, or passwords appear in `AdminAddAlertAction.java`. The DAO (`CompanyDAO`) obtains connections through `DBUtil` without embedding credentials. The action itself contains no configuration references.

### 2. Authentication and Authorization
**Result: FINDINGS 1, 2.**

- Authentication: The `PreFlightActionServlet` enforces that a session with a non-null `sessCompId` exists before `execute()` is called. Basic authentication is therefore enforced at the servlet level, not within `execute()` itself.
- Admin role enforcement: **Missing.** No `roles` attribute on the action mapping; no role check in `execute()`. (Finding 1, HIGH)
- IDOR / object ownership: **Missing.** The `alert_id` is entirely client-supplied and is not validated against the user's company or the set of permissible subscriptions. (Finding 2, HIGH)

### 3. Input Validation and Injection
**Result: FINDINGS 4, 5; SQL injection not present.**

- SQL injection: Not present. `CompanyDAO.addUserSubscription` uses parameterised queries with `PreparedStatement`. `getAlertList()` and `getReportList()` use fixed SQL with no user input. (No finding)
- Input validation: `alert_id` is unvalidated; no validation.xml rules exist for `adminAlertActionForm`. `Integer.parseInt` on a null or non-numeric value will throw an unhandled exception. (Finding 5, MEDIUM)
- Null dereference on session: `session` can be null but is dereferenced without a null guard. (Finding 4, MEDIUM)
- Command injection: No `Runtime.exec()` or `ProcessBuilder` calls. (No finding)
- Path traversal: No file operations. (No finding)
- XXE: No XML parsing. (No finding)
- SSRF: No outbound HTTP calls from this action. (No finding)
- Deserialization: No `ObjectInputStream` or unsafe Jackson usage. (No finding)

### 4. Session and CSRF
**Result: FINDING 3.**

- CSRF: No CSRF token check. This is a state-changing action with no protection against cross-site request forgery. (Finding 3, HIGH)
- Session fixation: No session manipulation (no `session.invalidate()` + `request.getSession(true)` calls). (No finding)
- Cookie/session configuration: `web.xml` sets `<session-timeout>30</session-timeout>`. Cookie flags (`Secure`, `HttpOnly`, `SameSite`) are not configured in `web.xml` and are out of scope for this individual action file; they should be addressed at the container/deployment level.
- CORS: Not applicable to a Struts 1.x action; no `@CrossOrigin`. (No finding)
- Security response headers (`X-Frame-Options`, etc.): Not set by this action; this is a container/filter concern out of scope for this file.

### 5. Data Exposure
**Result: No findings directly in this file; see notes.**

- Operator/operator PII in logs: The action itself logs nothing. The DAO logs `"Inside LoginDAO Method : addUserSubscription"` at INFO, which does not include PII.
- Error handling: Unhandled exceptions (e.g., from `Integer.parseInt`) may propagate to the global error handler. The `web.xml` error page (`/error/error.html`) appears to be a static HTML file, which reduces stack trace exposure risk. However the global exception handler in struts-config.xml does not cover `NumberFormatException` (noted in Finding 5).
- Alert/subscription data scoping: The `getAlertList()` and `getReportList()` calls return the full unscoped list of all subscriptions from the `subscription` table, not filtered by company. Depending on whether subscriptions are global or company-specific, this could expose subscription types that should not be visible to all users. This is an INFO-level data exposure concern dependent on the data model.

### 6. Dependencies
**Result: Not applicable to this individual Java source file.**
Dependency review is a pom.xml-level concern. Not assessed here.

### 7. Build and CI
**Result: Not applicable to this individual Java source file.**
Build and CI review is a project-level concern. Not assessed here.
