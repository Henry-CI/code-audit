# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A29
**Date:** 2026-02-26
**Scope:** ActionForm classes — AdminAlertActionForm, AdminDealerActionForm, AdminDriverAddForm

---

## 1. Source Files Audited

| # | File | Class | Lines |
|---|------|-------|-------|
| 1 | `src/main/java/com/actionform/AdminAlertActionForm.java` | `AdminAlertActionForm` | 75 |
| 2 | `src/main/java/com/actionform/AdminDealerActionForm.java` | `AdminDealerActionForm` | 13 |
| 3 | `src/main/java/com/actionform/AdminDriverAddForm.java` | `AdminDriverAddForm` | 84 |

---

## 2. Reading-Evidence Blocks

### 2.1 AdminAlertActionForm

**Extends:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`

**Fields:**

| Field | Type | Default | Line |
|-------|------|---------|------|
| `alertId` | `int` | `0` (primitive default) | 9 |
| `alertDesc` | `String` | _(none)_ | 10 |
| `alertCode` | `String` | _(none)_ | 11 |
| `arrVehicles` | `ArrayList` (raw) | `new ArrayList()` | 12 |
| `action` | `String` | _(none)_ | 13 |
| `unitIds` | `String[]` | _(none)_ | 14 |
| `alert_id` | `String` | `null` | 15 |
| `impactLevel` | `int` | `0` (primitive default) | 18 |
| `isActive` | `boolean` | `false` (primitive default) | 19 |

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `getAlertId` | `int getAlertId()` | 21 |
| `getAlertDesc` | `String getAlertDesc()` | 24 |
| `getAlertCode` | `String getAlertCode()` | 27 |
| `setAlertId` | `void setAlertId(int alertId)` | 30 |
| `setAlertDesc` | `void setAlertDesc(String alertDesc)` | 33 |
| `setAlertCode` | `void setAlertCode(String alertCode)` | 36 |
| `getArrVehicles` | `ArrayList getArrVehicles()` | 39 |
| `setArrVehicles` | `void setArrVehicles(ArrayList arrVehicles)` | 42 |
| `getAction` | `String getAction()` | 45 |
| `setAction` | `void setAction(String action)` | 48 |
| `getUnitIds` | `String[] getUnitIds()` | 51 |
| `setUnitIds` | `void setUnitIds(String[] unitIds)` | 54 |
| `getImpactLevel` | `int getImpactLevel()` | 57 |
| `setImpactLevel` | `void setImpactLevel(int impactLevel)` | 60 |
| `isActive` | `boolean isActive()` | 63 |
| `setActive` | `void setActive(boolean isActive)` | 66 |
| `getAlert_id` | `String getAlert_id()` | 69 |
| `setAlert_id` | `void setAlert_id(String alert_id)` | 72 |

**Notable absences:** No `validate()` override, no `reset()` override. The class inherits `ActionForm.validate()` (returns empty `ActionErrors`) and `ActionForm.reset()` (no-op) without overriding either.

---

### 2.2 AdminDealerActionForm

**Extends:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`
**Lombok annotations:** `@Getter`, `@Setter`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Default | Line |
|-------|------|---------|------|
| `companyId` | `String` | `null` | 12 |

**Methods (Lombok-generated, not in source):**

| Method | Origin |
|--------|--------|
| `getCompanyId()` | `@Getter` |
| `setCompanyId(String)` | `@Setter` |
| `AdminDealerActionForm()` (constructor) | `@NoArgsConstructor` |

**Notable absences:** No `validate()` override, no `reset()` override.

---

### 2.3 AdminDriverAddForm

**Extends:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`
**Lombok annotations:** `@Getter`, `@Setter`, `@NoArgsConstructor`, `@Slf4j`

**Fields:**

| Field | Type | Default | Line |
|-------|------|---------|------|
| `id` | `Long` | `null` | 22 |
| `first_name` | `String` | `null` | 23 |
| `last_name` | `String` | `null` | 24 |
| `licence_number` | `String` | `null` | 25 |
| `expiry_date` | `String` | `null` | 26 |
| `security_number` | `String` | `null` | 27 |
| `address` | `String` | `null` | 28 |
| `app_access` | `String` | `null` | 29 |
| `mobile` | `String` | `null` | 30 |
| `email_addr` | `String` | `null` | 31 |
| `pass` | `String` | `null` | 32 |
| `cpass` | `String` | `null` | 33 |
| `location` | `String` | `null` | 34 |
| `department` | `String` | `null` | 35 |
| `op_code` | `String` | `null` | 36 |

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `validate` | `ActionErrors validate(ActionMapping, HttpServletRequest)` | 38–59 |
| `getDriverBean` | `DriverBean getDriverBean(String sessCompId)` | 61–83 |
| _(Lombok-generated)_ | `get*()`/`set*()` for each field | — |
| _(Lombok-generated)_ | `AdminDriverAddForm()` (constructor) | — |

**validate() logic detail (lines 38–59):**

| Branch | Condition | Error key | Message key |
|--------|-----------|-----------|-------------|
| B1 | `first_name.equalsIgnoreCase("")` | `"first_name"` | `"error.firstname"` |
| B2 | `last_name.equalsIgnoreCase("")` | `"last_name"` | `"error.lastname"` |
| B3 | `!pass.equalsIgnoreCase(cpass)` | `"pass"` | `"error.pass"` |

---

## 3. Test-Coverage Grep Results

The entire test directory (`src/test/java/`) contains exactly four test files:

```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

Grep for `AdminAlertActionForm`, `AdminDealerActionForm`, `AdminDriverAddForm` across all four files: **zero matches**.

All four tests cover exclusively `com.calibration.*` and `com.util.ImpactUtil`. None import, instantiate, or reference any ActionForm class under audit.

**Coverage conclusion: 0% for all three classes.**

---

## 4. Findings

---

### A29-1 | Severity: CRITICAL | AdminDriverAddForm.validate() — NullPointerException on null first_name

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 41
**Code:**
```java
if( first_name.equalsIgnoreCase("") )
```
`first_name` is initialised to `null` (line 23). When Struts does not bind a `first_name` request parameter, the field remains `null`. Calling `.equalsIgnoreCase("")` on a `null` reference throws `NullPointerException`, which propagates unhandled through Struts and produces a 500 response to the client. The same defect exists on `last_name` (line 47) and on `pass` / `cpass` (line 53). There is no null-guard anywhere in `validate()`.

No test exercises `validate()` with any field value, null or otherwise.

---

### A29-2 | Severity: CRITICAL | AdminDriverAddForm.validate() — NullPointerException on null last_name

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 47
**Code:**
```java
if( last_name.equalsIgnoreCase("") )
```
Same class of defect as A29-1. `last_name` defaults to `null`; a missing form field causes an immediate NPE. Not tested.

---

### A29-3 | Severity: CRITICAL | AdminDriverAddForm.validate() — NullPointerException on null pass or cpass

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 53
**Code:**
```java
if (!pass.equalsIgnoreCase(cpass))
```
Both `pass` and `cpass` default to `null`. If either field is absent from the request, `pass.equalsIgnoreCase(cpass)` throws NPE before the password-match check can produce a useful validation message. Not tested.

---

### A29-4 | Severity: HIGH | AdminDriverAddForm.validate() — zero test coverage of all branches

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 38–59
`validate()` is the only method in the entire project carrying custom validation logic. It has three conditional branches (B1, B2, B3 — see reading-evidence block above). No test covers:
- the happy path (valid form data, empty `ActionErrors` returned),
- branch B1 true (empty first name),
- branch B1 false (non-empty first name),
- branch B2 true (empty last name),
- branch B2 false (non-empty last name),
- branch B3 true (mismatched passwords),
- branch B3 false (matching passwords),
- any combination of multiple simultaneous failures.

Branch coverage: 0 of 6 reachable branches.

---

### A29-5 | Severity: HIGH | AdminDriverAddForm.validate() — case-insensitive empty-string check is semantically incorrect

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 41, 47, 53
**Code:**
```java
first_name.equalsIgnoreCase("")
last_name.equalsIgnoreCase("")
pass.equalsIgnoreCase(cpass)
```
Using `equalsIgnoreCase` for an empty-string sentinel check (`""`) is always equivalent to `equals("")` because case-folding of an empty string is always empty — but this usage pattern indicates copy-paste of a password-comparison idiom into a presence check. More critically, `equalsIgnoreCase` is used for the password comparison on line 53, which means the passwords `"Secret1"` and `"SECRET1"` are treated as equal. Password comparison must be case-sensitive. No test exposes this behaviour. This defect cannot be caught without a test that submits passwords differing only in case.

---

### A29-6 | Severity: HIGH | AdminDriverAddForm.getDriverBean() — op_code field omitted from DriverBean builder call

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 61–79
**Code (relevant excerpt):**
```java
DriverBean driverBean = DriverBean.builder()
        .id(id)
        .first_name(first_name)
        ...
        .cpass(cpass)
        .comp_id(sessCompId)
        .build();
```
`AdminDriverAddForm` declares `op_code` (line 36) and `DriverBean` also declares `op_code` (verified in `src/main/java/com/bean/DriverBean.java`, line 40). However the `getDriverBean()` builder call does not pass `.op_code(op_code)`. The field will silently be `null` in the returned bean regardless of what the user submitted. No test exercises `getDriverBean()` to catch this omission.

---

### A29-7 | Severity: MEDIUM | AdminDriverAddForm — no reset() override; stale form state can persist across requests

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`
Struts session-scoped ActionForms are reused across multiple requests. Without a `reset()` override, fields from a previous form submission (especially `pass`, `cpass`, `unitIds`, checkboxes) remain set if a subsequent request omits those parameters. The boolean field pattern from `AdminAlertActionForm` (finding A29-9) makes this particularly dangerous. Not tested.

---

### A29-8 | Severity: MEDIUM | AdminAlertActionForm — no validate() override; server-side validation entirely absent

**File:** `src/main/java/com/actionform/AdminAlertActionForm.java`
The class binds `alertId`, `alertCode`, `alertDesc`, `unitIds`, `impactLevel`, and `action` but provides no `validate()` override. Struts calls `ActionForm.validate()` which returns an empty `ActionErrors`, meaning all submissions pass validation unconditionally. Fields such as `alertCode` (used as an alert type discriminator) and `impactLevel` (used to control impact-severity logic) are never verified for presence, format, or range. Not tested.

---

### A29-9 | Severity: MEDIUM | AdminAlertActionForm — no reset() override; boolean isActive persists incorrectly across reuse

**File:** `src/main/java/com/actionform/AdminAlertActionForm.java`, line 19
HTTP checkboxes submit no parameter when unchecked. Without a `reset()` override that sets `isActive = false` before each request, a session-scoped form will retain `isActive = true` from a prior submission even when the user unchecks the box. The Struts framework cannot distinguish "checkbox unchecked" from "parameter absent". Not tested.

---

### A29-10 | Severity: MEDIUM | AdminAlertActionForm — raw ArrayList use (unchecked type)

**File:** `src/main/java/com/actionform/AdminAlertActionForm.java`, line 12
```java
private ArrayList arrVehicles = new ArrayList();
```
The field uses a raw `ArrayList` without a type parameter. This suppresses compiler type-safety checks and will generate unchecked-cast warnings when elements are retrieved. No test verifies the expected element type or checks the list contents after population. This is a Java 5+ generics violation.

---

### A29-11 | Severity: MEDIUM | AdminDealerActionForm — no validate() override; companyId is never validated

**File:** `src/main/java/com/actionform/AdminDealerActionForm.java`
`companyId` is the sole field and it defaults to `null`. No `validate()` override is present. Any action that relies on `companyId` being non-null and well-formed will receive `null` without a Struts-level error having been raised. Not tested.

---

### A29-12 | Severity: LOW | AdminAlertActionForm — dual identity fields (alertId vs alert_id) with no reconciliation

**File:** `src/main/java/com/actionform/AdminAlertActionForm.java`, lines 9 and 15
```java
private int alertId;
private String alert_id = null;
```
Two fields represent what appears to be the same concept: an alert identifier. One is a primitive `int` (defaults to `0`), the other is a nullable `String` (defaults to `null`). There is no reconciliation logic, no conversion, and no test that verifies which field an action actually reads or which HTTP parameter name Struts binds to each field. This duplication creates a risk of stale or inconsistent data being used depending on which getter the consuming Action calls.

---

### A29-13 | Severity: LOW | AdminDriverAddForm — entire class has 0% test coverage (Lombok-generated accessors included)

**File:** `src/main/java/com/actionform/AdminDriverAddForm.java`
No test file imports, instantiates, or interacts with `AdminDriverAddForm` in any way. Lombok-generated getters and setters, the constructor, `validate()`, and `getDriverBean()` are all completely untested. While accessor coverage is of lower priority, the untested `validate()` and `getDriverBean()` methods carry the defects documented in A29-1 through A29-6.

---

### A29-14 | Severity: LOW | AdminAlertActionForm — entire class has 0% test coverage

**File:** `src/main/java/com/actionform/AdminAlertActionForm.java`
No test exercises any method in this class. All 18 hand-written accessor methods are untested.

---

### A29-15 | Severity: LOW | AdminDealerActionForm — entire class has 0% test coverage

**File:** `src/main/java/com/actionform/AdminDealerActionForm.java`
No test exercises any Lombok-generated method or the constructor of this class.

---

### A29-16 | Severity: INFO | No reset() override in AdminDealerActionForm

**File:** `src/main/java/com/actionform/AdminDealerActionForm.java`
Single-field form with no `reset()` override. Lower risk than multi-field forms but noted for completeness. If session-scoped, a stale `companyId` from a prior request would be silently reused.

---

## 5. Coverage Gap Summary

| Class | validate() covered | reset() covered | Accessor methods covered | Other methods covered |
|-------|--------------------|-----------------|-------------------------|-----------------------|
| `AdminAlertActionForm` | N/A — not overridden | N/A — not overridden | 0 / 18 | — |
| `AdminDealerActionForm` | N/A — not overridden | N/A — not overridden | 0 / 2 (Lombok) | — |
| `AdminDriverAddForm` | 0 / 6 branches | N/A — not overridden | 0 / 30 (Lombok) | `getDriverBean()`: 0% |

**Total test files referencing these classes: 0 of 4.**
**Total test methods exercising these classes: 0.**

---

## 6. Finding Index

| ID | Severity | Summary |
|----|----------|---------|
| A29-1 | CRITICAL | NPE in validate() when first_name is null |
| A29-2 | CRITICAL | NPE in validate() when last_name is null |
| A29-3 | CRITICAL | NPE in validate() when pass or cpass is null |
| A29-4 | HIGH | validate() has 0% branch coverage (6 branches untested) |
| A29-5 | HIGH | case-insensitive password comparison allows case-variant password bypass |
| A29-6 | HIGH | op_code silently dropped in getDriverBean() builder call |
| A29-7 | MEDIUM | No reset() in AdminDriverAddForm; stale state risk |
| A29-8 | MEDIUM | No validate() in AdminAlertActionForm; all submissions pass unchecked |
| A29-9 | MEDIUM | No reset() in AdminAlertActionForm; boolean isActive persists incorrectly |
| A29-10 | MEDIUM | Raw ArrayList use in AdminAlertActionForm (unchecked type) |
| A29-11 | MEDIUM | No validate() in AdminDealerActionForm; companyId never validated |
| A29-12 | LOW | Dual alert identity fields (alertId/alert_id) with no reconciliation |
| A29-13 | LOW | AdminDriverAddForm: 0% overall test coverage |
| A29-14 | LOW | AdminAlertActionForm: 0% overall test coverage |
| A29-15 | LOW | AdminDealerActionForm: 0% overall test coverage |
| A29-16 | INFO | No reset() in AdminDealerActionForm |
