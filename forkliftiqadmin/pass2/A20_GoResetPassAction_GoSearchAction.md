# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A20
**Date:** 2026-02-26
**Scope:** `GoResetPassAction.java`, `GoSearchAction.java`
**Project:** forkliftiqadmin (Java / Struts 1 / Tomcat)

---

## 1. Reading Evidence

### 1.1 GoResetPassAction

**File:** `src/main/java/com/action/GoResetPassAction.java`
**Package:** `com.action`
**Class:** `GoResetPassAction extends org.apache.struts.action.Action`
**Modifier:** public (no `final`)

**Fields / Constants defined in class:** none (no instance fields or static fields declared directly in this class)

**Imports (runtime dependencies):**
| Import | Purpose |
|---|---|
| `javax.servlet.http.HttpServletRequest` | Servlet request |
| `javax.servlet.http.HttpServletResponse` | Servlet response |
| `javax.servlet.http.HttpSession` | Session access |
| `org.apache.struts.action.Action` | Struts base class |
| `org.apache.struts.action.ActionForm` | Struts form bean |
| `org.apache.struts.action.ActionForward` | Struts navigation result |
| `org.apache.struts.action.ActionMapping` | Struts mapping |
| `com.cognito.bean.PasswordRequest` | Request payload bean (Lombok builder) |
| `com.cognito.bean.PasswordResponse` | Response payload bean |
| `com.service.RestClientService` | HTTP REST client (hard-instantiated) |
| `com.util.RuntimeConf` | Static config constant `HTTP_OK = 200` |

**Methods:**

| # | Method | Line | Return | Overrides |
|---|---|---|---|---|
| 1 | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 19 | `ActionForward` | Yes (`@Override` of `Action.execute`) |

**Branches inside `execute` (line 19-47):**

| Branch ID | Condition | Line | Forward returned |
|---|---|---|---|
| B1 | `action.equalsIgnoreCase("getcode")` is true | 27-30 | `"getcode"` |
| B2 | `action.equalsIgnoreCase("reset")` is true AND `passwordResponse.getCode().equals(HTTP_OK)` is true | 31-38 | `"reset"` |
| B3 | `action.equalsIgnoreCase("reset")` is true AND `passwordResponse.getCode()` is not HTTP_OK | 39-42 | `"getcode"` |
| B4 | `action` is neither `"getcode"` nor `"reset"` (default/else) | 43-46 | `"home"` |

**Struts mapping (struts-config.xml lines 115-121):**
```xml
<action path="/goResetPass" type="com.action.GoResetPassAction">
    <forward name="getcode" path="getCodeDefinition"/>
    <forward name="reset"   path="resetPassDefinition"/>
    <forward name="home"    path="loginDefinition"/>
</action>
```

---

### 1.2 GoSearchAction

**File:** `src/main/java/com/action/GoSearchAction.java`
**Package:** `com.action`
**Class:** `GoSearchAction extends org.apache.struts.action.Action`
**Modifier:** `public final`

**Fields / Constants defined in class:**

| Field | Type | Modifier | Line | Value |
|---|---|---|---|---|
| `log` | `org.apache.log4j.Logger` | `private static` | 22 | `InfoLogger.getLogger("com.action.GoSearchAction")` |

**Imports (runtime dependencies):**
| Import | Purpose |
|---|---|
| `javax.servlet.http.HttpServletRequest` | Servlet request |
| `javax.servlet.http.HttpServletResponse` | Servlet response |
| `javax.servlet.http.HttpSession` | Session access |
| `org.apache.struts.action.Action` | Struts base class |
| `org.apache.struts.action.ActionForm` | Struts form bean |
| `org.apache.struts.action.ActionForward` | Struts navigation result |
| `org.apache.struts.action.ActionMapping` | Struts mapping |
| `org.apache.log4j.Logger` | Logging |
| `com.util.InfoLogger` | Logger factory |

**Methods:**

| # | Method | Line | Return | Overrides |
|---|---|---|---|---|
| 1 | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 24 | `ActionForward` | Yes (no `@Override` annotation, but overrides `Action.execute`) |

**Branches inside `execute` (line 24-30):** None — linear execution only.

**Struts mapping (struts-config.xml lines 178-182):**
```xml
<action path="/goSerach" type="com.action.GoSearchAction">
    <forward name="goSearch" path="searchDefinition"/>
</action>
```
Note: the mapped path `/goSerach` contains a typo (missing `r`); the correct word would be `/goSearch`.

---

## 2. Test Directory Coverage Confirmation

**Test files in project:**
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

All four test files reside in `com.calibration` and `com.util` packages. None are in `com.action`.

**Grep results for class names across entire test directory:**

| Search term | Matches found |
|---|---|
| `GoResetPassAction` | 0 |
| `GoSearchAction` | 0 |

**Conclusion:** Zero direct or indirect test coverage exists for either action class.

---

## 3. Coverage Gap Findings

---

### GoResetPassAction

---

**A20-1 | Severity: CRITICAL | No test class exists for GoResetPassAction**

`GoResetPassAction` has zero test coverage. The class is an authentication-sensitive Struts action that handles password reset flows communicating with AWS Cognito. Not a single unit test, integration test, or mock-based test exists. Any regression in branching logic, null handling, or service interaction is completely undetected.

---

**A20-2 | Severity: CRITICAL | Null session causes NullPointerException — no null guard on session**

At line 22, `request.getSession(false)` is called, which returns `null` if no session exists. The return value is assigned directly to `session` and then used at line 25 without any null check:

```java
HttpSession session = request.getSession(false);          // line 22 — may be null
...
String accessToken = session.getAttribute("accessToken")  // line 25 — NPE if session is null
```

If an unauthenticated request (no active session) reaches `/goResetPass`, the action throws `NullPointerException` at line 25. There is no test that verifies this path, and no test that verifies graceful handling (e.g., redirect to login). This is a reliability and potentially a security concern: an attacker who can hit the endpoint without a session will trigger an unhandled server error which may leak stack trace details depending on container error handling configuration.

---

**A20-3 | Severity: CRITICAL | Null pointer risk on passwordResponse.getCode() — no null guard**

At line 36:
```java
if(passwordResponse.getCode().equals(RuntimeConf.HTTP_OK))
```

`PasswordResponse.getCode()` returns `Integer` (a nullable boxed type, as defined in `PasswordResponse.java` line 22: `private Integer code;`). If `RestClientService.resetPassword()` returns a `PasswordResponse` with `code` field null (which happens when the REST call fails or returns a non-200 HTTP status — `RestClientService` constructs a default `new PasswordResponse()` in the catch block, leaving all fields null), calling `.equals()` on the null `Integer` throws `NullPointerException`. No test covers this failure path.

---

**A20-4 | Severity: HIGH | RestClientService is hard-instantiated — untestable without live network**

At line 33:
```java
RestClientService restClientServce = new RestClientService();
```

`RestClientService` is instantiated directly inside the `execute` method rather than injected. This makes it impossible to unit test the `"reset"` branch without a live Cognito API running on `localhost:9090`. No test exists that mocks or stubs `RestClientService`, meaning the entire "reset" flow (branches B2 and B3) cannot be tested in isolation. This is an architectural testability defect.

---

**A20-5 | Severity: HIGH | Branch B2 ("reset" action, HTTP 200 response) is never tested**

The forward `"reset"` (mapping to `resetPassDefinition`) is returned only when `action == "reset"` AND `passwordResponse.getCode() == 200`. No test exercises this path. A regression here would silently break the successful password reset user journey.

---

**A20-6 | Severity: HIGH | Branch B3 ("reset" action, non-200 response) is never tested**

The forward `"getcode"` returned on a non-OK API response (lines 39-42) is never tested. This is the error/retry path for a failed password reset; a regression here would leave users stranded with no indication of failure.

---

**A20-7 | Severity: HIGH | Branch B1 ("getcode" action) is never tested**

The forward `"getcode"` returned when `action.equalsIgnoreCase("getcode")` (lines 27-30) is never tested. This is the entry point to the OTP/confirmation code flow; a regression here would prevent users from initiating password reset.

---

**A20-8 | Severity: HIGH | Default branch B4 (unknown action, forward "home") is never tested**

When `action` is neither `"getcode"` nor `"reset"` (lines 43-46), the action forwards to `"home"` (loginDefinition). This includes the case where `action` is an empty string (which is the default value when the request parameter is absent). No test verifies this default routing.

---

**A20-9 | Severity: MEDIUM | Null request parameter "action" produces empty string, not null — behavior not documented or tested**

Lines 23-24 use a ternary to convert a null `action` parameter to `""`:
```java
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
```
The empty string `""` falls into branch B4 and returns forward `"home"`. This is the implicit behavior when no `action` parameter is supplied. No test asserts this is the intended behavior, and the absence of `action` is not documented.

---

**A20-10 | Severity: MEDIUM | Null request parameter "username" produces empty string — empty username passed to Cognito API without validation**

Lines 23-24 convert a null or absent `username` parameter to `""`. An empty string username is silently passed to `PasswordRequest.builder().username("").build()` and forwarded to the Cognito REST API. No test verifies that an empty username is rejected before a network call is made, and no input validation exists at the action layer.

---

**A20-11 | Severity: MEDIUM | "accessToken" absent from session produces empty string — no authentication enforcement in action**

Line 25 converts a missing `accessToken` session attribute to `""`. An empty access token is then sent to the Cognito reset-password API. There is no check that the user is authenticated before attempting the reset. No test verifies behavior when the session has no access token.

---

**A20-12 | Severity: MEDIUM | Case-insensitive action dispatch not tested for mixed-case variants**

The action string is compared with `equalsIgnoreCase`, meaning `"GetCode"`, `"GETCODE"`, `"RESET"`, `"Reset"` etc. all route differently from empty or other strings. No test verifies that case-insensitive matching works correctly or that unexpected casing does not produce an unintended forward.

---

**A20-13 | Severity: MEDIUM | Exception propagation from RestClientService.resetPassword() is not handled or tested**

`RestClientService.resetPassword()` internally catches all exceptions and returns a default `PasswordResponse`, but the action's `execute` method declares `throws Exception`. If an uncaught exception were ever thrown from the service layer, it would propagate to the Struts framework. No test verifies the exception boundary behavior between the action and the service.

---

**A20-14 | Severity: LOW | Typo in variable name "restClientServce" — not a functional bug but indicates low code quality**

Line 33:
```java
RestClientService restClientServce = new RestClientService();
```
The variable is spelled `restClientServce` (missing the `i` in `Service`). This is a cosmetic code-quality issue; no test enforces naming standards or exercises code review tooling.

---

**A20-15 | Severity: LOW | No @Override annotation on GoResetPassAction.execute() — not caught by compiler**

`GoResetPassAction` overrides `Action.execute()` without the `@Override` annotation (unlike the explicit `@Override` on line 18 which is the annotation). Actually reviewing: line 18 does show `@Override` is present. This item is retracted — annotation is correctly present.

*Retracted — @Override is present at line 18.*

---

### GoSearchAction

---

**A20-15 | Severity: CRITICAL | No test class exists for GoSearchAction**

`GoSearchAction` has zero test coverage. No unit test, integration test, or mock-based test exists for any aspect of the class.

---

**A20-16 | Severity: CRITICAL | Null session causes NullPointerException — getSession(false) return not null-checked**

Line 27:
```java
HttpSession theSession = request.getSession(false);   // may return null
theSession.removeAttribute("arrDriver");              // NPE if no active session
```

`request.getSession(false)` returns `null` when no session exists. `theSession.removeAttribute("arrDriver")` immediately dereferences it with no null guard. An unauthenticated GET to `/goSerach` produces an unhandled `NullPointerException`. No test exercises the no-session case.

---

**A20-17 | Severity: HIGH | execute() always removes "arrDriver" regardless of whether attribute exists — no conditional check, no test**

`theSession.removeAttribute("arrDriver")` at line 28 always executes unconditionally. If `"arrDriver"` is not present in the session, `removeAttribute` is a no-op per the Servlet API, so this is not a functional bug on its own. However, no test verifies that the attribute is correctly removed when it is present, nor that subsequent calls to `mapping.findForward("goSearch")` succeed after the removal. A regression that accidentally removes the wrong attribute or fails to remove the expected one would go undetected.

---

**A20-18 | Severity: HIGH | The only forward "goSearch" is never tested**

`mapping.findForward("goSearch")` at line 29 is the sole navigation outcome of this action. No test verifies that this forward is returned, that the mapping key is spelled correctly, or that the tiles definition `searchDefinition` resolves correctly.

---

**A20-19 | Severity: MEDIUM | @Override annotation absent on GoSearchAction.execute()**

`GoSearchAction.execute()` at line 24 overrides `Action.execute()` but is not annotated with `@Override`. Without the annotation, if the parent class signature ever changed (e.g., in a Struts upgrade), the compiler would silently treat the method as a new override instead of flagging a mismatch. No test catches this scenario.

---

**A20-20 | Severity: MEDIUM | Static logger field initialized via InfoLogger.getLogger() — failure during class loading not tested**

Line 22:
```java
private static Logger log = InfoLogger.getLogger("com.action.GoSearchAction");
```

`InfoLogger` has a static initializer that calls `PropertyConfigurator.configure(...)`. If the log4j properties file is absent from the classpath, the static initializer catches and swallows the exception, then `getLogger` still returns a logger. No test verifies that the logging infrastructure initializes correctly in the test environment, and a misconfigured logging setup would silently produce no log output.

---

**A20-21 | Severity: MEDIUM | Struts action path "/goSerach" contains a typo — not covered by any test**

The struts-config.xml mapping uses path `/goSerach` (line 179) instead of `/goSearch`. This typo means the URL clients must use is non-intuitive. No test validates the mapped URL path, so a correction of the typo in struts-config.xml could break existing clients without any test failure to signal it.

---

**A20-22 | Severity: LOW | "arrDriver" session attribute key is a bare string literal — no constant, no test for key correctness**

The session attribute name `"arrDriver"` (line 28) is a raw string literal with no defined constant. If the same key is used elsewhere under a different spelling, no test catches the inconsistency. A typo in this string would silently fail (removeAttribute is a no-op for non-existent keys), leaving stale data in the session.

---

**A20-23 | Severity: LOW | `log` field declared but never used in execute() — dead code**

`private static Logger log` is declared at line 22 but is never invoked anywhere within `GoSearchAction.execute()`. No log statements exist in the method. The field is dead code. No static analysis or test enforces that logging is present for auditing or debugging of this action.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A20-1 | CRITICAL | GoResetPassAction | No test class exists |
| A20-2 | CRITICAL | GoResetPassAction | `getSession(false)` result not null-checked; NPE on unauthenticated request |
| A20-3 | CRITICAL | GoResetPassAction | `passwordResponse.getCode()` can be null; NPE on `.equals()` call |
| A20-4 | HIGH | GoResetPassAction | `RestClientService` hard-instantiated; action untestable without live network |
| A20-5 | HIGH | GoResetPassAction | Branch B2 ("reset" + HTTP 200) never tested |
| A20-6 | HIGH | GoResetPassAction | Branch B3 ("reset" + non-200) never tested |
| A20-7 | HIGH | GoResetPassAction | Branch B1 ("getcode") never tested |
| A20-8 | HIGH | GoResetPassAction | Branch B4 (default/else/"home") never tested |
| A20-9 | MEDIUM | GoResetPassAction | Empty-string default for null `action` param — behavior undocumented, untested |
| A20-10 | MEDIUM | GoResetPassAction | Empty-string default for null `username` — passed to Cognito without validation |
| A20-11 | MEDIUM | GoResetPassAction | Empty-string default for missing `accessToken` — no auth enforcement |
| A20-12 | MEDIUM | GoResetPassAction | Case-insensitive dispatch variants not tested |
| A20-13 | MEDIUM | GoResetPassAction | Exception propagation from RestClientService not handled or tested |
| A20-14 | LOW | GoResetPassAction | Typo in local variable name `restClientServce` |
| A20-15 | CRITICAL | GoSearchAction | No test class exists |
| A20-16 | CRITICAL | GoSearchAction | `getSession(false)` result not null-checked; NPE on unauthenticated request |
| A20-17 | HIGH | GoSearchAction | `removeAttribute("arrDriver")` unconditional, no test for attribute removal correctness |
| A20-18 | HIGH | GoSearchAction | Forward `"goSearch"` never tested |
| A20-19 | MEDIUM | GoSearchAction | `@Override` annotation absent on `execute()` |
| A20-20 | MEDIUM | GoSearchAction | Static logger initialization failure not tested |
| A20-21 | MEDIUM | GoSearchAction | Struts path `/goSerach` is a typo — untested, could break clients if corrected |
| A20-22 | LOW | GoSearchAction | `"arrDriver"` is a bare string literal with no constant definition |
| A20-23 | LOW | GoSearchAction | `log` field declared but never used — dead code |

---

## 5. Severity Counts

| Severity | Count |
|---|---|
| CRITICAL | 5 |
| HIGH | 7 |
| MEDIUM | 7 |
| LOW | 4 |
| **Total** | **23** |

---

## 6. Recommended Test Cases (not yet written)

The following test cases are absent and should be created. A test framework such as JUnit 4/5 with Mockito is assumed.

### GoResetPassAction

1. `execute_withGetcodeAction_returnsGetcodeForward` — mock session, set `action=getcode`, assert forward name is `"getcode"`.
2. `execute_withResetAction_andSuccessResponse_returnsResetForward` — mock session with valid accessToken, mock RestClientService returning HTTP 200, assert forward name is `"reset"`.
3. `execute_withResetAction_andFailureResponse_returnsGetcodeForward` — mock RestClientService returning non-200 code, assert forward name is `"getcode"`.
4. `execute_withResetAction_andNullCode_throwsOrHandlesGracefully` — mock RestClientService returning PasswordResponse with null code, assert no NPE reaches caller.
5. `execute_withUnknownAction_returnsHomeForward` — set `action=unknown`, assert forward name is `"home"`.
6. `execute_withNullAction_returnsHomeForward` — set `action` parameter absent (null), assert forward name is `"home"`.
7. `execute_withNoSession_handlesGracefully` — pass `getSession(false)` returning null, assert no NPE (this will currently fail, exposing the bug).
8. `execute_withEmptyUsername_doesNotCallService` or validates before service call.

### GoSearchAction

1. `execute_withValidSession_removesArrDriverAttribute_andReturnsGoSearchForward` — mock session containing `"arrDriver"`, assert attribute removed, assert forward name is `"goSearch"`.
2. `execute_withValidSession_noArrDriverAttribute_doesNotThrow` — mock session with no `"arrDriver"` attribute, assert no exception.
3. `execute_withNoSession_handlesGracefully` — pass `getSession(false)` returning null, assert no NPE (will currently fail, exposing the bug).

---

*End of report — Agent A20, Audit Run 2026-02-26-01*
