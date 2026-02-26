# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A43
**Files audited:**
- `src/main/java/com/bean/AnswerTypeBean.java`
- `src/main/java/com/bean/AttachmentBean.java`
- `src/main/java/com/bean/ChecklistBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 AnswerTypeBean

**File:** `src/main/java/com/bean/AnswerTypeBean.java`
**Package:** `com.bean`
**Class:** `AnswerTypeBean implements Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | static final long field | 10 |
| `id` | private String field (init null) | 12 |
| `name` | private String field (init null) | 13 |
| `getId()` | public method, returns String | 15-17 |
| `setId(String id)` | public method, void | 18-20 |
| `getName()` | public method, returns String | 21-23 |
| `setName(String name)` | public method, void | 24-26 |

Implements: `java.io.Serializable`
No constructors defined (implicit no-arg constructor only).
No business logic beyond standard getter/setter pattern.

---

### 1.2 AttachmentBean

**File:** `src/main/java/com/bean/AttachmentBean.java`
**Package:** `com.bean`
**Class:** `AttachmentBean implements Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | static final long field | 10 |
| `id` | private String field (init null) | 12 |
| `name` | private String field (init null) | 13 |
| `getId()` | public method, returns String | 14-16 |
| `setId(String id)` | public method, void | 17-19 |
| `getName()` | public method, returns String | 20-22 |
| `setName(String name)` | public method, void | 23-25 |

Implements: `java.io.Serializable`
No constructors defined (implicit no-arg constructor only).
Structurally identical to `AnswerTypeBean`.

---

### 1.3 ChecklistBean

**File:** `src/main/java/com/bean/ChecklistBean.java`
**Package:** `com.bean`
**Class:** `ChecklistBean` (no interface/superclass)

| Element | Kind | Line(s) |
|---|---|---|
| `equipId` | private int field (default 0) | 5 |
| `driverBased` | private boolean field (default false) | 6 |
| `getEquipId()` | public method, returns int | 8-10 |
| `setEquipId(int equipId)` | public method, void | 11-13 |
| `isDriverBased()` | public method, returns boolean | 14-16 |
| `setDriverBased(boolean driverBased)` | public method, void | 17-19 |

No `Serializable`. No constructors defined (implicit no-arg constructor only).
No business logic beyond standard getter/setter pattern.

---

## 2. Test-Directory Grep Results

**Search command:** grep for `AnswerTypeBean`, `AttachmentBean`, `ChecklistBean` across all files under `src/test/java/`.

**Test files present:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Result:** Zero matches for any of the three class names in any test file. No dedicated test class exists for any of the three beans.

---

## 3. Coverage Gaps

### AnswerTypeBean

| Method / Behaviour | Covered? |
|---|---|
| Default construction (`new AnswerTypeBean()`) | No |
| `getId()` returns null on fresh instance | No |
| `getName()` returns null on fresh instance | No |
| `setId()` / `getId()` round-trip | No |
| `setName()` / `getName()` round-trip | No |
| `setId(null)` accepted without exception | No |
| `setName(null)` accepted without exception | No |
| `Serializable` contract (serialise + deserialise) | No |

### AttachmentBean

| Method / Behaviour | Covered? |
|---|---|
| Default construction (`new AttachmentBean()`) | No |
| `getId()` returns null on fresh instance | No |
| `getName()` returns null on fresh instance | No |
| `setId()` / `getId()` round-trip | No |
| `setName()` / `getName()` round-trip | No |
| `setId(null)` accepted without exception | No |
| `setName(null)` accepted without exception | No |
| `Serializable` contract (serialise + deserialise) | No |

### ChecklistBean

| Method / Behaviour | Covered? |
|---|---|
| Default construction (`new ChecklistBean()`) | No |
| `getEquipId()` returns 0 on fresh instance | No |
| `isDriverBased()` returns false on fresh instance | No |
| `setEquipId()` / `getEquipId()` round-trip | No |
| `setDriverBased()` / `isDriverBased()` round-trip | No |
| `setDriverBased(true)` then `setDriverBased(false)` toggle | No |
| Missing `Serializable` (potential defect vs. sibling beans) | No |

---

## 4. Findings

A43-1 | Severity: CRITICAL | `AnswerTypeBean` has zero test coverage. No test class exists anywhere in the test tree (`src/test/java/`) that references `AnswerTypeBean`. All methods — `getId()`, `setId()`, `getName()`, `setName()` — are completely untested.

A43-2 | Severity: CRITICAL | `AttachmentBean` has zero test coverage. No test class exists anywhere in the test tree that references `AttachmentBean`. All methods — `getId()`, `setId()`, `getName()`, `setName()` — are completely untested.

A43-3 | Severity: CRITICAL | `ChecklistBean` has zero test coverage. No test class exists anywhere in the test tree that references `ChecklistBean`. All methods — `getEquipId()`, `setEquipId()`, `isDriverBased()`, `setDriverBased()` — are completely untested.

A43-4 | Severity: HIGH | No getter-null-default assertions exist for any of the three beans. On a freshly constructed instance, `AnswerTypeBean.getId()` and `AnswerTypeBean.getName()` should return `null` (as initialised); the same applies to `AttachmentBean`. `ChecklistBean.getEquipId()` should return `0` and `isDriverBased()` should return `false`. None of these default-state invariants are verified.

A43-5 | Severity: HIGH | No getter/setter round-trip tests exist for any field across all three beans. Setter-then-getter pairs for `id`, `name` (both String beans) and `equipId`, `driverBased` (`ChecklistBean`) are untested, meaning field assignment correctness is never verified.

A43-6 | Severity: HIGH | `Serializable` contract is untested for `AnswerTypeBean` and `AttachmentBean`. Both classes implement `java.io.Serializable` and declare explicit `serialVersionUID` values, indicating intent for serialisation. No test verifies that an instance can be serialised to a byte stream and deserialised back with field values preserved.

A43-7 | Severity: MEDIUM | Null-value setter behaviour is untested for `AnswerTypeBean` and `AttachmentBean`. Both beans initialise `id` and `name` to `null` and expose public setters. No test confirms that calling `setId(null)` or `setName(null)` on an already-populated instance correctly re-assigns the field to `null` without throwing a `NullPointerException`.

A43-8 | Severity: MEDIUM | `setDriverBased()` toggle behaviour is untested in `ChecklistBean`. No test verifies that the boolean field can be toggled from `true` back to `false` (and vice versa), which is a meaningful state transition for a flag field used in checklist business logic.

A43-9 | Severity: LOW | `ChecklistBean` does not implement `Serializable`, unlike its sibling beans `AnswerTypeBean` and `AttachmentBean`. This inconsistency is untested and undetected. If `ChecklistBean` instances are ever placed in an HTTP session or otherwise serialised (common in Struts/Tomcat environments), a `NotSerializableException` will be thrown at runtime. No test exercises this code path.

A43-10 | Severity: INFO | The overall test suite contains only 4 test classes (`UnitCalibrationImpactFilterTest`, `UnitCalibrationTest`, `UnitCalibratorTest`, `ImpactUtilTest`), all of which target the `com.calibration` and `com.util` packages exclusively. The `com.bean` package has no corresponding test package directory, indicating a systemic gap in bean-layer coverage, not an isolated omission.
