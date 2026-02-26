# Security Audit Report: adminReports.jsp

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**File Audited:** `src/main/webapp/html-jsp/adminReports.jsp`
**Auditor:** Automated Pass-1
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet auth gate (`sessCompId != null`), no Spring Security, no CSRF tokens

---

## 1. Reading Evidence

### 1.1 Form Action URLs

No `<form>` elements are present in this file. All navigation is via anchor (`<a href="...">`) links only.

| Line(s) | URL / Expression | Type |
|---------|-----------------|------|
| 4  | `session.getAttribute("isDealer").equals("true") ? "dealerIncidentReport.do" : "incidentreport.do"` | Scriptlet — sets `incidentReportUrl` |
| 5  | `session.getAttribute("isDealer").equals("true") ? "dealerSessionReport.do" : "sessionreport.do"` | Scriptlet — sets `sessionReportUrl` |
| 26 | `<a href="<%= incidentReportUrl %>">` | Navigation link |
| 29 | `<a href="<%= incidentReportUrl %>" class="box-a">` | Navigation link |
| 36 | `<a href="sessionreport.do">` | Navigation link (hardcoded, does NOT use `sessionReportUrl`) |
| 38 | `<a href="<%= sessionReportUrl %>" class="box-a">` | Navigation link |
| 45 | `<a href="gpsreport.do">` | Navigation link |
| 47 | `<a href="gpsreport.do" class="box-a">` | Navigation link |

### 1.2 Request Parameters Used in Output or JavaScript

None. No `request.getParameter(...)` calls and no URL query-string parameters are reflected into HTML output in this file.

### 1.3 Struts Tags That Output Data

No Struts `<html:*>`, `<bean:write>`, or `<logic:*>` tags are used in this file. All dynamic output is produced by raw JSP scriptlet expressions (`<%= ... %>`).

| Line(s) | Expression | Source |
|---------|-----------|--------|
| 26, 29 | `<%= incidentReportUrl %>` | Derived from `session.getAttribute("isDealer")` |
| 38      | `<%= sessionReportUrl %>`  | Derived from `session.getAttribute("isDealer")` |

### 1.4 JavaScript Blocks Using Server-Side Data

None. There are no `<script>` blocks in this file.

---

## 2. Security Findings

---

### FINDING-01 — HIGH — Unescaped Scriptlet Output in href Attributes (Reflected XSS via Session Attribute)

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminReports.jsp`
**Lines:** 26, 29, 38

**Description:**
The variables `incidentReportUrl` and `sessionReportUrl` are constructed directly from `session.getAttribute("isDealer")` and then emitted unescaped into `href` attributes using raw JSP expression tags (`<%= %>`). Although these variables are URL strings (not user-supplied HTTP request parameters), they originate from a session attribute that is set via `CompanySessionSwitcher.UpdateCompanySessionAttributes()` (which calls `LoginDAO.isAuthority()` returning a Boolean). In the current code path the values are always `"dealerIncidentReport.do"`, `"incidentreport.do"`, `"dealerSessionReport.do"`, or `"sessionreport.do"` — fixed strings — so exploitation requires the `isDealer` session attribute to have been tampered with or for this pattern to be generalised.

The more concrete risk is the pattern itself: using `<%= %>` without `ESAPI.encodeForHTMLAttribute()` or `<c:out>` / `fn:escapeXml()` means any future refactor that feeds a less-controlled value through the same mechanism would produce a stored/reflected XSS without any change to the JSP. Additionally, if an attacker were able to manipulate session attributes through a separate session-fixation or session-injection vulnerability elsewhere in the app, the unescaped output here would become a direct XSS vector.

**Evidence:**
```jsp
// Line 4-5 (scriptlet)
String incidentReportUrl = session.getAttribute("isDealer").equals("true")
    ? "dealerIncidentReport.do" : "incidentreport.do";
String sessionReportUrl = session.getAttribute("isDealer").equals("true")
    ? "dealerSessionReport.do" : "sessionreport.do";

// Line 26 — output directly into href without escaping
<h3><a href="<%= incidentReportUrl %>">Incident Report</a></h3>

// Line 29 — same pattern
<a href="<%= incidentReportUrl %>" class="box-a"><img src="" class="box-a-img"/></a>

// Line 38 — same pattern
<a href="<%= sessionReportUrl %>" class="box-a"><img src="" class="box-a-img"/></a>
```

**Recommendation:**
Replace raw `<%= %>` expressions with JSTL `<c:out>` with `escapeXml="true"` or ESAPI `ESAPI.encoder().encodeForHTMLAttribute(...)`. For URL values specifically, use `<c:url>` or ensure the value is validated against a whitelist of known-good path strings before rendering. Eliminating raw scriptlets entirely in favour of Struts/JSTL tags would remove the pattern.

---

### FINDING-02 — HIGH — NullPointerException Risk: Unguarded `.equals()` on Session Attribute

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/adminReports.jsp`
**Lines:** 4–5

**Description:**
Both scriptlet lines call `session.getAttribute("isDealer").equals("true")` without a null-check. If the `isDealer` session attribute is absent (e.g., on a fresh session before `CompanySessionSwitcher` has run, or if a different code path creates the session without setting this attribute), the expression will throw a `NullPointerException` at runtime. Struts 1.3 will propagate this as an unhandled server error, potentially exposing a stack trace to the browser if debug error pages are enabled.

**Evidence:**
```jsp
// Line 4 — no null guard
String incidentReportUrl = session.getAttribute("isDealer").equals("true")
    ? "dealerIncidentReport.do" : "incidentreport.do";

// Line 5 — no null guard
String sessionReportUrl = session.getAttribute("isDealer").equals("true")
    ? "dealerSessionReport.do" : "sessionreport.do";
```

**Recommendation:**
Use a null-safe comparison: `"true".equals(session.getAttribute("isDealer"))` (reversing the operands). Alternatively, retrieve and cast safely: `Boolean.TRUE.equals(session.getAttribute("isDealer"))`.

---

### FINDING-03 — MEDIUM — Inconsistent URL for Session Report Navigation Link

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminReports.jsp`
**Line:** 36

**Description:**
The heading anchor for the Session Report box (line 36) is hardcoded to `"sessionreport.do"` rather than using the computed `sessionReportUrl` variable, while the image/link below it (line 38) correctly uses `<%= sessionReportUrl %>`. A dealer-role user (where `isDealer == "true"`) will have the heading link point to the wrong endpoint (`sessionreport.do` instead of `dealerSessionReport.do`). This is a logic defect that bypasses the dealer-specific routing and could allow a dealer user to access the standard `sessionreport.do` endpoint without a corresponding authorisation check, potentially disclosing cross-company session data if `sessionreport.do` does not enforce company-scope filtering for dealer accounts.

**Evidence:**
```jsp
// Line 36 — hardcoded, does NOT respect dealer routing
<h3><a href="sessionreport.do">Session Report</a></h3>

// Line 38 — correctly uses dynamic variable
<a href="<%= sessionReportUrl %>" class="box-a"><img src="" class="box-a-img"/></a>
```

**Recommendation:**
Replace the hardcoded `href` on line 36 with `<%= sessionReportUrl %>` to be consistent with the rest of the panel. Separately, verify that `sessionreport.do` enforces company-scope filtering for dealer accounts.

---

### FINDING-04 — MEDIUM — No In-Page Authorization/Role Check Before Rendering Report Links

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminReports.jsp`
**Lines:** 1–54

**Description:**
The page renders navigation links to `incidentreport.do`, `sessionreport.do`, `dealerIncidentReport.do`, `dealerSessionReport.do`, and `gpsreport.do` for all authenticated sessions without any in-page role check. The only gate is the global `PreFlightActionServlet` check that `sessCompId != null`. There is no check for whether the current user has a specific role (e.g., `isDealer`, `isSuperAdmin`) before displaying links. While access control should be enforced by the target action classes themselves, the lack of in-page visibility control means that all authenticated users — regardless of role — see all report links, including `gpsreport.do` which may be a premium or restricted feature. This is an information disclosure of available application features and may confuse users who receive authorisation errors when following links they should not have been shown.

**Evidence:**
No `<logic:present>`, `<logic:equal>`, or Java `if` block restricts which links are rendered based on user role. The `isDealer` attribute is used only for URL selection, not for feature visibility.

**Recommendation:**
Wrap each report link in a role-appropriate conditional (e.g., using `<logic:equal name="sessionScope" property="isDealer" value="true">` or a JSTL `<c:if>`) to hide links that are not applicable or not authorised for the current user. Ensure the backing action classes also enforce the same access control (defence in depth).

---

### FINDING-05 — MEDIUM — CSRF: No Token on State-Changing Navigation

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/adminReports.jsp`
**Lines:** 10–12, 26, 29, 36, 38, 45, 47

**Description:**
Per the stated stack context, CSRF protection is a structural gap in this application. This file contains no forms, but all navigation links use GET requests to Struts `.do` actions. If any of the target report endpoints (`incidentreport.do`, `sessionreport.do`, `dealerIncidentReport.do`, `dealerSessionReport.do`, `gpsreport.do`) perform state-changing operations (e.g., logging access, generating/exporting reports, or toggling visibility flags) via GET, those operations are inherently CSRF-vulnerable. The link to `adminmenu.do?action=reports` could also be abused in a CSRF scenario to force an authenticated admin into the reports menu context.

**Evidence:**
```jsp
<li><a href="adminmenu.do?action=home">Home</a></li>
<li><a href="adminmenu.do?action=reports">Reports</a></li>
<h3><a href="<%= incidentReportUrl %>">Incident Report</a></h3>
<a href="gpsreport.do">GPS Report</a>
```

**Recommendation:**
Confirm that all linked `.do` actions with state-changing behaviour are reached only via POST with a CSRF synchroniser token. Pure read/display actions reached via GET are lower risk but should still be reviewed for any side-effects (audit logging, access tracking) that could be CSRF-abused.

---

### FINDING-06 — LOW — Empty `src` Attributes on `<img>` Elements

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/adminReports.jsp`
**Lines:** 29, 38, 47

**Description:**
All three `<img>` elements have empty `src=""` attributes. This causes browsers to make an additional HTTP request to the current page URL (in some browsers) or to emit a console error, and it may result in broken image icons being displayed. While not a security vulnerability in isolation, empty image sources have historically been used as a vector for certain CSRF techniques (forcing a GET request to the current page URL) and represent poor coding hygiene.

**Evidence:**
```jsp
<a href="<%= incidentReportUrl %>" class="box-a"><img src="" class="box-a-img"/></a>
<a href="<%= sessionReportUrl %>" class="box-a"><img src="" class="box-a-img"/></a>
<a href="gpsreport.do" class="box-a"><img src="" class="box-a-img"/></a>
```

**Recommendation:**
Populate the `src` attributes with the correct image paths, or remove the `<img>` elements if they are placeholders not yet implemented.

---

## 3. Category Summary

| Category | Finding(s) | Status |
|----------|-----------|--------|
| XSS — Unescaped output to HTML/JS | FINDING-01 | Issue present (HIGH) |
| CSRF — POST forms / AJAX | FINDING-05 | Issue present (MEDIUM — structural gap, no forms but linked actions may have side-effects) |
| Authentication / Authorization — role checks | FINDING-04 | Issue present (MEDIUM) |
| Information Disclosure | FINDING-04 | Issue present (MEDIUM — feature enumeration) |
| Sensitive Data Rendered | No sensitive data (PII, credentials, tokens) is rendered in this file. | NO ISSUES |
| NullPointerException / Error Disclosure | FINDING-02 | Issue present (HIGH) |
| Logic / Routing Defect | FINDING-03 | Issue present (MEDIUM) |
| Code Quality | FINDING-06 | Issue present (LOW) |

---

## 4. Finding Count by Severity

| Severity | Count | Findings |
|----------|-------|---------|
| CRITICAL | 0 | — |
| HIGH     | 2 | FINDING-01, FINDING-02 |
| MEDIUM   | 3 | FINDING-03, FINDING-04, FINDING-05 |
| LOW      | 1 | FINDING-06 |
| INFO     | 0 | — |
| **TOTAL** | **6** | |

---

## 5. Notes for Follow-On Passes

- The target action classes for all five linked `.do` endpoints (`incidentreport.do`, `sessionreport.do`, `dealerIncidentReport.do`, `dealerSessionReport.do`, `gpsreport.do`) should be audited separately to confirm:
  - Company-scope enforcement (tenant isolation)
  - Dealer-vs-regular-user authorisation
  - Whether any GET path causes a state change (CSRF exposure)
- `importLib.jsp` imports Struts tag libraries but this JSP uses none of them; all dynamic output is raw scriptlet. A future refactor to JSTL/Struts tags would eliminate FINDING-01.
- The `isDealer` session attribute is set via `CompanySessionSwitcher` (called at login and on company switch); it is a Boolean stored as `Object` in session. The `.equals("true")` string comparison (lines 4–5) will silently return `false` when the stored value is a `Boolean` object, meaning dealer routing could silently fail even for dealer accounts — this is an additional logic defect worth verifying in integration testing.
