# Security Audit Report: AdminSendMailAction

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**Auditor:** Automated Security Audit (Pass 1)
**Date:** 2026-02-26

---

## 1. Reading Evidence

### Package and Class

- **File:** `src/main/java/com/action/AdminSendMailAction.java`
- **Package:** `com.action`
- **Class:** `AdminSendMailAction extends org.apache.struts.action.Action`

### Public/Protected Methods

| Line | Method Signature |
|------|-----------------|
| 33 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |
| 77 | `public boolean sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail) throws AddressException, MessagingException` |
| 111 | `public boolean isValidEmailAddress(String email)` |

### DAOs / Services Called

| Location | Call | Purpose |
|----------|------|---------|
| Line 31 | `DriverDAO.getInstance()` | Singleton DAO instantiated at class level |
| Line 70–71 | `driverDao.getAllDriver(sessCompId, true)` | Fetches all active drivers for the session company |

### Form Class

- **Form bean name (struts-config):** `sendMailForm`
- **Form class:** `com.actionform.AdminSendMailActionForm extends ValidatorForm`
- **Fields:**
  - `id` (String)
  - `email` (String)
  - `accountAction` (String)

### Struts-Config Mapping

| Attribute | Value |
|-----------|-------|
| `path` | `/sendMail` |
| `name` | `sendMailForm` |
| `type` | `com.action.AdminSendMailAction` |
| `scope` | `request` |
| `validate` | `true` |
| `input` | `OperatorInviteDefinition` |
| `roles` | *(not set — no `roles` attribute present)* |
| Forward: `success` | `jsonResultDefinition` |
| Forward: `failure` | `jsonResultDefinition` |

**Struts-config source:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 159–167.

### validation.xml Coverage

The `sendMailForm` form name is **absent** from `src/main/webapp/WEB-INF/validation.xml`. Only three forms are defined: `loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm`.

---

## 2. Findings

---

### FINDING-01: Missing Role-Based Access Control on Sensitive Mail Action

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, line 159–167
**Category:** Authentication / Authorization

**Description:**
The `/sendMail` action mapping has no `roles` attribute. Struts 1 supports a `roles` attribute on `<action>` elements to restrict access to named J2EE security roles. Its absence means any authenticated session can invoke this action — there is no role separation between a regular operator, a company admin, and a platform super-admin.

**Evidence:**
```xml
<action
    path="/sendMail"
    name="sendMailForm"
    scope="request"
    type="com.action.AdminSendMailAction"
    validate="true"
    input="OperatorInviteDefinition">
    <forward name="success" path="jsonResultDefinition"/>
    <forward name="failure" path="jsonResultDefinition"/>
</action>
```
No `roles="..."` attribute is present.

**Recommendation:**
Add a `roles` attribute restricting access to the appropriate administrative role (e.g., `roles="admin"`). Additionally, enforce role checks programmatically inside the action's `execute` method using a session-stored role attribute, consistent with how other privileged actions in this application should be gated.

---

### FINDING-02: Authentication Check Weak — No Null-Safe Session Guard Before sessCompId Access

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 36–37
**Category:** Authentication

**Description:**
The action calls `request.getSession(false)` (correct — does not force session creation), but then immediately dereferences `session.getAttribute(...)` without checking whether `session` is `null`. If `PreFlightActionServlet` fails to intercept the request (e.g., due to a servlet container misconfiguration, a direct forward from an unauthenticated path, or a code path that bypasses the servlet), the action will throw a `NullPointerException` on line 37 rather than cleanly rejecting the request. More critically, the action does not itself verify that `sessCompId` is non-empty and treat an empty/null value as an authentication failure — it silently uses an empty string as the `compId`, causing `getAllDriver` to be called with an effectively invalid company ID.

**Evidence:**
```java
// Line 36
HttpSession session = request.getSession(false);
// Line 37 — session is dereferenced without null check
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
```
When `sessCompId` resolves to `""`, line 70 passes an empty string to `DriverDAO.getAllDriver(sessCompId, true)`, which then calls `Long.parseLong("")` — throwing a `NumberFormatException` at runtime rather than returning an authentication error to the caller.

**Recommendation:**
1. Check `session == null` immediately after `getSession(false)` and redirect to the login/expire page if null.
2. After reading `sessCompId`, check that it is non-blank; if blank, redirect to the expire page.
3. Do not rely solely on `PreFlightActionServlet` as the only authentication gate — defence-in-depth requires each action to validate its own preconditions.

---

### FINDING-03: No CSRF Protection

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminSendMailAction.java` (entire class); `src/main/webapp/WEB-INF/struts-config.xml`, lines 159–167
**Category:** CSRF

**Description:**
This is a state-changing action (it sends an email invitation to an address supplied in the request). There is no CSRF token generated, stored in session, or verified in the action. The stack context confirms this is a structural gap across the application: Apache Struts 1.3.10 has no built-in CSRF protection, no Spring Security is present, and no custom token mechanism is implemented here.

An attacker can craft a page that auto-submits a POST to `/sendMail.do` with an arbitrary `email` parameter from any origin where the victim has an active session. This causes the application to dispatch an "invitation" email on behalf of the victim to an attacker-controlled address, potentially facilitating phishing or enumerating that the victim's account is active.

**Evidence:**
- `sendMail` is called at line 55 using `emailAdd` taken directly from the form without any origin or token check.
- No token field is present in `AdminSendMailActionForm`.
- No token validation exists anywhere in `execute()`.

**Recommendation:**
Implement a synchronizer token pattern: generate a cryptographically random token at session start, embed it as a hidden field in all forms, and validate it at the start of every state-changing action's `execute` method before processing any business logic.

---

### FINDING-04: No Entry in validation.xml for sendMailForm — Struts Declarative Validation Absent

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/validation.xml`
**Category:** Input Validation

**Description:**
Although the struts-config mapping sets `validate="true"`, there is no `<form name="sendMailForm">` entry in `validation.xml`. With Struts 1 `ValidatorForm`, when `validate="true"` is declared but no corresponding entry exists in `validation.xml`, the framework performs no validation and calls `execute()` with whatever values the client supplied. This means the `email` and `accountAction` fields receive zero declarative validation.

The action compensates partially by calling `isValidEmailAddress()` for the `send_mail` branch (line 47), but the `accountAction` field is never sanitized or constrained, and the email validation is only applied in one branch.

**Evidence:**
- `validation.xml` contains entries for: `loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm` — `sendMailForm` is absent.
- `validate="true"` is set in struts-config (line 163) but is effectively a no-op for this form.

**Recommendation:**
Add a `<form name="sendMailForm">` block to `validation.xml` with at minimum: `email` field requiring `required` and `email` validators, and `accountAction` field requiring `required` with a mask validator that whitelists known values (e.g., `^send_mail$`).

---

### FINDING-05: Uncontrolled accountAction Parameter — Missing Whitelist Validation

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 40, 43
**Category:** Input Validation

**Description:**
The `accountAction` value is read directly from user-controlled form input and used to branch control flow via `equalsIgnoreCase("send_mail")`. No whitelist check or null guard is applied. If `accountAction` is `null`, the call to `accountAction.equalsIgnoreCase(...)` on line 43 throws a `NullPointerException`, which propagates as an unhandled exception and may result in a 500 response revealing stack trace detail.

The implicit `else` branch (lines 68–74) is taken for any unrecognised value of `accountAction`, causing a full driver list for the company to be loaded into a request attribute and the action to forward to the `failure` tile — which may render that list in the response depending on the tile configuration. This means an attacker with a valid session can trigger the full driver listing by sending any arbitrary value (or an empty string) for `accountAction`.

**Evidence:**
```java
// Line 40
String accountAction = sendMailForm.getAccountAction();
// Line 43 — no null check; NPE if accountAction is null
if (accountAction.equalsIgnoreCase("send_mail")) {
    ...
} else {
    // Line 70: driver list is loaded and attached to request for ANY other value
    List<DriverBean> arrDriver = driverDao.getAllDriver(sessCompId, true);
    request.setAttribute("arrAdminDriver", arrDriver);
    return mapping.findForward("failure");
}
```

**Recommendation:**
1. Null-check `accountAction` before use.
2. Use an explicit whitelist: if the value is not one of the expected discrete values, return an error forward immediately.
3. Do not fall through to data-loading logic for unrecognised action values.

---

### FINDING-06: sendMail() Swallows Exceptions and Always Returns true — Silent Failure / False Success Signal

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 77–109
**Category:** Error Handling / Data Integrity

**Description:**
The `sendMail` method catches `Exception` around `InternetAddress.parse()` (line 92) and catches `Exception` around `Transport.send()` (line 101), logging to `System.out` in both cases. It also catches `Throwable` at the outer level (line 105). Crucially, the method **always returns `true`** regardless of whether the email was actually sent. The caller at line 55 treats the return value as the definitive success indicator to set the `result` attribute and choose the forward.

This means:
- A mail delivery failure is reported to the UI as success.
- An attacker can observe no difference in application behaviour regardless of whether the mail infrastructure is functioning, making the feature appear to work while silently failing.
- More critically: if `Transport.send()` throws (line 100–103), the exception is caught and discarded, but the method still returns `true` — the caller shows the user a success message.

**Evidence:**
```java
// Line 100–103
try {
    Transport.send(message);
} catch (Exception e) {
    System.out.println("Transport Exception :" + e);
}
// ...
// Line 108 — always reached regardless of any exception above
return true;
```

**Recommendation:**
- Use a boolean flag (e.g., `boolean sent = false`) set to `true` only inside the `Transport.send()` try block after the call completes without exception.
- Return this flag.
- Replace `System.out.println` with proper logger calls (Log4j is already imported via `InfoLogger`).

---

### FINDING-07: Email Address Passed to InternetAddress.parse() with strict=false — Potential Header Injection Vector

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 90–94
**Category:** Email Injection

**Description:**
`InternetAddress.parse(rEmail, false)` is called with `strict=false`. The non-strict mode is more permissive in what it accepts as a valid RFC 2822 address and is less resistant to malformed input. While the action's current `send_mail` path passes a fixed `subject` and `body` ("Driver Invitation" / "Driver Invite body") that are not user-controlled, the `rEmail` parameter fed to this call comes directly from `sendMailForm.getEmail()` (user-supplied).

Email header injection via the `To:` header is possible when the recipient address field is not strictly validated before being passed to the mail API: a crafted address containing newline characters (`\r\n`) can inject additional headers into the MIME message. Although the regex in `isValidEmailAddress()` (line 116) does not explicitly allow `\n` or `\r`, the Java regex `.` by default does not match newlines — however, the character class `[a-zA-Z0-9.!#$%&'*+/=?^_\`{|}~-]` in the local-part pattern does not include `\r` or `\n`, providing some incidental protection. The risk is partially mitigated but relies on correct regex behaviour rather than explicit rejection of control characters.

The deeper concern is that `sendMail()` is a `public` method (line 77) with no access modifier making it package-private or protected. Any future caller within the codebase can pass arbitrary strings for `subject`, `mBody`, and `rEmail` directly without going through the regex check, bypassing the only validation layer.

**Evidence:**
```java
// Line 90–94
message.setRecipients(Message.RecipientType.TO,
        InternetAddress.parse(rEmail, false));
```
`strict=false` used; `sendMail()` is `public` with no internal sanitization of its parameters.

**Recommendation:**
1. Change `InternetAddress.parse(rEmail, false)` to `InternetAddress.parse(rEmail, true)` to enforce strict RFC 2822 parsing.
2. Explicitly strip or reject any `\r` or `\n` characters from `rEmail`, `subject`, and `mBody` before passing them to the mail API.
3. Change the visibility of `sendMail()` to `private` or `protected` since it is not part of the Struts action contract and should not be directly callable.

---

### FINDING-08: Driver Data Exposed via Implicit else Branch

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 68–74
**Category:** Data Exposure / IDOR

**Description:**
When `accountAction` is anything other than `"send_mail"` (including null, empty, or any crafted string), the action fetches the full list of active drivers for `sessCompId` and attaches it to the request as attribute `arrAdminDriver`. The forward target is `jsonResultDefinition` (the `failure` forward maps to `jsonResultDefinition` per struts-config line 166). Depending on what `jsonResultDefinition` renders, this driver list — which includes names, licence numbers, email addresses, phone numbers, department, location, and app access fields (see `DriverBean.builder()` at DriverDAO.java lines 300–312) — may be serialised into the response.

This is an IDOR-adjacent issue: a session holder from one company cannot see another company's data due to the `sessCompId` scope, but the intent of this action appears to be an email-send utility, not a driver listing endpoint. The driver data exposure in the else branch is a design accident rather than intentional, and should be treated as unintended data disclosure.

**Evidence:**
```java
// Lines 70–74
List<DriverBean> arrDriver = driverDao.getAllDriver(sessCompId, true);
request.setAttribute("arrAdminDriver", arrDriver);
return mapping.findForward("failure");
```
`DriverBean` fields populated: `id`, `first_name`, `last_name`, `active`, `licno`, `expiry_date`, `phone`, `location`, `department`, `joindt`, `email_addr`, `app_access`.

**Recommendation:**
Remove the data-loading logic from the else branch entirely. If the intent is to pre-populate an invite form with a driver list, this should be a distinct, explicitly named action. The else branch in this action should return a clean error forward without exposing any data.

---

## 3. Categories with No Issues

**SQL Injection:** No issues found. `DriverDAO.getAllDriver()` uses a `PreparedStatement` with a parameterized query (`QUERY_DRIVER_BY_COMP` at DriverDAO.java lines 76–77). The `compId` is bound via `stmt.setLong(1, Long.parseLong(compId))` — a typed bind, not string concatenation. No raw SQL construction occurs in the code paths exercised by this action.

---

## 4. Summary Table

| # | Severity | Category | Description |
|---|----------|----------|-------------|
| 01 | HIGH | Authorization | No `roles` attribute on `/sendMail` mapping — any authenticated user can invoke |
| 02 | HIGH | Authentication | No null check on session; empty `sessCompId` silently propagates |
| 03 | HIGH | CSRF | No synchronizer token — action sends email on behalf of victim via CSRF |
| 04 | MEDIUM | Input Validation | `sendMailForm` absent from `validation.xml` — declarative validation is a no-op |
| 05 | MEDIUM | Input Validation | `accountAction` not null-checked or whitelisted; unrecognised values trigger data loading |
| 06 | MEDIUM | Error Handling | `sendMail()` always returns `true`; swallows all exceptions silently |
| 07 | MEDIUM | Email Injection | `InternetAddress.parse(rEmail, false)` uses non-strict mode; `sendMail()` is public with no internal sanitization |
| 08 | MEDIUM | Data Exposure | Else branch loads and exposes full driver list (PII) for any non-`send_mail` action value |

**Finding counts by severity:**

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 3 |
| MEDIUM | 5 |
| LOW | 0 |
| INFO | 0 |
| **Total** | **8** |
