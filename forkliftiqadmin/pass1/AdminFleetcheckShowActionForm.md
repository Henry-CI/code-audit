# Security Audit Report: AdminFleetcheckShowActionForm

**Audit run:** audit/2026-02-26-01
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Stack:** Apache Struts 1.3.10

---

## 1. Reading Evidence

### 1.1 Package and Class

| Item | Value |
|------|-------|
| File | `src/main/java/com/actionform/AdminFleetcheckShowActionForm.java` |
| Package | `com.actionform` |
| Class | `AdminFleetcheckShowActionForm` |
| Superclass | `ValidateIdExistsAbstractActionForm` (which extends `org.apache.struts.action.ActionForm`) |
| Body | Empty — zero additional fields, no `validate()` override, no `reset()` override |

### 1.2 Inherited Fields (from `ValidateIdExistsAbstractActionForm`)

File: `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`

| Field | Type | Default | Lombok |
|-------|------|---------|--------|
| `id` | `String` | `null` | `@Getter` / `@Setter` on class |

### 1.3 `validate()` Details (inherited, not overridden)

Source: `ValidateIdExistsAbstractActionForm.java` lines 18–27

```java
@Override
public ActionErrors validate(ActionMapping mapping, HttpServletRequest request) {
    ActionErrors errors = new ActionErrors();
    if (StringUtils.isEmpty(this.id)) {
        ActionMessage message = new ActionMessage("error.id");
        errors.add("id", message);
    }
    return errors;
}
```

- Checks only that `id` is non-empty (using `StringUtils.isEmpty`).
- No numeric/integer format check.
- No maximum-length check.
- No character whitelist or injection character rejection.

### 1.4 `reset()` Details

Neither `AdminFleetcheckShowActionForm` nor `ValidateIdExistsAbstractActionForm` overrides `reset()`. The Struts default `reset()` on `ActionForm` is a no-op — it does **not** clear fields between requests. `id` therefore retains its previous value if the parameter is absent from the request.

### 1.5 `validation.xml` Rules

File: `src/main/webapp/WEB-INF/validation.xml`

The file defines three form entries:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

**`adminFleetcheckShowActionForm` is absent from `validation.xml`.** No Commons Validator rules apply to this form.

### 1.6 Associated Action

File: `src/main/java/com/action/AdminFleetcheckShowAction.java`

```java
public ActionForward execute(ActionMapping mapping, ActionForm actionForm,
                             HttpServletRequest request, HttpServletResponse response)
        throws Exception {
    AdminFleetcheckShowActionForm adminFleetcheckActionForm =
        (AdminFleetcheckShowActionForm) actionForm;
    QuestionDAO.showQuestionById(adminFleetcheckActionForm.getId());
    PrintWriter writer = response.getWriter();
    writer.write("true");
    writer.flush();
    return null;
}
```

The raw string `id` is passed directly to `QuestionDAO.showQuestionById()`.

### 1.7 DAO Call Chain

`QuestionDAO.showQuestionById(String id)` (lines 210–214) calls `getQuestionById(id)` and then `updateQuestionInfo(question)`.

`getQuestionById` (lines 263–308) executes:

```java
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id," +
             "attachment_id,answer_type,comp_id, active from question where id = " + id;
stmt.executeQuery(sql);
```

The `id` value is concatenated directly into the SQL string — **no parameterization**.

`updateQuestionInfo` (lines 516–553) uses a `PreparedStatement` with parameterized binding — safe.

### 1.8 Authorization Layer

`web.xml` registers `PreFlightActionServlet`. Its `doGet` calls `excludeFromFilter(path)`. The path `/fleetcheckshow.do` is **not** in the exclusion list, so the session check (`sessCompId` attribute) is applied. However:

- The servlet checks only that a session exists and that `sessCompId` is non-null/non-empty.
- It does **not** verify that the `question` record being acted upon belongs to the authenticated company. No ownership check exists in `AdminFleetcheckShowAction` or `QuestionDAO.showQuestionById`.

---

## 2. Findings

---

### FINDING-01

**Severity:** CRITICAL
**Category:** SQL Injection
**File:** `src/main/java/com/dao/QuestionDAO.java`
**Line:** 275
**Trigger path:** HTTP POST `id` parameter → `AdminFleetcheckShowActionForm.id` → `QuestionDAO.showQuestionById()` → `QuestionDAO.getQuestionById()`

**Description:**
The `id` value received from the HTTP request is concatenated verbatim into a SQL `SELECT` query without parameterization. An authenticated attacker can inject arbitrary SQL, enabling data exfiltration, modification, or denial-of-service against the underlying database.

**Evidence:**
```java
// QuestionDAO.java line 275
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id," +
             "attachment_id,answer_type,comp_id, active from question where id = " + id;
stmt.executeQuery(sql);
```
The `validate()` method (inherited) checks only that `id` is non-empty; it imposes no integer constraint and does not reject SQL metacharacters. Example payload: `1 UNION SELECT username,password,null,null,null,null,null,null,null,null,null FROM admin_users--`.

**Recommendation:**
Replace the `Statement`/string-concatenation pattern with a `PreparedStatement` and bind `id` as a typed parameter (`ps.setLong(1, Long.parseLong(id))`). Apply the same fix to all other concatenated SQL statements in `QuestionDAO` (`getQuesLanId` line 42, `getQuestionByUnitId` lines 83–89, `delQuestionById` line 183, `getQuestionContentById` lines 328/330).

---

### FINDING-02

**Severity:** HIGH
**Category:** Insecure Direct Object Reference (IDOR) / Missing Ownership Check
**File:** `src/main/java/com/action/AdminFleetcheckShowAction.java`
**Lines:** 19–20
**Supporting file:** `src/main/java/com/dao/QuestionDAO.java` lines 210–213

**Description:**
`AdminFleetcheckShowAction` passes the caller-supplied `id` directly to `QuestionDAO.showQuestionById()` without verifying that the question record belongs to the authenticated company (`sessCompId`). Any authenticated admin session can mark any question record as active regardless of tenancy.

**Evidence:**
```java
// AdminFleetcheckShowAction.java lines 19-20
AdminFleetcheckShowActionForm adminFleetcheckActionForm =
    (AdminFleetcheckShowActionForm) actionForm;
QuestionDAO.showQuestionById(adminFleetcheckActionForm.getId());
```
```java
// QuestionDAO.java lines 210-214
public static void showQuestionById(String id) throws Exception {
    QuestionBean question = QuestionDAO.getQuestionById(id).get(0);
    question.setActive("t");
    QuestionDAO.updateQuestionInfo(question);
}
```
No `comp_id` comparison between `session.getAttribute("sessCompId")` and `question.getComp_id()` is performed anywhere in the chain.

**Recommendation:**
After retrieving the `QuestionBean`, assert that `question.getComp_id()` equals the session `sessCompId` (or is `null` for global system questions that are intentionally shared). Return an authorization error if the check fails. Pass `sessCompId` into `showQuestionById` and enforce the comparison inside the DAO or service layer.

---

### FINDING-03

**Severity:** HIGH
**Category:** Input Validation — Missing Numeric Type Check
**File:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`
**Lines:** 18–27
**Also relevant:** `src/main/java/com/actionform/AdminFleetcheckShowActionForm.java` (inherits without override)

**Description:**
The inherited `validate()` method confirms only that `id` is non-empty. It does not verify that the value is a positive integer. Non-numeric values cause an unhandled exception in `getQuestionById` when the value is injected into the SQL string (leading directly to FINDING-01) and would also cause a `NumberFormatException` in any `Long.parseLong` call downstream. There is no Commons Validator rule for this form in `validation.xml` to compensate.

**Evidence:**
```java
// ValidateIdExistsAbstractActionForm.java lines 22-25
if (StringUtils.isEmpty(this.id)) {
    ActionMessage message = new ActionMessage("error.id");
    errors.add("id", message);
}
```
No integer-format check. No maximum-length constraint. No character blacklist/whitelist.

**Recommendation:**
Add a numeric format check in `validate()` (or override it in `AdminFleetcheckShowActionForm`):
```java
if (!StringUtils.isEmpty(this.id) && !this.id.matches("\\d{1,18}")) {
    errors.add("id", new ActionMessage("error.id.invalid"));
}
```
Alternatively, add a Commons Validator `integer` or `long` rule for `adminFleetcheckShowActionForm` in `validation.xml`.

---

### FINDING-04

**Severity:** MEDIUM
**Category:** CSRF — Structural Gap (framework-level)
**File:** `src/main/webapp/WEB-INF/struts-config.xml`
**Lines:** 402–410

**Description:**
The `/fleetcheckshow` action performs a state-changing operation (setting a question's `active` flag to `true`) but Apache Struts 1.3.10 provides no built-in CSRF token mechanism. There is no synchronizer token check (`saveToken` / `isTokenValid`) in `AdminFleetcheckShowAction`, and no custom filter provides CSRF protection. An attacker can craft a cross-site request that causes an authenticated admin to unwillingly re-activate any question record (compounded by FINDING-02 which removes tenancy isolation).

**Evidence:**
```xml
<!-- struts-config.xml lines 402-410 -->
<action
    path="/fleetcheckshow"
    name="adminFleetcheckShowActionForm"
    scope="request"
    validate="true"
    type="com.action.AdminFleetcheckShowAction"
    input="adminChecklistDefinition">
    <forward name="success" path="adminChecklistDefinition"/>
</action>
```
`web.xml` contains only a `CharsetEncodingFilter`; no CSRF filter is present.

**Recommendation:**
Implement the Struts 1 synchronizer token pattern: call `saveToken(request)` when rendering the form and `isTokenValid(request, true)` at the start of `AdminFleetcheckShowAction.execute()`. Alternatively, introduce a servlet filter that validates a double-submit cookie or a custom header (`X-Requested-With`) for all state-mutating `.do` endpoints.

---

### FINDING-05

**Severity:** MEDIUM
**Category:** Missing `reset()` Implementation
**File:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`
**Lines:** 15–28
**Also relevant:** `src/main/java/com/actionform/AdminFleetcheckShowActionForm.java`

**Description:**
Neither `ValidateIdExistsAbstractActionForm` nor `AdminFleetcheckShowActionForm` overrides `reset()`. In Struts 1, when a form bean is scoped to `session` (or when a request omits the `id` parameter for any reason), the previous value of `id` persists. Although the current struts-config scopes this form to `request`, the omission is a latent defect: if the scope is ever changed or if the bean is reused in another mapping, stale `id` values could silently be re-used, triggering unintended mutations.

**Evidence:**
No `reset()` method in either class. `struts-config.xml` line 405: `scope="request"` (currently safe, but the absence of `reset()` is a code-quality and forward-compatibility concern).

**Recommendation:**
Add an explicit `reset()` override in `ValidateIdExistsAbstractActionForm` that sets `this.id = null`. This is defensive practice for all subclasses and is aligned with the Struts 1 ActionForm contract.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Unhandled IndexOutOfBoundsException / Error Handling
**File:** `src/main/java/com/dao/QuestionDAO.java`
**Line:** 211

**Description:**
`showQuestionById` calls `getQuestionById(id).get(0)` without checking whether the returned list is empty. If no row matches the supplied `id`, the method throws an `IndexOutOfBoundsException`. This exception propagates through `AdminFleetcheckShowAction.execute()` (which declares `throws Exception`) and is caught by the global error page in `web.xml`. The error page may expose stack trace information to the client, and the uncontrolled exception path bypasses proper error signalling to the caller.

**Evidence:**
```java
// QuestionDAO.java line 211
QuestionBean question = QuestionDAO.getQuestionById(id).get(0);
```
No null/empty-list guard precedes `.get(0)`.

**Recommendation:**
Check the list size before accessing index 0 and throw a meaningful, application-defined exception (e.g., `EntityNotFoundException`) so the Action layer can return a proper user-facing error rather than relying on the generic error page. Ensure the global error page does not expose stack traces in production.

---

### FINDING-07

**Severity:** LOW
**Category:** Missing `validation.xml` Coverage
**File:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
`adminFleetcheckShowActionForm` is not registered in `validation.xml`. While the form's `validate()` method is invoked (struts-config has `validate="true"`), the absence of a declarative Commons Validator entry means no framework-level rules (type checking, length limits, pattern matching) are enforced via the standard validation pipeline for this form. This is consistent with the known structural gap that validation.xml covers only 3 forms across the application.

**Evidence:**
`validation.xml` contains entries for `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm` only. `adminFleetcheckShowActionForm` is absent.

**Recommendation:**
Add a `<form name="adminFleetcheckShowActionForm">` entry with at least a `required` and `integer` (or `long`) rule on the `id` field. This provides a defence-in-depth layer independent of the programmatic `validate()`.

---

## 3. Category Summary

| Category | Outcome |
|----------|---------|
| Input Validation | ISSUES FOUND — FINDING-01, FINDING-03, FINDING-07 |
| Type Safety | ISSUES FOUND — FINDING-03 (no numeric type enforcement on `id`) |
| IDOR Risk | ISSUES FOUND — FINDING-02 |
| Sensitive Fields | NO ISSUES — the sole field `id` is a reference key, not a credential or PII value |
| Data Integrity | ISSUES FOUND — FINDING-05 (missing `reset()`), FINDING-06 (unchecked `.get(0)`) |
| CSRF | ISSUES FOUND — FINDING-04 (structural gap, no token) |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | FINDING-01 |
| HIGH | 2 | FINDING-02, FINDING-03 |
| MEDIUM | 3 | FINDING-04, FINDING-05, FINDING-06 |
| LOW | 1 | FINDING-07 |
| INFO | 0 | — |
| **TOTAL** | **7** | |
