# Audit Report B04 — Pass 2: JSP View-Layer Test-Coverage Audit

**Audit agent:** B04
**Date:** 2026-02-26
**Scope:** JSP view files — test coverage gaps, security concerns, untestable patterns
**Test directory:** `src/test/java/`

---

## Files Audited

1. `src/main/webapp/html-jsp/formBuilder.jsp`
2. `src/main/webapp/html-jsp/getAjax.jsp`
3. `src/main/webapp/html-jsp/getDriverName.jsp`
4. `src/main/webapp/html-jsp/getcode.jsp`
5. `src/main/webapp/html-jsp/home.jsp`
6. `src/main/webapp/html-jsp/login.jsp`
7. `src/main/webapp/html-jsp/mailSuccuess.jsp`
8. `src/main/webapp/html-jsp/mod/sendmail.jsp`
9. `src/main/webapp/html-jsp/privacy.jsp`

---

## Section 1 — Reading Evidence

### 1.1 `formBuilder.jsp`

**Purpose:** Renders a dynamic form constructed from `FormElementBean` objects retrieved from the request attribute `arrFormEle`. Forwards to `formBuilder.do` on submit. Used for the diagnostic form builder feature.

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 47–69 | Iterates `arrFormEle` (cast from `request.getAttribute("arrFormEle")`); extracts `name`, `lable`, `value`, `type`, `style`, `position` from each `FormElementBean`; emits them directly as JavaScript arguments to a jQuery plugin call. No escaping applied. |

**Key EL / Struts tag expressions:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 7 | `<%=RuntimeConf.projectTitle%>` | Static class field |
| 24 | `<bean:write name="fomrmsg"/>` | Struts ActionMessage (safe via Struts tag) |
| 28 | `<bean:write name="type">` | Request attribute `type` set by `FormBuilderAction` |
| 29 | `<bean:write name="qid">` | Request attribute `qid` set by `FormBuilderAction` |
| 60–65 | `<%=type%>`, `<%=lable%>`, `<%=value%>`, `<%=style%>`, `<%=position%>` | Bean fields — raw scriptlet interpolation into JavaScript string literals |

**Forms:**

| Element | Action | Method |
|---------|--------|--------|
| `<form id="formbuilder">` | `formBuilder.do` | POST |

**Backing action class:** `com.action.FormBuilderAction`
**Included libs:** `../includes/importLib.jsp` (imports Struts tags, `RuntimeConf`)

---

### 1.2 `getAjax.jsp`

**Purpose:** XML response fragment for AJAX look-up operations. Renders an XML document from the `arrXml` request attribute (`List<XmlBean>`). Used by vehicle type/power/question-content look-ups.

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 5–25 | Entire page is a scriptlet. Casts `request.getAttribute("arrXml")` to `ArrayList`; iterates, retrieving `id` and `name` from each `XmlBean`; concatenates them directly into XML string without escaping. |

**Key EL / attribute access:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 8 | `request.getAttribute("arrXml")` | Set by `GetAjaxAction` |
| 19–20 | `xmlBean.getId()`, `xmlBean.getName()` | Bean fields, inserted raw into XML |

**Content type:** `text/xml` (set at line 6).
**Forms:** None.
**Backing action class:** `com.action.GetAjaxAction`

---

### 1.3 `getDriverName.jsp`

**Purpose:** XML response fragment returning driver full names. Used for AJAX population of driver-name drop-downs.

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 5–27 | Entire page is a scriptlet. Casts `request.getAttribute("arrDriverList")` to `ArrayList<DriverBean>`; iterates; concatenates `getFirst_name()` and `getLast_name()` directly into XML without escaping. |

**Key attribute access:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 10 | `request.getAttribute("arrDriverList")` | Set by `GetXmlAction` |
| 15 | `getFirst_name()`, `getLast_name()` | `DriverBean` fields, inserted raw into XML |

**Content type:** `text/xml` (set at line 6).
**Forms:** None.
**Backing action class:** `com.action.GetXmlAction`

---

### 1.4 `getcode.jsp`

**Purpose:** Password-reset "get verification code" page. Displays a form asking for the user's email address and submits to `goResetPass.do`.

**Key scriptlets:** None.

**Key EL / Struts tag expressions:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 11 | `<html:errors>` | Struts errors scope |
| 23 | Inline `<a>` triggers `fnSubmit()` JavaScript | Client-side only |

**Forms:**

| Element | Action | Method |
|---------|--------|--------|
| `#confirmationCodeFrom` | `goResetPass.do` | POST |
| Hidden field `action` | value `reset` | Static |

**Client-side validation:** Email format validated in `validateEmail()` regex (lines 49–52). No server-side duplicate.
**Backing action class:** `com.action.GoResetPassAction`
**Included libs:** `../includes/importLib.jsp`

---

### 1.5 `home.jsp`

**Purpose:** Authenticated dashboard home page. Shows KPI panels (drivers joined today, pre-ops completed, impacts reported), navigation tiles (Vehicles, Drivers, Checklist, Locations, Dealers, Reports, Users), and conditionally includes the expiring-trainings panel.

**Key scriptlets:**

| Lines | Description |
|-------|-------------|
| 53 | `<%= session.getAttribute("isDealer").equals("true") ? "dealerPreOpsReport.do" : "preopsreport.do" %>` — session attribute accessed and `.equals()` called without null check; used as an HTML `href`. |
| 75 | `<%= session.getAttribute("isDealer").equals("true") ? "dealerImpactReport.do" : "impactreport.do"%>` — same pattern. |

**Key EL / Struts tag expressions:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 25 | `<bean:write name="totalDriver"/>` | Request attribute `totalDriver` |
| 48 | `<bean:write name="totalFleetCheck"/>` | Request attribute `totalFleetCheck` |
| 70 | `<bean:write name="totalImpactToday"/>` | Request attribute `totalImpactToday` |
| 86 | `<logic:notEmpty name="arrExpiringTrainings">` | Request attribute |
| 103 | `<logic:notEqual value="true" name="isDealer">` | Session/request attribute |
| 129 | `<logic:equal name="isDealer" value="true">` | Session attribute |
| 144 | `<logic:equal name="isSuperAdmin" value="true">` | Session attribute |

**Forms:** None (navigation links only).
**Backing action:** Rendered via Struts Tiles from `adminDefinition`; data set by post-login flow.

---

### 1.6 `login.jsp`

**Purpose:** Login page. Displays support contact information, login form (`username`, `password`, `timezone`), a link to password reset, and a registration button.

**Key scriptlets:** None.

**Key EL / Struts tag expressions:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 17 | `<html:errors>` | Struts error scope |
| 18–22 | `<bean:write name="resetpassmsg"/>` | ActionMessage `resetpassmsg` |
| 26 | `<html:text property="username">` | `LoginActionForm.username` |
| 29 | `<html:password property="password">` | `LoginActionForm.password` |

**Forms:**

| Element | Action | Method |
|---------|--------|--------|
| `<html:form>` | `login.do` | POST |

**Hardcoded content:**
- Lines 13–16: AU/UK/US support phone numbers and email addresses (`help@fleetsupport.com.au`, `support@ciiquk.com`) are hardcoded in the HTML.

**Client-side:** Line 51 calls `new Date().getTimezone()` (non-standard; Moment.js needed).
**Backing action class:** `com.action.LoginAction`

---

### 1.7 `mailSuccuess.jsp`

**Purpose:** File is 0 bytes (empty). No content exists.

**Key scriptlets:** None.
**Key EL / expressions:** None.
**Forms:** None.

---

### 1.8 `mod/sendmail.jsp`

**Purpose:** Modal form for composing and submitting a driver-invitation email. Submits to `sendMail.do`.

**Key scriptlets:** None.

**Key EL / Struts tag expressions:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 17 | `<html:errors>` | Struts error scope |
| 22 | `<html:text property="email">` | `AdminSendMailActionForm.email` |
| 31 | `<html:hidden property="accountAction" value="send_mail">` | Static |

**Forms:**

| Element | Action | Method |
|---------|--------|--------|
| `<html:form>` | `sendMail.do` | POST |

**Dead code:** Lines 42–50 define a `send()` JavaScript function that is never called (the submit button uses the Struts `<html:submit>` tag). A commented-out `onclick` link was removed but the function was not.

**Backing action class:** `com.action.AdminSendMailAction`
**Included libs:** `../../includes/importLib.jsp`

---

### 1.9 `privacy.jsp`

**Purpose:** Privacy policy acceptance page. Displays the privacy text (included from `privacyText.jsp`) in a read-only textarea. A checkbox must be checked to enable the submit button, which submits to `privacy.do`.

**Key scriptlets:** None.

**Key EL / Struts tag expressions:**

| Lines | Expression | Source |
|-------|-----------|--------|
| 9 | `<%@ include file="../includes/privacyText.jsp"%>` | Static include |
| 13 | `<bean:message key="privacy.accept">` | i18n message |
| 14 | `<html:submit styleId="submitBtn" disabled="true">` | Static |

**Forms:**

| Element | Action | Method |
|---------|--------|--------|
| `<form name="privacyForm">` | `privacy.do` | POST |

**Client-side gate only:** Submit button is enabled/disabled by JavaScript `enableSubmit()` (lines 23–34). No server-side enforcement of the acceptance. Mixing plain `<form>` with `<html:submit>` (Struts tag) in a non-`<html:form>` context is potentially broken.

**Backing action class:** `com.action.PrivacyAction`

---

## Section 2 — Test Coverage Grep Results

Grep of `src/test/java/` for references to:

- `formBuilder`, `FormBuilderAction`
- `getAjax`, `GetAjaxAction`
- `getDriverName`, `GetXmlAction`
- `getcode`, `GoResetPassAction`
- `home.jsp`, `WelcomeAction`
- `login.jsp`, `LoginAction`
- `mailSuccuess`
- `sendmail`, `sendMail`, `AdminSendMailAction`
- `privacy`, `PrivacyAction`

**Result: zero matches found in any of the four test files.**

The test suite (`src/test/java/`) contains exactly four files, all unrelated to the audited JSPs:

- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

No JSP, no backing Action class, and no ActionForm for any of the nine audited files has any test coverage.

---

## Section 3 — Findings

---

### B04-1 — Unescaped Bean Field Output into JavaScript String Literals (XSS)

**Severity:** CRITICAL
**File:** `formBuilder.jsp`, lines 60–65
**Finding:**

The scriptlet loop on lines 47–69 retrieves `FormElementBean` fields (`type`, `lable`, `value`, `style`, `position`) from the request attribute and emits them directly into JavaScript string literals without any HTML or JavaScript encoding:

```javascript
// Lines 59–66 (generated output)
$("#formbuilder").formbuilder("add",{
    type:'<%=type%>',
    name:'<%=lable%>_<%=position%>',
    label:'<%=lable%>',
    value:'<%=value%>',
    style:'<%=style%>',
    position:'<%=position%>'
});
```

If any bean field contains a single-quote or JavaScript fragment (e.g., a form field `value` of `'); alert(1);//`), the injected text would break out of the string literal and execute arbitrary JavaScript. These values originate from `FormBuilderDAO` which reads from the database; any user who can write form-builder records can inject code that runs for every admin who opens the form builder. Neither `Util.encodeJS()` nor `ESAPI.encoder().encodeForJavaScript()` nor equivalent is applied.

**Untestability vector:** The rendering logic is entirely in the JSP. There is no unit test path for this output.

---

### B04-2 — Unescaped Data in XML Response (XML Injection / XSS)

**Severity:** HIGH
**Files:** `getAjax.jsp` (lines 20), `getDriverName.jsp` (line 15)
**Finding:**

Both files build raw XML by string concatenation without escaping the values they insert:

`getAjax.jsp` line 20:
```java
resp=resp+"<rec>"+"<code>"+id+"</code><name>"+name+"</name></rec>";
```

`getDriverName.jsp` line 15:
```java
resp=resp+"<rec><name>"+(arrDriver.get(i)).getFirst_name()+" "+(arrDriver.get(i)).getLast_name()+"</name></rec>";
```

A database value containing `<`, `>`, `&`, or `"` will produce malformed XML that XML parsers may reject or misparse. A value containing an XML tag (e.g., `</name><inject>`) constitutes XML injection and could alter the structure the JavaScript consumer parses. If the consuming JavaScript subsequently writes this data into the DOM without escaping, a stored XSS path exists. Driver names are user-supplied data (entered in the driver registration flow) and are not sanitised at the database layer as observed in other audit pass files.

---

### B04-3 — Null-Pointer Dereference on Session Attribute in `home.jsp`

**Severity:** HIGH
**File:** `home.jsp`, lines 53 and 75
**Finding:**

Two scriptlet expressions call `.equals()` directly on the return value of `session.getAttribute("isDealer")` without a prior null check:

```java
// Line 53
<a href="<%= session.getAttribute("isDealer").equals("true") ? "dealerPreOpsReport.do" : "preopsreport.do" %>">

// Line 75
<a href="<%= session.getAttribute("isDealer").equals("true") ? "dealerImpactReport.do" : "impactreport.do"%>">
```

If the `isDealer` attribute is absent from the session (session timeout mid-page render, or a code path that sets `sessCompId` but not `isDealer`), a `NullPointerException` is thrown at render time. The global exception handler in `web.xml` will forward to `/error/error.html`, leaking that the application encountered a server-side error. Under `PreFlightActionServlet.excludeFromFilter`, the admin pages require `sessCompId` to be set but do not individually validate every session attribute used within tiles.

**Untestability vector:** Conditional navigation logic is embedded in the view layer with no corresponding unit test.

---

### B04-4 — No Authorization Check on `getAjax.jsp` / `getDriverName.jsp` Endpoints

**Severity:** HIGH
**Files:** `getAjax.jsp`, `getDriverName.jsp`; backing actions `GetAjaxAction`, `GetXmlAction`
**Finding:**

The `PreFlightActionServlet.excludeFromFilter()` method checks session validity for all `.do` endpoints it does not explicitly exempt. `getAjax.do` and `getXml.do` are not in the exemption list, so a valid session is nominally required to call them. However, `GetAjaxAction` does not verify that the authenticated session belongs to a user with permission to query units, questions, or GPS data for the requested `manu_id`, `type_id`, `qus_id`, or `compId` parameters. Any authenticated user from any company can call `getAjax.do?action=last_gps&compId=<any_id>` and retrieve GPS position data for units belonging to other companies. This is an Insecure Direct Object Reference (IDOR). The `GetXmlAction` similarly retrieves the driver list using `sessCompId` from the session (acceptable isolation), but the absence of tests means the session-binding assumption is never verified.

---

### B04-5 — Session Attribute Null-Check Bug in `PrivacyAction` Propagates to `privacy.jsp`

**Severity:** MEDIUM
**File:** `privacy.jsp`; backing action `PrivacyAction.java` line 21
**Finding:**

`PrivacyAction.java` contains a precedence bug:

```java
String sessCompId = (String) session.getAttribute("sessCompId") == null ? "" :
    (String) session.getAttribute("sessCompId");
```

Due to Java operator precedence, `(String) session.getAttribute("sessCompId") == null` casts the return of `getAttribute` to `String` then compares with null; the ternary always assigns the raw attribute cast. If `sessCompId` is null the cast will succeed (null cast is valid) but `sessCompId` will be null, causing `companyDAO.updateCompPrivacy(null)` to be called. This silently passes a null company ID to the DAO, which may execute an unbounded `UPDATE` on the company privacy table. The `privacy.jsp` view itself is clean, but the zero-test coverage of `PrivacyAction` means this has never been caught.

---

### B04-6 — Client-Side-Only Privacy Acceptance Enforcement

**Severity:** MEDIUM
**File:** `privacy.jsp`, lines 13–33
**Finding:**

The privacy agreement submit button is disabled in HTML (`disabled="true"`) and re-enabled only by the `enableSubmit()` JavaScript function when the checkbox is checked. `PrivacyAction.java` performs no check that the form was submitted with the privacy checkbox ticked. A user can submit a direct POST to `privacy.do` with no checkbox field and the action will call `updateCompPrivacy()` unconditionally, marking the account as having accepted the policy without the user having done so.

The mixed use of a plain HTML `<form name="privacyForm">` with a Struts `<html:submit>` tag (which expects to be inside `<html:form>`) is also a framework misuse that is difficult to test through standard Struts testing tooling.

---

### B04-7 — `mailSuccuess.jsp` Is an Empty File

**Severity:** MEDIUM
**File:** `mailSuccuess.jsp`
**Finding:**

The file exists at the declared path but contains zero bytes. If any Struts forward references this file, the container will serve an empty HTTP 200 response with no content, silently failing to render anything to the user. Additionally, the filename contains a typo (`Succeess`). No test verifies the success flow after a mail send.

---

### B04-8 — Hardcoded Internal Contact Details in `login.jsp`

**Severity:** LOW
**File:** `login.jsp`, lines 12–16
**Finding:**

Production support contact information (phone numbers and email addresses) is hardcoded directly in the JSP:

```html
AU Phone: 1800 190 629 or email help@fleetsupport.com.au
UK Phone: +44 (0) 1460 259101 or email support@ciiquk.com
US Phone: 864-479-1080
```

Any update to support channels requires a source code change and redeployment. These should be externalised to a message-resource bundle (`ApplicationResources.properties`) consistent with the use of `<bean:message>` elsewhere in the application.

---

### B04-9 — Mixed HTTP/HTTPS Third-Party Script Inclusion

**Severity:** LOW
**File:** `formBuilder.jsp`, line 13
**Finding:**

Line 13 loads jQuery UI over plain HTTP:

```html
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.js"></script>
```

Line 12 loads jQuery over HTTPS. If the page is served over HTTPS (standard for production), browsers will block the mixed-content HTTP script load, silently breaking all jQuery UI interactions. Additionally, version 1.8.23 of jQuery UI (released circa 2012) contains multiple known vulnerabilities. No tests exercise the JavaScript-dependent form builder.

---

### B04-10 — Dead JavaScript Function in `mod/sendmail.jsp`

**Severity:** LOW
**File:** `mod/sendmail.jsp`, lines 42–50
**Finding:**

A `send()` JavaScript function is defined but never called. The form relies on the Struts `<html:submit>` button with no `onclick`. The dead function references `document.sendMailForm.email.value`, but the Struts form renders with a generated name (not `sendMailForm`), so even if it were called, the reference would be `undefined`. This is residual dead code from a commented-out UI approach and creates confusion about what the intended validation flow is. No test covers the client-side validation path.

---

### B04-11 — Missing CSRF Protection on All POST Forms

**Severity:** HIGH
**Files:** `formBuilder.jsp`, `getcode.jsp`, `mod/sendmail.jsp`, `privacy.jsp`, `login.jsp`
**Finding:**

None of the POST forms in the audited JSPs include a CSRF synchroniser token. The Struts 1 framework in use does not automatically add CSRF tokens. An attacker with network access to an authenticated admin can craft a cross-origin POST to:

- `formBuilder.do` — submit diagnostic form data on behalf of an admin.
- `goResetPass.do` — trigger a password reset email to an attacker-chosen address.
- `sendMail.do` — send an invitation email to an arbitrary address.
- `privacy.do` — mark privacy as accepted for any authenticated company.

The lack of tests means this structural absence has not been flagged by any automated check.

---

### B04-12 — Zero Test Coverage for All Nine Audited JSPs and Their Backing Classes

**Severity:** HIGH
**Files:** All nine JSPs; backing classes `FormBuilderAction`, `GetAjaxAction`, `GetXmlAction`, `GoResetPassAction`, `LoginAction`, `AdminSendMailAction`, `PrivacyAction`
**Finding:**

The test directory contains four files covering only calibration utilities and `ImpactUtil`. No test file references any of the audited JSPs or any of the following backing action classes:

- `FormBuilderAction` — email dispatch logic, form parameter iteration, HTML construction
- `GetAjaxAction` — multi-action AJAX dispatcher, session attribute access
- `GetXmlAction` — driver list retrieval for XML
- `GoResetPassAction` — password reset flow via Cognito
- `LoginAction` — full authentication and session initialisation
- `AdminSendMailAction` — email validation and JNDI mail sending
- `PrivacyAction` — privacy flag update (with known null-check bug B04-5)

Business logic residing in Action classes (email composition, HTML generation in `FormBuilderAction` line 61, form parameter iteration on lines 63–71) cannot be tested without the view but is also not covered at the controller level.

---

### B04-13 — Business Logic (HTML Email Generation) Inside Action Class, Not Testable from View

**Severity:** INFO
**File:** `FormBuilderAction.java`, lines 61–72 (view consequence in `formBuilder.jsp`)
**Finding:**

`FormBuilderAction` constructs raw HTML for diagnostic emails directly in the Action class by iterating `request.getParameterNames()`. This is untestable business logic embedded in the controller layer with no service abstraction. Combined with the untestable scriptlet rendering in `formBuilder.jsp`, there is no path to verify correct email content without a full integration test. The HTML construction (`html += "<tr><td>"+ParameterNames+"</td><td>"+ParameterValues+"</td></tr>"`) also echoes raw request parameter values into email HTML without sanitisation, creating a stored-to-email HTML injection risk.

---

## Summary Table

| ID | Severity | File(s) | Title |
|----|----------|---------|-------|
| B04-1 | CRITICAL | `formBuilder.jsp:60-65` | Unescaped bean fields into JavaScript literals (XSS) |
| B04-2 | HIGH | `getAjax.jsp:20`, `getDriverName.jsp:15` | Unescaped data in XML response (XML injection) |
| B04-3 | HIGH | `home.jsp:53,75` | Null-pointer dereference on `isDealer` session attribute |
| B04-4 | HIGH | `getAjax.jsp`, `getDriverName.jsp` | No IDOR protection on AJAX data endpoints |
| B04-5 | MEDIUM | `privacy.jsp` / `PrivacyAction.java:21` | Null-check precedence bug in PrivacyAction |
| B04-6 | MEDIUM | `privacy.jsp:13-33` | Client-side-only privacy acceptance enforcement |
| B04-7 | MEDIUM | `mailSuccuess.jsp` | File is empty (zero bytes) |
| B04-8 | LOW | `login.jsp:12-16` | Hardcoded support contact details |
| B04-9 | LOW | `formBuilder.jsp:13` | Mixed HTTP/HTTPS — outdated jQuery UI over HTTP |
| B04-10 | LOW | `mod/sendmail.jsp:42-50` | Dead JavaScript function (`send()`) |
| B04-11 | HIGH | All POST forms | No CSRF token on any form |
| B04-12 | HIGH | All nine JSPs + 7 action classes | Zero test coverage |
| B04-13 | INFO | `FormBuilderAction.java:61-72` | Business logic / HTML email generation untestable |
