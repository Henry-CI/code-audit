# Security Audit Report: AdminFleetcheckShowAction

**Audit run:** audit/2026-02-26-01
**Branch:** master
**Auditor:** Claude Sonnet 4.6 (automated pass 1)
**Date:** 2026-02-26

---

## 1. Reading Evidence

### 1.1 Package and Class

| Item | Value |
|------|-------|
| Package | `com.action` |
| Class | `AdminFleetcheckShowAction` |
| File | `src/main/java/com/action/AdminFleetcheckShowAction.java` |
| Superclass | `org.apache.struts.action.Action` |

### 1.2 Public / Protected Methods

| Line | Visibility | Signature |
|------|-----------|-----------|
| 16 | `public` | `execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

No other public or protected methods are declared in this class.

### 1.3 DAOs / Services Called

| Call Site (action, line) | DAO / Static Method | Transitively Calls |
|--------------------------|--------------------|--------------------|
| `AdminFleetcheckShowAction.java:20` | `QuestionDAO.showQuestionById(String id)` | `QuestionDAO.getQuestionById(String id)` (line 211 in DAO) then `QuestionDAO.updateQuestionInfo(QuestionBean)` (line 213 in DAO) |

**`QuestionDAO.getQuestionById` (DAO lines 263-308):** executes a raw-concatenated SQL SELECT:
```java
String sql = "select id,content,... from question where id = " + id;
stmt.executeQuery(sql);
```

**`QuestionDAO.updateQuestionInfo` (DAO lines 516-553):** uses a `PreparedStatement` — parameterized, safe.

### 1.4 Form Class

| Item | Value |
|------|-------|
| Form class | `com.actionform.AdminFleetcheckShowActionForm` |
| File | `src/main/java/com/actionform/AdminFleetcheckShowActionForm.java` |
| Superclass | `com.actionform.ValidateIdExistsAbstractActionForm` |
| Field exposed | `protected String id` (via Lombok `@Getter`/`@Setter` on the abstract parent) |
| Validation logic | `ValidateIdExistsAbstractActionForm.validate()` — rejects empty/null `id`; performs NO type or format check |

### 1.5 Struts-Config Mapping

Source: `src/main/webapp/WEB-INF/struts-config.xml`, lines 403-410.

```xml
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

| Attribute | Value | Security Implication |
|-----------|-------|----------------------|
| `path` | `/fleetcheckshow` | Action is reachable at `fleetcheckshow.do` |
| `scope` | `request` | Form is request-scoped — correct |
| `validate` | `true` | Struts validator is invoked before `execute` |
| `roles` | **not set** | No declarative role restriction |
| `input` | `adminChecklistDefinition` | Validation failure redirects to checklist page |

**validation.xml coverage:** `adminFleetcheckShowActionForm` has **no entry** in `WEB-INF/validation.xml`. The only validation executed is the code-level `required` check on `id` inside `ValidateIdExistsAbstractActionForm.validate()`.

---

## 2. Findings

---

### FINDING-01

**Severity:** CRITICAL
**Category:** SQL Injection
**File:** `src/main/java/com/dao/QuestionDAO.java`, line 275
**Triggered by:** `AdminFleetcheckShowAction.java`, line 20

#### Description

`QuestionDAO.getQuestionById(String id)` constructs a SQL query by directly concatenating the caller-supplied `id` parameter with no sanitisation:

```java
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id," +
             "fule_type_id,attachment_id,answer_type,comp_id, active " +
             "from question where id = " + id;
stmt.executeQuery(sql);
```

The `id` value originates from the HTTP request parameter `id` bound into `AdminFleetcheckShowActionForm` and is passed, unmodified, as a `String` directly into this query. The only pre-condition is that `id` is non-empty (from `ValidateIdExistsAbstractActionForm`). Any non-empty string is accepted, including SQL metacharacters.

An attacker can inject arbitrary SQL into the `WHERE` clause. Because `getQuestionById` is called inside `showQuestionById`, which also calls `updateQuestionInfo`, the injection point is exercised on every normal invocation of this action. A UNION-based injection can exfiltrate arbitrary tables; a stacked-query attack (depending on the JDBC driver and database) could execute DML or DDL.

#### Evidence

- `AdminFleetcheckShowAction.java:20` — `QuestionDAO.showQuestionById(adminFleetcheckActionForm.getId())`
- `QuestionDAO.java:210-213` — `showQuestionById` calls `getQuestionById(id)` directly
- `QuestionDAO.java:275` — `"... where id = " + id` via a raw `Statement`, not a `PreparedStatement`
- `ValidateIdExistsAbstractActionForm.java:22` — only checks `StringUtils.isEmpty(this.id)`; no integer constraint

#### Recommendation

Replace the raw `Statement` in `getQuestionById` with a `PreparedStatement`:

```java
String sql = "select ... from question where id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setInt(1, Integer.parseInt(id));
```

Additionally, enforce an integer type-check in `ValidateIdExistsAbstractActionForm.validate()` so that non-numeric values are rejected at the form layer before reaching the DAO. The same pattern should be applied to all other concatenation-based queries found elsewhere in `QuestionDAO` (e.g., `getQuesLanId` line 42, `getQuestionByUnitId` lines 83-89, `delQuestionById` line 183, `getQuestionContentById` lines 328/330).

---

### FINDING-02

**Severity:** HIGH
**Category:** Insecure Direct Object Reference (IDOR) / Missing Ownership Check
**File:** `src/main/java/com/action/AdminFleetcheckShowAction.java`, lines 19-20
**DAO:** `src/main/java/com/dao/QuestionDAO.java`, lines 210-213

#### Description

The action accepts a question `id` from the HTTP request and immediately marks that question as active (`active = 't'`) without verifying that the question belongs to the company of the authenticated session user.

`showQuestionById` fetches any row from the `question` table whose primary key matches the submitted `id`, then updates its `active` flag to `true` unconditionally. The session attribute `sessCompId` (available in the `HttpSession`) is never read inside the action or passed to the DAO. An authenticated admin from company A can therefore mark questions belonging to company B (or global questions outside their tenancy) as visible/active by submitting the correct `id`.

The `question` table has a `comp_id` column (retrieved in `getQuestionById`), which is available on the returned `QuestionBean`, but neither the action nor `showQuestionById` compares this value against the session company ID.

#### Evidence

- `AdminFleetcheckShowAction.java:19-20` — form `id` is passed directly to DAO; session is never consulted
- `QuestionDAO.java:210-213` — no WHERE clause filtering on `comp_id` during the show operation
- `QuestionDAO.java:275` — `getQuestionById` retrieves `comp_id` but only to populate the bean, not to enforce tenancy
- `PreFlightActionServlet.java:56` — `sessCompId` is set in session but is never forwarded to this DAO chain

#### Recommendation

After retrieving the `QuestionBean`, compare `question.getComp_id()` against the session's `sessCompId`. If the IDs do not match and the question is not a globally shared question (`comp_id IS NULL`), abort the operation and return an authorization error. This check should mirror the pattern already partially implemented in `hideQuestionById` (DAO lines 197-208), although that method also lacks a cross-tenant ownership check and should be fixed simultaneously.

---

### FINDING-03

**Severity:** HIGH
**Category:** Authentication — No Role Check
**File:** `src/main/java/com/action/AdminFleetcheckShowAction.java`, line 16
**Config:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 403-410

#### Description

The Struts mapping for `/fleetcheckshow` declares no `roles` attribute. The only authentication gate is the `PreFlightActionServlet`, which checks that `sessCompId` is non-null — i.e., any logged-in user of any role (admin, operator, driver) who can obtain a valid session can invoke this action and activate any question record. There is no programmatic role check inside `AdminFleetcheckShowAction.execute()`.

The action path prefix and name ("Admin...") imply it is intended exclusively for administrators, but this intent is not enforced.

#### Evidence

- `struts-config.xml:403-410` — no `roles` attribute on the `/fleetcheckshow` action mapping
- `AdminFleetcheckShowAction.java:16-26` — `execute()` performs no `session.getAttribute("sessRole")` or equivalent check
- `PreFlightActionServlet.java:56` — checks only `sessCompId != null`; no role validation in the pre-flight gate

#### Recommendation

Add a role check at the top of `execute()`, verifying that the session attribute representing admin privilege is set before proceeding. Where possible, also add a `roles` attribute to the Struts mapping (requires a supporting security realm). Consult the role checks applied in other admin actions in the codebase as a reference pattern.

---

### FINDING-04

**Severity:** HIGH
**Category:** CSRF — No Token Protection
**File:** `src/main/java/com/action/AdminFleetcheckShowAction.java`, line 16
**Config:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 403-410

#### Description

This action performs a state-changing database write (it sets `question.active = true`) but carries no CSRF token. The application uses Apache Struts 1.3.10, which has no built-in CSRF protection, no Spring Security, and no custom token filter is evident in the pre-flight servlet. An attacker can craft a page that causes an authenticated administrator's browser to submit `fleetcheckshow.do?id=<N>` via a GET or POST request, silently activating arbitrary question records.

Because `doPost` delegates to `doGet` in `PreFlightActionServlet` and the Struts mapping accepts both methods by default, there is no HTTP-verb restriction to reduce the attack surface.

#### Evidence

- `AdminFleetcheckShowAction.java:16-26` — no CSRF token read or validated
- `PreFlightActionServlet.java:94-96` — `doPost` delegates to `doGet`; no token check anywhere in the servlet
- `struts-config.xml:403-410` — no reference to any CSRF plug-in or token interceptor
- Stack description confirms "CSRF = structural gap" with no mitigating control identified

#### Recommendation

Implement synchroniser-token CSRF protection across all state-changing actions. A practical approach for Struts 1.x is to use the `saveToken` / `isTokenValid` pair from `org.apache.struts.action.Action` (already available in the superclass) or to introduce a servlet filter that validates a per-session nonce on every non-idempotent request. All admin write actions should be remediated together.

---

### FINDING-05

**Severity:** MEDIUM
**Category:** Input Validation — No Type Enforcement on `id`
**File:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`, lines 22-25
**Referenced by:** `src/main/java/com/actionform/AdminFleetcheckShowActionForm.java`

#### Description

The form-level `validate()` method checks only that `id` is non-empty. It does not verify that the value is a positive integer. A non-numeric value (e.g., `abc`, `1 OR 1=1`, or a very large number) passes validation and is forwarded to the DAO, where it triggers either a SQL injection exploit (see FINDING-01) or an unhandled `NumberFormatException` if any downstream caller attempts `Integer.parseInt(id)`. There is also no upper-bound check, so absurdly large numeric strings are accepted.

Additionally, `adminFleetcheckShowActionForm` has no entry in `WEB-INF/validation.xml`, meaning no declarative XML validation rules are applied at all; validation is entirely dependent on the abstract parent's minimal check.

#### Evidence

- `ValidateIdExistsAbstractActionForm.java:22` — `if (StringUtils.isEmpty(this.id))` is the sole constraint
- `validation.xml` (full file reviewed) — no `<form name="adminFleetcheckShowActionForm">` block
- `QuestionDAO.java:275` — `id` used in string concatenation without `Integer.parseInt` guard

#### Recommendation

Extend `ValidateIdExistsAbstractActionForm.validate()` to enforce that `id` matches `\d+` (digits only) and is within a reasonable positive integer range. Add a corresponding `<form name="adminFleetcheckShowActionForm">` entry to `validation.xml` with an `integer` or `mask` rule as a defence-in-depth measure.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Data Exposure — Unbounded Return Payload from `getQuestionById`
**File:** `src/main/java/com/dao/QuestionDAO.java`, lines 263-308
**Triggered by:** `AdminFleetcheckShowAction.java`, line 20

#### Description

`getQuestionById` returns an `ArrayList<QuestionBean>` containing every column from the `question` table for the matched row, including `comp_id`, `type_id`, `manu_id`, `fule_type_id`, `attachment_id`, `answer_type`, and `copied_from_id`. Although the action itself only uses the first element to set `active` and writes a plain `"true"` response to the client, the full bean is materialised in memory and logged (the SQL string including the raw `id` value is written to the application log at INFO level — `log.info(sql)` on line 276).

If `id` is user-controlled and malicious (see FINDING-01), the logged SQL will contain the injected payload, potentially facilitating log-injection or polluting audit trails.

Additionally, the action writes the literal string `"true"` directly to the `HttpServletResponse` writer (lines 22-24) without setting a `Content-Type` header, leaving the MIME type unspecified. Browsers may sniff the content type, which is a minor concern given the trivial payload.

#### Evidence

- `QuestionDAO.java:276` — `log.info(sql)` logs the concatenated SQL including user-supplied `id`
- `AdminFleetcheckShowAction.java:22-24` — `response.getWriter().write("true")` with no `response.setContentType()`

#### Recommendation

Set `response.setContentType("application/json; charset=UTF-8")` (or `text/plain`) before writing the response. Sanitise or avoid logging user-supplied values in SQL strings; use parameterised queries (resolving FINDING-01 will also mitigate the log-injection vector here).

---

### FINDING-07

**Severity:** LOW
**Category:** Session Handling — Return Value Discarded, No Redirect-After-Write
**File:** `src/main/java/com/action/AdminFleetcheckShowAction.java`, lines 20-25

#### Description

The action returns `null` from `execute()` after writing directly to the response. Returning `null` in Struts 1 signals that the action has handled the response itself. This is a deliberate AJAX pattern, but it bypasses Struts lifecycle hooks (including any configured `ActionForward` post-processing). The `success` forward declared in struts-config is therefore dead code and creates confusion.

More importantly, since the action is a state-changing operation (it persists a DB change), the standard Post/Redirect/Get pattern is not followed, making the browser re-submittable via refresh (though the AJAX context reduces practical risk).

The return value of `QuestionDAO.showQuestionById` is `void`; any exception from `updateQuestionInfo` returning `false` (DAO line 539) is silently swallowed at the `showQuestionById` level — the action always writes `"true"` regardless of whether the DB update actually succeeded.

#### Evidence

- `AdminFleetcheckShowAction.java:20` — result of `showQuestionById` is not captured (void return)
- `AdminFleetcheckShowAction.java:23` — `writer.write("true")` is unconditional
- `QuestionDAO.java:516-553` — `updateQuestionInfo` returns `boolean` indicating success/failure, but `showQuestionById` (line 213) calls it without checking the return value

#### Recommendation

Check the return value of `updateQuestionInfo` inside `showQuestionById` and propagate failure back to the action. The action should write `"false"` (or an error status) to the response if the update did not affect any rows. Remove the dead `success` forward from struts-config or convert the action to a proper redirect pattern if AJAX usage is not required.

---

## 3. Category Summary

| Category | Findings | Max Severity |
|----------|----------|--------------|
| Authentication | FINDING-03 | HIGH |
| CSRF | FINDING-04 | HIGH |
| Input Validation | FINDING-05 | MEDIUM |
| SQL Injection | FINDING-01 | CRITICAL |
| IDOR | FINDING-02 | HIGH |
| Session Handling | FINDING-07 | LOW |
| Data Exposure | FINDING-06 | MEDIUM |

**Categories with NO issues:** None — all seven audit categories have at least one finding.

---

## 4. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH | 3 |
| MEDIUM | 2 |
| LOW | 1 |
| INFO | 0 |
| **Total** | **7** |
