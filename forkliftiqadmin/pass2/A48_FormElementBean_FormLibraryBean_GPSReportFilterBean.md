# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A48
**Files audited:**
- `src/main/java/com/bean/FormElementBean.java`
- `src/main/java/com/bean/FormLibraryBean.java`
- `src/main/java/com/bean/GPSReportFilterBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 FormElementBean
**File:** `src/main/java/com/bean/FormElementBean.java`
**Class:** `com.bean.FormElementBean implements Serializable`

| Element | Kind | Line(s) |
|---------|------|---------|
| `serialVersionUID` | static final field (long) | 11 |
| `id` | private field (String, default `""`) | 12 |
| `name` | private field (String, default `""`) | 13 |
| `lable` | private field (String, default `""`) — note misspelling | 14 |
| `type` | private field (String, default `""`) | 15 |
| `value` | private field (String, default `""`) | 16 |
| `style` | private field (String, default `""`) | 17 |
| `position` | package-private field (int) | 18 |
| `getId()` | public method | 21–23 |
| `setId(String)` | public method | 24–26 |
| `getPosition()` | public method | 28–30 |
| `setPosition(int)` | public method | 31–33 |
| `getName()` | public method | 34–36 |
| `setName(String)` | public method | 37–39 |
| `getLable()` | public method | 40–42 |
| `setLable(String)` | public method | 43–45 |
| `getType()` | public method | 46–48 |
| `setType(String)` | public method | 49–51 |
| `getValue()` | public method | 52–54 |
| `setValue(String)` | public method | 55–57 |
| `render()` | public method — returns `""` unconditionally | 58–60 |
| `getStyle()` | public method | 61–63 |
| `setStyle(String)` | public method | 64–66 |

---

### 1.2 FormLibraryBean
**File:** `src/main/java/com/bean/FormLibraryBean.java`
**Class:** `com.bean.FormLibraryBean implements Serializable`

| Element | Kind | Line(s) |
|---------|------|---------|
| `serialVersionUID` | static final field (long) | 13 |
| `id` | private field (String, default `null`) | 17 |
| `type` | private field (String, default `null`) | 18 |
| `question_id` | private field (String, default `null`) | 19 |
| `form_object` | private field (FormBuilderBean, eagerly initialised) | 20 |
| `getForm_object()` | public method — returns deserialized `FormBuilderBean` | 23–25 |
| `setForm_content(byte[])` | public method — delegates to `getFormBuilderBean()` | 28–30 |
| `getId()` | public method | 31–33 |
| `setId(String)` | public method | 34–36 |
| `getType()` | public method | 38–40 |
| `setType(String)` | public method | 41–43 |
| `getQuestion_id()` | public method | 44–46 |
| `setQuestion_id(String)` | public method | 47–49 |
| `getByteArrayObject(FormBuilderBean)` | public method — serializes to `byte[]` via `ObjectOutputStream` | 52–66 |
| `getFormBuilderBean(byte[])` | public method — deserializes via `ObjectInputStream.readObject()` | 69–84 |

**Imports used:** `ByteArrayInputStream`, `ByteArrayOutputStream`, `ObjectInputStream`, `ObjectOutputStream`, `Serializable`.

---

### 1.3 GPSReportFilterBean
**File:** `src/main/java/com/bean/GPSReportFilterBean.java`
**Class:** `com.bean.GPSReportFilterBean extends ReportFilterBean`
**Lombok annotations:** `@Data`, `@EqualsAndHashCode(callSuper = true)`

| Element | Kind | Line(s) |
|---------|------|---------|
| `GPSReportFilterBean(Date, Date, Long, Long, int)` | `@Builder`-annotated constructor — calls `super(startDate, endDate, manuId, typeId, "")` | 15–17 |

**No additional fields declared** (all data fields are inherited from `ReportFilterBean`).

**Inherited from `ReportFilterBean` (relevant to coverage):**

| Element | Kind | Line(s) in ReportFilterBean |
|---------|------|----------------------------|
| `startDate` | private field (Date) | 15 |
| `endDate` | private field (Date) | 16 |
| `manuId` | private field (Long) | 17 |
| `typeId` | private field (Long) | 18 |
| `timezone` | private field (String) | 19 |
| `start()` | override — null-guards `startDate` | 22–24 |
| `end()` | override — null-guards `endDate` | 27–29 |
| `manufactureId()` | override | 32–34 |
| `type()` | override | 37–39 |
| `timezone()` | override | 42–44 |

Note: `GPSReportFilterBean`'s constructor passes a hard-coded empty string `""` for `timezone` and ignores the `unitId` parameter entirely.

---

## 2. Test-Directory Grep Results

Test directory scanned: `src/test/java/`

Existing test files (complete list):
```
com/calibration/UnitCalibrationImpactFilterTest.java
com/calibration/UnitCalibrationTest.java
com/calibration/UnitCalibratorTest.java
com/util/ImpactUtilTest.java
```

Grep results for each audited class name:

| Search term | Matches in test directory |
|-------------|--------------------------|
| `FormElementBean` | **0** |
| `FormLibraryBean` | **0** |
| `GPSReportFilterBean` | **0** |
| `getByteArrayObject` | **0** |
| `getFormBuilderBean` | **0** |
| `setForm_content` | **0** |
| `render()` | **0** |

**All three classes have zero test coverage.**

---

## 3. Findings

---

### A48-1 | Severity: CRITICAL | FormLibraryBean — untested unsafe deserialization via ObjectInputStream.readObject()

`getFormBuilderBean(byte[])` (lines 69–84) deserializes an arbitrary `byte[]` payload using raw `ObjectInputStream.readObject()` with no allowlist, no class filter (no `ObjectInputFilter`/`resolveClass` override), and no integrity verification. The calling method `setForm_content(byte[])` (line 28) passes database-sourced bytes directly into this path.

This is a textbook insecure deserialization vulnerability (CWE-502 / OWASP A08). If an attacker can influence the byte content stored in the database column — or if the byte array is ever exposed to a network input path — arbitrary gadget-chain execution becomes possible. No test exercises this path at all, meaning no guard rails (input validation, class filtering, exception handling adequacy) have ever been verified.

**Untested behaviors that must be covered:**
- Valid round-trip: `getByteArrayObject()` output fed into `getFormBuilderBean()` returns an equal object.
- Null input: `getFormBuilderBean(null)` — current code will throw `NullPointerException` inside `ByteArrayInputStream` constructor; the catch block catches `Exception` and silently returns a default `FormBuilderBean`. This silent swallowing is itself a defect.
- Corrupted/truncated bytes: deserialization of malformed data.
- Empty byte array: `new byte[0]` — causes `java.io.EOFException`, silently swallowed.
- Class-not-found scenario.

---

### A48-2 | Severity: CRITICAL | FormLibraryBean — exception swallowing in both serialization methods hides data-loss failures silently

`getByteArrayObject()` (lines 61–64): on any `Exception`, prints stack trace and returns `null`. Callers receive a `null` `byte[]` with no indication of failure.

`getFormBuilderBean()` (lines 79–81): on any `Exception`, prints stack trace and returns a freshly constructed, empty `FormBuilderBean`. Callers cannot distinguish a successful deserialization from a failed one. Stored form data is silently discarded.

Both behaviors are completely untested. No test verifies that callers detect or handle failure modes; no test asserts that the exception is propagated or logged via any structured mechanism.

---

### A48-3 | Severity: HIGH | FormElementBean — render() is a stub returning empty string, with no tests

`render()` (lines 58–60) is declared as a public API method that returns `""` unconditionally. This method exists specifically to be overridden or to generate UI output. Its current behavior (empty output always) is likely a defect or incomplete implementation. No test verifies:
- That the return value is empty (even to document the stub contract).
- That subclass overrides produce correct output.
- Any rendering logic that may be expected by callers.

---

### A48-4 | Severity: HIGH | GPSReportFilterBean — unitId constructor parameter is silently dropped

The `@Builder` constructor signature (line 15) accepts `int unitId` but never passes it to `super()` (line 16) or stores it. The `unitId` value is silently discarded on every instantiation. No test verifies this behavior, meaning there is no documentation of whether this is intentional design or a regression.

Additionally, `timezone` is always hard-coded to `""` (empty string) in the `super()` call, overriding any caller intent. No test verifies this constraint or its downstream effects (e.g., that `timezone()` always returns `""`).

---

### A48-5 | Severity: HIGH | GPSReportFilterBean — inherited null-guard branches in ReportFilterBean.start() and end() are untested via this subclass

`ReportFilterBean.start()` (line 23) returns `Calendar.getInstance().getTime()` when `startDate == null`. `end()` (line 28) does the same for `endDate`. These branches exist to prevent NullPointerExceptions in report query construction, but since `GPSReportFilterBean` has zero tests, neither the null-date branch nor the non-null branch has ever been exercised through this concrete type. A query built with a silently substituted current time instead of an explicit null would produce incorrect report data.

---

### A48-6 | Severity: MEDIUM | FormElementBean — misspelled field name `lable` propagated through public API

The field is named `lable` (lines 14, 40, 43) instead of `label`. The misspelling is exposed in the public getter `getLable()` and setter `setLable()`. This is a latent API defect that cannot be renamed without a breaking change. No test exists to document the current (misspelled) contract, so any future rename refactor has no regression safety net.

---

### A48-7 | Severity: MEDIUM | FormElementBean — `position` field has package-private visibility (no access modifier)

`position` (line 18) is declared without an access modifier, making it package-private. All other fields are `private`. This inconsistency exposes the field to direct mutation by any class in `com.bean` without going through `setPosition()`. No test verifies the access contract or detects unexpected mutation.

---

### A48-8 | Severity: MEDIUM | FormLibraryBean — getByteArrayObject() closes streams before retrieving byte array, creating a documentation/ordering risk

`bos.toByteArray()` is called (line 60) after `oos.close()` (line 58) and `bos.close()` (line 59). For `ByteArrayOutputStream`, `close()` is a no-op and `toByteArray()` is safe post-close, but this ordering is fragile documentation: it is not tested, so if the underlying stream type changes in a refactor the silent data-loss would go undetected.

---

### A48-9 | Severity: LOW | FormLibraryBean — serialVersionUID values are auto-generated, not intentionally assigned

Both `FormLibraryBean` (line 13: `-2617219494645726879L`) and `FormElementBean` (line 11: `-4110231449812104645L`) and `FormBuilderBean` (line 11: `3895903590422186042L`) use IDE-generated serial version UIDs. No tests verify that stored serialized blobs (e.g., in the database) remain deserializable after class changes. A schema evolution or field addition will silently break `setForm_content()` for all existing rows.

---

### A48-10 | Severity: LOW | GPSReportFilterBean — @EqualsAndHashCode(callSuper = true) behavior is untested

Lombok generates `equals()` and `hashCode()` incorporating the superclass fields. No test verifies that two `GPSReportFilterBean` instances with identical parameters are equal, or that instances with differing inherited fields are not equal. Collections and deduplication logic that use these beans will rely on untested behavior.

---

### A48-11 | Severity: INFO | FormLibraryBean — streams not closed via try-with-resources; resource leak on exception path in getFormBuilderBean()

In `getFormBuilderBean()` (lines 71–78), `bais` and `ins` are declared outside the `try` block and `ins.close()` (line 77) is inside the `try` body, not in a `finally` block or via `try-with-resources`. If `ins.readObject()` throws, `ins` is never closed. This resource leak is silent and completely untested.

---

## 4. Coverage Summary

| Class | Total testable methods | Methods with any test coverage | Coverage |
|-------|----------------------|-------------------------------|----------|
| `FormElementBean` | 14 (12 accessors + `render()` + constructor) | 0 | 0% |
| `FormLibraryBean` | 9 (7 accessors/mutators + `getByteArrayObject` + `getFormBuilderBean`) | 0 | 0% |
| `GPSReportFilterBean` | 1 explicit constructor + all Lombok-generated methods | 0 | 0% |

**Overall: 0% test coverage across all three classes.**

The most urgent remediation is A48-1 (unsafe deserialization) and A48-2 (silent exception swallowing), both in `FormLibraryBean`, as they represent a security vulnerability combined with an untestable failure mode that could cause silent data loss in production.
