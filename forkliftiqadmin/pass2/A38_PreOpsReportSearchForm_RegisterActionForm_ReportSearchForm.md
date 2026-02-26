# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A38
**Date:** 2026-02-26
**Technology:** Java / Struts / Tomcat

## Source Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/actionform/PreOpsReportSearchForm.java` |
| 2 | `src/main/java/com/actionform/RegisterActionForm.java` |
| 3 | `src/main/java/com/actionform/ReportSearchForm.java` |

**Test directory:** `src/test/java/`
**Existing test files found:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

---

## Reading-Evidence Blocks

### 1. PreOpsReportSearchForm.java

**Class:** `com.actionform.PreOpsReportSearchForm extends ActionForm`
**Annotations:** `@Data` (Lombok — generates getters, setters, toString, equals, hashCode)
**serialVersionUID:** `5162539434628110613L`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `manu_id` | `Long` | 15 |
| `type_id` | `Long` | 16 |
| `start_date` | `String` | 17 |
| `end_date` | `String` | 18 |
| `timezone` | `String` | 19 |
| `manufacturers` | `List<ManufactureBean>` (default `new ArrayList<>()`) | 21 |
| `unitTypes` | `List<UnitTypeBean>` (default `new ArrayList<>()`) | 22 |

**Methods (explicit — Lombok-generated accessors not listed individually):**

| Method | Signature | Lines | Notes |
|--------|-----------|-------|-------|
| Constructor | `PreOpsReportSearchForm()` | 24–25 | no-arg, empty body |
| `getPreOpsReportFilter` | `public PreOpsReportFilterBean getPreOpsReportFilter(String dateFormat)` | 27–34 | Core business logic; builds a `PreOpsReportFilterBean` via builder. Applies null/zero guard on `manu_id` (L29), `type_id` (L30); blank guard on `start_date` (L31) and `end_date` (L32) calling `DateUtil.stringToUTCDate`; identity-comparison timezone guard `timezone == ""` (L33). |

**Lombok-generated accessors** (via `@Data`, not written in source):
`getManu_id`, `setManu_id`, `getType_id`, `setType_id`, `getStart_date`, `setStart_date`,
`getEnd_date`, `setEnd_date`, `getTimezone`, `setTimezone`, `getManufacturers`, `setManufacturers`,
`getUnitTypes`, `setUnitTypes`, `toString`, `equals`, `hashCode`

---

### 2. RegisterActionForm.java

**Class:** `com.actionform.RegisterActionForm extends ActionForm` (`public final`)
**No Lombok annotations** — all accessors hand-written.

**Fields:**

| Field | Type | Default | Line |
|-------|------|---------|------|
| `firstName` | `String` | `null` | 12 |
| `lastName` | `String` | `null` | 13 |
| `expirydt` | `String` | `null` | 14 |
| `licence_no` | `String` | `null` | 15 |
| `veh_id` | `String` | `null` | 16 |
| `dept` | `String` | `null` | 17 |
| `loc` | `String` | `null` | 18 |
| `attachment` | `String` | `null` | 19 |

**Methods:**

| Method | Signature | Lines | Notes |
|--------|-----------|-------|-------|
| `getAttachment` | `public String getAttachment()` | 22–24 | simple getter |
| `setAttachment` | `public void setAttachment(String attachment)` | 25–27 | simple setter |
| `getFirstName` | `public String getFirstName()` | 28–30 | simple getter |
| `setFirstName` | `public void setFirstName(String firstName)` | 31–33 | simple setter |
| `getLastName` | `public String getLastName()` | 34–36 | simple getter |
| `setLastName` | `public void setLastName(String lastName)` | 37–39 | simple setter |
| `getExpirydt` | `public String getExpirydt()` | 41–43 | simple getter |
| `setExpirydt` | `public void setExpirydt(String expirydt)` | 44–46 | simple setter |
| `getLicence_no` | `public String getLicence_no()` | 47–49 | simple getter |
| `setLicence_no` | `public void setLicence_no(String licence_no)` | 50–52 | simple setter |
| `getVeh_id` | `public String getVeh_id()` | 54–56 | simple getter |
| `setVeh_id` | `public void setVeh_id(String veh_id)` | 57–59 | simple setter |
| `getDept` | `public String getDept()` | 61–63 | simple getter |
| `setDept` | `public void setDept(String dept)` | 64–66 | simple setter |
| `getLoc` | `public String getLoc()` | 67–69 | simple getter |
| `setLoc` | `public void setLoc(String loc)` | 70–72 | simple setter |
| `reset` | `public void reset(ActionMapping mapping, HttpServletRequest request)` | 73–77 | Overrides Struts `ActionForm.reset()`; sets `firstName=""`, `lastName=""`, `expirydt=null`; does NOT reset `licence_no`, `veh_id`, `dept`, `loc`, `attachment`. |
| `validate` | `public ActionErrors validate(ActionMapping mapping, HttpServletRequest request)` | 79–101 | Core validation logic; checks `firstName`, `lastName`, `licence_no`, `expirydt`; sets request attributes `veh_id` and `attachment`; contains bugs (see findings). |

---

### 3. ReportSearchForm.java

**Class:** `com.actionform.ReportSearchForm extends ActionForm`
**Annotations:** `@Data`, `@EqualsAndHashCode(callSuper = false)`, `@NoArgsConstructor`, `@AllArgsConstructor` (Lombok)

**Fields:**

| Field | Type | Visibility | Default | Line |
|-------|------|------------|---------|------|
| `manu_id` | `Long` | `protected` | — | 21 |
| `type_id` | `Long` | `protected` | — | 22 |
| `start_date` | `String` | `protected` | — | 23 |
| `end_date` | `String` | `protected` | — | 24 |
| `timezone` | `String` | `protected` | — | 25 |
| `manufacturers` | `List<ManufactureBean>` | `protected` | `new ArrayList<>()` | 27 |
| `unitTypes` | `List<UnitTypeBean>` | `protected` | `new ArrayList<>()` | 28 |

**Methods (explicit — none hand-written; all generated by Lombok):**

Lombok generates: `getManu_id`, `setManu_id`, `getType_id`, `setType_id`, `getStart_date`, `setStart_date`,
`getEnd_date`, `setEnd_date`, `getTimezone`, `setTimezone`, `getManufacturers`, `setManufacturers`,
`getUnitTypes`, `setUnitTypes`, `toString`, `equals`, `hashCode`, no-arg constructor, all-args constructor.

`@EqualsAndHashCode(callSuper = false)` means the parent class (`ActionForm`) fields are excluded from equals/hashCode.

---

## Grep Results — Test Directory Coverage

**Search performed:** `grep -r "PreOpsReportSearchForm" src/test/java/` → **0 matches**
**Search performed:** `grep -r "RegisterActionForm" src/test/java/` → **0 matches**
**Search performed:** `grep -r "ReportSearchForm" src/test/java/` → **0 matches**

**Result: All three classes have zero test coverage.**

---

## Coverage Gap Findings

---

### PreOpsReportSearchForm

**A38-1 | Severity: CRITICAL | `PreOpsReportSearchForm` — no test class exists**

No test file references `PreOpsReportSearchForm` anywhere in the test directory. The class has zero coverage. A dedicated test class `PreOpsReportSearchFormTest` must be created.

---

**A38-2 | Severity: CRITICAL | `getPreOpsReportFilter()` — all conditional branches untested**

The method `getPreOpsReportFilter(String dateFormat)` at lines 27–34 contains six distinct conditional branches; none are exercised by any test:

| Branch | Code | Line |
|--------|------|------|
| `manu_id` is `null` → maps to `null` | `this.manu_id == null \|\| this.manu_id == 0 ? null : this.manu_id` | 29 |
| `manu_id` is `0` → maps to `null` | same expression | 29 |
| `manu_id` is non-null, non-zero → passes through | same expression | 29 |
| `type_id` is `null` → maps to `null` | `this.type_id == null \|\| this.type_id == 0 ? null : this.type_id` | 30 |
| `type_id` is `0` → maps to `null` | same expression | 30 |
| `type_id` is non-null, non-zero → passes through | same expression | 30 |
| `start_date` blank → maps to `null` | `StringUtils.isBlank(this.start_date) ? null : DateUtil.stringToUTCDate(...)` | 31 |
| `start_date` non-blank → calls `DateUtil.stringToUTCDate` | same expression | 31 |
| `end_date` blank → maps to `null` | `StringUtils.isBlank(this.end_date) ? null : DateUtil.stringToUTCDate(...)` | 32 |
| `end_date` non-blank → calls `DateUtil.stringToUTCDate` | same expression | 32 |
| `timezone` is `null` → maps to `null` | `this.timezone == null \|\| this.timezone == "" ? null : this.timezone` | 33 |
| `timezone` non-null, non-empty → passes through | same expression | 33 |

Each input permutation must be tested to confirm the builder produces the correct `PreOpsReportFilterBean`.

---

**A38-3 | Severity: HIGH | `getPreOpsReportFilter()` — identity comparison on String `timezone` is a latent bug, untested**

At line 33: `this.timezone == ""` uses reference identity (`==`) instead of value equality (`.equals("")` or `StringUtils.isBlank()`). Any non-literal empty String (e.g., one read from a request parameter) will not match, causing a non-null empty timezone to be forwarded to the filter bean instead of being coerced to `null`. No test exists to expose this defect. Tests are needed for: (a) `timezone` set to the literal `""`, (b) `timezone` set to `new String("")` (a distinct object), and (c) `timezone` set to a whitespace-only string.

---

**A38-4 | Severity: MEDIUM | `PreOpsReportSearchForm()` constructor — untested**

The explicit no-arg constructor at lines 24–25 is not exercised. While trivial, instantiation should be verified (especially that the `manufacturers` and `unitTypes` lists are initialised to non-null `ArrayList` instances by the field initialisers).

---

**A38-5 | Severity: MEDIUM | Lombok-generated accessors on `PreOpsReportSearchForm` — untested**

All getters and setters (`getManu_id`/`setManu_id`, `getType_id`/`setType_id`, `getStart_date`/`setStart_date`, `getEnd_date`/`setEnd_date`, `getTimezone`/`setTimezone`, `getManufacturers`/`setManufacturers`, `getUnitTypes`/`setUnitTypes`) are generated by `@Data` and are never exercised. Although Lombok itself is assumed correct, round-trip tests confirm the field wiring is as expected.

---

### RegisterActionForm

**A38-6 | Severity: CRITICAL | `RegisterActionForm` — no test class exists**

No test file references `RegisterActionForm`. The class has zero coverage. A dedicated test class `RegisterActionFormTest` must be created.

---

**A38-7 | Severity: CRITICAL | `validate()` — all validation paths untested (lines 79–101)**

The `validate` method contains the only non-trivial logic in the class. None of its paths are covered:

| Scenario | Expected outcome |
|----------|-----------------|
| All fields valid (non-empty `firstName`, `lastName`, `licence_no`; non-null `expirydt`) | `errors` is empty |
| `firstName` is `""` | `errors` contains entry for key `"firstName"` with message key `"error.firstname"` |
| `lastName` is `""` | `errors` contains entry for key `"lastName"` with message key `"error.lastname"` |
| `licence_no` is `""` | `errors` contains entry for key `"lastName"` (note: this is itself a bug — see A38-9) |
| `expirydt` is `null` | `errors` contains entry for key `"expirydt"` with message key `"error.expDate"` |
| Multiple fields invalid simultaneously | `errors` contains multiple entries |
| Request attributes `veh_id` and `attachment` set correctly | `request.getAttribute("veh_id")` and `request.getAttribute("attachment")` match values from form |

---

**A38-8 | Severity: CRITICAL | `validate()` — `NullPointerException` when `firstName`, `lastName`, or `licence_no` is `null`; untested**

At lines 82, 86, and 90:
```java
if (firstName.equalsIgnoreCase("")) { ... }
if (lastName.equalsIgnoreCase("")) { ... }
if (licence_no.equalsIgnoreCase("")) { ... }
```
All three calls dereference the field directly without a null guard. If any field is `null` (which is the declared default for `firstName`, `lastName`, and `licence_no`), a `NullPointerException` is thrown before any `ActionErrors` is returned. The `reset()` method (line 73) sets `firstName` and `lastName` to `""` but not `licence_no`, so `licence_no` remains `null` after a reset. No test exercises the `null` path for any of these three fields. Tests are required for the `null` case to confirm (or expose) the NPE.

---

**A38-9 | Severity: HIGH | `validate()` — `licence_no` error uses wrong error key; untested**

At line 92, the error for an empty `licence_no` is added under the key `"lastName"` rather than `"licence_no"` or a dedicated key:
```java
errors.add("lastName", message);  // line 92 — should be "licence_no"
```
This causes the licence error message to be silently conflated with the last-name error in the UI. No test exists to detect this wrong-key defect. A test asserting the correct key for the `licence_no` error would catch this.

---

**A38-10 | Severity: HIGH | `reset()` — incomplete reset; untested (lines 73–77)**

`reset()` resets only `firstName`, `lastName`, and `expirydt`. Fields `licence_no`, `veh_id`, `dept`, `loc`, and `attachment` are not reset and will retain their previous request values. This is a standard Struts vulnerability (stale form data). No test verifies the post-reset state of any field:

```java
public void reset(ActionMapping mapping, HttpServletRequest request) {
    firstName = "";
    lastName = "";
    expirydt = null;
    // licence_no, veh_id, dept, loc, attachment not reset
}
```

---

**A38-11 | Severity: MEDIUM | All getters and setters on `RegisterActionForm` — untested**

None of the 16 hand-written accessor methods (lines 22–72) are exercised. While individually trivial, the presence of `final` on the class and hand-written (not Lombok-generated) accessors means field name typos or copy-paste errors could go undetected. Round-trip getter/setter tests are required for all eight fields.

---

### ReportSearchForm

**A38-12 | Severity: CRITICAL | `ReportSearchForm` — no test class exists**

No test file references `ReportSearchForm`. The class has zero coverage. A dedicated test class `ReportSearchFormTest` must be created.

---

**A38-13 | Severity: HIGH | `@AllArgsConstructor` — all-args constructor parameter order untested**

Lombok generates the all-args constructor at line 19 with parameters in field declaration order: `(Long manu_id, Long type_id, String start_date, String end_date, String timezone, List<ManufactureBean> manufacturers, List<UnitTypeBean> unitTypes)`. No test verifies that positional arguments map to the correct fields, meaning a reordering of field declarations would silently misroute values without any test failure.

---

**A38-14 | Severity: HIGH | `@EqualsAndHashCode(callSuper = false)` — exclusion of parent fields untested**

The annotation at line 17 explicitly excludes `ActionForm` superclass fields from `equals` and `hashCode`. No test verifies that two instances with identical `ReportSearchForm` field values but different superclass state are considered equal, nor that the generated `equals` correctly handles all field comparisons. This is particularly relevant because `PreOpsReportSearchForm` extends `ReportSearchForm` and relies on this field set.

---

**A38-15 | Severity: MEDIUM | `@NoArgsConstructor` — default list initialisation untested**

The no-arg constructor generated by `@NoArgsConstructor` at line 18 does NOT execute the field-level initialisers (`= new ArrayList<ManufactureBean>()` at line 27, `= new ArrayList<UnitTypeBean>()` at line 28). This means that after construction via the no-arg constructor, `manufacturers` and `unitTypes` will be `null`. No test verifies the post-construction state of these collections, which could lead to `NullPointerException` in calling code that iterates the lists without a null guard.

---

**A38-16 | Severity: MEDIUM | Lombok-generated accessors on `ReportSearchForm` — untested**

All getters and setters (`getManu_id`/`setManu_id`, `getType_id`/`setType_id`, `getStart_date`/`setStart_date`, `getEnd_date`/`setEnd_date`, `getTimezone`/`setTimezone`, `getManufacturers`/`setManufacturers`, `getUnitTypes`/`setUnitTypes`), `toString`, `equals`, and `hashCode` are not exercised by any test.

---

**A38-17 | Severity: LOW | `ReportSearchForm` field visibility `protected` — subclass contract untested**

All seven fields are declared `protected` (not `private` as is idiomatic for `@Data` forms) to expose them to subclasses (`PreOpsReportSearchForm`, and presumably other search form subclasses in the package). No test verifies that a subclass instance can read these fields directly (bypassing accessors) or that field-level access produces consistent results with accessor access.

---

## Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A38-1 | CRITICAL | `PreOpsReportSearchForm` | No test class exists |
| A38-2 | CRITICAL | `PreOpsReportSearchForm` | `getPreOpsReportFilter()` — all 12 conditional branches untested |
| A38-3 | HIGH | `PreOpsReportSearchForm` | `timezone == ""` identity comparison is a bug; untested |
| A38-4 | MEDIUM | `PreOpsReportSearchForm` | No-arg constructor not tested |
| A38-5 | MEDIUM | `PreOpsReportSearchForm` | Lombok-generated accessors untested |
| A38-6 | CRITICAL | `RegisterActionForm` | No test class exists |
| A38-7 | CRITICAL | `RegisterActionForm` | `validate()` — all validation paths untested |
| A38-8 | CRITICAL | `RegisterActionForm` | `validate()` — NPE when `firstName`, `lastName`, or `licence_no` is `null`; untested |
| A38-9 | HIGH | `RegisterActionForm` | `validate()` — `licence_no` error added under wrong key `"lastName"` |
| A38-10 | HIGH | `RegisterActionForm` | `reset()` — five fields not reset; untested |
| A38-11 | MEDIUM | `RegisterActionForm` | 16 hand-written accessors untested |
| A38-12 | CRITICAL | `ReportSearchForm` | No test class exists |
| A38-13 | HIGH | `ReportSearchForm` | All-args constructor field-order mapping untested |
| A38-14 | HIGH | `ReportSearchForm` | `@EqualsAndHashCode(callSuper = false)` parent exclusion untested |
| A38-15 | MEDIUM | `ReportSearchForm` | No-arg constructor leaves `manufacturers`/`unitTypes` as `null`; untested |
| A38-16 | MEDIUM | `ReportSearchForm` | Lombok-generated accessors untested |
| A38-17 | LOW | `ReportSearchForm` | `protected` field visibility subclass contract untested |

**Total findings: 17**
**CRITICAL: 6 | HIGH: 5 | MEDIUM: 5 | LOW: 1**

---

## Coverage Percentage by Class

| Class | Methods/Branches | Covered | Uncovered | Coverage % |
|-------|-----------------|---------|-----------|------------|
| `PreOpsReportSearchForm` | 1 explicit method (12 branches) + constructor + ~14 Lombok methods | 0 | All | 0% |
| `RegisterActionForm` | 18 methods (reset + validate + 16 accessors) | 0 | All | 0% |
| `ReportSearchForm` | ~16 Lombok methods + 2 constructors | 0 | All | 0% |

**Overall coverage for audited classes: 0%**
