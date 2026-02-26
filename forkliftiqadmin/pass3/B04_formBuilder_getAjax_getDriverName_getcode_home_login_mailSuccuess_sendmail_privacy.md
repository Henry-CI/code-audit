# Pass 3 Documentation Audit — Agent B04
**Date:** 2026-02-26
**Auditor:** B04
**Scope:** formBuilder.jsp, getAjax.jsp, getDriverName.jsp, getcode.jsp, home.jsp, login.jsp, mailSuccuess.jsp, mod/sendmail.jsp, privacy.jsp

---

## Reading Evidence

---

### 1. formBuilder.jsp
**File:** `src/main/webapp/html-jsp/formBuilder.jsp`
**Purpose:** Renders a drag-and-drop form builder UI. Iterates over a list of `FormElementBean` objects from the request attribute `arrFormEle` and emits JavaScript `formbuilder("add", ...)` calls to populate the builder widget. Submits to `formBuilder.do` with a hidden `action=save` field.

**JSP scriptlet blocks:**
- Lines 47–69: Loop over `arrFormEle` request attribute; extracts `name`, `lable`, `value`, `type`, `style`, `position` from each `FormElementBean`; emits JS `.formbuilder("add", {...})` call per element.

**JSP expression blocks:**
- Line 7: `<%=RuntimeConf.projectTitle%>` — page title
- Lines 60–65: `<%=type%>`, `<%=lable%>_<%=position%>`, `<%=lable%>`, `<%=value%>`, `<%=style%>`, `<%=position%>` — inline in JS object literal

**Include directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`
- Line 2: `<%@ page import="com.bean.FormElementBean" %>`
- Line 3: `<%@ page import="java.util.ArrayList" %>`
- Line 4: `<%@ page import="com.util.Util" %>`

**HTML form action attributes:**
- Line 22: `action="formBuilder.do"`

**Session attribute accesses:**
- None directly in this file (session indirectly used via `importLib.jsp`)

**Significant JavaScript functions:**
- Anonymous `$(window).ready(...)` handler (lines 43–70): initialises the `formbuilder` widget and populates it by calling `.formbuilder("add", {...})` for each server-side form element.

---

### 2. getAjax.jsp
**File:** `src/main/webapp/html-jsp/getAjax.jsp`
**Purpose:** AJAX endpoint that returns an XML response. Reads the `arrXml` request attribute (a list of `XmlBean` objects) and serialises each as `<rec><code>...</code><name>...</name></rec>` inside a `<body>` wrapper. Used to populate drop-downs or similar UI controls via AJAX.

**JSP scriptlet blocks:**
- Lines 5–26 (entire file body): Sets `contentType` to `text/xml`; iterates `arrXml`; builds and prints the XML string.

**JSP expression blocks:**
- None

**Include directives:**
- None (no `<%@ include %>` or `<jsp:include>`)

**HTML form action attributes:**
- None

**Session attribute accesses:**
- None

**Significant JavaScript functions:**
- None

---

### 3. getDriverName.jsp
**File:** `src/main/webapp/html-jsp/getDriverName.jsp`
**Purpose:** AJAX XML endpoint that returns a list of driver full names from the `arrDriverList` request attribute. Each driver entry is emitted as `<rec><name>first last</name></rec>`. Returns a single empty `<rec><name></name></rec>` if the list is empty.

**JSP scriptlet blocks:**
- Lines 5–27 (entire file body): Sets `contentType` to `text/xml`; iterates `arrDriver`; builds and prints XML.

**JSP expression blocks:**
- None

**Include directives:**
- None

**HTML form action attributes:**
- None

**Session attribute accesses:**
- None

**Significant JavaScript functions:**
- None

---

### 4. getcode.jsp
**File:** `src/main/webapp/html-jsp/getcode.jsp`
**Purpose:** Password-reset "get verification code" page. Presents a form with an email field; validates the input client-side before submitting to `goResetPass.do`. A hidden field `action=reset` indicates to the server-side action which sub-flow to execute.

**JSP scriptlet blocks:**
- None

**JSP expression blocks:**
- None

**Include directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form action attributes:**
- Line 12: `action="goResetPass.do"`

**Session attribute accesses:**
- None

**Significant JavaScript functions:**
- `fnSubmit()` (lines 32–47): Validates that the email field is non-empty and well-formed before programmatically submitting the form; shows SweetAlert dialogs on error.
- `validateEmail(email)` (lines 49–52): Regex-based email format validator.

---

### 5. home.jsp
**File:** `src/main/webapp/html-jsp/home.jsp`
**Purpose:** Admin dashboard / home page. Displays three summary stat panels (drivers joined today, pre-ops completed today, impacts reported today) and a grid of navigation tiles (Vehicles, Drivers, Checklist, Locations, Dealers, Reports, Users). Panel links and tile visibility are conditionally routed based on the session attributes `isDealer` and `isSuperAdmin`.

**JSP scriptlet blocks:**
- None (conditional logic handled via Struts `<logic:*>` tags)

**JSP expression blocks:**
- Line 53: `<%= session.getAttribute("isDealer").equals("true") ? "dealerPreOpsReport.do" : "preopsreport.do" %>` — href for "Pre-ops Completed Today" panel
- Line 75: `<%= session.getAttribute("isDealer").equals("true") ? "dealerImpactReport.do" : "impactreport.do"%>` — href for "Impacts Reported Today" panel

**Include directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`
- Line 87: `<jsp:include page="expiringTrainings.jsp"/>` (conditional on `arrExpiringTrainings` not empty)

**HTML form action attributes:**
- None

**Session attribute accesses:**
- Line 53: `session.getAttribute("isDealer")` — determines pre-ops report destination URL
- Line 75: `session.getAttribute("isDealer")` — determines impact report destination URL
- (Also used implicitly via Struts scoped beans: `isDealer` at lines 103, 129; `isSuperAdmin` at line 144)

**Significant JavaScript functions:**
- None

---

### 6. login.jsp
**File:** `src/main/webapp/html-jsp/login.jsp`
**Purpose:** Login page. Presents a username/password form submitting to `login.do`, displays support contact details in an alert banner, shows Struts validation errors and any reset-password success message, and provides a link to the password-reset flow and a register button.

**JSP scriptlet blocks:**
- None

**JSP expression blocks:**
- None

**Include directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form action attributes:**
- Line 23: `action="login.do"` (via `<html:form>`)

**Session attribute accesses:**
- None directly

**Significant JavaScript functions:**
- Anonymous inline script (line 51): Sets the hidden `timezone` field value using `new Date().getTimezone()`.

---

### 7. mailSuccuess.jsp
**File:** `src/main/webapp/html-jsp/mailSuccuess.jsp`
**Purpose:** Intended to display a mail-success confirmation message (inferred from filename). File is completely empty — zero bytes, zero lines.

**JSP scriptlet blocks:** None (file is empty)
**JSP expression blocks:** None
**Include directives:** None
**HTML form action attributes:** None
**Session attribute accesses:** None
**Significant JavaScript functions:** None

---

### 8. mod/sendmail.jsp
**File:** `src/main/webapp/html-jsp/mod/sendmail.jsp`
**Purpose:** Modal form for sending an email. Prompts the user to enter an email address and submits to `sendMail.do` with a hidden `accountAction=send_mail` field. Rendered inside a modal dialog (`modal-content-wrap`).

**JSP scriptlet blocks:**
- None

**JSP expression blocks:**
- None

**Include directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp"%>`

**HTML form action attributes:**
- Line 15: `action="sendMail.do"` (via `<html:form>`)

**Session attribute accesses:**
- None

**Significant JavaScript functions:**
- `send()` (lines 43–50): Validates that the email field is non-empty before submitting `sendMailForm`. NOTE: This function references `document.sendMailForm` but the form rendered by `<html:form action="sendMail.do">` will have a generated name; the function appears to be dead code — the form is now submitted via the `<html:submit>` button and the `ajax_mode_x` CSS class (AJAX interceptor). Two lines of the original button-based invocation are commented out (lines 23, 29).

**Dead/commented-out code:**
- Line 23: `<!-- <input class="col-md-12" name="mail_id" ... > -->` — original plain-HTML email input, replaced by `<html:text>`.
- Line 29: `<!-- <a href="#" ... onclick="send();">Send Mail</a> -->` — original button calling `send()`, replaced by `<html:submit>`.

---

### 9. privacy.jsp
**File:** `src/main/webapp/html-jsp/privacy.jsp`
**Purpose:** Privacy policy acceptance page. Displays the privacy policy text (included from `privacyText.jsp`) in a read-only textarea. A checkbox must be checked before the submit button is enabled, then the form posts to `privacy.do`.

**JSP scriptlet blocks:**
- None

**JSP expression blocks:**
- None

**Include directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp"%>`
- Line 9: `<%@ include file="../includes/privacyText.jsp"%>` (inlined into textarea)

**HTML form action attributes:**
- Line 6: `action="privacy.do"`

**Session attribute accesses:**
- None

**Significant JavaScript functions:**
- `enableSubmit()` (lines 23–33): Toggles the `disabled` property of the submit button based on the checkbox state.

---

## Findings

**B04-01 | LOW | formBuilder.jsp:1 | Missing page-level comment**
No HTML or JSP comment near the top of the file describes the page's purpose, what `arrFormEle` represents, or how the formbuilder widget is initialised. A brief `<%-- --%>` or `<!-- -->` header would aid maintainers unfamiliar with the Struts form-builder workflow.

**B04-02 | MEDIUM | formBuilder.jsp:47-69 | Complex scriptlet block without comment**
The scriptlet (22 lines) iterates `arrFormEle`, unpacks six fields from each `FormElementBean`, and emits JavaScript object literals directly into the page. There is no comment explaining: (a) why the element name is constructed as `lable + "_" + position` rather than the `name` field, (b) what the `style` field controls in the widget, or (c) why `Util` is imported but never used in this file. The raw `arrFormEle` attribute key is also undocumented.

**B04-03 | LOW | formBuilder.jsp:4 | Unused import with no comment**
`com.util.Util` is imported on line 4 but never referenced anywhere in the file. No comment explains why it is present (dead import, in-progress work, etc.).

**B04-04 | LOW | formBuilder.jsp:30 | Magic string `action=save` without comment**
The hidden field `<input type="hidden" value="save" name="action">` uses the string literal `"save"` with no comment indicating what other values are valid for this action dispatch parameter or how the server-side handler uses it.

**B04-05 | LOW | getAjax.jsp:1 | Missing page-level comment**
No comment describes the endpoint's purpose, the expected caller, the structure of the `arrXml` request attribute, or the XML schema returned. As a headless XML endpoint it is especially important to document what consumes it and the expected contract.

**B04-06 | MEDIUM | getAjax.jsp:5-26 | Non-trivial XML serialisation scriptlet without comment**
The entire file logic is one uncommented scriptlet block. The hand-built XML string concatenation (`resp=resp+"<rec>"...`) is non-obvious and fragile (no escaping of special characters in `id` or `name`). No comment explains the expected schema, the source of `arrXml`, or why manual string building is used instead of a proper XML library.

**B04-07 | LOW | getAjax.jsp:8 | Undocumented request attribute key `arrXml`**
The attribute name `arrXml` is cryptic. No comment documents what data it holds, which action populates it, or what `XmlBean.id` / `XmlBean.name` represent in business terms.

**B04-08 | LOW | getDriverName.jsp:1 | Missing page-level comment**
No comment describes the endpoint's purpose, the expected AJAX caller, or the XML schema it emits.

**B04-09 | MEDIUM | getDriverName.jsp:5-27 | Non-trivial scriptlet without comment**
The single uncommented scriptlet handles the entire response generation including the empty-list fallback branch. No comment explains why an empty name record (`<rec><name></name></rec>`) is returned instead of an empty body or a status element, nor what the downstream JavaScript is expected to do with it.

**B04-10 | LOW | getDriverName.jsp:10 | Undocumented request attribute key `arrDriverList`**
The attribute name `arrDriverList` is not self-evident as to which action populates it or whether it may legitimately be `null` (which would cause a `NullPointerException` before the size check).

**B04-11 | LOW | getcode.jsp:1 | Missing page-level comment**
No comment describes the page as part of the password-reset flow, its position in the reset sequence, or which action it targets.

**B04-12 | LOW | getcode.jsp:25 | Magic string `action=reset` without comment**
The hidden field `value="reset"` dispatches the server-side action sub-flow. No comment documents what other values exist or what `reset` triggers on the server.

**B04-13 | LOW | home.jsp:1 | Missing page-level comment**
No comment describes the page as the admin dashboard, which role/session attributes gate which tiles, or how `isDealer` and `isSuperAdmin` interact to produce the navigation layout.

**B04-14 | MEDIUM | home.jsp:53 | Undocumented session attribute `isDealer` used in inline expression**
`session.getAttribute("isDealer")` is called directly in a JSP expression without any comment. The attribute holds a `String` `"true"`/`"false"` (not a `Boolean`), compared via `.equals("true")`. This non-obvious string representation has no documentation. A `NullPointerException` would be thrown if the attribute is absent from the session (e.g. unauthenticated access), and there is no null guard.

**B04-15 | MEDIUM | home.jsp:75 | Same undocumented `isDealer` pattern repeated without null guard**
Identical to B04-14 at line 75 for the impact report link. Both occurrences carry the same risk and absence of documentation.

**B04-16 | LOW | home.jsp:53,75 | Magic action strings `dealerPreOpsReport.do`, `preopsreport.do`, `dealerImpactReport.do`, `impactreport.do` without comment**
Four hard-coded action strings control routing but have no comment explaining when each applies or where they are mapped in the Struts configuration.

**B04-17 | LOW | login.jsp:1 | Missing page-level comment**
No comment describes the page, the Struts ActionForm it relies on, or the significance of the hidden `timezone` field.

**B04-18 | LOW | login.jsp:51 | Non-standard `Date.getTimezone()` call without comment**
`new Date().getTimezone()` is not a standard JavaScript `Date` method. The standard method is `getTimezoneOffset()`. No comment explains what value is expected, whether a polyfill is in use, or what the server does with the `timezone` field.

**B04-19 | HIGH | mailSuccuess.jsp:— | Zero-byte file**
`mailSuccuess.jsp` is completely empty (0 bytes). Any code path that forwards or redirects to this page will produce a blank response with no HTML, no error, and no feedback to the user. The filename (noting the misspelling "Succuess") suggests it was intended to display a mail-sent confirmation. The empty state is a functional defect as well as a documentation failure.

**B04-20 | LOW | mod/sendmail.jsp:1 | Missing page-level comment**
No comment describes the modal's purpose, which workflow opens it, what `accountAction=send_mail` triggers on the server, or why it is inside the `mod/` subdirectory.

**B04-21 | LOW | mod/sendmail.jsp:31 | Magic string `accountAction=send_mail` without comment**
The hidden field `value="send_mail"` is a dispatch key with no explanation of valid alternatives or the server-side handling.

**B04-22 | LOW | mod/sendmail.jsp:23,29 | Commented-out code blocks without explanation**
Lines 23 and 29 contain commented-out HTML (`<input>` and `<a>` elements) with no note explaining when they were replaced, why the current approach (`<html:text>` / `<html:submit>`) was preferred, or whether they should be deleted.

**B04-23 | MEDIUM | mod/sendmail.jsp:43-50 | Dead JavaScript function `send()` with no comment**
The `send()` function references `document.sendMailForm` which does not match the name of the Struts-generated form, and the button that called it (the `onclick="send();"` anchor) is commented out. The function is unreachable dead code. No comment explains this or marks it for removal. If a future developer uncomments the button, the function will silently fail to locate the form and the `null.submit()` call will throw a runtime JS error.

**B04-24 | LOW | privacy.jsp:1 | Missing page-level comment**
No comment describes the page as a first-login privacy acceptance gate, the significance of the checkbox, or which action (`privacy.do`) it posts to.

**B04-25 | LOW | privacy.jsp:20 | Comment `<!-- /container -->` misleading**
Line 20 carries the comment `<!-- /container -->` but the element it closes is `<div class="span8">` (a Bootstrap 2 span column), not a container div. The nearest `.containerL` div closes at the same point. While minor, the comment references a class name that does not appear in the enclosing markup, which could mislead developers navigating the DOM structure.

---

## Summary Table

| ID     | Severity | File                        | Line(s) | Issue                                                                 |
|--------|----------|-----------------------------|---------|-----------------------------------------------------------------------|
| B04-01 | LOW      | formBuilder.jsp             | 1       | Missing page-level comment                                            |
| B04-02 | MEDIUM   | formBuilder.jsp             | 47-69   | Complex scriptlet (22 lines) without comment                          |
| B04-03 | LOW      | formBuilder.jsp             | 4       | Unused import `com.util.Util` with no explanatory comment             |
| B04-04 | LOW      | formBuilder.jsp             | 30      | Magic string `action=save` undocumented                               |
| B04-05 | LOW      | getAjax.jsp                 | 1       | Missing page-level comment on XML endpoint                            |
| B04-06 | MEDIUM   | getAjax.jsp                 | 5-26    | Non-trivial XML serialisation scriptlet without comment               |
| B04-07 | LOW      | getAjax.jsp                 | 8       | Cryptic undocumented request attribute key `arrXml`                   |
| B04-08 | LOW      | getDriverName.jsp           | 1       | Missing page-level comment on XML endpoint                            |
| B04-09 | MEDIUM   | getDriverName.jsp           | 5-27    | Non-trivial scriptlet with empty-list branch, no comment              |
| B04-10 | LOW      | getDriverName.jsp           | 10      | Undocumented request attribute key `arrDriverList`                    |
| B04-11 | LOW      | getcode.jsp                 | 1       | Missing page-level comment                                            |
| B04-12 | LOW      | getcode.jsp                 | 25      | Magic string `action=reset` undocumented                              |
| B04-13 | LOW      | home.jsp                    | 1       | Missing page-level comment                                            |
| B04-14 | MEDIUM   | home.jsp                    | 53      | `isDealer` session attribute: string-typed, no comment, no null guard |
| B04-15 | MEDIUM   | home.jsp                    | 75      | Same `isDealer` issue repeated, no null guard                         |
| B04-16 | LOW      | home.jsp                    | 53,75   | Four magic routing action strings undocumented                        |
| B04-17 | LOW      | login.jsp                   | 1       | Missing page-level comment                                            |
| B04-18 | LOW      | login.jsp                   | 51      | Non-standard `Date.getTimezone()` call, no comment or polyfill note   |
| B04-19 | HIGH     | mailSuccuess.jsp            | —       | Zero-byte file; any forward to this page produces blank response      |
| B04-20 | LOW      | mod/sendmail.jsp            | 1       | Missing page-level comment                                            |
| B04-21 | LOW      | mod/sendmail.jsp            | 31      | Magic string `accountAction=send_mail` undocumented                   |
| B04-22 | LOW      | mod/sendmail.jsp            | 23,29   | Commented-out code blocks without explanation                         |
| B04-23 | MEDIUM   | mod/sendmail.jsp            | 43-50   | Dead `send()` function with broken form reference, no comment         |
| B04-24 | LOW      | privacy.jsp                 | 1       | Missing page-level comment                                            |
| B04-25 | LOW      | privacy.jsp                 | 20      | `<!-- /container -->` comment does not match the actual closing element|

**Totals:** 1 HIGH, 6 MEDIUM, 18 LOW
