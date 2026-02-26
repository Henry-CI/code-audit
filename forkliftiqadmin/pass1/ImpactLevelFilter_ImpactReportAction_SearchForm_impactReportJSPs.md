# Security Audit Report
## Scope: ImpactLevelFilter, ImpactReportAction, ImpactReportSearchForm, impactReport JSPs
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master
**Audit Date:** 2026-02-26
**Pass:** 1

### Files Audited
1. `src/main/java/com/querybuilder/filters/ImpactLevelFilter.java`
2. `src/main/java/com/querybuilder/filters/ImpactLevelFilterHandler.java`
3. `src/main/java/com/action/ImpactReportAction.java`
4. `src/main/java/com/actionform/ImpactReportSearchForm.java`
5. `src/main/webapp/html-jsp/dealer/impactReport.jsp`
6. `src/main/webapp/html-jsp/reports/impactReport.jsp`

**Supporting files reviewed for context:**
- `com/querybuilder/impacts/ImpactsByCompanyIdQuery.java`
- `com/querybuilder/impacts/ImpactsReportByCompanyIdQuery.java`
- `com/querybuilder/filters/DateBetweenFilterHandler.java`
- `com/querybuilder/filters/UnitManufactureFilterHandler.java`
- `com/dao/ImpactReportDAO.java`
- `com/service/ReportService.java`
- `com/bean/ImpactReportFilterBean.java`
- `com/bean/ImpactReportGroupEntryBean.java`
- `com/util/ImpactUtil.java`
- `com/util/DateUtil.java`
- `com/action/DealerImpactReportAction.java`
- `com/action/DealerPreOpsReportAction.java`
- `com/action/LoginAction.java`
- `com/actionservlet/PreFlightActionServlet.java`
- `WEB-INF/struts-config.xml`

---

## Findings

---

### MEDIUM: ImpactLevelFilterHandler injects column names via String.format without parameterization

**File:** `src/main/java/com/querybuilder/filters/ImpactLevelFilterHandler.java` (lines 17-28)

**Description:**
`ImpactLevelFilterHandler.getQueryFilter()` builds SQL fragments by interpolating `impactFieldName` and `thresholdFieldName` directly into a `String.format()` template, producing fragments such as:

```java
// Line 18
if (ignoreFilter()) return String.format(" AND %s > %s ", impactFieldName, thresholdFieldName);
// Lines 21-25
case RED:
    return String.format(" AND %s > (%s * 10) ", impactFieldName, thresholdFieldName);
case AMBER:
    return String.format(" AND %s BETWEEN (%s * 5 + 1) AND (%s * 10) ", impactFieldName, thresholdFieldName, thresholdFieldName);
case BLUE:
    return String.format(" AND %s BETWEEN %s AND (%s * 5) ", impactFieldName, thresholdFieldName, thresholdFieldName);
```

The values `impactFieldName` and `thresholdFieldName` are constructor arguments supplied at call sites. At the only known call site (`ImpactsReportByCompanyIdQuery`, line 27) both are hard-coded string literals (`"impact_value"` and `"unit_threshold"`), so neither value originates from user input in the current codebase:

```java
new ImpactLevelFilterHandler(filter, "impact_value", "unit_threshold")
```

The `prepareStatement()` method (lines 31-34) is intentionally empty — no bind parameters are set for this filter fragment — which is correct for the current arithmetic expressions using existing column references. The `ImpactLevel` enum value that drives which branch is taken comes from `ImpactLevel.valueOf(this.impact_level)` in `ImpactReportSearchForm`, which means an invalid enum value will throw `IllegalArgumentException` rather than reaching the DAO, providing implicit input validation.

**However**, the design carries a structural risk: the `FilterHandler` interface contract does not prevent a future caller from passing user-supplied strings as field names. If any future `ImpactLevelFilterHandler` constructor call passes request parameters or other external input as `impactFieldName` / `thresholdFieldName`, SQL injection would result immediately. The `prepareStatement()` no-op also creates a mismatch between the `getQueryFilter()` output (which contains no `?` placeholders) and the broader `FilterHandler` contract where `prepareStatement()` is expected to bind values for any `?` introduced by `getQueryFilter()`. This deviation makes it harder to audit and maintain safely.

**Risk:**
No direct SQL injection in the current codebase because both field names are compile-time constants. The structural risk is a latent SQL injection vulnerability: any future change that passes externally influenced data to the constructor would be immediately exploitable without further code modification. Rated MEDIUM for the design deficiency and the empty `prepareStatement` discrepancy.

**Recommendation:**
Refactor `ImpactLevelFilterHandler` to eliminate the `String.format` field-name interpolation entirely. Use a constructor that accepts the column names as validated enums or from a fixed allow-list, and document explicitly that the `prepareStatement` no-op is intentional because no user-controlled bind parameters exist for this filter. Add a code comment at all call sites confirming the field names are constants.

---

### HIGH: Missing dealer role check in DealerImpactReportAction — any authenticated user can access the dealer impact report

**File:** `src/main/java/com/action/DealerImpactReportAction.java` (lines 23-25) / `WEB-INF/struts-config.xml` (line 555)

**Description:**
`DealerImpactReportAction.execute()` checks only that `sessCompId` is not null:

```java
String sessCompId = (String) session.getAttribute("sessCompId");
if (sessCompId == null) throw new RuntimeException("Must have valid user logged in here");
```

No check is made for `isDealerLogin` or any other role session attribute before executing the dealer-specific impact report. The login flow sets the `isDealerLogin` flag in `LoginAction` (line 59), and other dealer-sensitive code in the application (e.g., `SwitchCompanyAction`, `AdminRegisterAction`) does verify this flag before proceeding. The `/dealerImpactReport` endpoint is intended to serve dealer accounts viewing cross-company impact data, but because the action performs no role enforcement, any authenticated company user — including a regular (non-dealer) company admin — can POST to `dealerImpactReport.do` and receive impact report data.

The scope of the report is bounded by `sessCompId` (the authenticated user's company ID), so an attacker cannot read data belonging to another company. However, a non-dealer user should not have access to this report endpoint at all, and the absence of a role check means the dealer-specific view (which includes a `companyName` column exposing which customer company a forklift was assigned to at the time of impact) is available to users who should only see the standard `impactreport.do` view.

For contrast, `ImpactReportAction` (the non-dealer endpoint) is identical in its role-check logic — neither action checks the user role. The difference is that the dealer view (`dealer/impactReport.jsp`) adds the company assignment column, revealing tenant assignment information to non-dealer users.

**Risk:**
Any authenticated non-dealer user can access the dealer variant of the impact report, which exposes the `companyName` (tenant assignment) column for impact events. In a multi-tenant deployment this constitutes information disclosure about which customer companies are associated with units managed by the logged-in company.

**Recommendation:**
Add an `isDealerLogin` check at the start of `DealerImpactReportAction.execute()` immediately after confirming `sessCompId` is non-null. If the session flag is absent or false, return an `AccessDeniedException` or forward to an access-denied page rather than throwing a generic `RuntimeException`. Apply the same pattern symmetrically to any other `Dealer*ReportAction` classes that currently omit this check (e.g., `DealerPreOpsReportAction` exhibits the same missing role check).

---

### HIGH: Missing dealer role check in ImpactReportAction — same pattern, informational completeness

**File:** `src/main/java/com/action/ImpactReportAction.java` (lines 26-27)

**Description:**
`ImpactReportAction` (mapped to `/impactreport`) performs an identical session check to `DealerImpactReportAction`:

```java
String sessCompId = (String) session.getAttribute("sessCompId");
if (sessCompId == null) throw new RuntimeException("Must have valid user logged in here");
```

The `/impactreport` action is the standard (non-dealer) report endpoint and is intended to be accessed by regular company admins. The `PreFlightActionServlet` provides only authentication-level gating (checks `sessCompId != null`), not authorization. If the application intends `/impactreport` to be restricted to non-dealer users (or to require a specific admin role), no such check is present. If access to this endpoint should be role-restricted (e.g., requiring `ROLE_ADMIN`), the missing enforcement is a MEDIUM issue. As currently documented by the context, this is flagged primarily to note the uniform absence of role checks across all report actions, which in combination with the dealer action issue above creates an authorization gap.

**Risk:**
If the `/impactreport` endpoint is intended to be accessible only by company admins (not dealer users), dealer users can also access it since no role differentiation is enforced. If both endpoints are intended to be open to all authenticated users, this is an accepted design choice but should be documented.

**Recommendation:**
Clarify the intended access policy for `/impactreport` vs `/dealerImpactReport`. If dealer users should be redirected to the dealer variant, add a role-based forwarding check. If access to `/impactreport` should be blocked for dealer users, add an `isDealerLogin == false` guard.

---

### HIGH: Reflected XSS via unescaped `request.getParameter()` embedded directly into JavaScript in dealer/impactReport.jsp

**File:** `src/main/webapp/html-jsp/dealer/impactReport.jsp` (lines 117-123)

**Description:**
The JSP embeds the raw values of the `start_date` and `end_date` request parameters directly into a JavaScript `new Date(...)` call using `<%= ... %>` scriptlet expressions, without any HTML or JavaScript encoding:

```jsp
<% if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>");
<% } %>

<% if (request.getParameter("end_date") != null) { %>
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
```

`DateUtil.stringToIsoNoTimezone()` parses the input using `SimpleDateFormat` and then reformats it as `yyyy-MM-dd'T'HH:mm:ss`. If parsing fails (e.g., because the input does not match the expected date format), `DateUtil.stringToDate()` logs the parse exception and returns `null`. The subsequent `df.format(null)` call will then throw a `NullPointerException`, which propagates as a server error — meaning a malformed date prevents the XSS script injection. However, the `sessDateFormat` session attribute drives which format `SimpleDateFormat` accepts. If a format pattern is loose enough to parse a short prefix, and the remainder of the input (after the parsed portion) is discarded, the reformatted output is a safe ISO timestamp. Under the standard date formats used by the application this effectively neutralises the injection.

Despite the incidental neutralisation via format parsing, this is a design-level XSS vulnerability. The pattern `new Date("<%= unescapedInput %>")` is inherently unsafe. If the date format is ever changed to one that parses a wider range of input and returns a value that contains special characters, or if `stringToIsoNoTimezone` is refactored to return user-supplied content on parse error, the output will be injected verbatim into the JavaScript context. An attacker who can influence the `sessDateFormat` session attribute (or if the format changes) could inject a payload such as:

```
");alert(document.cookie);//
```

The identical pattern appears in `reports/impactReport.jsp` at lines 115-122, amplifying the finding.

**Risk:**
Reflected XSS in a JavaScript context. An attacker can craft a URL with a malicious `start_date` or `end_date` parameter and share it with authenticated users. Successful exploitation allows session cookie theft, forced actions on behalf of the victim, or redirection to malicious content. The current incidental mitigation (parse failure throws NPE) is fragile and should not be relied upon.

**Recommendation:**
Do not embed raw request parameters in JavaScript blocks. Pass the pre-parsed, server-formatted date value through the Struts form bean and render it via a safe mechanism. If a scriptlet is unavoidable, apply JavaScript-context encoding (e.g., using OWASP ESAPI's `encodeForJavaScript()` or an equivalent encoder) to every value placed inside a quoted JavaScript string:

```java
// Instead of:
new Date("<%= DateUtil.stringToIsoNoTimezone(...) %>")
// Use:
new Date("<%= ESAPI.encoder().encodeForJavaScript(DateUtil.stringToIsoNoTimezone(...)) %>")
```

---

### HIGH: Reflected XSS via unescaped `request.getParameter()` embedded directly into JavaScript in reports/impactReport.jsp

**File:** `src/main/webapp/html-jsp/reports/impactReport.jsp` (lines 115-122)

**Description:**
This file contains the identical reflected XSS pattern as `dealer/impactReport.jsp`, applied to the non-dealer `/impactreport` action. The script block at the bottom of the JSP embeds `start_date` and `end_date` request parameters into inline JavaScript without encoding:

```jsp
<% if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>");
<% } %>

<% if (request.getParameter("end_date") != null) { %>
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
```

The same analysis applies as in the dealer JSP finding above: incidental NPE on parse failure partially mitigates the risk at present, but the design is inherently unsafe.

**Risk:** Same as dealer/impactReport.jsp — reflected XSS in a JavaScript context targeting authenticated admin users.

**Recommendation:** Same as dealer/impactReport.jsp — apply JavaScript-context encoding or restructure to avoid embedding request parameters in script blocks.

---

### MEDIUM: CSRF — no synchronizer token on impact report search forms

**File:** `src/main/webapp/html-jsp/dealer/impactReport.jsp` (line 22) and `src/main/webapp/html-jsp/reports/impactReport.jsp` (line 22)

**Description:**
Both JSPs render a search form that submits via HTTP POST:

```jsp
<!-- dealer/impactReport.jsp line 22 -->
<html:form action="dealerImpactReport.do" method="POST" styleClass="checklist_form">

<!-- reports/impactReport.jsp line 22 -->
<html:form action="impactreport.do" method="POST" styleId="adminUnitEditForm" styleClass="checklist_from">
```

Neither form includes a CSRF synchronizer token. Struts 1.x does provide a token mechanism (`saveToken(request)` in the action and `isTokenValid(request)` in validation) but it is not used here. There is no evidence in the action classes (`ImpactReportAction`, `DealerImpactReportAction`) that tokens are generated or verified.

The impact report search forms are read-only report queries and do not directly modify server state. However, CSRF on a POST endpoint that returns sensitive report data enables Cross-Site Request Forgery for data exfiltration in some scenarios (e.g., where the response is rendered in a context that an attacker can read). Additionally, the absence of CSRF tokens is a systemic pattern across the application's report forms and should be addressed as a policy matter even where immediate exploitation is limited.

**Risk:**
An attacker who can trick an authenticated user into visiting a crafted page can cause the user's browser to silently POST search queries to the impact report. The response data is not directly readable by the attacker via a standard CSRF attack, so direct data exfiltration is difficult. The risk is rated MEDIUM because the affected endpoints are read-only but the lack of CSRF protection is a compliance and defence-in-depth issue.

**Recommendation:**
Use Struts 1.x's built-in CSRF token mechanism: call `saveToken(request)` in the action before forwarding to the form, include `<html:hidden property="org.apache.struts.taglib.html.TOKEN"/>` in the form, and verify the token with `isTokenValid(request, true)` at the start of form processing. Alternatively, adopt a framework-level CSRF filter (e.g., OWASP CSRFGuard).

---

### MEDIUM: `ImpactReportSearchForm.getImpactReportFilter()` uses `ImpactLevel.valueOf()` without a try/catch — unchecked exception propagates to user

**File:** `src/main/java/com/actionform/ImpactReportSearchForm.java` (line 38)

**Description:**
The form method `getImpactReportFilter()` calls `ImpactLevel.valueOf(this.impact_level)` with a value read from the HTTP request parameter `impact_level`:

```java
.impactLevel(StringUtils.isBlank(this.impact_level) ? null : ImpactLevel.valueOf(this.impact_level))
```

`ImpactLevel.valueOf()` throws `IllegalArgumentException` if the string does not match a declared enum constant (`BLUE`, `AMBER`, `RED`). There is no try/catch around this call, so a crafted request with `impact_level=INVALID` will cause an unhandled exception that propagates through `ImpactReportAction.execute()` and ultimately results in an HTTP 500 response. Struts 1.x action validation is disabled for this action (`validate="false"` in struts-config.xml, line 524).

While this is not directly exploitable for data extraction, it represents a denial-of-service vector (an authenticated user or automated scanner sending invalid values will always receive a 500 error) and a missing input validation point. It also means error messages and stack traces may be returned to the client depending on the Tomcat error page configuration, potentially leaking implementation details.

**Risk:**
Authenticated users (or any scanner) can trigger a server-side exception on demand by submitting an invalid `impact_level` value, causing a 500 response. Stack trace disclosure is possible if Tomcat's default error pages are not suppressed. No data is extracted or modified.

**Recommendation:**
Wrap `ImpactLevel.valueOf()` in a try/catch block and return `null` (treating invalid input as no filter) or propagate a user-friendly validation error. Alternatively, add explicit validation in the action or use Struts validation (`validate="true"` with a `validation.xml` entry that uses a valid-values constraint). Also configure Tomcat's `<error-page>` elements in `web.xml` to suppress stack trace output for all 5xx errors.

---

### MEDIUM: `DateUtil.stringToIsoNoTimezone()` throws NullPointerException on parse failure — reflected in the JSP script block

**File:** `src/main/webapp/html-jsp/dealer/impactReport.jsp` (lines 117-123) and `src/main/webapp/html-jsp/reports/impactReport.jsp` (lines 115-122); root cause in `src/main/java/com/util/DateUtil.java` (lines 60-64)

**Description:**
`DateUtil.stringToIsoNoTimezone()` calls `DateUtil.stringToDate()` which logs a parse error and returns `null` when parsing fails:

```java
public static String stringToIsoNoTimezone(String date, String dateFormat) {
    Date dateObj = DateUtil.stringToDate(date, dateFormat);  // returns null on parse failure
    DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
    return df.format(dateObj);  // throws NullPointerException if dateObj is null
}
```

`SimpleDateFormat.format(null)` throws a `NullPointerException`. This exception is thrown in a JSP scriptlet inside the HTTP response rendering phase, causing a partial-page render followed by a 500 error. An attacker (or a legitimate user) who submits a `start_date` or `end_date` value that does not match the user's configured date format will receive a 500 error. Because the values are taken from `request.getParameter()` directly in the JSP (not from the validated form bean), this is exploitable by any authenticated user who crafts a GET or POST request with a malformed date parameter.

**Risk:**
Denial of service for authenticated users; potential partial page content disclosure in 500 error responses. The NPE incidentally prevents the XSS scenario described in the earlier finding, but the correct fix is to address both the XSS and the NPE independently.

**Recommendation:**
Add a null guard in `DateUtil.stringToIsoNoTimezone()` and return a safe default or empty string if parsing fails. Independently, remove the direct `request.getParameter()` calls from the JSP script block and instead rely on the pre-validated and pre-parsed form bean values.

---

### LOW: `getImpactLevelCSSColor()` can return `null` — potential NullPointerException in CSS inline style if `calculateImpactLevel` returns null

**File:** `src/main/webapp/html-jsp/dealer/impactReport.jsp` (line 99) and `src/main/webapp/html-jsp/reports/impactReport.jsp` (line 97); root cause in `src/main/java/com/bean/ImpactReportGroupEntryBean.java` (line 45) and `src/main/java/com/util/ImpactUtil.java` (line 49)

**Description:**
`ImpactUtil.calculateImpactLevel()` returns `null` when `impactValue` does not exceed the blue threshold:

```java
// ImpactUtil.java line 45-49
public static ImpactLevel calculateImpactLevel(int impactValue, int impactThreshold) {
    if (impactValue > impactThreshold * RED_IMPACT_COEFFICIENT) return ImpactLevel.RED;
    if (impactValue > impactThreshold * AMBER_IMPACT_COEFFICIENT) return ImpactLevel.AMBER;
    if (impactValue > impactThreshold * BLUE_IMPACT_COEFFICIENT) return ImpactLevel.BLUE;
    return null;
}
```

`ImpactReportGroupEntryBean.getImpactLevelCSSColor()` calls `ImpactUtil.getCSSColor(getImpactLevel())`, and `getCSSColor()` calls a switch statement that throws `UnhandledImpactLevelException` for any unrecognised value — but receiving `null` would cause a `NullPointerException` in the switch. Both JSPs invoke `impactEntry.getImpactLevelCSSColor()` inside an inline CSS attribute:

```jsp
<span style="background-color: <%= impactEntry.getImpactLevelCSSColor() %>;">
```

If `getImpactLevelCSSColor()` throws or returns null, the page rendering will fail for any row where the impact value does not exceed the blue threshold. However, the SQL filter in `ImpactsByCompanyIdQuery.BASE_QUERY` includes `AND impact_value >= unit_threshold`, which enforces `impactValue >= threshold` (i.e., `BLUE` condition: `impactValue > threshold * 1`), so in practice a row should always have at least a BLUE level. The gap is: the `>=` in SQL maps to the `>` in `calculateImpactLevel` for the BLUE branch — a row where `impactValue == unit_threshold` satisfies the SQL filter but yields `null` from `calculateImpactLevel` because the Java check is strict `>`.

**Risk:**
Any impact row where `impactValue == unit_threshold` (exactly equal) will cause a NullPointerException during page rendering, resulting in a 500 error for the report page. This is a data-dependent crash, not an externally injectable condition.

**Recommendation:**
Fix the off-by-one inconsistency by changing `ImpactUtil.calculateImpactLevel()` to use `>=` for the BLUE check, matching the SQL filter's `>=` condition. Add a null guard in `getImpactLevelCSSColor()` to return a safe default CSS color (e.g., `"gray"`) if `calculateImpactLevel` returns null, preventing a page crash from reaching the user.

---

### LOW: `ImpactLevelFilterHandler.prepareStatement()` is silently empty — violates FilterHandler contract expectation

**File:** `src/main/java/com/querybuilder/filters/ImpactLevelFilterHandler.java` (lines 31-34)

**Description:**
The `FilterHandler` interface defines two coupled methods: `getQueryFilter()` which appends SQL fragments (possibly containing `?` bind parameter placeholders), and `prepareStatement()` which binds values for those placeholders in order. `ImpactLevelFilterHandler.prepareStatement()` is intentionally left empty:

```java
@Override
public void prepareStatement(StatementPreparer preparer) {
    // empty
}
```

This is technically correct for the current implementation because the SQL fragments produced by `getQueryFilter()` reference only column names and arithmetic constants (no `?` placeholders). However, the empty body contains no comment explaining why it is empty, creating a maintenance hazard: a developer who modifies `getQueryFilter()` to add `?` placeholders (e.g., to make thresholds configurable) might not notice that `prepareStatement()` also needs updating. A mismatch between the number of `?` placeholders and `prepareStatement()` calls would silently shift all subsequent parameters in `ImpactsReportByCompanyIdQuery.prepareStatement()` out of position, causing incorrect query results or a runtime SQL error.

**Risk:**
No current exploit. Maintenance hazard that could lead to incorrect query results or SQL errors if `getQueryFilter()` is modified to introduce `?` parameters without a corresponding update to `prepareStatement()`.

**Recommendation:**
Add an explicit comment in `prepareStatement()`:
```java
@Override
public void prepareStatement(StatementPreparer preparer) {
    // No bind parameters: getQueryFilter() uses only column name references and
    // arithmetic on existing columns — no user-supplied values are injected.
}
```

---

### INFO: `ImpactLevel.valueOf()` in SearchForm provides implicit allow-list validation for impact_level parameter

**File:** `src/main/java/com/actionform/ImpactReportSearchForm.java` (line 38)

**Description:**
The `impact_level` request parameter is converted to a typed `ImpactLevel` enum via `ImpactLevel.valueOf()`. Because `ImpactLevel` is a sealed enum with only three values (`BLUE`, `AMBER`, `RED`), any value outside these three will throw `IllegalArgumentException` before reaching the DAO layer. This means the impact level filter is effectively validated against an allow-list. The `ImpactLevelFilterHandler` switch statement correspondingly handles only the three known enum values plus a default empty-string return, meaning even if a new enum value were added without updating the handler, it would silently no-filter rather than inject SQL. This is a positive design element, noted for completeness. The unhandled exception on invalid input (noted in the MEDIUM finding above) is the downside.

**Risk:** None — informational.

**Recommendation:** No action required beyond the input-validation improvement described in the MEDIUM finding for the unhandled `IllegalArgumentException`.

---

### INFO: `manu_id` and `type_id` are bound as typed `Long` parameters — no SQL injection risk

**File:** `src/main/java/com/actionform/ImpactReportSearchForm.java` (lines 34-35)

**Description:**
The `manu_id` and `type_id` form fields are declared as `Long` in `ImpactReportSearchForm`. Struts 1.x type conversion will reject non-numeric values during form population, and the DAO layer binds them via `preparer.addLong()` which uses `PreparedStatement.setLong()`. There is no string concatenation involving these values anywhere in the query path. These fields are safe against SQL injection.

**Risk:** None — informational.

**Recommendation:** No action required.

---

### INFO: `compId` is always sourced from `sessCompId` session attribute — no IDOR risk on primary scope

**File:** `src/main/java/com/action/ImpactReportAction.java` (lines 26-32) and `src/main/java/com/action/DealerImpactReportAction.java` (lines 24-30)

**Description:**
Both action classes derive `compId` exclusively from the server-side session attribute `sessCompId`, not from any request parameter. This value is passed to `ReportService.getImpactReport()` and from there to the SQL query as two bound parameters (`vi.comp_id = ?` and `uc.company_id = ?` in `ImpactsByCompanyIdQuery.BASE_QUERY`). An authenticated user cannot substitute a different company ID by manipulating request parameters. The tenant scoping is correctly implemented at the query level.

**Risk:** None for IDOR — informational.

**Recommendation:** No action required. This is the correct pattern and should be preserved.

---

## Summary

| # | Severity | Title | File(s) |
|---|----------|-------|---------|
| 1 | MEDIUM | ImpactLevelFilterHandler injects column names via String.format | ImpactLevelFilterHandler.java |
| 2 | HIGH | Missing dealer role check in DealerImpactReportAction | DealerImpactReportAction.java |
| 3 | HIGH | Missing role check in ImpactReportAction | ImpactReportAction.java |
| 4 | HIGH | Reflected XSS via unescaped request param in JavaScript (dealer JSP) | dealer/impactReport.jsp |
| 5 | HIGH | Reflected XSS via unescaped request param in JavaScript (reports JSP) | reports/impactReport.jsp |
| 6 | MEDIUM | CSRF — no synchronizer token on search forms | dealer/impactReport.jsp, reports/impactReport.jsp |
| 7 | MEDIUM | Unhandled IllegalArgumentException from ImpactLevel.valueOf() | ImpactReportSearchForm.java |
| 8 | MEDIUM | NullPointerException in DateUtil.stringToIsoNoTimezone on parse failure | DateUtil.java, both JSPs |
| 9 | LOW | Off-by-one in calculateImpactLevel vs SQL filter causes NPE on exact-threshold rows | ImpactUtil.java, both JSPs |
| 10 | LOW | Empty prepareStatement() undocumented — maintenance hazard | ImpactLevelFilterHandler.java |
| 11 | INFO | ImpactLevel.valueOf() provides implicit allow-list validation | ImpactReportSearchForm.java |
| 12 | INFO | manu_id / type_id bound as Long — no SQL injection | ImpactReportSearchForm.java |
| 13 | INFO | compId from session only — no IDOR on primary scope | ImpactReportAction.java, DealerImpactReportAction.java |

---

CRITICAL: 0 / HIGH: 4 / MEDIUM: 4 / LOW: 2 / INFO: 3
