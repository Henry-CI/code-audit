# Audit Report: AdminFleetcheckDeleteActionForm

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**Auditor:** Security Audit Pass 1
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10

---

## 1. Reading Evidence

### 1.1 Package and Class Name

- **File:** `src/main/java/com/actionform/AdminFleetcheckDeleteActionForm.java`
- **Package:** `com.actionform`
- **Class:** `AdminFleetcheckDeleteActionForm`
- **Extends:** `ValidateIdExistsAbstractActionForm` (which extends `org.apache.struts.action.ActionForm`)

The class body is entirely empty — it contains no fields, no methods, and no annotations of its own. All behaviour is inherited from the parent abstract class.

### 1.2 Fields

The form class itself declares no fields. The sole field is inherited from the parent:

| Source | Type | Name | Lombok annotations | Default |
|--------|------|------|--------------------|---------|
| `ValidateIdExistsAbstractActionForm` (line 16) | `String` | `id` | `@Getter` / `@Setter` (class-level) | `null` |

### 1.3 validate() Method

**Exists:** Yes — inherited from `ValidateIdExistsAbstractActionForm` (lines 18–27). Not overridden in `AdminFleetcheckDeleteActionForm`.

**What it checks:**
- Uses `org.apache.commons.lang.StringUtils.isEmpty(this.id)`.
- If `id` is null or empty string, adds a single `ActionMessage("error.id")` keyed to field `"id"`.
- Returns the `ActionErrors` object (may be empty or contain one error).
- **Does NOT check:** numeric format, positive value, reasonable range, SQL-injection characters, or cross-tenant ownership.

### 1.4 reset() Method

**Exists:** No. Neither `AdminFleetcheckDeleteActionForm` nor `ValidateIdExistsAbstractActionForm` declares a `reset()` method. The Struts framework's default `ActionForm.reset()` is a no-op and will be called instead. Because the form is scoped as `request` in struts-config.xml (line 423), the practical impact is limited but the absence is still noteworthy.

### 1.5 validation.xml Rules

**None found.**

The file `src/main/webapp/WEB-INF/validation.xml` defines rules for exactly three forms:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

There is no `<form name="adminFleetcheckDeleteActionForm">` entry. The Commons Validator declarative layer provides zero additional constraint on the `id` field for this form.

---

## 2. Struts-Config Context

From `src/main/webapp/WEB-INF/struts-config.xml` lines 420–428:

```xml
<action
        path="/fleetcheckdelete"
        name="adminFleetcheckDeleteActionForm"
        scope="request"
        validate="true"
        type="com.action.AdminFleetcheckDeleteAction"
        input="adminChecklistDefinition">
    <forward name="success" path="adminChecklistDefinition"/>
</action>
```

- `validate="true"` — Struts will call `validate()` before dispatching to the Action.
- The only gate is the empty-string check in the parent abstract class.

---

## 3. Action and DAO Context

### AdminFleetcheckDeleteAction (lines 14–22)

```java
AdminFleetcheckDeleteActionForm adminFleetcheckDeleteActionForm =
    (AdminFleetcheckDeleteActionForm) actionForm;
QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId());
return null;
```

- Retrieves `id` directly from the form and passes it raw to the DAO.
- No session-based company/tenant ownership check.
- Returns `null` instead of a named `ActionForward`.

### QuestionDAO.delQuestionById (lines 174–195)

```java
String sql = "delete from question where id=" + id;
stmt.executeUpdate(sql);
```

- String concatenation, no `PreparedStatement`.
- No ownership / tenant filter in the WHERE clause.

---

## 4. Findings

---

### FINDING 1 — CRITICAL: SQL Injection via Unsanitised `id` Parameter

**Severity:** CRITICAL
**File + Line:** `src/main/java/com/dao/QuestionDAO.java`, line 183
**Category:** Input Validation

**Description:**
The `id` value collected by `AdminFleetcheckDeleteActionForm` is passed without sanitisation to `QuestionDAO.delQuestionById()`, which builds a raw SQL DELETE statement via string concatenation:

```java
String sql = "delete from question where id=" + id;
stmt.executeUpdate(sql);
```

The only upstream gate is `StringUtils.isEmpty()`, which accepts any non-empty string. An attacker who can reach `/fleetcheckdelete` may supply a crafted `id` value (e.g., `1 OR 1=1`, `1; DROP TABLE question--`) to delete arbitrary rows, truncate the table, or (depending on database user privileges) execute stacked queries.

**Evidence:**
- `ValidateIdExistsAbstractActionForm.validate()` (line 22): checks only that `id` is non-empty — no format, numeric, or whitelist check.
- `QuestionDAO.delQuestionById()` (line 183): raw string concatenation into a `Statement.executeUpdate()`.
- `validation.xml`: no entry for `adminFleetcheckDeleteActionForm`.

**Recommendation:**
Replace `Statement` with `PreparedStatement`:
```java
String sql = "delete from question where id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setLong(1, Long.parseLong(id));
ps.executeUpdate(ps);
```
Add numeric format validation in `validate()` (or via validation.xml) before the value reaches the DAO. Reject any `id` that does not match `^\d+$`.

---

### FINDING 2 — CRITICAL: Insecure Direct Object Reference (IDOR) — No Ownership / Tenant Check

**Severity:** CRITICAL
**File + Line:** `src/main/java/com/action/AdminFleetcheckDeleteAction.java`, lines 19–21; `src/main/java/com/dao/QuestionDAO.java`, line 183
**Category:** IDOR Risk

**Description:**
The DELETE operation is performed using only the user-supplied `id`. There is no check that the authenticated user's company (`comp_id`) matches the `comp_id` on the `question` record being deleted. Any authenticated admin may delete questions belonging to any other tenant by enumerating question IDs.

**Evidence:**
- `AdminFleetcheckDeleteAction.execute()` makes no reference to the HTTP session or any company/tenant context.
- `QuestionDAO.delQuestionById()` SQL (line 183): `delete from question where id=<id>` — no `comp_id` predicate.
- No session attribute lookup in the Action for company scope (grep returns no matches for `session`, `comp_id`, `compId`, `isAdmin`, `authorize`, `permission`, or `role` in the Action file).

**Recommendation:**
Retrieve the authenticated user's `comp_id` from the HTTP session and include it as an additional predicate in the DELETE query, or perform a pre-delete ownership check:

```java
// pseudocode
String sessionCompId = (String) request.getSession().getAttribute("compId");
QuestionDAO.delQuestionByIdAndCompId(form.getId(), sessionCompId);
```

The DAO method should use:
```sql
delete from question where id = ? and comp_id = ?
```

---

### FINDING 3 — HIGH: No Numeric / Format Validation on `id` Field

**Severity:** HIGH
**File + Line:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`, lines 18–27; `src/main/webapp/WEB-INF/validation.xml` (absence)
**Category:** Input Validation / Type Safety

**Description:**
The `id` field is typed as `String`. The `validate()` method checks only `StringUtils.isEmpty()`. There is no check that the value is a valid positive integer before it is used in a SQL integer comparison column. Non-numeric values will either cause a database type error (information disclosure via exception propagation) or, when concatenated, enable SQL injection (see Finding 1).

**Evidence:**
- `id` field declared as `String` in `ValidateIdExistsAbstractActionForm` (line 16).
- `validate()` (lines 18–27): only `StringUtils.isEmpty()`.
- `validation.xml`: no `integer` or `regex` rule for this form.
- DAO uses `id` directly in string concatenation (line 183) — no `Long.parseLong()` guard.

**Recommendation:**
Add a numeric format check in the abstract `validate()` or override it in the concrete form:
```java
if (!id.matches("^\\d+$")) {
    errors.add("id", new ActionMessage("error.id.invalid"));
}
```
Alternatively add a `<field property="id" depends="required,integer">` entry in `validation.xml` for this form.

---

### FINDING 4 — HIGH: CSRF — Destructive State-Changing Action Has No Token Protection

**Severity:** HIGH
**File + Line:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 420–428; `src/main/java/com/action/AdminFleetcheckDeleteAction.java`
**Category:** Input Validation (Structural — CSRF)

**Description:**
The `/fleetcheckdelete` endpoint performs a permanent, irreversible DELETE of a database record. As documented for this stack, CSRF protection is a structural gap in Struts 1.3.10. There is no synchroniser token, SameSite cookie attribute, or custom header check on this action. A forged cross-origin POST with a valid `id` parameter will be processed without any origin verification, allowing an attacker to delete question records by tricking a logged-in admin into visiting a malicious page.

The impact is compounded by the IDOR in Finding 2: an attacker does not even need to know the target admin's company — they can delete any question record.

**Evidence:**
- No CSRF token field in `AdminFleetcheckDeleteActionForm`.
- No `Globals.TRANSACTION_TOKEN_KEY` or `saveToken()`/`isTokenValid()` calls in `AdminFleetcheckDeleteAction`.
- `struts-config.xml` action entry contains no custom request processor or token-checking interceptor.

**Recommendation:**
Implement Struts synchroniser token pattern:
- Call `saveToken(request)` when rendering the checklist definition page.
- Call `isTokenValid(request, true)` at the start of `AdminFleetcheckDeleteAction.execute()` and reject the request if invalid.
Alternatively, enforce a `SameSite=Strict` (or `Lax`) cookie policy at the session level as a defence-in-depth measure.

---

### FINDING 5 — HIGH: Action Returns `null` — No Error Path / Response After Deletion

**Severity:** HIGH
**File + Line:** `src/main/java/com/action/AdminFleetcheckDeleteAction.java`, line 21
**Category:** Data Integrity

**Description:**
`AdminFleetcheckDeleteAction.execute()` returns `null` after calling the DAO. In Struts 1, returning `null` from `execute()` means no further response processing occurs — the response may be left uncommitted or result in a blank page / HTTP 200 with empty body. There is also no `try/catch` or error handling; an exception from `QuestionDAO.delQuestionById()` will propagate uncaught to the Struts framework and may expose a stack trace to the client.

**Evidence:**
- `AdminFleetcheckDeleteAction.execute()` (line 21): `return null;`.
- The action declares a `success` forward in struts-config but never uses it.
- No exception handling block in the Action class.

**Recommendation:**
Return the declared forward on success:
```java
return mapping.findForward("success");
```
Wrap the DAO call in a try/catch that returns a named error forward and logs the exception, preventing stack-trace disclosure.

---

### FINDING 6 — MEDIUM: `id` Field Not Reset Between Requests

**Severity:** MEDIUM
**File + Line:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`, line 16; `src/main/webapp/WEB-INF/struts-config.xml`, line 423
**Category:** Data Integrity

**Description:**
Neither `AdminFleetcheckDeleteActionForm` nor `ValidateIdExistsAbstractActionForm` overrides `reset()`. The form is scoped as `request` in struts-config, which mitigates the most severe replay risk (a new form instance is created per request). However, the absence of `reset()` means that if the scope were ever changed to `session`, stale `id` values would persist across requests, potentially acting on the wrong record. Additionally, the explicit declaration of `reset()` is considered a defensive standard for Struts ActionForms.

**Evidence:**
- No `reset()` method in either `AdminFleetcheckDeleteActionForm` or `ValidateIdExistsAbstractActionForm`.
- `struts-config.xml` line 423: `scope="request"` (current mitigation).

**Recommendation:**
Add a `reset()` override in `ValidateIdExistsAbstractActionForm`:
```java
@Override
public void reset(ActionMapping mapping, HttpServletRequest request) {
    this.id = null;
}
```

---

### FINDING 7 — LOW: SQL Logged in Plain Text Including User-Supplied Value

**Severity:** LOW
**File + Line:** `src/main/java/com/dao/QuestionDAO.java`, line 184
**Category:** Data Integrity / Sensitive Fields

**Description:**
`log.info(sql)` logs the full SQL string, which contains the raw user-supplied `id` value prior to execution. If the `id` value is a SQL injection payload, the malicious string is written to the application log. Log files may be accessible to operators or forwarded to SIEM systems with insufficient controls, potentially aiding an attacker in refining an injection payload.

**Evidence:**
```java
String sql = "delete from question where id=" + id;
log.info(sql);
stmt.executeUpdate(sql);
```

**Recommendation:**
After migrating to `PreparedStatement` (see Finding 1), log only the parameterised query template without the bound values, or log a sanitised identifier (e.g., the parsed `Long` value after validation).

---

## 5. Category Summary

| Category | Findings |
|----------|----------|
| Input Validation | F1 (CRITICAL), F3 (HIGH), F4 (HIGH) |
| Type Safety | F3 (HIGH) |
| IDOR Risk | F2 (CRITICAL) |
| Sensitive Fields | F7 (LOW) — logged SQL contains user input; no sensitive PII fields in the form itself |
| Data Integrity | F5 (HIGH), F6 (MEDIUM), F7 (LOW) |

---

## 6. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 2 (F1, F2) |
| HIGH | 3 (F3, F4, F5) |
| MEDIUM | 1 (F6) |
| LOW | 1 (F7) |
| INFO | 0 |
| **Total** | **7** |

---

## 7. Files Examined

| File | Purpose |
|------|---------|
| `src/main/java/com/actionform/AdminFleetcheckDeleteActionForm.java` | Subject form (empty body) |
| `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java` | Parent abstract class — provides `id` field and `validate()` |
| `src/main/java/com/action/AdminFleetcheckDeleteAction.java` | Action that consumes the form |
| `src/main/java/com/dao/QuestionDAO.java` | DAO — contains `delQuestionById()` (SQL injection sink) |
| `src/main/webapp/WEB-INF/struts-config.xml` | Action mapping — confirms `validate="true"`, `scope="request"` |
| `src/main/webapp/WEB-INF/validation.xml` | Commons Validator rules — no entry for this form |
