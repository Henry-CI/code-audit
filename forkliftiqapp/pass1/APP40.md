# Pass 1 Security Audit — APP40
**Agent:** APP40
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android / Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist states "Branch: main" but the actual current branch is `master`. Audit proceeds on `master` as confirmed.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/SyncService.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/TakePhotoPathPrefs.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/UserInfoPrefs.java`

Supporting files read to establish full evidence context:
- `WebService/WebApi.java`
- `WebService/URLBuilder.java`
- `WebService/WebData.java`
- `WebService/HttpClient.java`
- `WebService/FakeX509TrustManager.java`
- `model/ModelPrefs.java`
- `user/CurrentUser.java`
- `user/UserDb.java`
- `user/UserRealmObject.java`

---

## Reading Evidence

### SyncService.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.SyncService`
**Extends:** `android.app.IntentService`

**Fields / constants:**
| Name | Type | Scope | Value |
|------|------|-------|-------|
| `TAG` | `String` | private static | `"SyncService"` |
| `webApi` | `WebApi` | private | (instance, lazy-initialised) |

**Public methods:**

| Method | Line |
|--------|------|
| `SyncService()` constructor | 27 |
| `onHandleIntent(Intent intent)` (override) | 32 |
| `static startService()` | 157 |

**Private methods:**

| Method | Line |
|--------|------|
| `syncSession()` | 49 |
| `syncOfflineLocation()` | 82 |
| `deleteAbortedSession()` | 98 |
| `syncSessionItems()` | 118 |

**Data synced:**
- Offline sessions (pre-start results, driver ID, unit ID, start/finish times)
- Aborted sessions (delete on server)
- GPS location data (offline location queue)

**Authentication mechanism:** Uses `WebApi.sync()` which delegates to `HttpClient`. Every request attaches a Bearer token via `WebData.instance().getAuthHeader()`. Token is obtained via `authApp()` using hardcoded OAuth credentials (see WebData section below).

**Transport:** All URLs are constructed from `BuildConfig.BASE_URL` via `URLBuilder`. The token endpoint is `baseUrl + "/oauth/token"`. Protocol depends on the value of `BuildConfig.BASE_URL` (not hardcoded in source; build-config injected). However, `HttpClient.addRequest()` calls `FakeX509TrustManager.allowAllSSL()` before every request — see findings below.

**Service exported status:** Declared as a Service; manifest review (out of scope for this agent) needed to confirm `android:exported`.

**Deprecated API:** `IntentService` is deprecated as of Android API 30.

---

### TakePhotoPathPrefs.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.TakePhotoPathPrefs`
**Extends:** `Object` (no parent)

**SharedPreferences file name:** `"takephotoPrefs"`, mode `Context.MODE_PRIVATE`

**Keys:**
| Constant | Value |
|----------|-------|
| `KEY_0` | `"image0"` |
| `KEY_1` | `"image1"` |
| `KEY_2` | `"image2"` |
| `KEY_3` | `"image3"` |

**Public methods:**

| Method | Line |
|--------|------|
| `static saveObjectFromPosition(int position, String path)` | 26 |
| `static hasInvalidPhoto()` | 38 |
| `static getImagePathFromPosition(int position)` | 46 |
| `static clearImages()` | 53 |

**Data stored:** File-system paths to photo images (`image0`–`image3`). No PII, credentials, or tokens stored. The class stores file paths only, not the image binary data itself.

**Commit pattern:** Uses `commit()` (synchronous write) rather than `apply()` (asynchronous). This is a minor performance issue, not a security issue.

---

### UserInfoPrefs.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.UserInfoPrefs`
**Extends:** `au.com.collectiveintelligence.fleetiq360.model.ModelPrefs`

**Fields / constants:**
| Name | Value |
|------|-------|
| `TAG` | `"UserInfoPrefs"` |
| `USER_INFO_PREFS_KEY` | `"usr_info_key"` |

**SharedPreferences file name (own):** `"usrInfoPrefs"`, mode `Context.MODE_PRIVATE`

**Public methods:** None declared (inherits `ModelPrefs` static methods).

**Package-private methods:**
| Method | Line |
|--------|------|
| `static getUserInfoPrefs()` | 16 |

**SharedPreferences keys declared in this file:** `USER_INFO_PREFS_KEY = "usr_info_key"` (field exists but no read/write methods using it are implemented in this class — the key is unused within this file).

**Observation:** `UserInfoPrefs` is functionally a stub. It holds a preferences file accessor and one unused key constant. Actual user data storage in the inherited `ModelPrefs` class uses the shared `"prefs"` file. Through the inheritance chain, `ModelPrefs.saveObject(key, object)` serialises objects to JSON (via Gson) and writes to unencrypted SharedPreferences. `CurrentUser` uses `ModelPrefs` to store the OAuth token result (`token_result` key) and current user ID (`current_user_id` key). `UserDb` stores full user objects — including passwords — in a Realm database (not SharedPreferences).

---

## Findings by Checklist Section

### 1. Signing and Keystores
No keystore files, `storePassword`, or `keyPassword` values are present in the three assigned files. Signing configuration is not touched by these files.

No issues found in assigned files — Section 1.

---

### 2. Network Security

**CRITICAL — SSL/TLS certificate validation completely disabled**

File: `HttpClient.java` (read for context; called unconditionally from within the SyncService request path via `WebApi` and `HttpClient.addRequest()`)

`HttpClient.addRequest()` at line 122 calls `FakeX509TrustManager.allowAllSSL()` before every single network request — including those triggered by `SyncService`. `FakeX509TrustManager.allowAllSSL()` does two things:

1. Installs a global default `HostnameVerifier` that returns `true` for any hostname:
   ```java
   HttpsURLConnection.setDefaultHostnameVerifier(new HostnameVerifier() {
       @Override
       public boolean verify(String arg0, SSLSession arg1) {
           return true;
       }
   });
   ```
2. Installs a global default SSL socket factory backed by an `X509TrustManager` where both `checkClientTrusted` and `checkServerTrusted` are empty no-ops — accepting any certificate unconditionally:
   ```java
   @Override
   public void checkServerTrusted(X509Certificate[] x509Certificates, String s)
       throws CertificateException {
       // empty body — no validation performed
   }
   ```

This means every HTTPS request made by `SyncService` — syncing sessions, GPS locations, driver IDs, pre-start results — is fully susceptible to machine-in-the-middle attack. An attacker on the same network can intercept and modify all traffic. The `FakeX509TrustManager` is called via the static `allowAllSSL()` method which sets `HttpsURLConnection` global defaults, so the effect is process-wide, not limited to a single connection.

**Severity: Critical**

**File:** `FakeX509TrustManager.java` (lines 67–78), called from `HttpClient.java` line 122.

---

**CRITICAL — Hardcoded OAuth client credentials in source code**

File: `WebData.java`, method `getTokenFormData()` (lines 56–82):

```java
String clientId = "987654321";
String clientSecret = "8752361E593A573E86CA558FFD39E";
String userName = "gas";
String password = "ciiadmin";
```

These four values — `client_id`, `client_secret`, `username`, and `password` — are the credentials used to obtain the OAuth Bearer token that authenticates every API call made by `SyncService`. They are hardcoded as string literals in production source code and committed to version control. Any person with access to the repository or a decompiled APK can extract these credentials and make authenticated API calls directly to the `forkliftiqws` backend without possessing any legitimate account.

**Severity: Critical**

**File:** `WebData.java` lines 63–77.

---

**Hardcoded secondary base URL**

File: `URLBuilder.java`, line 26:

```java
final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora";
```

This URL is hardcoded for the `urlGetDiagnosis` and `urlGetUniversity` endpoints. It is HTTPS and does not appear to be a development/staging endpoint. This is a lower-severity concern (hardcoded production URL in code rather than build config) but is noteworthy. If this endpoint changes, a code change and app release is required.

**Severity: Low**

**File:** `URLBuilder.java` line 26.

---

**Commented-out local/development IP address**

File: `URLBuilder.java`, lines 171 and 355 (comments only):

```java
// Uri.Builder builder = Uri.parse("https://192.168.1.7/fleetiq360ws/rest").buildUpon();
```

The code is commented out and not active. However, it confirms that a local development server was used during development and that commented-out debug code remains in production source. Not a runtime risk, but indicates code hygiene gaps.

**Severity: Informational**

---

### 3. Data Storage

**HIGH — User passwords stored in plaintext in Realm database**

File: `UserRealmObject.java`, field `password` at line 15; written at line 36 in the constructor and read at line 56 in `makeUser()`. `UserDb.get(String email, String password)` (line 55–63) queries Realm directly on the `password` field to support offline login.

`CurrentUser.setTemporaryLoginInformation()` (line 122) stores an MD5 hash of the password:
```java
loginPassword = CommonFunc.MD5_Hash(password);
```

This MD5-hashed value is then passed to `UserDb` where it is stored in the Realm database under the `password` field and subsequently used for offline authentication. MD5 is a cryptographically broken hash function — it is not an acceptable password-hashing algorithm (no salt, trivially reversible via rainbow tables). The password stored in Realm is retrievable by any process that can access the Realm file, which on an unrooted device is the application itself, and on a rooted device or via ADB backup is any privileged attacker.

**Severity: High**

**Files:** `user/UserRealmObject.java` (field `password`, line 15), `user/UserDb.java` (line 59), `user/CurrentUser.java` (lines 90, 122).

---

**HIGH — OAuth Bearer token stored in unencrypted SharedPreferences**

File: `WebData.java`, `setGetTokenResult()` at line 92:
```java
ModelPrefs.saveObject(TOKEN_ITEM_KEY, result);
```

`ModelPrefs.saveObject()` serialises the `GetTokenResult` object to a JSON string via Gson and writes it to the `"prefs"` SharedPreferences file using standard (unencrypted) `SharedPreferences`. The token is read back at line 119:
```java
getTokenResult = (GetTokenResult) ModelPrefs.readObject(TOKEN_ITEM_KEY, GetTokenResult.class);
```

Bearer tokens are session credentials. Storing them in plaintext SharedPreferences means they can be extracted from a backup (if `android:allowBackup="true"`) or on a rooted device. `EncryptedSharedPreferences` from Jetpack Security should be used.

**Severity: High**

**Files:** `WebService/WebData.java` lines 92–119, `model/ModelPrefs.java` lines 53–64.

---

**MEDIUM — Photo file paths stored in unencrypted SharedPreferences (TakePhotoPathPrefs)**

File: `TakePhotoPathPrefs.java`. Keys `image0`–`image3` store absolute file-system paths to operator-taken photos in the `"takephotoPrefs"` SharedPreferences file. While file paths are not themselves sensitive PII, they reveal the structure of internal storage and the existence of photos, and could be used by a privileged attacker to locate and exfiltrate image files.

**Severity: Low / Informational** (paths only, not image data; mode is `MODE_PRIVATE`).

---

**MEDIUM — UserInfoPrefs stores nothing but inherits unencrypted storage**

`UserInfoPrefs` extends `ModelPrefs` and provides an accessor for a second SharedPreferences file (`"usrInfoPrefs"`). The constant `USER_INFO_PREFS_KEY = "usr_info_key"` is declared but unused within this file. The class appears incomplete or reserved. No active write of sensitive data was found in this file directly. However, the inherited `ModelPrefs` static methods write to a third, shared `"prefs"` file (not `"usrInfoPrefs"`), meaning any caller of `UserInfoPrefs.saveString(...)` etc. would inadvertently write to the generic `"prefs"` store rather than `"usrInfoPrefs"`.

No issues found specific to `UserInfoPrefs.java` beyond noting the unencrypted storage architecture inherited from `ModelPrefs`.

---

### 4. Input and Intent Handling

`SyncService` extends `IntentService` and is a background service. Exported status cannot be confirmed from source alone (requires manifest review, outside this agent's scope). The `startService()` static method creates an implicit `Intent` targeting `SyncService.class` by class reference — this is explicit intent usage, which is correct:
```java
new Intent(MyApplication.getContext(), SyncService.class)
```

The `onHandleIntent` method does not accept or process any external data from the `Intent` parameter. It operates entirely on local database state. No intent-borne data injection risk is present in the assigned files.

No issues found — Section 4 (assigned files scope).

---

### 5. Authentication and Session

**HIGH — MD5 used as password hashing — see Section 3 above**

**HIGH — Bearer token stored unencrypted — see Section 3 above**

**MEDIUM — No token expiry handling visible in SyncService**

`SyncService.onHandleIntent()` initialises `WebApi.sync()` once and then calls sync operations. When sync requests fail (`onFailed`), the service reschedules itself via `startService()` but does not attempt to re-authenticate or refresh the token. If the token has expired, subsequent sync attempts will silently fail and reschedule indefinitely. There is no observable token refresh or re-authentication path within `SyncService`.

**Severity: Medium**

**File:** `SyncService.java` lines 98–115 and 118–155.

**MEDIUM — Logout does not clear OAuth token**

`WebData.logout()` (line 108) calls `CurrentUser.logout()`, which calls `ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY)` and sets `user = null`. The OAuth Bearer token stored under key `TOKEN_ITEM_KEY` in `ModelPrefs` (`"prefs"` SharedPreferences) is **not** deleted on logout. A subsequent user picking up the device inherits a valid (until server-side expiry) Bearer token and could make authenticated API calls.

**Severity: Medium**

**Files:** `WebService/WebData.java` lines 108–110, `user/CurrentUser.java` lines 125–128, `WebService/WebData.java` lines 91–93.

---

### 6. Third-Party Libraries

The assigned files use:
- `com.android.volley` (Volley HTTP library) — used for async request queuing in `HttpClient`
- Realm (Java) — used in `UserDb` / `UserRealmObject`
- Android `IntentService` — deprecated

Specific library versions are not declared in the assigned files; they are in `build.gradle` (not assigned to this agent). No issues found within assigned files specifically.

**Deprecated API — IntentService**

`SyncService` extends `android.app.IntentService` (deprecated since Android API 30). The recommended replacement is `androidx.work.WorkManager`.

**Severity: Low**

**File:** `SyncService.java` line 22.

---

### 7. Google Play and Android Platform

**LOW — Deprecated IntentService**

As noted in Section 6: `SyncService extends IntentService` (line 22). `IntentService` was deprecated in API 30. Continued use triggers deprecation warnings and the class may be removed in future API levels.

**Severity: Low**

No other Android platform issues are determinable from the three assigned files alone.

---

## Summary of Findings

| ID | Severity | Section | Location | Title |
|----|----------|---------|----------|-------|
| F1 | Critical | 2 — Network Security | `HttpClient.java` line 122 / `FakeX509TrustManager.java` lines 67–78 | SSL/TLS certificate validation globally disabled — all HTTPS connections susceptible to MITM |
| F2 | Critical | 2 — Network Security | `WebData.java` lines 63–77 | Hardcoded OAuth client ID, client secret, username, and password in source code |
| F3 | High | 3 — Data Storage | `UserRealmObject.java` line 15; `CurrentUser.java` line 122 | User password stored as MD5 hash in plaintext Realm database — MD5 is not a password hash |
| F4 | High | 3 — Data Storage / 5 — Auth | `WebData.java` lines 92–119 | OAuth Bearer token stored in unencrypted SharedPreferences |
| F5 | Medium | 5 — Authentication | `WebData.java` lines 108–110 | Logout does not clear stored OAuth token from SharedPreferences |
| F6 | Medium | 5 — Authentication | `SyncService.java` lines 98–155 | No token refresh or re-authentication on sync failure; silent infinite retry loop |
| F7 | Low | 2 — Network Security | `URLBuilder.java` line 26 | Secondary base URL `pandora.fleetiq360.com` hardcoded in source rather than build config |
| F8 | Low | 6 — Libraries / 7 — Platform | `SyncService.java` line 22 | `IntentService` deprecated since API 30 |
| F9 | Informational | 2 — Network Security | `URLBuilder.java` lines 171, 355 | Commented-out local development IP address (`192.168.1.7`) remaining in production source |
| F10 | Informational | 3 — Data Storage | `TakePhotoPathPrefs.java` lines 14–57 | Photo file-system paths stored in plaintext SharedPreferences |
