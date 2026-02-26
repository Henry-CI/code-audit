# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A35
**Files audited:**
- `src/main/java/com/actionform/AdminUnitImpactForm.java`
- `src/main/java/com/actionform/AdminUnitServiceForm.java`
- `src/main/java/com/actionform/DealerCompaniesActionForm.java`

---

## 1. Reading-Evidence Blocks

### 1.1 AdminUnitImpactForm

**File:** `src/main/java/com/actionform/AdminUnitImpactForm.java`
**Package:** `com.actionform`
**Class:** `AdminUnitImpactForm extends ActionForm`
**Line range:** 1–86

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `private static final long` | 11 |
| `id` | `private int` | 13 |
| `unitId` | `private int` | 14 |
| `servLast` | `private int` | 15 |
| `servNext` | `private int` | 16 |
| `servDuration` | `private int` | 17 |
| `accHours` | `private double` | 18 |
| `hourmeter` | `private double` | 20 |
| `action` | `private String` | 22 |
| `servType` | `private String` | 23 |
| `servStatus` | `private String` | 24 |

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `getId` | `public int getId()` | 26–28 |
| `getUnitId` | `public int getUnitId()` | 29–31 |
| `getServLast` | `public int getServLast()` | 32–34 |
| `getServNext` | `public int getServNext()` | 35–37 |
| `getServDuration` | `public int getServDuration()` | 38–40 |
| `getAction` | `public String getAction()` | 41–43 |
| `getServType` | `public String getServType()` | 44–46 |
| `setId` | `public void setId(int id)` | 47–49 |
| `setUnitId` | `public void setUnitId(int unitId)` | 50–52 |
| `setServLast` | `public void setServLast(int servLast)` | 53–55 |
| `setServNext` | `public void setServNext(int servNext)` | 56–58 |
| `setServDuration` | `public void setServDuration(int servDuration)` | 59–61 |
| `setAction` | `public void setAction(String action)` | 62–64 |
| `setServType` | `public void setServType(String servType)` | 65–67 |
| `getServStatus` | `public String getServStatus()` | 68–70 |
| `setServStatus` | `public void setServStatus(String servStatus)` | 71–73 |
| `getHourmeter` | `public double getHourmeter()` | 74–76 |
| `setHourmeter` | `public void setHourmeter(double hourmeter)` | 77–79 |
| `getAccHours` | `public double getAccHours()` | 80–82 |
| `setAccHours` | `public void setAccHours(double accHours)` | 83–85 |

---

### 1.2 AdminUnitServiceForm

**File:** `src/main/java/com/actionform/AdminUnitServiceForm.java`
**Package:** `com.actionform`
**Class:** `AdminUnitServiceForm extends ActionForm`
**Line range:** 1–86

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `private static final long` | 11 |
| `id` | `private int` | 13 |
| `unitId` | `private int` | 14 |
| `servLast` | `private int` | 15 |
| `servNext` | `private int` | 16 |
| `servDuration` | `private int` | 17 |
| `accHours` | `private double` | 18 |
| `hourmeter` | `private double` | 20 |
| `action` | `private String` | 22 |
| `servType` | `private String` | 23 |
| `servStatus` | `private String` | 24 |

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `getId` | `public int getId()` | 26–28 |
| `getUnitId` | `public int getUnitId()` | 29–31 |
| `getServLast` | `public int getServLast()` | 32–34 |
| `getServNext` | `public int getServNext()` | 35–37 |
| `getServDuration` | `public int getServDuration()` | 38–40 |
| `getAction` | `public String getAction()` | 41–43 |
| `getServType` | `public String getServType()` | 44–46 |
| `setId` | `public void setId(int id)` | 47–49 |
| `setUnitId` | `public void setUnitId(int unitId)` | 50–52 |
| `setServLast` | `public void setServLast(int servLast)` | 53–55 |
| `setServNext` | `public void setServNext(int servNext)` | 56–58 |
| `setServDuration` | `public void setServDuration(int servDuration)` | 59–61 |
| `setAction` | `public void setAction(String action)` | 62–64 |
| `setServType` | `public void setServType(String servType)` | 65–67 |
| `getServStatus` | `public String getServStatus()` | 68–70 |
| `setServStatus` | `public void setServStatus(String servStatus)` | 71–73 |
| `getHourmeter` | `public double getHourmeter()` | 74–76 |
| `setHourmeter` | `public void setHourmeter(double hourmeter)` | 77–79 |
| `getAccHours` | `public double getAccHours()` | 80–82 |
| `setAccHours` | `public void setAccHours(double accHours)` | 83–85 |

---

### 1.3 DealerCompaniesActionForm

**File:** `src/main/java/com/actionform/DealerCompaniesActionForm.java`
**Package:** `com.actionform`
**Class:** `DealerCompaniesActionForm extends ActionForm`
**Line range:** 1–6

**Fields:** None declared (empty class body beyond the class declaration).
**Methods:** None declared (inherits only from `ActionForm`).

---

## 2. Test-Directory Grep Results

Test directory searched: `src/test/java/`

Test files present:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

| Search term | Matches found |
|-------------|---------------|
| `AdminUnitImpactForm` | None |
| `AdminUnitServiceForm` | None |
| `DealerCompaniesActionForm` | None |
| `UnitImpact`, `UnitService`, `DealerCompanies`, `actionform` (case-insensitive) | None |

No existing test file references any of the three audited classes, directly or indirectly.

---

## 3. Additional Code-Quality Observations

### 3.1 Duplicate serialVersionUID across multiple ActionForm classes

`AdminUnitImpactForm` and `AdminUnitServiceForm` both declare:

```java
private static final long serialVersionUID = -2208616500078494492L;
```

This value is also used verbatim in `AdminUnitChecklistForm`. Sharing a `serialVersionUID` across unrelated serializable classes violates the Java serialization contract: if objects of different types are ever serialised/deserialised through a generic `ActionForm` stream, the JVM may silently accept objects of the wrong type or produce unexpected `InvalidClassException` behaviour depending on the deserialization context.

### 3.2 Structural duplication between AdminUnitImpactForm and AdminUnitServiceForm

The two classes are byte-for-byte identical in field declarations (11 fields), method signatures (20 methods), and even the copied `serialVersionUID` value. Their only difference is the class name. This strongly suggests that one was created as a copy of the other. Both classes carry the same design defects simultaneously and will require the same remediation effort.

---

## 4. Coverage Findings

### A35-1 | Severity: CRITICAL | AdminUnitImpactForm — no test class exists

No test file for `AdminUnitImpactForm` exists anywhere in `src/test/java/`. All 20 methods (10 getters, 10 setters covering `id`, `unitId`, `servLast`, `servNext`, `servDuration`, `accHours`, `hourmeter`, `action`, `servType`, `servStatus`) have 0% line coverage, 0% branch coverage, and 0% method coverage. The class is completely untested.

### A35-2 | Severity: CRITICAL | AdminUnitServiceForm — no test class exists

No test file for `AdminUnitServiceForm` exists anywhere in `src/test/java/`. All 20 methods (10 getters, 10 setters covering the same 10 fields listed above) have 0% line coverage, 0% branch coverage, and 0% method coverage. The class is completely untested.

### A35-3 | Severity: HIGH | DealerCompaniesActionForm — no test class exists

No test file for `DealerCompaniesActionForm` exists anywhere in `src/test/java/`. The class body is empty (no declared fields or methods), so there is no executable logic to exercise. However, the absence of even a basic smoke test (instantiation, `assertNotNull`, Struts reset/validate inheritance check) means that any future addition of fields or methods will enter production with no coverage baseline in place. The severity is HIGH rather than CRITICAL only because there is currently no executable logic to miss.

### A35-4 | Severity: HIGH | AdminUnitImpactForm and AdminUnitServiceForm share an identical serialVersionUID with AdminUnitChecklistForm

All three classes use `serialVersionUID = -2208616500078494492L` (confirmed by grep across the `actionform` package). No test validates serialization/deserialization round-trip identity or type safety for any of these classes. A test exercising Java object serialization round-trips would detect a type-confusion defect at the deserialization boundary if these forms were ever persisted or transmitted.

### A35-5 | Severity: MEDIUM | No setter/getter round-trip tests for AdminUnitImpactForm

Even if a minimal test class is created, individual setter+getter round-trip assertions are absent for all 10 field pairs. For `double` fields (`accHours`, `hourmeter`) the default zero-value makes silent no-op assignments undetectable without explicit set-then-get assertions. Tests must cover at least one non-default value per field.

### A35-6 | Severity: MEDIUM | No setter/getter round-trip tests for AdminUnitServiceForm

Identical gap to A35-5, applying to `AdminUnitServiceForm`. All 10 field pairs (`id`, `unitId`, `servLast`, `servNext`, `servDuration`, `accHours`, `hourmeter`, `action`, `servType`, `servStatus`) lack round-trip assertions.

### A35-7 | Severity: LOW | DealerCompaniesActionForm is an empty class with no declared contract

The class declares no fields, no methods, and no `serialVersionUID`. If it is used as a Struts `ActionForm` (which it extends), Struts will attempt to bind HTTP request parameters to it via reflection. There is no test confirming the class can be instantiated by Struts or that it correctly rejects unexpected parameter binding. The absence of a `serialVersionUID` also means the JVM will generate one at compile time, making the class non-deterministically serialisable across different JVM builds.

### A35-8 | Severity: INFO | AdminUnitImpactForm and AdminUnitServiceForm are structurally identical — consider consolidation

The two classes share the same 11 fields and 20 methods with no semantic differentiation observable from the source code. A single parameterised class or a shared base class would eliminate the duplication and halve the test surface that must be maintained. This is a design observation rather than a direct coverage gap, but it affects the ongoing cost of achieving and maintaining coverage.

---

## 5. Coverage Summary

| Class | Methods | Methods tested | Line coverage | Verdict |
|-------|---------|---------------|---------------|---------|
| `AdminUnitImpactForm` | 20 | 0 | 0% | NO COVERAGE |
| `AdminUnitServiceForm` | 20 | 0 | 0% | NO COVERAGE |
| `DealerCompaniesActionForm` | 0 declared | 0 | N/A (empty) | NO COVERAGE BASELINE |

**All three classes have zero test coverage.**
