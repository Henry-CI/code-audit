# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP42
**Date:** 2026-02-27
**Stack:** Android / Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy:** The checklist states `Branch: main`. The actual branch is `master`. Audit proceeds on `master` as instructed.

---

## Step 2 — Reading Evidence

### File 1: PreStartCheckListPresenter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.presenter.PreStartCheckListPresenter`

**File path:**
`/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/presenter/PreStartCheckListPresenter.java`

**Fields / Constants:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `ui` | `EquipmentPrestartFragment` | `private` | 23 |
| `mapAnswers` | `HashMap<Integer, AnswerItem>` | `public` | 25 |
| `serverDateFormatter` | `ServerDateFormatter` | `private` | 27 |

**Public Methods:**
| Signature | Line |
|---|---|
| `PreStartCheckListPresenter(EquipmentPrestartFragment ui)` | 29 |
| `void getPreStartCheckListInfo()` | 34 |
| `void savePreStartCheckListAnswerResult(HashMap<Integer, AnswerItem> mapAnswers, String comments)` | 58 |

**No Activity, Fragment, Service, BroadcastReceiver, or ContentProvider declared in this file.**

---

### File 2: SelectDriverPresenter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.presenter.SelectDriverPresenter`

**File path:**
`/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/presenter/SelectDriverPresenter.java`

**Fields / Constants:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `ui` | `DriverListFragment` | `public` | 15 |

**Public Methods:**
| Signature | Line |
|---|---|
| `SelectDriverPresenter(DriverListFragment ui)` | 17 |
| `void getCompanyDriversList()` | 21 |
| `void showImage(String url, ImageView imageView)` | 25 |

**No Activity, Fragment, Service, BroadcastReceiver, or ContentProvider declared in this file.**

**Third-party library imported:**
- `com.nostra13.universalimageloader` (Universal Image Loader) — used in `showImage()`.

---

## Step 3 — Supporting File Evidence

The following files were read to support findings raised by the assigned files. They are not assigned files — findings against them are noted only where they are directly exercised by the assigned files.

### UserPhotoFragment.java (supporting)

**File path:**
`/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/UserPhotoFragment.java`

Contains the inner static class `SSLCertificateHandler` with the method `nuke()` at line 41. This method is called directly from `SelectDriverPresenter.showImage()` at line 39 of the assigned file.

`SSLCertificateHandler.nuke()` does all of the following:
1. Creates an `X509TrustManager` whose `checkClientTrusted()` and `checkServerTrusted()` methods are both empty — accepting any certificate from any issuer without validation (line 43–55, annotated `@SuppressLint("TrustAllX509TrustManager")`).
2. Initialises an `SSLContext` with that permissive `TrustManager` (line 57–58).
3. Sets it as the **process-wide default SSL socket factory** via `HttpsURLConnection.setDefaultSSLSocketFactory()` (line 59). This affects every subsequent HTTPS connection made by the app in the same process, not only image loading.
4. Sets a **process-wide default hostname verifier** that unconditionally returns `true` for every hostname (lines 60–65, annotated `@SuppressLint("BadHostnameVerifier")`).

### CurrentUser.java (supporting)

**File path:**
`/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/CurrentUser.java`

- Static fields `loginEmail` (line 22) and `loginPassword` (line 23) hold credentials in static process memory.
- `setTemporaryLoginInformation()` stores the MD5-hashed password in the static field `loginPassword` (line 122).
- `login()` stores the plain-text `loginPassword` back onto the `User` object via `get().setPassword(loginPassword)` (line 90).
- `logout()` clears only the user preference key and nulls the static `user` field (lines 125–128); it does not null `loginEmail` or `loginPassword`.

### WebData.java (supporting — called from both assigned files via `WebData.instance()`)

**File path:**
`/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebData.java`

- `getTokenFormData()` (lines 56–82) hardcodes OAuth2 credentials:
  - `client_id`: `987654321`
  - `client_secret`: `8752361E593A573E86CA558FFD39E`
  - `username`: `gas`
  - `password`: `ciiadmin`
- The auth token is persisted via `ModelPrefs.saveObject(TOKEN_ITEM_KEY, result)` (line 93), which writes to plain unencrypted `SharedPreferences`.

### ModelPrefs.java (supporting)

**File path:**
`/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/ModelPrefs.java`

Uses `Context.MODE_PRIVATE` `SharedPreferences` (line 17). No use of `EncryptedSharedPreferences`. All values — including auth tokens written by `WebData` — are stored in plaintext.

---

## Step 4 — Checklist Findings

### Section 1 — Signing and Keystores

No hardcoded keystore paths, passwords, or keystore files were encountered in the two assigned files. The assigned files do not reference `signingConfigs`, `build.gradle`, `.jks`, or pipeline credentials.

**No issues found — Section 1** (within scope of assigned files).

---

### Section 2 — Network Security

**CRITICAL — Disabled SSL/TLS certificate validation (global, process-wide)**

- **Location:** `SelectDriverPresenter.java`, line 39.
  ```java
  UserPhotoFragment.SSLCertificateHandler.nuke();
  ```
  Immediately before loading a driver photo URL via `ImageLoader.getInstance().displayImage(url, imageView, ...)`, the presenter calls `SSLCertificateHandler.nuke()`. This method (implemented in `UserPhotoFragment.java`, lines 41–69) does the following:
  - Installs a custom `X509TrustManager` that performs **no certificate validation whatsoever**: both `checkClientTrusted()` and `checkServerTrusted()` are empty method bodies. Android Lint suppression `@SuppressLint("TrustAllX509TrustManager")` is applied, indicating the developer was aware the code would otherwise be flagged.
  - Sets the result as the **default `SSLSocketFactory`** for the entire process via `HttpsURLConnection.setDefaultSSLSocketFactory()`. This is not scoped to image loading; every subsequent HTTPS connection from any thread in the process — including API calls to `forkliftiqws`, login requests, prestart checklist submission, and session data — will use this socket factory unless explicitly overridden.
  - Installs a **default `HostnameVerifier`** that returns `true` unconditionally, suppressed with `@SuppressLint("BadHostnameVerifier")`. This means a server presenting a certificate for any hostname will pass hostname verification.
  - The combination renders TLS entirely inoperative: any network adversary capable of intercepting traffic (e.g. on a warehouse Wi-Fi network) can present a self-signed certificate for any domain and have it accepted. All data transmitted over "HTTPS" — credentials, operator identifiers, forklift session data, prestart answers — is exposed to interception and modification.

  `nuke()` is also called from `UserPhotoFragment.showUserPhoto()` (line 30 of that file), meaning this occurs in at least two code paths.

**Severity: Critical.** This is not a configuration weakness; it is a deliberate removal of all TLS trust verification for the entire application process, triggered every time a driver photo is displayed.

**HIGH — Hardcoded OAuth2 client credentials in source code**

- **Location:** `WebData.java`, lines 63–77 (called via `WebData.instance()` by both assigned files).
  ```java
  String clientId = "987654321";
  String clientSecret = "8752361E593A573E86CA558FFD39E";
  String userName = "gas";
  String password = "ciiadmin";
  ```
  These are static string literals embedded in compiled bytecode. Any attacker with access to the APK can extract them with a decompiler. Because `nuke()` eliminates TLS verification, intercepting a login request to confirm these values in transit is also trivial.

**Severity: High.**

---

### Section 3 — Data Storage

**HIGH — Auth token stored in plain (unencrypted) SharedPreferences**

- **Location:** `WebData.setGetTokenResult()` (line 93 of `WebData.java`) calls `ModelPrefs.saveObject(TOKEN_ITEM_KEY, result)`.
- `ModelPrefs` uses standard `SharedPreferences` with `MODE_PRIVATE` (line 17 of `ModelPrefs.java`). There is no use of `EncryptedSharedPreferences` from Jetpack Security anywhere in the preferences layer.
- The auth token is therefore stored in plaintext in the app's shared preferences XML file. On a rooted device, or via ADB backup if `allowBackup` is enabled, this token is directly readable.

**Severity: High.**

**MEDIUM — Operator password held in static memory; not cleared on logout**

- **Location:** `CurrentUser.java`, static fields `loginEmail` (line 22) and `loginPassword` (line 23).
- `logout()` (lines 125–128) clears the `user` field and the user-ID preference key, but does **not** null `loginEmail` or `loginPassword`. The MD5-hashed password remains in static memory for the lifetime of the process after logout.
- Additionally, `login()` at line 90 calls `get().setPassword(loginPassword)` — storing the credential back onto the user object after authentication. The relationship between this and what is eventually persisted to `UserDb` would require further investigation (not in assigned files) but is a concern.

**Severity: Medium.**

Note: MD5 is used to hash passwords (via `CommonFunc.MD5_Hash`) before transmission (line 82 of `CurrentUser.java`) and before storage in the static field (line 122). MD5 is a broken cryptographic hash function, not suitable for password hashing. This is noted as a secondary concern under this section.

---

### Section 4 — Input and Intent Handling

The two assigned files are presenter classes. They do not declare or configure Activities, Services, BroadcastReceivers, or WebViews, and they do not handle deep links or intents directly.

`SelectDriverPresenter.getCompanyDriversList()` (line 21) passes the result of `CurrentUser.get().associatedDrivers()` to the UI without additional filtering — no input validation concern arises here as this is read-only display of server data already held in the local user object.

`SelectDriverPresenter.showImage(String url, ImageView imageView)` (line 25) accepts a URL string and passes it directly to `ImageLoader.getInstance().displayImage(url, ...)` without validating the scheme or host. If the URL originates from untrusted input (e.g. a server response that has been tampered with — which is feasible given the disabled TLS verification), this could load arbitrary content into the image view. This is a secondary consequence of the Critical SSL finding above.

**No standalone issues found — Section 4** (the URL validation concern is derivative of the Section 2 Critical finding).

---

### Section 5 — Authentication and Session

**HIGH — Auth token persisted to plain SharedPreferences (see Section 3)**

This finding is recorded under Section 3 and applies equally here: the auth token used for all requests to `forkliftiqws` is stored without encryption.

**MEDIUM — Credentials not fully cleared on logout**

As noted in Section 3, `CurrentUser.logout()` does not clear the static `loginEmail` and `loginPassword` fields. If the same device is shared between operators (a common scenario on a forklift fleet), the previous operator's credentials remain in process memory.

**No token expiry handling was visible in the two assigned files.** `PreStartCheckListPresenter` calls `WebApi.async()` methods and handles `onFailed` callbacks by falling back to cached data — there is no observable re-authentication or token-refresh path in the assigned files. This warrants investigation in the `WebApi` / `WebListener` layer (not assigned).

---

### Section 6 — Third-Party Libraries

**MEDIUM — Universal Image Loader (com.nostra13.universalimageloader) — abandoned library**

- **Location:** `SelectDriverPresenter.java`, imports at lines 8–12; used in `showImage()` at lines 26–40.
- Universal Image Loader's last release was version 1.9.5, published in 2015. The project has been officially deprecated by its author, who recommends migration to Glide or Picasso. The library has received no security patches in over a decade.
- In the context of this app, the library is being used alongside a disabled SSL trust chain (`nuke()` called on line 39 immediately before `ImageLoader.getInstance().displayImage()`), which compounds any risk from the abandoned library.

**Severity: Medium** (abandoned library, no recent CVE — but the usage pattern is insecure due to the companion SSL disablement).

---

### Section 7 — Google Play and Android Platform

**LOW — `@SuppressLint` used to suppress security lint warnings**

- `@SuppressLint("TrustAllX509TrustManager")` and `@SuppressLint("BadHostnameVerifier")` are applied in `UserPhotoFragment.SSLCertificateHandler.nuke()`. These suppressions were added specifically to silence Android Lint's detection of the insecure trust manager and hostname verifier. This indicates the developer was warned by tooling and chose to suppress the warnings rather than address the underlying issue.

No deprecated API usage (`AsyncTask`, `startActivityForResult`, etc.) was observed in the two assigned files.

The two assigned files contain no permission declarations — those are in `AndroidManifest.xml`, which is not an assigned file for this agent.

**No further issues found — Section 7** (within scope of assigned files).

---

## Summary of Findings

| ID | Severity | Section | File | Description |
|---|---|---|---|---|
| F01 | Critical | 2 — Network Security | `SelectDriverPresenter.java:39` (via `UserPhotoFragment.SSLCertificateHandler.nuke()`) | Process-wide SSL certificate validation and hostname verification disabled before every driver photo load. Affects all HTTPS connections in the app process. |
| F02 | High | 2 — Network Security | `WebData.java:63–77` (called by both assigned files) | OAuth2 `client_id`, `client_secret`, username, and password hardcoded as string literals in source. |
| F03 | High | 3 — Data Storage / 5 — Authentication | `WebData.java:93` + `ModelPrefs.java:17` | Auth token persisted to unencrypted `SharedPreferences`. |
| F04 | Medium | 3 — Data Storage / 5 — Authentication | `CurrentUser.java:22–23, 125–128` | Static `loginEmail` and `loginPassword` fields not cleared on logout; credential lingers in memory across operator sessions. |
| F05 | Medium | 6 — Third-Party Libraries | `SelectDriverPresenter.java:8–12` | Universal Image Loader is an abandoned library (last release 2015, no security patches). |
| F06 | Low | 7 — Platform | `UserPhotoFragment.java:40–41, 61` | `@SuppressLint("TrustAllX509TrustManager")` and `@SuppressLint("BadHostnameVerifier")` used to suppress Lint detection of the insecure SSL implementation. |

---

## Branch Discrepancy Record

The checklist header states `Branch: main`. The repository's current branch, as verified by `git branch --show-current`, is `master`. Audit was conducted on `master` per step 1 instructions.
