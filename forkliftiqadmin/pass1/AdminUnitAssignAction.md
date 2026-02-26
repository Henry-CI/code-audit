# Security Audit Report: AdminUnitAssignAction.java

**Audit Run:** audit/2026-02-26-01
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Pass 1 automated review
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet auth gate, no Spring Security

---

## 1. Reading Evidence

### Package and Class

- **File:** `src/main/java/com/action/AdminUnitAssignAction.java`
- **Package:** `com.action`
- **Class:** `AdminUnitAssignAction extends PandoraAction`
- **PandoraAction base:** `src/main/java/com/action/PandoraAction.java` — extends `org.apache.struts.action.Action`; provides `getRequestParam`, `getSessionAttribute`, `getLongSessionAttribute`, `getCompId` helpers. **No authentication checks in base class.**

### Public / Protected Methods

| Line | Signature | Notes |
|------|-----------|-------|
| 20 | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | Single entry point; dispatches on `action` request parameter |
| 65 | `private void writeJsonResponse(HttpServletResponse, String)` | Writes raw string to response body; no Content-Type set |

### DAOs / Services Called

| Call Site (Action line) | DAO Method | SQL / Mechanism |
|-------------------------|-----------|-----------------|
| 44 | `UnitDAO.isAssignmentOverlapping(unit_id, start, end)` | Parameterised (`?`) — safe |
| 52 | `UnitDAO.deleteAssignment(id)` | Parameterised (`?`) — safe |
| 55 | `UnitDAO.addAssignment(company_id, unit_id, start, end, dateFormat)` | Parameterised (`?`) — safe |
| 59 | `UnitDAO.getAllUnitsByCompanyId(companyId)` | Uses `UnitsByCompanyIdQuery` builder — safe |

### Form Class

- **Form bean name:** `adminUnitAssignForm`
- **Class:** `com.actionform.AdminUnitAssignForm`
- **Fields:** `id` (String), `unit_id` (String), `company_id` (String), `start` (String), `end` (String)
- Generated via Lombok `@Data @NoArgsConstructor`; no validation annotations; no Struts `validate()` override.

### Struts-config Mappings

Two mappings reference `AdminUnitAssignAction`:

#### Mapping 1 — `/adminunitassign` (struts-config.xml lines 343-351)

```xml
<action
    path="/adminunitassign"
    name="adminUnitAssignForm"
    scope="request"
    type="com.action.AdminUnitAssignAction"
    validate="true"
    input="UnitEditDefinition">
  <forward name="success" path="adminEquipmentDefinition"/>
  <forward name="failure" path="adminEquipmentDefinition"/>
</action>
```

- `validate="true"` — triggers Struts validator, but **`adminUnitAssignForm` has no entry in `validation.xml`** (only `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm` are defined). Validation therefore produces no errors and passes unconditionally.
- No `roles` attribute — no declarative role restriction.
- `scope="request"`.

#### Mapping 2 — `/assigndatesvalid` (struts-config.xml lines 374-379)

```xml
<action
    path="/assigndatesvalid"
    name="adminUnitAssignForm"
    scope="request"
    type="com.action.AdminUnitAssignAction"
    validate="false">
</action>
```

- `validate="false"` — Struts validator is explicitly disabled.
- No `roles` attribute.
- No `<forward>` elements — a successful `"validate"` action path can only `return null` (JSON write) or fall through to `mapping.findForward("success")` which would cause a null forward and a 500 error on the second mapping.

---

## 2. Findings

---

### FINDING-01 — CRITICAL: IDOR on `delete` — Assignment ID Not Verified Against Session Company

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminUnitAssignAction.java`
**Line:** 52

**Description:**
The `delete` case accepts a raw `id` parameter from the HTTP request and deletes the corresponding `unit_company` row without any check that the assignment belongs to the authenticated user's company. An authenticated user from Company A can delete assignments belonging to Company B by supplying a foreign assignment `id`.

**Evidence:**

```java
// Line 24-25: id comes directly from request parameter, no validation
String id = getRequestParam(request, "id", "");

// Line 52: deleted unconditionally — no ownership check
case "delete":
    UnitDAO.deleteAssignment(id);
    break;
```

`UnitDAO.deleteAssignment` (UnitDAO.java line 80-89):
```java
private static final String DELETE_UNIT_ASSIGNMENT = "delete from unit_company where id = ?";

public static void deleteAssignment(String id) throws SQLException {
    DBUtil.updateObject(DELETE_UNIT_ASSIGNMENT,
            ps -> ps.setInt(1, Integer.parseInt(id)));
}
```

The DELETE query contains no `company_id` filter. The action reads `sessCompId` on line 23 and derives `companyId` on line 26, but neither value is passed into the delete operation.

**Recommendation:**
Modify `UnitDAO.deleteAssignment` to accept the authenticated `companyId` as an additional parameter and add a `AND company_id = ?` constraint to the DELETE statement:
```sql
DELETE FROM unit_company WHERE id = ? AND company_id = ?
```
Pass `companyId` (derived from `sessCompId`) as the second bind parameter. Validate the assignment record exists and belongs to the session company before executing the delete; return an error if not found.

---

### FINDING-02 — CRITICAL: IDOR on `add` — `company_id` Taken from Form, Not Session

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminUnitAssignAction.java`
**Line:** 55

**Description:**
The `add` case passes `form.getCompany_id()` — a value under the attacker's control submitted in the HTTP request body — directly to `UnitDAO.addAssignment`. An attacker can supply any `company_id` value and create assignments attributed to another company. Likewise, `form.getUnit_id()` is taken from the form without verifying that the referenced unit belongs to the session company, enabling cross-company unit assignment.

**Evidence:**

```java
// Line 55: form.getCompany_id() comes from HTTP request, not session
case "add":
    UnitDAO.addAssignment(form.getCompany_id(), form.getUnit_id(),
                          form.getStart(), form.getEnd(), dateFormat);
    break;
```

`AdminUnitAssignForm` fields (AdminUnitAssignForm.java lines 12-16):
```java
private String id;
private String unit_id;
private String company_id;   // user-controlled
private String start;
private String end;
```

The session-derived `companyId` (line 26) is available in scope but is never used for the `add` path.

**Recommendation:**
Ignore `form.getCompany_id()` entirely. Use `sessCompId` (the session-derived value) as the `company_id` argument:
```java
UnitDAO.addAssignment(sessCompId, form.getUnit_id(), form.getStart(), form.getEnd(), dateFormat);
```
Additionally, verify that the `unit_id` supplied by the form belongs to the session company before performing the insert (query `unit` table with `WHERE id = ? AND comp_id = ?`).

---

### FINDING-03 — CRITICAL: IDOR on `validate` — `unit_id` Overlap Check Not Scoped to Session Company

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminUnitAssignAction.java`
**Line:** 44

**Description:**
The `validate` action calls `UnitDAO.isAssignmentOverlapping(form.getUnit_id(), ...)` using a `unit_id` from the form without verifying that the unit belongs to the session company. An attacker can probe whether any arbitrary unit ID in the database has overlapping assignments, leaking scheduling information for units across all companies.

**Evidence:**

```java
// Line 44: form.getUnit_id() is user-controlled; no company ownership check
if (UnitDAO.isAssignmentOverlapping(form.getUnit_id(), start, end)) {
    writeJsonResponse(response, "Assignment is overlapping with another one");
    return null;
}
```

`QUERY_ASSIGN_DATE_OVERLAP_CHECK` (UnitDAO.java lines 91-96):
```sql
SELECT count(id) FROM unit_company
WHERE ((? BETWEEN start_date AND end_date) OR
       (? BETWEEN start_date AND end_date) OR
       end_date IS NULL AND start_date <= ?) AND
      unit_id = ?
```

No `company_id` filter exists in this query.

**Recommendation:**
Before calling `isAssignmentOverlapping`, verify that the `unit_id` from the form corresponds to a unit whose `comp_id` matches `sessCompId`. Alternatively, add a `company_id` parameter to `isAssignmentOverlapping` and include `AND company_id = ?` in the query.

---

### FINDING-04 — HIGH: No CSRF Protection

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitAssignAction.java` (all mutation paths)
**Lines:** 52 (delete), 55 (add)

**Description:**
The application uses Apache Struts 1.3.10 with no CSRF framework (no Spring Security, no custom token mechanism visible). Both the `add` and `delete` operations are state-changing and are reachable via a standard POST (Struts maps both GET and POST through the same `doGet`/`doPost` chain in `PreFlightActionServlet`). Any page on any origin can submit a cross-site form to `/adminunitassign.do?action=delete&id=<N>` or `action=add` and the request will be processed provided the victim's session cookie is sent by the browser.

**Evidence:**
- No CSRF token field in `AdminUnitAssignForm` (AdminUnitAssignForm.java).
- No CSRF token check in `execute()`.
- `PreFlightActionServlet.doPost` unconditionally delegates to `doGet` with no origin/referer check (PreFlightActionServlet.java line 94-96).
- Stack declaration confirms: "CSRF = structural gap."

**Recommendation:**
Implement a synchroniser token pattern: generate a per-session or per-form token, store it in the session, embed it as a hidden field in every state-changing form, and verify it at the start of `execute()` before processing any `action` other than read-only `validate`. A Struts 1 compatible implementation can be placed in `PandoraAction` as a shared utility method.

---

### FINDING-05 — HIGH: Missing Input Validation — No Struts Validator Rules for `adminUnitAssignForm`

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/validation.xml`
**Lines:** 18-69 (entire file — `adminUnitAssignForm` is absent)

**Description:**
The struts-config mapping for `/adminunitassign` declares `validate="true"`, which causes Struts to invoke the Commons Validator framework before calling `execute()`. However, `validation.xml` contains no `<form name="adminUnitAssignForm">` entry. As a result, validation passes with zero errors for all submissions. Fields `id`, `unit_id`, `company_id`, `start`, and `end` receive no server-side type, length, or format constraints from the framework.

**Evidence:**
`validation.xml` defines three forms:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

`adminUnitAssignForm` is not present. The form bean class `AdminUnitAssignForm` has no `validate()` override and no constraint annotations.

**Recommendation:**
Add a `<form name="adminUnitAssignForm">` block to `validation.xml` enforcing at minimum:
- `unit_id`: required, integer
- `id`: integer (for delete path)
- `start`: required, valid date format
- `end`: optional, valid date format when present

Also implement server-side business rule validation in the action (or a dedicated validator) to reject non-numeric values for `id`, `unit_id`, and `company_id` before they reach DAO calls.

---

### FINDING-06 — HIGH: Null Pointer Dereference if `sessCompId` is Null — Auth Bypass via Missing Session Attribute

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitAssignAction.java`
**Lines:** 23, 26

**Description:**
The action reads `sessCompId` from the session on line 23 and immediately calls `Integer.parseInt(sessCompId)` on line 26 with no null check. `PreFlightActionServlet` only sets the `forward = true` redirect when `excludeFromFilter(path)` returns `true` AND the session is null or `sessCompId` is null/empty. The servlet's `excludeFromFilter` returns `true` for `/adminunitassign.do`, so the guard is active. However, there is a race window: if `sessCompId` is removed from the session after the PreFlight check (e.g., concurrent logout, session manipulation, or a bug in another action) and before line 23 executes, a `NullPointerException` is thrown on line 26. Struts' global exception handler forwards to `errorDefinition`, which may leak stack trace information depending on configuration.

More critically: the `/assigndatesvalid` mapping is a separate action path. Although it routes to the same class, the action's line 22 reads `sessDateFormat` and line 23 reads `sessCompId` with the same parse pattern. Any scenario that bypasses PreFlight (e.g., direct dispatcher forward from an unprotected resource) reaches line 26 without a null guard.

**Evidence:**

```java
// Line 23: no null guard
String sessCompId = (String) session.getAttribute("sessCompId");
// Line 26: NPE if sessCompId is null
int companyId = Integer.parseInt(sessCompId);
```

PandoraAction provides a `getCompId(session)` helper (PandoraAction.java line 41-43) but it is not used here. The action uses a direct attribute cast instead.

**Recommendation:**
Add an explicit null/empty check immediately after reading `sessCompId`. If null or empty, invalidate the session and redirect to the login/expire page rather than proceeding:
```java
if (sessCompId == null || sessCompId.isEmpty()) {
    response.sendRedirect(request.getContextPath() + "/expire.do");
    return null;
}
```
This mirrors the PreFlight guard and closes the race window.

---

### FINDING-07 — MEDIUM: `writeJsonResponse` Does Not Set `Content-Type` Header

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitAssignAction.java`
**Lines:** 65-68

**Description:**
`writeJsonResponse` writes a plain string to the response body (either a JSON-like primitive `"true"` or a plain English error string) without calling `response.setContentType("application/json")` or `response.setCharacterEncoding(...)`. The browser will receive the response with whatever content type the container defaults to (typically `text/html`). Returning text/html for a JSON endpoint enables reflected content injection: if any part of the response value were ever to include user-controlled input, the browser would render it as HTML, creating a reflected XSS vector. Even without injection, the missing content-type is a protocol violation and can cause client-side parsing errors.

**Evidence:**

```java
// Lines 65-68: no Content-Type set
private void writeJsonResponse(HttpServletResponse response, String result) throws IOException {
    response.getWriter().write(result);
    response.getWriter().flush();
}
```

The response strings are currently hard-coded literals, so XSS is not currently exploitable through this specific method. However, the pattern is unsafe and represents a maintenance risk.

**Recommendation:**
Set content type before writing:
```java
response.setContentType("application/json; charset=UTF-8");
response.getWriter().write(result);
response.getWriter().flush();
```
Also ensure the response is not committed before this call. Consider using a JSON serialisation library rather than raw string writes.

---

### FINDING-08 — MEDIUM: No Role-Based Access Control on Either Mapping

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/struts-config.xml`
**Lines:** 343-351, 374-379

**Description:**
Neither the `/adminunitassign` nor `/assigndatesvalid` action mapping declares a `roles` attribute. In Struts 1 the `roles` attribute on an `<action>` element causes the framework to check `HttpServletRequest.isUserInRole()` before dispatching. Without it, any authenticated session (regardless of role) can perform unit assignment add/delete operations. This is an administrative function; it should be restricted to users with a specific administrative role.

**Evidence:**
```xml
<!-- No roles= attribute on either mapping -->
<action path="/adminunitassign"
        name="adminUnitAssignForm"
        scope="request"
        type="com.action.AdminUnitAssignAction"
        validate="true"
        input="UnitEditDefinition">
```

**Recommendation:**
Add a `roles` attribute to restrict the action to appropriate administrative roles, e.g.:
```xml
<action path="/adminunitassign"
        roles="ROLE_ADMIN"
        ...>
```
Ensure the role is also enforced programmatically inside `execute()` as defence in depth, since Struts role checking depends on container-managed security being properly wired.

---

### FINDING-09 — LOW: `NumberFormatException` Not Handled for `id`, `unit_id`, `company_id`

**Severity:** LOW
**File:** `src/main/java/com/action/AdminUnitAssignAction.java`
**Lines:** 26, 52, 55 (indirectly through DAO at UnitDAO.java lines 83, 57, 110)

**Description:**
`Integer.parseInt(sessCompId)` on line 26 and `Integer.parseInt(id)` inside `UnitDAO.deleteAssignment` (UnitDAO.java line 83) and `Integer.parseInt(unitId)` inside `UnitDAO.isAssignmentOverlapping` (UnitDAO.java line 110) will throw `NumberFormatException` if non-numeric input is supplied. `NumberFormatException` is not `SQLException` or `IOException` and is not caught by the global exception handlers declared in struts-config.xml (which only handle `java.sql.SQLException`, `java.io.IOException`, `javax.servlet.ServletException`). An unhandled `NumberFormatException` propagates as a 500 error, potentially exposing a stack trace to the client depending on the server error page configuration.

**Evidence:**

```java
// Action line 26 — unchecked parse
int companyId = Integer.parseInt(sessCompId);

// UnitDAO.java line 83 — unchecked parse of user-supplied id
ps -> ps.setInt(1, Integer.parseInt(id))

// UnitDAO.java line 110 — unchecked parse of user-supplied unitId
stmt.setInt(4, Integer.parseInt(unitId));
```

struts-config.xml global exceptions (lines 43-55) do not include `java.lang.NumberFormatException` or `java.lang.RuntimeException`.

**Recommendation:**
Validate that `id`, `unit_id`, and `company_id` are non-null, non-empty, and numeric before performing `parseInt`. Reject the request with an appropriate error response if validation fails. Add `NumberFormatException` or a broader `RuntimeException` entry to the global exception handler, or handle it inside the action's `execute()` method.

---

### FINDING-10 — INFO: Second Struts Mapping (`/assigndatesvalid`) Has No Forwards Defined

**Severity:** INFO
**File:** `src/main/webapp/WEB-INF/struts-config.xml`
**Lines:** 374-379

**Description:**
The `/assigndatesvalid` mapping has no `<forward>` children. The `validate` action branch returns `null` after writing the JSON response, which is correct. However, if the `action` parameter in a request to `/assigndatesvalid` is anything other than `"validate"` (e.g., `"add"`, `"delete"`, or empty string), execution falls through the switch to the final `mapping.findForward("success")` call. Because the mapping has no `"success"` forward, `findForward` returns `null`, causing Struts to throw a `NullPointerException` or log a warning and produce a 500 response. This is a robustness issue and a minor information leak vector.

**Recommendation:**
Either restrict the `/assigndatesvalid` endpoint to only accept `action=validate` (returning an error response for any other value), or add a `<forward name="success">` pointing to a sensible destination as a fallback.

---

## 3. Category Summary

| Category | Status | Findings |
|----------|--------|----------|
| Authentication (sessCompId check) | ISSUE | FINDING-06: No null guard before `Integer.parseInt(sessCompId)` |
| Role Check | ISSUE | FINDING-08: No `roles` attribute on either mapping |
| CSRF | ISSUE | FINDING-04: No token mechanism |
| Input Validation | ISSUE | FINDING-05: No `validation.xml` entry for `adminUnitAssignForm` |
| SQL Injection | NO ISSUES | All three DAO methods used by this action (`deleteAssignment`, `addAssignment`, `isAssignmentOverlapping`) use parameterised PreparedStatement placeholders. Note: other methods in UnitDAO.java (e.g., `getUnitBySerial`, `getUnitNameByComp`, `getType`) use string concatenation and are HIGH-risk, but they are not called from this action. |
| IDOR | ISSUE | FINDING-01 (delete), FINDING-02 (add company_id), FINDING-03 (validate unit_id) |
| Session Handling | ISSUE | FINDING-06 (NPE race), FINDING-02 (form company_id overrides session) |
| Data Exposure | ISSUE | FINDING-07 (missing Content-Type), FINDING-09 (500/stack trace on NFE) |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 3 | FINDING-01, FINDING-02, FINDING-03 |
| HIGH | 3 | FINDING-04, FINDING-05, FINDING-06 |
| MEDIUM | 2 | FINDING-07, FINDING-08 |
| LOW | 1 | FINDING-09 |
| INFO | 1 | FINDING-10 |
| **Total** | **10** | |
