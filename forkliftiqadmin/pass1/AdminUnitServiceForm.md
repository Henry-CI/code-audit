# Security Audit Report: AdminUnitServiceForm.java

**Audit Run:** audit/2026-02-26-01/pass1
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Stack:** Apache Struts 1.3.10
**Branch:** master

---

## Reading Evidence

### Package and Class

- **File:** `src/main/java/com/actionform/AdminUnitServiceForm.java`
- **Package:** `com.actionform`
- **Class:** `AdminUnitServiceForm extends ActionForm`
- **serialVersionUID:** `-2208616500078494492L`

### Fields

| Field         | Type     | Line | Notes                                    |
|---------------|----------|------|------------------------------------------|
| `id`          | `int`    | 13   | Record identifier (unused in Action)     |
| `unitId`      | `int`    | 14   | Foreign key to unit; drives all DB ops   |
| `servLast`    | `int`    | 15   | Last service reading (hours as int)      |
| `servNext`    | `int`    | 16   | Next service threshold (hours as int)    |
| `servDuration`| `int`    | 17   | Service interval duration (hours as int) |
| `accHours`    | `double` | 18   | Accumulated hours                        |
| `hourmeter`   | `double` | 20   | Hourmeter reading                        |
| `action`      | `String` | 22   | Dispatch token (`saveservice`)           |
| `servType`    | `String` | 23   | Service type selector (`setIntval`, `setDur`, or other) |
| `servStatus`  | `String` | 24   | Status string (set by Action, also settable from request) |

### validate() Method

No `validate()` override is present. The class relies entirely on the Struts ActionForm default, which performs no validation unless the Commons Validator framework is configured for this form name.

### reset() Method

No `reset()` override is present. Primitive fields (`int`, `double`) will retain their JVM default values (0 / 0.0) on form reset; `String` fields will be `null`.

### validation.xml Coverage

`src/main/webapp/WEB-INF/validation.xml` defines rules for exactly three forms:

1. `loginActionForm`
2. `adminRegisterActionForm`
3. `AdminDriverEditForm`

**`adminUnitServiceForm` is not listed.** The action mapping in `struts-config.xml` (line 495) sets `validate="true"`, but with no matching entry in `validation.xml` the validator finds nothing to enforce, so all fields pass through without server-side validation.

### Action Mapping (struts-config.xml, lines 490-499)

```xml
<action
    path="/adminunitservice"
    name="adminUnitServiceForm"
    scope="request"
    validate="true"
    input="UnitServiceDefinition"
    type="com.action.AdminUnitServiceAction">
    <forward name="success" path="UnitServiceDefinition"/>
    <forward name="failure" path="UnitServiceDefinition"/>
</action>
```

### Downstream Usage (AdminUnitServiceAction.java)

`unitId` is passed directly from the form to `UnitDAO.saveService()` as the sole key for both `INSERT` and `UPDATE` on the `unit_service` table. No session-level ownership check is performed before the write.

---

## Findings

---

### FINDING-01

**Severity:** HIGH
**Category:** Input Validation — Missing Server-Side Validation
**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java` (entire class)
**Corroborating files:** `src/main/webapp/WEB-INF/validation.xml` (no entry for this form); `src/main/webapp/WEB-INF/struts-config.xml` line 495 (`validate="true"`)

**Description:**
`AdminUnitServiceForm` declares no `validate()` override and has no corresponding entry in `validation.xml`. Although `struts-config.xml` sets `validate="true"`, Struts/Commons Validator will find no rules for the form name `adminUnitServiceForm` and silently skip validation. Every field — including numeric ranges, required presence, and string enumeration — reaches the Action class completely unchecked.

**Evidence:**
- No `validate()` method in `AdminUnitServiceForm.java`.
- `validation.xml` contains entries only for `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`. `adminUnitServiceForm` is absent.
- `AdminUnitServiceAction.java` calls `serviceForm.getServType()`, `serviceForm.getServDuration()`, etc. without any null-guard or range check before using their values in arithmetic and passing them to the DAO.

**Recommendation:**
Add a `<form name="adminUnitServiceForm">` block to `validation.xml` with at minimum: `required` + `integer` constraints on `unitId`, `servLast`, `servNext`, `servDuration`; `required` + `double` on `accHours`; `required` + allowable-values mask on `servType`. Additionally, implement a `validate()` override in the form class to enforce cross-field business rules (e.g., `servNext > servLast`).

---

### FINDING-02

**Severity:** HIGH
**Category:** Input Validation — Unvalidated String Enum (`servType`)
**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java` line 23; `src/main/java/com/action/AdminUnitServiceAction.java` lines 36-40
**Corroborating file:** `src/main/java/com/dao/UnitDAO.java` line 727

**Description:**
`servType` is a free-form `String` with no allowable-values constraint at any layer. The Action uses it in a case-insensitive equality check to select a calculation branch, then persists it verbatim into the `service_type` column of `unit_service` via a `PreparedStatement`. An attacker can submit arbitrary string content for `servType`. While SQL injection is not possible through the parameterised statement, business logic can be bypassed (forcing the `else` branch of the `serviceRemain` calculation) and unexpected data can be stored in the database.

**Evidence:**
- `AdminUnitServiceAction.java` lines 36-40: only two values (`setIntval`, `setDur`) are tested; any other string causes the `else` branch to execute silently.
- `UnitDAO.java` line 727: `ps.setString(5, bean.getServType())` — raw form value persisted.
- No validation rule or `validate()` check restricts the set of accepted values.

**Recommendation:**
Whitelist `servType` to the known set of valid values (`setIntval`, `setDur`, and any others defined by the business domain) in `validation.xml` using a `mask` rule, or validate explicitly in `validate()`. Reject submissions with any other value before reaching the Action.

---

### FINDING-03

**Severity:** HIGH
**Category:** IDOR — Unverified `unitId` Ownership
**File:** `src/main/java/com/action/AdminUnitServiceAction.java` lines 52-61
**Corroborating file:** `src/main/java/com/dao/UnitDAO.java` lines 711-744

**Description:**
`unitId` is supplied entirely by the client via the form POST. `AdminUnitServiceAction` passes it directly to `UnitDAO.saveService()`, which uses it as the sole `WHERE` predicate for both `INSERT` and `UPDATE` on the `unit_service` table. There is no check — in the Action, the DAO, or any interceptor — that the authenticated session's company owns the unit identified by the submitted `unitId`. Any authenticated admin can therefore overwrite service records for units belonging to any other company by submitting an arbitrary `unitId`.

**Evidence:**
- `AdminUnitServiceAction.java`: no `request.getSession()` call, no company ownership lookup.
- `UnitDAO.saveService()` lines 711-744: both the existence check (`select count(unit_id) from unit_service where unit_id=?`) and the subsequent `INSERT`/`UPDATE` use only `unitId`; `company_id` is never joined or filtered.
- `AdminUnitServiceForm.java` line 14: `unitId` is a plain `int` set by the Struts framework directly from the HTTP parameter.

**Recommendation:**
Before calling `saveService()`, verify in the Action (or a dedicated ownership-check method in `UnitDAO`) that the submitted `unitId` belongs to the company associated with the current session. This check should be performed server-side; the session company identifier must never come from the request.

---

### FINDING-04

**Severity:** MEDIUM
**Category:** Input Validation — No Range or Sign Constraints on Numeric Fields
**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java` lines 13-18, 20

**Description:**
All numeric fields (`id`, `unitId`, `servLast`, `servNext`, `servDuration`, `accHours`, `hourmeter`) are primitive types that default to `0` on reset and accept any value the HTTP parameter parser can coerce. There are no minimum/maximum bounds enforced at any layer. Negative or zero values for service-interval fields produce meaningless `serviceRemain` calculations and can store logically invalid records (e.g., `servNext` less than `servLast`, or negative `accHours`).

**Evidence:**
- `AdminUnitServiceAction.java` line 37: `serviceRemain = serviceForm.getServDuration() - serviceForm.getAccHours()` — result is unchecked and can be zero or negative, which immediately triggers the "due in less than 5 hours" status string, masking the data problem.
- No `validate()` method and no `validation.xml` entry to enforce `minvalue`/`maxvalue` rules.

**Recommendation:**
Add `intRange` / `doubleRange` validator rules in `validation.xml` for each numeric field. At minimum: `unitId` and `id` must be `>= 1`; `servDuration`, `servLast`, `servNext` must be `>= 0`; `accHours` and `hourmeter` must be `>= 0.0`. Also enforce business-rule constraints (e.g., `servNext >= servLast`) in a `validate()` override.

---

### FINDING-05

**Severity:** MEDIUM
**Category:** Input Validation — `servStatus` Writable from Request
**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java` lines 68-73

**Description:**
`servStatus` has a public setter (`setServStatus`) and is bound as a standard Struts form property, meaning the Struts framework will populate it from any HTTP POST parameter named `servStatus`. In `AdminUnitServiceAction`, `servStatus` is computed server-side and set on the `ServiceBean`, but the form field value is never explicitly cleared or ignored. Although the current DAO code does not persist `servStatus` to the `unit_service` table, the field on the `ServiceBean` that is set to the `request` attribute (`request.setAttribute("serviceBean", serviceBean)`) uses the computed value from the Action, not the form value. The risk is that future maintenance refactors the code to read `serviceForm.getServStatus()` for persistence, inadvertently reintroducing client-controlled status text.

**Evidence:**
- `AdminUnitServiceForm.java` line 72: `setServStatus(String servStatus)` — public, no restriction.
- `AdminUnitServiceAction.java` lines 42-50: `servStatus` is computed solely from `serviceRemain` and assigned to `serviceBean`, not read from `serviceForm`. No defensive null-out of the form field.

**Recommendation:**
Remove the `servStatus` field from the form entirely if it does not need to travel in the request. If it must remain for display purposes, mark it read-only by removing `setServStatus()` or ignoring it explicitly at the start of the Action. Add a comment flagging that this field must never be sourced from client input.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Data Integrity — `id` Field Declared but Never Used
**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java` lines 13, 26-28, 47-49

**Description:**
The form declares an `id` field with getter and setter, but `AdminUnitServiceAction` never reads it and `UnitDAO.saveService()` does not use it. The `unit_service` table is keyed on `unit_id`, not a separate record `id`. The dead field creates confusion about the data model, increases the attack surface (an extra client-controlled integer that could mistakenly be used as a lookup key in future code), and may indicate the form was intended to support record-level updates that were never implemented.

**Evidence:**
- `AdminUnitServiceForm.java` line 13: `private int id;` declared.
- `AdminUnitServiceAction.java`: no reference to `serviceForm.getId()`.
- `UnitDAO.saveService()`: no `id` column in either the `INSERT` or `UPDATE` SQL.

**Recommendation:**
If `id` has no current or planned use, remove it from the form to reduce the attack surface and clarify intent. If it is intended for future use (e.g., record-level upsert), document the intent and ensure the forthcoming implementation includes ownership verification.

---

### FINDING-07

**Severity:** LOW
**Category:** Type Safety — `hourmeter` Field Declared but Never Persisted via This Form
**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java` line 20

**Description:**
`hourmeter` is declared as a `double` field with getter/setter, but `AdminUnitServiceAction` never reads `serviceForm.getHourmeter()` and the `unit_service` table `INSERT`/`UPDATE` in `UnitDAO.saveService()` does not include a `hourmeter` column. The `hourmeter` value that appears in `getServiceByUnitId()` is sourced from the `unit` table join, not from this form. Like `id`, this dead field is a maintenance and confusion risk.

**Evidence:**
- `AdminUnitServiceForm.java` line 20: `private double hourmeter;`.
- `AdminUnitServiceAction.java`: no call to `serviceForm.getHourmeter()`.
- `UnitDAO.saveService()` lines 720-744: no `hourmeter` binding.

**Recommendation:**
Remove `hourmeter` from the form if it serves no inbound data-transfer purpose. If it is present for display/pre-population purposes only (e.g., rendered into a JSP), mark it clearly with a comment and consider whether it should have a setter at all.

---

### FINDING-08

**Severity:** LOW
**Category:** Data Integrity — Missing `reset()` Override Risks Stale State
**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java` (entire class)

**Description:**
No `reset()` method is overridden. For the `String` fields (`action`, `servType`, `servStatus`), Struts will leave them as `null` if no corresponding HTTP parameter is submitted (e.g., in a partial POST). For the numeric primitives, the JVM default of `0` will remain. Without an explicit reset, re-use of a form instance (possible when `scope="session"` is set, though this form uses `scope="request"`) or tests that exercise the form out-of-container can encounter unexpected field state. More relevantly, the absence of a reset means that if a future developer changes the scope to `session`, stale field values from a prior request will silently persist into a new operation.

**Evidence:**
- No `reset()` method in `AdminUnitServiceForm.java`.
- `struts-config.xml` line 493: `scope="request"` (mitigates the immediate risk but does not eliminate it).

**Recommendation:**
Add a `reset()` override that sets all `String` fields to `null` (or empty string) and numeric fields to their safe defaults (`-1` for ID fields to make uninitialized state detectable). This is a defensive measure against scope changes and test harness misuse.

---

## Category Summaries

| Category            | Findings                  | Result         |
|---------------------|---------------------------|----------------|
| Input Validation    | FINDING-01, 02, 04, 05    | Issues found   |
| Type Safety         | FINDING-07                | Issues found   |
| IDOR Risk           | FINDING-03                | Issues found   |
| Sensitive Fields    | (none)                    | NO ISSUES — no passwords, tokens, PII, or cryptographic material are present in this form |
| Data Integrity      | FINDING-06, 08            | Issues found   |

> **Sensitive Fields — NO ISSUES:** `AdminUnitServiceForm` contains only operational service-scheduling data (service intervals, hourmeter readings, type codes). No passwords, authentication tokens, PII, financial data, or cryptographic material are present. This category is clear.

---

## Finding Count by Severity

| Severity | Count | Finding IDs                          |
|----------|-------|--------------------------------------|
| CRITICAL | 0     | —                                    |
| HIGH     | 3     | FINDING-01, FINDING-02, FINDING-03   |
| MEDIUM   | 3     | FINDING-04, FINDING-05, FINDING-06   |
| LOW      | 2     | FINDING-07, FINDING-08               |
| INFO     | 0     | —                                    |
| **Total**| **8** |                                      |
