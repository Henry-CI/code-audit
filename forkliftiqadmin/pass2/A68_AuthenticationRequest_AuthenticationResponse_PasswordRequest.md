# Pass 2 Test Coverage Audit — A68
**Audit Run:** 2026-02-26-01
**Agent ID:** A68
**Date:** 2026-02-26

**Source Files Audited:**
1. `src/main/java/com/cognito/bean/AuthenticationRequest.java`
2. `src/main/java/com/cognito/bean/AuthenticationResponse.java`
3. `src/main/java/com/cognito/bean/PasswordRequest.java`

**Test Directory Searched:** `src/test/java/`

---

## Reading Evidence

### 1. AuthenticationRequest.java

**Class:** `AuthenticationRequest`
**Package:** `com.cognito.bean`
**Implements:** `java.io.Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (with line numbers):**

| Line | Field | Type | Modifier |
|------|-------|------|----------|
| 17 | `serialVersionUID` | `long` | `private static final` |
| 18 | `username` | `String` | `private` |
| 19 | `password` | `String` | `private` |
| 20 | `newPassword` | `String` | `private` |
| 21 | `accessToken` | `String` | `private` |

**Methods (explicitly declared, with line numbers):**

| Line | Method | Modifier | Notes |
|------|--------|----------|-------|
| 24 | `AuthenticationRequest(String username, String password, String newPassword, String accessToken)` | `private` | Builder constructor annotated `@Builder` |

**Lombok-generated methods (via `@Data` and `@NoArgsConstructor`):**
- `AuthenticationRequest()` — no-args constructor
- `getUsername()`, `setUsername(String)`
- `getPassword()`, `setPassword(String)`
- `getNewPassword()`, `setNewPassword(String)`
- `getAccessToken()`, `setAccessToken(String)`
- `equals(Object)`, `hashCode()`, `toString()`
- `AuthenticationRequest.builder()` — Lombok `@Builder` factory method and `AuthenticationRequestBuilder` inner class

**Constants/Enums defined:** None (only `serialVersionUID`)

---

### 2. AuthenticationResponse.java

**Class:** `AuthenticationResponse`
**Package:** `com.cognito.bean`
**Implements:** (none declared; `serialVersionUID` field present but `Serializable` not in `implements` clause)
**Annotations:** `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`

**Fields (with line numbers):**

| Line | Field | Type | Modifier |
|------|-------|------|----------|
| 16 | `serialVersionUID` | `long` | `private static final` |
| 17 | `accessToken` | `String` | `private` |
| 18 | `sessionToken` | `String` | `private` |
| 19 | `expiresIn` | `String` | `private` |
| 20 | `actualDate` | `String` | `private` |
| 21 | `expirationDate` | `String` | `private` |
| 22 | `userData` | `UserResponse` | `private` |
| 23 | `username` | `String` | `private` |
| 24 | `message` | `String` | `private` |
| 25 | `code` | `Integer` | `private` |
| 26 | `detail` | `String` | `private` |

**Methods (explicitly declared):** None declared explicitly.

**Lombok-generated methods (via `@Data` and `@NoArgsConstructor`):**
- `AuthenticationResponse()` — no-args constructor
- `getAccessToken()`, `setAccessToken(String)`
- `getSessionToken()`, `setSessionToken(String)`
- `getExpiresIn()`, `setExpiresIn(String)`
- `getActualDate()`, `setActualDate(String)`
- `getExpirationDate()`, `setExpirationDate(String)`
- `getUserData()`, `setUserData(UserResponse)`
- `getUsername()`, `setUsername(String)`
- `getMessage()`, `setMessage(String)`
- `getCode()`, `setCode(Integer)`
- `getDetail()`, `setDetail(String)`
- `equals(Object)`, `hashCode()`, `toString()`

**Constants/Enums defined:** None (only `serialVersionUID`)

---

### 3. PasswordRequest.java

**Class:** `PasswordRequest`
**Package:** `com.cognito.bean`
**Implements:** `java.io.Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields (with line numbers):**

| Line | Field | Type | Modifier |
|------|-------|------|----------|
| 15 | `serialVersionUID` | `long` | `private static final` |
| 17 | `username` | `String` | `private` |
| 18 | `password` | `String` | `private` |
| 19 | `confirmationCode` | `String` | `private` |
| 20 | `oldPassword` | `String` | `private` |
| 21 | `accessToken` | `String` | `private` |

**Methods (explicitly declared, with line numbers):**

| Line | Method | Modifier | Notes |
|------|--------|----------|-------|
| 24–31 | `PasswordRequest(String username, String password, String confirmationCode, String oldPassword, String accessToken)` | `private` | Builder constructor annotated `@Builder` |

**Lombok-generated methods (via `@Data` and `@NoArgsConstructor`):**
- `PasswordRequest()` — no-args constructor
- `getUsername()`, `setUsername(String)`
- `getPassword()`, `setPassword(String)`
- `getConfirmationCode()`, `setConfirmationCode(String)`
- `getOldPassword()`, `setOldPassword(String)`
- `getAccessToken()`, `setAccessToken(String)`
- `equals(Object)`, `hashCode()`, `toString()`
- `PasswordRequest.builder()` — Lombok `@Builder` factory method and `PasswordRequestBuilder` inner class

**Constants/Enums defined:** None (only `serialVersionUID`)

---

## Test Search Results

Grep for `AuthenticationRequest` in `src/test/java/`: **No files found**
Grep for `AuthenticationResponse` in `src/test/java/`: **No files found**
Grep for `PasswordRequest` in `src/test/java/`: **No files found**

The entire `src/test/java/` tree contains only four test files, none of which reference any of the three audited classes:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

---

## Findings

### AuthenticationRequest

**A68-1 | Severity: CRITICAL | No test class exists for AuthenticationRequest**
There is zero test coverage for `AuthenticationRequest`. No test file referencing this class was found anywhere in `src/test/java/`. All generated and explicit behaviour — construction, getters, setters, builder, equality, serialization — is entirely untested.

**A68-2 | Severity: HIGH | Builder pattern is private and untestable via public API without builder test**
The `@Builder`-annotated constructor at line 24 is `private`. The only supported construction path beyond the no-args constructor is the Lombok-generated `AuthenticationRequest.builder()` static factory. There are no tests verifying that the builder correctly propagates all four fields (`username`, `password`, `newPassword`, `accessToken`) to the constructed object.

**A68-3 | Severity: HIGH | No test for getter/setter round-trip on all four fields**
`@Data` generates getters and setters for `username` (line 18), `password` (line 19), `newPassword` (line 20), and `accessToken` (line 21). No test verifies that values set via setters are returned unchanged by the corresponding getters, including boundary cases (null, empty string, special characters).

**A68-4 | Severity: MEDIUM | No test for equals() and hashCode() contract on AuthenticationRequest**
Lombok's `@Data`-generated `equals()` and `hashCode()` use all non-static fields. There are no tests confirming reflexivity, symmetry, transitivity, or that two instances with identical field values produce the same hash code, nor that null fields are handled without a NullPointerException.

**A68-5 | Severity: MEDIUM | No test for toString() on AuthenticationRequest**
`@Data` generates a `toString()` including the `password` field. There is no test asserting the format or confirming that sensitive credential fields (`password`, `newPassword`, `accessToken`) are not inadvertently included in log output — a secondary security hygiene concern.

**A68-6 | Severity: LOW | No serialization round-trip test for AuthenticationRequest**
`AuthenticationRequest` declares `serialVersionUID = 152396558777730489L` and implements `Serializable`. There is no test verifying that a populated instance serializes and deserializes to an equal object, nor that the `serialVersionUID` constant is stable against future field changes.

---

### AuthenticationResponse

**A68-7 | Severity: CRITICAL | No test class exists for AuthenticationResponse**
There is zero test coverage for `AuthenticationResponse`. No test file referencing this class was found anywhere in `src/test/java/`. This class is the primary authentication result object and contains security-sensitive fields (`accessToken`, `sessionToken`).

**A68-8 | Severity: HIGH | serialVersionUID declared but Serializable not implemented — no test to detect the inconsistency**
`AuthenticationResponse` declares `private static final long serialVersionUID = 408336884318011949L` at line 16 but does not declare `implements Serializable` in its class signature. This makes `serialVersionUID` a no-op dead field. No test exists that would detect serialization failure or catch this structural inconsistency. This is also a latent defect (see Pass 1 scope), but coverage is the direct concern here.

**A68-9 | Severity: HIGH | No test for @JsonInclude(NON_NULL) behaviour**
`@JsonInclude(JsonInclude.Include.NON_NULL)` at line 11 means null fields are excluded from JSON serialization. There are no tests verifying that null fields are absent from serialized JSON output and that non-null fields are present. Given this class is used in API authentication responses, this Jackson behaviour is critical to contract correctness.

**A68-10 | Severity: HIGH | No test for getter/setter round-trip on all ten fields**
`@Data` generates getters and setters for `accessToken` (17), `sessionToken` (18), `expiresIn` (19), `actualDate` (20), `expirationDate` (21), `userData` (22), `username` (23), `message` (24), `code` (25), and `detail` (26). No test verifies any field assignment or retrieval, including null-safety for the `Integer code` field.

**A68-11 | Severity: MEDIUM | No test for equals() and hashCode() contract on AuthenticationResponse**
Lombok's `@Data`-generated `equals()` and `hashCode()` apply to all ten fields including the `UserResponse userData` object reference. There are no tests for the equality contract, and deep equality through the `userData` nested object is unverified.

**A68-12 | Severity: MEDIUM | No test for toString() on AuthenticationResponse**
`@Data` generates a `toString()` that will include `accessToken` and `sessionToken`. There is no test asserting format correctness, nor any test that would identify accidental exposure of bearer tokens in log strings.

**A68-13 | Severity: LOW | No test for null userData field handling**
The `userData` field at line 22 is of type `UserResponse`, a complex object. There is no test ensuring that an `AuthenticationResponse` with a null `userData` behaves correctly across getters, `equals()`, `hashCode()`, and `toString()` without throwing a NullPointerException.

---

### PasswordRequest

**A68-14 | Severity: CRITICAL | No test class exists for PasswordRequest**
There is zero test coverage for `PasswordRequest`. No test file referencing this class was found anywhere in `src/test/java/`. This class carries highly sensitive fields (`password`, `confirmationCode`, `oldPassword`, `accessToken`) used in password reset and change flows.

**A68-15 | Severity: HIGH | Builder pattern is private and untestable via public API without builder test**
The `@Builder`-annotated constructor at lines 24–31 is `private`. The Lombok-generated `PasswordRequest.builder()` is the only multi-field construction path. There are no tests verifying that the builder correctly maps all five fields (`username`, `password`, `confirmationCode`, `oldPassword`, `accessToken`) to the constructed object, including partial population where some fields remain null.

**A68-16 | Severity: HIGH | No test for getter/setter round-trip on all five fields**
`@Data` generates getters and setters for `username` (17), `password` (18), `confirmationCode` (19), `oldPassword` (20), and `accessToken` (21). No test verifies any get/set round-trip, null handling, or mutual independence of field values.

**A68-17 | Severity: MEDIUM | No test for equals() and hashCode() contract on PasswordRequest**
Lombok's `@Data`-generated `equals()` and `hashCode()` use all five fields. There are no tests confirming the standard equality contract, including cases where sensitive fields differ only by case or whitespace.

**A68-18 | Severity: MEDIUM | No test for toString() on PasswordRequest**
`@Data` generates a `toString()` that will include `password`, `oldPassword`, `confirmationCode`, and `accessToken` in plain text. There is no test confirming the output format, and no test that would catch accidental credential leakage into logs or exception messages.

**A68-19 | Severity: LOW | No serialization round-trip test for PasswordRequest**
`PasswordRequest` declares `serialVersionUID = 6722563341130946506L` and implements `Serializable`. There is no test verifying serialize/deserialize round-trip equality for a fully populated instance, nor for an instance where only some fields are set.

---

## Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A68-1 | CRITICAL | AuthenticationRequest | No test class exists |
| A68-2 | HIGH | AuthenticationRequest | Builder construction path untested |
| A68-3 | HIGH | AuthenticationRequest | No getter/setter round-trip tests |
| A68-4 | MEDIUM | AuthenticationRequest | No equals/hashCode contract tests |
| A68-5 | MEDIUM | AuthenticationRequest | No toString() test; password in output |
| A68-6 | LOW | AuthenticationRequest | No serialization round-trip test |
| A68-7 | CRITICAL | AuthenticationResponse | No test class exists |
| A68-8 | HIGH | AuthenticationResponse | serialVersionUID declared but Serializable not implemented; undetected by any test |
| A68-9 | HIGH | AuthenticationResponse | @JsonInclude(NON_NULL) behaviour untested |
| A68-10 | HIGH | AuthenticationResponse | No getter/setter round-trip tests for all 10 fields |
| A68-11 | MEDIUM | AuthenticationResponse | No equals/hashCode contract tests |
| A68-12 | MEDIUM | AuthenticationResponse | No toString() test; tokens in output |
| A68-13 | LOW | AuthenticationResponse | No null userData handling test |
| A68-14 | CRITICAL | PasswordRequest | No test class exists |
| A68-15 | HIGH | PasswordRequest | Builder construction path untested |
| A68-16 | HIGH | PasswordRequest | No getter/setter round-trip tests |
| A68-17 | MEDIUM | PasswordRequest | No equals/hashCode contract tests |
| A68-18 | MEDIUM | PasswordRequest | No toString() test; credentials in output |
| A68-19 | LOW | PasswordRequest | No serialization round-trip test |

**Total findings: 19**
- CRITICAL: 3
- HIGH: 7
- MEDIUM: 6
- LOW: 3
