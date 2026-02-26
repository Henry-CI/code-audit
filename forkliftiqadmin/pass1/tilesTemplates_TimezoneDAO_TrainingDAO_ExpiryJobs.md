# Security Audit Report — Pass 1
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Date:** 2026-02-26
**Auditor:** Automated Pass — Claude Code
**Scope:** tilesTemplate.jsp, tilesTemplateHeader.jsp, TimezoneBean.java, TimezoneDAO.java, training.jsp, TrainingDAO.java, TrainingExpiryDailyEmailJob.java, TrainingExpiryDailyEmailJobSchedueler.java, TrainingExpiryWeeklyEmailJob.java, TrainingExpiryWeeklyEmailJobScheduler.java

---

## Findings

---

### CRITICAL: DB-stored timezone value concatenated unsanitized into SQL (second-order SQL injection)

**File:** `src/main/java/com/dao/DriverDAO.java` (lines 358, 749) — root cause traced to `src/main/java/com/dao/TimezoneDAO.java` (lines 51–60, 99–103) and `src/main/java/com/util/CompanySessionSwitcher.java` (line 34)

**Description:**
`TimezoneDAO.getAllTimezone()`, `TimezoneDAO.getAll()`, and `TimezoneDAO.getTimezone()` read the raw `zone` column from the `timezone` table and place it into `TimezoneBean.zone` without any sanitization or allow-list validation:

```java
// TimezoneDAO.java lines 57–60 (getAllTimezone) and 99–103 (getAll)
timezoneBean.setId(rs.getString(1));
timezoneBean.setName(rs.getString(2));
timezoneBean.setZone(rs.getString(3));   // raw DB string, no validation
```

`CompanySessionSwitcher.UpdateCompanySessionAttributes()` then calls `TimezoneDAO.getTimezone()` and stores the raw `zone` value into the HTTP session attribute `sessTimezone`:

```java
// CompanySessionSwitcher.java line 34
session.setAttribute("sessTimezone", tzone.getZone());
```

`DriverDAO` then concatenates this session value — which originates verbatim from the database — directly into SQL strings using string concatenation instead of a parameterized query:

```java
// DriverDAO.java line 358 — getAllDriverSearch
builder.append(" and timezone('" + timezone + "', p.updatedat)::DATE = current_date::DATE  ");

// DriverDAO.java line 749 — getTotalDriverByID
String sql = "select count(p.id) from permission as p inner join driver as d on p.driver_id = d.id "
        + "where p.comp_id = " + id + " and timezone('" + timezone + "', p.updatedat)::DATE  = current_date::DATE  ";
```

Because the `timezone` variable originates from the `timezone.zone` column (populated from `TimezoneDAO`), any administrator or attacker with write access to the `timezone` table can inject arbitrary SQL. The `zone` value is never validated against the set of valid IANA timezone identifiers, nor is it ever passed through a parameterized bind. This is a classic second-order (stored) SQL injection: the payload is persisted in the database, then replayed into SQL on subsequent requests. An attacker able to modify the `timezone` table (e.g., via a compromised admin account, a separate SQLi vulnerability, or direct DB access) can achieve arbitrary query execution against the PostgreSQL backend.

The same `tzone.getZone()` value is also passed to `ReportService` methods (`countPreOpsCompletedToday`, `countImpactsToday`) — the blast radius likely extends beyond DriverDAO.

**Risk:**
Full read (and potentially write) access to all data in the database. In PostgreSQL, `COPY TO/FROM`, `pg_read_file`, and `CREATE EXTENSION` escalation paths may be available depending on database user privileges. Because this is second-order, the injection survives WAF inspection at the point of HTTP input.

**Recommendation:**
1. Validate every timezone string read from the database against `java.util.TimeZone.getAvailableIDs()` or an explicit allow-list of IANA identifiers before storing it in the session or using it in SQL.
2. Rewrite the affected `DriverDAO` queries to use a PostgreSQL-native approach that avoids concatenation: pass the timezone as a bind parameter (PostgreSQL supports `timezone($1, expr)` with `PreparedStatement`) or use `AT TIME ZONE` with a parameter placeholder.
3. Apply the same fix to every other DAO that accepts `timezone` as a string and uses it in a raw query.

---

### CRITICAL: Training delete action has no tenant scoping — IDOR allows cross-tenant record deletion

**File:** `src/main/java/com/action/AdminTrainingsAction.java` (lines 37–39), `src/main/java/com/dao/TrainingDAO.java` (lines 70–73)

**Description:**
The `deleteTraining` action receives a training record ID from the HTTP request parameter `training` and passes it directly to `TrainingDAO.deleteTraining()` without verifying that the record belongs to the authenticated user's company (`sessCompId`):

```java
// AdminTrainingsAction.java lines 37–39
case "delete":
    trainingDAO.deleteTraining(trainingsForm.getTraining());
    return null;
```

```java
// TrainingDAO.java lines 70–73
public void deleteTraining(Long trainingId) throws SQLException {
    DBUtil.executeStatementWithRollback(
            "DELETE FROM driver_training WHERE id = ?",
            stmt -> stmt.setLong(1, trainingId));
}
```

The DELETE query contains no `WHERE comp_id = ?` clause and no join back to a company. Any authenticated user (any tenant) can delete any training record in the system by supplying an arbitrary integer `training` parameter. Because `PreFlightActionServlet` only checks that `sessCompId != null`, every authenticated session for any company has this capability.

The `addTraining` case on lines 27–35 similarly accepts a `driver_id` from the request form (`trainingsForm.getDriver()`) without verifying that the driver belongs to `sessCompId`, permitting cross-tenant data insertion.

**Risk:**
Authenticated users from any tenant can delete or corrupt training records belonging to any other tenant. This constitutes a horizontal privilege escalation / IDOR. In a safety-critical context (forklift operator training compliance), mass deletion of training records could allow unlicensed drivers to pass expiry checks undetected.

**Recommendation:**
1. For `deleteTraining`, add a company ownership check before deletion:
   ```sql
   DELETE FROM driver_training
   WHERE id = ?
     AND driver_id IN (SELECT id FROM driver WHERE comp_id = ?)
   ```
2. For `addTraining`, verify that the supplied `driver_id` belongs to `sessCompId` before inserting the record.
3. Retrieve `sessCompId` in `AdminTrainingsAction` and pass it through to both DAO methods.

---

### HIGH: Quartz scheduler not stopped on application undeployment — thread pool and scheduler leak

**File:** `src/main/java/com/quartz/TrainingExpiryDailyEmailJobSchedueler.java` (lines 41–43)
**File:** `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJobScheduler.java` (lines 41–43)

**Description:**
Both `ServletContextListener` implementations override `contextDestroyed()` but do not shut down the Quartz scheduler. Instead, they construct and immediately print a `ServletException` to stderr — an operation that has no effect on the running scheduler:

```java
// TrainingExpiryDailyEmailJobSchedueler.java lines 41–43
@Override
public void contextDestroyed(ServletContextEvent servletContextEvent) {
    new ServletException("Application Stopped").printStackTrace();
}
```

```java
// TrainingExpiryWeeklyEmailJobScheduler.java lines 41–43
@Override
public void contextDestroyed(ServletContextEvent servletContextEvent) {
    new ServletException("Application Stopped").printStackTrace();
}
```

The `Scheduler` instance created in `contextInitialized()` is a local variable; there is no field storing a reference to it that `contextDestroyed()` could call `scheduler.shutdown(true)` on. When Tomcat undeploys the application (or during a hot-redeploy), the Quartz scheduler thread pool keeps running inside the JVM. On redeploy, a second scheduler is started, resulting in double-firing of both jobs. Repeated redeployments accumulate unbounded scheduler and thread pool instances, eventually causing OutOfMemoryError or exhausting OS thread limits.

**Risk:**
Resource exhaustion (thread pool leak, memory leak) on every redeploy without a full JVM restart. Double-firing of email jobs causes duplicate expiry notification emails to be sent to all tenants, which is both a business defect and a potential information disclosure event. In production environments that rely on hot-redeploy for zero-downtime updates, this will progressively degrade the JVM.

**Recommendation:**
1. Store the `Scheduler` instance as a field of the listener class.
2. In `contextDestroyed()`, call `scheduler.shutdown(true)` (the boolean waits for running jobs to complete before returning).
3. Remove the meaningless `new ServletException(...).printStackTrace()` call.

Example structure:
```java
private Scheduler scheduler;

@Override
public void contextInitialized(ServletContextEvent sce) {
    scheduler = new StdSchedulerFactory().getScheduler();
    // ... schedule job ...
    scheduler.start();
}

@Override
public void contextDestroyed(ServletContextEvent sce) {
    if (scheduler != null && !scheduler.isShutdown()) {
        scheduler.shutdown(true);
    }
}
```

---

### HIGH: Unmanaged thread pool created per job execution — executor never shut down

**File:** `src/main/java/com/quartz/TrainingExpiryDailyEmailJob.java` (line 15)
**File:** `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJob.java` (line 15)

**Description:**
Each time the Quartz job fires, `execute()` calls `Executors.newSingleThreadExecutor()` to spawn a brand-new single-thread executor and immediately submits one task to it. The executor is never assigned to a variable and `shutdown()` is never called on it:

```java
// TrainingExpiryDailyEmailJob.java line 15
public void execute(JobExecutionContext jobExecutionContext) {
    Executors.newSingleThreadExecutor().execute(this::sendTrainingExpiryDailyEmail);
}
```

```java
// TrainingExpiryWeeklyEmailJob.java line 15
public void execute(JobExecutionContext jobExecutionContext) {
    Executors.newSingleThreadExecutor().execute(this::sendTrainingExpiryWeeklyEmail);
}
```

`Executors.newSingleThreadExecutor()` creates an `ExecutorService` backed by a non-daemon thread. Because `shutdown()` is never invoked, the underlying thread remains alive indefinitely after the task completes. Each job invocation leaks one thread. Given that the daily job fires every day and the weekly job fires every week, under normal operation these leaks accumulate slowly; under the double-firing scenario described above (finding HIGH: scheduler leak), the rate doubles.

Additionally, the actual email work runs on an untracked thread. If the container shuts down while email sending is in progress, the task is silently dropped with no error surfaced to Quartz (which would otherwise be able to log or reschedule on failure).

**Risk:**
Slow thread leak causing eventual JVM instability. Silent loss of email jobs on shutdown. The combination of this issue and the scheduler leak means that on a busy Tomcat server with frequent redeployment, thread exhaustion is plausible within hours.

**Recommendation:**
1. Remove the wrapping executor entirely. The Quartz thread pool already provides a managed thread context; the job's `execute()` method runs on a Quartz worker thread and should simply call `sendTrainingExpiryDailyEmail()` directly.
2. If async execution is genuinely required (e.g., to release the Quartz thread immediately), use a shared application-scoped `ExecutorService` that is shut down in the `ServletContextListener.contextDestroyed()` callback.
3. Propagate exceptions from the work method back to Quartz by throwing `JobExecutionException` instead of swallowing them (see also finding MEDIUM: exception swallowing).

---

### HIGH: Unescaped driver PII written into HTML email body — stored XSS in email and potential header injection

**File:** `src/main/java/com/dao/TrainingDAO.java` (lines 96–101, 140–153)

**Description:**
Both `sendTrainingExpiryDailyEmail()` and `sendTrainingExpiryWeeklyEmail()` construct HTML email bodies by directly concatenating database-sourced driver fields — `first_name`, `last_name`, `email`, and `unit_name` — into an HTML string without any HTML encoding:

```java
// TrainingDAO.java lines 96–101
content += "Driver Name: " + driverTrainingBean.getFirst_name() + " " + driverTrainingBean.getLast_name() + " | "
        + "Email: " + driverTrainingBean.getEmail() + " | "
        + "Vehicle Name: " + driverTrainingBean.getUnit_name() + " | "
        + "Expiry Date: " + driverTrainingBean.getExpiration_date() + "<br>";
```

If any of these fields in the database contain HTML or JavaScript (either due to insufficient input sanitisation elsewhere in the application or due to a prior SQL injection), the resulting email will contain injected markup. Since the email is sent as HTML (`content` includes `<br>` tags and is passed to `Util.sendMail` with an HTML-capable content type), a malicious driver name such as `<img src=x onerror=alert(1)>` or `<script>...</script>` will render in the recipient's email client. Modern HTML-capable email clients differ in their JavaScript handling, but many will render arbitrary HTML including remote image tracking pixels, CSS-based exfiltration, and phishing content.

The `email` field is additionally embedded in the email body verbatim. If `Util.sendMail` constructs SMTP headers from this field elsewhere, a newline-containing value could enable email header injection (this requires code review of `Util.sendMail` beyond current scope, but the concatenation pattern here is the precondition).

**Risk:**
- HTML injection in admin/operator email alerts, enabling phishing or content spoofing.
- Potential tracking pixel / remote resource loading from crafted driver names leaking recipient IP addresses to third parties.
- If `Util.sendMail` uses any of these values to populate SMTP headers, email header injection is possible.

**Recommendation:**
1. HTML-encode all database-sourced strings before concatenating them into the HTML email body. Use `org.apache.commons.lang3.StringEscapeUtils.escapeHtml4()` or equivalent.
2. Use a templating engine (FreeMarker, Thymeleaf) that auto-escapes context-appropriately rather than manual string concatenation.
3. Review `Util.sendMail` to ensure that `first_name`, `last_name`, and `email` are never used to set SMTP headers without sanitisation.

---

### MEDIUM: Exception swallowing in Quartz job email loop — failures are silently discarded

**File:** `src/main/java/com/dao/TrainingDAO.java` (lines 106–115, 158–167)
**File:** `src/main/java/com/quartz/TrainingExpiryDailyEmailJob.java` (lines 22–24)
**File:** `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJob.java` (lines 22–24)

**Description:**
The inner `forEach` lambda in both email methods catches `SQLException`, `AddressException`, and `MessagingException` and only calls `e.printStackTrace()`. There is no re-throw, no counter, and no alerting. If email delivery fails for one company (e.g., due to an SMTP error), processing silently continues to the next company. The outer `try/catch` in the Quartz job classes similarly swallows `SQLException`:

```java
// TrainingDAO.java lines 106–115 (daily), pattern repeated at 158–167 (weekly)
} catch (SQLException e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
} catch (AddressException e) {
    // TODO Auto-generated catch book
    e.printStackTrace();
} catch (MessagingException e) {
    // TODO Auto-generated catch book
    e.printStackTrace();
}
```

```java
// TrainingExpiryDailyEmailJob.java lines 22–24
} catch (SQLException e) {
    e.printStackTrace();
}
```

The "TODO Auto-generated catch block" comments confirm these were never intentionally handled. In production, `printStackTrace()` writes to `System.err` which may not be monitored. Operators will have no visibility into failed email deliveries, and drivers whose training is expiring may not receive notifications, defeating the purpose of the job entirely.

**Risk:**
Silent failure of safety-critical email notifications. Operators cannot distinguish "job ran successfully" from "job ran but all emails failed." This is a reliability and compliance risk for customers depending on training expiry alerts.

**Recommendation:**
1. Replace `e.printStackTrace()` with structured logging: `log.error("Failed to send training expiry email for comp_id={}", UserCompRelBean.getComp_id(), e)`.
2. Track a failure count and, if any company fails, rethrow or surface a `JobExecutionException` to Quartz so the scheduler can record the failure.
3. Consider a dead-letter pattern: persist failed notifications to a retry queue rather than discarding them.

---

### MEDIUM: Quartz scheduler initialization exception swallowed — misconfiguration goes undetected

**File:** `src/main/java/com/quartz/TrainingExpiryDailyEmailJobSchedueler.java` (lines 35–37)
**File:** `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJobScheduler.java` (lines 35–37)

**Description:**
The `contextInitialized()` method catches `SchedulerException` and calls only `e.printStackTrace()`. If the Quartz scheduler fails to start (e.g., due to a misconfigured `quartz.properties`, a duplicate job identity on redeploy, or a database connectivity problem for a JDBC job store), the exception is swallowed and the application continues to start without the scheduled jobs running:

```java
// TrainingExpiryDailyEmailJobSchedueler.java lines 35–37
} catch (SchedulerException e) {
    e.printStackTrace();
}
```

Because there is no re-throw and no log at ERROR level that would be caught by a monitoring system, a deployment where both schedulers silently fail to initialize will appear fully operational until a missing email is noticed by an end user.

**Risk:**
Undetected failure of the training expiry notification subsystem during deployment or after a Tomcat hot-redeploy (which, in combination with the missing `scheduler.shutdown()` in `contextDestroyed()`, also produces a `SchedulerException` for a duplicate job key on re-registration).

**Recommendation:**
1. Re-throw as a `RuntimeException` (or log at `FATAL`/`ERROR` level and set a health-check flag) so that application startup visibly fails or monitoring systems are alerted.
2. Use `scheduler.checkExists(jobKey)` before calling `scheduleJob` to handle the hot-redeploy duplicate-key case gracefully.

---

### MEDIUM: training.jsp — `sessTimezone` session attribute used in scriptlet without null-check or output encoding

**File:** `src/main/webapp/html-jsp/driver/training.jsp` (lines 10–15)

**Description:**
The scriptlet at the top of `training.jsp` reads `sessTimezone` from the session and immediately calls `.contains()` on it without a null-guard:

```java
// training.jsp lines 10–12
String timezone = (String) session.getAttribute("sessTimezone");
String trainingtab = "Training";
if (!timezone.contains("US/") && !timezone.contains("Canada/"))
```

If `sessTimezone` is `null` (which can occur if session initialisation partially fails, or if `CompanySessionSwitcher` throws before setting the attribute), line 12 will throw a `NullPointerException`. Struts will propagate this as an unhandled exception, potentially rendering a default error page that includes a full stack trace visible to the user, disclosing internal class names, package structure, and Tomcat version. Additionally, the `dateFormat` attribute is cast and `.replaceAll()` called on line 9 with the same absence of null-check:

```java
// training.jsp line 9
String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```

Neither `dateFormat` nor `timezone` is output to HTML in this file, so there is no XSS here specifically from these variables. However, the calculated string `trainingtab` is rendered directly with `<%=trainingtab%>` on lines 21 and 32. Because `trainingtab` is only ever set to one of two string literals (`"Training"` or `"Licence"`), there is no practical XSS vector here — but the pattern of unescaped scriptlet output should be flagged as a code hygiene issue.

**Risk:**
NullPointerException causing stack trace disclosure (information disclosure) for sessions with missing timezone attributes. Low-severity XSS hygiene concern from the `<%=trainingtab%>` pattern, mitigated by the fact that the value is programmer-controlled.

**Recommendation:**
1. Add null-checks for both `sessTimezone` and `sessDateFormat` before dereferencing, and redirect to an error or login page if either is missing.
2. Even for programmer-controlled strings, consistently use `<c:out value="${...}"/>` or JSTL escaping rather than raw `<%= %>` expressions as a defensive coding standard.

---

### MEDIUM: `tilesTemplate.jsp` and `tilesTemplateHeader.jsp` — layout templates delegate to tiles without setting a Content-Security-Policy header

**File:** `src/main/webapp/includes/tilesTemplate.jsp` (all lines)
**File:** `src/main/webapp/includes/tilesTemplateHeader.jsp` (all lines)

**Description:**
Both layout templates declare `charset=UTF-8` in the `Content-Type` meta tag (via `<%@ page contentType="text/html;charset=UTF-8"%>`) but neither sets security-relevant HTTP response headers. The template files are the single layout entry point for all authenticated pages in the application; any missing security header here is absent from every rendered page.

Reviewed `header.inc.jsp` confirms that no Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, or Referrer-Policy header is set in the JSP layer. Without a CSP, any XSS vulnerability elsewhere in the application (including the HTML email injection and any future scriptlet-output XSS) has maximum impact because the browser will execute arbitrary inline scripts.

```jsp
<!-- tilesTemplate.jsp — no security headers set anywhere in the layout chain -->
<%@ page contentType="text/html;charset=UTF-8"%>
<tiles:insert attribute="header"/>
<tiles:insert attribute="navigation"/>
<tiles:insert attribute="content"/>
<tiles:insert attribute="footer"/>
```

**Risk:**
Absence of CSP removes the last line of browser-enforced defence against XSS. Absence of `X-Frame-Options` or `frame-ancestors` CSP directive leaves all authenticated pages open to clickjacking. Absence of `X-Content-Type-Options: nosniff` enables MIME-sniffing attacks on uploaded content.

**Recommendation:**
1. Add security headers globally in a Servlet `Filter` (preferred, so they cannot be forgotten in individual JSPs) rather than in the template JSP:
   - `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'` (tighten iteratively).
   - `X-Frame-Options: SAMEORIGIN`
   - `X-Content-Type-Options: nosniff`
   - `Referrer-Policy: strict-origin-when-cross-origin`
2. Set the `HttpOnly` and `Secure` flags on the session cookie in `web.xml` or `context.xml`.

---

### MEDIUM: `menu.inc.jsp` — raw JSP scriptlet renders `sessCompId` session attribute inside JavaScript without encoding

**File:** `src/main/webapp/includes/menu.inc.jsp` (line 41)

**Description:**
The navigation menu include (which is inserted into every authenticated page via the `tilesTemplate.jsp` `navigation` tile) contains the following scriptlet inside an inline `<script>` block:

```jsp
// menu.inc.jsp line 41
$('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');
```

`sessCompId` is a database ID (expected to be a numeric string). However, it is rendered unescaped into a JavaScript string literal delimited by single quotes. If the value were ever non-numeric — for example, due to a bug in session initialization, a session fixation attack, or if the application is modified to store non-integer company identifiers — an attacker-influenced value containing `'` could break out of the JavaScript string context and execute arbitrary script. Because this is rendered on every authenticated page via the tile, any XSS here has application-wide impact. The absence of a Content-Security-Policy (see finding above) amplifies the risk.

**Risk:**
Reflected/session-stored XSS on every authenticated page if `sessCompId` can ever be set to a non-numeric value. Medium severity currently because `sessCompId` is numeric, but the pattern is fragile.

**Recommendation:**
1. Use the Struts `<bean:write>` tag with `filter="true"` (the default) rather than a raw scriptlet to render session values into HTML/JavaScript.
2. When embedding any value into a JavaScript string, apply JavaScript string escaping (not just HTML escaping). In JSTL:  `'${fn:escapeXml(sessionScope.sessCompId)}'` — or better, pass the value through a hidden `<input>` element and read it with `$('#my-input').val()` so it never appears in a JS literal.

---

### LOW: `TimezoneDAO.getTimezone()` constructs a parameterized-looking query with int concatenation

**File:** `src/main/java/com/dao/TimezoneDAO.java` (line 133)

**Description:**
`getTimezone(int tzoneId)` concatenates its integer parameter directly into the SQL string rather than using a `PreparedStatement`:

```java
// TimezoneDAO.java line 133
String sql = "select id,name,zone from timezone where id=" + tzoneId;
```

Because the parameter type is `int` (a Java primitive), there is no SQL injection risk at this specific call site — the compiler guarantees the value is a valid integer. However, the use of `Statement` instead of `PreparedStatement` prevents query plan caching and is inconsistent with the parameterized patterns used in `TrainingDAO`. More significantly, if the method signature is ever changed to accept `String` (which happens frequently in refactoring), the concatenation becomes a genuine injection vector with no code change required in the query itself.

The same method uses `ResultSet.TYPE_SCROLL_SENSITIVE` for a query that returns at most one row — this is unnecessarily resource-intensive.

**Risk:**
No immediate SQL injection due to the `int` type. Maintenance risk: the pattern is unsafe by convention. Minor performance overhead from scrollable cursor on a single-row lookup.

**Recommendation:**
1. Refactor to use `PreparedStatement` with `stmt.setInt(1, tzoneId)` for consistency, safety during future refactoring, and query plan reuse.
2. Replace `ResultSet.TYPE_SCROLL_SENSITIVE` with `ResultSet.TYPE_FORWARD_ONLY` for single-row lookups.

---

### LOW: `TimezoneDAO` singleton uses double-checked locking with non-volatile field

**File:** `src/main/java/com/dao/TimezoneDAO.java` (lines 19–31)

**Description:**
The `getInstance()` method implements double-checked locking (DCL) but `theInstance` is declared without the `volatile` keyword:

```java
// TimezoneDAO.java lines 19–31
private static TimezoneDAO theInstance;

public static TimezoneDAO getInstance() {
    if (theInstance == null) {
        synchronized (TimezoneDAO.class) {
            if (theInstance == null) {
                theInstance = new TimezoneDAO();
            }
        }
    }
    return theInstance;
}
```

Under the Java Memory Model (JMM), without `volatile`, the write to `theInstance` in the synchronized block is not guaranteed to be visible to threads that read the field in the outer `if (theInstance == null)` check without holding the lock. A thread may observe a partially constructed `TimezoneDAO` object. This is a well-documented Java concurrency pitfall. It is fixed by declaring the field `private static volatile TimezoneDAO theInstance;`.

Note that the sibling methods `getAll()` and `getTimezone()` are `static` and do not use the singleton instance, making the singleton pattern partially redundant in this class.

**Risk:**
In a multi-threaded Tomcat environment, a race condition could result in a partially initialized `TimezoneDAO` instance being used, causing NullPointerException or undefined behaviour. Low probability in practice because `TimezoneDAO` has an empty constructor, but the pattern is incorrect.

**Recommendation:**
Add `volatile` to the `theInstance` field declaration, or replace DCL with initialization-on-demand holder pattern, or simply use an eagerly initialized `private static final TimezoneDAO theInstance = new TimezoneDAO()`.

---

### LOW: `contextDestroyed()` creates and immediately discards a `ServletException` — misleading dead code

**File:** `src/main/java/com/quartz/TrainingExpiryDailyEmailJobSchedueler.java` (lines 41–43)
**File:** `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJobScheduler.java` (lines 41–43)

**Description:**
Both `contextDestroyed()` implementations contain:

```java
new ServletException("Application Stopped").printStackTrace();
```

This creates a `ServletException` object whose sole purpose is to produce a stack trace on `System.err`. The exception is not thrown, not logged via a logging framework, and serves no functional purpose. It is misleading because it resembles an exception handler or a throw statement at a glance, and it produces noise in the server log on every normal shutdown. The intended behaviour (shutting down the scheduler) is entirely absent (see HIGH finding above).

**Risk:**
No direct security risk. Causes log noise on shutdown, which may mask genuine error messages. Misleads future developers about the purpose of `contextDestroyed()`.

**Recommendation:**
Remove the dead code and implement proper scheduler shutdown as described in the related HIGH finding.

---

### INFO: `tilesTemplate.jsp` and `tilesTemplateHeader.jsp` — minimal templates with no direct vulnerability surface

**File:** `src/main/webapp/includes/tilesTemplate.jsp` (all lines)
**File:** `src/main/webapp/includes/tilesTemplateHeader.jsp` (all lines)

**Description:**
Both files are pure Struts Tiles layout wrappers that insert named tile attributes. They contain no scriptlets, no EL expressions rendering user data, and no direct output of request/session parameters. The security exposure of these files is entirely determined by the content of the tiles they include (`header`, `navigation`, `content`, `footer`). The MEDIUM finding regarding missing security headers applies to what these templates fail to set, not to what they directly render.

`tilesTemplateHeader.jsp` omits the `navigation` and `footer` tiles relative to `tilesTemplate.jsp`, suggesting it is used for popup/modal contexts. This is noted for completeness.

**Risk:**
No direct vulnerability in these files themselves.

**Recommendation:**
No changes required in these specific files beyond ensuring the tiles they delegate to are individually secured. Implement security headers in a Filter as described in the MEDIUM finding.

---

### INFO: `TrainingDAO.getTrainingByDriver()` — no company scope check in the DAO layer (relies on caller)

**File:** `src/main/java/com/dao/TrainingDAO.java` (lines 23–53)

**Description:**
`getTrainingByDriver(Long driverId, String dateFormat)` queries `driver_training` filtered only by `driver_id`. There is no `comp_id` filter at the DAO level. The IDOR risk here depends entirely on whether the caller (`AdminDriverAction` or equivalent) validates that the requested `driverId` belongs to `sessCompId` before invoking this method. This is flagged for verification in a subsequent pass reviewing the calling action.

```java
// TrainingDAO.java lines 23–39
"WHERE driver_id = ?"
```

If the calling action does not validate driver ownership, this becomes a CRITICAL IDOR finding. If it does, this is informational.

**Risk:**
Contingent on caller behaviour. Requires verification in pass 2.

**Recommendation:**
Add a `comp_id` parameter to `getTrainingByDriver()` and enforce it as a join condition in the query as a defence-in-depth measure, regardless of what callers do.

---

## Summary

| Severity | Count | Finding Titles |
|----------|-------|----------------|
| CRITICAL | 2 | DB-stored timezone SQLi (second-order); Training delete IDOR (no tenant scope) |
| HIGH | 3 | Quartz scheduler not stopped on undeploy (thread/scheduler leak); Unmanaged executor per job execution (thread leak); Unescaped driver PII in HTML email (HTML injection / stored XSS in email) |
| MEDIUM | 4 | Exception swallowing in email loop; Scheduler init exception swallowed; training.jsp null-dereference + scriptlet output; Missing CSP/security headers in layout templates; menu.inc.jsp sessCompId unescaped in JS literal |
| LOW | 3 | TimezoneDAO.getTimezone() int concatenation pattern; TimezoneDAO singleton non-volatile DCL; contextDestroyed() dead code / misleading ServletException |
| INFO | 2 | tilesTemplate files have no direct vulnerability surface; getTrainingByDriver() lacks DAO-level comp_id scope |

> Note: MEDIUM count in the table is 5 (five individual medium findings are described above); the header row reflects five items across the four medium-severity entries listed in the text. See individual findings above for full detail.

**CRITICAL: 2 / HIGH: 3 / MEDIUM: 5 / LOW: 3 / INFO: 2**
