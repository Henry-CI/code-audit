# Pass 1 Security Audit — Agent APP36

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Agent:** APP36

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy:** The checklist states `Branch: main`. The actual branch is `master`. Proceeding on `master` as instructed.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/CacheService.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/DataBaseHelp.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/EquipmentDb.java`

---

## Reading Evidence

### File 1: CacheService.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.CacheService`

**Extends:** `android.app.IntentService`

**Fields:**
- `private static String TAG` — line 18 — class tag for logging
- `private WebApi webApi` — line 19 — web API client instance

**Public methods:**
- `public CacheService()` — line 21 — constructor, calls `super(IntentService.class.getSimpleName())`
- `public static void startService()` — line 76 — posts a delayed `startService` Intent to self via `MyApplication.runLater(..., 5000)`

**Package-private / protected methods:**
- `protected void onHandleIntent(Intent intent)` — line 26 — main background logic; lazy-initialises `webApi`, retrieves `CurrentUser`, checks network, then conditionally fetches equipment list and pre-start question list from the web API; results are handled by anonymous `WebListener` callbacks; equipment item IDs are logged to Logcat; a 100 ms `Thread.sleep` is used at line 69.

**Component type:** `IntentService` (background service)

---

### File 2: DataBaseHelp.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.DataBaseHelp`

**Access modifier:** package-private (`class DataBaseHelp`)

**Fields:** none

**Package-private static methods:**
- `static <E extends RealmModel> RealmQuery<E> getRealmQuery(Realm realm, Class<E> clazz)` — line 9 — builds a Realm query filtered by `userKey` equal to `WebData.instance().getUserId()`
- `static boolean isExpired(long updateTime)` — line 13 — returns `true` if `updateTime` is more than 2 hours (7,200,000 ms) in the past; also returns `false` if `updateTime` is in the future (likely a guard against clock skew)

---

### File 3: EquipmentDb.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.EquipmentDb`

**Extends:** `io.realm.RealmObject`

**Fields (private instance):**
- `private int userId` — line 13
- `private long updateTime` — line 14
- `private String equipmentListStr` — line 15 — stores the entire equipment list serialised as a JSON string

**Private methods:**
- `private boolean isExpired()` — line 16 — delegates to `DataBaseHelp.isExpired(updateTime)`

**Package-private static methods:**
- `static boolean needToCache(final int userId)` — line 20 — queries Realm for any `EquipmentDb` record for the given user; returns `true` if none exists or the record is expired

**Public static methods:**
- `public static GetEquipmentResultArray getEquipmentResultArray(final int userId)` — line 30 — retrieves the equipment list from Realm for the given user; deserialises `equipmentListStr` JSON via `GsonHelper.objectFromString`; returns an empty list if no record exists
- `public static void saveEquipmentResultArray(final int userId, final GetEquipmentResultArray getEquipmentResultArray)` — line 45 — writes or updates the equipment record in Realm; stores `userId`, current system time as `updateTime`, and the full result serialised as JSON in `equipmentListStr`

**Realm configuration (from MyApplication.java, `initDataBase()` at line 65):**

```java
RealmConfiguration config = new RealmConfiguration.Builder()
        .schemaVersion(4)
        .deleteRealmIfMigrationNeeded()
        .build();
Realm.setDefaultConfiguration(config);
```

No encryption key is passed to the `RealmConfiguration.Builder`. All three files in scope use `Realm.getDefaultInstance()` (via `SafeRealm`), which maps to this unencrypted configuration.

---

## Findings by Checklist Section

### 1. Signing and Keystores

No issues found in the assigned files — CacheService.java, DataBaseHelp.java, and EquipmentDb.java contain no signing configuration, keystore references, or credential material.

---

### 2. Network Security

No issues found in the assigned files — no HTTP client configuration, no URL construction, no TrustManager or hostname verifier code is present in these three files.

Note: `CacheService.java` invokes `webApi.getEquipmentList()` and `webApi.getPreStartQuestionList()` but does not configure the HTTP client; network security of those calls is determined by `WebApi`, which is outside the scope of this agent's assigned files.

---

### 3. Data Storage

#### FINDING DS-1 — High: Realm database used without encryption

**File:** `EquipmentDb.java` (storage layer); `DataBaseHelp.java` (query helper); `SafeRealm.java` (Realm accessor); `MyApplication.java` (Realm initialisation)

**Evidence:**

`MyApplication.initDataBase()` (lines 65–73) constructs the Realm configuration without a `.encryptionKey(...)` call:

```java
RealmConfiguration config = new RealmConfiguration.Builder()
        .schemaVersion(4)
        .deleteRealmIfMigrationNeeded()
        .build();
Realm.setDefaultConfiguration(config);
```

`SafeRealm.Execute()` and `SafeRealm.executeTransaction()` both call `Realm.getDefaultInstance()`, which uses this unencrypted configuration. `EquipmentDb` stores the full equipment list — which includes equipment IDs and related operational data — as a plain-text JSON string in the field `equipmentListStr` (line 15, `EquipmentDb.java`).

**Impact:** The Realm database file (`default.realm`) is stored in the app's internal data directory. While not world-readable to other apps on a non-rooted device, it is accessible without decryption on any rooted device or via ADB backup if `android:allowBackup` is enabled. Realm's own documentation recommends at-rest encryption for sensitive data. For a forklift management application handling operator assignments, pre-start question results, and operational telemetry, the absence of database encryption represents a meaningful exposure risk.

**Recommendation:** Provide a 64-byte AES-256/SHA-2 encryption key — generated once and stored in Android Keystore — to `RealmConfiguration.Builder().encryptionKey(key)`.

---

#### FINDING DS-2 — Medium: `deleteRealmIfMigrationNeeded()` in production configuration

**File:** `MyApplication.java`, line 70 (context for assigned files)

**Evidence:**

```java
.deleteRealmIfMigrationNeeded()
```

This directive silently deletes the entire Realm database when the schema version increments rather than running a migration. All locally cached equipment data and pre-start question data is destroyed without any warning to the user or error reporting.

**Impact:** Operational data loss — if `CacheService` has not had time to re-sync after a schema bump, operators may temporarily see no equipment list or pre-start questions, which can block forklift use. This also masks upgrade issues in production, making regression harder to detect. While not a direct confidentiality issue, it is a data-integrity risk.

**Recommendation:** Replace `deleteRealmIfMigrationNeeded()` with an explicit `RealmMigration` implementation that handles schema changes in a controlled manner.

---

#### FINDING DS-3 — Low: Equipment item IDs logged to Logcat in production service

**File:** `CacheService.java`, lines 55 and 64

**Evidence:**

```java
Log.d(TAG, "Cache prestart done: " + equipmentItem.id);
// ...
Log.d(TAG, "Cache prestart last cache not expired: " + equipmentItem.id);
```

**Impact:** Equipment IDs are written to Android system Logcat using `Log.d`. On Android 4.0 and earlier any app with `READ_LOGS` permission could read this. On modern Android, Logcat access is restricted to the app's own process in production, but equipment IDs remain visible via ADB on debug builds and on rooted devices. If ProGuard/R8 with log stripping is not configured, these statements are present in release builds.

**Recommendation:** Remove or guard debug log statements containing operational identifiers behind a `BuildConfig.DEBUG` check, or use a logging library that strips debug-level logs in release builds.

---

### 4. Input and Intent Handling

No issues found — these files do not declare exported components, handle incoming intents with user-supplied data, use WebViews, or configure deep links. `CacheService` is an `IntentService` started explicitly by `MyApplication` and does not process any data from the triggering intent.

---

### 5. Authentication and Session

No issues found in the assigned files — `CacheService.java` reads `CurrentUser.get()` to obtain the authenticated user, but does not store or cache credentials itself. Token/credential storage is handled by `CurrentUser`/`WebData` classes outside the scope of this agent.

---

### 6. Third-Party Libraries

No issues found in the assigned files — no `build.gradle` dependencies are declared in these files. The Realm library is used; Realm version and CVE status should be assessed by the agent reviewing `build.gradle`.

---

### 7. Google Play and Android Platform

#### FINDING GP-1 — Low: `IntentService` is deprecated

**File:** `CacheService.java`, line 17

**Evidence:**

```java
public class CacheService extends IntentService {
```

`android.app.IntentService` was deprecated in API level 30 (Android 11). Google recommends migrating to `WorkManager` or `JobIntentService`.

**Impact:** No immediate security impact, but use of a deprecated component class signals outdated API usage that may attract additional scrutiny during Play Store reviews and will eventually be flagged by lint as an error.

**Recommendation:** Migrate `CacheService` to `WorkManager` with a `CoroutineWorker` or `ListenableWorker`.

---

## Summary Table

| ID    | Severity | Section        | File(s)                              | Title                                             |
|-------|----------|----------------|--------------------------------------|---------------------------------------------------|
| DS-1  | High     | Data Storage   | EquipmentDb.java, MyApplication.java | Realm database stored without encryption          |
| DS-2  | Medium   | Data Storage   | MyApplication.java                   | `deleteRealmIfMigrationNeeded()` causes data loss |
| DS-3  | Low      | Data Storage   | CacheService.java                    | Equipment IDs logged to Logcat in release code    |
| GP-1  | Low      | Android Platform | CacheService.java                  | `IntentService` is deprecated (API 30+)           |
