# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A51
**Date:** 2026-02-26
**Project:** forkliftiqadmin (Java / Struts / Tomcat)

---

## Source Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/bean/ImpactReportGroupEntryBean.java` |
| 2 | `src/main/java/com/bean/IncidentReportBean.java` |
| 3 | `src/main/java/com/bean/IncidentReportEntryBean.java` |

---

## Reading-Evidence Blocks

### 1. `ImpactReportGroupEntryBean`

**File:** `src/main/java/com/bean/ImpactReportGroupEntryBean.java`
**Class:** `ImpactReportGroupEntryBean implements Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `static final long` | 13 |
| `id` | `Long` | 15 |
| `impactDateTime` | `String` | 16 |
| `impactValue` | `Integer` | 17 |
| `impactThreshold` | `Integer` | 18 |
| `driverName` | `String` | 19 |
| `companyName` | `String` | 20 |

**Methods (explicit — Lombok-generated getters/setters/equals/hashCode/toString not listed separately):**

| Method | Visibility | Lines | Notes |
|--------|-----------|-------|-------|
| `ImpactReportGroupEntryBean(Long, String, Integer, Integer, String, String)` | `private` (builder) | 23-35 | `@Builder`-annotated all-args constructor |
| `getImpactLevel()` | `private` | 37-39 | Returns `ImpactLevel`; delegates to `ImpactUtil.calculateImpactLevel(impactValue, impactThreshold)` |
| `getGForce()` | `public` | 41-43 | Returns `double`; delegates to `ImpactUtil.calculateGForceOfImpact(impactValue)` |
| `getImpactLevelCSSColor()` | `public` | 45-47 | Returns `String`; calls `getImpactLevel()` then `ImpactUtil.getCSSColor(...)` |

**Lombok-generated (inferred from `@Data` + `@NoArgsConstructor` + `@Builder`):**
- No-args constructor (line 11 annotation)
- `getId()`, `setId(Long)`, `getImpactDateTime()`, `setImpactDateTime(String)`, `getImpactValue()`, `setImpactValue(Integer)`, `getImpactThreshold()`, `setImpactThreshold(Integer)`, `getDriverName()`, `setDriverName(String)`, `getCompanyName()`, `setCompanyName(String)`
- `equals(Object)`, `hashCode()`, `toString()`
- Static inner `ImpactReportGroupEntryBeanBuilder` class with fluent builder methods

---

### 2. `IncidentReportBean`

**File:** `src/main/java/com/bean/IncidentReportBean.java`
**Class:** `IncidentReportBean implements Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `static final long` | 20 |
| `entries` | `List<IncidentReportEntryBean>` | 21 |

**Methods (explicit):**
None — the class body contains no explicitly declared methods.

**Lombok-generated (inferred from `@Data` + `@NoArgsConstructor` + `@AllArgsConstructor`):**
- No-args constructor (field initializer: `entries = new ArrayList<>()`)
- All-args constructor: `IncidentReportBean(List<IncidentReportEntryBean>)`
- `getEntries()`, `setEntries(List<IncidentReportEntryBean>)`
- `equals(Object)`, `hashCode()`, `toString()`

---

### 3. `IncidentReportEntryBean`

**File:** `src/main/java/com/bean/IncidentReportEntryBean.java`
**Class:** `IncidentReportEntryBean implements Serializable`
**Lombok annotations:** `@Data`, `@Builder`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `static final long` | 11 |
| `unitName` | `String` | 13 |
| `manufacture` | `String` | 14 |
| `companyName` | `String` | 15 |
| `driverName` | `String` | 16 |
| `reportTime` | `String` | 17 |
| `injureType` | `String` | 18 |
| `witness` | `String` | 19 |
| `location` | `String` | 20 |
| `injury` | `Boolean` | 21 |
| `description` | `String` | 22 |
| `signature` | `String` | 23 |
| `event_time` | `String` | 24 |
| `near_miss` | `Boolean` | 25 |
| `incident` | `Boolean` | 26 |
| `image` | `String` | 27 |

**Methods (explicit):**
None — the class body contains no explicitly declared methods.

**Lombok-generated (inferred from `@Data` + `@Builder`):**
- All-args constructor (package-private, used by builder)
- Static `builder()` factory method
- Static inner `IncidentReportEntryBeanBuilder` class with per-field fluent setters and `build()`
- Getters and setters for all 14 non-static fields
- `equals(Object)`, `hashCode()`, `toString()`

---

## Test-Directory Grep Results

**Test directory searched:** `src/test/java/`

**Existing test files found:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Search term | Matches in test directory |
|-------------|--------------------------|
| `ImpactReportGroupEntryBean` | **None** |
| `IncidentReportBean` | **None** |
| `IncidentReportEntryBean` | **None** |

All three classes are completely absent from the test suite.

---

## Coverage Gaps and Findings

### ImpactReportGroupEntryBean

---

**A51-1 | Severity: CRITICAL | `ImpactReportGroupEntryBean` — zero test coverage: no test class exists**

No test file references `ImpactReportGroupEntryBean`. The class has hand-written, non-trivial public business methods (`getGForce()`, `getImpactLevelCSSColor()`) that delegate to `ImpactUtil`, as well as a private computation method (`getImpactLevel()`). None of these execution paths are exercised by any test.

---

**A51-2 | Severity: HIGH | `getGForce()` — public method completely untested**

`getGForce()` (line 41-43) calls `ImpactUtil.calculateGForceOfImpact(impactValue)` using the bean's own `impactValue` field (type `Integer`). No test verifies the returned `double` value for any combination of input, including boundary conditions (zero, null auto-unboxing, negative values). Auto-unboxing of a `null` `Integer` to primitive `int` (passed as `long` parameter) would throw a `NullPointerException` at runtime with no guard in place.

---

**A51-3 | Severity: HIGH | `getImpactLevelCSSColor()` — public method completely untested**

`getImpactLevelCSSColor()` (line 45-47) chains through `getImpactLevel()` then `ImpactUtil.getCSSColor(...)`. No test exercises this path for any impact level (BLUE, AMBER, RED) or for the edge case where `calculateImpactLevel` returns `null` (i.e., when `impactValue <= impactThreshold`). A `null` return from `getImpactLevel()` would cause `ImpactUtil.getCSSColor(null)` to fall through to the `default` branch in `getCSSColor`, throwing `UnhandledImpactLevelException` at runtime — a scenario that is never caught or tested.

---

**A51-4 | Severity: HIGH | `getImpactLevel()` (private) — null-return risk untested at the bean level**

`getImpactLevel()` (line 37-39) returns `null` when `impactValue <= impactThreshold` (per `ImpactUtil.calculateImpactLevel` line 49). Because `getImpactLevelCSSColor()` passes this return value directly to `ImpactUtil.getCSSColor()`, a `null` `ImpactLevel` triggers an `UnhandledImpactLevelException`. No test covers this bean-level null propagation path.

---

**A51-5 | Severity: MEDIUM | `@Builder` constructor — builder instantiation path untested**

The `@Builder`-annotated private constructor (lines 23-35) and the generated `ImpactReportGroupEntryBeanBuilder` are never exercised in any test. No test verifies that the builder correctly populates all six fields or that partial construction (omitting optional fields) results in expected null defaults.

---

**A51-6 | Severity: MEDIUM | `@Data`-generated `equals()` and `hashCode()` — untested**

`@Data` generates `equals()` and `hashCode()` based on all fields. No test verifies equality contracts (reflexivity, symmetry, transitivity) or that `hashCode` is consistent with `equals`. These are especially relevant if instances are used as map keys or in collections.

---

**A51-7 | Severity: LOW | `@Data`-generated `toString()` — untested**

The Lombok-generated `toString()` includes all field values. It is not tested for correct format or null-field handling. While low severity in isolation, `toString()` failures surface unexpectedly in logging/auditing contexts.

---

**A51-8 | Severity: LOW | `@NoArgsConstructor` — default construction path untested**

No test constructs `ImpactReportGroupEntryBean` via the no-args constructor and verifies that all fields default to `null`. Calling `getGForce()` or `getImpactLevelCSSColor()` on a default-constructed instance would trigger `NullPointerException` on auto-unboxing of `null` `Integer` fields.

---

### IncidentReportBean

---

**A51-9 | Severity: HIGH | `IncidentReportBean` — zero test coverage: no test class exists**

No test file references `IncidentReportBean`. The class is a list-bearing aggregate whose constructor and `@Data`-generated methods are entirely untested.

---

**A51-10 | Severity: HIGH | `@NoArgsConstructor` initializer `entries = new ArrayList<>()` — untested**

The field initializer `private List<IncidentReportEntryBean> entries = new ArrayList<>()` (line 21) ensures a non-null list on no-args construction. No test verifies this guarantee, which is an important defensive contract for code that calls `getEntries().add(...)` without a null-check.

---

**A51-11 | Severity: MEDIUM | `@AllArgsConstructor` — untested**

The all-args constructor `IncidentReportBean(List<IncidentReportEntryBean>)` is never tested. No test verifies that a provided list is stored correctly, nor that passing `null` does not cause downstream NPEs.

---

**A51-12 | Severity: MEDIUM | `@Data`-generated `equals()` and `hashCode()` — untested**

`equals()` compares `entries` list contents. No test verifies equality when entries differ, when lists are empty, or when lists contain equal/unequal `IncidentReportEntryBean` instances.

---

**A51-13 | Severity: LOW | `@Data`-generated `toString()` — untested**

Not tested for expected format or null-list handling.

---

### IncidentReportEntryBean

---

**A51-14 | Severity: HIGH | `IncidentReportEntryBean` — zero test coverage: no test class exists**

No test file references `IncidentReportEntryBean`. The class has 14 data fields, a Lombok-generated builder, and `@Data`-generated accessors, none of which are exercised by any test.

---

**A51-15 | Severity: HIGH | `@Builder` — builder instantiation and field population untested**

The `IncidentReportEntryBeanBuilder` (generated from `@Builder` at line 9) is never instantiated in any test. No test verifies that `unitName`, `manufacture`, `companyName`, `driverName`, `reportTime`, `injureType`, `witness`, `location`, `injury`, `description`, `signature`, `event_time`, `near_miss`, `incident`, or `image` are stored and retrieved correctly after a `build()` call.

---

**A51-16 | Severity: MEDIUM | Mixed naming convention (`event_time`, `near_miss`, `incident`) — Boolean getter semantics untested**

Fields `event_time` (line 24), `near_miss` (line 25), and `incident` (line 26) use snake_case, which is inconsistent with Java conventions. Lombok generates `getEvent_time()`, `isNear_miss()`, and `isIncident()` (for `Boolean` types). No test confirms what getter names are actually generated, which matters for frameworks that use reflection-based property binding (e.g., Struts, Jackson, JSP EL). Unexpected getter names may cause silent data-binding failures in production.

---

**A51-17 | Severity: MEDIUM | `@Data`-generated `equals()` and `hashCode()` across 14 fields — untested**

With 14 fields, the risk of incorrect equality behavior (e.g., due to mutable fields or `Boolean` boxing) is non-trivial. No test exercises `equals()` or `hashCode()` for any combination of field values.

---

**A51-18 | Severity: LOW | `Boolean` fields (`injury`, `near_miss`, `incident`) — null handling untested**

All three Boolean fields (lines 21, 25, 26) use boxed `Boolean` (not primitive `boolean`), meaning they can be `null`. No test verifies behavior when these fields are null — particularly important if consuming code performs unboxing without a null check.

---

**A51-19 | Severity: LOW | `@Data`-generated `toString()` — untested**

Not tested for expected format or null-field handling across 14 fields.

---

## Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A51-1 | CRITICAL | `ImpactReportGroupEntryBean` | No test class exists — zero coverage |
| A51-2 | HIGH | `ImpactReportGroupEntryBean` | `getGForce()` untested; null `impactValue` causes NPE |
| A51-3 | HIGH | `ImpactReportGroupEntryBean` | `getImpactLevelCSSColor()` untested; null ImpactLevel causes exception |
| A51-4 | HIGH | `ImpactReportGroupEntryBean` | `getImpactLevel()` null-return propagation untested |
| A51-5 | MEDIUM | `ImpactReportGroupEntryBean` | Builder instantiation path untested |
| A51-6 | MEDIUM | `ImpactReportGroupEntryBean` | `equals()` / `hashCode()` untested |
| A51-7 | LOW | `ImpactReportGroupEntryBean` | `toString()` untested |
| A51-8 | LOW | `ImpactReportGroupEntryBean` | No-args constructor + null-field NPE risk untested |
| A51-9 | HIGH | `IncidentReportBean` | No test class exists — zero coverage |
| A51-10 | HIGH | `IncidentReportBean` | `entries` field initializer contract untested |
| A51-11 | MEDIUM | `IncidentReportBean` | All-args constructor untested |
| A51-12 | MEDIUM | `IncidentReportBean` | `equals()` / `hashCode()` untested |
| A51-13 | LOW | `IncidentReportBean` | `toString()` untested |
| A51-14 | HIGH | `IncidentReportEntryBean` | No test class exists — zero coverage |
| A51-15 | HIGH | `IncidentReportEntryBean` | Builder instantiation and all 14 fields untested |
| A51-16 | MEDIUM | `IncidentReportEntryBean` | Snake_case fields may produce unexpected Lombok getter names; untested |
| A51-17 | MEDIUM | `IncidentReportEntryBean` | `equals()` / `hashCode()` across 14 fields untested |
| A51-18 | LOW | `IncidentReportEntryBean` | Boxed `Boolean` null handling untested |
| A51-19 | LOW | `IncidentReportEntryBean` | `toString()` untested |

**Totals:** 1 CRITICAL, 7 HIGH, 6 MEDIUM, 5 LOW
**Overall coverage for these three classes: 0%**
