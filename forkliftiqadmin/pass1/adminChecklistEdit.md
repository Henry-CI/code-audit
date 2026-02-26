# A08 — adminChecklistEdit.jsp
**Path:** src/main/webapp/html-jsp/adminChecklistEdit.jsp
**Auditor:** A08
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### File
`src/main/webapp/html-jsp/adminChecklistEdit.jsp`

### Includes
- Line 1: `<%@ include file="../includes/importLib.jsp" %>` — static include; pulls in Struts taglib declarations (struts-html, struts-bean, struts-logic) and Java imports. No session check performed here.

### Tiles / Page Template
- Tile definition: `adminChecklistEditDefinition` (tiles-defs.xml line 50–53) extends `loginDefinition` with `header_pop.inc.jsp`.
- `loginDefinition` renders via `tilesTemplateHeader.jsp` — no `adminDefinition` shell (no navigation menu wrapper). The popup tile has no session/role guard of its own.

### HTML / Struts Form Tags
There is no enclosing `<html:form>` tag in this JSP. The submit function constructs and posts via jQuery `$.post()` directly.

| Line | Element | Detail |
|------|---------|--------|
| 1 | `<%@ include %>` | `../includes/importLib.jsp` |
| 14 | `<logic:notEmpty name="arrQuestions">` | Conditional render block |
| 15 | `<logic:iterate name="arrQuestions" id="question" type="com.bean.QuestionBean">` | Iterates request attribute |
| 17 | `<bean:write property="order_no" name="question" />` | Output — numeric, filter=true (default) |
| 19 | `<html:hidden property="order_no" name="question" />` | Hidden field — order_no |
| 25–29 | `<html:textarea property="content" ... name="question"/>` | Textarea bound to QuestionBean.content |
| 35–44 | `<html:select property="expectedanswer" name="question" ...>` | Select — values: YES / NO |
| 51–57 | `<html:select property="answer_type" ... name="question" ...>` | Select — sourced from arrAnswerType |
| 55 | `<html:optionsCollection name="arrAnswerType" value="id" label="name"/>` | Options from request attribute |
| 59 | `<html:hidden property="id" name="question" styleId="question_id" />` | Hidden — question ID (primary key) |
| 60 | `<html:hidden property="type_id" name="question" />` | Hidden — type_id |
| 61 | `<html:hidden property="fuel_type_id" name="question" />` | Hidden — fuel_type_id |
| 62 | `<html:hidden property="manu_id" name="question" />` | Hidden — manu_id |
| 63 | `<html:hidden property="attachment_id" name="question" />` | Hidden — attachment_id |
| 64 | `<html:hidden property="comp_id" name="question" />` | Hidden — comp_id (company identifier) |
| 65 | `<html:hidden property="active" name="question" />` | Hidden — active flag |
| 66 | `<input type="hidden" name="action" value="search"/>` | Plain hidden input |
| 75 | `<button ... onclick="submit();">` | Triggers JavaScript submit() function |

### Scriptlet Blocks
None — no `<% %>` scriptlet blocks present in this JSP.

### Expression Output (`<%= %>`, `${...}`, `<bean:write>`)
| Line | Tag / Expression | Property | Escape (filter) |
|------|-----------------|----------|----------------|
| 17 | `<bean:write property="order_no" name="question" />` | `order_no` (int) | Yes (default filter=true) |

No `<%= %>` Java expressions. No EL `${...}` expressions. No `<bean:write filter="false">` occurrences.

### `<jsp:include>` / `<%@ include %>` / `<c:import>`
- Line 1: `<%@ include file="../includes/importLib.jsp" %>` (static, compile-time include)

### `request.getParameter()` / Session Access
No direct `request.getParameter()` calls in the JSP itself. Data flows through the Struts ActionForm (`AdminFleetcheckEditActionForm`), populated by the framework from request parameters before the JSP renders.

### URL Constructed
- Line 94 (JavaScript): `$.post('fleetcheckconf.do', ...)` — wait, this is actually `$.post('fleetcheckedit.do', ...)` (line 94). No user-controlled URL fragments.

### Hidden Fields
`<html:hidden>` fields (all sourced from `QuestionBean` in request scope, populated by `AdminFleetcheckEditAction`):
- `order_no` (line 19)
- `id` (line 59) — the question record primary key
- `type_id` (line 60)
- `fuel_type_id` (line 61)
- `manu_id` (line 62)
- `attachment_id` (line 63)
- `comp_id` (line 64) — the company identifier
- `active` (line 65)

### Action Class: `AdminFleetcheckEditAction`
`src/main/java/com/action/AdminFleetcheckEditAction.java`

- **GET handler (lines 39–44):** Calls `QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId())` using the user-supplied `id` parameter, then sets `arrQuestions` and `arrAnswerType` on the request and forwards to `adminChecklistEditDefinition`.
- **POST handler (lines 46–73):** Reads form fields, sets `comp_id` from session (`sessCompId`), builds a `QuestionBean`, then calls `update()` or `create()` depending on whether `id` is empty.
- **`update()` (lines 76–95):** Calls `QuestionDAO.updateQuestionInfo(bean)` — updates `WHERE id = ?` without checking whether that id belongs to the session company.
- **`create()` (lines 97–105):** Calls `QuestionDAO.saveQuestionInfo(bean, languageId, compId)` — inserts with the session company id, which is correct.
- Session attributes read: `sessCompId`, `arrComp`.

### QuestionDAO Methods of Interest
`src/main/java/com/dao/QuestionDAO.java`

- **`getQuestionById(String id)` (line 263–308):**
  ```java
  String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id,attachment_id,answer_type,comp_id, active from question where id = " + id;
  ```
  String concatenation — SQL injection. No `comp_id` scope filter.

- **`updateQuestionInfo(QuestionBean)` (line 516–553):**
  ```java
  String sql = "update question set content = ?, expectedanswer = ?, answer_type = ?, active = ? where id = ?";
  ```
  Uses `PreparedStatement` for the DML — not SQL-injectable. However, **no `comp_id` check** in the WHERE clause.

- **`delQuestionById(String id)` (line 174–195):**
  ```java
  String sql = "delete from question where id=" + id;
  ```
  String concatenation — SQL injection. No `comp_id` scope filter.

- **`getQuesLanId(String compId)` (line 30–61):**
  ```java
  String sql = "select lan_id from company where id = " + compId;
  ```
  String concatenation — SQL injection.

- **`getQuestionContentById(String qId, String lanId)` (line 311–360):**
  ```java
  sql = "select content from question where id = " + qId;
  sql = "select content from question_content where question_id = " + qId + " and lan_id = " + lanId;
  ```
  String concatenation — SQL injection.

### web.xml Security Constraints
No `<security-constraint>` elements are present in `web.xml`. The application relies entirely on the custom `PreFlightActionServlet` for session enforcement.

### PreFlightActionServlet (session guard)
`src/main/java/com/actionservlet/PreFlightActionServlet.java`

- Checks that `session != null` and `sessCompId` is not null/empty for all paths not in the exclusion list.
- `fleetcheckedit.do` is **not** in the exclusion list, so the session check applies.
- **No role check is performed.** Any authenticated session (regardless of user role) can reach `fleetcheckedit.do`.
- The check only verifies session existence and non-empty `sessCompId`; it does not verify that the authenticated user is an admin or has edit permission on checklists.

---

## Findings

### CRITICAL-01 — SQL Injection in `getQuestionById` (Read Path for Edit Form)

**Severity:** CRITICAL

**Description:**
`QuestionDAO.getQuestionById(String id)` is invoked directly with the user-supplied `id` request parameter (via `AdminFleetcheckEditActionForm.getId()`). The `id` value is concatenated into a SQL statement without parameterisation.

**File + Line:**
`src/main/java/com/dao/QuestionDAO.java`, line 275

**Code Evidence:**
```java
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id,attachment_id,answer_type,comp_id, active from question where id = " + id;
```
Called from `AdminFleetcheckEditAction.java` line 40:
```java
ArrayList<QuestionBean> arrQuestions = QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId());
```
The `id` is taken from the HTTP GET parameter `id` passed to `fleetcheckedit.do?id=<value>`.

**Recommendation:**
Convert `getQuestionById` to use `PreparedStatement` with a parameterised query: `WHERE id = ?`. Validate that `id` is a positive integer before passing it to the DAO.

---

### CRITICAL-02 — Insecure Direct Object Reference (IDOR) — Question Edit Not Scoped to Authenticated Company

**Severity:** CRITICAL

**Description:**
When a GET request is made to `fleetcheckedit.do?id=<questionId>`, `AdminFleetcheckEditAction` fetches the question record using the user-supplied `id` without verifying that the returned question's `comp_id` matches the authenticated user's `sessCompId`. An authenticated user from Company A can load and edit questions belonging to Company B (or global questions) by simply supplying a different `id` value.

On the POST (update) path, `updateQuestionInfo` executes `UPDATE question ... WHERE id = ?` with no `comp_id` predicate, meaning any authenticated user can overwrite any question record by supplying its `id`.

**File + Lines:**

GET path — `src/main/java/com/action/AdminFleetcheckEditAction.java`, lines 39–43:
```java
if (request.getMethod().equalsIgnoreCase("get")) {
    ArrayList<QuestionBean> arrQuestions = QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId());
    request.setAttribute("arrQuestions", arrQuestions);
    // No check: arrQuestions.get(0).getComp_id().equals(sessCompId)
    return mapping.findForward("edit");
}
```

POST/update path — `src/main/java/com/dao/QuestionDAO.java`, lines 527–536:
```java
String sql = "update question set content = ?, expectedanswer = ?, answer_type = ?, active = ? where id = ?";
// comp_id is NOT in the WHERE clause
ps.setInt(5, Integer.parseInt(questionBean.getId()));
```

**Recommendation:**
- On GET: after loading the question, verify `question.getComp_id().equals(sessCompId)`. Return an authorisation error if the check fails.
- On POST: add `AND comp_id = ?` to the UPDATE WHERE clause and bind the session `sessCompId` value.

---

### CRITICAL-03 — SQL Injection in `delQuestionById`

**Severity:** CRITICAL

**Description:**
`QuestionDAO.delQuestionById(String id)` concatenates the `id` parameter directly into a DELETE statement. Although this method is not called from `adminChecklistEdit.jsp` directly, it is part of the same checklist management surface (called from delete actions on the checklist page) and is in scope as related DAO code read during this audit.

**File + Line:**
`src/main/java/com/dao/QuestionDAO.java`, line 183

**Code Evidence:**
```java
String sql = "delete from question where id=" + id;
stmt.executeUpdate(sql);
```

**Recommendation:**
Use `PreparedStatement`: `DELETE FROM question WHERE id = ?`

---

### HIGH-01 — No CSRF Protection on Checklist Edit Submit

**Severity:** HIGH

**Description:**
The form submission in `adminChecklistEdit.jsp` is performed via a JavaScript `$.post()` call to `fleetcheckedit.do` (lines 93–108). Struts 1.x has no built-in CSRF token mechanism, and no token is generated or validated anywhere in the `AdminFleetcheckEditAction` or in the form. A malicious page visited by an authenticated admin can silently send a cross-site POST to `fleetcheckedit.do` to modify any checklist question (subject to the IDOR issue above).

**File + Lines:**
`src/main/webapp/html-jsp/adminChecklistEdit.jsp`, lines 93–108:
```javascript
function submit() {
    $.post('fleetcheckedit.do', {
        'id': $('input[id=question_id]').val(),
        ...
    }, function() {
        location.reload();
    })
}
```

**Recommendation:**
Implement a synchroniser-token pattern: generate a random CSRF token on session start, store it in the session, embed it as a hidden field in all forms, and validate it server-side on every state-changing POST. Alternatively, verify the `Origin` / `Referer` header server-side as a defence-in-depth measure.

---

### HIGH-02 — `comp_id` Exposed as Client-Side Hidden Field, Allowing Tampering

**Severity:** HIGH

**Description:**
The `comp_id` (the authenticated user's company identifier) is rendered as a client-side hidden field (`<html:hidden property="comp_id" name="question" />`, line 64) and is read back from the submitted form by the POST handler. Although `AdminFleetcheckEditAction` (line 66–67) does override `comp_id` with the session value when building the `QuestionBean` for create/update, the `comp_id` in the hidden field is the value loaded from the database record. A question with a null `comp_id` (a global/template question) will render an empty `comp_id` hidden field. More critically, the presence of this field in the DOM exposes internal company identifiers unnecessarily and creates a confusing dual-source for `comp_id` (form vs. session). If the assignment `bean.setComp_id(sessCompId)` is ever bypassed or removed (e.g., if `sessCompId` is empty due to a session quirk), the user-supplied `comp_id` could take effect.

**File + Line:**
`src/main/webapp/html-jsp/adminChecklistEdit.jsp`, line 64:
```jsp
<html:hidden property="comp_id" name="question" />
```

`src/main/java/com/action/AdminFleetcheckEditAction.java`, line 66:
```java
.comp_id(sessCompId)
```

**Recommendation:**
Remove `comp_id` from the client-side hidden fields entirely. Derive `comp_id` exclusively from the server-side session attribute `sessCompId`. This eliminates a class of potential tampering and reduces information exposure.

---

### HIGH-03 — No Role-Based Access Control: Any Authenticated Session Can Edit Checklists

**Severity:** HIGH

**Description:**
`PreFlightActionServlet` checks only that a session exists and `sessCompId` is non-null/empty. It performs no role check. The `AdminFleetcheckEditAction` action class performs no role check either. Any user with a valid session (including non-admin operator accounts, if they can authenticate) can reach `fleetcheckedit.do` and edit or create checklist questions. This is an admin-only function.

**File + Lines:**
`src/main/java/com/actionservlet/PreFlightActionServlet.java`, lines 56–60:
```java
else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
```
No role attribute is checked. `AdminFleetcheckEditAction.java` contains no role validation.

**Recommendation:**
Add an authorisation check in `AdminFleetcheckEditAction.execute()` that reads a role or permission attribute from the session (e.g., `sessUserRole`) and returns an HTTP 403 / redirect to an error page if the user does not hold an admin role. Alternatively, implement a Struts `RequestProcessor` subclass or servlet filter that enforces role requirements per action path.

---

### HIGH-04 — SQL Injection in `getQuesLanId` and `getQuestionContentById`

**Severity:** HIGH

**Description:**
Two additional DAO methods called as part of the checklist edit workflow contain string-concatenated SQL:

1. `QuestionDAO.getQuesLanId(String compId)` (line 42): `compId` is sourced from the session, so exploitation requires session compromise — but it is still an unsafe pattern.
2. `QuestionDAO.getQuestionContentById(String qId, String lanId)` (lines 328, 330): both parameters are concatenated.

**File + Lines:**
`src/main/java/com/dao/QuestionDAO.java`, line 42:
```java
String sql = "select lan_id from company where id = " + compId;
```
Lines 328 and 330:
```java
sql = "select content from question where id = " + qId;
sql = "select content from question_content where question_id = " + qId + " and lan_id = " + lanId;
```

**Recommendation:**
Replace all string concatenation in SQL statements with `PreparedStatement` parameterised queries.

---

### MEDIUM-01 — Question `content` Field Rendered via `<html:textarea>` Without Explicit Output Escaping Confirmation

**Severity:** MEDIUM

**Description:**
The `content` property of `QuestionBean` is rendered into an `<html:textarea>` tag (lines 25–29). Struts `<html:textarea>` HTML-encodes the value by default when rendering the textarea body, which mitigates stored XSS in the display context. However, this reliance on default framework escaping should be explicitly noted; if the framework version has a bypass or the tag is replaced with a plain `<textarea>` in future, stored XSS would result since `content` is free-form text entered by admin users and stored in the database.

The `<bean:write property="order_no" name="question" />` (line 17) renders an integer and is safe.

There are no `<bean:write filter="false">` usages in this file.

**File + Lines:**
`src/main/webapp/html-jsp/adminChecklistEdit.jsp`, lines 25–29:
```jsp
<html:textarea property="content"
               titleKey="question.content"
               styleClass="form-control input-lg ajax_selector"
               name="question"/>
```

**Recommendation:**
Confirm the Struts version in use HTML-encodes textarea content. Add a code-comment noting this reliance. In the longer term, move to a framework with explicit, opt-out-required escaping.

---

### MEDIUM-02 — `active` Flag Exposed as Hidden Field, Allowing State Manipulation

**Severity:** MEDIUM

**Description:**
The `active` field is rendered as a client-side hidden input (line 65). On POST, the action reads `active` from the form and passes it directly to `updateQuestionInfo`. A user can manipulate the hidden field value in the browser to set `active = "t"` for any question they can reach via the IDOR (CRITICAL-02), re-activating questions that have been administratively deactivated.

**File + Lines:**
`src/main/webapp/html-jsp/adminChecklistEdit.jsp`, line 65:
```jsp
<html:hidden property="active" name="question" />
```
`src/main/java/com/action/AdminFleetcheckEditAction.java`, lines 51, 79:
```java
String active = adminFleetcheckEditActionForm.getActive();
...
bean.setActive(active);
```

**Recommendation:**
The `active` flag should not be editable from the edit form. The edit form is for modifying question content and answer type. Active/inactive toggling is a separate operation (show/hide actions). Remove `active` from the edit form hidden fields and do not pass it through `updateQuestionInfo` from this code path.

---

### MEDIUM-03 — `order_no` Field Exposed as Hidden Field, Allowing Order Manipulation

**Severity:** MEDIUM

**Description:**
The `order_no` field is rendered as a hidden input (line 19) and passed back to the server on POST. There is no server-side validation that the submitted `order_no` is the original value or within an acceptable range. A user can submit an arbitrary integer to reorder questions within a checklist, disrupting the intended question sequence for safety-critical pre-operation checklists.

**File + Line:**
`src/main/webapp/html-jsp/adminChecklistEdit.jsp`, line 19:
```jsp
<html:hidden property="order_no" name="question" />
```

**Recommendation:**
Either remove `order_no` from the edit form (maintain the existing order on edit) or validate server-side that the submitted value is a positive integer within a reasonable range and, if changed, verify the user has permission to reorder.

---

### LOW-01 — No `<security-constraint>` in `web.xml`

**Severity:** LOW

**Description:**
`web.xml` defines no `<security-constraint>` elements. There is no declarative container-managed security. All access control is implemented in application code (`PreFlightActionServlet`). If this servlet is bypassed (e.g., by direct JSP access prior to the dispatcher, or a Tomcat misconfiguration), there is no fallback container-level protection.

**File + Line:**
`src/main/webapp/WEB-INF/web.xml` — no `<security-constraint>` present.

**Recommendation:**
Add a `<security-constraint>` requiring an authenticated role for all `*.do` URLs as a defence-in-depth measure, in addition to the application-level checks.

---

### LOW-02 — Session Timeout Set to 30 Minutes; No Cookie Security Flags Configured in `web.xml`

**Severity:** LOW

**Description:**
`web.xml` sets `<session-timeout>30</session-timeout>`. No `<cookie-config>` is defined to set `HttpOnly`, `Secure`, or `SameSite` attributes on the session cookie. This is a general application-level finding visible from the configuration read during this file's audit.

**File + Line:**
`src/main/webapp/WEB-INF/web.xml`, lines 45–47:
```xml
<session-config>
    <session-timeout>30</session-timeout>
</session-config>
```

**Recommendation:**
Add `<cookie-config><http-only>true</http-only><secure>true</secure></cookie-config>` inside `<session-config>`. Configure `SameSite=Strict` at the Tomcat `context.xml` level or via a response filter.

---

### INFO-01 — Multiple Hidden Fields Create Large Attack Surface for IDOR Chaining

**Severity:** INFO

**Description:**
The form submits seven hidden fields (`id`, `type_id`, `fuel_type_id`, `manu_id`, `attachment_id`, `comp_id`, `active`). All of these are attacker-controllable in the browser. Combined with the IDOR issues (CRITICAL-02), a malicious admin from one company could construct a crafted POST that specifies identifiers belonging to a different company, potentially reading or writing cross-tenant data.

**Recommendation:**
Reduce the number of parameters accepted from the client. The server should derive the category identifiers (`type_id`, `fuel_type_id`, `manu_id`, `attachment_id`) from the server-side record retrieved by `id`, not from client-supplied hidden fields. The only field the client needs to submit is the question `id` (plus the editable fields `content`, `answer_type`, `expectedanswer`).

---

### INFO-02 — Struts 1.x End-of-Life Framework

**Severity:** INFO

**Description:**
This application uses Struts 1.x (`struts-config_1_3.dtd`), which reached end-of-life in 2013. No security patches are released for this framework. Several CVEs exist against Struts 1.x, including class loader manipulation vulnerabilities.

**Recommendation:**
Plan migration to a supported framework. In the interim, keep the Struts 1.x JAR versions as current as possible and monitor for new advisories.

---

## Checklist Coverage

### 1. Secrets and Configuration
**NOT APPLICABLE** to this JSP file directly. No credentials, keys, or configuration values are present in `adminChecklistEdit.jsp`. Covered in other audit files.

### 2. Authentication and Authorization
**FAIL.**
- Authentication: `PreFlightActionServlet` enforces session existence and non-empty `sessCompId` for `fleetcheckedit.do`. Authentication check is present (PASS at the session-existence level).
- Role/authorisation: No role check is performed. Any authenticated user can access the checklist edit action (FAIL — see HIGH-03).
- IDOR: The question `id` is not validated against the authenticated user's organisation on either GET or POST (FAIL — see CRITICAL-02).
- Data scoping: `updateQuestionInfo` WHERE clause does not include `comp_id`, allowing cross-tenant record modification (FAIL — see CRITICAL-02).

### 3. Input Validation and Injection
**FAIL.**
- SQL Injection: `getQuestionById` concatenates user-supplied `id` into SQL (CRITICAL-01). Additional SQL injection in `delQuestionById`, `getQuesLanId`, `getQuestionContentById` (CRITICAL-03, HIGH-04).
- `updateQuestionInfo` uses `PreparedStatement` — PASS for the UPDATE DML.
- `saveQuestionInfo` uses `PreparedStatement` — PASS for the INSERT DML.
- No command injection, SSRF, XXE, or path traversal identified in this file's code path.
- No input validation / whitelist checks on `id`, `type_id`, `fuel_type_id`, `manu_id`, `attachment_id` before DAO calls.

### 4. Session and CSRF
**FAIL.**
- CSRF: No CSRF token is implemented. The `$.post()` submission to `fleetcheckedit.do` is unprotected (HIGH-01).
- Session timeout: 30 minutes configured in `web.xml`.
- Cookie flags: `HttpOnly` and `Secure` not configured in `web.xml` (LOW-02).
- No `X-Frame-Options` or other security headers visible in this JSP or its tile template.

### 5. Data Exposure
**PARTIAL FAIL.**
- `comp_id` is exposed as a hidden field (HIGH-02) — unnecessary client-side exposure of internal identifier.
- `active` flag is exposed as a hidden field (MEDIUM-02).
- `<bean:write filter="false">` is NOT used anywhere in this file — PASS.
- No stack traces or SQL errors rendered in this JSP — PASS (error handling forwards to `error.html`).
- `order_no`, `type_id`, `fuel_type_id`, `manu_id`, `attachment_id` are also exposed as hidden fields (INFO-01).

### 6. Dependencies
**NOT APPLICABLE** to this JSP file. Covered via `pom.xml` audit.

### 7. Build and CI
**NOT APPLICABLE** to this JSP file. Covered via build/pipeline audit.
