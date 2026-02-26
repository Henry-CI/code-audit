# Security Audit Report: AdminFleetcheckAction.java

**Audit run:** audit/2026-02-26-01
**Branch:** master
**Auditor:** CIG Automated Pass-1
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet auth gate, no Spring Security, no CSRF token mechanism

---

## 1. Reading Evidence

### 1.1 Package and Class Name

- **Package:** `com.action`
- **Class:** `AdminFleetcheckAction extends org.apache.struts.action.Action`
- **File:** `src/main/java/com/action/AdminFleetcheckAction.java`

### 1.2 Public/Protected Methods

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` | 18 |

No other public or protected methods are declared in this class. The class has a single entry point via Struts dispatch.

### 1.3 DAOs and Services Called

| DAO / Method | Call Site (line) | Parameters from user input |
|---|---|---|
| `ManufactureDAO.getAllManufactures(sessCompId)` | 33 | `sessCompId` (session-derived) |
| `QuestionDAO.getQuestionByCategory(manu_id, type_id, fuel_type_id, att_id, sessCompId)` | 36-37 | `manu_id`, `type_id`, `fuel_type_id`, `att_id` from form; `sessCompId` from session |
| `QuestionDAO.getMaxQuestionId(manu_id, type_id, fuel_type_id, sessCompId)` | 57 | `manu_id`, `type_id`, `fuel_type_id` from form; `sessCompId` from session |
| `QuestionDAO.getAllAnswerType()` | 62 | none (static lookup) |
| `QuestionDAO.getQuestionByCategory(manu_id, type_id, fuel_type_id, att_id, sessCompId)` | 69-70 | same as above (else-branch) |

### 1.4 Form Class Used

- **Form bean name:** `adminFleetcheckActionForm`
- **Form class:** `com.actionform.AdminFleetcheckActionForm`
- **File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`
- **Fields bound from HTTP request:** `action`, `id`, `manu_id`, `type_id`, `fuel_type_id`, `attachment_id`

### 1.5 struts-config.xml Mapping Details

```xml
<action
    path="/fleetcheckconf"
    name="adminFleetcheckActionForm"
    scope="request"
    validate="true"
    type="com.action.AdminFleetcheckAction"
    input="adminChecklistDefinition">
  <forward name="edit"    path="adminChecklistEditDefinition"/>
  <forward name="success" path="adminChecklistDefinition"/>
  <forward name="failure" path="adminChecklistDefinition"/>
</action>
```

| Attribute | Value |
|-----------|-------|
| Path | `/fleetcheckconf` |
| Scope | `request` |
| validate | `true` (calls `AdminFleetcheckActionForm.validate()`) |
| roles | **not set** (no Struts `roles` attribute anywhere in the config) |
| input (on validation failure) | `adminChecklistDefinition` |

---

## 2. Findings

---

### FINDING-01 — CRITICAL: Null-Pointer Dereference on Null Session Immediately Bypasses Auth Gate Intent

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminFleetcheckAction.java`
**Lines:** 21-23

**Description:**
The action obtains the session with `getSession(false)`, which correctly avoids creating a spurious session. However, on line 22, if `session` is `null` (i.e., the request carries no valid session cookie), the code immediately dereferences `session.getAttribute(...)` without a null check. This causes a `NullPointerException`, which is caught by the global Struts exception handler defined in `struts-config.xml` (line 43-54) and forwards to the `errorDefinition` tile rather than to the login page. An unauthenticated request therefore does **not** receive an authenticated response but it also does **not** receive a proper redirect to login — it receives an unhandled error page. More critically, if a future refactor moves exception handling or the NPE is suppressed, this would silently skip the entire authentication check.

The PreFlightActionServlet guard (`sessCompId != null`) is the authoritative auth gate and should block the request before the action fires. However, the action's own secondary check is broken and provides no safety net. Any path that bypasses or races `PreFlightActionServlet` (e.g., a forward that does not re-enter the servlet, a misconfiguration, or the `excludeFromFilter` whitelist expanding) would reach execute() with a null session and produce an NPE, leaking error detail rather than denying access cleanly.

**Evidence:**
```java
// Line 21
HttpSession session = request.getSession(false);
// Line 22-23 — session is dereferenced unconditionally; NPE if session == null
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? ""
        : session.getAttribute("sessCompId"));
```

**Recommendation:**
Add an explicit null check on `session` immediately after line 21. If null, invalidate and redirect to the login/expire forward rather than continuing. Example pattern:
```java
if (session == null || session.getAttribute("sessCompId") == null
        || session.getAttribute("sessCompId").toString().isEmpty()) {
    return mapping.findForward("globalfailure");
}
```

---

### FINDING-02 — CRITICAL: Auth Check Degrades to Empty String — Unauthenticated Requests May Proceed

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminFleetcheckAction.java`
**Lines:** 22-23

**Description:**
When `session.getAttribute("sessCompId")` returns `null`, the ternary expression assigns an **empty string `""`** to `sessCompId` rather than stopping execution. The code then passes this empty `sessCompId` directly to DAO calls on lines 33, 37, 57, and 69. `ManufactureDAO.getAllManufactures("")` will throw a `NumberFormatException` (because it calls `Long.valueOf("")`), but `QuestionDAO.getQuestionByCategory` calls `StringUtils.isEmpty(compId)` and throws `IllegalArgumentException("Company missing")` — both of which surface as unhandled exceptions and trigger the global error handler rather than a clean authentication denial.

Beyond the reliability issue, the design is wrong: the action should refuse to execute at all when `sessCompId` is absent, not attempt DAO calls with a sentinel empty string. Any future DAO that accepts an empty company ID without validation would expose cross-tenant or unauthenticated data.

**Evidence:**
```java
// sessCompId is set to "" when session attribute is null
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? ""
        : session.getAttribute("sessCompId"));
// Then passed directly to DAO without any further check
request.setAttribute("arrManufacturers", ManufactureDAO.getAllManufactures(sessCompId)); // line 33
```

**Recommendation:**
After retrieving `sessCompId`, assert it is non-null and non-empty before executing any business logic. Fail closed (forward to expire/login) rather than continuing with a sentinel value.

---

### FINDING-03 — HIGH: CSRF — State-Changing "add" Action Accepts Any Cross-Origin POST

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminFleetcheckAction.java`
**Lines:** 47-63
**Supporting file:** `src/main/webapp/WEB-INF/struts-config.xml` lines 391-401

**Description:**
The `action=add` branch (lines 47-63) prepares a new `QuestionBean` and returns the `edit` forward, which leads to a save operation via `AdminFleetcheckEditAction`. There is no CSRF token anywhere in the request processing chain: struts-config.xml declares no token mechanism for this mapping, the form class `AdminFleetcheckActionForm` contains no token field, and the stack description confirms there is no application-wide CSRF protection. An attacker who can induce a logged-in admin to visit a malicious page can forge a POST to `/fleetcheckconf.do?action=add&manu_id=X&type_id=Y&fuel_type_id=Z` to create checklist questions on behalf of the victim.

The `search` branch (line 35) and the `else` branch (line 64) are also reachable via CSRF but are read-only in this action; they do not directly mutate state here. The `add` branch, however, triggers downstream write operations.

**Evidence:**
- No token check in `AdminFleetcheckActionForm.validate()` (lines 49-68 of the form class).
- No token check in `execute()`.
- struts-config.xml `/fleetcheckconf` mapping has no `roles`, no custom filter, no token attribute.
- Stack note: "CSRF = structural gap (no token mechanism anywhere)."

**Recommendation:**
Implement the Struts `TokenProcessor` / `saveToken` + `isTokenValid` pattern or introduce a synchronizer-token filter. At minimum, generate a per-session token, embed it in the form as a hidden field, and validate it in the action or a servlet filter before processing state-changing requests.

---

### FINDING-04 — HIGH: No Role-Based Access Control — Any Authenticated User Can Access Admin Checklist Configuration

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml`
**Lines:** 391-401

**Description:**
The `/fleetcheckconf` mapping has no `roles` attribute. Struts 1.x supports declarative role checking via `<action roles="...">` which delegates to `HttpServletRequest.isUserInRole()`. The absence of this attribute means Struts performs no role enforcement. The PreFlightActionServlet only checks that `sessCompId` is non-null — it does not distinguish admin users from regular operators. Any authenticated company user who can obtain a session (e.g., a driver or operator account) can reach this action and invoke the `add` path, potentially injecting new checklist questions into the company's question set.

**Evidence:**
```xml
<!-- struts-config.xml lines 391-401: no roles attribute -->
<action
    path="/fleetcheckconf"
    name="adminFleetcheckActionForm"
    scope="request"
    validate="true"
    type="com.action.AdminFleetcheckAction"
    input="adminChecklistDefinition">
```
No `roles="admin"` or equivalent is present. `PreFlightActionServlet.excludeFromFilter` (lines 98-115) does not return `false` for `fleetcheckconf.do`, confirming it enters the session check but not a role check.

**Recommendation:**
Add a `roles` attribute to the action mapping restricting access to the appropriate admin role. Additionally, add an in-action role assertion (e.g., check a `sessRole` session attribute) so protection does not rely solely on the Struts declarative mechanism.

---

### FINDING-05 — HIGH: Input Validation Absent for Form Fields — No Format or Range Constraints on ID Parameters

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminFleetcheckActionForm.java`
**Lines:** 49-68
**Supporting file:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
`AdminFleetcheckActionForm.validate()` checks only that `manu_id`, `type_id`, and `fuel_type_id` are non-empty (presence check). It does **not** validate:

- That any of these fields are numeric integers (required by the DAOs which call `Long.parseLong()` / `Integer.parseInt()` on them without try/catch guarding the action layer).
- That `attachment_id` (`att_id`) is numeric or within a valid range.
- That the `action` field contains only expected values (`search`, `add`).
- Maximum length of any field.

`validation.xml` contains no entry for `adminFleetcheckActionForm`. The entire validation burden falls on the minimal `validate()` method in the form class.

Non-numeric input for any ID field (e.g., `manu_id=abc`) will cause a `NumberFormatException` inside the DAO at `Long.parseLong(manuId)`, which propagates as an unhandled exception caught by the global handler — leaking a stack trace in the error response depending on server configuration.

**Evidence:**
```java
// AdminFleetcheckActionForm.validate() — only isEmpty checks, no numeric/format validation
if (StringUtils.isEmpty(manu_id)) { ... }
if (StringUtils.isEmpty(type_id)) { ... }
if (StringUtils.isEmpty(fuel_type_id)) { ... }
// No check on attachment_id, action field, or numeric format of any field
```
```java
// QuestionDAO.getQuestionByCategory line 155 — will throw NFE on non-numeric input
stmt.setLong(++index, Long.parseLong(manuId));
```

**Recommendation:**
Add numeric format validation (`matches("[0-9]+")` or Apache Validator `integer` rule) for all ID fields in `AdminFleetcheckActionForm.validate()`. Add an `adminFleetcheckActionForm` entry to `validation.xml` with `integer` constraints. Also whitelist-validate the `action` field against the set `{search, add}`.

---

### FINDING-06 — MEDIUM: NullPointerException Risk in "add" Branch — Incomplete Null Guard

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminFleetcheckAction.java`
**Lines:** 47-50

**Description:**
The `add` branch checks whether `type_id`, `fuel_type_id`, or `manu_id` are null (line 48), but does **not** check `att_id` (attachment_id). The form's `validate()` method also does not require `attachment_id`. If `att_id` is submitted as an empty string (which is the default in the form class: `private String attachment_id = null;`), it is passed to `QuestionBean.setAttachment_id(att_id)` and then to `QuestionDAO.getMaxQuestionId(manu_id, type_id, fuel_type_id, sessCompId)` on line 57 — that DAO does not use `att_id`, so that call is safe. However, the inconsistent null/empty treatment of `att_id` relative to the other IDs creates a fragile contract.

More significantly, the null check on line 48 uses `== null` rather than `StringUtils.isEmpty()`. The form's `action` field defaults to `null`, and Struts may set empty-string values rather than null depending on request encoding, meaning the null check could fail to catch a case where `type_id` is the empty string `""`, which would then cause `Integer.parseInt("")` inside `getMaxQuestionId` to throw a `NumberFormatException`.

**Evidence:**
```java
// Line 48 — null check only, misses empty string case
if (type_id == null || fuel_type_id == null || manu_id == null) {
    return mapping.findForward("failure");
}
// att_id not checked at all before being set on the bean (line 55)
questionBean.setAttachment_id(att_id);
```

**Recommendation:**
Replace `== null` guards with `StringUtils.isEmpty()` checks consistent with the pattern used elsewhere in the codebase. Apply the same guard to `att_id` where it is used in DAO parameters downstream.

---

### FINDING-07 — MEDIUM: Error Message Key Typo Creates Silent Error-Handling Gap

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminFleetcheckAction.java`
**Lines:** 64-68

**Description:**
In the `else` branch, the error key used when adding the `ActionMessage` is `"resutlerror"` (line 67), which differs from the key used in the `search` branch on line 43 (`"resulterror"`). This is a typo (`resutl` vs `result`). If the JSP template references `"resulterror"` to display errors, the `else` branch error will never be rendered to the user, silently swallowing the error message. This is a logic/reliability issue rather than a direct security vulnerability, but it means error conditions are invisible to the user and may confuse the session state.

**Evidence:**
```java
// Line 43 — correct key
errors.add("resulterror", msg);
// Line 67 — typo: "resutlerror"
errors.add("resutlerror", msg);
```

**Recommendation:**
Correct the typo on line 67 to `"resulterror"`. Consider centralising error key strings as constants to prevent recurrence.

---

### FINDING-08 — LOW: Session Attribute Retrieved Twice Without Caching

**Severity:** LOW
**File:** `src/main/java/com/action/AdminFleetcheckAction.java`
**Lines:** 22-23

**Description:**
`session.getAttribute("sessCompId")` is called twice in the single ternary expression on lines 22-23. While not a security vulnerability in isolation, this is a minor inefficiency and creates a theoretical TOCTOU window in multi-threaded environments where a concurrent session invalidation could cause the first call to return non-null (passing the ternary condition) and the second call to return null (yielding `null` cast to `String`). The practical risk is extremely low given typical session behaviour, but it is poor defensive coding.

**Evidence:**
```java
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? ""
        : session.getAttribute("sessCompId"));
```

**Recommendation:**
Cache the attribute in a local variable before the ternary:
```java
Object rawCompId = session.getAttribute("sessCompId");
String sessCompId = (rawCompId == null) ? "" : (String) rawCompId;
```
Then apply the fail-closed null/empty check recommended in FINDING-02.

---

## 3. Category Summary

| Category | Findings | Notes |
|---|---|---|
| Authentication | FINDING-01, FINDING-02 | NPE on null session; empty-string sentinel used instead of fail-closed denial |
| CSRF | FINDING-03 | No token mechanism; state-changing `add` branch fully exposed |
| Input Validation | FINDING-05 | No numeric format validation; no validation.xml entry for this form |
| SQL Injection | **NO ISSUES** | See note below |
| IDOR | **NO ISSUES** | See note below |
| Session Handling | FINDING-01, FINDING-08 | `getSession(false)` is correct; but result is not null-checked before use |
| Data Exposure | **NO ISSUES** | See note below |
| Role-Based Access Control | FINDING-04 | No `roles` attribute in mapping; no in-action role check |
| Error Handling / Logic | FINDING-06, FINDING-07 | Incomplete null guard in add branch; error key typo |

### SQL Injection — NO ISSUES (in this action's direct DAO calls)

`ManufactureDAO.getAllManufactures(sessCompId)` uses a `PreparedStatement` with a positional parameter (`stmt.setLong(1, Long.valueOf(companyId))`). `QuestionDAO.getQuestionByCategory(...)` uses `PreparedStatement` with positional parameters for all user-supplied IDs. `QuestionDAO.getMaxQuestionId(...)` uses `PreparedStatement` with positional parameters. The DAO methods invoked directly from this action are safe from SQL injection for the inputs passed from this action's execute method.

Note: Other methods in `QuestionDAO` and `ManufactureDAO` that are **not** called from this action (e.g., `getQuestionById(id)`, `delQuestionById(id)`, `getQuesLanId(compId)`, `getQuestionByUnitId(...)`, `getManufactureById(id)`, `checkManuByNm(name, id)`, `getManu_type_fuel_rel(manuId)`) use string concatenation in SQL statements and carry SQL injection risk. These should be flagged in audits of the actions that invoke them.

### IDOR — NO ISSUES

All DAO calls in this action scope their queries to `sessCompId` (the session-derived company identifier). `ManufactureDAO.getAllManufactures(sessCompId)` and `QuestionDAO.getQuestionByCategory(..., sessCompId)` both bind `sessCompId` as a query parameter, ensuring data returned is restricted to the authenticated company. No direct object reference (e.g., a bare question ID) is fetched and returned without the session company scoping in this action. (The `add` branch sets `questionBean.setComp_id(sessCompId)` on line 56, correctly anchoring new records to the session company.)

### Data Exposure — NO ISSUES

No sensitive data (passwords, PII, credentials) is placed in request attributes. The action populates `arrManufacturers`, `arrQuestions`, and `arrAnswerType` — all product-configuration data scoped to the session company. No data is written to the response body directly; all rendering is delegated to the tile/JSP layer.

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|---|---|---|
| CRITICAL | 2 | FINDING-01, FINDING-02 |
| HIGH | 3 | FINDING-03, FINDING-04, FINDING-05 |
| MEDIUM | 2 | FINDING-06, FINDING-07 |
| LOW | 1 | FINDING-08 |
| INFO | 0 | — |
| **Total** | **8** | |

---

## 5. Prioritised Remediation Order

1. **FINDING-01** (CRITICAL) — Add null check on `session` before any attribute access.
2. **FINDING-02** (CRITICAL) — Fail closed when `sessCompId` is null or empty; never proceed with a sentinel value.
3. **FINDING-04** (HIGH) — Add `roles` attribute to the `/fleetcheckconf` mapping and add an in-action session role assertion.
4. **FINDING-03** (HIGH) — Implement synchronizer token (CSRF) protection for state-changing requests.
5. **FINDING-05** (HIGH) — Add numeric and whitelist validation for all ID and action fields; add `adminFleetcheckActionForm` to `validation.xml`.
6. **FINDING-06** (MEDIUM) — Replace null-only guards with `StringUtils.isEmpty()` and cover `att_id`.
7. **FINDING-07** (MEDIUM) — Fix `"resutlerror"` typo in the else-branch error key.
8. **FINDING-08** (LOW) — Cache `sessCompId` attribute in a single local variable lookup.
