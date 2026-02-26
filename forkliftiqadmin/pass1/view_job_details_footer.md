# Security Audit Report — Pass 1
**Files audited:**
- `src/main/webapp/html-jsp/vehicle/view_job_details.jsp`
- `src/main/webapp/includes/footer.inc.jsp`

**Application:** ForkliftIQ Admin — Apache Struts 1.3.10 / Tomcat
**Auditor:** Claude (automated pass)
**Date:** 2026-02-26
**Branch:** master

---

## Supporting context examined

The following additional files were read to provide full context for these findings:

| File | Purpose |
|------|---------|
| `src/main/java/com/bean/JobDetailsBean.java` | Bean whose properties are rendered by the JSP |
| `src/main/java/com/action/DriverJobDetailsAction.java` | Action that populates `arrJobDetails` |
| `src/main/java/com/dao/JobsDAO.java` | SQL queries that load job data from the database |
| `src/main/java/com/actionservlet/PreFlightActionServlet.java` | Auth gate / session check |
| `src/main/webapp/WEB-INF/tiles-defs.xml` | Tile definitions — confirms layout and included footer |
| `src/main/webapp/WEB-INF/struts-config.xml` | Action mappings (`/driverjob`, `/jobdetails`, `/driverjobreq`) |
| `src/main/webapp/WEB-INF/web.xml` | Filter chain — confirms absence of CSRF filter |
| `src/main/webapp/includes/importLib.jsp` | Tag-library imports used by both files |
| `src/main/webapp/includes/header.inc.jsp` | Full-page header (JS/CSS resource references) |
| `src/main/webapp/includes/header_pop.inc.jsp` | Pop-up header used by `driverJobDetailsDefinition` |
| `src/main/webapp/includes/privacyText.jsp` | Content included by `footer.inc.jsp` |
| `src/main/webapp/html-jsp/vehicle/driver_job_details.jsp` | Related form rendered via the same tile set |

---

## Findings

---

### HIGH: SQL Injection in `getJobListByJobId` — `jobNo` parameter concatenated into query

**File:** `src/main/java/com/dao/JobsDAO.java` (line 123) — called from `DriverJobDetailsAction.java` (line 52) which is triggered when `view_job_details.jsp` is rendered

**Description:**
The `DriverJobDetailsAction` passes the raw, unvalidated request parameter `job_no` directly into `JobsDAO.getJobListByJobId()`. Inside that method the value is concatenated into a `Statement`-based SQL query with no parameterisation:

```java
// DriverJobDetailsAction.java line 38
String jobNo = request.getParameter("job_no") == null ? "" : request.getParameter("job_no");

// JobsDAO.java line 123
String sql = "select j.id, j.unit_id, ja.driver_id, ... "
           + "from jobs j, job_allocation ja, job_sessions js "
           + "where ... and j.unit_id = " + equipId
           + " and j.job_no = '" + jobNo + "' order by js.start_time";
stmt.executeQuery(sql);
```

Both `equipId` and `jobNo` are user-controlled strings appended directly to the SQL string. An authenticated attacker can inject arbitrary SQL (e.g., `' OR '1'='1`) to read all job records across all tenants, escalate to blind or union-based extraction, or (depending on database permissions) cause additional damage.

The companion method `getJobList(String equipId)` (line 52) has the same problem for `equipId`.

**Risk:**
An authenticated user can bypass the `sessCompId` tenant boundary entirely, reading or potentially modifying job data belonging to other companies. Because `view_job_details.jsp` renders whatever rows the DAO returns, a successful injection that expands the result set will also cause that cross-tenant data to appear in the browser (information disclosure compounding the injection).

**Recommendation:**
Replace `Statement` with `PreparedStatement` and bind all user-supplied values as parameters:

```java
String sql = "select j.id, j.unit_id, ja.driver_id, ... "
           + "from jobs j, job_allocation ja, job_sessions js "
           + "where j.id = ja.job_id and j.id = js.job_id "
           + "and j.unit_id = ? and j.job_no = ? "
           + "order by js.start_time";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, equipId);
ps.setString(2, jobNo);
```

Additionally, enforce the tenant boundary in the query by joining on the company ID so a valid `equipId` belonging to another tenant cannot be queried.

---

### HIGH: Missing Tenant Isolation — `equipId` / `job_no` not validated against `sessCompId`

**File:** `src/main/java/com/action/DriverJobDetailsAction.java` (lines 36–53)

**Description:**
`DriverJobDetailsAction` reads `sessCompId` from the session but never uses it when querying job details. The call that populates `view_job_details.jsp` is:

```java
String sessCompId = (String) session.getAttribute("sessCompId") == null ? ""
                  : (String) session.getAttribute("sessCompId");
String equipId = request.getParameter("equipId") == null ? ""
               : request.getParameter("equipId");
String jobNo = request.getParameter("job_no") == null ? ""
             : request.getParameter("job_no");

if (action.equalsIgnoreCase("details")) {
    ArrayList<JobDetailsBean> jobs = jobsDAO.getJobListByJobId(equipId, jobNo);
    request.setAttribute("arrJobDetails", jobs);
    return mapping.findForward("details");
}
```

`sessCompId` is never passed to the DAO. Any authenticated user belonging to company A can supply an `equipId` that belongs to company B and retrieve that company's job details. The rendered page (`view_job_details.jsp`) will faithfully display the cross-tenant driver names, job numbers, timestamps, and durations.

**Risk:**
Broken Object-Level Authorization (BOLA / IDOR). An attacker authenticated as any tenant can enumerate all job records in the system by iterating numeric `equipId` values.

**Recommendation:**
Pass `sessCompId` into the DAO and add a SQL join (or WHERE clause) that restricts results to equipment owned by that company, e.g.:

```sql
... WHERE j.unit_id = ? AND j.job_no = ? AND u.company_id = ?
```

where `u` is the `units` (equipment) table and the third bind parameter is `sessCompId`.

---

### MEDIUM: Reflected XSS via `<bean:write>` — default `filter` attribute behaviour requires verification

**File:** `src/main/webapp/html-jsp/view_job_details.jsp` (lines 24, 27, 41, 44, 47)

**Description:**
All data-bearing tags in the JSP use `<bean:write>` without an explicit `filter` attribute:

```jsp
<label><bean:write name="jobDetails" property="driverName" /></label>   <!-- line 24 -->
<label><bean:write name="jobDetails" property="jobNo" /></label>         <!-- line 27 -->
<label><bean:write name="jobDetails" property="startTime" /></label>     <!-- line 41 -->
<label><bean:write name="jobDetails" property="endTime" /></label>       <!-- line 44 -->
<label><bean:write name="jobDetails" property="duration" /></label>      <!-- line 47 -->
```

In Struts 1.x the `filter` attribute defaults to `true`, which causes `<bean:write>` to HTML-encode the output. This is the safer default. **However**, the actual XSS risk here is elevated above INFO level for three reasons:

1. The backing `JobDetailsBean` fields (`driverName`, `jobNo`, `startTime`, `endTime`) are all `String` types with no input sanitisation applied at the DAO or action layer. If malicious content was stored in the database (e.g., via SQL injection as described above, or via an unsanitised data-entry form elsewhere in the application), it will be stored raw.
2. The Struts 1.3.10 `bean:write` `filter="true"` encodes only the five XML/HTML characters (`< > & " '`). It does not protect against all XSS vectors (e.g., `javascript:` in attribute contexts). The properties are output directly into HTML element text content, which is the safest context; in this layout the risk is lower.
3. If any developer ever adds `filter="false"` to any of these tags (as is already done in several other JSPs in this codebase — see companion findings), stored XSS becomes trivially exploitable given the SQL injection vector above.

**Risk:**
Stored XSS if input sanitation is absent elsewhere in the pipeline and data is persisted without encoding. Medium in current form (relies on missing encoding in data-entry paths); HIGH if `filter="false"` is ever added.

**Recommendation:**
- Add `filter="true"` explicitly to every `<bean:write>` tag so the intent is unambiguous and immune to future Struts configuration changes.
- Apply input validation and HTML-encoding at the point data enters the database, not only at output.
- Audit all data-entry forms that write to the `jobs`, `job_sessions`, and `job_allocation` tables.

---

### MEDIUM: No CSRF Protection on the `driverjobreq.do` Form

**File:** `src/main/webapp/html-jsp/vehicle/driver_job_details.jsp` (line 14) — rendered via the same `driverJobDetailsDefinition` tile set as `view_job_details.jsp`; `src/main/webapp/WEB-INF/web.xml` (entire file)

**Description:**
The form that submits driver-assignment data uses Struts `<html:form>`:

```jsp
<html:form method="post" action="driverjobreq.do" styleClass="ajax_mode_c assign_driver">
    ...
    <html:hidden property="equipId" value="<%=id %>"></html:hidden>
    <html:hidden property="jobId" value="<%=jobId %>"></html:hidden>
    <html:hidden property="action" value="assign_driver"></html:hidden>
    ...
</html:form>
```

Struts 1.x does not generate or validate synchroniser tokens automatically unless the developer explicitly calls `saveToken(request)` in the action and `isTokenValid(request)` on submission. Searching `web.xml` reveals only a `CharsetEncodingFilter`; there is no CSRF filter. Searching `DriverJobDetailsAction` shows no calls to `saveToken` or `isTokenValid`.

Any page on the internet can therefore cause an authenticated administrator's browser to submit this form by embedding an `<img>` or `<form>` pointing at `driverjobreq.do`.

**Risk:**
A cross-site request forgery attack can reassign forklift drivers to different jobs, modify job start/end times, or submit arbitrary driver-assignment data on behalf of an authenticated company administrator, without their knowledge.

**Recommendation:**
Implement synchroniser-token CSRF protection in Struts 1.x:

1. In the action that renders the form, call `saveToken(request)`.
2. In `DriverJobDetailsAction.execute()` for the `assign_driver` branch, call `isTokenValid(request, true)` and return an error forward if the check fails.

Alternatively, add a servlet filter that validates the `Referer` or `Origin` header as a defence-in-depth measure for all state-changing `.do` requests.

---

### MEDIUM: Information Disclosure — Internal Company Identity Exposed in Footer Modal

**File:** `src/main/webapp/includes/footer.inc.jsp` (line 20)

**Description:**
The privacy-policy modal hard-codes the company name in the HTML title:

```html
<h4 class="modal-title">CIIQ UK LTD PRIVACY POLICY</h4>
```

More significantly, `privacyText.jsp` (included at line 23) contains extensive operational information that is served to all authenticated sessions and is part of the DOM on every admin page:

- Full registered company name and trading names (lines 321–350 of `privacyText.jsp`)
- Physical postal address: `Unit 3 Bowdens Business Centre, Bowdens Farm, Hambridge, Nr Curry Rivel, Somerset TA10 0BP, United Kingdom`
- Direct contact email: `dp@ciiquk.com`
- Direct telephone number: `01460 259101`
- Partner company names including MHE providers: `Linde Material Handling UK`, `Westexe Forklifts Ltd` (line 304)
- Live production system hostnames: `fms.fleetiq360.com`, `pandora.fleetiq360.com` (lines 34–42)

Although some of this is intentional disclosure (GDPR requires a contact point), the production system URLs and partner names are directly accessible from the admin panel's DOM on every page load without requiring any further authentication step, making them trivially discoverable by any attacker who gains even read-only access to a single session.

**Risk:**
An attacker who compromises any session token gains immediate knowledge of production system hostnames to target, real staff contact details for spear-phishing, and the supply-chain partner relationships useful for social engineering.

**Recommendation:**
- Separate the GDPR contact-details page from the admin panel. Serve it from a public-facing URL instead of embedding it in the authenticated admin footer on every page.
- Remove production hostnames (`fms.fleetiq360.com`, `pandora.fleetiq360.com`) from the privacy text; link to an external public privacy policy URL instead of inlining the full text.
- Replace hard-coded partner names in the inline text with a reference to an external policy document.

---

### LOW: Empty `href` Attributes on Footer Anchor Tags

**File:** `src/main/webapp/includes/footer.inc.jsp` (lines 3, 5)

**Description:**
Two anchor elements in the footer have empty `href` attributes:

```html
<a href="" data-toggle="modal" data-target="#privacymodal">
    <bean:message key="footer.privacy"></bean:message>
</a>
| <a href="" target="_blank"><bean:message key="footer.term"></bean:message></a>
```

The first link (`footer.privacy`) launches a Bootstrap modal and is functionally harmless because `href=""` simply reloads the current page before the modal opens. The second link (`footer.term`, Terms of Use) opens with `target="_blank"` but `href=""` — it opens the current page in a new tab, meaning users who click "Terms" see the admin dashboard again rather than any terms document.

While neither is a direct security vulnerability, the `target="_blank"` link without a destination represents an unfinished feature stub that may be connected to a real URL in the future. If an `href` pointing to an external site is later added, the absence of `rel="noopener noreferrer"` would expose the application to a reverse tabnapping attack.

**Risk:**
Broken UI feature (Terms link does nothing useful). Future introduction of an external URL without `rel="noopener noreferrer"` would create a low-severity reverse tabnapping vector.

**Recommendation:**
- Point `footer.term` at the actual Terms of Use URL or remove the link until the document exists.
- Add `rel="noopener noreferrer"` to the `target="_blank"` anchor now, before an external URL is added:

```html
<a href="/terms" target="_blank" rel="noopener noreferrer">
    <bean:message key="footer.term"></bean:message>
</a>
```

---

### LOW: Privacy Policy Last-Updated Date Is Stale (2018)

**File:** `src/main/webapp/includes/privacyText.jsp` (line 12)

**Description:**
```html
1.5 This policy was last updated on 21st May 2018.
```

The policy is served on every authenticated admin page and references GDPR obligations (including right-to-erasure, data-subject rights, and data-transfer safeguards). A policy dated 2018 is likely to be materially out of date relative to current GDPR guidance, UK GDPR post-Brexit, and any subsequent changes in processing activity. This is primarily a legal/compliance risk rather than a technical security issue.

**Risk:**
Regulatory non-compliance risk under UK GDPR Article 13/14 (transparency obligations). May also mislead users about the actual data practices in use today.

**Recommendation:**
Review and update the privacy policy to reflect current data processing activities and bring it into line with current UK GDPR guidance. Update the "last updated" date and implement a change-management process so the policy is reviewed at least annually.

---

### LOW: No `X-Frame-Options` / CSP `frame-ancestors` — Clickjacking Risk on Tile Pages

**File:** `src/main/webapp/WEB-INF/web.xml` (entire file); `src/main/webapp/includes/header.inc.jsp`

**Description:**
The `web.xml` defines only a `CharsetEncodingFilter`. Neither the header JSP nor any filter sets `X-Frame-Options` or a `Content-Security-Policy: frame-ancestors` directive. The `driverJobDetailsDefinition` tile (`view_job_details.jsp`) can therefore be loaded inside an `<iframe>` by a third-party page.

**Risk:**
A clickjacking attack could overlay transparent iframes over the job-details modal, tricking an authenticated administrator into clicking UI elements — including the driver-assignment form submit button — while believing they are interacting with a benign page.

**Recommendation:**
Add a security-headers filter to `web.xml` that sets the following response headers on all responses:

```
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: frame-ancestors 'self'
X-Content-Type-Options: nosniff
```

---

### INFO: `<bean:write filter="false">` Usage Absent in These Two Files — Confirmed Safe Defaults

**File:** `src/main/webapp/html-jsp/vehicle/view_job_details.jsp` (lines 24, 27, 41, 44, 47)

**Description:**
All five `<bean:write>` usages in `view_job_details.jsp` rely on the Struts 1.x default of `filter="true"` (HTML-escaping enabled). No `filter="false"` pattern appears in either audited file. This is the correct behaviour. The note is recorded here to document the audit finding explicitly so future code reviewers know this was checked.

**Risk:** None in current code.

**Recommendation:** Explicitly add `filter="true"` to each tag to protect against inadvertent future changes and to make the intent clear in code review.

---

### INFO: `Calendar.getInstance().get(Calendar.YEAR)` — Scriptlet in Footer

**File:** `src/main/webapp/includes/footer.inc.jsp` (line 2)

**Description:**
```jsp
&copy; <%= Calendar.getInstance().get(Calendar.YEAR)%>
```

This is a JSP scriptlet (`<%= ... %>`) used to render the copyright year. The value is server-side generated (not user-controlled) and is a numeric integer. There is no XSS risk here. However, the use of scriptlets is considered deprecated best practice; it is included here as an informational note for code quality purposes.

**Risk:** None — the integer output is not attacker-controlled.

**Recommendation:** For code-quality consistency, replace with a Struts `<bean:write>` or JSTL `<fmt:formatDate>` tag rather than a scriptlet, in line with best-practice JSP coding standards.

---

### INFO: `driverJobDetailsDefinition` Tile Extends `loginDefinition` — Confirms No Admin Footer

**File:** `src/main/webapp/WEB-INF/tiles-defs.xml` (lines 34–37)

**Description:**
```xml
<definition name="driverJobDetailsDefinition" extends="loginDefinition">
    <put name="header" value="/includes/header_pop.inc.jsp"/>
    <put name="content" value="/html-jsp/vehicle/view_job_details.jsp"/>
</definition>
```

`driverJobDetailsDefinition` extends `loginDefinition` (which uses `tilesTemplateHeader.jsp` — a layout with header only, no footer slot). This means `footer.inc.jsp` is **not** included on the `view_job_details.jsp` page. The footer findings above apply to all pages using `adminDefinition` or `fleetcheckDefinition`, not to the job-details modal view.

This is recorded as an informational finding to clarify scope: the SQL injection, IDOR, and CSRF findings affect `view_job_details.jsp` via its action and related forms; the footer information-disclosure findings affect a different set of pages.

**Risk:** None — this is a scoping clarification.

**Recommendation:** No action required for this finding.

---

## Summary

| # | Severity | Title | File(s) |
|---|----------|-------|---------|
| 1 | HIGH | SQL Injection — `jobNo` and `equipId` concatenated into Statement query | `JobsDAO.java:123`, `DriverJobDetailsAction.java:52` |
| 2 | HIGH | Missing tenant isolation — `equipId` not validated against `sessCompId` | `DriverJobDetailsAction.java:49-55` |
| 3 | MEDIUM | Reflected/Stored XSS risk — `<bean:write>` without explicit `filter="true"` | `view_job_details.jsp:24,27,41,44,47` |
| 4 | MEDIUM | No CSRF protection on `driverjobreq.do` driver-assignment form | `driver_job_details.jsp:14`, `web.xml` |
| 5 | MEDIUM | Information disclosure — production hostnames and contact details in footer modal | `footer.inc.jsp:23`, `privacyText.jsp:34-42,321-350` |
| 6 | LOW | Empty `href` on footer Terms link + missing `rel="noopener noreferrer"` | `footer.inc.jsp:5` |
| 7 | LOW | Privacy policy last-updated date stale (2018) | `privacyText.jsp:12` |
| 8 | LOW | No `X-Frame-Options` / CSP `frame-ancestors` — clickjacking possible | `web.xml`, `header.inc.jsp` |
| 9 | INFO | `<bean:write filter="false">` absent — default escaping confirmed | `view_job_details.jsp` |
| 10 | INFO | `<%= Calendar.YEAR %>` scriptlet in footer — non-user-controlled | `footer.inc.jsp:2` |
| 11 | INFO | `driverJobDetailsDefinition` extends `loginDefinition` — footer not included on this tile | `tiles-defs.xml:34` |

---

**CRITICAL: 0 / HIGH: 2 / MEDIUM: 3 / LOW: 3 / INFO: 3**
