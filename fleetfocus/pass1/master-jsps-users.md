# Security Audit Report — master JSPs (Users / Drivers / Customers)
**Audit ID:** A12-user
**Run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Auditor:** Agent A12-user
**Date:** 2026-02-25

---

## Step 3 — Reading Evidence

### 1. `master/existing_user_lst.jsp`

**Page imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1) — session/expiry include
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Scriptlet blocks:**
- Lines 344–434: Main scriptlet. Reads request parameters (`cust_cd`, `loc_cd`, `dept_cd`, `search_crit`, `active`, `form_cd`, `message`). Reads session attributes (`access_level`, `access_cust`, `access_site`, `access_dept`, `user_cd`). Populates ArrayLists: `Vuser_cd`, `Vuser_id`, `Vuser_fnm`, `Vuser_lnm`, `Vuser_phno`, `Vuser_mno`, `Vuser_status`, `Vuser_al` (access level), `Vuser_acc_cust`, `Vuser_wiegand` (card/Wiegand ID).
- Lines 576–616: Rendering loop — iterates over user result set and emits table rows.

**`<%= %>` expressions (DB-sourced / user-controlled):**
| Line | Expression | Source | Escaped? |
|------|-----------|--------|----------|
| 7 | `<%=LindeConfig.systemName %>` | Config constant | N/A (constant) |
| 435 | `<%=access_cust%>` | Session attribute | No — rendered raw outside any tag |
| 436 | `set('<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>','<%=usr_status%>')` | Request params | No — interpolated into JS `onload` attribute |
| 480 | `<%=form_nm %>` | DB-sourced | No |
| 489 | `<%=vcust_cd.get(i) %>` / `<%=vcust_nm.get(i) %>` | DB-sourced | No |
| 498–499 | `<%=Vloc_cd.get(i) %>` / `<%=Vloc_nm.get(i) %>` | DB-sourced | No |
| 509 | `<%=vdept_cd.get(i) %>` / `<%=vdept_nm.get(i) %>` | DB-sourced | No |
| 528 | `<%=search_crit %>` (in input value=) | Request param | No |
| 540 | `<%=message %>` | Request param | No |
| 544–545 | `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>`, `<%=search_crit %>` | DB/request | No |
| 579 | `open_edit('<%=Vuser_cd.get(i) %>','<%=Vuser_id.get(i) %>')` | DB-sourced | No — interpolated into JS onclick |
| 579 | `<%=Vuser_id.get(i) %>` (link text) | DB-sourced | No |
| 581 | `<%=Vuser_id.get(i) %>` | DB-sourced | No |
| 583 | `<%=Vuser_fnm.get(i) %>` | DB-sourced | No |
| 585 | `<%=Vuser_lnm.get(i) %>` | DB-sourced | No |
| 587 | `<%=Vuser_al.get(i) %>` | DB-sourced | No — access level number exposed |
| 590 | `<%=Vuser_acc_cust.get(i) %>` | DB-sourced | No |
| 596 | `<%=tmp %>` (mobile number) | DB-sourced | No |
| 599 | `<%=Vuser_wiegand.get(i) %>` | DB-sourced | No |
| 604 | `<%=tmp %>` (status) | DB-sourced | No |
| 609,611 | `fndelete('<%=Vuser_cd.get(i)%>','<%=Vuser_id.get(i) %>')` | DB-sourced | No — in JS onclick |
| 619 | `<%=form_cd %>` (hidden input value) | Request param | No |
| 622–626 | Hidden input values: `cust_cd`, `loc_cd`, `dept_cd`, `usr_status`, `access_level` | Request param / session | No |

**Include directives:**
- `../sess/Expire.jsp` (line 1)
- `../menu/menu.jsp` (line 458)

---

### 2. `master/existing_driver_lst.jsp`

**Page imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Scriptlet blocks:**
- Lines 362–451: Main scriptlet. Reads request params (`cust_cd`, `loc_cd`, `dept_cd`, `search_crit`, `active`, `form_cd`, `message`). Reads session (`access_level`, `access_cust`, `access_site`, `access_dept`, `user_cd`). Populates `Vuser_cd`, `Vuser_id`, `Vuser_fnm`, `Vuser_lnm`, `Vuser_phno`, `Vuser_mno`, `Vuser_status`, `Vcard_prefix`, `Vcard_id` (PIN/card), `Vuser_wiegand` (driver_id).
- Lines 591–642: Rendering loop over drivers.

**`<%= %>` expressions (DB-sourced / user-controlled):**
| Line | Expression | Source | Escaped? |
|------|-----------|--------|----------|
| 452 | `set('<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>','<%=usr_status%>')` | Request params | No — in JS onload |
| 496 | `<%=form_nm %>` | DB-sourced | No |
| 505 | `<%=vcust_cd.get(i) %>` / `<%=vcust_nm.get(i) %>` | DB-sourced | No |
| 514 | `<%=Vloc_cd.get(i) %>` / `<%=Vloc_nm.get(i) %>` | DB-sourced | No |
| 525 | `<%=vdept_cd.get(i) %>` / `<%=vdept_nm.get(i) %>` | DB-sourced | No |
| 545 | `<%=search_crit %>` (input value) | Request param | No |
| 555 | `<%=message %>` | Request param | No |
| 559–560 | `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>`, `<%=search_crit %>` | DB/request | No |
| 599 | `<%=Vuser_id.get(i) %>` | DB-sourced | No |
| 601 | `<%=Vuser_fnm.get(i) %>` | DB-sourced | No |
| 603 | `<%=Vuser_lnm.get(i) %>` | DB-sourced | No |
| 607,611 | `<%=tmp %>` (card prefix, card/PIN) | DB-sourced | No — card/PIN data |
| 615 | `<%=tmp %>` (mobile) | DB-sourced | No |
| 618 | `<%=Vuser_wiegand.get(i) %>` (Wiegand/driver ID) | DB-sourced | No |
| 627 | `open_edit1('<%=Vuser_cd.get(i) %>','<%=Vuser_id.get(i) %>')` | DB-sourced | No — in JS onclick |
| 635,637 | `fndelete/fnrecover('<%=Vuser_cd.get(i)%>','<%=Vuser_id.get(i) %>')` | DB-sourced | No — in JS onclick |
| 645–652 | Hidden inputs: `form_cd`, `cust_cd`, `loc_cd`, `dept_cd`, `usr_status`, `access_level` | Request/session | No |

**Include directives:**
- `../sess/Expire.jsp` (line 1)
- `../menu/menu.jsp` (line 474)

---

### 3. `master/existing_customer_lst.jsp`

**Page imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Scriptlet blocks:**
- Lines 263–340: Main scriptlet. Reads request params (`gp_cd`, `loc_cd`, `st_dt`, `end_dt`, `sc` (search), `message`, `form_cd`). Reads session (`access_level`, `access_cust`, `access_site`, `access_dept`). Populates `Vuser_cd`, `Vuser_id` (company name), `Vuser_email`, `Vuser_gmtp` (account prefix), `Vuser_phno`, `Vuser_status`.
- Lines 465–490: Rendering loop over customers.

**`<%= %>` expressions:**
| Line | Expression | Source | Escaped? |
|------|-----------|--------|----------|
| 342 | `set('<%=gp_cd %>','<%=loc_cd %>')` | Request params | No — in JS onload |
| 386 | `asd<%=form_nm %>` | DB-sourced | No |
| 414,420 | `<%=st_dt %>`, `<%=end_dt %>` (hidden input values) | Request param | No |
| 431 | `<%=search_crit %>` (input value) | Request param | No |
| 439 | `<%=get_gp %>`, `<%=search_crit %>` | DB/request | No |
| 469 | `open_edit('<%=Vuser_cd.get(i) %>','<%=Vuser_id.get(i) %>')` | DB-sourced | No — in JS onclick |
| 469 | `<%=Vuser_gmtp.get(i) %>` (account prefix link text) | DB-sourced | No |
| 471 | `<%=Vuser_id.get(i) %>` (company name) | DB-sourced | No |
| 475 | `<%=tmp %>` (phone) | DB-sourced | No |
| 479 | `<%=tmp %>` (email) | DB-sourced | No |
| 483 | `<%=tmp %>` (status) | DB-sourced | No |
| 486 | `goto_site('<%=Vuser_cd.get(i) %>')` | DB-sourced | No — in JS onclick |
| 492 | `<%=form_cd %>` (hidden input) | Request param | No |

**Include directives:**
- `../sess/Expire.jsp` (line 1)
- `../menu/menu.jsp` (line 364)

---

### 4. `master/frm_access_customer.jsp`

**Page imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Scriptlet blocks:**
- Lines 129–180: Main scriptlet. Reads request params (`message`, `user_cd`, `form_cd`). Reads session (`access_level`, `access_cust`, `access_site`, `access_dept`). Populates `vuser_cd`, `vuser_fnm`, `vuser_lnm`, `vcust_cd`, `vcust_nm`, `vcust_rel_usr`. Note: `user_cd` is taken from **request parameter** and passed directly to `filter.setSet_user_cd(user_cd)` to control whose customer access is displayed.

**`<%= %>` expressions:**
| Line | Expression | Source | Escaped? |
|------|-----------|--------|----------|
| 182 | `set('<%=user_cd%>')` | Request param | No — in JS onload |
| 225 | `<%=form_nm %>` | DB-sourced | No |
| 235 | `<%=vuser_cd.get(i) %>` / `<%=vuser_fnm.get(i) %>` / `<%=vuser_lnm.get(i) %>` | DB-sourced | No — in option value/text |
| 253 | `<%=vcust_nm.get(i)%>` | DB-sourced | No |
| 255 | `DataUtil.checkedValueCheckbox(vcust_cd.get(i).toString(),vcust_rel_usr)` | DB-sourced | No — utility call |
| 256 | `<%=vcust_cd.get(i)%>` (hidden cust_id) | DB-sourced | No |
| 268 | `<%=message %>` | Request param | No |
| 274 | `<%=vcust_cd.size()%>` (count hidden) | DB-sourced | No |
| 275 | `<%=form_cd %>` (hidden) | Request param | No |

**Include directives:**
- `../sess/Expire.jsp` (line 1)
- `../menu/menu.jsp` (line 204)

---

### 5. `master/frm_blacklist_driv.jsp`

**Page imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Scriptlet blocks:**
- Lines 587–673: Main scriptlet. Reads request params (`cust_cd`, `loc_cd`, `dept_cd`, `search_crit`, `form_cd`, `message`). Reads session. Populates driver list (`Vuser_cd`, `Vuser_fnm`, `Vuser_lnm`), vehicle types (`vt_cds`, `vt_nms`), vehicles (`veh_cd`, `veh_nm`), dept (`vdept_cd`, `vdept_nm`).
- Lines 793–943: Rendering loop for driver checkboxes, dept checkboxes, vehicle type checkboxes, vehicle checkboxes.

**`<%= %>` expressions:**
| Line | Expression | Source | Escaped? |
|------|-----------|--------|----------|
| 674 | `set('<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>')` | Request params | No — in JS onload |
| 718 | `<%=form_nm %>` | DB-sourced | No |
| 727 | `<%=vcust_cd.get(i) %>` / `<%=vcust_nm.get(i) %>` | DB-sourced | No |
| 737 | `<%=Vloc_cd.get(i) %>` / `<%=Vloc_nm.get(i) %>` | DB-sourced | No |
| 748,751 | `<%=vdept_cd.get(i) %>` / `<%=vdept_nm.get(i) %>` | DB-sourced | No |
| 760 | `<%=search_crit %>` (input value) | Request param | No |
| 768 | `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>`, `<%=search_crit %>` | DB/request | No |
| 776 | `<%=message %>` | Request param | No — in `<tr>` directly |
| 786–788 | `sel_all_driver('<%=Vuser_cd.size()%>')` etc. | DB-derived count | No |
| 795–817 | `<%=Vuser_cd.get(i) %>`, `<%=Vuser_fnm.get(i) %>`, `<%=Vuser_lnm.get(i) %>` | DB-sourced | No |
| 838–860 | `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` | DB-sourced | No |
| 871–893 | `<%=vt_cds.get(i) %>`, `<%=vt_nms.get(i) %>` | DB-sourced | No |
| 907–929 | `<%=veh_cd.get(i) %>`, `<%=veh_nm.get(i) %>` | DB-sourced | No |
| 945–954 | Hidden inputs: form_cd, loc_cd, cust_cd, dept_cd, sizes, alevel | Request/session | No |

**Include directives:**
- `../sess/Expire.jsp` (line 1)
- `../menu/menu.jsp` (line 696)

---

### 6. `master/existing_opchk_lst.jsp`

**Page imports:**
- `<%@ include file="../sess/Expire.jsp" %>` (line 1)
- `<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>` (line 2)

**Scriptlet blocks:**
- Lines 328–415: Main scriptlet. Reads request params (`cust_cd`, `loc_cd`, `dept_cd`, `veh_typ_cd`, `message`, `form_cd`). Reads session. Populates operational check question lists: `vchk_cd`, `vord_no`, `vquest` (question text), `vans_typ`, `vexp_ans`, `vcri_ans`.
- Lines 550–628: Rendering loop for questions table.

**`<%= %>` expressions:**
| Line | Expression | Source | Escaped? |
|------|-----------|--------|----------|
| 417 | `set('<%=veh_typ_cd %>','<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>')` | Request params | No — in JS onload |
| 461 | `<%=form_nm %>` | DB-sourced | No |
| 470 | `<%=vcust_cd.get(i) %>` / `<%=vcust_nm.get(i) %>` | DB-sourced | No |
| 479 | `<%=Vloc_cd.get(i) %>` / `<%=Vloc_nm.get(i) %>` | DB-sourced | No |
| 490 | `<%=vdept_cd.get(i) %>` / `<%=vdept_nm.get(i) %>` | DB-sourced | No |
| 504 | `<%=Vveh_typ_cd.get(i) %>` / `<%=Vveh_typ_nm.get(i) %>` | DB-sourced | No |
| 526–527 | `<%=get_cust %>`, `<%=get_loc %>`, `<%=get_dep %>`, `<%=get_gp %>` | DB-sourced | No |
| 557–562 | `reorder('<%=vchk_cd.get(i) %>','<%=vchk_cd.get(i-1) %>')` etc. | DB-sourced | No — in JS onclick |
| 574 | `open_edit('<%=vchk_cd.get(i) %>','<%=i+1 %>')` | DB-sourced | No — in JS onclick |
| 578 | `<%=vquest.get(i) %>` | DB-sourced (question text) | No |
| 590,593,607 | `<%=tmp %>` (answer type, expected answer, critical) | DB-sourced | No |
| 607 | `<font color="<%=col %>">` | Derived from DB value | No |
| 611 | `call_delete('<%=vchk_cd.get(i)%>')` | DB-sourced | No — in JS onclick |
| 621 | `open_upload('<%=get_cust %>')` | DB-sourced customer name | No — in JS onclick |
| 631 | `<%=message %>` | Request param | No |
| 640–644 | Hidden inputs: cust_cd, loc_cd, dept_cd, form_cd, alevel | Request/session | No |

**Include directives:**
- `../sess/Expire.jsp` (line 1)
- `../menu/menu.jsp` (line 439)

---

## Step 4 — Security Findings

---

### A12u-1
**File:** `master/existing_user_lst.jsp`
**Line(s):** 436, 579, 609, 611
**Severity:** CRITICAL
**Category:** XSS — Stored/Reflected via JavaScript Context
**Description:**
DB-sourced and request-parameter values are interpolated directly into JavaScript event handler strings and `onload` attributes without any HTML or JavaScript escaping. An attacker who controls a user's first name, last name, or user ID (e.g., by registering/editing a user record) can inject arbitrary JavaScript. The `onload` attribute on line 436 interpolates four request parameters directly into a JS function call, making reflected XSS trivial.

**Evidence:**
```jsp
// Line 436
<body onload="set('<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>','<%=usr_status%>')">

// Line 579 — DB-sourced user ID in JS onclick
<a href="#" onClick="open_edit('<%=Vuser_cd.get(i) %>','<%=Vuser_id.get(i) %>');">

// Lines 609, 611 — DB-sourced user ID in JS onclick
<input type="button" value="Delete" onclick="fndelete('<%=Vuser_cd.get(i)%>','<%=Vuser_id.get(i) %>')">
<input type="button" value="Recover" onclick="fnrecover('<%=Vuser_cd.get(i)%>','<%=Vuser_id.get(i) %>')">
```

**Recommendation:**
All values interpolated into JavaScript contexts must be JavaScript-escaped (e.g., using `org.apache.commons.text.StringEscapeUtils.escapeEcmaScript()` or a comparable utility). Values interpolated into HTML attribute/element contexts must be HTML-escaped (e.g., `ESAPI.encoder().encodeForHTML()`). Request parameters used in `onload` must also be HTML-attribute-escaped.

---

### A12u-2
**File:** `master/existing_user_lst.jsp`
**Line(s):** 540, 544–545
**Severity:** HIGH
**Category:** XSS — Reflected in HTML Output
**Description:**
The `message` request parameter (line 540) and the `search_crit` request parameter (line 545) are output raw into HTML. `message` is rendered in a prominent red banner. An attacker who can craft a link with a malicious `message` or `search_crit` parameter can execute arbitrary JavaScript in the victim's browser session.

**Evidence:**
```jsp
// Line 540
<p style="color: red;font-weight:bold;font-size:16px" align="center"><%=message %></p>

// Lines 544–545
<td align=center> Data for the Customer: <%=get_cust %> for Site: <%=get_loc %>
 for the Department: <%=get_dep %> for names starting with '<%=search_crit %>'
```

**Recommendation:**
HTML-encode all request parameters before rendering into HTML. Use `ESAPI.encoder().encodeForHTML(message)` or equivalent. This applies to every `<%= %>` expression emitted into HTML content.

---

### A12u-3
**File:** `master/existing_user_lst.jsp`
**Line(s):** 435, 583, 585, 587, 590, 596, 599
**Severity:** HIGH
**Category:** Data Exposure — Sensitive User Fields Rendered Without Escaping
**Description:**
The user list exposes: user access level (`Vuser_al` — line 587), the list of customers a user can access (`Vuser_acc_cust` — line 590), mobile phone numbers (`Vuser_mno` — line 596), and Wiegand card IDs (physical access credentials — line 599). Additionally, on line 435, `access_cust` (a session attribute representing the current user's customer scope) is rendered raw outside any HTML element, leaking it into the page source body unconditionally.

**Evidence:**
```jsp
// Line 435 — leaks session attribute to page body
<%=access_cust%>

// Line 587 — access level number visible in table
<td> <%=Vuser_al.get(i) %></td>

// Line 590 — customer access rights listed per user
<td> <%=Vuser_acc_cust.get(i) %>asd</td>

// Line 599 — physical Wiegand card credential
<%=Vuser_wiegand.get(i) %>
```

**Recommendation:**
Remove the bare `<%=access_cust%>` rendering on line 435 (it appears to be a debug artefact — note also the trailing "asd" on line 590 which confirms debug/test code was left in production). Review whether access level numbers and Wiegand card IDs need to be visible in the UI to all users with access to this page. Wiegand IDs in particular are physical security credentials that enable card cloning; restrict their display. Apply HTML encoding to all remaining outputs.

---

### A12u-4
**File:** `master/existing_user_lst.jsp`
**Line(s):** 476 (form action `../servlet/Frm_saveuser`), state-changing via `fndelete` / `fnrecover`
**Severity:** HIGH
**Category:** CSRF — No Token on State-Changing Form
**Description:**
The form at line 476 posts to `../servlet/Frm_saveuser` with `op_code=user_delete` or `op_code=user_active` to delete or recover user accounts. There is no CSRF token in the form. An attacker who tricks an authenticated administrator into loading a crafted page can silently delete or recover arbitrary user accounts by forging a POST request.

**Evidence:**
```jsp
// Line 476
<form method="post" action="../servlet/Frm_saveuser">

// Lines 620–621 — state-changing hidden fields with no CSRF token
<input type="hidden" name="op_code" value="user_delete"></input>
<input type="hidden" name="action_uid" value=""></input>
```

**Recommendation:**
Implement the Synchronizer Token Pattern: generate a per-session (or per-request) CSRF token, store it in the session, include it as a hidden field in every state-changing form, and validate it in `Frm_saveuser` before processing any operation.

---

### A12u-5
**File:** `master/existing_driver_lst.jsp`
**Line(s):** 599, 601, 603, 607, 611, 615, 618, 627, 635, 637
**Severity:** CRITICAL
**Category:** XSS — Stored via JavaScript Context + HTML Output
**Description:**
Same class of vulnerability as A12u-1 but in the driver list. Driver first name, last name, user ID, card prefix, card/PIN value, mobile number, and Wiegand driver ID are all interpolated into HTML and JavaScript onclick handlers without escaping. The card/PIN field (`Vcard_id`, line 611) and Wiegand ID (`Vuser_wiegand`, line 618) are particularly sensitive — an attacker who stores a payload in a driver name or card field gains stored XSS. The `onload` on line 452 uses four request params.

**Evidence:**
```jsp
// Line 452
<body onload="set('<%=cust_cd %>','<%=loc_cd %>','<%=dept_cd %>','<%=usr_status%>')">

// Line 627 — DB-sourced driver ID in JS onclick
<input type="radio" onclick="open_edit1('<%=Vuser_cd.get(i) %>','<%=Vuser_id.get(i) %>');" .../>

// Line 611 — card/PIN value unescaped in table cell
<td> <%=tmp %></td>   // tmp = Vcard_id.get(i)

// Line 618 — Wiegand/driver ID
<%=Vuser_wiegand.get(i) %>
```

**Recommendation:**
Apply JavaScript escaping for all values in JS event handlers. Apply HTML encoding for all values in HTML element content. Remove or restrict display of card/PIN and Wiegand values (see also A12u-7).

---

### A12u-6
**File:** `master/existing_driver_lst.jsp`
**Line(s):** 492 (form action), 646–647
**Severity:** HIGH
**Category:** CSRF — No Token on State-Changing Form
**Description:**
Identical to A12u-4. The driver form posts to `../servlet/Frm_saveuser` with no CSRF token. Delete and recover operations (`driver_delete`, `driver_active`) can be forged.

**Evidence:**
```jsp
<form method="post" action="../servlet/Frm_saveuser">
<input type="hidden" name="op_code" value="user_delete"></input>
<input type="hidden" name="action_uid" value=""></input>
```

**Recommendation:**
Same as A12u-4: implement the Synchronizer Token Pattern.

---

### A12u-7
**File:** `master/existing_driver_lst.jsp`
**Line(s):** 607–618
**Severity:** HIGH
**Category:** Data Exposure — Driver Card/PIN and Wiegand IDs
**Description:**
The driver list table renders the card prefix (site code), the full card/PIN number, and the Wiegand ID for every driver in plaintext. These are physical access credentials used by the forklift access control system. Their exposure in a web table accessible to all authenticated users of appropriate level means that any user who can view this page — or who receives a forwarded screenshot or URL — obtains credentials that could enable card cloning or unauthorised vehicle access.

**Evidence:**
```jsp
// Lines 609–611 — Card/PIN rendered to screen
<%tmp = ""+Vcard_id.get(i);
if((tmp.equalsIgnoreCase("null"))||(tmp.equalsIgnoreCase(""))){tmp="-";}%>
<td> <%=tmp %></td>

// Lines 617–618 — Wiegand ID rendered
<td>
<%=Vuser_wiegand.get(i) %>
</td>
```

**Recommendation:**
Mask the card/PIN and Wiegand ID in the list view (e.g., show only the last 4 characters). Full values should only be visible in an edit form accessible to administrators, over HTTPS, with audit logging. Review whether the Wiegand ID needs to be displayed at all in the web interface.

---

### A12u-8
**File:** `master/existing_customer_lst.jsp`
**Line(s):** 382 (`<form>` has no `method` or `action`)
**Severity:** MEDIUM
**Category:** Design / Security Control Deficiency — Form Without Action
**Description:**
The customer list form has no `method` or `action` attribute (`<form>`). Navigation and filtering rely entirely on JavaScript `location.replace()`. While this is a usability issue rather than a direct attack vector, the absence of a form action means that if JavaScript is disabled or bypassed, state-changing requests may be submitted to the page itself with undefined server-side behaviour. Additionally, the "Add/Edit Site" button triggers `goto_site()` which navigates to `frm_customer_rel.jsp?user_cd=`+ccd — passing the customer code as a URL parameter, allowing IDOR (see A12u-10).

**Evidence:**
```jsp
// Line 382
<form>
```

**Recommendation:**
Explicitly declare `method="get"` (for read-only filter forms) or `method="post"` with a CSRF token (for state-changing forms). Do not rely on JavaScript-only navigation for security controls.

---

### A12u-9
**File:** `master/existing_customer_lst.jsp`
**Line(s):** 469, 471, 479
**Severity:** HIGH
**Category:** XSS — Stored in HTML and JS Context
**Description:**
Customer company name (`Vuser_id`, line 471), account prefix (`Vuser_gmtp`, line 469), contact email (`Vuser_email`, line 479), and phone number (`Vuser_phno`, line 475) are all rendered raw. Company name and email in particular are free-text fields that could contain HTML/JS payloads. The JS onclick on line 469 interpolates the customer code and company name into a JavaScript string without escaping.

**Evidence:**
```jsp
// Line 469 — customer code and name in JS onclick
<td> <a href="#" onClick="open_edit('<%=Vuser_cd.get(i) %>','<%=Vuser_id.get(i) %>');"><%=Vuser_gmtp.get(i) %></a>

// Line 471 — company name raw
<td> <%=Vuser_id.get(i) %></td>

// Line 479 — email raw
<td> <%=tmp %></td>
```

**Recommendation:**
HTML-encode all values output into HTML context. JavaScript-escape all values interpolated into JavaScript string literals within event handlers.

---

### A12u-10
**File:** `master/frm_access_customer.jsp`
**Line(s):** 136, 159
**Severity:** CRITICAL
**Category:** IDOR — user_cd Taken From Request Parameter
**Description:**
The `user_cd` parameter on line 136 is read directly from the HTTP request and passed to `filter.setSet_user_cd(user_cd)` on line 159, which loads that user's customer access rights. There is no verification that the requesting user is permitted to view or modify the target user's access rights. Any authenticated user who can reach this page can supply an arbitrary `user_cd` value to view or, via the save form, overwrite any other user's customer access permissions.

This is a classic Insecure Direct Object Reference: the application uses a client-supplied identifier to authorise access to a resource, without checking that the resource belongs to the requester's scope.

**Evidence:**
```jsp
// Line 136 — user_cd from request with no session validation
String user_cd = request.getParameter("user_cd")==null?"":request.getParameter("user_cd");

// Line 159 — passed directly to data layer
filter.setSet_user_cd(user_cd);
```

**Recommendation:**
After reading `user_cd` from the request, validate server-side that the requesting session's user is either (a) the same user, or (b) has an access level that permits managing the target user. The target user's customer scope should be verified against `access_cust` from the session to ensure cross-customer access is not possible.

---

### A12u-11
**File:** `master/frm_access_customer.jsp`
**Line(s):** 222 (form action `../servlet/Frm_saveuser`), op_code `set_access_customers`
**Severity:** HIGH
**Category:** CSRF — No Token on State-Changing Form
**Description:**
The form that saves customer access rights for a user has no CSRF token. Combined with A12u-10 (IDOR), an attacker can craft a cross-site request that grants or revokes a target user's access to any customer.

**Evidence:**
```jsp
// Line 222
<form method="post" action="../servlet/Frm_saveuser">
// Line 273
<input type="hidden" name="op_code" value="set_access_customers"/>
// No CSRF token field present anywhere in the form.
```

**Recommendation:**
Implement the Synchronizer Token Pattern. Fix A12u-10 (IDOR) first — a CSRF fix alone does not protect against a logged-in attacker directly submitting the form.

---

### A12u-12
**File:** `master/frm_access_customer.jsp`
**Line(s):** 235, 253, 268
**Severity:** HIGH
**Category:** XSS — Reflected/Stored in HTML and JS Context
**Description:**
User first/last names (lines 235), customer names (line 253), and the `message` request parameter (line 268) are output without HTML encoding. An attacker who stores a malicious payload in a user's name or a customer's name achieves stored XSS on this access-management page. Exploiting this on an admin session would allow privilege escalation.

**Evidence:**
```jsp
// Line 235 — user name in option text
<option value="<%=vuser_cd.get(i) %>"><%=vuser_fnm.get(i) %> <%=vuser_lnm.get(i) %></option>

// Line 253 — customer name raw
<td><%=vcust_nm.get(i)%></td>

// Line 268 — message parameter raw
&nbsp; <%=message %>
```

**Recommendation:**
HTML-encode all DB-sourced values in HTML contexts. Especially critical here because this is a privilege-management page.

---

### A12u-13
**File:** `master/frm_blacklist_driv.jsp`
**Line(s):** 776
**Severity:** HIGH
**Category:** XSS — Reflected `message` Parameter in HTML
**Description:**
The `message` request parameter is rendered directly into a `<tr>` element without HTML encoding. Unlike other pages where it appears in a `<p>` tag, here it appears in a table row context, making HTML injection slightly easier to exploit visually and still fully capable of XSS.

**Evidence:**
```jsp
// Line 776
<tr class="heading2"><%=message %>
</tr>
```

**Recommendation:**
HTML-encode the `message` parameter before output: `<%=ESAPI.encoder().encodeForHTML(message) %>`.

---

### A12u-14
**File:** `master/frm_blacklist_driv.jsp`
**Line(s):** 714 (form action), 946 (op_code `blacklist_driv`)
**Severity:** HIGH
**Category:** CSRF — No Token on State-Changing Form
**Description:**
The blacklist form, which restricts specific drivers from operating specific vehicle types or individual vehicles, has no CSRF token. An attacker can forge a cross-site request to blacklist or unblacklist any driver visible to the victim's session.

**Evidence:**
```jsp
// Line 714
<form method="post" action="../servlet/Frm_saveuser">
// Line 946
<input type="hidden" name="op_code" value="blacklist_driv">
// No CSRF token present.
```

**Recommendation:**
Implement the Synchronizer Token Pattern.

---

### A12u-15
**File:** `master/frm_blacklist_driv.jsp`
**Line(s):** 795–817 (driver checkboxes), 796–817 (driver first/last names)
**Severity:** HIGH
**Category:** XSS — Stored in HTML Context
**Description:**
Driver first and last names are rendered into table cells adjacent to checkboxes without HTML encoding. A driver name containing `<script>alert(1)</script>` or `"><img src=x onerror=alert(1)>` would execute in any admin session loading this page.

**Evidence:**
```jsp
// Line 796 — driver name unescaped in table cell
<td><input type="checkbox" name="driver" value="<%=Vuser_cd.get(i) %>"/>
 <%=Vuser_fnm.get(i) %> <%=Vuser_lnm.get(i) %>
</td>
```

**Recommendation:**
HTML-encode `Vuser_fnm.get(i)` and `Vuser_lnm.get(i)` before rendering.

---

### A12u-16
**File:** `master/existing_opchk_lst.jsp`
**Line(s):** 578, 631
**Severity:** HIGH
**Category:** XSS — Stored via Question Text
**Description:**
The operational checklist question text (`vquest.get(i)`, line 578) is rendered raw into a table cell. Questions are created by administrators via `frm_new_question.jsp`. If a question is crafted with embedded HTML/JS, it executes in any session that loads this page. The `message` request parameter (line 631) is also reflected raw.

**Evidence:**
```jsp
// Line 578 — question text from DB, unescaped
<td> <%=vquest.get(i) %>
</td>

// Line 631 — reflected message
&nbsp; <%=message %>
```

**Recommendation:**
HTML-encode `vquest.get(i)` and the `message` parameter.

---

### A12u-17
**File:** `master/existing_opchk_lst.jsp`
**Line(s):** 557, 562, 574, 611, 621
**Severity:** HIGH
**Category:** XSS — Stored via JS Context (onclick handlers)
**Description:**
Check codes (`vchk_cd.get(i)`) and the customer name (`get_cust`) are interpolated into JavaScript `onclick` handlers without escaping. The `get_cust` value used in `open_upload('<%=get_cust %>')` on line 621 is a customer name from the DB — if the name contains a single quote, it breaks the JS string and allows injection.

**Evidence:**
```jsp
// Line 557 — check code in JS onclick
<a href="#" onClick="reorder('<%=vchk_cd.get(i) %>','<%=vchk_cd.get(i-1) %>');">

// Line 621 — customer name in JS onclick
<input type=button ... onClick="open_upload('<%=get_cust %>');">
```

**Recommendation:**
JavaScript-escape all values placed into JS string contexts: `<%=StringEscapeUtils.escapeEcmaScript(get_cust) %>` etc.

---

### A12u-18
**File:** `master/existing_opchk_lst.jsp`
**Line(s):** 457 (form action), 637 (op_code `quest_del`), 319 (op_code `re-ord`)
**Severity:** HIGH
**Category:** CSRF — No Token on State-Changing Form
**Description:**
The operational checklist form, which deletes questions and reorders them, posts to `../servlet/Frm_saveuser` with no CSRF token. A forged request can delete or reorder any operational safety question, undermining the safety check workflow.

**Evidence:**
```jsp
// Line 457
<form method="post" action="../servlet/Frm_saveuser">
// Line 637
<input type="hidden" name="op_code" value="quest_del">
// No CSRF token present.
```

**Recommendation:**
Implement the Synchronizer Token Pattern.

---

### A12u-19
**File:** All six JSPs
**Line(s):** See per-file evidence above (access_level check pattern)
**Severity:** MEDIUM
**Category:** Authentication / Session — Weak Access Level Enforcement Pattern
**Description:**
All pages read `access_level` from the session and use it to determine which UI elements to show (e.g., "Add" and "Delete" buttons). However, this is a client-side hiding mechanism only — the buttons trigger form submissions to `Frm_saveuser` which must enforce the same access level server-side. Additionally, the `access_level` value is written back into the page as a hidden form field (`<input type="hidden" name="alevel" value="<%=access_level %>"/>`), which means a user with browser developer tools can modify it before form submission, potentially bypassing client-side controls if the servlet relies on the posted `alevel` value rather than the session value.

**Evidence:**
```jsp
// existing_user_lst.jsp line 626
<input type="hidden" name="alevel" value="<%=access_level %>"/>

// existing_driver_lst.jsp line 652
<input type="hidden" name="alevel" value="<%=access_level %>"/>

// frm_blacklist_driv.jsp line 954
<input type="hidden" name="alevel" value="<%=access_level %>"/>

// existing_opchk_lst.jsp line 644
<input type="hidden" name="alevel" value="<%=access_level %>"/>
```

**Recommendation:**
Verify that `Frm_saveuser` reads the access level exclusively from `session.getAttribute("access_level")` and never from `request.getParameter("alevel")`. If it currently uses the request parameter, this is an immediate privilege escalation vulnerability. Audit `Frm_saveuser` as a priority follow-on action.

---

### A12u-20
**File:** `master/existing_user_lst.jsp`
**Line(s):** 350–355
**Severity:** MEDIUM
**Category:** IDOR — Customer/Site/Dept Scope From Request Parameters
**Description:**
`cust_cd`, `loc_cd`, and `dept_cd` are read from request parameters (lines 350–352). While the Databean is also initialised with `access_cust`, `access_site`, and `access_dept` from the session, it is unclear from the JSP alone whether the bean enforces these session-scope limits when `cust_cd` is supplied directly. If the data layer does not enforce session-scope filtering when a request parameter overrides it, a lower-privileged user could supply a different `cust_cd` to list users belonging to a different customer.

This same pattern exists in `existing_driver_lst.jsp` (lines 368–371), `frm_blacklist_driv.jsp` (lines 593–596), and `existing_opchk_lst.jsp` (lines 333–336).

**Evidence:**
```jsp
// existing_user_lst.jsp lines 350–352
String cust_cd = request.getParameter("cust_cd")==null?"":request.getParameter("cust_cd");
String loc_cd = request.getParameter("loc_cd")==null?"":request.getParameter("loc_cd");
String dept_cd = request.getParameter("dept_cd")==null?"":request.getParameter("dept_cd");

// All three then passed into filter bean alongside session-sourced access_cust
filter.setAccess_cust(access_cust);   // from session
filter.setSet_cust_cd(cust_cd);       // from request — may override
```

**Recommendation:**
Audit `Databean_getuser` to confirm it enforces session-scope access restrictions and that a request-supplied `cust_cd` that does not belong to the session's `access_cust` is rejected. Document this in the data layer as an explicit access control assertion.

---

## Summary Table

| ID | File | Severity | Category |
|----|------|----------|----------|
| A12u-1 | existing_user_lst.jsp | CRITICAL | XSS — JS Context (onload + onclick) |
| A12u-2 | existing_user_lst.jsp | HIGH | XSS — Reflected HTML (message, search_crit) |
| A12u-3 | existing_user_lst.jsp | HIGH | Data Exposure (access level, Wiegand, debug artefacts) |
| A12u-4 | existing_user_lst.jsp | HIGH | CSRF — user delete/recover form |
| A12u-5 | existing_driver_lst.jsp | CRITICAL | XSS — JS Context + card/PIN data |
| A12u-6 | existing_driver_lst.jsp | HIGH | CSRF — driver delete/recover form |
| A12u-7 | existing_driver_lst.jsp | HIGH | Data Exposure — Card/PIN and Wiegand IDs |
| A12u-8 | existing_customer_lst.jsp | MEDIUM | Design — form without method/action |
| A12u-9 | existing_customer_lst.jsp | HIGH | XSS — Stored (company name, email, JS onclick) |
| A12u-10 | frm_access_customer.jsp | CRITICAL | IDOR — user_cd from request param |
| A12u-11 | frm_access_customer.jsp | HIGH | CSRF — access rights save form |
| A12u-12 | frm_access_customer.jsp | HIGH | XSS — Stored (user/customer names, message) |
| A12u-13 | frm_blacklist_driv.jsp | HIGH | XSS — Reflected message in table row |
| A12u-14 | frm_blacklist_driv.jsp | HIGH | CSRF — blacklist form |
| A12u-15 | frm_blacklist_driv.jsp | HIGH | XSS — Stored driver names in checkboxes |
| A12u-16 | existing_opchk_lst.jsp | HIGH | XSS — Stored question text + reflected message |
| A12u-17 | existing_opchk_lst.jsp | HIGH | XSS — Stored (JS onclick, customer name) |
| A12u-18 | existing_opchk_lst.jsp | HIGH | CSRF — question delete/reorder form |
| A12u-19 | All six JSPs | MEDIUM | Auth — access_level exposed as mutable hidden field |
| A12u-20 | existing_user_lst.jsp + 3 others | MEDIUM | IDOR — cust_cd/loc_cd/dept_cd from request |

**Total findings: 20**
**Critical: 3** (A12u-1, A12u-5, A12u-10)
**High: 14** (A12u-2, 3, 4, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18)
**Medium: 3** (A12u-8, A12u-19, A12u-20)

---

*Report generated by audit agent A12-user, 2026-02-25, run 2026-02-25-01.*
