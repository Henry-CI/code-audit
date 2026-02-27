# Pass 4 Code Quality — Agent A21
**Audit run:** 2026-02-26-01
**Agent:** A21
**Files audited:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/CompanyItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EquipmentItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EquipmentStatsItem.java`

---

## Step 1: Reading Evidence

### File 1 — CompanyItem.java

**Class:** `CompanyItem implements Serializable`

**Fields (all public):**
- `int id` (line 14)
- `String name` (line 15)
- `String email` (line 16)
- `String password` (line 17)
- `ArrayList<RoleItem> arrRoles` (line 18)
- `PermissionItem permission` (line 19)

**Methods:**

| Method | Lines |
|--------|-------|
| `CompanyItem()` — default no-arg constructor | 21–22 |
| `CompanyItem(JSONObject jsonObject) throws JSONException` — JSON-parsing constructor | 24–65 |

**Types/constants/enums/interfaces:** None defined in this file.

**Import inventory:**
- `org.json.JSONException` (line 3) — used
- `org.json.JSONObject` (line 4) — used
- `java.io.Serializable` (line 5) — used
- `org.json.JSONArray` (line 6) — used
- `java.util.ArrayList` (line 7) — used
- `java.math.BigDecimal` (line 8) — **NOT used anywhere in file**
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9) — wildcard; same package, redundant
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10) — wildcard; **no results types used in this file**

---

### File 2 — EquipmentItem.java

**Class:** `EquipmentItem implements Serializable`

**Fields (all public):**
- `int type_id` (line 10)
- `int comp_id` (line 11)
- `int fuel_type_id` (line 12)
- `int impact_threshold` (line 13)
- `int manu_id` (line 14)
- `int id` (line 15)
- `String name` (line 16)
- `String type` (line 17)
- `String manu` (line 18)
- `String fuel_type` (line 19)
- `String comp` (line 20)
- `String serial_no` (line 21)
- `String mac_address` (line 22)
- `String url` (line 23)
- `boolean active` (line 24)
- `boolean alert_enabled` (line 25)
- `boolean driver_based` (line 26)
- `int hours` (line 27)
- `boolean trained` (line 28)

**Methods:**

| Method | Lines |
|--------|-------|
| `EquipmentItem()` — default no-arg constructor | 30–31 |
| `EquipmentItem(JSONObject jsonObject) throws JSONException` — JSON-parsing constructor via `JSONObjectParser` | 33–57 |

**Types/constants/enums/interfaces:** None defined in this file.

**Import inventory:**
- `au.com.collectiveintelligence.fleetiq360.WebService.JSONObjectParser` (line 3) — used
- `org.json.JSONException` (line 4) — used
- `org.json.JSONObject` (line 5) — used
- `java.io.Serializable` (line 6) — used

---

### File 3 — EquipmentStatsItem.java

**Class:** `EquipmentStatsItem implements Serializable`

**Fields (all public):**
- `int unit_id` (line 14)
- `String unit` (line 15)
- `double total` (line 16)
- `ArrayList<EqupmentUsageItem> usageList` (line 17) — note: `EqupmentUsageItem` is a misspelling of `EquipmentUsageItem`

**Methods:**

| Method | Lines |
|--------|-------|
| `EquipmentStatsItem()` — default no-arg constructor | 19–20 |
| `EquipmentStatsItem(JSONObject jsonObject) throws JSONException` — JSON-parsing constructor | 22–53 |

**Types/constants/enums/interfaces:** None defined in this file.

**Import inventory:**
- `org.json.JSONException` (line 3) — used
- `org.json.JSONObject` (line 4) — used
- `java.io.Serializable` (line 5) — used
- `org.json.JSONArray` (line 6) — used
- `java.util.ArrayList` (line 7) — used
- `java.math.BigDecimal` (line 8) — **NOT used anywhere in file**
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9) — wildcard; same package, redundant
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10) — wildcard; **no results types used in this file**

---

## Step 2 & 3: Findings

---

### A21-1 — HIGH — Style inconsistency: two incompatible JSON-parsing patterns used across sibling classes

**Files:** `CompanyItem.java`, `EquipmentStatsItem.java` vs. `EquipmentItem.java`

`CompanyItem` and `EquipmentStatsItem` parse JSON manually by calling `jsonObject.isNull(key)` before every getter, using verbose if-blocks:

```java
// CompanyItem.java line 29-32
if (!jsonObject.isNull("id"))
{
    id = jsonObject.getInt("id");
}
```

`EquipmentItem` uses the shared `JSONObjectParser` abstraction, which encapsulates the null-check internally:

```java
// EquipmentItem.java line 36-43
JSONObjectParser parser = new JSONObjectParser(jsonObject);
type_id = parser.getInt("type_id");
id = parser.getInt("id");
```

`JSONObjectParser` was clearly introduced to eliminate this boilerplate. `CompanyItem` and `EquipmentStatsItem` were never migrated. This creates two divergent maintenance paths: null-check behaviour changes in `JSONObjectParser` will not apply to `CompanyItem` or `EquipmentStatsItem`, and vice versa. The same inconsistency is confirmed in the direct dependency `EqupmentUsageItem.java` (also uses the old pattern).

**Impact:** Inconsistent default values on missing fields. `JSONObjectParser.getInt()` returns `0` on null; the manual path leaves the field at its Java default (`0` for `int`, `null` for `String`) only if the `if` block is not entered — functionally equivalent today, but any future change to `JSONObjectParser` defaults will silently diverge.

---

### A21-2 — HIGH — Public `password` field on a Serializable class exposes plaintext credentials

**File:** `CompanyItem.java`, line 17

```java
public String password;
```

`CompanyItem implements Serializable`. A public `String password` field will be included in any serialized representation of the object (e.g. `Intent` extras, `SharedPreferences` via serialization, object streams). Storing or transmitting a plaintext password inside a serializable data-transfer object is a credential-exposure risk. The field carries a direct server password parsed from a JSON API response (`jsonObject.getString("password")`, line 46). Compare: `LoginItem.java` (a sibling class) also carries `public String password` with identical risk.

**Note for scoping:** only `CompanyItem` is in scope for this audit. The same pattern in `LoginItem` should be flagged by the agent assigned to that file.

---

### A21-3 — MEDIUM — Unused import `java.math.BigDecimal` in two files (copy-paste boilerplate)

**Files:** `CompanyItem.java` line 8, `EquipmentStatsItem.java` line 8

```java
import java.math.BigDecimal;
```

`BigDecimal` is imported but never referenced in either file. Investigation of the wider package confirms this import appears at line 8 in nearly every class in `webserviceclasses` and its subpackages — it is a copy-pasted boilerplate template import, never cleaned up. This generates a compiler/lint warning (`unused import`) across the entire package. For the two audited files the import is confirmed unused.

---

### A21-4 — MEDIUM — Wildcard import of own package and unused `results` wildcard in two files

**Files:** `CompanyItem.java` lines 9–10, `EquipmentStatsItem.java` lines 9–10

```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```

Two issues:
1. The first wildcard imports the class's own package — this import is always redundant in Java (same-package types are always in scope without an import statement). It will trigger a lint/IDE warning.
2. The second wildcard (`results.*`) imports types from the `results` sub-package. Neither `CompanyItem` nor `EquipmentStatsItem` reference any type from `results.*` anywhere in their bodies. The import is entirely unused.

Both wildcard imports are confirmed to be copy-pasted boilerplate (the same two lines appear in `EqupmentUsageItem`, `RoleItem`, `PermissionItem`, `FuelTypeItem`, and every other older-pattern class in the package).

---

### A21-5 — MEDIUM — Typo in class name `EqupmentUsageItem` propagated into field and loop variable

**File:** `EquipmentStatsItem.java` lines 17, 45, 48

```java
public ArrayList<EqupmentUsageItem> usageList;          // line 17
usageList = new ArrayList<EqupmentUsageItem>();          // line 45
EqupmentUsageItem temp = new EqupmentUsageItem(...);    // line 48
```

The class `EqupmentUsageItem` (defined in `EqupmentUsageItem.java`) is missing the letter `i` — it should be `EquipmentUsageItem`. The misspelling is present both in the source file name and throughout the codebase. Within `EquipmentStatsItem`, this manifests in three places. The typo is now frozen by the public API: renaming it would be a breaking change to any caller holding a reference. The error is systemic — the filename, class name, and all usages are consistently misspelled.

---

### A21-6 — LOW — Inconsistent brace style between files

**Files:** `CompanyItem.java`, `EquipmentStatsItem.java` vs. `EquipmentItem.java`

`CompanyItem` and `EquipmentStatsItem` use Allman style (opening brace on its own line):

```java
// CompanyItem.java line 12-13
public class CompanyItem implements Serializable
{
```

`EquipmentItem` uses K&R / Java-standard style (opening brace on the same line):

```java
// EquipmentItem.java line 9
public class EquipmentItem implements Serializable {
```

This is a minor style inconsistency within the same package but reflects the two different authoring generations of these classes (older hand-coded pattern vs. newer `JSONObjectParser`-based pattern).

---

### A21-7 — LOW — Inconsistent for-loop indentation / leading-space formatting in CompanyItem and EquipmentStatsItem

**Files:** `CompanyItem.java` line 54, `EquipmentStatsItem.java` line 47

```java
// CompanyItem.java line 54 — leading space before 'for' breaks tab-indentation
	 for (int i = 0; i < jsonArray.length(); i++){
```

```java
// EquipmentStatsItem.java line 47 — same issue
	 for (int i = 0; i < jsonArray.length(); i++){
```

Both for-loops are preceded by a tab character followed by an extra space (visible as `\t ` in the raw file), and the opening brace `{` is attached to the closing parenthesis with no space before it. This is inconsistent with both the surrounding code's indentation style and Java conventions. The same formatting defect appears in both files, confirming it was copy-pasted.

---

### A21-8 — LOW — Trailing whitespace on blank lines inside constructor bodies

**Files:** `CompanyItem.java`, `EquipmentStatsItem.java`

Lines 28, 33, 38, 43, 49, 59 in `CompanyItem.java` and lines 26, 31, 36, 42 in `EquipmentStatsItem.java` contain a single tab character on otherwise blank lines (visible as `\t` in the raw file — shown as blank in the read output but present in the source). This is a copy-paste artifact from the same template that produced the wildcard imports and `BigDecimal` import. It will trigger `whitespace` lint warnings.

---

## Summary Table

| ID | Severity | File(s) | Description |
|----|----------|---------|-------------|
| A21-1 | HIGH | CompanyItem, EquipmentStatsItem | Two incompatible JSON-parsing patterns; `JSONObjectParser` not adopted |
| A21-2 | HIGH | CompanyItem | Public `password` field on Serializable class exposes plaintext credentials |
| A21-3 | MEDIUM | CompanyItem, EquipmentStatsItem | Unused `import java.math.BigDecimal` (copy-paste boilerplate) |
| A21-4 | MEDIUM | CompanyItem, EquipmentStatsItem | Redundant same-package wildcard import; unused `results.*` wildcard import |
| A21-5 | MEDIUM | EquipmentStatsItem | Typo `EqupmentUsageItem` (missing `i`) frozen into public API |
| A21-6 | LOW | CompanyItem, EquipmentStatsItem vs. EquipmentItem | Inconsistent brace style (Allman vs. K&R) across sibling classes |
| A21-7 | LOW | CompanyItem, EquipmentStatsItem | For-loop indentation defect (`\t ` leading whitespace, no space before `{`) |
| A21-8 | LOW | CompanyItem, EquipmentStatsItem | Trailing whitespace on blank lines inside constructor bodies |

**No commented-out code found in any of the three files.**
**No deprecated API usage or `@SuppressWarnings` annotations found.**
**No dependency version conflicts visible in these files.**
