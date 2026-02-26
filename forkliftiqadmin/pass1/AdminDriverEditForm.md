# Audit Report: AdminDriverEditForm
**File:** `src/main/java/com/actionform/AdminDriverEditForm.java`
**Audit run:** audit/2026-02-26-01/
**Auditor note:** Also reviewed `AdminDriverEditAction.java` and `DriverDAO.java` for downstream consumption of form fields.

---

## 1. READING EVIDENCE

### 1.1 Full Class Name and Package

```
package com.actionform;
class: com.actionform.AdminDriverEditForm
extends: org.apache.struts.action.ActionForm
```

### 1.2 Every Field (type and name)

| # | Type | Field name | Notes |
|---|------|-----------|-------|
| 1 | `Long` | `id` | Driver primary key — bound directly from HTTP request |
| 2 | `String` | `first_name` | |
| 3 | `String` | `last_name` | |
| 4 | `String` | `licence_number` | |
| 5 | `String` | `expiry_date` | Date string, no format validation |
| 6 | `String` | `security_number` | Licence security/card number |
| 7 | `String` | `address` | |
| 8 | `String` | `app_access` | Controls app access flag |
| 9 | `String` | `mobile` | |
| 10 | `String` | `email_addr` | |
| 11 | `String` | `redImpactAlert` | Alert subscription toggle |
| 12 | `String` | `redImpactSMSAlert` | Alert subscription toggle |
| 13 | `String` | `driverDenyAlert` | Alert subscription toggle |
| 14 | `String` | `pass` | Plain-text password from user |
| 15 | `String` | `cpass` | Confirm password |
| 16 | `String` | `location` | |
| 17 | `String` | `department` | |
| 18 | `String` | `op_code` | Operation discriminator — controls action branch |
| 19 | `String` | `pass_hash` | Pre-hashed password — accepted from HTTP request |
| 20 | `String` | `cognito_username` | Cognito identity field |
| 21 | `List<DriverUnitBean>` | `vehicles` | Indexed vehicle assignments |

Lombok `@Getter` / `@Setter` / `@NoArgsConstructor` generate public accessors for **all** fields.

### 1.3 validate() Method

**Exists: YES** (lines 61–125)

Logic summary:
- If `op_code` is `edit_general` or `edit_general_user`:
  - Checks `first_name` is non-empty (line 65).
  - Checks `last_name` is non-empty (line 70).
  - Checks `pass.equals(cpass)` (line 75).
  - If `pass` equals `"******"` (mask sentinel), clears `pass`, `cpass`, and `pass_hash` (lines 80–85).
  - Builds a `DriverBean` and sets it on the request as `arrAdminDriver` attribute (side-effect inside validate, lines 87–102).
- If `op_code` is `edit_licence`:
  - Calls `isLicenceNumberInvalid()` — rejects licence numbers longer than 16 chars or containing non-alphanumeric characters.
  - Builds a `LicenceBean` and sets it on the request (side-effect, lines 111–121).
- **No validation for any other op_code** (`edit_subscription`, `edit_vehicle`, `check_licenceExist`, or any unknown value).

`isLicenceNumberInvalid()` (lines 127–131): max 16 chars, alphanumeric only.
`containSpecialCharacter()` (lines 133–137): regex `[^a-z0-9]` case-insensitive.

### 1.4 reset() Method

**Exists: NO.** No `reset()` override is present. Struts `ActionForm.reset()` default is a no-op. Fields are not cleared between requests.

### 1.5 validation.xml Rules for AdminDriverEditForm

The form is declared in `src/main/webapp/WEB-INF/validation.xml` at lines 60–67:

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

**Summary:** Only `first_name` and `last_name` have declarative rules (both `required` only). No other field is covered. No `maxlength`, no format, no type checking is declared.

---

## 2. FINDINGS

---

### FINDING-01 — CRITICAL: IDOR via Unvalidated Driver ID

**Severity:** CRITICAL
**File+Line:** `AdminDriverEditForm.java:28`, `AdminDriverEditAction.java:30`

**Description:**
The `id` field (type `Long`) is a driver primary key bound directly from the HTTP request with no server-side ownership check. In `AdminDriverEditAction`, the `id` is used verbatim to issue UPDATE and SELECT statements against the driver, licence, and user tables.

In `edit_general` (Action line 47):
```java
driverbean.setId(driverId);   // driverId = adminDriverEditForm.getId()
DriverDAO.updateGeneralInfo(driverbean);
```
SQL used (DriverDAO line 52):
```sql
update driver set first_name = ?, last_name = ?, phone = ? where id = ?
```

In `edit_licence` (Action line 124):
```java
LicenceBean licencebean = adminDriverEditForm.getLicenseBean();
DriverDAO.updateDriverLicenceInfo(licencebean, dateFormat);
```
SQL used (DriverDAO line 50):
```sql
update driver set licno = ?, expirydt = ?, securityno = ?, addr = ? where id = ?
```

The `comp_id` used for the UPDATE is `sessCompId` (from session) for display queries but **is NOT included in the WHERE clause of the UPDATE statements**. An authenticated admin of company A can submit `id=<any driver id>` and overwrite records belonging to drivers in other companies.

**Evidence:**
- `UPDATE_GENERAL_INFO_SQL` at DriverDAO line 52: `where id = ?` — no comp_id filter.
- `UPDATE_DRIVER_LICENSE_SQL` at DriverDAO line 50: `where id = ?` — no comp_id filter.
- `UPDATE_USER_INFO_SQL` at DriverDAO line 56: `where id = ?` — no comp_id filter.
- No validation of `id` ownership in `validate()` or in the action.

**Recommendation:**
Add a server-side ownership check before every UPDATE: verify that the driver record with the given `id` belongs to `sessCompId`. Modify the UPDATE SQL to include `AND comp_id = ?` (or join through the `permission` table) so cross-company modification is impossible even with a manipulated request.

---

### FINDING-02 — CRITICAL: pass_hash Field Accepted From HTTP Request

**Severity:** CRITICAL
**File+Line:** `AdminDriverEditForm.java:46`, `AdminDriverEditAction.java:40, 74`

**Description:**
The field `pass_hash` is a `String` field with a public Lombok-generated setter, meaning it is bound from the HTTP POST body by Struts introspection. The action uses this value directly as the password credential written to the database:

`edit_general` branch (Action line 40):
```java
String pass = adminDriverEditForm.getPass_hash();
// ...
driverbean.setPass(pass);
DriverDAO.updateGeneralInfo(driverbean);
```
`updateGeneralInfo` in DriverDAO (line 588):
```java
rowUpdated += DBUtil.updateObject(UPDATE_ACCESS_PWD_SQL, (stmt) -> {
    stmt.setString(1, driverbean.getEmail_addr());
    stmt.setString(2, driverbean.getPass());   // directly from pass_hash form field
    stmt.setLong(3, driverbean.getId());
});
```
SQL: `update driver set email = ?, password = ? where id = ?`

An attacker can POST a chosen `pass_hash` value and have it written verbatim into the `password` column, completely bypassing the intended hashing pipeline and allowing arbitrary credential injection for any driver (compounded by FINDING-01).

**Evidence:**
- `AdminDriverEditForm.java:46`: `private String pass_hash = null;` — no `@Ignore` annotation, no exclusion from Struts binding.
- `AdminDriverEditAction.java:40`: `String pass = adminDriverEditForm.getPass_hash();`
- `AdminDriverEditAction.java:51`: `driverbean.setPass(pass);`

**Recommendation:**
`pass_hash` must never be accepted as HTTP input. Remove the field from the form class (or annotate it as non-bindable) and compute the hash server-side from the user-submitted `pass` field only. Any pre-hashing must happen in the server tier.

---

### FINDING-03 — CRITICAL: cognito_username Field Accepted From HTTP Request

**Severity:** CRITICAL
**File+Line:** `AdminDriverEditForm.java:47`, `AdminDriverEditAction.java:76`

**Description:**
The field `cognito_username` is bound from the HTTP request and is passed directly into the Cognito user update pipeline:

```java
String cognito_username = adminDriverEditForm.getCognito_username();
driverbean.setCognito_username(cognito_username);
// ...
UserUpdateResponse userUpdateResponse = DriverDAO.updateGeneralUserInfo(driverbean);
```

In `updateGeneralUserInfo` (DriverDAO line 607–622), the Cognito username is first fetched from the DB using `driverbean.getId()`, but if not found, the function falls through to `return null`. The attacker-controlled `cognito_username` is set on `driverbean` and then placed into a `UserUpdateRequest` where `username = cognitoUsername` (DriverDAO line 617). An attacker can target the Cognito account of an arbitrary user by supplying a known or guessed `cognito_username`.

**Evidence:**
- `AdminDriverEditForm.java:47`: `private String cognito_username = null;`
- `AdminDriverEditAction.java:76`: `String cognito_username = adminDriverEditForm.getCognito_username();`
- DriverDAO line 617: `UserUpdateRequest.builder() ... .username(cognitoUsername) ...`

**Recommendation:**
`cognito_username` must be resolved exclusively server-side from the authenticated session and verified driver `id` (which itself must pass the ownership check from FINDING-01). It must not be accepted from HTTP input under any circumstances.

---

### FINDING-04 — HIGH: op_code Field Controls Action Branch With No Whitelist Validation

**Severity:** HIGH
**File+Line:** `AdminDriverEditForm.java:45`, `AdminDriverEditAction.java:32, 67, 109, 123, 150, 181`

**Description:**
The `op_code` field is a `String` accepted from the HTTP request and used as an operation discriminator to select which database operation the action executes. There is no whitelist check, no length constraint, and no declarative validation. Each operation branch is guarded by a separate `equalsIgnoreCase` check, but no branch validates that `op_code` is one of the known valid values before processing begins.

This means:
- Any unrecognised `op_code` silently falls through all branches, executing no DB call but also triggering `mapping.findForward(return_code)` where `return_code` is the empty string `""` (Action line 31). This will cause a `NullPointerException` or an unmapped forward runtime error.
- The `validate()` method only validates fields for `edit_general`, `edit_general_user`, and `edit_licence`. Operations `edit_subscription`, `edit_vehicle`, and `check_licenceExist` bypass all form-level validation.

**Evidence:**
- `AdminDriverEditForm.java:45`: `private String op_code = null;`
- No `op_code` entry in validation.xml.
- `validate()` at line 64: only handles two op_code values.
- Action line 31: `String return_code = "";` — default is empty, used verbatim in `findForward`.

**Recommendation:**
Validate `op_code` against an explicit allowlist (enum or `Set<String>`) at the earliest possible point, returning an error for any unrecognised value. Add `op_code` validation to `validation.xml` or to the `validate()` method. Handle the empty `return_code` fallthrough explicitly.

---

### FINDING-05 — HIGH: NullPointerException Risk on op_code in validate()

**Severity:** HIGH
**File+Line:** `AdminDriverEditForm.java:64, 65, 70, 75, 80`

**Description:**
The `validate()` method calls `op_code.equalsIgnoreCase(...)` at line 64 without a null guard. The field is initialised to `null`. If Struts does not bind a value (e.g., the parameter is absent from the request), `op_code` remains `null` and the call throws a `NullPointerException`, which Struts will propagate as an unhandled exception — potentially revealing a stack trace.

The same risk applies to `first_name` (line 65), `last_name` (line 70), `pass` (line 75, 80), and `licence_number` (line 128) — all are called with instance methods without null checks.

**Evidence:**
- Line 28: `private Long id = null;`
- Line 45: `private String op_code = null;`
- Line 64: `if (op_code.equalsIgnoreCase("edit_general") || ...)`  — NPE if op_code is null.
- Line 65: `if (first_name.equalsIgnoreCase(""))` — NPE if first_name is null.
- Line 75: `if (!pass.equalsIgnoreCase(cpass))` — NPE if pass is null.
- Line 128: `licenceNumber.length()` — NPE if licence_number is null.

**Recommendation:**
Use null-safe comparisons throughout: `"edit_general".equalsIgnoreCase(op_code)` (literal on left), or add explicit null guards. Initialise string fields to `""` rather than `null`, or validate null before use.

---

### FINDING-06 — HIGH: validate() Has Business-Logic Side Effects (Sets Request Attributes)

**Severity:** HIGH
**File+Line:** `AdminDriverEditForm.java:100–102, 119–121`

**Description:**
The `validate()` method is called by the Struts framework solely to determine whether validation passes. It is not supposed to mutate application state or set request attributes. This implementation sets `request.setAttribute("arrAdminDriver", arrDriver)` from within `validate()`:

- Lines 100–102 (edit_general/edit_general_user branch):
  ```java
  request.setAttribute("arrAdminDriver", arrDriver);
  ```
- Lines 119–121 (edit_licence branch):
  ```java
  request.setAttribute("arrAdminDriver", arrDriver);
  ```

The data set here is constructed from **unvalidated, user-controlled input** (fields have not yet passed validation). If validation subsequently fails and Struts forwards to the `input` page, the request attributes contain corrupt or attacker-crafted data. This can cause the re-displayed page to render attacker-controlled values and may also confuse downstream code that relies on those attributes being set by the action.

**Evidence:**
- `AdminDriverEditForm.java:87–102`: DriverBean built from raw form fields, placed on request, before `errors` is returned.
- `AdminDriverEditForm.java:111–121`: LicenceBean built from raw form fields, placed on request.

**Recommendation:**
Remove all `request.setAttribute` calls from `validate()`. The action layer should populate request attributes after validation succeeds. The `validate()` method must only accumulate and return `ActionErrors`.

---

### FINDING-07 — HIGH: String Fields Have No Length Constraints

**Severity:** HIGH
**File+Line:** `AdminDriverEditForm.java:29–47`, `validation.xml:60–67`

**Description:**
The following string fields are passed directly into PreparedStatement `setString()` calls with no server-side length validation, no `maxlength` rule in `validation.xml`, and no check in `validate()`:

| Field | Used in DB column | DB operation |
|-------|------------------|-------------|
| `first_name` | `driver.first_name` | UPDATE |
| `last_name` | `driver.last_name` | UPDATE |
| `mobile` | `driver.phone` | UPDATE |
| `email_addr` | `driver.email` | UPDATE |
| `address` | `driver.addr` | UPDATE |
| `location` | `permission.location` | UPDATE |
| `department` | `permission.department` | UPDATE |
| `expiry_date` | `driver.expirydt` | UPDATE (via DateUtil parse) |
| `security_number` | `driver.securityno` | UPDATE |
| `pass` | `driver.password` | UPDATE |

Submitting an excessively long value can cause database truncation errors, exception stack traces, or denial of service. `expiry_date` is passed to `DateUtil.stringToSQLDate()` with no format pre-check; malformed input will propagate a parse exception.

`validation.xml` only declares `required` for `first_name` and `last_name` — no `maxlength` is declared for any field.

**Evidence:**
- `validation.xml:61–66`: only `depends="required"`, no `maxlength` var.
- `AdminDriverEditAction.java:35–51`: all string fields passed to setters without trimming or length checks.
- `DriverDAO.java:580–597`: `setString()` calls with no length guard.

**Recommendation:**
Add `maxlength` constraints in `validation.xml` or in `validate()` for every field that maps to a database column. Values should also be trimmed before persistence.

---

### FINDING-08 — HIGH: app_access Field Accepted Without Whitelist Validation

**Severity:** HIGH
**File+Line:** `AdminDriverEditForm.java:35`, `AdminDriverEditAction.java:37, 48`

**Description:**
The `app_access` field is used to control whether a driver has application access. It is accepted from the HTTP request as an unconstrained String and set directly on the DriverBean:

```java
String app_access = adminDriverEditForm.getApp_access();
driverbean.setApp_access(app_access);
```

There is no validation in `validate()`, no entry in `validation.xml`, and no whitelist (e.g., `"true"`/`"false"` or `"Y"`/`"N"`) enforced anywhere in the form or action. An attacker can supply any string value for this field.

**Evidence:**
- `AdminDriverEditForm.java:35`: `private String app_access = null;`
- `AdminDriverEditAction.java:37`: `String app_access = adminDriverEditForm.getApp_access();`
- `AdminDriverEditAction.java:48`: `driverbean.setApp_access(app_access);`
- No rule for `app_access` in `validation.xml`.

**Recommendation:**
Validate `app_access` against an explicit allowlist of acceptable values before use. Reject any request where the value is not in the whitelist.

---

### FINDING-09 — MEDIUM: Alert Subscription Fields (redImpactAlert, redImpactSMSAlert, driverDenyAlert) Have No Validation

**Severity:** MEDIUM
**File+Line:** `AdminDriverEditForm.java:38–40`, `AdminDriverEditAction.java:152–175`

**Description:**
The three alert toggle fields are accepted from the HTTP request and compared directly against the hardcoded string `"on"` and `""` to decide whether to add or delete subscriptions:

```java
if (redImpactAlert.equals("on") && alertBean.getAlert_id() == null) {
    CompanyDAO.addUserSubscription(...);
} else if (redImpactAlert.equals("")) {
    CompanyDAO.deleteUserSubscription(...);
}
```

Any value other than `"on"` or `""` (e.g., `"OFF"`, `"true"`, `"1"`) silently takes neither branch — the subscription is neither added nor removed, creating a silent no-op that may be surprising and could be abused to bypass expected subscription removals.

There is no validation in `validate()`, no entry in `validation.xml`.

**Evidence:**
- `AdminDriverEditForm.java:38–40`: three string fields, null initialised.
- `AdminDriverEditAction.java:161–175`: exact string comparisons.
- No validation for these fields anywhere.

**Recommendation:**
Validate these fields against the allowlist `{"on", ""}`. Treat any other value as an error. Consider using a boolean or typed enum on the server side rather than a raw string.

---

### FINDING-10 — MEDIUM: expiry_date Accepted Without Format or Range Validation

**Severity:** MEDIUM
**File+Line:** `AdminDriverEditForm.java:32`, `DriverDAO.java:636–638`

**Description:**
The `expiry_date` field is a String accepted from the HTTP request. It is passed to `DateUtil.stringToSQLDate(licencebean.getExpiry_date(), dateFormat)` in `updateDriverLicenceInfo` without any pre-validation of format or sanity. `dateFormat` comes from the session attribute `sessDateFormat`. If the input is malformed, the parse exception propagates up uncaught at the DAO level, potentially exposing a stack trace.

There is no date-format validator in `validation.xml` and no check in `validate()` for the `edit_licence` branch.

**Evidence:**
- `AdminDriverEditForm.java:32`: `private String expiry_date = null;`
- `DriverDAO.java:636–638`: `stmt.setDate(2, DateUtil.stringToSQLDate(licencebean.getExpiry_date(), dateFormat));` — no try/catch.
- No `date` rule in `validation.xml`.

**Recommendation:**
Add a date format validator (Struts Validator supports `date` type) in `validation.xml`, or validate the format in `validate()` for the `edit_licence` op_code branch before the bean is built.

---

### FINDING-11 — MEDIUM: security_number Field Has No Constraints

**Severity:** MEDIUM
**File+Line:** `AdminDriverEditForm.java:33`, `AdminDriverEditAction.java:124`

**Description:**
The `security_number` field (licence card security number — a sensitive identifier) is accepted without any length, format, or character-set validation. It is passed directly to the database:

```java
stmt.setString(3, licencebean.getSecurity_number());
```

Unlike `licence_number`, which has an `isLicenceNumberInvalid()` check, `security_number` has no equivalent guard. No rule exists in `validation.xml` or `validate()`.

**Evidence:**
- `AdminDriverEditForm.java:33`: `private String security_number = null;`
- `DriverDAO.java:641`: `stmt.setString(3, licencebean.getSecurity_number());`
- No validation rule for `security_number`.

**Recommendation:**
Apply the same alphanumeric and maximum-length check that exists for `licence_number`. Add a rule in `validation.xml` or in the `edit_licence` branch of `validate()`.

---

### FINDING-12 — MEDIUM: Missing reset() Override Allows Field Leakage Between Requests

**Severity:** MEDIUM
**File+Line:** `AdminDriverEditForm.java` (entire class — no reset() method)

**Description:**
`ActionForm.reset()` is the Struts mechanism for clearing form fields before population from a new request. Because no `reset()` override is present, in any scenario where the form bean is scoped to session (or reused within a request processing chain), stale values from a previous request can persist into the current one. This is especially dangerous for fields like `id`, `pass_hash`, `cognito_username`, and `op_code`. The struts-config.xml declares `scope="request"` for the actions reviewed, which reduces (but does not eliminate) this risk in the current configuration.

**Evidence:**
- `AdminDriverEditForm.java`: no `reset()` method present.
- `@NoArgsConstructor` provides a constructor but no reset logic.
- `struts-config.xml:316`: `scope="request"` for `/admindriveredit`.

**Recommendation:**
Override `reset()` to nullify or blank-initialise all fields. This is defensive best practice in Struts 1.x and will prevent accidental state leakage if the scope is ever changed to session, or if the form is reused within the same thread context.

---

### FINDING-13 — LOW: Password Comparison Is Case-Insensitive

**Severity:** LOW
**File+Line:** `AdminDriverEditForm.java:75`

**Description:**
The password confirmation check uses `equalsIgnoreCase`:

```java
if (!pass.equalsIgnoreCase(cpass)) {
```

This means passwords differing only in case (e.g., `Secret1` and `secret1`) are accepted as matching. Depending on how the downstream hashing/storage operates, the user may find their password case-insensitively accepted at entry but rejected at login if the stored hash is case-sensitive. It also reduces the effective entropy of the accepted password space.

**Evidence:**
- `AdminDriverEditForm.java:75`: `if (!pass.equalsIgnoreCase(cpass))`

**Recommendation:**
Replace `equalsIgnoreCase` with `equals` for password comparison. Passwords are case-sensitive by convention and should be compared literally.

---

### FINDING-14 — LOW: validation.xml Form Name Case Mismatch Risk

**Severity:** LOW
**File+Line:** `validation.xml:60`, `struts-config.xml:14`

**Description:**
The form is registered in `struts-config.xml` with bean name `adminDriverEditForm` (lowercase `a`), but the `validation.xml` entry uses `AdminDriverEditForm` (uppercase `A`):

```xml
<!-- struts-config.xml line 14 -->
<form-bean name="adminDriverEditForm" type="com.actionform.AdminDriverEditForm"/>

<!-- validation.xml line 60 -->
<form name="AdminDriverEditForm">
```

In Apache Commons Validator as used by Struts 1.x, the form name in `validation.xml` must match the action form bean name in `struts-config.xml` exactly (case-sensitive) for the declarative rules to be applied automatically via the `ValidatorPlugIn`. If the name lookup is case-sensitive in this deployment, **the declarative validation rules in validation.xml are never applied** — the form only uses its programmatic `validate()` method, leaving even `first_name` and `last_name` without the `required` guard from the XML. This would mean the stated presence of declarative rules provides a false sense of coverage.

**Evidence:**
- `struts-config.xml:14`: `name="adminDriverEditForm"`
- `validation.xml:60`: `name="AdminDriverEditForm"`

**Recommendation:**
Normalise the form name across both files. The standard Struts convention is that the `validation.xml` form name matches the struts-config form-bean name exactly. Change `validation.xml` to use `adminDriverEditForm`.

---

### FINDING-15 — INFO: validate() Invoked for /admindriverlicencevalidateexist With validate="true"

**Severity:** INFO
**File+Line:** `struts-config.xml:325–331`, `AdminDriverEditForm.java:64`

**Description:**
The `/admindriverlicencevalidateexist` action uses the same `adminDriverEditForm` with `validate="true"`. When this path is invoked with `op_code=check_licenceExist`, none of the `validate()` branches match (`edit_general`, `edit_general_user`, `edit_licence`), so `validate()` returns an empty `ActionErrors` object without performing any checks. The action then proceeds to query the DB with the user-supplied `licence_number`. While `licence_number` is validated in the `edit_licence` branch, it is **not** validated when `op_code=check_licenceExist`.

**Evidence:**
- `struts-config.xml:328–330`: `validate="true"` for `check_licenceExist` path.
- `AdminDriverEditForm.java:105`: `validate()` only guards `edit_licence` for licence_number.
- `AdminDriverEditAction.java:110`: `String licence_number = adminDriverEditForm.getLicence_number();` used in `DriverDAO.checkDriverByLic(...)` without prior validation.

**Recommendation:**
Add validation for `licence_number` (format and length checks) when `op_code=check_licenceExist`, or refactor the validate method to apply field-level rules regardless of op_code.

---

## 3. SUMMARY TABLE

| ID | Severity | Short Title |
|----|----------|-------------|
| FINDING-01 | CRITICAL | IDOR — driver `id` not tied to session company |
| FINDING-02 | CRITICAL | `pass_hash` accepted from HTTP request |
| FINDING-03 | CRITICAL | `cognito_username` accepted from HTTP request |
| FINDING-04 | HIGH | `op_code` not whitelist-validated |
| FINDING-05 | HIGH | NPE risk on null fields in validate() |
| FINDING-06 | HIGH | Business logic side effects inside validate() |
| FINDING-07 | HIGH | No length constraints on any string field |
| FINDING-08 | HIGH | `app_access` no whitelist check |
| FINDING-09 | MEDIUM | Alert toggle fields no validation |
| FINDING-10 | MEDIUM | `expiry_date` no format/range validation |
| FINDING-11 | MEDIUM | `security_number` no constraints |
| FINDING-12 | MEDIUM | No reset() override |
| FINDING-13 | LOW | Case-insensitive password comparison |
| FINDING-14 | LOW | validation.xml form name case mismatch |
| FINDING-15 | INFO | licence_number not validated for check_licenceExist op_code |

### Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 5 |
| MEDIUM | 4 |
| LOW | 2 |
| INFO | 1 |
| **TOTAL** | **15** |

---

## 4. VALIDATION ADEQUACY ASSESSMENT

The validation.xml rules for `AdminDriverEditForm` are **wholly inadequate**:

- Only 2 of 21 fields (`first_name`, `last_name`) have any declarative rule.
- The only rule applied is `required` — no `maxlength`, no `email`, no `integer`, no `date`.
- The form name case mismatch (FINDING-14) means these two rules may not even be applied by the framework at runtime.
- The programmatic `validate()` covers `op_code` values `edit_general`, `edit_general_user`, and `edit_licence` only. Three operation branches (`edit_subscription`, `edit_vehicle`, `check_licenceExist`) receive zero validation.
- Critically sensitive fields (`id`, `pass_hash`, `cognito_username`, `op_code`, `app_access`) are completely absent from validation configuration.
