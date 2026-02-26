# Security Audit: AdminFleetcheckEditAction.java
**Audit Run:** audit/2026-02-26-01/
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated Pass 1

---

## 1. Reading Evidence

### Package and Class
- **Package:** `com.action`
- **Class:** `AdminFleetcheckEditAction extends org.apache.struts.action.Action`
- **File:** `src/main/java/com/action/AdminFleetcheckEditAction.java`

### Public / Protected Methods

| Line | Visibility | Signature |
|------|-----------|-----------|
| 29 | `public` | `execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |
| 76 | `private` | `update(ActionMapping mapping, HttpServletRequest request, QuestionBean bean, String active, String languageId) throws SQLException` |
| 97 | `private` | `create(ActionMapping mapping, HttpServletRequest request, QuestionBean bean, String languageId) throws SQLException` |
| 107 | `private` | `getFailureForward(ActionMapping mapping, HttpServletRequest request)` |

Note: `update`, `create`, and `getFailureForward` are package-private helper methods; only `execute` is the Struts dispatch entry point.

### DAOs and Services Called

| Call Site (Action line) | DAO / Method | SQL Style |
|-------------------------|--------------|-----------|
| Line 40 | `QuestionDAO.getQuestionById(id)` | String concatenation — **vulnerable** |
| Line 42 | `QuestionDAO.getAllAnswerType()` | Static query — safe |
| Line 54 | `ManufactureDAO.getAllManufactures(sessCompId)` | PreparedStatement — safe |
| Line 81 | `QuestionDAO.updateQuestionInfo(bean)` | PreparedStatement — safe |
| Line 89 | `QuestionDAO.saveQuestionContent(questionContentBean)` | PreparedStatement — safe |
| Lines 91–92 / 100 | `QuestionDAO.getQuestionByCategory(...)` | PreparedStatement — safe |
| Line 99 | `QuestionDAO.saveQuestionInfo(bean, languageId, compId)` | PreparedStatement — safe |

### Form Class
- **Name (struts-config):** `adminFleetcheckEditActionForm`
- **Type:** `com.actionform.AdminFleetcheckEditActionForm`
- **Fields:** `id`, `content`, `expectedanswer`, `order_no` (int), `active`, `type_id`, `fuel_type_id`, `answer_type`, `comp_id`, `manu_id`, `attachment_id`
- All fields are plain Strings (or int) with no built-in constraints.

### Struts-Config Mapping
(`src/main/webapp/WEB-INF/struts-config.xml`, lines 381–390)

```xml
<action
    path="/fleetcheckedit"
    name="adminFleetcheckEditActionForm"
    scope="request"
    validate="true"
    type="com.action.AdminFleetcheckEditAction">
    <forward name="edit"         path="adminChecklistEditDefinition"/>
    <forward name="success"      path="/fleetcheckconf.do"/>
    <forward name="successAdmin" path="adminQestionDefinition"/>
    <forward name="failure"      path="adminChecklistEditDefinition"/>
</action>
```

Key mapping attributes:
- `scope="request"` — form bean is request-scoped (correct)
- `validate="true"` — Struts Validator is invoked before `execute()`
- **No `roles` attribute** — no declarative role enforcement at the framework level
- **No `input` attribute** — if validation fails Struts cannot redirect to an input page; this is a secondary defect but does not affect security directly

---

## 2. Audit Findings

---

### FINDING-01 — CRITICAL: SQL Injection via Unparameterised `id` in GET Handler

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/QuestionDAO.java`
**Triggered from Action:** `AdminFleetcheckEditAction.java` line 40
**DAO line:** 275

**Description:**
On every HTTP GET to `/fleetcheckedit.do`, the action passes the user-supplied form field `id` directly to `QuestionDAO.getQuestionById()`. Inside that DAO method the value is concatenated into a raw SQL string executed with a plain `Statement`, not a `PreparedStatement`:

```java
// QuestionDAO.java line 275
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id," +
             "fule_type_id,attachment_id,answer_type,comp_id, active " +
             "from question where id = " + id;
stmt.executeQuery(sql);
```

An attacker can inject arbitrary SQL by supplying a crafted `id` parameter, e.g.:
```
/fleetcheckedit.do?id=1 UNION SELECT username,password,null,...
```

**Evidence:**
- `AdminFleetcheckEditAction.java` line 40: `QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId())`
- `QuestionDAO.java` line 275: raw string concatenation into `stmt.executeQuery(sql)`
- `AdminFleetcheckEditActionForm.java` line 20: `private String id = null;` — no type or length constraint

**Recommendation:**
Rewrite `QuestionDAO.getQuestionById()` to use a `PreparedStatement` with a `?` parameter. Validate that `id` is a positive integer in the action before it reaches the DAO, rejecting any non-numeric value immediately.

---

### FINDING-02 — HIGH: No CSRF Protection on Write Operations (POST)

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckEditAction.java` (entire POST path, lines 46–73)
**Struts-config:** lines 381–390

**Description:**
Apache Struts 1.3.10 provides no built-in CSRF token mechanism. This action handles both create (`QuestionDAO.saveQuestionInfo`) and update (`QuestionDAO.updateQuestionInfo`) of fleetcheck questions based solely on whether `id` is empty. There is no synchroniser token, double-submit cookie, or `Referer` check anywhere in the action or its form. An attacker who can lure an authenticated admin to a malicious page can forge POST requests that create or modify inspection questions under the victim's `sessCompId`.

**Evidence:**
- No `saveToken()` / `isTokenValid()` calls in `execute()` or any helper method.
- No token field in `AdminFleetcheckEditActionForm`.
- The stack audit context confirms "CSRF = structural gap" across the whole application; this action does not mitigate it locally.

**Recommendation:**
Implement the Struts 1 synchroniser token pattern: call `saveToken(request)` when rendering the edit form (GET branch, line 41–43) and call `isTokenValid(request, true)` at the top of the POST branch before any DAO write. Reject the request with an error if the token is absent or invalid.

---

### FINDING-03 — HIGH: No Ownership Check Before Read or Write — IDOR on Question Records

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckEditAction.java`
**Lines:** 40, 56–67, 81, 89

**Description:**
On GET (line 40) the action fetches a question by the user-supplied `id` without verifying that the returned question belongs to the session company (`sessCompId`). On POST/update (lines 56–67, 81) the `QuestionBean` is built with `comp_id` set to `sessCompId`, but the `UPDATE` statement in `QuestionDAO.updateQuestionInfo` (line 527 of QuestionDAO) filters only on `id`, not on `comp_id`:

```java
// QuestionDAO.java line 527
String sql = "update question set content = ?, expectedanswer = ?, " +
             "answer_type = ?, active = ? where id = ?";
```

This means any authenticated user in any company can overwrite the `content`, `expectedanswer`, `answer_type`, and `active` fields of any question row in the database by supplying a valid numeric `id` belonging to another company or a global question.

**Evidence:**
- Action line 40: `QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId())` — no subsequent ownership assertion.
- Action lines 66–67: `bean.setComp_id(sessCompId)` is set but the field is not part of the UPDATE WHERE clause.
- `QuestionDAO.java` lines 527–536: `where id = ?` only.

**Recommendation:**
After loading the question on GET, assert that `question.getComp_id().equals(sessCompId)` (or that `comp_id` is null for global questions which should be read-only). On UPDATE, add `AND comp_id = ?` to the WHERE clause and bind `sessCompId`, so that a row belonging to another company cannot be modified even if the `id` is known.

---

### FINDING-04 — HIGH: NullPointerException / DoS via Null Session or Empty `arrComp`

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckEditAction.java`
**Lines:** 32–36

**Description:**
The action calls `request.getSession(false)` (correct pattern), but then immediately dereferences the result without a null check on line 33:

```java
HttpSession session = request.getSession(false);   // line 32 — may return null
String sessCompId = session.getAttribute("sessCompId") == null ? ""   // line 33 — NPE if session is null
```

Although `PreFlightActionServlet` is supposed to redirect unauthenticated requests before they reach the action, the auth gate only checks `excludeFromFilter()`. If the servlet filter order, container configuration, or a direct request bypass were ever to allow the request through without a session, the action throws an unhandled `NullPointerException` at line 33 rather than gracefully redirecting.

Similarly, line 36 calls `arrComp.get(0)` without checking whether `arrComp` is null or empty, which would throw a `NullPointerException` or `IndexOutOfBoundsException`.

Additionally, `sessCompId` is assigned an empty string `""` if the session attribute is null (line 33–34), but the application then proceeds to use it in DAO calls (e.g., `ManufactureDAO.getAllManufactures(sessCompId)` at line 54), which would pass an empty string to `Long.valueOf(companyId)` and throw a `NumberFormatException` propagated as an unhandled exception.

**Evidence:**
- Line 32: `request.getSession(false)` — result not null-checked before line 33.
- Line 36: `arrComp.get(0)` — no null/empty-list check on `arrComp`.
- `PreFlightActionServlet.java` line 56: only redirects if `sessCompId == null || ""`; does not prevent action execution if session exists but `arrComp` is missing.

**Recommendation:**
Add an explicit null check for the session object immediately after line 32 and redirect to the expire page. Add a null/empty check on `arrComp` before accessing index 0. Validate that `sessCompId` is a non-empty numeric string before any DAO call.

---

### FINDING-05 — MEDIUM: No Role-Based Access Control on Admin Action

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/struts-config.xml` lines 381–390
**Action:** `AdminFleetcheckEditAction.java`

**Description:**
The struts-config mapping for `/fleetcheckedit` contains no `roles` attribute. Struts 1 supports a `roles` attribute on `<action>` elements that causes the framework to check `HttpServletRequest.isUserInRole()` before dispatching. Without this, any authenticated user — regardless of whether they hold an admin role — can invoke this action and create or modify fleetcheck inspection questions. The sole gate is that `sessCompId` is not null, which is satisfied by any logged-in user of any role.

**Evidence:**
- Struts-config line 381–390: no `roles="..."` attribute on the `/fleetcheckedit` action.
- No role check inside `AdminFleetcheckEditAction.execute()`.
- Stack context: "No Spring Security" — no framework-level role enforcement exists outside the mapping.

**Recommendation:**
Add `roles="ADMIN"` (or the appropriate role constant) to the `<action>` mapping, and ensure the container/`PreFlightActionServlet` populates roles correctly. Additionally, add an explicit role check inside `execute()` as defence-in-depth.

---

### FINDING-06 — MEDIUM: `validate="true"` but No Validation Rules Defined for `adminFleetcheckEditActionForm`

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/validation.xml`
**Struts-config reference:** line 384

**Description:**
The struts-config mapping declares `validate="true"`, meaning the Struts Validator plugin is invoked before `execute()`. However, `validation.xml` defines rules for only three forms: `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`. There is no `<form name="adminFleetcheckEditActionForm">` block. When Struts finds no matching validation form, it silently skips validation and allows the request to proceed with completely unconstrained inputs.

As a result, all fields on `AdminFleetcheckEditActionForm` — including `id`, `content`, `type_id`, `fuel_type_id`, `manu_id`, `attachment_id`, `answer_type`, and `order_no` — receive no declarative validation whatsoever: no required-field checks, no length limits, no type checks (other than `order_no` which is an `int` and will throw a Struts conversion error on non-numeric input, not a clean validation error).

**Evidence:**
- `validation.xml` lines 18–69: only `loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm` are defined.
- Struts-config line 384: `validate="true"` on `/fleetcheckedit`.
- Stack context: "Validation.xml covers only 3 forms."
- `AdminFleetcheckEditActionForm.java`: all fields are plain Strings with no JSR-303 or other annotations.

**Recommendation:**
Add a `<form name="adminFleetcheckEditActionForm">` block to `validation.xml` with at minimum: `id` as optional integer, `content` as required with maxlength, `type_id`/`fuel_type_id`/`manu_id`/`answer_type` as required integers. This also reduces the SQL injection surface for the DAO methods.

---

### FINDING-07 — MEDIUM: Unchecked `Integer.parseInt` Calls Risk Unhandled Exceptions

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminFleetcheckEditAction.java` line 99
**DAO:** `src/main/java/com/dao/QuestionDAO.java` lines 155–161, 389, 395, 399, 409, 533, 536, 574–575

**Description:**
`AdminFleetcheckEditAction.java` line 99 calls `Integer.parseInt(bean.getComp_id())` where `bean.getComp_id()` is `sessCompId` — derived from the session. While `sessCompId` is generally trustworthy, multiple DAO methods also call `Integer.parseInt()` / `Long.parseLong()` on form-derived values (`type_id`, `fuel_type_id`, `manu_id`, `attachment_id`, `answer_type`) that have no validated numeric format. Any non-numeric string input in these fields causes an unhandled `NumberFormatException` that bypasses the `getFailureForward` error path, produces an uncontrolled stack trace response, and may leak internal information.

**Evidence:**
- Action line 99: `Integer.parseInt(bean.getComp_id())`
- `QuestionDAO.java` lines 155–161: `Long.parseLong(manuId)`, `Long.parseLong(typeId)`, etc. on form-sourced values without prior numeric validation.
- No try/catch for `NumberFormatException` in the action or in the DAO public static methods called from this action.

**Recommendation:**
Validate that `type_id`, `fuel_type_id`, `manu_id`, `answer_type`, and `attachment_id` are numeric before calling the DAO. The recommended location is the `validation.xml` form rules (see FINDING-06) combined with an explicit pre-check in `execute()` using `StringUtils.isNumeric()` before building the `QuestionBean`.

---

### FINDING-08 — LOW: Missing `input` Attribute on Struts-Config Mapping

**Severity:** LOW
**File:** `src/main/webapp/WEB-INF/struts-config.xml` lines 381–390

**Description:**
The `/fleetcheckedit` action mapping sets `validate="true"` but does not declare an `input` attribute. In Apache Struts 1 the `input` attribute specifies where to forward the user when validation fails. Without it, Struts 1 throws `NullPointerException` internally (or returns a generic 500 error) when validation does produce errors, rather than re-displaying the form. Although in practice validation currently produces no errors (see FINDING-06), any future addition of validation rules would result in an opaque server error rather than a user-friendly form redisplay.

**Evidence:**
- Struts-config lines 381–390: `validate="true"` without `input="..."`.
- Comparable mappings in the same file (e.g., `/admindriveradd` line 307, `/adminunitedit` line 337) all include `input="..."`.

**Recommendation:**
Add `input="adminChecklistEditDefinition"` (or the appropriate tile definition) to the `/fleetcheckedit` action mapping.

---

### FINDING-09 — LOW: SQL Query Result Logged at INFO Level Before Execution

**Severity:** LOW
**File:** `src/main/java/com/dao/QuestionDAO.java` lines 96, 276

**Description:**
`QuestionDAO` logs the fully-constructed SQL string (including any injected payload in the `id` parameter) at `INFO` level before executing it. This means any SQL injection attempt, along with the injected SQL text, is written to application logs. While logging is not itself a vulnerability, it means that log files may contain attacker-controlled content, enabling log injection attacks where log-parsing tools misinterpret injected newlines or escape sequences. If the `id` field contained `\n` or ANSI escape sequences they would be written verbatim.

**Evidence:**
- `QuestionDAO.java` line 96: `log.info(sql)` where `sql` contains the unparameterised `id`.
- `QuestionDAO.java` line 276: same pattern in `getQuestionById`.

**Recommendation:**
After remediating FINDING-01 with a `PreparedStatement`, the concatenated SQL will no longer be logged. As a general practice, sanitise or omit parameter values from log statements, or use parameterised logging that separates the template from variable data.

---

## 3. Categories with No Issues

- **Session Handling:** `request.getSession(false)` is used correctly (no session fixation risk from this action). The action does not call `request.getSession(true)` which would create a new session for unauthenticated requests. Session attribute `sessCompId` is read-only in this action; it is never written or regenerated here, which is appropriate.

- **Data Exposure in Response:** The action sets request attributes (`arrQuestions`, `arrAnswerType`, `arrManufacturers`) scoped to the current request and forwards to a tile definition. It does not write directly to `response.getWriter()` or set raw JSON/XML bodies that could expose unexpected data. No sensitive fields (passwords, tokens) are placed in request scope.

---

## 4. Summary Table

| ID | Severity | Category | Short Description |
|----|----------|----------|-------------------|
| FINDING-01 | CRITICAL | SQL Injection | `getQuestionById` uses string concatenation on user-supplied `id` |
| FINDING-02 | HIGH | CSRF | No synchroniser token on create/update POST operations |
| FINDING-03 | HIGH | IDOR | No ownership check; any company can read or overwrite any question by `id` |
| FINDING-04 | HIGH | Session Handling / Availability | No null check on session or `arrComp`; empty `sessCompId` causes NPE/NFE |
| FINDING-05 | MEDIUM | Authentication / AuthZ | No `roles` attribute and no in-action role check |
| FINDING-06 | MEDIUM | Input Validation | `validate="true"` but no validation rules in `validation.xml` for this form |
| FINDING-07 | MEDIUM | Input Validation | Unguarded `parseInt`/`parseLong` on unvalidated form fields |
| FINDING-08 | LOW | Configuration | Missing `input` attribute on mapping with `validate="true"` |
| FINDING-09 | LOW | Log Injection | Unparameterised SQL logged at INFO level with attacker-controlled content |

**Finding counts by severity:**
- CRITICAL: 1
- HIGH: 3
- MEDIUM: 3
- LOW: 2
- INFO: 0

**Total findings: 9**
