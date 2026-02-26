# Security Audit Report: AdminUnitAssignForm

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** CIG Security Audit (automated pass)
**Stack:** Apache Struts 1.3.10

---

## Files Examined

| File | Purpose |
|------|---------|
| `src/main/java/com/actionform/AdminUnitAssignForm.java` | Form bean under audit |
| `src/main/webapp/WEB-INF/validation.xml` | Struts Commons Validator configuration |
| `src/main/webapp/WEB-INF/struts-config.xml` | Action mappings for this form |
| `src/main/java/com/action/AdminUnitAssignAction.java` | Action class consuming this form |
| `src/main/java/com/dao/UnitDAO.java` | DAO methods called by the action |
| `src/main/java/com/action/PandoraAction.java` | Base action class |

---

## Reading Evidence

### Package and Class

```
Package : com.actionform
Class   : AdminUnitAssignForm
Extends : org.apache.struts.action.ActionForm
Lombok  : @Data (generates getters/setters/equals/hashCode/toString)
          @NoArgsConstructor (generates no-arg constructor)
```

### Fields

| # | Name | Declared Type | Notes |
|---|------|--------------|-------|
| 1 | `id` | `String` | Assignment record primary key |
| 2 | `unit_id` | `String` | Foreign key — equipment/unit record |
| 3 | `company_id` | `String` | Foreign key — company/tenant record |
| 4 | `start` | `String` | Assignment start date (locale-formatted string) |
| 5 | `end` | `String` | Assignment end date (locale-formatted string) |

Note: `java.util.Date` is imported at line 7 but is not used anywhere in the class. It is dead import.

### validate() Details

The class does **not** override `validate()`. No server-side validation logic exists inside the form bean itself. Validation is delegated entirely to the Struts Commons Validator framework via `validation.xml`.

### reset() Details

The class does **not** override `reset()`. Struts will not clear fields between requests for this form; field values persist from one population to the next within the same request scope.

### validation.xml Rules for This Form

The `validation.xml` file defines rules for exactly three forms:

1. `loginActionForm`
2. `adminRegisterActionForm`
3. `AdminDriverEditForm`

**`adminUnitAssignForm` is entirely absent from `validation.xml`.** No `<form name="adminUnitAssignForm">` element exists. Despite the action mapping in `struts-config.xml` declaring `validate="true"` for the `/adminunitassign` path, Commons Validator has no rules to enforce — it will pass all submissions through without constraint.

### struts-config.xml Action Mappings

```xml
<!-- Path 1 — mutating actions (add / delete) -->
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

<!-- Path 2 — AJAX overlap-check -->
<action
    path="/assigndatesvalid"
    name="adminUnitAssignForm"
    scope="request"
    type="com.action.AdminUnitAssignAction"
    validate="false">
</action>
```

---

## Findings

---

### FINDING-01

**Severity:** HIGH
**Category:** Input Validation — Missing Server-Side Validation (no validation.xml entry)
**File:** `src/main/webapp/WEB-INF/validation.xml` (entire file) /
         `src/main/webapp/WEB-INF/struts-config.xml` lines 343–350
**Description:**
`adminUnitAssignForm` is completely absent from `validation.xml`. The `/adminunitassign` action mapping declares `validate="true"`, which normally triggers Commons Validator; however, because no `<form name="adminUnitAssignForm">` entry exists, the validator silently passes every submission with no field-level checks applied. All five form fields (`id`, `unit_id`, `company_id`, `start`, `end`) reach the action and DAO layers without any framework-enforced presence, length, format, or character-set constraints.

**Evidence:**
- `validation.xml` contains three `<form>` entries; none is named `adminUnitAssignForm`.
- `struts-config.xml` line 347: `validate="true"` — the intent to validate exists but the rules do not.
- `AdminUnitAssignForm.java`: no `validate()` override; no inline validation.

**Recommendation:**
Add a `<form name="adminUnitAssignForm">` block to `validation.xml` with at minimum:
- `unit_id` — `required`, `integer`, positive range (> 0).
- `company_id` — `required`, `integer`, positive range (> 0).
- `start` — `required`, date format matching the session date format.
- `end` — optional, date format matching the session date format (when present, must be >= start; enforce in `validate()` override).
- `id` — `required` only when `action=delete`, `integer`.

---

### FINDING-02

**Severity:** HIGH
**Category:** IDOR — Unvalidated `id` Parameter Controls Direct Record Deletion
**File:** `src/main/java/com/action/AdminUnitAssignAction.java` lines 25, 52–53 /
         `src/main/java/com/dao/UnitDAO.java` lines 78–89
**Description:**
When `action=delete` is submitted, the raw request parameter `id` (read directly via `getRequestParam`, bypassing the form bean entirely) is passed to `UnitDAO.deleteAssignment(id)`. The DAO executes `DELETE FROM unit_company WHERE id = ?` with no ownership or tenancy check. Any authenticated admin who can reach `/adminunitassign` can delete any assignment record in the database by supplying an arbitrary numeric `id`, regardless of which company that assignment belongs to. There is no verification that the targeted `unit_company` row belongs to the session company (`sessCompId`).

**Evidence:**
- `AdminUnitAssignAction.java` line 25: `String id = getRequestParam(request, "id", "");`
- `AdminUnitAssignAction.java` line 52: `UnitDAO.deleteAssignment(id);` — no tenancy guard.
- `UnitDAO.java` line 78: `DELETE FROM unit_company WHERE id = ?` — single-column predicate, no `company_id` filter.
- Session company identity is captured at line 23 (`sessCompId`) but is never used in the delete path.

**Recommendation:**
Modify `UnitDAO.deleteAssignment` (or add an overloaded method) to accept the session `companyId` and include it as an additional predicate:
`DELETE FROM unit_company WHERE id = ? AND company_id = ?`
This ensures the delete is a no-op if the record does not belong to the requesting tenant. Verify the affected row count and return an error if it is 0.

---

### FINDING-03

**Severity:** HIGH
**Category:** IDOR — Unvalidated `company_id` in Form Allows Cross-Tenant Assignment Injection
**File:** `src/main/java/com/action/AdminUnitAssignAction.java` line 55 /
         `src/main/java/com/actionform/AdminUnitAssignForm.java` line 14
**Description:**
When `action=add` is submitted, the `company_id` used in the `INSERT` statement is taken directly from the user-controlled form field `form.getCompany_id()` rather than from the server-authoritative session attribute `sessCompId`. An attacker can submit any `company_id` value in the POST body, causing a unit assignment to be created under an arbitrary company — including companies that the authenticated user does not administer. This is a tenant-boundary bypass.

**Evidence:**
- `AdminUnitAssignForm.java` line 14: `private String company_id;` — user-supplied.
- `AdminUnitAssignAction.java` line 55: `UnitDAO.addAssignment(form.getCompany_id(), form.getUnit_id(), ...)` — form value used directly.
- `AdminUnitAssignAction.java` line 23: `String sessCompId = (String) session.getAttribute("sessCompId");` — authoritative value present but unused in the add path.

**Recommendation:**
Replace `form.getCompany_id()` with the session value `sessCompId` in the `addAssignment` call. The `company_id` field should be removed from the form bean entirely, or at minimum ignored and overwritten with the session value before any persistence operation.

---

### FINDING-04

**Severity:** MEDIUM
**Category:** Input Validation — Missing Numeric Format and Range Validation on ID Fields
**File:** `src/main/java/com/actionform/AdminUnitAssignForm.java` lines 12–14 /
         `src/main/java/com/dao/UnitDAO.java` lines 56, 57, 83, 110
**Description:**
The fields `id`, `unit_id`, and `company_id` are all declared as `String` and are parsed with `Integer.parseInt()` deep in the DAO layer without any prior format validation. If a non-numeric, empty, or excessively long value is submitted, `parseInt` throws a `NumberFormatException`. Unless the action or a surrounding exception handler maps this to a safe error page, this produces an unhandled 500 response that may leak stack-trace information. Additionally, there is no upper-bound check, so very large integers (exceeding `Integer.MAX_VALUE`) will also cause an exception.

**Evidence:**
- `UnitDAO.java` line 56: `ps.setInt(1, Integer.parseInt(unitId));` — no guard.
- `UnitDAO.java` line 57: `ps.setInt(2, Integer.parseInt(subCompanyId));` — no guard.
- `UnitDAO.java` line 83: `ps.setInt(1, Integer.parseInt(id));` — no guard.
- `UnitDAO.java` line 110: `stmt.setInt(4, Integer.parseInt(unitId));` — no guard.
- No `validate()` override in the form; no `validation.xml` entry for this form (see FINDING-01).

**Recommendation:**
Add `integer` and `intRange` validators in `validation.xml` for `id`, `unit_id`, and `company_id`. Additionally wrap the DAO `parseInt` calls in a try-catch or add a utility guard method, and configure a global Struts exception handler to render a sanitised error page rather than a raw stack trace.

---

### FINDING-05

**Severity:** MEDIUM
**Category:** Input Validation — Date Fields Accept Arbitrary String Input; No Format Enforcement at Framework Layer
**File:** `src/main/java/com/actionform/AdminUnitAssignForm.java` lines 15–16 /
         `src/main/java/com/action/AdminUnitAssignAction.java` lines 32–41
**Description:**
The `start` and `end` fields are plain `String` with no validation constraint. The action performs partial validation in the `validate` AJAX path (checking nulls and ordering), but the `/adminunitassign` `action=add` path calls `UnitDAO.addAssignment` directly with the raw string values, relying on `DateUtil.stringToSQLDate` to parse them. If `DateUtil` accepts unexpected formats or throws on malformed input, the error propagates as an unhandled exception. The AJAX overlap check (`/assigndatesvalid`) is a client-side convenience call; it is not mandatory before the `add` action executes. An attacker can skip the overlap-check entirely and submit an `add` action with malformed or boundary-case dates.

**Evidence:**
- `AdminUnitAssignForm.java` lines 15–16: `start` and `end` typed as `String`.
- `AdminUnitAssignAction.java` lines 32–41: date validation only occurs in the `validate` switch case, which maps to the `/assigndatesvalid` endpoint (`validate="false"`), not the `/adminunitassign` endpoint.
- `/adminunitassign` action (`action=add`) at line 55 calls `addAssignment` without re-running the date-order and overlap checks performed in the AJAX path.

**Recommendation:**
Move the date parsing, ordering, and overlap validation from the `validate` case into a shared private method, and call it from both the `validate` case and the `add` case. Add `date` and `dateRange` (or a custom `mask`) validator in `validation.xml` to enforce the expected date pattern at the framework layer before the action executes.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Data Integrity — Overlap Check is Not Enforced on the Add Path
**File:** `src/main/java/com/action/AdminUnitAssignAction.java` lines 44–47, 54–56
**Description:**
The assignment-overlap check (`UnitDAO.isAssignmentOverlapping`) is only called from the `validate` action case, which is an optional AJAX pre-flight. The `add` case at line 55 inserts the record directly without repeating the overlap check. A client that bypasses the AJAX call (or a race condition between two near-simultaneous submissions) can create overlapping assignments, corrupting the data model.

**Evidence:**
- `AdminUnitAssignAction.java` line 44: overlap check inside `case "validate":`.
- `AdminUnitAssignAction.java` line 54–56: `case "add":` calls `UnitDAO.addAssignment` with no overlap check.

**Recommendation:**
Execute the overlap check unconditionally inside `case "add":` before calling `addAssignment`. Return an error response if overlap is detected. Consider wrapping the check-and-insert in a database transaction with a serializable or repeatable-read isolation level to eliminate the race condition.

---

### FINDING-07

**Severity:** MEDIUM
**Category:** Input Validation — No Upper-Bound Length Constraint on Any String Field
**File:** `src/main/java/com/actionform/AdminUnitAssignForm.java` lines 12–16
**Description:**
None of the five `String` fields have a declared maximum length. Struts will bind any parameter value of any length to the form bean. Extremely long values can cause excessive memory allocation, slow `parseInt` exceptions with misleading error messages, or — if any future rendering or logging of these values is added — potential log-injection or UI rendering issues.

**Evidence:**
- All five fields (`id`, `unit_id`, `company_id`, `start`, `end`) are declared as unbounded `String`.
- No `maxlength` validator exists in `validation.xml` for this form.

**Recommendation:**
Add `maxlength` validators in `validation.xml`. Suggested limits: `id`, `unit_id`, `company_id` — 10 characters (covers `Integer.MAX_VALUE`); `start`, `end` — constrained to the expected date format length (e.g., 10 characters for `dd/MM/yyyy`).

---

### FINDING-08

**Severity:** LOW
**Category:** Type Safety — All Fields Typed as String; Integer Semantics Only Enforced at DAO
**File:** `src/main/java/com/actionform/AdminUnitAssignForm.java` lines 12–14
**Description:**
`id`, `unit_id`, and `company_id` represent database integer foreign keys but are typed as `String`. Type safety is deferred entirely to the DAO layer (`Integer.parseInt`). This pattern spreads type-parsing concerns across the codebase, increases the surface for `NumberFormatException`, and makes the API contract of the form bean less obvious to maintainers.

**Evidence:**
- Form fields declared `String` at lines 12–14.
- DAO parses with `Integer.parseInt` at lines 56, 57, 83, 110 of `UnitDAO.java`.

**Recommendation:**
Consider typing `id`, `unit_id`, and `company_id` as `Integer` (or `Long`) in the form bean and providing a `validate()` override or Struts type-conversion configuration that produces a user-friendly error message on parse failure rather than an unhandled exception.

---

### FINDING-09

**Severity:** LOW
**Category:** Code Quality / Dead Import
**File:** `src/main/java/com/actionform/AdminUnitAssignForm.java` line 7
**Description:**
`import java.util.Date;` is present but `Date` is not referenced anywhere in the class. This is a dead import, likely a remnant of an earlier version of the class. While not a direct security risk, it can mislead reviewers into thinking date handling occurs within the form bean.

**Evidence:**
- Line 7: `import java.util.Date;`
- No field, method, or annotation in the class uses `java.util.Date`.

**Recommendation:**
Remove the unused import.

---

### FINDING-10

**Severity:** INFO
**Category:** CSRF — Structural Gap (Stack-Wide)
**File:** `src/main/webapp/WEB-INF/struts-config.xml` lines 342–351 (both action mappings)
**Description:**
As noted in the audit scope, Apache Struts 1.3.10 has no built-in CSRF token mechanism. Both `/adminunitassign` (add and delete) and `/assigndatesvalid` are state-changing or information-disclosing endpoints with no CSRF protection. A cross-site request forgery attack could trick an authenticated admin into deleting or creating unit assignments. This is a stack-wide structural gap acknowledged in the audit brief and is recorded here for completeness.

**Evidence:**
- Struts 1.3.10 does not include a synchroniser token filter by default.
- No token-checking code is present in `AdminUnitAssignAction.java` or `PandoraAction.java`.
- Both action mappings are reachable by any authenticated browser session via a forged cross-origin form POST.

**Recommendation:**
Implement the Struts 1 synchroniser token pattern (`saveToken` / `isTokenValid`) in `PandoraAction` or a dedicated filter for all state-mutating actions. Alternatively, migrate to a framework with built-in CSRF protection.

---

## Category Summary

| Category | Verdict |
|----------|---------|
| Input Validation | FINDINGS PRESENT — FINDING-01, FINDING-04, FINDING-05, FINDING-07 |
| Type Safety | FINDINGS PRESENT — FINDING-08 |
| IDOR Risk | FINDINGS PRESENT — FINDING-02, FINDING-03 |
| Sensitive Fields | NO ISSUES — no passwords, tokens, PII, or secrets present in this form |
| Data Integrity | FINDINGS PRESENT — FINDING-06 |
| CSRF | FINDING-10 (stack-wide structural gap, INFO) |

---

## Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 0 | — |
| HIGH | 3 | FINDING-01, FINDING-02, FINDING-03 |
| MEDIUM | 4 | FINDING-04, FINDING-05, FINDING-06, FINDING-07 |
| LOW | 2 | FINDING-08, FINDING-09 |
| INFO | 1 | FINDING-10 |
| **TOTAL** | **10** | |

---

## Sensitive Fields Assessment

AdminUnitAssignForm contains no password fields, authentication tokens, API keys, PII (personally identifiable information), or other sensitive data categories. All fields are operational assignment identifiers and date strings. **NO ISSUES in this category.**
