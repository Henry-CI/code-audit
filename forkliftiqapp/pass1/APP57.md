# Pass 1 Security Audit — Agent APP57

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Agent ID:** APP57

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist header states `Branch: main`. The actual working branch is `master`. Audit proceeds on `master`.

---

## Reading Evidence

### File 1: SavedReportFragment.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.fragment.SavedReportFragment`

**Superclass:** `FleetFragment` (which extends `BaseFragment`)

**Fields:**
- `private SavedReportListAdapter listAdapter` (line 23)
- `private ArrayList<ReportItem> listData` (line 24) — initialized to empty `ArrayList`

**Public methods:**
- `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 28 (overrides Fragment)
- `public void initViews()` — line 33

**Package-private / non-public methods:**
- `private void loadData()` — line 45
- `private void onData(ReportResultArray resultArray)` — line 65
- `void onResend(ReportItem reportItem)` — line 71 (package-private; called by adapter)

**Key behaviours:**
- `loadData()` at line 47 calls `WebApi.async().getReports(WebData.instance().getUserId(), ...)` — passes authenticated user ID to web API.
- `onResend()` at line 73 calls `WebApi.async().resendReport(WebData.instance().getUserId(), reportItem.id, ...)` — passes user ID and report ID to re-trigger report submission.

---

### File 2: SavedReportListAdapter.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.fragment.SavedReportListAdapter`

**Superclass:** `ArrayAdapter<ReportItem>`

**Fields:**
- `private Context context` — line 18
- `private ArrayList<ReportItem> mData` — line 19
- `SavedReportFragment savedReportFragment` — line 20 (package-private; set directly by fragment at line 40 of SavedReportFragment)

**Public methods:**
- `public View getView(int position, View convertView, @NonNull ViewGroup parent)` — line 30 (overrides ArrayAdapter)
- `public int getCount()` — line 61 (overrides ArrayAdapter)
- `public ReportItem getItem(int i)` — line 66 (overrides ArrayAdapter)

**Package-private methods:**
- `SavedReportListAdapter(Context context, ArrayList<ReportItem> data)` — line 22 (package-private constructor)

**Static nested class:**
- `static class ListHolder` — line 70; fields: `TextView name`, `View resend_report_view`

**Key behaviours:**
- `getView()` at line 47 calls `Objects.requireNonNull(recordItem).name` — display name drawn directly from server data without sanitisation.
- Click listener at line 48-54 delegates directly to `savedReportFragment.onResend(recordItem)`.

---

### File 3: ServiceEditFragment.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.fragment.ServiceEditFragment`

**Superclass:** `FleetFragment`

**Fields:**
- `private static String TAG` — line 39 (class name string, not a secret)
- `ArrayList<ServiceRecordItem> mRecordItems` — line 41
- `int mCurrentIndex` — line 42
- `ServiceRecordItem mServiceRecordItem` — line 43
- `TextView status_text` — line 45
- `TextView hours_to_next_service` — line 46
- `TextView accumulate_hour` — line 47
- `RadioImageButton toggle_by_hours` — line 48
- `RadioImageButton toggle_by_interval` — line 49
- `EditText service_at` — line 50
- `EditText service_interval` — line 51
- `TextView service_title` — line 52
- `View previous_record` — line 53
- `View next_record` — line 54
- `TextView equipment_name` — line 55
- `public boolean fromProfile` — line 56 (public field)

**Public methods:**
- `public static ServiceEditFragment createInstance(ArrayList<ServiceRecordItem> recordItems, int currentIndex)` — line 58
- `public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 67 (overrides Fragment)
- `public void initViews()` — line 73 (overrides FleetFragment)
- `public void onMiddleButton(View view)` — line 241 (overrides FleetFragment)
- `public void onRightButton(View view)` — line 248 (overrides FleetFragment)

**Package-private methods:**
- `void setData()` — line 137
- `void initNaviButton()` — line 177
- `void onNext()` — line 197
- `void onPrevious()` — line 208
- `void updateServiceTitle()` — line 218
- `ServiceRecordItem getCurrentRecordItem()` — line 231
- `void onServiceEdited()` — line 345 (empty stub)

**Key behaviours:**
- `onRightButton()` at lines 248-342 reads raw `EditText` values, converts to `Integer` via `Integer.valueOf()`, applies boundary checks, builds a parameter packet, and submits via `WebApi.async().saveService(...)`.
- `parameter.driver_id = WebData.instance().getUserId()` at lines 289 and 300 — user ID injected into the service-save parameters.

---

## Section-by-Section Findings

### 1. Signing and Keystores

No `.jks`, `.keystore`, or `.p12` files are referenced or present in the three assigned files. No `signingConfigs` blocks, `build.gradle` content, or keystore property references appear in these files.

**No issues found — Section 1** (within scope of assigned files).

---

### 2. Network Security

No hardcoded API endpoint URLs, IP addresses, or base URL strings appear in any of the three assigned files. Calls to `WebApi.async().getReports(...)`, `WebApi.async().resendReport(...)`, and `WebApi.async().saveService(...)` are delegated to the `WebApi` class and do not encode URLs directly.

No `TrustAllCertificates`, `hostnameVerifier`, or `SSLContext` patterns appear in these files.

**Note (contextual, from WebData.java which was read to understand getUserId()):** `WebData.getTokenFormData()` (lines 56-82 of WebData.java) contains hardcoded OAuth2 client credentials:
- `clientId = "987654321"` (line 64)
- `clientSecret = "8752361E593A573E86CA558FFD39E"` (line 68)
- `userName = "gas"` (line 72)
- `password = "ciiadmin"` (line 76)

These hardcoded credentials are in a support file read to understand context for the assigned files, not in the three assigned files themselves. They are included here as an observation should another agent not have flagged them. They are not attributed as a finding against APP57's assigned files.

**No issues found — Section 2** (within assigned file scope).

---

### 3. Data Storage

**Finding DS-1 — Medium: Auth token stored in plain SharedPreferences**

`SavedReportFragment.loadData()` (line 47) and `onResend()` (line 73) invoke `WebData.instance().getUserId()`. Tracing the call chain:

- `WebData.getUserId()` calls `CurrentUser.get()`, which reads from `ModelPrefs.readInt(CURRENT_USER_ID_KEY)`.
- `ModelPrefs` (confirmed by reading ModelPrefs.java) stores all data in a plain `SharedPreferences` file named `"prefs"` with `Context.MODE_PRIVATE`.
- `WebData.setGetTokenResult()` persists the auth token (`GetTokenResult`) via `ModelPrefs.saveObject(TOKEN_ITEM_KEY, result)` — serialised as JSON to the same plain `SharedPreferences` store.

The OAuth2 bearer token used to authenticate all API calls (including the `getReports` and `resendReport` calls originating in these fragments) is stored in plain, unencrypted `SharedPreferences`. `EncryptedSharedPreferences` from Jetpack Security is not used. On a rooted device, or via backup extraction if `allowBackup` is not set to `false`, this token is recoverable in plaintext.

Relevant call path from assigned files:
- `SavedReportFragment.java` line 47: `WebData.instance().getUserId()`
- `SavedReportFragment.java` line 73: `WebData.instance().getUserId()`
- `ServiceEditFragment.java` line 289: `parameter.driver_id = WebData.instance().getUserId()`
- `ServiceEditFragment.java` line 300: `parameter.driver_id = WebData.instance().getUserId()`

All three assigned files depend on `WebData.instance()` and thereby on the unencrypted credential store.

**Finding DS-2 — Medium: Operator password stored in local Realm database without encryption**

`CurrentUser.setUser(LoginItem)` (CurrentUser.java line 37, read for context) calls `UserDb.save(createUser(loginItem))`, passing `loginItem.password` into the `User` object. `UserDb.save()` persists the `User` — including the password field — into Realm. `UserDb.get(String email, String password)` at line 55-63 of UserDb.java performs a direct plaintext password match query against the Realm store.

The `CurrentUser.get()` method called from `WebData.getUserId()` (used by all three assigned fragments) reads from this same store. The Realm database is not configured with encryption in the files examined. Operator passwords are therefore at rest in plaintext in the local Realm database, recoverable on rooted devices.

**No issues found — Section 3 (external storage, `MODE_WORLD_READABLE`, static field lifetime):** No `Environment.getExternalStorageDirectory()`, `openFileOutput()`, or long-lived static credential fields are present in the three assigned files themselves.

---

### 4. Input and Intent Handling

**Finding IH-1 — Low: Missing try/catch around Integer.valueOf() in ServiceEditFragment.onRightButton()**

`ServiceEditFragment.onRightButton()` at lines 253-254 and 260-261:

```java
String sa = service_at.getText().toString();
Integer lastService = Integer.valueOf(sa);   // line 254

sa = service_interval.getText().toString();
Integer serviceInterval = Integer.valueOf(sa);  // line 261
```

`Integer.valueOf(String)` throws `NumberFormatException` if the input string is not a valid integer (e.g., empty string, floating-point value like `"3.5"`, or non-numeric input). There is no `try/catch` block wrapping these calls and no `null`-check is possible to guard this — `Integer.valueOf()` never returns `null` for a non-parseable string; it throws. The subsequent null-checks at lines 255 and 262 (`if (null == lastService)`) are dead code: they can never be `true`, because `Integer.valueOf()` either returns a non-null `Integer` or throws an uncaught exception.

If a user enters a non-integer value (decimal, empty, special character), the fragment will crash with an unhandled `NumberFormatException`. This is a robustness/denial-of-service issue at the UI level — a legitimate user can inadvertently crash the fragment.

No WebView usage, deep link handlers, implicit intents carrying sensitive data, or exported component patterns are present in the three assigned files.

**No issues found — Section 4 (WebView, deep links, implicit intents with sensitive data).**

---

### 5. Authentication and Session

**Finding AS-1 — Medium: Logout does not clear the auth token from SharedPreferences**

`WebData.logout()` (line 108-110 of WebData.java, read for context) calls `CurrentUser.logout()`. `CurrentUser.logout()` (lines 125-128 of CurrentUser.java) deletes only `CURRENT_USER_ID_KEY` from `ModelPrefs` and sets `user = null` in the static field.

The auth token (`TOKEN_ITEM_KEY` / `"token_result"`) stored in `ModelPrefs` via `WebData.setGetTokenResult()` is **not cleared** on logout. After logout, a subsequent call to `WebData.getTokenString()` will reload the token from `SharedPreferences` and the `getAuthHeader()` method will return a valid Bearer header. This is directly relevant to the assigned fragments: if a second operator logs in after the first logs out, the stale bearer token may persist and be used in API calls made from `SavedReportFragment` and `ServiceEditFragment` until a new `getToken` request overwrites it — or indefinitely if the second session uses offline mode.

The `loginPassword` and `loginEmail` static fields in `CurrentUser` (lines 22-23) are also not cleared on logout, though these are transient login-flow fields.

**Finding AS-2 — Low: Static loginPassword field retains MD5-hashed password in memory after login**

`CurrentUser.loginPassword` (line 23) is a `static String` field set at `setTemporaryLoginInformation()` (line 121) and never cleared. It holds the MD5 hash of the operator's password for the duration of the application's process lifetime, surviving across shift changes. While MD5 is not reversible trivially, keeping a credential derivative in a static field beyond the authentication handshake violates least-privilege and the checklist requirement that credentials not be cached in memory beyond their useful lifetime. This field is never nulled out in `logout()`.

**No issues found — Section 5 (token expiry handling in assigned files):** The assigned fragments do not implement token refresh logic themselves; they delegate to `WebApi.async()`. No session token handling code is present in the three files.

---

### 6. Third-Party Libraries

No `build.gradle` content, dependency declarations, or ProGuard configuration appears in the three assigned files.

**No issues found — Section 6** (within assigned file scope).

---

### 7. Google Play and Android Platform

**Finding GP-1 — Low: Use of deprecated `startActivityForResult` in FleetFragment**

`FleetFragment.startConnect()` (line 228 of FleetFragment.java, read as the base class of all three assigned fragments) calls `getActivity().startActivityForResult(enableGPS, LOCATION_SETTINGS_REQUEST_GPS)`. `startActivityForResult` is deprecated in `androidx.activity` 1.2+ in favour of the Activity Result API. All three assigned fragments inherit from `FleetFragment` and therefore transitively use the deprecated API path when GPS is enabled.

**Finding GP-2 — Low: Support library annotations instead of AndroidX**

All three assigned files import `android.support.annotation.NonNull` and/or `android.support.annotation.Nullable` (the legacy Android Support Library). The modern equivalent is `androidx.annotation`. This indicates the project has not migrated to AndroidX, which means it is pinned to an end-of-life support library ecosystem.

**No issues found — Section 7 (AsyncTask, runtime permission request handling in assigned files):** `FleetFragment` does handle `ACCESS_FINE_LOCATION` permission at runtime correctly via `checkSelfPermission` and `requestPermissions`. No `AsyncTask` usage appears in the three assigned files.

---

## Summary of Findings

| ID    | Severity | Section             | File(s)                                  | Description |
|-------|----------|---------------------|------------------------------------------|-------------|
| DS-1  | Medium   | 3 — Data Storage    | SavedReportFragment.java, ServiceEditFragment.java (via WebData) | Auth token stored in plain unencrypted SharedPreferences; recoverable on rooted device or via ADB backup |
| DS-2  | Medium   | 3 — Data Storage    | SavedReportFragment.java, ServiceEditFragment.java (via WebData / UserDb) | Operator password stored in Realm database without encryption; plaintext password query at rest |
| AS-1  | Medium   | 5 — Auth & Session  | SavedReportFragment.java, ServiceEditFragment.java (via WebData.logout) | Logout does not clear bearer token from SharedPreferences; token persists for subsequent operators |
| IH-1  | Low      | 4 — Input Handling  | ServiceEditFragment.java lines 254, 261 | `Integer.valueOf()` called without try/catch; dead null-check guards; non-numeric input causes uncaught `NumberFormatException` crash |
| AS-2  | Low      | 5 — Auth & Session  | (CurrentUser.java static field, used by all assigned files) | Static `loginPassword` field holds MD5-hashed password beyond authentication; never cleared on logout |
| GP-1  | Low      | 7 — Platform        | FleetFragment.java (base class of all three assigned files) | `startActivityForResult` is deprecated; inherited by all three assigned fragments |
| GP-2  | Low      | 7 — Platform        | All three assigned files | Android Support Library annotations used instead of AndroidX equivalents |

---

*Report generated by Agent APP57. Audit date: 2026-02-27.*
