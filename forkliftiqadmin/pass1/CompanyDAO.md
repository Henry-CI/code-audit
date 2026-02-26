# Pass 1 Audit — CompanyDAO
**File:** src/main/java/com/dao/CompanyDAO.java
**Date:** 2026-02-26

## Summary

`CompanyDAO` is the central data-access object for company, user, entity, alert, and subscription
operations in the ForkliftIQ admin application. It is a manually managed singleton with 40+ public
methods touching at least seven database tables (`company`, `users`, `entity`, `subscription`,
`user_subscription`, `permission`, `company_rel`). It also calls an external Cognito REST API for
user management.

Overall risk level: **CRITICAL**. The file contains multiple unauthenticated SQL injection vectors,
systematic sensitive-data exposure (hashed passwords, security Q&A, PIN returned to callers),
IDOR vulnerabilities caused by accepting caller-supplied IDs without session binding, swallowed
exceptions in `DBUtil` that cause the DAO to silently return empty/default results on database
failure, and one resource leak.

---

## Findings

---

### CRITICAL: SQL Injection — checkExist (column name and value both injectable)
**File:** CompanyDAO.java (lines 367–370)
**Description:**
`checkExist` accepts three caller-supplied strings: `name` (the value to search for), `dbField`
(the database column name), and `compId` (a record ID to exclude). Both `dbField` and `name` are
interpolated directly into the SQL string via concatenation, with no parameterisation and no
whitelist validation on `dbField`:

```java
String sql = "select id from company where " + dbField + " ='" + name + "'";
if (!compId.equalsIgnoreCase("")) {
    sql += " and id != " + compId;
}
```

`dbField` is a second-order injection point that bypasses quote-based defences entirely; an
attacker can inject arbitrary SQL keywords and sub-queries at the column-name position (e.g.
`1=1 UNION SELECT ...`). `name` is single-quote wrapped but trivially escaped with `'`. `compId`
is appended numerically without quotes, making it a clean numeric injection vector.

A `Statement` (not `PreparedStatement`) executes the constructed string.

**Risk:** Full SQL injection. Authentication bypass, data exfiltration of the entire `company`
table (including hashed passwords, PINs, security questions and answers), and potentially
destructive write operations depending on database-user privileges.
**Recommendation:** Replace with a `PreparedStatement`. Validate `dbField` against an explicit
whitelist of allowable column names before use. Use `?` placeholder for `name`. Parse `compId` to
an integer before use and pass via a bound parameter.

---

### CRITICAL: SQL Injection — checkUserExit (column name and value both injectable)
**File:** CompanyDAO.java (lines 385–393)
**Description:**
`checkUserExit` mirrors the same pattern as `checkExist` against the `users` table. The
constructed SQL string (with concatenated `dbField`, `name`, and numeric `id`) is then passed as a
raw SQL string directly to `DBUtil.queryForObject(String, ResultMapper)` — the two-argument
overload that accepts a pre-built string with no `PreparedStatement` binding at all:

```java
String sql = "select id from users where " + dbField + " ='" + name + "'";
if (!id.equalsIgnoreCase("")) {
    sql += " and id != " + id;
}
return DBUtil.queryForObject(sql, (rs) -> rs.getInt(1)).orElse(0);
```

Both the column name (`dbField`) and the search value (`name`) are fully injectable. The `id`
exclusion term is a bare numeric concatenation.

**Risk:** Full SQL injection against the `users` table. Can be used to exfiltrate user records,
circumvent duplicate-check logic, or — given the permissive DBUtil error handling — cause silent
failures that a caller may interpret as "no conflict found", allowing duplicate or privileged
accounts to be created.
**Recommendation:** Whitelist `dbField`. Use a three-argument `DBUtil.queryForObject` call with a
`PreparedStatementHandler` to bind `name` and `id` as parameters.

---

### CRITICAL: SQL Injection — checkCompExist (four concatenated fields)
**File:** CompanyDAO.java (lines 408–418)
**Description:**
Four fields from a `CompanyBean` are concatenated directly into SQL:

```java
String sql = "select id from company where name = '" + companyBean.getName()
    + "' and email = '" + companyBean.getEmail() + "'";
if (!companyBean.getQuestion().equalsIgnoreCase("")) {
    sql += " and question ilike '" + companyBean.getQuestion() + "'";
} else { ... }
if (!companyBean.getAnswer().equalsIgnoreCase("")) {
    sql += " and answer = '" + companyBean.getAnswer() + "'";
} else { ... }
```

`name`, `email`, `question`, and `answer` all originate from HTTP form input and are not sanitised.
A `Statement` (not `PreparedStatement`) executes the result. The `ilike` operator on `question`
additionally makes wildcards (`%`, `_`) effective against this column.

**Risk:** Full SQL injection. This method is likely reachable at the company registration or
password-reset flow, making it a pre-authentication injection point.
**Recommendation:** Replace with a `PreparedStatement` using `?` for all four values.

---

### CRITICAL: SQL Injection — getCompLogo (numeric string concatenation)
**File:** CompanyDAO.java (lines 471–472)
**Description:**
`compId` is a caller-supplied string interpolated directly into SQL without any numeric validation:

```java
String sql = "select logo from company where id = " + compId + "";
```

If `compId` originates from a session attribute it carries partial trust, but the method is
`public` and the parameter type is `String`. There is no `parseInt` guard. A caller passing
`1 OR 1=1` or a UNION payload retrieves arbitrary data.

**Risk:** SQL injection yielding data from the `company` table (or joined tables). The method is
also called from `FleetCheckAlert.java` (line 45) where `compId` comes from a job parameter,
potentially widening the attack surface.
**Recommendation:** Parse `compId` to an integer before use and use a `PreparedStatement` with a
bound parameter.

---

### CRITICAL: SQL Injection — getEntityComp (entityId concatenated numerically)
**File:** CompanyDAO.java (lines 669–670)
**Description:**
`entityId` is appended to SQL without parsing or binding:

```java
if (!entityId.equalsIgnoreCase("1")) {
    sql += " where comp_entity_rel.entity_id = " + entityId;
}
```

Additionally, when `entityId` equals the string `"1"` the `WHERE` clause is omitted entirely,
returning every company record to the caller — this is a logic flaw independent of injection.

A `Statement` executes the result.

**Risk:** SQL injection against the `company` table. The special-case "1 returns all" behaviour is
also an unintended information disclosure path.
**Recommendation:** Parse `entityId` to an integer, use `PreparedStatement`. Evaluate whether the
"entity 1 returns everything" bypass is intentional; if not, add an explicit `WHERE` for all
inputs.

---

### CRITICAL: SQL Injection — getEntityByQuestion (two concatenated values)
**File:** CompanyDAO.java (lines 702–703)
**Description:**
Both `qId` (numeric) and `type` (string) are concatenated into SQL executed via `Statement`:

```java
String sql = "select entity.id,name, email from entity, form_library "
    + "where entity.id = form_library.lock_entity_id "
    + "and question_id = " + qId
    + " and type= '" + type + "'";
```

`qId` is a bare numeric concatenation; `type` is single-quote wrapped but trivially escapable.

**Risk:** SQL injection against `entity` and `form_library` tables.
**Recommendation:** Use `PreparedStatement` with bound `?` parameters for both `qId` and `type`.

---

### CRITICAL: SQL Injection — getAllEntity (inner loop concatenation)
**File:** CompanyDAO.java (lines 745–747)
**Description:**
Inside the result-set loop of `getAllEntity`, the string value from the outer query is concatenated
directly into a second SQL query executed on a second `Statement`:

```java
sql = "select roles.id,name,description from roles,entity_role_rel "
    + "where roles.id = entity_role_rel.role_id and entity_id = " + rs.getString(1);
rst = stm.executeQuery(sql);
```

Although `rs.getString(1)` is a database-sourced value (the entity `id`), using it in a string
concatenation and re-executing it as SQL is still a second-order SQL injection pattern. If any
process can write a crafted value into `entity.id`, it will be executed.

**Risk:** Second-order SQL injection. Even without attacker-controlled input today, the pattern
establishes a fragile dependency on the data layer being clean.
**Recommendation:** Use a `PreparedStatement` in the inner loop. Alternatively, use a single JOIN
query.

---

### HIGH: Sensitive Data Exposure — password and PIN returned in CompanyBean
**File:** CompanyDAO.java (lines 81–85, 75–79, 187–188, 498–499, 533–534)
**Description:**
`QUERY_COMPANY_BY_ID` and `QUERY_SUBCOMPANYLST_BY_ID` both `SELECT` the `password` and `pin`
columns and map them into `CompanyBean.password` and `CompanyBean.pin`. Methods `getCompanyById`,
`getCompanyByCompId`, and `getSubCompanies` all return fully populated `CompanyBean` objects
carrying these hashed credentials to their callers:

```sql
select c.name, c.address, c.postcode, c.password, c.pin, ...
```

```java
.password(rs.getString(4))
.pin(rs.getString(5))
```

If any Action class serialises this bean to JSON, writes it to a JSP attribute, or logs it, the
hashed password and PIN are exposed to the browser tier or log files.

**Risk:** Credential hash exposure. MD5-hashed passwords are trivially crackable with modern
GPU-based tools. PINs are typically short numeric values and even easier to reverse. If the bean
is ever returned as an API response body, the impact escalates to direct credential disclosure.
**Recommendation:** Define a separate read-only projection bean or DTO for display purposes that
excludes `password` and `pin`. Remove those columns from all `SELECT *` queries used in non-admin
flows. Where the hash is genuinely needed (e.g., a verification check), perform the comparison in
the DAO and return a boolean, never the hash.

---

### HIGH: Sensitive Data Exposure — security question and answer returned in CompanyBean
**File:** CompanyDAO.java (lines 82–84, 75–78, 498–500, 533–535)
**Description:**
`QUERY_COMPANY_BY_ID` and `QUERY_SUBCOMPANYLST_BY_ID` both `SELECT` the `question` and `answer`
columns and populate `CompanyBean.question` and `CompanyBean.answer`. The answer to a security
question is effectively a secondary credential. It is stored in plain text (no hashing) and
returned in full to the caller.

**Risk:** Plain-text security-answer exposure. If the bean reaches a view layer or is serialised
to a client, the password-reset secret is directly disclosed. Because `checkCompExist` accepts
these values as input and compares them to stored rows, an attacker with the injection vector
found there can also exfiltrate all answers.
**Recommendation:** Never return the plain-text answer outside the DAO. If a comparison is needed,
perform it server-side. Consider hashing security answers at rest.

---

### HIGH: Sensitive Data Exposure — entity password returned in getAllEntity
**File:** CompanyDAO.java (lines 737–742)
**Description:**
`getAllEntity` executes `select id,name,email,password from entity order by name` and populates the
result into `EntityBean` objects. Although `EntityBean.password` is not populated in the result
loop (lines 740–758 only call `setId`, `setName`, `setEmail`), the column is still fetched from
the database and held in the `ResultSet` in memory. More importantly, the query itself is
unnecessarily wide — the `password` column has no legitimate use in a method that is retrieving
entity display information.

**Risk:** Unnecessary retrieval of credential data; any future code change that adds
`entityBean.setPassword(rs.getString(4))` would silently introduce full exposure. The column
fetch also widens the data footprint unnecessarily.
**Recommendation:** Remove `password` from the `SELECT` list in `getAllEntity`.

---

### HIGH: IDOR — getCompanyById and getCompanyByCompId accept arbitrary companyId
**File:** CompanyDAO.java (lines 488–519, 521–556)
**Description:**
Both `getCompanyById` and `getCompanyByCompId` accept a `companyId` / `id` string from the caller
and query the `company` table directly without verifying that the requested company belongs to or
is reachable from the authenticated user's session company. No JOIN to `company_rel` or comparison
to a session-scoped `sessCompId` is performed.

If a Struts Action calls `CompanyDAO.getCompanyById(form.getCompanyId())` where `form.getCompanyId()`
originates from a request parameter, any authenticated user can retrieve any company's data —
including its hashed password, PIN, and security answer — by iterating numeric IDs.

**Risk:** Insecure Direct Object Reference. Full horizontal privilege escalation across all
companies in the database.
**Recommendation:** Pass the session's `sessCompId` as an additional parameter and add a
`WHERE c.id = ? AND (c.id = :sessCompId OR EXISTS (SELECT 1 FROM company_rel WHERE ...))` scope
guard, or verify the returned company's ID is in the caller's reachable set before returning.

---

### HIGH: IDOR — getSubCompanies accepts arbitrary companyId
**File:** CompanyDAO.java (lines 177–199)
**Description:**
`getSubCompanies(String companyId)` returns the full list of sub-companies (with password, PIN,
question, and answer fields) for any `companyId` passed in. There is no check that `companyId`
equals the session's `sessCompId` or a parent thereof. A static method, it can also be called
from any context.

**Risk:** Horizontal IDOR — any authenticated user can enumerate all sub-companies of any company.
The returned beans also carry credential fields (see sensitive-data finding above), so this is
also a credential enumeration vector.
**Recommendation:** Enforce that the requested `companyId` matches the session company or is
explicitly accessible to the calling user.

---

### HIGH: IDOR — addUserSubscription and deleteUserSubscription accept arbitrary userId
**File:** CompanyDAO.java (lines 862–878)
**Description:**
Both static methods accept `userId` and `alertId` as caller-supplied strings and execute
`INSERT`/`DELETE` against `user_subscription` without verifying that the specified `userId`
belongs to the authenticated session:

```java
public static void addUserSubscription(String userId, String alertId) throws Exception {
    DBUtil.updateObject("insert into user_subscription(user_id, subscription_id) values(?, ?)", stmt -> {
        stmt.setInt(1, Integer.parseInt(userId));
        stmt.setInt(2, Integer.parseInt(alertId));
    });
}
```

An attacker can subscribe or unsubscribe any user to any alert by supplying an arbitrary `userId`.

**Risk:** Privilege escalation / account manipulation. An attacker can silence alerting for other
users or add spurious subscriptions.
**Recommendation:** Require that `userId` be bound to the session's `sessUserId` inside the DAO or
the calling Action, and reject any request where the two differ.

---

### MEDIUM: MD5 Used for Password Hashing
**File:** CompanyDAO.java (lines 61, 95, 443)
**Description:**
Three SQL statements hash passwords using PostgreSQL's `md5()` function:

```sql
INSERT INTO users (id, email, password, ...) values (?,?,md5(?),?,?,?)
update users set password = md5(?)  where id = ?
update company set password = md5(?) where id = ?
```

MD5 is a fast, cryptographically broken hash. It provides no salting and is trivially reversible
via rainbow tables or GPU brute-force. Common passwords (including short PINs) can be reversed in
milliseconds.

**Risk:** All stored passwords are effectively recoverable from the database if an attacker obtains
the hash values (which multiple other findings in this audit facilitate).
**Recommendation:** Use a slow, salted password hashing algorithm: `bcrypt`, `scrypt`, or
`argon2`. Migrate existing MD5 hashes on next login.

---

### MEDIUM: Swallowed Exceptions in DBUtil — Silent Failure Masks Errors
**File:** src/main/java/com/util/DBUtil.java (lines 75–77, 98–100, 119–121, 140–142, 164–166, 204–206, 221–223)
**Description:**
Every `queryForObjects`, `queryForObject`, and `updateObject` method in `DBUtil` catches
`SQLException`, prints a stack trace (`e.printStackTrace()`), and then **continues execution**,
returning an empty list, `Optional.empty()`, or `-1` to the caller. The exception is not
re-thrown.

```java
} catch (SQLException e) {
    e.printStackTrace();   // stack trace to stderr only
}
return results;            // returns empty list — caller cannot distinguish failure from "no rows"
```

In `CompanyDAO`, methods such as `getCompanyById` then call `results.get(0)` (line 518) on what
may be an empty list returned from a silent database error, causing a secondary
`IndexOutOfBoundsException` that does propagate but with a misleading root cause.

Critically, `checkExist` and `checkUserExit` return `false` / `0` on database failure —
indicating "no conflict found" when the database was unreachable — allowing duplicate records or
invalid operations to proceed silently.

**Risk:** Incorrect security decisions based on failed queries that appear to succeed. Database
errors are invisible to monitoring (stderr only, no log framework). Logic that relies on a count
of zero or an empty list to gate an operation will produce the wrong outcome under failure
conditions.
**Recommendation:** Re-throw the `SQLException` from all `DBUtil` catch blocks (or wrap and
re-throw as a runtime exception). Use the application's logging framework (`log.error(...)`)
rather than `e.printStackTrace()`. Never swallow exceptions in security-sensitive query paths.

---

### MEDIUM: e.printStackTrace() Used Instead of Structured Logging
**File:** CompanyDAO.java (lines 622, 648); DBUtil.java (multiple)
**Description:**
In `updateCompInfo` and `updateCompSettings`, caught exceptions are written to stderr via
`e.printStackTrace()` before being re-thrown. `DBUtil` uses the same pattern. In a containerised
or application-server environment, stderr may not be captured by the log aggregation pipeline,
making these failures invisible to security monitoring and alerting.

**Risk:** Security-relevant exceptions (failed authentication updates, failed credential changes)
are not observable through the application's normal logging infrastructure.
**Recommendation:** Replace all `e.printStackTrace()` calls with `log.error("context message", e)`.

---

### MEDIUM: updateCompSettings Accepts companyId from the Bean (No Session Binding)
**File:** CompanyDAO.java (lines 636–643)
**Description:**
`updateCompSettings` reads the target company ID directly from the caller-supplied `CompanyBean`:

```java
ps.setInt(4, Integer.parseInt(compBean.getId()));
```

If the Struts Action populating `compBean` does so from a request parameter (which is the standard
Struts form-bean pattern), an attacker can modify the `id` field to target any company.

**Risk:** IDOR / horizontal privilege escalation. An authenticated user at any company could
modify the settings (date format, max session length, timezone) of any other company.
**Recommendation:** Pass `sessCompId` from the session as a separate parameter and use it as the
WHERE key instead of `compBean.getId()`.

---

### LOW: SQL Logged at INFO Level Before Execution (Including Sensitive Values)
**File:** CompanyDAO.java (lines 371, 389, 420, 447, 471, 473, 703)
**Description:**
The constructed SQL strings — which contain the literal values of `name`, `email`, `question`,
`answer`, `pass`, `compId`, etc. — are written to the application log at `INFO` level
immediately before execution:

```java
log.info(sql);
```

For injection-vulnerable methods this means the injected payload itself is logged. For
`resetPass` and `checkCompExist`, sensitive values (names, emails, security answers) appear in
log files.

**Risk:** Credential and PII leakage into log files. Log files are frequently archived to less
secure storage, forwarded to third-party SIEM systems, or accessible to a wider group of
personnel than the database itself.
**Recommendation:** Log a static query identifier or the query template only, never the
parameterised values. For `PreparedStatement` usage the parameterised template is already safe to
log; remove `log.info(sql)` calls that include user data.

---

### LOW: Resource Leak — second Statement (stm) not closed on Connection in getAllEntity
**File:** CompanyDAO.java (lines 764–765)
**Description:**
`getAllEntity` opens two `Statement` objects (`stmt` and `stm`) and two `ResultSet` objects
(`rs` and `rst`). The `finally` block correctly closes each pair, but the two `DbUtils.closeQuietly`
calls use separate invocations and pass `null` for the connection in the first call:

```java
DbUtils.closeQuietly(null, stm, rst);   // conn is null — connection NOT closed here
DbUtils.closeQuietly(conn, stmt, rs);   // conn closed here
```

This is the correct pattern when sharing a single connection, so the connection itself is not
leaked. However, if an exception occurs after `stmt` is created but before `stm` is created,
`stm` is `null` and `rst` is `null` — both are handled safely by `closeQuietly`. The pattern is
fragile: if refactored to add a third statement the ordering must be maintained carefully.

**Risk:** Low under current code; the connection is closed. However, the pattern is brittle and
could yield a connection leak under future refactoring.
**Recommendation:** Refactor `getAllEntity` to use a single JOIN query, eliminating the need for
two concurrent statements entirely.

---

### LOW: Singleton Not Thread-Safe for Compound Operations
**File:** CompanyDAO.java (lines 109–115)
**Description:**
`getInstance()` uses a `synchronized` method for lazy initialisation, which is correct. However,
`getCompanyMaxId()` and `getUserMaxId()` fetch the next sequence value and then use it in a
subsequent independent database call. Between the two calls another thread could interleave and
consume the same ID (depending on sequence isolation). In practice PostgreSQL sequences are
session-scoped so this is low risk, but the DAO also increments a local variable (`compId`) and
shares it across two operations with no transactional boundary.

**Risk:** Low. Potential for duplicate-key errors under concurrent load rather than a direct
security impact.
**Recommendation:** Wrap `saveCompInfo` in a transaction, or use a `RETURNING` clause in the
INSERT to generate and return the ID atomically.

---

### LOW: Commented-Out Password Insert Leaves Dead Code with Security Implication
**File:** CompanyDAO.java (lines 247–254)
**Description:**
`SAVE_USERS` (line 61) and its corresponding `PreparedStatement` block (lines 247–254) are
commented out. The constant still declares the MD5 password insert:

```java
private static final String SAVE_USERS =
    "INSERT INTO users (id, email, password, first_name, last_name, mobile) values (?,?,md5(?),?,?,?) ";
```

The comment block is the only place where `SAVE_USERS` would be used, so the constant is dead
code. Its presence implies this path may be re-enabled in the future, which would reintroduce
MD5 password storage.

**Risk:** Low currently (code is commented out), but the dead constant creates confusion about
the intended authentication path and could be carelessly re-enabled.
**Recommendation:** Remove the dead constant and commented block entirely. Document the migration
to Cognito clearly in the source.

---

### INFO: Singleton Pattern — All Methods Operate on the Same Instance
**File:** CompanyDAO.java (lines 107–118)
**Description:**
`CompanyDAO` is a manually managed singleton. All instance methods share state only through
method parameters and local variables (there are no instance fields beyond the logger), so the
singleton itself does not introduce data races. This is noted for completeness.

**Risk:** Informational.

---

### INFO: UPDATE_USR_PIN Constant Defined but No Public Caller Found in This File
**File:** CompanyDAO.java (line 95)
**Description:**
`UPDATE_USR_PIN = "update users set password = md5(?) where id = ?"` is declared as a class
constant but is not referenced by any method within `CompanyDAO.java`. It may be used by another
class via reflection or it may be dead code. If it is dead code, remove it; if another class uses
it, review that usage for the same IDOR and MD5 concerns that apply elsewhere.

**Risk:** Informational / potential dead code.

---

## Finding Count
- CRITICAL: 7
- HIGH: 5
- MEDIUM: 4
- LOW: 4
- INFO: 2
