# Security Audit: adminUser.jsp

**File:** `src/main/webapp/html-jsp/adminUser.jsp`
**Audit run:** audit/2026-02-26-01
**Auditor:** Claude Sonnet 4.6 (automated pass1)
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10 (NOT Spring)

---

## 1. Reading Evidence

### Form Action URLs

| Line | Method | Action URL | Purpose |
|------|--------|-----------|---------|
| 20 | GET | `admindriver.do` | Search/list users (form submit) |
| 34 | GET (link) | `admindriver.do?action=adduser` | Open Add User lightbox |
| 64 | GET (link) | `admindriver.do?action=edituser&driverId=<bean:write .../>` | Open Edit User lightbox |

### Request Parameters Used in Output or JS

| Line | Parameter | Source | Usage |
|------|-----------|--------|-------|
| 4 | `searchDriver` | `request.getParameter(...)` | Stored in scriptlet variable `searchDriver` |
| 25 | `searchDriver` | Scriptlet variable from line 4 | Reflected directly into HTML input `value` attribute via `<%= searchDriver %>` |

### Struts Tags That Output Data

| Line | Tag | Bean | Property | filter default |
|------|-----|------|----------|---------------|
| 64 | `<bean:write>` | `driverRecord` | `id` | `true` (HTML context — URL attribute) |
| 67 | `<bean:write>` | `driverRecord` | `id` | `true` (HTML class attribute) |
| 73 | `<bean:write>` | `driverRecord` | `id` | `true` (HTML data attribute) |
| 79 | `<bean:write>` | `driverRecord` | `first_name` | `true` (HTML text node) |
| 82 | `<bean:write>` | `driverRecord` | `last_name` | `true` (HTML text node) |
| 84 | `<bean:write>` | `driverRecord` | `email_addr` | `true` (HTML text node) |
| 85 | `<bean:write>` | `driverRecord` | `phone` | `true` (HTML text node) |
| 43 | `<html:errors/>` | — | — | Struts HTML errors tag |

### JavaScript Blocks Using Server-Side Data

- No `<script>` block in this file directly embeds server-side data.
- JS interaction happens via `data-delete-value` and `data-method-action` HTML data attributes (lines 71–74), which are consumed by `scripts.js` (lines 56–114) using `$(this).attr(...)`. The values written into those attributes are `<bean:write property="id">` (a Long) and the literal string `"delete_user"`.
- The jQuery delete handler in `scripts.js` (lines 74, 100) performs `$.post('./admindriver.do', {...})` — a plain AJAX POST — passing `action` and `driverId` values sourced from those data attributes.

---

## 2. Audit Findings

---

### XSS (Cross-Site Scripting)

---

#### FINDING XSS-1 — HIGH

**Severity:** HIGH
**File+Line:** `src/main/webapp/html-jsp/adminUser.jsp`, line 25
**Description:** The request parameter `searchDriver` is read directly from `request.getParameter()` in a scriptlet (line 4) and reflected unescaped into the HTML `value` attribute of an `<input>` element using a JSP expression (`<%= searchDriver %>`). There is no call to `ESAPI.encoder().encodeForHTML()`, `StringEscapeUtils.escapeHtml4()`, or any equivalent. The value is written inside a double-quoted HTML attribute, so a payload of `" onmouseover="alert(1)` or `"><script>alert(1)</script>` would break out and execute arbitrary JavaScript.

**Evidence:**
```jsp
// Line 4
String searchDriver = request.getParameter("searchDriver") == null ? "" : request.getParameter("searchDriver");

// Line 24-25
<input type="text" name="searchDriver" class="form-control input-lg" placeholder="Search"
       value="<%=searchDriver %>"/>
```

The form uses `method="get"` and `action="admindriver.do"`, making the reflected payload trivially shareable via a crafted URL. Any admin user who clicks a malicious link will have the payload execute in their browser session.

**Recommendation:** Replace `<%= searchDriver %>` with a properly HTML-attribute-escaped value. Options in order of preference:
1. Use `<html:text property="searchDriver" .../>` from the Struts HTML tag library, which applies `filter=true` by default.
2. Use OWASP ESAPI: `<%=ESAPI.encoder().encodeForHTMLAttribute(searchDriver)%>`.
3. At minimum, use `<%=org.apache.commons.lang.StringEscapeUtils.escapeHtml(searchDriver)%>` (already on the classpath via Struts/Commons).

---

#### FINDING XSS-2 — LOW

**Severity:** LOW
**File+Line:** `src/main/webapp/html-jsp/adminUser.jsp`, lines 64, 67, 73
**Description:** `<bean:write property="id" name="driverRecord"/>` is used three times inside HTML attribute values: an `href` URL query string, an element `class` attribute, and a `data-delete-value` attribute. The `id` property is typed as `Long` in `DriverBean` (line 14 of `DriverBean.java`), so under normal DB-populated conditions this will always be a numeric string and cannot carry an XSS payload. However, the `filter="true"` default on `<bean:write>` applies HTML entity escaping rather than JavaScript-context or URL-context escaping.

The `href` attribute on line 64 constructs a URL via string concatenation; a numeric `id` is safe here. The `class` attribute on line 67 (`class="driver<bean:write ...>"`) would be unsafe if `id` were ever a string type or the bean property type changed. The `data-delete-value` attribute on line 73 feeds directly into a jQuery `$.post` parameter — safe for a numeric Long.

This is LOW rather than MEDIUM because the property is a database-sourced `Long`, not a user-controlled string. The risk becomes higher if the type is ever widened.

**Evidence:**
```jsp
// Line 64
href="admindriver.do?action=edituser&driverId=<bean:write property="id" name="driverRecord"/>"

// Line 67
class="driver<bean:write property="id" name="driverRecord"/>"

// Line 73
data-delete-value="<bean:write property="id" name="driverRecord"/>"
```

**Recommendation:** Use explicit attribute-context escaping even for numeric outputs to be defensive against future type changes. For URL parameters, apply URL encoding in addition to HTML attribute encoding.

---

#### FINDING XSS-3 — MEDIUM

**Severity:** MEDIUM
**File+Line:** `src/main/webapp/html-jsp/adminUser.jsp`, lines 79, 82, 84, 85
**Description:** `<bean:write>` outputs `first_name`, `last_name`, `email_addr`, and `phone` from `DriverBean` directly into HTML table cell text nodes. The Struts 1.3 `<bean:write>` tag applies `filter="true"` by default, which converts `<`, `>`, `&`, `"`, and `'` to HTML entities. This provides protection against basic reflected XSS in text-node context.

However, `filter="true"` in Struts 1.3 is documented to perform only minimal escaping and does NOT cover all Unicode-based bypass vectors. More critically, the fields `first_name`, `last_name`, `email_addr`, and `phone` are user-supplied PII values that are stored in the database and then rendered back; this is a **stored XSS** surface. If an attacker can register a user (via the add-user flow, `admindriver.do?action=adduser`) with a crafted name containing HTML-breaking characters that survive DB storage and defeat the `filter="true"` encoding, the payload executes for every admin who loads this page.

The actual exploitability depends on whether input validation/sanitisation occurs in `AdminDriverAddAction` and `DriverDAO.addDriverInfo()`/`DriverDAO.saveUsers()` — which were not found to contain explicit input sanitisation in the reviewed action code.

**Evidence:**
```jsp
// Lines 79, 82, 84, 85
<bean:write property="first_name" name="driverRecord"/>
<bean:write property="last_name" name="driverRecord"/>
<bean:write property="email_addr" name="driverRecord"/>
<bean:write property="phone" name="driverRecord"/>
```
`DriverBean.java` fields are plain `String` with no sanitisation annotations.

**Recommendation:** Audit `DriverDAO.addDriverInfo()` and `DriverDAO.saveUsers()` for input sanitisation. Apply a content security policy header. Consider replacing `<bean:write>` with explicit ESAPI HTML encoding for PII fields.

---

### CSRF (Cross-Site Request Forgery)

---

#### FINDING CSRF-1 — HIGH

**Severity:** HIGH
**File+Line:** `src/main/webapp/html-jsp/adminUser.jsp`, lines 70–76; `src/main/webapp/skin/js/scripts.js`, lines 90–113
**Description:** The delete-user operation is performed by a jQuery `$.post` AJAX call to `admindriver.do` with `action=deleteUser` and `driverId=<value>`. This is a state-changing (destructive) POST request. No CSRF token is present anywhere: not in the form, not in the AJAX call, not as a custom header. The `PreFlightActionServlet` only checks that `sessCompId` is non-null in the session — it does not validate any anti-CSRF token.

A malicious page visited by an authenticated admin can silently issue `$.post` (or a plain form POST) to `./admindriver.do` with `action=deleteUser` and any `driverId` to delete arbitrary users. Because the session cookie is attached automatically by the browser, the attack succeeds without any user interaction beyond visiting the attacker's page.

**Evidence:**
```javascript
// scripts.js lines 100-103
$.post('./admindriver.do', {
    'action': "deleteUser",
    'driverId': value
}, function (data) { ... })
```
```jsp
// adminUser.jsp line 73 — driverId value sourced from data attribute, no token:
data-delete-value="<bean:write property="id" name="driverRecord"/>"
```
```java
// AdminOperatorAction.java lines 52-53 — no token check:
case "deleteuser":
    return mapping.findForward(deleteUserAction(request, driverId, sessCompId, sessionToken));
```

**Recommendation:** Implement a synchroniser-token pattern. Generate a cryptographically random token per-session (or per-form), store it in the session, and require it on every state-changing request. For AJAX calls, embed the token in a meta tag or hidden field and include it as a request header or POST parameter. Validate in `PreFlightActionServlet` or in a Struts `RequestProcessor` subclass before action dispatch.

---

#### FINDING CSRF-2 — MEDIUM

**Severity:** MEDIUM
**File+Line:** `src/main/webapp/html-jsp/adminUser.jsp`, line 20; linked to `admindriver.do?action=adduser` (line 34)
**Description:** The search form (line 20) uses `method="get"` and is therefore not a CSRF risk itself (GET is idempotent per HTTP). However, the Add User action is triggered by a GET link (`admindriver.do?action=adduser`, line 34) which opens a lightbox modal containing a form. The actual user-creation POST goes to `admindriveradd.do` (Struts config line 303). That downstream form has no CSRF token either (confirmed by reviewing `AdminDriverAddAction.java` and `AdminDriverAddForm.java` — no token fields). This is catalogued here as context for the CSRF-1 finding. The lightbox link itself is not exploitable as a CSRF vector for destructive mutation, but the form it loads is.

**Evidence:**
```jsp
// Line 34
<a href="admindriver.do?action=adduser" ... data-toggle="lightbox" ...>Add</a>
```

**Recommendation:** As per CSRF-1, apply synchroniser tokens to all state-changing forms loaded via the lightbox modals.

---

### Authentication / Authorization

---

#### FINDING AUTHN-1 — MEDIUM

**Severity:** MEDIUM
**File+Line:** `src/main/java/com/actionservlet/PreFlightActionServlet.java`, lines 56–60; `src/main/java/com/action/AdminOperatorAction.java`, lines 27–59
**Description:** Authentication is gated solely on `sessCompId != null && !sessCompId.equals("")` in `PreFlightActionServlet`. There is no role-based authorization check in `AdminOperatorAction`. Any authenticated session — regardless of whether the user is a site admin, a driver, or any other role — can reach `admindriver.do` and invoke the `delete`, `deleteuser`, `edituser`, `adduser` actions. A lower-privileged user who has a valid session (e.g., obtained via the driver mobile app or a different admin panel) could enumerate and delete all users of any company.

Contrast this with `AdminDriverAddAction.java` line 92, where `compDao.saveUserRoles(userId, RuntimeConf.ROLE_SITEADMIN)` is called — meaning user creation grants site-admin role, but the action itself is not restricted to only existing site admins.

**Evidence:**
```java
// PreFlightActionServlet.java lines 56-60
else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
```
```java
// AdminOperatorAction.java lines 27-59 — no role check before switch:
String sessCompId = getSessionAttribute(session, "sessCompId", "");
String action = getRequestParam(request, "action", "");
switch (action.toLowerCase()) {
    case "deleteuser":
        return mapping.findForward(deleteUserAction(...));
```

**Recommendation:** Add a role-based authorization check at the top of `AdminOperatorAction.execute()`. Verify that the session contains a role attribute (e.g., `sessRole == ROLE_SITEADMIN`) before allowing access to user management operations. This check should also be applied in `AdminDriverAddAction` and `AdminDriverEditAction`.

---

#### FINDING AUTHN-2 — MEDIUM

**Severity:** MEDIUM
**File+Line:** `src/main/java/com/action/AdminOperatorAction.java`, lines 134–144; `src/main/webapp/html-jsp/adminUser.jsp`, lines 70–76
**Description:** The delete operations (`deleteAction` and `deleteUserAction`) use the `driverId` supplied as a GET/POST parameter without verifying that the target user belongs to the currently authenticated company (`sessCompId`). `deleteUserAction` calls `DriverDAO.delUserById(driverId, sessionToken)` with no company scope check. An authenticated attacker can iterate numeric `driverId` values to delete users belonging to other companies (insecure direct object reference, IDOR).

`deleteAction` passes `compId` to `DriverDAO.delDriverById(driverId, compId)` — this may include a company check at the DAO level, but `deleteUserAction` does not pass `compId` to the delete call at all.

**Evidence:**
```java
// AdminOperatorAction.java lines 140-143
private String deleteUserAction(HttpServletRequest request, Long driverId, String compId, String sessionToken) throws Exception {
    DriverDAO.delUserById(driverId, sessionToken);  // compId not passed to delete call
    request.setAttribute("arrAdminDriver", DriverDAO.getAllUser(compId, sessionToken));
    return "operatorlist";
}
```

**Recommendation:** Ensure all data-access operations for user management are scoped by `sessCompId`. In `DriverDAO.delUserById()`, verify the target `driverId` belongs to `compId` before executing the delete. Apply the same ownership check to edit and subscription operations.

---

### Information Disclosure

---

#### FINDING INFO-1 — MEDIUM

**Severity:** MEDIUM
**File+Line:** `src/main/java/com/bean/DriverBean.java`, lines 37–39; rendered indirectly via edit actions
**Description:** `DriverBean` contains sensitive credential fields: `pass` (plaintext password), `cpass` (confirm password), and `pass_hash` (MD5 hash — see `users/general.jsp` line 190 for MD5 hashing evidence). While `adminUser.jsp` itself only renders `first_name`, `last_name`, `email_addr`, and `phone`, the same `DriverBean` objects are stored in request scope (`arrAdminDriver`) and passed to subsequent views. If any other JSP in the response chain inadvertently outputs additional bean properties (e.g., via a debug tag or a future developer adding `<bean:write property="pass_hash"/>`), credential data would be disclosed.

The immediate risk to this file is LOW. The broader DriverBean design is the concern: credential fields should never be in the same bean as display data, and MD5 is cryptographically broken for password storage.

**Evidence:**
```java
// DriverBean.java lines 37-39
private String pass = null;
private String cpass = null;
private String pass_hash = null;
```
```java
// AdminOperatorAction.java line 142
request.setAttribute("arrAdminDriver", DriverDAO.getAllUser(compId, sessionToken));
```

**Recommendation:** Remove `pass`, `cpass`, and `pass_hash` from `DriverBean`. Use a separate credential DTO for authentication operations. Migrate from MD5 to bcrypt or Argon2 for password storage.

---

#### FINDING INFO-2 — LOW

**Severity:** LOW
**File+Line:** `src/main/webapp/html-jsp/adminUser.jsp`, line 84
**Description:** User email addresses are rendered in plaintext in the table (`<bean:write property="email_addr" name="driverRecord"/>`). This is expected in an admin interface, but it means email addresses of all users are exposed to any authenticated session regardless of role (see AUTHN-1). Combined with the missing authorization check, any authenticated user can harvest all email addresses in the company.

**Evidence:**
```jsp
// Line 84
<td><bean:write property="email_addr" name="driverRecord"/></td>
```

**Recommendation:** Restrict this page to site-admin role (see AUTHN-1). Consider partial masking of email addresses in list views if the role model is broadened.

---

### Sensitive Data Rendered

---

#### FINDING SENS-1 — INFO

**Severity:** INFO
**File+Line:** `src/main/webapp/html-jsp/adminUser.jsp`, lines 79–85
**Description:** The following PII fields are rendered in the user listing table: `first_name`, `last_name`, `email_addr`, `phone`. This is appropriate for an admin user-management interface and expected by design. No passwords, tokens, or cryptographic material are directly rendered by this JSP. Noted for completeness.

**No additional issues found in this category beyond what is covered by INFO-1 and INFO-2 above.**

---

## 3. Summary Table

| ID | Severity | Category | Line(s) | Title |
|----|----------|----------|---------|-------|
| XSS-1 | HIGH | XSS | 4, 25 | Reflected XSS via unescaped `searchDriver` parameter in input value attribute |
| XSS-2 | LOW | XSS | 64, 67, 73 | `bean:write id` in HTML attributes — safe now due to Long type, brittle by design |
| XSS-3 | MEDIUM | XSS | 79, 82, 84, 85 | Stored XSS surface: user PII fields rendered via `bean:write` with only default filter |
| CSRF-1 | HIGH | CSRF | 70–76 (JSP), scripts.js 90–113 | Delete-user AJAX POST has no CSRF token |
| CSRF-2 | MEDIUM | CSRF | 34 | Add-user lightbox flow has no CSRF token on the downstream POST |
| AUTHN-1 | MEDIUM | Authorization | PreFlightActionServlet 56–60, AdminOperatorAction 27–59 | No role check — any authenticated session can perform user management operations |
| AUTHN-2 | MEDIUM | Authorization | AdminOperatorAction 140–143 | IDOR on delete-user: driverId not scoped to sessCompId |
| INFO-1 | MEDIUM | Information Disclosure | DriverBean 37–39 | DriverBean carries plaintext pass, cpass, and MD5 pass_hash alongside display data |
| INFO-2 | LOW | Information Disclosure | adminUser.jsp 84 | Email addresses exposed to any authenticated role due to absent authorization gate |
| SENS-1 | INFO | Sensitive Data | 79–85 | PII fields (name, email, phone) rendered — expected in admin UI, noted for record |

---

## 4. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 2 |
| MEDIUM | 4 |
| LOW | 2 |
| INFO | 1 |
| **Total** | **9** |
