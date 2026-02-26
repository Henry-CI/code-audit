# Pass 1 Audit — DriverService / DriverServiceException / DriverTrainingBean / DriverUnitBean / DriverVehicleBean / DriverUnitDAO

**Files:**
- `src/main/java/com/service/DriverService.java`
- `src/main/java/com/service/DriverServiceException.java`
- `src/main/java/com/bean/DriverTrainingBean.java`
- `src/main/java/com/bean/DriverUnitBean.java`
- `src/main/java/com/bean/DriverVehicleBean.java`
- `src/main/java/com/dao/DriverUnitDAO.java`

**Date:** 2026-02-26

---

## Summary

This audit covers the driver service layer, its exception type, three driver-related bean classes, and the authorization-critical DriverUnitDAO. The most severe issues are concentrated in `DriverUnitDAO.saveDriverVehicle()` and `DriverService.updateAssignedVehicle()`. The DAO performs a multi-step read-modify-write operation that controls which drivers are assigned to which forklift units; it contains no ownership or company-scope authorization check before executing DELETE and INSERT operations, enabling any authenticated caller to reassign or revoke unit access for any driver in the system (IDOR). Rollback handling in the same method silently swallows secondary `SQLException`s, meaning failed rollbacks are never surfaced. The service singleton is also implemented with a broken double-checked locking pattern that can yield a partially-initialized instance under the Java Memory Model. Additionally, `DriverTrainingBean` carries PII fields (`email`, `comp_email`, `first_name`, `last_name`) that will be emitted in full by Lombok `@Data`-generated `toString()`, creating log-exposure risk, and the bean lacks `serialVersionUID` entirely, risking `InvalidClassException` after any field change. `DriverUnitBean` has a type mismatch between its builder and field declarations. The exception class is clean but is a `RuntimeException`, meaning callers can silently ignore it at compile time.

---

## Findings

### [CRITICAL]: Insecure Direct Object Reference — Unit Assignment Modifiable Without Ownership Check

**File:** DriverUnitDAO.java (lines 49–93)
**Description:** `saveDriverVehicle()` accepts a `DriverVehicleBean` containing a `driverId` and a list of `DriverUnitBean` entries. It reads the currently assigned units for the driver using only `driver_id` (line 57), then performs DELETE and INSERT operations driven purely by the bean contents. At no point is `compId` from the bean (or from a session context) compared against the company that owns the driver or the units being modified. An authenticated user from one company could submit a crafted request supplying any `driver_id` and any `unit_id` values, and the DAO would silently re-assign or revoke forklift unit access for drivers at a completely different company.

```java
// line 57 — query scoped to driver_id only, no comp_id filter
List<Long> unitsAssigned =
    DBUtil.queryForObjects(connection, QUERY_UNITS_ASSIGNED,
        stmt -> stmt.setLong(1, driverVehicle.getId()), rs -> rs.getLong(1));

// line 61-64 — DELETE with no company ownership assertion
DBUtil.updateObject(connection, UNASSIGN_DRIVER_UNIT, stmt -> {
    stmt.setLong(1, driverVehicle.getId());
    stmt.setLong(2, driverUnitBean.getUnitId());
});
```

**Risk:** Complete cross-tenant authorization bypass. An attacker can grant themselves access to any forklift unit in the database, or strip access from any driver at any company, without owning those records. This is an authorization-critical table.
**Recommendation:** Before executing any DML, verify that `driverVehicle.getId()` (driver) and every `unitId` in `driverVehicle.getDriverUnits()` belong to the same `comp_id` as the authenticated session. Add a pre-flight query that confirms the driver belongs to the caller's company, and add a `comp_id` column constraint (or view-based restriction) on unit lookups. The `DriverVehicleBean.compId` field exists but is never used in the DAO for authorization.

---

### [CRITICAL]: Broken Double-Checked Locking in DriverService Singleton

**File:** DriverService.java (lines 12–23)
**Description:** The singleton implementation checks `theInstance == null` outside the `synchronized` block but does not re-check inside it. Under the Java Memory Model, without a second null-check inside `synchronized`, two threads can race through the outer check simultaneously; the first enters the synchronized block and constructs the instance, but by the time the second thread acquires the lock, `theInstance` is already set — so the pattern as written happens to avoid a double-instantiation for this particular class. However, the `theInstance` field is not declared `volatile`, which means the JVM is free to reorder the write to `theInstance` relative to the constructor body. A second thread reading `theInstance` after the first thread writes the reference but before the constructor finishes can see a partially constructed object. This is a classic broken double-checked locking defect.

```java
private static DriverService theInstance;  // not volatile

public static DriverService getInstance() {
    if (theInstance == null) {              // unsynchronized read
        synchronized (DriverService.class) {
            theInstance = new DriverService(); // no inner null check, non-volatile write
        }
    }
    return theInstance;
}
```

**Risk:** Under concurrent load, a thread may receive a `DriverService` reference whose `driverUnitDAO` field has not yet been written, resulting in a `NullPointerException` or use of a partially-initialized DAO, which could lead to data corruption or silent authorization failures.
**Recommendation:** Declare `theInstance` as `volatile`, add a second null-check inside the synchronized block, or replace the pattern with initialization-on-demand holder idiom or a simple `enum`-based singleton.

---

### [HIGH]: Silent Swallowing of Rollback Failure Masks Data Integrity Errors

**File:** DriverUnitDAO.java (lines 66–70, 81–85)
**Description:** Both the unassign and assign loops catch `SQLException` from the DML operation, attempt a `connection.rollback()`, and then — if `rollback()` itself throws — catch and ignore that secondary exception with an inline comment `// Ignore the error`. The outer `RuntimeException` is then thrown without any indication that the rollback failed. The transaction is left in an ambiguous state: the caller believes a rollback occurred, but it may not have, leaving partial unit assignment changes committed.

```java
} catch (SQLException e) {
    try {
        connection.rollback();
    } catch (SQLException e1) {
        // Ignore the error   <-- rollback failure silently swallowed
    }
    throw new RuntimeException("Unable to save driver unit assignations...", e);
}
```

**Risk:** If a rollback fails (e.g., connection interruption), partial DML changes may be committed unintentionally. The system appears to have rolled back but has not, causing driver-unit authorization records to be in an inconsistent state without any log entry or alert.
**Recommendation:** Log the rollback failure at ERROR level (including the cause) before rethrowing. Consider using a proper transaction management framework (Spring `@Transactional` or equivalent) that handles rollback lifecycle reliably. At minimum, `e1` should be added as a suppressed exception to the rethrown `RuntimeException` via `e.addSuppressed(e1)`.

---

### [HIGH]: No Input Validation in Service Layer Before Delegating to DAO

**File:** DriverService.java (lines 25–31)
**Description:** `updateAssignedVehicle()` accepts a `DriverVehicleBean` and immediately delegates to `driverUnitDAO.saveDriverVehicle()` without any validation of the bean's contents. There is no null-check on `driverVehicle`, no check that `driverVehicle.getId()` is non-null or positive, no check that `driverVehicle.getCompId()` is non-null, no size limit on `driverVehicle.getDriverUnits()`, and no verification that the caller's session matches the bean's embedded `compId`. The only null assertions present are `assert` statements in the DAO itself (lines 51–52), which are disabled at runtime unless the JVM is started with `-ea`.

```java
public void updateAssignedVehicle(DriverVehicleBean driverVehicle) throws DriverServiceException {
    try {
        driverUnitDAO.saveDriverVehicle(driverVehicle);  // no prior validation
    } catch (SQLException e) { ... }
}
```

**Risk:** Null values reach the DAO and produce database errors rather than clean validation failures. More critically, no authorization check gates this operation — any caller reaching the service layer can modify arbitrary driver-unit assignments. Combined with the IDOR finding above, this represents a complete lack of defense-in-depth.
**Recommendation:** Add explicit precondition validation at the service layer: verify non-null bean, non-null/positive IDs, and that the authenticated session's company ID equals `driverVehicle.getCompId()`. The service layer is the correct place for authorization enforcement in Struts 1.x, since there is no declarative security model on Action classes.

---

### [HIGH]: `assert` Statements Used as Runtime Guards in DAO (Disabled by Default)

**File:** DriverUnitDAO.java (lines 51–52)
**Description:** Two `assert` statements act as the sole null guards before the DAO executes database operations:

```java
assert driverVehicle != null : "driverVehicle must not be null";
assert driverVehicle.getId() != null : "driver_id must not be null";
```

Java `assert` statements are disabled by default at runtime. Unless the application server is launched with `-ea` (enable assertions), these checks never execute and a `NullPointerException` will be thrown from deep within the JDBC layer, leaking a stack trace that may expose internal SQL structure.
**Risk:** Defensive null checks are silently inactive in production, meaning malformed beans propagate unchecked into JDBC calls. Stack traces from NPEs may reach HTTP responses in the Struts error handling path, leaking SQL query structure and table names.
**Recommendation:** Replace `assert` with explicit `if` checks that throw `IllegalArgumentException` with a descriptive message, or use a utility such as `Objects.requireNonNull()`.

---

### [MEDIUM]: PII Exposure via Lombok `@Data` `toString()` in DriverTrainingBean

**File:** DriverTrainingBean.java (lines 9–68)
**Description:** `DriverTrainingBean` is annotated with Lombok `@Data`, which auto-generates a `toString()` method that includes every field. The bean contains the following PII fields: `first_name`, `last_name`, `email`, and `comp_email`. If this bean is ever logged (e.g., via `log.debug("bean: {}", bean)` or as part of an exception message), all four PII fields are emitted to the log in plaintext. This is a concern under GDPR/CCPA for any deployment serving EU or California users.

```java
private String first_name;
private String last_name;
private String email;
private String comp_email;
```

**Risk:** PII leakage into application logs. If logs are shipped to a SIEM, log aggregator, or third-party service, driver names and email addresses are exposed without consent.
**Recommendation:** Annotate PII fields with `@ToString.Exclude` (Lombok), or replace `@Data` with explicit `@Getter`/`@Setter`/`@EqualsAndHashCode` and write a custom `toString()` that omits or masks email fields.

---

### [MEDIUM]: Missing `serialVersionUID` in DriverTrainingBean

**File:** DriverTrainingBean.java (line 11)
**Description:** `DriverTrainingBean implements Serializable` but does not declare a `serialVersionUID` field. In contrast, `DriverVehicleBean` (line 15) declares one explicitly. Without `serialVersionUID`, the JVM computes a default value based on the class structure. Any change to the class (adding or removing a field, changing a field type) will change the computed UID, causing `InvalidClassException` if a previously serialized instance is deserialized — for example, from an HTTP session stored in a distributed session store or a file-based session cache.

**Risk:** Uncontrolled deserialization failures after code deployments. In a clustered Struts deployment using session replication, drivers may be silently logged out or encounter errors after any code change to this bean.
**Recommendation:** Add `private static final long serialVersionUID = <generated value>L;` to the class, consistent with the pattern already used in `DriverVehicleBean`.

---

### [MEDIUM]: `DriverUnitBean` Builder / Field Type Mismatch for `trained`

**File:** DriverUnitBean.java (lines 20 vs. 23)
**Description:** The `trained` field is declared as `String` at line 20 (`private String trained;`), but the `@Builder`-annotated constructor at line 23 accepts it as `boolean`:

```java
private String trained;                    // field type: String

@Builder
private DriverUnitBean(..., boolean trained) {  // builder param type: boolean
    this.trained = trained ? "Yes" : "No";
}
```

The public setter generated by `@Data` will be `setTrained(String trained)`, while the builder accepts a `boolean`. Any code that uses the setter path (e.g., Struts form binding, reflection-based mapping) can write an arbitrary string directly into `trained`, bypassing the "Yes"/"No" normalization. The DAO at `DriverUnitDAO.java` line 46 calls `rs.getBoolean("trained")` and routes through the builder, which is consistent, but the setter path is unguarded.

**Risk:** If a downstream component calls `setTrained("1")` or `setTrained("true")` via the setter, the field will contain an unnormalized value, which could cause incorrect display logic or incorrect authorization decisions if `trained` status gates unit access.
**Recommendation:** Either change the field type to `boolean` and use `@Data` uniformly, or remove the public setter for `trained` using `@Setter(AccessLevel.NONE)` and require all construction to go through the builder.

---

### [MEDIUM]: `FOR UPDATE` Lock Acquired Without Explicit Timeout

**File:** DriverUnitDAO.java (line 13)
**Description:** The constant `QUERY_UNITS_ASSIGNED` uses a `SELECT ... FOR UPDATE` advisory lock:

```java
private static final String QUERY_UNITS_ASSIGNED =
    "select unit_id from driver_unit du where driver_id = ? for update";
```

This row-level lock is held for the duration of the outer transaction (until `connection.commit()` on line 91 or until the connection closes). No lock wait timeout is configured at the query or connection level. Under concurrent load, if two requests attempt to save vehicle assignments for the same driver simultaneously, one will block indefinitely on the lock.

**Risk:** Denial-of-service via lock contention. A slow client or a network error occurring between the `FOR UPDATE` and the `commit()` can hold the lock for the full JDBC connection timeout, blocking all other requests for that driver's unit assignments. If connection pool exhaustion is reached, the entire application can become unresponsive.
**Recommendation:** Set a lock wait timeout at the session level before executing the query (e.g., `SET innodb_lock_wait_timeout = N` for MySQL, or use `SELECT ... FOR UPDATE NOWAIT`). Alternatively, refactor the logic to avoid row-level locking by using optimistic concurrency (version column).

---

### [LOW]: `DriverServiceException` Extends `RuntimeException` — Silently Ignorable

**File:** DriverServiceException.java (lines 3–12)
**Description:** `DriverServiceException` is an unchecked exception (`extends RuntimeException`). While this is a common modern Java convention, in the context of Struts 1.x Action classes it means callers that invoke `DriverService.updateAssignedVehicle()` are not required by the compiler to handle or declare the exception. If an Action class omits a try-catch, assignment failures will propagate as unhandled exceptions to the Struts exception handler, potentially producing generic error pages that disclose exception messages.

**Risk:** Low probability of data loss, but the exception message constructed in `DriverService` (line 29) includes `driverVehicle.getId()` — a driver ID — which may be surfaced to the end user via a generic Struts error page if the exception is not caught upstream.
**Recommendation:** Confirm that all Struts Action classes calling `updateAssignedVehicle()` explicitly catch `DriverServiceException` and handle it gracefully. Alternatively, convert to a checked exception to force callers to acknowledge it.

---

### [LOW]: Exception Message Leaks Internal Driver ID

**File:** DriverService.java (line 29)
**Description:** The exception message constructed on failure includes the driver's internal database ID:

```java
throw new DriverServiceException(
    "Unable to update assigned vehicle for driver " + driverVehicle.getId(), e);
```

If this exception reaches a Struts error page (e.g., via Struts' default exception handler writing to `ActionMessages` or an unhandled exception filter), the driver ID is exposed to the end user.

**Risk:** Minor information disclosure — internal primary key enumeration aids IDOR attacks by confirming valid driver ID values.
**Recommendation:** Remove the ID from the user-facing exception message. Log the ID at ERROR level for internal diagnostics only, and present a generic message to the caller.

---

### [LOW]: `DriverVehicleBean` — No `serialVersionUID` Stability Concern for Nested Bean

**File:** DriverVehicleBean.java (line 15)
**Description:** `DriverVehicleBean` declares `serialVersionUID = -8541229534532258948L` (line 15), which is correct. However, it contains a `List<DriverUnitBean>` field (line 20), and `DriverUnitBean` itself does not declare a `serialVersionUID`. During serialization of `DriverVehicleBean`, Java serializes the embedded `DriverUnitBean` instances as well. Because `DriverUnitBean` lacks a stable UID, changes to `DriverUnitBean` can cause deserialization of previously stored `DriverVehicleBean` instances to fail with `InvalidClassException`.

**Risk:** Cascading deserialization failure when `DriverUnitBean` fields change, even if `DriverVehicleBean` itself is unchanged.
**Recommendation:** Add `serialVersionUID` to `DriverUnitBean` to match the pattern in `DriverVehicleBean`. Note that `DriverUnitBean` does not currently declare `implements Serializable`, so this also needs to be added for the serialization chain to be formally correct.

---

### [INFO]: `DriverUnitBean` Does Not Declare `implements Serializable`

**File:** DriverUnitBean.java (line 11)
**Description:** `DriverUnitBean` is embedded as a `List<DriverUnitBean>` field inside `DriverVehicleBean implements Serializable`, but `DriverUnitBean` itself does not implement `Serializable`. Attempting to serialize a `DriverVehicleBean` instance that contains `DriverUnitBean` objects will throw `java.io.NotSerializableException` at runtime.

**Risk:** If `DriverVehicleBean` is placed in an HTTP session (which is `Serializable` in clustered environments) with a populated `driverUnits` list, session replication or passivation will throw a `NotSerializableException`, likely crashing the request.
**Recommendation:** Add `implements Serializable` to `DriverUnitBean` and add a `serialVersionUID`.

---

### [INFO]: DriverUnitDAO — Static Method on Instance Singleton

**File:** DriverUnitDAO.java (lines 19–33)
**Description:** `DriverUnitDAO` is designed as a singleton (instance-based, accessed via `getInstance()`), but `getDriverUnitsByCompAndDriver()` is declared `static` (line 33). This means the method can be called without going through the singleton and bypasses any future instance-level state (e.g., connection pooling configuration, mock injection for tests). Meanwhile, `saveDriverVehicle()` is an instance method. The API surface is inconsistent.

**Risk:** Low direct security risk, but the inconsistency makes it harder to inject test doubles or mock the DAO layer for security testing. It also means calls to the static method will bypass any future instance-level access controls or audit hooks added to the singleton.
**Recommendation:** Make `getDriverUnitsByCompAndDriver()` an instance method to be consistent with `saveDriverVehicle()` and injectable via the singleton.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH     | 3 |
| MEDIUM   | 4 |
| LOW      | 3 |
| INFO     | 2 |
| **Total**| **14** |
