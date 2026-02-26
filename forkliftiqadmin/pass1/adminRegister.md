# Security Audit Report — adminRegister.jsp

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**Auditor:** Automated Pass 1 (Claude Sonnet 4.6)
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10 (NOT Spring)
**Auth Gate:** PreFlightActionServlet — `sessCompId != null`

---

## Files Examined

| File | Purpose |
|------|---------|
| `src/main/webapp/html-jsp/adminRegister.jsp` | Primary audit target — public registration form |
| `src/main/java/com/action/AdminRegisterAction.java` | Struts Action backing the form |
| `src/main/java/com/actionform/AdminRegisterActionForm.java` | ActionForm (form bean) |
| `src/main/java/com/actionservlet/PreFlightActionServlet.java` | Auth gate servlet |
| `src/main/webapp/WEB-INF/struts-config.xml` | Action mapping and forwards |
| `src/main/java/com/util/RuntimeConf.java` | Application constants |
| `src/main/webapp/includes/importLib.jsp` | Shared imports and tag library declarations |

---

## Section 1 — Reading Evidence

### 1.1 Form Action URLs

| Line | Tag / Element | Action URL | Method |
|------|--------------|------------|--------|
| 12 | `<html:form>` | `adminRegister.do` | POST |

### 1.2 Request Parameters Used in the Form

| Parameter Name | Element | Lines | Notes |
|---------------|---------|-------|-------|
| `name` | `<html:text property="name">` | 30–35 | Company name |
| `timezone` | `<select name="timezone">` | 38–48 | Plain HTML select, not Struts tag |
| `address` | `<html:textarea property="address">` | 52–57 | Multi-line text |
| `contact_fname` | `<html:text property="contact_fname">` | 69–75 | First name |
| `contact_lname` | `<html:text property="contact_lname">` | 77–83 | Last name |
| `contact_no` | `<html:text property="contact_no">` | 85–91 | Phone number |
| `email` | `<html:text property="email">` | 94–100 | Email address |
| `pin` | `<input type="password" name="pin">` | 102–110 | Password — plain HTML, not Struts tag |
| `cpassword` | `<input type="password" name="cpassword">` | 112–119 | Confirm password — plain HTML |
| `id` | `<html:hidden property="id">` | 138 | Hidden — company ID |
| `accountAction` | `<html:hidden property="accountAction" value="register">` | 139 | Hidden — action discriminator |

### 1.3 Struts Tags That Output Data

| Line | Tag | Attribute / Property | Filter Applied |
|------|-----|---------------------|----------------|
| 14 | `<html:errors />` | Global error messages | HTML-escaped by Struts (from message resources) |
| 15–19 | `<html:messages id="accountmsg">` + `<bean:write name="accountmsg" />` | Message resource string | `bean:write` defaults to **no escaping** (filter="false") |
| 25 | `<bean:message key="comp.title"/>` | i18n message resource key | Safe — static key lookup |
| 39 | `<bean:message key="settings.timezone"/>` | i18n message resource key | Safe — static key lookup |
| 43 | `<bean:write name="timezone" property="id" />` | `TimezoneBean.id` rendered inside `option value='...'` using **single quotes** | No escaping applied; rendered inside attribute |
| 44 | `<bean:write name="timezone" property="name"/>` | `TimezoneBean.name` rendered as option text | `bean:write` defaults to **no escaping** |
| 64 | `<bean:message key="user"/>` | i18n message resource key | Safe — static key lookup |
| 129 | `<bean:message key="button.back"/>` | i18n message resource key | Safe — static key lookup |

### 1.4 JavaScript Blocks Using Server-Side Data

| Lines | Description |
|-------|-------------|
| 149–187 | `fnsubmitAccount()` — reads field values from the DOM via jQuery (`$('[name="..."]').val()`) and performs client-side validation before submitting `#adminRegActionForm`. No server-side data is interpolated into the JS at render time. |
| 184–187 | `fnGoBackHome()` — hardcodes `url = "index.jsp"` and calls `location.replace(url)`. No server-side data interpolated. |

---

## Section 2 — Findings

---

### FINDING-01

**Severity:** CRITICAL
**Category:** Authentication / Authorization — Unauthenticated Account Creation
**File:** `src/main/webapp/html-jsp/adminRegister.jsp` (line 12) / `src/main/java/com/actionservlet/PreFlightActionServlet.java` (line 107)

**Description:**
`adminRegister.do` is explicitly listed in the `excludeFromFilter` exclusion list of `PreFlightActionServlet`, meaning the auth check (`sessCompId != null`) is **never applied** to this endpoint. Any anonymous internet user can POST to `adminRegister.do` with `accountAction=register` and create a fully provisioned company account plus Cognito identity in the system. The action also accepts `accountAction=add` (to create a sub-company under an existing session company), and although `add` relies on `sessCompId` from the session, the session object itself is never validated at the servlet gate for this path — the action proceeds to call `session.getAttribute("sessCompId")` but the gate never forces a redirect for this `.do` path even when the session is null or unauthenticated.

**Evidence:**

```java
// PreFlightActionServlet.java line 107
else if (path.endsWith("adminRegister.do")) return false;
```

`excludeFromFilter` returns `false` when the path matches `adminRegister.do`, meaning the auth gate block (lines 51–60) is **never entered** for this action — both GET and POST requests reach `AdminRegisterAction.execute()` without any session check being enforced at the servlet layer.

```java
// AdminRegisterAction.java lines 76–180
if (accountAction.equalsIgnoreCase("register") || accountAction.equalsIgnoreCase("add")) {
    ...
    compId = compDao.saveCompInfo(companybean, RuntimeConf.ROLE_COMP);
    if (compId > 0 && subscriptionDAO.saveDefualtSubscription(compId)) {
        ...
        return mapping.findForward("successregister");
    }
}
```

There is no secondary authorization check inside the action itself before inserting into the database.

**Recommendation:**
Remove `adminRegister.do` from the exclusion list OR add an explicit check inside `AdminRegisterAction.execute()` to differentiate between the public self-registration flow (`register`) and the authenticated sub-company creation flow (`add`). The `add` path must require a valid authenticated session. If self-registration is intentionally public, consider rate-limiting, CAPTCHA, and email verification before account activation.

---

### FINDING-02

**Severity:** CRITICAL
**Category:** CSRF — No Token on State-Changing Public POST
**File:** `src/main/webapp/html-jsp/adminRegister.jsp` (line 12)

**Description:**
The form at line 12 POSTs to `adminRegister.do` which creates a company account and triggers a Cognito user sign-up. There is no CSRF token anywhere in the form. Because the endpoint is unauthenticated (see FINDING-01), an attacker can construct a cross-origin form targeting this endpoint and trigger account creation, Cognito provisioning, and subscription creation on behalf of an arbitrary visitor who loads attacker-controlled content. While the harm of a public-registration CSRF is lower than an authenticated CSRF, the backend effects (Cognito user creation, DB writes, default subscription provisioning) make this exploitable for resource abuse, tenant enumeration, and denial-of-service against the Cognito user pool.

**Evidence:**

```jsp
<!-- adminRegister.jsp line 12 — no token field anywhere in the form -->
<html:form method="post" action="adminRegister.do" styleId="adminRegActionForm">
```

Struts 1.3.10 does not generate CSRF tokens automatically. No `<html:hidden>` carrying a synchronizer token is present. The `accountAction` hidden field (line 139) has a static, guessable value (`register`) and provides no CSRF protection.

**Recommendation:**
Implement a synchronizer token pattern: generate a cryptographically random token per session, store it in the session, render it as a hidden field, and verify it server-side before processing the POST in `AdminRegisterAction.execute()`. Alternatively, enforce `SameSite=Strict` or `SameSite=Lax` on session cookies.

---

### FINDING-03

**Severity:** HIGH
**Category:** XSS — Unescaped `bean:write` in HTML Attribute (Timezone Option Value)
**File:** `src/main/webapp/html-jsp/adminRegister.jsp` (line 43)

**Description:**
`TimezoneBean.id` is rendered directly into an HTML `<option value='...'>` attribute using `<bean:write>` with its default `filter="false"` behaviour. In Struts 1.x, `bean:write` does **not** HTML-encode output unless `filter="true"` is explicitly set. If the `arrTimezone` list is populated from database content that an attacker can influence (e.g., through another admin inserting a malicious timezone record), a value containing `'><script>alert(1)</script>` would break out of the attribute and execute in the browser.

The page is publicly accessible (no auth gate), so any user who loads it receives the rendered output. If the data source is even partially attacker-influenced, this is a stored XSS vector on a public page.

**Evidence:**

```jsp
<!-- adminRegister.jsp line 43 — no filter="true" -->
<option value='<bean:write name="timezone" property="id" />'>
    <bean:write name="timezone" property="name"/>
</option>
```

The `id` is rendered inside single-quoted attribute delimiters. A value containing `'` can break the attribute context. The `name` property on line 44 is rendered as element text content without filtering, allowing `<script>` injection there as well.

**Recommendation:**
Add `filter="true"` to both `bean:write` tags on lines 43 and 44:
```jsp
<option value='<bean:write name="timezone" property="id" filter="true" />'>
    <bean:write name="timezone" property="name" filter="true"/>
</option>
```
Additionally, audit the data source for `arrTimezone` to confirm it cannot be influenced by untrusted input.

---

### FINDING-04

**Severity:** HIGH
**Category:** XSS — Unescaped `bean:write` for Message Content
**File:** `src/main/webapp/html-jsp/adminRegister.jsp` (lines 15–19)

**Description:**
The `<html:messages>` block at lines 15–19 renders a message stored under the key `"accountmsg"` using `<bean:write name="accountmsg" />`. As with FINDING-03, `bean:write` in Struts 1.x does not escape HTML by default. The `accountmsg` attribute is set by `AdminRegisterAction` via `saveMessages()` using message resource keys (e.g., `"msg.compUpdate"`), which appear safe because they resolve to static strings from the properties file. However, the pattern establishes a precedent: any future code path that stores user-controlled data under `"accountmsg"` and forwards back to this JSP will result in reflected or stored XSS. Additionally, `error.cognito` messages (line 136 of the Action) embed a raw `errormsg` string from the Cognito API response, and if a Cognito error message ever contains HTML metacharacters, it will pass through unescaped.

**Evidence:**

```jsp
<!-- adminRegister.jsp lines 15–19 -->
<html:messages id="accountmsg" message="true">
    <div class="alert alert-success">
        <bean:write name="accountmsg" />
    </div>
</html:messages>
```

```java
// AdminRegisterAction.java lines 134–136 — Cognito error string placed into ActionErrors
String errormsg = signUpResponse.getMessage();
ActionMessage msg = new ActionMessage("error.cognito", errormsg);
errors.add("AdminRegisterError", msg);
```

If `error.cognito` in the message resources uses a positional parameter (e.g., `error.cognito={0}`) and the `errormsg` from Cognito contains HTML, `<html:errors />` will render it unescaped.

**Recommendation:**
Add `filter="true"` to the `bean:write` tag on line 17. Sanitize or HTML-encode all external error strings (including Cognito API responses) before placing them into `ActionMessage` parameters. Prefer message resource keys that do not embed raw external data.

---

### FINDING-05

**Severity:** HIGH
**Category:** Information Disclosure — Plaintext Password in Registration Email
**File:** `src/main/java/com/action/AdminRegisterAction.java` (lines 174–176)

**Description:**
Upon successful registration, the action constructs an email body that includes the user's plaintext password and sends it to their registered address. Transmitting plaintext passwords in email is a well-established insecure practice: email is not a confidential channel, is stored in sent/received folders, may be forwarded, and may be intercepted. If the system stores a hashed form of the password, sending the original plaintext proves the system either stores plaintext or processes credentials in a way that allows retrieval.

**Evidence:**

```java
// AdminRegisterAction.java lines 174–176
String content = "Your account has been registered succesfully in ForklfitIQ360 and can be used on the Portal Website.<br/>"
        + "Username:" + adminRegisterActionForm.getEmail() + "<br/>"
        + "Password:" + adminRegisterActionForm.getPin();

Util.sendMail(RuntimeConf.REGISTER_SUBJECT, content, "", adminRegisterActionForm.getEmail(), "", RuntimeConf.emailFrom);
```

**Recommendation:**
Do not include the plaintext password in the confirmation email. Send only a confirmation that registration succeeded and prompt the user to set a password via a secure, time-limited link if needed. The credential should never leave the authentication subsystem after the sign-up call.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Authentication / Authorization — Hidden `accountAction` Field is Attacker-Controllable
**File:** `src/main/webapp/html-jsp/adminRegister.jsp` (line 139) / `src/main/java/com/action/AdminRegisterAction.java` (line 76)

**Description:**
The form renders `accountAction` as a hidden field with a default value of `"register"`. Because the endpoint has no CSRF protection and no auth gate, an attacker can craft a POST with `accountAction=update` or `accountAction=add` and reach the `update` or `add` code path in `AdminRegisterAction`. The `update` path calls `compDao.updateCompInfo(companybean, sessUserId, sessionToken)` which relies on session attributes; an unauthenticated request will have a null/empty session, potentially causing a NullPointerException or defaulting to empty strings — but the exact behaviour depends on DAO internals not audited here. The `add` path similarly relies on `sessCompId` from the session.

More critically, the `accountAction` field is not validated to the expected enum of values (`register`, `add`, `update`) before use; it is passed directly to a chain of `equalsIgnoreCase` comparisons. An unexpected value (e.g., `accountAction=delete`) falls through to the else branch which returns a generic error — but the attack surface for future code additions is open.

**Evidence:**

```jsp
<!-- adminRegister.jsp line 139 -->
<html:hidden property="accountAction" value="register" />
```

```java
// AdminRegisterAction.java line 76
if (accountAction.equalsIgnoreCase("register") || accountAction.equalsIgnoreCase("add")) {
```

There is no server-side enforcement that unauthenticated requests can only trigger `accountAction=register`.

**Recommendation:**
On the server side, enforce that unauthenticated callers (no valid `sessCompId` in session) may only use `accountAction=register`. For `add` and `update`, explicitly verify a valid session before proceeding, independently of the servlet filter exclusion list.

---

### FINDING-07

**Severity:** MEDIUM
**Category:** Information Disclosure — Application Internal Name in Email Subject
**File:** `src/main/java/com/util/RuntimeConf.java` (line 13)

**Description:**
The registration confirmation email subject is `"Pandora Registration Successful"` while the product name visible to users and in the email body is `"ForklfitIQ360"`. This mismatch exposes an internal codename (`Pandora`) to all registered users, which may assist attackers in identifying internal systems, related products, or prior security research under that name.

**Evidence:**

```java
// RuntimeConf.java line 13
public static String REGISTER_SUBJECT = "Pandora Registration Successful";
```

**Recommendation:**
Update the subject line to use the public product name to avoid internal codename disclosure.

---

### FINDING-08

**Severity:** MEDIUM
**Category:** Information Disclosure — Typo in Product Name Suggests Low Code Quality Assurance
**File:** `src/main/java/com/action/AdminRegisterAction.java` (line 174)

**Description:**
The confirmation email body contains `"ForklfitIQ360"` (misspelling of `"ForkliftIQ360"`) and `"succesfully"` (missing second `s`). While not a security vulnerability in isolation, these errors indicate the confirmation email content was never reviewed or tested end-to-end, supporting the concern that the surrounding security controls (CSRF token, password handling) may also have gone unreviewed. This is noted as an observation to flag the lack of QA coverage on this code path.

**Evidence:**

```java
// AdminRegisterAction.java line 174
"Your account has been registered succesfully in ForklfitIQ360..."
```

**Recommendation:**
Correct the typos and ensure the email content, including credential handling, undergoes a code review pass.

---

### FINDING-09

**Severity:** LOW
**Category:** Missing Input Validation — No Server-Side Length Constraints on Free-Text Fields
**File:** `src/main/java/com/action/AdminRegisterAction.java` (lines 89–98) / `src/main/java/com/actionform/AdminRegisterActionForm.java`

**Description:**
The `AdminRegisterAction` server-side validation only checks for empty `name`, invalid `email` format, and empty `pin`. No maximum-length validation is applied to any field (`name`, `address`, `contact_fname`, `contact_lname`, `contact_no`, `pin`, etc.). An attacker can submit arbitrarily large values for these fields, potentially causing database truncation errors, log flooding, or Cognito API errors that expose internal error messages. The `AdminRegisterActionForm` extends `ValidatorForm` but the validator XML configuration was not reviewed in this pass; if no `<field maxlength=...>` rules are configured, the gap is confirmed.

**Evidence:**

```java
// AdminRegisterAction.java lines 89–98 — only checks for empty/invalid values, no length check
if (adminRegisterActionForm.getName().trim().equalsIgnoreCase("")) { ... }
else if (...!isValidEmailAddress(adminRegisterActionForm.getEmail())) { ... }
else if (adminRegisterActionForm.getPin().trim().equals("")) { ... }
```

**Recommendation:**
Add maximum-length constraints in the Struts validator XML (`validation.xml`) for all string fields. Enforce these server-side regardless of client-side JS validation.

---

### FINDING-10

**Severity:** LOW
**Category:** Missing Input Validation — Client-Side-Only Password Confirmation Check
**File:** `src/main/webapp/html-jsp/adminRegister.jsp` (lines 170–173) / `src/main/java/com/action/AdminRegisterAction.java`

**Description:**
The password confirmation check (`pass != cpassword`) exists only in the client-side JavaScript function `fnsubmitAccount()`. The `cpassword` field is never sent to or validated by the server; `AdminRegisterAction` only uses `pin`. An attacker submitting a raw POST request bypasses the JS entirely and can register without needing to know the confirm-password value. This is a defence-in-depth gap: while the confirm-password check is a UX feature, its complete absence server-side means there is no assurance the user intended the submitted password.

**Evidence:**

```jsp
<!-- adminRegister.jsp lines 170–173 — JS only -->
else if (pass != cpassword) {
    swal("Error", "Password does not match!\nPlease re-enter confirm password!", "error");
}
```

The `cpassword` field has no corresponding property in `AdminRegisterActionForm` and is not read in `AdminRegisterAction`.

**Recommendation:**
Add server-side confirmation that `pin` and `cpassword` match, or remove the confirm-password field and rely solely on server-side logic.

---

### FINDING-11

**Severity:** INFO
**Category:** Observation — No Rate Limiting on Public Registration Endpoint
**File:** `src/main/java/com/action/AdminRegisterAction.java`

**Description:**
The public `adminRegister.do` endpoint performs Cognito user creation, database inserts, and sends a confirmation email on each successful POST. There is no observable rate limiting, CAPTCHA, or account-creation throttle. This exposes the application to automated abuse: mass account creation, Cognito user pool exhaustion, email flooding from `info@forkliftiq360.com`, and database growth. This observation is noted for completeness; a dedicated rate-limiting or CAPTCHA control review is recommended.

**Recommendation:**
Implement server-side rate limiting (e.g., per IP or per email domain) and a CAPTCHA or proof-of-work challenge on the public registration endpoint.

---

## Section 3 — Category Summaries

| Category | Status | Finding IDs |
|----------|--------|-------------|
| XSS (Unescaped Output) | ISSUES FOUND | FINDING-03, FINDING-04 |
| CSRF | ISSUES FOUND | FINDING-02 |
| Authentication / Authorization | ISSUES FOUND | FINDING-01, FINDING-06 |
| Information Disclosure | ISSUES FOUND | FINDING-05, FINDING-07, FINDING-08 |
| Input Validation | ISSUES FOUND | FINDING-09, FINDING-10 |
| Rate Limiting / Abuse Prevention | ISSUES FOUND (INFO) | FINDING-11 |

---

## Section 4 — Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 2 | FINDING-01, FINDING-02 |
| HIGH | 3 | FINDING-03, FINDING-04, FINDING-05 |
| MEDIUM | 3 | FINDING-06, FINDING-07, FINDING-08 |
| LOW | 2 | FINDING-09, FINDING-10 |
| INFO | 1 | FINDING-11 |
| **TOTAL** | **11** | |

---

## Section 5 — Prioritised Remediation Order

1. **FINDING-01** — Remove `adminRegister.do` from the PreFlight exclusion list or add per-action-path authorization inside the action. This is the root cause that makes all other issues on this endpoint significantly worse.
2. **FINDING-02** — Implement synchronizer CSRF tokens on all POST forms.
3. **FINDING-05** — Stop emailing plaintext passwords immediately.
4. **FINDING-03** — Add `filter="true"` to `bean:write` tags rendering `TimezoneBean` properties.
5. **FINDING-04** — Add `filter="true"` to `bean:write` rendering message content; sanitize Cognito error strings.
6. **FINDING-06** — Add server-side enforcement of allowed `accountAction` values per authentication state.
7. **FINDING-09** — Add maximum-length validation to all form fields in `validation.xml`.
8. **FINDING-10** — Move password confirmation check to the server side.
9. **FINDING-07** — Update email subject to use public product name.
10. **FINDING-08** — Correct typos in email content.
11. **FINDING-11** — Implement CAPTCHA and rate limiting on the public registration endpoint.
