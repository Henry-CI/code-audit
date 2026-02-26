# A03 — add-alert.jsp
**Path:** src/main/webapp/html-jsp/settings/add-alert.jsp
**Auditor:** A03
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### File path
`src/main/webapp/html-jsp/settings/add-alert.jsp`

### HTML form tags
None. There is no raw `<form>` HTML element.

### Struts form tags

| Tag | Attribute / Property | Line |
|-----|---------------------|------|
| `<html:form>` | method="post", action="adminAlertAdd.do", styleClass="ajax_mode_c" | 3 |
| `<html:select>` | property="alert_id", styleClass="form-control add_alert_selector main_selector edit", style="adminalert.do?action=alerts", value="1" | 10 |
| `<html:options>` | collection="alertList", property="alert_id", labelProperty="alert_name" | 11 |
| `<html:submit>` | property="submit", styleClass="btn btn-blue" | 23 |

No `<html:text>`, `<html:hidden>`, or `<html:password>` tags are present.

### Scriptlet blocks (`<% ... %>`)
None. The file contains no Java scriptlets.

### Expression outputs (`<%= %>`, `${...}`, `<bean:write>`)

| Line | Expression | Notes |
|------|-----------|-------|
| 23 | `<bean:message key="button.submit">` | Reads from MessageResources bundle — not user-controlled; not an XSS sink. |

No raw `<%= %>` expressions, no EL `${...}` expressions, no `<bean:write>` tags are present. The only dynamic content rendered to the page is the alert list options populated server-side from `alertList` (a request attribute set by `AdminAlertAction`) and the localised button label.

### Includes

| Line | Include directive | Included path |
|------|------------------|--------------|
| 1 | `<%@ include file="..."%>` | `../../includes/importLib.jsp` |

`importLib.jsp` only imports tag libraries and a few Java classes. It contains no authentication check and outputs nothing to the response.

The JSP is rendered inside the Tiles `AdminAlertDefinition` layout (tiles-defs.xml line 85-88), which extends `loginDefinition`.

### `request.getParameter()` / `request.getAttribute()` / session access
None in this JSP file itself. The `alertList` collection is a request attribute populated before the JSP renders. No direct parameter access occurs in the view layer.

### URLs constructed or output to the page
- The `<html:select>` tag has a non-standard misuse of the `style` attribute: `style="adminalert.do?action=alerts"`. This is a CSS style attribute — the URL has no functional effect and is not output as a link or redirect. It appears to be a developer annotation or copy-paste error.

### `<html:hidden>` fields
None. There is one raw HTML hidden field:

| Line | Field | Value |
|------|-------|-------|
| 20 | `<input type="hidden" name="src" value="alert">` | Static literal string "alert" |

This field is a static, hardcoded discriminator value. It is not a CSRF token.

---

## Findings

---

### FINDING 1 — HIGH: No CSRF protection on state-changing form submission

**Severity:** HIGH

**Description:**
The form at line 3 posts to `adminAlertAdd.do` (handled by `AdminAddAlertAction`), which writes a new row into the `user_subscription` table
(`insert into user_subscription(user_id, subscription_id) values(?, ?)`).
This is an authenticated state-changing operation. The form contains no CSRF token — no hidden token field, no synchroniser token, and no custom header check is present anywhere in the JSP or in the Struts action.

Struts 1.x provides no built-in CSRF protection. The `PreFlightActionServlet` performs only a session-existence check; it does not validate request origin. An attacker who can get an authenticated admin to visit a crafted page can silently subscribe that admin (or any user whose session the attacker can target) to arbitrary alerts by issuing a cross-origin POST to `adminAlertAdd.do`.

**File + Line:**
- `src/main/webapp/html-jsp/settings/add-alert.jsp`, line 3 (`<html:form>`) and line 20 (`<input type="hidden" name="src" value="alert">`)
- `src/main/java/com/action/AdminAddAlertAction.java`, lines 27-32

**Evidence:**
```jsp
<!-- add-alert.jsp line 3 -->
<html:form method="post" action="adminAlertAdd.do" styleClass="ajax_mode_c">

<!-- add-alert.jsp line 20 — only hidden field; it is not a CSRF token -->
<input type="hidden" name="src" value="alert" />
```
```java
// AdminAddAlertAction.java line 27-28
if (src.equalsIgnoreCase("alert")) {
    CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
```

**Recommendation:**
Implement a synchroniser token pattern. Generate a cryptographically random token per session (e.g., stored as a session attribute), emit it as a hidden field in the form, and verify it in `AdminAddAlertAction` before performing the database write. Alternatively, migrate to a framework with built-in CSRF protection (Spring MVC + Spring Security).

---

### FINDING 2 — HIGH: Broken access control — no role check in action handler; session check is authentication-only, not authorisation

**Severity:** HIGH

**Description:**
`AdminAddAlertAction.execute()` reads `sessCompId` and `sessUserId` from the session and immediately proceeds to call `CompanyDAO.addUserSubscription()`. There is no check that the authenticated user holds an admin or privileged role. Any authenticated user who can reach `adminAlertAdd.do` (i.e., has a non-null `sessCompId`) can subscribe any user ID to any subscription ID.

The `PreFlightActionServlet.excludeFromFilter()` gate checks only that the session is non-null and `sessCompId` is non-empty. It performs no role check. There are no `web.xml` `<security-constraint>` elements at all — `web.xml` contains no `<security-role>`, `<auth-constraint>`, or `<security-constraint>` elements.

The checklist explicitly notes: "forkliftiqadmin is an admin application — verify that admin-only functionality is protected by an admin role check, not just authentication."

**File + Line:**
- `src/main/java/com/action/AdminAddAlertAction.java`, lines 21-28 (no role check between session read and DB write)
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`, lines 56-60 (only checks `sessCompId` non-null)
- `src/main/webapp/WEB-INF/web.xml` — no `<security-constraint>` elements present

**Evidence:**
```java
// AdminAddAlertAction.java — full execute() body; no role check
HttpSession session = request.getSession(false);
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
String src = request.getParameter("src") == null ? "" : request.getParameter("src");
int sessUserId = session.getAttribute("sessUserId") == null ? 0 : (Integer) session.getAttribute("sessUserId");
AdminAlertActionForm alertAction = (AdminAlertActionForm) actionForm;

if (src.equalsIgnoreCase("alert")) {
    CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
```
```java
// PreFlightActionServlet.java — only check performed
else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
```

**Recommendation:**
Add a role attribute to the session at login and check it in every privileged action. For this action: read a `sessRole` or equivalent attribute from the session and return an error/redirect if the user does not hold the required admin role. Enforce this at the framework level (e.g., a Struts `RequestProcessor` subclass or servlet filter) so it cannot be omitted per-action.

---

### FINDING 3 — MEDIUM: Insecure Direct Object Reference (IDOR) — alert_id not validated against company scope

**Severity:** MEDIUM

**Description:**
The `alert_id` submitted in the form is taken directly from the `<html:select>` dropdown, whose options are populated from `CompanyDAO.getAlertList()`. However, `AdminAddAlertAction` passes the submitted `alertAction.getAlert_id()` directly to `CompanyDAO.addUserSubscription()` with no server-side verification that the submitted ID is one of the valid IDs returned in `alertList`. An attacker can manipulate the POST body to supply any arbitrary integer as `alert_id`, causing a subscription to be created for an alert record outside the intended scope.

```java
// CompanyDAO.java line 862-868
public static void addUserSubscription(String userId, String alertId) throws Exception {
    DBUtil.updateObject("insert into user_subscription(user_id, subscription_id) values(?, ?)", stmt -> {
        stmt.setInt(1, Integer.parseInt(userId));
        stmt.setInt(2, Integer.parseInt(alertId));
    });
}
```

The insert uses a parameterised query (no SQL injection), but the value of `alertId` is not checked against the allowable set before insertion.

**File + Line:**
- `src/main/webapp/html-jsp/settings/add-alert.jsp`, line 10-12 (dropdown — client-side only)
- `src/main/java/com/action/AdminAddAlertAction.java`, line 28
- `src/main/java/com/dao/CompanyDAO.java`, lines 862-868

**Evidence:**
```java
// AdminAddAlertAction.java line 28 — no whitelist check before insert
CompanyDAO.addUserSubscription(String.valueOf(sessUserId), alertAction.getAlert_id());
```

**Recommendation:**
After retrieving `alertList` from `CompanyDAO.getAlertList()`, verify that the submitted `alert_id` is present in that list before calling `addUserSubscription()`. Reject the request with an error if the value is not in the allowed set.

---

### FINDING 4 — LOW: No Struts validation rules defined for `adminAlertActionForm`

**Severity:** LOW

**Description:**
The `adminAlertAdd` action mapping in `struts-config.xml` (line 295) declares `validate="true"` and binds to `adminAlertActionForm`, but there are no corresponding validation rules for this form bean in `WEB-INF/validation.xml`. The Struts Validator plug-in is configured and active, but with no rules defined the form's `validate()` method falls back to the `ActionForm` default, which performs no validation. The `alert_id` field submitted by the user is therefore accepted without any type, range, or format check at the framework level.

**File + Line:**
- `src/main/webapp/WEB-INF/struts-config.xml`, lines 294-301 (`validate="true"` but no validation rules)
- `src/main/webapp/WEB-INF/validation.xml` — no entry for `adminAlertActionForm`

**Evidence:**
```xml
<!-- struts-config.xml lines 294-301 -->
<action
    path="/adminAlertAdd"
    name="adminAlertActionForm"
    scope="request"
    type="com.action.AdminAddAlertAction"
    validate="true"
    input="adminDefinition">
    <forward name="adminalerts" path="AdminAlertDefinition"/>
</action>
```
`grep` of `validation.xml` for `adminAlertActionForm` — no matches.

**Recommendation:**
Add a validation rule in `validation.xml` for `adminAlertActionForm` ensuring `alert_id` is required and is a valid integer within an acceptable range, consistent with what the server would accept.

---

### FINDING 5 — LOW: Misuse of `style` attribute to embed a URL (dead code / developer artefact)

**Severity:** LOW (code quality / information exposure)

**Description:**
The `<html:select>` tag at line 10 sets `style="adminalert.do?action=alerts"`. The `style` attribute of an HTML `<select>` element is a CSS style attribute; placing a URL there has no functional effect. This appears to be a developer annotation or a copy-paste error where a `data-url` or similar custom attribute was intended. While it does not create a security vulnerability in isolation, it leaks an internal action path in the rendered HTML source and reflects low code quality that may obscure other unintended behaviours.

**File + Line:**
- `src/main/webapp/html-jsp/settings/add-alert.jsp`, line 10

**Evidence:**
```jsp
<html:select property="alert_id" styleClass="form-control add_alert_selector main_selector edit "
    style="adminalert.do?action=alerts" value="1">
```

**Recommendation:**
Remove or replace this attribute with the appropriate custom data attribute (e.g., `data-url="adminalert.do?action=alerts"`) if it is used by JavaScript to reload the dropdown. Avoid placing internal URLs in CSS style attributes.

---

### FINDING 6 — INFO: Session timeout configured at 30 minutes; no Secure/HttpOnly/SameSite cookie configuration observed

**Severity:** INFO

**Description:**
`web.xml` sets a 30-minute session timeout (line 46-47), which is a reasonable default. However, there is no `<cookie-config>` element in `web.xml` to enforce `HttpOnly` or `Secure` flags on the session cookie, and no `SameSite` attribute is configured. Without `SameSite=Lax` or `SameSite=Strict`, the session cookie is sent on cross-origin navigations, increasing the risk from the CSRF finding (Finding 1). Cookie hardening configuration may exist in server-level Tomcat configuration outside the repository.

**File + Line:**
- `src/main/webapp/WEB-INF/web.xml`, lines 45-47

**Evidence:**
```xml
<session-config>
    <session-timeout>30</session-timeout>
</session-config>
```

**Recommendation:**
Add a `<cookie-config>` block specifying `<http-only>true</http-only>` and `<secure>true</secure>`. Configure `SameSite=Lax` at the Tomcat `context.xml` level (`useHttpOnly="true"`, `sameSiteCookies="lax"`).

---

## Checklist Coverage

### 1. Secrets and Configuration
No hardcoded credentials, API keys, database URLs, or internal configuration values are present in `add-alert.jsp` itself. The misuse of the `style` attribute to embed an internal URL path (`adminalert.do?action=alerts`) is noted under Finding 5 but is not a secret. **No findings in this category for this file.**

### 2. Authentication and Authorization
**Findings raised.** The `adminAlertAdd.do` action is protected only by a session-existence check (no null `sessCompId`). No role check is performed in the action or at the framework level. No `web.xml` security constraints exist. See **Finding 2 (HIGH)**.

### 3. Input Validation and Injection

- **XSS:** No user-controlled data is reflected to the page. The `alertList` collection is fetched from the database by the action and rendered via `<html:options>` (which HTML-encodes output by default in Struts). No `<bean:write filter="false">`, no raw `<%= %>` with request parameters, and no unescaped EL expressions are present. **No XSS findings.**
- **CSRF:** The form performs a state-changing POST with no CSRF token. See **Finding 1 (HIGH)**.
- **SQL Injection:** `CompanyDAO.addUserSubscription()` uses a parameterised query (`?` placeholders via `PreparedStatement`). **No SQL injection finding.**
- **Input validation absent:** No server-side validation rules exist for `adminAlertActionForm`. See **Finding 4 (LOW)**.
- **IDOR:** `alert_id` is not validated server-side against the allowable set. See **Finding 3 (MEDIUM)**.
- **Command injection, SSRF, XXE, path traversal, deserialization:** Not applicable to this JSP or its action handler.

### 4. Session and CSRF
**Finding raised.** CSRF protection is absent. Session cookie hardening is not configured at the `web.xml` level. See **Finding 1 (HIGH)** and **Finding 6 (INFO)**.

### 5. Data Exposure
The page renders the global alert list from `CompanyDAO.getAlertList()`, which appears to be a shared/global list (not per-company scoped). The alert list is selected subscription options — not operator PII or telemetry data. The rendered option labels and IDs are from the `alertList` request attribute, not directly from user input. No stack traces or internal error details are rendered. **No high-severity data exposure finding specific to this file; IDOR risk noted under Finding 3.**

### 6. Dependencies
Not assessed at the individual JSP level. Dependencies (pom.xml, framework versions) are assessed at repository level, not per-file.

### 7. Build and CI
Not assessed at the individual JSP level. Build pipeline assessment is performed at repository level.
