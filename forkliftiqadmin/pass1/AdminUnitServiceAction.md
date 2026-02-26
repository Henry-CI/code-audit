# Security Audit: AdminUnitServiceAction.java
**Audit Run:** audit/2026-02-26-01
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet auth gate, no Spring Security

---

## 1. Reading Evidence

### 1.1 Package and Class

- **File:** `src/main/java/com/action/AdminUnitServiceAction.java`
- **Package:** `com.action`
- **Class:** `AdminUnitServiceAction extends org.apache.struts.action.Action`

### 1.2 Public / Protected Methods

| Line | Signature |
|------|-----------|
| 21 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

No other public or protected methods are declared in this class.

### 1.3 DAOs / Services Called

| Call Site (Action) | DAO Method | File |
|--------------------|------------|------|
| Line 61 | `UnitDAO.getInstance().saveService(serviceBean)` | `src/main/java/com/dao/UnitDAO.java` line 699 |

No other DAO or service calls are made by this action.

### 1.4 Form Class

- **Form bean name (struts-config):** `adminUnitServiceForm`
- **Form class:** `com.actionform.AdminUnitServiceForm`
- **File:** `src/main/java/com/actionform/AdminUnitServiceForm.java`
- **Fields bound from request:**
  - `int id`
  - `int unitId` — the primary key used to address the `unit_service` record
  - `int servLast`
  - `int servNext`
  - `int servDuration`
  - `double accHours`
  - `double hourmeter`
  - `String action`
  - `String servType`
  - `String servStatus`

### 1.5 Struts-Config Mapping

From `src/main/webapp/WEB-INF/struts-config.xml`, lines 491–499:

```xml
<action
        path="/adminunitservice"
        name="adminUnitServiceForm"
        scope="request"
        type="com.action.AdminUnitServiceAction"
        validate="true"
        input="UnitServiceDefinition">
    <forward name="success" path="UnitServiceDefinition"/>
    <forward name="failure" path="UnitServiceDefinition"/>
</action>
```

| Attribute | Value |
|-----------|-------|
| path | `/adminunitservice` |
| scope | `request` |
| validate | `true` |
| roles | _(not specified — no `roles` attribute present)_ |
| input (on validation failure) | `UnitServiceDefinition` |

### 1.6 Validation.xml Coverage

`src/main/webapp/WEB-INF/validation.xml` defines rules for exactly three forms:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

`adminUnitServiceForm` has **no entry** in `validation.xml`. Despite `validate="true"` in struts-config, the Struts Validator plug-in will apply no constraints because no `<form name="adminUnitServiceForm">` block exists.

### 1.7 UnitDAO.saveService Summary

`UnitDAO.saveService` (lines 699–759) uses `PreparedStatement` with positional parameters for both the `INSERT` and `UPDATE` paths. The query key is `unit_id` supplied directly from `serviceBean.getUnitId()`, which in turn is set from the form field `serviceForm.getUnitId()` (Action line 52). No company-ownership check is performed anywhere in the call chain.

---

## 2. Findings

---

### FINDING-01 — CRITICAL: Insecure Direct Object Reference (IDOR) — No Ownership Verification on unitId

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminUnitServiceAction.java`, line 52
**Also implicates:** `src/main/java/com/dao/UnitDAO.java`, lines 699–758

**Description:**
The `unitId` value is taken directly from the submitted form (`serviceForm.getUnitId()`, line 52) and passed without modification into `UnitDAO.saveService()`. The DAO performs no check that the unit belongs to the company identified by the session attribute `sessCompId`. An authenticated user (any company) can supply an arbitrary `unitId` in the POST body to overwrite the service schedule of a unit belonging to a different company.

**Evidence:**
```java
// AdminUnitServiceAction.java line 52
serviceBean.setUnitId(serviceForm.getUnitId());
// ...
UnitDAO.getInstance().saveService(serviceBean);  // line 61
```

```java
// UnitDAO.java lines 710-745 — saveService uses only unit_id, no comp_id join
String sql = "select count(unit_id) from unit_service where unit_id=?";
// ...
sql = "update unit_service set ... where unit_id=?";
```

The `unit` table has a `comp_id` column (evident from other DAO methods, e.g., `QUERY_COUNT_UNIT_BY_NAME`, line 117). The `saveService` method never queries or checks it.

**Recommendation:**
Before executing the save, verify that the unit identified by `unitId` belongs to `sessCompId`. A pre-save query such as `SELECT comp_id FROM unit WHERE id = ?` should be compared against `sessCompId`. Alternatively, add a `comp_id` predicate to the UPDATE/INSERT check: `SELECT count(unit_id) FROM unit_service us JOIN unit u ON us.unit_id = u.id WHERE us.unit_id = ? AND u.comp_id = ?`.

---

### FINDING-02 — HIGH: No Role-Based Access Control on the Action Mapping

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 491–499

**Description:**
The `/adminunitservice` action mapping carries no `roles` attribute. Struts 1 supports declarative role enforcement via `roles="ROLE_ADMIN"` on the `<action>` element. Without it, any authenticated session — regardless of whether the user is a regular operator, driver-level user, or admin — can call this endpoint and modify service records. The PreFlightActionServlet only verifies that `sessCompId` is non-null (a presence check), not that the caller holds an administrative role.

**Evidence:**
```xml
<action
        path="/adminunitservice"
        name="adminUnitServiceForm"
        scope="request"
        type="com.action.AdminUnitServiceAction"
        validate="true"
        input="UnitServiceDefinition">
```
No `roles` attribute is present.

**Recommendation:**
Add `roles="ROLE_ADMIN"` (or the appropriate application role constant) to the action mapping. Additionally, enforce a programmatic role check inside `execute()` by reading a role attribute from the session and returning early if the caller is not an admin.

---

### FINDING-03 — HIGH: Missing CSRF Protection

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitServiceAction.java` (entire execute method)
**Also implicates:** `src/main/webapp/WEB-INF/struts-config.xml`, line 491

**Description:**
There is no CSRF token mechanism in this action or anywhere in the Struts configuration for this endpoint. The scope is `request` (not `session`), so no session-scoped form token is retained across requests. Struts 1.3 provides `org.apache.struts.action.Action.isTokenValid()` / `saveToken()` helpers, but neither is used here. A cross-site request forgery attack from any page on the internet can cause an authenticated admin's browser to POST to `/adminunitservice.do` and alter service schedules. Combined with FINDING-01, a CSRF attack can also target units across company boundaries.

**Evidence:**
No call to `isTokenValid(request)` appears anywhere in `AdminUnitServiceAction.java`. The stack note confirms "CSRF = structural gap."

**Recommendation:**
Implement the Struts synchronizer token pattern: call `saveToken(request)` when rendering the service form, and call `isTokenValid(request, true)` at the start of `execute()`. Reject the request and invalidate if the check fails. As a defence-in-depth measure, require a `SameSite=Strict` or `SameSite=Lax` cookie attribute on the session cookie.

---

### FINDING-04 — HIGH: No Server-Side Input Validation — validate="true" Is Inert for This Form

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/validation.xml` (absence of `adminUnitServiceForm` block)
**Also implicates:** `src/main/webapp/WEB-INF/struts-config.xml`, line 495; `src/main/java/com/action/AdminUnitServiceAction.java`, lines 36–59

**Description:**
`validate="true"` is declared in struts-config, which tells Struts to invoke the Validator framework for `adminUnitServiceForm` before calling `execute()`. However, `validation.xml` contains no `<form name="adminUnitServiceForm">` block. The Validator plug-in therefore applies zero constraints; `validate="true"` is functionally equivalent to `validate="false"` for this action. The action code performs no manual validation of any field. Consequently:

- `servType` (a `String`) is accepted with any value, including null or empty string, which feeds into the `equalsIgnoreCase` branch at line 36 — a null `servType` would throw a `NullPointerException`, bypassing the action logic entirely rather than producing a controlled error response.
- Numeric fields (`servDuration`, `servNext`, `accHours`) are not range-checked. Negative or extreme values produce nonsensical `serviceRemain` and `serviceStatus` calculations (lines 37–50) that are persisted to the database.
- `unitId` is not validated to be a positive integer.
- There is no check that `accHours` is non-negative or within a plausible machine-hours range.

**Evidence:**
```java
// Line 36 — servType used without null check
if (serviceForm.getServType().equalsIgnoreCase("setIntval") || ...)
```
```xml
<!-- validation.xml — only three forms defined, adminUnitServiceForm absent -->
<form name="loginActionForm"> ... </form>
<form name="adminRegisterActionForm"> ... </form>
<form name="AdminDriverEditForm"> ... </form>
```

**Recommendation:**
Add a `<form name="adminUnitServiceForm">` block to `validation.xml` with `required` and `integer`/`double` rules for `unitId`, `servDuration`, `servNext`, `servLast`, and `accHours`, and a `required` rule for `servType`. Additionally add a manual null guard for `servType` in the action before line 36. Define and enforce a whitelist of valid `servType` values (`setIntval`, `setDur`, and the third branch type) rather than relying solely on string comparison.

---

### FINDING-05 — MEDIUM: NullPointerException Risk via Unvalidated servType

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitServiceAction.java`, line 36

**Description:**
`serviceForm.getServType()` is called directly with `.equalsIgnoreCase(...)` with no null guard. If a request is submitted with no `servType` parameter (or with the form field absent), Struts populates the form bean with the default Java value of `null` for `String`. The `equalsIgnoreCase` call will throw a `NullPointerException` at runtime. Although this results in a caught exception (the global `java.sql.SQLException` exception handler in struts-config does not cover `NullPointerException`, so it would propagate up as a 500), it leaks an unhandled error path and may expose stack trace information.

**Evidence:**
```java
// Line 36
if (serviceForm.getServType().equalsIgnoreCase("setIntval") || serviceForm.getServType().equalsIgnoreCase("setDur")) {
```
No null check precedes this call.

**Recommendation:**
Apply a null-and-blank check before line 36:
```java
String servType = serviceForm.getServType();
if (servType == null || servType.isEmpty()) {
    // add error and return mapping.findForward("failure");
}
```
Or use `"setIntval".equalsIgnoreCase(servType)` (Yoda style) to at least prevent NPE, and add a validation rule in `validation.xml` marking `servType` as `required`.

---

### FINDING-06 — MEDIUM: Redundant and Unreachable Null Check on `action` Variable

**Severity:** MEDIUM (Logic / Defensive-Coding Defect)
**File:** `src/main/java/com/action/AdminUnitServiceAction.java`, lines 23–29

**Description:**
The ternary expression at line 23 guarantees `action` is never null (it is assigned `""` if `request.getParameter("action")` returns null). The subsequent check `if (action == null || action.equals(""))` at line 27 is therefore unreachable for the null branch, but it still re-assigns `action` from `serviceForm.getAction()`. If `serviceForm.getAction()` itself returns null (a common default for unset String fields in a Struts form bean), then `action` becomes null after line 28, and the call `action.equalsIgnoreCase("saveservice")` at line 31 will throw a `NullPointerException`. The developer likely intended to fall back to the form-bean's action only when the request parameter was absent, but the logic creates a silent null-propagation path.

**Evidence:**
```java
// Line 23 — action is guaranteed non-null here
String action = request.getParameter("action") == null ? "" : request.getParameter("action");

// Line 27-29 — the null branch of the outer if is dead, but the reassignment on line 28
// can introduce null if serviceForm.getAction() returns null
if (action == null || action.equals("")) {
    action = serviceForm.getAction();  // may be null
}

// Line 31 — NPE if action is null after line 28
if (action.equalsIgnoreCase("saveservice")) {
```

**Recommendation:**
Consolidate the action resolution:
```java
String action = request.getParameter("action");
if (action == null || action.isEmpty()) {
    action = serviceForm.getAction();
}
if (action == null) {
    action = "";
}
```
Then use `"saveservice".equalsIgnoreCase(action)` to eliminate the NPE risk.

---

### FINDING-07 — LOW: serviceBean Placed in Request Scope and Forwarded — Potential Data Leakage via Forwarded JSP

**Severity:** LOW
**File:** `src/main/java/com/action/AdminUnitServiceAction.java`, lines 63–64

**Description:**
`serviceBean` is placed into request scope and the request is forwarded to `UnitServiceDefinition`. The bean contains computed values (`hoursTillNextService`, `servStatus`) derived from user-supplied inputs. If the target JSP renders `serviceBean` attributes without escaping, this is a potential reflected cross-site scripting (XSS) vector if any String field (e.g., `servType`, `servStatus`) is rendered directly into HTML. The `servStatus` field is set to one of three hard-coded strings in the action (line 42–50), so XSS via `servStatus` is not currently possible. However `servType` originates entirely from user input and is stored in the bean; if the JSP renders it unescaped, XSS is possible. This is rated LOW here because the vector depends on the JSP rendering behaviour, which is outside this file's scope, but it is recorded as a finding to prompt JSP review.

**Evidence:**
```java
// Line 59
serviceBean.setServType(serviceForm.getServType());  // raw user input stored in bean
// Line 63
request.setAttribute("serviceBean", serviceBean);
// Line 64
return mapping.findForward("success");  // forwarded to UnitServiceDefinition JSP
```

**Recommendation:**
Ensure the `UnitServiceDefinition` JSP uses `<c:out value="${serviceBean.servType}" escapeXml="true"/>` or equivalent escaping for all bean attributes rendered in HTML. Consider not forwarding the raw user-supplied `servType` back to the view; use the freshly-read DB record instead.

---

### FINDING-08 — INFO: SQL Injection in UnitDAO (Other Methods) — Not Directly Exploitable via This Action

**Severity:** INFO (context note — not directly triggered by this action)
**File:** `src/main/java/com/dao/UnitDAO.java`

**Description:**
The `saveService` method called by this action uses `PreparedStatement` throughout (lines 711–744) and is not vulnerable to SQL injection. However, several other methods in the same DAO file contain raw string concatenation into SQL that is relevant to the overall `UnitDAO` risk surface:

- `getUnitBySerial` (line 212): `"select id,comp_id from unit where serial_no = '" + serial_no + "'"` — direct concatenation, SQL injection if `serial_no` is attacker-controlled.
- `getUnitNameByComp` (line 311): `"select id,name from unit where comp_id in (" + compLst + ")"` — `compLst` is assembled from `cDAO.getSubCompanyLst(compId)`.
- `getTotalUnitByID` (line 548): similar `compLst` pattern.
- `delUnitById` (line 349): `"update unit set active = false where id=" + id` — direct integer concatenation without `PreparedStatement`.
- `getType` (line 627): `" where manu_id = " + manu_id` — direct concatenation.
- `getPower` (lines 666–671): `" where manu_id = " + manu_id` and `" and type_id= " + type_id` — direct concatenation.

These are recorded here for completeness. They are not exercised by `AdminUnitServiceAction` but share the same DAO class and are in scope for the overall repository audit.

**Recommendation:**
Convert all raw string-concatenation SQL in `UnitDAO` to `PreparedStatement` parameter binding. In particular `delUnitById`, `getType`, and `getPower` should be prioritised as they operate on less-trusted input paths.

---

## 3. Category Summary

| Category | Verdict |
|----------|---------|
| Authentication (sessCompId gate) | Gate is present (PreFlightActionServlet checks `sessCompId != null`). The action itself performs no additional session checks — accepted as covered by the servlet gate. No direct bypass identified within this file. |
| Role-Based Access Control | **ISSUE — see FINDING-02.** No `roles` attribute; no programmatic role check. |
| CSRF | **ISSUE — see FINDING-03.** No token validation. |
| Input Validation | **ISSUE — see FINDING-04, FINDING-05, FINDING-06.** `validation.xml` entry absent; manual validation absent; NPE risk. |
| SQL Injection (this action's DAO path) | NO ISSUES. `saveService` uses `PreparedStatement` throughout. |
| IDOR / Tenant Isolation | **ISSUE — see FINDING-01.** `unitId` not validated against session company. |
| Session Handling | No session manipulation or creation in this action. Gate relies on existing session. No issues within this file. |
| Data Exposure | **ISSUE (LOW) — see FINDING-07.** Raw user input forwarded in request bean; JSP rendering risk. |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | FINDING-01 |
| HIGH | 3 | FINDING-02, FINDING-03, FINDING-04 |
| MEDIUM | 2 | FINDING-05, FINDING-06 |
| LOW | 1 | FINDING-07 |
| INFO | 1 | FINDING-08 |
| **TOTAL** | **8** | |
