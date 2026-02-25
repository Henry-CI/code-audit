# Security Audit Report — master JSPs: Vehicle & Alert Pages
**Agent:** A12-vehicle
**Audit run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production (confirmed via `.git/HEAD`)
**Date:** 2026-02-25

---

## STEP 3 — READING EVIDENCE

### 1. `C:\Projects\cig-audit\repos\fleetfocus\master\existing_vehicle_lst.jsp`

**Imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session/expiry include
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ include file="../menu/menu.jsp" %>` (line 371)

**Scriptlet blocks:**
- Lines 293–347: Main server-side logic. Reads request parameters (`veh_typ_cd`, `loc_cd`, `st_dt`, `end_dt`, `search_crit`, `form_cd`), reads `user_cd` from session, passes all to `Databean_getuser` filter bean, calls `filter.init()`, retrieves result ArrayLists.
- Lines 402–403, 412–413, 477–503: Loop scriptlets rendering vehicle rows from DB-sourced ArrayLists.
- Lines 471–474, 491–500, 497–500: Conditional rendering of CANBus/edit columns based on `fmod` flag.

**`<%= %>` expressions (all DB-sourced unless noted):**
- Line 7: `<%=LindeConfig.systemName %>` — system config constant, not user-controlled.
- Line 349: `<%=veh_typ_cd %>` and `<%=loc_cd %>` — **request param-sourced**, written into `onload` JS attribute.
- Line 393: `<%=form_nm %>` — DB-sourced.
- Line 403: `<%=Vveh_typ_cd.get(i) %>`, `<%=Vveh_typ_nm.get(i) %>` — DB-sourced, rendered in `<option>` tags.
- Line 413: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — DB-sourced.
- Line 419: `<%=st_dt %>`, line 425: `<%=end_dt %>` — request param-sourced, written into hidden inputs.
- Line 436: `<%=search_crit %>` — **request param-sourced**, written as `value` of a text input.
- Lines 445–446: `<%=get_gp %>`, `<%=get_loc %>`, `<%=search_crit %>` — DB-sourced (get_gp, get_loc) and request param (search_crit), rendered into HTML table cell.
- Lines 484, 489, 492–494, 498: `<%=Vsereal_no.get(i) %>`, `<%=Vhire_no.get(i) %>`, `<%=Vveh_cd.get(i) %>`, `<%=Vgmtp_id.get(i) %>` — DB-sourced, rendered directly into HTML and **into JavaScript event handler strings** (onClick attributes).
- Line 507: `<%=form_cd %>` — request param-sourced, written into hidden input.

---

### 2. `C:\Projects\cig-audit\repos\fleetfocus\master\existing_cust_vehicle_lst.jsp`

**Imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ include file="../menu/menu.jsp" %>` (line 580)

**Scriptlet blocks:**
- Lines 459–556: Main logic. Reads request params (`veh_typ_cd`, `st_dt`, `end_dt`, `search_crit`, `form_cd`, `cust_cd`, `loc_cd`, `dept_cd`). Reads access control attributes from session (`access_level`, `access_cust`, `access_site`, `access_dept`). Sets all on filter bean, calls `filter.init()`, retrieves ArrayLists. Note: `cust_cd` is taken from request param and passed directly to the filter — it is **not cross-checked** against a session-bound customer value.
- Lines 610–613, 619–621, 633–634, 647–649: Loop scriptlets for dropdown options.
- Lines 706–735: Loop rendering vehicle rows.

**`<%= %>` expressions:**
- Line 7: `<%=LindeConfig.systemName %>` — config constant.
- Line 558: `<%=veh_typ_cd %>`, `<%=cust_cd %>`, `<%=loc_cd %>`, `<%=dept_cd %>` — **request param-sourced**, injected into `onload` JS call.
- Line 602: `<%=form_nm %>` — DB-sourced.
- Lines 611, 612: `<%=vcust_cd.get(i) %>`, `<%=vcust_nm.get(i) %>` — DB-sourced, `<option>` values.
- Lines 620, 621: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — DB-sourced.
- Lines 633, 634: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — DB-sourced.
- Lines 648, 649: `<%=Vveh_typ_cd.get(i) %>`, `<%=Vveh_typ_nm.get(i) %>` — DB-sourced.
- Line 652: `<%=search_crit %>` — **request param-sourced**, rendered in text input `value`.
- Lines 655, 656: `<%=st_dt %>`, `<%=end_dt %>` — request param-sourced, hidden inputs.
- Line 673: `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>`, `<%=get_gp %>`, `<%=search_crit %>` — mixed DB and request param, rendered in heading cell.
- Lines 709, 714, 719–731: `<%=Vsereal_no.get(i) %>`, `<%=Vhire_no.get(i) %>`, `<%=Vveh_cd.get(i) %>`, `<%=Vis_unit.get(i) %>`, `<%=Vgmtp_id.get(i) %>`, `<%=Vccid.get(i) %>`, `<%=vtp.get(i) %>` — DB-sourced, rendered into HTML and **into onClick JS handler strings**.
- Line 738: `<%=form_cd %>` — request param-sourced, hidden input.
- Line 739: `<%=access_level %>` — session-sourced, hidden input.

---

### 3. `C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst.jsp`

**Imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ include file="../menu/menu.jsp" %>` (line 146)

**Scriptlet blocks:**
- Lines 96–122: Reads `message` and `form_cd` from request params. Reads `user_cd` from **session** — critically, alert list is scoped to the session user: `filter.setSet_user_cd(user)`.
- Lines 205–253: Loop rendering alert rows from DB-sourced ArrayLists; inline scriptlet computes human-readable impact labels from integer DB values.

**`<%= %>` expressions:**
- Line 7: `<%=LindeConfig.systemName %>` — config constant.
- Line 167: `<%=form_nm %>` — DB-sourced.
- Line 172: `<%=message %>` — **request param-sourced**, rendered unescaped into HTML.
- Line 207: `<%=Valert_id.get(i) %>` — DB-sourced, injected into onClick JS attribute string.
- Line 209: `<%=Valert_type.get(i) %>` — DB-sourced, rendered in table cell.
- Line 215: `<%=tmp %>` (machines) — DB-sourced.
- Line 243: `<%=tmp %>` (impact label) — computed from DB integer, safe.
- Line 249: `<%=tmp %>` (active status) — computed from DB string, safe.
- Line 251: `<%=Valert_id.get(i) %>` — DB-sourced, injected into onClick JS attribute string.
- Line 266: `<%=form_cd %>` — request param-sourced, hidden input.

**Form:** `method="post" action="../servlet/Frm_saveuser"` — handles alert deletion.

---

### 4. `C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst_admin.jsp`

**Imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ include file="../menu/menu.jsp" %>` (line 394)

**Scriptlet blocks:**
- Lines 286–370: Reads `user_cd`, `cust_cd`, `loc_cd`, `dept_cd`, `search_crit` from **request params** (not from session). Reads `access_level`, `access_cust`, `access_site`, `access_dept` from session. Sets all on filter bean. **No explicit role/admin check is present in the JSP itself** — access control relies entirely on what `Expire.jsp` and menu permissions enforce, plus the filter bean's internal logic.
- Lines 499–553: Loop rendering alert rows with same impact-label computation as `existing_alert_lst.jsp`.

**`<%= %>` expressions:**
- Line 7: `<%=LindeConfig.systemName %>` — config constant.
- Line 372: `<%=cust_cd %>`, `<%=loc_cd %>`, `<%=dept_cd %>`, `<%=user %>` — **request param-sourced**, injected into `onload` JS call.
- Line 415: `<%=form_nm %>` — DB-sourced.
- Lines 424, 425: `<%=vcust_cd.get(i) %>`, `<%=vcust_nm.get(i) %>` — DB-sourced.
- Lines 433, 434: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — DB-sourced.
- Lines 444, 445: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — DB-sourced.
- Lines 455, 456: `<%=Vuser_cd.get(i) %>`, `<%=Vuser_fnm.get(i) %>`, `<%=Vuser_lnm.get(i) %>` — DB-sourced.
- Line 466: `<%=message %>` — **request param-sourced**, rendered unescaped into HTML.
- Line 501: `<%=Valert_id.get(i) %>` — DB-sourced, in onClick JS string.
- Line 503: `<%=Valert_type.get(i) %>` — DB-sourced.
- Line 509: `<%=tmp %>` (machines) — DB-sourced.
- Line 536: `<%=tmp %>` (impact label) — computed from DB integer.
- Line 543: `<%=tmp %>` (active) — computed from DB string.
- Line 544: `<%=Valert_id.get(i) %>` — DB-sourced, in onClick JS string.
- Line 559: `<%=form_cd %>` — request param, hidden input.
- Line 560: `<%=access_level %>` — session-sourced, hidden input.

**Form:** `method="post" action="../servlet/Frm_saveuser"` — handles `del_alert_admin`.

---

### 5. `C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add.jsp`

**Imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 3)

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)

**Scriptlet blocks:**
- Lines 350–417: Reads `message`, `alert_id`, `alert_type`, `form_cd` from request params. Reads `user_cd` from **session** (`filter.setSet_ucd(ucd)` at line 381, `filter.setSet_my_alert("t")` at line 386). Alert context is tied to session user.
- Lines 431–433, 472–473, 483–485, 499–500, 521–529: Loop scriptlets rendering alert type options, customer/site/dept dropdowns, machine checkboxes.

**`<%= %>` expressions:**
- Line 8: `<%=LindeConfig.systemName %>` — config constant.
- Line 419: `onload` call — `<%=alert_type %>`, `<%=mach %>`, `<%=imp %>`, `<%=active %>`, `<%=alert_id %>`, `<%=alert_cust_cd %>`, `<%=alert_loc_cd %>`, `<%=alert_dept_cd %>` — all **DB-sourced** (retrieved for the session user's alert), but **injected unescaped into a JavaScript string context** in the onload attribute.
- Line 423: `<%=name %>` — DB-sourced user/customer name.
- Lines 432, 433: `<%=vid.get(i)%>`, `<%=valert.get(i) %>` — DB-sourced alert type options.
- Lines 473, 474: `<%=vcust_cd.get(i) %>`, `<%=vcust_nm.get(i) %>` — DB-sourced.
- Lines 484, 485: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — DB-sourced.
- Lines 500, 501: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — DB-sourced.
- Line 518: `<%=vgmtp.size()%>` — DB count.
- Lines 523, 524, 526, 527: `<%=vgmtp.get(i) %>`, `<%=vmachine.get(i) %>` — DB-sourced, rendered in checkbox values and labels.
- Line 533: `<%=message %>` — **request param-sourced**, rendered unescaped into HTML.
- Line 541: `<%=form_cd %>` — request param, in Close button onClick.
- Line 547: `<%=alert_id %>` — request param, hidden input.
- Line 548: `<%=user %>` — session-sourced, hidden input.
- Line 549: `<%=vgmtp.size() %>` — DB count, hidden input.
- Line 550: `<%=form_cd %>` — request param, hidden input.
- Line 551: `<%=access_level %>` — session-sourced, hidden input.

**Form:** `method="post" action="../servlet/Frm_saveuser"` with `op_code=add_alert`.

---

### 6. `C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add1.jsp`

**Imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Include directives:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)

**Scriptlet blocks:**
- Lines 362–434: Reads `message`, `alert_id`, `user_cd`, `alert_type`, `cust_cd`, `site_cd`, `dep_cd`, `form_cd` entirely from **request params** — in particular `user` (`user_cd`) comes from `request.getParameter("user_cd")` at line 370, not from session. Sets `filter.setSet_ucd(user)` at line 394. This is the admin form; the target user is controlled by the caller.
- Lines 449–451, 491–492, 503–504, 518–519, 553–561: Loop scriptlets for dropdowns and machine checkboxes.

**`<%= %>` expressions:**
- Line 7: `<%=LindeConfig.systemName %>` — config constant.
- Line 436: `onload` call — `<%=alert_type %>`, `<%=mach %>`, `<%=imp %>`, `<%=active %>`, `<%=alert_id %>`, `<%=alert_cust_cd %>`, `<%=alert_loc_cd %>`, `<%=alert_dept_cd %>`, `<%=cust_cd %>`, `<%=site_cd %>`, `<%=dep_cd%>` — DB-sourced and **request param-sourced** values, all **injected unescaped into JavaScript string context** in onload attribute.
- Line 440: `<%=name %>` — DB-sourced user name.
- Lines 450, 451: `<%=vid.get(i)%>`, `<%=valert.get(i) %>` — DB-sourced.
- Lines 492, 493: `<%=vcust_cd.get(i) %>`, `<%=vcust_nm.get(i) %>` — DB-sourced.
- Lines 503, 504: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — DB-sourced.
- Lines 518, 519: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — DB-sourced.
- Lines 540, 539: `<%=message %>` — **request param-sourced**, rendered unescaped.
- Line 546: `<%=form_cd %>`, `<%=cust_cd %>`, `<%=site_cd %>`, `<%=dep_cd %>`, `<%=user %>` — request param-sourced, in Close button onClick JS.
- Lines 555, 558: `<%=vgmtp.get(i) %>`, `<%=vmachine.get(i) %>` — DB-sourced, checkbox values and labels.
- Line 567: `<%=alert_id %>` — request param, hidden input.
- Line 568: `<%=user %>` — **request param-sourced**, hidden input (not from session).
- Lines 569, 570, 571, 572, 573: `<%=vgmtp.size() %>`, `<%=form_cd %>`, `<%=cust_cd%>`, `<%=site_cd%>`, `<%=dep_cd%>` — request param-sourced, hidden inputs.

**Form:** `method="post" action="../servlet/Frm_saveuser"` with `op_code=add_alert_admin`.

---

## STEP 4 — SECURITY REVIEW & FINDINGS

---

### A12v-1
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst.jsp`, line 172
`C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst_admin.jsp`, line 466
`C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add.jsp`, line 533
`C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add1.jsp`, line 540

**Severity:** High

**Category:** XSS — Reflected (request parameter rendered without escaping)

**Description:**
The `message` request parameter is read directly and output unescaped into HTML via `<%= message %>` in all four files. An attacker can craft a URL containing a `message` parameter with arbitrary HTML or JavaScript, which will be rendered in the browser. Because these are GET-style links and the pages are served after actions (e.g., error/success redirects), a victim can be sent a crafted URL that executes attacker JavaScript in their browser session. This is a classic reflected XSS.

**Evidence:**

`existing_alert_lst.jsp` line 102–104 and line 172:
```java
String message=request.getParameter("message")==null?"":request.getParameter("message");
...
&nbsp; <%=message %>
```

`existing_alert_lst_admin.jsp` line 293 and line 466:
```java
String message=request.getParameter("message")==null?"":request.getParameter("message");
...
&nbsp; <%=message %>
```

`frm_alert_add.jsp` line 356 and line 533:
```java
String message=request.getParameter("message")==null?"":request.getParameter("message");
...
&nbsp; <%=message %>
```

`frm_alert_add1.jsp` line 368 and line 540:
```java
String message=request.getParameter("message")==null?"":request.getParameter("message");
...
&nbsp; <%=message %>
```

**Recommendation:**
HTML-encode `message` before output. Replace all `<%=message %>` occurrences with `<%=org.apache.commons.lang.StringEscapeUtils.escapeHtml(message) %>` or an equivalent utility already present in the codebase (e.g., `Util` bean if it exposes an escaping method). Do not rely on the browser or downstream processing to neutralise injected markup.

---

### A12v-2
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_vehicle_lst.jsp`, line 349
`C:\Projects\cig-audit\repos\fleetfocus\master\existing_cust_vehicle_lst.jsp`, line 558

**Severity:** High

**Category:** XSS — Reflected into JavaScript context (onload attribute)

**Description:**
Request parameters `veh_typ_cd`, `loc_cd`, `cust_cd`, `dept_cd` are read from the URL, assigned to Java `String` variables without any sanitisation, and then written directly into the HTML `body onload` attribute JavaScript call. A value containing a single quote or closing parenthesis can break out of the JS string context and inject arbitrary script that executes on page load.

**Evidence:**

`existing_vehicle_lst.jsp` lines 298–300 and 349:
```java
String veh_typ_cd = request.getParameter("veh_typ_cd")==null?"all":request.getParameter("veh_typ_cd");
String loc_cd = request.getParameter("loc_cd")==null?"all":request.getParameter("loc_cd");
...
<body onload="set('<%=veh_typ_cd %>','<%=loc_cd %>')">
```

`existing_cust_vehicle_lst.jsp` lines 464, 472, 473 and 558:
```java
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
String loc_cd = request.getParameter("loc_cd")==null?"":request.getParameter("loc_cd");
String dept_cd = request.getParameter("dept_cd")==null?"":request.getParameter("dept_cd");
...
<body onload="set('<%=veh_typ_cd %>','<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>')">
```

Payload example: `loc_cd=');alert(document.cookie);//`

**Recommendation:**
JavaScript-encode all values before embedding in JS string literals. Use `StringEscapeUtils.escapeEcmaScript()` (Apache Commons Lang) or equivalent. For integer/code values, enforce numeric format server-side before rendering.

---

### A12v-3
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst_admin.jsp`, line 372
`C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add1.jsp`, line 436
`C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add.jsp`, line 419

**Severity:** High

**Category:** XSS — DB-sourced and request param-sourced values injected into JavaScript string context (onload attribute) without escaping

**Description:**
Multiple values — some DB-sourced (e.g., `alert_cust_cd`, `alert_loc_cd`, `mach`, `alert_type`) and some request param-sourced (`cust_cd`, `site_cd`, `dep_cd`, `user` in `frm_alert_add1.jsp`) — are injected unescaped into a multi-argument JavaScript `set(...)` call in the `body onload` attribute. A DB value containing a single quote (e.g., a machine GMTP ID or customer code with special characters) or a crafted request parameter can break out of the JS string context. In `frm_alert_add1.jsp`, `cust_cd`, `site_cd`, `dep_cd`, and `user` are entirely request param-controlled.

**Evidence:**

`frm_alert_add.jsp` line 419:
```jsp
<body onload="set('<%=alert_type %>','<%=mach %>','<%=imp %>','<%=active %>','<%=alert_id %>','<%=alert_cust_cd %>','<%=alert_loc_cd %>','<%=alert_dept_cd %>');do_switch();">
```

`frm_alert_add1.jsp` line 436:
```jsp
<body onload="set('<%=alert_type %>','<%=mach %>','<%=imp %>','<%=active %>','<%=alert_id %>','<%=alert_cust_cd %>','<%=alert_loc_cd %>','<%=alert_dept_cd %>','<%=cust_cd %>','<%=site_cd %>','<%=dep_cd%>');do_switch();">
```
Where `cust_cd`, `site_cd`, `dep_cd` are from `request.getParameter(...)` (lines 372–374).

`existing_alert_lst_admin.jsp` line 372:
```jsp
<body onload="set('<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>','<%=user %>')">
```
Where all four are from `request.getParameter(...)` (lines 295–297, 293).

**Recommendation:**
Apply `StringEscapeUtils.escapeEcmaScript()` to every value embedded in a JS string literal. Validate that ID/code parameters match an expected pattern (alphanumeric, fixed length) before use.

---

### A12v-4
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_vehicle_lst.jsp`, lines 492, 494, 498
`C:\Projects\cig-audit\repos\fleetfocus\master\existing_cust_vehicle_lst.jsp`, lines 714, 727, 731

**Severity:** Medium

**Category:** XSS — DB-sourced vehicle identifiers injected into JavaScript onClick handler strings without escaping

**Description:**
Vehicle code (`Vveh_cd.get(i)`), GMTP ID (`Vgmtp_id.get(i)`), and hire/fleet number are rendered directly into `onClick` JavaScript handler string arguments without HTML/JS escaping. If any of these DB values contains a single quote, backslash, or HTML metacharacter (possible if upstream data entry is uncontrolled or another injection path populates the vehicle table), it would break the JS string and could lead to script execution. This is a stored XSS vector.

**Evidence:**

`existing_vehicle_lst.jsp` lines 492, 498:
```jsp
<a href="#" onClick="open_edit('<%=Vveh_cd.get(i) %>','<%=Vgmtp_id.get(i) %>');"><%=Vgmtp_id.get(i) %></a>
...
<input type="button" name="b1" value="Set CANBus rules" onclick="open_canb('<%=Vveh_cd.get(i) %>','<%=Vgmtp_id.get(i) %>');"/>
```

`existing_cust_vehicle_lst.jsp` lines 714, 727, 731:
```jsp
<a href="#" onClick="open_edit('<%=Vveh_cd.get(i) %>','<%=tmp %>','<%=Vis_unit.get(i) %>');"><%=tmp %></a>
...
<input type="button" name="cm" value="Change Module" onClick="open_repl('<%=Vveh_cd.get(i) %>','<%=Vgmtp_id.get(i) %>');">
<input type="button" name="b1" value="Set CANBus rules" onclick="open_canb('<%=Vveh_cd.get(i) %>','<%=Vgmtp_id.get(i) %>');"/>
```

**Recommendation:**
JS-encode all values placed inside JS string literals in event handler attributes. HTML-encode values used as visible text content. Apply `StringEscapeUtils.escapeEcmaScript()` for the JS context and `escapeHtml()` for the HTML context.

---

### A12v-5
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_cust_vehicle_lst.jsp`, lines 471, 501, 503

**Severity:** High

**Category:** IDOR — Customer vehicle list scoped by user-controlled `cust_cd` parameter, not enforced against session identity for non-admin users

**Description:**
The page reads `cust_cd` from the request parameter (line 471) and passes it directly to the filter bean (`filter.setSet_cust_cd(cust_cd)`). While the filter bean also receives `access_level`, `access_cust`, `access_site`, and `access_dept` from session, the page's JSP layer makes no explicit check that the requested `cust_cd` matches or is a child of `session.getAttribute("access_cust")`. A user with a valid session for Customer A could potentially pass `cust_cd=B` in the URL and receive Customer B's vehicle list if the filter bean's internal logic does not enforce the boundary for all access level combinations. The risk is compounded because the same `cust_cd` is used to drive AJAX sub-queries (`get_site.jsp`, `get_dept.jsp`, `get_vehicle_dept.jsp`) via the `cust` form field, which is also rendered from the (already-accepted) request value. There is no visible server-side assertion in the JSP that `cust_cd` is within the authenticated tenant's scope.

**Evidence:**
```java
// Line 471
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
...
// Lines 480-483 — session-sourced access variables
String access_cust=(String)session.getAttribute("access_cust");
...
// Line 501 — cust_cd from request goes directly to bean, no explicit comparison
filter.setSet_cust_cd(cust_cd);
```

No code in the JSP checks `cust_cd.equals(access_cust)` or similar before use.

**Recommendation:**
In the JSP (or in the filter bean, confirmed by code review of `Databean_getuser`), enforce that the requested `cust_cd` is equal to or a permitted child of `session.getAttribute("access_cust")` before executing the query. For users with `access_level >= 3` (site-level or below), the customer scope must be fixed to the session value and the `cust_cd` parameter must be ignored or validated.

---

### A12v-6
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst_admin.jsp`, lines 291–329

**Severity:** High

**Category:** Broken Access Control — Admin alert management page lacks explicit role/privilege check in JSP

**Description:**
`existing_alert_lst_admin.jsp` is the administrative view of all users' alerts (op_code `alert_list_admin`), allows viewing, adding, editing, and deleting alerts belonging to arbitrary users selected via the `user_cd` URL parameter. The JSP scriptlet reads `access_level` and related attributes from session (lines 300–309), but performs **no conditional block** that would halt rendering or redirect a non-admin user. There is no `if(al > someAdminThreshold) { response.sendRedirect(...); }` guard. The page relies entirely on the `Expire.jsp` include (which only enforces session existence) and on the filter bean's internal scoping, which may still return data at lower access levels. An authenticated non-admin user who navigates directly to this URL receives the admin UI without any JSP-level rejection.

**Evidence:**
```java
// Lines 300-309: access level read from session
String access_level = (String)session.getAttribute("access_level");
...
int al = Integer.parseInt(access_level);

filter.setAccess_level(access_level);
filter.setAccess_cust(access_cust);
// ...
filter.init();
// No: if(al > 2) { response.sendRedirect("..."); return; }
```

The page then renders customer/site/user selection dropdowns and an "Add New Alert" button with no visible JSP-level block for low-privilege users.

**Recommendation:**
Add an explicit access level guard at the top of the scriptlet block. For example:
```java
if(al > 2) { // or whatever threshold constitutes "admin"
    response.sendRedirect("../error/access_denied.jsp");
    return;
}
```
This should be a defence-in-depth measure in addition to menu/permission controls, not in lieu of them.

---

### A12v-7
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add1.jsp`, lines 370, 394, 568

**Severity:** High

**Category:** IDOR / Privilege Escalation — Target user for alert creation/editing is fully request-controlled, not session-validated

**Description:**
In `frm_alert_add1.jsp` (the admin alert form), the `user` variable — representing the user whose alert is being created or edited — is taken from `request.getParameter("user_cd")` (line 370), not from the session. This value is then passed to `filter.setSet_ucd(user)` (line 394) and emitted into the form as `<input type="hidden" name="user" value="<%=user %>">` (line 568). This means:
1. Any authenticated user who can reach this page can specify an arbitrary `user_cd` parameter and create/edit alerts on behalf of that user.
2. The save action (`Frm_saveuser` servlet with `op_code=add_alert_admin`) receives the user value from the hidden field — which was sourced from an earlier request param — and may associate the alert with the attacker-specified user.
3. This is a cross-tenant data manipulation vector if users from different customers can be targeted.

**Evidence:**
```java
// Line 370
String user = request.getParameter("user_cd")==null?"":request.getParameter("user_cd");
...
// Line 394
filter.setSet_ucd(user);
...
// Line 568
<input type="hidden" name="user" value="<%=user %>">
```

Compare with `frm_alert_add.jsp` line 358–381 where `user` is correctly sourced from session:
```java
String user = (String)session.getAttribute("user_cd");
```

**Recommendation:**
If `frm_alert_add1.jsp` is legitimately an admin-only form, enforce an admin-level check before accepting `user_cd` from the request. The `user_cd` of the target should be validated against the admin's permitted customer scope (i.e., target user must belong to a customer the admin manages). If editing one's own alert, the user code must be forced from session. Never trust a user code supplied in a request parameter without server-side authorisation validation.

---

### A12v-8
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst.jsp`, line 164
`C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst_admin.jsp`, line 412
`C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add.jsp`, line 420
`C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add1.jsp`, line 437

**Severity:** Medium

**Category:** CSRF — State-changing forms (alert add, edit, delete) have no CSRF token

**Description:**
All alert mutation forms POST to `../servlet/Frm_saveuser` with `op_code` values `add_alert`, `del_alert`, `add_alert_admin`, `del_alert_admin`. None of the forms contain a CSRF synchroniser token, a double-submit cookie, or any other CSRF mitigation. An attacker can host a page that auto-submits a POST to these endpoints from a victim's authenticated browser session, silently adding, editing, or deleting that user's alert subscriptions. The delete action in particular is triggered by a radio button `onClick` that directly submits the form, making it even simpler to trigger via a crafted page.

**Evidence:**

`existing_alert_lst.jsp` line 164:
```html
<form method="post" action="../servlet/Frm_saveuser">
```
No `<input type="hidden" name="csrf_token" ...>` or equivalent anywhere in the form.

`frm_alert_add.jsp` line 420:
```html
<form method="post" action="../servlet/Frm_saveuser">
```

Delete trigger (`existing_alert_lst.jsp` lines 251, 83–85):
```java
// onClick on radio button calls submit_del which does:
document.forms[0].id.value=id;
document.forms[0].submit();
```
No token verification before submit.

**Recommendation:**
Generate a per-session (or per-request) CSRF token, store it in the HTTP session, include it as a hidden field in all state-changing forms, and validate the submitted token server-side in `Frm_saveuser` before processing any `op_code` that mutates data. Standard implementations include the Synchronizer Token Pattern or using a framework-provided CSRF filter.

---

### A12v-9
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_cust_vehicle_lst.jsp`, line 739
`C:\Projects\cig-audit\repos\fleetfocus\master\frm_alert_add.jsp`, line 551
`C:\Projects\cig-audit\repos\fleetfocus\master\existing_alert_lst_admin.jsp`, line 560

**Severity:** Low

**Category:** Information Exposure — Access level exposed in client-side hidden form field

**Description:**
The session-sourced `access_level` value is written into a hidden HTML form input (`<input type="hidden" name="alevel" value="<%=access_level %>"/>`). While it originates from the session (not from a request parameter), exposing access level integers in the HTML provides an attacker with reconnaissance data about the privilege model and, depending on how the downstream servlet handles this field, could allow privilege escalation if the servlet trusts the submitted `alevel` value rather than re-reading it from session.

**Evidence:**

`existing_cust_vehicle_lst.jsp` line 739:
```html
<input type="hidden" name="alevel" value="<%=access_level %>"/>
```

`existing_alert_lst_admin.jsp` line 560:
```html
<input type="hidden" name="alevel" value="<%=access_level %>"/>
```

`frm_alert_add.jsp` line 551:
```html
<input type="hidden" name="alevel" value="<%=access_level %>"/>
```

**Recommendation:**
Remove the `alevel` hidden field from the HTML. The `Frm_saveuser` servlet should read `access_level` directly from the server-side session, never from a submitted form field. If the JavaScript client-side logic needs it for display purposes (e.g., showing/hiding "All" options in dropdowns), retain the value in the HTML but ensure the server ignores the submitted form value.

---

### A12v-10
**File:** `C:\Projects\cig-audit\repos\fleetfocus\master\existing_vehicle_lst.jsp`, line 436
`C:\Projects\cig-audit\repos\fleetfocus\master\existing_cust_vehicle_lst.jsp`, line 652

**Severity:** Medium

**Category:** XSS — `search_crit` request parameter rendered unescaped into HTML input value attribute

**Description:**
The `search_crit` parameter is read from the request and rendered directly into the `value` attribute of a text input (`<input type="text" name="sc" value="<%=search_crit %>">`). HTML attribute injection is possible: a value containing `"` can close the attribute and inject new HTML attributes or break the tag structure. In addition, `search_crit` is also rendered in a table heading cell (`<%=search_crit %>`) without escaping. An attacker can inject arbitrary HTML/JS by crafting the `search_crit` URL parameter.

**Evidence:**

`existing_vehicle_lst.jsp` lines 302, 436, 446:
```java
String search_crit = request.getParameter("search_crit")==null?"":request.getParameter("search_crit");
...
<input type="text" name="sc" value="<%=search_crit %>">
...
starting with '<%=search_crit %>'
```

`existing_cust_vehicle_lst.jsp` lines 467, 652, 674:
```java
String search_crit = request.getParameter("search_crit")==null?"":request.getParameter("search_crit");
...
<input type="text" name="sc" value="<%=search_crit %>">
...
starting with '<%=search_crit %>'
```

**Recommendation:**
HTML-encode `search_crit` before rendering in both the input value attribute and the inline text context. Use `escapeHtml(search_crit)` consistently. Additionally, limit the permitted character set for search criteria server-side.

---

## Summary Table

| ID      | File(s)                                                   | Severity | Category                          |
|---------|-----------------------------------------------------------|----------|-----------------------------------|
| A12v-1  | existing_alert_lst.jsp:172, existing_alert_lst_admin.jsp:466, frm_alert_add.jsp:533, frm_alert_add1.jsp:540 | High | XSS — Reflected `message` param |
| A12v-2  | existing_vehicle_lst.jsp:349, existing_cust_vehicle_lst.jsp:558 | High | XSS — Reflected params into JS onload |
| A12v-3  | existing_alert_lst_admin.jsp:372, frm_alert_add1.jsp:436, frm_alert_add.jsp:419 | High | XSS — DB/param values into JS onload |
| A12v-4  | existing_vehicle_lst.jsp:492,498, existing_cust_vehicle_lst.jsp:714,727,731 | Medium | XSS — DB vehicle IDs into JS onClick |
| A12v-5  | existing_cust_vehicle_lst.jsp:471,501                     | High     | IDOR — cust_cd param, no tenant enforcement in JSP |
| A12v-6  | existing_alert_lst_admin.jsp:291–329                      | High     | Broken Access Control — no admin guard in JSP |
| A12v-7  | frm_alert_add1.jsp:370,394,568                            | High     | IDOR / Privilege Escalation — user_cd from request |
| A12v-8  | existing_alert_lst.jsp:164, existing_alert_lst_admin.jsp:412, frm_alert_add.jsp:420, frm_alert_add1.jsp:437 | Medium | CSRF — no token on mutation forms |
| A12v-9  | existing_cust_vehicle_lst.jsp:739, frm_alert_add.jsp:551, existing_alert_lst_admin.jsp:560 | Low | Info Exposure — access_level in hidden field |
| A12v-10 | existing_vehicle_lst.jsp:436,446, existing_cust_vehicle_lst.jsp:652,674 | Medium | XSS — search_crit param unescaped in input and heading |

**Total findings: 10**
