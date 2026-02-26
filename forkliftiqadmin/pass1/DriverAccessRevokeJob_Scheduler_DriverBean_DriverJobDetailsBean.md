# Pass 1 Audit — DriverAccessRevokeJob / DriverAccessRevokeJobScheduler / DriverBean / DriverJobDetailsBean

**Files:**
- `src/main/java/com/quartz/DriverAccessRevokeJob.java`
- `src/main/java/com/quartz/DriverAccessRevokeJobScheduler.java`
- `src/main/java/com/bean/DriverBean.java`
- `src/main/java/com/bean/DriverJobDetailsBean.java`

**Date:** 2026-02-26

---

## Summary

This audit covers two Quartz scheduler components (`DriverAccessRevokeJob` and `DriverAccessRevokeJobScheduler`) and two bean classes (`DriverBean` and `DriverJobDetailsBean`). The Quartz job executes a daily 2 AM database operation that deletes `driver_unit` rows for drivers with expired training certifications, effectively revoking equipment access. The bean classes are used throughout the application as data-transfer objects; `DriverBean` is the core credential-bearing user record.

Significant findings include: a thread leak that compounds each time the job fires (HIGH), a missing scheduler shutdown that leaves Quartz threads running after container stop (HIGH), a Lombok `@Data`-generated `toString()` on a `Serializable` bean that carries plaintext password and access-token fields (HIGH), `DriverBean` being stored in the HTTP session while holding plaintext password data populated from the database (HIGH), a mismatched password assignment bug in `DriverDAO.updateGeneralUserInfo` that may send the wrong credential to Cognito (MEDIUM), a `contextDestroyed` implementation that creates and immediately discards an exception object (MEDIUM), and several lower-severity issues around error handling, raw types, and missing `@DisallowConcurrentExecution`.

---

## Findings

---

### HIGH: Thread Pool Leak — New Executor Created on Every Job Execution

**File:** `DriverAccessRevokeJob.java` (line 16)

**Description:**
`execute()` calls `Executors.newSingleThreadExecutor().execute(...)` without ever calling `shutdown()` or `shutdownNow()` on the returned `ExecutorService`. Each time Quartz fires the job a new single-thread executor is created and its internal thread is never reclaimed. Over time — across application restarts, redeployments, or if the cron schedule is ever changed to a higher frequency — unclosed executors accumulate in the JVM, preventing garbage collection of the associated threads, task queues, and class-loader references.

```java
// DriverAccessRevokeJob.java line 16
Executors.newSingleThreadExecutor().execute(this::revokeDriverAccessOnTrainingExpiry);
```

**Risk:**
Memory and thread handle exhaustion on long-running containers. On application servers that track unclosed resources (e.g., Tomcat thread-pool monitoring), repeated redeployment without full JVM restarts will cause `OutOfMemoryError` or prevent clean shutdown. The detached thread also means exceptions thrown after `execute()` returns cannot be observed by Quartz or any monitoring infrastructure.

**Recommendation:**
Remove the extra executor entirely. `DriverAccessRevokeJob.execute()` is already invoked by Quartz on a pooled thread. Call `revokeDriverAccessOnTrainingExpiry()` directly without wrapping in a new executor, or — if async execution is genuinely required — inject a shared `ExecutorService` managed by the application lifecycle that is shut down in `contextDestroyed`.

---

### HIGH: Scheduler Not Shut Down on Application Stop — Resource Leak and Ghost Jobs

**File:** `DriverAccessRevokeJobScheduler.java` (lines 37–40)

**Description:**
`contextDestroyed()` does not obtain a reference to the running `Scheduler` and call `scheduler.shutdown()`. The Quartz scheduler and its internal thread pool continue executing after the servlet context is destroyed. On containers that support hot redeployment (Tomcat, JBoss), this means the 2 AM job continues firing against whatever database connection pool is still reachable, potentially against a half-torn-down application. On a full JVM shutdown the threads are killed abruptly, which may leave partially committed database state (a `driver_unit` delete loop could be interrupted mid-batch).

Additionally, no reference to the `Scheduler` instance is retained anywhere, so even if the intent were to shut it down it is no longer accessible.

```java
// DriverAccessRevokeJobScheduler.java lines 37-40
@Override
public void contextDestroyed(ServletContextEvent servletContextEvent) {
    new ServletException("Application Stopped").printStackTrace();
}
```

**Risk:**
Ghost Quartz threads continue running after undeployment, causing database operations to fire against a context that no longer exists. On hot-redeploy scenarios a new scheduler is also started by `contextInitialized`, resulting in duplicate concurrent job executions.

**Recommendation:**
Store the `Scheduler` reference as an instance field. In `contextDestroyed`, call `scheduler.shutdown(true)` (blocking until running jobs complete) and remove the meaningless `new ServletException(...).printStackTrace()` line. The `scheduler` field should be `volatile` or otherwise safely published between the listener callbacks, which run on potentially different threads.

---

### HIGH: Lombok @Data Generates toString() That Exposes Plaintext Passwords and Access Token

**File:** `DriverBean.java` (lines 9, 37–42)

**Description:**
`DriverBean` is annotated `@Data`, which generates a `toString()` method that includes every field. The bean holds:

- `pass` — plaintext password (populated from the database column `password` via `DriverDAO.getDriverById`, lines 438–439 of DriverDAO.java)
- `cpass` — confirm-password copy (same database value)
- `pass_hash` — password hash
- `op_code` — operator code / PIN
- `accessToken` — Bearer/access token used for Cognito API calls
- `cognito_username` — AWS Cognito username

Any log statement, exception message, JPA dirty-checking trace, or debugger watch that calls `toString()` on a `DriverBean` instance will emit all of these values in plaintext. Because the class also implements `Serializable`, the same data would appear in any session snapshot written to disk or a distributed cache.

```java
// DriverBean.java lines 9, 37-42
@Data
@NoArgsConstructor
public class DriverBean implements Serializable {
    ...
    private String pass = null;
    private String cpass = null;
    private String pass_hash = null;
    private String op_code = null;
    private String cognito_username = null;
    private String accessToken = null;
```

**Risk:**
Credential leakage into application logs, heap dumps, thread dumps, session-persistence stores, and any serialized form written by the Java session replication mechanism. The `pass` field is confirmed to be populated with a live database password value in `DriverDAO.getDriverById` (lines 438–439), and the list of `DriverBean` instances is stored in the HTTP session via `session.setAttribute("arrDriver", arrDriver)`.

**Recommendation:**
Override `toString()` explicitly (or use `@ToString(exclude = {"pass","cpass","pass_hash","op_code","accessToken"})`) to exclude all credential fields. Implement `writeObject`/`readObject` to prevent serialization of those fields, or mark them `transient`. Better still, separate the authentication/credential concern into a distinct, non-serializable object rather than carrying passwords alongside display data.

---

### HIGH: Serializable DriverBean with Credential Fields Stored in HTTP Session

**File:** `DriverBean.java` (lines 11–12); confirmed cross-reference in `SearchAction.java` line 53 and `RegisterAction.java` line 67

**Description:**
`DriverBean implements Serializable` with a declared `serialVersionUID`. The DAO populates `pass` and `cpass` with the driver's password hash directly from the database result set (`DriverDAO.java` lines 438–439). Action classes then store a `List<DriverBean>` in the HTTP session:

```java
// SearchAction.java line 53
session.setAttribute("arrDriver", arrDriver);

// RegisterAction.java line 67
session.setAttribute("arrDriver", arrDriver);
```

If session persistence is enabled (file store, JDBC store, distributed cache), these serialized beans — including the password field — are written to persistent storage in plaintext. Even without session persistence, in-memory `DriverBean` objects containing passwords remain live for the entire session lifetime, expanding the attack window if memory is dumped.

**Risk:**
Passwords at rest in session store files or database tables. Any path that serializes the session (clustering, session fixation exploits, heap dump) exposes credentials.

**Recommendation:**
Do not populate `pass`/`cpass` fields when constructing beans for session storage or list display. The query used by `getDriverById` (line 9 of the `DriverBean` builder call chain) selects the password column unnecessarily for display contexts. Use a dedicated projection/DTO without credential fields for list and session operations.

---

### MEDIUM: contextDestroyed Creates and Immediately Discards a ServletException — Misleading Operational Behaviour

**File:** `DriverAccessRevokeJobScheduler.java` (lines 37–40)

**Description:**
The `contextDestroyed` implementation allocates a new `ServletException` object purely to call `printStackTrace()` on it. The exception is never thrown, never stored, and carries no diagnostic payload. The stack trace printed is the allocation site, not any real error context. Any operations monitoring tool that scrapes stderr for exception stack traces will produce false-positive alerts every time the application stops normally.

```java
new ServletException("Application Stopped").printStackTrace();
```

**Risk:**
Noise in operational logs that can mask genuine errors. Operators who rely on "no exceptions in logs" as a health signal will see false positives. The intent appears to have been a log message; the implementation is functionally wrong.

**Recommendation:**
Replace with a proper log statement: `log.info("DriverAccessRevokeJobScheduler: context destroyed, shutting down scheduler.")`. Remove the `ServletException` construction entirely. Add the actual `scheduler.shutdown()` call described in the HIGH finding above.

---

### MEDIUM: Incorrect Password Field Used in Cognito Update (pass vs pass_hash Guard)

**File:** `DriverBean.java` (fields `pass`, `pass_hash` at lines 37–39); cross-reference `DriverDAO.java` line 620

**Description:**
In `DriverDAO.updateGeneralUserInfo` the logic reads:

```java
if (StringUtils.isNotBlank(driverbean.getPass_hash())) userUpdateRequest.setPassword(driverbean.getPass());
```

The condition checks whether `pass_hash` is non-blank (i.e., a hashed credential exists) and then sets the Cognito password to `driverbean.getPass()` — the plaintext password field. If `pass` contains the raw database hash (as it does when populated via `getDriverById` lines 438–439, where both `pass` and `cpass` are set to `rs.getString(9)` which is the stored `password` column) then a bcrypt/hash string may be transmitted to Cognito as the new plaintext password, corrupting the Cognito credential. The guard condition also conflates "a hash exists" with "the user is changing their password," which is semantically unclear.

**Risk:**
Corrupted Cognito credentials, locking out drivers from the mobile application, or — if the password column stores plaintext in some legacy context — transmission of plaintext passwords to a third-party API in a field that should carry a user-chosen new password.

**Recommendation:**
Audit the semantics of `pass` vs `pass_hash` vs the intent of this update path. Introduce a dedicated `newPassword` field that is only populated when a password change is explicitly requested, and gate the Cognito update on that field rather than on the presence of a hash value.

---

### MEDIUM: Missing @DisallowConcurrentExecution — Overlapping Job Runs Possible

**File:** `DriverAccessRevokeJob.java` (line 12)

**Description:**
`DriverAccessRevokeJob` does not carry the `@DisallowConcurrentExecution` annotation. If Quartz is configured with more than one worker thread (the default `StdSchedulerFactory` provisions 10 threads), and if the job is ever misfired and replayed, or if a future cron schedule change causes executions to overlap, two instances of `revokeDriverAccessOnTrainingExpiry()` can run simultaneously. Both instances call `getALLExpiredTrainigs()` and then delete from `driver_unit` for each result. Without a `SELECT ... FOR UPDATE` or application-level lock, both instances query the same snapshot of expired trainings and attempt to delete the same rows, producing duplicate delete attempts and possible race conditions in the DB connection pool.

**Risk:**
Benign at the database level if deletes are idempotent (deleting an already-deleted row is a no-op), but the pattern is fragile: if the schema gains cascades or triggers, concurrent deletes may cause constraint violations or double-notification emails.

**Recommendation:**
Annotate `DriverAccessRevokeJob` with `@DisallowConcurrentExecution`. This is low-cost and prevents the overlapping execution class of bugs entirely.

---

### MEDIUM: Silent Exception Swallowing Inside Lambda — Per-Driver Failures Are Invisible

**File:** `DriverAccessRevokeJob.java` (lines 22–24); `DriverDAO.java` (lines 913–916)

**Description:**
Inside `revokeDriverAccessOnTrainingExpiry()`, the `forEach` lambda in `DriverDAO` catches `SQLException` and calls `e.printStackTrace()` only, then continues processing the next driver. The outer catch in `DriverAccessRevokeJob.revokeDriverAccessOnTrainingExpiry()` also only calls `e.printStackTrace()`. This means:

1. If any driver's access revocation fails (e.g., a transient DB error), the failure is printed to stderr and silently skipped with no retry, no alerting, and no audit record.
2. The overall job succeeds from Quartz's perspective (no `JobExecutionException` is thrown), so Quartz will not reschedule a retry or trigger a misfire handler.
3. Because the job is dispatched to a detached executor thread (see thread leak finding), even the `SQLException` caught in `revokeDriverAccessOnTrainingExpiry()` is swallowed without Quartz ever seeing it.

```java
// DriverAccessRevokeJob.java lines 20-24
try {
    DriverDAO.revokeDriverAccessOnTrainingExpiry();
} catch (SQLException e) {
    e.printStackTrace();
}
```

**Risk:**
Drivers whose access should have been revoked remain active without any indication of failure. Partial batch failures (some drivers revoked, some not) go undetected. The security invariant that expired-training drivers cannot operate equipment is silently broken.

**Recommendation:**
Log exceptions using the application's structured logger at ERROR level. Throw a `JobExecutionException` from `execute()` on failure so Quartz can apply configured misfire/retry policies. Consider accumulating per-driver failures and emitting a summary alert after the batch completes.

---

### LOW: Scheduler Not Referenced After Start — Cannot Be Shut Down

**File:** `DriverAccessRevokeJobScheduler.java` (line 28)

**Description:**
The `Scheduler` instance created in `contextInitialized` is a local variable and is not stored anywhere (instance field, `ServletContext` attribute, or static registry). Even if a developer attempts to fix the `contextDestroyed` shutdown gap, there is currently no way to reach the running `Scheduler` from that method.

```java
Scheduler scheduler = ((SchedulerFactory) new StdSchedulerFactory()).getScheduler();
scheduler.scheduleJob(...);
scheduler.start();
// scheduler goes out of scope here
```

**Risk:**
Compounds the HIGH shutdown finding. The architectural mistake makes correct shutdown harder to retrofit.

**Recommendation:**
Store the `Scheduler` as a private instance field on `DriverAccessRevokeJobScheduler`. Declare it `private volatile Scheduler scheduler` to ensure safe publication between `contextInitialized` and `contextDestroyed` calls.

---

### LOW: SchedulerException Silenced with printStackTrace

**File:** `DriverAccessRevokeJobScheduler.java` (lines 32–34)

**Description:**
If `StdSchedulerFactory.getScheduler()`, `scheduleJob()`, or `start()` throws a `SchedulerException`, the catch block calls `e.printStackTrace()` and returns normally. The servlet context listener completes without error, so the container considers initialization successful. The Quartz job will never run, but there is no indication in any health check, startup log, or monitoring system.

**Risk:**
Silent failure of the entire access-revocation subsystem at startup. Expired-training drivers retain equipment access indefinitely with no alert.

**Recommendation:**
Log at ERROR level using the application logger and consider rethrowing as a `RuntimeException` to abort context initialization, or at minimum emit a structured alert so operations can detect the failure.

---

### LOW: Raw ArrayList Type in DriverJobDetailsBean

**File:** `DriverJobDetailsBean.java` (lines 11, 33, 75)

**Description:**
The `driverList` field and its getter/setter use the raw type `ArrayList` without a type parameter:

```java
private ArrayList driverList;
public ArrayList getDriverList() { return driverList; }
public void setDriverList(ArrayList driverList) { this.driverList = driverList; }
```

Raw types suppress generic type checking, making it impossible for the compiler to enforce what the list contains. Combined with `setDriverList` accepting any `ArrayList`, a caller could inject an `ArrayList` of arbitrary objects.

**Risk:**
Low in isolation, but raw types are a common source of `ClassCastException` at runtime and make static analysis tools less effective. If `driverList` content is ever cast without a null/type check before use, this could become an exploitable path for unexpected object injection.

**Recommendation:**
Parameterise the field: `private ArrayList<DriverBean> driverList` (or `List<DriverBean>`). Update getter and setter accordingly.

---

### LOW: DriverJobDetailsBean Has No equals/hashCode and No Serializable

**File:** `DriverJobDetailsBean.java`

**Description:**
`DriverJobDetailsBean` provides no `equals()`, `hashCode()`, or `toString()` implementations, and does not implement `Serializable`. If instances are placed in `HashSet`, used as `Map` keys, or compared with `equals()`, identity semantics (object reference) are used rather than value semantics, which is typically not the intended behaviour for a data bean. Unlike `DriverBean`, the absence of `Serializable` is actually a protective default here (session serialization cannot accidentally capture this bean), but the lack of documentation of that choice means a future developer may add `implements Serializable` without considering the implications.

**Risk:**
Correctness bugs if the bean is placed in collections that rely on `equals`/`hashCode`. Minor risk of inadvertently becoming serializable in a future change.

**Recommendation:**
Add `equals` and `hashCode` implementations (or use Lombok `@EqualsAndHashCode` with appropriate field selection). Add a comment documenting that the class is intentionally not `Serializable`.

---

### INFO: Pass / Confirm-Pass Fields Appear to Carry Database Hash, Not User Input

**File:** `DriverBean.java` (lines 37–38); `DriverDAO.java` (lines 438–439)

**Description:**
`pass` and `cpass` are named as if they hold user-entered plaintext password and confirm-password values (a common pattern for registration forms). However, `getDriverById` populates both fields from `rs.getString(9)` which maps to the database `password` column — almost certainly a stored hash. This field naming is confusing and causes the `pass_hash` guard logic in `updateGeneralUserInfo` to be incorrect (see MEDIUM finding). The comment `// FIXME is it same than licno ?` at line 29 suggests existing uncertainty about field semantics.

**Risk:**
Developer confusion leading to credential handling bugs as already observed in line 620 of DriverDAO.

**Recommendation:**
Rename fields to reflect their actual semantics (`storedPasswordHash`, `newPasswordPlaintext`, etc.) and add Javadoc. Remove `cpass` if it is always a duplicate of `pass`.

---

### INFO: No Authorization Check in Quartz Job

**File:** `DriverAccessRevokeJob.java`

**Description:**
The job executes `DriverDAO.revokeDriverAccessOnTrainingExpiry()` with no credential validation, authorization check, or tenant-scoping guard. `QUER_ALL_EXPIRED_TRAININGS` operates across all companies and all drivers in the database. This is the expected design for a system-level background job, but it is worth noting that any misconfiguration of the scheduler (e.g., triggering the job via an unauthenticated HTTP endpoint in a future change) would revoke access for all expired-training drivers across the entire platform without any per-company authorization gate.

**Risk:**
Informational for current architecture. Becomes a risk if the job is ever exposed via an administrative HTTP trigger without authentication.

**Recommendation:**
Document in code comments that this job operates globally across all tenants by design. If an on-demand trigger endpoint is ever added, ensure it requires strong authentication and authorization.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 4     |
| MEDIUM   | 4     |
| LOW      | 4     |
| INFO     | 2     |
| **Total**| **14**|
