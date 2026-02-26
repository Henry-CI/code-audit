# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A46
**Files audited:**
- `src/main/java/com/bean/DriverUnitBean.java`
- `src/main/java/com/bean/DriverVehicleBean.java`
- `src/main/java/com/bean/DynamicBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 DriverUnitBean

**File:** `src/main/java/com/bean/DriverUnitBean.java`
**Class:** `com.bean.DriverUnitBean`
**Implements:** `java.io.Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `compId` | `Long` | 12 |
| `driverId` | `Long` | 13 |
| `unitId` | `Long` | 14 |
| `name` | `String` | 15 |
| `location` | `String` | 16 |
| `department` | `String` | 17 |
| `assigned` | `boolean` | 18 |
| `hours` | `int` | 19 |
| `trained` | `String` | 20 |

**Explicit methods:**

| Method | Lines | Notes |
|--------|-------|-------|
| `DriverUnitBean(Long compId, Long driverId, Long unitId, String name, String location, String department, boolean assigned, int hours, boolean trained)` | 23–33 | `private`, `@Builder`-annotated all-args constructor. Contains a boolean-to-String conversion: `trained ? "Yes" : "No"` (line 32). |

**Lombok-generated methods (not written explicitly, generated at compile time):**

| Generated method | Source annotation |
|------------------|-------------------|
| `getCompId()` | `@Data` |
| `setCompId(Long)` | `@Data` |
| `getDriverId()` | `@Data` |
| `setDriverId(Long)` | `@Data` |
| `getUnitId()` | `@Data` |
| `setUnitId(Long)` | `@Data` |
| `getName()` | `@Data` |
| `setName(String)` | `@Data` |
| `getLocation()` | `@Data` |
| `setLocation(String)` | `@Data` |
| `getDepartment()` | `@Data` |
| `setDepartment(String)` | `@Data` |
| `isAssigned()` | `@Data` |
| `setAssigned(boolean)` | `@Data` |
| `getHours()` | `@Data` |
| `setHours(int)` | `@Data` |
| `getTrained()` | `@Data` |
| `setTrained(String)` | `@Data` |
| `equals(Object)` | `@Data` |
| `hashCode()` | `@Data` |
| `toString()` | `@Data` |
| `DriverUnitBean()` | `@NoArgsConstructor` |
| `DriverUnitBeanBuilder` (inner class + `builder()`) | `@Builder` |

**`serialVersionUID`:** Not declared (missing — compiler-generated implicit value).

---

### 1.2 DriverVehicleBean

**File:** `src/main/java/com/bean/DriverVehicleBean.java`
**Class:** `com.bean.DriverVehicleBean`
**Implements:** `java.io.Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `static final long` | 15 |
| `compId` | `Long` | 17 |
| `id` | `Long` | 18 |
| `driverUnits` | `List<DriverUnitBean>` | 20 (initialised to `new ArrayList<>()`) |

**Explicit methods:**

| Method | Lines | Notes |
|--------|-------|-------|
| `DriverVehicleBean(Long id, Long compId, List<DriverUnitBean> driverUnits)` | 23–27 | `private`, `@Builder`-annotated all-args constructor. |

**Lombok-generated methods:**

| Generated method | Source annotation |
|------------------|-------------------|
| `getCompId()` | `@Data` |
| `setCompId(Long)` | `@Data` |
| `getId()` | `@Data` |
| `setId(Long)` | `@Data` |
| `getDriverUnits()` | `@Data` |
| `setDriverUnits(List<DriverUnitBean>)` | `@Data` |
| `equals(Object)` | `@Data` |
| `hashCode()` | `@Data` |
| `toString()` | `@Data` |
| `DriverVehicleBean()` | `@NoArgsConstructor` |
| `DriverVehicleBeanBuilder` (inner class + `builder()`) | `@Builder` |

---

### 1.3 DynamicBean

**File:** `src/main/java/com/bean/DynamicBean.java`
**Class:** `com.bean.DynamicBean`
**Implements:** `java.io.Serializable`
**No Lombok annotations** — all methods are hand-written.

**Fields (package-private):**

| Field | Type | Initial value | Line |
|-------|------|---------------|------|
| `name` | `String` | `""` | 6 |
| `type` | `String` | `""` | 7 |
| `value` | `String` | `""` | 8 |

**Explicit methods:**

| Method | Lines |
|--------|-------|
| `getName()` | 10–12 |
| `setName(String name)` | 13–15 |
| `getType()` | 16–18 |
| `setType(String type)` | 19–21 |
| `getValue()` | 22–24 |
| `setValue(String value)` | 25–27 |

**Missing/absent:** No explicit constructor (implicit no-args used), no `serialVersionUID`, no `equals`, `hashCode`, or `toString`.

---

## 2. Test-Directory Grep Results

Test files present under `src/test/java/`:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

Grep for `DriverUnitBean` across all test sources: **0 matches**
Grep for `DriverVehicleBean` across all test sources: **0 matches**
Grep for `DynamicBean` across all test sources: **0 matches**

**All three classes have zero test coverage.**

---

## 3. Coverage Gap Findings

---

### A46-1 | Severity: CRITICAL | DriverUnitBean — no test class exists

No test file references `DriverUnitBean`. The class has zero unit test coverage. All fields, the no-args constructor, the `@Builder` constructor, and all Lombok-generated accessors/`equals`/`hashCode`/`toString` are completely untested.

---

### A46-2 | Severity: CRITICAL | DriverVehicleBean — no test class exists

No test file references `DriverVehicleBean`. The class has zero unit test coverage. All fields, both constructors, and all Lombok-generated methods are completely untested.

---

### A46-3 | Severity: CRITICAL | DynamicBean — no test class exists

No test file references `DynamicBean`. The class has zero unit test coverage. All six hand-written accessor methods are completely untested.

---

### A46-4 | Severity: HIGH | DriverUnitBean — `trained` boolean-to-String conversion logic is untested

The `@Builder` private constructor at line 32 contains a non-trivial conditional expression:

```java
this.trained = trained ? "Yes" : "No";
```

This is the only piece of branching logic in any of the three files. Both branches (`true` → `"Yes"` and `false` → `"No"`) must be exercised independently. Without tests, it is possible that a future refactor silently corrupts this mapping. This gap is elevated above ordinary getter/setter gaps because it encodes business-visible display logic.

---

### A46-5 | Severity: HIGH | DriverUnitBean — `@Builder` constructor is `private`; builder access path is untested

The `@Builder` constructor (lines 23–33) is declared `private`. The only legitimate construction path for a fully populated `DriverUnitBean` is through the Lombok-generated `DriverUnitBeanBuilder`. Because no tests exist, it is unknown whether the builder correctly propagates all nine fields, and whether the `trained` conversion (A46-4) is reachable through the builder at all.

---

### A46-6 | Severity: HIGH | DriverVehicleBean — `@Builder` constructor is `private`; builder access path is untested

Identical pattern to A46-5: the `@Builder` private constructor (lines 23–27) is the sole path to a fully-populated `DriverVehicleBean`. The `driverUnits` field initialises to `new ArrayList<>()` via field initialiser (line 20) for the no-args constructor, but the builder path replaces this with the caller-supplied list. The behaviour when `null` is passed for `driverUnits` through the builder is untested and undocumented.

---

### A46-7 | Severity: MEDIUM | DriverUnitBean — missing `serialVersionUID`

`DriverUnitBean` implements `Serializable` but declares no explicit `serialVersionUID`. The JVM computes one from class metadata; any structural change (field added/removed, method signature changed) will silently change the implicit UID, causing `InvalidClassException` during deserialisation of persisted or network-transmitted instances. No test verifies round-trip serialisation.

---

### A46-8 | Severity: MEDIUM | DynamicBean — missing `serialVersionUID`

`DynamicBean` implements `Serializable` but declares no explicit `serialVersionUID`. Same risk as A46-7. No test verifies round-trip serialisation.

---

### A46-9 | Severity: MEDIUM | DynamicBean — fields are package-private, not `private`

Fields `name`, `type`, and `value` (lines 6–8) are declared without an access modifier, making them package-private. Code in the same package can read/write these fields directly, bypassing the accessor methods entirely. This is likely unintentional for a bean and means `setName`/`getName` etc. are not the sole access path. No tests verify encapsulation boundaries.

---

### A46-10 | Severity: MEDIUM | DriverVehicleBean — `driverUnits` null-safety through builder is untested

The no-args constructor initialises `driverUnits` to `new ArrayList<>()` (line 20). The `@Builder` constructor (line 26) assigns the caller-supplied list directly with no null guard:

```java
this.driverUnits = driverUnits;
```

If a caller invokes `DriverVehicleBean.builder().id(x).compId(y).build()` without setting `driverUnits`, Lombok's builder will pass `null`, resulting in a `null` list rather than an empty list — inconsistent with the no-args constructor behaviour. No test exercises this divergence.

---

### A46-11 | Severity: LOW | DynamicBean — no `equals`, `hashCode`, or `toString`

`DynamicBean` has no `equals` or `hashCode`, so identity equality is used. If instances are stored in sets or used as map keys this silently produces incorrect behaviour. No test verifies equality semantics.

---

### A46-12 | Severity: LOW | DriverUnitBean — `hours` field type is primitive `int`, not `Long`/`Integer`

All numeric fields in `DriverUnitBean` except `hours` use boxed `Long`. The `hours` field (line 19) is a primitive `int`. This inconsistency means `hours` cannot be `null`, cannot be distinguished from zero, and may lose precision if the database column type or DTO source ever returns a `Long`. No test checks boundary values (e.g., `0`, `Integer.MAX_VALUE`, negative hours).

---

### A46-13 | Severity: INFO | DriverUnitBean — `trained` field stored as `String`, passed as `boolean` in builder

The field `trained` (line 20) is declared `String`, but the `@Builder` constructor parameter (line 23) accepts a `boolean`. Callers using the no-args constructor + `setTrained(String)` can set arbitrary strings (e.g., `"yes"`, `"true"`, `""`) that are not `"Yes"` or `"No"`. There is no validation. This asymmetry between the two construction paths is not tested.

---

### A46-14 | Severity: INFO | No `serialVersionUID` consistency check between DriverUnitBean and DriverVehicleBean

`DriverVehicleBean` declares `serialVersionUID = -8541229534532258948L` (line 15), but `DriverUnitBean` (which is embedded in `DriverVehicleBean.driverUnits`) does not. Serialising a `DriverVehicleBean` graph that contains `DriverUnitBean` instances will still work, but any silent incompatibility on the `DriverUnitBean` side will only surface at deserialisation time. No integration-level serialisation test exists.

---

## 4. Summary Table

| Finding | Severity | Class(es) | Description |
|---------|----------|-----------|-------------|
| A46-1 | CRITICAL | DriverUnitBean | No test class exists |
| A46-2 | CRITICAL | DriverVehicleBean | No test class exists |
| A46-3 | CRITICAL | DynamicBean | No test class exists |
| A46-4 | HIGH | DriverUnitBean | `trained` boolean-to-String branch logic untested |
| A46-5 | HIGH | DriverUnitBean | Private `@Builder` constructor / builder access path untested |
| A46-6 | HIGH | DriverVehicleBean | Private `@Builder` constructor / builder access path untested |
| A46-7 | MEDIUM | DriverUnitBean | Missing `serialVersionUID` |
| A46-8 | MEDIUM | DynamicBean | Missing `serialVersionUID` |
| A46-9 | MEDIUM | DynamicBean | Fields are package-private, not `private` |
| A46-10 | MEDIUM | DriverVehicleBean | `driverUnits` null-safety divergence between constructors untested |
| A46-11 | LOW | DynamicBean | No `equals`, `hashCode`, or `toString` |
| A46-12 | LOW | DriverUnitBean | `hours` primitive `int` vs boxed `Long` inconsistency untested |
| A46-13 | INFO | DriverUnitBean | `trained` field type asymmetry between construction paths |
| A46-14 | INFO | DriverUnitBean / DriverVehicleBean | Missing `serialVersionUID` consistency in serialisation graph |

**Total findings: 14**
**CRITICAL: 3 | HIGH: 3 | MEDIUM: 4 | LOW: 2 | INFO: 2**
