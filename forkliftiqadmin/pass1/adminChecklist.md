# A07 — adminChecklist.jsp
**Path:** src/main/webapp/html-jsp/adminChecklist.jsp
**Auditor:** A07
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### File
`src/main/webapp/html-jsp/adminChecklist.jsp`

### Include directives
- Line 1: `<%@ include file="../includes/importLib.jsp" %>` — static include of `src/main/webapp/includes/importLib.jsp`. That file imports Struts tag libraries (`struts-html`, `struts-bean`, `struts-logic`) and Java utility imports. It does not perform any session/auth check itself.

### HTML / Struts form tags
| Line | Tag | Action | Method |
|------|-----|--------|--------|
| 14–17 | `<html:form>` | `fleetcheckconf.do` | `post` |

The form has no CSRF token field of any kind.

### `<html:hidden>` fields inside the form
| Line | Property | Value attribute |
|------|----------|-----------------|
| 70 | `action` | `""` (set by JavaScript `$('.chkact').val('search')` before submit) |
| 71 | `id` | `""` (not populated on list page; used by edit/delete flows) |

### `<bean:write>` output sinks (potential XSS)
All occurrences use default `<bean:write>` without `filter="false"`, meaning the Struts tag applies HTML entity escaping by default.

| Line | Bean / Property | Notes |
|------|-----------------|-------|
| 98 | `QuestionRecord.order_no` | Integer — low XSS risk even if unescaped |
| 101 | `QuestionRecord.content` | String from DB — HTML-escaped by default `<bean:write>` |
| 123 | `QuestionRecord.id` (inside `onclick="showQuestion(...)"`) | Integer injected directly into a JavaScript event handler attribute. No `filter` attribute, but `<bean:write>` HTML-escapes; **HTML encoding does not neutralise JavaScript context injection** |
| 131 | `QuestionRecord.id` (inside `onclick="hideQuestion(...)"`) | Same JavaScript context issue as line 123 |
| 138 | `QuestionRecord.id` (inside `href` URL) | Integer in URL — low direct XSS risk; URL not encoded but value is expected integer |
| 147 | `QuestionRecord.id` (inside `data-delete-value` attribute) | HTML attribute context — escaped by `<bean:write>` default |
| 155 | `QuestionRecord.id` (inside `onclick="hideQuestion(...)"`) | Same JavaScript context issue as line 123 |

### `<%= %>` scriptlet expressions
None present in this file.

### `${...}` EL expressions
None present in this file.

### Scriptlet blocks `<% %>`
None present in this file.

### `request.getParameter()` / session access in JSP
None directly in the JSP. All data arrives via request attributes set by the Action.

### URLs constructed
- Line 195 (JavaScript): `var url = "fleetcheckconf.do?action=add&manu_id=" + manu_id + "&type_id=" + type_id + "&fuel_type_id=" + fuel_type_id;` — values come from `<select>` DOM values. These are passed as GET parameters. No encoding applied (raw string concatenation).
- Lines 235, 239 (JavaScript): `'./fleetcheckhide.do'` and `'./fleetcheckshow.do'` — static URLs, no user input in the URL itself; `id` is passed as POST body parameter via `$.post`.

### `<jsp:include>` / `<c:import>`
None present in this file.

---

### Tiles / Struts routing context

**Tile definition** (`tiles-defs.xml` line 38–40):
```xml
<definition name="adminChecklistDefinition" extends="adminDefinition">
    <put name="content" value="/html-jsp/adminChecklist.jsp"/>
</definition>
```
This tile extends `adminDefinition`, which uses `tilesTemplate.jsp` with a standard navigation menu.

**Action mappings that forward to this view:**

1. `/adminmenu` → `adminchecklist` forward → `adminChecklistDefinition`
   (`AdminMenuAction.java` line 57–59, triggered by `?action=configChecklist`)

2. `/fleetcheckconf` → `success` or `failure` forward → `adminChecklistDefinition`
   (`struts-config.xml` lines 391–401, `AdminFleetcheckAction.java`)

3. `/fleetcheckshow` → `success` → `adminChecklistDefinition`
4. `/fleetcheckhide` → `success` → `adminChecklistDefinition`
5. `/fleetcheckdelete` → `success` → `adminChecklistDefinition`

**Action class populating request attributes for this JSP:**
- `com.action.AdminFleetcheckAction` (primary)
- `com.action.AdminMenuAction` (initial navigation path)

**Request attributes rendered by the JSP:**
| Attribute | Set by | Type |
|-----------|--------|------|
| `arrManufacturers` | `AdminFleetcheckAction` line 33; `AdminMenuAction` line 58 | `List` from `ManufactureDAO.getAllManufactures(sessCompId)` |
| `arrQuestions` | `AdminFleetcheckAction` lines 45, 61, 71 | `List<QuestionBean>` from `QuestionDAO.getQuestionByCategory(...)` |
| `arrAdminUnitType` | `AdminFleetcheckActionForm` constructor (via `UnitDAO`) | `ArrayList` |
| `arrAdminUnitFuelType` | `AdminFleetcheckActionForm` constructor (via `UnitDAO`) | `ArrayList` |
| `arrAttachment` | `AdminFleetcheckActionForm` constructor (via `UnitDAO`) | `ArrayList` |

**Session attributes read by Action classes serving this page:**
- `sessCompId` — company ID of authenticated user (used to scope all data queries)
- `sessUserId` — user ID
- `sessTimezone`, `sessDateFormat` — formatting preferences

---

### Authentication gate: PreFlightActionServlet

`com.actionservlet.PreFlightActionServlet` (web.xml) intercepts all `*.do` requests. For paths NOT in the exclusion list, it checks that:
1. Session is not null.
2. `session.getAttribute("sessCompId")` is not null and not empty.

`fleetcheckconf.do`, `fleetcheckhide.do`, `fleetcheckshow.do`, `fleetcheckdelete.do`, and `adminmenu.do` are all subject to this gate — none appear in the `excludeFromFilter` exclusion list.

No **role** check is performed — only a session/company-ID presence check.

---

### SQL in QuestionDAO relevant to this page

**`getQuestionByCategory`** (line 128–172): Uses parameterised `PreparedStatement` — no injection risk.

**`getQuestionById`** (line 275): String concatenation — `"... where id = " + id` — SQL injection if `id` is attacker-controlled.

**`delQuestionById`** (line 183): String concatenation — `"delete from question where id=" + id` — SQL injection.

**`getQuesLanId`** (line 42): String concatenation — `"select lan_id from company where id = " + compId` — SQL injection if `compId` is attacker-controlled, though `compId` is sourced from session.

**`getQuestionByUnitId`** (lines 82–94): Multiple string-concatenated parameters including `unitId`, `lanId`, `compId`, `attchId`.

---

## Findings

### FINDING 1 — HIGH — CSRF: All state-changing POST endpoints lack anti-CSRF tokens

**Severity:** HIGH

**Description:**
Struts 1.x provides no built-in CSRF protection. The `<html:form>` on `adminChecklist.jsp` (line 14) submits to `fleetcheckconf.do` (action=search/add) with no synchronizer token. The AJAX calls in `postAndReload()` (lines 247–256) POST to `fleetcheckhide.do` and `fleetcheckshow.do` without any token. The delete action triggered via `data-method-action="delete_questions"` and `data-delete-value` (line 147) also submits to `fleetcheckdelete.do` without a token. No CSRF token field exists anywhere in the form, in the Action classes, or in the codebase (confirmed by full-codebase search returning zero matches for "csrf").

A cross-site request forgery attack can cause any authenticated admin user to unknowingly add, hide, show, or delete checklist questions.

**File + Lines:**
- `src/main/webapp/html-jsp/adminChecklist.jsp` lines 14–72 (form), lines 235–256 (AJAX POSTs)
- `src/main/java/com/action/AdminFleetcheckHideAction.java` (no token check)
- `src/main/java/com/action/AdminFleetcheckShowAction.java` (no token check)
- `src/main/java/com/action/AdminFleetcheckDeleteAction.java` (no token check)

**Code Evidence:**
```jsp
<!-- adminChecklist.jsp lines 14-17: form with no token -->
<html:form method="post"
           action="fleetcheckconf.do"
           styleId="adminUnitEditForm"
           styleClass="checklist_from">
```
```java
// AdminFleetcheckDeleteAction.java — no session/token validation at all
QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId());
```
```javascript
// adminChecklist.jsp lines 247-256 — raw AJAX POST, no token
$.post(url, {
    'manu_id': manu_id,
    'type_id': type_id,
    'fuel_type_id': fuel_type_id,
    'id': id
}, function(data) { ... });
```

**Recommendation:**
Implement a synchronizer token pattern. Generate a cryptographically random token on session creation, store it in session, embed it as a hidden form field and as a header on AJAX requests, and validate it in each Action (or in a shared filter/interceptor) before processing state changes. Struts 1.x `TokenProcessor` provides a built-in mechanism via `saveToken(request)` / `isTokenValid(request)`.

---

### FINDING 2 — HIGH — Missing authorization role check: any authenticated session can manage checklist data

**Severity:** HIGH

**Description:**
`PreFlightActionServlet` only verifies that `sessCompId` is present in the session. It does not verify that the authenticated user holds an admin role or any specific privilege to configure checklists. If a non-admin user (e.g., an operator who has any valid session) accesses `adminmenu.do?action=configChecklist` or posts directly to `fleetcheckconf.do`, `fleetcheckhide.do`, `fleetcheckshow.do`, or `fleetcheckdelete.do`, the Action classes perform no role check before executing database writes.

`AdminFleetcheckDeleteAction.java` is the most severe case: it performs a hard delete of any question with the supplied `id` with no ownership or role verification at all beyond session presence.

**File + Lines:**
- `src/main/java/com/actionservlet/PreFlightActionServlet.java` lines 48–61 (only checks `sessCompId`)
- `src/main/java/com/action/AdminFleetcheckDeleteAction.java` lines 18–22 (no role check)
- `src/main/java/com/action/AdminFleetcheckHideAction.java` lines 19–38 (no role check)
- `src/main/java/com/action/AdminFleetcheckShowAction.java` lines 18–26 (no role check)

**Code Evidence:**
```java
// PreFlightActionServlet.java lines 56-60: only presence check
else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
```
```java
// AdminFleetcheckDeleteAction.java lines 19-21: no role check before delete
AdminFleetcheckDeleteActionForm adminFleetcheckDeleteActionForm = (AdminFleetcheckDeleteActionForm) actionForm;
QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId());
return null;
```

**Recommendation:**
Add an explicit role/privilege check in each Action class (or a centralised filter). At minimum, verify that the session contains a flag indicating the user is an admin (e.g., `session.getAttribute("sessUserRole")`). Return an HTTP 403 or redirect to an error page if the check fails. The application is named `forkliftiqadmin` — all endpoints should require a confirmed admin role.

---

### FINDING 3 — HIGH — SQL Injection in `delQuestionById` (reachable from this JSP)

**Severity:** HIGH

**Description:**
`QuestionDAO.delQuestionById(String id)` builds a DELETE statement by direct string concatenation without parameterisation. The `id` value originates from `AdminFleetcheckDeleteActionForm.getId()`, which is populated from the `id` request parameter. Although the form validator (`ValidateIdExistsAbstractActionForm.validate()`) rejects an empty `id`, it does not validate that the value is numeric. An attacker who bypasses client-side validation can supply a crafted `id` such as `1 OR 1=1` to delete all questions, or use a subquery to exfiltrate data.

**File + Line:**
- `src/main/java/com/dao/QuestionDAO.java` line 183

**Code Evidence:**
```java
// QuestionDAO.java line 183
String sql = "delete from question where id=" + id;
stmt.executeUpdate(sql);
```

**Recommendation:**
Replace string concatenation with a `PreparedStatement`:
```java
String sql = "delete from question where id = ?";
ps = conn.prepareStatement(sql);
ps.setLong(1, Long.parseLong(id));
ps.executeUpdate();
```
Additionally, validate that `id` is a positive integer in the `ActionForm` before it reaches the DAO.

---

### FINDING 4 — HIGH — SQL Injection in `getQuestionById` (reachable from hide/show flows)

**Severity:** HIGH

**Description:**
`QuestionDAO.getQuestionById(String id)` uses string concatenation: `"... where id = " + id`. This method is called by `hideQuestionById` and `showQuestionById`, which are invoked from `AdminFleetcheckHideAction` and `AdminFleetcheckShowAction` respectively. The `id` parameter originates from the form action form (`AdminFleetcheckHideActionForm.getId()`), which is populated from the POST body. The validator only checks that `id` is non-empty.

**File + Line:**
- `src/main/java/com/dao/QuestionDAO.java` line 275

**Code Evidence:**
```java
// QuestionDAO.java line 275
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id,attachment_id,answer_type,comp_id, active from question where id = " + id;
```

**Recommendation:**
Use a `PreparedStatement` with a parameterised `?` placeholder and parse `id` as a `Long` before binding. Apply the same fix to `getQuestionContentById` (lines 328, 330) and `getQuesLanId` (line 42) which share the same pattern.

---

### FINDING 5 — MEDIUM — XSS: `QuestionBean.id` written into JavaScript event handlers without JS encoding

**Severity:** MEDIUM

**Description:**
`<bean:write>` applies HTML entity encoding (`filter="true"` by default), which is sufficient for HTML attribute and text node contexts. However, at lines 123, 131, and 155, `QuestionRecord.id` is embedded directly inside JavaScript `onclick` attribute values:

```jsp
onclick="showQuestion(<bean:write property="id" name="QuestionRecord"/>)"
onclick="hideQuestion(<bean:write property="id" name="QuestionRecord"/>)"
```

HTML encoding does not neutralise JavaScript injection. If the `id` field in the database were ever populated with a non-numeric value (e.g., by a direct DB injection or a future code path that does not enforce integer-only IDs), a value such as `0);alert(1)//` would survive HTML encoding and execute as JavaScript. The `id` is currently always a database-assigned integer, which limits exploitability in practice, but the pattern is architecturally unsafe.

**File + Lines:**
- `src/main/webapp/html-jsp/adminChecklist.jsp` lines 123, 131, 155

**Code Evidence:**
```jsp
<!-- line 123 -->
onclick="showQuestion(<bean:write property="id" name="QuestionRecord"/>)">
<!-- line 131 -->
onclick="hideQuestion(<bean:write property="id" name="QuestionRecord"/>)">
<!-- line 155 -->
onclick="hideQuestion(<bean:write property="id" name="QuestionRecord"/>)">
```

**Recommendation:**
Since `id` is expected to be a numeric integer, add explicit integer validation in `QuestionBean` or in the JSP. The safest pattern is to ensure IDs are always rendered as integers (e.g., use `<c:out>` with an integer cast or validate the value server-side). Do not rely solely on HTML encoding for JavaScript contexts.

---

### FINDING 6 — MEDIUM — XSS: `QuestionBean.content` displayed via `<bean:write>` — default escaping confirmed but sourced from user-editable DB content

**Severity:** MEDIUM

**Description:**
Line 101 renders `QuestionRecord.content` using `<bean:write property="content" name="QuestionRecord"/>`. The default `filter="true"` applies HTML entity encoding, which is correct for an HTML text node context and mitigates stored XSS here. However, the `content` field is user-supplied checklist question text (editable via `adminChecklistEdit.jsp` / `AdminFleetcheckEditAction`). The reliance on a tag-level default rather than an explicit `filter="true"` attribute means that if this tag were ever copied and the default changed (e.g., to `filter="false"` as is done elsewhere in the codebase), stored XSS would be introduced. Additionally, `QuestionDAO.saveQuestionContent` and `updateQuestionInfo` store the raw string with no sanitisation, creating a dependency on output-encoding at every rendering point.

**File + Lines:**
- `src/main/webapp/html-jsp/adminChecklist.jsp` line 101
- `src/main/java/com/dao/QuestionDAO.java` lines 454–455, 527–528 (raw string stored)

**Code Evidence:**
```jsp
<!-- line 101: implicit filter=true -->
<bean:write property="content" name="QuestionRecord"/>
```
```java
// QuestionDAO.java line 455: raw content stored
ps.setString(1, qeustionContentBean.getContent());
```

**Recommendation:**
Add explicit `filter="true"` to all `<bean:write>` tags rendering user-controlled string content. Consider adding a content-security policy header to provide defence-in-depth.

---

### FINDING 7 — MEDIUM — Missing org-scoping check in `AdminFleetcheckDeleteAction` (IDOR)

**Severity:** MEDIUM

**Description:**
`AdminFleetcheckDeleteAction` calls `QuestionDAO.delQuestionById(id)` where `id` comes directly from the request. `delQuestionById` executes `DELETE FROM question WHERE id = ?` with no `comp_id` filter. There is no check that the question being deleted belongs to the authenticated user's company. An authenticated admin from Company A can delete questions owned by Company B by supplying a valid question `id` belonging to Company B.

`AdminFleetcheckShowAction` has the same issue: `showQuestionById` fetches the question by raw `id` and updates `active = 't'` with no ownership check.

**File + Lines:**
- `src/main/java/com/action/AdminFleetcheckDeleteAction.java` lines 19–22
- `src/main/java/com/dao/QuestionDAO.java` line 183 (`delQuestionById`)
- `src/main/java/com/action/AdminFleetcheckShowAction.java` lines 18–26
- `src/main/java/com/dao/QuestionDAO.java` line 210–213 (`showQuestionById`)

**Code Evidence:**
```java
// AdminFleetcheckDeleteAction.java
QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId());
```
```java
// QuestionDAO.java line 183
String sql = "delete from question where id=" + id;
```
No `comp_id = ?` clause.

**Recommendation:**
Add `AND comp_id = ?` (binding `sessCompId` from session) to the DELETE and UPDATE statements in `delQuestionById`, `showQuestionById`, and `hideQuestionById` when they modify non-global questions. In `AdminFleetcheckDeleteAction`, retrieve `sessCompId` from session and pass it to the DAO for use in the WHERE clause.

---

### FINDING 8 — MEDIUM — No security-constraint declarations in web.xml; no declarative role enforcement

**Severity:** MEDIUM

**Description:**
`web.xml` contains no `<security-constraint>` elements. Declarative container-level access control (requiring a valid authenticated role to access `*.do` patterns) is entirely absent. All access control is implemented ad hoc in `PreFlightActionServlet`, which only checks for the presence of `sessCompId` in session — it does not enforce any role, and it only runs for GET requests (POST calls `doGet`, which does execute the check, but the structure is fragile and error-prone).

**File + Lines:**
- `src/main/webapp/WEB-INF/web.xml` (entire file — no `<security-constraint>` present)
- `src/main/java/com/actionservlet/PreFlightActionServlet.java` lines 36–86

**Code Evidence:**
```xml
<!-- web.xml: session-config only, no security-constraint -->
<session-config>
    <session-timeout>30</session-timeout>
</session-config>
```

**Recommendation:**
Add `<security-constraint>` declarations in `web.xml` to restrict all `*.do` URLs to authenticated users at the container level. Consider implementing a proper Struts 1.x interceptor or filter that checks role claims on every request, and remove the `doPost -> doGet` delegation pattern in `PreFlightActionServlet` to avoid subtle bypass risks.

---

### FINDING 9 — LOW — JavaScript URL construction without encoding (open redirect risk in add flow)

**Severity:** LOW

**Description:**
`fnaddchecklist()` (lines 191–198) constructs a URL by concatenating raw DOM select values:
```javascript
var url = "fleetcheckconf.do?action=add&manu_id=" + manu_id + "&type_id=" + type_id + "&fuel_type_id=" + fuel_type_id;
```
The values come from `<select>` elements whose options are populated server-side from database lookups scoped to `sessCompId`, so the option values are not directly user-typed. However, an attacker who can tamper the DOM (e.g., via a previously injected script or browser developer tools) could insert arbitrary values. More significantly, the values are never `encodeURIComponent`-encoded, which means special characters in future dynamic option values could break the URL structure or introduce query-string injection.

**File + Lines:**
- `src/main/webapp/html-jsp/adminChecklist.jsp` lines 192–197

**Code Evidence:**
```javascript
var url = "fleetcheckconf.do?action=add&manu_id=" + manu_id + "&type_id=" + type_id + "&fuel_type_id=" +  fuel_type_id;
```

**Recommendation:**
Wrap each variable with `encodeURIComponent()` when constructing URL query strings in JavaScript.

---

### FINDING 10 — LOW — `session.getSession(false)` result not null-checked before attribute access in Action classes

**Severity:** LOW

**Description:**
`AdminFleetcheckAction.execute()` (line 22) calls `request.getSession(false)` and immediately dereferences the result on line 22–23 without a null check. If the session is genuinely null (race condition on session expiry after `PreFlightActionServlet` checks but before the Action executes), a `NullPointerException` will be thrown, which is caught by the global exception handler and forwarded to `errorDefinition`. This is an availability/error-handling concern rather than a direct security vulnerability, but exception stack traces leaking to error pages could reveal internal information.

**File + Lines:**
- `src/main/java/com/action/AdminFleetcheckAction.java` lines 21–23

**Code Evidence:**
```java
HttpSession session = request.getSession(false);
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? ""
        : session.getAttribute("sessCompId"));
```

**Recommendation:**
Add a null check: `if (session == null) { return mapping.findForward("failure"); }` immediately after `getSession(false)`.

---

### FINDING 11 — INFO — `fleetcheckdelete.do` triggered client-side without AJAX confirmation; no server-side response

**Severity:** INFO

**Description:**
The delete button (line 143–149) uses `data-delete-action` and `data-method-action` attributes to trigger deletion through a JavaScript framework (likely a custom handler elsewhere in the template). `AdminFleetcheckDeleteAction` returns `null` (line 22), meaning no Struts forward is executed and no response is written — the HTTP response will be empty (200 with no body). This is a design inconsistency that could cause silent failure or unexpected client-side behaviour, and it means the framework's "success" forward to `adminChecklistDefinition` (in `struts-config.xml` line 427) is never actually used.

**File + Lines:**
- `src/main/java/com/action/AdminFleetcheckDeleteAction.java` line 22
- `src/main/webapp/WEB-INF/struts-config.xml` line 427

**Recommendation:**
`AdminFleetcheckDeleteAction` should either write an explicit JSON response (as `AdminFleetcheckHideAction` does with `writer.write("true")`) or return a proper Struts forward. The current `return null` is a latent maintenance hazard.

---

## Checklist Coverage

### 1. Secrets and Configuration
**NOT APPLICABLE to this JSP directly.** No credentials, API keys, or database URLs are present in `adminChecklist.jsp`. Covered separately for config files.

### 2. Authentication and Authorization
**FAIL.**
- Authentication: `PreFlightActionServlet` enforces session presence (`sessCompId` not null) for all `*.do` paths except a small exclusion list. `fleetcheckconf.do`, `fleetcheckhide.do`, `fleetcheckshow.do`, `fleetcheckdelete.do` are all protected at this level. PASS for basic authentication gate.
- Authorization / role check: **FAIL.** No role check is performed beyond session presence. Any user with a valid `sessCompId` in session can execute all checklist management operations. See Finding 2.
- IDOR: **FAIL.** `delQuestionById` and `showQuestionById` accept arbitrary question `id` values with no ownership verification against `sessCompId`. See Finding 7.

### 3. Input Validation and Injection
**FAIL.**
- SQL Injection: **FAIL.** `delQuestionById` (line 183) and `getQuestionById` (line 275) use string concatenation. See Findings 3 and 4.
- `getQuestionByCategory` uses `PreparedStatement` — PASS for that method.
- XSS input validation: No sanitisation at input layer; relies on output encoding — acceptable only if output encoding is consistently applied (see Section 5).
- Command injection, SSRF, XXE, path traversal, deserialization: No evidence of these patterns in the code paths exercised by this JSP.

### 4. Session and CSRF
**FAIL.**
- CSRF: **FAIL.** No synchronizer token or any other CSRF protection exists anywhere in the application (zero matches for "csrf" in entire Java source tree). All POST endpoints driven by this page are vulnerable. See Finding 1.
- Session: Session timeout is set to 30 minutes (web.xml line 46) — acceptable. Session fixation not investigated at this layer (login flow out of scope for this file). No `secure` or `HttpOnly` cookie configuration found in web.xml.
- Security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`): Not set in web.xml. Not assessed in this file's scope, but no evidence of header-setting filters in the servlet configuration.

### 5. Data Exposure
**PARTIAL PASS / FAIL.**
- Org-scoping for question list: `getQuestionByCategory` correctly filters by `sessCompId` (parameterised). PASS.
- Org-scoping for delete/show: **FAIL.** No `comp_id` check in delete and show operations. See Finding 7.
- Error responses: The global exception handler in `struts-config.xml` (lines 42–55) forwards to `errorDefinition` (which resolves to `/error/error.html`). Stack traces are not directly rendered in this JSP. Acceptable.
- Logging: `QuestionDAO` logs raw SQL statements (including parameter values in some methods via `log.info(sql)`) at INFO level. Concern exists for any SQL that includes user-visible data in non-parameterised queries — but this is a DAO-level concern rather than JSP-specific.

### 6. Dependencies
**NOT IN SCOPE for this JSP.** Covered separately via `pom.xml` review.

### 7. Build and CI
**NOT IN SCOPE for this JSP.** Covered separately.
