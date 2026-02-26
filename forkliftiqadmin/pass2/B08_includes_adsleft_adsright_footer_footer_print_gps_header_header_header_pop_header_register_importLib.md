# Pass 2 Test Coverage Audit — B08
**Audit Run:** 2026-02-26-01
**Agent:** B08
**Scope:** JSP include fragments — adsleft.inc.jsp, adsright.inc.jsp, footer.inc.jsp, footer_print.inc.jsp, gps_header.jsp, header.inc.jsp, header_pop.inc.jsp, header_register.inc.jsp, importLib.jsp
**Test Directory Searched:** /mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/

---

## Test Directory — File Inventory

The test directory contains exactly four files, all unrelated to the JSP fragments under audit:

- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

Grep of all nine filenames (without extension) against the test directory returned zero matches in every case. No JSP rendering tests, no Mockito/Selenium/HtmlUnit coverage, and no integration tests exist for any of the fragments.

---

## Per-File Evidence and Analysis

### 1. adsleft.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/adsleft.inc.jsp`

**Purpose:** Renders a left-column advertisement panel. Iterates over a session-scoped list of `AdvertisementBean` records and emits image and text content for up to three ads (indices 0–2).

**Scriptlet blocks:**
- `<%=RuntimeConf.IMG_SRC%>` — emits the static string `"images/"` into an `<img src>` attribute without escaping.

**EL / Struts tag attribute access:**
- `<logic:notEmpty name="sessAds">` — reads `sessAds` from session scope.
- `<logic:iterate name="sessAds" id="adsRecord" type="com.bean.AdvertisementBean" length="3">` — iterates session attribute; no null guard beyond `notEmpty`.
- `<bean:write property="pic" name="adsRecord"/>` — emits `AdvertisementBean.pic` directly into an `<img src>` attribute. `bean:write` does **not** HTML-encode by default; `filter="true"` is not set.
- `<bean:write property="text" name="adsRecord" />` — emits `AdvertisementBean.text` directly into HTML body. `filter="true"` not set.

**JavaScript with security implications:** None.

**External URL/CDN references:** None directly; `RuntimeConf.IMG_SRC` resolves to a relative path (`"images/"`).

**Test evidence:** Zero test references found.

---

### 2. adsright.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/adsright.inc.jsp`

**Purpose:** Identical in structure to adsleft.inc.jsp but renders a right-column advertisement panel, iterating the same session list with `offset="3"` to display ads at indices 3–5.

**Scriptlet blocks:**
- `<%=RuntimeConf.IMG_SRC%>` — same as adsleft; emits `"images/"` unescaped into `<img src>`.

**EL / Struts tag attribute access:**
- `<logic:notEmpty name="sessAds">` — reads `sessAds` from session scope.
- `<logic:iterate name="sessAds" id="adsRecord" type="com.bean.AdvertisementBean" length="3" offset="3">` — iterates session attribute.
- `<bean:write property="pic" name="adsRecord"/>` — emits `AdvertisementBean.pic` into `<img src>` without `filter="true"`.
- `<bean:write property="text" name="adsRecord" />` — emits `AdvertisementBean.text` into HTML without `filter="true"`.

**JavaScript with security implications:** None.

**External URL/CDN references:** None.

**Test evidence:** Zero test references found.

---

### 3. footer.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/footer.inc.jsp`

**Purpose:** Site-wide footer fragment. Emits copyright year, company name, a privacy modal trigger, and a terms link. Closes the page body/html structure. Includes `importLib.jsp` and dynamically includes `privacyText.jsp` inside a Bootstrap modal.

**Scriptlet blocks:**
- `<%= Calendar.getInstance().get(Calendar.YEAR)%>` — emits the current year (integer, safe). Imported via `importLib.jsp` which supplies the `java.util.Calendar` import.

**EL / Struts tag attribute access:**
- `<bean:message key="footer.copyright">` — i18n resource key lookup; not user-controlled.
- `<bean:message key="footer.company">` — i18n resource key lookup; not user-controlled.
- `<bean:message key="footer.privacy">` — i18n resource key lookup; not user-controlled.
- `<bean:message key="footer.term">` — i18n resource key lookup; not user-controlled.

**JavaScript with security implications:** None in this file. `importLib.jsp` is pulled in via `<%@ include file%>`.

**External URL/CDN references:**
- `<jsp:include page="privacyText.jsp">` — dynamic include; references a sibling JSP that contains hardcoded external domain URLs (`https://fms.fleetiq360.com`, `https://pandora.fleetiq360.com/PandoraAdmin`).

**Structural issues:**
- The `<a href="" target="_blank">` for the terms link has an empty `href`, so it is non-functional.
- The privacy modal title is hardcoded as `"CIIQ UK LTD PRIVACY POLICY"` — not localised, not configurable.

**Test evidence:** Zero test references found.

---

### 4. footer_print.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/footer_print.inc.jsp`

**Purpose:** Minimal print-layout footer. Closes `</div>`, `</body>`, and `</html>` tags. Contains no logic, no scriptlets, no EL expressions, and no JavaScript.

**Scriptlet blocks:** None.

**EL / Struts tag attribute access:** None.

**JavaScript with security implications:** None.

**External URL/CDN references:** None.

**Test evidence:** Zero test references found.

---

### 5. gps_header.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/gps_header.jsp`

**Purpose:** GPS map header fragment — currently consists entirely of two commented-out lines referencing a Leaflet CSS file and an `ajaxStore.js` script. The fragment emits no active output at runtime.

**Scriptlet blocks:** None (all content is commented out).

**EL / Struts tag attribute access:** None.

**JavaScript with security implications:** None active; the commented lines would reference local assets if uncommented.

**External URL/CDN references:** None active.

**Test evidence:** Zero test references found.

---

### 6. header.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header.inc.jsp`

**Purpose:** Main application page header. Emits the full HTML `<head>` section including all CSS and JavaScript asset tags used across the application.

**Scriptlet blocks:**
- No traditional `<% %>` scriptlets in the rendered markup, but line 42 contains a JS scriptlet pattern: `<script>document.write("<script type='text/javascript' src='skin/js/scripts.js?v=" + Date.now() + "'><\/script>");</script>` — uses `document.write` with a cache-busting timestamp to inject a `<script>` element at parse time.

**EL / Struts tag attribute access:** None — this is a pure HTML/JavaScript asset-loading header.

**JavaScript with security implications:**
- `document.write()` used to inject a `<script>` tag (line 42). `document.write` is deprecated in modern browsers and can be a target for DOM-injection if any surrounding variable were to become attacker-controlled in the future. The current usage is static, but the pattern itself is considered unsafe practice.
- `RuntimeConf` import is declared at line 1 but `RuntimeConf` is not referenced in the rendered output of this file.

**External URL/CDN references:**
- All CSS and JS assets are loaded from relative `skin/` paths — no external CDN references in this file.
- Leaflet, Esri-Leaflet, ajaxStore, and other mapping libraries are included unconditionally on every page that uses this header, regardless of whether the page requires mapping functionality.

**Imported page class:** `com.util.RuntimeConf` — imported but unused in this file.

**Test evidence:** Zero test references found.

---

### 7. header_pop.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header_pop.inc.jsp`

**Purpose:** Pop-up window header fragment. Contains only an inline `<style>` block that constrains the height of a `.modal-content-form` element using `calc()`. No dynamic content or scripting.

**Scriptlet blocks:** None.

**EL / Struts tag attribute access:** None.

**JavaScript with security implications:** None.

**External URL/CDN references:** None.

**Test evidence:** Zero test references found.

---

### 8. header_register.inc.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header_register.inc.jsp`

**Purpose:** Registration page header. Emits the HTML `<head>` section for login/registration pages, including Bootstrap, jQuery UI, Sweet Alert, and a watermark placeholder library. Contains inline CSS and a `$(document).ready` script block.

**Scriptlet blocks:**
- `<%@ page import="com.util.RuntimeConf"%>` — imported but `RuntimeConf` is not referenced anywhere in the rendered output of this file.

**EL / Struts tag attribute access:** None in the rendered markup.

**JavaScript with security implications:**
- `$(document).ready` block (lines 58–62) iterates all `.insertPhld` elements and applies the jQuery watermark plugin using the element's `title` attribute as placeholder text: `$(this).watermark($(this).attr('title'))`. If any element's `title` attribute contains HTML or script, the watermark library could be a vector for DOM-based XSS. The `title` attribute is typically set by Struts `titleKey` i18n lookup — not directly user-controlled — but this path is not validated or encoded before being passed to the watermark plugin.
- jQuery loaded from an external CDN: `https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js`. This is **jQuery version 1.7.1**, which is severely end-of-life (released 2011, unsupported since 2016) and known to contain multiple XSS and prototype-pollution vulnerabilities.

**External URL/CDN references:**
- `https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js` — external CDN load of a critically outdated jQuery version (line 15). This introduces a supply-chain dependency on Google's CDN availability, and the library version is known-vulnerable.

**Test evidence:** Zero test references found.

---

### 9. importLib.jsp
**Path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/importLib.jsp`

**Purpose:** Central import library fragment. Pulled in via `<%@ include file="../includes/importLib.jsp"%>` by other fragments (e.g., footer.inc.jsp). Contains only `<%@ page import %>` directives and Struts taglib declarations — no rendered output.

**Scriptlet blocks:** None (only `<%@ page import %>` directives).

**Imports declared:**
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

**Taglib declarations:**
- `struts-html` as `html`
- `struts-bean` as `bean`
- `struts-logic` as `logic`

**EL / Struts tag attribute access:** None — no rendered output.

**JavaScript with security implications:** None.

**External URL/CDN references:** None.

**Observations:**
- Several imports (`Action`, `ActionMessage`, `ActionErrors`, `Logger`, `SwitchLanguageAction`, `Cookie`, `Iterator`, `ArrayList`, `InfoLogger`) are declared globally but their necessity depends entirely on what the including page uses. Unused imports create unnecessary compilation coupling.
- `log4j` is being used (imported via `org.apache.log4j.Logger`) — the version of log4j in use should be confirmed against Log4Shell (CVE-2021-44228) exposure, though that vulnerability is in log4j-core 2.x, not log4j 1.x.

**Test evidence:** Zero test references found.

---

## Coverage Gap Summary

| File | Scriptlet Logic Tested | Output Encoding Verified | Error Handling Tested | External URL Audit |
|---|---|---|---|---|
| adsleft.inc.jsp | No | No | No | N/A |
| adsright.inc.jsp | No | No | No | N/A |
| footer.inc.jsp | No | No | No | No |
| footer_print.inc.jsp | No (no logic) | No (no output) | N/A | N/A |
| gps_header.jsp | No (no active logic) | N/A | N/A | N/A |
| header.inc.jsp | No | No | No | N/A |
| header_pop.inc.jsp | No (no logic) | N/A | N/A | N/A |
| header_register.inc.jsp | No | No | No | No |
| importLib.jsp | No (no logic) | N/A | N/A | N/A |

---

## Findings

**B08-1 | Severity: CRITICAL | Unescaped ad content output — stored XSS via bean:write without filter**

Both `adsleft.inc.jsp` (lines 11, 14) and `adsright.inc.jsp` (lines 10, 13) use `<bean:write>` to emit database-sourced `AdvertisementBean.pic` and `AdvertisementBean.text` fields directly into HTML without setting `filter="true"`. The Struts 1.x `bean:write` tag defaults to `filter="false"`, meaning no HTML entity encoding is applied. `AdvertisementBean.text` is emitted into HTML body context and `AdvertisementBean.pic` is emitted into an `<img src>` attribute. If an attacker can insert records into the `advertisment` database table, malicious HTML or JavaScript payloads would be rendered directly in every user's browser. The `getAllAdvertisement()` method in `AdvertismentDAO` fetches all rows without any sanitisation. There are no tests validating that encoded or malicious ad content is rejected or escaped.

Files:
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/adsleft.inc.jsp` lines 11, 14
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/adsright.inc.jsp` lines 10, 13

---

**B08-2 | Severity: CRITICAL | Critically outdated jQuery loaded from external CDN in header_register.inc.jsp**

`header_register.inc.jsp` line 15 loads jQuery version 1.7.1 from `https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js`. jQuery 1.7.1 was released in November 2011 and has been unsupported since 2016. It is known to contain multiple security vulnerabilities including XSS via `jQuery.htmlPrefilter` (CVE-2020-11022, CVE-2020-11023) and HTML injection. The registration/login pages that use this header are unauthenticated entry points, making this a high-impact attack surface. There are no tests validating that the library version in use is free of known vulnerabilities.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header_register.inc.jsp` line 15

---

**B08-3 | Severity: HIGH | document.write() used to inject script tag in header.inc.jsp**

`header.inc.jsp` line 42 uses `document.write()` to dynamically inject a `<script>` element with a cache-busting timestamp:
```
<script>document.write("<script type='text/javascript' src='skin/js/scripts.js?v=" + Date.now() + "'><\/script>");</script>
```
`document.write()` is deprecated, blocks the HTML parser, and is rejected entirely by browsers in certain modes (e.g., cross-origin, async). More critically, if any variable ever replaces the static string in this pattern, it becomes a direct DOM-based XSS injection point. The pattern establishes an unsafe coding convention that is not tested. No test exists to verify the rendered output of the header, the integrity of loaded scripts, or that the injected script URL cannot be manipulated.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header.inc.jsp` line 42

---

**B08-4 | Severity: HIGH | Watermark plugin receives title attribute content without HTML encoding in header_register.inc.jsp**

`header_register.inc.jsp` lines 58–62 invoke the jQuery watermark plugin by passing `$(this).attr('title')` directly:
```javascript
$('.insertPhld').each(function() {
    $(this).watermark($(this).attr('title'));
});
```
If any input element's `title` attribute contains HTML markup or JavaScript — whether through a misconfigured i18n resource key or through a future code path where `title` is populated from user data — the watermark plugin could render it as live DOM content, enabling XSS. No output encoding is applied before the value is passed to `watermark()`. There are no tests for this JavaScript behaviour.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header_register.inc.jsp` lines 58–62

---

**B08-5 | Severity: HIGH | No tests exist for any of the nine JSP fragments — zero coverage**

Grep of all nine filenames (adsleft, adsright, footer.inc, footer_print, gps_header, header.inc, header_pop, header_register, importLib) against the test directory at `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/` returned zero matches in every case. The entire test suite consists of four files, all in the calibration domain. No rendering tests (e.g., HtmlUnit, Selenium, Mockito+MockMvc), no tile-integration tests, and no logic-path tests exist for any of these fragments. The untested surface includes all XSS-risk outputs, the CDN dependency, the session-attribute rendering pipeline, and the calendar scriptlet.

---

**B08-6 | Severity: HIGH | sessAds session attribute rendered without type safety or null protection in adsleft.inc.jsp and adsright.inc.jsp**

`adsleft.inc.jsp` and `adsright.inc.jsp` cast the `sessAds` session attribute to `com.bean.AdvertisementBean` via `logic:iterate type="com.bean.AdvertisementBean"`. If the session attribute exists but contains a different type (e.g., due to a session corruption or serialisation mismatch after a deployment), a `ClassCastException` will propagate to the browser as a 500 error with no error page handling in the fragment itself. The `<logic:notEmpty>` guard only tests for non-null and non-empty; it does not guard against type mismatch. `WelcomeAction` sets `sessAds` via `AdvertismentDAO.getInstance().getAllAdvertisement()` — if that call throws, the session attribute is never set and the fragment silently renders empty. There is no test for the behaviour when `sessAds` is absent, malformed, or of the wrong type.

Files:
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/adsleft.inc.jsp` line 9
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/adsright.inc.jsp` line 8

---

**B08-7 | Severity: MEDIUM | footer.inc.jsp terms-of-service link has empty href — dead link, no test**

`footer.inc.jsp` line 5 renders `<a href="" target="_blank"><bean:message key="footer.term"></bean:message></a>`. The `href` is an empty string, meaning the link navigates to the current page rather than any terms document. This is a functional defect with user-facing impact. No test exists to verify the terms link resolves to a valid destination.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/footer.inc.jsp` line 5

---

**B08-8 | Severity: MEDIUM | Privacy modal company name hardcoded — not localised, not configurable**

`footer.inc.jsp` line 20 hardcodes `"CIIQ UK LTD PRIVACY POLICY"` as the modal title. This contradicts the application's localisation strategy (all other footer text uses `bean:message` with resource keys) and will display the wrong entity name if the application is rebranded or deployed under a different legal entity. No test validates that the modal title is consistent with the configured company identity.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/footer.inc.jsp` line 20

---

**B08-9 | Severity: MEDIUM | RuntimeConf imported but unused in header.inc.jsp and header_register.inc.jsp**

`header.inc.jsp` line 1 and `header_register.inc.jsp` line 1 both import `com.util.RuntimeConf` via `<%@ page import="com.util.RuntimeConf" %>`, but neither file references `RuntimeConf` anywhere in its rendered output. Dead imports unnecessarily couple the JSP compilation to the `RuntimeConf` class and introduce confusion about whether these files are intended to use runtime configuration values. No test asserts that these headers render correctly without `RuntimeConf` being populated.

Files:
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header.inc.jsp` line 1
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header_register.inc.jsp` line 1

---

**B08-10 | Severity: MEDIUM | importLib.jsp declares broad unused imports — unnecessary compilation coupling**

`importLib.jsp` declares eleven class imports and three taglib declarations as a shared library included by multiple fragments. Imports for `Action`, `ActionMessage`, `ActionErrors`, `Logger`, `SwitchLanguageAction`, `Cookie`, `Iterator`, `ArrayList`, and `InfoLogger` are included regardless of whether the including fragment uses them. In JSP, `<%@ include %>` performs a textual merge at compile time, meaning every including fragment acquires all these imports. Unused imports bloat the translated servlet and mask intentional dependencies. No test validates the minimal import requirements of any individual including fragment.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/importLib.jsp`

---

**B08-11 | Severity: MEDIUM | All JavaScript and CSS assets in header.inc.jsp loaded with no Subresource Integrity (SRI)**

`header.inc.jsp` loads seventeen JavaScript and CSS files from relative `skin/` paths with no `integrity` or `crossorigin` attributes on any tag. If any served asset file were to be replaced (via a compromised build pipeline, a misconfigured web server, or a path-traversal attack), the browser would execute the replacement without any integrity check. While all paths are relative (not CDN), SRI is still a defence-in-depth measure for local assets. No tests validate the integrity of loaded assets.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header.inc.jsp` lines 13–45

---

**B08-12 | Severity: LOW | gps_header.jsp is entirely commented out — dead fragment with no active purpose**

`gps_header.jsp` contains only two commented-out lines (Leaflet CSS and `ajaxStore.js` script references). The file emits no output and serves no runtime purpose. However, it is included in the Tiles template configuration and is part of the build. Its existence as a named include slot without active content may cause confusion about whether GPS map functionality is enabled or disabled. There is no test or assertion about the active/inactive state of GPS header content.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/gps_header.jsp`

---

**B08-13 | Severity: LOW | Mapping libraries (Leaflet, Esri-Leaflet) unconditionally loaded on all pages via header.inc.jsp**

`header.inc.jsp` lines 43–45 unconditionally load `leaflet.js`, `esri-leaflet.js`, and `ajaxStore.js`. These are substantial libraries needed only on GPS/map pages. Loading them on all pages increases page weight for every user regardless of the page type, and expands the client-side attack surface. No conditional logic or lazy-loading mechanism guards these includes. There are no tests verifying that map libraries are absent from non-map page responses.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/header.inc.jsp` lines 43–45

---

**B08-14 | Severity: LOW | Calendar scriptlet in footer.inc.jsp depends on importLib.jsp include ordering**

`footer.inc.jsp` line 2 uses `<%= Calendar.getInstance().get(Calendar.YEAR)%>` which requires `java.util.Calendar` to be imported. This import is provided by `importLib.jsp` line 14, which is included at `footer.inc.jsp` line 1. If `importLib.jsp` is ever removed from the include chain or reordered, the JSP will fail to compile with a class-not-found error. The dependency is implicit and undocumented. No test validates that the footer renders correctly or that the year output is the expected current year.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/footer.inc.jsp` line 2

---

**B08-15 | Severity: INFO | log4j 1.x imported in importLib.jsp — confirm version is not log4j-core 2.x**

`importLib.jsp` line 4 imports `org.apache.log4j.Logger`, indicating use of Log4j 1.x. Log4Shell (CVE-2021-44228) affects log4j-core 2.x, not 1.x. However, Log4j 1.x itself reached end-of-life in 2015 and has its own known vulnerabilities (CVE-2019-17571, deserialization via SocketServer). This finding is informational to confirm the log4j version declared in `pom.xml` is 1.x and not a shaded or misidentified 2.x artifact.

File: `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/importLib.jsp` line 4

---

*End of B08 report.*
