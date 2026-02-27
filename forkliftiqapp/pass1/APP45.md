# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP45
**Date:** 2026-02-27
**Auditor:** Automated — Claude (claude-sonnet-4-6)
**Repo:** /c/Projects/cig-audit/repos/forkliftiqapp

---

## Branch Verification

- Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
- Result: `master`
- Checklist states "Branch: main" — **discrepancy recorded**. Actual branch is `master`, not `main`. Audit proceeds on `master`.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/DriverStatsActivity.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/DriversActivity.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/EquipmentActivity.java`

Supporting files read for context:
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/common/FleetActivity.java`
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/TakePhotoPathPrefs.java`
- `app/src/main/AndroidManifest.xml`
- `app/build.gradle`
- `build.gradle`
- `gradle.properties`
- `app/proguard-rules.pro`

---

## Reading Evidence

### File 1 — DriverStatsActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.DriverStatsActivity`

**Superclass:** `FleetActivity` (extends `BaseActivity` via `com.yy.libcommon.BaseActivity`)

**Fields/Constants declared in this file:** None.

**Public methods (this file only):**

| Method | Line |
|---|---|
| `protected void onCreate(Bundle savedInstanceState)` | 10 |

**AndroidManifest entry (from `app/src/main/AndroidManifest.xml`, line 65):**
```xml
<activity
    android:name=".ui.activity.DriverStatsActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute declared (omitted). On `targetSdkVersion` 26 this defaults to `false` (no `<intent-filter>` present), so the activity is not exported.

---

### File 2 — DriversActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.DriversActivity`

**Superclass:** `FleetActivity`

**Fields/Constants declared in this file:** None.

**Unused import noted:** `au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment` is imported but never referenced in this file (line 8).

**Public methods (this file only):**

| Method | Line |
|---|---|
| `protected void onCreate(Bundle savedInstanceState)` | 13 |

**AndroidManifest entry (line 85):**
```xml
<activity
    android:name=".ui.activity.DriversActivity"
    android:label="@string/title_activity_company_driver"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:theme="@style/AppThemeDark"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute; no `<intent-filter>`. Defaults to not exported on API 26.

---

### File 3 — EquipmentActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.EquipmentActivity`

**Superclass:** `FleetActivity`

**Imports:**
- `android.content.Intent` — imported but not directly used in this file
- `android.support.v4.app.Fragment` — imported but not directly used in this file
- `au.com.collectiveintelligence.fleetiq360.model.TakePhotoPathPrefs`

**Fields/Constants declared in this file:** None.

**Public methods (this file only):**

| Method | Line |
|---|---|
| `protected void onCreate(Bundle savedInstanceState)` | 15 |

**AndroidManifest entry (line 49):**
```xml
<activity
    android:name=".ui.activity.EquipmentActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute; no `<intent-filter>`. Defaults to not exported on API 26.

---

### FleetActivity.java — Base Class (Supporting Context)

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity`

**Superclass:** `com.yy.libcommon.BaseActivity`

**Fields declared:**

| Field | Modifier | Type | Line |
|---|---|---|---|
| `mLoadingView` | private | `View` | 59 |
| `connectingDevice` | public | `boolean` | 60 |
| `isDismissed` | private | `boolean` | 61 |
| `mLocation` | package-private | `LocationProvider` | 62 |
| `GPSParam` | package-private | `SaveSingleGPSParameter` | 63 |
| `runnable` | package-private | `Runnable` | 65 |
| `service` | package-private | `ScheduledExecutorService` | 66 |
| `broadcastReceiver` | private | `BroadcastReceiver` | 116 |
| `RECONNECT_REQUEST_ENABLE_BT` | private | `int` | 328 |
| `LOCATION_SETTINGS_REQUEST_GPS` | public static | `int` | 329 |

**Public methods:**

| Method | Line |
|---|---|
| `protected void onCreate(Bundle savedInstanceState)` | 69 |
| `public void showLoadingLayout()` | 84 |
| `public void hideLoadingLayout()` | 90 |
| `public void setContentView(int layoutId)` | 97 |
| `public void onActivityResult(int requestCode, int resultCode, Intent imageReturnedIntent)` | 331 |
| `public static class AbortSessionCallback` (inner) | 410 |
| `protected static void abortSessionWithCallback(...)` | 418 |
| `protected void onResume()` | 441 |
| `protected void onPause()` | 454 |

---

### TakePhotoPathPrefs.java — Supporting Context (Called from EquipmentActivity)

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.model.TakePhotoPathPrefs`

**Fields:**

| Field | Modifier | Type | Value |
|---|---|---|---|
| `KEY_0` | private static | `String` | `"image0"` |
| `KEY_1` | private static | `String` | `"image1"` |
| `KEY_2` | private static | `String` | `"image2"` |
| `KEY_3` | private static | `String` | `"image3"` |
| `keyArray` | private static | `String[]` | `{KEY_0, KEY_1, KEY_2, KEY_3}` |

**Public methods:**

| Method | Line |
|---|---|
| `static SharedPreferences getPref()` | 21 (package-private) |
| `public static void saveObjectFromPosition(int position, String path)` | 26 |
| `public static int hasInvalidPhoto()` | 38 |
| `public static String getImagePathFromPosition(int position)` | 46 |
| `public static void clearImages()` | 53 |

---

## Findings by Checklist Section

---

### Section 1 — Signing and Keystores

**Finding 1.1 — CRITICAL: Keystore files committed to version control**

Two JKS keystore files are present in the repository:
- `/c/Projects/cig-audit/repos/forkliftiqapp/app.jks`
- `/c/Projects/cig-audit/repos/forkliftiqapp/fleetiq.jks`

Neither `.jks` nor `*.keystore` patterns appear in `.gitignore`. Private signing keys committed to version control are permanently compromised; any party with access to the repository history can extract the private key used to sign all release, UAT, and dev builds.

**Finding 1.2 — CRITICAL: Keystore passwords hardcoded in gradle.properties (committed to version control)**

`gradle.properties` (committed; not in `.gitignore`) contains plaintext credentials for all three signing environments:

```
DEV_STORE_FILE=../fleetiq.jks
DEV_STORE_PASSWORD=ciadmin
DEV_KEY_ALIAS=fleetiq
DEV_KEY_PASSWORD=ciadmin

UAT_STORE_FILE=../fleetiq.jks
UAT_STORE_PASSWORD=ciadmin
UAT_KEY_ALIAS=fleetiq
UAT_KEY_PASSWORD=ciadmin

RELEASE_STORE_FILE=../fleetiq.jks
RELEASE_STORE_PASSWORD=ciadmin
RELEASE_KEY_ALIAS=fleetiq
RELEASE_KEY_PASSWORD=ciadmin
```

The password `ciadmin` is used for all environments — dev, UAT, and release — with the same keystore file (`fleetiq.jks`). This means all signed builds share an identical key pair protected by a trivially guessable password. `gradle.properties` is listed in `.gitignore` as `/local.properties`, not as `gradle.properties`, so it is tracked by git.

**Finding 1.3 — HIGH: No environment separation for signing keys**

All three environments (dev, UAT, release/prod) reference the same keystore file (`fleetiq.jks`) and the same key alias (`fleetiq`) with the same password. There is no separation between development and production signing credentials.

**Finding 1.4 — No Bitbucket Pipelines file found**

`bitbucket-pipelines.yml` is absent from the repository. Pipeline-specific checks are not applicable.

**Finding 1.5 — Note: minifyEnabled false for release builds**

In `app/build.gradle`, the release build type sets `minifyEnabled false`. While ProGuard files are referenced, minification and obfuscation are disabled for release builds (see also Section 6).

---

### Section 2 — Network Security

**Finding 2.1 — MEDIUM: No network_security_config.xml present**

No `network_security_config.xml` exists anywhere in the repository. The app relies entirely on Android platform defaults for certificate validation. Platform defaults for API 24+ trust only system CAs, which is acceptable. However, the absence of an explicit configuration means:
- There is no certificate pinning for the backend (forkliftiqws) endpoints.
- There is no documented intention to restrict allowed authorities.

This is a gap rather than an active misconfiguration, but is notable given the app transmits operator identity and equipment telemetry.

**Finding 2.2 — INFORMATIONAL: No usesCleartextTraffic flag in AndroidManifest.xml**

`android:usesCleartextTraffic` is not set in `AndroidManifest.xml`. On `targetSdkVersion` 26, the default permits cleartext for some APIs. The absence of `android:usesCleartextTraffic="false"` is not a misconfiguration at this API level but is worth noting.

**Finding 2.3 — MEDIUM: Hardcoded backend URLs in build.gradle productFlavors**

`app/build.gradle` embeds backend URLs directly in the build file for each product flavor:

```java
// dev flavor (line 74)
buildConfigField "String", "BASE_URL", '"https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws"'

// uat flavor (line 80)
buildConfigField "String", "BASE_URL", '"https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws"'

// prod flavor (line 86-87)
buildConfigField "String", "BASE_URL", '"https://pandora.fleetiq360.com/fleetiq360ws"'
```

The UAT URL (`ec2-54-86-82-22.compute-1.amazonaws.com`) is a raw AWS EC2 public DNS name, exposing the cloud provider and region. Infrastructure enumeration is trivially possible from the repository. These should be externalized to environment-specific configuration rather than committed source.

**Finding 2.4 — No direct SSL trust-override code observed in assigned files**

The three assigned Activity files (`DriverStatsActivity`, `DriversActivity`, `EquipmentActivity`) contain no HTTP client instantiation, no `TrustAllCertificates` patterns, and no `HostnameVerifier` overrides. This section is clear for the assigned files specifically.

---

### Section 3 — Data Storage

**Finding 3.1 — MEDIUM: android:allowBackup="true" in AndroidManifest.xml**

`AndroidManifest.xml` line 18:
```xml
android:allowBackup="true"
```

With ADB backup enabled, any user with USB debugging access can extract the app's data directory (`shared_prefs`, databases, files) without root. This app stores operator session data in Realm databases and SharedPreferences. The combination of `allowBackup="true"` with sensitive operational data constitutes a Medium risk.

**Finding 3.2 — MEDIUM: TakePhotoPathPrefs uses unencrypted SharedPreferences**

`TakePhotoPathPrefs.java` (called by `EquipmentActivity.onCreate()` via `TakePhotoPathPrefs.clearImages()`) stores image file paths in a plain `SharedPreferences` file (`"takephotoPrefs"`) using `Context.MODE_PRIVATE`. The file is not encrypted. File paths to equipment inspection photos are stored here. While the paths themselves are not operator credentials, they reveal where sensitive inspection images are stored on the device filesystem.

This class uses `MODE_PRIVATE` (correct — not world-readable), and stores only file paths (not photo content), which reduces severity. However, the use of plain `SharedPreferences` for any app data is a concern relative to the checklist requirement for `EncryptedSharedPreferences`.

**Finding 3.3 — No world-readable or world-writable file access in assigned files**

The three assigned Activity files contain no `openFileOutput()` calls. No `MODE_WORLD_READABLE` or `MODE_WORLD_WRITEABLE` usage observed in the assigned files.

**Finding 3.4 — No external storage writes in assigned files**

No calls to `Environment.getExternalStorageDirectory()` or equivalent are present in the three assigned Activity files.

---

### Section 4 — Input and Intent Handling

**Finding 4.1 — No android:exported="true" on assigned activities**

All three assigned activities (`DriverStatsActivity`, `DriversActivity`, `EquipmentActivity`) are declared in `AndroidManifest.xml` without `android:exported="true"` and without any `<intent-filter>`. At `targetSdkVersion` 26, these activities default to not exported and cannot be invoked by external applications.

**Finding 4.2 — No implicit intents carrying sensitive data in assigned files**

The three assigned Activity files do not construct or dispatch any `Intent` objects. No sensitive data is carried in intents within these files.

**Finding 4.3 — No WebView usage in assigned files**

No WebView instantiation, `setJavaScriptEnabled`, `setAllowFileAccess`, or URL loading is present in the three assigned Activity files.

**Finding 4.4 — No deep link handlers on assigned activities**

None of the three assigned activities declare an `<intent-filter>` with a custom scheme in `AndroidManifest.xml`. No deep link attack surface from these activities.

**Finding 4.5 — DEPRECATED: startActivityForResult used in FleetActivity (base class)**

`FleetActivity.java` line 302:
```java
startActivityForResult(enableBtIntent, RECONNECT_REQUEST_ENABLE_BT);
```
`startActivityForResult` is deprecated as of `androidx.activity` 1.2.0 / Android API 30. The assigned activities inherit this behavior through `FleetActivity`. This is a code quality / platform deprecation concern rather than a direct security vulnerability.

**Finding 4.6 — Unused import in DriversActivity.java**

`DriversActivity.java` line 8 imports `EquipmentListFragment` but never uses it. This is dead code rather than a security concern, but is noted.

---

### Section 5 — Authentication and Session

**Finding 5.1 — No authentication logic in the three assigned Activity files**

`DriverStatsActivity`, `DriversActivity`, and `EquipmentActivity` each contain only a single `onCreate` method that sets a content view and initiates a Fragment. No credential handling, token storage, login logic, or session management is present in these three files directly.

**Finding 5.2 — Authentication and session security deferred to FleetActivity and supporting classes**

All session-related logic (session timeout via `SessionTimeouter`, session end via `WebApi`, BLE reconnect, GPS location) is in the `FleetActivity` base class and its collaborators. These are outside the assigned file scope but are the effective security surface for these three activities.

No issues found specific to authentication in the three assigned files — the assigned files themselves are thin wrappers delegating entirely to FleetActivity and the loaded Fragments.

---

### Section 6 — Third-Party Libraries

**Finding 6.1 — CRITICAL: minifyEnabled false for release builds**

`app/build.gradle` line 52:
```groovy
release {
    minifyEnabled false
    proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
    signingConfig signingConfigs.release
}
```
Code minification and obfuscation are disabled for release builds despite ProGuard files being configured. Release APKs are fully readable with standard decompilation tools. Class names, method names, and field names — including those referencing authentication, session management, and backend communication — are fully exposed.

**Finding 6.2 — HIGH: Severely outdated Android Support Library**

`app/build.gradle` declares:
```groovy
implementation 'com.android.support:appcompat-v7:26.0.2'
implementation 'com.android.support:recyclerview-v7:26.0.2'
implementation 'com.android.support:support-v4:26.0.2'
implementation 'com.android.support:multidex:1.0.2'
implementation 'com.android.support:cardview-v7:26.0.2'
```
The `com.android.support` namespace was superseded by AndroidX in 2018 (Google I/O). Version `26.0.2` dates to 2017. These libraries no longer receive security updates. The project should be migrated to AndroidX equivalents. The assigned files (`DriverStatsActivity`, `DriversActivity`, `EquipmentActivity`) all inherit from this dependency chain through `FleetActivity`.

`EquipmentActivity.java` line 5 imports:
```java
import android.support.v4.app.Fragment;
```
This confirms active use of the legacy support library namespace.

**Finding 6.3 — HIGH: Multiple severely outdated dependencies**

From `app/build.gradle`:

| Dependency | Version in Repo | Status |
|---|---|---|
| `com.android.support:appcompat-v7` | 26.0.2 (2017) | Superseded by AndroidX; no security updates |
| `com.android.support:recyclerview-v7` | 26.0.2 (2017) | Superseded by AndroidX; no security updates |
| `com.android.support:support-v4` | 26.0.2 (2017) | Superseded by AndroidX; no security updates |
| `com.android.support:cardview-v7` | 26.0.2 (2017) | Superseded by AndroidX; no security updates |
| `com.android.support:multidex` | 1.0.2 (2017) | Superseded by AndroidX; no security updates |
| `com.android.volley:volley` | 1.1.1 (2018) | Latest is 1.2.1 (2021); SSRF and request-smuggling fixes in subsequent versions |
| `com.squareup.retrofit2:retrofit` | 2.5.0 (2019) | Current is 2.11.0 (2024) |
| `com.squareup.retrofit2:converter-gson` | 2.5.0 (2019) | Current is 2.11.0 (2024) |
| `com.google.code.gson:gson` | 2.8.5 (2018) | CVE-2022-25647 (Deserialization of Untrusted Data, CVSS 7.5) — fixed in 2.8.9 |
| `com.google.android.gms:play-services-location` | 11.8.0 (2017) | Current is 21.x; major API and security changes since 11.x |
| `com.github.PhilJay:MPAndroidChart` | v3.0.2 (2018) | Current is 3.1.0; charting library, low direct security risk |
| `io.realm:realm-gradle-plugin` | 3.7.2 (2017) | Current is 10.x; major versions behind |
| `com.android.tools.build:gradle` | 3.0.0 (2017) | Current is 8.x; significant build security improvements since 3.x |

**CVE specifically noted:** `com.google.code.gson:gson:2.8.5` — CVE-2022-25647 (ReDoS / deserialization vulnerability, CVSS 7.5). This library is used for JSON deserialization of backend responses from forkliftiqws.

**Finding 6.4 — Internal library modules use embedded/vendored code**

The repo contains vendored library modules (`LibCircleImageView`, `LibImagePicker`, `LibImageloader`, `LibPercentProgress`). These are listed in the checklist as known inclusions. Version and CVE status of these vendored libraries depends on when they were copied into the repository, which cannot be determined from source alone without commit history analysis.

---

### Section 7 — Google Play and Android Platform

**Finding 7.1 — CRITICAL: targetSdkVersion 26 — does not meet Google Play requirements**

`build.gradle` (root):
```groovy
myTargetSdkVersion=26
myMinSdkVersion=21
myCompileSdkVersion=26
```

Google Play requires `targetSdkVersion` 34 or higher for all new app updates (as of August 2023). `targetSdkVersion` 26 (Android 8.0, 2017) is significantly below this requirement. An app targeting API 26:
- Does not receive Android 8.1+ security behavioral improvements.
- Is exempt from foreground service restrictions introduced in API 28.
- Is exempt from scoped storage restrictions introduced in API 29.
- Is exempt from package visibility restrictions introduced in API 30.
- Does not enforce `android:exported` declaration requirements mandated from API 31.
- Cannot be published as a new update to Google Play in its current state.

**Finding 7.2 — HIGH: Declared permissions without confirmed usage scope in assigned files**

`AndroidManifest.xml` declares the following dangerous permissions:

| Permission | Dangerous | Noted Usage |
|---|---|---|
| `READ_EXTERNAL_STORAGE` | Yes (API 16+) | Image picker / photo capture |
| `WRITE_EXTERNAL_STORAGE` | Yes (API 16+) | Image picker / photo capture |
| `CAMERA` | Yes | Photo capture for equipment inspection |
| `ACCESS_FINE_LOCATION` | Yes | GPS for forklift telemetry |
| `BLUETOOTH` | Standard (elevated API 31+) | BLE device connection |
| `BLUETOOTH_ADMIN` | Standard (elevated API 31+) | BLE scanning |

Runtime permission request handling for `CAMERA`, `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`, and `ACCESS_FINE_LOCATION` is not present in the three assigned Activity files. Runtime permission handling is expected to reside in fragments or in the base class. This is noted for completeness; the assigned files do not themselves invoke these permission-requiring APIs.

**Finding 7.3 — MEDIUM: BLUETOOTH and BLUETOOTH_ADMIN permissions not modernized for API 31+**

For apps targeting API 31+, `BLUETOOTH` and `BLUETOOTH_ADMIN` are replaced by `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, and `BLUETOOTH_ADVERTISE`. At `targetSdkVersion` 26 this is currently not an enforcement issue, but is a blocker to any future `targetSdkVersion` upgrade.

**Finding 7.4 — DEPRECATED: startActivityForResult in FleetActivity (inherited by all assigned activities)**

`FleetActivity` line 302 uses `startActivityForResult(enableBtIntent, RECONNECT_REQUEST_ENABLE_BT)`. This is deprecated in modern `androidx.activity`. All three assigned activities inherit this through `FleetActivity`. Modernization requires migrating to `ActivityResultLauncher`.

**Finding 7.5 — No LAUNCHER activity ambiguity — assigned activities are not entry points**

The LAUNCHER `<intent-filter>` in `AndroidManifest.xml` is attached to `.autoupdate.activity.ShowPackageAvailable` (lines 91-97), not to any of the three assigned activities. The three assigned activities are internal navigation screens, confirming they are not external entry points.

---

## Summary of Findings

| ID | Severity | Section | Description |
|---|---|---|---|
| 1.1 | CRITICAL | Signing | Two `.jks` keystore files committed to version control (`app.jks`, `fleetiq.jks`) |
| 1.2 | CRITICAL | Signing | All signing passwords plaintext in `gradle.properties` (committed, not gitignored); password is `ciadmin` for all environments |
| 1.3 | HIGH | Signing | Same keystore and key used for dev, UAT, and release — no environment separation |
| 2.1 | MEDIUM | Network | No `network_security_config.xml`; no certificate pinning for forkliftiqws |
| 2.3 | MEDIUM | Network | Hardcoded backend URLs in `build.gradle` including raw AWS EC2 public DNS for UAT |
| 3.1 | MEDIUM | Storage | `android:allowBackup="true"` permits ADB extraction of app data without root |
| 3.2 | MEDIUM | Storage | `TakePhotoPathPrefs` stores file paths in unencrypted `SharedPreferences` |
| 6.1 | CRITICAL | Libraries | `minifyEnabled false` for release — release APKs are fully unobfuscated |
| 6.2 | HIGH | Libraries | All `com.android.support` libraries at version 26.0.2 (2017) — no security updates since 2018 migration to AndroidX |
| 6.3 | HIGH | Libraries | `gson:2.8.5` affected by CVE-2022-25647 (CVSS 7.5); multiple other dependencies severely out of date |
| 7.1 | CRITICAL | Platform | `targetSdkVersion 26` — fails Google Play requirement (34+); bypasses 7 years of Android security restrictions |
| 7.4 | LOW | Platform | `startActivityForResult` deprecated (inherited by all three assigned activities via `FleetActivity`) |

**No issues found — Section 4 (Input and Intent Handling) for the three assigned files specifically.** All three activities are not exported, contain no WebView usage, dispatch no implicit intents, and declare no deep link handlers.

**No issues found — Section 5 (Authentication and Session) for the three assigned files specifically.** The assigned Activity files contain no credential handling or session token logic; these concerns exist in the base class and fragment layer which are outside this assignment scope.

---

## Notes on Assigned File Scope

All three assigned Activity files (`DriverStatsActivity`, `DriversActivity`, `EquipmentActivity`) are minimal thin wrappers. Each contains only a single overridden `onCreate` method that:
1. Sets a content view layout.
2. Loads a Fragment into a container.

`EquipmentActivity` additionally calls `TakePhotoPathPrefs.clearImages()` on startup, clearing previously stored image file paths from SharedPreferences (a defensive hygiene action, though using unencrypted SharedPreferences).

The majority of significant security findings in this report originate from supporting infrastructure files (build configuration, manifest, base class) that were read to provide complete context per checklist requirements. The assigned Activity files themselves introduce no independent security vulnerabilities beyond what they inherit from the project's build and platform configuration.
