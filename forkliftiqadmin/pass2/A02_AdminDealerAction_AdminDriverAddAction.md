# Pass 2 — Test-Coverage Audit
## Files: AdminDealerAction.java | AdminDriverAddAction.java

**Audit Run:** 2026-02-26-01
**Pass:** 2 (Test-Coverage Analysis)
**Agent ID:** A02
**Date:** 2026-02-26
**Branch:** master

---

## 1. READING EVIDENCE

### 1.1 AdminDealerAction.java

**Source path:** `src/main/java/com/action/AdminDealerAction.java`
**Package:** `com.action`
**Class:** `AdminDealerAction`
**Extends:** `org.apache.struts.action.Action` (line 16)

#### Fields / Constants

None. No instance fields or class-level constants are declared.

#### Methods

| Line | Modifier(s) | Return Type | Name | Parameters |
|------|-------------|-------------|------|-----------|
| 18 | `public` (override) | `ActionForward` | `execute` | `ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response` — throws `Exception` |
| 32 | `public static` | `void` | `prepareDealerRequest` | `HttpServletRequest request, HttpSession session` — throws `SQLException` |

#### Imports

- `com.actionform.AdminDealerActionForm`
- `com.bean.CompanyBean`
- `com.bean.RoleBean`
- `com.dao.CompanyDAO`
- `org.apache.commons.lang.StringUtils`
- `org.apache.struts.action.*`
- `javax.servlet.http.HttpServletRequest`
- `javax.servlet.http.HttpServletResponse`
- `javax.servlet.http.HttpSession`
- `java.sql.SQLException`
- `java.util.ArrayList`

#### Logical Branches and Execution Paths

**`execute()` (lines 18–30)**

| Path | Condition | Outcome |
|------|-----------|---------|
| E1 | `adminDealerForm.getCompanyId()` is non-blank | Calls `CompanyDAO.getInstance().convertCompanyToDealer(companyId)` then `prepareDealerRequest`, returns `"success"` forward |
| E2 | `adminDealerForm.getCompanyId()` is blank/null | Skips DAO call; calls `prepareDealerRequest`, returns `"success"` forward |

**`prepareDealerRequest()` (lines 32–53)**

| Path | Condition | Outcome |
|------|-----------|---------|
| P1 | `session.getAttribute("isSuperAdmin")` equals `false` | Early return; request attributes NOT set |
| P2 | `isSuperAdmin` attribute is `null` | `NullPointerException` thrown on line 33 |
| P3 | `isSuperAdmin` attribute is not a `Boolean` (e.g., `String`) | `.equals(false)` compares String to Boolean → returns `false` → proceeds as if superadmin |
| P4 | `isSuperAdmin` is `true` (or truthy non-Boolean) | Calls `getAllCompany()`, iterates, partitions into dealers / non-dealers, sets request attributes `arrCompanies` and `arrDealers` |
| P5 | `company.getRoles()` is empty for some companies | Inner role loop does not execute; company is placed in `nonDealers` |
| P6 | A company has multiple roles, one of which is `ROLE_DEALER` | Company is added to `dealers` list; `isDealer` flag prevents re-add to `nonDealers` |
| P7 | A company has `ROLE_DEALER` role but `getAuthority()` returns `null` | `NullPointerException` in `.equals("ROLE_DEALER")` (line 42) |
| P8 | `CompanyDAO.getAllCompany()` throws `SQLException` | Propagates; action re-throws as `Exception` |

---

### 1.2 AdminDriverAddAction.java

**Source path:** `src/main/java/com/action/AdminDriverAddAction.java`
**Package:** `com.action`
**Class:** `AdminDriverAddAction`
**Extends:** `org.apache.struts.action.Action` (line 19)

#### Fields / Constants

None. No instance fields or class-level constants are declared.

#### Methods

| Line | Modifier(s) | Return Type | Name | Parameters |
|------|-------------|-------------|------|-----------|
| 21 | `public` (override) | `ActionForward` | `execute` | `ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response` — throws `Exception` |

#### Imports

- `com.actionform.AdminDriverAddForm`
- `com.bean.DriverBean`
- `com.bean.UserBean`
- `com.cognito.bean.UserSignUpRequest`
- `com.cognito.bean.UserSignUpResponse`
- `com.dao.CompanyDAO`
- `com.dao.DriverDAO`
- `com.service.RestClientService`
- `com.util.RuntimeConf`
- `org.apache.struts.action.*`
- `javax.servlet.http.HttpServletRequest`
- `javax.servlet.http.HttpServletResponse`
- `javax.servlet.http.HttpSession`

#### Logical Branches and Execution Paths

**`execute()` — setup (lines 22–28)**

| Path | Condition | Outcome |
|------|-----------|---------|
| S1 | `request.getSession(false)` returns `null` | `NullPointerException` on line 24 (session.getAttribute) |
| S2 | Session exists but `sessCompId` attribute is absent/null | `sessCompId` is null; downstream `Integer.parseInt(sessCompId)` (line 91) throws `NumberFormatException` |

**`execute()` — `op_code = "add_general"` branch (lines 30–42)**

| Path | Condition | Outcome |
|------|-----------|---------|
| AG1 | `opCode` is `null` | `NullPointerException` on line 30 (`null.equalsIgnoreCase(...)`) |
| AG2 | `opCode.equalsIgnoreCase("add_general")` — `DriverDAO.addDriverInfo` returns `false` | `ActionErrors` saved; `return_code = "globalfailure"` |
| AG3 | `opCode.equalsIgnoreCase("add_general")` — `DriverDAO.addDriverInfo` returns `true` | `return_code = "success"` |
| AG4 | `DriverDAO.addDriverInfo` throws an exception | Propagates uncaught from `execute()` |

**`execute()` — `op_code = "add_general_user"` branch (lines 44–96)**

| Path | Condition | Outcome |
|------|-----------|---------|
| AU1 | Cognito response message contains `"User already exists"` | Saves `errors.global` error; `return_code = "globalfailure"` |
| AU2 | Cognito response code is not `HTTP_OK` (and not "User already exists") | Saves `error.cognito` error; `return_code = "globalfailure"` |
| AU3 | Cognito response code is `HTTP_OK` | Calls `getUserMaxId()`, builds `UserBean`, calls `saveUsers()`, calls `saveUserRoles(userId, ROLE_SITEADMIN)`, `return_code = "successUser"` |
| AU4 | `signUpResponse` itself is `null` | `NullPointerException` on line 63 (`signUpResponse.getMessage()`) |
| AU5 | `signUpResponse.getMessage()` is `null` AND `signUpResponse.getCode()` equals `HTTP_OK` | Happy-path proceeds; null message is not a problem on this branch |
| AU6 | `signUpResponse.getMessage()` is `null` AND `signUpResponse.getCode()` is not `HTTP_OK` | Line 73 assigns `null` to `errormsg`; `ActionMessage` constructed with `null` parameter |
| AU7 | `RestClientService` constructor or `signUpRequest()` throws an exception | Propagates uncaught |
| AU8 | `compDao.saveUsers()` or `compDao.saveUserRoles()` throws `SQLException` | Propagates uncaught; Cognito user has been created but DB user record is not saved (split-brain) |

**`execute()` — terminal (lines 98–99)**

| Path | Condition | Outcome |
|------|-----------|---------|
| T1 | `op_code` is neither `add_general` nor `add_general_user` | `return_code = ""`; `mapping.findForward("")` returns `null`; Struts NPE / 500 error |
| T2 | Both `if` blocks execute (mutually exclusive by design but not enforced) | Only `add_general_user` value of `return_code` survives |

---

## 2. TEST-COVERAGE CONFIRMATION

### 2.1 Existing Test Files

The project contains exactly four test files:

| File | Package / Class |
|------|----------------|
| `src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java` | Calibration domain |
| `src/test/java/com/calibration/UnitCalibrationTest.java` | Calibration domain |
| `src/test/java/com/calibration/UnitCalibratorTest.java` | Calibration domain |
| `src/test/java/com/util/ImpactUtilTest.java` | Utility domain |

### 2.2 Grep Confirmation — Zero Indirect Coverage

The following patterns were searched across the entire test directory (`src/test/java/`) and returned zero matches:

| Search Pattern | Result |
|----------------|--------|
| `AdminDealerAction` | 0 matches |
| `AdminDriverAddAction` | 0 matches |
| `prepareDealerRequest` | 0 matches |
| `convertCompanyToDealer` | 0 matches |

**Conclusion:** Neither class is exercised by any test — directly or indirectly. Coverage for both classes is 0%.

---

## 3. COVERAGE GAPS — ALL FINDINGS

---

### A02-1 | Severity: CRITICAL | AdminDealerAction.execute() — zero test coverage for entire method

No test exists for `AdminDealerAction.execute()`. The method is responsible for a state-changing privileged operation (company-to-dealer promotion). The following execution paths are all untested:

- E1: companyId non-blank — DAO mutation path
- E2: companyId blank — read-only path
- The transition from `execute()` to `prepareDealerRequest()` in both cases

Without tests, there is no regression safety net for any of the security findings identified in Pass 1 (auth guard order-of-operations, IDOR, session-scope form, NPE on `isSuperAdmin`). Any code change could silently remove or break whatever partial safeguards exist.

**Untested method:** `execute` (line 18)
**Untested paths:** E1, E2

---

### A02-2 | Severity: CRITICAL | AdminDealerAction.prepareDealerRequest() — zero test coverage for entire method

`prepareDealerRequest` is `public static` and is the only location of the `isSuperAdmin` access-control guard. It is completely untested, meaning:

- The guard itself (line 33) has never been exercised.
- The NullPointerException risk when `isSuperAdmin` is absent from the session is untested (path P2).
- The type-mismatch silent-bypass risk (path P3) is untested.
- The full company list partitioning logic (paths P4–P6) is untested.
- The NullPointerException risk from `role.getAuthority()` returning null (path P7) is untested.
- The `getAllCompany()` SQL exception propagation (path P8) is untested.

This is the sole authorisation enforcement point for the dealer management page. Its correctness has never been verified by an automated test.

**Untested method:** `prepareDealerRequest` (line 32)
**Untested paths:** P1, P2, P3, P4, P5, P6, P7, P8

---

### A02-3 | Severity: CRITICAL | AdminDriverAddAction.execute() — zero test coverage for entire method

`AdminDriverAddAction.execute()` is completely untested. This single method contains:

- The only entry point for driver creation and privileged user account creation.
- Unconditional `ROLE_SITE_ADMIN` assignment to newly created users (line 92).
- Two distinct branching paths (`add_general` and `add_general_user`) each with their own sub-paths.
- Three external integration calls (DriverDAO, CompanyDAO, RestClientService/Cognito).

Zero tests means all of paths AG1–AG4, AU1–AU8, S1–S2, and T1–T2 are untested.

**Untested method:** `execute` (line 21)
**Untested paths:** S1, S2, AG1, AG2, AG3, AG4, AU1, AU2, AU3, AU4, AU5, AU6, AU7, AU8, T1, T2

---

### A02-4 | Severity: HIGH | No test for isSuperAdmin == false early-return in prepareDealerRequest (path P1)

The guard `if (session.getAttribute("isSuperAdmin").equals(false)) return;` (line 33) is the primary authorisation check for the dealer management view. There is no test confirming that a non-superadmin session correctly exits without populating `arrCompanies` and `arrDealers`. If this guard were accidentally removed or inverted by a future change, no test would catch it.

**Untested path:** P1 — superadmin check early return

---

### A02-5 | Severity: HIGH | No test for NullPointerException when isSuperAdmin session attribute is absent (path P2)

If `session.getAttribute("isSuperAdmin")` returns `null` (attribute never set, or session was created without proper login-flow completion), line 33 throws `NullPointerException`. This is an unhandled runtime exception. No test exists to confirm this edge case is handled, detected, or at minimum produces a predictable error response rather than a stack-trace leak.

**Untested path:** P2 — null isSuperAdmin attribute

---

### A02-6 | Severity: HIGH | No test for isSuperAdmin stored as non-Boolean type (path P3)

If `isSuperAdmin` is stored in the session as a `String` (e.g., `"false"` or `"true"`), the comparison `.equals(false)` compares a `String` to a `Boolean` and always returns `false`, causing `prepareDealerRequest` to silently treat all authenticated sessions as superadmins and expose the full company list. No test validates the type and value of this attribute under varied login scenarios.

**Untested path:** P3 — type-mismatch bypass

---

### A02-7 | Severity: HIGH | No test for null session in AdminDriverAddAction (path S1)

`request.getSession(false)` can return `null` if no session exists. The result is assigned to `session` (line 23) and `.getAttribute("sessCompId")` is called immediately on line 24 without a null check. No test exercises this path to verify the action fails safely rather than throwing an uncaught `NullPointerException`.

**Untested path:** S1 — null session

---

### A02-8 | Severity: HIGH | No test for null opCode causing NPE in AdminDriverAddAction (path AG1)

`adminDriverAddForm.getOp_code()` can return `null`. The return value is stored in `opCode` (line 26) and then `opCode.equalsIgnoreCase("add_general")` is called on line 30 without a null guard. No test exercises the null `opCode` path. This is a caller-controlled NullPointerException that results in an unhandled 500 error.

**Untested path:** AG1 — null opCode

---

### A02-9 | Severity: HIGH | No test for AdminDriverAddAction DriverDAO failure path (path AG2)

When `DriverDAO.addDriverInfo(driverbean)` returns `false` (insert failure), the action is expected to save an `ActionErrors` message and forward to `"globalfailure"`. No test confirms that the `ActionErrors` object is correctly constructed and saved, that the forward resolves to `"globalfailure"`, or that the driver bean is still correctly placed in request scope.

**Untested path:** AG2 — addDriverInfo returns false

---

### A02-10 | Severity: HIGH | No test for Cognito "User already exists" error handling (path AU1)

When the Cognito service returns a message containing `"User already exists"`, the action saves an error and returns `"globalfailure"`. No test verifies the exact error key (`DriverAddError`), message key (`errors.global`), or that no database writes occurred on this path (i.e., no partial driver record creation).

**Untested path:** AU1 — Cognito "User already exists"

---

### A02-11 | Severity: HIGH | No test for Cognito non-OK response handling (path AU2)

When Cognito returns a code other than `HTTP_OK` (and the message does not contain "User already exists"), the action saves an error using `error.cognito` and returns `"globalfailure"`. No test verifies this path, including the distinct error message key `error.cognito` vs. `errors.global` used in path AU1.

**Untested path:** AU2 — Cognito non-OK code

---

### A02-12 | Severity: HIGH | No test for successful user creation path including unconditional ROLE_SITEADMIN grant (path AU3)

The `add_general_user` happy path (path AU3) calls `saveUserRoles(userId, RuntimeConf.ROLE_SITEADMIN)` unconditionally. No test confirms:

- That this call is made with the correct `userId` from `getUserMaxId()`.
- That `ROLE_SITEADMIN` is the role assigned (rather than a less or more privileged role).
- That the `compDao.saveUsers()` call precedes `saveUserRoles()`.
- That `return_code` is set to `"successUser"` and the forward resolves correctly.

This is the highest-impact path in the file (privilege escalation) and has no test coverage at all.

**Untested path:** AU3 — successful add_general_user including ROLE_SITEADMIN grant

---

### A02-13 | Severity: HIGH | No test for split-brain failure: Cognito success followed by DB exception (path AU8)

If `RestClientService.signUpRequest()` succeeds (Cognito user created) but `compDao.saveUsers()` or `compDao.saveUserRoles()` subsequently throws a `SQLException`, the Cognito account exists in the identity provider but no corresponding record is written to the local database. The system is left in an inconsistent state. No test confirms this scenario is detectable, logged, or handled with a compensating action.

**Untested path:** AU8 — Cognito/DB split-brain on SQLException

---

### A02-14 | Severity: HIGH | No test for null mapping.findForward("") when op_code is unrecognised (path T1)

When `op_code` is neither `add_general` nor `add_general_user`, `return_code` remains `""` and `mapping.findForward("")` returns `null`. Struts attempts to use this `null` `ActionForward` and throws a `NullPointerException`, producing an unhandled 500 error. No test exercises this path to confirm the observed failure mode or to detect if defensive handling is ever added.

**Untested path:** T1 — unrecognised op_code

---

### A02-15 | Severity: MEDIUM | No test for company list partitioning logic in prepareDealerRequest (paths P4–P6)

The loop in `prepareDealerRequest` (lines 39–50) partitions companies into `dealers` and `nonDealers` by checking each company's roles for `ROLE_DEALER`. No test verifies:

- A company with no roles is placed in `nonDealers`.
- A company with `ROLE_DEALER` is placed in `dealers` and not also in `nonDealers`.
- A company with multiple roles, one of which is `ROLE_DEALER`, is handled correctly.
- The resulting lists are correctly set as request attributes `arrCompanies` and `arrDealers`.

**Untested paths:** P4, P5, P6

---

### A02-16 | Severity: MEDIUM | No test for NullPointerException when RoleBean.getAuthority() returns null (path P7)

On line 42, `role.getAuthority().equals("ROLE_DEALER")` will throw `NullPointerException` if `getAuthority()` returns `null`. This can occur if a `RoleBean` was constructed without a value for `authority` (e.g., from a DB row with a null column). No test exercises this path.

**Untested path:** P7 — null role authority

---

### A02-17 | Severity: MEDIUM | No test for null sessCompId causing NumberFormatException in add_general_user (path S2)

In the `add_general_user` branch, `Integer.parseInt(sessCompId)` is called on line 91 where `sessCompId` was obtained from the session on line 24. If the session exists but `sessCompId` is `null` or a non-integer string, `NumberFormatException` is thrown. No test confirms this is handled or produces a safe, predictable response.

**Untested path:** S2 — null/non-integer sessCompId

---

### A02-18 | Severity: MEDIUM | No test for null signUpResponse from RestClientService (path AU4)

If `restClientServce.signUpRequest()` returns `null`, line 63 `signUpResponse.getMessage()` throws `NullPointerException`. No test exercises this failure mode, which would produce an unhandled exception rather than a user-friendly error message.

**Untested path:** AU4 — null signUpResponse

---

### A02-19 | Severity: MEDIUM | No test for null signUpResponse.getMessage() in non-OK path causing null ActionMessage parameter (path AU6)

In path AU6 (non-OK response code, null message), line 73 assigns `null` to `errormsg` and line 75 constructs `new ActionMessage("error.cognito", null)`. No test verifies the downstream behaviour: whether Struts renders a blank error, throws an exception, or otherwise misbehaves when an `ActionMessage` is constructed with a null parameter.

**Untested path:** AU6 — null message in non-OK Cognito response

---

### A02-20 | Severity: MEDIUM | execute() calls prepareDealerRequest with a session that was obtained with getSession(false) — no test for consistency of session-null handling across the two actions

`AdminDealerAction.execute()` calls `request.getSession(false)` and passes the result directly to `prepareDealerRequest()` (line 27) without a null check. `prepareDealerRequest()` then calls `session.getAttribute("isSuperAdmin")` on line 33. If the session is null, this throws `NullPointerException` inside `prepareDealerRequest`. No test exercises this cross-method null-session path.

**Untested path:** Implicit null-session path in AdminDealerAction.execute() → prepareDealerRequest()

---

### A02-21 | Severity: MEDIUM | No test confirming prepareDealerRequest is called even when companyId is blank (path E2)

In `execute()`, `prepareDealerRequest` is always called regardless of whether the DAO conversion was triggered. No test confirms that a GET request with no `companyId` (path E2) still correctly populates the view attributes, without accidentally triggering a conversion.

**Untested path:** E2 — blank companyId, read-only page load

---

### A02-22 | Severity: MEDIUM | No test for getAllCompany() SQLException propagation (path P8)

If `CompanyDAO.getAllCompany()` throws a `SQLException` (DB unreachable, connection pool exhausted), the exception propagates from `prepareDealerRequest` through `execute()` as an `Exception`. No test verifies that this produces a safe error response and does not expose stack trace information, and no test confirms whether the Struts global-exception handler or `web.xml` error page intercepts it correctly.

**Untested path:** P8 — SQLException from getAllCompany()

---

### A02-23 | Severity: LOW | No test for plaintext password exposure in request scope via driverbean (AdminDriverAddAction)

After the `add_general_user` branch (or on any path), line 98 sets `request.setAttribute("driver", driverbean)`. The `DriverBean` at this point contains the plaintext password from `adminDriverAddForm.getPass()`. No test verifies that this attribute is absent from the request after the action completes, or that the password field within it is null/cleared. Without a test, silent regression toward exposing the password via the JSP layer has no automated detection.

**Related finding:** Pass 1 FINDING-03 (HIGH — plaintext password in request scope)

---

### A02-24 | Severity: LOW | No test for prepareDealerRequest being called from any other action class

`prepareDealerRequest` is `public static` and could be called by any other action in the codebase without the `isSuperAdmin` guard being in effect. No test confirms that no other caller invokes it with an untrusted session state, and no test would catch such a caller being introduced in future.

**Untested scenario:** External invocation of `prepareDealerRequest` bypassing `execute()`

---

### A02-25 | Severity: INFO | No integration or end-to-end test for /dealerconvert.do or /admindriveradd.do endpoints

Neither Struts action has any integration test that exercises the full request-processing pipeline (servlet filter → action servlet → action → DAO → forward). The only test infrastructure in the project tests calibration domain utilities in isolation. There is no test harness for Struts action testing (e.g., StrutsTestCase, MockStrutsTestCase, or Spring MVC Test analogues). Introducing such a harness is a prerequisite for any meaningful automated coverage of these classes.

---

## 4. COVERAGE SUMMARY

### AdminDealerAction

| Metric | Value |
|--------|-------|
| Methods declared | 2 |
| Methods with any test coverage | 0 |
| Executable paths identified | 10 (E1, E2, P1–P8) |
| Paths covered by tests | 0 |
| Statement coverage (estimated) | 0% |
| Branch coverage (estimated) | 0% |

### AdminDriverAddAction

| Metric | Value |
|--------|-------|
| Methods declared | 1 |
| Methods with any test coverage | 0 |
| Executable paths identified | 17 (S1–S2, AG1–AG4, AU1–AU8, T1–T2) |
| Paths covered by tests | 0 |
| Statement coverage (estimated) | 0% |
| Branch coverage (estimated) | 0% |

---

## 5. FINDING INDEX

| ID | Severity | Scope | Description |
|----|----------|-------|-------------|
| A02-1 | CRITICAL | AdminDealerAction.execute() | Entire method — 0% coverage; all paths untested |
| A02-2 | CRITICAL | AdminDealerAction.prepareDealerRequest() | Entire method — 0% coverage; sole auth guard never tested |
| A02-3 | CRITICAL | AdminDriverAddAction.execute() | Entire method — 0% coverage; privilege-escalation path never tested |
| A02-4 | HIGH | prepareDealerRequest — path P1 | isSuperAdmin == false early-return not tested |
| A02-5 | HIGH | prepareDealerRequest — path P2 | isSuperAdmin absent from session → NPE untested |
| A02-6 | HIGH | prepareDealerRequest — path P3 | isSuperAdmin stored as non-Boolean → silent bypass untested |
| A02-7 | HIGH | AdminDriverAddAction — path S1 | Null session → NPE untested |
| A02-8 | HIGH | AdminDriverAddAction — path AG1 | Null opCode → NPE untested |
| A02-9 | HIGH | AdminDriverAddAction — path AG2 | DriverDAO failure → globalfailure forward untested |
| A02-10 | HIGH | AdminDriverAddAction — path AU1 | Cognito "User already exists" error handling untested |
| A02-11 | HIGH | AdminDriverAddAction — path AU2 | Cognito non-OK code error handling untested |
| A02-12 | HIGH | AdminDriverAddAction — path AU3 | Successful user creation + ROLE_SITEADMIN grant untested |
| A02-13 | HIGH | AdminDriverAddAction — path AU8 | Cognito/DB split-brain on SQLException untested |
| A02-14 | HIGH | AdminDriverAddAction — path T1 | Unrecognised op_code → null forward → NPE untested |
| A02-15 | MEDIUM | prepareDealerRequest — paths P4–P6 | Company/dealer partitioning logic untested |
| A02-16 | MEDIUM | prepareDealerRequest — path P7 | Null role authority → NPE untested |
| A02-17 | MEDIUM | AdminDriverAddAction — path S2 | Null/non-integer sessCompId → NumberFormatException untested |
| A02-18 | MEDIUM | AdminDriverAddAction — path AU4 | Null signUpResponse → NPE untested |
| A02-19 | MEDIUM | AdminDriverAddAction — path AU6 | Null message in non-OK Cognito response → null ActionMessage parameter untested |
| A02-20 | MEDIUM | AdminDealerAction cross-method | Null session propagated from execute() into prepareDealerRequest() untested |
| A02-21 | MEDIUM | AdminDealerAction — path E2 | Blank companyId read-only page load still calls prepareDealerRequest — untested |
| A02-22 | MEDIUM | prepareDealerRequest — path P8 | SQLException from getAllCompany() propagation untested |
| A02-23 | LOW | AdminDriverAddAction | Plaintext password in request scope via driverbean not caught by any test |
| A02-24 | LOW | AdminDealerAction.prepareDealerRequest | Public static visibility — external caller bypass not tested |
| A02-25 | INFO | Both actions | No integration/E2E test harness exists for any Struts action in the project |

---

## 6. RECOMMENDED TEST PRIORITIES

The following test scenarios address the highest-severity untested paths and should be implemented first:

1. **A02-2 / A02-4 / A02-5 / A02-6** — Unit tests for `prepareDealerRequest` with mocked `HttpSession` covering: `isSuperAdmin = true`, `isSuperAdmin = false`, `isSuperAdmin = null`, `isSuperAdmin = "false"` (String). These directly exercise the only access-control logic in the class.

2. **A02-3 / A02-12** — Unit test for `AdminDriverAddAction.execute()` with `op_code = "add_general_user"` and a mocked `RestClientService` returning an HTTP-OK Cognito response. Verify that `saveUserRoles` is called with `ROLE_SITEADMIN` and that `return_code = "successUser"`.

3. **A02-7 / A02-8** — Unit tests for `AdminDriverAddAction.execute()` with a null session and with a null `op_code`. Verify that a safe forward is returned rather than an uncaught exception.

4. **A02-13** — Integration test for the split-brain path: mock `signUpRequest()` to succeed but mock `saveUsers()` to throw `SQLException`. Verify the failure mode produces a user-facing error rather than a silent inconsistent state.

5. **A02-1 / A02-9 / A02-10 / A02-11** — Unit tests covering the remaining `AdminDealerAction.execute()` and `AdminDriverAddAction.execute()` paths once a Struts action test harness is in place.
