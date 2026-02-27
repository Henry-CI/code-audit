# Pass 1 Security Audit — Agent APP41

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

`git branch --show-current` returned: **master**

Checklist specifies "Branch: main". Actual branch is "master". Discrepancy recorded. Branch is confirmed as the correct working branch; audit proceeds.

---

## Step 2 — Reading Evidence

### File 1: EquipmentDriverAccessPresenter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.presenter.EquipmentDriverAccessPresenter`

**Fields:**
- `private BaseFragment ui` — instance field, reference to the UI fragment

**Public methods (with line numbers):**
- `EquipmentDriverAccessPresenter(BaseFragment ui)` — constructor, line 40
- `void createAndSaveSession()` — line 44

**Private methods (with line numbers):**
- `void startSession()` — line 106
- `EquipmentItem getEquipmentItem(int unitId)` — line 117
- `void onSessionNotStopped(final SessionResult sessionResult)` — line 133
- `void deleteSession(final int sessionId)` — line 209
- `void stopSession(SessionResult sessionResult)` — line 237
- `void resumeSession(SessionResult result, EquipmentItem equipmentItem)` — line 275
- `void onSessionSaved()` — line 282

**Notable imports/dependencies:**
- `javax.net.ssl.HttpsURLConnection` — used for HTTP status code constants only
- `au.com.collectiveintelligence.fleetiq360.WebService.WebApi` — async web API
- `au.com.collectiveintelligence.fleetiq360.model.SessionDb` — local session database
- `au.com.collectiveintelligence.fleetiq360.model.SyncService` — background sync
- `au.com.collectiveintelligence.fleetiq360.session.SessionTimeouter` — session timeout
- `au.com.collectiveintelligence.fleetiq360.ui.activity.SessionActivity` — session screen

**No Android component declarations** (presenter class only, not an Activity/Fragment/Service/Receiver).

---

### File 2: EquipmentSelectForkPresenter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.presenter.EquipmentSelectForkPresenter`

**Fields:**
- `public EquipmentListFragment ui` — **public** field, reference to the UI fragment (line 22)
- `private ShowResultCallBack uiCb` — callback interface reference (line 23)

**Public methods (with line numbers):**
- `EquipmentSelectForkPresenter(EquipmentListFragment ui)` — constructor, line 25
- `void getEquipmentList()` — line 30
- `void showImage(String url, ImageView imageView)` — line 57

**Inner interface:**
- `interface ShowResultCallBack` — line 75
  - `void uiUpdateEquipmentList(GetEquipmentResultArray resultArray)` — line 76

**Notable imports/dependencies:**
- `com.nostra13.universalimageloader.*` — Universal Image Loader library
- `au.com.collectiveintelligence.fleetiq360.ui.fragment.UserPhotoFragment` — references `SSLCertificateHandler.nuke()` at line 71

**Critical observation — `showImage()` at line 71:**
```java
UserPhotoFragment.SSLCertificateHandler.nuke();
ImageLoader.getInstance().displayImage(url, imageView, displayImageOptions, ...);
```
This calls `UserPhotoFragment.SSLCertificateHandler.nuke()` immediately before loading any equipment image. The `nuke()` method (confirmed by reading `UserPhotoFragment.java`) globally disables SSL/TLS certificate validation for the entire JVM process.

---

### File 3: JobsPresenter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.presenter.JobsPresenter`

**Fields:**
- `private JobsFragment ui` — UI fragment reference (line 29)
- `private SessionResult sessionResult` — holds the active session object (line 30)
- `private LocalDateTime startDate` — session start timestamp (line 31)
- `private ServerDateFormatter serverDateFormatter` — date formatter (line 33)
- `private Handler myHandler` — main-thread handler for timer (line 35)
- `private boolean timerStopped` — timer state flag (line 36)
- `private Runnable timerRunnable` — repeating runnable, posts every 500 ms (line 37)

**Public methods (with line numbers):**
- `void stopTimer()` — line 54
- `JobsPresenter(JobsFragment ui)` — constructor, line 59
- `void saveSessionEnd()` — line 74

**Private methods (with line numbers):**
- `void startTimer()` — line 48
- `void setTimeText()` — line 68

**Notable imports/dependencies:**
- `org.joda.time.LocalDateTime`, `org.joda.time.Period` — Joda-Time library
- `au.com.collectiveintelligence.fleetiq360.WebService.WebApi` — async web API
- `au.com.collectiveintelligence.fleetiq360.model.SessionDb` — local session database
- `au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication` — imported **twice** (lines 23 and 26 — duplicate import)

**Notable observation — duplicate import:**
`au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication` is imported on both line 23 and line 26. This is a code quality defect but not a security issue.

---

## Step 3 — Checklist Review

### Section 1: Signing and Keystores

These three presenter files contain no signing configuration, keystore references, passwords, or build-system credentials. Not applicable to assigned files.

No issues found — Section 1 (Signing and Keystores).

---

### Section 2: Network Security

**CRITICAL — SSL/TLS Certificate Validation Globally Disabled**

**File:** `EquipmentSelectForkPresenter.java`, line 71
**Also confirmed in:** `UserPhotoFragment.java`, lines 37–69

`EquipmentSelectForkPresenter.showImage()` calls `UserPhotoFragment.SSLCertificateHandler.nuke()` before every equipment image load. The `nuke()` method does the following (confirmed by reading `UserPhotoFragment.java`):

1. Creates an `X509TrustManager` that overrides `checkClientTrusted()` and `checkServerTrusted()` with empty bodies — accepting any certificate from any authority, including self-signed, expired, or attacker-controlled certificates.
2. Initialises an `SSLContext` with this trust-all manager.
3. Calls `HttpsURLConnection.setDefaultSSLSocketFactory(...)` — this replaces the **process-wide default** SSL socket factory. Every subsequent HTTPS connection in the app — including connections to forkliftiqws — uses this broken factory.
4. Calls `HttpsURLConnection.setDefaultHostnameVerifier(...)` with a verifier that always returns `true`, accepting any hostname including mismatched ones.

The `@SuppressLint("TrustAllX509TrustManager")` and `@SuppressLint("BadHostnameVerifier")` annotations confirm the authors were warned by Android Lint and suppressed the warnings instead of fixing them.

**Impact:** After `showImage()` is first called, the app becomes fully vulnerable to man-in-the-middle (MITM) attacks on all HTTPS connections for the remainder of the process lifetime. An attacker on the same network can intercept session tokens, operator credentials, equipment assignment data, and all API traffic to forkliftiqws. Because `setDefaultSSLSocketFactory` is a process-global call, the attack surface is not limited to image loading — it covers every network call the app makes after that point.

**Severity:** Critical

**File:** `EquipmentSelectForkPresenter.java`, line 71
**Supporting file:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/UserPhotoFragment.java`, lines 41–69

---

**MEDIUM — Unvalidated URL passed to image loader**

**File:** `EquipmentSelectForkPresenter.java`, line 57 (`showImage(String url, ImageView imageView)`)

The `url` parameter received by `showImage()` is passed directly to `ImageLoader.getInstance().displayImage(url, ...)` without any validation, scheme check, or whitelist enforcement. If a caller passes an attacker-controlled URL (e.g., through a tampered server response), the image loader will attempt to fetch and display it. Given that SSL validation has already been nuked, this compounds the risk — the loader will happily fetch content from a MITM-injected URL over a falsely-trusted connection.

**Severity:** Medium (elevates to High in combination with the Critical SSL finding above)

---

**Note — EquipmentDriverAccessPresenter.java (Section 2):**

`EquipmentDriverAccessPresenter` imports `javax.net.ssl.HttpsURLConnection` but uses it only for HTTP status code constants (`HTTP_BAD_REQUEST`, `HTTP_BAD_GATEWAY`) on lines 70 and 84. No SSL configuration is performed in this file.

No additional network security issues found in `EquipmentDriverAccessPresenter.java` or `JobsPresenter.java` beyond the global SSL nuke introduced via `EquipmentSelectForkPresenter`.

---

### Section 3: Data Storage

**EquipmentDriverAccessPresenter.java:**
- `SessionDb.saveData()` is called at lines 89 and 276. The `SessionDb` class is not within the assigned files. The call pattern passes `SessionResult` and `EquipmentItem` objects to local storage. Whether this storage is encrypted cannot be determined from this file alone; the `SessionDb` class should be reviewed separately.
- `MyCommonValue.currentEquipmentItem` (lines 45, 48, 118, 277) is a static field used to hold the currently selected equipment item. Static fields on application-scope classes persist for the process lifetime and are accessible from any thread. This is a form of in-memory state sharing. If `MyCommonValue` is a class with broad accessibility, this could expose the equipment item reference. The `MyCommonValue` class is not in the assigned files.
- No direct `SharedPreferences`, file writes, or external storage access observed in the assigned files.

**JobsPresenter.java:**
- `SessionDb.setSessionFinished()` is called on line 123. Same `SessionDb` caveat as above.
- `sessionResult` (line 30) holds the active session result in an instance field for the presenter's lifetime. This includes `sessionResult.id`, `sessionResult.start_time`, and `sessionResult.unit_id` (referenced elsewhere in the codebase). This is appropriate scoping for a presenter; no concern at this level.
- No `SharedPreferences`, file writes, or external storage access in this file.

No issues found directly attributable to the assigned files — Section 3 (Data Storage). `SessionDb` should be examined in a separate audit pass.

---

### Section 4: Input and Intent Handling

**EquipmentDriverAccessPresenter.java — Implicit Intent with extras:**

`startSession()` at line 109 creates an `Intent` targeting `SessionActivity.class` explicitly:
```java
Intent intent = new Intent(getContext(), SessionActivity.class);
intent.putExtra("auto_connect", true);
```
This is an **explicit intent** (class specified directly), which is correct and not interceptable by third-party apps. The extra carried is a boolean `"auto_connect"` — not sensitive data. No issue here.

**EquipmentSelectForkPresenter.java — Unvalidated URL parameter:**

Covered above under Section 2. The `url` string in `showImage(String url, ImageView imageView)` is not validated. No deep link handler or WebView is present in these files.

**No WebView usage** detected in any of the three assigned files.

**No exported component declarations** in any of the three assigned files (presenter classes, not Activities or Services).

No additional issues found — Section 4 (Input and Intent Handling).

---

### Section 5: Authentication and Session

**EquipmentDriverAccessPresenter.java — Session start offline fallback without server confirmation:**

Lines 87–100 (inside the `onFailed` branch of `saveSessionStart`):
```java
SessionResult sessionResult = WebData.getTempSessionResult(parameter);
SessionDb.saveData(sessionResult, equipmentItem, true);
// ... then proceeds to startSession()
```

When the server call to save a new session fails for any reason other than HTTP 400 or 502, the app generates a temporary local session result and proceeds to start the session as if it succeeded. This means a session can be initiated locally without any server-side authentication or authorisation of the session start. While there is clearly an offline-mode design intent here, the logic does not distinguish between a network timeout (legitimate offline scenario) and an authentication/authorisation rejection (e.g., a 401 or 403 response). A server-side rejection for an unauthorised driver would fall into this `else` branch and silently grant local access.

**Severity:** Medium — Authentication bypass in offline fallback

**JobsPresenter.java — Session end: logout on dialog timeout:**

`saveSessionEnd()` at lines 110–113 and 139–141: when the session-end dialog times out (30 seconds, line 96/132), `ui.logout()` is called automatically. This is a positive behaviour — the app does not leave a session in a limbo state indefinitely. No issue.

**JobsPresenter.java — Null check for sessionResult at line 75:**
```java
if (null == sessionResult) {
    ui.showToast(ui.getString(R.string.session_already_stopped));
    return;
}
```
The constructor at line 62 calls `WebData.instance().getSessionResult()` and immediately dereferences `sessionResult.start_time` on line 63 without a null check. If `getSessionResult()` returns null, the constructor throws a `NullPointerException` before `saveSessionEnd()` is ever callable. The null guard at line 75 is therefore unreachable if the constructor was able to complete. Minor logic inconsistency; not a security issue but indicates defensive coding was not applied consistently.

No issues found — Section 5 (Authentication and Session) beyond the offline fallback finding above.

---

### Section 6: Third-Party Libraries

**EquipmentSelectForkPresenter.java:**
- `com.nostra13.universalimageloader` — Universal Image Loader (UIL) is referenced. This library had its last release in 2016 (version 1.9.5) and is confirmed abandoned. It has known issues and no active security maintenance. Its use here is compounded by the SSL nuke applied immediately before each image load.

**JobsPresenter.java:**
- `org.joda.time` — Joda-Time is referenced. While not abandoned, it has been superseded by `java.time` (available from Android API 26) and is no longer the recommended library. No known active CVEs, but it represents unnecessary third-party dependency weight.

**Severity (UIL):** Medium — abandoned library in active use for network image loading, with no SSL certificate validation.

---

### Section 7: Google Play and Android Platform

**JobsPresenter.java — Deprecated `android.os.Handler` constructor:**

Line 35:
```java
private Handler myHandler = new Handler();
```
The no-argument `Handler()` constructor is deprecated as of Android API 30. The deprecation warning exists because this constructor implicitly binds to the current thread's `Looper`, which can cause memory leaks and unexpected behaviour. The recommended replacement is `new Handler(Looper.getMainLooper())` or `new Handler(Looper.myLooper())`. This is a deprecated API usage.

**Severity:** Low — deprecated API, no direct security impact.

**EquipmentDriverAccessPresenter.java — `e.printStackTrace()` at line 78:**

```java
} catch (Exception e) {
    e.printStackTrace();
}
```
Printing stack traces to the system log (`logcat`) can expose internal class names, method names, and package paths to any app with `READ_LOGS` permission or to anyone with ADB access. In a production build, stack traces should be logged to a controlled logging framework or suppressed. This is a low-severity information disclosure.

**Severity:** Low

No other deprecated API or Play Store compliance issues identified within the assigned files.

---

## Summary of Findings

| # | Severity | File | Location | Finding |
|---|----------|------|----------|---------|
| 1 | Critical | `EquipmentSelectForkPresenter.java` | Line 71 | `SSLCertificateHandler.nuke()` called before every image load, globally disabling SSL certificate validation and hostname verification for the entire process via `HttpsURLConnection.setDefaultSSLSocketFactory` and `setDefaultHostnameVerifier`. Enables MITM attacks on all subsequent HTTPS traffic including forkliftiqws API calls. |
| 2 | Medium | `EquipmentSelectForkPresenter.java` | Line 57–72 | `showImage(String url, ...)` accepts an unvalidated URL string and passes it directly to Universal Image Loader with no scheme check or whitelist. Compounds finding #1. |
| 3 | Medium | `EquipmentDriverAccessPresenter.java` | Lines 87–100 | Offline session-start fallback proceeds to grant local session access on any non-400/non-502 server error, including authentication rejections (401/403). Server-side authorisation denial is not distinguished from a network error. |
| 4 | Medium | `EquipmentSelectForkPresenter.java` | Line 5–9 (imports) | Universal Image Loader (`com.nostra13.universalimageloader`) is an abandoned library (last release 2016, no security maintenance) used for network image loading in combination with disabled SSL validation. |
| 5 | Low | `JobsPresenter.java` | Line 35 | `new Handler()` no-argument constructor is deprecated since API 30. Should use `new Handler(Looper.getMainLooper())`. |
| 6 | Low | `EquipmentDriverAccessPresenter.java` | Line 78 | `e.printStackTrace()` in production code; stack traces written to logcat expose internal package/class structure. |
| 7 | Info | `JobsPresenter.java` | Lines 23, 26 | Duplicate import of `au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication`. Code quality defect, no security impact. |
| 8 | Info | Checklist | — | Checklist specifies "Branch: main"; actual branch is "master". Discrepancy recorded. Audit proceeded on master. |

---

*Report produced by agent APP41. Pass 1 review only — findings are based on static reading of the three assigned presenter files and one supporting file (`UserPhotoFragment.java`) referenced directly by the assigned code. No dynamic analysis performed.*
