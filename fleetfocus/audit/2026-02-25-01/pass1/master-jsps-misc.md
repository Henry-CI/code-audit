# Security Audit: master/ JSPs (Miscellaneous)
**Audit ID:** A12-misc
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Auditor:** Agent A12-misc

---

## STEP 3 — Reading Evidence

### 1. chk_dup_acode.jsp

**Path:** `master/chk_dup_acode.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:** None (no session include)

**Scriptlet block (lines 6–26):**
- Sets XML content type
- Reads `acode` and `usr_cd` from request parameters (unchecked, no session guard)
- Passes both to `Databean_getuser` with op_code `get_dup_acode_ajax`
- Calls `filter.init()` and retrieves `getDup_acode()` count
- Builds raw XML string using string concatenation and prints to output

**`<%= %>` expressions:** None in HTML (XML output only via `out.println`)

**No session include, no CSRF token, no authentication check.**

---

### 2. chk_dup_card.jsp

**Path:** `master/chk_dup_card.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:** None (no session include)

**Scriptlet block (lines 6–41):**
- Sets XML content type
- Reads `bt`, `cpre`, `cid`, `ccd`, `scd`, `usr_cd`, `hid_type`, `id_type`, `wiegand` from request parameters (all unchecked)
- Passes all to `Databean_getuser` with op_code `get_dup_ajax`
- Calls `filter.init()` and retrieves `getDup_card()` count
- Builds raw XML string and prints

**`<%= %>` expressions:** None in HTML (XML output only via `out.println`)

**No session include, no CSRF token, no authentication check.**

---

### 3. edit_dept_name.jsp

**Path:** `master/edit_dept_name.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present

**Scriptlet block (lines 27–39):**
- Reads `user_cd`, `loc_cd`, `dept_cd`, `loc_nm`, `form_cd`, `message` from request parameters
- `loc_nm` is null-checked and "null"-string-checked

**`<%= %>` expressions:**
- Line 46: `<%=location_nm %>` — in `<b>` tag heading (unescaped)
- Line 50: `<%=location_nm %>` — in `input value=""` attribute (unescaped)
- Line 54: `<%=message %>` — raw rendered to HTML (unescaped)
- Line 58: inline `onclick` attribute JavaScript string
- Line 62: `<%=user_cd %>` — in hidden input value (unescaped)
- Line 63: `<%=location_cd %>` — in hidden input value (unescaped)
- Line 64: `<%=dept_cd %>` — in hidden input value (unescaped)
- Line 66: `<%=form_cd %>` — in hidden input value (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**

---

### 4. edit_site_address.jsp

**Path:** `master/edit_site_address.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present

**Scriptlet block (lines 27–40):**
- Reads `user_cd`, `loc_cd`, `loc_nm`, `st`, `addr`, `form_cd`, `message` from request parameters
- `addr` is null-checked and "null"-string-checked

**`<%= %>` expressions:**
- Line 47: `<%=location_nm %>` and `<%=state %>` — in `<b>` heading (unescaped)
- Line 51: `<%=addr %>` — in `input value=""` attribute (unescaped)
- Line 55: `<%=message %>` — raw rendered to HTML (unescaped)
- Line 63: `<%=user_cd %>` — hidden input (unescaped)
- Line 64: `<%=location_cd %>` — hidden input (unescaped)
- Line 66: `<%=form_cd %>` — hidden input (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**

---

### 5. edit_site_name.jsp

**Path:** `master/edit_site_name.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present

**Scriptlet block (lines 27–39):**
- Reads `user_cd`, `loc_cd`, `loc_nm`, `st`, `form_cd`, `message` from request parameters

**`<%= %>` expressions:**
- Line 46: `<%=location_nm %>` and `<%=state %>` — in `<b>` heading (unescaped)
- Line 50: `<%=location_nm %>` — in `input value=""` attribute (unescaped)
- Line 54: `<%=message %>` — raw rendered to HTML (unescaped)
- Line 62: `<%=user_cd %>` — hidden input (unescaped)
- Line 63: `<%=location_cd %>` — hidden input (unescaped)
- Line 65: `<%=form_cd %>` — hidden input (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**

---

### 6. frm_new_customer.jsp

**Path:** `master/frm_new_customer.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present

**Scriptlet block (lines 111–164):**
- Reads `message`, `usr_cd`, `gp_cd`, `loc_cd`, `st_dt`, `end_dt`, `search_crit`, `form_cd` from request parameters
- Retrieves customer data from `Databean_getuser` with op_code `customer_add`
- Retrieves `usr_nm`, `usr_fnm`, `usr_lnm`, `usr_email`, `usr_addr`, `usr_pno`, `usr_mno`, `usr_status`, `usr_desc`, `usr_gmtp`, `usr_cno`, `usr_branch`, `usr_cont_no`, `usr_cont_dt`, `usr_gp`

**`<%= %>` expressions:**
- Line 166 (onload): `<%=usr_gp %>`, `<%=usr_status %>` — injected into JS string (unescaped)
- Line 172: `<%=form_nm %>` — heading (unescaped)
- Line 179: `<%=usr_nm %>` — input value (unescaped)
- Line 191: `<%=usr_cont_no %>` — input value (unescaped)
- Line 197: `<%=usr_cont_dt %>` — input value (unescaped)
- Line 217: `<%=usr_gmtp %>` — input value (unescaped)
- Line 223: `<%=usr_cno %>` — input value (unescaped)
- Line 230: `<%=usr_email %>` — input value (unescaped)
- Line 251: `<%=usr_fnm %>` — input value (unescaped)
- Line 257: `<%=usr_lnm %>` — input value (unescaped)
- Line 265: `<%=usr_pno %>` — input value (unescaped)
- Line 270: `<%=usr_mno %>` — input value (unescaped)
- Line 278: `<%=usr_addr %>` — inside `<TEXTAREA>` (unescaped)
- Line 288: `<%=mach_pic %>` — input value (unescaped)
- Line 302: `<%=vpic_list.get(i) %>` — select option value and text (unescaped)
- Line 310: `<%=mach_pic %>` — inside `img src` attribute (unescaped)
- Line 316: `<%=gp_cd %>`, `<%=loc_cd %>`, `<%=st_dt %>`, `<%=end_dt %>`, `<%=search_crit %>`, `<%=form_cd %>` — in JS onclick string (unescaped)
- Line 321: `<%=message %>` — raw rendered to HTML (unescaped)
- Lines 325–332: multiple hidden inputs (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**

---

### 7. frm_new_department.jsp

**Path:** `master/frm_new_department.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present
- `<%@ include file="../menu/menu.jsp" %>` (line 95) — navigation menu

**Scriptlet block (lines 54–71):**
- Reads `message`, `form_cd` from request parameters
- Retrieves division/department list from `Databean_getuser` with op_code `dep_add`

**`<%= %>` expressions:**
- Line 7: `<%=LindeConfig.systemName %>` — page title (unescaped)
- Line 117: `<%=form_nm %>` — heading (unescaped)
- Line 143: `<%=message %>` — raw rendered to HTML (unescaped)
- Line 165: `<%=group_cd.get(i)%>`, `<%=group_nm.get(i)%>`, `<%=group_desc.get(i)%>` — in JS onclick attribute (unescaped, XSS via DB data)
- Line 167: `<%=group_nm.get(i) %>` — table cell (unescaped)
- Line 170: `<%=group_desc.get(i) %>` — table cell (unescaped)
- Line 178: `<%=form_cd %>` — hidden input (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**

---

### 8. frm_customer_rel.jsp

**Path:** `master/frm_customer_rel.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present
- `<%@ include file="../menu/menu.jsp" %>` (line 353) — navigation menu

**Scriptlet block (lines 246–316):**
- Reads `gp_cd`, `user_cd`, `gp_cd1`, `user_cd1`, `loc_cd`, `type_cd`, `form_cd`, `message` from request parameters
- Reads `user_cd` from session (`session.getAttribute("user_cd")`) at line 258 for the internal `ucd` passed to the filter
- Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session for access control
- Calls `filter.init()` and retrieves site/customer relationship lists
- NOTE: The `user_cd` request parameter is used as `filter.setSet_cust_cd(user_cd)` — not the session value — to drive which customer's sites are displayed

**`<%= %>` expressions (selection):**
- Line 318 (body onload): `<%=user_cd %>` — in JS string (unescaped)
- Line 374: `<%=form_nm %>` — heading (unescaped)
- Line 396: `<%=group_cd.get(i)%>`, `<%=group_nm.get(i) %>` — select option (unescaped)
- Line 460: `<%=user %>` — displayed in heading (unescaped)
- Line 453: `<%=message %>` — raw rendered to HTML (unescaped)
- Lines 493–494: `<%=Vcust_rel_cd.get(i) %>`, `<%=Vcust_rel_usr.get(i) %>`, `<%=Vcust_rel_usr_st.get(i) %>` — in JS onclick attribute and table cell (unescaped)
- Line 500–501: `<%=Vcust_rel_cd.get(i) %>`, `<%=Vcust_rel_addr.get(i) %>`, `<%=Vcust_rel_usr.get(i) %>`, `<%=Vcust_rel_usr_st.get(i) %>` — in JS onclick attribute (unescaped)
- Line 506: `<%=Vcust_rel_cd.get(i) %>`, `<%=Vcust_rel_usr.get(i) %>` — radio value and onclick (unescaped)
- Line 511: `<%=user_cd %>`, `<%=Vcust_rel_cd.get(i) %>` — in onclick JS (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`. Debug code present (line 322–325): `alert($(this).serialize())` left in production.**

---

### 9. frm_customer_vehicle_rel.jsp

**Path:** `master/frm_customer_vehicle_rel.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present
- `<%@ include file="../menu/menu.jsp" %>` (line 346) — navigation menu

**Scriptlet block (lines 249–323):**
- Reads `gp_cd`, `user_cd`, `veh_typ_cd`, `veh_cd`, `loc_cd`, `dep_cd`, `form_cd`, `message` from request parameters
- Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session
- `user_cd` from request parameter used as `filter.setSet_cust_cd(user_cd)`

**`<%= %>` expressions (selection):**
- Line 324 (body onload): multiple request-derived values injected into JS (unescaped)
- Line 368: `<%=form_nm %>` — heading (unescaped)
- Line 388: `<%=Vuser_cd.get(i)%>`, `<%=Vuser_nm.get(i) %>` — select options (unescaped)
- Line 450: `<%=message %>` — raw HTML (unescaped)
- Line 458: `<%=user %>`, `<%=loc %>`, `<%=dept %>` — table heading (unescaped)
- Line 475: `<%=Vveh_rel_tp.get(i) %>` — table cell (unescaped)
- Line 478: `<%=Vveh_rel_nm.get(i) %>` — table cell (unescaped)
- Line 483: `<%=tmp %>` — table cell (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**

---

### 10. frm_customer_vehicle_reset.jsp

**Path:** `master/frm_customer_vehicle_reset.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present
- `<%@ include file="../menu/menu.jsp" %>` (line 413) — navigation menu

**Scriptlet block (lines 315–390):**
- Reads `gp_cd`, `user_cd`, `veh_typ_cd`, `veh_cd`, `loc_cd`, `dep_cd`, `form_cd`, `message` from request parameters
- Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session
- `user_cd` from request parameter used as `filter.setSet_cust_cd(user_cd)`
- op_code is `customer_veh_reset`
- Hardcoded hidden input `res_gmtp` value `"Y"` (line 496): reset GMTP prefix is always forced on

**`<%= %>` expressions (selection):**
- Line 391 (body onload): request-derived values injected into JS (unescaped)
- Line 435: `<%=form_nm %>` — heading (unescaped)
- Line 445: `<%=Vuser_cd.get(i)%>`, `<%=Vuser_nm.get(i) %>` — select options (unescaped)
- Line 509: `<%=message %>` — raw HTML (unescaped)
- Line 524: `<%=user %>`, `<%=loc %>`, `<%=dept %>` — heading (unescaped)
- Line 541: `<%=Vveh_rel_tp.get(i) %>` — table cell (unescaped)
- Line 544: `<%=Vveh_rel_nm.get(i) %>` — table cell (unescaped)
- Line 549: `<%=tmp %>` — table cell (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**
**Reset operation is NOT scoped to the authenticated user's customer — `user_cd` comes from the request, not the session.**

---

### 11. frm_mastercode.jsp

**Path:** `master/frm_mastercode.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present
- `<%@ include file="../menu/menu.jsp" %>` (line 232) — navigation menu

**Scriptlet block (lines 23–133):**
- Reads `gp_cd`, `user_cd`, `model_cd`, `st_dt`, `to_dt`, `loc_cd`, `dept_cd`, `form_cd` from request parameters
- Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session
- Uses `Databean_report` (not `Databean_getuser`) with op_code `key_hour`
- Retrieves customer list, site list, department list and vehicle/slot data for master code generation
- `user_cd` from request parameter used as `filter.setSet_cust_cd(user_cd)` — not validated against session

**`<%= %>` expressions (selection):**
- Line 7: `<%=LindeConfig.systemName %>` — title (unescaped)
- Line 10: `<%=LindeConfig.systemName %>` — title (unescaped)
- Line 250: `<%=form_nm%>` — page heading (unescaped)
- Lines 257–258: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — select options (unescaped)
- Lines 268–269: `<%=Vuser_cd.get(i) %>`, `<%=Vuser_nm.get(i) %>` — select options (unescaped)
- Lines 276–277: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — select options (unescaped)
- Lines 352–353 (JS inline): `<%if(al<3){ %>` — server-side access level conditionally renders "All" site option
- Lines 385–386 (JS inline): `<%if(al<4){ %>` — server-side access level conditionally renders "All" dept option

**Form action is `frm_mastercode_step2.jsp` (GET method). No CSRF token.**
**Access level check exists in server-side rendering of "All" option, but customer filter is driven by request parameter, not session.**

---

### 12. frm_hourcount_config.jsp

**Path:** `master/frm_hourcount_config.jsp`

**Imports:**
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>`

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session guard present
- `<%@ include file="../menu/menu.jsp" %>` (line 295) — navigation menu

**Scriptlet block (lines 195–272):**
- Reads `cust_cd`, `loc_cd`, `dept_cd`, `form_cd`, `message` from request parameters
- Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session
- Reads `user_cd` from session at line 229 (`session.getAttribute("user_cd")`) and passes as `filter.setSet_ucd(ucd)`
- `cust_cd` from request parameter used as `filter.setSet_cust_cd(cust_cd)` — not forced from session

**`<%= %>` expressions (selection):**
- Line 7: `<%=LindeConfig.systemName %>` — title (unescaped)
- Line 273 (body onload): `<%=cust_cd %>`, `<%=loc_cd %>`, `<%=dept_cd %>` — in JS string (unescaped)
- Line 317: `<%=form_nm %>` — heading (unescaped)
- Line 326: `<%=vcust_cd.get(i) %>`, `<%=vcust_nm.get(i) %>` — select options (unescaped)
- Line 335: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — select options (unescaped)
- Line 346: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — select options (unescaped)
- Line 362: `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>` — table heading (unescaped)
- Line 380: `<%=vhire_no.get(i) %>` — table cell (unescaped)
- Line 383: `<%=vcount_hour.get(i) %>` — input value (unescaped)
- Line 387: `<%=vveh_cd.get(i)%>`, `<%=i%>` — in onclick JS (unescaped)
- Line 395: `<%=message %>` — raw HTML (unescaped)

**No CSRF token. Form posts to `../servlet/Frm_saveuser`.**

---

## STEP 4 — Security Findings

---

### A12m-1 — CRITICAL — No Authentication on AJAX Duplicate-Check Endpoints

**Files:**
- `master/chk_dup_acode.jsp` (entire file)
- `master/chk_dup_card.jsp` (entire file)

**Severity:** Critical

**Category:** Authentication / Broken Access Control

**Description:**
Both `chk_dup_acode.jsp` and `chk_dup_card.jsp` are AJAX endpoints that accept user input and query the database to check for duplicate account codes and card numbers respectively. Neither file includes `../sess/Expire.jsp` or any other authentication/session check. Any unauthenticated HTTP request can invoke these endpoints, probing whether specific account codes or card IDs exist in the system — effectively enabling enumeration of users, card numbers, and account codes without logging in.

**Evidence:**
```jsp
// chk_dup_acode.jsp — lines 1-4: no <%@ include file="../sess/Expire.jsp" %>
<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>
<%@ page errorPage="../home/ExceptionHandler.jsp" %>
// No session guard — request parameters flow directly to Databean
String acode=request.getParameter("acode") ;
String usr_cd = request.getParameter("usr_cd");
```

```jsp
// chk_dup_card.jsp — lines 1-4: no <%@ include file="../sess/Expire.jsp" %>
String bt=request.getParameter("bt") ;
String cpre = request.getParameter("cpre") ;
String cid = request.getParameter("cid") ;
String ccd = request.getParameter("ccd") ;
// ... all passed to filter without authentication
```

**Recommendation:**
Add `<%@ include file="../sess/Expire.jsp" %>` as the very first directive in both files, identical to the pattern used by all other JSPs in the `master/` directory. Additionally, ensure the servlet/DAO layer also enforces session authentication independently.

---

### A12m-2 — CRITICAL — SQL Injection Risk via Unvalidated Parameters to Databean (chk_dup_acode.jsp, chk_dup_card.jsp)

**Files:**
- `master/chk_dup_acode.jsp` lines 8–18
- `master/chk_dup_card.jsp` lines 8–30

**Severity:** Critical

**Category:** SQL Injection (indirect — parameter flow to DAO)

**Description:**
Both files read multiple request parameters with no validation, sanitisation, or type-checking before passing them directly to `Databean_getuser` setter methods. Since no authentication guard exists (see A12m-1), an anonymous attacker controls all inputs. The actual SQL is in the Databean/DAO layer. If the DAO uses string concatenation to build queries (a pattern confirmed in other files in this audit), these parameters are SQL-injectable. Even if parameterised queries are used, the complete absence of input validation on an unauthenticated endpoint amplifies the risk.

**Evidence:**
```jsp
// chk_dup_acode.jsp lines 8-17
String acode = request.getParameter("acode");    // no validation
String usr_cd = request.getParameter("usr_cd");  // no validation
filter.setSet_acode(acode);
filter.setSet_ucd(usr_cd);
filter.init();  // DAO executes query
```

```jsp
// chk_dup_card.jsp lines 8-30
String bt    = request.getParameter("bt");     // no validation
String cpre  = request.getParameter("cpre");   // no validation
String cid   = request.getParameter("cid");    // no validation
String ccd   = request.getParameter("ccd");    // no validation
String scd   = request.getParameter("scd");    // no validation
// ... all passed directly to filter setters
filter.init(); // DAO executes query
```

**Recommendation:**
Verify that all DAO queries for `get_dup_acode_ajax` and `get_dup_ajax` use parameterised `PreparedStatement` calls. Apply whitelist input validation (e.g., card number fields should only accept numeric or alphanumeric patterns of bounded length) before passing to the DAO. Authentication must also be enforced (A12m-1).

---

### A12m-3 — HIGH — Reflected XSS: Unescaped Request Parameters Rendered in HTML (Multiple Files)

**Files:**
- `master/edit_dept_name.jsp` lines 46, 50, 54
- `master/edit_site_address.jsp` lines 47, 51, 55
- `master/edit_site_name.jsp` lines 46, 50, 54
- `master/frm_new_customer.jsp` lines 172, 179, 191, 217, 223, 230, 251, 257, 265, 270, 278, 288, 310, 316, 321
- `master/frm_new_department.jsp` lines 117, 143, 165, 167, 170
- `master/frm_customer_rel.jsp` lines 453, 460, 493–494, 500–501, 506, 511
- `master/frm_customer_vehicle_rel.jsp` lines 450, 458, 475, 478, 483
- `master/frm_customer_vehicle_reset.jsp` lines 509, 524, 541, 544, 549
- `master/frm_mastercode.jsp` lines 250, 257–258, 268–269, 276–277
- `master/frm_hourcount_config.jsp` lines 362, 380, 383, 395

**Severity:** High

**Category:** Cross-Site Scripting (XSS) — Reflected and Stored

**Description:**
Every file uses raw `<%= expression %>` JSP expression syntax to embed values into HTML output — in table cells, input `value=""` attributes, `<textarea>` bodies, `onclick` JavaScript attributes, and `<img src="">` attributes — with no HTML encoding applied. The JSP expression tag `<%= %>` in standard JSPs does not escape HTML characters. Any value containing `<`, `>`, `"`, `'`, or `&` will be rendered verbatim.

Three distinct attack vectors exist:

1. **Reflected XSS via URL parameters**: Values such as `location_nm`, `addr`, `state`, `message`, `form_cd`, `user_cd` are taken from request parameters and reflected directly. A crafted URL sent to a victim who is already authenticated will execute attacker-controlled JavaScript.

2. **Stored XSS via database values**: Values such as `group_nm`, `group_desc` (department names), `Vcust_rel_usr` (site names), `Vcust_rel_addr` (site addresses), `vhire_no` (fleet hire numbers), `Vuser_nm` (customer names), `Vloc_nm` (location names) are retrieved from the database and rendered without escaping. If an attacker can create or edit a customer name, site name, or department name containing `<script>` tags (via any data-entry form in the system), that payload will execute in the browser of any user viewing these pages.

3. **XSS in JavaScript event handlers**: Values injected into `onclick="..."` or `onload="..."` attributes (e.g., `edit_dept_name.jsp` line 58, `frm_customer_rel.jsp` lines 493–511, `frm_new_customer.jsp` line 316) can break out of JS string context with a single quote, achieving XSS.

**Evidence (representative samples):**
```jsp
// edit_dept_name.jsp line 46 — location_nm from request parameter
<b>Edit name for dept:<%=location_nm %></b>

// edit_dept_name.jsp line 54 — message from request parameter
<%=message %>

// frm_new_department.jsp line 165 — DB values injected into onclick JS
onclick="set_editvalues('<%=group_cd.get(i)%>','<%=group_nm.get(i)%>','<%=group_desc.get(i)%>');"

// frm_customer_rel.jsp lines 500-501 — DB address value in onclick
onclick="open_addr_edit('<%=Vcust_rel_cd.get(i) %>','<%=Vcust_rel_addr.get(i) %>'
,'<%=Vcust_rel_usr.get(i) %>','<%=Vcust_rel_usr_st.get(i) %>');"

// frm_new_customer.jsp line 278 — address in textarea (no escaping needed for HTML but
// quotes in value can break surrounding JS context)
<TEXTAREA NAME="addr" ROWS="3" cols="60"><%=usr_addr %></TEXTAREA>

// frm_hourcount_config.jsp line 395 — message from request
<p style="color: red;font-weight:bold;font-size:16px" align="center"><%=message %></p>
```

**Recommendation:**
Replace all `<%= value %>` expressions with JSTL `<c:out value="${value}" escapeXml="true"/>` or use a utility method such as `ESAPI.encoder().encodeForHTML(value)` for HTML contexts. For JavaScript event handler attributes, use `ESAPI.encoder().encodeForJavaScript(value)`. For `value=""` HTML attributes, use `ESAPI.encoder().encodeForHTMLAttribute(value)`. Import ESAPI or enable JSTL and systematically replace all raw expression tags in these files.

---

### A12m-4 — HIGH — IDOR / Tenant Isolation: customer_id Taken from Request, Not Session (Multiple Files)

**Files:**
- `master/frm_customer_rel.jsp` lines 251, 288
- `master/frm_customer_vehicle_rel.jsp` lines 254, 288
- `master/frm_customer_vehicle_reset.jsp` lines 320, 355
- `master/frm_mastercode.jsp` lines 28, 60
- `master/frm_hourcount_config.jsp` lines 201, 234

**Severity:** High

**Category:** Insecure Direct Object Reference (IDOR) / Broken Tenant Isolation

**Description:**
In all five pages, the customer identifier (`user_cd` / `cust_cd`) is read from the URL/request parameter and passed directly to the data access layer as the customer filter. A lower-privileged user who knows (or guesses) another customer's code can simply change the `user_cd` parameter in the URL and retrieve data scoped to that other customer — including their sites, departments, vehicles, hour count configurations, and master code (override code) generation slots.

While `access_level`, `access_cust`, `access_site`, and `access_dept` are read from the session and passed to the filter bean, the actual primary customer discriminator (`user_cd`/`cust_cd`) itself is still taken from the request parameter. It is unclear from the JSP layer alone whether the DAO enforces that the session's `access_cust` constrains the query result relative to the supplied `user_cd`. The absence of an explicit server-side check of the form "if `user_cd` != `session.access_cust` then reject" in the JSP layer means tenant isolation is entirely dependent on the DAO implementation, which is opaque from this review.

The `frm_mastercode.jsp` case is particularly sensitive: this page is used to generate and send master override codes to fleet devices (seen by reference to `frm_mastercode_step2.jsp` and `rpt_override_code_lst.jsp`). An attacker who can specify an arbitrary `user_cd` may be able to trigger master code generation for a vehicle fleet belonging to another customer.

**Evidence:**
```jsp
// frm_customer_vehicle_reset.jsp lines 319-320
String user_cd = request.getParameter("user_cd")==null?"":request.getParameter("user_cd");
// ...
filter.setSet_cust_cd(user_cd);  // No cross-check against session access_cust

// frm_mastercode.jsp lines 28, 60
String user_cd = request.getParameter("user_cd")==null?"":request.getParameter("user_cd");
// ...
filter.setSet_cust_cd(user_cd);  // Controls which customer's master codes are visible/sendable

// frm_hourcount_config.jsp lines 201, 234
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
// ...
filter.setSet_cust_cd(cust_cd);  // Controls which customer's vehicle hour configs are shown
```

**Recommendation:**
For customer-scoped operations, derive the customer identifier from the session (`session.getAttribute("access_cust")`) rather than from the request parameter. Where legitimate use cases require admin users to select arbitrary customers, enforce an explicit server-side check: compare the requested `user_cd` against the list of customers the authenticated user is permitted to access (as returned by the access control layer) and reject the request if the requested customer is not in the permitted set.

---

### A12m-5 — HIGH — Sensitive Operation (Vehicle Reclaim) Not Scoped to Session Customer

**File:** `master/frm_customer_vehicle_reset.jsp`

**Severity:** High

**Category:** Insecure Direct Object Reference / Privilege Escalation

**Description:**
The "Reclaim Vehicle" operation (op_code `customer_veh_reset`) dissociates a vehicle from its current customer, freeing it for reassignment. The vehicle and customer are both specified entirely via request parameters (`veh_cd`, `user_cd`, `loc_cd`, `dep_cd`). There is no server-side check in the JSP layer confirming that the authenticated user has permission to reclaim vehicles from the specified customer. The hardcoded hidden field `res_gmtp` with value `"Y"` (line 496) forces the GMTP prefix reset unconditionally whenever the form is submitted.

An authenticated user (even a customer-level user) who can craft or replay a POST request with a different `user_cd` and `veh_cd` may be able to reclaim a vehicle from an unrelated customer, disrupting fleet assignments and potentially the GMTP prefix data integrity for that vehicle.

**Evidence:**
```jsp
// frm_customer_vehicle_reset.jsp line 319-320
String user_cd = request.getParameter("user_cd")==null?"":request.getParameter("user_cd");
// ...
// line 496: always resets GMTP prefix
<input type="hidden" name="res_gmtp" value="Y" >

// line 558: operation posted to servlet
<input type="hidden" name="op_code" value="customer_veh_reset">
// user_cd, veh_cd, loc_cd, dep_cd all from request parameters
```

**Recommendation:**
Validate server-side (in the servlet `Frm_saveuser` handling `customer_veh_reset`) that the vehicle being reclaimed belongs to a customer the authenticated session is authorised to manage. Verify the vehicle-customer relationship using a query that joins against the session's `access_cust` value rather than the client-supplied parameter.

---

### A12m-6 — HIGH — frm_mastercode.jsp: Master Override Code Generation Not Restricted to Admin

**File:** `master/frm_mastercode.jsp`

**Severity:** High

**Category:** Insufficient Authorization / Sensitive Functionality Exposure

**Description:**
`frm_mastercode.jsp` allows a user to generate and transmit master override codes ("mastercodes") to fleet devices. The page's comment confirms the purpose: buttons `Send Selected` and `Send All` trigger `frm_mastercode_step2.jsp`, which dispatches override codes to physical fleet control devices. The customer and site for which override codes are generated are controlled by request parameters (`user_cd`, `loc_cd`), not session-bound values.

The only access-level restriction visible in the JSP is a conditional rendering of "All Sites" and "All Departments" dropdown options based on `al` (access level integer). Lower-level users simply do not see the "All" option in the UI — but there is no server-side enforcement preventing a lower-privileged user from manually submitting a request with `site_cd=all` or an arbitrary `user_cd`. The page is accessible to any authenticated session without an admin-only access level gate.

Generating unauthorised master override codes for a vehicle provides physical-layer access (the override code can be used at the device to bypass normal access restrictions). This is a significant real-world impact beyond data disclosure.

**Evidence:**
```jsp
// frm_mastercode.jsp lines 352-387 — UI-only restriction, no server-side gate
<%if(al<3){ %>
document.frm_mastercode.site.options[i]=new Option("All","all");
<%}%>
// ...
<%if(al<4){ %>
document.frm_mastercode.dept.options[i]=new Option("All","all");
<%}%>

// lines 579-580 — customer from request parameter in AJAX call
var params = "user_cd="+$('#usr').val()+"&loc_cd="+$('#site').val()+"&dep_cd="+$('#dept').val()+serial;
removableDialog("Send Selected Mastercodes",'frm_mastercode_step2.jsp?'+params,800,680);
```

**Recommendation:**
Implement a server-side access level gate at the top of `frm_mastercode.jsp` and in `frm_mastercode_step2.jsp`: check that `al` (access level from session) meets a minimum admin threshold before rendering any content or processing any submission. In `frm_mastercode_step2.jsp` (the actual code-sending endpoint), re-validate the session's `access_cust` against the requested `user_cd` to ensure the requesting user is authorised to generate codes for that specific customer.

---

### A12m-7 — HIGH — frm_hourcount_config.jsp: Hour Count Configuration Driven by Request Parameter

**File:** `master/frm_hourcount_config.jsp`

**Severity:** High

**Category:** IDOR / Tenant Isolation

**Description:**
The hour count (contracted hours per year) per vehicle is a billing-sensitive configuration. `frm_hourcount_config.jsp` reads `cust_cd`, `loc_cd`, and `dept_cd` from request parameters to determine which customer's vehicle fleet is displayed and configurable. While `session.getAttribute("user_cd")` is read and passed as `filter.setSet_ucd(ucd)`, the primary customer discriminator `cust_cd` is still request-controlled. An attacker who changes `cust_cd` in the URL can view (and potentially modify, via the Update button) contracted hour settings for any other customer's vehicles.

**Evidence:**
```jsp
// frm_hourcount_config.jsp lines 201, 234-235
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
// ...
String ucd = ""+session.getAttribute("user_cd");  // session user cd stored separately
filter.setSet_ucd(ucd);         // session user_cd passed here
filter.setSet_cust_cd(cust_cd); // but customer filter is from request — not session
```

**Recommendation:**
Derive `cust_cd` from the session's `access_cust` attribute for single-customer users. For multi-customer admin users, validate that the requested `cust_cd` is within the set of customers the session's `access_cust` grants access to, using a server-side allowlist check before passing to the DAO.

---

### A12m-8 — MEDIUM — Missing CSRF Protection on All State-Changing Forms

**Files:** All 12 files that contain `<form method="post" ...>`:
- `master/edit_dept_name.jsp` (line 42)
- `master/edit_site_address.jsp` (line 43)
- `master/edit_site_name.jsp` (line 42)
- `master/frm_new_customer.jsp` (line 167)
- `master/frm_new_department.jsp` (line 113)
- `master/frm_customer_rel.jsp` (line 371)
- `master/frm_customer_vehicle_rel.jsp` (line 364)
- `master/frm_customer_vehicle_reset.jsp` (line 431)
- `master/frm_mastercode.jsp` (line 251, GET method — also vulnerable)
- `master/frm_hourcount_config.jsp` (line 313)

**Severity:** Medium

**Category:** Cross-Site Request Forgery (CSRF)

**Description:**
None of the state-changing forms include a CSRF token (synchroniser token, double-submit cookie, or SameSite cookie enforcement). Operations include: creating new customers, editing department names, editing site names and addresses, assigning vehicles to customers, reclaiming vehicles (with forced GMTP reset), and updating contracted hour configurations. The master code form uses `method='get'` (line 251), which is additionally vulnerable since the action URL with all parameters is bookmarkable and embeddable in an `<img src="">` tag.

An attacker who can lure an authenticated user to a malicious page can trigger any of these operations silently in the background.

**Evidence:**
```jsp
// edit_dept_name.jsp lines 42-67 — no token
<form method="post" action="../servlet/Frm_saveuser">
  ...
  <input type="hidden" name="op_code" value="dept_name_edit">
  // No <input type="hidden" name="csrf_token" value="...">
</form>

// frm_mastercode.jsp line 251 — GET form for master code send
<form id='frm_mastercode' name='frm_mastercode' action='frm_mastercode_step2.jsp' method='get'>
// No CSRF protection; all parameters visible in URL
```

**Recommendation:**
Implement a synchroniser token pattern: generate a cryptographically random token per session (or per form), store it in the session, embed it as a hidden field in every form, and validate it in `Frm_saveuser` and `frm_mastercode_step2.jsp` before processing. Alternatively, configure `SameSite=Strict` on the session cookie to prevent cross-origin form submissions (does not protect GET-based actions). The master code form should be changed to `method="post"`.

---

### A12m-9 — MEDIUM — Debug/Development Code Left in Production: alert(serialize) in frm_customer_rel.jsp

**File:** `master/frm_customer_rel.jsp`

**Severity:** Medium

**Category:** Information Disclosure / Development Artefact

**Description:**
Lines 321–330 contain a jQuery `$(document).ready` block that intercepts all form submissions and displays the serialised form data in a browser `alert()` dialog. This causes every form submission on `frm_customer_rel.jsp` to be blocked (`e.preventDefault(); return false;`) and display the full form payload — including customer codes, site codes, operation codes, and any entered data — in an alert box. This prevents the actual form from submitting at all, breaking the page's functionality, and exposes internal field names and values to the user (or an attacker observing the screen).

**Evidence:**
```javascript
// frm_customer_rel.jsp lines 321-330
$(document).ready(function(){
    $('form').submit(function(e){
        e.preventDefault();
        alert($(this).serialize());  // Exposes all form data; blocks submission
        return false;
    });
});
```

**Recommendation:**
Remove this block entirely. It appears to be a debugging artefact that was committed to the production branch. Its presence breaks the form's intended functionality and discloses form field names and values.

---

### A12m-10 — LOW — XSS in JavaScript Context: Request Parameters Injected into onload/onclick Attributes

**Files:**
- `master/frm_customer_vehicle_rel.jsp` line 324
- `master/frm_customer_vehicle_reset.jsp` line 391
- `master/frm_customer_rel.jsp` line 318
- `master/edit_dept_name.jsp` line 58
- `master/edit_site_address.jsp` line 59
- `master/edit_site_name.jsp` line 58
- `master/frm_new_customer.jsp` line 316

**Severity:** Low (escalates to High in combination with A12m-3 stored XSS)

**Category:** Cross-Site Scripting (XSS) — DOM/Attribute

**Description:**
In addition to the general reflected XSS covered in A12m-3, these specific locations inject request parameters directly into JavaScript event handler attribute strings without JavaScript encoding. A value containing a single quote will break out of the JS string literal. This is a separate encoding context from HTML body/attribute encoding.

**Evidence:**
```jsp
// frm_customer_vehicle_rel.jsp line 324
<body onload="set('<%=gp_cd %>','<%=user_cd %>','<%=veh_typ_cd %>','<%=veh_cd %>','<%=location_cd %>','<%=dep_cd %>');">
// A value of: ');alert(1);// would break out

// edit_dept_name.jsp line 58
<input type="button" name="b2" value="Close" onclick="close_form('<%=form_cd %>');">
// form_cd from request parameter, unescaped in JS string context
```

**Recommendation:**
For values embedded inside JavaScript string literals within HTML event handler attributes, apply `ESAPI.encoder().encodeForJavaScript(value)` in addition to HTML attribute encoding. Alternatively, move all JavaScript logic to a separate `.js` file and pass values via `data-*` attributes on the HTML elements, reading them in JavaScript — which eliminates the need for server-side JS encoding entirely.

---

### A12m-11 — LOW — Unauthenticated Information Disclosure via chk_dup_acode.jsp and chk_dup_card.jsp (Enumeration)

**Files:**
- `master/chk_dup_acode.jsp`
- `master/chk_dup_card.jsp`

**Severity:** Low (as standalone; Critical when combined with A12m-1)

**Category:** Information Disclosure / User Enumeration

**Description:**
These AJAX endpoints return a count (duplicate check result) that reveals whether a given account code or card number/ID exists in the database. Since no authentication is required (A12m-1), an external attacker can perform automated enumeration of account codes and card identifiers by iterating possible values and observing the response. This leaks whether cards and accounts exist in the system without any authentication.

**Evidence:**
```jsp
// chk_dup_acode.jsp lines 20-25
resp=resp+"<body>";
resp=resp+"<rec>"+"<code>"+cnt+"</code></rec>";  // cnt = "0" or "1"
resp=resp+"</body>";
out.println(resp);
```

**Recommendation:**
In addition to adding authentication (A12m-1), consider whether these endpoints need to be separate JSPs at all. If the duplicate check is only needed during user creation (while a session is active), the check is already protected once authentication is added. Additionally, implement rate limiting on these endpoints to prevent automated enumeration even by authenticated users.

---

## Summary Table

| ID | File(s) | Severity | Category | Summary |
|----|---------|----------|----------|---------|
| A12m-1 | chk_dup_acode.jsp, chk_dup_card.jsp | **Critical** | Authentication | No session check — endpoints fully unauthenticated |
| A12m-2 | chk_dup_acode.jsp, chk_dup_card.jsp | **Critical** | SQL Injection (risk) | Unvalidated request params flow to DAO on unauthenticated endpoint |
| A12m-3 | 10 files | **High** | XSS (Reflected + Stored) | All `<%= %>` expressions unescaped in HTML, attribute, JS, textarea, and img src contexts |
| A12m-4 | frm_customer_rel, frm_customer_vehicle_rel, frm_customer_vehicle_reset, frm_mastercode, frm_hourcount_config | **High** | IDOR / Tenant Isolation | Customer ID from request parameter, not enforced from session |
| A12m-5 | frm_customer_vehicle_reset.jsp | **High** | IDOR / Privilege Escalation | Vehicle reclaim operation not scoped to session customer |
| A12m-6 | frm_mastercode.jsp | **High** | Insufficient Authorization | Master override code generation accessible without admin gate; customer from request param |
| A12m-7 | frm_hourcount_config.jsp | **High** | IDOR / Tenant Isolation | Hour count config editable for any customer via URL param |
| A12m-8 | 10 files | **Medium** | CSRF | No CSRF token on any state-changing form; master code form uses GET |
| A12m-9 | frm_customer_rel.jsp | **Medium** | Info Disclosure / Dev Artefact | `alert(serialize)` debug code in production breaks form and exposes field data |
| A12m-10 | 7 files | **Low** | XSS (JS Context) | Request params injected into JS event handlers without JS encoding |
| A12m-11 | chk_dup_acode.jsp, chk_dup_card.jsp | **Low** | Info Disclosure / Enumeration | Duplicate-check responses enable unauthenticated account/card enumeration |

**Total findings: 11**
(2 Critical, 5 High, 2 Medium, 2 Low)
