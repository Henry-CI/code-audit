# Pass 1 Security Audit — Agent APP37

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Agent ID:** APP37

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

DISCREPANCY: The checklist states "Branch: main" but the actual branch is "master". The audit proceeds on "master" as instructed.

---

## Step 2 — Files Assigned

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/LocationDb.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/ModelPrefs.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/MyCommonValue.java`

---

## Step 3 & 4 — Reading Evidence

### File 1: LocationDb.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.LocationDb`

**Extends:** `io.realm.RealmObject` (Realm mobile database)

**Fields / Constants:**
- `public static String TAG` — class simple name, used for logging (line 24)
- `public int userKey` — initialized at field declaration from `WebData.instance().getUserId()` (line 26)
- `public int unit_id` (line 28)
- `public Double longitude` (line 29)
- `public Double latitude` (line 30)
- `public String gps_time` (line 31)

**Public methods (with line numbers):**
- `public static ArrayList<LocationDb> readAllLocationToSync()` — line 33
- `public static void removeData(SaveSingleGPSParameter)` — line 47
- `public static void uploadLocation()` — line 81
- `public static void saveNewLocation(SaveSingleGPSParameter)` — line 112

**Package-private methods:**
- `static RealmResults<LocationDb> readData(Realm)` — line 43
- `static void removeData(Realm, SaveMultipleGPSParameter)` — line 64

**Private methods:**
- `private static RealmResults<LocationDb> getMatchingRecord(Realm, int)` — line 76

---

### File 2: ModelPrefs.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.ModelPrefs`

**SharedPreferences file name:** `"prefs"` with `Context.MODE_PRIVATE` (line 17)

**Public methods (with line numbers):**
- `public static void saveInt(String key, int d)` — line 22
- `public static int readInt(String key)` — line 26
- `public static void deleteDataForKey(String key)` — line 31
- `public static void saveString(String key, String s)` — line 36
- `public static String readString(String key)` — line 40
- `public static void saveBoolean(String key, boolean s)` — line 45
- `public static boolean readBoolean(String key)` — line 49
- `public static void saveObject(String key, Object object)` — line 53 (serializes to JSON via Gson)
- `public static Object readObject(String key, Class<?>)` — line 61

**Package-private methods:**
- `static SharedPreferences getPref()` — line 16

**SharedPreferences keys observed in callers (via grep across codebase):**

| Key | Data stored | Source file |
|-----|-------------|-------------|
| `"current_user_id"` | Integer user ID | `CurrentUser.java` |
| `"last_session_id"` | Integer session counter (negative offline IDs) | `WebData.java` |
| `"token_result"` | Full `GetTokenResult` object serialized to JSON (authentication bearer token) | `WebData.java` |

All three are stored in plain (unencrypted) `SharedPreferences`.

---

### File 3: MyCommonValue.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.MyCommonValue`

**All constants and static fields:**
- `public static EquipmentItem currentEquipmentItem = null` — line 10: holds current equipment/forklift assignment; mutable static field on a non-Application class
- `public static Boolean isCheckLocationPermissionDone = false` — line 11: permission check flag
- `public static String companyName = ""` — line 13
- `public static String companyContract = ""` — line 14
- `public static String companyRole = ""` — line 15
- `public static String companyenabled = ""` — line 16

No hardcoded URLs, API keys, or credentials found in this file.

---

## Step 5 — Checklist Review

### Section 1 — Signing and Keystores

No keystore, signing, or Gradle files are within the assigned scope. Not applicable to these three files.

No issues found — Section 1 (not in scope for assigned files).

---

### Section 2 — Network Security

**FINDING — NS-01 — Hardcoded OAuth Client Credentials (Critical)**

File: `WebData.java` (discovered as a direct caller of `ModelPrefs`; reviewed as necessary supporting evidence for token storage findings).

Within `WebData.getTokenFormData()` (lines 56–82), the following values are hardcoded as string literals:

```java
String clientId = "987654321";                         // line 64
String clientSecret = "8752361E593A573E86CA558FFD39E"; // line 68
String userName = "gas";                               // line 72
String password = "ciiadmin";                          // line 76
```

These are OAuth2 Resource Owner Password Credentials grant parameters. A hardcoded `client_secret` and a hardcoded service-account username/password (`gas` / `ciiadmin`) are committed to version control. Any party with repository access has these credentials. Severity: **Critical**.

No hardcoded URLs, IP addresses, or API keys were found in the three assigned files (`LocationDb.java`, `ModelPrefs.java`, `MyCommonValue.java`).

---

### Section 3 — Data Storage

**FINDING — DS-01 — Authentication Token Stored in Plain SharedPreferences (High)**

File: `ModelPrefs.java` / `WebData.java`

The authentication bearer token (`GetTokenResult`) is persisted via `ModelPrefs.saveObject(TOKEN_ITEM_KEY, result)` (WebData.java line 93) and read back at `ModelPrefs.readObject(TOKEN_ITEM_KEY, GetTokenResult.class)` (line 119). `ModelPrefs` uses plain `SharedPreferences` (MODE_PRIVATE) with no encryption. The token is serialized to a JSON string and stored in `/data/data/<package>/shared_prefs/prefs.xml`.

On a rooted device or via ADB backup (if `allowBackup="true"`), this file is trivially readable. Jetpack Security `EncryptedSharedPreferences` should be used for any value that conveys authentication state.

Key: `"token_result"` — stores the full authentication token object. Severity: **High**.

**FINDING — DS-02 — User ID Persisted in Plain SharedPreferences (Low/Informational)**

Key: `"current_user_id"` — stores an integer user ID in plain SharedPreferences (CurrentUser.java lines 28, 34, 126). By itself an integer ID is low sensitivity, but in combination with the token finding it contributes to session reconstruction from storage. Severity: **Low**.

**FINDING — DS-03 — Offline Session ID Counter Persisted in Plain SharedPreferences (Informational)**

Key: `"last_session_id"` — stores a negative integer counter for offline session IDs (WebData.java lines 30–32). Not directly sensitive but demonstrates the pattern of using plain SharedPreferences for all persistence without any encrypted storage layer. Severity: **Informational**.

**FINDING — DS-04 — GPS/Location Data Stored in Unencrypted Realm Database (Medium)**

File: `LocationDb.java`

Forklift GPS coordinates (`latitude`, `longitude`, `gps_time`, `unit_id`) are persisted to a Realm database with no indication of Realm encryption. The Realm file is stored in the app's data directory. Without an encryption key passed to `RealmConfiguration`, the database file is a plain binary file readable on rooted devices. This data is operational telemetry tied to equipment unit IDs and timestamps. Severity: **Medium**.

**FINDING — DS-05 — Equipment Assignment Held in Static Field (Medium)**

File: `MyCommonValue.java` line 10

`public static EquipmentItem currentEquipmentItem` is a mutable public static field on a plain class. It holds the current operator's forklift assignment (confirmed via callers: includes `mac_address`, equipment `id`, and `trained` status). Using a static field for state that should be session-scoped creates risk of data leakage between operator sessions (e.g., if logout does not explicitly null this field, a subsequent operator inherits the prior assignment). This is particularly relevant given that the checklist calls out shift-change scenarios. Severity: **Medium**.

**FINDING — DS-06 — Company Metadata Fields Are Public Mutable Static (Low)**

File: `MyCommonValue.java` lines 13–16

`companyName`, `companyContract`, `companyRole`, and `companyenabled` are public mutable static fields with no access control. While not directly credentials, `companyContract` and `companyRole` may contain business-sensitive or authorization-related data. Access should be gated through methods, not bare public statics. Severity: **Low**.

No use of `MODE_WORLD_READABLE`, `MODE_WORLD_WRITEABLE`, or `Environment.getExternalStorageDirectory()` was found in the assigned files.

---

### Section 4 — Input and Intent Handling

No Activity, Service, BroadcastReceiver, WebView, or Intent handling code exists in the three assigned files. Not applicable.

No issues found — Section 4 (not in scope for assigned files).

---

### Section 5 — Authentication and Session

**FINDING — AUTH-01 — Token Not Stored in EncryptedSharedPreferences (High)**

As documented in DS-01 above, the bearer token is persisted to plain SharedPreferences. Checklist requirement: tokens must use EncryptedSharedPreferences or Android Keystore. This requirement is not met.

**FINDING — AUTH-02 — Logout Does Not Clear Token from SharedPreferences (High)**

File: `CurrentUser.java` lines 125–128

```java
public static void logout() {
    ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY);  // removes "current_user_id"
    user = null;
}
```

`logout()` removes only the `current_user_id` key. The `"token_result"` key (the bearer token) is never deleted on logout. After logout, a subsequent call to `WebData.instance().isAppInitialized()` would still return `true` and the stored token would be re-used. An operator logging out does not invalidate stored authentication state. Severity: **High**.

**FINDING — AUTH-03 — Static `currentEquipmentItem` Not Cleared on Logout (Medium)**

`MyCommonValue.currentEquipmentItem` (a public static field) is set in multiple places but there is no evidence in `CurrentUser.logout()` that it is nulled. If a new operator logs in on the same device without the app being fully restarted, the prior operator's forklift assignment persists in memory. Severity: **Medium** (linked to DS-05).

**FINDING — AUTH-04 — Hardcoded OAuth Service Account Password (Critical)**

As documented in NS-01 / DS-01, `WebData.getTokenFormData()` contains a hardcoded username (`gas`) and password (`ciiadmin`) used to obtain OAuth tokens. This is a service-account credential embedded in source code. Severity: **Critical** (cross-referenced from Section 2).

---

### Section 6 — Third-Party Libraries

No `build.gradle` or dependency declarations are in the assigned files. Not applicable.

No issues found — Section 6 (not in scope for assigned files).

---

### Section 7 — Google Play and Android Platform

**FINDING — PLAT-01 — Use of Deprecated Android Support Library (Low)**

File: `LocationDb.java` line 3

```java
import android.support.annotation.NonNull;
```

The `android.support.*` namespace is the legacy Android Support Library, superseded by AndroidX. This import should be `androidx.annotation.NonNull`. Projects still on the Support Library cannot use current Jetpack Security (`EncryptedSharedPreferences`), which requires AndroidX. This is relevant because one remediation for DS-01/AUTH-01 depends on AndroidX availability. Severity: **Low** (but blocking for recommended remediation).

No issues found — Section 7 (remainder not in scope for assigned files).

---

## Summary of Findings

| ID | Severity | File(s) | Description |
|----|----------|---------|-------------|
| AUTH-04 / NS-01 | Critical | `WebData.java` | Hardcoded OAuth2 client secret and service-account credentials (`gas`/`ciiadmin`) in source code |
| DS-01 / AUTH-01 | High | `ModelPrefs.java`, `WebData.java` | Bearer authentication token persisted in plain (unencrypted) SharedPreferences |
| AUTH-02 | High | `CurrentUser.java` | Logout does not delete `"token_result"` from SharedPreferences; token persists after logout |
| DS-04 | Medium | `LocationDb.java` | GPS location data stored in Realm database with no evidence of encryption |
| DS-05 / AUTH-03 | Medium | `MyCommonValue.java` | Current equipment assignment held in public mutable static field; not cleared on logout |
| DS-02 | Low | `ModelPrefs.java`, `CurrentUser.java` | User ID stored in plain SharedPreferences |
| DS-06 | Low | `MyCommonValue.java` | Company metadata (`companyContract`, `companyRole`) in public mutable static fields |
| DS-03 | Informational | `ModelPrefs.java`, `WebData.java` | Offline session ID counter in plain SharedPreferences |
| PLAT-01 | Low | `LocationDb.java` | Use of deprecated `android.support.annotation.NonNull` instead of AndroidX |

---

## Branch Discrepancy (Recorded)

The checklist header specifies `Branch: main`. The repository's active branch is `master`. The audit was conducted on `master` as directed by the task instructions.
