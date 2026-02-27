# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** CFG
**Date:** 2026-02-27
**Stack:** Android/Java
**Audit pass:** CFG (Build Configuration, Signing, Manifests, Dependencies)

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Output: `master`

**Discrepancy noted:** The checklist header states `Branch: main`. The actual branch is `master`. Branch verification passed on `master`.

---

## Files Assigned and Read

1. `/c/Projects/cig-audit/repos/forkliftiqapp/.gitignore`
2. `/c/Projects/cig-audit/repos/forkliftiqapp/build.gradle`
3. `/c/Projects/cig-audit/repos/forkliftiqapp/gradle.properties`
4. `/c/Projects/cig-audit/repos/forkliftiqapp/gradle/wrapper/gradle-wrapper.properties`
5. `/c/Projects/cig-audit/repos/forkliftiqapp/gradlew`
6. `/c/Projects/cig-audit/repos/forkliftiqapp/gradlew.bat`
7. `/c/Projects/cig-audit/repos/forkliftiqapp/settings.gradle`
8. `/c/Projects/cig-audit/repos/forkliftiqapp/app/.gitignore`
9. `/c/Projects/cig-audit/repos/forkliftiqapp/app/build.gradle`
10. `/c/Projects/cig-audit/repos/forkliftiqapp/app/proguard-rules.pro`
11. `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/.gitignore`
12. `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/build.gradle`
13. `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/proguard-rules.pro`
14. `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
15. `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/AndroidManifest.xml`

Additional files discovered and checked:
- `/c/Projects/cig-audit/repos/forkliftiqapp/app.jks` (git-tracked keystore)
- `/c/Projects/cig-audit/repos/forkliftiqapp/fleetiq.jks` (git-tracked keystore)

---

## Reading Evidence

### `/c/Projects/cig-audit/repos/forkliftiqapp/.gitignore` (root)

Rules listed:
```
*.iml
.gradle
/local.properties
/.idea/workspace.xml
/.idea/libraries
.DS_Store
/build
/captures
.idea
*/build
```

Notably absent: no rule excluding `*.jks`, `*.keystore`, `*.p12`, `gradle.properties`, or `keystore.properties`.

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/build.gradle` (root)

Plugins applied:
- `com.android.tools.build:gradle:3.0.0` (buildscript classpath)
- `io.realm:realm-gradle-plugin:3.7.2` (buildscript classpath)

Repositories: `google()`, `jcenter()`, `https://jitpack.io`

Project-wide ext properties:
```
myBuildToolsVersion = "26.0.2"
myTargetSdkVersion  = 26
myMinSdkVersion     = 21
myCompileSdkVersion = 26
```

No signingConfigs block in root build.gradle.

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/gradle.properties`

Full content (secrets present):
```
org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

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

`gradle.properties` is NOT listed in the root `.gitignore`. This file — containing all keystore passwords — is committed to version control.

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/gradle/wrapper/gradle-wrapper.properties`

```
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-4.1-all.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

Gradle wrapper version: 4.1 (released 2017). No checksum verification configured (`distributionSha256Sum` absent).

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/gradlew` and `gradlew.bat`

Standard Gradle wrapper bootstrap scripts. No modifications. No embedded secrets.

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/settings.gradle`

Modules included:
```
':app', ':LibCommon', ':LibImageloader', ':LibImagePicker', ':LibCircleImageView', ':LibPercentProgress'
```

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/app/.gitignore`

Rules:
```
/build
```

No exclusion of keystore files or sensitive properties.

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/app/build.gradle`

Plugins applied:
- `com.android.application`
- `realm-android`

signingConfigs block:

| Config   | storeFile        | storePassword | keyAlias | keyPassword | v2SigningEnabled |
|----------|------------------|---------------|----------|-------------|-----------------|
| dev      | `../fleetiq.jks` | `ciadmin`     | `fleetiq`| `ciadmin`   | false           |
| uat      | `../fleetiq.jks` | `ciadmin`     | `fleetiq`| `ciadmin`   | false           |
| release  | `../fleetiq.jks` | `ciadmin`     | `fleetiq`| `ciadmin`   | false           |

Values sourced from `gradle.properties` variables (`DEV_STORE_PASSWORD`, etc.) which are committed to version control.

SDK versions (from root ext):
- `compileSdkVersion`: 26
- `targetSdkVersion`: 26
- `minSdkVersion`: 21

`minifyEnabled false` for release build type.
`multiDexEnabled true`

Product flavors and hardcoded BASE_URL values:

| Flavor | BASE_URL |
|--------|----------|
| local  | `https://<localHost.hostAddress>:8443/fleetiq360ws` (dynamic) |
| dev    | `https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws` |
| uat    | `https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws` |
| prod   | `https://pandora.fleetiq360.com/fleetiq360ws` |

Dependencies (app/build.gradle):
```
implementation project(':LibCommon')
implementation project(':LibImageloader')
implementation project(':LibImagePicker')
implementation project(':LibCircleImageView')
implementation 'info.hoang8f:android-segmented:1.0.6'
implementation 'com.github.PhilJay:MPAndroidChart:v3.0.2'
implementation 'com.android.volley:volley:1.1.1'
implementation 'joda-time:joda-time:2.10'
implementation 'com.squareup.retrofit2:retrofit:2.5.0'
implementation 'com.google.code.gson:gson:2.8.5'
implementation 'com.squareup.retrofit2:converter-gson:2.5.0'
testImplementation 'junit:junit:4.12'
implementation 'com.android.support:appcompat-v7:26.0.2'
implementation 'com.android.support:recyclerview-v7:26.0.2'
implementation 'com.android.support:support-v4:26.0.2'
implementation 'com.android.support:multidex:1.0.2'
implementation 'com.android.support:cardview-v7:26.0.2'
implementation 'com.google.android.gms:play-services-location:11.8.0'
```

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/app/proguard-rules.pro`

No active `-keep` rules. All rules are commented out. File is effectively empty.

Comment reference to developer local path: `D:\d_before_20150611\adt-bundle-windows-x86-20130522\sdk/tools/proguard/proguard-android.txt` — a personal machine path from approximately 2013–2015.

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/.gitignore`

Rules:
```
/build
```

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/build.gradle`

Plugins applied:
- `com.android.library`

`lintOptions { abortOnError false }` — lint errors suppressed.

`minifyEnabled false` for release build type.

Dependencies:
```
implementation 'com.google.code.gson:gson:2.8.5'
implementation 'com.android.support:appcompat-v7:26.0.2'
implementation 'com.android.support:design:26.0.2'
implementation project(path: ':LibPercentProgress')
```

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/proguard-rules.pro`

No active `-keep` rules. All rules are commented out. File is effectively empty.

Comment reference to developer local path: `/Users/steveyang/Library/Android/sdk/tools/proguard/proguard-android.txt` — personal machine path of a developer named "steveyang".

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`

Package: `au.com.collectiveintelligence.fleetiq360`

Permissions declared:
```
android.permission.INTERNET
android.permission.ACCESS_WIFI_STATE
android.permission.ACCESS_NETWORK_STATE
android.permission.READ_EXTERNAL_STORAGE
android.permission.WRITE_EXTERNAL_STORAGE
android.permission.CAMERA
android.permission.BLUETOOTH
android.permission.BLUETOOTH_ADMIN
android.permission.ACCESS_FINE_LOCATION
```

Uses-feature: `android.hardware.bluetooth_le` (required=true)

Application attributes:
- `android:allowBackup="true"`
- `android:largeHeap="true"`
- No `android:usesCleartextTraffic` attribute (defaults to platform behavior)
- No `android:networkSecurityConfig` reference

Components:

| Component | Class | exported | Notes |
|-----------|-------|----------|-------|
| Provider | `android.support.v4.content.FileProvider` | `false` | grantUriPermissions=true |
| Activity | `.ui.activity.ActionClearActivity` | not set | No intent-filter; implicitly not exported (API <31 default) |
| Activity | `.ui.activity.LoginActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.DashboardActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.EquipmentActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.JobsActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.ProfileActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.IncidentActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.DriverStatsActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.EquipmentStatsActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.ActionActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.SessionActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `com.yy.libcommon.WebActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.ui.activity.DriversActivity` | not set | No intent-filter; implicitly not exported |
| Activity | `.autoupdate.activity.ShowPackageAvailable` | not set | Has MAIN/LAUNCHER intent-filter — effectively exported (launcher entry point) |
| Service | `.WebService.BLE.BleMachineService` | not set | No intent-filter; implicitly not exported |
| Service | `.WebService.BLE.ShockEventService` | not set | No intent-filter; implicitly not exported |
| Service | `.model.SyncService` | not set | No intent-filter; implicitly not exported |
| Service | `.model.CacheService` | not set | No intent-filter; implicitly not exported |
| Service | `.WebService.BLE.BleDataService` | not set | No intent-filter; implicitly not exported |
| Service | `.WebService.BLE.BleControlService` | not set | No intent-filter; implicitly not exported |
| Service | `.session.SessionTimeoutJobService` | not set | `android:permission="android.permission.BIND_JOB_SERVICE"` |

---

### `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/AndroidManifest.xml`

Package: `com.yy.libcommon`

Permissions declared:
```
android.permission.ACCESS_NETWORK_STATE
android.permission.ACCESS_WIFI_STATE
android.permission.VIBRATE
```

Application attributes:
- `android:allowBackup="true"`
- No components declared (empty application element)

---

## Findings by Checklist Section

---

### Section 1: Signing and Keystores

#### FINDING CFG-001
**Severity:** Critical
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/fleetiq.jks`
**Line:** N/A (file presence)
**Detail:** The file `fleetiq.jks` is committed to the git repository and tracked in version control (confirmed via `git ls-files`). It appears in git history as far back as the "Initial commit to Bitbucket" (`a3863e3`). A private signing keystore in version control is permanently compromised: anyone with read access to the repository has possessed the private key material at least since that commit. The password for this keystore (`ciadmin`) is also committed, making extraction of the private key trivial.
**Recommendation:** Immediately revoke/rotate this signing key. Remove the file from git history using `git filter-repo` or BFG Repo Cleaner. Generate a new keystore stored outside the repository. Rotate any app signing on Google Play if this key was used for production releases.

#### FINDING CFG-002
**Severity:** Critical
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app.jks`
**Line:** N/A (file presence)
**Detail:** A second keystore file `app.jks` (6,817 bytes) is also committed to and tracked in version control. Its purpose relative to `fleetiq.jks` (2,323 bytes) is unclear from the assigned files, but both are present as tracked files.
**Recommendation:** Same as CFG-001. Audit which builds use `app.jks` vs `fleetiq.jks`. Remove from git history and rotate.

#### FINDING CFG-003
**Severity:** Critical
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/gradle.properties`
**Lines:** 19–31
**Detail:** Keystore passwords for all three signing configurations (dev, uat, release) are hardcoded as plaintext in `gradle.properties`, which is committed to version control. The password `ciadmin` is identical across all three environments (dev, uat, release), meaning that compromise of any one environment compromises all.
```
DEV_STORE_PASSWORD=ciadmin
DEV_KEY_PASSWORD=ciadmin
UAT_STORE_PASSWORD=ciadmin
UAT_KEY_PASSWORD=ciadmin
RELEASE_STORE_PASSWORD=ciadmin
RELEASE_KEY_PASSWORD=ciadmin
```
**Recommendation:** Remove all keystore credentials from `gradle.properties`. Use environment variables or a gitignored `signing.properties` file. Add `gradle.properties` to `.gitignore` or move secrets to `local.properties` (which is already gitignored). Use distinct strong passwords for each environment.

#### FINDING CFG-004
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/build.gradle`
**Lines:** 11–33
**Detail:** The signingConfigs block reads credentials from `gradle.properties` variables (`DEV_STORE_PASSWORD`, `RELEASE_STORE_PASSWORD`, etc.), which are committed. While the indirection via properties variables is a reasonable pattern, the properties file itself is not gitignored, making this equivalent to hardcoding the values directly in `build.gradle`. All three configs (dev, uat, release) reference the same `fleetiq.jks` keystore and the same password (`ciadmin`).
**Recommendation:** Gitignore `gradle.properties` or extract the secret properties to `local.properties` (already gitignored). Inject credentials from CI/CD environment variables for pipeline builds. Use distinct keystores and strong distinct passwords for dev, uat, and release environments.

#### FINDING CFG-005
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/build.gradle`
**Lines:** 15, 23, 31
**Detail:** `v2SigningEnabled false` is set for all three signing configurations. APK Signature Scheme v2 provides full-file integrity protection and is significantly stronger than the v1 JAR signing scheme. Disabling v2 signing means the app relies solely on v1 signing, which is susceptible to known bypass techniques. Google Play required v2 signing for apps targeting API 30+.
**Recommendation:** Enable `v2SigningEnabled true` (or remove the line; true is the default in modern Android Gradle Plugin). Consider also enabling v3 signing for API 28+ key rotation support.

#### FINDING CFG-006
**Severity:** Info
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/.gitignore` (root)
**Line:** N/A
**Detail:** No bitbucket-pipelines.yml was found in the repository. Therefore the Bitbucket Pipelines sub-checklist items (hardcoded keystore passwords in pipeline, service account credentials, secure variable injection) cannot be evaluated. This may mean CI/CD configuration is stored elsewhere or has not been implemented.
**Recommendation:** Verify CI/CD pipeline configuration location. If pipeline configuration exists externally, confirm it injects signing credentials as secure variables rather than hardcoding them.

---

### Section 2: Network Security

#### FINDING CFG-007
**Severity:** Medium
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Line:** 16–23 (application element)
**Detail:** `android:usesCleartextTraffic` is not explicitly set in the manifest. For `targetSdkVersion 26` (Android 8.0), the platform default is `true` — cleartext HTTP traffic is permitted by default. The app should explicitly set `android:usesCleartextTraffic="false"` to enforce HTTPS-only communication and eliminate the possibility of accidental HTTP connections. Given that this app transmits operator telemetry and forklift management data, cleartext traffic presents a material risk.
**Recommendation:** Add `android:usesCleartextTraffic="false"` to the `<application>` element in `AndroidManifest.xml`. Also add a `network_security_config.xml` to make the policy explicit and auditable.

#### FINDING CFG-008
**Severity:** Medium
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Line:** 16 (application element)
**Detail:** No `android:networkSecurityConfig` attribute is set. Without a Network Security Configuration file, the app uses Android platform defaults, which for `targetSdkVersion 26` include trusting the system CA store only (no user CAs in production). While the defaults are reasonable for this SDK level, the absence of an explicit `network_security_config.xml` means there is no documented, auditable policy for which certificate authorities are trusted, whether cleartext is permitted, and whether certificate pinning is applied. For an industrial IoT application, certificate pinning to the forkliftiqws backend should be strongly considered.
**Recommendation:** Create a `network_security_config.xml` that explicitly: (1) disallows cleartext, (2) trusts only system CAs, and (3) implements certificate or public-key pinning for the `pandora.fleetiq360.com` production endpoint.

#### FINDING CFG-009
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/build.gradle`
**Lines:** 74, 80, 86
**Detail:** Infrastructure hostnames and IP addresses for the dev, uat, and production environments are hardcoded as `BuildConfig` string fields committed to version control:
- Dev: `forklift360.canadaeast.cloudapp.azure.com:8443`
- UAT: `ec2-54-86-82-22.compute-1.amazonaws.com:8443`
- Prod: `pandora.fleetiq360.com`

The UAT endpoint is an AWS EC2 public IP hostname (`ec2-54-86-82-22.compute-1.amazonaws.com`), which encodes the IP address `54.86.82.22` directly in the hostname. Public exposure of infrastructure addresses in source code increases the attack surface.
**Recommendation:** Move endpoint URLs to build-time environment variables injected by the CI/CD system, or to a gitignored properties file. Do not commit infrastructure addresses to source control. Particularly for the UAT environment, use a stable DNS name rather than an IP-encoded AWS hostname.

---

### Section 3: Data Storage

#### FINDING CFG-010
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Line:** 18
**Detail:** `android:allowBackup="true"` is set in the app manifest. This allows the full contents of the app's data directory (`/data/data/au.com.collectiveintelligence.fleetiq360/`) to be extracted via `adb backup` without root access on unencrypted or developer-mode devices. For a forklift management app, this data directory may contain operator credentials, session tokens, and cached assignment data stored in SharedPreferences or the Realm database.
**Recommendation:** Set `android:allowBackup="false"`. If backup of non-sensitive user preferences is desired, use the `android:fullBackupContent` attribute to explicitly exclude sensitive files and SharedPreferences from backup.

#### FINDING CFG-011
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/AndroidManifest.xml`
**Line:** 9
**Detail:** The LibCommon library manifest also declares `android:allowBackup="true"`. While library manifests are merged into the app manifest at build time and the app-level setting typically takes precedence, the presence of `allowBackup="true"` in the library manifest means that if the app's setting were ever removed or if the manifest merge behaves unexpectedly, backup would remain enabled.
**Recommendation:** Remove or explicitly set `android:allowBackup="false"` in the LibCommon manifest to prevent ambiguity during manifest merging.

#### FINDING CFG-012
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Lines:** 7–8
**Detail:** `android.permission.WRITE_EXTERNAL_STORAGE` and `android.permission.READ_EXTERNAL_STORAGE` are declared. External storage (`/sdcard`, `Environment.getExternalStorageDirectory()`) is world-readable by any app on the device on Android versions below API 29. If the app writes operator data, credentials, Realm database files, or logs to external storage, that data is accessible to any installed app. The use of Realm (via the `realm-android` plugin) and the presence of image-handling libraries (LibImageloader, LibImagePicker) make external storage writes likely.
**Recommendation:** Audit all file write operations to confirm that sensitive data (operator records, credentials, session data) is written only to internal storage (`getFilesDir()`, `getCacheDir()`). Non-sensitive media (captured photos) should use `FileProvider` (already declared) rather than direct external storage paths.

---

### Section 4: Input and Intent Handling

#### FINDING CFG-013
**Severity:** Info
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Lines:** 91–98
**Detail:** The launcher activity is `.autoupdate.activity.ShowPackageAvailable`, not a more descriptively named login or main activity. This suggests the app performs an auto-update check on launch before navigating to `LoginActivity`. The activity has no explicit `android:exported` attribute but possesses a `MAIN`/`LAUNCHER` intent-filter, making it exported to the system launcher. The class name (`ShowPackageAvailable`) suggests it may download or install APK packages. If this activity can be invoked externally (e.g., via a deep link or another app's intent), it could be abused to trigger package installation with a malicious APK.
**Recommendation:** This finding requires source code review of `.autoupdate.activity.ShowPackageAvailable` (out of scope for CFG pass). Flag for the source code audit pass. Verify that: (1) the activity validates the package source, (2) installation cannot be triggered by an external intent, and (3) APK downloads occur only over HTTPS from the verified backend.

#### FINDING CFG-014
**Severity:** Info
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Line:** 81
**Detail:** A `com.yy.libcommon.WebActivity` is registered. The class name suggests a WebView-based activity in the LibCommon library. WebViews with JavaScript enabled that load arbitrary URLs pose risks (XSS, JavaScript bridge exposure, local file access). This requires source code review.
**Recommendation:** Flag for source code audit pass. Verify: JavaScript enabled/disabled setting, `setAllowFileAccess`, URL whitelist enforcement, and absence of `@JavascriptInterface` methods that expose sensitive operations.

#### FINDING CFG-015
**Severity:** Info
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Lines:** 99–106
**Detail:** Six background services are declared (BleMachineService, ShockEventService, SyncService, CacheService, BleDataService, BleControlService). None have explicit `android:exported` attributes or intent-filters, so they are not exported and cannot be invoked by other apps. The `SessionTimeoutJobService` has `android:permission="android.permission.BIND_JOB_SERVICE"` which correctly restricts binding to the system. No issues with service declarations from a configuration perspective.
**Recommendation:** No issues found at the manifest configuration level. Source code review should verify that these services do not store sensitive data insecurely or expose sensitive operations through bound interfaces.

No deep link handlers (`<intent-filter>` with `android:scheme`) were found in the manifest.

---

### Section 5: Authentication and Session

No issues found from configuration files alone — authentication implementation requires source code review (out of scope for CFG pass). The following observations are noted for the source code audit pass:

- The app uses Realm (via `realm-android` plugin) for data persistence. Realm databases are not encrypted by default. The source code audit should verify whether a Realm encryption key is used.
- The presence of `SessionTimeoutJobService` suggests session timeout functionality exists, which is a positive indicator.
- Five BLE-related services suggest operator authentication may rely on Bluetooth hardware keys or BLE proximity — the source code audit should verify that BLE identifiers are not used as sole authentication factors.

---

### Section 6: Third-Party Libraries

#### FINDING CFG-016
**Severity:** Critical
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/build.gradle`
**Line:** 9
**Detail:** `com.android.tools.build:gradle:3.0.0` was released in October 2017. The current version is 8.x. Version 3.0.0 is over 7 years old and no longer receives security updates from Google. Using an ancient build tool version means the build system itself may have unpatched vulnerabilities and does not support modern Android security features (e.g., APK Signature Scheme v3, R8 full mode, baseline profiles).
**Recommendation:** Update Android Gradle Plugin to the current stable version (8.x). This will require updating `gradle-wrapper.properties` from Gradle 4.1 to a compatible version (Gradle 8.x).

#### FINDING CFG-017
**Severity:** Critical
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/gradle/wrapper/gradle-wrapper.properties`
**Line:** 3
**Detail:** `gradle-4.1-all.zip` — Gradle 4.1 was released in August 2017. The current version is 8.x. This is over 7 years old and receives no security updates. Additionally, no `distributionSha256Sum` is configured in `gradle-wrapper.properties`, meaning a compromised or man-in-the-middle distribution URL could substitute a malicious Gradle binary without detection.
**Recommendation:** Update Gradle to the current stable version. Add `distributionSha256Sum` to `gradle-wrapper.properties` to verify the integrity of the downloaded Gradle distribution.

#### FINDING CFG-018
**Severity:** Critical
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/build.gradle`
**Line:** 10
**Detail:** `io.realm:realm-gradle-plugin:3.7.2` was released in 2017. The current version of Realm (now MongoDB Realm / Atlas Device SDK) is significantly newer. Realm 3.7.2 is unsupported and has known issues. More importantly, the combination of Realm without explicit encryption (not configured in build files) and `allowBackup="true"` means the Realm database could be extracted via ADB backup.
**Recommendation:** Update to a supported version of Realm or Atlas Device SDK. Enable Realm encryption by providing an encryption key stored in Android Keystore.

#### FINDING CFG-019
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/build.gradle`
**Lines:** 4–7, 16–20
**Detail:** Both `buildscript` and `allprojects` repository blocks include `jcenter()`. JCenter was shut down and is read-only as of February 2022; new artifacts are no longer published. More critically, JCenter's artifact integrity cannot be guaranteed post-shutdown, and the service may eventually cease distributing artifacts entirely. Using JCenter as a repository is a supply chain risk.
**Recommendation:** Remove `jcenter()` from all repository blocks and replace with `mavenCentral()`. Audit all JCenter-sourced dependencies to confirm they are available on Maven Central.

#### FINDING CFG-020
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/build.gradle`
**Lines:** 96–110
**Detail:** Multiple dependencies are severely outdated:

| Dependency | Version Used | Current Version | Age |
|---|---|---|---|
| `info.hoang8f:android-segmented` | 1.0.6 | ~1.0.6 (abandoned, last commit 2015) | ~11 years |
| `com.github.PhilJay:MPAndroidChart` | v3.0.2 (2018) | v3.1.0 (2020) | ~6 years |
| `com.android.volley:volley` | 1.1.1 (2018) | 1.2.1 (2021) | ~6 years |
| `joda-time:joda-time` | 2.10 (2018) | 2.12.7 (2024) | ~6 years |
| `com.squareup.retrofit2:retrofit` | 2.5.0 (2018) | 2.11.0 (2024) | ~6 years |
| `com.google.code.gson:gson` | 2.8.5 (2018) | 2.10.1 (2022) | ~6 years |
| `com.squareup.retrofit2:converter-gson` | 2.5.0 (2018) | 2.11.0 (2024) | ~6 years |
| `com.android.support:*` | 26.0.2 (2017) | AndroidX (migrated 2018+) | ~7 years (unmigrated) |
| `com.android.support:multidex` | 1.0.2 (2016) | 2.0.1 (2019) | ~8 years |
| `com.google.android.gms:play-services-location` | 11.8.0 (2017) | 21.x (2024) | ~7 years |
| `junit:junit` | 4.12 (2014) | 4.13.2 (2021) | ~10 years |

Notable CVEs:
- `gson:2.8.5` — CVE-2022-25647 (Deserialization of untrusted data, CVSS 7.5; fixed in 2.8.9)
- `com.android.support` libraries — The entire `android.support` namespace is deprecated and unmaintained; superseded by AndroidX. No security patches are backported to `android.support`.
- `play-services-location:11.8.0` — Multiple fixes in intervening versions including privacy-related changes.

**Recommendation:** Migrate from `android.support` to AndroidX. Update all dependencies to current versions. Prioritize `gson` due to the known high-severity CVE.

#### FINDING CFG-021
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/build.gradle`
**Lines:** 26–29
**Detail:** LibCommon repeats the same outdated dependency versions: `gson:2.8.5` (CVE-2022-25647), `com.android.support:appcompat-v7:26.0.2`, `com.android.support:design:26.0.2`.
**Recommendation:** Same as CFG-020.

#### FINDING CFG-022
**Severity:** Medium
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/settings.gradle`
**Line:** 1
**Detail:** Four library modules — `:LibImageloader`, `:LibImagePicker`, `:LibCircleImageView`, `:LibPercentProgress` — are included as local source modules rather than versioned Maven dependencies. Their build.gradle files were not in the assigned files list for this pass. The `LibImageloader` module appears to be a vendored copy of Universal Image Loader (last maintained ~2016), and `LibCircleImageView` is likely a vendored copy of the Hdodenhof CircleImageView library. Vendored copies may not receive security updates, and their provenance and modification history are opaque.
**Recommendation:** Audit each vendored library module in the source code pass. Replace vendored copies with versioned Maven Central dependencies where possible to enable dependency update tooling.

#### FINDING CFG-023
**Severity:** Medium
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/build.gradle` and `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/build.gradle`
**Lines:** app/build.gradle:53; LibCommon/build.gradle:19
**Detail:** `minifyEnabled false` is set for the release build type in both the app module and LibCommon. This disables ProGuard/R8 code shrinking, obfuscation, and minification for release builds. Without obfuscation, the app's reverse engineering difficulty is minimal — class names, method names, field names, and application logic are fully readable in the release APK. For an app handling operator authentication and telemetry data, this increases the risk of logic analysis by a malicious actor.
**Recommendation:** Enable `minifyEnabled true` for the release build type. Update `proguard-rules.pro` to add necessary `-keep` rules for Realm, Gson, Retrofit model classes, and any reflection-dependent code. Test thoroughly after enabling.

#### FINDING CFG-024
**Severity:** Low
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/proguard-rules.pro` and `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/proguard-rules.pro`
**Lines:** Both files — all lines
**Detail:** Both ProGuard rules files are effectively empty (all meaningful lines are commented out). Given that `minifyEnabled false` means ProGuard is not currently applied, this is a secondary concern. However, if `minifyEnabled` is ever enabled without first populating these files with appropriate rules, the build will likely fail or produce a broken app (e.g., Realm model classes, Gson-serialized DTOs, and Retrofit interfaces all require specific `-keep` rules).
**Recommendation:** Populate `proguard-rules.pro` with appropriate rules before enabling minification. Use the ProGuard/R8 rules recommended by each library (Realm, Gson, Retrofit all publish their required rules).

---

### Section 7: Google Play and Android Platform

#### FINDING CFG-025
**Severity:** Critical
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/build.gradle`
**Line:** 27
**Detail:** `targetSdkVersion 26` (Android 8.0, released 2017). Google Play requires `targetSdkVersion >= 34` for all new app submissions and updates (as of August 2024). The app cannot be updated on the Play Store with this configuration. Additionally, targeting SDK 26 means the app does not benefit from security improvements introduced in API 27–34, including:
- Background activity restrictions (API 29)
- Scoped storage enforcement (API 29+)
- Safer intent redirection (API 30)
- Blob storage API (API 33)
- Photo picker (API 33)
- Granular media permissions (API 33)

**Recommendation:** Update `targetSdkVersion` to 34 (minimum for Play Store compliance) or 35. This will require testing and remediation of deprecated API usage (see CFG-026).

#### FINDING CFG-026
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/build.gradle`
**Line:** 28
**Detail:** `minSdkVersion 21` (Android 5.0, released 2014). Android 5.0 and 5.1 reached end-of-life in November 2021 and represent approximately 0.1% of active Android devices. Supporting API 21 imposes development constraints and prevents use of modern security APIs (e.g., `EncryptedSharedPreferences` requires API 23, Android Keystore StrongBox requires API 28). This is a low operational risk but a development impediment.
**Recommendation:** Raise `minSdkVersion` to at least 23 (Android 6.0, ~99.5% device coverage) to enable use of runtime permissions, `EncryptedSharedPreferences`, and other security APIs introduced in Marshmallow.

#### FINDING CFG-027
**Severity:** High
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Lines:** 10–12
**Detail:** `android.permission.BLUETOOTH` and `android.permission.BLUETOOTH_ADMIN` are declared. On Android 12+ (API 31), these permissions are deprecated and replaced by the new `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, and `BLUETOOTH_ADVERTISE` permissions. If the app is updated to `targetSdkVersion 31+`, BLE functionality will break unless the manifest is updated with the new granular Bluetooth permissions.
**Recommendation:** When updating `targetSdkVersion`, add the API 31+ Bluetooth permissions (`BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`) with `usesPermissionFlags="neverForLocation"` where applicable. Retain the legacy permissions for backward compatibility on pre-API 31 devices using `maxSdkVersion`.

#### FINDING CFG-028
**Severity:** Medium
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Lines:** 7–8
**Detail:** `android.permission.WRITE_EXTERNAL_STORAGE` is declared without a `maxSdkVersion` constraint. On Android 10+ (API 29), `WRITE_EXTERNAL_STORAGE` has no effect on app-private directories and is disallowed for shared media storage (scoped storage). On Android 13+ (API 33), this permission is fully removed and replaced by granular media permissions. Declaring it unconditionally may trigger Play Store warnings.
**Recommendation:** Add `android:maxSdkVersion="28"` to the `WRITE_EXTERNAL_STORAGE` declaration. Replace external storage writes with scoped storage APIs for API 29+ (MediaStore API or app-specific directories).

#### FINDING CFG-029
**Severity:** Medium
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/AndroidManifest.xml`
**Lines:** 11–12
**Detail:** `android.permission.BLUETOOTH` and `android.permission.BLUETOOTH_ADMIN` are dangerous permissions on API 31+ but are declared without `maxSdkVersion` constraints. On API levels below 31, these permissions were classified as "normal" (automatically granted). The app requires BLE for core functionality (`bluetooth_le` is marked `required="true"`), making these permissions essential. However, no corresponding `BLUETOOTH_CONNECT` or `BLUETOOTH_SCAN` permissions are declared for API 31+ devices. This means BLE features will be non-functional on Android 12+ devices if the `targetSdkVersion` is ever updated to 31+.
**Recommendation:** Plan for API 31 Bluetooth permission migration as part of the `targetSdkVersion` upgrade.

#### FINDING CFG-030
**Severity:** Low
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/build.gradle`
**Line:** 4
**Detail:** `lintOptions { abortOnError false }` is set in LibCommon. This suppresses lint errors that would otherwise fail the build. Lint errors in a library module — including security-relevant lint checks (e.g., unsafe intent launches, exported component warnings, deprecated API usage) — will be silently ignored.
**Recommendation:** Remove `abortOnError false` or replace it with a specific list of suppressed lint IDs. At minimum, ensure security-relevant lint checks are not suppressed.

#### FINDING CFG-031
**Severity:** Info
**File:** `/c/Projects/cig-audit/repos/forkliftiqapp/LibCommon/src/main/AndroidManifest.xml`
**Line:** 7
**Detail:** LibCommon declares `android.permission.VIBRATE`. This permission is not declared in the main app manifest. Since library manifests are merged into the app manifest at build time, the app does acquire this permission at runtime. Vibrate is a low-risk normal permission, but it may indicate functionality (notifications, haptic alerts) that is not surfaced in the main app manifest.
**Recommendation:** No security risk. Confirm the permission is actually used in LibCommon source code (haptic feedback, notification vibration). If not used, remove it to follow the principle of least privilege.

---

## Summary Table

| ID | Severity | Section | Description |
|----|----------|---------|-------------|
| CFG-001 | Critical | Signing | `fleetiq.jks` keystore committed to git |
| CFG-002 | Critical | Signing | `app.jks` keystore committed to git |
| CFG-003 | Critical | Signing | All keystore passwords hardcoded in committed `gradle.properties` |
| CFG-016 | Critical | Libraries | Android Gradle Plugin 3.0.0 (2017), severely outdated |
| CFG-017 | Critical | Libraries | Gradle 4.1 (2017), no SHA256 verification |
| CFG-018 | Critical | Libraries | Realm 3.7.2 (2017), unsupported |
| CFG-025 | Critical | Play/Platform | `targetSdkVersion 26` — Play Store rejects updates |
| CFG-004 | High | Signing | signingConfigs read from committed `gradle.properties` |
| CFG-005 | High | Signing | `v2SigningEnabled false` on all signing configs |
| CFG-009 | High | Network | Infrastructure hostnames/IPs hardcoded in `build.gradle` |
| CFG-010 | High | Data Storage | `android:allowBackup="true"` in app manifest |
| CFG-011 | High | Data Storage | `android:allowBackup="true"` in LibCommon manifest |
| CFG-012 | High | Data Storage | `WRITE_EXTERNAL_STORAGE` declared — external storage risk |
| CFG-019 | High | Libraries | `jcenter()` repository — shut down, supply chain risk |
| CFG-020 | High | Libraries | Multiple severely outdated dependencies incl. gson CVE-2022-25647 |
| CFG-021 | High | Libraries | LibCommon repeats outdated deps incl. gson CVE-2022-25647 |
| CFG-023 | High | Libraries | `minifyEnabled false` for release — no obfuscation |
| CFG-026 | High | Play/Platform | `minSdkVersion 21` — prevents use of modern security APIs |
| CFG-027 | High | Play/Platform | Legacy Bluetooth permissions, will break on API 31+ |
| CFG-007 | Medium | Network | No explicit `usesCleartextTraffic="false"` |
| CFG-008 | Medium | Network | No `network_security_config.xml` — no cert pinning |
| CFG-022 | Medium | Libraries | Vendored local library modules, update opacity |
| CFG-028 | Medium | Play/Platform | `WRITE_EXTERNAL_STORAGE` no `maxSdkVersion` constraint |
| CFG-029 | Medium | Play/Platform | Bluetooth permissions not updated for API 31+ |
| CFG-030 | Low | Play/Platform | `lintOptions { abortOnError false }` suppresses lint errors |
| CFG-024 | Low | Libraries | ProGuard rules files are empty |
| CFG-006 | Info | Signing | No bitbucket-pipelines.yml found |
| CFG-013 | Info | Intents | Launcher activity is auto-update handler — review in SRC pass |
| CFG-014 | Info | Intents | `WebActivity` registered — JavaScript/WebView review needed |
| CFG-015 | Info | Intents | Six background services — no manifest-level issues |
| CFG-031 | Info | Play/Platform | LibCommon adds `VIBRATE` permission via manifest merge |

---

## Notes for Subsequent Audit Passes

The following items were identified as requiring source code review (out of scope for this CFG pass):

1. **SRC pass — Realm encryption:** Verify whether a Realm encryption key is provided at database open time. Key should be stored in Android Keystore.
2. **SRC pass — SharedPreferences encryption:** Audit all `SharedPreferences` usage for credential or token storage; verify `EncryptedSharedPreferences` is used for sensitive values.
3. **SRC pass — WebActivity:** Audit `com.yy.libcommon.WebActivity` for `setJavaScriptEnabled`, `setAllowFileAccess`, URL validation.
4. **SRC pass — ShowPackageAvailable:** Audit auto-update mechanism for APK source validation, HTTPS enforcement, and intent-based triggering risk.
5. **SRC pass — HTTP clients:** Audit Volley and Retrofit usage for `TrustAllCertificates` or permissive `HostnameVerifier` implementations.
6. **SRC pass — External storage writes:** Audit all `File` and `Environment` API calls for data written to external storage.
7. **SRC pass — Logout/session clearing:** Verify that logout clears all credentials, tokens, and Realm data from device storage.
8. **SRC pass — BLE authentication:** Verify BLE proximity is not used as a sole authentication factor.

---

*Report generated by Agent CFG — 2026-02-27*
