# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP43
**Date:** 2026-02-27
**Stack:** Android/Java
**Branch Verified:** master

---

## Branch Discrepancy

The checklist specifies Branch: main. The actual current branch is **master**. Audit proceeds on master as instructed.

---

## Reading Evidence

### File 1 — SessionTimeoutJobService.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.session.SessionTimeoutJobService`
**Extends:** `android.app.job.JobService`

**Public methods:**

| Signature | Line |
|---|---|
| `boolean onStartJob(JobParameters params)` | 18 |
| `boolean onStopJob(JobParameters params)` | 32 |

**Package-private (non-public) static methods:**

| Signature | Line |
|---|---|
| `static void schedule(Context context)` | 36 |
| `static void cancel(Context context)` | 46 |

**Constants / fields:**

| Name | Value | Line |
|---|---|---|
| `SESSION_TIMEOUT_JOB_SERVICE_ID` (private static final int) | 1 | 15 |

**Manifest declaration (AndroidManifest.xml, line 105-106):**
```xml
<service android:name=".session.SessionTimeoutJobService"
         android:permission="android.permission.BIND_JOB_SERVICE"/>
```
No `android:exported` attribute is explicitly set on this service declaration.

**Polling interval:** 60,000 ms (60 seconds), set via `JobInfo.Builder.setPeriodic(60000)`.

---

### File 2 — SessionTimeouter.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.session.SessionTimeouter`

**Public methods:**

| Signature | Line |
|---|---|
| `static SessionTimeouter getInstance()` | 30 |
| `void start(Context context)` | 36 |
| `void cancel(Context context)` | 42 |
| `static void register(Activity activity)` | 108 |
| `static void unregister(Activity activity)` | 114 |

**Package-private methods:**

| Signature | Line |
|---|---|
| `void endSession()` | 62 |
| `void showSessionTimeoutWarningDialog(Context context)` | 120 |
| `static void showSessionTimeoutWarningDialog()` (no-arg overload) | 159 |

**Private methods:**

| Signature | Line |
|---|---|
| `private void restart()` | 47 |
| `private void preEndSession()` | 53 |
| `private void onSessionEnded()` | 86 |
| `private static Context getContext()` | 165 |

**Fields / constants:**

| Name | Type | Line |
|---|---|---|
| `instance` | `private static SessionTimeouter` | 27 |
| `warningDisplayed` | `private boolean` | 28 |
| `registrations` | `private static HashMap<Activity, SessionTimeouterReceiver>` | 102 |

**Key behaviour:**
- Singleton (non-synchronized).
- Registers activities with a `Context.registerReceiver()` call using the action string `"MyApplication.INTENT_DISPLAYERROR"`.
- On session end, delegates navigation to `FleetFragment.onSessionEnded()`.
- A `CountDownTimer` of 5 minutes is started when the warning dialog is displayed; if it fires, `endSession()` is called automatically.
- `endSession()` calls `SessionTimeoutJobService.cancel()`, marks the session ended in the Realm DB, and posts the result to the backend via `WebApi`.
- On both API success and API failure (`onFailed`), `onSessionEnded()` is called — ensuring the UI is updated regardless of network outcome.

---

### File 3 — SessionTimeouterReceiver.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.session.SessionTimeouterReceiver`
**Extends:** `android.content.BroadcastReceiver`
**Access modifier:** package-private (`class`, not `public class`)

**Public methods:**

| Signature | Line |
|---|---|
| `void onReceive(Context context, Intent intent)` | 16 |

**Fields:**

| Name | Type | Line |
|---|---|---|
| `context` | `private Context` | 9 |

**Constructor:** `SessionTimeouterReceiver(Activity activity)` — package-private, line 11.

**Key behaviour:** Calls `abortBroadcast()` then delegates to `SessionTimeouter.getInstance().showSessionTimeoutWarningDialog(context)`. Not declared in AndroidManifest.xml — it is registered dynamically via `activity.registerReceiver()` in `SessionTimeouter.register()`.

---

## Checklist Review

### Section 1 — Signing and Keystores

Not applicable to the assigned files. No signing configuration, keystore references, or credentials for build signing are present in any of the three session files.

No issues found — Section 1 (not in scope for assigned files).

---

### Section 2 — Network Security

No HTTP client configuration, URL construction, TrustManager, or HostnameVerifier is present in the three assigned files. Network calls are delegated to `WebApi.async()` which is outside this assignment's scope.

No issues found — Section 2 (not in scope for assigned files).

---

### Section 3 — Data Storage

**Finding S3-1 — Severity: Informational (context-dependent)**
`SessionTimeouter.endSession()` (line 62-84) ends the operator session and posts to the backend, but it does NOT clear credentials, authentication tokens, or cached operator data from storage. Logout (`CurrentUser.logout()` / `WebData.logout()`) is not called anywhere in the session timeout path. When a session times out, the operator is returned to a pre-session state, but the authentication token stored via `ModelPrefs` (plain `SharedPreferences`) and the user identity stored in `ModelPrefs` under `current_user_id` remain intact. This is architecturally intentional for a shift-change device scenario, but it means a timed-out session does not perform a full credential wipe.

Supporting evidence from adjacent files (read for context):
- `ModelPrefs` uses unencrypted `SharedPreferences` (mode `MODE_PRIVATE`) to persist the token (`token_result`) and user ID (`current_user_id`).
- `CurrentUser.logout()` (line 125-128, `CurrentUser.java`) only removes `current_user_id` from prefs and nulls the static `user` field — it does not clear the authentication token stored under `token_result`.
- `FleetFragment.onSessionEnded()` (line 285-286, `FleetFragment.java`) is an empty method body — it provides no credential or session data clearing.

This is raised here because the checklist (Section 5) explicitly requires: "Verify that logout clears all stored credentials, tokens, and cached operator data." The session timeout path does not perform this clearing. Whether this is acceptable depends on the application's operator model; if a single device is shared across multiple operators in shift changes, it may be by design. However, the authentication token persists after timeout, which means any subsequent user of the device can pick up an authenticated session without re-entering credentials.

---

### Section 4 — Input and Intent Handling

**Finding S4-1 — Severity: Medium**

`SessionTimeouterReceiver` is registered dynamically via `activity.registerReceiver()` (line 110, `SessionTimeouter.java`) using the action `"MyApplication.INTENT_DISPLAYERROR"`. On Android versions prior to API 26 (Android 8.0), dynamically registered receivers respond to both local and global broadcasts. The intent action is a plain string — not a local broadcast action.

The registration code:
```java
// SessionTimeouter.java, line 110
activity.registerReceiver(receiver, new IntentFilter("MyApplication.INTENT_DISPLAYERROR"));
```

This is a **standard (global) broadcast registration**, not a `LocalBroadcastManager` registration. Any process on the device — or an external app on pre-Android 8.0 devices — could send a broadcast with action `"MyApplication.INTENT_DISPLAYERROR"` and trigger `showSessionTimeoutWarningDialog()`. This would:
1. Cause a dialog to appear in the foreground of the app.
2. Present the operator with "Continue" and "Terminate" session options.
3. If the operator dismisses the dialog without acting, a 5-minute `CountDownTimer` starts and will call `endSession()` automatically, terminating the operator's active session.

The effect is that a malicious app could force premature session termination by sending this broadcast. On Android 8.0+ (API 26+), implicit broadcasts to dynamically registered receivers from external apps are generally blocked by the platform, mitigating the external vector — but the action string naming convention (`MyApplication.INTENT_DISPLAYERROR`) is generic and suggests this may have been designed for internal use only, while being registered globally.

There is no validation of the intent extras, sender identity, or any permission check in `onReceive()`.

**Evidence from search:** A global-scope broadcast using this action string is only sent in one place — via `LocalBroadcastManager` in `BleControlService.java` (line 75). The `LocalBroadcastManager` send does NOT satisfy the global `registerReceiver()` listener; these are two different registration mechanisms. This means the global registration has no legitimate internal sender and appears to be a leftover or mismatched registration.

**Recommendation:** Change to `LocalBroadcastManager.registerReceiver()` and `LocalBroadcastManager.sendBroadcast()` consistently, or use an explicit intent targeting only the receiver class.

---

**Finding S4-2 — Severity: Low**

`SessionTimeoutJobService` is declared in the manifest without an explicit `android:exported="false"` attribute:

```xml
<!-- AndroidManifest.xml, line 105-106 -->
<service android:name=".session.SessionTimeoutJobService"
         android:permission="android.permission.BIND_JOB_SERVICE"/>
```

The `android:permission="android.permission.BIND_JOB_SERVICE"` attribute restricts binding to callers holding this system permission, which is only grantable to the Android job scheduler system process. This effectively prevents arbitrary third-party apps from binding to the service and calling its job callbacks directly. However, the absence of `android:exported="false"` is a defence-in-depth gap; on some SDK versions the behaviour of omitting this attribute for services differs. Android Lint will flag this for `targetSdkVersion` 31+. Best practice is to explicitly declare `android:exported="false"` since there is no need to export this service to other applications.

---

### Section 5 — Authentication and Session

**Finding S5-1 — Severity: Medium**

The session timeout mechanism (`endSession()` in `SessionTimeouter.java`, lines 62-84) ends the **operator session** (forklift assignment) but does not revoke or clear the **authentication token** or **operator credentials** from device storage. The flow on timeout:
1. `SessionTimeoutJobService.onStartJob()` detects `result.isFinished()` is true.
2. Calls `SessionTimeouter.getInstance().endSession()`.
3. `endSession()` cancels the job, marks the session in Realm DB as ended, posts to the backend.
4. On completion, `onSessionEnded()` notifies UI fragments.

At no point in this chain is `CurrentUser.logout()` or `WebData.logout()` called, nor is the `token_result` SharedPreferences key cleared.

**Impact:** After a session timeout, the app retains a valid bearer token. If the device is left unattended after timeout (the primary scenario this feature is designed for), a new person picking up the device can proceed without authenticating — they are already authenticated at the API level because the token is still present.

The checklist requirement: "Verify that logout clears all stored credentials, tokens, and cached operator data from device storage." — **Not satisfied by the timeout path.**

Note: `CurrentUser.logout()` itself has a secondary deficiency — it does not clear the `token_result` key from SharedPreferences (only `current_user_id` is removed). This means even an intentional logout path leaves the bearer token persisted. This is beyond the scope of the assigned files but is relevant context.

---

**Finding S5-2 — Severity: Low**

`SessionTimeouter` uses a non-synchronized singleton pattern:

```java
// SessionTimeouter.java, lines 27, 30-33
private static SessionTimeouter instance;

public static SessionTimeouter getInstance() {
    if (instance == null)
        instance = new SessionTimeouter();
    return instance;
}
```

`onStartJob()` in `SessionTimeoutJobService` is called on the main thread by the Android job scheduler, and `register()`/`unregister()` are called from Activity lifecycle methods also on the main thread. In normal Android usage this is safe. However, the absence of `synchronized` or a `volatile` keyword means this is technically susceptible to a race condition if any background thread ever calls `getInstance()`. This is a low-risk observation given the threading model, but noted for completeness.

---

**Finding S5-3 — Severity: Informational**

The "Continue" button in the session timeout warning dialog calls `restart()` (line 131, `SessionTimeouter.java`), which re-schedules the timeout job. This is a legitimate session extension mechanism. However, there is no limit on the number of times a user can press "Continue" to extend their session. An operator could indefinitely extend their session beyond the intended `max_session_length` by repeatedly pressing "Continue" on the warning dialog. Whether this is an intended design decision or a policy gap is not determinable from the code alone; it is flagged for review.

---

### Section 6 — Third-Party Libraries

Not applicable to the assigned files. No dependencies are declared or used within the three session files beyond Android SDK classes and internal application classes.

No issues found — Section 6 (not in scope for assigned files).

---

### Section 7 — Google Play and Android Platform

**Finding S7-1 — Severity: Informational**

The support library import in `SessionTimeouter.java` (line 9):
```java
import android.support.v4.app.Fragment;
```
This uses the legacy `android.support` namespace rather than the AndroidX equivalent (`androidx.fragment.app.Fragment`). The Android support library is no longer maintained. This is a project-wide migration concern that surfaces in this file.

---

## Summary of Findings

| ID | Severity | File | Description |
|---|---|---|---|
| S3-1 | Informational | SessionTimeouter.java | Session timeout does not clear authentication token or credentials from storage |
| S4-1 | Medium | SessionTimeouter.java | Global BroadcastReceiver registration for `INTENT_DISPLAYERROR` allows any app to trigger session termination dialog on pre-API-26 devices; mismatched with LocalBroadcastManager sender |
| S4-2 | Low | AndroidManifest.xml | `SessionTimeoutJobService` lacks explicit `android:exported="false"` attribute |
| S5-1 | Medium | SessionTimeouter.java | Timeout path does not revoke bearer token; post-timeout device retains authenticated state |
| S5-2 | Low | SessionTimeouter.java | Singleton `getInstance()` is not synchronized |
| S5-3 | Informational | SessionTimeouter.java | No limit on "Continue" presses in warning dialog; operator can extend session indefinitely |
| S7-1 | Informational | SessionTimeouter.java | Legacy `android.support.v4.app.Fragment` import instead of AndroidX |

---

*Report generated by Agent APP43 — Pass 1 only. No code was modified.*
