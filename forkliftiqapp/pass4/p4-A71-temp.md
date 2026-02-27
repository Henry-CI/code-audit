# Pass 4 Code Quality Audit — Agent A71
**Audit Run:** 2026-02-26-01
**Agent:** A71
**Date:** 2026-02-27
**Scope:** Build configuration, Gradle files, ProGuard rules, Android manifests

---

## Step 1: Reading Evidence

### File 1: `.gitignore`
**Purpose:** Tells Git which files and directories to exclude from version control.

**Significant declarations:**
- `*.iml` — Android Studio module files excluded
- `.gradle` — Gradle cache directory excluded
- `/local.properties` — Local SDK path file excluded (correct — contains machine-specific paths)
- `/.idea/workspace.xml` — IDE workspace excluded
- `/.idea/libraries` — IDE library index excluded
- `.DS_Store` — macOS metadata excluded
- `/build` — Root-level build output excluded
- `/captures` — Android profiler captures excluded
- `.idea` — Entire IDE config directory excluded
- `*/build` — Per-module build outputs excluded

**Observations:**
- `gradle.properties` is NOT listed in `.gitignore`. This file contains plaintext keystore passwords (see File 3).
- `/local.properties` is correctly excluded (standard Android convention).

---

### File 2: `build.gradle` (root)
**Purpose:** Top-level project build script. Configures repositories and classpath dependencies shared across all modules. Defines shared SDK version properties via `project.ext`.

**Significant declarations:**
- Plugin classpath: `com.android.tools.build:gradle:3.0.0`
- Plugin classpath: `io.realm:realm-gradle-plugin:3.7.2`
- Repositories (buildscript): `google()`, `jcenter()`
- Repositories (allprojects): `google()`, `jcenter()`, `https://jitpack.io`
- Shared ext properties (applied to all projects via `allprojects`):
  - `myBuildToolsVersion = "26.0.2"`
  - `myTargetSdkVersion = 26`
  - `myMinSdkVersion = 21`
  - `myCompileSdkVersion = 26`
- `task clean(type: Delete)` — standard clean task

**Observations:**
- Android Gradle Plugin version `3.0.0` is extremely old (current stable is 8.x as of 2026). This version predates many breaking changes.
- `jcenter()` repository is deprecated and shut down (read-only mirror ended 2022). Any dependency resolution from jcenter will now fail for packages not mirrored to Maven Central.
- Gradle wrapper is `4.1` (see File 4), which is the minimum required for AGP 3.0. Both are severely outdated.
- `myBuildToolsVersion = "26.0.2"` and `myCompileSdkVersion = 26` correspond to Android 8.0, released August 2017. As of 2024, the Play Store requires `targetSdkVersion >= 34`.
- Shared ext properties are defined inside `allprojects {}` block, making them available to all subprojects. This is a valid pattern, though defining them in `subprojects {}` or a separate `ext` block at root level would be cleaner.

---

### File 3: `gradle.properties`
**Purpose:** Project-wide Gradle properties. Configures JVM args for the Gradle daemon and defines keystore credentials used in signing configurations.

**Significant declarations:**
- `org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8`
- `# org.gradle.parallel=true` — parallel builds commented out
- Signing credential properties for three environments:
  - `DEV_STORE_FILE=../fleetiq.jks`
  - `DEV_STORE_PASSWORD=ciadmin`
  - `DEV_KEY_ALIAS=fleetiq`
  - `DEV_KEY_PASSWORD=ciadmin`
  - `UAT_STORE_FILE=../fleetiq.jks`
  - `UAT_STORE_PASSWORD=ciadmin`
  - `UAT_KEY_ALIAS=fleetiq`
  - `UAT_KEY_PASSWORD=ciadmin`
  - `RELEASE_STORE_FILE=../fleetiq.jks`
  - `RELEASE_STORE_PASSWORD=ciadmin`
  - `RELEASE_KEY_ALIAS=fleetiq`
  - `RELEASE_KEY_PASSWORD=ciadmin`

**Observations:**
- `-XX:MaxPermSize=512m` is a JVM flag for the Permanent Generation heap space, which was removed in Java 8 (JEP 122). On JDK 8+, this flag is silently ignored but generates a warning from the JVM on some distributions. It is dead configuration.
- All three environments (dev, uat, release) use the same keystore file (`../fleetiq.jks`), same alias (`fleetiq`), and identical passwords (`ciadmin`). There is no separation of signing keys between environments.
- Plaintext credentials for all environments are committed directly to `gradle.properties`, which is tracked by git (not in `.gitignore`). This is a critical secret exposure issue.
- The commented-out `# org.gradle.parallel=true` is dead/disabled configuration left in the file without explanation.

---

### File 4: `gradle/wrapper/gradle-wrapper.properties`
**Purpose:** Configures the Gradle wrapper — specifies which Gradle distribution to download and use.

**Significant declarations:**
- `distributionBase=GRADLE_USER_HOME`
- `distributionPath=wrapper/dists`
- `distributionUrl=https\://services.gradle.org/distributions/gradle-4.1-all.zip`
- `zipStoreBase=GRADLE_USER_HOME`
- `zipStorePath=wrapper/dists`

**Observations:**
- Gradle `4.1` was released September 2017. Current stable is Gradle 8.x. This is extremely outdated.
- The `-all` distribution type is used (includes sources and documentation). The `-bin` distribution is recommended for CI and production builds as it is smaller and faster to download.

---

### File 5: `settings.gradle`
**Purpose:** Defines which subprojects/modules are included in the multi-project build.

**Significant declarations:**
- Included modules: `:app`, `:LibCommon`, `:LibImageloader`, `:LibImagePicker`, `:LibCircleImageView`, `:LibPercentProgress`

**Observations:**
- Module naming is inconsistent: `:LibImageloader` uses lowercase `l` in "loader", while all other `Lib*` modules use PascalCase (`:LibImagePicker`, `:LibCircleImageView`, `:LibPercentProgress`, `:LibCommon`). The correct PascalCase form would be `:LibImageLoader`.
- No `rootProject.name` is set. While not required, it is a best practice to explicitly name the root project.

---

### File 6: `app/build.gradle`
**Purpose:** Module-level build script for the `:app` application module. Defines plugins, SDK versions, signing configs, build types, product flavors, and dependencies.

**Significant declarations:**
- Plugins: `com.android.application`, `realm-android`
- SDK versions referenced via `project.ext.*`
- Signing configs: `dev`, `uat`, `release` (each with `v2SigningEnabled false`)
- `buildTypes` block:
  - `defaultConfig` nested inside `buildTypes` (structural error — see findings)
  - `release` build type: `minifyEnabled false`, proguard files, `signingConfig signingConfigs.release`
- `flavorDimensions "environment"`
- Product flavors: `local`, `dev`, `uat`, `prod`
  - `local`: reads `local.properties`, constructs URL from `InetAddress.localHost.hostAddress`, sets `BASE_URL`
  - `dev`: `BASE_URL` = Azure Canada East endpoint
  - `uat`: `BASE_URL` = AWS EC2 public DNS endpoint
  - `prod`: `BASE_URL` = `pandora.fleetiq360.com`
- Dependencies:
  - Local module projects: `:LibCommon`, `:LibImageloader`, `:LibImagePicker`, `:LibCircleImageView`
  - `info.hoang8f:android-segmented:1.0.6`
  - `com.github.PhilJay:MPAndroidChart:v3.0.2`
  - `com.android.volley:volley:1.1.1`
  - `joda-time:joda-time:2.10`
  - `com.squareup.retrofit2:retrofit:2.5.0`
  - `com.google.code.gson:gson:2.8.5`
  - `com.squareup.retrofit2:converter-gson:2.5.0`
  - `junit:junit:4.12` (testImplementation)
  - `com.android.support:appcompat-v7:26.0.2`
  - `com.android.support:recyclerview-v7:26.0.2`
  - `com.android.support:support-v4:26.0.2`
  - `com.android.support:multidex:1.0.2`
  - `com.android.support:cardview-v7:26.0.2`
  - `com.google.android.gms:play-services-location:11.8.0`

**Observations:**
- `defaultConfig` is placed inside the `buildTypes {}` block (line 37). This is structurally incorrect in Gradle DSL. `defaultConfig` is a sibling of `buildTypes`, not a child of it. That AGP 3.0 apparently processes this without a compile error is surprising — it may work due to DSL quirks in older AGP versions, but it is wrong and would break under current AGP.
- `v2SigningEnabled false` is set on all three signing configs. APK Signature Scheme v2 was introduced in Android 7.0 (API 24). Disabling it means only v1 (JAR signing) is used, which is weaker and officially deprecated.
- The `local` flavor loads `local.properties` via `newDataInputStream()` but the loaded `properties` object is never used — the `serverUrl` is built directly from `InetAddress.localHost.hostAddress` without reading anything from `local.properties`. The file load is dead code.
- `minifyEnabled false` in the `release` build type means ProGuard/R8 is not run at all for release builds, despite `proguardFiles` being configured. The proguard-rules.pro file is effectively ignored.
- Hardcoded server endpoint IPs and hostnames appear in plaintext in the build file (uat flavor references an AWS EC2 public DNS with a literal IP in the hostname).
- Volley (`com.android.volley:volley:1.1.1`) and Retrofit (`com.squareup.retrofit2:retrofit:2.5.0`) are both present as networking libraries, indicating dual HTTP stacks without clear separation of concern.
- `:LibPercentProgress` is listed in `settings.gradle` and used in `:LibCommon`, but is not directly referenced in `app/build.gradle`. This is not itself a bug (transitive dependency via `:LibCommon`), but the dependency chain is implicit.

---

### File 7: `app/proguard-rules.pro`
**Purpose:** Module-specific ProGuard/R8 rules for the `:app` module.

**Significant declarations:**
- All content is comments — no active rules
- Comment at line 3 references a local developer path: `D:\d_before_20150611\adt-bundle-windows-x86-20130522\sdk/tools/proguard/proguard-android.txt`
- Commented-out WebView/JavaScript interface keep rule (lines 15–17)

**Observations:**
- The SDK path in the comment (`D:\d_before_20150611\adt-bundle-windows-x86-20130522\`) is a developer machine-specific absolute path from approximately 2013 (pre-Android Studio era, ADT Bundle). This is stale boilerplate from an extremely old project template.
- The file contains no active ProGuard rules whatsoever. Combined with `minifyEnabled false` in `app/build.gradle`, release builds receive zero shrinking, obfuscation, or optimization.

---

### File 8: `LibCommon/build.gradle`
**Purpose:** Module-level build script for the `:LibCommon` Android library module.

**Significant declarations:**
- Plugin: `com.android.library`
- `lintOptions { abortOnError false }` — lint errors do not fail the build
- SDK versions referenced via `project.ext.*`
- `defaultConfig` inside `buildTypes {}` block (same structural issue as app module):
  - `versionCode 1`
  - `versionName "1.0"`
- `release` build type: `minifyEnabled false`, proguard files
- Dependencies:
  - `com.google.code.gson:gson:2.8.5`
  - `com.android.support:appcompat-v7:26.0.2`
  - `com.android.support:design:26.0.2`
  - `project(path: ':LibPercentProgress')`

**Observations:**
- `defaultConfig` is again placed inside `buildTypes {}` (same structural error as in `app/build.gradle`).
- `versionCode` and `versionName` in a library module's `defaultConfig` are ignored by the Android build system — library modules do not produce APKs and do not use these values. They are dead configuration.
- `lintOptions { abortOnError false }` silences all lint errors globally for this module. This hides genuine code quality issues.
- `com.google.code.gson:gson:2.8.5` is declared in both `:LibCommon` (line 26) and `:app` (line 101) at the same version. While this does not cause a conflict, the duplication means the version must be kept in sync manually.
- `com.android.support:appcompat-v7:26.0.2` is declared in both `:LibCommon` (line 27) and `:app` (line 104) at the same version — same duplication concern as gson.

---

### File 9: `LibCommon/proguard-rules.pro`
**Purpose:** Module-specific ProGuard/R8 rules for the `:LibCommon` module.

**Significant declarations:**
- All content is comments — no active rules
- Comment at line 2 references a developer machine path: `/Users/steveyang/Library/Android/sdk/tools/proguard/proguard-android.txt`
- Commented-out WebView keep rule (lines 15–17)
- Commented-out `keepattributes SourceFile,LineNumberTable` (lines 20–21)
- Commented-out `-renamesourcefileattribute SourceFile` (lines 24–25)

**Observations:**
- SDK path references a macOS developer home directory (`/Users/steveyang/`), a different developer machine than the Windows path in `app/proguard-rules.pro`. Both files are boilerplate from different developer environments.
- No active rules exist in this file either.

---

### File 10: `app/src/main/AndroidManifest.xml`
**Purpose:** Application manifest. Declares the application package, permissions, hardware features, application components (activities, services, providers).

**Significant declarations:**
- Package: `au.com.collectiveintelligence.fleetiq360`
- Permissions declared:
  - `INTERNET`
  - `ACCESS_WIFI_STATE`
  - `ACCESS_NETWORK_STATE`
  - `READ_EXTERNAL_STORAGE`
  - `WRITE_EXTERNAL_STORAGE`
  - `CAMERA`
  - `BLUETOOTH`
  - `BLUETOOTH_ADMIN`
  - `ACCESS_FINE_LOCATION`
- Hardware feature: `android.hardware.bluetooth_le` required=true
- Application attributes:
  - `android:name=".ui.application.MyApplication"`
  - `android:allowBackup="true"`
  - `android:icon="@mipmap/ic_launcher"`
  - `android:label="@string/app_name"`
  - `android:largeHeap="true"`
  - `android:supportsRtl="true"`
  - `android:theme="@style/AppThemeDark"`
- Provider: `android.support.v4.content.FileProvider` (authorities: `au.com.collectiveintelligence.fleetiq360.fileprovider`)
- Activities (12 total): `ActionClearActivity`, `LoginActivity`, `DashboardActivity`, `EquipmentActivity`, `JobsActivity`, `ProfileActivity`, `IncidentActivity`, `DriverStatsActivity`, `EquipmentStatsActivity`, `ActionActivity`, `SessionActivity`, `com.yy.libcommon.WebActivity`, `DriversActivity`, `ShowPackageAvailable`
- LAUNCHER intent-filter on: `ShowPackageAvailable` (autoupdate activity)
- Services (6): `BleMachineService`, `ShockEventService`, `SyncService`, `CacheService`, `BleDataService`, `BleControlService`, `SessionTimeoutJobService`

**Observations:**
- `android:allowBackup="true"` — allows ADB backup of the application's data partition. For an industrial fleet management application, this may expose sensitive operational data.
- `android:largeHeap="true"` — requests a larger heap from the system. This is a workaround for memory issues rather than a root-cause fix and should be used only when profiling confirms it is necessary.
- The LAUNCHER activity is `ShowPackageAvailable` (an auto-update activity in the `autoupdate` package), not a login or main screen. This is an unusual design — the app starts with an auto-update check rather than a main application entry point. This may be intentional but is architecturally unconventional.
- `BLUETOOTH` and `BLUETOOTH_ADMIN` are legacy Bluetooth permissions. On Android 12+ (API 31), these are replaced by `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, and `BLUETOOTH_ADVERTISE`. Since `targetSdkVersion=26`, this is not currently a manifest compatibility issue, but it is a significant forward-compatibility concern.
- `READ_EXTERNAL_STORAGE` and `WRITE_EXTERNAL_STORAGE` are deprecated on Android 10+ (scoped storage). Since `targetSdkVersion=26`, these still apply, but upgrading the target SDK will require storage scope migration.
- The `FileProvider` uses `android.support.v4.content.FileProvider` (AndroidX migration has not been performed — legacy support library is used throughout).
- `com.yy.libcommon.WebActivity` is declared directly in the app manifest with its full qualified class name from the library package. This is a pattern that tightly couples the app manifest to the library's internal package name.

---

### File 11: `LibCommon/src/main/AndroidManifest.xml`
**Purpose:** Library module manifest for `:LibCommon`. Declares library-level permissions and an empty application element.

**Significant declarations:**
- Package: `com.yy.libcommon`
- Permissions:
  - `ACCESS_NETWORK_STATE`
  - `ACCESS_WIFI_STATE`
  - `VIBRATE`
- Application element: present but empty (`android:allowBackup="true"`, `android:label="@string/app_name"`, `android:supportsRtl="true"`)

**Observations:**
- `ACCESS_NETWORK_STATE` and `ACCESS_WIFI_STATE` are declared in both the library manifest (`LibCommon/src/main/AndroidManifest.xml`) and the app manifest (`app/src/main/AndroidManifest.xml`). Manifest merger will deduplicate these, but the duplication indicates no deliberate ownership of these permissions.
- `VIBRATE` is declared in the library manifest but not in the app manifest. The library implicitly adds this permission to any app that uses it. If the app does not use vibration directly, this is an unnecessary permission being silently injected.
- The `<application>` element in a library manifest with `android:allowBackup="true"` and `android:label="@string/app_name"` can cause manifest merger conflicts if the app's application element has different values. The `android:label` pointing to `@string/app_name` requires that string to exist in the library's resources, or manifest merger may fail.
- The empty `<application>` block (with only whitespace between tags) serves no functional purpose in a library manifest and is unnecessary boilerplate.

---

## Step 2 & 3: Findings

---

### A71-1 — CRITICAL: Plaintext keystore credentials committed to version-controlled `gradle.properties`

**File:** `gradle.properties` (lines 19–32)
**Category:** Secret exposure

All keystore passwords for dev, UAT, and release signing are stored in plaintext in `gradle.properties`. This file is not listed in `.gitignore` and is tracked by git. The credentials (`ciadmin`) are exposed to anyone with read access to the repository.

```
DEV_STORE_PASSWORD=ciadmin
DEV_KEY_PASSWORD=ciadmin
UAT_STORE_PASSWORD=ciadmin
UAT_KEY_PASSWORD=ciadmin
RELEASE_STORE_PASSWORD=ciadmin
RELEASE_KEY_PASSWORD=ciadmin
```

Additionally, `gradle.properties` is not in `.gitignore`, meaning there is no mechanical barrier preventing future credential additions from also being committed.

---

### A71-2 — CRITICAL: `defaultConfig` misplaced inside `buildTypes {}` block in both `app/build.gradle` and `LibCommon/build.gradle`

**Files:** `app/build.gradle` (line 37), `LibCommon/build.gradle` (line 12)
**Category:** Structural DSL error / leaky abstraction

In Android Gradle DSL, `defaultConfig` must be a direct child of the `android {}` block, not nested inside `buildTypes {}`. Both modules have this structural error:

```groovy
// app/build.gradle (incorrect structure)
android {
    buildTypes {
        defaultConfig {          // <-- WRONG: should be sibling of buildTypes, not child
            applicationId '...'
            minSdkVersion ...
            ...
        }
        release { ... }
    }
}
```

The correct structure is:
```groovy
android {
    defaultConfig { ... }    // sibling of buildTypes
    buildTypes { ... }
}
```

This works under AGP 3.0 only because of lenient DSL parsing in that ancient version. Under any current AGP version this would be a build error. It also means `defaultConfig` is being treated as a custom build type named "defaultConfig", not as the actual `defaultConfig` configuration.

---

### A71-3 — HIGH: `jcenter()` repository used in both `buildscript` and `allprojects`

**File:** `build.gradle` (root), lines 6, 19
**Category:** Build warning / deprecated dependency source

JCenter was shut down by JFrog. It is no longer receiving new artifacts and its read-only period has ended. Any dependency resolved exclusively from JCenter will fail to download in a clean environment.

```groovy
buildscript {
    repositories {
        google()
        jcenter()   // deprecated and closed
    }
}
allprojects {
    repositories {
        google()
        jcenter()   // deprecated and closed
        maven { url "https://jitpack.io" }
    }
}
```

---

### A71-4 — HIGH: `minifyEnabled false` on release build type — ProGuard rules are dead configuration

**Files:** `app/build.gradle` (line 52), `LibCommon/build.gradle` (line 19)
**Category:** Dead code / security gap

Both modules set `minifyEnabled false` in their release build types despite declaring `proguardFiles`. This means:
- No code shrinking
- No obfuscation
- No optimization
- The `proguard-rules.pro` files in both modules have no effect

For a production application, this leaves the APK unobfuscated and larger than necessary.

---

### A71-5 — HIGH: `v2SigningEnabled false` on all signing configurations

**File:** `app/build.gradle` (lines 15, 23, 31)
**Category:** Security / deprecated signing

APK Signature Scheme v2 was introduced in Android 7.0 and is now the minimum recommended scheme. It provides stronger tamper detection than v1 (JAR signing). All three signing configurations explicitly disable it:

```groovy
dev     { ... v2SigningEnabled false }
uat     { ... v2SigningEnabled false }
release { ... v2SigningEnabled false }
```

The `v2SigningEnabled` property itself is deprecated in recent AGP versions (replaced by `enableV2Signing`), making this both a security issue and a deprecated API usage.

---

### A71-6 — HIGH: Severely outdated toolchain — AGP 3.0.0, Gradle 4.1, compileSdkVersion 26, targetSdkVersion 26

**Files:** `build.gradle` (root) line 9; `gradle/wrapper/gradle-wrapper.properties` line 3; `build.gradle` (root) lines 26–28
**Category:** Build warnings / obsolete flags

The entire toolchain is from 2017:
- Android Gradle Plugin: `3.0.0` (current: ~8.5)
- Gradle Wrapper: `4.1` (current: ~8.10)
- `compileSdkVersion`: `26` (Android 8.0, August 2017)
- `targetSdkVersion`: `26`

Google Play Store requires `targetSdkVersion >= 34` for new app submissions and updates (as of August 2024). Shipping with `targetSdkVersion 26` means:
- The app cannot be updated on the Play Store
- Android behaviour compatibility shims for old target SDKs apply, potentially masking bugs
- Many modern APIs are unavailable

---

### A71-7 — HIGH: `lintOptions { abortOnError false }` in `LibCommon/build.gradle`

**File:** `LibCommon/build.gradle` (lines 4–6)
**Category:** Dead code / build warnings suppressed

Lint errors are globally suppressed for the LibCommon module. This means any lint violations, including serious ones (security issues, API level violations, resource problems), will not fail the build and will likely go unnoticed.

```groovy
lintOptions {
    abortOnError false
}
```

---

### A71-8 — MEDIUM: `-XX:MaxPermSize=512m` JVM flag is obsolete (removed in Java 8)

**File:** `gradle.properties` (line 13)
**Category:** Obsolete flag / dead configuration

```
org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```

`-XX:MaxPermSize` was removed in Java 8 when PermGen was replaced by Metaspace. On JDK 8+, this flag generates a warning (`Unrecognized VM option 'MaxPermSize=512m'`) and is silently ignored. It is dead configuration.

---

### A71-9 — MEDIUM: Module name capitalization inconsistency in `settings.gradle`

**File:** `settings.gradle` (line 1)
**Category:** Style inconsistency

All library module names follow PascalCase (`:LibCommon`, `:LibImagePicker`, `:LibCircleImageView`, `:LibPercentProgress`) except `:LibImageloader`, which uses lowercase `l` in "loader":

```
include ':app', ':LibCommon', ':LibImageloader', ':LibImagePicker', ':LibCircleImageView', ':LibPercentProgress'
```

The consistent name would be `:LibImageLoader`.

---

### A71-10 — MEDIUM: `local` product flavor loads `local.properties` but never uses the loaded data

**File:** `app/build.gradle` (lines 61–63)
**Category:** Dead code

```groovy
local {
    def properties = new Properties()
    properties.load(project.rootProject.file("local.properties").newDataInputStream())

    def serverUrl = '\"https://' + java.net.InetAddress.localHost.hostAddress + ':8443/fleetiq360ws\"'
    // properties object is loaded but never read
    ...
}
```

The `local.properties` file is read into `properties` but `properties` is never queried. The server URL is constructed entirely from `InetAddress.localHost`, making the file load dead code. This also creates an unnecessary build-time dependency on the existence of `local.properties`.

---

### A71-11 — MEDIUM: Dual HTTP networking stacks (Volley + Retrofit) without separation of concern

**File:** `app/build.gradle` (lines 98, 100, 102)
**Category:** Style inconsistency / leaky abstraction

Both Volley and Retrofit/OkHttp are included as runtime dependencies:
```
implementation 'com.android.volley:volley:1.1.1'
implementation 'com.squareup.retrofit2:retrofit:2.5.0'
implementation 'com.squareup.retrofit2:converter-gson:2.5.0'
```

Having two HTTP stacks increases APK size and creates ambiguity about which stack owns which network calls.

---

### A71-12 — MEDIUM: `android:allowBackup="true"` on app handling operational fleet data

**File:** `app/src/main/AndroidManifest.xml` (line 18)
**Category:** Security concern

`android:allowBackup="true"` permits ADB backup of all application data, including cached credentials, Realm database contents, and session data. For an industrial fleet management application, this may expose sensitive operational or safety-related information. If backups are not an intended feature, this should be `false`.

---

### A71-13 — MEDIUM: `VIBRATE` permission injected silently by `LibCommon` library manifest

**File:** `LibCommon/src/main/AndroidManifest.xml` (line 7)
**Category:** Leaky abstraction

The library manifest declares `VIBRATE` permission:
```xml
<uses-permission android:name="android.permission.VIBRATE" />
```

This permission will be merged into the final app manifest by the manifest merger. The app's own manifest does not declare `VIBRATE`, meaning any app consuming `LibCommon` will acquire this permission without explicit awareness. Library manifests should declare only permissions that are strictly required by library functionality, and this injection is not visible in the app's manifest file.

---

### A71-14 — MEDIUM: All environments share the same keystore file and alias

**File:** `gradle.properties` (lines 19–32)
**Category:** Security / signing

All three signing configurations (`dev`, `uat`, `release`) reference the same keystore file (`../fleetiq.jks`), same alias (`fleetiq`), and identical passwords (`ciadmin`). There is no separation between development, test, and production signing keys. A compromise of any one environment's credentials exposes all signing keys.

---

### A71-15 — MEDIUM: Launcher activity is the auto-update activity, not a main entry point

**File:** `app/src/main/AndroidManifest.xml` (lines 91–98)
**Category:** Style inconsistency / architectural concern

The LAUNCHER intent-filter is placed on `ShowPackageAvailable` in the `autoupdate` package, not on `LoginActivity` or a dedicated splash/entry activity. This is architecturally unconventional and means the auto-update check is the application's entry point, which could cause issues if the update service is unavailable.

---

### A71-16 — LOW: `versionCode` and `versionName` declared in `LibCommon/build.gradle` `defaultConfig` are ignored

**File:** `LibCommon/build.gradle` (lines 15–16)
**Category:** Dead code

Library modules do not produce APKs and do not use `versionCode` or `versionName`. These declarations are dead configuration:
```groovy
versionCode 1
versionName "1.0"
```

---

### A71-17 — LOW: ProGuard boilerplate comments contain developer machine-specific absolute paths

**Files:** `app/proguard-rules.pro` (line 3), `LibCommon/proguard-rules.pro` (line 2)
**Category:** Dead code / stale boilerplate

`app/proguard-rules.pro` contains:
```
# in D:\d_before_20150611\adt-bundle-windows-x86-20130522\sdk/tools/proguard/proguard-android.txt
```

`LibCommon/proguard-rules.pro` contains:
```
# in /Users/steveyang/Library/Android/sdk/tools/proguard/proguard-android.txt
```

These are machine-specific absolute paths from two different developers' machines embedded in committed files. The paths are also from different operating systems (Windows and macOS respectively), indicating these are unmodified boilerplate from individual development environments.

---

### A71-18 — LOW: Duplicate dependency declarations across `app` and `LibCommon` without version centralization

**Files:** `app/build.gradle` (lines 101, 104), `LibCommon/build.gradle` (lines 26–27)
**Category:** Style inconsistency / maintenance concern

The following dependencies are declared independently in both modules without a centralized version variable:
- `com.google.code.gson:gson:2.8.5` (app line 101, LibCommon line 26)
- `com.android.support:appcompat-v7:26.0.2` (app line 104, LibCommon line 27)

Version management is manual and error-prone. A `versions.gradle` or `buildSrc` approach, or Gradle version catalogs, would centralize this.

---

### A71-19 — LOW: `gradle/wrapper/gradle-wrapper.properties` uses `-all` distribution instead of `-bin`

**File:** `gradle/wrapper/gradle-wrapper.properties` (line 3)
**Category:** Build inefficiency

```
distributionUrl=https\://services.gradle.org/distributions/gradle-4.1-all.zip
```

The `-all` distribution includes Gradle source code and documentation. For a build environment, `-bin` (binary-only) is recommended as it is smaller and faster to resolve. The `-all` distribution is primarily useful for IDE navigation of Gradle source.

---

### A71-20 — LOW: Empty `<application>` block in `LibCommon/src/main/AndroidManifest.xml`

**File:** `LibCommon/src/main/AndroidManifest.xml` (lines 9–12)
**Category:** Dead code / unnecessary boilerplate

```xml
<application android:allowBackup="true" android:label="@string/app_name"
    android:supportsRtl="true">

</application>
```

Library manifests do not need an `<application>` element unless registering components. This empty block adds noise and the `android:label` attribute requires `@string/app_name` to be defined in the library's resources, which may cause merge warnings. The `android:allowBackup="true"` on a library manifest is also meaningless (only the app manifest's value is used).

---

### A71-21 — INFO: `org.gradle.parallel=true` is commented out

**File:** `gradle.properties` (line 18)
**Category:** Disabled configuration

```
# org.gradle.parallel=true
```

Parallel project execution is disabled with no explanation. For a multi-module project, enabling parallel builds (when modules are properly decoupled) significantly reduces build times.

---

### A71-22 — INFO: `android:largeHeap="true"` set on application

**File:** `app/src/main/AndroidManifest.xml` (line 21)
**Category:** Potential code quality concern

`android:largeHeap="true"` is present. While sometimes necessary, it is generally a workaround for memory management issues rather than a targeted fix. Noted as informational — investigation of whether memory profiling was performed before adding this flag would be warranted.

---

## Summary Table

| ID     | Severity | File(s)                                         | Issue                                                                              |
|--------|----------|-------------------------------------------------|------------------------------------------------------------------------------------|
| A71-1  | CRITICAL | `gradle.properties`                             | Plaintext keystore credentials committed to tracked file                           |
| A71-2  | CRITICAL | `app/build.gradle`, `LibCommon/build.gradle`    | `defaultConfig` misplaced inside `buildTypes {}` block — structural DSL error      |
| A71-3  | HIGH     | `build.gradle` (root)                           | `jcenter()` repository is deprecated and closed                                    |
| A71-4  | HIGH     | `app/build.gradle`, `LibCommon/build.gradle`    | `minifyEnabled false` on release — ProGuard configuration is dead                  |
| A71-5  | HIGH     | `app/build.gradle`                              | `v2SigningEnabled false` on all signing configs — weak/deprecated signing           |
| A71-6  | HIGH     | `build.gradle`, `gradle-wrapper.properties`     | Severely outdated toolchain (AGP 3.0.0, Gradle 4.1, SDK 26)                       |
| A71-7  | HIGH     | `LibCommon/build.gradle`                        | `lintOptions { abortOnError false }` suppresses all lint errors                    |
| A71-8  | MEDIUM   | `gradle.properties`                             | `-XX:MaxPermSize` is obsolete (removed in Java 8)                                  |
| A71-9  | MEDIUM   | `settings.gradle`                               | `:LibImageloader` naming is inconsistent (should be `:LibImageLoader`)             |
| A71-10 | MEDIUM   | `app/build.gradle`                              | `local.properties` loaded but never read in `local` flavor — dead code            |
| A71-11 | MEDIUM   | `app/build.gradle`                              | Dual HTTP stacks (Volley + Retrofit) without clear separation                      |
| A71-12 | MEDIUM   | `app/src/main/AndroidManifest.xml`              | `android:allowBackup="true"` on app handling fleet data                            |
| A71-13 | MEDIUM   | `LibCommon/src/main/AndroidManifest.xml`        | `VIBRATE` permission silently injected into app via library manifest               |
| A71-14 | MEDIUM   | `gradle.properties`                             | All environments share identical keystore, alias, and password                     |
| A71-15 | MEDIUM   | `app/src/main/AndroidManifest.xml`              | LAUNCHER activity is the auto-update screen, not a primary entry point             |
| A71-16 | LOW      | `LibCommon/build.gradle`                        | `versionCode`/`versionName` in library `defaultConfig` are dead configuration     |
| A71-17 | LOW      | `app/proguard-rules.pro`, `LibCommon/proguard-rules.pro` | Developer machine-specific absolute paths in committed boilerplate comments |
| A71-18 | LOW      | `app/build.gradle`, `LibCommon/build.gradle`    | Shared dependencies duplicated without version centralization                      |
| A71-19 | LOW      | `gradle-wrapper.properties`                     | `-all` distribution used instead of `-bin`                                         |
| A71-20 | LOW      | `LibCommon/src/main/AndroidManifest.xml`        | Empty `<application>` block with unnecessary attributes in library manifest        |
| A71-21 | INFO     | `gradle.properties`                             | `org.gradle.parallel=true` commented out with no explanation                       |
| A71-22 | INFO     | `app/src/main/AndroidManifest.xml`              | `android:largeHeap="true"` — may indicate unresolved memory issues                 |
