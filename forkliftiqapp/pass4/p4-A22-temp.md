# Pass 4 – Code Quality Audit
**Agent:** A22
**Audit run:** 2026-02-26-01
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EquipmentTypeItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EqupmentUsageItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/FuelTypeItem.java`

---

## Step 1: Reading Evidence

### File 1 — EquipmentTypeItem.java

**Class:** `EquipmentTypeItem` (implements `Serializable`)

**Fields (all public):**
- `int id` — line 14
- `String name` — line 15
- `String url` — line 16

**Methods:**
| Method | Line |
|---|---|
| `EquipmentTypeItem()` (no-arg constructor) | 18 |
| `EquipmentTypeItem(JSONObject jsonObject) throws JSONException` | 21 |

**Types / Constants / Enums / Interfaces defined:** none beyond the class itself.

**Imports (lines 3–10):**
```
org.json.JSONException
org.json.JSONObject
java.io.Serializable
org.json.JSONArray                                        ← unused
java.util.ArrayList                                       ← unused
java.math.BigDecimal                                      ← unused
au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*    ← self-package wildcard
au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*  ← unused
```

---

### File 2 — EqupmentUsageItem.java

**Class:** `EqupmentUsageItem` (implements `Serializable`)
Note: class name is a misspelling of "Equipment" — missing the "i" in "Equip".

**Fields (all public):**
- `String time` — line 14
- `double usage` — line 15

**Methods:**
| Method | Line |
|---|---|
| `EqupmentUsageItem()` (no-arg constructor) | 17 |
| `EqupmentUsageItem(JSONObject jsonObject) throws JSONException` | 20 |

**Types / Constants / Enums / Interfaces defined:** none beyond the class itself.

**Imports (lines 3–10):**
```
org.json.JSONException
org.json.JSONObject
java.io.Serializable
org.json.JSONArray                                        ← unused
java.util.ArrayList                                       ← unused
java.math.BigDecimal                                      ← unused
au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*    ← self-package wildcard
au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*  ← unused
```

---

### File 3 — FuelTypeItem.java

**Class:** `FuelTypeItem` (implements `Serializable`)

**Fields (all public):**
- `int id` — line 14
- `String name` — line 15

**Methods:**
| Method | Line |
|---|---|
| `FuelTypeItem()` (no-arg constructor) | 17 |
| `FuelTypeItem(JSONObject jsonObject) throws JSONException` | 20 |

**Types / Constants / Enums / Interfaces defined:** none beyond the class itself.

**Imports (lines 3–10):**
```
org.json.JSONException
org.json.JSONObject
java.io.Serializable
org.json.JSONArray                                        ← unused
java.util.ArrayList                                       ← unused
java.math.BigDecimal                                      ← unused
au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*    ← self-package wildcard
au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*  ← unused
```

---

## Step 2 & 3: Findings

---

### A22-1 — HIGH: Typo in class name `EqupmentUsageItem` (missing "i" in "Equipment")

**File:** `EqupmentUsageItem.java`, line 12
**Class name:** `EqupmentUsageItem`

The class name is permanently misspelled. The word "Equipment" is missing its second "i", yielding "Equpment". This misspelling has already propagated into `EquipmentStatsItem.java` (field `usageList` typed as `ArrayList<EqupmentUsageItem>`, line 17 and 45–48), `DriverStatsFragment3.java`, and the file name itself. Renaming requires a coordinated refactor of all references. The longer this persists, the greater the surface area of the defect.

**Category:** Style inconsistency / Dead naming accuracy
**Severity:** HIGH — the incorrect name is part of the public API surface and is referenced in at least three other files, making future maintenance error-prone.

---

### A22-2 — MEDIUM: Missing `serialVersionUID` on all three `Serializable` classes

**Files:** `EquipmentTypeItem.java`, `EqupmentUsageItem.java`, `FuelTypeItem.java`

All three classes implement `java.io.Serializable` but declare no `serialVersionUID`. Java will synthesize a UID at compile time based on the class structure. Any change to fields, constructors, or method signatures will silently alter the UID, causing `java.io.InvalidClassException` if a serialized instance (e.g., stored in a `Bundle`, `Intent`, or on-disk cache) is deserialized after an app update. The absence of an explicit UID is also a build warning under the `-Xlint:serial` compiler flag.

This pattern is consistent across all sibling item classes in the package (confirmed: zero occurrences of `serialVersionUID` across 51 files searched), so this is a package-wide systemic gap, not isolated to these three files. It is reported here because all three assigned files exhibit it.

**Category:** Build warnings / potential serialization breakage
**Severity:** MEDIUM

---

### A22-3 — MEDIUM: Three unused imports present in every file (`JSONArray`, `ArrayList`, `BigDecimal`)

**Files:** `EquipmentTypeItem.java` lines 6–8; `EqupmentUsageItem.java` lines 6–8; `FuelTypeItem.java` lines 6–8

```java
import org.json.JSONArray;        // line 6 — not referenced
import java.util.ArrayList;       // line 7 — not referenced
import java.math.BigDecimal;      // line 8 — not referenced
```

None of the three classes use `JSONArray`, `ArrayList`, or `BigDecimal` anywhere in their bodies. These imports appear verbatim in all three files (and in the majority of sibling item classes), indicating a copy-paste template that was never pruned. Unused imports generate IDE and lint warnings and obscure the actual dependency footprint of each class.

**Category:** Build warnings / dead code
**Severity:** MEDIUM

---

### A22-4 — MEDIUM: Self-package wildcard import is redundant and misleading

**Files:** `EquipmentTypeItem.java` line 9; `EqupmentUsageItem.java` line 9; `FuelTypeItem.java` line 9

```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;
```

Each of these classes is itself a member of the `webserviceclasses` package. A class never needs to import its own package — members of the same package are in scope automatically in Java. This import is a no-op at compile time but is misleading: it implies the class depends on other types from the package when in fact these three files reference no other type from that package at all. Additionally, the `results.*` wildcard import on line 10 is also unused in all three files (neither `EquipmentTypeItem`, `EqupmentUsageItem`, nor `FuelTypeItem` reference any result class), adding a second redundant wildcard.

**Category:** Style inconsistency / dead code
**Severity:** MEDIUM

---

### A22-5 — LOW: All data fields are `public` with no encapsulation

**Files:** All three files (lines 14–16 in `EquipmentTypeItem.java`; lines 14–15 in `EqupmentUsageItem.java`; lines 14–15 in `FuelTypeItem.java`)

All fields (`id`, `name`, `url`, `time`, `usage`) are declared `public`. There are no getters, setters, or any form of access control. For data-transfer objects this is a common intentional pattern in this codebase (confirmed consistent across sibling classes), so it is not a finding against these files in isolation. However, combined with `Serializable` and `public` fields, there is no ability to enforce invariants or control serialization behavior (e.g., via `transient`). Reported at LOW as an encapsulation concern rather than a defect.

**Category:** Leaky abstractions
**Severity:** LOW

---

### A22-6 — LOW: `int id` fields default to `0` when JSON key is absent or null

**Files:** `EquipmentTypeItem.java` lines 26–29; `FuelTypeItem.java` lines 25–28

```java
if (!jsonObject.isNull("id"))
{
    id = jsonObject.getInt("id");
}
```

When the `"id"` key is missing from the JSON payload, the field retains the Java default value of `0`. The value `0` is a valid server-issued id in many APIs, making it impossible to distinguish "server returned 0" from "server did not return an id at all". The `double usage` field in `EqupmentUsageItem` has the same issue (`0.0`). Using `Integer`/`Double` boxed types (nullable) or a sentinel such as `-1` would distinguish the two states. This is reported at LOW because the behavior is consistent with all sibling item classes and may be acceptable given the API contract, but it is a latent correctness risk.

**Category:** Style inconsistency / correctness
**Severity:** LOW

---

## Summary Table

| ID | Severity | File(s) | Description |
|---|---|---|---|
| A22-1 | HIGH | `EqupmentUsageItem.java` | Typo "Equpment" in class name, file name, and all references |
| A22-2 | MEDIUM | All three | Missing `serialVersionUID` on `Serializable` classes |
| A22-3 | MEDIUM | All three | Unused imports: `JSONArray`, `ArrayList`, `BigDecimal` |
| A22-4 | MEDIUM | All three | Redundant self-package wildcard import and unused `results.*` wildcard import |
| A22-5 | LOW | All three | All fields `public` — no encapsulation |
| A22-6 | LOW | `EquipmentTypeItem.java`, `FuelTypeItem.java` | `int`/`double` fields default to `0`/`0.0` when JSON key absent, indistinguishable from valid value |
