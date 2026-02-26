# A06 — AdminAlertActionForm.java
**Path:** src/main/java/com/actionform/AdminAlertActionForm.java
**Auditor:** A06
**Date:** 2026-02-26
**Branch:** master

## Reading Evidence

### Fully Qualified Class Name
`com.actionform.AdminAlertActionForm`

### Inheritance
| Line | Relationship | Target |
|------|-------------|--------|
| 7 | `extends` | `org.apache.struts.action.ActionForm` |

No interfaces implemented.

### Fields
| Line | Access | Type | Name |
|------|--------|------|------|
| 9 | `private` | `int` | `alertId` |
| 10 | `private` | `String` | `alertDesc` |
| 11 | `private` | `String` | `alertCode` |
| 12 | `private` | `ArrayList` (raw) | `arrVehicles` |
| 13 | `private` | `String` | `action` |
| 14 | `private` | `String[]` | `unitIds` |
| 15 | `private` | `String` | `alert_id` (initialised `null`) |
| 18 | `private` | `int` | `impactLevel` |
| 19 | `private` | `boolean` | `isActive` |

### Public Methods
| Line | Return | Name | Parameters |
|------|--------|------|------------|
| 21 | `int` | `getAlertId` | — |
| 24 | `String` | `getAlertDesc` | — |
| 27 | `String` | `getAlertCode` | — |
| 30 | `void` | `setAlertId` | `int alertId` |
| 33 | `void` | `setAlertDesc` | `String alertDesc` |
| 36 | `void` | `setAlertCode` | `String alertCode` |
| 39 | `ArrayList` | `getArrVehicles` | — |
| 42 | `void` | `setArrVehicles` | `ArrayList arrVehicles` |
| 45 | `String` | `getAction` | — |
| 48 | `void` | `setAction` | `String action` |
| 51 | `String[]` | `getUnitIds` | — |
| 54 | `void` | `setUnitIds` | `String[] unitIds` |
| 57 | `int` | `getImpactLevel` | — |
| 60 | `void` | `setImpactLevel` | `int impactLevel` |
| 63 | `boolean` | `isActive` | — |
| 66 | `void` | `setActive` | `boolean isActive` |
| 69 | `String` | `getAlert_id` | — |
| 72 | `void` | `setAlert_id` | `String alert_id` |

### Annotations
None — on either the class or any method.

### struts-config.xml Mappings Using This Form

**Form bean declaration** (struts-config.xml line 33):
```xml
<form-bean name="adminAlertActionForm" type="com.actionform.AdminAlertActionForm"/>
```

**Action mapping 1** — list/display action (struts-config.xml lines 257–261):
```xml
<action
    path="/adminalert"
    type="com.action.AdminAlertAction">
    <forward name="adminalerts" path="AdminAlertDefinition"/>
</action>
```
Note: this mapping does NOT reference `adminAlertActionForm` by `name=`, so the form is NOT bound here. `AdminAlertAction` reads `action` directly from `request.getParameter("action")`.

**Action mapping 2** — add/subscribe action (struts-config.xml lines 294–301):
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
`validate="true"` is declared, meaning Struts will call the form's `validate()` method before executing the action.

### validation.xml Rules for This Form
There is **no entry** for `adminAlertActionForm` (or any variant of that name) in validation.xml. The file defines rules only for `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`.

---

## Findings

### FINDING 1
**Severity:** HIGH
**Title:** No `validate()` method — form performs zero server-side validation despite `validate="true"`

**Description:**
`AdminAlertActionForm` does not override the `validate()` method inherited from `ActionForm`. The inherited default returns an empty `ActionErrors` collection, which means validation always passes. The `/adminAlertAdd` action mapping declares `validate="true"`, so Struts calls `validate()` before executing `AdminAddAlertAction` — but the call does nothing. All fields accepted from the HTTP request (`alertDesc`, `alertCode`, `alert_id`, `unitIds`, `impactLevel`) pass through without any server-side check.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` — entire class (no `validate()` override exists)
- `src/main/webapp/WEB-INF/struts-config.xml` line 298: `validate="true"`

**Code Evidence:**
```java
// AdminAlertActionForm.java — no validate() override present
public class AdminAlertActionForm extends ActionForm {
    // only getter/setter pairs; validate() is never overridden
}
```
```xml
<!-- struts-config.xml line 298 -->
validate="true"
```

**Recommendation:**
Override `validate()` in `AdminAlertActionForm`. At minimum: require `alert_id` to be non-null and match `^\d+$` (integer-only) before it reaches `Integer.parseInt()` in `CompanyDAO.addUserSubscription`; constrain `alertDesc` and `alertCode` to a maximum length; validate `impactLevel` is within an expected numeric range.

---

### FINDING 2
**Severity:** HIGH
**Title:** No validation.xml rules for `adminAlertActionForm` — declarative validation layer entirely absent

**Description:**
The Struts ValidatorPlugIn is registered and validation.xml is loaded. However, there is no `<form name="adminAlertActionForm">` block in validation.xml. This means declarative field-level validation (required, minlength, maxlength, integer, regex) is not applied to any field in this form. Combined with Finding 1 (no programmatic `validate()` either), all field constraints are completely absent at the form layer.

**File + Line:**
- `src/main/webapp/WEB-INF/validation.xml` — entire file (no entry for `adminAlertActionForm`)
- `src/main/webapp/WEB-INF/struts-config.xml` lines 586–591 (ValidatorPlugIn registration)

**Code Evidence:**
```xml
<!-- validation.xml contains only these three forms: -->
<form name="loginActionForm"> ... </form>
<form name="adminRegisterActionForm"> ... </form>
<form name="AdminDriverEditForm"> ... </form>
<!-- adminAlertActionForm is absent -->
```

**Recommendation:**
Add a `<form name="adminAlertActionForm">` block to validation.xml. Apply `required` and `integer` to `alert_id`; apply `required` and `maxlength` to `alertDesc` and `alertCode`; apply `integer` and a `range` check to `impactLevel`.

---

### FINDING 3
**Severity:** HIGH
**Title:** `alert_id` (String) passed directly to `Integer.parseInt()` without validation — NumberFormatException / denial-of-service

**Description:**
`AdminAddAlertAction` retrieves `alertAction.getAlert_id()` and passes it as the second argument to `CompanyDAO.addUserSubscription(String userId, String alertId)`. That method calls `Integer.parseInt(alertId)` without any guard (CompanyDAO.java line 867). Since `alert_id` is a raw, unbounded `String` field populated directly from HTTP form submission, a non-numeric value (empty string, letters, oversized value) causes an unhandled `NumberFormatException`. The action has no try/catch around this path, so the exception propagates and may expose a stack trace or disrupt the request.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` line 15: field declaration
- `src/main/java/com/action/AdminAddAlertAction.java` line 28: `alertAction.getAlert_id()` consumed without validation
- `src/main/java/com/dao/CompanyDAO.java` line 867: `Integer.parseInt(alertId)`

**Code Evidence:**
```java
// AdminAlertActionForm.java line 15
private String alert_id = null;

// AdminAddAlertAction.java line 28
CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());

// CompanyDAO.java line 867
stmt.setInt(2, Integer.parseInt(alertId));
```

**Recommendation:**
Validate `alert_id` in `validate()` (or via validation.xml) to confirm it matches `^\d+$` and is non-null/non-empty before the action executes. Add a catch for `NumberFormatException` in the DAO or action as a defence-in-depth measure.

---

### FINDING 4
**Severity:** MEDIUM
**Title:** `alert_id` is a client-supplied subscription identifier — potential for IDOR against other users' subscriptions

**Description:**
The `/adminAlertAdd` action binds `alert_id` from the HTTP request form and writes a `user_subscription` row associating the session's `sessUserId` with the client-supplied `alert_id`. Although the row is written for the authenticated user's own `user_id`, the `subscription_id` value is entirely attacker-controlled. If subscription/alert IDs are sequential integers, an authenticated user can subscribe to (or, via a companion delete action) unsubscribe from any alert in the system by enumerating `alert_id` values. There is no server-side check that the supplied `alert_id` is a legitimate, active alert that the user is permitted to reference.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` line 15: `alert_id` field
- `src/main/java/com/action/AdminAddAlertAction.java` lines 28, 31
- `src/main/java/com/dao/CompanyDAO.java` lines 865–868

**Code Evidence:**
```java
// AdminAddAlertAction.java lines 27–32
if (src.equalsIgnoreCase("alert")) {
    CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
    ...
} else if (src.equalsIgnoreCase("report")) {
    CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
    ...
}
```
```java
// CompanyDAO.java lines 865–868
DBUtil.updateObject("insert into user_subscription(user_id, subscription_id) values(?, ?)", stmt -> {
    stmt.setInt(1, Integer.parseInt(userId));
    stmt.setInt(2, Integer.parseInt(alertId));  // alertId is fully attacker-controlled
});
```

**Recommendation:**
Before inserting the subscription, query the database to verify that the supplied `alert_id` refers to a real, active alert/report record. Consider whether the list of valid alert IDs should be fetched server-side from `CompanyDAO.getAlertList()` / `getReportList()` and the client-supplied value validated against that list, rather than trusting the submitted ID directly.

---

### FINDING 5
**Severity:** MEDIUM
**Title:** String fields `alertDesc` and `alertCode` have no length constraint

**Description:**
`alertDesc` and `alertCode` are `String` fields with no maximum-length validation at either the form layer or in validation.xml. If these fields are stored in the database or rendered in a UI, an oversized input could cause database truncation errors, application exceptions, or stored cross-site scripting (if rendered unescaped). There is no `maxlength` rule applied anywhere.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` lines 10–11

**Code Evidence:**
```java
private String alertDesc;   // line 10 — no length constraint
private String alertCode;   // line 11 — no length constraint
```

**Recommendation:**
Add `maxlength` validator rules in validation.xml for both `alertDesc` and `alertCode` appropriate to the corresponding database column lengths. If these fields are rendered in JSP output, ensure they are HTML-escaped.

---

### FINDING 6
**Severity:** MEDIUM
**Title:** `impactLevel` (`int`) has no range validation

**Description:**
`impactLevel` is an `int` field bound from the HTTP request. Struts will attempt to convert the submitted string to `int` (throwing a type conversion error if non-numeric), but there is no validation that the value falls within an expected range (e.g. 1–5 or whatever the application domain defines). An out-of-range integer could cause unexpected behaviour in business logic that uses this field to classify impact severity. Additionally, if Struts type-conversion fails silently and leaves the field at its default (0), logic that treats 0 as a valid level may behave incorrectly.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` line 18

**Code Evidence:**
```java
private int impactLevel;  // line 18 — no range validated
```

**Recommendation:**
Add an `intRange` validator rule in validation.xml (or check in `validate()`) to confirm `impactLevel` is within the permitted domain values.

---

### FINDING 7
**Severity:** MEDIUM
**Title:** `unitIds` (String array) has no validation — each element is unvalidated

**Description:**
`unitIds` is a `String[]` field populated from multi-value HTTP form parameters. No validation exists to check that the array is non-null, that its length is bounded (protection against oversized submissions), or that each element is a valid numeric unit identifier. If downstream code passes elements of `unitIds` to a DAO method that calls `Integer.parseInt()` or uses them in SQL, each element is a potential injection point or crash vector.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` line 14

**Code Evidence:**
```java
private String[] unitIds;  // line 14 — no validation of elements or array size
```

**Recommendation:**
In `validate()`, iterate `unitIds` and confirm each element matches `^\d+$`. Enforce a reasonable maximum array length to prevent resource exhaustion.

---

### FINDING 8
**Severity:** LOW
**Title:** Raw `ArrayList` type used without generics

**Description:**
`arrVehicles` is declared as a raw `ArrayList` (line 12), meaning it carries no compile-time type safety. This is a code quality concern that can mask type errors and makes the form contract unclear. It is not directly exploitable but contributes to overall code fragility.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` line 12

**Code Evidence:**
```java
private ArrayList arrVehicles = new ArrayList();  // raw type, no generic parameter
```

**Recommendation:**
Parameterise the field with the intended element type, e.g. `ArrayList<SomeBean>`.

---

### FINDING 9
**Severity:** LOW
**Title:** Duplicate / redundant alert identifier fields (`alertId` int and `alert_id` String)

**Description:**
The form exposes two fields that appear to represent the same concept: `alertId` (primitive `int`, line 9) and `alert_id` (`String`, line 15). Only `alert_id` is actually used by `AdminAddAlertAction`. The `alertId` field is populated from the request but never consumed in any visible action, creating dead surface area that increases the attack surface without serving a purpose, and introduces confusion about the authoritative field.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` lines 9 and 15

**Code Evidence:**
```java
private int alertId;         // line 9 — not used by any identified action
private String alert_id = null;  // line 15 — used by AdminAddAlertAction
```

**Recommendation:**
Remove the unused `alertId` field. If it is required by another action not reviewed here, document its purpose and add validation for it.

---

### FINDING 10
**Severity:** INFO
**Title:** `action` field on form shadows the Struts `action` request parameter pattern

**Description:**
The form includes a field named `action` (line 13). `AdminAlertAction` reads the action discriminator directly from `request.getParameter("action")` rather than from the form, so the form field is not used there. However, having a field named `action` on the form could cause unexpected binding behaviour or confusion about which source is canonical. This is informational.

**File + Line:**
- `src/main/java/com/actionform/AdminAlertActionForm.java` line 13

**Code Evidence:**
```java
private String action;  // line 13
```

**Recommendation:**
Rename the field to something less ambiguous (e.g. `formAction` or `operationType`) to avoid confusion with the Struts action discriminator pattern.

---

## Checklist Coverage

### 1. Secrets and Configuration
NOT APPLICABLE to this file. `AdminAlertActionForm` is an ActionForm bean with no configuration, credentials, or connection setup.

### 2. Authentication and Authorization
PARTIAL CONCERN — MEDIUM finding raised (Finding 4). The form's `alert_id` field is client-controlled and used to write database records linked to the session user without verifying the submitted ID is a valid, permitted alert. No authorization check exists in the action or DAO to confirm the subscription target is legitimate. The broader question of whether the `/adminAlertAdd` endpoint is protected by an admin session check is outside the form itself but should be verified in the filter/interceptor chain.

### 3. Input Validation and Injection
FAIL — multiple findings raised:
- No `validate()` override (Finding 1).
- No validation.xml rules (Finding 2).
- `alert_id` String passed to `Integer.parseInt()` without validation (Finding 3).
- `alertDesc` and `alertCode` unconstrained strings (Finding 5).
- `impactLevel` unconstrained integer (Finding 6).
- `unitIds` array elements unvalidated (Finding 7).
SQL injection risk is mitigated in the DAO by use of prepared statements (`stmt.setInt()`), so no direct SQLi finding is raised for the fields that reach the DAO — however this mitigation is in the DAO, not in the form.

### 4. Session and CSRF
NOT APPLICABLE at the form level. CSRF protection in Struts 1.x is not handled by the ActionForm. The `/adminAlertAdd` mapping has `validate="true"` and `scope="request"` which is correct scope. CSRF token presence/absence should be reviewed at the JSP/filter layer.

### 5. Data Exposure
LOW CONCERN — the form itself does not produce output. The `arrVehicles` raw ArrayList (Finding 8) is a data quality issue. If `alertDesc` or `alertCode` values are echoed back in JSP without escaping, XSS is a risk — this is noted in Finding 5 but requires JSP-layer review to confirm.

### 6. Dependencies
NOT APPLICABLE to this file.

### 7. Build and CI
NOT APPLICABLE to this file.

### Struts 1.x — ActionForm Specific Checks
| Check | Result |
|-------|--------|
| `validate()` method exists and validates all fields | FAIL — method is absent entirely |
| validation.xml rules cover all fields | FAIL — no entry for this form in validation.xml |
| Numeric fields validated as numeric before use | FAIL — `alert_id` (String→int) has no pre-validation; `impactLevel` has no range check |
| String fields length-constrained | FAIL — `alertDesc`, `alertCode` have no maxlength constraint |
| Form exposes IDOR-risky fields (companyId, userId, etc.) | CONCERN — `alert_id` is client-supplied and used directly as a database FK without server-side existence/permission check (Finding 4); `unitIds` array is also fully client-controlled |
