# Pass 4 — Code Quality Audit
**Agent:** A14
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleUtil.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/ShockEventService.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/ShockEventsDb.java`

---

## Step 1: Reading Evidence

### File 1: BleUtil.java

**Class:** `BleUtil` (public)

**Inner Class:** `BleUtil.BleTimeItem` (public static)
- Fields (all package-private): `int year`, `int month`, `int day`, `int hour`, `int minute`, `int second`, `int dayOfWeek`
- Lines 33–42

**Constants defined in `BleUtil` (all package-private `static`):**
| Name | Value | Line |
|---|---|---|
| `UPDATE_REASON_UNKNOWN` | `(byte) 0` | 26 |
| `UPDATE_REASON_MANUAL` | `(byte) 1` | 27 |
| `UPDATE_REASON_EXTERNAL_REF` | `(byte)(1 << 1)` | 28 |
| `UPDATE_REASON_TIME_ZONE_CHANGE` | `(byte)(1 << 2)` | 29 |
| `UPDATE_REASON_DAYLIGHT_SAVING` | `(byte)(1 << 3)` | 30 |
| `hexArray` | `"0123456789ABCDEF".toCharArray()` (private final static) | 150 |

**Methods in `BleUtil`:**
| Method | Access | Line |
|---|---|---|
| `BleUtil()` | public (constructor) | 24 |
| `parseBleTime(byte[])` | public static | 43 |
| `isTimeSetSucceed(BleTimeItem, BleTimeItem)` | public static | 63 |
| `getTimeData()` | public static | 91 |
| `isTheSameByteArray(byte[], byte[])` | public static | 127 |
| `timezoneWithDstOffset(Calendar)` | static (package-private) | 134 |
| `bytesToHexStr(byte[])` | public static | 151 |
| `unsignedByteToInt(byte)` | static public | 164 |
| `unsignedBytesToInt(byte, byte)` | static public | 171 |
| `unsignedBytesToInt(byte, byte, byte, byte)` | static public | 178 |
| `bytesToFloat(byte, byte)` | static public | 186 |
| `bytesToFloat(byte, byte, byte, byte)` | static public | 196 |
| `unsignedToSigned(int, int)` | static public | 207 |
| `intToSignedBits(int, int)` | static public | 217 |
| `getTypeLen(int)` | static private | 227 |
| `getIntValue(byte[], int)` | static public | 231 |
| `getIntValue(byte[], int, int)` | static public | 234 |

---

### File 2: ShockEventService.java

**Class:** `ShockEventService` extends `android.app.IntentService` (public)

**Constants / public fields:**
| Name | Type | Access | Line |
|---|---|---|---|
| `TAG` | `String` | public static | 26 |
| `IMPACT` | `String` | public static final | 144 |
| `lastImpactEvent` | `ShockEventsItem` | public static | 145 |
| `lastShockEventsItem` | `ShockEventsItem` | private static | 115 |

**Methods:**
| Method | Access | Line |
|---|---|---|
| `ShockEventService()` | public (constructor) | 28 |
| `onHandleIntent(Intent)` | protected (override) | 33 |
| `onShockDataRead(String, Intent)` | private | 55 |
| `uploadEvent()` | private | 71 |
| `startService()` | public static | 102 |
| `sendData(Intent)` | static (package-private) | 109 |
| `saveShockEvent(String, byte[])` | private static | 117 |
| `showShockAlertIfNeeded(ShockEventsItem)` | private static | 147 |

---

### File 3: ShockEventsDb.java

**Class:** `ShockEventsDb` extends `io.realm.RealmObject` (public)

**Fields (all public):**
| Name | Type | Line |
|---|---|---|
| `mac_address` | `String` | 15 |
| `time` | `Date` | 16 |
| `magnitude` | `long` | 17 |

**Methods:**
| Method | Access | Line |
|---|---|---|
| `readData(Realm)` | static (package-private) | 19 |
| `removeData(Realm, SaveShockEventParameter)` | static (package-private) | 23 |
| `alreadySaved(ShockEventsItem)` | static (package-private) | 36 |
| `saveData(ShockEventsItem)` | static (package-private) | 46 |
| `getMatchingEvents(Realm, Date, String)` | private static | 68 |

---

## Step 2 & 3: Findings

---

### A14-1 — HIGH: `IntentService` is deprecated (API 30+)

**File:** `ShockEventService.java`, line 25
**Severity:** HIGH

`ShockEventService` extends `android.app.IntentService`, which was deprecated in API level 30 (Android 11). The deprecation notice in Android docs directs developers to use `WorkManager` or `JobIntentService` instead. The `build.gradle` targets `targetSdkVersion` via `project.ext.myTargetSdkVersion`; even at lower target SDK levels, this is a build warning and a technical debt item that will block future API upgrades.

```java
// ShockEventService.java line 25
public class ShockEventService extends IntentService {
```

---

### A14-2 — HIGH: Legacy Android support library used instead of AndroidX

**File:** `ShockEventService.java`, line 6; `ShockEventsDb.java`, line 3
**Severity:** HIGH

Both files import from `android.support.*` rather than the AndroidX equivalents (`androidx.*`). AndroidX superseded the support library in 2018 (library version 28.0.0 was the last support-lib release). The `build.gradle` pins `com.android.support:appcompat-v7:26.0.2`, `com.android.support:support-v4:26.0.2`, and `com.android.support:recyclerview-v7:26.0.2` — all unmaintained.

```java
// ShockEventService.java line 6
import android.support.v4.content.LocalBroadcastManager;

// ShockEventsDb.java line 3
import android.support.annotation.NonNull;
```

This affects the entire project and will produce build warnings. The support library is incompatible with the latest Gradle Android Plugin and AAPT2 versions.

---

### A14-3 — HIGH: Silent exception swallowing in `startService()`

**File:** `ShockEventService.java`, lines 103–107
**Severity:** HIGH

The `catch (Exception ignored)` block discards all exceptions from `startService()`. This means any `IllegalStateException` thrown when starting the service from the background (a firm Android 8+ restriction) is silently lost, making the shock event upload pipeline fail invisibly with no log entry whatsoever.

```java
public static void startService() {
    try {
        MyApplication.getContext().startService(new Intent(MyApplication.getContext(), ShockEventService.class));
    } catch (Exception ignored) {
    }
}
```

At minimum the exception should be logged; in practice the caller should handle background execution restrictions explicitly.

---

### A14-4 — HIGH: `saveShockEvent` is `private static` but accesses instance-contextual state (`lastShockEventsItem`)

**File:** `ShockEventService.java`, lines 115–142
**Severity:** HIGH

`lastShockEventsItem` is a `private static` field used to de-duplicate consecutive identical shock events. Because `ShockEventService` is an `IntentService` (and each `onHandleIntent` call runs sequentially), this is not directly a race condition — but the state is shared across all future instances of the service. More critically, the duplicate-suppression logic at lines 133–138 is inconsistent:

- It calls `ShockEventsDb.alreadySaved()` to check persistence but then unconditionally calls `ShockEventsDb.saveData()` two lines later (line 140) **regardless of whether the event was already present**. The `saveData` implementation internally deletes then re-creates matching records, so duplicate data is overwritten rather than skipped, but the showAlertIfNeeded path is blocked by this condition while the save is not — the two branches apply different de-duplication rules, making the logic fragile and hard to reason about.

```java
if ((lastShockEventsItem == null ||
        !lastShockEventsItem.time.equals(shockEventsItem.time) ||
        !lastShockEventsItem.mac_address.equals(shockEventsItem.mac_address)) &&
        !ShockEventsDb.alreadySaved(shockEventsItem)) {
    showShockAlertIfNeeded(shockEventsItem);
}
lastShockEventsItem = shockEventsItem;
ShockEventsDb.saveData(shockEventsItem);  // always called
```

---

### A14-5 — MEDIUM: Commented-out code left in production files

**File:** `BleUtil.java`, lines 45–46, 93–94, 123
**Severity:** MEDIUM

Three blocks of commented-out code remain in the production file:

**Lines 45–46 (inside `parseBleTime`):**
```java
//        bleTimeRaw = struct.pack('<HBBBBBBBB', nowTime.tm_year, nowTime.tm_mon, nowTime.tm_mday,
//                nowTime.tm_hour, nowTime.tm_min, nowTime.tm_sec, nowTime.tm_wday, 0, 0)
```
This is a Python `struct.pack` snippet — a development reference comment from the original protocol author. It serves no Java purpose and should be removed.

**Lines 93–94 (inside `getTimeData`):**
```java
//        bleTimeRaw = struct.pack('<HBBBBBBBB', nowTime.tm_year, nowTime.tm_mon, nowTime.tm_mday,
//                nowTime.tm_hour, nowTime.tm_min, nowTime.tm_sec, nowTime.tm_wday, 0, 0)
```
Duplicate of the Python snippet above.

**Line 123 (inside `getTimeData`):**
```java
//BleTimeItem bleTimeItem = parseBleTime(da);
```
Disabled debug call. Should be deleted.

---

### A14-6 — MEDIUM: Inconsistent access-modifier ordering on `static` methods

**File:** `BleUtil.java`, multiple lines
**Severity:** MEDIUM

The file mixes two orderings of `static` and the access modifier throughout the class:

- `public static` (e.g., `parseBleTime` line 43, `isTimeSetSucceed` line 63, `isTheSameByteArray` line 127)
- `static public` (e.g., `unsignedByteToInt` line 164, `unsignedBytesToInt` line 171, `bytesToFloat` line 186, `unsignedToSigned` line 207)
- `static private` (e.g., `getTypeLen` line 227)

Java permits both orderings but style guides (Google Java Style, Oracle Code Conventions) mandate that the access modifier appear first (`public static`, not `static public`). The inconsistency indicates the file was assembled from two different codebases without normalisation.

---

### A14-7 — MEDIUM: `BleUtil` constants are package-private but the class is public utility

**File:** `BleUtil.java`, lines 26–30
**Severity:** MEDIUM

The five `UPDATE_REASON_*` constants have no explicit access modifier, making them package-private. The class is `public` and the constants follow a naming convention implying they are intended for use by callers (they encode BLE protocol values). Their package-private visibility means they cannot be used outside the `BLE` package, and if they are only used internally, they are dead constants (no references to them were found in the three audited files). Either they should be `public static final` if used externally, or they should be deleted if unused.

```java
static byte UPDATE_REASON_UNKNOWN = 0;
static byte UPDATE_REASON_MANUAL = 1;
static byte UPDATE_REASON_EXTERNAL_REF = (1 << 1);
static byte UPDATE_REASON_TIME_ZONE_CHANGE = (1 << 2);
static byte UPDATE_REASON_DAYLIGHT_SAVING = (1 << 3);
```

Additionally, none are declared `final`, so they are mutable class-level state, which is incorrect for symbolic constants.

---

### A14-8 — MEDIUM: `BleTimeItem` fields are all package-private (no encapsulation)

**File:** `BleUtil.java`, lines 34–41
**Severity:** MEDIUM

The inner class `BleTimeItem` exposes all seven fields with package-private visibility (no access modifier). The class is `public static`, meaning it is part of the public API surface, but its fields can only be read or set within the same package. This is a leaky abstraction: callers outside the `BLE` package receive a `BleTimeItem` from `parseBleTime()` but cannot access any of its data.

```java
public static class BleTimeItem {
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    int dayOfWeek;
}
```

---

### A14-9 — MEDIUM: `TAG` field is `public` (not `private static final`)

**File:** `ShockEventService.java`, line 26
**Severity:** MEDIUM

The log tag field `TAG` is declared `public static` (non-final, non-private). Log tag fields should be `private static final String`. The current declaration allows external code to mutate the tag, corrupting log output from the service. The value is also unnecessarily complex — prepending `"CI_BLE_SHOCK_EVENT"` to `getSimpleName()` produces `"CI_BLE_SHOCK_EVENTShockEventService"`, which is 34 characters — exceeding the 23-character limit that `Log` enforces on Android API < 26 (the tag is silently truncated on older devices).

```java
public static String TAG = "CI_BLE_SHOCK_EVENT" + ShockEventService.class.getSimpleName();
```

---

### A14-10 — MEDIUM: `lastImpactEvent` is a `public static` mutable field (shared global state)

**File:** `ShockEventService.java`, line 145
**Severity:** MEDIUM

`lastImpactEvent` is declared `public static ShockEventsItem lastImpactEvent = null`. This is a globally mutable reference accessible from any class in the application. The field is written in `showShockAlertIfNeeded` (line 160) and presumably read by UI components reacting to the `IMPACT` broadcast. This pattern creates invisible coupling between `ShockEventService` and any consumer, making it impossible to understand the contract without reading all callers. The field should be communicated through the `Intent` extras of the broadcast rather than via static state.

```java
public static ShockEventsItem lastImpactEvent = null;
```

---

### A14-11 — MEDIUM: `isTimeSetSucceed` uses sequential field comparisons instead of a compound date comparison

**File:** `BleUtil.java`, lines 63–89
**Severity:** MEDIUM

`isTimeSetSucceed` performs six sequential `<` comparisons (year, month, day, hour, minute, second), each independently returning `false`. This logic is incorrect for cross-boundary cases: a time of month=3, day=1 will return `false` if `expectItem.month=2, expectItem.day=15` because `day (1) < expectItem.day (15)` — even though the date is actually later. The method name implies it checks whether the device time was set successfully (i.e., the received time is at least as late as the expected time), but the field-by-field comparison does not implement that correctly for dates that cross month or year boundaries.

```java
if(bleTimeItem.month < expectItem.month){ return false; }
if(bleTimeItem.day < expectItem.day){ return false; }
// ... (day comparison ignores month context)
```

---

### A14-12 — MEDIUM: `removeData` opens nested Realm transactions inside a loop

**File:** `ShockEventsDb.java`, lines 23–34
**Severity:** MEDIUM

`removeData` calls `realm.executeTransaction(...)` inside a `for` loop over `parameter.impactList`. Each iteration opens and commits a separate Realm transaction. For a list of N events this creates N transactions where a single batched transaction would suffice. On a low-power device this causes unnecessary I/O overhead and risks partial deletion if any transaction in the sequence throws (earlier deletions are committed but later ones are not, leaving an inconsistent state between what was uploaded and what remains in the local cache).

```java
for (SaveShockEventItem item : parameter.impactList) {
    final RealmResults<ShockEventsDb> events = getMatchingEvents(...);
    realm.executeTransaction(new Realm.Transaction() {
        @Override
        public void execute(@NonNull Realm realm) {
            if (events != null) events.deleteAllFromRealm();
        }
    });
}
```

---

### A14-13 — LOW: `BleUtil` has a public no-argument constructor on an all-static utility class

**File:** `BleUtil.java`, line 24
**Severity:** LOW

`BleUtil` contains only static methods and static fields. The explicit public constructor `public BleUtil() {}` allows instantiation of an object that carries no state and provides no instance behaviour. Utility classes should declare a private constructor to prevent instantiation and signal intent clearly.

```java
public BleUtil() {}
```

---

### A14-14 — LOW: `timezoneWithDstOffset` is package-private but unused in audited files

**File:** `BleUtil.java`, line 134
**Severity:** LOW

`timezoneWithDstOffset(Calendar)` has package-private visibility and is not referenced in any of the three audited files. If it is also not referenced elsewhere in the `BLE` package it is dead code. Even if it is referenced elsewhere in the package, the absence of `public` or any documentation makes its intended callers unclear.

---

### A14-15 — LOW: `sendData` is package-private with no documentation or apparent callers in audited scope

**File:** `ShockEventService.java`, line 109
**Severity:** LOW

`static void sendData(Intent intent)` wraps `startService` with an action-specific intent construction. It has package-private access. None of the three audited files call it, and its role relative to the public `startService()` is undocumented. If it is dead code it should be removed; if it is a legitimate entry point its accessibility should be clarified.

```java
static void sendData(Intent intent) {
    Intent dataIntent = new Intent(intent.getAction(), null, MyApplication.getContext(), ShockEventService.class);
    dataIntent.putExtras(intent);
    MyApplication.getContext().startService(dataIntent);
}
```

---

### A14-16 — LOW: Operator-precedence ambiguity in `unsignedToSigned` and `intToSignedBits`

**File:** `BleUtil.java`, lines 208–209, 219
**Severity:** LOW

The expressions `(1 << size-1)` rely on the fact that `-` has higher precedence than `<<` in Java, making this equivalent to `(1 << (size - 1))`. While technically correct, the missing parentheses around `size-1` reduce readability and are a common source of bugs when the expression is refactored. This pattern appears three times.

```java
if ((unsigned & (1 << size-1)) != 0) {
    unsigned = -1 * ((1 << size-1) - (unsigned & ((1 << size-1) - 1)));
}
```

---

### A14-17 — INFO: Copyright header references a third-party origin (Relish Technologies Ltd.)

**File:** `BleUtil.java`, lines 3–9
**Severity:** INFO

The file carries a copyright notice attributing the code to "Relish Technologies Ltd." under the MIT license. This appears to be third-party utility code incorporated into the project. The audit notes this for IP compliance review; it is not a code-quality defect per se, but the provenance should be confirmed and the license file should be present in the repository.

---

## Summary Table

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| A14-1 | HIGH | ShockEventService.java | 25 | `IntentService` deprecated (API 30+) |
| A14-2 | HIGH | ShockEventService.java / ShockEventsDb.java | 6 / 3 | `android.support.*` instead of AndroidX |
| A14-3 | HIGH | ShockEventService.java | 103–107 | Silent `catch (Exception ignored)` in `startService()` |
| A14-4 | HIGH | ShockEventService.java | 115–142 | Inconsistent duplicate suppression: alert guarded, DB write is not |
| A14-5 | MEDIUM | BleUtil.java | 45–46, 93–94, 123 | Commented-out code (Python struct.pack snippets + debug call) |
| A14-6 | MEDIUM | BleUtil.java | 164, 171, 178, 186, 196, 207, 227 | Mixed `public static` / `static public` / `static private` ordering |
| A14-7 | MEDIUM | BleUtil.java | 26–30 | `UPDATE_REASON_*` constants are package-private and non-final |
| A14-8 | MEDIUM | BleUtil.java | 34–41 | `BleTimeItem` fields are package-private on a public class |
| A14-9 | MEDIUM | ShockEventService.java | 26 | `TAG` is `public` non-final; value exceeds 23-char log limit |
| A14-10 | MEDIUM | ShockEventService.java | 145 | `lastImpactEvent` is public static mutable global state |
| A14-11 | MEDIUM | BleUtil.java | 63–89 | `isTimeSetSucceed` sequential field comparison is logically incorrect for cross-boundary dates |
| A14-12 | MEDIUM | ShockEventsDb.java | 23–34 | Per-item Realm transactions in `removeData` loop; should be single batched transaction |
| A14-13 | LOW | BleUtil.java | 24 | Public constructor on all-static utility class |
| A14-14 | LOW | BleUtil.java | 134 | `timezoneWithDstOffset` is package-private; possibly dead code |
| A14-15 | LOW | ShockEventService.java | 109 | `sendData` is package-private with no callers in audited scope |
| A14-16 | LOW | BleUtil.java | 208–209, 219 | `(1 << size-1)` precedence ambiguity; missing parentheses |
| A14-17 | INFO | BleUtil.java | 3–9 | Third-party copyright (Relish Technologies Ltd.) — IP provenance check recommended |
