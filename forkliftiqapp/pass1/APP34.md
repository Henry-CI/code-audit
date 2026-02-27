# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP34
**Date:** 2026-02-27
**Stack:** Android/Java
**Branch Verified:** master

---

## Branch Discrepancy

The checklist specifies `Branch: main`. The actual default branch is `master`. Audit proceeded on `master` as instructed.

---

## Reading Evidence

### File 1: `ShowPackageAvailable.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.autoupdate.activity.ShowPackageAvailable`

**Type:** `Activity` (extends `android.app.Activity`)

**Declared in AndroidManifest.xml:** Yes — at line 91–98, with `<intent-filter>` declaring `ACTION_MAIN` / `CATEGORY_LAUNCHER`. This is the app's launch activity. No `android:exported` attribute is explicitly set; when an `<intent-filter>` is present, the component is exported by default.

**Public methods and line numbers:**

| Signature | Line |
|---|---|
| `ShowPackageAvailable()` (constructor) | 47 |
| `void onCreate(Bundle savedInstanceState)` | 52 |
| `void onStart()` | 59 |
| `boolean onKeyDown(int keyCode, KeyEvent event)` | 153 |
| `void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults)` | 174 |

**Private methods:**

| Signature | Line |
|---|---|
| `void alertNewPackageAvailable(APKPackage apkPackage)` | 88 |
| `boolean haveStoragePermission()` | 103 |
| `void downloadAndInstall(APKPackage apkPackage)` | 120 |
| `void writeResponseBodyToDisk(ResponseBody body, File apkPackageFile)` | 143 |
| `void raiseNotificationPackageReadyToInstall(File apkPackageFile)` | 158 |

**Fields / constants:**

| Name | Type | Value | Line |
|---|---|---|---|
| `TAG` | `String` (static final) | canonical class name | 40 |
| `PACKAGE_EXTRA` | `String` (static final) | `"apkPackage"` | 42 |
| `ANDROID_APK_MIME_TYPE` | `String` (static final) | `"application/vnd.android.package-archive"` | 43 |
| `service` | `APKUpdateService` (instance) | — | 45 |

---

### File 2: `APKPackage.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.autoupdate.model.APKPackage`

**Type:** Model / POJO (implements `java.io.Serializable`)

**Public methods and line numbers:**

| Signature | Line |
|---|---|
| `String getName()` | 14 |
| `void setName(String name)` | 18 |
| `String getFileName()` | 22 |
| `void setFileName(String fileName)` | 26 |
| `String getUrl()` | 30 |
| `void setUrl(String url)` | 34 |
| `int getMajor()` | 38 |
| `void setMajor(int major)` | 42 |
| `int getMinor()` | 46 |
| `void setMinor(int minor)` | 50 |
| `int getPatch()` | 54 |
| `void setPatch(int patch)` | 58 |

**Fields:**

| Name | Type | Line |
|---|---|---|
| `name` | `String` (private) | 7 |
| `fileName` | `String` (private) | 8 |
| `url` | `String` (private) | 9 |
| `major` | `int` (private) | 10 |
| `minor` | `int` (private) | 11 |
| `patch` | `int` (private) | 12 |

---

### File 3: `APKUpdateService.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.autoupdate.service.APKUpdateService`

**Type:** Retrofit2 service interface

**Public methods and line numbers:**

| Signature | Annotation | Line |
|---|---|---|
| `Call<APKPackage> getLatestAvailableUpdate(String pkgName, String version)` | `@GET("rest/apk/{pkgname}/update")` | 13 |
| `Call<ResponseBody> downloadPackage(String packageUrl)` | `@GET` with `@Url` | 15 |

**Note on `downloadPackage`:** The `@Url` annotation means Retrofit replaces the base URL entirely with whatever string is passed in `packageUrl`. The URL value originates from the server-controlled `APKPackage.url` field deserialized from the JSON response body. There is no client-side validation of this URL.

---

### Supporting files read (for context)

- `APKUpdateServiceFactory.java` — constructs the Retrofit instance using `BuildConfig.BASE_URL` and an `OkHttpClient` sourced from `OkHttpClientFactory`.
- `OkHttpClientFactory.java` — configures OkHttp with `FakeX509TrustManager` and a blanket `HostnameVerifier` that returns `true`.
- `FakeX509TrustManager.java` — implements `X509TrustManager` with no-op `checkClientTrusted` and `checkServerTrusted` methods; accepts all certificates.
- `app/build.gradle` — defines product flavors (`local`, `dev`, `uat`, `prod`) each with a hardcoded `BASE_URL`; signing passwords in `gradle.properties`.
- `gradle.properties` — contains signing credentials for all environments in plaintext.
- `AndroidManifest.xml` — full manifest for the application module.

---

## Findings

### 1. Signing and Keystores

**CRITICAL — Keystore files committed to version control**
Two keystore files are present in the repository root:
- `/c/Projects/cig-audit/repos/forkliftiqapp/fleetiq.jks`
- `/c/Projects/cig-audit/repos/forkliftiqapp/app.jks`

Neither file is listed in `.gitignore` (root `.gitignore` does not exclude `*.jks`). These private keys are permanently compromised from the moment of commit. Any party with read access to the repository can sign arbitrary APKs with the official release identity.

**CRITICAL — Keystore passwords hardcoded in `gradle.properties` committed to version control**
`gradle.properties` (lines 19–31) contains plaintext credentials for all three signing environments:

```
DEV_STORE_PASSWORD=ciadmin
DEV_KEY_PASSWORD=ciadmin
UAT_STORE_PASSWORD=ciadmin
UAT_KEY_PASSWORD=ciadmin
RELEASE_STORE_PASSWORD=ciadmin
RELEASE_KEY_PASSWORD=ciadmin
```

The release keystore password (`ciadmin`) is identical across all environments, which reduces effective key security to zero even if the file were later removed from version control history.

**FINDING — `gradle.properties` is not excluded by `.gitignore`**
The root `.gitignore` excludes `/local.properties` but makes no mention of `gradle.properties`. Signing credentials are therefore committed to the repository.

**FINDING — APK Signature Scheme v2 disabled for all signing configurations**
`app/build.gradle` lines 15, 23, 32 each set `v2SigningEnabled false`. APK Signature Scheme v2 (introduced in Android 7.0) provides stronger integrity guarantees over the entire APK archive. Disabling it degrades tamper detection.

**FINDING — No `bitbucket-pipelines.yml` found**
No CI/CD pipeline configuration file was found in the repository. It cannot be determined whether signing credentials are injected via pipeline environment variables. Given the credentials are committed in `gradle.properties`, the build system does not use secure secret injection.

---

### 2. Network Security

**CRITICAL — SSL certificate validation entirely disabled**
`OkHttpClientFactory.getOkHttpClient()` (line 16) calls `FakeX509TrustManager.getUnsafeSSLContext()` and passes the resulting context to `builder.sslSocketFactory()`. `FakeX509TrustManager` implements `X509TrustManager` with empty `checkClientTrusted` and `checkServerTrusted` method bodies (lines 26–33 of `FakeX509TrustManager.java`). Neither method throws `CertificateException` under any condition. Every TLS certificate presented by any server is silently accepted.

This OkHttp client is used directly by the APK update mechanism. An on-path attacker can present any certificate, intercept the HTTPS connection, and serve a malicious APK that will be downloaded and offered for installation.

**CRITICAL — Hostname verification entirely disabled**
`OkHttpClientFactory.getOkHttpClient()` (lines 18–24) installs a `HostnameVerifier` that unconditionally returns `true` for every hostname/session pair. The Android Studio lint suppression annotation `@SuppressLint("BadHostnameVerifier")` confirms the developer was aware this is flagged by tooling. Combined with the disabled certificate validation, TLS provides no server authentication whatsoever for the APK download flow.

**CRITICAL — `FakeX509TrustManager.allowAllSSL()` also disables validation globally**
`FakeX509TrustManager` (lines 67–78) contains a static method `allowAllSSL()` that sets the JVM-wide defaults on `HttpsURLConnection` — `setDefaultHostnameVerifier` and `setDefaultSSLSocketFactory`. If this method is called anywhere in the application lifecycle (not confirmed in these three files but the method exists in production code), all HTTPS connections made by the app, including those not using OkHttp, would be affected.

**HIGH — APK download URL is server-controlled with no client-side validation**
`APKUpdateService.downloadPackage(@Url String packageUrl)` passes the URL directly to Retrofit as a `@Url` parameter, replacing the base URL entirely. The URL value originates from `APKPackage.url`, which is deserialized from the server JSON response. There is no scheme check (e.g., enforcing `https://`), no hostname allowlist, and no path validation in the client code. If the server is compromised, or if the update-check endpoint is spoofed (facilitated by the disabled TLS validation above), an attacker can direct the download to an arbitrary URL including `http://` addresses or internal network addresses.

**FINDING — Hardcoded server addresses for dev and UAT environments**
`app/build.gradle` lines 74 and 80 embed explicit infrastructure addresses:
- `dev`: `https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws`
- `uat`: `https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws`

These expose environment topology. The UAT address is a raw AWS EC2 public DNS name, which may change with instance restarts.

**FINDING — No `network_security_config.xml` present**
No network security configuration file was found. The app relies on Android platform defaults. Given the use of `FakeX509TrustManager`, a custom security config would be insufficient to address the issue, but its absence also means no certificate pinning for the APK update server is configured.

**FINDING — `android:usesCleartextTraffic` not explicitly set**
`AndroidManifest.xml` does not set `android:usesCleartextTraffic`. For `targetSdkVersion 26`, the default is `true`, meaning cleartext HTTP traffic is permitted. Given that `downloadPackage` accepts arbitrary URLs from the server without scheme enforcement, HTTP download of an APK is possible.

---

### 3. Data Storage

**HIGH — APK downloaded to public external storage**
`ShowPackageAvailable.java` line 125:
```java
final File apkPackageFile = new File(
    Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
        .getAbsolutePath() + "/" + apkPackage.getFileName()
);
```
`Environment.getExternalStoragePublicDirectory(DIRECTORY_DOWNLOADS)` is a world-readable location. Any other app on the device holding `READ_EXTERNAL_STORAGE` can read the downloaded APK file. More critically, a malicious app holding `WRITE_EXTERNAL_STORAGE` can overwrite the file after it is written and before the user taps the install notification, replacing a legitimate APK with a malicious one (TOCTOU / file substitution attack). There is no integrity check performed on the written file before installation is offered.

**HIGH — No APK integrity verification before installation offer**
`writeResponseBodyToDisk` (lines 143–150) writes the downloaded bytes directly to disk. After writing, `raiseNotificationPackageReadyToInstall` immediately raises an install prompt. There is no hash comparison, no signature verification, and no check that the written bytes match an expected checksum supplied by the server. Combined with the disabled TLS validation, an attacker who intercepts or replaces the download can deliver arbitrary code.

**FINDING — `android:allowBackup="true"` set in `AndroidManifest.xml`**
`AndroidManifest.xml` line 18: `android:allowBackup="true"`. For a forklift management app that stores operator credentials and session data, this permits full extraction of the app's data directory via ADB backup on a USB-connected device without root access.

**No issues found** — No `MODE_WORLD_READABLE` or `MODE_WORLD_WRITEABLE` in `openFileOutput()` calls within the audited files. No use of `Environment.getExternalStorageDirectory()` directly (public Downloads subdirectory is used instead, which is still public).

**No issues found** — No credentials or session tokens are stored in the three audited files. Storage of authentication material is outside the scope of these specific files.

---

### 4. Input and Intent Handling

**FINDING — `ShowPackageAvailable` is the LAUNCHER activity with no explicit `android:exported` declaration**
`AndroidManifest.xml` lines 91–98 register `ShowPackageAvailable` with an `<intent-filter>` but without `android:exported="true"` or `android:exported="false"`. On Android 12+ (API 31+), activities with intent filters must explicitly declare `exported`. For the `targetSdkVersion 26` declared here, the implicit export still applies. Any app on the device can start this activity. Because `onStart()` immediately calls the update service and can then trigger APK download and install, any third-party app starting this activity would initiate the update check flow. The impact is limited by the fact that a user prompt is required to install the APK, but the download to public storage occurs without user interaction.

**FINDING — `onRequestPermissionsResult` retrieves `APKPackage` via `getSerializableExtra` on an intent that could be externally supplied**
`ShowPackageAvailable.java` line 180:
```java
downloadAndInstall((APKPackage) getIntent().getSerializableExtra(PACKAGE_EXTRA));
```
The intent that started the activity is used to retrieve the `APKPackage` object. If the activity is started by a third-party app (see exported finding above) with a crafted `APKPackage` serializable extra containing an attacker-controlled `url` and `fileName`, and the user has already granted storage permissions, the activity will download from and save to attacker-specified locations when permissions are granted. This is an intent-based injection of the download URL.

**FINDING — `raiseNotificationPackageReadyToInstall` uses `Uri.fromFile` (deprecated for API 24+)**
`ShowPackageAvailable.java` line 160:
```java
notificationIntent.setDataAndType(Uri.fromFile(apkPackageFile), ANDROID_APK_MIME_TYPE);
```
`Uri.fromFile` is blocked by `FileProvider` requirements on Android 7.0+ (API 24+). On devices running API 24+, tapping the notification will fail with a `FileUriExposedException` unless the `FileProvider` declared in the manifest is used. The `FileProvider` is declared (manifest line 24–32), but it is not used here for the install intent.

**FINDING — `PendingIntent` created without `FLAG_IMMUTABLE`**
`ShowPackageAvailable.java` line 161:
```java
PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, notificationIntent, 0);
```
The flags parameter is `0`. Android 12+ (API 31+) requires `PendingIntent.FLAG_IMMUTABLE` or `FLAG_MUTABLE` to be explicitly set. Without `FLAG_IMMUTABLE`, a malicious app may be able to modify the pending intent before it is dispatched.

**No issues found** — No WebView usage or deep link handlers were found in the three audited files.

---

### 5. Authentication and Session

No issues found in the audited files — Authentication and session management logic is not present in `ShowPackageAvailable.java`, `APKPackage.java`, or `APKUpdateService.java`. The `TokenAuthenticator` installed in `OkHttpClientFactory` handles re-authentication for the OkHttp client but was not in scope for this pass.

---

### 6. Third-Party Libraries

**FINDING — Retrofit 2.5.0 is significantly out of date**
`app/build.gradle` line 100: `com.squareup.retrofit2:retrofit:2.5.0`. Current version as of audit date is 2.11.x. Version 2.5.0 was released in January 2019. Outdated networking library in direct contact with APK download logic.

**FINDING — OkHttp version is not pinned independently**
No direct OkHttp dependency is declared in `app/build.gradle`. OkHttp is pulled in transitively by Retrofit 2.5.0, which pins to OkHttp 3.x. OkHttp 3.x reached end-of-life. Current production version is OkHttp 4.x.

**FINDING — Android Support Library (`com.android.support:*` at version `26.0.2`) is used instead of AndroidX**
`app/build.gradle` lines 104–107 reference `com.android.support:appcompat-v7:26.0.2`, `recyclerview-v7`, `support-v4`, `multidex`, and `cardview-v7`. The Android Support Library was superseded by AndroidX in 2018. Support library version 26.0.2 is from 2017 and receives no security updates.

**FINDING — `minifyEnabled false` for release builds**
`app/build.gradle` line 52: `minifyEnabled false`. Code obfuscation (R8/ProGuard) is explicitly disabled for release builds. All class names, method names, and string literals are preserved in the release APK. This facilitates reverse engineering, including discovery of the hardcoded server URLs and the `FakeX509TrustManager` class.

**FINDING — `proguard-rules.pro` is effectively empty**
The `app/proguard-rules.pro` file contains only commented-out template text and no active rules. Given `minifyEnabled false`, this has no current effect, but confirms no obfuscation strategy is in place.

**FINDING — `google-play-services-location:11.8.0` is outdated**
`app/build.gradle` line 109: `com.google.android.gms:play-services-location:11.8.0`. This version is from 2017. Current Play Services releases are in the 21.x range.

**FINDING — `realm-gradle-plugin:3.7.2` is significantly outdated**
Declared in root `build.gradle` line 10. Realm 3.7.2 dates to 2017. Realm Mobile Platform has undergone substantial security and API changes since this version.

**FINDING — `jcenter()` repository is used**
Root `build.gradle` lines 6 and 19 include `jcenter()`. JCenter was shut down in February 2022. New artifact requests fail, but cached/mirrored artifacts may still resolve. Continued reliance on JCenter is a supply-chain risk: it should be replaced with `mavenCentral()`.

---

### 7. Google Play and Android Platform

**FINDING — `targetSdkVersion 26` does not meet current Google Play requirements**
Root `build.gradle` line 27: `myTargetSdkVersion=26` (Android 8.0, Oreo). Google Play requires `targetSdkVersion` 34 or higher for new app submissions and updates. This app cannot be published or updated on Google Play in its current configuration.

**FINDING — `minSdkVersion 21` with deprecated `AsyncTask`-era patterns**
`minSdkVersion 21` (Android 5.0). Given `targetSdkVersion 26`, `AsyncTask` (deprecated at API 30) may be in use elsewhere in the codebase. The autoupdate files use Retrofit callbacks rather than `AsyncTask`, so no direct issue within these three files. However, the `android.support.v4.app.ActivityCompat` import at line 16 of `ShowPackageAvailable.java` uses the legacy Support Library rather than AndroidX, consistent with the API 26 target.

**FINDING — `WRITE_EXTERNAL_STORAGE` and `READ_EXTERNAL_STORAGE` are declared and requested at runtime**
`AndroidManifest.xml` lines 7–8 declare both permissions. `ShowPackageAvailable.java` lines 108–114 request them at runtime via `ActivityCompat.requestPermissions`. This is correct procedure for `minSdkVersion 21`; however, `WRITE_EXTERNAL_STORAGE` has no effect on Android 10+ (API 29+) when writing to scoped storage. The implementation uses `getExternalStoragePublicDirectory`, which on Android 10+ in legacy mode still works when `android:requestLegacyExternalStorage` is set, but the manifest does not include that attribute. Behaviour on API 29+ devices may be inconsistent.

**FINDING — `BLUETOOTH_ADMIN` permission is declared**
`AndroidManifest.xml` line 11: `android:name="android.permission.BLUETOOTH_ADMIN"`. On Android 12+ (API 31+), `BLUETOOTH_ADMIN` is replaced by `BLUETOOTH_CONNECT` and `BLUETOOTH_SCAN`. With `targetSdkVersion 26`, the legacy permissions are still used, but forward compatibility is broken.

**No issues found** — No WebView, deep link handlers, or `ContentProvider` with exported access were found in the audited files. The `FileProvider` in the manifest is correctly declared with `android:exported="false"`.

---

## Summary of Findings

| Severity | Count | Issues |
|---|---|---|
| Critical | 4 | Keystore files committed; passwords in `gradle.properties`; SSL validation disabled; hostname verification disabled |
| High | 4 | APK download to public external storage with no integrity check; server-controlled download URL with no validation; intent-based URL injection via exported launcher activity; `android:allowBackup="true"` |
| Medium | 7 | `Uri.fromFile` use on API 24+; `PendingIntent` without `FLAG_IMMUTABLE`; APK Signature Scheme v2 disabled; `minifyEnabled false`; `targetSdkVersion 26`; `allowAllSSL()` global override method exists in production code; no network security config |
| Low / Informational | 8 | Outdated Retrofit, OkHttp, Support Library, Play Services, Realm; `jcenter()` repo; hardcoded dev/UAT hostnames; `BLUETOOTH_ADMIN` forward-compat |

The most severe risk chain in the audited files is: disabled TLS validation + disabled hostname verification + server-controlled download URL + no APK integrity verification + public external storage write = an attacker with network access can replace the APK being served and cause the app to offer installation of arbitrary code with no cryptographic protection at any layer of the download pipeline.
