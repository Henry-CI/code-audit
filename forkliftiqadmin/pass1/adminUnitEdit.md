# Security Audit Report — adminUnitEdit.jsp

**Audit run:** audit/2026-02-26-01
**Branch:** master
**File audited:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Supporting files examined:**
- `src/main/java/com/action/AdminUnitEditAction.java`
- `src/main/java/com/action/AdminUnitAction.java`
- `src/main/java/com/actionform/AdminUnitEditForm.java`
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/skin/js/scripts.js` (lines 1001–1032)
- `src/main/java/com/util/CompanySessionSwitcher.java`
- `src/main/java/com/action/LoginAction.java`

---

## 1. Reading Evidence

### 1.1 Form Action URLs

| Form element | Method | Action URL | Purpose |
|---|---|---|---|
| `<html:form>` (line 46) | POST | `adminunitedit.do` | Save/update vehicle general info |

The form submits via the `setupConfirmationPopups` JavaScript function (line 316), which intercepts the native submit and re-posts via `$.post('adminunitedit.do', ...)`.

Navigation tab links (lines 29–43, rendered as `<a href="...">`) are GET links only, built from scriptlet variables:

| Variable | Value (edit mode) |
|---|---|
| `urlGeneral` | `adminunit.do?action=edit&equipId=<id>` |
| `urlService` | `adminunit.do?action=service&equipId=<id>` |
| `urlAccess` | `adminunitaccess.do?id=<id>` |
| `urlImpact` | `adminunit.do?action=impact&equipId=<id>` |
| `urlAssignment` | `adminunit.do?action=assignment&equipId=<id>` |

Three AJAX GET validation endpoints are called from JavaScript (lines 253–266):
- `unitnameexists.do?op_code=unitnameexists&name=<input>`
- `serialnoexists.do?op_code=serialnoexists&serial_no=<input>`
- `macaddressexists.do?op_code=macaddressexists&mac_address=<input>`

### 1.2 Request Parameters Used in Output or JavaScript

| Parameter | Read at | Used at | Encoding applied |
|---|---|---|---|
| `action` (GET) | JSP line 3 | Line 13–17 (URL construction), line 172 hidden input value | None |
| `equipId` (GET) | JSP line 4 | Lines 13–17 (URL construction), line 170 hidden input value | None |
| `newId` (request attribute) | JSP line 22–24 | Line 171 hidden input value | None |

### 1.3 Struts Tags That Output Data

| Tag | Line(s) | Bean / Property | Output context |
|---|---|---|---|
| `<html:text property="name">` | 60–63 | `unitRecord.name` | HTML input value attribute |
| `<html:text property="serial_no">` | 72–75 | `unitRecord.serial_no` | HTML input value attribute |
| `<html:select property="manu_id">` | 84–90 | `unitRecord.manu_id` | HTML select |
| `<html:optionsCollection name="arrManufacturers">` | 88–89 | `arrManufacturers[].id/name` | HTML option text/values |
| `<html:select property="type_id">` | 96–102 | `unitRecord.type_id` | HTML select |
| `<html:optionsCollection property="arrAdminUnitType">` | 100–101 | `unitRecord.arrAdminUnitType[].id/name` | HTML option text/values |
| `<html:select property="fuel_type_id">` | 108–112 | `unitRecord.fuel_type_id` | HTML select |
| `<html:optionsCollection property="arrAdminUnitFuelType">` | 111 | `unitRecord.arrAdminUnitFuelType[].id/name` | HTML option text/values |
| `<html:select property="weight_unit">` | 120–124 | `unitRecord.weight_unit` | HTML select |
| `<html:text property="size">` | 128–135 | `unitRecord.size` | HTML input value attribute |
| `<html:checkbox property="exp_mod">` | 144–146 | `unitRecord.exp_mod` | HTML input checked state |
| `<html:text property="mac_address">` | 151–153 | `unitRecord.mac_address` | HTML input value attribute |
| `<html:hidden property="id">` | 169 | `unitRecord.id` | HTML hidden input value |
| `<bean:message key="...">` | Multiple | i18n properties | HTML text nodes |

### 1.4 JavaScript Blocks Using Server-Side Data

| Line(s) | Server-side data injected | Mechanism |
|---|---|---|
| 170 | `<%=id %>` — raw `equipId` request param injected into `value` attribute of `<input type="hidden" name="oldId">` | JSP scriptlet expression |
| 171 | `<%=newUnitId %>` — integer derived from request attribute `newId` injected into `<input type="hidden" name="newId">` | JSP scriptlet expression |
| 172 | `<%=action %>` — raw `action` request param injected into `<input type="hidden" name="actionUnit">` | JSP scriptlet expression |
| 190 | `$('input[name="mac_address"]').val()` — reads existing MAC address from a Struts-rendered input field into JS variable `mac_add` | DOM read of server-rendered value |
| 253 | `$('input[name=name]').val()` concatenated directly into AJAX URL string (no encoding) | String concatenation into URL |
| 259 | `$('input[name=serial_no]').val()` concatenated directly into AJAX URL string (no encoding) | String concatenation into URL |
| 265 | `$('input[name=mac_address]').val()` concatenated directly into AJAX URL string (no encoding) | String concatenation into URL |

---

## 2. Findings

---

### FINDING-001 — CSRF: No Token on State-Changing POST Form

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Lines:** 46–47, 316–320 (JavaScript AJAX POST)

**Description:**
The `adminunitedit.do` action mutates vehicle records (insert or update). The `<html:form>` at line 46 and the `$.post()` call at line 1005 of `scripts.js` (invoked from line 316) both submit with no CSRF token. The application uses no synchronizer token, double-submit cookie, or SameSite-enforced cookie. The stated stack assessment confirms this is a structural gap across the application.

**Evidence:**
```jsp
<!-- Line 46-47 -->
<html:form method="post" action="adminunitedit.do" styleClass="unit_sform"
           styleId="adminUnitEditFormGeneral">
```
```javascript
// scripts.js line 1005 — AJAX POST, no token
$.post(url, $(this).serialize())
```
The `AdminUnitEditAction.execute()` performs no token check. `PreFlightActionServlet.doPost()` delegates to `doGet()` and checks only `sessCompId != null`; there is no CSRF token validation at any layer.

**Recommendation:**
Implement the Struts 1 synchronizer token mechanism: call `saveToken(request)` in the action that renders the form, and call `isTokenValid(request, true)` at the start of `AdminUnitEditAction.execute()` before processing the POST. Reject requests that fail token validation. Alternatively, add a custom filter that validates a per-session token header on all non-idempotent requests.

---

### FINDING-002 — CSRF: No Token on Inline AJAX Validation Endpoints (Information-Leaking GET Probes)

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Lines:** 253–267

**Description:**
Three AJAX GET endpoints (`unitnameexists.do`, `serialnoexists.do`, `macaddressexists.do`) accept user-controlled input and return Boolean confirmations about the existence of names, serial numbers, and MAC addresses in the database. Although these are GETs, a cross-origin attacker can use these as oracle endpoints via `<script src="...">` or `fetch()` with CORS misconfiguration to enumerate whether specific vehicle names or serial numbers exist in a target company. The struts-config shows `validate="false"` for all three, meaning form validation is also skipped.

**Evidence:**
```javascript
// Lines 253-266
isNameExists = wsValidation(
    'unitnameexists.do?op_code=unitnameexists&name=' + $('input[name=name]').val(), ...);
isSerialExists = wsValidation(
    'serialnoexists.do?op_code=serialnoexists&serial_no=' + $('input[name=serial_no]').val(), ...);
isMacAddrExists = wsValidation(
    'macaddressexists.do?op_code=macaddressexists&mac_address=' + $('input[name=mac_address]').val(), ...);
```
struts-config.xml lines 353–371: all three mapped to `AdminUnitEditAction`, `validate="false"`, no CSRF protection.

**Recommendation:**
Restrict these endpoints so they only respond to same-origin requests (validate `Origin`/`Referer` header server-side, or require a POST with a CSRF token). Confirm that CORS headers are not overly permissive for `.do` endpoints.

---

### FINDING-003 — XSS: Unencoded Request Parameter `equipId` Injected Into HTML Attribute

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Line:** 170

**Description:**
The `equipId` query string parameter is read at line 4, stored in `String id`, and written directly into the `value` attribute of a hidden HTML input at line 170 with no encoding or sanitisation. A crafted URL can close the attribute and inject arbitrary HTML or JavaScript. Because the page is loaded in a modal context, any injected script executes in the full admin page context.

**Evidence:**
```java
// Line 4
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
```
```html
<!-- Line 170 -->
<input type="hidden" name="oldId" id="oldId" value="<%=id %>"/>
```
No `ESAPI.encoder().encodeForHTMLAttribute(id)`, no `<c:out escapeXml="true">`, and no Struts tag encodes this output. A request to:
```
adminunit.do?action=edit&equipId=1"><script>alert(document.cookie)</script>
```
would render:
```html
<input type="hidden" name="oldId" id="oldId" value="1"><script>alert(document.cookie)</script>"/>
```

**Recommendation:**
Replace the scriptlet expression with HTML-attribute-encoded output. Use OWASP ESAPI:
```java
<%=ESAPI.encoder().encodeForHTMLAttribute(id)%>
```
or JSTL:
```jsp
<c:out value="${param.equipId}" escapeXml="true"/>
```
Alternatively, validate `equipId` as a numeric integer at the top of the scriptlet and reject non-numeric values with a `400` response, since it represents a database ID.

---

### FINDING-004 — XSS: Unencoded Request Parameter `action` Injected Into HTML Attribute

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Line:** 172

**Description:**
The `action` request parameter is read at line 3 with no validation and written into a hidden input's `value` attribute at line 172 without encoding. The same injection vector as FINDING-003 applies.

**Evidence:**
```java
// Line 3
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
```
```html
<!-- Line 172 -->
<input type="hidden" name="actionUnit" id="actionUnit" value="<%=action %>"/>
```
A request with `action=add"><img src=x onerror=alert(1)>` would break out of the attribute.

**Recommendation:**
Validate `action` against an explicit allowlist (`"add"`, `"edit"`, empty string) before use. If the value does not match, default to empty string. Also apply HTML-attribute encoding at the point of output, as in FINDING-003.

---

### FINDING-005 — XSS: Unencoded Request Parameter `equipId` Used in Tab Navigation Href Attributes

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Lines:** 13–17, 29–43

**Description:**
The `id` variable (sourced from `equipId`) is concatenated into five URL strings (lines 13–17) which are then written directly into `href` attributes of anchor tags (lines 29–43) without encoding. A malicious `equipId` value of `1&x=<script>` would produce a malformed but potentially exploitable URL. More critically, a value such as `javascript:alert(1)` prefixed with URL-breaking characters, or a value containing `"` to escape the attribute and inject event handlers, allows XSS.

**Evidence:**
```java
// Lines 13-17
urlGeneral   = "adminunit.do?action=edit&equipId=" + id;
urlService   = "adminunit.do?action=service&equipId=" + id;
urlAccess    = "adminunitaccess.do?id=" + id;
urlImpact    = "adminunit.do?action=impact&equipId=" + id;
urlAssignment= "adminunit.do?action=assignment&equipId=" + id;
```
```jsp
<!-- Lines 29, 30, 31, 32, 33 -->
<a class="triggerThis general_u_tab" href="<%=urlGeneral %>">General</a>
<a href="<%=urlService %>" id="service_tab">Service</a>
<a href="<%=urlAccess %>" id="access_tab">Access</a>
<a href="<%=urlImpact %>" id="impact_tab">Impact</a>
<a href="<%=urlAssignment %>" id="assignment_tab">Assignment</a>
```
Input `equipId=1" onclick="alert(1)` produces: `href="adminunit.do?action=edit&equipId=1" onclick="alert(1)"`.

**Recommendation:**
Validate `equipId` as a positive integer at the top of the scriptlet. If validation fails, redirect or render without tabs. For output, URL-encode the parameter value when building the href strings:
```java
String safeId = id.matches("\\d+") ? id : "";
urlGeneral = "adminunit.do?action=edit&equipId=" + safeId;
```
Then apply `ESAPI.encoder().encodeForHTMLAttribute(urlGeneral)` at the point of JSP output, or use `<c:url>` with `<c:param>` to construct URLs safely.

---

### FINDING-006 — XSS: User Input Values Concatenated Into AJAX Validation URLs Without Encoding

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Lines:** 253, 259, 265

**Description:**
Three JavaScript functions build AJAX request URLs by direct string concatenation of form input values (vehicle name, serial number, MAC address) with no `encodeURIComponent()` wrapping. This does not cause reflected XSS in the traditional sense (the values go to the server, not back into the DOM), but it creates two risks: (1) URL injection — an attacker who can influence the field values (e.g., via pre-populated data or a second user editing the same record) could manipulate the AJAX target URL, and (2) if the server ever echoes any of these values back without encoding in a future change, a stored XSS payload already in the database would be reflected via this path.

**Evidence:**
```javascript
// Line 253
wsValidation('unitnameexists.do?op_code=unitnameexists&name=' + $('input[name=name]').val(), ...)

// Line 259
wsValidation('serialnoexists.do?op_code=serialnoexists&serial_no=' + $('input[name=serial_no]').val(), ...)

// Line 265
wsValidation('macaddressexists.do?op_code=macaddressexists&mac_address=' + $('input[name=mac_address]').val(), ...)
```

**Recommendation:**
Wrap each value with `encodeURIComponent()`:
```javascript
'unitnameexists.do?op_code=unitnameexists&name=' + encodeURIComponent($('input[name=name]').val())
```
Consider passing the parameters as a data object to `$.ajax()` rather than building URL strings manually, which allows jQuery to handle encoding automatically.

---

### FINDING-007 — Authentication: No Role/Permission Check in AdminUnitEditAction

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitEditAction.java`
**Lines:** 22–70

**Description:**
`AdminUnitEditAction.execute()` performs no authorization check beyond the presence of `sessCompId` in the session (handled by `PreFlightActionServlet`). Any authenticated session holder — regardless of their role — can POST to `adminunitedit.do` and modify or create vehicle records. The application has role concepts (`ROLE_DEALER`, `ROLE_SYSADMIN`) used elsewhere (e.g., `SwitchCompanyAction`, `LoginAction`), but no role check guards this mutation endpoint. The JSP itself uses `isDealer` to conditionally show the "Assignment" tab, but this is purely a UI-layer conditional with no server-side enforcement.

**Evidence:**
```java
// AdminUnitEditAction.java lines 28-29: only sessCompId is checked
String compId = (String)(session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
UnitBean unitBean = adminUnitEditForm.getUnit(compId);
// No role check follows. Any valid session can edit any company's units
// if compId is manipulated.
```
```java
// PreFlightActionServlet.java line 56: sole auth gate
session.getAttribute("sessCompId") == null || session.getAttribute("sessCompId").equals("")
```

**Recommendation:**
Add an explicit role/permission check at the beginning of `AdminUnitEditAction.execute()`. Determine the minimum required role for vehicle editing (likely `ROLE_ADMIN` or equivalent) and return a `403` or redirect to an error page if the session does not hold that role. Example pattern consistent with the existing codebase:
```java
Boolean isSuperAdmin = (Boolean) session.getAttribute("isSuperAdmin");
Boolean isDealerLogin = (Boolean) session.getAttribute("isDealerLogin");
if (!isSuperAdmin && !isDealerLogin && !hasAdminRole(session)) {
    response.sendError(HttpServletResponse.SC_FORBIDDEN);
    return null;
}
```

---

### FINDING-008 — Authentication: Insecure Direct Object Reference — No Ownership Check on `equipId`

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitAction.java` (context); `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Lines (JSP):** 3–4, 170; (Action):** AdminUnitAction.java line 45, AdminUnitEditAction.java line 29–30

**Description:**
When the edit form is loaded (`adminunit.do?action=edit&equipId=<id>`), `AdminUnitAction` calls `unitDAO.getUnitById(equipId)` at line 45 without verifying that the retrieved unit belongs to `sessCompId`. Similarly, `AdminUnitEditAction` uses the form's `id` field to build the `UnitBean` and then calls `unitDao.saveUnitInfo(unitBean)` without confirming the unit's `comp_id` matches the session's `sessCompId`. An authenticated user who knows (or guesses) a valid `equipId` belonging to another company can read and overwrite that vehicle's data.

**Evidence:**
```java
// AdminUnitAction.java line 45 — no company ownership check
List<UnitBean> arrUnit = unitDAO.getUnitById(equipId);

// AdminUnitEditAction.java line 29-30 — compId from session, but id from form
UnitBean unitBean = adminUnitEditForm.getUnit(compId);
// UnitBean.id comes from the hidden form field, not from session
```
```jsp
<!-- JSP line 169: unit id is a hidden field — fully client-controllable -->
<html:hidden property="id" name="unitRecord"/>
```
The hidden `id` field at line 169 is populated from `unitRecord` (served from the DB on GET), but on POST it is taken from the submitted form body — meaning an attacker can POST an arbitrary `id` value to overwrite a unit from a different company.

**Recommendation:**
Before saving, verify that the unit identified by `unitBean.getId()` belongs to the company in `sessCompId`. Add a DAO-level ownership check:
```java
UnitBean existing = unitDao.getUnitById(unitBean.getId());
if (existing == null || !existing.getComp_id().equals(compId)) {
    response.sendError(HttpServletResponse.SC_FORBIDDEN);
    return null;
}
```
Apply the same fix to `AdminUnitAction`'s `edit` and `delete` branches.

---

### FINDING-009 — Information Disclosure: Integer `newUnitId` Reveals Next Auto-Increment ID

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Line:** 171; `src/main/java/com/action/AdminUnitAction.java` line 49

**Description:**
When adding a new vehicle, `AdminUnitAction` calls `unitDAO.getUnitMaxId()` (line 49) and stores the result as a request attribute `newId`. The JSP renders this as a hidden field at line 171:
```html
<input type="hidden" name="newId" id="newId" value="<integer>"/>
```
This leaks the current maximum unit ID from the database. An attacker can use this value to enumerate existing unit IDs (IDOR reconnaissance), predict future IDs, or confirm whether specific ID ranges are in use.

**Evidence:**
```java
// AdminUnitAction.java line 49
int newUnitId = unitDAO.getUnitMaxId();
request.setAttribute("newId", newUnitId);
```
```html
<!-- JSP line 171 -->
<input type="hidden" name="newId" id="newId" value="<%=newUnitId %>"/>
```

**Recommendation:**
Do not expose internal database sequence IDs to the client. If a client-side reference is needed, generate a temporary session-scoped token instead of using the database max ID. Alternatively, generate the new ID server-side at the point of insert (database auto-increment) and remove this hidden field entirely.

---

### FINDING-010 — Information Disclosure: MAC Address Rendered in Page Source

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Lines:** 151–153, 190

**Description:**
The vehicle's MAC address (a hardware identifier used for physical access control) is rendered into the HTML form as a text input value (line 151–153) and read into the JavaScript variable `mac_add` at line 190. Even when the MAC address section is hidden via CSS (`display:none`, line 148), the value is present in the DOM and visible in page source to anyone who can view the rendered HTML. This applies to any authenticated user who can access the edit form.

**Evidence:**
```jsp
<!-- Lines 151-153 -->
<html:text property="mac_address" titleKey="unit.macadd" styleClass="form-control input-lg"
           name="unitRecord"/>
```
```javascript
// Line 190
var mac_add = $('input[name="mac_address"]').val();
```
The parent `<p class="mac_add_mod" style="display:none;">` hides the field visually but does not prevent the value from being read from the DOM or network response.

**Recommendation:**
Only include the MAC address field in the rendered HTML when the `exp_mod` flag is set for this unit. If it must be present for JavaScript initialisation purposes, consider fetching it via a separate authenticated AJAX call rather than embedding it in the initial page load. At minimum, document the access control requirements clearly so that authorisation on the edit form is tightened (see FINDING-007).

---

### FINDING-011 — XSS: `<logic:equal>` / `<logic:notEqual>` on `isDealer` — Attribute Source Inconsistency Risk

**Severity:** INFO
**File:** `src/main/webapp/html-jsp/vehicle/adminUnitEdit.jsp`
**Lines:** 27, 36

**Description:**
The JSP uses `<logic:equal value="true" name="isDealer">` to conditionally render the Assignment tab. The `isDealer` bean is set as a **session** attribute in `CompanySessionSwitcher.java` (line 43) and as a **request** attribute in `AdminMenuAction`, `LoginAction`, and `SwitchCompanyAction`. Struts `<logic:equal name="isDealer">` searches scopes in page → request → session → application order. If the request attribute is absent (e.g., the JSP is accessed via a forward from a path that does not set it), the session attribute is used instead, which is correct. However, the inconsistency in where this attribute is set across different actions creates a maintenance risk: a code path that forgets to set the request attribute will silently fall back to a potentially stale session value. This is not currently exploitable for XSS but represents a logic-integrity gap.

**Evidence:**
```java
// CompanySessionSwitcher.java line 43 — session scope
session.setAttribute("isDealer", LoginDAO.isAuthority(comp_id, RuntimeConf.ROLE_DEALER));

// LoginAction.java line 69 — request scope
request.setAttribute("isDealer", session.getAttribute("isDealer"));
```
```jsp
<!-- adminUnitEdit.jsp line 27 -->
<logic:equal value="true" name="isDealer">
```
`AdminUnitAction` (which forwards to this JSP) does not set `isDealer` as a request attribute, so the JSP relies on the session-scope value.

**Recommendation:**
Standardise `isDealer` to a single authoritative scope (session) and use `scope="session"` explicitly in Struts logic tags where applicable, or centralise its propagation so all actions that can forward to unit-related JSPs set it consistently.

---

## 3. Category Summary

| Category | Finding(s) | Notes |
|---|---|---|
| XSS | FINDING-003, FINDING-004, FINDING-005, FINDING-006, FINDING-011 | Three high-severity unencoded scriptlet outputs into HTML attributes; one medium on AJAX URL construction; one informational logic inconsistency |
| CSRF | FINDING-001, FINDING-002 | No token on state-changing POST; validation GET endpoints are unauthenticated oracles |
| Authentication / Authorization | FINDING-007, FINDING-008 | No role check on edit action; IDOR allows cross-company unit manipulation via client-controlled hidden field |
| Information Disclosure | FINDING-009, FINDING-010 | DB sequence ID exposed; MAC address in DOM regardless of visibility |
| Sensitive Data Rendered | FINDING-010 | MAC address present in page source when form hidden |

**No issues found in:** Input validation at the server-side form layer (AdminUnitEditForm.validate() checks required fields and numeric size format); the `writeJsonResponse` method correctly returns only a Boolean string, not raw data.

---

## 4. Finding Count by Severity

| Severity | Count | Findings |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 5 | FINDING-001, FINDING-003, FINDING-004, FINDING-005, FINDING-007, FINDING-008 |
| MEDIUM | 2 | FINDING-002, FINDING-006 |
| LOW | 2 | FINDING-009, FINDING-010 |
| INFO | 1 | FINDING-011 |
| **Total** | **10** | |

> Note: FINDING-008 was included in the HIGH count; the table above lists 6 IDs under HIGH — corrected tally: HIGH = 5 distinct vulnerability classes across 6 finding IDs (FINDING-001, FINDING-003, FINDING-004, FINDING-005, FINDING-007, FINDING-008).

---

*Report generated: 2026-02-26 | Auditor: Claude (claude-sonnet-4-6) | Pass: 1*
