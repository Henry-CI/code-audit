# Security Audit Report — AdminOperatorAction.java

**Audit run:** audit/2026-02-26-01
**Branch:** master
**Auditor:** Claude Sonnet 4.6 (automated pass 1)
**Date:** 2026-02-26

---

## 1. Reading Evidence

### 1.1 Package and Class

| Item | Value |
|------|-------|
| File | `src/main/java/com/action/AdminOperatorAction.java` |
| Package | `com.action` |
| Class | `AdminOperatorAction extends PandoraAction` |
| Parent | `PandoraAction extends org.apache.struts.action.Action` |
| Annotations | `@Slf4j` (Lombok) |

### 1.2 Public / Protected Methods with Line Numbers

| Line | Visibility | Signature |
|------|-----------|-----------|
| 22 | `public` | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` |
| 63 | `private` | `editAction(HttpServletRequest, Long driverId) throws Exception` |
| 68 | `private` | `editUserAction(HttpServletRequest, Long driverId, String sessionToken) throws Exception` |
| 74 | `private` | `addAction(HttpServletRequest, String compId) throws SQLException` |
| 93 | `private` | `addUserAction(HttpServletRequest, String compId) throws SQLException` |
| 106 | `private` | `trainingAction(HttpServletRequest, Long driverId, String compId, String dateFormat) throws Exception` |
| 115 | `private` | `subscriptionAction(HttpServletRequest, Long driverId, String sessionToken) throws Exception` |
| 123 | `private` | `vehicleAction(HttpServletRequest, Long driverId, String compId) throws SQLException` |
| 134 | `private` | `deleteAction(HttpServletRequest, Long driverId, String compId, String dateFormat) throws Exception` |
| 140 | `private` | `deleteUserAction(HttpServletRequest, Long driverId, String compId, String sessionToken) throws Exception` |
| 146 | `private` | `inviteAction(HttpServletRequest, String compId)` |
| 153 | `private` | `searchAction(HttpServletRequest, String compId, String dateFormat, String search) throws Exception` |
| 161 | `private` | `searchUserAction(HttpServletRequest, String compId, String search, String sessionToken) throws Exception` |

### 1.3 DAOs / Services Called

| DAO / Service | Method(s) Called | Line(s) in Action |
|---------------|-----------------|-------------------|
| `DriverDAO` (static) | `getDriverById(driverId)` | 64 |
| `DriverDAO` (static) | `getUserById(driverId, sessionToken)` | 69, 116 |
| `DriverDAO` (static) | `getNextDriverId()` | 75 |
| `DriverDAO` (static) | `getNextUserId()` | 94 |
| `TrainingDAO` (instance) | `getTrainingByDriver(driverId, dateFormat)` | 108 |
| `ManufactureDAO` (singleton) | `getAllManufactures(compId)` | 109 |
| `UnitDAO` (singleton) | `getAllUnitType()`, `getAllUnitFuelType()` | 110–111 |
| `DriverUnitDAO` (static) | `getDriverUnitsByCompAndDriver(companyId, driverId)` | 128 |
| `CompanyDAO` (singleton) | `getUserAlert(String, String, String)` × 3 | 117–119 |
| `DriverDAO` (static) | `delDriverById(driverId, compId)` | 135 |
| `DriverDAO` (static) | `getAllDriver(compId, true, dateFormat)` | 136, 155 |
| `DriverDAO` (static) | `delUserById(driverId, sessionToken)` | 141 |
| `DriverDAO` (static) | `getAllUser(compId, sessionToken)` | 142, 163 |
| `DriverDAO` (static) | `getAllDriverSearch(compId, true, search, dateFormat, timezone)` | 156 |
| `DriverDAO` (static) | `getAllUserSearch(compId, search)` | 164 |

### 1.4 Form Class

No ActionForm is associated with this action. The struts-config mapping for `/admindriver` declares **no `name` attribute** (no form bean) and **no `validate` attribute**.

### 1.5 Struts-Config Mapping Details

Source file: `src/main/webapp/WEB-INF/struts-config.xml`, lines 233–244.

```xml
<action
        path="/admindriver"
        type="com.action.AdminOperatorAction">
    <forward name="operatoredit"       path="OperatorEditDefinition"/>
    <forward name="useredit"           path="UserEditDefinition"/>
    <forward name="operatortraining"   path="OperatorTrainingDefinition"/>
    <forward name="operatorsubscription" path="OperatorSubscriptionDefinition"/>
    <forward name="operatorvehicle"    path="OperatorVehicleDefinition"/>
    <forward name="operatorlist"       path="adminOperatorDefinition"/>
    <forward name="userlist"           path="adminUserDefinition"/>
    <forward name="operatorinvite"     path="OperatorInviteDefinition"/>
</action>
```

| Attribute | Value | Implication |
|-----------|-------|-------------|
| `name` (form bean) | **absent** | No ActionForm bound; all input arrives raw via `request.getParameter()` |
| `scope` | **absent** (defaults to `session`) | Struts default applies |
| `validate` | **absent** (defaults to `false` when no form) | No declarative validation runs |
| `roles` | **absent** | No Struts role-based access control declared |

---

## 2. Findings

---

### FINDING-01 — CRITICAL: Insecure Direct Object Reference (IDOR) — `editAction` fetches driver across company boundaries

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Line:** 64
**Also implicates:** `src/main/java/com/dao/DriverDAO.java` line 154–157

**Description:**
`editAction` calls `DriverDAO.getDriverById(driverId)` where `driverId` is taken directly from the HTTP request parameter at line 30. The underlying SQL query `QUERY_DRIVER_BY_ID` is:

```sql
select d.id, d.first_name, d.last_name, p.location, p.department, d.phone, p.enabled, d.email,'******'
from driver d
inner join permission p on d.id = p.driver_id
where d.id = ?
```

There is **no `comp_id` filter**. An authenticated user of Company A can enumerate any integer `driverId` and read the personal details (name, email, phone, location, department, app access flag) of drivers belonging to any other company. The password is masked (`'******'`) in this query, which is the only partial mitigation.

**Evidence:**
- `DriverDAO.java:154–157`: `QUERY_DRIVER_BY_ID` has no `comp_id` predicate.
- `AdminOperatorAction.java:30`: `driverId` sourced from raw request parameter.
- `AdminOperatorAction.java:63–65`: `editAction` passes that id directly to the DAO with no ownership check.

**Recommendation:**
Add `AND p.comp_id = ?` to `QUERY_DRIVER_BY_ID` and pass `sessCompId` as a second bound parameter. In the action, verify `driver.getComp_id().equals(sessCompId)` after retrieval and return HTTP 403 / redirect to the operator list if the check fails.

---

### FINDING-02 — CRITICAL: IDOR — `editUserAction` / `subscriptionAction` fetch user with no company scope

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Lines:** 69, 116
**Also implicates:** `src/main/java/com/dao/DriverDAO.java` lines 159–160

**Description:**
Both `editUserAction` and `subscriptionAction` call `DriverDAO.getUserById(driverId, sessionToken)`. The SQL constant `QUERY_USER_BY_ID` is:

```sql
select c.user_id, c.cognito_username
from users_cognito c
where c.user_id = ?
```

Again, **no company filter**. Any authenticated admin can access the Cognito profile and subscription alert data for users of other tenants by supplying a foreign `driverId`.

**Evidence:**
- `DriverDAO.java:159–160`: `QUERY_USER_BY_ID` contains no `comp_id` predicate.
- `AdminOperatorAction.java:68–70`, `115–121`: both call paths exercise this query with an attacker-controlled id.

**Recommendation:**
Join `users_cognito` to `user_comp_rel` and add a `comp_id = ?` predicate. Pass the session `sessCompId` as the second parameter. Validate ownership in the action layer before setting request attributes.

---

### FINDING-03 — CRITICAL: IDOR — `deleteAction` deletes driver with attacker-controlled `driverId`, company check is in SQL but not validated in application layer

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Lines:** 134–138
**Also implicates:** `src/main/java/com/dao/DriverDAO.java` line 60

**Description:**
`deleteAction` calls `DriverDAO.delDriverById(driverId, compId)`. The SQL `DELETE_DRIVER_BY_ID` is:

```sql
update permission set enabled = false where driver_id = ? and comp_id = ?
```

The `comp_id` is bound from `sessCompId`, which provides a SQL-level tenant guard for the delete itself. However, the action then immediately calls `DriverDAO.getAllDriver(compId, true, dateFormat)` (line 136) to refresh the list — this is safe. The more serious concern is that `driverId` is taken directly from the request (line 30) with no prior validation that the driver belongs to the session company **before** the delete call. If the DAO logic were ever changed (or if an attacker attempts to delete a driver from another company), the absence of an application-level ownership check means there is no defence-in-depth. Additionally, `delUserById` at line 141 (for `deleteUserAction`) deletes the Cognito user and wipes rows from `users_cognito` and `user_role_rel` using **only** the attacker-controlled `driverId` with no company filter anywhere in `DELETE_USER_BY_ID`:

```sql
update users set active = false where id = ?
```

**Evidence:**
- `DriverDAO.java:62–66`: `DELETE_USER_BY_ID`, `DELETE_USER_COGNITO_BY_ID`, `DELETE_USER_ROLE_REL` all filter on `id` only — no company scope.
- `AdminOperatorAction.java:140–143`: `deleteUserAction` passes attacker-controlled `driverId` directly.
- No application-layer ownership assertion exists before deletion in either case.

**Recommendation:**
Before calling any delete DAO method, first retrieve the entity and assert it belongs to `sessCompId`. Return an error if not. For `delUserById`, add a company-scoped check (e.g., query `user_comp_rel` to confirm `user_id` belongs to `sessCompId`) before proceeding.

---

### FINDING-04 — HIGH: SQL Injection via unsanitised `sessTimezone` session attribute

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Line:** 156
**Also implicates:** `src/main/java/com/dao/DriverDAO.java` lines 357–358

**Description:**
When `search` equals `"current_date"` (case-insensitive), `getAllDriverSearch` constructs a SQL fragment by **direct string interpolation** of the `timezone` parameter:

```java
// DriverDAO.java:358
builder.append(" and timezone('" + timezone + "', p.updatedat)::DATE = current_date::DATE  ");
```

The `timezone` value originates from:

```java
// AdminOperatorAction.java:156
request.getSession().getAttribute("sessTimezone").toString()
```

`sessTimezone` is a session attribute. If an attacker can control the value stored in their own session (e.g., via a profile-update action that writes an unsanitised value to `sessTimezone`, or via session fixation), they can inject arbitrary SQL. Even without that vector, the pattern is inherently unsafe — a session attribute is not a trusted, validated constant and must not be interpolated into SQL strings.

**Evidence:**
- `DriverDAO.java:357–358`: literal `timezone` string concatenated into SQL.
- `AdminOperatorAction.java:156`: `sessTimezone` session attribute passed unchecked.

**Recommendation:**
Replace string interpolation with a parameterised form. PostgreSQL's `timezone()` function accepts the timezone as a text parameter in a prepared statement: `timezone(?, p.updatedat)` with `stmt.setString(n, timezone)`. Additionally, validate `sessTimezone` at login/profile-update time against a whitelist of valid IANA timezone identifiers before storing it in the session.

---

### FINDING-05 — HIGH: No CSRF protection on destructive state-changing actions

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Lines:** 36–60 (entire switch block, specifically `delete`, `deleteuser`, `add`, `adduser`, `edituser`)

**Description:**
The `/admindriver.do` action mapping has no form bean, no `validate="true"`, and — consistent with the project-wide structural gap identified in the stack description — no CSRF token is checked anywhere in `execute()` or in the sub-action methods. Any state-changing operation (delete driver, delete user, add driver) can be triggered by a malicious cross-origin request or by a crafted link visited by an authenticated admin. The `action` discriminator is a plain GET/POST parameter and carries no anti-forgery credential.

**Evidence:**
- `struts-config.xml:233–244`: no form bean, no `validate`, no role constraint.
- `AdminOperatorAction.java:28–60`: no CSRF token read, checked, or invalidated.
- Stack description confirms CSRF is a structural gap across the application.

**Recommendation:**
Introduce a synchroniser token pattern. On every page render that presents a destructive form or link, embed a per-session nonce (`sessCSRFToken`). In `execute()`, for every action that mutates state (`delete`, `deleteuser`, `add`, `adduser`), read the submitted token and compare it to `session.getAttribute("sessCSRFToken")`. Reject and log the request if they do not match. Struts 1 does not provide this natively; it must be implemented in `PandoraAction` or a custom request processor.

---

### FINDING-06 — HIGH: No role check inside `AdminOperatorAction`

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Lines:** 22–61

**Description:**
The struts-config mapping for `/admindriver` declares no `roles` attribute (struts-config.xml:233–244). The action itself performs no programmatic role check. `PreFlightActionServlet` only verifies that `sessCompId` is non-null (i.e., that some company is associated with the session), but does not check whether the authenticated user holds an admin-level role. Any authenticated user — including lower-privilege roles if the application has them — who can reach `/admindriver.do` has full access to all sub-actions including deletion and invite.

**Evidence:**
- `struts-config.xml:233–244`: no `roles` attribute on the `/admindriver` action mapping.
- `AdminOperatorAction.java:22–61`: no call to any role-verification helper.
- `PreFlightActionServlet.java:56–60`: checks only `sessCompId != null`.

**Recommendation:**
Add a role assertion at the top of `execute()`, checking that the session holds a role attribute (e.g., `sessRole`) with an expected admin-level value before dispatching any sub-action. Alternatively, configure `roles="admin"` in the struts-config mapping and ensure the container/servlet is wired to honour it.

---

### FINDING-07 — HIGH: `getDriverById` exposes password hash column via `cpass` / `pass` mapping

**Severity:** HIGH
**File:** `src/main/java/com/dao/DriverDAO.java`
**Lines:** 438–439

**Description:**
`getDriverById` maps column 9 of its result set to both `cpass` and `pass` on the `DriverBean`:

```java
.cpass(rs.getString(9))
.pass(rs.getString(9))
```

The SQL constant (`QUERY_DRIVER_BY_ID`) at line 154 hardcodes that column as the literal string `'******'`, which does mask an actual password in current production SQL. However, the fact that `DriverBean.pass` and `DriverBean.cpass` are populated and the bean is placed directly into `request` scope (`request.setAttribute("driver", ...)`) means the password placeholder — or any future change that accidentally returns a real hash — could be rendered in the edit JSP template. The design pattern of carrying credential fields through the presentation layer is inherently risky.

**Evidence:**
- `DriverDAO.java:438–439`: both credential fields populated from result set.
- `AdminOperatorAction.java:64`: bean placed into `request` attribute `"driver"` for rendering.

**Recommendation:**
Remove `cpass` and `pass` from `getDriverById`'s result-set mapping entirely. Credential management (password change) should be handled by a dedicated, separate DAO operation that never sends the hash to the presentation layer.

---

### FINDING-08 — MEDIUM: `session.getAttribute("sessTimezone")` called without null-check — potential NullPointerException

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Line:** 156

**Description:**
```java
request.getSession().getAttribute("sessTimezone").toString()
```

If `sessTimezone` is absent from the session (e.g., a new session, partial login state, or deliberate attribute removal), this call throws a `NullPointerException`. This is caught by the global `java.sql.SQLException` handler in struts-config (which would not fire for NPE), so it would bubble up to the container, potentially revealing stack trace information in the error response. The same method also calls `request.getSession()` (line 156) without the `false` argument, meaning it **creates a new session** if none exists, unlike line 27 which correctly uses `getSession(false)`.

**Evidence:**
- `AdminOperatorAction.java:156`: direct `.toString()` on unchecked session attribute.
- `AdminOperatorAction.java:27`: correct use of `getSession(false)`.
- `struts-config.xml:42–55`: global exceptions cover only `SQLException`, `IOException`, `ServletException` — not `NullPointerException`.

**Recommendation:**
Use the existing `getSessionAttribute(session, "sessTimezone", "UTC")` helper from `PandoraAction` to retrieve the timezone safely. Do not call `request.getSession()` (without `false`) in the middle of the action; use the session reference already obtained at line 27.

---

### FINDING-09 — MEDIUM: Inconsistent session reference — `request.getSession()` creates new session at line 156

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Line:** 156

**Description:**
Line 27 correctly acquires the session without creating a new one:

```java
HttpSession session = request.getSession(false);
```

Line 156 subsequently calls:

```java
request.getSession().getAttribute("sessTimezone").toString()
```

`getSession()` without `false` creates a new, empty session if the original session has expired or been invalidated. This bypasses the intended intent of `getSession(false)` used elsewhere in the action, could silently succeed when it should fail, and undermines the session-expiry flow enforced by `PreFlightActionServlet`.

**Recommendation:**
Replace `request.getSession().getAttribute("sessTimezone")` with `getSessionAttribute(session, "sessTimezone", "UTC")` using the session variable already bound at line 27.

---

### FINDING-10 — MEDIUM: No input validation on `action` dispatcher parameter

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Lines:** 29, 35

**Description:**
The `action` request parameter drives the entire control flow of the class. It is read unvalidated:

```java
String action = getRequestParam(request, "action", "");
// ...
switch (action.toLowerCase()) {
```

Although `toLowerCase()` reduces case-manipulation risk, there is no whitelist check, length limit, or sanitisation. The `getRequestParam` implementation in `PandoraAction` (line 25–27) returns any non-null value from the servlet parameter. Unrecognised values fall through to the `default` branch and execute a database query, meaning an attacker can trigger `searchAction` (which queries all drivers for the session company) with any unknown action string. More broadly, absent a whitelist, any future addition of action strings is one typo away from being accessible with an empty default.

**Recommendation:**
Define an enum or a `Set<String>` of permitted action values. Log and reject (with a safe forward) any `action` value not in the whitelist.

---

### FINDING-11 — MEDIUM: `driverId` of `null` silently accepted by several sub-actions

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Lines:** 30, 36–54

**Description:**
`getLongRequestParam` (PandoraAction line 13–15) returns `null` when the `driverId` parameter is absent or set to the string `"undefined"`. The actions `editAction`, `editUserAction`, `trainingAction`, `subscriptionAction`, `vehicleAction`, `deleteAction`, and `deleteUserAction` all pass this potentially-null value directly to DAO methods. DAO methods `getDriverById` and `getUserById` do null-check and throw `NullArgumentException`, but `trainingDAO.getTrainingByDriver`, `DriverUnitDAO.getDriverUnitsByCompAndDriver`, `DriverDAO.delDriverById`, and `DriverDAO.delUserById` contain only Java `assert` guards. In production builds, Java `assert`s are typically disabled by default, making these null checks ineffective, leading to uncaught `NullPointerException`s that can expose stack traces.

**Evidence:**
- `PandoraAction.java:13–15`: returns `null` for missing or `"undefined"` param.
- `AdminOperatorAction.java:30`: `driverId` can be null.
- `DriverDAO.java:691–692`: `assert id != null` — disabled in typical production JVM.

**Recommendation:**
For all actions that require `driverId`, validate it is non-null and positive at the top of `execute()` before dispatching, returning a safe error forward if the check fails. Replace `assert` in DAO methods with explicit `if (id == null) throw new IllegalArgumentException(...)` guards.

---

### FINDING-12 — LOW: `sessCompId` read with empty-string default; empty string propagates to DAO

**Severity:** LOW
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Line:** 28

**Description:**
```java
String sessCompId = getSessionAttribute(session, "sessCompId", "");
```

If `sessCompId` is somehow absent from the session (e.g., partial session state), the empty string is passed to DAOs. `Long.parseLong("")` will throw a `NumberFormatException`, and `DBUtil.updateObject(DELETE_DRIVER_BY_ID, ...)` will throw before any DB call — an accidental partial protection. However, the root cause is that the action does not explicitly verify that `sessCompId` is non-blank before any DAO call. `PandoraAction.getCompId()` (line 41–43) returns `null` for missing compId, which would be cleaner, but it is not used here.

**Recommendation:**
After line 28, assert `StringUtils.isNotBlank(sessCompId)` and redirect to the expiry page if false. Alternatively, use `getCompId(session)` and null-check the result.

---

### FINDING-13 — LOW: No validation on `struts-config.xml` — action has no form bean and no `validate`

**Severity:** LOW
**File:** `src/main/webapp/WEB-INF/struts-config.xml`
**Lines:** 233–244

**Description:**
The `/admindriver` mapping has no `name` (form bean) and no `validate` attribute. All parameter extraction, type coercion, and validation is performed manually inside the action with no Struts validation framework involvement. While the manual approach is functional, it means `validation.xml` provides zero coverage for this action, and there is no declarative audit trail of what fields are expected. This is consistent with the project-wide gap noted in the audit context (validation.xml covers only 3 forms).

**Recommendation:**
Define a dedicated ActionForm (e.g., `adminDriverActionForm`) that binds and validates at minimum `action`, `driverId`, and `searchDriver`, and register it with `validate="true"` in the mapping. This consolidates input validation in one auditable location.

---

### FINDING-14 — INFO: `TrainingDAO` is instantiated with `new` rather than a singleton

**Severity:** INFO
**File:** `src/main/java/com/action/AdminOperatorAction.java`
**Line:** 20

**Description:**
```java
private TrainingDAO trainingDAO = new TrainingDAO();
```

`ManufactureDAO` and `UnitDAO` use the singleton pattern (`getInstance()`), but `TrainingDAO` is instantiated directly as an instance field. Because Struts 1 Actions are effectively singletons (one instance per action class per application), this is a single instantiation and does not cause per-request overhead. However, the inconsistency is a code quality concern and warrants review for thread-safety within `TrainingDAO`.

**Recommendation:**
Verify `TrainingDAO` is thread-safe. If so, convert it to the singleton pattern for consistency. If not, move the instantiation inside `execute()` or use a per-request factory.

---

### FINDING-15 — INFO: SQL constant `QUERY_DRIVER_BY_ID` used in `editAction` returns a driver even if that driver has no active permission for any company

**Severity:** INFO
**File:** `src/main/java/com/dao/DriverDAO.java`
**Lines:** 154–157

**Description:**
`QUERY_DRIVER_BY_ID` performs an INNER JOIN on `permission`, so a driver with no permission row will correctly not be returned. However, a driver with a permission row for a *different* company will be returned (see FINDING-01). The INNER JOIN is not a substitute for a company-scoped WHERE clause.

**Recommendation:**
Addressed by FINDING-01 recommendation.

---

## 3. Category Summary

| Category | Verdict |
|----------|---------|
| Authentication (sessCompId present) | PARTIAL — `PreFlightActionServlet` checks `sessCompId != null`, but no null/blank guard exists inside the action itself (FINDING-12). |
| Role Check | MISSING — No role check in action or struts-config (FINDING-06). |
| Order of auth vs DB calls | ISSUE — Auth check (sessCompId) occurs at servlet filter level, but role check and ownership checks are absent; DB calls execute before any ownership assertion (FINDING-01, -02, -03). |
| CSRF | MISSING — Structural gap confirmed; no token checked for any mutating operation (FINDING-05). |
| Input Validation | MISSING for this action — No form bean, no `validate="true"`, no action-level whitelist (FINDING-10, -11, -13). |
| SQL Injection | ONE CONFIRMED INSTANCE — `sessTimezone` string-concatenated into SQL in `getAllDriverSearch` (FINDING-04). All other DAO calls use parameterised queries. |
| IDOR | THREE INSTANCES — `editAction`, `editUserAction`/`subscriptionAction`, `deleteUserAction` all allow cross-tenant access (FINDING-01, -02, -03). |
| Session Handling | TWO ISSUES — NPE risk from unchecked session attribute, inconsistent `getSession()` vs `getSession(false)` (FINDING-08, -09). |
| Data Exposure | ONE INSTANCE — `DriverBean.pass` / `cpass` populated and placed into request scope (FINDING-07). |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 3 | FINDING-01, FINDING-02, FINDING-03 |
| HIGH | 4 | FINDING-04, FINDING-05, FINDING-06, FINDING-07 |
| MEDIUM | 4 | FINDING-08, FINDING-09, FINDING-10, FINDING-11 |
| LOW | 2 | FINDING-12, FINDING-13 |
| INFO | 2 | FINDING-14, FINDING-15 |
| **TOTAL** | **15** | |
