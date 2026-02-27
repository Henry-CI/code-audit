# Pass 1 Security Audit — Agent APP51
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android / Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Confirmed on correct branch. Discrepancy noted: the checklist specifies `Branch: main`; the actual default branch is `master`. Audit continues.

---

## Step 2 — Checklist Reference

Checklist read in full: `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`
Sections: Signing and Keystores, Network Security, Data Storage, Input and Intent Handling, Authentication and Session, Third-Party Libraries, Google Play and Android Platform.

---

## Step 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/application/MyApplication.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/common/FleetActivity.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/common/FleetFragment.java`

Supporting files read for context (not assigned; evidence only):
- `user/CurrentUser.java`
- `WebService/WebApi.java`
- `model/ModelPrefs.java`
- `user/UserDb.java`

---

## Step 4 — Reading Evidence

### 4.1 MyApplication.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication`
**Extends:** `android.support.multidex.MultiDexApplication`

**Fields / constants:**
| Name | Type | Modifier | Line |
|---|---|---|---|
| `context` | `Context` | `private static` | 41 |
| `mHandler` | `Handler` | `private static` | 42 |
| `GPSParam` | `SaveSingleGPSParameter` | `private static` | 43 |
| `runnable` | `Runnable` | package-private | 45 |
| `locationService` | `ScheduledExecutorService` | `private static` | 46 |
| `networkConnected` | `boolean` | `private` | 75 |

**Public methods (signature → line):**
| Method | Line |
|---|---|
| `void onCreate()` | 49 |
| `static Handler getHandler()` | 112 |
| `static void runOnMainThread(Runnable runnable)` | 116 |
| `static void runLater(Runnable runnable, int time)` | 122 |
| `static void startLocationUpdate()` | 140 |
| `static void sendLocationUpdate()` | 195 |
| `static boolean getGPSProviderStatus()` | 190 |
| `static Context getContext()` | 213 |

**Private / package methods:**
- `initDataBase()` (line 65) — Realm initialisation
- `registerNetworkStatus()` (line 77)
- `onNetworkChanged()` (line 89)
- `onNetworkDisconnected()` (line 106)
- `onNetworkConnected()` (line 109)
- `static initImageLoader(Context)` (line 128)
- `static SaveUnitLocation()` (line 165)

**Imports of note:** `com.nostra13.universalimageloader.*`, `io.realm.Realm`, `io.realm.RealmConfiguration`

No import of `FakeX509TrustManager` or any custom `TrustManager` in this file.

---

### 4.2 FleetActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity`
**Extends:** `com.yy.libcommon.BaseActivity` (abstract class)

**Fields / constants:**
| Name | Type | Modifier | Line |
|---|---|---|---|
| `mLoadingView` | `View` | `private` | 59 |
| `connectingDevice` | `boolean` | `public` | 60 |
| `isDismissed` | `boolean` | `private` | 61 |
| `mLocation` | `LocationProvider` | package-private | 62 |
| `GPSParam` | `SaveSingleGPSParameter` | package-private | 63 |
| `runnable` | `Runnable` | package-private | 65 |
| `service` | `ScheduledExecutorService` | package-private | 66 |
| `broadcastReceiver` | `BroadcastReceiver` | `private` | 116 |
| `RECONNECT_REQUEST_ENABLE_BT` | `int` | `private` | 328 |
| `LOCATION_SETTINGS_REQUEST_GPS` | `int` | `public static` | 329 |

**Public methods (signature → line):**
| Method | Line |
|---|---|
| `void onCreate(Bundle savedInstanceState)` | 69 |
| `void showLoadingLayout()` | 84 |
| `void hideLoadingLayout()` | 90 |
| `void setContentView(int layoutId)` | 97 |
| `void onActivityResult(int, int, Intent)` | 331 |
| `void onResume()` | 441 |
| `void onPause()` | 454 |
| `static void abortSessionWithCallback(SessionResult, AbortSessionCallback)` | 418 |

**Inner class:** `AbortSessionCallback` (static, public) — lines 410–416

**Authentication gate on resume:** `SessionTimeouter.register(this)` called at line 450, and the BLE broadcast receiver is re-registered. No explicit credential/session-validity check is performed in `onResume()` itself; session management is delegated to `SessionTimeouter`.

---

### 4.3 FleetFragment.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.common.FleetFragment`
**Extends:** `com.yy.libcommon.BaseFragment`

**Public methods (signature → line):**
| Method | Line |
|---|---|
| `static void checkUsePreviousPreStart(BaseActivity, SessionResult, Runnable, Runnable)` | 65 |
| `void initBottomBar(int[], String[], View)` | 137 |
| `void onLeftButton(View view)` | 177 |
| `void onMiddleButton(View view)` | 181 |
| `void onRightButton(View view)` | 184 |
| `void showLoadingLayout()` | 187 |
| `void hideLoadingLayout()` | 194 |
| `void onActivityCreated(Bundle savedInstanceState)` | 202 |
| `void onRequestPermissionsResult(int, String[], int[])` | 265 |
| `void initViews()` | 282 |
| `void onSessionEnded()` | 285 |

**Protected methods:**
- `showPreStartOrJobFragment()` (line 39)
- `initChart()` (line 106)
- `initChartExtra(PieChart)` (line 127)

**Private methods:**
- `startConnect()` (line 213)
- `checkLocationPermission(Runnable)` (line 251)

**Field:**
- `runnableAfterPermission` (`Runnable`, private, line 263)

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

Not directly in scope for the three assigned files. No signing configuration, keystore references, or credential literals appear in `MyApplication.java`, `FleetActivity.java`, or `FleetFragment.java`.

No issues found — Section 1 (from assigned files).

---

### Section 2 — Network Security

**FINDING NET-01 — Severity: Medium**
**Realm database configured without encryption**

File: `MyApplication.java`, lines 65–73

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

The `RealmConfiguration.Builder` does not call `.encryptionKey(...)`. The Realm database (which, per `UserDb.java`, stores user records including `email` and `password` fields) is written to the device as a plain, unencrypted file. Any actor with physical access to the device or an ADB backup (if backups are enabled) can read the full Realm database.

**FINDING NET-02 — Severity: Informational**
**No FakeX509TrustManager in assigned files**

The checklist directive to check for `FakeX509TrustManager` usage in `MyApplication.java` was completed. No such import or instantiation is present in this file. The SSL/TLS configuration is handled in `HttpClient` (not an assigned file for this agent); no custom `TrustManager` exists within the three assigned files.

No other network security issues found in assigned files — Section 2.

---

### Section 3 — Data Storage

**FINDING DS-01 — Severity: High**
**Plaintext password stored as a static field in `CurrentUser` (referenced from assigned files)**

File: `user/CurrentUser.java`, lines 21–24 (read as supporting context)

```java
private static String loginEmail;
private static String loginPassword;
```

`MyApplication.java` calls `WebApi.init(context)` at line 55, which wires up the web service layer. `CurrentUser.setTemporaryLoginInformation(email, password)` (line 120 of `CurrentUser.java`) sets these static fields, and `CurrentUser.login()` (line 80) passes the password onwards. After successful login, `get().setPassword(loginPassword)` (line 90 of `CurrentUser.java`) re-stores the plaintext MD5-hashed password on the in-memory `User` object, which is then persisted to the unencrypted Realm database by `UserDb.save()`.

The password stored is the MD5 hash of the user's input, not the raw credential, but MD5 is a broken algorithm for credential storage and the hash is recoverable via rainbow tables. The hash is also stored persistently in the unencrypted Realm database (see NET-01 / DS-03 below), allowing offline brute-force.

**FINDING DS-02 — Severity: Medium**
**Plain `SharedPreferences` used for persistent session identity (no encryption)**

File: `model/ModelPrefs.java` (supporting context), used directly from `CurrentUser.java`

```java
static SharedPreferences getPref() {
    SharedPreferences prefs = MyApplication.getContext()
        .getSharedPreferences("prefs", Context.MODE_PRIVATE);
    return prefs;
}
```

`ModelPrefs` is called from `CurrentUser.setUser()` (line 34: `ModelPrefs.saveInt(CURRENT_USER_ID_KEY, user.getId())`) and `CurrentUser.logout()` (line 126: `ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY)`). This uses standard `SharedPreferences`, not `EncryptedSharedPreferences`. While only an integer user ID is stored here, the same `ModelPrefs` class exposes `saveString` and `saveObject` with no encryption wrapper, meaning any subsequent use for more sensitive values would be unprotected by design.

**FINDING DS-03 — Severity: High**
**User credentials (email + MD5 password) persisted in unencrypted Realm database**

File: `user/UserDb.java` (supporting context), `UserDb.get(String email, String password)` line 55

The offline login fallback in `CurrentUser.login()` queries Realm with `equalTo("email", email).equalTo("password", password)`, proving that both the email and MD5-hashed password are written to the Realm object and persisted on disk. Combined with the absence of Realm encryption (NET-01), these credentials are readable from the device storage without root on devices where ADB backup is enabled.

**FINDING DS-04 — Severity: Medium**
**`deleteRealmIfMigrationNeeded()` causes silent data loss on schema change**

File: `MyApplication.java`, line 71

```java
.deleteRealmIfMigrationNeeded()
```

This setting silently deletes all locally stored data (sessions, users, GPS records) when the schema version increments. For a shift-management app, a schema bump during a deployment could cause an operator's active session data, offline queued GPS points, and pre-start records to be irreversibly deleted before they are synced. This is a data-integrity concern with secondary security implications (audit log gaps).

**FINDING DS-05 — Severity: Low**
**Global static `Context` reference held in `MyApplication`**

File: `MyApplication.java`, line 41

```java
@SuppressLint("StaticFieldLeak")
private static Context context;
```

The suppression annotation acknowledges the lint warning. While the application context is generally safe to hold statically, the `@SuppressLint` indicates the developer bypassed the warning without documenting why. This is a maintenance risk; if the field is ever reassigned to an Activity context, it would produce a memory/context leak.

**FINDING DS-06 — Severity: Low**
**Static `GPSParam` field on `MyApplication` holds last GPS coordinates indefinitely**

File: `MyApplication.java`, line 43

```java
private static SaveSingleGPSParameter GPSParam;
```

`SaveUnitLocation()` (line 165) populates this static field with `unit_id`, `latitude`, `longitude`, and `gps_time`. The field is never nulled after a successful upload. After logout, this field continues to hold the last known GPS location and equipment ID of the previous operator's session in process memory.

No issues found beyond those above — Section 3.

---

### Section 4 — Input and Intent Handling

**FINDING II-01 — Severity: Low**
**`startActivityForResult` used (deprecated API)**

File: `FleetActivity.java`, line 302; `FleetFragment.java`, line 228

```java
// FleetActivity.java line 302
startActivityForResult(enableBtIntent, RECONNECT_REQUEST_ENABLE_BT);

// FleetFragment.java line 228
getActivity().startActivityForResult(enableGPS, LOCATION_SETTINGS_REQUEST_GPS);
```

`startActivityForResult` is deprecated as of Android API 30 in favour of the `ActivityResultLauncher` API. This is a platform-deprecation finding that does not present an immediate security risk, but is noted per checklist Section 7 and flagged here because both assigned files contain it.

**FINDING II-02 — Severity: Informational**
**BroadcastReceiver in `FleetActivity` filters on custom action strings; no validation of extras**

File: `FleetActivity.java`, lines 116–132

The `broadcastReceiver` responds to `ShockEventService.IMPACT` and `BleMachineService.ACTION_GATT_DISCONNECTED`. These are registered with `LocalBroadcastManager`, which scopes them to in-process messages only. This mitigates the risk of a malicious external app crafting a matching broadcast. No issues found for this specific pattern.

**FINDING II-03 — Severity: Low**
**Permission denial path in `FleetFragment` is silenced**

File: `FleetFragment.java`, lines 272–277

```java
} else {
    //permissionNotGranted = true;
    //onLocationNotGranted();
}
```

When `ACCESS_FINE_LOCATION` is denied by the user, the denial handler is entirely commented out. The app continues silently without location permission. Depending on downstream usage (e.g. GPS tracking of forklifts), this could cause silent functional failures or incorrect safety records, though it is not a direct security vulnerability.

No other input/intent handling issues — Section 4.

---

### Section 5 — Authentication and Session

**FINDING AS-01 — Severity: High**
**No authentication gate on `FleetActivity.onResume()`**

File: `FleetActivity.java`, lines 441–451

```java
@Override
protected void onResume() {
    super.onResume();
    if (ShockEventService.lastImpactEvent != null) showImpactAlert();
    IntentFilter intentFilter = new IntentFilter(ShockEventService.IMPACT);
    intentFilter.addAction(BleMachineService.ACTION_GATT_DISCONNECTED);
    LocalBroadcastManager.getInstance(this).registerReceiver(broadcastReceiver, intentFilter);
    SessionTimeouter.register(this);
}
```

Session validity on resume is delegated entirely to `SessionTimeouter.register(this)` (an external class not in scope for this agent). There is no direct check in `FleetActivity.onResume()` that a valid, authenticated session still exists before re-engaging operational UI. If `SessionTimeouter` fails silently or is misconfigured, a backgrounded activity could resume without re-validating the operator's session. This should be verified against `SessionTimeouter` in a subsequent pass.

**FINDING AS-02 — Severity: Medium**
**Logout does not clear Realm database or the static credential fields**

File: `user/CurrentUser.java` (supporting context), lines 125–128

```java
public static void logout() {
    ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY);
    user = null;
}
```

On logout, only the `current_user_id` SharedPreferences key is removed and the in-memory `user` reference is nulled. The static fields `loginEmail` and `loginPassword` are not cleared. The Realm database (which stores all user records including emails and MD5 passwords) is not cleared or re-keyed. An operator who logs out on a shared-device scenario (shift change) leaves their credentials retrievable from Realm and their email/password accessible via static fields until the process is killed.

This is directly relevant to the checklist item: "if the app supports multiple operators using the same device (shift changes), verify that one operator's data is fully cleared before another operator logs in."

**FINDING AS-03 — Severity: Medium**
**MD5 used for password hashing**

File: `user/CurrentUser.java` (supporting context), lines 82 and 122

```java
loginParameter.email = CommonFunc.MD5_Hash(loginEmail);   // line 82
loginPassword = CommonFunc.MD5_Hash(password);             // line 122
```

MD5 is a cryptographically broken hash function. It is not a password hashing algorithm (no salt, no work factor). The MD5 hash of the user password is transmitted to the server as the credential and is also stored persistently in the Realm database. An attacker who extracts the Realm file (possible without root if `allowBackup` is true) obtains MD5 hashes which are trivially reversible via precomputed tables.

**FINDING AS-04 — Severity: Informational**
**Pre-start bypass path exists for driver-based equipment**

File: `FleetFragment.java`, lines 77–80

```java
if (equipmentItem.driver_based) {
    runnableToJob.run();
    SessionDb.setSessionPreStartFinished(sessionResult.id, null, isSessionOffline);
    SessionDb.setSessionResultWithPreStartRequired(sessionResult, false);
}
```

When a piece of equipment is marked `driver_based`, the pre-start safety check is skipped entirely and a completed pre-start is recorded in the session database with a `null` parameter. This is noted as a business-logic concern: the server-side audit record will show a pre-start as completed when it was not performed. This may be intentional design, but it is flagged for review.

No other authentication/session issues found — Section 5.

---

### Section 6 — Third-Party Libraries

**FINDING LIB-01 — Severity: Medium**
**Universal Image Loader (UIL) — abandoned library**

File: `MyApplication.java`, lines 12–15, 128–136

```java
import com.nostra13.universalimageloader.cache.disc.naming.Md5FileNameGenerator;
import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;
import com.nostra13.universalimageloader.core.assist.QueueProcessingType;
```

Universal Image Loader has had no releases since 2016. The library is archived and receives no security updates. The checklist specifically calls this out. The disk cache is configured at 50 MB (`config.diskCacheSize(50 * 1024 * 1024)`). Images cached to disk may include operator profile photos or equipment images that remain accessible after logout.

**FINDING LIB-02 — Severity: Informational**
**`android.support.*` imports indicate legacy support library (not AndroidX)**

File: `MyApplication.java` (line 10), `FleetActivity.java` (lines 13–14), `FleetFragment.java` (implicit via `BaseFragment`)

```java
import android.support.multidex.MultiDexApplication;  // MyApplication.java:10
import android.support.v4.app.Fragment;               // FleetActivity.java:13
import android.support.v4.content.LocalBroadcastManager; // FleetActivity.java:14
```

The use of the legacy `android.support` library (rather than `androidx`) indicates the project has not migrated to AndroidX. Google ended active security patching of the legacy support library. This is a maintenance finding; migration to AndroidX is required to receive ongoing security fixes.

Library-specific CVE assessment for remaining dependencies (CircleImageView, ImagePicker, PercentProgress) is deferred to the agent assigned the Gradle build files.

---

### Section 7 — Google Play and Android Platform

**FINDING GP-01 — Severity: Medium**
**`AsyncTask` import present in `WebApi.java` (deprecated API 30)**

File: `WebApi.java` (supporting context), line 5

```java
import android.os.AsyncTask;
```

`AsyncTask` is deprecated since Android API 30 (Android 11). The import appears in `WebApi.java` though no direct instantiation was observed in the lines reviewed. This should be confirmed by the agent assigned `WebApi.java`. Flagged here because `MyApplication.java` calls `WebApi.init(context)` and `WebApi.async()` throughout.

**FINDING GP-02 — Severity: Low**
**`startActivityForResult` used in assigned files (deprecated)**

Already recorded under II-01. Cross-referenced here per Section 7: this affects `targetSdkVersion` compliance and will generate lint errors on API 30+.

**FINDING GP-03 — Severity: Informational**
**`ACCESS_FINE_LOCATION` runtime permission requested correctly**

File: `FleetFragment.java`, lines 251–261

```java
private void checkLocationPermission(Runnable runnable) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
        if (getBaseActivity().checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 300);
        } else {
            runnable.run();
        }
    } else {
        runnable.run();
    }
}
```

`ACCESS_FINE_LOCATION` is correctly requested at runtime for API 23+. However, denial handling is silenced (see II-03).

---

## Summary of Findings

| ID | Severity | Section | Description |
|---|---|---|---|
| DS-03 / NET-01 | High | Data Storage / Network | User credentials (email + MD5 password) stored in unencrypted Realm database |
| AS-01 | High | Authentication | No explicit session-validity check in `FleetActivity.onResume()` |
| DS-01 | High | Data Storage | Plaintext MD5 password held in static field `CurrentUser.loginPassword` |
| NET-01 | Medium | Network / Data Storage | Realm initialised without encryption key |
| DS-02 | Medium | Data Storage | Plain (unencrypted) `SharedPreferences` used for session persistence |
| AS-02 | Medium | Authentication | Logout does not clear Realm data or static credential fields |
| AS-03 | Medium | Authentication | MD5 used as password hash — cryptographically broken |
| LIB-01 | Medium | Libraries | Universal Image Loader is abandoned (no updates since 2016) |
| GP-01 | Medium | Platform | `AsyncTask` import in `WebApi.java` — deprecated API 30 |
| DS-04 | Medium | Data Storage | `deleteRealmIfMigrationNeeded()` causes silent data loss on schema bump |
| DS-05 | Low | Data Storage | Static `Context` field suppresses lint warning without justification |
| DS-06 | Low | Data Storage | Static `GPSParam` retains last GPS coordinates after logout |
| II-01 | Low | Intent Handling | `startActivityForResult` used — deprecated API 30 |
| II-03 | Low | Intent Handling | Location permission denial silently ignored |
| GP-02 | Low | Platform | `startActivityForResult` deprecated (cross-reference of II-01) |
| AS-04 | Info | Authentication | Pre-start bypassed for `driver_based` equipment; null recorded as completion |
| NET-02 | Info | Network | No `FakeX509TrustManager` found in assigned files |
| LIB-02 | Info | Libraries | Legacy `android.support` library used; not migrated to AndroidX |
| II-02 | Info | Intent Handling | LocalBroadcastManager scoping confirmed; no external interception risk |
| GP-03 | Info | Platform | `ACCESS_FINE_LOCATION` runtime request implemented correctly |
