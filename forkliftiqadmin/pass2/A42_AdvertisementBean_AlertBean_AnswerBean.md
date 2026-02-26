# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A42
**Date:** 2026-02-26
**Scope:** com.bean.AdvertisementBean, com.bean.AlertBean, com.bean.AnswerBean
**Project:** forkliftiqadmin (Java / Struts / Tomcat)

---

## 1. Reading-Evidence Blocks

### 1.1 AdvertisementBean
**File:** `src/main/java/com/bean/AdvertisementBean.java`
**Class:** `com.bean.AdvertisementBean`
**Implements:** `java.io.Serializable`
**Lombok annotations:** none — all accessors hand-written

| Element | Kind | Line(s) |
|---------|------|---------|
| `serialVersionUID` | static final field (long) | 10 |
| `id` | private String field, default `null` | 12 |
| `pic` | private String field, default `null` | 13 |
| `text` | private String field, default `null` | 14 |
| `order_no` | private String field, default `null` | 15 |
| `getId()` | getter | 17–19 |
| `setId(String)` | setter | 20–22 |
| `getPic()` | getter | 23–25 |
| `setPic(String)` | setter | 26–28 |
| `getText()` | getter | 29–31 |
| `setText(String)` | setter | 32–34 |
| `getOrder_no()` | getter | 35–37 |
| `setOrder_no(String)` | setter | 38–40 |
| *(implicit)* no-arg constructor | constructor | — |

**Notes:**
- No custom logic; pure data-transfer object.
- Field names use mixed convention (`order_no` with underscore) — non-standard Java naming.
- No `equals()`, `hashCode()`, or `toString()` override.

---

### 1.2 AlertBean
**File:** `src/main/java/com/bean/AlertBean.java`
**Class:** `com.bean.AlertBean`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`, `@Builder` (on all-args private constructor)

| Element | Kind | Line(s) |
|---------|------|---------|
| `alert_id` | private String field, default `null` | 11 |
| `alert_name` | private String field, default `null` | 12 |
| `alert_type` | private String field, default `null` | 13 |
| `file_name` | private String field, default `null` | 14 |
| `frequency` | private String field, default `null` | 15 |
| `AlertBean()` | `@NoArgsConstructor` (Lombok-generated) | 8 |
| `AlertBean(String,String,String,String,String)` | `@Builder` private all-args constructor | 18–24 |
| `AlertBean.builder()` | Lombok-generated builder factory | — |
| `getAlert_id()` | `@Data`-generated getter | — |
| `setAlert_id(String)` | `@Data`-generated setter | — |
| `getAlert_name()` | `@Data`-generated getter | — |
| `setAlert_name(String)` | `@Data`-generated setter | — |
| `getAlert_type()` | `@Data`-generated getter | — |
| `setAlert_type(String)` | `@Data`-generated setter | — |
| `getFile_name()` | `@Data`-generated getter | — |
| `setFile_name(String)` | `@Data`-generated setter | — |
| `getFrequency()` | `@Data`-generated getter | — |
| `setFrequency(String)` | `@Data`-generated setter | — |
| `equals(Object)` | `@Data`-generated | — |
| `hashCode()` | `@Data`-generated | — |
| `toString()` | `@Data`-generated | — |

**Notes:**
- The `@Builder` constructor is `private`, meaning object construction is only possible via the no-arg constructor or the builder. Direct `new AlertBean(...)` is impossible from outside the class.
- `@Data` does NOT generate `@Builder`-style builder automatically; the builder here is attached to the private constructor, so `AlertBean.builder()...build()` is the intended pattern.
- Does not implement `Serializable` — inconsistent with `AdvertisementBean` and `AnswerBean`.
- No custom logic; pure data-transfer object.

---

### 1.3 AnswerBean
**File:** `src/main/java/com/bean/AnswerBean.java`
**Class:** `com.bean.AnswerBean`
**Implements:** `java.io.Serializable`
**Lombok annotations:** `@Data`, `@NoArgsConstructor`

| Element | Kind | Line(s) |
|---------|------|---------|
| `serialVersionUID` | static final field (long) | 14 |
| `id` | private String field, default `""` | 17 |
| `answer` | private String field, default `""` | 18 |
| `faulty` | private String field, default `""` | 19 |
| `quesion_id` | private String field, default `""` | 20 |
| `result_id` | private String field, default `""` | 21 |
| `AnswerBean()` | `@NoArgsConstructor` (Lombok-generated) | 9 |
| `getId()` | `@Data`-generated getter | — |
| `setId(String)` | `@Data`-generated setter | — |
| `getAnswer()` | `@Data`-generated getter | — |
| `setAnswer(String)` | `@Data`-generated setter | — |
| `getFaulty()` | `@Data`-generated getter | — |
| `setFaulty(String)` | `@Data`-generated setter | — |
| `getQuesion_id()` | `@Data`-generated getter | — |
| `setQuesion_id(String)` | `@Data`-generated setter | — |
| `getResult_id()` | `@Data`-generated getter | — |
| `setResult_id(String)` | `@Data`-generated setter | — |
| `equals(Object)` | `@Data`-generated | — |
| `hashCode()` | `@Data`-generated | — |
| `toString()` | `@Data`-generated | — |

**Notes:**
- Field `quesion_id` is a typo — should be `question_id`. This is a source-level defect baked into the public API of the bean.
- Fields default to `""` (empty string), whereas `AdvertisementBean` and `AlertBean` default to `null` — inconsistent default strategy within the same package.
- No custom logic; pure data-transfer object.

---

## 2. Test Directory Grep Results

**Test files found under `src/test/java/`:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Search results:**

| Class searched | Matches in test directory |
|----------------|--------------------------|
| `AdvertisementBean` | **0 matches** |
| `AlertBean` | **0 matches** |
| `AnswerBean` | **0 matches** |

All four existing test files target the `com.calibration` and `com.util` packages exclusively. None reference any `com.bean` class.

---

## 3. Coverage Gaps and Findings

### A42-1 | Severity: HIGH | AdvertisementBean — no test class exists

No test class exists for `AdvertisementBean`. The class has a hand-written no-arg constructor (implicit), four hand-written getters, and four hand-written setters. Because the accessors are written manually (not Lombok-generated), they carry real executable bytecode and must be exercised to achieve line or branch coverage. None of the eight accessor methods nor the default constructor are covered by any test.

Affected elements:
- Implicit no-arg constructor
- `getId()` / `setId(String)` (lines 17–22)
- `getPic()` / `setPic(String)` (lines 23–28)
- `getText()` / `setText(String)` (lines 29–34)
- `getOrder_no()` / `setOrder_no(String)` (lines 35–40)

---

### A42-2 | Severity: HIGH | AlertBean — no test class exists

No test class exists for `AlertBean`. The class relies on Lombok (`@Data`, `@NoArgsConstructor`, `@Builder`). While Lombok-generated methods are widely considered lower priority to test directly, the following require explicit test coverage:

1. **Builder pattern** — the `@Builder`-annotated private constructor at lines 18–24 assigns all five fields. There are no tests confirming the builder sets each field correctly or that a partially-constructed builder produces a valid object with correct defaults (`null`).
2. **No-arg constructor** — `@NoArgsConstructor` produces a default-field-value object; no test verifies the initial state of a freshly constructed `AlertBean`.
3. **`@Data`-generated `equals()` / `hashCode()`** — Lombok `@Data` generates structural equality; no test verifies equality semantics or hashCode contract (reflexive, symmetric, transitive, consistent).
4. **`@Data`-generated `toString()`** — not tested.

---

### A42-3 | Severity: HIGH | AnswerBean — no test class exists

No test class exists for `AnswerBean`. The class uses Lombok (`@Data`, `@NoArgsConstructor`). Gaps mirror those described for AlertBean:

1. **No-arg constructor** — no test verifies all five fields are initialised to `""` (not `null`) after construction.
2. **`@Data`-generated `equals()` / `hashCode()`** — not tested.
3. **`@Data`-generated `toString()`** — not tested.
4. All five Lombok-generated getter/setter pairs are untested.

---

### A42-4 | Severity: MEDIUM | AnswerBean — field name typo `quesion_id` baked into public API

`AnswerBean` declares the field `quesion_id` (line 20), which is a misspelling of `question_id`. Lombok generates `getQuesion_id()` and `setQuesion_id(String)` from this name. The typo is now part of the public API. No existing test would catch a regression if the field is renamed as a spelling correction, nor does any test document the current (misspelled) name as intentional. This warrants both a test that pins the current getter name and a tracked decision about whether to correct the spelling (which would be an API-breaking change).

---

### A42-5 | Severity: MEDIUM | AlertBean — does not implement Serializable; inconsistent with sibling beans

`AdvertisementBean` and `AnswerBean` both implement `java.io.Serializable`. `AlertBean` does not. In a Struts/Tomcat context where beans may be stored in `HttpSession` or passed across serialization boundaries (e.g., clustering, session replication), omitting `Serializable` can cause `java.io.NotSerializableException` at runtime. No test validates serialization behaviour for any of the three beans, nor flags the inconsistency.

---

### A42-6 | Severity: MEDIUM | AdvertisementBean — no `equals()`, `hashCode()`, or `toString()` override

`AdvertisementBean` is hand-written and does not override `equals()`, `hashCode()`, or `toString()`. It relies on `Object` identity semantics. If two `AdvertisementBean` instances representing the same advertisement are compared (e.g., in a `List.contains()` call or assertion in a test), identity comparison will produce false negatives. No test documents or enforces the intended equality semantics.

---

### A42-7 | Severity: LOW | AnswerBean — inconsistent field default strategy (`""` vs `null`)

`AnswerBean` initialises all fields to `""` (empty string), while `AdvertisementBean` and `AlertBean` initialise all fields to `null`. This inconsistency creates risk in downstream code that branches on `null` vs empty-string checks. No test exercises or documents the intended sentinel value for any field in any of the three beans.

---

### A42-8 | Severity: LOW | AdvertisementBean / AnswerBean — no test for serialization round-trip

Both `AdvertisementBean` and `AnswerBean` implement `Serializable` and declare explicit `serialVersionUID` values. No test verifies that either bean can be serialized to a byte stream and deserialized back to a structurally equal object, which is the primary contract of `Serializable`. A change to a field type or name without updating `serialVersionUID` would not be caught by the current test suite.

---

### A42-9 | Severity: INFO | All three beans — zero test coverage across the entire com.bean package

The entire `com.bean` package has 0% test coverage. The four existing test files cover only `com.calibration` and `com.util`. New test classes are required for all three beans before any coverage target can be met for this package.

---

## 4. Summary Table

| Finding | Severity | Class(es) Affected | Description |
|---------|----------|--------------------|-------------|
| A42-1 | HIGH | AdvertisementBean | No test class; all hand-written constructors, getters, setters uncovered |
| A42-2 | HIGH | AlertBean | No test class; builder, no-arg constructor, equals/hashCode/toString uncovered |
| A42-3 | HIGH | AnswerBean | No test class; no-arg constructor, equals/hashCode/toString, all accessors uncovered |
| A42-4 | MEDIUM | AnswerBean | Field name typo `quesion_id` baked into public API with no test pinning it |
| A42-5 | MEDIUM | AlertBean | Missing `Serializable` implementation; inconsistent with sibling beans; no serialization test |
| A42-6 | MEDIUM | AdvertisementBean | No `equals()`/`hashCode()`/`toString()` override; identity semantics undocumented by test |
| A42-7 | LOW | AnswerBean | Fields default to `""` not `null`; inconsistent with sibling beans; no test documents intent |
| A42-8 | LOW | AdvertisementBean, AnswerBean | No serialization round-trip test despite `implements Serializable` |
| A42-9 | INFO | All three | Entire `com.bean` package has 0% test coverage |

---

*End of audit report — Agent A42, Pass 2, Run 2026-02-26-01*
