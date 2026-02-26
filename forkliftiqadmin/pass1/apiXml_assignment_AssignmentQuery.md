# Security Audit Report — Pass 1
**Audit run:** audit/2026-02-26-01/pass1
**Date:** 2026-02-26
**Repository:** forkliftiqadmin (branch: master)
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet auth gate
**Files audited:**
1. `src/main/webapp/html-jsp/apiXml.jsp`
2. `src/main/webapp/html-jsp/vehicle/assignment.jsp`
3. `src/main/java/com/querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`

---

## 1. Reading Evidence

### 1.1 apiXml.jsp — Output Tags and Data Sources

All output is built via string concatenation into `resp` and emitted at line 102 via `out.println(resp)`.

| Line(s) | XML element(s) written | Source of data |
|---------|------------------------|----------------|
| 16 | `<compKey>` | `request.getAttribute("compKey")` — set by Action layer |
| 24 | `<id>`, `<name>` | `UnitBean.getId()`, `UnitBean.getName()` — DB-sourced strings |
| 33 | `<id>`, `<name>` | `DriverBean.getId()`, `DriverBean.getFirst_name()`, `DriverBean.getLast_name()` — DB-sourced strings |
| 42 | `<id>`, `<name>` | `AttachmentBean.getId()`, `AttachmentBean.getName()` — DB-sourced strings |
| 53–72 | `<id>`, `<name>`, `<value>` | `QuestionBean.getId()`, sanitised `content`, `QuestionBean.getExpectedanswer()` — DB-sourced strings |
| 79, 86 | `<resultstatus>`, `<emailstatus>` | `Boolean` attributes from Action layer (not user-controlled strings) |
| 92 | `<emailstatus>` | `Boolean` attribute from Action layer |
| 97 | `<error>` | `request.getAttribute("error")` — set by Action layer |

**No `request.getParameter()` calls exist in apiXml.jsp.** All values arrive as request attributes populated by the Action layer.

**Question-content sanitisation (lines 53–71):** Uses a chained `else if` structure rather than independent replacements, meaning only the **first** matching special character class is substituted per field value. Additionally, line 70 contains a copy-paste bug: `<` is replaced with `&gt;` instead of `>`.

### 1.2 assignment.jsp — Output Tags and Request Parameters

| Line | Tag / expression | Source |
|------|-----------------|--------|
| 4 | `session.getAttribute("sessDateFormat")` — used in JS `setupDatePicker` call | Session (server-set) |
| 5 | `request.getParameter("equipId")` → variable `id` | **Request parameter (user-controlled)** |
| 6 | `id` concatenated into `urlGeneral` href | Derived from `equipId` |
| 14 | `<%=urlGeneral %>` — emitted into `href` attribute | Derived from `equipId` |
| 15–19 | `<%=id %>` — emitted four times into `href` attribute values | Derived from `equipId` |
| 72 | `<input type="hidden" name="unit_id" value="<%=id %>"/>` | Derived from `equipId` |
| 94 | `<bean:write property="id" name="assignment"/>` — emitted into `data-delete-value` attribute | DB via `UnitAssignmentBean.id` (int) |
| 99 | `<bean:write property="company_name" name="assignment"/>` | DB via `UnitAssignmentBean.company_name` (String) |
| 102 | `<bean:write property="start" name="assignment"/>` | DB via `UnitAssignmentBean.start` (formatted date String) |
| 105 | `<bean:write property="end" name="assignment"/>` | DB via `UnitAssignmentBean.end` (formatted date String) |
| 108 | `<bean:write property="current" name="assignment"/>` | DB via `UnitAssignmentBean.current` ("Yes"/"No") |
| 122–123 | `<%= dateFormat %>` — emitted into JavaScript string argument | Derived from `sessDateFormat` session attribute |
| 132–134 | AJAX URL built with `$('input[name=unit_id]').val()` and date field values | DOM values (all user-controllable at runtime) |

**`<html:form>` at line 24:** Struts 1.3.10 `html:form` does **not** generate a CSRF synchroniser token by default.

**`<bean:write>` tag note:** In Struts 1.x, `<bean:write>` does **not** HTML-encode output by default; it requires the `filter="true"` attribute to escape HTML entities.

### 1.3 AssignmentByCompanyAndUnitIdQuery.java — SQL Methods

| Line(s) | Method / mechanism | Parameterised? |
|---------|-------------------|----------------|
| 14–18 | Static `query` String with three `?` placeholders | Yes — placeholders only |
| 29 | `DBUtil.queryForObjects(query, this::prepareStatement, ...)` | Yes — delegates binding to `prepareStatement` |
| 42–46 | `PreparedStatement` binding via `StatementPreparer.addLong()` for `unitId`, `companyId` (×2) | Yes — `PreparedStatement` |
| 32–39 | `ResultSet` column access by name (`getString`, `getInt`, `getDate`, `getBoolean`) | n/a — read-only mapping |

**No string concatenation into SQL is present.** All three parameter slots are bound via `PreparedStatement`.

---

## 2. Findings

### FINDING-001
**Severity:** CRITICAL
**File:** `src/main/webapp/html-jsp/apiXml.jsp`
**Lines:** 11–13 (method attribute retrieval and first use)
**Category:** Authentication — Unauthenticated API endpoint

**Description:**
`api.do` is explicitly listed in `PreFlightActionServlet.excludeFromFilter()` (line 106 of `PreFlightActionServlet.java`) with `return false`, which means the auth gate — the `sessCompId != null` check — is **never applied** to requests reaching the `api.do` path. `apiXml.jsp` is the view rendered for that action. Any unauthenticated HTTP client can call `api.do` and receive XML responses containing vehicle lists, driver names, question content, and checklist result data.

**Evidence:**
```java
// PreFlightActionServlet.java line 106
else if (path.endsWith("api.do")) return false;
```
When `excludeFromFilter` returns `false`, the surrounding `if(excludeFromFilter(path))` block at line 48 is skipped, so the `sessCompId` check at lines 56–60 is never reached for this path.

**Recommendation:**
Remove `api.do` from the exclusion list **or** implement token-based authentication (e.g., API key / Bearer token validated inside the Action) before the data is placed into request attributes for the JSP to render. If mobile/device clients require unauthenticated access, an isolated credential model (per-device token) should be used rather than bypassing all session-based auth.

---

### FINDING-002
**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/apiXml.jsp`
**Lines:** 24, 33, 42
**Category:** XML Injection / XSS (XML context)

**Description:**
`UnitBean.getName()`, `DriverBean.getFirst_name()`, `DriverBean.getLast_name()`, `AttachmentBean.getName()`, and `UnitBean.getId()` / `DriverBean.getId()` / `AttachmentBean.getId()` are all written directly into XML element bodies via string concatenation with **no escaping**. If any of these DB-sourced strings contain `<`, `>`, `&`, `"`, or `'` characters, the resulting XML will be malformed or contain injected markup. Because the endpoint is unauthenticated (see FINDING-001), an attacker who can influence these values (e.g., by registering a vehicle with a crafted name) can produce XML that injects elements visible to parsing clients, breaking client-side XML parsers or injecting content rendered by those clients.

**Evidence:**
```java
// apiXml.jsp line 24
resp=resp+"<rec><id>"+unitBean.getId()+"</id><name>"+ unitBean.getName()+"</name></rec>";
// line 33
resp=resp+"<rec><id>"+driverBean.getId()+"</id><name>"+ driverBean.getFirst_name()+" "+ driverBean.getLast_name()+"</name></rec>";
// line 42
resp=resp+"<rec><id>"+attachmentBean.getId()+"</id><name>"+ attachmentBean.getName()+"</name></rec>";
```

**Recommendation:**
Use a proper XML serialisation library (e.g., JAXB, `DocumentBuilder`, or a SAX/StAX writer) rather than manual string concatenation. As a minimum interim fix, apply XML entity encoding to all dynamic values before insertion: replace `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`, `'` → `&apos;`. Extract this into a shared utility method.

---

### FINDING-003
**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/apiXml.jsp`
**Lines:** 53–71
**Category:** Broken XML Sanitisation — Incomplete Escaping (XSS/XML Injection)

**Description:**
The question `content` field is partially sanitised, but the logic uses a chained `else if` block rather than sequential `if` statements. As a result, **only the first matching character class is substituted** per string value. A value containing both `&` and `<` (e.g., `"AT&T <br>"`) will only have `&` replaced; the `<` will pass through unescaped. This partial escaping provides a false sense of security and still allows XML injection via multi-character payloads.

Additionally, line 70 contains a **copy-paste bug**: the condition tests `content.contains(">")` but the replacement incorrectly substitutes `<` with `&gt;` instead of `>` with `&gt;`. The `>` character therefore passes through unmodified into the XML output.

**Evidence:**
```java
// lines 53–71 — else-if chain means only the first match is processed
if(content.contains("&")) {
    content = content.replace("&","&amp;");
} else if(content.contains("'")) {
    ...
} else if(content.contains("<")) {
    ...
} else if(content.contains(">")) {
    content = content.replace("<","&gt;");  // BUG: replaces "<" not ">"
}
```

**Recommendation:**
Replace the `else if` chain with sequential, independent `if` statements (or a single multi-pass replace), and fix the copy-paste bug on line 70. Better still, use `StringEscapeUtils.escapeXml11()` from Apache Commons Text (already a transitive dependency in many Struts projects) applied to every dynamic value in this file, or use an XML serialisation library as described in FINDING-002.

---

### FINDING-004
**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/vehicle/assignment.jsp`
**Lines:** 5–6, 14–19, 72
**Category:** XSS — Reflected, Unescaped `equipId` in HTML Attribute Context

**Description:**
`request.getParameter("equipId")` is stored in `id` (line 5) without any validation or HTML encoding. It is then reflected directly into multiple HTML attribute values:
- Line 14: `href="<%=urlGeneral %>"` where `urlGeneral` is built by concatenating `id` (line 6).
- Lines 15–19: `<%=id %>` appears four times inside `href` attribute values.
- Line 72: `value="<%=id %>"` in a hidden form input.

An attacker who can induce an authenticated user to visit a crafted URL (e.g., `assignment.jsp?equipId="><script>alert(1)</script>`) will cause arbitrary JavaScript to execute in the victim's browser session. This is a stored-authentication-context reflected XSS — the victim must be authenticated, but the CSRF structural gap (see FINDING-005) compounds the risk.

**Evidence:**
```java
// assignment.jsp line 5
String id = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
// line 6
String urlGeneral = id.isEmpty() ? "adminunit.do?action=add" : "adminunit.do?action=edit&equipId=" + id;
// line 14
<a href="<%=urlGeneral %>" class="general_u_tab">General</a>
// line 72
<input type="hidden" name="unit_id" id="unit_id" value="<%=id %>"/>
```

**Recommendation:**
HTML-encode `id` before use in any HTML context. Use `ESAPI.encoder().encodeForHTMLAttribute(id)` (OWASP ESAPI) or at minimum `id = id.replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll("\"","&quot;")` before the variable is used in markup. Additionally, validate that `equipId` is a numeric integer (matching `/^\d+$/`) and reject the request if it is not, since the backing query expects a numeric unit ID.

---

### FINDING-005
**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/vehicle/assignment.jsp`
**Lines:** 24, 73
**Category:** CSRF — No Synchroniser Token

**Description:**
The assignment form at line 24 uses `<html:form method="post" action="adminunitassign.do">`. In Struts 1.3.10, `<html:form>` does **not** automatically generate or validate a CSRF synchroniser token. No hidden CSRF token field is present anywhere in the form. The form submits a POST to `adminunitassign.do` which creates a vehicle-to-company assignment.

Because the auth gate only checks that a valid session exists (not that the request originated from the application's own UI), any website that can trick an authenticated admin into loading a page containing a forged form can silently create or delete vehicle assignments on their behalf. The `data-method-action="delete_assignment"` attribute on the delete anchor (line 93) similarly triggers a state-changing operation without any CSRF protection.

**Evidence:**
```html
<!-- assignment.jsp line 24 — no token field generated -->
<html:form method="post" action="adminunitassign.do" styleId="adminUnitAssignForm">
<!-- line 73 — only a static action hidden field -->
<input type="hidden" name="action" id="action" value="add"/>
```

**Recommendation:**
Implement the synchroniser token pattern. Options for Struts 1.x:
1. Call `saveToken(request)` in the Action's `execute` method that renders this page, and validate with `isTokenValid(request, true)` in `adminunitassign`'s Action.
2. Use a custom filter that generates and validates a per-session CSRF token stored in `HttpSession`, with the token embedded in the form as a hidden field and in AJAX requests as a custom header (`X-CSRF-Token`).

---

### FINDING-006
**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/vehicle/assignment.jsp`
**Lines:** 99, 102, 105, 108
**Category:** XSS — `<bean:write>` Without `filter="true"`

**Description:**
The four `<bean:write>` tags that render `company_name`, `start`, `end`, and `current` properties of `UnitAssignmentBean` do not include the `filter="true"` attribute. In Struts 1.x, `<bean:write>` outputs the property value **as-is** (no HTML encoding) unless `filter="true"` is explicitly set. If any of these values contain HTML special characters (e.g., a company name containing `<` or `&`), they will be rendered as raw HTML.

In the case of `company_name`, this value is a DB-sourced string that could have been set by an admin with write access to company records. While the immediate risk depends on input validation at the data entry layer, the output layer should not rely solely on upstream controls.

**Evidence:**
```jsp
<!-- assignment.jsp lines 99, 102, 105, 108 — no filter="true" -->
<bean:write property="company_name" name="assignment"/>
<bean:write property="start" name="assignment"/>
<bean:write property="end" name="assignment"/>
<bean:write property="current" name="assignment"/>
```

**Recommendation:**
Add `filter="true"` to all `<bean:write>` tags that render string content in an HTML context:
```jsp
<bean:write property="company_name" name="assignment" filter="true"/>
```
The `start`, `end`, and `current` fields are formatted date strings and a static "Yes"/"No" value respectively, so the risk is low for those three, but the fix should be applied consistently for defence-in-depth.

---

### FINDING-007
**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/vehicle/assignment.jsp`
**Lines:** 122–123
**Category:** XSS — Session-Derived `dateFormat` Injected into JavaScript String

**Description:**
`sessDateFormat`, fetched from the session at line 4 and transformed into `dateFormat`, is emitted directly into a JavaScript string argument at lines 122–123:
```javascript
setupDatePicker('#start_date', '<%= dateFormat %>', null);
```
If `sessDateFormat` contains a single quote, backslash, or newline character, the JavaScript string literal would be broken or injected into. Although `sessDateFormat` is set server-side (not from direct user input in this request), session attributes can in some flows be influenced by user-supplied data (e.g., if user preferences are stored). The value is not JavaScript-encoded before insertion.

**Evidence:**
```java
// assignment.jsp line 4
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
// lines 122–123
setupDatePicker('#start_date', '<%= dateFormat %>', null);
setupDatePicker('#end_date', '<%= dateFormat %>', null);
```

**Recommendation:**
Apply JavaScript string encoding to `dateFormat` before embedding it in a JS literal. Use `ESAPI.encoder().encodeForJavaScript(dateFormat)` or escape `\`, `'`, `"`, `\n`, `\r`, and `</` characters. Alternatively, pass the value as a `data-*` attribute on the HTML element and read it from the DOM in the script, which eliminates the inline injection vector entirely.

---

### FINDING-008
**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/apiXml.jsp`
**Lines:** 95–98
**Category:** Information Disclosure — Unescaped Error Message in XML Response

**Description:**
The `error` attribute (line 96, sourced from `request.getAttribute("error")`) is rendered directly into the XML response body without escaping. If the Action layer populates this attribute with exception messages, stack trace excerpts, SQL state codes, or internal class names, this information is disclosed to any caller of `api.do` — which, as established in FINDING-001, requires no authentication.

**Evidence:**
```java
// apiXml.jsp lines 95–98
if(error!=null && !error.equalsIgnoreCase(""))
{
    resp=resp+"<rec><error>"+error+"</error></rec>";
}
```

**Recommendation:**
1. Sanitise error messages before placing them into the `error` request attribute — use a fixed, user-facing message rather than raw exception text.
2. Apply XML entity encoding to the `error` value before rendering (as per the broader recommendation in FINDING-002).
3. Log full error detail server-side only.

---

### FINDING-009
**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/vehicle/assignment.jsp`
**Lines:** 131–148
**Category:** Authorization — AJAX Validation Endpoint Receives Unvalidated Unit ID from DOM

**Description:**
The AJAX call at lines 131–134 constructs its URL from `$('input[name=unit_id]').val()`, which reads the hidden `unit_id` form field. This field is rendered from the unvalidated `equipId` request parameter (line 72). An attacker can manipulate the DOM (or send a direct request) to substitute any `unit_id` value, potentially validating assignment date ranges against a unit belonging to a different company. The downstream `assigndatesvalid.do` action would need to verify that the submitted `unit_id` belongs to the requesting user's company — if it does not, cross-company data probing is possible.

**Evidence:**
```javascript
// assignment.jsp lines 132–134
url: 'assigndatesvalid.do?action=validate&unit_id=' + $('input[name=unit_id]').val() +
    '&start=' + $('#start_date').val() +
    '&end=' + $('#end_date').val(),
```

**Recommendation:**
The `assigndatesvalid.do` Action must re-validate that the supplied `unit_id` is owned by (or accessible to) the session's `sessCompId` before performing any query. Do not rely on the hidden form field value as a trusted input. This is a server-side authorization check and must not be enforced solely on the client side.

---

### FINDING-010
**Severity:** LOW
**File:** `src/main/webapp/html-jsp/apiXml.jsp`
**Lines:** 1, 7
**Category:** Content-Type Mismatch — `pageEncoding` vs. `setContentType`

**Description:**
The `<%@ page %>` directive at line 1 declares `contentType="text/html;charset=UTF-8"`, but line 7 overrides this at runtime with `response.setContentType("text/xml")`. The `charset` parameter is lost in the override, so the XML response is served without an explicit charset declaration in the HTTP `Content-Type` header. XML parsers that do not default to UTF-8 may misparse multi-byte characters.

**Evidence:**
```jsp
// line 1
<%@ page language="java" contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"%>
// line 7
response.setContentType("text/xml");
```

**Recommendation:**
Change line 7 to `response.setContentType("text/xml; charset=UTF-8");` and remove the misleading `contentType="text/html"` from the `page` directive, or replace it with `contentType="text/xml; charset=UTF-8"` so it is consistent.

---

### FINDING-011
**Severity:** LOW
**File:** `src/main/webapp/html-jsp/apiXml.jsp`
**Lines:** 75–88
**Category:** Dead / Duplicate Code

**Description:**
The `else if(method.equalsIgnoreCase(RuntimeConf.API_RESULT))` block appears twice (lines 75–81 and lines 82–88) with identical logic. The second block is unreachable dead code. While not a security vulnerability in isolation, dead code blocks are a maintenance liability that can mask future changes and complicate audits.

**Evidence:**
```java
// lines 75–81 (first occurrence)
else if(method.equalsIgnoreCase(RuntimeConf.API_RESULT)) { ... }
// lines 82–88 (second occurrence — unreachable)
else if(method.equalsIgnoreCase(RuntimeConf.API_RESULT)) { ... }
```

**Recommendation:**
Remove the duplicate block (lines 82–88).

---

### FINDING-012
**Severity:** INFO
**File:** `src/main/java/com/querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`
**Lines:** 14–18, 42–46
**Category:** SQL Injection — NO ISSUES

**Description:**
All three parameters (`unit_id`, `company_id`, `parent_company_id`) are bound via `PreparedStatement` using `StatementPreparer.addLong()`. No string concatenation into the query is present. The query is a static constant with placeholder-only parameterisation. This is correctly implemented.

---

### FINDING-013
**Severity:** INFO
**File:** `src/main/java/com/querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`
**Lines:** 14–18
**Category:** Data Access Scope — NO ISSUES

**Description:**
The WHERE clause contains `unit_id = ? AND (company_id = ? OR parent_company_id = ?)`. The query is scoped to the calling company's ID (and its parent) in addition to the unit ID. This prevents one company from reading assignment records belonging to another company simply by varying the `unit_id` parameter. The scoping is structurally correct.

Note: the effectiveness of this control depends on how `companyId` is sourced before constructing this query object. Auditors should verify at the Action layer that `companyId` is drawn from `session.getAttribute("sessCompId")` and not from a user-supplied request parameter.

---

### FINDING-014
**Severity:** INFO
**File:** `src/main/webapp/html-jsp/vehicle/assignment.jsp`
**Lines:** 1
**Category:** Authentication — Context Note

**Description:**
`assignment.jsp` is rendered as a Struts tile/include (not a direct JSP URL). The `.do` path that triggers this view (e.g., `adminunit.do?action=assignment`) goes through `PreFlightActionServlet`, which **does** check `sessCompId != null` for paths not in the exclusion list. `adminunit.do` is not in the exclusion list, so this view is correctly protected by the session auth gate. No authentication bypass is present for this file.

---

## 3. Summary Table

| ID | Severity | File | Category | Title |
|----|----------|------|----------|-------|
| 001 | CRITICAL | apiXml.jsp | Authentication | `api.do` bypasses session auth gate entirely |
| 002 | HIGH | apiXml.jsp | XML Injection/XSS | Unescaped bean values in XML output (units, drivers, attachments) |
| 003 | HIGH | apiXml.jsp | XML Injection/XSS | Broken `else-if` sanitisation for question content + copy-paste bug on line 70 |
| 004 | HIGH | assignment.jsp | XSS (Reflected) | Unencoded `equipId` reflected into HTML attribute and hidden field |
| 005 | HIGH | assignment.jsp | CSRF | No synchroniser token on assignment create/delete form |
| 006 | MEDIUM | assignment.jsp | XSS | `<bean:write>` tags missing `filter="true"` |
| 007 | MEDIUM | assignment.jsp | XSS (DOM/JS) | `dateFormat` session value emitted into JS literal without JS encoding |
| 008 | MEDIUM | apiXml.jsp | Information Disclosure | Raw `error` attribute (may contain exception detail) returned to unauthenticated callers |
| 009 | MEDIUM | assignment.jsp | Authorization | AJAX unit_id drawn from DOM; server must re-validate ownership |
| 010 | LOW | apiXml.jsp | Content-Type | `text/xml` response missing charset parameter |
| 011 | LOW | apiXml.jsp | Code Quality | Duplicate unreachable `API_RESULT` else-if block |
| 012 | INFO | AssignmentByCompanyAndUnitIdQuery.java | SQL Injection | No issues — PreparedStatement used correctly |
| 013 | INFO | AssignmentByCompanyAndUnitIdQuery.java | Data Access Scope | No issues — company scoping present in WHERE clause |
| 014 | INFO | assignment.jsp | Authentication | No bypass — view served via authenticated `.do` path |

---

## 4. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH | 4 |
| MEDIUM | 4 |
| LOW | 2 |
| INFO | 3 |
| **Total** | **14** |
