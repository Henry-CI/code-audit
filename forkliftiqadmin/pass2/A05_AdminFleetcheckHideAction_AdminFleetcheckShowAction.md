# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A05
**Files audited:**
- `src/main/java/com/action/AdminFleetcheckHideAction.java`
- `src/main/java/com/action/AdminFleetcheckShowAction.java`

---

## 1. Reading Evidence

### 1.1 AdminFleetcheckHideAction

**File:** `src/main/java/com/action/AdminFleetcheckHideAction.java`
**Package:** `com.action`
**Class:** `AdminFleetcheckHideAction extends org.apache.struts.action.Action`

**Fields/Constants defined:** none (no instance fields or static constants)

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` | 19 |

**Imports of note:**
- `com.actionform.AdminFleetcheckHideActionForm` (line 3)
- `com.actionform.AdminFleetcheckActionForm` (line 4) — imported but **never used**
- `com.dao.ManufactureDAO` (line 5) — imported but **never used**
- `com.dao.QuestionDAO` (line 6)
- `javax.servlet.http.HttpSession` (line 14)
- `java.io.PrintWriter` (line 15)

**execute() logic summary (lines 19–39):**
1. Obtains session with `request.getSession(false)` — returns `null` if no active session.
2. Reads `sessCompId` from session attribute; falls back to `""` if null.
3. Casts `actionForm` to `AdminFleetcheckHideActionForm`.
4. Reads four fields from the form: `type_id`, `fuel_type_id`, `manu_id`, `attachment_id`.
5. Calls `QuestionDAO.hideQuestionById(id, manu_id, type_id, fuel_type_id, att_id, sessCompId)`.
6. Writes the literal string `"true"` to the response writer and flushes it.
7. Returns `null` (no Struts forward navigation).

---

### 1.2 AdminFleetcheckShowAction

**File:** `src/main/java/com/action/AdminFleetcheckShowAction.java`
**Package:** `com.action`
**Class:** `AdminFleetcheckShowAction extends org.apache.struts.action.Action`

**Fields/Constants defined:** none

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` | 16 |

**Imports of note:**
- `com.actionform.AdminFleetcheckShowActionForm` (line 3)
- `com.dao.QuestionDAO` (line 4)
- `java.io.PrintWriter` (line 12)

**execute() logic summary (lines 16–26):**
1. Casts `actionForm` to `AdminFleetcheckShowActionForm`.
2. Calls `QuestionDAO.showQuestionById(adminFleetcheckActionForm.getId())`.
3. Writes the literal string `"true"` to the response writer and flushes it.
4. Returns `null`.

---

### 1.3 Supporting classes examined

**AdminFleetcheckHideActionForm** (`src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`)
- Extends `ValidateIdExistsAbstractActionForm`.
- Fields: `type_id`, `fuel_type_id`, `manu_id`, `attachment_id` (all `String`, default `null`).
- `validate()` adds errors for empty `manu_id`, `type_id`, `fuel_type_id`; delegates `id` validation to parent.

**AdminFleetcheckShowActionForm** (`src/main/java/com/actionform/AdminFleetcheckShowActionForm.java`)
- Extends `ValidateIdExistsAbstractActionForm`.
- No additional fields or methods (inherits `id` and `validate()`).

**ValidateIdExistsAbstractActionForm** (`src/main/java/com/actionform/ValidateIdExistsAbstractActionForm.java`)
- Abstract base; field `id` (String, default `null`).
- `validate()` adds `"error.id"` ActionMessage if `id` is empty.

**QuestionDAO.hideQuestionById** (lines 197–208 of `QuestionDAO.java`):
- Calls `getQuestionById(id).get(0)` — throws `IndexOutOfBoundsException` if the list is empty.
- Branch A (global question): `comp_id == null && copied_from_id == null` → copies question then updates.
- Branch B (company question): `comp_id != null` → sets `active = "f"` and updates.
- Implicit Branch C: `comp_id == null && copied_from_id != null` (already-copied global) → **no action taken, silent no-op**.

**QuestionDAO.showQuestionById** (lines 210–213 of `QuestionDAO.java`):
- Calls `getQuestionById(id).get(0)` — throws `IndexOutOfBoundsException` if the list is empty.
- Sets `active = "t"` and calls `updateQuestionInfo`.

---

## 2. Test Coverage Confirmation

**Test files in project:**
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

**Grep results for class names in test directory:**
- `AdminFleetcheckHideAction` — **0 matches**
- `AdminFleetcheckShowAction` — **0 matches**
- `AdminFleetcheckHideActionForm` — **0 matches**
- `AdminFleetcheckShowActionForm` — **0 matches**
- `hideQuestionById` — **0 matches**
- `showQuestionById` — **0 matches**
- `QuestionDAO` — **0 matches**

**Conclusion: Zero test coverage. Neither action class, nor their forms, nor the DAO methods they invoke are referenced anywhere in the test suite.**

---

## 3. Coverage Gaps and Findings

---

### A05-1 | Severity: CRITICAL | AdminFleetcheckHideAction.execute() — no tests whatsoever

The entire `execute()` method of `AdminFleetcheckHideAction` is untested. This method performs a privileged write operation (hiding a fleet-check question from a company's question list by either copying-and-deactivating a global question or deactivating a company-owned question). There is no test for the happy path, no test for any error path, and no test for any edge case.

---

### A05-2 | Severity: CRITICAL | AdminFleetcheckShowAction.execute() — no tests whatsoever

The entire `execute()` method of `AdminFleetcheckShowAction` is untested. This method performs a privileged write operation (restoring a previously hidden question by setting `active = "t"`). There is no test for the happy path, no test for any error path, and no test for any edge case.

---

### A05-3 | Severity: CRITICAL | Null session causes NullPointerException — untested

In `AdminFleetcheckHideAction.execute()` (line 22), `request.getSession(false)` is called. This returns `null` when no HTTP session exists. The very next line (line 23) unconditionally dereferences the returned value by calling `session.getAttribute(...)`, which throws `NullPointerException`. There is no null guard and no test for the unauthenticated / session-expired scenario. An attacker or an expired-session user invoking this action receives an unhandled server error, and the stack trace may be exposed depending on server configuration.

---

### A05-4 | Severity: HIGH | Unsafe cast of ActionForm — untested

Both actions cast `actionForm` directly to their respective form classes without a prior `instanceof` check:
- `AdminFleetcheckHideAction` line 26: `(AdminFleetcheckHideActionForm) actionForm`
- `AdminFleetcheckShowAction` line 19: `(AdminFleetcheckShowActionForm) actionForm`

If the Struts framework is misconfigured and the wrong form class is bound to the action mapping, a `ClassCastException` is thrown and propagates unhandled. No test verifies behavior under an incorrect form type.

---

### A05-5 | Severity: HIGH | QuestionDAO.hideQuestionById() called with empty sessCompId — untested

`sessCompId` defaults to `""` (empty string) when the session attribute is absent (line 23–24 of `AdminFleetcheckHideAction`). This empty string is passed as `compId` to `QuestionDAO.hideQuestionById()`, which internally calls `copyQuestionToCompId`. Inside that method, `Integer.parseInt(compId)` (line 240 of `QuestionDAO`) is called on the empty string, throwing `NumberFormatException`. No test covers this scenario.

---

### A05-6 | Severity: HIGH | getQuestionById().get(0) throws IndexOutOfBoundsException for unknown id — untested

Both `QuestionDAO.hideQuestionById()` (line 198) and `QuestionDAO.showQuestionById()` (line 211) call `getQuestionById(id).get(0)` without checking whether the returned list is empty. If the supplied `id` does not exist in the database, `get(0)` throws `IndexOutOfBoundsException`. Neither action class handles this exception, and there is no test for a non-existent question id in either action.

---

### A05-7 | Severity: HIGH | Response writer obtained after DAO call — partial-write on exception is untested

In both action classes, `response.getWriter()` is obtained after the DAO call completes (line 35 in `AdminFleetcheckHideAction`, line 22 in `AdminFleetcheckShowAction`). If the DAO call throws, the `"true"` response is never written and `null` is returned, resulting in an empty HTTP response body. The calling JavaScript client presumably interprets a non-`"true"` body as failure, but this error-signalling contract is untested and undocumented.

---

### A05-8 | Severity: HIGH | AdminFleetcheckShowAction does not validate session or authorization — untested

Unlike `AdminFleetcheckHideAction`, `AdminFleetcheckShowAction` does not retrieve the session at all. A question can be shown (re-enabled) by supplying only its `id` with no company-scoping check. The action performs no ownership or authorization verification: it will re-activate any question in the database regardless of which company it belongs to. No test verifies that cross-company authorization is enforced (it is not).

---

### A05-9 | Severity: HIGH | Silent no-op for already-copied global question — untested

`QuestionDAO.hideQuestionById()` has three implicit branches based on the question's `comp_id` and `copied_from_id` state:
- Branch A: `comp_id == null && copied_from_id == null` → copy and deactivate (correct behavior for global questions).
- Branch B: `comp_id != null` → deactivate directly (correct behavior for company questions).
- Branch C: `comp_id == null && copied_from_id != null` → **neither branch executes; the method returns without making any database change.** The action still writes `"true"` to the response, falsely reporting success.

This silent no-op means that a previously-copied global question that was not yet associated with a company cannot be hidden; the UI receives `"true"` and the user is given no indication that the operation had no effect. No test covers this branch.

---

### A05-10 | Severity: MEDIUM | Unused imports (AdminManufactureDAO, AdminFleetcheckActionForm) — untested dead code risk

`AdminFleetcheckHideAction.java` imports `com.actionform.AdminFleetcheckActionForm` (line 4) and `com.dao.ManufactureDAO` (line 5), neither of which is used anywhere in the class. This suggests either dead code left from a refactoring or a copy-paste error. If the intent was to use these classes, missing functionality is never exercised. No test would detect the missing usage.

---

### A05-11 | Severity: MEDIUM | attachment_id field name mismatch between form and DAO — untested

`AdminFleetcheckHideActionForm` declares the field as `attachment_id` (getter: `getAttachment_id()`), and the action reads it into `att_id` on line 31. However, `QuestionDAO.hideQuestionById()` takes a parameter also named `attchId` which maps to `compId` in the signature at line 197: `hideQuestionById(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)`. The call at line 33 of the action passes arguments in the order: `id, manu_id, type_id, fuel_type_id, att_id, sessCompId`. Mapping against the DAO signature: `id→id`, `manu_id→manuId`, `type_id→typeId`, `fuel_type_id→fuleTypeId`, `att_id→compId`, `sessCompId→attchId`. **The company id and attachment id arguments are swapped.** `sessCompId` is passed as `attchId` and `att_id` (the attachment id) is passed as `compId`. No test exists to catch this argument-order defect.

---

### A05-12 | Severity: MEDIUM | PrintWriter not closed on normal or exceptional paths — untested

In both action classes the `PrintWriter` obtained from `response.getWriter()` is flushed but never closed. While Struts/the servlet container typically manages the response stream lifecycle, not closing the writer means resource cleanup is entirely implicit. No test verifies that the stream is properly flushed and closed in both the success and exception paths.

---

### A05-13 | Severity: MEDIUM | execute() returns null — no Struts forward configured — untested

Both actions return `null` from `execute()`. In Struts 1, returning `null` instructs the framework to perform no further navigation. This is a valid pattern for AJAX-style actions that write directly to the response. However, there is no test confirming that the HTTP response is well-formed (correct Content-Type, no Struts error page rendered), and there is no documentation or Struts config validation test ensuring the `null` return is intentional and handled correctly by all calling clients.

---

### A05-14 | Severity: LOW | AdminFleetcheckShowAction local variable misnamed — untested

In `AdminFleetcheckShowAction.execute()` (line 19), the local variable cast to `AdminFleetcheckShowActionForm` is named `adminFleetcheckActionForm` (missing `Show`). This is a naming inconsistency. While it does not affect runtime behaviour, it reduces readability and could cause confusion during maintenance. No test would flag this.

---

### A05-15 | Severity: LOW | Response always writes "true" regardless of DAO outcome — untested

Both actions write the literal `"true"` string unconditionally after the DAO call, with no check of whether the DAO operation actually succeeded. `QuestionDAO.updateQuestionInfo()` returns a `boolean` (false if `executeUpdate != 1`), but this return value is not checked anywhere in the call chain initiated by either action. The client always receives `"true"` even when the database update fails silently. No test verifies the response body under DAO failure conditions.

---

### A05-16 | Severity: INFO | No Struts mock / servlet container test infrastructure exists in the project

The four existing test files (`UnitCalibrationImpactFilterTest`, `UnitCalibrationTest`, `UnitCalibratorTest`, `ImpactUtilTest`) are plain unit tests with no servlet or Struts mock infrastructure (e.g., StrutsTestCase, Spring MockMvc, or Mockito servlet mocks). To test the action classes at all, a mocking framework for `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `ActionMapping`, and `ActionForm` would need to be introduced. This is an infrastructure gap that makes all action-class coverage impossible without first setting up that test infrastructure.

---

## 4. Summary Table

| Finding | Severity | Description |
|---------|----------|-------------|
| A05-1 | CRITICAL | `AdminFleetcheckHideAction.execute()` — zero test coverage |
| A05-2 | CRITICAL | `AdminFleetcheckShowAction.execute()` — zero test coverage |
| A05-3 | CRITICAL | `request.getSession(false)` returns null; next line NPEs with no guard and no test |
| A05-4 | HIGH | Unsafe unchecked `ActionForm` cast in both actions; no test for wrong form type |
| A05-5 | HIGH | Empty `sessCompId` passed to DAO causes `NumberFormatException`; untested |
| A05-6 | HIGH | `getQuestionById().get(0)` throws `IndexOutOfBoundsException` for unknown id; untested |
| A05-7 | HIGH | Response writer obtained after DAO; empty body on exception; untested error contract |
| A05-8 | HIGH | `AdminFleetcheckShowAction` performs no session/authorization check; cross-company re-activation possible; untested |
| A05-9 | HIGH | Silent no-op for already-copied global question; action still returns `"true"`; untested |
| A05-10 | MEDIUM | Unused imports (`AdminFleetcheckActionForm`, `ManufactureDAO`) indicate dead or missing code |
| A05-11 | MEDIUM | `att_id` and `sessCompId` arguments are swapped in call to `hideQuestionById`; no test catches defect |
| A05-12 | MEDIUM | `PrintWriter` flushed but never closed; no test for resource cleanup |
| A05-13 | MEDIUM | `execute()` returns `null`; no test confirms AJAX response contract or Struts config alignment |
| A05-14 | LOW | Local variable `adminFleetcheckActionForm` in `AdminFleetcheckShowAction` is misnamed (missing `Show`) |
| A05-15 | LOW | Response always writes `"true"` even when DAO update returns false; untested |
| A05-16 | INFO | No servlet/Struts mock infrastructure in project; action-class tests are not possible without it |
