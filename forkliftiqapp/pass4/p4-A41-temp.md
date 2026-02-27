# Audit Report — Pass 4 (Code Quality)
**Agent:** A41
**Audit run:** 2026-02-26-01
**Date:** 2026-02-27

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/SaveSingleGPSResult.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ServiceRecordResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ServiceSummaryResultArray.java`

---

## Step 1: Reading Evidence

### File 1: SaveSingleGPSResult.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/SaveSingleGPSResult.java`

**Class name:**
`SaveSingleGPSResult` — extends `WebServiceResultPacket`, implements `Serializable`

**Package:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results`

**Imports:**
- Line 3: `org.json.JSONException`
- Line 4: `org.json.JSONObject`
- Line 6: `java.io.Serializable`
- Line 8: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServiceResultPacket`

**Fields (all public):**
- Line 12: `public int unit_id`
- Line 13: `public Double longitude`  (boxed)
- Line 14: `public Double latitude`   (boxed)
- Line 15: `public String gps_time`

**Methods (exhaustive):**
| Line | Signature |
|------|-----------|
| 17 | `public SaveSingleGPSResult()` — no-arg constructor |
| 20 | `public SaveSingleGPSResult(JSONObject jsonObject) throws JSONException` — JSON-parsing constructor |

**Types / constants / enums / interfaces defined:** None.

**Observations:**
- No `serialVersionUID` despite implementing `Serializable`.
- No superclass `super(jsonObject)` call is missing — it IS present at line 22.
- Indentation uses 4 spaces throughout (consistent with `SaveMultipleGPSResult`).
- `unit_id` is a primitive `int`; `longitude` and `latitude` are boxed `Double`, meaning they can be `null` if the JSON key is absent.
- No type constants, no enums, no nested types.

---

### File 2: ServiceRecordResultArray.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ServiceRecordResultArray.java`

**Class name:**
`ServiceRecordResultArray` — extends `WebServiceResultPacket`, implements `Serializable`

**Package:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results`

**Imports:**
- Line 3: `org.json.JSONException`
- Line 4: `org.json.JSONObject`  (UNUSED — constructor takes `JSONArray`, not `JSONObject`)
- Line 5: `java.io.Serializable`
- Line 6: `org.json.JSONArray`
- Line 7: `java.util.ArrayList`
- Line 8: `java.math.BigDecimal`  (UNUSED)
- Line 9: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`  (wildcard; `WebServiceResultPacket` is already in parent package, `ServiceRecordItem` is in this package)
- Line 10: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`  (SELF-IMPORT — class is itself in this package)

**Fields (all public):**
- Line 14: `public ArrayList<ServiceRecordItem> arrayList`

**Methods (exhaustive):**
| Line | Signature |
|------|-----------|
| 16 | `public ServiceRecordResultArray()` — no-arg constructor; leaves `arrayList` null |
| 19 | `public ServiceRecordResultArray(JSONArray jsonArray) throws JSONException` — JSON-parsing constructor |

**Types / constants / enums / interfaces defined:** None.

**Observations:**
- No `serialVersionUID` despite implementing `Serializable`.
- No-arg constructor leaves `arrayList` as `null` (not initialized).
- Indentation uses tabs (not 4 spaces). This differs from `SaveSingleGPSResult.java` which uses 4 spaces.
- There is a leading space on the `for` keyword at line 25 (`·for`) beyond the tab indentation — inconsistent within the file.
- `JSONObject` is imported but never used in this class (the constructor takes `JSONArray`).
- `BigDecimal` is imported but not used.
- The `results.*` wildcard imports the class's own package — a self-import.
- The `super()` call (passing `jsonObject` / `jsonArray`) is absent from both constructors. Neither constructor chains to `WebServiceResultPacket`. The no-arg constructor body is empty; the JSON constructor never calls `super(...)`.

---

### File 3: ServiceSummaryResultArray.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/ServiceSummaryResultArray.java`

**Class name:**
`ServiceSummaryResultArray` — extends `WebServiceResultPacket`, implements `Serializable`

**Package:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results`

**Imports:**
- Line 3: `org.json.JSONException`
- Line 4: `org.json.JSONObject`  (UNUSED)
- Line 5: `java.io.Serializable`
- Line 6: `org.json.JSONArray`
- Line 7: `java.util.ArrayList`
- Line 8: `java.math.BigDecimal`  (UNUSED)
- Line 9: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- Line 10: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`  (SELF-IMPORT)

**Fields (all public):**
- Line 14: `public ArrayList<ServiceSummaryItem> arrayList`

**Methods (exhaustive):**
| Line | Signature |
|------|-----------|
| 16 | `public ServiceSummaryResultArray()` — no-arg constructor; leaves `arrayList` null |
| 19 | `public ServiceSummaryResultArray(JSONArray jsonArray) throws JSONException` — JSON-parsing constructor |

**Types / constants / enums / interfaces defined:** None.

**Observations:**
- No `serialVersionUID` despite implementing `Serializable`.
- No-arg constructor leaves `arrayList` as `null`.
- Indentation uses tabs (matches `ServiceRecordResultArray`, differs from `SaveSingleGPSResult`).
- Same leading space anomaly on `for` at line 25 (`·for`).
- `JSONObject` is imported but never used.
- `BigDecimal` is imported but not used.
- Self-import of the class's own package via `results.*`.
- Neither constructor calls `super(...)`.
- No callers found in any production Java source file. `ServiceSummaryResultArray` and `ServiceSummaryItem` are referenced only in their own definition files — the class appears to be dead code in the production codebase.

---

## Step 2 & 3: Code Quality Findings

---

### A41-1 — MEDIUM — `ServiceSummaryResultArray` is unreferenced in production code (dead class)

**File:** `ServiceSummaryResultArray.java`
**Lines:** 12–31

**Description:**
A search across the entire `app/src/main/java` tree finds zero usages of `ServiceSummaryResultArray` outside its own definition file. No `WebApi` method accepts or returns this type; no fragment, activity, service, or adapter imports or instantiates it. The companion item class `ServiceSummaryItem` is similarly unreferenced outside its own source.

The class occupies the results package, carries the same fields and semantics as `ServiceRecordResultArray` (same JSON field names: `unit_id`, `acc_hours`, `service_due`, `last_serv`, `next_serv`, `serv_duration`, `unit_name`, `service_type`), but is never wired to a `WebApi` endpoint. This is dead code that inflates the compiled artifact and misleads maintainers.

**Evidence:**
```
# grep across app/src/main/java — matches only the definition file itself:
ServiceSummaryResultArray.java:12:public class ServiceSummaryResultArray ...
ServiceSummaryResultArray.java:16:    public ServiceSummaryResultArray()
ServiceSummaryResultArray.java:19:    public ServiceSummaryResultArray(JSONArray ...
ServiceSummaryResultArray.java:26:        ServiceSummaryItem temp = ...
```

**Recommendation:** Confirm with the team whether a `getServiceSummary` endpoint was planned but never implemented. If so, either wire it or delete the class and its companion `ServiceSummaryItem`.

---

### A41-2 — MEDIUM — `acc_hours` type divergence between `ServiceRecordItem` (double) and `ServiceSummaryItem` (int)

**Files:**
- `ServiceRecordItem.java` line 14: `public double acc_hours`
- `ServiceSummaryItem.java` line 15: `public int acc_hours`

**Description:**
Both item classes parse the same JSON field name `"acc_hours"` from what is stated to be a related API (service record vs service summary). `ServiceRecordItem` uses `double` (parsed via `getDouble`), while `ServiceSummaryItem` uses `int` (parsed via `getInt`). The two classes describe overlapping data about the same fleet units and service intervals; the remaining fields (`unit_id`, `last_serv`, `next_serv`, `serv_duration`, `unit_name`, `service_type`) share identical names and types.

This divergence indicates one of the following problems:
1. The summary endpoint intentionally truncates fractional hours, but callers would lose precision silently.
2. One type is wrong — if the server returns a decimal, `getInt` will succeed only when the JSON value is an integer, and will throw `JSONException` for a fractional value.
3. The summary class was copied from the record class and its type was changed without clear justification.

Because `ServiceSummaryResultArray` has no production callers this cannot currently cause a runtime failure, but it is a latent defect that would manifest if the endpoint is ever wired.

**Recommendation:** Align the type for `acc_hours` across both item classes based on the actual API contract.

---

### A41-3 — MEDIUM — No-arg constructor leaves `arrayList` null in both array result classes

**Files:**
- `ServiceRecordResultArray.java` line 16
- `ServiceSummaryResultArray.java` line 16

**Description:**
Both no-arg constructors are empty. `arrayList` is never initialized in the no-arg path. Any caller that constructs via `new ServiceRecordResultArray()` and then accesses `.arrayList` (including the for-each loop in `ServiceRecordFragment.onData()`) will receive a `NullPointerException`.

The Gson/Volley deserialization infrastructure (`GsonRequest`) instantiates via the no-arg constructor and then populates fields via field injection. If Gson does not inject `arrayList`, or if the class is instantiated directly by application code, null-safety is violated.

In contrast, `SaveSingleGPSResult` initializes all its primitive and boxed fields only via the JSON constructor; there is no analogous ArrayList field at risk.

**Recommendation:** Initialize `arrayList` at the field declaration site: `public ArrayList<ServiceRecordItem> arrayList = new ArrayList<>();`.

---

### A41-4 — LOW — Missing `super()` call in JSON-parsing constructors of both array result classes

**Files:**
- `ServiceRecordResultArray.java` line 19
- `ServiceSummaryResultArray.java` line 19

**Description:**
`ServiceRecordResultArray` and `ServiceSummaryResultArray` each extend `WebServiceResultPacket`, which itself has a `WebServiceResultPacket(JSONObject jsonObject)` constructor that (after review) chains to `WebServicePacket(JSONObject)`. The array classes' JSON-parsing constructors (`(JSONArray)`) cannot directly call the parent `(JSONObject)` constructor with the array payload, but they also make no `super()` call at all, meaning the no-arg `super()` is invoked implicitly. This leaves any state initialized in the parent's JSON constructor (currently empty in `WebServiceResultPacket`, but subject to future change) unpopulated.

`SaveSingleGPSResult` correctly calls `super(jsonObject)` from its JSON constructor (line 22). The array classes use a different constructor signature (`JSONArray`) so direct parity is impossible, but the absence of even a `super()` call is a structural inconsistency that makes the inheritance chain fragile to future parent changes.

**Recommendation:** Confirm that the no-arg super is intentional for array types and document this in a comment.

---

### A41-5 — LOW — Unused imports: `JSONObject`, `BigDecimal`, and self-package wildcard in both array result classes

**Files:**
- `ServiceRecordResultArray.java` lines 4, 8, 10
- `ServiceSummaryResultArray.java` lines 4, 8, 10

**Description:**
Each of the two array result classes carries three categories of unused imports:

1. `import org.json.JSONObject` (line 4) — Neither class has a method that accepts or uses a `JSONObject`. The constructor signature is `(JSONArray)`. This import is dead.

2. `import java.math.BigDecimal` (line 8) — Neither class references `BigDecimal`. This is a template artifact (the same unused `BigDecimal` import appears in 40+ files across the `webserviceclasses` package tree).

3. `import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10) — Both files are themselves in the `results` package. A class cannot import its own package; on Android/Java toolchains this is silently ignored, but it is noise that obscures the real dependency surface and falsely suggests cross-package coupling.

These would appear as compiler warnings (unused imports) with standard Android Studio / lint configuration.

**Recommendation:** Remove all three unused import categories from both files. The `BigDecimal` template import should be addressed globally across the `webserviceclasses` package tree.

---

### A41-6 — LOW — Missing `serialVersionUID` on all three `Serializable` classes

**Files:**
- `SaveSingleGPSResult.java` line 10
- `ServiceRecordResultArray.java` line 12
- `ServiceSummaryResultArray.java` line 12

**Description:**
All three classes implement `java.io.Serializable` but declare no `private static final long serialVersionUID`. When `serialVersionUID` is absent the JVM computes one from the class structure. Any change to fields, method signatures, or the class hierarchy will silently change the computed UID, making previously serialized instances unreadable and causing `InvalidClassException` at deserialization.

On Android, serialization is commonly used for `Intent` extras and `Bundle` values (since these types extend `WebServiceResultPacket implements Serializable`). A field addition or refactoring between app versions — including OTA updates — would break deserialization of any instance stored before the update.

This finding applies to all three assigned files and is a project-wide pattern (zero `serialVersionUID` declarations found anywhere in the `webserviceclasses` tree).

**Recommendation:** Declare `private static final long serialVersionUID = 1L;` (or a version generated by the IDE) in all `Serializable` classes.

---

### A41-7 — LOW — Indentation inconsistency: tabs in array result classes vs spaces in GPS result class

**Files:**
- `SaveSingleGPSResult.java` — uses 4-space indentation throughout
- `ServiceRecordResultArray.java` — uses tab indentation
- `ServiceSummaryResultArray.java` — uses tab indentation

**Description:**
The three files in the same `results` package use two different indentation characters. `SaveSingleGPSResult.java` follows 4-space indentation (consistent with `SaveMultipleGPSResult.java`). Both array result files use tabs. Mixed indentation in the same package complicates diffs, code review, and editor configuration.

Additionally, within `ServiceRecordResultArray.java` (line 25) and `ServiceSummaryResultArray.java` (line 25), there is an extraneous leading space before the `for` keyword (a tab followed by a space, then `for`), indicating the files were not consistently formatted even within themselves.

**Recommendation:** Standardize all files in the package to a single indentation style and enforce it via the project's `.editorconfig` or Android Studio code style settings.

---

### A41-8 — LOW — Style inconsistency: `for` loop brace placement differs between the two array result classes and the broader codebase

**Files:**
- `ServiceRecordResultArray.java` line 25: closing brace of `for` body on line 28 (Allman style for outer braces, K&R for `for` body: `for (...){`)
- `ServiceSummaryResultArray.java` line 25: same mixed style

**Description:**
The outer `if` blocks use Allman-style (opening brace on its own line, lines 23–24, 29), while the `for` loop on line 25 uses K&R style (opening brace on the same line as the `for` keyword: `for (int i ...){`). Within the same file, brace placement is inconsistent. This is a minor style issue but contributes to the overall impression that these files were machine-generated and not reviewed.

---

### A41-9 — INFO — `ServiceRecordResultArray` and `ServiceSummaryResultArray` are structurally identical modulo item type

**Files:**
- `ServiceRecordResultArray.java`
- `ServiceSummaryResultArray.java`

**Description:**
The two classes are byte-for-byte identical except for the item type (`ServiceRecordItem` vs `ServiceSummaryItem`) and the class name. Their fields, constructors, import lists, and logic are otherwise duplicated. This is a generics opportunity: a parameterized base class or a shared static factory would eliminate the duplication. Because `ServiceSummaryResultArray` is currently unreferenced (finding A41-1), the duplication has no runtime impact, but it doubles the maintenance surface if the pattern is ever extended.

---

## Summary Table

| ID | Severity | File(s) | Description |
|----|----------|---------|-------------|
| A41-1 | MEDIUM | ServiceSummaryResultArray.java | Class is unreferenced in all production Java source — dead code |
| A41-2 | MEDIUM | ServiceRecordItem.java / ServiceSummaryItem.java | `acc_hours` is `double` in one item class and `int` in the other — type divergence for the same JSON field |
| A41-3 | MEDIUM | ServiceRecordResultArray.java, ServiceSummaryResultArray.java | No-arg constructor leaves `arrayList` null; NPE risk on caller access |
| A41-4 | LOW | ServiceRecordResultArray.java, ServiceSummaryResultArray.java | JSON-parsing constructor makes no `super()` call; parent initialization not guaranteed |
| A41-5 | LOW | ServiceRecordResultArray.java, ServiceSummaryResultArray.java | Unused imports: `JSONObject`, `BigDecimal`, self-package wildcard |
| A41-6 | LOW | All three assigned files | `Serializable` classes lack `serialVersionUID`; deserialization incompatibility risk across versions |
| A41-7 | LOW | All three assigned files | Mixed indentation (spaces vs tabs) across files in the same package; extra space inside `for` line |
| A41-8 | LOW | ServiceRecordResultArray.java, ServiceSummaryResultArray.java | Inconsistent brace placement: Allman for outer blocks, K&R for `for` loop in same file |
| A41-9 | INFO | ServiceRecordResultArray.java, ServiceSummaryResultArray.java | Classes are structural duplicates of each other; generics could eliminate duplication |
