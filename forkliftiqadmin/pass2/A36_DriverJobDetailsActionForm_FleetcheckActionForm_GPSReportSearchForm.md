# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A36
**Date:** 2026-02-26

## Source files audited

| # | File | Class |
|---|------|-------|
| 1 | `src/main/java/com/actionform/DriverJobDetailsActionForm.java` | `DriverJobDetailsActionForm` |
| 2 | `src/main/java/com/actionform/FleetcheckActionForm.java` | `FleetcheckActionForm` |
| 3 | `src/main/java/com/actionform/GPSReportSearchForm.java` | `GPSReportSearchForm` |

---

## Reading-evidence blocks

### 1. DriverJobDetailsActionForm

**File:** `src/main/java/com/actionform/DriverJobDetailsActionForm.java`
**Superclass:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`

**Fields (all private, declared lines 9-22):**

| Field | Type | Line |
|-------|------|------|
| `id` | `int` | 9 |
| `action` | `String` | 10 |
| `equipId` | `String` | 11 |
| `jobId` | `String` | 12 |
| `driverList` | `ArrayList` (raw) | 13 |
| `name` | `String` | 14 |
| `startTime` | `String` | 15 |
| `endTime` | `String` | 16 |
| `fromTime` | `String` | 17 |
| `toTime` | `String` | 18 |
| `instruct` | `String` | 19 |
| `jobTitle` | `String` | 20 |
| `description` | `String` | 21 |
| `driverId` | `String` | 22 |

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `getId` | `public int getId()` | 24-26 |
| `getAction` | `public String getAction()` | 27-29 |
| `getEquipId` | `public String getEquipId()` | 30-32 |
| `getJobId` | `public String getJobId()` | 33-35 |
| `getDriverList` | `public ArrayList getDriverList()` | 36-38 |
| `getName` | `public String getName()` | 39-41 |
| `getStartTime` | `public String getStartTime()` | 42-44 |
| `getEndTime` | `public String getEndTime()` | 45-47 |
| `getFromTime` | `public String getFromTime()` | 48-50 |
| `getToTime` | `public String getToTime()` | 51-53 |
| `getInstruct` | `public String getInstruct()` | 54-56 |
| `setId` | `public void setId(int id)` | 57-59 |
| `setAction` | `public void setAction(String action)` | 60-62 |
| `setEquipId` | `public void setEquipId(String equipId)` | 63-65 |
| `setJobId` | `public void setJobId(String jobId)` | 66-68 |
| `setDriverList` | `public void setDriverList(ArrayList driverList)` | 69-71 |
| `setName` | `public void setName(String name)` | 72-74 |
| `setStartTime` | `public void setStartTime(String startTime)` | 75-77 |
| `setEndTime` | `public void setEndTime(String endTime)` | 78-80 |
| `setFromTime` | `public void setFromTime(String fromTime)` | 81-83 |
| `setToTime` | `public void setToTime(String toTime)` | 84-86 |
| `setInstruct` | `public void setInstruct(String instruct)` | 87-89 |
| `getJobTitle` | `public String getJobTitle()` | 90-92 |
| `getDescription` | `public String getDescription()` | 93-95 |
| `setJobTitle` | `public void setJobTitle(String jobTitle)` | 96-98 |
| `setDescription` | `public void setDescription(String description)` | 99-101 |
| `getDriverId` | `public String getDriverId()` | 102-104 |
| `setDriverId` | `public void setDriverId(String driverId)` | 105-107 |

**Total methods:** 27 (no explicit constructor; raw-typed `ArrayList` used throughout)

---

### 2. FleetcheckActionForm

**File:** `src/main/java/com/actionform/FleetcheckActionForm.java`
**Superclass:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`
**Unused imports:** `ActionMessage`, `ActionErrors`, `ActionMapping`, `HttpServletRequest` (lines 3-8; no `validate` method is implemented)

**Fields (all private, declared lines 12-18):**

| Field | Type | Line | Default |
|-------|------|------|---------|
| `id` | `String[]` | 12 | `null` |
| `answer` | `String[]` | 13 | `null` |
| `faulty` | `String[]` | 14 | `null` |
| `comment` | `String` | 15 | `null` |
| `veh_id` | `String` | 16 | `null` |
| `att_id` | `String` | 17 | `null` |
| `hourmeter` | `String` | 18 | `null` |

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `getHourmeter` | `public String getHourmeter()` | 20-22 |
| `setHourmeter` | `public void setHourmeter(String hourmeter)` | 23-25 |
| `getId` | `public String[] getId()` | 26-28 |
| `setId` | `public void setId(String[] id)` | 29-31 |
| `getAnswer` | `public String[] getAnswer()` | 32-34 |
| `setAnswer` | `public void setAnswer(String[] answer)` | 35-37 |
| `getComment` | `public String getComment()` | 38-40 |
| `setComment` | `public void setComment(String comment)` | 41-43 |
| `getVeh_id` | `public String getVeh_id()` | 44-46 |
| `setVeh_id` | `public void setVeh_id(String veh_id)` | 47-49 |
| `getFaulty` | `public String[] getFaulty()` | 50-52 |
| `setFaulty` | `public void setFaulty(String[] faulty)` | 53-55 |
| `getAtt_id` | `public String getAtt_id()` | 56-58 |
| `setAtt_id` | `public void setAtt_id(String att_id)` | 59-61 |

**Total methods:** 14 (no explicit constructor, no `validate` override despite validation imports)

---

### 3. GPSReportSearchForm

**File:** `src/main/java/com/actionform/GPSReportSearchForm.java`
**Superclass:** `org.apache.struts.action.ActionForm`
**Package:** `com.actionform`
**Annotations:** `@Data` (Lombok — generates getters, setters, `toString`, `equals`, `hashCode` at compile time)

**Fields (all private, declared lines 18-25):**

| Field | Type | Line | Default |
|-------|------|------|---------|
| `manu_id` | `Long` | 18 | `null` |
| `type_id` | `Long` | 19 | `null` |
| `start_date` | `String` | 20 | `null` |
| `end_date` | `String` | 21 | `null` |
| `unitId` | `int` | 22 | `0` |
| `manufacturers` | `List<ManufactureBean>` | 24 | `new ArrayList<>()` |
| `unitTypes` | `List<UnitTypeBean>` | 25 | `new ArrayList<>()` |

**Methods (explicit):**

| Method | Signature | Lines |
|--------|-----------|-------|
| `GPSReportSearchForm` (constructor) | `public GPSReportSearchForm()` | 27-29 |
| `getGPSReportFilter` | `public GPSReportFilterBean getGPSReportFilter(String dateFormat)` | 30-37 |

**Lombok-generated methods (compile-time, not in source):**
`getManu_id`, `getType_id`, `getStart_date`, `getEnd_date`, `getUnitId`, `getManufacturers`, `getUnitTypes`,
`setManu_id`, `setType_id`, `setStart_date`, `setEnd_date`, `setUnitId`, `setManufacturers`, `setUnitTypes`,
`toString`, `equals`, `hashCode`

---

## Test-directory grep results

**Test directory searched:** `src/test/java/`

**Existing test files:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Class searched | Files found |
|----------------|-------------|
| `DriverJobDetailsActionForm` | **None** |
| `FleetcheckActionForm` | **None** |
| `GPSReportSearchForm` | **None** |

All three classes have **zero test coverage**.

---

## Findings

### A36-1 | Severity: CRITICAL | DriverJobDetailsActionForm — no test class exists

No test file references `DriverJobDetailsActionForm`. All 27 methods (14 setters, 13 getters) and the class itself are completely untested. The class carries 14 fields representing job scheduling data (driver assignment, equipment, time windows, instructions) that flow into Struts form processing. Any regression in setter/getter symmetry, field naming, or Struts binding would be undetected.

---

### A36-2 | Severity: CRITICAL | FleetcheckActionForm — no test class exists

No test file references `FleetcheckActionForm`. All 14 methods are completely untested. The class handles fleet inspection checklist data including array-typed fields (`id[]`, `answer[]`, `faulty[]`) representing multi-item form submissions. Array field round-trip behaviour (null initialisation, reference identity after set/get) is wholly untested.

---

### A36-3 | Severity: CRITICAL | GPSReportSearchForm — no test class exists

No test file references `GPSReportSearchForm`. The class contains a non-trivial business-logic method (`getGPSReportFilter`) with conditional branches that are entirely untested. See A36-4 and A36-5 for specific logic defects within this method.

---

### A36-4 | Severity: HIGH | GPSReportSearchForm.getGPSReportFilter — redundant tautological condition on unitId silently drops all non-zero unitId values

**Location:** `GPSReportSearchForm.java`, line 36

```java
.unitId(this.unitId == 0 || this.unitId == 0 ? null : this.unitId)
```

The condition `this.unitId == 0 || this.unitId == 0` is a copy-paste error: both operands are identical. The intended logic was almost certainly `this.unitId == 0` (singular), but regardless of intent the expression always evaluates to `true` when `unitId` is `0` and always `false` otherwise — which is functionally identical to a single `this.unitId == 0` check. While this produces the same branch outcome as the corrected single condition, the duplicate expression is dead code and indicates the filter was written by copying the `manu_id`/`type_id` pattern without proper adaptation. A test asserting that a non-zero `unitId` produces a non-null `unitId` in the returned filter bean would immediately expose this as the existing code actually does pass a non-zero `unitId` through correctly (the `false` branch returns `this.unitId`) — however, any future refactor that changes the `0` literal on the right side of only one operand would silently create a divergence. This must be confirmed by a test.

---

### A36-5 | Severity: HIGH | GPSReportSearchForm.getGPSReportFilter — no test coverage for any of the six conditional branches

**Location:** `GPSReportSearchForm.java`, lines 31-37

The method contains six independent conditional guards producing nullable vs. non-null values in the builder:

| Line | Guard | Branch: null | Branch: value |
|------|-------|-------------|---------------|
| 32 | `manu_id == null \|\| manu_id == 0` | → `null` | → `manu_id` |
| 33 | `type_id == null \|\| type_id == 0` | → `null` | → `type_id` |
| 34 | `StringUtils.isBlank(start_date)` | → `null` | → `DateUtil.stringToUTCDate(start_date, dateFormat)` |
| 35 | `StringUtils.isBlank(end_date)` | → `null` | → `DateUtil.stringToUTCDate(end_date, dateFormat)` |
| 36 | `unitId == 0 \|\| unitId == 0` (tautology) | → `null` | → `unitId` |

None of the 10 resulting paths (null or value for each of 5 fields) are covered by any test. This method also delegates to `DateUtil.stringToUTCDate` which performs timezone conversion; no integration-level assertion validates that a date string round-trips correctly through this form method.

---

### A36-6 | Severity: HIGH | GPSReportFilterBean builder discards unitId — silent data loss not caught by any test

**Location:** `GPSReportSearchForm.java` line 36; `GPSReportFilterBean.java` lines 14-17

The `GPSReportSearchForm.getGPSReportFilter` method passes `unitId` to `GPSReportFilterBean.builder().unitId(...)`, but the `GPSReportFilterBean` constructor (line 15-16 of `GPSReportFilterBean.java`) accepts `unitId` as a parameter yet passes only `startDate`, `endDate`, `manuId`, `typeId`, and a hardcoded empty string `""` to the `ReportFilterBean` superclass. The `unitId` parameter is accepted but never stored or forwarded — `ReportFilterBean` has no `unitId` field. The value is silently discarded. No test exists to detect this data-loss defect.

---

### A36-7 | Severity: MEDIUM | FleetcheckActionForm — unused validation imports indicate missing validate() override

**Location:** `FleetcheckActionForm.java`, lines 3-8

The class imports `ActionMessage`, `ActionErrors`, `ActionMapping`, and `HttpServletRequest` — the exact types required to implement `ActionForm.validate(ActionMapping, HttpServletRequest)`. No `validate` method is implemented. The `FleetcheckActionForm` processes fleet inspection answers including a `hourmeter` value (a numeric reading submitted as a String) that would benefit from server-side validation. The abandoned validation scaffolding means invalid data (e.g., non-numeric hourmeter, empty `veh_id`) is not rejected at the form layer. There are no tests to specify or enforce the expected validation behaviour.

---

### A36-8 | Severity: MEDIUM | DriverJobDetailsActionForm — raw ArrayList type without generics

**Location:** `DriverJobDetailsActionForm.java`, lines 13, 36, 69

```java
private ArrayList driverList;
public ArrayList getDriverList() { ... }
public void setDriverList(ArrayList driverList) { ... }
```

The `driverList` field uses the raw `ArrayList` type (no type parameter). This suppresses compile-time type safety for the driver list. Without tests that exercise the getter/setter with typed data, the actual element type expected by callers is undocumented and unenforced. A regression that changes the element type would not be detected at compile time.

---

### A36-9 | Severity: MEDIUM | GPSReportSearchForm — Lombok @Data on ActionForm subclass; equals/hashCode contract untested

**Location:** `GPSReportSearchForm.java`, line 16

Lombok `@Data` generates `equals` and `hashCode` based on all fields, including the mutable `manufacturers` and `unitTypes` list fields. `ActionForm` subclasses are typically used as mutable request-scoped beans; generating `equals`/`hashCode` over mutable collection fields can produce incorrect behaviour if instances are placed in sets or used as map keys during their lifecycle. The `@Data`-generated `toString` also exposes the full list contents, which may be verbose in log output. No tests assert the equality or hashing semantics of this class.

---

### A36-10 | Severity: LOW | DriverJobDetailsActionForm — no explicit constructor; no test for default field values

**Location:** `DriverJobDetailsActionForm.java`

No explicit constructor is defined. The JVM default constructor leaves `id` at `0` (int) and all String/ArrayList fields as `null`. No test verifies the post-construction state of a new instance. In particular, `getDriverList()` returning `null` (rather than an empty list) on a fresh instance is a latent NPE risk for callers that iterate the returned list without a null check.

---

### A36-11 | Severity: LOW | FleetcheckActionForm — no explicit constructor; array fields default to null with no test coverage

**Location:** `FleetcheckActionForm.java`

No explicit constructor is defined. All three array fields (`id[]`, `answer[]`, `faulty[]`) and all String fields default to `null`. No test verifies the post-construction state. Callers iterating `getId()`, `getAnswer()`, or `getFaulty()` without null checks would produce `NullPointerException`.

---

## Coverage summary

| Class | Test file exists | Methods tested | Branches tested | Notable defects |
|-------|-----------------|---------------|-----------------|-----------------|
| `DriverJobDetailsActionForm` | No | 0 / 27 (0%) | 0 / 0 | Raw ArrayList (A36-8), null driverList risk (A36-10) |
| `FleetcheckActionForm` | No | 0 / 14 (0%) | 0 / 0 | Missing validate() (A36-7), null array risk (A36-11) |
| `GPSReportSearchForm` | No | 0 / 1 explicit + 0 / 15 Lombok (0%) | 0 / 10 | Tautological condition (A36-4), unitId data loss (A36-6) |

**Overall: 0% test coverage across all three audited classes.**
