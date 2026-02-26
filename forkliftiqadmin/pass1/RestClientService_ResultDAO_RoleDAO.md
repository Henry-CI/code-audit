# Security Audit Report — Pass 1
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Date:** 2026-02-26
**Auditor:** Automated static analysis (Claude Code)
**Files Audited:**
- `src/main/java/com/service/RestClientService.java`
- `src/main/java/com/bean/ResultBean.java`
- `src/main/java/com/dao/ResultDAO.java`
- `src/main/java/com/bean/RoleBean.java`
- `src/main/java/com/dao/RoleDAO.java`

**Supporting context files read:**
- `src/main/java/com/action/FleetcheckAction.java`
- `src/main/java/com/action/AdminRegisterAction.java`
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`

---

## Findings

---

### CRITICAL: Cognito sidecar uses plain HTTP — credentials and tokens in cleartext

**File:** `RestClientService.java` (lines 53, 88, 123, 158, 192, 228, 265, 297)

**Description:**
Every method in `RestClientService` calls the local Cognito sidecar proxy over plain `http://`:

```java
// line 53
restTemplate.exchange("http://localhost:"+COGNITO_API_PORT+"/auth", HttpMethod.POST, entity, AuthenticationResponse.class);

// line 88
restTemplate.exchange("http://localhost:"+COGNITO_API_PORT+"/auth/SignUp", HttpMethod.POST, entity, UserSignUpResponse.class);

// line 123
restTemplate.exchange("http://localhost:"+COGNITO_API_PORT+"/auth/ResetPassword", HttpMethod.POST, entity, PasswordResponse.class);

// line 297
String baseUrl = "http://localhost:"+COGNITO_API_PORT+"/auth/delete_user?accessToken="+sessionToken+"&email="+...;
```

Calls include authentication credentials (username/password for `authenticationRequest` and `signUpRequest`), access tokens, and password-reset confirmation codes — all transported over an unencrypted loopback connection.

While loopback traffic is not routed on the wire, using HTTP means:
1. Any local process running on the same host (including other Tomcat webapps, application log interceptors, or a compromised JVM agent) can observe the cleartext payload via `/proc` inspection, Java instrumentation, or a local proxy.
2. When the sidecar is moved to a separate container or host (a common containerisation migration step), the protocol will still be HTTP without any code change, creating an immediate plaintext-over-network vulnerability.
3. Session tokens and user passwords appear as unencrypted strings in thread-dump and heap snapshots.

**Risk:** Credential and token exposure to any co-resident process. Silent protocol downgrade when deployment topology changes. Applicable when this runs in a shared-server or container environment (Tomcat on AWS EC2/ECS).

**Recommendation:** Switch all URLs to `https://` and ensure the sidecar terminates TLS even on loopback. If mutual TLS is not feasible, enforce HTTPS at minimum and validate the sidecar certificate. The port should also be sourced from configuration (see finding below) so the scheme can be changed without recompilation.

---

### CRITICAL: SQL injection via unparameterised `question_id` in `saveResult`

**File:** `ResultDAO.java` (lines 65, 74, 91)

**Description:**
Inside the per-answer loop of `saveResult`, `answer.getQuesion_id()` — a value that originates directly from the HTTP request form field `id[]` in `FleetcheckActionForm` — is concatenated unsanitised into three separate SQL statements executed with a raw `Statement`:

```java
// line 65 — injected into SELECT
sql = "select content from question_content where lan_id = " + lanId
    + " and question_id = " + answer.getQuesion_id();
rs = stmt.executeQuery(sql);

// line 74 — injected into INSERT via inline string
sql = "insert into answer (...) select ?,?,?,'" + content + "',expectedanswer,answer_type,? from question where id = ?";
// note: 'content' here came from the DB but could itself carry injected data if line-65 was exploited

// line 91 — injected into SELECT
sql = "select answer_type.name from question,answer_type where question.id ="
    + answer.getQuesion_id()
    + " and question.answer_type = answer_type.id";
rs = stmt.executeQuery(sql);
```

In `FleetcheckAction.java` (lines 96, 125):
```java
String[] quesion_ids = fleetcheckActionForm.getId();   // from HTTP form post
...
answerBean.setQuesion_id(quesion_ids[i]);
```

An authenticated user (or a user of the mobile API path) can submit an arbitrary `id[]` value such as:
```
1 OR 1=1--
1; DROP TABLE answer--
1 UNION SELECT password,NULL,NULL,NULL FROM company--
```
The `parseInt` call at line 80 (`Integer.parseInt(answer.getQuesion_id())`) provides partial protection for the third positional bind parameter only — it will throw `NumberFormatException` if the value is not a plain integer. However this does NOT protect lines 65 and 91, because those execute the raw string before `parseInt` is reached. An attacker can supply `1` as the `parseInt`-consumed parameter while arranging for the raw-string uses on lines 65 and 91 to contain a crafted suffix (since the id array element is read multiple times from the same bean field on each loop iteration).

Additionally, lines 61 and 85/113 concatenate `result_id` (an integer from a DB sequence) into raw delete statements executed via `stmt.execute(sql)` — while `result_id` is itself not user-supplied, using a raw `Statement` for cleanup DML is a code quality risk if refactored.

**Risk:** Authenticated SQL injection enabling full database read/write/delete, potential remote code execution via PostgreSQL `COPY TO/FROM` or `pg_read_file`, and cross-tenant data exfiltration.

**Recommendation:** Replace all concatenated SQL in the loop with `PreparedStatement` using positional bind parameters for `lanId` and `question_id`. The `content` variable from line 67–75 should never be interpolated directly into SQL — use a bind parameter for it as well. Lines 65 and 91 must be converted first as they are the highest-risk sites.

---

### CRITICAL: SQL injection in `checkDuplicateResult` — String parameters concatenated directly

**File:** `ResultDAO.java` (lines 294–295)

**Description:**
`checkDuplicateResult` accepts `driverId` and `unitId` as `String` parameters and concatenates them directly into the WHERE clause using a raw `Statement`:

```java
String sql = "select count(id) from result "
    + " where driver_id= " + driverId
    + " and unit_id= " + unitId
    + " and timestamp = '" + time + "'";
stmt.executeQuery(sql);
```

The caller in `BarCodeAction.java` (line 212) passes `resultBean.getDriver_id().toString()` and `resultBean.getUnit_id()`, both of which originate from the mobile API request body. The `time` parameter is a `java.sql.Timestamp` cast from a user-supplied string via `DateUtil.stringToTimestamp`.

An attacker controlling the mobile API body (the `api.do` endpoint is **excluded from the `PreFlightActionServlet` auth check** — see `PreFlightActionServlet.java` line 106) can inject arbitrary SQL through these parameters. While the `api.do` handler body is largely commented out at the time of this audit, the method itself is public, called from other paths, and the exclusion from auth makes it a zero-authentication attack surface.

**Risk:** Unauthenticated SQL injection on the `api.do` endpoint path; authenticated injection on other callers.

**Recommendation:** Convert to `PreparedStatement` with bind parameters for all three values.

---

### HIGH: No `comp_id` isolation in `getChecklistResultById`, `getOverallStatus`, `printErrors`, and `getChecklistResultInc` — cross-tenant IDOR

**File:** `ResultDAO.java` (lines 179, 214–225, 258–260, 145)

**Description:**
Four query methods retrieve result/answer records using only the caller-supplied `resultId` or `driverId`, with no filter on `comp_id`:

```java
// getChecklistResultById — line 179
String sql = "select id,driver_id,comment,...,unit_id,location,odemeter from result where id=" + resultId;

// getOverallStatus — lines 214, 225
String sql = "select count(id) from answer where result_id = " + resultId;
sql = "select count(id) from answer where result_id= " + resultId + " and answer != expectedanswer ...";

// printErrors — lines 258–260
String sql = "select question_text, answer, faulty from answer where result_id= " + resultId + " ...";

// getChecklistResultInc — line 145
String sql = "select ... from result where driver_id = " + driverId + " and timestamp >= ...";
```

None of these queries join to or filter on a `comp_id` column. An authenticated user from Company A can supply a `resultId` belonging to Company B (any integer, guessable by enumeration) and retrieve that company's inspection records, driver comments, odometer readings, and pass/fail status. The `sessCompId` is present in session and passed to `saveResult`, but is never passed to or used by any of the read methods.

**Risk:** Complete cross-tenant data exposure (IDOR). Every authenticated user can read inspection results, location data, and equipment defect details belonging to any other company in the system.

**Recommendation:** Add a `comp_id` join or subquery to each of these queries. For `result`-table queries, join through `unit` or `driver` to the `company` table and filter `company.id = ?` with the session `sessCompId`. Pass `compId` as a parameter to each method.

---

### HIGH: SQL injection via `driverId` and date parameters in `getChecklistResultInc`

**File:** `ResultDAO.java` (lines 145–146)

**Description:**
`getChecklistResultInc` takes `driverId` as a `Long` (safe from injection) but takes `sDate` and `eDate` as `java.util.Date` objects and interpolates them directly by calling `toString()` (implicit) inside the concatenated SQL string:

```java
String sql = "select id,driver_id,comment,to_char(timestamp,'dd/mm/yyyy HH24:MI:SS'),unit_id "
    + "from result where driver_id = " + driverId
    + " and timestamp >= '" + sDate + "'::timestamp"
    + " and timestamp <= '" + eDate + "'::timestamp"
    + " order by timestamp";
```

`java.util.Date.toString()` produces locale-dependent, non-canonical output. If the application locale or JVM timezone is manipulated, or if the caller derives `sDate`/`eDate` from a user-supplied string (as in `FleetCheckPDF`), the resulting string may contain SQL-significant characters. While exploitation requires specific locale or date-format manipulation, the pattern is inherently unsafe and should be parameterised.

**Risk:** SQL injection via crafted date strings; unexpected query failure under locale changes.

**Recommendation:** Use a `PreparedStatement` with `ps.setTimestamp(n, new java.sql.Timestamp(date.getTime()))` for both date parameters.

---

### HIGH: `deleteUser` silently returns "Deleted" even on failure — no error propagation

**File:** `RestClientService.java` (lines 295–309)

**Description:**
`deleteUser` catches all exceptions and returns the hardcoded string `"Deleted"` regardless of whether the HTTP DELETE call succeeded:

```java
try {
    String baseUrl = "http://localhost:"+COGNITO_API_PORT+"/auth/delete_user?accessToken="+sessionToken+"&email="+URLEncoder.encode(username);
    URI uri = new URI(baseUrl);
    restTemplate.delete(uri);
} catch(Exception e) {
    log.info(method +"HttpStatus Failed");
    e.printStackTrace();
    log.error(method +"error:"+ e.getMessage());
}
return "Deleted";
```

If the Cognito sidecar is unavailable, returns a non-200 response, or the network call fails entirely, the caller receives `"Deleted"` as if the operation succeeded. The user record will remain active in Cognito while the application believes it has been removed, creating an orphaned active Cognito account that retains authentication capability.

**Risk:** Deleted users can continue to authenticate via Cognito if their Cognito record was not actually removed. This is an authentication bypass risk following account deletion.

**Recommendation:** Inspect the HTTP response status code and throw a checked exception (or return a typed response object with a success flag) on non-200 responses. The return type should be changed from `String` to a response object or `boolean` to make success/failure unambiguous to callers.

---

### HIGH: Cognito service port hardcoded as a class constant — no externalised configuration

**File:** `RestClientService.java` (line 35)

**Description:**
The Cognito sidecar port is declared as a hardcoded class-level constant:

```java
private final String COGNITO_API_PORT = "9090";
```

Combined with the hardcoded `localhost` hostname, the entire Cognito endpoint URL is baked into the compiled artifact. This means:
1. Moving the sidecar to a different host or port requires recompilation and redeployment of the WAR.
2. There is no way to point to a different (e.g., test or staging) sidecar without rebuilding.
3. If the port is changed in a deployment for security hardening, the application will silently fail all Cognito calls (all exceptions are swallowed — see separate finding), leading to broken authentication with no visible error to operators.

**Risk:** Operational inflexibility; silent authentication breakage when topology changes; inhibits security patching of the sidecar deployment.

**Recommendation:** Externalise both the host and port to a properties file (e.g., `cognito.api.url=http://localhost:9090`) loaded via `RuntimeConf` or a `@Value` / JNDI injection. This also makes it trivial to enforce HTTPS in all environments by changing the scheme in configuration.

---

### HIGH: `authenticationRequest` and all Cognito response paths treat a `null` body as a success

**File:** `RestClientService.java` (lines 54–62, 89–97, etc.)

**Description:**
Every method follows this pattern:

```java
ResponseEntity<AuthenticationResponse> result = restTemplate.exchange(...);
if (HttpStatus.OK == result.getStatusCode()) {
    response = result.getBody();   // getBody() can return null
    log.info(method + "HttpStatus Succuss");
} else {
    log.info(method + "HttpStatus Failed");
}
```

`RestTemplate.getBody()` returns `null` when the HTTP 200 response has an empty or un-parseable body. The code does not check for `null` before assigning `response = result.getBody()`. Callers receive a non-null response object only if the body was non-null; when it is null, the pre-initialised empty `AuthenticationResponse` is returned, which will typically have all fields at their default (null/0) values. Callers that test `response.getCode().equals(RuntimeConf.HTTP_OK)` (as in `AdminRegisterAction.java` line 149) will throw a `NullPointerException`, which is caught by the outer try-catch and returned as a generic failure — but callers that only check a boolean field may interpret the default value as success.

**Risk:** Null-response from Cognito may be silently treated as a successful authentication or sign-up, depending on the caller's check logic.

**Recommendation:** Add a null-check on `result.getBody()` in every method before assigning to `response`. If the body is null, log an error and return a response object with an explicit failure code.

---

### MEDIUM: `URLEncoder.encode(username)` called without a charset — deprecated API, platform-dependent encoding

**File:** `RestClientService.java` (line 297)

**Description:**
```java
String baseUrl = "http://localhost:"+COGNITO_API_PORT+"/auth/delete_user?accessToken="+sessionToken
    +"&email="+URLEncoder.encode(username);
```

`URLEncoder.encode(String)` without an explicit `Charset` argument is deprecated since Java 1.4 and uses the platform default encoding. On a JVM running with a non-UTF-8 default encoding (e.g., ISO-8859-1 on some Tomcat deployments), email addresses containing non-ASCII characters (common in internationalised deployments) will be encoded incorrectly, causing the delete request to silently target the wrong or non-existent user.

Additionally, `accessToken` (the Cognito JWT) is appended without any URL encoding — if the token contains `+` or `=` characters (common in Base64-encoded JWTs), the query parameter may be parsed incorrectly by the sidecar.

**Risk:** Silent account deletion failure for non-ASCII usernames; JWT access token corruption in URL parameter.

**Recommendation:** Use `URLEncoder.encode(username, StandardCharsets.UTF_8)` and apply the same encoding to `sessionToken`.

---

### MEDIUM: Cognito `signUpRequest` sends a plaintext password in the request log

**File:** `RestClientService.java` (lines 88, 92) and `AdminRegisterAction.java` (lines 174–178)

**Description:**
In `signUpRequest`, `log.info(method + "HttpStatus Succuss")` is called after a successful signup, which itself is benign. However, in `AdminRegisterAction.java`, after a successful Cognito registration the application constructs a confirmation email body that includes the plaintext password:

```java
// AdminRegisterAction.java lines 174–176
String content = "Your account has been registered succesfully in ForklfitIQ360 and can be used on the Portal Website.<br/>"
    + "Username:" + adminRegisterActionForm.getEmail() + "<br/>"
    + "Password:" + adminRegisterActionForm.getPin();
Util.sendMail(RuntimeConf.REGISTER_SUBJECT, content, "", adminRegisterActionForm.getEmail(), "", RuntimeConf.emailFrom);
```

The `UserSignUpRequest` bean is also built with the raw `pin` (password) field before being passed to `RestClientService`. If any logging framework intercepting the bean serialisation is active (debug-level logging of HTTP entity, Spring `RestTemplate` request/response logging), the password will appear in log files.

**Risk:** Plaintext password exposure in email and potentially in logs. Email transmission is not guaranteed to be encrypted, and email is an insecure channel for credential delivery.

**Recommendation:** Remove the password from confirmation emails. Use a Cognito-native "temporary password / force change on first login" flow so passwords are never known to the admin application. Ensure `RestTemplate` debug logging is disabled in production.

---

### MEDIUM: `getUser` URL is built by direct string concatenation of `username` and `accessToken` without encoding

**File:** `RestClientService.java` (lines 192–193)

**Description:**
```java
String baseUrl = "http://localhost:"+COGNITO_API_PORT+"/auth/user?username="+username+"&accessToken="+accessToken;
URI uri = new URI(baseUrl);
```

`username` (an email address) and `accessToken` (a JWT) are concatenated without URL encoding. An email address containing `&`, `=`, `#`, or `+` characters (all RFC 5321 legal in the local-part) will corrupt the query string, causing the sidecar to receive an unexpected or split parameter. A Cognito JWT contains `=` and `+` characters in its Base64url segments.

`new URI(baseUrl)` will throw `URISyntaxException` at runtime for characters outside URI syntax (e.g., spaces in display names), resulting in an unchecked exception that is swallowed by the catch block, and the caller receives an empty `UserResponse`.

**Risk:** Silent failure of user lookups; potential query-string injection if either value is attacker-influenced.

**Recommendation:** Use `UriComponentsBuilder` (already available via Spring on the classpath) to safely construct the URL with encoded parameters.

---

### MEDIUM: `RoleDAO.getRoles` query exposes all non-admin roles to any authenticated session — no comp_id scope

**File:** `RoleDAO.java` (lines 31–33)

**Description:**
```java
String sql = "select id,name,description,authority from roles where name != 'CIIFM Admin' order by name";
```

The query returns every role in the `roles` table (except the super-admin role), unscoped to the requesting company. In `AdminRegisterAction.java` (lines 274–277), the full role list is placed on the request and rendered in the UI for the company settings/update page. If future roles are added that should only be assignable by certain privilege tiers (e.g., a `ROLE_DEALER` that only a super-admin should be able to grant), those roles will be visible in the dropdown for all authenticated users.

The exclusion filter `name != 'CIIFM Admin'` is a hardcoded string match — renaming the admin role in the database would silently expose it.

**Risk:** Privilege escalation risk if higher-privilege roles are added to the table; admin role exposure if the role name changes.

**Recommendation:** Add a `where assignable_by_company = true` (or equivalent) column to the `roles` table and filter on it. Additionally, enforce server-side validation that the role being assigned is permitted for the requesting user's privilege level — the current code has no such check when a company record is saved.

---

### MEDIUM: `saveResult` error handler uses a raw `Statement` to execute a DELETE during exception cleanup

**File:** `ResultDAO.java` (lines 113–114)

**Description:**
Inside the `catch` block, a compensating `DELETE` is built by concatenating `result_id` (an integer from the DB sequence) and executed via `Objects.requireNonNull(stmt).execute(sql)`:

```java
} catch (Exception e) {
    sql = "delete from result where id = " + result_id;
    Objects.requireNonNull(stmt).execute(sql);  // throws NullPointerException if stmt is null
    InfoLogger.logException(log, e);
    return 0;
}
```

1. If `stmt` is `null` (e.g., the exception was thrown before `conn.createStatement` succeeded), `Objects.requireNonNull` throws a `NullPointerException` inside the catch block, completely suppressing the original exception and leaving the `result` row potentially persisted with no answers.
2. The same `stmt` object that threw the originating exception is re-used for the compensating DELETE, which may fail if the connection is in a broken state.
3. The cleanup DML should be in a `finally` block or a separate connection to guarantee execution.

**Risk:** Silent data inconsistency (orphaned result rows with no answers); original exception information lost; potential partial-write DoS.

**Recommendation:** Move compensating cleanup to a `finally` block with its own `try-catch`. Use a database transaction (`conn.setAutoCommit(false)` with `conn.rollback()` in catch) rather than manual compensating DML.

---

### LOW: All Cognito call exceptions are swallowed — failures invisible to callers

**File:** `RestClientService.java` (lines 63–67, 98–102, 133–137, 168–172, 204–208, 241–245, 275–279, 301–306)

**Description:**
Every method catches `Exception` and calls only `e.printStackTrace()` and `log.error(...)`, then returns an empty/default response object. The stack trace goes to `stderr` (not the application log) and the caller receives a structurally valid but empty bean with null fields. There is no way for callers to distinguish a network timeout, a Cognito 500, an SSL handshake failure, or a JSON parse error — all produce the same silent empty-object return.

```java
} catch(Exception e) {
    e.printStackTrace();
    log.error(method + "error:" + e.getMessage());
}
return response; // always returns, never throws
```

**Risk:** Authentication failures, failed user creations, and failed password resets will appear to succeed at the service layer. Operators have no alerting hook. Intermittent Cognito outages go undetected.

**Recommendation:** Define a checked `CognitoServiceException` and rethrow it from all catch blocks, or at minimum set an explicit error code on the returned response object and document that callers must check it. Remove `e.printStackTrace()` and route all exception details through the log framework.

---

### LOW: `getChecklistResultById` and related methods have no `comp_id` parameter — enforcing isolation requires callers to re-query

**File:** `ResultDAO.java` (line 166, method signature)

**Description:**
Related to the IDOR finding above, the method signatures themselves do not include `compId`:

```java
public ArrayList<ResultBean> getChecklistResultById(int resultId) throws Exception
public String getOverallStatus(Long resultId, String unitId) throws Exception
public String[] printErrors(Long resultId, boolean pdfTag) throws Exception
```

Because `compId` is not a parameter, callers cannot add isolation without modifying the method signatures. This creates a structural API contract that makes it easy to call these methods insecurely and difficult to audit all call sites for correct `comp_id` scoping.

**Risk:** Any new call site that invokes these methods will have cross-tenant access by default, requiring auditors to check every caller individually.

**Recommendation:** Add `String compId` to the signatures of all `ResultDAO` read methods, make the SQL filter mandatory at the DAO layer, and update all call sites.

---

### LOW: `PreFlightActionServlet` auth check only covers `doGet` — POST requests bypass session validation on excluded paths

**File:** `PreFlightActionServlet.java` (lines 94–96, 99–114)

**Description:**
`doPost` simply delegates to `doGet`, which applies the session check. However, the `excludeFromFilter` method returns `false` (meaning "do not enforce auth") for several paths including `adminRegister.do`, `api.do`, `mailer.do`, `loadbarcode.do`, and `uploadfile.do`. The auth exclusion for `adminRegister.do` means an unauthenticated user can POST to the registration endpoint, which in turn calls the Cognito sign-up API and creates a Cognito user account. There is no CAPTCHA or rate-limiting visible in the audited code.

**Risk:** Unauthenticated account creation endpoint could be abused for Cognito user enumeration or spam account creation, consuming Cognito API quota.

**Recommendation:** This is largely by design for a self-registration flow, but consider adding server-side rate limiting (e.g., by IP) and CAPTCHA challenge on `adminRegister.do`.

---

### INFO: `ResultBean.isDriverIdSetted()` uses identity comparison for Long autoboxing

**File:** `ResultBean.java` (line 41)

**Description:**
```java
public boolean isDriverIdSetted() {
    return this.driver_id != null && this.driver_id != 0L;
}
```

`this.driver_id` is of type `Long` (boxed). The comparison `this.driver_id != 0L` triggers autoboxing of the literal `0L` to `Long`, then applies reference equality (`!=`) rather than value equality (`.equals()`). Due to JVM Long caching, values in the range -128 to 127 will compare correctly by identity, but this is an implementation detail of the JVM, not a language guarantee. Values outside that range would produce incorrect results — however, since `0L` is within the cached range, this specific check is safe in practice but represents a coding error that could mislead future maintenance.

**Risk:** Low. Functionally correct for `0L` on standard JVMs, but logically incorrect code pattern that may cause defects if changed.

**Recommendation:** Use `!Long.valueOf(0L).equals(this.driver_id)` or `this.driver_id.longValue() != 0L` for the zero check.

---

### INFO: `RoleBean` declares `@Builder` on the private constructor while also using `@NoArgsConstructor` — inconsistent construction pattern

**File:** `RoleBean.java` (lines 9–25)

**Description:**
```java
@Data
@NoArgsConstructor
public class RoleBean implements Serializable {
    ...
    @Builder
    private RoleBean(String id, String name, String description, String authority) { ... }
}
```

`@Builder` on a private constructor with `@NoArgsConstructor` at the class level means the Lombok-generated builder calls the private all-args constructor, while all external code that uses `new RoleBean()` gets the no-args constructor. In `RoleDAO.getRoles()` the bean is constructed with the no-args constructor and populated via setters, which is inconsistent with the builder pattern. The builder is never used within the audited code. The `@Builder` annotation on a private constructor is non-standard and may produce confusing generated code in some Lombok versions.

**Risk:** No security impact. Code quality and maintainability concern.

**Recommendation:** Remove the private constructor and `@Builder` annotation if the builder is unused, or switch entirely to builder-based construction in the DAO.

---

## Summary

| Severity | Count |
|---|---|
| CRITICAL | 3 |
| HIGH | 4 |
| MEDIUM | 5 |
| LOW | 3 |
| INFO | 2 |

**CRITICAL: 3 / HIGH: 4 / MEDIUM: 5 / LOW: 3 / INFO: 2**

### Priority remediation order

1. **(CRITICAL)** SQL injection in `ResultDAO.saveResult` — lines 65, 74, 91 — convert to `PreparedStatement`.
2. **(CRITICAL)** SQL injection in `ResultDAO.checkDuplicateResult` — lines 294–295 — convert to `PreparedStatement`.
3. **(CRITICAL)** HTTP (not HTTPS) for all Cognito sidecar calls — `RestClientService` all methods.
4. **(HIGH)** Missing `comp_id` isolation across all `ResultDAO` read methods — `getChecklistResultById`, `getOverallStatus`, `printErrors`, `getChecklistResultInc`.
5. **(HIGH)** SQL injection in `getChecklistResultInc` date parameters — line 145.
6. **(HIGH)** `deleteUser` silently returns "Deleted" on failure.
7. **(HIGH)** Cognito response body null-check absent — all `RestClientService` methods.
