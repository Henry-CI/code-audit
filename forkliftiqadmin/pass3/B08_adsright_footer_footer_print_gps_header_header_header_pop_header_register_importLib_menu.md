# Pass 3 Documentation Audit — Agent B08
**Date:** 2026-02-26
**Files audited:** 9 JSP include fragments under `src/main/webapp/includes/`

---

## Reading Evidence

---

### 1. `includes/adsright.inc.jsp`

**Full path:** `src/main/webapp/includes/adsright.inc.jsp`

**Purpose (inferred):** Renders a right-hand sidebar advertisement panel. Iterates over a session-scoped list named `sessAds`, displaying the 4th through 6th advertisement records (offset=3, length=3) as image+text blocks inside a hidden `<div id="adsright">`.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):**
- Line 10: `<%=RuntimeConf.IMG_SRC%>` — emits the base image URL from the `RuntimeConf` utility constant.

**Session attribute accesses:**
- Line 7–15: Struts `<logic:notEmpty name="sessAds">` / `<logic:iterate name="sessAds" ...>` — reads the session-scoped bean `sessAds` (a list of `AdvertisementBean` objects).

**Significant JavaScript/CSS:**
- None directly in file. CSS class `adsimg` / `adstext` applied; rendered element is `display:none` by default.

---

### 2. `includes/footer.inc.jsp`

**Full path:** `src/main/webapp/includes/footer.inc.jsp`

**Purpose (inferred):** Closes the main page layout (multiple nested `</div>` tags), renders the footer copyright line with a dynamically computed current year, provides links to the Privacy Policy (opens a Bootstrap modal) and Terms of Service (blank `href`), and includes a Bootstrap modal containing the privacy policy text via `privacyText.jsp`.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):**
- Line 2: `<%= Calendar.getInstance().get(Calendar.YEAR)%>` — outputs the current four-digit year for the copyright notice.

**Session attribute accesses:** None directly. Depends on `importLib.jsp` (line 1 `<%@ include file="../includes/importLib.jsp"%>`) for class imports including `Calendar`.

**Significant JavaScript/CSS:**
- Bootstrap modal markup (`id="privacymodal"`) triggered by `data-toggle="modal"` anchor (line 3–4).
- Closes `<body>` and `<html>` tags (lines 33–34).

---

### 3. `includes/footer_print.inc.jsp`

**Full path:** `src/main/webapp/includes/footer_print.inc.jsp`

**Purpose (inferred):** Minimal closing fragment for print-view pages — closes an open `<div>`, then closes `<body>` and `<html>`.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:** None.

---

### 4. `includes/gps_header.jsp`

**Full path:** `src/main/webapp/includes/gps_header.jsp`

**Purpose (inferred):** Intended as a GPS-specific header fragment. In its current state the entire content consists of two commented-out HTML lines: a Leaflet CSS `<link>` and a custom `ajaxStore.js` `<script>` tag. The file is effectively empty/no-op at runtime.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:**
- Line 1 (commented out): `skin/css/leaflet.css`
- Line 2 (commented out): `skin/js/ajaxStore.js`
  Both resources are disabled; the main `header.inc.jsp` loads both unconditionally.

---

### 5. `includes/header.inc.jsp`

**Full path:** `src/main/webapp/includes/header.inc.jsp`

**Purpose (inferred):** The primary HTML `<head>` fragment for the main admin application. Emits the full `<!DOCTYPE>`-equivalent conditional IE HTML element, all `<head>` metadata, page title, and loads every CSS stylesheet and JavaScript library required by the application (Bootstrap, jQuery, jQuery UI, sweet-alert, ekko-lightbox, nanoscroller, chosen, leaflet, esri-leaflet, md5, custom scripts, etc.).

**JSP scriptlet blocks (`<% %>`):** None (no standalone scriptlet blocks).

**JSP expression blocks (`<%= %>`):** None (no JSP expressions; the `RuntimeConf` import at line 1 is present but unused in this file).

**Session attribute accesses:** None.

**Significant JavaScript/CSS (all via `<link>` / `<script>` tags, lines 13–45):**
- CSS: `bootstrap.min.css`, `rvbar.css`, `sweet-alert.css`, `ekko-lightbox.min.css`, `jquery-ui.min.css`, `jquery-ui-timepicker-addon.css`, `nanoscroller.css`, `chosen.css`, `styles.css`, `print.css`, `rr-subs.css`, `strength.css`, `mobile.css`, `font-awesome.min.css`, `leaflet.css`
- JS: `jquery.min.js`, `jquery-ui.min.js`, `bootstrap.min.js`, `rvbar.js`, `sweet-alert.js`, `ekko-lightbox.min.js`, `jquery.nanoscroller.min.js`, `chosen.jquery.min.js`, `strength.js`, `ajaxSwithType.js`, `jquery.datetimepicker.js`, `jquery-ui-timepicker-addon.js`, `date.js`, `md5.js`, `scripts.js` (cache-busted via `Date.now()`), `leaflet.js`, `esri-leaflet.js`, `ajaxStore.js`
- Line 42: `document.write(...)` used to inject `scripts.js` with a cache-buster query string.

---

### 6. `includes/header_pop.inc.jsp`

**Full path:** `src/main/webapp/includes/header_pop.inc.jsp`

**Purpose (inferred):** A minimal CSS-only header fragment for popup/modal windows. Contains only an inline `<style>` block that constrains `.modal-content-form` height to a scrollable viewport-relative value. No `<html>` or `<head>` wrapper tags are included.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:**
- Lines 1–6: Inline `<style>` block defining `.modal-content-form { overflow-y: scroll; max-height: calc(100vh - 220px); }`.

---

### 7. `includes/header_register.inc.jsp`

**Full path:** `src/main/webapp/includes/header_register.inc.jsp`

**Purpose (inferred):** HTML `<head>` fragment for the registration/login pages (standalone, not the main admin layout). Sets up the page title, loads a v2 Bootstrap CSS, an older jQuery UI CSS theme (redmond 1.7.2), sweet-alert CSS, jQuery 1.7.1 from Google CDN, jQuery UI 1.7.2 custom, sweet-alert JS, and the watermark plugin. Contains inline styles for the login/registration panel appearance and an inline `$(document).ready` script that initialises watermark placeholders on elements with class `insertPhld`.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:**
- Line 12: `skin/css/v2/bootstrap.min.css` (different Bootstrap version than main header)
- Line 13: External jQuery UI CSS: `css/redmond/jquery-ui-1.7.2.custom.css`
- Line 15: jQuery 1.7.1 from Google CDN (`https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js`)
- Line 16: `js/jquery-ui-1.7.2.custom.min.js`
- Line 17: `skin/js/sweet-alert.js`
- Line 18: `js/jquery.watermark.js`
- Lines 19–56: Inline `<style>` — body background image, login panel positioning, panel-primary theming, alert/alert-danger colours.
- Lines 57–63: Inline `<script>` — `$(document).ready` applying watermark plugin to all `.insertPhld` elements using their `title` attribute.

---

### 8. `includes/importLib.jsp`

**Full path:** `src/main/webapp/includes/importLib.jsp`

**Purpose (inferred):** Central import aggregator for JSP pages. Uses `<%@ page import="..." %>` directives to make common Java classes available across all including pages, and declares the three Struts tag libraries (`struts-html`, `struts-bean`, `struts-logic`) that are used throughout the application.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**Session attribute accesses:** None (import-only file).

**Imported classes (lines 1–14):**
- `org.apache.struts.action.Action`
- `org.apache.struts.action.ActionMessage`
- `org.apache.struts.action.ActionErrors`
- `org.apache.log4j.Logger`
- `com.action.SwitchLanguageAction`
- `javax.servlet.http.Cookie`
- `java.util.Iterator`
- `java.util.ArrayList`
- `com.util.RuntimeConf`
- `com.util.InfoLogger`
- `java.util.Calendar`

**Tag library declarations (lines 16–18):** `struts-html`, `struts-bean`, `struts-logic`.

**Significant JavaScript/CSS:** None.

---

### 9. `includes/menu.inc.jsp`

**Full path:** `src/main/webapp/includes/menu.inc.jsp`

**Purpose (inferred):** The main application shell fragment. Renders the full page wrapper: top bar (logo, company switcher dropdown for multi-company users, My Account / Help / Logout links), a Help FAQ modal, and the left sidebar navigation menu. The sidebar conditionally shows a "Locations" link if `isDealer` is true and a "Dealers" link if `isSuperAdmin` is true. Opens the main content wrapper `<div>` but does not close it (paired with the footer).

**JSP scriptlet blocks (`<% %>`):** None standalone (all logic uses Struts tags).

**JSP expression blocks (`<%= %>`):**
- Line 32: `<%= RuntimeConf.ROLE_SUBCOMP %>` — used as the value comparison in a `<logic:equal>` tag to indent sub-company entries in the company dropdown.
- Line 41: `<%= session.getAttribute("sessCompId") %>` — directly reads `sessCompId` from the HTTP session to pre-select the current company in the dropdown via inline JavaScript.

**Session attribute accesses:**
- Line 17: `<bean:size id="size" name="sessArrComp"/>` — reads `sessArrComp` (list of companies for the logged-in user).
- Line 19: `<bean:write name="sessCompName"/>` — reads `sessCompName` (display name of current company).
- Line 30: `<logic:iterate name="sessArrComp" ...>` — iterates `sessArrComp`.
- Line 32: `<logic:equal name="company" property="authority" value="<%=RuntimeConf.ROLE_SUBCOMP %>">` — checks a company's `authority` property.
- Line 41: `session.getAttribute("sessCompId")` — raw session read of the current company ID.
- Line 154: `<logic:equal value="true" name="isDealer">` — reads `isDealer` session/request attribute to gate the Locations menu item.
- Line 162: `<logic:equal name="isSuperAdmin" value="true">` — reads `isSuperAdmin` to gate the Dealers menu item.

**Significant JavaScript/CSS:**
- Lines 40–42: Inline `<script>` — jQuery selector to pre-select the current company in the `<select>` dropdown using the raw `sessCompId` session value.
- Line 7: `toggler-mobile` anchor for mobile sidebar toggle.
- Bootstrap modal (`id="helpmodal"`, lines 74–124) containing a 10-item FAQ.
- Line 186: HTML comment `<!--  Start the Content -->` marking the content division.

---

## Findings

---

**B08-1 | LOW | includes/adsright.inc.jsp:1 | Missing fragment-level comment**

The file has no HTML (`<!-- -->`) or JSP (`<%-- --%>`) comment describing its purpose. A reader must infer from context that this fragment renders right-side advertisements with an offset of 3. A brief top-of-file comment explaining the offset/length parameters and the `sessAds` dependency would aid maintenance.

---

**B08-2 | LOW | includes/adsright.inc.jsp:8 | Magic numeric values without comment**

`<logic:iterate ... length="3" offset="3">` uses hard-coded literals `3` and `3` with no explanation. It is not documented why the first three advertisement records are skipped (offset=3) and only three are shown (length=3). This implies another include fragment renders the first three, but that relationship is entirely undocumented.

---

**B08-3 | LOW | includes/footer.inc.jsp:1 | Missing fragment-level comment**

No comment describes what this fragment does. It closes the main layout `<div>` structure, renders copyright with a dynamic year, and includes a privacy modal. The absence of context is particularly risky because the file opens with several closing `</div>` tags that depend on corresponding opening tags elsewhere.

---

**B08-4 | LOW | includes/footer.inc.jsp:5 | Blank href in Terms of Service link — magic empty string, no comment**

Line 5: `<a href="" target="_blank"><bean:message key="footer.term"></bean:message></a>` — the `href` is an empty string, meaning the Terms of Service link navigates nowhere. There is no comment explaining whether this is intentional (feature not yet implemented), a placeholder, or a defect. The blank href is a silent no-op that will confuse maintainers and users.

---

**B08-5 | LOW | includes/footer_print.inc.jsp:1 | Missing fragment-level comment**

The file contains only three closing HTML tags with no indication of which page or layout context it closes. A single-line comment identifying its paired header (e.g., `header_print.inc.jsp`) would prevent incorrect reuse.

---

**B08-6 | LOW | includes/gps_header.jsp:1 | Missing fragment-level comment**

The file has no comment. Its entire active content is commented-out resource links, making its purpose and usage context completely opaque. There is no explanation of why both resources are disabled, whether they are superseded by `header.inc.jsp` (which loads both unconditionally), or when/if they should be re-enabled.

---

**B08-7 | MEDIUM | includes/gps_header.jsp:1-2 | Entire file body is commented-out code with no explanation**

Both resource lines in this file are disabled HTML comments with no accompanying explanation:
```
<!-- <link rel="stylesheet" href="../skin/css/leaflet.css" /> -->
<!-- <script language="javascript" src="../skin/js/ajaxStore.js"></script> -->
```
`header.inc.jsp` already loads both `leaflet.css` and `ajaxStore.js` unconditionally, suggesting these were made redundant by a refactoring. The absence of any explanatory comment means it is impossible to determine whether: (a) the file should be deleted, (b) it is a deliberate override mechanism for GPS-specific pages, or (c) it is dead code left from an incomplete refactor. Any future developer could uncomment these lines believing they are fixing a missing resource, causing double-inclusion. The non-trivial maintenance risk and complete absence of documentation warrants MEDIUM severity.

---

**B08-8 | LOW | includes/header.inc.jsp:1 | Missing fragment-level comment**

No comment describes the fragment. Given the file loads 15 CSS files and 18 JavaScript libraries, a brief comment naming its role (e.g., "Main application HTML head: loads all CSS and JS dependencies") would significantly aid maintenance and onboarding.

---

**B08-9 | LOW | includes/header.inc.jsp:1 | Unused import — `RuntimeConf` imported but never referenced**

Line 1: `<%@ page import="com.util.RuntimeConf" %>` appears at the top of the file, but `RuntimeConf` is never used anywhere in `header.inc.jsp`. This is a minor comment/documentation gap: no note explains why the import is present, and it may mislead readers into thinking dynamic configuration values are consumed here.

---

**B08-10 | MEDIUM | includes/header.inc.jsp:42 | `document.write` cache-buster with no comment**

```javascript
<script>document.write("<script type='text/javascript' src='skin/js/scripts.js?v=" + Date.now() + "'><\/script>");</script>
```
This is the only script loaded via `document.write`; all others use straightforward `<script src="...">` tags. The technique is non-obvious (use of `document.write` is generally discouraged and behaves differently in async contexts), and no comment explains why only `scripts.js` requires a cache-busting version parameter while the other 17 scripts do not. A maintainer unfamiliar with the pattern could remove or mis-replicate it.

---

**B08-11 | LOW | includes/header_pop.inc.jsp:1 | Missing fragment-level comment**

No comment identifies which popup contexts include this fragment, or explains the significance of the `calc(100vh - 220px)` magic constant. A single-line comment noting its purpose (scrollable modal content form constraint) would suffice.

---

**B08-12 | LOW | includes/header_pop.inc.jsp:4 | Magic numeric constant `220px` without comment**

`max-height: calc(100vh - 220px)` uses a hard-coded pixel offset with no explanation of how `220px` was derived (presumably header + footer heights within the modal). If modal chrome dimensions change, this value will silently produce incorrect behaviour.

---

**B08-13 | LOW | includes/header_register.inc.jsp:1 | Missing fragment-level comment**

No comment explains that this is the header for registration/login pages rather than the main admin shell. The title tag says "FORKLIFT iQ360", which is shared with the main header, further reducing discoverability.

---

**B08-14 | MEDIUM | includes/header_register.inc.jsp:12-17 | Version mismatch between libraries with no comment**

This fragment loads Bootstrap from `skin/css/v2/bootstrap.min.css` (a different directory and likely a different version than the `skin/css/bootstrap.min.css` loaded by `header.inc.jsp`) and jQuery 1.7.1 from Google CDN together with a jQuery UI 1.7.2 custom build. The main header uses local, presumably newer, versions of these libraries. There is no comment explaining the intentional version divergence between the registration pages and the main admin pages. This is a non-trivial maintenance concern: security patches or UI updates applied to one set of assets will not affect the other.

---

**B08-15 | LOW | includes/header_register.inc.jsp:15 | External CDN dependency without comment**

Line 15 loads jQuery from `https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js` — an external Google CDN. All other assets in the application are served locally. No comment documents this deliberate externalisation or its implications (offline unavailability, CDN availability dependency, version lock to 1.7.1). jQuery 1.7.1 is a very old version (released 2011) and no longer receives security updates.

---

**B08-16 | LOW | includes/importLib.jsp:1 | Missing fragment-level comment**

No comment explains that this file is the central import aggregator for JSP pages. Developers must open the file and read all 18 directives to understand its role. A single descriptive comment would clarify intent and discourage ad-hoc duplication of imports in individual pages.

---

**B08-17 | LOW | includes/importLib.jsp:6 | Unused import — `SwitchLanguageAction` with no comment**

Line 6: `<%@ page import="com.action.SwitchLanguageAction" %>` is present with no explanation of why an Action class needs to be directly imported into JSP pages. If it is used to reference a constant, that dependency is undocumented.

---

**B08-18 | LOW | includes/menu.inc.jsp:1 | Missing fragment-level comment**

No comment describes the fragment's role as the main application shell (top bar + sidebar navigation + help modal). Given this is the largest and most structurally important of the include files, the absence of a description is particularly notable.

---

**B08-19 | LOW | includes/menu.inc.jsp:41 | Non-obvious session attribute key `sessCompId`**

```java
session.getAttribute("sessCompId")
```
The session key `sessCompId` is a raw string literal with no documentation. There is no comment explaining what type this attribute holds (presumably a numeric or string company identifier), where it is set, or what happens if it is null. The attribute is also not accessed via a typed constant (e.g., a `RuntimeConf` field), making it susceptible to silent typo-related bugs.

---

**B08-20 | LOW | includes/menu.inc.jsp:32 | Magic role constant `RuntimeConf.ROLE_SUBCOMP` without comment**

```jsp
<logic:equal name="company" property="authority" value="<%=RuntimeConf.ROLE_SUBCOMP %>">
```
The `ROLE_SUBCOMP` constant controls UI indentation of sub-company entries in the company switcher dropdown. Its meaning and the visual effect (adding three non-breaking spaces of indentation) are entirely undocumented at the point of use. Readers must navigate to `RuntimeConf` to understand what role value is being compared.

---

**B08-21 | LOW | includes/menu.inc.jsp:154 | Session attribute keys `isDealer` and `isSuperAdmin` are undocumented**

Lines 154 and 162 gate navigation menu items on `isDealer` and `isSuperAdmin` session/request attributes respectively. Neither attribute name is documented: there is no comment explaining where these boolean flags are set, what their scope is (session vs. request), or what combination of role/permissions they represent. The security implication (controlling which administrative menu items are visible) makes the lack of documentation a maintenance risk.

---

**B08-22 | MEDIUM | includes/menu.inc.jsp:40-42 | Inline script reads raw session attribute to drive UI selection — no comment**

```javascript
<script>
    $('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');
</script>
```
This inline script directly emits a session attribute value into JavaScript to pre-select the company dropdown. No comment explains the pattern or why the standard Struts `<html:select>` mechanism (which would normally handle pre-selection via the form bean) is insufficient here. Additionally, if `sessCompId` is null or contains characters that break a JavaScript string literal, this produces a client-side syntax error. The non-obvious mixing of server-side session access with inline DOM manipulation, without any comment, warrants MEDIUM severity.

---

## Summary Table

| ID | Severity | File | Line | Issue |
|----|----------|------|------|-------|
| B08-1 | LOW | adsright.inc.jsp | 1 | Missing fragment-level comment |
| B08-2 | LOW | adsright.inc.jsp | 8 | Magic `length=3` / `offset=3` without comment |
| B08-3 | LOW | footer.inc.jsp | 1 | Missing fragment-level comment |
| B08-4 | LOW | footer.inc.jsp | 5 | Blank href on Terms of Service link, no comment |
| B08-5 | LOW | footer_print.inc.jsp | 1 | Missing fragment-level comment |
| B08-6 | LOW | gps_header.jsp | 1 | Missing fragment-level comment |
| B08-7 | MEDIUM | gps_header.jsp | 1-2 | Entire file body is commented-out code with no explanation |
| B08-8 | LOW | header.inc.jsp | 1 | Missing fragment-level comment |
| B08-9 | LOW | header.inc.jsp | 1 | Unused `RuntimeConf` import, no comment |
| B08-10 | MEDIUM | header.inc.jsp | 42 | `document.write` cache-buster for `scripts.js` only — unexplained pattern |
| B08-11 | LOW | header_pop.inc.jsp | 1 | Missing fragment-level comment |
| B08-12 | LOW | header_pop.inc.jsp | 4 | Magic constant `220px` in `calc()` without comment |
| B08-13 | LOW | header_register.inc.jsp | 1 | Missing fragment-level comment |
| B08-14 | MEDIUM | header_register.inc.jsp | 12-17 | Library version divergence from main header, no comment |
| B08-15 | LOW | header_register.inc.jsp | 15 | External CDN dependency (old jQuery 1.7.1) without comment |
| B08-16 | LOW | importLib.jsp | 1 | Missing fragment-level comment |
| B08-17 | LOW | importLib.jsp | 6 | Unexplained import of `SwitchLanguageAction` into JSP layer |
| B08-18 | LOW | menu.inc.jsp | 1 | Missing fragment-level comment |
| B08-19 | LOW | menu.inc.jsp | 41 | Non-obvious session attribute key `sessCompId` undocumented |
| B08-20 | LOW | menu.inc.jsp | 32 | Magic role constant `RuntimeConf.ROLE_SUBCOMP` at point of use undocumented |
| B08-21 | LOW | menu.inc.jsp | 154,162 | Session attributes `isDealer` / `isSuperAdmin` undocumented |
| B08-22 | MEDIUM | menu.inc.jsp | 40-42 | Inline script mixes raw session access with jQuery pre-selection — no comment |

**Totals: 4 MEDIUM, 18 LOW, 0 HIGH**
