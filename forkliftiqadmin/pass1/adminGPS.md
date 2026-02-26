# Security Audit Report: adminGPS.jsp

**File:** `src/main/webapp/html-jsp/adminGPS.jsp`
**Audit run:** audit/2026-02-26-01/
**Auditor:** CIG Automated Pass 1
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet session gate

---

## 1. Reading Evidence

### Form Action URLs

| Line | Method | Action |
|------|--------|--------|
| 17 | POST | `adminunit.do` |

### Request Parameters Used in Output or JS

| Line | Parameter / Source | Usage Location |
|------|--------------------|----------------|
| 3 | `session.getAttribute("sessDateFormat")` | Scriptlet — stored in local Java var `dateFormat`; **never rendered to the page** in this file |
| 44 | `custCd` (Java scriptlet variable, hardcoded `"0"`) | Written into `<input type="hidden" name="cust_cd" value="<%=custCd %>">` |
| 72–73 | `$('#cust').val()` | JS — read from a DOM element (presumably set by a parent/menu include), appended directly into an AJAX URL string |
| 74 | `$('#site').val()` | JS — same as above |
| 76 | `str` (function parameter, caller-supplied) | JS — appended directly into an AJAX URL string |

### Struts Tags That Output Data

| Line | Tag | Bean / Property | filter attribute |
|------|-----|-----------------|-----------------|
| 26 | `<bean:write property="id" name="unitRecord" />` | `UnitBean.id` | **not specified** (defaults to `true` — HTML-escaped) |
| 27 | `<bean:write property="name" name="unitRecord" />` | `UnitBean.name` | **not specified** (defaults to `true` — HTML-escaped) |

Both `<bean:write>` calls are used inside an `<option>` element — one as the `value` attribute value (inline, no surrounding quotes from the tag itself) and one as the visible text content.

### JavaScript Blocks Using Server-Side Data

| Lines | Description |
|-------|-------------|
| 48–103 | Single `<script>` block; uses `$('#cust').val()` and `$('#site').val()` from DOM, and a caller-supplied `str` parameter, to build an AJAX URL without encoding |
| 64 | `initialize($('#cust').val(),$('#site').val())` — passes DOM values directly to a function defined in an external script (`ajaxStore.js` / `scripts.js`) |
| 76 | `url:'../master/get_cust_vehicle.jsp?cust_cd='+cust_cd+"&loc_cd="+loc_cd+"&dept_cd="+str` — URL built by string concatenation |

---

## 2. Findings

---

### FINDING 1 — MEDIUM — CSRF: Unprotected POST Form to State-Changing Action

**Severity:** MEDIUM
**File:Line:** `src/main/webapp/html-jsp/adminGPS.jsp:17`

**Description:**
The page contains an HTML form that POSTs to `adminunit.do`. The `adminunit.do` action (`AdminUnitAction`) handles multiple state-changing operations including `delete` (permanent unit deletion), `add_job`, `edit_job`, and `assignment` mutations, all dispatched via the `action` request parameter. There is no CSRF token in this form. The application has no framework-level CSRF protection (confirmed: no Spring Security, no custom token filter in `web.xml`). Any authenticated admin user visiting a malicious page can have their browser silently submit a cross-origin POST to `adminunit.do` with arbitrary parameters (e.g., `action=delete&equipId=<id>`).

**Evidence:**
```jsp
<!-- adminGPS.jsp line 17 -->
<form method="post" action="adminunit.do" name="adminUnitEditForm" id="adminUnitForm">
```
```java
// AdminUnitAction.java lines 57-61
} else if (action.equalsIgnoreCase("delete")) {
    unitDAO.delUnitById(equipId);
    ...
}
```
No CSRF token field is present anywhere in the form, and no token validation exists in `AdminUnitAction.execute()`.

**Recommendation:**
Implement a synchronizer token pattern. Generate a cryptographically random per-session (or per-request) token, store it in the HTTP session, render it as a hidden form field, and validate it in `AdminUnitAction` (or a shared base action/filter) before processing any mutating action. Reject requests where the submitted token does not match the session token.

---

### FINDING 2 — LOW — XSS (Latent): `<bean:write>` Inside HTML Attribute Without Explicit `filter="true"`

**Severity:** LOW
**File:Line:** `src/main/webapp/html-jsp/adminGPS.jsp:26`

**Description:**
The `<bean:write>` tag at line 26 renders `UnitBean.id` directly as the `value` attribute of an `<option>` element using inline concatenation — the tag output is placed between the surrounding `"` characters of the attribute value without any extra quoting layer:

```jsp
<option value="<bean:write property="id" name="unitRecord" />">
```

The Struts 1 `<bean:write>` tag defaults `filter` to `true`, which applies HTML entity encoding. In the common case this prevents HTML-context XSS. **However**, the `filter` attribute is not explicitly set, leaving the protection entirely implicit. If a future developer copies this pattern but sets `filter="false"` — or if this tag is ever refactored to a raw scriptlet or JSTL `${...}` expression — the protection silently disappears. Additionally, if `UnitBean.id` ever contains characters such as `"` (double-quote), the HTML attribute context is broken even with entity encoding (Struts HTML-encodes `"` as `&quot;` in some configurations, but this depends on the tag implementation version).

**Evidence:**
```jsp
<!-- line 26 -->
<option value="<bean:write property="id" name="unitRecord" />">
    <bean:write property="name" name="unitRecord"/>
</option>
```
`filter` attribute is absent on both `<bean:write>` calls.

**Recommendation:**
Explicitly declare `filter="true"` on every `<bean:write>` tag so the intent is unambiguous and protected during code review and refactoring:
```jsp
<option value="<bean:write property="id" name="unitRecord" filter="true" />">
    <bean:write property="name" name="unitRecord" filter="true"/>
</option>
```

---

### FINDING 3 — LOW — XSS (Latent): AJAX URL Built by String Concatenation Without Encoding

**Severity:** LOW
**File:Line:** `src/main/webapp/html-jsp/adminGPS.jsp:76`

**Description:**
The `fetchUnit(str)` function constructs the URL for an AJAX request by direct string concatenation of DOM-sourced values and the caller-supplied `str` parameter:

```javascript
url:'../master/get_cust_vehicle.jsp?cust_cd='+cust_cd+"&loc_cd="+loc_cd+"&dept_cd="+str,
```

None of `cust_cd`, `loc_cd`, or `str` are passed through `encodeURIComponent()` before being appended to the URL. If any of these values contain special characters (e.g., `&`, `=`, `#`, `+`), the query string is malformed, potentially allowing parameter injection into the downstream JSP request. If the downstream JSP (`get_cust_vehicle.jsp`) reflects any of these parameters unsafely, this becomes a reflected XSS vector exploitable from the client side.

The `str` parameter is passed to `fetchUnit()` from caller code (not visible in this file). Its origin and sanitization are not verified here.

**Evidence:**
```javascript
// adminGPS.jsp lines 72–76
function fetchUnit(str) {
    var cust_cd = $('#cust').val();
    custCd = cust_cd;
    var loc_cd = $('#site').val();
    $.ajax({
        url:'../master/get_cust_vehicle.jsp?cust_cd='+cust_cd+"&loc_cd="+loc_cd+"&dept_cd="+str,
```

**Recommendation:**
Wrap all dynamic URL components in `encodeURIComponent()`:
```javascript
url: '../master/get_cust_vehicle.jsp?cust_cd=' + encodeURIComponent(cust_cd)
     + '&loc_cd=' + encodeURIComponent(loc_cd)
     + '&dept_cd=' + encodeURIComponent(str),
```
Additionally audit `get_cust_vehicle.jsp` to confirm it does not reflect these parameters into HTML or JavaScript without escaping.

---

### FINDING 4 — LOW — Unhandled NullPointerException Risk from Session Attribute

**Severity:** LOW
**File:Line:** `src/main/webapp/html-jsp/adminGPS.jsp:3`

**Description:**
The scriptlet at line 3 calls `.replaceAll(...)` directly on the result of `session.getAttribute("sessDateFormat")` without a null check:

```java
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```

If `sessDateFormat` is absent from the session (e.g., after a partial session population, after deserialization of a session that pre-dates this attribute, or in a test/debug context), this throws a `NullPointerException` at page render time. The `web.xml` global error page redirects to `/error/error.html` for `java.lang.Exception`, which mitigates information leakage from a stack trace, but the NPE itself causes an unhanded failure that disrupts the page and could be exploited to deny service by triggering controlled session states.

Note: `dateFormat` is computed but never actually used or rendered anywhere in this JSP — making the entire line dead code and the risk purely theoretical in terms of XSS/injection, but the crash risk is real.

**Evidence:**
```java
// adminGPS.jsp line 3
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```
The variable `dateFormat` is never referenced again in the file.

**Recommendation:**
Either remove the dead code entirely (the variable is unused), or add a null guard:
```java
String rawFormat = (String) session.getAttribute("sessDateFormat");
String dateFormat = (rawFormat != null) ? rawFormat.replaceAll("yyyy", "yy").replaceAll("M", "m") : "";
```

---

### FINDING 5 — INFO — Dead/Unused JavaScript Function `fetchUnit()`

**Severity:** INFO
**File:Line:** `src/main/webapp/html-jsp/adminGPS.jsp:70–103`

**Description:**
The `fetchUnit(str)` function (lines 70–103) builds and fires an AJAX request to `../master/get_cust_vehicle.jsp` and then writes results into `document.forms[0].model_cd.options`. However, the current form (`adminUnitForm`) contains no `model_cd` select element — there is only `gps_vehicle` and `cust_cd`. There is no call to `fetchUnit()` anywhere within this file. The function appears to be dead/orphaned code copied from another page (likely a vehicle-filter form). Dead code introduces audit surface and maintenance risk.

**Evidence:**
```javascript
// adminGPS.jsp lines 70–103
function fetchUnit(str) { ... document.forms[0].model_cd.options.length=0; ... }
```
No `model_cd` element exists in the form on this page. No invocation of `fetchUnit` appears in the file.

**Recommendation:**
Remove the `fetchUnit()` function and associated AJAX logic from this page entirely to reduce attack surface and eliminate the dead URL concatenation finding (Finding 3) as a by-product.

---

### FINDING 6 — INFO — Commented-Out Hardcoded Geographic Coordinates (Australia)

**Severity:** INFO
**File:Line:** `src/main/webapp/html-jsp/adminGPS.jsp:54–55`

**Description:**
Commented-out code at lines 54–55 contains hardcoded GPS coordinates labeled "AU" (Australia), while active code at lines 57–58 contains coordinates labeled "UK". This suggests the application has been geographically migrated and the old default location was simply commented out rather than removed. No direct security risk, but it discloses deployment context and that the application has been used in Australia and the UK.

**Evidence:**
```javascript
// 	    var defaultLat = "-24.2761156"; //AU
// 	   	var defaultLong = "133.5912902";
var defaultLat = "55.378051"; //UK- 55.378051, -3.435973
var defaultLong = "-3.435973"
```

**Recommendation:**
Remove commented-out code before production deployment. If a configurable default location is required, source it from a server-side configuration value rather than hardcoding coordinates.

---

## 3. Category Summary

### XSS
Two latent findings (LOW severity). The `<bean:write>` tags rely on implicit `filter="true"` defaulting (Finding 2). The AJAX URL is built by unencoded string concatenation (Finding 3). Neither is immediately exploitable given current data flows, but both represent fragile protections.

### CSRF
One MEDIUM finding. The POST form targeting `adminunit.do` carries no CSRF token. `AdminUnitAction` performs destructive operations (unit delete, job add/edit) without any token validation. This is the highest-severity finding on this page.

### Authentication / Authorization
**No issues on this page.** The page is served through the `PreFlightActionServlet` which enforces `sessCompId != null` for all `.do` paths (confirmed in `PreFlightActionServlet.java` lines 56–60). The JSP itself contains no role-based conditional logic, which is appropriate for a page that delegates authorization to the action layer. No admin-only action links are constructed from user-supplied data.

### Information Disclosure
**No issues.** No stack traces are rendered. The global `web.xml` error handler redirects to a static HTML page. The GPS coordinates in comments (Finding 6) are INFO-level only.

### Sensitive Data Rendered
**No issues.** No passwords, credentials, tokens, or personal operator data are rendered on this page. The `UnitBean` properties output (`id`, `name`) are equipment identifiers appropriate to the GPS report context.

---

## 4. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 1 |
| LOW | 3 |
| INFO | 2 |
| **Total** | **6** |
