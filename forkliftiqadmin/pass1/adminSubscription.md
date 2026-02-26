# Security Audit Report — adminSubscription.jsp

**Repository:** forkliftiqadmin
**Branch:** master
**Audit run:** audit/2026-02-26-01
**File audited:** `src/main/webapp/html-jsp/adminSubscription.jsp`
**Auditor:** Claude (claude-sonnet-4-6)
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10, JSP, Java

---

## 1. Reading Evidence

### 1.1 Form Action URL

| Line | Method | Action URL |
|------|--------|------------|
| 7    | POST   | `adminsubscription.do` |

**Key finding — orphaned action target:** There is no `<action path="/adminsubscription" ...>` mapping anywhere in `struts-config.xml`. The path `adminsubscription.do` is a **dead-end URL** at the Struts dispatcher level. Submitting the form will cause Struts to throw an `InvalidPathException` or return a 404/error page rather than executing any action class. The form is therefore inert as written, but its presence on a live page still constitutes a structural problem (see findings below).

**Delivery path to this JSP:**
- `tiles-defs.xml` line 54 — `adminSubscriptionDefinition` → renders `adminSubscription.jsp`
- `struts-config.xml` line 229 — forward `adminsubscription` under `/adminmenu` action points to `AccountSubscriptionDefinition` (which resolves to `settings/subscription.jsp`, not this file)
- `AdminMenuAction.java` line 111 — `action=subscription` branch (commented `//Not used`) returns forward `adminsubscription` → this resolves to `AccountSubscriptionDefinition` → `settings/subscription.jsp`
- The tile definition `adminSubscriptionDefinition` (this file's tile) exists but is **not referenced by any active forward** in `struts-config.xml`. This JSP is currently unreachable via any valid navigation flow.

### 1.2 Request Parameters Used in Output or JavaScript

| Parameter / Bean property | Location | Tag / Method |
|---------------------------|----------|--------------|
| `comp_sub_id` (String[])  | Line 20 — `<html:multibox property="comp_sub_id" name="subscriptionRecord">` | `html:multibox` — value used as checkbox value attribute |
| `subscriptionRecord.id`   | Line 21 — `<bean:write property="id" name="subscriptionRecord">` | `bean:write` — rendered into checkbox body |
| `subscriptionRecord.name` | Line 23 — `<bean:write property="name" name="subscriptionRecord">` | `bean:write` — rendered as visible label text inside `<h5>` |
| `arrSubscription`         | Lines 17–18 — `logic:notEmpty` + `logic:iterate` | Iterates `SubscriptionBean` objects from request scope |

### 1.3 Struts Tags That Output Data

| Line | Tag | Bean / Property | Output Context |
|------|-----|-----------------|----------------|
| 10   | `<html:errors>` | Global action errors | HTML |
| 11–15 | `<html:messages id="submsg" message="true">` + `<bean:write name="submsg">` | Action messages (success) | HTML inside `<div class="alert alert-success">` |
| 20   | `<html:multibox property="comp_sub_id" name="subscriptionRecord">` | `SubscriptionBean.id` used as checkbox value | HTML attribute `value=` |
| 21   | `<bean:write property="id" name="subscriptionRecord">` | `SubscriptionBean.id` | HTML text node (checkbox label body) |
| 23   | `<bean:write property="name" name="subscriptionRecord">` | `SubscriptionBean.name` | HTML text node inside `<h5>` |

### 1.4 JavaScript Blocks

None. This file contains no `<script>` blocks and no inline event handlers. No server-side data is injected into JavaScript in this file.

---

## 2. Findings

---

### FINDING 1 — HIGH — CSRF: No Token on State-Changing POST Form

**File:** `src/main/webapp/html-jsp/adminSubscription.jsp` line 7
**Severity:** HIGH

**Description:**
The form submits via POST to `adminsubscription.do` with no CSRF token. As documented in the audit stack notes, CSRF protection is a structural gap across this application. Any authenticated admin user who visits a malicious third-party page while logged in could have their subscription settings silently modified. The form selects checkboxes (`comp_sub_id[]`) that represent the subscriptions assigned to the current company — modifying these is a state-changing operation.

Although the `adminsubscription.do` action mapping is currently absent from `struts-config.xml` (making the form inoperable today), if the mapping is added in future without concurrent addition of CSRF protection, the vulnerability becomes immediately exploitable. The pattern is recorded here because the form structure is wrong regardless of the action's current existence.

**Evidence:**
```jsp
<!-- Line 7 -->
<html:form method="post" action="adminsubscription.do">
```
No `<html:hidden>` CSRF token field present anywhere in the form. No CSRF filter is declared in `web.xml`. `PreFlightActionServlet` checks only `sessCompId != null`; it performs no anti-CSRF validation.

**Recommendation:**
Implement a synchronizer token pattern. Generate a cryptographically random token on form render, store it in the session, and validate it server-side before processing any POST. Struts 1 does not provide a built-in CSRF token mechanism — a servlet filter or a custom `RequestProcessor` must be used. All state-changing forms must include this token.

---

### FINDING 2 — MEDIUM — XSS: `bean:write` Rendering of DB-Sourced `id` and `name` Fields Without Explicit Filter Verification

**File:** `src/main/webapp/html-jsp/adminSubscription.jsp` lines 21 and 23
**Severity:** MEDIUM

**Description:**
`<bean:write>` in Struts 1.3 applies HTML entity encoding by default (`filter="true"` is the default). However, there is no explicit `filter="true"` attribute on either tag, which means the behaviour is implicitly relied upon. This is a defence-in-depth concern: if a developer copies the tag and explicitly sets `filter="false"` elsewhere (a common mistake in this codebase), or if the Struts configuration is altered, unescaped output would immediately produce a stored XSS vector.

More critically, the `id` property (line 21) is also passed directly into the `value=""` attribute of `<html:multibox>` (line 20). The `html:multibox` tag generates an `<input type="checkbox" value="...">`. If `SubscriptionBean.id` ever contains characters like `"`, `>`, or `'`, and if the Struts HTML tag does not escape the value attribute properly, an attribute-injection XSS is possible. In Struts 1.3.10, `html:multibox` does HTML-encode the `value` attribute, but the reliance is entirely implicit.

The `name` property (line 23) is database-sourced (read from the `subscription` table's `name` column). If an administrator can insert subscription records with HTML/script content, the stored content would be rendered inside an `<h5>` element. With only implicit `bean:write` encoding as a defence, any bypass or misconfiguration would result in stored XSS.

**Evidence:**
```jsp
<!-- Lines 20-23 -->
<html:multibox property="comp_sub_id" name="subscriptionRecord">
    <bean:write property="id" name="subscriptionRecord"></bean:write>
</html:multibox>
<bean:write property="name" name="subscriptionRecord"></bean:write>
```

SubscriptionBean source (read from DB):
```java
// SubscriptionBean.java lines 17-18
private String id = "";
private String name = "";
```

No output encoding is applied anywhere between the database read and the JSP render beyond the implicit Struts tag default.

**Recommendation:**
Always specify `filter="true"` explicitly on every `<bean:write>` tag as a defence-in-depth control. Additionally, validate and sanitise `id` and `name` values at the DAO layer — subscription IDs should be numeric/alphanumeric only; subscription names should be restricted to printable non-markup characters. Document the encoding expectation in code comments so future developers do not accidentally disable it.

---

### FINDING 3 — MEDIUM — Authorization: No Role Check Before Rendering Subscription Management UI

**File:** `src/main/webapp/html-jsp/adminSubscription.jsp` (entire file)
**Severity:** MEDIUM

**Description:**
The JSP contains no role or permission check. Any user whose session has a non-null `sessCompId` will pass the `PreFlightActionServlet` gate and, if routed to this page, will be able to view and submit subscription preferences for the company. The `PreFlightActionServlet` verifies only that a session exists with `sessCompId != null` — it does not verify whether the user is a company administrator, a read-only user, or a dealer user.

Subscription management (enabling/disabling report subscriptions) is an administrative operation. There is no evidence in the JSP, in the `AdminMenuAction`, or in the `SubscriptionActionForm` that any further role constraint is applied.

**Evidence:**
```java
// PreFlightActionServlet.java lines 56-60
else if(session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
```
No admin-role assertion anywhere in the subscription rendering flow.

```java
// AdminMenuAction.java lines 108-111
} else if (action.equalsIgnoreCase("subscription")) {  //Not used
    request.setAttribute("alertList", CompanyDAO.getInstance().getUserAlert(String.valueOf(sessUserId)));
    request.setAttribute("reportList", CompanyDAO.getInstance().getUserReport(String.valueOf(sessUserId)));
    return mapping.findForward("adminsubscription");
}
```
No `isAdmin` or privilege check before fetching and forwarding subscription data.

**Recommendation:**
Add an explicit role check in the action handler before returning a forward to this page. Retrieve the user's role from the session (e.g., `sessRole` or equivalent) and deny access with an error forward if the user is not an administrator. The check should be enforced server-side in the Action class, not just in the navigation menu.

---

### FINDING 4 — MEDIUM — Broken / Unmapped Action: `adminsubscription.do` Has No Struts Action Mapping

**File:** `src/main/webapp/html-jsp/adminSubscription.jsp` line 7
**Severity:** MEDIUM

**Description:**
The form targets `adminsubscription.do` (POST), but there is no `<action path="/adminsubscription" ...>` entry in `struts-config.xml`. When submitted, Struts will be unable to dispatch the request and will throw an error (typically `InvalidPathException`, which is caught by the global exception handler and forwarded to the error page). This means:

1. The subscription management feature is completely non-functional — no submission can succeed.
2. Repeated submission attempts produce visible error pages, potentially revealing stack trace or application path information depending on error page configuration.
3. The `SubscriptionActionForm` (`comp_sub_id` field) and the tile definition `adminSubscriptionDefinition` are unreferenced dead artefacts.

The struts-config.xml forward `adminsubscription` under `/adminmenu` correctly points to `AccountSubscriptionDefinition` → `settings/subscription.jsp` (a different file), not this JSP. The tile `adminSubscriptionDefinition` (this file) has no corresponding struts-config forward in any active action.

**Evidence:**
```jsp
<!-- adminSubscription.jsp line 7 -->
<html:form method="post" action="adminsubscription.do">
```
```xml
<!-- struts-config.xml — full scan of action-mappings: no /adminsubscription path found -->
<!-- The only reference to "adminsubscription" in struts-config.xml is a forward name, not a path -->
<forward name="adminsubscription" path="AccountSubscriptionDefinition"/>
```
```xml
<!-- tiles-defs.xml line 54 — tile exists but no struts-config forward points to it -->
<definition name="adminSubscriptionDefinition" extends="adminDefinition">
    <put name="content" value="/html-jsp/adminSubscription.jsp"/>
</definition>
```

**Recommendation:**
Either: (a) Remove this JSP, the `adminSubscriptionDefinition` tile, and the `subscriptionActionForm` form bean if the feature has been superseded by `settings/subscription.jsp`; or (b) Add a proper Struts action mapping for `/adminsubscription` if the feature is intended to be active. Do not leave broken forms in production code — they confuse developers and create ambiguous attack surface.

---

### FINDING 5 — LOW — Information Disclosure: Error and Success Messages Rendered Directly from Server Messages

**File:** `src/main/webapp/html-jsp/adminSubscription.jsp` lines 10–15
**Severity:** LOW

**Description:**
`<html:errors>` renders all global action errors from the `ActionErrors` object, and `<html:messages>` renders success messages. These messages originate from `MessageResources.properties` key lookups performed in the action class. In normal operation this is benign. However, if the `errors.global` key in `MessageResources.properties` interpolates exception text (e.g., SQL error messages) into the rendered output, internal error details such as table names, SQL syntax, or stack trace fragments could be disclosed to authenticated users.

The global exception handler in `struts-config.xml` maps `java.sql.SQLException` to `errors.global`. Depending on how the message resource is defined and whether the exception message is interpolated, this could expose DB internals.

**Evidence:**
```jsp
<!-- Lines 10-15 -->
<html:errors></html:errors>
<html:messages id="submsg" message="true">
    <div class="alert alert-success">
        <bean:write name="submsg" />
    </div>
</html:messages>
```
```xml
<!-- struts-config.xml lines 43-47 -->
<exception
    key="errors.global"
    type="java.sql.SQLException"
    path="errorDefinition"/>
```

**Recommendation:**
Ensure `MessageResources.properties` defines `errors.global` as a generic user-facing message that does not include exception details. Do not pass exception messages through to the UI. Log full exception details server-side only.

---

### FINDING 6 — LOW — Dead Code / Unreachable Page Increases Attack Surface

**File:** `src/main/webapp/html-jsp/adminSubscription.jsp` (entire file)
**Severity:** LOW

**Description:**
This JSP is defined as a Tiles content fragment (`adminSubscriptionDefinition`) but has no active forward in `struts-config.xml` routing to its tile. The `AdminMenuAction` comment `//Not used` on the subscription branch confirms the feature is inactive. Despite being unreachable through the normal navigation flow, the file remains deployed on the server and its tile definition remains in `tiles-defs.xml`. If any future action forward accidentally references `adminSubscriptionDefinition`, this page — with its broken form, implicit-only encoding, and lack of role checks — would become live.

**Evidence:**
```java
// AdminMenuAction.java line 108
} else if (action.equalsIgnoreCase("subscription")) {  //Not used
```
```xml
<!-- tiles-defs.xml line 54 -->
<definition name="adminSubscriptionDefinition" extends="adminDefinition">
    <put name="content" value="/html-jsp/adminSubscription.jsp"/>
</definition>
```

**Recommendation:**
Remove `adminSubscription.jsp`, its tile definition `adminSubscriptionDefinition`, the unused `SubscriptionActionForm` form-bean registration, and the dead `action=subscription` branch in `AdminMenuAction` if this feature has been replaced. Retaining dead UI code creates maintenance burden and ambiguous security posture.

---

## 3. Category Summary

| Category | Finding Count | Highest Severity |
|---|---|---|
| XSS (unescaped output) | 1 | MEDIUM (Finding 2) |
| CSRF | 1 | HIGH (Finding 1) |
| Authentication / Authorization | 1 | MEDIUM (Finding 3) |
| Broken Functionality / Mapping | 1 | MEDIUM (Finding 4) |
| Information Disclosure | 1 | LOW (Finding 5) |
| Dead Code / Attack Surface | 1 | LOW (Finding 6) |
| **Total** | **6** | **HIGH** |

**No issues found in:** JavaScript injection (no JS blocks exist in this file).

---

## 4. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH     | 1 |
| MEDIUM   | 3 |
| LOW      | 2 |
| INFO     | 0 |
| **Total**| **6** |

---

## 5. Notes on Scope and Context

- The `bean:write` default `filter="true"` behaviour in Struts 1.3 provides a baseline HTML-encoding defence for lines 21 and 23. This prevents the XSS from being CRITICAL today, but the implicit reliance and absence of explicit declaration is flagged as a hygiene concern.
- The broken action mapping (Finding 4) means the form is currently inoperable. Findings 1 (CSRF) and 3 (Authorization) are rated on the severity they would represent if the mapping were added — which is the realistic path for this feature to be "re-enabled" by a developer who does not re-audit the security controls.
- The `SubscriptionDAO.checkCompFleetAlert()` method (line 99) contains a string-concatenated SQL query using `comId` without parameterisation — this is a SQL Injection vulnerability in the DAO layer itself, but it is outside the scope of this file's audit (the JSP does not call this method). This is noted for cross-reference with a DAO-level audit pass.
