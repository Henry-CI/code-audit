# Audit Report — Pass 4 (Code Quality)
**Agent:** A45
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27
**Files Assigned:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/CacheService.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/DataBaseHelp.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/EquipmentDb.java`

---

## Step 1: Reading Evidence

### File 1: CacheService.java

**Class:** `CacheService` extends `android.app.IntentService`
**Package:** `au.com.collectiveintelligence.fleetiq360.model`
**Lines:** 1–84

**Fields:**
| Name | Type | Modifier | Line |
|------|------|----------|------|
| `TAG` | `String` | `private static` | 18 |
| `webApi` | `WebApi` | `private` | 19 |

**Methods:**
| Method | Modifier | Line |
|--------|----------|------|
| `CacheService()` (constructor) | `public` | 21 |
| `onHandleIntent(Intent intent)` | `protected @Override` | 26 |
| `startService()` | `public static` | 76 |

**Types/Constants defined:** None.

**Imports used:**
- `android.app.IntentService`
- `android.content.Intent`
- `android.util.Log`
- `WebApi`, `WebListener`, `WebResult`
- `EquipmentItem`, `GetEquipmentResultArray`, `PreStartQuestionResultArray`
- `CurrentUser`, `MyApplication`, `User`
- `com.yy.libcommon.CommonLib.NetworkDetect`

---

### File 2: DataBaseHelp.java

**Class:** `DataBaseHelp`
**Package:** `au.com.collectiveintelligence.fleetiq360.model`
**Access:** package-private
**Lines:** 1–22

**Fields:** None.

**Methods:**
| Method | Modifier | Line |
|--------|----------|------|
| `getRealmQuery(Realm realm, Class<E> clazz)` | `static` (package-private) | 9 |
| `isExpired(long updateTime)` | `static` (package-private) | 13 |

**Types/Constants defined:** None. No constructor defined (relies on implicit no-arg constructor).

**Hardcoded literals:**
- `"userKey"` — field name string literal, line 10
- `2 * 60 * 60 * 1000` — 2-hour expiry duration in milliseconds, line 19

---

### File 3: EquipmentDb.java

**Class:** `EquipmentDb` extends `io.realm.RealmObject`
**Package:** `au.com.collectiveintelligence.fleetiq360.model`
**Lines:** 1–58

**Fields:**
| Name | Type | Modifier | Line |
|------|------|----------|------|
| `userId` | `int` | `private` | 12 |
| `updateTime` | `long` | `private` | 13 |
| `equipmentListStr` | `String` | `private` | 14 |

**Methods:**
| Method | Modifier | Line |
|--------|----------|------|
| `isExpired()` | `private` | 16 |
| `needToCache(final int userId)` | `static` (package-private) | 20 |
| `getEquipmentResultArray(final int userId)` | `public static` | 30 |
| `saveEquipmentResultArray(final int userId, final GetEquipmentResultArray getEquipmentResultArray)` | `public static` | 45 |

**Types/Constants defined:** None.

---

## Step 2 & 3: Findings

---

### A45-1 — HIGH: `TAG` field not declared `final` — mutable static field

**File:** `CacheService.java`, line 18
**Severity:** HIGH
**Category:** Style inconsistency / Build warning

```java
private static String TAG = CacheService.class.getSimpleName();
```

`TAG` is a logging constant that should never change. It is declared as a mutable `static` field (`String`) rather than `static final String`. This means the field is technically writable by any code within the class at runtime. Android Lint raises a warning for non-`final` log tag fields. The same pattern appears in `SyncService.java` (line 23) but the correct pattern (`private static final String TAG`) is used in other files (e.g., `WebListener.java`). The inconsistency means the project has no single enforced style for this common idiom.

**Resolution:** Change to `private static final String TAG = CacheService.class.getSimpleName();`

---

### A45-2 — HIGH: `IntentService` constructor passes wrong name — uses `IntentService` class name instead of `CacheService`

**File:** `CacheService.java`, line 22
**Severity:** HIGH
**Category:** Bug / Style inconsistency

```java
public CacheService() {
    super(IntentService.class.getSimpleName());
}
```

`IntentService` requires its subclass to pass a thread name that identifies the worker thread for debugging. The idiomatic and correct argument is the *subclass* name: `CacheService.class.getSimpleName()` or the string literal `"CacheService"`. Passing `IntentService.class.getSimpleName()` (which evaluates to `"IntentService"`) gives the worker thread a generic name that is indistinguishable from any other `IntentService` subclass in thread dumps and logcat. The companion class `SyncService.java` (line 28) makes exactly the same error with `super(IntentService.class.getSimpleName())`, confirming this is a copy-paste defect repeated across the codebase.

**Resolution:** Replace with `super("CacheService");` or `super(CacheService.class.getSimpleName());`

---

### A45-3 — HIGH: Race condition — async network requests fired before prior async request can complete; `Thread.sleep(100)` used as a synchronisation proxy

**File:** `CacheService.java`, lines 52–72
**Severity:** HIGH
**Category:** Logic defect / Style inconsistency

```java
for (final EquipmentItem equipmentItem : resultArray.arrayList) {
    if (PreStartQuestionDb.needToCache(equipmentItem.id)) {
        webApi.getPreStartQuestionList(equipmentItem.id, new WebListener<...>() {
            // async callback — may not complete before loop ends
        });
    }
    ...
}

try {
    Thread.sleep(100);   // arbitrary 100 ms pause
} catch (InterruptedException e) {
    e.printStackTrace();
}
```

`webApi` in `CacheService` is created via `WebApi.sync()` (line 27), which sets `isSynchronous = true` on the underlying `HttpClient`. However, each call to `getPreStartQuestionList` inside the loop fires an independent request. There is no guarantee that all N outstanding requests complete within 100 ms, especially on slow or lossy networks. The `Thread.sleep(100)` is an acknowledgment that concurrent completion must be awaited, but it is not a reliable synchronisation mechanism. On slow networks the sleep exits before all responses return; on fast networks it wastes 100 ms unconditionally. This same pattern appears in `SyncService.java` as well (100 ms and 2000 ms sleeps), confirming a widespread design smell rather than a one-off.

Additionally, `InterruptedException` is silently swallowed via `e.printStackTrace()` (see A45-4) rather than restoring the interrupt flag, which prevents proper thread lifecycle management within `IntentService`.

**Resolution:** Use a `CountDownLatch`, `CompletableFuture`, or convert to truly synchronous HTTP calls so each request completes before the next begins. Do not use `Thread.sleep` as an ad-hoc barrier.

---

### A45-4 — MEDIUM: `InterruptedException` caught and swallowed via `e.printStackTrace()` without restoring interrupt flag

**File:** `CacheService.java`, lines 70–72
**Severity:** MEDIUM
**Category:** Style inconsistency / Dead code pathway

```java
} catch (InterruptedException e) {
    e.printStackTrace();
}
```

When `Thread.sleep` is interrupted, the thread's interrupted status is cleared. The correct response is to either propagate the exception or restore the interrupted status via `Thread.currentThread().interrupt()`. Using only `e.printStackTrace()` silently discards the interrupt signal and leaves the thread unaware that it was interrupted. This is against Java best practice and against the Android recommendation to handle interrupts in `IntentService` worker threads properly.

`e.printStackTrace()` also writes to `System.err`, which is invisible in Android's logcat unless explicitly redirected. It is not a substitute for `Log.e(TAG, ...)`.

**Resolution:**
```java
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    Log.w(TAG, "Sleep interrupted", e);
}
```

---

### A45-5 — MEDIUM: `IntentService` is deprecated in API 30 — no migration to `WorkManager` or `JobIntentService`

**File:** `CacheService.java`, line 3, 17
**Severity:** MEDIUM
**Category:** Build warning / Deprecated API usage

```java
import android.app.IntentService;
...
public class CacheService extends IntentService {
```

`android.app.IntentService` was deprecated in Android API level 30 (Android 11). The recommended replacement is `androidx.work.WorkManager` (for deferrable background work) or `JobIntentService` for compatibility. The same deprecation affects `SyncService.java`. Neither class has a migration path or a suppression annotation with a documented rationale. On Android 12+ (API 31), background service start restrictions mean `startService()` called from a `runLater` Runnable (which runs on the main thread from a delayed Handler post) can throw `IllegalStateException` if the app is not in the foreground at the time.

**Resolution:** Migrate `CacheService` to `WorkManager` with `PeriodicWorkRequest` or `OneTimeWorkRequest`, which handles background scheduling constraints natively.

---

### A45-6 — MEDIUM: Hardcoded magic number for cache TTL — no named constant

**File:** `DataBaseHelp.java`, line 19
**Severity:** MEDIUM
**Category:** Style inconsistency / Dead code

```java
long de = 2 * 60 * 60 * 1000;
```

The 2-hour cache TTL is an inline arithmetic expression with no named constant, no comment, and no connection to any configuration. If this value needs adjustment (e.g., for different network conditions or data freshness requirements), it must be hunted down in source. The variable name `de` (presumably short for "duration expiry") is cryptic. The companion variable `du` (line 18, presumably "duration used") is equally opaque.

**Resolution:** Extract to a named constant: `private static final long CACHE_TTL_MS = 2 * 60 * 60 * 1000L; // 2 hours`. Use `TimeUnit.HOURS.toMillis(2)` for clarity. Also rename `du` / `de` to `elapsedMs` / `ttlMs`.

---

### A45-7 — MEDIUM: `DataBaseHelp` class has no `private` constructor — instantiable utility class

**File:** `DataBaseHelp.java`, line 8
**Severity:** MEDIUM
**Category:** Style inconsistency / Leaky abstraction

```java
class DataBaseHelp {
    static <E extends RealmModel> RealmQuery<E> getRealmQuery(...) { ... }
    static boolean isExpired(long updateTime) { ... }
}
```

`DataBaseHelp` is a pure utility class: all methods are `static`, it holds no state, and it is never meant to be instantiated. However, the Java compiler generates a default public no-arg constructor. Any code with package access can call `new DataBaseHelp()`, which is meaningless. A `private DataBaseHelp() {}` constructor should be declared to make the intent explicit and suppress the compiler-generated one.

**Resolution:** Add `private DataBaseHelp() { throw new AssertionError("Utility class"); }`.

---

### A45-8 — MEDIUM: Asymmetric query pattern — `EquipmentDb.needToCache` does not filter by `userKey` via `DataBaseHelp.getRealmQuery`; `PreStartQuestionDb.needToCache` does

**File:** `EquipmentDb.java`, lines 24–25 vs. `PreStartQuestionDb.java`, lines 30–31 (context)
**Severity:** MEDIUM
**Category:** Style inconsistency / Leaky abstraction

```java
// EquipmentDb.java — needToCache (line 24)
RealmResults<EquipmentDb> equipments = realm.where(EquipmentDb.class)
        .equalTo("userId", userId)
        .findAll();

// PreStartQuestionDb.java — needToCache (line 30–31)
RealmResults<PreStartQuestionDb> questions = DataBaseHelp.getRealmQuery(realm, PreStartQuestionDb.class)
        .equalTo("equipmentId", equipmentId).findAll();
```

`DataBaseHelp.getRealmQuery` exists specifically to add a `userKey` scoping filter to all queries, preventing data from one user from being seen by another. `PreStartQuestionDb` uses this helper. `EquipmentDb` bypasses it entirely and queries directly by `userId`. This inconsistency means:

1. The purpose of `DataBaseHelp.getRealmQuery` is undermined — its contract ("all queries should be user-scoped via this helper") is not honoured by `EquipmentDb`.
2. `EquipmentDb` stores user data by `userId` (an `int`), while `PreStartQuestionDb` stores it by `userKey` (also derived from `WebData.instance().getUserId()`). The two field names for the same concept (`userId` vs `userKey`) are inconsistent across the model layer.

This is both a style inconsistency and a leaky abstraction — the encapsulation that `DataBaseHelp.getRealmQuery` was meant to provide is only partially applied.

**Resolution:** Either consistently use `DataBaseHelp.getRealmQuery` across all `Db` classes (adding a `userKey` field to `EquipmentDb`), or document why `EquipmentDb` intentionally bypasses it.

---

### A45-9 — MEDIUM: `SafeRealm.Execute(Action)` is not exception-safe — Realm is not closed if `action.Execute` throws

**File:** Referenced from `EquipmentDb.java` lines 21–27, 31–42, 46–55; `SafeRealm.java` lines 7–11
**Severity:** MEDIUM
**Category:** Leaky abstraction / Resource leak

```java
// SafeRealm.java lines 7–11
public static void Execute(SafeRealm.Action action) {
    Realm realm = Realm.getDefaultInstance();
    action.Execute(realm);
    realm.close();           // not called if action.Execute() throws
}
```

`SafeRealm.Execute(Action)` and `SafeRealm.Execute(Func<T>)` do not use try-finally to guarantee `realm.close()` is called. If `action.Execute(realm)` throws a `RuntimeException` (e.g., `RealmException`, `NullPointerException`), the Realm instance leaks. Realm has a per-thread reference count and leaked instances can cause `RealmFileException: Another process has the file open` or thread-level Realm corruption over time.

This is a quality issue in `SafeRealm.java` (not directly in the assigned files) but it directly affects all three files because they exclusively use `SafeRealm` for all database operations. It is reported here because every `SafeRealm.Execute` call in `EquipmentDb.java` inherits the defect.

**Resolution:** Wrap with try-finally:
```java
Realm realm = Realm.getDefaultInstance();
try {
    return func.Execute(realm);
} finally {
    realm.close();
}
```

---

### A45-10 — MEDIUM: `getEquipmentResultArray` parameter name `getEquipmentResultArray` shadows its own type — misleading parameter name in `saveEquipmentResultArray`

**File:** `EquipmentDb.java`, line 45
**Severity:** MEDIUM
**Category:** Style inconsistency

```java
public static void saveEquipmentResultArray(final int userId,
        final GetEquipmentResultArray getEquipmentResultArray) {
```

The parameter is named `getEquipmentResultArray`, which is identical to the type name `GetEquipmentResultArray` (modulo case). This naming conflates "get" (a verb suggestive of retrieval) with a parameter that is being *saved*. The same pattern appears in `PreStartQuestionDb.saveQuestions` (line 53) where the parameter is `getEquipmentResultArray` even though it carries `PreStartQuestionResultArray` data — a different type. This suggests the method and its parameter were copy-pasted from `EquipmentDb` without renaming.

**Resolution:** Rename the parameter to `resultArray` or `data` in both methods.

---

### A45-11 — LOW: `onSucceed` and `onFailed` callbacks in `onHandleIntent` perform no meaningful action — cache write never confirmed

**File:** `CacheService.java`, lines 35–43 and 54–62
**Severity:** LOW
**Category:** Dead code / Logic gap

```java
webApi.getEquipmentList(currentUser.getId(), new WebListener<GetEquipmentResultArray>() {
    @Override
    public void onSucceed(GetEquipmentResultArray result) {
        Log.d(TAG, "Cache equipment succeeded.");
        // result is not used — EquipmentDb.saveEquipmentResultArray not called here
    }

    @Override
    public void onFailed(WebResult result) {
        Log.d(TAG, "Cache equipment failed.");
    }
});
```

The `onSucceed` callback receives the `GetEquipmentResultArray` result but does not call `EquipmentDb.saveEquipmentResultArray`. Examining `WebApi.getEquipmentList` (line 198 of `WebApi.java`) reveals that the save is performed *inside* `WebApi` itself before the listener is called, so the result being unused here is technically correct — the architectural decision to embed the cache write inside `WebApi` rather than in the caller. However, this means the `CacheService` listener bodies are effectively no-ops beyond logging, and a future maintainer may not realise that the data is persisted elsewhere. The pattern is misleading.

**Resolution:** Either document with a comment why `result` is unused (the save occurs in `WebApi`), or move the save responsibility to the listener in `CacheService` for clarity of ownership.

---

### A45-12 — LOW: `startService()` delay is hardcoded at 5000 ms with no documentation

**File:** `CacheService.java`, line 82
**Severity:** LOW
**Category:** Style inconsistency / Dead code

```java
MyApplication.runLater(new Runnable() {
    @Override
    public void run() {
        MyApplication.getContext().startService(
            new Intent(MyApplication.getContext(), CacheService.class));
    }
}, 5000);
```

The 5-second delay before starting the service is a magic number with no accompanying comment explaining why this duration was chosen. `SyncService.startService()` also uses a 5-second delay. No named constant is shared between the two. If the delay exists to allow the calling activity to finish its own initialisation before background tasks begin, this should be documented.

**Resolution:** Extract to a named constant `private static final int START_DELAY_MS = 5000;` and add a comment explaining the rationale.

---

### A45-13 — LOW: `isExpired` branch for `updateTime > currentTime` returns `false` without logging — silent clock-skew acceptance

**File:** `DataBaseHelp.java`, lines 15–17
**Severity:** LOW
**Category:** Style inconsistency

```java
if (updateTime > currentTime) {
    return false;
}
```

If `updateTime` is in the future (e.g., due to device clock skew or a corrupted Realm record), the method silently returns `false` (not expired), meaning the cached data is treated as permanently fresh. This can cause stale equipment or prestart question data to persist indefinitely without a network refresh. There is no log message, no metric, and no fallback. A log warning would at minimum make this observable.

**Resolution:** Add `Log.w(TAG, "updateTime is in the future: " + updateTime + ", treating as not expired");` and consider returning `true` (expired) to force a refresh when the timestamp is implausible.

---

## Step 4: Summary Table

| ID | Severity | File | Lines | Description |
|----|----------|------|-------|-------------|
| A45-1 | HIGH | CacheService.java | 18 | `TAG` not declared `final` — mutable static logging constant |
| A45-2 | HIGH | CacheService.java | 22 | Constructor passes `IntentService` class name instead of `CacheService` as worker thread name |
| A45-3 | HIGH | CacheService.java | 52–72 | `Thread.sleep(100)` used as async-request synchronisation barrier — unreliable race condition |
| A45-4 | MEDIUM | CacheService.java | 70–72 | `InterruptedException` swallowed; interrupt flag not restored; `e.printStackTrace()` used instead of `Log` |
| A45-5 | MEDIUM | CacheService.java | 3, 17 | `IntentService` deprecated in API 30 — no migration path to `WorkManager` |
| A45-6 | MEDIUM | DataBaseHelp.java | 18–19 | Hardcoded 2-hour TTL as magic number; cryptic variable names `du` / `de` |
| A45-7 | MEDIUM | DataBaseHelp.java | 8 | Utility class lacks private constructor — instantiable via default no-arg constructor |
| A45-8 | MEDIUM | EquipmentDb.java | 24–25 | Asymmetric query pattern: bypasses `DataBaseHelp.getRealmQuery`; `userId` vs `userKey` field naming inconsistency |
| A45-9 | MEDIUM | EquipmentDb.java | 21–55 | `SafeRealm.Execute` not exception-safe — Realm not closed on `RuntimeException` (inherited defect from `SafeRealm`) |
| A45-10 | MEDIUM | EquipmentDb.java | 45 | Parameter named `getEquipmentResultArray` in a save method — misleading name copied from `PreStartQuestionDb` |
| A45-11 | LOW | CacheService.java | 35–62 | `onSucceed` callbacks are no-ops beyond logging — save occurs inside `WebApi`, undocumented |
| A45-12 | LOW | CacheService.java | 82 | 5000 ms start delay is a magic number with no explanation |
| A45-13 | LOW | DataBaseHelp.java | 15–17 | Silent clock-skew acceptance — future `updateTime` treated as not expired with no log or metric |
