# Security Audit Report: AdminTrainingsActionForm.java
**Audit Run:** audit/2026-02-26-01
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** Automated Security Review
**Stack:** Apache Struts 1.3.10 (not Spring)

---

## 1. Reading Evidence

### Package and Class
- **File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java`
- **Package:** `com.actionform`
- **Class:** `AdminTrainingsActionForm extends org.apache.struts.action.ActionForm`
- **Lombok annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`

### Fields
| Line | Type | Name | Default |
|------|------|------|---------|
| 14 | `String` | `action` | `null` |
| 16 | `Long` | `driver` | `null` |
| 17 | `Long` | `manufacturer` | `null` |
| 18 | `Long` | `type` | `null` |
| 19 | `Long` | `fuelType` | `null` |
| 20 | `String` | `trainingDate` | `null` |
| 21 | `String` | `expirationDate` | `null` |
| 23 | `Long` | `training` | `null` |

All getters/setters are Lombok-generated. No explicit getter/setter overrides are present.

### `validate()` Method
Not overridden. `AdminTrainingsActionForm` inherits the no-op `validate()` from `ActionForm`, which returns an empty `ActionErrors` collection. No programmatic validation logic exists in this class.

### `reset()` Method
Not overridden. `AdminTrainingsActionForm` inherits the no-op `reset()` from `ActionForm`. No fields are explicitly reset between requests.

### Struts-Config Mapping (`/trainings`) — struts-config.xml lines 283-292
```xml
<action
    path="/trainings"
    type="com.action.AdminTrainingsAction"
    name="AdminTrainingsActionForm"
    scope="request"
    validate="false">
    <forward name="operatortraining" path="OperatorTrainingDefinition"/>
    <forward name="success"          path="OperatorTrainingDefinition"/>
    <forward name="failure"          path="/adminmenu.do?action=home"/>
</action>
```
| Attribute | Value |
|-----------|-------|
| scope | `request` |
| validate | **`false`** — framework validation is explicitly disabled |
| input | not set |

### validation.xml Coverage
`validation.xml` defines declarative rules for exactly three forms:
- `loginActionForm` (lines 23-30)
- `adminRegisterActionForm` (lines 32-58)
- `AdminDriverEditForm` (lines 60-67)

`AdminTrainingsActionForm` has **no entry** in `validation.xml`. Zero fields are covered by declarative validation.

---

## 2. Findings

---

### FINDING-01 — HIGH: Struts Validation Disabled and No Declarative Rules — All Fields Unvalidated

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml` line 288; `src/main/webapp/WEB-INF/validation.xml` (absence)
**Category:** Input Validation

**Description:**
The action mapping for `/trainings` sets `validate="false"`, which instructs the Struts framework to skip calling `AdminTrainingsActionForm.validate()` and to bypass the Commons Validator plug-in entirely before dispatching to `AdminTrainingsAction.execute()`. Compounding this, `validation.xml` contains no `<form name="AdminTrainingsActionForm">` block, so even if `validate` were switched to `true` there would be no rules to enforce. Additionally, the form class itself does not override `validate()`, so there is no programmatic fallback. The net result is that all eight fields (`action`, `driver`, `manufacturer`, `type`, `fuelType`, `trainingDate`, `expirationDate`, `training`) reach the action class with no type, format, presence, or range checking performed by the form layer.

**Evidence:**
```xml
<!-- struts-config.xml lines 283-292 -->
<action
    path="/trainings"
    ...
    validate="false">
```
`validation.xml`: no `<form name="AdminTrainingsActionForm">` element present anywhere in the file.

`AdminTrainingsActionForm.java`: no override of `validate(ActionMapping, HttpServletRequest)`.

**Recommendation:**
1. Set `validate="true"` on the `/trainings` mapping in `struts-config.xml`.
2. Add a `<form name="AdminTrainingsActionForm">` block to `validation.xml` with at minimum:
   - `action`: `required`; `mask` rule restricting to `^(add|delete)$`.
   - `driver`, `manufacturer`, `type`, `fuelType`: `required` (conditional on `action=add`); `long` type check.
   - `training`: `required` (conditional on `action=delete`); `long` type check.
   - `trainingDate`, `expirationDate`: `required` (conditional on `action=add`); `date` mask matching the allowed format.
3. As a defence-in-depth measure, override `validate()` in `AdminTrainingsActionForm` to perform programmatic checks where declarative rules are insufficient (e.g., cross-field date ordering).

---

### FINDING-02 — HIGH: `action` Field Defaults to `null` — NullPointerException in Consumer

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java` line 14; `src/main/java/com/action/AdminTrainingsAction.java` line 25
**Category:** Input Validation / Robustness

**Description:**
The `action` field is declared as `String` with a default value of `null`. The consuming action class (`AdminTrainingsAction`) passes the return value of `getAction()` directly to a `switch` statement without a null guard. In Java, switching on a `null` `String` throws `NullPointerException` unconditionally. Because `validate="false"` is set and no `validate()` override exists in the form, there is no opportunity to catch the null before it reaches the switch. The form class is the correct place to enforce that `action` is non-null; it currently provides no such guarantee.

**Evidence:**
```java
// AdminTrainingsActionForm.java line 14
private String action = null;   // default null, no required constraint
```
```java
// AdminTrainingsAction.java line 25 — NPE if getAction() returns null
switch (trainingsForm.getAction()) {
    case "add":    ...
    case "delete": ...
    default:       return null;
}
```
No null-check or blank-check is present between form population and the switch.

**Recommendation:**
Override `validate()` in `AdminTrainingsActionForm` to add an `ActionError` when `action` is null or blank, and return a non-empty `ActionErrors` to cause the framework to redirect to the `input` page rather than calling `execute()`. Additionally, set `validate="true"` (see FINDING-01) so the override is actually invoked.

---

### FINDING-03 — HIGH: Date Fields Stored as Raw `String` — No Type Safety or Format Contract

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java` lines 20-21
**Category:** Type Safety / Input Validation

**Description:**
`trainingDate` and `expirationDate` are declared as `String` fields. Struts 1 binds HTTP request parameters as strings, so the type declaration is not itself the problem; the problem is that the form class provides no parsing, no format validation, and no type conversion to a well-typed date representation. These raw strings are passed directly from the form to `TrainingDAO.addTraining()` via `DriverTrainingBean`, where `DateUtil.stringToSQLDate()` attempts to parse them using `SimpleDateFormat`. `SimpleDateFormat` defaults to `setLenient(true)`, silently normalising out-of-range values (e.g., month 13 becomes month 1 of the next year). A completely unparseable string causes a swallowed `ParseException` followed by `Objects.requireNonNull(null)` throwing `NullPointerException` in `DateUtil`, resulting in an unhandled server error. There is no server-side check that `expirationDate >= trainingDate`.

**Evidence:**
```java
// AdminTrainingsActionForm.java lines 20-21
private String trainingDate   = null;
private String expirationDate = null;
```
No parsing, format mask, or cross-field check exists anywhere in the form class.

```java
// DateUtil.java (referenced from AdminTrainingsAction.java) — lenient parse, NPE on failure
formatter = new SimpleDateFormat(dateFormat);       // lenient=true by default
try {
    date = formatter.parse(str_date);
} catch (ParseException e) {
    System.out.println("Exception :" + e);          // exception swallowed
}
dte = new java.sql.Date(Objects.requireNonNull(date).getTime()); // NPE if parse failed
```

**Recommendation:**
At minimum, add a `validate()` override in `AdminTrainingsActionForm` that:
1. Verifies `trainingDate` and `expirationDate` are non-null and non-blank when `action` is `"add"`.
2. Attempts to parse each date using `SimpleDateFormat` with `setLenient(false)` to confirm the format matches the expected pattern.
3. Checks that the parsed expiration date is on or after the parsed training date.
Return `ActionErrors` containing descriptive messages for each failure so the user can correct the input. Separately, fix `DateUtil.stringToSQLDate` to use `setLenient(false)` and to propagate or handle `ParseException` rather than swallowing it.

---

### FINDING-04 — MEDIUM: No `reset()` Override — Stale Field State on Form Reuse

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java`
**Category:** Data Integrity

**Description:**
`AdminTrainingsActionForm` does not override `reset(ActionMapping, HttpServletRequest)`. The inherited no-op `reset()` from `ActionForm` leaves all fields at whatever value they held from the previous request population. The mapping is `scope="request"` (struts-config.xml line 287), which means a new form instance is created per request, so field bleed-over between requests is not a practical concern under normal conditions. However, the form class itself provides no explicit reset contract. If the scope is ever changed to `session`, all fields from a prior request would persist and could be acted upon without the user re-submitting them. The absence of `reset()` is a design gap that makes the form fragile under refactoring.

**Evidence:**
```java
// AdminTrainingsActionForm.java — no reset() method
// struts-config.xml line 287
scope="request"   // currently request-scoped; safe today, fragile under scope change
```

**Recommendation:**
Add an explicit `reset()` override that sets all fields to `null` (or appropriate defaults). This makes the contract clear and makes the form safe if scope is ever changed to `session`.

---

### FINDING-05 — MEDIUM: `Long` ID Fields Accept Any Arbitrary Value — No Range or Ownership Constraint at Form Level

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java` lines 16-19, 23
**Category:** IDOR Risk / Input Validation

**Description:**
The fields `driver`, `manufacturer`, `type`, `fuelType`, and `training` are typed as `Long` (auto-boxed from `long`). The `Long` type provides implicit numeric coercion from the HTTP parameter string (via Struts' `BeanUtils` population), but imposes no constraint on the value itself. Any positive or negative integer can be submitted. There is no minimum/maximum range check, no check against an enumeration of valid values for `type` and `fuelType`, and no check that the submitted `driver` or `training` id exists within the authenticated admin's company. The form layer is the earliest point at which oversized, negative, or zero values could be rejected cheaply without a database round-trip. All such constraints are currently absent. This contributes directly to the IDOR risk documented in the companion `AdminTrainingsAction.md` report (FINDING-01 of that report), because the form passes arbitrary foreign-key values to the DAO without any sanitisation.

**Evidence:**
```java
// AdminTrainingsActionForm.java lines 16-19, 23
private Long driver       = null;   // no range check
private Long manufacturer = null;   // no range check
private Long type         = null;   // no enum constraint
private Long fuelType     = null;   // no enum constraint
private Long training     = null;   // no range check; used directly in DELETE
```
No `validate()` override enforces constraints on any of these fields.

**Recommendation:**
At minimum, add a `validate()` override that rejects null, zero, or negative values for all ID fields that are required for the chosen operation. For `type` and `fuelType`, consider validating against a known set of valid identifiers (loaded from application context or a static enum) to prevent insecure direct object reference at the form level. Company-scope ownership checks belong in the action/DAO layer (see companion report), but basic range rejection is appropriate here.

---

### FINDING-06 — LOW: `action` Field Accepts Unbounded String — No Allowlist Constraint

**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java` line 14
**Category:** Input Validation

**Description:**
The `action` field is an unbounded `String` with no length limit, no character mask, and no allowlist enforcement. The consuming code in `AdminTrainingsAction` handles only `"add"` and `"delete"` via a `switch` statement; any other value falls through to the `default: return null` branch and is silently ignored. While this does not currently lead to a directly exploitable code path, the form class should enforce an allowlist at the type/validation level rather than relying on silent discard in the action. Excessively long `action` values could also contribute to log spam or, in edge cases, trigger unexpected behaviour in logging or monitoring tooling.

**Evidence:**
```java
// AdminTrainingsActionForm.java line 14
private String action = null;   // unbounded, no mask, no allowlist
```
No `validate()` override restricts `action` to `"add"` or `"delete"`.

**Recommendation:**
Add a `validate()` override (or declarative `mask` rule in `validation.xml`) that rejects any value of `action` not in `{"add", "delete"}` and limits the field length to a small maximum (e.g., 10 characters).

---

### FINDING-07 — INFO: Lombok `@NoArgsConstructor` and `@Getter`/`@Setter` Suppress Explicit Control Over Field Lifecycle

**Severity:** INFO
**File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java` lines 9-10, 12
**Category:** Design

**Description:**
Lombok annotations (`@Getter`, `@Setter`, `@NoArgsConstructor`) are used to generate all accessor methods and the no-argument constructor. This is not a security vulnerability in itself, but it means there is no opportunity in the current source to add validation logic inside a setter (e.g., range-checking `driver` on set). If a future developer wishes to add per-field sanitisation within a setter, they will need to either remove the Lombok annotation and write the setter manually, or add a Lombok-incompatible custom setter, which can be a source of confusion. The use of `@Slf4j` imports a logger but no logging call is present in the class (because the class is currently empty of methods), meaning the logger import is dead code.

**Evidence:**
```java
// AdminTrainingsActionForm.java lines 3-12
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
...
@Getter
@Setter
@Slf4j
@NoArgsConstructor
public class AdminTrainingsActionForm extends ActionForm {
    // no methods; @Slf4j logger is unused
}
```

**Recommendation:**
Remove the unused `@Slf4j` annotation and its import to eliminate dead code. Consider whether per-field validation belongs in setters; if so, write explicit setters rather than relying on Lombok for security-sensitive fields.

---

## 3. Categories With No Issues

**Sensitive Fields:** The form does not contain password, credential, token, PII (beyond a driver ID foreign key), or payment data fields. The date fields and ID fields are operational data. No sensitive fields requiring encryption, masking, or special handling are present in this class.

**SQL Injection (form layer):** SQL injection is not a concern at the ActionForm layer. The form class performs no SQL operations. SQL injection risk is assessed in the companion `AdminTrainingsAction.md` and `TrainingDAO` reports. For reference, the DAO uses parameterised `PreparedStatement` queries with typed setters; no concatenation is used.

---

## 4. Finding Summary

| ID | Severity | Category | Title |
|----|----------|----------|-------|
| FINDING-01 | HIGH | Input Validation | Struts validation disabled and no declarative rules — all fields unvalidated |
| FINDING-02 | HIGH | Input Validation / Robustness | `action` field defaults to `null` — NPE in consumer action |
| FINDING-03 | HIGH | Type Safety / Input Validation | Date fields stored as raw `String` — no format contract or cross-field check |
| FINDING-04 | MEDIUM | Data Integrity | No `reset()` override — stale field state on potential scope change |
| FINDING-05 | MEDIUM | IDOR Risk / Input Validation | `Long` ID fields accept any arbitrary value — no range or ownership constraint |
| FINDING-06 | LOW | Input Validation | `action` field accepts unbounded string — no allowlist at form level |
| FINDING-07 | INFO | Design | `@Slf4j` logger unused; Lombok suppresses explicit setter control |

**Count by severity:**
- CRITICAL: 0
- HIGH: 3
- MEDIUM: 2
- LOW: 1
- INFO: 1
- **Total: 7**
