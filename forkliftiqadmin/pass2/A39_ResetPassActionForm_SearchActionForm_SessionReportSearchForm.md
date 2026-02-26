# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A39
**Auditor model:** claude-sonnet-4-6

## Source files audited
| # | File |
|---|------|
| 1 | `src/main/java/com/actionform/ResetPassActionForm.java` |
| 2 | `src/main/java/com/actionform/SearchActionForm.java` |
| 3 | `src/main/java/com/actionform/SessionReportSearchForm.java` |

## Test directory scanned
`src/test/java/`

Existing test files (all test files found in the directory):
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

---

## Reading Evidence

### 1. ResetPassActionForm
**File:** `src/main/java/com/actionform/ResetPassActionForm.java`
**Class:** `ResetPassActionForm extends ActionForm`

**Fields:**
| Field | Type | Line | Initial value |
|-------|------|------|---------------|
| `email` | `String` | 13 | `null` |
| `question` | `String` | 14 | `null` |
| `answer` | `String` | 15 | `null` |
| `name` | `String` | 16 | `null` |

**Methods:**
| Method signature | Lines | Notes |
|-----------------|-------|-------|
| `getName()` | 18–20 | getter |
| `setName(String name)` | 21–23 | setter |
| `getQuestion()` | 24–26 | getter |
| `setQuestion(String question)` | 27–29 | setter |
| `getAnswer()` | 30–32 | getter |
| `setAnswer(String answer)` | 33–35 | setter |
| `getEmail()` | 37–39 | getter |
| `setEmail(String email)` | 40–42 | setter |
| `validate(ActionMapping, HttpServletRequest)` | 44–60 | `@Override`; returns `ActionErrors`; calls `name.equalsIgnoreCase("")` (line 49) and `email.equalsIgnoreCase("")` (line 54); NPE risk on null fields |

**Behavioural notes:**
- `validate()` calls `name.equalsIgnoreCase("")` without a null-guard. Because `name` is initialised to `null`, invoking `validate()` before `setName()` will throw `NullPointerException`.
- Same null-dereference risk exists for `email` on line 54.
- `question` and `answer` fields have getters/setters but are never read inside `validate()`, so their validation is absent.

---

### 2. SearchActionForm
**File:** `src/main/java/com/actionform/SearchActionForm.java`
**Class:** `SearchActionForm extends ActionForm`

**Fields:**
| Field | Type | Line | Initial value |
|-------|------|------|---------------|
| `fname` | `String` | 18 | `null` |
| `veh_id` | `String` | 19 | `null` |
| `attachment` | `String` | 20 | `null` |
| `arrAttachment` | `ArrayList` (raw) | 21 | `new ArrayList()` |

**Methods:**
| Method signature | Lines | Notes |
|-----------------|-------|-------|
| `SearchActionForm()` | 23–27 | constructor; `throws Exception`; calls `setArrAttachment()` |
| `getArrAttachment()` | 29–31 | getter |
| `setArrAttachment()` | 33–36 | calls `UnitDAO.getInstance().getAllUnitAttachment()`; `throws Exception`; tightly couples form to DAO |
| `getVeh_id()` | 38–40 | getter |
| `setVeh_id(String veh_id)` | 41–43 | setter |
| `getFname()` | 45–47 | getter |
| `setFname(String fname)` | 48–50 | setter |
| `reset(ActionMapping, HttpServletRequest)` | 52–54 | sets `fname = ""`; does not reset `veh_id` or `attachment` |
| `getAttachment()` | 56–58 | getter |
| `setAttachment(String attachment)` | 59–61 | setter |
| `validate(ActionMapping, HttpServletRequest)` | 63–75 | returns `ActionErrors`; calls `fname.equalsIgnoreCase("")` (line 66) and `veh_id.equalsIgnoreCase("")` (line 70); NPE risk on null fields |

**Behavioural notes:**
- Constructor calls `UnitDAO.getInstance()` — a live database call at construction time; this makes unit testing without mocking infrastructure impossible without a real DB or a mock of `UnitDAO`.
- `validate()` dereferences `fname` and `veh_id` without null-guards; both are initialised to `null`, so NPE will occur unless setters are called first (mitigated only partially by `reset()` which sets `fname` to `""` but leaves `veh_id` as `null`).
- Raw `ArrayList` usage (no generics) on line 21.
- `reset()` only resets `fname`, leaving `veh_id` and `attachment` unreset across requests.

---

### 3. SessionReportSearchForm
**File:** `src/main/java/com/actionform/SessionReportSearchForm.java`
**Class:** `SessionReportSearchForm extends ActionForm`
**Annotations:** `@Data` (Lombok), `@EqualsAndHashCode(callSuper = false)`

**Fields:**
| Field | Type | Line | Notes |
|-------|------|------|-------|
| `serialVersionUID` | `long` (static final) | 15 | `-8378135874225584484L` |
| `vehicle_id` | `Long` | 17 | Lombok generates getter/setter |
| `driver_id` | `Long` | 18 | Lombok generates getter/setter |
| `start_date` | `String` | 19 | Lombok generates getter/setter |
| `end_date` | `String` | 20 | Lombok generates getter/setter |
| `timezone` | `String` | 21 | Lombok generates getter/setter |

**Methods (explicitly declared):**
| Method signature | Lines | Notes |
|-----------------|-------|-------|
| `getSessionReportFilter(String dateFormat)` | 23–30 | builds and returns a `SessionFilterBean` via its builder; applies null/zero-check for `vehicle_id` (line 25) and `driver_id` (line 26); passes `start_date` and `end_date` through `DateUtil.stringToUTCDate()` with null-guard; applies `StringUtils.isBlank()` guard on `timezone` |

**Lombok-generated methods (not explicitly declared, but present at compile time):**
- `getVehicle_id()`, `setVehicle_id(Long)`, `getDriver_id()`, `setDriver_id(Long)`, `getStart_date()`, `setStart_date(String)`, `getEnd_date()`, `setEnd_date(String)`, `getTimezone()`, `setTimezone(String)`, `equals(Object)`, `hashCode()`, `toString()`

**Behavioural notes:**
- The `vehicle_id == 0` comparison on line 25 uses auto-unboxing; if `vehicle_id` were `null` this would NPE — however the null-check short-circuits it safely via `||`.
- Same pattern for `driver_id` on line 26.
- `DateUtil.stringToUTCDate()` behaviour (e.g., for invalid date strings) is not guarded in this form; error handling is delegated entirely to that utility.
- `@EqualsAndHashCode(callSuper = false)` means the superclass (`ActionForm`) fields are excluded from equality — this may be intentional but is worth noting.

---

## Grep results — test directory coverage

| Class | Pattern searched | Matches found |
|-------|-----------------|---------------|
| `ResetPassActionForm` | `ResetPassActionForm` | **0** |
| `SearchActionForm` | `SearchActionForm` | **0** |
| `SessionReportSearchForm` | `SessionReportSearchForm` | **0** |

**No test class references any of the three audited source classes.**

---

## Findings

### ResetPassActionForm

**A39-1 | Severity: CRITICAL | ResetPassActionForm — zero test coverage: no test class exists**
`ResetPassActionForm` has no corresponding test file anywhere under `src/test/java/`. No method is exercised by any automated test.

**A39-2 | Severity: CRITICAL | ResetPassActionForm.validate() — NullPointerException when `name` is null**
Line 49: `name.equalsIgnoreCase("")` is called without a null-guard. The field is initialised to `null` (line 16) and there is no `reset()` override that initialises it to `""`. Invoking `validate()` before calling `setName()` will throw `NullPointerException` at runtime. No test exercises or catches this defect.

**A39-3 | Severity: CRITICAL | ResetPassActionForm.validate() — NullPointerException when `email` is null**
Line 54: `email.equalsIgnoreCase("")` carries the same null-dereference risk as `name`. The field defaults to `null` (line 13). No test exercises or catches this defect.

**A39-4 | Severity: HIGH | ResetPassActionForm.validate() — `question` and `answer` fields are never validated**
The form collects a security question (`question`, line 14) and answer (`answer`, line 15), but `validate()` applies no checks to either field. A user could submit blank/null values with no error returned. No test documents this intentional or accidental omission.

**A39-5 | Severity: MEDIUM | ResetPassActionForm — getters/setters for `question` and `answer` are untested**
Accessors at lines 24–35 have no coverage.

---

### SearchActionForm

**A39-6 | Severity: CRITICAL | SearchActionForm — zero test coverage: no test class exists**
`SearchActionForm` has no corresponding test file anywhere under `src/test/java/`. No method is exercised by any automated test.

**A39-7 | Severity: CRITICAL | SearchActionForm constructor — live DAO call makes unit testing impossible without infrastructure**
The constructor (lines 23–27) calls `UnitDAO.getInstance().getAllUnitAttachment()`, a real database call, at construction time. Any unit test that instantiates `SearchActionForm` will require a live database or a static mock of `UnitDAO`. No test exercises this, and no mocking strategy is in place.

**A39-8 | Severity: CRITICAL | SearchActionForm.validate() — NullPointerException when `fname` is null**
Line 66: `fname.equalsIgnoreCase("")` is called without a null-guard. `fname` is initialised to `null` (line 18). Although `reset()` sets `fname = ""`, `reset()` is only called by the Struts framework between requests; a caller that never invokes `reset()` will hit NPE. No test exercises or catches this.

**A39-9 | Severity: CRITICAL | SearchActionForm.validate() — NullPointerException when `veh_id` is null**
Line 70: `veh_id.equalsIgnoreCase("")` has the same null-dereference risk. `veh_id` is initialised to `null` (line 19) and is never reset by `reset()` (line 52–54 only resets `fname`). No test exercises or catches this.

**A39-10 | Severity: HIGH | SearchActionForm.reset() — incomplete reset: `veh_id` and `attachment` are not reset**
Lines 52–54: `reset()` only assigns `fname = ""`, leaving `veh_id` and `attachment` as `null`. On subsequent requests the old (null or stale) values persist. No test validates the post-reset state of all fields.

**A39-11 | Severity: MEDIUM | SearchActionForm — raw `ArrayList` use (no generic type parameter)**
Line 21: `private ArrayList arrAttachment = new ArrayList()` uses a raw type, bypassing compile-time type safety. No test validates the type or contents of the list returned by `getArrAttachment()`.

---

### SessionReportSearchForm

**A39-12 | Severity: CRITICAL | SessionReportSearchForm — zero test coverage: no test class exists**
`SessionReportSearchForm` has no corresponding test file anywhere under `src/test/java/`. No method is exercised by any automated test.

**A39-13 | Severity: HIGH | SessionReportSearchForm.getSessionReportFilter() — no test for vehicle_id == 0 boundary (maps to null)**
Line 25: `vehicle_id == 0` causes the filter to treat vehicle ID zero as "not specified" (null). There is no test verifying this boundary, confirming the zero-exclusion is intentional, or ensuring positive/negative IDs pass through correctly.

**A39-14 | Severity: HIGH | SessionReportSearchForm.getSessionReportFilter() — no test for driver_id == 0 boundary (maps to null)**
Line 26: Same zero-maps-to-null logic applies to `driver_id`. Untested.

**A39-15 | Severity: HIGH | SessionReportSearchForm.getSessionReportFilter() — no test for invalid date string handling**
Lines 27–28: `DateUtil.stringToUTCDate(this.start_date, dateFormat)` and the equivalent for `end_date` are called with no guard for malformed date strings. Behaviour on invalid input (exception, null return, garbage date) is entirely untested.

**A39-16 | Severity: MEDIUM | SessionReportSearchForm.getSessionReportFilter() — no test for blank/null timezone mapping to null**
Line 29: `StringUtils.isBlank(this.timezone) ? null : this.timezone` — the blank-becomes-null contract has no test verifying it for all relevant inputs (null, `""`, `"   "`, valid zone string).

**A39-17 | Severity: MEDIUM | SessionReportSearchForm.getSessionReportFilter() — no test for fully null/empty form (all-null input)**
No test exercises the case where all five fields are null (default construction), which is the most common pre-population state.

**A39-18 | Severity: LOW | SessionReportSearchForm — Lombok-generated equals/hashCode excluded from callSuper**
`@EqualsAndHashCode(callSuper = false)` means `ActionForm` superclass fields are excluded from equality comparisons. No test documents or validates the expected equality semantics.

---

## Summary table

| Finding | Class | Severity | Short description |
|---------|-------|----------|-------------------|
| A39-1 | ResetPassActionForm | CRITICAL | No test class exists |
| A39-2 | ResetPassActionForm | CRITICAL | NPE in validate() when name is null |
| A39-3 | ResetPassActionForm | CRITICAL | NPE in validate() when email is null |
| A39-4 | ResetPassActionForm | HIGH | question and answer fields never validated |
| A39-5 | ResetPassActionForm | MEDIUM | question/answer getters/setters untested |
| A39-6 | SearchActionForm | CRITICAL | No test class exists |
| A39-7 | SearchActionForm | CRITICAL | Constructor makes live DAO call; unit testing requires real DB |
| A39-8 | SearchActionForm | CRITICAL | NPE in validate() when fname is null |
| A39-9 | SearchActionForm | CRITICAL | NPE in validate() when veh_id is null |
| A39-10 | SearchActionForm | HIGH | reset() does not reset veh_id or attachment |
| A39-11 | SearchActionForm | MEDIUM | Raw ArrayList with no generic type |
| A39-12 | SessionReportSearchForm | CRITICAL | No test class exists |
| A39-13 | SessionReportSearchForm | HIGH | vehicle_id == 0 boundary untested |
| A39-14 | SessionReportSearchForm | HIGH | driver_id == 0 boundary untested |
| A39-15 | SessionReportSearchForm | HIGH | Invalid date string behaviour untested |
| A39-16 | SessionReportSearchForm | MEDIUM | Blank/null timezone mapping untested |
| A39-17 | SessionReportSearchForm | MEDIUM | All-null form construction untested |
| A39-18 | SessionReportSearchForm | LOW | callSuper=false on equals/hashCode undocumented by tests |

**Total findings: 18**
- CRITICAL: 8
- HIGH: 5
- MEDIUM: 4
- LOW: 1
