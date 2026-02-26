# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A59
**Files audited:**
- `src/main/java/com/bean/TimezoneBean.java`
- `src/main/java/com/bean/UnitAssignmentBean.java`
- `src/main/java/com/bean/UnitBean.java`

---

## 1. Reading-Evidence Block

### 1.1 TimezoneBean
**File:** `src/main/java/com/bean/TimezoneBean.java`
**Class:** `com.bean.TimezoneBean implements Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor` (Lombok — generates getters, setters, equals, hashCode, toString, no-arg constructor)

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | `private static final long` field | 15 |
| `id` | `private String` field, default `""` | 17 |
| `name` | `private String` field, default `""` | 18 |
| `zone` | `private String` field, default `""` | 19 |
| `getId()` | Lombok-generated getter | — |
| `getName()` | Lombok-generated getter | — |
| `getZone()` | Lombok-generated getter | — |
| `setId(String)` | Lombok-generated setter | — |
| `setName(String)` | Lombok-generated setter | — |
| `setZone(String)` | Lombok-generated setter | — |
| `equals(Object)` | Lombok-generated | — |
| `hashCode()` | Lombok-generated | — |
| `toString()` | Lombok-generated | — |
| `TimezoneBean()` | Lombok-generated no-arg constructor | — |

**Notes:** Fields default to empty string `""` (not null). No explicit constructor with arguments; the only mutation path is through Lombok setters.

---

### 1.2 UnitAssignmentBean
**File:** `src/main/java/com/bean/UnitAssignmentBean.java`
**Class:** `com.bean.UnitAssignmentBean implements Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`, `@Builder` (on private constructor)

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | `private static final long` field | 12 |
| `id` | `private int` field | 14 |
| `company_name` | `private String` field | 15 |
| `start` | `private String` field | 16 |
| `end` | `private String` field | 17 |
| `current` | `private String` field | 18 |
| `UnitAssignmentBean()` | Lombok-generated no-arg constructor | — |
| `UnitAssignmentBean(int, String, String, String, boolean)` | `@Builder` private constructor | 21–27 |
| `isCurrent` → `current` mapping | boolean → `"Yes"`/`"No"` conversion | 26 |
| `UnitAssignmentBean.builder()` | Lombok-generated builder | — |
| Lombok-generated getters/setters for all five fields | — | — |
| `equals(Object)`, `hashCode()`, `toString()` | Lombok-generated | — |

**Notes:** The boolean-to-`"Yes"`/`"No"` conversion (line 26) is the only hand-written logic. The builder is private, meaning external construction requires the Lombok builder pattern; the no-arg constructor also exists via `@NoArgsConstructor`. `current` is stored as a `String` ("Yes"/"No") rather than as a boolean, which can cause confusion.

---

### 1.3 UnitBean
**File:** `src/main/java/com/bean/UnitBean.java`
**Class:** `com.bean.UnitBean implements Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`, `@Builder` (on private constructor)

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | `private static final long` field | 11 |
| `id` | `private String` field | 13 |
| `name` | `private String` field | 14 |
| `location` | `private String` field | 15 |
| `department` | `private String` field | 16 |
| `type_id` | `private String` field | 17 |
| `type_nm` | `private String` field | 18 |
| `comp_id` | `private String` field | 19 |
| `active` | `private String` field | 20 |
| `size` | `private double` field | 21 |
| `manu_id` | `private String` field | 22 |
| `manu_name` | `private String` field | 23 |
| `fuel_type_id` | `private String` field | 24 |
| `fule_type_name` | `private String` field (**note typo: "fule"**) | 25 |
| `hourmeter` | `private double` field | 26 |
| `serial_no` | `private String` field | 27 |
| `acchours` | `private String` field | 28 |
| `mac_address` | `private String` field | 29 |
| `exp_mod` | `private String` field | 30 |
| `accessible` | `private boolean` field | 31 |
| `access_type` | `private String` field | 32 |
| `keypad_reader` | `private KeypadReaderModel` field — **physical access credential** | 33 |
| `facility_code` | `private String` field — **physical access credential** | 34 |
| `access_id` | `private String` field — **physical access credential** | 35 |
| `weight_unit` | `private String` field | 36 |
| `UnitBean()` | Lombok-generated no-arg constructor | — |
| `UnitBean(String, String, ..., String)` | `@Builder` private constructor (24 params) | 39–64 |
| `UnitBean.builder()` | Lombok-generated builder | — |
| Lombok getters/setters for all 24 fields | — | — |
| `equals(Object)`, `hashCode()`, `toString()` | Lombok-generated | — |
| `KeypadReaderModel` | `public enum` — nested | 66–71 |
| `KeypadReaderModel.ROSLARE` | enum constant | 67 |
| `KeypadReaderModel.KERI` | enum constant | 68 |
| `KeypadReaderModel.SMART` | enum constant | 69 |
| `KeypadReaderModel.HID_ICLASS` | enum constant | 70 |

**Physical access credential fields (highlighted):**
- `access_id` (line 35) — identifier used to authenticate/authorise a forklift unit against a physical access control system
- `facility_code` (line 34) — Wiegand-format facility code passed to keypad/card readers
- `keypad_reader` (line 33) — enum identifying the hardware reader model (ROSLARE, KERI, SMART, HID_ICLASS); drives system behaviour in `AdminUnitAccessForm`, `AdminUnitEditForm`, `UnitsByIdQuery`, `UnitDAO.saveUnitAccessInfo`

---

## 2. Test-Directory Grep Results

**Test directory searched:** `src/test/java/`
**Test files present (4 total):**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Search term | Matches in test directory |
|---|---|
| `TimezoneBean` | **0** |
| `UnitAssignmentBean` | **0** |
| `UnitBean` | **0** |
| `KeypadReaderModel` | **0** |

All four class names return zero matches across the entire test suite.

---

## 3. Coverage Gaps

### 3.1 TimezoneBean — zero test coverage

**A59-1 | Severity: HIGH | TimezoneBean has no test class**

No test file exercises `TimezoneBean`. While the class is a simple Lombok-driven POJO, it is used in three production paths:
- `TimezoneDAO.getAllTimezone()` / `TimezoneDAO.getAll()` / `TimezoneDAO.getTimezone(int)` instantiate it directly.
- `CompanySessionSwitcher` and `AdminSettingsAction` consume the populated bean to drive timezone-switching logic for user sessions.

Missing coverage:
- No-arg constructor produces fields defaulting to `""` (empty string), not `null` — this empty-string default is unusual and untested; callers may not guard against it.
- Lombok `equals`/`hashCode` contract: field identity uses only `id`, `name`, `zone` — no test validates equality semantics used in collections or deduplication.
- No test confirms that `id`, `name`, `zone` round-trip correctly through getters/setters after being set via `TimezoneDAO`.

---

### 3.2 UnitAssignmentBean — zero test coverage

**A59-2 | Severity: HIGH | UnitAssignmentBean has no test class**

No test file exercises `UnitAssignmentBean`. The class contains hand-written boolean-to-String conversion logic that is entirely untested.

Missing coverage:
- **`isCurrent` → `"Yes"`/`"No"` conversion (line 26):** This is the only non-trivial line in the entire file. The ternary `isCurrent ? "Yes" : "No"` is never tested. A regression here (e.g., case change, logic inversion) would be silent.
- **Builder with `isCurrent = true`:** No test verifies that `current` is `"Yes"` when the builder is given `isCurrent = true`.
- **Builder with `isCurrent = false`:** No test verifies that `current` is `"No"` when the builder is given `isCurrent = false`.
- **No-arg constructor:** No test confirms that the no-arg path leaves `current` null (not `"Yes"` or `"No"`), which is a distinct state from builder-constructed instances and could cause NPEs in presentation logic.
- **`equals`/`hashCode`:** `current` participates in Lombok `equals`; `"Yes"`/`"No"` string values affect equality but are never tested.

---

### 3.3 UnitBean — zero test coverage

**A59-3 | Severity: CRITICAL | UnitBean has no test class, and it carries physical access control credentials**

`UnitBean` is the most complex and security-sensitive bean in this audit batch. It has 24 fields, four of which are physical access credentials (`access_id`, `facility_code`, `keypad_reader`, `access_type`). None of its behaviour is tested.

**A59-4 | Severity: CRITICAL | Physical access credential fields are untested — access_id, facility_code, keypad_reader**

`access_id`, `facility_code`, and `keypad_reader` are used in the following production paths with no tests at any layer:
- `UnitDAO.saveUnitAccessInfo(UnitBean)` (line 517 of `UnitDAO.java`) — writes credentials directly to the database.
- `AdminUnitAccessForm.getUnit(String)` / `AdminUnitAccessForm.setUnit(UnitBean)` — reads credentials from HTTP form fields and populates a `UnitBean` for persistence. No validation of `facility_code` or `access_id` format is performed.
- `AdminUnitEditForm.getUnit(String)` — same pattern.
- `UnitsByIdQuery.getResult(ResultSet)` (lines 58–62) — reconstructs `KeypadReaderModel` from a raw database string via `valueOf()` without a try/catch; an unexpected string value would throw `IllegalArgumentException` at runtime.
- `UnitsByCompanyIdQuery.mapResult(ResultSet)` — same `valueOf()` pattern.

Missing coverage:
- No test verifies that `KeypadReaderModel.valueOf()` is called safely (guarded against unknown strings).
- No test verifies each of the four enum constants (`ROSLARE`, `KERI`, `SMART`, `HID_ICLASS`) round-trips through builder and getter.
- No test verifies `keypad_reader = null` is handled by builder and by callers.
- No test verifies `facility_code` and `access_id` accept, reject, or sanitise any particular input format.
- No test verifies `accessible = false` correctly prevents access-credential fields from being acted upon.

**A59-5 | Severity: MEDIUM | Field name typo `fule_type_name` is untested and carries forward into SQL mapping**

The field `fule_type_name` (line 25, should be `fuel_type_name`) is a typo that is permanently encoded in both the class and in `UnitsByIdQuery.getResult()` (`fule_type_name` mapped from column `fuel_type_name`). Because there is no test, this typo has never been caught by any automated check. Any future refactor that corrects the spelling in one location but not the other will cause a silent null-population of the field.

**A59-6 | Severity: MEDIUM | UnitBean.builder() with 24 parameters has no completeness or validation test**

The builder (line 39) accepts 24 parameters. There is no test confirming:
- Which combinations of fields are mandatory vs optional.
- That numeric fields (`size`, `hourmeter`) default to `0.0` (double default) via the no-arg constructor vs builder omission.
- That `accessible = false` (boolean default via no-arg constructor) vs explicit `accessible(true)` in the builder produce different behaviour downstream.

**A59-7 | Severity: LOW | KeypadReaderModel enum has no dedicated enum-contract test**

The four enum constants (`ROSLARE`, `KERI`, `SMART`, `HID_ICLASS`) are never iterated or validated in tests. In `UnitsByIdQuery` and `UnitsByCompanyIdQuery`, enum construction is performed via `KeypadReaderModel.valueOf(...)` on raw database strings. An unrecognised value (e.g., a newly added reader model in the database before a code deployment) will throw an unchecked `IllegalArgumentException` at runtime. No test documents the expected failure mode, and no test exercises the guarded `StringUtils.isNotBlank(...)` path that conditionally calls `valueOf()`.

---

### 3.4 Cross-cutting gap

**A59-8 | Severity: HIGH | The test suite contains only 4 test files covering calibration and impact utilities; the entire bean layer has zero test coverage**

The four existing test files (`UnitCalibrationImpactFilterTest`, `UnitCalibrationTest`, `UnitCalibratorTest`, `ImpactUtilTest`) exclusively test the calibration subsystem. No test infrastructure exists for:
- Any bean class (`com.bean.*`)
- Any DAO class (`com.dao.*`)
- Any action class (`com.action.*`)
- Any action form class (`com.actionform.*`)
- Any query builder class (`com.querybuilder.*`)

The three beans audited here are representative of a systemic absence of bean-layer test coverage across the entire application.

---

## 4. Summary Table

| Finding | Severity | Description |
|---|---|---|
| A59-1 | HIGH | `TimezoneBean` has no test class; empty-string field defaults and equals semantics untested |
| A59-2 | HIGH | `UnitAssignmentBean` has no test class; `isCurrent` → `"Yes"`/`"No"` conversion is the only hand-written logic and is completely untested |
| A59-3 | CRITICAL | `UnitBean` has no test class despite being the most complex bean and carrying physical access credentials |
| A59-4 | CRITICAL | Physical access credential fields `access_id`, `facility_code`, `keypad_reader` flow from HTTP form through persistence with no tests at any layer; `KeypadReaderModel.valueOf()` called without try/catch in two query builders |
| A59-5 | MEDIUM | Field typo `fule_type_name` (line 25) is encoded in both bean and SQL mapping; no test would catch a partial spelling fix |
| A59-6 | MEDIUM | 24-parameter builder has no test for field defaults, mandatory-vs-optional semantics, or numeric zero-defaults |
| A59-7 | LOW | `KeypadReaderModel` enum constants are never exercised in tests; unrecognised DB string values will throw unchecked `IllegalArgumentException` at runtime |
| A59-8 | HIGH | Systemic gap: entire bean/DAO/action/form/querybuilder layers have zero test coverage; only calibration utilities are tested |
