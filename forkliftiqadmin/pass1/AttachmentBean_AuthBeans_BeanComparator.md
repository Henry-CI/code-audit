# Security Audit Report
## Files: AttachmentBean, AuthenticationRequest, AuthenticationResponse, BeanComparator
**Audit run:** audit/2026-02-26-01/pass1
**Date:** 2026-02-26
**Auditor:** Automated Security Review (Claude Sonnet 4.6)
**Branch:** master

---

## 1. Reading Evidence

### 1.1 `src/main/java/com/bean/AttachmentBean.java`

**Class:** `AttachmentBean`
**Implements:** `java.io.Serializable`
**serialVersionUID:** `-2969164023760074040L`

| Field | Type | Access |
|-------|------|--------|
| `id` | `String` | `private`, initialized `null` |
| `name` | `String` | `private`, initialized `null` |

**Methods with logic:**
- `getId()` / `setId(String id)` — standard getter/setter, no logic.
- `getName()` / `setName(String name)` — standard getter/setter, no logic.
- No `toString()`, `equals()`, or `hashCode()` overrides present.

---

### 1.2 `src/main/java/com/cognito/bean/AuthenticationRequest.java`

**Class:** `AuthenticationRequest`
**Implements:** `java.io.Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`
**serialVersionUID:** `152396558777730489L`

| Field | Type | Sensitivity |
|-------|------|-------------|
| `username` | `String` | Moderate |
| `password` | `String` | **CRITICAL — plaintext credential** |
| `newPassword` | `String` | **CRITICAL — plaintext credential** |
| `accessToken` | `String` | **HIGH — AWS Cognito bearer token** |

**Methods with logic:**
- `@Builder`-annotated private all-args constructor: `AuthenticationRequest(String username, String password, String newPassword, String accessToken)` — assigns all four fields, no masking or validation.
- Lombok `@Data` generates at compile time: `toString()`, `equals()`, `hashCode()`, and all getters/setters. The generated `toString()` will include **all four fields**, including `password`, `newPassword`, and `accessToken`, in plain text.

**Observed usage (RestClientService.java:49, LoginAction.java:39-42):**
```java
AuthenticationRequest authenticationRequest = AuthenticationRequest.builder()
    .username(loginActionForm.getUsername())
    .password(loginActionForm.getPassword())
    .build();
```
The object is serialized to JSON and POSTed to `http://localhost:9090/auth`.

---

### 1.3 `src/main/java/com/cognito/bean/AuthenticationResponse.java`

**Class:** `AuthenticationResponse`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`
**Jackson annotation:** `@JsonInclude(JsonInclude.Include.NON_NULL)`
**serialVersionUID:** `408336884318011949L` (declared but class does NOT implement `Serializable`)

| Field | Type | Sensitivity |
|-------|------|-------------|
| `accessToken` | `String` | **HIGH — AWS Cognito access token** |
| `sessionToken` | `String` | **HIGH — session bearer token** |
| `expiresIn` | `String` | Low |
| `actualDate` | `String` | Low |
| `expirationDate` | `String` | Low |
| `userData` | `UserResponse` | Moderate — contains username, email, phone |
| `username` | `String` | Moderate |
| `message` | `String` | Low |
| `code` | `Integer` | Low |
| `detail` | `String` | Low |

**Methods with logic:**
- None beyond Lombok-generated methods. Lombok `@Data` generates `toString()` which will include `accessToken` and `sessionToken` in plain text.
- `@JsonInclude(NON_NULL)` suppresses null fields in JSON serialization but does NOT suppress them in `toString()`.

**Observed usage:**
- `RestClientService.authenticationRequest()` (line 56): response object is returned to `LoginAction`, which stores `sessionToken` in the HTTP session (`session.setAttribute("sessionToken", sessionToken)` at LoginAction.java:51).
- The `accessToken` field is received from Cognito but **not stored separately in the session**; however, it is carried within the full `AuthenticationResponse` object and could appear in log output if the object is ever logged.

---

### 1.4 `src/main/java/com/util/BeanComparator.java`

**Class:** `BeanComparator`
**Implements:** `java.util.Comparator` (raw, non-generic)

| Field | Type | Notes |
|-------|------|-------|
| `method` | `java.lang.reflect.Method` | Resolved once at construction |
| `isAscending` | `boolean` | Default `true` |
| `isIgnoreCase` | `boolean` | Default `true` |
| `isNullsLast` | `boolean` | Default `true` |
| `EMPTY_CLASS_ARRAY` | `static final Class[]` | Constant |
| `EMPTY_OBJECT_ARRAY` | `static final Object[]` | Constant |

**Methods with logic:**

- **`BeanComparator(Class<?> beanClass, String methodName)`** (line 34): delegates to the 3-arg constructor.
- **`BeanComparator(Class<?> beanClass, String methodName, boolean isAscending)`** (line 42): delegates to the 4-arg constructor.
- **`BeanComparator(Class<?> beanClass, String methodName, boolean isAscending, boolean isIgnoreCase)`** (line 51): resolves the method via `beanClass.getMethod(methodName, EMPTY_CLASS_ARRAY)`. Throws `IllegalArgumentException` if the method does not exist or returns `void`. The resolved `Method` object is stored as an instance field.
- **`compare(Object object1, Object object2)`** (line 107): invokes the stored `Method` reflectively on both objects via `method.invoke(object1, EMPTY_OBJECT_ARRAY)`. Handles nulls, empty strings, ascending/descending order, and `Comparable` vs `toString()` fallback. Raw `@SuppressWarnings("unchecked")` applied. Any `Exception` from reflection is wrapped in a `RuntimeException`.

**Observed call site (FormBuilderAction.java:97):**
```java
BeanComparator bc = new BeanComparator(FormElementBean.class, "getPosition");
```
The `methodName` is a hard-coded string literal at this call site.

---

## 2. Findings

---

### FINDING-01
**Severity:** HIGH
**File:** `src/main/java/com/cognito/bean/AuthenticationRequest.java`
**Lines:** 10, 19-21 (Lombok `@Data` annotation; `password`, `newPassword`, `accessToken` fields)

**Category:** Sensitive Data Exposure via Lombok-generated `toString()`

**Description:**
The `@Data` annotation causes Lombok to generate a `toString()` method that includes the values of **all** fields: `username`, `password`, `newPassword`, and `accessToken`. Any code path that logs, prints, or serializes this object to a string — such as `log.info(authenticationRequest.toString())`, an exception message, a test assertion failure, or a framework debug dump — will expose plaintext passwords and a live Cognito access token.

**Evidence:**
```java
// AuthenticationRequest.java:10,18-21
@Data
@NoArgsConstructor
public class AuthenticationRequest implements Serializable {
    private String username;
    private String password;       // plaintext credential
    private String newPassword;    // plaintext credential
    private String accessToken;    // AWS Cognito token
```
Lombok `@Data` generates (at compile time):
```java
// effective generated toString():
public String toString() {
    return "AuthenticationRequest(username=" + this.username
        + ", password=" + this.password
        + ", newPassword=" + this.newPassword
        + ", accessToken=" + this.accessToken + ")";
}
```
RestClientService.java line 207 already logs exception messages from this service layer (`log.error("authenticationRequest error:" + e.getMessage())`). Should any framework or library call `toString()` on the request object during an error, credentials would be emitted to the log.

**Recommendation:**
Add a custom `toString()` override that masks sensitive fields, or use Lombok's `@ToString.Exclude` on `password`, `newPassword`, and `accessToken`:
```java
@ToString.Exclude
private String password;
@ToString.Exclude
private String newPassword;
@ToString.Exclude
private String accessToken;
```
This ensures generated `toString()` output never contains credential or token values.

---

### FINDING-02
**Severity:** HIGH
**File:** `src/main/java/com/cognito/bean/AuthenticationResponse.java`
**Lines:** 9, 17-18 (Lombok `@Data`; `accessToken`, `sessionToken` fields)

**Category:** Sensitive Data Exposure via Lombok-generated `toString()`

**Description:**
The `@Data` annotation generates a `toString()` that includes `accessToken` and `sessionToken` in plain text. These are live AWS Cognito bearer tokens. Any debug logging, exception handling, or accidental serialization of the response object will expose these tokens.

**Evidence:**
```java
// AuthenticationResponse.java:9,17-18
@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AuthenticationResponse {
    private String accessToken;    // AWS Cognito access token
    private String sessionToken;   // session bearer token
```
Effective generated `toString()` will render both token fields as plain text. The `@JsonInclude(NON_NULL)` annotation affects only Jackson JSON serialization — it does NOT suppress fields in `toString()`.

**Recommendation:**
Apply `@ToString.Exclude` to `accessToken` and `sessionToken`:
```java
@ToString.Exclude
private String accessToken;
@ToString.Exclude
private String sessionToken;
```

---

### FINDING-03
**Severity:** HIGH
**File:** `src/main/java/com/cognito/bean/AuthenticationRequest.java`
**Lines:** 19-20

**Category:** Sensitive Data in Serializable Object

**Description:**
`AuthenticationRequest` implements `java.io.Serializable` and carries `password` and `newPassword` as plain `String` fields. A serializable credential carrier is at elevated risk of: (1) inadvertent serialization to disk (e.g., HTTP session persistence, distributed cache), (2) deserialization gadget chain attacks if the object is ever deserialized from an untrusted source, and (3) inclusion in heap dumps or thread dumps.

**Evidence:**
```java
// AuthenticationRequest.java:12,19-20
public class AuthenticationRequest implements Serializable {
    private static final long serialVersionUID = 152396558777730489L;
    private String password;
    private String newPassword;
```
The object is constructed from a user-submitted form (`loginActionForm.getPassword()`) and passed via a REST call. If the application server persists HTTP sessions (e.g., to disk or a shared cache) and a session attribute ever holds this object, plaintext passwords would be written to storage.

**Recommendation:**
- Mark `password` and `newPassword` as `transient` so they are excluded from Java serialization:
  ```java
  private transient String password;
  private transient String newPassword;
  ```
- Consider whether this bean actually needs to implement `Serializable` at all, given it is used as a short-lived REST request DTO. If not needed, remove the interface.
- Do not store `AuthenticationRequest` objects as HTTP session attributes.

---

### FINDING-04
**Severity:** MEDIUM
**File:** `src/main/java/com/cognito/bean/AuthenticationResponse.java`
**Lines:** 16 (`serialVersionUID` declaration)

**Category:** Misleading `serialVersionUID` on Non-Serializable Class

**Description:**
`AuthenticationResponse` declares `private static final long serialVersionUID = 408336884318011949L` but the class does **not** implement `java.io.Serializable`. The field is therefore meaningless and may mislead developers into believing the class is safely serializable. If a developer later adds `implements Serializable` without further review, the sensitive `accessToken` and `sessionToken` fields would immediately become serializable without any transient guards.

**Evidence:**
```java
// AuthenticationResponse.java:12,16
public class AuthenticationResponse {   // <-- no "implements Serializable"
    private static final long serialVersionUID = 408336884318011949L;  // dead field
```

**Recommendation:**
Remove the orphaned `serialVersionUID` field. If serialization is genuinely required in future, add the interface deliberately at that time and mark sensitive token fields as `transient`.

---

### FINDING-05
**Severity:** MEDIUM
**File:** `src/main/java/com/util/BeanComparator.java`
**Lines:** 20, 34, 42, 51, 107

**Category:** Raw (Non-Generic) `Comparator` Implementation — Type Safety

**Description:**
`BeanComparator` implements the raw `Comparator` interface (`implements Comparator` rather than `Comparator<T>`). The `compare(Object object1, Object object2)` method accepts any object type, suppresses unchecked warnings (`@SuppressWarnings("unchecked")`), and casts field values to `Comparable` without verifying that `c2` is the same type as `c1`. If the two objects passed to `compare` are of different types, or the reflectively retrieved field values are of incompatible types, a `ClassCastException` will be thrown at runtime and wrapped in a `RuntimeException`, providing no informative failure message and potentially disrupting sort operations silently or crashing request processing.

**Evidence:**
```java
// BeanComparator.java:20,106-165
public class BeanComparator implements Comparator  // raw type
{
    @SuppressWarnings("unchecked")
    public int compare(Object object1, Object object2)
    {
        ...
        if (c1 instanceof Comparable)
        {
            if (c1 instanceof String && isIgnoreCase)
                return ((String)c1).compareToIgnoreCase((String)c2); // c2 assumed String, no check
            else
                return ((Comparable)c1).compareTo(c2);  // raw Comparable, unsafe cast
        }
```
The cast `(String)c2` on line 162 and the raw `((Comparable)c1).compareTo(c2)` on line 164 are both unchecked. If `c2` is not the same type, a `ClassCastException` results.

**Recommendation:**
- Parameterize the class: `public class BeanComparator<T> implements Comparator<T>`.
- Add a runtime type check before the `compareToIgnoreCase` cast: verify `c2 instanceof String` before casting.
- Log or throw a more informative exception than a bare `RuntimeException(e)` from the reflection invocation.

---

### FINDING-06
**Severity:** MEDIUM
**File:** `src/main/java/com/util/BeanComparator.java`
**Lines:** 34, 51, 60

**Category:** Caller-Controlled Method Name via Reflection — Potential for Unintended Method Invocation

**Description:**
The `methodName` parameter passed to the constructor is used directly in `beanClass.getMethod(methodName, EMPTY_CLASS_ARRAY)` with no validation or allowlisting. If any call site passes a `methodName` sourced from external input (e.g., a request parameter), an attacker could cause the comparator to invoke any publicly accessible no-arg method on the bean objects, including methods with side effects such as `toString()`, `hashCode()`, or any public no-arg method that performs I/O or state mutation.

**Evidence:**
```java
// BeanComparator.java:60
method = beanClass.getMethod(methodName, EMPTY_CLASS_ARRAY);
```
```java
// FormBuilderAction.java:97 — current safe call site (hard-coded)
BeanComparator bc = new BeanComparator(FormElementBean.class, "getPosition");
```
The current known call site uses a hard-coded string. However, the class is a reusable utility, and there is no enforcement preventing future callers from passing user-controlled input.

**Recommendation:**
- In the constructor, validate that `methodName` matches an expected getter pattern (e.g., starts with `get` or `is` and is alphanumeric only): `if (!methodName.matches("(get|is)[A-Za-z0-9]+")) throw new IllegalArgumentException(...)`.
- Document clearly that `methodName` must never be derived from user-supplied input.

---

### FINDING-07
**Severity:** LOW
**File:** `src/main/java/com/util/BeanComparator.java`
**Lines:** 117-119

**Category:** Silent Exception Swallowing in `compare()`

**Description:**
Any exception thrown during reflective method invocation in `compare()` is caught generically and re-thrown as `new RuntimeException(e)` with no logging. This means invocation failures (e.g., `IllegalAccessException`, `InvocationTargetException`) are invisible in logs and present only as an opaque `RuntimeException` in stack traces, making diagnosis difficult.

**Evidence:**
```java
// BeanComparator.java:112-119
try {
    field1 = method.invoke(object1, EMPTY_OBJECT_ARRAY);
    field2 = method.invoke(object2, EMPTY_OBJECT_ARRAY);
}
catch (Exception e)
{
    throw new RuntimeException( e );
}
```

**Recommendation:**
Log the exception before re-throwing, including the method name and class involved:
```java
catch (Exception e) {
    log.error("BeanComparator: reflection invocation failed for method ["
        + method.getName() + "]", e);
    throw new RuntimeException(e);
}
```

---

### FINDING-08
**Severity:** LOW
**File:** `src/main/java/com/cognito/bean/AuthenticationRequest.java`
**Lines:** 6-8, 10-11

**Category:** Missing `@Builder` Accessibility — Builder Pattern Inconsistency

**Description:**
The class uses `@NoArgsConstructor` (public, no-arg) alongside a `private` `@Builder`-annotated all-args constructor. The intent appears to be to restrict direct construction to the builder pattern. However, `@NoArgsConstructor` generates a `public` no-arg constructor, making it possible to create an `AuthenticationRequest` with all fields null and then set sensitive fields (including `password` and `accessToken`) individually via setters generated by `@Data`. This undermines any invariant intended by the builder pattern (e.g., always supplying a username with a password together).

**Evidence:**
```java
// AuthenticationRequest.java:10-12,23-24
@Data
@NoArgsConstructor                     // public no-arg constructor generated
public class AuthenticationRequest ... {
    ...
    @Builder
    private AuthenticationRequest(...) { ... }  // private all-args
```
Result: an `AuthenticationRequest` can be fully constructed field-by-field via setters without any co-validation.

**Recommendation:**
If the builder is intended as the only construction mechanism, remove `@NoArgsConstructor` (or replace it with `@NoArgsConstructor(access = AccessLevel.PRIVATE)`). If a public no-arg constructor is required for a framework (e.g., Jackson deserialization), add a custom `toString()` and consider using `@JsonProperty` annotations to control deserialization explicitly.

---

### FINDING-09
**Severity:** INFO
**File:** `src/main/java/com/bean/AttachmentBean.java`
**Lines:** 5, 14, 20

**Category:** No Issues — Informational Note

**Description:**
`AttachmentBean` is a minimal data carrier with two non-sensitive string fields (`id`, `name`). It correctly implements `Serializable` with an explicit `serialVersionUID`. No credentials, tokens, or sensitive data are present. No logic methods exist beyond standard getters and setters. No `toString()` override is present, but neither field carries sensitive content.

**No security issues identified in this file.**

---

### FINDING-10
**Severity:** INFO
**File:** `src/main/java/com/service/RestClientService.java` (supporting context)
**Lines:** 192-193, 228, 297

**Category:** Access Tokens Appended to URL Query Strings

**Description:**
Although not one of the four audited files, the caller context for the audited beans reveals that `accessToken` values are appended directly to URL query strings in multiple methods:
- `getUser()` (line 192): `?username=` + username + `&accessToken=` + accessToken
- `getUserList()` (line 228): `?accessToken=` + accessToken
- `deleteUser()` (line 297): `?accessToken=` + sessionToken + `&email=` + username

Tokens in URL query strings are captured in web server access logs, browser history, HTTP `Referer` headers, and network appliance logs. This amplifies the exposure risk of `accessToken` and `sessionToken` values from `AuthenticationResponse`.

**Recommendation:**
Pass access tokens via HTTP `Authorization: Bearer <token>` headers rather than as URL query parameters.

---

## 3. Category Summary

| Category | Files Affected | Findings |
|----------|---------------|----------|
| Sensitive data in bean fields (credentials/tokens) | `AuthenticationRequest.java` | FINDING-01, FINDING-03, FINDING-08 |
| AWS Cognito credentials/tokens serialized or exposed | `AuthenticationRequest.java`, `AuthenticationResponse.java` | FINDING-01, FINDING-02, FINDING-03, FINDING-04 |
| Reflection-based ordering issues in BeanComparator | `BeanComparator.java` | FINDING-05, FINDING-06, FINDING-07 |
| Sensitive data in `AttachmentBean` | `AttachmentBean.java` | **NO ISSUES** |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 0 | — |
| HIGH | 3 | FINDING-01, FINDING-02, FINDING-03 |
| MEDIUM | 3 | FINDING-04, FINDING-05, FINDING-06 |
| LOW | 2 | FINDING-07, FINDING-08 |
| INFO | 2 | FINDING-09, FINDING-10 |
| **TOTAL** | **10** | |

---

## 5. Prioritised Remediation Order

1. **FINDING-01** (HIGH) — Add `@ToString.Exclude` to `password`, `newPassword`, `accessToken` in `AuthenticationRequest`.
2. **FINDING-02** (HIGH) — Add `@ToString.Exclude` to `accessToken`, `sessionToken` in `AuthenticationResponse`.
3. **FINDING-03** (HIGH) — Mark `password` and `newPassword` as `transient` in `AuthenticationRequest`; review whether `Serializable` is needed.
4. **FINDING-05** (MEDIUM) — Genericise `BeanComparator<T>` and add type-safety checks.
5. **FINDING-06** (MEDIUM) — Validate `methodName` format in `BeanComparator` constructor.
6. **FINDING-04** (MEDIUM) — Remove orphaned `serialVersionUID` from `AuthenticationResponse`.
7. **FINDING-08** (LOW) — Tighten `AuthenticationRequest` construction access control.
8. **FINDING-07** (LOW) — Add logging in `BeanComparator.compare()` catch block.
9. **FINDING-10** (INFO) — Move access tokens from URL parameters to `Authorization` headers in `RestClientService`.
