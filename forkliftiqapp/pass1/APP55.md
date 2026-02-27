# Security Audit — Pass 1
**Agent ID:** APP55
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android / Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist specifies `Branch: main`. The actual default branch is `master`. Audit proceeds on `master` as confirmed above.

---

## Reading Evidence

### File 1 — EquipmentPrestartFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentPrestartFragment`

**Superclass / interfaces:**
- Extends `FleetFragment` (which extends `BaseFragment`)
- Implements `AbsRecyclerAdapter.OnItemClickListener`

**Public methods and line numbers:**

| Method | Line |
|--------|------|
| `onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle) : View` | 45 |
| `setRecyclerViewdata(PreStartQuestionResultArray) : void` | 50 |
| `initViews() : void` | 60 |
| `showNext() : void` | 120 |
| `onLeftButton(View) : void` | 125 |
| `onMiddleButton(View) : void` | 135 |
| `onRightButton(View) : void` | 143 |
| `onHiddenChanged(boolean) : void` | 150 |
| `onItemClick(View, int) : void` | 155 |

**Fields / constants:**

| Name | Type | Visibility | Value |
|------|------|------------|-------|
| `TAG` | `String` | private static | `"EquipmentPrestartFragment"` |
| `myAdapter` | `PrestartCheckListAdapter` | private | — |
| `qustionItemArrayList` | `ArrayList<PreStartQuestionItem>` | **public** | new ArrayList |
| `presenter` | `PreStartCheckListPresenter` | private | — |
| `myCommentStr` | `String` | private | `""` |

---

### File 2 — IncidentFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.IncidentFragment`

**Superclass:**
- Extends `FleetFragment`

**Public methods and line numbers:**

| Method | Line |
|--------|------|
| `onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle) : View` | 128 |
| `initViews() : void` | 134 |
| `onRightButton(View) : void` | 255 |

**Fields / constants (all private):**

| Name | Type |
|------|------|
| `incident_checkbox` | `ToggleImageButton` |
| `near_miss_checkbox` | `ToggleImageButton` |
| `incident_date` | `TextView` |
| `incident_time` | `TextView` |
| `description` | `EditText` |
| `incidentActivity` | `IncidentActivity` |
| `equipment_name` | `TextView` |
| `incidentCal` | `Calendar` |
| `companyDateFormatter` | `CompanyDateFormatter` |
| `serverDateFormatter` | `ServerDateFormatter` |
| `dateSet` | `Boolean` |
| `timeSet` | `Boolean` |
| `equipmentItem` | `EquipmentItem` |
| `equipmentList` | `ArrayList<EquipmentItem>` |

---

### File 3 — IncidentPart2Fragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.IncidentPart2Fragment`

**Superclass:**
- Extends `FleetFragment`

**Public methods and line numbers:**

| Method | Line |
|--------|------|
| `onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle) : View` | 38 |
| `initViews() : void` | 43 |
| `onRightButton(View) : void` | 147 |
| `onMiddleButton(View) : void` | 260 |

**Fields (all private):**

| Name | Type |
|------|------|
| `location` | `EditText` |
| `injury` | `ToggleImageButton` |
| `injury_type` | `TextView` |
| `witness` | `EditText` |
| `injury_photo` | `ImageView` |
| `signature_image` | `ImageView` |
| `incidentActivity` | `IncidentActivity` |

---

## Findings by Checklist Section

### 1. Signing and Keystores

No `.jks`, `.keystore`, or `.p12` files are referenced in these three fragment files. The `app/build.gradle` `signingConfigs` block uses variable references (`DEV_STORE_FILE`, `DEV_STORE_PASSWORD`, `RELEASE_STORE_FILE`, etc.) rather than inline literal values — consistent with injection from `gradle.properties` or a CI environment. This is in scope for other agents; no issues arise directly from the three assigned fragments.

**No issues found — Signing and Keystores** (within scope of assigned files)

---

### 2. Network Security

#### 2a. WebView in EquipmentPrestartFragment — JavaScript enabled, no URL whitelist (Medium)

`EquipmentPrestartFragment.onRightButton()` at line 144–146 constructs an explicit `Intent` targeting `WebActivity` and passes a URL built by `URLBuilder.urlGetDiagnosis()`:

```java
Intent intent = new Intent(getContext(), WebActivity.class);
intent.putExtra(WebActivity.URL_KEY, URLBuilder.urlGetDiagnosis(MyCommonValue.currentEquipmentItem.id).url);
startActivity(intent);
```

`WebActivity.initWebView()` (LibCommon) enables JavaScript unconditionally:

```java
webView.getSettings().setJavaScriptEnabled(true);  // line 43, WebActivity.java
```

`WebActivity.shouldOverrideUrlLoading()` returns `false` for all URLs, meaning any redirect or navigation that occurs within the WebView is followed without validation or whitelisting. There is no check that the loaded URL belongs to an expected domain (e.g. `pandora.fleetiq360.com`). A server-side XSS or a man-in-the-middle response could inject arbitrary JavaScript into the WebView, which runs in the app's context.

**Severity: Medium.** The URL is constructed server-side via `BuildConfig.BASE_URL` and an equipment ID; it is not user-supplied. However, if the connection is downgraded or the HTTPS certificate is not validated, injected content could execute JavaScript. The absence of a URL whitelist in `shouldOverrideUrlLoading` is also a weakness.

#### 2b. Hardcoded secondary base URL in URLBuilder (Low / Informational)

`URLBuilder.java` contains a hardcoded HTTPS URL at line 26:

```java
final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora";
```

This URL is used by `urlGetDiagnosis()` (called from `EquipmentPrestartFragment.onRightButton()` at line 145) and `urlGetUniversity()`. While it uses HTTPS, the URL is a literal in source code rather than a build-flavor configuration field. It cannot be changed per environment without a code change, and it is visible in decompiled APKs. This is a low-severity information disclosure rather than an exploitable network vulnerability.

#### 2c. ImagePostRequest uses HttpURLConnection without explicit TLS/hostname verification

`ImagePostRequest.SendHttpImage()` and `SendMultipartHttpImage()` open `HttpURLConnection` directly at lines 46 and 128 respectively. The connection is used to upload incident photos and signatures. No custom `SSLSocketFactory`, `TrustManager`, or `HostnameVerifier` is set; the JDK default chain validation applies. This is acceptable practice. However, there is no explicit timeout set on the single-image variant (`SendHttpImage`), only on `SendMultipartHttpImage` (`setConnectTimeout(10*1000)`). A missing connect timeout can cause the UI thread (via `AsyncTask`) to hang indefinitely on network failure — not a security vulnerability but a reliability concern noted for completeness.

**No exploitable SSL bypass found in the three assigned files or their direct network helpers.**

---

### 3. Data Storage

#### 3a. Auth token and user data stored in plain SharedPreferences (High)

`ModelPrefs` (the sole persistence layer used by `WebData` and `CurrentUser` for in-scope functionality) stores all values in unencrypted `SharedPreferences`:

```java
// ModelPrefs.java line 17
SharedPreferences prefs = MyApplication.getContext().getSharedPreferences("prefs", Context.MODE_PRIVATE);
```

`WebData.setGetTokenResult()` serialises the OAuth bearer token to this store under the key `"token_result"` (line 93, WebData.java). `CurrentUser.setUser()` persists the user ID (line 34, CurrentUser.java). The `User` object cached in `UserDb` (Realm database, unencrypted) includes the password field — visible at `UserDb.get(String email, String password)` line 59, which queries by plaintext `password`.

The password is stored in the Realm database in plaintext. `CurrentUser.createUser()` at line 61 passes `loginItem.password` directly into the `User` constructor. After login, `get().setPassword(loginPassword)` stores the raw password in memory and in the Realm database.

**Severity: High.** The app handles operator credentials (username, password, bearer token) for safety-critical equipment access. Storing the bearer token in unencrypted `SharedPreferences` and the user password in an unencrypted Realm database violates Android security best practices. On a rooted device or via ADB backup (see 3b), these values are directly readable. The Jetpack `EncryptedSharedPreferences` API and Realm's encryption key support should be used instead.

#### 3b. android:allowBackup="true" enables ADB data extraction (High)

`AndroidManifest.xml` at line 19 declares:

```xml
android:allowBackup="true"
```

With this setting, any user with USB debugging enabled can extract the app's entire data directory — including the unencrypted `SharedPreferences` file containing the bearer token and the unencrypted Realm database containing operator passwords — via `adb backup` without requiring root. For a forklift management app storing safety-critical operator data, this is a High finding.

**Severity: High.** Set `android:allowBackup="false"` in the `<application>` element of `AndroidManifest.xml`.

#### 3c. Signature file path stored as plain String in IncidentActivity (Low)

In `IncidentPart2Fragment`, the operator's signature is captured via `SignatureDialog` and stored as a file-system path string in `incidentActivity.signaturePath` (line 73, IncidentPart2Fragment.java). The field is declared `public String signaturePath` in `IncidentActivity.java` (line 14). The file itself is written to internal storage by `SignatureDialog`; the path is passed without validation into `ImagePostRequest` for upload. If the `signaturePath` were tampered with (unlikely given it originates from `SignatureDialog` within the same process), an arbitrary file could be uploaded. This is a low-severity concern given the in-process origin but is noted because the field is public.

#### 3d. No issues with external storage or MODE_WORLD_READABLE

No calls to `Environment.getExternalStorageDirectory()`, `openFileOutput()` with `MODE_WORLD_READABLE`, or `MODE_WORLD_WRITEABLE` were found in the three assigned files or their direct dependencies (`ImagePostBackgroundTask`, `ImagePostRequest`).

---

### 4. Input and Intent Handling

#### 4a. Public mutable field qustionItemArrayList (Low / Design)

`EquipmentPrestartFragment` declares:

```java
public ArrayList<PreStartQuestionItem> qustionItemArrayList = new ArrayList<>();  // line 38
```

This field is `public`, allowing any class with a reference to the fragment to mutate the answer set without going through the presenter. While fragments are not typically accessible across process boundaries, direct mutation of this list by other in-app code bypasses the presenter's answer-count validation at line 136:

```java
if (presenter.mapAnswers.size() != qustionItemArrayList.size())
```

If `qustionItemArrayList` is cleared by external code after answers are collected but before `onMiddleButton` is called, the check `presenter.mapAnswers.size() != qustionItemArrayList.size()` would evaluate `0 != 0 == false` and the save would proceed with no questions answered. This would result in incomplete pre-start data being submitted for safety-critical equipment operation.

**Severity: Low** (requires in-app code to exploit; no cross-process vector). The field should be made private with a controlled accessor.

#### 4b. No validation of description length or content in IncidentFragment (Low)

`IncidentFragment.onRightButton()` at lines 271–275 stores the raw text of the `description` EditText directly into `incidentActivity.impactParameter.description` with no length limit or sanitisation:

```java
incidentActivity.impactParameter.description = description.getText().toString();
```

Similarly, `IncidentPart2Fragment.setParameter()` at lines 192–194 stores `witness` and `location` fields:

```java
incidentActivity.impactParameter.witness = witness.getText().toString();
incidentActivity.impactParameter.location = location.getText().toString();
```

These values are subsequently submitted to the backend via `WebApi.async().saveImpact()`. No maximum-length validation is applied on the client side. Excessively large strings could cause backend errors or, if the server is vulnerable, contribute to injection attacks. The location field has a non-empty check (line 148), but no upper bound.

**Severity: Low.** Input should be length-capped on the client side to match backend constraints.

#### 4c. No exported activities, services, or receivers in the assigned fragments' scope

`AndroidManifest.xml` declares all app activities without `android:exported="true"`. No `<intent-filter>` elements (other than the launcher intent on `ShowPackageAvailable`) are present. The `IncidentActivity` (line 61–63) has no intent filter and is not exported. The `FileProvider` is correctly declared with `android:exported="false"` and `android:grantUriPermissions="true"`.

**No issues found — exported component attack surface** (within scope of assigned activities).

#### 4d. WebView URL not validated against a whitelist

Covered under section 2a above.

---

### 5. Authentication and Session

#### 5a. Pre-start save proceeds without re-validating session authenticity (Medium)

`EquipmentPrestartFragment.onMiddleButton()` at line 139 calls:

```java
presenter.savePreStartCheckListAnswerResult(presenter.mapAnswers, myCommentStr);
```

`PreStartCheckListPresenter.savePreStartCheckListAnswerResult()` reads the session from `WebData.instance().getSessionResult()` (which calls `SessionDb.readRunningSession()`) and constructs the save parameter from it. There is no re-check that the current user's session is still valid (i.e., that the token has not expired) before submitting pre-start results. If the token is stale, the network call will fail and the error path (offline fallback) will activate, silently committing the pre-start result to local offline storage as if it were legitimate. The offline fallback at lines 84–95 of `PreStartCheckListPresenter` does not check token validity.

**Severity: Medium.** A user whose session token has expired can still save pre-start results into the local offline store, which will be synced to the server when connectivity and a valid token are restored — but under a potentially outdated user context.

#### 5b. impactParameter.driver_id set from in-memory WebData.getUserId() (Informational)

In `IncidentPart2Fragment.setParameter()` at line 189:

```java
incidentActivity.impactParameter.driver_id = WebData.instance().getUserId();
```

`WebData.getUserId()` reads from `CurrentUser.get()`, which in turn reads from `ModelPrefs` (unencrypted SharedPreferences). If the current user state is inconsistent (e.g., stale from a previous login due to incomplete logout), the incident could be attributed to the wrong operator. This is a data integrity concern rather than a direct security vulnerability, but in a safety-critical context it merits attention.

**Severity: Informational** (no direct exploitability; depends on incomplete logout, which is handled by other agents).

#### 5c. Incident recording is not gated by an active, authenticated session check

`IncidentActivity` is launched without verifying that a session is currently active. `ImpactParameter.driver_id` is populated only at save time (in `IncidentPart2Fragment.setParameter()`), not at the start of the flow. An operator who is not in an active session can open the incident flow and submit an incident report attributed to the last logged-in user's ID. There is no guard at the entry point of `IncidentActivity.onCreate()` that checks `WebData.instance().getSessionResult() != null` or that a valid authentication token exists.

**Severity: Medium.** In a safety environment, incident reports must be unambiguously tied to an authenticated, currently-active operator.

---

### 6. Third-Party Libraries

The following libraries are directly involved in the three assigned files:

| Library | Version | Notes |
|---------|---------|-------|
| `com.android.volley:volley` | `1.1.1` | Released 2018. Volley 1.2.x series is available (1.2.1 released 2021). No critical CVEs known for 1.1.1 in the context of this app's usage, but the library is behind by several years. |
| `com.squareup.retrofit2:retrofit` | `2.5.0` | Released 2019. Current is 2.11.x (2024). Known to lack OkHttp 4.x improvements. No critical CVEs for this usage pattern, but significantly out of date. |
| `com.google.code.gson:gson` | `2.8.5` | Released 2018. CVE-2022-25647 (deserialization of untrusted data) is present in versions before 2.8.9. **Flagged.** |
| `com.android.support:appcompat-v7` | `26.0.2` | Released 2017. AndroidX migration not performed. Support library is no longer maintained. |
| `com.google.android.gms:play-services-location` | `11.8.0` | Released 2017. Current is 21.x. Significantly out of date. |
| `io.realm:realm-gradle-plugin` | `3.7.2` | Released 2017. Realm Java 3.x is well past end of life (current is 10.x). Unencrypted Realm databases in this version have no built-in encryption by default. |
| `com.pizidea.imagepicker` (AndroidImagePicker) | unknown (local lib) | Used in `IncidentPart2Fragment` for injury photo selection. Version not determinable from build.gradle — it is an included local module. |
| `com.android.tools.build:gradle` | `3.0.0` | Gradle plugin version 3.0.0 is from 2017. Well out of date. |

**CVE finding — Gson 2.8.5 (CVE-2022-25647) — Medium:**
Gson versions before 2.8.9 are vulnerable to stack overflow via deeply nested JSON during deserialization. The app uses Gson for all web service response parsing (`GsonHelper`). Attacker-controlled server responses (e.g., via MITM or a compromised backend) could exploit this to crash the app. Upgrade to 2.8.9 or later (current: 2.10.1).

**Deprecated library — AsyncTask (Medium):**
`ImagePostBackgroundTask` at line 15 extends `AsyncTask`, which is deprecated as of Android API 30. The app's `targetSdkVersion` is 26 (see section 7), so this does not yet cause a runtime issue, but it is a design concern for future SDK upgrades.

**Realm unencrypted — High (cross-reference with section 3a):**
Realm 3.7.2 stores data in an unencrypted database file. User credentials including passwords are stored in this Realm instance (confirmed via `UserDb`). Upgrading to Realm 10.x and enabling Realm encryption with a key stored in Android Keystore would remediate this.

---

### 7. Google Play and Android Platform

#### 7a. targetSdkVersion 26 — below Google Play minimum requirement (High)

`build.gradle` (root) at line 27:

```groovy
myTargetSdkVersion=26
```

Google Play requires `targetSdkVersion` 34 or higher for new app submissions and updates as of August 2024. `targetSdkVersion` 26 (Android 8.0, released 2017) means the app does not receive Android 8.1+ security enforcement improvements, including:

- Stricter implicit broadcast restrictions
- `FLAG_ACTIVITY_NEW_TASK` requirements
- Background execution limits

**Severity: High** (Google Play compliance; app cannot be updated on Play Store without resolving this).

#### 7b. AsyncTask deprecated (Low)

`ImagePostBackgroundTask` extends `android.os.AsyncTask` (line 15). `AsyncTask` was deprecated in API 30. With `targetSdkVersion` 26 this is not a runtime issue, but as `targetSdkVersion` is raised to meet Play Store requirements, this will generate compiler warnings and requires migration to `java.util.concurrent` or Kotlin coroutines.

#### 7c. minifyEnabled false for release builds (Medium)

`app/build.gradle` at line 53:

```groovy
minifyEnabled false
```

Code minification and obfuscation are disabled for release builds. ProGuard/R8 is referenced (`proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'`) but not applied. Class names, method names, field names, and constants — including the OAuth client ID (`"987654321"`) and client secret (`"8752361E593A573E86CA558FFD39E"`) hardcoded in `WebData.getTokenFormData()` — are trivially readable in a decompiled APK.

**Severity: Medium.** Enable `minifyEnabled true` for release builds. The hardcoded OAuth client secret is a separate critical finding (see section 7d).

#### 7d. Hardcoded OAuth client credentials in WebData (Critical — cross-file)

Although `WebData.java` is not one of the three assigned files, it is a direct runtime dependency of `IncidentFragment` (via `WebData.instance().getUserId()`) and `EquipmentPrestartFragment` (via the presenter). The finding is recorded here as it is encountered during evidence review of the assigned scope:

`WebData.getTokenFormData()` at lines 64–76:

```java
String clientId = "987654321";
String clientSecret = "8752361E593A573E86CA558FFD39E";
String userName = "gas";
String password = "ciiadmin";
```

These are hardcoded OAuth2 client credentials embedded in the application binary. Any actor who decompiles the APK (made easier by `minifyEnabled false`) can retrieve the `client_secret` and use it to authenticate against the token endpoint directly. This is a Critical finding but is assigned to the agent covering `WebData.java` as the primary file. It is noted here for completeness because its use is triggered by the incident and pre-start flows in the assigned fragments.

#### 7e. startActivityForResult deprecated (Informational)

`FleetFragment.startConnect()` at line 228 calls `getActivity().startActivityForResult(enableGPS, LOCATION_SETTINGS_REQUEST_GPS)`. This API is deprecated from `Activity` as of API 30, requiring migration to the Activity Result API. Low-priority given `targetSdkVersion` 26 but will need resolution when SDK is raised.

#### 7f. v2SigningEnabled false in all signingConfigs (Low)

All three `signingConfigs` blocks in `app/build.gradle` set `v2SigningEnabled false`. APK Signature Scheme v2 provides stronger integrity guarantees than v1 (JAR signing). Disabling v2 signing means the APK relies solely on JAR-based signing, which offers weaker tamper detection. Google Play requires v2 signing for API 30+ target. This should be enabled.

---

## Summary of Findings

| # | Severity | Section | Finding |
|---|----------|---------|---------|
| 1 | High | 3 — Data Storage | Bearer token stored in unencrypted SharedPreferences; operator password stored in unencrypted Realm database |
| 2 | High | 3 — Data Storage | `android:allowBackup="true"` permits ADB extraction of all app data including credentials |
| 3 | High | 6 — Libraries | Realm 3.7.2 — unencrypted database; well past end-of-life |
| 4 | High | 7 — Platform | `targetSdkVersion 26` — below Google Play minimum (34); cannot update app on Play Store |
| 5 | Medium | 2 — Network | WebView in WebActivity has JavaScript enabled with no URL whitelist; used by EquipmentPrestartFragment for diagnosis content |
| 6 | Medium | 5 — Auth/Session | Pre-start save falls through to offline store without re-validating token; stale session can commit safety data |
| 7 | Medium | 5 — Auth/Session | Incident recording not gated by an active authenticated session; any user can submit an incident under the last logged-in operator's ID |
| 8 | Medium | 6 — Libraries | Gson 2.8.5 — CVE-2022-25647 stack overflow on deeply nested JSON deserialization |
| 9 | Medium | 7 — Platform | `minifyEnabled false` for release — no obfuscation; secrets readable in decompiled APK |
| 10 | Low | 2 — Network | `baseUrlForPreStartHelp` hardcoded in URLBuilder; not environment-configurable |
| 11 | Low | 3 — Data Storage | `incidentActivity.signaturePath` is public; unvalidated file path passed to image upload |
| 12 | Low | 4 — Input | `qustionItemArrayList` is public; direct mutation bypasses presenter validation of pre-start completeness |
| 13 | Low | 4 — Input | No client-side length validation on description, location, witness fields in incident fragments |
| 14 | Low | 7 — Platform | `v2SigningEnabled false` in all signing configs — weaker APK integrity |
| 15 | Informational | 5 — Auth/Session | `impactParameter.driver_id` sourced from potentially stale in-memory `CurrentUser`; risk of misattribution |
| 16 | Informational | 7 — Platform | `AsyncTask` and `startActivityForResult` deprecated; migration required when targetSdkVersion is raised |

---

*End of Pass 1 report — Agent APP55*
