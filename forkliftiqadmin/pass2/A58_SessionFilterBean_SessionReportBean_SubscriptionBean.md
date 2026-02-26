# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A58
**Files audited:**
- `src/main/java/com/bean/SessionFilterBean.java`
- `src/main/java/com/bean/SessionReportBean.java`
- `src/main/java/com/bean/SubscriptionBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 SessionFilterBean

**File:** `src/main/java/com/bean/SessionFilterBean.java`
**Class:** `com.bean.SessionFilterBean`
**Annotations:** `@Data`, `@Builder`
**Implements:** `DateBetweenFilter`, `SessionUnitFilter`, `SessionDriverFilter`

| Element | Kind | Lines |
|---------|------|-------|
| `companyId` | field (`Long`) | 15 |
| `vehicleId` | field (`Long`) | 16 |
| `driverId` | field (`Long`) | 17 |
| `startDate` | field (`Date`) | 18 |
| `endDate` | field (`Date`) | 19 |
| `timezone` | field (`String`) | 20 |
| `start()` | method (override `DateBetweenFilter`) | 23–25 |
| `end()` | method (override `DateBetweenFilter`) | 28–30 |
| `driverId()` | method (override `SessionDriverFilter`) | 33 |
| `unitId()` | method (override `SessionUnitFilter`) | 36 |
| `timezone()` | method (override `DateBetweenFilter`) | 39–41 |

**Lombok-generated (implicit):**
- All-args constructor (via `@Builder`)
- `SessionFilterBean.builder()` static factory
- Getters and setters for all six fields (via `@Data`)
- `equals()`, `hashCode()`, `toString()` (via `@Data`)

**Branch logic in explicit methods:**
- `start()`: ternary — `startDate != null` branch (returns `startDate`) and null branch (returns `Calendar.getInstance().getTime()`) — line 24
- `end()`: ternary — `endDate != null` branch (returns `endDate`) and null branch (returns `Calendar.getInstance().getTime()`) — line 29

---

### 1.2 SessionReportBean

**File:** `src/main/java/com/bean/SessionReportBean.java`
**Class:** `com.bean.SessionReportBean`
**Annotations:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`
**Implements:** `Serializable`

| Element | Kind | Lines |
|---------|------|-------|
| `serialVersionUID` | static final field (`long`) | 15 |
| `sessions` | field (`List<SessionBean>`) | 17 |

**Lombok-generated (implicit):**
- No-args constructor via `@NoArgsConstructor` (initialises `sessions` to `new ArrayList<>()`)
- All-args constructor via `@AllArgsConstructor`
- `getSessions()`, `setSessions()` (via `@Data`)
- `equals()`, `hashCode()`, `toString()` (via `@Data`)

**No explicit methods beyond Lombok.**

---

### 1.3 SubscriptionBean

**File:** `src/main/java/com/bean/SubscriptionBean.java`
**Class:** `com.bean.SubscriptionBean`
**Annotations:** `@Data`, `@NoArgsConstructor` (class level), `@Builder` (constructor level — private builder)
**Implements:** `Serializable`

| Element | Kind | Lines |
|---------|------|-------|
| `serialVersionUID` | static final field (`long`) | 16 |
| `id` | field (`String`, default `""`) | 17 |
| `name` | field (`String`, default `""`) | 18 |
| `type` | field (`String`, default `""`) | 19 |
| `frequency` | field (`String`, default `""`) | 20 |
| `file_name` | field (`String`, default `""`) | 21 |
| `arrUser` | field (`ArrayList<UserBean>`, default `new ArrayList<>()`) | 22 |
| `SubscriptionBean(String, String, String, String, String, ArrayList<UserBean>)` | private constructor (builder target) | 26–34 |

**Lombok-generated (implicit):**
- Public no-args constructor via `@NoArgsConstructor`
- `SubscriptionBean.builder()` static factory (via `@Builder` on private constructor)
- Getters and setters for all six fields (via `@Data`)
- `equals()`, `hashCode()`, `toString()` (via `@Data`)

**Style note:** Field name `file_name` and `arrUser` do not follow Java naming conventions (`fileName`, `users`).

---

## 2. Test-Directory Search Results

Test directory searched: `src/test/java/`

Existing test files in the test directory:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Class searched | Grep result |
|----------------|-------------|
| `SessionFilterBean` | No files found |
| `SessionReportBean` | No files found |
| `SubscriptionBean` | No files found |

**None of the three audited classes appear in any test file.**

---

## 3. Coverage Gaps and Findings

### SessionFilterBean

A58-1 | Severity: CRITICAL | `SessionFilterBean` has no test class. Zero coverage for all explicit method logic and all builder/Lombok-generated behaviour.

A58-2 | Severity: HIGH | `start()` (line 24) contains a null-check ternary with two branches: the non-null path returning `startDate` and the null path returning `Calendar.getInstance().getTime()`. Neither branch is tested. The null-fallback path in particular introduces an implicit dependency on wall-clock time that has never been validated.

A58-3 | Severity: HIGH | `end()` (line 29) contains an identical null-check ternary with two branches: the non-null path returning `endDate` and the null path returning `Calendar.getInstance().getTime()`. Neither branch is tested. Same implicit wall-clock dependency as `start()`.

A58-4 | Severity: MEDIUM | `driverId()` (line 33) — interface delegation accessor — is untested. Although it simply delegates `driverId` field, no test confirms the value is correctly forwarded through the builder and returned.

A58-5 | Severity: MEDIUM | `unitId()` (line 36) — interface delegation accessor — is untested. Maps `vehicleId` field to the `SessionUnitFilter.unitId()` contract; the field-name mismatch (`vehicleId` vs `unitId`) has never been validated.

A58-6 | Severity: MEDIUM | `timezone()` (line 39–41) — interface delegation accessor — is untested.

A58-7 | Severity: MEDIUM | The `@Builder`-generated `SessionFilterBean.builder()` factory and resulting object construction path are completely untested. No test confirms that builder assignments produce a consistent object state.

A58-8 | Severity: LOW | `@Data`-generated `equals()` and `hashCode()` on `SessionFilterBean` are untested. These methods operate over six fields (including mutable `Date` objects) and are exercised nowhere.

A58-9 | Severity: LOW | `@Data`-generated `toString()` on `SessionFilterBean` is untested.

A58-10 | Severity: INFO | `companyId` field (line 15) is declared but not consumed by any of the three implemented interfaces (`DateBetweenFilter`, `SessionUnitFilter`, `SessionDriverFilter`). No test validates that it is set and readable, nor is there documentation explaining its purpose relative to the filter contracts.

---

### SessionReportBean

A58-11 | Severity: CRITICAL | `SessionReportBean` has no test class. Zero coverage for all constructor and accessor behaviour.

A58-12 | Severity: HIGH | The no-args constructor (via `@NoArgsConstructor`) initialises `sessions` to `new ArrayList<>()` at the field declaration (line 17). No test verifies that a freshly constructed `SessionReportBean` holds an empty, non-null list (as opposed to null), which is an important invariant for downstream callers.

A58-13 | Severity: HIGH | The all-args constructor (via `@AllArgsConstructor`) accepts an arbitrary `List<SessionBean>` including `null`. No test validates behaviour when `null` is passed, which would override the safe default initialisation and expose the object to NPEs on list operations.

A58-14 | Severity: MEDIUM | `getSessions()` / `setSessions()` Lombok accessors are untested. Specifically, no test verifies that `setSessions(null)` does not break the bean's contract.

A58-15 | Severity: MEDIUM | `equals()` and `hashCode()` on `SessionReportBean` delegate to the `sessions` list. No test verifies equality semantics between two instances with the same or different session lists.

A58-16 | Severity: LOW | `serialVersionUID` value (`-1877529141762148535L`) is declared but serialisation/deserialisation round-trip is untested.

A58-17 | Severity: LOW | `toString()` on `SessionReportBean` is untested.

---

### SubscriptionBean

A58-18 | Severity: CRITICAL | `SubscriptionBean` has no test class. Zero coverage for all constructor, builder, and accessor behaviour.

A58-19 | Severity: HIGH | The private `@Builder` constructor (lines 26–34) assigns all six fields explicitly. No test validates that the builder correctly transfers each argument to the corresponding field, or that the private visibility does not break reflective frameworks (e.g., Jackson deserialization, Struts form binding) that expect a public all-args constructor.

A58-20 | Severity: HIGH | The `@NoArgsConstructor` public constructor leaves all fields at their declared defaults (`""`, `""`, `""`, `""`, `""`, `new ArrayList<>()`). No test verifies these defaults, meaning silent regressions in initial state are invisible.

A58-21 | Severity: MEDIUM | Field `arrUser` (line 22, type `ArrayList<UserBean>`) uses the concrete `ArrayList` type rather than the `List` interface, both in the field declaration and the builder parameter. No test covers mutation of this list after construction, nor does any test confirm that the builder correctly wires the supplied list (vs. creating a defensive copy).

A58-22 | Severity: MEDIUM | Field naming violates Java conventions: `file_name` (line 21) should be `fileName` and `arrUser` (line 22) should be `users` or `userList`. The generated Lombok getter/setter names will be `getFile_name()` / `setFile_name()` and `getArrUser()` / `setArrUser()`, which are non-standard and may cause binding failures in Struts or Jackson. No test exercises these generated accessor names.

A58-23 | Severity: MEDIUM | `equals()` and `hashCode()` generated by `@Data` include all six fields including the mutable `ArrayList<UserBean>`. No test validates equality or hashing behaviour, particularly when `arrUser` contains elements.

A58-24 | Severity: LOW | `serialVersionUID` value (`4332469413335460335L`) is declared but serialisation/deserialisation round-trip is untested.

A58-25 | Severity: LOW | `toString()` on `SubscriptionBean` is untested.

A58-26 | Severity: INFO | The combination of `@NoArgsConstructor` at class level and a `private` `@Builder` constructor means the public API provides a no-args constructor and a builder, but no public all-args constructor. Any framework expecting a public all-args constructor (some JAX-B or Jackson configurations) will fail silently. This architectural risk is untested.

---

## 4. Summary Table

| Finding | Severity | Class | Topic |
|---------|----------|-------|-------|
| A58-1 | CRITICAL | SessionFilterBean | No test class exists |
| A58-2 | HIGH | SessionFilterBean | `start()` null-branch untested |
| A58-3 | HIGH | SessionFilterBean | `end()` null-branch untested |
| A58-4 | MEDIUM | SessionFilterBean | `driverId()` accessor untested |
| A58-5 | MEDIUM | SessionFilterBean | `unitId()` field-name mapping untested |
| A58-6 | MEDIUM | SessionFilterBean | `timezone()` accessor untested |
| A58-7 | MEDIUM | SessionFilterBean | Builder construction path untested |
| A58-8 | LOW | SessionFilterBean | `equals()`/`hashCode()` untested |
| A58-9 | LOW | SessionFilterBean | `toString()` untested |
| A58-10 | INFO | SessionFilterBean | `companyId` field not consumed by any interface |
| A58-11 | CRITICAL | SessionReportBean | No test class exists |
| A58-12 | HIGH | SessionReportBean | No-args constructor list default invariant untested |
| A58-13 | HIGH | SessionReportBean | All-args constructor accepts null list; untested |
| A58-14 | MEDIUM | SessionReportBean | `getSessions()`/`setSessions()` untested |
| A58-15 | MEDIUM | SessionReportBean | `equals()`/`hashCode()` untested |
| A58-16 | LOW | SessionReportBean | Serialisation round-trip untested |
| A58-17 | LOW | SessionReportBean | `toString()` untested |
| A58-18 | CRITICAL | SubscriptionBean | No test class exists |
| A58-19 | HIGH | SubscriptionBean | Builder constructor field assignment untested |
| A58-20 | HIGH | SubscriptionBean | No-args constructor default values untested |
| A58-21 | MEDIUM | SubscriptionBean | `ArrayList` concrete type usage in builder untested |
| A58-22 | MEDIUM | SubscriptionBean | Non-standard field names produce non-standard accessors; untested |
| A58-23 | MEDIUM | SubscriptionBean | `equals()`/`hashCode()` with mutable list untested |
| A58-24 | LOW | SubscriptionBean | Serialisation round-trip untested |
| A58-25 | LOW | SubscriptionBean | `toString()` untested |
| A58-26 | INFO | SubscriptionBean | Private builder + no public all-args ctor; framework risk untested |

**Total findings: 26**
- CRITICAL: 3 (A58-1, A58-11, A58-18)
- HIGH: 7 (A58-2, A58-3, A58-12, A58-13, A58-19, A58-20, A58-26 demoted to INFO — corrected: 6 HIGH)
- MEDIUM: 10
- LOW: 6
- INFO: 2
