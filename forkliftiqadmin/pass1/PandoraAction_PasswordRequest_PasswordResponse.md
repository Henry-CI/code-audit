# Security Audit: PandoraAction, PasswordRequest, PasswordResponse
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Branch:** master
**Scope:** Base action class and Cognito password beans

---

## Files Audited

| File | Lines |
|------|-------|
| `src/main/java/com/action/PandoraAction.java` | 44 |
| `src/main/java/com/cognito/bean/PasswordRequest.java` | 34 |
| `src/main/java/com/cognito/bean/PasswordResponse.java` | 25 |

---

## Executive Summary

`PandoraAction` is the base class for five confirmed admin action classes
(`AdminUnitAssignAction`, `AdminManufacturersAction`, `AdminOperatorAction`,
`AdminTrainingsAction`, `AdminUnitAccessAction`) and potentially more actions that
read session or request data through its helpers. It performs **no authorization,
no CSRF protection, no security response headers, and no role or ownership
verification**. Every deficiency listed below is therefore inherited by every
subclass.

`PasswordRequest` carries plaintext credentials (`password`, `oldPassword`,
`accessToken`) with `@Data` (Lombok), meaning `toString()` will emit those values
to any log that calls it. The bean is also `Serializable` without field-level
protection and has no `@JsonIgnore` annotations. `PasswordResponse` does not carry
passwords but shares the same structural pattern.

---

## Findings

### CRITICAL: No authorization or role check in the base class — all subclasses inherit zero authorization
**File:** `PandoraAction.java` (entire class)
**Description:**
`PandoraAction` overrides nothing from `org.apache.struts.action.Action` and adds
no `execute()` / `perform()` hook that enforces role or ownership checks before
delegating to subclasses. There is no role attribute read from the session (e.g.,
`sessRole`, `sessUserType`), no call to any access-control service, and no
abstract method that subclasses are forced to implement before business logic runs.

The only auth gate in the entire application is `PreFlightActionServlet.doGet()`,
which checks only that `sessCompId != null`. This means any authenticated user at
any company can invoke any admin action — there is no check that the caller is an
admin, a dealer, or any other privileged role. The `getCompId()` helper (line 41)
returns the session company ID but never verifies it against a required permission.

```java
// PandoraAction.java — the entire class; no execute() override, no role check
public abstract class PandoraAction extends Action {
    // ...utility helpers only...
    protected String getCompId(HttpSession session) {
        return getSessionAttribute(session, "sessCompId", null);
    }
}
```

**Risk:** A non-admin authenticated user who knows the `.do` endpoint names of
admin actions (unit management, operator management, training management, etc.) can
call those actions directly. The session gate in `PreFlightActionServlet` will pass
them because they hold a valid `sessCompId`. All five known `PandoraAction`
subclasses perform administrative database mutations.

**Recommendation:** Add an `execute()` override in `PandoraAction` that reads a
role/privilege attribute from the session and throws an `UnauthorizedException` (or
redirects to an error page) if the caller does not hold the required privilege. At
minimum, define an abstract `requiredRole()` method that every subclass must
implement, so the base class can enforce it before calling the subclass logic.

---

### CRITICAL: No CSRF protection in the base class or anywhere in the framework
**File:** `PandoraAction.java` (entire class), cross-referenced with `PreFlightActionServlet.java`
**Description:**
Neither `PandoraAction` nor `PreFlightActionServlet` validates a CSRF synchronizer
token. Struts 1.3.10 does not include built-in CSRF protection. There is no token
generation, no token storage in session, and no token validation before any state-
changing action executes. Every `.do` endpoint that performs a write operation (add
driver, edit unit, assign training, etc.) is therefore forgeable by a malicious
third-party page.

```java
// PreFlightActionServlet.java lines 56-60 — the complete auth gate
else if(session.getAttribute("sessCompId") == null
        || session.getAttribute("sessCompId").equals(""))
{
    stPath = RuntimeConf.EXPIRE_PAGE;
    forward = true;
}
// No CSRF token check anywhere in the gate or in PandoraAction
```

**Risk:** An attacker who can lure any authenticated admin user to a malicious
page can silently submit cross-origin POST requests to any admin `.do` action. This
can result in arbitrary data mutation (creating/deleting drivers, units, alerts,
etc.) under the victim's session and tenant context.

**Recommendation:** Introduce a CSRF token filter (e.g., OWASP CSRFGuard, or a
custom `javax.servlet.Filter`) that generates a per-session token, stores it as a
session attribute, and validates it on every non-idempotent request. Alternatively,
add CSRF token generation and validation inside `PandoraAction.execute()` so all
subclasses inherit it automatically.

---

### HIGH: No security response headers set by the base class or the servlet
**File:** `PandoraAction.java` (entire class), `PreFlightActionServlet.java`
**Description:**
Neither `PandoraAction` nor `PreFlightActionServlet` sets any of the following
security-relevant HTTP response headers:

- `X-Frame-Options` (clickjacking protection)
- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `Strict-Transport-Security`
- `Cache-Control: no-store` (prevents sensitive page caching)
- `Referrer-Policy`

`PreFlightActionServlet.doGet()` calls `super.doGet()` without adding any headers,
and `PandoraAction` has no `execute()` override that could inject them via
`HttpServletResponse`.

**Risk:** Absence of `X-Frame-Options` exposes every admin page to clickjacking.
Absence of `X-Content-Type-Options` enables MIME-sniffing attacks. Absence of
`Cache-Control: no-store` means sensitive admin data may be stored in browser or
proxy caches and recoverable after logout. Absence of CSP significantly widens
the exploitable surface area if XSS is found elsewhere.

**Recommendation:** Add a `javax.servlet.Filter` (mapped to `/*`) that sets all
required security headers on every response. This is independent of the action
framework and is the most robust location. Alternatively, add header injection in
`PandoraAction.execute()` via the `HttpServletResponse` parameter for all
subclasses.

---

### HIGH: `PasswordRequest` uses Lombok `@Data` — `toString()` leaks plaintext credentials to logs
**File:** `PasswordRequest.java` (lines 9, 17–21)
**Description:**
The class is annotated with `@Data`, which causes Lombok to generate a `toString()`
method that includes every field. The fields `password`, `oldPassword`, and
`accessToken` are all plaintext strings that will appear verbatim in any log line
that calls `toString()` on this object, including:

- Framework-level debug logging (Spring `RestTemplate` debug mode)
- Exception messages if the object is embedded in a log statement
- Any accidental `log.info(passwordRequest.toString())` call

```java
@Data                        // generates toString() exposing ALL fields
@NoArgsConstructor
public class PasswordRequest implements Serializable {
    private String username;
    private String password;       // EXPOSED by toString()
    private String confirmationCode;
    private String oldPassword;    // EXPOSED by toString()
    private String accessToken;    // EXPOSED by toString()
    ...
}
```

`RestClientService` logs method names and status around every Cognito call
(lines 57, 101, 130, 163). If the log level is ever raised to DEBUG (a common
troubleshooting action), Spring `RestTemplate` will log the full request body,
which Jackson serializes from all fields of `PasswordRequest`.

**Risk:** Cleartext passwords and access tokens written to application logs,
which are frequently shipped to log aggregators (Splunk, CloudWatch, etc.).
Any party with read access to logs gains credentials that can be used to take
over Cognito accounts.

**Recommendation:**
1. Add `@ToString(exclude = {"password", "oldPassword", "accessToken"})` to the
   class, or replace `@Data` with individual Lombok annotations (`@Getter`,
   `@Setter`, `@EqualsAndHashCode`) and write a manual `toString()` that
   redacts sensitive fields.
2. Annotate `password` and `oldPassword` fields with `@JsonIgnore` to prevent
   accidental JSON serialization in any response path.

---

### HIGH: `PasswordRequest` is `Serializable` with unprotected credential fields — session/cache persistence risk
**File:** `PasswordRequest.java` (lines 3, 11, 15)
**Description:**
`PasswordRequest` implements `java.io.Serializable` with a fixed `serialVersionUID`.
The fields `password`, `oldPassword`, and `accessToken` are neither `transient` nor
protected in any way. If this object is ever placed in the HTTP session, a session
cache (Redis, Memcached), or a session file store, the credentials will be
persisted in plaintext in that backing store.

```java
public class PasswordRequest implements Serializable {
    private static final long serialVersionUID = 6722563341130946506L;

    private String username;
    private String password;        // not transient — serialized
    private String confirmationCode;
    private String oldPassword;     // not transient — serialized
    private String accessToken;     // not transient — serialized
    ...
}
```

While the current codebase does not explicitly store `PasswordRequest` in session,
the combination of `Serializable` + `@NoArgsConstructor` (required by some
serialization frameworks) makes it easy for future code to do so accidentally.
Tomcat session persistence (the default `FileStore` or `JDBCStore` when configured)
would write these fields to disk or a database.

**Risk:** Credentials at rest in session files, database rows, or distributed
caches. A breach of the session store would expose all in-flight credentials.

**Recommendation:** Mark `password`, `oldPassword`, and `accessToken` as
`transient`. If the bean is only used as a one-shot request DTO to `RestClientService`
and never stored in session, consider removing `Serializable` entirely.

---

### HIGH: `PasswordResponse` declares `serialVersionUID` but does not implement `Serializable`
**File:** `PasswordResponse.java` (lines 17–18)
**Description:**
The class declares a `private static final long serialVersionUID` field but does
**not** declare `implements Serializable`. This is a defect in the code: the field
has no effect and gives a false impression that serialization is properly managed.
More importantly, if the object is ever placed in an HTTP session (a common pattern
in Struts 1.x), the Tomcat serialization mechanism will fail at runtime with a
`java.io.NotSerializableException` when session persistence is enabled, causing
silent data loss or session errors.

```java
@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class PasswordResponse {          // <-- does NOT implement Serializable
    private static final long serialVersionUID = -8677893765042629588L;  // dead field
    private String destination;
    private String deliveryMedium;
    private String message;
    private String username;
    private Integer code;
    private String detail;
}
```

**Risk:** Runtime `NotSerializableException` if session persistence is enabled and
this object is placed in session. The dead `serialVersionUID` field misleads
developers into believing the class is serialization-safe.

**Recommendation:** Either add `implements Serializable` (and keep `serialVersionUID`)
if the object may be stored in session, or remove the dead `serialVersionUID` field.
Given that `PasswordResponse` carries a `message` and `detail` that may contain
Cognito error details (potentially sensitive), the safer choice is to keep it
non-serializable and remove the field to avoid confusion.

---

### MEDIUM: `getRequestParam(String, String defaultValue)` does not filter the `"undefined"` JavaScript sentinel
**File:** `PandoraAction.java` (lines 24–27)
**Description:**
The `Long`-returning overload of `getRequestParam` (line 17) correctly filters the
JavaScript string `"undefined"` and returns `defaultValue` in that case. The
`String`-returning overload (line 24) does **not** apply the same filter:

```java
// Long overload — correctly handles "undefined"
protected Long getRequestParam(HttpServletRequest request, String name, Long defaultValue) {
    String param = request.getParameter(name);
    return StringUtils.isBlank(param) || UNDEFINED_PARAM.equalsIgnoreCase(param)
           ? defaultValue : Long.valueOf(param);  // line 21
}

// String overload — does NOT handle "undefined"
protected String getRequestParam(HttpServletRequest request, String name, String defaultValue) {
    String param = request.getParameter(name);
    return param == null ? defaultValue : param;  // line 26 — returns literal "undefined"
}
```

Subclasses that call the `String` overload will receive the literal string
`"undefined"` when a JavaScript `undefined` variable is submitted. This can cause
downstream logic errors: DAO queries with `WHERE column = 'undefined'`,
data stored as `"undefined"` in the database, or incorrect branching in action
logic (e.g., `if (action.equalsIgnoreCase("reset"))` failing because `action` is
`"undefined"`).

**Risk:** Data integrity issues, silent logic failures, and potential for
unexpected code paths when `"undefined"` propagates into DAO layers. Because
`sessCompId` is retrieved via `getSessionAttribute()` (a different method), tenant
isolation is not directly threatened, but business logic in subclasses is.

**Recommendation:** Apply the same `UNDEFINED_PARAM` sentinel check in the
`String`-returning overload, returning `defaultValue` when the value is blank or
equals `"undefined"` (case-insensitive).

---

### MEDIUM: `getLongSessionAttribute` will throw `NumberFormatException` on malformed session data
**File:** `PandoraAction.java` (lines 35–39)
**Description:**
`getLongSessionAttribute` calls `Long.valueOf(attrib.toString())` without any
`try/catch` or validation. If a session attribute has been set to a non-numeric
value (through session fixation, a bug in a setter, or a misconfiguration), this
will throw an unchecked `NumberFormatException` that propagates up through the
action and may produce a 500 error page. The same pattern exists in the `Long`
overload of `getRequestParam` (line 21), which is used by subclasses to parse
user-supplied input directly:

```java
// PandoraAction.java line 38
return attrib == null ? defaultValue : Long.valueOf(attrib.toString());

// PandoraAction.java line 21
return StringUtils.isBlank(param) || UNDEFINED_PARAM.equalsIgnoreCase(param)
       ? defaultValue : Long.valueOf(param);  // throws NumberFormatException on "abc"
```

**Risk:** An attacker who can influence session attribute values (e.g., via session
fixation) or who passes non-numeric values in request parameters can trigger
unhandled exceptions. Depending on Tomcat and Struts error page configuration,
this may leak stack traces containing class names, package structure, or query
fragments.

**Recommendation:** Wrap `Long.valueOf()` calls in a try/catch that returns
`defaultValue` (or a dedicated error value), or use `StringUtils.isNumeric()`
as a guard before parsing.

---

### MEDIUM: `ResetPasswordAction` and `GoResetPassAction` bypass `PandoraAction` entirely — password reset has no session validation
**File:** `ResetPasswordAction.java` (line 24), `GoResetPassAction.java` (line 17)
**Description:**
Both password reset action classes extend `org.apache.struts.action.Action`
directly rather than `PandoraAction`. They are also listed in
`PreFlightActionServlet.excludeFromFilter()` (lines 110–111), meaning
`sessCompId` is never checked for these endpoints. However, the critical issue is
that `GoResetPassAction` reads `accessToken` from the session
(line 25: `session.getAttribute("accessToken")`) but also calls
`request.getSession(false)` — if there is no existing session, `session` will be
`null` and the code will throw a `NullPointerException` on line 25 before
reaching that check.

```java
// GoResetPassAction.java lines 22-25
HttpSession session = request.getSession(false);  // returns null if no session
String action = ...;
String username = ...;
String accessToken = session.getAttribute("accessToken") == null ? ""   // NPE if session is null
                     : (String) session.getAttribute("accessToken");
```

The same pattern exists in `ResetPasswordAction.java` line 33. The reset flow
initiates with the username supplied as a plain request parameter (no CAPTCHA,
no rate limiting visible in the code) and the `username` value is passed directly
to `PasswordRequest.builder()` and sent to the Cognito API, enabling an
**unauthenticated password reset trigger for any username**.

**Risk:** (1) NullPointerException denial-of-service on the reset endpoints if
called without a prior session. (2) An unauthenticated actor can trigger a
Cognito password reset email for any known username by calling
`goResetPass.do?action=reset&username=victim@example.com`, as the endpoint is
excluded from the session gate. There is no CAPTCHA, no rate limiting in code,
and no verification that the caller owns the account.

**Recommendation:** Add a null check for `session` before accessing it. Evaluate
whether the reset trigger endpoint should require a pre-step (CAPTCHA, account
existence verification that does not leak enumeration) and add rate limiting at
the WAF or servlet filter level.

---

### LOW: `assert` statements used for parameter validation — disabled in production JVMs
**File:** `PandoraAction.java` (lines 18, 30, 36)
**Description:**
Three methods use Java `assert` statements to validate that the `name` parameter
is not blank:

```java
assert StringUtils.isNotBlank(name) : "request param name must not be blank";
```

Java assertions are disabled by default in standard JVM deployments (including
Tomcat) unless the JVM is started with `-ea`. In production, these assertions
silently do nothing. A blank or null `name` passed to `getSessionAttribute` or
`getLongSessionAttribute` would proceed to `session.getAttribute(null)`, which
throws `IllegalArgumentException` from the servlet container, producing an
unhandled exception and possible stack trace exposure rather than a clean error.

**Risk:** Low direct security impact, but the false confidence that validation is
occurring could lead developers to omit proper null/blank checks in calling code.
If `session.getAttribute(null)` is reached, the resulting exception may leak
internal details.

**Recommendation:** Replace `assert` statements with explicit `if` guards that
throw `IllegalArgumentException` unconditionally, or use
`Objects.requireNonNull` / `Validate.notBlank` (Apache Commons) which are always
active regardless of JVM flags.

---

### INFO: `getCompId()` is a convenience method, not an authorization check — name may be misleading
**File:** `PandoraAction.java` (lines 41–43)
**Description:**
`getCompId()` retrieves `sessCompId` from the session and returns it as a raw
string. It performs no validation that the returned value is a valid, non-null
company ID, and it performs no authorization check. Developers reading the method
signature may believe that calling `getCompId()` performs some form of access
control verification. In practice it is equivalent to
`session.getAttribute("sessCompId")`.

```java
protected String getCompId(HttpSession session) {
    return getSessionAttribute(session, "sessCompId", null);
    // returns null if not set; no authorization logic
}
```

Subclasses that call `getCompId()` and then pass the result to DAO methods without
a null check risk NullPointerException or unscoped queries if the session state is
inconsistent.

**Risk:** Informational / code clarity. The combination of a misleading method name
and a null return value is a latent bug surface rather than a direct vulnerability.

**Recommendation:** Add a Javadoc comment making explicit that this method is a
session attribute accessor only and does not perform authorization. Subclasses
that require a valid company ID should check for null and handle the absent case
explicitly.

---

### INFO: `PasswordResponse` carries a `message` and `detail` field that may reflect Cognito error strings
**File:** `PasswordResponse.java` (lines 22–23)
**Description:**
`PasswordResponse.message` and `PasswordResponse.detail` are populated from the
Cognito API response and, per `ResetPasswordAction.java` line 48, the `message`
value is passed directly into a Struts `ActionMessage` that is displayed to the
user:

```java
// ResetPasswordAction.java line 48
String errormsg = passwordResponse.getMessage();
ActionMessage msg = new ActionMessage("error.incorrect.reset.cognito", errormsg);
```

If the Cognito service returns verbose internal error messages, user-account
enumeration hints (e.g., "User does not exist"), or stack trace fragments, these
will be rendered in the browser.

**Risk:** Potential information leakage about user account existence or internal
Cognito configuration through error messages reflected to the client. Low severity
in isolation, but a contributing factor if combined with other findings.

**Recommendation:** Normalize Cognito error responses in the service layer before
setting `message` and `detail`. Map known Cognito exception codes to generic
user-facing messages (e.g., "Password reset failed. Please try again.") and log
the raw detail server-side only.

---

## Finding Count

CRITICAL: 2 / HIGH: 4 / MEDIUM: 3 / LOW: 1 / INFO: 2
