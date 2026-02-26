# Security Audit Report: AdminUnitImpactForm.java

**Audit Run:** audit/2026-02-26-01/
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** Automated Security Audit (claude-sonnet-4-6)
**Stack:** Apache Struts 1.3.10

---

## Files Examined

| File | Purpose |
|------|---------|
| `src/main/java/com/actionform/AdminUnitImpactForm.java` | ActionForm under audit |
| `src/main/java/com/action/AdminUnitImpactAction.java` | Consuming action class |
| `src/main/webapp/WEB-INF/validation.xml` | Declarative validation rules |

---

## Reading Evidence

### Package and Class

```
Package : com.actionform
Class   : AdminUnitImpactForm
Extends : org.apache.struts.action.ActionForm
```

### Fields

| Line | Name | Type | Getter | Setter |
|------|------|------|--------|--------|
| 13 | `id` | `int` | yes (L26) | yes (L47) |
| 14 | `unitId` | `int` | yes (L29) | yes (L50) |
| 15 | `servLast` | `int` | yes (L32) | yes (L53) |
| 16 | `servNext` | `int` | yes (L35) | yes (L56) |
| 17 | `servDuration` | `int` | yes (L38) | yes (L59) |
| 18 | `accHours` | `double` | yes (L80) | yes (L83) |
| 20 | `hourmeter` | `double` | yes (L74) | yes (L77) |
| 22 | `action` | `String` | yes (L41) | yes (L62) |
| 23 | `servType` | `String` | yes (L44) | yes (L65) |
| 24 | `servStatus` | `String` | yes (L68) | yes (L71) |

### validate() Method

Not present. The class defines no `validate()` override. Struts will invoke the default no-op `ActionForm.validate()`, which returns an empty `ActionErrors` collection — effectively performing no server-side validation for any field.

### reset() Method

Not present. The class defines no `reset()` override. Struts will invoke the default no-op `ActionForm.reset()`. Primitive fields (`int`, `double`) will retain their Java defaults (0 / 0.0) on first population but will NOT be cleared between requests in the same session if the form bean is session-scoped. String fields will retain whatever value Struts bound from the prior request in that scenario.

### validation.xml Coverage

The `validation.xml` `<formset>` contains three `<form>` entries:

1. `loginActionForm`
2. `adminRegisterActionForm`
3. `AdminDriverEditForm`

`AdminUnitImpactForm` is **not listed**. No declarative field-level validation rules exist for this form.

---

## Findings

---

### FINDING-01

**Severity:** HIGH
**Category:** Input Validation — No Server-Side Validation
**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java`
**Lines:** 5, 86 (entire class)
**Supporting file:** `src/main/webapp/WEB-INF/validation.xml` (absence of entry)

**Description:**
The form class neither overrides `validate()` nor has a corresponding entry in `validation.xml`. Every field accepted by this form — including numeric identifiers, service scheduling integers, floating-point hourmeter values, and free-text strings — arrives at the action layer with zero server-side validation. Struts 1 will bind raw HTTP parameter strings directly to typed fields via its `BeanUtils`-based population mechanism. If the bound value cannot be converted, Struts may silently default the field to 0 (for primitives) or leave String fields as-is.

**Evidence:**
- No `validate()` method in the class (lines 1–86 searched).
- `validation.xml` lists only `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`; `AdminUnitImpactForm` is absent.

**Recommendation:**
Add a `<form name="AdminUnitImpactForm">` block in `validation.xml` with at minimum: `required` and `integer` validators for `id`, `unitId`, `servLast`, `servNext`, `servDuration`; `required` and appropriate range/pattern validators for `hourmeter` and `accHours`; and `mask` or whitelist validators for `action`, `servType`, and `servStatus`. Alternatively implement `validate()` directly in the form class and return populated `ActionErrors`.

---

### FINDING-02

**Severity:** HIGH
**Category:** IDOR — Unvalidated Unit and Record Identifiers
**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java` lines 13–14
**Supporting file:** `src/main/java/com/action/AdminUnitImpactAction.java` lines 21–31

**Description:**
Both `id` (line 13) and `unitId` (line 14) are `int` fields that are bound directly from HTTP request parameters with no validation, range check, or authorization check. In `AdminUnitImpactAction`, the separate raw parameter `equipId` (line 22) is also bound without bounds checking and passed directly to `UnitDAO.getInstance().resetCalibration(equip)` (line 32) after a bare `Integer.parseInt()`. An authenticated user with access to the admin area can supply an arbitrary integer for `equipId` / `unitId` / `id` and manipulate records belonging to any unit in the database, including units belonging to other companies (cross-tenant access).

**Evidence:**
```java
// AdminUnitImpactAction.java L21-32
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
...
if (action.equalsIgnoreCase("reset_calibration")) {
    int equip = Integer.parseInt(equipId);          // no validation, no authz check
    UnitDAO.getInstance().resetCalibration(equip);  // operates on caller-supplied ID
```

**Recommendation:**
Before executing any DAO operation, verify that the requested `id`, `unitId`, and `equipId` belong to the tenant/company associated with the authenticated session. Implement an authorization helper (e.g., `UnitDAO.isUnitOwnedByCompany(unitId, sessionCompanyId)`) and return an error forward if the check fails. Add positive-integer range validation so that non-positive and absurdly large values are rejected before reaching the DAO.

---

### FINDING-03

**Severity:** HIGH
**Category:** Input Validation — Uncontrolled Action Discriminator
**File:** `src/main/java/com/action/AdminUnitImpactAction.java` lines 21, 26–28
**Related field:** `AdminUnitImpactForm.java` line 22 (`action`)

**Description:**
The `action` discriminator is read first from the raw HTTP parameter (`request.getParameter("action")`) and, if absent, falls back to `impactForm.getAction()`. There is no whitelist or enumeration check. Any string value can be submitted. Currently only `"reset_calibration"` is handled, but the pattern allows future action strings to be injected freely. Because the field is also on the form bean, it persists in the form state (especially under session scope) and may bleed into subsequent requests.

**Evidence:**
```java
// L21
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
// L26-28
if (action == null || action.equals("")) {
    action = impactForm.getAction();
}
// L30
if (action.equalsIgnoreCase("reset_calibration")) { ... }
```

**Recommendation:**
Validate `action` against an explicit whitelist (e.g., an `enum` or a `Set<String>`) before branching. Return a controlled error forward for unrecognised action values rather than silently falling through to the default `"success"` forward.

---

### FINDING-04

**Severity:** HIGH
**Category:** Input Validation — `Integer.parseInt` Without Exception Handling
**File:** `src/main/java/com/action/AdminUnitImpactAction.java` line 31

**Description:**
`Integer.parseInt(equipId)` is called with no surrounding try/catch and no prior format check. If `equipId` is empty (the default when the parameter is absent), this will throw `NumberFormatException`. If `equipId` contains non-numeric input, it likewise throws. Because the method signature declares `throws Exception`, the exception will propagate to Struts' exception handling chain, potentially exposing a stack trace to the caller and triggering a 500 response rather than a controlled error page.

**Evidence:**
```java
// L22 — equipId defaults to "" when parameter is absent
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
// L31 — bare parseInt with no guard
int equip = Integer.parseInt(equipId);
```

**Recommendation:**
Validate that `equipId` is a non-empty, positive-integer string before calling `parseInt`. Wrap in a try/catch `NumberFormatException` block and return a controlled error forward.

---

### FINDING-05

**Severity:** MEDIUM
**Category:** Data Integrity — No reset() Override; Potential Field Bleed
**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java` line 5

**Description:**
No `reset()` method is defined. If the form bean is configured as session-scoped in `struts-config.xml`, field values from a previous request will persist into a subsequent request where those parameters are not submitted (e.g., a partial form post). This can cause stale `unitId`, `id`, or scheduling values to be silently reused, leading to incorrect data being persisted without the user's intent.

**Evidence:**
`reset()` is absent from lines 1–86. Struts 1's default `ActionForm.reset()` is a no-op.

**Recommendation:**
Implement `reset(ActionMapping mapping, HttpServletRequest request)` to explicitly zero out or null all fields at the start of each request cycle. Alternatively, configure the form bean as request-scoped in `struts-config.xml` (`scope="request"`), which avoids cross-request bleed by construction.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Type Safety — Unvalidated Double Fields
**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java` lines 18, 20

**Description:**
`accHours` and `hourmeter` are `double` fields. Struts' `BeanUtils` type conversion will silently coerce malformed input to `0.0` or throw a conversion error that Struts may absorb, depending on configuration. There are no validation rules ensuring these values are non-negative or within a plausible operational range (e.g., 0–99999 hours for a forklift hourmeter). A negative `hourmeter` value could corrupt service scheduling logic downstream.

**Evidence:**
- `private double accHours;` (L18), `private double hourmeter;` (L20).
- No `validation.xml` entry for this form.
- No `validate()` override.

**Recommendation:**
Add `floatRange` (or equivalent) validators in `validation.xml` enforcing a minimum of 0.0 and a reasonable maximum. Validate that `servNext > servLast` and that `servDuration > 0` at the business logic layer.

---

### FINDING-07

**Severity:** MEDIUM
**Category:** Input Validation — Unvalidated String Fields (Potential Stored XSS / Injection)
**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java` lines 22–24

**Description:**
`action` (L22), `servType` (L23), and `servStatus` (L24) are unbounded `String` fields with no length cap, no character whitelist, and no encoding applied at the form layer. If any of these values are persisted to the database and subsequently rendered in admin views without escaping, stored cross-site scripting is possible. If they are incorporated into queries without parameterisation, SQL injection is a secondary risk (to be confirmed at the DAO layer).

**Evidence:**
Fields declared at lines 22–24; no `maxlength`, no `mask` validator, no validation entry in `validation.xml`.

**Recommendation:**
Apply `maxlength` and `mask` validators in `validation.xml` for `servType` and `servStatus` restricting to expected character sets (e.g., alphanumeric plus limited punctuation). Ensure all rendering of these values in JSPs uses `<bean:write filter="true"/>` or JSTL `<c:out/>` with escaping enabled.

---

### FINDING-08

**Severity:** LOW
**Category:** Data Integrity — No Business-Logic Cross-Field Validation
**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java` lines 15–17

**Description:**
There is no validation ensuring the relationship `servNext >= servLast` or `servDuration > 0`. Submitting `servNext` less than `servLast` (scheduling a past service as the next service) or a zero/negative `servDuration` would silently produce logically invalid records.

**Evidence:**
Fields `servLast` (L15), `servNext` (L16), `servDuration` (L17) are plain `int` with no constraints.

**Recommendation:**
Implement cross-field validation in a `validate()` override: verify `servNext >= servLast` and `servDuration > 0`, adding appropriate `ActionError` entries for violations.

---

### FINDING-09

**Severity:** INFO
**Category:** CSRF — Structural Gap (Stack-Wide)
**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java` (all mutation operations)

**Description:**
As noted in the audit scope, Apache Struts 1.3.10 provides no built-in CSRF protection. This form handles a `reset_calibration` operation that modifies equipment state. Without a synchroniser token, an attacker can craft a cross-origin request that triggers calibration resets on behalf of an authenticated admin. This is a stack-wide structural gap, noted here for completeness.

**Evidence:**
No CSRF token field present in the form. Struts 1 `ActionForm` has no token mechanism. `AdminUnitImpactAction` does not call `isTokenValid()`.

**Recommendation:**
Implement Struts 1 synchroniser token pattern: call `saveToken(request)` in the GET handler and `isTokenValid(request, true)` at the start of the POST handler. Reject requests that fail token validation with an appropriate error forward.

---

## Category Summary

| Category | Finding IDs | Status |
|----------|-------------|--------|
| Input Validation | 01, 03, 04, 07 | Issues found |
| Type Safety | 06 | Issues found |
| IDOR Risk | 02 | Issues found |
| Sensitive Fields | — | NO ISSUES — no passwords, PII, or credentials are stored in this form |
| Data Integrity | 05, 08 | Issues found |
| CSRF | 09 | Structural gap (stack-wide, INFO) |

---

## Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 0 | — |
| HIGH | 4 | 01, 02, 03, 04 |
| MEDIUM | 3 | 05, 06, 07 |
| LOW | 1 | 08 |
| INFO | 1 | 09 |
| **TOTAL** | **9** | |

---

## Notes

- The `serialVersionUID` field (L11) is standard Java serialization boilerplate and presents no security concern in this context.
- The companion action class `AdminUnitImpactAction.java` was read as supporting evidence. Its issues (FINDING-02, FINDING-03, FINDING-04) are rooted in the absence of form-layer validation and are reported here; the action class itself should be audited as a separate pass item.
- Sensitive Fields category has NO issues: this form contains no passwords, authentication tokens, PII (names, emails, SSNs), or financial data.
