# Pass 2 – Test Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A88
**Date:** 2026-02-26

## Files Audited
1. `src/main/java/com/quartz/DriverAccessRevokeJob.java`
2. `src/main/java/com/quartz/DriverAccessRevokeJobScheduler.java`
3. `src/main/java/com/quartz/TrainingExpiryDailyEmailJob.java`

**Test directory searched:** `src/test/java/`

---

## Reading Evidence

### 1. `DriverAccessRevokeJob.java`

**Class name:** `com.quartz.DriverAccessRevokeJob`
**Implements:** `org.quartz.Job`

**Fields:** None declared.

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public void execute(JobExecutionContext jobExecutionContext)` | 15 |
| `revokeDriverAccessOnTrainingExpiry` | `public void revokeDriverAccessOnTrainingExpiry()` | 19 |

**Structural observations:**
- `execute()` (line 15–17): Spawns a new single-threaded executor and submits `this::revokeDriverAccessOnTrainingExpiry` as a method reference. The executor is created via `Executors.newSingleThreadExecutor()` and is never shut down.
- `revokeDriverAccessOnTrainingExpiry()` (line 19–25): Calls the static method `DriverDAO.revokeDriverAccessOnTrainingExpiry()`. Catches `SQLException` and calls `e.printStackTrace()`. No logging, no rethrow, no return value.

---

### 2. `DriverAccessRevokeJobScheduler.java`

**Class name:** `com.quartz.DriverAccessRevokeJobScheduler`
**Implements:** `javax.servlet.ServletContextListener`
**Registered in:** `WEB-INF/web.xml` (line 37)

**Fields:** None declared.

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `contextInitialized` | `public void contextInitialized(ServletContextEvent servletContextEvent)` | 17 |
| `contextDestroyed` | `public void contextDestroyed(ServletContextEvent servletContextEvent)` | 38 |

**Structural observations:**
- `contextInitialized()` (line 17–35): Creates a `JobDetail` for `DriverAccessRevokeJob`, a `CronTrigger` with expression `"0 0 2 * * ?"` (daily at 02:00), calls `scheduler.scheduleJob()` and `scheduler.start()`. Catches `SchedulerException` and calls `e.printStackTrace()`.
- `contextDestroyed()` (line 38–40): Does not call `scheduler.shutdown()`. Instead, it instantiates a new `ServletException("Application Stopped")` and calls `.printStackTrace()` on it — a clear logic error. No scheduler lifecycle teardown occurs.

---

### 3. `TrainingExpiryDailyEmailJob.java`

**Class name:** `com.quartz.TrainingExpiryDailyEmailJob`
**Implements:** `org.quartz.Job`

**Fields:** None declared.

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public void execute(JobExecutionContext jobExecutionContext)` | 14 |
| `sendTrainingExpiryDailyEmail` | `public void sendTrainingExpiryDailyEmail()` | 18 |

**Structural observations:**
- `execute()` (line 14–16): Spawns a new single-threaded executor and submits `this::sendTrainingExpiryDailyEmail` as a method reference. The executor is never shut down.
- `sendTrainingExpiryDailyEmail()` (line 18–25): Instantiates `TrainingDAO traingDAO` (note typo in variable name `traingDAO`) and calls `traingDAO.sendTrainingExpiryDailyEmail()`. Catches `SQLException` and calls `e.printStackTrace()`. No logging at job level, no rethrow.

**Related scheduler file identified (not in audit scope but relevant context):**
`com.quartz.TrainingExpiryDailyEmailJobSchedueler` (note typo in class/file name: `Schedueler` instead of `Scheduler`) — registered in `web.xml` and uses cron `"0 0 1 * * ?"` (daily at 01:00). Its `contextDestroyed()` has the identical defect as `DriverAccessRevokeJobScheduler`: no `scheduler.shutdown()` call; prints a freshly created `ServletException` instead.

---

## Test Search Results

| Class Searched | Grep Result |
|----------------|-------------|
| `DriverAccessRevokeJob` | **No files found** |
| `DriverAccessRevokeJobScheduler` | **No files found** |
| `TrainingExpiryDailyEmailJob` | **No files found** |

**Test coverage for all three audited classes: 0%.**

---

## Findings

### DriverAccessRevokeJob

---

**A88-1 | Severity: CRITICAL | No test class exists for `DriverAccessRevokeJob`**

Zero test files reference `DriverAccessRevokeJob`. Neither `execute()` nor `revokeDriverAccessOnTrainingExpiry()` has any test coverage whatsoever. Both methods are completely untested in a class that performs destructive database operations (`DELETE FROM driver_unit`).

---

**A88-2 | Severity: CRITICAL | `execute()` is completely untested — Quartz job lifecycle entry point**

`execute(JobExecutionContext)` is the sole Quartz-mandated entry point for this job. It is never exercised by any test. There is no verification that the method reference `this::revokeDriverAccessOnTrainingExpiry` is submitted correctly to the executor, nor that execution actually proceeds. Because the executor runs on a separate thread, test coverage needs to account for asynchronous completion.

---

**A88-3 | Severity: CRITICAL | `revokeDriverAccessOnTrainingExpiry()` success path is untested**

The method calls `DriverDAO.revokeDriverAccessOnTrainingExpiry()` (a static method performing a `DELETE FROM driver_unit` for every expired training record). There is no test verifying:
- That the DAO method is invoked at all.
- That it is invoked exactly once per `execute()` call.
- That the database deletion affects the correct rows.

---

**A88-4 | Severity: HIGH | `SQLException` error path in `revokeDriverAccessOnTrainingExpiry()` is untested**

The `catch (SQLException e)` block on line 22 silently swallows the exception after printing the stack trace. There is no test confirming that a DAO-level `SQLException` does not propagate further, does not crash the thread, and does not leave partial state. Silent swallowing of a DB error during a bulk access-revocation operation is a data-integrity risk; a test should at minimum confirm observable behaviour on failure.

---

**A88-5 | Severity: HIGH | Executor thread leak is untested and unverified**

`execute()` creates a new `ExecutorService` via `Executors.newSingleThreadExecutor()` on every Quartz invocation and never calls `shutdown()` or `shutdownNow()`. Over time (daily job runs) this accumulates non-terminated threads. There is no test verifying that executor resources are released, nor any assertion that thread count remains bounded across repeated invocations.

---

**A88-6 | Severity: MEDIUM | No test for behaviour when `DriverDAO.revokeDriverAccessOnTrainingExpiry()` returns with zero expired records**

If `getALLExpiredTrainigs()` (called inside the static DAO method) returns an empty list, the job should complete silently without touching the database. There is no test confirming this no-op path.

---

**A88-7 | Severity: MEDIUM | Asynchronous execution in `execute()` is untested — race condition risk**

The method reference is dispatched to a background thread. The calling Quartz thread returns immediately. No test validates that the background task actually completes or that the `JobExecutionContext` is not required by the background task after the main thread discards it. Quartz may reuse or discard the context after `execute()` returns.

---

### DriverAccessRevokeJobScheduler

---

**A88-8 | Severity: CRITICAL | No test class exists for `DriverAccessRevokeJobScheduler`**

Zero test files reference `DriverAccessRevokeJobScheduler`. Both `contextInitialized()` and `contextDestroyed()` are completely untested. This scheduler is a registered `ServletContextListener` in `web.xml`; failures at startup will prevent the entire Quartz job from ever running.

---

**A88-9 | Severity: CRITICAL | `contextInitialized()` success path is untested**

There is no test verifying that:
- A `JobDetail` is built with the correct identity (`"driverAccessRevokeJob"`, `"driverAccessRevoke"`).
- A `CronTrigger` is built with the correct cron expression `"0 0 2 * * ?"`.
- `scheduler.scheduleJob()` is called with matching job and trigger.
- `scheduler.start()` is called to activate the scheduler.
- The correct `Job` class (`DriverAccessRevokeJob.class`) is bound to the `JobDetail`.

---

**A88-10 | Severity: CRITICAL | `contextDestroyed()` does not shut down the scheduler — defect is untested**

`contextDestroyed()` (line 38–40) instantiates `new ServletException("Application Stopped")` and calls `printStackTrace()` on it. It does **not** retrieve the running scheduler and call `scheduler.shutdown()`. This is a defect: on application shutdown the Quartz scheduler thread pool is not stopped. There is no test exposing this behaviour, meaning the defect has no automated regression protection.

---

**A88-11 | Severity: HIGH | `SchedulerException` error path in `contextInitialized()` is untested**

The `catch (SchedulerException e)` block on line 32 silently swallows the exception. If the scheduler factory fails (e.g., due to a missing `quartz.properties`, a duplicate job identity, or a Quartz version conflict), the job is silently not scheduled and no error surfaces. There is no test simulating a `SchedulerException` to confirm observable failure behaviour.

---

**A88-12 | Severity: HIGH | Cron expression correctness for `DriverAccessRevokeJobScheduler` is untested**

The cron expression `"0 0 2 * * ?"` is hardcoded. There is no test validating that this expression fires at the intended time (02:00 AM daily) and not at any unintended time. An expression typo would cause the job to never fire or fire at the wrong time.

---

**A88-13 | Severity: MEDIUM | Job/trigger group name consistency is untested**

The `JobDetail` uses group `"driverAccessRevoke"` and the trigger's `forJob()` call references the same group, but no test verifies that these strings are self-consistent and would not cause a Quartz `JobPersistenceException` at runtime. A mismatch would silently fail into the swallowed `SchedulerException`.

---

**A88-14 | Severity: MEDIUM | `contextDestroyed()` misuse of `ServletException` for logging is untested and is a design defect**

Creating `new ServletException("Application Stopped")` solely to call `.printStackTrace()` is not a valid shutdown mechanism. No test verifies that application stop is signalled correctly, that the scheduler stops, or that in-progress job executions are allowed to complete before context destruction finishes.

---

### TrainingExpiryDailyEmailJob

---

**A88-15 | Severity: CRITICAL | No test class exists for `TrainingExpiryDailyEmailJob`**

Zero test files reference `TrainingExpiryDailyEmailJob`. Neither `execute()` nor `sendTrainingExpiryDailyEmail()` has any test coverage. This job sends emails to potentially all company administrators for drivers with expired training — a high-impact, externally visible operation.

---

**A88-16 | Severity: CRITICAL | `execute()` is completely untested — Quartz job lifecycle entry point**

`execute(JobExecutionContext)` is the Quartz entry point and is entirely without test coverage. There is no test verifying that the method reference `this::sendTrainingExpiryDailyEmail` is correctly submitted to the executor.

---

**A88-17 | Severity: CRITICAL | `sendTrainingExpiryDailyEmail()` success path is untested**

The method creates a new `TrainingDAO` instance and calls `sendTrainingExpiryDailyEmail()`. No test verifies:
- That `TrainingDAO` is instantiated.
- That `sendTrainingExpiryDailyEmail()` is called on the instance.
- That emails are sent to the correct recipients.
- That the correct email subject and content are generated.

---

**A88-18 | Severity: HIGH | `SQLException` error path in `sendTrainingExpiryDailyEmail()` is untested**

The `catch (SQLException e)` block on line 23 silently swallows the exception via `e.printStackTrace()`. If the database is unreachable at the time the job runs, no emails are sent and no alert is raised. There is no test confirming this silent-failure behaviour, nor verifying that partial email sends do not occur when a `SQLException` is raised mid-iteration (the iteration occurs inside `TrainingDAO`, but the contract here relies on the DAO's own exception propagation).

---

**A88-19 | Severity: HIGH | Executor thread leak is untested and unverified**

Identical to finding A88-5. `execute()` creates a new `ExecutorService` on every invocation and never shuts it down. For a daily job this accumulates abandoned thread-pool threads. There is no test.

---

**A88-20 | Severity: HIGH | Variable name typo `traingDAO` masks refactoring risk**

Line 20: `TrainingDAO traingDAO = new TrainingDAO();` — the variable is named `traingDAO` (missing 'i'). While functionally harmless now, this is an indicator of absent code review and absent tests that would have caught dead-variable or naming issues via static analysis integration. It is reported here as an indicator of test-process absence rather than a runtime defect.

---

**A88-21 | Severity: MEDIUM | Asynchronous execution in `execute()` is untested — same race condition risk as A88-7**

The email-sending task runs on a background thread. The Quartz thread returns from `execute()` immediately. No test validates task completion, thread safety of the `TrainingDAO` instance, or that the `JobExecutionContext` is not referenced after main-thread return.

---

**A88-22 | Severity: MEDIUM | No test for empty-list path in `sendTrainingExpiryDailyEmail()`**

If `DriverDAO.getInstance().getExpiredTrainigsComp()` returns an empty list (no companies with expired training today), the `forEach` lambda in `TrainingDAO.sendTrainingExpiryDailyEmail()` is never entered and no emails are sent. There is no test verifying this is the correct no-op behaviour.

---

**A88-23 | Severity: MEDIUM | Timezone-conditional email content ("training" vs "licence") is untested**

Inside `TrainingDAO.sendTrainingExpiryDailyEmail()`, the content string switches between `"training"` (for `US/` or `Canada/` timezones) and `"licence"` (all other timezones) based on `UserCompRelBean.getTimezone()`. There is no test exercising either branch, meaning both the US/Canada path and the international path are uncovered. A regression here would cause incorrect email content to be sent to users.

---

**A88-24 | Severity: MEDIUM | `AddressException` and `MessagingException` paths inside `TrainingDAO.sendTrainingExpiryDailyEmail()` are untested**

The lambda inside `sendTrainingExpiryDailyEmail()` (in `TrainingDAO`) catches `AddressException` and `MessagingException` separately and swallows each silently. A test at the `TrainingExpiryDailyEmailJob` level calling through to the DAO would expose whether these paths are reachable and what the observable effects are when `Util.sendMail()` fails.

---

**A88-25 | Severity: LOW | No integration-level test for the full daily email job pipeline**

There is no integration or end-to-end test covering the chain: `TrainingExpiryDailyEmailJob.execute()` → background thread → `TrainingDAO.sendTrainingExpiryDailyEmail()` → `DriverDAO.getExpiredTrainigsComp()` → `CompanyDAO.getUserAlert()` → `Util.sendMail()`. Without such a test, any breakage in the wiring between these components would only be detected in production.

---

**A88-26 | Severity: LOW | No test verifying that `TrainingExpiryDailyEmailJob` and `DriverAccessRevokeJob` do not interfere with each other when both run at adjacent scheduled times**

Both jobs are scheduled to run nightly (01:00 and 02:00). `TrainingExpiryDailyEmailJob` sends email notifications about expiring drivers; `DriverAccessRevokeJob` then revokes their access one hour later. There is no test verifying ordering assumptions or that the email job completes before the revoke job begins deleting `driver_unit` records.

---

## Coverage Summary

| Class | Methods | Tested Methods | Coverage |
|-------|---------|----------------|----------|
| `DriverAccessRevokeJob` | 2 | 0 | 0% |
| `DriverAccessRevokeJobScheduler` | 2 | 0 | 0% |
| `TrainingExpiryDailyEmailJob` | 2 | 0 | 0% |
| **Total** | **6** | **0** | **0%** |

---

## Finding Severity Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 8 |
| HIGH | 7 |
| MEDIUM | 7 |
| LOW | 4 |
| **Total** | **26** |
