# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A33
**Date:** 2026-02-26
**Scope:** AdminSettingsActionForm, AdminTrainingsActionForm, AdminUnitAccessForm

---

## 1. Reading Evidence

### 1.1 AdminSettingsActionForm
**File:** `src/main/java/com/actionform/AdminSettingsActionForm.java`
**Class:** `AdminSettingsActionForm extends ActionForm`
**Annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Initial Value | Line |
|---|---|---|---|
| `serialVersionUID` | `static final long` | `7884549462560104854L` | 23 |
| `id` | `String` | `null` | 24 |
| `dateFormat` | `String` | `null` | 25 |
| `maxSessionLength` | `Integer` | `null` | 26 |
| `action` | `String` | `null` | 27 |
| `timezone` | `String` | `null` | 28 |
| `redImpactAlert` | `String` | `null` | 29 |
| `redImpactSMSAlert` | `String` | `null` | 30 |
| `driverDenyAlert` | `String` | `null` | 31 |

**Methods:**

| Method | Signature | Lines |
|---|---|---|
| `validate` | `ActionErrors validate(ActionMapping mapping, HttpServletRequest request)` | 33-52 |

**Lombok-generated methods (implicit via @Getter/@Setter/@NoArgsConstructor):**
- `getId()`, `setId(String)`
- `getDateFormat()`, `setDateFormat(String)`
- `getMaxSessionLength()`, `setMaxSessionLength(Integer)`
- `getAction()`, `setAction(String)`
- `getTimezone()`, `setTimezone(String)`
- `getRedImpactAlert()`, `setRedImpactAlert(String)`
- `getRedImpactSMSAlert()`, `setRedImpactSMSAlert(String)`
- `getDriverDenyAlert()`, `setDriverDenyAlert(String)`
- `AdminSettingsActionForm()` (no-arg constructor)

**Validate method branch inventory (lines 33-52):**
- Branch 1: `dateFormat == null` → adds `error.date_format` (line 37)
- Branch 2: `dateFormat.equals("")` → adds `error.date_format` (line 37)
- Branch 3: `timezone == null` → adds `error.timezone` (line 42)
- Branch 4: `timezone.equals("")` → adds `error.timezone` (line 42)
- Branch 5: `timezone.equals("0")` → adds `error.timezone` (line 42)
- Branch 6: `maxSessionLength == null` → adds `error.max_session_length` (line 46)
- Branch 7 (implicit): all fields valid → returns empty `ActionErrors` (line 51)

---

### 1.2 AdminTrainingsActionForm
**File:** `src/main/java/com/actionform/AdminTrainingsActionForm.java`
**Class:** `AdminTrainingsActionForm extends ActionForm`
**Annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Initial Value | Line |
|---|---|---|---|
| `action` | `String` | `null` | 14 |
| `driver` | `Long` | `null` | 16 |
| `manufacturer` | `Long` | `null` | 17 |
| `type` | `Long` | `null` | 18 |
| `fuelType` | `Long` | `null` | 19 |
| `trainingDate` | `String` | `null` | 20 |
| `expirationDate` | `String` | `null` | 21 |
| `training` | `Long` | `null` | 23 |

**Methods:**
None explicitly declared. All access is via Lombok-generated methods:
- `getAction()`, `setAction(String)`
- `getDriver()`, `setDriver(Long)`
- `getManufacturer()`, `setManufacturer(Long)`
- `getType()`, `setType(Long)`
- `getFuelType()`, `setFuelType(Long)`
- `getTrainingDate()`, `setTrainingDate(String)`
- `getExpirationDate()`, `setExpirationDate(String)`
- `getTraining()`, `setTraining(Long)`
- `AdminTrainingsActionForm()` (no-arg constructor)

**Note:** No `validate()` override — Struts will invoke the parent `ActionForm.validate()` which returns `null` by default. No explicit validation logic exists for any field.

---

### 1.3 AdminUnitAccessForm
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java`
**Class:** `AdminUnitAccessForm extends ActionForm`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Initial Value | Line |
|---|---|---|---|
| `id` | `String` | (unset) | 25 |
| `accessible` | `boolean` | `false` (Java default) | 26 |
| `access_type` | `String` | (unset) | 27 |
| `keypad_reader` | `String` | (unset) | 28 |
| `facility_code` | `String` | (unset) | 29 |
| `access_id` | `String` | (unset) | 30 |

**Methods:**

| Method | Signature | Lines |
|---|---|---|
| `validate` | `ActionErrors validate(ActionMapping mapping, HttpServletRequest request)` | 33-37 |
| `getUnit` | `UnitBean getUnit(String compId)` | 39-48 |
| `setUnit` | `void setUnit(UnitBean unitBean)` | 51-60 |

**Lombok-generated methods (implicit via @Data/@NoArgsConstructor):**
- `getId()`, `setId(String)`
- `isAccessible()`, `setAccessible(boolean)`
- `getAccess_type()`, `setAccess_type(String)`
- `getKeypad_reader()`, `setKeypad_reader(String)`
- `getFacility_code()`, `setFacility_code(String)`
- `getAccess_id()`, `setAccess_id(String)`
- `equals(Object)`, `hashCode()`, `toString()`
- `AdminUnitAccessForm()` (no-arg constructor)

**getUnit method branch inventory (lines 39-48):**
- Branch 1: `StringUtils.isBlank(id)` → `id` mapped as `null` (line 41)
- Branch 2: `StringUtils.isNotBlank(id)` → `id` mapped as value (line 41)
- Branch 3: `StringUtils.isNotBlank(keypad_reader)` → `KeypadReaderModel.valueOf(keypad_reader)` (line 46)
- Branch 4: `keypad_reader` blank/null → `keypad_reader` mapped as `null` (line 46)

**setUnit method branch inventory (lines 51-60):**
- Branch 1: `unitBean.getKeypad_reader() != null` → sets `this.keypad_reader = unitBean.getKeypad_reader().name()` (lines 56-58)
- Branch 2: `unitBean.getKeypad_reader() == null` → `this.keypad_reader` left unchanged (null/previous value)

---

## 2. Test Directory Search Results

**Test directory:** `src/test/java/`

**Existing test files:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep results for class names in test directory:**

| Class Name | Files Found |
|---|---|
| `AdminSettingsActionForm` | None |
| `AdminTrainingsActionForm` | None |
| `AdminUnitAccessForm` | None |

**Grep results for package `com.actionform` in test directory:** None found.

**Conclusion:** Zero test coverage exists for all three audited classes.

---

## 3. Coverage Gap Findings

---

### A33-1 | Severity: CRITICAL | AdminSettingsActionForm — No test class exists

No test class for `AdminSettingsActionForm` was found anywhere in `src/test/java/`. The class contains a non-trivial `validate()` method with six distinct conditional branches covering three separate fields (`dateFormat`, `timezone`, `maxSessionLength`). All branches, all Lombok-generated accessors, and the no-arg constructor are completely untested.

---

### A33-2 | Severity: CRITICAL | AdminTrainingsActionForm — No test class exists

No test class for `AdminTrainingsActionForm` was found anywhere in `src/test/java/`. The class contains eight fields with Lombok-generated accessors and a no-arg constructor. No `validate()` override is present; the absence of validation for business-critical fields (driver, manufacturer, type, fuelType, trainingDate, expirationDate, training) is itself a behavioural gap that is entirely untested.

---

### A33-3 | Severity: CRITICAL | AdminUnitAccessForm — No test class exists

No test class for `AdminUnitAccessForm` was found anywhere in `src/test/java/`. The class contains two non-trivial hand-written methods (`getUnit` and `setUnit`) with multiple conditional branches, as well as a stub `validate()`. All of these are completely untested.

---

### A33-4 | Severity: HIGH | AdminSettingsActionForm.validate — all six conditional branches untested

The `validate()` method (lines 33-52) has the following untested branches:

| Branch | Condition | Expected Outcome |
|---|---|---|
| 1 | `dateFormat == null` | `error.date_format` added |
| 2 | `dateFormat.equals("")` | `error.date_format` added |
| 3 | `timezone == null` | `error.timezone` added |
| 4 | `timezone.equals("")` | `error.timezone` added |
| 5 | `timezone.equals("0")` | `error.timezone` added |
| 6 | `maxSessionLength == null` | `error.max_session_length` added |
| 7 (happy path) | all fields valid | empty `ActionErrors` returned |

No test exercises any of these branches.

---

### A33-5 | Severity: HIGH | AdminUnitAccessForm.getUnit — all four conditional branches untested

The `getUnit(String compId)` method (lines 39-48) has the following untested branches:

| Branch | Condition | Expected Outcome |
|---|---|---|
| 1 | `StringUtils.isBlank(id)` | `id` field of `UnitBean` is `null` |
| 2 | `id` is non-blank | `id` field of `UnitBean` equals `id` value |
| 3 | `StringUtils.isNotBlank(keypad_reader)` | `KeypadReaderModel.valueOf(keypad_reader)` assigned |
| 4 | `keypad_reader` blank/null | `keypad_reader` field of `UnitBean` is `null` |

Additionally, passing an invalid enum string (e.g. `"INVALID"`) to `KeypadReaderModel.valueOf()` would throw `IllegalArgumentException`; no test validates this failure mode.

---

### A33-6 | Severity: HIGH | AdminUnitAccessForm.setUnit — conditional branch for null keypad_reader untested

The `setUnit(UnitBean unitBean)` method (lines 51-60) contains a branch at line 56 (`if (unitBean.getKeypad_reader() != null)`). Neither branch is tested:

- When `keypad_reader` is non-null, `this.keypad_reader` should be set to the enum's `.name()`.
- When `keypad_reader` is null, `this.keypad_reader` should remain at its prior value (typically null).

---

### A33-7 | Severity: HIGH | AdminUnitAccessForm.validate — stub returns empty errors with no field validation

The `validate()` method (lines 33-37) returns an empty `ActionErrors` unconditionally, performing no validation on any of the six form fields (`id`, `accessible`, `access_type`, `keypad_reader`, `facility_code`, `access_id`). This is a behavioural gap in addition to a test gap: malformed or missing values (e.g., an invalid `access_type` or `keypad_reader` string) will silently pass validation. No test asserts this behaviour or flags it as intentional.

---

### A33-8 | Severity: MEDIUM | AdminTrainingsActionForm — no validate() override; no field validation tested or documented

`AdminTrainingsActionForm` contains eight fields used in training record management (`driver`, `manufacturer`, `type`, `fuelType`, `trainingDate`, `expirationDate`, `training`, `action`) but declares no `validate()` override. The parent `ActionForm.validate()` returns null, meaning all input passes silently. There is no test confirming that this omission is intentional, nor any test exercising date fields (`trainingDate`, `expirationDate`) for format correctness.

---

### A33-9 | Severity: MEDIUM | AdminSettingsActionForm — fields redImpactAlert, redImpactSMSAlert, driverDenyAlert have no validate() coverage and no tests

Fields `redImpactAlert` (line 29), `redImpactSMSAlert` (line 30), and `driverDenyAlert` (line 31) are present in the form but are not validated in `validate()`. There is no test confirming whether this is intentional or an oversight. These fields likely represent alert email/SMS addresses where format validation (e.g. email format) would be expected.

---

### A33-10 | Severity: MEDIUM | AdminUnitAccessForm.getUnit — no test for invalid KeypadReaderModel enum value

At line 46, `UnitBean.KeypadReaderModel.valueOf(keypad_reader)` is called when `keypad_reader` is non-blank. If the form receives any string that is not one of `{ROSLARE, KERI, SMART, HID_ICLASS}`, `valueOf` will throw `IllegalArgumentException` at runtime. The `validate()` method performs no pre-validation of this field, and there is no test covering this failure path.

---

### A33-11 | Severity: LOW | AdminSettingsActionForm — Lombok-generated accessors (getters/setters) untested

All nine Lombok-generated getters and setters for `AdminSettingsActionForm` are untested. While Lombok itself is considered reliable, the expected field names, types, and null-initialisation behaviour are not verified by any test.

---

### A33-12 | Severity: LOW | AdminTrainingsActionForm — Lombok-generated accessors (getters/setters) untested

All eight Lombok-generated getter/setter pairs and the no-arg constructor for `AdminTrainingsActionForm` are untested. Field default values (all `null`) and type correctness (e.g., `Long` for `driver`, `manufacturer`) are unverified.

---

### A33-13 | Severity: LOW | AdminUnitAccessForm — Lombok @Data-generated equals/hashCode/toString untested

`@Data` generates `equals()`, `hashCode()`, and `toString()` for `AdminUnitAccessForm`. These are not exercised by any test, meaning field-equality semantics are unverified.

---

### A33-14 | Severity: INFO | No test infrastructure exists for com.actionform package

The `src/test/java/` directory contains only four test files, all targeting `com.calibration` and `com.util`. There is no test infrastructure (base class, mock configuration, Struts test harness) established for the `com.actionform` package. Any new tests will need to establish this foundation, including a Struts `ActionMapping` mock and `HttpServletRequest` mock for `validate()` testing.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A33-1 | CRITICAL | AdminSettingsActionForm | No test class exists |
| A33-2 | CRITICAL | AdminTrainingsActionForm | No test class exists |
| A33-3 | CRITICAL | AdminUnitAccessForm | No test class exists |
| A33-4 | HIGH | AdminSettingsActionForm | All 6 validate() branches untested |
| A33-5 | HIGH | AdminUnitAccessForm | All 4 getUnit() branches untested |
| A33-6 | HIGH | AdminUnitAccessForm | setUnit() null-keypad_reader branch untested |
| A33-7 | HIGH | AdminUnitAccessForm | validate() is a no-op stub; not tested or documented |
| A33-8 | MEDIUM | AdminTrainingsActionForm | No validate() override; no field validation tested |
| A33-9 | MEDIUM | AdminSettingsActionForm | redImpactAlert/redImpactSMSAlert/driverDenyAlert not validated or tested |
| A33-10 | MEDIUM | AdminUnitAccessForm | Invalid KeypadReaderModel enum value causes unhandled IllegalArgumentException |
| A33-11 | LOW | AdminSettingsActionForm | Lombok accessors untested |
| A33-12 | LOW | AdminTrainingsActionForm | Lombok accessors untested |
| A33-13 | LOW | AdminUnitAccessForm | Lombok @Data equals/hashCode/toString untested |
| A33-14 | INFO | All | No test infrastructure exists for com.actionform package |

**Overall coverage: 0% for all three audited classes.**
