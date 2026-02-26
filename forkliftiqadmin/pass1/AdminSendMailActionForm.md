# Security Audit: AdminSendMailActionForm
**Repository:** forkliftiqadmin
**Branch:** master
**Audit run:** audit/2026-02-26-01/
**Auditor:** Claude (automated pass 1)
**Date:** 2026-02-26

---

## 1. Reading Evidence

### Package and Class

```
package com.actionform;
public class AdminSendMailActionForm extends ValidatorForm
```

File: `src/main/java/com/actionform/AdminSendMailActionForm.java`
Lines 1–40. No `validate()` override. No `reset()` override. The class relies entirely on the Struts `ValidatorForm` framework mechanism.

### Fields

| Field | Declared Type | Line |
|---|---|---|
| `id` | `String` (default `null`) | 7 |
| `email` | `String` (default `null`) | 8 |
| `accountAction` | `String` (default `null`) | 9 |

Standard getter/setter pairs present for all three fields (lines 13–35). No custom logic in any accessor.

### validate() — None Defined

No `validate()` method is overridden in the form class. The class inherits `ValidatorForm.validate()`, which delegates to the Commons Validator framework using rules declared in `validation.xml`.

### reset() — None Defined

No `reset()` override. Default `ValidatorForm.reset()` is in effect; all fields are reset to `null` on each request (Struts default for `String` fields in scope `request`, which is what `struts-config.xml` declares for this action).

### validation.xml Rules for This Form

`src/main/webapp/WEB-INF/validation.xml` defines three `<form>` entries:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

**There is no `<form name="sendMailForm">` entry.** The bean is registered in `struts-config.xml` as `name="sendMailForm"` (line 25). Because no matching form name exists in `validation.xml`, Commons Validator will find no rules to run, and framework validation is therefore entirely absent for this form.

Additionally, **no `<plug-in>` element for `ValidatorPlugIn` is present in `struts-config.xml`**, which means even if rules were declared they would not be loaded. This confirms zero framework-level validation is active.

### Action class cross-reference

`src/main/java/com/action/AdminSendMailAction.java` (reviewed for context):

- Line 43: branches on `accountAction.equalsIgnoreCase("send_mail")`.
- Line 47: calls `isValidEmailAddress(sendMailForm.getEmail())` — custom regex check.
- Line 55: calls `sendMail(subject, body, "", emailAdd, "", "")` — passes `emailAdd` (the raw form field) as the recipient address `rEmail`.
- Lines 90–93: passes `rEmail` to `InternetAddress.parse(rEmail, false)` — `strict=false`.
- The `id` field from the form is **never used** in `AdminSendMailAction.execute()`.
- `accountAction` is sourced from a hidden form field (JSP line 31), not session state.

---

## 2. Findings

---

### FINDING 1 — CRITICAL: Email Header Injection via Comma-Separated Addresses in `email` Field

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 47, 55, 90–91
**Form field:** `AdminSendMailActionForm.email` (line 8)

**Description:**
The recipient email address supplied by the user is passed directly to `InternetAddress.parse(rEmail, false)`. The second argument `false` sets `strict=false`, which instructs the JavaMail parser to accept a **comma-separated list of addresses**. The application's custom validator (`isValidEmailAddress`) uses a regex that matches only a single email address (`m.matches()` — anchored, single value). However, an attacker can bypass the regex because the regex local-part allows many characters (`[a-zA-Z0-9.!#$%&'*+/=?^_{|}~-]+`).

More critically, an attacker who can craft a value that satisfies the regex for a first address and then appends additional recipients via URL encoding or via a form submission where encoding is relaxed can supply:

```
victim@example.com,attacker@evil.com
```

The `m.matches()` call on that string will **fail** the regex check (the comma is not in the allowed character class for the local part), so comma injection of multiple plain addresses is blocked at the regex layer for simple comma-separated strings.

**However**, the `InternetAddress.parse(..., false)` call accepts addresses in RFC 2822 display-name form. An attacker may supply:

```
"=?utf-8?b?...?=" <victim@example.com>
```

or exploit the fact that `strict=false` tolerates many malformed inputs, potentially leading to unintended recipients if the regex is somehow bypassed (e.g., via encoded newlines that JavaMail normalises before the regex sees the value — see Finding 2).

The core structural risk is the unconditional use of `InternetAddress.parse(..., false)` on untrusted input without stripping whitespace or CRLF sequences before parsing. This is the vector enabling Finding 2.

**Evidence:**
```java
// AdminSendMailAction.java line 55
sendMail(subject, body, "", emailAdd, "", "")

// AdminSendMailAction.java lines 90–91
message.setRecipients(Message.RecipientType.TO,
        InternetAddress.parse(rEmail, false));   // strict=false — accepts address lists
```

**Recommendation:**
Use `new InternetAddress(rEmail, true)` (strict single-address constructor) instead of `InternetAddress.parse`. Before constructing the `InternetAddress`, strip all CR (`\r`) and LF (`\n`) characters from the input. Validate that only a single address is present.

---

### FINDING 2 — CRITICAL: SMTP Header Injection via Newline Characters in `email` Field

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 47, 90–91
**Form field:** `AdminSendMailActionForm.email` (line 8)

**Description:**
The `email` field value is validated by a regex (`isValidEmailAddress`) that uses `java.util.regex.Pattern.compile` and `m.matches()`. The regex character class for the local part includes many printable characters but **does not explicitly exclude `\r` or `\n`**. Depending on how the Struts request processor presents the field value (some containers normalise CRLF in form data, others do not), an attacker may be able to embed newline sequences in the email parameter.

If a newline sequence reaches `InternetAddress.parse(rEmail, false)`, JavaMail may interpret it in ways that inject additional headers into the MIME message, or the SMTP transport layer may split the `RCPT TO` command, enabling:

- **BCC injection** — injecting `\r\nBcc: attacker@evil.com` after a valid address.
- **Additional header injection** — injecting arbitrary RFC 822 headers such as `Content-Type` overrides.

The absence of an explicit CRLF-stripping step before the call to `InternetAddress.parse` means this channel is not hardened.

**Evidence:**
```java
// isValidEmailAddress — regex does not strip or reject \r\n
String ePattern = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@...";
java.util.regex.Matcher m = p.matcher(email);
return m.matches();

// Value used directly in parse() call with no sanitisation
InternetAddress.parse(rEmail, false);
```

**Recommendation:**
Before any validation or use, apply:
```java
email = email.replaceAll("[\r\n]", "");
```
Then use the strict single-address constructor. Log and reject any input that contained CRLF sequences.

---

### FINDING 3 — HIGH: No Framework Validation for `sendMailForm` — All Fields Unvalidated at Framework Layer

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/validation.xml` (entire file)
**Form bean:** `sendMailForm` declared at `struts-config.xml` line 25

**Description:**
`validation.xml` contains no `<form name="sendMailForm">` block. The Struts action declares `validate="true"` (struts-config.xml line 163), so the framework will invoke `ValidatorForm.validate()`, but because no rules are registered, validation passes unconditionally regardless of field content.

This means:
- `email` has no `required` rule, no `email` format rule at the framework layer.
- `accountAction` has no `required` rule and no whitelist rule.
- `id` has no rule at all.

The only gate is the ad-hoc `isValidEmailAddress()` check in the action class, which is bypassable (see Findings 1 and 2) and provides no protection for `accountAction` or `id`.

Additionally, **no `ValidatorPlugIn` is registered in `struts-config.xml`**, so even adding rules to `validation.xml` would have no effect until the plug-in is wired in.

**Evidence:**
`validation.xml` lines 23–67: three `<form>` entries, none named `sendMailForm`.
`struts-config.xml` line 25: `<form-bean name="sendMailForm" .../>`.

**Recommendation:**
1. Register `ValidatorPlugIn` in `struts-config.xml`.
2. Add a `<form name="sendMailForm">` block to `validation.xml` with at minimum:
   - `email` field: `depends="required,email"` — enforces presence and RFC-compliant single-address format.
   - `accountAction` field: `depends="required"` with a mask rule limiting to the known value `send_mail`.
3. Remove the `id` field from the form entirely if it is not used (see Finding 5).

---

### FINDING 4 — HIGH: `accountAction` Controlled Entirely by Hidden Form Field — Control-Flow Bypass

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/mod/sendmail.jsp` line 31; `src/main/java/com/action/AdminSendMailAction.java` lines 40, 43
**Form field:** `AdminSendMailActionForm.accountAction` (line 9)

**Description:**
The value `send_mail` that drives the email-sending code path is embedded in the JSP as:

```jsp
<html:hidden property="accountAction" value="send_mail">
```

This hidden field is entirely under attacker control in a crafted POST request. Any authenticated user (or unauthenticated user if the session check is weak — see Finding 6) can submit a POST to `/sendMail.do` with any `accountAction` value. If `accountAction` does not equal `send_mail` (case-insensitive), the action returns all driver records for the company (`driverDao.getAllDriver(sessCompId, true)`) and forwards to a JSON result tile — constituting an information disclosure path (see Finding 5).

More significantly, there is no server-side enforcement that `accountAction` must be one of a fixed set of values. Any unexpected value silently falls through to the `else` branch and exposes driver data.

**Evidence:**
```java
// AdminSendMailAction.java lines 40, 43, 68–74
String accountAction = sendMailForm.getAccountAction();
if (accountAction.equalsIgnoreCase("send_mail")) {
    ...
} else {
    List<DriverBean> arrDriver = driverDao.getAllDriver(sessCompId, true);
    request.setAttribute("arrAdminDriver", arrDriver);
    return mapping.findForward("failure");
}
```

**Recommendation:**
Validate `accountAction` server-side against an explicit whitelist before branching. Do not use a hidden field to carry application flow-control tokens; use session state or action path parameters instead. The `else` branch should not return driver data by default — it should return an error or redirect.

---

### FINDING 5 — HIGH: Dead Field `id` — IDOR Vector if Activated

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminSendMailActionForm.java` lines 7, 29–35

**Description:**
The form declares an `id` field (String) with full getter and setter. This field is not referenced anywhere in `AdminSendMailAction.java`. However:

1. Because it is declared and has a public setter, Struts will automatically bind any `id` request parameter to this field. An attacker can POST `id=<arbitrary_value>` and it will be accepted silently.
2. If the field is later activated by a developer who adds `id`-based lookups (e.g., to look up a driver and send mail to that driver's address rather than the user-supplied address), the absence of validation rules and the `String` type create an IDOR risk — no ownership check would be enforced at the form layer.
3. The field name `id` is extremely generic, increasing the likelihood of accidental future use.

**Evidence:**
```java
// AdminSendMailActionForm.java line 7
private String id = null;
// Lines 29–35: getter and setter present, no use in Action
```
`AdminSendMailAction.java`: no reference to `sendMailForm.getId()`.

**Recommendation:**
Remove the `id` field from the form entirely if it is not needed. If it is needed in future, add a validation rule and an ownership check in the action before any database lookup.

---

### FINDING 6 — HIGH: NullPointerException Risk — Unguarded `accountAction.equalsIgnoreCase()`

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminSendMailAction.java` line 43

**Description:**
`sendMailForm.getAccountAction()` returns `null` by default (field initialised to `null`, no `reset()` override, no `required` validator). If a request is submitted without an `accountAction` parameter, `accountAction` will be `null` and the call `accountAction.equalsIgnoreCase("send_mail")` will throw a `NullPointerException`. Depending on Struts error handling configuration, this may produce a 500 response leaking a stack trace, or it may be silently swallowed by the catch-all `catch (Throwable t)` in `sendMail()` (though that catch block is not in the execution path for this NPE).

The same risk applies to `sendMailForm.getEmail()` at line 47 if the `email` parameter is absent.

**Evidence:**
```java
// AdminSendMailAction.java line 40–43
String accountAction = sendMailForm.getAccountAction();
// accountAction is null if parameter absent
if (accountAction.equalsIgnoreCase("send_mail")) {  // NPE if null
```

**Recommendation:**
Use `"send_mail".equalsIgnoreCase(accountAction)` (constant on the left) to safely handle `null`. Add a `required` validator for `accountAction` in `validation.xml`. Add null checks or use `StringUtils.equalsIgnoreCase`.

---

### FINDING 7 — MEDIUM: Session Not Validated Before Use — Potential NullPointerException / Authentication Bypass

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSendMailAction.java` lines 36–37

**Description:**
The session is obtained with `request.getSession(false)`, which correctly avoids creating a new session. However, the return value is not checked for `null` before calling `session.getAttribute(...)`. If no session exists (e.g., a direct unauthenticated POST to `/sendMail.do`), this will throw a `NullPointerException` at line 37.

Additionally, `sessCompId` is used at line 71 (`driverDao.getAllDriver(sessCompId, true)`) in the `else` branch. If `sessCompId` is empty string (the default fallback), `getAllDriver` may return data for a null/empty company — the safety of that depends on the DAO implementation, but the fallback value `""` is concerning.

**Evidence:**
```java
// Lines 36–37
HttpSession session = request.getSession(false);
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
// session itself is not null-checked
```

**Recommendation:**
Check `if (session == null)` and redirect to login immediately. Validate that `sessCompId` is non-empty and belongs to the authenticated principal before using it in any query.

---

### FINDING 8 — MEDIUM: `sendMail()` Always Returns `true` Regardless of Failure

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSendMailAction.java` lines 77–109

**Description:**
The `sendMail()` method catches `AddressException` and `MessagingException` in inner try-catch blocks (lines 92–94 and 100–103) and prints them to stdout rather than propagating them. The method always reaches `return true` (line 108) even if the mail was never sent. The outer `catch (Throwable t)` on lines 105–107 also swallows all errors.

This means:
- Mail delivery failures are silently swallowed and logged only to `System.out` (which may not be monitored).
- The action returns `"success"` to the client even when mail delivery failed, misleading the user and masking operational failures.
- There is no audit trail of email send attempts, successes, or failures.

**Evidence:**
```java
// Lines 92–94, 100–103, 105–107
} catch (Exception e) {
    System.out.println("Message Recipents Exception :" + e);
}
// ...
} catch (Exception e) {
    System.out.println("Transport Exception :" + e);
}
// ...
} catch (Throwable t) {
    t.printStackTrace();
}
return true;  // line 108 — always
```

**Recommendation:**
Return `false` (or throw) when a delivery exception is caught. Use a proper logging framework (SLF4J/Log4j) rather than `System.out.println`. Consider adding an audit log entry for every email send attempt.

---

### FINDING 9 — MEDIUM: CSRF — No Token Protection on Email-Sending Action

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/mod/sendmail.jsp`; `src/main/webapp/WEB-INF/struts-config.xml` lines 158–167

**Description:**
As noted for the stack as a whole, Apache Struts 1.3.10 has no built-in CSRF token mechanism. The `/sendMail.do` action performs a state-changing operation (sending email) and is protected only by session authentication. A CSRF attack from any page the authenticated admin visits can trigger arbitrary email sends to attacker-controlled addresses by submitting a forged POST with `email=attacker@evil.com&accountAction=send_mail`.

This is a structural gap for the entire application, but the email-sending action is a particularly attractive CSRF target because it can be used to send phishing invitations that appear to come from the platform's legitimate mail infrastructure (`info@ciiquk.com`).

**Evidence:**
`sendmail.jsp` — no CSRF token field present.
`struts-config.xml` line 163: `validate="true"` but no token check configured.

**Recommendation:**
Implement CSRF protection for all state-changing actions. For Struts 1, the standard approach is to use `saveToken(request)` / `isTokenValid(request, true)` from `org.apache.struts.action.Action`. Add token generation to the page that loads the invite modal, and validate the token in `AdminSendMailAction.execute()` before processing.

---

### FINDING 10 — MEDIUM: Hardcoded Sender Address Reveals Infrastructure Detail

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminSendMailAction.java` line 87

**Description:**
The sender address `info@ciiquk.com` is hardcoded in the source code. This leaks the production mail identity in the repository. More importantly, the `sendMail` method accepts `sEmail` as a parameter (for a configurable sender), but it is always called with `""` (line 55), meaning the configurable sender parameter is unused and the hardcoded address is always used.

**Evidence:**
```java
// Line 87
message.setFrom(new InternetAddress("info@ciiquk.com"));
// Line 55
sendMail(subject, body, "", emailAdd, "", "")  // sEmail = ""
```

**Recommendation:**
Move the sender address to a configuration property (JNDI or properties file). Use the `sEmail` parameter as intended, populated from configuration.

---

### FINDING 11 — LOW: `email` Field Accepts Null — No Null Guard Before `isValidEmailAddress`

**Severity:** LOW
**File:** `src/main/java/com/action/AdminSendMailAction.java` line 47

**Description:**
`isValidEmailAddress` correctly handles null via `StringUtils.isBlank(email)` (line 112), so this does not produce a NullPointerException. However, the absence of a `required` rule in `validation.xml` means the flow reaches the action with a null `email` and silently returns `"failure"` without any user-facing error message distinguishing "email was blank" from "email was malformed" or "mail server is down". This degrades user experience and makes debugging harder.

**Evidence:**
```java
// isValidEmailAddress line 112
if (StringUtils.isBlank(email)) {
    return false;
}
```

**Recommendation:**
Add a `required` rule for `email` in `validation.xml`. Return a meaningful error message to the user when the email field is empty vs. invalid format.

---

### FINDING 12 — LOW: HTML Injection in Email Body — Not Present (Current Code)

**Severity:** INFO
**File:** `src/main/java/com/action/AdminSendMailAction.java` lines 44–45

**Description:**
The subject and body are currently hardcoded string literals (`"Driver Invitation"` and `"Driver Invite body"`). No user-supplied content is included in either field at this time. Therefore there is **no HTML injection or stored XSS risk in the email body at present**.

However, the `sendMail` method signature accepts `mBody` and `subject` as parameters and sends them via `message.setContent(mBody, "text/html")` without any escaping. If future development adds user-controlled content to either field, HTML injection into the email body and subject will be trivially possible. This is flagged as a design-level concern.

**Evidence:**
```java
// Lines 44–45
String subject = "Driver Invitation";
String body = "Driver Invite body";
// Line 96: message.setContent(mBody, "text/html") — no escaping
```

**Recommendation:**
Document that `sendMail()` renders its body argument as `text/html` without escaping. Any future caller that introduces user-controlled content into `subject` or `body` must HTML-encode that content first, or the content-type must be changed to `text/plain`.

---

## 3. Category Summary

| Category | Status |
|---|---|
| Input Validation — Coverage | ISSUES FOUND (Findings 1, 2, 3) |
| Input Validation — Email address format | ISSUES FOUND (Findings 1, 2) |
| Input Validation — HTML injection in body | NO ISSUES (current hardcoded body — see Finding 12 / INFO) |
| Type Safety | NO ISSUES (all fields are String; no numeric parsing performed) |
| IDOR Risk | ISSUES FOUND (Finding 5 — latent; Finding 4 — active in else-branch) |
| Sensitive Fields | ISSUES FOUND (Finding 10 — hardcoded address) |
| Data Integrity | ISSUES FOUND (Finding 8 — silent failure; Finding 6 — NPE) |
| CSRF | ISSUES FOUND (Finding 9 — structural gap, stack-wide) |

---

## 4. Finding Count by Severity

| Severity | Count | Finding Numbers |
|---|---|---|
| CRITICAL | 2 | 1, 2 |
| HIGH | 4 | 3, 4, 5, 6 |
| MEDIUM | 4 | 7, 8, 9, 10 |
| LOW | 1 | 11 |
| INFO | 1 | 12 |
| **Total** | **12** | |

---

## 5. Files Reviewed

| File | Purpose |
|---|---|
| `src/main/java/com/actionform/AdminSendMailActionForm.java` | Primary audit target — form bean |
| `src/main/webapp/WEB-INF/validation.xml` | Framework validation rules (no rules for this form) |
| `src/main/java/com/action/AdminSendMailAction.java` | Action class consuming this form |
| `src/main/webapp/html-jsp/mod/sendmail.jsp` | JSP rendering the form |
| `src/main/webapp/WEB-INF/struts-config.xml` | Action mapping and form bean registration |
| `src/main/webapp/WEB-INF/tiles-defs.xml` | Tile definition for OperatorInviteDefinition |
