# Pass 4 — Code Quality Audit
**Agent:** A36
**Audit run:** 2026-02-26-01
**Date:** 2026-02-27

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/EquipmentTypeResultArray.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/FuelTypeResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/GetCompanyResultArray.java`

---

## Step 1: Reading Evidence

### File 1 — EquipmentTypeResultArray.java

**Class:** `EquipmentTypeResultArray`
- Extends: `WebServiceResultPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results`

**Fields:**
- `public ArrayList<EquipmentTypeItem> arrayList` (line 14)

**Methods:**

| Method | Lines | Notes |
|---|---|---|
| `EquipmentTypeResultArray()` | 16–17 | No-arg constructor |
| `EquipmentTypeResultArray(JSONArray jsonArray)` | 19–30 | Parameterized constructor; throws JSONException |

**Types/Constants/Interfaces defined:** None beyond the class itself.

**Imports (lines 3–10):**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

### File 2 — FuelTypeResultArray.java

**Class:** `FuelTypeResultArray`
- Extends: `WebServiceResultPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results`

**Fields:**
- `public ArrayList<FuelTypeItem> arrayList` (line 14)

**Methods:**

| Method | Lines | Notes |
|---|---|---|
| `FuelTypeResultArray()` | 16–17 | No-arg constructor |
| `FuelTypeResultArray(JSONArray jsonArray)` | 19–30 | Parameterized constructor; throws JSONException |

**Types/Constants/Interfaces defined:** None beyond the class itself.

**Imports (lines 3–10):** Identical to File 1.

---

### File 3 — GetCompanyResultArray.java

**Class:** `GetCompanyResultArray`
- Extends: `WebServiceResultPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results`

**Fields:**
- `public ArrayList<CompanyItem> arrayList` (line 14)

**Methods:**

| Method | Lines | Notes |
|---|---|---|
| `GetCompanyResultArray()` | 16–17 | No-arg constructor |
| `GetCompanyResultArray(JSONArray jsonArray)` | 19–30 | Parameterized constructor; throws JSONException |

**Types/Constants/Interfaces defined:** None beyond the class itself.

**Imports (lines 3–10):** Identical to Files 1 and 2.

---

### Supporting Context Read

The following files were also read to verify cross-cutting concerns:

- `WebServiceResultPacket.java` — parent class; itself extends `WebServicePacket`; declares `public transient String requestID`
- `WebServicePacket.java` — root ancestor; empty body in both constructors
- `EquipmentTypeItem.java` — item class for file 1
- `FuelTypeItem.java` — item class for file 2
- `CompanyItem.java` — item class for file 3 (contains a `public String password` field)
- `ManufactureResultArray.java` — sibling result array for style comparison (identical structural pattern)

---

## Step 2 & 3: Findings

---

### A36-1 — MEDIUM: Unused imports (`JSONObject`, `BigDecimal`) present in all three files

**Affected files (all three):**
- `EquipmentTypeResultArray.java` lines 4, 8
- `FuelTypeResultArray.java` lines 4, 8
- `GetCompanyResultArray.java` lines 4, 8

**Detail:** `org.json.JSONObject` (line 4) and `java.math.BigDecimal` (line 8) are imported in every file but neither is referenced anywhere in the class body. The constructor accepts `JSONArray`, not `JSONObject`, and no decimal arithmetic exists. These imports will generate "unused import" compiler warnings in most IDEs and static analysis tools. The same pattern is present across all sibling result-array classes (e.g., `ManufactureResultArray.java`), indicating the issue originates in a code-generation template that was never cleaned up.

---

### A36-2 — MEDIUM: Self-referential (redundant) wildcard import in all three files

**Affected files (all three):**
- `EquipmentTypeResultArray.java` line 10
- `FuelTypeResultArray.java` line 10
- `GetCompanyResultArray.java` line 10

**Detail:** Each file contains:
```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```
This is a wildcard import of the package that the file itself belongs to. Members of the same package are always in scope without an explicit import; this import is therefore entirely redundant and will produce a compiler/IDE warning. It appears in every file in this package, indicating a systemic template defect.

---

### A36-3 — MEDIUM: `Serializable` declared redundantly on subclasses

**Affected files (all three):**
- `EquipmentTypeResultArray.java` line 12
- `FuelTypeResultArray.java` line 12
- `GetCompanyResultArray.java` line 12

**Detail:** All three classes declare `implements Serializable` directly. Their superclass chain (`WebServiceResultPacket` → `WebServicePacket`) also implements `Serializable`, making the re-declaration on each subclass redundant. While not a runtime defect, it creates noise and can mislead readers into thinking the subclass requires a special serialization contract. It also generates IDE warnings in some configurations. The pattern is consistent across sibling classes (`ManufactureResultArray`, etc.), again pointing to a flawed template.

---

### A36-4 — HIGH: Public mutable field `arrayList` exposes internal collection directly

**Affected files (all three):**
- `EquipmentTypeResultArray.java` line 14
- `FuelTypeResultArray.java` line 14
- `GetCompanyResultArray.java` line 14

**Detail:** The parsed result collection is exposed as a bare `public` field:
```java
public ArrayList<EquipmentTypeItem> arrayList;
public ArrayList<FuelTypeItem> arrayList;
public ArrayList<CompanyItem> arrayList;
```
Any caller can replace the list reference (`obj.arrayList = null`), clear it, or add arbitrary items, bypassing any invariants. This is a leaky abstraction: callers are coupled to both the concrete `ArrayList` type and the field name. A getter returning an unmodifiable view (or at minimum `List<T>`) would be the appropriate pattern. The field is also uninitialized if the no-arg constructor is used, meaning `arrayList` will be `null` until the parameterized constructor runs, creating a latent NPE risk for callers that use the no-arg constructor without subsequently setting the field.

---

### A36-5 — LOW: Inconsistent brace/spacing style in the `for` loop across all three files

**Affected files (all three):**
- `EquipmentTypeResultArray.java` line 25
- `FuelTypeResultArray.java` line 25
- `GetCompanyResultArray.java` line 25

**Detail:** The `for` loop header has a leading space before the loop keyword and inconsistent indentation relative to the surrounding `if` block:
```java
         for (int i = 0; i < jsonArray.length(); i++){
```
Specifically: (a) the leading extra space before `for`, and (b) the opening brace `{` is placed directly after `)` with no space, while the enclosing `if` block uses `)\n{` (Allman style). The loop body is also under-indented by one level. This inconsistency is present identically in the sibling class `ManufactureResultArray.java`, confirming it is a template defect rather than per-file variation.

---

### A36-6 — LOW: Trailing blank line inside the parameterized constructor body (cosmetic / whitespace noise)

**Affected files (all three):**
- `EquipmentTypeResultArray.java` line 21
- `FuelTypeResultArray.java` line 21
- `GetCompanyResultArray.java` line 21

**Detail:** There is a blank line immediately after the opening brace of the parameterized constructor before `arrayList = new ArrayList<>()`. While minor, this is inconsistent with the no-arg constructor (which is compact) and with the outer class formatting. It appears in every sibling result-array file, confirming template origin.

---

### A36-7 — INFO: Naming inconsistency — class name prefix `Get` is absent from peer classes

**Affected file:** `GetCompanyResultArray.java`

**Detail:** Two of the three files follow the naming convention `<DomainConcept>ResultArray` (e.g., `EquipmentTypeResultArray`, `FuelTypeResultArray`, `ManufactureResultArray`). The third uses `GetCompanyResultArray`, prefixing the class name with the HTTP verb/action `Get`. This is a style inconsistency within the result-array family; the class should be named `CompanyResultArray` for uniformity. The inconsistency likely reflects the name of the web service endpoint leaking into the DTO naming layer.

---

## Summary Table

| ID | Severity | File(s) | Issue |
|---|---|---|---|
| A36-1 | MEDIUM | All three | Unused imports: `JSONObject`, `BigDecimal` |
| A36-2 | MEDIUM | All three | Redundant self-referential wildcard import of own package |
| A36-3 | MEDIUM | All three | `Serializable` re-declared redundantly on subclasses |
| A36-4 | HIGH | All three | Public mutable `ArrayList` field — leaky abstraction, NPE risk |
| A36-5 | LOW | All three | Inconsistent brace/indentation style in `for` loop |
| A36-6 | LOW | All three | Spurious blank line inside parameterized constructor body |
| A36-7 | INFO | `GetCompanyResultArray.java` | Naming prefix `Get` inconsistent with peer result-array classes |

**Total findings:** 7 (1 HIGH, 3 MEDIUM, 2 LOW, 1 INFO)

No commented-out code, deprecated API usage, `@SuppressWarnings` annotations, stale TODO/FIXME markers, or dependency version conflicts were observed in the three assigned files.
