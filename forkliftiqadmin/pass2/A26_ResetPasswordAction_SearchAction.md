# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A26
**Date:** 2026-02-26
**Files audited:**
- `src/main/java/com/action/ResetPasswordAction.java`
- `src/main/java/com/action/SearchAction.java`

---

## Section 1 — Reading Evidence

### 1.1 ResetPasswordAction

**File:** `src/main/java/com/action/ResetPasswordAction.java`
**Package:** `com.action`
**Class:** `ResetPasswordAction extends Action` (line 24)

**Fields / Constants defined:** none (no instance fields; all variables are method-local)

**Imports (dependencies):**
- `javax.servlet.http.HttpServletRequest` (line 3)
- `javax.servlet.http.HttpServletResponse` (line 4)
- `javax.servlet.http.HttpSession` (line 5)
- `org.apache.struts.action.*` (lines 7-13)
- `com.actionform.ResetPassActionForm` (line 15)
- `com.bean.CompanyBean` (line 16) — imported but **not used**
- `com.cognito.bean.PasswordRequest` (line 17)
- `com.cognito.bean.PasswordResponse` (line 18)
- `com.dao.CompanyDAO` (line 19) — imported but **not used**
- `com.service.RestClientService` (line 20)
- `com.util.RuntimeConf` (line 21)
- `com.util.Util` (line 22) — imported but **not used**

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 26 |

**Local variables within `execute`:**
- `session` — `HttpSession` obtained via `request.getSession(false)` (line 29)
- `username` — from `request.getParameter("username")`, defaults to `""` (line 30)
- `password` — from `request.getParameter("npass")`, defaults to `""` (line 31)
- `code` — from `request.getParameter("code")`, defaults to `""` (line 32)
- `accessToken` — from `session.getAttribute("accessToken")`, defaults to `""` (line 33)
- `restClientServce` — new `RestClientService()` instantiated inline (line 36)
- `passwordRequest` — built via `PasswordRequest.builder()` (line 37)
- `passwordResponse` — returned from `restClientServce.confirmResetPassword(passwordRequest)` (line 38)

**Code branches:**
1. `passwordResponse.getCode().equals(RuntimeConf.HTTP_OK)` → true: save success message, forward "success" (lines 40-45)
2. `passwordResponse.getCode().equals(RuntimeConf.HTTP_OK)` → false: save error with `passwordResponse.getMessage()`, forward "failure" (lines 46-53)

---

### 1.2 SearchAction

**File:** `src/main/java/com/action/SearchAction.java`
**Package:** `com.action`
**Class:** `SearchAction extends Action` (line 31)

**Fields / Constants defined:**

| Field | Type | Initialiser | Line |
|-------|------|-------------|------|
| `log` | `static Logger` | `InfoLogger.getLogger("com.action.SearchAction")` | 33 |
| `driverDao` | `DriverDAO` | `DriverDAO.getInstance()` (singleton) | 35 |

**Methods:**

| Method | Signature | Line |
|--------|-----------|------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 37 |

**Local variables within `execute`:**
- `session` — from `request.getSession(false)` (line 40)
- `sessCompId` — from `session.getAttribute("sessCompId")`, defaults to `""` (line 41)
- `searchActionForm` — cast of `actionForm` to `SearchActionForm` (line 42)
- `sessArrComp` — `(ArrayList<CompanyBean>) session.getAttribute("sessArrComp")` — unchecked cast, no null guard (line 43)
- `template` — `sessArrComp.get(0).getTemplate()` — index 0 assumed present (line 44)
- `quesionDao` — new `QuestionDAO()` (line 46)
- `arrQues` — from `quesionDao.getQuestionByUnitId(...)` (line 47)
- `arrDriver` — from `driverDao.getDriverByFullNm(...)` (line 50)

**Code branches:**
1. `arrQues != null && arrQues.size() > 0` → true, then `arrDriver != null && arrDriver.size() > 0` → true:
   - `template.equalsIgnoreCase("multiple")` → forward "multiple" (line 59)
   - `template.equalsIgnoreCase("single")` → forward "single" (line 61)
   - else → forward "multiple" (line 63)
2. `arrQues != null && arrQues.size() > 0` → true, but `arrDriver` empty/null: save "error.noDriver", forward "successDriver" (lines 66-74)
3. `arrQues` is null or empty: save "error.noQuestion", forward "failure" (lines 75-81)

---

## Section 2 — Test Coverage Confirmation

**All test files in the project:**
1. `src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java`
2. `src/test/java/com/calibration/UnitCalibrationTest.java`
3. `src/test/java/com/calibration/UnitCalibratorTest.java`
4. `src/test/java/com/util/ImpactUtilTest.java`

**Grep for `ResetPasswordAction` across all test sources:** 0 matches
**Grep for `SearchAction` across all test sources:** 0 matches

**Conclusion:** Neither class has any test coverage — direct or indirect — anywhere in the project test suite. All four existing tests are confined to the `com.calibration` and `com.util` packages and exercise entirely unrelated functionality (impact calibration, G-force utilities).

---

## Section 3 — Coverage Gaps and Findings

---

### A26-1 | Severity: CRITICAL | `ResetPasswordAction.execute` — zero test coverage

The entire `execute` method (lines 26-57) has no test coverage whatsoever. The method is the sole entry point of the class and contains all business logic including an external Cognito API call, response parsing, session reads, and two distinct forward paths. No mock-based or integration test exercises any code path.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, lines 26-57

---

### A26-2 | Severity: CRITICAL | `SearchAction.execute` — zero test coverage

The entire `execute` method (lines 37-84) has no test coverage. The method contains three distinct control-flow branches, two DAO calls (QuestionDAO and DriverDAO), session attribute reads, and three different forward outcomes. No test exercises any path.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 37-84

---

### A26-3 | Severity: CRITICAL | `ResetPasswordAction` — null session NPE not tested

`request.getSession(false)` on line 29 returns `null` when no active session exists (the `false` argument explicitly suppresses session creation). The result is stored in `session` and immediately used on line 33 without any null guard (`session.getAttribute("accessToken")`). A request arriving with no active session will throw `NullPointerException` at line 33, causing an unhandled exception that propagates through the Struts framework. No test exercises this crash path.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, lines 29, 33

---

### A26-4 | Severity: CRITICAL | `SearchAction` — null session NPE not tested

Identical pattern to A26-3. `request.getSession(false)` on line 40 may return `null`. The result is immediately used on line 41 (`session.getAttribute("sessCompId")`) without a null guard. No test covers this path.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 40-41

---

### A26-5 | Severity: CRITICAL | `SearchAction` — null `sessArrComp` causes NPE, not tested

Line 43 casts `session.getAttribute("sessArrComp")` to `ArrayList<CompanyBean>`. If this session attribute is absent (null), `sessArrComp` will be `null`. Line 44 then calls `sessArrComp.get(0)` unconditionally, producing a `NullPointerException`. No null check or empty-list guard exists before the `.get(0)` call. No test exercises this condition.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 43-44

---

### A26-6 | Severity: CRITICAL | `SearchAction` — empty `sessArrComp` causes `IndexOutOfBoundsException`, not tested

Even if `sessArrComp` is non-null but an empty list, `sessArrComp.get(0)` on line 44 will throw `IndexOutOfBoundsException`. No bounds check is performed before accessing index 0. No test exercises this condition.

**Affected file:** `src/main/java/com/action/SearchAction.java`, line 44

---

### A26-7 | Severity: CRITICAL | `ResetPasswordAction` — `passwordResponse.getCode()` null causes NPE, not tested

`PasswordResponse.getCode()` returns an `Integer` (boxed type, line 22 of `PasswordResponse.java`). If the Cognito API returns a response with no `code` field (network error, partial response, or a malformed JSON body), `getCode()` returns `null`. The comparison `passwordResponse.getCode().equals(RuntimeConf.HTTP_OK)` on line 40 will then throw a `NullPointerException`. No test exercises this scenario.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, line 40
**Supporting file:** `src/main/java/com/cognito/bean/PasswordResponse.java`, line 22

---

### A26-8 | Severity: HIGH | `ResetPasswordAction` — success path ("success" forward) not tested

The branch at lines 41-45 — where `passwordResponse.getCode()` equals `200` — saves a success message under key `"resetpassmsg"` with message key `"reset.succuss"` (note: apparent typo "succuss") and forwards to `"success"`. This path is never exercised by any test.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, lines 41-45

---

### A26-9 | Severity: HIGH | `ResetPasswordAction` — failure path ("failure" forward) not tested

The branch at lines 47-53 — where `passwordResponse.getCode()` is not `200` — reads `passwordResponse.getMessage()`, creates an error under key `"infoerror"` with message key `"error.incorrect.reset.cognito"`, and forwards to `"failure"`. This path is never exercised by any test.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, lines 47-53

---

### A26-10 | Severity: HIGH | `SearchAction` — "multiple" template forward path not tested

The branch at lines 58-59 (and default at 62-64) that forwards to `"multiple"` when the template value is `"multiple"` or any unrecognised value is never tested.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 58-64

---

### A26-11 | Severity: HIGH | `SearchAction` — "single" template forward path not tested

The branch at lines 60-61 that forwards to `"single"` when `template.equalsIgnoreCase("single")` is never tested.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 60-61

---

### A26-12 | Severity: HIGH | `SearchAction` — "error.noDriver" path ("successDriver" forward) not tested

The branch at lines 66-74 — triggered when questions are found but no driver matches the search name — saves error message `"error.noDriver"` and forwards to `"successDriver"`. This is a meaningful user-facing error state that is never exercised by any test.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 66-74

---

### A26-13 | Severity: HIGH | `SearchAction` — "error.noQuestion" path ("failure" forward) not tested

The branch at lines 75-81 — triggered when `getQuestionByUnitId` returns null or an empty list — saves error message `"error.noQuestion"` and forwards to `"failure"`. This is a meaningful user-facing error state that is never exercised by any test.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 75-81

---

### A26-14 | Severity: HIGH | `ResetPasswordAction` — `RestClientService` network exception not tested

`restClientServce.confirmResetPassword(passwordRequest)` on line 38 can throw a `RestClientException` or any other runtime exception if the Cognito sidecar is unreachable or returns an unexpected HTTP status (as seen in the `RestClientService.confirmResetPassword` implementation). `ResetPasswordAction.execute` is declared `throws Exception` but has no try/catch block — any exception propagates uncaught to the Struts framework and likely results in a generic error page rather than a controlled user message. No test validates this failure mode.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, line 38
**Supporting file:** `src/main/java/com/service/RestClientService.java`, lines 142-175

---

### A26-15 | Severity: HIGH | `SearchAction` — DAO exceptions propagate uncaught, not tested

`quesionDao.getQuestionByUnitId(...)` (line 47) and `driverDao.getDriverByFullNm(...)` (line 50) both perform JDBC operations that can throw `SQLException` or other runtime exceptions. `SearchAction.execute` is declared `throws Exception` but has no try/catch — any DAO failure propagates to the Struts framework without a controlled error message shown to the user. No test validates this behaviour.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 47, 50

---

### A26-16 | Severity: MEDIUM | `SearchAction` — `sessCompId` defaults silently to empty string, not tested

Line 41 defaults `sessCompId` to `""` when the session attribute is absent. An empty company ID is passed directly to DAO calls (lines 47, 50) as a valid parameter, meaning the query will execute with an empty string rather than failing fast with a meaningful error. This silent degradation is not tested.

**Affected file:** `src/main/java/com/action/SearchAction.java`, line 41

---

### A26-17 | Severity: MEDIUM | `ResetPasswordAction` — all parameters default silently to empty strings, not tested

Lines 30-32 default `username`, `password`, and `code` to `""` when the corresponding request parameters are absent. Empty-string credentials are then passed to the Cognito API without any pre-flight validation, meaning the full round-trip to the external service occurs before a failure is detected. The form class `ResetPassActionForm` does not cover these parameters (it covers `name` and `email`), so no Struts-level validation catches empty values. No test verifies the behaviour for any missing parameter.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, lines 30-33

---

### A26-18 | Severity: MEDIUM | `SearchAction` — `template` null causes NPE, not tested

`getTemplate()` on `CompanyBean` (line 44) may return `null` if the company record has no template configured. The subsequent `template.equalsIgnoreCase("multiple")` on line 58 would throw a `NullPointerException`. No test covers a null template scenario. Safe practice would be to call `"multiple".equalsIgnoreCase(template)` or add an explicit null check before the if-block.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 44, 58

---

### A26-19 | Severity: MEDIUM | `SearchAction` — default "else" forward to "multiple" when template is unrecognised, not tested

Lines 62-64 silently forward to `"multiple"` for any template value that is neither `"multiple"` nor `"single"`. An unexpected or newly introduced template type would silently fall through to the wrong view. No test verifies the default-branch behaviour.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 62-64

---

### A26-20 | Severity: MEDIUM | `ResetPasswordAction` — `accessToken` defaults silently to empty string when session attribute is missing, not tested

Line 33 silently falls back to `""` when `session.getAttribute("accessToken")` is null (i.e., the token was never set or the session was freshly created). An empty access token is then passed to the Cognito `confirmResetPassword` endpoint, which would likely produce an authentication or validation error from Cognito. No test validates the missing-token scenario.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, line 33

---

### A26-21 | Severity: LOW | `ResetPasswordAction` — unused imports (`CompanyBean`, `CompanyDAO`, `Util`)

Lines 16, 19, and 22 import `CompanyBean`, `CompanyDAO`, and `Util` respectively. None of these are referenced anywhere in the class. These dead imports suggest either copy-paste from a template or a planned feature that was abandoned. While not a runtime defect, there is no test that could have caught this unused-code drift.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, lines 16, 19, 22

---

### A26-22 | Severity: LOW | `ResetPasswordAction` — typo in message key "reset.succuss"

Line 42 uses `new ActionMessage("reset.succuss")`. The key appears to be a misspelling of "reset.success". If the properties file defines `reset.success` (correct spelling) and not `reset.succuss`, the success message will be silently blank at runtime. No test validates that the correct localised message is produced on the success path.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, line 42

---

### A26-23 | Severity: LOW | `ResetPasswordAction` — `RestClientService` instantiated with `new` (untestable without reflection or framework)

Line 36 uses `new RestClientService()` directly, hardwiring the action to a concrete implementation that makes a live HTTP call to `localhost:9090`. This design makes it impossible to inject a mock or stub without modifying the source, significantly raising the barrier to unit testing. No test exists that bypasses this coupling.

**Affected file:** `src/main/java/com/action/ResetPasswordAction.java`, line 36
**Supporting file:** `src/main/java/com/service/RestClientService.java`, line 31

---

### A26-24 | Severity: LOW | `SearchAction` — `QuestionDAO` instantiated with `new` (untestable without reflection)

Line 46 uses `new QuestionDAO()`, hardwiring the action to a concrete DAO that requires a live JDBC datasource. Like A26-23, this makes unit testing without container support impossible. The `driverDao` field at line 35 uses a singleton pattern (`DriverDAO.getInstance()`) which is equally non-injectable. No tests exist to expose this coupling.

**Affected file:** `src/main/java/com/action/SearchAction.java`, lines 35, 46

---

### A26-25 | Severity: INFO | `SearchAction` — typo in variable name `quesionDao` (missing 't')

Line 46 declares `QuestionDAO quesionDao`. The variable name is missing the letter 't' (should be `questionDao`). This is a cosmetic defect with no runtime impact but is an indicator of low code-review discipline and the absence of any test that would flag naming issues through static analysis.

**Affected file:** `src/main/java/com/action/SearchAction.java`, line 46

---

## Section 4 — Summary Table

| Finding | Severity | Description |
|---------|----------|-------------|
| A26-1 | CRITICAL | `ResetPasswordAction.execute` — zero test coverage |
| A26-2 | CRITICAL | `SearchAction.execute` — zero test coverage |
| A26-3 | CRITICAL | `ResetPasswordAction` — null session (getSession(false)) causes NPE at line 33, not tested |
| A26-4 | CRITICAL | `SearchAction` — null session (getSession(false)) causes NPE at line 41, not tested |
| A26-5 | CRITICAL | `SearchAction` — null `sessArrComp` causes NPE at `sessArrComp.get(0)`, not tested |
| A26-6 | CRITICAL | `SearchAction` — empty `sessArrComp` causes `IndexOutOfBoundsException`, not tested |
| A26-7 | CRITICAL | `ResetPasswordAction` — null `passwordResponse.getCode()` causes NPE at `.equals()`, not tested |
| A26-8 | HIGH | `ResetPasswordAction` — success path ("success" forward) not tested |
| A26-9 | HIGH | `ResetPasswordAction` — failure path ("failure" forward) not tested |
| A26-10 | HIGH | `SearchAction` — "multiple" template forward path not tested |
| A26-11 | HIGH | `SearchAction` — "single" template forward path not tested |
| A26-12 | HIGH | `SearchAction` — "error.noDriver" / "successDriver" path not tested |
| A26-13 | HIGH | `SearchAction` — "error.noQuestion" / "failure" path not tested |
| A26-14 | HIGH | `ResetPasswordAction` — `RestClientService` network exception propagates uncaught, not tested |
| A26-15 | HIGH | `SearchAction` — DAO exceptions propagate uncaught, not tested |
| A26-16 | MEDIUM | `SearchAction` — `sessCompId` silently defaults to `""`, not tested |
| A26-17 | MEDIUM | `ResetPasswordAction` — all request parameters silently default to `""`, no validation, not tested |
| A26-18 | MEDIUM | `SearchAction` — null `template` from `getTemplate()` causes NPE, not tested |
| A26-19 | MEDIUM | `SearchAction` — unrecognised template silently defaults to "multiple" forward, not tested |
| A26-20 | MEDIUM | `ResetPasswordAction` — missing `accessToken` silently defaults to `""`, not tested |
| A26-21 | LOW | `ResetPasswordAction` — unused imports (`CompanyBean`, `CompanyDAO`, `Util`) |
| A26-22 | LOW | `ResetPasswordAction` — typo in message key `"reset.succuss"` may cause silent blank message |
| A26-23 | LOW | `ResetPasswordAction` — `RestClientService` instantiated with `new`, untestable without framework |
| A26-24 | LOW | `SearchAction` — `QuestionDAO` / `DriverDAO` instantiated with `new` or singleton, untestable |
| A26-25 | INFO | `SearchAction` — typo in variable name `quesionDao` (missing 't') |

**Totals:** 7 CRITICAL, 8 HIGH, 5 MEDIUM, 4 LOW, 1 INFO
**Measured coverage:** 0% — no test exercises either class under any condition.
