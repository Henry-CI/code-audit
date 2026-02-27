# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP39
**Date:** 2026-02-27
**Stack:** Android/Java
**Auditor:** Automated — Claude Sonnet 4.6

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Branch confirmed as `master`. The checklist specifies "Branch: main" — this is a discrepancy. The active branch is `master`, not `main`. Audit proceeds on `master`.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/RealmString.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/SafeRealm.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/SessionDb.java`

Supporting files read for context:
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/application/MyApplication.java` (Realm initialisation)
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/SessionResult.java` (session data shape)

---

## Reading Evidence

### File 1: RealmString.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.RealmString`

**Superclass:** `io.realm.RealmObject`

**Fields:**
| Name | Type | Access | Line |
|------|------|--------|------|
| `data` | `String` | package-private (no modifier) | 9 |

**Public methods:** None declared. Inherits `RealmObject` lifecycle methods.

**Notes:** A minimal Realm model that wraps a single String. No annotations (`@PrimaryKey`, `@Index`, `@Required`) are present. The `data` field has package-private visibility, meaning it is accessible across the model package without a getter.

---

### File 2: SafeRealm.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.SafeRealm`

**Public methods:**
| Signature | Line |
|-----------|------|
| `public static void Execute(SafeRealm.Action action)` | 7 |
| `public static void executeTransaction(final SafeRealm.Action action)` | 13 |
| `public static <T> T Execute(SafeRealm.Func<T> func)` | 24 |

**Public interfaces declared:**
| Interface | Method signature | Line |
|-----------|-----------------|------|
| `Action` | `void Execute(Realm realm)` | 31–33 |
| `Func<T>` | `T Execute(Realm realm)` | 35–37 |

**Realm acquisition:** All three methods call `Realm.getDefaultInstance()` (lines 8, 14, 25). No `RealmConfiguration` is constructed here; SafeRealm delegates entirely to the application-level default configuration.

**Encryption:** No `encryptionKey` call anywhere in this file. Encryption is not configured at the wrapper level.

**Supporting context — MyApplication.java (initDataBase, lines 65–73):**
```java
private void initDataBase() {
    Realm.init(context);
    RealmConfiguration config = new RealmConfiguration.Builder()
            .schemaVersion(4)
            .deleteRealmIfMigrationNeeded()
            .build();
    Realm.setDefaultConfiguration(config);
}
```
No `.encryptionKey(...)` call is present. The Realm database is initialised without encryption. All data written through `SafeRealm` is stored unencrypted on disk.

---

### File 3: SessionDb.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.SessionDb`

**Superclass:** `io.realm.RealmObject`

**Fields:**
| Name | Type | Access | Line |
|------|------|--------|------|
| `userKey` | `int` | `public` | 21 |
| `sessionId` | `int` | package-private | 23 |
| `dataStr` | `String` | `private` | 24 |
| `equipmentItemStr` | `String` | `private` | 25 |
| `connectionRetry` | `int` | `private` | 27 |
| `equipmentSetupDone` | `boolean` | `private` | 29 |
| `preStartFinished` | `boolean` | `public` | 30 |
| `preStartResults` | `String` | `private` | 31 |
| `sessionFinished` | `boolean` | `private` | 33 |
| `startedOffline` | `boolean` | `private` | 34 |
| `stoppedOffline` | `boolean` | `private` | 35 |
| `prestartOffline` | `boolean` | `private` | 36 |
| `abortedOffline` | `boolean` | package-private | 37 |
| `aborted` | `boolean` | `private` | 38 |
| `toDelete` | `boolean` | `private` | 39 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `public SessionResult getSessionResult()` | 41 |
| `public void setSessionResult(SessionResult result)` | 50 |
| `public EquipmentItem getEquipmentItem()` | 54 |
| `public static boolean isEquipmentSetupDone(final int sessionId)` | 58 |
| `public static boolean isPreStartFinished(final int sessionId)` | 68 |
| `public static void setSessionPreFinish(final int sessionId, final String finishTime)` | 178 |
| `public static void addRunningChangeListener(...)` | 202 |
| `public static SessionDb readRunningSessionDb()` | 255 |
| `public static EquipmentItem readRunningEquipmentItem()` | 260 |
| `public static SessionResult readRunningSession()` | 265 |
| `public static SessionResult readUnfinishedSession()` | 270 |
| `public static boolean hasOfflineData(final int sessionId)` | 290 |
| `public static void setSessionAborted(final int sessionId, final boolean offline)` | 306 |
| `public static void setSessionFinished(final int sessionId, final String finish_time, final boolean offline)` | 338 |
| `public static void setSessionResultWithPreStartRequired(final SessionResult sessionResult, boolean prestartRequired)` | 378 |
| `public static void setSessionPreStartFinished(final int sessionId, final SavePreStartParameter parameter, final boolean offline)` | 395 |
| `public static void setSessionConnected(final int sessionId, final boolean connected)` | 418 |
| `public static void saveData(final SessionResult result, final EquipmentItem equipmentItem, final boolean offline)` | 461 |
| `public int incrementConnectionRetry()` | 467 |

**Session data stored (via `SessionResult`):**
`driver_id` (operator identifier), `unit_id` (forklift identifier), `start_time`, `finish_time`, `prestart_required`, session `id`. These are serialised to JSON and stored in `dataStr` (line 24). Pre-start answers are stored in `preStartResults` (line 31).

**Notable initialisation:** `userKey` is populated at field-declaration time with `WebData.instance().getUserId()` (line 21) — this executes on object construction, not on a Realm transaction thread.

---

## Findings by Checklist Section

### 1. Signing and Keystores

No signing or keystore configuration is present in the assigned files. No issue raised for these files.

**No issues found — Section 1 (assigned files scope)**

---

### 2. Network Security

No network client code, URL configuration, or SSL handling is present in the assigned files.

**No issues found — Section 2 (assigned files scope)**

---

### 3. Data Storage

#### FINDING DS-1 — High: Realm database has no encryption

**File:** `SafeRealm.java` (all three `Execute`/`executeTransaction` methods, lines 7–29)
**Confirmed by:** `MyApplication.java`, `initDataBase()`, lines 65–73

`SafeRealm` acquires its Realm instance exclusively via `Realm.getDefaultInstance()`. The default `RealmConfiguration` is set in `MyApplication.initDataBase()` using a builder that sets only `schemaVersion(4)` and `deleteRealmIfMigrationNeeded()`. No `.encryptionKey(...)` call is present.

The Realm database file is therefore stored unencrypted on the device's internal storage. All data written through `SafeRealm` — including the session data stored in `SessionDb` — is readable by any process with root access or via a physical device extraction. On devices without full-disk encryption (or devices that have been rooted), this data is recoverable.

```java
// MyApplication.java lines 68–71 — no encryptionKey():
RealmConfiguration config = new RealmConfiguration.Builder()
        .schemaVersion(4)
        .deleteRealmIfMigrationNeeded()
        .build();
```

**Recommendation:** Supply a 64-byte encryption key generated once and stored in Android Keystore using `KeyGenerator` with `KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT`. Pass it to `RealmConfiguration.Builder().encryptionKey(key)`.

---

#### FINDING DS-2 — Medium: Session records contain operator and forklift identifiers stored without encryption

**File:** `SessionDb.java`, fields `dataStr` (line 24) and `preStartResults` (line 31)
**Related:** `SessionResult.java` — fields `driver_id`, `unit_id`, `start_time`, `finish_time`

`SessionDb.dataStr` stores a JSON-serialised `SessionResult` object. This object contains `driver_id` (operator identity) and `unit_id` (forklift identity), timestamps, and pre-start check results. The field `preStartResults` stores serialised `SavePreStartParameter` objects, including checklist answers and timestamps.

These records are persisted into the unencrypted Realm database and are available without authentication to any process that can read the database file. Even if the Realm encryption issue (DS-1) is resolved, the field-level data modelling should be reviewed: `dataStr` and `preStartResults` are plain JSON blobs, and there is no field-level encryption applied.

Additionally, `userKey` is assigned at field-declaration time (`public int userKey = WebData.instance().getUserId()`, line 21). This is called on the object constructor thread (during Realm object creation), not within a Realm write transaction. While this is unlikely to cause a data corruption bug in practice, it is irregular for a Realm-managed field to be initialised this way.

---

#### FINDING DS-3 — Low: `deleteRealmIfMigrationNeeded()` causes silent data loss on schema change

**File:** `MyApplication.java`, `initDataBase()`, line 70 (context for SafeRealm usage)

The Realm configuration uses `.deleteRealmIfMigrationNeeded()`. This means that on any schema version mismatch the entire database — including all locally stored sessions, pre-start results, and offline-buffered data — is silently deleted. If a firmware update or app update changes the schema while the device holds unsynced offline session records, those records are permanently destroyed without user notification. This is a data integrity concern with an operational safety implication for a forklift management system where offline pre-start checks may not have been synced.

---

#### FINDING DS-4 — Low: `RealmString.data` field has package-private access with no getter

**File:** `RealmString.java`, line 9

The field `data` is package-private (no access modifier). Realm requires either a matching getter/setter pair or direct field access. Without a getter, the field is directly accessible to all classes within `au.com.collectiveintelligence.fleetiq360.model`. This does not constitute a security vulnerability in isolation, but it means there is no access control boundary around the data this object holds.

---

### 4. Input and Intent Handling

No Activity, Intent, WebView, or deep link handling code is present in the assigned files.

**No issues found — Section 4 (assigned files scope)**

---

### 5. Authentication and Session

#### FINDING AUTH-1 — Informational: Session records do not store raw authentication tokens

**File:** `SessionDb.java`, all fields (lines 20–39)

Reviewing all fields and the `SessionResult` structure, `SessionDb` does not directly store authentication tokens or passwords. The session data (operator ID, unit ID, timestamps, pre-start results) is operational/telemetry data, not authentication credentials. The authentication token layer is handled elsewhere (see `GetTokenResult`, `TokenAuthenticator` classes outside the assigned scope).

This is an informational note: the session database holds PII-adjacent data (operator identity and activity) but not credential material, which partially limits the impact of the unencrypted Realm finding (DS-1). Nevertheless, operator activity data is sensitive in an employment and safety-audit context and should be protected accordingly.

---

#### FINDING AUTH-2 — Low: `Objects.requireNonNull` in `incrementConnectionRetry()` will throw NullPointerException if no running session exists

**File:** `SessionDb.java`, line 486

```java
return Objects.requireNonNull(readRunningSessionDb()).connectionRetry;
```

If `readRunningSessionDb()` returns `null` (no active session), this line throws `NullPointerException` at runtime. This is a reliability issue; a crash here could interrupt a sync retry loop. Not a direct security finding, but uncaught exceptions in sync services can lead to session data not being uploaded, potentially affecting auditability of operator activity.

---

### 6. Third-Party Libraries

`SafeRealm` and `SessionDb` use `io.realm.Realm`. The specific Realm version is not determinable from the assigned files; the `build.gradle` dependency list is outside the assigned scope and has not been read. No findings raised from the assigned files alone.

**No issues found — Section 6 (assigned files scope)**

---

### 7. Google Play and Android Platform

The assigned files use `android.support.annotation.NonNull` (lines `SafeRealm.java:3`, `SessionDb.java` import context). The `android.support.*` namespace is from the legacy Android Support Library, which was superseded by AndroidX. This indicates the project has not been migrated to AndroidX. Support Library is no longer updated and received its final release in 2018. This is noted here as context; full assessment of deprecated API usage is outside the assigned file scope.

**No issues found directly — Section 7 (assigned files scope); see note on Support Library**

---

## Summary of Findings

| ID | Severity | File | Description |
|----|----------|------|-------------|
| DS-1 | High | `SafeRealm.java` / `MyApplication.java` | Realm database initialised without encryption; all persisted session and operator data is stored in plaintext |
| DS-2 | Medium | `SessionDb.java` | Operator identity (`driver_id`), unit identity (`unit_id`), and pre-start check results written as plain JSON blobs into the unencrypted Realm database |
| DS-3 | Low | `MyApplication.java` (context) | `deleteRealmIfMigrationNeeded()` causes silent, total database deletion on schema version mismatch; unsynced offline session records can be permanently lost |
| DS-4 | Low | `RealmString.java` | `data` field is package-private with no getter; no access control boundary |
| AUTH-1 | Informational | `SessionDb.java` | Session records do not store raw auth tokens; credential impact of unencrypted Realm is limited to operator identity and activity data |
| AUTH-2 | Low | `SessionDb.java:486` | `Objects.requireNonNull(readRunningSessionDb())` will throw NPE if no active session exists, potentially breaking sync retry |

---

## Branch Discrepancy Record

The checklist header states `Branch: main`. The repository's active branch is `master`. These are distinct branches; it is possible the checklist was written against a branch that has since been renamed or that `main` does not exist in this repository. All audit work in this report was performed against the `master` branch as confirmed by `git branch --show-current`.
