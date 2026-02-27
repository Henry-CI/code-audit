# Pass 4 — Code Quality Audit
**Agent:** A23
**Audit Run:** 2026-02-26-01
**Files Assigned:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/LoginItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/ManufactureItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/PermissionItem.java`

---

## Step 1: Reading Evidence

### File 1: LoginItem.java

**Class:** `LoginItem implements Serializable`

**Fields (all public):**
- Line 15: `public int id`
- Line 16: `public int comp_id`
- Line 17: `public String first_name`
- Line 18: `public String last_name`
- Line 19: `public String email`
- Line 20: `public String password`
- Line 21: `public String phone`
- Line 22: `public String licno`
- Line 23: `public String expirydt`
- Line 24: `public String addr`
- Line 25: `public String securityno`
- Line 26: `public String photo_url`
- Line 27: `public boolean contactperson`
- Line 28: `public String date_format`
- Line 29: `public int max_session_length`
- Line 30: `public String compliance_date`
- Line 31: `public int gps_frequency`
- Line 33: `public List<LoginItem> drivers` (initialized as `new ArrayList<>()`)
- Line 34: `public List<TrainingItem> arrDriverTrainings` (initialized as `new ArrayList<TrainingItem>()`)

**Methods:**
- Line 36–77: `public LoginItem(JSONObject jsonObject) throws JSONException` — constructor; parses JSON using `JSONObjectParser`; populates `arrDriverTrainings` list (lines 60–67) and, conditionally, `drivers` list (lines 69–76)

**Imports:**
- `android.util.Log` (line 3)
- `JSONObjectParser` (line 5)
- `org.json.JSONArray`, `JSONException`, `JSONObject` (lines 6–8)
- `java.io.Serializable`, `java.util.ArrayList`, `java.util.List` (lines 10–12)

**Types/interfaces defined:** None beyond the class itself.

---

### File 2: ManufactureItem.java

**Class:** `ManufactureItem implements Serializable`

**Fields (all public):**
- Line 14: `public int id`
- Line 15: `public String name`

**Methods:**
- Line 17–18: `public ManufactureItem()` — no-arg constructor (empty body)
- Line 20–35: `public ManufactureItem(JSONObject jsonObject) throws JSONException` — constructor; parses `id` and `name` directly from `JSONObject` with null guards

**Imports:**
- `org.json.JSONException`, `JSONObject` (lines 3–4)
- `java.io.Serializable` (line 5)
- `org.json.JSONArray` (line 6)
- `java.util.ArrayList` (line 7)
- `java.math.BigDecimal` (line 8)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10)

**Types/interfaces defined:** None beyond the class itself.

---

### File 3: PermissionItem.java

**Class:** `PermissionItem implements Serializable`

**Fields (all public):**
- Line 14: `public int id`
- Line 15: `public int driver_id`
- Line 16: `public String driver_name`
- Line 17: `public int comp_id`
- Line 18: `public String enabled`
- Line 19: `public String gsm_token`

**Methods:**
- Line 21–22: `public PermissionItem()` — no-arg constructor (empty body)
- Line 24–59: `public PermissionItem(JSONObject jsonObject) throws JSONException` — constructor; parses all fields directly from `JSONObject` with per-field null guards

**Imports:**
- `org.json.JSONException`, `JSONObject` (lines 3–4)
- `java.io.Serializable` (line 5)
- `org.json.JSONArray` (line 6)
- `java.util.ArrayList` (line 7)
- `java.math.BigDecimal` (line 8)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10)

**Types/interfaces defined:** None beyond the class itself.

---

## Step 2 & 3: Findings

---

### A23-1 — HIGH — Plaintext password stored in public field (LoginItem.java, line 20)

`LoginItem` has a `public String password` field that is populated directly from the JSON response (line 47) and stored as plaintext in the object. The class implements `Serializable`, meaning the password value will be included in any serialized form (e.g., written to disk via `Intent` extras, object streams, or `SharedPreferences`). There is no transient modifier, no masking, and no indication that the value is hashed before storage. This is a security-class defect surfaced during a code quality pass because there is no protective pattern (e.g., `transient` keyword, dedicated credential wrapper) in place.

**File:** `LoginItem.java`, line 20
```java
public String password;
```
And populated at line 47:
```java
password = parser.getString("password");
```

---

### A23-2 — HIGH — Unused import `android.util.Log` (LoginItem.java, line 3)

`android.util.Log` is imported but never referenced anywhere in `LoginItem.java`. This generates a compiler/lint warning and is a build hygiene issue. More significantly, it may indicate that logging of sensitive login data (including the password field) was previously present and was removed by deleting only the log call but not the import — or that logging is intended to be added. Either case warrants attention.

**File:** `LoginItem.java`, line 3
```java
import android.util.Log;
```

---

### A23-3 — HIGH — Wildcard self-import and unused wildcard imports (ManufactureItem.java lines 9–10; PermissionItem.java lines 9–10)

Both `ManufactureItem.java` and `PermissionItem.java` import their own package via wildcard:
```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```
Neither class uses any type from these imports (or from `JSONArray`, `ArrayList`, `BigDecimal` — see A23-4). Wildcard imports from the class's own package are meaningless in Java. Wildcard imports from unrelated packages that are wholly unused inflate the classpath surface, make dependency analysis difficult, and will produce lint/IDE warnings. The `results.*` import in particular pulls in an unknown set of types with no justification.

**Files:** `ManufactureItem.java` lines 9–10; `PermissionItem.java` lines 9–10

---

### A23-4 — MEDIUM — Multiple unused imports across ManufactureItem and PermissionItem

The following imports are present in both `ManufactureItem.java` and `PermissionItem.java` but are entirely unused by the class body:

| Import | File(s) |
|--------|---------|
| `org.json.JSONArray` | ManufactureItem.java line 6; PermissionItem.java line 6 |
| `java.util.ArrayList` | ManufactureItem.java line 7; PermissionItem.java line 7 |
| `java.math.BigDecimal` | ManufactureItem.java line 8; PermissionItem.java line 8 |

Neither class holds a list field or performs any arithmetic. These are likely cargo-culted from a template. They generate lint warnings and make intent unclear.

---

### A23-5 — MEDIUM — Inconsistent JSON parsing strategy across sibling classes (style inconsistency)

`LoginItem` uses `JSONObjectParser` (a null-safe wrapper) for all field parsing, whereas `ManufactureItem` and `PermissionItem` call `JSONObject` methods directly with per-field `isNull` guards. The two approaches achieve the same result but are maintained differently: `JSONObjectParser` centralises the null-defaulting logic; the direct approach scatters it. All three classes live in the same package and represent the same design pattern (JSON DTO). Using two incompatible strategies in sibling classes is a style inconsistency that increases maintenance cost.

**LoginItem.java** (lines 42–58):
```java
JSONObjectParser parser = new JSONObjectParser(jsonObject);
id = parser.getInt("id");
first_name = parser.getString("first_name");
```

**ManufactureItem.java** (lines 25–33) and **PermissionItem.java** (lines 29–57):
```java
if (!jsonObject.isNull("id")) {
    id = jsonObject.getInt("id");
}
```

---

### A23-6 — MEDIUM — `enabled` field typed as `String` instead of `boolean` (PermissionItem.java, line 18)

`PermissionItem.enabled` is declared as `public String enabled` but semantically represents an on/off flag (field name is `enabled`). Storing a boolean concept as a `String` forces every consumer to perform string comparison (e.g., `"true"`, `"1"`, `"yes"`) with no type enforcement. This is a leaky abstraction — the internal wire-format detail (the server sending a string representation) is exposed directly in the public API of the class rather than being normalised at parse time. Contrast with `LoginItem.contactperson` which is correctly typed as `boolean` (line 27).

**File:** `PermissionItem.java`, line 18
```java
public String enabled;
```

---

### A23-7 — MEDIUM — All fields public with no encapsulation across all three classes

All three classes expose every field as `public` with no accessor methods and no validation. While this is a common (if discouraged) pattern for simple DTOs in Android, it means:
- The `Serializable` contract cannot exclude sensitive fields without the `transient` keyword.
- Field values can be mutated by any caller after construction with no invariant checks.
- The `LoginItem.password` field (see A23-1) in particular is directly readable by any class that holds a `LoginItem` reference.

This is a systemic design issue across all three files. Reported once at MEDIUM to avoid duplicating A23-1.

---

### A23-8 — MEDIUM — `LoginItem.arrDriverTrainings` bypasses `JSONObjectParser` for null guard (LoginItem.java, lines 60–67)

The `arrDriverTrainings` array is populated using a direct `jsonObject.isNull()` call (line 60) rather than `parser.getJSONArray()`, which is inconsistent with the rest of the constructor that uses `parser` for all other fields. This is a localised style inconsistency within a single method.

**File:** `LoginItem.java`, lines 60–67
```java
if (!jsonObject.isNull("arrDriverTrainings"))
{
    JSONArray jsonArray = jsonObject.getJSONArray("arrDriverTrainings");
    ...
}
```
Compare with the consistent use of `parser.getJSONArray("drivers")` at line 70.

---

### A23-9 — LOW — Inconsistent brace style between LoginItem and ManufactureItem/PermissionItem

`LoginItem.java` uses same-line opening braces (K&R style) throughout. `ManufactureItem.java` and `PermissionItem.java` use next-line opening braces (Allman style) for class and method declarations. This is a style inconsistency across sibling files in the same package.

**LoginItem.java** (line 36):
```java
public LoginItem(JSONObject jsonObject) throws JSONException {
```

**ManufactureItem.java** (line 20–21):
```java
public ManufactureItem(JSONObject jsonObject) throws JSONException
{
```

---

### A23-10 — LOW — Diamond operator not used in `LoginItem.java` line 34

`LoginItem.java` line 33 correctly uses the diamond operator (`new ArrayList<>()`), but line 34 uses the verbose form `new ArrayList<TrainingItem>()`. This is a minor style inconsistency within the same file; the diamond operator was available since Java 7.

**File:** `LoginItem.java`, lines 33–34
```java
public List<LoginItem> drivers = new ArrayList<>();
public List<TrainingItem> arrDriverTrainings = new ArrayList<TrainingItem>();
```

---

### A23-11 — LOW — Trailing whitespace on blank lines inside constructor body (ManufactureItem.java, PermissionItem.java)

`ManufactureItem.java` lines 24 and 28 and `PermissionItem.java` lines 28, 32, 36, 40, 44, 48, 52 contain blank lines with leading tab characters (trailing whitespace). This is a minor formatting hygiene issue that produces diff noise.

---

### A23-12 — INFO — No-arg constructor present in ManufactureItem and PermissionItem but not LoginItem

`ManufactureItem` and `PermissionItem` both expose a public no-arg constructor. `LoginItem` does not. If any framework (e.g., a reflection-based serializer) expects a no-arg constructor on all DTOs, `LoginItem` will fail at runtime while the other two succeed. This asymmetry may be intentional but is worth confirming.

---

## Summary Table

| ID | Severity | File(s) | Description |
|----|----------|---------|-------------|
| A23-1 | HIGH | LoginItem.java:20,47 | Plaintext password in public Serializable field |
| A23-2 | HIGH | LoginItem.java:3 | Unused import `android.util.Log` — possible removed logging of sensitive data |
| A23-3 | HIGH | ManufactureItem.java:9-10; PermissionItem.java:9-10 | Wildcard self-import and unused wildcard `results.*` import |
| A23-4 | MEDIUM | ManufactureItem.java:6-8; PermissionItem.java:6-8 | Unused imports: JSONArray, ArrayList, BigDecimal |
| A23-5 | MEDIUM | All three files | Inconsistent JSON parsing strategy: JSONObjectParser vs direct JSONObject calls |
| A23-6 | MEDIUM | PermissionItem.java:18 | `enabled` field typed as String instead of boolean — leaky wire-format abstraction |
| A23-7 | MEDIUM | All three files | All fields public, no encapsulation, no transient on sensitive fields |
| A23-8 | MEDIUM | LoginItem.java:60-67 | `arrDriverTrainings` bypasses JSONObjectParser within same constructor |
| A23-9 | LOW | All three files | Inconsistent brace style between files (K&R vs Allman) |
| A23-10 | LOW | LoginItem.java:34 | Diamond operator omitted in ArrayList initialisation |
| A23-11 | LOW | ManufactureItem.java; PermissionItem.java | Trailing whitespace on blank lines inside constructor |
| A23-12 | INFO | ManufactureItem.java; PermissionItem.java | No-arg constructor present in 2 of 3 DTO classes — asymmetric |
