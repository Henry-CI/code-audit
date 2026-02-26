# Security Audit Report — GPS Report & Header Files
**Application:** forkliftiqadmin (internal name: "pandora")
**Framework:** Apache Struts 1.3.10 on Tomcat
**Branch:** master
**Audit date:** 2026-02-26
**Pass:** 1
**Files audited:**
- `src/main/java/com/action/GPSReportAction.java`
- `src/main/java/com/bean/GPSReportFilterBean.java`
- `src/main/java/com/actionform/GPSReportSearchForm.java`
- `src/main/java/com/bean/GPSUnitBean.java`
- `src/main/webapp/includes/gps_header.jsp`
- `src/main/webapp/includes/header.inc.jsp`
- `src/main/webapp/includes/header_pop.inc.jsp`
- `src/main/webapp/includes/header_register.inc.jsp`
- `src/main/webapp/html-jsp/home.jsp`

---

## Findings

---

### CRITICAL: SQL Injection via string concatenation — `getUnitBySerial`

**File:** `src/main/java/com/dao/UnitDAO.java` (line 212)
**Description:**
The `getUnitBySerial` method builds a SQL query by concatenating the caller-supplied `serial_no` string directly into the query string, then executes it with a raw `Statement` (not a `PreparedStatement`). The `serial_no` value ultimately originates from user-controlled input.

```java
String sql = "select id,comp_id from unit where serial_no = '" + serial_no + "'";
// ...
rs = stmt.executeQuery(sql);
```

Any value that reaches this method without sanitisation allows a classic string-based SQL injection attack (e.g., `' OR '1'='1` to dump all units, or stacked queries on databases that support them).

**Risk:** Full database read/write compromise, cross-tenant data access, potential remote code execution via database-side functions (e.g., PostgreSQL `COPY TO/FROM`, `pg_read_file`).
**Recommendation:** Replace the `Statement` with a `PreparedStatement`:
```java
String sql = "select id,comp_id from unit where serial_no = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, serial_no);
```

---

### CRITICAL: SQL Injection via string concatenation — `getUnitNameByComp` / `getTotalUnitByID`

**File:** `src/main/java/com/dao/UnitDAO.java` (lines 311, 548)
**Description:**
Both `getUnitNameByComp` and `getTotalUnitByID` embed the result of `cDAO.getSubCompanyLst(compId)` directly into SQL via string concatenation. `getSubCompanyLst` returns a comma-joined list of integers sourced from a DB query, but that list is then re-inserted into a new SQL `IN (...)` clause without using parameterised binding. The `compId` passed to `getSubCompanyLst` is taken from the session, not from user input in the normal path — however any corruption or injection of the intermediate `compLst` string (e.g., if `getSubCompanyLst` were ever fed attacker-controlled input, or if the returned list were manipulated) would directly affect these queries.

```java
// getUnitNameByComp (line 311):
String sql = "select id,name from unit where comp_id in (" + compLst + ")";

// getTotalUnitByID (line 548):
String sql = "select count(id) from unit where comp_id in (" + compLst + ")";
```

Even if the immediate source is a database value, the pattern is inherently fragile and violates defence-in-depth. A second-order injection is possible if `compLst` values are ever derived from user input elsewhere and stored to the DB.

**Risk:** Second-order SQL injection; cross-tenant data enumeration if the company-list logic is bypassed.
**Recommendation:** Use `PreparedStatement` with individual `?` placeholders for each element of the list, or use a safe parameterised `IN` helper. Do not build SQL with string concatenation of any external or database-derived value.

---

### CRITICAL: SQL Injection via string concatenation — `getType` and `getPower`

**File:** `src/main/java/com/dao/UnitDAO.java` (lines 626–628, 667–670)
**Description:**
Both `getType(String manu_id)` and `getPower(String manu_id, String type_id)` concatenate their String parameters directly into SQL queries. These parameters are populated from HTTP request parameters (`request.getParameter("manu_id")`, `request.getParameter("type_id")`) in `GetAjaxAction` (lines 26 and 35) without any sanitisation.

```java
// getType (line 626):
String sql = "select distinct(type.id),name from manu_type_fuel_rel"
    + " left outer join type on type.id = manu_type_fuel_rel.type_id "
    + " where manu_id = " + manu_id
    + " order by name";

// getPower (lines 667–670):
String sql = "select fuel_type.id,name from manu_type_fuel_rel"
    + " left outer join fuel_type on fuel_type.id = manu_type_fuel_rel.fuel_type_id "
    + " where manu_id = " + manu_id;
if (!type_id.equalsIgnoreCase("")) {
    sql += " and type_id= " + type_id;
}
```

An attacker can pass `manu_id=0 UNION SELECT username,password FROM users--` or equivalent payloads via the AJAX endpoints.

**Risk:** Unauthenticated (or minimally authenticated) SQL injection allowing extraction of arbitrary database tables, including credential tables.
**Recommendation:** Validate that `manu_id` and `type_id` are numeric (e.g., `Long.parseLong(manu_id)`) before use, and use `PreparedStatement` with `?` placeholders.

---

### CRITICAL: SQL Injection via string concatenation — `delUnitById`

**File:** `src/main/java/com/dao/UnitDAO.java` (line 349)
**Description:**
The `delUnitById` method builds an UPDATE statement by concatenating the `id` parameter directly:

```java
String sql = "update unit set active = false where id=" + id;
stmt.executeUpdate(sql);
```

`id` is set from the HTTP request parameter `equipId` in `AdminUnitAction` (line 34) without numeric validation before it reaches the DAO. An attacker who controls `equipId` can inject arbitrary SQL.

**Risk:** Arbitrary SQL execution; an attacker could deactivate all units across all tenants, or — with a stacked query — exfiltrate or destroy data.
**Recommendation:** Parse `id` as a long/integer before use, and use `PreparedStatement`:
```java
private static final String DELETE_UNIT = "update unit set active = false where id = ?";
// ...
PreparedStatement ps = conn.prepareStatement(DELETE_UNIT);
ps.setLong(1, Long.parseLong(id));
```

---

### HIGH: IDOR — Unit deletion not scoped to authenticated tenant

**File:** `src/main/java/com/action/AdminUnitAction.java` (lines 57–61) / `src/main/java/com/dao/UnitDAO.java` (line 349)
**Description:**
When `action=delete`, `AdminUnitAction` passes the user-supplied `equipId` parameter directly to `unitDAO.delUnitById(equipId)`. The `delUnitById` query does not include a `comp_id = ?` predicate, so any authenticated user can soft-delete any unit in the entire database by supplying an arbitrary `equipId`:

```java
// AdminUnitAction.java line 57-58:
} else if (action.equalsIgnoreCase("delete")) {
    unitDAO.delUnitById(equipId);   // no sessCompId check
```

```java
// UnitDAO.java line 349:
String sql = "update unit set active = false where id=" + id;  // no comp_id filter
```

`sessCompId` is available in the session but is never used in the DELETE path.

**Risk:** Any tenant's administrator can deactivate equipment belonging to any other tenant, causing operational disruption and denial of service.
**Recommendation:** Add a `comp_id` constraint to the delete query and pass `sessCompId` as a second parameter:
```java
"update unit set active = false where id = ? and comp_id = ?"
```

---

### HIGH: IDOR — Unit assignment deletion not scoped to authenticated tenant

**File:** `src/main/java/com/action/AdminUnitAssignAction.java` (line 52) / `src/main/java/com/dao/UnitDAO.java` (line 83)
**Description:**
When `action=delete`, `AdminUnitAssignAction` calls `UnitDAO.deleteAssignment(id)` where `id` is taken directly from the request parameter. The underlying SQL is:

```java
private static final String DELETE_UNIT_ASSIGNMENT = "delete from unit_company where id = ?";
```

There is no check that the `unit_company` record identified by `id` belongs to the company of the authenticated user (`sessCompId`). An attacker can iterate over integer `id` values to delete assignment records belonging to other tenants.

**Risk:** Cross-tenant deletion of unit-to-company assignment records, disrupting other customers' fleet configurations.
**Recommendation:** Join against the `unit` table and add a `comp_id` predicate:
```sql
DELETE FROM unit_company uc
USING unit u
WHERE uc.id = ? AND u.id = uc.unit_id AND u.comp_id = ?
```

---

### HIGH: IDOR — Unit edit does not verify ownership before loading unit data

**File:** `src/main/java/com/action/AdminUnitAction.java` (lines 44–47)
**Description:**
The `action=edit` branch fetches the unit by the user-supplied `equipId` parameter using `unitDAO.getUnitById(equipId)`, which queries `unit` by primary key only, with no company-scope filter:

```java
if (action.equalsIgnoreCase("edit")) {
    List<UnitBean> arrUnit = unitDAO.getUnitById(equipId);
    request.setAttribute("arrAdminUnit", arrUnit);
    return mapping.findForward("unitedit");
```

An authenticated user from company A can read the full configuration details (serial number, MAC address, manufacturer, type, location, department, etc.) of any unit in the database by supplying another company's `equipId`.

**Risk:** Cross-tenant information disclosure of hardware identifiers (serial number, MAC address) and operational configuration data.
**Recommendation:** After fetching the unit, verify `unitBean.getComp_id().equals(sessCompId)` and return a 403 / redirect if it does not match; alternatively add a `comp_id` filter to `UnitsByIdQuery`.

---

### HIGH: XSS — Unescaped session attribute rendered in `href` attribute

**File:** `src/main/webapp/html-jsp/home.jsp` (lines 53, 75)
**Description:**
The `isDealer` session attribute is retrieved and compared inside a JSP scriptlet expression that is placed directly inside an `href` attribute. While the comparison itself is boolean, the pattern uses `session.getAttribute("isDealer").equals("true")` and renders the result of the ternary expression into the HTML:

```jsp
<a href="<%= session.getAttribute("isDealer").equals("true") ? "dealerPreOpsReport.do" : "preopsreport.do" %>">
...
<a href="<%= session.getAttribute("isDealer").equals("true") ? "dealerImpactReport.do" : "impactreport.do"%>">
```

Although the outputs here are hardcoded string literals, the `session.getAttribute("isDealer")` call is made without a null check and without escaping. If `isDealer` is null (e.g., the session attribute was never set or was invalidated), this call throws a `NullPointerException`, which Tomcat will render as a 500 error page that can expose stack trace information. More broadly, the use of raw `<%= session.getAttribute(...) %>` scriptlet pattern without escaping in JSP is inherently dangerous and sets a precedent for XSS whenever the attribute value is used directly in output.

**Risk:** NullPointerException causing information-disclosing 500 error page; establishes an unsafe pattern that, if extended with user-controlled session attributes, leads to reflected XSS.
**Recommendation:** Use `logic:equal` / `logic:notEqual` Struts tags (already used elsewhere in the same file) instead of scriptlet `href` construction. At minimum, null-check the attribute and use `ESAPI.encoder().encodeForHTMLAttribute(value)` if scriptlets must be used.

---

### HIGH: Insecure (HTTP) third-party JavaScript inclusion

**File:** `src/main/webapp/includes/header_register.inc.jsp` (line 15)
**Description:**
The registration page header loads jQuery from Google's CDN over plain HTTP:

```html
<script type="text/javascript"
  src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
```

Wait — the URL uses `https://`, however the jQuery version being loaded is **1.7.1**, which was released in 2011 and has numerous known XSS and prototype-pollution vulnerabilities. This version is more than 14 years old and has no security patches available from the jQuery project.

Additionally, no `integrity` (Subresource Integrity / SRI) hash is specified on the `<script>` tag. If Google's CDN were compromised or subject to a BGP hijack / DNS poisoning attack, or if a network-level attacker performed a man-in-the-middle against the CDN, arbitrary JavaScript could be injected into the login/registration page with no browser-side detection.

```html
<!-- No integrity attribute, outdated version: -->
<script type="text/javascript"
  src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
```

**Risk:** Supply-chain attack on the registration/login page; known CVEs in jQuery 1.7.1 including XSS via `jQuery.html()` (CVE-2015-9251, CVE-2019-11358, CVE-2020-11022, CVE-2020-11023). Credential theft of admin users at login time.
**Recommendation:** (1) Vendor the jQuery library locally rather than using a CDN. (2) If a CDN must be used, upgrade to a current jQuery version (3.7+) and add an `integrity="sha384-..."` SRI hash with `crossorigin="anonymous"`. (3) Replace on-page usage of deprecated jQuery APIs.

---

### MEDIUM: CSRF — No synchronizer token on any state-changing Struts action

**File:** `src/main/webapp/WEB-INF/struts-config.xml` (line 530); `src/main/java/com/action/AdminUnitAction.java`; `src/main/java/com/action/AdminUnitAssignAction.java`
**Description:**
Struts 1.x does not provide built-in CSRF protection. None of the audited state-changing actions (`/gpsreport`, `/adminunit?action=delete`, `/adminunitassign?action=delete`) use a synchronizer token pattern. Struts 1 does provide `html:form` with a token mechanism via `saveToken(request)` / `isTokenValid(request)`, but this is opt-in and not enabled for any of the observed actions.

An attacker who lures an authenticated administrator to a malicious page can trigger unit deletions, assignment deletions, or report queries on behalf of the victim:

```html
<!-- Attacker's page: -->
<img src="https://target.example.com/adminunit.do?action=delete&equipId=42" />
```

**Risk:** Cross-site request forgery allowing an unauthenticated attacker to delete units, remove assignments, or modify settings of any authenticated administrator's company, including from the `isSuperAdmin` role.
**Recommendation:** Implement the Struts 1 token mechanism: call `saveToken(request)` in every GET handler that renders a form, and call `isTokenValid(request, true)` at the start of every POST/action handler that mutates state. Alternatively, migrate to a framework with built-in CSRF protection (Spring Security, Struts 2 + CSRFGuard).

---

### MEDIUM: Lombok `@Data` on `GPSUnitBean` — `toString()` leaks sensitive telemetry data

**File:** `src/main/java/com/bean/GPSUnitBean.java` (line 9)
**Description:**
`GPSUnitBean` is annotated with Lombok `@Data`, which auto-generates a `toString()` method that includes every field:

```java
@Data
public class GPSUnitBean {
    String vehName;
    String longitude;
    String latitude;
    Timestamp timeStmp;
    String status;
    String manufacturer;
    String type;
    String power;
}
```

The generated `toString()` will produce output like:
```
GPSUnitBean(vehName=Forklift-7, longitude=-73.935242, latitude=40.730610, timeStmp=2025-11-01 09:14:22.0, status=ACTIVE, ...)
```

If this bean is ever logged (e.g., via `log.debug(gpsUnit)`, in exception messages, or via an ORM/framework that calls `toString()` on request attributes), the physical GPS coordinates and operational status of vehicles are written to log files. Log files in Java web applications are frequently accessible to a wider set of users than the application data itself, and are often shipped to centralised logging infrastructure (ELK, Splunk) with broader access.

**Risk:** Disclosure of real-time vehicle location data (latitude/longitude) in application logs, potentially violating privacy regulations (GDPR, CCPA) and customer confidentiality obligations.
**Recommendation:** Remove `@Data` or add `@ToString(exclude = {"longitude","latitude"})` to prevent coordinates appearing in `toString()`. Consider whether any field in this bean should appear in logs; a conservative approach excludes all fields and logs only identifiers.

---

### MEDIUM: Lombok `@Data` on `GPSReportSearchForm` — `toString()` leaks filter parameters including date range

**File:** `src/main/java/com/actionform/GPSReportSearchForm.java` (line 16)
**Description:**
`GPSReportSearchForm` is annotated `@Data`, which generates `toString()` including `manu_id`, `type_id`, `start_date`, `end_date`, `unitId`, and the `manufacturers` and `unitTypes` list references. When Struts binds the form to the action, framework code may call `toString()` on the form. The `manufacturers` and `unitTypes` lists could contain a large number of `ManufactureBean` and `UnitTypeBean` objects (all of which will themselves invoke their `@Data`-generated `toString()` recursively), potentially producing extremely large log entries or verbose error messages.

```java
@Data
public class GPSReportSearchForm extends ActionForm {
    private Long manu_id;
    private Long type_id;
    private String start_date;
    private String end_date;
    private int unitId;
    private List<ManufactureBean> manufacturers = ...;
    private List<UnitTypeBean> unitTypes = ...;
```

**Risk:** Excessive data disclosure in logs; potential log flooding / denial-of-service if the lists are large.
**Recommendation:** Use `@ToString(exclude = {"manufacturers", "unitTypes"})` to prevent the full list objects from being serialised into log strings, and review whether `start_date` / `end_date` need to appear in toString output.

---

### MEDIUM: Null-pointer dereference on unauthenticated or partially-established session

**File:** `src/main/webapp/html-jsp/home.jsp` (lines 53, 75)
**Description:**
Both lines invoke `.equals("true")` directly on `session.getAttribute("isDealer")` without a null guard:

```jsp
<a href="<%= session.getAttribute("isDealer").equals("true") ? "dealerPreOpsReport.do" : "preopsreport.do" %>">
```

If the `isDealer` attribute is absent from the session (e.g., after a session expiry mid-page, a race condition, or a missing session setup in a code path that was added later), a `NullPointerException` is thrown at render time, producing a 500 error response. Tomcat's default error page renders the full stack trace unless `<error-page>` handlers are configured, potentially leaking internal class names and file paths.

**Risk:** Information disclosure via stack trace on error pages; application crash visible to end users.
**Recommendation:** Use `Boolean.TRUE.toString().equals(session.getAttribute("isDealer"))` (which is null-safe), or use Struts `logic:equal` tags as is already done for the navigation pane below on the same page.

---

### LOW: `GPSReportFilterBean` constructor silently drops `unitId` parameter

**File:** `src/main/java/com/bean/GPSReportFilterBean.java` (lines 14–17)
**Description:**
The `@Builder`-annotated constructor accepts a `unitId` parameter but does not store it anywhere — it passes only `startDate`, `endDate`, `manuId`, `typeId`, and an empty string to the superclass constructor. The `unitId` is silently discarded:

```java
@Builder
public GPSReportFilterBean(Date startDate, Date endDate, Long manuId, Long typeId, int unitId) {
    super(startDate, endDate, manuId, typeId, "");
    // unitId is never stored or used
}
```

Meanwhile, `GPSReportSearchForm.getGPSReportFilter()` (line 36) passes `unitId` to the builder:

```java
.unitId(this.unitId == 0 || this.unitId == 0 ? null : this.unitId).build();
```

(Note also the duplicate `this.unitId == 0` condition on the same line — the second branch is dead code and should read `this.unitId == 0` is already covered by the first clause, making the null-elision logic effectively broken for `unitId`.)

This means any filter that should scope a GPS report to a specific vehicle unit is silently ignored, potentially causing reports to return data for all units in the company when the user expects only one unit.

**Risk:** Business logic bypass — unit-scoped GPS reports return data for the entire fleet. Depending on how the report data is used, this could cause inadvertent data over-disclosure within the same tenant.
**Recommendation:** Add a `unitId` field to `GPSReportFilterBean`, store it in the constructor, expose it via a getter, and use it in the report query. Also fix the duplicate null-check condition in `GPSReportSearchForm.getGPSReportFilter()`.

---

### LOW: Commented-out code leaves dead `GPSReportAction` effectively a stub

**File:** `src/main/java/com/action/GPSReportAction.java` (lines 35–42)
**Description:**
The body of `GPSReportAction.execute()` has virtually all meaningful logic commented out. The only active code loads the unit list for the company and forwards to the success view:

```java
// searchForm.setManufacturers(this.manufactureDAO.getAllManufactures(sessCompId));
// searchForm.setUnitTypes(unitDAO.getAllUnitType());
// ImpactReportBean impactReport = reportService.getImpactReport(...);
// request.setAttribute("impactReport", impactReport);
```

This means the GPS report action is currently non-functional: it loads the unit dropdown but never retrieves or displays any GPS report data. Code that is commented out but left in production source creates ambiguity about intended functionality and may be accidentally re-enabled without full security review.

**Risk:** Latent functionality risk; dead code that may be re-enabled without a security review. The commented code calls `getImpactReport` which needs to be verified for SQL injection and IDOR before being re-enabled.
**Recommendation:** Remove commented-out code from production source; track incomplete features in version control branches or issue trackers. Before re-enabling the impact report call, audit `reportService.getImpactReport()` for SQL injection and tenant-scoping.

---

### LOW: `gps_header.jsp` contains only commented-out resource references — no active content

**File:** `src/main/webapp/includes/gps_header.jsp` (lines 1–2)
**Description:**
The entire file consists of two HTML comments wrapping `<link>` and `<script>` tags:

```html
<!-- <link rel="stylesheet" href="../skin/css/leaflet.css" /> -->
<!-- <script language="javascript" src="../skin/js/ajaxStore.js"></script> -->
```

The GPS mapping page (`gps_header.jsp`) is included in map views but its CSS and JavaScript dependencies have been commented out. The `header.inc.jsp` file does however load `leaflet.js` and `ajaxStore.js` in the main header, suggesting these were duplicates that were removed from the GPS-specific header. No security risk in the file as currently committed, but the presence of an effectively empty include file raises a maintenance concern.

**Risk:** Informational / maintenance concern only. If the Leaflet resources in `header.inc.jsp` are ever removed, the GPS map feature will silently break.
**Recommendation:** Either delete `gps_header.jsp` if it is no longer needed, or document why it is kept. Ensure resource loading is tested as part of the GPS feature's integration tests.

---

### INFO: `header.inc.jsp` loads all JS/CSS from relative, server-local paths — no CDN risk in main header

**File:** `src/main/webapp/includes/header.inc.jsp` (lines 13–46)
**Description:**
The main application header loads all CSS and JavaScript from relative `skin/` paths that are served locally by the application server. There are no external CDN references (unlike `header_register.inc.jsp`). This is good practice for integrity and availability.

The `document.write()` call on line 42 is worth noting:
```javascript
document.write("<script type='text/javascript' src='skin/js/scripts.js?v=" + Date.now() + "'><\/script>");
```
Using `document.write()` for cache-busting is a legacy pattern. In modern browsers, `document.write()` can block page rendering and is deprecated. While not a security vulnerability in itself (the value `Date.now()` is not user-controlled), it should be replaced with a build-time cache-busting mechanism.

**Risk:** No direct security risk. Minor performance concern with `document.write()`.
**Recommendation:** Replace the `document.write()` cache-bust with a build-time version stamp (e.g., a Maven `resources` filter that injects a version string at build time) or a `<script>` element appended via `document.createElement`.

---

### INFO: `header_pop.inc.jsp` contains only a CSS rule — no security concerns

**File:** `src/main/webapp/includes/header_pop.inc.jsp` (lines 1–6)
**Description:**
The popup header include contains only an inline `<style>` block with a single CSS rule:

```html
<style>
    .modal-content-form {
        overflow-y: scroll;
        max-height: calc(100vh - 220px);
    }
</style>
```

There are no script includes, session data renderings, or HTML comments. No security findings.

**Risk:** None.
**Recommendation:** No action required.

---

### INFO: Internal project name "pandora" exposed in class name `PandoraAction`

**File:** `src/main/java/com/action/AdminUnitAssignAction.java` (line 18, extends `PandoraAction`)
**Description:**
`AdminUnitAssignAction` extends `PandoraAction`, which exposes the internal project codename "pandora" in compiled class names and stack traces. While not a vulnerability in isolation, internal codenames appearing in exception stack traces or error pages can provide reconnaissance value to an attacker.

**Risk:** Minor information disclosure.
**Recommendation:** If error pages are properly suppressed in production (`<error-page>` handlers configured in `web.xml`), this is low risk. Ensure generic error pages are configured and that stack traces are never shown to end users.

---

## Summary Table

| # | Severity | Title | File |
|---|----------|-------|------|
| 1 | CRITICAL | SQL injection — `getUnitBySerial` string concat | `UnitDAO.java:212` |
| 2 | CRITICAL | SQL injection — `getUnitNameByComp` / `getTotalUnitByID` string concat | `UnitDAO.java:311,548` |
| 3 | CRITICAL | SQL injection — `getType` and `getPower` HTTP param concat | `UnitDAO.java:626,667` |
| 4 | CRITICAL | SQL injection — `delUnitById` string concat | `UnitDAO.java:349` |
| 5 | HIGH | IDOR — unit deletion not scoped to tenant | `AdminUnitAction.java:58` |
| 6 | HIGH | IDOR — assignment deletion not scoped to tenant | `AdminUnitAssignAction.java:52` |
| 7 | HIGH | IDOR — unit edit loads data without ownership check | `AdminUnitAction.java:45` |
| 8 | HIGH | XSS / NPE — unguarded `session.getAttribute` in `href` | `home.jsp:53,75` |
| 9 | HIGH | Insecure third-party JS — outdated jQuery 1.7.1 without SRI | `header_register.inc.jsp:15` |
| 10 | MEDIUM | CSRF — no synchronizer token on state-changing actions | `struts-config.xml:530`, multiple actions |
| 11 | MEDIUM | Lombok `@Data` `toString()` leaks GPS coordinates | `GPSUnitBean.java:9` |
| 12 | MEDIUM | Lombok `@Data` `toString()` leaks filter + full list objects | `GPSReportSearchForm.java:16` |
| 13 | MEDIUM | NPE on null session attribute in home.jsp | `home.jsp:53,75` |
| 14 | LOW | `unitId` silently dropped in `GPSReportFilterBean` constructor | `GPSReportFilterBean.java:15` |
| 15 | LOW | Commented-out code makes `GPSReportAction` a non-functional stub | `GPSReportAction.java:35–42` |
| 16 | LOW | `gps_header.jsp` is effectively empty (all content commented out) | `gps_header.jsp:1–2` |
| 17 | INFO | `document.write()` cache-bust pattern in main header | `header.inc.jsp:42` |
| 18 | INFO | `header_pop.inc.jsp` — no findings | `header_pop.inc.jsp` |
| 19 | INFO | Internal codename "pandora" in class hierarchy | `AdminUnitAssignAction.java:18` |

---

**CRITICAL: 4 / HIGH: 5 / MEDIUM: 4 / LOW: 3 / INFO: 3**
