# GPS JSP Security Audit — Pass 1
**Audit run:** 2026-02-25-01
**Agent:** A11
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Files reviewed:** 7
**Findings:** 12

---

## Step 3 — Reading Evidence

### 1. `gps/Copy of gpsZonesData.jsp`

- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **useBean:** `com.torrent.surat.fms6.master.Databean_getuser` id=`filter` scope=`request`
- **Error page:** `../home/ExceptionHandler.jsp`
- **Includes:** None
- **Scriptlet (lines 5–61):** Reads `site` and `ccd` from request parameters; passes them directly to `filter.setSet_loc_cd()` / `filter.setSet_cust_cd()`; fetches GPS zone data; builds XML response by string-concatenating zone names (`znm`) and IDs (`zcd`) from DB into XML attribute values.
- **Expression outputs:** None (all output via `out.println(resp)` inside scriptlet). Zone name embedded unescaped into XML attribute value at line 42: `resp=resp+"<zone name='"+znm+"' id='"+zcd+"'>";`
- **Forms:** None
- **Session check:** None

---

### 2. `gps/gpsWhereIAm.jsp`

- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `<%@ include file="../sess/Expire.jsp" %>` (line 2), `<%@ include file="../menu/menu.jsp" %>` (line 372)
- **useBeans:** `com.torrent.surat.fms6.reports.Databean_report` id=`filter` scope=`request`; `com.torrent.surat.fms6.util.UtilBean` id=`Util` scope=`page`
- **Scriptlet (lines 256–348):** Reads `gp_cd`, `user_cd`, `loc_cd`, `dept_cd`, `form_cd` from request parameters; reads session attributes `access_level`, `access_cust`, `access_site`, `access_dept`; passes all to `filter`; calls `filter.init()`. **No session check guards these request parameters against cross-customer access at the JSP level.**
- **Expression outputs:**
  - Line 7: `<%=LindeConfig.systemName %>` — static config value, safe
  - Line 350 (body onload): `set('<%=user_cd %>','<%=loc_cd %>','<%=dept_cd %>')` — DB-sourced, but if defaults fall back to user-supplied request params without sanitisation, XSS is possible
  - Line 394: `<%=form_nm %>` — DB-sourced report name, unescaped
  - Lines 402–403: `<%=Vuser_cd.get(i) %>`, `<%=Vuser_nm.get(i) %>` — DB-sourced, unescaped HTML
  - Lines 411, 412: `<%=Vloc_cd.get(i) %>`, `<%=Vloc_nm.get(i) %>` — DB-sourced, unescaped
  - Lines 426–427: `<%=vdept_cd.get(i) %>`, `<%=vdept_nm.get(i) %>` — DB-sourced, unescaped
  - Lines 436–437: `<%=veh_cd.get(i) %>` — DB-sourced, unescaped; `<%=user_gmtp_prefix+veh_nm.get(i) %>` — DB-sourced string concatenation, unescaped
  - Line 452: `<%=form_cd %>` — user-controlled request parameter echoed to hidden field, unescaped
  - Line 453: `<%=access_level %>` — session-sourced, unescaped
- **JavaScript blocks:** `gpsTracker.updateMap()` at line 588 constructs: `var url = "unit.gps.jsp?&ccd="+cust_cd+"&site="+site_cd+"&dep="+dep_cd;` — these are taken from DOM form values (themselves DB-sourced), passed via URL to `unit.gps.jsp`. No sanitisation.
- **Forms:** Single unnamed form (line 390) — GET method implied; fields: `usr`, `site`, `dep`, `unitlst`, `form_cd` (hidden), `alevel` (hidden), `interval` (hidden). No CSRF token.

---

### 3. `gps/gpsZonesData.jsp`

- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **useBean:** `com.torrent.surat.fms6.master.Databean_getuser` id=`filter` scope=`request`
- **Error page:** `../home/ExceptionHandler.jsp`
- **Includes:** None
- **Scriptlet (line 1–61):** Identical logic to `Copy of gpsZonesData.jsp`. Reads `site` and `ccd` from request parameters with no session validation; passes to bean; builds XML with DB zone names embedded unescaped into XML attributes.
- **Expression outputs:** None (scriptlet-only output)
- **Forms:** None
- **Session check:** None

---

### 4. `gps/setGpsZones.jsp`

- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **useBean:** `com.torrent.surat.fms6.master.Databean_getuser` id=`filter` scope=`request`
- **Error page:** `../home/ExceptionHandler.jsp`
- **Includes:** None
- **Scriptlet (lines 6–36):** Reads `site`, `ccd`, `zpoints0`–`zpoints3`, `zcds`, `znames`, `zsizes` from request; passes all directly to bean; calls `filter.init()` to persist zone data. Response is the msg from the bean.
- **Expression outputs:** None
- **Forms:** None (data-only endpoint, called via AJAX POST from `ajaxSendStore.js`)
- **Session check:** None — no `<%@ include file="../sess/Expire.jsp" %>` present

---

### 5. `gps/speedZones.jsp`

- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **Includes:** `<%@ include file="../sess/Expire.jsp" %>` (line 2), `<%@ include file="../menu/menu.jsp" %>` (line 359)
- **useBeans:** `com.torrent.surat.fms6.reports.Databean_report` id=`filter` scope=`request`; `com.torrent.surat.fms6.util.UtilBean` id=`Util` scope=`page`
- **Scriptlet (lines 239–335):** Same pattern as `gpsWhereIAm.jsp`. Session access-level variables read and passed to bean, but `user_cd`, `loc_cd`, `dept_cd`, `form_cd` come from request parameters and are passed without cross-customer verification at JSP level.
- **Expression outputs (unescaped):**
  - Line 337: body onload: `set('<%=user_cd %>','<%=loc_cd %>','<%=dept_cd %>')` — partially user-controlled
  - Line 381: `<%=form_nm %>` — DB-sourced, unescaped
  - Lines 390, 391: user/site/dept/vehicle codes and names — DB-sourced, unescaped
  - Line 424: `<%=veh_cd.get(i) %>`, `<%=veh_nm.get(i) %>` — DB-sourced, unescaped
  - Line 431: `<%=form_cd %>` — user-controlled request parameter echoed to hidden field, unescaped
  - Line 432: `<%=access_level %>` — session-sourced, unescaped
- **JavaScript:** `initialize($('#cust').val(),$('#site').val())` at line 468 — passes DOM values (DB-sourced codes) to JS; calls into `ajaxSendStore.js` which constructs URL for `gpsZonesData.jsp` and `unit.gps.jsp`.
- **Forms:** Single unnamed form (line 377) — GET method implied; fields: `usr`, `site`, `dep`, `unitlst`, `form_cd` (hidden), `alevel` (hidden). No CSRF token.

---

### 6. `gps/speedZones_back.jsp`

- Structurally identical to `speedZones.jsp`. Includes `../sess/Expire.jsp`, `../menu/menu.jsp`. Same scriptlet logic, same expression outputs. Difference: uses Google Maps API (line 18) rather than Leaflet, and outputs `user_gmtp_prefix` is absent from vehicle display (line 420 outputs `<%=veh_nm.get(i) %>` without prefix).
- **Same findings apply as speedZones.jsp.** This file is a backup/stale copy deployed alongside the live file.

---

### 7. `gps/unit.gps.jsp`

- **Imports:** `java.util.*`, `com.torrent.surat.fms6.util.*`
- **useBean:** `com.torrent.surat.fms6.reports.Databean_report` id=`filter` scope=`request`
- **Error page:** `../home/ExceptionHandler.jsp`
- **Includes:** None
- **Scriptlet (lines 1–38):** Reads `ccd`, `site`, `dep`, `unit` (multi-value) from request parameters. All are passed directly to the bean without session-based customer ownership verification. Returns JSON array of GPS unit positions (lat, lon, name, time, speed, heading, model, dept).
- **Expression outputs:** None (scriptlet-only output)
- **Forms:** None
- **Session check:** None — no `<%@ include file="../sess/Expire.jsp" %>` present

---

## Step 5 — Findings

---

### A11-1
**File:** `gps/unit.gps.jsp` — lines 1, 3–6
**Severity:** CRITICAL
**Category:** Broken Access Control / GPS Data Exposure
**Description:** `unit.gps.jsp` is the JSON endpoint that returns real-time GPS location data (latitude, longitude, unit name, speed, heading) for fleet vehicles. It has no session authentication check whatsoever — `Expire.jsp` is not included. Any unauthenticated HTTP request supplying arbitrary `ccd` (customer code) and `site` parameters will receive live GPS location data for that customer's vehicles. This is an unauthenticated GPS data disclosure endpoint.
**Evidence:**
```jsp
// Line 1 — no Expire.jsp include, no session check at all
<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>
<%@ page errorPage="../home/ExceptionHandler.jsp" %>
<jsp:useBean class="com.torrent.surat.fms6.reports.Databean_report" id="filter" scope="request"/>
<%
String cust_cd=request.getParameter("ccd")==null?"0":request.getParameter("ccd");
String st_cd=request.getParameter("site")==null?"0":request.getParameter("site");
String dept_cd= request.getParameter("dep")==null?"0":request.getParameter("dep");
String[] unitlst = request.getParameterValues("unit");
// ...no session.getAttribute("user_cd") check, no Expire.jsp include
filter.setSet_cust_cd(cust_cd);
filter.setSet_loc_cd(st_cd);
```
**Recommendation:** Add `<%@ include file="../sess/Expire.jsp" %>` as the first statement. Additionally, the `ccd` parameter must be validated server-side against `session.getAttribute("access_cust")` to enforce customer-scoping — an authenticated user must not be able to supply an arbitrary customer code to retrieve another customer's vehicle locations.

---

### A11-2
**File:** `gps/gpsZonesData.jsp` — lines 1, 3–5
**Severity:** CRITICAL
**Category:** Broken Access Control / GPS Zone Data Exposure
**Description:** `gpsZonesData.jsp` returns GPS zone boundary data (lat/lng polygon points and zone names) for any customer code and site code passed in request parameters. There is no session authentication check — `Expire.jsp` is not included, and no session attribute is read. An unauthenticated or cross-tenant request can retrieve zone configurations for any customer.
**Evidence:**
```jsp
// Line 1 — all on one line, no Expire.jsp, no session check
<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>
<%@ page errorPage="../home/ExceptionHandler.jsp" %>
<jsp:useBean class="com.torrent.surat.fms6.master.Databean_getuser" id="filter" scope="request"/>
<%
response.setContentType("text/xml");
String st_cd=request.getParameter("site");   // line 3
String cust_cd=request.getParameter("ccd");  // line 4
// no session validation before use
filter.setSet_loc_cd(st_cd);
filter.setSet_cust_cd(cust_cd);
```
**Recommendation:** Add `<%@ include file="../sess/Expire.jsp" %>` as the first statement. Validate `ccd` against `session.getAttribute("access_cust")` before executing the zone query.

---

### A11-3
**File:** `gps/setGpsZones.jsp` — lines 1–36 (entire file)
**Severity:** CRITICAL
**Category:** Broken Access Control / Missing Authentication on Data-Modifying Endpoint
**Description:** `setGpsZones.jsp` is a write endpoint that creates or updates GPS geofence zones (polygon coordinates and names) in the database. It has no session authentication check — `Expire.jsp` is not included. Any unauthenticated HTTP POST can write zone data for an arbitrary customer (`ccd`) and site (`site`). Additionally, there is no CSRF token, so an authenticated user can be made to submit zone modifications via a CSRF attack.
**Evidence:**
```jsp
// setGpsZones.jsp lines 1–10: no Expire.jsp, no session check
<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
<%@ page import="java.util.*,com.torrent.surat.fms6.util.*"%>
<%@ page errorPage="../home/ExceptionHandler.jsp" %>
<jsp:useBean class="com.torrent.surat.fms6.master.Databean_getuser" id="filter" scope="request"/>
<%
    response.setContentType("text/xml");
    String st_cd=request.getParameter("site");
    String cust_cd=request.getParameter("ccd");
    String op_code="save_gps_zones_ajax";
    // ... no session.getAttribute check
    filter.setSet_loc_cd(st_cd);
    filter.setSet_cust_cd(cust_cd);
    filter.setSet_op_code(op_code);
    // zone data arrays from request parameters passed straight to persistence
    filter.setZcds(zcds);
    filter.setZnames(znames);
    filter.init(); // saves to database
```
**Recommendation:** Add `<%@ include file="../sess/Expire.jsp" %>`. Validate `ccd` against `session.getAttribute("access_cust")`. Implement a synchroniser-token CSRF defence for all state-changing AJAX endpoints.

---

### A11-4
**File:** `gps/Copy of gpsZonesData.jsp` — entire file
**Severity:** HIGH
**Category:** Stale/Backup File Deployed to Production
**Description:** A file named `Copy of gpsZonesData.jsp` (with a Windows "Copy of" prefix naming convention indicating it was created by a developer via Explorer copy operation) exists in the production `gps/` directory and is a functional JSP that the web container will serve at its URL. It is functionally equivalent to `gpsZonesData.jsp` (same logic, only whitespace and commented debug `System.out.println` differences). It shares the same access control deficiencies (no session check, no customer scoping). Backup/copy files deployed to production increase attack surface and may not receive security patches applied to the primary file.
**Evidence:**
```
File: gps/Copy of gpsZonesData.jsp
diff shows only:
- Line formatting (multi-line vs single-line page directives)
- Two commented-out System.out.println debug lines present in gpsZonesData.jsp only
- Logic is identical
```
**Recommendation:** Remove `gps/Copy of gpsZonesData.jsp` from the production deployment immediately. Add a build/deployment process check to reject files matching `Copy of *` or `*_back.*` patterns.

---

### A11-5
**File:** `gps/speedZones_back.jsp` — entire file
**Severity:** HIGH
**Category:** Stale/Backup File Deployed to Production
**Description:** `speedZones_back.jsp` is a backup copy of `speedZones.jsp` (the `_back` suffix is a common developer backup naming convention). Both files are functional JSPs served by the web container. The `_back` version uses the old Google Maps API integration while the live version uses Leaflet — indicating it is a prior-version snapshot left in the deployment. It is identical in session and access-control structure to the live file (both include `Expire.jsp`) but it unnecessarily expands attack surface and may be missed during future patching.
**Evidence:**
```
speedZones_back.jsp line 18:
<script src="http://maps.googleapis.com/maps/api/js?v=3&client=gme-collectiveintelligence&channel=fms.fleetiq360.com"></script>
vs speedZones.jsp lines 17-22 which uses Leaflet.
Both files include Expire.jsp and have the same scriptlet structure.
```
**Recommendation:** Remove `speedZones_back.jsp` from the production deployment. Use version control (Git) to preserve history; backup files must not be deployed.

---

### A11-6
**File:** `gps/gpsWhereIAm.jsp` — line 290; `gps/speedZones.jsp` — line 276
**Severity:** HIGH
**Category:** Broken Access Control — Cross-Customer GPS Data Access
**Description:** Both `gpsWhereIAm.jsp` and `speedZones.jsp` read the target customer code from the request parameter `user_cd` (line 261 / 244) and pass it to the data bean as `filter.setSet_cust_cd(user_cd)`. Although `Expire.jsp` enforces that a session exists, there is no check that the requested `user_cd` matches or is subordinate to `session.getAttribute("access_cust")`. A lower-privileged authenticated user can manipulate the `user_cd` URL parameter to request GPS location and zone data for another customer's fleet. The `access_cust` session variable is passed to the bean but only for use in query-level scoping within the bean — the JSP itself never asserts that `user_cd == access_cust` (or is a child thereof). Higher-access levels (al < 3/4) may legitimately see multiple customers, but there is no demonstrated guard preventing lateral movement.
**Evidence:**
```jsp
// gpsWhereIAm.jsp lines 261, 271, 289-290
String user_cd = request.getParameter("user_cd")==null?"":request.getParameter("user_cd");
// ...
String access_cust=(String)session.getAttribute("access_cust");
// ...
filter.setAccess_cust(access_cust);     // passed to bean for scoping
filter.setSet_cust_cd(user_cd);          // user-supplied customer code — never compared to access_cust in JSP
filter.init();
```
**Recommendation:** Before calling `filter.init()`, assert that `user_cd` equals `access_cust` (for access levels >= 3) or is within the list of permitted customers. Reject requests where the supplied customer code does not correspond to the authenticated user's permitted scope.

---

### A11-7
**File:** `gps/gpsWhereIAm.jsp` — line 452; `gps/speedZones.jsp` — line 431; `gps/speedZones_back.jsp` — line 427
**Severity:** MEDIUM
**Category:** Cross-Site Scripting (Reflected XSS) — Request Parameter Echoed to HTML
**Description:** The request parameter `form_cd` is read from the query string and echoed directly into a hidden HTML form field without HTML encoding. If an attacker can craft a link with a malicious `form_cd` value, the payload will be rendered in the victim's browser in the context of the page.
**Evidence:**
```jsp
// gpsWhereIAm.jsp line 452
<input type="hidden" name="form_cd" value="<%=form_cd %>"/>

// form_cd is set at line 264:
String form_cd = request.getParameter("form_cd")==null?"":request.getParameter("form_cd");
// No escaping applied before output
```
A payload of `form_cd="><script>alert(1)</script>` would break out of the attribute and execute.
**Recommendation:** HTML-encode all request parameters before echoing to HTML. Use `ESAPI.encoder().encodeForHTML(form_cd)` or equivalent. The value should also be validated to be a known form code before use.

---

### A11-8
**File:** `gps/gpsWhereIAm.jsp` — lines 403, 412, 427, 437; `gps/speedZones.jsp` — lines 390–391, 399–400, 414–415, 424–425; `gps/speedZones_back.jsp` — same
**Severity:** MEDIUM
**Category:** Cross-Site Scripting (Stored XSS via DB values) — Unescaped HTML Output
**Description:** Numerous `<%= %>` expressions output database-sourced strings (customer names, site names, department names, vehicle codes, vehicle names, report names) directly into HTML `<option>` elements and table cells without HTML encoding. If any of these database fields contain characters such as `<`, `>`, `"`, or `&` (whether from legitimate data or from a stored XSS payload introduced via an unprotected admin interface), they will be rendered as HTML.
**Evidence:**
```jsp
// gpsWhereIAm.jsp lines 402-403 (unescaped DB string in option elements)
<option value="<%=Vuser_cd.get(i) %>"><%=Vuser_nm.get(i) %></option>

// line 437 (unescaped DB string concatenated into option)
<option value="<%=veh_cd.get(i) %>"><%=user_gmtp_prefix+veh_nm.get(i) %></option>

// line 394 (unescaped DB string in table cell)
<td align=center colspan=9> <%=form_nm %>
```
**Recommendation:** All `<%= %>` outputs to HTML must be wrapped with an HTML-encoding utility. Introduce a project-wide encoding helper (e.g., `HtmlUtils.htmlEscape(value)` or ESAPI's `encodeForHTML`) and apply it to every DB-sourced string rendered into HTML context.

---

### A11-9
**File:** `gps/gpsWhereIAm.jsp` — lines 638–641 (JavaScript block); `gps/ajaxSendStore.js` — lines 849–858
**Severity:** MEDIUM
**Category:** Cross-Site Scripting — Unescaped DB Values Interpolated into JavaScript String
**Description:** In `gpsWhereIAm.jsp`, the `unit.name`, `unit.time`, `unit.speed` values returned from the JSON GPS endpoint are interpolated directly into an HTML string assigned to `contentString` and inserted into a Google Maps InfoWindow. In `ajaxSendStore.js`, `unit.name`, `unit.model`, `unit.dept`, `unit.time` are similarly interpolated. These values originate from the database via `unit.gps.jsp`'s JSON response. If a vehicle name, model, or department name contains HTML/JavaScript, it will be executed in the map info popup context (DOM-based XSS).
**Evidence:**
```javascript
// gpsWhereIAm.jsp lines 638-641
var contentString = '<div style="width:200px; ...">'+
    '<span style="...">Unit:</span><strong>'+unit.name+   // DB value, unescaped
    '</strong><br />...Time:</span>'+unit.time+           // DB value, unescaped
    '...<br />...Speed:</span> '+unit.speed+              // DB value, unescaped
    '...<br />...Heading:</span> '+icnNameTbl+'</div>';

// ajaxSendStore.js lines 849-858
var contentString = '...<strong>'+ unit.name +'</strong>...'  // DB value, unescaped
    + unit.model + '...' + unit.dept + '...' + unit.time + '...';
```
**Recommendation:** HTML-encode all database-sourced values before interpolating into HTML strings in JavaScript. Use a client-side encoding function or use DOM methods (`document.createElement`, `textContent`) rather than string concatenation to build InfoWindow content.

---

### A11-10
**File:** `gps/gpsZonesData.jsp` — lines 41, 45–47; `gps/Copy of gpsZonesData.jsp` — lines 42, 46–47
**Severity:** MEDIUM
**Category:** XML Injection — Unescaped DB Values in XML Output
**Description:** Zone names (`znm`) and zone IDs (`zcd`) retrieved from the database are interpolated directly into XML attribute values without XML encoding. A zone name containing a single quote or angle bracket will produce malformed XML, and a crafted value could inject additional XML elements or attributes into the response consumed by the JavaScript XML parser in `ajaxSendStore.js`.
**Evidence:**
```jsp
// gpsZonesData.jsp line 41
resp=resp+"<zone name='"+znm+"' id='"+zcd+"'>";
// znm and zcd from DB (vpn.get(4) and vpn.get(3)) — no XML encoding

// lines 45-47
resp=resp+"<point id='"+pno+"'>"+"<lat>"+
lat+"</lat>"+"<lng>"+lon+"</lng>"+"</point>";
// lat/lon are expected numeric but sourced from DB without validation
```
A zone name of `' injected='value` would break the attribute boundary.
**Recommendation:** Apply XML attribute encoding to `znm`, `zcd`, and `pno` before embedding in XML. For lat/lon values, validate that they are numeric before output. Use an XML-building library rather than manual string concatenation.

---

### A11-11
**File:** `gps/gpsWhereIAm.jsp` — lines 16–18; `gps/speedZones_back.jsp` — line 18
**Severity:** MEDIUM
**Category:** Insecure External Resource Loading (HTTP, not HTTPS)
**Description:** Multiple external JavaScript libraries are loaded over plain HTTP rather than HTTPS. This exposes the application to man-in-the-middle attacks where an attacker on the network path could substitute the JavaScript payload with malicious code, leading to full compromise of the GPS tracking page (which handles vehicle location data).
**Evidence:**
```html
<!-- gpsWhereIAm.jsp line 16 -->
<script language="javascript" src="http://code.jquery.com/ui/1.8.21/jquery-ui.min.js"></script>

<!-- gpsWhereIAm.jsp line 18 -->
<script src="http://maps.googleapis.com/maps/api/js?v=3&client=gme-collectiveintelligence&channel=fms.fleetiq360.com"></script>

<!-- speedZones.jsp lines 16, 21, 22 -->
<script language="javascript" src="http://code.jquery.com/ui/1.8.21/jquery-ui.min.js"></script>
<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css" />
<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script>
<script src="http://cdn.jsdelivr.net/leaflet.esri/1.0.0/esri-leaflet.js"></script>
```
Additionally, jQuery UI 1.8.21 and Leaflet 0.7.3 are significantly outdated versions with known CVEs.
**Recommendation:** Serve all third-party libraries over HTTPS. Migrate to current supported versions. Preferably vendor/bundle libraries locally rather than using public CDNs, and implement Subresource Integrity (SRI) hashes.

---

### A11-12
**File:** `gps/gpsWhereIAm.jsp` — line 17; `gps/speedZones.jsp` — line 17; `gps/speedZones_back.jsp` — line 17
**Severity:** LOW
**Category:** Exposed / Hardcoded API Key in Source Code (Commented)
**Description:** A Google Maps API key (`AIzaSyCOyV9n_Yz5bcNNJfvvbAgZc016ThnFhFM`) is present in a commented-out script tag in three GPS JSP files. Although currently commented out, the key is present in version-controlled source code and any deployment artefact. Anyone with read access to the source (developers, contractors, repository exports, deployed WAR contents) can extract this key and use it.
**Evidence:**
```html
<!-- gpsWhereIAm.jsp line 17 (same in speedZones.jsp and speedZones_back.jsp) -->
<!-- <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCOyV9n_Yz5bcNNJfvvbAgZc016ThnFhFM"></script> -->
```
**Recommendation:** Remove the API key from source code entirely. If the key has been committed to version control history, treat it as compromised and rotate it immediately in the Google Cloud Console. Apply HTTP referrer restrictions to the key. Manage API keys via environment variables or a secrets manager, not source files.

---

## Summary Table

| ID | File(s) | Severity | Category |
|----|---------|----------|----------|
| A11-1 | `gps/unit.gps.jsp` | CRITICAL | No authentication — GPS location endpoint publicly accessible |
| A11-2 | `gps/gpsZonesData.jsp` | CRITICAL | No authentication — GPS zone data endpoint publicly accessible |
| A11-3 | `gps/setGpsZones.jsp` | CRITICAL | No authentication + no CSRF — zone write endpoint publicly accessible |
| A11-4 | `gps/Copy of gpsZonesData.jsp` | HIGH | Backup file deployed to production, same vulnerabilities as A11-2 |
| A11-5 | `gps/speedZones_back.jsp` | HIGH | Backup file deployed to production |
| A11-6 | `gps/gpsWhereIAm.jsp`, `gps/speedZones.jsp` | HIGH | Cross-customer GPS data access via unvalidated `user_cd` parameter |
| A11-7 | `gps/gpsWhereIAm.jsp`, `gps/speedZones.jsp`, `gps/speedZones_back.jsp` | MEDIUM | Reflected XSS via `form_cd` parameter echoed to HTML |
| A11-8 | `gps/gpsWhereIAm.jsp`, `gps/speedZones.jsp`, `gps/speedZones_back.jsp` | MEDIUM | Stored XSS — DB values output unescaped to HTML |
| A11-9 | `gps/gpsWhereIAm.jsp`, `gps/ajaxSendStore.js` | MEDIUM | DOM-based XSS — DB values interpolated unescaped into JS HTML strings |
| A11-10 | `gps/gpsZonesData.jsp`, `gps/Copy of gpsZonesData.jsp` | MEDIUM | XML injection — DB zone names unescaped in XML attribute values |
| A11-11 | `gps/gpsWhereIAm.jsp`, `gps/speedZones.jsp`, `gps/speedZones_back.jsp` | MEDIUM | External JS/CSS loaded over HTTP; outdated library versions |
| A11-12 | `gps/gpsWhereIAm.jsp`, `gps/speedZones.jsp`, `gps/speedZones_back.jsp` | LOW | Google Maps API key present in commented source code |
