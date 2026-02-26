# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** B09
**Scope:** JSP fragments – menu_popup.inc.jsp, menu_print.inc.jsp, menu_register.inc.jsp, menu_systemadmin.inc.jsp, privacyText.jsp, tilesTemplate.jsp, tilesTemplateHeader.jsp, index.jsp

---

## Methodology

1. Each JSP file was read in full.
2. The test directory (`src/test/java/`) was grepped exhaustively for every filename stem (`menu_popup`, `menu_print`, `menu_register`, `menu_systemadmin`, `privacyText`, `tilesTemplate`, `tilesTemplateHeader`, `index`) and for every session attribute name referenced by these JSPs (`sessMenu`, `arryEntity`, `menuRecord`, `entityRecord`).
3. `struts-config.xml`, `tiles-defs.xml`, `importLib.jsp`, and the relevant action classes (`SwitchLanguageAction`, `AdminMenuAction`) were examined for context.

**Test files found in scope:** NONE

Grep for every filename stem and all session attribute keys returned zero results in `src/test/java/`. The only existing test files in the project are:

- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None have any relationship to the JSP view layer.

---

## Reading Evidence

---

### File 1: `menu_popup.inc.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_popup.inc.jsp`

**Apparent purpose:** Intended as a popup navigation variant, based on its filename and the naming convention established by `header_pop.inc.jsp` and the popup tile definitions in `tiles-defs.xml`.

**File content:** The file is **completely empty** (0 bytes, confirmed by `wc -c`). There is no content, no scriptlets, no EL expressions, no HTML, no imports.

**Scriptlet blocks (`<% %>`):** None — file is empty.

**EL expressions (`${}`):** None — file is empty.

**Session/request attributes accessed:** None.

**Forms and action URLs:** None.

**Test directory grep result:** No matches for `menu_popup` in `src/test/java/`.

**Tiles reference:** No definition in `tiles-defs.xml` references this file. The popup header slot in all popup tile definitions is filled by `/includes/header_pop.inc.jsp`, not this file.

---

### File 2: `menu_print.inc.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_print.inc.jsp`

**Apparent purpose:** Navigation shell fragment for a print-view popup. The `onload` handler triggers the browser print dialog and closes the window immediately. This file provides the `<body>` opening tag and print trigger for print-mode pages.

**File content (full, 5 lines):**

```
Line 1:  <%@ taglib uri="/tags/struts-html" prefix="html" %>
Line 2:  <%@ taglib uri="/tags/struts-bean" prefix="bean" %>
Line 3:  <%@ taglib uri="/tags/struts-logic" prefix="logic" %>
Line 4:  <%@ page import="com.util.RuntimeConf" %>
Line 5:  <body onload="print('document');window.close();"><body>
```

**Scriptlet blocks (`<% %>`):** None.

**EL expressions (`${}`):** None.

**Session/request attributes accessed:** None explicitly in this file.

**Forms and action URLs:** None.

**JavaScript on line 5:**
- `print('document')` — called within `onload`. The browser `print()` / `window.print()` function takes no arguments; the string `'document'` is silently ignored.
- `window.close()` — closes the window immediately after the print dialog is triggered.
- The same line contains two consecutive `<body>` opening tags: `<body onload="..."><body>`. This is invalid HTML.

**Imports on line 4:** `com.util.RuntimeConf` is imported but never referenced in the file body.

**Test directory grep result:** No matches for `menu_print` in `src/test/java/`.

---

### File 3: `menu_register.inc.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`

**Apparent purpose:** Navigation header for the registration workflow. Renders the application banner only; contains no navigation links and no session-dependent content. Used by `adminRegiserDefinition` (note the typo in the tile name) via `header_register.inc.jsp` — though that header file is different; this file is referenced by tiles-defs.xml in `adminRegiserDefinition`:

```xml
<put name="header" value="/includes/header_register.inc.jsp"/>
```

`header_register.inc.jsp` itself includes `menu_register.inc.jsp` as its body fragment.

**File content (full, 30 lines):**

```
Line 1:  <%@ taglib uri="/tags/struts-html" prefix="html" %>
Line 2:  <%@ taglib uri="/tags/struts-bean" prefix="bean" %>
Line 3:  <%@ taglib uri="/tags/struts-logic" prefix="logic" %>
Line 4:  <%@ page import="com.util.RuntimeConf" %>
Line 5:  <%@ page import="com.action.SwitchLanguageAction" %>
Line 6:  <%@ page import="javax.servlet.http.Cookie" %>
Lines 8–30: <body> ... banner table with image map and two <area> elements ... <div id="adcontent">
```

**Scriptlet blocks (`<% %>`):** None.

**EL expressions (`${}`):** None.

**Session/request attributes accessed:** None.

**Forms and action URLs:** None.

**Key observations:**
- Line 4–6: Three `<%@ page import %>` declarations for `RuntimeConf`, `SwitchLanguageAction`, and `Cookie`. None of these classes are referenced anywhere in the file body. All three are dead imports.
- Line 18: `href="http://www.prestart.com.au""` — an extraneous double-quote follows the closing quote of the `href` value, producing a markup syntax error.
- Line 19: `href="http://www.collectiveintelligence.com.au"` — correctly formed.
- Both `<area>` elements use `target='_blank'` without `rel="noopener noreferrer"`.

**Test directory grep result:** No matches for `menu_register` in `src/test/java/`.

---

### File 4: `menu_systemadmin.inc.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`

**Apparent purpose:** Navigation header for a system-admin context. Renders a Bootstrap nav-pills bar whose menu items are dynamically built from the `sessMenu` session attribute (a collection of `MenuBean` objects). Also displays the entity name from the `arryEntity` session attribute. Provides a logout link to `adminmenu.do?action=quit`.

**File content (full, 60 lines):**

```
Line 1:  <%@ taglib uri="/tags/struts-html" prefix="html" %>
Line 2:  <%@ taglib uri="/tags/struts-bean" prefix="bean" %>
Line 3:  <%@ taglib uri="/tags/struts-logic" prefix="logic" %>
Line 4:
Line 5:  <%@ page import="com.util.RuntimeConf" %>
Lines 6–60: <body> ... nav-pills menu ... </div>
```

**Scriptlet blocks (`<% %>`):** None.

**EL expressions (`${}`):** None. All dynamic output uses Struts 1.x tags (`bean:write`, `logic:iterate`, `bean:message`).

**Session/request attributes accessed:**

| Attribute | Struts tag | Scope | Line(s) | Usage |
|-----------|-----------|-------|---------|-------|
| `sessMenu` | `<logic:notEmpty name="sessMenu">` | implicit (all scopes) | 38 | Guards iteration of menu items |
| `sessMenu` | `<logic:iterate name="sessMenu" id="menuRecord" type="com.bean.MenuBean">` | implicit | 39 | Iterates to build nav links |
| `menuRecord.action` | `<bean:write property="action" name="menuRecord" />` | request (loop var) | 40 | Written into `href` attribute query string |
| `menuRecord.description` | `<bean:write property="description" name="menuRecord" />` | request (loop var) | 40 | Written as link text |
| `arryEntity` | `<logic:notEmpty name="arryEntity">` | implicit | 51 | Guards iteration of entity records |
| `arryEntity` | `<logic:iterate id="entityRecord" name="arryEntity" length="1" type="com.bean.EntityBean" scope="session">` | session | 52 | Reads entity name |
| `entityRecord.name` | `<bean:write property="name" name="entityRecord">` | request (loop var) | 53 | Written as entity display name |

**Forms and action URLs:**
- `href="adminmenu.do?action=dashboard"` (line 31) — home nav link
- `href="adminmenu.do?action=<bean:write property="action" name="menuRecord" />"` (line 40) — dynamic menu link; the `action` property value from the database is interpolated directly into the URL query string and `href` attribute context
- `href="adminmenu.do?action=quit"` (line 45) — logout link

**Other markup issues:**
- Line 16 (inside `map` element): `href="http://www.prestart.com.au""` — same double-quote syntax error as in `menu_register.inc.jsp`.
- Both `<area>` targets use `target='_blank'` without `rel="noopener noreferrer"`.

**Import on line 5:** `com.util.RuntimeConf` imported but never referenced in the file body. Dead import.

**Test directory grep result:** No matches for `menu_systemadmin`, `sessMenu`, or `arryEntity` in `src/test/java/`.

**sessMenu / arryEntity origin:** A full search of `src/main/java/` for `setAttribute` calls using the string `"sessMenu"` or `"arryEntity"` returned no results. These session attributes have no discoverable setter in the current source tree. Their population path is undocumented.

---

### File 5: `privacyText.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/privacyText.jsp`

**Apparent purpose:** Static GDPR/privacy policy text fragment. Pure HTML prose included by `html-jsp/privacy.jsp` and (via tiles) the `privacyDefinition` tile. Contains no scriptlets, EL, forms, or JavaScript.

**File content:** 353 lines of HTML `<p>` paragraphs containing the Collective Intelligence Group privacy policy text, last updated "21st May 2018" (line 12).

**Scriptlet blocks (`<% %>`):** None.

**EL expressions (`${}`):** None.

**Session/request attributes accessed:** None.

**Forms and action URLs:** None.

**Notable content:**
- Policy last-updated date: `21st May 2018` (line 12) — hardcoded and stale by approximately 8 years.
- Production URLs embedded as plain text: `https://fms.fleetiq360.com`, `https://fms.fleetiq360.com/fleetfocus`, `https://fms.fleetiq360.com/digitaldashboard`, `https://pandora.fleetiq360.com/PandoraAdmin`, `www.ciiquk.com`, `www.thecollectiveintelligencegroup.com` (lines 32–43).
- Physical mailing address, phone number (`01460 259101`), and email address (`dp@ciiquk.com`) hardcoded in the committed source file (lines 322–331).
- Unclosed `<p>` tags at lines 211, 214, 222, 260, 264, 308 — malformed HTML.

**Test directory grep result:** No matches for `privacyText` or `privacy` in `src/test/java/`.

---

### File 6: `tilesTemplate.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplate.jsp`

**Apparent purpose:** Root Struts Tiles layout template for all authenticated admin-area and fleet-check pages. Composes four named regions (`header`, `navigation`, `content`, `footer`) via `<tiles:insert>`. Used directly by `adminDefinition`, `fleetcheckDefinition`, and `fleetcheckDashboardDefinition`, and indirectly (via extension) by the majority of all other tile definitions in `tiles-defs.xml`.

**File content (full, 9 lines):**

```
Line 1:   <%@ taglib uri="/tags/struts-tiles" prefix="tiles"%>
Line 2:   <%@ page contentType="text/html;charset=UTF-8"%>
Line 3:
Line 4:   <!DOCTYPE html>
Line 5:
Line 6:   <tiles:insert attribute="header"/>
Line 7:   <tiles:insert attribute="navigation"/>
Line 8:   <tiles:insert attribute="content"/>
Line 9:   <tiles:insert attribute="footer"/>
```

**Scriptlet blocks (`<% %>`):** None.

**EL expressions (`${}`):** None.

**Session/request attributes accessed:** None directly. All content is injected via the Tiles framework from `tiles-defs.xml` definitions.

**Forms and action URLs:** None in this file.

**Tile regions declared:** `header`, `navigation`, `content`, `footer`. All four must be resolved by the tile definition at render time.

**Test directory grep result:** No matches for `tilesTemplate` in `src/test/java/`.

**Tiles-defs.xml usage:**
- `adminDefinition` (path): sets all four attributes; inherited by 30+ child definitions
- `fleetcheckDefinition` (path): sets `header`, `navigation`, `content`, `footer` directly
- `fleetcheckDashboardDefinition` (path): same

**Structural observation:** No `<html>`, `<head>`, or `<body>` wrapper is provided by this template itself. These must come from the `header` fragment (`header.inc.jsp`). The `<!DOCTYPE html>` declaration on line 4 appears before `<tiles:insert attribute="header"/>`, which itself will emit `<html><head>...</head><body>`. This means the `DOCTYPE` is placed correctly above the `<html>` tag, but this structure is fully dependent on the assembled header fragment — never independently tested.

---

### File 7: `tilesTemplateHeader.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplateHeader.jsp`

**Apparent purpose:** Reduced Struts Tiles layout template for login-flow and popup/modal pages. Composes only two named regions (`header` and `content`). Used directly by `loginDefinition` and indirectly (via extension) by all popup, edit-panel, and drill-down tile definitions.

**File content (full, 7 lines):**

```
Line 1:   <%@ taglib uri="/tags/struts-tiles" prefix="tiles"%>
Line 2:   <%@ page contentType="text/html;charset=UTF-8"%>
Line 3:
Line 4:   <!DOCTYPE html>
Line 5:
Line 6:   <tiles:insert attribute="header"/>
Line 7:   <tiles:insert attribute="content"/>
```

**Scriptlet blocks (`<% %>`):** None.

**EL expressions (`${}`):** None.

**Session/request attributes accessed:** None directly.

**Forms and action URLs:** None in this file.

**Tile regions declared:** `header`, `content`. Navigation and footer are absent by design (popup/modal context).

**Test directory grep result:** No matches for `tilesTemplateHeader` in `src/test/java/`.

**Tiles-defs.xml usage:** `loginDefinition` (base path), extended by 30+ definitions including all `extends="loginDefinition"` definitions:
`adminJobDefinition`, `driverJobDetailsDefinition`, `adminChecklistEditDefinition`, `adminRegiserDefinition`, `OperatorEditDefinition`, `UserEditDefinition`, `OperatorTrainingDefinition`, `OperatorSubscriptionDefinition`, `OperatorVehicleDefinition`, `OperatorInviteDefinition`, `AdminAlertDefinition`, `UnitEditDefinition`, `UnitServiceDefinition`, `UnitImpactDefinition`, `UnitAssignmentDefinition`, `UnitAccessDefinition`, `AccountProfileDefinition`, `AccountSubscriptionDefinition`, `AccountSettingsDefinition`, `AccountManufacturersDefinition`, `successRegisterDefinition`, `resetPassDefinition`, `getCodeDefinition`, `dealerCompaniesAddDefinition`, and others.

---

### File 8: `index.jsp`

**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/index.jsp`

**Apparent purpose:** Root entry point of the web application. The sole purpose of this file is to immediately redirect any request to the application's root URL (`/`) onward to the `welcome` global forward.

**File content (full, 2 lines):**

```
Line 1:  <%@ include file="includes/importLib.jsp"%>
Line 2:  <logic:redirect forward="welcome"></logic:redirect>
```

**Scriptlet blocks (`<% %>`):** None.

**EL expressions (`${}`):** None.

**Session/request attributes accessed:** None in this file. The static include of `importLib.jsp` (line 1) pulls in imports for `SwitchLanguageAction`, `Cookie`, `RuntimeConf`, `InfoLogger`, `Calendar`, `Iterator`, `ArrayList`, and the three Struts taglibs. None of these are used in `index.jsp` itself; they are included solely because `importLib.jsp` is a shared import header for other JSPs that actually use those classes.

**Forms and action URLs:**
- `<logic:redirect forward="welcome">` — Struts 1.x global forward `welcome` resolves (per `struts-config.xml` line 57) to `/welcome.do`, which is handled by `com.action.WelcomeAction`. `WelcomeAction` forwards to `loginDefinition` (the login page) regardless of session state.

**Test directory grep result:** No matches for `index` in `src/test/java/`.

---

## Coverage Gap Summary

**Zero test coverage exists for all eight files in scope.** The four test classes in the project (`UnitCalibrationImpactFilterTest`, `UnitCalibrationTest`, `UnitCalibratorTest`, `ImpactUtilTest`) are entirely unrelated to the web/view layer. No Mock MVC, Selenium, HtmlUnit, or JSP compilation test exists anywhere in `src/test/java/`.

The following categories of untested behaviour were identified:

| Category | Files affected |
|----------|---------------|
| Unescaped DB-sourced output into HTML/URL attribute context | `menu_systemadmin.inc.jsp` |
| Session attribute with undocumented/untraceable setter | `menu_systemadmin.inc.jsp` |
| Unused JSP imports (dead compile-time dependencies) | `menu_print.inc.jsp`, `menu_register.inc.jsp`, `menu_systemadmin.inc.jsp` |
| Invalid HTML (duplicate tags, unclosed tags, syntax errors) | `menu_print.inc.jsp`, `menu_register.inc.jsp`, `menu_systemadmin.inc.jsp`, `privacyText.jsp` |
| Tiles assembly with missing-attribute behaviour | `tilesTemplate.jsp`, `tilesTemplateHeader.jsp` |
| Root redirect correctness and authenticated-user handling | `index.jsp` |
| Empty placeholder file with no documented intent | `menu_popup.inc.jsp` |
| Hardcoded PII and production system URLs in committed file | `privacyText.jsp` |
| target=_blank without rel=noopener/noreferrer | `menu_register.inc.jsp`, `menu_systemadmin.inc.jsp` |

---

## Findings

---

**B09-1 | Severity: HIGH | menu_systemadmin.inc.jsp — DB-sourced values written unencoded into href attribute and link text (stored XSS)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`, line 40.

```jsp
<li><a href="adminmenu.do?action=<bean:write property="action" name="menuRecord" />">
    <bean:write property="description" name="menuRecord" />
</a></li>
```

`MenuBean.action` and `MenuBean.description` originate from the `sessMenu` session attribute, which is populated from the database (via `MenuDAO.getAllMenu()`). Two risks exist:

1. **`action` property in href context:** The value is interpolated inside the already-open `href="..."` attribute. While Struts 1.x `<bean:write>` defaults to `filter=true` (which HTML-encodes `<`, `>`, `&`, `"`), the inner double-quotes on the `<bean:write>` tags themselves will break the outer `href="..."` attribute in the as-written markup — the rendered output becomes:
   ```html
   href="adminmenu.do?action=<bean:write property="action" .../>
   ```
   The `property="action"` attribute of the tag uses the same double-quote character that delimits `href="..."`, causing the `href` to be prematurely terminated by the parser at the `property=` boundary. An attacker controlling `MenuBean.action` via the database can inject arbitrary attributes or event handlers.

2. **`description` property as link text:** If `description` contains unfiltered HTML (e.g., `<img src=x onerror=alert(1)>`), it is rendered as raw HTML in link text. The `filter=true` default in `<bean:write>` mitigates standard XSS characters but does not protect against all injection vectors (e.g., Unicode bypasses, URL-encoded payloads that are decoded client-side).

No test validates the content of `sessMenu` items at render time, and no sanitisation occurs before the data is placed into session.

---

**B09-2 | Severity: HIGH | menu_systemadmin.inc.jsp — sessMenu and arryEntity session attributes have no discoverable setter (phantom session state)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`, lines 38–55.

```jsp
<logic:notEmpty name="sessMenu">
    <logic:iterate name="sessMenu" id="menuRecord" type="com.bean.MenuBean">
        ...
    </logic:iterate>
</logic:notEmpty>
<logic:notEmpty name="arryEntity">
    <logic:iterate id="entityRecord" name="arryEntity" length="1"
                   type="com.bean.EntityBean" scope="session">
        ...
    </logic:iterate>
</logic:notEmpty>
```

A full-text search of `src/main/java/` for `setAttribute` calls using the keys `"sessMenu"` or `"arryEntity"` returned no results. Neither `LoginAction`, `AdminMenuAction`, `SwitchCompanyAction`, `CompanySessionSwitcher`, nor any other visible action class populates these session attributes. Possible implications:

- The code path that sets these attributes may have been deleted, leaving a silently empty menu.
- The attributes may be set by a system-admin-specific login flow not present in this repository snapshot.
- In the absence of a setter, the `<logic:notEmpty>` guard prevents a runtime exception, but the correct administrative menu is never rendered. This failure is silent and would not be detected without a test.

---

**B09-3 | Severity: MEDIUM | menu_print.inc.jsp — Duplicate opening body tag and incorrect window.print() invocation**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_print.inc.jsp`, line 5.

```jsp
<body onload="print('document');window.close();"><body>
```

Two defects on a single line:

1. `print('document')` — the DOM `window.print()` function accepts no arguments. The string `'document'` is silently ignored by all browsers. The intent of printing the current document is achieved only because `print()` without arguments prints the current window, not because of the argument.

2. A second `<body>` opening tag immediately follows the first. The HTML specification forbids multiple `<body>` elements. Browser parsers typically merge the two opening tags' attributes (there are none on the second), but this is implementation-defined behaviour. No test validates the rendered DOM.

Additionally, `com.util.RuntimeConf` is imported on line 4 but never used in the file.

---

**B09-4 | Severity: MEDIUM | menu_register.inc.jsp and menu_systemadmin.inc.jsp — Malformed href attribute (extraneous double-quote)**

Files:
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`, line 18
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`, line 16

```html
<area shape="rect" coords="0,5,447,67" href="http://www.prestart.com.au"" target='_blank' alt="PreStart" />
```

A trailing double-quote follows the closing quote of the `href` value: `"http://www.prestart.com.au""`. HTML parsers terminate the `href` attribute value at the first closing `"`, then encounter a second `"` as an unexpected character. Browsers silently recover (treating the extra `"` as part of the next attribute context), but:

- HTML validators report this as a parse error.
- Security scanners may flag attribute parsing anomalies.
- The `target='_blank'` attribute uses single-quote delimiters while the surrounding attributes use double-quotes — inconsistent quoting that compounds parsing complexity.

No test validates the markup produced by either file.

---

**B09-5 | Severity: MEDIUM | menu_register.inc.jsp and menu_systemadmin.inc.jsp — target=_blank links without rel=noopener noreferrer**

Files:
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`, lines 18–19
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`, lines 16–17

```html
<area ... href="http://www.prestart.com.au" target='_blank' alt="PreStart" />
<area ... href="http://www.collectiveintelligence.com.au" target='_blank' alt="Collective Intelligence" />
```

Both `<area>` elements open external URLs in a new browsing context (`target='_blank'`) without `rel="noopener noreferrer"`. In older browsers (pre-Chrome 88/Firefox 79), this allows the opened page to access the opener via `window.opener` and potentially redirect the parent page (reverse tabnapping). While modern browsers now default to `noopener` for cross-origin navigation, this is not guaranteed across all supported environments and the missing attribute is a code quality and security hygiene issue.

---

**B09-6 | Severity: MEDIUM | menu_register.inc.jsp — Three unused JSP page import declarations (dead code)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`, lines 4–6.

```jsp
<%@ page import="com.util.RuntimeConf" %>
<%@ page import="com.action.SwitchLanguageAction" %>
<%@ page import="javax.servlet.http.Cookie" %>
```

None of these three classes — `RuntimeConf`, `SwitchLanguageAction`, or `Cookie` — are referenced anywhere in the file body. The file renders a banner image only, with no scriptlet logic. These imports suggest the file was derived from a more complex template (likely `importLib.jsp`) without removing unused dependencies. The presence of `SwitchLanguageAction` and `Cookie` imports suggests language-switching logic was intended but never implemented. No test verifies that the file body makes no use of these classes.

---

**B09-7 | Severity: MEDIUM | menu_systemadmin.inc.jsp — Unused RuntimeConf import**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`, line 5.

```jsp
<%@ page import="com.util.RuntimeConf" %>
```

`RuntimeConf` is imported but never referenced in the file body. This is a dead compile-time dependency. No test validates the absence of scriptlet usage.

---

**B09-8 | Severity: MEDIUM | tilesTemplate.jsp — No test validates four-region tile assembly or missing-attribute failure mode**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplate.jsp`

```jsp
<tiles:insert attribute="header"/>
<tiles:insert attribute="navigation"/>
<tiles:insert attribute="content"/>
<tiles:insert attribute="footer"/>
```

This template is the root layout for all authenticated admin pages and both fleet-check page variants. It is used (directly or via inheritance) by 30+ tile definitions in `tiles-defs.xml`. The Tiles 1.x `insert` tag throws `NoSuchAttributeException` when a declared attribute is absent from the tile definition, unless the attribute is marked `ignore="true"`. No tile definition in `tiles-defs.xml` uses `ignore="true"` for the regions of this template.

No test:
1. Validates that all 30+ definitions using this template supply all four required attributes.
2. Verifies the correct JSP fragment is rendered for each region for each page.
3. Exercises the failure path when an attribute is absent.

A single missing `<put>` in a child tile definition would cause a runtime exception on page load with no prior test warning.

---

**B09-9 | Severity: MEDIUM | tilesTemplateHeader.jsp — No test validates two-region tile assembly across 30+ dependent definitions**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplateHeader.jsp`

```jsp
<tiles:insert attribute="header"/>
<tiles:insert attribute="content"/>
```

This reduced template is the root layout for login, popup, and modal pages. It is extended by `loginDefinition` and 30+ further definitions (`adminJobDefinition`, `OperatorEditDefinition`, `UnitEditDefinition`, `AccountProfileDefinition`, etc.). The same missing-attribute risk applies as for `tilesTemplate.jsp`. Additionally:

- The absence of `navigation` and `footer` is intentional for popup/modal windows, but this is not documented or enforced.
- The `header` attribute resolves to different header fragments in different child definitions (`header.inc.jsp` vs `header_pop.inc.jsp` vs `header_register.inc.jsp`). No test verifies the correct header is rendered in each context.

---

**B09-10 | Severity: MEDIUM | index.jsp — No test for root redirect correctness or authenticated-user loop**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/index.jsp`

```jsp
<%@ include file="includes/importLib.jsp"%>
<logic:redirect forward="welcome"></logic:redirect>
```

The root URL redirects via the Struts global forward `welcome` to `/welcome.do`, handled by `WelcomeAction`, which unconditionally forwards to `loginDefinition` regardless of whether the user is already authenticated. No test covers:

1. That the `welcome` forward name correctly resolves — a typo or removal of the global forward definition in `struts-config.xml` would produce a runtime exception at application root access.
2. That an already-authenticated user who navigates to `/` is sent to the login screen rather than their dashboard (a UX defect that could confuse users or log them out inadvertently).
3. That `importLib.jsp` compiles and is included without side-effects at the root path.

---

**B09-11 | Severity: LOW | menu_popup.inc.jsp — Empty file committed to repository with no tile definition reference**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_popup.inc.jsp`

The file is 0 bytes. No tile definition in `tiles-defs.xml` references it. Its naming follows the convention of other active navigation include files (`menu_print.inc.jsp`, `menu_register.inc.jsp`, `menu_systemadmin.inc.jsp`), implying it was either:
- A placeholder for popup navigation that was never implemented, or
- A file whose content was deleted without removing the file from the repository.

Its presence creates an ambiguous artefact in the include hierarchy. If a future developer adds a reference to it expecting content, the result would be a silently empty navigation region. No test documents its expected content or confirms the empty state is intentional.

---

**B09-12 | Severity: LOW | privacyText.jsp — Stale policy date, unclosed HTML tags, hardcoded PII and production URLs**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/privacyText.jsp`

Multiple issues in a static content file:

1. **Stale policy:** The text states "This policy was last updated on 21st May 2018" (line 12). As of the audit date (2026-02-26), this is approximately 8 years out of date. GDPR Article 13/14 requires privacy notices to be accurate and current.

2. **Unclosed `<p>` tags:** Lines 211, 214, 222, 260, 264, and 308 contain `<p>` tags that are not closed before the next `<p>` opening tag. While browsers handle this via optional tag omission, it produces invalid HTML and will be flagged by HTML validators and accessibility checkers.

3. **Hardcoded production system URLs:** The following public production system hostnames are embedded as plain text in the committed source file (lines 32–43):
   - `www.ciiquk.com`
   - `https://fms.fleetiq360.com`
   - `https://fms.fleetiq360.com/fleetfocus`
   - `https://fms.fleetiq360.com/digitaldashboard`
   - `www.thecollectiveintelligencegroup.com`
   - `https://pandora.fleetiq360.com/PandoraAdmin`

4. **Hardcoded PII (contact details):** The following personal/organisational contact data is committed in plaintext (lines 322–331):
   - Physical address: `Unit 3 Bowdens Business Centre, Bowdens Farm, Hambridge, Nr Curry Rivel, Somerset TA10 0BP`
   - Email: `dp@ciiquk.com`
   - Phone: `01460 259101`

   These details are exposed in version control history and in any repository clone. If the contact details change, they require a code change and redeployment.

---

**B09-13 | Severity: INFO | All eight files — Zero JSP-layer test coverage**

The test directory (`src/test/java/`) contains exactly four test classes, all covering the calibration and impact-utility subsystems. There are no tests of any kind for:

- JSP compilation (no JSP-compilation unit tests or integration tests)
- View rendering (no Mock MVC, Selenium, HtmlUnit, or Arquillian tests)
- Session attribute presence and type assumptions (no tests that verify the view correctly handles null or wrong-type session attributes)
- Tiles assembly correctness (no tests that verify tile definitions resolve to the correct JSP fragments)
- Output encoding (no tests that inject XSS payloads into session attributes and verify they are encoded in the output)
- HTML validity (no tests that validate rendered markup against the HTML specification)

The entire view layer — spanning 8 include fragments and the root index, composing 60+ page definitions via Tiles — is completely untested.

---

## Finding Index

| ID | Severity | File | Description |
|----|----------|------|-------------|
| B09-1 | HIGH | menu_systemadmin.inc.jsp | DB-sourced `action`/`description` written unencoded into href attribute and link text — stored XSS |
| B09-2 | HIGH | menu_systemadmin.inc.jsp | `sessMenu` and `arryEntity` session attributes have no discoverable setter — phantom session state |
| B09-3 | MEDIUM | menu_print.inc.jsp | Duplicate `<body>` opening tag and incorrect `print('document')` invocation |
| B09-4 | MEDIUM | menu_register.inc.jsp, menu_systemadmin.inc.jsp | Extraneous double-quote inside `href` attribute value — HTML syntax error |
| B09-5 | MEDIUM | menu_register.inc.jsp, menu_systemadmin.inc.jsp | `target='_blank'` links missing `rel="noopener noreferrer"` |
| B09-6 | MEDIUM | menu_register.inc.jsp | Three unused `<%@ page import %>` declarations — dead compile-time dependencies |
| B09-7 | MEDIUM | menu_systemadmin.inc.jsp | Unused `RuntimeConf` import |
| B09-8 | MEDIUM | tilesTemplate.jsp | No test validates four-region assembly or missing-attribute exception path across 30+ definitions |
| B09-9 | MEDIUM | tilesTemplateHeader.jsp | No test validates two-region assembly or correct header variant selection across 30+ definitions |
| B09-10 | MEDIUM | index.jsp | No test for root redirect resolution or authenticated-user redirect loop |
| B09-11 | LOW | menu_popup.inc.jsp | Empty (0-byte) placeholder file committed with no tile reference and no documented intent |
| B09-12 | LOW | privacyText.jsp | Stale 2018 policy date; unclosed `<p>` tags; hardcoded production URLs and contact PII in committed source |
| B09-13 | INFO | All eight files | Zero JSP-layer test coverage — no rendering, compilation, session-attribute, or output-encoding tests exist |
