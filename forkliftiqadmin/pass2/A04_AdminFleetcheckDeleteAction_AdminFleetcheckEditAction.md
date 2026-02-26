# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A04
**Files audited:**
- `src/main/java/com/action/AdminFleetcheckDeleteAction.java`
- `src/main/java/com/action/AdminFleetcheckEditAction.java`

---

## 1. Reading-Evidence

### 1.1 AdminFleetcheckDeleteAction

**File:** `src/main/java/com/action/AdminFleetcheckDeleteAction.java`
**Class:** `com.action.AdminFleetcheckDeleteAction extends org.apache.struts.action.Action`

**Fields / constants defined:** none (no instance fields; no static constants)

**Imports / collaborators:**
- `com.actionform.AdminFleetcheckDeleteActionForm` — cast target for `actionForm`
- `com.dao.QuestionDAO` — static call `QuestionDAO.delQuestionById(id)`
- Struts: `Action`, `ActionForm`, `ActionForward`, `ActionMapping`
- Servlet: `HttpServletRequest`, `HttpServletResponse`

**Methods:**

| # | Method | Line | Signature |
|---|--------|------|-----------|
| 1 | `execute` | 15–22 | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` |

**execute() logic summary (lines 15–22):**
1. Casts `actionForm` to `AdminFleetcheckDeleteActionForm` (line 19).
2. Calls `QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId())` (line 20).
3. Returns `null` unconditionally (line 21).

---

### 1.2 AdminFleetcheckEditAction

**File:** `src/main/java/com/action/AdminFleetcheckEditAction.java`
**Class:** `com.action.AdminFleetcheckEditAction extends org.apache.struts.action.Action`

**Fields / constants defined:** none (no instance fields; no static constants)

**Imports / collaborators:**
- `com.actionform.AdminFleetcheckEditActionForm` — cast target for `actionForm`
- `com.dao.QuestionDAO` — `getQuestionById`, `getAllAnswerType`, `updateQuestionInfo`, `saveQuestionContent`, `getQuestionByCategory`, `saveQuestionInfo`
- `com.dao.ManufactureDAO` — `getAllManufactures(sessCompId)`
- `com.bean.QuestionBean`, `com.bean.QuestionContentBean`, `com.bean.CompanyBean`
- `org.apache.commons.lang.StringUtils` — `isEmpty`
- Struts: `Action`, `ActionErrors`, `ActionForm`, `ActionForward`, `ActionMapping`, `ActionMessage`
- Servlet: `HttpServletRequest`, `HttpServletResponse`, `HttpSession`

**Methods:**

| # | Method | Lines | Visibility | Signature |
|---|--------|-------|------------|-----------|
| 1 | `execute` | 29–74 | `public` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` |
| 2 | `update` | 76–95 | `private` | `ActionForward update(ActionMapping, HttpServletRequest, QuestionBean, String active, String languageId) throws SQLException` |
| 3 | `create` | 97–105 | `private` | `ActionForward create(ActionMapping, HttpServletRequest, QuestionBean, String languageId) throws SQLException` |
| 4 | `getFailureForward` | 107–112 | `private` | `ActionForward getFailureForward(ActionMapping, HttpServletRequest)` |

**execute() logic summary (lines 29–74):**
1. Gets session with `request.getSession(false)` (line 32); reads `sessCompId` from session (line 33–34).
2. Reads `arrComp` list from session; accesses `arrComp.get(0).getLan_id()` (lines 35–36) — no null-guard on `arrComp`.
3. Casts `actionForm` to `AdminFleetcheckEditActionForm` (line 37).
4. **Branch A — GET request (lines 39–44):** calls `QuestionDAO.getQuestionById`, `QuestionDAO.getAllAnswerType`, sets request attributes, returns `"edit"` forward.
5. **Branch B — non-GET request (lines 46–73):** extracts form fields, calls `ManufactureDAO.getAllManufactures`, builds `QuestionBean`, then:
   - If `questionId` is empty → `create(...)` (line 70).
   - Otherwise → `update(...)` (line 72).

**update() logic summary (lines 76–95):**
1. Sets `active` on bean (line 79).
2. Calls `QuestionDAO.updateQuestionInfo(bean)`; on `false` → `getFailureForward` (line 81).
3. Builds `QuestionContentBean` and calls `QuestionDAO.saveQuestionContent` (lines 83–89).
4. Calls `QuestionDAO.getQuestionByCategory` and sets `arrQuestions` attribute (lines 91–92).
5. Returns `"success"` forward (line 94).

**create() logic summary (lines 97–105):**
1. Calls `QuestionDAO.saveQuestionInfo(bean, languageId, Integer.parseInt(bean.getComp_id()))` (line 99).
2. On `true` → sets `arrQuestions` attribute, returns `"success"` (lines 100–101).
3. On `false` → `getFailureForward` (line 103).

**getFailureForward() logic summary (lines 107–112):**
1. Creates `ActionErrors`, adds `"errors.global"` message (lines 108–110).
2. Calls `saveErrors(request, errors)` (line 110).
3. Returns `"globalfailure"` forward (line 111).

---

### 1.3 Supporting form — AdminFleetcheckDeleteActionForm

**File:** `src/main/java/com/actionform/AdminFleetcheckDeleteActionForm.java`
**Class:** Extends `ValidateIdExistsAbstractActionForm` (which extends `ActionForm`).
**Inherited field:** `protected String id` (from `ValidateIdExistsAbstractActionForm`).
**Inherited method:** `validate(ActionMapping, HttpServletRequest)` — returns `ActionErrors` with `"error.id"` when `id` is null/empty.
No additional fields or methods declared in the concrete class.

### 1.4 Supporting form — AdminFleetcheckEditActionForm

**File:** `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java`
**Fields (all `private`, Lombok `@Getter`/`@Setter`):**
- `serialVersionUID = -8103158863153194997L`
- `String id`, `String content`, `String expectedanswer`, `int order_no`, `String active`
- `String type_id`, `String fuel_type_id`, `String answer_type`, `String comp_id`
- `ArrayList<AnswerTypeBean> arrAnswerType`
- `String manu_id`, `String attachment_id`

---

## 2. Test-Coverage Confirmation

**Test files in project (total: 4):**
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

All four test files are scoped exclusively to `com.calibration` and `com.util` packages (impact/calibration domain). A grep search of the entire test directory for the strings `AdminFleetcheckDelete`, `AdminFleetcheckEdit`, `QuestionDAO`, and `AdminFleetcheck` returned **zero matches**.

**Conclusion:** Zero test coverage exists for either audited class or any of their immediate DAO collaborators.

---

## 3. Coverage Gaps and Findings

---

### A04-1 | Severity: CRITICAL | Zero test coverage — AdminFleetcheckDeleteAction.execute()

`AdminFleetcheckDeleteAction.execute()` is completely untested. This is the sole entry point of the class. It performs a permanent, irreversible database DELETE (`QuestionDAO.delQuestionById`) and returns `null` as the `ActionForward`, which is atypical Struts behavior (it means the framework performs no navigation). No test verifies the deletion is triggered, that the correct ID is passed, that the `null` return is intentional, or that an exception thrown by `delQuestionById` is handled or propagated.

---

### A04-2 | Severity: CRITICAL | Zero test coverage — AdminFleetcheckEditAction (all methods)

`AdminFleetcheckEditAction` and its three private methods (`execute`, `update`, `create`, `getFailureForward`) are entirely untested. Combined these methods contain at least eight distinct branches, multiple DAO interactions, and several null-dereference risks (detailed below). No test exists for any execution path.

---

### A04-3 | Severity: CRITICAL | Null return from execute() in DeleteAction — undefined Struts behavior

**File:** `AdminFleetcheckDeleteAction.java`, line 21.

`execute()` unconditionally returns `null`. In Struts 1, returning `null` from `execute()` instructs the framework to render no view — the HTTP response is left incomplete. This is valid only if the action writes directly to the response. This class never touches the response. The consequence is a blank HTTP response delivered to the browser after a delete. No test verifies whether `null` is intentional (e.g., AJAX scenario) or a latent defect. The absence of any forward name also means redirection to a confirmation or list page never occurs.

---

### A04-4 | Severity: CRITICAL | NullPointerException when session is null — EditAction.execute()

**File:** `AdminFleetcheckEditAction.java`, lines 32–33.

```java
HttpSession session = request.getSession(false);
String sessCompId = session.getAttribute("sessCompId") == null ? ""
        : (String) session.getAttribute("sessCompId");
```

`request.getSession(false)` returns `null` if no session exists. The very next line dereferences `session` without a null check. If a user accesses the action without an active session (e.g., after timeout, direct URL access), a `NullPointerException` is thrown. This path is untested.

---

### A04-5 | Severity: CRITICAL | NullPointerException when arrComp session attribute is null or empty — EditAction.execute()

**File:** `AdminFleetcheckEditAction.java`, lines 35–36.

```java
List<CompanyBean> arrComp = (List<CompanyBean>) session.getAttribute("arrComp");
String lan_id = arrComp.get(0).getLan_id();
```

Two risks:
1. `session.getAttribute("arrComp")` may return `null`; calling `.get(0)` on `null` throws `NullPointerException`.
2. If `arrComp` is an empty list, `.get(0)` throws `IndexOutOfBoundsException`.

Neither case is handled or tested.

---

### A04-6 | Severity: HIGH | Untested GET branch — EditAction.execute()

**File:** `AdminFleetcheckEditAction.java`, lines 39–44.

```java
if (request.getMethod().equalsIgnoreCase("get")) {
    ArrayList<QuestionBean> arrQuestions = QuestionDAO.getQuestionById(adminFleetcheckEditActionForm.getId());
    request.setAttribute("arrQuestions", arrQuestions);
    request.setAttribute("arrAnswerType", QuestionDAO.getAllAnswerType());
    return mapping.findForward("edit");
}
```

No test covers the GET path. Untested behaviors include: the `"edit"` forward being resolved, `getQuestionById` returning an empty list (question not found), `getQuestionById` or `getAllAnswerType` throwing `Exception`, and the resulting `arrQuestions` attribute containing stale or missing data.

---

### A04-7 | Severity: HIGH | Untested create path — EditAction.create()

**File:** `AdminFleetcheckEditAction.java`, lines 97–105.

```java
if (QuestionDAO.saveQuestionInfo(bean, languageId, Integer.parseInt(bean.getComp_id()))) {
    ...
    return mapping.findForward("success");
} else {
    return getFailureForward(mapping, request);
}
```

No test covers:
- Successful creation (DAO returns `true`) and the resulting `"success"` forward.
- Failed creation (DAO returns `false`) and the resulting `"globalfailure"` forward.
- `Integer.parseInt(bean.getComp_id())` throwing `NumberFormatException` when `comp_id` is null, empty, or non-numeric (inherited from `sessCompId` which defaults to `""` at line 33–34).

---

### A04-8 | Severity: HIGH | Untested update path — EditAction.update()

**File:** `AdminFleetcheckEditAction.java`, lines 76–95.

No test covers:
- Successful update (`updateQuestionInfo` returns `true`) continuing to `saveQuestionContent` and returning `"success"`.
- Failed update (`updateQuestionInfo` returns `false`) returning `"globalfailure"` via `getFailureForward`.
- `saveQuestionContent` throwing `SQLException` (exception propagates uncaught from `update` to `execute` and ultimately to the Struts error handler).
- `getQuestionByCategory` throwing `IllegalArgumentException` (which it does when `manuId`, `typeId`, `fuelTypeId`, or `compId` is empty — see `QuestionDAO` lines 131–134).

---

### A04-9 | Severity: HIGH | Untested failure-forward path — EditAction.getFailureForward()

**File:** `AdminFleetcheckEditAction.java`, lines 107–112.

```java
private ActionForward getFailureForward(ActionMapping mapping, HttpServletRequest request) {
    ActionErrors errors = new ActionErrors();
    errors.add(ActionErrors.GLOBAL_MESSAGE, new ActionMessage("errors.global"));
    saveErrors(request, errors);
    return mapping.findForward("globalfailure");
}
```

No test verifies that the `"errors.global"` message is correctly added to the error collection, that `saveErrors` stores errors in the expected request attribute, or that `"globalfailure"` forward is resolved. A misconfigured `struts-config.xml` forward would silently return `null` from `findForward`, yielding a blank response.

---

### A04-10 | Severity: HIGH | No validation of form ID in DeleteAction — SQL injection risk via direct string concatenation

**File:** `com/dao/QuestionDAO.java`, lines 182–185 (called by `AdminFleetcheckDeleteAction`).

```java
String sql = "delete from question where id=" + id;
stmt.executeUpdate(sql);
```

`delQuestionById` receives the `id` string directly from the form field and concatenates it into a SQL statement without using a `PreparedStatement`. While `ValidateIdExistsAbstractActionForm.validate()` confirms that `id` is non-empty, it does not sanitize or validate that the value is numeric. A value such as `1 OR 1=1` would delete all rows. No test verifies that the validation rejects non-numeric or malicious `id` values, and no test verifies that only the intended row is deleted.

---

### A04-11 | Severity: HIGH | NumberFormatException in create() when sessCompId is empty string

**File:** `AdminFleetcheckEditAction.java`, line 99.

```java
QuestionDAO.saveQuestionInfo(bean, languageId, Integer.parseInt(bean.getComp_id()))
```

`bean.getComp_id()` is set from `sessCompId` (line 66), which defaults to `""` (empty string) when the session attribute is null (line 33–34). `Integer.parseInt("")` throws `NumberFormatException`. This runtime exception is not caught inside `execute()`, which only declares `throws Exception`, and no test exercises this path.

---

### A04-12 | Severity: MEDIUM | Untested routing logic — POST with empty questionId routes to create(), non-empty routes to update()

**File:** `AdminFleetcheckEditAction.java`, lines 69–73.

```java
if (StringUtils.isEmpty(questionId)) {
    return create(mapping, request, bean, lan_id);
} else {
    return update(mapping, request, bean, active, lan_id);
}
```

No test verifies that the branch selection is correct (e.g., that a whitespace-only `questionId` is treated as empty by `StringUtils.isEmpty`, or that a non-null but logically invalid ID reaches `update` and causes a downstream error).

---

### A04-13 | Severity: MEDIUM | Exception from QuestionDAO.delQuestionById propagates to Struts uncaught — DeleteAction

**File:** `AdminFleetcheckDeleteAction.java`, line 20.

`delQuestionById` throws `Exception` (re-declared as `SQLException` internally). `execute()` declares `throws Exception`. Any database error propagates to the Struts framework without being caught, logged at the action level, or converted to a user-visible error message. The user receives a Struts-level error page. No test confirms this propagation behavior or verifies that appropriate error pages are mapped in `struts-config.xml`.

---

### A04-14 | Severity: MEDIUM | ManufactureDAO.getAllManufactures called before branch decision — unnecessary DAO call on GET

**File:** `AdminFleetcheckEditAction.java`, line 54.

```java
request.setAttribute("arrManufacturers", ManufactureDAO.getAllManufactures(sessCompId));
```

This line is placed after the GET-branch early return (lines 39–44) and before the POST branch logic, meaning it is executed only on non-GET requests. However, it is placed outside of the `update`/`create` private methods, making it unclear whether it is intentional for all non-GET methods or only relevant to the edit form submission. If another HTTP method (PUT, DELETE, PATCH) were ever routed here, the manufacturer list would be loaded unnecessarily. No test covers the non-GET, non-POST method scenario, nor confirms `sessCompId` is valid before this call.

---

### A04-15 | Severity: MEDIUM | Unchecked cast of session attribute arrComp — ClassCastException risk

**File:** `AdminFleetcheckEditAction.java`, line 35.

```java
List<CompanyBean> arrComp = (List<CompanyBean>) session.getAttribute("arrComp");
```

The session attribute is cast without `instanceof` verification. If the session attribute is populated with a different type (e.g., after a session serialization/deserialization cycle, or a code change to the session population logic), a `ClassCastException` is thrown. No test covers this path.

---

### A04-16 | Severity: MEDIUM | saveQuestionContent result ignored in update() — silent data loss

**File:** `AdminFleetcheckEditAction.java`, line 89.

```java
QuestionDAO.saveQuestionContent(questionContentBean);
```

`saveQuestionContent` returns `boolean` indicating success or failure. The return value is ignored. A failure to persist the question content (e.g., the content update or insert affects zero rows) will not be detected; the action proceeds to return `"success"`, misleading the user into believing the content was saved. No test verifies this behavior.

---

### A04-17 | Severity: LOW | No test for ValidateIdExistsAbstractActionForm.validate() — inherited by DeleteActionForm

**File:** `src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`, lines 19–27.

The `validate()` method is the only server-side guard preventing an empty `id` from reaching `QuestionDAO.delQuestionById`. No test verifies that `validate()` returns an error when `id` is null, that it returns no errors when `id` is a valid non-empty string, or that it is actually invoked by Struts before `execute()` (which depends on correct `validate="true"` in `struts-config.xml`).

---

### A04-18 | Severity: LOW | No test for AdminFleetcheckEditActionForm field accessors

**File:** `src/main/java/com/actionform/AdminFleetcheckEditActionForm.java`

Although Lombok generates the getters and setters, none are exercised by tests. The `arrAnswerType` default initialization (empty `ArrayList`) and the `serialVersionUID` value are never verified. A regression (e.g., removal of a Lombok annotation) would go undetected.

---

### A04-19 | Severity: LOW | No navigation contract tested — forward names "edit", "success", "globalfailure" unverified

Both action classes reference forward names (`"edit"`, `"success"`, `"globalfailure"`) resolved via `mapping.findForward(...)`. No test verifies that the correct forward name is selected under each condition, or that `findForward` does not return `null` due to a misconfigured `struts-config.xml`. A typo in any forward name produces a `null` `ActionForward` silently at runtime.

---

### A04-20 | Severity: INFO | No integration or end-to-end tests for the fleetcheck admin workflow

The fleetcheck question administration workflow (create, read/edit, delete) is a complete admin-facing feature with no test coverage at any layer: no unit tests, no mock-based controller tests, no integration tests. The four existing tests in the project cover only calibration mathematics and utility logic. Adding coverage here would require Mockito (or similar) for DAO mocking, and a Struts test harness such as StrutsTestCase or Spring MVC Test adapted for Struts 1.

---

## 4. Summary Table

| Finding | Severity | Description |
|---------|----------|-------------|
| A04-1 | CRITICAL | Zero test coverage for `AdminFleetcheckDeleteAction.execute()` |
| A04-2 | CRITICAL | Zero test coverage for all methods in `AdminFleetcheckEditAction` |
| A04-3 | CRITICAL | `execute()` returns `null` ActionForward — blank HTTP response, untested intent |
| A04-4 | CRITICAL | NPE when `request.getSession(false)` returns null — no null check at line 33 |
| A04-5 | CRITICAL | NPE / IOOBE when `arrComp` session attribute is null or empty list — line 36 |
| A04-6 | HIGH | GET branch entirely untested — "edit" forward, empty-result, and exception paths |
| A04-7 | HIGH | `create()` path entirely untested — both success and failure branches |
| A04-8 | HIGH | `update()` path entirely untested — both success and failure branches |
| A04-9 | HIGH | `getFailureForward()` path entirely untested — error message assembly and forward |
| A04-10 | HIGH | SQL injection via string concatenation in `delQuestionById` — id not validated as numeric |
| A04-11 | HIGH | `NumberFormatException` in `create()` when `sessCompId` defaults to empty string |
| A04-12 | MEDIUM | Routing branch (create vs update) based on `questionId` emptiness — untested |
| A04-13 | MEDIUM | DAO exception propagates uncaught in `DeleteAction.execute()` — no action-level handling |
| A04-14 | MEDIUM | `ManufactureDAO.getAllManufactures` called without validating `sessCompId` is non-empty |
| A04-15 | MEDIUM | Unchecked cast of `arrComp` session attribute — ClassCastException risk |
| A04-16 | MEDIUM | Return value of `saveQuestionContent` silently ignored — content failures masked as success |
| A04-17 | LOW | `ValidateIdExistsAbstractActionForm.validate()` not tested — sole guard before delete |
| A04-18 | LOW | `AdminFleetcheckEditActionForm` field accessors and defaults untested |
| A04-19 | LOW | Forward names ("edit", "success", "globalfailure") never verified against Struts config |
| A04-20 | INFO | No integration or end-to-end tests exist for the fleetcheck admin workflow |
