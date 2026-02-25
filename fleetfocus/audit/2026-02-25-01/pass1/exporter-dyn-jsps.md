# Security Audit: exporter/, sess/, dyn_report/, includes/, au_email/, linde_reports/

**Agent:** A13
**Audit run:** 2026-02-25-01
**Branch verified:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Date:** 2026-02-25
**Scope:** All JSP files in the six assigned directories

---

## File Inventory (Reading Evidence)

### exporter/ (3 files)
- `exporter/checklist.jsp` — includes `../sess/Expire.jsp`; reads vehicle_cd, div_cd, module_cd, form_cd, customer from request; produces CSV via PrintWriter; session access_user passed to filter
- `exporter/users.jsp` — includes `../sess/Expire.jsp`; reads customer from request; passes access_level, access_cust, access_site, access_dept from session to filter; exports PII (name, card number, facility code, expiry date)
- `exporter/vehicles.jsp` — includes `../sess/Expire.jsp`; reads customer from request; passes session access controls to filter; exports fleet data

### sess/ (1 file)
- `sess/Expire.jsp` — authentication guard included by all protected pages; checks session existence and `user_cd` attribute; forwards to login.jsp if absent; does NOT call `session.invalidate()`

### dyn_report/ (29 files)
- `dyn_report/email_vor_status_report.jsp` — includes report_email_header.jsp (chain: Expire.jsp); access_level hardcoded "1", access_cust/site/dept hardcoded ""; unescaped DB outputs in HTML
- `dyn_report/excel_driver_league.jsp` — includes report_export_header.jsp (chain: Expire.jsp); NO access_level/access_cust reads from session; no filter.setAccess_* calls
- `dyn_report/email_driver_league.jsp` — includes report_email_header.jsp; NO access_level/access_cust reads; unescaped DB outputs
- `dyn_report/print_driver_league.jsp` — includes report_export_header.jsp; NO access_level/access_cust reads; unescaped DB outputs
- `dyn_report/get_dept.jsp` — includes Expire.jsp; reads dept list; DB values concatenated into XML string without escaping
- `dyn_report/get_site.jsp` — includes Expire.jsp; reads site list; DB values concatenated into XML string without escaping
- `dyn_report/mail_conf.jsp` — includes report_header.jsp (chain: Expire.jsp); reflects `message`, `url`, time params unescaped; form has no CSRF token
- `dyn_report/mail_first.jsp` — includes Expire.jsp; reflects `url` in hidden input unescaped; form targets mail_report.jsp; no CSRF token
- `dyn_report/mail_report.jsp` — includes Expire.jsp; `mail_id` and `subject` from request passed to sendMail(); `url` from request prepended with base URL; `mail_id` reflected in HTML unescaped
- `dyn_report/email_dyn_driver_report.jsp` — includes report_email_header.jsp; access_level hardcoded "1", access_cust/site/dept hardcoded ""; unescaped DB outputs
- `dyn_report/email_dyn_seen_report.jsp` — same hardcoded bypass pattern; unescaped DB outputs
- `dyn_report/email_dyn_unit_report.jsp` — same hardcoded bypass pattern; unescaped DB outputs
- `dyn_report/email_dyn_unit_report_exc.jsp` — session variables explicitly commented out; access_level hardcoded "1"; NO Expire.jsp include (head block only)
- `dyn_report/email_vor_report.jsp` — same hardcoded bypass; vor_flag hardcoded "1"
- `dyn_report/excel_dyn_driver_report.jsp` — includes report_export_header.jsp; session access controls properly set on filter
- `dyn_report/excel_dyn_seen_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/excel_dyn_unit_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/excel_dyn_unit_report_exc.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/excel_vor_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/excel_vor_unit_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/print_dyn_driver_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/print_dyn_seen_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/print_dyn_unit_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/print_dyn_unit_report_exc.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/print_vor_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/print_vor_unit_report.jsp` — includes report_export_header.jsp; session access controls properly set
- `dyn_report/rpt_dyn_driver_report.jsp` — includes report_header_keyword.jsp; session access controls properly set; request params reflected in JS onclick handlers
- `dyn_report/rpt_dyn_seen_report.jsp` — same; request params in JS onclick handlers
- `dyn_report/rpt_dyn_unit_report.jsp` — same; request params in JS onclick handlers

### includes/ (27 files)
- `includes/report_header.jsp` — includes `../sess/Expire.jsp` at line 3; provides auth guard for standard report pages
- `includes/report_header_basic.jsp` — includes `../sess/Expire.jsp` at line 3
- `includes/report_header_keyword.jsp` — includes `../sess/Expire.jsp` at line 3
- `includes/report_header_nodate.jsp` — includes `../sess/Expire.jsp` at line 3
- `includes/report_header_nodate_model.jsp` — includes `../sess/Expire.jsp` at line 3
- `includes/report_export_header.jsp` — includes `../sess/Expire.jsp`; auth guard for export/print pages
- `includes/report_nevigation.jsp` — form POSTs to `../servlet/Frm_saveuser`; no CSRF token; renders DB-sourced customer/site/dept lists
- `includes/report_nevigation_keyword.jsp` — form POSTs to `../servlet/Frm_saveuser`; no CSRF token; reflects `search_crit` unescaped
- `includes/report_nevigation_nodate.jsp` — filter form; no CSRF token; renders DB-sourced lists
- `includes/report_nevigation_nodate_model.jsp` — filter form; no CSRF token; renders DB-sourced lists
- `includes/report_nevigation_todate.jsp` — form POSTs to `../servlet/Frm_saveuser`; no CSRF token
- `includes/report_email.jsp` — email body header fragment; outputs `st_dt`, `to_dt`, `get_user`, `get_loc`, `get_dep`, `form_nm` unescaped; values from filter bean (DB-sourced)
- `includes/report_email_footer.jsp` — static HTML email footer; no dynamic content
- `includes/report_email_header.jsp` — includes `../sess/Expire.jsp`; provides auth guard for email report pages
- `includes/report_email_keyword.jsp` — email body header; outputs `st_dt`, `to_dt`, `get_user`, `get_loc`, `get_dep`, `form_nm` unescaped; DB-sourced
- `includes/report_email_month.jsp` — email body header with month parameter; outputs `month`, `st_dt`, `to_dt`, `get_user`, `get_loc`, `get_dep`, `form_nm` unescaped
- `includes/report_excel.jsp` — Excel export header; outputs `st_dt`, `to_dt`, `get_user`, `get_loc`, `get_dep`, `form_nm` unescaped
- `includes/report_excel_keyword.jsp` — Excel export header; same unescaped outputs
- `includes/report_export.jsp` — print/export header; outputs `st_dt`, `to_dt`, `get_user`, `get_loc`, `get_dep`, `form_nm` unescaped; conditional on LindeConfig.siteName
- `includes/report_export_footer.jsp` — static HTML export footer
- `includes/report_export_keyword.jsp` — export header; outputs `st_dt`, `to_dt`, `search_crit`, `form_nm` unescaped
- `includes/report_export_keyword_footer.jsp` — static HTML footer
- `includes/report_export_keyword_no_cust_site_dept.jsp` — export header; outputs `st_dt`, `to_dt`, `search_crit`, `form_nm` unescaped
- `includes/report_export_keyword_zlinde.jsp` — export header with ZLinde flag; outputs `st_dt`, `to_dt`, `get_user`, `get_loc`, `get_dep`, `search_crit`, `form_nm` unescaped
- `includes/report_export_keyword_zlinde_opmode.jsp` — export header; same unescaped outputs; `opModeLabel` derived from `opMode` request param (validated via known values)
- `includes/report_export_with_duration.jsp` — export header; outputs `st_dt`, `to_dt`, `get_user`, `get_loc`, `get_dep`, `duration`, `form_nm` unescaped
- `includes/report_footer.jsp` — page footer fragment; hidden inputs output `form_cd` and `access_level` unescaped

### au_email/ (2 files)
- `au_email/xlsx_daily_veh_summary_input_mail.jsp` — includes `../sess/Expire.jsp`; session access controls read and set; reflects `loc_nm`, `dept_nm`, `cust` from request in hidden inputs unescaped
- `au_email/xlsx_daily_veh_summary_report_mail.jsp` — NO Expire.jsp include; session access controls read; `mail_id` from request passed to sendExcelReport(); `mail_id` reflected in HTML unescaped

### linde_reports/ (9 files)
- `linde_reports/linde_reports_subscription.jsp` — NO Expire.jsp; NO authentication; `rpt_name`, `email`, `cust_cd`, `loc_cd`, `st_dt`, `end_dt` from request concatenated into ProcessBuilder shell commands
- `linde_reports/impact_by_unit_with_util.jsp` — includes `linde_reports_inc.jsp` (file not found in repo); NO standalone auth; `cust_cd`, `loc_cd` from request; DB model/unit names injected into Highcharts JS config unescaped
- `linde_reports/red_impact.jsp` — NO Expire.jsp; NO authentication; `email` reflected in hidden input; `siteList.get(i)` from DB injected into JavaScript unescaped
- `linde_reports/preop_complete.jsp` — includes `linde_reports_inc.jsp`; `cust_cd`, `loc_cd`, `email` from request; `siteList.get(i)` injected into JavaScript unescaped
- `linde_reports/unit_utilisation.jsp` — NO standalone auth; `cust_cd`, `loc_cd`, `email` from request; `siteList.get(i)` from DB injected into JavaScript unescaped
- `linde_reports/util_driver_all_models.jsp` — includes `linde_reports_inc.jsp`; `cust_cd`, `loc_cd` from request; `modelList.get(k)` from DB injected into JS unescaped
- `linde_reports/util_driver_logon.jsp` — includes `linde_reports_inc.jsp`; `cust_cd`, `loc_cd` from request; `modelList.get(k)` from DB injected into JS unescaped
- `linde_reports/national_preop_checks.jsp` — includes `linde_reports_inc.jsp`; `cust_cd`, `loc_cd` from request; DB model names injected into JS unescaped
- `linde_reports/nat2_util_driver_all_models.jsp` — includes `linde_reports_inc.jsp`; `cust_cd`, `loc_cd` from request; DB-sourced strings injected into JS unescaped

---

## Security Findings

---

### A13-1

**File:** `C:\Projects\cig-audit\repos\fleetfocus\linde_reports\linde_reports_subscription.jsp`, lines 58–73
**Severity:** Critical
**Category:** OS Command Injection
**Description:** User-supplied request parameters `rpt_name`, `email`, `cust_cd`, `loc_cd`, `st_dt`, and `end_dt` are concatenated without any sanitisation directly into shell commands executed via `ProcessBuilder`. On Linux the command is passed to `/bin/sh -c`, making shell metacharacter injection (`;`, `&&`, `|`, backticks, `$()`) trivially exploitable. The `rpt_name` parameter is especially dangerous because it appears as a path component. An attacker can execute arbitrary OS commands as the application server user. There is also no authentication on this page (no Expire.jsp include).
**Evidence:**
```java
builder = new ProcessBuilder(
    "/bin/sh", "-c","/usr/local/share/phantomjs-1.9.8-linux-x86_64/bin/phantomjs "
        + " /home/gmtp/phantomjs_files/linde_charts.js "
        + " '"+RuntimeConf.emailurl+"/linde_reports/"
        + rpt_name+".jsp?email="+email+"&cust_cd="+cust_cd+"&loc_cd="+loc_cd
        + "&st_dt="+st_dt+"&end_dt="+end_dt
        + "' >> /home/gmtp/phantom.log");
```
On Windows (lines 62–65):
```java
builder = new ProcessBuilder(
    "cmd.exe", "/c", "cd D:\\MyFiles\\Work\\PanthomJs\\bin\\ && D: && phantomjs.exe "
        + " linde_charts.js "
        + " \"http://192.168.10.47:8090/fms/linde_reports/"+rpt_name+".jsp?email="+email
        + "&cust_cd="+cust_cd+"&loc_cd="+loc_cd+"&st_dt="+st_dt+"&end_dt="+end_dt+"\" ");
```
**Recommendation:** This endpoint must be authenticated. All parameters passed to external processes must be validated against a strict allowlist before use. The `rpt_name` parameter should be validated to match only known report names (exact string comparison against a fixed set). All other parameters must be validated for format (e.g. date format, numeric IDs). Consider replacing shell invocation with a direct Java API call that does not involve a shell interpreter.

---

### A13-2

**File:** `C:\Projects\cig-audit\repos\fleetfocus\linde_reports\linde_reports_subscription.jsp`, line 1 (no include)
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\red_impact.jsp`, line 1 (no include)
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\unit_utilisation.jsp`, lines 1–15 (no include)
`C:\Projects\cig-audit\repos\fleetfocus\au_email\xlsx_daily_veh_summary_report_mail.jsp`, lines 1–39 (no include)
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_unit_report_exc.jsp`, lines 1–33 (no include and commented-out session reads)
**Severity:** Critical
**Category:** Missing Authentication (Unauthenticated Access)
**Description:** Five pages are entirely missing the `Expire.jsp` authentication guard (or any equivalent check). Any unauthenticated user who can reach the application server can call these URLs and receive data or trigger actions. `linde_reports_subscription.jsp` additionally executes OS commands. `xlsx_daily_veh_summary_report_mail.jsp` sends email with attacker-controlled recipient. `email_dyn_unit_report_exc.jsp` has the session attribute reads explicitly commented out.
**Evidence:**

`dyn_report/email_dyn_unit_report_exc.jsp` lines 27–33:
```java
//String access_level = (String)session.getAttribute("access_level");
//String access_cust = (String)session.getAttribute("access_cust");
//String access_site = (String)session.getAttribute("access_site");
//String access_dept = (String)session.getAttribute("access_dept");
String access_level = "1";
String access_cust = "";
String access_site = "";
String access_dept = "";
```
`au_email/xlsx_daily_veh_summary_report_mail.jsp` — no `<%@include file="../sess/Expire.jsp" %>` present anywhere in file.

`linde_reports/linde_reports_subscription.jsp` — no `<%@include file="../sess/Expire.jsp" %>` present anywhere in file.

`linde_reports/red_impact.jsp` — no `<%@include file="../sess/Expire.jsp" %>` present anywhere in file.

`linde_reports/unit_utilisation.jsp` — no `<%@include file="../sess/Expire.jsp" %>` present anywhere in file.

**Recommendation:** Every JSP that serves data or triggers actions must include `<%@include file="../sess/Expire.jsp" %>` (or its equivalent through an include chain) as the first statement. Review all pages in the `linde_reports/` and `au_email/` directories; none of the linde_reports chart pages appear to rely on Expire.jsp except through the missing `linde_reports_inc.jsp` include whose content is not in the repository.

---

### A13-3

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_vor_status_report.jsp`, lines 22–25
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_driver_report.jsp`, lines 22–25
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_seen_report.jsp`, lines 21–24
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_unit_report.jsp`, lines 22–25
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_unit_report_exc.jsp`, lines 30–33
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_vor_report.jsp`, lines 22–25
**Severity:** Critical
**Category:** Broken Access Control / Hardcoded Access Level Bypass
**Description:** Six email report delivery pages hardcode `access_level = "1"` and set `access_cust`, `access_site`, and `access_dept` to empty strings rather than reading the authenticated user's session attributes. Access level 1 is the highest privilege (admin/all-customer) level in this system. This means any authenticated user who triggers one of these email report URLs will have their customer/site/department scope restrictions stripped away and will receive data scoped to access level 1 with no customer filter. The result is cross-tenant data exposure: a user belonging to customer A can receive report data for all customers.
**Evidence** (pattern repeated in all six files):
```java
// email_vor_status_report.jsp lines 22–25
String access_level = "1";
String access_cust = "";
String access_site = "";
String access_dept = "";
```
Compare correct pattern in `excel_dyn_driver_report.jsp`:
```java
String access_level = (String)session.getAttribute("access_level");
String access_cust = (String)session.getAttribute("access_cust");
String access_site = (String)session.getAttribute("access_site");
String access_dept = (String)session.getAttribute("access_dept");
```
**Recommendation:** Replace all hardcoded access level values with reads from `session.getAttribute(...)` as done in the correctly implemented export pages. Do not commit these pages to production until corrected. Audit the backend query named ops (`fetch_vor_status`, `fetch_email_dyn_driver`, etc.) to confirm that access_cust and related parameters are enforced as hard filters in SQL.

---

### A13-4

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\excel_driver_league.jsp`, lines 1–40
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_driver_league.jsp`, lines 1–40
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\print_driver_league.jsp`, lines 1–40
**Severity:** High
**Category:** Missing Access Control Scoping (Driver League Reports)
**Description:** The three Driver League report delivery pages (Excel export, email, print) include the Expire.jsp authentication guard via their header includes, so unauthenticated access is blocked. However, none of these pages read `access_level`, `access_cust`, `access_site`, or `access_dept` from session, and none call `filter.setAccess_*()`. The customer scoping of the report data depends entirely on whatever default the backend applies. A user at customer A could potentially manipulate request parameters to receive Driver League data belonging to customer B if the backend does not apply independent customer enforcement.
**Evidence** (from `excel_driver_league.jsp`):
```java
// Lines 1–40: no session.getAttribute("access_level"), no filter.setAccess_*() calls
// filter is populated only with:
filter.setParam_Customer(user_cd);
filter.setParam_Location(loc_cd);
filter.setParam_Dept(dept_cd);
filter.setParam_Form(form_cd);
```
**Recommendation:** Add `access_level`, `access_cust`, `access_site`, `access_dept` reads from session and pass them to the filter bean via `filter.setAccess_level()`, `filter.setAccess_cust()`, `filter.setAccess_site()`, `filter.setAccess_dept()` as implemented in the correctly scoped pages. Confirm backend enforcement independently.

---

### A13-5

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\mail_report.jsp`, lines 19–70
**Severity:** High
**Category:** Email Header Injection / SSRF
**Description:** Two injection risks exist. (1) The `mail_id` parameter (email recipient address) and `subject` parameter are taken from the request without sanitisation and passed directly to `mobj.sendMail(subject, data, group_id, mail_id, sName, sEmail)`. If the underlying mail library does not sanitise these, an attacker can inject SMTP headers via newline characters in `mail_id` or `subject`, redirecting or copying the email. (2) The `url` parameter from the request is prepended with a hardcoded base: `url = LindeConfig.emailurl+"/dyn_report/"+url`. The result is used as a URL to fetch report content. If `url` is not validated to be a safe relative path on the same server, this constitutes an SSRF vector allowing the application to fetch internal resources.
**Evidence:**
```java
String url = request.getParameter("url") == null ? "" : request.getParameter("url");
String mail_id = request.getParameter("mail_id") == null ? "" : request.getParameter("mail_id");
String subject = request.getParameter("subject") == null ? "" : request.getParameter("subject");
// ...
url = LindeConfig.emailurl+"/dyn_report/"+url;
// ...
mobj.sendMail(subject,data,group_id,mail_id,sName,sEmail);
```
**Recommendation:** Validate `mail_id` against RFC 5322 email format and reject any value containing `\r` or `\n`. Validate `subject` and strip newline characters. For the `url` parameter, validate it is a known report page name matching a fixed allowlist of valid report JSP names; do not use free-form user input to construct server-side fetch URLs.

---

### A13-6

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_email\xlsx_daily_veh_summary_report_mail.jsp`, lines 85–136
**Severity:** High
**Category:** Email Injection / Missing Authentication
**Description:** This page has no authentication guard and accepts `mail_id` from the request. The `mail_id` is passed directly to `mailReport.sendExcelReport(subject, mail_id, ...)` without sanitisation, enabling SMTP header injection. `mail_id` is also reflected unescaped in the HTML response.
**Evidence:**
```java
String mail_id = request.getParameter("mail_id") == null ? "" : request.getParameter("mail_id");
// ...
mailReport.sendExcelReport(subject, mail_id, ...);
// ...
out.write(mail_id); // line ~136, unescaped
```
**Recommendation:** Add `<%@include file="../sess/Expire.jsp" %>` as the first statement. Validate `mail_id` as a valid email address and strip any `\r` or `\n` characters before use.

---

### A13-7

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\mail_conf.jsp`, lines 127, 242, 309, 314–319
**Severity:** High
**Category:** Reflected Cross-Site Scripting (XSS)
**Description:** The `message` parameter from the request is reflected unescaped into HTML at lines 242 and 309. Additional request parameters `url`, `hour`, `min`, `st_time`, `to_time` are reflected into hidden input values without HTML-encoding at lines 314–319. Any attacker who can cause a victim user to visit a crafted URL can inject and execute arbitrary JavaScript in the victim's browser session.
**Evidence:**
```jsp
// Line 242 and 309:
<%=message %>

// Lines 314–319 (hidden inputs):
<input type="hidden" name="url" value="<%=url %>">
<input type="hidden" name="hour" value="<%=hour %>">
<input type="hidden" name="min" value="<%=min %>">
<input type="hidden" name="st_time" value="<%=st_time %>">
<input type="hidden" name="to_time" value="<%=to_time %>">
```
**Recommendation:** HTML-encode all request parameters before reflecting them in HTML responses. Use `ESAPI.encoder().encodeForHTML(message)` or equivalent (e.g. `StringEscapeUtils.escapeHtml4()`). For attributes in particular, use `encodeForHTMLAttribute()`. Do not pass user-supplied values to `<%= %>` without encoding.

---

### A13-8

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\rpt_dyn_driver_report.jsp`, lines 123–126, 188–189
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\rpt_dyn_seen_report.jsp`, lines 118–128
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\rpt_dyn_unit_report.jsp`, lines 125–128
**Severity:** High
**Category:** Reflected XSS / JavaScript Injection
**Description:** Request parameters `do_list`, `undo_list`, `sort_by`, `sort_asc`, `field_cd`, `field_nm`, and `refresh_page_url` are concatenated unescaped into JavaScript `onclick` handler strings within server-rendered HTML. An attacker can inject arbitrary JavaScript by supplying a value such as `','');alert(1)//` for any of these parameters.
**Evidence** (from `rpt_dyn_driver_report.jsp` lines 123–126):
```jsp
onclick="do_hide('<%=do_list %>','<%=field_cd %>','<%=field_nm %>','<%=undo_list %>',
    '<%=sort_by %>', '<%=sort_asc %>','<%=refresh_page_url %>');"
```
**Recommendation:** HTML-encode values placed inside HTML attributes using `encodeForHTMLAttribute()`, and JavaScript-encode values placed inside JavaScript string literals using `encodeForJavaScript()`. Both encodings are required when a value appears inside a JS string inside an HTML attribute. Alternatively, pass these values through a DOM-based approach (e.g. data attributes read by JavaScript) to avoid mixing contexts.

---

### A13-9

**File:** `C:\Projects\cig-audit\repos\fleetfocus\linde_reports\red_impact.jsp`, lines 58–65, 159–161
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\impact_by_unit_with_util.jsp`, lines 47–49, 62–64
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\preop_complete.jsp`, lines 63, 185–187
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\unit_utilisation.jsp`, lines 68–70, 196–199
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\util_driver_all_models.jsp`, lines 47–49, 86–88
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\util_driver_logon.jsp`, lines 47–49, 86–88
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\national_preop_checks.jsp`, lines 53–62
`C:\Projects\cig-audit\repos\fleetfocus\linde_reports\nat2_util_driver_all_models.jsp`, lines 53–62
**Severity:** High
**Category:** Stored XSS / JavaScript Injection via Database-Sourced Values
**Description:** Database-sourced strings (site names, model names, unit names, numeric counts) are concatenated without escaping directly into Highcharts JavaScript configuration objects that are rendered as inline `<script>` blocks. If a site name, model name, or unit name stored in the database contains a single-quote or JavaScript metacharacter, it will break out of the string literal and execute arbitrary JavaScript in every user's browser that views these report pages. Since these values originate from the database rather than the current request, this is a stored XSS vector.
**Evidence** (from `red_impact.jsp` line 160):
```jsp
'<%=siteList.get(i) %>' : 'style="font-size:12px;"',
```
From `impact_by_unit_with_util.jsp` lines 47–49:
```java
catString += "{"
    + "name : '"+modelList.get(k)+"',"
    + "categories : [ ";
```
**Recommendation:** All database-sourced strings injected into JavaScript contexts must be JavaScript-encoded before insertion. Use `ESAPI.encoder().encodeForJavaScript(value)` or equivalent. Alternatively, pass the data as JSON via a separate API call and parse it client-side, which avoids inline injection entirely.

---

### A13-10

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\mail_first.jsp`, line 152
`C:\Projects\cig-audit\repos\fleetfocus\au_email\xlsx_daily_veh_summary_input_mail.jsp`, lines 169–171
**Severity:** Medium
**Category:** Reflected XSS in Hidden Input Attributes
**Description:** Request parameters are reflected unescaped into HTML hidden input `value` attributes. In `mail_first.jsp`, the `url` parameter is reflected: `<input type="hidden" name="url" value="<%=url %>">`. In `xlsx_daily_veh_summary_input_mail.jsp`, `loc_nm`, `dept_nm`, and `cust` from the request are reflected. An attacker supplying `" onmouseover="alert(1)` as the value would break out of the attribute.
**Evidence** (`mail_first.jsp` line 152):
```jsp
<input type="hidden" name="url" value="<%=url %>">
```
`xlsx_daily_veh_summary_input_mail.jsp` lines 169–171:
```jsp
<input type="hidden" name="loc_nm" value="<%=loc_nm %>">
<input type="hidden" name="dept_nm" value="<%=dept_nm %>">
<input type="hidden" name="cust" value="<%=cust %>">
```
**Recommendation:** Encode all reflected values using `encodeForHTMLAttribute()` before inserting them into HTML attribute contexts.

---

### A13-11

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_vor_status_report.jsp`, lines 82–98
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_driver_report.jsp`, multiple table output lines
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_seen_report.jsp`, multiple table output lines
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_dyn_unit_report.jsp`, multiple table output lines
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_driver_league.jsp`, lines 109–116
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\print_driver_league.jsp`, multiple lines
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\email_vor_report.jsp`, multiple lines
**Severity:** Medium
**Category:** Reflected/Stored XSS via Unescaped DB Output in HTML
**Description:** Database-sourced strings (vehicle serial numbers, vehicle names, driver names, notes, model names, department names, date-time strings) are inserted directly into HTML table cells using `<%= %>` without HTML-encoding. While many of these values originate from the database rather than direct user input, any value that contains HTML-significant characters (`<`, `>`, `"`, `&`) will be rendered as markup. If an attacker can influence database content (e.g. by registering a vehicle with a name containing `<script>`), the injected content will execute in users' browsers when the report is emailed or printed.
**Evidence** (from `email_vor_status_report.jsp` lines 82–98):
```jsp
<td><%=vorStatusHireNo.get(i)%></td>
<td><%=vorStatusSerialNo.get(i)%></td>
<td><%=vorStatusModel.get(i)%></td>
<td><%=vorStatusName.get(i)%></td>
<td><%=vorStatusNote.get(i)%></td>
```
**Recommendation:** HTML-encode all database-sourced values before inserting them into HTML using `ESAPI.encoder().encodeForHTML(value)` or `StringEscapeUtils.escapeHtml4(value)`. Apply this consistently across all report output pages.

---

### A13-12

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\get_dept.jsp`, line 45
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\get_site.jsp`, line 45 (similar pattern)
**Severity:** Medium
**Category:** XML Injection via Unescaped DB Values
**Description:** Department codes and names from the database are concatenated directly into an XML string without XML-escaping. If a department name in the database contains `<`, `>`, `&`, or `"`, the resulting XML will be malformed or will inject content into the XML structure returned to the client.
**Evidence** (from `get_dept.jsp` line 45):
```java
resp = resp+"<rec>"+"<code>"+tmp+"</code><name>"+tmp1+"</name></rec>";
```
**Recommendation:** XML-encode all database values before inserting them into XML strings. Use `StringEscapeUtils.escapeXml11(value)` or an XML writer API (e.g. `XMLOutputFactory`) to produce well-formed XML rather than string concatenation.

---

### A13-13

**File:** `C:\Projects\cig-audit\repos\fleetfocus\dyn_report\mail_conf.jsp`, line 170
`C:\Projects\cig-audit\repos\fleetfocus\dyn_report\mail_first.jsp` (form element)
`C:\Projects\cig-audit\repos\fleetfocus\includes\report_nevigation.jsp`, line 91
`C:\Projects\cig-audit\repos\fleetfocus\includes\report_nevigation_keyword.jsp` (form element)
`C:\Projects\cig-audit\repos\fleetfocus\includes\report_nevigation_todate.jsp`, line 91
**Severity:** Medium
**Category:** Cross-Site Request Forgery (CSRF)
**Description:** Multiple POST forms do not include a synchroniser token or any other CSRF mitigation. An attacker can cause an authenticated user's browser to submit these forms from a malicious third-party page, triggering report subscriptions, email configuration changes, or report generation in the context of the victim's session. The `mail_conf.jsp` form POSTs to `../servlet/Frm_security` (line 170), and the navigation include forms POST to `../servlet/Frm_saveuser`.
**Evidence** (`mail_conf.jsp` line 170):
```html
<form method="post" action="../servlet/Frm_security">
```
`report_nevigation.jsp` line 91:
```html
<form method="post" action="../servlet/Frm_saveuser">
```
No `<input type="hidden" name="csrf_token" ...>` present in any of these forms.
**Recommendation:** Implement the synchroniser token pattern: generate a cryptographically random token per session, store it server-side, embed it as a hidden field in every state-changing form, and validate it in the servlet before processing the request. The Java ESAPI `CSRFGuard` library or Spring Security CSRF support provide ready-made implementations.

---

### A13-14

**File:** `C:\Projects\cig-audit\repos\fleetfocus\sess\Expire.jsp`, lines 10–29
**Severity:** Medium
**Category:** Incomplete Session Invalidation
**Description:** `Expire.jsp` is the shared authentication guard for the entire application. When a session is detected as expired or lacking the `user_cd` attribute, it forwards the user to the login page but does not call `session.invalidate()`. This means the server-side session object remains allocated and active. If an attacker has obtained a session ID (e.g. through a network sniff or XSS), they can continue using it until the container's idle timeout expires, even after the legitimate user has been redirected to the login page. Additionally, `jsp:forward` does not stop execution of code that follows the include in the parent page in all JSP container configurations, which may allow logic below the include to execute for invalid sessions.
**Evidence:**
```java
// sess/Expire.jsp lines 10–16: forward to login but no session.invalidate()
if (request.getSession(false) == null) {
%>
    <jsp:forward page="../pages/login.jsp">
        <jsp:param name="message" value="Session Expired. Kindly Re-login." />
    </jsp:forward>
<%
}
```
No `session.invalidate()` call anywhere in this file.
**Recommendation:** Call `request.getSession(false).invalidate()` before the `jsp:forward` to destroy the server-side session. After `jsp:forward`, add `return;` to prevent further execution in the calling JSP. Consider replacing `jsp:forward` with `response.sendRedirect()` (after invalidation) to prevent any possibility of continued execution.

---

### A13-15

**File:** `C:\Projects\cig-audit\repos\fleetfocus\exporter\users.jsp`, lines 13–113
`C:\Projects\cig-audit\repos\fleetfocus\exporter\vehicles.jsp`, lines 1–90
**Severity:** Medium
**Category:** Insecure Direct Object Reference / Tenant Data Isolation Risk
**Description:** Both export pages accept a `customer` request parameter and pass it to the filter bean alongside the session-scoped access controls. The session access controls (`access_cust`) are set, but the final data scoping depends entirely on the backend query implementation. If the backend query uses `customer` (from the request) as the primary customer filter and treats `access_cust` only as an additional restriction that can be bypassed when `access_level` is permissive, an authenticated user from customer A who manipulates the `customer` parameter to customer B's code may export customer B's user PII or vehicle data. The JSP-level code alone cannot confirm safe isolation.
**Evidence** (`users.jsp` lines 33–41):
```java
String access_level = (String)session.getAttribute("access_level");
String access_cust = (String)session.getAttribute("access_cust");
String access_site = (String)session.getAttribute("access_site");
String access_dept = (String)session.getAttribute("access_dept");
// ...
filter.setParam_Customer(customer); // customer from request.getParameter()
filter.setAccess_level(access_level);
filter.setAccess_cust(access_cust);
```
**Recommendation:** The backend query for `get_users_xls` and its vehicles equivalent must enforce `access_cust` as a mandatory filter that cannot be overridden by the `customer` parameter when the user's access level does not grant cross-customer access. Conduct a DAO-layer review of these named queries to confirm. At the JSP level, if `access_level` does not grant cross-customer access, validate that the requested `customer` value matches `access_cust` before proceeding.

---

### A13-16

**File:** `C:\Projects\cig-audit\repos\fleetfocus\linde_reports\linde_reports_subscription.jsp`, lines 43–49
**Severity:** Low
**Category:** Insufficient Input Validation (Date Format Check)
**Description:** The page calls `DataUtil.checkDateFormat(st_dt)` to validate the start date, but at line 92 it checks `!DataUtil.checkDateFormat(st_dt) || !DataUtil.checkDateFormat(st_dt)` — the second check is a duplicate of the first (both check `st_dt`) rather than checking `end_dt`. This means a malformed `end_dt` value passes the validation check and is used unchecked in downstream operations. While the primary issue on this page is command injection (A13-1), the date validation is additionally defective.
**Evidence:**
```java
if(!DataUtil.checkDateFormat(st_dt) || !DataUtil.checkDateFormat(st_dt)){
    // should be: !DataUtil.checkDateFormat(end_dt)
```
**Recommendation:** Correct the duplicate condition to check `end_dt` in the second branch: `!DataUtil.checkDateFormat(st_dt) || !DataUtil.checkDateFormat(end_dt)`. This is a secondary concern to A13-1 (command injection) which must be addressed first.

---

### A13-17

**File:** `C:\Projects\cig-audit\repos\fleetfocus\linde_reports\linde_reports_subscription.jsp`, lines 62–65
**Severity:** Informational
**Category:** Hardcoded Internal IP Address
**Description:** The Windows code path hardcodes the internal application server IP address `192.168.10.47:8090` in the command string. This reveals internal network topology and port information in the source code and would fail if the server is migrated.
**Evidence:**
```java
"cmd.exe", "/c", "cd D:\\MyFiles\\Work\\PanthomJs\\bin\\ && D: && phantomjs.exe "
    + " linde_charts.js "
    + " \"http://192.168.10.47:8090/fms/linde_reports/"+rpt_name+"..."
```
**Recommendation:** Move the internal URL to a configuration property (e.g. `RuntimeConf.emailurl` as used in the Linux path). Remove hardcoded IP addresses from source code.

---

## Summary Table

| ID | Severity | Category | File(s) |
|----|----------|----------|---------|
| A13-1 | Critical | OS Command Injection | linde_reports/linde_reports_subscription.jsp |
| A13-2 | Critical | Missing Authentication | linde_reports_subscription.jsp, red_impact.jsp, unit_utilisation.jsp, xlsx_daily_veh_summary_report_mail.jsp, email_dyn_unit_report_exc.jsp |
| A13-3 | Critical | Hardcoded Access Level Bypass | email_vor_status_report.jsp, email_dyn_driver_report.jsp, email_dyn_seen_report.jsp, email_dyn_unit_report.jsp, email_dyn_unit_report_exc.jsp, email_vor_report.jsp |
| A13-4 | High | Missing Access Control Scoping | excel_driver_league.jsp, email_driver_league.jsp, print_driver_league.jsp |
| A13-5 | High | Email Header Injection / SSRF | dyn_report/mail_report.jsp |
| A13-6 | High | Email Injection / Missing Auth | au_email/xlsx_daily_veh_summary_report_mail.jsp |
| A13-7 | High | Reflected XSS | dyn_report/mail_conf.jsp |
| A13-8 | High | Reflected XSS / JS Injection | rpt_dyn_driver_report.jsp, rpt_dyn_seen_report.jsp, rpt_dyn_unit_report.jsp |
| A13-9 | High | Stored XSS via DB Values in JS | 8 linde_reports/ chart pages |
| A13-10 | Medium | Reflected XSS in Hidden Inputs | mail_first.jsp, xlsx_daily_veh_summary_input_mail.jsp |
| A13-11 | Medium | Stored XSS via Unescaped DB Output | 7 email/print report pages |
| A13-12 | Medium | XML Injection | get_dept.jsp, get_site.jsp |
| A13-13 | Medium | CSRF | mail_conf.jsp, mail_first.jsp, report_nevigation*.jsp |
| A13-14 | Medium | Incomplete Session Invalidation | sess/Expire.jsp |
| A13-15 | Medium | Tenant Data Isolation Risk | exporter/users.jsp, exporter/vehicles.jsp |
| A13-16 | Low | Defective Input Validation | linde_reports/linde_reports_subscription.jsp |
| A13-17 | Info | Hardcoded Internal IP Address | linde_reports/linde_reports_subscription.jsp |

**Total findings: 17**
