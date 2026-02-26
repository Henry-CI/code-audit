# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A89
**Report Date:** 2026-02-26

## Source Files Audited

1. `src/main/java/com/quartz/TrainingExpiryDailyEmailJobSchedueler.java`
2. `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJob.java`
3. `src/main/java/com/quartz/TrainingExpiryWeeklyEmailJobScheduler.java`

**Test directory searched:** `src/test/java/`

---

## Reading Evidence

### File 1: TrainingExpiryDailyEmailJobSchedueler

**Class name:** `TrainingExpiryDailyEmailJobSchedueler`
**Implements:** `ServletContextListener`
**Package:** `com.quartz`

**Fields:** None declared (no instance fields).

**Methods:**

| Method | Line |
|--------|------|
| `contextInitialized(ServletContextEvent servletContextEvent)` | 20 |
| `contextDestroyed(ServletContextEvent servletContextEvent)` | 41 |

**Key implementation details:**
- `contextInitialized`: builds a `JobDetail` for `TrainingExpiryDailyEmailJob`, builds a `CronTrigger` with cron expression `"0 0 1 * * ?"` (daily at 1:00am), obtains a `Scheduler` via `new StdSchedulerFactory()`, calls `scheduleJob(...)` and `scheduler.start()`. `SchedulerException` is caught and only `e.printStackTrace()` is called (line 36).
- `contextDestroyed`: constructs `new ServletException("Application Stopped")` and calls `.printStackTrace()` on it. It does NOT shut down the scheduler (line 41-43).

---

### File 2: TrainingExpiryWeeklyEmailJob

**Class name:** `TrainingExpiryWeeklyEmailJob`
**Implements:** `org.quartz.Job`
**Package:** `com.quartz`

**Fields:** None declared (no instance fields).

**Methods:**

| Method | Line |
|--------|------|
| `execute(JobExecutionContext jobExecutionContext)` | 14 |
| `sendTrainingExpiryWeeklyEmail()` | 18 |

**Key implementation details:**
- `execute`: creates a new single-thread executor via `Executors.newSingleThreadExecutor()` and submits `this::sendTrainingExpiryWeeklyEmail` as a method reference. The executor is never shut down.
- `sendTrainingExpiryWeeklyEmail`: instantiates `TrainingDAO` directly (hard-coded `new TrainingDAO()`), calls `traingDAO.sendTrainingExpiryWeeklyEmail()`. Catches `SQLException` and calls `e.printStackTrace()` only. Note: local variable name is misspelled `traingDAO`.

---

### File 3: TrainingExpiryWeeklyEmailJobScheduler

**Class name:** `TrainingExpiryWeeklyEmailJobScheduler`
**Implements:** `ServletContextListener`
**Package:** `com.quartz`

**Fields:** None declared (no instance fields).

**Methods:**

| Method | Line |
|--------|------|
| `contextInitialized(ServletContextEvent servletContextEvent)` | 20 |
| `contextDestroyed(ServletContextEvent servletContextEvent)` | 41 |

**Key implementation details:**
- `contextInitialized`: builds a `JobDetail` for `TrainingExpiryWeeklyEmailJob`, builds a `CronTrigger` with cron expression `"0 0 3 ? * SUN"` (every Sunday at 3:00am), obtains a `Scheduler` via `new StdSchedulerFactory()`, calls `scheduleJob(...)` and `scheduler.start()`. `SchedulerException` is caught and only `e.printStackTrace()` is called (line 35).
- `contextDestroyed`: constructs `new ServletException("Application Stopped")` and calls `.printStackTrace()` on it. It does NOT shut down the scheduler (line 41-43).

---

## Test Coverage Search Results

Grep for `TrainingExpiryDailyEmailJobSchedueler` in `src/test/java/`: **No files found.**
Grep for `TrainingExpiryWeeklyEmailJob` in `src/test/java/`: **No files found.**
Grep for `TrainingExpiryWeeklyEmailJobScheduler` in `src/test/java/`: **No files found.**

The four test files present in the project are:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these files reference any of the three audited classes.

---

## Findings

### TrainingExpiryDailyEmailJobSchedueler

**A89-1 | Severity: CRITICAL | No test class exists for TrainingExpiryDailyEmailJobSchedueler**
There is zero test coverage for this class. Neither `contextInitialized` nor `contextDestroyed` is exercised by any test. All logic within the class — job construction, trigger configuration, scheduler creation, scheduler startup, and exception handling — is entirely untested.

**A89-2 | Severity: CRITICAL | contextInitialized: SchedulerException path is silent and untested**
The `catch (SchedulerException e)` block at line 35-37 only calls `e.printStackTrace()`. There is no test that verifies this path is reached when the scheduler fails, no re-throw, no logging to a proper framework, and no notification mechanism. A scheduler failure at startup would be silently swallowed.

**A89-3 | Severity: HIGH | contextInitialized: scheduler startup is never verified by a test**
No test verifies that the scheduler is actually started (`scheduler.start()` is called), that `scheduleJob` receives the correct `JobDetail` and `CronTrigger`, or that the correct job class (`TrainingExpiryDailyEmailJob.class`) is registered.

**A89-4 | Severity: HIGH | contextInitialized: cron expression correctness is not tested**
The cron expression `"0 0 1 * * ?"` (daily at 1:00am) is hardcoded but never validated by a test. A malformed expression would produce a `SchedulerException` that is silently swallowed.

**A89-5 | Severity: HIGH | contextInitialized: trigger group name mismatch is untested**
The trigger is created with group `"driverAccessRevoke"` (line 26) but the job belongs to group `"trainingExpiryDailyEmail"` (line 23). The trigger group name appears to be a copy-paste error from a different scheduler. No test catches this logical inconsistency.

**A89-6 | Severity: HIGH | contextDestroyed: scheduler is never shut down**
`contextDestroyed` does not call `scheduler.shutdown()`. When the servlet context is destroyed, the Quartz scheduler continues running, which can cause thread leaks, duplicate job executions, and classloader issues during redeployment. No test verifies teardown behaviour.

**A89-7 | Severity: HIGH | contextDestroyed: uses ServletException as a logging mechanism**
`contextDestroyed` instantiates `new ServletException("Application Stopped")` and calls `.printStackTrace()` on it (line 42). This is not a logging approach; it is a misuse of exception construction for side-effect output only. The exception is not thrown and nothing meaningful happens. No test asserts any expected behaviour of `contextDestroyed`.

**A89-8 | Severity: MEDIUM | contextInitialized: StdSchedulerFactory is instantiated inline, preventing dependency injection and mocking**
`new StdSchedulerFactory()` is created directly inside the method (line 31). This makes it impossible to inject a mock scheduler in tests without bytecode manipulation. No test exercises this path at all.

**A89-9 | Severity: MEDIUM | contextInitialized: scheduler instance is not retained as a field**
The `Scheduler` reference obtained from the factory is a local variable. It is therefore unreachable from `contextDestroyed`, making a proper shutdown impossible. No test exercises or detects this design flaw.

**A89-10 | Severity: LOW | Class name contains a typo ("Schedueler" instead of "Scheduler")**
The class name `TrainingExpiryDailyEmailJobSchedueler` is misspelled. This is not a test-coverage gap per se, but it is undetected by any test, code review gate, or naming convention check.

---

### TrainingExpiryWeeklyEmailJob

**A89-11 | Severity: CRITICAL | No test class exists for TrainingExpiryWeeklyEmailJob**
There is zero test coverage for this class. Neither `execute` nor `sendTrainingExpiryWeeklyEmail` is exercised by any test.

**A89-12 | Severity: CRITICAL | execute: asynchronous dispatch via Executors is never tested**
`execute` submits work to `Executors.newSingleThreadExecutor()` as a method reference (line 15). No test verifies that `sendTrainingExpiryWeeklyEmail` is actually called when `execute` is invoked, that the executor is used correctly, or that the asynchronous dispatch completes without error.

**A89-13 | Severity: CRITICAL | sendTrainingExpiryWeeklyEmail: SQLException catch block is silent and untested**
The `catch (SQLException e)` block at lines 22-24 only calls `e.printStackTrace()`. No test verifies behaviour when `TrainingDAO.sendTrainingExpiryWeeklyEmail()` throws a `SQLException`. Failures in email dispatch are silently swallowed.

**A89-14 | Severity: HIGH | sendTrainingExpiryWeeklyEmail: TrainingDAO is instantiated directly, preventing mocking**
`new TrainingDAO()` is created inline (line 20). This hard dependency makes it impossible to mock the DAO in unit tests without bytecode manipulation. The method cannot be tested in isolation.

**A89-15 | Severity: HIGH | execute: executor thread pool is never shut down**
`Executors.newSingleThreadExecutor()` creates an executor that is never shut down. Each invocation of `execute` leaks a thread pool. Under load or repeated invocations, this can exhaust thread resources. No test detects this resource leak.

**A89-16 | Severity: HIGH | execute: JobExecutionContext parameter is ignored and untested**
The `jobExecutionContext` parameter (line 14) is never used. No test verifies whether ignoring the context is intentional or whether context data (job data map, fire time, etc.) should be consumed.

**A89-17 | Severity: MEDIUM | sendTrainingExpiryWeeklyEmail: local variable name is misspelled ("traingDAO")**
The local variable at line 20 is named `traingDAO` instead of `trainingDAO`. This is a recurring pattern across the codebase and is undetected by any test or static analysis gate.

**A89-18 | Severity: MEDIUM | execute: no test for JobExecutionException wrapping**
The Quartz `Job` interface allows implementations to throw `JobExecutionException`. The `execute` method swallows all exceptions by design (the executor task has no error handler). No test verifies whether failures should propagate as `JobExecutionException`.

**A89-19 | Severity: LOW | No integration test for end-to-end weekly email dispatch**
There is no integration or smoke test that verifies the full chain: Quartz fires the job → `execute` dispatches asynchronously → `sendTrainingExpiryWeeklyEmail` calls the DAO → email is sent.

---

### TrainingExpiryWeeklyEmailJobScheduler

**A89-20 | Severity: CRITICAL | No test class exists for TrainingExpiryWeeklyEmailJobScheduler**
There is zero test coverage for this class. Neither `contextInitialized` nor `contextDestroyed` is exercised by any test.

**A89-21 | Severity: CRITICAL | contextInitialized: SchedulerException path is silent and untested**
The `catch (SchedulerException e)` block at lines 35-37 only calls `e.printStackTrace()`. A scheduler failure at startup is silently swallowed with no test verifying this behaviour.

**A89-22 | Severity: HIGH | contextInitialized: scheduler startup and job registration are never verified**
No test asserts that `scheduler.start()` is called, that `scheduleJob` receives the correct `JobDetail` and `CronTrigger`, or that `TrainingExpiryWeeklyEmailJob.class` is correctly registered.

**A89-23 | Severity: HIGH | contextInitialized: cron expression correctness is not tested**
The cron expression `"0 0 3 ? * SUN"` (every Sunday at 3:00am) is hardcoded but never validated by a test. A malformed expression would produce a silently swallowed `SchedulerException`.

**A89-24 | Severity: HIGH | contextInitialized: trigger group name mismatch is untested**
The trigger is created with group `"driverAccessRevoke"` (line 26) but the job belongs to group `"trainingExpiryWeeklyEmail"` (line 23). This appears to be the same copy-paste error present in `TrainingExpiryDailyEmailJobSchedueler`. No test catches this inconsistency.

**A89-25 | Severity: HIGH | contextDestroyed: scheduler is never shut down**
`contextDestroyed` does not call `scheduler.shutdown()`. The weekly Quartz scheduler continues running after servlet context destruction, risking thread leaks and duplicate job firing during redeployment. No test verifies teardown behaviour.

**A89-26 | Severity: HIGH | contextDestroyed: uses ServletException as a logging mechanism**
Identical anti-pattern to `TrainingExpiryDailyEmailJobSchedueler` (line 42): `new ServletException("Application Stopped").printStackTrace()`. No test asserts any expected behaviour of `contextDestroyed`.

**A89-27 | Severity: MEDIUM | contextInitialized: StdSchedulerFactory is instantiated inline, preventing mocking**
`new StdSchedulerFactory()` is created directly inside the method (line 31). No test exercises this path, and the design precludes straightforward unit testing with a mock scheduler.

**A89-28 | Severity: MEDIUM | contextInitialized: scheduler instance is not retained as a field**
As with the daily scheduler, the `Scheduler` reference is a local variable, making it unreachable from `contextDestroyed`. No test detects this design flaw.

---

## Coverage Gap Summary

| Class | Methods | Methods With Any Test | Coverage |
|---|---|---|---|
| TrainingExpiryDailyEmailJobSchedueler | 2 | 0 | 0% |
| TrainingExpiryWeeklyEmailJob | 2 | 0 | 0% |
| TrainingExpiryWeeklyEmailJobScheduler | 2 | 0 | 0% |
| **Total** | **6** | **0** | **0%** |

All three classes have 0% test coverage. There are no unit tests, no integration tests, and no lifecycle tests for any Quartz job or scheduler in the `com.quartz` package covering these files.

---

## Cross-Cutting Observations

**A89-29 | Severity: CRITICAL | Entire com.quartz package for training expiry jobs has 0% test coverage**
All six methods across the three audited classes are completely untested. The Quartz job lifecycle (schedule, trigger, execute, destroy) has no test verification whatsoever.

**A89-30 | Severity: HIGH | Both scheduler classes share identical structural defects with no test to detect regression**
`TrainingExpiryDailyEmailJobSchedueler` and `TrainingExpiryWeeklyEmailJobScheduler` are near-identical copies with the same bugs (wrong trigger group, no scheduler shutdown, exception swallowing, misuse of ServletException). The lack of tests means these defects propagate undetected across all scheduler implementations.

**A89-31 | Severity: HIGH | No test verifies that daily and weekly schedulers do not conflict at runtime**
Both schedulers use `new StdSchedulerFactory()` independently. Depending on Quartz configuration, this may share the same default scheduler instance. No test verifies isolation between the two scheduler registrations, and duplicate job key conflicts are possible.

**A89-32 | Severity: MEDIUM | No test for exception propagation from TrainingDAO into the job layer**
`TrainingDAO.sendTrainingExpiryDailyEmail()` and `TrainingDAO.sendTrainingExpiryWeeklyEmail()` both declare `throws SQLException`. The job classes catch only `SQLException`. No test verifies that other runtime exceptions (e.g., `NullPointerException`, `RuntimeException` from database connection pool exhaustion) propagate correctly or are handled.

**A89-33 | Severity: INFO | No test framework configuration for Quartz in-memory scheduler**
The project has no `quartz.properties` test configuration and no embedded/in-memory Quartz scheduler setup in the test suite. Adding tests for these classes would require either an in-memory scheduler configuration or Mockito/PowerMock for the `StdSchedulerFactory` dependency.
