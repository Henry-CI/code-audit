# Security Audit: AdminUnitChecklistForm.java

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**Auditor:** CIG Security Audit (Pass 1)
**Date:** 2026-02-26
**File Audited:** `src/main/java/com/actionform/AdminUnitChecklistForm.java`
**Stack:** Apache Struts 1.3.10

---

## 1. Reading Evidence

### 1.1 Package and Class

```
Package:  com.actionform
Class:    AdminUnitChecklistForm
Extends:  org.apache.struts.action.ActionForm
```

`serialVersionUID = -2208616500078494492L`

No `validate()` override is present. No `reset()` override is present. The class relies entirely on Struts default behaviour for both operations.

### 1.2 Fields

| # | Name        | Type    | Getter              | Setter              |
|---|-------------|---------|---------------------|---------------------|
| 1 | `id`        | `int`   | `getId()`           | `setId(int)`        |
| 2 | `unitId`    | `int`   | `getUnitId()`       | `setUnitId(int)`    |
| 3 | `action`    | `String`| `getAction()`       | `setAction(String)` |
| 4 | `driverBased` | `boolean` | `isDriverBased()` | `setDriverBased(boolean)` |

Lines of interest:
- `id` — line 13
- `unitId` — line 14
- `action` — line 15
- `driverBased` — line 17
- `setId` — line 27
- `setUnitId` — line 30
- `setAction` — line 43

### 1.3 validate() Details

No `validate()` method is defined. The class does not override `ActionForm.validate()`. Struts 1 will call the base no-op implementation, meaning **no programmatic server-side validation of any field occurs**.

### 1.4 reset() Details

No `reset()` method is defined. The class does not override `ActionForm.reset()`. Struts 1 calls the base no-op implementation. For `boolean` fields, Struts re-uses the prior value if the checkbox is absent from the request, which is the classic Struts checkbox-retention bug. The `driverBased` field is subject to this behaviour.

### 1.5 validation.xml Rules for This Form

`src/main/webapp/WEB-INF/validation.xml` defines exactly three `<form>` entries:

1. `loginActionForm`
2. `adminRegisterActionForm`
3. `AdminDriverEditForm`

**`adminUnitChecklistForm` is entirely absent from validation.xml.**

### 1.6 struts-config.xml Registration

`src/main/webapp/WEB-INF/struts-config.xml` lists 34 `<form-bean>` entries. **`adminUnitChecklistForm` / `AdminUnitChecklistForm` is not declared as a form-bean in struts-config.xml.** No `<action>` mapping references this form class.

### 1.7 Client-Side Reference

`src/main/webapp/skin/js/scripts.js` lines 337 and 339 reference `document.adminUnitChecklistForm.driverBased.value`, indicating the form is rendered under the name `adminUnitChecklistForm` in at least one JSP page. This confirms the form is actively used in the UI despite the absence of a struts-config registration.

---

## 2. Findings

---

### FINDING-01

**Severity:** HIGH
**Category:** Input Validation
**File:** `src/main/java/com/actionform/AdminUnitChecklistForm.java` — entire class
**Title:** No server-side validation whatsoever — no `validate()` override and no validation.xml entry

**Description:**
The form defines no `validate()` method and has no corresponding entry in `validation.xml`. All four fields (`id`, `unitId`, `action`, `driverBased`) arrive at the Action class entirely unchecked. There is no required-field check, no range check on the integer IDs, and no allowlist check on the `action` string.

**Evidence:**
- Lines 1–49: No `validate()` method in the source file.
- `validation.xml`: Form name `adminUnitChecklistForm` is absent; only `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm` have entries.
- `struts-config.xml`: The form bean is not registered, meaning the Struts validator plug-in cannot attach rules to it even if rules existed.

**Recommendation:**
Add a `validate()` override that asserts `id > 0`, `unitId > 0`, and that `action` is non-null and restricted to a whitelist of known values (e.g., `"save"`, `"delete"`). Alternatively, register the form in `struts-config.xml` and add a `<form>` block to `validation.xml` with `required` and `intRange` rules for the two integer fields and an `mask` rule for `action`.

---

### FINDING-02

**Severity:** HIGH
**Category:** IDOR Risk
**File:** `src/main/java/com/actionform/AdminUnitChecklistForm.java` — lines 13–14 (`id`, `unitId`)
**Title:** Unvalidated integer IDs enable direct object reference manipulation

**Description:**
Both `id` and `unitId` are plain `int` fields with no bounds checking, no ownership verification in the form layer, and no validation.xml rules. An authenticated user who can submit a POST request can supply arbitrary values for either field and potentially reference checklist records or unit records belonging to other companies/tenants.

**Evidence:**
- Line 13: `private int id;` — no minimum/maximum constraint.
- Line 14: `private int unitId;` — no minimum/maximum constraint.
- No `validate()` override; no validation.xml entry.
- The form is not registered in struts-config.xml, so even declarative `validate="true"` on an action mapping cannot trigger commons-validator rules.
- `scripts.js` lines 337–339 confirm the form is submitted from client-side UI, meaning `id` and `unitId` values are user-controllable.

**Recommendation:**
The Action class consuming this form must verify that the resolved `id` and `unitId` records belong to the session's company/tenant before performing any read, write, or delete operation. At the form layer, add `intRange` validation (minimum 1) to reject obviously invalid IDs before they reach the database layer.

---

### FINDING-03

**Severity:** HIGH
**Category:** Input Validation / Command Injection Surface
**File:** `src/main/java/com/actionform/AdminUnitChecklistForm.java` — lines 15, 43 (`action` field)
**Title:** Unvalidated free-text `action` field used as a command discriminator

**Description:**
The `action` field is a `String` with no length limit, no null check, no allowlist, and no validation.xml rule. In Struts 1 action classes it is common pattern to branch on this field (e.g., `if ("delete".equals(form.getAction())`). Without server-side enforcement of a finite set of permitted values, an attacker can supply unexpected strings to probe unintended code paths or to cause null-pointer exceptions if the Action does not handle unknown values defensively.

**Evidence:**
- Line 15: `private String action;`
- Line 43: `public void setAction(String action) { this.action = action; }` — no sanitisation.
- No `validate()` method; no validation.xml entry.

**Recommendation:**
Define an explicit allowlist of valid action strings. In `validate()`, reject any `action` value not in the allowlist. Maximum length should be enforced (e.g., 32 characters). Do not pass the raw `action` string to any persistence or shell-execution layer without further sanitisation.

---

### FINDING-04

**Severity:** MEDIUM
**Category:** Data Integrity
**File:** `src/main/java/com/actionform/AdminUnitChecklistForm.java` — line 17 (`driverBased`)
**Title:** Missing `reset()` causes stale boolean state across requests

**Description:**
The `boolean driverBased` field is not reset in a `reset()` override. In Struts 1, when a checkbox is unchecked by the user the browser sends no parameter for it. Without `reset()` clearing the field to `false` before binding, the field retains its prior value from the previous request (when the form is scoped to session, or when the form object is reused). This can cause `driverBased` to remain `true` even when the user deselects the option.

`scripts.js` lines 337–339 show client-side JavaScript explicitly setting the hidden/checkbox value, which partially mitigates this for JavaScript-enabled browsers, but does not address direct API calls or browsers with JavaScript disabled.

**Evidence:**
- Line 17: `private boolean driverBased;` — no `reset()` override in the class.
- `scripts.js` lines 337–339: client-side workaround present, but insufficient as a server-side control.

**Recommendation:**
Override `reset(ActionMapping mapping, HttpServletRequest request)` and set `this.driverBased = false;` (and any other boolean/checkbox fields added in future) at the start of each request cycle.

---

### FINDING-05

**Severity:** MEDIUM
**Category:** Input Validation / Type Safety
**File:** `src/main/java/com/actionform/AdminUnitChecklistForm.java` — lines 13–14 (`id`, `unitId`)
**Title:** Primitive `int` fields silently default to `0` on missing or non-numeric input, masking binding errors

**Description:**
Struts 1 binds request parameters to `int` fields by attempting to parse the string value. If the parameter is absent from the request or cannot be parsed as an integer, Struts silently leaves the field at its default value of `0` (or, depending on the Struts version and error handling, generates a non-fatal `ActionError`). Since there is no `validate()` method and no validation.xml entry, value `0` passes undetected to the Action, which may then execute a `WHERE id = 0` query against the database — potentially returning unexpected rows or triggering unintended logic.

**Evidence:**
- Line 13: `private int id;` — Java default is `0`.
- Line 14: `private int unitId;` — Java default is `0`.
- No `validate()` method to assert `id != 0` and `unitId != 0`.
- No validation.xml `intRange` rule with `min=1`.

**Recommendation:**
Add `intRange` rules in validation.xml with `min` set to `1` for both `id` and `unitId`, or assert `id > 0 && unitId > 0` inside `validate()`. Use `Integer` (boxed) wrapper types if distinguishing "not supplied" from `0` is important.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Structural / Registration Gap
**File:** `src/main/webapp/WEB-INF/struts-config.xml` — entire `<form-beans>` block
**Title:** `AdminUnitChecklistForm` is not registered as a form-bean in struts-config.xml

**Description:**
The class exists and is referenced by client-side JavaScript (`scripts.js`), but `struts-config.xml` contains no `<form-bean>` declaration for it. This means the class is being used outside of the standard Struts form-bean lifecycle, which bypasses the commons-validator plug-in entirely (even if validation.xml rules were added). It also makes the form's scope, action mapping, and validate flag invisible to the framework and to future maintainers.

**Evidence:**
- `struts-config.xml` lines 6–41: 34 form-bean entries; none reference `AdminUnitChecklistForm` or `adminUnitChecklistForm`.
- No `<action>` mapping with `name="adminUnitChecklistForm"`.
- `scripts.js` lines 337–339 confirm active UI use under the name `adminUnitChecklistForm`.

**Recommendation:**
Register the form in `struts-config.xml` with an appropriate scope (`request` is preferred over `session` for mutable write forms). Map it to the correct action path with `validate="true"`. This is a prerequisite for any validation.xml rules to take effect.

---

### FINDING-07

**Severity:** INFO
**Category:** CSRF (Structural Gap — Framework Level)
**File:** `src/main/java/com/actionform/AdminUnitChecklistForm.java` — class level
**Title:** No CSRF token field; inherits framework-wide CSRF gap

**Description:**
As noted in the audit context, Apache Struts 1.3.10 does not provide built-in CSRF protection. `AdminUnitChecklistForm` contains no CSRF token field. Any state-changing operation triggered by this form (checklist assignment, driver-based flag toggling) is vulnerable to cross-site request forgery. This is a framework-wide structural gap applicable to this form in common with all other Struts 1 forms in the application.

**Evidence:**
- Lines 13–17: Only `id`, `unitId`, `action`, `driverBased` fields — no token field.
- Struts 1.3.10 has no synchroniser token mechanism enabled by default.

**Recommendation:**
Implement a per-session or per-request synchroniser token. Options include: (a) add a hidden `token` field to this form and validate it manually in the Action class using `isTokenValid(request)` / `saveToken(request)`; (b) introduce a servlet filter that enforces a CSRF token header (e.g., `X-CSRF-Token`) on all POST requests. This is a cross-cutting concern and should be addressed at the framework level.

---

## 3. Category Summary

| Category          | Verdict                                                                                   |
|-------------------|-------------------------------------------------------------------------------------------|
| Input Validation  | ISSUES FOUND — FINDING-01, FINDING-03, FINDING-05                                        |
| Type Safety       | ISSUES FOUND — FINDING-05 (silent int default), FINDING-04 (boolean stale state)         |
| IDOR Risk         | ISSUES FOUND — FINDING-02                                                                 |
| Sensitive Fields  | NO ISSUES — no passwords, PII, tokens, or secrets are stored in this form                |
| Data Integrity    | ISSUES FOUND — FINDING-04 (missing reset), FINDING-06 (unregistered form bean)           |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs                              |
|----------|-------|------------------------------------------|
| CRITICAL | 0     | —                                        |
| HIGH     | 3     | FINDING-01, FINDING-02, FINDING-03       |
| MEDIUM   | 3     | FINDING-04, FINDING-05, FINDING-06       |
| LOW      | 0     | —                                        |
| INFO     | 1     | FINDING-07                               |
| **Total**| **7** |                                          |
