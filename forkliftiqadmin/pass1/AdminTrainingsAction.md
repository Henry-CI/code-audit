# Security Audit Report: AdminTrainingsAction.java
**Audit Run:** audit/2026-02-26-01
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** Automated Security Review
**Stack:** Apache Struts 1.3.10 (not Spring)

---

## 1. Reading Evidence

### Package and Class
- **File:** `src/main/java/com/action/AdminTrainingsAction.java`
- **Package:** `com.action`
- **Class:** `AdminTrainingsAction extends PandoraAction` (which extends `org.apache.struts.action.Action`)

### Public/Protected Methods
| Line | Signature |
|------|-----------|
| 17 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

### DAOs / Services Called
| Line | Call |
|------|------|
| 15 | `private TrainingDAO trainingDAO = new TrainingDAO()` (field initialisation) |
| 27-35 | `trainingDAO.addTraining(DriverTrainingBean, dateFormat)` — INSERT into `driver_training` |
| 38 | `trainingDAO.deleteTraining(trainingsForm.getTraining())` — DELETE from `driver_training` by id |

### Form Class
- **Form:** `AdminTrainingsActionForm` (`src/main/java/com/actionform/AdminTrainingsActionForm.java`)
- **Fields:** `action` (String), `driver` (Long), `manufacturer` (Long), `type` (Long), `fuelType` (Long), `trainingDate` (String), `expirationDate` (String), `training` (Long — the record id used for delete)

### Struts-Config Mapping (`/trainings`)
```xml
<action
    path="/trainings"
    type="com.action.AdminTrainingsAction"
    name="AdminTrainingsActionForm"
    scope="request"
    validate="false">
    <forward name="operatortraining" path="OperatorTrainingDefinition"/>
    <forward name="success"          path="OperatorTrainingDefinition"/>
    <forward name="failure"          path="/adminmenu.do?action=home"/>
</action>
```
| Attribute | Value |
|-----------|-------|
| path | `/trainings` |
| scope | `request` |
| validate | **`false`** |
| roles | **not set** |
| input | not set |

### Parent Class — `PandoraAction`
- Provides `getCompId(HttpSession)` which reads `sessCompId` from session.
- `AdminTrainingsAction.execute()` **never calls `getCompId()`**.

### Auth Gate — `PreFlightActionServlet`
- `doGet` / `doPost` check `session.getAttribute("sessCompId") != null` before dispatching.
- `/trainings.do` is **not** in the `excludeFromFilter` whitelist, so the servlet-level check is active.

### Validation Configuration
- `validation.xml` defines rules for three forms only: `loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm`.
- `AdminTrainingsActionForm` has **no entry** in `validation.xml`.
- The struts-config mapping sets `validate="false"`, so even if a rule existed it would be bypassed.

---

## 2. Findings

---

### FINDING-01 — CRITICAL: No Company-Scope Enforcement (IDOR / Broken Object-Level Authorisation)

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminTrainingsAction.java`
**Lines:** 27-42
**Category:** IDOR / Broken Object-Level Authorisation

**Description:**
The action accepts a raw `training` id (for delete) and raw `driver` id (for add) directly from the HTTP request with no verification that these records belong to the company of the authenticated user. Any authenticated admin from company A can delete training records owned by company B simply by supplying an arbitrary numeric id. Similarly, a training record can be added for any driver id in the system, not just drivers belonging to the caller's company.

**Evidence:**
```java
// Line 38 — no ownership check before delete
trainingDAO.deleteTraining(trainingsForm.getTraining());

// Lines 27-35 — no check that trainingsForm.getDriver() belongs to sessCompId
trainingDAO.addTraining(DriverTrainingBean.builder()
        .driver_id(trainingsForm.getDriver())
        ...
        .build(), dateFormat);
```
The DAO query is:
```java
// TrainingDAO.java line 72
"DELETE FROM driver_training WHERE id = ?"
```
No JOIN or sub-select on `company_id` / `comp_id`. The parent class `PandoraAction.getCompId()` exists but is never called in this action.

**Recommendation:**
Before the delete, verify that the training record's associated driver belongs to `sessCompId`. Before the add, verify that `driver_id` belongs to `sessCompId`. The DAO's `deleteTraining` should be extended (or a new method created) that includes a company-scoped WHERE clause, e.g.:
`DELETE FROM driver_training WHERE id = ? AND driver_id IN (SELECT id FROM driver WHERE comp_id = ?)`

---

### FINDING-02 — HIGH: CSRF — No Token Validation on State-Changing Operations

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminTrainingsAction.java` / `src/main/webapp/WEB-INF/struts-config.xml` line 284-292
**Category:** CSRF

**Description:**
Both the `add` and `delete` operations are state-changing (INSERT and DELETE to the database). There is no CSRF token generated, embedded in the form, or validated in the action. Apache Struts 1.3.10 provides the `org.apache.struts.action.Action#saveToken` / `isTokenValid` mechanism, but it is not used here. An attacker who can induce an authenticated admin to visit a crafted page can delete or create training records on their behalf.

**Evidence:**
- `struts-config.xml` line 285-292: no `<set-property>` for token validation.
- `AdminTrainingsAction.java`: no call to `isTokenValid(request)` or `resetToken(request)`.
- The CSRF gap is a documented structural issue across the stack as noted in the audit brief.

**Recommendation:**
Add `saveToken(request)` in the JSP that renders the training form, and call `isTokenValid(request, true)` at the top of `execute()` before performing any mutation. Return the `failure` forward (and do not execute the mutation) if the token is absent or invalid.

---

### FINDING-03 — HIGH: Struts Validation Disabled — No Input Validation on Any Field

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml` line 288 / `src/main/webapp/WEB-INF/validation.xml`
**Category:** Input Validation

**Description:**
The action mapping explicitly sets `validate="false"`. No declarative rules exist for `AdminTrainingsActionForm` in `validation.xml`. As a result, none of the form inputs — `action`, `driver`, `manufacturer`, `type`, `fuelType`, `trainingDate`, `expirationDate`, `training` — undergo any Struts-level validation before `execute()` is called. The date fields arrive as raw `String` values and are parsed by `DateUtil.stringToSQLDate()` without prior sanitisation.

**Evidence:**
```xml
<!-- struts-config.xml lines 283-292 -->
<action
    path="/trainings"
    ...
    validate="false">
```
`validation.xml` contains no `<form name="AdminTrainingsActionForm">` element.

**Recommendation:**
Set `validate="true"` on the mapping and add a `<form name="AdminTrainingsActionForm">` block in `validation.xml` that enforces:
- `action`: required; mask rule restricting to `add|delete`.
- `driver`, `manufacturer`, `type`, `fuelType`, `training`: required (per operation); long/integer type.
- `trainingDate`, `expirationDate`: required (for add); date mask matching the allowed format.
At minimum, add programmatic validation inside `execute()` or via `AdminTrainingsActionForm.validate()`.

---

### FINDING-04 — HIGH: NullPointerException / Application Crash on Missing `action` Parameter

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminTrainingsAction.java` line 25
**Category:** Input Validation / Denial of Service

**Description:**
The `switch` on `trainingsForm.getAction()` is executed without a null-check. `AdminTrainingsActionForm` initialises `action` to `null`. If the `action` HTTP parameter is absent or empty, `getAction()` returns `null` and `switch (null)` throws `NullPointerException` at runtime in Java. This is caught by the global `<exception>` handler (mapped to `errorDefinition`), meaning it fails silently from the user's perspective, but it constitutes an uncontrolled exception path and, when repeatedly triggered, can pollute logs and consume server resources.

**Evidence:**
```java
// AdminTrainingsActionForm.java line 14
private String action = null;

// AdminTrainingsAction.java line 25 — NPE if action is null
switch (trainingsForm.getAction()) {
```

**Recommendation:**
Guard the switch with a null/blank check and return the `failure` forward explicitly:
```java
String action = trainingsForm.getAction();
if (action == null || action.isBlank()) {
    return mapping.findForward("failure");
}
switch (action) { ... }
```
Additionally, declaring `action` as required in `validation.xml` (see FINDING-03) would prevent the null from reaching `execute()`.

---

### FINDING-05 — MEDIUM: `sessDateFormat` Read Without Null-Check — Potential NullPointerException

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminTrainingsAction.java` line 23
**Category:** Session Handling / Robustness

**Description:**
`session.getAttribute("sessDateFormat")` is cast directly to `String` and used to parse dates for the `add` operation. If `sessDateFormat` is absent from the session (e.g., session was created but not fully populated, or a concurrent logout stripped attributes), `dateFormat` will be `null`. This null is passed to `DateUtil.stringToSQLDate()` (line 65 of `TrainingDAO.java`), which passes it to `new SimpleDateFormat(null)`, throwing `NullPointerException` or `IllegalArgumentException`, causing an unhandled exception on the add path.

**Evidence:**
```java
// AdminTrainingsAction.java line 23
String dateFormat = (String)session.getAttribute("sessDateFormat");

// TrainingDAO.java line 65
stmt.setDate(5, DateUtil.stringToSQLDate(trainingBean.getTraining_date(), dateFormat));

// DateUtil.java line 80
formatter = new SimpleDateFormat(dateFormat);  // NPE if dateFormat is null
```

**Recommendation:**
Add a null/blank check and fail-safe default:
```java
String dateFormat = (String) session.getAttribute("sessDateFormat");
if (dateFormat == null || dateFormat.isBlank()) {
    return mapping.findForward("failure");
}
```
Alternatively, store the format in an application-scoped constant with a fallback.

---

### FINDING-06 — MEDIUM: Unvalidated `action` Parameter Controls Execution Branch

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminTrainingsAction.java` line 25
**Category:** Input Validation

**Description:**
The `action` field is a raw, unbounded `String` sourced from the HTTP request. It determines which database operation is performed. Although the current code only acts on `"add"` and `"delete"` (the `default` case is a no-op), the absence of an allowlist means that any string value is accepted without rejection. If the switch branches are ever extended without a corresponding allowlist check, arbitrary behaviour could be triggered. The pattern is fragile and relies on implicit no-op behaviour of the default branch rather than explicit rejection.

**Evidence:**
```java
// AdminTrainingsActionForm.java line 14 — unbounded string
private String action = null;

// AdminTrainingsAction.java lines 25-42 — no allowlist rejection
switch (trainingsForm.getAction()) {
    case "add": ...
    case "delete": ...
    default: return null;  // silently accepts any value
}
```

**Recommendation:**
Explicitly validate `action` against an allowlist (`"add"`, `"delete"`) and return the `failure` forward for any unexpected value. Do not rely on the default branch as a safety net.

---

### FINDING-07 — MEDIUM: Date String Input Not Validated Before Database Insertion

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminTrainingsAction.java` lines 32-33 / `src/main/java/com/util/DateUtil.java` lines 76-88
**Category:** Input Validation

**Description:**
`trainingDate` and `expirationDate` are free-form strings passed from the form directly to `DateUtil.stringToSQLDate()`. `stringToSQLDate` uses `SimpleDateFormat` with `setLenient(true)` (the default), which silently coerces invalid dates (e.g., month 13 becomes January of the next year). There is no server-side range check, no check that expiration is after training date, and no format enforcement before the parse attempt. A parse failure results in `Objects.requireNonNull(date)` throwing `NullPointerException` (DateUtil.java line 86), producing an unhandled server error.

**Evidence:**
```java
// DateUtil.java lines 80-86
formatter = new SimpleDateFormat(dateFormat);
try {
    date = formatter.parse(str_date);
} catch (ParseException e) {
    System.out.println("Exception :" + e);  // exception swallowed
}
dte = new java.sql.Date(Objects.requireNonNull(date).getTime()); // NPE on parse failure
```
No validation in `AdminTrainingsAction.java` before calling `trainingDAO.addTraining()`.

**Recommendation:**
Add server-side date format validation before invoking the DAO. Reject requests where either date fails to parse. Add a business rule check that `expirationDate >= trainingDate`. Call `SimpleDateFormat.setLenient(false)` in `DateUtil.stringToSQLDate` to prevent silent date coercion.

---

### FINDING-08 — LOW: All Execution Branches Return `null` — Forward Contract Violated

**Severity:** LOW
**File:** `src/main/java/com/action/AdminTrainingsAction.java` lines 36, 39, 41
**Category:** Design / Error Handling

**Description:**
Every branch of `execute()` returns `null` instead of a named `ActionForward`. Struts 1 treats a `null` return as "no forward — the action has handled the response itself." The action has not written any response, so the browser receives an empty body with HTTP 200. The declared forwards (`operatortraining`, `success`, `failure`) in struts-config are never used by this action. This design makes error handling invisible to the Struts framework: if the DAO throws, the global exception handler fires, but on success there is no redirect, which breaks normal post-redirect-get patterns and can result in duplicate submissions on browser refresh.

**Evidence:**
```java
// Lines 36, 39, 41 — all return null
case "add":    ... return null;
case "delete": ... return null;
default:       return null;
```
```xml
<!-- struts-config.xml 289-291 — forwards declared but unreachable -->
<forward name="operatortraining" path="OperatorTrainingDefinition"/>
<forward name="success"          path="OperatorTrainingDefinition"/>
<forward name="failure"          path="/adminmenu.do?action=home"/>
```

**Recommendation:**
Return an explicit `ActionForward` on all paths. On success, return `mapping.findForward("success")`. On invalid input or auth failure, return `mapping.findForward("failure")`. This enforces post-redirect-get and ensures the Struts framework and logging infrastructure can observe the outcome of every request.

---

### FINDING-09 — INFO: DAO Instantiated as Instance Field — Shared Across Requests

**Severity:** INFO
**File:** `src/main/java/com/action/AdminTrainingsAction.java` line 15
**Category:** Design

**Description:**
`TrainingDAO` is instantiated as an instance field (`private TrainingDAO trainingDAO = new TrainingDAO()`). In Struts 1, the same `Action` instance is reused across concurrent requests (the framework caches Action instances). If `TrainingDAO` holds any per-request or connection state, this is a thread-safety hazard. Review of the current `TrainingDAO` shows it is stateless (no instance fields holding request data), so this is low-risk in its current form but is a fragile pattern that could introduce concurrency bugs if the DAO is modified in future.

**Evidence:**
```java
// AdminTrainingsAction.java line 15
private TrainingDAO trainingDAO = new TrainingDAO();
```

**Recommendation:**
Instantiate the DAO locally inside `execute()` or use a static utility / singleton pattern consistently across the codebase.

---

## 3. Categories With No Issues

**SQL Injection:** No issues found. All three DAO methods (`getTrainingByDriver`, `addTraining`, `deleteTraining`) use parameterised `PreparedStatement`-style queries with `?` placeholders and typed setter calls (`setLong`, `setDate`). No string concatenation is used in SQL construction within `TrainingDAO`. This is the correct pattern.

**Authentication (sessCompId gate):** The servlet-level `PreFlightActionServlet` check for `sessCompId != null` is active for `/trainings.do` (it is not in the `excludeFromFilter` whitelist). A valid session with `sessCompId` is therefore required to reach `execute()`. The authentication gate itself is functioning. The IDOR finding (FINDING-01) is a separate authorisation concern, not an authentication bypass.

**Data Exposure:** The action does not return data to the client (all branches return `null` with no response body written). No sensitive fields are serialised or echoed back in the action itself.

---

## 4. Finding Summary

| ID | Severity | Category | Title |
|----|----------|----------|-------|
| FINDING-01 | CRITICAL | IDOR / Broken Object-Level Auth | No company-scope check — cross-tenant delete and add |
| FINDING-02 | HIGH | CSRF | No CSRF token on state-changing operations |
| FINDING-03 | HIGH | Input Validation | Struts validation disabled (`validate="false"`), no validation.xml rules |
| FINDING-04 | HIGH | Input Validation / DoS | NullPointerException on null `action` parameter |
| FINDING-05 | MEDIUM | Session Handling | `sessDateFormat` not null-checked — cascading NPE |
| FINDING-06 | MEDIUM | Input Validation | `action` field not restricted to an allowlist |
| FINDING-07 | MEDIUM | Input Validation | Date strings not validated; lenient parsing silently coerces invalid dates |
| FINDING-08 | LOW | Design / Error Handling | All branches return `null` — forward contract violated |
| FINDING-09 | INFO | Design | DAO as instance field in shared Action class |

**Count by severity:**
- CRITICAL: 1
- HIGH: 3
- MEDIUM: 3
- LOW: 1
- INFO: 1
- **Total: 9**
