# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A49
**Files audited:**
- `src/main/java/com/bean/GPSUnitBean.java`
- `src/main/java/com/bean/ImpactBean.java`
- `src/main/java/com/bean/ImpactLevel.java`

---

## 1. Reading-Evidence Blocks

### 1.1 GPSUnitBean

**File:** `src/main/java/com/bean/GPSUnitBean.java`
**Class:** `GPSUnitBean` (line 16) — `public class`

**Lombok annotations (lines 12–15):**
| Annotation | Line | Generated behaviour |
|---|---|---|
| `@Data` | 12 | Generates getters, setters, `equals`, `hashCode`, `toString` for all fields |
| `@NoArgsConstructor` | 13 | Generates public no-arg constructor |
| `@Builder` | 14 | Generates static inner `Builder` class and `builder()` factory method |
| `@AllArgsConstructor(access = AccessLevel.PRIVATE)` | 15 | Generates private all-args constructor (consumed by `@Builder`) |

**Fields:**
| Field | Type | Line |
|---|---|---|
| `vehName` | `String` | 18 |
| `longitude` | `String` | 19 |
| `latitude` | `String` | 20 |
| `timeStmp` | `java.sql.Timestamp` | 21 |
| `status` | `String` | 22 |
| `manufacturer` | `String` | 23 |
| `type` | `String` | 24 |
| `power` | `String` | 25 |

**Explicitly declared methods:** None. All methods are Lombok-generated at compile time.

**Lombok-generated methods (all untested):**
- `getVehName()`, `setVehName(String)`
- `getLongitude()`, `setLongitude(String)`
- `getLatitude()`, `setLatitude(String)`
- `getTimeStmp()`, `setTimeStmp(Timestamp)`
- `getStatus()`, `setStatus(String)`
- `getManufacturer()`, `setManufacturer(String)`
- `getType()`, `setType(String)`
- `getPower()`, `setPower(String)`
- `equals(Object)`, `hashCode()`, `toString()`
- `builder()` / `GPSUnitBean.GPSUnitBeanBuilder`

---

### 1.2 ImpactBean

**File:** `src/main/java/com/bean/ImpactBean.java`
**Class:** `ImpactBean` (line 12) — `public class implements Serializable`

**Annotations (lines 10–11):**
| Annotation | Line | Generated behaviour |
|---|---|---|
| `@Data` | 10 | Generates getters, setters, `equals`, `hashCode`, `toString` |
| `@NoArgsConstructor` | 11 | Generates public no-arg constructor |
| `@Builder` | 24 | Applied to private constructor — generates `builder()` factory |

**Fields:**
| Field | Type | Line |
|---|---|---|
| `serialVersionUID` | `private static final long` | 13 |
| `equipId` | `private int` | 15 |
| `accHours` | `private double` | 16 |
| `sessHours` | `private double` | 17 |
| `impact_threshold` | `private double` | 18 |
| `alert_enabled` | `private boolean` | 19 |
| `percentage` | `private double` | 20 |
| `reset_calibration_date` | `private String` | 21 |
| `calibration_date` | `private String` | 22 |

**Explicitly declared methods:**
| Method | Lines | Description |
|---|---|---|
| `ImpactBean(int, double, double, double, boolean, double, String, String)` (private `@Builder` constructor) | 25–41 | All-field constructor, used exclusively by the Lombok builder |
| `calculateGForceRequiredForImpact(ImpactLevel)` | 43–45 | Delegates to `ImpactUtil.calculateGForceRequiredForImpact(impact_threshold, impactLevel)` |

**Lombok-generated methods (all untested):**
- `getEquipId()`, `setEquipId(int)`
- `getAccHours()`, `setAccHours(double)`
- `getSessHours()`, `setSessHours(double)`
- `getImpact_threshold()`, `setImpact_threshold(double)`
- `isAlert_enabled()`, `setAlert_enabled(boolean)`
- `getPercentage()`, `setPercentage(double)`
- `getReset_calibration_date()`, `setReset_calibration_date(String)`
- `getCalibration_date()`, `setCalibration_date(String)`
- `equals(Object)`, `hashCode()`, `toString()`
- `builder()` / `ImpactBean.ImpactBeanBuilder`

---

### 1.3 ImpactLevel

**File:** `src/main/java/com/bean/ImpactLevel.java`
**Class:** `ImpactLevel` (line 3) — `public enum`

**Enum constants:**
| Constant | Line |
|---|---|
| `BLUE` | 4 |
| `AMBER` | 5 |
| `RED` | 6 |

**Implicitly generated enum methods (all untested as direct subjects):**
- `values()` — returns all constants in declaration order
- `valueOf(String)` — parses a constant by name
- `name()`, `ordinal()`, `toString()` — inherited from `java.lang.Enum`

---

## 2. Test-Directory Grep Results

**Search target:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Existing test files:**
```
com/calibration/UnitCalibrationImpactFilterTest.java
com/calibration/UnitCalibrationTest.java
com/calibration/UnitCalibratorTest.java
com/util/ImpactUtilTest.java
```

| Search term | Files matched |
|---|---|
| `GPSUnitBean` | **0** |
| `ImpactBean` | **0** |
| `ImpactLevel` | `com/util/ImpactUtilTest.java` (as a parameter to `ImpactUtil` static methods only; no direct tests of the enum itself) |

---

## 3. Coverage Gaps and Findings

---

### GPSUnitBean

**A49-1 | Severity: HIGH | GPSUnitBean — no test class exists**

There is no test file anywhere under `src/test/java/` that references `GPSUnitBean`. The class has no hand-written logic, but untested Lombok configuration is a meaningful gap: if annotations are mis-ordered or a field is added/removed, no regression will be caught. The `@Builder` + `@AllArgsConstructor(access = AccessLevel.PRIVATE)` pattern requires that the private constructor is correctly consumed by the builder; this interaction is never exercised by a test.

**A49-2 | Severity: MEDIUM | GPSUnitBean — builder construction is not tested**

`GPSUnitBean.builder()` and the resulting `GPSUnitBeanBuilder` are never instantiated in any test. There is no verification that a fully-populated builder produces an object whose getters return the expected values, nor that the `@Data`-generated `equals` and `hashCode` behave correctly for GPS coordinate comparison scenarios.

**A49-3 | Severity: MEDIUM | GPSUnitBean — no-arg constructor and setters are not tested**

The `@NoArgsConstructor` path (used by frameworks such as Struts when populating beans from HTTP request parameters) is untested. No test verifies that fields can be set individually via setters and retrieved via getters, which is the primary runtime usage pattern of this bean.

**A49-4 | Severity: LOW | GPSUnitBean — `equals` / `hashCode` / `toString` contract is not tested**

`@Data` generates `equals` based on all fields. Any future addition of a field that should be excluded from equality (e.g. `timeStmp` in a de-duplication context) will not be caught without a contract test.

**A49-5 | Severity: LOW | GPSUnitBean — `java.sql.Timestamp` field type carries a serialisation concern**

`Timestamp` extends `java.util.Date` and has known `equals`/`compareTo` asymmetry with `Date`. `GPSUnitBean` has no explicit `serialVersionUID`, yet if it were to implement `Serializable` in the future the `@Data`-generated `equals` would silently include the `Timestamp` field. This is an absence-of-test observation, not a code defect, but there is no test guarding this behaviour.

---

### ImpactBean

**A49-6 | Severity: CRITICAL | ImpactBean — no test class exists**

There is no test file anywhere under `src/test/java/` that references `ImpactBean`. The class contains one hand-written method with real business logic (`calculateGForceRequiredForImpact`) that is completely untested through the bean's own public interface.

**A49-7 | Severity: HIGH | ImpactBean.calculateGForceRequiredForImpact — zero direct test coverage**

`calculateGForceRequiredForImpact(ImpactLevel)` at line 43 delegates to `ImpactUtil.calculateGForceRequiredForImpact(impact_threshold, impactLevel)`. While `ImpactUtil`'s static method is tested directly in `ImpactUtilTest`, the delegation path through `ImpactBean` — which reads the bean's own `impact_threshold` field — is never exercised. Scenarios not covered:
- Correct result when `impact_threshold` was set via the builder.
- Correct result when `impact_threshold` was set to 0.0 (zero threshold edge case).
- Correct result for each of the three `ImpactLevel` constants (BLUE, AMBER, RED) when called through the bean.
- Behaviour when `impact_threshold` is negative (ImpactUtil would compute `Math.sqrt` of a negative product, yielding `NaN`).

**A49-8 | Severity: HIGH | ImpactBean — builder construction with `@Builder` on a private constructor is not tested**

The `@Builder` annotation is placed on the private all-args constructor (line 24). This is a non-standard pattern compared to class-level `@Builder`. No test verifies that `ImpactBean.builder().equipId(1).impact_threshold(500000).build()` produces a bean with the correct field values accessible through getters.

**A49-9 | Severity: MEDIUM | ImpactBean — no-arg constructor leaves all numeric fields at default zero values**

The `@NoArgsConstructor` at line 11 initialises `impact_threshold` to `0.0`. Calling `calculateGForceRequiredForImpact(ImpactLevel.BLUE)` on a default-constructed `ImpactBean` will return `0.0` (since `sqrt(0) = 0`). This edge case is not tested, and callers could misinterpret zero as a valid G-force result rather than an uninitialised-bean error.

**A49-10 | Severity: MEDIUM | ImpactBean — `equals` / `hashCode` contract is not tested**

`@Data` generates `equals` and `hashCode` from all fields. If `ImpactBean` objects are ever stored in a `Set` or used as `Map` keys (common in session-level caching), the untested contract could produce duplicates or lost entries.

**A49-11 | Severity: LOW | ImpactBean — `serialVersionUID` is declared but serialisation round-trip is not tested**

`private static final long serialVersionUID = -140132772466965248L` (line 13) signals deliberate serialisation support. There are no tests verifying that an `ImpactBean` can be serialised and deserialised with field fidelity, nor that the declared `serialVersionUID` matches the class structure after future refactors.

---

### ImpactLevel

**A49-12 | Severity: HIGH | ImpactLevel — no dedicated test class exists**

There is no test file that directly targets `ImpactLevel`. The enum constants are used as inputs to `ImpactUtil` methods in `ImpactUtilTest`, but no test verifies the enum's own contract.

**A49-13 | Severity: MEDIUM | ImpactLevel.values() — exhaustiveness assumption is untested**

`ImpactUtil.getImpactLevelCoefficient` and `ImpactUtil.getCSSColor` both have `switch` statements with a `default` branch that throws `UnhandledImpactLevelException`. No test verifies that every constant returned by `ImpactLevel.values()` is handled by those switches, meaning a future addition of a fourth constant (e.g., `BLACK`) would compile cleanly but throw at runtime without triggering a test failure. A parameterised test iterating over `ImpactLevel.values()` would close this gap.

**A49-14 | Severity: MEDIUM | ImpactLevel.valueOf — string parsing is untested**

`ImpactLevel.valueOf("BLUE")`, `"AMBER"`, and `"RED"` are the paths used when deserialising enum values from database strings or JSON. No test covers correct parsing or the `IllegalArgumentException` thrown for an invalid string. This is particularly relevant since `ImpactBean` and `ImpactUtil` are part of a data-pipeline that presumably reads thresholds from a database.

**A49-15 | Severity: LOW | ImpactLevel — ordinal/declaration order is untested**

The ordinal values (`BLUE=0`, `AMBER=1`, `RED=2`) are implicit in the enum declaration. If severity-ordering logic elsewhere assumes BLUE < AMBER < RED by ordinal, any re-ordering of constants would not be caught by any existing test.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A49-1 | HIGH | GPSUnitBean | No test class exists |
| A49-2 | MEDIUM | GPSUnitBean | Builder construction not tested |
| A49-3 | MEDIUM | GPSUnitBean | No-arg constructor and setter path not tested |
| A49-4 | LOW | GPSUnitBean | `equals`/`hashCode`/`toString` contract not tested |
| A49-5 | LOW | GPSUnitBean | `Timestamp` field equality edge case not guarded by tests |
| A49-6 | CRITICAL | ImpactBean | No test class exists; hand-written business logic is completely uncovered |
| A49-7 | HIGH | ImpactBean | `calculateGForceRequiredForImpact` zero direct coverage; edge cases unexercised |
| A49-8 | HIGH | ImpactBean | Non-standard `@Builder` on private constructor not tested |
| A49-9 | MEDIUM | ImpactBean | Zero `impact_threshold` (default-constructed bean) edge case not tested |
| A49-10 | MEDIUM | ImpactBean | `equals`/`hashCode` contract not tested |
| A49-11 | LOW | ImpactBean | Serialisation round-trip not tested despite `serialVersionUID` declaration |
| A49-12 | HIGH | ImpactLevel | No dedicated test class exists |
| A49-13 | MEDIUM | ImpactLevel | Switch exhaustiveness over `values()` not verified by any test |
| A49-14 | MEDIUM | ImpactLevel | `valueOf(String)` parsing and invalid-string exception not tested |
| A49-15 | LOW | ImpactLevel | Ordinal/declaration order assumptions not tested |

**Total findings: 15**
- CRITICAL: 1
- HIGH: 4
- MEDIUM: 6
- LOW: 4

---

## 5. Recommended Test Classes

Three new test classes are needed:

1. **`src/test/java/com/bean/GPSUnitBeanTest.java`** — test builder construction, no-arg + setter round-trip, `equals`/`hashCode`, and `toString`.
2. **`src/test/java/com/bean/ImpactBeanTest.java`** — test builder construction, `calculateGForceRequiredForImpact` for all three `ImpactLevel` values, zero-threshold edge case, negative-threshold edge case, and serialisation round-trip.
3. **`src/test/java/com/bean/ImpactLevelTest.java`** — test `values()` count and member identity, `valueOf` for all valid strings, `valueOf` for an invalid string, and ordinal order.
