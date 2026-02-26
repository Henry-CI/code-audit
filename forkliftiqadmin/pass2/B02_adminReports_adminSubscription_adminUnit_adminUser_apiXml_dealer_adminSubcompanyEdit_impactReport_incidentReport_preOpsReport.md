# Pass 2 Audit Report — JSP View Layer
**Audit ID:** B02
**Date:** 2026-02-26
**Auditor:** Agent B02
**Scope:** Test-coverage audit of nine JSP view files; no corresponding test files exist in this project.

---

## 1. Reading Evidence

### 1.1 `adminReports.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminReports.jsp`
**Purpose:** Navigation hub that renders three report-type tiles (Incident Report, Session Report, GPS Report). The page is reached via `adminmenu.do?action=reports`.

**Scriptlets:**

| Lines | Content |
|-------|---------|
| 3–6 | Reads `session.getAttribute("isDealer")` without null-check; applies `.equals("true")` directly; computes `incidentReportUrl` and `sessionReportUrl` as ternary expressions outputting either dealer or non-dealer `.do` paths. |

**EL expressions / session variables accessed:**
- `session.getAttribute("isDealer")` — raw Java scriptlet, line 4–5.

**Forms and action URLs:**
- No `<form>` elements; navigation only.
- Output of `incidentReportUrl` injected directly into `href` attributes at lines 26, 29, 38.
- Hardcoded `href` values: `sessionreport.do` (line 36), `gpsreport.do` (lines 45, 47).

---

### 1.2 `adminSubscription.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminSubscription.jsp`
**Purpose:** Displays a list of subscriptions as checkboxes and allows the user to update selections. Reached via `adminmenu.do?action=subscription` (noted as "Not used" in `AdminMenuAction`).

**Scriptlets:** None.

**EL expressions / Struts tag attributes accessed:**
- `arrSubscription` — request attribute iterated via `<logic:iterate>`.
- Properties accessed per record: `id`, `name` (via `<bean:write>`).

**Forms and action URLs:**
- `<html:form method="post" action="adminsubscription.do">` (line 7).
- Submit button (line 28); Reset button (line 30).

---

### 1.3 `adminUnit.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminUnit.jsp`
**Purpose:** Manage Vehicles list page. Displays a searchable table of vehicles with edit/delete action links.

**Scriptlets:**

| Lines | Content |
|-------|---------|
| 3–5 | Reads `request.getParameter("searchUnit")`, defaulting to `""` if null; stores in `searchUnit`. |
| 23 | `<%= searchUnit %>` — raw request parameter reflected into an HTML input `value` attribute. |

**EL expressions / attributes accessed:**
- `arrAdminUnit` — request attribute (`logic:iterate`).
- Per record: `id`, `name`, `serial_no`, `manu_name`, `type_nm`, `acchours` via `<bean:write>`.

**Forms and action URLs:**
- `<form method="post" action="adminunit.do" name="adminUnitForm" id="adminUnitForm">` (line 18).
- Hidden fields: `equipId`, `action` (lines 82–83).

---

### 1.4 `adminUser.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/adminUser.jsp`
**Purpose:** Manage Users list page. Displays a searchable table of users with edit/delete action links.

**Scriptlets:**

| Lines | Content |
|-------|---------|
| 3–5 | Reads `request.getParameter("searchDriver")`, defaulting to `""` if null; stores in `searchDriver`. |
| 25 | `<%= searchDriver %>` — raw request parameter reflected into an HTML input `value` attribute. |

**EL expressions / attributes accessed:**
- `arrAdminDriver` — request attribute (`logic:iterate`).
- Per record: `id`, `first_name`, `last_name`, `email_addr`, `phone` via `<bean:write>`.

**Forms and action URLs:**
- `<form method="get" action="admindriver.do">` (line 20) — uses GET method, causing search term to appear in URL and browser history.
- Hidden fields: `driverId`, `action` (lines 91–92).

---

### 1.5 `apiXml.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/apiXml.jsp`
**Purpose:** XML API response renderer. Reads `method` and `error` from request attributes and serialises appropriate bean collections into an XML string written directly to the response output stream.

**Scriptlets:** Entire file is one large scriptlet (lines 6–103). Key logic:

| Lines | Logic |
|-------|-------|
| 7 | Sets content type to `text/xml` |
| 11–12 | Reads `method` and `error` from request attributes; `method` called with `.equalsIgnoreCase()` without null-check. |
| 13–16 | `API_LOGIN`: reads `compKey` from request attributes; appends to XML string without XML-escaping. |
| 18–25 | `API_VEHICLE`: iterates `arrUnit`, appends `id` and `name` to XML without escaping. |
| 27–35 | `API_DRIVER`: iterates `arrDriver`, appends `id`, first name, last name to XML without escaping. |
| 36–44 | `API_ATTACHMENT`: iterates `arrAtt`, appends `id` and `name` without escaping. |
| 46–74 | `API_QUESTION`: partial XML escaping — uses `else if` chain; only the **first** matching character is escaped in any given string. |
| 75–88 | `API_RESULT`: block appears **twice** (lines 75–81 and 82–88) — exact duplicate dead code. |
| 89–93 | `API_PDFRPT`: reads `emailstatus` from request; no escaping. |
| 95–98 | Error block: `error` value appended without escaping. |
| 102 | `out.println(resp)` — entire XML string written at once. |

**EL expressions / request attributes accessed:**
- `request.getAttribute("method")` (line 11) — no null-check.
- `request.getAttribute("error")` (line 12).
- `request.getAttribute("compKey")` (line 15).
- `request.getAttribute("arrUnit")`, `arrDriver`, `arrAtt`, `arrQues` — cast directly without null-check.
- `request.getAttribute("resultstatus")`, `emailstatus` (lines 77, 91).

**Forms and action URLs:** None (response-only page).

---

### 1.6 `dealer/adminSubcompanyEdit.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/adminSubcompanyEdit.jsp`
**Purpose:** Modal form for creating/editing a dealer sub-company account. Uses `AdminRegisterAction`.

**Scriptlets:** None in JSP body.

**JavaScript validation (inline script, lines 137–175):**
- `fnsubmitAccount()` function validates company name, email, password, confirm-password match, and timezone — **client-side only**.

**EL expressions / attributes accessed:**
- `companyRecord` — request attribute iterated via `<logic:iterate>`.
- Per company record: `name`, `timezone`, `address`, `contact_fname`, `contact_lname`, `contact_no`, `email` via `<html:text>` / `<html:textarea>`.
- `arrTimezone` — used as `<html:options collection>` (must be in scope from calling action).
- `<html:hidden property="accountAction" value="add" />` (line 133) — hardcodes action to `"add"`.

**Forms and action URLs:**
- `<html:form method="post" action="adminRegister" styleClass="ajax_mode_c" styleId="adminCompActionForm">` (line 4).
- Note: `adminRegister` (without `.do`) — Struts resolves this, but inconsistent with other forms.
- Password field (`name="pin"`) and confirm-password field (`name="cpassword"`) are plain `<input type="password">` elements outside Struts tag library, so values are not bound through ActionForm.

---

### 1.7 `dealer/impactReport.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/impactReport.jsp`
**Purpose:** Dealer-scoped Impact Report page showing forklift impact events. Filtered by manufacturer, type, impact level, and date range.

**Scriptlets:**

| Lines | Content |
|-------|---------|
| 4–6 | Reads `session.getAttribute("sessDateFormat")` — no null-check; calls `.replaceAll()` directly. |
| 88–89 | `<%= impactGroup.getEntries().size() %>` — JSP scriptlet inside loop building `rowspan` attribute value. |
| 99 | `<%= impactEntry.getImpactLevelCSSColor() %>` — scriptlet injecting CSS color string into `style` attribute. |
| 102 | `<%= String.format(" (%.1fg)", impactEntry.getGForce()) %>` — numeric value formatted and injected into HTML. |
| 117–119 | `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), ...) %>` — raw request parameter fed to date parser and injected into JavaScript `new Date(...)` string. |
| 121–123 | Same pattern for `end_date`. |
| 125–126 | `<%= dateFormat %>` — session-derived format string injected into JavaScript `setupDatePicker` call. |

**EL expressions / session variables accessed:**
- `session.getAttribute("sessDateFormat")` (line 5).
- `request.getAttribute("impactReport")` — iterated via `<logic:iterate>` with `name="impactReport"`.

**Forms and action URLs:**
- `<html:form action="dealerImpactReport.do" method="POST" styleClass="checklist_form">` (line 22).

---

### 1.8 `dealer/incidentReport.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/incidentReport.jsp`
**Purpose:** Dealer-scoped Incident Report page showing near-miss and incident events.

**Scriptlets:**

| Lines | Content |
|-------|---------|
| 4–6 | `session.getAttribute("sessDateFormat")` — no null-check; `.replaceAll()` called directly. |
| 7–11 | JSP declaration (`<%! %>`) defines `getYesNoMessageKey(boolean value)` — view-layer helper method. |
| 107–109 | `<%= getYesNoMessageKey(incidentEntry.getNear_miss()) %>` etc. — helper called inside `<bean:message key="...">` attribute — dynamic message key lookup inside the view. |
| 148–150 | `request.getParameter("start_date")` fed to `DateUtil.stringToIsoNoTimezone` and injected into JavaScript `new Date(...)`. |
| 152–154 | Same for `end_date`. |
| 156 | `<%= dateFormat %>` injected into JavaScript `setupDatePicker` call. |

**EL expressions / session variables accessed:**
- `session.getAttribute("sessDateFormat")` (line 5).
- `request.getAttribute("incidentReport")` — iterated via `<logic:iterate>`.

**Forms and action URLs:**
- `<html:form action="dealerIncidentReport.do" method="POST" styleClass="checklist_form">` (line 27).

---

### 1.9 `dealer/preOpsReport.jsp`
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/preOpsReport.jsp`
**Purpose:** Dealer-scoped Pre-Ops (pre-operation checklist) Report page.

**Scriptlets:**

| Lines | Content |
|-------|---------|
| 4–6 | `session.getAttribute("sessDateFormat")` — no null-check; `.replaceAll()` called directly. |
| 109–111 | `request.getParameter("start_date")` fed to `DateUtil.stringToIsoNoTimezone` and injected into JavaScript `new Date(...)`. |
| 113–115 | Same for `end_date`. |
| 117–118 | `<%= dateFormat %>` injected into JavaScript `setupDatePicker` call. |

**EL expressions / session variables accessed:**
- `session.getAttribute("sessDateFormat")` (line 5).
- `request.getAttribute("preOpsReport")` — iterated via `<logic:iterate>`.

**Forms and action URLs:**
- `<html:form action="dealerPreOpsReport.do" method="POST" styleClass="checklist_form">` (line 22).
- Print button: `onclick="window.print(); return false;"` (line 54) — client-side only.

---

## 2. Test Coverage Search

**Test directory searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Test files present:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Result:** Zero test files reference any of the nine audited JSP files, their containing action classes (`AdminMenuAction`, `AdminUnitAction`, `AppAPIAction`, `AdminRegisterAction`, `DealerImpactReportAction`, `DealerIncidentReportAction`, `DealerPreOpsReportAction`), their form beans, or their session/request attribute names (`isDealer`, `sessDateFormat`, `searchUnit`, `searchDriver`, `arrSubscription`, `arrAdminUnit`, `arrAdminDriver`, `impactReport`, `incidentReport`, `preOpsReport`, `compKey`).

**Coverage: 0 % across all nine files.**

---

## 3. Findings

---

### B02-1 — CRITICAL: Reflected XSS via `searchUnit` Parameter in `adminUnit.jsp`

**File:** `adminUnit.jsp`, line 23
**Severity:** CRITICAL

```jsp
<input type="text" name="searchUnit" class="form-control input-lg" placeholder="Search"
       value="<%=searchUnit %>"/>
```

`searchUnit` is read directly from `request.getParameter("searchUnit")` (line 4) and emitted unescaped into an HTML attribute. A crafted URL such as:

```
adminunit.do?searchUnit="><script>alert(1)</script>
```

will close the `value` attribute and inject arbitrary JavaScript into the page. The `PreFlightActionServlet` only checks for session existence, not parameter content. No HTML-encoding is applied.

---

### B02-2 — CRITICAL: Reflected XSS via `searchDriver` Parameter in `adminUser.jsp`

**File:** `adminUser.jsp`, line 25
**Severity:** CRITICAL

```jsp
<input type="text" name="searchDriver" class="form-control input-lg" placeholder="Search"
       value="<%=searchDriver %>"/>
```

Identical pattern to B02-1. `searchDriver` is copied verbatim from `request.getParameter("searchDriver")` and reflected unescaped into an HTML attribute value. The form uses `method="get"`, making this payload directly constructible and shareable as a URL.

---

### B02-3 — CRITICAL: JavaScript Injection via `start_date` / `end_date` Parameters in `impactReport.jsp`, `incidentReport.jsp`, `preOpsReport.jsp`

**Files:**
- `dealer/impactReport.jsp`, lines 117–123
- `dealer/incidentReport.jsp`, lines 148–154
- `dealer/preOpsReport.jsp`, lines 109–115
**Severity:** CRITICAL

```jsp
<% if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
```

The raw request parameter `start_date` (and `end_date`) is passed to `DateUtil.stringToIsoNoTimezone` and the result is injected without escaping into an inline `<script>` block inside a JavaScript string literal. If `stringToIsoNoTimezone` propagates unexpected characters or throws and is caught upstream, or if a malformed date causes a fallback string to be returned, an attacker controlling the parameter can break out of the JavaScript string and execute arbitrary code. Even if the parser throws a `NullPointerException` on a badly formatted date, the exception propagates up the JSP rendering chain. Regardless of the date-parsing outcome, the injection vector is present because the parameter value is user-controlled and reaches JavaScript context without sanitization.

---

### B02-4 — CRITICAL: XML Injection / Stored Data Injection in `apiXml.jsp`

**File:** `apiXml.jsp`, lines 13–98
**Severity:** CRITICAL

Entity names, driver names, attachment names, and error codes are concatenated directly into an XML string without encoding:

```java
resp=resp+"<rec><id>"+unitBean.getId()+"</id><name>"+ unitBean.getName()+"</name></rec>";
resp=resp+"<rec><error>"+error+"</error></rec>";
```

Any value containing `<`, `>`, `&`, or `"` will produce malformed XML. If a stored record contains `</name></rec></body><injection>`, it breaks the XML structure for all downstream consumers (mobile app). The `error` attribute from request is also appended verbatim with no escaping. An attacker who can store a malformed unit or driver name will corrupt all API responses for that company.

---

### B02-5 — HIGH: Broken XML Escaping in `apiXml.jsp` — `else if` Chain Only Escapes First Matched Character

**File:** `apiXml.jsp`, lines 52–72
**Severity:** HIGH

```java
if(content.contains("&")) {
    content = content.replace("&","&amp;");
} else if(content.contains("'")) {
    content = content.replace("'","&apos;");
} else if(content.contains("\"")) {
    content = content.replace("\"","&quot;");
} else if(content.contains("<")) {
    content = content.replace("<","&lt;");
} else if(content.contains(">")) {
    content = content.replace("<","&gt;");  // also wrong: replaces "<" not ">"
}
```

Only the `API_QUESTION` branch attempts any XML escaping, but the `else if` chain means a string containing both `&` and `<` (e.g., `"A&B<C"`) will only have `&` escaped; the `<` remains raw. Additionally, the final `else if` branch has a copy-paste bug: it tests for `>` but calls `content.replace("<","&gt;")` — replacing `<` instead of `>`. The other API branches (`API_VEHICLE`, `API_DRIVER`, `API_ATTACHMENT`, `API_LOGIN`) have no escaping at all.

---

### B02-6 — HIGH: NullPointerException on `session.getAttribute("isDealer")` Without Null-Check in `adminReports.jsp`

**File:** `adminReports.jsp`, lines 4–5
**Severity:** HIGH

```java
String incidentReportUrl = session.getAttribute("isDealer").equals("true") ? ...
String sessionReportUrl  = session.getAttribute("isDealer").equals("true") ? ...
```

`session.getAttribute("isDealer")` is never null-checked before calling `.equals()`. If the session attribute is absent (e.g., first render after session partially initialised, or if the attribute name changed), a `NullPointerException` is thrown inside the JSP, causing an HTTP 500 response visible to the user. The `PreFlightActionServlet` only validates the presence of `sessCompId`, not `isDealer`.

---

### B02-7 — HIGH: NullPointerException on `session.getAttribute("sessDateFormat")` Without Null-Check in Three Report JSPs

**Files:**
- `dealer/impactReport.jsp`, line 5
- `dealer/incidentReport.jsp`, line 5
- `dealer/preOpsReport.jsp`, line 5
**Severity:** HIGH

```java
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```

`session.getAttribute("sessDateFormat")` is cast to `String` and `.replaceAll()` is called without any null-check. If the attribute is absent from the session, a `NullPointerException` is thrown. The session guard in `PreFlightActionServlet` only checks `sessCompId`. Separate action classes (`DealerImpactReportAction`, `DealerIncidentReportAction`, `DealerPreOpsReportAction`) also read `sessDateFormat` and would already have thrown if null, but the JSP is the point of visible failure if the action succeeds without setting it.

---

### B02-8 — HIGH: `apiXml.jsp` — `method` Attribute Read Without Null-Check Causes NPE

**File:** `apiXml.jsp`, line 13
**Severity:** HIGH

```java
String method = (String)request.getAttribute("method");
...
if(method.equalsIgnoreCase(RuntimeConf.API_LOGIN))
```

`method` is read from a request attribute (set by the action class) without a null-check. `AppAPIAction` is fully commented out — it sets no `method` attribute and returns `mapping.findForward("apiXml")` unconditionally. Therefore every request to `/api.do` reaches `apiXml.jsp` with `method == null`, causing an immediate `NullPointerException` on line 13.

---

### B02-9 — HIGH: `apiXml.jsp` Endpoint is Excluded From Session Authentication

**File:** `apiXml.jsp` (via `/api.do`)
**Related:** `PreFlightActionServlet.java`, line 106
**Severity:** HIGH

```java
else if (path.endsWith("api.do")) return false;
```

The `excludeFromFilter` method in `PreFlightActionServlet` returns `false` for `api.do`, meaning the session check is **skipped**. The endpoint is accessible without any valid session. Combined with B02-8 (NPE on `method`), the API is currently broken, but the authentication bypass is a separate standing defect that would be exploitable if the action were re-enabled.

---

### B02-10 — HIGH: `adminRegister` Action is Excluded From Session Authentication

**File:** `adminSubcompanyEdit.jsp` (via `adminRegister` action)
**Related:** `PreFlightActionServlet.java`, line 107
**Severity:** HIGH

```java
else if (path.endsWith("adminRegister.do")) return false;
```

The `adminRegister.do` action — which creates new company accounts including Cognito user sign-up — bypasses the session check entirely. `adminSubcompanyEdit.jsp` is the form that POSTs to this endpoint. An unauthenticated request that constructs the correct form parameters could register a new company account without being logged in. The action does enforce minimum field validation (name, email, password) but performs no authentication check.

---

### B02-11 — MEDIUM: URL Inconsistency — `sessionreport.do` Hardcoded Alongside Dynamic URL in `adminReports.jsp`

**File:** `adminReports.jsp`, line 36
**Severity:** MEDIUM

```html
<h3><a href="sessionreport.do">Session Report</a></h3>
...
<a href="<%= sessionReportUrl %>" class="box-a"><img .../>
```

The heading link for Session Report is hardcoded to `sessionreport.do` (line 36) while the image/icon link uses the correctly computed `sessionReportUrl` variable (line 38). For dealer users, the heading link will incorrectly navigate to the non-dealer endpoint rather than `dealerSessionReport.do`. This is a functional bug that causes a navigation failure for dealer accounts.

---

### B02-12 — MEDIUM: Business Logic (Role-Routing) in View Layer — `adminReports.jsp`

**File:** `adminReports.jsp`, lines 3–6
**Severity:** MEDIUM

```java
String incidentReportUrl = session.getAttribute("isDealer").equals("true") ? "dealerIncidentReport.do" : "incidentreport.do";
String sessionReportUrl  = session.getAttribute("isDealer").equals("true") ? "dealerSessionReport.do" : "sessionreport.do";
```

The role-based URL routing decision (dealer vs. non-dealer) is embedded in the JSP scriptlet rather than being computed in the action class (`AdminMenuAction`) and passed as a request attribute. This makes the routing logic untestable without a full JSP container, and creates a divergence from how the action class already passes `isDealer` as a request attribute (`request.setAttribute("isDealer", session.getAttribute("isDealer"))` in `AdminMenuAction`). The JSP re-reads from session directly rather than using the request attribute set by the controller.

---

### B02-13 — MEDIUM: JSP Declaration Defines Business Helper in View Layer — `incidentReport.jsp`

**File:** `dealer/incidentReport.jsp`, lines 7–11
**Severity:** MEDIUM

```jsp
<%!
    String getYesNoMessageKey(boolean value) {
        return value ? "clst.answerY" : "clst.answerN";
    }
%>
```

A JSP `<%! %>` declaration defines a method (`getYesNoMessageKey`) directly in the JSP servlet class. This is untestable in isolation — it cannot be unit-tested without instantiating the JSP container. The method belongs in a utility class or in the `IncidentReportEntryBean`. The method is then used dynamically to construct `<bean:message>` keys (line 107–109), which is a non-idiomatic Struts pattern.

---

### B02-14 — MEDIUM: `adminSubcompanyEdit.jsp` — Client-Side-Only Validation, No Server-Side Equivalent in View

**File:** `dealer/adminSubcompanyEdit.jsp`, lines 137–169
**Severity:** MEDIUM

The `fnsubmitAccount()` JavaScript function is the sole field-validation gate before form submission. The function checks: non-empty company name, non-empty email, non-empty password, password confirmation match, and timezone selection. These checks are client-side only and can be bypassed by submitting the form directly (e.g., via `curl`). While `AdminRegisterAction` does validate name, email, and password on the server, it does **not** validate the timezone or confirm-password match. The `cpassword` field is not present in `AdminRegisterActionForm` at all (confirmed from action code), so confirm-password validation exists only in JavaScript.

---

### B02-15 — MEDIUM: `apiXml.jsp` Contains Duplicate Dead Code Block

**File:** `apiXml.jsp`, lines 75–88
**Severity:** MEDIUM

```java
else if(method.equalsIgnoreCase(RuntimeConf.API_RESULT))
{
    // ... same body at lines 75-81
}
else if(method.equalsIgnoreCase(RuntimeConf.API_RESULT))  // duplicate condition, lines 82-88
{
    // ... identical body
}
```

The `API_RESULT` branch appears twice with identical condition and body. The second block is dead code — it can never execute because the first `else if` will always match first. This indicates copy-paste error and reduces confidence in the correctness of this file. The entire file's action code is commented out in `AppAPIAction`, meaning this dead code also has no live execution path.

---

### B02-16 — MEDIUM: `adminUnit.jsp` and `adminUser.jsp` — Hidden `action` Field Controllable by Client

**Files:** `adminUnit.jsp` line 83; `adminUser.jsp` line 92
**Severity:** MEDIUM

```html
<input type="hidden" name="action" value=""/>
<input type="hidden" name="equipId" value=""/>
```

Both list pages include hidden form fields `action` and `equipId`/`driverId` with empty default values. These are populated by JavaScript before form submission. However, because they are standard HTML `<input>` fields, a client could intercept or construct a request with arbitrary `action` values (e.g., `action=delete`). In `AdminUnitAction`, the `delete` branch calls `unitDAO.delUnitById(equipId)` with no additional ownership or CSRF check beyond session presence. There is no CSRF token in either form.

---

### B02-17 — LOW: `adminUser.jsp` — Form Uses GET Method, Exposing Search Term in URL

**File:** `adminUser.jsp`, line 20
**Severity:** LOW

```html
<form method="get" action="admindriver.do">
```

The search form uses `GET`, which causes the `searchDriver` value to appear in the browser URL bar, address-bar history, server access logs, and HTTP `Referer` headers. While `searchDriver` is an employee search term (not a credential), exposure in logs or browser history is undesirable for a user-management page. The equivalent vehicle search (`adminUnit.jsp`) correctly uses `POST`.

---

### B02-18 — LOW: `impactReport.jsp` — Scriptlet Accesses Bean Method in HTML Attribute Without Escaping

**File:** `dealer/impactReport.jsp`, line 99
**Severity:** LOW

```jsp
<span style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;">
```

`getImpactLevelCSSColor()` returns a value derived from an enumeration (`ImpactUtil.getCSSColor`) that currently returns fixed strings (`"blue"`, `"orange"`, `"red"`). However, if the return value were ever changed to incorporate a database-sourced string, it would be injected unescaped into a CSS `style` attribute, enabling CSS injection or potentially DOM XSS. The value is not under direct user control today, so severity is LOW, but the pattern is unsafe.

---

### B02-19 — LOW: `adminSubscription.jsp` — Page Described as "Not Used" in Controlling Action

**File:** `adminSubscription.jsp`
**Related:** `AdminMenuAction.java`, line 108 — comment "//Not used"
**Severity:** LOW

The `subscription` action branch in `AdminMenuAction` (line 108) is commented as "Not used", yet the tile definition `adminSubscriptionDefinition` remains active and the form submits to `adminsubscription.do`. The JSP renders against `arrSubscription` (a request attribute not set by `AdminMenuAction`'s subscription branch — it sets `alertList` and `reportList` instead), so the form would render with no checkboxes. This dead page presents a maintenance hazard and may represent an abandoned feature that was not properly retired.

---

### B02-20 — INFO: No Test Coverage for Any JSP View File or Their Primary Action Classes

**Severity:** INFO

None of the four existing test files (`UnitCalibrationImpactFilterTest`, `UnitCalibrationTest`, `UnitCalibratorTest`, `ImpactUtilTest`) reference any JSP, the `AdminMenuAction`, `AdminUnitAction`, `AppAPIAction`, `AdminRegisterAction`, `DealerImpactReportAction`, `DealerIncidentReportAction`, or `DealerPreOpsReportAction` classes. There is no integration test, JSP unit test, or Selenium/functional test for any page in scope. All eight issues in the view layer identified above (B02-1 through B02-9) have zero automated detection coverage.

---

### B02-21 — INFO: `dateFormat` Session Variable Injected into JavaScript Without JS-Encoding

**Files:** `dealer/impactReport.jsp` line 125; `dealer/incidentReport.jsp` line 156; `dealer/preOpsReport.jsp` line 117
**Severity:** INFO

```jsp
setupDatePicker('#start_date', '<%= dateFormat %>', start_date);
```

`dateFormat` is derived from `session.getAttribute("sessDateFormat")` which is set at login. The value is company-controlled (set by an admin), not directly end-user controlled. However, if a malicious company-level admin were to set a date format string containing a single-quote or JavaScript-significant characters, the value would be injected verbatim into a JavaScript string literal. This is currently low risk due to the source of the value, but the pattern is unsafe.

---

## 4. Finding Summary

| ID | Severity | File(s) | Issue |
|----|----------|---------|-------|
| B02-1 | CRITICAL | `adminUnit.jsp` | Reflected XSS — `searchUnit` unescaped in HTML attribute |
| B02-2 | CRITICAL | `adminUser.jsp` | Reflected XSS — `searchDriver` unescaped in HTML attribute |
| B02-3 | CRITICAL | `dealer/impactReport.jsp`, `dealer/incidentReport.jsp`, `dealer/preOpsReport.jsp` | JavaScript injection via `start_date`/`end_date` parameters into inline script |
| B02-4 | CRITICAL | `apiXml.jsp` | XML injection — stored data written to XML without encoding |
| B02-5 | HIGH | `apiXml.jsp` | Broken `else if` XML escaping; wrong character replaced in `>` branch |
| B02-6 | HIGH | `adminReports.jsp` | NPE — `session.getAttribute("isDealer")` without null-check |
| B02-7 | HIGH | `dealer/impactReport.jsp`, `dealer/incidentReport.jsp`, `dealer/preOpsReport.jsp` | NPE — `session.getAttribute("sessDateFormat")` without null-check |
| B02-8 | HIGH | `apiXml.jsp` | NPE — `method` request attribute read without null-check; action class is commented out |
| B02-9 | HIGH | `apiXml.jsp` (via `/api.do`) | Endpoint excluded from session authentication |
| B02-10 | HIGH | `dealer/adminSubcompanyEdit.jsp` (via `adminRegister.do`) | Account registration endpoint excluded from session authentication |
| B02-11 | MEDIUM | `adminReports.jsp` | Hardcoded `sessionreport.do` link overrides computed dealer URL for heading |
| B02-12 | MEDIUM | `adminReports.jsp` | Role-routing logic in view layer (untestable scriptlet) |
| B02-13 | MEDIUM | `dealer/incidentReport.jsp` | Business helper method defined as JSP declaration (untestable) |
| B02-14 | MEDIUM | `dealer/adminSubcompanyEdit.jsp` | Confirm-password and timezone validation exists only client-side |
| B02-15 | MEDIUM | `apiXml.jsp` | Duplicate dead code — `API_RESULT` branch appears twice |
| B02-16 | MEDIUM | `adminUnit.jsp`, `adminUser.jsp` | Hidden `action` field controllable by client; no CSRF protection |
| B02-17 | LOW | `adminUser.jsp` | Search form uses GET method — search terms visible in URL/logs |
| B02-18 | LOW | `dealer/impactReport.jsp` | CSS injection risk if `getImpactLevelCSSColor()` source changes |
| B02-19 | LOW | `adminSubscription.jsp` | Page marked "Not used" in action but tile/form remain active |
| B02-20 | INFO | All nine files | Zero automated test coverage for all JSP views and primary action classes |
| B02-21 | INFO | `dealer/impactReport.jsp`, `dealer/incidentReport.jsp`, `dealer/preOpsReport.jsp` | Session-derived `dateFormat` injected into JS string without JS-encoding |
