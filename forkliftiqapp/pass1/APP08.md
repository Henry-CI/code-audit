# Pass 1 Security Audit — Agent APP08
**Date:** 2026-02-27
**Repo:** forkliftiqapp (Android/Java)
**Agent:** APP08
**Files reviewed:**
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebApi.java`
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebData.java`
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebListener.java`

---

## Step 1 — Branch Verification

**Result:** Branch is `master`.

**Discrepancy noted:** The checklist states `Branch: main`. The actual branch in this repository is `master`. Audit proceeds on `master` as instructed.

---

## Step 2 — Reading Evidence

### File 1: `WebApi.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.WebApi`

**Public fields / static fields:**
- None public. Private static field: `mContext` (Context) — line 19, annotated `@SuppressLint("StaticFieldLeak")`.

**Public methods (signature : line number):**
- `public static WebApi sync()` — line 23
- `public static WebApi async()` — line 31
- `public static void init(Context context)` — line 39
- `public void resendReport(int uid, int rid, WebListener<CommonResult> resultListener)` — line 47
- `public void saveShockEvent(SaveShockEventParameter parameter, WebListener<CommonResult> resultListener)` — line 51
- `public void updateUser(int uid, UpdateUserParameter parameter, WebListener<CommonResult> resultListener)` — line 55
- `public void addEquipment(AddEquipmentParameter parameter, WebListener<CommonResult> resultListener)` — line 59
- `public void getEmails(int uid, WebListener<GetEmailResult> resultListener)` — line 63
- `public void getReports(int uid, WebListener<ReportResultArray> resultListener)` — line 67
- `public void getEquipmentStats(int uid, int frequency, WebListener<EquipmentStatsResultArray> resultListener)` — line 71
- `public void getDriverStats(int uid, WebListener<GetDriverStatsResultArray> resultListener)` — line 84
- `public void saveService(WebServiceParameterPacket parameter, WebListener<WebServiceResultPacket> resultListener)` — line 88
- `public void getServiceRecord(int uid, WebListener<ServiceRecordResultArray> resultListener)` — line 92
- `void authApp(WebListener<GetTokenResult> resultListener)` — line 96 (package-private)
- `public void resetPassword(ResetPasswordParameter parameter, WebListener<WebServiceResultPacket> resultListener)` — line 112
- `public void login(LoginParameter parameter, WebListener<LoginResultArray> resultListener)` — line 131
- `public void register(UserRegisterParameter parameter, WebListener<LoginItem> resultListener)` — line 150
- `public void setupEmails(SetEmailsParameter parameter, WebListener<WebServiceResultPacket> resultListener)` — line 187
- `public void getEquipmentList(int userId, WebListener<GetEquipmentResultArray> resultListener)` — line 192
- `public void getPreStartQuestionList(int eid, WebListener<PreStartQuestionResultArray> resultListener)` — line 210
- `public void savePreStartResult(SavePreStartParameter parameter, WebListener<WebServiceResultPacket> resultListener)` — line 226
- `public void saveSessionStart(EquipmentItem equipmentItem, SessionStartParameter parameter, WebListener<SessionResult> resultListener)` — line 243
- `public void syncSaveSession(SaveSessionsParameter parameter, WebListener<SessionResult> resultListener)` — line 265
- `public void deleteSession(int sessionId, WebListener<WebServiceResultPacket> resultListener)` — line 269
- `public void saveSessionPreEnd(SessionResult sessionResult, SessionEndParameter parameter, WebListener<SessionEndResult> resultListener)` — line 286
- `public void saveSessionEnd(SessionResult sessionResult, SessionEndParameter parameter, WebListener<SessionEndResult> resultListener)` — line 300
- `public void getManufacture(WebListener<ManufactureResultArray> resultListener)` — line 321
- `public void getEquipmentType(int mid, WebListener<EquipmentTypeResultArray> resultListener)` — line 325
- `public void getFuelType(int mid, int etype, WebListener<FuelTypeResultArray> resultListener)` — line 329
- `public void saveLicense(SaveLicenseParameter parameter, WebListener<SaveLicenseResult> resultListener)` — line 333
- `public void saveImpact(ImpactParameter parameter, WebListener<SaveImpactResult> resultListener)` — line 337
- `public void saveSingleGPSLocation(SaveSingleGPSParameter parameter, WebListener<SaveSingleGPSResult> resultListener)` — line 341
- `public void saveMultipleGPSLocation(SaveMultipleGPSParameter parameter, WebListener<SaveMultipleGPSResult> resultListener)` — line 345

**API endpoint calls (via URLBuilder), all delegated through `GsonRequest` / `HttpClient`:**
- `URLBuilder.urlResendReport(uid, rid)` — GET
- `URLBuilder.urlSaveShockEvent()` — POST
- `URLBuilder.urlUpdateUser(uid)` — POST
- `URLBuilder.urlAddEquipment()` — POST
- `URLBuilder.urlGetEmails(uid)` — GET
- `URLBuilder.urlGetReports(uid)` — GET
- `URLBuilder.urlGetEquipmentStatsWeekly/Monthly/Yearly(uid)` — GET
- `URLBuilder.urlGetDriverStats(uid)` — GET
- `URLBuilder.urlSaveService()` — POST
- `URLBuilder.urlGetServiceRecord(uid)` — GET
- `URLBuilder.urlGetToken()` — POST (OAuth token endpoint)
- `URLBuilder.urlResetPassword()` — POST
- `URLBuilder.urlLogin()` — POST
- `URLBuilder.urlUserRegister()` — POST
- `URLBuilder.urlSetEmails()` — POST
- `URLBuilder.urlGetEquipmentList(userId)` — GET
- `URLBuilder.urlGetPreStartQuestions(eid)` — GET
- `URLBuilder.urlSavePreStartResult()` — POST
- `URLBuilder.urlSessionStart()` — POST
- `URLBuilder.urlSaveSession()` — POST
- `URLBuilder.urlAbortSession(sessionId)` — PUT
- `URLBuilder.urlSessionEnd()` — POST
- `URLBuilder.urlGetManufacture()` — GET
- `URLBuilder.urlGetEquipmentType(mid)` — GET
- `URLBuilder.urlGetFuelType(mid, etype)` — GET
- `URLBuilder.urlSaveLicense()` — POST
- `URLBuilder.urlSaveImpact()` — POST
- `URLBuilder.urlSaveSingleGPSLocation()` — POST
- `URLBuilder.urlSaveMultipleGPSLocation()` — POST

**Token / auth handling in WebApi.java:**
- `authApp()` (line 96) calls `URLBuilder.urlGetToken()` to obtain an OAuth Bearer token. On success it stores the token via `WebData.instance().setGetTokenResult(result)`.
- All subsequent API requests use Bearer token auth injected by `WebData.setHttpHeader()` or `WebData.setHttpHeaderForConnection()`.
- Three endpoints (`resetPassword`, `login`, `register`) gate on `WebData.instance().isAppInitialized()` and auto-invoke `authApp()` if not yet authenticated.

---

### File 2: `WebData.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.WebData`

**Public fields / constants:**
- None public. Package-private constants: `authHeaderType = "Authorization"` (line 22), `MAC_ADDRESS_LENGTH = 17` (line 23), `TOKEN_ITEM_KEY = "token_result"` (line 27).

**Public methods (signature : line number):**
- `public static int getTempSessionId()` — line 29
- `public static boolean isSessionOffline(int sessionId)` — line 40
- `public static SessionResult getTempSessionResult(SessionStartParameter parameter)` — line 46
- `public String getTokenFormData()` — line 56
- `public static WebData instance()` — line 84
- `public SessionResult getSessionResult()` — line 96
- `public void onSessionEnded()` — line 100
- `public static boolean isValidMacAddress(String address)` — line 104
- `public void logout()` — line 108
- `public int getUserId()` — line 112

**Package-private methods:**
- `void setGetTokenResult(GetTokenResult result)` — line 91
- `boolean isAppInitialized()` — line 124
- `void setHttpHeaderForConnection(HttpURLConnection connection)` — line 129
- `String getAuthHeader()` — line 134
- `void setHttpHeader(boolean authMessage, Map<String, String> header)` — line 138

---

### File 3: `WebListener.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.WebListener<T>`

**Public methods:**
- `public void onSucceed(T result)` — line 11 (empty default implementation)
- `public void onFailed(WebResult result)` — line 13 (empty default implementation)

No fields. Utility callback base class only.

---

### Ancillary file read for context: `URLBuilder.java`

**Key observations:**
- `baseUrl` — line 22: `BuildConfig.BASE_URL` (injected from build config, not hardcoded to a literal here).
- `baseDataUrl` — line 24: `baseUrl + "/rest"` (derives from `BuildConfig.BASE_URL`).
- `baseUrlForPreStartHelp` — line 26: **hardcoded literal** `"https://pandora.fleetiq360.com/pandora"`.
- Commented-out lines 171 and 355 contain a development LAN IP: `"https://192.168.1.7/fleetiq360ws/rest"` (commented, not active).

### Ancillary file read for context: `ModelPrefs.java`

- Uses plain (unencrypted) `SharedPreferences` for all persistence, including token objects serialised as JSON strings via Gson.

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No `.jks`, `.keystore`, or `.p12` files are present in these three source files. Signing config is not visible in these files.

No issues found in these files — Section 1.

---

### Section 2 — Network Security

**FINDING 2-A — Hardcoded secondary base URL (Medium)**

`URLBuilder.java` line 26:
```java
final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora";
```
This production hostname is hardcoded directly in source. It is used for `urlGetDiagnosis()` and `urlGetUniversity()`. Although the scheme is HTTPS and this is a production URL rather than a dev/staging endpoint, hardcoding a hostname in source means it cannot be changed without a full app release and it bypasses any build-flavour or environment-configuration mechanism. This is a low-to-medium concern for the same reason the primary `BASE_URL` was moved to `BuildConfig`: operational flexibility and separation of config from code.

**FINDING 2-B — Commented-out development IP address in production source (Low / Informational)**

`URLBuilder.java` lines 171 and 355 contain:
```java
// Uri.Builder builder = Uri.parse("https://192.168.1.7/fleetiq360ws/rest").buildUpon();
```
These are commented out and inactive. However, their presence confirms internal LAN topology details remain in source control. These should be removed.

**Primary base URL:** `BuildConfig.BASE_URL` — correctly injected from build config. Protocol cannot be confirmed as HTTPS from source alone; this must be verified in `build.gradle` `buildConfigField` declarations or `gradle.properties`.

No issues found regarding `TrustAllCertificates`, permissive `TrustManager`, or `hostnameVerifier` overrides — these three files contain no SSL customisation.

---

### Section 3 — Data Storage

**FINDING 3-A — OAuth token stored in plain (unencrypted) SharedPreferences (High)**

`WebData.java` line 93:
```java
ModelPrefs.saveObject(TOKEN_ITEM_KEY, result);
```
`ModelPrefs.saveObject()` serialises the `GetTokenResult` object as a plain JSON string and writes it to `SharedPreferences` at key `"token_result"` using `Context.MODE_PRIVATE`. This is standard (unencrypted) `SharedPreferences`.

On a rooted device or via ADB backup (if `android:allowBackup` is not disabled) the bearer token is fully recoverable in plaintext. The token grants access to all backend APIs including session management, GPS data, impact events, and operator credentials. This should use `EncryptedSharedPreferences` from Jetpack Security (`androidx.security:security-crypto`).

**FINDING 3-B — Static Context leak on Application class (Medium)**

`WebApi.java` line 18-19:
```java
@SuppressLint("StaticFieldLeak")
private static Context mContext;
```
A `Context` reference is held in a static field. The `@SuppressLint` annotation suppresses the IDE warning but does not fix the leak. If `mContext` is an Activity context this is a memory leak; if it is the Application context it is less severe but the suppression annotation is masking the issue rather than addressing it. The checklist notes that credentials cached in static fields on the Application class are a concern — this context reference is adjacent to that risk pattern.

---

### Section 4 — Input and Intent Handling

No WebView usage is present in these three files. No Intent construction or deep-link handling is present. No exported component declarations (those are in `AndroidManifest.xml`, not these files).

No issues found in these files — Section 4.

---

### Section 5 — Authentication and Session

**FINDING 5-A — Hardcoded OAuth client credentials in source code (Critical)**

`WebData.java` lines 63–77, method `getTokenFormData()`:
```java
String clientId = "987654321";
// ...
String clientSecret = "8752361E593A573E86CA558FFD39E";
// ...
String userName = "gas";
// ...
String password = "ciiadmin";
```
Four OAuth2 credential values — `client_id`, `client_secret`, `username`, and `password` — are hardcoded as string literals in source code. These are the credentials the app uses to obtain a Bearer token via the resource-owner password grant (`grant_type=password`).

Consequences:
1. Anyone who decompiles the APK (trivial with `apktool` + `jadx`) obtains all four values.
2. These values can be used outside the app to call the token endpoint directly and receive a valid Bearer token, bypassing all app-level controls.
3. The resource-owner password grant with a shared `username`/`password` (`gas` / `ciiadmin`) suggests a single shared application-level account — not per-user credentials. If that account's token is obtained by an attacker, all API endpoints are accessible.
4. Because these values are in version control history, they are permanently exposed even after remediation in code. The credentials must be rotated immediately on remediation.

This is the highest-severity finding in these files. The `client_secret`, `username`, and `password` must be removed from source, rotated at the server, and the token-acquisition flow must be rearchitected (e.g., client-credentials grant via a backend proxy so the shared secret never ships in the APK, or migration to OAuth PKCE for a public client).

**FINDING 5-B — Token persistence survives logout (Medium)**

`WebData.logout()` (line 108) calls only `CurrentUser.logout()`. It does not call `ModelPrefs.deleteDataForKey(TOKEN_ITEM_KEY)` or otherwise clear the OAuth token stored in SharedPreferences at key `"token_result"`. After logout the Bearer token remains persisted on-device and will be loaded again by `getTokenString()` on next app start (`isAppInitialized()` will return `true`). If the token has a long lifetime, a subsequent user of the same device (or an attacker with ADB access) can make authenticated API calls using the previous operator's token.

**FINDING 5-C — Deprecated AsyncTask import (Low)**

`WebApi.java` line 5:
```java
import android.os.AsyncTask;
```
`AsyncTask` is imported (though not directly called in this file — the `@SuppressLint("StaticFieldLeak")` annotation on line 18 and the import suggest it was previously used or is used in a related class). `AsyncTask` was deprecated in API level 30 (Android 11). Its presence in imports keeps a deprecated API in the compilation surface.

---

### Section 6 — Third-Party Libraries

These three files do not declare dependencies. Dependency review is out of scope for this file set.

No issues found in these files — Section 6.

---

### Section 7 — Google Play and Android Platform

**FINDING 7-A — Deprecated AsyncTask import (see 5-C above)**

`WebApi.java` line 5 imports `android.os.AsyncTask` which is deprecated from API 30. This is noted under Section 5-C as well.

No other platform / Play-specific issues are detectable from these three files alone.

---

## Summary Table

| ID | Severity | File | Line(s) | Description |
|----|----------|------|---------|-------------|
| 5-A | **Critical** | `WebData.java` | 63–77 | Hardcoded OAuth `client_id`, `client_secret`, `username`, `password` in source. Credentials must be rotated immediately. |
| 3-A | **High** | `WebData.java` | 93 | Bearer token stored in plain (unencrypted) SharedPreferences. Use `EncryptedSharedPreferences`. |
| 5-B | **Medium** | `WebData.java` | 108 | Logout does not clear persisted OAuth token from SharedPreferences. Token survives logout. |
| 3-B | **Medium** | `WebApi.java` | 18–19 | Static `Context` field with `@SuppressLint` suppressing the leak warning rather than fixing it. |
| 2-A | **Medium** | `URLBuilder.java` | 26 | Hardcoded secondary hostname `pandora.fleetiq360.com` bypasses build-flavour configuration. |
| 2-B | **Low** | `URLBuilder.java` | 171, 355 | Commented-out development LAN IP `192.168.1.7` exposes internal topology in version control. |
| 5-C / 7-A | **Low** | `WebApi.java` | 5 | Import of deprecated `android.os.AsyncTask` (deprecated API 30). |

---

## Notes on Scope

`URLBuilder.java` and `ModelPrefs.java` were read as supporting context because the assigned files directly call them and the checklist requires evaluation of base URL hardcoding and token storage mechanisms. Findings from those files are reported here because the root cause is visible in `WebData.java` and `WebApi.java` respectively.

The primary `BASE_URL` resolution via `BuildConfig.BASE_URL` in `URLBuilder.java` is the correct approach; the `pandora.fleetiq360.com` secondary URL should be treated consistently.

SSL/TLS configuration, certificate pinning, `TrustManager` customisation, and `HostnameVerifier` overrides are not present in these three files. Those checks require review of `HttpClient.java` and `GsonRequest.java`, which are not in this agent's assigned file set.
