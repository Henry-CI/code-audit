# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** B04
**Scope:** 9 JSP view files
**Test directory:** `src/test/java/`

---

## Preamble: Test Infrastructure State

The test directory contains exactly **4 test files**, none of which address any JSP file audited here:

| Test File | Subject |
|---|---|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | `UnitCalibrationImpactFilter` business logic |
| `com/calibration/UnitCalibrationTest.java` | `UnitCalibration` business logic |
| `com/calibration/UnitCalibratorTest.java` | `UnitCalibrator` business logic |
| `com/util/ImpactUtilTest.java` | `ImpactUtil` utility methods |

**Zero JSP tests exist.** No Selenium, HTMLUnit, Mockito MVC, or equivalent view-layer tests are present anywhere in the project. Every finding below is therefore a coverage gap by definition.

---

## JSP 1: fleetcheckSuccess.jsp

**Path:** `src/main/webapp/html-jsp/fleetcheckSuccess.jsp`

### Evidence

**Purpose:** Post-fleet-check success/completion page. Displays a localised success message and a 10-second countdown timer before automatically submitting a hidden form that redirects to `goSerach.do` (search). Also provides a manual logout button via `logout.do`.

**Scriptlet blocks:** None. All server-side content is via Struts tags (`bean:message`).

**EL expressions / request attributes accessed:** None directly. `bean:message` keys used:
- `clst.successcomplete`
- `clst.note1`
- `clst.note2`
- `button.logout`

**JavaScript with security implications:**
```javascript
var time = 10;
document.onload = init();   // incorrect: assigns return value, not function reference

function init() {
    setInterval(countDown, 1000);
}

function countDown() {
    if (time > 0) {
        time--;
        document.getElementById("timer").innerHTML = time;
        if (time == 0) { redirect(); }
    }
}

function redirect() {
    document.searchForm.submit();
}
```

### Findings

**B04-1 | Severity: HIGH | Untested automatic form submission via countdown timer**
The countdown timer calls `document.searchForm.submit()` after 10 seconds. The form `searchForm` posts to `goSerach.do`. There is no test verifying that the redirect target is correct, that the timer fires exactly once (no double-submission), or that the timer is cancelled when the user manually logs out. A malformed or prematurely triggered submission could leave session state inconsistent.

**B04-2 | Severity: MEDIUM | JavaScript bug: `document.onload` assigned return value, not function reference**
Line `document.onload = init();` calls `init()` immediately and assigns its return value (`undefined`) to `document.onload`. The interval is started synchronously during page evaluation, not deferred to document load. There is no test that would catch this mis-wiring. In some browsers this may work incidentally; in others the DOM element `timer` may not yet exist when `countDown` first fires.

**B04-3 | Severity: MEDIUM | No null/missing-element guard in countdown JavaScript**
`document.getElementById("timer").innerHTML = time;` will throw a JavaScript `TypeError` if the element `timer` is absent for any reason (e.g., i18n template changes or partial page loads). No test covers this defensive path.

**B04-4 | Severity: LOW | `goSerach.do` — apparent typo in action URL**
The form action is `goSerach.do` (missing letter). No test verifies this resolves to a valid action mapping, so a renamed action would silently cause a 404 after fleet-check completion.

**B04-5 | Severity: LOW | No test for i18n key resolution**
Three `bean:message` keys (`clst.successcomplete`, `clst.note1`, `clst.note2`) are untested. A missing or mis-spelled resource key causes a visible `???clst.successcomplete???` string in production with no automated detection.

---

## JSP 2: formBuilder.jsp

**Path:** `src/main/webapp/html-jsp/formBuilder.jsp`

### Evidence

**Purpose:** Dynamic form-builder view. Renders form elements stored in the `arrFormEle` request attribute (an `ArrayList<FormElementBean>`) into a sortable jQuery UI list. Allows saving a form (`formBuilder.do` POST). Conditionally shows a submit button only when `type == "diagnostic"`.

**Scriptlet blocks:**
```java
// Lines 47-69 — inside <script> block, renders JavaScript calls
ArrayList arrFormEle = (ArrayList) request.getAttribute("arrFormEle");
for (int m = 0; m < arrFormEle.size(); m++) {
    FormElementBean formElementBean = (FormElementBean) arrFormEle.get(m);
    String name  = formElementBean.getName();
    String lable = formElementBean.getLable();
    String value = formElementBean.getValue();
    String type  = formElementBean.getType();
    String style = formElementBean.getStyle();
    int position = formElementBean.getPosition();
    // emits JavaScript:
    // $("#formbuilder").formbuilder("add", {
    //     type:'<%=type%>', name:'<%=lable%>_<%=position%>',
    //     label:'<%=lable%>', value:'<%=value%>',
    //     style:'<%=style%>', position:'<%=position%>'
    // });
}
```

**Request attributes accessed:**
- `arrFormEle` — `ArrayList<FormElementBean>` (used in scriptlet and `<logic:notEmpty>`)
- `type` — `String` (used in `bean:write` hidden input and `logic:equal`)
- `qid` — `String` (used in `bean:write` hidden input)

**EL / Struts tags:**
- `<logic:notEmpty name="arrFormEle">` / `<logic:empty name="arrFormEle">`
- `<bean:write name="type">` (inside hidden input `value` attribute)
- `<bean:write name="qid">` (inside hidden input `value` attribute)
- `<logic:equal name="type" value="diagnostic">` (conditional submit button)
- `<html:messages id="fomrmsg" message="true">` / `<bean:write name="fomrmsg">`

**JavaScript with security implications:**
- External jQuery loaded over HTTP (not HTTPS): `http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.js` (line 13)
- FormElementBean field values (`lable`, `value`, `style`, `type`) are interpolated **without escaping** directly into a JavaScript string literal context:
  ```javascript
  type:'<%=type%>',
  name:'<%=lable%>_<%=position%>',
  label:'<%=lable%>',
  value:'<%=value%>',
  style:'<%=style%>'
  ```

### Findings

**B04-6 | Severity: CRITICAL | Stored XSS via unescaped FormElementBean fields into JavaScript context**
`lable`, `value`, `style`, and `type` from `FormElementBean` are written verbatim into JavaScript string literals (single-quoted) inside the `<script>` block. If any of these fields contain a single quote, backslash, or `</script>`, an attacker who can control form element data (e.g., via the admin form builder) can inject arbitrary JavaScript executed in every user's browser that views the form. There is no HTML escaping, no JavaScript escaping, and no test verifying this output is sanitised.

**B04-7 | Severity: HIGH | NullPointerException if `arrFormEle` is null in scriptlet**
The scriptlet at line 48 calls `request.getAttribute("arrFormEle")` and immediately accesses `.size()` with no null check. The `<logic:notEmpty>` guard on lines 21 and 37 only wraps the Struts HTML; the scriptlet inside the `<script>` block (line 47–69) is **outside** the `<logic:notEmpty>` block and runs unconditionally. If the action does not set `arrFormEle`, a `NullPointerException` is thrown at line 49, producing a 500 error. No test exercises the null/missing attribute path.

**B04-8 | Severity: HIGH | External jQuery UI loaded over plain HTTP (mixed content / supply chain)**
Line 13 loads jQuery UI from `http://ajax.googleapis.com/...` — a non-HTTPS URL. On HTTPS deployments this is a mixed-content block. On any deployment this is a supply-chain risk (no subresource integrity check). No test covers script load failure or degraded behaviour.

**B04-9 | Severity: HIGH | Unchecked raw cast of `ArrayList` without generic type parameter**
Line 48: `ArrayList arrFormEle = (ArrayList) request.getAttribute("arrFormEle");` uses a raw type. Line 51: `FormElementBean formElementBean = (FormElementBean) arrFormEle.get(m);` is an unchecked cast. If the action places a differently-typed object in the attribute, a `ClassCastException` is thrown at runtime with no test detecting this contract breakage.

**B04-10 | Severity: HIGH | `bean:write name="type"` and `bean:write name="qid"` output unescaped into HTML attribute**
`<bean:write>` by default does **not** HTML-encode output. Values of `type` and `qid` are written directly into `value="..."` HTML attributes. If either contains `"` or `>`, the attribute is broken or HTML-injected. No test validates encoding of these values.

**B04-11 | Severity: MEDIUM | Unused import of `com.util.Util`**
Line 4 imports `com.util.Util` but it is never referenced in the JSP. Untested dead import may indicate a removed feature whose server-side logic still populates attributes consumed here.

**B04-12 | Severity: MEDIUM | No test for `logic:empty` fallback branch (empty form)**
The empty-form path (`arrFormEle` is an empty list, triggering `<logic:empty>`) shows a localised message `clst.formbuilder.nocontent`. No test verifies this branch is reached or renders correctly.

**B04-13 | Severity: MEDIUM | `type == "diagnostic"` conditional submit button — no test for boundary values**
The submit button only appears when `type` exactly equals `"diagnostic"`. No test verifies that other `type` values suppress the button, or that the `diagnostic` case shows it.

---

## JSP 3: getAjax.jsp

**Path:** `src/main/webapp/html-jsp/getAjax.jsp`

### Evidence

**Purpose:** AJAX endpoint. Returns an XML document (content type `text/xml`) listing code/name pairs from the `arrXml` request attribute. Used for populating dropdowns or other dynamic UI elements.

**Scriptlet blocks (entire file is scriptlet):**
```java
response.setContentType("text/xml");
ArrayList arrXml = (ArrayList) request.getAttribute("arrXml");
String resp = "";
resp = resp + "<body>";
if (arrXml.size() > 0) {
    for (int i = 0; i < arrXml.size(); i++) {
        XmlBean xmlBean = (XmlBean) arrXml.get(i);
        String id   = xmlBean.getId();
        String name = xmlBean.getName();
        resp = resp + "<rec><code>" + id + "</code><name>" + name + "</name></rec>";
    }
}
resp = resp + "</body>";
out.println(resp);
```

**Request attributes accessed:**
- `arrXml` — `ArrayList<XmlBean>`

**JavaScript with security implications:** None (this file produces XML output only).

### Findings

**B04-14 | Severity: CRITICAL | XML injection via unescaped `id` and `name` fields**
`xmlBean.getId()` and `xmlBean.getName()` are concatenated directly into the XML string without any XML escaping. If either field contains `<`, `>`, `&`, `"`, or `'`, the resulting output is malformed XML or—if the data originates from user input—could inject additional XML elements, corrupting the consumer's parsed result or enabling XML-based client-side attacks. No test validates output encoding.

**B04-15 | Severity: HIGH | NullPointerException if `arrXml` attribute is null**
`request.getAttribute("arrXml")` is cast and immediately dereferenced (`.size()`) with no null check. If the backing action does not set this attribute, the JSP throws `NullPointerException`, producing a malformed XML response or HTTP 500. No test covers this path.

**B04-16 | Severity: HIGH | NullPointerException if `xmlBean.getId()` or `xmlBean.getName()` is null**
`XmlBean` fields default to `null` (not `""`). Concatenating a null `String` in Java produces the literal string `"null"` which would appear in XML output, but any direct method call on a null reference would throw NPE. No null-guard exists and no test exercises null-field beans.

**B04-17 | Severity: HIGH | Unchecked raw `ArrayList` cast — no generic type safety**
`ArrayList arrXml = (ArrayList) request.getAttribute("arrXml")` uses a raw type. The subsequent `(XmlBean) arrXml.get(i)` cast is unchecked. A type mismatch causes `ClassCastException` at runtime with no test preventing regression.

**B04-18 | Severity: MEDIUM | String concatenation in loop is O(n²) — untested performance boundary**
Each iteration appends to an immutable `String resp` using `+`. For large result sets this is quadratic in memory and time. No performance or load test exists to establish a safe upper bound on `arrXml.size()`.

**B04-19 | Severity: MEDIUM | XML content type set to `text/xml` but no XML declaration or charset**
The response sets `text/xml` without an XML declaration (`<?xml version="1.0" encoding="UTF-8"?>`). RFC 2616 / RFC 7303 defaults `text/xml` to US-ASCII, while the page encoding is UTF-8. Non-ASCII characters in `id` or `name` may be misinterpreted by consumers. No test validates the encoding contract.

---

## JSP 4: getDriverName.jsp

**Path:** `src/main/webapp/html-jsp/getDriverName.jsp`

### Evidence

**Purpose:** AJAX endpoint returning an XML list of driver full names from the `arrDriverList` request attribute. Used for driver-name lookups in dynamic UI.

**Scriptlet blocks (entire file is scriptlet):**
```java
response.setContentType("text/xml");
String resp = "";
resp = resp + "<body>";
ArrayList<DriverBean> arrDriver = (ArrayList<DriverBean>) request.getAttribute("arrDriverList");
if (arrDriver.size() > 0) {
    for (int i = 0; i < arrDriver.size(); i++) {
        resp = resp + "<rec><name>"
             + (arrDriver.get(i)).getFirst_name()
             + " "
             + (arrDriver.get(i)).getLast_name()
             + "</name></rec>";
    }
} else {
    resp = resp + "<rec><name></name></rec>";
}
resp = resp + "</body>";
out.println(resp);
```

**Request attributes accessed:**
- `arrDriverList` — `ArrayList<DriverBean>`

**JavaScript with security implications:** None.

### Findings

**B04-20 | Severity: CRITICAL | XML injection via unescaped driver first_name and last_name**
`getFirst_name()` and `getLast_name()` are concatenated into XML without escaping. Driver names containing XML special characters (`<`, `&`, `"`) produce malformed or injected XML output. No test validates safe encoding of driver name data.

**B04-21 | Severity: HIGH | NullPointerException if `arrDriverList` attribute is null**
`request.getAttribute("arrDriverList")` is cast to `ArrayList<DriverBean>` and `.size()` is called immediately with no null check. If the backing action omits the attribute, a `NullPointerException` is thrown. No test exercises this error path.

**B04-22 | Severity: HIGH | NullPointerException if `getFirst_name()` or `getLast_name()` returns null**
`DriverBean` fields `first_name` and `last_name` default to `null`. String concatenation of null produces the literal `"null"` in output, but this is semantically incorrect for a name field. No test verifies graceful handling of null name fields (e.g., empty string or a placeholder).

**B04-23 | Severity: HIGH | `arrDriver.get(i)` called twice per iteration — potential for ConcurrentModificationException**
Each loop iteration calls `arrDriver.get(i)` twice (once for `first_name`, once for `last_name`). While not a threading issue in single-threaded JSP evaluation, this pattern is fragile and untested for any concurrent access or list-modification scenario.

**B04-24 | Severity: MEDIUM | Same O(n²) string concatenation issue as getAjax.jsp**
See B04-18. The same performance anti-pattern applies here.

**B04-25 | Severity: MEDIUM | Empty-list branch outputs an empty-name record rather than an empty body**
The `else` branch emits `<rec><name></name></rec>` when no drivers exist. Consumers receiving this sentinel value must distinguish it from a real empty-name driver. This contract is untested, and a change to the sentinel would silently break all consumers.

---

## JSP 5: getcode.jsp

**Path:** `src/main/webapp/html-jsp/getcode.jsp`

### Evidence

**Purpose:** Password-reset "get code" page. Presents an email input form that POSTs to `goResetPass.do` with `action=reset`. Client-side validation checks that the field is non-empty and matches an email regex before submitting.

**Scriptlet blocks:** None.

**EL expressions / request attributes accessed:**
- `<html:errors>` — renders Struts action errors (from request scope).

**JavaScript with security implications:**
```javascript
function fnSubmit() {
    var username = $('[name="username"]').val();
    if (username == "") {
        swal("Error", "Email is required", "error");
    } else if (!validateEmail(username)) {
        swal("Error", "Email format is incorrect", "error");
    } else {
        $('#confirmationCodeFrom').submit();
    }
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@
              ((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|
              (([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
```

### Findings

**B04-26 | Severity: HIGH | Client-side-only email validation — no server-side test coverage**
`validateEmail()` runs only in the browser. JavaScript can be disabled or bypassed, allowing any string (including empty, SQL, or script content) to reach `goResetPass.do`. No test verifies server-side validation of the `username` parameter in the action.

**B04-27 | Severity: MEDIUM | `html:errors` output is unescaped by default in Struts 1.x**
`<html:errors>` renders Struts `ActionErrors` messages without HTML encoding unless the resource bundle values themselves are encoded. If an error message incorporates user-supplied input (e.g., reflecting the submitted username), XSS is possible. No test validates the output of this error block.

**B04-28 | Severity: MEDIUM | No CSRF protection on password reset form**
The form at `confirmationCodeFrom` contains no CSRF token. An attacker can craft a page that submits a victim's email address to `goResetPass.do`, triggering a reset email without the victim's intent. No test verifies CSRF mitigations.

**B04-29 | Severity: LOW | `swal` (SweetAlert) dependency undeclared in this file**
`swal(...)` is called but the SweetAlert library is not imported in this JSP; it presumably comes from the `importLib.jsp` include. If the include changes or the library is removed, validation fails silently (no error is shown). No test verifies the validation feedback path.

**B04-30 | Severity: LOW | No test for `html:errors` empty state**
No test verifies that the page renders without errors when `html:errors` has nothing to display (i.e., that no stale error bleed-through from a previous request occurs).

---

## JSP 6: home.jsp

**Path:** `src/main/webapp/html-jsp/home.jsp`

### Evidence

**Purpose:** Main authenticated dashboard. Displays summary statistics (drivers joined today, pre-ops completed today, impacts reported today) and navigation tiles for Vehicles, Drivers, Checklist, Locations (dealer), Dealers (super-admin), Reports, and Users. Conditionally shows sections based on `isDealer` and `isSuperAdmin` session attributes.

**Scriptlet blocks:**
```java
// Line 53
session.getAttribute("isDealer").equals("true") ? "dealerPreOpsReport.do" : "preopsreport.do"

// Line 75
session.getAttribute("isDealer").equals("true") ? "dealerImpactReport.do" : "impactreport.do"
```

**Request/session attributes accessed:**
- `totalDriver` (request) — via `<bean:write name="totalDriver"/>`
- `totalFleetCheck` (request) — via `<bean:write name="totalFleetCheck"/>`
- `totalImpactToday` (request) — via `<bean:write name="totalImpactToday"/>`
- `arrExpiringTrainings` (request) — via `<logic:notEmpty name="arrExpiringTrainings">`
- `isDealer` (session) — via scriptlet and `<logic:notEqual>`, `<logic:equal>` tags
- `isSuperAdmin` (session) — via `<logic:equal name="isSuperAdmin" value="true">`

**JavaScript with security implications:** None directly in this file.

### Findings

**B04-31 | Severity: CRITICAL | NullPointerException if `session.getAttribute("isDealer")` returns null**
Lines 53 and 75 call `.equals("true")` directly on the result of `session.getAttribute("isDealer")` without a null check. If the session attribute is absent (e.g., session expired, attribute not set by action, or new session without login action), a `NullPointerException` is thrown, crashing the page. No test verifies behaviour when this attribute is missing.

**B04-32 | Severity: HIGH | `bean:write` renders `totalDriver`, `totalFleetCheck`, `totalImpactToday` unescaped**
`<bean:write>` does not HTML-encode by default. If any of these attributes contains HTML-special characters (unlikely for counts, but possible if a string is placed in the attribute by error), it is rendered raw. No test validates the type or encoding of these values.

**B04-33 | Severity: HIGH | No test for `isDealer=true` rendering path**
When `isDealer` is `"true"`, the "Drivers" navigation tile is hidden, a "Locations" tile appears, and all report links point to dealer-specific actions. None of these conditional rendering paths are tested.

**B04-34 | Severity: HIGH | No test for `isSuperAdmin=true` rendering path**
When `isSuperAdmin` is `"true"`, a "Dealers" navigation tile appears. This path is untested.

**B04-35 | Severity: HIGH | No test for `arrExpiringTrainings` present vs. absent**
`<logic:notEmpty name="arrExpiringTrainings">` conditionally includes `expiringTrainings.jsp`. Neither the truthy path (include rendered) nor the falsy path (omitted) is covered by any test.

**B04-36 | Severity: MEDIUM | Hardcoded action URL strings — no validation test**
Report and navigation links include hardcoded action names (`admindriver.do`, `dealerPreOpsReport.do`, `preopsreport.do`, `dealerImpactReport.do`, `impactreport.do`, `adminmenu.do`, `dealercompanies.do`). A renamed action silently produces a 404 with no automated detection.

**B04-37 | Severity: MEDIUM | No test for dashboard with all stats at zero**
The zero-count boundary case for `totalDriver`, `totalFleetCheck`, and `totalImpactToday` is not tested. If these values are rendered as `null` (attribute not set), `<bean:write>` renders nothing, which is visually misleading.

---

## JSP 7: login.jsp

**Path:** `src/main/webapp/html-jsp/login.jsp`

### Evidence

**Purpose:** Login page. Renders a username/password form posting to `login.do`. Also displays Struts action errors, a password-reset success message, and static support contact information. Contains a small script to populate a hidden timezone field.

**Scriptlet blocks:** None.

**EL expressions / request attributes accessed:**
- `<html:errors>` — Struts action errors
- `<html:messages id="resetpassmsg" message="true">` / `<bean:write name="resetpassmsg"/>` — password reset success message

**Struts form fields:**
- `username` (`html:text`)
- `password` (`html:password`)
- `timezone` (`html:hidden`)
- `signin` (`html:submit`)

**JavaScript with security implications:**
```javascript
$('input[name="timezone"]').val(new Date().getTimezone());
```
`Date.prototype.getTimezone()` does not exist in standard JavaScript (the correct method is `getTimezoneOffset()`). This call returns `undefined`, setting an empty value on the hidden field.

### Findings

**B04-38 | Severity: HIGH | `new Date().getTimezone()` is not a valid JavaScript method**
`Date.prototype.getTimezone()` does not exist in any browser. The call returns `undefined`, so `$('input[name="timezone"]').val(undefined)` sets the hidden input to the string `"undefined"` or leaves it unchanged depending on the jQuery version. The intended value (user's timezone offset) is never captured. No test verifies the timezone value submitted to the server, meaning the server-side action receives a garbage or empty timezone on every login.

**B04-39 | Severity: HIGH | `html:errors` and `bean:write name="resetpassmsg"` unescaped output**
Both `<html:errors>` and `<bean:write name="resetpassmsg"/>` render without HTML escaping by default in Struts 1.x. If any error or message value includes user-controlled input (e.g., reflecting the submitted username in a "User X not found" message), XSS is possible. No test validates the encoding of rendered messages.

**B04-40 | Severity: HIGH | Hardcoded support contact information (phone numbers and email addresses) in view**
Lines 12–16 contain:
- AU Phone: `1800 190 629`, email `help@fleetsupport.com.au`
- UK Phone: `+44 (0) 1460 259101`, email `support@ciiquk.com`
- US Phone: `864-479-1080`

These are hardcoded strings in the JSP. A change in contact details requires a code deployment. No test ensures these values are current or intentional.

**B04-41 | Severity: MEDIUM | No CSRF token on login form**
The login form (`login.do` POST) carries no CSRF token. While login CSRF is lower risk than authenticated CSRF, it can be exploited to log a victim into an attacker's account (login CSRF). No test checks for CSRF mitigation.

**B04-42 | Severity: MEDIUM | No test for password-reset message display path**
The `<html:messages>` block for `resetpassmsg` renders only when a message is present. No test verifies this conditional block appears correctly after a successful reset, or that it is absent on a normal login page load.

**B04-43 | Severity: LOW | No test for empty vs. populated `html:errors` on failed login**
No test verifies that `<html:errors>` renders the expected error message on login failure, nor that it renders nothing on a fresh page load.

---

## JSP 8: mailSuccuess.jsp

**Path:** `src/main/webapp/html-jsp/mailSuccuess.jsp`

### Evidence

**Purpose:** Unable to determine. The file exists on disk but has **zero bytes** (0 bytes confirmed by `wc -c`). The file is completely empty.

**Scriptlet blocks:** None.
**EL expressions:** None.
**JavaScript:** None.

### Findings

**B04-44 | Severity: HIGH | `mailSuccuess.jsp` is an empty file — dead or incomplete view**
The file has 0 bytes of content. If any action forwards to this view, the user receives a completely blank response. There is no test verifying what this page should display, no test detecting that it is empty, and no Struts action configuration audit confirming whether this view is reachable. The misspelled filename (`Succuess` rather than `Success`) also suggests this may be a stub or renamed artefact that was never completed. Combined with zero test coverage, the intended success message after a mail operation is entirely untested.

**B04-45 | Severity: LOW | Filename typo: `mailSuccuess.jsp` (double 'u' in 'Succ**u**ess')**
The filename contains a typographical error. Any Struts action mapping referencing this exact misspelled name will function, but the name is confusing and makes the file harder to locate. No test would catch a corrected filename breaking an existing mapping.

---

## JSP 9: mod/sendmail.jsp

**Path:** `src/main/webapp/html-jsp/mod/sendmail.jsp`

### Evidence

**Purpose:** Modal dialog content for sending an email. Presents a single email address input field that POSTs to `sendMail.do`. Used as an in-page overlay (modal), based on the `modal-content-wrap` CSS class and the `ajax_mode_x` form class.

**Scriptlet blocks:** None.

**EL expressions / request attributes accessed:**
- `<html:errors>` — Struts action errors
- Form fields:
  - `email` (`html:text`, property on backing ActionForm)
  - `submit` (`html:submit`)
  - `accountAction` (`html:hidden`, value hardcoded to `"send_mail"`)

**JavaScript with security implications:**
```javascript
function send() {
    var email = document.sendMailForm.email.value;
    if (email == "") {
        swal("Error", "Email is required", "error");
    } else {
        document.sendMailForm.submit();
    }
}
```
Note: The `send()` function references `document.sendMailForm` but the form rendered by `<html:form>` generates a form with `name` based on the ActionForm class name (not `sendMailForm`). This function is also **dead code** — it is defined but never called (the commented-out `onclick="send();"` anchor was replaced by an `html:submit` button).

### Findings

**B04-46 | Severity: HIGH | `send()` JavaScript function is dead code and references a non-existent form name**
The function `send()` at line 43 references `document.sendMailForm.email.value`. The Struts `<html:form>` tag generates the form `name` from the ActionForm class name (likely `AdminSendMailActionForm` or similar), not `sendMailForm`. The function is never invoked (the only visible trigger — an `onclick` anchor — is commented out at line 29). This dead, broken code is untested and misleading.

**B04-47 | Severity: HIGH | No client-side email format validation on the active submit path**
The active submit button (`html:submit`) has no `onclick` validation handler. The `send()` function (which contained the empty-check) is dead code. The form submits directly to `sendMail.do` with whatever value (including empty) is in the email field. No test verifies that the server-side action rejects invalid or empty email addresses.

**B04-48 | Severity: HIGH | `html:errors` rendered without HTML escaping — potential XSS in modal**
`<html:errors>` inside the modal will render Struts action errors without encoding. If the email field value is reflected in an error message, a crafted email input could inject HTML into the modal. No test validates error message encoding.

**B04-49 | Severity: MEDIUM | Hardcoded hidden field `accountAction=send_mail` — no test for value integrity**
`<html:hidden property="accountAction" value="send_mail">` hardcodes the action discriminator. If the server-side action's expected value changes, mail sending silently fails. No test verifies the round-trip value.

**B04-50 | Severity: MEDIUM | No CSRF protection on send-mail form**
The `sendMail.do` POST form carries no CSRF token. An authenticated user visiting a malicious page could be made to send emails through the application without consent. No test checks for CSRF mitigation.

**B04-51 | Severity: MEDIUM | No test for the `html:errors` empty state in modal context**
No test verifies that the modal renders cleanly when no errors are present and that a previous form submission's errors do not bleed into a fresh modal open.

**B04-52 | Severity: LOW | `swal` dependency not declared in this file**
`swal(...)` in the (dead) `send()` function depends on SweetAlert being loaded by the including page. No test verifies the dependency chain, and since `send()` is dead code, this is informational only.

---

## Summary Table

| Finding | JSP | Severity | Category |
|---|---|---|---|
| B04-1 | fleetcheckSuccess | HIGH | Untested automatic form submission |
| B04-2 | fleetcheckSuccess | MEDIUM | JavaScript bug — onload misuse |
| B04-3 | fleetcheckSuccess | MEDIUM | Missing null guard in timer JS |
| B04-4 | fleetcheckSuccess | LOW | Typo in action URL `goSerach.do` |
| B04-5 | fleetcheckSuccess | LOW | Untested i18n key resolution |
| B04-6 | formBuilder | CRITICAL | Stored XSS — unescaped fields into JS |
| B04-7 | formBuilder | HIGH | NPE if `arrFormEle` is null in scriptlet |
| B04-8 | formBuilder | HIGH | jQuery UI loaded over HTTP (mixed content) |
| B04-9 | formBuilder | HIGH | Unchecked raw ArrayList cast |
| B04-10 | formBuilder | HIGH | `bean:write` unescaped into HTML attribute |
| B04-11 | formBuilder | MEDIUM | Unused import `com.util.Util` |
| B04-12 | formBuilder | MEDIUM | Empty form branch untested |
| B04-13 | formBuilder | MEDIUM | `type == "diagnostic"` button untested |
| B04-14 | getAjax | CRITICAL | XML injection via unescaped id/name |
| B04-15 | getAjax | HIGH | NPE if `arrXml` is null |
| B04-16 | getAjax | HIGH | NPE if XmlBean fields are null |
| B04-17 | getAjax | HIGH | Unchecked raw ArrayList cast |
| B04-18 | getAjax | MEDIUM | O(n²) string concatenation |
| B04-19 | getAjax | MEDIUM | Missing XML declaration / charset |
| B04-20 | getDriverName | CRITICAL | XML injection via unescaped driver names |
| B04-21 | getDriverName | HIGH | NPE if `arrDriverList` is null |
| B04-22 | getDriverName | HIGH | NPE if first_name or last_name is null |
| B04-23 | getDriverName | HIGH | `arrDriver.get(i)` called twice per iteration |
| B04-24 | getDriverName | MEDIUM | O(n²) string concatenation |
| B04-25 | getDriverName | MEDIUM | Empty-list sentinel contract untested |
| B04-26 | getcode | HIGH | Client-side-only email validation |
| B04-27 | getcode | MEDIUM | `html:errors` unescaped output |
| B04-28 | getcode | MEDIUM | No CSRF token on reset form |
| B04-29 | getcode | LOW | `swal` dependency undeclared |
| B04-30 | getcode | LOW | No test for empty `html:errors` state |
| B04-31 | home | CRITICAL | NPE if `isDealer` session attribute is null |
| B04-32 | home | HIGH | `bean:write` stats rendered unescaped |
| B04-33 | home | HIGH | `isDealer=true` rendering path untested |
| B04-34 | home | HIGH | `isSuperAdmin=true` rendering path untested |
| B04-35 | home | HIGH | `arrExpiringTrainings` conditional untested |
| B04-36 | home | MEDIUM | Hardcoded action URLs — no validation test |
| B04-37 | home | MEDIUM | Zero-count boundary untested |
| B04-38 | login | HIGH | `Date.getTimezone()` is not a valid JS method |
| B04-39 | login | HIGH | `html:errors` / `resetpassmsg` unescaped |
| B04-40 | login | HIGH | Hardcoded support contact info in view |
| B04-41 | login | MEDIUM | No CSRF token on login form |
| B04-42 | login | MEDIUM | Reset message display path untested |
| B04-43 | login | LOW | `html:errors` empty vs. populated untested |
| B04-44 | mailSuccuess | HIGH | File is empty (0 bytes) — dead/incomplete view |
| B04-45 | mailSuccuess | LOW | Filename typo `Succuess` |
| B04-46 | mod/sendmail | HIGH | `send()` is dead code referencing wrong form name |
| B04-47 | mod/sendmail | HIGH | No email validation on active submit path |
| B04-48 | mod/sendmail | HIGH | `html:errors` unescaped in modal — XSS risk |
| B04-49 | mod/sendmail | MEDIUM | Hardcoded `accountAction` value untested |
| B04-50 | mod/sendmail | MEDIUM | No CSRF token on send-mail form |
| B04-51 | mod/sendmail | MEDIUM | `html:errors` empty state untested in modal |
| B04-52 | mod/sendmail | LOW | `swal` dependency undeclared (dead code) |

**Severity counts:** CRITICAL: 4 | HIGH: 23 | MEDIUM: 17 | LOW: 8
**Total findings:** 52
**JSP test coverage:** 0 of 9 files have any test coverage (0%)
