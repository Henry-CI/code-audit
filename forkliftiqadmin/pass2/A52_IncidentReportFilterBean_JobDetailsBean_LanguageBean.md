# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A52
**Files audited:**
- `src/main/java/com/bean/IncidentReportFilterBean.java`
- `src/main/java/com/bean/JobDetailsBean.java`
- `src/main/java/com/bean/LanguageBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 IncidentReportFilterBean

**File:** `src/main/java/com/bean/IncidentReportFilterBean.java`
**Package:** `com.bean`
**Class:** `IncidentReportFilterBean extends ReportFilterBean`
**Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = true)`

| Element | Kind | Line(s) |
|---|---|---|
| `IncidentReportFilterBean(Date startDate, Date endDate, Long manuId, Long typeId, String timezone)` | `@Builder` public constructor, delegates to `super(...)` | 13-15 |

**Inherited from `ReportFilterBean` (via `@Data` and `@AllArgsConstructor`):**

| Element | Kind | Line(s) in ReportFilterBean |
|---|---|---|
| `startDate` | private Date field | 15 |
| `endDate` | private Date field | 16 |
| `manuId` | private Long field | 17 |
| `typeId` | private Long field | 18 |
| `timezone` | private String field | 19 |
| `start()` | public method (DateBetweenFilter override), returns startDate or Calendar.getInstance().getTime() | 22-24 |
| `end()` | public method (DateBetweenFilter override), returns endDate or Calendar.getInstance().getTime() | 27-29 |
| `manufactureId()` | public method (UnitManufactureFilter override), returns manuId | 32-34 |
| `type()` | public method (UnitTypeFilter override), returns typeId | 37-39 |
| `timezone()` | public method (DateBetweenFilter override), returns timezone | 42-44 |

Lombok `@Data` generates: `getStartDate()`, `setStartDate()`, `getEndDate()`, `setEndDate()`, `getManuId()`, `setManuId()`, `getTypeId()`, `setTypeId()`, `getTimezone()`, `setTimezone()`, `equals()`, `hashCode()`, `toString()` at compile time.

Lombok `@EqualsAndHashCode(callSuper = true)` generates `equals()` and `hashCode()` including superclass fields.

Lombok `@Builder` on the constructor generates a static `IncidentReportFilterBean.builder()` factory.

Implements interfaces (via `ReportFilterBean`): `DateBetweenFilter`, `UnitManufactureFilter`, `UnitTypeFilter`.

**Notable logic in `ReportFilterBean.start()` and `ReportFilterBean.end()`:** both contain a conditional branch — they return `Calendar.getInstance().getTime()` when the respective field is `null`. This constitutes testable business logic beyond a trivial getter.

---

### 1.2 JobDetailsBean

**File:** `src/main/java/com/bean/JobDetailsBean.java`
**Package:** `com.bean`
**Class:** `JobDetailsBean` (no superclass, no interface, no annotations)

| Element | Kind | Line(s) |
|---|---|---|
| `id` | package-private int field (default 0) | 5 |
| `unitId` | package-private int field (default 0) | 6 |
| `driverId` | package-private int field (default 0) | 7 |
| `duration` | package-private int field (default 0) | 8 |
| `status` | package-private String field (default null) | 9 |
| `driverName` | package-private String field (default null) | 11 |
| `jobNo` | package-private String field (default null) | 12 |
| `description` | package-private String field (default null) | 13 |
| `startTime` | package-private String field (default null) | 14 |
| `endTime` | package-private String field (default null) | 15 |
| `jobTitle` | package-private String field (default null) | 16 |
| `getId()` | public method, returns int | 18-20 |
| `getUnitId()` | public method, returns int | 21-23 |
| `getDriverId()` | public method, returns int | 24-26 |
| `getDuration()` | public method, returns int | 27-29 |
| `getJobNo()` | public method, returns String | 30-32 |
| `getDescription()` | public method, returns String | 33-35 |
| `getStartTime()` | public method, returns String | 36-38 |
| `getEndTime()` | public method, returns String | 39-41 |
| `getJobTitle()` | public method, returns String | 42-44 |
| `setId(int id)` | public method, void | 45-47 |
| `setUnitId(int unitId)` | public method, void | 48-50 |
| `setDriverId(int driverId)` | public method, void | 51-53 |
| `setDuration(int duration)` | public method, void | 54-56 |
| `setJobNo(String jobNo)` | public method, void | 57-59 |
| `setDescription(String description)` | public method, void | 60-62 |
| `setStartTime(String startTime)` | public method, void | 63-65 |
| `setEndTime(String endTime)` | public method, void | 66-68 |
| `setJobTitle(String jobTitle)` | public method, void | 69-71 |
| `getDriverName()` | public method, returns String | 72-74 |
| `setDriverName(String driverName)` | public method, void | 75-77 |
| `getStatus()` | public method, returns String | 78-80 |
| `setStatus(String status)` | public method, void | 81-83 |

No explicit constructor (implicit public no-arg constructor only).
No business logic beyond plain getter/setter pattern.
Fields are package-private (no `private` modifier), exposing them to direct access from within the same package — a design concern.
No `equals()`, `hashCode()`, or `toString()` overrides.
Does not implement `Serializable` (notable given Struts/Tomcat session usage patterns).

---

### 1.3 LanguageBean

**File:** `src/main/java/com/bean/LanguageBean.java`
**Package:** `com.bean`
**Class:** `LanguageBean implements Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | private static final long field (value: 1779643485158161640L) | 10 |
| `id` | private String field (init null) | 11 |
| `name` | private String field (init null) | 12 |
| `local` | private String field (init null) | 19 |
| `getName()` | public method, returns String | 13-15 |
| `setName(String name)` | public method, void | 16-18 |
| `getLocal()` | public method, returns String | 21-23 |
| `setLocal(String local)` | public method, void | 24-26 |
| `getId()` | public method, returns String | 28-30 |
| `setId(String id)` | public method, void | 31-33 |

No explicit constructor (implicit public no-arg constructor only).
Implements `java.io.Serializable` with an explicit `serialVersionUID`.
No business logic beyond standard getter/setter pattern.
No `equals()`, `hashCode()`, or `toString()` overrides.

---

## 2. Test-Directory Grep Results

**Test directory searched:** `src/test/java/`

**Test files present (entire suite):**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Search results:**

| Class name searched | Files matched |
|---|---|
| `IncidentReportFilterBean` | 0 |
| `JobDetailsBean` | 0 |
| `LanguageBean` | 0 |

**Result:** Zero matches for any of the three class names in any test file. No dedicated test class exists for any of the three beans. The `com.bean` package has no corresponding test directory or test class anywhere in the test tree.

---

## 3. Coverage Gaps

### 3.1 IncidentReportFilterBean

| Method / Behaviour | Covered? |
|---|---|
| Builder construction with all fields populated | No |
| Builder construction with all fields null | No |
| `start()` returns `startDate` when `startDate` is non-null | No |
| `start()` returns current time when `startDate` is null (branch in `ReportFilterBean`) | No |
| `end()` returns `endDate` when `endDate` is non-null | No |
| `end()` returns current time when `endDate` is null (branch in `ReportFilterBean`) | No |
| `manufactureId()` returns `manuId` | No |
| `type()` returns `typeId` | No |
| `timezone()` returns `timezone` | No |
| Lombok-generated getters/setters for all five fields | No |
| `equals()` / `hashCode()` including superclass fields (`callSuper = true`) | No |
| `equals()` symmetry / reflexivity / transitivity | No |
| `hashCode()` consistency between equal instances | No |
| `toString()` does not throw | No |
| Interface contracts: `DateBetweenFilter`, `UnitManufactureFilter`, `UnitTypeFilter` | No |

### 3.2 JobDetailsBean

| Method / Behaviour | Covered? |
|---|---|
| Default construction (`new JobDetailsBean()`) | No |
| `getId()` returns 0 on fresh instance | No |
| `getUnitId()` returns 0 on fresh instance | No |
| `getDriverId()` returns 0 on fresh instance | No |
| `getDuration()` returns 0 on fresh instance | No |
| `getStatus()` returns null on fresh instance | No |
| `getDriverName()` returns null on fresh instance | No |
| `getJobNo()` returns null on fresh instance | No |
| `getDescription()` returns null on fresh instance | No |
| `getStartTime()` returns null on fresh instance | No |
| `getEndTime()` returns null on fresh instance | No |
| `getJobTitle()` returns null on fresh instance | No |
| `setId()` / `getId()` round-trip | No |
| `setUnitId()` / `getUnitId()` round-trip | No |
| `setDriverId()` / `getDriverId()` round-trip | No |
| `setDuration()` / `getDuration()` round-trip | No |
| `setStatus()` / `getStatus()` round-trip | No |
| `setDriverName()` / `getDriverName()` round-trip | No |
| `setJobNo()` / `getJobNo()` round-trip | No |
| `setDescription()` / `getDescription()` round-trip | No |
| `setStartTime()` / `getStartTime()` round-trip | No |
| `setEndTime()` / `getEndTime()` round-trip | No |
| `setJobTitle()` / `getJobTitle()` round-trip | No |
| Null-value setter behaviour for all String fields | No |
| `Serializable` contract (not implemented — session safety risk) | No |

### 3.3 LanguageBean

| Method / Behaviour | Covered? |
|---|---|
| Default construction (`new LanguageBean()`) | No |
| `getId()` returns null on fresh instance | No |
| `getName()` returns null on fresh instance | No |
| `getLocal()` returns null on fresh instance | No |
| `setId()` / `getId()` round-trip | No |
| `setName()` / `getName()` round-trip | No |
| `setLocal()` / `getLocal()` round-trip | No |
| Null-value re-assignment via setters | No |
| `Serializable` contract (serialise + deserialise preserving all fields) | No |
| `serialVersionUID` value stability under class changes | No |

---

## 4. Findings

A52-1 | Severity: CRITICAL | `IncidentReportFilterBean` has zero test coverage. No test class exists anywhere in the test tree (`src/test/java/`) that references `IncidentReportFilterBean`. The class inherits and exposes interface-contract methods (`start()`, `end()`, `manufactureId()`, `type()`, `timezone()`) that carry conditional branching logic in the parent `ReportFilterBean`. None of these execution paths — including the null-guard fallback branches in `start()` and `end()` — are exercised by any test.

A52-2 | Severity: CRITICAL | `JobDetailsBean` has zero test coverage. No test class exists anywhere in the test tree that references `JobDetailsBean`. All 22 public methods (11 getters, 11 setters) across 11 fields are completely untested. This bean is a data-carrier used in job/driver reporting; silent field-assignment failures would produce incorrect report output with no automated detection.

A52-3 | Severity: CRITICAL | `LanguageBean` has zero test coverage. No test class exists anywhere in the test tree that references `LanguageBean`. All 6 public methods (`getId`, `setId`, `getName`, `setName`, `getLocal`, `setLocal`) are untested. As a `Serializable` session bean in a Struts/Tomcat application, its serialisation contract is also completely untested.

A52-4 | Severity: HIGH | The conditional null-guard branches in `ReportFilterBean.start()` (line 23) and `ReportFilterBean.end()` (line 28) are untested. Both methods return `Calendar.getInstance().getTime()` when the corresponding date field is `null`. Because `IncidentReportFilterBean` is the only concrete subclass of `ReportFilterBean` audited, these branches can only be triggered through it. The null-field path — which silently substitutes the current timestamp — is a source of subtle data-integrity bugs in date-filtered incident reports and is never verified.

A52-5 | Severity: HIGH | `IncidentReportFilterBean`'s Lombok-generated `equals()` and `hashCode()` (with `callSuper = true`) are untested. The `@EqualsAndHashCode(callSuper = true)` annotation means equality depends on all five superclass fields. No test verifies reflexivity, symmetry, or consistency, nor that two builder-constructed instances with identical field values are considered equal. This matters when instances are used in collections or compared in report-filtering logic.

A52-6 | Severity: HIGH | `JobDetailsBean` fields are package-private (no access modifier), not `private` (lines 5-16). This breaks encapsulation: any class within the `com.bean` package can read or write fields directly, bypassing setters. No test detects or documents this. The absence of `private` is likely an unintentional omission. In a Struts framework, if a framework binding mechanism targets setters but field access is used directly elsewhere, the two values can diverge.

A52-7 | Severity: HIGH | `JobDetailsBean` does not implement `java.io.Serializable` (lines 3-88). In a Struts/Tomcat environment, beans placed in HTTP sessions or passed through action contexts must be serialisable for session replication and failover. `LanguageBean` correctly implements `Serializable`; `JobDetailsBean` does not. No test guards against `NotSerializableException` at runtime when this bean is placed in a session.

A52-8 | Severity: MEDIUM | No getter/setter round-trip tests exist for any field in any of the three beans. Setter-then-getter pairs across all 22 `JobDetailsBean` methods, all 6 `LanguageBean` methods, and the 10 Lombok-generated `IncidentReportFilterBean` accessors are untested. Field-assignment correctness is never verified by the test suite.

A52-9 | Severity: MEDIUM | Null-value setter behaviour is untested for `LanguageBean` and for the String fields of `JobDetailsBean`. Both classes initialise String fields to `null` and expose public setters that accept `null`. No test confirms that calling a setter with `null` on an already-populated instance correctly reassigns the field without throwing a `NullPointerException`, and no test confirms that a subsequent getter returns `null`.

A52-10 | Severity: MEDIUM | The `Serializable` contract for `LanguageBean` is untested. The class declares a specific `serialVersionUID` (1779643485158161640L), indicating deliberate serialisation management. No test serialises a `LanguageBean` instance to a byte stream and deserialises it, verifying that `id`, `name`, and `local` field values are preserved. A future field addition or reordering could silently break deserialisation of persisted sessions.

A52-11 | Severity: MEDIUM | `IncidentReportFilterBean` exposes a Lombok `@Builder` API (line 12) whose construction path is completely untested. No test invokes `IncidentReportFilterBean.builder()...build()`. The builder pattern is the intended public API for constructing instances; its correctness — including that the superclass constructor is called with all five arguments in the correct positions — is never verified.

A52-12 | Severity: LOW | `JobDetailsBean` provides no `equals()`, `hashCode()`, or `toString()` overrides (lines 3-88). It uses the default `Object` identity-based implementations. If two `JobDetailsBean` instances representing the same logical job are compared, they will be unequal. If instances are added to Sets or used as Map keys, duplicates will appear. No test documents the intended equality semantics, and no Lombok or manual override is present.

A52-13 | Severity: LOW | `LanguageBean` provides no `equals()`, `hashCode()`, or `toString()` overrides (lines 5-35), same concern as `JobDetailsBean`. No test documents or validates the intended equality semantics for language entries.

A52-14 | Severity: INFO | The entire test suite contains only 4 test classes (`UnitCalibrationImpactFilterTest`, `UnitCalibrationTest`, `UnitCalibratorTest`, `ImpactUtilTest`), all targeting the `com.calibration` and `com.util` packages exclusively. The `com.bean` package — which contains all three audited classes plus their siblings — has no test package directory and no test class, indicating a systemic and complete absence of bean-layer test coverage, not an isolated omission for these three files.
