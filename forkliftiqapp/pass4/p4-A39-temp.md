# Pass 4 – Code Quality Audit
**Audit run:** 2026-02-26-01
**Agent:** A39
**Date:** 2026-02-27

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/PreStartHelpResultArray.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/PreStartQuestionResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ReportResultArray.java`

---

## Step 1: Reading Evidence

### File 1: PreStartHelpResultArray.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/PreStartHelpResultArray.java`

**Class name:** `PreStartHelpResultArray`

**Extends:** `WebServiceResultPacket`

**Implements:** `Serializable`

**Fields:**
- Line 14: `public ArrayList<PreStartHelpItem> arrayList`

**Methods (exhaustive):**
- Line 16–17: `PreStartHelpResultArray()` — default no-arg constructor (empty body)
- Line 19–30: `PreStartHelpResultArray(JSONArray jsonArray) throws JSONException` — parameterized constructor; initializes `arrayList`, iterates `jsonArray`, constructs `PreStartHelpItem` per element

**Types / constants / enums / interfaces defined:** None beyond the class itself.

**Imports:**
- `org.json.JSONException` (used in constructor signature)
- `org.json.JSONObject` (unused — not referenced anywhere in file)
- `java.io.Serializable` (used)
- `org.json.JSONArray` (used)
- `java.util.ArrayList` (used)
- `java.math.BigDecimal` (unused — not referenced anywhere in file)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (used transitively for `PreStartHelpItem`)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` — self-import (this file is in the `results` package; importing own package is a no-op)

---

### File 2: PreStartQuestionResultArray.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/PreStartQuestionResultArray.java`

**Class name:** `PreStartQuestionResultArray`

**Extends:** `WebServiceResultPacket`

**Implements:** `Serializable`

**Fields:**
- Line 14: `public ArrayList<PreStartQuestionItem> arrayList`

**Methods (exhaustive):**
- Line 16–17: `PreStartQuestionResultArray()` — default no-arg constructor (empty body)
- Line 19–30: `PreStartQuestionResultArray(JSONArray jsonArray) throws JSONException` — parameterized constructor; initializes `arrayList`, iterates `jsonArray`, constructs `PreStartQuestionItem` per element

**Types / constants / enums / interfaces defined:** None beyond the class itself.

**Imports:**
- `org.json.JSONException` (used in constructor signature)
- `org.json.JSONObject` (unused — not referenced anywhere in file)
- `java.io.Serializable` (used)
- `org.json.JSONArray` (used)
- `java.util.ArrayList` (used)
- `java.math.BigDecimal` (unused — not referenced anywhere in file)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (used transitively for `PreStartQuestionItem`)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` — self-import (this file is in the `results` package)

---

### File 3: ReportResultArray.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ReportResultArray.java`

**Class name:** `ReportResultArray`

**Extends:** `WebServiceResultPacket`

**Implements:** `Serializable`

**Fields:**
- Line 14: `public ArrayList<ReportItem> arrayList`

**Methods (exhaustive):**
- Line 16–17: `ReportResultArray()` — default no-arg constructor (empty body)
- Line 19–30: `ReportResultArray(JSONArray jsonArray) throws JSONException` — parameterized constructor; initializes `arrayList`, iterates `jsonArray`, constructs `ReportItem` per element

**Types / constants / enums / interfaces defined:** None beyond the class itself.

**Imports:**
- `org.json.JSONException` (used in constructor signature)
- `org.json.JSONObject` (unused — not referenced anywhere in file)
- `java.io.Serializable` (used)
- `org.json.JSONArray` (used)
- `java.util.ArrayList` (used)
- `java.math.BigDecimal` (unused — not referenced anywhere in file)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (used transitively for `ReportItem`)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` — self-import (this file is in the `results` package)

---

## Step 2 & 3: Code Quality Review and Findings

The three files are structurally identical copies of the same template, differing only in the parameterized type (`PreStartHelpItem`, `PreStartQuestionItem`, `ReportItem`). All findings below apply equally to all three files unless noted.

Cross-reference confirmed: the same import block and structural boilerplate is present in every `*ResultArray.java` in the package (at least 10 files examined: `EquipmentStatsResultArray`, `GetEquipmentResultArray`, `LoginResultArray`, `ServiceRecordResultArray`, `ManufactureResultArray`, etc.), making this a package-wide pattern, not isolated to the three assigned files.

---

### A39-1 — MEDIUM — Unused imports: `JSONObject` and `BigDecimal`

**Affected files:** All three assigned files (lines 4 and 8 in each).

```java
import org.json.JSONObject;   // line 4
import java.math.BigDecimal;  // line 8
```

Neither `JSONObject` nor `BigDecimal` is referenced anywhere in the body of any of these three classes. The imports are cargo-culted from a template. They generate compiler warnings and add noise to every file. The same unused-import pattern is present in all sibling `*ResultArray` files in the package, meaning the boilerplate template itself is defective.

---

### A39-2 — LOW — Self-referential package import

**Affected files:** All three assigned files (line 10 in each).

```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```

Each of these files is declared in the `results` package. Importing one's own package is a no-op in Java; the compiler silently ignores it. This is not a compile error but is dead noise in every file, again copied from the shared template.

---

### A39-3 — HIGH — Leaky abstraction: `public` field `arrayList` directly exposes mutable collection

**Affected files:** All three assigned files (line 14 in each).

```java
public ArrayList<PreStartHelpItem> arrayList;      // PreStartHelpResultArray
public ArrayList<PreStartQuestionItem> arrayList;  // PreStartQuestionResultArray
public ArrayList<ReportItem> arrayList;            // ReportResultArray
```

The internal `ArrayList` is declared `public` with no accessor method. Any caller can replace the entire list (`result.arrayList = null`), clear it, or mutate its contents without the owning object's knowledge. Callers across the codebase (confirmed in `EquipmentPrestartFragment.java` line 53–54, `SavedReportFragment.java` lines 52 and 67, `PreStartQuestionDb.java` line 47, etc.) directly read and in some cases write `arrayList`. This breaks encapsulation and makes the object's invariants impossible to enforce. The same leaky pattern exists across the entire `*ResultArray` family (at least 10 classes).

---

### A39-4 — MEDIUM — Redundant `Serializable` declaration on subclass

**Affected files:** All three assigned files (line 12 in each).

```java
public class PreStartHelpResultArray extends WebServiceResultPacket implements Serializable
```

`WebServiceResultPacket` already `implements Serializable` (confirmed by reading `WebServiceResultPacket.java`, which itself extends `WebServicePacket implements Serializable`). Declaring `implements Serializable` again on each subclass is redundant. While harmless at runtime, it creates visual clutter and implies the developer did not check the superclass hierarchy, which is consistent with a copy-paste template workflow.

---

### A39-5 — MEDIUM — Massive code duplication / missing generic abstraction

**Affected files:** All three assigned files; all `*ResultArray` files in the package (at least 10).

All three assigned files are structurally identical, differing only in the type parameter. Java generics would eliminate this duplication entirely. A single class such as:

```java
public class ResultArray<T> extends WebServiceResultPacket implements Serializable { ... }
```

would replace at least 10 near-identical files. The copy-paste approach means any future bug in the shared logic must be fixed in every copy independently, and the import/field errors documented in A39-1 through A39-4 are perpetuated across the entire family.

---

### A39-6 — LOW — Minor whitespace inconsistency in `for` loop

**Affected files:** All three assigned files (line 25 in each).

```java
         for (int i = 0; i < jsonArray.length(); i++){
```

The opening brace `{` on the `for` line is not preceded by a space (style: `i++){` vs. `i++) {`), and the indentation of the leading space before `for` is one extra space compared to the surrounding block. This is a minor but consistent deviation from standard Java style visible in every copy of the template. The closing brace of the `for` block (line 28) is correctly indented, making the inconsistency purely in the `for` statement line.

---

## Summary Table

| ID    | Severity | Description                                                              | Lines (each file) |
|-------|----------|--------------------------------------------------------------------------|--------------------|
| A39-1 | MEDIUM   | Unused imports: `JSONObject` (line 4) and `BigDecimal` (line 8)         | 4, 8               |
| A39-2 | LOW      | Self-referential package import (`results.*` in `results` package)       | 10                 |
| A39-3 | HIGH     | `public` mutable field `arrayList` — leaky abstraction, no encapsulation | 14                 |
| A39-4 | MEDIUM   | Redundant `implements Serializable` already inherited from superclass    | 12                 |
| A39-5 | MEDIUM   | Massive copy-paste duplication; generic abstraction not used             | entire files       |
| A39-6 | LOW      | Minor whitespace/brace style inconsistency in `for` statement            | 25                 |

**Total findings: 6**
**No commented-out code, no TODO/FIXME markers, no deprecated API usage, and no @SuppressWarnings annotations were found in any of the three assigned files.**
