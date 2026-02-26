# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A101
**Date:** 2026-02-26
**Scope:** ReportService, ReportServiceException, RestClientService

---

## 1. Reading Evidence

### 1.1 ReportService
**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/service/ReportService.java`
**Class name:** `ReportService`

| Element | Type | Line |
|---|---|---|
| `resultDAO` | field (private) | 15 |
| `incidentReportDAO` | field (private) | 16 |
| `impactReportDAO` | field (private) | 17 |
| `theInstance` | field (private static) | 18 |
| `getInstance()` | method (public static) | 20 |
| `ReportService()` | constructor (private) | 29 |
| `countPreOpsCompletedToday(Long compId, String timezone)` | method (public) | 32 |
| `getPreOpsCheckReport(Long compId, PreOpsReportFilterBean filter, String dateFormat, String timezone)` | method (public) | 41 |
| `getIncidentReport(int compId, IncidentReportFilterBean filter, String dateFormat, String timezone)` | method (public) | 53 |
| `countImpactsToday(Long compId, String timezone)` | method (public) | 65 |
| `getImpactReport(Long compId, ImpactReportFilterBean filter, String dateFormat, String timezone)` | method (public) | 76 |
| `getSessionReport(int compId, SessionFilterBean filter, String dateFormat, String timezone)` | method (public) | 90 |

---

### 1.2 ReportServiceException
**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/service/ReportServiceException.java`
**Class name:** `ReportServiceException`

| Element | Type | Line |
|---|---|---|
| `ReportServiceException(String message)` | constructor (public) | 4 |
| `ReportServiceException(String message, Throwable cause)` | constructor (public) | 8 |

No fields declared (no serialVersionUID).

---

### 1.3 RestClientService
**File:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/service/RestClientService.java`
**Class name:** `RestClientService`

| Element | Type | Line |
|---|---|---|
| `log` | field (private static Logger) | 33 |
| `COGNITO_API_PORT` | field (private final String) | 35 |
| `authenticationRequest(AuthenticationRequest authenticationRequest)` | method (public) | 37 |
| `signUpRequest(UserSignUpRequest signUpRequest)` | method (public) | 72 |
| `resetPassword(PasswordRequest resetPasswordRequest)` | method (public) | 107 |
| `confirmResetPassword(PasswordRequest resetPasswordRequest)` | method (public) | 142 |
| `getUser(String username, String accessToken)` | method (public) | 177 |
| `getUserList(List<UserRequest> userRequestList, String accessToken)` | method (public) | 213 |
| `updateUser(UserUpdateRequest userUpdateRequest)` | method (public) | 250 |
| `deleteUser(String username, String sessionToken)` | method (public) | 284 |

---

## 2. Test Directory Search Results

**Test directory searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Test files found (entire suite):**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep for `ReportService`, `ReportServiceException`, `RestClientService` across all test files:** No matches found.

None of the four existing test files reference any of the three audited classes in any capacity — not as imports, not as string literals, not as comments.

---

## 3. Findings

---

### ReportService

---

**A101-1 | Severity: CRITICAL | No test class exists for ReportService**

There is no test file for `ReportService` anywhere under the test source root. Zero of the six public methods (`countPreOpsCompletedToday`, `getPreOpsCheckReport`, `getIncidentReport`, `countImpactsToday`, `getImpactReport`, `getSessionReport`) are exercised by any test. All business logic delegated through this service layer is unverified at the unit-test level.

---

**A101-2 | Severity: HIGH | Broken singleton — double-checked locking is incomplete**

`getInstance()` (line 20–27) checks `theInstance == null` outside the synchronized block but does not re-check inside it. Any JVM without a memory-model guarantee (pre-Java 5 or without a `volatile` declaration) can observe a partially constructed object. The field `theInstance` is not declared `volatile`. There is no test that exercises concurrent instantiation, and there is no test that verifies exactly one instance is returned across multiple calls.

---

**A101-3 | Severity: HIGH | SQLException error path untested for all five delegating methods**

Each of `countPreOpsCompletedToday`, `getPreOpsCheckReport`, `getIncidentReport`, `countImpactsToday`, and `getImpactReport` wraps a DAO call and converts `SQLException` to `ReportServiceException`. No test mocks the DAO to throw `SQLException` and verifies that the conversion and message content are correct.

---

**A101-4 | Severity: HIGH | `getSessionReport` declares no checked exception but throws `ReportServiceException` unchecked — and the error message is wrong**

`getSessionReport` (line 90–99) has no `throws` clause in its signature, yet the catch block (line 97) throws `new ReportServiceException("Unable to get impact report for compId : " + compId, e)`. The error message says "impact report" rather than "session report" — a copy-paste defect that would mislead operators diagnosing production failures. No test verifies the exception message or that the exception propagates at all.

---

**A101-5 | Severity: MEDIUM | `countImpactsToday` and `getImpactReport` use `assert` for null-guard — assertions are disabled by default in production JVMs**

Lines 67 and 81 use Java `assert compId != null` to enforce a non-null precondition. JVM assertions are disabled at runtime unless explicitly enabled with `-ea`. A `null` compId will silently pass the guard and likely produce a `NullPointerException` inside the DAO rather than a meaningful error. No test verifies the null-argument behaviour under either assertion-enabled or assertion-disabled conditions, and no test confirms what exception (if any) is surfaced to callers.

---

**A101-6 | Severity: MEDIUM | DAO fields are hardwired via `new` / static factory — not injectable, blocking unit testing**

`resultDAO` (line 15) is instantiated with `new ResultDAO()`, `incidentReportDAO` (line 16) with `new IncidentReportDAO()`, and `impactReportDAO` (line 17) via `ImpactReportDAO.getInstance()`. Because there is no constructor injection or setter injection, it is impossible to substitute mock DAOs in a unit test without bytecode manipulation. This architectural decision is the root cause of the complete absence of unit tests for this class.

---

**A101-7 | Severity: LOW | Happy-path return values are never asserted**

Even if DAO mocks could be injected, no test verifies that the return value of any method is the same object returned by the underlying DAO call. For example, `countPreOpsCompletedToday` should return exactly what `resultDAO.countResultsCompletedToday` returns, but no assertion exists.

---

**A101-8 | Severity: LOW | `getInstance()` singleton state leaks between tests**

`theInstance` is a static field with no reset mechanism. If any future test exercises `getInstance()`, the singleton created in one test will persist into subsequent tests, making test order significant and preventing isolated testing of the constructor path.

---

### ReportServiceException

---

**A101-9 | Severity: CRITICAL | No test class exists for ReportServiceException**

There is no test file for `ReportServiceException`. Neither constructor is exercised by any test.

---

**A101-10 | Severity: HIGH | Both constructors are completely untested**

`ReportServiceException(String message)` (line 4) and `ReportServiceException(String message, Throwable cause)` (line 8) have no tests verifying that `getMessage()` returns the supplied string, that `getCause()` returns the supplied `Throwable`, or that the class extends `RuntimeException` (and is therefore unchecked).

---

**A101-11 | Severity: MEDIUM | Missing `serialVersionUID` for a `Serializable` subclass**

`ReportServiceException` extends `RuntimeException`, which implements `java.io.Serializable`. No `serialVersionUID` constant is declared. The JVM will compute a default UID based on class structure; any change to the class (adding fields, changing method signatures) will silently break deserialization of any serialized exception captured in logs or transferred across a wire. No test checks serialization round-trip behaviour.

---

### RestClientService

---

**A101-12 | Severity: CRITICAL | No test class exists for RestClientService**

There is no test file for `RestClientService`. All eight public methods are completely untested.

---

**A101-13 | Severity: CRITICAL | Hardcoded localhost URL in all eight methods — no test verifies correct base URL construction**

Every method constructs its URL using the string literal `"http://localhost:"` concatenated with `COGNITO_API_PORT` (`"9090"`). The URLs are:
- Line 53: `http://localhost:9090/auth`
- Line 88: `http://localhost:9090/auth/SignUp`
- Line 123: `http://localhost:9090/auth/ResetPassword`
- Line 158: `http://localhost:9090/auth/ConfirmResetPassword`
- Line 192: `http://localhost:9090/auth/user?username=...&accessToken=...`
- Line 228: `http://localhost:9090/auth/user-list?accessToken=...`
- Line 265: `http://localhost:9090/auth/update`
- Line 297: `http://localhost:9090/auth/delete_user?accessToken=...&email=...`

The host and port are not configurable via properties, environment variables, or dependency injection. This means: (a) the service can never contact a non-localhost endpoint without a code change, (b) it cannot be reconfigured for different environments (dev, staging, production), and (c) no test verifies what URL is actually sent to the HTTP client.

---

**A101-14 | Severity: CRITICAL | `RestTemplate` is instantiated inside every method — cannot be mocked in tests**

Each of the eight methods creates its own `new RestTemplate()` on the first line. Because `RestTemplate` is not injected, no test can substitute a mock or stub HTTP client to simulate HTTP responses, network failures, or non-200 status codes. All HTTP interaction paths are completely unreachable in unit tests without bytecode manipulation.

---

**A101-15 | Severity: HIGH | Network failure / exception swallowing in all eight methods — callers receive default empty objects**

Every method wraps its HTTP call in a `try/catch(Exception e)` block (lines 63–67, 98–102, 133–137, 168–172, 204–208, 241–245, 275–279, 301–305). On any exception — including `RestClientException`, `URISyntaxException`, or `ResourceAccessException` (connection refused, timeout) — the exception is only printed to stderr and logged; the method then silently returns a default empty response object (or `"Deleted"` for `deleteUser`). No test verifies this behaviour, and callers have no programmatic way to distinguish a successful empty response from a failed call.

---

**A101-16 | Severity: HIGH | Non-200 HTTP status is silently ignored in all eight methods**

The `else` branches on lines 60–62, 95–97, 130–132, 165–167, 201–203, 238–240, 272–274, and 303 only log an info message when the HTTP response status is not 200 OK. The method then falls through and returns the default empty response object. No exception is raised, no error flag is set, and no test verifies the non-200 path or confirms that callers can detect a failure.

---

**A101-17 | Severity: HIGH | `deleteUser` always returns `"Deleted"` regardless of actual outcome**

`deleteUser` (line 284–309) calls `restTemplate.delete(uri)` and, whether the call succeeds or throws an exception, always returns the string `"Deleted"` (line 308). A network failure or a 404/500 response from the Cognito API is indistinguishable from a successful deletion. No test verifies this behaviour or checks the return value under failure conditions.

---

**A101-18 | Severity: HIGH | `getUser` URL construction appends raw, un-encoded query parameters**

`getUser` (line 192) builds its URL by string-concatenating `username` and `accessToken` directly into the query string without URL-encoding either value:

```java
String baseUrl = "http://localhost:"+COGNITO_API_PORT+"/auth/user?username="+username+"&accessToken="+accessToken;
```

A username or access token containing `&`, `=`, `+`, spaces, or other reserved characters will silently corrupt the URL. `deleteUser` (line 297) uses `URLEncoder.encode(username)` (without a charset argument — see A101-19), but `getUser` does not encode `username` at all, and neither method encodes `accessToken`. No test supplies special characters to verify encoding behaviour.

---

**A101-19 | Severity: HIGH | `deleteUser` calls the deprecated `URLEncoder.encode(String)` without specifying a charset**

Line 297 calls `URLEncoder.encode(username)` with a single argument. This overload is deprecated since Java 1.4 and relies on the platform default encoding, which may differ between development and production environments and can cause silent encoding mismatches. No test verifies the encoding behaviour or exercises usernames with non-ASCII characters.

---

**A101-20 | Severity: MEDIUM | `getUserList` — `result.getBody()` may return null, causing NullPointerException**

`getUserList` (line 234) calls `Arrays.asList(result.getBody())` without a null check on `getBody()`. If the HTTP response has no body (204 No Content, or a body that fails deserialization), `getBody()` returns `null` and `Arrays.asList(null)` produces a single-element list containing `null` rather than an empty list. This would propagate silently to callers as a list with one null element. No test exercises an empty-body response.

---

**A101-21 | Severity: MEDIUM | `getUser` uses a deprecated `URI` construction path and does not validate the URI before use**

Line 193 constructs `new URI(baseUrl)` where `baseUrl` is built by direct string concatenation. If `username` or `accessToken` contain characters that are illegal in a URI (such as spaces), `new URI(baseUrl)` will throw `URISyntaxException`, which is caught by the blanket `catch(Exception e)` and swallowed (see A101-15). No test supplies an invalid URI character to verify this failure mode.

---

**A101-22 | Severity: MEDIUM | Log message in `getUser` catch block references wrong method name**

Line 207: `log.error("authenticationRequest error:"+ e.getMessage())` — the log prefix says `authenticationRequest` but the method is `getUser`. This copy-paste error will produce misleading log output in production when `getUser` fails. No test verifies log output.

---

**A101-23 | Severity: MEDIUM | `COGNITO_API_PORT` is a hardcoded string constant with no external configuration**

The port `"9090"` is declared as `private final String COGNITO_API_PORT = "9090"` (line 35) with no mechanism to override it via system property, environment variable, or application configuration. If the Cognito sidecar ever moves to a different port, every method URL must be manually updated. No test verifies the port value used in outbound requests.

---

**A101-24 | Severity: LOW | `RestClientService` has no no-arg constructor or singleton control**

Unlike `ReportService`, `RestClientService` is not a singleton and has no documented instantiation contract. Callers instantiate it directly with `new RestClientService()`. There is no test verifying how many instances are created in practice or whether shared state (e.g., the static `log` field) behaves correctly under concurrent use.

---

**A101-25 | Severity: LOW | Typo "Succuss" in log messages across multiple methods**

Log messages in `authenticationRequest` (line 57), `signUpRequest` (line 92), `resetPassword` (line 127), `confirmResetPassword` (line 162), `getUser` (line 198), `getUserList` (line 235) read `"HttpStatus Succuss"` (double-s). The correct spelling is "Success". `updateUser` (line 269) spells it correctly (`"HttpStatus Success"`). No test verifies log output, so this inconsistency is invisible in the test record.

---

## 4. Coverage Summary

| Class | Test File Exists | Methods Tested | Methods Total | Coverage |
|---|---|---|---|---|
| `ReportService` | No | 0 | 6 public | 0% |
| `ReportServiceException` | No | 0 | 2 constructors | 0% |
| `RestClientService` | No | 0 | 8 public | 0% |

**Total findings: 25**

| Severity | Count |
|---|---|
| CRITICAL | 5 |
| HIGH | 10 |
| MEDIUM | 7 |
| LOW | 3 |
