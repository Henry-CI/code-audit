# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A07
**Date:** 2026-02-26
**Files audited:**
- `src/main/java/com/action/AdminOperatorAction.java`
- `src/main/java/com/action/AdminRegisterAction.java`

---

## 1. Reading Evidence

### 1.1 AdminOperatorAction

**Full class name:** `com.action.AdminOperatorAction`
**Extends:** `PandoraAction` (which extends `org.apache.struts.action.Action`)
**Annotations:** `@Slf4j` (Lombok)

**Fields / instance-level dependencies (lines 18-20):**

| Field | Type | Initializer | Line |
|-------|------|-------------|------|
| `manufactureDAO` | `ManufactureDAO` | `ManufactureDAO.getInstance()` | 18 |
| `unitDAO` | `UnitDAO` | `UnitDAO.getInstance()` | 19 |
| `trainingDAO` | `TrainingDAO` | `new TrainingDAO()` | 20 |

**Methods:**

| Method | Visibility | Return | Lines | Notes |
|--------|-----------|--------|-------|-------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | `ActionForward` | 22-61 | Entry-point; switch on `action` param |
| `editAction(HttpServletRequest, Long)` | `private` | `String` | 63-66 | Forwards to `"operatoredit"` |
| `editUserAction(HttpServletRequest, Long, String)` | `private` | `String` | 68-71 | Forwards to `"useredit"` |
| `addAction(HttpServletRequest, String)` | `private` | `String` | 74-91 | Forwards to `"operatoredit"` |
| `addUserAction(HttpServletRequest, String)` | `private` | `String` | 93-104 | Forwards to `"useredit"` |
| `trainingAction(HttpServletRequest, Long, String, String)` | `private` | `String` | 106-113 | Forwards to `"operatortraining"` |
| `subscriptionAction(HttpServletRequest, Long, String)` | `private` | `String` | 115-121 | Forwards to `"operatorsubscription"` |
| `vehicleAction(HttpServletRequest, Long, String)` | `private` | `String` | 123-132 | Forwards to `"operatorvehicle"` |
| `deleteAction(HttpServletRequest, Long, String, String)` | `private` | `String` | 134-138 | Forwards to `"operatorlist"` |
| `deleteUserAction(HttpServletRequest, Long, String, String)` | `private` | `String` | 140-144 | Forwards to `"operatorlist"` |
| `inviteAction(HttpServletRequest, String)` | `private` | `String` | 146-151 | Forwards to `"operatorinvite"` |
| `searchAction(HttpServletRequest, String, String, String)` | `private` | `String` | 153-159 | Default case; conditional DAO branch |
| `searchUserAction(HttpServletRequest, String, String, String)` | `private` | `String` | 161-167 | Conditional DAO branch |

**Switch-case actions recognised (line 35):** `edit`, `edituser`, `add`, `adduser`, `training`, `subscription`, `vehicle`, `delete`, `deleteuser`, `invite`, `searchdriver`, `(default)`.

---

### 1.2 AdminRegisterAction

**Full class name:** `com.action.AdminRegisterAction`
**Extends:** `org.apache.struts.action.Action` (directly; does NOT extend PandoraAction)
**Annotations:** none

**Fields / constants:** none declared at class level (all objects are local within `execute`).

**Methods:**

| Method | Visibility | Return | Lines | Notes |
|--------|-----------|--------|-------|-------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | `ActionForward` | 39-301 | Main dispatch; branches on `accountAction` |
| `isValidEmailAddress(String)` | `private` | `boolean` | 303-310 | Regex email validator |

**Top-level accountAction branches (line 76 / 246 / 292):**

| Branch | Lines | Description |
|--------|-------|-------------|
| `register` or `add` | 76-245 | Sign-up / add sub-company flow |
| `update` | 246-289 | Update existing company info |
| `(else / unknown)` | 292-300 | Global error, forward `"failure"` |

**Forwards emitted:**

| Forward key | Conditions |
|-------------|-----------|
| `failure` | validation fail on register; Cognito error on register; `saveCompInfo` returns ≤0 or `saveDefualtSubscription` false; exception caught; unknown `accountAction` |
| `failAdd` | validation fail on add; Cognito error on add; `saveSubCompInfo` returns ≤0 |
| `successregister` | register path: `compId > 0` and default subscription saved |
| `successadd` | add path: `compId > 0` |
| `successupdate` | update path: HTTP 200 from `updateCompInfo` |
| `failUpdate` | update path: non-200 from `updateCompInfo` |

---

## 2. Test-Coverage Grep Confirmation

All four existing test files:
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

Grep for `AdminOperatorAction`, `AdminRegisterAction`, `operatorAction`, `registerAction` (case-insensitive) across the entire test directory returned **zero matches**.

**Conclusion: Both classes have 0% direct or indirect test coverage.**

---

## 3. Coverage Gap Findings

### AdminOperatorAction

---

**A07-1 | Severity: CRITICAL | No test coverage for AdminOperatorAction — entire class is untested**

`AdminOperatorAction` (169 lines, 13 methods) has zero test coverage. Every behaviour described in findings A07-2 through A07-16 below is therefore also completely uncovered.

---

**A07-2 | Severity: CRITICAL | Null-session NPE not tested — `execute()` calls `request.getSession(false)` which may return null**

At line 27, `request.getSession(false)` can return `null` if no session exists. The result is immediately used at line 32 as `session.getAttribute("sessDateFormat")` without a null check. No test exercises the no-session path; a production request with no active session causes an unhandled `NullPointerException`.

---

**A07-3 | Severity: HIGH | Null driverId not tested for action branches that require it**

`getLongRequestParam` (inherited from `PandoraAction`) returns `null` when the `driverId` parameter is absent or `"undefined"`. The following private methods receive that `null` and pass it directly into DAO calls without null-guards:
- `editAction` → `DriverDAO.getDriverById(null)` (line 64)
- `editUserAction` → `DriverDAO.getUserById(null, ...)` (line 69)
- `trainingAction` → `trainingDAO.getTrainingByDriver(null, ...)` (line 108)
- `subscriptionAction` → `DriverDAO.getUserById(null, ...)` and `CompanyDAO...getUserAlert(null, ...)` (lines 116-119)
- `vehicleAction` → `Long.valueOf(compId)` and `DriverUnitDAO.getDriverUnitsByCompAndDriver(...)` (lines 124-128)
- `deleteAction` → `DriverDAO.delDriverById(null, ...)` (line 135)
- `deleteUserAction` → `DriverDAO.delUserById(null, ...)` (line 141)

No test verifies safe handling or an appropriate error forward for a missing `driverId`.

---

**A07-4 | Severity: HIGH | Null / blank compId causes NumberFormatException in vehicleAction and addAction — not tested**

`vehicleAction` (line 124) calls `Long.valueOf(compId)` where `compId` is sourced from `getSessionAttribute(session, "sessCompId", "")`. If the session attribute is missing, the default is an empty string `""`, causing `NumberFormatException`. Similarly, `addAction` (line 88) calls `Long.valueOf(compId)`. Neither path is tested.

---

**A07-5 | Severity: HIGH | Default (unknown action) route not tested**

When `action` does not match any known case-label, `execute()` falls through to the default branch (line 59) which calls `searchAction`. No test verifies this routing, nor that `searchAction` is invoked correctly when `action` is null, blank, or unrecognised.

---

**A07-6 | Severity: HIGH | NullPointerException in searchAction when sessTimezone is null — not tested**

`searchAction` (line 156) calls `request.getSession().getAttribute("sessTimezone").toString()` without a null check. If `"sessTimezone"` has not been set in the session, this produces an unhandled NPE. No test covers either the null-timezone path or the non-empty-search branch in general.

---

**A07-7 | Severity: HIGH | deleteAction destroys data — DriverDAO.delDriverById called with no tested guards**

`deleteAction` (lines 135-137) permanently deletes a driver record. No test exists to verify:
- that the correct `driverId` is passed;
- that `getAllDriver` is called after deletion;
- that a null or invalid `driverId` results in an error rather than a silent DAO call.

---

**A07-8 | Severity: HIGH | deleteUserAction destroys data — DriverDAO.delUserById called with no tested guards**

Equivalent to A07-7 for the Cognito-backed user deletion path (lines 141-143).

---

**A07-9 | Severity: MEDIUM | searchAction empty-search vs non-empty-search branch not tested**

`searchAction` (lines 154-156) has two branches: when `search.trim().isEmpty()` it calls `getAllDriver`; otherwise it calls `getAllDriverSearch` (which also reads the session timezone). Neither branch is tested.

---

**A07-10 | Severity: MEDIUM | searchUserAction empty-search vs non-empty-search branch not tested**

`searchUserAction` (lines 162-164) mirrors the same binary branch for Cognito-based users. Neither branch is tested.

---

**A07-11 | Severity: MEDIUM | trainingAction sets multiple request attributes — none verified by any test**

`trainingAction` (lines 107-112) sets `driverId`, `trainings`, `manufacturers`, `types`, and `fuelTypes` on the request. No test asserts that any of these attributes are set correctly, including the case where any DAO call throws.

---

**A07-12 | Severity: MEDIUM | subscriptionAction makes four DAO calls — no exception-path test exists**

`subscriptionAction` (lines 116-120) calls `DriverDAO.getUserById` and three `CompanyDAO.getUserAlert` invocations. Any of these may throw. No test exercises the success path or any failure path.

---

**A07-13 | Severity: MEDIUM | addAction and addUserAction set multiple request attributes — not verified**

`addAction` (lines 74-91) constructs a `DriverVehicleBean` with `Long.valueOf(compId)` and sets five request attributes. `addUserAction` (lines 93-104) sets three. No test verifies construction logic or attribute population.

---

**A07-14 | Severity: MEDIUM | inviteAction builds DriverBean with comp_id — not tested**

`inviteAction` (lines 147-151) calls `DriverBean.builder().comp_id(compId).build()`. No test confirms the bean is correctly constructed or that the forward `"operatorinvite"` is returned.

---

**A07-15 | Severity: LOW | Instance-field DAO singletons initialised at class load — no test verifies injection or substitutability**

`ManufactureDAO.getInstance()` and `UnitDAO.getInstance()` are assigned at field-declaration time (lines 18-19), and `TrainingDAO` is `new`-ed (line 20). Because these are hard-coded into the field initialisers rather than injected, they cannot be replaced with mocks without PowerMock or a refactor. No test exercises this concern, and no documentation of this design decision exists.

---

**A07-16 | Severity: LOW | switch uses action.toLowerCase() but no test exercises mixed-case action values**

`action.toLowerCase()` (line 35) is applied before the switch, but `getRequestParam` returns the raw parameter value including any case variant. No test verifies that `"Edit"`, `"EDIT"`, or `"SEARCHDRIVER"` route correctly.

---

### AdminRegisterAction

---

**A07-17 | Severity: CRITICAL | No test coverage for AdminRegisterAction — entire class is untested**

`AdminRegisterAction` (311 lines, 2 methods) has zero test coverage. Every behaviour described in findings A07-18 through A07-35 below is therefore completely uncovered.

---

**A07-18 | Severity: CRITICAL | Null-session NPE — `execute()` calls `request.getSession(false)` at line 40 with no null check**

`request.getSession(false)` can return `null`. All subsequent `session.getAttribute(...)` calls at lines 42-49 would then throw an unhandled `NullPointerException`. No test exercises the no-session case.

---

**A07-19 | Severity: CRITICAL | Password written into email body in plain text — no test guards this behaviour**

On the `register` success path (lines 173-179), the company PIN (password) is concatenated directly into the email body sent via `Util.sendMail`. This is a sensitive data-exposure vulnerability. No test exists to flag or monitor this behaviour, meaning a future refactor could accidentally remove even this fragile mechanism without a failing test.

---

**A07-20 | Severity: HIGH | Validation logic has no unit tests — three independent validation branches**

The validation block (lines 89-98) checks:
1. `name.trim().equalsIgnoreCase("")` → `"error.company"`
2. `email.trim().equals("") || !isValidEmailAddress(email)` → `"errors.invalid.email"`
3. `pin.trim().equals("")` → `"error.entity.password"`

No test verifies that any of these errors is triggered, that the correct message key is set, or that the correct forward (`"failure"` vs `"failAdd"`) is returned for each case and for each `accountAction` value.

---

**A07-21 | Severity: HIGH | isValidEmailAddress regex not tested with any boundary inputs**

`isValidEmailAddress` (lines 303-310) is a private method using a hand-written regex. No test covers:
- valid typical addresses (e.g., `user@example.com`)
- empty string
- addresses with IP literals (`user@[192.168.1.1]`)
- addresses with special characters in the local part
- very long or Unicode-containing addresses
- addresses without a TLD
- `null` input (would throw NPE before the regex is reached)

---

**A07-22 | Severity: HIGH | Cognito "User already exists" path not tested**

Lines 133-148 check `signUpResponse.getMessage().contains("User already exists")` and route to `"failAdd"` or `"failure"`. No test verifies:
- that this string comparison is robust (case-sensitivity, substring position);
- that `getMessage()` can be `null` (NPE risk at line 133);
- the correct forward for each `accountAction` value.

---

**A07-23 | Severity: HIGH | Non-200 Cognito response path not tested**

Lines 149-164 handle any non-200 Cognito response code other than "User already exists". No test verifies the forward selection or error-message population.

---

**A07-24 | Severity: HIGH | saveCompInfo failure path (compId <= 0 or saveDefualtSubscription returns false) not tested**

Lines 182-191: when `compId <= 0` or `saveDefualtSubscription(compId)` returns `false`, an `"errors.general"` message is added and forward `"failure"` is returned. No test covers this path. Note also the typo `saveDefualtSubscription` (misspelled "Default") which could indicate a method that itself has never been integration-tested from this call site.

---

**A07-25 | Severity: HIGH | saveSubCompInfo failure path (compId <= 0 on add) not tested**

Lines 209-218: the add path returns `"failAdd"` when `saveSubCompInfo` returns ≤0. No test exercises this branch.

---

**A07-26 | Severity: HIGH | Exception catch-all in register/add path loses root cause — not tested**

Lines 234-245: any exception thrown anywhere in the register/add block is silently swallowed by `e.printStackTrace()`, a generic error message is set, and forward `"failure"` is returned. No test verifies which exceptions are caught, whether the error message is correctly set, or whether the logging is sufficient for diagnosis.

---

**A07-27 | Severity: HIGH | update path — updateCompInfo non-200 response returns no exception but silently fails — not tested**

Lines 273-288: when `updateCompInfo` returns a non-200 code, `failUpdate` is returned. No test verifies that the error message from the response is propagated, that `RoleDAO.getRoles()` is called, or that `companyRecord` is correctly populated.

---

**A07-28 | Severity: HIGH | Unknown / null accountAction path not tested**

Lines 292-300: an `accountAction` that is not `"register"`, `"add"`, or `"update"` (including `null`, empty string, or any other value) results in a global-error forward `"failure"`. No test exercises this path; a null `accountAction` from the form would cause a NPE at line 76 (`accountAction.equalsIgnoreCase(...)`) before reaching this else-branch.

---

**A07-29 | Severity: HIGH | Null accountAction causes NPE before else-branch is reached**

`adminRegisterActionForm.getAccountAction()` (line 48) can return `null` if the form field is not populated. `accountAction.equalsIgnoreCase("register")` at line 76 would then throw an unhandled `NullPointerException`. No test exercises a null `accountAction`.

---

**A07-30 | Severity: MEDIUM | update path success — isSuperAdmin / isDealerLogin branching not tested**

Lines 253-259 (update path): the company list is fetched via `LoginDAO.getInstance().getCompanies(...)` when `isSuperAdmin || isDealerLogin`, or via `compDao.getCompanyContactsByCompId(...)` otherwise. The same branching logic exists in the add path (lines 200-204). No test verifies either branch, nor the case where `isSuperAdmin` is `null` (would cause NPE at line 255 via unboxing `Boolean`).

---

**A07-31 | Severity: MEDIUM | isSuperAdmin null-unboxing NPE not tested**

Both update (line 253) and add (line 199) paths read `(Boolean) session.getAttribute("isSuperAdmin")` and use it in `if (isSuperAdmin || isDealerLogin)`. Auto-unboxing a `null` Boolean causes a `NullPointerException`. No test verifies the behaviour when this session attribute is missing.

---

**A07-32 | Severity: MEDIUM | isDealerLogin null-unboxing NPE not tested**

`isDealerLogin` (line 49) is read as `(Boolean) session.getAttribute("isDealerLogin")`. Auto-unboxing `null` in the conditional `isSuperAdmin || isDealerLogin` causes a NPE. No test covers the case where `isDealerLogin` is absent from the session.

---

**A07-33 | Severity: MEDIUM | register path success — email sent with no error handling — not tested**

`Util.sendMail(...)` (line 178) is called on the success path with no try-catch around it. A mail-server failure would propagate as an unchecked exception and be caught by the outer catch (lines 234-245), returning `"failure"` even though the company was already saved in the database. No test verifies this partial-success / compensation behaviour.

---

**A07-34 | Severity: MEDIUM | update path — arrComp.get(0) not tested for empty list — IndexOutOfBoundsException risk**

Line 269: `arrComp.get(0).getRoles()` is called without verifying that `arrComp` is non-empty. If `getCompanyContactsByCompId` returns an empty list, this throws `IndexOutOfBoundsException`. No test covers the empty-list case.

---

**A07-35 | Severity: LOW | CompanyBean is populated from form fields before any validation — not tested**

Lines 54-71 map all form fields onto a `CompanyBean` before the `accountAction` check. Fields such as `password` (line 61) and `pin` (line 62) are transferred regardless of whether validation will fail. While this is not a security vulnerability by itself, it means sensitive data lives in memory longer than necessary, and no test verifies the shape of the bean at this stage.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A07-1 | CRITICAL | AdminOperatorAction | Entire class has zero test coverage |
| A07-2 | CRITICAL | AdminOperatorAction | NPE when session is null (`getSession(false)` returns null) |
| A07-3 | HIGH | AdminOperatorAction | Null `driverId` passed to DAO calls without null-guard |
| A07-4 | HIGH | AdminOperatorAction | Blank `compId` causes `NumberFormatException` in `vehicleAction`/`addAction` |
| A07-5 | HIGH | AdminOperatorAction | Default (unknown action) route not tested |
| A07-6 | HIGH | AdminOperatorAction | NPE in `searchAction` when `sessTimezone` session attribute is null |
| A07-7 | HIGH | AdminOperatorAction | Destructive `deleteAction` has no tested guards |
| A07-8 | HIGH | AdminOperatorAction | Destructive `deleteUserAction` has no tested guards |
| A07-9 | MEDIUM | AdminOperatorAction | `searchAction` empty vs non-empty search branch not tested |
| A07-10 | MEDIUM | AdminOperatorAction | `searchUserAction` empty vs non-empty search branch not tested |
| A07-11 | MEDIUM | AdminOperatorAction | `trainingAction` request attributes not verified; exception path uncovered |
| A07-12 | MEDIUM | AdminOperatorAction | `subscriptionAction` four DAO calls — no exception path tested |
| A07-13 | MEDIUM | AdminOperatorAction | `addAction`/`addUserAction` attribute population not tested |
| A07-14 | MEDIUM | AdminOperatorAction | `inviteAction` DriverBean construction not tested |
| A07-15 | LOW | AdminOperatorAction | Hard-coded singleton DAOs prevent mocking without PowerMock |
| A07-16 | LOW | AdminOperatorAction | Mixed-case `action` parameter routing not tested |
| A07-17 | CRITICAL | AdminRegisterAction | Entire class has zero test coverage |
| A07-18 | CRITICAL | AdminRegisterAction | NPE when session is null (`getSession(false)` returns null) |
| A07-19 | CRITICAL | AdminRegisterAction | Plain-text password emailed with no test guarding the behaviour |
| A07-20 | HIGH | AdminRegisterAction | All three validation branches completely untested |
| A07-21 | HIGH | AdminRegisterAction | `isValidEmailAddress` regex untested against any input |
| A07-22 | HIGH | AdminRegisterAction | Cognito "User already exists" path not tested; `getMessage()` NPE risk |
| A07-23 | HIGH | AdminRegisterAction | Cognito non-200 response path not tested |
| A07-24 | HIGH | AdminRegisterAction | `saveCompInfo` / `saveDefualtSubscription` failure path not tested |
| A07-25 | HIGH | AdminRegisterAction | `saveSubCompInfo` failure path not tested |
| A07-26 | HIGH | AdminRegisterAction | Exception catch-all swallows root cause — no test coverage |
| A07-27 | HIGH | AdminRegisterAction | `updateCompInfo` non-200 failure path not tested |
| A07-28 | HIGH | AdminRegisterAction | Unknown `accountAction` else-branch not tested |
| A07-29 | HIGH | AdminRegisterAction | Null `accountAction` causes NPE before any branch is reached |
| A07-30 | MEDIUM | AdminRegisterAction | `isSuperAdmin`/`isDealerLogin` branching untested in both add and update paths |
| A07-31 | MEDIUM | AdminRegisterAction | Null `isSuperAdmin` Boolean causes NPE on unboxing |
| A07-32 | MEDIUM | AdminRegisterAction | Null `isDealerLogin` Boolean causes NPE on unboxing |
| A07-33 | MEDIUM | AdminRegisterAction | `Util.sendMail` failure on register success path not tested |
| A07-34 | MEDIUM | AdminRegisterAction | `arrComp.get(0)` called without empty-list guard — IOOBE risk |
| A07-35 | LOW | AdminRegisterAction | Sensitive fields mapped to bean before validation; never tested |

**Total findings: 35**
- CRITICAL: 5
- HIGH: 17
- MEDIUM: 11
- LOW: 2

---

## 5. Recommended Test Strategy

### AdminOperatorAction

1. **Test harness:** Use Mockito to mock `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `ActionMapping`, and all DAO classes. Replace singleton field assignments using reflection or refactor to constructor injection.
2. **Session-null guard:** Add and test a null-check on the return value of `request.getSession(false)` that forwards to an error page.
3. **Switch dispatch tests:** One test per `action` string value confirming the correct private method is invoked and the correct forward key is returned.
4. **driverId null tests:** Verify that each action requiring a non-null `driverId` returns a controlled error when `driverId` is absent.
5. **compId blank tests:** Verify that `vehicleAction` and `addAction` handle a blank or null `compId` without throwing `NumberFormatException`.
6. **searchAction timezone null:** Add null check before `.toString()` and test both branches of the search predicate.
7. **Delete action guards:** Verify that `deleteAction` and `deleteUserAction` do not proceed with a null `driverId`.

### AdminRegisterAction

1. **Test harness:** Use Mockito for `HttpServletRequest`, `HttpSession`, `ActionMapping`, `AdminRegisterActionForm`, `CompanyDAO`, `LoginDAO`, `SubscriptionDAO`, and `RestClientService`.
2. **Validation unit tests:** Test each of the three validation error paths (`name` empty, `email` invalid/empty, `pin` empty) independently for both `"register"` and `"add"` `accountAction` values.
3. **`isValidEmailAddress` unit tests:** Extract to a package-private or protected method (or test via reflection) and cover: valid email, empty string, null, no-TLD, IP-literal, special characters.
4. **Null `accountAction`:** Test that a `null` `accountAction` is handled without NPE (likely requires a null-check in `execute` before line 76).
5. **Cognito response tests:** Mock `RestClientService` to return: user-already-exists response, non-200 non-duplicate response, and 200 success response.
6. **Register success path:** Verify `Util.sendMail` is called with correct content (without including the raw password — this also serves as a security regression test).
7. **Add success path:** Verify `isSuperAdmin` and `isDealerLogin` branches, including null-value cases.
8. **Update success and failure paths:** Verify forward selection, session attribute mutation, and request attribute population.
9. **Exception catch-all:** Verify that a DAO exception results in `"failure"` forward and correct error message key.
10. **Empty company list guard:** Add `arrComp.isEmpty()` check before `arrComp.get(0)` on the update success path and test it.
