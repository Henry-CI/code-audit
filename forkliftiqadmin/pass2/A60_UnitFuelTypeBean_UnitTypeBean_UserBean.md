# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A60
**Files audited:**
- `src/main/java/com/bean/UnitFuelTypeBean.java`
- `src/main/java/com/bean/UnitTypeBean.java`
- `src/main/java/com/bean/UserBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 UnitFuelTypeBean
**File:** `src/main/java/com/bean/UnitFuelTypeBean.java`
**Package:** `com.bean`
**Class:** `UnitFuelTypeBean implements Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | static final long field | 10 |
| `id` | private String field (default null) | 12 |
| `name` | private String field (default null) | 13 |
| `getId()` | public method, returns String | 14-16 |
| `setId(String id)` | public method, void | 17-19 |
| `getName()` | public method, returns String | 20-22 |
| `setName(String name)` | public method, void | 23-25 |

No-arg constructor: implicit (compiler-generated).
No `equals`, `hashCode`, or `toString` overrides.

---

### 1.2 UnitTypeBean
**File:** `src/main/java/com/bean/UnitTypeBean.java`
**Package:** `com.bean`
**Class:** `UnitTypeBean implements Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | static final long field | 9 |
| `id` | private String field (default `""`) | 10 |
| `name` | private String field (default `""`) | 11 |
| `getId()` | public method, returns String | 13-15 |
| `setId(String id)` | public method, void | 16-18 |
| `getName()` | public method, returns String | 19-21 |
| `setName(String name)` | public method, void | 22-24 |

No-arg constructor: implicit (compiler-generated).
Default field values are empty strings (`""`), unlike `UnitFuelTypeBean` which defaults to `null`.
No `equals`, `hashCode`, or `toString` overrides.

---

### 1.3 UserBean
**File:** `src/main/java/com/bean/UserBean.java`
**Package:** `com.bean`
**Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)
**Class:** `UserBean implements Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | static final long field | 18 |
| `iduser` | private int field | 20 |
| `name` | private String field | 21 |
| `email` | private String field | 22 |
| `password` | private String field | 23 |
| `enabled` | private boolean field | 24 |
| `mobile` | private String field | 25 |
| `first_name` | private String field | 26 |
| `last_name` | private String field | 27 |
| `UserBean(int, String, String, String, boolean, String, String, String)` | `@Builder` private all-args constructor | 30-39 |

Lombok `@Data` generates: `getIduser()`, `setIduser(int)`, `getName()`, `setName(String)`, `getEmail()`, `setEmail(String)`, `getPassword()`, `setPassword(String)`, `isEnabled()`, `setEnabled(boolean)`, `getMobile()`, `setMobile(String)`, `getFirst_name()`, `setFirst_name(String)`, `getLast_name()`, `setLast_name(String)`, `equals(Object)`, `hashCode()`, `toString()`.
Lombok `@NoArgsConstructor` generates: `UserBean()`.
Lombok `@Builder` (on private constructor) generates: `UserBean.builder()` static method and `UserBeanBuilder` inner class.
**Unused import:** `com.bean.CompanyBean.CompanyBeanBuilder` (line 5) — imported but never referenced in this class.

---

## 2. Test Directory Search Results

Test directory searched: `src/test/java/`

Existing test files found:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Class searched | Grep result |
|---|---|
| `UnitFuelTypeBean` | No matches in any test file |
| `UnitTypeBean` | No matches in any test file |
| `UserBean` | No matches in any test file |

**All three classes have zero test coverage.**

---

## 3. Coverage Gap Findings

---

A60-1 | Severity: CRITICAL | `UnitFuelTypeBean` has no test class. Zero test coverage for the entire class — no constructor, getter, or setter is exercised. All four public methods (`getId`, `setId`, `getName`, `setName`) and the implicit no-arg constructor are untested.

---

A60-2 | Severity: CRITICAL | `UnitTypeBean` has no test class. Zero test coverage for the entire class — all four public methods (`getId`, `setId`, `getName`, `setName`) and the implicit no-arg constructor are untested.

---

A60-3 | Severity: CRITICAL | `UserBean` has no test class. Zero test coverage for the entire class. All Lombok-generated getters, setters, `equals`, `hashCode`, `toString`, the no-arg constructor (`@NoArgsConstructor`), and the builder pattern (`@Builder`) are completely untested.

---

A60-4 | Severity: HIGH | `UnitFuelTypeBean` and `UnitTypeBean` have inconsistent field defaults: `UnitFuelTypeBean.id` and `UnitFuelTypeBean.name` default to `null` (line 12-13), while `UnitTypeBean.id` and `UnitTypeBean.name` default to `""` (lines 10-11). This structural inconsistency between two semantically parallel beans is unverified by any test and could cause `NullPointerException` vs empty-string behaviour differences in consuming code that treats them interchangeably.

---

A60-5 | Severity: HIGH | `UserBean` `@Builder` constructor is `private` (line 30). The Lombok-generated `UserBean.builder()` static factory depends on this private constructor. No tests verify that builder construction produces a correctly populated object, that all fields are set, or that the generated `equals`/`hashCode` contract holds.

---

A60-6 | Severity: MEDIUM | `UserBean` has an unused import on line 5: `import com.bean.CompanyBean.CompanyBeanBuilder;`. This import is never referenced within `UserBean` and is dead code. No test exists to surface compilation warnings or static analysis failures triggered by this artefact.

---

A60-7 | Severity: MEDIUM | `UserBean.password` (line 23) is a plain-text String field with no masking in `toString()`. Lombok `@Data` will include `password` in the generated `toString()` output, risking credential exposure in logs. No test verifies that sensitive fields are excluded from `toString()` output.

---

A60-8 | Severity: MEDIUM | Neither `UnitFuelTypeBean` nor `UnitTypeBean` override `equals()` or `hashCode()`. Collections-based operations (deduplication, Map keys) using these beans will fall back to identity equality (`Object` default), which is a common correctness trap. No tests exercise equality semantics for either class.

---

A60-9 | Severity: MEDIUM | `UnitFuelTypeBean` and `UnitTypeBean` implement `Serializable` but neither declares `serialVersionUID` in a manner that is tested for stability, and neither class has a serialisation round-trip test to verify that objects survive serialise/deserialise cycles correctly.

---

A60-10 | Severity: LOW | `UserBean` field names use snake_case (`first_name`, `last_name`, lines 26-27) which is inconsistent with Java naming conventions and the camelCase used for all other fields. Lombok generates `getFirst_name()` / `getLast_name()` accessors accordingly. No test exercises or documents this intentional/unintentional deviation, leaving the API contract unverified.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A60-1 | CRITICAL | UnitFuelTypeBean | No test class exists; 0% coverage |
| A60-2 | CRITICAL | UnitTypeBean | No test class exists; 0% coverage |
| A60-3 | CRITICAL | UserBean | No test class exists; 0% coverage |
| A60-4 | HIGH | UnitFuelTypeBean / UnitTypeBean | Inconsistent null vs empty-string field defaults unverified by tests |
| A60-5 | HIGH | UserBean | @Builder on private constructor unverified; generated builder contract untested |
| A60-6 | MEDIUM | UserBean | Unused import `CompanyBeanBuilder` (line 5) — dead code, no test catches it |
| A60-7 | MEDIUM | UserBean | `password` field exposed in Lombok `toString()` output; no test verifies masking |
| A60-8 | MEDIUM | UnitFuelTypeBean / UnitTypeBean | No `equals`/`hashCode` override; identity equality silently used in collections |
| A60-9 | MEDIUM | UnitFuelTypeBean / UnitTypeBean | No serialisation round-trip tests despite implementing `Serializable` |
| A60-10 | LOW | UserBean | Snake_case field names (`first_name`, `last_name`) violate Java conventions; no test documents this contract |

**Total findings: 10**
**CRITICAL: 3 | HIGH: 2 | MEDIUM: 4 | LOW: 1**
