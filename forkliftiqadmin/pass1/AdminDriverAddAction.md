# Security Audit Report: AdminDriverAddAction

**Audit Run:** audit/2026-02-26-01
**Branch:** master
**Auditor:** Automated Pass 1
**Date:** 2026-02-26

---

## 1. READING EVIDENCE

### 1.1 Full Class Name and Package

```
Package:    com.action
Class:      AdminDriverAddAction
Extends:    org.apache.struts.action.Action
Full name:  com.action.AdminDriverAddAction
Source:     src/main/java/com/action/AdminDriverAddAction.java
```

### 1.2 Public/Protected Methods

| Line | Signature |
|------|-----------|
| 21 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

No other public or protected methods are declared in this class.

### 1.3 DAO/Service Calls

| Line | Class | Method | Input Source |
|------|-------|--------|-------------|
| 32 | `DriverDAO` (static) | `addDriverInfo(driverbean)` | `driverbean` built from form fields + `sessCompId` |
| 46 | `CompanyDAO` | `getInstance()` | — |
| 49 | `RestClientService` | constructor (instantiation) | — |
| 61 | `RestClientService` | `signUpRequest(signUpRequest)` | form fields: `email_addr`, `pass`, `first_name`, `last_name` |
| 82 | `CompanyDAO` | `getUserMaxId()` | — |
| 91 | `CompanyDAO` | `saveUsers(int compId, UserBean userBean)` | `sessCompId` (parsed to int), `UserBean` built from form fields |
| 92 | `CompanyDAO` | `saveUserRoles(int userId, String role)` | `userId` from `getUserMaxId()`, `RuntimeConf.ROLE_SITEADMIN` |

### 1.4 Form Class Used

```
com.actionform.AdminDriverAddForm
Source: src/main/java/com/actionform/AdminDriverAddForm.java
```

Fields declared: `id`, `first_name`, `last_name`, `licence_number`, `expiry_date`, `security_number`, `address`, `app_access`, `mobile`, `email_addr`, `pass`, `cpass`, `location`, `department`, `op_code`

The form implements its own `validate()` method (lines 38-58) checking that `first_name` and `last_name` are non-empty and that `pass.equals(cpass)`.

### 1.5 struts-config.xml Mapping

```xml
<!-- struts-config.xml lines 302-312 -->
<action
        path="/admindriveradd"
        name="adminDriverAddForm"
        scope="request"
        type="com.action.AdminDriverAddAction"
        validate="true"
        input="OperatorEditDefinition">
    <forward name="success"      path="OperatorEditDefinition"/>
    <forward name="successUser"  path="UserEditDefinition"/>
    <forward name="failure"      path="OperatorEditDefinition"/>
</action>
```

| Attribute | Value | Security Relevance |
|-----------|-------|--------------------|
| `path` | `/admindriveradd` | URL endpoint |
| `scope` | `request` | Form populated per-request (correct) |
| `validate` | `true` | Triggers `AdminDriverAddForm.validate()` before `execute()` |
| `roles` | **not set** | No declarative role restriction |
| `input` | `OperatorEditDefinition` | Redirected on validation failure |

### 1.6 validation.xml Entry

Searching `validation.xml` for `adminDriverAddForm` (or any case variant):

**No entry exists** for `adminDriverAddForm` in `validation.xml`. The file contains entries only for:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

Validation for `AdminDriverAddAction` relies entirely on the programmatic `validate()` method in `AdminDriverAddForm` (lines 38-58 of the form class).

---

## 2. FINDINGS

---

### FINDING-01 — CRITICAL: No Role/Authorization Check — Any Authenticated Session Can Create Drivers and Promote Accounts to ROLE_SITE_ADMIN

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminDriverAddAction.java`
**Lines:** 21-101 (entire `execute()` method)

**Description:**

The action performs no role or privilege check beyond the presence of `sessCompId` in the session. The `PreFlightActionServlet` only verifies that `sessCompId != null && !sessCompId.equals("")` (PreFlightActionServlet.java lines 56-60). Any user who has any valid authenticated session — regardless of whether they are a regular driver, a low-privilege operator, or a site admin — can POST to `/admindriveradd.do` and:

1. Insert a new driver record into the database (`op_code=add_general`).
2. Register an entirely new Cognito user, insert that user into `users`, link them to the session's company, and grant them `ROLE_SITE_ADMIN` privileges (`op_code=add_general_user`, lines 91-93).

The privilege escalation via `op_code=add_general_user` is particularly severe: `compDao.saveUserRoles(userId, RuntimeConf.ROLE_SITEADMIN)` (line 92) assigns `ROLE_SITE_ADMIN` unconditionally to any newly created user. Any authenticated user can promote a new account to site administrator within the company.

**Evidence:**

```java
// AdminDriverAddAction.java lines 21-27
public ActionForward execute(...) throws Exception {
    AdminDriverAddForm adminDriverAddForm = (AdminDriverAddForm) actionForm;
    HttpSession session = request.getSession(false);
    String sessCompId = (String) session.getAttribute("sessCompId");
    // <-- NO role check here or anywhere in the method
```

```java
// AdminDriverAddAction.java lines 91-93
compDao.saveUsers(Integer.parseInt(sessCompId), userBean);
compDao.saveUserRoles(userId, RuntimeConf.ROLE_SITEADMIN);  // unconditional admin grant
return_code = "successUser";
```

```java
// PreFlightActionServlet.java lines 56-60 — the only auth gate
else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
```

**Recommendation:**

1. Immediately add a role check at the top of `execute()` before any state-changing code. Retrieve the session's role (e.g., `sessRole` or query the DB) and verify the caller has at minimum `ROLE_SITE_ADMIN` before allowing either `op_code` branch to proceed.
2. Separate the `add_general_user` path into a distinct action that is explicitly restricted to super-admin or site-admin roles.
3. Do not grant `ROLE_SITE_ADMIN` unconditionally — drive the assigned role from a controlled configuration, not a hardcoded escalation path.

---

### FINDING-02 — CRITICAL: NullPointerException / Authentication Bypass via Null Session

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminDriverAddAction.java`
**Lines:** 23-24

**Description:**

`request.getSession(false)` correctly avoids creating a new session, but the return value is **never null-checked** before `session.getAttribute("sessCompId")` is called on line 24. If the session does not exist (expired, no cookie, or first request), `session` will be `null` and the `.getAttribute()` call will throw a `NullPointerException`.

In the Struts 1 `global-exceptions` handler (struts-config.xml lines 42-55), all `java.lang.RuntimeException` (and by extension `NullPointerException`) fall through to the default unhandled exception behavior — the handler only catches `SQLException`, `IOException`, and `ServletException`. The result is an unhandled 500 error, which may leak stack traces to the user.

More critically, a crafted request with no session cookie (or an expired session) will crash the action before the `PreFlightActionServlet` guard can forward to the expire page, because the action itself is invoked inside the servlet's `super.doGet()` call path — after the filter decision. If the filter failed to block the request (e.g., due to a timing window or filter bypass), the null session would produce an uncaught NPE rather than a safe redirect, potentially revealing internal path information.

**Evidence:**

```java
// AdminDriverAddAction.java lines 23-24
HttpSession session = request.getSession(false);
String sessCompId = (String) session.getAttribute("sessCompId");  // NPE if session is null
```

**Recommendation:**

Add a null-check immediately after obtaining the session:

```java
HttpSession session = request.getSession(false);
if (session == null || session.getAttribute("sessCompId") == null) {
    return mapping.findForward("globalfailure");
}
String sessCompId = (String) session.getAttribute("sessCompId");
```

This is a defensive measure even if `PreFlightActionServlet` is relied upon as the primary gate.

---

### FINDING-03 — HIGH: Plaintext Password Stored in UserBean and Passed to saveUsers / Cognito

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminDriverAddAction.java`
**Lines:** 53, 88
**Related file:** `src/main/java/com/dao/CompanyDAO.java` line 61

**Description:**

In the `add_general_user` branch, the plaintext password from the form (`adminDriverAddForm.getPass()`) is:

1. Sent to the external Cognito service as plaintext in the `UserSignUpRequest` (line 53).
2. Placed into `UserBean.password` (line 88) and then passed to `compDao.saveUsers()`.

In `CompanyDAO.saveUsers()`, the active SQL path is:

```java
// CompanyDAO.java lines 242-244 (SAVE_COGNITO_USERS path — active)
DBUtil.updateObject(SAVE_COGNITO_USERS, stmt -> {
    stmt.setInt(1, userBean.getIduser());
    stmt.setString(2, userBean.getEmail());    // stores email as cognito_username, password not written here
});
```

The `SAVE_USERS` insert (which would call `md5(?)`) is commented out (CompanyDAO.java lines 247-254). The password is therefore **not written to the database in this code path** currently, but it is:

- Carried in the `UserBean` object in memory and in request scope.
- Set on the request attribute `driver` (line 98: `request.setAttribute("driver", driverbean)`), which is then forwarded to a JSP. If the JSP inadvertently renders all bean properties, the password could be exposed.
- Transmitted to the external Cognito service in plaintext over whatever transport `RestClientService` uses.

The `DriverBean` set on the request attribute at line 98 includes the `pass` field (AdminDriverAddForm.java line 75: `.pass(pass)`), making cleartext password available in request scope on every forward.

**Evidence:**

```java
// AdminDriverAddAction.java lines 51-59
UserSignUpRequest signUpRequest = UserSignUpRequest.builder()
    .username(adminDriverAddForm.getEmail_addr())
    .password(adminDriverAddForm.getPass())   // plaintext password to Cognito
    ...
    .build();
```

```java
// AdminDriverAddAction.java lines 83-90
UserBean userBean = UserBean.builder()
    ...
    .password(adminDriverAddForm.getPass())   // plaintext password in UserBean
    .build();
```

```java
// AdminDriverAddAction.java line 98
request.setAttribute("driver", driverbean);  // driverbean.pass = plaintext password in request scope
```

**Recommendation:**

1. Do not store the plaintext password in `DriverBean` or `UserBean` after the Cognito sign-up call succeeds. Zero/null the password field immediately after use.
2. Do not place the `driverbean` object (which contains `pass`) into request scope. Either use a separate DTO that excludes the password, or explicitly null out the password before the `setAttribute` call.
3. Verify that `RestClientService.signUpRequest()` communicates with Cognito only over TLS.

---

### FINDING-04 — HIGH: CSRF — No Token Validation on State-Changing Action

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminDriverAddAction.java`
**Lines:** 21-101

**Description:**

As noted in the stack context, there is no CSRF protection across the application. This action creates driver records and user accounts with elevated roles. An authenticated admin visiting a malicious page could have their browser silently POST to `/admindriveradd.do` with attacker-controlled form data, resulting in:

- Creation of attacker-controlled driver records in the victim's company.
- Creation of a new `ROLE_SITE_ADMIN` account under the victim's company (the `add_general_user` branch).

The `add_general_user` CSRF scenario is effectively a CSRF-driven privilege escalation and account takeover path.

**Evidence:**

No synchronizer token, `SameSite` cookie attribute enforcement, `Origin`/`Referer` header check, or any other anti-CSRF mechanism is present in the action or in the struts-config mapping.

**Recommendation:**

Implement a synchronizer token pattern for all state-changing Struts actions. Struts 1 does not provide this natively; it must be added manually (generate a random token in the session, embed it as a hidden form field, validate in `execute()` before processing). At minimum, verify the `Origin` or `Referer` header matches the expected server host.

---

### FINDING-05 — HIGH: Insufficient Input Validation — No validation.xml Coverage; Programmatic Validation Has Gaps

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`
**Lines:** 38-58
**Related file:** `src/main/webapp/WEB-INF/validation.xml` (no entry for `adminDriverAddForm`)

**Description:**

**Gap 1 — No validation.xml entry.** The `adminDriverAddForm` form bean has no corresponding entry in `validation.xml`. All validation is programmatic in `AdminDriverAddForm.validate()`.

**Gap 2 — NullPointerException on null fields.** The `validate()` method calls `first_name.equalsIgnoreCase("")` (line 41) and `last_name.equalsIgnoreCase("")` (line 47) without first checking for `null`. If a request is submitted without those parameters (e.g., stripped by a proxy or sent via a crafted HTTP client), these will throw `NullPointerException`, bypassing validation and potentially allowing the action to proceed with null field values, or causing an unhandled exception.

The same null risk applies to `pass.equalsIgnoreCase(cpass)` on line 53 — if `pass` is null, this throws NPE and may bypass the password-match check.

**Gap 3 — No length, format, or content validation.** The following fields accepted from the form have no length or format constraints in either `validate()` or `validation.xml`:

- `email_addr` — not checked for valid email format; passed directly to Cognito and into the `users_cognito` table
- `pass` / `cpass` — no minimum length, no complexity requirement
- `mobile` — no format validation; stored in DB
- `first_name` / `last_name` — only checked for non-empty; no length cap
- `licence_number`, `security_number`, `address`, `location`, `department` — no validation at all

**Gap 4 — op_code not validated.** The `op_code` field controls which database branch executes. It is read directly from the form (line 26) and compared with `equalsIgnoreCase` (lines 30, 44). There is no validation that `op_code` is one of the expected values. An unexpected `op_code` value causes both `if` blocks to be skipped; `return_code` remains `""`, and `mapping.findForward("")` returns `null`, which Struts will handle as a null forward (typically a 500 error). No explicit error is returned to the user.

**Evidence:**

```java
// AdminDriverAddForm.java lines 41-42 — null-unsafe
if( first_name.equalsIgnoreCase("") ) {
```

```java
// AdminDriverAddForm.java lines 53-56 — null-unsafe
if (!pass.equalsIgnoreCase(cpass)) {
```

```java
// AdminDriverAddAction.java line 26 — unvalidated op_code
String opCode = adminDriverAddForm.getOp_code();
```

**Recommendation:**

1. Add null-guards to all fields in `validate()` before calling instance methods on them.
2. Add an `adminDriverAddForm` entry to `validation.xml` with at minimum `required`, `email`, and `maxlength` rules for `email_addr`, `first_name`, `last_name`, and `pass`.
3. Validate `op_code` against an allowlist (`add_general`, `add_general_user`) and return an error for any unrecognized value.
4. Add a minimum password length requirement (at least 8 characters).

---

### FINDING-06 — MEDIUM: IDOR — Company Scope Taken From Session but Not Verified Against Submitted Driver ID

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminDriverAddAction.java`
**Lines:** 27, 32

**Description:**

In the `add_general` path, the `driverbean.comp_id` is set to `sessCompId` (AdminDriverAddForm.java line 77), which correctly scopes the new driver to the session's company. The `DriverDAO.addDriverInfo()` method then uses parameterized queries with this value, so the company association itself is correctly enforced.

However, the form also accepts an `id` field (`AdminDriverAddForm.java` line 22: `private Long id = null`) that is passed into `DriverBean` (line 63: `.id(id)`). In `add_general` mode, this `id` is not used by `addDriverInfo` (the insert ignores it — `RETURNING id` generates the ID server-side). But the `id` field on the form is entirely user-controlled, and if any code path were to use `driverbean.getId()` as a lookup key for an existing record, no ownership check is performed. This is a latent IDOR risk that could be activated by future code changes.

Additionally, in the `add_general_user` branch, `sessCompId` is passed to `compDao.saveUsers(Integer.parseInt(sessCompId), userBean)` (line 91) which correctly ties the new user to the session company. No override of company ID from form input is possible in this path.

**Evidence:**

```java
// AdminDriverAddForm.java line 22 — user-supplied id accepted
private Long id = null;

// AdminDriverAddForm.java line 63 — id flows into DriverBean
.id(id)

// AdminDriverAddAction.java lines 27-32 — id is in driverbean but no ownership check
DriverBean driverbean = adminDriverAddForm.getDriverBean(sessCompId);
...
if (!DriverDAO.addDriverInfo(driverbean)) {
```

**Recommendation:**

For an `add` action, the `id` field from the form should be ignored entirely — the server should always generate the new record ID. Remove the `id` field from `AdminDriverAddForm` or explicitly set `driverbean.setId(null)` before calling `addDriverInfo()`. This prevents any form-submitted ID from influencing the operation and closes the latent IDOR vector.

---

### FINDING-07 — MEDIUM: Unhandled null Return from mapping.findForward for Empty return_code

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminDriverAddAction.java`
**Lines:** 28, 99

**Description:**

`return_code` is initialized to `""` (line 28) and is only set to a non-empty value if `opCode` matches `add_general` or `add_general_user`. If `op_code` is absent, null, or neither expected value, both `if` blocks are skipped and `mapping.findForward("")` is called (line 99). `ActionMapping.findForward("")` returns `null` when no forward with that name exists, and Struts will throw a `NullPointerException` internally, resulting in an unhandled 500 error potentially leaking stack trace information.

Furthermore, if `op_code` is `null`, the call `opCode.equalsIgnoreCase(...)` on line 30 will itself throw a `NullPointerException` before `return_code` is even evaluated.

**Evidence:**

```java
// AdminDriverAddAction.java lines 26, 28, 30, 44, 99
String opCode = adminDriverAddForm.getOp_code();   // can be null
DriverBean driverbean = adminDriverAddForm.getDriverBean(sessCompId);
String return_code = "";

if(opCode.equalsIgnoreCase("add_general"))        // NPE if opCode is null
...
if(opCode.equalsIgnoreCase("add_general_user"))   // NPE if opCode is null
...
return mapping.findForward(return_code);           // null forward if return_code = ""
```

**Recommendation:**

Add a null/empty check on `op_code` at the start of the method and return a named failure forward immediately. Add an `else` or final fallthrough that returns a specific `"failure"` forward rather than relying on an empty string.

---

### FINDING-08 — LOW: Error Message May Expose Internal Cognito Error Details to the Client

**Severity:** LOW
**File:** `src/main/java/com/action/AdminDriverAddAction.java`
**Lines:** 64-79

**Description:**

When Cognito sign-up fails, the raw error message returned from the Cognito API (`signUpResponse.getMessage()`) is placed directly into an `ActionMessage` and forwarded to the user-visible JSP:

```java
String errormsg = signUpResponse.getMessage();
ActionMessage msg = new ActionMessage("errors.global", errormsg);
errors.add("DriverAddError", msg);
```

This may expose internal service error text (e.g., Cognito error codes, policy details, internal hostnames or ARNs) to the user interface.

**Evidence:**

```java
// AdminDriverAddAction.java lines 64-69 (User already exists branch)
String errormsg = signUpResponse.getMessage();
ActionErrors errors = new ActionErrors();
ActionMessage msg = new ActionMessage("errors.global", errormsg);
errors.add("DriverAddError", msg);

// AdminDriverAddAction.java lines 73-79 (other Cognito failure branch)
String errormsg = signUpResponse.getMessage();
ActionMessage msg = new ActionMessage("error.cognito", errormsg);
```

**Recommendation:**

Map Cognito error responses to user-friendly, application-controlled messages. Log the raw `errormsg` server-side (to the secure log) and display only a generic message (e.g., "Registration failed. Please try again or contact support.") to the user. The "User already exists" message is acceptable in most flows but should be reviewed for whether it constitutes a user enumeration risk.

---

### FINDING-09 — INFO: CSRF (Structural Gap — App-Wide)

**Severity:** INFO
**File:** `src/main/java/com/action/AdminDriverAddAction.java`

**Description:**

As documented in the stack context, CSRF protection is absent across the entire application. This finding is recorded here as a confirmation that `AdminDriverAddAction` participates in this structural gap. See FINDING-04 above for the action-specific CSRF risk. No additional action-specific CSRF mechanism was found.

---

### FINDING-10 — INFO: SQL Injection — DAO Methods Called by This Action Use Parameterized Queries

**Severity:** INFO (no issue in this action's direct call path)
**File:** `src/main/java/com/dao/DriverDAO.java` lines 511-512
**File:** `src/main/java/com/dao/CompanyDAO.java` lines 61, 67

**Description:**

The two DAO methods directly invoked by this action — `DriverDAO.addDriverInfo()` and `CompanyDAO.saveUsers()` — both use `PreparedStatement` with `?` placeholders and `setString()`/`setInt()` calls. No string concatenation of user-supplied data was found in these specific methods.

Note: Other methods in `CompanyDAO` and `DriverDAO` contain SQL injection vulnerabilities via string concatenation (e.g., `CompanyDAO.checkExist()` at line 367, `CompanyDAO.checkUserExit()` at line 385, `DriverDAO` lines 226-228, 264), but those methods are not called by `AdminDriverAddAction` and are therefore out of scope for this file's audit.

**Evidence:**

```java
// DriverDAO.java lines 511-512 — parameterized, safe
stmt = conn.prepareStatement("insert into driver(first_name,last_name,licno,expirydt,securityno,addr,active,phone,email,password) " +
        "values (?,?,NULL,NULL,NULL,NULL,TRUE,?,?,md5(?)) RETURNING id");
stmt.setString(1, driverbean.getFirst_name());
stmt.setString(2, driverbean.getLast_name());
```

**Recommendation:** No action required for this action's call path. Cross-reference the SQL injection findings in `CompanyDAO` and `DriverDAO` to the actions that invoke the vulnerable methods.

---

## 3. SUMMARY TABLE

| # | Severity | Category | Description |
|---|----------|----------|-------------|
| 01 | CRITICAL | Authentication/Authorization | No role check — any session can add drivers or create ROLE_SITE_ADMIN accounts |
| 02 | CRITICAL | Session Handling | `getSession(false)` result not null-checked before `.getAttribute()` call |
| 03 | HIGH | Data Exposure | Plaintext password stored in DriverBean and placed in request scope via `setAttribute("driver", ...)` |
| 04 | HIGH | CSRF | No CSRF token validation on state-changing (driver add, user creation) action |
| 05 | HIGH | Input Validation | No validation.xml entry; programmatic validate() is null-unsafe and missing format/length/allowlist checks |
| 06 | MEDIUM | IDOR | User-supplied `id` field in form flows into DriverBean unchecked (latent IDOR vector) |
| 07 | MEDIUM | Error Handling | Empty `return_code` default causes null forward and potential NPE; null `op_code` causes NPE |
| 08 | LOW | Data Exposure | Raw Cognito API error messages surfaced to the client |
| 09 | INFO | CSRF | App-wide structural gap confirmed present in this action |
| 10 | INFO | SQL Injection | DAO calls from this action use parameterized queries — no SQL injection in this path |

---

## 4. FINDING COUNT BY SEVERITY

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 3 |
| MEDIUM | 2 |
| LOW | 1 |
| INFO | 2 |
| **TOTAL** | **10** |
