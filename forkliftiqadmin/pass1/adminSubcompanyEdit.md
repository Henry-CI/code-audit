# Security Audit Report — adminSubcompanyEdit.jsp

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**Pass:** 1
**Auditor:** Claude (claude-sonnet-4-6)
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10 (NOT Spring)
**Auth Gate:** PreFlightActionServlet — `sessCompId != null`
**File audited:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`
**Subdirectory scope:** `dealer/` — expected to be accessible only to dealer-level accounts

---

## Section 1 — Reading Evidence

### 1.1 Form Action URLs

| Line | Tag | Action URL | Method | Form ID |
|------|-----|------------|--------|---------|
| 4 | `<html:form>` | `adminRegister` (resolves to `adminRegister.do`) | POST | `adminCompActionForm` |

One form. The Struts `<html:form action="adminRegister">` tag renders as a POST to `adminRegister.do`. No query parameters or context-path manipulation are present.

### 1.2 Request Parameters Used in the Form

All parameters are bound via `<html:text>`, `<html:textarea>`, `<html:select>`, `<html:hidden>`, or plain `<input>` tags. The backing bean for iterated fields is `company` (type `com.bean.CompanyBean`) from the `companyRecord` request attribute.

| Parameter Name | Tag / Element | Line(s) | Bean Property | Notes |
|---------------|---------------|---------|---------------|-------|
| `name` | `<html:text property="name" name="company">` | 24–28 | `CompanyBean.name` | Company name; value populated from CompanyBean |
| `timezone` | `<html:select property="timezone" name="company">` + `<html:options>` | 33–36 | `CompanyBean.timezone` | Populates from `arrTimezone` collection |
| `address` | `<html:textarea property="address" name="company">` | 43–47 | `CompanyBean.address` | Multi-line text area |
| `contact_fname` | `<html:text property="contact_fname" name="company">` | 62–67 | `CompanyBean.contact_fname` | First name |
| `contact_lname` | `<html:text property="contact_lname" name="company">` | 72–76 | `CompanyBean.contact_lname` | Last name |
| `contact_no` | `<html:text property="contact_no" name="company">` | 82–86 | `CompanyBean.contact_no` | Phone number |
| `email` | `<html:text property="email" name="company">` | 92–97 | `CompanyBean.email` | Email address |
| `pin` | `<input type="password" name="pin" value="">` | 102–108 | — (plain HTML, not Struts tag) | Password; hardcoded `value=""` |
| `cpassword` | `<input type="password" name="cpassword" value="">` | 113–119 | — (plain HTML, not Struts tag) | Confirm password; hardcoded `value=""`; not read server-side |
| `accountAction` | `<html:hidden property="accountAction" value="add">` | 133 | `AdminRegisterActionForm.accountAction` | Hardcoded `"add"` — controls action branch server-side |

**Key observation:** `accountAction` is hardcoded to `"add"` in this form. This means submissions from this JSP are routed to the `add` (sub-company creation) branch of `AdminRegisterAction`, not `register` or `update`.

**Key observation:** There is no hidden `id` field on this form. The prior registration form (`adminRegister.jsp`) rendered an `<html:hidden property="id">`. Its absence here means no company ID is submitted; the sub-company parent is derived server-side from `sessCompId`.

### 1.3 Struts Tags That Output Data

| Line | Tag | Property / Key | Escaping |
|------|-----|----------------|----------|
| 22 | `<bean:message key="compName"/>` | i18n resource key | Safe — static lookup |
| 31 | `<bean:message key="timezone"/>` | i18n resource key | Safe — static lookup |
| 34 | `<bean:message key="settings.timezone"/>` | i18n resource key (default option label) | Safe — static lookup |
| 35 | `<html:options collection="arrTimezone" property="id" labelProperty="name" />` | `TimezoneBean.id` (value attr), `TimezoneBean.name` (label text) | See XSS-1 below |
| 41 | `<bean:message key="address"/>` | i18n resource key | Safe — static lookup |
| 55 | `<bean:message key="user"/>` | i18n resource key | Safe — static lookup |
| 60 | `<bean:message key="contactFname"/>` | i18n resource key | Safe — static lookup |
| 70 | `<bean:message key="contactLname"/>` | i18n resource key | Safe — static lookup |
| 80 | `<bean:message key="contactNumber"/>` | i18n resource key | Safe — static lookup |
| 90 | `<bean:message key="email"/>` | i18n resource key | Safe — static lookup |
| 100 | `<bean:message key="admin.entity.password"/>` | i18n resource key | Safe — static lookup |
| 111 | `<bean:message key="driver.acpass"/>` | i18n resource key | Safe — static lookup |
| 131 | `<bean:message key="button.submit">` | i18n resource key | Safe — static lookup |

**Data-bearing Struts tags rendering CompanyBean content:**

| Line | Tag | Property | Escaping Behaviour |
|------|-----|----------|--------------------|
| 24–28 | `<html:text property="name" name="company">` | `CompanyBean.name` | `html:text` HTML-encodes the `value` attribute output — safe |
| 33–36 | `<html:select property="timezone" name="company">` | `CompanyBean.timezone` (selected value) | `html:select` HTML-encodes selected value — safe |
| 35 | `<html:options collection="arrTimezone" property="id" labelProperty="name">` | `TimezoneBean.id`, `TimezoneBean.name` | `html:options` **does not guarantee HTML-escaping** in Struts 1.3.10 — see XSS-1 |
| 43–47 | `<html:textarea property="address" name="company">` | `CompanyBean.address` | `html:textarea` HTML-encodes body content — safe |
| 62–67 | `<html:text property="contact_fname" name="company">` | `CompanyBean.contact_fname` | `html:text` HTML-encodes — safe |
| 72–76 | `<html:text property="contact_lname" name="company">` | `CompanyBean.contact_lname` | `html:text` HTML-encodes — safe |
| 82–86 | `<html:text property="contact_no" name="company">` | `CompanyBean.contact_no` | `html:text` HTML-encodes — safe |
| 92–97 | `<html:text property="email" name="company">` | `CompanyBean.email` | `html:text` HTML-encodes — safe |

### 1.4 JavaScript Blocks Using Server-Side Data

| Lines | Description | Server-Side Data Interpolated? |
|-------|-------------|-------------------------------|
| 137–174 | `fnsubmitAccount()` — reads field values from the DOM via jQuery selectors (`$('[name="name"]').val()`, etc.) and performs client-side validation before calling `$("#adminCompActionForm").submit()` | No server-side data is interpolated into the JS at render time. All values come from DOM reads at runtime. |
| 171–174 | `jQuery(document).ready` — calls `$('#pword').strength()` | No server-side data interpolated. Note: the element with `id="pword"` does not exist in this JSP (the password `<input>` has `name="pin"` and no `id` attribute), making this call a no-op. |

No `<%= ... %>` scriptlet expressions or `${...}` EL interpolations are used to inject server-side values into JS string literals.

---

## Section 2 — Findings

---

### FINDING XSS-1 — MEDIUM: `<html:options>` tag does not guarantee HTML-encoding of `TimezoneBean.id` and `TimezoneBean.name`

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`, line 35
**CWE:** CWE-79 (Improper Neutralization of Input During Web Page Generation — Stored XSS)

**Description:**
The `<html:options>` tag at line 35 renders timezone data from the `arrTimezone` request attribute into `<option value="...">label</option>` markup. In Struts 1.3.10, the `html:options` tag renders the `property` attribute as an HTML attribute value and the `labelProperty` as element text content. The Struts 1.3.x `html:options` tag does **not** apply the same HTML-encoding filter that `html:text` and `html:textarea` apply to their `value` attributes. If the `arrTimezone` collection contains `TimezoneBean` entries whose `id` or `name` fields contain HTML metacharacters (e.g., `"`, `'`, `<`, `>`), those characters will be rendered unescaped into the HTML.

The `arrTimezone` collection is populated by the action class that forwards to this JSP (almost certainly `DealerCompaniesAction` or a related dealer action). If that collection is ultimately sourced from the database and any timezone record was inserted with a malicious payload, this would be a stored XSS vector. The page is protected by the `sessCompId` auth gate (dealer-level access), so exploitation requires a dealer-level or higher session, reducing severity compared to a fully public XSS. However, a compromised or malicious dealer user who has write access to the timezone data table could inject content that fires against other dealer-level users viewing this form.

**Evidence:**
```jsp
<!-- adminSubcompanyEdit.jsp line 33–36 -->
<html:select styleClass="form-control input-lg" name="company" property="timezone">
    <html:option value="0">-- <bean:message key="settings.timezone"/> --</html:option>
    <html:options collection="arrTimezone" property="id" labelProperty="name" />
</html:select>
```

The `html:options` tag generates `<option>` elements from the collection without the explicit `filter="true"` attribute available on `bean:write`. The encoding behaviour depends on the Struts TLD implementation detail, and in Struts 1.3 the `html:options` tag does not uniformly HTML-encode all output. The same pattern was identified in `adminRegister.jsp` (audit report: adminRegister.md, FINDING-03, HIGH), where the timezone collection was rendered via `bean:write` without `filter="true"`. Here the mechanism is different (`html:options`) but the underlying data source and escaping risk are the same.

**Recommendation:**
1. Verify that the timezone data source is controlled exclusively by system administrators and cannot be populated with attacker-controlled values.
2. If there is any path by which an external actor (or a lower-privileged authenticated user) can insert or modify timezone records, this must be treated as HIGH severity and the data must be HTML-encoded before rendering.
3. Apply a pre-render sanitization pass on the `arrTimezone` collection in the action class, ensuring `id` and `name` values contain only expected characters (e.g., alphanumeric, `/`, `_`, `-` for IANA timezone IDs).
4. Consider replacing `<html:options>` with an explicit `<logic:iterate>` loop using `<html:option>` with the value rendered via `<bean:write filter="true">` for guaranteed encoding.

---

### FINDING CSRF-1 — HIGH: No CSRF token on state-changing POST form (sub-company creation)

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`, line 4
**CWE:** CWE-352 (Cross-Site Request Forgery)

**Description:**
The form at line 4 POSTs to `adminRegister.do` with `accountAction=add`, triggering the sub-company creation branch of `AdminRegisterAction`. This is a state-changing operation: it creates a new company record in the database (`CompanyDAO.saveSubCompInfo`), creates a Cognito user identity, and sets up a company relationship under the dealer's `sessCompId`. No CSRF token is present anywhere in the form.

As established in the wider audit of `AdminRegisterAction` (see AdminRegisterAction.md, FINDING CSRF-1), Struts 1.3.10 does not generate CSRF tokens automatically. The Struts `saveToken` / `isTokenValid` mechanism is available but is not used for this action mapping.

A CSRF attack against this form requires the victim to be a dealer-level authenticated user (because the `sessCompId` auth gate applies to the `dealer/` path). An attacker who can induce a dealer user to visit a crafted page could silently create sub-company records under that dealer's account, triggering Cognito identity creation and consuming system resources.

**Evidence:**
```jsp
<!-- adminSubcompanyEdit.jsp line 4 — no token field, no CSRF mechanism -->
<html:form method="post" action="adminRegister" styleClass="ajax_mode_c" styleId="adminCompActionForm">
```

```jsp
<!-- adminSubcompanyEdit.jsp line 133 — only hidden field is the action discriminator -->
<html:hidden property="accountAction" value="add" />
```

No `<html:hidden property="token">` or equivalent synchronizer token field is present. The static value `accountAction=add` is known and guessable, providing no CSRF protection.

**Recommendation:**
Implement the Struts synchronizer token pattern for this form:
1. In the action class that populates this JSP (before forwarding to the `add` form), call `saveToken(request)`.
2. In `AdminRegisterAction.execute()` on the `add` branch, call `isTokenValid(request, true)` and return an error forward if the token is missing or invalid.
3. Render the token as a hidden field using `<html:hidden property="token" />` or the Struts `token` tag.
Alternatively, enforce `SameSite=Strict` on the session cookie as a defence-in-depth measure.

---

### FINDING AUTH-1 — HIGH: `accountAction=add` branch depends on session-gated auth, but no in-action role verification confirms dealer privilege

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`, line 133
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 194–210
**CWE:** CWE-285 (Improper Authorization)

**Description:**
This JSP is located in the `dealer/` subdirectory and is described as accessible only to dealer-level accounts. The auth gate (`PreFlightActionServlet`) checks only that `sessCompId != null` — it does not check the role of the authenticated account. Any authenticated user with a valid session (including `ROLE_COMP`, `ROLE_SUBCOMP`, `ROLE_SITE_ADMIN`) who can reach this form can submit it and trigger the `add` branch of `AdminRegisterAction`.

The `AdminRegisterAction.execute()` method on the `add` path (lines 194–210) reads session attributes `sessCompId`, `sessAccountId`, `sessUserId`, `sessionToken`, and the boolean flags `isSuperAdmin` / `isDealerLogin`. The `isDealerLogin` flag is checked on the list-display branch (`getCompanyContactsByCompId` at line 204) only to differentiate which companies to display — it is **not** used to gate whether the `add` operation is permitted. A `ROLE_COMP` (regular company) user who submits `accountAction=add` will have `isDealerLogin=false` but will still reach line 195 (`compDao.saveSubCompInfo(sessCompId, companybean)`) and attempt to insert a sub-company record.

This means a non-dealer authenticated user can create sub-companies under their own company, a privilege that should be restricted to dealer-level accounts.

**Evidence:**
```jsp
<!-- adminSubcompanyEdit.jsp line 133 -->
<html:hidden property="accountAction" value="add" />
```

```java
// AdminRegisterAction.java lines 194–210 (from prior audit AdminRegisterAction.md)
// accountAction == "add" branch:
compId = compDao.saveSubCompInfo(sessCompId, companybean);   // line 195
// No check: if (!isDealerLogin) { return error; }
// isDealerLogin is only used later (line 202) for the getCompanies() display query
```

The Tiles definition for this form (`dealerCompaniesAddDefinition`, referenced from adminCompany.md context) is accessible from the `dealercompanies.do?action=add` flow, which is reached from the dealer company list. However, the underlying `adminRegister.do` action accepts the POST from any authenticated caller regardless of the Tiles entry point.

**Recommendation:**
Add an explicit role check in `AdminRegisterAction.execute()` before the `add` branch proceeds:
```java
Boolean isDealerLogin = (Boolean) session.getAttribute("isDealerLogin");
Boolean isSuperAdmin  = (Boolean) session.getAttribute("isSuperAdmin");
if (accountAction.equalsIgnoreCase("add")) {
    if ((isDealerLogin == null || !isDealerLogin)
            && (isSuperAdmin == null || !isSuperAdmin)) {
        // Not a dealer or superadmin — deny
        response.sendError(HttpServletResponse.SC_FORBIDDEN);
        return null;
    }
}
```
The pre-flight servlet should also be enhanced to enforce role-based routing for the `dealer/` subdirectory path.

---

### FINDING AUTH-2 — HIGH: `accountAction` hidden field is attacker-controllable — non-dealer users can reach `update` branch

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`, line 133
**File:** `src/main/java/com/action/AdminRegisterAction.java`, lines 246–265
**CWE:** CWE-285 (Improper Authorization) / CWE-807 (Reliance on Untrusted Inputs in a Security Decision)

**Description:**
The form renders `accountAction` as a hidden field with value `"add"`. Because this is a client-side hidden field, any authenticated user submitting a crafted POST can change `accountAction` to `"update"`, triggering the company profile update branch of `AdminRegisterAction`. The `update` branch calls `compDao.updateCompInfo(companybean, sessUserId, sessionToken)` (line 248), which modifies the company record associated with the current session's `sessUserId`.

There is no server-side enforcement that an authenticated session that reached this form via the `dealer/` subdirectory is restricted to `accountAction=add`. The server processes whatever `accountAction` value is submitted.

This is a separate issue from AUTH-1: even a dealer user legitimately viewing this "add sub-company" form could modify the hidden field to `"update"` and update their own (or another, depending on the `id` handling) company record rather than creating a new one.

**Evidence:**
```jsp
<!-- adminSubcompanyEdit.jsp line 133 — client-supplied, no server-side enforcement -->
<html:hidden property="accountAction" value="add" />
```

The prior audit of `AdminRegisterActionForm` (AdminRegisterActionForm.md, FINDING-02, CRITICAL) confirms that `accountAction` is an open String field with no whitelist validation. The prior audit of `AdminRegisterAction` (AdminRegisterAction.md, FINDING V-4, MEDIUM) confirms the action uses `equalsIgnoreCase` comparisons without an allowlist guard.

**Recommendation:**
In `AdminRegisterAction.execute()`, validate `accountAction` against an explicit allowlist before any processing. Additionally, each allowed value should be gated by the appropriate session role check (as described in AUTH-1). For the specific case of this JSP (which should only trigger `add`), the action should verify that the form entry point is consistent with the `add` operation.

---

### FINDING AUTH-3 — MEDIUM: No server-side verification that the `add` operation targets the authenticated dealer's own tenant

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminRegisterAction.java`, line 195
**CWE:** CWE-639 (Authorization Bypass Through User-Controlled Key — IDOR)

**Description:**
On the `add` path, the parent company ID for the new sub-company is taken from `sessCompId` (the session attribute). The JSP does not submit a `parentCompanyId` parameter, and `saveSubCompInfo(sessCompId, companybean)` uses the session value directly. This is correct in principle — the parent is the dealer's own company, taken from the session.

However, `AdminRegisterAction` (per AdminRegisterAction.md) reads `sessCompId` from the session with no null guard, and there is no server-side assertion that the `sessCompId` in the session actually corresponds to a company with `ROLE_DEALER`. If a `ROLE_COMP` or `ROLE_SITE_ADMIN` user has a `sessCompId` set to a dealer company's ID (e.g., via session fixation or a misconfigured `SwitchCompanyAction`), they would create sub-companies under that dealer's account, not their own.

The `adminCompany.md` audit notes (FINDING-06) document that `SwitchCompanyAction` allows an authenticated user to change `sessCompId` to any company in `sessArrComp`, and that if `sessArrComp` is not tightly scoped at login, cross-tenant company ID access is possible.

**Evidence:**
```java
// AdminRegisterAction.java line 195 — parent derived from session only
compId = compDao.saveSubCompInfo(sessCompId, companybean);
// No assertion: "companyWithId(sessCompId).role == ROLE_DEALER"
```

**Recommendation:**
Before calling `saveSubCompInfo`, verify that the company identified by `sessCompId` holds the `ROLE_DEALER` role. This check should be performed against the database, not against a session flag that could be manipulated.

---

### FINDING INFO-1 — LOW: Password confirmation check is client-side only; `cpassword` field is not validated server-side

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`, lines 113–119, 158–160
**CWE:** CWE-603 (Use of Client-Side Authentication)

**Description:**
The form includes a "Confirm Password" field (`<input name="cpassword" type="password">`). The JavaScript function `fnsubmitAccount()` checks that `pass == cpassword` before allowing form submission (lines 158–160). If the passwords do not match, a SweetAlert error is shown.

However, `cpassword` is not a property of `AdminRegisterActionForm` and is not read or validated in `AdminRegisterAction`. An attacker submitting a raw HTTP POST bypasses the JavaScript entirely and can submit `pin` without a matching `cpassword`, with no server-side rejection. The confirmation check provides zero security guarantee.

This mirrors the same issue found in `adminRegister.jsp` (adminRegister.md, FINDING-10).

**Evidence:**
```jsp
<!-- adminSubcompanyEdit.jsp lines 113–119 -->
<input class="form-control input-lg" name="cpassword" type="password"
       placeholder="Confirm Password" value=""/>
```
```javascript
// adminSubcompanyEdit.jsp lines 158–160
else if (pass != cpassword) {
    swal("Error", "Password does not match!\nPlease re-enter confirm password!", "error");
}
```

`cpassword` has no corresponding property in `AdminRegisterActionForm` and is absent from `AdminRegisterAction`'s processing.

**Recommendation:**
Add a server-side check in `AdminRegisterAction.execute()` that the submitted `pin` and `cpassword` values match before proceeding with account creation. This can be done by adding `cpassword` to `AdminRegisterActionForm` (or reading it directly from `request.getParameter("cpassword")`), then asserting equality with `pin` before the DAO call.

---

### FINDING INFO-2 — LOW: Dead jQuery `strength()` call references a non-existent element ID

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`, lines 171–174
**CWE:** N/A (code quality / security control ineffective)

**Description:**
The `document.ready` block at lines 171–174 calls `$('#pword').strength()`, which is intended to invoke a password-strength meter plugin on the password field. However, no element with `id="pword"` exists anywhere in this JSP. The password `<input>` at line 102 has `name="pin"` and no `id` attribute.

```javascript
jQuery(document).ready(function($) {
    $('#pword').strength();
});
```

This means the password-strength meter is silently inactive on this form. Users are given no visual indication of password strength when creating sub-company accounts via this form. The strength meter presumably works on the `adminRegister.jsp` form (where it may have been written), but it was not adapted when this form was created.

The absence of the strength meter reduces the likelihood that users will choose strong passwords, compounding the weak password policy finding documented in AdminRegisterActionForm.md (FINDING-03, FINDING-04).

**Recommendation:**
Add `id="pword"` to the `<input name="pin">` element at line 102, or update the selector to `$('[name="pin"]').strength()`. Verify the password strength plugin is loaded by the page template.

---

### FINDING INFO-3 — INFO: `companyRecord` iteration renders CompanyBean fields into Struts `html:text` / `html:textarea` tags — XSS mitigation relies on Struts encoding

**Severity:** INFO
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`, lines 10–123
**CWE:** CWE-79 (Stored XSS — mitigated by framework default, not explicit declaration)

**Description:**
The `<logic:iterate>` block (lines 11–123) iterates over `companyRecord` and populates Struts form tags with `CompanyBean` field values. The tags used — `<html:text>`, `<html:textarea>`, `<html:select>` — all HTML-encode their output by default in Struts 1.3.10. This means stored XSS from database-sourced values in `name`, `address`, `contact_fname`, `contact_lname`, `contact_no`, and `email` fields is mitigated by the framework default behaviour.

This is informational rather than a finding: the encoding is correct, but it relies on framework default behaviour rather than explicit `filter="true"` declarations. If a developer modifies these tags or substitutes them with `bean:write` (which defaults to `filter="false"` in some read contexts), stored XSS could be introduced.

**Recommendation:**
No immediate action required. For defence-in-depth, add explicit encoding declarations where possible and document the expected encoding behaviour in code comments.

---

### FINDING INFO-4 — INFO: This form performs the same action as `adminRegister.jsp` (`accountAction=add`) — dual entry points to the same state-changing action

**Severity:** INFO
**File:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp` vs `src/main/webapp/html-jsp/adminRegister.jsp`

**Description:**
Both this JSP and `adminRegister.jsp` POST to `adminRegister.do`. The public `adminRegister.jsp` uses `accountAction=register` and is excluded from the auth gate. This JSP uses `accountAction=add` and is expected to be auth-gated (dealer-level). Having two different JSPs with overlapping action targets on the same endpoint creates ambiguity about what is and is not protected. The critical vulnerability documented in `AdminRegisterAction.md` (FINDING AUTH-1, CRITICAL) — that `adminRegister.do` is on the PreFlight exclusion list, making `add` reachable without authentication — directly affects this form's underlying action.

This is not a new finding for this JSP specifically, but it is important context: the action this form targets (`adminRegister.do`, `accountAction=add`) can also be reached unauthenticated by a direct HTTP POST, bypassing the dealer-level session gate entirely.

**Cross-reference:** AdminRegisterAction.md, FINDING AUTH-1 (CRITICAL).

---

## Section 3 — Category Summaries

| Category | Status | Finding IDs |
|----------|--------|-------------|
| XSS (Unescaped Output to HTML/JS) | ISSUE FOUND | XSS-1 (MEDIUM) |
| CSRF (POST to state-changing action) | ISSUE FOUND | CSRF-1 (HIGH) |
| Authentication / Authorization | ISSUES FOUND | AUTH-1 (HIGH), AUTH-2 (HIGH), AUTH-3 (MEDIUM) |
| Information Disclosure | NO DIRECT ISSUES | — (see cross-refs to AdminRegisterAction.md) |
| Sensitive Data Rendered | NO ISSUES | Passwords are `type="password"` with hardcoded empty values; no credential data is pre-populated |
| Input Validation | PARTIAL — LOW | INFO-1 (client-side confirm only) |
| Code Quality / Dead Code | ISSUE FOUND | INFO-2 (LOW) |

**Categories with NO issues:**
- **Information Disclosure (JSP-level):** No server-side data (session values, internal identifiers, stack traces, internal paths) is rendered into the HTML output or into JavaScript string literals. All i18n keys resolve to static strings. No `<%= ... %>` scriptlet output is present.
- **Sensitive Data Rendered:** The password and confirm-password fields use `type="password"` with hardcoded `value=""`. No existing credential data from the CompanyBean is pre-populated into password fields. The `pin` and `cpassword` fields are plain HTML `<input>` tags, not Struts bean-bound tags, ensuring no accidental value pre-population from the form bean.
- **Path Traversal:** No file system operations are initiated from this JSP or its immediate action.
- **Redirect Injection:** No redirect targets are constructed from user input; all forwards use named Struts forward aliases.
- **JavaScript Injection:** No server-side values are interpolated into JS string literals at render time.

---

## Section 4 — Summary Table

| ID | Severity | Category | File | Line(s) | Short Description |
|----|----------|----------|------|---------|-------------------|
| CSRF-1 | HIGH | CSRF | adminSubcompanyEdit.jsp | 4, 133 | No CSRF token on sub-company creation POST |
| AUTH-1 | HIGH | Authorization | adminSubcompanyEdit.jsp:133 / AdminRegisterAction.java:194 | 133 / 194 | No role check — non-dealer users can trigger `add` branch |
| AUTH-2 | HIGH | Authorization | adminSubcompanyEdit.jsp:133 / AdminRegisterAction.java:246 | 133 / 246 | Hidden `accountAction` field is attacker-controllable; can switch to `update` branch |
| XSS-1 | MEDIUM | XSS | adminSubcompanyEdit.jsp | 35 | `html:options` timezone rendering — escaping not guaranteed |
| AUTH-3 | MEDIUM | IDOR / Authorization | AdminRegisterAction.java | 195 | No verification that `sessCompId` belongs to a dealer-role company |
| INFO-1 | LOW | Input Validation | adminSubcompanyEdit.jsp | 113–119, 158–160 | Password confirmation is client-side only; `cpassword` not validated server-side |
| INFO-2 | LOW | Code Quality / Security Control | adminSubcompanyEdit.jsp | 171–174 | Dead `$('#pword').strength()` call — password strength meter inactive |
| INFO-3 | INFO | XSS (mitigated) | adminSubcompanyEdit.jsp | 10–123 | Struts tag HTML-encoding mitigates stored XSS; relies on framework default |
| INFO-4 | INFO | Architecture | adminSubcompanyEdit.jsp / adminRegister.do | 4 | Dual entry point to same action; `add` branch reachable unauthenticated (cross-ref AUTH-1 in AdminRegisterAction.md) |

---

## Section 5 — Finding Count by Severity

| Severity | Count | IDs |
|----------|-------|-----|
| CRITICAL | 0 | — |
| HIGH | 3 | CSRF-1, AUTH-1, AUTH-2 |
| MEDIUM | 2 | XSS-1, AUTH-3 |
| LOW | 2 | INFO-1, INFO-2 |
| INFO | 2 | INFO-3, INFO-4 |
| **TOTAL** | **9** | |

---

## Section 6 — Prioritised Remediation Order

1. **AUTH-2** — Validate and allowlist `accountAction` server-side before use; enforce that only the appropriate value (`add`) is processed for this form's context, and gate each branch by role.
2. **AUTH-1** — Add explicit dealer-role check in `AdminRegisterAction.execute()` before the `add` branch proceeds.
3. **CSRF-1** — Implement the Struts synchronizer token pattern for this form.
4. **AUTH-3** — Add server-side assertion that `sessCompId` belongs to a `ROLE_DEALER` company before creating sub-company records.
5. **XSS-1** — Verify timezone data source trust; replace `html:options` with an explicit iterate loop using `bean:write filter="true"`.
6. **INFO-1** — Add server-side password confirmation match check in `AdminRegisterAction`.
7. **INFO-2** — Fix the `#pword` selector / add the missing `id` attribute to the password input.

**Note on cross-cutting issues:** The root cause of AUTH-1 and AUTH-2 is the architectural decision to place `adminRegister.do` on the PreFlight exclusion list (documented as CRITICAL in AdminRegisterAction.md, FINDING AUTH-1). Remediation of that root cause will automatically strengthen the protections here.
