# Security Audit — JSP Files
**Audit ID:** 2026-02-25-01
**Agent:** A10
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25

---

## STEP 3 — FILE EVIDENCE SUMMARY

### 1. `security/auto_change_pass.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Beans:** `UtilBean` (page scope), `Databean_security` (request scope)
- **Includes:** None
- **Scriptlets:**
  - Lines 59–70: Reads `user_cd`, `user_fnm`, `user_lnm` from session; reads `message` and `reset` from request parameters; calls `filter.init()`
- **Expression outputs:**
  - Line 6: `<%=LindeConfig.systemName %>` — static config value
  - Line 117: `<%=user_fnm %> <%=user_lnm %>` — from session (originally from DB)
  - Line 154: `<%=message %>` — from request parameter `message`, unescaped
  - Line 162: `<%=reset%>` — from request parameter `reset`, unescaped (placed in hidden input value)
  - Line 163: `<%=user_cd%>` — from session, placed in hidden input
- **Forms:** `POST ../servlet/Frm_security` — inputs: `cpass`, `npass`, `rnpass`, `op_code` (hidden=`pass_chg`), `auto_reset` (hidden=`t`), `reset` (hidden), `user_cd` (hidden)
- **CSRF token:** None

---

### 2. `security/frm_access_rights.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 2), `../menu/menu.jsp` (line 299)
- **Beans:** `Databean_security` (request scope), `UtilBean` (page scope)
- **Scriptlets:**
  - Lines 215–275: Reads `message`, `gp_cd`, `user_cd` (session), `form_cd`, `cust_cd` from request; reads access-level attributes from session; calls `filter.init()` with all parameters; populates ArrayLists from bean
- **Expression outputs:**
  - Line 8: `<%=LindeConfig.systemName %>` — static
  - Line 219: `<%=message %>` — from request parameter, unescaped
  - Line 277: `<%=cust_cd %>`, `<%=gp_cd %>` — from request parameters, unescaped, injected into onLoad JS attribute
  - Lines 321, 330, 331, 342–344, 383, 397–417, 444–445, 452–454: DB-sourced values (customer names, group names, form codes, form names, permissions) — unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: checkboxes (view/edit/del/print), hidden fields: `op_code`, `count`, `user_cd`, `form_cd`
- **CSRF token:** None

---

### 3. `security/frm_add_form.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 2), `../menu/menu.jsp` (line 184)
- **Beans:** `Databean_security` (request scope), `UtilBean` (page scope)
- **Scriptlets:**
  - Lines 142–161: Reads `message`, `form_cd`, `frm_cd` from request; calls `filter.init()` and populates ArrayLists
- **Expression outputs:**
  - Line 206: `<%=form_nm %>` — DB value, unescaped
  - Line 265: `<%=message %>` — request parameter, unescaped
  - Lines 215, 235: DB-sourced `form_cd`, `form_nm`, `module_cd`, `module_nm` values in `<option>` elements — unescaped
  - Lines 272–273: `<%=form_cd %>`, `<%=frm_cd %>` — request parameters in hidden inputs, unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: `fname`, `path`, `desc`, `mod` (select), `op_code` (hidden), `form_cd` (hidden), `frm_cd` (hidden)
- **CSRF token:** None

---

### 4. `security/frm_add_mail_group.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 2), `../menu/menu.jsp` (line 93)
- **Beans:** `Databean_security` (request scope), `UtilBean` (page scope)
- **Scriptlets:**
  - Lines 51–69: Reads `message`, `grp_cd`, `form_cd` from request; calls `filter.init()`; populates `vgrp_cd`, `vgrp_nm`
- **Expression outputs:**
  - Lines 115, 129, 132, 152–158: DB-sourced group codes/names in links and table cells — unescaped; `<%=message %>` — request param, unescaped
  - Line 129: `set_editvalues('<%=vgrp_cd.get(i) %>','<%=vgrp_nm.get(i) %>')` — DB values injected into JS onclick attribute — unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: `gcd`, `gname`, `op_code` (hidden), `grp_cd` (hidden), `form_cd` (hidden)
- **CSRF token:** None

---

### 5. `security/frm_add_mail_group_pop.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 2)
- **Beans:** `Databean_security` (request scope), `UtilBean` (page scope)
- **Scriptlets:**
  - Lines 58–100: Reads `message`, `grp_cd`, `form_cd` from request; reads access-level attributes from session; calls `filter.init()`; populates ArrayLists for groups and customers
- **Expression outputs:**
  - Line 122: `set_editvalues('<%=vgrp_cd.get(i) %>','<%=vgrp_nm.get(i) %>','<%=mail_grp_cust.get(i)%>')` — DB values in JS onclick — unescaped
  - Lines 124, 141, 153: DB-sourced values in table cells — unescaped; `<%=message %>` — request param, unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: `gname`, `usr` (select for customer), `op_code` (hidden=`mail_group_add_pop`), `grp_cd` (hidden), `form_cd` (hidden)
- **CSRF token:** None

---

### 6. `security/frm_add_module.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 2), `../menu/menu.jsp` (line 180)
- **Beans:** `Databean_security` (request scope), `UtilBean` (page scope)
- **Scriptlets:**
  - Lines 138–156: Reads `message`, `module_cd`, `form_cd` from request; calls `filter.init()`; populates `vmodule_cd`, `vmodule_nm`
- **Expression outputs:**
  - Line 202: `<%=form_nm %>` — DB, unescaped; Line 250: `<%=message %>` — request param, unescaped
  - Lines 212, 256–257: DB-sourced module codes/names, request params in hidden inputs — unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: `frm` (select), `mname`, `ipath`, `desc` (textarea), `op_code` (hidden), `module_cd` (hidden), `form_cd` (hidden)
- **CSRF token:** None

---

### 7. `security/frm_change_pass.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 1), `../menu/menu.jsp` (line 94)
- **Beans:** `UtilBean` (page scope), `Databean_security` (request scope)
- **Scriptlets:**
  - Lines 60–71: Reads `user_cd` from session; reads `form_cd`, `message` from request; calls `filter.init()`
- **Expression outputs:**
  - Line 116: `<%=form_nm %>` — DB, unescaped; Line 120: `<%=user_fnm %> <%=user_lnm %>` — session values (DB origin), unescaped
  - Line 157: `<%=message %>` — request param, unescaped
  - Lines 164–165: `<%=user_cd%>`, `<%=form_cd %>` — session/request in hidden inputs, unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: `cpass`, `npass`, `rnpass`, `op_code` (hidden=`pass_chg`), `user_cd` (hidden), `form_cd` (hidden)
- **CSRF token:** None

---

### 8. `security/frm_edit_mail_list.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 2), `../menu/menu.jsp` (line 158)
- **Beans:** `Databean_security` (request scope), `UtilBean` (page scope)
- **Scriptlets:**
  - Lines 85–134: Reads `message`, `grp_cd`, `form_cd` from request; reads access-level and `user_cd` from session; calls `filter.init()`; populates ArrayLists
- **Expression outputs:**
  - Lines 136, 180, 194, 205, 224, 232, 256: `grp_cd` in onload JS, DB-sourced group codes/names in options, mail group customer name, mail list items, `message` — all unescaped
  - Line 224: `<%=vmail_grp_lst.get(i) %>` in radio button value and JS `call_del()` argument — DB values in JS context — unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: `mg` (select), `del` (radio), `mail_id`, `op_code` (hidden), `form_cd` (hidden)
- **CSRF token:** None

---

### 9. `security/frm_form_priority.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `../sess/Expire.jsp` (line 2), `../menu/menu.jsp` (line 236)
- **Beans:** `Databean_security` (request scope), `UtilBean` (page scope)
- **Scriptlets:**
  - Lines 156–212: Reads `message`, `gp_cd`, `user_cd` (session), `form_cd`, `cust_cd` from request; reads access-level from session; calls `filter.init()`; populates form/module ArrayLists
- **Expression outputs:**
  - Lines 259, 288, 326, 336–337, 314, 318: DB-sourced form names, module names, form codes in `exchange()` JS onclick calls — unescaped; `<%=message %>` — request param, unescaped
  - Lines 344–345: `<%=user_cd%>`, `<%=form_cd %>` in hidden inputs — unescaped
- **Forms:** `POST ../servlet/Frm_security` — inputs: `op_code` (hidden), `count` (hidden), `user_cd` (hidden), `form_cd` (hidden), `form_cd1` (hidden), `form_cd2` (hidden), `frm_cd` (hidden, per row)
- **CSRF token:** None

---

### 10. `security/get_form_data.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** None (errorPage set to `../home/ExceptionHandler.jsp`)
- **Beans:** `Databean_security` (request scope)
- **Scriptlets:**
  - Lines 6–33: Reads `q` parameter from request (no auth check); uses it as form code lookup in DB; builds unescaped XML response with form name, path, module code, and description
- **No session/authentication check** present

---

### 11. `security/get_mail_data.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** None
- **Beans:** `Databean_security` (request scope)
- **Scriptlets:**
  - Lines 6–37: Reads `q` parameter (no auth check); uses it to look up mail group list; returns comma-separated mail addresses in XML
- **No session/authentication check** present

---

### 12. `security/get_module_data.jsp`
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** None
- **Beans:** `Databean_security` (request scope)
- **Scriptlets:**
  - Lines 6–34: Reads `q` parameter (no auth check); looks up module name, path, description; returns in XML
- **No session/authentication check** present

---

### 13. `security/output.jsp`
- **Imports:** Many: `java.io.*`, `java.sql.*`, `java.util.*`, `javax.sql.*`, `javax.naming.*`, `org.mindrot.jbcrypt.BCrypt`, `com.torrent.surat.fms6.util.RuntimeConf`
- **Includes:** None
- **Session/auth check:** None
- **Scriptlets (lines 16–161):**
  - Reads request parameters `form_cd`, `cust_cd`, `loc_cd`, `dept_cd` (none are used in SQL — file paths are hardcoded)
  - Opens `D:/reset.csv` from server filesystem (hardcoded absolute path)
  - Iterates over lines from file, using each line (`gmtp_id`) directly in SQL string concatenation — CRITICAL SQL injection
  - Executes multiple SELECT/INSERT/UPDATE queries against `FMS_VEHICLE_MST` and `outgoing` tables using `gmtp_id` from CSV file via string concatenation
  - Uses `prepareStatement()` but defeats its purpose by concatenating `gmtp_id` directly into the query string before passing to `prepareStatement()`
- **Output:** Writes `<h3>Recalibration Done!</h3>`
- **No authentication gate** on this page

---

### 14. `security/threshold_par.jsp`
- **Imports:** Same as output.jsp (identical import block including BCrypt, SQL, IO)
- **Includes:** None
- **Session/auth check:** None
- **Scriptlets (lines 16–165):**
  - Reads `form_cd`, `cust_cd`, `loc_cd`, `dept_cd` from request (not used in queries)
  - Opens `D:/PAR_messages.log` from server filesystem (hardcoded absolute path)
  - Reads lines from log file, iterates `dataList` (always empty per logic) building SQL strings with `gmtp_id` via concatenation
  - Same SQL injection pattern as `output.jsp`
- **No authentication gate**

---

### 15. `pages/login.jsp`
- **Imports:** `com.torrent.surat.fms6.dao.MessageDao`, `LindeConfig`, `java.util.Properties`, `java.util.ArrayList`, `java.net.*`, `org.owasp.esapi.ESAPI`, `org.owasp.esapi.Encoder`
- **Includes:** None
- **Scriptlets:**
  - Lines 77–142: Reads `val`, `message`, `validity`, `sessmsg`, `comb` from request — all encoded via ESAPI `encodeForHTML()`. Reads cookie `login` and `password`. On `val=1` or `val=logout`, calls `session.invalidate()`.
  - Lines 148–155: Creates `MessageDao`, fetches status message from DB
- **Expression outputs:**
  - Line 12: `<%=LindeConfig.systemName %>` — static
  - Line 403: `<%=msg %>` — DB-sourced status message, **unescaped**
  - Lines 409, 641: `<%=message1%>` and `var value = '<%=value%>'` — both ESAPI-encoded at parameter read time; however `value` is placed into a JavaScript string variable on line 641 — the HTML encoding does not prevent JS context injection for characters like `'` that ESAPI `encodeForHTML` does not encode as JS-safe
- **Forms:** `POST ../servlet/Frm_security` — inputs: `login`, `password`, `op_code` (hidden=`login`), `tc` (hidden=`false`), `release` (hidden=`false`)
- **CSRF token:** None (login form — lower risk)
- **Session invalidation:** `session.invalidate()` is called on logout (`val=1` or `val=logout`) but **not** on new login (no session regeneration post-login)
- **Cookies:** Reads `login` and `password` cookies; password cookie is read but not used visibly in the JSP

---

### 16. `pages/changepass.jsp`
- **Imports:** `com.torrent.surat.fms6.bean.CustomerBean`, `com.torrent.surat.fms6.util.UtilBean`
- **Includes:** None (fragment, included by other pages)
- **Scriptlets:**
  - Lines 4–9: Reads `user_cd`, `force_change`, `lastUpdate`, `reset_pass` from request parameters — all unescaped; fetches `CustomerBean` by `user_cd`
- **Expression outputs:**
  - Line 17: `<%=lastUpdate %>` — request parameter, unescaped, placed in HTML
  - Line 56: `var pSetting = "<%=currCustomer.isPasswordPolicy()%>"` — DB/config value in JS string
  - Line 58: `<%=currCustomer.getId()%>` — DB value in JS expression (numeric comparison, lower XSS risk)
  - Line 39: `<%=reset_pass%>` — request parameter in hidden input value, unescaped
  - Line 40: `<%=user_cd%>` — request parameter in hidden input, unescaped
- **Forms:** `POST ../servlet/Frm_customer` (ajax_form class) — inputs: `cpass`, `npass`, `rnpass`, `method` (hidden=`change_password`), `reset_pass` (hidden), `user_cd` (hidden)
- **CSRF token:** None
- **Note:** When `reset_pass` equals `"false"` (its default), the current password field is hidden/omitted — the form submits only new password without verifying old password server-side in this JSP (relies on servlet)

---

### 17. `pages/resetpass.jsp`
- **Imports:** `com.torrent.surat.fms6.bean.CustomerBean`, `com.torrent.surat.fms6.util.UtilBean`, `LindeConfig`
- **Includes:** None (fragment)
- **Forms:** `POST ../servlet/Frm_security` — inputs: `username`, `op_code` (hidden=`resetpassword`)
- **No XSS expression outputs**
- **CSRF token:** None

---

### 18. `pages/checker.jsp`
- **Imports:** `java.util.Properties`, `java.util.ArrayList`, `java.net.*`
- **Includes:** None
- **Beans:** `Databean_security` (request scope, id=`loginalerter`)
- **Scriptlets (lines 7–48):**
  - Reads `user_cd` and `message` from request parameters — unescaped
  - Calls `loginalerter.init()` to get access-level/customer/site/dept
  - **Sets session attributes** (`user_cd`, `access_level`, `access_cust`, `access_site`, `access_dept`, `user_fnm`, `user_lnm`) directly from bean output using `user_cd` from the request parameter — no session ID regeneration
  - Builds redirect URL: `link = "index.jsp?message="+message` (unencoded `message` in URL) or `link = "admin.jsp?message="+message`
  - Performs HTTP redirect via `response.setHeader("Location", link)`
- **Critical issue:** `user_cd` is taken from the **request parameter**, not from a securely validated session. If `checker.jsp` is directly accessible without prior authentication, an attacker can pass any `user_cd` to establish an authenticated session.

---

### 19. `sess/Expire.jsp`
- **Includes:** Included via `<%@ include %>` in all `security/frm_*.jsp` pages
- **Logic:**
  - Line 10: `if (request.getSession(false) == null)` — forwards to login
  - Line 20: `if (request.getSession(false).getAttribute("user_cd") == null)` — forwards to login
- **Gap:** Only checks that `user_cd` attribute is non-null in session. Does not verify that the session is valid/authenticated beyond attribute presence.

---

### 20. `index.jsp` (root)
- No imports, no scriptlets
- Meta-refresh redirect to `pages/login.jsp`
- No security concerns

---

### 21. `pages/index.jsp`
- **Imports:** `java.util.Properties`, `java.util.ArrayList`, `java.net.*`, `java.io.File`
- **Includes:** `../sess/Expire.jsp` (line 5), `../layout/header.jsp` (line 6), `../layout/footer.jsp` (end)
- **Scriptlets:**
  - Lines 7–16: Reads `user_cd` and `access_level` from session
  - Lines 32–53: Reads `mnm` and `sub` request parameters — constructs a server-side filesystem path as `/pages/admin/<mnm>.jsp` or `/pages/admin/<sub>.jsp`; checks if file exists via `File.exists()`; then includes the page using `<jsp:include page="<%= filepath %>" />`
- **CRITICAL:** `mnm` and `sub` are user-controlled request parameters used to build a JSP include path without any sanitisation or allowlisting — this is a path traversal / arbitrary file inclusion vulnerability

---

## STEP 4 & 5 — SECURITY FINDINGS

---

### A10-1
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\index.jsp`
**Lines:** 34–49
**Severity:** CRITICAL
**Category:** Arbitrary File Inclusion / Path Traversal

**Description:**
The `mnm` and `sub` request parameters are used without sanitisation or allowlisting to construct a JSP include path that is then directly executed via `<jsp:include>`. An attacker can supply `../` sequences or navigate to other JSP files on the server filesystem.

**Evidence:**
```jsp
String mnm = request.getParameter("mnm")==null? "Home" : request.getParameter("mnm");
String sub = request.getParameter("sub")==null? "" : request.getParameter("sub");
String filepath = "";
if( sub.isEmpty() ) {
  filepath = "/pages/admin/"+mnm+".jsp";
} else {
  filepath = "/pages/admin/"+sub+".jsp";
}
String realpath = servletContext.getRealPath(filepath);
File f=new File(realpath);
if (f.exists()) {
%>
  <jsp:include page="<%= filepath %>" flush="true" />
```

**Recommendation:**
Validate `mnm` and `sub` against an explicit allowlist of known page names (e.g., regex `^[a-zA-Z0-9_-]+$` with maximum length). Never construct include paths from user-controlled input. Consider routing through a servlet dispatch map.

---

### A10-2
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\output.jsp`
**Lines:** 92–94, 101, 109, 114, 122–123
**Severity:** CRITICAL
**Category:** SQL Injection

**Description:**
The file reads lines from a CSV file on disk (`D:/reset.csv`) and concatenates them directly into SQL query strings passed to `prepareStatement()`. Although `PreparedStatement` is used, the query string is assembled by concatenation before being passed to `prepareStatement()`, completely defeating parameterised query protections. If the CSV file can be influenced by an attacker (e.g., through another vulnerability), arbitrary SQL can be executed. Additionally, `output.jsp` has no authentication check, meaning it can be invoked by any unauthenticated party to trigger database operations.

**Evidence:**
```java
String queryString = "select \"CALIBRATED_STD_DEV\" + \"CALIBRATED_SETTING\" from \"FMS_VEHICLE_MST\" "
        + " where \"VEHICLE_ID\" = '"+gmtp_id+"'";
ps = dbcon.prepareStatement(queryString);

queryString="update \"FMS_VEHICLE_MST\" set \"FSSXMULTI\" = '10' " + " where \"VEHICLE_ID\" = '"+gmtp_id+"'";
ps = dbcon.prepareStatement(queryString);

queryString="Insert into outgoing (outgoing_id,destination, message, timestamp) "
    + "values (nextval(('seq_outgoing'::text)::regclass),'"+gmtp_id+"','"+msg+"',current_timestamp)";
```

**Recommendation:**
Use proper parameterised queries with `?` placeholders. The file should also be removed from production (it appears to be a one-off administrative/maintenance script) or at minimum protected behind admin authentication and access controls.

---

### A10-3
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\threshold_par.jsp`
**Lines:** 97, 106, 114, 122–123, 127
**Severity:** CRITICAL
**Category:** SQL Injection

**Description:**
Same SQL injection pattern as `output.jsp`. Lines from `D:/PAR_messages.log` are concatenated into SQL strings. The page has no authentication gate.

**Evidence:**
```java
queryString="update \"FMS_VEHICLE_MST\" set \"FSSXMULTI\" = '10' " + " where \"VEHICLE_ID\" = '"+gmtp_id+"'";
ps = dbcon.prepareStatement(queryString);

queryString="Insert into outgoing (outgoing_id,destination, message, timestamp) "
    + "values (nextval(('seq_outgoing'::text)::regclass),'"+gmtp_id+"','"+msg+"','"+tm+"',current_timestamp)";
```

**Recommendation:**
Same as A10-2. Remove or gate these operational scripts. Use parameterised queries exclusively.

---

### A10-4
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\output.jsp`, `C:\Projects\cig-audit\repos\fleetfocus\security\threshold_par.jsp`
**Lines:** output.jsp:16–161; threshold_par.jsp:16–165
**Severity:** CRITICAL
**Category:** Missing Authentication — Unauthenticated Access to Sensitive Operations

**Description:**
Both `output.jsp` and `threshold_par.jsp` perform destructive and sensitive database operations (UPDATE, INSERT on vehicle and messaging tables) with no session check, no login requirement, and no CSRF protection. Any unauthenticated HTTP request to these pages triggers the operations.

**Evidence:**
```jsp
<%
String url = "";
String form_cd = request.getParameter("form_cd") == null ? "" : request.getParameter("form_cd");
// ... directly executes database modifications with no session.getAttribute("user_cd") check
```

**Recommendation:**
These pages must either be removed from the web-accessible directory entirely (they appear to be development/maintenance scripts) or protected with strong authentication and authorisation checks matching the rest of the application.

---

### A10-5
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\checker.jsp`
**Lines:** 9, 24–30
**Severity:** CRITICAL
**Category:** Authentication Bypass / Session Fixation

**Description:**
`checker.jsp` accepts `user_cd` from the request parameter and uses it to look up access rights and then directly set session attributes — including `user_cd`, `access_level`, `access_cust`, `access_site`, `access_dept`. If this page is accessible without prior authenticated context (or if it is callable at any time), an attacker who knows or guesses a valid `user_cd` value can establish a fully authenticated session for any user without knowing their password. Furthermore, the existing session is not invalidated and regenerated before setting new attributes — a classic session fixation vulnerability.

**Evidence:**
```jsp
String user_cd= request.getParameter("user_cd")==null?"":request.getParameter("user_cd");
// ...
session.setAttribute("user_cd",user_cd);
session.setAttribute("access_level",access_level);
session.setAttribute("access_cust",access_cust);
// ...
request.getSession(true);
response.setStatus(response.SC_MOVED_TEMPORARILY);
response.setHeader("Location", link);
```

**Recommendation:**
`checker.jsp` must not accept `user_cd` from request parameters and must not write security-sensitive session attributes based on externally supplied input. The servlet that processes login should set session attributes after validating credentials, then call `session.invalidate()` and `request.getSession(true)` to regenerate the session ID before committing attributes.

---

### A10-6
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\login.jsp`
**Line:** 641
**Severity:** HIGH
**Category:** XSS — JavaScript Context Injection

**Description:**
The `value` parameter is HTML-encoded via ESAPI `encodeForHTML()` at line 80, but is then embedded directly into a JavaScript string literal on line 641:

```jsp
var value = '<%=value%>'
```

ESAPI's `encodeForHTML()` encodes for HTML attribute/body context (e.g., `<`, `>`, `&`, `"`) but does NOT encode single quotes (`'`) or backslashes, which are the delimiters and escape characters in this JavaScript string context. An attacker supplying `value=';alert(1)//` would not be HTML-encoded (no `<`, `>`, or `&` involved) and would break out of the JavaScript string, enabling script injection.

**Evidence:**
```java
String value = request.getParameter("val") == null ? "0" : request.getParameter("val");
value = encoder.encodeForHTML(value);  // Line 80 — wrong encoding context
// ...
var value = '<%=value%>'   // Line 641 — JavaScript string context, not JS-encoded
```

**Recommendation:**
Use `encoder.encodeForJavaScript(value)` (ESAPI) when embedding values into JavaScript string literals, not `encodeForHTML`. Alternatively, use `JSON.stringify()` on the server side to produce a properly escaped JavaScript value.

---

### A10-7
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\login.jsp`
**Lines:** 403
**Severity:** HIGH
**Category:** XSS — Unescaped Database Value in HTML

**Description:**
The status message fetched from the database via `MessageDao` is output directly without any escaping:

```jsp
<%=msg %>
```

If an attacker or privileged user can insert HTML/script into the database status message, it will be rendered as markup on the login page — a stored XSS vulnerability reachable by all users, including unauthenticated ones.

**Evidence:**
```jsp
String msg = msgDao.getMsg();
// ...
<%=msg %>
```

**Recommendation:**
Escape `msg` with ESAPI `encoder.encodeForHTML(msg)` before rendering, or use JSTL `<c:out value="${msg}" />`.

---

### A10-8
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\auto_change_pass.jsp`
**Line:** 154
**Severity:** HIGH
**Category:** XSS — Reflected Unescaped Request Parameter

**Description:**
The `message` request parameter is reflected directly into the HTML page without any escaping:

```jsp
<%=message %>
```

An attacker can craft a URL with `message=<script>alert(1)</script>` and trick a user (e.g., via phishing) into visiting it, causing script execution in their browser. This file does not have `Expire.jsp` protection (no session check at top of file), making this exploitable pre-authentication in theory.

**Evidence:**
```java
String message=request.getParameter("message")==null?"":request.getParameter("message");
// ...
<%=message %>   // Line 154
```

**Recommendation:**
HTML-encode `message` before rendering. Use ESAPI `encoder.encodeForHTML(message)` or JSTL `<c:out>`.

---

### A10-9
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\frm_change_pass.jsp`
**Line:** 157
**Severity:** HIGH
**Category:** XSS — Reflected Unescaped Request Parameter

**Description:**
Same pattern as A10-8. `message` parameter is reflected without escaping into the password change page, which is accessible to authenticated users.

**Evidence:**
```java
String message=request.getParameter("message")==null?"":request.getParameter("message");
// ...
&nbsp; <%=message %>   // Line 157
```

**Recommendation:**
HTML-encode `message` before output.

---

### A10-10
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\frm_access_rights.jsp`
**Lines:** 277, 444–445
**Severity:** HIGH
**Category:** XSS — Reflected Parameters and DB Values in JS and HTML

**Description:**
Two issues in this file:

1. Line 277: `cust_cd` and `gp_cd` (from request parameters) are embedded unescaped into the `onLoad` JavaScript attribute:
   ```html
   <body onLoad="set('<%=cust_cd %>','<%=gp_cd %>');">
   ```
   An attacker can inject arbitrary JavaScript by supplying `cust_cd=');alert(1);//`.

2. Line 444–445: `message` (from request parameter) is reflected unescaped into HTML:
   ```jsp
   &nbsp; <%=message %>
   ```

**Evidence:**
```jsp
<body onLoad="set('<%=cust_cd %>','<%=gp_cd %>');">  // Line 277
// ...
&nbsp; <%=message %>   // Line 444-445
```

**Recommendation:**
For JS context, use `encodeForJavaScript()`. For HTML context, use `encodeForHTML()` or JSTL `<c:out>`.

---

### A10-11
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\frm_add_mail_group.jsp`
**Line:** 129
**Severity:** HIGH
**Category:** XSS — Database Values in JavaScript `onclick` Attribute

**Description:**
DB-sourced group codes and names are embedded unescaped into a JavaScript `onclick` attribute:
```html
<a href="#" onClick="set_editvalues('<%=vgrp_cd.get(i) %>','<%=vgrp_nm.get(i) %>');">
```
If a group name contains a single quote or HTML/JS metacharacters, it breaks out of the JS context. Since group names are entered by administrators, this is a stored XSS vector.

**Evidence:**
```jsp
<a href="#" onClick="set_editvalues('<%=vgrp_cd.get(i) %>','<%=vgrp_nm.get(i) %>');"><%=vgrp_cd.get(i) %></a>
// Line 129
```

**Recommendation:**
Use `encodeForJavaScript()` for values embedded in JS string arguments. Use `encodeForHTML()` for values in HTML text nodes.

---

### A10-12
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\frm_add_mail_group_pop.jsp`
**Line:** 122
**Severity:** HIGH
**Category:** XSS — Database Values in JavaScript `onclick` Attribute

**Description:**
Same stored XSS pattern as A10-11. DB-sourced group name, code, and customer code are unescaped in a JS onclick handler.

**Evidence:**
```jsp
<a href="#" onClick="set_editvalues('<%=vgrp_cd.get(i) %>','<%=vgrp_nm.get(i) %>','<%=mail_grp_cust.get(i)%>');"><%=vgrp_nm.get(i) %></a>
// Line 122
```

**Recommendation:**
Apply `encodeForJavaScript()` to all values embedded in JavaScript string contexts.

---

### A10-13
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\frm_edit_mail_list.jsp`
**Line:** 224
**Severity:** HIGH
**Category:** XSS — Database Values in JavaScript Function Call

**Description:**
Mail addresses from the database are embedded directly into a JavaScript `onClick` handler:
```html
<input type="radio" ... onClick="call_del('<%=vmail_grp_lst.get(i) %>');"/>
```
An email address containing a single quote or semicolon (both syntactically valid in email addresses) would break out of the JS string, enabling stored XSS.

**Evidence:**
```jsp
<input type = "radio" name="del" value="<%=vmail_grp_lst.get(i) %>"
    onClick="call_del('<%=vmail_grp_lst.get(i) %>');"/>
// Line 224
```

**Recommendation:**
Apply `encodeForJavaScript()` to values used inside JS string arguments. Apply `encodeForHTML()` to HTML attribute values.

---

### A10-14
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\frm_form_priority.jsp`
**Lines:** 314, 318
**Severity:** HIGH
**Category:** XSS — Database Values in JavaScript `onclick` Attribute

**Description:**
Form codes from the database are embedded unescaped into JavaScript `onclick` event handlers:
```html
<a href="#" onclick="exchange('<%=vform_cd.get(i-1) %>','<%=vform_cd.get(i) %>')">
```
While form codes are likely numeric in practice, there is no enforcement, and a poisoned form code with JS metacharacters would result in stored XSS.

**Evidence:**
```jsp
<a href="#" onclick="exchange('<%=vform_cd.get(i-1) %>','<%=vform_cd.get(i) %>')">  // Line 314
<a href="#" onclick="exchange('<%=vform_cd.get(i) %>','<%=vform_cd.get(i+1) %>')">  // Line 318
```

**Recommendation:**
Apply `encodeForJavaScript()` or validate that form codes are strictly numeric before inclusion.

---

### A10-15
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\changepass.jsp`
**Line:** 17
**Severity:** HIGH
**Category:** XSS — Reflected Request Parameter in HTML

**Description:**
The `lastUpdate` request parameter is rendered unescaped into HTML:
```jsp
<i>(Last Update: <%=lastUpdate %>)</i>
```
This parameter is passed when the user is prompted to update an expiring password. An attacker who can control the URL can inject HTML/script here.

**Evidence:**
```java
String lastUpdate = request.getParameter("lastUpdate")==null ? "" : request.getParameter("lastUpdate");
// ...
<i>(Last Update: <%=lastUpdate %>)</i>  // Line 17
```

**Recommendation:**
HTML-encode `lastUpdate` before rendering. Also validate that it conforms to expected date format server-side.

---

### A10-16
**File:** All `security/frm_*.jsp` files and `pages/changepass.jsp`
**Lines:** Multiple (see each file's form section)
**Severity:** HIGH
**Category:** CSRF — Missing Anti-CSRF Tokens on All State-Changing Forms

**Description:**
Not a single form across the entire audited set of security-related JSPs contains a CSRF token. Every form that performs a state-changing POST operation — including password change, access rights modification, mail group management, form/module administration, and form priority reordering — is vulnerable to Cross-Site Request Forgery. An attacker who tricks an authenticated administrator into visiting a malicious page can submit any of these forms on their behalf.

Affected files and operations:
- `frm_change_pass.jsp` — password change (`op_code=pass_chg`)
- `auto_change_pass.jsp` — forced password change (`op_code=pass_chg`)
- `frm_access_rights.jsp` — access rights modification
- `frm_add_form.jsp` — form registration
- `frm_add_mail_group.jsp` — mail group creation/editing
- `frm_add_mail_group_pop.jsp` — mail group creation popup
- `frm_add_module.jsp` — module creation/editing
- `frm_edit_mail_list.jsp` — mail list management and deletion
- `frm_form_priority.jsp` — form priority reordering
- `pages/changepass.jsp` — new-skin password change
- `pages/resetpass.jsp` — password reset request

**Evidence (representative):**
```html
<!-- frm_change_pass.jsp, line 112 -->
<form method="post" action="../servlet/Frm_security">
<!-- no <input type="hidden" name="csrf_token" ...> -->
<input type="hidden" name="op_code" value="pass_chg">
<input type="hidden" name="user_cd" value="<%=user_cd%>">
```

**Recommendation:**
Implement synchroniser token pattern: generate a cryptographically random token per session, store it in the session, include it as a hidden field in every form, and validate it in the servlet before processing any state-changing request. Spring Security CSRF protection or a custom servlet filter is the recommended implementation approach.

---

### A10-17
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\get_form_data.jsp`, `C:\Projects\cig-audit\repos\fleetfocus\security\get_mail_data.jsp`, `C:\Projects\cig-audit\repos\fleetfocus\security\get_module_data.jsp`
**Lines:** All (no session check present)
**Severity:** HIGH
**Category:** Missing Authentication — Unauthenticated Data Enumeration Endpoints

**Description:**
All three AJAX data endpoints have no session check and no authentication requirement. Any unauthenticated user who can reach the server can directly query these endpoints to enumerate:
- `get_form_data.jsp?q=<form_id>` — form names, paths, module codes, descriptions
- `get_mail_data.jsp?q=<group_id>` — email addresses for every mail group
- `get_module_data.jsp?q=<module_id>` — module names, icon paths, descriptions

This allows complete enumeration of the application's structural configuration and all registered email addresses without authentication.

**Evidence:**
```jsp
// get_form_data.jsp, lines 6-11
response.setContentType("text/xml");
String form_cd=request.getParameter("q") ;
String op_code="get_form_data";
filter.setSet_frm_cd(form_cd);
filter.setSet_op_code(op_code);
filter.init();
// No session check
```

**Recommendation:**
Add session authentication check (via `Expire.jsp` include or equivalent) to all three endpoints before processing requests.

---

### A10-18
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\login.jsp`
**Lines:** 85–95
**Severity:** MEDIUM
**Category:** Session Fixation — No Session Regeneration on Login

**Description:**
The login page calls `session.invalidate()` on logout but does not regenerate the session ID upon new successful authentication. The `checker.jsp` file (which sets session attributes after login) calls `request.getSession(true)` but only after potentially reusing the existing session. If an attacker can fix a session ID before login (e.g., via network-level attack or shared session store), they retain access after the victim authenticates.

**Evidence:**
```jsp
// login.jsp lines 85-95 — invalidation on logout only
if (value.equalsIgnoreCase("1")) {
    session.invalidate();
}
// checker.jsp line 44 — session reuse, not regeneration
request.getSession(true);   // does not invalidate old session first
```

**Recommendation:**
In the login processing servlet (or at the top of `checker.jsp`), call `session.invalidate()` to destroy the existing session and then `request.getSession(true)` to create a fresh session before setting authentication attributes.

---

### A10-19
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\login.jsp`
**Lines:** 101–123
**Severity:** MEDIUM
**Category:** Sensitive Data in Cookie — Password Stored in Cookie

**Description:**
The login page reads a cookie named `password` from the request. Storing a password (even as a hash) in a browser cookie is a significant security risk. Cookies persist on the client, are transmitted with every request, may be logged by proxies, and can be stolen via XSS or network interception (if not on HTTPS-only cookies with proper flags).

**Evidence:**
```java
Cookie cks[] = request.getCookies();
// ...
if (cks[i].getName().equalsIgnoreCase("password")) {
    password = cks[i].getValue();
}
```

**Recommendation:**
Remove the password cookie mechanism entirely. If "remember me" functionality is needed, use a cryptographically random, single-use token stored in the database, not the password itself.

---

### A10-20
**File:** `C:\Projects\cig-audit\repos\fleetfocus\security\output.jsp`, `C:\Projects\cig-audit\repos\fleetfocus\security\threshold_par.jsp`
**Lines:** output.jsp:46; threshold_par.jsp:46
**Severity:** MEDIUM
**Category:** Hardcoded Absolute Filesystem Path — Server Path Disclosure / Operational Risk

**Description:**
Both files reference hardcoded absolute server filesystem paths (`D:/reset.csv` and `D:/PAR_messages.log`). These paths expose server filesystem structure information in source code and create operational dependencies on specific file locations. These appear to be development/maintenance scripts left in the production codebase.

**Evidence:**
```java
// output.jsp line 46
String fileName = "D:/reset.csv";

// threshold_par.jsp line 46
String fileName = "D:/PAR_messages.log";
```

**Recommendation:**
Remove these scripts from the deployed application. If batch operations are required, implement them as properly authenticated, audited administrative functions — not as web-accessible JSPs with hardcoded paths.

---

### A10-21
**File:** `C:\Projects\cig-audit\repos\fleetfocus\sess\Expire.jsp`
**Lines:** 20
**Severity:** MEDIUM
**Category:** NullPointerException Risk / Weak Session Guard

**Description:**
`Expire.jsp` first checks `if (request.getSession(false) == null)` and forwards to login if true. However, the second check on line 20:
```java
if (request.getSession(false).getAttribute("user_cd") == null)
```
is executed unconditionally even if the first `<jsp:forward>` was issued — in JSP, `<jsp:forward>` does not terminate execution of the current scriptlet block. If the session is null when line 20 is reached (after the forward in the first block), this will throw a NullPointerException. While in practice the forward likely terminates response processing, this constitutes a logic defect that could under some container configurations allow fall-through.

Additionally, the guard only checks for presence of `user_cd` attribute, not for a valid/verified session-bound authentication flag. Any code that sets `user_cd` in the session (such as the `checker.jsp` vulnerability described in A10-5) satisfies this check.

**Evidence:**
```java
if (request.getSession(false) == null) {
    %> <jsp:forward page="../pages/login.jsp"> ... </jsp:forward> <%
}
// Execution may continue here after forward in some containers:
if (request.getSession(false).getAttribute("user_cd") == null) {
```

**Recommendation:**
Add `return;` after the `<jsp:forward>` block, or restructure using `else if`. Also supplement the session check with an explicit authentication flag (e.g., `session.getAttribute("authenticated")`) that is only set after successful credential verification.

---

### A10-22
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\changepass.jsp`
**Lines:** 56–74
**Severity:** MEDIUM
**Category:** Client-Side Only Password Policy Enforcement

**Description:**
Password strength and policy requirements are enforced exclusively via JavaScript on the client side. The JavaScript `CheckPassword()` function and minimum length checks can be trivially bypassed by submitting the form directly (e.g., via `curl` or browser DevTools). The server-side servlet must independently enforce password complexity requirements.

**Evidence:**
```javascript
function saveForm(){
    var pSetting = "<%=currCustomer.isPasswordPolicy()%>";
    // ...
    if ( CheckPassword($('#pword').val()) == false ) {
        swal("error","Password must contain minimum of 10 characters...");
    } else if($('.strength_meter').text() == "Weak" ){
        swal("error"," Password is not strong enough.","error");
    } else {
        $('.ajax_form').submit();  // Only submitted if client-side checks pass
    }
```

**Recommendation:**
Enforce all password policy rules in the server-side servlet that processes the password change request, independent of client-side validation. Client-side validation should be treated as UX only.

---

### A10-23
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\checker.jsp`
**Lines:** 32–41
**Severity:** MEDIUM
**Category:** Open Redirect

**Description:**
The `message` parameter from the request is concatenated unescaped into redirect URLs and then used in `response.setHeader("Location", link)`. While the base URL is constructed server-side, the `message` parameter value appears in the URL query string without encoding, and the overall redirect target is assembled from user input. Depending on server/proxy handling, crafted `message` values could potentially manipulate the redirect behaviour.

**Evidence:**
```java
String message= request.getParameter("message")==null?"":request.getParameter("message");
// ...
String link = "index.jsp?message="+message;
// ...
response.setHeader("Location", link);
```

**Recommendation:**
URL-encode the `message` parameter value before appending it to the redirect URL using `URLEncoder.encode(message, "UTF-8")`. Additionally, validate that redirect targets remain within the expected application domain.

---

## SUMMARY TABLE

| ID     | Severity | Category | File(s) |
|--------|----------|----------|---------|
| A10-1  | CRITICAL | Arbitrary File Inclusion / Path Traversal | pages/index.jsp |
| A10-2  | CRITICAL | SQL Injection | security/output.jsp |
| A10-3  | CRITICAL | SQL Injection | security/threshold_par.jsp |
| A10-4  | CRITICAL | Missing Authentication | security/output.jsp, security/threshold_par.jsp |
| A10-5  | CRITICAL | Authentication Bypass / Session Fixation | pages/checker.jsp |
| A10-6  | HIGH | XSS — JS Context | pages/login.jsp |
| A10-7  | HIGH | XSS — Stored DB Value | pages/login.jsp |
| A10-8  | HIGH | XSS — Reflected | security/auto_change_pass.jsp |
| A10-9  | HIGH | XSS — Reflected | security/frm_change_pass.jsp |
| A10-10 | HIGH | XSS — Reflected + JS Context | security/frm_access_rights.jsp |
| A10-11 | HIGH | XSS — Stored, JS onclick | security/frm_add_mail_group.jsp |
| A10-12 | HIGH | XSS — Stored, JS onclick | security/frm_add_mail_group_pop.jsp |
| A10-13 | HIGH | XSS — Stored, JS onclick | security/frm_edit_mail_list.jsp |
| A10-14 | HIGH | XSS — Stored, JS onclick | security/frm_form_priority.jsp |
| A10-15 | HIGH | XSS — Reflected | pages/changepass.jsp |
| A10-16 | HIGH | CSRF — All State-Changing Forms | All security/frm_*.jsp + changepass/resetpass |
| A10-17 | HIGH | Missing Authentication — Data Enumeration | security/get_form_data.jsp, get_mail_data.jsp, get_module_data.jsp |
| A10-18 | MEDIUM | Session Fixation | pages/login.jsp, pages/checker.jsp |
| A10-19 | MEDIUM | Password in Cookie | pages/login.jsp |
| A10-20 | MEDIUM | Hardcoded Paths / Operational Script Exposure | security/output.jsp, security/threshold_par.jsp |
| A10-21 | MEDIUM | Weak Session Guard / NPE Risk | sess/Expire.jsp |
| A10-22 | MEDIUM | Client-Side Only Password Policy | pages/changepass.jsp |
| A10-23 | MEDIUM | Open Redirect | pages/checker.jsp |

**Total findings: 23**
- CRITICAL: 5
- HIGH: 12
- MEDIUM: 6
