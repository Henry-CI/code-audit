# Pass 4 — Code Quality Audit
**Agent:** A46
**Audit run:** 2026-02-26-01
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/LocationDb.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/ModelPrefs.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/MyCommonValue.java`

---

## Step 1: Reading Evidence

### File 1: `LocationDb.java`

**Class:** `LocationDb extends RealmObject`
**Package:** `au.com.collectiveintelligence.fleetiq360.model`

**Fields (all public):**
- `public static String TAG` — line 24
- `@SuppressWarnings("unused") public int userKey` — line 25–26 (initialized from `WebData.instance().getUserId()`)
- `public int unit_id` — line 28
- `public Double longitude` — line 29
- `public Double latitude` — line 30
- `public String gps_time` — line 31

**Methods (exhaustive):**
| Line | Visibility | Name | Signature |
|------|------------|------|-----------|
| 33 | `public static` | `readAllLocationToSync` | `() -> ArrayList<LocationDb>` |
| 43 | `static` (package-private) | `readData` | `(Realm realm) -> RealmResults<LocationDb>` |
| 47 | `public static` | `removeData` | `(SaveSingleGPSParameter) -> void` |
| 64 | `static` (package-private) | `removeData` | `(Realm, SaveMultipleGPSParameter) -> void` |
| 76 | `private static` | `getMatchingRecord` | `(Realm, int) -> RealmResults<LocationDb>` |
| 81 | `public static` | `uploadLocation` | `() -> void` |
| 112 | `public static` | `saveNewLocation` | `(SaveSingleGPSParameter) -> void` |

**Imports:**
- `android.support.annotation.NonNull` — line 3 (legacy support library)
- `au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventService` — line 8
- `au.com.collectiveintelligence.fleetiq360.WebService.WebApi` — line 9
- `au.com.collectiveintelligence.fleetiq360.WebService.WebData` — line 10
- `au.com.collectiveintelligence.fleetiq360.WebService.WebListener` — line 11
- `au.com.collectiveintelligence.fleetiq360.WebService.WebResult` — line 12
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveGPSLocationItem` — line 13
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveMultipleGPSParameter` — line 14
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveSingleGPSParameter` — line 15
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveMultipleGPSResult` — line 16
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveSingleGPSResult` — line 17
- `io.realm.Realm`, `RealmObject`, `RealmQuery`, `RealmResults` — lines 18–21

**Annotations:**
- `@SuppressWarnings("unused")` on `userKey` field — line 25

**Types/constants defined:** None beyond the class itself.

---

### File 2: `ModelPrefs.java`

**Class:** `ModelPrefs`
**Package:** `au.com.collectiveintelligence.fleetiq360.model`
**Author comment:** "Created by steveyang on 20/11/2015."

**Fields:** None declared.

**Methods (exhaustive):**
| Line | Visibility | Name | Signature |
|------|------------|------|-----------|
| 16 | `static` (package-private) | `getPref` | `() -> SharedPreferences` |
| 22 | `public static` | `saveInt` | `(String key, int d) -> void` |
| 26 | `public static` | `readInt` | `(String key) -> int` |
| 31 | `public static` | `deleteDataForKey` | `(String key) -> void` |
| 36 | `public static` | `saveString` | `(String key, String s) -> void` |
| 40 | `public static` | `readString` | `(String key) -> String` |
| 45 | `public static` | `saveBoolean` | `(String key, boolean s) -> void` |
| 49 | `public static` | `readBoolean` | `(String key) -> boolean` |
| 53 | `public static` | `saveObject` | `(String key, Object object) -> void` |
| 61 | `public static` | `readObject` | `(String key, Class<?> classType) -> Object` |

**Imports:**
- `android.content.Context` — line 3
- `android.content.SharedPreferences` — line 4
- `com.yy.libcommon.WebService.GsonHelper` — line 6
- `au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication` — line 7

**Types/constants defined:** None.

---

### File 3: `MyCommonValue.java`

**Class:** `MyCommonValue`
**Package:** `au.com.collectiveintelligence.fleetiq360.model`
**Author comment:** "Created by Administrator on 2017/6/18."

**Fields (all public static):**
- `public static EquipmentItem currentEquipmentItem` — line 10, initialized to `null`
- `public static Boolean isCheckLocationPermissionDone` — line 11, initialized to `false`
- `public static String companyName` — line 13, initialized to `""`
- `public static String companyContract` — line 14, initialized to `""`
- `public static String companyRole` — line 15, initialized to `""`
- `public static String companyenabled` — line 16, initialized to `""`

**Methods:** None.

**Imports:**
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.EquipmentItem` — line 3

**Types/constants/enums:** None.

---

## Step 2 & 3: Findings

---

### A46-1 — HIGH — `LocationDb.java`: Unused import `ShockEventService` (dead import / wrong-module coupling)

**File:** `LocationDb.java`, line 8
**Category:** Dead code / Leaky abstraction

```java
import au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventService;
```

`ShockEventService` is imported but never referenced anywhere in `LocationDb.java`. Cross-module confirmation shows this class is unrelated to GPS/location logic (it is a BLE shock-event service). This import is an artifact of copy-paste from a BLE-related file and introduces a spurious compile-time dependency between the location model and the BLE subsystem. It should be deleted.

---

### A46-2 — HIGH — `LocationDb.java`: Unused import `SaveSingleGPSResult` (dead import)

**File:** `LocationDb.java`, line 17
**Category:** Dead code

```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveSingleGPSResult;
```

`SaveSingleGPSResult` is imported but never referenced in `LocationDb.java`. The only API call in this file uses `SaveMultipleGPSResult`. This is a dead import.

---

### A46-3 — HIGH — `LocationDb.java`: Unused import `RealmQuery` (dead import)

**File:** `LocationDb.java`, line 20
**Category:** Dead code

```java
import io.realm.RealmQuery;
```

`RealmQuery` is imported but never used directly; the query chain returns `RealmResults` directly from fluent calls on `realm.where(...)`. This dead import will cause a build warning in IDEs and static analysis tools.

---

### A46-4 — HIGH — `LocationDb.java`: `@SuppressWarnings("unused")` on `userKey` suppresses a legitimate dead-field warning

**File:** `LocationDb.java`, lines 25–26
**Category:** Build warnings / Dead code suppression

```java
@SuppressWarnings("unused")
public int userKey = WebData.instance().getUserId();
```

The field `userKey` is never accessed from within `LocationDb.java` or referenced by any other class confirmed through codebase-wide grep. The annotation silences the IDE/lint warning rather than resolving it. Furthermore the field is initialized via a side-effecting singleton call (`WebData.instance().getUserId()`) at object construction time, meaning every `LocationDb` Realm object carries a stale snapshot of the user ID at the moment of construction — this is the same initialization-time capture anti-pattern found in sibling Db classes (`SessionDb`, `PreStartQuestionDb`, `PreStartHistoryDb`). The `@SuppressWarnings` makes this invisible. The field should be removed if truly unused, or actually used in queries rather than suppressed.

---

### A46-5 — MEDIUM — `LocationDb.java`: Deprecated `android.support.annotation.NonNull` (legacy support library)

**File:** `LocationDb.java`, line 3
**Category:** Build warnings / deprecated API

```java
import android.support.annotation.NonNull;
```

This is the old Android Support Library annotation package. All 57 occurrences of this import across the codebase use the legacy `android.support.*` path rather than the AndroidX equivalent `androidx.annotation.NonNull`. While not a compile error, the Support Library reached end-of-life in 2020. This is a systemic issue visible in this file.

---

### A46-6 — MEDIUM — `LocationDb.java`: Mixed access modifiers on overloaded `removeData` / `readData` methods — inconsistent visibility design

**File:** `LocationDb.java`, lines 43–74
**Category:** Style inconsistency / leaky abstraction

The two `removeData` overloads have mismatched access:
- `public static void removeData(SaveSingleGPSParameter ...)` — line 47 (public)
- `static void removeData(Realm, SaveMultipleGPSParameter)` — line 64 (package-private)

Similarly, `readData(Realm)` at line 43 is package-private but `readAllLocationToSync()` at line 33 is public and wraps it. There is no documented rationale for the asymmetry. The package-private `removeData(Realm, ...)` is called exclusively from within `uploadLocation()` which is `public static`, meaning the data-deletion path for multi-GPS sync is fully hidden behind an internal implementation detail. This makes it impossible to call from outside the package without going through `uploadLocation`, which introduces tight coupling and makes unit-testing the deletion path impossible without executing a full upload flow.

---

### A46-7 — MEDIUM — `ModelPrefs.java`: All write operations use `commit()` instead of `apply()`

**File:** `ModelPrefs.java`, lines 23, 33, 37, 46, 58
**Category:** Build warnings / style inconsistency / performance

```java
getPref().edit().putInt(key,d).commit();       // line 23
getPref().edit().remove(key).commit();         // line 33
getPref().edit().putString(key,s).commit();    // line 37
getPref().edit().putBoolean(key,s).commit();   // line 46
getPref().edit().putString(key,s).commit();    // line 58
```

`SharedPreferences.Editor.commit()` performs a synchronous disk write and returns a boolean indicating success. That boolean is discarded in every call. Android documentation recommends `apply()` for asynchronous writes when the caller does not need to check the result. Five calls that block the calling thread (which may be the main/UI thread for some callers) and discard the return value indicate both a style inconsistency (returning but ignoring a meaningful result) and a latent performance risk.

---

### A46-8 — MEDIUM — `ModelPrefs.java`: `readString` assigns to an intermediate variable unnecessarily

**File:** `ModelPrefs.java`, lines 40–43
**Category:** Style inconsistency

```java
public static String readString(String key) {
    String s = getPref().getString(key, "");
    return s;
}
```

Every other read method returns the result directly (e.g., `readInt` at line 27, `readBoolean` at line 50). `readString` introduces a needless intermediate variable `s`, creating a style inconsistency across the class. Minor but symptomatic of inconsistent authorship.

---

### A46-9 — MEDIUM — `ModelPrefs.java`: `saveBoolean` parameter named `s` — misleading name for a `boolean`

**File:** `ModelPrefs.java`, line 45
**Category:** Style inconsistency

```java
public static void saveBoolean(String key, boolean s) {
```

The parameter `s` (which conventionally denotes a `String`) is used for a `boolean` argument. All other write methods use descriptive names (`d` for `int`, `s` for `String`, `object` for `Object`). Using `s` for a boolean parameter is confusing and inconsistent with normal conventions; it was likely copied from `saveString` without renaming.

---

### A46-10 — MEDIUM — `ModelPrefs.java`: `readObject` returns raw `Object` instead of a typed result

**File:** `ModelPrefs.java`, lines 61–64
**Category:** Leaky abstraction / style inconsistency

```java
public static Object readObject(String key, Class<?> classType) {
    String s = getPref().getString(key, "");
    return GsonHelper.objectFromString(s, classType);
}
```

The caller passes a `Class<?>` type token, and `GsonHelper.objectFromString` presumably deserializes to that type internally, yet the return type is raw `Object`. The caller must cast the result unsafely at the call site. The method signature should use a generic return type `<T> T readObject(String key, Class<T> classType)` to let the compiler enforce type safety. As written, this is an untyped leaky abstraction. Additionally, this method — like `readString` — needlessly assigns to an intermediate variable `s`.

---

### A46-11 — HIGH — `MyCommonValue.java`: Mutable public static fields used as global application state (global variable anti-pattern)

**File:** `MyCommonValue.java`, lines 10–16
**Category:** Leaky abstraction / architecture

```java
public static EquipmentItem currentEquipmentItem = null;
public static Boolean isCheckLocationPermissionDone = false;
public static  String  companyName="";
public static  String  companyContract="";
public static  String  companyRole="";
public static  String  companyenabled="";
```

All six fields are mutable public static state with no synchronization, no accessor methods, and no lifecycle management. This class is used as a global state bag shared across 13 source files. There is no mechanism to reset this state (e.g., on logout or session change), making it a source of stale-state bugs between sessions. `currentEquipmentItem` is reference-typed and nullable, and direct writes from multiple fragments/activities create data races on Android's multi-threaded environment. The class has no constructor, no methods, and no encapsulation — it is effectively a struct of global variables.

---

### A46-12 — LOW — `MyCommonValue.java`: `companyenabled` violates naming convention (camel case)

**File:** `MyCommonValue.java`, line 16
**Category:** Style inconsistency

```java
public static  String  companyenabled="";
```

All other fields in this class follow camelCase naming: `currentEquipmentItem`, `isCheckLocationPermissionDone`, `companyName`, `companyContract`, `companyRole`. The field `companyenabled` is fully lowercase, deviating from Java camelCase conventions and from the pattern of every sibling field. The correct name would be `companyEnabled`. Confirmed by codebase-wide grep: this field is not referenced anywhere outside its own declaration, making it effectively dead — no code reads or writes `companyenabled` except its declaration.

---

### A46-13 — LOW — `MyCommonValue.java`: `companyenabled` is a dead field (unreferenced)

**File:** `MyCommonValue.java`, line 16
**Category:** Dead code

```java
public static  String  companyenabled="";
```

A codebase-wide search for `companyenabled` finds zero references outside the declaration. The field is declared and initialized but never read or written by any other class. It is dead code and should be removed.

---

### A46-14 — LOW — `MyCommonValue.java`: Irregular whitespace in field declarations

**File:** `MyCommonValue.java`, lines 13–16
**Category:** Style inconsistency

```java
public static  String  companyName="";
public static  String  companyContract="";
public static  String  companyRole="";
public static  String  companyenabled="";
```

All four `String` field declarations use double-space between `static` and `String`, and between `String` and the field name. Lines 10 and 11 use standard single-space separators. This is inconsistent formatting that suggests the four String fields were authored separately or copy-pasted without normalization.

---

### A46-15 — LOW — `ModelPrefs.java`: `getPref` creates a new `SharedPreferences` instance on every call

**File:** `ModelPrefs.java`, lines 16–19
**Category:** Style inconsistency / performance

```java
static SharedPreferences getPref() {
    SharedPreferences prefs = MyApplication.getContext().getSharedPreferences("prefs", Context.MODE_PRIVATE);
    return prefs;
}
```

`getPref()` is called once per read or write operation, obtaining a fresh `SharedPreferences` handle each time. While the Android framework returns the same cached instance for the same file name, the pattern discards the local variable `prefs` immediately after assignment and could be simplified to a single-line return. More significantly, `getPref` calls `MyApplication.getContext()` on every invocation, making all `ModelPrefs` methods implicitly dependent on a globally initialized application context singleton with no null-safety guard — if called before `MyApplication` is initialized (e.g., in tests or early process startup), it will throw a `NullPointerException` silently.

---

### A46-16 — LOW — `LocationDb.java`: `TAG` field is not `private` or `final`

**File:** `LocationDb.java`, line 24
**Category:** Style inconsistency

```java
public static String TAG = LocationDb.class.getSimpleName();
```

Convention for Android logging tags is `private static final String TAG`. This field is `public` (allowing external modification) and not `final` (allowing reassignment). Cross-referencing sibling classes confirms this pattern is inconsistent: some Db classes declare `TAG` as `private static String`, others as `public static String`. The field should be `private static final`.

---

## Summary Table

| ID | Severity | File | Category | Description |
|----|----------|------|----------|-------------|
| A46-1 | HIGH | LocationDb.java | Dead code | Unused import `ShockEventService` (BLE cross-module coupling) |
| A46-2 | HIGH | LocationDb.java | Dead code | Unused import `SaveSingleGPSResult` |
| A46-3 | HIGH | LocationDb.java | Dead code | Unused import `RealmQuery` |
| A46-4 | HIGH | LocationDb.java | Dead code / build warning | `@SuppressWarnings("unused")` masking dead `userKey` field with stale initialization |
| A46-5 | MEDIUM | LocationDb.java | Build warning | `android.support.annotation.NonNull` — legacy support library, not AndroidX |
| A46-6 | MEDIUM | LocationDb.java | Style / leaky abstraction | Mixed visibility on overloaded `removeData`/`readData` methods |
| A46-7 | MEDIUM | ModelPrefs.java | Performance / style | `commit()` used everywhere; return value discarded; should use `apply()` |
| A46-8 | MEDIUM | ModelPrefs.java | Style inconsistency | `readString` uses unnecessary intermediate variable unlike all other read methods |
| A46-9 | MEDIUM | ModelPrefs.java | Style inconsistency | `saveBoolean` parameter named `s` — misleading, copied from `saveString` |
| A46-10 | MEDIUM | ModelPrefs.java | Leaky abstraction | `readObject` returns raw `Object` despite having a type token parameter |
| A46-11 | HIGH | MyCommonValue.java | Leaky abstraction / architecture | Six mutable public static fields used as unsynchronized global state across 13 files |
| A46-12 | LOW | MyCommonValue.java | Style inconsistency | `companyenabled` violates camelCase convention |
| A46-13 | LOW | MyCommonValue.java | Dead code | `companyenabled` is never referenced outside its declaration |
| A46-14 | LOW | MyCommonValue.java | Style inconsistency | Irregular double-space in four `String` field declarations |
| A46-15 | LOW | ModelPrefs.java | Style / robustness | `getPref()` has no null-safety guard on `MyApplication.getContext()` |
| A46-16 | LOW | LocationDb.java | Style inconsistency | `TAG` is `public static` rather than `private static final` |
