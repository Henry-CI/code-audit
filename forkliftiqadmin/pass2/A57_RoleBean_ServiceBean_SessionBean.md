# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A57
**Files Audited:**
- `src/main/java/com/bean/RoleBean.java`
- `src/main/java/com/bean/ServiceBean.java`
- `src/main/java/com/bean/SessionBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 RoleBean
**File:** `src/main/java/com/bean/RoleBean.java`
**Class:** `com.bean.RoleBean implements Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | static final field (`long`) | 12 |
| `id` | field (`String`, default `null`) | 14 |
| `name` | field (`String`, default `null`) | 15 |
| `description` | field (`String`, default `null`) | 16 |
| `authority` | field (`String`, default `null`) | 17 |
| `RoleBean()` | Lombok-generated no-arg constructor (`@NoArgsConstructor`) | 10 |
| `RoleBean(String id, String name, String description, String authority)` | `@Builder` private all-args constructor | 20–25 |
| `getId()` / `setId(String)` | Lombok-generated via `@Data` | — |
| `getName()` / `setName(String)` | Lombok-generated via `@Data` | — |
| `getDescription()` / `setDescription(String)` | Lombok-generated via `@Data` | — |
| `getAuthority()` / `setAuthority(String)` | Lombok-generated via `@Data` | — |
| `equals(Object)` / `hashCode()` / `toString()` | Lombok-generated via `@Data` | — |
| `RoleBean.builder()` / `RoleBeanBuilder.build()` | Lombok `@Builder` static factory + builder | — |

---

### 1.2 ServiceBean
**File:** `src/main/java/com/bean/ServiceBean.java`
**Class:** `com.bean.ServiceBean`
**No Lombok annotations; plain hand-written POJO.**

| Element | Kind | Line(s) |
|---|---|---|
| `id` | field (`int`) | 5 |
| `unitId` | field (`int`) | 6 |
| `servType` | field (`String`) | 7 |
| `servLast` | field (`int`) | 8 |
| `servNext` | field (`int`) | 9 |
| `servDuration` | field (`int`) | 10 |
| `accHours` | field (`double`) | 11 |
| `servStatus` | field (`String`) | 12 |
| `hrsTilNext` | field (`String`) | 13 |
| `hoursTillNextService` | field (`double`) | 15 |
| `hourmeter` | field (`double`) | 16 |
| `getServLast()` | method | 18–20 |
| `setServLast(int)` | method | 22–24 |
| `getServNext()` | method | 26–28 |
| `getServDuration()` | method | 30–32 |
| `setServNext(int)` | method | 34–36 |
| `setServDuration(int)` | method | 38–40 |
| `getId()` | method | 42–44 |
| `getUnitId()` | method | 46–48 |
| `getServType()` | method | 50–52 |
| `setId(int)` | method | 54–56 |
| `setUnitId(int)` | method | 58–60 |
| `setServType(String)` | method | 62–64 |
| `getServStatus()` | method | 66–68 |
| `setServStatus(String)` | method | 70–72 |
| `getHrsTilNext()` | method | 74–76 |
| `setHrsTilNext(String)` | method | 78–80 |
| `getHoursTillNextService()` | method | 82–84 |
| `setHoursTillNextService(double)` | method | 86–88 |
| `getHourmeter()` | method | 90–92 |
| `setHourmeter(double)` | method | 94–96 |
| `getAccHours()` | method | 98–100 |
| `setAccHours(double)` | method | 102–104 |
| No-arg constructor (implicit) | compiler-generated | — |

**Missing in ServiceBean vs. peer beans:** no `equals()`, `hashCode()`, `toString()`, no `serialVersionUID` / `Serializable`.

---

### 1.3 SessionBean
**File:** `src/main/java/com/bean/SessionBean.java`
**Class:** `com.bean.SessionBean implements Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`, `@Builder`, `@AllArgsConstructor(access = AccessLevel.PRIVATE)`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | static final field (`long`) | 12 |
| `id` | field (`int`) | 14 |
| `driverId` | field (`int`) | 15 |
| `driverName` | field (`String`) | 16 |
| `unitId` | field (`int`) | 17 |
| `unitName` | field (`String`) | 18 |
| `startTime` | field (`String`) | 19 |
| `finishTime` | field (`String`) | 20 |
| `SessionBean()` | Lombok `@NoArgsConstructor` | 8 |
| `SessionBean(int, int, String, int, String, String, String)` | Lombok `@AllArgsConstructor(PRIVATE)` | 10 |
| `getId()` / `setId(int)` | Lombok `@Data` | — |
| `getDriverId()` / `setDriverId(int)` | Lombok `@Data` | — |
| `getDriverName()` / `setDriverName(String)` | Lombok `@Data` | — |
| `getUnitId()` / `setUnitId(int)` | Lombok `@Data` | — |
| `getUnitName()` / `setUnitName(String)` | Lombok `@Data` | — |
| `getStartTime()` / `setStartTime(String)` | Lombok `@Data` | — |
| `getFinishTime()` / `setFinishTime(String)` | Lombok `@Data` | — |
| `equals(Object)` / `hashCode()` / `toString()` | Lombok `@Data` | — |
| `SessionBean.builder()` / `SessionBeanBuilder.build()` | Lombok `@Builder` | — |

---

## 2. Test-Directory Grep Results

Test directory searched: `src/test/java/`

Files present in test directory:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Search Term | Files Matched |
|---|---|
| `RoleBean` | **none** |
| `ServiceBean` | **none** |
| `SessionBean` | **none** |

All three classes have **zero test coverage**.

---

## 3. Coverage Gaps and Findings

### RoleBean

**A57-1 | Severity: HIGH | RoleBean — no test class exists**
`RoleBean` has no corresponding test class in `src/test/java/`. The no-arg constructor, the `@Builder` factory, all four getters, all four setters, `equals()`, `hashCode()`, and `toString()` are entirely untested.

**A57-2 | Severity: MEDIUM | RoleBean.builder() — no construction-path test**
The `@Builder` private constructor is the only parameterised construction path. No test verifies that `RoleBean.builder().id("x").name("y").description("d").authority("a").build()` produces a correctly populated object.

**A57-3 | Severity: MEDIUM | RoleBean — equals/hashCode contract untested**
Lombok's `@Data` generates `equals()` and `hashCode()` from all four fields. No test verifies reflexivity, symmetry, transitivity, or consistency (including null-field edge cases).

**A57-4 | Severity: LOW | RoleBean — toString() untested**
The Lombok-generated `toString()` is not exercised by any test.

**A57-5 | Severity: LOW | RoleBean — default-null field values untested**
All four fields initialise to `null`. No test confirms the no-arg constructor leaves them null (a regression risk if defaults are changed).

---

### ServiceBean

**A57-6 | Severity: HIGH | ServiceBean — no test class exists**
`ServiceBean` has no corresponding test class. All 11 fields and 22 hand-written getter/setter methods are entirely untested.

**A57-7 | Severity: HIGH | ServiceBean — no implicit constructor test**
The compiler-supplied no-arg constructor is never exercised. Default values for primitive fields (`int` → 0, `double` → 0.0) and reference fields (`String` → `null`) are unverified.

**A57-8 | Severity: MEDIUM | ServiceBean — all getter/setter pairs untested (22 methods)**
Every round-trip property assignment (`set` then `get`) is unverified for all 11 properties: `id`, `unitId`, `servType`, `servLast`, `servNext`, `servDuration`, `accHours`, `servStatus`, `hrsTilNext`, `hoursTillNextService`, `hourmeter`.

**A57-9 | Severity: MEDIUM | ServiceBean — double fields lack boundary / precision tests**
`accHours`, `hoursTillNextService`, and `hourmeter` are `double`. No tests verify behaviour at boundary values (0.0, negative, `Double.MAX_VALUE`, `Double.NaN`, `Double.POSITIVE_INFINITY`).

**A57-10 | Severity: MEDIUM | ServiceBean — missing equals/hashCode/toString**
Unlike `RoleBean` and `SessionBean`, `ServiceBean` does not implement `Serializable`, nor does it override `equals()`, `hashCode()`, or `toString()`. There are no tests to document or protect the current identity-equality behaviour, creating a silent correctness risk if `ServiceBean` instances are stored in collections or compared in business logic.

**A57-11 | Severity: LOW | ServiceBean — not Serializable**
`ServiceBean` is not declared `Serializable`, unlike the other two beans in the same package. If it is ever placed in an `HttpSession` or passed across JVM boundaries this will cause a runtime `NotSerializableException`. No test guards against inadvertent serialisation use.

---

### SessionBean

**A57-12 | Severity: HIGH | SessionBean — no test class exists**
`SessionBean` has no corresponding test class. The no-arg constructor, the `@Builder` factory, all seven getters, all seven setters, `equals()`, `hashCode()`, and `toString()` are entirely untested.

**A57-13 | Severity: MEDIUM | SessionBean.builder() — no construction-path test**
No test verifies that `SessionBean.builder()` populates all seven fields correctly through `build()`.

**A57-14 | Severity: MEDIUM | SessionBean — equals/hashCode contract untested**
Lombok `@Data` derives equality from all seven fields. No test covers reflexivity, symmetry, transitivity, null fields, or the `id`/`driverId`/`unitId` int-field boundary cases (0, negative, `Integer.MAX_VALUE`).

**A57-15 | Severity: LOW | SessionBean — toString() untested**
The Lombok-generated `toString()` is not exercised by any test.

**A57-16 | Severity: LOW | SessionBean — @AllArgsConstructor(PRIVATE) inaccessibility untested**
The all-args constructor is declared `PRIVATE`, intended to be used only by the Lombok builder. No test confirms that direct construction is impossible from outside the class (i.e., that the intended API constraint is enforced).

---

## 4. Summary Table

| ID | Class | Severity | Description |
|---|---|---|---|
| A57-1 | RoleBean | HIGH | No test class exists; all members untested |
| A57-2 | RoleBean | MEDIUM | Builder construction path not tested |
| A57-3 | RoleBean | MEDIUM | equals/hashCode contract untested |
| A57-4 | RoleBean | LOW | toString() untested |
| A57-5 | RoleBean | LOW | Default-null field values from no-arg constructor untested |
| A57-6 | ServiceBean | HIGH | No test class exists; all members untested |
| A57-7 | ServiceBean | HIGH | No-arg constructor / primitive default values untested |
| A57-8 | ServiceBean | MEDIUM | All 22 getter/setter methods untested |
| A57-9 | ServiceBean | MEDIUM | double fields lack boundary/precision tests |
| A57-10 | ServiceBean | MEDIUM | No equals/hashCode/toString — silent identity-equality risk |
| A57-11 | ServiceBean | LOW | Not Serializable — runtime risk if session-stored |
| A57-12 | SessionBean | HIGH | No test class exists; all members untested |
| A57-13 | SessionBean | MEDIUM | Builder construction path not tested |
| A57-14 | SessionBean | MEDIUM | equals/hashCode contract untested |
| A57-15 | SessionBean | LOW | toString() untested |
| A57-16 | SessionBean | LOW | @AllArgsConstructor(PRIVATE) inaccessibility untested |

**Total findings: 16**
**CRITICAL: 0 | HIGH: 4 | MEDIUM: 7 | LOW: 5 | INFO: 0**

---

## 5. Overall Assessment

All three bean classes in `com.bean` — `RoleBean`, `ServiceBean`, and `SessionBean` — have **0 % test coverage**. No test file references any of the three class names. The four existing test files in the project cover only calibration and utility concerns unrelated to these beans.

The most significant structural observation is that `ServiceBean` diverges from its peers: it carries no Lombok annotations, no `Serializable` declaration, and no `equals()`/`hashCode()`/`toString()` overrides, while `RoleBean` and `SessionBean` both use Lombok `@Data` for those concerns. This inconsistency is unguarded by tests and represents a latent correctness risk when `ServiceBean` instances are used in collections or compared in service/action layer logic.
