# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A56
**Project:** forkliftiqadmin (Java / Struts / Tomcat)
**Scope:** com.bean.QuestionContentBean, com.bean.ReportFilterBean, com.bean.ResultBean
**Date:** 2026-02-26

---

## 1. Reading Evidence

### 1.1 QuestionContentBean
**File:** `src/main/java/com/bean/QuestionContentBean.java`
**Class:** `QuestionContentBean implements Serializable`
**Annotations:** `@Getter`, `@Setter`, `@Builder` (Lombok)

| Element | Line(s) | Notes |
|---------|---------|-------|
| `serialVersionUID` (field, static final long) | 13 | |
| `id` (field, String, default null) | 15 | |
| `question_id` (field, String, default null) | 16 | |
| `content` (field, String, default null) | 17 | |
| `language_id` (field, String, default null) | 18 | |
| `getId()` | Lombok-generated | via `@Getter` |
| `setId(String)` | Lombok-generated | via `@Setter` |
| `getQuestion_id()` | Lombok-generated | via `@Getter` |
| `setQuestion_id(String)` | Lombok-generated | via `@Setter` |
| `getContent()` | Lombok-generated | via `@Getter` |
| `setContent(String)` | Lombok-generated | via `@Setter` |
| `getLanguage_id()` | Lombok-generated | via `@Getter` |
| `setLanguage_id(String)` | Lombok-generated | via `@Setter` |
| `QuestionContentBean.builder()` | Lombok-generated | via `@Builder` |
| `QuestionContentBeanBuilder` (inner class) | Lombok-generated | via `@Builder` |

No hand-written methods. All logic is Lombok-generated at compile time.

---

### 1.2 ReportFilterBean
**File:** `src/main/java/com/bean/ReportFilterBean.java`
**Class:** `ReportFilterBean implements DateBetweenFilter, UnitManufactureFilter, UnitTypeFilter`
**Annotations:** `@Data`, `@AllArgsConstructor` (Lombok)

| Element | Line(s) | Notes |
|---------|---------|-------|
| `startDate` (field, Date) | 15 | |
| `endDate` (field, Date) | 16 | |
| `manuId` (field, Long) | 17 | |
| `typeId` (field, Long) | 18 | |
| `timezone` (field, String) | 19 | |
| `start()` | 22-24 | Override of DateBetweenFilter; returns startDate if non-null, else Calendar.getInstance().getTime() |
| `end()` | 27-29 | Override of DateBetweenFilter; returns endDate if non-null, else Calendar.getInstance().getTime() |
| `manufactureId()` | 32-34 | Override of UnitManufactureFilter; returns manuId |
| `type()` | 37-39 | Override of UnitTypeFilter; returns typeId |
| `timezone()` | 41-44 | Override of DateBetweenFilter; returns timezone |
| Lombok `@Data` getters/setters/equals/hashCode/toString | Lombok-generated | |
| Lombok `@AllArgsConstructor` 5-arg constructor | Lombok-generated | |

Hand-written methods with branching logic: `start()` (line 23), `end()` (line 28).

---

### 1.3 ResultBean
**File:** `src/main/java/com/bean/ResultBean.java`
**Class:** `ResultBean implements Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)

| Element | Line(s) | Notes |
|---------|---------|-------|
| `serialVersionUID` (field, static final long) | 17 | |
| `id` (field, Long, default null) | 20 | |
| `driver_id` (field, Long, default null) | 21 | |
| `unit_id` (field, String, default null) | 22 | |
| `comment` (field, String, default null) | 23 | |
| `timestamp` (field, Timestamp, default null) | 24 | |
| `time` (field, String, default null) | 25 | |
| `loc` (field, String, default null) | 26 | |
| `odemeter` (field, String, default null) | 27 | Note: misspelled; should be "odometer" |
| `arrAnswer` (field, List\<AnswerBean\>, default new ArrayList) | 28 | |
| `ans` (field, Map\<String,String\>, default new LinkedHashMap) | 29 | |
| `addAnswer(String queId, String anser)` | 32-34 | Puts into `ans` map; note: param name "anser" is misspelled |
| `addAnswer(AnswerBean answerBean)` | 36-38 | Adds to `arrAnswer` list |
| `isDriverIdSetted()` | 40-42 | Returns true if driver_id != null AND driver_id != 0L; note: "Setted" is non-standard ("Set") |
| Lombok `@Data` getters/setters/equals/hashCode/toString | Lombok-generated | |
| Lombok `@NoArgsConstructor` | Lombok-generated | |

Hand-written methods with logic: `addAnswer(String, String)`, `addAnswer(AnswerBean)`, `isDriverIdSetted()`.

---

## 2. Test Directory Grep Results

**Test files found:**
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

| Search term | Matches in test directory |
|-------------|--------------------------|
| `QuestionContentBean` | **0** |
| `ReportFilterBean` | **0** |
| `ResultBean` | **0** |

None of the three audited classes appear in any test file. The four existing test files cover unrelated classes (`UnitCalibrationImpactFilter`, `UnitCalibration`, `UnitCalibrator`, `ImpactUtil`) in the `com.calibration` and `com.util` packages.

---

## 3. Coverage Gap Findings

---

### QuestionContentBean

**A56-1 | Severity: HIGH | QuestionContentBean has zero test coverage**

No test class exists for `com.bean.QuestionContentBean`. The class uses `@Builder`, `@Getter`, and `@Setter`; while the accessors are Lombok-generated, the builder pattern and its interaction with default field values (all fields default to `null`) are not exercised. There is no test confirming that a fully-constructed instance has the expected field values, that a partially-built instance leaves unset fields as `null`, or that the class correctly serialises (it implements `Serializable`).

**A56-2 | Severity: LOW | No serialisation round-trip test for QuestionContentBean**

`QuestionContentBean implements Serializable` with an explicit `serialVersionUID` (8571950545814110379L). No test verifies that instances survive object serialisation and deserialisation with field values intact, nor that the declared `serialVersionUID` is consistent with the current field set.

---

### ReportFilterBean

**A56-3 | Severity: CRITICAL | ReportFilterBean has zero test coverage**

No test class exists for `com.bean.ReportFilterBean`. This class contains non-trivial hand-written branching logic in two override methods and is the central data-transfer object for report filtering throughout the application. Complete absence of tests means regressions in filter behaviour cannot be detected automatically.

**A56-4 | Severity: HIGH | start() null-branch is untested**

`start()` (line 22-24) contains a conditional: if `startDate` is non-null it is returned; otherwise `Calendar.getInstance().getTime()` is returned (current wall-clock time). The null/non-null branches are both untested. The fallback branch is particularly risky because it silently substitutes the current time, which can produce incorrect report ranges without any visible error.

**A56-5 | Severity: HIGH | end() null-branch is untested**

`end()` (line 27-29) has the identical conditional pattern as `start()`. Both the non-null and fallback (current time) branches are untested. Same risk profile as A56-4.

**A56-6 | Severity: MEDIUM | manufactureId() and type() delegate methods are untested**

`manufactureId()` (line 32-34) and `type()` (line 37-39) are interface-required overrides that simply expose `manuId` and `typeId` respectively. While the logic is trivial, correct wiring of field-to-method is unverified; a future refactor could silently return the wrong field.

**A56-7 | Severity: MEDIUM | timezone() delegate method is untested**

`timezone()` (line 41-44) is an interface-required override that returns `timezone`. Same concern as A56-6: field-to-method wiring is unverified.

**A56-8 | Severity: MEDIUM | No test for @AllArgsConstructor field ordering**

`@AllArgsConstructor` generates a constructor whose parameter order is determined by field declaration order (`startDate`, `endDate`, `manuId`, `typeId`, `timezone`). No test verifies that the constructor correctly assigns each argument to the corresponding field. A field reordering refactor would silently break the mapping without a failing test.

---

### ResultBean

**A56-9 | Severity: CRITICAL | ResultBean has zero test coverage**

No test class exists for `com.bean.ResultBean`. The class contains three hand-written methods including an overloaded `addAnswer` pair and a non-trivial boolean predicate `isDriverIdSetted()`. Complete absence of tests leaves all business logic unverified.

**A56-10 | Severity: HIGH | isDriverIdSetted() logic is untested**

`isDriverIdSetted()` (line 40-42) evaluates `this.driver_id != null && this.driver_id != 0L`. This predicate has four reachable states that require distinct test cases:

| driver_id value | Expected result |
|-----------------|-----------------|
| `null` | `false` |
| `0L` | `false` |
| any positive non-zero Long | `true` |
| any negative Long | `true` (potentially surprising) |

None of these cases are tested. The comparison `this.driver_id != 0L` uses reference inequality on a boxed `Long`, not `.equals()`. For `Long` values outside the JVM cache range (-128 to 127), this comparison is unreliable; since `0L` is within the cache range the current code is functionally correct, but the latent intent is obscured and no test guards against a future change to `==` with a value outside the cache range.

**A56-11 | Severity: HIGH | addAnswer(String, String) is untested**

`addAnswer(String queId, String anser)` (line 32-34) inserts into the `ans` LinkedHashMap. No test verifies: (a) that the key-value pair is correctly stored; (b) that insertion order is preserved (LinkedHashMap property); (c) that overwriting a duplicate key replaces the value; or (d) that the map is initially empty on a fresh instance.

**A56-12 | Severity: HIGH | addAnswer(AnswerBean) is untested**

`addAnswer(AnswerBean answerBean)` (line 36-38) appends to the `arrAnswer` ArrayList. No test verifies: (a) that the bean is correctly added; (b) that ordering is preserved across multiple calls; or (c) that the list is initially empty on a fresh instance.

**A56-13 | Severity: MEDIUM | No test for overloaded addAnswer method disambiguation**

The two `addAnswer` overloads operate on completely separate collections (`ans` map vs. `arrAnswer` list). No test confirms that calling one overload does not affect the collection managed by the other, and that both collections can hold data simultaneously.

**A56-14 | Severity: MEDIUM | No serialisation round-trip test for ResultBean**

`ResultBean implements Serializable` with an explicit `serialVersionUID` (8057837640488605051L). No test verifies serialisation/deserialisation fidelity, particularly for the `ArrayList` and `LinkedHashMap` fields that hold mutable collection state.

**A56-15 | Severity: LOW | Field naming defects are undetected by tests**

Two field-level naming defects exist with no test pressure to expose or prevent them:
- `odemeter` (line 27): misspelled; should be `odometer`. The Lombok-generated getter/setter will be `getOdemeter()`/`setOdemeter()`, propagating the typo to all callers.
- `quesion_id` in the referenced `AnswerBean` class (line 19 of AnswerBean.java): misspelled; should be `question_id`. Tests that assert getter/setter names would surface these defects.

**A56-16 | Severity: LOW | Method naming defect is undetected by tests**

`isDriverIdSetted()` (line 40): "Setted" is not standard English (correct form: "Set"). The method name `isDriverIdSet()` is the conventional form. With no test referencing this method by name, the misnaming is invisible and may cause API confusion for downstream consumers.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A56-1 | HIGH | QuestionContentBean | Zero test coverage |
| A56-2 | LOW | QuestionContentBean | No serialisation round-trip test |
| A56-3 | CRITICAL | ReportFilterBean | Zero test coverage |
| A56-4 | HIGH | ReportFilterBean | `start()` null-branch untested |
| A56-5 | HIGH | ReportFilterBean | `end()` null-branch untested |
| A56-6 | MEDIUM | ReportFilterBean | `manufactureId()` and `type()` delegate methods untested |
| A56-7 | MEDIUM | ReportFilterBean | `timezone()` delegate method untested |
| A56-8 | MEDIUM | ReportFilterBean | `@AllArgsConstructor` field-ordering unverified |
| A56-9 | CRITICAL | ResultBean | Zero test coverage |
| A56-10 | HIGH | ResultBean | `isDriverIdSetted()` logic untested (4 distinct states) |
| A56-11 | HIGH | ResultBean | `addAnswer(String, String)` untested |
| A56-12 | HIGH | ResultBean | `addAnswer(AnswerBean)` untested |
| A56-13 | MEDIUM | ResultBean | Overloaded `addAnswer` collection isolation unverified |
| A56-14 | MEDIUM | ResultBean | No serialisation round-trip test |
| A56-15 | LOW | ResultBean | Field naming defects undetected (`odemeter`, `quesion_id` in AnswerBean) |
| A56-16 | LOW | ResultBean | Method naming defect undetected (`isDriverIdSetted`) |

**Totals:** 2 CRITICAL, 6 HIGH, 5 MEDIUM, 3 LOW
**Overall coverage for audited classes:** 0% (no test files reference any of the three classes)
