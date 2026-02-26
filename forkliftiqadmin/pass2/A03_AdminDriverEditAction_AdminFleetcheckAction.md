# Pass 2 Test-Coverage Audit Report
**Audit run:** 2026-02-26-01
**Agent ID:** A03
**Date:** 2026-02-26
**Scope:** AdminDriverEditAction, AdminFleetcheckAction

---

## 1. Reading-Evidence Blocks

### 1.1 AdminDriverEditAction

**File:** `src/main/java/com/action/AdminDriverEditAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

**Fields / Constants defined:** None (no instance fields or static constants declared in this class).

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 22–190 |

**Internal op_code branches inside `execute` (each is a discrete logical unit requiring independent coverage):**

| Branch / Sub-path | Lines |
|-------------------|-------|
| `edit_general` — DAO update succeeds | 32–57 |
| `edit_general` — DAO update fails (globalfailure) | 58–65 |
| `edit_general_user` — Cognito update HTTP 200 (successUser) | 67–96 |
| `edit_general_user` — Cognito update non-200 (globalfailure) | 97–104 |
| `check_licenceExist` — licence exists (true) | 109–120 |
| `check_licenceExist` — licence does not exist (false) | 109–120 |
| `edit_licence` — licence already exists (failure + duplicate error) | 123–134 |
| `edit_licence` — licence valid, DAO update succeeds (success) | 135–139 |
| `edit_licence` — licence valid, DAO update fails (globalfailure) | 140–147 |
| `edit_subscription` — all three subscription add/delete combinations (9 combinations) | 150–178 |
| `edit_vehicle` — vehicle assigned, DriverService succeeds (success) | 181–187 |
| `edit_vehicle` — DriverService throws DriverServiceException (unhandled exception) | 181–187 |
| `opCode` does not match any branch — `return_code` remains `""` | 32–189 |

**Dependencies used inside `execute`:**
- `AdminDriverEditForm` (cast from ActionForm, line 23)
- `HttpSession.getAttribute("sessCompId")`, `"sessDateFormat"`, `"sessionToken"` (lines 26–28)
- `DriverDAO.updateGeneralInfo(DriverBean)` (line 53)
- `DriverDAO.getAllDriver(String, boolean)` (lines 54, 136)
- `DriverDAO.getDriverById(Long)` (lines 56, 131, 184)
- `DriverDAO.updateGeneralUserInfo(DriverBean)` (line 91)
- `DriverDAO.getAllUser(String, String)` (line 93)
- `DriverDAO.getUserById(Long, String)` (lines 95, 177)
- `DriverDAO.checkDriverByLic(String, String, Long, boolean)` (lines 111, 126)
- `DriverDAO.updateDriverLicenceInfo(LicenceBean, String)` (line 135)
- `CompanyDAO.getInstance()` (lines 89, 156)
- `CompanyDAO.getUserAlert(String, String, String)` (lines 157–159)
- `CompanyDAO.addUserSubscription(String, String)` (lines 162, 167, 172)
- `CompanyDAO.deleteUserSubscription(String, String)` (lines 164, 169, 174)
- `SubscriptionDAO.getSubscriptionByName(String)` (lines 162–174, six calls)
- `DriverService.getInstance().updateAssignedVehicle(DriverVehicleBean)` (line 183)
- `RuntimeConf.HTTP_OK` (line 92)

---

### 1.2 AdminFleetcheckAction

**File:** `src/main/java/com/action/AdminFleetcheckAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

**Fields / Constants defined:** None (no instance fields or static constants declared in this class).

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 18–74 |

**Internal action branches inside `execute` (each is a discrete logical unit requiring independent coverage):**

| Branch / Sub-path | Lines |
|-------------------|-------|
| `action == "search"` — results found | 35–46 |
| `action == "search"` — results empty or null (error added) | 39–44 |
| `action == "add"` — type_id/fuel_type_id/manu_id all non-null (edit forward) | 47–63 |
| `action == "add"` — any of type_id/fuel_type_id/manu_id is null (failure forward) | 48–49 |
| `action` empty/null or unrecognised (else branch, failure forward) | 64–72 |
| `sessCompId` null on session (empty string substitution) | 22–23 |

**Dependencies used inside `execute`:**
- `AdminFleetcheckActionForm` (cast from ActionForm, line 25)
- `HttpSession.getAttribute("sessCompId")` (lines 22–23)
- `ManufactureDAO.getAllManufactures(String)` (line 33)
- `QuestionDAO.getQuestionByCategory(String, String, String, String, String)` (lines 37, 69)
- `QuestionDAO.getMaxQuestionId(String, String, String, String)` (line 57)
- `QuestionDAO.getAllAnswerType()` (line 62)
- `StringUtils.isNotEmpty(String)` (lines 35, 47)

---

## 2. Test-Coverage Confirmation

### 2.1 Grep Results — Test Directory

Grep pattern `AdminDriverEditAction|AdminFleetcheckAction|AdminDriverEdit|AdminFleetcheck` run against:
`/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Result: No matches found.**

### 2.2 Existing Test Files (all 4)

| Test File | Package | What it tests |
|-----------|---------|---------------|
| `UnitCalibrationImpactFilterTest.java` | `com.calibration` | `UnitCalibrationImpactFilter` |
| `UnitCalibrationTest.java` | `com.calibration` | `UnitCalibration` |
| `UnitCalibratorTest.java` | `com.calibration` | `UnitCalibrator` |
| `ImpactUtilTest.java` | `com.util` | `ImpactUtil` |

None of these files reference or exercise `AdminDriverEditAction`, `AdminFleetcheckAction`, or any of their collaborators in an action-layer context. Zero indirect coverage exists for either audited class.

---

## 3. Coverage Gaps and Findings

### AdminDriverEditAction — Findings

---

**A03-1 | Severity: CRITICAL | Zero test coverage — AdminDriverEditAction has no tests whatsoever**

The class `AdminDriverEditAction` has 0% test coverage. No unit test, integration test, or mock-servlet test of any kind exists for this class. The class contains complex multi-branch business logic across six distinct operation codes (`edit_general`, `edit_general_user`, `check_licenceExist`, `edit_licence`, `edit_subscription`, `edit_vehicle`). Every code path — success, failure, and error — is completely unexercised by the test suite.

---

**A03-2 | Severity: CRITICAL | Null session causes NullPointerException — no test guards this**

At line 25, `request.getSession(false)` is called. If no session exists (unauthenticated or expired request), `getSession(false)` returns `null`. Immediately at lines 26–28, `session.getAttribute(...)` is called on the potentially-null reference without a null check. This produces an uncaught `NullPointerException`, bypassing any framework error handling. No test covers the null-session path.

---

**A03-3 | Severity: CRITICAL | Null opCode causes NullPointerException — no test guards this**

At line 29, `adminDriverEditForm.getOp_code()` is retrieved. At line 32, `opCode.equalsIgnoreCase("edit_general")` is called. If `getOp_code()` returns `null` (e.g., missing form parameter), a `NullPointerException` is thrown before any branch executes. The Lombok-generated getter returns `null` because `op_code` is initialised to `null` in the form (line 45 of `AdminDriverEditForm`). No test covers this path.

---

**A03-4 | Severity: CRITICAL | Unmapped return_code causes Struts runtime error — no test guards this**

`return_code` is initialised to `""` (line 31). If the submitted `opCode` does not case-insensitively match any of the five recognised strings, all five `if` blocks are skipped and `mapping.findForward("")` is called at line 189. Struts will throw a runtime exception or return `null` for an unmapped forward name, crashing the request. No test exercises this path.

---

**A03-5 | Severity: HIGH | edit_general — DAO failure path untested**

When `DriverDAO.updateGeneralInfo(driverbean)` returns `false` (lines 58–65), an `ActionErrors` object is created, a generic `"errors.global"` message is added, and the forward `"globalfailure"` is returned. No test verifies that the error is properly saved to the request, that the correct forward is issued, or that no partial state (e.g., `arrAdminDriver`) is set on the request.

---

**A03-6 | Severity: HIGH | edit_general_user — Cognito failure path untested**

When `DriverDAO.updateGeneralUserInfo(driverbean)` returns a response whose code is not `HTTP_OK` (lines 97–104), an `ActionErrors` object is created with a Cognito-specific error message. No test verifies the error key `"error.cognito"`, the propagation of `userUpdateResponse.getMessage()` into the error, the `"DriverEditError"` error key, or the `"globalfailure"` forward.

---

**A03-7 | Severity: HIGH | edit_licence — duplicate licence path untested**

When `DriverDAO.checkDriverByLic(...)` returns `true` (lines 126–134), an `"error.duplcateLicence"` message is added and `"failure"` is forwarded. No test verifies this duplicate-licence detection path. Note also that the message key `"error.duplcateLicence"` contains a typo ("duplcate" instead of "duplicate") which is undetected without tests.

---

**A03-8 | Severity: HIGH | edit_vehicle — DriverServiceException not caught — no test guards this**

At line 183, `DriverService.getInstance().updateAssignedVehicle(driverVehicle)` is declared to throw `DriverServiceException`. The `execute` method declares `throws Exception`, so the exception propagates unhandled to the Struts framework, producing a generic 500-level error page rather than a controlled error response. No test exercises this failure path to verify the user experience or error logging.

---

**A03-9 | Severity: HIGH | edit_subscription — subscription logic never tested (9 combination paths)**

Lines 150–178 contain nine independent conditional paths for three alert types (`RedImpactAlert`, `RedImpactSMS`, `DriverDenyAlert`), each with three states: `"on"` with null `alert_id` (add), `"on"` with existing `alert_id` (no-op), and `""` (delete). None of these paths are tested. A no-op state exists for `"on"` when `alert_id` is already set, meaning a re-subscription attempt is silently swallowed — this business logic is untested.

---

**A03-10 | Severity: HIGH | check_licenceExist — double getWriter() call leaks response state**

At lines 113–116, `response.getWriter()` is called twice: once at line 113 (return value discarded) and again at line 115. The first call is a dead statement that does nothing except confirm the writer can be obtained, but this may cause issues with certain servlet containers if the writer state changes between calls. Neither the true-result nor the false-result write path is tested, and the double-call pattern is never caught by a test.

---

**A03-11 | Severity: MEDIUM | edit_general — CompanyDAO instantiated but unused (dead code)**

At line 89, `CompanyDAO compDao = CompanyDAO.getInstance()` is called and the result assigned to `compDao`. This local variable is never used within the `edit_general_user` block (lines 67–106). The `CompanyDAO` is obtained purely for side-effects (if any), which is a code correctness concern. No test could surface this dead assignment unless code coverage tooling was run — which it never is.

---

**A03-12 | Severity: MEDIUM | edit_subscription — sessCompId used via sessionToken but sessionToken not validated**

In the `edit_subscription` block, `DriverDAO.getUserById(driverId, sessionToken)` is called at line 177, where `sessionToken` may be `""` (see line 28: null becomes `""`). An empty token may produce a failed external service call that is silently swallowed or returns null, which would then be set on the request attribute `"driver"`. No test exercises the empty-token scenario.

---

**A03-13 | Severity: MEDIUM | edit_general and edit_general_user execute independently with no mutual exclusion**

The five `if` blocks (lines 32, 67, 109, 123, 150, 181) are independent `if` statements, not `if/else if`. If an `opCode` were to match two patterns (impossible with `equalsIgnoreCase` given the distinct strings, but not structurally enforced), both blocks would execute, with the second overwriting `return_code`. No test verifies the forward-selection logic is idempotent per request.

---

**A03-14 | Severity: LOW | edit_licence — dateFormat from session used without null check**

At line 27, `session.getAttribute("sessDateFormat")` is cast to `String` with no null guard. At line 135, `dateFormat` is passed to `DriverDAO.updateDriverLicenceInfo(licencebean, dateFormat)`. If the session does not contain the date format attribute, `dateFormat` is `null`, which may cause a `NullPointerException` inside the DAO or incorrect date handling. No test exercises this null-dateFormat path.

---

**A03-15 | Severity: LOW | edit_general_user and edit_subscription both call getUserById — success path not verified**

The request attribute `"driver"` is set to the return value of `DriverDAO.getUserById(driverId, sessionToken)` in both branches (lines 95 and 177). No test verifies that the attribute is correctly set on the request, that the correct driver object corresponds to the edited driver, or that a null return from the DAO is handled gracefully.

---

### AdminFleetcheckAction — Findings

---

**A03-16 | Severity: CRITICAL | Zero test coverage — AdminFleetcheckAction has no tests whatsoever**

The class `AdminFleetcheckAction` has 0% test coverage. No unit test, integration test, or mock-servlet test of any kind exists for this class. The class contains three distinct execution paths (search, add, else/failure) plus internal edge cases within each path.

---

**A03-17 | Severity: CRITICAL | Null session causes NullPointerException — no test guards this**

At line 21, `request.getSession(false)` may return `null` for a sessionless request. Lines 22–23 call `session.getAttribute("sessCompId")` without a null check, producing an uncaught `NullPointerException`. No test covers this path.

---

**A03-18 | Severity: HIGH | search branch — null/empty result path only partially handled**

At lines 39–44, when `arrQuestions` is `null` or empty, an `ActionErrors` is added with key `"resulterror"` and message `"error.noresult"`. However, `arrQuestions` (which may be `null`) is still set as the request attribute `"arrQuestions"` at line 45. If a JSP iterates over this attribute assuming it is non-null, a `NullPointerException` will occur at render time. No test exercises the null-results path.

---

**A03-19 | Severity: HIGH | add branch — null field check is incomplete**

At lines 48–50, only `type_id`, `fuel_type_id`, and `manu_id` are null-checked before the `"failure"` forward. The `att_id` (attachment ID) retrieved at line 31 is passed to `QuestionBean.setAttachment_id(att_id)` at line 55 without any null check. If `att_id` is null and the downstream DAO or persistence layer requires it, a `NullPointerException` or data-integrity violation may result. No test exercises the null-attachment path.

---

**A03-20 | Severity: HIGH | else branch — typo in error key is silent without tests**

At line 67, `errors.add("resutlerror", msg)` contains a typo: `"resutlerror"` instead of `"resulterror"` (which is used correctly in the search branch at line 42). Any view layer code that looks up the `"resulterror"` key to display an error message will silently fail to find the error in the else-branch path. This typo is undetectable without a test that asserts the error key name.

---

**A03-21 | Severity: HIGH | else branch — QuestionDAO called with potentially null/empty filter parameters**

In the else-branch fallback (lines 69–71), `QuestionDAO.getQuestionByCategory(manu_id, type_id, fuel_type_id, att_id, sessCompId)` is called with whatever values are present on the form — potentially all null or all empty. No test verifies the behaviour when all filter fields are null or empty, or confirms that the DAO handles these gracefully rather than generating a malformed SQL query.

---

**A03-22 | Severity: MEDIUM | ManufactureDAO called unconditionally before action routing**

At line 33, `ManufactureDAO.getAllManufactures(sessCompId)` is called before any action-branch check. This means the DAO is called even for the `"add"` branch that immediately returns `"failure"` at line 49. If the DAO call fails (database unavailable, connection pool exhausted), an exception is thrown before any routing occurs, producing an uncontrolled failure. No test exercises this pre-routing DAO failure.

---

**A03-23 | Severity: MEDIUM | add branch — getMaxQuestionId return value used with prefix-increment, not bounds-checked**

At line 57, `QuestionDAO.getMaxQuestionId(...)` returns an `int` which is immediately prefix-incremented (`++orderNO`) and set as the question's order number. If the DAO returns a negative sentinel (e.g., -1 for "no questions exist") or an unexpected value, the resulting order number may be incorrect (e.g., 0). No test verifies the first-question scenario (where max returns 0 or -1) or that the order number is set correctly.

---

**A03-24 | Severity: MEDIUM | search branch — action comparison uses equalsIgnoreCase but form field may have leading/trailing whitespace**

At lines 35 and 47, `action.equalsIgnoreCase("search")` and `action.equalsIgnoreCase("add")` are used. If the `action` form field contains leading or trailing whitespace (e.g., from a malformed HTTP request), neither comparison matches, and execution falls to the else-branch at line 64, silently treating the request as an unrecognised action. No test verifies trim-robustness.

---

**A03-25 | Severity: LOW | sessCompId null-to-empty coercion untested**

At lines 22–23, if `session.getAttribute("sessCompId")` returns `null`, the variable is set to `""`. This empty string is then passed to every DAO call. No test verifies the behaviour of `ManufactureDAO.getAllManufactures("")`, `QuestionDAO.getQuestionByCategory(...)` with empty `sessCompId`, etc. An empty company ID may bypass multi-tenancy filters in the DAO layer, potentially leaking cross-tenant data.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A03-1 | CRITICAL | AdminDriverEditAction | Zero test coverage — entire class untested |
| A03-2 | CRITICAL | AdminDriverEditAction | Null session → NullPointerException at line 26 |
| A03-3 | CRITICAL | AdminDriverEditAction | Null opCode → NullPointerException at line 32 |
| A03-4 | CRITICAL | AdminDriverEditAction | Unrecognised opCode → empty return_code → Struts runtime error |
| A03-5 | HIGH | AdminDriverEditAction | edit_general DAO failure path untested |
| A03-6 | HIGH | AdminDriverEditAction | edit_general_user Cognito failure path untested |
| A03-7 | HIGH | AdminDriverEditAction | edit_licence duplicate-licence path untested; message key typo undetected |
| A03-8 | HIGH | AdminDriverEditAction | edit_vehicle DriverServiceException propagates unhandled |
| A03-9 | HIGH | AdminDriverEditAction | edit_subscription — 9 subscription-state combination paths untested |
| A03-10 | HIGH | AdminDriverEditAction | check_licenceExist — double getWriter() call; neither write path tested |
| A03-11 | MEDIUM | AdminDriverEditAction | CompanyDAO obtained but result unused (dead code) in edit_general_user |
| A03-12 | MEDIUM | AdminDriverEditAction | edit_subscription — empty sessionToken passed to getUserById without guard |
| A03-13 | MEDIUM | AdminDriverEditAction | Independent if-blocks (not if/else-if) — multiple branch execution not structurally prevented |
| A03-14 | LOW | AdminDriverEditAction | dateFormat may be null; passed to DAO without null check |
| A03-15 | LOW | AdminDriverEditAction | getUserById return not validated; null return set silently on request |
| A03-16 | CRITICAL | AdminFleetcheckAction | Zero test coverage — entire class untested |
| A03-17 | CRITICAL | AdminFleetcheckAction | Null session → NullPointerException at line 22 |
| A03-18 | HIGH | AdminFleetcheckAction | search branch — null arrQuestions set on request attribute; JSP NPE risk |
| A03-19 | HIGH | AdminFleetcheckAction | add branch — att_id null check absent; potential NPE or data integrity issue |
| A03-20 | HIGH | AdminFleetcheckAction | else branch — typo "resutlerror" vs "resulterror"; error silently lost |
| A03-21 | HIGH | AdminFleetcheckAction | else branch — DAO called with all-null/empty filter parameters, untested |
| A03-22 | MEDIUM | AdminFleetcheckAction | ManufactureDAO called unconditionally; DAO failure crashes request pre-routing |
| A03-23 | MEDIUM | AdminFleetcheckAction | add branch — getMaxQuestionId return not bounds-checked before increment |
| A03-24 | MEDIUM | AdminFleetcheckAction | action field whitespace not trimmed; misroutes to else-branch silently |
| A03-25 | LOW | AdminFleetcheckAction | sessCompId coerced to empty string; empty string passed to DAOs may bypass tenancy filters |

**Totals:** 6 CRITICAL, 9 HIGH, 6 MEDIUM, 4 LOW — **25 findings across 2 classes**

---

## 5. Coverage Metrics

| Class | Methods | Branches | Lines | Test Coverage |
|-------|---------|----------|-------|---------------|
| AdminDriverEditAction | 1 (execute) | 13+ discrete paths | 170 | 0% |
| AdminFleetcheckAction | 1 (execute) | 6 discrete paths | 57 | 0% |

Both classes are at **0% test coverage**. Neither class is referenced, imported, extended, or indirectly exercised by any of the 4 existing test files in the project.
