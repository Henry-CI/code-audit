# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A09
**Date:** 2026-02-26
**Files audited:**
- `src/main/java/com/action/AdminTrainingsAction.java`
- `src/main/java/com/action/AdminUnitAccessAction.java`

---

## 1. Reading-Evidence Block

### 1.1 AdminTrainingsAction

**File:** `src/main/java/com/action/AdminTrainingsAction.java`
**Class:** `com.action.AdminTrainingsAction` (extends `PandoraAction`)

| Element | Kind | Line |
|---|---|---|
| `trainingDAO` | field — `TrainingDAO` instance, initialised inline | 15 |
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | public method (override) | 17–43 |

**Internal structure of `execute`:**
- Line 21: casts `actionForm` to `AdminTrainingsActionForm` (unchecked, hard-cast)
- Line 22: `request.getSession(false)` — returns `null` when no session exists
- Line 23: reads `"sessDateFormat"` from session — no null-guard on session reference
- Lines 25–42: `switch` on `trainingsForm.getAction()`
  - `"add"` branch (lines 26–36): builds `DriverTrainingBean` via builder, calls `trainingDAO.addTraining(bean, dateFormat)`, returns `null`
  - `"delete"` branch (lines 37–39): calls `trainingDAO.deleteTraining(trainingsForm.getTraining())`, returns `null`
  - `default` branch (lines 40–41): returns `null` silently

**Fields on `AdminTrainingsActionForm` (via `@Getter`/`@Setter` Lombok):**
- `action` (String, default null) — line 14
- `driver` (Long, default null) — line 16
- `manufacturer` (Long, default null) — line 17
- `type` (Long, default null) — line 18
- `fuelType` (Long, default null) — line 19
- `trainingDate` (String, default null) — line 20
- `expirationDate` (String, default null) — line 21
- `training` (Long, default null) — line 23

---

### 1.2 AdminUnitAccessAction

**File:** `src/main/java/com/action/AdminUnitAccessAction.java`
**Class:** `com.action.AdminUnitAccessAction` (extends `PandoraAction`)

| Element | Kind | Line |
|---|---|---|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | public method (override) | 17–37 |

**Internal structure of `execute`:**
- Line 18: `request.getSession(false)` — returns `null` when no session exists
- Line 19: reads `"sessCompId"` from session; applies null-coalesce to empty string `""` — but session itself is not null-checked
- Line 20: calls inherited `getRequestParam(request, "action", (String) null)` — returns `null` when param absent
- Line 21: `Integer.parseInt(sessCompId)` — throws `NumberFormatException` when `sessCompId` is `""` (the coalesced value) or any non-integer string
- Line 23: casts `actionForm` to `AdminUnitAccessForm` (unchecked, hard-cast)
- Lines 25–31: `if ("save".equalsIgnoreCase(action))` branch
  - Line 26: `accessForm.getUnit(sessCompId)` — builds a `UnitBean`; `sessCompId` at this point is `""` when session attribute was null, which will be used as `comp_id`
  - Line 27: `UnitDAO.saveUnitAccessInfo(unitBean)` — static DAO call; `unitBean.getId()` is used in a `Long.valueOf(unitBean.getId())` inside the DAO with no null guard; throws `NumberFormatException` or `NullPointerException` if `id` is blank/null
- Lines 28–31: else (load) branch
  - Line 29: `UnitDAO.getUnitById(accessForm.getId()).get(0)` — `Integer.parseInt(id)` inside `UnitsByIdQuery`; `.get(0)` throws `IndexOutOfBoundsException` if the list is empty (unit not found)
  - Line 30: `accessForm.setUnit(unitBean)` — populates form from DB bean
- Line 33: `UnitDAO.getAllUnitsByCompanyId(companyId)` — executed on every request regardless of branch; uses `companyId` parsed on line 21
- Line 34: places unit list in request attribute `"arrAdminUnit"`
- Line 36: `mapping.findForward("success")` — only forward used; `null` return from `findForward` if forward not configured

**Fields on `AdminUnitAccessForm` (via `@Data` Lombok):**
- `id` (String) — line 25
- `accessible` (boolean) — line 26
- `access_type` (String) — line 27
- `keypad_reader` (String) — line 28
- `facility_code` (String) — line 29
- `access_id` (String) — line 30

**`UnitBean.KeypadReaderModel` enum values (relevant to form-to-bean conversion):**
- `ROSLARE`, `KERI`, `SMART`, `HID_ICLASS`

---

## 2. Test-Coverage Grep Confirmation

The test suite contains exactly four files:
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

A grep of the entire test directory for all relevant identifiers produced **zero matches**:

| Search term | Matches |
|---|---|
| `AdminTrainingsAction` | 0 |
| `AdminUnitAccessAction` | 0 |
| `AdminTrainingsActionForm` | 0 |
| `AdminUnitAccessForm` | 0 |
| `TrainingDAO` | 0 |
| `UnitDAO` | 0 |
| `DriverTrainingBean` | 0 |
| `UnitBean` | 0 |

**Conclusion:** Neither action class has any direct or indirect test coverage.

---

## 3. Coverage Gap Findings

---

### A09-1 | Severity: CRITICAL | AdminTrainingsAction.execute — null session causes NullPointerException

`request.getSession(false)` returns `null` when no session exists. The return value is assigned directly to `session` (line 22) and immediately dereferenced on line 23 (`session.getAttribute("sessDateFormat")`). There is no null-check on `session`. Any unauthenticated or session-expired request will throw a `NullPointerException` and produce an HTTP 500 rather than a controlled redirect.

**Untested paths:**
- Request with no active session (session-expired scenario)
- Request where the server has invalidated the session between the action dispatch and this line

**Location:** `AdminTrainingsAction.java` lines 22–23

---

### A09-2 | Severity: CRITICAL | AdminUnitAccessAction.execute — null session causes NullPointerException

Identical pattern to A09-1. `request.getSession(false)` on line 18 can return `null`. The result is used on line 19 without a null-check (`session.getAttribute("sessCompId")`). A session-expired or unauthenticated request will throw `NullPointerException`.

**Untested paths:**
- Request with no active session

**Location:** `AdminUnitAccessAction.java` lines 18–19

---

### A09-3 | Severity: CRITICAL | AdminUnitAccessAction.execute — NumberFormatException when sessCompId is absent

When `session.getAttribute("sessCompId")` returns `null`, `sessCompId` is coalesced to `""` (line 19). On line 21, `Integer.parseInt("")` throws `NumberFormatException`. This is an unhandled runtime exception that will produce an HTTP 500 with no error message to the user.

**Untested paths:**
- Session exists but `sessCompId` attribute has not been set
- Session attribute is an empty string

**Location:** `AdminUnitAccessAction.java` lines 19–21

---

### A09-4 | Severity: CRITICAL | AdminUnitAccessAction.execute — IndexOutOfBoundsException when unit not found

In the else (load) branch, line 29 calls `UnitDAO.getUnitById(accessForm.getId()).get(0)`. If the unit ID does not correspond to any database record, `getUnitById` returns an empty list and `.get(0)` throws `IndexOutOfBoundsException`. This can be triggered by any tampered or stale `id` form parameter.

**Untested paths:**
- Form `id` refers to a unit that has been deleted
- Form `id` refers to a unit in a different company
- `getUnitById` returns an empty result for any reason

**Location:** `AdminUnitAccessAction.java` line 29

---

### A09-5 | Severity: HIGH | AdminTrainingsAction.execute — no test for "add" action branch

The `"add"` switch branch (lines 26–36) is completely untested. This branch:
- Builds a `DriverTrainingBean` from form fields — any null Long field (driver, manufacturer, type, fuelType) will silently be passed to the DAO as `null`, which may cause SQL errors or `NullPointerException` inside `TrainingDAO.addTraining`
- Relies on `dateFormat` from session, which may be `null` if `"sessDateFormat"` is not set; `DateUtil.stringToSQLDate` is then called with a `null` format string
- Returns `null` rather than a named forward — the Struts framework behaviour on a `null` ActionForward is undefined / container-specific

**Untested paths:**
- Happy-path add with all required fields populated
- Add with null `driver` field
- Add with null `trainingDate` or `expirationDate`
- Add with null `dateFormat` from session
- `TrainingDAO.addTraining` throws `SQLException`

**Location:** `AdminTrainingsAction.java` lines 26–36

---

### A09-6 | Severity: HIGH | AdminTrainingsAction.execute — no test for "delete" action branch

The `"delete"` switch branch (lines 37–39) is completely untested. `trainingsForm.getTraining()` defaults to `null` (field initialised to `null` in `AdminTrainingsActionForm` line 23). Passing `null` to `TrainingDAO.deleteTraining(Long trainingId)` causes `stmt.setLong(1, trainingId)` to throw a `NullPointerException` (auto-unboxing of `null` Long).

**Untested paths:**
- Happy-path delete with a valid training ID
- Delete with `training` field null (form not populated)
- `TrainingDAO.deleteTraining` throws `SQLException`

**Location:** `AdminTrainingsAction.java` lines 37–39

---

### A09-7 | Severity: HIGH | AdminUnitAccessAction.execute — no test for "save" action branch

The `"save"` branch (lines 25–27) is completely untested. Key risks:
- `accessForm.getUnit(sessCompId)` calls `UnitBean.KeypadReaderModel.valueOf(keypad_reader)` when `keypad_reader` is non-blank; an unrecognised enum value throws `IllegalArgumentException`
- The resulting `UnitBean` has its `id` set from `accessForm.getId()`; inside `UnitDAO.saveUnitAccessInfo`, `Long.valueOf(unitBean.getId())` throws `NumberFormatException` if `id` is blank or null
- `UnitDAO.saveUnitAccessInfo` throws `Exception` (not just `SQLException`); the checked exception declaration on `execute` is `throws Exception`, so this propagates unhandled

**Untested paths:**
- Happy-path save with all fields valid
- Save with blank `id` (new unit scenario — but the DAO SQL is an UPDATE, not an INSERT, so this silently updates zero rows)
- Save with invalid `keypad_reader` string value
- Save with `sessCompId` coalesced to `""` (empty comp_id written to DB)
- `saveUnitAccessInfo` throws `Exception`

**Location:** `AdminUnitAccessAction.java` lines 25–27

---

### A09-8 | Severity: HIGH | AdminUnitAccessAction.execute — no test for load (else) branch

The else (data-load) branch (lines 28–31) is completely untested. See also A09-4. Additional risks:
- `accessForm.getId()` may be `null` or non-numeric; `Integer.parseInt(id)` inside `UnitsByIdQuery.prepare()` throws `NumberFormatException`
- `accessForm.setUnit(unitBean)` accesses `unitBean.getKeypad_reader()` which may be `null` — the null-guard exists (line 56 of `AdminUnitAccessForm`), but the surrounding path is entirely untested

**Untested paths:**
- Happy-path load with a valid numeric ID
- Load with null `id`
- Load with non-numeric `id`

**Location:** `AdminUnitAccessAction.java` lines 28–31

---

### A09-9 | Severity: HIGH | AdminTrainingsAction.execute — null return on all branches bypasses Struts forward mechanism

All three branches of the `switch` statement (`"add"`, `"delete"`, `default`) return `null`. In Struts 1, returning `null` from `execute` instructs the framework to not forward or redirect. This means the browser receives no response body after a successful add or delete — the request simply completes with an empty response unless the caller relies on an AJAX contract. This behaviour is undocumented in the code and is not validated by any test.

**Untested paths:**
- Verification that the caller (JavaScript/AJAX) correctly handles a null-forward (empty body) response
- Verification that the null return does not cause downstream Struts processing errors

**Location:** `AdminTrainingsAction.java` lines 36, 39, 41

---

### A09-10 | Severity: HIGH | AdminTrainingsAction.execute — null sessDateFormat passed to DAO

If the session exists but `"sessDateFormat"` has not been populated (e.g., the session was partially initialised), `dateFormat` is `null` (line 23). This value is passed to `trainingDAO.addTraining(bean, dateFormat)` (line 35), where it is forwarded to `DateUtil.stringToSQLDate(trainingDate, dateFormat)`. Passing a `null` format string to a date parser typically causes `NullPointerException` or `IllegalArgumentException`. No test validates this path.

**Untested paths:**
- Session exists but `sessDateFormat` attribute is not set

**Location:** `AdminTrainingsAction.java` lines 23, 35

---

### A09-11 | Severity: MEDIUM | AdminTrainingsAction.execute — default switch branch silently swallows unknown actions

An unrecognised `action` value (including `null`, which is the field default) falls through to the `default` branch and returns `null` with no error, no logging, and no user feedback. No test validates that this silent discard is intentional or that it does not mask incorrect client behaviour.

**Untested paths:**
- `trainingsForm.getAction()` returns `null` (form never populated)
- `trainingsForm.getAction()` returns an unrecognised string such as `"edit"` or `"update"`

**Location:** `AdminTrainingsAction.java` lines 40–41

---

### A09-12 | Severity: MEDIUM | AdminUnitAccessAction.execute — getAllUnitsByCompanyId always called, even on failed save

`UnitDAO.getAllUnitsByCompanyId(companyId)` on line 33 is executed unconditionally after both the save and the load branches. If `companyId` is 0 (because `sessCompId` was `""` and `Integer.parseInt` — see A09-3 — somehow produced a default), or if the DAO call fails with `SQLException`, the exception propagates through `execute`. No test validates the fallback behaviour or confirms the unit list is populated correctly for the page regardless of the save/load outcome.

**Untested paths:**
- `getAllUnitsByCompanyId` throws `SQLException`
- `companyId` is 0 or negative
- Unit list is empty (company has no active units)

**Location:** `AdminUnitAccessAction.java` line 33

---

### A09-13 | Severity: MEDIUM | AdminUnitAccessAction.execute — "save" branch: empty sessCompId written as comp_id to UnitBean

When `session.getAttribute("sessCompId")` is `null`, `sessCompId` coalesces to `""` (line 19). In the save branch, `accessForm.getUnit(sessCompId)` passes `""` as `compId`. Inside `AdminUnitAccessForm.getUnit()`, `comp_id` is set directly to that empty string. `UnitDAO.saveUnitAccessInfo` does not use `comp_id` in its UPDATE SQL, so this silently overwrites access fields with no company context validation. An attacker with a partial session could save access data without a valid company binding. No test verifies the company-ID guard.

**Untested paths:**
- Save where the session `sessCompId` attribute is missing
- Save where `sessCompId` belongs to a different company than the unit being saved

**Location:** `AdminUnitAccessAction.java` lines 19, 26; `AdminUnitAccessForm.java` line 40–47

---

### A09-14 | Severity: MEDIUM | AdminUnitAccessAction.execute — invalid keypad_reader enum value causes uncaught IllegalArgumentException

In `AdminUnitAccessForm.getUnit()` (line 46), `UnitBean.KeypadReaderModel.valueOf(keypad_reader)` is called when `keypad_reader` is non-blank. Valid values are `ROSLARE`, `KERI`, `SMART`, `HID_ICLASS`. Any other string (e.g., from a tampered form submission) causes `IllegalArgumentException`. This exception is not caught anywhere in the action or form classes and propagates as an HTTP 500.

**Untested paths:**
- `keypad_reader` contains an unrecognised string value
- `keypad_reader` contains a value with different capitalisation (enum lookup is case-sensitive)

**Location:** `AdminUnitAccessForm.java` line 46; triggered via `AdminUnitAccessAction.java` line 26

---

### A09-15 | Severity: MEDIUM | AdminTrainingsAction — trainingDAO field is a concrete instance, making unit testing impossible without refactoring

`trainingDAO` is initialised inline as `new TrainingDAO()` on line 15. There is no constructor injection, setter injection, or interface abstraction. `TrainingDAO` is a concrete class with direct JDBC calls. This makes it impossible to mock the DAO in a unit test without a live database connection or bytecode manipulation (e.g., PowerMock). No tests exist, but this design prevents straightforward test authoring.

**Location:** `AdminTrainingsAction.java` line 15

---

### A09-16 | Severity: LOW | AdminUnitAccessAction — no validation in AdminUnitAccessForm.validate()

`AdminUnitAccessForm.validate()` (lines 33–37 of `AdminUnitAccessForm.java`) returns an empty `ActionErrors` object unconditionally. No field-level validation is performed — `id`, `access_type`, `keypad_reader`, `facility_code`, and `access_id` are accepted without any check. This means:
- A blank `id` passes validation and reaches the DAO where it causes a runtime exception (see A09-7)
- An invalid `keypad_reader` passes validation and causes `IllegalArgumentException` in the DAO layer (see A09-14)

No test verifies that validation is being intentionally skipped or that the empty-errors contract is correct.

**Location:** `AdminUnitAccessForm.java` lines 33–37

---

### A09-17 | Severity: LOW | AdminTrainingsAction.execute — no validation of form field nullity before building DriverTrainingBean

In the `"add"` branch, all form fields (`driver`, `manufacturer`, `type`, `fuelType`, `trainingDate`, `expirationDate`) default to `null` in `AdminTrainingsActionForm`. The code builds a `DriverTrainingBean` without asserting that mandatory fields are non-null. `TrainingDAO.addTraining` calls `stmt.setLong(1, trainingBean.getDriver_id())` which auto-unboxes the Long — a `null` Long causes `NullPointerException`. No test validates this constraint.

**Untested paths:**
- Add request submitted without driver, manufacturer, type, or fuelType values

**Location:** `AdminTrainingsAction.java` lines 27–34; `TrainingDAO.java` line 61

---

### A09-18 | Severity: LOW | AdminUnitAccessAction.execute — UnitDAO.getUnitById accepts null or non-numeric id without guard

`accessForm.getId()` returns the raw string from the form. `UnitDAO.getUnitById(String id)` passes it directly to `Integer.parseInt(id)` (UnitDAO line 290). If `id` is `null` or non-numeric, a `NullPointerException` or `NumberFormatException` is thrown before any DB query. This is not documented or tested.

**Untested paths:**
- Load request with `id` param absent (null)
- Load request with `id` param set to a non-integer string

**Location:** `AdminUnitAccessAction.java` line 29; `UnitDAO.java` line 290

---

### A09-19 | Severity: INFO | No test exists for PandoraAction.getRequestParam used by AdminUnitAccessAction

`AdminUnitAccessAction.execute` calls the inherited `getRequestParam(request, "action", (String) null)` (line 20 of the action). `PandoraAction.getRequestParam(HttpServletRequest, String, String)` returns `null` when the parameter is absent (not blank, but literally absent from the request). This is a subtlety — a present-but-blank `action` parameter returns `""`, while an absent one returns `null`. The `"save".equalsIgnoreCase(null)` call on line 25 returns `false` safely, but the semantic difference between absent and blank action is untested and undocumented.

**Location:** `PandoraAction.java` lines 24–27; `AdminUnitAccessAction.java` line 20

---

### A09-20 | Severity: INFO | AdminTrainingsAction — both DAO methods declare throws SQLException but execute declares throws Exception; exception propagation is untested

`trainingDAO.addTraining` and `trainingDAO.deleteTraining` both declare `throws SQLException`. `execute` declares `throws Exception`. Any `SQLException` from the DAO propagates uncaught through the action to the Struts framework's default exception handler, which typically renders a generic error page. No test verifies this error-path behaviour or checks that appropriate error information is surfaced to the user.

**Location:** `AdminTrainingsAction.java` line 20

---

## 4. Summary Table

| Finding | Severity | Description |
|---|---|---|
| A09-1 | CRITICAL | AdminTrainingsAction: null session reference — NullPointerException on `getSession(false)` |
| A09-2 | CRITICAL | AdminUnitAccessAction: null session reference — NullPointerException on `getSession(false)` |
| A09-3 | CRITICAL | AdminUnitAccessAction: `Integer.parseInt("")` — NumberFormatException when `sessCompId` absent |
| A09-4 | CRITICAL | AdminUnitAccessAction: `.get(0)` on empty list — IndexOutOfBoundsException when unit not found |
| A09-5 | HIGH | AdminTrainingsAction: "add" branch entirely untested, null field risks |
| A09-6 | HIGH | AdminTrainingsAction: "delete" branch entirely untested, null training ID auto-unbox NPE |
| A09-7 | HIGH | AdminUnitAccessAction: "save" branch entirely untested, enum/parse/blank-id risks |
| A09-8 | HIGH | AdminUnitAccessAction: load branch entirely untested, null/non-numeric id risks |
| A09-9 | HIGH | AdminTrainingsAction: all branches return null ActionForward — undocumented/untested contract |
| A09-10 | HIGH | AdminTrainingsAction: null `sessDateFormat` propagated to DAO date parser |
| A09-11 | MEDIUM | AdminTrainingsAction: default branch silently discards unknown/null action values |
| A09-12 | MEDIUM | AdminUnitAccessAction: `getAllUnitsByCompanyId` unconditional call not tested for failure or empty result |
| A09-13 | MEDIUM | AdminUnitAccessAction: empty `sessCompId` written as comp_id on save — no company validation |
| A09-14 | MEDIUM | AdminUnitAccessAction: invalid `keypad_reader` string causes uncaught IllegalArgumentException |
| A09-15 | MEDIUM | AdminTrainingsAction: concrete DAO instantiation prevents unit testing without refactoring |
| A09-16 | LOW | AdminUnitAccessForm.validate() always returns empty errors — no field validation |
| A09-17 | LOW | AdminTrainingsAction: null Long fields in DriverTrainingBean cause NPE in DAO auto-unbox |
| A09-18 | LOW | AdminUnitAccessAction: null or non-numeric `id` not guarded before DAO parse call |
| A09-19 | INFO | PandoraAction.getRequestParam null-vs-blank action parameter distinction untested |
| A09-20 | INFO | SQLException propagation from DAO through execute to Struts error handler untested |

**Total findings: 20**
CRITICAL: 4 | HIGH: 6 | MEDIUM: 5 | LOW: 3 | INFO: 2
