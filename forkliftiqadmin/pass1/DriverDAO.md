# Pass 1 Audit — DriverDAO
**File:** src/main/java/com/dao/DriverDAO.java
**Date:** 2026-02-26

---

## Summary

DriverDAO.java is the central data-access layer for operator/driver management in the ForkliftIQ Admin application. The file is 944 lines and mixes two distinct coding styles: newer methods use a `DBUtil.queryForObjects` / `PreparedStatement`-lambda abstraction that is generally safe, while a cohort of older methods use raw `Statement` with string concatenation. The concatenation methods contain confirmed SQL injection sinks. The most severe finding is a timezone string injected directly into SQL in `getTotalDriverByID` and `getAllDriverSearch`; that string originates from the HTTP session attribute `sessTimezone`, which itself originates from a database lookup — but session data may be attacker-influenced in certain scenarios and is in any case not sanitised before SQL composition. Two additional methods (`getDriverByNm`, `getDriverByFullNm`) concatenate firstName, lastName, fullName, and compId without parameterisation and carry a developer-acknowledged `FIXME` comment. A further method (`getDriverName`) concatenates a Long id directly into SQL. Several IDOR risks exist because `getDriverById`, `updateGeneralInfo`, `updateDriverLicenceInfo`, and `updateEmailSubsInfo` accept IDs without cross-checking that the target record belongs to the session company. Password-handling issues are present: `addDriverInfo` stores passwords hashed with MD5 (cryptographically broken), and `UPDATE_ACCESS_PWD_SQL` stores a plaintext password column. `cognito_username` is returned by a query constant and populated into `DriverBean` objects in several methods. Swallowed exceptions and resource leaks occur in `revokeDriverAccessOnTrainingExpiry`. The `getAllUserSearch` method appends column aliases that do not exist in the base `QUERY_USER_BY_COMP` query, causing a latent runtime SQL error.

---

## Findings

---

### CRITICAL: SQL Injection via `timezone` Parameter in `getTotalDriverByID`
**File:** DriverDAO.java (lines 748–749)
**Description:**
`getTotalDriverByID(String id, boolean status, String timezone)` builds its SQL string by directly concatenating both `id` and `timezone` without parameterisation:

```java
String sql = "select count(p.id) from permission as p inner join driver as d on p.driver_id = d.id "
        + "where p.comp_id = " + id + " and timezone('"+timezone+"', p.updatedat)::DATE  = current_date::DATE  ";
```

`id` is a raw String (type not enforced) and `timezone` is a free-form string. Both are passed to `conn.createStatement()` then `stmt.executeQuery(sql)`.

**Call chain:** `AdminMenuAction.execute()` (line 66) reads `timezone` from `session.getAttribute("sessTimezone")` and passes it directly. `CompanySessionSwitcher.UpdateCompanySessionAttributes()` (line 37) does the same. `sessTimezone` is set from `TimezoneDAO.getTimezone()` on login and on company switch — but an authenticated user who can manipulate the company-switch flow, or whose session has been tampered with, can inject arbitrary SQL into the timezone argument. Because the database driver is PostgreSQL and the injection site is inside a function call string literal, payloads such as `UTC'); DROP TABLE driver;--` are syntactically plausible.

**Risk:** Authenticated SQL injection enabling data exfiltration, mutation, or destruction. Although `sessTimezone` is populated from the DB at login, the value is a mutable session attribute readable and (in theory) injectable via the company-switcher or any path that writes `sessTimezone` without further validation.

**Recommendation:** Replace `Statement` + concatenation with `PreparedStatement`. PostgreSQL's `timezone()` function can be parameterised: use `timezone(?, p.updatedat)` and bind the timezone string as a `setString` parameter. Validate `id` as a numeric Long before use.

---

### CRITICAL: SQL Injection via `timezone` in `getAllDriverSearch`
**File:** DriverDAO.java (lines 357–358)
**Description:**
When `search.equalsIgnoreCase("current_date")` is true, the method appends:

```java
builder.append(" and timezone('"+timezone+"', p.updatedat)::DATE = current_date::DATE  ");
```

`timezone` is the `sessTimezone` session attribute (passed through `AdminOperatorAction.searchAction()` at line 156). The query is then executed via `DBUtil.queryForObjects` which uses a `PreparedStatement`, but the SQL string is already tainted before it is handed to `queryForObjects`. A `PreparedStatement` provides no protection against injection that has already been baked into the SQL string before `prepareStatement()` is called.

**Risk:** Same as above — authenticated SQL injection. The trigger condition (`search == "current_date"`) is easily satisfied by a legitimate UI option (filtering drivers updated today).

**Recommendation:** Parameterise the timezone argument or validate it against a strict allowlist of IANA timezone identifiers (e.g., using `java.time.ZoneId.of()` to validate before using in SQL).

---

### CRITICAL: SQL Injection via `firstName`, `lastName`, `compId` in `getDriverByNm`
**File:** DriverDAO.java (lines 225–233)
**Description:**
The method builds SQL using raw string concatenation of all three caller-supplied arguments and executes via a raw `Statement`:

```java
String sql = "select id,first_name,last_name,active,comp_id from driver where trim(both ' ' from first_name) ilike trim(both ' ' from '" + firstName + "')  "
        + " and trim(both ' ' from last_name) ilike trim(both ' ' from '" + lastName + "')"
        + " and comp_id = " + compId;
```

The developer left a `// FIXME` comment explicitly acknowledging the injection risk. `firstName` and `lastName` arrive from `RegisterAction` (user-submitted form input). Single-quote injection in a name field (e.g., `O'Brien`) will corrupt the query structure; a crafted payload will allow arbitrary SQL execution.

**Risk:** Unauthenticated (pre-login) SQL injection if `RegisterAction` is accessible without a session check, or authenticated injection through the operator-edit form.

**Recommendation:** Replace with `PreparedStatement` using the existing parameterised constant `QUERY_DRIVER_BY_NAME` that is already defined at line 79 and used correctly by `checkDriverByNm`.

---

### CRITICAL: SQL Injection via `fullName`, `compId` in `getDriverByFullNm`
**File:** DriverDAO.java (lines 263–268)
**Description:**
Same pattern as `getDriverByNm`:

```java
String sql = "select id,first_name,last_name,active,comp_id,licno from driver where first_name||' '||last_name ilike '" + fullName + "' and comp_id = " + compId;
```

`fullName` is passed directly from `SearchAction` (line 50), which reads it from a submitted form field. The developer `FIXME` comment is present here as well.

**Risk:** Authenticated SQL injection through the search form.

**Recommendation:** Use `PreparedStatement` with `? ` bind parameter for `fullName`.

---

### HIGH: SQL Injection via `id` (Long) in `getDriverName`
**File:** DriverDAO.java (lines 783–785)
**Description:**

```java
String sql = "select first_name||' '||last_name as name from driver where id=" + id;
```

`id` is typed as `Long` in the method signature, so numeric injection is not directly possible from this method's own signature. However, the method is called from `PreFlightReport.getDriverName(Long driverId)` and `FleetCheckPDF`, where `driverId` originates from a database result set. The practice of concatenating any value into SQL is architecturally dangerous: a type change (e.g., refactoring to String), an autoboxing edge case, or future callers passing attacker-controlled longs would immediately introduce injection. The use of `Statement` (not `PreparedStatement`) and concatenation is the structural defect.

**Risk:** Currently low direct injection risk due to Long type enforcement, but HIGH risk from the structural anti-pattern and proximity to injection-vulnerable peer methods.

**Recommendation:** Replace with `PreparedStatement` and `stmt.setLong(1, id)`.

---

### HIGH: IDOR — `getDriverById` Does Not Scope to Session Company
**File:** DriverDAO.java (lines 154–157, 419–446)
**Description:**
`QUERY_DRIVER_BY_ID` filters only on `d.id`:

```sql
select d.id, d.first_name, d.last_name, p.location, p.department, d.phone, p.enabled, d.email,'******'
from driver d inner join permission p on d.id = p.driver_id
where d.id = ?
```

There is no `AND p.comp_id = ?` clause. Any authenticated admin who knows (or guesses) a driver ID belonging to a different company can retrieve that driver's name, phone, email, location, department, and access status by supplying an arbitrary `driverId` to `AdminOperatorAction` (line 64) or `AdminDriverEditAction` (line 56, 131, 184).

**Risk:** Cross-tenant data leakage. An admin of Company A can enumerate and read PII records belonging to Company B drivers.

**Recommendation:** Add `AND p.comp_id = ?` to `QUERY_DRIVER_BY_ID` and pass `sessCompId` as a second bind parameter at all call sites.

---

### HIGH: IDOR — `updateGeneralInfo` Does Not Scope UPDATE to Session Company
**File:** DriverDAO.java (lines 577–601)
**Description:**
`UPDATE_GENERAL_INFO_SQL` (line 52) and `UPDATE_ACCESS_PWD_SQL` / `UPDATE_ACCESS_EMAIL_SQL` all filter only by `id`:

```sql
update driver set first_name = ?, last_name = ?, phone = ? where id = ?
update driver set email = ?, password = ? where id = ?
```

No `comp_id` constraint is applied. An authenticated admin who submits an arbitrary driver ID (e.g., from another company) via the edit form will successfully overwrite that driver's PII and credentials.

**Risk:** Cross-tenant data modification. Company A admin can modify or reset the password of a Company B driver.

**Recommendation:** Add `AND id IN (SELECT driver_id FROM permission WHERE comp_id = ?)` or join back to `permission` with a company check in all UPDATE statements for driver records.

---

### HIGH: IDOR — `updateDriverLicenceInfo` Does Not Scope to Session Company
**File:** DriverDAO.java (lines 630–647)
**Description:**
`UPDATE_DRIVER_LICENSE_SQL` at line 50:

```sql
update driver set licno = ?, expirydt = ?, securityno = ?, addr = ? where id = ?
```

Filters only by driver `id`. A cross-company driver ID will be updated without restriction.

**Risk:** Same cross-tenant write vulnerability as above; allows modification of licence/security number on any driver.

**Recommendation:** Same as above — add company-scoped constraint.

---

### HIGH: IDOR — `delDriverById` Accepts `comp_id` from Caller Without Session Validation
**File:** DriverDAO.java (lines 690–700)
**Description:**
`DELETE_DRIVER_BY_ID` uses both `driver_id` and `comp_id` (line 60), which is correct structurally. However, both values are accepted as method parameters from the caller without any enforcement that `comp_id` matches the session. `AdminOperatorAction.deleteAction()` passes `sessCompId` as the second argument, which is session-sourced and therefore trusted. The DAO itself provides no defence-in-depth — a future caller could pass a mismatched `comp_id`. This is a lower-severity IDOR risk compared to the read/update findings above, but noteworthy.

**Risk:** Medium — the DAO is one refactor away from cross-tenant soft-delete. Currently mitigated by the calling action using `sessCompId`.

**Recommendation:** Document the contract that `comp_id` must come from the session. Consider adding an assertion or service-layer check.

---

### HIGH: Weak Password Hashing (MD5) in `addDriverInfo`
**File:** DriverDAO.java (lines 511–512)
**Description:**
New driver accounts are created with:

```java
stmt = conn.prepareStatement("insert into driver(...,password) values (...,md5(?)) RETURNING id");
```

MD5 is a general-purpose hash algorithm; it is not a password hashing function. MD5 passwords can be cracked via precomputed rainbow tables in seconds. There is no salt. Furthermore, `UPDATE_ACCESS_PWD_SQL` (line 46) writes a `password` column directly, and the caller in `updateGeneralInfo` (line 588) passes the raw `driverbean.getPass()` value with no explicit hashing — meaning update paths may store plaintext passwords.

**Risk:** If the `driver` table is compromised, all driver passwords are recoverable. The mismatch between insert (MD5) and update (possibly plaintext) paths compounds the risk.

**Recommendation:** Use a proper password hashing library (BCrypt, Argon2, or PBKDF2). Apply hashing uniformly in a service layer before any value reaches the DAO. Audit the update path to confirm whether passwords are pre-hashed before `UPDATE_ACCESS_PWD_SQL`.

---

### MEDIUM: `cognito_username` Exposed via `getAllUser` / `getUserById`
**File:** DriverDAO.java (lines 71–74, 159–160, 315–348, 449–477)
**Description:**
`QUERY_USER_BY_COMP` (line 71) selects `c.cognito_username` from `users_cognito`. `getAllUser()` builds a list of `DriverBean` objects each containing a `cognito_username`. `getUserById()` returns a `DriverBean` with `cognito_username` set. These beans are placed in request attributes and forwarded to JSP templates for rendering. `cognito_username` is also used as a Cognito API key to trigger password reset, user update, and deletion operations. If the JSP inadvertently renders it to the browser (e.g., in a hidden field or debug dump), an attacker could use it to interact with the Cognito admin API.

**Risk:** If `cognito_username` leaks to the client, an attacker may be able to invoke Cognito operations against any user identity without knowing internal IDs.

**Recommendation:** Strip `cognito_username` from `DriverBean` before it is added to request attributes destined for JSP rendering. Use a separate DTO that only contains display-safe fields.

---

### MEDIUM: `getAllUserSearch` References Invalid Column Aliases Causing Runtime SQL Error
**File:** DriverDAO.java (lines 394–417)
**Description:**
`getAllUserSearch` builds its query by appending to `QUERY_USER_BY_COMP`, which selects only `c.user_id` and `c.cognito_username` from `users_cognito` joined to `user_comp_rel`. The appended WHERE clause references columns `d.first_name`, `d.last_name`, `d.email`, and `d.mobile` — but there is no `driver` table alias `d` in the base query. Additionally, the trailing `ORDER BY first_name, last_name` references columns that do not exist in the projection. This will produce a SQL error at runtime whenever a non-blank search string is provided to the user-search flow.

**Risk:** The user-search feature is broken and will throw a `SQLException` at runtime, potentially exposing a stack trace to the caller if exception handling propagates it. No direct security injection risk from this bug, but the broken code masks the intent and may have been introduced while copying from `getAllDriverSearch`.

**Recommendation:** Correct the base query to include the `users` or `driver` table, or fix the column references. Confirm intended data source for user search.

---

### MEDIUM: `updateEmailSubsInfo` — Connection Not Rolled Back on Error
**File:** DriverDAO.java (lines 649–688)
**Description:**
`updateEmailSubsInfo` obtains a connection via `DBUtil.getConnection()` (auto-commit behaviour unclear — likely auto-commit ON by default). The method performs two sequential operations: a `count` query followed by either an `INSERT` or an `UPDATE`. If the second operation fails after the first has succeeded in a non-auto-commit context, there is no `conn.rollback()` call in the catch block — only `throw new SQLException(e.getMessage())`. The original exception's cause chain is also lost because `new SQLException(e.getMessage())` discards the original `Throwable`.

**Risk:** Partial state corruption if the connection is transactional; loss of diagnostic information from the discarded original exception stack trace.

**Recommendation:** Add `if (conn != null) conn.rollback()` to the catch block. Preserve the original exception: `throw new SQLException(e.getMessage(), e)`.

---

### MEDIUM: IDOR — `getSubscriptionByDriverId` Does Not Scope to Company
**File:** DriverDAO.java (lines 480–500)
**Description:**
`QUERY_DRIVER_EMAILS_BY_DRIVER_ID` (line 162) selects email subscription addresses purely by `driver_id` with no company check. A caller that supplies a driver ID belonging to another company will retrieve that driver's alert email addresses.

**Risk:** Cross-tenant information disclosure of email addresses registered for alert subscriptions.

**Recommendation:** Add a `comp_id` join/filter if the subscription is company-scoped, or verify that `driver_id` is validated against the session company before calling this method.

---

### LOW: `revokeDriverAccessOnTrainingExpiry` — Swallowed Exception via `printStackTrace`
**File:** DriverDAO.java (lines 902–918)
**Description:**
Inside the `forEach` lambda, the `SQLException` from `DBUtil.updateObject` is caught and printed to stderr via `e.printStackTrace()` rather than logged or rethrown:

```java
} catch (SQLException e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
}
```

The `TODO` comment confirms this is a known stub. If a batch revocation operation fails mid-loop, processing silently continues, the error is only printed to stderr (not the application log), and the caller receives no indication that some records were not revoked.

**Risk:** Silent partial failure of a security-critical operation (revoking access on training expiry). Drivers whose access should have been revoked may retain forklift access.

**Recommendation:** Log the exception at ERROR level using the class logger. Collect failures and rethrow or alert after the loop completes.

---

### LOW: Resource Leak — `ResultSet` Not Closed in `getTotalDriverByID`
**File:** DriverDAO.java (lines 735–762)
**Description:**
`ResultSet rs` is declared but not passed to `DbUtils.closeQuietly()` in the `finally` block (line 761 passes `null` for the RS argument):

```java
} finally {
    DbUtils.closeQuietly(conn, stmt, null);  // rs is never closed
}
```

The local `rs` variable is assigned inside the `try` block but will not be closed if the method returns normally (the `return total` at line 756 exits before `finally`). The same pattern exists in `getDriverName` (line 793) where `rs` is also local and not passed to `closeQuietly`.

**Risk:** Under high load, unclosed `ResultSet` objects consume database cursor resources and may cause cursor exhaustion.

**Recommendation:** Declare `rs` at the top of the method (as `null`), and pass it to `DbUtils.closeQuietly(conn, stmt, rs)` in the `finally` block. Alternatively, refactor to use the `DBUtil.queryForObject` abstraction already used elsewhere.

---

### LOW: Static Singleton Pattern is Not Thread-Safe for Lazy Init (Minor)
**File:** DriverDAO.java (lines 168–174)
**Description:**
The `getInstance()` method is `synchronized` on the class method lock, which is correct. However, `instance` is a plain non-`volatile` static field. Under the Java Memory Model, a thread could observe a partially constructed instance even with the `synchronized` keyword if the JVM or CPU reorders writes. The idiomatic fix is to declare `private static volatile DriverDAO instance`.

**Risk:** Very low in practice on modern JVMs, but technically a visibility hazard in a multi-threaded servlet container.

**Recommendation:** Declare `instance` as `volatile`, or use the initialization-on-demand holder idiom.

---

### INFO: Developer-Acknowledged `FIXME` Comments on SQL Injection
**File:** DriverDAO.java (lines 225, 263)
**Description:**
Both `getDriverByNm` and `getDriverByFullNm` contain the comment:

```
// FIXME Use string constant to avoid to re-instantiating new string at every call. Also work with prepared statement to prevent SQL injection.
```

The injection risk was known to the development team but was not remediated. This suggests a pattern of deferred security fixes that may be present elsewhere in the codebase.

**Risk:** Informational — the FIXME comments confirm the issues are known and unresolved.

**Recommendation:** Treat FIXME/TODO security notes as defect backlog items with severity assignments and remediation deadlines.

---

### INFO: Logged SQL Query Contains User Input (Information Disclosure via Logs)
**File:** DriverDAO.java (lines 232, 268, 752, 784)
**Description:**
Several methods call `log.info(sql)` or `log.debug(sql)` after constructing a SQL string that includes user-supplied input (first name, last name, full name, timezone). If log files are accessible to lower-privileged staff or stored insecurely, this leaks the exact user input (including any injection payloads) into application logs.

**Risk:** Log injection and information leakage. A malicious actor who can read logs can confirm whether an injection attempt succeeded and refine payloads.

**Recommendation:** Do not log composed SQL strings that contain user input. Use parameterised logging at DEBUG level that omits the raw parameter values, or log only the query template (without values).

---

## Finding Count
- CRITICAL: 4
- HIGH: 5
- MEDIUM: 4
- LOW: 3
- INFO: 2
