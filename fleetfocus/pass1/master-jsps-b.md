# Security Audit Report — master/ JSP Files (Batch B)
**Agent:** A12b
**Repository:** ff-new
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Audit Run:** 2026-02-25-01
**Date:** 2026-02-25
**Output:** C:\Projects\cig-audit\repos\fleetfocus\audit\2026-02-25-01\pass1\master-jsps-b.md

---

## Scope

This report covers JSP files in `master/` that were **not** audited by agent A12a. The A12a exclusion list is:

chk_dup_acode.jsp, chk_dup_card.jsp, copy_site_hour_settings.jsp, edit_dept_name.jsp, edit_site_address.jsp, edit_site_name.jsp, existing_alert_lst.jsp, existing_alert_lst_admin.jsp, existing_cust_vehicle_lst.jsp, existing_customer_lst.jsp, existing_driver_lst.jsp, existing_opchk_lst.jsp, existing_user_lst.jsp, existing_vehicle_lst.jsp, existing_vehicle_lst_prod.jsp, existing_vehicle_lst_serv.jsp, frm_access_customer.jsp, frm_alert_add.jsp, frm_alert_add1.jsp, frm_blacklist_driv.jsp, frm_conf_driv_setting.jsp, frm_conf_driv_setting_wol.jsp, frm_conf_firmware_display.jsp, frm_conf_firmware_upg.jsp, frm_conf_firmware_upg_bean.jsp, frm_conf_machine_setting.jsp, frm_conf_machine_upg.jsp, frm_conf_maint_setting.jsp, frm_conf_shocks_settings.jsp, frm_customer_dept_rel.jsp

**Files audited in this batch (56 files):**

| # | File |
|---|------|
| 1 | frm_customer_rel.jsp |
| 2 | frm_customer_vehicle_rel.jsp |
| 3 | frm_customer_vehicle_reset.jsp |
| 4 | frm_fc_vehicle_conf.jsp |
| 5 | frm_fc_vehicle_lst.jsp |
| 6 | frm_group_loc_rel.jsp |
| 7 | frm_hourcount_config.jsp |
| 8 | frm_impact_setting.jsp |
| 9 | frm_io_setting.jsp |
| 10 | frm_mastercode.jsp |
| 11 | frm_mastercode_40slots.jsp |
| 12 | frm_mastercode_step2.jsp |
| 13 | frm_new_branch.jsp |
| 14 | frm_new_branch_old.jsp |
| 15 | frm_new_customer.jsp |
| 16 | frm_new_department.jsp |
| 17 | frm_new_department_win.jsp |
| 18 | frm_new_division.jsp |
| 19 | frm_new_driver.jsp |
| 20 | frm_new_group.jsp |
| 21 | frm_new_location.jsp |
| 22 | frm_new_question.jsp |
| 23 | frm_new_user.jsp |
| 24 | frm_new_vehicle.jsp |
| 25 | frm_new_vehicle1.jsp |
| 26 | frm_new_vehicle_short.jsp |
| 27 | frm_new_vehicle_type.jsp |
| 28 | frm_new_vehicle_type_pop.jsp |
| 29 | frm_override_codes.jsp |
| 30 | frm_repl_vehiclemod.jsp |
| 31 | frm_send_canbus_rules.jsp |
| 32 | frm_sendmsg.jsp |
| 33 | frm_service_flag.jsp |
| 34 | frm_service_status.jsp |
| 35 | frm_setup_driver.jsp |
| 36 | frm_site_hours.jsp |
| 37 | frm_upload_questions.jsp |
| 38 | frm_vehicle_prod.jsp |
| 39 | get_assigned_vehicle.jsp |
| 40 | get_codes.jsp |
| 41 | get_customer.jsp |
| 42 | get_cust_vehicle.jsp |
| 43 | get_customergp.jsp |
| 44 | get_dept.jsp |
| 45 | get_driver.jsp |
| 46 | get_impact.jsp |
| 47 | get_mst_cd_exist.jsp |
| 48 | get_mst_cd_like.jsp |
| 49 | get_site.jsp |
| 50 | get_unassigned_vehicle.jsp |
| 51 | get_user.jsp |
| 52 | get_vehicle.jsp |
| 53 | get_vehicle_dept.jsp |
| 54 | pic_upload_logo.jsp |
| 55 | register.jsp |
| 56 | rpt_preop_unsync_qustion.jsp |
| 57 | update_all_user_weigand.jsp |

---

## Security Checklist Applied

For each file the following checks were applied:

1. **XSS** — Unescaped `<%= %>` output in HTML body, HTML attribute, or JavaScript context
2. **SQL Injection** — String concatenation in query construction (all queries are bean-delegated; no direct SQL found in JSPs)
3. **Authentication** — Presence of `<%@ include file="../sess/Expire.jsp" %>`
4. **CSRF** — Presence of anti-CSRF token on state-changing forms
5. **IDOR** — Record IDs (usr_cd, veh_cd, chk_cd, etc.) taken from request parameters without session ownership validation
6. **File Upload** — Client-side-only extension check, missing server-side validation
7. **File Inclusion** — Dynamic include directives using user-controlled values

---

## Findings

---

### A12b-1

**File:** `master/frm_customer_rel.jsp`, line 453
**Severity:** High
**Category:** XSS — Reflected Request Parameter in HTML Body
**Description:** The `message` parameter is taken directly from `request.getParameter("message")` and rendered into HTML without any encoding. An attacker who can control the redirect URL (e.g., via a CSRF attack that triggers a server redirect with a malicious `message` value) can inject arbitrary HTML/JavaScript into the page.
**Evidence:**
```java
String message=request.getParameter("message")==null?"":request.getParameter("message");
```
```jsp
<%=message %>
```
This pattern (`<%=message %>` where `message` is a raw request parameter) appears in every form page in this batch. The finding is catalogued once here; all occurrences are listed under A12b-2.
**Recommendation:** HTML-encode all user-controlled values before rendering: use `ESAPI.encoder().encodeForHTML(message)` or equivalent. Do not reflect request parameters directly into HTML output.

---

### A12b-2

**File:** All form JSPs — see list below
**Severity:** High
**Category:** XSS — Reflected `message` Request Parameter (Widespread)
**Description:** Every form page in this batch reflects the `message` request parameter raw into HTML. The full list of affected files and lines:

| File | Line |
|------|------|
| frm_customer_rel.jsp | 453 |
| frm_customer_vehicle_rel.jsp | 450 |
| frm_customer_vehicle_reset.jsp | 509 |
| frm_fc_vehicle_conf.jsp | 476 |
| frm_fc_vehicle_lst.jsp | 518 |
| frm_group_loc_rel.jsp | 121 |
| frm_hourcount_config.jsp | 395 |
| frm_impact_setting.jsp | 823 |
| frm_io_setting.jsp | 278 |
| frm_mastercode_step2.jsp | 453 |
| frm_new_branch.jsp | 163 |
| frm_new_branch_old.jsp | 147 |
| frm_new_customer.jsp | 320 |
| frm_new_department.jsp | 143 |
| frm_new_department_win.jsp | 100 |
| frm_new_division.jsp | 143 |
| frm_new_driver.jsp | 907 |
| frm_new_group.jsp | 207 |
| frm_new_location.jsp | 199 |
| frm_new_question.jsp | 163 |
| frm_new_user.jsp | 1013 |
| frm_new_vehicle.jsp | 266 |
| frm_new_vehicle1.jsp | 302 |
| frm_new_vehicle_short.jsp | 243 |
| frm_new_vehicle_type.jsp | 142 |
| frm_new_vehicle_type_pop.jsp | 106 |
| frm_override_codes.jsp | 607 |
| frm_repl_vehiclemod.jsp | 121 |
| frm_send_canbus_rules.jsp | 115 |
| frm_service_flag.jsp | (no explicit message output found; message param read but not displayed) |
| frm_service_status.jsp | 264 |
| frm_setup_driver.jsp | 274 |
| frm_site_hours.jsp | 459 |
| frm_upload_questions.jsp | 249 |
| frm_vehicle_prod.jsp | 179 |
| pic_upload_logo.jsp | 76 |

**Recommendation:** Apply `encodeForHTML()` to all `message` parameter outputs across the codebase. A global search-and-replace of the pattern `<%=message %>` where `message` derives from `request.getParameter` should be performed.

---

### A12b-3

**File:** `master/frm_customer_rel.jsp`, lines 493–501
**Severity:** High
**Category:** XSS — DB Values Interpolated Raw into Inline JavaScript Event Handler
**Description:** Site names, addresses, and status codes retrieved from the database are interpolated directly into `onclick` attribute strings without JavaScript encoding. If any DB value contains a single quote, closing parenthesis, or other JavaScript metacharacter (possible through stored XSS injection at data-entry time, or through a compromised data source), this results in JS injection.
**Evidence:**
```jsp
onclick="open_name_edit('<%=Vcust_rel_cd.get(i) %>','<%=Vcust_rel_usr.get(i) %>','<%=Vcust_rel_usr_st.get(i) %>');"
onclick="open_addr_edit('<%=Vcust_rel_cd.get(i) %>','<%=Vcust_rel_addr.get(i) %>','<%=Vcust_rel_usr.get(i) %>','<%=Vcust_rel_usr_st.get(i) %>')"
```
**Recommendation:** Encode DB values for the JavaScript string context using `ESAPI.encoder().encodeForJavaScript()` before interpolating into inline event handlers. Consider moving to unobtrusive event handling patterns (e.g., data attributes + addEventListener) to avoid inline JS altogether.

---

### A12b-4

**File:** `master/frm_new_driver.jsp`, line 695; `master/frm_new_user.jsp`, line 767
**Severity:** High
**Category:** XSS — Multiple DB Values in `onload` JavaScript Call
**Description:** Multiple DB-sourced values (user group, status, driver flag, customer code, site code, department code, access level, ID type, expiry) are interpolated raw into a `<body onload="set(...)">` call. Any DB value containing a single quote or JavaScript special character produces a JS injection vector (stored XSS).
**Evidence (frm_new_driver.jsp line 695):**
```jsp
<body onload="set('<%=usr_gp %>','<%=usr_status %>','<%=isdriver %>','<%=u_cust_cd %>',
'<%=u_site_cd %>','<%=u_dept_cd %>','<%=u_al %>','<%=idtype%>','<%=hidtype%>','<%=usr_expiry%>');">
```
**Evidence (frm_new_user.jsp line 767):** Identical pattern.
**Recommendation:** Apply `encodeForJavaScript()` to every value interpolated into JS string literals in event handler attributes. Alternatively, write JS values to a JSON object in the page `<head>` (inside a `<script>` block with `encodeForHTML`-encoded output) and read from that object in the event handler.

---

### A12b-5

**File:** `master/frm_new_customer.jsp`, line 310
**Severity:** Medium
**Category:** XSS / Path Traversal — DB Filename in `img src` Attribute
**Description:** A filename stored in the database (`mach_pic`) is written directly into an `<img src>` attribute without encoding. If the value contains `"` or `>`, it can break out of the attribute. Additionally, since the path is `../images/pics/<%=mach_pic %>`, a DB value containing `../` sequences could potentially reference unintended server files (path traversal in the URL).
**Evidence:**
```jsp
<img src="../images/pics/<%=mach_pic %>" .../>
```
**Recommendation:** Validate `mach_pic` against an allowlist of safe filenames (alphanumeric, dot, underscore only) before storing to DB and before rendering. HTML-encode the value on output: `encodeForHTMLAttribute(mach_pic)`.

---

### A12b-6

**File:** `master/frm_new_user.jsp`, lines 942 and 946
**Severity:** Critical
**Category:** Plaintext Password Exposure
**Description:** The user's password is fetched from the database and pre-populated into both the `password` and `confirm password` fields as plaintext `value` attributes in HTML. This means the password is transmitted to the browser in plaintext in the page source, visible via View Source, browser developer tools, proxy logs, and browser autofill history. This indicates passwords are stored in recoverable (plaintext or reversibly-encrypted) form in the database, which is itself a critical finding.
**Evidence:**
```jsp
<input type="password" name="pass" ... value="<%=usr_pwd %>">
<input type="password" name="pass1" ... value="<%=usr_pwd %>">
```
**Recommendation:** Passwords must be hashed using a strong one-way hash (bcrypt, scrypt, or Argon2). They must never be read back from the database and displayed to any user. When editing a user, leave the password fields empty; only update the password hash if the admin enters a new value.

---

### A12b-7

**File:** `master/frm_new_driver.jsp`, line 14; `master/frm_new_user.jsp`, line 14
**Severity:** High
**Category:** Supply-Chain / Integrity — External Script Loaded over HTTP
**Description:** Both files load jQuery UI from an external CDN over plain HTTP (not HTTPS). This allows a man-in-the-middle attacker on any network path between the user's browser and the CDN to replace the jQuery UI library with malicious JavaScript, achieving full script execution in the user's browser.
**Evidence:**
```html
<script language="javascript" src="http://code.jquery.com/ui/1.8.21/jquery-ui.min.js"></script>
```
Additionally, jQuery UI 1.8.21 is from 2012 and contains multiple known security vulnerabilities.
**Recommendation:** Remove the external CDN dependency. Bundle the jQuery UI library locally within the application and serve it over HTTPS. Upgrade to a current, supported version.

---

### A12b-8

**File:** `master/frm_customer_rel.jsp`, line 325
**Severity:** Low
**Category:** Information Disclosure — Debug Code Left in Production
**Description:** A jQuery debug alert statement that serializes and displays all form data is present in production code.
**Evidence:**
```javascript
alert($(this).serialize());
```
**Recommendation:** Remove all `alert()` debug calls from production code. Implement a code review or pre-commit hook to detect and block debug output statements.

---

### A12b-9

**File:** All state-changing form JSPs (full list below)
**Severity:** High
**Category:** CSRF — Missing Anti-CSRF Token on All State-Changing Forms
**Description:** Every form in this batch that POSTs to `../servlet/Frm_saveuser` contains no anti-CSRF token. An attacker can craft a page that silently submits any of these forms using the victim's active session, causing unauthorized state changes (creating/editing users, drivers, vehicles, customers, vehicle assignments, password changes, etc.).

Affected files (all POST to `../servlet/Frm_saveuser` with no CSRF token):

| File | op_code |
|------|---------|
| frm_customer_rel.jsp | customer_rel |
| frm_customer_vehicle_rel.jsp | customer_veh_rel |
| frm_customer_vehicle_reset.jsp | customer_veh_reset |
| frm_fc_vehicle_conf.jsp | (various) |
| frm_group_loc_rel.jsp | group_rel_add |
| frm_hourcount_config.jsp | update_contracthour |
| frm_impact_setting.jsp | impact_set |
| frm_io_setting.jsp | (various) |
| frm_mastercode_step2.jsp | mastercode_add |
| frm_new_branch.jsp | branch_add |
| frm_new_branch_old.jsp | branch_add |
| frm_new_customer.jsp | customer_add |
| frm_new_department.jsp | dept_add |
| frm_new_department_win.jsp | dept_add |
| frm_new_division.jsp | division_add |
| frm_new_driver.jsp | driver_add |
| frm_new_group.jsp | group_add |
| frm_new_location.jsp | location_add |
| frm_new_question.jsp | question_add |
| frm_new_user.jsp | user_add |
| frm_new_vehicle.jsp | vehicle_add |
| frm_new_vehicle1.jsp | vehicle_add1 |
| frm_new_vehicle_short.jsp | vehicle_add |
| frm_new_vehicle_type.jsp | vehicle_type_add |
| frm_new_vehicle_type_pop.jsp | vehicle_type_add |
| frm_override_codes.jsp | override_add |
| frm_repl_vehiclemod.jsp | mod_repl |
| frm_send_canbus_rules.jsp | send_canbus_rules |
| frm_sendmsg.jsp | send_outmsg |
| frm_service_flag.jsp | delete_reminder / add_reminder |
| frm_service_status.jsp | service_update |
| frm_setup_driver.jsp | driver_setup |
| frm_site_hours.jsp | updateHours |
| frm_upload_questions.jsp | question_upload |
| frm_vehicle_prod.jsp | vehicle_prod |
| pic_upload_logo.jsp | upload |
| update_all_user_weigand.jsp | update_weigand |
| rpt_preop_unsync_qustion.jsp | (read-only display but form present) |

**Recommendation:** Implement the Synchronizer Token Pattern: generate a cryptographically random per-session CSRF token, store it in the session, embed it as a hidden field in every form, and validate it in `Frm_saveuser` before processing any state-changing operation. Alternatively, implement the Double Submit Cookie pattern or use framework-provided CSRF protection (e.g., Spring Security CSRF).

---

### A12b-10

**File:** All `get_*.jsp` AJAX data endpoints (14 files)
**Severity:** High
**Category:** Authentication — Missing Session Enforcement on AJAX Data Endpoints
**Description:** All AJAX data-fetching endpoints in the `master/` directory lack the session enforcement include (`../sess/Expire.jsp`). These endpoints return sensitive organizational data (customer names and codes, site names, driver names and card IDs, vehicle serial numbers and fleet numbers, department names, impact settings, mastercode slot assignments) to any unauthenticated HTTP client.

Affected files:

| File | Data Returned |
|------|--------------|
| get_assigned_vehicle.jsp | Vehicle codes and hire numbers by customer/site/dept |
| get_codes.jsp | Override/mastercode data |
| get_customer.jsp | Customer names and codes |
| get_cust_vehicle.jsp | Customer vehicle assignments |
| get_customergp.jsp | Customer group codes |
| get_dept.jsp | Department names and codes |
| get_driver.jsp | Driver names and card/Wiegand IDs |
| get_impact.jsp | Impact calibration settings |
| get_mst_cd_exist.jsp | Driver names and slot assignments |
| get_mst_cd_like.jsp | Driver names matching a search string |
| get_site.jsp | Site names and codes |
| get_unassigned_vehicle.jsp | Unassigned vehicle serial numbers |
| get_user.jsp | User first/last names and codes |
| get_vehicle.jsp | Vehicle serial numbers |
| get_vehicle_dept.jsp | Vehicle types by customer/site/dept |

**Recommendation:** Add `<%@ include file="../sess/Expire.jsp" %>` as the first line in every `get_*.jsp` file. The `Expire.jsp` include must redirect unauthenticated requests to the login page before any data is fetched or output. Verify that `Expire.jsp` itself does not produce any output before redirecting, to avoid sending data before the redirect header.

---

### A12b-11

**File:** `master/register.jsp`
**Severity:** Critical
**Category:** Authentication — Publicly Accessible Registration API with No Session Check
**Description:** `register.jsp` is a JSP-based web API (returns XML, no HTML body) that accepts username/password credentials in plain HTTP parameters and, if they match a hardcoded or DB-stored API credential pair, creates full company registrations in the database including customer accounts, vehicle records, and driver records. It has no `Expire.jsp` include, no session check, and no CSRF protection. The authentication is performed inside the endpoint (`registerDAO.checkAuthority(username, password)`) using credentials passed as plain request parameters (susceptible to interception and brute-force). The `email` input from the registrant is placed directly into the XML response without entity encoding (`<code>"+email+"</code>`), which can cause XML injection.
**Evidence:**
```java
// No <%@ include file="../sess/Expire.jsp" %>
String username = request.getParameter("username");
String password = request.getParameter("password");
RegisterDAO registerDAO = new RegisterDAO();
boolean access = registerDAO.checkAuthority(username,password);
...
resp=resp+"<rec>"+"<code>"+email+"</code><name>"+result[1]+"</name></rec>";
```
**Recommendation:** If this endpoint is intended for use by an external mobile/tablet application, implement a proper API authentication mechanism (OAuth 2.0 bearer token or HMAC-signed requests over HTTPS). Credentials must not be passed as plain query/form parameters. The `email` value and all other user-supplied data must be XML-entity-encoded before insertion into the XML response string. Consider whether this endpoint should be accessible from the public internet at all or should be restricted to a separate service layer.

---

### A12b-12

**File:** `master/update_all_user_weigand.jsp`
**Severity:** High
**Category:** Authentication — Missing Session Enforcement
**Description:** `update_all_user_weigand.jsp` is a state-changing form that updates all user Wiegand codes. It does not include `../sess/Expire.jsp`. It imports and uses `Databean_report` (not `Databean_getuser`) and contains a form that POSTs `op_code=update_weigand` to `../servlet/Frm_saveuser`. Any unauthenticated user can load this page and trigger the Wiegand update operation.
**Evidence:**
```jsp
<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>
<!-- No <%@ include file="../sess/Expire.jsp" %> -->
...
<form method="post" action="../servlet/Frm_saveuser">
<input type=button name="save_button" value="Save" onclick="saveform();"/>
<input type="hidden" name="op_code" value="update_weigand"/>
```
**Recommendation:** Add `<%@ include file="../sess/Expire.jsp" %>` as the first line. Also add a CSRF token.

---

### A12b-13

**File:** `master/frm_group_loc_rel.jsp`
**Severity:** High
**Category:** Authentication — Missing Session Enforcement
**Description:** `frm_group_loc_rel.jsp` (Group Site Authorization form) does not include `../sess/Expire.jsp`. Despite reading session attributes for access level control (which would throw a NullPointerException if session is absent, potentially revealing a stack trace via ExceptionHandler), there is no explicit authentication gate. An unauthenticated user may be able to access this page.
**Evidence:**
```jsp
<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>
<!-- No <%@ include file="../sess/Expire.jsp" %> -->
...
String access_level = (String) session.getAttribute("access_level");
```
**Recommendation:** Add `<%@ include file="../sess/Expire.jsp" %>` as the first line.

---

### A12b-14

**File:** Multiple form JSPs — see list below
**Severity:** High
**Category:** IDOR — Record IDs from Request Parameters Without Session Ownership Validation
**Description:** Many edit forms accept a record identifier (usr_cd, veh_cd, chk_cd) directly from the request parameter and use it to fetch and modify that record, with no check that the record belongs to the currently logged-in user's customer scope. A logged-in user from Customer A can edit records belonging to Customer B by manipulating the request parameter.

Affected files and parameters:

| File | Parameter | Record Type |
|------|-----------|-------------|
| frm_new_customer.jsp | usr_cd | Customer master record |
| frm_new_driver.jsp | usr_cd | Driver record |
| frm_new_user.jsp | usr_cd | User account |
| frm_new_question.jsp | chk_cd | Pre-op check question |
| frm_new_vehicle.jsp | veh_cd | Vehicle record |
| frm_new_vehicle1.jsp | veh_cd | Vehicle record |
| frm_new_vehicle_short.jsp | veh_cd | Vehicle record |
| frm_repl_vehiclemod.jsp | veh_cd | Vehicle module replacement |
| frm_service_status.jsp | veh_cd | Vehicle service settings |
| frm_setup_driver.jsp | usr_cd | Driver assignment |
| frm_send_canbus_rules.jsp | veh_cd | Vehicle CANBus configuration |
| frm_vehicle_prod.jsp | veh_cd | Vehicle production/EOS dates |

**Recommendation:** After fetching a record by its primary key, verify that the record's customer/tenant identifier matches the `access_cust` value stored in the server-side session. Reject requests where there is a mismatch and log the attempted access. This validation should occur in the data access layer (Databean or DAO), not only in JSP presentation logic.

---

### A12b-15

**File:** `master/pic_upload_logo.jsp`, lines 27–32
**Severity:** High
**Category:** File Upload — Client-Side-Only Extension Validation
**Description:** The logo upload form validates the uploaded file extension only in client-side JavaScript. The check (`ext=="jpg"||ext=="JPG"||ext=="gif"||ext=="GIF"||ext=="bmp"||ext=="BMP"`) can be completely bypassed by submitting the form directly (e.g., with curl, Burp Suite, or by disabling JavaScript). The server-side handler (`../servlet/Frm_upload`) must perform its own validation; if it does not, an attacker can upload arbitrary file types including JSP webshells.
**Evidence:**
```javascript
var ext = pnm.substr(pnm.lastIndexOf('.')+1);
if(!(ext=="jpg"||ext=="JPG"||ext=="gif"||ext=="GIF"||ext=="bmp"||ext=="BMP"))
{
    flag=false;
    msg="Please enter the valid file format (jpg/gif/bmp)";
}
```
**Recommendation:** Implement server-side validation in `Frm_upload` that: (1) checks the file extension against an allowlist, (2) validates the MIME type by inspecting the file's magic bytes (not the Content-Type header), and (3) stores uploaded files outside the web root or in a directory where JSP/servlet execution is disabled. Rename uploaded files to a random UUID-based name to prevent filename-based attacks.

---

### A12b-16

**File:** `master/frm_upload_questions.jsp`, line 170
**Severity:** Medium
**Category:** XSS — Request Parameter Reflected in HTML Body
**Description:** The `cust_nm` parameter is taken from the request and reflected directly into the page body without HTML encoding. This is distinct from the `message` parameter pattern (A12b-2) in that `cust_nm` is a filter parameter passed as a URL query string, making it directly attacker-controllable via a crafted link.
**Evidence:**
```java
// Not shown in JSP — cust_nm comes from URL parameter
```
```jsp
<b>Question Upload Form for Customer <%=cust_nm %></b>
```
**Recommendation:** Apply `encodeForHTML(cust_nm)` before output.

---

### A12b-17

**File:** `master/frm_fc_vehicle_lst.jsp`, line 481
**Severity:** Medium
**Category:** XSS — `search_crit` Request Parameter Reflected in HTML Body
**Description:** The `search_crit` request parameter is reflected raw into the page body within a `<b>` tag. An attacker can inject HTML and script via a crafted URL.
**Evidence:**
```jsp
starting with '<%=search_crit %>'
```
**Recommendation:** Apply `encodeForHTML(search_crit)` before output.

---

### A12b-18

**File:** `master/frm_new_branch.jsp`, lines 181; `master/frm_new_branch_old.jsp`, line 169; `master/frm_new_department.jsp`, line 165; `master/frm_new_department_win.jsp`, ~line 110; `master/frm_new_division.jsp`, line 165; `master/frm_new_location.jsp`, line 221; `master/frm_new_group.jsp`, line 182
**Severity:** High
**Category:** XSS — DB Values in Inline JavaScript `onclick` Event Handlers
**Description:** Location names, addresses, group names, descriptions, and timezone values retrieved from the database are interpolated directly into `onclick="set_editvalues('...')"` attribute strings without JavaScript encoding. If any DB value contains a single quote, JavaScript special character, or HTML special character, this produces a stored XSS vector exploitable by any user who can control those DB values (e.g., an admin who saves a maliciously crafted location name).
**Evidence (representative, frm_new_branch.jsp):**
```jsp
onclick="set_editvalues('<%=loc_cd.get(i)%>','<%=loc_nm.get(i)%>','<%=addr.get(i)%>');"
```
**Recommendation:** Apply `encodeForJavaScript()` to all values interpolated into JS string contexts within HTML event attributes.

---

### A12b-19

**File:** All XML-producing `get_*.jsp` endpoints
**Severity:** Medium
**Category:** XML Injection — Unencoded DB Values in XML Response
**Description:** All `get_*.jsp` files construct XML responses by string concatenation without XML-encoding the DB values placed inside XML element content. If any DB value contains `<`, `>`, `&`, `"`, or `'`, the generated XML is malformed and the parser on the client side may fail or misbehave. A value containing `</code><inject>` would inject arbitrary XML nodes into the response, potentially enabling client-side injection attacks when the JavaScript processes the XML document.

The one partial exception is `get_cust_vehicle.jsp`, which applies `resp.replace("&","&amp;")` — encoding only ampersands, leaving `<` and `>` unhandled.

Affected files: get_assigned_vehicle.jsp, get_codes.jsp, get_customer.jsp, get_cust_vehicle.jsp (partial), get_customergp.jsp, get_dept.jsp, get_driver.jsp, get_impact.jsp, get_mst_cd_exist.jsp, get_mst_cd_like.jsp, get_site.jsp, get_unassigned_vehicle.jsp, get_user.jsp, get_vehicle.jsp, get_vehicle_dept.jsp, register.jsp.
**Evidence (representative, get_mst_cd_exist.jsp):**
```java
resp=resp+"<slot id='"+tmp3+"'>"+"<driver_id>"+tmp+"</driver_id><driver_nm>"+tmp4+"</driver_nm></slot>";
```
**Recommendation:** Use a proper XML library (e.g., `javax.xml.stream.XMLStreamWriter` or DOM + Transformer) to construct XML responses, which will automatically encode special characters. As a minimum fix, apply all five XML entity replacements (`&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `"`→`&quot;`, `'`→`&apos;`) to every value before inserting it into the XML string.

---

### A12b-20

**File:** `master/frm_new_customer.jsp`, multiple lines; `master/frm_new_driver.jsp`, multiple lines; `master/frm_new_user.jsp`, multiple lines; `master/frm_new_vehicle.jsp`, multiple lines; `master/frm_new_vehicle1.jsp`, multiple lines
**Severity:** Medium
**Category:** XSS — DB Values in HTML Form Field `value` Attributes
**Description:** Database-sourced values (user names, addresses, phone numbers, email addresses, serial numbers, hire numbers, comments, descriptions, etc.) are written raw into HTML `<input value="...">` and `<textarea>` elements. If any value contains `"`, `<`, or `>`, it breaks out of the attribute context. Since users can enter these values themselves (and they are stored then redisplayed), this constitutes a stored XSS vector.
**Evidence (representative, frm_new_customer.jsp):**
```jsp
<input type="text" name="fnm" ... value="<%=usr_fnm %>">
<TEXTAREA NAME="addr" ROWS="3" cols="60"><%=usr_addr %></TEXTAREA>
```
**Recommendation:** Apply `encodeForHTMLAttribute()` to all values used in HTML attribute contexts, and `encodeForHTML()` to all values rendered in HTML element content (such as within `<textarea>`).

---

### A12b-21

**File:** `master/frm_io_setting.jsp`, line 321
**Severity:** High
**Category:** XSS — DB Values in Inline JavaScript `onclick` Event Handler
**Description:** I/O violation number and level values from the database are interpolated raw into an `onclick` attribute string.
**Evidence:**
```jsp
onclick="call_delete('<%=vio_no.get(i)%>','<%= vio_level.get(i)%>');"
```
**Recommendation:** Apply `encodeForJavaScript()` to `vio_no` and `vio_level` before interpolation.

---

### A12b-22

**File:** `master/frm_mastercode_step2.jsp`, lines 305, 315, 321
**Severity:** Medium
**Category:** XSS — DB Values Rendered Raw in HTML and Hidden Fields
**Description:** DB-sourced display names (`get_user`, `get_loc`, `get_dep`) are rendered raw in an H2 heading. Additionally, driver code and slot number arrays (sourced from session-stored request parameters) are echoed back into hidden input fields without encoding.
**Evidence:**
```jsp
<h2><%=get_user%> - <%=get_loc%> - <%=get_dep%></h2>
<input type="hidden" name="driv_cd" value="<%=driv_cd[i]%>">
<input type="hidden" name="slot_no" value="<%=slot_no[i]%>">
```
**Recommendation:** Apply `encodeForHTML()` to heading content and `encodeForHTMLAttribute()` to hidden field values.

---

### A12b-23

**File:** `master/frm_override_codes.jsp`, line 449
**Severity:** Medium
**Category:** XSS — Request Parameters in `onload` JavaScript Call
**Description:** Several request parameters (veh_typ_cd, veh_cd, cust_cd, loc_cd, dept_cd) are interpolated directly into the `<body onload="set(...)">` call without JavaScript encoding.
**Evidence:**
```jsp
<body onload="set('<%=veh_typ_cd %>','<%=veh_cd %>','<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>');">
```
**Recommendation:** Apply `encodeForJavaScript()` to all values in the onload handler.

---

### A12b-24

**File:** `master/frm_service_flag.jsp`, lines 399, 403, 453, 455–469
**Severity:** Medium
**Category:** XSS — DB Values Rendered Raw in Data Table
**Description:** Service reminder hour values (`vservice_hour.get(i)`) and service IDs (`vservice_id.get(i)`) are rendered raw in the table and in an onclick handler. Vehicle hire numbers, service hours remaining, accumulated hours, last service dates, and next service dates are all rendered raw in table cells.
**Evidence:**
```jsp
<%=vservice_hour.get(i)%>
onclick="deleteReminder('<%=vservice_id.get(i) %>')"
<%=vhire_no.get(i) %>
<%=vserv_remain.get(i) %>
<%=vserv_acc_hours.get(i) %>
<%=vserv_last.get(i) %>
<%=vserv_next.get(i) %>
```
Note also that `vserv_color.get(i)` is interpolated into a `<td>` attribute: `<td <%=vserv_color.get(i) %>>` — this is an HTML attribute injection point if the DB value is attacker-controlled.
**Recommendation:** Apply `encodeForHTML()` to all cell content and `encodeForJavaScript()` to onclick handler parameters. Validate `vserv_color` against a strict allowlist of CSS class names before rendering into the attribute position.

---

### A12b-25

**File:** `master/frm_send_canbus_rules.jsp`, lines 57, 71, 83, 97, 105, 115, 121–123
**Severity:** Medium
**Category:** XSS — DB Values Rendered Raw; Request Parameters in Hidden Fields
**Description:** Vehicle hire number, serial number, GMTP ID, and vehicle type are retrieved from DB and rendered raw in table cells. The `veh_cd`, `gmtp_id`, and `form_cd` request parameters are echoed into hidden input value attributes without encoding.
**Evidence:**
```jsp
<td><%=tmp %></td>   <!-- tmp = hire_no / serial_no / gmtp_id / veh_type from DB -->
<option value="<%=vcan_mod.get(i) %>"><%=vcan_mod.get(i) %></option>
<td colspan=2> <%=message %></td>
<input type="hidden" name="veh_cd" value="<%=veh_cd %>">
<input type="hidden" name="gmtp_id" value="<%=gmtp_id %>">
```
**Recommendation:** Encode all DB values and request parameters before output.

---

### A12b-26

**File:** `master/frm_customer_vehicle_rel.jsp`, line 324; `master/frm_customer_vehicle_reset.jsp`, line 391
**Severity:** Medium
**Category:** XSS — Request Parameters in `onload` JavaScript Call
**Description:** Multiple request parameters (gp_cd, user_cd, veh_typ_cd, veh_cd, location_cd, dep_cd) are interpolated directly into the `<body onload="set(...)">` call.
**Evidence:**
```jsp
<body onload="set('<%=gp_cd %>','<%=user_cd %>','<%=veh_typ_cd %>','<%=veh_cd %>','<%=location_cd %>','<%=dep_cd %>');">
```
**Recommendation:** Apply `encodeForJavaScript()` to all values in the onload handler.

---

### A12b-27

**File:** `master/frm_impact_setting.jsp`, line 658
**Severity:** Medium
**Category:** XSS — Multiple DB/Request Values in `onload` JavaScript Call
**Description:** Vehicle type, vehicle code, customer code, site code, department code, and a boolean flag are interpolated raw into the `<body onload>` JS call.
**Evidence:**
```jsp
<body onload="set('<%=veh_typ_cd %>','<%=veh_cd %>','<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>');fetch_impact('<%=set_veh_cd %>');disable_bar('<%=impact_hundred %>')">
```
**Recommendation:** Apply `encodeForJavaScript()` to all values in the onload handler.

---

### A12b-28

**File:** `master/frm_hourcount_config.jsp`, lines 362–363, 380, 383, 387, 395
**Severity:** Medium
**Category:** XSS — DB Values Rendered Raw in Data Table and onclick Handler
**Description:** Customer, site, and department display names from the DB are rendered raw in a heading. Vehicle hire numbers and contracted hours are rendered raw in table cells. Vehicle code is interpolated into an `onclick` handler.
**Evidence:**
```jsp
<b>Hour Count Settings for the Customer: <%=get_cust %> for Site: <%=get_loc %> for the Department: <%=get_dep %></b>
<%=vhire_no.get(i) %>
<input type="text" name='hour' value='<%=vcount_hour.get(i) %>' .../>
<input type="button" value="Update" onclick="fnupdate('<%=vveh_cd.get(i)%>','<%=i%>')"/>
```
**Recommendation:** Encode all DB values with `encodeForHTML()` for HTML contexts and `encodeForJavaScript()` for JS contexts.

---

### A12b-29

**File:** `master/rpt_preop_unsync_qustion.jsp`, lines 478, 485–488
**Severity:** Medium
**Category:** XSS — DB Values Rendered Raw in Data Table
**Description:** Vehicle hire numbers, question order numbers, question text, expected answers, and critical-answer flags from the DB are all rendered raw in table cells. The `bgcol` variable derived from DB string comparison is interpolated into a `bgcolor` attribute.
**Evidence:**
```jsp
<%=Vhire_no.get(i)%>
<td bgcolor="<%=bgcol%>"><%=vord_no.get(j) %></td>
<td bgcolor="<%=bgcol%>"><%=vquest.get(j) %></td>
<td bgcolor="<%=bgcol%>"><%=vexp_ans.get(j) %></td>
<td bgcolor="<%=bgcol%>"> <font color="<%=col %>">&nbsp;<%=tmp %></font></td>
```
**Recommendation:** Encode all DB values before output. Validate `bgcol` and `col` against a strict allowlist before interpolating into attribute positions.

---

### A12b-30

**File:** `master/frm_site_hours.jsp`, line 361
**Severity:** Medium
**Category:** XSS — Multiple Parameters in `onload` JavaScript Call
**Description:** Four filter parameters (cust_cd, loc_cd, dep_cd, type_cd) are interpolated raw into the `<body onload="set(...)">` call.
**Evidence:**
```jsp
<body onload="set('<%=cust_cd %>','<%=loc_cd %>','<%=dep_cd %>','<%=type_cd %>')">
```
**Recommendation:** Apply `encodeForJavaScript()` to all values.

---

### A12b-31

**File:** `master/frm_service_flag.jsp`, lines 291, 403
**Severity:** Medium
**Category:** XSS — Parameters in `onload`; DB Values in onclick
**Description:** Three filter parameters in the `<body onload="set(...)">` call; service ID in `deleteReminder('<%=vservice_id.get(i) %>')` onclick.
**Evidence:**
```jsp
<body onload="set('<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>')">
onclick="deleteReminder('<%=vservice_id.get(i) %>')"
```
**Recommendation:** Apply `encodeForJavaScript()` to all values in JS event handler contexts.

---

### A12b-32

**File:** `master/frm_new_vehicle.jsp`, line 261; `master/frm_new_vehicle1.jsp`, lines 295–296; `master/frm_repl_vehiclemod.jsp`, lines 115–116
**Severity:** Medium
**Category:** XSS — Request Parameters in JavaScript `onclick` Close-Form Call
**Description:** Filter parameters (veh_typ_cd, loc_cd, st_dt, end_dt, search_crit, form_cd, cust_cd, dept_cd) that were passed to the page as GET parameters are echoed raw into an `onclick="closeform(...)"` call, creating a JS injection vector.
**Evidence (frm_new_vehicle.jsp):**
```jsp
<input type=button name="close_button" value="Close"
  onClick="closeform('<%=veh_typ_cd %>','<%=loc_cd %>','<%=st_dt %>','<%=end_dt %>','<%=search_crit %>','<%=form_cd %>');">
```
**Recommendation:** Apply `encodeForJavaScript()` to all request parameters embedded in inline JS event handlers.

---

## Summary Table

| ID | Severity | Category | Files Affected |
|----|----------|----------|----------------|
| A12b-1 | High | XSS — Reflected message parameter | frm_customer_rel.jsp |
| A12b-2 | High | XSS — Reflected message parameter (widespread) | 35 files |
| A12b-3 | High | XSS — DB values in onclick JS string | frm_customer_rel.jsp |
| A12b-4 | High | XSS — DB values in onload JS call | frm_new_driver.jsp, frm_new_user.jsp |
| A12b-5 | Medium | XSS / Path Traversal — DB filename in img src | frm_new_customer.jsp |
| A12b-6 | Critical | Plaintext password exposure | frm_new_user.jsp |
| A12b-7 | High | Supply-chain — External script over HTTP | frm_new_driver.jsp, frm_new_user.jsp |
| A12b-8 | Low | Information Disclosure — Debug alert() in production | frm_customer_rel.jsp |
| A12b-9 | High | CSRF — No token on state-changing forms | 38 files |
| A12b-10 | High | Authentication — No session check on AJAX endpoints | 15 get_*.jsp files |
| A12b-11 | Critical | Authentication — Unauthenticated public registration API | register.jsp |
| A12b-12 | High | Authentication — No session check | update_all_user_weigand.jsp |
| A12b-13 | High | Authentication — No session check | frm_group_loc_rel.jsp |
| A12b-14 | High | IDOR — Record IDs not validated against session scope | 12 files |
| A12b-15 | High | File Upload — Client-side-only validation | pic_upload_logo.jsp |
| A12b-16 | Medium | XSS — cust_nm request parameter in HTML | frm_upload_questions.jsp |
| A12b-17 | Medium | XSS — search_crit request parameter in HTML | frm_fc_vehicle_lst.jsp |
| A12b-18 | High | XSS — DB values in onclick JS string | 7 form files |
| A12b-19 | Medium | XML Injection — Unencoded DB values in XML responses | 16 files |
| A12b-20 | Medium | XSS — DB values in HTML form field value attributes | 5 files |
| A12b-21 | High | XSS — DB values in onclick JS string | frm_io_setting.jsp |
| A12b-22 | Medium | XSS — DB values in HTML and hidden fields | frm_mastercode_step2.jsp |
| A12b-23 | Medium | XSS — Request params in onload JS call | frm_override_codes.jsp |
| A12b-24 | Medium | XSS — DB values in table and onclick; HTML attr injection | frm_service_flag.jsp |
| A12b-25 | Medium | XSS — DB values and request params in cells/hidden fields | frm_send_canbus_rules.jsp |
| A12b-26 | Medium | XSS — Request params in onload JS call | frm_customer_vehicle_rel.jsp, frm_customer_vehicle_reset.jsp |
| A12b-27 | Medium | XSS — Multiple values in onload JS call | frm_impact_setting.jsp |
| A12b-28 | Medium | XSS — DB values in table and onclick | frm_hourcount_config.jsp |
| A12b-29 | Medium | XSS — DB values in table; HTML attr injection via bgcol | rpt_preop_unsync_qustion.jsp |
| A12b-30 | Medium | XSS — Filter params in onload JS call | frm_site_hours.jsp |
| A12b-31 | Medium | XSS — Params in onload; DB value in onclick | frm_service_flag.jsp |
| A12b-32 | Medium | XSS — Request params in onclick closeform() call | frm_new_vehicle.jsp, frm_new_vehicle1.jsp, frm_repl_vehiclemod.jsp |

**Total findings: 32**

**By severity:**
- Critical: 2 (A12b-6, A12b-11)
- High: 14 (A12b-1, A12b-2, A12b-3, A12b-4, A12b-7, A12b-9, A12b-10, A12b-12, A12b-13, A12b-14, A12b-15, A12b-18, A12b-21, A12b-22 is Medium — correcting: A12b-22 Medium)
- Medium: 16
- Low: 1

Corrected severity counts:
- Critical: 2
- High: 12 (A12b-1, A12b-2, A12b-3, A12b-4, A12b-7, A12b-9, A12b-10, A12b-12, A12b-13, A12b-14, A12b-15, A12b-18, A12b-21)
- Medium: 17
- Low: 1

---

## Key Systemic Observations

1. **No output encoding anywhere.** The codebase makes no use of any output encoding library (ESAPI, StringEscapeUtils, or equivalent). Every `<%= %>` expression in the codebase renders raw, regardless of context. This is a systemic defect, not isolated bugs.

2. **No CSRF protection anywhere.** The `Frm_saveuser` servlet processes all state-changing operations with no CSRF token validation. All forms across the entire application are vulnerable.

3. **AJAX data endpoints are unauthenticated.** The 15 `get_*.jsp` endpoints that power the dynamic dropdowns throughout the application return organizational data (customers, sites, drivers, vehicles, departments) without any authentication gate.

4. **Passwords stored reversibly.** The ability to pre-populate password fields from the database (frm_new_user.jsp) proves that user passwords are stored in a form that allows recovery of the plaintext value — either as plaintext directly or using reversible encryption. This violates all current security standards.

5. **IDOR is a design pattern, not individual bugs.** The pattern of accepting record IDs as request parameters and not validating ownership against the session is applied consistently across all edit forms. A fix requires a cross-cutting ownership check in the data access layer, not individual JSP patches.

6. **register.jsp is a critical unauthenticated API.** This endpoint bypasses the session-based security model entirely. Its existence and exposure to unauthenticated callers represents the highest-priority remediation item alongside the plaintext password issue.
