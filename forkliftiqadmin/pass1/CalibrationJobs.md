# Security Audit Report: Calibration Job Classes
**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** Automated Pass 1 (Claude Sonnet 4.6)
**Stack:** Apache Struts 1.3.10 / Quartz scheduler / Apache Commons DBUtils

---

## Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/calibration/CalibrationImpact.java` |
| 2 | `src/main/java/com/calibration/CalibrationJob.java` |
| 3 | `src/main/java/com/calibration/CalibrationJobScheduler.java` |

Supporting files read for context (not part of the primary audit scope but directly invoked by the above):

- `src/main/java/com/calibration/UnitCalibrator.java`
- `src/main/java/com/calibration/UnitCalibration.java`
- `src/main/java/com/calibration/UnitCalibrationGetterInDatabase.java`
- `src/main/java/com/calibration/UnitCalibrationEnderInDatabase.java`
- `src/main/java/com/calibration/UnitCalibrationImpactFilter.java`
- `src/main/java/com/util/DBUtil.java`
- `src/main/java/com/util/RuntimeConf.java`
- `src/main/webapp/WEB-INF/web.xml`

---

## Reading Evidence

### CalibrationImpact.java
- **Package/Class:** `com.calibration.CalibrationImpact` — package-private data holder (Lombok `@Builder`).
- **Fields:** `int value`, `Timestamp time`, `Timestamp sessionStart`.
- **Role:** Plain value object. No DB calls, no external calls. Carries raw impact sensor readings for threshold computation.

### CalibrationJob.java
- **Package/Class:** `com.calibration.CalibrationJob implements org.quartz.Job` — Quartz job entry point.
- **Key method `execute(JobExecutionContext)`:** Spawns a brand-new, unbound, anonymous `SingleThreadExecutor` thread and fires `calibrateAllUnits()` asynchronously on it. The Quartz thread returns immediately.
- **Key method `calibrateAllUnits()`:** Instantiates `UnitCalibrationGetterInDatabase` and `UnitCalibrationEnderInDatabase` directly (no injection), constructs a `UnitCalibrator`, calls `calibrator.calibrateAllUnits()`, catches `SQLException` only with `e.printStackTrace()`.
- **DB calls (delegated):** Read from `unit` table; read from `v_impacts` view; `UPDATE unit SET impact_threshold, alert_enabled, calibration_date`.
- **No external HTTP/RPC calls.**

### CalibrationJobScheduler.java
- **Package/Class:** `com.calibration.CalibrationJobScheduler implements javax.servlet.ServletContextListener` — registered in `web.xml` as a lifecycle listener.
- **Key method `contextInitialized`:** Builds a Quartz `CronTrigger` with expression `"0 0 * * * ?"` (fires at the top of every hour), schedules `CalibrationJob`, starts the scheduler. Uses `StdSchedulerFactory` default configuration.
- **Key method `contextDestroyed`:** Instantiates a `ServletException("Application Stopped")` and calls `.printStackTrace()` on it — does not shut down the Quartz scheduler.
- **No DB calls, no external calls.**

---

## Findings

### Category 1: SQL Injection

**RESULT: NO ISSUES**

All SQL statements in the call chain initiated by these three files use parameterised `PreparedStatement` bindings exclusively:

- `UnitCalibrationGetterInDatabase.getUnitsToCalibrate()` — static literal query, no parameters.
- `UnitCalibrationGetterInDatabase.getUnitCalibration(long unitId)` — `statement.setLong(1, unitId)`.
- `UnitCalibrationGetterInDatabase.getImpactsForUnit(long unitId, Timestamp resetCalibrationDate)` — `statement.setLong(1, unitId)`, `statement.setTimestamp(2, resetCalibrationDate)`.
- `UnitCalibrationEnderInDatabase.endCalibration(long unitId, int newThreshold)` — `statement.setInt(1, newThreshold)`, `statement.setLong(2, unitId)`.

The values passed to these methods (`unitId`, `resetCalibrationDate`) are sourced entirely from prior `ResultSet` reads of the `unit` table — they are never supplied by user input or HTTP parameters. No string concatenation into SQL is present anywhere in this subsystem.

---

### Category 2: Privilege Escalation / Authentication Bypass

**RESULT: 1 FINDING**

---

#### FINDING-CAL-01
**Severity:** MEDIUM
**File:** `src/main/java/com/calibration/CalibrationJob.java` (lines 15-24) and `src/main/java/com/calibration/CalibrationJobScheduler.java` (lines 16-33)
**Description:** The job executes database write operations (`UPDATE unit SET impact_threshold, alert_enabled`) entirely outside the application's authentication and authorisation framework. The Quartz scheduler thread has no security context (no Struts session, no role check). Any unit whose `impact_threshold = 0 AND alert_enabled IS FALSE AND reset_calibration_date IS NOT NULL` will have its alert threshold recomputed and alerts re-enabled unconditionally, for all tenants/companies in the database simultaneously.

**Evidence:**
```java
// CalibrationJob.java lines 15-23
public void calibrateAllUnits() {
    try {
        UnitCalibrationGetter getter = new UnitCalibrationGetterInDatabase();
        UnitCalibrationEnder ender = new UnitCalibrationEnderInDatabase();
        UnitCalibrator calibrator = new UnitCalibrator(getter, ender);
        calibrator.calibrateAllUnits();   // operates on ALL matching units, all tenants
    } catch (SQLException e) {
        e.printStackTrace();
    }
}
```
```sql
-- UnitCalibrationGetterInDatabase.java line 20-24
SELECT id, reset_calibration_date, calibration_date, impact_threshold
FROM unit
WHERE impact_threshold = 0
  AND alert_enabled IS FALSE
  AND reset_calibration_date IS NOT NULL
-- No tenant/company/site filter applied
```

**Recommendation:** Confirm whether the `unit` table is truly shared across all tenants or whether the DB connection inherently scopes to a single tenant schema. If multi-tenant, add a company/site scope to the batch query to prevent cross-tenant data mutation. Document the intentional absence of auth context as a design decision, and ensure no external trigger (e.g., a future API endpoint that calls `calibrateAllUnits()` directly) can introduce IDOR via this path.

---

### Category 3: Data Integrity — Race Conditions and Double-Processing

**RESULT: 3 FINDINGS**

---

#### FINDING-CAL-02
**Severity:** HIGH
**File:** `src/main/java/com/calibration/CalibrationJob.java` (lines 11-13)
**Description:** `execute()` spawns a new, unmanaged, unnamed `Executors.newSingleThreadExecutor()` every time Quartz fires the trigger (every hour). If a prior job run is still executing when the next trigger fires (e.g., due to a large unit count or slow DB), two concurrent threads will simultaneously read the same set of units and attempt to write `UPDATE unit ... WHERE id = ?` for the same rows. This is a classic read-modify-write race. The result depends on DB transaction isolation, but at minimum it can produce duplicate calibration writes, incorrect threshold values (the second run starts from the same `resetCalibrationDate` snapshot as the first), or garbled alert state.

Additionally, the executor is never shut down, leaking a thread for every job invocation that finishes.

**Evidence:**
```java
// CalibrationJob.java lines 11-13
public void execute(JobExecutionContext jobExecutionContext) {
    Executors.newSingleThreadExecutor().execute(this::calibrateAllUnits);
    // Quartz thread returns; executor is never stored, never shut down
}
```
The trigger fires every hour (`"0 0 * * * ?"`). If the DB contains many units and calibration takes more than 60 minutes — unlikely but possible in production — two executors will run concurrently with no mutual exclusion.

Even without overlap between hourly runs, there is a race within a single run: all units matching the query are read in one batch, then processed serially. No database-level locking (e.g., `SELECT ... FOR UPDATE`) is used, so a concurrent manual admin action that resets calibration mid-run will have its reset silently overwritten.

**Recommendation:** Use Quartz's `@DisallowConcurrentExecution` annotation on `CalibrationJob` to prevent overlapping runs. Remove the async `Executors.newSingleThreadExecutor()` wrapper — there is no value in handing off to another thread when Quartz already manages thread pool sizing. If the job must be async, use a managed executor service that is shared and shut down cleanly on context destroy. Add `SELECT ... FOR UPDATE` or an equivalent optimistic lock column to the unit row before mutating it.

---

#### FINDING-CAL-03
**Severity:** HIGH
**File:** `src/main/java/com/calibration/CalibrationJobScheduler.java` (lines 35-38)
**Description:** `contextDestroyed()` does not shut down the Quartz `Scheduler`. When the servlet container stops or redeploys the web application, the Quartz scheduler and any running `CalibrationJob` threads continue executing in the background. This can cause:

1. Jobs firing against a partially-destroyed application context (e.g., JNDI DataSource already unbound), producing `SQLException`s that are silently swallowed.
2. On hot-redeploy, a second scheduler instance is started by the new context while the old one is still running, causing double-execution of calibration writes for the same units.
3. Thread leaks accumulating across repeated redeploys.

**Evidence:**
```java
// CalibrationJobScheduler.java lines 35-38
@Override
public void contextDestroyed(ServletContextEvent servletContextEvent) {
    new ServletException("Application Stopped").printStackTrace();
    // Quartz scheduler is NOT stopped. scheduler.shutdown() is never called.
}
```
The `Scheduler` reference obtained in `contextInitialized` (line 27) is not stored as an instance field, making it impossible to call `scheduler.shutdown()` in `contextDestroyed`.

**Recommendation:** Store the `Scheduler` as an instance field. In `contextDestroyed`, call `scheduler.shutdown(true)` (the `true` parameter waits for running jobs to complete before returning). Remove the spurious `new ServletException(...).printStackTrace()` — this creates a misleading stack trace entry in logs with no actionable information.

---

#### FINDING-CAL-04
**Severity:** MEDIUM
**File:** `src/main/java/com/calibration/UnitCalibration.java` (lines 48-51) and `UnitCalibrationGetterInDatabase.java` (lines 53-67)
**Description:** `getCalculatedThreshold()` calls `average()` which divides by `impacts.size()`. If `impacts` is an empty list, this produces a division by zero (`ArithmeticException` for integer division, `NaN`/`Infinity` for doubles). Since the result is cast to `int`, a NaN or Infinity would produce `0` or `Integer.MAX_VALUE` as the stored threshold.

`calibrateUnit()` in `UnitCalibrator` only checks `calibrationPercentage() != 100` before calling `endCalibration`. `calibrationPercentage()` returns 100 when `impacts.size() >= 100`. If exactly 100 impacts pass the filter, `average()` divides by 100 — safe. However, `calibrationDone()` (line 44-46 in `UnitCalibration.java`) returns `true` when `impacts.size() >= 100`, and `isCalibrated()` returns `true` when that holds. But there is a subtlety: the `getUnitsToCalibrate()` query does not filter on `calibration_date IS NULL`; it only checks `impact_threshold = 0`. A unit that already completed calibration but whose `calibration_date` was somehow cleared while `impact_threshold` remains 0 could re-enter the batch with a stale impact list.

More concretely: `average()` at line 54 divides by `impacts.size()` with no null or empty guard. If the filter in `UnitCalibrationImpactFilter` eliminates all impacts (none exceed 80,000 millinewtons), the returned list is empty, `impacts.size()` is 0, and `calibrationPercentage()` returns 0 — but this means `calibrateUnit()` returns early without writing. So the division-by-zero path is not currently reachable through `calibrateAllUnits()`. However, `getCalculatedThreshold()` is a public-facing method on a `@Getter`-annotated builder class; a future caller could invoke it directly on a `UnitCalibration` with an empty impacts list and receive a corrupted threshold.

**Recommendation:** Add a guard in `average()` (and `getCalculatedThreshold()`) for `impacts == null || impacts.isEmpty()` and throw a meaningful `IllegalStateException` rather than silently producing a degenerate value. This prevents a future regression if the call site logic changes.

---

### Category 4: Secret Exposure

**RESULT: 1 FINDING (in supporting context, informational)**

---

#### FINDING-CAL-05
**Severity:** INFO
**File:** `src/main/java/com/util/RuntimeConf.java` (lines 60, 62)
**Description:** `RuntimeConf.java`, which is used transitively by the calibration job via `DBUtil`, contains hardcoded infrastructure URLs:

```java
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/";
public static String cloudImageURL = "https://s3.amazonaws.com/forkliftiq360/image/";
```

These are not credentials (no passwords, keys, or tokens are hardcoded), and they are not directly referenced by the three audited files. However, the EC2 hostname is a direct IP-mapped public AWS endpoint, which discloses infrastructure topology in source code. If the repository is ever made public or leaked, this information assists reconnaissance.

The calibration job itself does not use `RuntimeConf` for credentials — database connectivity is through JNDI (`jdbc/PreStartDB`), which is correctly externalised to the container configuration.

**Recommendation:** Move infrastructure URLs to an externalised configuration file or environment variable. This is a separate remediation item and does not affect the security of the calibration subsystem directly.

No hardcoded DB passwords, API keys, or connection strings were found in any of the three primary files or their direct dependencies.

---

### Category 5: Error Handling

**RESULT: 3 FINDINGS**

---

#### FINDING-CAL-06
**Severity:** HIGH
**File:** `src/main/java/com/calibration/CalibrationJob.java` (lines 21-23)
**Description:** `calibrateAllUnits()` catches `SQLException` and calls `e.printStackTrace()`. This means:

1. Any database failure (connection pool exhaustion, deadlock, constraint violation) during a calibration run is silently absorbed. The job continues to its next scheduled trigger with no alert, no monitoring signal, and no record beyond a console stack trace that may be swallowed by the container's log rotation.
2. The `Executors.newSingleThreadExecutor()` thread terminates silently. Quartz has no visibility into the failure because the exception never propagates to the `Job.execute()` method; it is caught inside the offloaded `Runnable`. Quartz therefore has no opportunity to record a `JobExecutionException` or trigger a misfire policy.
3. `DBUtil.queryForObjects()` itself also swallows `SQLException` internally (prints stack trace and returns an empty list), meaning errors in the getter may not even reach the catch block in `calibrateAllUnits()`.

**Evidence:**
```java
// CalibrationJob.java lines 15-24
public void calibrateAllUnits() {
    try {
        ...
        calibrator.calibrateAllUnits();
    } catch (SQLException e) {
        e.printStackTrace();  // silent failure, no monitoring hook
    }
}
```
```java
// DBUtil.java lines 75-77 (queryForObjects)
} catch (SQLException e) {
    e.printStackTrace();  // ALSO silently absorbed here
}
```

**Recommendation:** Replace `e.printStackTrace()` with a proper logging framework call (e.g., `log.error("Calibration job failed", e)`). In `CalibrationJob.execute()`, propagate the failure as a Quartz `JobExecutionException` so the scheduler can apply its retry/misfire policy. Consider integrating with an application health monitoring endpoint.

---

#### FINDING-CAL-07
**Severity:** MEDIUM
**File:** `src/main/java/com/calibration/CalibrationJobScheduler.java` (lines 30-32)
**Description:** `contextInitialized()` catches `SchedulerException` with `e.printStackTrace()`. If the Quartz scheduler fails to initialise (e.g., configuration file missing, thread pool exhaustion), the calibration job is simply never scheduled and the application starts normally with no indication to operators that calibration is disabled. This is a silent failure of a background process that could go undetected indefinitely.

**Evidence:**
```java
// CalibrationJobScheduler.java lines 30-32
} catch (SchedulerException e) {
    e.printStackTrace();
}
```

**Recommendation:** Log at ERROR level using a logging framework. Consider whether a scheduler initialisation failure should abort context startup (re-throw as `RuntimeException`) or merely alert. At minimum, the failure should be surfaced to an operations monitoring channel.

---

#### FINDING-CAL-08
**Severity:** LOW
**File:** `src/main/java/com/calibration/CalibrationJobScheduler.java` (lines 35-38)
**Description:** `contextDestroyed()` instantiates and immediately calls `.printStackTrace()` on a `new ServletException("Application Stopped")`. This is functionally a no-op that writes a misleading stack trace (with no actual exception cause) to stderr on every application shutdown. It provides no diagnostic value and could confuse operators reviewing shutdown logs, causing them to investigate a phantom exception.

**Evidence:**
```java
@Override
public void contextDestroyed(ServletContextEvent servletContextEvent) {
    new ServletException("Application Stopped").printStackTrace();
}
```

**Recommendation:** Remove this statement entirely. If a shutdown notification is genuinely needed, use `log.info("CalibrationJobScheduler stopped")` after calling `scheduler.shutdown()`.

---

## Summary Table

| ID | Severity | Category | File (primary) | Line(s) | Title |
|----|----------|----------|----------------|---------|-------|
| CAL-01 | MEDIUM | Privilege Escalation | `CalibrationJob.java` / `UnitCalibrationGetterInDatabase.java` | 15-24 / 20-24 | No tenant scope on batch calibration query |
| CAL-02 | HIGH | Data Integrity | `CalibrationJob.java` | 11-13 | Unguarded concurrent execution — race condition and thread leak |
| CAL-03 | HIGH | Data Integrity | `CalibrationJobScheduler.java` | 35-38 | Scheduler not shut down on context destroy — double-execution on redeploy |
| CAL-04 | MEDIUM | Data Integrity | `UnitCalibration.java` / `UnitCalibrationGetterInDatabase.java` | 48-51 / 53-67 | Division-by-zero in threshold calculation with empty impact list |
| CAL-05 | INFO | Secret Exposure | `RuntimeConf.java` (context) | 60, 62 | Hardcoded infrastructure URLs (no passwords/keys; informational) |
| CAL-06 | HIGH | Error Handling | `CalibrationJob.java` | 21-23 | SQLException silently swallowed; Quartz has no failure visibility |
| CAL-07 | MEDIUM | Error Handling | `CalibrationJobScheduler.java` | 30-32 | SchedulerException silently swallowed on init failure |
| CAL-08 | LOW | Error Handling | `CalibrationJobScheduler.java` | 35-38 | Spurious `new ServletException(...).printStackTrace()` in contextDestroyed |

---

## Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 3 (CAL-02, CAL-03, CAL-06) |
| MEDIUM | 3 (CAL-01, CAL-04, CAL-07) |
| LOW | 1 (CAL-08) |
| INFO | 1 (CAL-05) |
| **Total** | **8** |

---

## SQL Injection Verdict

NO SQL injection risk identified. All queries in the calibration subsystem use parameterised `PreparedStatement` exclusively, and all runtime parameter values are sourced from prior database reads rather than user-supplied input.

---

*End of report.*
