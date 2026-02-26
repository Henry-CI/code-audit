# Security Audit Report: AdminRegisterAction.java

**Audit Run:** audit/2026-02-26-01/
**Auditor:** Claude (claude-sonnet-4-6)
**Date:** 2026-02-26
**Pass:** 1

---

## Reading Evidence

### Package + Class
- **File:** `src/main/java/com/action/AdminRegisterAction.java`
- **Package:** `com.action`
- **Class:** `AdminRegisterAction extends org.apache.struts.action.Action`

### Public / Protected Methods with Line Numbers

| Line | Modifier | Signature |
|------|----------|-----------|
| 39 | `public` | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` |
| 303 | `private` | `isValidEmailAddress(String email)` |

### DAOs / Services Called

| Caller Line | Class | Method | Action Scope |
|-------------|-------|--------|--------------|
| 73 | `CompanyDAO` (singleton) | `getInstance()` | All branches |
| 74 | `SubscriptionDAO` (new instance) | `saveDefualtSubscription(int)` | register path |
| 170 | `CompanyDAO` | `saveCompInfo(CompanyBean, String)` | register |
| 195 | `CompanyDAO` | `saveSubCompInfo(String sessCompId, CompanyBean)` | add |
| 202 | `LoginDAO` | `getCompanies(Boolean, Boolean, String, String, int)` | add (superAdmin/dealer) |
| 204 | `CompanyDAO` | `getCompanyContactsByCompId(String, int, String)` | add |
| 248 | `CompanyDAO` | `updateCompInfo(CompanyBean, int, String)` | update |
| 250/258 | `CompanyDAO` | `getCompanyContactsByCompId(String, int, String)` | update |
| 256 | `LoginDAO` | `getCompanies(Boolean, Boolean, String, String, int)` | update (superAdmin/dealer) |
| 117/130 | `RestClientService` | `signUpRequest(UserSignUpRequest)` | register/add |
| 178 | `Util` | `sendMail(...)` | register success |

### Form Class
- `com.actionform.AdminRegisterActionForm extends org.apache.struts.validator.ValidatorForm`
- Fields: `id`, `name`, `address`, `postcode`, `email`, `contact_no`, `contact_fname`, `contact_lname`, `password`, `pin`, `refnm`, `refno`, `question`, `answer`, `code`, `accountAction`, `unit`, `subemail`, `timezone`, `lan_id`, `mobile`

### Struts-Config Mapping
File: `src/main/webapp/WEB-INF/struts-config.xml`, lines 144–157:
```xml
<action
    path="/adminRegister"
    name="adminRegActionForm"
    scope="request"
    type="com.action.AdminRegisterAction"
    validate="true"
    input="adminRegiserDefinition">
  <forward name="successregister" path="successRegisterDefinition"/>
  <forward name="successadd"      path="/dealercompanies.do"/>
  <forward name="successupdate"   path="/adminmenu.do?action=home"/>
  <forward name="failure"         path="adminRegiserDefinition"/>
  <forward name="failUpdate"      path="/adminmenu.do?action=home"/>
  <forward name="failAdd"         path="/dealercompanies.do"/>
</action>
```

**Critical note on form-bean name mismatch:** The action mapping references `name="adminRegActionForm"`, which is defined in struts-config.xml line 24 as:
```xml
<form-bean name="adminRegActionForm" type="com.actionform.AdminRegisterActionForm"/>
```
The validation.xml rules are declared under `<form name="adminRegisterActionForm">` (line 32 of validation.xml) — a **different name**. The form-bean actually bound to this action is `adminRegActionForm`, not `adminRegisterActionForm`. This means the validation.xml rules never fire for this action (see finding V-1 below).

### Validation.xml Rules for `adminRegisterActionForm`
File: `src/main/webapp/WEB-INF/validation.xml`, lines 32–58:

| Field | Rules | Constraints |
|-------|-------|-------------|
| `name` | required, minlength | min 3 characters |
| `contact_name` | required | — |
| `email` | required, email | — |
| `contact_no` | integer | — |
| `password` | required, minlength | min 4 characters |

Fields **not** covered by any rule: `address`, `postcode`, `contact_fname`, `contact_lname`, `pin`, `refnm`, `refno`, `question`, `answer`, `code`, `accountAction`, `unit`, `subemail`, `timezone`, `lan_id`, `mobile`

---

## Authentication Analysis

`adminRegister.do` is confirmed in the `excludeFromFilter` exclusion list at line 107 of `PreFlightActionServlet.java`:
```java
else if (path.endsWith("adminRegister.do")) return false;
```
When `excludeFromFilter` returns `false`, the authentication check (sessCompId != null) is **skipped**. This endpoint is fully publicly accessible — no session, no credentials required.

The action handles three `accountAction` values: `register`, `add`, and `update`. Only `register` is the intended public self-registration flow. The `add` and `update` paths perform privileged operations (sub-company creation and company profile update) but rely on session attributes (`sessCompId`, `sessAccountId`, `sessUserId`, `sessionToken`, `isSuperAdmin`, `isDealerLogin`) rather than enforcing authentication at the action level.

---

## Findings

### FINDING AUTH-1 — CRITICAL: Unauthenticated Access to Privileged `add` and `update` Branches

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 76, 194, 246
**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java`, line 107

**Description:**
The `adminRegister.do` endpoint is on the auth exclusion list, making it reachable without any session. The action's `execute` method processes three branches based on the `accountAction` form parameter: `register` (intended public path), `add` (create a sub-company), and `update` (modify company profile). Both `add` and `update` are privileged operations. An unauthenticated attacker can POST `accountAction=add` or `accountAction=update` to invoke these code paths.

**Evidence:**
- `PreFlightActionServlet.java` line 107: `else if (path.endsWith("adminRegister.do")) return false;` — skips auth check.
- `AdminRegisterAction.java` line 76: `if (accountAction.equalsIgnoreCase("register") || accountAction.equalsIgnoreCase("add"))` — `add` runs in the same unauthenticated-accessible branch as `register`.
- `AdminRegisterAction.java` line 246: `else if (accountAction.equalsIgnoreCase("update"))` — `update` is similarly reachable.
- For `add`: line 195 calls `compDao.saveSubCompInfo(sessCompId, companybean)` — `sessCompId` will be empty string (line 42 default) when there is no session, likely causing a DB error, but the code path is still reached and attempted.
- For `update`: line 248 calls `compDao.updateCompInfo(companybean, sessUserId, sessionToken)` — with empty/zero session values from unauthenticated context.

**Impact:**
An unauthenticated attacker can attempt to invoke sub-company creation and company update operations. Even if the DAO calls fail due to empty session values, this represents an unintended attack surface. If future session handling changes (e.g., a session created elsewhere) allow the operation to proceed, it becomes a full unauthenticated company manipulation vulnerability.

**Recommendation:**
Split the `add` and `update` flows into a separate action class (e.g., `AdminCompanyManageAction.java`) that is **not** on the exclusion list, so they are protected by the `sessCompId` auth gate. Alternatively, add an explicit session authentication guard at the top of the `execute` method before processing `add` or `update` branches:
```java
if (accountAction.equalsIgnoreCase("add") || accountAction.equalsIgnoreCase("update")) {
    if (session == null || session.getAttribute("sessCompId") == null
            || session.getAttribute("sessCompId").toString().isEmpty()) {
        response.sendError(HttpServletResponse.SC_UNAUTHORIZED);
        return null;
    }
}
```

---

### FINDING AUTH-2 — HIGH: NullPointerException Risk on Unauthenticated Requests (session=null)

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 40–45

**Description:**
The action calls `request.getSession(false)` (line 40), which returns `null` if no session exists. The subsequent reads on lines 42–45 check for null on `session.getAttribute(...)`, but only after calling the method on `session` itself. If `session` is `null`, all four lines throw a `NullPointerException`.

**Evidence:**
```java
HttpSession session = request.getSession(false);                    // line 40 - can be null

String sessCompId = session.getAttribute("sessCompId") == null ? "" // line 42 - NPE if session==null
int sessAccountId = session.getAttribute("sessAccountId") == null ? 0 // line 43
int sessUserId = session.getAttribute("sessUserId") == null ? 0     // line 44
String sessionToken = session.getAttribute("sessionToken") == null ? "" // line 45
```

Since `adminRegister.do` is publicly accessible, any unauthenticated GET/POST with no prior session will cause an NPE at line 42. The exception is caught by the catch block at line 234 (`e.printStackTrace()`) and the action returns a generic `failure` forward, but the stack trace is printed to server output, and the request fails non-gracefully.

**Recommendation:**
Guard against a null session before accessing its attributes:
```java
HttpSession session = request.getSession(false);
if (session == null) {
    session = request.getSession(true); // create one for register path only
}
```
Or use safe null checks: `session != null ? session.getAttribute("sessCompId") : null`.

---

### FINDING V-1 — CRITICAL: Validation.xml Rules Never Execute Due to Form-Bean Name Mismatch

**Severity:** CRITICAL
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 24, 146
**File:** `src/main/webapp/WEB-INF/validation.xml`, line 32

**Description:**
The action mapping binds to form-bean name `adminRegActionForm` (struts-config.xml line 146). The form-bean `adminRegActionForm` is declared at line 24 of struts-config.xml:
```xml
<form-bean name="adminRegActionForm" type="com.actionform.AdminRegisterActionForm"/>
```
However, the validation.xml rules are declared for `<form name="adminRegisterActionForm">` (note: `Register` vs `Reg`). The Struts Validator plugin matches validation rules to actions by the form-bean **name** attribute used in the action mapping. Because the action uses `adminRegActionForm` and no rule set exists for that name, **zero validation rules are applied** when `validate="true"` is processed by Struts.

The action mapping does have `validate="true"` set, giving a false sense of security that declarative validation is active.

**Evidence:**
- struts-config.xml line 24: `<form-bean name="adminRegActionForm" .../>` — name used by the action.
- struts-config.xml line 11: `<form-bean name="adminRegisterActionForm" .../>` — a separately declared form-bean with the matching validation.xml name, but not used by this action.
- struts-config.xml line 146: `name="adminRegActionForm"` — action binding.
- validation.xml line 32: `<form name="adminRegisterActionForm">` — validator looks for this name; no match for `adminRegActionForm`.

**Impact:**
No declarative validation of any kind runs on submitted form data. The following fields arrive in the action with no pre-validated constraints: `name`, `email`, `contact_no`, `password`, `pin`, and all others. The action performs only three manual checks (lines 89–98): name not blank, email not blank + regex check, pin not blank. All other fields (address, postcode, refnm, refno, question, answer, timezone, lan_id, mobile, subemail, unit, contact_fname, contact_lname) are passed directly to DAO calls with no validation whatsoever. This is reachable by unauthenticated attackers.

**Recommendation:**
Rename the validation.xml form entry from `adminRegisterActionForm` to `adminRegActionForm` to match the form-bean name used by the action:
```xml
<form name="adminRegActionForm">
```
Verify that the action mapping uses the corrected name consistently. Additionally expand the validation rules to cover all input fields used in DB operations.

---

### FINDING V-2 — HIGH: `pin` Field Has No Minimum Length or Complexity Enforcement

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 95–98
**File:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
The form field `pin` is used as the Cognito authentication password (line 121: `.password(adminRegisterActionForm.getPin())`) and is written as the company PIN credential. The only validation in the action is a blank check (line 95: `adminRegisterActionForm.getPin().trim().equals("")`). Even if validation.xml were correctly wired, `pin` is not declared in its rule set at all — only `password` is. There is no length minimum, no complexity requirement, and no maximum length cap on `pin`.

**Evidence:**
- Line 121: `UserSignUpRequest.builder()...password(adminRegisterActionForm.getPin())...` — pin is submitted directly to Cognito as the user's password.
- Line 176: `"Password:" + adminRegisterActionForm.getPin()` — pin is echoed in confirmation email.
- validation.xml: `pin` field has no rule entry; only `password` has a 4-character minlength rule (which itself does not fire, per V-1).

**Impact:**
An attacker can register accounts with single-character or trivially guessable PINs. The confirmation email (finding DE-1) then exposes this weak credential in plaintext.

**Recommendation:**
Add server-side pin validation enforcing a minimum length of 8 characters and basic complexity. Remove pin/password from email content (see DE-1).

---

### FINDING V-3 — MEDIUM: No Input Length Caps on Any Field — DoS / Oversized Payload Risk

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 54–71
**File:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
The form fields `address`, `postcode`, `refnm`, `refno`, `question`, `answer`, `unit`, `subemail`, `timezone`, `lan_id`, `mobile`, `contact_fname`, `contact_lname` are not constrained by any maximum length validation. They are assigned directly into `CompanyBean` and passed to DAO methods which use parameterised queries that will relay the full string to the database. Large inputs may exceed column constraints (causing SQL errors), consume excessive memory during processing, or be forwarded as oversized payloads to the external Cognito REST service.

**Recommendation:**
Add `maxlength` validation rules in validation.xml for all string fields that map to database columns. Enforce database column width constraints at the application layer.

---

### FINDING V-4 — MEDIUM: `accountAction` Parameter is Attacker-Controlled with No Allowlist Validation

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 48, 76, 194, 246

**Description:**
The `accountAction` form field drives which code branch executes (`register`, `add`, `update`). This value is read directly from the form (line 48) and passed through a series of `equalsIgnoreCase` comparisons. There is no allowlist check before use, no null guard, and no trimming. If `accountAction` is `null`, the `equalsIgnoreCase` call at line 76 throws a `NullPointerException`. If it is an unexpected value, the else branch at line 292 returns a `failure` forward, but not before all `CompanyBean` fields have been populated from form input (lines 54–71).

**Evidence:**
```java
String accountAction = adminRegisterActionForm.getAccountAction(); // line 48 - can be null
...
if (accountAction.equalsIgnoreCase("register") || ...) // line 76 - NPE if null
```

**Recommendation:**
Validate `accountAction` against a strict allowlist immediately after reading it, before any bean population:
```java
if (accountAction == null || !Arrays.asList("register","add","update").contains(accountAction.toLowerCase())) {
    return mapping.findForward("failure");
}
```

---

### FINDING SQL-1 — CRITICAL: SQL Injection in `CompanyDAO.checkExist` and `CompanyDAO.checkUserExit`

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/CompanyDAO.java`, lines 363–379 (`checkExist`) and lines 382–394 (`checkUserExit`)

**Description:**
Both methods construct SQL strings by direct string concatenation of attacker-controlled values. `checkExist` accepts `name` (user input) and `dbField` (a column name selector) without sanitization. `checkUserExit` similarly concatenates `name` and `dbField`. While these methods are not called directly from `AdminRegisterAction.execute()`, they exist in the same DAO used by this action and are callable from other actions that process the same form data. Given that CompanyDAO is a singleton, these methods pose systemic risk.

**Evidence (CompanyDAO.java):**
```java
// line 367
String sql = "select id from company where " + dbField + " ='" + name + "'";
if (!compId.equalsIgnoreCase("")) {
    sql += " and id != " + compId;   // line 369 - second injection point
}

// line 385
String sql = "select id from users where " + dbField + " ='" + name + "'";
if (!id.equalsIgnoreCase("")) {
    sql += " and id != " + id;       // line 387 - second injection point
}
```

**Recommendation:**
Replace with parameterized queries. Since `dbField` is used as a column name (not a value), it must be validated against an explicit allowlist of known column names before inclusion in any SQL string. The value parameter `name` must always be bound as a prepared statement parameter.

---

### FINDING SQL-2 — HIGH: SQL Injection in `CompanyDAO.checkCompExist`

**Severity:** HIGH
**File:** `src/main/java/com/dao/CompanyDAO.java`, lines 396–432

**Description:**
The `checkCompExist` method constructs an SQL query by concatenating values from `CompanyBean` fields (`name`, `email`, `question`, `answer`) using string concatenation. The `question` and `answer` fields originate from user form input and flow into this query without sanitization.

**Evidence:**
```java
// lines 408–418
String sql = "select id from company where name = '" + companyBean.getName()
           + "' and email = '" + companyBean.getEmail() + "'";
if (!companyBean.getQuestion().equalsIgnoreCase("")) {
    sql += " and question ilike '" + companyBean.getQuestion() + "'";
} else { ... }
if (!companyBean.getAnswer().equalsIgnoreCase("")) {
    sql += " and answer = '" + companyBean.getAnswer() + "'";
}
```

**Recommendation:**
Replace all string concatenation with prepared statement parameter binding.

---

### FINDING SQL-3 — HIGH: SQL Injection in `SubscriptionDAO.saveDefualtSubscription`

**Severity:** HIGH
**File:** `src/main/java/com/dao/SubscriptionDAO.java`, lines 122–151

**Description:**
The `saveDefualtSubscription` method is called directly from `AdminRegisterAction.java` line 172 on the public `register` path. It inserts `compId` (an integer derived from a database sequence) directly into a SQL string via concatenation, then executes it via a `Statement` rather than a `PreparedStatement`.

**Evidence:**
```java
// line 133
String sql = "insert into company_subscription (comp_id,subscription_id) select "
           + compId + ", id from subscription where frequency is not null";
stmt.execute(sql);
```

**Mitigating factor:** `compId` is an internally generated integer from a database sequence (`company_id_seq`), not directly from user input. However, the pattern is unsafe — if the source of `compId` ever changes, this becomes directly exploitable. The use of a raw `Statement` rather than `PreparedStatement` is also a code quality defect.

**Recommendation:**
Rewrite using a `PreparedStatement` with `?` binding:
```java
String sql = "insert into company_subscription (comp_id,subscription_id) "
           + "select ?, id from subscription where frequency is not null";
```

---

### FINDING DE-1 — HIGH: Plaintext Password Transmitted in Registration Confirmation Email

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 173–178

**Description:**
Upon successful registration, the action constructs an email body containing the user's plaintext username (email) and password (pin), then sends it to the registering user via `Util.sendMail`. This is a critical credential exposure pattern: the password is stored in email infrastructure (mail servers, spam filters, user mailboxes) where it may be retained indefinitely in plaintext.

**Evidence:**
```java
String content = "Your account has been registered succesfully in ForklfitIQ360 and can be used on the Portal Website.<br/>"
        + "Username:" + adminRegisterActionForm.getEmail() + "<br/>"
        + "Password:" + adminRegisterActionForm.getPin();    // line 176

Util.sendMail(RuntimeConf.REGISTER_SUBJECT, content, "", adminRegisterActionForm.getEmail(), "", RuntimeConf.emailFrom);
```

**Recommendation:**
Remove the `Password:` line from the email content entirely. If a credential reminder is required, implement a secure one-time-link mechanism or instruct users to use the password reset flow.

---

### FINDING DE-2 — MEDIUM: Full Cognito Error Messages Reflected to User

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 134–148, 150–164

**Description:**
When the Cognito sign-up or update API returns an error, the raw error message string from the external service response is passed directly into an `ActionMessage` and surfaced to the user via the `error.cognito` message key.

**Evidence:**
```java
// lines 134–137
String errormsg = signUpResponse.getMessage();
ActionMessage msg = new ActionMessage("error.cognito", errormsg);
```
```java
// lines 150–153
String errormsg = signUpResponse.getMessage();
ActionMessage msg = new ActionMessage("error.cognito", errormsg);
```

**Impact:**
Cognito error messages may reveal internal service identifiers, account existence (e.g., "User already exists" is already explicitly checked at line 133 and shown), API versioning details, or internal AWS infrastructure references. The explicit "User already exists" check at line 133 is itself an account enumeration vector (see AE-1).

**Recommendation:**
Map Cognito error codes to generic, user-safe messages. Never pass raw third-party API error strings to UI output.

---

### FINDING AE-1 — MEDIUM: Account Enumeration via Cognito "User already exists" Response

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 133–148

**Description:**
The code explicitly checks if the Cognito response message contains "User already exists" and returns a distinct error path/message. This allows an unauthenticated attacker to enumerate registered email addresses by submitting registration attempts — a `register` response containing this error message confirms that the email is already registered in Cognito.

**Evidence:**
```java
if(signUpResponse.getMessage() != null && signUpResponse.getMessage().contains("User already exists")) {
    String errormsg = signUpResponse.getMessage();
    ActionMessage msg = new ActionMessage("error.cognito", errormsg);
    ...
    return mapping.findForward("failure");
}
```

**Recommendation:**
Return a uniform message for all registration failures (e.g., "Registration could not be completed. Please check your details and try again.") without differentiating between "user exists" and other error conditions. Implement rate limiting on the `adminRegister.do` endpoint to reduce enumeration throughput.

---

### FINDING CSRF-1 — HIGH: No CSRF Protection on State-Changing Public Endpoint

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminRegisterAction.java` (all state-changing branches)
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 144–157

**Description:**
As noted in the stack brief, CSRF protection is a structural gap across the application. For this action specifically, the `register` path creates new company accounts and Cognito users, and the `add`/`update` paths modify company data. None of these state-changing operations verify a CSRF token. Since `adminRegister.do` is publicly accessible, even standard same-origin CSRF defenses based on session cookies do not apply here — there is no session requirement at all.

**Recommendation:**
For the `register` path: implement a challenge-response mechanism (e.g., CAPTCHA or a time-limited, server-generated form token) to prevent automated or cross-origin form submissions.
For the `add` and `update` paths: address AUTH-1 first (move to authenticated-only endpoint), then apply a synchronizer token CSRF mitigation consistent with the rest of the application's CSRF remediation plan.

---

### FINDING IDOR-1 — INFO: Potential IDOR in `add` Path — sessCompId Controls Parent Company

**Severity:** INFO (blocked by AUTH-1 in practice, escalates to HIGH if AUTH-1 is not fixed)
**File:** `src/main/java/com/action/AdminRegisterAction.java`, line 195

**Description:**
On the `add` path, the parent company is determined by `sessCompId` from the session (line 195: `compDao.saveSubCompInfo(sessCompId, companybean)`). An authenticated attacker who can manipulate their session's `sessCompId` value could create a sub-company under an arbitrary parent company. The DAO method `saveSubCompInfo` accepts this value as an integer and inserts it into `company_rel.parent_company_id` without verifying that the current user has the right to create sub-companies under that parent.

**Recommendation:**
Once AUTH-1 is resolved, add a server-side authorization check confirming that the authenticated user's actual company ID matches `sessCompId` and that the user has the `add sub-company` privilege before invoking `saveSubCompInfo`.

---

### Categories with NO Issues

- **Stack-Specific CVE Exposure (Struts 1.3.10 ClassLoader):** The `execute` method does not perform any dynamic class loading or accept class-hierarchy parameters in a way that exposes the known Struts 1 ClassLoader injection vector (CVE-2014-0114) beyond the general Struts framework level. No specific exploitation pattern was identified in this action's code.
- **Path Traversal:** No file system operations are performed in this action.
- **Deserialization:** No deserialization of untrusted data occurs in this action.
- **Redirect Injection:** All forwards use named Struts forward aliases; no redirect targets are constructed from user input.

---

## Summary Table

| ID | Severity | Category | File | Short Description |
|----|----------|----------|------|-------------------|
| AUTH-1 | CRITICAL | Authentication | AdminRegisterAction.java:76,194,246 | Unauthenticated access to `add` and `update` privileged branches |
| V-1 | CRITICAL | Input Validation | struts-config.xml:24,146 / validation.xml:32 | Form-bean name mismatch — validation.xml rules never fire |
| AUTH-2 | HIGH | Authentication | AdminRegisterAction.java:40-45 | NPE on null session crashes action, exposes stack trace |
| SQL-1 | CRITICAL | SQL Injection | CompanyDAO.java:367,369,385,387 | String-concatenated column name and value in `checkExist`/`checkUserExit` |
| SQL-2 | HIGH | SQL Injection | CompanyDAO.java:408-418 | String-concatenated user values in `checkCompExist` |
| SQL-3 | HIGH | SQL Injection | SubscriptionDAO.java:133 | Integer concatenated into SQL string, raw Statement used |
| DE-1 | HIGH | Data Exposure | AdminRegisterAction.java:174-178 | Plaintext password in registration confirmation email |
| CSRF-1 | HIGH | CSRF | AdminRegisterAction.java (all branches) | No CSRF protection on state-changing public endpoint |
| V-2 | HIGH | Input Validation | AdminRegisterAction.java:95-98 | `pin` field: no length/complexity enforcement |
| DE-2 | MEDIUM | Data Exposure | AdminRegisterAction.java:134-137,150-153 | Raw Cognito error messages reflected to user |
| AE-1 | MEDIUM | Account Enumeration | AdminRegisterAction.java:133-148 | "User already exists" response enables email enumeration |
| V-3 | MEDIUM | Input Validation | AdminRegisterAction.java:54-71 | No maximum length caps on any field |
| V-4 | MEDIUM | Input Validation | AdminRegisterAction.java:48,76 | `accountAction` not null-checked or allowlisted before use |
| IDOR-1 | INFO | IDOR | AdminRegisterAction.java:195 | sessCompId-controlled parent company in `add` path (blocked by AUTH-1) |

---

## Finding Count by Severity

| Severity | Count | IDs |
|----------|-------|-----|
| CRITICAL | 3 | AUTH-1, V-1, SQL-1 |
| HIGH | 6 | AUTH-2, SQL-2, SQL-3, DE-1, CSRF-1, V-2 |
| MEDIUM | 4 | DE-2, AE-1, V-3, V-4 |
| INFO | 1 | IDOR-1 |
| **Total** | **14** | |
