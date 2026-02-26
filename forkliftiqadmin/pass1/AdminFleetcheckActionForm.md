# Audit Report: AdminFleetcheckActionForm
**Audit run:** audit/2026-02-26-01/
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** Security Audit (automated)
**File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`

---

## 1. Reading Evidence

### Package + Class Name
- **Package:** `com.actionform`
- **Class:** `AdminFleetcheckActionForm extends ActionForm`

### Fields (all declared at class level)

| # | Type | Name | Default |
|---|------|------|---------|
| 1 | `String` | `action` | `null` |
| 2 | `String` | `id` | `null` |
| 3 | `String` | `manu_id` | `null` |
| 4 | `String` | `type_id` | `null` |
| 5 | `String` | `fuel_type_id` | `null` |
| 6 | `String` | `attachment_id` | `null` |
| 7 | `ArrayList` (raw) | `arrAdminUnitType` | `new ArrayList()` |
| 8 | `ArrayList` (raw) | `arrAdminUnitFuelType` | `new ArrayList()` |
| 9 | `ArrayList` (raw) | `arrAttachment` | `new ArrayList()` |

Getters and setters are generated via Lombok `@Getter` / `@Setter` on the class, meaning all nine fields are publicly accessible for both read and write via HTTP parameter binding.

### validate() Method
**Exists: YES** (lines 49–68)

Checks performed:
1. `manu_id` — fails if `StringUtils.isEmpty(manu_id)` (null or blank) → emits `error.manufacturer`
2. `type_id` — fails if `StringUtils.isEmpty(type_id)` (null or blank) → emits `error.type`
3. `fuel_type_id` — fails if `StringUtils.isEmpty(fuel_type_id)` (null or blank) → emits `error.power`

**Not checked by validate():**
- `id` — no presence or format check
- `action` — no whitelist or format check
- `attachment_id` — no check at all
- No numeric/integer format check on any field before downstream `Long.parseLong()` / `Integer.parseInt()` calls in the DAO

### reset() Method
**Exists: NO** — no `reset(ActionMapping, HttpServletRequest)` override is present. Struts 1 does not clear fields between requests when `reset()` is absent; field values can persist across requests under certain scoping conditions.

### validation.xml Rules for This Form
**None found.**

`validation.xml` defines rules for exactly three forms:
```xml
<form name="loginActionForm"> ... </form>
<form name="adminRegisterActionForm"> ... </form>
<form name="AdminDriverEditForm"> ... </form>
```

There is no `<form name="adminFleetcheckActionForm">` entry. The action mapping in `struts-config.xml` has `validate="true"`, meaning only the programmatic `validate()` method runs — no Commons Validator declarative rules apply.

---

## 2. Audit Findings

### Category A: Input Validation

---

#### FINDING-01
- **Severity:** HIGH
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`, line 49–68
- **Description:** `validate()` does not verify numeric format for `manu_id`, `type_id`, `fuel_type_id`, or `attachment_id` before they are consumed by `Long.parseLong()` and `Integer.parseInt()` in the DAO layer. A non-numeric value (e.g., `"abc"`, `"1; DROP TABLE question"`) passes `validate()` successfully because `StringUtils.isEmpty()` only tests for null/blank. The exception thrown by `parseLong` is caught and re-thrown as `SQLException`, producing a server error rather than a user-friendly validation rejection, but more importantly it means the application has no controlled rejection path for malformed numeric input — the only barrier is the unchecked exception propagation.
- **Evidence:**
  - Form `validate()` (lines 54–65): checks `isEmpty()` only, no `StringUtils.isNumeric()` or regex guard.
  - `QuestionDAO.getQuestionByCategory()` (QuestionDAO.java line 155): `Long.parseLong(manuId)` called with unvalidated form value.
  - `QuestionDAO.getMaxQuestionId()` (QuestionDAO.java line 572): `Integer.parseInt(typeId)` with unvalidated value.
  - `QuestionDAO.copyQuestionToCompId()` (QuestionDAO.java lines 231–242): `Integer.parseInt()` called on all four ID strings with no prior validation.
- **Recommendation:** Add numeric format validation in `validate()` for all four ID fields using `StringUtils.isNumeric()` or a regex match (`\d+`) before the form is accepted. Reject the form with an appropriate error message if the value is non-numeric.

---

#### FINDING-02
- **Severity:** MEDIUM
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`, line 20
- **Description:** The `action` field accepts arbitrary string values and is used in `AdminFleetcheckAction` as a branch selector (`action.equalsIgnoreCase("search")`, `action.equalsIgnoreCase("add")`). There is no whitelist validation — any value other than "search" or "add" silently falls through to the `else` branch (lines 65–73 of `AdminFleetcheckAction.java`), which still calls `QuestionDAO.getQuestionByCategory()` with potentially null/empty ID fields, bypassing the `validate()` pre-condition checks because `validate()` only runs when action routing triggers it and does not guard the `else` path's DAO call.
- **Evidence:**
  - `AdminFleetcheckActionForm.java` line 20: `private String action = null;` — no constraint.
  - `AdminFleetcheckAction.java` lines 35–73: three-branch dispatch on `action` string with no normalization or whitelist guard; `else` branch calls the DAO directly.
- **Recommendation:** Validate `action` against an explicit whitelist (e.g., `{"search", "add"}`) in `validate()` and reject the submission if the value is not in the list. Do not rely on the silent `else` fallthrough.

---

#### FINDING-03
- **Severity:** MEDIUM
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java` (form-level)
  Cross-reference: `src/main/webapp/WEB-INF/validation.xml`
- **Description:** No Commons Validator (`validation.xml`) rules exist for `adminFleetcheckActionForm`. The entire validation burden falls on the hand-written `validate()` method, which is incomplete (see FINDING-01 and FINDING-02). There is no declarative layer providing defense-in-depth (e.g., `integer`, `required`, `mask` rules). This is consistent with the known structural gap across this codebase but creates an elevated risk surface for this particular form because all fields bind to DAO numeric parameters.
- **Evidence:** `validation.xml` lines 22–69: no `<form name="adminFleetcheckActionForm">` entry present.
- **Recommendation:** Add a `<form name="adminFleetcheckActionForm">` block to `validation.xml` with at minimum `required` and `integer` validators on `manu_id`, `type_id`, `fuel_type_id`, and `attachment_id`.

---

#### FINDING-04
- **Severity:** LOW
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java` (class level)
- **Description:** No `reset()` method is implemented. In Struts 1, `reset()` is responsible for clearing checkbox and multi-value fields between requests. While this form does not currently contain checkboxes, the absence of `reset()` means that if the form scope were to change (e.g., `session` scope) or fields were added in future, stale values from prior requests could silently persist. Currently the action is mapped as `scope="request"` which reduces immediate risk, but the pattern is unsafe.
- **Evidence:** `AdminFleetcheckActionForm.java` lines 1–69: no `reset()` method present. `struts-config.xml` line 394: `scope="request"`.
- **Recommendation:** Implement a `reset()` method that sets all user-supplied string fields to `null`.

---

### Category B: Type Safety

---

#### FINDING-05
- **Severity:** HIGH
- **File:** `src/main/java/com/dao/QuestionDAO.java`, lines 155–161
- **Description:** `Long.parseLong()` is called directly on form-sourced strings (`manuId`, `typeId`, `fuelTypeId`, `compId`, `attchId`) inside a lambda in `getQuestionByCategory()` with no prior numeric validation. Although `compId` originates from the session (`sessCompId`) rather than the form — partially reducing its attack surface — `manuId`, `typeId`, `fuelTypeId`, and `attchId` all come directly from `AdminFleetcheckActionForm` fields. A non-numeric value throws `NumberFormatException`, which propagates up as an unhandled application error. This can be used to probe server internals (error message leakage in development/staging) or to cause a denial-of-service condition.
- **Evidence:**
  ```java
  // QuestionDAO.java lines 155–161
  stmt.setLong(++index, Long.parseLong(manuId));
  stmt.setLong(++index, Long.parseLong(typeId));
  stmt.setLong(++index, Long.parseLong(fuelTypeId));
  stmt.setLong(++index, Long.parseLong(compId));
  if (StringUtils.isNotBlank(attchId)) {
      stmt.setLong(++index, Long.parseLong(attchId));
  }
  ```
  Form `validate()` only checks `isEmpty()`, not numeric format.
- **Recommendation:** Validate all four ID fields as numeric in `AdminFleetcheckActionForm.validate()` before they reach the DAO. Add try/catch around `parseLong` in the DAO as a secondary defensive measure, converting `NumberFormatException` to a controlled `IllegalArgumentException`.

---

#### FINDING-06
- **Severity:** HIGH
- **File:** `src/main/java/com/dao/QuestionDAO.java`, lines 231–242
- **Description:** `Integer.parseInt()` is called on form-sourced `typeId`, `manuId`, `fuleTypeId`, `attchId`, `compId`, and `id` inside `copyQuestionToCompId()`. The `id` parameter is sourced from `AdminFleetcheckHideActionForm` (a related form, not the subject form), but the other four parameters (`manuId`, `typeId`, `fuleTypeId`, `attchId`) trace back to the same unvalidated form-sourced strings. Same attack surface as FINDING-05 with the additional note that `copyQuestionToCompId` performs a database INSERT, making the impact of unexpected input higher.
- **Evidence:**
  ```java
  // QuestionDAO.java lines 231–242
  ps.setInt(1, Integer.parseInt(typeId));
  ps.setInt(2, Integer.parseInt(manuId));
  ps.setInt(3, Integer.parseInt(fuleTypeId));
  // ...
  ps.setInt(5, Integer.parseInt(compId));
  ps.setInt(6, Integer.parseInt(id));
  ps.setInt(7, Integer.parseInt(id));
  ```
  No numeric format check precedes any of these calls.
- **Recommendation:** Same as FINDING-05. All ID values must be validated as numeric at the form layer before reaching insert-path DAO code.

---

### Category C: IDOR Risk

---

#### FINDING-07
- **Severity:** HIGH
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`, lines 22–25
- **Description:** The fields `manu_id`, `type_id`, `fuel_type_id`, and `attachment_id` are direct database foreign-key IDs that are accepted verbatim from user-controlled HTTP request parameters. The action uses `sessCompId` (from the session) to scope query results at the company level in `getQuestionByCategory()`, which provides partial tenant isolation. However, there is no server-side verification that the submitted `manu_id`, `type_id`, `fuel_type_id`, and `attachment_id` values are valid and belong to the authenticated user's company context. An attacker can submit arbitrary integer values to enumerate or access question configurations belonging to other companies if the DAO filtering on `comp_id` has any gaps (e.g., global/null-comp_id records are always included in the UNION query at QuestionDAO.java lines 145–149).
- **Evidence:**
  - Form fields `manu_id` (line 22), `type_id` (line 23), `fuel_type_id` (line 24), `attachment_id` (line 25): all `String`, bound from HTTP params.
  - `AdminFleetcheckAction.java` lines 28–31: values read directly from form with no server-side ownership check.
  - `QuestionDAO.getQuestionByCategory()` (QuestionDAO.java lines 145–149): UNION query explicitly includes global questions (`comp_id is null`) for any submitted combination of IDs, meaning knowledge of valid global `manu_id`/`type_id`/`fuel_type_id` tuples is enough to retrieve questions regardless of company.
- **Recommendation:** Validate that submitted `manu_id`, `type_id`, `fuel_type_id`, and `attachment_id` values correspond to records that are either global or owned by `sessCompId` before passing them to the DAO. Reject the request if any foreign key value cannot be confirmed as accessible to the authenticated company.

---

#### FINDING-08
- **Severity:** MEDIUM
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`, line 21
- **Description:** The `id` field is declared on the form and bound from user input (Lombok `@Setter` generates a public setter). Although `AdminFleetcheckAction` does not directly use `id`, the field is present on the form and a Lombok-generated `setId()` method is publicly accessible. If Struts binds this field from HTTP parameters (which it will, given the generated setter), it can be populated by an attacker. This is a latent risk: if a future code path reads `getId()` without server-side ownership verification, it becomes an exploitable IDOR. The `id` field is actively exploited in the related `AdminFleetcheckHideActionForm`, which uses it to target specific question records — the same pattern on this form should be treated as a risk before it is wired up.
- **Evidence:**
  - `AdminFleetcheckActionForm.java` line 21: `private String id = null;` — Lombok `@Setter` creates `setId(String)`, which Struts 1 will bind from request parameter `id`.
  - `AdminFleetcheckAction.java`: `id` is not read; however the field is present and bindable.
- **Recommendation:** Remove the `id` field from `AdminFleetcheckActionForm` if it is not required by the current action. If it is needed for future paths, add ownership verification in the action before any DAO call that uses it.

---

### Category D: Sensitive Fields

---

#### FINDING-09
- **Severity:** MEDIUM
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`, lines 26–28
- **Description:** The three `ArrayList` fields `arrAdminUnitType`, `arrAdminUnitFuelType`, and `arrAttachment` are populated from the database in the constructor and used to populate UI dropdowns. Because Lombok `@Setter` is applied at the class level, public setters are generated for these collections (`setArrAdminUnitType(ArrayList)`, `setArrAdminUnitFuelType(ArrayList)`, `setArrAttachment(ArrayList)`). Struts 1 parameter binding can, in some configurations, invoke these setters via HTTP parameters, potentially overwriting server-authoritative lookup data with attacker-controlled content. Even if Struts does not bind directly to the ArrayList setters in practice, the exposure exists and the lookup data should not be settable from external input.
- **Evidence:**
  - Lines 26–28: `private ArrayList arrAdminUnitType`, `arrAdminUnitFuelType`, `arrAttachment` — all under class-level `@Setter`.
  - Lines 37–47: custom setter methods used for DB population, but Lombok also generates a `setArrAdminUnitType(ArrayList)` overload that accepts arbitrary list data.
- **Recommendation:** Annotate the three ArrayList fields with `@Setter(AccessLevel.NONE)` (Lombok) to suppress the public setter generation. Retain the custom private population methods. This prevents any possibility of the lookup lists being overwritten via HTTP parameter binding.

---

### Category E: Data Integrity (Whitelist)

---

#### FINDING-10
- **Severity:** MEDIUM
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`, line 20
- **Description:** The `action` field drives branching logic in `AdminFleetcheckAction` but is never validated against a whitelist of permitted values. Submitting an unexpected value causes silent fallthrough to the `else` branch (AdminFleetcheckAction.java lines 65–73), which calls `getQuestionByCategory()` even when `validate()` might have intended to block the request. This violates the principle that only known-good action values should be accepted and processed.
- **Evidence:**
  - `AdminFleetcheckActionForm.java` line 20: `private String action = null;`.
  - `AdminFleetcheckAction.java` lines 35–73: three-way branch with no `action` whitelist. The `else` clause (line 64) runs the DAO query with whatever IDs were submitted.
- **Recommendation:** Define an enum or constant set of permitted action values. Validate `action` against this set in `validate()`. Reject the form if the value is not in the whitelist.

---

#### FINDING-11
- **Severity:** LOW
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`, lines 22–25
- **Description:** The four ID fields (`manu_id`, `type_id`, `fuel_type_id`, `attachment_id`) have no maximum-length or format constraint defined anywhere (neither in `validate()` nor in `validation.xml`). An attacker can submit arbitrarily long strings. While the downstream `parseLong` / `parseInt` calls will throw an exception for non-numeric content, an extremely long numeric string (e.g., 10,000 digits) would also cause a `NumberFormatException` before reaching the DB, meaning no SQL is executed — but the exception still generates server-side log noise and may expose stack traces.
- **Evidence:** `validate()` (lines 54–65): only `StringUtils.isEmpty()` checked; no `maxlength` or `mask` validation. `validation.xml`: no rules for this form.
- **Recommendation:** Add `maxlength` constraints (e.g., 10 characters, matching typical integer ID range) on all four ID fields via `validation.xml` or `validate()`.

---

## 3. CSRF Structural Note

No CSRF token mechanism is present in this form or its action. As documented for this codebase: Apache Struts 1.3.10 does not provide built-in CSRF protection, and no application-level token is implemented. The `/fleetcheckconf.do` action (mapped with `validate="true"`) accepts a state-changing `add` operation via a standard form POST. An attacker who can induce an authenticated admin to load a crafted page can trigger question creation under the victim's `sessCompId`. This is a structural gap affecting the entire application and is noted here for completeness; it is tracked as a project-level finding rather than repeated per form.

---

## 4. Summary Table

| ID | Severity | Category | Short Description |
|----|----------|----------|-------------------|
| FINDING-01 | HIGH | Input Validation | No numeric format check in validate() for manu_id/type_id/fuel_type_id/attachment_id |
| FINDING-02 | MEDIUM | Input Validation | action field not whitelist-validated; else-branch bypasses validate() intent |
| FINDING-03 | MEDIUM | Input Validation | No validation.xml rules for adminFleetcheckActionForm |
| FINDING-04 | LOW | Input Validation | reset() method absent |
| FINDING-05 | HIGH | Type Safety | Long.parseLong() called without prior numeric check in getQuestionByCategory() |
| FINDING-06 | HIGH | Type Safety | Integer.parseInt() called without prior check in copyQuestionToCompId() (INSERT path) |
| FINDING-07 | HIGH | IDOR Risk | manu_id/type_id/fuel_type_id/attachment_id not verified against authenticated company |
| FINDING-08 | MEDIUM | IDOR Risk | id field bindable from HTTP params with no ownership check |
| FINDING-09 | MEDIUM | Sensitive Fields | Lookup ArrayList fields have Lombok-generated public setters allowing overwrite |
| FINDING-10 | MEDIUM | Data Integrity | action field not whitelisted; silent else-branch executes DAO query |
| FINDING-11 | LOW | Data Integrity | No maxlength constraint on any ID field |

### Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 4 (FINDING-01, FINDING-05, FINDING-06, FINDING-07) |
| MEDIUM | 5 (FINDING-02, FINDING-03, FINDING-08, FINDING-09, FINDING-10) |
| LOW | 2 (FINDING-04, FINDING-11) |
| INFO | 0 |
| **Total** | **11** |
