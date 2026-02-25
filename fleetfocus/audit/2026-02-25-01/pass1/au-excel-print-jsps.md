# Security Audit — au_excel/ and au_print/ JSP Files
**Agent:** A16
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Scope:** All JSP files under `au_excel/` (33 files) and `au_print/` (29 files)

---

## Methodology

Each file was read in full. For each JSP the following were enumerated:

- `<%@ page import %>` directives
- All scriptlet blocks (`<% %>`) with line numbers and descriptions
- All expression outputs (`<%= %>`) noting whether the source is a request parameter, session attribute, or DB-sourced value
- All `<%@ include %>` and `<jsp:include>` directives
- `response.setContentType()` and `response.setHeader("Content-Disposition", ...)` calls

Security review categories applied:

1. Authorization / Data Scope — can a caller retrieve another customer's data by manipulating report parameters?
2. SQL Injection — unsanitized parameters passed to query execution
3. Cross-Site Scripting (XSS) — unescaped output in HTML or JavaScript contexts
4. CSV / Excel injection — formula-injectable values written to spreadsheet cells
5. Content-Type header correctness
6. Content-Disposition / filename injection
7. Session / authentication robustness

---

## File Inventory

### au_excel/ (33 files)

| File | Bean | op_code | Access control set |
|---|---|---|---|
| excel_hourmeter_exception.jsp | Databean_report | hour_exc | Yes |
| xlsx_battery_report.jsp | Databean_report | email_battery | Yes |
| xlsx_broadcastmsg_report.jsp | Databean_report | broadcastmsg_rpt | Yes |
| xlsx_cimplicity_shock_report.jsp | Databean_report | (XlsxCimplicityShockReport) | Yes |
| xlsx_cimplicity_util_report.jsp | Databean_report | (XlsxCimplicityUtilReport) | Yes |
| xlsx_curr_driv_report.jsp | Databean_report | curr_driv_report | Yes |
| **xlsx_curr_unit_report.jsp** | Databean_report | **NONE — commented out** | **NO** |
| xlsx_daily_driver_summary_report.jsp | Databean_report | daily_driv_sum | Yes |
| xlsx_daily_veh_summary_report.jsp | Databean_report | daily_veh_sum | Yes |
| xlsx_driver_access_abuse_report.jsp | Databean_report | driver_access_abuse | Yes |
| xlsx_driver_impact_report.jsp | Databean_report | impact_report | Yes |
| xlsx_dyn_driver_report.jsp | Databean_dyn_reports | dyn_driv_report | Yes |
| xlsx_dyn_seen_report.jsp | Databean_dyn_reports | dyn_seen_report | Yes |
| xlsx_dyn_transport_driver_report.jsp | Databean_dyn_reports | transport_driv_report | Yes |
| xlsx_dyn_unit_report.jsp | Databean_dyn_reports | dyn_unit_report | Yes |
| xlsx_exception_session_report.jsp | Databean_report | exception_session | Yes |
| xlsx_hire_dehire_report.jsp | Databean_report | hire_dehire_report | Yes |
| xlsx_impact_meter_report.jsp | Databean_report | impact_meter_report | Yes |
| xlsx_impact_report.jsp | Databean_report | impact_report | Yes |
| xlsx_key_hour_util_report.jsp | Databean_report | key_hour_util | Yes |
| xlsx_operational_status_report.jsp | Databean_report | operational_status | Yes |
| xlsx_preop_chk_fail_report.jsp | Databean_report | preop_chk_fail | Yes |
| xlsx_preop_chk_report.jsp | Databean_report | preop_chk | Yes |
| xlsx_preop_chk_report_orig_no_fitler.jsp | Databean_report | preop_chk | Yes |
| xlsx_restricted_access_usage_report.jsp | Databean_report | restricted_access | Yes |
| xlsx_seat_hour_util_report.jsp | Databean_report | seat_hour | Yes |
| xlsx_serv_maintenance_report.jsp | Databean_report | serv_maintenance | Yes |
| xlsx_spare_module.jsp | Databean_getter | spare_modules | Yes |
| xlsx_super_master_auth_report.jsp | Databean_report | super_master_auth | Yes |
| xlsx_unit_unlock_report.jsp | Databean_report | rpt_unlock | Yes |
| xlsx_utilisation_report.jsp | Databean_report | util_rpt | Yes |
| xlsx_util_wow_report.jsp | Databean_report | util_wow_dtl / email_util_wow | Yes |
| xlsx_vor_report.jsp | Databean_report | vor_report | Yes |

### au_print/ (29 files)

| File | Include chain | Session expiry guarded |
|---|---|---|
| print_battery.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_broadcastmsg.jsp | sess/Expire.jsp | Yes |
| print_curr_driv_report.jsp | sess/Expire.jsp | Yes |
| print_curr_unit_report.jsp | sess/Expire.jsp | Yes |
| print_daily_driver_summary.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_daily_veh_summary.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_driver_access_abuse.jsp | report_export_header.jsp, report_export_with_duration.jsp | Via header include |
| print_dyn_driver_report.jsp | report_export_header.jsp, report_export_keyword.jsp | Via header include |
| print_dyn_seen_report.jsp | report_export_header.jsp, report_export_keyword.jsp | Via header include |
| print_dyn_transport_driver_report.jsp | report_export_header.jsp, report_export_keyword_no_cust_site_dept.jsp | Via header include |
| print_dyn_unit_report.jsp | report_export_header.jsp, report_export_keyword.jsp | Via header include |
| print_exception_session_report.jsp | report_export_header.jsp, report_export_keyword_zlinde_opmode.jsp | Via header include |
| **print_hire_dehire_report.jsp** | **None** | **No** |
| print_hourmeter_exception.jsp | sess/Expire.jsp | Yes |
| print_impact_meter_report.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_impact_report.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_key_hour_util.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_operational_status_report.jsp | report_export_header.jsp, report_export_keyword_zlinde.jsp | Via header include |
| print_preop_chk.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_preop_chk_fail.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_preop_chk_inc.jsp | sess/Expire.jsp | Yes |
| print_seat_hour_util.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_serv_maintenance.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_shock_summary.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_unit_unlock.jsp | report_export_header.jsp | Via header include |
| print_util_summary.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_util_wow.jsp | sess/Expire.jsp | Yes |
| print_utilisation.jsp | report_export_header.jsp, report_export.jsp | Via header include |
| print_vor_report.jsp | report_export_header.jsp, report_export_keyword.jsp | Via header include |

---

## Findings

### A16-1 — Critical Authorization Bypass: Access Control Block Entirely Commented Out

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_excel\xlsx_curr_unit_report.jsp`
**Lines:** 29–57
**Severity:** Critical
**Category:** Authorization / Data Scope

**Description:**
The entire access-control block in `xlsx_curr_unit_report.jsp` has been commented out using `//` line comments. This includes the `op_code` assignment, all session attribute reads (`access_level`, `access_cust`, `access_site`, `access_dept`), the access-level parse, all `filter.set*` calls for the session scope, and the customer identifier assignment (`filter.setSet_cust_cd(cust_cd)`). As a result, `filter.init()` is called with none of the session-scoped constraints set. The filter bean's SQL query runs without any customer, site, department, or access-level restriction, returning data for all customers in the database.

Any authenticated session — regardless of what customer they belong to — can call this endpoint and receive the full current unit dataset across all customers.

**Evidence:**

```java
// File: xlsx_curr_unit_report.jsp, lines 29–57
// 	String op_code="curr_unit_report";
//
// 	// Session variables for the access level control
//
// 	String access_level = (String)session.getAttribute("access_level");
// 	String access_cust=(String)session.getAttribute("access_cust");
// 	String access_site=(String)session.getAttribute("access_site");
// 	String access_dept=(String)session.getAttribute("access_dept");
//
// 	if(access_level.equalsIgnoreCase(""))
// 	{
// 		access_level = "5";
// 	}
// 	int al = Integer.parseInt(access_level);
//
// 	filter.setAccess_level(access_level);
// 	filter.setAccess_cust(access_cust);
// 	filter.setAccess_site(access_site);
// 	filter.setAccess_dept(access_dept);
//
// 	//end of access level control
// 	filter.setSet_opcode(op_code);
// 	filter.setSet_gp_cd(gp_cd);
// 	filter.setSet_cust_cd(cust_cd);
// 	filter.setSt_dt(st_dt);
// 	filter.setEnd_dt(to_dt);
// 	filter.setSet_loc_cd(loc_cd);
// 	filter.setSet_dept_cd(dept_cd);
// 	filter.setSet_form_cd(form_cd);
```

`filter.init()` is then called at line 59 with no op_code, no access_cust, no access_level, and no customer ID set on the filter.

**Recommendation:**
Uncomment the access-control block immediately. Review git history to determine when the block was commented out and whether this was intentional (e.g., for debugging) or an accidental omission. After restoring the block, verify that the `filter.init()` call produces results scoped to the session's `access_cust` value. Add a unit test or integration test that asserts cross-customer data isolation on this endpoint.

---

### A16-2 — Reflected XSS: Request Parameter Directly Output in HTML

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_print\print_hire_dehire_report.jsp`
**Line:** 93
**Severity:** High
**Category:** Cross-Site Scripting (XSS)

**Description:**
The `search_crit` parameter is read directly from the HTTP request and written unescaped into the HTML response body inside a `<td>` element. An attacker can craft a URL containing a `search_crit` value with HTML or JavaScript payload (e.g., `<script>alert(1)</script>`) and send that URL to a logged-in user. When the user's browser loads the page, the injected script executes in the user's session context.

**Evidence:**

```java
// Line 11 — parameter read without sanitization
String search_crit = request.getParameter("search_crit")==null?"":request.getParameter("search_crit");

// Line 93 — direct unescaped output into HTML
<td><b><%=search_crit %></b></td>
```

This file also has no standard session-expiry or authentication include (it includes no `../sess/Expire.jsp` and no `../includes/report_export_header.jsp`), meaning it may be reachable without an active session check depending on container configuration.

**Recommendation:**
HTML-encode all request parameter values before output. Replace `<%=search_crit %>` with `<%=org.apache.commons.text.StringEscapeUtils.escapeHtml4(search_crit) %>` or an equivalent utility already used elsewhere in the codebase. Add the standard authentication include to this file.

---

### A16-3 — XSS via Request Parameters Injected into JavaScript Event Handler

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_print\print_dyn_driver_report.jsp`
**Line:** 156 (approximate — the `<th>` column header loop with onclick)
**Severity:** High
**Category:** Cross-Site Scripting (XSS)

**Description:**
The column-header rendering loop injects five request parameters directly into a JavaScript `onclick` attribute string without encoding: `do_list`, `field_cd` (DB-sourced field code), `field_nm` (DB-sourced field name), `undo_list`, `sort_by`, and `sort_asc`. The `do_list`, `undo_list`, `sort_by`, and `sort_asc` values come directly from `request.getParameter()`. An attacker can close the single-quoted JavaScript string literal, inject arbitrary JavaScript, and execute code in the victim's browser session.

**Evidence:**

```java
// Request parameter reads (top of scriptlet)
String do_list   = request.getParameter("do_list")==null?"":request.getParameter("do_list");
String undo_list = request.getParameter("undo_list")==null?"":request.getParameter("undo_list");
String sort_by   = request.getParameter("sort_by")==null?"":request.getParameter("sort_by");
String sort_asc  = request.getParameter("sort_asc")==null?"":request.getParameter("sort_asc");

// Column header output — all four injected into onclick attribute
<th><a href="#" onclick="do_hide('<%=do_list %>','<%=field_cd %>','<%=field_nm %>','<%=undo_list %>','<%=sort_by %>', '<%=sort_asc %>');"><%=field_nm %></a></th>
```

Injecting `','','');alert(document.cookie);//` into any of these parameters would execute arbitrary JavaScript.

The same pattern is present in `print_vor_report.jsp` which also reads `do_list`, `undo_list`, `sort_by`, `sort_asc` from request parameters and uses them in similar column-visibility logic (though `print_vor_report.jsp` does not appear to emit the onclick attribute itself, the tokenizer logic consuming the raw `do_list` string should still be reviewed).

**Recommendation:**
JavaScript-encode all values before embedding them in JavaScript string literals. Use `org.apache.commons.text.StringEscapeUtils.escapeEcmaScript()` or equivalent. Alternatively, pass the column-hide state via a data attribute and read it in a separate script block, eliminating inline event handlers entirely.

---

### A16-4 — Pervasive Unescaped DB-Sourced Output in HTML (Stored XSS Surface)

**Files:** All 29 `au_print/` JSP files
**Severity:** High
**Category:** Cross-Site Scripting (XSS) — Stored

**Description:**
Every `au_print/` page renders DB-sourced values directly into HTML using `<%= %>` expressions without HTML encoding. Any value stored in the database that contains HTML special characters (`<`, `>`, `"`, `&`, `'`) will be rendered literally by the browser. If any data-entry surface in the application allows a malicious user or device to inject HTML/script into fields such as vehicle name, driver name, model name, broadcast message text, or pre-operation check comments, those values will execute as script in every user's browser that views the affected report.

Representative unescaped expressions spanning multiple files:

| File | Expression | Data origin |
|---|---|---|
| print_battery.jsp | `<%=vunit_name.get(i) %>` | DB — vehicle name |
| print_battery.jsp | `<%=vdriver_name.get(i) %>` | DB — driver name |
| print_broadcastmsg.jsp | `<%=broadcastmsgBean.getText() %>` | Device/user-submitted message text |
| print_curr_driv_report.jsp | `<%=vdriv_nm.get(i) %>` | DB — driver name |
| print_curr_unit_report.jsp | `<%=vveh_nm.get(i) %>` | DB — vehicle name |
| print_dyn_driver_report.jsp | `<%=field_nm %>` in `<th>` | DB — field name |
| print_dyn_seen_report.jsp | `<%=veh_nm %>`, `<%=dnm %>` | DB — vehicle/driver |
| print_exception_session_report.jsp | `<%=field_nm %>` in `<th>` | DB — field name |
| print_hire_dehire_report.jsp | `<%=form_nm %>` | DB — report name |
| print_hourmeter_exception.jsp | `<%=vmachine_nm.get(i) %>` | DB — machine name |
| print_impact_report.jsp | `<%=location %>`, `<%=speed %>` | DB — JSON-parsed RTLS string |
| print_operational_status_report.jsp | `<%=result.getNote() %>` | DB — operator note |
| print_preop_chk.jsp | `<%=vfail_desc.get(i) %>` | DB — failure description |
| print_preop_chk_fail.jsp | `<%=filter.getPreOpCheckCommentList().get(i) %>` | DB — operator comment |
| print_preop_chk_inc.jsp | `<%=filter.getPreOpCheckCommentList().get(i) %>` | DB — operator comment |
| print_shock_summary.jsp | `<%=vuser_nm.get(i) %>`, `<%=vmachine_nm.get(i) %>` | DB — names |
| print_unit_unlock.jsp | `<%=vunit_loreason.get(i) %>`, `<%=vunit_unloreason.get(i) %>` | DB — reason text |
| print_utilisation.jsp | `<%=utilBean.getHire_no() %>`, `<%=utilBean.getModel_nm() %>` | DB — vehicle data |
| print_vor_report.jsp | `<%=dnm %>`, `<%=veh_nm %>`, `<%=mod_nm %>` | DB — names |

The broadcast message text (`print_broadcastmsg.jsp`) and pre-operation check comments (`print_preop_chk_fail.jsp`, `print_preop_chk_inc.jsp`) represent the highest-risk inputs because they accept free-form text submitted by operators or devices with minimal length constraints visible at this layer.

**Evidence (print_broadcastmsg.jsp):**

```java
// DB/device-sourced text output without encoding
<%=broadcastmsgBean.getText() %>
<%=broadcastmsgBean.getUnit() %>
<%=broadcastmsgBean.getDriver() %>
<%=broadcastmsgBean.getResponse() %>
```

**Evidence (print_preop_chk_fail.jsp):**

```java
// Free-text operator comment output without encoding
<%=filter.getPreOpCheckCommentList().get(i) %>
```

**Recommendation:**
Apply `StringEscapeUtils.escapeHtml4()` (Apache Commons Text) or JSTL `<c:out value="..."/>` to every `<%= %>` expression that outputs a DB-sourced or user-supplied string into an HTML context. Priority order: broadcast message text, pre-op check comments, failure descriptions, operator notes, then all remaining name/ID fields. Consider introducing a shared escaping utility method or a custom JSP tag to enforce consistent encoding across the codebase.

---

### A16-5 — Unescaped Broadcast Message Text

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_print\print_broadcastmsg.jsp`
**Lines:** Output expressions throughout the body loop
**Severity:** High
**Category:** Cross-Site Scripting (XSS) — Stored (elevated risk)

**Description:**
This finding is a specific high-priority instance within A16-4. Broadcast message text originates from forklift-mounted devices or operator consoles and is stored verbatim. It is output directly into HTML without encoding. Unlike vehicle names or model names (which are typically set by administrators), broadcast message content is submitted by device operators in the field and represents a realistic injection vector for an attacker with physical or network access to a fleet device.

**Evidence:**

```java
<%=broadcastmsgBean.getText() %>
<%=broadcastmsgBean.getType() %>
<%=broadcastmsgBean.getResponse() %>
<%=broadcastmsgBean.getDriver() %>
<%=broadcastmsgBean.getVeh_id() %>
```

**Recommendation:**
HTML-encode all fields from `broadcastmsgBean` before output. Validate and sanitize broadcast message text at the point of ingestion (device communication handler / DAO layer) in addition to encoding at output.

---

### A16-6 — Incorrect and Inconsistent Content-Type Headers on Excel Exports

**Files:**
- `xlsx_driver_impact_report.jsp` (lines 31 and 97)
- `xlsx_hire_dehire_report.jsp` (lines 30 and 91)
- `xlsx_impact_meter_report.jsp` (lines 32 and 107)
- `xlsx_impact_report.jsp` (lines 31 and 112)
- `excel_hourmeter_exception.jsp` (line 30)
- All remaining `xlsx_*.jsp` files set `application/x-download`

**Severity:** Low
**Category:** Content-Type Headers

**Description:**
Two distinct problems are present:

1. **Double Content-Type assignment.** Four files set `response.setContentType("application/vnd.ms-excel")` before the download try-block and then override it with `response.setContentType("application/x-download")` inside the try-block (or vice versa). The second call wins, but the intent is unclear and the pattern suggests copy-paste maintenance errors.

2. **Non-standard MIME type.** `application/x-download` is not a registered IANA MIME type. The correct types for Excel output are `application/vnd.ms-excel` (XLS) or `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (XLSX). Using `application/x-download` forces a download dialog in most browsers but provides no semantic information about the file type, and some security proxies may flag or block the response.

3. **HTML served as `application/vnd.ms-excel`.** `excel_hourmeter_exception.jsp` renders a full HTML table and sends it with `Content-Type: application/vnd.ms-excel`. This is an old technique to open HTML in Excel but it relies on Excel's tolerance for malformed input and is not a genuine Excel format.

**Evidence (double set — xlsx_driver_impact_report.jsp):**

```java
// Line 31
response.setContentType("application/vnd.ms-excel");
// ...
// Line 97 (inside try block)
response.setContentType("application/x-download");
```

**Recommendation:**
For genuine XLSX files (Apache POI output), use `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`. Set the Content-Type exactly once, before writing the response body. Remove the redundant earlier assignment. For `excel_hourmeter_exception.jsp`, either generate a genuine XLSX file using POI (consistent with the rest of the codebase) or document the HTML-as-Excel approach explicitly. Add `response.setHeader("X-Content-Type-Options", "nosniff")` to prevent browser MIME-type sniffing.

---

### A16-7 — HTML-as-Excel Export with Unescaped DB Values

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_excel\excel_hourmeter_exception.jsp`
**Lines:** Throughout the HTML table body
**Severity:** Medium
**Category:** Cross-Site Scripting (XSS) / Content-Type

**Description:**
`excel_hourmeter_exception.jsp` is an old-style HTML-to-Excel export: it renders a full HTML page, sets `Content-Type: application/vnd.ms-excel`, and relies on Excel opening the HTML. The page outputs multiple DB-sourced values without HTML encoding into the HTML response. Although the primary consumer is Excel (which does not execute embedded scripts in the same way a browser does), the response is still a valid HTML document. If a browser is directed to this URL (e.g., via a direct navigation or a link), it renders as HTML and the unescaped values constitute stored XSS in a browser context.

Additionally, the hidden form field at the bottom of the page outputs `form_cd` directly from the request parameter without encoding:

```java
<input type="hidden" name="form_cd" value="<%=form_cd %>"/>
```

This is an attribute-context injection point: if `form_cd` contains `"` or `>`, the HTML attribute is broken.

**Evidence:**

```java
// DB values output unescaped into HTML
<%=vmachine_nm.get(i) %>
<%=sm_hour_meter_ts.get(i) %>
<%=sm_hour_meter.get(i) %>
<%=get_user %>
<%=get_loc %>
<%=get_dep %>
<%=form_nm %>
<%=to_dt %>

// Request parameter in HTML attribute (line near bottom)
<input type="hidden" name="form_cd" value="<%=form_cd %>"/>
```

**Recommendation:**
Convert this export to a genuine XLSX file using the existing Apache POI infrastructure already used by the other `xlsx_*.jsp` files. This eliminates both the content-type confusion and the HTML injection surface. If the HTML-as-Excel approach must be retained, apply `StringEscapeUtils.escapeHtml4()` to all output expressions and use `escapeHtml4(form_cd)` in the hidden input value attribute.

---

### A16-8 — Request Parameter `form_cd` Output Unescaped in Hidden Input Attribute

**Files:**
- `excel_hourmeter_exception.jsp` (line near end of file)
- `print_curr_driv_report.jsp`
- `print_curr_unit_report.jsp`
- `print_util_wow.jsp` (line 186)

**Severity:** Low
**Category:** Cross-Site Scripting (XSS)

**Description:**
Several files echo the `form_cd` request parameter directly into an HTML `<input>` element's `value` attribute without HTML-encoding:

```java
<input type="hidden" name="form_cd" value="<%=form_cd %>"/>
```

If `form_cd` contains a double-quote character, the attribute boundary is broken, allowing injection of additional HTML attributes or closing the tag and injecting new elements. In practice `form_cd` appears to be a numeric or short-code identifier controlled by the application's own UI, so exploitation requires either a compromised form or a crafted URL. However, the pattern is inconsistent with secure-by-default output handling.

**Evidence (print_util_wow.jsp line 186):**

```java
<input type="hidden" name="form_cd" value="<%=form_cd %>"/>
```

**Recommendation:**
Encode the attribute value: `value="<%=StringEscapeUtils.escapeHtml4(form_cd) %>"`. Apply consistently to all hidden fields that echo request parameters.

---

### A16-9 — No JSP-Layer Validation of Customer ID Parameter Against Session

**Files:** All 62 JSP files in au_excel/ and au_print/
**Severity:** Medium
**Category:** Authorization / Data Scope

**Description:**
Every file reads a customer identifier (`user_cd` or `cust_cd`) from the HTTP request parameter and passes it directly to the filter bean via `filter.setSet_cust_cd(user_cd)`. The session's `access_cust` value is also set on the filter (`filter.setAccess_cust(access_cust)`), but there is no JSP-layer assertion that `user_cd == access_cust` (or that `user_cd` is within the set of customers permitted by the session).

The practical data-scope enforcement relies entirely on the filter bean's internal SQL logic correctly intersecting the supplied `user_cd` with the session's `access_cust`. If the SQL in the bean has a path where `access_cust` is ignored (e.g., when `access_level` is low, i.e., high-privilege), a high-privilege user who knows another customer's code could specify an arbitrary `user_cd` and retrieve that customer's data.

This is a defence-in-depth gap: the JSP layer should fail fast if `user_cd` from the request does not match the session's permitted customer scope, rather than delegating all enforcement to the bean layer.

**Evidence (representative — xlsx_battery_report.jsp):**

```java
// Request parameter — caller-supplied
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");

// Session attribute — server-controlled
String access_cust = (String)session.getAttribute("access_cust");

// Both set on filter — no JSP-layer comparison performed
filter.setAccess_cust(access_cust);
filter.setSet_cust_cd(cust_cd);   // no check: cust_cd == access_cust?

filter.init();
```

**Recommendation:**
Add an explicit check in each JSP (or in the shared include header) before calling `filter.init()`:

```java
if (!cust_cd.isEmpty() && !cust_cd.equals(access_cust) && al > 3) {
    // al > 3 means non-admin; admins legitimately access any customer
    response.sendError(HttpServletResponse.SC_FORBIDDEN);
    return;
}
```

Alternatively, enforce this logic in the filter bean's `init()` method so that it is guaranteed regardless of the calling JSP. Document the intended access model (which `access_level` values permit cross-customer access) and ensure it is tested.

---

### A16-10 — Potential NullPointerException on Unauthenticated Access (Missing Session Null Check)

**Files:** All au_excel/ and au_print/ JSP files that read session attributes
**Severity:** Medium
**Category:** Authorization / Authentication Robustness

**Description:**
Every file reads session attributes as follows:

```java
String access_level = (String)session.getAttribute("access_level");
// ...
if(access_level.equalsIgnoreCase(""))
```

If a request arrives without a valid session (e.g., the session has expired and the session-expiry redirect has not fired, or the file is accessed directly without a valid container session), `session.getAttribute("access_level")` returns `null`. The subsequent call to `access_level.equalsIgnoreCase("")` throws a `NullPointerException`. The exception propagates as an HTTP 500 error rather than a redirect to the login page.

In the au_print/ files that include `../sess/Expire.jsp`, the null-check / redirect is expected to be handled by that include. However, files such as `print_hire_dehire_report.jsp` do not include `../sess/Expire.jsp` or the standard `report_export_header.jsp`, and therefore have no session-expiry protection at all.

**Evidence:**

```java
// xlsx_battery_report.jsp (representative of all files)
String access_level = (String)session.getAttribute("access_level");
// access_level could be null if session is new or expired
if(access_level.equalsIgnoreCase(""))  // NullPointerException if null
{
    access_level = "5";
}
```

**Evidence (print_hire_dehire_report.jsp — no session expiry include):**

```jsp
<%-- No <%@ include file="../sess/Expire.jsp"%> present --%>
<%-- No <%@ include file="../includes/report_export_header.jsp"%> present --%>
```

**Recommendation:**
Add a null check before dereferencing `access_level`:

```java
if (access_level == null || access_level.equalsIgnoreCase("")) {
    response.sendRedirect("../login.jsp");
    return;
}
```

Alternatively, centralise this logic in a JSP include or a servlet filter (a `javax.servlet.Filter`) that intercepts all requests to `au_excel/` and `au_print/` and redirects unauthenticated requests to the login page before the JSP scriptlet runs. Add the standard authentication include to `print_hire_dehire_report.jsp`.

---

### A16-11 — Content-Disposition Filename Derived from Bean Method with Potential User-Controlled Input

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_excel\xlsx_cimplicity_shock_report.jsp`
**Line:** 85
**Severity:** Low
**Category:** Content-Disposition / Header Injection

**Description:**
The Content-Disposition header is constructed by concatenating the result of `xlsxReport.getTitle()` directly into the header string:

```java
response.setHeader("Content-Disposition", "attachment;filename=" + xlsxReport.getTitle() + ".xlsx");
```

If `getTitle()` returns a value that incorporates user-supplied or DB-stored data (e.g., a customer name or site name embedded in the report title), and if that value contains newline characters (`\r` or `\n`), an attacker who can control the title could inject additional HTTP response headers (HTTP header injection / response splitting). While modern servlet containers strip newlines from header values, this is a container-dependent mitigation and should not be relied upon.

The majority of other files use `xlsx.getFileName()` which is presumably set by the report object to a safe, fixed string; this file deviates by using `getTitle()`.

**Evidence:**

```java
// xlsx_cimplicity_shock_report.jsp line 85
response.setHeader("Content-Disposition", "attachment;filename=" + xlsxReport.getTitle() + ".xlsx");
```

**Recommendation:**
Sanitize the filename before embedding it in the header: strip or encode any characters outside the alphanumeric, hyphen, underscore, and dot set. Wrap the filename in double quotes per RFC 6266: `"attachment; filename=\"" + safeName + "\""`. Alternatively, use a fixed filename for this report, as is done for other exports via `xlsx.getFileName()`.

---

### A16-12 — Duplicate/Redundant JSP File with Disabled Filter Logic

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_excel\xlsx_preop_chk_report_orig_no_fitler.jsp`
**Severity:** Informational
**Category:** Code Hygiene / Attack Surface

**Description:**
A file named `xlsx_preop_chk_report_orig_no_fitler.jsp` (note the deliberate misspelling "fitler" in the filename and "orig" prefix) is present in `au_excel/`. The name implies it is an original or unfiltered copy of `xlsx_preop_chk_report.jsp` that was retained for reference or debugging. If this file is accessible via the web container, it represents an additional endpoint that may have different filtering behaviour than the production file.

The file uses the same `op_code="preop_chk"` and session access-control block as the production file, so the immediate data-scope risk appears equivalent. However, the presence of debug/backup JSPs in the web root is a maintenance and security hygiene concern: future modifications to the production file may not be replicated to this copy, leaving it with stale or weaker access controls over time.

**Evidence:**

```
File path: au_excel/xlsx_preop_chk_report_orig_no_fitler.jsp
op_code: preop_chk (same as xlsx_preop_chk_report.jsp)
```

**Recommendation:**
Remove `xlsx_preop_chk_report_orig_no_fitler.jsp` from the web root. If historical reference is needed, preserve it in version control but exclude it from the deployed artifact using `.war` build exclusion rules or a servlet mapping that returns 404 for the `*_orig_*` pattern.

---

### A16-13 — Double Invocation of filter.init() in Single Request

**File:** `C:\Projects\cig-audit\repos\fleetfocus\au_excel\xlsx_util_wow_report.jsp`
**Severity:** Low
**Category:** Logic / Correctness

**Description:**
`xlsx_util_wow_report.jsp` calls `filter.init()` twice within the same request: once for `op_code="util_wow_dtl"` and a second time for `op_code="email_util_wow"`. Each `init()` call executes database queries. If the filter bean is stateful and the second `init()` overwrites result sets from the first, data from the first query may be lost or replaced with incorrect values before it is consumed. If both sets of results are needed, the second `init()` call on the same bean object is a fragile pattern — a refactoring that changes the bean's state management could silently corrupt the report output.

**Evidence:**

```java
filter.setSet_opcode("util_wow_dtl");
filter.init();   // first query

// ... result collection ...

filter.setSet_opcode("email_util_wow");
filter.init();   // second query on same bean
```

**Recommendation:**
Extract each logical operation into a distinct bean instance, or refactor the bean to support multiple named result sets without overwriting state between calls. Document the intended interaction between the two `init()` calls.

---

## Summary Table

| ID | File(s) | Severity | Category | One-line description |
|---|---|---|---|---|
| A16-1 | xlsx_curr_unit_report.jsp | **Critical** | Authorization | Entire access-control block commented out; filter runs without any data-scope constraint |
| A16-2 | print_hire_dehire_report.jsp:93 | High | XSS (Reflected) | `search_crit` request parameter output unescaped into HTML |
| A16-3 | print_dyn_driver_report.jsp | High | XSS (Reflected) | `do_list`, `undo_list`, `sort_by`, `sort_asc` injected unescaped into JavaScript onclick attribute |
| A16-4 | All 29 au_print/ files | High | XSS (Stored) | Pervasive unescaped DB-sourced output across all print pages |
| A16-5 | print_broadcastmsg.jsp | High | XSS (Stored) | Broadcast message text (device/operator-controlled) output unescaped into HTML |
| A16-6 | xlsx_driver_impact_report.jsp, xlsx_hire_dehire_report.jsp, xlsx_impact_meter_report.jsp, xlsx_impact_report.jsp, excel_hourmeter_exception.jsp | Low | Content-Type | Double Content-Type assignment; use of non-standard `application/x-download` |
| A16-7 | excel_hourmeter_exception.jsp | Medium | XSS / Content-Type | HTML-as-Excel export with unescaped DB values; accessible as HTML in browser |
| A16-8 | excel_hourmeter_exception.jsp, print_curr_driv_report.jsp, print_curr_unit_report.jsp, print_util_wow.jsp | Low | XSS | `form_cd` request parameter echoed unescaped into hidden input value attribute |
| A16-9 | All 62 JSP files | Medium | Authorization | No JSP-layer check that caller-supplied `user_cd`/`cust_cd` matches session `access_cust` |
| A16-10 | All JSP files; critical in print_hire_dehire_report.jsp | Medium | Authentication | `session.getAttribute("access_level")` not null-checked before dereferencing; no session-expiry include in print_hire_dehire_report.jsp |
| A16-11 | xlsx_cimplicity_shock_report.jsp:85 | Low | Header Injection | Content-Disposition filename constructed from `xlsxReport.getTitle()` without sanitization |
| A16-12 | xlsx_preop_chk_report_orig_no_fitler.jsp | Info | Code Hygiene | Debug/backup JSP file with misleading name present in web root |
| A16-13 | xlsx_util_wow_report.jsp | Low | Logic | `filter.init()` called twice on same bean instance in one request with different op_codes |

**Total findings: 13**
**Critical: 1 | High: 4 | Medium: 2 | Low: 5 | Informational: 1**
