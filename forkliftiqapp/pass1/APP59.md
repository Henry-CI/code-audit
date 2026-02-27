# Pass 1 Security Audit — APP59
**Agent:** APP59
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** Checklist specifies `Branch: main`. Actual branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SetUserPhotoFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SetupEmailFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SignupFragment.java`

Supporting files read for context:
- `WebService/URLBuilder.java`
- `WebService/WebData.java`
- `WebService/ImagePostBackgroundTask.java`
- `WebService/webserviceclasses/parameters/UserRegisterParameter.java`
- `util/CommonFunc.java`
- `model/ModelPrefs.java`
- `ui/fragment/DashboardFragment.java` (partial — static field)

---

## Step 3 — Reading Evidence

### File 1: SetUserPhotoFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.SetUserPhotoFragment`

**Extends / Implements:**
`FleetFragment`, `View.OnClickListener`

**Fields / Constants:**
| Line | Modifier | Type | Name |
|------|----------|------|------|
| 24 | package-private | `Activity` | `activity` |
| 25 | private | `Bitmap` | `mBitmap` (initialized `null`) |
| 26 | private | `ImageView` | `user_photo` |
| 27 | private | `ImageView` | `user_photo_none` |
| 28 | package-private | `boolean` | `fromDashboard` (default `false`) |

**Public methods (and overrides with line numbers):**
| Line | Signature |
|------|-----------|
| 31 | `public View onCreateView(LayoutInflater, ViewGroup, Bundle)` |
| 37 | `public void onActivityCreated(Bundle)` |
| 45 | `public void initViews()` |
| 180 | `public void onResume()` |
| 185 | `public void onStop()` |
| 190 | `public void onDestroy()` |
| 195 | `public void onClick(View)` |

**Private methods:**
| Line | Signature |
|------|-----------|
| 98 | `private void getUserDetail()` |
| 102 | `private void onPhotoSaved()` |
| 115 | `private void uploadUserPhoto()` |
| 148 | `private void choosePhoto()` |

**Key observations:**
- Line 126: `URLBuilder.urlUploadUserPhoto(WebData.instance().getUserId())` — user photo upload URL built via `URLBuilder`, which uses `BuildConfig.BASE_URL` (not hardcoded in this file).
- Line 132: `ImagePostBackgroundTask.uploadImage(urlItem.url, mBitmap, ...)` — uses `AsyncTask` (deprecated API 30+).
- Line 157: `AndroidImagePicker.getInstance().pickAndCrop(...)` — third-party image picker library used.
- Line 165–166: `DashboardFragment.userPhotoBitmap = mBitmap` — bitmap assigned to a static field on `DashboardFragment`. This field is package-private/static; the bitmap is cleared after display (confirmed in `DashboardFragment` line 49).

---

### File 2: SetupEmailFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.SetupEmailFragment`

**Extends / Implements:**
`FleetFragment`, `View.OnClickListener`

**Fields:**
| Line | Modifier | Type | Name |
|------|----------|------|------|
| 32 | package-private | `SignupActivity` | `activity` |
| 33 | private | `boolean` | `mFromDashboard` (default `false`) |
| 91 | private | `GetEmailResult` | `getEmailResult` |

**Public methods (and overrides with line numbers):**
| Line | Signature |
|------|-----------|
| 35 | `public static SetupEmailFragment createInstance(boolean)` |
| 42 | `public View onCreateView(LayoutInflater, ViewGroup, Bundle)` |
| 49 | `public void onActivityCreated(Bundle)` |
| 57 | `public void initViews()` |
| 207 | `public void onResume()` |
| 211 | `public void onStop()` |
| 215 | `public void onDestroy()` |
| 222 | `public void onClick(View)` |

**Private methods:**
| Line | Signature |
|------|-----------|
| 93 | `private void loadData()` |
| 112 | `private void onEmailLoaded()` |
| 124 | `private void saveEmail()` |
| 195 | `private void onSaved()` |

**Key observations:**
- Lines 95, 169: API calls via `WebApi.async().getEmails(...)` and `WebApi.async().setupEmails(...)` — use backend user ID from `WebData.instance().getUserId()`.
- Line 163: Email address parameters read directly from `TextView` widgets — no sanitisation or format validation applied before sending to backend.
- Line 200: `startActivity(new Intent(getContext(), DashboardActivity.class))` — explicit intent, no sensitive data in extras.

---

### File 3: SignupFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.SignupFragment`

**Extends / Implements:**
`FleetFragment`, `View.OnClickListener`

**Fields / Constants:**
| Line | Modifier | Type | Name |
|------|----------|------|------|
| 31 | package-private | `SignupActivity` | `activity` |
| 32 | private | `EditText` | `firstNameET, lastNameET, emailAddressET, mobileNumET, passwordET, confirmPWET` |
| 33 | private | `TextView` | `sign_up_group_choice_id` |
| 86 | private static final | `String` | `TYPE_DRIVER = "DRIVER"` |
| 87 | private static final | `String` | `TYPE_COMPANY = "COMPANY"` |

**Public methods (and overrides with line numbers):**
| Line | Signature |
|------|-----------|
| 36 | `public View onCreateView(LayoutInflater, ViewGroup, Bundle)` |
| 43 | `public void onActivityCreated(Bundle)` |
| 50 | `public void initViews()` |
| 204 | `public void onClick(View)` |

**Private methods:**
| Line | Signature |
|------|-----------|
| 89 | `private void showGroupType()` |
| 112 | `private void register()` |

**Password and credential handling in `register()` (lines 112–201):**
- Line 118: `String passwordStr = passwordET.getText().toString()` — password extracted as a `String` object. Java `String` objects are immutable and remain in heap memory until garbage collected; they cannot be zeroed after use. A `char[]` would allow explicit clearing.
- Line 119: `String pp = confirmPWET.getText().toString()` — confirm password extracted as a `String`.
- Line 146: `CommonFunc.isPasswordValid(passwordStr)` — validation is only performed for `TYPE_COMPANY` users (line 146). `TYPE_DRIVER` users have the password field hidden (`View.INVISIBLE`, line 103) but the field is never cleared. If a user switches from COMPANY to DRIVER after entering a password, the password value remains in `passwordStr` and is sent to the backend in `userRegisterParameter.password` (line 196).
- `CommonFunc.isPasswordValid()` (line 92–94 of `CommonFunc.java`): checks only that password is non-null and non-empty. No minimum length, no complexity requirements.
- Lines 192–200: `UserRegisterParameter` populated with `passwordStr` (plain text String) and passed to `WebApi.async().register(...)`. The password is serialised to JSON and transmitted over the network.
- No hashing or pre-transmission transformation of the password is performed at the client side — it is sent as plain text in the JSON request body. Whether transport-layer encryption is applied depends on the URL scheme in `BuildConfig.BASE_URL`, which was not verified in this file set.

---

## Step 4 — Supporting File Findings

### WebData.java — Hardcoded OAuth credentials (Critical)

Lines 59–77 of `WebData.java` (method `getTokenFormData()`):

```java
String clientId = "987654321";
String clientSecret = "8752361E593A573E86CA558FFD39E";
String userName = "gas";
String password = "ciiadmin";
```

These are hardcoded OAuth2 client credentials and a service account username/password in source code. Any attacker with access to the APK or repository can extract these values. This directly affects all three assigned fragments because they all call backend APIs authenticated via this token mechanism.

### WebData.java — Token stored in plain SharedPreferences

Line 93: `ModelPrefs.saveObject(TOKEN_ITEM_KEY, result)` — the OAuth bearer token is serialised as JSON and saved to plain (unencrypted) `SharedPreferences` via `ModelPrefs`. `ModelPrefs.java` uses `Context.MODE_PRIVATE` (line 17), which is correct for file system access control but provides no encryption. On rooted devices or via ADB backup (if `android:allowBackup` is true), this token can be extracted.

### CommonFunc.java — Weak password validation

`isPasswordValid()` at line 92–94 accepts any non-empty string. There is no minimum length, no character class requirement. This directly affects `SignupFragment.register()` at line 146.

### ImagePostBackgroundTask.java — Deprecated AsyncTask

Line 15: `extends AsyncTask<...>` — `AsyncTask` was deprecated in API level 30 (Android 11). This is used in `SetUserPhotoFragment.uploadUserPhoto()` via `ImagePostBackgroundTask.uploadImage()`.

### URLBuilder.java — Hardcoded third-party URL

Line 26: `final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora"` — this URL is hardcoded and not pulled from `BuildConfig`. This is a secondary endpoint used for pre-start help and university content. Not directly invoked by the three assigned fragments but relevant to the overall network security posture.

Line 171, 355 (comments): `//Uri.Builder builder = Uri.parse("https://192.168.1.7/fleetiq360ws/rest").buildUpon();` — commented-out local development IP address remains in source code. Not active but indicates development infrastructure exposure.

---

## Step 5 — Findings by Checklist Section

### 1. Signing and Keystores

No `.jks`, `.keystore`, or `.p12` files are referenced by the three assigned files. `URLBuilder.java` uses `BuildConfig.BASE_URL`, suggesting the base URL is injected at build time. Signing configuration not visible in assigned files.

**No issues found — Signing and Keystores** (from the scope of assigned files).

---

### 2. Network Security

**FINDING — NS-01 — Medium**
`URLBuilder.java` line 26 contains a hardcoded secondary endpoint: `https://pandora.fleetiq360.com/pandora`. The scheme is HTTPS, so this is not plaintext. However, hardcoding an endpoint for an external production service in source code removes the ability to rotate or redirect the URL without a code change and re-release.

**FINDING — NS-02 — Informational**
`URLBuilder.java` lines 171 and 355 contain commented-out `https://192.168.1.7/...` local development IP addresses. These are not active but expose internal development infrastructure details.

**FINDING — NS-03 — Requires further verification (out of scope for assigned files)**
The primary base URL is `BuildConfig.BASE_URL`. The scheme (HTTP vs HTTPS) cannot be confirmed from the assigned files alone. The protocol used for `register()`, photo upload, and email operations depends on this value. Whether HTTPS is enforced must be confirmed in `build.gradle` or `BuildConfig` source (not assigned).

**FINDING — NS-04 — Critical (from supporting file WebData.java)**
Hardcoded OAuth client credentials (`clientId`, `clientSecret`, `userName`, `password`) in `WebData.getTokenFormData()` at lines 59–77. These credentials authenticate the app-level service account against `forkliftiqws`. All three assigned fragments rely on API calls backed by this authentication mechanism. Any actor who decompiles the APK gains permanent access to these backend credentials.

---

### 3. Data Storage

**FINDING — DS-01 — High**
The OAuth bearer token is persisted to plain (unencrypted) `SharedPreferences` via `ModelPrefs.saveObject("token_result", result)` (`WebData.java` line 93, `ModelPrefs.java` line 53–58). `ModelPrefs` uses `Context.MODE_PRIVATE` but does not use `EncryptedSharedPreferences`. On a rooted device or via ADB backup, this token is extractable.

**FINDING — DS-02 — Medium**
`SignupFragment.register()` stores the user's plaintext password in a `java.lang.String` at line 118. Java `String` objects are immutable and cannot be explicitly zeroed. The password value remains in heap memory until GC collects it and the memory is overwritten. Using a `char[]` (which can be zeroed with `Arrays.fill`) would reduce the exposure window. This is a well-known Android/Java security guidance item (OWASP MSTG-STORAGE-10).

**FINDING — DS-03 — Low**
`SetUserPhotoFragment` writes the captured bitmap to a static field `DashboardFragment.userPhotoBitmap` (line 166 of `SetUserPhotoFragment.java`). Static fields on Fragment/Activity classes persist for the lifetime of the process. The bitmap is cleared after first display (`DashboardFragment` line 49 sets it to `null`), which mitigates the risk. However, the static exposure window between photo capture and dashboard display is uncontrolled.

No issues found with external storage, `MODE_WORLD_READABLE/WRITEABLE`, or SD card writes in the assigned files.

---

### 4. Input and Intent Handling

**FINDING — IH-01 — Low**
`SetupEmailFragment.saveEmail()` at lines 163–166 reads email addresses directly from `TextView` widgets and sends them to the backend without any format validation. The `getEmails` response pre-populates these fields, so the risk is limited to a user submitting a malformed email address that the backend must reject. No server-side rejection error handling causes a silent failure.

No WebView usage found in the three assigned files.
No deep link handlers in the assigned files.
`SetupEmailFragment.onSaved()` line 200 uses an explicit intent (`DashboardActivity.class`) — no implicit intent exposure.

---

### 5. Authentication and Session

**FINDING — AU-01 — Critical (from supporting WebData.java)**
Hardcoded service account credentials (`userName = "gas"`, `password = "ciiadmin"`) in `WebData.getTokenFormData()`. These authenticate the app to the OAuth token endpoint. All API calls from all three assigned fragments flow through this authentication path.

**FINDING — AU-02 — Medium**
`CommonFunc.isPasswordValid()` referenced by `SignupFragment.register()` line 146 accepts any non-empty string. A password of a single character passes validation. No minimum length, no complexity, no breach/common-password check. This is the only password complexity gate in the signup flow for COMPANY-type users.

**FINDING — AU-03 — Low**
In `SignupFragment.register()`, the password field (line 103) is set to `View.INVISIBLE` when the user selects `TYPE_DRIVER`. If a user first enters a password (TYPE_COMPANY selected), then switches to TYPE_DRIVER, `passwordStr` at line 118 captures the previously entered password value. This password is included in `userRegisterParameter.password` (line 196) and sent to the backend even for DRIVER-type registrations. The backend must ignore this field for DRIVER accounts, but the client unnecessarily transmits a credential value.

No token expiry handling is visible in the assigned fragments. Token refresh/re-authentication logic would be in `WebApi` (not assigned).

---

### 6. Third-Party Libraries

**FINDING — TPL-01 — Medium**
`SetUserPhotoFragment.java` line 157 uses `com.pizidea.imagepicker.AndroidImagePicker` (import line 20). The `ImagePicker` library is noted in the checklist as a dependency to verify for CVE status and maintenance activity. This library is not maintained by a major vendor. Its version and CVE status must be verified against `build.gradle` (not an assigned file).

**FINDING — TPL-02 — Medium**
`ImagePostBackgroundTask.java` extends `android.os.AsyncTask` (line 15). `AsyncTask` was deprecated in Android API 30 (Android 11, 2020). Google's guidance is to use `java.util.concurrent` executors or Kotlin coroutines. The deprecation itself is not a CVE but is flagged by the checklist.

No other third-party libraries were directly instantiated in the three assigned files beyond standard Android SDK and the project's own `WebApi`/`WebData` classes.

---

### 7. Google Play and Android Platform

**FINDING — GP-01 — Medium**
`ImagePostBackgroundTask.java` uses `android.os.AsyncTask`, deprecated at API 30. This is instantiated by `SetUserPhotoFragment.uploadUserPhoto()`. This will produce lint deprecation warnings at the declared `targetSdkVersion` and represents technical debt.

`targetSdkVersion` and `minSdkVersion` values are in `build.gradle` (not assigned). The deprecated API usage here is confirmed regardless of those values.

**FINDING — GP-02 — Low**
`SetUserPhotoFragment.choosePhoto()` (lines 149–176) invokes runtime permission checks via `subFragPermission.checkFilePermissionWithRun(...)` and `subFragPermission.checkCameraPermissionWithRun(...)` before launching the image picker. This is the correct pattern for dangerous permissions. No issues found in permission request handling within the assigned file.

---

## Summary of Findings

| ID | Severity | File | Description |
|----|----------|------|-------------|
| NS-04 / AU-01 | **Critical** | `WebData.java` (supporting) | Hardcoded OAuth client credentials and service account username/password in `getTokenFormData()` lines 59–77. |
| DS-01 | **High** | `WebData.java` / `ModelPrefs.java` (supporting) | OAuth bearer token persisted to unencrypted plain `SharedPreferences`. |
| NS-01 | **Medium** | `URLBuilder.java` (supporting) | Hardcoded secondary endpoint `https://pandora.fleetiq360.com/pandora`. |
| DS-02 | **Medium** | `SignupFragment.java` line 118 | Password stored as immutable `String`; cannot be zeroed after use. |
| AU-02 | **Medium** | `SignupFragment.java` line 146 / `CommonFunc.java` line 92 | Password validation accepts any non-empty string — no minimum length or complexity. |
| TPL-01 | **Medium** | `SetUserPhotoFragment.java` line 20 | `AndroidImagePicker` library — maintenance status and CVE history require verification against `build.gradle`. |
| TPL-02 / GP-01 | **Medium** | `ImagePostBackgroundTask.java` line 15 | `AsyncTask` deprecated API 30+, used in photo upload path. |
| IH-01 | **Low** | `SetupEmailFragment.java` lines 163–166 | Email addresses sent to backend without client-side format validation. |
| DS-03 | **Low** | `SetUserPhotoFragment.java` line 166 | Captured user photo bitmap assigned to static field; cleared post-display but static window is uncontrolled. |
| AU-03 | **Low** | `SignupFragment.java` lines 103, 118, 196 | Password field value transmitted for DRIVER-type registrations when user switches type after entering a password. |
| NS-02 | **Info** | `URLBuilder.java` lines 171, 355 | Commented-out local development IP addresses remain in source. |
| NS-03 | **Unverified** | `URLBuilder.java` line 22 / `BuildConfig` | Primary base URL scheme (HTTP vs HTTPS) not confirmable from assigned files — requires `build.gradle` review. |

---

*End of APP59 Pass 1 Report*
