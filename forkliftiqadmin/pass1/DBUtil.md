# Pass 1 Audit — DBUtil
**File:** src/main/java/com/util/DBUtil.java
**Date:** 2026-02-26

## Summary

`DBUtil` is the sole database access utility used by all DAOs in the application. It obtains connections via JNDI lookup against a `DataSource`, wraps them in a `log4jdbc.ConnectionSpy` for logging, and exposes a family of `queryForObjects`, `queryForObject`, `updateObject`, and `executeStatementWithRollback` methods. All public query methods accept `PreparedStatement`-based SQL, which is structurally sound, but one critical overload (`queryForObject(String, ResultMapper)`) accepts a pre-built SQL string with no parameter-binding step, enabling raw SQL injection if callers pass user-supplied data. More pervasively, every method except `executeStatementWithRollback` swallows `SQLException` silently via `e.printStackTrace()` and returns an empty result or `-1`, meaning security-relevant query failures are invisible to callers and can cause authorization logic to silently permit or deny access based on an empty/default result set. Additional concerns include JVM-argument-controlled database name selection, a deprecated but still-compiled `closeConnection` helper, and inconsistent resource-cleanup patterns in some overloads.

---

## Findings

### CRITICAL: `queryForObject(String, ResultMapper)` accepts a raw SQL string with no parameter binding
**File:** DBUtil.java (lines 128–146)
**Description:**
The two-argument overload `queryForObject(String query, ResultMapper<T> mapper)` calls `conn.prepareStatement(query)` and immediately calls `stmt.executeQuery()` — there is no `PreparedStatementHandler` argument and therefore no step where bind parameters can be set. Any caller that constructs the `query` string by concatenating user-supplied values before passing it to this method will achieve SQL injection. All other query/update methods require a `PreparedStatementHandler` that forces the caller to use `setXxx()` bind methods; this overload is the lone exception and stands out as the injection-ready entry point.
**Risk:**
Full SQL injection. A DAO that calls this overload with a dynamically-built string can read, modify, or (depending on DB user privileges) drop arbitrary data. Because DAOs are widespread in this codebase, every caller of this overload must be reviewed in Pass 2.
**Recommendation:**
Remove this overload entirely and replace all call sites with the three-argument form `queryForObject(String, PreparedStatementHandler, ResultMapper)`. If a no-parameter query is genuinely needed, document it clearly, restrict callers to compile-time constant SQL strings, and add a code-review gate (e.g., a `@SuppressWarnings` equivalent with mandatory comment) to prevent future misuse.

---

### HIGH: `SQLException` swallowed in all read/write methods — security decisions based on empty results
**File:** DBUtil.java (lines 75–77, 98–100, 119–121, 140–142, 164–166, 186–188, 203–205, 220–222)
**Description:**
Every method except `executeStatementWithRollback` catches `SQLException`, prints a stack trace to stderr, and then returns:
- An empty `List` for `queryForObjects` variants
- `Optional.empty()` for `queryForObject` variants
- `-1` for `updateObject` variants

The methods still declare `throws SQLException` in their signatures, giving callers the false impression that a thrown exception means failure; in practice, exceptions are never propagated from these paths. Callers that rely on a non-empty result for authentication checks (e.g., "look up user by credentials; if found, log in") will silently treat a DB error as "user not found" rather than as an error condition, which may produce either a security bypass or an undetected denial-of-service, depending on how the caller interprets an empty result.
**Risk:**
- Authentication/authorisation bypass or silent denial: if a credential query fails, `Optional.empty()` is returned, and callers may grant or deny access based on that empty result without knowing the query failed.
- Update operations returning `-1` are indistinguishable from a legitimate "0 rows updated" return if callers do not check for the sentinel value explicitly.
- Stack traces written to stderr may leak schema/query details to server logs accessible to lower-privileged users or log-aggregation pipelines.
**Recommendation:**
Re-throw the `SQLException` from all catch blocks (or wrap it in a runtime exception) so callers receive a genuine error signal. Remove the misleading `throws SQLException` declarations from methods that currently swallow exceptions. Audit every DAO caller for logic that silently tolerates empty results in security-sensitive paths.

---

### HIGH: JVM argument `-Ddb=` can override the production database name at startup
**File:** DBUtil.java (lines 43–54)
**Description:**
`ensureDatabaseNameIsSet()` iterates over JVM input arguments and, if any argument starts with `-Ddb=`, uses the supplied value as the JNDI name for the `DataSource`. This value is never validated against a whitelist. An operator with the ability to set JVM arguments (e.g., via a startup script, container environment variable, or CI/CD pipeline) can redirect the entire application to an arbitrary JNDI resource — including one pointing to a different database, or a resource that does not exist (causing a `NamingException`). In a shared hosting or containerised environment where multiple applications share a JVM process, this is a lateral-movement vector.
**Risk:**
- Privileged data exfiltration if the attacker-controlled JNDI name points to a data source they control or can observe.
- Application-wide DoS if the name is invalid.
- In legacy JNDI environments, JNDI injection (attacker-controlled `InitialContext`) could enable remote code execution, though this is constrained by the Java version and JVM security settings in use.
**Recommendation:**
Validate the value read from `-Ddb=` against an explicit allowlist of known JNDI names before assignment. Log a warning and fall back to `RuntimeConf.database` if an unrecognised name is supplied. Consider eliminating the JVM argument override entirely and using an environment-variable or properties-file approach with documented allowed values.

---

### MEDIUM: `queryForObject` overloads use `rs.isLast()` for uniqueness check — unreliable with some JDBC drivers
**File:** DBUtil.java (lines 137, 161, 183)
**Description:**
The three `queryForObject` overloads detect more-than-one result by calling `rs.isLast()` after the first `rs.next()`. `isLast()` is not supported by all JDBC drivers (the JDBC specification allows drivers to throw `SQLException` with "not supported"), and for forward-only result sets it may return incorrect results depending on the driver implementation. If `isLast()` incorrectly returns `true` (or throws), the method returns the first row without detecting the duplicate, silently masking data-integrity problems. Furthermore, the thrown `SQLException` from `isLast()` falls into the swallowing catch block described above, making it completely invisible.
**Risk:**
Security-relevant uniqueness guarantees (e.g., "look up a single user by ID") can be silently violated, returning the first of multiple matching rows without signalling the anomaly. This is particularly dangerous if an attacker can arrange for duplicate rows to exist.
**Recommendation:**
Replace the `isLast()` check with a second call to `rs.next()` to confirm no additional rows exist. This is portable across all JDBC drivers and avoids the forward-only cursor limitation.

---

### MEDIUM: `updateObject(Connection, String, PreparedStatementHandler)` returns `-1` on failure, indistinguishable from success by many callers
**File:** DBUtil.java (lines 195–209)
**Description:**
When a `SQLException` occurs inside `updateObject`, the method returns `-1`. The JDBC contract for `executeUpdate()` returns the number of affected rows (>= 0). Callers that check only for `> 0` or `!= 0` will silently treat the `-1` error sentinel as "zero rows updated" rather than as a failure. This is a correctness and auditability problem in any DAO that performs security-relevant writes (access-control changes, password updates, audit log insertions).
**Risk:**
Silent failure of security-critical writes (e.g., password changes, role assignments, audit records) without any exception propagating to the caller.
**Recommendation:**
As with the broader exception-swallowing issue, re-throw rather than return a sentinel. If a sentinel return is unavoidable for compatibility, document it explicitly and require all callers to check for `< 0` as an error condition, not just `== 0`.

---

### MEDIUM: `queryForObject(String, ResultMapper)` does not initialise `conn` before the `try` block — connection leak on `getConnection()` failure edge case
**File:** DBUtil.java (lines 128–146)
**Description:**
Unlike every other method in the class, this overload calls `conn = getConnection()` before the `try` block (line 131) but after the local declarations. If `getConnection()` itself throws a `SQLException`, the `finally` block still calls `DbUtils.closeQuietly(conn, stmt, rs)` where `conn` is the object obtained just before the exception — however, `conn` may be partially initialised (the `ConnectionSpy` constructor could theoretically throw). More importantly, if `getConnection()` throws, the connection is passed to `closeQuietly` when it is already in an indeterminate state, which may mask the original error. This is a structural inconsistency compared to all other methods that initialise `conn = null` and obtain the connection inside the `try`.
**Risk:**
Low likelihood of exploitable vulnerability, but potential connection leak and confusing error messages during failure conditions, which could mask authentication or availability problems.
**Recommendation:**
Move `conn = getConnection()` inside the `try` block, consistent with all other methods in the class.

---

### LOW: `closeConnection(Connection)` is `@Deprecated` but still compiled and accessible
**File:** DBUtil.java (lines 56–59)
**Description:**
The method is marked `@Deprecated` but remains public and callable. Deprecated methods in utility classes are frequently used by developers who miss (or ignore) the deprecation warning, leading to inconsistent resource-management patterns across DAOs. The method delegates to `DbUtils.closeQuietly(conn)`, which swallows exceptions — callers who migrate away from explicit `closeConnection` calls must rely on the `finally`-block patterns in `DBUtil` itself.
**Risk:**
Continued use of a deprecated API can lead to connection leaks if callers do not pair it correctly with other resource management. Low direct security impact, but contributes to overall code hygiene issues.
**Recommendation:**
If no callers remain (verify in Pass 2), remove the method. If callers exist, enforce migration and then remove.

---

### LOW: `log4jdbc.ConnectionSpy` wraps every connection — SQL statements and bind parameters written to application logs
**File:** DBUtil.java (line 37)
**Description:**
Every connection is wrapped in a `ConnectionSpy` from the `log4jdbc` library, which logs every SQL statement, including bind-parameter values, to the configured Log4j appenders. If the logging level is DEBUG or higher and the appender writes to a file accessible to non-administrative users (or to a remote log aggregator), sensitive query parameters (user identifiers, session tokens, credential hashes) may be exposed.
**Risk:**
Information disclosure of query parameters in log output. Severity depends on log configuration and who can read the logs.
**Recommendation:**
Review the log4jdbc and Log4j configuration to ensure SQL parameter logging is disabled in production, or that log output is restricted to administrative access only. Consider replacing `log4jdbc` with application-level audit logging that deliberately excludes sensitive bind values.

---

### INFO: `databaseName` is a mutable static field with no synchronisation
**File:** DBUtil.java (line 22, lines 43–54)
**Description:**
`databaseName` is a `private static String` written by `ensureDatabaseNameIsSet()` without synchronisation. In a multi-threaded servlet container (all Struts 1.x deployments are multi-threaded), two threads can simultaneously observe `databaseName == null` and both enter the initialisation block. While the write is idempotent (both threads would write the same value under normal conditions), the lack of synchronisation or a `volatile` declaration means the assignment is not guaranteed to be visible across CPU caches without a memory barrier, and a race on the `-Ddb=` argument-scanning loop could theoretically produce a torn write on JVMs that do not guarantee atomic 64-bit reference writes.
**Risk:**
Very low probability of observable race condition in practice, but a minor code quality and thread-safety concern.
**Recommendation:**
Initialise `databaseName` in a static initialiser block, or use `volatile` / `synchronized`, or use a `java.util.concurrent.atomic.AtomicReference` to ensure safe publication.

---

### INFO: `RuntimeConf.database` and other sensitive constants are public mutable static fields
**File:** src/main/java/com/util/RuntimeConf.java (line 6, all fields)
**Description:**
`RuntimeConf.database` (the default JNDI name) and all other configuration values are `public static` (non-`final`) fields. Any code in the application — including third-party libraries on the classpath — can overwrite `RuntimeConf.database` at runtime, redirecting all subsequent JNDI lookups.
**Risk:**
If any part of the application accepts untrusted input and can write to static fields (e.g., via reflection, Struts form population bugs, or deserialization), the database name can be hijacked. Low direct exploitability without a separate injection primitive, but contributes to an insecure-by-design configuration model.
**Recommendation:**
Declare all `RuntimeConf` fields `public static final`. Externalise mutable configuration to a properties file or environment variables read once at startup.

---

## Finding Count
- CRITICAL: 1
- HIGH: 2
- MEDIUM: 3
- LOW: 2
- INFO: 2
