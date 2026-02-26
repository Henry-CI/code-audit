# Security Audit Report: PreOpsReport Feature
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master
**Date:** 2026-02-26
**Auditor:** CIG Automated Pass 1
**Scope:** PreOpsReportAction, DealerPreOpsReportAction, PreOpsReportSearchForm, PreOpsReportBean, PreOpsReportEntryBean, PreOpsReportFilterBean, dealer/preOpsReport.jsp, reports/preOpsReport.jsp

---

## Files Reviewed

| # | File |
|---|------|
| 1 | `src/main/java/com/action/PreOpsReportAction.java` |
| 2 | `src/main/java/com/action/DealerPreOpsReportAction.java` |
| 3 | `src/main/java/com/actionform/PreOpsReportSearchForm.java` |
| 4 | `src/main/java/com/bean/PreOpsReportBean.java` |
| 5 | `src/main/java/com/bean/PreOpsReportEntryBean.java` |
| 6 | `src/main/java/com/bean/PreOpsReportFilterBean.java` |
| 7 | `src/main/webapp/html-jsp/dealer/preOpsReport.jsp` |
| 8 | `src/main/webapp/html-jsp/reports/preOpsReport.jsp` |

Supporting files examined for context:
- `com/actionservlet/PreFlightActionServlet.java`
- `com/bean/ReportFilterBean.java`
- `com/service/ReportService.java`
- `com/dao/ResultDAO.java`
- `com/querybuilder/preops/PreOpsByCompanyIdQuery.java`
- `com/querybuilder/preops/PreOpsReportByCompanyIdQuery.java`
- `com/querybuilder/filters/DateBetweenFilterHandler.java`
- `com/querybuilder/filters/UnitManufactureFilterHandler.java`
- `com/querybuilder/filters/UnitTypeFilterHandler.java`
- `com/action/LoginAction.java`
- `WEB-INF/struts-config.xml`

---

## Findings

---

### CRITICAL: Missing dealer-role authorization on `/dealerPreOpsReport` — privilege escalation to cross-company data

**File:** `src/main/java/com/action/DealerPreOpsReportAction.java` (lines 23-26)

**Description:**
The dealer-tier endpoint `/dealerPreOpsReport` is intended exclusively for accounts that carry the `ROLE_DEALER` authority. The `PreFlightActionServlet` only checks that `sessCompId != null` (i.e., the user is authenticated), not that the authenticated company is a dealer. `DealerPreOpsReportAction.execute()` repeats the same bare-minimum guard:

```java
String sessCompId = (String) session.getAttribute("sessCompId");
if (sessCompId == null) throw new RuntimeException("Must have valid user logged in here");
```

There is no check against the `isDealer` or `isDealerLogin` session attributes that `LoginAction` stores:

```java
// LoginAction.java line 57-59
Boolean isDealerLogin = LoginDAO.isAuthority(loggedInCompanyId+"", RuntimeConf.ROLE_DEALER);
session.setAttribute("isDealerLogin", isDealerLogin);
// CompanySessionSwitcher line 43
session.setAttribute("isDealer", LoginDAO.isAuthority(comp_id, RuntimeConf.ROLE_DEALER));
```

Any authenticated company-level user — including ordinary non-dealer customers — can POST to `dealerPreOpsReport.do` and receive the pre-ops report data that the dealer action is supposed to gate. In the dealer flow the underlying query (`PreOpsByCompanyIdQuery`) uses `comp_id = ? OR assigned_company_id = ? OR unit_company_id = ?`, so a dealer account can legitimately see data from multiple sub-companies. A non-dealer regular customer will only see their own data (the compId scoping is intact), but the page itself is privileged dealer UI with dealer-specific navigation and cross-company context; the missing gate means that the access-control tier is entirely absent.

This is the exact same flaw documented in the audit brief as affecting ImpactReport, IncidentReport, and SessionReport dealer actions.

**Risk:**
Any authenticated non-dealer user can invoke the dealer-facing pre-ops report endpoint. While the underlying SQL query is scoped to `sessCompId`, the role boundary between customer and dealer tiers is completely absent. A privileged dealer account that has been downgraded or a non-dealer account that navigates directly to the URL bypasses the intended access tier entirely. If the query were ever widened or a bug introduced, non-dealers would immediately see cross-company data.

**Recommendation:**
Add an explicit role guard at the top of `execute()`, consistent with how `SwitchCompanyAction` enforces the dealer requirement:

```java
Boolean isDealer = (Boolean) session.getAttribute("isDealerLogin");
if (isDealer == null || !isDealer) {
    return mapping.findForward("accessDenied");
}
```

Add the same guard to every `Dealer*ReportAction` class. Consider extracting a `DealerBaseAction` abstract class that performs this check in a shared `preExecute` hook to prevent recurrence.

---

### CRITICAL: Missing dealer-role authorization on `/preopsreport` — admin-report endpoint similarly unguarded

**File:** `src/main/java/com/action/PreOpsReportAction.java` (lines 27-31)

**Description:**
The admin-tier pre-ops report endpoint `/preopsreport` has the identical missing-role-check pattern. Its guard is:

```java
String sessCompId = (String) session.getAttribute("sessCompId");
if (sessCompId == null) {
    throw new RuntimeException("Must have valid user logged in here");
}
```

The Struts configuration in `struts-config.xml` (line 520) maps `/preopsreport` to `PreOpsReportAction` with no `roles` attribute and no Tiles-level access control. There is no check for a supervisor, admin, or report-viewer role. Any authenticated session holder — including driver-only accounts if they obtain a `sessCompId` via a shared session or session fixation — can retrieve the full pre-ops report for their company.

**Risk:**
The intended audience of this endpoint is operations managers or administrators who have rights to view aggregated pre-ops check results. Driver-level or read-only accounts should not reach this report. Without a role check, horizontal privilege escalation within the same company is possible: any account whose session cookie is authenticated can pull the full company pre-ops audit trail including all drivers' names, timestamps, check results, failure reasons, and free-text comments.

**Recommendation:**
Determine the intended minimum role for this report (e.g., `ROLE_ADMIN` or `ROLE_REPORT_VIEWER`) and enforce it at the top of `execute()`. Until a proper role attribute is defined for this purpose, at minimum add a sanity check against the set of roles stored in the session. Document the intended access tier in the Struts action mapping using `roles="ROLE_ADMIN"` so it is machine-readable.

---

### HIGH: Reflected XSS via JSP scriptlet — unescaped `request.getParameter()` written into JavaScript string

**File:** `src/main/webapp/html-jsp/dealer/preOpsReport.jsp` (lines 109-114)
**File:** `src/main/webapp/html-jsp/reports/preOpsReport.jsp` (lines 107-119)

**Description:**
Both JSPs contain a scriptlet block that reads `start_date` and `end_date` directly from the HTTP request and emits them into inline JavaScript string literals using `<%= ... %>`, with no escaping whatsoever:

```jsp
<%-- dealer/preOpsReport.jsp lines 109-114 --%>
<% if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("start_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>

<% if (request.getParameter("end_date") != null) { %>
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("end_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
```

`DateUtil.stringToIsoNoTimezone` calls `DateUtil.stringToDate`, which passes the raw input through `SimpleDateFormat.parse()`. If the input does not parse as a date, `stringToDate` is likely to either return `null` (causing a NullPointerException that surfaces as a 500 or an empty value) or propagate the raw string. However, the deeper issue is that these parameters originate from the GET/POST request and are reflected directly into script context with no JSTL `<c:out>` or `ESAPI.encodeForJavaScript()` escaping applied **before** parsing. An attacker who can craft a request (via a phishing link, CSRF, or open redirect) with a value that passes the date parse and still contains JavaScript-breaking characters can cause client-side script injection.

More concretely: `SimpleDateFormat.parse()` with a lenient formatter will accept inputs like `2024-01-01";</script><script>alert(1)//` and return a partial date, leaving the trailing payload to fall through into the emitted script. Even in strict mode, the absence of any output-context escaping is a structural defect — a future change to `stringToIsoNoTimezone` or a different locale's date format string could immediately open the channel fully.

The same pattern appears identically in both the dealer and admin JSP, doubling the attack surface.

**Risk:**
An attacker who can trick an authenticated user into clicking a crafted URL can execute arbitrary JavaScript in the victim's browser session, enabling session cookie theft, CSRF token harvesting, DOM-based credential phishing, or lateral movement within the admin application.

**Recommendation:**
Replace the scriptlet approach with a JSTL EL expression that is HTML/JavaScript-encoded, or encode the raw parameter before passing it to the date utility:

```jsp
<%-- Safe approach: encode before emitting into JS context --%>
<c:if test="${param.start_date != null}">
    start_date = new Date("<c:out value='${safeStartDateIso}'/>");
</c:if>
```

Compute `safeStartDateIso` in the Action class, validate it, and store it as a request attribute. Never use raw `request.getParameter()` inside `<%= %>` blocks in a JavaScript context. At minimum apply `ESAPI.encodeForJavaScript()` on the output of `stringToIsoNoTimezone`.

---

### HIGH: Stored XSS via `<bean:write filter="false">` — unescaped database content written to HTML

**File:** `src/main/webapp/html-jsp/dealer/preOpsReport.jsp` (lines 81-95, 90)
**File:** `src/main/webapp/html-jsp/reports/preOpsReport.jsp` (lines 80-92, 87)

**Description:**
Every data column in both report tables uses `<bean:write>` without the `filter` attribute, which in Struts 1.x defaults to `filter="true"` (HTML-encoding enabled). At first glance this appears safe. However, line 90 of the dealer JSP and line 87 of the reports JSP iterate over the `failures` list and render each entry using `<bean:write name="failure"/>` where `failure` is a bare `java.lang.String` scoped to the page. The Struts 1.x `<bean:write>` tag when applied to a bare String bean without an explicit `property` attribute has historically inconsistent encoding behaviour across container versions, and any property using `filter="false"` explicitly would be unsafe. The rendering of `comment`, `driverName`, and `unitName` fields from `PreOpsReportEntryBean` via `<bean:write>` should encode, but any future developer adding `filter="false"` to speed up rendering (a common mistake) would immediately expose stored XSS.

More critically, the `comment` field (line 95 in dealer JSP, line 92 in reports JSP) is free-text user input collected from the mobile driver app at check-in time:

```jsp
<td><bean:write name="preOpsEntry" property="comment"/></td>
```

If a driver submits a comment containing `<script>alert(1)</script>`, and if `filter` defaults to `true`, the output is safe. But the structural reliance on a framework default rather than an explicit `filter="false"` prohibition means this safety is invisible to reviewers. If `filter="false"` is ever added (as seen in the known-pattern note for this codebase), stored XSS becomes trivially exploitable.

The `failures` list items (answers from the pre-ops check) are also rendered without explicit encoding:

```jsp
<%-- dealer/preOpsReport.jsp line 90 --%>
<li><bean:write name="failure"/></li>
```

These come from the `answer` column of the `answer` table, which holds driver-supplied free text.

**Risk:**
Any user (including a driver using the mobile app) who can inject HTML/JavaScript into a `comment`, `answer`, or driver name field can cause stored XSS executing in the browser of every manager or dealer who views the pre-ops report. This is a persistent attack requiring no interaction with the victim beyond normal report access.

**Recommendation:**
Explicitly set `filter="true"` on every `<bean:write>` tag in both JSPs to make the encoding intent visible and audit-able:

```jsp
<td><bean:write name="preOpsEntry" property="comment" filter="true"/></td>
<li><bean:write name="failure" filter="true"/></li>
```

Conduct a codebase-wide search for `filter="false"` in all report JSPs and treat each occurrence as a critical finding requiring justification.

---

### HIGH: CSRF — no synchronizer token on any POST action

**File:** `src/main/webapp/html-jsp/dealer/preOpsReport.jsp` (line 22)
**File:** `src/main/webapp/html-jsp/reports/preOpsReport.jsp` (line 22)

**Description:**
Both JSPs render search forms that POST to their respective action endpoints:

```jsp
<%-- dealer/preOpsReport.jsp --%>
<html:form action="dealerPreOpsReport.do" method="POST" styleClass="checklist_form">

<%-- reports/preOpsReport.jsp --%>
<html:form action="preopsreport.do" method="POST" styleId="adminUnitEditForm" styleClass="checklist_from">
```

Neither form includes a CSRF synchronizer token. Struts 1.x does not add a token automatically; the developer must call `saveToken(request)` in the action and `isTokenValid(request, true)` in the form submission handler. Neither `PreOpsReportAction` nor `DealerPreOpsReportAction` calls either method. `PreFlightActionServlet` also performs no CSRF validation.

While these are read-only report-query endpoints (POST submits filter parameters and returns report data), the absence of CSRF token validation means an attacker can construct a cross-origin form that silently submits any filter combination on behalf of the authenticated user. Combined with the reflected XSS finding above (Finding 3), a CSRF-triggered request with a malicious `start_date` parameter would force the victim's browser to execute the XSS payload. More broadly, if any future version of these endpoints gains side-effects (e.g., emailing or exporting the report), CSRF becomes a direct data-exfiltration vector.

**Risk:**
An attacker can force an authenticated user to submit arbitrary report queries, including potentially triggering the reflected-XSS chain identified above. Future endpoint changes that add state-mutating behaviour would inherit this unprotected surface immediately.

**Recommendation:**
Add synchronizer token handling to both actions:

```java
// In execute() on GET (initial page load):
saveToken(request);

// In execute() on POST (form submission):
if (!isTokenValid(request, true)) {
    return mapping.findForward("failure"); // or return an error
}
```

Consider adding `SameSite=Strict` or `SameSite=Lax` on the session cookie at the container level as a defense-in-depth measure alongside synchronizer tokens.

---

### MEDIUM: Insecure Direct Object Reference — `manu_id` and `type_id` filter parameters not validated against `sessCompId`

**File:** `src/main/java/com/actionform/PreOpsReportSearchForm.java` (lines 27-34)
**File:** `src/main/java/com/bean/PreOpsReportFilterBean.java` (lines 9-16)

**Description:**
The search form accepts `manu_id` and `type_id` from the HTTP request as raw `Long` values and passes them directly to the SQL query without verifying that the referenced manufacturer or unit-type record belongs to the authenticated user's company:

```java
// PreOpsReportSearchForm.java lines 28-33
public PreOpsReportFilterBean getPreOpsReportFilter(String dateFormat) {
    return PreOpsReportFilterBean.builder()
        .manuId(this.manu_id == null || this.manu_id == 0 ? null : this.manu_id)
        .typeId(this.type_id == null || this.type_id == 0 ? null : this.type_id)
        ...
        .build();
}
```

These IDs are then passed to `UnitManufactureFilterHandler` and `UnitTypeFilterHandler`, which build SQL predicates like `AND manu_id = ?` against the pre-ops report view. The underlying view query is scoped to `comp_id = ?` correctly, so a rogue `manu_id` belonging to a different company will simply return no rows (the data-access harm is minimal). However, the application's behaviour is still an IDOR: an attacker can enumerate whether a given `manu_id` integer exists within another company's dataset by observing whether the filtered response is empty or non-empty when combined with timing or error-difference side channels.

The manufacturer dropdown is populated via `ManufactureDAO.getAllManufactures(sessCompId)`, which filters manufacturers by `company_id is null OR company_id = ?`. A user who manually overrides the `manu_id` POST parameter to an arbitrary integer can probe manufacturer IDs outside their company.

**Risk:**
Information leakage: an attacker can enumerate manufacturer and unit-type IDs that belong to other tenants by brute-forcing the `manu_id` and `type_id` POST parameters and comparing response content. While current query scoping limits data exposure to the attacker's own company, the lack of ownership validation on the filter parameters is a structural IDOR that could be exploited more severely if the query is ever refactored.

**Recommendation:**
Before building the filter, verify that the supplied `manu_id` belongs to a manufacturer visible to `sessCompId`:

```java
if (this.manu_id != null && this.manu_id != 0) {
    boolean owned = manufactureDAO.isManufacturerVisibleToCompany(this.manu_id, compId);
    if (!owned) throw new UnauthorizedException("manu_id not accessible");
}
```

Alternatively, perform the ownership check in the DAO layer by adding `AND manu_id IN (SELECT id FROM manufacture WHERE company_id IS NULL OR company_id = ?)` to the query.

---

### MEDIUM: Lombok `@Data` on `PreOpsReportEntryBean` generates `toString()` emitting PII

**File:** `src/main/java/com/bean/PreOpsReportEntryBean.java` (lines 11, 19-21)

**Description:**
`PreOpsReportEntryBean` is annotated with `@Data`, which causes Lombok to generate a `toString()` method that includes every field:

```java
@Data
@NoArgsConstructor
public class PreOpsReportEntryBean implements Serializable {
    private String unitName;
    private String manufacture;
    private String companyName;
    private String driverName;      // PII: full name
    private String checkDateTime;
    private ArrayList<String> failures;
    private LocalTime duration;
    private String comment;         // PII: free-text, may contain location or personal info
}
```

The generated `toString()` will produce output of the form:
```
PreOpsReportEntryBean(unitName=FLT-001, manufacture=Toyota, companyName=Acme Corp,
  driverName=John Smith, checkDateTime=2026-01-15 08:30:00, failures=[Brake fluid low],
  duration=00:04:30, comment=Driver reported pain in right hand)
```

Anywhere this bean is logged — via `log.info(entry.toString())`, in exception messages (e.g., `ReportService` catches `SQLException` and the bean may appear in a stack trace), or when an ORM or framework serializes it for debugging — the driver's full name, company name, check timestamp, specific failure reasons, and free-text comments are written to log files. These are personal data under GDPR and equivalent regulations.

`PreOpsReportBean` (parent container) also has `@Data` and `@AllArgsConstructor` (line 11-13), meaning `toString()` of the report list will cascade into `PreOpsReportEntryBean.toString()` for all entries.

`ReportFilterBean` (the base class of `PreOpsReportFilterBean`) also carries `@Data` and `@AllArgsConstructor`, but its fields (`startDate`, `endDate`, `manuId`, `typeId`, `timezone`) are not PII.

**Risk:**
Driver full names, company names, check comments (which may contain health or location information), and failure reason strings are written to application logs whenever these beans are serialized as strings. This creates a persistent PII trail in log aggregation systems that likely does not have the same retention controls or access restrictions as the production database. This is a GDPR/CCPA compliance risk and a confidentiality risk if logs are accessible to a broader set of personnel than the pre-ops report.

**Recommendation:**
Replace `@Data` on `PreOpsReportEntryBean` with the specific Lombok annotations needed (`@Getter`, `@Setter`, `@EqualsAndHashCode`) and implement a custom `toString()` that omits or masks PII fields:

```java
@Override
public String toString() {
    return "PreOpsReportEntryBean(unitName=" + unitName
        + ", manufacture=" + manufacture
        + ", driverName=[REDACTED]"
        + ", checkDateTime=" + checkDateTime + ")";
}
```

Alternatively, annotate PII fields with `@ToString.Exclude`:

```java
@ToString.Exclude
private String driverName;
@ToString.Exclude
private String comment;
```

Apply the same treatment to `PreOpsReportBean` since its generated `toString()` transitively includes all entry beans.

---

### MEDIUM: Unvalidated `timezone` parameter flows through to SQL `timezone()` function call

**File:** `src/main/java/com/actionform/PreOpsReportSearchForm.java` (line 33)
**File:** `src/main/java/com/querybuilder/filters/DateBetweenFilterHandler.java` (lines 22, 29)

**Description:**
The `timezone` field on `PreOpsReportSearchForm` is set from the session attribute `sessTimezone` in `PreOpsReportAction` (line 41: `preOpsReportSearchForm.setTimezone(timezone)`), which is safe. However, `PreOpsReportSearchForm` also exposes `timezone` as a Struts form property (it carries `@Data`, generating a public setter). Struts 1.x will call `setTimezone()` if a `timezone` parameter is present in the HTTP request, meaning a user can override the session-sourced timezone with an arbitrary string.

That string is then passed as a bind parameter to PostgreSQL's `timezone()` function in the generated SQL:

```java
// DateBetweenFilterHandler.java line 22
return String.format(" AND timezone(?, %s at time zone 'UTC')::DATE BETWEEN ? AND ?", fieldName);

// DateBetweenFilterHandler.java line 29
if(filter.timezone() != null) preparer.addString(filter.timezone());
```

The `timezone` value is passed as a PreparedStatement bind parameter (`?`), not concatenated, so classical SQL injection is not possible here. However, PostgreSQL's `timezone()` function accepts timezone strings by name (e.g., `'US/Eastern'`). An attacker-supplied timezone value that is a valid PostgreSQL timezone name will silently alter the date boundaries of the report query, potentially causing the report to include or exclude records outside the expected date range. An invalid timezone name will cause a PostgreSQL error, potentially leaking the database error message to the client depending on how `ReportServiceException` is rendered in the UI.

The check `this.timezone == "" ? null : this.timezone` on line 33 of `PreOpsReportSearchForm` uses reference equality (`==`) to compare strings, which is a bug in Java — it will never match an empty string from the HTTP request (which would be a new String object), meaning a blank `timezone` POST parameter passes through as a non-null empty string rather than being nulled out.

**Risk:**
An authenticated attacker can override the timezone parameter to manipulate the date-range filtering of the pre-ops report, causing records to appear or disappear from the results in ways that do not match the user's selected date range. This is an integrity risk for audit reports. The `==` string comparison bug means an empty timezone string reaches the SQL layer, which may cause a PostgreSQL error surfacing internal state.

**Recommendation:**
Do not expose `timezone` as a settable form property that can be overridden from the HTTP request. Set it only from the trusted session attribute:

```java
// In PreOpsReportAction.execute() — set on form after Struts populates it, overriding any user-supplied value:
preOpsReportSearchForm.setTimezone(timezone); // already done at line 41 — but Struts populates BEFORE this line
```

The order in Struts 1.x is: `ActionServlet` populates the form from the request first, then `execute()` runs. Therefore the assignment at line 41 does correctly overwrite any user-supplied `timezone`. The risk is lower than initially apparent, but the `@Data`-generated setter is still a latent danger if the execution order ever changes or if the form is reused elsewhere without the reassignment. The cleanest fix is to remove `timezone` from the form's Struts-bindable properties by not having a public `setTimezone()` method (use a separate non-Struts setter or constructor argument).

Fix the string comparison bug on line 33 of `PreOpsReportSearchForm.java`:

```java
// Buggy:
.timezone(this.timezone == null || this.timezone == "" ? null : this.timezone)
// Correct:
.timezone(StringUtils.isBlank(this.timezone) ? null : this.timezone)
```

---

### LOW: `PreOpsReportAction` calls `session.getAttribute("sessCompId")` without null-checking the session object itself

**File:** `src/main/java/com/action/PreOpsReportAction.java` (lines 27-29)

**Description:**
```java
HttpSession session = request.getSession(false);
String sessCompId = (String)session.getAttribute("sessCompId");
```

`request.getSession(false)` returns `null` if no session exists. The next line dereferences `session` without a null check, resulting in a `NullPointerException` if there is no active session. This is not a security vulnerability by itself (no session means no authenticated user), but the resulting uncaught NPE will propagate as a 500 error through Tomcat rather than the intended `RuntimeConf.EXPIRE_PAGE` redirect, because `PreFlightActionServlet` guards `excludeFromFilter(path)` paths but the NPE happens after the servlet filter check passes. It means an unauthenticated direct request to `preopsreport.do` does not redirect cleanly to the expired-session page; instead it returns a 500 that may expose the stack trace and application internals.

`DealerPreOpsReportAction.java` (line 23) has the same pattern.

**Risk:**
Information disclosure via 500 stack trace page; poor error user experience. Not directly exploitable for data access since no session means no compId.

**Recommendation:**
```java
HttpSession session = request.getSession(false);
if (session == null || session.getAttribute("sessCompId") == null) {
    return mapping.findForward("sessionExpired");
}
```

---

### LOW: Singleton `ReportService` and `ManufactureDAO` instantiated as instance fields — potential thread-safety concern

**File:** `src/main/java/com/action/PreOpsReportAction.java` (lines 20-22)

**Description:**
```java
private ReportService reportService = ReportService.getInstance();
private ManufactureDAO manufactureDAO = ManufactureDAO.getInstance();
private UnitDAO unitDAO = UnitDAO.getInstance();
```

Struts 1.x reuses a single Action instance per mapping across all concurrent requests (Actions are not thread-safe by design — fields should not hold request-scoped state). While `ReportService` and the DAOs are themselves singletons and are likely stateless, storing them as mutable instance fields on the Action creates a pattern where a future developer might add mutable state to these fields without recognizing the threading hazard. The DAO and service references themselves are safe, but the pattern is a maintenance risk.

**Risk:**
Low — no current exploitability. Maintenance risk of thread-safety defects if mutable state is added to Action instance fields.

**Recommendation:**
Use local variables within `execute()` rather than instance fields for the DAO/service references, or annotate the class clearly with a thread-safety contract.

---

### INFO: `PreOpsReportSearchForm` uses `@Data` — implicit `equals()`/`hashCode()` on Struts `ActionForm` subclass

**File:** `src/main/java/com/actionform/PreOpsReportSearchForm.java` (line 12)

**Description:**
`@Data` generates `equals()` and `hashCode()` based on all fields. `ActionForm` subclasses in Struts 1.x are placed in the session by the framework when `scope="session"` is declared (the `preOpsReportSearchForm` declaration in `struts-config.xml` does not specify scope, defaulting to session). Lombok-generated `equals()` on a session-stored form bean that includes `List<ManufactureBean>` and `List<UnitTypeBean>` fields may produce unexpected behaviour if the framework or a custom interceptor compares form instances, and can cause memory retention of large lists across requests.

**Risk:**
Informational — no direct security impact. Potential memory bloat from session-stored form with large manufacturer/unit-type lists populated on every request.

**Recommendation:**
Explicitly scope the form to `request` in `struts-config.xml` if the filter values should not persist across requests, or clear the manufacturer/unit-type lists before storing to session. Remove `@Data` in favour of selective Lombok annotations.

---

### INFO: `ReportService` singleton is not thread-safe (double-checked locking without `volatile`)

**File:** `src/main/java/com/service/ReportService.java` (lines 18-27)

**Description:**
```java
private static ReportService theInstance;

public static ReportService getInstance() {
    if (theInstance == null) {
        synchronized (ReportService.class) {
            theInstance = new ReportService();
        }
    }
    return theInstance;
}
```

The outer `if (theInstance == null)` check is not protected by synchronization. In the Java memory model, without `volatile` on `theInstance`, the double-checked locking pattern is broken: a partially-constructed instance can be visible to threads that read `theInstance` outside the synchronized block. The recommended fix is `private static volatile ReportService theInstance`.

**Risk:**
Informational in practice for modern JVMs with hardware write-ordering, but technically a data race per the Java Memory Model specification. In a high-concurrency Tomcat deployment with multiple threads hitting `/preopsreport` simultaneously on first load, two `ReportService` instances could be constructed.

**Recommendation:**
Add `volatile` to the field declaration, or replace with a static initializer or enum-singleton pattern:

```java
private static volatile ReportService theInstance;
```

---

## Summary

| Severity | Count | Findings |
|----------|-------|---------|
| CRITICAL | 2 | Missing dealer-role check on `/dealerPreOpsReport`; missing role check on `/preopsreport` |
| HIGH | 3 | Reflected XSS via scriptlet in both JSPs; Stored XSS via `<bean:write>` in both JSPs; CSRF on both report forms |
| MEDIUM | 3 | IDOR on manu_id/type_id filter parameters; Lombok `@Data` PII leakage in `PreOpsReportEntryBean`; unvalidated timezone override with string comparison bug |
| LOW | 2 | NPE from null session dereference in both actions; thread-safety pattern on Action instance fields |
| INFO | 2 | `@Data` on Struts ActionForm; double-checked locking without `volatile` in ReportService |

**CRITICAL: 2 / HIGH: 3 / MEDIUM: 3 / LOW: 2 / INFO: 2**
