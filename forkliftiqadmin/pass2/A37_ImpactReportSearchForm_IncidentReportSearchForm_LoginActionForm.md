# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A37
**Files audited:**
- `src/main/java/com/actionform/ImpactReportSearchForm.java`
- `src/main/java/com/actionform/IncidentReportSearchForm.java`
- `src/main/java/com/actionform/LoginActionForm.java`

---

## 1. Reading-Evidence Blocks

### 1.1 ImpactReportSearchForm
**File:** `src/main/java/com/actionform/ImpactReportSearchForm.java`
**Class:** `com.actionform.ImpactReportSearchForm extends ActionForm`
**Lombok annotation:** `@Data` (generates getters, setters, equals, hashCode, toString)

| Element | Kind | Line(s) |
|---------|------|---------|
| `manu_id` | field `Long` | 18 |
| `type_id` | field `Long` | 19 |
| `start_date` | field `String` | 20 |
| `end_date` | field `String` | 21 |
| `impact_level` | field `String` | 22 |
| `timezone` | field `String` | 23 |
| `manufacturers` | field `List<ManufactureBean>` (init `new ArrayList<>`) | 25 |
| `unitTypes` | field `List<UnitTypeBean>` (init `new ArrayList<>`) | 26 |
| `impactLevels` | field `List<ImpactLevel>` (init `Arrays.asList(BLUE, AMBER, RED)`) | 27 |
| `ImpactReportSearchForm()` | constructor (no-arg) | 29–30 |
| `getImpactReportFilter(String dateFormat)` | method — returns `ImpactReportFilterBean` | 32–40 |

**Branch map for `getImpactReportFilter`:**

| Field | Condition | True branch | False branch |
|-------|-----------|-------------|--------------|
| `manu_id` | `null \|\| == 0` | maps to `null` | passes value through |
| `type_id` | `null \|\| == 0` | maps to `null` | passes value through |
| `start_date` | `StringUtils.isBlank` | maps to `null` | calls `DateUtil.stringToUTCDate` |
| `end_date` | `StringUtils.isBlank` | maps to `null` | calls `DateUtil.stringToUTCDate` |
| `impact_level` | `StringUtils.isBlank` | maps to `null` | calls `ImpactLevel.valueOf` |
| `timezone` | `StringUtils.isBlank` | maps to `null` | passes value through |

---

### 1.2 IncidentReportSearchForm
**File:** `src/main/java/com/actionform/IncidentReportSearchForm.java`
**Class:** `com.actionform.IncidentReportSearchForm extends ReportSearchForm`
**Lombok annotations:** `@Data`, `@EqualsAndHashCode(callSuper = false)`

**Declared members (own):**

| Element | Kind | Line(s) |
|---------|------|---------|
| `serialVersionUID` | field `static final long` | 13 |
| `getIncidentReportFilter(String dateFormat)` | method — returns `IncidentReportFilterBean` | 15–22 |

**Inherited fields from `ReportSearchForm` (src/main/java/com/actionform/ReportSearchForm.java):**

| Field | Type |
|-------|------|
| `manu_id` | `Long` |
| `type_id` | `Long` |
| `start_date` | `String` |
| `end_date` | `String` |
| `timezone` | `String` |
| `manufacturers` | `List<ManufactureBean>` |
| `unitTypes` | `List<UnitTypeBean>` |

**Branch map for `getIncidentReportFilter`:**

| Field | Condition | True branch | False branch |
|-------|-----------|-------------|--------------|
| `manu_id` | `null \|\| == 0` | maps to `null` | passes value through |
| `type_id` | `null \|\| == 0` | maps to `null` | passes value through |
| `start_date` | `StringUtils.isBlank` | maps to `null` | calls `DateUtil.stringToUTCDate` |
| `end_date` | `StringUtils.isBlank` | maps to `null` | calls `DateUtil.stringToUTCDate` |
| `timezone` | `StringUtils.isBlank` | maps to `null` | passes value through |

---

### 1.3 LoginActionForm
**File:** `src/main/java/com/actionform/LoginActionForm.java`
**Class:** `com.actionform.LoginActionForm extends ValidatorForm` (`final`)
**Lombok annotations:** `@Data`, `@EqualsAndHashCode(callSuper = true)`

| Element | Kind | Line(s) |
|---------|------|---------|
| `serialVersionUID` | field `static final long` | 13 |
| `username` | field `String` (init `null`) | 15 |
| `password` | field `String` (init `null`) | 16 |
| `message` | field `String` (init `null`) | 17 |
| `action` | field `String` (init `null`) | 18 |
| `timezone` | field `String` (init `null`) | 19 |
| `reset(ActionMapping, HttpServletRequest)` | method — overrides `ValidatorForm.reset` | 21–24 |
| `getTimezone()` | method — returns `String` (custom switch logic) | 26–46 |

**Branch map for `getTimezone`:**

| Input `timezone` | Returned value |
|-----------------|----------------|
| `null` | `null` (line 27) |
| `"ADT"` | `"AST4ADT"` (line 30) |
| `"EDT"` | `"EST5EDT"` (line 32) |
| `"CDT"` | `"CST6CDT"` (line 34) |
| `"MDT"` | `"MST7MDT"` (line 36) |
| `"PDT"` | `"PST8PDT"` (line 38) |
| `"AKDT"` | `"AKST9AKDT"` (line 40) |
| `"HDT"` | `"HST10HDT"` (line 42) |
| any other | `timezone` (default, line 44) |

**Branch map for `reset`:**

| Action | Effect |
|--------|--------|
| Called | Sets `password = ""` and `username = ""` unconditionally |

---

## 2. Test-Directory Grep Results

Test directory searched: `src/test/java/`

Existing test files:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Search term | Matches in test directory |
|-------------|--------------------------|
| `ImpactReportSearchForm` | **None** |
| `IncidentReportSearchForm` | **None** |
| `LoginActionForm` | **None** |
| `getImpactReportFilter` | **None** |
| `getIncidentReportFilter` | **None** |
| `getTimezone` (LoginActionForm context) | **None** |
| `reset.*ActionMapping` | **None** |

None of the three audited classes is referenced anywhere in the test suite.

---

## 3. Coverage Gaps and Findings

---

### A37-1 | Severity: CRITICAL | ImpactReportSearchForm — no test class exists

No test class for `ImpactReportSearchForm` exists anywhere in `src/test/java/`. The class contains a substantive method (`getImpactReportFilter`) with 12 distinct conditional branches. Zero coverage.

---

### A37-2 | Severity: CRITICAL | IncidentReportSearchForm — no test class exists

No test class for `IncidentReportSearchForm` exists anywhere in `src/test/java/`. The class contains a substantive method (`getIncidentReportFilter`) with 10 distinct conditional branches. Zero coverage.

---

### A37-3 | Severity: CRITICAL | LoginActionForm — no test class exists

No test class for `LoginActionForm` exists anywhere in `src/test/java/`. The class contains two non-trivial handwritten methods (`reset` and `getTimezone`) with 9 reachable branches in `getTimezone` alone. Zero coverage.

---

### A37-4 | Severity: HIGH | ImpactReportSearchForm.getImpactReportFilter — manu_id zero-value branch untested

The expression `this.manu_id == null || this.manu_id == 0` contains a separate branch for the value `0` (distinct from `null`). This zero-sentinel idiom is not documented and is untested. Passing `manu_id = 0L` must collapse to `null` in the filter; this is a silent data-contract decision that requires explicit test coverage.

---

### A37-5 | Severity: HIGH | ImpactReportSearchForm.getImpactReportFilter — type_id zero-value branch untested

Identical issue to A37-4 for the `type_id` field. The branch `this.type_id == 0` is a zero-sentinel that maps to `null` and is completely untested.

---

### A37-6 | Severity: HIGH | IncidentReportSearchForm.getIncidentReportFilter — manu_id and type_id zero-value branches untested

Same zero-sentinel pattern (`== 0` maps to `null`) appears in `IncidentReportSearchForm.getIncidentReportFilter` for both `manu_id` and `type_id`. Untested.

---

### A37-7 | Severity: HIGH | LoginActionForm.getTimezone — switch default branch untested

The `default` branch of the `getTimezone` switch (line 44) returns the raw `timezone` string unchanged. This is the path taken for any timezone abbreviation not in the known set (e.g., `"UTC"`, `"GMT"`, unknown strings). It is untested and its contract (pass-through vs. rejection) is undocumented.

---

### A37-8 | Severity: HIGH | LoginActionForm.getTimezone — null guard branch untested

Line 27: `if (timezone == null) return null;` is a guard that silently returns `null` when the field has never been set. This is untested. Combined with `@Data`-generated setter and the field initializer of `null`, there is no test confirming this path.

---

### A37-9 | Severity: HIGH | LoginActionForm.reset — side-effect behaviour untested

`reset(ActionMapping, HttpServletRequest)` overrides `ValidatorForm.reset` and unconditionally blanks `password` and `username`. This is security-relevant behaviour (ensuring credentials are cleared between requests). It is completely untested.

---

### A37-10 | Severity: MEDIUM | ImpactReportSearchForm.getImpactReportFilter — ImpactLevel.valueOf failure path untested

Line 38: `ImpactLevel.valueOf(this.impact_level)` throws `IllegalArgumentException` if `impact_level` is a non-blank string that does not match any enum constant. No test covers this failure path and no exception handling exists in the method. This represents a latent runtime crash risk.

---

### A37-11 | Severity: MEDIUM | ImpactReportSearchForm — Lombok-generated members untested

`@Data` generates `getManu_id`, `setManu_id`, `getType_id`, `setType_id`, `getStart_date`, `setStart_date`, `getEnd_date`, `setEnd_date`, `getImpact_level`, `setImpact_level`, `getTimezone`, `setTimezone`, `getManufacturers`, `setManufacturers`, `getUnitTypes`, `setUnitTypes`, `getImpactLevels`, `setImpactLevels`, `equals`, `hashCode`, and `toString`. While Lombok-generated code is generally trusted, the field initializers (`impactLevels = Arrays.asList(BLUE, AMBER, RED)`) encode a business rule (the fixed set of impact levels presented to users) that has no test verifying the default value is correct and immutable.

---

### A37-12 | Severity: MEDIUM | IncidentReportSearchForm — @EqualsAndHashCode(callSuper = false) untested and potentially incorrect

`@EqualsAndHashCode(callSuper = false)` means the inherited fields from `ReportSearchForm` (`manu_id`, `type_id`, `start_date`, `end_date`, `timezone`) are excluded from equality comparison. This is a significant semantic decision: two `IncidentReportSearchForm` instances differing only in inherited fields will compare as equal. There is no test documenting or verifying this intended behaviour.

---

### A37-13 | Severity: MEDIUM | LoginActionForm.getTimezone — each of the 7 timezone mappings individually untested

All seven explicit `case` branches (`ADT`, `EDT`, `CDT`, `MDT`, `PDT`, `AKDT`, `HDT`) are untested. Each mapping encodes a hardcoded string conversion that could silently regress if values are changed. Absence of a parameterised test means any one mapping could be wrong with no detection.

---

### A37-14 | Severity: MEDIUM | LoginActionForm — reset does not clear message or action fields

The `reset` override clears only `password` and `username` but not `message` or `action`. This is potentially intentional but is undocumented and untested. A test is needed to both confirm the fields that are cleared and confirm the fields that are intentionally left untouched.

---

### A37-15 | Severity: LOW | ImpactReportSearchForm — no-arg constructor is redundant but untested

The explicit no-arg constructor at lines 29–30 is a no-op body that adds nothing beyond what the compiler provides. Because `@Data` does not generate a no-arg constructor and no `@NoArgsConstructor` is present, this constructor is required for Struts form instantiation. However, there is no test confirming that `new ImpactReportSearchForm()` produces the expected default field values (particularly the `impactLevels` list and the empty `ArrayList` instances).

---

### A37-16 | Severity: LOW | ImpactReportSearchForm.getImpactReportFilter — DateUtil.stringToUTCDate integration untested

Lines 36–37 invoke `DateUtil.stringToUTCDate(this.start_date, dateFormat)` and `DateUtil.stringToUTCDate(this.end_date, dateFormat)`. The conversion is only exercised indirectly through the form; there is no test confirming that a known date string and format round-trip correctly through `getImpactReportFilter`.

---

### A37-17 | Severity: LOW | IncidentReportSearchForm — serialVersionUID value is not tested against a known constant

`serialVersionUID = -7959149868858265846L` is declared but never verified in a test. If the class is serialised and the UID changes, deserialization will silently fail. A regression test pinning the UID value would catch inadvertent changes.

---

### A37-18 | Severity: LOW | LoginActionForm — serialVersionUID value is not tested against a known constant

Same issue as A37-17: `serialVersionUID = -4392152148586227798L` has no pinning test.

---

### A37-19 | Severity: INFO | ReportSearchForm (parent) is also without test coverage

`ReportSearchForm` (the parent of `IncidentReportSearchForm`) contains `@NoArgsConstructor`, `@AllArgsConstructor`, `@Data`, and `@EqualsAndHashCode(callSuper = false)` with five protected fields and two list fields. Although not directly in scope for this audit agent, it contributes untested inherited behaviour consumed by `IncidentReportSearchForm`. Flagged for awareness.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A37-1 | CRITICAL | ImpactReportSearchForm | No test class exists — zero coverage |
| A37-2 | CRITICAL | IncidentReportSearchForm | No test class exists — zero coverage |
| A37-3 | CRITICAL | LoginActionForm | No test class exists — zero coverage |
| A37-4 | HIGH | ImpactReportSearchForm | `manu_id == 0` zero-sentinel branch untested |
| A37-5 | HIGH | ImpactReportSearchForm | `type_id == 0` zero-sentinel branch untested |
| A37-6 | HIGH | IncidentReportSearchForm | `manu_id == 0` and `type_id == 0` zero-sentinel branches untested |
| A37-7 | HIGH | LoginActionForm | `getTimezone` switch `default` branch untested |
| A37-8 | HIGH | LoginActionForm | `getTimezone` null-guard branch untested |
| A37-9 | HIGH | LoginActionForm | `reset` security-relevant side effects untested |
| A37-10 | MEDIUM | ImpactReportSearchForm | `ImpactLevel.valueOf` failure path (invalid string) untested |
| A37-11 | MEDIUM | ImpactReportSearchForm | `impactLevels` default-value business rule untested |
| A37-12 | MEDIUM | IncidentReportSearchForm | `@EqualsAndHashCode(callSuper=false)` semantic untested |
| A37-13 | MEDIUM | LoginActionForm | All 7 explicit timezone case mappings individually untested |
| A37-14 | MEDIUM | LoginActionForm | `reset` omits `message`/`action` — intent not verified by test |
| A37-15 | LOW | ImpactReportSearchForm | No-arg constructor default field values not asserted |
| A37-16 | LOW | ImpactReportSearchForm | `DateUtil.stringToUTCDate` integration path untested |
| A37-17 | LOW | IncidentReportSearchForm | `serialVersionUID` value not pinned by a regression test |
| A37-18 | LOW | LoginActionForm | `serialVersionUID` value not pinned by a regression test |
| A37-19 | INFO | ReportSearchForm (parent) | Parent class also has zero test coverage (out of direct scope) |

**Totals:** 3 CRITICAL, 6 HIGH, 5 MEDIUM, 4 LOW, 1 INFO
