# Pass 3 Documentation Audit — Agent B09
**Audit date:** 2026-02-26
**Files audited:** 9
**Auditor:** B09

---

## Reading Evidence

---

### File 1: `includes/menu_loginInfo.inc.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_loginInfo.inc.jsp`

**Purpose (inferred):** Header/navigation include fragment rendered after a successful login. Displays the application banner image (with two clickable map areas for external vendor sites), the current company name (from session), the current driver's first and last name (from session), and a logout link that submits a POST form to `logout.do`. Opens the `#wrap` and `#adcontent` layout divs that are presumably closed by a footer fragment.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**Session attribute accesses:**
- `sessArrComp` — accessed via Struts `<logic:notEmpty name="sessArrComp">` and `<logic:iterate name="sessArrComp" scope="session">` (line 31–35). Iterates over a list of `CompanyBean` objects; reads only the first element.
- `arrDriver` — accessed via `<logic:notEmpty name="arrDriver">` and `<logic:iterate name="arrDriver" scope="session">` (lines 39–43). Iterates over a list of `DriverBean` objects; reads only the first element.

**Significant JavaScript/CSS:** None inline. The logout link uses an inline `onclick` calling `document.logoutform.submit()` (line 47).

**Notable structural observations:**
- Line 52 contains a stray `</form>` closing tag with no matching opening `<form>` tag at that nesting level (the form opened at line 46 is already closed at line 48).
- Duplicate `<%@ page import="com.util.RuntimeConf,com.bean.CompanyBean" %>` and `<%@ page import="com.util.RuntimeConf,com.bean.DriverBean" %>` directives appear on lines 5–6; both import `RuntimeConf` redundantly.
- No `RuntimeConf` is used anywhere in the file despite being imported on both lines 5 and 6.
- The `adcontent` div opened at line 55 is never closed within this fragment.

---

### File 2: `includes/menu_popup.inc.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_popup.inc.jsp`

**Purpose (inferred):** Unknown — the file is zero bytes (completely empty).

**JSP scriptlet blocks:** None (empty file).

**JSP expression blocks:** None (empty file).

**Session attribute accesses:** None (empty file).

**Significant JavaScript/CSS:** None (empty file).

---

### File 3: `includes/menu_print.inc.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_print.inc.jsp`

**Purpose (inferred):** A minimal page/fragment intended to trigger a browser print dialog and immediately close the window. Used as a print-layout target: on body load it calls `print('document')` and then `window.close()`.

**JSP scriptlet blocks:** None.

**JSP expression blocks:** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:**
- Inline `onload` handler on `<body>` (line 5): `print('document');window.close();`

**Notable structural observations:**
- Line 5 contains two `<body>` opening tags: `<body onload="print('document');window.close();"><body>`. The second `<body>` tag is a duplicate that will be silently ignored by browsers but represents a markup defect.
- `com.util.RuntimeConf` is imported (line 4) but never used.

---

### File 4: `includes/menu_register.inc.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_register.inc.jsp`

**Purpose (inferred):** Header/navigation include fragment for the user registration flow (pre-login). Displays the application banner with two external vendor image-map links, but no logout link and no user-identity display. Opens the `#wrap`, `.header`, and `#adcontent` layout divs. The `SwitchLanguageAction` and `Cookie` imports suggest this fragment was intended to support or once did support a language-switch mechanism from the registration screen, though no such logic is present in the current content.

**JSP scriptlet blocks:** None.

**JSP expression blocks:** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:** None.

**Notable structural observations:**
- Imports `com.action.SwitchLanguageAction`, `javax.servlet.http.Cookie`, and `com.util.RuntimeConf` (lines 4–6), none of which are used anywhere in the file.
- Line 18 contains a double-quote typo in the `href` attribute: `href="http://www.prestart.com.au""` (extra trailing `"`).
- The `<td>` opened at line 15 (`<td rowspan="2">`) is not closed before the next `<td>` at line 21.
- `#adcontent` div opened at line 29 is never closed within this fragment.

---

### File 5: `includes/menu_systemadmin.inc.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/menu_systemadmin.inc.jsp`

**Purpose (inferred):** Header/navigation include fragment for the system-administration area. Displays the application banner, a Bootstrap navbar (`nav-pills`) with a Home link, a dynamic Settings dropdown menu built from a session-stored menu list, and a Quit/Logout link. Also displays the current entity name from the session.

**JSP scriptlet blocks:** None.

**JSP expression blocks:** None.

**Session attribute accesses:**
- `sessMenu` — accessed via `<logic:notEmpty name="sessMenu">` and `<logic:iterate name="sessMenu" id="menuRecord" type="com.bean.MenuBean">` (lines 38–42). Builds the Settings dropdown from a list of `MenuBean` objects, rendering each as `adminmenu.do?action=<action>`.
- `arryEntity` — accessed via `<logic:notEmpty name="arryEntity">` and `<logic:iterate name="arryEntity" scope="session" length="1" type="com.bean.EntityBean">` (lines 51–55). Displays the current entity name in the header.

**Significant JavaScript/CSS:**
- Bootstrap dropdown widget activated via `data-toggle="dropdown"` on the Settings nav item (line 33). Requires Bootstrap JS to be loaded by the including page.

**Notable structural observations:**
- Line 16 has the same double-quote typo in the `href` attribute: `href="http://www.prestart.com.au""`.
- The hard-coded action string `dashboard` (`adminmenu.do?action=dashboard`, line 31) and `quit` (`adminmenu.do?action=quit`, line 45) are magic strings with no documentation.
- The `#adcontent` div opened at line 60 is never closed within this fragment.
- `com.util.RuntimeConf` is imported (line 5) but never used.

---

### File 6: `includes/privacyText.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/privacyText.jsp`

**Purpose (inferred):** Static HTML fragment containing the full privacy policy text for the Collective Intelligence Group / CIIQ UK Ltd. Included into a parent JSP to render the policy. Contains no server-side logic.

**JSP scriptlet blocks:** None.

**JSP expression blocks:** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:** None.

**Notable structural observations:**
- The file is pure HTML `<p>` blocks with no JSP directives whatsoever.
- Several `<p>` tags are left unclosed before subsequent `<p>` tags appear on the same line (e.g., lines 213–214, 222, 260, 264, 298–300, 308). This is invalid HTML that browsers tolerate but represents a markup quality issue.
- The policy states it was last updated on "21st May 2018" (line 12); the document may be stale.

---

### File 7: `includes/tilesTemplate.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplate.jsp`

**Purpose (inferred):** Apache Struts Tiles layout template. Assembles full pages by inserting four tile attributes in order: `header`, `navigation`, `content`, `footer`. Used as the standard four-region page layout.

**JSP scriptlet blocks:** None.

**JSP expression blocks:** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:** None.

---

### File 8: `includes/tilesTemplateHeader.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/includes/tilesTemplateHeader.jsp`

**Purpose (inferred):** Apache Struts Tiles layout template variant. Assembles pages using only two tile attributes: `header` and `content`. Likely used for pages that do not require a navigation bar or footer (e.g., login, registration, or print pages).

**JSP scriptlet blocks:** None.

**JSP expression blocks:** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:** None.

---

### File 9: `index.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/index.jsp`

**Purpose (inferred):** Application entry-point / root redirect. Includes the shared import library (`importLib.jsp`) and then issues a Struts redirect to the named forward `welcome`, effectively routing any direct access to the application root to the welcome/login page.

**JSP scriptlet blocks:** None.

**JSP expression blocks:** None.

**Session attribute accesses:** None.

**Significant JavaScript/CSS:** None.

---

## Findings

---

### B09-1 | LOW | `includes/menu_loginInfo.inc.jsp`:1 | Missing page-level comment

No HTML or JSP comment exists anywhere in the file describing its purpose, what session attributes it requires, or which layout divs it opens. A brief comment at the top would aid maintainers in understanding when and where this fragment is included.

---

### B09-2 | LOW | `includes/menu_loginInfo.inc.jsp`:5-6 | Undocumented and duplicate session attribute keys `sessArrComp` and `arrDriver`

The session attribute names `sessArrComp` and `arrDriver` are accessed with no comment explaining their content, lifecycle, or who populates them. The inconsistent naming convention (one has the `sess` prefix, the other does not) adds confusion. No documentation is present to clarify the difference.

---

### B09-3 | LOW | `includes/menu_popup.inc.jsp`:1 | Zero-byte / empty file

`menu_popup.inc.jsp` is completely empty (0 bytes). If this file is actively referenced by an `<%@ include %>` or Tiles definition, it silently contributes nothing. If it is dead code it should be removed. There is no comment or stub explaining the intent.

---

### B09-4 | LOW | `includes/menu_print.inc.jsp`:1 | Missing page-level comment

No HTML or JSP comment describes the purpose of this fragment, the expected caller context, or how the print-and-close lifecycle is intended to work. The duplicate `<body>` tag on line 5 is an additional unexplained defect.

---

### B09-5 | LOW | `includes/menu_print.inc.jsp`:4 | Unused import with no comment

`com.util.RuntimeConf` is imported but never referenced in the file. There is no comment explaining why the import is present or whether it was intentional. (Same pattern appears in `menu_loginInfo.inc.jsp` lines 5–6, `menu_register.inc.jsp` lines 4–6, and `menu_systemadmin.inc.jsp` line 5.)

---

### B09-6 | LOW | `includes/menu_register.inc.jsp`:1 | Missing page-level comment

No HTML or JSP comment describes the purpose of this fragment, its intended inclusion context (pre-login / registration flow), or why language-switch and cookie imports are present when no corresponding logic exists in the file.

---

### B09-7 | MEDIUM | `includes/menu_register.inc.jsp`:4-6 | Unused imports suggest removed logic with no explanatory comment

`com.action.SwitchLanguageAction`, `javax.servlet.http.Cookie`, and `com.util.RuntimeConf` are all imported but unused. The presence of `SwitchLanguageAction` and `Cookie` strongly suggests that language-switching code was once present and was removed. No comment documents this removal or explains the remaining imports, leaving the intent of the fragment ambiguous.

---

### B09-8 | LOW | `includes/menu_systemadmin.inc.jsp`:1 | Missing page-level comment

No HTML or JSP comment describes the purpose of this fragment, the session attributes it depends on (`sessMenu`, `arryEntity`), or the Bootstrap dependencies it requires.

---

### B09-9 | LOW | `includes/menu_systemadmin.inc.jsp`:38-42 | Undocumented session attribute key `sessMenu`

The session attribute `sessMenu` is iterated to build the Settings dropdown, but no comment explains what populates it, what roles or conditions control its contents, or how the `action` property maps to application behaviour. Magic action strings `dashboard` (line 31) and `quit` (line 45) are also undocumented.

---

### B09-10 | LOW | `includes/menu_systemadmin.inc.jsp`:51-55 | Undocumented session attribute key `arryEntity`

The session attribute `arryEntity` is accessed to display the current entity name. There is no comment explaining what an "entity" represents in the domain model, who sets this attribute, or what the difference is between an entity (in the admin menu) and a company (`sessArrComp` in the login info menu). The inconsistent naming (`arryEntity` vs. `sessArrComp` vs. `arrDriver`) is undocumented.

---

### B09-11 | LOW | `includes/privacyText.jsp`:1 | Missing page/fragment-level comment

No JSP or HTML comment at the top of `privacyText.jsp` identifies its purpose, version, last-review date, or that it is a static include fragment. The only date information is buried in the policy prose itself (line 12: "last updated on 21st May 2018").

---

### B09-12 | LOW | `includes/tilesTemplate.jsp`:1 | Missing page-level comment

No comment documents that this is the standard four-region Tiles layout template, which tile attributes are required (`header`, `navigation`, `content`, `footer`), or which page types use it. Developers must infer the intent from the four `<tiles:insert>` lines alone.

---

### B09-13 | LOW | `includes/tilesTemplateHeader.jsp`:1 | Missing page-level comment

No comment documents that this is a reduced two-region Tiles layout template (`header` + `content` only), or which page categories (login, registration, print) use it instead of the full `tilesTemplate.jsp`.

---

### B09-14 | LOW | `index.jsp`:1 | Missing page-level comment

No comment explains that `index.jsp` is the application root entry-point whose sole purpose is to redirect to the `welcome` forward. The hard-coded forward name `welcome` is also undocumented.

---

## Summary Table

| ID     | Severity | File                              | Line(s) | Issue                                                                    |
|--------|----------|-----------------------------------|---------|--------------------------------------------------------------------------|
| B09-1  | LOW      | menu_loginInfo.inc.jsp            | 1       | Missing page-level comment                                               |
| B09-2  | LOW      | menu_loginInfo.inc.jsp            | 5–6     | Undocumented / inconsistently named session keys `sessArrComp`, `arrDriver` |
| B09-3  | LOW      | menu_popup.inc.jsp                | 1       | Zero-byte empty file with no stub comment                                |
| B09-4  | LOW      | menu_print.inc.jsp                | 1       | Missing page-level comment                                               |
| B09-5  | LOW      | menu_print.inc.jsp                | 4       | Unused import `RuntimeConf` with no comment (pattern repeated in 3 other files) |
| B09-6  | LOW      | menu_register.inc.jsp             | 1       | Missing page-level comment                                               |
| B09-7  | MEDIUM   | menu_register.inc.jsp             | 4–6     | Unused imports imply removed logic; no comment documents the removal     |
| B09-8  | LOW      | menu_systemadmin.inc.jsp          | 1       | Missing page-level comment                                               |
| B09-9  | LOW      | menu_systemadmin.inc.jsp          | 38–45   | Undocumented session key `sessMenu`; magic action strings `dashboard`, `quit` |
| B09-10 | LOW      | menu_systemadmin.inc.jsp          | 51–55   | Undocumented session key `arryEntity`; naming inconsistency undocumented |
| B09-11 | LOW      | privacyText.jsp                   | 1       | Missing page/fragment-level comment                                      |
| B09-12 | LOW      | tilesTemplate.jsp                 | 1       | Missing page-level comment on standard four-region Tiles layout          |
| B09-13 | LOW      | tilesTemplateHeader.jsp           | 1       | Missing page-level comment on reduced two-region Tiles layout            |
| B09-14 | LOW      | index.jsp                         | 1       | Missing page-level comment; undocumented `welcome` forward name          |

**Total findings: 14** (1 MEDIUM, 13 LOW)
