# Security Audit Report: adminJob.jsp

**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Audit Run:** audit/2026-02-26-01
**Auditor:** Automated Pass 1
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet session gate

---

## 1. Reading Evidence

### Form Action URLs

| Line | Method | Action URL | Purpose |
|------|--------|------------|---------|
| 35 | POST | `adminunit.do` | Edit existing job (one form per job, iterated) |

### Request Parameters Used in Output or Hidden Fields

| Line | Parameter | Usage |
|------|-----------|-------|
| 3 | `request.getParameter("action")` | Captured into scriptlet variable `action` |
| 4 | `request.getParameter("equipId")` | Captured into scriptlet variable `id` |
| 9 | `id` (from `equipId`) | Written unescaped into `<input value="...">` via `<%=id %>` |
| 10 | `action` (from `action`) | Written unescaped into `<input value="...">` via `<%=action %>` |
| 72 | `id` (from `equipId`) | Written unescaped into hidden `<input value="...">` per-form via `<%=id %>` |

### Struts Tags That Output Data

| Line | Tag | Bean | Property | filter Attribute |
|------|-----|------|----------|-----------------|
| 38 | `<bean:write>` | `jobs` | `jobTitle` | Not set (default escaping applies) |
| 42 | `<bean:write>` | `jobs` | `description` | Not set (default escaping applies) — inside `<textarea>` |
| 45 | `<bean:write>` | `jobs` | `driverName` | Not set (default escaping applies) |
| 68 | `<bean:write>` | `jobs` | `unitId` | Not set — embedded in href attribute string |
| 68 | `<bean:write>` | `jobs` | `jobNo` | Not set — embedded in href attribute string |
| 73 | `<bean:write>` | `jobs` | `id` | Not set — inside hidden `<input value="...">` |

### JavaScript Blocks That Use Server-Side Data

| Lines | Description |
|-------|-------------|
| 6–8 | Empty `<script>` block — no server data used |
| 93–119 | `triggerClick(id, genId)` builds a dynamic anchor tag using JS-parameter `id` and `genId` (passed from caller, not directly from server-side output in this file). `saveJobs()` serialises all `.ajax_mode_c` forms and posts them via `ajax_recaller`. No server-side data injected directly into JS string literals in this file. |
| 101 | `href="driverjob.do?action=assign&equipId='+id+'&job_id='+genId+'"` — `id` and `genId` are JS function arguments; their origin depends on the call site (see Finding XSS-3). |

---

## 2. Findings

---

### [HIGH] XSS-1 — Unescaped Request Parameter Reflected into HTML Attribute Value

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Lines:** 9, 10, 72

**Description:**
The JSP captures `equipId` and `action` directly from the request at lines 3–4 using a scriptlet, then writes them unescaped into HTML `<input value="...">` attributes at lines 9, 10, and 72 using the JSP expression `<%=id %>` and `<%=action %>`. No HTML encoding is applied. An attacker who can influence these parameters (e.g., through a reflected URL or an opener frame) can inject arbitrary HTML and JavaScript.

**Evidence:**
```jsp
// Lines 3-4
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String id     = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");

// Lines 9-10
<input type="hidden" name="equip_id" value="<%=id %>" />
<input type="hidden" name="action"   value="<%=action %>" />

// Line 72 (inside the logic:iterate loop, per job)
<input type="hidden" name="equipId" value="<%=id %>" />
```

A payload such as `equipId="><script>alert(1)</script>` would break out of the `value` attribute and execute arbitrary script.

**Recommendation:**
Replace all scriptlet-based output with properly escaped equivalents. Use `ESAPI.encoder().encodeForHTML(id)` or the Struts `<bean:write>` tag (which HTML-escapes by default), or at minimum use `org.apache.commons.lang.StringEscapeUtils.escapeHtml(id)` before writing to the response. Never write raw request parameters into HTML attributes.

---

### [HIGH] XSS-2 — `<bean:write>` Output in href Attribute Without URL Encoding

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Line:** 68

**Description:**
`jobs.unitId` and `jobs.jobNo` are bean properties of type `int` / `String` respectively, written directly into an `href` attribute as query-string values. While `<bean:write>` HTML-escapes by default, the values are embedded in a URL context inside an `href`. A `jobNo` value containing characters such as `"`, `>`, or JavaScript protocol strings (e.g. if stored as a non-numeric string) could break out of the attribute or enable an injection. More critically, `jobNo` is a `String` field with no validation visible in `JobDetailsBean`; if a malicious value reaches the database (e.g. via add_job), it will be reflected here.

**Evidence:**
```jsp
<a title="View Details"
   href="jobdetails.do?action=details&equipId=<bean:write name="jobs" property="unitId" />&job_no=<bean:write name="jobs" property="jobNo" />"
   data-toggle="lightbox" ...>
```
`unitId` is an `int` (safe). `jobNo` is a `String` with no enforced format — a stored value of `foo" onmouseover="alert(1)` would become an XSS vector.

**Recommendation:**
URL-encode query-string values in `href` attributes. Use `<c:url>` / `<c:param>` from JSTL, or manually apply `java.net.URLEncoder.encode()` in the action before placing values in request scope. Additionally enforce that `jobNo` is validated/sanitised on write (see `AdminUnitAction` `add_job` / `edit_job` handlers — no sanitisation observed).

---

### [MEDIUM] XSS-3 — JS `triggerClick` Builds DOM href from Unsanitised JS Arguments

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Lines:** 94–105

**Description:**
The `triggerClick(id, genId)` function constructs an anchor element by string-concatenating the `id` and `genId` function arguments directly into an HTML string that is injected into the DOM via jQuery `$('...')`. If the caller passes values that originate from attacker-controlled data (e.g. a job ID that was stored containing special characters), this is a DOM-XSS vector.

**Evidence:**
```javascript
$('<a id="hLink" title="Driver Allocation"
   href="driverjob.do?action=assign&equipId='+id+'&job_id='+genId+'"
   data-backdrop="static" ...><span class="btn-xs">&nbsp</span></a>')
  .appendTo($('body'));
document.getElementById('hLink').click();
document.getElementById('hLink').remove();
```
If `id` or `genId` contains `" onmouseover="alert(1)` or similar, it is injected verbatim into the HTML string before jQuery parses it.

**Note:** In the current file, `triggerClick` is defined but never called (the call site is commented out on line 18). However the function is registered on the global scope and could be invoked from other pages or scripts that load this fragment. The risk should be treated as active until the function is removed or hardened.

**Recommendation:**
Use `document.createElement('a')` and set `href` via `.setAttribute()` or `.href = ...` rather than injecting into an HTML string. Validate / type-assert that `id` and `genId` are numeric before use.

---

### [MEDIUM] XSS-4 — `<bean:write>` for `description` Inside `<textarea>` Without Explicit `filter="true"`

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Line:** 42

**Description:**
`jobs.description` is output inside a `<textarea>` element using `<bean:write>`. In Struts 1.3.x, `<bean:write>` HTML-escapes output by default (equivalent to `filter="true"`), which is correct. However the absence of the explicit `filter="true"` attribute creates a maintenance risk: it relies on the default behaviour being preserved, which is non-obvious to maintainers and has historically been a source of regression when tag library versions change. Additionally, `description` is a free-text `String` field that is stored and replayed with no sanitisation visible at the DAO layer.

**Evidence:**
```jsp
<textarea name="description" cols=100 class="form-control fader">
    <bean:write name="jobs" property="description" />
</textarea>
```

**Recommendation:**
Add `filter="true"` explicitly to make the escaping intent unambiguous. Independently, consider sanitising job description content on save in `AdminUnitAction` (lines 85–99) before persisting.

---

### [MEDIUM] XSS-5 — `<bean:write>` for `jobTitle` in Input `value` Attribute Without Explicit `filter="true"`

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Line:** 38

**Description:**
Same maintenance concern as XSS-4. `jobTitle` is written into an `<input value='...' />` attribute using single-quote delimiters. The default HTML escaping in `<bean:write>` escapes `<`, `>`, `&`, and `"` but does NOT escape single quotes. If the stored `jobTitle` contains a single quote, it can break out of the `value='...'` attribute.

**Evidence:**
```jsp
<input name="title" ... value='<bean:write name="jobs" property="jobTitle" />' class="form-control fader" />
```
A `jobTitle` stored as `O'Brien's Forklift` would render as `value='O'Brien's Forklift'`, causing a malformed attribute. A malicious title such as `' onmouseover='alert(1)` would result in attribute injection.

**Recommendation:**
Switch the attribute delimiter to double quotes and add `filter="true"` to `<bean:write>`, or use `<c:out value="${jobs.jobTitle}" escapeXml="true" />`. Validate `jobTitle` on input (it has a `maxlength="50"` client-side hint but no server-side validation visible in `AdminUnitAction`).

---

### [CRITICAL] CSRF-1 — All Job Mutation Forms Lack CSRF Tokens

**Severity:** CRITICAL
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Lines:** 35–74, and `saveJobs()` at lines 110–118

**Description:**
Every `<form method="post" action="adminunit.do">` emitted in the `logic:iterate` loop submits state-changing operations (`action=edit_job`) to `AdminUnitAction`. The `saveJobs()` function serialises all such forms and fires them as sequential AJAX POST requests via `ajax_recaller`. No CSRF token is present in any form or AJAX call. The application uses no Spring Security and has no visible token mechanism anywhere in the stack.

An attacker can craft a page that causes a logged-in admin's browser to submit arbitrary job edits (title, description) to `adminunit.do` without the victim's knowledge.

**Evidence:**
```jsp
<form method="post" action="adminunit.do" class="ajax_mode_c edit_job">
    ...
    <input type="hidden" name="action" value="edit_job" />
    <input type="hidden" name="equipId" value="<%=id %>" />
    <input type="hidden" name="job_id" value="<bean:write name="jobs" property="id" />" />
</form>
```
```javascript
// scripts.js lines 740-770
$.ajax({
    type: "POST",
    data: list[recalled].serialize(),
    url: list[recalled].attr('action'),  // adminunit.do
    ...
});
```
No `X-CSRF-Token` header, no hidden token field, no `SameSite` cookie controls observed.

**Recommendation:**
Implement the Synchronizer Token Pattern: generate a per-session CSRF token in `PreFlightActionServlet` or a base action, store it in the session, render it as a hidden field in all mutating forms and include it as a request header in all AJAX calls, then validate it in `AdminUnitAction` before processing any state-changing action. Also set `SameSite=Strict` or `SameSite=Lax` on the session cookie.

---

### [CRITICAL] CSRF-2 — AJAX POST to `adminunit.do` (add_job) Without CSRF Token

**Severity:** CRITICAL
**File:** `src/main/webapp/skin/js/scripts.js` (called from `adminJob.jsp` context)
**Lines:** 700–718 (scripts.js), 110–118 (adminJob.jsp)

**Description:**
The "Add Job" flow (triggered by the `addjob` button at line 16) dynamically injects a new form into the DOM (scripts.js lines 700–718) with `action="adminunit.do"` and `action=add_job`. This form is then serialised and POSTed via `ajax_recaller`. No CSRF token is injected into the dynamically-built form template. This is the same structural gap as CSRF-1 but on the add path.

**Evidence:**
```javascript
// scripts.js ~line 700-703
'<form method="post" action="adminunit.do" class="ajax_mode_c save_job">'
  + '<input type="hidden" name="job_no" value="' + genId + '" />'
  + '<input type="hidden" name="action" value="add_job" />'
  + '<input type="hidden" name="equipId" value="' + equipId + '" />'
```

**Recommendation:**
Same as CSRF-1. The dynamically built form template must also include the CSRF token, which should be read from a page-level JS variable that is itself populated from the session token on page load.

---

### [HIGH] CSRF-3 — Driver Assignment Navigation Link Triggers State-Changing Action Without Token

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Lines:** 101–103

**Description:**
`triggerClick` constructs a link to `driverjob.do?action=assign` and programmatically clicks it. While this is a GET-based navigation to a form (not itself a direct mutation), the endpoint `driverjob.do` maps to `DriverJobDetailsAction` which also handles `assign_driver` (a mutation). The use of GET for navigation to sensitive assignment workflows, combined with no CSRF protection on the underlying action, is a risk escalation point. More directly, the pattern of programmatic click on a constructed anchor to trigger lightbox loading of the assignment form means any CSRF protection must also cover the assignment form loaded in the lightbox.

**Evidence:**
```javascript
$('<a id="hLink" ... href="driverjob.do?action=assign&equipId='+id+'&job_id='+genId+'" ...></a>')
  .appendTo($('body'));
document.getElementById('hLink').click();
document.getElementById('hLink').remove();
```

**Recommendation:**
Ensure the driver assignment form rendered by `driverjob.do` contains a CSRF token and that the action validates it. Convert driver assignment to a POST-only flow.

---

### Authentication / Authorization

**NO separate issues found in this file.**

The page is loaded as a fragment within the admin lightbox pattern. Session-level authentication is enforced by `PreFlightActionServlet` checking `sessCompId != null` before any `.do` action is dispatched. The `AdminUnitAction.execute()` confirms it reads `sessCompId` from the session and uses it to scope company-level data. The job list (`arrJobs`) is loaded with `jobsDAO.getJobList(equipId)` where `equipId` is a request parameter — there is a potential insecure direct object reference (IDOR) risk if `equipId` is not validated against the session company, but this is in `AdminUnitAction` rather than in this JSP. That concern is noted for the `AdminUnitAction` audit file, not raised as a finding here.

No role-differentiated admin actions are visible in this file — all visible actions (add job, edit job, view details) are consistent with a generic admin session.

---

### Information Disclosure

**NO high-severity issues found.**

The `jobs.description` and `jobs.jobTitle` fields are expected business data for an admin managing equipment jobs. No internal paths, stack traces, DB credentials, or system metadata are rendered by this page.

`jobs.id`, `jobs.unitId`, and `jobs.jobNo` are exposed as integer/string identifiers in hidden fields and URL parameters. While predictable sequential IDs could facilitate enumeration, this is a design-level concern consistent with the rest of the application and is rated INFO.

---

### [INFO] INFO-1 — Sequential Integer IDs Exposed in Hidden Fields and URLs

**Severity:** INFO
**File:** `src/main/webapp/html-jsp/adminJob.jsp`
**Lines:** 68, 73

**Description:**
`jobs.id` (database primary key) and `jobs.unitId` are written into hidden form fields and query-string parameters. If the session boundary check in `AdminUnitAction` does not verify that `job_id` belongs to the requesting company, these sequential IDs could enable IDOR. This is noted here for completeness; the authorisation check must be evaluated at the DAO / action layer.

**Evidence:**
```jsp
<input type="hidden" name="job_id" value="<bean:write name="jobs" property="id" />" />
href="jobdetails.do?action=details&equipId=<bean:write name="jobs" property="unitId" />&job_no=<bean:write name="jobs" property="jobNo" />"
```

**Recommendation:**
Verify in `JobsDAO.editJob()` and `JobsDAO.getJobListByJobId()` that the supplied `job_id` / `equipId` belongs to the `sessCompId` company before operating on it.

---

## 3. Summary

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 2 | CSRF-1, CSRF-2 |
| HIGH | 3 | XSS-1, XSS-2, CSRF-3 |
| MEDIUM | 3 | XSS-3, XSS-4, XSS-5 |
| LOW | 0 | — |
| INFO | 1 | INFO-1 |
| **Total** | **9** | |

---

## 4. Key Remediation Priorities

1. **CSRF-1 / CSRF-2 (CRITICAL):** Implement the Synchronizer Token Pattern across all mutating forms and AJAX calls. This is a systemic gap affecting the entire application, not just this file.
2. **XSS-1 (HIGH):** Eliminate all raw scriptlet `<%=request.getParameter(...)%>` output into HTML. Apply `ESAPI.encodeForHTML()` or equivalent at every write point.
3. **XSS-2 (HIGH):** Apply URL encoding to `bean:write` outputs embedded in `href` query strings; validate `jobNo` on input.
4. **XSS-5 (MEDIUM):** Change `value='...'` single-quote delimiters to double-quotes for all `<bean:write>` attributes, add `filter="true"` explicitly.
5. **XSS-3 (MEDIUM):** Refactor `triggerClick` to use DOM methods rather than HTML string concatenation.
