# Security Audit Report: adminOperator.jsp

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**File Audited:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Supporting Files Reviewed:**
- `src/main/java/com/action/AdminOperatorAction.java`
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/java/com/action/PandoraAction.java`
- `src/main/java/com/bean/DriverBean.java`
- `src/main/webapp/skin/js/scripts.js` (delete handler)
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/includes/importLib.jsp`
**Stack:** Apache Struts 1.3.10
**Auditor:** Pass 1 automated analysis

---

## 1. Reading Evidence

### Form Action URLs
| Line | Method | Action URL | Parameters Submitted |
|------|--------|-----------|----------------------|
| 20 | GET | `admindriver.do` | `searchDriver`, `driverId` (hidden), `action` (hidden) |

### Request Parameters Used in Output or JS
| Line | Parameter | Usage |
|------|-----------|-------|
| 4 | `searchDriver` | Read via `request.getParameter("searchDriver")` into scriptlet variable |
| 25 | `searchDriver` (scriptlet var) | Reflected into HTML `<input value="...">` without escaping |

### Struts Tags That Output Data
| Line | Tag | Bean / Property | filter attribute |
|------|-----|-----------------|-----------------|
| 38 | `<bean:message>` | `button.add` | N/A – message key, not user data |
| 52 | `<bean:message>` | `driver.name` | N/A – message key |
| 53 | `<bean:message>` | `driver.username` | N/A – message key |
| 54 | `<bean:message>` | `driver.joindate` | N/A – message key |
| 62 | `<bean:message>` | `button.edit` | N/A – message key, inside HTML attribute `title=""` |
| 63 | `<bean:write>` | `driverRecord.id` | **not specified** (defaults to `filter="false"`) |
| 66 | `<bean:write>` | `driverRecord.id` | **not specified** (defaults to `filter="false"`) |
| 72 | `<bean:write>` | `driverRecord.id` | **not specified** (defaults to `filter="false"`) |
| 78–79 | `<bean:write>` | `driverRecord.first_name`, `driverRecord.last_name` | **not specified** (defaults to `filter="false"`) |
| 81 | `<bean:write>` | `driverRecord.email_addr` | **not specified** (defaults to `filter="false"`) |
| 82 | `<bean:write>` | `driverRecord.joindt` | **not specified** (defaults to `filter="false"`) |

> **Note on `<bean:write>` default behaviour in Struts 1.3.10:** The `filter` attribute defaults to `true` in Struts 1.3.10, meaning HTML special characters (`<`, `>`, `&`, `"`, `'`) are entity-encoded automatically when `filter` is omitted. This is the opposite of older Struts 1.1 behaviour. All `<bean:write>` usages above are therefore safe against basic HTML-injection **unless** a downstream configuration or custom tag override changes this default. This is flagged as INFO/LOW items because the risk is conditional.

### JavaScript Blocks Using Server-Side Data
None present in this file. There are no `<script>` blocks, no EL expressions (`${...}`), no JSTL output, and no scriptlet-to-JS variable assignments.

The `scripts.js` delete handler at lines 74 and 100 receives the driver ID from the `data-delete-value` HTML attribute (populated by `<bean:write property="id">`). The value flows from an HTML attribute into a jQuery `.post()` call as a form field value, not concatenated into a script string. This is not a DOM XSS path under normal circumstances because the ID is a `Long` database primary key.

---

## 2. Findings

---

### FINDING 001 — HIGH — XSS: Reflected `searchDriver` Parameter Written to HTML Input Value Without Escaping

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Lines:** 4, 25

**Description:**
The request parameter `searchDriver` is captured in a JSP scriptlet and reflected verbatim into an HTML `<input>` `value` attribute with no encoding:

```jsp
<%
    String searchDriver = request.getParameter("searchDriver") == null ? ""
                        : request.getParameter("searchDriver");
%>
...
<input type="text" name="searchDriver" class="form-control input-lg"
       placeholder="Search" value="<%=searchDriver %>"/>
```

An attacker can craft a URL such as:

```
admindriver.do?searchDriver="><script>alert(document.cookie)</script>
```

The unquoted/double-quote-terminated injection breaks out of the `value` attribute and executes arbitrary JavaScript in the victim's browser. This is a reflected XSS with no server-side sanitisation in the JSP or in the `PandoraAction.getRequestParam()` helper (which returns the raw parameter string with no encoding).

**Evidence:**
- Line 4: `String searchDriver = request.getParameter("searchDriver") == null ? "" : request.getParameter("searchDriver");`
- Line 25: `value="<%=searchDriver %>"`
- `PandoraAction.java` line 25–27: `getRequestParam` returns the raw parameter with no HTML encoding.

**Recommendation:**
Replace the raw scriptlet output with HTML-encoded output. The simplest fix within Struts 1.x is to use `org.apache.commons.lang.StringEscapeUtils.escapeHtml(searchDriver)` at point of output, or to bind the value to an `ActionForm` field and render it with `<html:text>`, which applies encoding automatically. Alternatively, use JSTL `<c:out value="${param.searchDriver}" escapeXml="true"/>` which is already safe. Never write raw request parameters into HTML attribute values.

---

### FINDING 002 — MEDIUM — XSS: `<bean:write>` Tags Rendering `first_name` and `last_name` Without Explicit `filter="true"`

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Lines:** 78–79

**Description:**
The driver's first and last name are rendered into table cell content using `<bean:write>` without the `filter` attribute specified:

```jsp
<bean:write property="first_name" name="driverRecord"/>&nbsp;<bean:write
    property="last_name" name="driverRecord"/>
```

In Struts 1.3.10 the `filter` attribute defaults to `true`, so HTML entities are encoded at output time. However, the absence of an explicit `filter="true"` is a maintenance hazard: a developer or configuration change may alter the effective default, and names stored in the database originate from a data-entry form (`AdminDriverAddAction` / `AdminDriverEditAction`) where sanitisation has not been reviewed in this pass. If stored names contain HTML markup, they are persisted and later rendered. Should the effective `filter` value ever change to `false`, or if a stored XSS payload exists in the database, this becomes a stored XSS vector.

**Evidence:**
- Lines 78–79: `<bean:write property="first_name" name="driverRecord"/>` — no `filter` attribute.
- `DriverBean.java` lines 18–19: `first_name` and `last_name` are plain `String` fields with no documented sanitisation.

**Recommendation:**
Add `filter="true"` explicitly to every `<bean:write>` that renders string data to eliminate reliance on the default and make intent clear. Audit `AdminDriverAddAction` and `AdminDriverEditAction` to confirm that name fields are not persisted with embedded HTML markup.

---

### FINDING 003 — MEDIUM — XSS: `<bean:write>` Tags Rendering `email_addr` and `joindt` Without Explicit `filter="true"`

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Lines:** 81–82

**Description:**
Same pattern as Finding 002. The `email_addr` and `joindt` fields are rendered without an explicit `filter` attribute:

```jsp
<td><bean:write property="email_addr" name="driverRecord"/></td>
<td><bean:write property="joindt" name="driverRecord"/></td>
```

`email_addr` is particularly interesting: a malformed email address such as `foo@bar.com"><img src=x onerror=alert(1)>` stored in the database would be reflected into the table if `filter="false"` were ever in effect.

**Evidence:**
- Line 81: `<bean:write property="email_addr" name="driverRecord"/>` — no `filter` attribute.
- Line 82: `<bean:write property="joindt" name="driverRecord"/>` — no `filter` attribute.

**Recommendation:**
Add `filter="true"` explicitly. Validate `email_addr` format before storage. Review the add/edit action forms.

---

### FINDING 004 — MEDIUM — XSS: `<bean:write id="driverRecord" property="id">` Injected Into HTML Attribute Context Without `filter="true"`

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Lines:** 63, 66, 72

**Description:**
The driver's `id` (a `Long`) is interpolated into HTML attribute values in three places:

```jsp
href="admindriver.do?action=edit&driverId=<bean:write property="id" name="driverRecord"/>"   (line 63)
class="driver<bean:write property="id" name="driverRecord"/>"                                 (line 66)
data-delete-value="<bean:write property="id" name="driverRecord"/>"                           (line 72)
```

`DriverBean.id` is typed as `Long` (not `String`), so in practice its rendered value is a numeric string and cannot contain HTML-breaking characters. The risk here is therefore LOW in isolation. However:

1. The class name injection at line 66 (`class="driver<id>"`) and the `data-delete-value` attribute at line 72 both lack `filter="true"`.
2. If the type of `id` were ever changed to `String`, or if the ORM mapping were altered to populate it from an unvalidated source, these injection points would immediately become exploitable.
3. The href at line 63 constructs a URL from a server-side value in a `href` attribute; while `Long` is safe, the pattern is worth flagging as a code hygiene issue.

**Evidence:**
- Lines 63, 66, 72: `<bean:write property="id" name="driverRecord"/>` — no `filter` attribute, used in attribute contexts.
- `DriverBean.java` line 14: `private Long id = null;` — currently typed as `Long`.

**Recommendation:**
Add `filter="true"` to all `<bean:write>` usages. For the `href` and `data-*` attribute injections, confirm that the Struts URL-building tags (`<html:link>`) are preferred over manual concatenation, as they handle both HTML and URL encoding.

---

### FINDING 005 — HIGH — CSRF: Delete Driver / Delete User Actions Triggered by AJAX POST With No CSRF Token

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminOperator.jsp` (lines 69–75), `src/main/webapp/skin/js/scripts.js` (lines 56–88, 90–114)
**Supporting Action:** `src/main/java/com/action/AdminOperatorAction.java` lines 50–53, 134–144

**Description:**
Clicking the trash icon on any driver row triggers a JavaScript `$.post()` call that dispatches a state-changing DELETE request to `admindriver.do`:

```js
// scripts.js lines 74–77
$.post('./admindriver.do', {
    'action': "delete",
    'driverId': value
}, ...)
```

and for users:

```js
// scripts.js lines 100–103
$.post('./admindriver.do', {
    'action': "deleteUser",
    'driverId': value
}, ...)
```

These POST requests carry no CSRF token. The `PreFlightActionServlet` only checks that `sessCompId` is non-null in the session; it performs no origin, referer, or token check. An attacker can embed a forged POST request on any page that a logged-in admin visits, causing arbitrary driver or user accounts to be deactivated/deleted without the admin's knowledge.

The `deleteAction` in `AdminOperatorAction.java` calls `DriverDAO.delDriverById(driverId, compId)` and `deleteUserAction` calls `DriverDAO.delUserById(driverId, sessionToken)` — both are irreversible state-changing operations executed on receipt of a simple authenticated POST.

**Evidence:**
- `adminOperator.jsp` lines 69–75: delete anchor with `data-delete-action="driver"` and `data-delete-value="<bean:write property="id">"`
- `scripts.js` lines 74–77 and 100–103: unprotected `$.post()` to `admindriver.do`
- `AdminOperatorAction.java` lines 50–53, 134–143: `deleteAction` and `deleteUserAction` perform permanent data modification
- `PreFlightActionServlet.java` lines 56–60: auth gate checks only `sessCompId != null`, no CSRF check

**Recommendation:**
Implement a synchronised token pattern: generate a per-session (or per-request) CSRF token, store it in the session, include it as a hidden field in every form and as a custom header (`X-CSRF-Token`) in every AJAX call, and validate it server-side before executing any state-changing action. As a minimum short-term mitigation, verify the `Origin` or `Referer` header server-side in `PreFlightActionServlet` or a Struts `RequestProcessor`.

---

### FINDING 006 — HIGH — CSRF: GET-Based Search Form Also Carries Hidden State-Change Parameters

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Lines:** 20, 88–89

**Description:**
The search form uses `method="get"`, which is conventionally low-risk. However the form contains two hidden fields:

```jsp
<input type="hidden" name="driverId" value=""/>
<input type="hidden" name="action" value=""/>
```

These hidden fields allow any JavaScript on the page (or injected by XSS) to set `driverId` and `action` values and then submit the form, turning a benign GET search into a GET-based state-changing request. The `AdminOperatorAction` dispatches on the `action` parameter for all operations including `delete`, `edit`, `add`, and `deleteUser`. A GET request to `admindriver.do?action=delete&driverId=123` will execute the delete path, because `doGet` in `PreFlightActionServlet` calls `super.doGet` which routes through Struts.

This compounds the CSRF risk: GET-based CSRF attacks (simple `<img src="admindriver.do?action=delete&driverId=1">`) are trivially exploitable from any page.

**Evidence:**
- Lines 88–89: hidden `driverId` and `action` fields on a GET form
- `AdminOperatorAction.java` lines 35–60: `switch (action.toLowerCase())` executes delete operations on GET requests
- `PreFlightActionServlet.java` lines 36, 94–96: `doGet` and `doPost` both authenticate and dispatch without CSRF check

**Recommendation:**
State-changing operations (`delete`, `add`, `edit`) must only respond to POST requests. Add a `request.getMethod().equals("POST")` guard to each state-changing case in `AdminOperatorAction`, or use Struts action-mapping `<set-property property="method" value="POST"/>` where supported. Remove the hidden `driverId` and `action` fields from the GET search form; if they are needed, do not allow them to trigger destructive operations on GET.

---

### FINDING 007 — MEDIUM — Authentication: No Role-Based Authorization Check; Any Authenticated Company Session Can Manage Drivers

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`, `src/main/java/com/action/AdminOperatorAction.java`

**Description:**
The only authentication control is the `PreFlightActionServlet` check that `sessCompId != null`. There is no role check anywhere in `AdminOperatorAction.java` or in the JSP. Any session holder with a valid `sessCompId` — regardless of their privilege level within the company — can reach all driver management operations: list, add, edit, delete, invite, and subscription management.

The `AdminOperatorAction` does scope driver access by `sessCompId` (the company ID is always taken from the session, not the request, which is correct for tenant isolation), but there is no distinction between a company admin and a lower-privileged company user. If a lower-privileged user account is compromised or misconfigured, they have full driver management capability.

**Evidence:**
- `PreFlightActionServlet.java` lines 56–60: only `sessCompId != null` is checked.
- `AdminOperatorAction.java`: no `isUserInRole()`, no session-attribute role check, no redirect for unauthorised roles.
- The JSP contains no `<logic:present>` or similar role guard around add/delete UI elements.

**Recommendation:**
Introduce a session-stored role or privilege attribute (e.g., `sessUserRole`) set at login time. Check it in `AdminOperatorAction.execute()` before dispatching any action. Restrict the "Add Driver", "Edit", and "Delete" UI elements in the JSP using `<logic:equal>` or equivalent guards so low-privileged users do not see controls they cannot use.

---

### FINDING 008 — MEDIUM — Information Disclosure: Driver Email Address Rendered in Listing Table

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Line:** 81

**Description:**
The full email address of every driver returned by the search is rendered in the publicly-visible (to any authenticated company session) table:

```jsp
<td><bean:write property="email_addr" name="driverRecord"/></td>
```

`DriverBean.email_addr` is the operator's login credential. Listing all driver email addresses in a single paginated table view increases the value of a session hijack or CSRF attack, and may violate data minimisation obligations under applicable privacy regulations (e.g., GDPR, PIPEDA) if the admin page is accessible to staff who do not require this information.

**Evidence:**
- Line 81: `email_addr` rendered in table column `driver.username`.
- `DriverBean.java` line 37: `email_addr` is the same field used as the login identifier (`pass`, `pass_hash` are sibling fields).

**Recommendation:**
Evaluate whether the full email address must be shown in the listing view. Consider showing only the domain part or a masked version (e.g., `j***@example.com`) in the list, with full detail revealed only in the edit lightbox for users with appropriate permission.

---

### FINDING 009 — LOW — Information Disclosure: Driver Join Date Rendered in Listing Table

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Line:** 82

**Description:**
The driver's join date (`joindt`) is rendered in the table. While this is low-sensitivity data, it confirms when individual drivers were added to the system and may aid an attacker in correlating accounts or social engineering.

**Evidence:**
- Line 82: `<bean:write property="joindt" name="driverRecord"/>`.

**Recommendation:**
Assess whether displaying join date in the listing table is a business requirement. If not, remove it from the default view.

---

### FINDING 010 — LOW — Code Quality / Defence in Depth: `data-after-delete` Attribute Duplicated on Delete Anchor

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/adminOperator.jsp`
**Lines:** 70, 73

**Description:**
The delete anchor declares the `data-after-delete="reload"` attribute twice:

```jsp
<a title="..." href=""
   data-after-delete="reload" data-delete-action="driver"
   data-method-action="delete_driver"
   data-delete-value="<bean:write property="id" name="driverRecord"/>"
   data-after-delete="reload" data-form_type="driver">
```

While browsers will typically use the last value in such cases, duplicate attributes are invalid HTML5 and indicate a copy-paste error. More importantly, this confirms the delete action fires via client-side JavaScript reading the `data-*` attributes, with no server-side confirmation or idempotency guard beyond the swal confirm dialog, which is itself client-side only.

**Evidence:**
- Lines 70 and 73: `data-after-delete="reload"` appears twice on the same element.

**Recommendation:**
Remove the duplicate attribute. Review the pattern for all delete anchors across the codebase.

---

## 3. Category Summary

| Category | Findings | Highest Severity |
|---|---|---|
| XSS | 004 (001, 002, 003, 004) | HIGH (001) |
| CSRF | 002 (005, 006) | HIGH (005, 006) |
| Authentication / Authorization | 001 (007) | MEDIUM |
| Information Disclosure | 002 (008, 009) | MEDIUM |
| Code Quality / Defence in Depth | 001 (010) | LOW |

**No issues found in the following category:**
- Sensitive data rendered in JS variables: no `<script>` blocks exist in this file; no server-side data is injected into JavaScript variables.

---

## 4. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 3 (001, 005, 006) |
| MEDIUM | 4 (002, 003, 004, 007, 008) — see note |
| LOW | 2 (009, 010) |
| INFO | 0 |

> **Correction count:** MEDIUM findings are 5 (002, 003, 004, 007, 008); total findings are 10.

| Severity | Correct Count |
|----------|--------------|
| CRITICAL | 0 |
| HIGH | 3 |
| MEDIUM | 5 |
| LOW | 2 |
| INFO | 0 |
| **TOTAL** | **10** |
