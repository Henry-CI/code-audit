# Security Audit: AdminSettingsActionForm
**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**Pass:** 1
**Auditor:** CIG Automated Security Review
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10

---

## 1. Reading Evidence

### 1.1 Package and Class

- **File:** `src/main/java/com/actionform/AdminSettingsActionForm.java`
- **Package:** `com.actionform`
- **Class:** `AdminSettingsActionForm extends ActionForm`
- **serialVersionUID:** `7884549462560104854L`
- **Lombok annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`

### 1.2 Fields

| # | Name | Declared Type | Initial Value |
|---|------|--------------|---------------|
| 1 | `id` | `String` | `null` |
| 2 | `dateFormat` | `String` | `null` |
| 3 | `maxSessionLength` | `Integer` (boxed) | `null` |
| 4 | `action` | `String` | `null` |
| 5 | `timezone` | `String` | `null` |
| 6 | `redImpactAlert` | `String` | `null` |
| 7 | `redImpactSMSAlert` | `String` | `null` |
| 8 | `driverDenyAlert` | `String` | `null` |

### 1.3 validate() Method (lines 33-52)

`validate()` is declared but **never invoked by the framework** because `struts-config.xml` sets `validate="false"` for the `/settings` action mapping (struts-config.xml line 267).

Logic present in `validate()`:
- `dateFormat`: checks for `null` or empty string only — no format/length/whitelist check.
- `timezone`: checks for `null`, empty, or `"0"` only — no numeric range check.
- `maxSessionLength`: checks for `null` only — no range, no upper bound.
- No validation at all for: `id`, `action`, `redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`.

### 1.4 reset() Method

**Absent.** The form does not override `reset()`. Struts 1 does not clear fields between requests without an explicit `reset()` implementation; field values can persist across requests if the framework re-uses the form bean instance (scope="request" mitigates this for this mapping, but no defensive reset is present).

### 1.5 validation.xml Coverage

`src/main/webapp/WEB-INF/validation.xml` defines rules for exactly three forms:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

**`AdminSettingsActionForm` has no entry in validation.xml.** No Commons Validator rules exist for any of its fields.

---

## 2. Findings

---

### FINDING-01

**Severity:** CRITICAL
**Category:** Input Validation — Bypass of All Server-Side Validation
**File:** `src/main/webapp/WEB-INF/struts-config.xml` line 267; `src/main/java/com/actionform/AdminSettingsActionForm.java` lines 33-52

**Description:**
The `/settings` action mapping sets `validate="false"`, which causes the Struts 1 framework to skip the `validate()` method of `AdminSettingsActionForm` entirely on every request. The form's own `validate()` method, even though it performs partial checks, is therefore dead code from a security enforcement perspective. No validation of any kind executes before `AdminSettingsAction.execute()` receives control, meaning all eight form fields arrive at the Action and DAO layer completely unvalidated.

**Evidence:**
```xml
<!-- struts-config.xml line 263-272 -->
<action
    path="/settings"
    type="com.action.AdminSettingsAction"
    name="AdminSettingsActionForm"
    scope="request"
    validate="false">
```
```java
// AdminSettingsActionForm.java line 33 — never called by framework
public ActionErrors validate(ActionMapping mapping, HttpServletRequest request) {
```

**Recommendation:**
Change `validate="false"` to `validate="true"` in struts-config.xml for the `/settings` mapping, add this form to validation.xml with appropriate rules, and ensure the Action-level forward for validation failure (`input` attribute) is configured. Do not rely solely on client-side JavaScript validation in `settings.jsp`.

---

### FINDING-02

**Severity:** HIGH
**Category:** Input Validation — Unconstrained `timezone` Passed to String-Concatenated SQL
**File:** `src/main/java/com/dao/TimezoneDAO.java` line 133; `src/main/java/com/action/AdminSettingsAction.java` line 53

**Description:**
`timezone` is read from the form as a free-form `String` with no length, format, or numeric range validation. In `AdminSettingsAction`, `Integer.parseInt(timezone)` is called (line 53) to pass the value to `TimezoneDAO.getTimezone()`. `TimezoneDAO.getTimezone()` uses string concatenation to build a SQL query:

```java
// TimezoneDAO.java line 133
String sql = "select id,name,zone from timezone where id=" + tzoneId;
```

Although `Integer.parseInt()` will throw `NumberFormatException` for non-numeric input (preventing classic SQL injection through this specific path), the exception is unhandled in `AdminSettingsAction` and will propagate as an uncaught `Exception`, potentially leaking stack trace information. More importantly, the pattern itself is architecturally dangerous: if the `parseInt` guard were ever removed or bypassed, or if similar concatenation is used elsewhere with the raw `String` value, SQL injection would result. The root cause is the absence of a whitelist/numeric range constraint on the form field.

**Evidence:**
```java
// AdminSettingsAction.java line 53
TimezoneBean tzone = TimezoneDAO.getTimezone(Integer.parseInt(timezone));
```
```java
// TimezoneDAO.java line 133
String sql = "select id,name,zone from timezone where id=" + tzoneId;
```

**Recommendation:**
Validate `timezone` server-side as a positive integer within the known range of timezone table IDs before use. Replace the string-concatenated query in `TimezoneDAO.getTimezone()` with a `PreparedStatement` parameterised query. Handle `NumberFormatException` explicitly to avoid uncontrolled exception propagation.

---

### FINDING-03

**Severity:** HIGH
**Category:** Input Validation — `maxSessionLength` Has No Upper Bound; Denial-of-Service via Extreme Value
**File:** `src/main/java/com/actionform/AdminSettingsActionForm.java` lines 46-49; `src/main/java/com/dao/CompanyDAO.java` line 639

**Description:**
`maxSessionLength` is declared as `Integer` (boxed) and is only checked for `null` in the (dead) `validate()`. No minimum or maximum value is enforced server-side. The client-side check in `settings.jsp` (line 148) enforces a minimum of 15 minutes but is trivially bypassable by submitting the form directly. An authenticated admin could set `maxSessionLength` to `Integer.MAX_VALUE` (2,147,483,647 minutes, approximately 4,000 years), effectively creating permanent sessions for all users of the company. This is a privilege-abuse / denial-of-session-expiry risk rather than a classic DoS, but it undermines the security control the field is meant to enforce.

**Evidence:**
```java
// AdminSettingsActionForm.java lines 46-49 — only null check, in dead code
if (this.maxSessionLength == null) {
    ActionMessage message = new ActionMessage("error.max_session_length");
    errors.add("maxSessionLength", message);
}
```
```java
// CompanyDAO.java line 639 — persisted directly
ps.setInt(2, compBean.getMaxSessionLength());
```
Client-side only guard (bypassable):
```javascript
// settings.jsp line 148
if (document.AdminSettingsActionForm.maxSessionLength.value < 15) {
```

**Recommendation:**
Add server-side range validation (e.g., 15 to 1440 minutes, or a domain-appropriate upper limit) in both `validate()` — once it is re-enabled — and as a guard in `AdminSettingsAction.execute()`. Do not rely on the client-side check.

---

### FINDING-04

**Severity:** HIGH
**Category:** Input Validation — `dateFormat` Is Unconstrained; No Whitelist Check Against Known-Good Values
**File:** `src/main/java/com/actionform/AdminSettingsActionForm.java` lines 37-40; `src/main/java/com/dao/CompanyDAO.java` line 638

**Description:**
`dateFormat` is validated only for non-null/non-empty in the dead `validate()` method. No check is performed to confirm the submitted value is one of the known-good formats returned by `DateFormatDAO.getAll()`. The value is written directly into the `date_format` database column via a parameterised statement (`ps.setString(1, compBean.getDateFormat())`), so SQL injection is not the immediate concern. However, the field is later read from the session and used in date-formatting operations throughout the application (e.g., `DateUtil.getDateFormatFromDateTimeFormat(dateFormat)` at `AdminSettingsAction.java` line 57). An arbitrary format string could cause `SimpleDateFormat` parsing exceptions, corrupt session state, or, depending on how format strings are used in templates, be reflected to other users of the same company.

**Evidence:**
```java
// AdminSettingsActionForm.java lines 37-40
if (this.dateFormat == null || this.dateFormat.equals("")) {
    ActionMessage message = new ActionMessage("error.date_format");
    errors.add("dateFormat", message);
}
```
```java
// AdminSettingsAction.java line 56-57
session.setAttribute("sessDateTimeFormat", dateFormat);
session.setAttribute("sessDateFormat", DateUtil.getDateFormatFromDateTimeFormat(dateFormat));
```
```java
// CompanyDAO.java line 638
ps.setString(1, compBean.getDateFormat());
```

**Recommendation:**
Server-side whitelist validation: confirm the submitted `dateFormat` value exactly matches one of the values returned by `DateFormatDAO.getAll()` before storing or placing in session. Reject any value not present in the whitelist.

---

### FINDING-05

**Severity:** HIGH
**Category:** CSRF — No Anti-CSRF Token on State-Changing Action
**File:** `src/main/webapp/html-jsp/settings/settings.jsp` lines 16-131; `src/main/java/com/action/AdminSettingsAction.java` lines 22-80

**Description:**
The settings form (`settings.jsp`) POSTs to `/settings.do` and modifies persistent company settings (date format, timezone, session length) and user subscription preferences (alert subscriptions). There is no CSRF token in the form or validated in the Action. A `sessionToken` attribute is read from the session (line 41 in `AdminSettingsAction`) but is used only as an API bearer token for Cognito calls, not as a CSRF nonce validated against the form submission. Struts 1.3.10 has no built-in CSRF protection. A cross-site request can force a logged-in admin to silently modify their company's security settings.

**Evidence:**
```java
// AdminSettingsAction.java line 41 — token read but NOT validated as CSRF guard
String sessionToken = session.getAttribute("sessionToken") == null ? "" : (String) session.getAttribute("sessionToken");
```
No `<html:hidden property="csrfToken"/>` or equivalent is present in `settings.jsp`. The form action gate at line 45 checks only `action.equalsIgnoreCase("savesettings")`, which is also a form field an attacker controls.

**Recommendation:**
This is documented as a structural gap for the stack. The minimum mitigation within Struts 1 is: generate a per-session or per-request nonce, embed it as a hidden field in the form, validate it server-side in `AdminSettingsAction` before processing. Consider the `SynchronizerToken` utility provided by Struts 1 (`Action.saveToken()` / `Action.isTokenValid()`).

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Input Validation — `id` Field Is Declared on the Form but Ignored in the Action
**File:** `src/main/java/com/actionform/AdminSettingsActionForm.java` line 24; `src/main/java/com/action/AdminSettingsAction.java` lines 30-31

**Description:**
The form declares a `String id` field (line 24). It is never read in `AdminSettingsAction.execute()`. The company identity for the DB update is sourced correctly from the session (`sessCompId`, line 30). However, the exposed `id` setter on the form (generated by Lombok `@Setter`) means any client may POST an arbitrary value for `id`. While it is not used in this Action, its presence creates confusion and a latent risk: if a future developer reads `adminSettingsActionForm.getId()` instead of the session attribute, it would introduce a direct IDOR vulnerability. The field should be removed or made read-only if it serves no function.

**Evidence:**
```java
// AdminSettingsActionForm.java line 24
private String id = null;
// AdminSettingsAction.java line 30 — correct: reads from session, not form
String sessCompId = (String)(session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
```

**Recommendation:**
Remove the `id` field from the form entirely if it is not required. If it is needed for display, mark it as not populated from HTTP request parameters. Document that company identity must always be derived from the authenticated session.

---

### FINDING-07

**Severity:** MEDIUM
**Category:** Input Validation — Alert Flag Fields Accept Arbitrary String; Logic Depends on Exact Value Match
**File:** `src/main/java/com/action/AdminSettingsAction.java` lines 38-40, 63-77

**Description:**
`redImpactAlert`, `redImpactSMSAlert`, and `driverDenyAlert` are declared as unconstrained `String` fields. The Action logic branches on exact equality with `"on"` or `""`. An HTML checkbox that is checked sends `"on"`; unchecked sends nothing (field absent, Struts binds to `""`). However, because these are free-form strings on the form, a client submitting any value other than `"on"` or `""` (e.g., `"true"`, `"yes"`, `"1"`, or any other string) will cause both branches of each `if/else if` to be skipped silently. This means an attacker could submit an unexpected value to cause subscription state to be left unchanged regardless of the intended UI action, or to probe the branching logic.

**Evidence:**
```java
// AdminSettingsAction.java lines 63-67
if (redImpactAlert.equals("on") && alertBean.getAlert_id() == null) {
    CompanyDAO.addUserSubscription(...);
} else if (redImpactAlert.equals("")) {
    CompanyDAO.deleteUserSubscription(...);
}
```

**Recommendation:**
Whitelist-validate each alert flag server-side: accept only `"on"` or `""` (or convert to `boolean`). Treat any other value as invalid and return an error or coerce to a safe default.

---

### FINDING-08

**Severity:** MEDIUM
**Category:** Type Safety — `Integer.parseInt(timezone)` on Unvalidated String; Unhandled Exception
**File:** `src/main/java/com/action/AdminSettingsAction.java` line 53

**Description:**
`timezone` is a `String` field with no server-side numeric validation. `AdminSettingsAction` calls `Integer.parseInt(timezone)` directly. If a non-numeric value is submitted (possible because `validate="false"` suppresses all framework validation), a `NumberFormatException` is thrown and propagates uncaught from `execute()`. Struts 1 will typically catch this as an unhandled `Exception` and render a generic error page, but the stack trace may be logged or exposed to the user depending on error page configuration. The same risk applies to `Integer.parseInt(compBean.getId())` inside `CompanyDAO.updateCompSettings()` (CompanyDAO.java line 641), though `id` there comes from the session-loaded `CompanyBean`.

**Evidence:**
```java
// AdminSettingsAction.java line 53
TimezoneBean tzone = TimezoneDAO.getTimezone(Integer.parseInt(timezone));
```

**Recommendation:**
Validate `timezone` as a non-null, non-empty, parseable positive integer before calling `parseInt`. Use a try/catch with a user-facing error message rather than allowing unhandled exception propagation.

---

### FINDING-09

**Severity:** LOW
**Category:** Sensitive Fields — `action` Field Is User-Controlled Gate
**File:** `src/main/java/com/action/AdminSettingsAction.java` line 45

**Description:**
The form contains a hidden `action` field set to `"savesettings"` in the JSP. `AdminSettingsAction` gates the entire save operation on `action.equalsIgnoreCase("savesettings")`. The `action` field is a user-controlled string with no validation. While this is a weak gate rather than a security control (the same endpoint is used for both load and save), if a request is crafted without the `action` field the Action returns the settings page view without saving, which is safe. The risk is that this pattern could mislead developers into treating the `action` field as a security boundary rather than a UX routing hint.

**Evidence:**
```java
// AdminSettingsAction.java line 45
if (!action.equalsIgnoreCase("savesettings")) return mapping.findForward("adminsettings");
```
```jsp
<!-- settings.jsp line 21 -->
<html:hidden property="action" value="savesettings"/>
```

**Recommendation:**
Document that the `action` field is a routing hint only, not a security control. Consider using separate Struts action mappings for load vs. save rather than a discriminating field.

---

### FINDING-10

**Severity:** LOW
**Category:** Data Integrity — Missing `reset()` Method
**File:** `src/main/java/com/actionform/AdminSettingsActionForm.java`

**Description:**
`AdminSettingsActionForm` does not override `reset()`. For `scope="request"` mappings (as configured here), Struts 1 creates a new form instance per request, which mitigates the stale-value risk for most fields. However, the absence of `reset()` is a latent defect: if the scope were ever changed to `session`, field values from a previous request would persist into subsequent requests, potentially allowing one submission's values to silently carry over. As a defence-in-depth measure, `reset()` should always be implemented on ActionForms.

**Recommendation:**
Implement `reset()` to set all fields to `null` (or safe defaults). This eliminates the risk if scope is changed in future and is a Struts 1 best practice.

---

### FINDING-11

**Severity:** INFO
**Category:** Validation Coverage Gap
**File:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
`validation.xml` contains rules for only three forms (`loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm`). `AdminSettingsActionForm` has no entry. Even if `validate="false"` were corrected, Commons Validator rules would still be absent. This represents a gap in the declarative validation layer.

**Recommendation:**
Add a `<form name="AdminSettingsActionForm">` block to `validation.xml` with at minimum `required` and appropriate type/range rules for `dateFormat`, `timezone`, and `maxSessionLength`.

---

## 3. Category Summary

| Category | Verdict |
|----------|---------|
| Input Validation | MULTIPLE ISSUES — see F-01, F-02, F-03, F-04, F-07, F-08 |
| Type Safety | ISSUE — see F-08 |
| IDOR Risk | LATENT — `id` field on form is dead but dangerous; see F-06 |
| Sensitive Fields | NO sensitive credential fields exposed on this form. `action` field misuse noted (F-09, LOW). |
| Data Integrity | ISSUE — missing `reset()` (F-10); `maxSessionLength` unbounded (F-03) |
| CSRF | STRUCTURAL GAP — no token on state-changing POST; see F-05 |
| validation.xml Coverage | GAP — form absent from validation.xml; see F-11 |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | F-01 |
| HIGH | 4 | F-02, F-03, F-04, F-05 |
| MEDIUM | 3 | F-06, F-07, F-08 |
| LOW | 2 | F-09, F-10 |
| INFO | 1 | F-11 |
| **TOTAL** | **11** | |
