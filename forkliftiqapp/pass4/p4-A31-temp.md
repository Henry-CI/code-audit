# Pass 4 — Code Quality Audit
**Agent:** A31
**Audit run:** 2026-02-26-01
**Pass:** 4 (Code Quality)

---

## Step 1: Reading Evidence

### File 1: SaveLicenseParameter.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveLicenseParameter.java`

**Class name:**
`SaveLicenseParameter` — extends `WebServiceParameterPacket` implements `Serializable`

**Methods (exhaustive):**

| Line | Method |
|------|--------|
| 20   | `public SaveLicenseParameter()` — default constructor, empty body |

**Fields:**

| Line | Field |
|------|-------|
| 14   | `public int id` |
| 15   | `public String licno` |
| 16   | `public String addr` |
| 17   | `public String expirydt` |
| 18   | `public String securityno` |

**Types / constants / enums / interfaces defined:** none beyond the class itself.

**Imports (lines 3–10):**
- `org.json.JSONException` (line 3)
- `org.json.JSONObject` (line 4)
- `java.io.Serializable` (line 5)
- `org.json.JSONArray` (line 6)
- `java.util.ArrayList` (line 7)
- `java.math.BigDecimal` (line 8)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10)

---

### File 2: SaveMultipleGPSParameter.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveMultipleGPSParameter.java`

**Class name:**
`SaveMultipleGPSParameter` — extends `WebServiceParameterPacket` implements `Serializable`

**Methods (exhaustive):**

| Line | Method |
|------|--------|
| 12   | `public SaveMultipleGPSParameter()` — initialises `gpsList` to `new ArrayList<>()` |

**Fields:**

| Line | Field |
|------|-------|
| 10   | `public ArrayList<SaveGPSLocationItem> gpsList` |

**Types / constants / enums / interfaces defined:** none beyond the class itself.

**Imports (lines 3–8):**
- `java.io.Serializable` (line 3)
- `java.util.ArrayList` (line 4)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveGPSLocationItem` (line 6)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServiceParameterPacket` (line 7)

---

### File 3: SavePreStartParameter.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SavePreStartParameter.java`

**Class name:**
`SavePreStartParameter` — extends `WebServiceParameterPacket` implements `Serializable`

**Methods (exhaustive):**

| Line | Method |
|------|--------|
| 20   | `public SavePreStartParameter()` — default constructor, empty body |

**Fields:**

| Line | Field |
|------|-------|
| 14   | `public String start_time` |
| 15   | `public String finish_time` |
| 16   | `public String comment` |
| 17   | `public int session_id` |
| 18   | `public ArrayList<AnswerItem> arrAnswers` |

**Types / constants / enums / interfaces defined:** none beyond the class itself.

**Imports (lines 3–10):**
- `org.json.JSONException` (line 3)
- `org.json.JSONObject` (line 4)
- `java.io.Serializable` (line 5)
- `org.json.JSONArray` (line 6)
- `java.util.ArrayList` (line 7)
- `java.math.BigDecimal` (line 8)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10)

---

## Step 2 & 3: Findings

### A31-1 — MEDIUM: Unused imports in SaveLicenseParameter and SavePreStartParameter

**Files:**
- `SaveLicenseParameter.java`, lines 3–4, 6–8, 10
- `SavePreStartParameter.java`, lines 3–4, 6–8, 10

**Detail:**
`SaveLicenseParameter` and `SavePreStartParameter` each carry the same set of seven imports that appear to have been copied from a template. None of these imports are used by either class:

| Import | Used in SaveLicenseParameter | Used in SavePreStartParameter |
|--------|------------------------------|-------------------------------|
| `org.json.JSONException` | No | No |
| `org.json.JSONObject` | No | No |
| `org.json.JSONArray` | No | No |
| `java.math.BigDecimal` | No | No |
| `au.com.collectiveintelligence...results.*` (wildcard) | No | No |

The wildcard `webserviceclasses.*` is needed in `SavePreStartParameter` to resolve `AnswerItem` (which lives in that package), but `results.*` is not needed by either file. The explicit JSON and BigDecimal imports are completely unused. `SaveMultipleGPSParameter` does not carry these extraneous imports, confirming the pattern is inconsistent across the parameter class family.

Unused imports are a compiler warning under standard Android lint rules and contribute noise that obscures which dependencies a class actually has.

---

### A31-2 — MEDIUM: Inconsistent import style across sibling parameter classes

**Files:**
- `SaveLicenseParameter.java`, lines 3–10
- `SavePreStartParameter.java`, lines 3–10
- `SaveMultipleGPSParameter.java`, lines 3–7
- (Reference baseline: `SaveSingleGPSParameter.java`, `LoginParameter.java`, `SaveSessionsParameter.java`)

**Detail:**
Three distinct import styles are in use across the nine parameter classes in this package:

1. **Template-bulk style** (`SaveLicenseParameter`, `SavePreStartParameter`, `SaveSessionsParameter`, `LoginParameter`, and several others): wildcard `webserviceclasses.*` plus wildcard `results.*`, plus `JSONException`, `JSONObject`, `JSONArray`, `BigDecimal`, and `ArrayList` regardless of actual usage.

2. **Minimal explicit style** (`SaveMultipleGPSParameter`): only the two imports actually required (`Serializable`, `ArrayList`, plus explicit named imports for `SaveGPSLocationItem` and `WebServiceParameterPacket`).

3. **Minimal hybrid style** (`SaveSingleGPSParameter`): only `Serializable` and the named parent class import — no wildcards, no unused JSON types.

This inconsistency means each class communicates a false picture of its dependencies. A reader of `SaveLicenseParameter` cannot tell whether JSON serialisation logic was removed or was never present. Consistent minimal imports would make dependency intent clear.

---

### A31-3 — MEDIUM: `arrAnswers` field not initialised in `SavePreStartParameter` constructor; NPE risk

**File:** `SavePreStartParameter.java`, line 18 (field), line 20 (constructor)

**Detail:**
`public ArrayList<AnswerItem> arrAnswers` is declared but never initialised in the constructor. The default value is `null`. The companion class `SaveMultipleGPSParameter` (the analogous GPS list parameter) *does* initialise its list field in the constructor:

```java
// SaveMultipleGPSParameter.java line 13 — initialised
public SaveMultipleGPSParameter() {
    gpsList = new ArrayList<>();
}

// SavePreStartParameter.java line 20 — NOT initialised
public SavePreStartParameter() {
}
```

Any caller that adds elements to `arrAnswers` without first checking for null will throw a `NullPointerException`. The call site in `PreStartCheckListPresenter.java` (line 61 onward) constructs a `SavePreStartParameter` and then populates `arrAnswers` by assignment from an externally built list, which avoids the NPE in that path. However, any future caller using `parameter.arrAnswers.add(...)` directly on a freshly constructed instance will crash. The inconsistency between this class and `SaveMultipleGPSParameter` is a latent defect.

---

### A31-4 — LOW: `serialVersionUID` absent on all three classes

**Files:**
- `SaveLicenseParameter.java`, line 12
- `SaveMultipleGPSParameter.java`, line 9
- `SavePreStartParameter.java`, line 12

**Detail:**
All three classes implement `Serializable` (directly declared and inherited through the `WebServiceParameterPacket` → `WebServicePacket` chain). None declares a `serialVersionUID`. Without an explicit `serialVersionUID`, the JVM auto-generates one from the class structure. Any change to the class (adding a field, changing a field type, or altering a method signature) will change the auto-generated UID, causing deserialization of any previously serialized instances to throw `InvalidClassException`.

`SavePreStartParameter` is persisted via Gson string in Realm (`SessionDb`) for offline replay — not via Java serialization directly — so the immediate runtime risk for that class is low. For `SaveLicenseParameter` and `SaveMultipleGPSParameter`, the risk depends on whether `Serializable` is used for inter-process communication or bundle passing. The absence of `serialVersionUID` is a standard Java warning (javac `-Xlint:serial`).

---

### A31-5 — LOW: Field naming convention inconsistency across the parameter family

**Files:**
- `SaveLicenseParameter.java`, lines 14–18
- `SavePreStartParameter.java`, lines 14–18
- `SaveMultipleGPSParameter.java`, line 10

**Detail:**
The fields in these classes follow snake_case naming (`licno`, `addr`, `expirydt`, `securityno`, `start_time`, `finish_time`, `session_id`, `arrAnswers`, `gpsList`). This is a deliberate design choice to match JSON API field names for Gson serialization without custom `@SerializedName` annotations. However, the naming is internally inconsistent:

- `arrAnswers` in `SavePreStartParameter` uses a Hungarian-notation prefix (`arr`) combined with camelCase — inconsistent with the other snake_case fields in the same class (`start_time`, `finish_time`, `session_id`).
- `gpsList` in `SaveMultipleGPSParameter` uses camelCase with a suffix — inconsistent with snake_case fields in sibling classes.

The inconsistency within `SavePreStartParameter` (snake_case fields alongside one camelCase/Hungarian field) is particularly notable because the Gson serialization will produce the key `"arrAnswers"` for the array, while the server API likely expects a different key name (e.g., `"arr_answers"` or `"answers"`). If the server uses a different name, the field will silently serialize with the wrong key and its data will be dropped.

---

### A31-6 — LOW: Redundant `implements Serializable` declaration

**Files:**
- `SaveLicenseParameter.java`, line 12
- `SavePreStartParameter.java`, line 12

**Detail:**
Both classes declare `implements Serializable` explicitly while also extending `WebServiceParameterPacket`. Inspection of the inheritance chain shows:

```
SaveLicenseParameter → WebServiceParameterPacket → WebServicePacket → (implements Serializable via WebServiceParameterPacket)
```

`WebServiceParameterPacket` itself already declares `implements Serializable`. The re-declaration in the subclass is redundant (though not incorrect). `SaveMultipleGPSParameter` also re-declares it, so this is a consistent pattern in the family, but it is unnecessary boilerplate.

---

### A31-7 — INFO: Extra blank line inside `SaveGPSLocationItem` constructor has no counterpart in the parameter classes

**File:** `SaveMultipleGPSParameter.java`, line 10 (field type reference)

**Detail:**
This is an informational observation about the `SaveGPSLocationItem` type referenced by `SaveMultipleGPSParameter`. `SaveGPSLocationItem` has a convenience constructor `SaveGPSLocationItem(LocationDb gps)` that copies fields from a Realm `LocationDb` model. This is a form of tight coupling: the web-service DTO layer directly depends on the Realm model class. If `LocationDb` changes (column renamed, type changed), `SaveGPSLocationItem` must also change. No equivalent coupling concern exists in the other two parameter classes under audit. This is noted for completeness; the leaky abstraction was introduced in `SaveGPSLocationItem`, not in `SaveMultipleGPSParameter` itself.

---

## Step 4: Summary Table

| ID     | Severity | File(s)                                                  | Description |
|--------|----------|----------------------------------------------------------|-------------|
| A31-1  | MEDIUM   | SaveLicenseParameter.java, SavePreStartParameter.java    | Five or more unused imports in each file (JSON types, BigDecimal, results wildcard); compiler warnings, obscures actual dependencies |
| A31-2  | MEDIUM   | All three files (and sibling parameter classes)          | Three distinct import styles in use across the parameter class family; no consistent convention |
| A31-3  | MEDIUM   | SavePreStartParameter.java                               | `arrAnswers` field not initialised in constructor, unlike analogous `gpsList` in SaveMultipleGPSParameter; NPE risk for direct-add callers |
| A31-4  | LOW      | All three files                                          | No `serialVersionUID` declared on any Serializable class; class changes will break deserialization silently |
| A31-5  | LOW      | SavePreStartParameter.java, SaveMultipleGPSParameter.java | Mixed field naming conventions (snake_case, camelCase, Hungarian) within and across classes; `arrAnswers` key may not match server API expectation |
| A31-6  | LOW      | SaveLicenseParameter.java, SavePreStartParameter.java    | Redundant `implements Serializable` declaration; parent class already declares it |
| A31-7  | INFO     | SaveMultipleGPSParameter.java (via SaveGPSLocationItem)  | `SaveGPSLocationItem` is tightly coupled to Realm `LocationDb` model via convenience constructor; DTO depends on persistence layer |
