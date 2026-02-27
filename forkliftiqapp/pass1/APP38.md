# Pass 1 Security Audit — APP38
**Agent ID:** APP38
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`, but the actual active branch is `master`. Audit proceeds on `master` as instructed.

---

## Step 2 — Checklist Reference

Full checklist read from `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`. Sections covered: Signing and Keystores, Network Security, Data Storage, Input and Intent Handling, Authentication and Session, Third-Party Libraries, Google Play and Android Platform.

---

## Step 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/PreStartHistoryDb.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/PreStartQuestionDb.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/RealmInt.java`

Supporting files read for context (Realm configuration evidence):
- `model/SafeRealm.java`
- `model/DataBaseHelp.java`
- `ui/application/MyApplication.java`

---

## Step 4 — Reading Evidence

### File 1: PreStartHistoryDb.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.PreStartHistoryDb`

**Extends:** `io.realm.RealmObject`

**Fields:**
| Field | Type | Visibility | Line |
|---|---|---|---|
| `userKey` | `int` | `public` | 13 |
| `dateTime` | `String` | `private` | 15 |
| `driver_id` | `int` | `public` | 16 |
| `unit_id` | `int` | `public` | 17 |

**Field initialisation note:** `userKey` is initialised inline at declaration time (line 13): `public int userKey = WebData.instance().getUserId();`. This calls a live singleton at class/object construction time.

**Public methods:**
| Method | Return type | Line |
|---|---|---|
| `hasPreStartDoneForToday(final int driver_id, final int unit_id)` | `static boolean` | 19 |

**Package-private methods:**
| Method | Return type | Line |
|---|---|---|
| `setPreStartDone(final int driver_id, final int unit_id)` | `static void` | 33 |

**Imports / dependencies:**
- `au.com.collectiveintelligence.fleetiq360.WebService.WebData`
- `au.com.collectiveintelligence.fleetiq360.util.CommonFunc`
- `io.realm.Realm`, `io.realm.RealmObject`, `io.realm.RealmResults`
- `org.joda.time.DateTime`

**Data stored:** Driver ID, unit (equipment) ID, datetime of last completed pre-start check. This constitutes operational safety-critical records: whether a forklift operator performed a mandated vehicle inspection for the current day.

---

### File 2: PreStartQuestionDb.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.PreStartQuestionDb`

**Extends:** `io.realm.RealmObject`

**Fields:**
| Field | Type | Visibility | Line |
|---|---|---|---|
| `userKey` | `int` | `public` | 15 |
| `updateTime` | `long` | `private` | 17 |
| `prestartQuestionResultArray` | `String` | `private` | 18 |
| `equipmentId` | `int` | `private` | 20 |

**Private methods:**
| Method | Return type | Line |
|---|---|---|
| `isExpired()` | `boolean` | 22 |

**Package-private methods:**
| Method | Return type | Line |
|---|---|---|
| `needToCache(final int equipmentId)` | `static boolean` | 26 |

**Public methods:**
| Method | Return type | Line |
|---|---|---|
| `getQuestionResultArray(final int equipmentId)` | `static PreStartQuestionResultArray` | 37 |
| `saveQuestions(final int equipmentId, final PreStartQuestionResultArray getEquipmentResultArray)` | `static void` | 53 |

**Imports / dependencies:**
- `au.com.collectiveintelligence.fleetiq360.WebService.WebData`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.PreStartQuestionResultArray`
- `com.yy.libcommon.WebService.GsonHelper`
- `io.realm.Realm`, `io.realm.RealmObject`, `io.realm.RealmResults`

**Data stored:** The full pre-start checklist question set for a given piece of equipment, serialised as a JSON string via `GsonHelper.stringFromObjectNoPolicy()`, plus the equipment ID and a cache timestamp. The `isExpired()` method enforces a 2-hour cache TTL (confirmed in `DataBaseHelp.isExpired()`: `de = 2 * 60 * 60 * 1000`). This is safety-critical data: it defines the questions operators must answer before operating forklifts.

---

### File 3: RealmInt.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.RealmInt`

**Extends:** `io.realm.RealmObject`

**Fields:**
| Field | Type | Visibility | Line |
|---|---|---|---|
| `data` | `int` | package-private | 9 |

**Public methods:** None.

**Purpose:** A simple Realm-compatible wrapper for a primitive integer. No sensitive data stored in this class itself. Created 1/10/16 (comment on line 7).

---

### Supporting context — Realm Configuration (MyApplication.java lines 65–73)

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

No `.encryptionKey(...)` call is present. The Realm database is created with no encryption key. All `RealmObject` subclasses (including `PreStartHistoryDb` and `PreStartQuestionDb`) are stored in this unencrypted database.

**SafeRealm.java:** All Realm access goes through `Realm.getDefaultInstance()`, which uses the configuration above with no encryption.

**DataBaseHelp.java:** All queries are scoped by `userKey` (the logged-in user's integer ID), providing logical data separation between users but no cryptographic protection.

---

## Step 5 — Checklist Review

### Section 1 — Signing and Keystores

No `.jks`, `.keystore`, or `.p12` files are present in the assigned files. No signing configuration is present in these model files.

**No issues found — Section 1** (from assigned files; signing config not present in these files).

---

### Section 2 — Network Security

No HTTP client code, URL configuration, or network calls are present in the three assigned files. `PreStartQuestionDb` and `PreStartHistoryDb` are pure Realm model/cache classes. Network calls originate elsewhere (e.g., `WebApi`).

**No issues found — Section 2** (from assigned files).

---

### Section 3 — Data Storage

**FINDING DS-1 — HIGH — Unencrypted Realm database storing safety-critical pre-start check data**

The Realm database is initialised in `MyApplication.initDataBase()` (lines 65–73) without an encryption key:

```java
RealmConfiguration config = new RealmConfiguration.Builder()
        .schemaVersion(4)
        .deleteRealmIfMigrationNeeded()
        .build();
```

No `.encryptionKey(byte[])` call is made. As a result, the Realm database file (stored at the app's internal storage path, typically `/data/data/<package>/files/default.realm`) is written in plaintext to disk.

`PreStartHistoryDb` stores:
- `driver_id` — identifies the forklift operator
- `unit_id` — identifies the forklift
- `dateTime` — timestamp of the last completed pre-start inspection

`PreStartQuestionDb` stores:
- `equipmentId` — equipment identifier
- `prestartQuestionResultArray` — the full JSON payload of pre-start checklist questions for that equipment, fetched from the backend and cached locally

This data is safety-critical: it is the mechanism by which the app enforces whether an operator has completed a mandatory vehicle safety inspection before operating a forklift. Storing it in an unencrypted database means:

1. On a rooted device, any app or actor with root access can read, modify, or delete these records.
2. If the device is physically accessed (e.g., seized, lost, or forensically imaged), all pre-start records and question definitions are exposed without any key material being required.
3. An attacker with root access could forge `PreStartHistoryDb` records to make the app believe a pre-start check has already been completed for today, bypassing the safety gate entirely. The `hasPreStartDoneForToday()` method reads directly from this unprotected store.

Realm's documentation provides `RealmConfiguration.Builder().encryptionKey(byte[])` accepting a 64-byte AES key, which would protect the data at rest. The key should be stored in the Android Keystore.

**FINDING DS-2 — LOW — `deleteRealmIfMigrationNeeded()` in production configuration**

`MyApplication.initDataBase()` uses `.deleteRealmIfMigrationNeeded()` on the `RealmConfiguration`. This instructs Realm to silently delete and recreate the database whenever a schema version mismatch is detected (e.g., after an app update). For general cache data this is acceptable; however, `PreStartHistoryDb` records are safety-critical audit trail data. Silent database deletion on upgrade would erase all historical pre-start check records stored on device, with no warning to the user or server-side reconciliation trigger visible in these files. If any offline records had not yet synced, they would be unrecoverably lost.

**FINDING DS-3 — INFO — `prestartQuestionResultArray` serialised with `GsonHelper.stringFromObjectNoPolicy()`**

In `PreStartQuestionDb.saveQuestions()` (line 64), the pre-start question array is serialised using `GsonHelper.stringFromObjectNoPolicy()`. The method name suffix `NoPolicy` suggests a serialisation path that bypasses a serialisation exclusion policy (e.g., `@Expose`-filtered fields). If the `PreStartQuestionResultArray` object graph contains fields that should not be persisted (e.g., transient answer state, user-specific metadata), they may be inadvertently written to the cache. This requires review of `PreStartQuestionResultArray` and `GsonHelper`, which are outside the assigned files.

**FINDING DS-4 — INFO — `userKey` initialised at field declaration from live singleton**

Both `PreStartHistoryDb` (line 13) and `PreStartQuestionDb` (line 15) declare:

```java
public int userKey = WebData.instance().getUserId();
```

This executes at object construction time. If a `PreStartHistoryDb` or `PreStartQuestionDb` object is ever constructed before a user has authenticated (i.e., before `WebData` has a valid user ID), the `userKey` field will be set to whatever `getUserId()` returns for an unauthenticated state (likely `0` or `-1`). Records written with an incorrect `userKey` would either be invisible to subsequent queries (which filter on `userKey`) or, if `0`, potentially visible across all unauthenticated sessions. This should be verified against the lifecycle guarantees of `WebData.instance()`.

---

### Section 4 — Input and Intent Handling

No Activity, Fragment, Service, BroadcastReceiver, ContentProvider, WebView, or Intent handling code is present in the three assigned files. These are pure model/data-access classes.

**No issues found — Section 4** (from assigned files).

---

### Section 5 — Authentication and Session

`DataBaseHelp.getRealmQuery()` scopes all queries with `.equalTo("userKey", WebData.instance().getUserId())`. This provides logical per-user data isolation within the shared Realm database. However, because the database is unencrypted (see DS-1), this isolation is only logical, not cryptographic — any actor who can access the raw database file can read all users' records regardless of `userKey`.

There is no code in the assigned files that clears pre-start history on logout. Whether `PreStartHistoryDb` records are removed when a user logs out or when a shift changes requires review of the logout/session teardown path, which is outside the assigned files.

**No new issues beyond DS-1.**

---

### Section 6 — Third-Party Libraries

Libraries referenced in the assigned files:

| Library | Reference | Notes |
|---|---|---|
| `io.realm` | Realm Java (RealmObject, Realm, RealmResults, RealmQuery, RealmConfiguration) | Used throughout; version not visible in assigned files |
| `org.joda.time` | Joda-Time (`DateTime`) | Used in `PreStartHistoryDb`; legacy library, superceded by `java.time` (API 26+) |
| `com.yy.libcommon` | Internal/vendored `GsonHelper` | Not a public library; cannot assess CVE status from assigned files |

The Realm version cannot be determined from the assigned files. Realm Java has had significant security and compatibility issues across versions, and its encryption feature is only available if configured (which it is not here — see DS-1). Version check requires `build.gradle`.

**No issues found — Section 6** (from assigned files only; version audit requires `build.gradle`).

---

### Section 7 — Google Play and Android Platform

`PreStartHistoryDb` uses `org.joda.time.DateTime` (line 27, 46) rather than `java.time` (available from API 26, fully backported via desugaring). Joda-Time has been deprecated in favour of `java.time` and is no longer actively maintained for Android use. This is a maintenance-level concern rather than a security issue.

No deprecated Android API usage (`AsyncTask`, `startActivityForResult`, etc.) is present in the assigned files.

**No issues found — Section 7** (from assigned files).

---

## Summary of Findings

| ID | Severity | Section | File | Description |
|---|---|---|---|---|
| DS-1 | HIGH | Data Storage | `MyApplication.java` (configuration) / all Realm models | Realm database has no encryption key configured. Safety-critical pre-start check records (`PreStartHistoryDb`, `PreStartQuestionDb`) stored in plaintext on disk. An attacker with root access can read or forge pre-start history to bypass the vehicle safety inspection gate. |
| DS-2 | LOW | Data Storage | `MyApplication.java` | `deleteRealmIfMigrationNeeded()` silently destroys all on-device pre-start records on schema version change. Offline records not yet synced would be unrecoverably lost. |
| DS-3 | INFO | Data Storage | `PreStartQuestionDb.java` line 64 | `GsonHelper.stringFromObjectNoPolicy()` may serialise fields that should be excluded. Requires review of `PreStartQuestionResultArray`. |
| DS-4 | INFO | Data Storage | `PreStartHistoryDb.java` line 13, `PreStartQuestionDb.java` line 15 | `userKey` initialised at field-declaration time from a live singleton; risk of zero/default `userKey` if object constructed before user authentication is established. |

---

*End of report — Agent APP38*
