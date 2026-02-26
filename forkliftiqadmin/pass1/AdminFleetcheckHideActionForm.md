# Audit Report: AdminFleetcheckHideActionForm

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**File Audited:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`
**Auditor:** CIG Security Audit (Pass 1)
**Date:** 2026-02-26

---

## 1. Reading Evidence

### 1.1 Package and Class

- **Package:** `com.actionform`
- **Class:** `AdminFleetcheckHideActionForm`
- **Extends:** `ValidateIdExistsAbstractActionForm` (which itself extends `org.apache.struts.action.ActionForm`)
- **Lombok:** `@Getter` and `@Setter` on class — all fields get public getters/setters generated at compile time.

### 1.2 Fields

| # | Name | Declared Type | Default Value | Source |
|---|------|--------------|---------------|--------|
| 1 | `id` (inherited) | `String` | `null` | `ValidateIdExistsAbstractActionForm`, line 16 |
| 2 | `type_id` | `String` | `null` | Line 15 |
| 3 | `fuel_type_id` | `String` | `null` | Line 16 |
| 4 | `manu_id` | `String` | `null` | Line 17 |
| 5 | `attachment_id` | `String` | `null` | Line 18 |

All five fields are numeric database foreign-key / primary-key identifiers stored as raw `String` with no type enforcement at the form layer.

### 1.3 validate() Details

**Parent class** (`ValidateIdExistsAbstractActionForm`, line 19-27):
- Creates a fresh `ActionErrors` instance.
- Checks `id` with `StringUtils.isEmpty()` — adds `error.id` message key if empty.
- Does NOT validate format or numeric content of `id`.

**This class** (`AdminFleetcheckHideActionForm`, lines 21-38):
- Calls `super.validate(mapping, request)` to obtain the errors collection (inheriting the `id` empty-check).
- Checks `manu_id` empty → adds `error.manufacturer`.
- Checks `type_id` empty → adds `error.type`.
- Checks `fuel_type_id` empty → adds `error.power`.
- Returns the combined errors.
- `attachment_id` has **no validate() check** whatsoever.
- No numeric format validation on any field.
- No length/range validation on any field.
- No whitelist/pattern validation on any field.

### 1.4 reset() Details

`reset()` is **not overridden** in this class or in `ValidateIdExistsAbstractActionForm`. The Struts `ActionForm` base class `reset()` is a no-op. As a result, all five fields retain their Lombok-default values (`null`) between requests only by JVM object lifecycle — they are not explicitly cleared, which in a shared or reused form-bean scenario could permit field value leakage between requests.

### 1.5 validation.xml Rules

`AdminFleetcheckHideActionForm` (registered as `adminFleetcheckHideActionForm` in `struts-config.xml`) has **zero entries** in `src/main/webapp/WEB-INF/validation.xml`. The file defines rules only for:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

No declarative Commons Validator rules exist for any field of this form.

---

## 2. Action Context

The form is bound to path `/fleetcheckhide` in `struts-config.xml` (line 412-419), `validate="true"`, scope `request`, handled by `AdminFleetcheckHideAction`.

`AdminFleetcheckHideAction.execute()` (`src/main/java/com/action/AdminFleetcheckHideAction.java`):
1. Reads `sessCompId` from the HTTP session (company-scoping tenant value).
2. Unpacks all five form fields.
3. Calls `QuestionDAO.hideQuestionById(id, manu_id, type_id, fuel_type_id, att_id, sessCompId)`.

`QuestionDAO.hideQuestionById()` (`src/main/java/com/dao/QuestionDAO.java`, line 197-208):
1. Calls `getQuestionById(id)` — raw string concatenation SQL: `"select ... from question where id = " + id` (line 275) — **SQL injection**.
2. Branches on `comp_id` to decide whether to copy or deactivate the question.
3. Notably: the `sessCompId` is passed through to `copyQuestionToCompId` but **is not used to verify ownership of the record identified by `id`** before the branch decision is made.

---

## 3. Findings

---

### FINDING-01 — CRITICAL: SQL Injection via `id` field (inherited)

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/QuestionDAO.java`, line 275
**Form file:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`, line 14 (inherits `id` from `ValidateIdExistsAbstractActionForm`, line 16)

**Description:**
The `id` field accepted by this form is passed directly into a raw string-concatenated SQL statement with no parameterisation. `getQuestionById(String id)` builds:
```java
String sql = "select id,content,... from question where id = " + id;
stmt.executeQuery(sql);
```
Because `validate()` only checks that `id` is non-empty — not that it is numeric — an attacker can submit any SQL fragment as the `id` parameter value, achieving full SQL injection against the underlying database.

**Evidence:**
- `validate()` check at form line 23 (super): `StringUtils.isEmpty(this.id)` only — no numeric check.
- `QuestionDAO.java` line 275: `"select ... from question where id = " + id` — unparameterised.
- No validation.xml rule exists for this form.

**Recommendation:**
- In `validate()` (or in the abstract parent) add a strict integer-format check on `id`, e.g., `id.matches("^[0-9]+$")` — reject with an error if it fails.
- In `QuestionDAO.getQuestionById()`, replace the `Statement`/string concatenation with a `PreparedStatement` with a parameterised `?` placeholder and `ps.setInt()`.
- Apply the same fix to all other raw-concatenation queries in `QuestionDAO` (`delQuestionById`, `getQuestionContentById`, etc.).

---

### FINDING-02 — CRITICAL: SQL Injection via `type_id`, `fuel_type_id`, `manu_id`, `attachment_id` fields

**Severity:** CRITICAL
**File:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`, lines 15-18
**DAO file:** `src/main/java/com/dao/QuestionDAO.java`, lines 231-242

**Description:**
`type_id`, `fuel_type_id`, `manu_id`, and `attachment_id` are passed to `copyQuestionToCompId()`, which uses `PreparedStatement` — this specific path is parameterised and therefore safe from SQL injection **within that method**. However, the form-layer `validate()` only enforces non-empty for `manu_id`, `type_id`, and `fuel_type_id`; `attachment_id` has no validation at all. Non-numeric values submitted for any of these fields will cause `Integer.parseInt()` to throw a runtime `NumberFormatException` (line 231-241 in QuestionDAO), which propagates as an unhandled exception, producing a 500 error. This is a secondary data-type enforcement gap and application reliability issue, but non-numeric input to `attachment_id` can also trigger the same uncaught exception path silently since validation does not cover it.

**Evidence:**
- `validate()` does not check numeric format for `type_id` (line 29-32), `fuel_type_id` (line 33-36), `manu_id` (line 25-28), or `attachment_id` (no check at all).
- `QuestionDAO.java` lines 231-241: `Integer.parseInt(typeId)`, `Integer.parseInt(manuId)`, `Integer.parseInt(fuleTypeId)`, `Integer.parseInt(attchId)` — all unchecked.

**Recommendation:**
Add numeric format validation in `validate()` for all four fields. For `attachment_id`, add a presence-or-numeric check (it is nullable, so if non-empty it must be numeric). Use a shared utility method to avoid repetition.

---

### FINDING-03 — HIGH: IDOR — No Ownership Verification on `id` Before Record Mutation

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckHideAction.java`, line 33
**DAO file:** `src/main/java/com/dao/QuestionDAO.java`, lines 197-208

**Description:**
The action retrieves `sessCompId` from the session (tenant identifier) and passes it to `hideQuestionById`, but `hideQuestionById` **does not verify that the question identified by the user-supplied `id` belongs to `sessCompId`** before deciding whether to copy or deactivate it. The branch logic checks `question.getComp_id() == null` (global question) or non-null (company-owned), but never asserts that a company-owned record's `comp_id` matches `sessCompId`. An authenticated admin of company A can supply the `id` of a question owned by company B and trigger the `active = 'f'` deactivation branch against that foreign record, or force an unwanted copy into their own company.

**Evidence:**
- `QuestionDAO.hideQuestionById()` lines 201-207: branch on `comp_id == null` vs non-null; `sessCompId` is only used as a destination in the copy path (line 202), never as an ownership guard.
- `id` field validated only for emptiness, not matched against the session company.

**Recommendation:**
After fetching the question by `id`, assert `sessCompId.equals(question.getComp_id())` (for company-owned records) before allowing the deactivation branch. For global records, the copy-to-company path is reasonable but should still validate that `sessCompId` is non-null and legitimate before proceeding.

---

### FINDING-04 — HIGH: Missing Input Validation for `attachment_id` — No Empty or Format Check

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`, lines 18, 21-38

**Description:**
`attachment_id` is the only form field that has zero validation in `validate()`. While the DAO handles a null/empty `attachment_id` by calling `ps.setNull(4, Types.INTEGER)`, the form makes no contract that `attachment_id` will be either empty/null or a valid integer. A non-numeric non-empty value (e.g. `"abc"`) passes `validate()` successfully and then causes `Integer.parseInt(attchId)` in `copyQuestionToCompId()` to throw `NumberFormatException`, yielding an unhandled 500 response that leaks stack trace information.

**Evidence:**
- `validate()` lines 21-38: no block that references `attachment_id`.
- `QuestionDAO.java` line 235: `ps.setInt(4, Integer.parseInt(attchId))` called only after `StringUtils.isNotEmpty(attchId)` — any non-empty non-integer value will throw.

**Recommendation:**
Add a check in `validate()`: if `attachment_id` is non-empty, verify it matches `^[0-9]+$` and add an error if not.

---

### FINDING-05 — HIGH: No CSRF Protection (Structural Gap)

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 411-419
**Form file:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`

**Description:**
As documented for this stack, Apache Struts 1.3.10 provides no built-in CSRF token mechanism. The `/fleetcheckhide` action accepts the form submission with `validate="true"` but there is no synchroniser token check (no `saveToken`/`isTokenValid` calls in the action), no `SameSite` cookie configuration observed, and no custom CSRF filter mapped to this path. A crafted cross-site request from any origin can trigger the hide/deactivate operation on behalf of an authenticated admin, including the IDOR vector described in FINDING-03.

**Evidence:**
- `AdminFleetcheckHideAction.java`: no call to `isTokenValid()` or any token handling.
- struts-config.xml action definition contains no custom roles, filters, or token attributes.
- No CSRF filter class found mapped to `/fleetcheckhide`.

**Recommendation:**
Implement Struts synchroniser token pattern: call `saveToken(request)` when rendering the form and `isTokenValid(request, true)` at the start of `execute()`. Alternatively, introduce a servlet filter that enforces a per-session CSRF token for all state-mutating POST actions.

---

### FINDING-06 — MEDIUM: No reset() Override — Potential Field Residue

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java` (entire class)
**Parent:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`

**Description:**
Neither this class nor its abstract parent overrides `reset()`. In Struts 1, `ActionForm` instances may be reused across requests when the form bean is session-scoped (this form is request-scoped per struts-config, which mitigates the risk), but the absence of `reset()` is a defensive coding gap. If the scope were ever changed to session or if the form is inadvertently reused in a server-side forward chain, field values from a prior request (`type_id`, `fuel_type_id`, `manu_id`, `attachment_id`, `id`) could persist and be acted upon silently.

**Evidence:**
- No `reset()` method in `AdminFleetcheckHideActionForm.java` (lines 1-39).
- No `reset()` method in `ValidateIdExistsAbstractActionForm.java` (lines 1-28).
- struts-config.xml: `scope="request"` currently set — partially mitigates.

**Recommendation:**
Override `reset()` in this class (or in the abstract parent) to explicitly null all fields. This is standard Struts 1 defensive practice regardless of current scope.

---

### FINDING-07 — MEDIUM: No validation.xml Coverage

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
`adminFleetcheckHideActionForm` has no entry in `validation.xml`. The application relies entirely on the programmatic `validate()` method. While programmatic validation is acceptable in Struts 1, the absence of declarative rules means there is no consistent, reviewable, framework-enforced validation layer. The programmatic validate() misses format validation entirely (see FINDING-01, FINDING-02, FINDING-04), and there is no safety net from the declarative layer.

**Evidence:**
- `validation.xml` lines 18-70: only three forms declared — `loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm`. `adminFleetcheckHideActionForm` is absent.

**Recommendation:**
Add declarative validation rules for all five fields to `validation.xml` using Commons Validator's `integer` rule for ID fields. This provides a second validation layer and makes validation intent auditable without reading Java source.

---

### FINDING-08 — LOW: Inconsistent Error Key Naming (`attachment_id` Omission Reflects Incomplete Design)

**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`, lines 25-36

**Description:**
The `validate()` method validates `manu_id`, `type_id`, and `fuel_type_id` as required, but omits `attachment_id` entirely. The field naming convention uses `_id` suffix for all four fields, suggesting they are parallel in nature. The inconsistency signals incomplete implementation — whether `attachment_id` is intentionally optional is not documented in code or comments. This ambiguity makes future maintenance error-prone.

**Evidence:**
- Lines 25-36: three required-field checks.
- Line 18: `attachment_id` field declared but not validated.
- No comment explaining why `attachment_id` is exempt.

**Recommendation:**
Add a code comment explicitly stating `attachment_id` is optional (nullable FK). If it is truly optional, add a format check (FINDING-04). Remove ambiguity for future maintainers.

---

### FINDING-09 — INFO: Lombok @Getter/@Setter Exposes All Fields Publicly

**Severity:** INFO
**File:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`, lines 12-13

**Description:**
The `@Getter` and `@Setter` annotations at class level generate public getter and setter methods for all fields, including the inherited `id`. This is standard Struts 1 form-bean practice, but it means any code in the application can mutate form field values directly without going through any validation logic. There is no encapsulation protection.

**Evidence:**
- Lines 12-13: class-level `@Getter @Setter`.
- Inherited `id` field in parent class also covered.

**Recommendation:**
Informational only. This is a Struts 1 architectural constraint. No immediate action required beyond awareness.

---

## 4. Category Summary

| Category | Status | Findings |
|---|---|---|
| Input Validation | ISSUES FOUND | FINDING-01 (CRITICAL), FINDING-02 (CRITICAL), FINDING-04 (HIGH), FINDING-07 (MEDIUM), FINDING-08 (LOW) |
| Type Safety | ISSUES FOUND | FINDING-02 (CRITICAL) — all ID fields are `String`; integer parsing is deferred to DAO with no form-layer type check |
| IDOR Risk | ISSUES FOUND | FINDING-03 (HIGH) — `id` can reference any question regardless of tenant ownership |
| Sensitive Fields | NO ISSUES | No credentials, PII, tokens, or secrets are fields of this form |
| Data Integrity | ISSUES FOUND | FINDING-01 (CRITICAL, SQL injection), FINDING-03 (HIGH, cross-tenant mutation), FINDING-05 (HIGH, CSRF), FINDING-06 (MEDIUM, no reset()) |

---

## 5. Finding Count by Severity

| Severity | Count | Finding IDs |
|---|---|---|
| CRITICAL | 2 | FINDING-01, FINDING-02 |
| HIGH | 3 | FINDING-03, FINDING-04, FINDING-05 |
| MEDIUM | 2 | FINDING-06, FINDING-07 |
| LOW | 1 | FINDING-08 |
| INFO | 1 | FINDING-09 |
| **TOTAL** | **9** | |
