# Security Audit Report: AdminDriverEditAction.java

**Audit run:** audit/2026-02-26-01
**Branch:** master
**Auditor:** Automated Pass-1
**Date:** 2026-02-26

---

## 1. READING EVIDENCE

### 1.1 Full Class Name and Package

```
Package : com.action
Class   : com.action.AdminDriverEditAction
Extends : org.apache.struts.action.Action
```

File: `src/main/java/com/action/AdminDriverEditAction.java`

---

### 1.2 Public/Protected Methods

| Line | Signature |
|------|-----------|
| 22 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

No other public or protected methods are declared in this class.

---

### 1.3 Every DAO / Service Called, with Method Names

| Class | Method | Line(s) in Action |
|---|---|---|
| `DriverDAO` (static) | `updateGeneralInfo(DriverBean)` | 53 |
| `DriverDAO` (static) | `getAllDriver(String sessCompId, boolean)` | 54 |
| `DriverDAO` (static) | `getDriverById(Long driverId)` | 56 |
| `DriverDAO` (static) | `updateGeneralUserInfo(DriverBean)` | 91 |
| `DriverDAO` (static) | `getAllUser(String sessCompId, String sessionToken)` | 93 |
| `DriverDAO` (static) | `getUserById(Long driverId, String sessionToken)` | 95 |
| `DriverDAO` (static) | `checkDriverByLic(String sessCompId, String licence, Long id, boolean)` | 111, 126 |
| `DriverDAO` (static) | `updateDriverLicenceInfo(LicenceBean, String dateFormat)` | 135 |
| `DriverDAO` (static) | `getDriverById(Long driverId)` | 131 |
| `DriverDAO` (static) | `getUserById(Long driverId, String sessionToken)` | 177 |
| `CompanyDAO` (instance) | `getUserAlert(String driverId, String type, String file_name)` | 157–159 |
| `CompanyDAO` (static) | `addUserSubscription(String userId, String alertId)` | 162, 167, 172 |
| `CompanyDAO` (static) | `deleteUserSubscription(String userId, String alertId)` | 164, 169, 174 |
| `SubscriptionDAO` (static) | `getSubscriptionByName(String name)` | 162–174 |
| `DriverService` (singleton) | `updateAssignedVehicle(DriverVehicleBean)` | 183 |

Note: `CompanyDAO compDao = CompanyDAO.getInstance()` is instantiated at line 89 (inside `edit_general_user` block) but `compDao` is never actually used — the subscription work is done using the instance obtained at line 156 inside the `edit_subscription` block.

---

### 1.4 Form Class Used

`com.actionform.AdminDriverEditForm`
File: `src/main/java/com/actionform/AdminDriverEditForm.java`

Key fields accepted from user input:
`id`, `op_code`, `first_name`, `last_name`, `app_access`, `mobile`, `email_addr`, `pass_hash`, `pass`, `cpass`, `department`, `location`, `licence_number`, `expiry_date`, `security_number`, `address`, `redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`, `cognito_username`, `vehicles` (list).

---

### 1.5 struts-config.xml Mappings for this Action

Two mappings share `com.action.AdminDriverEditAction`:

**Mapping 1 — `/admindriveredit`** (lines 313–323 of struts-config.xml):
```xml
<action
    path="/admindriveredit"
    name="adminDriverEditForm"
    scope="request"
    type="com.action.AdminDriverEditAction"
    validate="true"
    input="OperatorEditDefinition">
    <forward name="success"      path="OperatorEditDefinition"/>
    <forward name="successUser"  path="UserEditDefinition"/>
    <forward name="failure"      path="OperatorEditDefinition"/>
</action>
```

**Mapping 2 — `/admindriverlicencevalidateexist`** (lines 324–331 of struts-config.xml):
```xml
<action
    path="/admindriverlicencevalidateexist"
    name="adminDriverEditForm"
    scope="request"
    type="com.action.AdminDriverEditAction"
    validate="true"
    input="OperatorEditDefinition">
</action>
```

Key observations from both mappings:
- `scope="request"` — form is request-scoped (good; no session form pollution).
- `validate="true"` — Struts validator framework is invoked before `execute()`.
- `roles` attribute: **NOT PRESENT** on either mapping. No role-based access control declared at the Struts layer.
- No `input` forward defined for `/admindriverlicencevalidateexist`, meaning validation failures on that path have no defined error destination.

---

### 1.6 validation.xml Entry for AdminDriverEditForm

```xml
<form name="AdminDriverEditForm">
    <field property="first_name" depends="required">
        <arg0 key="driver.firstname" />
    </field>
    <field property="last_name" depends="required">
        <arg0 key="driver.lastname" />
    </field>
</form>
```

Only `first_name` and `last_name` are declared as required. No rules exist for: `id`, `op_code`, `mobile`, `email_addr`, `pass`, `cpass`, `pass_hash`, `licence_number`, `expiry_date`, `security_number`, `address`, `department`, `location`, `cognito_username`, `redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`.

The form-level `validate()` method in `AdminDriverEditForm` adds further checks for `edit_general` / `edit_general_user` (first_name, last_name non-empty; pass == cpass) and for `edit_licence` (licence_number length <= 16, alphanumeric only).

---

## 2. AUDIT FINDINGS

---

### CATEGORY 1: Authentication / Authorization

#### Finding AUTH-1 — Missing In-Action sessCompId Null-Check Creates NPE / Auth Bypass Window

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Line:** 26

**Description:**
`request.getSession(false)` is called at line 25 but the returned `HttpSession` object is never null-checked before being dereferenced at line 26. If the session is null (e.g., session expired between the servlet check and action execution, or if a race condition occurs), a `NullPointerException` is thrown. More critically, the code at line 26 reads `sessCompId` from the session but then falls through to an empty-string default rather than stopping execution:

```java
// Line 25-26
HttpSession session = request.getSession(false);
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
```

If `session` itself is null, the dereference at line 26 (`session.getAttribute(...)`) throws an NPE, which is caught by the global exception handler and redirected to the error page. However if somehow the session exists but `sessCompId` is null or empty, the code silently continues with `sessCompId = ""`. Any subsequent DAO calls that accept `sessCompId` as a query parameter (e.g. `DriverDAO.getAllDriver(sessCompId, true)` at line 54, `DriverDAO.checkDriverByLic(sessCompId, ...)` at line 111) will execute against an empty company ID. While the PreFlightActionServlet gate should prevent reaching this action with a missing `sessCompId`, the action itself provides no defence-in-depth check.

**Evidence:**
```java
// Line 25 — getSession(false) result never null-checked
HttpSession session = request.getSession(false);
// Line 26 — immediate dereference; NPE if session is null
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
```

PreFlightActionServlet does check `sessCompId != null` before forwarding, but the action itself has no guard. If `sessCompId` is empty string, execution continues silently.

**Recommendation:**
Add a null check on `session` and an explicit empty/null check on `sessCompId` at the top of `execute()`. Redirect to the session-expired page if either condition is not met:
```java
if (session == null || session.getAttribute("sessCompId") == null
        || session.getAttribute("sessCompId").toString().isEmpty()) {
    return mapping.findForward("globalfailure");
}
```

---

#### Finding AUTH-2 — No Role or SuperAdmin Check; Any Authenticated Company User Can Edit Any Driver Record

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Lines:** 22–190 (entire execute method)

**Description:**
The action performs no check for whether the authenticated user holds an administrative role (e.g. `superAdmin`, `isAdmin`, or any role flag). The Struts mapping carries no `roles` attribute. Any user who possesses a valid session (a valid `sessCompId`) can POST to `/admindriveredit.do` and modify driver general info, passwords, licence records, subscriptions, and vehicle assignments. This is also visible in `/admindriverlicencevalidateexist.do`.

No check such as:
```java
String isAdmin = (String) session.getAttribute("isAdmin");
```
appears anywhere in this action.

**Evidence:**
struts-config.xml lines 313–323: no `roles` attribute on the `/admindriveredit` mapping.
`execute()` method: zero references to `isAdmin`, `superAdmin`, or any role attribute.

**Recommendation:**
Add a role check at the top of `execute()`, before any state-changing DAO call, and return a forbidden forward if the user does not hold the required role. Alternatively, add a `roles` attribute to the struts-config.xml mapping if container-managed security is acceptable.

---

#### Finding AUTH-3 — Unused CompanyDAO Instance (Dead Code / Logic Error)

**Severity:** LOW
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Line:** 89

**Description:**
Inside the `edit_general_user` branch, `CompanyDAO compDao = CompanyDAO.getInstance()` is instantiated but `compDao` is never used. This is dead code and may indicate a missing ownership check — for example, a check that the driver being updated belongs to the company of the logged-in session. The omission means the edit proceeds without any company-ownership guard on the driver ID.

**Evidence:**
```java
// Line 89
CompanyDAO compDao = CompanyDAO.getInstance();
// compDao is never referenced again in this block
```

**Recommendation:**
Either remove the unused variable (and acknowledge the missing ownership check) or implement the intended company ownership verification using `compDao` before proceeding with the update.

---

### CATEGORY 2: CSRF

#### Finding CSRF-1 — No CSRF Token Validation

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Lines:** 22–190

**Description:**
As documented in the stack context, the entire application has no CSRF protection. This action performs multiple state-changing operations (update driver general info, update password, update licence, modify subscriptions, reassign vehicle) with no anti-CSRF token check. A malicious page on any origin can cause an authenticated admin to perform any of these operations by inducing a cross-origin POST to `/admindriveredit.do` with an attacker-chosen `driverId` and `op_code`.

**Evidence:**
No token field is read from the form or request. No call to any CSRF validation utility anywhere in the action or the `AdminDriverEditForm`.

**Recommendation:**
Implement the Synchronizer Token Pattern: generate a per-session (or per-form) token on page load, store it in the session, include it as a hidden form field, and verify it matches on every POST that modifies state. The token check should be performed at the top of `execute()` before any DAO call.

---

### CATEGORY 3: Input Validation

#### Finding VAL-1 — Validation Rules Are Condition-Blind: All op_code Branches Fail Validation for Non-edit_general Requests

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminDriverEditForm.java`
**Lines:** 61–103
**Related:** `src/main/webapp/WEB-INF/validation.xml` lines 60–67

**Description:**
The `validation.xml` entry for `AdminDriverEditForm` marks `first_name` and `last_name` as required with no condition. This means that when `op_code` is `check_licenceExist`, `edit_subscription`, or `edit_vehicle`, Struts still runs the `required` validator against `first_name` and `last_name`. If the browser sends a request for those operations without those fields populated, validation will fail and the action will not execute — which is overly restrictive but arguably safe. However, it creates the inverse problem: the `validate="true"` setting provides a false sense of security for fields that actually matter to those operations (e.g., `driverId`, `op_code` itself, `redImpactAlert`, `cognito_username`) — none of which are validated.

Additionally, the form's `validate()` method only validates `first_name`, `last_name`, and `pass == cpass` for `edit_general`/`edit_general_user` operations, and licence number format for `edit_licence`. It does NOT validate:

- `op_code` — no whitelist check; any arbitrary string causes `mapping.findForward("")` (empty string) at line 189, which will throw an exception or return null depending on the Struts version's null-forward handling.
- `id` (driverId) — not checked for null before use at line 30, 47, 56, 78, etc.
- `cognito_username` — no length or format validation.
- `mobile` — no format check.
- `email_addr` — no email format validation in this form's `validate()`.

**Evidence:**
```xml
<!-- validation.xml lines 60-67 -->
<form name="AdminDriverEditForm">
    <field property="first_name" depends="required">...</field>
    <field property="last_name"  depends="required">...</field>
</form>
```
```java
// AdminDriverEditAction.java line 29-30
String opCode = adminDriverEditForm.getOp_code();
Long driverId = adminDriverEditForm.getId();
// driverId used at line 47, 56, 78, etc. with no null check
```

**Recommendation:**
1. Add a server-side whitelist check on `op_code` (e.g. `edit_general`, `edit_general_user`, `check_licenceExist`, `edit_licence`, `edit_subscription`, `edit_vehicle`).
2. Null-check `driverId` before use.
3. Add `email` format validation for `email_addr` in `validation.xml` or in the form's `validate()`.
4. Consider op_code-conditional validation rules or separate action mappings per operation.

---

#### Finding VAL-2 — op_code Not Validated; No-Match Path Returns Empty Forward Key

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Line:** 189

**Description:**
`return_code` is initialised to `""` at line 31. If `op_code` does not match any of the five expected values (case-insensitive), none of the `if` blocks execute, `return_code` remains `""`, and `mapping.findForward("")` is called. In Apache Struts 1.3, `findForward("")` returns `null`, which causes Struts to throw a `NullPointerException` or log an unhandled forward. This is an application error path that produces a 500 response, potentially leaking stack-trace information in non-production configurations.

**Evidence:**
```java
// Line 31
String return_code = "";
// Lines 32–187: only five equalsIgnoreCase branches set return_code
// Line 189
return mapping.findForward(return_code); // returns null if no branch matched
```

**Recommendation:**
Validate `op_code` against an explicit whitelist before entering the branch logic. Add a final `else` clause that returns a defined error forward or throws an `InvalidOperationException`.

---

#### Finding VAL-3 — Password Sent and Processed in Plaintext

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Lines:** 40, 51, 75, 84

**Description:**
The `pass` and `pass_hash` fields are accepted directly from the submitted form, stored in `DriverBean`, and passed to `DriverDAO.updateGeneralInfo()` and `DriverDAO.updateGeneralUserInfo()`. While `pass_hash` field naming implies the client may be hashing before submission, the server-side action performs no hashing, no minimum length enforcement, and no complexity validation before the value is written to the database. If the client-side hash is absent or bypassed, cleartext passwords may be stored.

**Evidence:**
```java
// Line 40
String pass = adminDriverEditForm.getPass_hash();
// Line 51
driverbean.setPass(pass);
// Line 53 — immediately written to DB
if (DriverDAO.updateGeneralInfo(driverbean)) { ...
```

**Recommendation:**
Apply a server-side hash (e.g. bcrypt) unconditionally before persisting passwords, regardless of whether the client has already hashed. Do not rely on client-side hashing as a security control.

---

### CATEGORY 4: SQL Injection

#### Finding SQLI-1 — DriverDAO Methods Called by This Action Use Prepared Statements (No Direct Injection via This Action)

**Severity:** INFO

**Description:**
The five DriverDAO methods invoked from this action (`updateGeneralInfo`, `updateGeneralUserInfo`, `checkDriverByLic`, `updateDriverLicenceInfo`, `getAllDriver`) all use `DBUtil.updateObject`/`DBUtil.queryForObject` with parameterized `PreparedStatement` setters. No string concatenation of user-supplied data into SQL is present in those methods.

The CompanyDAO methods (`getUserAlert`, `addUserSubscription`, `deleteUserSubscription`) similarly use parameterized queries.

**Evidence (representative):**
```java
// DriverDAO.java line 580-584 — parameterized
int rowUpdated = DBUtil.updateObject(UPDATE_GENERAL_INFO_SQL, (stmt) -> {
    stmt.setString(1, driverbean.getFirst_name());
    ...
    stmt.setLong(4, driverbean.getId());
});
```

**Note:** `DriverDAO.getDriverByNm()` and `DriverDAO.getDriverByFullNm()` (lines 226–228, 264 in DriverDAO.java) use raw string concatenation and are therefore SQL injectable, but those methods are **not called from this action**. They are flagged here as context for the broader DAO audit.

**Recommendation:**
No remediation required within this action for SQL injection. The broader `getDriverByNm` / `getDriverByFullNm` SQL-concatenation defects should be addressed in the DriverDAO audit.

---

### CATEGORY 5: IDOR (Insecure Direct Object Reference)

#### Finding IDOR-1 — Driver ID Not Verified as Belonging to the Session Company Before Mutation

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Lines:** 30, 46–47, 53, 78, 91, 126, 135, 157–175, 182–183

**Description:**
`driverId` is taken directly from the form at line 30 (`Long driverId = adminDriverEditForm.getId()`). In every operation branch, this ID is used to update the driver record without first confirming that the driver identified by `driverId` belongs to the company identified by `sessCompId`. An authenticated user can supply any arbitrary `driverId` and modify driver records belonging to a different company.

Specific vulnerable call-sites:

- **`edit_general`** (line 53): `DriverDAO.updateGeneralInfo(driverbean)` — `driverbean` has `comp_id` set to `sessCompId`, but the UPDATE SQL in DriverDAO does not filter by `comp_id` (only by `driver.id`). A cross-tenant attacker can overwrite first/last name, mobile, and password of any driver on the platform.
- **`edit_general_user`** (line 91): `DriverDAO.updateGeneralUserInfo(driverbean)` — looks up `cognitoUsername` by `driverbean.getId()` only (line 607–609 in DriverDAO), with no `comp_id` constraint.
- **`check_licenceExist`** (line 111): `DriverDAO.checkDriverByLic(sessCompId, licence_number, null, true)` — scoped to `sessCompId` only, no `driverId` constraint here; lower severity for this branch.
- **`edit_licence`** (lines 126, 135): `DriverDAO.checkDriverByLic(sessCompId, ..., licencebean.getDriver_id(), ...)` uses `sessCompId` but `updateDriverLicenceInfo(licencebean, dateFormat)` updates by `driver_id` only, with no company constraint.
- **`edit_subscription`** (lines 157–175): All subscription mutations use only `String.valueOf(driverId)` — no company scoping.
- **`edit_vehicle`** (line 183): `DriverService.updateAssignedVehicle(driverVehicle)` — the `driverVehicle` bean is built with `sessCompId` (line 182), which may provide some scoping, but only if the service enforces it.

**Evidence:**
```java
// Line 30 — driverId taken directly from user-supplied form
Long driverId = adminDriverEditForm.getId();

// Line 46-47 — comp_id set in bean but not verified against actual driver owner
driverbean.setComp_id(sessCompId);
driverbean.setId(driverId);

// Line 53 — UPDATE executed; no pre-check that driverId belongs to sessCompId
if (DriverDAO.updateGeneralInfo(driverbean)) { ...

// Lines 157-175 — subscription mutations use driverId with no ownership check
AlertBean alertBean = dao.getUserAlert(String.valueOf(driverId),"alert","RedImpactAlert");
CompanyDAO.addUserSubscription(String.valueOf(driverId), ...);
CompanyDAO.deleteUserSubscription(String.valueOf(driverId), ...);
```

**Recommendation:**
Before executing any state-changing operation, perform an ownership check:
```java
DriverBean existing = DriverDAO.getDriverById(driverId);
if (existing == null || !existing.getComp_id().equals(sessCompId)) {
    // return forbidden / error forward
}
```
This pre-fetch must occur before the first DAO mutation call in every op_code branch. Alternatively, all UPDATE SQL statements in DriverDAO should include `AND comp_id = ?` to enforce ownership at the database layer.

---

### CATEGORY 6: Session Handling

#### Finding SESSION-1 — getSession(false) Result Not Null-Checked Before Use

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Lines:** 25–28

**Description:**
`request.getSession(false)` returns `null` if no session currently exists. The return value is stored in `session` (line 25) and immediately dereferenced at line 26 without a null check. If the session is invalidated between the PreFlightActionServlet check and the action's own execution (e.g., concurrent logout, session timeout, load-balancer routing to a node without the session), a `NullPointerException` is thrown. This produces a 500 error and falls to the global exception handler.

This is covered in AUTH-1 above but is restated here as a distinct session-handling finding because the fix is specifically a null-guard on `session`.

**Evidence:**
```java
// Line 25
HttpSession session = request.getSession(false);
// Line 26 — NPE if session is null
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
// Line 27 — second unguarded dereference
String dateFormat = (String) session.getAttribute("sessDateFormat");
// Line 28 — third unguarded dereference
String sessionToken = session.getAttribute("sessionToken") == null ? "" : (String) session.getAttribute("sessionToken");
```

**Recommendation:**
Null-check `session` immediately after line 25 and return an appropriate forward (session expired) if it is null.

---

### CATEGORY 7: Data Exposure

#### Finding DATAEXP-1 — Cognito Access Token Passed Through DriverBean to External Service

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Lines:** 28, 87, 93, 95, 177

**Description:**
`sessionToken` is read from the session at line 28 and placed into `driverbean.setAccessToken(sessionToken)` at line 87. This token is then forwarded to `DriverDAO.updateGeneralUserInfo()` (line 91), which passes it to an external REST call via `RestClientService`. Additionally, `sessionToken` is passed directly as a parameter to `DriverDAO.getAllUser(sessCompId, sessionToken)` (line 93), `DriverDAO.getUserById(driverId, sessionToken)` (line 95), and `DriverDAO.getUserById(driverId, sessionToken)` (line 177).

While using the token for Cognito API calls may be intentional, transmitting the raw `sessionToken` as a method parameter and into the bean graph means it is exposed to any logging framework, serialization, or diagnostic output that touches those objects. If debug logging is enabled at DAO or service level, the live access token may appear in log files.

**Evidence:**
```java
// Line 28
String sessionToken = session.getAttribute("sessionToken") == null ? "" : (String) session.getAttribute("sessionToken");
// Line 87
driverbean.setAccessToken(sessionToken);
// Line 93
List<DriverBean> arrDriver = DriverDAO.getAllUser(sessCompId, sessionToken);
```

**Recommendation:**
Ensure that `sessionToken` / `accessToken` fields are excluded from `toString()`, logging annotations (e.g., Lombok `@ToString.Exclude`), and any serialization that might write to logs or request attributes. Review DAO and service log statements to confirm the token is not logged at DEBUG or INFO level.

---

#### Finding DATAEXP-2 — Raw Password Value Set in Request Attribute on Validation Error Path

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminDriverEditForm.java`
**Lines:** 87–102

**Description:**
In `AdminDriverEditForm.validate()`, when `op_code` is `edit_general` or `edit_general_user`, a `DriverBean` is built from form fields including `pass` and `cpass`, then stored as a request attribute (`arrAdminDriver`) for the re-display of the form on error. While `pass` and `cpass` are included in the bean, the JSP that re-renders the form would receive these values in the request scope. If the JSP echoes these fields back, the password (even masked) is round-tripped through HTML.

**Evidence:**
```java
// AdminDriverEditForm.java lines 87-102
DriverBean driverbean = DriverBean.builder()
    .pass(this.pass)
    .cpass(this.cpass)
    ...
    .build();
List<DriverBean> arrDriver = new ArrayList<>();
arrDriver.add(driverbean);
request.setAttribute("arrAdminDriver", arrDriver);
```

**Recommendation:**
Do not include `pass` or `cpass` in the bean placed on the request. Passwords should never be reflected back to the client in HTML form values.

---

## 3. FINDING SUMMARY

| ID | Severity | Category | Title |
|----|----------|----------|-------|
| IDOR-1 | CRITICAL | IDOR | Driver ID not verified as belonging to session company |
| CSRF-1 | HIGH | CSRF | No CSRF token validation on state-changing operations |
| AUTH-1 | HIGH | Auth/Authz | sessCompId not null-checked in action; empty-string fallthrough |
| AUTH-2 | HIGH | Auth/Authz | No role or admin check; any authenticated user can edit any driver |
| SESSION-1 | HIGH | Session | getSession(false) not null-checked before dereference |
| VAL-3 | HIGH | Input Validation | Password processed without server-side hashing or length enforcement |
| VAL-1 | MEDIUM | Input Validation | Validation rules insufficient; most op_code branches unvalidated |
| VAL-2 | MEDIUM | Input Validation | op_code not whitelisted; unrecognised value causes null forward |
| DATAEXP-1 | MEDIUM | Data Exposure | Cognito sessionToken in bean graph risks exposure via logging |
| DATAEXP-2 | MEDIUM | Data Exposure | Password fields set in request attribute on validation error path |
| AUTH-3 | LOW | Auth/Authz | Unused CompanyDAO instance; missing ownership verification hint |
| SQLI-1 | INFO | SQL Injection | DAO calls from this action use parameterised queries (no injection) |

### Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH | 5 |
| MEDIUM | 4 |
| LOW | 1 |
| INFO | 1 |
| **Total** | **12** |
