# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent:** B02
**Date:** 2026-02-26

## Scope

| # | JSP File |
|---|----------|
| 1 | `src/main/webapp/html-jsp/adminRegister.jsp` |
| 2 | `src/main/webapp/html-jsp/adminReports.jsp` |
| 3 | `src/main/webapp/html-jsp/adminSubscription.jsp` |
| 4 | `src/main/webapp/html-jsp/adminUnit.jsp` |
| 5 | `src/main/webapp/html-jsp/adminUser.jsp` |
| 6 | `src/main/webapp/html-jsp/apiXml.jsp` |
| 7 | `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp` |
| 8 | `src/main/webapp/html-jsp/dealer/impactReport.jsp` |
| 9 | `src/main/webapp/html-jsp/dealer/incidentReport.jsp` |

**Test directory searched:** `src/test/java/`

**Test files found in project (total):**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep result for all nine JSP basenames in the test directory: NO MATCHES.** None of the nine JSP files under audit have any corresponding test coverage.

---

## Per-File Evidence and Findings

---

### 1. adminRegister.jsp

**Path:** `src/main/webapp/html-jsp/adminRegister.jsp`

**Purpose:** Self-contained company registration form (new account sign-up). Collects company name, timezone, address, first/last name, contact number, email, password, and confirm password. Submits to `adminRegister.do`. Displays Struts `<html:errors/>` and success messages via `<html:messages>`.

**Scriptlet blocks:** None. This JSP uses only Struts tag library elements.

**EL / Struts tag attribute access:**
- `arrTimezone` — request/session attribute iterated for timezone dropdown (`logic:iterate name="arrTimezone"`)
- `accountmsg` — Struts action messages written via `<bean:write name="accountmsg"/>`
- `id` property — written to hidden field via `<html:hidden property="id"/>`
- `accountAction` — hidden field hardcoded to `"register"`

**JavaScript (security implications):**
- `fnsubmitAccount()`: client-side-only validation. Checks that company name, email, password, and timezone are non-empty, and that password equals confirm password. Calls `swal()` for errors. Submits form `#adminRegActionForm` on pass.
- `fnGoBackHome()`: redirects to `index.jsp` via `location.replace()`.
- No server-side password complexity enforcement is visible in the JSP. Validation is exclusively client-side.

**Test grep result:** No matches for `adminRegister` in `src/test/java/`.

---

**Findings:**

**B02-1 | Severity: HIGH | adminRegister.jsp — Client-side-only password validation, no server-side equivalent tested**
The `fnsubmitAccount()` function is the only enforcement that passwords match and are non-empty. No server-side validation logic is visible in the JSP, and no test exercises the path where a crafted POST bypasses JavaScript. An attacker who submits the form directly (e.g., via curl) can register with an empty or mismatched password if the backing action does not re-validate.

**B02-2 | Severity: HIGH | adminRegister.jsp — No password complexity enforcement anywhere in the view layer**
The password field (`name="pin"`) and confirm-password field (`name="cpassword"`) accept any non-empty string. There is no minimum length, character-class, or pattern check in the JavaScript validation, and no test confirms the action layer enforces complexity. Weak passwords (e.g., a single character) will pass.

**B02-3 | Severity: MEDIUM | adminRegister.jsp — `arrTimezone` null/empty path untested**
`<logic:notEmpty name="arrTimezone">` silently renders an empty dropdown if the attribute is null or empty. No test verifies the controller always populates `arrTimezone` before forwarding to this JSP. A missing attribute produces a timezone dropdown with only the default option, allowing a value of `"0"` to reach the action.

**B02-4 | Severity: MEDIUM | adminRegister.jsp — Struts error/message display completely untested**
`<html:errors/>` and `<html:messages id="accountmsg">` render server-side validation feedback. No test verifies that error or success messages are actually placed into the request by the action, nor that they render correctly.

**B02-5 | Severity: LOW | adminRegister.jsp — `<bean:write name="accountmsg"/>` may render unescaped message content**
`<bean:write>` does not HTML-encode output by default (filter="false" is the Struts 1 default when not specified). If the action places user-controlled content in the action message, it could be rendered unescaped. No test confirms message content is sanitised before placement.

---

### 2. adminReports.jsp

**Path:** `src/main/webapp/html-jsp/adminReports.jsp`

**Purpose:** Reports landing page. Renders links to Incident Report, Session Report, and GPS Report. URL selection for Incident Report and Session Report is conditional on the `isDealer` session attribute.

**Scriptlet blocks:**
```jsp
<%
    String incidentReportUrl = session.getAttribute("isDealer").equals("true")
        ? "dealerIncidentReport.do" : "incidentreport.do";
    String sessionReportUrl = session.getAttribute("isDealer").equals("true")
        ? "dealerSessionReport.do" : "sessionreport.do";
%>
```

**EL / session attribute access:**
- `session.getAttribute("isDealer")` — read directly in scriptlet, result written into href attributes via `<%= incidentReportUrl %>` and `<%= sessionReportUrl %>`.

**JavaScript (security implications):** None present.

**Test grep result:** No matches for `adminReports` in `src/test/java/`.

---

**Findings:**

**B02-6 | Severity: CRITICAL | adminReports.jsp — NullPointerException if `isDealer` session attribute is absent**
`session.getAttribute("isDealer").equals("true")` will throw a `NullPointerException` if `isDealer` has not been set on the session (e.g., unauthenticated request that bypasses the pre-flight filter, expired session, or a session created outside the normal login flow). The NPE propagates as a 500 error with a stack trace, potentially leaking implementation details. No null-guard is present, and no test covers this path.

**B02-7 | Severity: MEDIUM | adminReports.jsp — Session attribute `isDealer` drives URL routing without validation**
The scriptlet trusts the string value of `isDealer` with a plain `.equals("true")` comparison. No test verifies the attribute value is always exactly `"true"` or `"false"` — any other value (e.g., `"True"`, `1`, `Boolean.TRUE` object) silently routes the user to non-dealer URLs. The logic is untested.

**B02-8 | Severity: MEDIUM | adminReports.jsp — Session Report anchor href is hardcoded, ignoring computed URL**
Line 36 hardcodes `href="sessionreport.do"` in the `<h3>` heading link but the image anchor at line 38 correctly uses `<%= sessionReportUrl %>`. A dealer user clicking the heading link is routed to the wrong (non-dealer) endpoint. No test covers this discrepancy.

---

### 3. adminSubscription.jsp

**Path:** `src/main/webapp/html-jsp/adminSubscription.jsp`

**Purpose:** Subscription selection form. Iterates over `arrSubscription` request attribute and renders a multibox checkbox list for selecting subscription options. Submits to `adminsubscription.do`.

**Scriptlet blocks:** None.

**EL / Struts tag attribute access:**
- `arrSubscription` — iterated via `<logic:notEmpty name="arrSubscription"><logic:iterate name="arrSubscription" id="subscriptionRecord">`
- `subscriptionRecord.id` — written to multibox value via `<bean:write property="id" name="subscriptionRecord"/>`
- `subscriptionRecord.name` — written to display label via `<bean:write property="name" name="subscriptionRecord"/>`
- `submsg` — Struts action messages rendered via `<bean:write name="submsg"/>`

**JavaScript (security implications):** None present.

**Test grep result:** No matches for `adminSubscription` in `src/test/java/`.

---

**Findings:**

**B02-9 | Severity: MEDIUM | adminSubscription.jsp — `arrSubscription` null/empty path renders empty form with no user feedback**
When `arrSubscription` is null or empty, `<logic:notEmpty>` renders nothing — only Submit and Reset buttons remain. No message or explanation is shown to the user. No test verifies the action always populates the attribute or that the empty-list UI path is acceptable.

**B02-10 | Severity: MEDIUM | adminSubscription.jsp — `<bean:write property="name">` renders subscription names without explicit HTML encoding**
`<bean:write>` in Struts 1 does not guarantee HTML encoding. If subscription names stored in the database contain `<`, `>`, or `&` characters (or are attacker-influenced), they would be rendered unescaped, creating a stored XSS risk. No test validates output encoding for this field.

**B02-11 | Severity: MEDIUM | adminSubscription.jsp — `<bean:write property="id">` written to multibox value without encoding**
The subscription `id` value is written directly into the multibox form value. If the id is numeric this is low-risk, but no test or type assertion enforces that the id is numeric, and unexpected string content would be submitted to the action unencoded.

**B02-12 | Severity: LOW | adminSubscription.jsp — Struts error and message display untested**
`<html:errors/>` and `<html:messages id="submsg">` are present but no test verifies the action places correct messages into the request under success or error conditions.

---

### 4. adminUnit.jsp

**Path:** `src/main/webapp/html-jsp/adminUnit.jsp`

**Purpose:** "Manage Vehicles" list view. Displays a searchable, paginated table of vehicle records from `arrAdminUnit`. Provides edit (lightbox) and delete (data-attribute-driven AJAX) action links per row.

**Scriptlet blocks:**
```jsp
<%
    String searchUnit = request.getParameter("searchUnit") == null
        ? "" : request.getParameter("searchUnit");
%>
```

**EL / request attribute access:**
- `request.getParameter("searchUnit")` — raw parameter assigned to local variable
- `searchUnit` — written directly into the search input `value` attribute: `value="<%=searchUnit %>"`
- `arrAdminUnit` — iterated via `<logic:notEmpty name="arrAdminUnit"><logic:iterate ...>`
- Per-row: `unitRecord.id`, `unitRecord.name`, `unitRecord.serial_no`, `unitRecord.manu_name`, `unitRecord.type_nm`, `unitRecord.acchours` — written via `<bean:write>`

**JavaScript (security implications):**
- No inline JavaScript; AJAX deletion relies on data-attributes (`data-delete-value`, `data-delete-action`, `data-method-action`) consumed by a shared JavaScript library. The `data-delete-value` is populated with `<bean:write property="id" name="unitRecord"/>`.

**Test grep result:** No matches for `adminUnit` in `src/test/java/`.

---

**Findings:**

**B02-13 | Severity: CRITICAL | adminUnit.jsp — Reflected XSS via `searchUnit` request parameter written unescaped into HTML**
`request.getParameter("searchUnit")` is assigned to a local variable and then output directly into the HTML input `value` attribute as `value="<%=searchUnit %>"`. There is no HTML encoding applied. A crafted URL such as `adminunit.do?searchUnit="><script>alert(1)</script>` would inject arbitrary HTML/JavaScript into the page. This is a textbook reflected XSS vulnerability with no mitigation and no test covering it.

**B02-14 | Severity: MEDIUM | adminUnit.jsp — `arrAdminUnit` null/empty path shows an empty table with no user feedback**
When `arrAdminUnit` is absent or empty, `<logic:notEmpty>` renders no rows. No "no results" message is shown. No test verifies the controller always sets this attribute, nor that the empty-state rendering is intentional.

**B02-15 | Severity: MEDIUM | adminUnit.jsp — `<bean:write>` outputs for `unitRecord.name`, `unitRecord.serial_no`, etc. are unencoded**
Vehicle field values (name, serial number, manufacturer name, type name) are rendered via `<bean:write>` without confirming Struts 1 default encoding behaviour is active. If these fields contain HTML-special characters stored in the database, they may render as markup. No test validates output encoding for any vehicle field.

**B02-16 | Severity: LOW | adminUnit.jsp — Delete action `data-delete-value` exposes internal entity ID in DOM**
The vehicle `id` is emitted into a `data-delete-value` HTML attribute consumed by JavaScript to perform deletion. No test verifies that the shared JS library validates the user's authorisation before sending the delete request, nor that the action re-checks ownership server-side.

---

### 5. adminUser.jsp

**Path:** `src/main/webapp/html-jsp/adminUser.jsp`

**Purpose:** "Manage Users" list view. Displays a searchable table of driver/user records from `arrAdminDriver`. Provides edit (lightbox) and delete (data-attribute AJAX) action links per row. Search submits via GET to `admindriver.do`.

**Scriptlet blocks:**
```jsp
<%
    String searchDriver = request.getParameter("searchDriver") == null
        ? "" : request.getParameter("searchDriver");
%>
```

**EL / request attribute access:**
- `request.getParameter("searchDriver")` — raw parameter assigned to local variable
- `searchDriver` — written directly into search input `value` attribute: `value="<%=searchDriver %>"`
- `arrAdminDriver` — iterated via `<logic:notEmpty name="arrAdminDriver"><logic:iterate ...>`
- Per-row: `driverRecord.id`, `driverRecord.first_name`, `driverRecord.last_name`, `driverRecord.email_addr`, `driverRecord.phone` — written via `<bean:write>`

**JavaScript (security implications):**
- Same data-attribute AJAX pattern as adminUnit.jsp. `data-delete-value` populated with `<bean:write property="id" name="driverRecord"/>`.
- The edit link uses a CSS class `class="driver<bean:write property="id" name="driverRecord"/>"` which writes the driver id directly into the class attribute.

**Test grep result:** No matches for `adminUser` in `src/test/java/`.

---

**Findings:**

**B02-17 | Severity: CRITICAL | adminUser.jsp — Reflected XSS via `searchDriver` request parameter written unescaped into HTML**
Identical pattern to B02-13. `request.getParameter("searchDriver")` is output directly into `value="<%=searchDriver %>"` without HTML encoding. A crafted GET parameter can inject arbitrary content into the page. No test covers this path.

**B02-18 | Severity: MEDIUM | adminUser.jsp — Driver `id` written unencoded into CSS class attribute**
`class="driver<bean:write property="id" name="driverRecord"/>"` injects the driver id directly into the HTML `class` attribute. If the id is ever non-numeric or contains spaces or special characters, this produces malformed HTML. No test validates the format of ids rendered into attributes.

**B02-19 | Severity: MEDIUM | adminUser.jsp — `<bean:write>` outputs for driver fields are unencoded**
`first_name`, `last_name`, `email_addr`, `phone` are output via `<bean:write>` without confirmed encoding. User-controlled PII fields stored with HTML-special characters may render as markup. No test validates output encoding.

**B02-20 | Severity: MEDIUM | adminUser.jsp — `arrAdminDriver` null/empty path renders silent empty table**
When `arrAdminDriver` is absent, no records are displayed and no message informs the user. No test verifies the controller always populates this attribute.

**B02-21 | Severity: LOW | adminUser.jsp — Search form uses GET method, exposing search terms in URL and logs**
The form `method="get"` means search terms appear in browser history, server access logs, and Referer headers. If `searchDriver` contains PII (e.g., partial email or name), it is persisted in logs. No test or policy controls are in place.

---

### 6. apiXml.jsp

**Path:** `src/main/webapp/html-jsp/apiXml.jsp`

**Purpose:** XML API response generator. A scriptlet-heavy JSP that constructs an XML response string based on the `method` request attribute. Handles branches for `API_LOGIN`, `API_VEHICLE`, `API_DRIVER`, `API_ATTACHMENT`, `API_QUESTION`, `API_RESULT` (duplicated), and `API_PDFRPT`. Outputs the result via `out.println(resp)`.

**Scriptlet blocks (full JSP is a single scriptlet):**
```java
response.setContentType("text/xml");
String resp = "";
resp = resp + "<body>";

String method = (String) request.getAttribute("method");
String error = (String) request.getAttribute("error");

if (method.equalsIgnoreCase(RuntimeConf.API_LOGIN)) { ... }
else if (method.equalsIgnoreCase(RuntimeConf.API_VEHICLE)) { ... }
else if (method.equalsIgnoreCase(RuntimeConf.API_DRIVER)) { ... }
else if (method.equalsIgnoreCase(RuntimeConf.API_ATTACHMENT)) { ... }
else if (method.equalsIgnoreCase(RuntimeConf.API_QUESTION)) { ... }
else if (method.equalsIgnoreCase(RuntimeConf.API_RESULT)) { ... }  // DUPLICATE
else if (method.equalsIgnoreCase(RuntimeConf.API_RESULT)) { ... }  // DUPLICATE
else if (method.equalsIgnoreCase(RuntimeConf.API_PDFRPT)) { ... }
```

**EL / request attribute access:**
- `method` — `(String) request.getAttribute("method")` — no null check before `.equalsIgnoreCase()`
- `error` — `(String) request.getAttribute("error")` — null-checked before appending
- `compKey` — `(String) request.getAttribute("compKey")` — null-coalesced to `"0"`
- `arrUnit` — `(ArrayList<UnitBean>) request.getAttribute("arrUnit")` — no null check before `.size()` / `.get(i)`
- `arrDriver` — `(ArrayList<DriverBean>) request.getAttribute("arrDriver")` — no null check
- `arrAtt` — `(ArrayList<AttachmentBean>) request.getAttribute("arrAtt")` — no null check
- `arrQues` — `(ArrayList<QuestionBean>) request.getAttribute("arrQues")` — no null check
- `resultstatus` — null-coalesced to `false`
- `emailstatus` — null-coalesced to `false`

**JavaScript (security implications):** None — this JSP produces XML, not HTML.

**Test grep result:** No matches for `apiXml` in `src/test/java/`.

---

**Findings:**

**B02-22 | Severity: CRITICAL | apiXml.jsp — NullPointerException if `method` attribute is null**
`method.equalsIgnoreCase(...)` is called without a null check on `method`. If the request attribute `method` is not set (e.g., the JSP is accessed directly rather than through the action), a `NullPointerException` is thrown, producing a 500 error. No test covers this null path.

**B02-23 | Severity: CRITICAL | apiXml.jsp — NullPointerException on array attributes for `API_VEHICLE`, `API_DRIVER`, `API_ATTACHMENT`, `API_QUESTION` branches**
All four collection branches (lines 21, 29, 38, 48) cast the request attribute and immediately call `.size()` or iterate without null-checking the collection first. If the action fails to set the attribute, a NullPointerException is thrown. No test covers missing-attribute paths for any branch.

**B02-24 | Severity: CRITICAL | apiXml.jsp — XML injection via unescaped data written into XML output**
In the `API_VEHICLE` branch, `unitBean.getName()` is concatenated directly into XML: `"<name>" + unitBean.getName() + "</name>"`. In the `API_DRIVER` branch, `driverBean.getFirst_name()` and `driverBean.getLast_name()` are similarly concatenated. If these fields contain `<`, `>`, `&`, or `"` characters, the resulting XML is malformed or can be exploited to inject arbitrary XML nodes. No test covers data containing XML-special characters for these branches.

**B02-25 | Severity: HIGH | apiXml.jsp — Incomplete XML encoding in `API_QUESTION` branch uses if/else-if chain, leaving multiple characters unescaped**
The `API_QUESTION` branch attempts to escape XML special characters in `content` using a chain of `if / else if` conditions (lines 53-70). Because the chain uses `else if`, only the first matching special character is escaped per string — a string containing both `&` and `<` will have `&` escaped but `<` left raw. Furthermore, the `>` branch on line 68-71 contains a copy-paste bug: it calls `content.replace("<","&gt;")` instead of `content.replace(">","&gt;")`. No test exercises multi-special-character content or the `>` escape path.

**B02-26 | Severity: HIGH | apiXml.jsp — `API_RESULT` branch is duplicated (dead code)**
Lines 82-88 are an exact duplicate of lines 75-81, both matching `method.equalsIgnoreCase(RuntimeConf.API_RESULT)`. The second occurrence is unreachable dead code. This likely masks a missing branch for another method constant (e.g., `API_INCIDENT`). No test verifies the correct method constants are handled.

**B02-27 | Severity: MEDIUM | apiXml.jsp — `error` attribute written unescaped into XML**
`resp = resp + "<rec><error>" + error + "</error></rec>"` (line 97) appends the error string without XML encoding. If the error message contains XML-special characters, the output is malformed. No test covers this path.

**B02-28 | Severity: MEDIUM | apiXml.jsp — Response content type set to `text/xml` but no XML declaration is emitted**
The JSP sets `response.setContentType("text/xml")` but does not emit an XML declaration (`<?xml version="1.0" encoding="UTF-8"?>`). The encoding of the response depends on the container default. No test validates well-formed XML output.

**B02-29 | Severity: LOW | apiXml.jsp — `compKey` silently defaults to `"0"` on null**
For `API_LOGIN`, if `compKey` is null the response returns `<compKey>0</compKey>`. A caller cannot distinguish a legitimate key of `"0"` from a missing/failed key. No test verifies error signalling for the login branch.

---

### 7. dealer/adminSubcompanyEdit.jsp

**Path:** `src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`

**Purpose:** Modal/lightbox form for editing an existing subcompany (dealer sub-account). Iterates over `companyRecord` (a collection of `CompanyBean`) and renders editable fields for company name, timezone, address, first/last name, contact number, email, password, and confirm password. Submits AJAX to `adminRegister` action via `styleClass="ajax_mode_c"`. Also includes a password strength meter reference.

**Scriptlet blocks:** None.

**EL / Struts tag attribute access:**
- `companyRecord` — iterated via `<logic:notEmpty name="companyRecord"><logic:iterate name="companyRecord" id="company" type="com.bean.CompanyBean">`
- `arrTimezone` — used in `<html:options collection="arrTimezone" property="id" labelProperty="name"/>`
- `company.name`, `company.timezone`, `company.address`, `company.contact_fname`, `company.contact_lname`, `company.contact_no`, `company.email` — all bound via `<html:text>`, `<html:textarea>`, `<html:select>`
- `accountAction` — hardcoded hidden field `value="add"` (note: this is an edit form, but `accountAction` is set to `"add"`, which may be a bug)

**JavaScript (security implications):**
- `fnsubmitAccount()`: identical client-side-only validation as adminRegister.jsp (B02-1/B02-2 pattern).
- `jQuery(document).ready(function($) { $('#pword').strength(); })` — references `#pword` but no element with `id="pword"` exists in the form. The password input has `name="pin"` with no id, so the strength meter is silently broken.

**Test grep result:** No matches for `adminSubcompany` or `adminSubcompanyEdit` in `src/test/java/`.

---

**Findings:**

**B02-30 | Severity: HIGH | adminSubcompanyEdit.jsp — `accountAction` hidden field hardcoded to `"add"` in an edit form**
`<html:hidden property="accountAction" value="add"/>` is present in what is clearly an edit context (the form iterates `companyRecord` which is populated from an existing company). If the backing action uses `accountAction` to distinguish create vs. update, this field will always signal a create operation, potentially creating duplicate records or silently failing. No test verifies the correct action discriminator is submitted.

**B02-31 | Severity: HIGH | adminSubcompanyEdit.jsp — Client-side-only password validation, identical to B02-1**
The `fnsubmitAccount()` function provides the only password match and non-empty enforcement. A direct POST bypasses it. No test covers the edit path.

**B02-32 | Severity: MEDIUM | adminSubcompanyEdit.jsp — Password strength meter targets non-existent element ID**
`$('#pword').strength()` is called but no element with `id="pword"` exists in the rendered HTML. The password field uses `name="pin"` with no `id`. The strength meter is silently inoperative. No test verifies UI security controls are actually attached to their intended elements.

**B02-33 | Severity: MEDIUM | adminSubcompanyEdit.jsp — `companyRecord` null/empty renders blank modal body**
If `companyRecord` is null or an empty collection, `<logic:notEmpty>` renders nothing inside the modal, and the user sees an empty form panel. No test verifies the controller always populates this attribute for the edit path.

**B02-34 | Severity: MEDIUM | adminSubcompanyEdit.jsp — `arrTimezone` null renders an empty timezone dropdown**
`<html:options collection="arrTimezone" .../>` will throw a `JspException` or render nothing if `arrTimezone` is null. No test verifies this attribute is always present.

**B02-35 | Severity: LOW | adminSubcompanyEdit.jsp — No CSRF protection on the AJAX edit form submission**
The form submits via `ajax_mode_c` class with no visible CSRF token. No test verifies that the backing action enforces a CSRF token or same-origin check.

---

### 8. dealer/impactReport.jsp

**Path:** `src/main/webapp/html-jsp/dealer/impactReport.jsp`

**Purpose:** Dealer Impact Report view. Renders a filterable table of impact events grouped by vehicle. Filters include manufacturer, type, impact level, start date, and end date. Table rows include manufacturer, unit name, company name, driver name, impact datetime, and a coloured impact level indicator with g-force value.

**Scriptlet blocks:**
```java
// Top-level scriptlet:
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");

// Inside <logic:equal value="0"> block:
<td rowspan="<%= impactGroup.getEntries().size() %>">
<td rowspan="<%= impactGroup.getEntries().size() %>">

// Inline scriptlets for CSS colour and g-force:
<span style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;">
<%= String.format(" (%.1fg)", impactEntry.getGForce()) %>

// JavaScript date picker scriptlets:
<% if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("start_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
<% if (request.getParameter("end_date") != null) { %>
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("end_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
setupDatePicker('#start_date', '<%= dateFormat %>', start_date);
setupDatePicker('#end_date', '<%= dateFormat %>', end_date);
```

**EL / session and request attribute access:**
- `session.getAttribute("sessDateFormat")` — cast to String, methods called on it directly
- `impactReport` — iterated via `<logic:iterate id="impactGroup" name="impactReport" property="groups">`
- `impactGroup.manufacturer`, `impactGroup.unitName`, `impactGroup.entries` — read via `<bean:write>` and scriptlet
- `impactEntry.companyName`, `impactEntry.driverName`, `impactEntry.impactDateTime` — written via `<bean:write>`
- `impactEntry.getImpactLevelCSSColor()` — method called directly in scriptlet, output written to `style` attribute
- `impactEntry.getGForce()` — method called directly in scriptlet, formatted and output
- `request.getParameter("start_date")` and `request.getParameter("end_date")` — passed to `DateUtil.stringToIsoNoTimezone()`, result written into JavaScript `new Date("...")` call

**JavaScript (security implications):**
- `DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), ...)` result is emitted directly into a JavaScript string literal `new Date("...<%=...%>...")`. If the date utility does not sanitise the input, a crafted `start_date` parameter could close the string literal and inject JavaScript (DOM-based XSS).
- `dateFormat` derived from `sessDateFormat` is written into `setupDatePicker(...)` call. If session attribute contains JavaScript-special characters, it could break out of the string context.

**Test grep result:** No matches for `impactReport` in `src/test/java/`.

---

**Findings:**

**B02-36 | Severity: CRITICAL | impactReport.jsp — NullPointerException if `sessDateFormat` session attribute is null**
`((String) session.getAttribute("sessDateFormat")).replaceAll(...)` is called at the top of the JSP without a null check. If `sessDateFormat` is not set (unauthenticated request, session expiry, or missing initialisation), an NPE is thrown. No test covers this path.

**B02-37 | Severity: HIGH | impactReport.jsp — Potential DOM-based XSS via `start_date`/`end_date` parameters written into JavaScript string literal**
`request.getParameter("start_date")` is passed to `DateUtil.stringToIsoNoTimezone()` and the result is written directly into a JavaScript `new Date("...")` constructor without JavaScript encoding: `start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(...) %>");`. If `stringToIsoNoTimezone()` returns or passes through attacker-controlled content (e.g., malformed date triggering a fallback that echoes input), an attacker could inject `"); alert(1); //` to break out of the string and execute JavaScript. No test verifies the sanitisation behaviour of `DateUtil.stringToIsoNoTimezone()` under malicious input.

**B02-38 | Severity: HIGH | impactReport.jsp — `impactEntry.getImpactLevelCSSColor()` output written unescaped into CSS style attribute**
`style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;"` writes the method's return value directly into an HTML style attribute without encoding. If `getImpactLevelCSSColor()` can return attacker-influenced content or unexpected values, CSS injection is possible. No test validates the bounded set of values returned.

**B02-39 | Severity: MEDIUM | impactReport.jsp — `impactReport` attribute null or missing causes `<logic:iterate>` to throw or silently render nothing**
If the action does not populate `impactReport` in the request, `<logic:iterate name="impactReport" property="groups">` will throw a `JspException` (attribute not found) or render no rows depending on Struts version behaviour. No test verifies the attribute is always present.

**B02-40 | Severity: MEDIUM | impactReport.jsp — `<bean:write>` on `companyName`, `driverName`, `impactDateTime`, `manufacturer`, `unitName` lacks confirmed encoding**
These fields are rendered without explicit `filter="true"` and no test validates that data containing HTML-special characters is correctly encoded in the report table.

**B02-41 | Severity: LOW | impactReport.jsp — `dateFormat` written into JavaScript without encoding**
`'<%= dateFormat %>'` is written into a JavaScript string literal. The `dateFormat` value is derived from `sessDateFormat` via regex substitution. If `sessDateFormat` contains a single-quote, it would break the JavaScript string. No test validates the format string is JavaScript-safe.

---

### 9. dealer/incidentReport.jsp

**Path:** `src/main/webapp/html-jsp/dealer/incidentReport.jsp`

**Purpose:** Dealer Incident Report view. Renders a filterable table of incident entries. Filters include manufacturer, type, start date, and end date. Table columns include unit name, manufacture, company, driver, description, event time, near miss (yes/no), incident (yes/no), injury (yes/no), injury type, location, witness, signature link, and image link.

**Scriptlet blocks:**
```java
// Top-level scriptlet:
String dateFormat = ((String) session.getAttribute("sessDateFormat"))
    .replaceAll("yyyy", "yy").replaceAll("M", "m");

// JSP declaration:
<%!
    String getYesNoMessageKey(boolean value) {
        return value ? "clst.answerY" : "clst.answerN";
    }
%>

// Within table rows:
<bean:message key="<%= getYesNoMessageKey(incidentEntry.getNear_miss()) %>"/>
<bean:message key="<%= getYesNoMessageKey(incidentEntry.getIncident()) %>"/>
<bean:message key="<%= getYesNoMessageKey(incidentEntry.getInjury()) %>"/>

// JavaScript date picker scriptlets (identical pattern to impactReport.jsp):
<% if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("start_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
<% if (request.getParameter("end_date") != null) { %>
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("end_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
setupDatePicker('#start_date', '<%= dateFormat %>', start_date);
setupDatePicker('#end_date', '<%= dateFormat %>', end_date);
```

**EL / session and request attribute access:**
- `session.getAttribute("sessDateFormat")` — cast and method-called directly, no null check
- `incidentReport` — iterated via `<logic:iterate name="incidentReport" property="entries">`
- `incidentEntry.unitName`, `incidentEntry.manufacture`, `incidentEntry.companyName`, `incidentEntry.driverName`, `incidentEntry.description`, `incidentEntry.event_time`, `incidentEntry.injureType`, `incidentEntry.location`, `incidentEntry.witness` — all rendered via `<bean:write>`
- `incidentEntry.getNear_miss()`, `incidentEntry.getIncident()`, `incidentEntry.getInjury()` — called in scriptlet expression passed to `<bean:message key=...>`
- `incidentEntry.signature`, `incidentEntry.image` — written directly into `href` attributes via `<bean:write>`

**JavaScript (security implications):**
- Same `start_date`/`end_date` DOM-based XSS risk as B02-37.
- `incidentEntry.signature` and `incidentEntry.image` are written into `href` attributes. If these fields contain `javascript:` URIs, clicking the link executes JavaScript.

**Test grep result:** No matches for `incidentReport` in `src/test/java/`.

---

**Findings:**

**B02-42 | Severity: CRITICAL | incidentReport.jsp — NullPointerException if `sessDateFormat` session attribute is null**
Identical pattern to B02-36. `((String) session.getAttribute("sessDateFormat")).replaceAll(...)` without null check. No test covers this.

**B02-43 | Severity: HIGH | incidentReport.jsp — Potential DOM-based XSS via `start_date`/`end_date` parameters in JavaScript**
Identical pattern to B02-37. `DateUtil.stringToIsoNoTimezone()` result written directly into a JavaScript `new Date("...")` literal without JavaScript encoding. No test covers malicious date input.

**B02-44 | Severity: HIGH | incidentReport.jsp — `incidentEntry.signature` and `incidentEntry.image` written unvalidated into `href` attributes**
`<bean:write name="incidentEntry" property="signature"/>` and `<bean:write name="incidentEntry" property="image"/>` are written directly into anchor `href` attributes. If these database fields contain a `javascript:` URI, clicking the view-signature or view-image link will execute JavaScript in the browser (stored XSS via `javascript:` URI). No test validates that these fields are constrained to `http://` or `https://` URLs.

**B02-45 | Severity: HIGH | incidentReport.jsp — `incidentEntry.description` and other free-text fields rendered unescaped in table**
`description`, `location`, `witness`, `injureType` are user-supplied free-text fields output via `<bean:write>` without confirmed HTML encoding. If any of these fields contain HTML-special characters stored by a malicious user, they render as markup (stored XSS). No test validates encoding of free-text incident fields.

**B02-46 | Severity: MEDIUM | incidentReport.jsp — `incidentReport` attribute null/missing causes `<logic:iterate>` to throw or render nothing**
Same pattern as B02-39. No test verifies the action always populates this attribute before forwarding.

**B02-47 | Severity: LOW | incidentReport.jsp — `getYesNoMessageKey()` is a JSP declaration method with no unit test**
The `<%! ... %>` declaration block defines `getYesNoMessageKey(boolean)`. This trivial method is untested in isolation. While its logic is simple, the pattern of placing utility logic in JSP declarations rather than a tested utility class means any change to this logic is invisible to the test suite.

---

## Summary Table

| Finding | JSP File | Severity | Category |
|---------|----------|----------|----------|
| B02-1 | adminRegister.jsp | HIGH | Missing server-side validation |
| B02-2 | adminRegister.jsp | HIGH | Weak password policy |
| B02-3 | adminRegister.jsp | MEDIUM | Missing null/empty attribute path |
| B02-4 | adminRegister.jsp | MEDIUM | Untested error/message display |
| B02-5 | adminRegister.jsp | LOW | Potential unescaped message output |
| B02-6 | adminReports.jsp | CRITICAL | NPE on null session attribute |
| B02-7 | adminReports.jsp | MEDIUM | Unvalidated session attribute drives routing |
| B02-8 | adminReports.jsp | MEDIUM | Hardcoded URL ignores dealer flag (wrong route for dealers) |
| B02-9 | adminSubscription.jsp | MEDIUM | Empty subscription list — no user feedback |
| B02-10 | adminSubscription.jsp | MEDIUM | Stored XSS risk — `name` field unencoded |
| B02-11 | adminSubscription.jsp | MEDIUM | Unencoded `id` in multibox value |
| B02-12 | adminSubscription.jsp | LOW | Struts error/message display untested |
| B02-13 | adminUnit.jsp | CRITICAL | Reflected XSS — `searchUnit` parameter unescaped |
| B02-14 | adminUnit.jsp | MEDIUM | Empty unit list — no user feedback |
| B02-15 | adminUnit.jsp | MEDIUM | Vehicle fields potentially unescaped |
| B02-16 | adminUnit.jsp | LOW | Internal entity ID exposed in DOM |
| B02-17 | adminUser.jsp | CRITICAL | Reflected XSS — `searchDriver` parameter unescaped |
| B02-18 | adminUser.jsp | MEDIUM | Driver id injected into CSS class attribute |
| B02-19 | adminUser.jsp | MEDIUM | Driver PII fields potentially unescaped |
| B02-20 | adminUser.jsp | MEDIUM | Empty driver list — no user feedback |
| B02-21 | adminUser.jsp | LOW | GET form exposes PII in URL/logs |
| B02-22 | apiXml.jsp | CRITICAL | NPE on null `method` attribute |
| B02-23 | apiXml.jsp | CRITICAL | NPE on null collection attributes |
| B02-24 | apiXml.jsp | CRITICAL | XML injection via unescaped field values |
| B02-25 | apiXml.jsp | HIGH | Broken XML encoding — if/else-if chain, `>` escape bug |
| B02-26 | apiXml.jsp | HIGH | Duplicate `API_RESULT` branch — dead code, missing handler |
| B02-27 | apiXml.jsp | MEDIUM | `error` attribute unescaped in XML output |
| B02-28 | apiXml.jsp | MEDIUM | No XML declaration emitted |
| B02-29 | apiXml.jsp | LOW | `compKey` silent default `"0"` masks error |
| B02-30 | adminSubcompanyEdit.jsp | HIGH | `accountAction` hardcoded `"add"` in edit form |
| B02-31 | adminSubcompanyEdit.jsp | HIGH | Client-side-only password validation |
| B02-32 | adminSubcompanyEdit.jsp | MEDIUM | Password strength meter targets non-existent element |
| B02-33 | adminSubcompanyEdit.jsp | MEDIUM | `companyRecord` null/empty renders blank modal |
| B02-34 | adminSubcompanyEdit.jsp | MEDIUM | `arrTimezone` null — empty/broken timezone dropdown |
| B02-35 | adminSubcompanyEdit.jsp | LOW | No CSRF token on AJAX edit form |
| B02-36 | impactReport.jsp | CRITICAL | NPE on null `sessDateFormat` session attribute |
| B02-37 | impactReport.jsp | HIGH | DOM-based XSS via date parameter in JavaScript |
| B02-38 | impactReport.jsp | HIGH | CSS injection via `getImpactLevelCSSColor()` unescaped |
| B02-39 | impactReport.jsp | MEDIUM | `impactReport` attribute null/missing |
| B02-40 | impactReport.jsp | MEDIUM | Report fields potentially unescaped in table |
| B02-41 | impactReport.jsp | LOW | `dateFormat` written unencoded into JavaScript |
| B02-42 | incidentReport.jsp | CRITICAL | NPE on null `sessDateFormat` session attribute |
| B02-43 | incidentReport.jsp | HIGH | DOM-based XSS via date parameter in JavaScript |
| B02-44 | incidentReport.jsp | HIGH | Stored XSS via `javascript:` URI in signature/image href |
| B02-45 | incidentReport.jsp | HIGH | Stored XSS — free-text incident fields unescaped |
| B02-46 | incidentReport.jsp | MEDIUM | `incidentReport` attribute null/missing |
| B02-47 | incidentReport.jsp | LOW | Utility method in JSP declaration — untestable |

### Severity Totals

| Severity | Count |
|----------|-------|
| CRITICAL | 8 |
| HIGH | 13 |
| MEDIUM | 18 |
| LOW | 8 |
| **Total** | **47** |

---

## Coverage Gap Assessment

**Zero test coverage exists for all nine JSP files.** The four existing test files in `src/test/java/` cover only calibration business logic (`UnitCalibrationImpactFilterTest`, `UnitCalibrationTest`, `UnitCalibratorTest`) and a utility (`ImpactUtilTest`). None of these tests exercise any JSP rendering, request attribute population, session attribute handling, or view-layer output encoding.

### Critical untested paths requiring immediate attention:

1. **Null session attribute guards** — `adminReports.jsp`, `impactReport.jsp`, `incidentReport.jsp` all dereference session attributes without null checks, causing NPEs on unauthenticated or session-expired requests.
2. **Reflected XSS** — `adminUnit.jsp` (`searchUnit`) and `adminUser.jsp` (`searchDriver`) write raw request parameters into HTML without encoding.
3. **XML injection** — `apiXml.jsp` concatenates bean field values directly into XML output strings with no entity encoding across all branches.
4. **Stored XSS** — `incidentReport.jsp` writes `signature` and `image` URLs directly into `href` attributes without `javascript:` URI validation.
5. **DOM-based XSS** — `impactReport.jsp` and `incidentReport.jsp` write `DateUtil`-processed request parameters directly into JavaScript string literals.
6. **Logic bug** — `apiXml.jsp` has a duplicate `API_RESULT` branch making one handler permanently unreachable, and a `>` character escaping bug in the `API_QUESTION` branch.
7. **Hardcoded action discriminator** — `adminSubcompanyEdit.jsp` always submits `accountAction=add` even in edit context.
