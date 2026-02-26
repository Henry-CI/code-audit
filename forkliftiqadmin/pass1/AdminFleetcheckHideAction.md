# Security Audit: AdminFleetcheckHideAction.java
**Audit run:** audit/2026-02-26-01
**Branch:** master
**Auditor:** CIG Automated Security Review (Pass 1)
**Date:** 2026-02-26

---

## 1. Reading Evidence

### Package and Class
- **File:** `src/main/java/com/action/AdminFleetcheckHideAction.java`
- **Package:** `com.action`
- **Class:** `AdminFleetcheckHideAction extends org.apache.struts.action.Action`

### Public/Protected Methods
| Line | Method | Signature |
|------|--------|-----------|
| 19 | `execute` | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

### Form Class
- **Class:** `com.actionform.AdminFleetcheckHideActionForm`
  - **File:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`
  - **Extends:** `ValidateIdExistsAbstractActionForm` (which extends `ActionForm`)
  - **Fields:** `type_id`, `fuel_type_id`, `manu_id`, `attachment_id` (all `String`, all nullable/default null)
  - **Inherited field:** `id` (String, from `ValidateIdExistsAbstractActionForm`)
  - **validate() logic:** Checks `id` not empty (super), `manu_id` not empty, `type_id` not empty, `fuel_type_id` not empty. `attachment_id` is NOT validated.

### DAOs / Services Called
| Call site (Action line) | DAO Method | File |
|-------------------------|------------|------|
| Line 33 | `QuestionDAO.hideQuestionById(id, manu_id, type_id, fuel_type_id, att_id, sessCompId)` | `src/main/java/com/dao/QuestionDAO.java` |

### DAO Chain inside `hideQuestionById` (QuestionDAO.java lines 197–208)
1. Line 198: `QuestionDAO.getQuestionById(id)` — raw string concatenation SQL (line 275): `"select ... where id = " + id`
2. Line 202: `QuestionDAO.copyQuestionToCompId(id, manuId, typeId, fuleTypeId, attchId, compId)` — uses `PreparedStatement` (safe)
3. Line 203: `QuestionDAO.updateQuestionInfo(newQuestion)` — uses `PreparedStatement` (safe)
4. Line 206: `QuestionDAO.updateQuestionInfo(question)` — uses `PreparedStatement` (safe)

### struts-config.xml Mapping (lines 411–419)
```xml
<action
    path="/fleetcheckhide"
    name="adminFleetcheckHideActionForm"
    scope="request"
    validate="true"
    type="com.action.AdminFleetcheckHideAction"
    input="adminChecklistDefinition">
    <forward name="success" path="adminChecklistDefinition"/>
</action>
```
- **path:** `/fleetcheckhide`
- **scope:** `request`
- **validate:** `true` (form's `validate()` method IS invoked by Struts)
- **roles:** NOT specified (no `roles` attribute)
- **input:** `adminChecklistDefinition` (fallback tile on validation error)

---

## 2. Audit Findings

---

### FINDING 1 — CRITICAL: SQL Injection in `QuestionDAO.getQuestionById` via user-supplied `id`

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/QuestionDAO.java`, line 275
**Triggered by:** `AdminFleetcheckHideAction.java` line 33 → `QuestionDAO.hideQuestionById` line 198

**Description:**
The `id` field is taken directly from the HTTP form parameter (`adminFleetcheckHideActionForm.getId()`, action line 28–33) and passed without sanitisation into `QuestionDAO.hideQuestionById`. Inside that method, `getQuestionById(id)` concatenates `id` into a raw SQL string:

```java
// QuestionDAO.java line 275
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id," +
             "attachment_id,answer_type,comp_id, active from question where id = " + id;
```

The form-level `validate()` only checks that `id` is not empty (non-null, non-blank); it does NOT enforce that `id` is an integer, and there is no type-coercion or `PreparedStatement` in `getQuestionById`. An attacker can inject arbitrary SQL through the `id` parameter.

**Evidence:**
- `ValidateIdExistsAbstractActionForm.java` lines 22–26: only `StringUtils.isEmpty(this.id)` check.
- `QuestionDAO.java` line 275: `"... where id = " + id` executed via `stmt.executeQuery(sql)` (a raw `Statement`, not a `PreparedStatement`).
- `AdminFleetcheckHideAction.java` line 33: passes raw form value directly to DAO.

**Proof-of-concept vector:**
POST `/fleetcheckhide.do` with `id=1 OR 1=1--` — bypasses the single-row fetch; more destructive payloads (UNION, stacked queries depending on driver) are possible.

**Recommendation:**
Replace `getQuestionById(String id)` with a `PreparedStatement` identical to the pattern already used in `copyQuestionToCompId` and `updateQuestionInfo`. Validate `id` as a positive integer in `ValidateIdExistsAbstractActionForm` before any DAO call.

---

### FINDING 2 — HIGH: Missing Role/Authorization Check — Any Authenticated User Can Hide Questions

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckHideAction.java`, lines 22–38
**struts-config.xml:** lines 411–419

**Description:**
The struts-config mapping for `/fleetcheckhide` carries no `roles` attribute. The only access gate is the `PreFlightActionServlet` session check (`sessCompId != null`), which confirms only that the user has a valid company session — not that they are an administrator. Any authenticated user (including a regular driver/operator account with a valid session) can POST to `/fleetcheckhide.do` and suppress fleetcheck questions for any `id` they can guess, cross-company (see IDOR below).

**Evidence:**
- `struts-config.xml` lines 411–419: no `roles="..."` attribute.
- `PreFlightActionServlet.java` lines 56–60: only checks `sessCompId != null`.
- `AdminFleetcheckHideAction.java` lines 22–24: reads `sessCompId` but uses it only as a pass-through parameter to the DAO; no comparison against a required admin role stored in the session.

**Recommendation:**
Add a role/privilege check in the action `execute()` method (or via a Struts `roles` attribute if container-managed security is available): verify the session contains an `admin` or equivalent role attribute before proceeding. Reject with HTTP 403 or redirect to an error page if the check fails.

---

### FINDING 3 — HIGH: IDOR — `sessCompId` Is Not Verified Against the Target Question's `comp_id`

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckHideAction.java`, line 33
**DAO:** `src/main/java/com/dao/QuestionDAO.java`, lines 197–208

**Description:**
`sessCompId` (the caller's company ID from the session) is passed into `hideQuestionById` as the sixth argument (mapped to the `compId` parameter). However, inside `hideQuestionById` the first operation is an unconditional fetch of the question by `id` only (line 198), with no WHERE clause restricting to the caller's company. The returned `question.getComp_id()` is then compared to `null` to decide whether to copy or deactivate — but there is no check that `question.getComp_id()` matches `sessCompId`.

Consequence: a user from company A can supply the `id` of a question belonging to company B. If that question is company-owned (`comp_id != null`) the action will deactivate it (set `active = 'f'`) regardless of company ownership. If the question is global, a company-scoped copy will be created with the attacker's `compId` — which is benign for the global record but confirms cross-company enumeration.

**Evidence:**
- `QuestionDAO.java` line 198: `QuestionDAO.getQuestionById(id).get(0)` — no company filter.
- `QuestionDAO.java` lines 201–207: branch logic uses `question.getComp_id() == null` but never asserts `question.getComp_id().equals(compId)`.
- `AdminFleetcheckHideAction.java` line 33: `sessCompId` is passed as the last arg (`compId`) yet the DAO does not enforce ownership before acting.

**Recommendation:**
After fetching the question at line 198, assert `question.getComp_id() == null || question.getComp_id().equals(compId)`. If this assertion fails, abort with an appropriate error (log the anomaly, return HTTP 403, do not forward to the success tile).

---

### FINDING 4 — HIGH: Null Pointer Dereference / Authentication Bypass via `session.getAttribute` Without Null-Check on Session Object

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckHideAction.java`, lines 22–24

**Description:**
`request.getSession(false)` (line 22) returns `null` if no session exists. The very next line immediately calls `session.getAttribute(...)` without first checking whether `session` is null:

```java
HttpSession session = request.getSession(false);           // line 22 — can return null
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? ""  // line 23 — NPE if session is null
        : session.getAttribute("sessCompId"));
```

If `session` is `null`, this throws a `NullPointerException`. While `PreFlightActionServlet` is intended to intercept unauthenticated requests before they reach the action, the servlet checks `excludeFromFilter(path)` first (lines 48–61). If `fleetcheckhide.do` were ever added to the exclusion list by mistake, or if the servlet is bypassed (e.g., direct invocation in tests, misconfiguration, or future refactoring), the NPE would be thrown rather than a clean auth rejection. Additionally, when the NPE is caught by the global exception handler (struts-config.xml lines 42–55), it falls through to the `errorDefinition` page, leaking that an unauthenticated request reached an admin action.

Separately, even when `sessCompId` resolves to `""` (empty string, line 23's fallback), the action continues executing and passes `""` as `compId` to the DAO. `QuestionDAO.hideQuestionById` then calls `copyQuestionToCompId(..., "", ...)`, which calls `Integer.parseInt("")`, throwing a `NumberFormatException`. This means the code relies entirely on the servlet pre-filter for null-session protection; no defensive guard exists in the action itself.

**Evidence:**
- Action lines 22–24: `getSession(false)` without null guard, immediate attribute access.
- `PreFlightActionServlet.java` lines 44–61: protection is conditional on `excludeFromFilter`.
- DAO `copyQuestionToCompId` line 240: `ps.setInt(5, Integer.parseInt(compId))` — crashes on empty string.

**Recommendation:**
Add an explicit null and empty-string guard immediately after `getSession(false)`:
```java
if (session == null || session.getAttribute("sessCompId") == null
        || session.getAttribute("sessCompId").toString().isEmpty()) {
    response.sendError(HttpServletResponse.SC_UNAUTHORIZED);
    return null;
}
```

---

### FINDING 5 — HIGH: CSRF — No Token Protection on State-Changing Action

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckHideAction.java` (entire action)
**struts-config.xml:** lines 411–419

**Description:**
This is a structural gap acknowledged for the entire application. The `/fleetcheckhide.do` endpoint permanently suppresses fleetcheck questions for a company. It accepts a POST (or GET — Struts 1 does not enforce method) with no CSRF token. An attacker who can induce an authenticated admin to visit a crafted page can forge a request that hides arbitrary questions from a company's fleetcheck configuration.

**Evidence:**
- No CSRF token field in `AdminFleetcheckHideActionForm.java`.
- No token validation in `AdminFleetcheckHideAction.java`.
- `struts-config.xml` mapping has no custom request-processor or interceptor for CSRF.
- Struts 1.3.10 provides `TokenProcessor` (Synchronizer Token Pattern) but it is not used here.

**Recommendation:**
Implement Struts 1's built-in synchronizer token: call `saveToken(request)` when rendering the checklist page and `isTokenValid(request, true)` at the top of `execute()`. Reject requests that fail token validation.

---

### FINDING 6 — MEDIUM: `attachment_id` Not Validated — Potential SQL Injection Secondary Vector

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminFleetcheckHideActionForm.java`, lines 20–38
**DAO:** `src/main/java/com/dao/QuestionDAO.java`, line 234–237

**Description:**
The form's `validate()` method checks `manu_id`, `type_id`, and `fuel_type_id` for emptiness, but `attachment_id` is accepted with no validation whatsoever. In `copyQuestionToCompId`, `attachment_id` is handled via a `PreparedStatement` (`ps.setInt(4, Integer.parseInt(attchId))`), so this specific call site is not directly injectable. However, the absence of validation means:

1. A non-numeric `attachment_id` causes an unhandled `NumberFormatException` inside the DAO, exposing internal stack information if exception handling is improperly configured.
2. Other DAO methods that accept `attchId` (e.g., `getQuestionByCategory` line 128, `getQuestionByUnitId` line 89) handle it via string comparisons (`equalsIgnoreCase("0")`, string appends) — a non-numeric value passed to those paths from other entry points could create injection conditions if `attachment_id` flows there.
3. Consistency: all ID fields should be constrained to positive integers at the form layer.

**Evidence:**
- `AdminFleetcheckHideActionForm.java`: no validation block for `attachment_id`.
- `QuestionDAO.java` line 235: `Integer.parseInt(attchId)` — no prior numeric check.
- `QuestionDAO.java` line 89: `sql += " and (attachment_id is null or attachment_id = " + attchId + ")"` — raw concatenation (though not triggered from this action's path).

**Recommendation:**
Add integer-range validation for `attachment_id` in `AdminFleetcheckHideActionForm.validate()` mirroring the checks for the other ID fields. Consider adding a shared utility method in `ValidateIdExistsAbstractActionForm` to validate all numeric ID fields.

---

### FINDING 7 — MEDIUM: Unchecked List Access — `getQuestionById(id).get(0)` Can Throw on Empty Result

**Severity:** MEDIUM
**File:** `src/main/java/com/dao/QuestionDAO.java`, line 198

**Description:**
`hideQuestionById` calls `QuestionDAO.getQuestionById(id).get(0)` without checking whether the returned list is empty. If the provided `id` does not correspond to any row in the `question` table (e.g., a deleted record, an out-of-range id), the call throws `IndexOutOfBoundsException`. This exception propagates to the action, is caught by the Struts global exception handler, and renders the `errorDefinition` page — confirming to the attacker that the supplied ID was invalid (oracle behaviour useful for enumeration).

**Evidence:**
- `QuestionDAO.java` line 198: `.get(0)` with no preceding size check.
- `QuestionDAO.java` lines 210–213 (`showQuestionById`): same pattern, same risk.
- `struts-config.xml` lines 42–55: `SQLException` and `IOException` are caught globally but `IndexOutOfBoundsException` (a `RuntimeException`) is not explicitly listed, so it propagates as an unhandled 500.

**Recommendation:**
Check the list size before calling `.get(0)`. If empty, throw a descriptive application exception (or return cleanly with an appropriate user-facing error message) rather than letting an `IndexOutOfBoundsException` propagate.

---

### FINDING 8 — MEDIUM: Raw SQL Logging Exposes Full Query Including User Input

**Severity:** MEDIUM
**File:** `src/main/java/com/dao/QuestionDAO.java`, lines 96, 184, 276

**Description:**
Multiple DAO methods log the fully constructed SQL string (including user-supplied values) at `INFO` level via `log.info(sql)`. For the raw-concatenation queries (`getQuestionById`, `delQuestionById`, `getQuestionByUnitId`) this means user-controlled input — including any injection payloads — is written to application logs. Log injection (newline injection into log entries) and sensitive data leakage through log aggregation systems are the direct risks.

**Evidence:**
- `QuestionDAO.java` line 276: `log.info(sql)` after `"... where id = " + id`.
- `QuestionDAO.java` line 184: `log.info(sql)` after `"delete from question where id=" + id`.
- `QuestionDAO.java` line 96: `log.info(sql)` after a multi-concatenation query including `unitId`, `compId`, `lanId`, `attchId`.

**Recommendation:**
Do not log the assembled SQL string at INFO level in production. If query logging is required for debugging, use a parameterised representation (log the template and parameters separately, not the concatenated string). Apply log sanitisation (strip/escape CRLF) before writing any user-supplied value to the log.

---

### FINDING 9 — LOW: Response Written Directly via `PrintWriter`; Content-Type Not Set

**Severity:** LOW
**File:** `src/main/java/com/action/AdminFleetcheckHideAction.java`, lines 35–38

**Description:**
The action bypasses Struts forwarding by writing `"true"` directly to the `HttpServletResponse` and returning `null`. No `Content-Type` header is set before calling `response.getWriter()`. Most servlet containers default to `text/html; charset=ISO-8859-1`, which allows a browser to attempt HTML parsing of the response body. While the single word `"true"` is not exploitable as-is, the pattern is fragile: if error state causes a different string to be written (e.g., exception message), it could expose internal information in a context where the browser renders it as HTML.

**Evidence:**
- Action lines 35–38: `response.getWriter()` / `writer.write("true")` / `return null`.
- No `response.setContentType(...)` call.

**Recommendation:**
Set `response.setContentType("text/plain; charset=UTF-8")` before calling `getWriter()`. Consider whether returning a Struts forward with a JSON/text result tile would be a cleaner and more maintainable pattern.

---

### FINDING 10 — INFO: `validate="true"` Is Correctly Set; Form Validation Partially Covers Fields

**Severity:** INFO
**File:** `struts-config.xml` line 415; `AdminFleetcheckHideActionForm.java` lines 20–38

**Description:**
The mapping correctly sets `validate="true"`, and the form's `validate()` method enforces non-empty values for `id`, `manu_id`, `type_id`, and `fuel_type_id` at the application layer. This is a partial positive finding. However, as noted in Findings 1 and 6, the validation does not enforce numeric type constraints on any of these fields, and `attachment_id` is wholly unvalidated.

**Recommendation:**
Extend existing validation to include numeric type checking (positive integer) for all ID fields including `attachment_id`.

---

### FINDING 11 — INFO: `adminFleetcheckHideActionForm` Not Listed in `validation.xml`

**Severity:** INFO
**File:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
The Commons Validator `validation.xml` file defines rules for only three forms: `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`. `adminFleetcheckHideActionForm` has no corresponding `<form>` entry. Validation for this action relies entirely on the programmatic `validate()` method in the form class. This is acceptable in Struts 1, but means the validation rules are not visible in the centralised validation descriptor and are not subject to the declarative constraint checking (e.g., `integer`, `range` validator rules) that `validation.xml` provides.

**Recommendation:**
No immediate action required, but consider migrating numeric field constraints to declarative `validation.xml` rules (using the `integer` and `intRange` validators) so that all ID field validation is consistently enforced and auditable from a single location.

---

## 3. Summary Table

| # | Severity | Category | Location |
|---|----------|----------|----------|
| 1 | CRITICAL | SQL Injection | `QuestionDAO.java:275` via `AdminFleetcheckHideAction.java:33` |
| 2 | HIGH | Missing Authorization / Role Check | `AdminFleetcheckHideAction.java:19-38`, `struts-config.xml:411-419` |
| 3 | HIGH | IDOR (Cross-Company Question Manipulation) | `QuestionDAO.java:197-208`, `AdminFleetcheckHideAction.java:33` |
| 4 | HIGH | Null-Session NPE / Auth Bypass Risk | `AdminFleetcheckHideAction.java:22-24` |
| 5 | HIGH | CSRF (Structural Gap) | `AdminFleetcheckHideAction.java` (whole action) |
| 6 | MEDIUM | Missing Input Validation (`attachment_id`) | `AdminFleetcheckHideActionForm.java:20-38` |
| 7 | MEDIUM | Unchecked List Access / Error Oracle | `QuestionDAO.java:198` |
| 8 | MEDIUM | Raw SQL Logged (Log Injection / Data Exposure) | `QuestionDAO.java:96,184,276` |
| 9 | LOW | Missing `Content-Type` on Direct Response | `AdminFleetcheckHideAction.java:35-38` |
| 10 | INFO | Validation Partially Covers Fields (no type check) | `AdminFleetcheckHideActionForm.java`, `struts-config.xml:415` |
| 11 | INFO | Form Absent from `validation.xml` | `validation.xml` |

**Finding counts:**
- CRITICAL: 1
- HIGH: 4
- MEDIUM: 3
- LOW: 1
- INFO: 2
- **Total: 11**
