# Security Audit — master config JSPs
**Audit ID:** A12-config
**Run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Auditor:** Agent A12-config
**Date:** 2026-02-25

---

## STEP 3 — Reading Evidence (File Inventory)

### 1. frm_conf_firmware_upg.jsp

**Path:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_upg.jsp`

**`<%@ page import %>`:**
- Line 2: `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:** None. No `<%@ include %>` or `<jsp:include>` present.

**`<jsp:useBean>`:**
- Line 500: `<jsp:useBean class="com.torrent.surat.fms6.master.Databean_getuser" id="filter" scope="request"/>`
- Line 501: `<jsp:useBean id="Util" class="com.torrent.surat.fms6.util.UtilBean" scope="page"/>`

**Scriptlet blocks:**
- Lines 502–600: Main logic block. Reads `cust_cd`, `loc_cd`, `dept_cd`, `search_crit`, `form_cd`, `message` from request parameters (no null-safety for `message`). Hard-codes `access_level = "1"`, `access_cust="0"`, `access_site="0"`, `access_dept="0"`. Hard-codes `ucd = "1"`. Reads no session attributes whatsoever for access control. Populates filter bean and retrieves vehicle/firmware ArrayLists.
- Lines 617–637: JSP loop scriptlets rendering customer/site/dept dropdowns.
- Lines 694–724: Loop scriptlet rendering vehicle type checkboxes.
- Lines 733–773: Loop scriptlet rendering vehicle checkboxes (outdated firmware section).
- Lines 784–824: Loop scriptlet rendering vehicles with current firmware section.

**`<%= %>` expressions (selected):**
- Line 7: `<%=LindeConfig.systemName %>` — in `<title>`, unescaped
- Line 602: `<%=cust_cd %>`, `<%=loc_cd %>`, `<%=dept_cd %>` — in `onload` attribute, unescaped
- Line 609: `<%=form_nm %>` — in table heading, unescaped
- Lines 618–619: `<%=vcust_cd.get(i) %>`, `<%=vcust_nm.get(i) %>` — in `<option>`, unescaped
- Lines 627–629: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — unescaped
- Lines 636, 637: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — unescaped
- Line 646: `<%=search_crit %>` — reflected into `<input value=...>`, unescaped
- Line 654: `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>` — unescaped
- Line 655: `<%=search_crit %>` — unescaped
- Line 659: `<%=message %>` — reflected from request parameter, rendered directly into a `<tr>`, unescaped
- Lines 673, 674: `<%=firm_vers.get(i) %>` — firmware version in `<option>`, unescaped
- Lines 698, 704, 711, 718: `<%=vt_cds.get(i) %>`, `<%=vt_nms.get(i) %>` — unescaped checkbox values and labels
- Lines 766–767: `<%=veh_nm.get(i) %>`, `<%=vgmtp_id.get(i) %>`, `<%=curr_ver.get(i) %>`, `<%=rep_time.get(i) %>` — unescaped
- Lines 817–818: Same pattern for latest-firmware section
- Lines 832–839: Hidden fields — `<%=form_cd %>`, `<%=loc_cd %>`, `<%=cust_cd %>`, `<%=dept_cd %>`, `<%=Vuser_cd.size() %>`, `<%=vt_cds.size() %>`, `<%=veh_cd.size() %>` — unescaped

**HTML forms:**
- Line 605: `<form method="post" action="../servlet/Frm_saveuser">` — submits firmware dispatch command

---

### 2. frm_conf_firmware_upg_bean.jsp

**Path:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_upg_bean.jsp`

**`<%@ page import %>`:**
- Line 1: `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`
- Line 2: `<%@ page import="com.torrent.surat.fms6.master.FirmwareverBean"%>`

**Include directives:** None.

**`<jsp:useBean>`:**
- Line 513: `<jsp:useBean class="com.torrent.surat.fms6.master.Databean_getuser" id="filter" scope="request"/>`
- Line 514: `<jsp:useBean id="Util" class="com.torrent.surat.fms6.util.UtilBean" scope="page"/>`

**Scriptlet blocks:**
- Lines 515–601: Main logic. Reads request parameters. Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session (lines 532–535). Reads `user_cd` from session (line 550). No authentication guard — null session is not handled before `session.getAttribute("access_level")` at line 532 (NullPointerException risk if session absent). Passes access constraints to filter bean.
- Lines 618–644: Dropdown rendering loops.
- Lines 694–724: Vehicle type checkbox loop.
- Lines 733–753: Vehicle checkbox loop (outdated firmware).
- Lines 762–783: Vehicle checkbox loop (current firmware).

**`<%= %>` expressions (selected):**
- Line 7: `<%=LindeConfig.systemName %>` — unescaped in `<title>`
- Line 603: `<%=cust_cd %>`, `<%=loc_cd %>`, `<%=dept_cd %>`, `<%=model_cd%>` — in `onload`, unescaped
- Line 610: `<%=form_nm %>` — unescaped
- Lines 619, 620, 629, 630, 637, 638, 644, 645: Dropdown codes and names — unescaped
- Line 656: `<%=search_crit %>` — reflected into `<input value=...>`, unescaped
- Lines 664–665: `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>`, `<%=search_crit %>` — unescaped
- Line 669: `<%=message %>` — request parameter reflected directly, unescaped
- Lines 679, 680: `<%=firm_vers.get(i) %>` — firmware version in `<option>`, unescaped
- Lines 698, 704, 711, 718: Vehicle type codes and names — unescaped
- Lines 746–747: `<%=firmwareverbean.getHire_no() %>`, `<%=firmwareverbean.getGmtp_id() %>`, `<%=firmwareverbean.getCurr_ver() %>`, `<%=firmwareverbean.getRep_time() %>` — unescaped
- Lines 776–777: Same for latest firmware section
- Lines 785–792: Hidden fields — unescaped values

**HTML forms:**
- Line 606: `<form method="post" action="../servlet/Frm_saveuser">` — submits firmware dispatch

---

### 3. frm_conf_firmware_display.jsp

**Path:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_display.jsp`

**`<%@ page import %>`:**
- Line 2: `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:** None.

**`<jsp:useBean>`:**
- Line 57: `<jsp:useBean class="com.torrent.surat.fms6.master.Databean_getuser" id="filter" scope="request"/>`
- Line 58: `<jsp:useBean id="Util" class="com.torrent.surat.fms6.util.UtilBean" scope="page"/>`

**Scriptlet blocks:**
- Lines 59–158: Main logic. Hard-codes `access_level = "1"`, `access_cust="0"`, `access_site="0"`, `access_dept="0"` (lines 72–75). Hard-codes `ucd = "1"` (line 90). Reads no session attributes. No session check present.
- Lines 175, 177: Dropdown render loop for customer.
- Lines 205–239: Table row rendering loop for vehicle firmware data.

**`<%= %>` expressions (selected):**
- Line 7: `<%=LindeConfig.systemName %>` — unescaped
- Line 160: `<%=cust_cd %>` — in `onload`, unescaped
- Line 167: `<%=form_nm %>` — unescaped
- Lines 175–176: `<%=vcust_cd.get(i) %>`, `<%=vcust_nm.get(i) %>` — unescaped
- Lines 188: `<%=get_cust %>`, `<%=rep_unino %>` — unescaped
- Lines 224, 226–230, 232, 234, 236: Vehicle fleet no, version, type, dates, location, department — all unescaped DB values
- Lines 242–246: Hidden fields — unescaped

**HTML forms:**
- Line 163: `<form method="post" action="../servlet/Frm_saveuser">`

---

### 4. frm_conf_driv_setting.jsp

**Path:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_driv_setting.jsp`

**`<%@ page import %>`:**
- Line 2: `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- Line 1: `<%@ include file="../sess/Expire.jsp" %>` — session guard

**`<jsp:useBean>`:**
- Line 602: `<jsp:useBean class="com.torrent.surat.fms6.master.Databean_getuser" id="filter" scope="request"/>`
- Line 603: `<jsp:useBean id="Util" class="com.torrent.surat.fms6.util.UtilBean" scope="page"/>`

**Scriptlet blocks:**
- Lines 604–690: Main logic. Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session (lines 622–625). `access_level` can be null (no null guard before `equalsIgnoreCase` at line 627 — NullPointerException if session missing despite Expire.jsp). Reads `user_cd` from session (line 639). Passes access constraints to filter bean. The filter bean (`Databean_getuser`) is responsible for scoping the data list to the authenticated user's accessible customers/sites/departments.
- Lines 743–755: Site dropdown render loop with conditional `all` option based on `al < 3`.
- Lines 763–769: Department dropdown render loop with conditional `all` option based on `al < 4`.
- Lines 862–892: Driver checkbox render loop.
- Lines 902–928: Department checkbox render loop.
- Lines 937–963: Vehicle type checkbox render loop.
- Lines 972–998: Vehicle checkbox render loop.

**`<%= %>` expressions (selected):**
- Line 7: `<%=LindeConfig.systemName %>` — unescaped
- Line 691: `<%=cust_cd %>`, `<%=loc_cd %>`, `<%=dept_cd %>` — in `onload`, unescaped
- Line 735: `<%=form_nm %>` — unescaped
- Lines 744–745, 754, 765–766: Dropdown codes and names — unescaped
- Line 779: `<%=search_crit %>` — reflected into `<input value=...>`, unescaped
- Line 786: `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>` — unescaped
- Line 787: `<%=search_crit %>` — unescaped
- Line 791: `<%=message %>` — request param reflected, unescaped
- Lines 864–886: Driver codes, first/last names — DB data, unescaped
- Lines 904, 908, 915, 922: Department codes and names — unescaped
- Lines 939, 943, 950, 957: Vehicle type codes and names — unescaped
- Lines 974, 978, 985, 992: Vehicle codes and names — unescaped
- Lines 1005–1014: Hidden fields including `access_level` written back to page — unescaped

**HTML forms:**
- Line 731: `<form method="post" action="../servlet/Frm_saveuser">`

---

### 5. frm_impact_setting.jsp

**Path:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_impact_setting.jsp`

**`<%@ page import %>`:**
- Line 2: `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- Line 1: `<%@ include file="../sess/Expire.jsp" %>` — session guard
- Line 680: `<%@ include file="../menu/menu.jsp" %>` — navigation menu

**`<jsp:useBean>`:**
- Line 562: `<jsp:useBean class="com.torrent.surat.fms6.master.Databean_getuser" id="filter" scope="request"/>`
- Line 563: `<jsp:useBean id="Util" class="com.torrent.surat.fms6.util.UtilBean" scope="page"/>`

**Scriptlet blocks:**
- Lines 564–657: Main logic. Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session (lines 581–584). Reads `user_cd` from session (line 598). Same null-before-equalsIgnoreCase risk on `access_level` at line 586. Reads `veh_cd`, `veh_typ_cd`, `cust_cd`, `loc_cd`, `dept_cd`, `form_cd` from request. Passes access constraints to filter bean.
- Lines 711, 723, 737, 754, 767: Filter dropdown render loops.
- Lines 790–796: Conditional "Reset Calibration" button based on `fmod`.

**`<%= %>` expressions (selected):**
- Line 7: `<%=LindeConfig.systemName %>` — unescaped
- Line 658: `<%=veh_typ_cd %>`, `<%=veh_cd %>`, `<%=cust_cd %>`, `<%=loc_cd %>`, `<%=dept_cd %>`, `<%=set_veh_cd %>`, `<%=impact_hundred %>` — in `onload`, unescaped
- Line 702: `<%=form_nm %>` — unescaped
- Lines 712–713, 724, 737–741, 755–756, 768–769: Dropdown codes and names — unescaped
- Line 823: `<%=message %>` — request param reflected, unescaped
- Lines 830–836: Hidden fields including `avg`, `dev`, `fsss_multiplicator`, `fssx_multiplicator`, `access_level` — unescaped
- Line 836: `<%=access_level %>` — session value written as hidden field, unescaped

**HTML forms:**
- Line 698: `<form method="post" action="../servlet/Frm_saveuser">`

---

## STEP 4 — SECURITY REVIEW

---

### Finding A12c-1

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_upg.jsp`
**Lines:** 519–538
**Severity:** CRITICAL
**Category:** Authentication — Missing Session Check

**Description:**
`frm_conf_firmware_upg.jsp` contains no session authentication guard whatsoever. Unlike `frm_conf_driv_setting.jsp` and `frm_impact_setting.jsp` which include `../sess/Expire.jsp`, this page includes no equivalent. Access control variables are entirely hard-coded to bypass any real restriction: `access_level = "1"`, `access_cust="0"`, `access_site="0"`, `access_dept="0"`, and `ucd = "1"`. Any unauthenticated HTTP request can load this page and submit the firmware dispatch form.

**Evidence:**
```java
// frm_conf_firmware_upg.jsp lines 519–538
String access_level = "1";
String access_cust="0";
String access_site="0";
String access_dept="0";

if(access_level.equalsIgnoreCase(""))
{
    access_level = "5";
}
int al = Integer.parseInt(access_level);

filter.setAccess_level(access_level);
filter.setAccess_cust(access_cust);
filter.setAccess_site(access_site);
filter.setAccess_dept(access_dept);

//end of access level control
//String ucd = ""+session.getAttribute("user_cd");
String ucd = "1";
```
Note the commented-out `session.getAttribute("user_cd")` line 537, showing this was previously session-driven and was intentionally disabled.

**Recommendation:** Re-add `<%@ include file="../sess/Expire.jsp" %>` as the first line. Remove all hard-coded access values; restore reading from `session.getAttribute(...)`. This page must never be accessible without an authenticated session.

---

### Finding A12c-2

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_display.jsp`
**Lines:** 72–91
**Severity:** CRITICAL
**Category:** Authentication — Missing Session Check

**Description:**
`frm_conf_firmware_display.jsp` also contains no session guard and has identical hard-coded access values. It displays the live firmware version matrix for all fleet devices assigned to a customer, including fleet numbers, GMTP device IDs, firmware version strings, upgrade dates, and last report times. This information is accessible to unauthenticated parties.

**Evidence:**
```java
// frm_conf_firmware_display.jsp lines 72–91
String access_level = "1";
String access_cust="0";
String access_site="0";
String access_dept="0";

if(access_level.equalsIgnoreCase(""))
{
    access_level = "5";
}
int al = Integer.parseInt(access_level);
...
//String ucd = ""+session.getAttribute("user_cd");
String ucd = "1";
```

**Recommendation:** Add `<%@ include file="../sess/Expire.jsp" %>` at line 1. Restore session-driven access level reading.

---

### Finding A12c-3

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_upg.jsp` (form dispatch) and
`C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\master\Frm_saveuser.java`
**Lines (JSP):** 605; **(Servlet):** 54–80, 177–181
**Severity:** CRITICAL
**Category:** Authentication — Servlet Missing Session Enforcement

**Description:**
The `Frm_saveuser` servlet's `doPost()` method performs no session authentication check before dispatching to any operation handler including `conf_firmware_upg` and `conf_firmware_upg_bean`. There is no `req.getSession(false)` null check, no `user_cd` attribute verification, and no redirect to login. Any unauthenticated HTTP POST to `/servlet/Frm_saveuser` with `op_code=conf_firmware_upg` will be processed, allowing an attacker to dispatch firmware upgrade commands to fleet devices without any valid session.

**Evidence:**
```java
// Frm_saveuser.java doPost(), lines 54–80 (no auth check)
protected void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException,
    IOException {
    res.setContentType("text/plain");
    try{
        // ... database connection setup only ...
        op_code=req.getParameter("op_code")==null?"":req.getParameter("op_code");
        // ... no session.getAttribute("user_cd") check, no redirect to login ...
        else if(req.getParameter("op_code").equalsIgnoreCase("conf_firmware_upg")) {
            conf_firmware_upg(req);    // line 178
        }
        else if(req.getParameter("op_code").equalsIgnoreCase("conf_firmware_upg_bean")) {
            conf_firmware_upg_bean(req);    // line 181
        }
```

**Recommendation:** Add a session authentication guard at the top of `doPost()`: verify `req.getSession(false) != null` and `req.getSession(false).getAttribute("user_cd") != null`, and send HTTP 401 or redirect to login if either fails.

---

### Finding A12c-4

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\master\Frm_saveuser.java`
**Lines:** 10204, 10211, 10220–10241, 10264–10280
**Severity:** CRITICAL
**Category:** Firmware Dispatch — Cross-Customer Scope Violation (IDOR)

**Description:**
In both `conf_firmware_upg` and `conf_firmware_upg_bean`, the `cust_cd` passed to the firmware dispatch operation is taken **entirely from the HTTP request parameters** (`request.getParameter("cust_cd")`). There is no comparison between the submitted `cust_cd` and the `access_cust` value from the authenticated session. The vehicle lookup queries use the caller-supplied `cust_cd` directly in SQL `WHERE` clauses. As a result, any authenticated user (or, given A12c-1/A12c-3, any user at all) can substitute any other customer's code and push an FTPF firmware-upgrade command to that customer's fleet devices.

The FTPF command string is then written directly into the `outgoing` table, which is polled by the telematics gateway and transmitted over-the-air to the physical forklift devices.

**Evidence:**
```java
// conf_firmware_upg_bean, Frm_saveuser.java line 10204
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
// ... no check against session.getAttribute("access_cust") ...

// Line 10264 — vehicle lookup uses caller-supplied cust_cd directly:
queryString="select \"VEHICLE_ID\" from \"FMS_VEHICLE_MST\" where \"VEHICLE_TYPE_CD\" = '"+mod_cd[j]+"' and \"VEHICLE_CD\" in " +
    "(select \"VEHICLE_CD\" from \"FMS_USR_VEHICLE_REL\" where \"USER_CD\" = '"+cust_cd+"' and \"LOC_CD\" = '"+loc_cd+"' and \"DEPT_CD\" = '"+dep+"')";

// Line 10211 — FTPF command constructed with unvalidated firmware version parameter:
String msg = "FTPF="+LindeConfig.firmwareserver+","+RuntimeConf.firmwareport+","+RuntimeConf.firmwareuser+","+RuntimeConf.firmwarepass+","+RuntimeConf.firmwareuploadfolder+message+"/FleetMS.bin";
```

**Recommendation:** After reading `cust_cd` from the request, compare it to `request.getSession().getAttribute("access_cust")`. If the session's access level restricts the user to one customer, reject any request where `cust_cd` does not match. Apply equivalent checks for `loc_cd` and `dept_cd`.

---

### Finding A12c-5

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\master\Frm_saveuser.java`
**Lines:** 10211, 10343–10376, 10386, 10220, 10228, 10235, 10241, 10264, 10280, 10292, 10297, 10304
**Severity:** HIGH
**Category:** SQL Injection — String Concatenation in Firmware Dispatch Queries

**Description:**
Both `conf_firmware_upg` and `conf_firmware_upg_bean` build every SQL query using raw string concatenation with unvalidated, user-supplied request parameters (`veh_cd[]`, `mod_cd[]`, `cust_cd`, `loc_cd`, `dep`, `message`). The `message` parameter in particular is the **firmware version string** submitted from the form's dropdown but is never sanitised. An attacker who can submit a POST request (and given A12c-3 no session is required) can inject arbitrary SQL. Similarly, vehicle IDs submitted as `veh[]` checkboxes are spliced into queries without parameterisation.

**Evidence (representative):**
```java
// Line 10386 (conf_firmware_upg) — veh_cd from request, concatenated:
queryString="select \"VEHICLE_ID\" from \"FMS_VEHICLE_MST\" where \"VEHICLE_CD\" = '"+veh_cd[j]+"'";

// Line 10220 (conf_firmware_upg_bean) — same pattern:
queryString="select \"VEHICLE_ID\" from \"FMS_VEHICLE_MST\" where \"VEHICLE_CD\" = '"+veh_cd[j]+"'";

// Line 10228 — message (firmware version) concatenated:
queryString="select  outgoing_id from \"outgoing\" where destination = '"+gmtp+"' and message = '"+msg+"'";

// Line 10235 — INSERT with msg (which contains user-controlled message parameter):
queryString="insert into \"outgoing\" (destination,message) values('"+gmtp+"','"+msg+"')";

// Line 10264 — mod_cd and cust_cd, loc_cd, dep all concatenated:
queryString="select \"VEHICLE_ID\" from \"FMS_VEHICLE_MST\" where \"VEHICLE_TYPE_CD\" = '"+mod_cd[j]+"' and \"VEHICLE_CD\" in " +
    "(select \"VEHICLE_CD\" from \"FMS_USR_VEHICLE_REL\" where \"USER_CD\" = '"+cust_cd+"' and \"LOC_CD\" = '"+loc_cd+"' and \"DEPT_CD\" = '"+dep+"')";

// Line 10280 — message concatenated into version check:
queryString="select count(*) from \"FMS_VER_STORE\", \"FMS_VEHICLE_MST\" " +
    " where \"FMS_VEHICLE_MST\".\"VEHICLE_CD\"= \"FMS_VER_STORE\".\"VEHICLE_CD\" AND  \"FMS_VEHICLE_MST\".\"VEHICLE_ID\" = '"+gmtp_id.get(k)+"' and \"CURR_VER\" = '"+message+"'";
```

**Recommendation:** Replace all string-concatenated queries with `PreparedStatement` with parameterised placeholders. Validate the `message` (firmware version) parameter against the set of known valid version strings fetched from the DB before use.

---

### Finding A12c-6

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_upg.jsp`
**Lines:** 659, 646, 655, 654; also `frm_conf_firmware_upg_bean.jsp` lines 669, 656, 665; `frm_conf_firmware_display.jsp` lines 224–237; `frm_conf_driv_setting.jsp` lines 779, 787, 791; `frm_impact_setting.jsp` line 823
**Severity:** HIGH
**Category:** Cross-Site Scripting (XSS) — Reflected, Unescaped Output

**Description:**
Throughout all five JSP files, request parameters and database-sourced values are emitted directly using `<%= %>` with no HTML encoding. The most acute instances are:

1. **`message` parameter** — present in all five files, reflected verbatim from request into page HTML (e.g., `frm_conf_firmware_upg.jsp:659` `<%=message %>`). After a form submission the servlet redirects back with a `message=` URL parameter containing the success/error string. An attacker who crafts a URL with a `<script>` payload in `message` can deliver a stored-looking XSS to any user who follows that link.

2. **`search_crit` parameter** — rendered unescaped into an `<input value=...>` attribute and a bare table cell (e.g., `frm_conf_firmware_upg.jsp:646` and `:655`). Payload: `search_crit="><script>alert(1)</script>`.

3. **DB-sourced data** — vehicle hire numbers (`veh_nm`), GMTP device IDs (`vgmtp_id`), firmware version strings (`curr_ver`), location names, department names, and customer names are all rendered unescaped. If any of these DB fields are ever corrupted or injected via another route, they produce stored XSS.

**Evidence (representative):**
```java
// frm_conf_firmware_upg.jsp line 659 — message request param, unescaped:
<tr class="heading2"><%=message %>
</tr>

// frm_conf_firmware_upg.jsp line 646 — search_crit in input value, unescaped:
<input type="text" name="sc" value="<%=search_crit %>" />

// frm_conf_firmware_upg_bean.jsp line 669 — same message pattern:
<tr class="heading2"><%=message %>
</tr>

// frm_conf_firmware_display.jsp line 224 — DB vehicle hire no, unescaped:
<td> <%=veh_nm.get(i) %>

// frm_conf_driv_setting.jsp line 791 — message in table row, unescaped:
<tr class="heading2"><%=message %>
</tr>

// frm_impact_setting.jsp line 823 — message in styled red td, unescaped:
&nbsp; <%=message %><div id='message'></div>
```

**Recommendation:** Wrap every `<%= %>` expression that outputs user-supplied or DB-sourced data through an HTML-encoding utility, e.g., `<%=Util.htmlEncode(value) %>` (or an equivalent JSTL `<c:out value="${...}" escapeXml="true" />`). At minimum: `message`, `search_crit`, `get_cust`, `get_loc`, `get_dep`, all hire numbers, version strings, and device IDs must be encoded.

---

### Finding A12c-7

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_driv_setting.jsp`
**Lines:** 622–625, 631, 662–663
**Severity:** HIGH
**Category:** IDOR — Driver Device Settings Lack Customer-Scope Validation at Presentation Layer

**Description:**
`frm_conf_driv_setting.jsp` reads session attributes for access control (`access_level`, `access_cust`, `access_site`, `access_dept`) and passes them to `Databean_getuser`. However, the `cust_cd`, `loc_cd`, and `dept_cd` filter values used to scope which drivers and vehicles are displayed are taken directly from request parameters without cross-referencing them against the session's `access_cust`. The page trusts that the filter bean will enforce scoping, but from the form submission side (`../servlet/Frm_saveuser`, `op_code=conf_driv_setting`), the `cust_cd` submitted in the form's hidden field is the raw request-parameter value, not validated against the session. An authenticated user-A belonging to customer-1 can alter the form's `cust_cd` hidden field to customer-2's code and issue IDAUTH/IDDENY/IDCLEAR/IDMAST driver memory commands to customer-2's fleet devices.

**Evidence:**
```java
// frm_conf_driv_setting.jsp lines 622–625 — session attrs read:
String access_level = (String)session.getAttribute("access_level");
String access_cust=(String)session.getAttribute("access_cust");
String access_site=(String)session.getAttribute("access_site");
String access_dept=(String)session.getAttribute("access_dept");

// Lines 610–614 — filter values taken from request, not compared to session:
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
String loc_cd = request.getParameter("loc_cd")==null?"":request.getParameter("loc_cd");
String dept_cd = request.getParameter("dept_cd")==null?"":request.getParameter("dept_cd");

// Line 1008 — cust_cd echoed to hidden form field for submission:
<input type="hidden" name="cust_cd" value="<%=loc_cd %>">
```
The servlet handler `conf_driv_setting_ftp` (line 142–144 of `Frm_saveuser.doPost`) similarly receives `cust_cd` from the request.

**Recommendation:** After reading `cust_cd` from the request parameter, compare it against `session.getAttribute("access_cust")` when `access_level > 1`. If the level restricts the user to one customer, reject mismatched `cust_cd` values at both the JSP and the servlet. The servlet handler must also enforce this independently.

---

### Finding A12c-8

**File:** All five JSP files — `frm_conf_firmware_upg.jsp` (line 605), `frm_conf_firmware_upg_bean.jsp` (line 606), `frm_conf_firmware_display.jsp` (line 163), `frm_conf_driv_setting.jsp` (line 731), `frm_impact_setting.jsp` (line 698)
**Severity:** HIGH
**Category:** Cross-Site Request Forgery (CSRF) — No Token on State-Changing Forms

**Description:**
All five pages present HTML forms that POST to `../servlet/Frm_saveuser`. None of the forms contain a CSRF token (hidden field carrying a session-bound random nonce). The forms accept standard `application/x-www-form-urlencoded` POSTs with predictable field names. An attacker who can induce an authenticated user to visit a malicious page can cause that user's browser to silently submit firmware upgrade dispatch, driver memory management, or impact calibration commands to real fleet devices. The firmware dispatch forms are particularly dangerous: a CSRF attack could instruct devices at an entire customer site to re-flash themselves.

**Evidence:**
```html
<!-- frm_conf_firmware_upg.jsp line 605 — no CSRF token -->
<form method="post" action="../servlet/Frm_saveuser">
...
<input type="hidden" name="op_code" value="conf_firmware_upg">
<!-- no <input type="hidden" name="csrf_token" value="..."> anywhere in form -->

<!-- frm_conf_driv_setting.jsp line 731 -->
<form method="post" action="../servlet/Frm_saveuser">
...
<input type="hidden" name="op_code" value="conf_driv_setting">
```

**Recommendation:** Generate a cryptographically random per-session CSRF token on login (e.g., `UUID.randomUUID().toString()`), store it in the session, include it as a hidden field in every state-changing form, and validate it in `Frm_saveuser.doPost()` before dispatching any operation.

---

### Finding A12c-9

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_driv_setting.jsp`
**Lines:** 622–627
**Severity:** MEDIUM
**Category:** Authentication — Null Pointer Risk on Absent Session Attribute

**Description:**
`frm_conf_driv_setting.jsp` includes `Expire.jsp` (which forwards to login if the session or `user_cd` is null), but immediately after, calls `access_level.equalsIgnoreCase("")` on line 627 without a null guard. If `access_level` was never written to the session, `session.getAttribute("access_level")` returns `null`, and the `equalsIgnoreCase` call throws a `NullPointerException`. This surfaces as an HTTP 500 error and may expose a stack trace, revealing internal class names and server paths. The same pattern exists in `frm_impact_setting.jsp` at line 586 and `frm_conf_firmware_upg_bean.jsp` at line 537 (though the bean page has no Expire.jsp guard at all, compounding this).

**Evidence:**
```java
// frm_conf_driv_setting.jsp lines 622–627:
String access_level = (String)session.getAttribute("access_level");
// ... access_level may be null if attribute was never set ...
if(access_level.equalsIgnoreCase(""))   // NullPointerException if null
{
    access_level = "5";
}
```

**Recommendation:** Change to `if(access_level == null || access_level.equalsIgnoreCase(""))` in all affected pages. Alternatively, initialise `access_level` with `session.getAttribute("access_level") != null ? (String)session.getAttribute("access_level") : "5"` in a single assignment.

---

### Finding A12c-10

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_firmware_upg.jsp` and `frm_conf_firmware_upg_bean.jsp`
**Lines (upg):** 671–675; **(upg_bean):** 678–682
**Severity:** MEDIUM
**Category:** Firmware Dispatch — Version String Not Server-Side Validated; Path Traversal Possible

**Description:**
The firmware version string (`message` parameter, submitted as the selected `<option>` from the dropdown) is taken directly from the request and concatenated into an FTPF command path:
```
FTPF=<server>,<port>,<user>,<pass>,<uploadfolder><message>/FleetMS.bin
```
The value is not validated against the list of legitimate firmware versions (which the page fetches from the DB for display only). An attacker who bypasses the UI and submits an arbitrary `message` value could attempt path traversal (e.g., `../../etc/`) or point devices at a non-existent or attacker-controlled path on the firmware FTP server. While exploitation depends on how the telematics device parses the FTPF path, this represents a server-side trust failure — the server constructs a command string for physical devices using unvalidated client input.

**Evidence:**
```java
// conf_firmware_upg_bean, Frm_saveuser.java line 10211:
String msg = "FTPF="+LindeConfig.firmwareserver+","+RuntimeConf.firmwareport+","
    +RuntimeConf.firmwareuser+","+RuntimeConf.firmwarepass+","
    +RuntimeConf.firmwareuploadfolder+message+"/FleetMS.bin";
// message = request.getParameter("message") — never validated against DB version list
```

**Recommendation:** After reading `message` from the request, perform a server-side query to confirm the value exists in the `FMS_VER_STORE` (or equivalent firmware version table) before constructing the FTPF string. Reject and return an error for any value not in the approved list. This also mitigates the SQL injection surface on the same field.

---

### Finding A12c-11

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_impact_setting.jsp`
**Lines:** 453–467 (JavaScript `sendSlidersSettings()`)
**Severity:** MEDIUM
**Category:** Impact Calibration — Sensitive Operation Dispatched via Unauthenticated AJAX Without CSRF Token

**Description:**
The impact slider calibration settings are sent via an inline `$.ajax()` POST directly to `../servlet/Frm_saveuser` with `op_code=set_fssxmulti`. This AJAX call is constructed entirely in client-side JavaScript without any CSRF token. Because it is a same-origin POST with standard form-encoded content, a cross-origin CSRF attack using a simple HTML form (not fetch/XHR) could trigger it. The result is that an attacker could silently re-calibrate impact detection thresholds on any vehicle the victim user can access.

**Evidence:**
```javascript
// frm_impact_setting.jsp lines 452–467:
$.ajax({
    cache:false,
    url:'../servlet/Frm_saveuser',
    data:'op_code=set_fssxmulti&fsss_multi='+fsss_multi+'&fssx_multi='+fssx_multi+'&veh_cd='+veh_cd + extra,
    async:false,
    type:'POST',
    success:function(){ ... },
    error:function(){ ... }
});
// No CSRF token included in data string
```

**Recommendation:** Include the session CSRF token (see A12c-8) in the AJAX `data` parameter and validate it in the servlet before processing `set_fssxmulti`.

---

### Finding A12c-12

**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_conf_driv_setting.jsp`
**Lines:** 1014
**Severity:** LOW
**Category:** Information Exposure — Access Level Written to Hidden Form Field

**Description:**
The session's `access_level` value is written to a hidden form field `alevel` and submitted with the form. While the filter bean reads `access_level` from the server session for display-side data scoping, the `alevel` field is also echoed back to the client where a user can alter it before submission. The JavaScript for the `site` and `dep` dropdowns reads `document.forms[0].alevel.value` to decide whether to show "All" options (lines 52–56, 107–111). Client-side UI logic gated on a user-modifiable hidden field is trivially bypassable — a user can set `alevel=1` and force the "All" option to appear in the dropdown without having the corresponding server-side permission level.

**Evidence:**
```html
<!-- frm_conf_driv_setting.jsp line 1014 -->
<input type="hidden" name="alevel" value="<%=access_level %>"/>
```
```javascript
// line 52–56 in frm_conf_driv_setting.jsp stateChanged():
var alevel = document.forms[0].alevel.value;
if(alevel<3) {
    document.forms[0].site.options[rec.childNodes.length]=new Option("All","all");
}
```

**Recommendation:** Access level enforcement must remain entirely server-side. Remove the `alevel` hidden field. If the JavaScript needs to know the access level for UI purposes, embed it in the page as a JavaScript constant set from the session at render time rather than as a submittable form field.

---

### Finding A12c-13

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\src\com\torrent\surat\fms6\master\Frm_saveuser.java`
**Lines:** 34–36
**Severity:** MEDIUM
**Category:** Concurrency / Race Condition — SingleThreadModel Deprecated, Shared State

**Description:**
`Frm_saveuser` implements the deprecated `javax.servlet.SingleThreadModel` interface. The class has multiple instance-level fields (`dbcon`, `queryString`, `message`, `url`, `stmt`, `rset`, `stmt1`, `rset1`) that are mutated per-request. While `SingleThreadModel` serialises requests in theory, it was removed from the Servlet specification in Servlet 2.4 and has no practical concurrency guarantee in modern containers. Under load, concurrent requests processed by multiple servlet instances from the container pool can corrupt each other's `queryString`, `message`, or `url` state, potentially leaking one user's firmware dispatch response to another user's session, or producing incorrect SQL queries.

**Evidence:**
```java
// Frm_saveuser.java lines 34–36:
@SuppressWarnings("deprecation")
public  class Frm_saveuser extends HttpServlet implements SingleThreadModel {
    private  Connection dbcon = null;
    private  String queryString = "";
    private  String message = "";
    private  String url="";
    private  Statement stmt = null;
    private  ResultSet rset = null;
```

**Recommendation:** Remove `SingleThreadModel`. Move all mutable state (`dbcon`, `stmt`, `rset`, `queryString`, `message`, `url`) to local variables within `doPost()` and the individual handler methods. Use try-with-resources for DB connections and statements.

---

## Summary Table

| ID | File | Lines | Severity | Category |
|----|------|-------|----------|----------|
| A12c-1 | frm_conf_firmware_upg.jsp | 519–538 | CRITICAL | Missing Session Check |
| A12c-2 | frm_conf_firmware_display.jsp | 72–91 | CRITICAL | Missing Session Check |
| A12c-3 | Frm_saveuser.java | 54–80, 177–181 | CRITICAL | Servlet Missing Auth |
| A12c-4 | Frm_saveuser.java | 10204, 10264 | CRITICAL | IDOR / Cross-Customer Firmware Dispatch |
| A12c-5 | Frm_saveuser.java | 10211, 10220–10304 | HIGH | SQL Injection |
| A12c-6 | All 5 JSPs | Multiple | HIGH | Reflected/Stored XSS |
| A12c-7 | frm_conf_driv_setting.jsp | 610–625, 731 | HIGH | IDOR Driver Settings |
| A12c-8 | All 5 JSPs | Form elements | HIGH | CSRF — No Token |
| A12c-9 | frm_conf_driv_setting.jsp, frm_impact_setting.jsp, frm_conf_firmware_upg_bean.jsp | 622–627 | MEDIUM | NPE / Auth Bypass Risk |
| A12c-10 | Frm_saveuser.java | 10211, 10343–10376 | MEDIUM | Path Traversal / Firmware Version Unvalidated |
| A12c-11 | frm_impact_setting.jsp | 452–467 | MEDIUM | CSRF on AJAX Calibration |
| A12c-12 | frm_conf_driv_setting.jsp | 1014 | LOW | Access Level in Hidden Field |
| A12c-13 | Frm_saveuser.java | 34–36 | MEDIUM | Concurrency / Shared State |

**Total findings: 13**

---

*End of audit pass 1 — master-jsps-config*
