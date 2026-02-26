# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** B09
**Scope:** JSP fragments and layout templates – includes/menu, menu_loginInfo, menu_popup, menu_print, menu_register, menu_systemadmin, privacyText, tilesTemplate, tilesTemplateHeader, and root index

---

## Methodology

1. Each JSP file was read in full.
2. The test directory (`src/test/java/`) was grepped for each filename stem and for all session attribute names referenced by the JSPs.
3. The `LoginAction`, `SwitchCompanyAction`, `CompanySessionSwitcher`, `PreFlightActionServlet`, `RuntimeConf`, and `tiles-defs.xml` were examined for context.

**Test files found in scope:** NONE
Grep for every filename stem and all session attribute keys (`sessArrComp`, `sessCompId`, `isSuperAdmin`, `isDealer`, `sessMenu`, `arryEntity`, `menu`, `tilesTemplate`, `privacy`, `index`) returned no results in the test directory. The only existing test files are:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these have any relationship to the JSP layer.

---

## File-by-File Evidence and Findings

---

### 1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu.inc.jsp`

**Apparent purpose:** Primary authenticated navigation shell. Includes the top bar (company switcher, My Account, Help, Logout) and the left sidebar menu. Wraps the page content area. Used by `adminDefinition` in `tiles-defs.xml` — the default tile for all admin-area pages.

**Scriptlet blocks:**
- Line 32: `<logic:equal name="company" property="authority" value="<%=RuntimeConf.ROLE_SUBCOMP %>">` — inlines the Java constant `RuntimeConf.ROLE_SUBCOMP` to conditionally indent sub-company entries in the company dropdown.
- Line 41: `$('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');` — raw session attribute echoed into a JavaScript string literal without any escaping.

**EL / Struts tag reads on session/request attributes:**
- `sessArrComp` — `<bean:size>` and `<logic:iterate>` (company list)
- `sessCompName` — `<bean:write name="sessCompName"/>` (single-company display)
- `sessCompId` — raw scriptlet read via `session.getAttribute("sessCompId")`
- `company.id` / `company.name` / `company.authority` — iterated over `sessArrComp` items
- `isDealer` — `<logic:equal value="true" name="isDealer">` (controls Customers/Locations sidebar link)
- `isSuperAdmin` — `<logic:equal name="isSuperAdmin" value="true">` (controls Dealers sidebar link)

**JavaScript with security implications:**
- Line 41: `$('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');`
  The session attribute `sessCompId` is injected directly into a JS string without HTML or JS escaping. If `sessCompId` ever contains a single-quote, backslash, or angle bracket (possible if data originates from attacker-controlled input upstream), this is a stored XSS sink.

**Session attribute assumptions:**
- `sessArrComp` is assumed non-null. If null, `<bean:size id="size" name="sessArrComp"/>` will throw a `JspException` (NullPointerException at runtime).
- `isSuperAdmin` and `isDealer` are `Boolean` objects set by `LoginAction` and `CompanySessionSwitcher`. Their absence (null) from the session would not cause an exception for Struts `<logic:equal>` (it evaluates to false), but this is implicitly assumed and never tested.
- The company-switcher form POSTs to `switchCompany.do`. `SwitchCompanyAction` performs a null-safety check (`if (!isSuperAdmin && !isDealerLogin)`) but auto-unboxes `Boolean` objects — an NPE will be thrown if `isSuperAdmin` or `isDealerLogin` is null in the session.

**Hardcoded URLs / external links:**
- Help modal links to `http://forklift-iq360.kayako.com/` (HTTP, not HTTPS; third-party; may be stale).

---

### 2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_loginInfo.inc.jsp`

**Apparent purpose:** Alternate navigation header used for the driver/fleet-check workflow (`fleetcheckDefinition`, `fleetcheckDashboardDefinition`). Shows company name and driver name from session; provides a logout link.

**Scriptlet blocks:** None (uses Struts tags only).

**EL / Struts tag reads on session/request attributes:**
- `sessArrComp` (session, scope="session") — `<logic:notEmpty>`, `<logic:iterate length="1">`, `compRecord.name` via `<bean:write>`
- `arrDriver` (session, scope="session") — `<logic:notEmpty>`, `<logic:iterate length="1">`, `driverRecord.first_name`, `driverRecord.last_name` via `<bean:write>`

**JavaScript with security implications:** None.

**Session attribute assumptions:**
- Both `sessArrComp` and `arrDriver` are expected as `ArrayList` objects in session scope. `<logic:notEmpty>` guards their use, but the guard only prevents iteration — it does not guard against the attributes being wrong types. No tests validate that these attributes are set before this fragment is rendered.
- The logout link uses an HTML `<form>` with `<a href="#" onclick="document.logoutform.submit();"` — this bypasses CSRF token concerns but a test environment has never verified the form name matches the form tag's `name` attribute.

**Other issues:**
- Duplicate `<%@ page import="com.util.RuntimeConf,com.bean.CompanyBean" %>` and `<%@ page import="com.util.RuntimeConf,com.bean.DriverBean" %>` on lines 5–6 — `RuntimeConf` imported twice, which will cause a JSP compilation warning/error in strict containers. This has never been caught by any test.
- Malformed HTML: line 52 contains `</form>` with no corresponding `<form>` tag in this file (the logout `<form>` tag is on line 46 but a stray `</form>` on line 52 closes an outer phantom form).

---

### 3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_popup.inc.jsp`

**Apparent purpose:** Declared as a popup navigation variant (referenced by name in the project). The file exists in the repository but is **completely empty** (0 bytes).

**Scriptlet blocks:** None (file is empty).
**EL / session attribute reads:** None (file is empty).
**JavaScript:** None.

**Key observation:** The file is a 0-byte placeholder. No tile definition in `tiles-defs.xml` currently references it. Its presence in the repository with no content and no callers creates a dead-code artifact with no corresponding test.

---

### 4. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_print.inc.jsp`

**Apparent purpose:** Navigation header for a print view. Renders body with an `onload` that immediately triggers `window.print()` and closes the window.

**Scriptlet blocks:** None (uses Struts taglib imports only).

**EL / Struts tag reads on session/request attributes:** None explicitly in this file.

**JavaScript with security implications:**
- Line 5: `<body onload="print('document');window.close();">` — note the argument `'document'` is passed to `window.print()`, which does not accept arguments in standard browsers (the argument is silently ignored). The intent is to print the current document. This is harmless but incorrect JavaScript.
- Immediately followed by a second `<body>` tag on the same line (`<body onload="..."><body>`), producing two opening `<body>` tags, which is invalid HTML and browser-behaviour-dependent.

**Session attribute assumptions:** None in this file, but it presumably relies on surrounding tile content.

---

### 5. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`

**Apparent purpose:** Navigation header for the registration workflow. Minimal — shows only the banner image; no navigation links, no session-dependent content.

**Scriptlet blocks:** None.

**EL / Struts tag reads on session/request attributes:** None.

**JavaScript with security implications:** None.

**Other issues:**
- Line 18: `href="http://www.prestart.com.au""` — trailing spurious double-quote inside the `href` attribute value. This is a markup syntax error that browsers may recover from silently but is untested.
- Unused imports declared: `com.util.RuntimeConf`, `com.action.SwitchLanguageAction`, `javax.servlet.http.Cookie` — none of these are referenced anywhere in the file.

---

### 6. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`

**Apparent purpose:** Navigation header for the system-admin context. Includes a nav-pill menu dynamically built from the session attribute `sessMenu`, an entity name display from `arryEntity`, and a logout link.

**Scriptlet blocks:** None.

**EL / Struts tag reads on session/request attributes:**
- `sessMenu` (implied session) — `<logic:notEmpty name="sessMenu">`, `<logic:iterate name="sessMenu" id="menuRecord" type="com.bean.MenuBean">`, writes `menuRecord.action` and `menuRecord.description` via `<bean:write>`.
- `arryEntity` (session scope="session") — `<logic:notEmpty name="arryEntity">`, `<logic:iterate length="1" type="com.bean.EntityBean">`, writes `entityRecord.name`.

**JavaScript with security implications:** None directly, but see XSS finding below.

**XSS risk:**
- Line 40: `href="adminmenu.do?action=<bean:write property="action" name="menuRecord" />"` — the `action` property from `MenuBean` is written unescaped into an HTML `href` attribute. If `action` contains `"` or `>` characters, the attribute is broken. `<bean:write>` does NOT HTML-encode by default in Struts 1.x (the `filter` attribute defaults to `true` on `<bean:write>` but only for special HTML characters; URL-encoded payloads injected via DB could still produce XSS). The description field is also written into link text: `<bean:write property="description" name="menuRecord" />` — same risk if description contains `<script>`.
- No test validates what data `sessMenu` may contain or that it is sanitised before being stored in the session.

**Session attribute assumptions:**
- `sessMenu` is never set by `LoginAction` or `CompanySessionSwitcher`. The population path for this attribute is unknown from code inspection, creating an untested/unclear dependency.
- `arryEntity` similarly has no setter in visible action code — its origin is undocumented and untested.

---

### 7. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/privacyText.jsp`

**Apparent purpose:** Static HTML-only privacy policy text fragment. Included by `footer.inc.jsp` and by `html-jsp/privacy.jsp`. Contains GDPR policy boilerplate dated May 2018.

**Scriptlet blocks:** None.
**EL / session attribute reads:** None.
**JavaScript:** None.

**Other issues:**
- Contains unclosed `<p>` tags (lines 211, 214, 222, 260, 264, 308) — malformed HTML. Browser rendering is tolerant but this is not validated by any test.
- Policy last updated date is "21st May 2018" (line 12) — this text is hardcoded and has never been updated. The URL `https://fms.fleetiq360.com` is exposed as a public endpoint in a committed file.
- Internal company contact details (postal address, email `dp@ciiquk.com`, phone number) are committed to the repository and rendered publicly.

---

### 8. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplate.jsp`

**Apparent purpose:** Main Tiles layout template composing four regions: `header`, `navigation`, `content`, `footer`. Used by `adminDefinition` and all admin-area definitions that extend it, and by both `fleetcheckDefinition` and `fleetcheckDashboardDefinition`.

**Scriptlet blocks:** None.
**EL / session attribute reads:** None (only `<tiles:insert>` directives).
**JavaScript:** None.

**Key observation:** This template is the root composition point for the majority of authenticated pages. It has no logic of its own, but its correct assembly depends entirely on the tiles-defs.xml configuration. No test validates that all four attributes are correctly resolved or that missing tile attributes fail gracefully rather than throwing a `NullPointerException` at render time.

---

### 9. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplateHeader.jsp`

**Apparent purpose:** Reduced Tiles layout template composing only `header` and `content` regions. Used by `loginDefinition` and all popup/modal definitions (lightbox forms, edit panels, etc.).

**Scriptlet blocks:** None.
**EL / session attribute reads:** None.
**JavaScript:** None.

**Key observation:** All popup and modal content (vehicle edit, driver edit, checklist edit, alert add, etc.) flows through this template. No test validates the two-region assembly. Missing `header` or `content` tile attributes would produce silent empty output or a runtime exception — neither case is tested.

---

### 10. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/index.jsp`

**Apparent purpose:** Root entry point of the web application. Contains exactly two lines: includes `importLib.jsp` and immediately redirects via `<logic:redirect forward="welcome">`.

**Scriptlet blocks:** None.
**EL / session attribute reads:** None.
**JavaScript:** None.

**Session attribute assumptions:** None in this file. However, the `welcome` forward is mapped in `struts-config.xml` to `/welcome.do`, which in turn renders `loginDefinition`. The forward does not preserve or inspect any session state, so a user who is already authenticated will be redirected to the login page. No test covers this redirect path or the correct resolution of the `welcome` forward name.

---

## Coverage Gap Summary

### No tests exist for any JSP in scope

All ten files are completely uncovered. The test suite (`UnitCalibration*Test`, `ImpactUtilTest`) is unrelated to the web/view layer.

---

## Findings

**B09-1 | Severity: CRITICAL | menu.inc.jsp — Unescaped session attribute echoed into JavaScript string (stored XSS)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu.inc.jsp`, line 41.

```jsp
$('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');
```

`sessCompId` is a session attribute set from database-sourced company ID data. It is interpolated directly into a JavaScript string literal with no escaping. If the value were ever to contain a single quote, the string literal is broken and arbitrary JavaScript executes. No test validates the content of `sessCompId` at render time, and no encoding filter is applied. This is the most severe XSS vector in the JSP layer.

---

**B09-2 | Severity: HIGH | menu_systemadmin.inc.jsp — Unencoded database-sourced values written into href and link text (reflected/stored XSS)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`, line 40.

```jsp
<li><a href="adminmenu.do?action=<bean:write property="action" name="menuRecord" />">
    <bean:write property="description" name="menuRecord" />
</a></li>
```

`MenuBean.action` and `MenuBean.description` originate from the `sessMenu` session attribute, which is populated from the database. `<bean:write>` in Struts 1.x applies HTML character filtering for `<`, `>`, `&`, `"` by default (filter=true), but the `action` value is placed inside an already-open attribute context delimited by `"`, making the default filter insufficient to prevent attribute injection. The `description` field written as link text is also unescaped for contextual URL injection. No sanitisation or output-encoding test exists.

---

**B09-3 | Severity: HIGH | menu.inc.jsp — Role-based sidebar gating has zero test coverage**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu.inc.jsp`, lines 154–169.

```jsp
<logic:equal value="true" name="isDealer">
    <li><a href="dealercompanies.do">...</a></li>
</logic:equal>
<logic:equal name="isSuperAdmin" value="true">
    <li><a href="adminmenu.do?action=configDealer">...</a></li>
</logic:equal>
```

The Customers/Locations link is gated by `isDealer` and the Dealers administration link is gated by `isSuperAdmin`. Both are `Boolean` session attributes. No test verifies:
1. That a regular non-dealer, non-superadmin user cannot see these links.
2. That the attributes being `null` (session fixation, session expiry mid-request) does not expose the links or throw a `NullPointerException`.
3. That setting `isDealer=true` in the session (e.g., via session manipulation) actually restricts the backend — the JSP gating is purely presentational.

---

**B09-4 | Severity: HIGH | SwitchCompanyAction — NPE on Boolean auto-unbox when session attributes are null (reachable from menu.inc.jsp company switcher)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/action/SwitchCompanyAction.java`, lines 27–31.

```java
Boolean isSuperAdmin = (Boolean) session.getAttribute("isSuperAdmin");
Boolean isDealerLogin = (Boolean) session.getAttribute("isDealerLogin");
if (!isSuperAdmin && !isDealerLogin) {   // NPE if either is null
```

The company-switcher `<html:form>` in `menu.inc.jsp` (line 24) posts to `switchCompany.do`. If `isSuperAdmin` or `isDealerLogin` is absent from the session (after expiry, manual removal, or a new session after partial login), the auto-unboxing on line 31 throws `NullPointerException`. `PreFlightActionServlet` only guards on `sessCompId` being null, not on these role flags. No test covers the null-session scenario for `SwitchCompanyAction`.

---

**B09-5 | Severity: HIGH | menu.inc.jsp — Company switcher submits without CSRF protection**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu.inc.jsp`, lines 24–39.

```jsp
<html:form method="post" action="switchCompany.do">
    <html:select property="currentCompany" onchange="this.form.submit()">
```

The company-switch form auto-submits on `onchange` with no synchroniser token. Struts 1.x's `<html:form>` does not add CSRF tokens by default. A cross-site request can silently switch the victim's active company context, causing them to operate on data belonging to a different company. No test validates that the action is CSRF-protected.

---

**B09-6 | Severity: MEDIUM | menu_loginInfo.inc.jsp — Duplicate import of com.util.RuntimeConf causes JSP compile warning/error**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_loginInfo.inc.jsp`, lines 5–6.

```jsp
<%@ page import="com.util.RuntimeConf,com.bean.CompanyBean" %>
<%@ page import="com.util.RuntimeConf,com.bean.DriverBean" %>
```

`com.util.RuntimeConf` is declared in both `import` directives. The JSP specification (JSP 2.x §JSP.7.1.14) treats duplicate class imports as a translation-time error in strict containers. In Tomcat/Jasper this typically produces a compile warning but may be an error in other containers. Neither import of `RuntimeConf` is actually used in the file body. No test exercises JSP compilation of this fragment.

---

**B09-7 | Severity: MEDIUM | menu_loginInfo.inc.jsp — Stray closing </form> tag creates malformed DOM**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_loginInfo.inc.jsp`, line 52.

```jsp
</form >
```

This closing tag has no matching opening `<form>` tag in this file (the logout form on line 46 closes with its own `</form>` on line 48). The stray tag creates an invalid document structure that browser parsers may handle unpredictably. No test validates the rendered DOM structure.

---

**B09-8 | Severity: MEDIUM | menu.inc.jsp — sessArrComp null causes runtime JspException (no null guard on bean:size)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu.inc.jsp`, line 17.

```jsp
<bean:size id="size" name="sessArrComp"/>
```

If `sessArrComp` is null in the session (e.g., session partially initialised, session fixation attack), `<bean:size>` throws a `JspException: Cannot find bean sessArrComp in any scope`. `PreFlightActionServlet` only checks for `sessCompId` being null — it does not guard against `sessArrComp` being absent. The result is an unhandled exception propagated to the user. No test covers this failure mode.

---

**B09-9 | Severity: MEDIUM | menu_systemadmin.inc.jsp — sessMenu population path is undocumented and untested**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`, lines 38–42.

```jsp
<logic:notEmpty name="sessMenu">
    <logic:iterate name="sessMenu" id="menuRecord" type="com.bean.MenuBean">
        <li><a href="adminmenu.do?action=<bean:write property="action" name="menuRecord" />">
```

No `LoginAction`, `CompanySessionSwitcher`, or any other visible action class sets `sessMenu` in the session. The attribute's origin is not traceable in the source tree — it may be set by a legacy or system-admin-specific action not present in the current codebase. Its absence causes the menu to silently render empty (the `<logic:notEmpty>` guard prevents an exception), but the correct administrative menu is never verified by any test. The same applies to `arryEntity`.

---

**B09-10 | Severity: MEDIUM | menu_print.inc.jsp — Invalid HTML: duplicate body tags and incorrect window.print() call**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_print.inc.jsp`, line 5.

```jsp
<body onload="print('document');window.close();"><body>
```

Two issues on a single line:
1. `window.print()` is called as `print('document')` — `print()` takes no arguments in any browser; the argument is silently discarded. The intent (print the page) still works, but the code is incorrect.
2. A second `<body>` tag immediately follows. This produces invalid HTML. In browsers the second `<body>` tag is typically ignored, but it is a markup error that has never been tested.

---

**B09-11 | Severity: MEDIUM | menu_register.inc.jsp — Syntax error: double quote inside href attribute value**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`, line 18 (same pattern in menu_systemadmin.inc.jsp line 16 and menu_loginInfo.inc.jsp line 18).

```html
<area shape="rect" coords="0,5,447,67" href="http://www.prestart.com.au"" target='_blank' alt="PreStart" />
```

A trailing double-quote appears inside the `href` attribute: `"http://www.prestart.com.au""`. This is a syntax error that browsers recover from by truncating the attribute at the first closing quote, producing `href="http://www.prestart.com.au"` with the second `"` being consumed as the next attribute name. While browsers are forgiving, HTML validators and security scanners will flag this. The pattern repeats in `menu_loginInfo.inc.jsp` and `menu_systemadmin.inc.jsp`. No test validates rendered markup validity.

---

**B09-12 | Severity: MEDIUM | menu_register.inc.jsp — Unused JSP imports (dead code)**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`, lines 4–6.

```jsp
<%@ page import="com.util.RuntimeConf" %>
<%@ page import="com.action.SwitchLanguageAction" %>
<%@ page import="javax.servlet.http.Cookie" %>
```

None of `RuntimeConf`, `SwitchLanguageAction`, or `Cookie` are referenced anywhere in the file body. These imports inflate the compile-time dependency surface and suggest this file was copied from another template without cleanup. No test exercises or validates the imports.

---

**B09-13 | Severity: MEDIUM | tilesTemplate.jsp / tilesTemplateHeader.jsp — No test validates tile assembly or missing-attribute behaviour**

Files:
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplate.jsp`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplateHeader.jsp`

Both files use `<tiles:insert attribute="..."/>` for all content regions. The Tiles 1.x `insert` tag throws a `NoSuchAttributeException` (or silently omits content, depending on configuration) when a named attribute is not defined in the tile definition. No test:
1. Verifies that all four attributes (`header`, `navigation`, `content`, `footer`) are present for every `adminDefinition`-based tile.
2. Verifies graceful behaviour when an attribute is missing.
3. Confirms the correct JSP fragment is actually rendered for each region.

---

**B09-14 | Severity: MEDIUM | index.jsp — No test for root redirect correctness or session state on entry**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/index.jsp`

```jsp
<%@ include file="includes/importLib.jsp"%>
<logic:redirect forward="welcome"></logic:redirect>
```

The root URL redirects to `welcome.do`. No test verifies:
1. That the `welcome` forward name resolves correctly.
2. That an already-authenticated user is sent to the login page rather than home (potential UX defect — a logged-in user hitting `/` will be dumped to the login page again).
3. That the included `importLib.jsp` renders without side-effects (it does not, but this is untested).

---

**B09-15 | Severity: LOW | menu_popup.inc.jsp — Empty file committed to repository**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_popup.inc.jsp`

The file is 0 bytes. It is not referenced by any `tiles-defs.xml` definition. Its purpose is unknown. This dead file adds confusion to the include hierarchy and could be accidentally referenced in future. No test documents its expected content or confirms it is intentionally empty.

---

**B09-16 | Severity: LOW | privacyText.jsp — Malformed HTML (unclosed p-tags) and stale policy date**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/privacyText.jsp`

Multiple unclosed `<p>` tags (lines 211, 214, 222, 260, 264, 308) create invalid HTML. Additionally:
- The policy is dated "21st May 2018" (line 12) — over seven years stale.
- Physical company address, phone number, and email (`dp@ciiquk.com`) are hardcoded in the committed file.
- External URLs (`https://fms.fleetiq360.com`, `https://pandora.fleetiq360.com/PandoraAdmin`, `www.ciiquk.com`) are embedded as plain text, exposing production system hostnames in version control.

No test validates the content or freshness of the privacy policy text.

---

**B09-17 | Severity: LOW | menu.inc.jsp — Hardcoded HTTP external link in Help modal**

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu.inc.jsp`, lines 116–117.

```html
<a href="http://forklift-iq360.kayako.com/" target="_blank">
```

The help URL uses HTTP (not HTTPS) and links to a third-party support platform. Mixed-content warnings may be raised by browsers when the admin application is served over HTTPS. The domain `forklift-iq360.kayako.com` may no longer be active. No test validates the content or availability of external links.

---

**B09-18 | Severity: INFO | All JSP fragments — Zero JSP-layer test coverage across the entire project**

The test directory contains exactly four test classes, all covering the calibration and impact-utility subsystems. There are no:
- Mock MVC or Selenium/HTMLUnit tests for any JSP rendering.
- Unit tests for scriptlet logic embedded in JSPs.
- Tests for session attribute presence/type assumptions in menu fragments.
- Tests for role-gate correctness (`isDealer`, `isSuperAdmin`).
- Tests for Tiles layout assembly.
- Tests for XSS output encoding.

The entire view layer is untested.

---

## Finding Index

| ID | Severity | File | Description |
|----|----------|------|-------------|
| B09-1 | CRITICAL | menu.inc.jsp | Unescaped `sessCompId` echoed into JS string — stored XSS |
| B09-2 | HIGH | menu_systemadmin.inc.jsp | DB-sourced `action`/`description` written unencoded into href and link text |
| B09-3 | HIGH | menu.inc.jsp | Role-based sidebar gating (`isDealer`, `isSuperAdmin`) has zero test coverage |
| B09-4 | HIGH | SwitchCompanyAction (triggered by menu.inc.jsp) | NPE on Boolean auto-unbox when session role flags are null |
| B09-5 | HIGH | menu.inc.jsp | Company-switcher form has no CSRF protection |
| B09-6 | MEDIUM | menu_loginInfo.inc.jsp | Duplicate `RuntimeConf` import — JSP compile error in strict containers |
| B09-7 | MEDIUM | menu_loginInfo.inc.jsp | Stray `</form>` tag with no matching open tag — malformed DOM |
| B09-8 | MEDIUM | menu.inc.jsp | `<bean:size name="sessArrComp">` throws JspException if attribute is null |
| B09-9 | MEDIUM | menu_systemadmin.inc.jsp | `sessMenu` and `arryEntity` population path is undocumented and untested |
| B09-10 | MEDIUM | menu_print.inc.jsp | Duplicate `<body>` tags and incorrect `window.print('document')` call |
| B09-11 | MEDIUM | menu_register.inc.jsp (and others) | Double-quote syntax error inside `href` attribute |
| B09-12 | MEDIUM | menu_register.inc.jsp | Unused JSP imports — dead code |
| B09-13 | MEDIUM | tilesTemplate.jsp, tilesTemplateHeader.jsp | No test for tile assembly or missing-attribute behaviour |
| B09-14 | MEDIUM | index.jsp | No test for root redirect correctness or authenticated-user redirect loop |
| B09-15 | LOW | menu_popup.inc.jsp | Empty (0-byte) file committed to repository |
| B09-16 | LOW | privacyText.jsp | Unclosed p-tags, stale 2018 policy date, hardcoded production URLs and contact PII |
| B09-17 | LOW | menu.inc.jsp | Hardcoded HTTP link to third-party support site in Help modal |
| B09-18 | INFO | All files | Zero JSP-layer test coverage across entire project |
