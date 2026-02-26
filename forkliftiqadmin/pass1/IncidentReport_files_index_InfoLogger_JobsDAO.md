# Security Audit Report: IncidentReport, index.jsp, InfoLogger, JobsDAO
**Application:** forkliftiqadmin (FleetIQ System)
**Framework:** Apache Struts 1.3.10 on Apache Tomcat
**Branch:** master
**Audit Date:** 2026-02-26
**Auditor:** Automated pass-1 analysis
**Scope:** dealer/incidentReport.jsp, reports/incidentReport.jsp, IncidentReportAction.java, IncidentReportBean.java, IncidentReportByCompanyIdQuery.java, IncidentReportDAO.java, IncidentReportEntryBean.java, IncidentReportFilterBean.java, IncidentReportSearchForm.java, index.jsp, InfoLogger.java, JobDetailsBean.java, JobsDAO.java (+ supporting callers AdminUnitAction.java, DriverJobDetailsAction.java, PreFlightActionServlet.java)

---

## Findings

---

### CRITICAL: SQL Injection via string concatenation in `getJobList` — `equipId` parameter

**File:** `src/main/java/com/dao/JobsDAO.java` (line 52)

**Description:**
The method `getJobList(String equipId)` builds a SQL query by directly concatenating the caller-supplied `equipId` string into the query without using a `PreparedStatement` parameter placeholder. A `java.sql.Statement` object is used, not a `PreparedStatement`.

```java
String sql = "select j.id, j.unit_id, ja.driver_id, j.description, j.start_time, j.end_time, j.job_no, j.duration, j.job_title "
           + "from jobs j "
           + "left outer join job_allocation ja on j.id = ja.job_id "
           + "where j.unit_id = " + equipId;   // <-- direct concatenation
log.info(sql);                                  // <-- also logged before execution
rs = stmt.executeQuery(sql);
```

The caller `AdminUnitAction.java` (line 34 and line 64) reads `equipId` directly from `request.getParameter("equipId")` with no validation:

```java
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
// ...
ArrayList<JobDetailsBean> jobs = jobsDAO.getJobList(equipId);
```

A request such as `?action=job&equipId=1+OR+1=1--` would return all rows from the `jobs` table across all tenants. More destructive payloads can execute stacked queries depending on the database driver and server configuration.

**Risk:** Complete database compromise; cross-tenant data exfiltration; potential data destruction. This is exploitable by any authenticated user (the action is behind the auth gate).

**Recommendation:** Replace the `Statement` with a `PreparedStatement` with a `?` placeholder. Validate that `equipId` is a numeric value before use:

```java
String sql = "SELECT ... FROM jobs j LEFT OUTER JOIN job_allocation ja ON j.id = ja.job_id WHERE j.unit_id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setInt(1, Integer.parseInt(equipId));
```

---

### CRITICAL: SQL Injection via string concatenation in `getJobListByJobId` — `equipId` and `jobNo` parameters

**File:** `src/main/java/com/dao/JobsDAO.java` (line 123)

**Description:**
The method `getJobListByJobId(String equipId, String jobNo)` uses the same pattern: a single-line SQL string is assembled by directly concatenating both `equipId` and `jobNo` into the query, and then executed with a plain `Statement`.

```java
String sql = "select j.id, j.unit_id, ja.driver_id, j.description, "
    + "to_char(js.start_time,'dd/mm/yyyy HH24:MI:SS'), "
    + "to_char(js.end_time,'dd/mm/yyyy HH24:MI:SS'), "
    + "j.job_no, j.duration, j.job_title, js.event "
    + "from jobs j, job_allocation ja, job_sessions js "
    + "where j.id = ja.job_id and j.id = js.job_id "
    + "and j.unit_id = " + equipId          // <-- injection point 1
    + " and j.job_no = '" + jobNo + "'"     // <-- injection point 2
    + " order by js.start_time";
log.info(sql);
rs = stmt.executeQuery(sql);
```

The caller `DriverJobDetailsAction.java` (lines 37–38, 52) takes both values directly from request parameters:

```java
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String jobNo   = request.getParameter("job_no")  == null ? "" : request.getParameter("job_no");
// ...
ArrayList<JobDetailsBean> jobs = jobsDAO.getJobListByJobId(equipId, jobNo);
```

`jobNo` is a string column and is quoted in the SQL, making it a classic single-quote injection vector: `?job_no=x' OR '1'='1`. `equipId` provides a numeric-context injection point.

**Risk:** Same as above — complete database read and potential destructive access across all tenants.

**Recommendation:** Convert to a `PreparedStatement` with two `?` placeholders; validate `equipId` as numeric; sanitize `jobNo`.

---

### CRITICAL: IDOR — `getJobList` and `getJobListByJobId` query jobs with no company scope

**File:** `src/main/java/com/dao/JobsDAO.java` (lines 49–53, 123); caller `src/main/java/com/action/AdminUnitAction.java` (lines 62–64); caller `src/main/java/com/action/DriverJobDetailsAction.java` (lines 49–52)

**Description:**
Both job-query methods filter only on `unit_id` (or `unit_id + job_no`) but never join or filter on the authenticated user's `sessCompId`. The `jobs` table is never constrained to the company of the logged-in user.

In `AdminUnitAction.java`:
```java
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
// ...
ArrayList<JobDetailsBean> jobs = jobsDAO.getJobList(equipId);
```

`sessCompId` is read from session (line 31) but is never passed to `getJobList` or used to scope the query. An attacker who knows (or can enumerate) a valid unit ID belonging to a different tenant can retrieve that tenant's complete job list by supplying `?action=job&equipId=<other_tenant_unit_id>`.

Note that `AdminUnitAction` also calls `unitDAO.getUnitById(equipId)` (line 65) after the job list, but `getUnitById` itself must be independently verified for company scoping; the jobs query is definitely unscoped.

**Risk:** A tenant with authenticated access can access job data of any other tenant by supplying a foreign `equipId`. This violates multi-tenancy isolation.

**Recommendation:** Join the `jobs` query to a company-ownership table and add `WHERE company_id = ?` bound to `sessCompId`. Alternatively, verify that the requested `unit_id` belongs to the authenticated user's company before querying jobs.

---

### HIGH: Broken Double-Checked Locking — `IncidentReportDAO` synchronizes on wrong class

**File:** `src/main/java/com/dao/IncidentReportDAO.java` (lines 16–26)

**Description:**
`IncidentReportDAO` implements the double-checked locking singleton pattern but acquires the lock on `ImpactReportDAO.class` instead of `IncidentReportDAO.class`.

```java
public static IncidentReportDAO getInstance() {
    if (theInstance == null) {
        synchronized (ImpactReportDAO.class) {   // <-- WRONG CLASS LOCK
            if (theInstance == null) {
                theInstance = new IncidentReportDAO();
            }
        }
    }
    return theInstance;
}
```

`ImpactReportDAO` correctly locks on its own class:
```java
// ImpactReportDAO.java line 16–17
synchronized (ImpactReportDAO.class) { // correct for ImpactReportDAO
```

Because both DAOs use the same lock object (`ImpactReportDAO.class`), they contend on a shared mutex. More critically, `IncidentReportDAO.theInstance` is not `volatile`, so the double-checked locking pattern is not safe under Java Memory Model semantics — the inner null-check on a non-volatile field may observe a partially-constructed object in a multi-threaded environment. Both of these issues together mean concurrent initialization of `IncidentReportDAO` can result in multiple instances being created (defeating the singleton), and/or a thread observing a partially-constructed `IncidentReportDAO` instance, causing unpredictable behavior.

**Risk:** Under concurrent load the DAO may be initialized multiple times; in pathological cases a thread obtains a partially-constructed object and subsequently fails with a NullPointerException or, worse, proceeds silently with a broken object. The wrong lock also introduces unintended coupling between two unrelated DAO classes.

**Recommendation:** Declare `theInstance` as `volatile` and change the lock to `IncidentReportDAO.class`. Alternatively, use the initialization-on-demand holder idiom:

```java
private static class Holder {
    private static final IncidentReportDAO INSTANCE = new IncidentReportDAO();
}
public static IncidentReportDAO getInstance() {
    return Holder.INSTANCE;
}
```

---

### HIGH: Authentication Guard Logic Inversion in `PreFlightActionServlet`

**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java` (lines 98–115, 48–61)

**Description:**
The method `excludeFromFilter` is named as if it returns `true` for paths that should be *excluded* from the auth check (i.e., public paths). However, the logic is inverted: the method returns `false` for all known public paths (login, logout, welcome, etc.) and returns `true` for everything else. Then the caller only enforces authentication when `excludeFromFilter` returns `true`:

```java
if (excludeFromFilter(path)) {      // enters auth block for NON-excluded (protected) paths
    if (session == null) {
        stPath = RuntimeConf.EXPIRE_PAGE;
        forward = true;
    } else if (session.getAttribute("sessCompId") == null || ...) {
        stPath = RuntimeConf.EXPIRE_PAGE;
        forward = true;
    }
}
```

Mechanically this is functionally correct — auth is enforced for all paths that are NOT in the exclusion list — but the naming convention is dangerously misleading. A developer extending the exclusion list may misread the method semantics and add `return true` for a path they intend to make public, which would actually keep it protected; conversely, a developer who changes `return false` to `return true` for a public path would accidentally apply the auth check to it (though that would be a harmless failure mode, not a bypass). The more dangerous scenario is when a developer adds a new public endpoint by adding `else if (path.endsWith("newpublicendpoint.do")) return true;` — this would enforce auth on the new endpoint rather than exempting it.

Additionally, the auth check applies only within the `excludeFromFilter(path) == true` block; if `excludeFromFilter` were ever changed to return `false` for a protected resource (e.g., by mistake), that resource would become entirely unprotected with no secondary check.

**Risk:** Developer confusion leading to future authentication bypass when adding public or protected endpoints. The naming inversion is a latent defect that may cause a security regression in the next code change to this method.

**Recommendation:** Rename the method to `requiresAuthCheck` or invert the return values and rename to `isPublicPath` (returning `true` for public paths, `false` otherwise), and update the call site accordingly. Add a comment block documenting the contract.

---

### HIGH: Reflected XSS via unescaped `request.getParameter` injected into JavaScript block

**File:** `src/main/webapp/html-jsp/reports/incidentReport.jsp` (lines 164, 172)
**File:** `src/main/webapp/html-jsp/dealer/incidentReport.jsp` (lines 149, 153)

**Description:**
Both JSPs include a `<script>` block that reflects the raw `start_date` and `end_date` request parameters (after passing through `DateUtil.stringToIsoNoTimezone`) directly into JavaScript string literals without HTML encoding or JavaScript escaping:

```jsp
<%  if (request.getParameter("start_date") != null) { %>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(
    request.getParameter("start_date"),
    (String) session.getAttribute("sessDateFormat")) %>");
<% } %>
```

If `DateUtil.stringToIsoNoTimezone` does not sanitize all characters and returns unmodified input when parsing fails (e.g., passes through the raw value on a format mismatch), an attacker can inject arbitrary JavaScript. For example, if the date utility returns the raw input on parse failure:

```
start_date=");alert(document.cookie);//
```

would produce:
```javascript
start_date = new Date("");alert(document.cookie);//");
```

Even if `DateUtil` only returns null or a formatted date on valid input, this code path is fragile: the protection against XSS is entirely dependent on `DateUtil` implementation rather than explicit output encoding. Any change to that utility, or a bypass of its format validation, immediately creates a reflected XSS.

**Risk:** An attacker who tricks an authenticated user into clicking a crafted link can execute arbitrary JavaScript in the victim's browser session — session token theft, UI redirection, credential harvesting.

**Recommendation:** Do not reflect request parameters directly into JavaScript contexts. Either perform explicit JavaScript string escaping (e.g., using `StringEscapeUtils.escapeEcmaScript`) or compute all date values server-side and embed them as safely formatted ISO strings. If the dates are only used to initialize a date-picker, pass them via a `data-*` attribute on a DOM element and read them in JavaScript using `dataset`.

---

### HIGH: IDOR — `editJob` in `JobsDAO` / `AdminUnitAction` accepts any `job_id` without company scope verification

**File:** `src/main/java/com/dao/JobsDAO.java` (lines 275–282); caller `src/main/java/com/action/AdminUnitAction.java` (lines 85–98)

**Description:**
The `editJob` method updates the `description` and `job_title` of any job matching the caller-supplied `id` without any ownership check:

```java
// JobsDAO.java
String sql = "update jobs set description = ?, job_title = ? where id = ?";
ps = conn.prepareStatement(sql);
ps.setString(1, jobdetails.getDescription());
ps.setString(2, jobdetails.getJobTitle());
ps.setInt(3, jobdetails.getId());
```

The caller takes `job_id` from a request parameter with no company check:

```java
// AdminUnitAction.java lines 86–98
int jobId = Integer.parseInt(job_id);  // job_id = request.getParameter("job_id")
JobDetailsBean jobdetails = new JobDetailsBean();
jobdetails.setDescription(job_description);
jobdetails.setJobTitle(job_title);
jobdetails.setId(jobId);
jobsDAO.editJob(jobdetails);
```

An authenticated user from Company A can send `?action=edit_job&job_id=<id_of_company_B_job>` and overwrite another tenant's job record.

**Risk:** Cross-tenant data tampering; a malicious tenant can corrupt or modify job records owned by other companies.

**Recommendation:** Add a `WHERE company_id = ?` (or join-based scope check) to the `UPDATE` statement, binding to `sessCompId`. Verify the affected row count is exactly 1 and reject updates where it is 0.

---

### MEDIUM: CSRF — Incident Report search forms have no synchronizer token

**File:** `src/main/webapp/html-jsp/reports/incidentReport.jsp` (line 22)
**File:** `src/main/webapp/html-jsp/dealer/incidentReport.jsp` (line 27)

**Description:**
Both incident report forms submit via HTTP POST without any CSRF synchronizer token. Struts 1.x does not provide built-in CSRF protection.

```jsp
<html:form action="incidentreport.do" method="POST" styleClass="checklist_from">
```

An attacker can craft a page that POSTs to `incidentreport.do` (or `dealerIncidentReport.do`) when visited by an authenticated user, causing a report search to be executed in their context. While this particular endpoint is a search (read-only state change), the same structural absence of CSRF tokens affects all POST actions in the application that rely on this form pattern, including the `edit_job` and `add_job` actions in `AdminUnitAction` (which are state-mutating).

**Risk:** For the incident report search forms specifically, risk is lower (data retrieval), but the same missing token on state-changing forms in the application allows cross-site request forgery — unauthorized creation or modification of job records on behalf of authenticated users.

**Recommendation:** Implement a synchronizer token pattern: generate a per-session random token, store it in the session, embed it as a hidden field in every form, and validate it server-side before processing any POST. Apache Struts 1.x `TokenProcessor` (`saveToken` / `isTokenValid`) provides this facility.

---

### MEDIUM: `bean:write` without `filter="true"` — potential XSS from stored data in incident report tables

**File:** `src/main/webapp/html-jsp/reports/incidentReport.jsp` (lines 99–130)
**File:** `src/main/webapp/html-jsp/dealer/incidentReport.jsp` (lines 101–112)

**Description:**
All data fields from `IncidentReportEntryBean` are rendered via `<bean:write>` without setting `filter="true"`. In Struts 1.x, `bean:write` does HTML-encode output **by default** (`filter` defaults to `true`), so this is not currently exploitable assuming the Struts library version behaves as documented.

However, the absence of an explicit `filter="true"` attribute represents a maintenance risk: if the template is ever modified to use `<%= %>` scriptlet output (as is partially done elsewhere in the same files with date parameters), the encoding guarantee disappears silently. This is also a code-quality concern that reviewers should flag during peer review.

Additionally, the `signature` and `image` properties are rendered as `href` attribute values:
```jsp
href="<bean:write name="incidentEntry" property="signature"/>"
```
If `signature` or `image` contain a `javascript:` URI (possible if the database value has been tampered with), `bean:write`'s HTML encoding does not prevent URL-based XSS in `href` context — `javascript:alert(1)` does not contain HTML special characters and will not be encoded.

**Risk:** Currently low risk for standard text fields due to Struts default HTML encoding, but moderate risk for the `href` context with `javascript:` URI injection if stored data is attacker-influenced.

**Recommendation:** Add `filter="true"` explicitly on all `<bean:write>` tags as a defense-in-depth measure. For URL-valued properties (`signature`, `image`), validate that the value begins with `https://` server-side before setting it on the bean, and consider using a Content Security Policy header to block `javascript:` navigation.

---

### MEDIUM: `signature` and `image` URLs constructed by string concatenation with database values — potential open redirect or URL injection

**File:** `src/main/java/com/querybuilder/incidents/IncidentReportByCompanyIdQuery.java` (lines 75–76)

**Description:**
The `signature` and `image` URLs are assembled by prepending a fixed S3 base URL to a raw database string:

```java
.signature(RuntimeConf.cloudImageURL + result.getString("signature"))
.image(RuntimeConf.cloudImageURL + result.getString("image"))
```

Where `RuntimeConf.cloudImageURL = "https://s3.amazonaws.com/forkliftiq360/image/"`.

If an attacker can store a crafted value in the `signature` or `image` database column (e.g., through a mobile app API endpoint that writes incident records), they could inject:
- A path traversal segment: `../../malicious-bucket/evil.js`
- An absolute URL by injecting `//evil.com/payload` as the column value — in that case the concatenation yields `https://s3.amazonaws.com/forkliftiq360/image///evil.com/payload` which most browsers normalize to `https://evil.com/payload` (open redirect / resource hijack via URL normalization).
- A `javascript:` URI as noted above.

**Risk:** If database writes of incident signature/image paths are not validated, this can lead to open redirect, resource hijacking, or stored XSS via `javascript:` URI in the `href` attribute.

**Recommendation:** Validate that the stored path component is a plain filename or safe relative path (e.g., matches `^[a-zA-Z0-9_\-\.]+$`) before concatenation. Reject or sanitize values that begin with `/`, `//`, or a scheme like `javascript:`.

---

### MEDIUM: SQL query logged before execution — sensitive query content written to log files

**File:** `src/main/java/com/dao/JobsDAO.java` (lines 53, 124)

**Description:**
Both `getJobList` and `getJobListByJobId` call `log.info(sql)` with the fully assembled SQL string immediately before executing it:

```java
// getJobList, line 53
log.info(sql);
rs = stmt.executeQuery(sql);

// getJobListByJobId, line 124
log.info(sql);
rs = stmt.executeQuery(sql);
```

Because these SQL strings are built by concatenating user-supplied request parameters (`equipId`, `jobNo`), any malicious payload in those parameters is written verbatim to the log file before the query executes. An attacker attempting SQL injection will have their full injection string recorded — but this also means that legitimate input values (which may include sensitive business data such as job numbers) are written to logs in plaintext, which may violate log data retention and access control policies.

More practically: an attacker with log access (via a separate vulnerability — path traversal, log viewer, etc.) can inspect their own injection attempts to confirm the exact SQL structure and tune their payload.

**Risk:** Query structure disclosure in logs aids SQL injection exploitation; user-controlled data written to logs may satisfy attacker reconnaissance if log access is obtained.

**Recommendation:** Remove `log.info(sql)` calls that log dynamically constructed SQL. Use parameterized logging for diagnostic purposes (logging only the static query template, not the final assembled string with parameter values).

---

### MEDIUM: `InfoLogger.logException` duplicates stack trace to both log file and `System.err`

**File:** `src/main/java/com/util/InfoLogger.java` (lines 44–49)

**Description:**
`logException` calls both `e.printStackTrace(new PrintWriter(sw))` (to capture for log4j) and `e.printStackTrace()` (which writes to `System.err` / stdout of the Tomcat process):

```java
public static void logException(Logger log, final Exception e) {
    StringWriter sw = new StringWriter();
    e.printStackTrace(new PrintWriter(sw));
    e.printStackTrace();          // <-- also written to System.err
    log.error(sw);
}
```

The `e.printStackTrace()` call writes the full stack trace to the Tomcat process standard error stream. In production environments this stream may be redirected to `catalina.out` or displayed in monitoring consoles with less access control than the structured log files managed by log4j. Stack traces often include class names, package structures, and internal library versions which aid an attacker in fingerprinting the application.

Additionally, `InfoLogger` itself is initialized via a `static {}` block that calls `e.printStackTrace()` on failure (line 22), again writing directly to stderr.

**Risk:** Stack traces exposed via stderr may reach monitoring dashboards or support personnel who should not have access to internal error details; aids attacker reconnaissance.

**Recommendation:** Remove the bare `e.printStackTrace()` calls; rely solely on `log.error(sw)` (or use the log4j `log.error("message", e)` overload directly).

---

### LOW: `index.jsp` — Struts `logic:redirect` does not prevent Tomcat serving the JSP source on certain error paths

**File:** `src/main/webapp/index.jsp` (lines 1–2)

**Description:**
`index.jsp` consists of two lines:
```jsp
<%@ include file="includes/importLib.jsp"%>
<logic:redirect forward="welcome"></logic:redirect>
```

The `logic:redirect` tag issues an HTTP 302 redirect to the `welcome` forward defined in `struts-config.xml`. This is functionally correct for normal operation. However:

1. If `importLib.jsp` throws a runtime exception before the redirect tag executes (e.g., if a required tag library is missing), Tomcat may serve a partial or empty response without redirecting.
2. The redirect is a 302 (temporary), not a 301 (permanent), which means browsers will always re-request `index.jsp` rather than caching the redirect to the login page. This is a minor informational issue.
3. There is no explicit check for an existing authenticated session in `index.jsp` itself — the redirect goes to `welcome.do`, which is excluded from the auth gate (`excludeFromFilter` returns `false` for `welcome.do`). Depending on the behavior of the welcome action, an unauthenticated user landing at `welcome.do` may see a login page (correct), but this relies on the welcome action performing its own session check rather than the pre-flight servlet.

**Risk:** Low — in normal operation the redirect works correctly. Edge-case error paths could expose application state.

**Recommendation:** Confirm that the `welcome.do` action enforces login (or redirects to `login.do`). Consider using an HTTP 301 if the root URL always redirects to the same login page. Add a `response.setHeader("Cache-Control", "no-store")` before the redirect to prevent caching of the root URL response.

---

### LOW: `JobDetailsBean` has no Lombok `@Data` — no `toString()` credential leak risk, but also no equals/hashCode

**File:** `src/main/java/com/bean/JobDetailsBean.java`

**Description:**
`JobDetailsBean` is written as a plain Java bean with manual getters and setters, without Lombok annotations. This means there is no auto-generated `toString()` that could leak bean field values to logs. This is actually the safer pattern compared to other beans in the codebase that use `@Data`.

However, for completeness: if this class were ever migrated to use `@Data`, all fields including `driverName`, `description`, `jobTitle`, and `jobNo` would be included in the generated `toString()`. If such objects were ever passed to a logger (e.g., `log.info(bean.toString())`), business-sensitive job information would be written to log files.

**Risk:** Informational — current code has no Lombok `toString()` exposure. The risk is latent.

**Recommendation:** No immediate action required. Document that if Lombok annotations are added in future, the `@ToString.Exclude` annotation should be applied to any field that constitutes sensitive business data.

---

### LOW: `IncidentReportFilterBean` and `IncidentReportEntryBean` — Lombok `@Data` generates `toString()` containing PII

**File:** `src/main/java/com/bean/IncidentReportEntryBean.java` (line 8)
**File:** `src/main/java/com/bean/IncidentReportFilterBean.java` (line 9)

**Description:**
Both beans use `@Data` (or `@Data` on a parent). Lombok's `@Data` annotation generates a `toString()` method that includes all fields. `IncidentReportEntryBean` contains:

```java
private String driverName;
private String description;
private String witness;
private String location;
private String signature;   // URL to a signature image
private String image;       // URL to an incident image
```

These are personally identifiable and operationally sensitive fields. If any logging statement anywhere in the application passes an `IncidentReportEntryBean` instance to a logger (e.g., in a catch block or debug trace), all of this data — including URLs to stored signature images — would be written to log files in plaintext.

`IncidentReportBean` (which holds `List<IncidentReportEntryBean>`) also uses `@Data`, so logging a full report bean would dump every entry.

**Risk:** PII (driver names, incident descriptions, witness names, locations) and S3 URL leakage to log files if beans are ever logged. Depending on jurisdiction, logging PII to application logs may violate data protection regulations (GDPR, CCPA, etc.).

**Recommendation:** Apply `@ToString.Exclude` to PII-bearing fields in `IncidentReportEntryBean`, or replace `@Data` with `@Getter @Setter @EqualsAndHashCode` and write a custom `toString()` that omits sensitive fields.

---

### INFO: `addJob` uses `SELECT MAX(id)+1` for ID generation — race condition under concurrent inserts

**File:** `src/main/java/com/dao/JobsDAO.java` (lines 193–213)

**Description:**
The `addJob` method manually computes the next job ID using `SELECT MAX(id)+1 FROM jobs` and then uses it in a subsequent INSERT, without any transaction isolation or locking:

```java
sql = "select max(id)+1 from jobs";
rs = stmt.executeQuery(sql);
if (rs.next()) { job_id = rs.getString(1); }

sql = "insert into jobs(unit_id, description, job_title, job_no, id) values (?,?,?,?,?)";
ps = conn.prepareStatement(sql);
ps.setInt(5, Integer.parseInt(job_id));
```

Two concurrent `addJob` calls can obtain the same `MAX(id)+1` value and then one will fail with a primary key constraint violation. The error is caught and re-thrown as `SQLException` but the operation is not retried, resulting in a job not being created.

This is not a direct security vulnerability, but a reliability defect that could be exploited to cause a denial of service by flooding the add-job endpoint with concurrent requests.

**Risk:** Data loss (job creation failures under concurrent load); potential DoS via repeated concurrent requests causing lock contention.

**Recommendation:** Use a database sequence or the `SERIAL`/`IDENTITY` column type for auto-increment, or use `INSERT ... RETURNING id` (PostgreSQL) and remove the manual ID computation entirely.

---

### INFO: `mailer.do`, `api.do`, `loadbarcode.do`, `uploadfile.do` excluded from authentication gate

**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java` (lines 105–113)

**Description:**
The following endpoints are excluded from session/authentication verification in `PreFlightActionServlet.excludeFromFilter`:

- `mailer.do`
- `api.do`
- `adminRegister.do`
- `switchRegister.do`
- `swithLanguage.do` (note typo — `swith` not `switch`)
- `resetpass.do`
- `goResetPass.do`
- `loadbarcode.do`
- `uploadfile.do`

Each of these endpoints receives requests without any `sessCompId` check in the pre-flight servlet. Any security for these endpoints depends entirely on the action classes themselves implementing authentication checks. `uploadfile.do` and `api.do` in particular are high-value targets: if they do not independently validate session or authentication, they may accept unauthenticated file uploads or API calls.

This finding is scoped to alerting that these exclusions exist and should each be independently audited. The naming typo (`swithLanguage.do`) also suggests the intended path `switchLanguage.do` may not be excluded, which could cause an unnecessary auth redirect for legitimate language-switching requests.

**Risk:** Informational for the current audit scope; requires follow-on verification of each excluded endpoint's own authentication logic.

**Recommendation:** Audit each excluded endpoint. Document the business reason for each exclusion. Fix the typo `swithLanguage.do`. Consider whether `uploadfile.do` and `api.do` implement their own stateless authentication (e.g., API tokens) and verify that they do so correctly.

---

## Summary

| # | Severity | Title | File |
|---|----------|-------|------|
| 1 | CRITICAL | SQL Injection in `getJobList` via `equipId` | JobsDAO.java:52 |
| 2 | CRITICAL | SQL Injection in `getJobListByJobId` via `equipId`+`jobNo` | JobsDAO.java:123 |
| 3 | CRITICAL | IDOR — job queries not scoped to `sessCompId` | JobsDAO.java + AdminUnitAction.java |
| 4 | HIGH | Broken DCL — `IncidentReportDAO` locks on wrong class + non-volatile field | IncidentReportDAO.java:18 |
| 5 | HIGH | Auth gate logic inversion / misleading `excludeFromFilter` naming | PreFlightActionServlet.java:98 |
| 6 | HIGH | Reflected XSS — date params injected raw into JS `<script>` block | reports/incidentReport.jsp:164; dealer/incidentReport.jsp:149 |
| 7 | HIGH | IDOR — `editJob` accepts any `job_id` without company scope | JobsDAO.java:275; AdminUnitAction.java:85 |
| 8 | MEDIUM | CSRF — no synchronizer token on incident report or job forms | reports/incidentReport.jsp:22; dealer/incidentReport.jsp:27 |
| 9 | MEDIUM | `bean:write` without explicit `filter="true"`; `javascript:` URI in `href` | reports/incidentReport.jsp; dealer/incidentReport.jsp |
| 10 | MEDIUM | URL injection via string concat of DB value onto S3 base URL | IncidentReportByCompanyIdQuery.java:75–76 |
| 11 | MEDIUM | SQL queries logged before execution — user-controlled content in logs | JobsDAO.java:53, 124 |
| 12 | MEDIUM | `InfoLogger.logException` duplicates stack traces to `System.err` | InfoLogger.java:47 |
| 13 | LOW | `index.jsp` redirect correctness / caching edge cases | index.jsp |
| 14 | LOW | `JobDetailsBean` no Lombok — latent PII-in-toString risk if refactored | JobDetailsBean.java |
| 15 | LOW | Lombok `@Data` on `IncidentReportEntryBean` generates PII-inclusive `toString()` | IncidentReportEntryBean.java; IncidentReportFilterBean.java |
| 16 | INFO | `addJob` uses `MAX(id)+1` — race condition under concurrent inserts | JobsDAO.java:195 |
| 17 | INFO | Multiple endpoints excluded from auth gate — require individual audit | PreFlightActionServlet.java:100–113 |

---

**CRITICAL: 3 / HIGH: 4 / MEDIUM: 5 / LOW: 3 / INFO: 2**
