# Security Audit Report: adminUnit.jsp

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**File Audited:** `src/main/webapp/html-jsp/adminUnit.jsp`
**Supporting Files Reviewed:**
- `src/main/java/com/action/AdminUnitAction.java`
- `src/main/java/com/dao/UnitDAO.java` (delUnitById, getAllUnitSearch)
- `src/main/java/com/bean/UnitBean.java`
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/skin/js/scripts.js` (delete vehicle AJAX handler)
- `src/main/webapp/js/ajaxSwithType.js`
- `src/main/webapp/includes/importLib.jsp`

---

## Section 1: Reading Evidence

### Form Action URLs

| Element | Method | Action URL | Line(s) |
|---------|--------|------------|---------|
| `<form id="adminUnitForm">` | POST | `adminunit.do` | 18 |
| Add Vehicle link | GET (lightbox) | `adminunit.do?action=add` | 31 |
| Edit Vehicle link | GET (lightbox) | `adminunit.do?action=edit&equipId=<bean:write property="id"/>` | 60-61 |
| Delete anchor (AJAX) | POST via `$.post` in scripts.js | `./adminunit.do` with `action=delete&equipId=<value>` | 65-70 (JSP), scripts.js:153 |

### Request Parameters Used in Output or JS

| Parameter | Source | Usage Location | Line |
|-----------|--------|---------------|------|
| `searchUnit` | `request.getParameter("searchUnit")` | Written directly to `value` attribute of `<input>` | JSP:4, JSP:23 |
| `equipId` | `request.getParameter("equipId")` in Action | Passed to `delUnitById(equipId)` — concatenated into SQL | Action:34, DAO:349 |
| `action` | `request.getParameter("action")` in Action | Routing switch in AdminUnitAction | Action:33 |

### Struts Tags That Output Data

| Tag | Bean / Property | Output Location | Line |
|-----|----------------|-----------------|------|
| `<bean:write property="id" name="unitRecord"/>` | `UnitBean.id` | `href` attribute of Edit link, `data-delete-value` attribute | 60, 68 |
| `<bean:write property="name" name="unitRecord"/>` | `UnitBean.name` | Table cell (`<td>`) | 72 |
| `<bean:write property="serial_no" name="unitRecord"/>` | `UnitBean.serial_no` | Table cell (`<td>`) | 73 |
| `<bean:write property="manu_name" name="unitRecord"/>` | `UnitBean.manu_name` | Table cell (`<td>`) | 74 |
| `<bean:write property="type_nm" name="unitRecord"/>` | `UnitBean.type_nm` | Table cell (`<td>`) | 75 |
| `<bean:write property="acchours" name="unitRecord"/>` | `UnitBean.acchours` | Table cell (`<td>`) | 76 |
| `<html:errors/>` | Struts ActionErrors | Error message block | 38 |
| `<bean:message key="..."/>` | i18n resource bundles | Static labels (not data-driven) | 34, 47-52, 59, 62, 65 |

### JavaScript Blocks Using Server-Side Data

No inline `<script>` blocks exist within this JSP file. Server-side data flows into the DOM solely via HTML attributes and table cell content as listed above. The delete operation is wired at the DOM level via the `data-delete-value` attribute (line 68), which is read by `scripts.js` at click time and submitted as a POST body parameter without any token.

---

## Section 2: Audit Findings

---

### CRITICAL: SQL Injection via `equipId` in Delete Action

**Severity:** CRITICAL
**File + Line:**
- `src/main/webapp/html-jsp/adminUnit.jsp` line 65-70 (delete anchor sets `data-delete-value`)
- `src/main/java/com/action/AdminUnitAction.java` line 34, 58
- `src/main/java/com/dao/UnitDAO.java` line 349

**Description:**
The `equipId` request parameter is read from the HTTP request in `AdminUnitAction.java` without sanitization and passed verbatim to `UnitDAO.delUnitById(equipId)`. Inside that method the value is concatenated directly into a SQL statement string:

```java
// AdminUnitAction.java line 34
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
...
// line 58
unitDAO.delUnitById(equipId);
```

```java
// UnitDAO.java line 349
String sql = "update unit set active = false where id=" + id;
stmt.executeUpdate(sql);
```

An authenticated attacker can send a crafted POST to `adminunit.do` with `action=delete&equipId=1 OR 1=1` or a UNION-based payload to affect arbitrary rows or exfiltrate data. Because the underlying statement uses `Statement` (not `PreparedStatement`), the full SQL injection attack surface is open.

**Evidence:**
- `UnitDAO.java:349`: `String sql = "update unit set active = false where id=" + id;`
- `AdminUnitAction.java:34`: unsanitized `equipId` passed to DAO
- The same `equipId` is also passed to `unitDAO.getUnitById(equipId)` (edit action, line 45) — that method should also be reviewed for the same pattern.

**Recommendation:**
Replace the `Statement` with a `PreparedStatement` using a parameterized query:
```java
String sql = "UPDATE unit SET active = false WHERE id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setInt(1, Integer.parseInt(id));
ps.executeUpdate();
```
Validate that `id` is a positive integer before DAO entry using `NumberUtils.isNumber(id)` and `Integer.parseInt`. Apply the same fix to all other DAO methods that accept `equipId` as a raw string.

---

### HIGH: Reflected XSS via Unescaped `searchUnit` Parameter in Input Value Attribute

**Severity:** HIGH
**File + Line:** `src/main/webapp/html-jsp/adminUnit.jsp` lines 3-5, 22-23

**Description:**
The `searchUnit` request parameter is read using a raw scriptlet and written directly into the `value` attribute of an HTML `<input>` element without any HTML encoding:

```jsp
<%
    String searchUnit = request.getParameter("searchUnit") == null ? "" : request.getParameter("searchUnit");
%>
...
<input type="text" name="searchUnit" class="form-control input-lg" placeholder="Search"
       value="<%=searchUnit %>"/>
```

An attacker can craft a URL such as:
```
/adminunit.do?searchUnit="><script>alert(document.cookie)</script>
```
This breaks out of the `value` attribute and injects arbitrary JavaScript into the page. Because this is a GET-accessible search parameter, it is also exploitable as a reflected XSS vector via a crafted link sent to an authenticated admin.

**Evidence:**
- JSP line 4: `request.getParameter("searchUnit")` stored without encoding
- JSP line 23: `value="<%=searchUnit %>"` — raw scriptlet output into HTML attribute

**Recommendation:**
HTML-encode the value before output. Use JSTL `<c:out>` or explicitly call `org.apache.commons.lang.StringEscapeUtils.escapeHtml(searchUnit)`:
```jsp
value="<c:out value="${param.searchUnit}"/>"
```
Or pass the value through the Struts action, store it in an ActionForm field, and render it with `<html:text property="searchUnit"/>` which escapes by default.

---

### HIGH: Reflected XSS via `<bean:write>` Without `filter="true"` — Vehicle Data in HTML Attributes

**Severity:** HIGH
**File + Line:** `src/main/webapp/html-jsp/adminUnit.jsp` lines 60-61, 68

**Description:**
The Struts `<bean:write>` tag defaults to `filter="true"`, which HTML-encodes output. However, two uses of `<bean:write>` embed database-sourced values directly inside HTML tag attributes where the escaping context matters:

1. **Edit link `href` (line 60-61):**
```jsp
href="adminunit.do?action=edit&equipId=<bean:write property="id" name="unitRecord"/>"
```
`UnitBean.id` is a `String`. If `filter="true"` is active (the default), `<` and `>` are encoded but `"` inside an attribute may not be fully safe depending on Struts 1.x version behavior. More critically, if `id` were ever non-numeric (database corruption, injection into the data layer), this URL would allow manipulation.

2. **Delete anchor `data-delete-value` (line 68):**
```jsp
data-delete-value="<bean:write property="id" name="unitRecord"/>"
```
Same concern as above for the `id` field. More importantly, `name`, `serial_no`, `manu_name`, and `type_nm` fields (lines 72-75) are output to `<td>` cells. If any of these fields contain stored HTML/JavaScript (e.g., a vehicle name saved as `<script>alert(1)</script>`), they will be rendered via `<bean:write>` with `filter="true"` and will be encoded — this is a mitigating factor. However, the encoding relies solely on Struts 1.x default behavior, and no explicit `filter="true"` is set, making the intent ambiguous and the protection version-dependent.

**Evidence:**
- JSP lines 72-76: six `<bean:write>` tags with no explicit `filter` attribute
- JSP lines 60, 68: `<bean:write property="id">` embedded in HTML attribute context
- `UnitBean.java`: all fields are `String` type with no validation constraints

**Recommendation:**
Explicitly set `filter="true"` on all `<bean:write>` tags to make the escaping intent unambiguous and version-proof. For data appearing in HTML attributes, additionally validate that numeric ID fields are actually numeric before persisting to the database. Consider adopting JSTL `<c:out>` for all output to enforce a single, well-understood escaping mechanism.

---

### HIGH: CSRF on Vehicle Delete (State-Changing POST Without Token)

**Severity:** HIGH
**File + Line:**
- `src/main/webapp/html-jsp/adminUnit.jsp` lines 65-70 (delete anchor element)
- `src/main/webapp/skin/js/scripts.js` lines 142-165 (vehicle case AJAX handler)
- `src/main/java/com/action/AdminUnitAction.java` lines 57-61

**Description:**
The vehicle delete operation is performed via an AJAX POST request issued by `scripts.js` when the trash icon is clicked:

```javascript
// scripts.js lines 153-156
$.post('./adminunit.do', {
    'action': "delete",
    'equipId': value
}, function (data) { ... })
```

There is no CSRF token included in this POST body, no `X-Requested-With` header check in the server-side action, and no synchronizer token pattern implemented anywhere in the Struts action. The `PreFlightActionServlet` only checks that `sessCompId != null` in the session — it performs no origin or referrer validation.

A malicious page visited by an authenticated admin can trigger this POST silently, causing vehicle records to be soft-deleted without the admin's knowledge. The `equipId` value is rendered in the DOM from the server (line 68), but an attacker who knows or can enumerate valid vehicle IDs can craft the attack independently.

**Evidence:**
- `scripts.js:153`: `$.post('./adminunit.do', {'action': 'delete', 'equipId': value}, ...)`
- No token field in the POST body
- `AdminUnitAction.java:57-61`: delete branch has no token check
- `PreFlightActionServlet.java:56`: only checks `sessCompId != null`

**Recommendation:**
Implement the Struts Synchronizer Token pattern. In the action that renders the list page, call `saveToken(request)`. In `AdminUnitAction.execute()` for the delete branch, call `isTokenValid(request, true)` and reject requests where the token is invalid. For AJAX deletes, embed the token as a hidden form field or a meta tag, and include it in the POST body. Alternatively, adopt a `SameSite=Strict` or `SameSite=Lax` cookie policy at the session level.

---

### HIGH: CSRF on Search POST (Form Without Token)

**Severity:** HIGH
**File + Line:** `src/main/webapp/html-jsp/adminUnit.jsp` lines 18-88

**Description:**
The search form uses `method="post"` and posts to `adminunit.do` without a CSRF synchronizer token:

```jsp
<form method="post" action="adminunit.do" name="adminUnitForm" id="adminUnitForm">
    <input type="text" name="searchUnit" .../>
    ...
    <input type="hidden" name="equipId" value=""/>
    <input type="hidden" name="action" value=""/>
</form>
```

The form also includes hidden `equipId` and `action` fields. While the default (no `action`) path only returns a unit list (read-only), the same form structure — particularly the hidden `action` field — could be abused cross-site to trigger any action branch in `AdminUnitAction` (including `delete`) by pre-filling `action=delete` and `equipId=<target>` from an external page that submits the form via JavaScript.

**Evidence:**
- JSP lines 18, 82-84: POST form with hidden `action` and `equipId` fields and no CSRF token
- `AdminUnitAction.java:33-34`: `action` and `equipId` read directly from request parameters

**Recommendation:**
Add a Struts synchronizer token to the form using `<html:form>` (which automatically manages tokens when configured) or manually embed `<html:hidden property="org.apache.struts.taglib.html.TOKEN"/>`. Validate the token on all POST processing branches in the action. Alternatively, separate read-only (GET) operations from state-changing (POST) operations into distinct action paths.

---

### MEDIUM: No Authorization / Role Check in AdminUnitAction

**Severity:** MEDIUM
**File + Line:** `src/main/java/com/action/AdminUnitAction.java` lines 27-219

**Description:**
`AdminUnitAction.execute()` performs all vehicle management operations (list, add, edit, delete, service, impact, assignment, checklist, job management) without any role or privilege check beyond the presence of a valid `sessCompId` session attribute. The `PreFlightActionServlet` only validates that a session exists and `sessCompId` is non-null — it does not verify that the authenticated user has administrative rights to manage vehicles.

Any authenticated session holder (regardless of their role in the system) who can reach `adminunit.do` can:
- Delete any vehicle belonging to their company
- Trigger service, impact, assignment, and checklist sub-actions on any `equipId`

**Evidence:**
- `AdminUnitAction.java:31`: only `sessCompId` is checked, no role attribute read
- `PreFlightActionServlet.java:56`: `sessCompId != null` is the sole gate
- No `sessRole`, `sessAdmin`, or equivalent attribute checked anywhere in the action

**Recommendation:**
Introduce a role attribute into the session (e.g., `sessRole`) set at login time. At the top of `AdminUnitAction.execute()` (and all admin actions), verify the role before processing any branch:
```java
String sessRole = (String) session.getAttribute("sessRole");
if (!"ADMIN".equals(sessRole)) {
    return mapping.findForward("accessDenied");
}
```
Centralise this check in a base `AdminAction` class or a Servlet Filter so it cannot be inadvertently omitted.

---

### MEDIUM: Insecure Direct Object Reference (IDOR) on `equipId`

**Severity:** MEDIUM
**File + Line:** `src/main/java/com/action/AdminUnitAction.java` lines 44-46, 57-61

**Description:**
The `equipId` parameter is accepted from the request and used to fetch or delete a unit record. The action does verify that the calling session has a `sessCompId`, but it does not confirm that the requested `equipId` belongs to the company associated with `sessCompId`. An authenticated admin from Company A could supply the `equipId` of Company B's vehicle and edit or delete it.

For the delete path:
```java
unitDAO.delUnitById(equipId);   // no company ownership check
```

For the edit/read path:
```java
List<UnitBean> arrUnit = unitDAO.getUnitById(equipId);   // no company ownership check
```

**Evidence:**
- `AdminUnitAction.java:45`: `unitDAO.getUnitById(equipId)` — no `sessCompId` filter
- `AdminUnitAction.java:58`: `unitDAO.delUnitById(equipId)` — no `sessCompId` filter
- `UnitDAO.java:349`: SQL only filters by `id`, not by `comp_id`

**Recommendation:**
Add a company ownership assertion before any single-record operation. Either pass `sessCompId` into the DAO method and add `AND comp_id = ?` to the query, or perform an ownership check after retrieval and return an access-denied forward if the record's `comp_id` does not match the session's `sessCompId`.

---

### MEDIUM: Integer Parsing Without Validation — Potential `NumberFormatException` DoS

**Severity:** MEDIUM
**File + Line:** `src/main/java/com/action/AdminUnitAction.java` lines 40, 70, 86

**Description:**
Three locations parse request parameters directly to `int` without validation:

```java
// line 40 — always executes
int companyId = Integer.parseInt(sessCompId);

// line 70 — add_job branch
int unitId = Integer.parseInt(equipId);

// line 86 — edit_job branch
int jobId = Integer.parseInt(job_id);
```

If `sessCompId` has been corrupted in the session (unlikely but possible through session fixation or other attacks) or if a non-numeric `equipId` or `job_id` is supplied, an unhandled `NumberFormatException` propagates to the container, potentially exposing a stack trace to the client via the global error handler.

**Evidence:**
- `AdminUnitAction.java:40`: `Integer.parseInt(sessCompId)` — no prior numeric check
- `AdminUnitAction.java:70`: `Integer.parseInt(equipId)` — `equipId` comes from user input
- `AdminUnitAction.java:86`: `Integer.parseInt(job_id)` — `job_id` comes from user input

**Recommendation:**
Guard all `Integer.parseInt` calls with `NumberUtils.isNumber()` or a try/catch block, and return an appropriate error forward on invalid input:
```java
if (!NumberUtils.isNumber(equipId)) {
    return mapping.findForward("globalfailure");
}
```

---

### LOW: Sensitive Internal Data Exposed in Table — `acchours` Field

**Severity:** LOW
**File + Line:** `src/main/webapp/html-jsp/adminUnit.jsp` line 76

**Description:**
The vehicle list table renders `acchours` (accumulated/total operational hours) for every vehicle:

```jsp
<td><bean:write property="acchours" name="unitRecord"/></td>
```

While this is an admin-facing page and is expected to display operational data, the combination of vehicle name, serial number, manufacturer, type, and accumulated hours constitutes a detailed operational fingerprint of the company's fleet. If the authentication or authorization controls were bypassed (as noted above), this data would be fully enumerable by an unauthenticated or unauthorized user.

**Evidence:**
- JSP lines 72-76: name, serial_no, manu_name, type_nm, acchours all rendered in one table row
- `UnitBean.java:29`: `acchours` is a `String` field; no masking or truncation applied

**Recommendation:**
No immediate action required assuming authentication and authorization fixes are applied. Consider whether accumulated hours need to be displayed on the list page or whether they should be reserved for the detail/edit view.

---

### LOW: Search Form Uses POST for a Read-Only Operation

**Severity:** LOW
**File + Line:** `src/main/webapp/html-jsp/adminUnit.jsp` line 18

**Description:**
The search form uses `method="post"` even though the search action is a pure read operation (fetches and returns a filtered vehicle list). Using POST for read operations:
- Prevents bookmarking or sharing of search results
- Causes browser "are you sure you want to resubmit?" warnings on page refresh
- Unnecessarily enlarges the CSRF attack surface (POST requests carry the CSRF risk described above; GET requests with no state change do not)

**Evidence:**
- JSP line 18: `<form method="post" action="adminunit.do" name="adminUnitForm" id="adminUnitForm">`
- `AdminUnitAction.java:210-213`: the default (no `action`) branch only reads data

**Recommendation:**
Change the search form to `method="get"`. Ensure that state-changing operations (add, edit, delete) remain exclusively on POST paths. This also removes the search operation from CSRF scope.

---

### INFO: No JavaScript Blocks Using Server-Side Data in adminUnit.jsp

**Category:** Information Disclosure / XSS (JS context)
**Severity:** INFO

There are no inline `<script>` blocks in `adminUnit.jsp` that directly embed server-side data into JavaScript string variables (e.g., `var id = '<%= id %>'`). All server-side data flows into the DOM via HTML attributes and table cells. The JavaScript delete handler in `scripts.js` reads `data-delete-value` from the DOM at click time — it does not receive data via server-side script injection into JS. This is a positive pattern.

---

### INFO: `<html:errors/>` Present — ActionErrors Displayed

**Severity:** INFO
**File + Line:** `src/main/webapp/html-jsp/adminUnit.jsp` line 38

`<html:errors/>` renders Struts ActionErrors. Struts HTML-encodes error messages from the resource bundle by default, so this tag does not introduce XSS. Verify that no user-supplied data is ever interpolated into error message strings in the action layer.

---

## Section 3: Summary Table

| # | Severity | Category | File | Line(s) | Title |
|---|----------|----------|------|---------|-------|
| 1 | CRITICAL | SQL Injection | `UnitDAO.java` | 349 | Unsanitized `equipId` concatenated into SQL DELETE |
| 2 | HIGH | XSS (Reflected) | `adminUnit.jsp` | 4, 23 | `searchUnit` parameter written to HTML attribute unencoded |
| 3 | HIGH | XSS (Stored, potential) | `adminUnit.jsp` | 60, 68, 72-76 | `<bean:write>` tags lack explicit `filter="true"` |
| 4 | HIGH | CSRF | `adminUnit.jsp` / `scripts.js` | 65-70 / 153 | Vehicle delete AJAX POST has no CSRF token |
| 5 | HIGH | CSRF | `adminUnit.jsp` | 18, 82-84 | Search/action POST form has no CSRF token |
| 6 | MEDIUM | Authorization | `AdminUnitAction.java` | 27-219 | No role check; any authenticated session can manage vehicles |
| 7 | MEDIUM | IDOR | `AdminUnitAction.java` | 45, 58 | `equipId` not validated against session `sessCompId` |
| 8 | MEDIUM | Input Validation | `AdminUnitAction.java` | 40, 70, 86 | Unguarded `Integer.parseInt` on user-supplied parameters |
| 9 | LOW | Info Disclosure | `adminUnit.jsp` | 72-76 | Fleet operational data exposed in list view |
| 10 | LOW | Design | `adminUnit.jsp` | 18 | Read-only search uses POST method |
| 11 | INFO | XSS (JS) | `adminUnit.jsp` | (all) | No inline JS blocks embedding server-side data |
| 12 | INFO | XSS | `adminUnit.jsp` | 38 | `<html:errors/>` uses encoded output |

---

## Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH | 4 |
| MEDIUM | 3 |
| LOW | 2 |
| INFO | 2 |
| **Total** | **12** |
