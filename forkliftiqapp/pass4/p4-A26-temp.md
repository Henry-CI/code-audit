# Pass 4 – Code Quality Audit
**Agent:** A26
**Audit run:** 2026-02-26-01
**Date:** 2026-02-27
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/SavePreStartItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/SaveSessionItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/SaveShockEventItem.java`

---

## Step 1: Reading Evidence

### File 1: SavePreStartItem.java

**Class:** `SavePreStartItem implements Serializable`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses`

**Fields (all public):**
- `String start_time` (line 14)
- `String finish_time` (line 15)
- `String comment` (line 16)
- `int session_id` (line 17)
- `ArrayList<AnswerItem> arrAnswers` (line 18)

**Methods:**
| Method | Lines |
|--------|-------|
| `SavePreStartItem()` (no-arg constructor) | 20–21 |
| `SavePreStartItem(JSONObject jsonObject) throws JSONException` | 23–59 |

**Types/constants/enums/interfaces defined:** None beyond the class itself.

**Imports present:**
- `org.json.JSONException`, `org.json.JSONObject`, `java.io.Serializable`, `org.json.JSONArray`, `java.util.ArrayList`, `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (wildcard)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (wildcard)

---

### File 2: SaveSessionItem.java

**Class:** `SaveSessionItem implements Serializable`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses`

**Fields (all public):**
- `int id` (line 14)
- `int driver_id` (line 15)
- `int unit_id` (line 16)
- `String start_time` (line 17)
- `String finish_time` (line 18)
- `boolean prestart_required` (line 19)

**Methods:**
| Method | Lines |
|--------|-------|
| `SaveSessionItem()` (no-arg constructor) | 21–22 |
| `SaveSessionItem(JSONObject jsonObject) throws JSONException` | 24–59 |

**Types/constants/enums/interfaces defined:** None beyond the class itself.

**Imports present:**
- `org.json.JSONException`, `org.json.JSONObject`, `java.io.Serializable`, `org.json.JSONArray`, `java.util.ArrayList`, `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (wildcard)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (wildcard)

---

### File 3: SaveShockEventItem.java

**Class:** `SaveShockEventItem implements Serializable`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses`

**Fields (all public):**
- `String impact_time` (line 13)
- `long impact_value` (line 14)
- `String mac_address` (line 15)

**Methods:**
| Method | Lines |
|--------|-------|
| `SaveShockEventItem()` (no-arg constructor) | 17–18 |
| `SaveShockEventItem(ShockEventsDb event)` | 20–24 |
| `SaveShockEventItem(JSONObject jsonObject) throws JSONException` | 26–34 |

**Types/constants/enums/interfaces defined:** None beyond the class itself.

**Imports present:**
- `au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventsDb`
- `au.com.collectiveintelligence.fleetiq360.WebService.JSONObjectParser`
- `au.com.collectiveintelligence.fleetiq360.util.ServerDateFormatter`
- `org.json.JSONException`, `org.json.JSONObject`, `java.io.Serializable`

---

## Step 2 & 3: Findings

---

### A26-1 — HIGH: Inconsistent JSON deserialization pattern across sibling classes

**Files:** SavePreStartItem.java (lines 28–56), SaveSessionItem.java (lines 29–57), SaveShockEventItem.java (lines 27–33)

The three classes are all DTOs in the same package that deserialize from `JSONObject`, yet they use two structurally different patterns:

- **SavePreStartItem** and **SaveSessionItem** use inline, verbose, hand-rolled null guards:
  ```java
  if (!jsonObject.isNull("start_time")) {
      start_time = jsonObject.getString("start_time");
  }
  ```
- **SaveShockEventItem** uses the shared `JSONObjectParser` helper, which encapsulates the same null guard:
  ```java
  JSONObjectParser parser = new JSONObjectParser(jsonObject);
  impact_time = parser.getString("impact_time");
  ```

The `JSONObjectParser` helper already exists precisely to remove this boilerplate from individual classes. Its adoption in `SaveShockEventItem` (and also `SaveGPSLocationItem`) without back-porting to the other two older classes creates a maintenance split: a future field added to `SavePreStartItem` or `SaveSessionItem` will be written by a developer using the old pattern, widening the inconsistency. Any bug fix or behavior change to null-handling must now be made in two places (the inline guard pattern and `JSONObjectParser`).

---

### A26-2 — HIGH: Unused imports — `BigDecimal` in SavePreStartItem and SaveSessionItem

**Files:** SavePreStartItem.java (line 8), SaveSessionItem.java (line 8)

Both files import `java.math.BigDecimal` but the class body contains no reference to it anywhere. This is a dead import that will generate a compiler/IDE warning in every build and indicates code was copied from a template or sibling class without cleanup.

---

### A26-3 — HIGH: Unused imports — `JSONArray` in SaveSessionItem

**File:** SaveSessionItem.java (line 6)

`org.json.JSONArray` is imported but never referenced in `SaveSessionItem`. The class deserializes only flat primitive fields; there is no array field or array-parsing logic. This is a dead import producing a build warning.

(Note: `JSONArray` is used in `SavePreStartItem` line 50 and is therefore legitimate there.)

---

### A26-4 — MEDIUM: Wildcard imports expose unnecessary coupling in SavePreStartItem and SaveSessionItem

**Files:** SavePreStartItem.java (lines 9–10), SaveSessionItem.java (lines 9–10)

Both files carry two wildcard imports:
```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```

These classes live inside the `webserviceclasses` package itself; the self-referential wildcard is a no-op and misleading. The `results.*` wildcard is completely unused in both files (confirmed: no result type appears in either class body). `SaveShockEventItem` and `SaveGPSLocationItem` (the newer counterparts) import only what they actually use. The wildcards generate IDE warnings, pollute the namespace, and increase coupling surface without benefit.

---

### A26-5 — MEDIUM: `SaveShockEventItem(ShockEventsDb event)` instantiates `ServerDateFormatter` inline on every call

**File:** SaveShockEventItem.java (lines 20–24)

```java
public SaveShockEventItem(ShockEventsDb event) {
    this.impact_time = new ServerDateFormatter().formatDateTime(event.time);
    ...
}
```

`ServerDateFormatter` allocates two `SimpleDateFormat` instances and two `TimeZone.getTimeZone()` lookups in its constructor. This constructor is called in a loop in `ShockEventsDb.removeData()` for every item in `parameter.impactList`. Constructing a new `ServerDateFormatter` (and its two `SimpleDateFormat` objects) for each element in that loop is wasteful and inconsistent with `ShockEventsDb.removeData()` itself, which correctly reuses a single instance:
```java
ServerDateFormatter serverDateFormatter = new ServerDateFormatter();
for (SaveShockEventItem item : parameter.impactList) { ... }
```

The DTO constructor should accept a pre-constructed formatter or the date string directly, rather than owning the formatting concern itself.

---

### A26-6 — MEDIUM: Leaky abstraction — `SaveShockEventItem` directly imports a Realm persistence class (`ShockEventsDb`)

**File:** SaveShockEventItem.java (lines 3, 20–24)

`SaveShockEventItem` is a web-service DTO (a data transfer object). Its constructor `SaveShockEventItem(ShockEventsDb event)` takes a `ShockEventsDb` argument, which is a `RealmObject` — a Realm database entity. This tightly couples the web-service layer to the Realm persistence layer. Any change to `ShockEventsDb` (schema migration, ORM library replacement) may require changes to this DTO. The DTO has no business knowing about database entities; the mapping should happen at a higher layer (e.g., a repository or service class).

---

### A26-7 — LOW: Inconsistent null-guard style in `SaveShockEventItem(JSONObject)` versus sibling constructors

**File:** SaveShockEventItem.java (lines 26–34)

```java
if (jsonObject == null) return;
```

The two sibling classes guard with `if (jsonObject != null) { ... }` (wrapping the entire body). `SaveShockEventItem` uses an early-return guard. Both achieve the same result, but the inconsistency across three directly related classes is a style issue. The early-return style is generally preferable, but the mix creates unnecessary cognitive load when reading across the module.

---

### A26-8 — LOW: Trailing whitespace / spurious indentation on blank lines inside constructors

**Files:** SavePreStartItem.java (lines 27, 32, 37, 43, 48), SaveSessionItem.java (lines 28, 33, 38, 44, 49)

Each `if` block in the JSON constructors is preceded by a blank line that contains a tab character (visible as `\t` in the raw source). This is cosmetically inconsistent with standard Java style where blank lines between statements are truly empty. While not a functional defect, it indicates the code was generated or copy-pasted from a template without cleanup and will trigger whitespace lint warnings.

---

## Summary Table

| ID | Severity | File(s) | Issue |
|----|----------|---------|-------|
| A26-1 | HIGH | SavePreStartItem, SaveSessionItem vs SaveShockEventItem | Inconsistent JSON deserialization pattern; `JSONObjectParser` not adopted in older sibling classes |
| A26-2 | HIGH | SavePreStartItem (L8), SaveSessionItem (L8) | Unused import `java.math.BigDecimal` |
| A26-3 | HIGH | SaveSessionItem (L6) | Unused import `org.json.JSONArray` |
| A26-4 | MEDIUM | SavePreStartItem (L9–10), SaveSessionItem (L9–10) | Unused wildcard imports (`webserviceclasses.*`, `results.*`) |
| A26-5 | MEDIUM | SaveShockEventItem (L21) | `ServerDateFormatter` instantiated per-call inside constructor called in a loop |
| A26-6 | MEDIUM | SaveShockEventItem (L3, L20–24) | DTO imports and depends on Realm `ShockEventsDb` — cross-layer leaky abstraction |
| A26-7 | LOW | SaveShockEventItem (L28) vs siblings | Inconsistent null-guard style (early-return vs. wrapping-if) |
| A26-8 | LOW | SavePreStartItem, SaveSessionItem | Blank lines inside constructors contain trailing tab characters |
