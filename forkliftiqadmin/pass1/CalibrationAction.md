# Security Audit: CalibrationAction.java
**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**Auditor Pass:** Pass 1
**Date:** 2026-02-26
**Audited File:** src/main/java/com/action/CalibrationAction.java

---

## 1. Reading Evidence

### Package and Class
- **Package:** `com.action`
- **Class:** `CalibrationAction extends org.apache.struts.action.Action`
- **File:** `src/main/java/com/action/CalibrationAction.java`

### Public/Protected Methods

| Line | Method | Signature |
|------|--------|-----------|
| 14 | `execute` | `public ActionForward execute(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception` |

### DAOs / Services Called (call chain)

| Layer | Class | File | Method |
|-------|-------|------|--------|
| Action | `CalibrationAction` | `com/action/CalibrationAction.java:18-19` | Instantiates `CalibrationJob`, calls `job.calibrateAllUnits()` |
| Job | `CalibrationJob` | `com/calibration/CalibrationJob.java:15-24` | `calibrateAllUnits()` — creates `UnitCalibrationGetterInDatabase`, `UnitCalibrationEnderInDatabase`, delegates to `UnitCalibrator` |
| Calibrator | `UnitCalibrator` | `com/calibration/UnitCalibrator.java:16-20` | `calibrateAllUnits()` — fetches all units to calibrate, calls `calibrateUnit()` for each |
| DAO (read) | `UnitCalibrationGetterInDatabase` | `com/calibration/UnitCalibrationGetterInDatabase.java:19-28` | `getUnitsToCalibrate()` — queries ALL units in the `unit` table where `impact_threshold = 0 AND alert_enabled IS FALSE AND reset_calibration_date IS NOT NULL` |
| DAO (read) | `UnitCalibrationGetterInDatabase` | `com/calibration/UnitCalibrationGetterInDatabase.java:53-67` | `getImpactsForUnit()` — queries `v_impacts` view for impacts per unit |
| DAO (write) | `UnitCalibrationEnderInDatabase` | `com/calibration/UnitCalibrationEnderInDatabase.java:9-18` | `endCalibration()` — `UPDATE unit SET impact_threshold = ?, alert_enabled = TRUE, calibration_date = NOW() WHERE id = ?` |

### Form Class
No form bean is declared in struts-config.xml for this action. `ActionForm form` is `null` at runtime.

### struts-config.xml Mapping (line 582-583)

```xml
<action path="/calibration" type="com.action.CalibrationAction">
</action>
```

| Attribute | Value | Notes |
|-----------|-------|-------|
| `path` | `/calibration` | Accessible at `/calibration.do` |
| `name` (form-bean) | **not set** | No form, no validation binding |
| `scope` | **not set** | Defaults to `request` |
| `validate` | **not set** | Defaults to `false` |
| `roles` | **not set** | No declarative role restriction |
| Forwards | **none declared** | Return value of `super.execute()` is `null`; Struts will not forward anywhere |

---

## 2. Security Findings

---

### FINDING-01 — CRITICAL: Unauthenticated Access — No Role Check in Action

**Severity:** CRITICAL
**File:** `src/main/java/com/action/CalibrationAction.java`, line 14-21
**Also:** `src/main/webapp/WEB-INF/struts-config.xml`, line 582-583

**Description:**
`CalibrationAction.execute()` performs zero authentication or authorisation checks before invoking `CalibrationJob.calibrateAllUnits()`. There is no check for `sessCompId`, no role verification, and no `roles` attribute in the struts-config mapping. The action fires the full calibration routine against the entire `unit` table the moment `/calibration.do` is requested.

**Evidence:**

```java
// CalibrationAction.java lines 14-21 — no session or role guard
public ActionForward execute(ActionMapping mapping, ActionForm form,
                             HttpServletRequest request, HttpServletResponse response)
        throws Exception {
    CalibrationJob job = new CalibrationJob();
    job.calibrateAllUnits();           // <-- executes immediately, unconditionally
    return super.execute(mapping, form, request, response);
}
```

```xml
<!-- struts-config.xml line 582-583 — no roles attribute -->
<action path="/calibration" type="com.action.CalibrationAction">
</action>
```

**Why the auth gate does NOT protect this endpoint:**
`PreFlightActionServlet.excludeFromFilter()` returns `true` for `/calibration.do` (it is not in the exclusion list), so a valid `sessCompId` is required. However, `sessCompId` only proves that *some* authenticated session exists — it does not enforce that the caller is a system administrator or any privileged role. Any authenticated user (operator, site admin, dealer, etc.) can trigger this endpoint. Furthermore, the calibration operation acts globally across ALL companies (see FINDING-03), meaning a low-privilege user from Company A can recalibrate units belonging to all other companies.

**Recommendation:**
Add an explicit role check at the top of `execute()` verifying the session role equals `RuntimeConf.ROLE_SYSADMIN`. Alternatively, remove the HTTP endpoint entirely (see FINDING-02) and rely solely on the Quartz scheduler.

---

### FINDING-02 — CRITICAL: Duplicate / Conflicting Trigger — HTTP Endpoint Bypasses Scheduled Job Design

**Severity:** CRITICAL
**File:** `src/main/java/com/action/CalibrationAction.java`, lines 18-19
**Also:** `src/main/java/com/calibration/CalibrationJobScheduler.java`, lines 16-29

**Description:**
The calibration process is designed as an automated scheduled job (`CalibrationJobScheduler` registers a Quartz cron trigger `"0 0 * * * ?"` — every hour on the hour). The existence of a public HTTP endpoint that triggers the identical job creates an unintended manual trigger surface. An attacker (or misconfigured client) can fire calibration runs at arbitrary frequency, causing:

1. Repeated `UPDATE unit` writes mid-calibration cycle, potentially corrupting in-progress calibration data (race condition with the scheduled job — see FINDING-05).
2. Denial-of-service via database load: each request scans the full `unit` table and all associated impact records.

**Evidence:**

```java
// CalibrationJobScheduler.java — legitimate scheduled path
.withSchedule(cronSchedule("0 0 * * * ?"))  // hourly

// CalibrationAction.java — unrestricted HTTP-triggered path
CalibrationJob job = new CalibrationJob();
job.calibrateAllUnits();   // same code path, callable at will
```

**Recommendation:**
If the HTTP endpoint is genuinely needed for operational use (e.g., forced recalibration by a super-admin), restrict it to `ROLE_SYS_ADMIN` and add request-rate limiting or a mutex to prevent concurrent execution with the scheduled job. If it is not needed, delete the action and remove the struts-config mapping.

---

### FINDING-03 — CRITICAL: Insecure Direct Object Reference / Missing Tenant Isolation — Cross-Company Data Mutation

**Severity:** CRITICAL
**File:** `src/main/java/com/calibration/UnitCalibrationGetterInDatabase.java`, lines 20-28
**Also:** `src/main/java/com/calibration/UnitCalibrationEnderInDatabase.java`, lines 9-18

**Description:**
`getUnitsToCalibrate()` queries the `unit` table with no company-ID filter — it returns every unit across every tenant in the database that meets the calibration criteria. When invoked via the HTTP endpoint (triggered by any authenticated user), the caller's session `sessCompId` is never consulted. `endCalibration()` then writes `impact_threshold`, `alert_enabled`, and `calibration_date` back to those records without any tenancy scope. A user authenticated to Company A triggers recalibration of units owned by Company B, C, etc.

**Evidence:**

```java
// UnitCalibrationGetterInDatabase.java lines 20-28
String query = "SELECT id, reset_calibration_date, calibration_date, impact_threshold " +
        "FROM unit " +
        "WHERE impact_threshold = 0 " +
        "AND alert_enabled IS FALSE " +
        "AND reset_calibration_date IS NOT NULL";
// No WHERE company_id = ? clause
```

```java
// UnitCalibrationEnderInDatabase.java lines 10-13
String query = "UPDATE unit SET impact_threshold = ?, " +
        "alert_enabled = TRUE, " +
        "calibration_date = NOW() " +
        "WHERE id = ?";
// No company_id scoping on the UPDATE
```

**Recommendation:**
This finding applies to the Quartz-scheduled path as well as the HTTP path. The scheduled job's cross-tenant behaviour is likely intentional (system-level maintenance). The critical issue is that the HTTP endpoint allows any authenticated user to trigger it. The primary remediation is restricting the HTTP endpoint to `ROLE_SYS_ADMIN` only (see FINDING-01). As a defence-in-depth measure, the scheduled job's SQL queries should be reviewed to confirm that cross-tenant execution is an accepted architectural decision and documented accordingly.

---

### FINDING-04 — HIGH: CSRF — No Token Protection on State-Changing Endpoint

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, line 582-583
**Also:** `src/main/java/com/action/CalibrationAction.java`, line 14

**Description:**
The `/calibration.do` endpoint triggers a database write operation (UPDATE on the `unit` table) and accepts both GET and POST (PreFlightActionServlet routes both through `doGet`). There is no CSRF token in the struts-config mapping, no form bean, and no token validation in the action. An attacker can craft a page containing:

```html
<img src="https://target.example.com/calibration.do" />
```

or a JavaScript `fetch()` call that causes any authenticated browser session to trigger the full calibration run.

**Evidence:**
- `struts-config.xml` line 582: no `name` (form-bean), no `validate`, no token mechanism.
- `CalibrationAction.java` line 14: no `isTokenValid()` call (Struts 1 built-in CSRF mechanism).
- `PreFlightActionServlet.doPost()` line 94: delegates to `doGet()` — GET and POST are functionally identical.

**Recommendation:**
This is a structural gap noted for the entire application. For this specific action: if the endpoint is retained, bind it to a form bean and call `isTokenValid(request)` (Struts 1 `Action` method) at the start of `execute()`, returning an error forward if the token is absent or stale. Additionally, restrict the action to POST-only at the servlet filter level.

---

### FINDING-05 — HIGH: Race Condition / Missing Synchronisation — Concurrent Execution of Calibration

**Severity:** HIGH
**File:** `src/main/java/com/calibration/CalibrationJob.java`, lines 11-13 and 15-24
**Also:** `src/main/java/com/action/CalibrationAction.java`, lines 18-19

**Description:**
`CalibrationJob.execute()` (the Quartz path) dispatches `calibrateAllUnits()` to a new single-thread executor on every scheduled firing:

```java
Executors.newSingleThreadExecutor().execute(this::calibrateAllUnits);
```

The HTTP action path calls `job.calibrateAllUnits()` synchronously on the servlet thread. There is no mutex, lock, or guard preventing the scheduled job and an HTTP-triggered run from executing `calibrateAllUnits()` concurrently. Both paths read the same rows, compute thresholds, and issue `UPDATE unit SET impact_threshold = ?` — a classic check-then-act race condition. A concurrent run can overwrite a threshold value computed by the other thread with stale data.

**Evidence:**

```java
// Quartz path — CalibrationJob.java line 12
Executors.newSingleThreadExecutor().execute(this::calibrateAllUnits);

// HTTP path — CalibrationAction.java line 19 (synchronous, no locking)
job.calibrateAllUnits();
```

**Recommendation:**
Use a `java.util.concurrent.locks.ReentrantLock` or a database-level advisory lock to ensure only one calibration run executes at a time. Alternatively, remove the HTTP endpoint, eliminating the second trigger entirely.

---

### FINDING-06 — HIGH: Exception Silencing — SQL Exceptions Swallowed in Scheduled Path

**Severity:** HIGH
**File:** `src/main/java/com/calibration/CalibrationJob.java`, lines 21-23

**Description:**
The `calibrateAllUnits()` method catches `SQLException` and only calls `e.printStackTrace()`. There is no alerting, logging framework integration, or error propagation. A database failure during calibration will go unnoticed in production (stack traces to stderr are typically not monitored). The calibration run will silently fail, leaving units in an uncalibrated state with no operator notification.

**Evidence:**

```java
// CalibrationJob.java lines 21-23
} catch (SQLException e) {
    e.printStackTrace();   // no log4j/slf4j, no alerting, silent failure
}
```

**Recommendation:**
Replace `e.printStackTrace()` with a proper logging call (e.g., `log.error("Calibration job failed", e)`) using the application's existing log4j infrastructure and raise an operational alert.

---

### FINDING-07 — MEDIUM: Null Return from super.execute() — Undefined Navigation Behaviour

**Severity:** MEDIUM
**File:** `src/main/java/com/action/CalibrationAction.java`, line 20

**Description:**
`super.execute()` on `org.apache.struts.action.Action` returns `null`. The struts-config mapping declares no `<forward>` elements. Struts 1 interprets a `null` `ActionForward` return as "no navigation" — the response is left open with no content written. This can result in a blank HTTP 200 response to the client, or in some container configurations a `NullPointerException` propagated to the global exception handler, leaking stack trace information to the caller.

**Evidence:**

```java
// CalibrationAction.java line 20
return super.execute(mapping, form, request, response);
// Action.execute() base implementation returns null
```

```xml
<!-- struts-config.xml lines 582-583 — no forwards defined -->
<action path="/calibration" type="com.action.CalibrationAction">
</action>
```

**Recommendation:**
Define at least a `success` and `failure` forward in the struts-config mapping, and return an appropriate `ActionForward` from `execute()`. Do not delegate to `super.execute()`.

---

### FINDING-08 — LOW: Sensitive Configuration Data Exposed in Source — RuntimeConf.java

**Severity:** LOW
**File:** `src/main/java/com/util/RuntimeConf.java`, lines 8, 16, 58, 60

**Description:**
`RuntimeConf.java` contains hardcoded internal email addresses, an internal AWS EC2 hostname, an S3 bucket URL, and a database JNDI name. While not directly part of `CalibrationAction`, `CalibrationJob` is embedded in the same codebase and these values are visible to anyone with read access to the repository. The AWS EC2 URL (`http://ec2-52-5-205-104.compute-1.amazonaws.com/...`) is a plain HTTP endpoint indicating a potentially live infrastructure address.

**Evidence:**

```java
// RuntimeConf.java
public static String RECEIVER_EMAIL  = "hui@ciifm.com";
public static String debugEmailRecipet = "hui@collectiveintelligence.com.au";
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/";
public static String cloudImageURL = "https://s3.amazonaws.com/forkliftiq360/image/";
```

**Recommendation:**
Move all environment-specific values to externalised configuration (environment variables, a properties file excluded from version control, or a secrets manager). Do not commit infrastructure hostnames, email addresses, or cloud resource URLs to source control.

---

## 3. Categories with No Issues Found

**Input Validation:** No user-supplied input is accepted by this action (no form bean, no request parameters read). SQL injection via this action's own code is not possible. The underlying DAOs (`UnitCalibrationGetterInDatabase`, `UnitCalibrationEnderInDatabase`) use parameterised queries exclusively — no string concatenation is present in the SQL. NO ISSUES in this category.

**Session Handling:** No session attributes are read or written by `CalibrationAction`. The session is neither created nor invalidated. The 30-minute session timeout configured in `web.xml` applies normally. NO ISSUES in this category specific to session state manipulation.

**Data Exposure via Response:** The action writes no data to the HTTP response. No calibration results, unit IDs, threshold values, or other data are returned to the caller. NO ISSUES in this category.

---

## 4. Summary Table

| ID | Severity | Category | File | Line(s) |
|----|----------|----------|------|---------|
| FINDING-01 | CRITICAL | Authentication / Authorisation | `CalibrationAction.java` | 14-21 |
| FINDING-02 | CRITICAL | Unauthorised Trigger / DoS Surface | `CalibrationAction.java` | 18-19 |
| FINDING-03 | CRITICAL | IDOR / Tenant Isolation | `UnitCalibrationGetterInDatabase.java` | 20-28 |
| FINDING-04 | HIGH | CSRF | `struts-config.xml` | 582-583 |
| FINDING-05 | HIGH | Race Condition | `CalibrationJob.java` | 11-13, 15-24 |
| FINDING-06 | HIGH | Exception Silencing / Observability | `CalibrationJob.java` | 21-23 |
| FINDING-07 | MEDIUM | Undefined Navigation / Null Forward | `CalibrationAction.java` | 20 |
| FINDING-08 | LOW | Hardcoded Sensitive Configuration | `RuntimeConf.java` | 8, 16, 58, 60 |

**Finding Count by Severity:**

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 3 |
| MEDIUM | 1 |
| LOW | 1 |
| INFO | 0 |
| **Total** | **8** |
