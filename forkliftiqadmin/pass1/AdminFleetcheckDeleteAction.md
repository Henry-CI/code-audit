# Security Audit Report: AdminFleetcheckDeleteAction

**Audit run:** audit/2026-02-26-01
**Auditor:** CIG Automated Pass 1
**Date:** 2026-02-26
**Repository:** forkliftiqadmin (branch: master)

---

## 1. Reading Evidence

### 1.1 Package and Class Name

| Item | Value |
|---|---|
| Package | `com.action` |
| Class | `AdminFleetcheckDeleteAction` |
| Superclass | `org.apache.struts.action.Action` |
| Source file | `src/main/java/com/action/AdminFleetcheckDeleteAction.java` |

### 1.2 Public / Protected Methods

| Line | Modifier | Signature |
|---|---|---|
| 15 | `public` (override) | `execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

No other methods are declared in the class. The class body is 23 lines total.

### 1.3 DAOs / Services Called

| Call site (Action file line) | DAO / method | DAO file | DAO line |
|---|---|---|---|
| Line 20 | `QuestionDAO.delQuestionById(id)` | `src/main/java/com/dao/QuestionDAO.java` | 174 |

`delQuestionById` is a `public static` method that builds a raw SQL DELETE string via string concatenation and executes it with `Statement.executeUpdate()`.

```java
// QuestionDAO.java line 183
String sql = "delete from question where id=" + id;
stmt.executeUpdate(sql);
```

### 1.4 Form Class Used

| Item | Value |
|---|---|
| Form class | `com.actionform.AdminFleetcheckDeleteActionForm` |
| Source file | `src/main/java/com/actionform/AdminFleetcheckDeleteActionForm.java` |
| Superclass | `com.actionform.ValidateIdExistsAbstractActionForm` |

`AdminFleetcheckDeleteActionForm` is an empty subclass; all logic is in the abstract parent which exposes a single `String id` field (Lombok `@Getter`/`@Setter`). The parent `validate()` method checks only that `id` is non-empty (null/blank check via `StringUtils.isEmpty`). No format, type, or range constraints are applied.

### 1.5 struts-config.xml Mapping Details

File: `src/main/webapp/WEB-INF/struts-config.xml` lines 420–428.

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

| Attribute | Value |
|---|---|
| URL path | `/fleetcheckdelete.do` |
| Form bean | `adminFleetcheckDeleteActionForm` |
| Scope | `request` |
| `validate` | `true` (parent `validate()` called; only checks non-blank) |
| `input` | `adminChecklistDefinition` (redirect target on validation failure) |
| Forwards | `success` → `adminChecklistDefinition` |
| HTTP method restriction | None declared; both GET and POST accepted |

---

## 2. Audit Findings

---

### FINDING-01

**Severity:** CRITICAL
**Category:** Insecure Direct Object Reference (IDOR) / Missing Ownership Verification
**File:** `src/main/java/com/action/AdminFleetcheckDeleteAction.java`
**Line:** 20

**Description:**
The action accepts an arbitrary `id` value from the HTTP request and immediately passes it to `QuestionDAO.delQuestionById()` without any check that the question record identified by that ID belongs to the company of the currently authenticated session (`sessCompId`). Any authenticated admin-level session from Company A can delete checklist questions belonging to Company B, or global system questions, by supplying an arbitrary numeric ID.

**Evidence:**

```java
// AdminFleetcheckDeleteAction.java lines 19-21
AdminFleetcheckDeleteActionForm adminFleetcheckDeleteActionForm =
        (AdminFleetcheckDeleteActionForm) actionForm;
QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId());
return null;
```

The session attribute `sessCompId` is never read inside this action. `QuestionDAO.getQuestionById()` (which includes a `comp_id` column) exists in the DAO but is not called here to compare ownership before deletion. The `question` table contains rows with `comp_id = NULL` (global/system questions) and rows scoped to specific companies; both are equally vulnerable.

**Recommendation:**
Before calling `delQuestionById`, retrieve the question record with `QuestionDAO.getQuestionById(id)` and compare `questionBean.getComp_id()` against `session.getAttribute("sessCompId")`. If they do not match, or if `comp_id` is null (global record), abort with an authorisation error and log the attempt. Delete must only be permitted for records owned by the caller's company.

---

### FINDING-02

**Severity:** CRITICAL
**Category:** SQL Injection
**File:** `src/main/java/com/dao/QuestionDAO.java`
**Line:** 183

**Description:**
`delQuestionById` builds the DELETE statement by direct string concatenation of the caller-supplied `id` value, then executes it with an unparameterised `Statement`. Although the Struts `validate()` in the abstract form class confirms the value is non-blank, it imposes no integer or format constraint. A value such as `1 OR 1=1` would produce `DELETE FROM question WHERE id=1 OR 1=1`, wiping the entire `question` table. More sophisticated payloads (stacked queries, if the JDBC driver permits them) could extend the impact further.

**Evidence:**

```java
// QuestionDAO.java lines 182-185
String sql = "delete from question where id=" + id;
log.info(sql);           // raw SQL also logged — secondary information-disclosure risk
stmt.executeUpdate(sql);
```

The `id` originates from the HTTP request parameter, flows through the form bean's unvalidated `String id` field, and arrives here without any sanitisation.

**Recommendation:**
Replace the `Statement` with a `PreparedStatement`:

```java
// Illustrative fix pattern (do not alter production code without change-control approval)
String sql = "DELETE FROM question WHERE id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setLong(1, Long.parseLong(id));   // parse first to guarantee numeric
ps.executeUpdate();
```

Parse `id` to `long` before binding; throw `IllegalArgumentException` if parsing fails so the action can reject the request before hitting the database.

---

### FINDING-03

**Severity:** HIGH
**Category:** Input Validation — Insufficient Type and Range Constraint
**File:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`
**Line:** 22
**Also relevant:** `src/main/webapp/WEB-INF/validation.xml` (no entry for `adminFleetcheckDeleteActionForm`)

**Description:**
The `validate()` method in `ValidateIdExistsAbstractActionForm` only rejects a null or blank `id`. It does not assert that the value is a positive integer. Non-numeric strings, negative numbers, floating-point values, and SQL metacharacters all pass validation and are forwarded to the DAO. Combined with the SQL injection finding above (FINDING-02), this makes exploitation trivially easy. Additionally, `adminFleetcheckDeleteActionForm` has no entry in `validation.xml`, so declarative Struts validator rules provide no supplementary protection.

**Evidence:**

```java
// ValidateIdExistsAbstractActionForm.java lines 21-26
if (StringUtils.isEmpty(this.id)) {
    ActionMessage message = new ActionMessage("error.id");
    errors.add("id", message);
}
```

Only emptiness is checked. Validation.xml contains entries only for `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm` — `adminFleetcheckDeleteActionForm` is absent.

**Recommendation:**
Add a numeric/positive-integer assertion to `ValidateIdExistsAbstractActionForm.validate()`:

```java
if (!this.id.matches("^[1-9][0-9]*$")) {
    errors.add("id", new ActionMessage("error.id.invalid"));
}
```

Alternatively, add a declarative `integer` and `intRange` rule for `adminFleetcheckDeleteActionForm` in `validation.xml`.

---

### FINDING-04

**Severity:** HIGH
**Category:** CSRF — No Token Protection on Destructive State-Changing Action
**File:** `src/main/webapp/WEB-INF/struts-config.xml`
**Line:** 421–428
**Also relevant:** `src/main/java/com/action/AdminFleetcheckDeleteAction.java` line 15

**Description:**
The `/fleetcheckdelete.do` endpoint is a state-changing (DELETE) action with no CSRF token mechanism. The stack note confirms there is no Spring Security CSRF filter. Struts 1.3.10 does not include built-in CSRF protection. The action accepts both GET and POST (no method restriction is configured in the mapping; `PreFlightActionServlet.doPost` calls `doGet` which calls `super.doGet`, so both verbs are processed identically). An attacker who can induce an authenticated admin to load a crafted page or click a link can trigger deletion of arbitrary questions.

**Evidence:**
- No CSRF token is read from the session or request in `AdminFleetcheckDeleteAction.execute()`.
- struts-config.xml mapping specifies no HTTP method restriction.
- `PreFlightActionServlet.doPost` delegates directly to `doGet` (line 95 of `PreFlightActionServlet.java`), making both verbs equivalent.
- The only parameter required is a non-blank `id` — trivially guessable or enumerable given FINDING-01.

**Recommendation:**
Implement a synchroniser-token pattern. On each admin page that submits this action, embed a per-session or per-form random token as a hidden field. In the action (or a shared base class / filter), verify that the submitted token matches the session-stored value before proceeding. Reject the request if it is absent or mismatched.

---

### FINDING-05

**Severity:** HIGH
**Category:** Authentication — Missing Role / Privilege Check Inside the Action
**File:** `src/main/java/com/action/AdminFleetcheckDeleteAction.java`
**Line:** 15–22

**Description:**
Authentication at the servlet-filter level only confirms that `sessCompId` is non-null (i.e., the user is logged in as some company principal). There is no role or privilege check inside the action. The action does not verify that the authenticated principal holds an admin role, a checklist-management permission, or any other authorisation attribute. Any session with a valid `sessCompId` — including lower-privilege roles if they exist — can invoke this endpoint.

**Evidence:**

```java
// AdminFleetcheckDeleteAction.java lines 15-22 — entire execute() method
public ActionForward execute(ActionMapping mapping, ActionForm actionForm,
                             HttpServletRequest request, HttpServletResponse response)
        throws Exception {
    AdminFleetcheckDeleteActionForm adminFleetcheckDeleteActionForm =
            (AdminFleetcheckDeleteActionForm) actionForm;
    QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId());
    return null;
}
```

No `session.getAttribute(...)` call for role, permission, or user-type attributes is present.

**Recommendation:**
Add an explicit authorisation check at the start of `execute()`. Retrieve the session role attribute (e.g., `sessRole` or equivalent) and verify the principal holds the admin or checklist-management privilege. Return an error forward (or throw an authorisation exception) if the check fails.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Session Handling — Action Returns `null` on Success
**File:** `src/main/java/com/action/AdminFleetcheckDeleteAction.java`
**Line:** 21

**Description:**
`execute()` returns `null` unconditionally after the deletion. In Struts 1, returning `null` instructs the framework to perform no further forwarding; response writing is left entirely to whatever the action (or the container) has written. No response is written here, so the behaviour is a blank HTTP 200 with an empty body. The nominal `success` forward defined in struts-config.xml is never used. This means:

1. The caller receives no confirmation that the delete succeeded or failed.
2. If an exception is thrown by the DAO (including from a SQL injection attempt that causes a syntax error), the global exception handler (`java.sql.SQLException` → `errorDefinition`) will take over — revealing to the client that a database error occurred.

**Evidence:**

```java
// Line 21
return null;
```

The `success` forward at struts-config.xml line 427 (`path="adminChecklistDefinition"`) is unreachable.

**Recommendation:**
Return an explicit `ActionForward` on both success and failure paths. On success, redirect to `adminChecklistDefinition`. On failure, handle the exception inside the action, log it server-side, and return a safe error forward rather than propagating a raw `SQLException` to the global handler.

---

### FINDING-07

**Severity:** MEDIUM
**Category:** Data Exposure — Raw SQL Logged at INFO Level
**File:** `src/main/java/com/dao/QuestionDAO.java`
**Line:** 184

**Description:**
`delQuestionById` logs the fully assembled SQL string — including the unvalidated `id` value — at `INFO` level before execution. If log files are accessible to lower-privilege users, stored in insecure locations, or forwarded to a log aggregator with weak access controls, an attacker can observe the exact SQL being executed, facilitating blind enumeration and confirming injection payloads.

**Evidence:**

```java
// QuestionDAO.java line 184
log.info(sql);   // logs: "delete from question where id=<user-supplied-value>"
```

**Recommendation:**
Once the query is converted to a `PreparedStatement` (see FINDING-02), log the intent and the sanitised ID value rather than the full SQL string. Ensure log access is restricted to operations/security personnel.

---

## 3. Categories with NO Issues

**Session Handling — sessCompId null check:** `PreFlightActionServlet` correctly checks for a non-null, non-empty `sessCompId` before forwarding to any protected action. The `/fleetcheckdelete.do` path is not in the `excludeFromFilter` list, so an unauthenticated request will be redirected to the expiry page. No issue in the gate itself.

---

## 4. Summary Table

| ID | Severity | Category | File | Line |
|---|---|---|---|---|
| FINDING-01 | CRITICAL | IDOR — No ownership verification before delete | `AdminFleetcheckDeleteAction.java` | 20 |
| FINDING-02 | CRITICAL | SQL Injection — string-concatenated DELETE | `QuestionDAO.java` | 183 |
| FINDING-03 | HIGH | Input Validation — no integer/format constraint on `id` | `ValidateIdExistsAbstractActionForm.java` | 22 |
| FINDING-04 | HIGH | CSRF — no token protection on destructive action | `struts-config.xml` / `AdminFleetcheckDeleteAction.java` | 421 / 15 |
| FINDING-05 | HIGH | Authentication — no role/privilege check inside action | `AdminFleetcheckDeleteAction.java` | 15 |
| FINDING-06 | MEDIUM | Session Handling — `null` return, success forward unreachable | `AdminFleetcheckDeleteAction.java` | 21 |
| FINDING-07 | MEDIUM | Data Exposure — raw SQL logged at INFO level | `QuestionDAO.java` | 184 |

**Finding counts by severity:**

| Severity | Count |
|---|---|
| CRITICAL | 2 |
| HIGH | 3 |
| MEDIUM | 2 |
| LOW | 0 |
| INFO | 0 |
| **Total** | **7** |
