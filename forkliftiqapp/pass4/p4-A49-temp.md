# Pass 4 — Code Quality
**Audit run:** 2026-02-26-01
**Agent:** A49
**Date reviewed:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/SyncService.java`

**Class:** `SyncService` — extends `android.app.IntentService`

**Fields:**
- `private static String TAG` — line 23
- `private WebApi webApi` — line 25

**Methods (exhaustive):**
| Method | Visibility | Line |
|---|---|---|
| `SyncService()` (constructor) | public | 27 |
| `onHandleIntent(Intent intent)` | protected, @Override | 32 |
| `syncSession()` | private | 49 |
| `syncOfflineLocation()` | private | 82 |
| `deleteAbortedSession()` | private | 98 |
| `syncSessionItems()` | private | 118 |
| `startService()` | public static | 157 |

**Types/constants defined:** none beyond the class itself.

**Imports in file:**
- `android.app.IntentService` (line 3)
- `android.content.Intent` (line 4)
- `android.util.Log` (line 5)
- `au.com.collectiveintelligence.fleetiq360.WebService.*` (line 6, wildcard)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveSessionItem` (line 7)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServiceResultPacket` (line 8)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveMultipleGPSParameter` (line 9)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveSessionsParameter` (line 10)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveSingleGPSParameter` (line 11)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveSingleGPSResult` (line 12)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SessionResult` (line 13)
- `au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication` (line 14)
- `au.com.collectiveintelligence.fleetiq360.util.ServerDateFormatter` (line 15)
- `com.yy.libcommon.CommonLib.NetworkDetect` (line 17)
- `java.util.ArrayList` (line 19)
- `java.util.Calendar` (line 20)

---

### File 2: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/TakePhotoPathPrefs.java`

**Class:** `TakePhotoPathPrefs` — no superclass (implicit `Object`)

**Fields:**
- `private static String KEY_0 = "image0"` — line 14
- `private static String KEY_1 = "image1"` — line 15
- `private static String KEY_2 = "image2"` — line 16
- `private static String KEY_3 = "image3"` — line 17
- `private static String[] keyArray = {KEY_0, KEY_1, KEY_2, KEY_3}` — line 18

**Methods (exhaustive):**
| Method | Visibility | Line |
|---|---|---|
| `getPref()` | static (package-private) | 21 |
| `saveObjectFromPosition(int position, String path)` | public static | 26 |
| `hasInvalidPhoto()` | public static | 38 |
| `getImagePathFromPosition(int position)` | public static | 46 |
| `clearImages()` | public static | 53 |

**Types/constants defined:** none beyond the class itself.

---

### File 3: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/UserInfoPrefs.java`

**Class:** `UserInfoPrefs` — extends `ModelPrefs`

**Fields:**
- `private static String TAG = UserInfoPrefs.class.getSimpleName()` — line 14
- `private static String USER_INFO_PREFS_KEY = "usr_info_key"` — line 15

**Methods (exhaustive):**
| Method | Visibility | Line |
|---|---|---|
| `getUserInfoPrefs()` | static (package-private) | 16 |

**Types/constants defined:** none beyond the class itself.

---

## Section 2 & 3: Findings

---

### A49-1 — HIGH — Deprecated API: `IntentService` used in `SyncService`

**File:** `SyncService.java`, line 3, 22, 28

`android.app.IntentService` was deprecated in Android API level 30 (Android 11). The recommended replacement is `androidx.work.WorkManager` or a `JobIntentService`. The class also passes `IntentService.class.getSimpleName()` (the string `"IntentService"`) as the worker thread name in the constructor (line 28) rather than its own class name — a secondary naming error that makes thread identification in logs incorrect.

```java
// Line 27-29
public SyncService() {
    super(IntentService.class.getSimpleName()); // should be SyncService.class.getSimpleName()
}
```

The same pattern is repeated in `CacheService.java` (confirmed by cross-file search), indicating a copy-paste propagation of both the deprecated API and the wrong name argument.

---

### A49-2 — HIGH — Logic bug: network-not-connected branch falls through to `syncSession()`

**File:** `SyncService.java`, lines 37–47

The `onHandleIntent` method checks whether the network is connected. If it is **not** connected, it schedules a retry via `MyApplication.runLater(...)` but then **falls through** and calls `syncSession()` anyway on the next line (line 46). The `return` statement is missing. As a result, every sync attempt proceeds unconditionally regardless of network state, and the delayed re-start simply causes a duplicate execution later.

```java
if (!NetworkDetect.isNetworkConnected(this)) {
    MyApplication.runLater(new Runnable() { ... }, 10 * 1000);
    // MISSING: return;
}
syncSession(); // always executed, even when offline
```

---

### A49-3 — HIGH — Unused imports (`SaveMultipleGPSParameter`, `SaveSingleGPSParameter`, `SaveSingleGPSResult`, `ServerDateFormatter`, `Calendar`)

**File:** `SyncService.java`, lines 9, 11, 12, 15, 20

Five imported symbols are never referenced anywhere in the file body:
- `SaveMultipleGPSParameter` (line 9)
- `SaveSingleGPSParameter` (line 11)
- `SaveSingleGPSResult` (line 12)
- `au.com.collectiveintelligence.fleetiq360.util.ServerDateFormatter` (line 15)
- `java.util.Calendar` (line 20)

These are stale imports, most likely left over from an earlier implementation of GPS sync logic that was moved or deleted. They produce build warnings and indicate dead code paths that were not cleaned up.

---

### A49-4 — MEDIUM — Wildcard import in production service

**File:** `SyncService.java`, line 6

```java
import au.com.collectiveintelligence.fleetiq360.WebService.*;
```

Wildcard imports obscure which types are actually used, make it harder to detect naming collisions, and can cause IDE warnings. Given that specific imports for sub-packages of `WebService` appear on lines 7–13, the wildcard on line 6 is redundant and should be replaced with explicit imports.

---

### A49-5 — MEDIUM — `Thread.sleep()` used for inter-step pacing in `syncSession()` and `syncOfflineLocation()`

**File:** `SyncService.java`, lines 52–76, 90–94

Fixed-duration `Thread.sleep()` calls are scattered across `syncSession()` and `syncOfflineLocation()` as ad-hoc delays between async operations (2000 ms, 2000 ms, 1000 ms, 1000 ms, 100 ms). These sleeps do not synchronise on actual operation completion — the underlying web API calls (`webApi.deleteSession`, `webApi.syncSaveSession`) are asynchronous (callback-based). The sleeps are an unreliable heuristic; they will over-wait on a fast connection and under-wait on a slow one, potentially producing data races. Interrupt handling swallows the `InterruptedException` by only calling `e.printStackTrace()`, which loses the interrupted status and prevents clean service shutdown.

```java
try {
    Thread.sleep(2000);
} catch (InterruptedException e) {
    e.printStackTrace(); // interrupted status not restored
}
```

---

### A49-6 — MEDIUM — Dead unused field and method in `UserInfoPrefs`

**File:** `UserInfoPrefs.java`, lines 14–19

`UserInfoPrefs` contains:
- `private static String TAG` — never used within the file (no log calls exist).
- `private static String USER_INFO_PREFS_KEY` — never used within the file.
- `static SharedPreferences getUserInfoPrefs()` — package-private method, confirmed unreferenced anywhere in the codebase (search returned no call sites outside the file itself).

The class is effectively a stub that extends `ModelPrefs` but provides no functional additions. It exists in the codebase without any call site. Either the implementation was never completed or it was abandoned.

---

### A49-7 — MEDIUM — Dead/unreachable public method: `saveObjectFromPosition` never called

**File:** `TakePhotoPathPrefs.java`, line 26

`public static void saveObjectFromPosition(int position, String path)` is the only write path for individual photo slots. A codebase-wide search found zero call sites for this method outside of `TakePhotoPathPrefs.java` itself. Photos can never be saved via the class's intended API, making the `hasInvalidPhoto()` and `getImagePathFromPosition()` read paths return `null` for every slot regardless of application state.

---

### A49-8 — MEDIUM — `clearImages()` performs four separate `SharedPreferences` edit/commit cycles instead of one

**File:** `TakePhotoPathPrefs.java`, lines 53–58

```java
getPref().edit().remove(KEY_0).commit();
getPref().edit().remove(KEY_1).commit();
getPref().edit().remove(KEY_2).commit();
getPref().edit().remove(KEY_3).commit();
```

Each `.edit()...commit()` opens and synchronously writes the entire preferences file to disk. Four sequential commits are four disk writes where one batched transaction would suffice. The correct approach is a single editor chaining all four removals before one `commit()` or `apply()`. The same inefficiency applies to `saveObjectFromPosition()` (lines 29–35), which always commits a single key but could be consolidated. This pattern is also inconsistent with `ModelPrefs`, which chains operations but still uses `commit()` synchronously throughout.

---

### A49-9 — LOW — `SharedPreferences.commit()` used throughout instead of `apply()`

**File:** `TakePhotoPathPrefs.java`, lines 29, 31, 33, 35, 54, 55, 56, 57; `ModelPrefs.java` throughout

`SharedPreferences.Editor.commit()` is a synchronous blocking disk write that Android documentation explicitly recommends avoiding on the main thread. `apply()` performs an asynchronous write and is the preferred replacement for all cases where the return value (success/failure boolean) is not checked. Since no call site checks the boolean return of `commit()`, the synchronous behaviour provides no benefit and risks ANR events if called on the UI thread.

---

### A49-10 — LOW — Style inconsistency: `KEY_0`–`KEY_3` implemented as separate fields instead of using the `keyArray` already present

**File:** `TakePhotoPathPrefs.java`, lines 14–18

The four individual constants `KEY_0` through `KEY_3` are declared as separate `private static String` fields and then also aggregated into `keyArray`. The `saveObjectFromPosition()` method (lines 28–35) re-implements positional dispatch via a chain of `if/else if` branches using the individual constants, while `hasInvalidPhoto()` and `getImagePathFromPosition()` use `keyArray`. This internal inconsistency means `saveObjectFromPosition` ignores `keyArray` entirely and must be updated in two places if a new key is ever added.

---

### A49-11 — LOW — Dead local variable `String s` in `saveObjectFromPosition`

**File:** `TakePhotoPathPrefs.java`, line 27

```java
public static void saveObjectFromPosition(int position, String path) {
    String s = "";   // declared but never read or written to again
    if (0 == position)
        ...
```

`String s = ""` is declared and assigned but never used. This is dead code and will produce a compiler/IDE warning.

---

### A49-12 — LOW — `TAG` field is not `final` in `SyncService`

**File:** `SyncService.java`, line 23

```java
private static String TAG = SyncService.class.getSimpleName();
```

The `TAG` field is declared `private static String` but is never reassigned. It should be `private static final String` to reflect its constant semantics, prevent accidental mutation, and enable compiler optimisation. This pattern is idiomatic and enforced by Android lint rule `LogTagMismatch`/`FieldCanBeLocal`.

---

### A49-13 — INFO — `SyncService` misplaced in `model` package

**File:** `SyncService.java`, package declaration line 1

`SyncService` is a background Android `Service` component, not a data model. Its package `au.com.collectiveintelligence.fleetiq360.model` is inconsistent with the rest of the project structure (services are typically in a `service` or `background` package). This is a structural/organisational issue with no runtime impact.

---

## Summary Table

| ID | Severity | File | Issue |
|---|---|---|---|
| A49-1 | HIGH | SyncService.java | Deprecated `IntentService` API; wrong thread name passed to `super()` |
| A49-2 | HIGH | SyncService.java | Missing `return` after scheduling retry — sync always runs even when offline |
| A49-3 | HIGH | SyncService.java | Five unused imports (dead code / stale GPS implementation remnants) |
| A49-4 | MEDIUM | SyncService.java | Wildcard import `WebService.*` in production service |
| A49-5 | MEDIUM | SyncService.java | `Thread.sleep()` used as async-completion heuristic; `InterruptedException` swallowed |
| A49-6 | MEDIUM | UserInfoPrefs.java | Stub class — all fields and the only method are dead/unused |
| A49-7 | MEDIUM | TakePhotoPathPrefs.java | `saveObjectFromPosition()` has zero call sites — photo save path is dead |
| A49-8 | MEDIUM | TakePhotoPathPrefs.java | Four separate `commit()` disk writes in `clearImages()` instead of one batch |
| A49-9 | LOW | TakePhotoPathPrefs.java, ModelPrefs.java | `commit()` used instead of `apply()` throughout, unchecked return value |
| A49-10 | LOW | TakePhotoPathPrefs.java | Inconsistent positional dispatch: `if/else if` vs `keyArray` for same key set |
| A49-11 | LOW | TakePhotoPathPrefs.java | Dead local variable `String s` in `saveObjectFromPosition` |
| A49-12 | LOW | SyncService.java | `TAG` field not declared `final` |
| A49-13 | INFO | SyncService.java | Service class placed in `model` package |
