# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A50
**Files Audited:**
- `src/main/java/com/bean/ImpactReportBean.java`
- `src/main/java/com/bean/ImpactReportFilterBean.java`
- `src/main/java/com/bean/ImpactReportGroupBean.java`

---

## 1. Reading Evidence

### 1.1 ImpactReportBean

**File:** `src/main/java/com/bean/ImpactReportBean.java`
**Class:** `ImpactReportBean` (line 14)
**Implements:** `Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

| Member | Kind | Line |
|---|---|---|
| `serialVersionUID` | static final long field | 16 |
| `groups` | field `List<ImpactReportGroupBean>` (init to `new ArrayList<>()`) | 18 |
| `ImpactReportBean()` | no-arg constructor (Lombok) | 12 |
| `ImpactReportBean(List<ImpactReportGroupBean>)` | all-args constructor (Lombok) | 13 |
| `getGroups()` | accessor (Lombok `@Data`) | generated |
| `setGroups(List<ImpactReportGroupBean>)` | mutator (Lombok `@Data`) | generated |
| `equals(Object)` | Lombok `@Data` | generated |
| `hashCode()` | Lombok `@Data` | generated |
| `toString()` | Lombok `@Data` | generated |

---

### 1.2 ImpactReportFilterBean

**File:** `src/main/java/com/bean/ImpactReportFilterBean.java`
**Class:** `ImpactReportFilterBean` (line 12)
**Extends:** `ReportFilterBean`
**Implements:** `ImpactLevelFilter`
**Lombok annotations:** `@Data`, `@EqualsAndHashCode(callSuper = true)`, `@Builder` (on constructor)

| Member | Kind | Line |
|---|---|---|
| `impactLevel` | field `ImpactLevel` | 13 |
| `ImpactReportFilterBean(Date, Date, Long, Long, ImpactLevel, String)` | `@Builder` constructor | 16-19 |
| `impactLevel()` | `@Override` from `ImpactLevelFilter` — returns `impactLevel` field | 22-24 |
| `getImpactLevel()` | accessor (Lombok `@Data`) | generated |
| `setImpactLevel(ImpactLevel)` | mutator (Lombok `@Data`) | generated |
| `equals(Object)` | Lombok `@EqualsAndHashCode(callSuper=true)` (includes superclass fields) | generated |
| `hashCode()` | Lombok `@EqualsAndHashCode(callSuper=true)` | generated |
| `toString()` | Lombok `@Data` | generated |

Inherited from `ReportFilterBean` (via `@Data` / `@AllArgsConstructor`):
- fields: `startDate`, `endDate`, `manuId`, `typeId`, `timezone`
- methods: `start()`, `end()`, `manufactureId()`, `type()`, `timezone()`

---

### 1.3 ImpactReportGroupBean

**File:** `src/main/java/com/bean/ImpactReportGroupBean.java`
**Class:** `ImpactReportGroupBean` (line 14)
**Implements:** `Serializable`, `Comparable<ImpactReportGroupBean>`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`, `@Builder` (on private constructor)

| Member | Kind | Line |
|---|---|---|
| `serialVersionUID` | static final long field | 16 |
| `manufacturer` | field `String` | 18 |
| `unitName` | field `String` | 19 |
| `entries` | field `List<ImpactReportGroupEntryBean>` (init to `new ArrayList<>()`) | 21 |
| `ImpactReportGroupBean()` | no-arg constructor (Lombok `@NoArgsConstructor`) | 13 |
| `ImpactReportGroupBean(String, String)` | private `@Builder` constructor | 25-28 |
| `addEntry(ImpactReportGroupEntryBean)` | public method — appends to `entries` list | 30-32 |
| `compareTo(ImpactReportGroupBean)` | `@Override` from `Comparable` — sums `manufacturer` and `unitName` comparisons | 35-37 |
| `getManufacturer()` | accessor (Lombok `@Data`) | generated |
| `setManufacturer(String)` | mutator (Lombok `@Data`) | generated |
| `getUnitName()` | accessor (Lombok `@Data`) | generated |
| `setUnitName(String)` | mutator (Lombok `@Data`) | generated |
| `getEntries()` | accessor (Lombok `@Data`) | generated |
| `setEntries(List<ImpactReportGroupEntryBean>)` | mutator (Lombok `@Data`) | generated |
| `equals(Object)` | Lombok `@Data` | generated |
| `hashCode()` | Lombok `@Data` | generated |
| `toString()` | Lombok `@Data` | generated |

---

## 2. Test Directory Search Results

Test directory searched: `src/test/java/`

Existing test files:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Search term | Files found |
|---|---|
| `ImpactReportBean` | none |
| `ImpactReportFilterBean` | none |
| `ImpactReportGroupBean` | none |

**Result: Zero test coverage exists for all three audited classes.**

---

## 3. Coverage Gaps and Findings

### A50-1 | Severity: CRITICAL | ImpactReportBean — no test class exists

No test class exists for `ImpactReportBean`. The class has zero test coverage. All Lombok-generated behaviour (no-arg constructor, all-args constructor, `getGroups`, `setGroups`, `equals`, `hashCode`, `toString`) and the default field initialisation (`groups` initialised to `new ArrayList<>()` in the no-args path) are entirely untested.

---

### A50-2 | Severity: CRITICAL | ImpactReportFilterBean — no test class exists

No test class exists for `ImpactReportFilterBean`. The class has zero test coverage. All behaviour is untested, including:
- The `@Builder` constructor (lines 16-19) that delegates to `super(startDate, endDate, manuId, typeId, timezone)` and sets `this.impactLevel`.
- The `impactLevel()` interface method (lines 22-24) that returns the stored `ImpactLevel`.
- The `@EqualsAndHashCode(callSuper = true)` contract, which includes inherited fields from `ReportFilterBean` — incorrect superclass chaining would go undetected.

---

### A50-3 | Severity: CRITICAL | ImpactReportGroupBean — no test class exists

No test class exists for `ImpactReportGroupBean`. The class has zero test coverage. All behaviour is untested, including:
- `addEntry(ImpactReportGroupEntryBean)` (lines 30-32).
- `compareTo(ImpactReportGroupBean)` (lines 35-37).
- The private `@Builder` constructor (lines 25-28).
- Default field initialisation (`entries` initialised to `new ArrayList<>()`).

---

### A50-4 | Severity: HIGH | ImpactReportGroupBean.compareTo — logic defect not caught by tests

`compareTo` (line 36) is implemented as:

```java
return this.manufacturer.compareTo(o.manufacturer) + this.unitName.compareTo(o.unitName);
```

The `Comparable` contract requires a negative/zero/positive result that consistently reflects ordering. Summing two `String.compareTo` results violates this contract: two individually non-zero comparisons can cancel to zero (implying equality) when the objects are not equal, breaking sort stability and `TreeSet`/`TreeMap` correctness. This defect is completely undetected because no test exercises `compareTo`. The correct implementation must establish a primary/secondary sort (e.g., compare manufacturer first; if equal, compare unitName).

---

### A50-5 | Severity: HIGH | ImpactReportGroupBean.compareTo — NullPointerException risk not caught by tests

`compareTo` (line 36) calls `this.manufacturer.compareTo(...)` and `this.unitName.compareTo(...)` without null-guards. Because `@NoArgsConstructor` is present (line 13) and both fields are `String` (no `@NonNull`), either field may be null after no-arg construction. Calling `compareTo` on a bean with a null field causes a `NullPointerException`. No test exists to verify null-safe behaviour or document that nulls are explicitly prohibited.

---

### A50-6 | Severity: HIGH | ImpactReportFilterBean — callSuper equals/hashCode untested

`@EqualsAndHashCode(callSuper = true)` means the generated `equals` and `hashCode` methods incorporate all five superclass fields (`startDate`, `endDate`, `manuId`, `typeId`, `timezone`) in addition to `impactLevel`. This cross-class contract is complex and cannot be verified without tests. Incorrect superclass field inclusion or exclusion would silently produce wrong collection behaviour (e.g., duplicate entries in a `HashSet` or missed map lookups).

---

### A50-7 | Severity: MEDIUM | ImpactReportBean — no-arg constructor default field initialisation untested

The field declaration `private List<ImpactReportGroupBean> groups = new ArrayList<>()` (line 18) is not exercised by any test. When Lombok's `@NoArgsConstructor` is used, the field initialiser runs. When `@AllArgsConstructor` is used, the caller supplies the list. A test should confirm that the no-arg path returns a non-null, mutable, empty list rather than null.

---

### A50-8 | Severity: MEDIUM | ImpactReportFilterBean — null ImpactLevel not tested

The `@Builder` constructor accepts `impactLevel` without a null check. Passing `null` stores it and `impactLevel()` returns `null`. Downstream consumers of the `ImpactLevelFilter` interface may not handle a null return. No test documents or exercises the null-impact-level case.

---

### A50-9 | Severity: MEDIUM | ImpactReportGroupBean — addEntry does not guard against null entries

`addEntry(ImpactReportGroupEntryBean impactReportModelEntry)` (lines 30-32) calls `this.entries.add(impactReportModelEntry)` without a null check. Passing null succeeds silently and can cause downstream `NullPointerException` when iterating entries. No test verifies the null-input behaviour or confirms it is intentionally permissive.

---

### A50-10 | Severity: LOW | ImpactReportBean — Serializable without serialVersionUID test

`ImpactReportBean` declares `serialVersionUID = 2904473942126123445L` (line 16) and `ImpactReportGroupBean` declares `serialVersionUID = 4050487266714624293L` (line 16). No test serialises and deserialises instances to confirm round-trip fidelity. If fields are added or reordered without updating the UID, silent data corruption occurs during deserialisation.

---

### A50-11 | Severity: LOW | ImpactReportFilterBean — no no-arg constructor, builder is only construction path

`ImpactReportFilterBean` has no `@NoArgsConstructor`, so the only construction path is the `@Builder`-backed constructor. There is no test that demonstrates the builder pattern producing a correctly populated instance, including the superclass delegation via `super(...)` (line 17). A test confirming the builder populates all inherited fields is absent.

---

### A50-12 | Severity: INFO | ImpactReportGroupBean — private @Builder constructor inaccessible from test scope

The `@Builder` constructor (line 25) is `private`. The Lombok-generated builder class itself is public, but the constructor it delegates to is private. Tests must use the builder pattern (`ImpactReportGroupBean.builder().manufacturer(...).unitName(...).build()`). No test exercises this path to confirm the builder correctly assigns fields and leaves `entries` at its default `new ArrayList<>()` value.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A50-1 | CRITICAL | ImpactReportBean | No test class exists — zero coverage |
| A50-2 | CRITICAL | ImpactReportFilterBean | No test class exists — zero coverage |
| A50-3 | CRITICAL | ImpactReportGroupBean | No test class exists — zero coverage |
| A50-4 | HIGH | ImpactReportGroupBean | `compareTo` sums two `String.compareTo` results — violates Comparable contract |
| A50-5 | HIGH | ImpactReportGroupBean | `compareTo` NPE risk when `manufacturer` or `unitName` is null |
| A50-6 | HIGH | ImpactReportFilterBean | `callSuper` equals/hashCode contract untested |
| A50-7 | MEDIUM | ImpactReportBean | No-arg constructor default list initialisation untested |
| A50-8 | MEDIUM | ImpactReportFilterBean | Null `ImpactLevel` accepted silently, no test documents intent |
| A50-9 | MEDIUM | ImpactReportGroupBean | `addEntry` accepts null without guard, no test covers this |
| A50-10 | LOW | ImpactReportBean / ImpactReportGroupBean | No serialisation round-trip test |
| A50-11 | LOW | ImpactReportFilterBean | Builder-only construction with super-delegation not exercised by any test |
| A50-12 | INFO | ImpactReportGroupBean | Private `@Builder` constructor path not exercised by any test |
