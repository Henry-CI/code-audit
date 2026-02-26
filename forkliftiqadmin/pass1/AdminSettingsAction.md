# Security Audit: AdminSettingsAction.java
**Audit Run:** audit/2026-02-26-01/
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated Security Review (Pass 1)
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet auth gate, no Spring Security

---

## 1. Reading Evidence

### 1.1 Package and Class
- **File:** `src/main/java/com/action/AdminSettingsAction.java`
- **Package:** `com.action`
- **Class:** `AdminSettingsAction extends org.apache.struts.action.Action`

### 1.2 Public / Protected Methods

| Line | Signature |
|------|-----------|
| 22 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

No other public or protected methods are present.

### 1.3 DAOs / Services Called (within `execute`)

| Line | Call | Nature |
|------|------|--------|
| 43 | `DateFormatDAO.getAll()` | Read-only lookup — no user-supplied params |
| 47 | `CompanyDAO.getInstance()` | Singleton accessor |
| 48 | `dao.getCompanyContactsByCompId(sessCompId, sessUserId, sessionToken)` | Reads company record keyed on session values |
| 53 | `TimezoneDAO.getTimezone(Integer.parseInt(timezone))` | Lookup using **user-supplied** `timezone` form field |
| 59 | `dao.getUserAlert(String.valueOf(sessUserId), "alert", "RedImpactAlert")` | Alert existence check |
| 60 | `dao.getUserAlert(String.valueOf(sessUserId), "sms", "RedImpactSMS")` | Alert existence check |
| 61 | `dao.getUserAlert(String.valueOf(sessUserId), "alert", "DriverDenyAlert")` | Alert existence check |
| 64/66 | `CompanyDAO.addUserSubscription / deleteUserSubscription` | Write — subscription add/remove keyed on `sessUserId` |
| 69/71 | `CompanyDAO.addUserSubscription / deleteUserSubscription` | Write — subscription add/remove keyed on `sessUserId` |
| 74/76 | `CompanyDAO.addUserSubscription / deleteUserSubscription` | Write — subscription add/remove keyed on `sessUserId` |
| 64,69,74 | `SubscriptionDAO.getSubscriptionByName(...)` | Lookup using hard-coded string literals |
| 79 | `dao.updateCompSettings(company)` | **Write** — persists date format, timezone, max session length to `company` table |

### 1.4 Form Class
- **Form bean name (struts-config):** `AdminSettingsActionForm`
- **Java class:** `com.actionform.AdminSettingsActionForm`
- **Fields:** `id`, `dateFormat`, `maxSessionLength`, `action`, `timezone`, `redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`
- **`validate()` method present:** Yes — checks `dateFormat` not blank, `timezone` not blank/zero, `maxSessionLength` not null

### 1.5 Struts-Config Mapping (`struts-config.xml` lines 263–272)

```xml
<action
    path="/settings"
    type="com.action.AdminSettingsAction"
    name="AdminSettingsActionForm"
    scope="request"
    validate="false">
    <forward name="adminsettings" path="/adminmenu.do?action=home"/>
    <forward name="manufacturers" path="/adminmenu.do?action=home"/>
    <forward name="success"       path="/adminmenu.do?action=home"/>
    <forward name="failure"       path="/adminmenu.do?action=home"/>
</action>
```

**Key mapping attributes:**
- `scope="request"` — form is request-scoped (correct)
- `validate="false"` — Struts validator is **disabled** for this action
- No `roles` attribute — no declarative role enforcement in struts-config
- No `input` attribute — if validation were enabled, error redirect would be undefined

---

## 2. Findings

---

### FINDING-01 — CRITICAL: Struts Validation Disabled (`validate="false"`) Despite Form Having a `validate()` Method

**Severity:** CRITICAL
**File:** `src/main/webapp/WEB-INF/struts-config.xml` line 267; `src/main/java/com/action/AdminSettingsAction.java` lines 33–57
**Category:** Input Validation

**Description:**
The `AdminSettingsActionForm.validate()` method checks that `dateFormat` is non-blank, `timezone` is non-blank/non-zero, and `maxSessionLength` is non-null. However, the struts-config mapping sets `validate="false"`, which completely suppresses the Struts framework call to `validate()`. None of those checks are ever executed at the framework level before `execute()` is entered.

Additionally, `AdminSettingsActionForm` is not listed in `validation.xml` (which covers only `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`), so declarative validator rules are also absent.

**Evidence:**
- `struts-config.xml` line 267: `validate="false"`
- `AdminSettingsActionForm.java` lines 33–52: `validate()` method with field checks that are never invoked
- `validation.xml`: no `<form name="AdminSettingsActionForm">` entry
- `AdminSettingsAction.java` line 53: `Integer.parseInt(timezone)` — if `timezone` is blank or non-numeric, a `NumberFormatException` is thrown, propagating as an unhandled exception

**Recommendation:**
Change `validate="true"` in struts-config for the `/settings` mapping and add an `input` attribute pointing to the settings page. Supplement with a `validation.xml` entry for `AdminSettingsActionForm` covering required/integer rules on all numeric fields. Apply whitelist validation inside `execute()` as a defence-in-depth measure before any `Integer.parseInt()` call.

---

### FINDING-02 — CRITICAL: SQL Injection in `TimezoneDAO.getTimezone()` via User-Supplied Form Field

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/TimezoneDAO.java` line 133; called from `AdminSettingsAction.java` line 53
**Category:** SQL Injection

**Description:**
`TimezoneDAO.getTimezone(int tzoneId)` constructs the SQL query by direct string concatenation of the integer parameter:

```java
// TimezoneDAO.java line 133
String sql = "select id,name,zone from timezone where id=" + tzoneId;
```

The integer value originates from `Integer.parseInt(timezone)` at `AdminSettingsAction.java` line 53, where `timezone` is the raw value of the `adminSettingsActionForm.getTimezone()` form field. While `Integer.parseInt()` provides a partial defence (a non-numeric value raises `NumberFormatException` before reaching the DAO), this pattern is still incorrect:

1. The integer conversion is an accident of the call site, not an enforced contract in the DAO itself.
2. Any future code path that calls `getTimezone()` with a value derived from user input without parsing will be directly injectable.
3. With `validate="false"` (FINDING-01), there is no upstream framework gate to guarantee the value is numeric.

**Evidence:**
- `TimezoneDAO.java` line 133: `"select id,name,zone from timezone where id="+tzoneId`
- `AdminSettingsAction.java` line 53: `TimezoneDAO.getTimezone(Integer.parseInt(timezone))`
- `AdminSettingsActionForm.java` line 28: `private String timezone = null;` — raw String from HTTP request

**Recommendation:**
Replace the string-concatenated query with a `PreparedStatement` using a positional parameter (`?`). This is consistent with how all other DAOs in this codebase handle parameterized queries (e.g., `DBUtil.queryForObjects` pattern used in `CompanyDAO`). Example:

```java
// Use PreparedStatement instead
String sql = "select id,name,zone from timezone where id = ?";
// ps.setInt(1, tzoneId);
```

---

### FINDING-03 — HIGH: No CSRF Protection on State-Changing POST

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminSettingsAction.java` lines 22–80; `src/main/webapp/WEB-INF/struts-config.xml` line 263
**Category:** CSRF

**Description:**
The `/settings.do` action performs multiple state-changing database writes when `action.equalsIgnoreCase("savesettings")`: it updates company-level settings (date format, timezone, max session length) and modifies user alert subscriptions. There is no CSRF token check anywhere in this action. The application stack (Struts 1.3.10) has no built-in CSRF protection, and no custom token mechanism (e.g., `saveToken` / `isTokenValid`) is used.

The session token stored at line 41 (`session.getAttribute("sessionToken")`) is passed to the Cognito REST service as a bearer token for identity federation; it is not used as a CSRF synchroniser token — it is never compared to any value in the incoming request.

A cross-origin request forged from any other site or an XSS vector could silently change an admin's company timezone, date format, session length cap, or alert subscriptions.

**Evidence:**
- `AdminSettingsAction.java` line 41: `sessionToken` read from session, passed to DAO at line 48, never validated against request parameter
- `AdminSettingsAction.java` lines 48–79: all writes occur without any token validation
- `struts-config.xml` line 263: no token-validation mechanism configured
- No call to `isTokenValid()` or equivalent anywhere in `execute()`

**Recommendation:**
Implement the Struts `saveToken` / `isTokenValid` synchroniser-token pattern. Generate a token on the GET render of the settings page (`saveToken(request)`) and validate it on POST (`isTokenValid(request, true)`). Redirect to an error page if the token is absent or mismatched. As a structural complement, configure `SameSite=Strict` or `SameSite=Lax` on the session cookie.

---

### FINDING-04 — HIGH: No Role-Based Access Control Check Within the Action

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminSettingsAction.java` lines 22–80
**Category:** Authentication / Authorisation

**Description:**
The authentication gate (`PreFlightActionServlet`) checks only that `sessCompId != null && !sessCompId.equals("")`. It does not verify the user's role. There is no `roles` attribute in the struts-config mapping for `/settings`. The action itself performs no role check — it does not inspect `sessRole`, `sessAuthority`, or the `CompanyBean.getRoles()` result before executing the save branch.

Any authenticated session holder — regardless of whether they are a site admin, a dealer operator, a sub-company user, or any other lower-privilege role — can POST to `/settings.do?action=savesettings` and modify company-wide settings (timezone, date format, max session length) as well as alert subscriptions for the user identified by `sessUserId`.

**Evidence:**
- `PreFlightActionServlet.java` lines 56–59: gate checks only `sessCompId`
- `struts-config.xml` line 263–272: no `roles` attribute on `/settings` mapping
- `AdminSettingsAction.java` lines 30–32: only `sessCompId` and `sessUserId` are read from session; no role attribute is read or checked
- `AdminSettingsAction.java` lines 47–79: all DAO writes proceed unconditionally after the `action.equalsIgnoreCase("savesettings")` branch is entered

**Recommendation:**
Add an explicit role guard at the top of the `execute()` method, checking that the session user holds the required administrative role before any DAO call is made. A reusable `AuthorizationUtil.requireRole(session, RuntimeConf.ROLE_SITEADMIN)` helper (or equivalent) should be introduced and applied consistently. Supplement with a `roles` attribute in the struts-config mapping as an additional layer.

---

### FINDING-05 — HIGH: NullPointerException / Unchecked `.get(0)` on DAO Result — Potential Authentication Bypass via Exception

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminSettingsAction.java` line 48
**Category:** Session Handling / Robustness

**Description:**
`dao.getCompanyContactsByCompId(sessCompId, sessUserId, sessionToken).get(0)` will throw an unchecked `IndexOutOfBoundsException` if the query returns an empty list (e.g., if `sessCompId` or `sessUserId` does not match any row in `company`/`users_cognito`). The exception bubbles up through `execute()` and is caught by the Struts global exception handler mapped to `java.sql.SQLException` — but `IndexOutOfBoundsException` is not a `SQLException`, so it is not caught by the declared global handler.

More critically, the `sessCompId` value is obtained from the session (line 30–31) with a silent fallback to the empty string `""` when the attribute is null, rather than enforcing presence. If `sessCompId` is `""`, the `assert` inside `getCompanyContactsByCompId` (CompanyDAO line 559) fires only if assertions are enabled (they typically are not in production JVMs). The query then runs with an empty string company ID, likely returning zero rows, and `.get(0)` throws.

Meanwhile, line 30–31 also means an unauthenticated request where `session` is not null but `sessCompId` is not set will not be redirected by the auth gate before reaching DAO calls (the gate only redirects when `excludeFromFilter` returns `true` for that path — `/settings.do` passes the filter — but the gate code at line 56 specifically checks `sessCompId == null || sessCompId.equals("")`, which should redirect). The double-blank-string fallback in the action means the action code can be reached with `sessCompId = ""`, which bypasses the intent of the gate and causes DAO failures rather than a clean redirect.

**Evidence:**
- `AdminSettingsAction.java` lines 30–31: `sessCompId` defaulted to `""` on null
- `AdminSettingsAction.java` line 48: `.get(0)` with no null/empty-list guard
- `CompanyDAO.java` line 559: `assert StringUtils.isNotBlank(compId)` — assertions likely disabled in production
- `PreFlightActionServlet.java` lines 56–59: gate checks `sessCompId == null || sessCompId.equals("")` and should redirect — but the action's own fallback to `""` is inconsistent defensive programming

**Recommendation:**
Replace the silent `""` fallback at lines 30–31 with an explicit null check that redirects to the expire/login page immediately. Guard the `.get(0)` result (check `results.isEmpty()` before calling `.get(0)`). Enable Java assertions in production or replace them with explicit `IllegalArgumentException` guards inside the DAO.

---

### FINDING-06 — MEDIUM: User-Supplied `timezone` String Parsed Without Validation Before DAO Call

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSettingsAction.java` line 53
**Category:** Input Validation / Error Handling

**Description:**
`Integer.parseInt(timezone)` is called at line 53 with no prior validation that `timezone` is a non-null, non-empty, numeric string within an expected range. Because `validate="false"` (FINDING-01), the form's `validate()` method does not run. If a user submits a blank or non-numeric `timezone` value, a `NumberFormatException` is thrown. This exception is not a `java.sql.SQLException`, `java.io.IOException`, or `javax.servlet.ServletException` — the three types covered by the global exception handler — so it will propagate as an unhandled exception, potentially resulting in an HTTP 500 with stack trace disclosure (see FINDING-07).

**Evidence:**
- `AdminSettingsAction.java` line 53: `Integer.parseInt(timezone)` where `timezone = adminSettingsActionForm.getTimezone()`
- `AdminSettingsActionForm.java` line 28: `timezone` is a plain `String` with no type constraint
- `struts-config.xml` line 267: `validate="false"`
- `struts-config.xml` lines 42–55: global exception handler covers only `SQLException`, `IOException`, `ServletException`

**Recommendation:**
Validate `timezone` (and `maxSessionLength`) as numeric and within an expected range before any `parseInt` call. Use `StringUtils.isNumeric()` or a try/catch with redirect. Enable `validate="true"` and rely on the form's `validate()` as the primary gate (see FINDING-01).

---

### FINDING-07 — MEDIUM: Stack Trace / Sensitive Information Disclosure via Unhandled Exceptions

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSettingsAction.java` line 26 (`throws Exception`); `src/main/webapp/WEB-INF/struts-config.xml` lines 42–55
**Category:** Data Exposure

**Description:**
The `execute()` method declares `throws Exception`. The global exception handler in struts-config covers only `java.sql.SQLException`, `java.io.IOException`, and `javax.servlet.ServletException`. Runtime exceptions — `NumberFormatException` (FINDING-06), `IndexOutOfBoundsException` (FINDING-05), `NullPointerException` — are not caught and will surface as HTTP 500 responses. Depending on server configuration, the container's default error page may expose a full stack trace, revealing internal class names, DAO method names, SQL query fragments logged just before the failure, and server path information.

`CompanyDAO.updateCompSettings()` also calls `e.printStackTrace()` (line 647) which writes to stdout/stderr in addition to the logger, creating a secondary disclosure vector in hosted environments where stdout is externally accessible.

**Evidence:**
- `AdminSettingsAction.java` line 26: `throws Exception` — no try/catch within `execute()`
- `struts-config.xml` lines 42–55: global handler covers only three exception types
- `CompanyDAO.java` line 647: `e.printStackTrace()`
- `TimezoneDAO.java` line 148: `e.printStackTrace()`

**Recommendation:**
Wrap the body of `execute()` in a try/catch for `Exception`, log at ERROR level, and forward to a generic error page without exposing stack details. Add `RuntimeException` to the global exception handler or introduce a custom Struts `ExceptionHandler`. Remove all `e.printStackTrace()` calls from DAO classes and rely solely on the structured logger.

---

### FINDING-08 — MEDIUM: `maxSessionLength` Accepted Without Range Validation — Privilege Escalation via Session Length Manipulation

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSettingsAction.java` lines 36, 51; `src/main/java/com/actionform/AdminSettingsActionForm.java` line 26
**Category:** Input Validation / Business Logic

**Description:**
`maxSessionLength` is an `Integer` form field that is stored directly into the `CompanyBean` and persisted to the `company` table via `updateCompSettings()`. There is no minimum or maximum boundary check anywhere in the action or the form. An authenticated user with access to this action could:

1. Set `maxSessionLength` to `0` or a negative value, potentially disabling session expiry for all users of the company.
2. Set `maxSessionLength` to an arbitrarily large integer (e.g., `Integer.MAX_VALUE`), effectively creating permanent sessions for all company users.
3. Submit a value that triggers integer overflow in downstream session-management logic.

The form's `validate()` method only checks for null, not for sensible bounds.

**Evidence:**
- `AdminSettingsActionForm.java` line 46–49: only null check, no range validation
- `AdminSettingsAction.java` line 51: `company.setMaxSessionLength(maxSessionLength)` — value taken directly from form
- `CompanyDAO.java` line 639: `ps.setInt(2, compBean.getMaxSessionLength())` — written to DB without bounds enforcement

**Recommendation:**
Add range validation in `AdminSettingsActionForm.validate()`: enforce a positive minimum (e.g., 5 minutes) and a reasonable maximum (e.g., 1440 minutes / 24 hours). Reject zero and negative values. Apply the same check inside `execute()` as defence-in-depth.

---

### FINDING-09 — LOW: Insecure Direct Object Reference (IDOR) — `sessUserId` Governs Alert Subscription Writes Without Cross-Tenant Ownership Check

**Severity:** LOW
**File:** `src/main/java/com/action/AdminSettingsAction.java` lines 59–77
**Category:** IDOR

**Description:**
Alert subscription operations (lines 59–77) are performed for the user identified by `sessUserId`. The action does not verify that `sessUserId` belongs to `sessCompId`. If an attacker can manipulate `sessUserId` in the session (e.g., via session fixation or a separate session-attribute-write vulnerability), they could modify alert subscriptions for arbitrary user IDs. This is a low-severity issue in isolation because `sessUserId` is a session attribute (not a request parameter), but the absence of an ownership join is a structural gap.

**Evidence:**
- `AdminSettingsAction.java` lines 59–61: `getUserAlert(String.valueOf(sessUserId), ...)` — no company-membership check
- `AdminSettingsAction.java` lines 64–77: `addUserSubscription` / `deleteUserSubscription` keyed on `sessUserId` only
- `CompanyDAO.java` lines 862–878: subscription operations use only `userId`, no `compId` join

**Recommendation:**
Before performing subscription writes, verify that the user identified by `sessUserId` is a member of the company identified by `sessCompId` (e.g., query `user_comp_rel` where `user_id = sessUserId AND comp_id = sessCompId`). This also serves as an integrity guard against stale session state.

---

### FINDING-10 — LOW: `sessionToken` Stored in Session and Passed to External REST Service Without Expiry or Revocation Guard

**Severity:** LOW
**File:** `src/main/java/com/action/AdminSettingsAction.java` lines 41, 48
**Category:** Session Handling

**Description:**
`sessionToken` (a Cognito access token) is retrieved from the HTTP session and forwarded to `RestClientService.getUser()` inside `getCompanyContactsByCompId()`. If the Cognito token has expired, the REST call will fail and the resulting exception will propagate unhandled (see FINDING-07). There is no check on token validity or expiry before the call. Additionally, storing a bearer token as a plain session attribute means it will appear in any session serialisation/dump, increasing exposure if the session store is compromised.

**Evidence:**
- `AdminSettingsAction.java` line 41: `sessionToken` read from session
- `AdminSettingsAction.java` line 48: passed directly to `getCompanyContactsByCompId()`
- `CompanyDAO.java` lines 582–588: token used as bearer token against Cognito REST API

**Recommendation:**
Check token expiry before use (Cognito JWTs carry an `exp` claim). Handle `401 Unauthorized` responses from Cognito gracefully by forcing re-authentication rather than propagating the exception. Consider whether the full bearer token needs to be stored in the session or whether a shorter-lived reference is sufficient.

---

### FINDING-11 — INFO: All Four Struts Forwards Route to the Same Destination — No Distinct Failure Path

**Severity:** INFO
**File:** `src/main/webapp/WEB-INF/struts-config.xml` lines 268–271
**Category:** Robustness / Observability

**Description:**
All four named forwards (`adminsettings`, `manufacturers`, `success`, `failure`) map to the identical path `/adminmenu.do?action=home`. This means a save failure (e.g., `updateCompSettings` returning `false` at line 79) is silently swallowed — the user is redirected to the home page with no error indication. Audit logs cannot distinguish a successful save from a failed one based on the forward taken.

**Evidence:**
- `struts-config.xml` lines 268–271: all four forwards → `/adminmenu.do?action=home`
- `AdminSettingsAction.java` line 79: ternary on `updateCompSettings()` result selects between `"success"` and `"failure"` forwards — but both resolve identically

**Recommendation:**
Define distinct forward paths for success and failure. On failure, forward to the settings page with an error message so the user is informed and the failure is distinguishable in access logs.

---

## 3. Category Summary

| Category | Findings | Max Severity |
|----------|----------|--------------|
| Authentication | FINDING-04 (no role check), FINDING-05 (null/empty sessCompId bypass) | HIGH |
| CSRF | FINDING-03 | HIGH |
| Input Validation | FINDING-01 (validate=false), FINDING-06 (parseInt without guard), FINDING-08 (maxSessionLength no bounds) | CRITICAL |
| SQL Injection | FINDING-02 (TimezoneDAO concatenation) | CRITICAL |
| IDOR | FINDING-09 | LOW |
| Session Handling | FINDING-05 (partial), FINDING-10 (Cognito token) | HIGH |
| Data Exposure | FINDING-07 (stack traces) | MEDIUM |
| Robustness / Info | FINDING-11 | INFO |

**No issues found in:** Direct reflected XSS from this action (outputs are session attributes, not written directly to response); use of HTTP verbs (Struts handles GET/POST uniformly, consistent with the rest of the application's pattern).

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 2 | FINDING-01, FINDING-02 |
| HIGH | 3 | FINDING-03, FINDING-04, FINDING-05 |
| MEDIUM | 3 | FINDING-06, FINDING-07, FINDING-08 |
| LOW | 2 | FINDING-09, FINDING-10 |
| INFO | 1 | FINDING-11 |
| **TOTAL** | **11** | |
