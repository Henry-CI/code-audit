# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A53
**Date:** 2026-02-26
**Scope:** LicenceBean, ManuTypeFuleRelBean, ManufactureBean

---

## 1. Reading-Evidence Blocks

### 1.1 LicenceBean
**File:** `src/main/java/com/bean/LicenceBean.java`
**Class:** `com.bean.LicenceBean`
**Implements:** `java.io.Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**

| Line | Field | Type | Initial value |
|------|-------|------|---------------|
| 13 | `driver_id` | `Long` | `null` |
| 14 | `licence_number` | `String` | `null` |
| 15 | `expiry_date` | `String` | `null` |
| 16 | `security_number` | `String` | `null` — **sensitive / PII** |
| 17 | `address` | `String` | `null` |
| 18 | `op_code` | `String` | `null` |

**Methods (explicit in source):**

| Lines | Method | Visibility | Notes |
|-------|--------|------------|-------|
| 21-28 | `LicenceBean(Long driver_id, String licence_number, String expiry_date, String security_number, String address, String op_code)` | `private` | `@Builder` constructor; all six fields set |

**Methods (Lombok-generated — not visible in source):**

| Generated method | Lombok source |
|-----------------|---------------|
| `LicenceBean()` | `@NoArgsConstructor` |
| `getDriver_id()` | `@Data` |
| `setDriver_id(Long)` | `@Data` |
| `getLicence_number()` | `@Data` |
| `setLicence_number(String)` | `@Data` |
| `getExpiry_date()` | `@Data` |
| `setExpiry_date(String)` | `@Data` |
| `getSecurity_number()` | `@Data` — **exposes PII** |
| `setSecurity_number(String)` | `@Data` — **exposes PII** |
| `getAddress()` | `@Data` |
| `setAddress(String)` | `@Data` |
| `getOp_code()` | `@Data` |
| `setOp_code(String)` | `@Data` |
| `equals(Object)` | `@Data` |
| `hashCode()` | `@Data` |
| `toString()` | `@Data` — **includes security_number in output** |
| `canEqual(Object)` | `@Data` |
| `LicenceBean.LicenceBeanBuilder builder()` | `@Builder` (static) |

**Note on `serialVersionUID`:** Class implements `Serializable` but does not declare an explicit `serialVersionUID`. The JVM will compute one at runtime, which can change across compiler versions and cause `InvalidClassException` on deserialization.

---

### 1.2 ManuTypeFuleRelBean
**File:** `src/main/java/com/bean/ManuTypeFuleRelBean.java`
**Class:** `com.bean.ManuTypeFuleRelBean`
**Annotations:** none
**Implements:** none

**Fields:**

| Line | Field | Type | Initial value |
|------|-------|------|---------------|
| 4 | `id` | `String` | `null` |
| 5 | `manu_id` | `String` | `null` |
| 6 | `type_id` | `String` | `null` |
| 7 | `fuel_type_id` | `String` | `null` |
| 8 | `typename` | `String` | `null` |
| 9 | `fueltypename` | `String` | `null` |
| 10 | `manuname` | `String` | `null` |

**Methods (all explicit in source):**

| Lines | Method | Visibility |
|-------|--------|------------|
| 12-14 | `getManuname()` | `public` |
| 15-17 | `setManuname(String manuname)` | `public` |
| 18-20 | `getId()` | `public` |
| 21-23 | `setId(String id)` | `public` |
| 25-27 | `getTypename()` | `public` |
| 28-30 | `setTypename(String typename)` | `public` |
| 31-33 | `getFueltypename()` | `public` |
| 34-36 | `setFueltypename(String fueltypename)` | `public` |
| 39-41 | `getManu_id()` | `public` |
| 42-44 | `setManu_id(String manu_id)` | `public` |
| 45-47 | `getType_id()` | `public` |
| 48-50 | `setType_id(String type_id)` | `public` |
| 51-53 | `getFuel_type_id()` | `public` |
| 54-56 | `setFuel_type_id(String fuel_type_id)` | `public` |

**Note:** No no-args constructor declared; Java implicitly provides one. No `equals`, `hashCode`, or `toString` overrides. Not `Serializable`.

---

### 1.3 ManufactureBean
**File:** `src/main/java/com/bean/ManufactureBean.java`
**Class:** `com.bean.ManufactureBean`
**Implements:** `java.io.Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**

| Line | Field | Type | Initial value |
|------|-------|------|---------------|
| 13 | `serialVersionUID` | `static final long` | `1390610283858544445L` |
| 14 | `id` | `String` | `null` |
| 15 | `name` | `String` | `null` |
| 16 | `company_id` | `String` | `null` |

**Methods (explicit in source):**

| Lines | Method | Visibility | Notes |
|-------|--------|------------|-------|
| 19-23 | `ManufactureBean(String id, String name, String company_id)` | `private` | `@Builder` constructor; all three fields set |

**Methods (Lombok-generated — not visible in source):**

| Generated method | Lombok source |
|-----------------|---------------|
| `ManufactureBean()` | `@NoArgsConstructor` |
| `getId()` | `@Data` |
| `setId(String)` | `@Data` |
| `getName()` | `@Data` |
| `setName(String)` | `@Data` |
| `getCompany_id()` | `@Data` |
| `setCompany_id(String)` | `@Data` |
| `equals(Object)` | `@Data` |
| `hashCode()` | `@Data` |
| `toString()` | `@Data` |
| `canEqual(Object)` | `@Data` |
| `ManufactureBean.ManufactureBeanBuilder builder()` | `@Builder` (static) |

---

## 2. Test Directory Search Results

**Test files found in** `src/test/java/`:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep results for each class name across entire test tree:**

| Search term | Matches |
|-------------|---------|
| `LicenceBean` | **0 files, 0 matches** |
| `ManuTypeFuleRelBean` | **0 files, 0 matches** |
| `ManufactureBean` | **0 files, 0 matches** |
| `security_number` | **0 files, 0 matches** |
| `licence_number` | **0 files, 0 matches** |

None of the three classes are referenced anywhere in the test suite.

---

## 3. Coverage Gaps and Findings

### A53-1 | Severity: CRITICAL | LicenceBean — zero test coverage; security_number field is untested and unprotected

`LicenceBean` has no test class and no test references whatsoever. The field `security_number` (line 16) holds a sensitive credential / government-issued identifier. Lombok's `@Data` unconditionally generates a public `getSecurity_number()` getter and includes `security_number` in `toString()` output. There are no tests verifying:
- that `security_number` is excluded from logs or serialized output,
- that the getter is absent or access-controlled,
- that equality/hashCode/toString behaviour involving `security_number` is intentional.

Without test coverage this exposure is undetected and unchallenged.

### A53-2 | Severity: CRITICAL | ManuTypeFuleRelBean — zero test coverage

`ManuTypeFuleRelBean` has no test class and no test references. All 14 hand-written public getter/setter methods are completely untested. There is no test for default field values, setter/getter round-trips, or object identity. Because this class has no `equals`, `hashCode`, or `toString`, any code that compares or logs instances will silently use `Object` identity semantics; this is untested behaviour.

### A53-3 | Severity: CRITICAL | ManufactureBean — zero test coverage

`ManufactureBean` has no test class and no test references. All Lombok-generated methods (`getId`, `setId`, `getName`, `setName`, `getCompany_id`, `setCompany_id`, `equals`, `hashCode`, `toString`, `builder`) are completely untested.

### A53-4 | Severity: HIGH | LicenceBean — `toString()` leaks `security_number` into logs; not caught by any test

Lombok `@Data` generates a `toString()` that includes every field. Because `security_number` is a field, any logger that prints a `LicenceBean` instance (e.g., via `log.debug("{}", bean)`) will emit the security number in plain text. No test asserts that `toString()` omits or masks this value. A `@ToString(exclude = "security_number")` annotation (or equivalent) is absent, and no test would catch its addition being forgotten.

### A53-5 | Severity: HIGH | LicenceBean — missing `serialVersionUID`; not caught by any test

`LicenceBean` implements `Serializable` (line 11) but declares no `serialVersionUID`. The compiler will generate one based on class structure; any change to the class (e.g., adding a field) silently changes the implicit UID, breaking deserialization of persisted objects. No test verifies that a declared `serialVersionUID` is present or that round-trip serialization produces a stable result.

### A53-6 | Severity: HIGH | ManuTypeFuleRelBean — missing `equals`, `hashCode`, `toString`; not caught by any test

`ManuTypeFuleRelBean` has no `equals`, `hashCode`, or `toString` overrides and is not annotated with Lombok `@Data`. Instances in collections (e.g., `Set`, `Map`) rely on `Object` reference identity. Any business logic that deduplicates or compares `ManuTypeFuleRelBean` instances will produce incorrect results silently. No test covers this behaviour.

### A53-7 | Severity: HIGH | ManuTypeFuleRelBean — not `Serializable`; not caught by any test

Unlike the other two beans in scope, `ManuTypeFuleRelBean` does not implement `Serializable`. If instances are placed in an `HttpSession`, passed through Struts action state, or otherwise serialized, a `NotSerializableException` will occur at runtime. No test exercises serialization of this class.

### A53-8 | Severity: MEDIUM | LicenceBean — `@Builder` constructor is `private`; builder accessibility untested

The `@Builder`-annotated constructor is `private` (line 21), which is necessary for Lombok builder correctness. However, no test verifies that the builder correctly populates all six fields (including `security_number`), that the no-args constructor leaves all fields `null`, or that the two construction paths produce equivalent beans via `equals`.

### A53-9 | Severity: MEDIUM | ManufactureBean — `@Builder` constructor is `private`; builder accessibility untested

Same pattern as A53-8 for `ManufactureBean` (line 19). No test verifies the builder populates `id`, `name`, and `company_id` correctly, that the no-args constructor leaves all fields `null`, or that builder and no-args construction paths produce equivalent `equals` results.

### A53-10 | Severity: MEDIUM | ManuTypeFuleRelBean — field `fuel_type_id` vs. `fueltypename` naming inconsistency is untested

The class mixes naming conventions: `fuel_type_id` (snake_case with underscore) alongside `fueltypename` (concatenated lowercase). The getter for `fuel_type_id` is `getFuel_type_id()` while the getter for `fueltypename` is `getFueltypename()`. This inconsistency is a maintenance hazard. No test documents or constrains the expected naming contract, so a refactor could silently break callers.

### A53-11 | Severity: LOW | LicenceBean — `expiry_date` stored as `String`; no format validation tested

`expiry_date` (line 15) is stored as a plain `String` with no format constraint. No test verifies that an invalid date string (e.g., `"not-a-date"`, `""`, `null`) is handled or rejected by the bean or its callers.

### A53-12 | Severity: LOW | ManuTypeFuleRelBean — implicit no-args constructor undocumented and untested

Java provides an implicit public no-args constructor because no explicit constructor is declared. No test confirms default field values are `null` after construction, which is the implicit contract of the class.

### A53-13 | Severity: INFO | All three classes — no test package exists for `com.bean`

The test source tree contains only `com/calibration/` and `com/util/` packages. There is no `com/bean/` test package. All bean classes in `com.bean` are structurally excluded from coverage.

---

## 4. Summary Table

| Finding | Class | Severity | Description |
|---------|-------|----------|-------------|
| A53-1 | LicenceBean | CRITICAL | Zero test coverage; `security_number` exposure unchallenged |
| A53-2 | ManuTypeFuleRelBean | CRITICAL | Zero test coverage; all 14 public methods untested |
| A53-3 | ManufactureBean | CRITICAL | Zero test coverage; all Lombok-generated methods untested |
| A53-4 | LicenceBean | HIGH | `toString()` leaks `security_number`; no test asserts masking |
| A53-5 | LicenceBean | HIGH | Missing `serialVersionUID`; no serialization round-trip test |
| A53-6 | ManuTypeFuleRelBean | HIGH | No `equals`/`hashCode`/`toString`; collection behaviour untested |
| A53-7 | ManuTypeFuleRelBean | HIGH | Not `Serializable`; session/state serialization failure untested |
| A53-8 | LicenceBean | MEDIUM | Builder and no-args construction paths untested |
| A53-9 | ManufactureBean | MEDIUM | Builder and no-args construction paths untested |
| A53-10 | ManuTypeFuleRelBean | MEDIUM | Mixed naming conventions untested and undocumented |
| A53-11 | LicenceBean | LOW | `expiry_date` stored as `String`; no format validation tested |
| A53-12 | ManuTypeFuleRelBean | LOW | Implicit no-args constructor default-value contract untested |
| A53-13 | All three | INFO | No `com.bean` test package exists in the test tree |

**Total findings: 13 (3 CRITICAL, 4 HIGH, 3 MEDIUM, 2 LOW, 1 INFO)**
