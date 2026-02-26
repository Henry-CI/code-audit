# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A30
**Files audited:**
- `src/main/java/com/actionform/AdminDriverEditForm.java`
- `src/main/java/com/actionform/AdminFleetcheckActionForm.java`
- `src/main/java/com/actionform/AdminFleetcheckDeleteActionForm.java`

**Test directory searched:** `src/test/java/`

---

## 1. Reading Evidence

### 1.1 AdminDriverEditForm

**Class:** `AdminDriverEditForm` (extends `ActionForm`)
**Package:** `com.actionform`
**Lombok annotations:** `@Getter`, `@Setter`, `@NoArgsConstructor`

**Fields (all at class level, lines 28-49):**

| Line | Field | Type | Initial value |
|------|-------|------|---------------|
| 28 | `id` | `Long` | `null` |
| 29 | `first_name` | `String` | `null` |
| 30 | `last_name` | `String` | `null` |
| 31 | `licence_number` | `String` | `null` |
| 32 | `expiry_date` | `String` | `null` |
| 33 | `security_number` | `String` | `null` |
| 34 | `address` | `String` | `null` |
| 35 | `app_access` | `String` | `null` |
| 36 | `mobile` | `String` | `null` |
| 37 | `email_addr` | `String` | `null` |
| 38 | `redImpactAlert` | `String` | `null` |
| 39 | `redImpactSMSAlert` | `String` | `null` |
| 40 | `driverDenyAlert` | `String` | `null` |
| 41 | `pass` | `String` | `null` |
| 42 | `cpass` | `String` | `null` |
| 43 | `location` | `String` | `null` |
| 44 | `department` | `String` | `null` |
| 45 | `op_code` | `String` | `null` |
| 46 | `pass_hash` | `String` | `null` |
| 47 | `cognito_username` | `String` | `null` |
| 49 | `vehicles` | `List<DriverUnitBean>` | `new ArrayList<>()` |

**Methods:**

| Line | Method | Visibility | Notes |
|------|--------|------------|-------|
| 51 | `getVehicle(int index)` | `public` | Lazy-grows `vehicles` list to accommodate `index`, returns element |
| 61 | `validate(ActionMapping mapping, HttpServletRequest request)` | `public` | Overrides Struts `ActionForm.validate()`; branches on `op_code` |
| 127 | `isLicenceNumberInvalid(String licenceNumber)` | `private` | Returns `true` if length > 16 or contains special characters |
| 133 | `containSpecialCharatcter(String value)` | `private` | Regex `[^a-z0-9]` (case-insensitive); returns `true` if match found |
| 139 | `getDriverVehicle(String sessCompId)` | `public` | Builds and returns `DriverVehicleBean`; asserts `sessCompId` non-blank |
| 149 | `getLicenseBean()` | `public` | Builds and returns `LicenceBean` from current field state |

**Lombok-generated methods (not explicit in source):**
- Getters and setters for all 21 fields listed above (via `@Getter` / `@Setter`)
- No-arg constructor (via `@NoArgsConstructor`)

---

### 1.2 AdminFleetcheckActionForm

**Class:** `AdminFleetcheckActionForm` (extends `ActionForm`)
**Package:** `com.actionform`
**Lombok annotations:** `@Getter`, `@Setter`

**Fields (lines 20-28):**

| Line | Field | Type | Initial value |
|------|-------|------|---------------|
| 20 | `action` | `String` | `null` |
| 21 | `id` | `String` | `null` |
| 22 | `manu_id` | `String` | `null` |
| 23 | `type_id` | `String` | `null` |
| 24 | `fuel_type_id` | `String` | `null` |
| 25 | `attachment_id` | `String` | `null` |
| 26 | `arrAdminUnitType` | `ArrayList` (raw) | `new ArrayList()` |
| 27 | `arrAdminUnitFuelType` | `ArrayList` (raw) | `new ArrayList()` |
| 28 | `arrAttachment` | `ArrayList` (raw) | `new ArrayList()` |

**Methods:**

| Line | Method | Visibility | Notes |
|------|--------|------------|-------|
| 30 | `AdminFleetcheckActionForm()` | `public` | Constructor; calls `setArrAdminUnitType()`, `setArrAdminUnitFuelType()`, `setArrAttachment()`; throws `Exception` |
| 37 | `setArrAdminUnitType()` | `public` | Calls `UnitDAO.getInstance().getAllUnitType()`; throws `Exception` |
| 41 | `setArrAdminUnitFuelType()` | `public` | Calls `UnitDAO.getInstance().getAllUnitFuelType()`; throws `Exception` |
| 45 | `setArrAttachment()` | `public` | Calls `UnitDAO.getInstance().getAllUnitAttachment()`; throws `Exception` |
| 49 | `validate(ActionMapping mapping, HttpServletRequest request)` | `public` | Validates `manu_id`, `type_id`, `fuel_type_id` non-empty; returns `ActionErrors` |

---

### 1.3 AdminFleetcheckDeleteActionForm

**Class:** `AdminFleetcheckDeleteActionForm` (extends `ValidateIdExistsAbstractActionForm`)
**Package:** `com.actionform`

**Fields:** None declared directly. Inherits `id` (String, line 16 of parent).

**Methods:** None declared directly. Inherits the following from `ValidateIdExistsAbstractActionForm`:

| Line (parent) | Method | Visibility | Notes |
|---------------|--------|------------|-------|
| 19 | `validate(ActionMapping mapping, HttpServletRequest request)` | `public` | Validates `id` non-empty via `StringUtils.isEmpty` |

**Lombok-generated (inherited):** Getter/setter for `id` (via `@Getter`/`@Setter` on parent).

---

## 2. Test Directory Search Results

Test files found under `src/test/java/`:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

Grep results for each class name:

| Class name searched | Matches in test directory |
|--------------------|--------------------------|
| `AdminDriverEditForm` | **0 matches** |
| `AdminFleetcheckActionForm` | **0 matches** |
| `AdminFleetcheckDeleteActionForm` | **0 matches** |
| `ValidateIdExistsAbstractActionForm` | **0 matches** |

None of the three audited classes (or their shared abstract parent) are referenced anywhere in the test suite.

---

## 3. Coverage Gaps and Findings

### AdminDriverEditForm

---

**A30-1 | Severity: CRITICAL | AdminDriverEditForm has zero test coverage**

No test class exists for `AdminDriverEditForm`. The class contains complex validation and business logic across six explicit methods. None are tested.

---

**A30-2 | Severity: CRITICAL | validate() op_code="edit_general" branch is untested**

`validate()` lines 64-103: when `op_code` equals `"edit_general"` or `"edit_general_user"`, first name and last name empty checks fire, password mismatch check fires, and password masking logic (`"******"` sentinel) resets `pass`, `cpass`, and `pass_hash` to empty strings. None of these branches have any test coverage.

---

**A30-3 | Severity: CRITICAL | validate() op_code="edit_licence" branch is untested**

`validate()` lines 105-122: when `op_code` equals `"edit_licence"`, the licence number is validated via `isLicenceNumberInvalid()` and a `LicenceBean` is constructed and placed on the request. No tests exist for this path.

---

**A30-4 | Severity: HIGH | isLicenceNumberInvalid() private method logic is untested**

Lines 127-131: the method returns `true` if `licenceNumber.length() > 16` OR if it contains special characters. There are no tests verifying the boundary at 16 characters (valid at 16, invalid at 17), nor tests for alphanumeric-only vs. special-character-containing strings. Although private, it is the sole guard for licence number format and is reachable via `validate()`.

---

**A30-5 | Severity: HIGH | containSpecialCharatcter() private method logic is untested**

Lines 133-137: the regex `[^a-z0-9]` (case-insensitive) is applied to detect non-alphanumeric characters. No tests verify that spaces, hyphens, dots, underscores, or unicode characters are correctly flagged, nor that purely alphanumeric strings pass. Note also that the method name contains a typo ("Charatcter") that could cause confusion; this is an additional code-quality issue but is not a test gap in itself.

---

**A30-6 | Severity: HIGH | getVehicle() lazy-growth logic is untested**

Lines 51-59: if `index` is at or beyond the current list size, new `DriverUnitBean` instances are appended until the list is large enough. No tests verify: (a) normal in-bounds retrieval, (b) exact boundary access, or (c) growth by multiple slots when a large index is provided.

---

**A30-7 | Severity: HIGH | getDriverVehicle() is untested**

Lines 139-147: builds and returns a `DriverVehicleBean` from form state. Includes an `assert` precondition on `sessCompId` (only active when assertions are enabled at JVM startup). No tests verify the happy path, the assert guard, the `Long.valueOf()` conversion, or that `vehicles` are correctly forwarded into the bean.

---

**A30-8 | Severity: HIGH | getLicenseBean() is untested**

Lines 149-156: builds and returns a `LicenceBean` from the form's field values. No tests verify correct field mapping.

---

**A30-9 | Severity: MEDIUM | Password masking sentinel "******" behaviour is untested**

Lines 80-85 inside `validate()`: when `pass` equals `"******"` (case-insensitive), `pass`, `cpass`, and `pass_hash` are cleared. This is security-relevant behaviour. A regression in this logic could cause a hashed password to be stored or displayed. No test documents or guards this contract.

---

**A30-10 | Severity: MEDIUM | Password mismatch check executes before masking check, creating ordering dependency that is untested**

Lines 75-85: `!pass.equalsIgnoreCase(cpass)` is evaluated before the `"******"` sentinel check. If `pass` is `"******"` and `cpass` is also `"******"`, no error is added for mismatch and both are then cleared. If they differ, an error is added and then they are still cleared. The resulting combination of error state and cleared fields is an untested edge case.

---

**A30-11 | Severity: MEDIUM | NullPointerException risk in validate() is untested**

`op_code.equalsIgnoreCase(...)` at line 64 will throw `NullPointerException` if `op_code` is `null` (its default initialised value). Similarly, `first_name.equalsIgnoreCase("")` (line 65), `last_name.equalsIgnoreCase("")` (line 70), and `pass.equalsIgnoreCase(cpass)` (line 75) all dereference fields that default to `null`. No tests verify safe handling of null inputs, and there is no null-guard in the code.

---

**A30-12 | Severity: MEDIUM | NullPointerException risk in isLicenceNumberInvalid() is untested**

Line 128: `licenceNumber.length()` will throw `NullPointerException` if `licence_number` is `null`. No null-guard exists and no test verifies the behaviour when the field is unset.

---

**A30-13 | Severity: LOW | Fields redImpactAlert, redImpactSMSAlert, driverDenyAlert are declared but never used in any logic**

Lines 38-40: three fields are declared and have Lombok-generated getters/setters but are not referenced in any method within the class. No test documents their expected role or verifies that they are correctly transferred to any downstream object.

---

### AdminFleetcheckActionForm

---

**A30-14 | Severity: CRITICAL | AdminFleetcheckActionForm has zero test coverage**

No test class exists for `AdminFleetcheckActionForm`. The class has a DAO-calling constructor and a non-trivial `validate()` method, none of which are tested.

---

**A30-15 | Severity: HIGH | Constructor throws checked Exception making it untestable without DAO infrastructure**

Lines 30-35: the constructor calls `UnitDAO.getInstance()` three times. Without mocking or stubbing the DAO singleton, the constructor cannot be instantiated in a unit test. No tests exist and no test infrastructure (mocks, stubs, or integration test setup) is present.

---

**A30-16 | Severity: HIGH | validate() missing manu_id, type_id, fuel_type_id branches are untested**

Lines 49-68: three separate `StringUtils.isEmpty` checks each produce distinct `ActionErrors` entries. No tests verify: (a) all three fields valid produces no errors, (b) each field individually empty produces exactly one error, or (c) all three fields empty produces exactly three errors.

---

**A30-17 | Severity: HIGH | setArrAdminUnitType(), setArrAdminUnitFuelType(), setArrAttachment() public mutators are untested**

Lines 37-47: these three methods call DAO singletons directly. They are individually callable (public), but no test verifies their behaviour in isolation or with stubbed DAO responses.

---

**A30-18 | Severity: MEDIUM | Raw ArrayList fields (no generic type) are untested**

Lines 26-28: `arrAdminUnitType`, `arrAdminUnitFuelType`, and `arrAttachment` are raw `ArrayList` (unchecked). No test verifies that the contents populated by the DAO calls are of the expected type or that the getters return the correctly populated lists.

---

**A30-19 | Severity: MEDIUM | attachment_id field is declared and Lombok-accessible but not validated in validate()**

Line 25: `attachment_id` has a getter and setter via `@Getter`/`@Setter` but is never checked in `validate()`. No test documents whether this is intentional or an oversight.

---

### AdminFleetcheckDeleteActionForm

---

**A30-20 | Severity: CRITICAL | AdminFleetcheckDeleteActionForm has zero test coverage**

No test class exists for `AdminFleetcheckDeleteActionForm`. The class itself is a body-less subclass, but its inherited validate logic is material and untested in this subclass context.

---

**A30-21 | Severity: HIGH | Inherited validate() from ValidateIdExistsAbstractActionForm is untested for this subclass**

`AdminFleetcheckDeleteActionForm` inherits `validate()` from `ValidateIdExistsAbstractActionForm` (parent lines 19-27), which checks `StringUtils.isEmpty(this.id)` and adds an `"error.id"` message. No test verifies that instantiating `AdminFleetcheckDeleteActionForm` and calling `validate()` with a null or empty `id` produces the expected error, nor that a valid `id` produces none.

---

**A30-22 | Severity: MEDIUM | ValidateIdExistsAbstractActionForm itself has zero test coverage**

`ValidateIdExistsAbstractActionForm` (the abstract parent shared by `AdminFleetcheckDeleteActionForm` and potentially other subclasses) has no tests at all. Its `validate()` method is non-trivial and its correctness cannot be confirmed.

---

## 4. Summary Table

| Finding | Severity | Class | Subject |
|---------|----------|-------|---------|
| A30-1 | CRITICAL | AdminDriverEditForm | No test class exists |
| A30-2 | CRITICAL | AdminDriverEditForm | `validate()` edit_general/edit_general_user branch untested |
| A30-3 | CRITICAL | AdminDriverEditForm | `validate()` edit_licence branch untested |
| A30-4 | HIGH | AdminDriverEditForm | `isLicenceNumberInvalid()` logic untested |
| A30-5 | HIGH | AdminDriverEditForm | `containSpecialCharatcter()` regex untested |
| A30-6 | HIGH | AdminDriverEditForm | `getVehicle()` lazy-growth logic untested |
| A30-7 | HIGH | AdminDriverEditForm | `getDriverVehicle()` untested |
| A30-8 | HIGH | AdminDriverEditForm | `getLicenseBean()` untested |
| A30-9 | MEDIUM | AdminDriverEditForm | Password masking sentinel untested |
| A30-10 | MEDIUM | AdminDriverEditForm | Password mismatch/masking ordering edge case untested |
| A30-11 | MEDIUM | AdminDriverEditForm | NPE risk on null fields in `validate()` untested |
| A30-12 | MEDIUM | AdminDriverEditForm | NPE risk on null `licence_number` untested |
| A30-13 | LOW | AdminDriverEditForm | Three declared fields unused in logic, not documented by tests |
| A30-14 | CRITICAL | AdminFleetcheckActionForm | No test class exists |
| A30-15 | HIGH | AdminFleetcheckActionForm | DAO-coupled constructor untestable without mocking |
| A30-16 | HIGH | AdminFleetcheckActionForm | `validate()` field-empty branches untested |
| A30-17 | HIGH | AdminFleetcheckActionForm | DAO-calling public setter methods untested |
| A30-18 | MEDIUM | AdminFleetcheckActionForm | Raw ArrayList fields untested |
| A30-19 | MEDIUM | AdminFleetcheckActionForm | `attachment_id` not validated; intent undocumented |
| A30-20 | CRITICAL | AdminFleetcheckDeleteActionForm | No test class exists |
| A30-21 | HIGH | AdminFleetcheckDeleteActionForm | Inherited `validate()` untested for this subclass |
| A30-22 | MEDIUM | ValidateIdExistsAbstractActionForm | Abstract parent has zero test coverage |

**Total findings: 22**
**CRITICAL: 4 | HIGH: 9 | MEDIUM: 7 | LOW: 1 | INFO: 0**
