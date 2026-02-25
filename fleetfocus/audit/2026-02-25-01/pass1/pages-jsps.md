# FleetFocus JSP Pages Security Audit
**Audit ID:** A15
**Date:** 2026-02-25
**Run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Agent:** A15

---

## STEP 3 — READING EVIDENCE (File Inventory)

### C:\Projects\cig-audit\repos\fleetfocus\sess\Expire.jsp
- **Imports:** `java.util.Date`, `java.text.DateFormat`, `java.text.SimpleDateFormat`, `org.apache.logging.log4j.Logger`
- **Scriptlet (lines 3–29):** Checks `request.getSession(false)` and `session.getAttribute("user_cd")`. If either is null, forwards to `../pages/login.jsp`. This is the session guard included across all protected pages.
- **Expressions:** None rendered to HTML.
- **Includes:** None.
- **Forms:** None.

### C:\Projects\cig-audit\repos\fleetfocus\pages\login.jsp
- **Imports:** `MessageDao`, `LindeConfig`, `java.util.Properties`, `java.util.ArrayList`, `java.net.*`, `org.owasp.esapi.ESAPI`, `org.owasp.esapi.Encoder`
- **Scriptlets:**
  - Lines 77–141: Reads `val`, `message`, `validity`, `sessmsg`, `comb` from request parameters; encodes each with `encoder.encodeForHTML()`. Invalidates session if `val=1` or `val=logout`. Reads `login` and `password` values from cookies.
  - Lines 148–155: `MessageDao` query for system notification message.
  - Lines 384–399: Branching on `LindeConfig.siteName` for logo rendering.
  - Lines 401–405: Renders `msg` from DB directly without HTML encoding (see A15-1).
  - Line 641: Outputs `value` (request parameter, ESAPI-encoded) into a JavaScript string literal (see A15-2).
- **Expressions:**
  - Line 12: `<%=LindeConfig.systemName %>` — static config value, not user-controlled.
  - Line 25: `<%=LindeConfig.siteCss %>` — static config value.
  - Line 403: `<%=msg %>` — DB-sourced notification message, NOT HTML-encoded before rendering (see A15-1).
  - Line 409: `<%=message1%>` — ESAPI-encoded request parameter. Safe.
  - Line 641: `var value = '<%=value%>'` — ESAPI HTML-encoded but placed inside a JS string literal; HTML encoding is insufficient for JS context (see A15-2).
- **Includes:** None (standalone page).
- **Forms:**
  - Line 406: `<form method="post" action="../servlet/Frm_security">` — login form. No CSRF token (login forms are conventionally exempt but noted).

### C:\Projects\cig-audit\repos\fleetfocus\pages\manage_form.jsp
- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Scriptlet (lines 7–30):** Reads `module_cd` and `type` request parameters. Calls `filter.query("manage_modules")` to retrieve all module/form definitions from DB.
- **Session guard:** Line 1 `<%@ include file="../sess/Expire.jsp" %>` — session is checked. However, there is **no role/admin-level check** beyond session existence (see A15-3).
- **Expressions:**
  - Line 67: `<%=Form_Cd.get(x).toString()%>` in `data-form_cd` attribute — DB-sourced, unescaped (see A15-4).
  - Line 67: `<legend>Form CD: <%=Form_Cd.get(x).toString()%>` — DB value, unescaped in HTML.
  - Line 68: `value="<%=Form_Name.get(x).toString()%>"` — DB value in form field, unescaped (see A15-4).
  - Line 69: `value="<%=(Form_Desc.get(x).toString()...%>"` — DB value, unescaped.
  - Line 70: `value="<%=(Form_Path.get(x).toString()...%>"` — DB value, unescaped.
  - Line 71: `value="<%=(Form_Priority.get(x).toString()...%>"` — DB value, unescaped.
  - Line 89: `href="../pages/manage_form.jsp?module_cd=<%=Module__Cd%>"` — request parameter, unescaped in URL/HTML context.
  - Line 103: `<option ... value="<%=Module_Cd.get(i).toString()%>"><%=Module_Name.get(i).toString()%>` — DB values, unescaped.
  - Line 107: `href="../pages/manage_form.jsp?module_cd=<%=Module__Cd%>&amp;type=new"` — request parameter in href, unescaped.
- **Includes:** `../sess/Expire.jsp` (line 1).
- **Forms:**
  - Line 63: `<form method="post" action="../servlet/Frm_Customer">` (update_forms) — no CSRF token (see A15-5).
  - Line 79: `<form method="post" action="../servlet/Frm_Customer">` (new_form) — no CSRF token (see A15-5).
  - Line 98: `<form method="get">` — module selector, no CSRF token.

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin.jsp
- **Imports:** `MessageDao`, `java.util.Properties`, `java.util.ArrayList`, `java.net.*`, `java.io.File`
- **Scriptlets:**
  - Lines 16–43: Reads session attributes `user_cd`, `access_level`, `access_cust`, `user_cd`. Reads `form_cd`, `module_cd`, `sub`, `mnm` from request parameters. Constructs `filepath` as `/pages/admin/<mnm>.jsp` or `/pages/admin/<sub>.jsp` — **no sanitisation of `mnm` or `sub`** for path traversal (see A15-6).
  - Lines 117–152: Constructs filepath from user-controlled `mnm`/`sub` parameters, checks file existence via `servletContext.getRealPath()`, then does `<jsp:include page="<%= filepath %>">`. Permission check only applied when `form__cd` is not null (see A15-7).
  - Lines 158–172: Reads `message` request parameter, emits it raw into a JavaScript `swal()` call without encoding (see A15-8).
- **Expressions:**
  - Line 55: `var FORM__CD = "<%=form__cd%>";` — request parameter injected into JS, no JS-safe encoding (see A15-8).
  - Line 145: `<jsp:include page="<%= filepath %>" flush="true" />` — filepath derived from unvalidated `mnm`/`sub` parameters.
- **Includes:** `../sess/Expire.jsp` (line 6), `../layout/header.jsp` (line 7), `../layout/footer.jsp` (line 175).
- **Forms:** None directly in admin.jsp (forms are in included sub-pages).

### C:\Projects\cig-audit\repos\fleetfocus\layout\header.jsp
- **Imports:** `com.torrent.surat.fms6.util.LindeConfig`
- **Scriptlet (lines 3–4, 41–48):** Reads `user_fnm` and `user_lnm` from session. Reads `access_level` from session for menu rendering logic.
- **Expressions:**
  - Line 14: `<%=LindeConfig.systemName %>` — static config.
  - Line 169: `<%=fnm+" "+lnm %>` — session-stored first/last name rendered without HTML encoding in top menu (see A15-9).
  - Line 91: `<%=request.getSession(false).getAttribute("user_cd")%>` — rendered into Google Analytics `ga('set', 'userId', ...)` in footer (see A15-10, informational).
- **Includes:** None (is itself an include target).
- **Forms:** None.

### C:\Projects\cig-audit\repos\fleetfocus\layout\footer.jsp
- **Imports:** `com.torrent.surat.fms6.util.LindeConfig`
- **Scriptlet (lines 82–96):** Conditional Google Analytics block for AU site.
- **Expressions:**
  - Line 91: `<%=request.getSession(false).getAttribute("user_cd")%>` — user_cd output into GA script block without JS encoding. Integer value in practice, low risk.
- **Includes:** None.
- **Forms:** None.
- **Information disclosure:** `web.xml` description tag says "Linde Fleet Management SYSTEM". Footer does not expose version strings to the browser.

### C:\Projects\cig-audit\repos\fleetfocus\layout\sidebar.jsp
- File exists but is empty (1 line). No findings.

### C:\Projects\cig-audit\repos\fleetfocus\menu\menu.jsp
- **Imports:** `java.util.*`
- **Scriptlet (lines 26–70):** Reads `username`, `user_cd`, `emp_cd`, `userid`, `access_level`, `module` from session. No request parameter inputs rendered to HTML.
- **Expressions:**
  - Line 89/92: `<%=mdn %>` — DB-sourced module name, unescaped in `<font>` tag (see A15-4).
- **Includes:** None.
- **Forms:** None.
- **Note:** This is a legacy menu (old home/home1.jsp architecture); the main admin portal uses `menu-new.jsp`.

### C:\Projects\cig-audit\repos\fleetfocus\menu\menu-new.jsp
- **Imports:** `java.util.*`
- **Scriptlet (lines 5–51):** Reads `username`, `user_cd`, `emp_cd`, `userid`, `access_level`, `module` from session; queries `Menu_Bean` for modules.
- **Expressions:**
  - Line 90: `<%=mdn %>` — DB-sourced module name, unescaped in `<span>` tag (see A15-4).
  - Line 102: `<%=(String)mform_name1.get(i) %>` — DB-sourced form name, unescaped in `<li><a>` tags (see A15-4).
- **Includes:** None.
- **Forms:** None.

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\Administration.jsp
- **Session guard:** No direct `Expire.jsp` include — relies on the parent `admin.jsp` which includes it. This is the standard pattern.
- No forms, no request parameters rendered to HTML.

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\add-general.jsp
- **Session guard:** Line 1 `<%@ include file="../../../sess/Expire.jsp" %>`.
- **Scriptlet:** Reads access context from session; no role-level check beyond session (see A15-3).
- **Forms:**
  - Line 54: `<form id="allocate_user_form" method="post" action="../servlet/Frm_customer">` (add_user) — no CSRF token (see A15-5).
- **Expressions:** DB-sourced customer/site/department lists rendered without encoding (see A15-4).

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\edit-general.jsp
- **Session guard:** Line 1 `<%@ include file="../../../sess/Expire.jsp" %>`.
- **Expressions:**
  - Line 229: `value="<%=Current_User_First_Name%>"` — DB value in form input, unescaped (see A15-4).
  - Line 235: `value="<%=Current_User_Last_Name%>"` — DB value in form input, unescaped.
- **Forms:**
  - Line 160: `<form id="allocate_user_form" method="post" action="../servlet/Frm_customer">` (update_user) — no CSRF token (see A15-5).

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\edit-website-access.jsp
- **Session guard:** None directly (loaded as an include via `admin.jsp` which has session guard, but file has no own guard — partial inconsistency).
- **Expressions:**
  - Line 131: `value="<%=Current_User_Access_Level%>"` — DB value, unescaped.
  - Line 159: `value="<%=Current_User_Email%>"` — DB value in input, unescaped (see A15-4).
  - Lines 204–226: `<%=access_level%>` and `<%=Current_User_Access_Level%>` injected into JavaScript comparisons without JS encoding (see A15-9).
- **Forms:**
  - Line 100: `<form method="post" action="../servlet/Frm_customer">` (update_user tab=4) — no CSRF token (see A15-5).

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\customer\edit-general.jsp
- **Session guard:** Line 2 `<%@ include file="../../../sess/Expire.jsp" %>`.
- **Expressions:** DB-sourced customer fields (`usr_nm`, `usr_fnm`, `usr_lnm`, `usr_email`, etc.) rendered in form field values without escaping (see A15-4).
- **Forms:**
  - Line 108: `<form method="post" action="../servlet/Frm_saveuser">` — no CSRF token (see A15-5).

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\customer\view.jsp
- **Session guard:** Line 1 `<%@ include file="../../../sess/Expire.jsp" %>`.
- **Expressions:**
  - Line 66: `<%=filter.getDebug()%>` — debug output rendered directly to HTML (see A15-11).
  - Lines 81–96: Customer data fields (name, email, phone, address, prefix, company, contract number/date) rendered without HTML encoding (see A15-4).
  - Lines 120–124: Site name, state, address — unescaped.
  - Lines 148–151: Department name — unescaped.

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\Users.jsp (Customers.jsp pattern)
- **Session guard:** Line 1 `<%@ include file="../../sess/Expire.jsp" %>`.
- **Expressions:** User first name, last name, username, department, card/pin, weigand rendered without escaping (see A15-4).
- **Access control:** Buttons gated by `permision[p_user][0/1/2]` checks from session, and `Integer.parseInt(access_level) == 1` for admin-only actions. Pattern is sound but relies entirely on session data set at login.

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\SpecialAdminRights.jsp
- **Session guard:** Line 2 `<%@ include file="../../sess/Expire.jsp" %>`.
- **No explicit role check** beyond session existence (see A15-3).
- **Forms:**
  - Line 44: `<form method="post" action="../servlet/Frm_saveuser">` (special_acess) — no CSRF token (see A15-5).

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\setting\my_profile.jsp
- **Session guard:** Line 2 `<%@ include file="../../../sess/Expire.jsp" %>`.
- **Expressions:**
  - Lines 41, 44, 57: `Fms_Usr_First_Name`, `Fms_Usr_Last_Name`, `Fms_Usr_Email` rendered into form input values without encoding (see A15-4).
  - Line 49, 52: `Fms_Usr_Group_Name`, `Fms_Usr_Access_Level` rendered in `<span>` without encoding.
- **Forms:**
  - Line 31: `<form action="../servlet/Frm_customer" method="post">` — no CSRF token (see A15-5).

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\setting\change_password.jsp
- **Session guard:** Line 1 `<%@ include file="../../../sess/Expire.jsp" %>`.
- **Expressions:**
  - Line 25: `<%=user_fnm %> <%=user_lnm %>` — session-sourced, rendered without encoding (see A15-9).
- **Forms:**
  - Line 28: `<form method="post" action="../servlet/Frm_security">` — no CSRF token (see A15-5).

### C:\Projects\cig-audit\repos\fleetfocus\pages\admin\reports\mod\mail_report.jsp
- **Imports:** Various, including `com.torrent.surat.fms6.util.mail`.
- **Session guard:** Line 1 `<%@ include file="../../../../sess/Expire.jsp" %>`.
- **Scriptlet:** Reads `url` from request parameter, prepends `LindeConfig.emailurl`, then uses `GetHtml.getHTML1(url)` to fetch the page content and email it (see A15-12 — SSRF).
- **Expression:** Line 29: `<%=url%>` — url rendered without encoding. Low impact here as it is a server-side only page, but confirms the parameter is used unvalidated.

---

## STEP 4 — SECURITY REVIEW SUMMARY

### Authentication
- `sess/Expire.jsp` correctly checks `request.getSession(false)` and `session.getAttribute("user_cd")`. All examined protected pages include it.
- `manage_form.jsp` includes `Expire.jsp` but performs **no role or access-level check**, meaning any authenticated user with a valid session can access the form management administrative page.
- Admin sub-pages loaded via `admin.jsp` `<jsp:include>` inherit the `Expire.jsp` guard from the parent, but individual fragments (e.g. `edit-website-access.jsp`) have no own guard, making them potentially directly accessible.

### Authorization / Role Checks
- `Customers.jsp` correctly checks `Integer.parseInt(access_level) == 1` before showing Add/Delete customer buttons.
- `Users.jsp` and most user/customer admin pages rely on a `permision[][]` matrix stored in session, which is set at login. This is correct in principle.
- `manage_form.jsp`, `SpecialAdminRights.jsp`: no admin-level (access_level == 1) check. Any authenticated user can reach these pages.

### Path Traversal in admin.jsp
- `mnm` and `sub` request parameters are concatenated directly into a file path (`/pages/admin/<sub>.jsp`). Only an existence check (`File.exists()`) is performed — no whitelist validation. An attacker with a valid session could attempt to include arbitrary JSP files from within the web application via crafted `sub` parameter values.

### XSS
- Login page uses ESAPI for HTML encoding of URL parameters (good). DB-sourced `msg` variable is rendered without encoding.
- `header.jsp` renders session `user_fnm`/`user_lnm` without HTML encoding. If these contain `<`, `>`, `"` etc., stored XSS is possible.
- Virtually all admin sub-pages render DB-sourced data (names, emails, addresses, form names, module names) without any HTML encoding. No use of ESAPI, `StringEscapeUtils`, or JSTL `fn:escapeXml` was found in the admin pages.
- `admin.jsp` line 166 renders a `message` request parameter directly into a JavaScript `swal()` text value without JS-safe encoding.
- `admin.jsp` line 55 outputs `form__cd` request parameter into a JS variable without encoding.

### CSRF
- No CSRF tokens were found in any of the examined JSP forms. Confirmed by grep across all pages and admin sub-directories returning zero matches for "csrf", "token", "_token", "csrfToken". Every state-changing POST form (user create/edit, customer edit, form management, password change, special admin rights) is vulnerable.

### SQL Injection
- No direct SQL in the examined JSP files. All DB interactions go through `Databean_*` JavaBeans and DAO classes. SQL injection risk must be assessed in those Java classes (separate audit pass).

### Information Disclosure
- `header.jsp` line 14: `<title><%=LindeConfig.systemName %> - Empowered by COLLECTIVE INTELLIGENCE</title>` — reveals the company name/platform name. Low risk but confirms technology.
- `customer/view.jsp` line 66: `<%=filter.getDebug()%>` — debug output is rendered to the user's browser in the customer view page.
- `manage_form.jsp` exposes the complete list of all modules and form paths defined in the database to any authenticated user, regardless of their assigned permissions.
- `mail_report.jsp` accepts a `url` parameter and makes a server-side HTTP request to it (SSRF).

---

## STEP 5 — FINDINGS

---

### A15-1: Stored XSS via Unescaped Database Message in Login Page
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\login.jsp`
**Line:** 403
**Severity:** High
**Category:** XSS (Stored)

**Description:**
The system notification message (`msg`) is retrieved from the database via `MessageDao` and rendered directly into the HTML without any HTML encoding. If an attacker with database write access or an admin who can set this message includes HTML/JavaScript, it will execute in every user's browser on the login page.

**Evidence:**
```java
// lines 149-154
MessageDao msgDao = new MessageDao();
msgDao.setOpCode("get_msg");
msgDao.setFid("1");
msgDao.init();
boolean enableStatus = msgDao.isStatus();
String msg = msgDao.getMsg();
```
```html
<!-- line 401-405 -->
<% if (enableStatus) { %>
<div class="alert alert-info" role="alert">
    <%=msg %>   <!-- NO HTML encoding applied -->
</div>
<%} %>
```

**Recommendation:**
Encode `msg` before output: replace `<%=msg %>` with `<%=org.owasp.esapi.ESAPI.encoder().encodeForHTML(msg) %>`. Note that ESAPI is already imported on this page.

---

### A15-2: JavaScript Context Injection in Login Page (Insufficient Encoding)
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\login.jsp`
**Line:** 641
**Severity:** Medium
**Category:** XSS (Reflected)

**Description:**
The `val` request parameter, after ESAPI HTML encoding, is placed inside a JavaScript string literal. HTML encoding (`&lt;`, `&gt;`, `&#x27;`, etc.) does not protect against JavaScript injection. An attacker can craft a request with `val=';alert(1)//` — HTML encoding would pass the single quote through, breaking out of the JavaScript string.

**Evidence:**
```java
// line 79-80
String value = request.getParameter("val") == null ? "0" : request.getParameter("val");
value = encoder.encodeForHTML(value);   // HTML encoding only — insufficient for JS context
```
```html
<!-- line 641 -->
var value = '<%=value%>'
if (value.toUpperCase() === 'logout'.toUpperCase()) sessionStorage.clear();
```

**Recommendation:**
Use `encoder.encodeForJavaScript(value)` (ESAPI) instead of `encodeForHTML` when embedding values into JavaScript string literals. Alternatively, whitelist-validate `value` as only `"0"`, `"1"`, or `"logout"` before using it.

---

### A15-3: Missing Role-Level Authorization Check on Administrative Pages
**Files:**
- `C:\Projects\cig-audit\repos\fleetfocus\pages\manage_form.jsp`
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\SpecialAdminRights.jsp`
**Lines:** manage_form.jsp:1, SpecialAdminRights.jsp:2 (Expire.jsp include — session check only)
**Severity:** High
**Category:** Broken Access Control / Insufficient Authorization

**Description:**
`manage_form.jsp` and `SpecialAdminRights.jsp` include `Expire.jsp` (which only verifies a valid session exists) but perform no subsequent check that the logged-in user has administrative access level (access_level == 1). Any authenticated user — including a low-privilege customer-level user (access_level 5) — can navigate directly to these pages and:
- `manage_form.jsp`: View, modify, or create application module/form definitions for all customers.
- `SpecialAdminRights.jsp`: View and grant special VOR/CANBUS access rights.

By contrast, `Customers.jsp` correctly checks `Integer.parseInt(access_level) == 1` before showing admin-only actions.

**Evidence:**
```java
// manage_form.jsp line 1 — only session check, no role check
<%@ include file="../sess/Expire.jsp" %>
// No subsequent: if (!access_level.equals("1")) { forward to access denied; }
```
```java
// SpecialAdminRights.jsp line 2 — only session check
<%@ include file="../../sess/Expire.jsp" %>
// access_level is read at line 10 but never checked against "1"
String access_level = (String)session.getAttribute("access_level");
// Used only to scope filter queries, not to gate page access
```

**Recommendation:**
Add an explicit role check immediately after the session guard on both pages:
```java
if (!access_level.equalsIgnoreCase("1")) {
    response.sendRedirect("../pages/admin/customer/access_denied.jsp");
    return;
}
```

---

### A15-4: Widespread Reflected/Stored XSS — Unescaped DB Data in Admin Pages
**Files (representative — pattern is pervasive across all admin sub-pages):**
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\customer\view.jsp` (lines 81–96, 120–124, 148–151)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\edit-general.jsp` (lines 229, 235)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\edit-website-access.jsp` (line 159)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\setting\my_profile.jsp` (lines 41, 44, 57)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\customer\edit-general.jsp` (lines 131–211)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\manage_form.jsp` (lines 67–71, 103)
- `C:\Projects\cig-audit\repos\fleetfocus\menu\menu-new.jsp` (lines 90, 102)
- `C:\Projects\cig-audit\repos\fleetfocus\menu\menu.jsp` (lines 89, 92)

**Severity:** High
**Category:** XSS (Stored)

**Description:**
Database-sourced values (customer names, user first/last names, email addresses, phone numbers, addresses, form names, module names, site names, department names) are rendered throughout the admin pages using `<%= ... %>` with no HTML encoding. No use of ESAPI, JSTL `fn:escapeXml`, `StringEscapeUtils.escapeHtml4`, or any other encoding function was found across admin JSP files.

An attacker with write access to any of these DB fields (e.g. by editing their own profile name, or if an admin were socially engineered into setting a malicious customer name) could achieve stored XSS affecting all users who view the relevant admin page.

**Evidence:**
```java
// customer/view.jsp lines 81-96 — all unescaped
<tr><td>Account Prefix</td><td> <%=Customer_Data_Prefix%></td></tr>
<tr><td>Company Name</td>  <td> <%=Customer_Data_Company%></td></tr>
<tr><td>Contract No</td>   <td> <%=Customer_Data_Contract_No%></td></tr>
<tr><td>Name</td>          <td> <%=Customer_Data_Name%></td></tr>
<tr><td>Email</td>         <td> <%=Customer_Data_Email%></td></tr>
<tr><td>Phone</td>         <td> <%=Customer_Data_Phone%></td></tr>
<tr><td>Address</td>       <td> <%=Customer_Data_Address%></td></tr>
```
```java
// edit-general.jsp lines 229, 235 — DB values in input field values, unescaped
<input type="text" name="fname" value="<%=Current_User_First_Name%>" ... />
<input type="text" name="lname" value="<%=Current_User_Last_Name%>" ... />
```
```java
// menu-new.jsp line 90 — module name from DB, unescaped in navigation
<a href="..."><span>...</span><span class="menulabel"><%=mdn %></span></a>
```

**Recommendation:**
Introduce a consistent output encoding strategy. The ESAPI library is already a declared dependency (used on login.jsp). Create a shared utility method or JSTL tag library function and apply `ESAPI.encoder().encodeForHTML(value)` to all `<%= ... %>` expressions that render data-sourced strings into HTML. For values placed inside HTML attribute values, use `encodeForHTMLAttribute()`. This is a systemic remediation — consider a global find-and-replace pass on all JSP files followed by testing.

---

### A15-5: No CSRF Protection on Any State-Changing Forms
**Files (representative — pattern covers all admin forms):**
- `C:\Projects\cig-audit\repos\fleetfocus\pages\manage_form.jsp` (lines 63, 79)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\add-general.jsp` (line 54)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\edit-general.jsp` (line 160)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\user\edit-website-access.jsp` (line 100)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\customer\edit-general.jsp` (line 108)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\setting\my_profile.jsp` (line 31)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\setting\change_password.jsp` (line 28)
- `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\SpecialAdminRights.jsp` (line 44)

**Severity:** High
**Category:** CSRF

**Description:**
A global grep for "csrf", "token", "_token", and "csrfToken" across all JSP files under `pages/` and `pages/admin/` returned zero matches. No CSRF tokens are included in any form. All state-changing POST operations (add user, edit user, change password, edit customer, manage forms, special admin rights) can be triggered by a cross-site request forged by a malicious page — provided the victim is currently logged in.

This is particularly severe because:
- An attacker can create admin accounts or grant admin access level to a target user.
- An attacker can change a victim user's password.
- An attacker can modify customer or form data.

**Evidence:**
```html
<!-- manage_form.jsp line 63 — no token -->
<form method="post" action="../servlet/Frm_Customer">
  <input type="hidden" value="update_forms" name="method">
  <!-- no <input type="hidden" name="csrf_token" value="..."> -->

<!-- edit-website-access.jsp line 100 — no token -->
<form method="post" action="../servlet/Frm_customer" class="ajax_mode_c">
  <input type="hidden" name="method" value="update_user">
  <!-- no CSRF token -->

<!-- change_password.jsp line 28 — no token -->
<form method="post" action="../servlet/Frm_security" class="ajax_mode_c">
  <input type="hidden" name="op_code" value="pass_chg">
  <!-- no CSRF token -->
```

**Recommendation:**
Implement the Synchronizer Token Pattern. Generate a cryptographically random token at session creation time and store it in the session. Include it as a hidden field in every POST form. Validate the submitted token server-side in every servlet handler before processing the request. Libraries such as OWASP ESAPI's `CSRFGuard` or Spring Security CSRF support can streamline this. For AJAX requests, include the token in a custom HTTP header and validate server-side.

---

### A15-6: Path Traversal via Unvalidated `mnm`/`sub` Parameters in admin.jsp
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\admin.jsp`
**Lines:** 119–145
**Severity:** High
**Category:** Path Traversal / Unauthorized File Inclusion

**Description:**
The `mnm` and `sub` request parameters are concatenated directly into a file path and then included via `<jsp:include>`. Only a file-existence check is performed. No whitelist validation of allowed values, no path canonicalization check, and no prevention of `..` sequences.

An attacker with a valid session can craft a `sub` parameter value to attempt to include arbitrary JSP files outside the intended `/pages/admin/` directory. For example: `sub=../../WEB-INF/web.xml` (though JSP include of non-JSP files would behave differently). More practically, `sub=../../pages/manage_form` would include the form management page regardless of whether the user has been granted access to it through the permissions system — and with a `form__cd` of null, the permission check is bypassed (line 144: `form__cd == null || permision[...][0].equalsIgnoreCase("t")`).

**Evidence:**
```java
// admin.jsp lines 119-145
String mnm = request.getParameter("mnm")==null? "Home" : request.getParameter("mnm");
String sub = request.getParameter("sub")==null? "" : request.getParameter("sub");
String filepath = "";
if( sub.isEmpty() ) {
    filepath = "/pages/admin/"+mnm+".jsp";   // mnm is user-controlled, not validated
} else {
    filepath = "/pages/admin/"+sub+".jsp";   // sub is user-controlled, not validated
    // ...only 3 hardcoded UK-specific overrides
}
String realpath = servletContext.getRealPath(filepath);
File f=new File(realpath);
if (f.exists()) {
    // Permission check is bypassed when form__cd is null:
    <%if( form__cd == null || permision[Integer.parseInt(form__cd)][0].equalsIgnoreCase("t")){ %>
    <jsp:include page="<%= filepath %>" flush="true" />
```

**Recommendation:**
- Implement a whitelist of permitted `mnm` and `sub` values, validated before constructing the filepath.
- Alternatively, store the allowed page mappings in the database (as the permissions system already does) and resolve only those paths, refusing any `sub` value not present in the authorised list.
- Add a path canonicalization check to reject any `filepath` that does not start with `/pages/admin/` after resolution.
- When `form__cd` is null (i.e., for pages that are not registered in the permissions system), access should be denied rather than defaulting to allow.

---

### A15-7: Permission Check Bypassed When `form_cd` Parameter is Absent
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\admin.jsp`
**Line:** 144
**Severity:** Medium
**Category:** Broken Access Control

**Description:**
The permission check in `admin.jsp` is conditional on `form__cd` being non-null. When the `form_cd` request parameter is omitted, `form__cd` is null, and the `permision[][]` check is skipped entirely — the page is included with no access control. This means any authenticated user can access any sub-page of `/pages/admin/` simply by omitting the `form_cd` parameter from the URL.

**Evidence:**
```java
// admin.jsp line 144
<%if( form__cd == null || permision[Integer.parseInt(form__cd)][0].equalsIgnoreCase("t")){ %>
  <jsp:include page="<%= filepath %>" flush="true" />
<%}else{
    out.println("Access Denied!");
} %>
```
When `form__cd == null` the entire `permision[]` check is short-circuited; the include proceeds unconditionally.

**Recommendation:**
Reverse the logic to deny by default. Change the condition to:
```java
if (form__cd != null && permision[Integer.parseInt(form__cd)][0].equalsIgnoreCase("t")) {
    // include page
} else {
    out.println("Access Denied!");
}
```
This ensures that any request without a valid `form_cd` that maps to an authorised permission is rejected.

---

### A15-8: JavaScript Context XSS via Unencoded Request Parameters in admin.jsp
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\admin.jsp`
**Lines:** 55, 159–172
**Severity:** High
**Category:** XSS (Reflected)

**Description:**
Two separate JavaScript injection points exist in `admin.jsp`:

1. **Line 55:** `form__cd` (request parameter) is injected directly into a JavaScript string without any encoding. An attacker can inject arbitrary JavaScript.

2. **Lines 159–172:** The `message` request parameter is read without encoding and placed verbatim inside a JavaScript `swal()` call. A request to `admin.jsp?mnm=Home&message=<payload>` would inject the payload into the `swal()` text.

**Evidence:**
```java
// admin.jsp line 20-21, 55
String form__cd = request.getParameter("form_cd");   // raw, no sanitization
...
<script>
var FORM__CD = "<%=form__cd%>";   // direct injection into JS — if form_cd=";alert(1)// then XSS
</script>
```
```java
// admin.jsp lines 158-172
String message = request.getParameter("message") == null ? "" : request.getParameter("message");
// No encoding applied
if(!message.isEmpty()){ %>
<script>
  setTimeout(function(){
    swal({
      title: "Success",
      text: "<%=message%>",   // raw request parameter in JS — reflected XSS
      ...
    });
  },100);
</script>
```

**Recommendation:**
Use `ESAPI.encoder().encodeForJavaScript(value)` when embedding values inside JavaScript string literals. For `form__cd`, validate that it is a numeric integer before use. For `message`, apply JS encoding before embedding.

---

### A15-9: Unescaped Session Data (User Name) Rendered in Header — Stored XSS Risk
**File:** `C:\Projects\cig-audit\repos\fleetfocus\layout\header.jsp`
**Line:** 169
**Severity:** Medium
**Category:** XSS (Stored)

**Description:**
The user's first name and last name are retrieved from the session and rendered into the top navigation bar without HTML encoding. These values originate from the database (set at login from the user record). If a user's name in the database contains HTML-special characters (either from legitimate data or due to insufficient input validation at account creation), it will be injected into the HTML of every page that includes `header.jsp` — i.e., every page the user visits after logging in.

Additionally, `change_password.jsp` line 25 outputs session `user_fnm`/`user_lnm` without encoding in a heading.

**Evidence:**
```java
// header.jsp lines 3-4, 169
String fnm = ""+session.getAttribute("user_fnm");
String lnm = ""+session.getAttribute("user_lnm");
...
<li class="username"><a><%=fnm+" "+lnm %></a></li>   <!-- no encoding -->
```
```java
// change_password.jsp line 25
<h3 class="panel-title">You are logged on as:  <%=user_fnm %> <%=user_lnm %></h3>
```

**Recommendation:**
Apply `ESAPI.encoder().encodeForHTML()` to `fnm` and `lnm` before rendering. This is a one-line fix in `header.jsp` that protects every page that includes it:
```java
<li class="username"><a><%=ESAPI.encoder().encodeForHTML(fnm+" "+lnm) %></a></li>
```

---

### A15-10: Debug Output Rendered to Browser in Customer View Page
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\customer\view.jsp`
**Line:** 66
**Severity:** Low
**Category:** Information Disclosure

**Description:**
The `filter.getDebug()` method output is rendered directly to the browser on the customer view page. Depending on what the `Databean_customer` bean populates in its debug field, this could expose SQL query strings, internal exception messages, or other implementation details to the authenticated user.

**Evidence:**
```java
// customer/view.jsp line 66
<%=filter.getDebug()%>
```

**Recommendation:**
Remove the debug output line from the production JSP. Debug information should only be written to server-side logs, never rendered to the browser. If this output is empty in production, the line is still a code quality concern and should be removed to prevent future accidental disclosure.

---

### A15-11: manage_form.jsp Exposes Full Application Form/Module Registry to Any Authenticated User
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\manage_form.jsp`
**Lines:** 7–30 (data retrieval), 61–113 (rendering)
**Severity:** Medium
**Category:** Information Disclosure / Broken Access Control

**Description:**
`manage_form.jsp` queries and renders the complete list of all modules, forms, form paths, and form codes defined in the application database. This page is accessible to any authenticated user (access_level check is absent — see A15-3). An attacker with any valid account can:
1. Enumerate all application modules and their internal codes.
2. See the filesystem paths of all JSP pages in the application.
3. Identify forms they do not have permission to access, then attempt to navigate to them directly or exploit A15-6 (path traversal).

**Evidence:**
```java
// manage_form.jsp lines 15-29 — retrieves everything
ArrayList Module_Cd = filter.getBonus_Module_Cd();
ArrayList Module_Name = filter.getBonus_Module_Name();
ArrayList Form_Cd = filter.getBonus_Form_Cd();
ArrayList Form_Name = filter.getBonus_Form_Name();
ArrayList Form_Path = filter.getBonus_Form_Path();   // filesystem paths exposed
...
// lines 67-71 — rendered to browser
<legend>Form CD: <%=Form_Cd.get(x).toString()%></legend>
<input ... value="<%=Form_Name.get(x).toString()%>" />
<input ... value="<%=(Form_Path.get(x).toString()...)%>" />
```

**Recommendation:**
Add an admin-level access check as described in A15-3. Additionally, consider whether form paths need to be displayed in the browser UI, or whether they can be stored server-side only and referenced by opaque identifiers.

---

### A15-12: SSRF via Unvalidated `url` Parameter in mail_report.jsp
**File:** `C:\Projects\cig-audit\repos\fleetfocus\pages\admin\reports\mod\mail_report.jsp`
**Lines:** 2–5, 20
**Severity:** High
**Category:** Server-Side Request Forgery (SSRF)

**Description:**
The `url` request parameter is taken from user input, prefixed with `LindeConfig.emailurl`, and passed to `GetHtml.getHTML1(url)` which performs an HTTP request to fetch the page content. While the `LindeConfig.emailurl` prefix provides partial mitigation, the remainder of the path is entirely attacker-controlled. If `LindeConfig.emailurl` points to the application's own base URL, an attacker can supply path traversal sequences or query strings to cause the server to make arbitrary internal HTTP requests to any path within the application. If the email URL base can be bypassed (e.g. via URL encoding or protocol-relative references), broader SSRF to internal network resources is possible.

**Evidence:**
```java
// mail_report.jsp lines 2-5
String url = request.getParameter("url")==null?"":request.getParameter("url");
url= LindeConfig.emailurl+"/pages/admin/reports/mod/"+url;   // url is user-controlled suffix
url = url.replaceAll(" ","+");
...
data+=obj.getHTML1(url);   // server-side HTTP request to attacker-influenced URL
```

**Recommendation:**
- Validate the `url` parameter against a strict whitelist of permitted report page paths (e.g. only file names matching `[a-z_]+` with no slashes or dots).
- Do not accept user-supplied path components for server-side HTTP requests.
- If the report page to fetch must be dynamic, use an internal identifier (numeric ID or enum) that is resolved server-side to a pre-approved path list.

---

## Summary Table

| ID     | Severity | Category                        | File(s)                                         |
|--------|----------|---------------------------------|-------------------------------------------------|
| A15-1  | High     | Stored XSS                      | pages/login.jsp:403                             |
| A15-2  | Medium   | Reflected XSS (JS context)      | pages/login.jsp:641                             |
| A15-3  | High     | Broken Access Control           | pages/manage_form.jsp, admin/SpecialAdminRights.jsp |
| A15-4  | High     | Stored XSS (pervasive)          | All admin sub-pages — unescaped DB output       |
| A15-5  | High     | CSRF                            | All state-changing forms (no tokens anywhere)   |
| A15-6  | High     | Path Traversal                  | pages/admin.jsp:119-145                         |
| A15-7  | Medium   | Broken Access Control           | pages/admin.jsp:144                             |
| A15-8  | High     | Reflected XSS (JS context)      | pages/admin.jsp:55, 159-172                     |
| A15-9  | Medium   | Stored XSS                      | layout/header.jsp:169                           |
| A15-10 | Low      | Information Disclosure          | pages/admin/customer/view.jsp:66                |
| A15-11 | Medium   | Information Disclosure / AuthZ  | pages/manage_form.jsp                           |
| A15-12 | High     | SSRF                            | pages/admin/reports/mod/mail_report.jsp:2-5     |

**Total findings: 12**
**High severity: 7 (A15-1, A15-3, A15-4, A15-5, A15-6, A15-8, A15-12)**
**Medium severity: 4 (A15-2, A15-7, A15-9, A15-11)**
**Low severity: 1 (A15-10)**
