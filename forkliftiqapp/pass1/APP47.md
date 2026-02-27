# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP47
**Date:** 2026-02-27
**Stack:** Android / Java
**Repository:** /c/Projects/cig-audit/repos/forkliftiqapp

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist states `Branch: main`. The actual default branch is `master`. Branch is confirmed as `master`; audit proceeds.

---

## Step 2 — Reading Evidence

### File 1: LoginActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.LoginActivity`

**Extends:** `FleetActivity` (which extends `BaseActivity`)

**Public methods:**

| Method | Line |
|--------|------|
| `protected void onCreate(Bundle savedInstanceState)` | 14 |

**Fields / constants:** None declared directly in this class.

**Manifest declaration (from AndroidManifest.xml, line 39–42):**
```xml
<activity
    android:name=".ui.activity.LoginActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"
    android:theme="@style/AppThemeClear"/>
```
No `android:exported` attribute. No `<intent-filter>`.

---

### File 2: ProfileActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.ProfileActivity`

**Extends:** `FleetActivity`

**Public methods:**

| Method | Line |
|--------|------|
| `protected void onCreate(Bundle savedInstanceState)` | 11 |

**Fields / constants:** None declared directly in this class.

**Manifest declaration (from AndroidManifest.xml, line 57–59):**
```xml
<activity
    android:name=".ui.activity.ProfileActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute. No `<intent-filter>`.

---

### File 3: SessionActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.SessionActivity`

**Extends:** `FleetActivity`

**Public methods:**

| Method | Line |
|--------|------|
| `protected void onCreate(Bundle savedInstanceState)` | 24 |
| `public void onBackPressed()` | 76 |
| `public void onExitSessionActivity()` | 90 |
| `public void abortSession(final SessionResult sessionResult)` | 118 |

**Fields / constants:** None declared directly; `connectingDevice` inherited from `FleetActivity` (line 134, 153).

**Manifest declaration (from AndroidManifest.xml, line 77–79):**
```xml
<activity
    android:name=".ui.activity.SessionActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute. No `<intent-filter>`.

---

### Supporting files read (evidence chain)

- `CurrentUser.java` — authentication logic, static credential fields, logout
- `User.java` — user model with `password` field
- `UserRealmObject.java` — Realm persistence model, stores `password` plaintext
- `UserDb.java` — Realm query layer, queries by `email`+`password` for offline login
- `ModelPrefs.java` — plain `SharedPreferences` wrapper ("prefs", `MODE_PRIVATE`)
- `WebData.java` — token storage, hardcoded API credentials, logout delegation
- `SessionDb.java` — session persistence in Realm
- `MyCommonValue.java` — static singleton holding `currentEquipmentItem`
- `FleetActivity.java` — base activity: BroadcastReceiver, BLE reconnect, session abort
- `CommonFunc.java` — MD5 and SHA-1 hashing utilities
- `LoginFragment.java` — login UI, calls `CurrentUser.setTemporaryLoginInformation`
- `LoginParameter.java` — login request DTO
- `AndroidManifest.xml` — permissions, components, `android:allowBackup`

---

## Step 3 — Findings by Checklist Section

---

### Section 1: Signing and Keystores

No `.jks`, `.keystore`, or `.p12` files were searched by this agent in this pass (out of assigned scope). No hardcoded signing credentials were observed in the assigned files.

**No issues found in assigned files — Section 1.**

---

### Section 2: Network Security

**FINDING 2-A — Severity: Critical**
**Hardcoded API client credentials in WebData.java**

File: `au/com/collectiveintelligence/fleetiq360/WebService/WebData.java`, lines 63–77

```java
String clientId = "987654321";
// ...
String clientSecret = "8752361E593A573E86CA558FFD39E";
// ...
String userName = "gas";
// ...
String password = "ciiadmin";
```

The `getTokenFormData()` method assembles an OAuth2 password-grant token request. The `client_id`, `client_secret`, `username`, and `password` are hardcoded as string literals in the source. These values will be present in compiled bytecode and are extractable by decompiling the APK without root access. Any party with access to the APK — including an end user or a malicious actor — can obtain these credentials and make authenticated API calls directly to the forkliftiqws backend without possessing an operator account. This credential pair is effectively permanently compromised from the moment the APK is distributed.

**FINDING 2-B — Severity: Medium**
**Token stored in plain SharedPreferences**

File: `WebData.java`, line 93:
```java
ModelPrefs.saveObject(TOKEN_ITEM_KEY, result);
```

`ModelPrefs` (line 17, `ModelPrefs.java`) writes to `SharedPreferences` using `Context.MODE_PRIVATE`:
```java
SharedPreferences prefs = MyApplication.getContext()
    .getSharedPreferences("prefs", Context.MODE_PRIVATE);
```

The OAuth2 bearer token is serialised as a JSON string and stored in the `prefs` shared preferences file under the key `"token_result"`. While `MODE_PRIVATE` prevents other apps from reading this file on non-rooted devices, the value is unencrypted on disk. On rooted devices or via ADB backup (see Section 3 finding), this token is recoverable as plaintext. Jetpack `EncryptedSharedPreferences` is the appropriate mitigation.

**No issues found in assigned files regarding cleartext HTTP or certificate validation overrides — Section 2 (those checks are in scope for other agents examining network configuration files).**

---

### Section 3: Data Storage

**FINDING 3-A — Severity: High**
**Operator password stored in plaintext in Realm database**

After successful authentication, `CurrentUser.login()` calls `get().setPassword(loginPassword)` (line 90, `CurrentUser.java`), which stores the MD5-hashed password on the `User` object in memory and then persists it via `UserDb.save()` → `UserRealmObject.setValues()` → Realm. The `password` field is written without encryption into the Realm database file on internal storage.

Evidence chain:
- `CurrentUser.java` line 90: `get().setPassword(loginPassword);`
- `User.java` lines 110–113: `void setPassword(String password) { this.password = password; UserDb.save(this); }`
- `UserRealmObject.java` line 15: `private String password;`
- `UserDb.java` lines 55–63: the offline fallback at `CurrentUser.java` line 103 queries Realm directly by `email` + `password` to re-authenticate: `realm.where(UserRealmObject.class).equalTo("email", email).equalTo("password", password).findFirst()`

The Realm database is not encrypted (no `RealmConfiguration` with an encryption key was observed in the assigned files). The password value stored is an MD5 hash. MD5 is a broken hashing algorithm — it is not a password hashing function and provides no meaningful protection against offline cracking. Rainbow tables for MD5 hashes of common passwords are freely available.

**FINDING 3-B — Severity: Medium**
**Credential hashing uses MD5 — not a password hashing function**

File: `CurrentUser.java` line 122:
```java
loginPassword = CommonFunc.MD5_Hash(password);
```

File: `CommonFunc.java` lines 68–83 confirm this is a plain MD5 digest with no salt.

The email field sent to the server is also MD5-hashed (line 82, `CurrentUser.java`):
```java
loginParameter.email = CommonFunc.MD5_Hash(loginEmail);
```

MD5 is cryptographically broken. It produces no salt, making all identical passwords produce identical hashes and making them vulnerable to precomputed rainbow-table attacks. The correct approach for password transmission is TLS (which protects in transit) combined with a server-side password hash using bcrypt, scrypt, or Argon2. The client-side MD5 pre-hash provides false assurance and does not replace a proper server-side key derivation function.

**FINDING 3-C — Severity: High**
**Static field retains credentials in memory for application lifetime**

File: `CurrentUser.java` lines 22–24:
```java
private static User user;
private static String loginEmail;
private static String loginPassword;
```

`loginEmail` and `loginPassword` are static fields on `CurrentUser`. `loginPassword` is set to the MD5-hashed password on each login attempt and is never explicitly cleared after authentication completes. `CurrentUser.logout()` (lines 125–128) clears `user` and removes the user-id preference key, but does not null out `loginEmail` or `loginPassword`:

```java
public static void logout() {
    ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY);
    user = null;
    // loginEmail and loginPassword are NOT cleared
}
```

These static fields survive for the lifetime of the process. On a multi-operator device (shift change), the previous operator's email and credential hash remain in memory when the next operator's login screen is shown. A memory dump or heap inspection on a rooted device would recover them.

**FINDING 3-D — Severity: High**
**`android:allowBackup="true"` — operator data extractable via ADB**

File: `AndroidManifest.xml` line 19:
```xml
android:allowBackup="true"
```

With ADB backup enabled, the entire application data directory — including the Realm database containing operator credentials, the `SharedPreferences` file containing the bearer token, and all session data — can be extracted by anyone with physical access to an unlocked Android device using:

```
adb backup -noapk au.com.collectiveintelligence.fleetiq360
```

This does not require root access. For a forklift management app processing operator identity, forklift telemetry, and workplace safety prestart data, this represents an unacceptable data exposure risk. The manifest attribute should be `android:allowBackup="false"`.

**FINDING 3-E — Severity: Medium**
**Static mutable field exposes equipment assignment data at application scope**

File: `MyCommonValue.java` lines 10–16:
```java
public static EquipmentItem currentEquipmentItem = null;
public static Boolean isCheckLocationPermissionDone = false;
public static String companyName = "";
public static String companyContract = "";
public static String companyRole = "";
public static String companyenabled = "";
```

`currentEquipmentItem` is a publicly mutable static field. It is assigned in `SessionActivity.onCreate()` (line 38) and `FleetActivity.reconnectEquipment()` (line 269) without synchronisation. On a shift-change, this field is not cleared in `CurrentUser.logout()`. A second operator logging in would initially see the previous operator's assigned equipment item until overwritten by the next session start.

---

### Section 4: Input and Intent Handling

**FINDING 4-A — Severity: Low / Informational**
**Activities declare no `android:exported` attribute — implicit default behaviour**

`LoginActivity` (line 39), `ProfileActivity` (line 57), and `SessionActivity` (line 77) in `AndroidManifest.xml` each omit the `android:exported` attribute. None of these activities has an `<intent-filter>`, so on Android API 31+ (target SDK verification is out of assigned scope) Android defaults `exported` to `false`. However, explicitly setting `android:exported="false"` is required by Google Play for apps targeting API 31+ and is a defence-in-depth best practice.

**No issues found in assigned files regarding WebView, deep links, or implicit intents carrying sensitive data — Section 4.**

---

### Section 5: Authentication and Session

**FINDING 5-A — Severity: High**
**Logout does not clear the bearer token from SharedPreferences**

`WebData.logout()` (line 108, `WebData.java`) delegates to `CurrentUser.logout()` (lines 125–128, `CurrentUser.java`), which only:
1. Deletes the `"current_user_id"` key from `SharedPreferences`.
2. Nulls the static `user` reference.

The bearer token stored under `"token_result"` in `SharedPreferences` (saved at `WebData.java` line 93) is **not** removed during logout. After logout, if a second operator on the same device inspects the device storage (rooted) or if the token is recovered via ADB backup, the previous operator's bearer token remains valid until server-side expiry.

The `LoginFragment.login()` method (line 73) calls `WebData.instance().logout()` before initiating a new login, but this does not erase the persisted token from the prefs file — it only affects the in-memory `user` reference.

**FINDING 5-B — Severity: Medium**
**No observed token expiry or refresh handling in assigned files**

The token obtained via `getTokenFormData()` (OAuth2 password grant) is stored and reused. No token expiry check, token refresh call, or re-authentication trigger was observed in the assigned files. If the token expires, the app's behaviour (silent failure vs. redirect to login) was not visible within the assigned file scope, but the absence of a refresh mechanism in the token storage path is a concern.

**FINDING 5-C — Severity: Medium**
**Operator Realm records are not cleared between operators on shift change**

`CurrentUser.logout()` does not purge the Realm `UserRealmObject` records for the previous operator. `UserDb.save()` persists every operator who has ever authenticated on the device. The offline fallback login at `CurrentUser.java` line 103 queries this accumulated Realm store by email+password. An operator who has previously used the device can re-authenticate offline without a network connection indefinitely, even after their account has been deactivated on the server — as long as their record remains in the local Realm database.

**FINDING 5-D — Severity: Low**
**Session exit on abort does not verify BLE disconnect before finishing**

In `SessionActivity.abortSession()` (line 118), the `abortSessionWithCallback` delegates to `FleetActivity.abortSessionWithCallback()` (line 418, `FleetActivity.java`), which calls `BleController.instance().stopConnection()`. The `finish()` call in `onSessionStopped()` (line 132, `SessionActivity.java`) is scheduled 800 ms after the abort callback fires:

```java
MyApplication.runLater(new Runnable() {
    @Override
    public void run() {
        hideProgress();
        finish();
        connectingDevice = false;
    }
}, 800);
```

The 800 ms fixed delay provides no guarantee that the BLE connection teardown has completed before the activity finishes. This is primarily a reliability concern but can contribute to orphaned BLE sessions persisting in device state.

---

### Section 6: Third-Party Libraries

Not in scope for assigned files. No findings raised from assigned files — Section 6.

---

### Section 7: Google Play and Android Platform

**FINDING 7-A — Severity: Medium**
**`startActivityForResult` used in FleetActivity — deprecated API**

File: `FleetActivity.java` line 302:
```java
startActivityForResult(enableBtIntent, RECONNECT_REQUEST_ENABLE_BT);
```

`startActivityForResult` is deprecated as of API 30. The `ActivityResultLauncher` / `ActivityResultContracts` API from `androidx.activity` is the current replacement.

**FINDING 7-B — Severity: Low**
**Support library imports instead of AndroidX**

Multiple assigned and supporting files import from `android.support.v4.*` rather than `androidx.*`:
- `SessionActivity.java` line 4: `import android.support.v4.app.Fragment;`
- `FleetActivity.java` lines 13–14: `import android.support.v4.app.Fragment; import android.support.v4.content.LocalBroadcastManager;`
- `LoginFragment.java` line 6: `import android.support.annotation.NonNull;`
- `UserDb.java` line 3: `import android.support.annotation.NonNull;`

The Android Support Library reached end-of-life in 2018 and is superseded by AndroidX. Support library components may not receive security fixes.

**No issues found in assigned files regarding permission usage — Section 7 (permissions are declared in AndroidManifest.xml and reviewed by the agent covering that file).**

---

## Summary of Findings

| ID | Section | Severity | Title |
|----|---------|----------|-------|
| 2-A | Network Security | **Critical** | Hardcoded API client credentials (client_id, client_secret, username, password) in WebData.java |
| 3-A | Data Storage | **High** | Operator password (MD5 hash) stored plaintext in unencrypted Realm database |
| 3-C | Data Storage | **High** | Static fields `loginEmail` and `loginPassword` not cleared on logout |
| 3-D | Data Storage | **High** | `android:allowBackup="true"` — full app data extractable via ADB without root |
| 5-A | Auth & Session | **High** | Logout does not remove bearer token from SharedPreferences |
| 2-B | Network Security | **Medium** | Bearer token stored in plain (unencrypted) SharedPreferences |
| 3-B | Data Storage | **Medium** | MD5 used for password hashing — not a password hashing function, no salt |
| 3-E | Data Storage | **Medium** | Static mutable equipment/company fields not cleared on logout |
| 5-B | Auth & Session | **Medium** | No token expiry or refresh mechanism observed |
| 5-C | Auth & Session | **Medium** | Realm user records accumulate across operators; offline login persists indefinitely |
| 7-A | Android Platform | **Medium** | `startActivityForResult` used — deprecated API 30+ |
| 4-A | Intent Handling | **Low** | `android:exported` not explicitly set on LoginActivity, ProfileActivity, SessionActivity |
| 5-D | Auth & Session | **Low** | Fixed 800 ms delay used for BLE disconnect timing on session abort |
| 7-B | Android Platform | **Low** | Support library (android.support.*) used instead of AndroidX |

---

*Report generated by Agent APP47. Pass 1 scope limited to assigned files and their direct dependencies required to evaluate the checklist sections.*
