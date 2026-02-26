# Audit Report: AdminFleetcheckEditActionForm
**Audit run:** audit/2026-02-26-01/
**Branch:** master
**Auditor:** CIG Security Audit (Pass 1)
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10

---

## 1. Reading Evidence

### Package and Class
- **File:** `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java`
- **Package:** `com.actionform`
- **Class:** `AdminFleetcheckEditActionForm extends ActionForm`
- **Annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor` (Lombok)
- **serialVersionUID:** `-8103158863153194997L`

### Fields (all declared at class level, lines 20-31)

| Line | Name             | Type                        | Default       |
|------|------------------|-----------------------------|---------------|
| 20   | `id`             | `String`                    | `null`        |
| 21   | `content`        | `String`                    | `null`        |
| 22   | `expectedanswer` | `String`                    | `null`        |
| 23   | `order_no`       | `int`                       | `0` (JVM default) |
| 24   | `active`         | `String`                    | `null`        |
| 25   | `type_id`        | `String`                    | `null`        |
| 26   | `fuel_type_id`   | `String`                    | `null`        |
| 27   | `answer_type`    | `String`                    | `null`        |
| 28   | `comp_id`        | `String`                    | `null`        |
| 29   | `arrAnswerType`  | `ArrayList<AnswerTypeBean>` | `new ArrayList<>()` |
| 30   | `manu_id`        | `String`                    | `null`        |
| 31   | `attachment_id`  | `String`                    | `null`        |

### validate() method
**Not overridden.** The form inherits the no-op `ActionForm.validate()` which returns an empty `ActionErrors` object. No server-side validation logic exists in this class.

### reset() method
**Not overridden.** The form inherits the no-op `ActionForm.reset()`. The `order_no` primitive `int` field is never explicitly reset; it retains its JVM default of `0` between requests if not submitted.

### validation.xml rules for this form
**None.** The file `src/main/webapp/WEB-INF/validation.xml` defines rules for exactly three forms:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

`adminFleetcheckEditActionForm` is **absent** from validation.xml entirely.

### struts-config.xml mapping (for reference)
`src/main/webapp/WEB-INF/struts-config.xml` lines 381-390:
```xml
<action
    path="/fleetcheckedit"
    name="adminFleetcheckEditActionForm"
    scope="request"
    validate="true"
    type="com.action.AdminFleetcheckEditAction">
```
`validate="true"` is set, but because no `<form>` entry exists in `validation.xml` for `adminFleetcheckEditActionForm`, the Commons Validator framework performs no validation at all — the `validate="true"` flag is silently inert.

---

## 2. Audit Findings

---

### FINDING 01 — CRITICAL: SQL Injection via `id` field used in `getQuestionById`

**Severity:** CRITICAL
**File + Line:**
- Form field: `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` line 20
- Sink: `src/main/java/com/dao/QuestionDAO.java` line 275
- Action: `src/main/java/com/action/AdminFleetcheckEditAction.java` line 40

**Description:**
The `id` field is a raw `String` accepted directly from user HTTP input. In the GET path of `AdminFleetcheckEditAction.execute()`, it is passed without any sanitisation to `QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId())`. That DAO method concatenates the value directly into a SQL string:

```java
// QuestionDAO.java line 275
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id," +
             "attachment_id,answer_type,comp_id, active from question where id = " + id;
```

An attacker who can reach the `/fleetcheckedit.do?id=1 OR 1=1` endpoint can exfiltrate all question records. More destructive payloads (UNION SELECT, stacked queries depending on the JDBC driver / database) are also possible.

**Evidence:**
- `AdminFleetcheckEditAction.java` line 40: `QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId())`
- `QuestionDAO.java` line 275: `"... where id = " + id` (string concatenation, no PreparedStatement)
- Form field `id` is `String` with no numeric validation in the form, no validation.xml rule, and no `validate()` override.

**Recommendation:**
Replace the `Statement`-based concatenation in `QuestionDAO.getQuestionById` with a `PreparedStatement` using a `?` placeholder. Additionally, validate `id` as a positive integer in the form's `validate()` method before any DAO call is made.

---

### FINDING 02 — CRITICAL: SQL Injection via `id` field used in `delQuestionById`

**Severity:** CRITICAL
**File + Line:**
- Sink: `src/main/java/com/dao/QuestionDAO.java` line 183

**Description:**
`QuestionDAO.delQuestionById(String id)` constructs a DELETE statement by direct string concatenation:

```java
// QuestionDAO.java line 183
String sql = "delete from question where id=" + id;
stmt.executeUpdate(sql);
```

If any action in the application passes the form's `id` field to this method without sanitisation, an attacker can delete arbitrary rows or (with stacked queries) cause broader damage. The pattern is identical to Finding 01 and stems from the same unvalidated `id` field.

**Evidence:**
- `QuestionDAO.java` lines 183-185: bare string concatenation in a DELETE statement.
- The `id` field originates from the same form and is a raw, unvalidated `String`.

**Recommendation:**
Use a `PreparedStatement` with a `?` placeholder for all DELETE operations involving user-supplied identifiers. Enforce integer-only format at the form/action layer.

---

### FINDING 03 — CRITICAL: SQL Injection via `compId` / `qId` / `lanId` in multiple DAO methods

**Severity:** CRITICAL
**File + Line:**
- `src/main/java/com/dao/QuestionDAO.java` lines 42, 83-89, 275, 328-330

**Description:**
Several DAO methods used in the fleetcheck edit flow concatenate user-derived or session-derived string values directly into SQL without parameterisation:

- `getQuesLanId`: `"select lan_id from company where id = " + compId` (line 42) — `compId` comes from the session but was originally user-supplied at registration and is not re-validated here.
- `getQuestionByUnitId`: multiple columns including `unitId`, `compId`, `lanId` concatenated into a multi-join query (lines 83-89).
- `getQuestionContentById`: `"select content from question where id = " + qId` and `"... where question_id = " + qId + " and lan_id = " + lanId` (lines 328-330).

While some of these values are sourced from the session, the root cause of unparameterised queries is systemic. Any path that allows a value to be influenced by user input is exploitable.

**Evidence:**
- `QuestionDAO.java` line 42: `"select lan_id from company where id = " + compId`
- `QuestionDAO.java` line 85: `" where unit.id = " + unitId + " and ... comp_id = " + compId`
- `QuestionDAO.java` line 275: `"... where id = " + id`
- `QuestionDAO.java` line 328: `"select content from question where id = " + qId`
- `QuestionDAO.java` line 330: `"... where question_id = " + qId + " and lan_id = " + lanId`

**Recommendation:**
Refactor all DAO query construction to use `PreparedStatement`. This is a systemic issue in the DAO layer that should be addressed via a project-wide remediation pass.

---

### FINDING 04 — HIGH: No Server-Side Input Validation on Any Form Field

**Severity:** HIGH
**File + Line:**
- `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` lines 20-31 (all fields)
- `src/main/webapp/WEB-INF/validation.xml` (absence of entry)
- `src/main/webapp/WEB-INF/struts-config.xml` line 384 (`validate="true"`)

**Description:**
Although `validate="true"` is set in struts-config.xml, there is no corresponding `<form name="adminFleetcheckEditActionForm">` block in validation.xml. The Commons Validator therefore performs zero validation for this form. The form's own `validate()` method is not overridden. The result is that every field reaches the action layer completely unchecked:

- `id`, `type_id`, `fuel_type_id`, `manu_id`, `attachment_id`, `comp_id`, `answer_type`, `order_no` — all numeric foreign-key fields — accept arbitrary strings with no length, format, or range check.
- `content` — a free-text question body — has no maximum length constraint, enabling potential denial-of-service via oversized payloads or XSS via stored markup.
- `expectedanswer` — constrained by a UI `<html:select>` to YES/NO, but the server never enforces this; any string is accepted.
- `active` — similar select-only constraint at the UI layer; server enforces nothing.

**Evidence:**
- `validation.xml` contains no entry for `adminFleetcheckEditActionForm`.
- `AdminFleetcheckEditActionForm.java`: no `validate()` override.
- `AdminFleetcheckEditAction.java` lines 46-65: all field values consumed without any guard.

**Recommendation:**
Add a `<form name="adminFleetcheckEditActionForm">` block to `validation.xml` with at minimum: `required` + `integer` checks on all ID fields; `maxlength` on `content` and `expectedanswer`; `required` on `content`, `type_id`, `fuel_type_id`, `manu_id`. Supplement with an overridden `validate()` method for business-logic checks (e.g., enumeration check on `expectedanswer` and `active`).

---

### FINDING 05 — HIGH: Type Safety — `order_no` Declared as Primitive `int` Without Input Validation

**Severity:** HIGH
**File + Line:**
- `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` line 23
- `src/main/java/com/action/AdminFleetcheckEditAction.java` line 65

**Description:**
`order_no` is declared as primitive `int`. Struts 1.x binding will attempt to convert the HTTP parameter string to `int` at bind time. If the submitted value is non-numeric, empty, or exceeds `Integer.MAX_VALUE`, Struts generates a binding error and populates `ActionErrors`. However, because `validate="true"` with no matching validation rule means the validator phase is a no-op, and because the action itself does not inspect binding errors from the form, the error is silently ignored and `order_no` defaults to `0`. This means:

1. An attacker can force `order_no = 0` on any edit, corrupting question ordering.
2. There is no explicit maximum bound; an arbitrarily large valid integer is accepted and stored.

The same `order_no` value is passed as `ps.setInt(4, questionBean.getOrder_no())` in `saveQuestionInfo` (QuestionDAO line 387) — at that point any integer is written directly to the database.

**Evidence:**
- Form field `order_no` is `int` (line 23), not `Integer` (no null-check capability).
- No `validate()` override to call `errors.hasErrors()` after binding.
- `AdminFleetcheckEditAction.java` line 65: `order_no` consumed without range check.

**Recommendation:**
Change `order_no` to `String` in the form, validate it as a required positive integer in `validate()` or validation.xml, then parse it explicitly in the action. Alternatively, keep `int` but override `validate()` to inspect binding errors and reject non-positive values.

---

### FINDING 06 — HIGH: IDOR — `id` Field Allows Cross-Tenant Question Modification

**Severity:** HIGH
**File + Line:**
- `src/main/java/com/action/AdminFleetcheckEditAction.java` lines 46, 71-73
- `src/main/java/com/dao/QuestionDAO.java` lines 527-537 (`updateQuestionInfo`)

**Description:**
On POST, the action reads `questionId` from the form (`adminFleetcheckEditActionForm.getId()`, line 46) and passes it directly to `QuestionDAO.updateQuestionInfo(bean)`. The UPDATE statement in that DAO method is:

```java
// QuestionDAO.java line 527
String sql = "update question set content = ?, expectedanswer = ?, answer_type = ?, active = ? where id = ?";
```

There is **no ownership check** before or within the UPDATE: the code does not verify that the question identified by `id` belongs to the same company (`comp_id`) as the currently authenticated admin. An authenticated admin from Company A can submit `id` = any valid question ID for Company B (or a global question) and overwrite its `content`, `expectedanswer`, `answer_type`, and `active` fields.

Note that the `bean.setComp_id(sessCompId)` call (line 66) sets the company on the bean used for CREATE, but `updateQuestionInfo` ignores `comp_id` entirely in its WHERE clause.

**Evidence:**
- `AdminFleetcheckEditAction.java` line 66: `comp_id` set from session to bean only.
- `QuestionDAO.java` line 527: `WHERE id = ?` — no `AND comp_id = ?` guard.
- No pre-update ownership query in the action (e.g., `getQuestionById` result is not checked against `sessCompId`).

**Recommendation:**
Before calling `updateQuestionInfo`, retrieve the question by `id` via `getQuestionById` and assert that its `comp_id` equals `sessCompId`. Add `AND comp_id = ?` to the UPDATE WHERE clause as a defence-in-depth database-layer guard. Global questions (comp_id IS NULL) should not be directly modifiable via this endpoint.

---

### FINDING 07 — HIGH: IDOR — `comp_id` Supplied as Hidden Form Field, Bypassable Client-Side

**Severity:** HIGH
**File + Line:**
- `src/main/webapp/html-jsp/adminChecklistEdit.jsp` line 64
- `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` line 28
- `src/main/java/com/action/AdminFleetcheckEditAction.java` line 66

**Description:**
The JSP renders `comp_id` as a hidden HTML input field:

```jsp
<!-- adminChecklistEdit.jsp line 64 -->
<html:hidden property="comp_id" name="question" />
```

The JavaScript `submit()` function reads this field and POSTs it to the server. Although the action ultimately overrides the form's `comp_id` with the session value (`sessCompId`) when building the `QuestionBean` for create/update, the form field `comp_id` is still bound from HTTP request parameters. A malicious user can observe the pattern, understand the intent, and could in a different code path (or future change) exploit the field to target another company. The exposure of `comp_id` in the rendered HTML also leaks internal database identifiers to end users.

**Evidence:**
- `adminChecklistEdit.jsp` line 64: `<html:hidden property="comp_id" name="question" />`
- `AdminFleetcheckEditActionForm.java` line 28: `private String comp_id = null;`
- `AdminFleetcheckEditAction.java` line 66: `comp_id(sessCompId)` — session value overrides the form field correctly in the current code, but the form field remains a vector.

**Recommendation:**
Remove `comp_id` from the form fields entirely — both the JSP hidden input and the `AdminFleetcheckEditActionForm` field. The action already sources `comp_id` from the session exclusively; the form field serves no function and represents unnecessary attack surface. Removing it eliminates the client-side exposure of internal IDs.

---

### FINDING 08 — HIGH: Stored XSS via Unvalidated `content` Field

**Severity:** HIGH
**File + Line:**
- `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` line 21
- `src/main/java/com/action/AdminFleetcheckEditAction.java` line 52
- `src/main/java/com/dao/QuestionDAO.java` lines 387, 531 (stored)

**Description:**
The `content` field accepts free-text question body content. There is no server-side length limit, no HTML encoding, and no XSS sanitisation applied before the value is stored in the `question.content` database column. When retrieved and rendered in JSPs (e.g., `adminChecklistEdit.jsp` line 25-29 via `<html:textarea>`), Struts 1.x `<html:textarea>` does HTML-encode the value in that particular tag. However:

1. The same question content is also stored in `question_content` table via `saveQuestionContent` and may be rendered via other JSPs or XML-based response paths (see `getQuestionContentById` which returns raw content for XML export — `XmlBean.setName(rs.getString(1))`). If any XML/JSON output path renders this without encoding it will be a stored XSS sink.
2. The lack of a maximum length check means arbitrarily large payloads can be stored, constituting a denial-of-service vector against the database and any rendering component.

**Evidence:**
- `AdminFleetcheckEditActionForm.java` line 21: `private String content = null;` — no constraint.
- `validation.xml`: no `maxlength` or `mask` rule for `content`.
- `QuestionDAO.java` line 387: `ps.setString(2, questionBean.getContent())` — raw value stored.
- `QuestionDAO.java` line 337: `xmlBean.setName(rs.getString(1))` — content placed in `XmlBean` used for XML output without visible encoding.

**Recommendation:**
Enforce a `maxlength` constraint on `content` in validation.xml (e.g., 1000 characters). Apply server-side HTML sanitisation (e.g., OWASP Java HTML Sanitizer) before persistence. Ensure all rendering paths — including any XML/API output — encode `content` appropriately for their output format.

---

### FINDING 09 — MEDIUM: `expectedanswer` and `active` Not Validated Against Allowed Values

**Severity:** MEDIUM
**File + Line:**
- `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` lines 22, 24
- `src/main/java/com/dao/QuestionDAO.java` line 534

**Description:**
`expectedanswer` is intended to be `"YES"` or `"NO"` (enforced only by an HTML `<select>` at line 35-46 of the JSP). `active` is intended to be `"t"` or `"f"` (the DAO casts it as `questionBean.getActive().equalsIgnoreCase("t")` for a boolean at line 534). Both fields are accepted as arbitrary strings from HTTP parameters. The server never validates the enumeration. Consequences:

- A non-`"t"`/`"f"` value for `active` does not crash the application (it evaluates to `false`) but represents a silent data integrity failure.
- A crafted `expectedanswer` value is stored verbatim in the database and returned to mobile/web clients that may interpret it.

**Evidence:**
- JSP lines 35-46 and 65: client-side-only constraint via `<html:select>` and `<html:hidden>`.
- `QuestionDAO.java` line 534: `questionBean.getActive().equalsIgnoreCase("t")` — no prior null/value check.
- `validation.xml`: no `mask` rule for `expectedanswer` or `active`.

**Recommendation:**
Add server-side enumeration checks in the form's `validate()` method: reject any `expectedanswer` that is not `"YES"` or `"NO"`, and any `active` that is not `"t"` or `"f"`. A null/empty `active` on an update path will cause a `NullPointerException` in `updateQuestionInfo` (line 534); add a null guard there as well.

---

### FINDING 10 — MEDIUM: NullPointerException Risk — `active` Not Null-Checked Before `equalsIgnoreCase`

**Severity:** MEDIUM
**File + Line:**
- `src/main/java/com/dao/QuestionDAO.java` line 534
- `src/main/java/com/action/AdminFleetcheckEditAction.java` line 79

**Description:**
`updateQuestionInfo` calls `questionBean.getActive().equalsIgnoreCase("t")` (line 534) without a null guard. If `active` is `null` (its default value in the form at line 24), this throws a `NullPointerException` at runtime, producing an HTTP 500 error. An unauthenticated-but-session-valid attacker who omits the `active` parameter from a crafted POST request can trigger this unhandled exception, potentially revealing stack traces and internal class/package information in default Struts error pages.

**Evidence:**
- `AdminFleetcheckEditActionForm.java` line 24: `private String active = null;`
- `QuestionDAO.java` line 534: `questionBean.getActive().equalsIgnoreCase("t")` — no null check preceding this call.
- No validation rule or `validate()` override ensures `active` is non-null before the DAO is invoked.

**Recommendation:**
Add a null guard in `updateQuestionInfo`: `"t".equalsIgnoreCase(questionBean.getActive())` (reversed operands) or an explicit `if (questionBean.getActive() == null) throw new IllegalArgumentException(...)`. Validate `active` as required in the form layer.

---

### FINDING 11 — MEDIUM: `answer_type` Not Validated as Integer Before `Integer.parseInt`

**Severity:** MEDIUM
**File + Line:**
- `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` line 27
- `src/main/java/com/dao/QuestionDAO.java` lines 399, 533

**Description:**
`answer_type` is a `String` in the form. In both `saveQuestionInfo` (line 399) and `updateQuestionInfo` (line 533), the code calls `Integer.parseInt(questionBean.getAnswer_type())`. If `answer_type` is `null`, empty, or non-numeric, this throws a `NumberFormatException` at runtime — an unhandled exception in the DAO that surfaces as HTTP 500. The `arrAnswerType` list is populated from the database via `QuestionDAO.getAllAnswerType()`, but a crafted HTTP request can bypass the dropdown entirely.

**Evidence:**
- `AdminFleetcheckEditActionForm.java` line 27: `private String answer_type = null;`
- `QuestionDAO.java` line 399: `ps.setInt(10, Integer.parseInt(questionBean.getAnswer_type()))` — no prior validation.
- `QuestionDAO.java` line 533: `ps.setInt(3, Integer.parseInt(questionBean.getAnswer_type()))` — same issue.
- `validation.xml`: no `integer` or `required` rule for `answer_type`.

**Recommendation:**
Add `required` and `integer` validation rules for `answer_type` in validation.xml. Also validate that the parsed integer is a valid `answer_type.id` value (exists in the lookup table) to prevent insertion of orphaned foreign-key references.

---

### FINDING 12 — MEDIUM: `id` Field Used as Both Create/Update Switch Without Authorisation Check

**Severity:** MEDIUM
**File + Line:**
- `src/main/java/com/action/AdminFleetcheckEditAction.java` lines 69-73

**Description:**
The action uses the presence or absence of `questionId` as the sole switch between create and update operations:

```java
if (StringUtils.isEmpty(questionId)) {
    return create(mapping, request, bean, lan_id);
} else {
    return update(mapping, request, bean, active, lan_id);
}
```

There is no server-side state to confirm which operation the user was authorised to perform. A user who navigates to a create form (empty `id`) could craft a POST that supplies a valid existing `id` to force an update instead, and vice versa. The missing pre-update ownership check (Finding 06) compounds this: any valid `id` triggers an update path against that record.

**Evidence:**
- `AdminFleetcheckEditAction.java` lines 69-73: operation routing is entirely controlled by the user-supplied `id` field.

**Recommendation:**
Validate the intended operation server-side (e.g., via a session-stored expected operation token or by looking up whether the record exists and belongs to the current company before choosing the path). Tie this to the IDOR fix in Finding 06.

---

### FINDING 13 — LOW: `reset()` Not Overridden — `order_no` Retains Stale Value

**Severity:** LOW
**File + Line:**
- `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java` line 23

**Description:**
`order_no` is a primitive `int`. The `reset()` method is not overridden, so in Struts 1.x session-scoped forms (or if the scope were changed to session), the field would retain its value from a prior request. In request scope (as configured) the risk is lower, but the lack of a `reset()` override is a structural gap that can cause subtle state bleed if the scope is ever changed, or in test/integration environments that reuse form instances.

**Evidence:**
- `AdminFleetcheckEditActionForm.java` line 23: `private int order_no;` — no `reset()` to zero it explicitly.
- `struts-config.xml` line 383: `scope="request"` — currently mitigates the issue.

**Recommendation:**
Override `reset()` to explicitly zero/null all fields, consistent with Struts 1.x best practice for `ActionForm` classes.

---

### FINDING 14 — LOW: Sensitive Internal Identifiers Exposed in Hidden Form Fields

**Severity:** LOW
**File + Line:**
- `src/main/webapp/html-jsp/adminChecklistEdit.jsp` lines 59-65

**Description:**
The rendered HTML exposes the following internal database IDs as plaintext hidden fields readable in browser developer tools or via view-source:

- `id` (question primary key)
- `type_id`, `fuel_type_id`, `manu_id`, `attachment_id` (foreign keys)
- `comp_id` (company identifier)

While this is a common Struts 1.x pattern for maintaining state across form submissions, unnecessarily exposing these identifiers to the client increases the attack surface for IDOR exploitation (see Findings 06 and 07) and leaks the internal data model to potential attackers.

**Evidence:**
- `adminChecklistEdit.jsp` lines 59-65: five `<html:hidden>` fields plus one plain `<input type="hidden">` rendering internal IDs.

**Recommendation:**
Evaluate each hidden field and remove those (like `comp_id`) that should be sourced from the session server-side. For genuinely required round-trip fields, consider using signed/encrypted session tokens or server-side state storage (e.g., storing the context in the session keyed by a nonce) rather than raw database IDs in hidden inputs.

---

### FINDING 15 — INFO: CSRF — Structural Gap (Known Stack-Wide Issue)

**Severity:** INFO
**File + Line:**
- `src/main/webapp/html-jsp/adminChecklistEdit.jsp` lines 93-108 (AJAX POST)
- `src/main/java/com/action/AdminFleetcheckEditAction.java` (POST handler)

**Description:**
As documented for this stack, Struts 1.3.10 has no built-in CSRF protection mechanism. The `/fleetcheckedit.do` endpoint accepts POST requests (including AJAX via `$.post()`) with no CSRF token. A malicious page loaded in a browser where an admin is authenticated could silently create or modify fleetcheck questions. This is a known structural gap affecting the entire application, not specific to this form alone.

**Evidence:**
- `adminChecklistEdit.jsp` line 94: `$.post('fleetcheckedit.do', { ... })` — no CSRF token in the payload.
- No CSRF filter or token check visible in the action or a Struts plugin configuration.

**Recommendation:**
Implement a synchroniser token pattern: generate a per-session or per-form token server-side, embed it as a hidden field in all forms, and validate it on every state-changing POST. The OWASP CSRFGuard library integrates with Struts 1.x applications.

---

## 3. Category Summary

| Category            | Status                                               |
|---------------------|------------------------------------------------------|
| Input Validation    | ISSUES FOUND — Findings 04, 09, 11, 12               |
| Type Safety         | ISSUES FOUND — Findings 05, 10, 11, 13               |
| IDOR Risk           | ISSUES FOUND — Findings 06, 07, 12                   |
| Sensitive Fields    | ISSUES FOUND — Findings 07, 14                       |
| Data Integrity      | ISSUES FOUND — Findings 01, 02, 03, 08, 09, 10, 15  |

No category is free of issues.

---

## 4. Finding Count by Severity

| Severity | Count | Finding Numbers              |
|----------|-------|------------------------------|
| CRITICAL | 3     | 01, 02, 03                   |
| HIGH     | 5     | 04, 05, 06, 07, 08           |
| MEDIUM   | 4     | 09, 10, 11, 12               |
| LOW      | 2     | 13, 14                       |
| INFO     | 1     | 15                           |
| **Total**| **15**|                              |
