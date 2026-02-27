# Pass 1 Security Audit — Agent APP60
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SignupLoadingFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/UniversityGuideFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/UserPhotoFragment.java`

---

## Branch Verification

**Result:** PASS — current branch is `master`.

**Discrepancy noted:** The checklist header states `Branch: main`, but the actual default branch is `master`. This is a documentation inconsistency only; the audit proceeds on `master` as instructed.

---

## Reading Evidence

### 1. SignupLoadingFragment.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.fragment.SignupLoadingFragment`

**Superclass / interfaces:** extends `FleetFragment`, implements `View.OnClickListener`

**Fields and constants:**
- `LoginActivity activity` — package-private instance field (line 24)
- `private ImageView loadingIV` — (line 25)
- `private int[] loadingResIds` — array of 15 drawable resource IDs (line 47)
- `private static boolean loginFinished` — static, shared across instances (line 51)
- `private static int runTime` — static, shared across instances (line 52)

**Public methods (with line numbers):**
- `public View onCreateView(@NonNull LayoutInflater, @Nullable ViewGroup, @Nullable Bundle)` — line 28
- `public void onActivityCreated(Bundle)` — line 35
- `public void initViews()` — line 41
- `public void onResume()` — line 122
- `public void onStop()` — line 129
- `public void onDestroy()` — line 134
- `public void onClick(View)` — line 139

**Private methods:**
- `private void timerHandle()` — line 54
- `private void onLoginSucceed()` — line 79
- `private void loadingLoginHandle()` — line 85
- `private void showDashboard()` — line 111

---

### 2. UniversityGuideFragment.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.fragment.UniversityGuideFragment`

**Superclass:** extends `FleetFragment`

**Fields and constants:** none declared in this class

**Public methods (with line numbers):**
- `public View onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle)` — line 21
- `public void initViews()` — line 26
- `public void onResume()` — line 49
- `public void onPause()` — line 54

**Key behaviour:** `initViews()` constructs a URL via `URLBuilder.urlGetUniversity(MyCommonValue.currentEquipmentItem.id)` — which resolves to `https://pandora.fleetiq360.com/pandora/uni?id=<equipmentId>` — and passes it as a plain string extra to `WebActivity` via an explicit `Intent`. `WebActivity` (LibCommon) loads that URL into a WebView with `setJavaScriptEnabled(true)` and no URL whitelist validation.

---

### 3. UserPhotoFragment.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.fragment.UserPhotoFragment`

**Note:** Despite the name, this is **not** a Fragment subclass. It is a plain utility class with no superclass.

**Fields and constants:**
- `protected static final String TAG = "NukeSSLCerts"` — on inner class `SSLCertificateHandler` (line 38)

**Public methods (with line numbers):**
- `public static void nuke()` — on `SSLCertificateHandler` (line 41)

**Package-private methods:**
- `static void showUserPhoto(final ImageView imageView)` — line 18

**Inner class:** `public static class SSLCertificateHandler` — line 37

---

## Findings by Checklist Section

### 1. Signing and Keystores

No signing configuration, keystore files, or pipeline files are referenced or present in the three assigned files.

No issues found — Section 1.

---

### 2. Network Security

#### CRITICAL — Global SSL Certificate Validation Disabled
**File:** `UserPhotoFragment.java`, lines 37–69
**Class:** `UserPhotoFragment.SSLCertificateHandler`

`SSLCertificateHandler.nuke()` installs a custom `X509TrustManager` whose `checkClientTrusted()` and `checkServerTrusted()` methods have **empty bodies** — they perform no certificate validation whatsoever. The method then:

1. Initialises an `SSLContext` with the trust-all `TrustManager` and sets it as the **default** SSL socket factory via `HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())` (line 59). This affects **every** HTTPS connection made by the application for the remainder of the process lifetime, not just image loading.
2. Installs a `HostnameVerifier` via `HttpsURLConnection.setDefaultHostnameVerifier(...)` that **always returns `true`** regardless of the hostname or session (line 60–65). This completely disables hostname verification globally.

The `@SuppressLint("TrustAllX509TrustManager")` and `@SuppressLint("BadHostnameVerifier")` annotations on lines 40 and 61 confirm the developer was aware Android Lint flagged these as dangerous and explicitly suppressed the warnings.

`nuke()` is called from `showUserPhoto()` every time a user photo is displayed (line 30). After the first call, all subsequent HTTPS traffic — including authentication against forkliftiqws, session tokens, operator data, telemetry — is subject to man-in-the-middle attack because certificate and hostname validation have been permanently disabled for the process.

**Severity: Critical**

**Checklist reference:** Section 2 — "Check for `TrustAllCertificates` implementations, `hostnameVerifier` overrides that return `true`, or `SSLContext` initialized with a permissive `TrustManager` — these disable certificate validation entirely."

---

#### MEDIUM — WebView JavaScript Enabled, No URL Whitelist
**Files:** `UniversityGuideFragment.java` (line 33–34) and `WebActivity.java` (line 43)

`UniversityGuideFragment.initViews()` constructs a URL using `URLBuilder.urlGetUniversity(MyCommonValue.currentEquipmentItem.id)`, which builds the string `https://pandora.fleetiq360.com/pandora/uni?id=<int>`, and passes it to `WebActivity` as an Intent string extra. `WebActivity.initWebView()` calls `webView.getSettings().setJavaScriptEnabled(true)` (line 43) with no URL validation before calling `webView.loadUrl(url)` (line 84).

Two concerns:

1. **No URL whitelist validation.** The URL is accepted directly from the Intent extra without checking that it begins with the expected origin (`pandora.fleetiq360.com`). Any component that can send an Intent to `WebActivity` could supply an arbitrary URL, including a `file://` URL or an attacker-controlled domain (relevant if `WebActivity` is exported or reachable via deep links).

2. **JavaScript enabled in WebView loading an external URL.** If the remote page at `pandora.fleetiq360.com` were ever compromised or redirected, JavaScript would execute in the context of the WebView. No `addJavascriptInterface` was observed, which limits the attack surface, but the combination of JavaScript + no URL whitelist is still a concern.

`shouldOverrideUrlLoading()` in `WebActivity` always returns `false` (line 61), meaning all navigations — including any redirects from the initial URL — proceed within the same WebView without validation.

**Severity: Medium**

**Checklist reference:** Section 2 (WebView / checklist Section 4) — "Are URLs loaded into WebView validated against a whitelist?"

---

#### LOW — Hardcoded URL for Pre-Start Help and University Guide
**File:** `URLBuilder.java`, line 26

```java
final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora";
```

This URL is hardcoded and shared between `urlGetDiagnosis()` and `urlGetUniversity()`. It is distinct from the main `BASE_URL` (which is sourced from `BuildConfig`) and is not configurable per build flavour. While the domain is HTTPS and does not represent an immediate vulnerability, hardcoded secondary base URLs should be managed through build configuration to allow environment-specific overrides.

**Severity: Low**

**Checklist reference:** Section 2 — "Check for hardcoded API endpoints, server URLs, or IP addresses in source files."

---

### 3. Data Storage

#### MEDIUM — Static Fields Retain Login Credentials in Memory
**File:** `CurrentUser.java`, lines 21–24 (called from `SignupLoadingFragment.java`)

The `CurrentUser` class stores credentials in static fields:

```java
private static String loginEmail;    // line 22
private static String loginPassword; // line 23
```

These are set by `setTemporaryLoginInformation()` and are accessed during `SignupLoadingFragment.loadingLoginHandle()` via `CurrentUser.login(loginHandler)`. The password is MD5-hashed before storage (line 122 of `CurrentUser`), but MD5 is cryptographically broken for password hashing and trivially reversible for common passwords.

More critically, neither field is cleared after a successful or failed login. They remain in the static heap for the lifetime of the process. If a second operator logs in (shift change), the previous operator's email and hashed password remain accessible in static memory until they are overwritten. The `logout()` method (line 125) clears `user` and the SharedPreferences key, but does **not** clear `loginEmail` or `loginPassword`.

**Severity: Medium**

**Checklist reference:** Section 3 — "Check for operator credentials cached in memory beyond their useful lifetime (e.g. stored in a static field on the Application class)." Also Section 5 — "verify that one operator's data is fully cleared before another operator logs in."

---

No issues found in the three assigned files for: external storage usage, `MODE_WORLD_READABLE`/`MODE_WORLD_WRITEABLE`, `allowBackup` (declared in Manifest, not these files), or direct SQLite/file writes.

---

### 4. Input and Intent Handling

#### LOW — Implicit Intent Risk: Equipment ID from Static Global Field
**File:** `UniversityGuideFragment.java`, line 33

```java
intent.putExtra(WebActivity.URL_KEY, URLBuilder.urlGetUniversity(MyCommonValue.currentEquipmentItem.id).url);
```

`MyCommonValue.currentEquipmentItem` is a `public static` field. Its `id` is embedded directly into the URL passed to `WebActivity`. If `currentEquipmentItem` is null at the point `initViews()` runs, this line will throw a `NullPointerException`. There is no null guard before the field access.

**Severity: Low** (null-pointer / defensive programming concern; the equipment ID is an integer and is appended via `Uri.Builder`, which prevents injection)

---

#### NOTE — WebView URL Not Validated (see Section 2 above for full detail)

No issues found for: exported components (not declared in these files), deep link handlers, or implicit intents carrying session tokens (the Intent carries only a URL string, not a token).

---

### 5. Authentication and Session

#### MEDIUM — MD5 Used for Password Hashing
**File:** `CurrentUser.java`, lines 82 and 122 (called indirectly via `SignupLoadingFragment`)

`CommonFunc.MD5_Hash()` is applied to both the email (line 82) and the password (line 122). MD5 is not a suitable password hashing algorithm — it is not a key derivation function, has no salt, and is computationally trivial to reverse for common passwords via rainbow tables. If the hashed password is transmitted over the network or stored, it provides minimal protection beyond plaintext.

**Severity: Medium**

**Checklist reference:** Section 5 — "Check how the app authenticates with forkliftiqws. Verify tokens or credentials are stored securely."

---

#### LOW — Logout Does Not Clear Static Credential Fields
**File:** `CurrentUser.java`, lines 125–128 (called from `SignupLoadingFragment` flow)

As described in Section 3: `logout()` clears `user` and the SharedPreferences key but does not null `loginEmail` or `loginPassword`. The credential fields persist in static memory post-logout.

**Severity: Low** (overlaps with Section 3 / Medium finding above; noted separately for the authentication section)

No issues found for: token expiry handling (not visible in these three files) or `EncryptedSharedPreferences` (SharedPreferences usage is in `ModelPrefs`, outside the three assigned files).

---

### 6. Third-Party Libraries

The three assigned files import the following third-party libraries relevant to this section:

- **Universal Image Loader** (`com.nostra13.universalimageloader`) — `UserPhotoFragment.java` lines 8–10. This library is **abandoned** (last release 1.9.5 in 2015; no updates in over 10 years). It has no active maintainer and is not patched for any vulnerabilities discovered since 2015. Its use here is particularly concerning because it is used alongside the SSL-nuking code to load user photos.
- **`com.yy.libcommon`** — an internal library (`LibCommon` module within this repo). `WebActivity` is part of this library.

**Severity: Medium** (abandoned library — Universal Image Loader)

**Checklist reference:** Section 6 — "Check for abandoned libraries (no updates in 2+ years). The codebase is noted to include ... ImageLoader ... — verify current versions and CVE status for each."

No issues found for: ProGuard/R8 configuration (not in these files).

---

### 7. Google Play and Android Platform

#### LOW — `onActivityCreated` Deprecated
**File:** `SignupLoadingFragment.java`, line 35

`Fragment.onActivityCreated(Bundle)` is deprecated as of API level 28. The checklist notes deprecated API usage as a concern for the declared `targetSdkVersion`.

**Severity: Low**

---

#### LOW — Raw Thread Used Instead of Modern Concurrency
**File:** `SignupLoadingFragment.java`, lines 55–76

`timerHandle()` spawns a raw `new Thread(...)` with a `while(true)` loop that sleeps for 100ms. The thread has no explicit termination mechanism tied to the Fragment lifecycle — it terminates only when `loginFinished` becomes `true`. The static nature of `loginFinished` and `runTime` means if a second `SignupLoadingFragment` is created while the first thread is still running, both threads will share and concurrently write to these static fields without synchronisation, creating a data race.

**Severity: Low** (Android platform / quality concern, not a direct security vulnerability, but static mutable state shared across instances is a relevant observation for the session-isolation checklist requirement)

---

No issues found in the three assigned files for: runtime permission requests, explicit permission declarations (in Manifest), or `targetSdkVersion`/`minSdkVersion` (in Gradle files, outside scope).

---

## Summary Table

| Severity | Count | Finding |
|----------|-------|---------|
| Critical | 1 | Global SSL/TLS certificate and hostname validation disabled (`SSLCertificateHandler.nuke()`) |
| Medium | 3 | WebView with JavaScript enabled and no URL whitelist; Static credential fields not cleared on logout; Abandoned Universal Image Loader library; MD5 used for password hashing |
| Low | 4 | Hardcoded secondary base URL; Null-dereference risk on `currentEquipmentItem`; `onActivityCreated` deprecated; Unsynchronised static fields in `timerHandle()` |

---

## Files Reviewed

| File | Lines |
|------|-------|
| `SignupLoadingFragment.java` | 141 |
| `UniversityGuideFragment.java` | 58 |
| `UserPhotoFragment.java` | 71 |
| `URLBuilder.java` | 466 (supporting evidence) |
| `WebActivity.java` | 86 (supporting evidence) |
| `CurrentUser.java` | 129 (supporting evidence) |
| `MyCommonValue.java` | 18 (supporting evidence) |
| `User.java` | 182 (supporting evidence) |
