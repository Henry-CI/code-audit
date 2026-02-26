# Pass 2 Test Coverage Audit — B08 (Part 2)
**Audit Run:** 2026-02-26-01
**Agent:** B08
**Scope:** JSP include fragments — footer.inc.jsp, footer_print.inc.jsp, gps_header.jsp, header.inc.jsp, header_pop.inc.jsp, header_register.inc.jsp, importLib.jsp, menu.inc.jsp, menu_loginInfo.inc.jsp
**Test Directory Searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

---

## Test Directory — File Inventory

The test directory contains exactly four files, all unrelated to the JSP fragments under audit:

- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

Grep of all nine target filenames (without extension) against the test directory returned zero matches. No JSP rendering tests, no Mockito/Selenium/HtmlUnit coverage, and no integration tests exist for any fragment. The action classes referenced by these fragments (`SwitchCompanyAction`, `LogoutAction`, `SwitchLanguageAction`, `AdminMenuAction`) are likewise absent from the test tree.

---

## Per-File Reading Evidence

### 1. footer.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/footer.inc.jsp`
**Size:** 34 lines
**Purpose:** Closes the main page layout (multiple nested `</div>` closings), emits a copyright line, renders Privacy Policy and Terms links, and includes a Bootstrap modal containing `privacyText.jsp`.

**Scriptlet blocks:**
| Line | Expression | Description |
|------|------------|-------------|
| 1 | `<%@ include file="../includes/importLib.jsp"%>` | Static include of importLib (see §3 below) |
| 2 | `<%= Calendar.getInstance().get(Calendar.YEAR)%>` | Emits the current four-digit year into HTML |

**EL / tag expressions:**
- Line 2: `<bean:message key="footer.copyright">` — i18n label
- Line 2: `<bean:message key="footer.company">` — i18n label
- Line 4: `<bean:message key="footer.privacy">` — i18n label
- Line 5: `<bean:message key="footer.term">` — i18n label

**Forms:** None.

**External resources:** `<jsp:include page="privacyText.jsp">` (line 23) — dynamic include of privacy modal body.

**Test grep result:** Zero matches in test directory for "footer" or related action class names.

---

### 2. footer_print.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/footer_print.inc.jsp`
**Size:** 6 lines
**Purpose:** Minimal print-variant footer fragment. Closes a `<div>`, `<body>`, and `<html>` tag only. No logic whatsoever.

**Scriptlet blocks:** None.
**EL / tag expressions:** None.
**Forms:** None.
**Session attributes accessed:** None.

**Test grep result:** Zero matches in test directory for "footer_print".

---

### 3. gps_header.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/gps_header.jsp`
**Size:** 2 lines
**Purpose:** Commented-out GPS-related CSS and JS includes. The entire file consists of two HTML comments with originally referenced `leaflet.css` and `ajaxStore.js` resources.

**Scriptlet blocks:** None.
**EL / tag expressions:** None.
**Forms:** None.
**Session attributes accessed:** None.
**Active HTML:** Zero (all content commented out).

**Test grep result:** Zero matches in test directory for "gps_header".

---

### 4. header.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header.inc.jsp`
**Size:** 46 lines
**Purpose:** Full HTML `<head>` section for the main authenticated application. Declares charset, IE-compatibility, cache-control, and viewport meta tags. Loads the application title, twelve CSS files, and sixteen JavaScript files. Also includes a `document.write` pattern to cache-bust `scripts.js`.

**Scriptlet blocks:**
| Line | Expression | Description |
|------|------------|-------------|
| 1 | `<%@ page import="com.util.RuntimeConf" %>` | Page directive; RuntimeConf is imported but not used within this fragment |

**EL / tag expressions:** None.
**Forms:** None.
**Session attributes accessed:** None.

**JavaScript files loaded (all relative paths, no SRI):**
`jquery.min.js`, `jquery-ui.min.js`, `bootstrap.min.js`, `rvbar.js`, `sweet-alert.js`, `ekko-lightbox.min.js`, `jquery.nanoscroller.min.js`, `chosen.jquery.min.js`, `strength.js`, `ajaxSwithType.js`, `jquery.datetimepicker.js`, `jquery-ui-timepicker-addon.js`, `date.js`, `md5.js`, `scripts.js` (via `document.write`), `leaflet.js`, `esri-leaflet.js`, `ajaxStore.js`

**Notable patterns:**
- Line 42: `document.write("<script … src='skin/js/scripts.js?v=" + Date.now() + "'><\/script>");` — uses `document.write` to inject a script tag for cache-busting.

**Test grep result:** Zero matches in test directory for "header.inc" or "RuntimeConf".

---

### 5. header_pop.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header_pop.inc.jsp`
**Size:** 6 lines
**Purpose:** Minimal CSS fragment for pop-up/modal windows. Defines a single `.modal-content-form` style rule (`overflow-y: scroll; max-height: calc(100vh - 220px)`). No server-side logic.

**Scriptlet blocks:** None.
**EL / tag expressions:** None.
**Forms:** None.
**Session attributes accessed:** None.

**Test grep result:** Zero matches in test directory for "header_pop".

---

### 6. header_register.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header_register.inc.jsp`
**Size:** 64 lines
**Purpose:** Full HTML `<head>` section for the unauthenticated registration/login-related pages. Loads Bootstrap v2, jQuery UI 1.7.2 CSS, jQuery 1.7.1 (from Google CDN), jQuery UI 1.7.2 (local), sweet-alert, and `jquery.watermark.js`. Includes inline CSS for background image and panel styling. Includes an inline `$(document).ready` script that initializes watermark placeholders.

**Scriptlet blocks:**
| Line | Expression | Description |
|------|------------|-------------|
| 1 | `<%@ page import="com.util.RuntimeConf"%>` | Page directive; RuntimeConf imported but not used within this fragment |

**EL / tag expressions:** None.
**Forms:** None.
**Session attributes accessed:** None.

**External scripts loaded:**
- Line 15: `https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js` — loaded from Google CDN (no SRI, version pinned at 1.7.1 from 2012)

**Test grep result:** Zero matches in test directory for "header_register".

---

### 7. importLib.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/importLib.jsp`
**Size:** 17 lines
**Purpose:** Shared page-directive import file. Provides all Java class imports and Struts tag library declarations consumed by any fragment that does `<%@ include file="../includes/importLib.jsp"%>`.

**Scriptlet blocks (all `<%@ page import ... %>` directives):**
| Line | Import | Used in this fragment? |
|------|--------|----------------------|
| 1 | `org.apache.struts.action.Action` | No — declared for including pages |
| 2 | `org.apache.struts.action.ActionMessage` | No |
| 3 | `org.apache.struts.action.ActionErrors` | No |
| 4 | `org.apache.log4j.Logger` | No |
| 6 | `com.action.SwitchLanguageAction` | No — imported so including pages can call its static helpers |
| 7 | `javax.servlet.http.Cookie` | No |
| 9 | `java.util.Iterator` | No |
| 10 | `java.util.ArrayList` | No |
| 12 | `com.util.RuntimeConf` | No |
| 13 | `com.util.InfoLogger` | No |
| 14 | `java.util.Calendar` | Yes — used in footer.inc.jsp via this include |

**Tag library declarations (lines 16–18):**
- `struts-html` → prefix `html`
- `struts-bean` → prefix `bean`
- `struts-logic` → prefix `logic`

**EL / tag expressions:** None (pure directives).
**Forms:** None.
**Session attributes accessed:** None.

**Test grep result:** Zero matches in test directory for "importLib" or "SwitchLanguageAction".

---

### 8. menu.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu.inc.jsp`
**Size:** 187 lines
**Purpose:** Main authenticated application shell. Renders the top navigation bar (company switcher, My Account link, Help modal, Logout link) and the left sidebar navigation menu (Home, Vehicles, Drivers, Checklist, Locations, Dealers, Reports, Users). Conditionally shows Dealers menu item for Super Admin and Locations for Dealer role. Also renders a Help FAQ modal with an external support link.

**Scriptlet blocks:**
| Line | Expression | Description |
|------|------------|-------------|
| 1 | `<%@ include file="../includes/importLib.jsp" %>` | Static include of importLib |
| 32 | `value="<%=RuntimeConf.ROLE_SUBCOMP %>"` | Embeds Java static constant into a Struts `logic:equal` tag attribute |
| 41 | `$('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');` | Raw scriptlet expression embedding session attribute value into JavaScript string literal |

**EL / tag expressions and session attributes accessed:**
| Line | Expression | Session/Request Attribute |
|------|------------|--------------------------|
| 17 | `<bean:size id="size" name="sessArrComp"/>` | Session: `sessArrComp` (company list) |
| 18 | `<logic:equal name="size" value="1">` | Derived from `sessArrComp` |
| 19 | `<bean:write name="sessCompName"/>` | Session: `sessCompName` (company display name) |
| 21 | `<logic:greaterThan name="size" value="1">` | Derived from `sessArrComp` |
| 30 | `<logic:iterate name="sessArrComp" id="company" ...>` | Session: `sessArrComp` |
| 31 | `<bean:write name="company" property="id"/>` | Iterated CompanyBean.id |
| 35 | `<bean:write name="company" property="name"/>` | Iterated CompanyBean.name |
| 41 | `session.getAttribute("sessCompId")` | Session: `sessCompId` |
| 154 | `<logic:equal value="true" name="isDealer">` | Request/Session: `isDealer` |
| 162 | `<logic:equal name="isSuperAdmin" value="true">` | Session: `isSuperAdmin` |

**Forms and action URLs:**
| Line | Form action | Method | Purpose |
|------|------------|--------|---------|
| 24–39 | `switchCompany.do` | POST | Company switcher — submitted automatically on `<select>` change |

**External URLs:**
- Lines 116–117: `http://forklift-iq360.kayako.com/` — hardcoded plain-HTTP external support system URL

**Test grep result:** Zero matches in test directory for "menu.inc", "switchCompany", or "AdminMenuAction".

---

### 9. menu_loginInfo.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_loginInfo.inc.jsp`
**Size:** 55 lines
**Purpose:** Legacy-style header/navigation fragment for an older UI layout. Renders a banner image with clickable image-map links, a company name and driver name display from session, and a logout form.

**Scriptlet blocks:**
| Line | Expression | Description |
|------|------------|-------------|
| 1 | `<%@ taglib uri="/tags/struts-html" prefix="html" %>` | Taglib directive |
| 2 | `<%@ taglib uri="/tags/struts-bean" prefix="bean" %>` | Taglib directive |
| 3 | `<%@ taglib uri="/tags/struts-logic" prefix="logic" %>` | Taglib directive |
| 5 | `<%@ page import="com.util.RuntimeConf,com.bean.CompanyBean" %>` | Page import |
| 6 | `<%@ page import="com.util.RuntimeConf,com.bean.DriverBean" %>` | Page import — duplicate `RuntimeConf` import |
| 7 | `<%@ page import="java.util.ArrayList" %>` | Page import |

**EL / tag expressions and session attributes accessed:**
| Line | Expression | Session Attribute |
|------|------------|------------------|
| 31–35 | `<logic:notEmpty name="sessArrComp">` / `<logic:iterate ... name="sessArrComp" scope="session">` | Session: `sessArrComp` (company list) |
| 33 | `<bean:write property="name" name="compRecord">` | CompanyBean.name from `sessArrComp` |
| 39–43 | `<logic:notEmpty name="arrDriver">` / `<logic:iterate ... name="arrDriver" scope="session">` | Session: `arrDriver` (driver list) |
| 41 | `<bean:write property="first_name" name="driverRecord">` | DriverBean.first_name from `arrDriver` |
| 41 | `<bean:write property="last_name" name="driverRecord">` | DriverBean.last_name from `arrDriver` |

**Forms and action URLs:**
| Line | Form action | Method | Name | Purpose |
|------|------------|--------|------|---------|
| 46–48 | `logout.do` | POST | `logoutform` | JavaScript-triggered logout via `document.logoutform.submit()` |

**HTML syntax defect:**
- Line 18: `href="http://www.prestart.com.au""` — trailing extra double-quote in the image map `<area>` href attribute (same defect also present in `menu_register.inc.jsp` and `menu_systemadmin.inc.jsp`, but those are out of scope for this report).

**Stray tag:**
- Line 52: `</form>` closing tag with no corresponding opening `<form>` tag within this fragment (the `logoutform` was opened on line 46 and closed on line 48; this is a dangling close tag).

**Test grep result:** Zero matches in test directory for "menu_loginInfo", "logout.do", or "LogoutAction".

---

## Findings

### B08-01
**Severity:** HIGH
**File:** `menu.inc.jsp`, line 41
**Category:** Unescaped output of session attribute into JavaScript context (potential stored XSS)

The session attribute `sessCompId` is written directly into a JavaScript string literal without any escaping:

```jsp
$('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');
```

`sessCompId` is set from a database-sourced company ID (`LoginAction.java` line 61, `CompanySessionSwitcher.java` line 30). While the value is typically numeric at login time, any crafted or manipulated value that reaches the session (e.g., via a compromised admin account, a session fixation, or a Struts action that stores an unsanitised string) would be emitted unescaped into a JavaScript string. A value containing `'` would break out of the string, and a value such as `'; alert(1);//` would execute arbitrary JavaScript. The `sessCompId` is never validated or escaped before being placed into this JS context. No test verifies this rendering path.

---

### B08-02
**Severity:** HIGH
**File:** `menu.inc.jsp`, line 31
**Category:** Unescaped bean output inside HTML attribute value (attribute injection / potential XSS)

The `company.id` property is interpolated directly into an HTML attribute value without using `html:option` (which would handle escaping):

```jsp
<option value="<bean:write name="company" property="id"/>">
```

This construction uses raw double-quotes to delimit both the outer `value="..."` attribute and the inner `<bean:write .../>` tag. If the `id` property ever contains a double-quote character, the HTML attribute closes prematurely, enabling attribute injection. While integer IDs are expected, the pattern is fragile and untested. The correct Struts pattern is `<html:option>` or `<html:options>`.

---

### B08-03
**Severity:** MEDIUM
**File:** `menu.inc.jsp`, lines 17–19 and 154/162
**Category:** Missing null-check on session attributes used to drive conditional rendering and authorization display

`<bean:size id="size" name="sessArrComp"/>` (line 17), `<logic:equal name="isDealer">` (line 154), and `<logic:equal name="isSuperAdmin">` (line 162) all read session attributes without a null guard. If the session is present but `sessArrComp` was not populated (e.g., after session recovery, partial login failure, or a future code path that forgets to populate it), Struts `bean:size` throws a `JspException` due to a missing bean, surfacing a raw exception to the user. Similarly, `isDealer` and `isSuperAdmin` are set in `LoginAction` but are not guaranteed to survive all session-switching or impersonation paths. There are no tests exercising these null/missing-attribute conditions.

---

### B08-04
**Severity:** MEDIUM
**File:** `menu.inc.jsp`, lines 24–42
**Category:** No CSRF protection on the company-switching form

The `switchCompany.do` form is submitted automatically on `<select>` change with no synchroniser token, hidden CSRF field, or any equivalent protection:

```jsp
<html:form method="post" action="switchCompany.do">
    <html:select ... onchange="this.form.submit()">
```

`web.xml` declares only a character-encoding filter; there is no CSRF filter. `SwitchCompanyAction.java` performs no CSRF check. An attacker who can get an authenticated super-admin or dealer user to visit a crafted page could silently switch them to a different company context. No tests exist to verify CSRF resistance.

---

### B08-05
**Severity:** MEDIUM
**File:** `menu_loginInfo.inc.jsp`, lines 39–43
**Category:** Unescaped driver first/last name output (potential stored XSS)

Driver first and last names from the session-scoped `arrDriver` list are emitted with `<bean:write>` without `filter="false"` being explicitly set to false, which means Struts 1 will apply its default HTML filtering. However, the default `bean:write` filter only escapes `<`, `>`, `&`, `"`, `'` for HTML body context. Driver names entered with crafted values (e.g., names containing `<script>` or JavaScript event attributes) could still produce functional XSS in older Struts 1 versions whose `bean:write` filter is incomplete or disabled by configuration. No tests verify that names with HTML special characters are rendered safely. This should be confirmed against the exact Struts 1 version in use.

---

### B08-06
**Severity:** MEDIUM
**File:** `menu.inc.jsp`, lines 19 and 35
**Category:** Unescaped company name output (potential stored XSS)

`<bean:write name="sessCompName"/>` (line 19) and `<bean:write name="company" property="name"/>` (line 35) emit company display names without `filter="false"`. Struts 1's default `bean:write` HTML-encodes HTML characters, but the concern is the same as B08-05: correctness depends on the exact version of Struts 1 deployed and its default filter configuration. Company names are admin-supplied strings that are stored in and retrieved from the database. No test validates that a company name containing HTML is correctly escaped in the rendered output.

---

### B08-07
**Severity:** MEDIUM
**File:** `importLib.jsp`, lines 1–14
**Category:** Action class imported directly into view layer (untestable coupling)

`importLib.jsp` contains `<%@ page import="com.action.SwitchLanguageAction" %>` (line 6). This imports an Action class — a controller-layer concern — into a shared view-layer import file. The import is used transitively by `footer.inc.jsp` and `menu.inc.jsp` (via `<%@ include file="../includes/importLib.jsp"%>`), meaning every page that includes `importLib.jsp` has a compile-time dependency on the Action class. This couples view compilation to controller internals, makes the dependency non-obvious, and cannot be tested via unit tests of the JSP in isolation. Inspecting the generated `work/` sources confirms this propagation.

---

### B08-08
**Severity:** MEDIUM
**File:** `header_register.inc.jsp`, line 15
**Category:** Outdated third-party library loaded from external CDN without Subresource Integrity (SRI)

jQuery 1.7.1 (released 2012) is loaded from `ajax.googleapis.com` with no `integrity` or `crossorigin` attribute:

```html
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
```

jQuery 1.7.1 has multiple known security vulnerabilities (including XSS in `.html()`, `.append()`, and `.load()` calls). Absence of SRI means that if the CDN were compromised, malicious script would execute with no client-side defence. The registration/login pages are the most exposed surface as they are reachable without authentication. No tests verify library integrity.

---

### B08-09
**Severity:** LOW
**File:** `menu.inc.jsp`, lines 116–117
**Category:** Hardcoded plain-HTTP external URL (mixed-content / information disclosure)

The Help modal contains a hardcoded `http://` (not `https://`) URL pointing to an external support system:

```html
<a href="http://forklift-iq360.kayako.com/" target="_blank">
```

Modern browsers will block or warn on mixed-content HTTP links loaded from an HTTPS page. The URL also exposes the name of the support ticket system vendor and the support-site subdomain to all authenticated users. If the support URL changes or the domain expires, there is no configuration mechanism to update it without a code deployment.

---

### B08-10
**Severity:** LOW
**File:** `header.inc.jsp`, line 42
**Category:** Use of `document.write` for script injection

The cache-busting pattern for `scripts.js` uses `document.write`:

```js
document.write("<script type='text/javascript' src='skin/js/scripts.js?v=" + Date.now() + "'><\/script>");
```

`document.write` is deprecated in modern browsers, can block the HTML parser, and is disallowed under Content Security Policy (CSP). While `Date.now()` is not user-controlled here, the pattern sets a precedent and would need to be removed if CSP is ever introduced. There is no test exercising script loading order or cache-busting correctness.

---

### B08-11
**Severity:** LOW
**File:** `menu_loginInfo.inc.jsp`, lines 5–6
**Category:** Duplicate import of `RuntimeConf`

The file contains two `<%@ page import %>` directives that both import `com.util.RuntimeConf`:

```jsp
<%@ page import="com.util.RuntimeConf,com.bean.CompanyBean" %>
<%@ page import="com.util.RuntimeConf,com.bean.DriverBean" %>
```

This is a compilation warning in most servlet containers and indicates copy-paste development practice. `RuntimeConf` is not used anywhere in this file.

---

### B08-12
**Severity:** LOW
**File:** `menu_loginInfo.inc.jsp`, line 18
**Category:** HTML syntax error — stray double-quote in `href` attribute

The `<area>` element for the PreStart banner link contains a trailing double-quote that is not part of the URL:

```html
<area shape="rect" coords="0,5,447,67" href="http://www.prestart.com.au"" target='_blank' alt="PreStart" />
```

The extra `"` after the URL terminates the `href` attribute prematurely, leaving the bare second `"` as unparsed content. This is a well-formed HTML violation. Browsers may repair it silently, but the rendered link target is unreliable. The same defect appears in at least two other out-of-scope include files (`menu_register.inc.jsp`, `menu_systemadmin.inc.jsp`), suggesting a systemic copy-paste origin.

---

### B08-13
**Severity:** LOW
**File:** `menu_loginInfo.inc.jsp`, line 52
**Category:** Stray `</form>` closing tag

A bare `</form>` tag appears on line 52 with no corresponding opening `<form>` tag after the `logoutform` form (which was opened on line 46 and properly closed on line 48). This dangling close tag is invalid HTML and may confuse browser parsers when nesting this fragment inside a parent page that itself contains a `<form>`.

---

### B08-14
**Severity:** LOW
**File:** `importLib.jsp`, lines 4, 9, 10, 13
**Category:** Unused imports create dead coupling

Four imports declared in `importLib.jsp` are not used in any of the audited include files that consume it:

- `org.apache.log4j.Logger` (line 4) — imported but no `Logger` variable is created in these fragments
- `com.util.InfoLogger` (line 13) — same as above
- `java.util.Iterator` (line 9) — not referenced
- `java.util.ArrayList` (line 10) — not referenced in the fragments that include importLib

These imports increase compilation surface, can mask intent, and cannot be verified for necessity without a full transitive include analysis.

---

### B08-15
**Severity:** INFO
**File:** `gps_header.jsp`
**Category:** Dead file — entirely commented out

The entire content of `gps_header.jsp` is commented-out HTML. The file provides no functionality. If it is still included by any page, it adds parse overhead for zero benefit. If it is not included anywhere, it is orphaned dead code that should be removed from the repository.

---

### B08-16
**Severity:** INFO
**File:** `header.inc.jsp`, `header_register.inc.jsp`
**Category:** No HTTP security headers set

Neither header file sets any security-related HTTP response headers (`Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`, `Referrer-Policy`). The `web.xml` declares only a character-encoding filter with no security-header filter. All header concerns are delegated to the server/proxy layer, but there is no evidence of configuration at that layer within the repository. This is especially relevant given the mix of inline scripts in `header.inc.jsp` (line 42) and `header_register.inc.jsp` (lines 57–63).

---

### B08-17
**Severity:** INFO
**File:** `menu.inc.jsp`, line 162
**Category:** Authorization gate relies solely on session attribute comparison with no fallback logging or alerting

The Dealers menu item is gated by `<logic:equal name="isSuperAdmin" value="true">`. If `isSuperAdmin` is `null` (unset session), Struts `logic:equal` treats the bean as not found and renders nothing — silently suppressing the menu item rather than raising an error. This fail-closed behaviour is acceptable for UI display, but there is no logging, audit trail, or test to confirm the behaviour. An attacker who can manipulate session attributes (e.g., via deserialization) and set `isSuperAdmin` to `"true"` would gain access to the Dealers menu item. The actual action-level authorization in `AdminDealerAction.java` (`if (session.getAttribute("isSuperAdmin").equals(false)) return;`) also deserializes the attribute without a null-check and uses `.equals(false)` rather than `!Boolean.TRUE.equals(...)`, but that is a finding for the action-class audit.

---

## Coverage Gap Summary

| File | Test coverage | Primary risk |
|------|--------------|--------------|
| footer.inc.jsp | None | Untested scriptlet year logic; privacy modal include |
| footer_print.inc.jsp | None | No logic; risk negligible |
| gps_header.jsp | None | Dead file |
| header.inc.jsp | None | `document.write` script injection; no CSP; no SRI on local assets |
| header_pop.inc.jsp | None | No logic; risk negligible |
| header_register.inc.jsp | None | Outdated jQuery 1.7.1 from CDN without SRI |
| importLib.jsp | None | Action class import in view layer; unused imports |
| menu.inc.jsp | None | Raw session attribute in JS (B08-01); attribute injection (B08-02); no CSRF on form (B08-04); hardcoded HTTP URL |
| menu_loginInfo.inc.jsp | None | Duplicate imports; HTML syntax errors; stray close tag |

Zero tests exist across the entire test directory (`src/test/java/`) for any JSP fragment, any Struts action invoked by these fragments, or any session attribute population path exercised through these includes. All findings above are untested.
