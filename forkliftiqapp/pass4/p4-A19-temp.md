# Pass 4 — Code Quality Audit
**Agent:** A19
**Audit run:** 2026-02-26-01
**Files:** WebApi.java, WebData.java, WebListener.java

---

## Step 1: Reading Evidence

### File 1 — `WebApi.java`
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebApi.java`
**Class:** `WebApi`

**Fields:**
- `private static Context mContext` (line 19) — annotated `@SuppressLint("StaticFieldLeak")`
- `private boolean isSynchronous` (line 20)
- `private HttpClient httpClient` (line 21)

**Methods (exhaustive, with line numbers):**
| Line | Method |
|------|--------|
| 23 | `public static WebApi sync()` |
| 31 | `public static WebApi async()` |
| 39 | `public static void init(Context context)` |
| 43 | `private <T> void enqueueRequest(GsonRequest<T> gsonRequest)` |
| 47 | `public void resendReport(int uid, int rid, final WebListener<CommonResult> resultListener)` |
| 51 | `public void saveShockEvent(SaveShockEventParameter parameter, final WebListener<CommonResult> resultListener)` |
| 55 | `public void updateUser(int uid, UpdateUserParameter parameter, final WebListener<CommonResult> resultListener)` |
| 59 | `public void addEquipment(AddEquipmentParameter parameter, final WebListener<CommonResult> resultListener)` |
| 63 | `public void getEmails(int uid, final WebListener<GetEmailResult> resultListener)` |
| 67 | `public void getReports(int uid, final WebListener<ReportResultArray> resultListener)` |
| 71 | `public void getEquipmentStats(int uid, int frequency, final WebListener<EquipmentStatsResultArray> resultListener)` |
| 84 | `public void getDriverStats(int uid, final WebListener<GetDriverStatsResultArray> resultListener)` |
| 88 | `public void saveService(WebServiceParameterPacket parameter, final WebListener<WebServiceResultPacket> resultListener)` |
| 92 | `public void getServiceRecord(int uid, final WebListener<ServiceRecordResultArray> resultListener)` |
| 96 | `void authApp(final WebListener<GetTokenResult> resultListener)` — package-private |
| 112 | `public void resetPassword(final ResetPasswordParameter parameter, final WebListener<WebServiceResultPacket> resultListener)` |
| 131 | `public void login(final LoginParameter parameter, final WebListener<LoginResultArray> resultListener)` |
| 150 | `public void register(final UserRegisterParameter parameter, final WebListener<LoginItem> resultListener)` |
| 187 | `public void setupEmails(SetEmailsParameter parameter, final WebListener<WebServiceResultPacket> resultListener)` |
| 192 | `public void getEquipmentList(final int userId, final WebListener<GetEquipmentResultArray> resultListener)` |
| 210 | `public void getPreStartQuestionList(final int eid, final WebListener<PreStartQuestionResultArray> resultListener)` |
| 226 | `public void savePreStartResult(final SavePreStartParameter parameter, final WebListener<WebServiceResultPacket> resultListener)` |
| 243 | `public void saveSessionStart(final EquipmentItem equipmentItem, final SessionStartParameter parameter, final WebListener<SessionResult> resultListener)` |
| 265 | `public void syncSaveSession(SaveSessionsParameter parameter, final WebListener<SessionResult> resultListener)` |
| 269 | `public void deleteSession(final int sessionId, final WebListener<WebServiceResultPacket> resultListener)` |
| 286 | `public void saveSessionPreEnd(SessionResult sessionResult, SessionEndParameter parameter, WebListener<SessionEndResult> resultListener)` |
| 300 | `public void saveSessionEnd(SessionResult sessionResult, final SessionEndParameter parameter, final WebListener<SessionEndResult> resultListener)` |
| 321 | `public void getManufacture(final WebListener<ManufactureResultArray> resultListener)` |
| 325 | `public void getEquipmentType(int mid, final WebListener<EquipmentTypeResultArray> resultListener)` |
| 329 | `public void getFuelType(int mid, int etype, final WebListener<FuelTypeResultArray> resultListener)` |
| 333 | `public void saveLicense(SaveLicenseParameter parameter, final WebListener<SaveLicenseResult> resultListener)` |
| 337 | `public void saveImpact(ImpactParameter parameter, final WebListener<SaveImpactResult> resultListener)` |
| 341 | `public void saveSingleGPSLocation(SaveSingleGPSParameter parameter, final WebListener<SaveSingleGPSResult> resultListener)` |
| 345 | `public void saveMultipleGPSLocation(SaveMultipleGPSParameter parameter, final WebListener<SaveMultipleGPSResult> resultListener)` |

**Annotations observed:**
- `@SuppressLint("StaticFieldLeak")` on field `mContext` (line 18) and method `getEquipmentList` (line 191) and `getPreStartQuestionList` (line 209)

**Imports:**
- `android.os.AsyncTask` — imported but never used in this file (line 5)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveGPSLocationItem` — imported but not directly referenced (line 8)
- `au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication` — imported but not directly referenced (line 14)

---

### File 2 — `WebData.java`
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebData.java`
**Class:** `WebData` — singleton

**Fields:**
- `private static WebData ourInstance` (line 21)
- `private final static String authHeaderType = "Authorization"` (line 22)
- `private final static int MAC_ADDRESS_LENGTH = 17` (line 23)
- `private GetTokenResult getTokenResult` (line 25)
- `private final static String TOKEN_ITEM_KEY = "token_result"` (line 27)

**Methods (exhaustive, with line numbers):**
| Line | Method |
|------|--------|
| 29 | `public static int getTempSessionId()` |
| 36 | `static boolean isOffline()` — package-private |
| 40 | `public static boolean isSessionOffline(int sessionId)` |
| 46 | `public static SessionResult getTempSessionResult(SessionStartParameter parameter)` |
| 56 | `public String getTokenFormData()` |
| 84 | `public static WebData instance()` — singleton accessor |
| 91 | `void setGetTokenResult(GetTokenResult result)` — package-private |
| 96 | `public SessionResult getSessionResult()` |
| 100 | `public void onSessionEnded()` |
| 104 | `public static boolean isValidMacAddress(String address)` |
| 108 | `public void logout()` |
| 112 | `public int getUserId()` |
| 117 | `private String getTokenString()` |
| 124 | `boolean isAppInitialized()` — package-private |
| 129 | `void setHttpHeaderForConnection(HttpURLConnection connection)` — package-private |
| 134 | `String getAuthHeader()` — package-private |
| 138 | `void setHttpHeader(boolean authMessage, Map<String, String> header)` — package-private |

**Constants / string literals of note (within `getTokenFormData`, lines 60–76):**
- `grant_type` = `"password"`
- `client_id` = `"987654321"`
- `client_secret` = `"8752361E593A573E86CA558FFD39E"`
- `username` = `"gas"`
- `password` = `"ciiadmin"`

---

### File 3 — `WebListener.java`
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebListener.java`
**Class:** `WebListener<T>` — generic base class (concrete class used as callback, not an interface)

**Fields:**
- `private static final String TAG = "WebListener"` (line 9)

**Methods (exhaustive, with line numbers):**
| Line | Method |
|------|--------|
| 11 | `public void onSucceed(T result)` — empty body |
| 13 | `public void onFailed(WebResult result)` — empty body |

**No constants, enums, or interfaces defined.**

---

## Step 2 & 3: Findings

---

### A19-1 — CRITICAL: Hardcoded OAuth credentials in production source code

**File:** `WebData.java`, lines 59–77
**Method:** `getTokenFormData()`

Hardcoded OAuth2 credentials are embedded directly in source:

```java
String clientId = "987654321";
String clientSecret = "8752361E593A573E86CA558FFD39E";
String userName = "gas";
String password = "ciiadmin";
```

These values are stored as local variables inside the method body and assembled into a URL-encoded form string. Because they live in version-controlled source code, every developer with repository access, every build artifact, and every decompilable APK exposes these credentials. A client secret must be treated as a secret; it does not belong in source. The `client_id` value (`987654321`) and the application-level credentials (`gas` / `ciiadmin`) compound the exposure.

**Impact:** Full OAuth token issuance capability for anyone who decompiles the APK or reads the source. The credentials cannot be rotated without a code change and new release.

---

### A19-2 — HIGH: Unused import of deprecated `android.os.AsyncTask`

**File:** `WebApi.java`, line 5

```java
import android.os.AsyncTask;
```

`AsyncTask` is never used anywhere in `WebApi.java`. Its presence generates an "unused import" compiler warning. More critically, `AsyncTask` itself was deprecated in Android API level 30 (Android 11) and has been fully removed in API 33 (Android 13) in the platform source. Importing it signals either leftover scaffolding from an earlier implementation attempt or copy-paste remnants, and it may cause confusion about whether background tasks in this class are handled by `AsyncTask`.

---

### A19-3 — HIGH: Null-pointer dereference risk in `getEquipmentStats` when frequency is out of range

**File:** `WebApi.java`, lines 71–82

```java
public void getEquipmentStats(int uid, int frequency, ...) {
    //frequency=0:weekly,1:monthly,2:yearly
    UrlItem urlItem = null;
    if (frequency == 0) {
        urlItem = URLBuilder.urlGetEquipmentStatsWeekly(uid);
    } else if (frequency == 1) {
        urlItem = URLBuilder.urlGetEquipmentStatsMonthly(uid);
    } else if (frequency == 2) {
        urlItem = URLBuilder.urlGetEquipmentStatsYearly(uid);
    }
    enqueueRequest(new GsonRequest<>(urlItem, null, ...));
}
```

If `frequency` is any value other than 0, 1, or 2, `urlItem` remains `null`. `GsonRequest` and `WebRequest` constructors both dereference `urlItem` (e.g. `urlItem.method`, `urlItem.url`) without null-checking. This will produce a `NullPointerException` at runtime. There is no `else` branch that logs or propagates an error, no guard or validation at the call site, and the comment encoding the valid range is informal only.

---

### A19-4 — HIGH: Non-thread-safe singleton in `WebData.instance()`

**File:** `WebData.java`, lines 84–89

```java
public static WebData instance() {
    if (ourInstance == null) {
        ourInstance = new WebData();
    }
    return ourInstance;
}
```

This is a classic "check-then-act" race. Two threads calling `instance()` simultaneously when `ourInstance` is `null` can each pass the null check and each construct a separate `WebData`. Because `WebData` holds mutable state (the OAuth token `getTokenResult`, and it writes to `ModelPrefs`), this can result in one thread losing its token state. The field `ourInstance` is not `volatile` and the method is not `synchronized`. In this application context, background sync services and UI threads both call `WebData.instance()` concurrently.

---

### A19-5 — HIGH: `@SuppressLint("StaticFieldLeak")` on static `Context` field — real leak suppressed

**File:** `WebApi.java`, lines 18–19

```java
@SuppressLint("StaticFieldLeak")
private static Context mContext;
```

The annotation does not fix the underlying leak; it silences the lint warning. A static `Context` field outlives any individual `Activity` and prevents GC of the entire view hierarchy rooted at that context. The field is assigned by `WebApi.init(context)` (line 39–41) and the caller is responsible for passing an appropriate context (ideally `ApplicationContext`), but nothing enforces this. The suppression also appears redundantly on `getEquipmentList` (line 191) and `getPreStartQuestionList` (line 209), which do not themselves declare static fields — those annotations on instance methods are meaningless and add noise.

---

### A19-6 — MEDIUM: `WebListener` is a concrete class with empty bodies instead of an interface or abstract class

**File:** `WebListener.java`, lines 7–17

```java
public class WebListener<T> {
    private static final String TAG = "WebListener";

    public void onSucceed(T result){}

    public void onFailed(WebResult result){

    }
}
```

Callers subclass `WebListener` and override only the callbacks they care about. Using a concrete class with empty defaults rather than an interface means:
1. Callers that forget to override `onFailed` silently swallow errors — there is no compiler enforcement.
2. Callers that override neither method (a legal subclass) produce a completely inert callback, with no warning.
3. `WebListener` cannot be composed alongside other class hierarchies because Java is single-inheritance.

An interface (or abstract class with at minimum `onFailed` as abstract) would catch both problems at compile time. The existing pattern has already produced at least one real bug: several call sites in the codebase provide only `onSucceed`, meaning failures are silently ignored.

---

### A19-7 — MEDIUM: `TAG` field in `WebListener` is unused dead code

**File:** `WebListener.java`, line 9

```java
private static final String TAG = "WebListener";
```

This field is declared but never referenced anywhere in `WebListener.java`. Both callback methods have empty bodies with no logging. The field will generate an "unused field" compiler warning. It is residual scaffolding from an earlier version that had logging.

---

### A19-8 — MEDIUM: `authApp` is package-private but is called from `HttpClient` in the same package — leaky design coupling

**File:** `WebApi.java`, line 96
**Caller:** `HttpClient.java`, line 250

```java
// WebApi.java
void authApp(final WebListener<GetTokenResult> resultListener) { ... }

// HttpClient.java
WebApi.async().authApp(new WebListener<GetTokenResult>(){ ... });
```

`HttpClient` (transport layer) reaches up into `WebApi` (API facade layer) to re-trigger authentication. This inverts the intended dependency direction: `WebApi` depends on `HttpClient` for all requests, and `HttpClient` should not depend on `WebApi`. The result is a circular dependency between `WebApi` and `HttpClient`. `authApp` is package-private specifically to enable this back-channel; it cannot be `private` and the access cannot be expressed cleanly. Any refactoring of the auth flow must be aware of both classes simultaneously.

---

### A19-9 — MEDIUM: Duplicate auth-bootstrap pattern — `resetPassword`, `login`, and `register` repeat identical boilerplate

**File:** `WebApi.java`, lines 112–185

All three methods follow the same two-branch pattern:

```java
if (WebData.instance().isAppInitialized()) {
    enqueueRequest(new GsonRequest<>(...));
    return;
}
authApp(new WebListener<GetTokenResult>() {
    @Override public void onSucceed(GetTokenResult result) {
        enqueueRequest(new GsonRequest<>(...));
    }
    @Override public void onFailed(WebResult webResult) {
        resultListener.onFailed(webResult);
    }
});
```

The `enqueueRequest(...)` call for the actual endpoint is duplicated in both branches every time. This is copy-paste code: three separate call sites encode the same "ensure token then call" logic. If the auth-bootstrap behavior needs to change (e.g., token refresh instead of re-auth), all three sites must be updated consistently. A helper method accepting a `Runnable` or a lambda would eliminate the duplication.

---

### A19-10 — MEDIUM: Two unused imports in `WebApi.java`

**File:** `WebApi.java`, lines 8 and 14

```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveGPSLocationItem;
import au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication;
```

Neither `SaveGPSLocationItem` nor `MyApplication` is referenced directly anywhere in `WebApi.java`'s method bodies or field declarations. Both generate unused-import compiler warnings. `SaveGPSLocationItem` is used in `SaveMultipleGPSParameter` (a parameter type that is passed through opaquely), not in `WebApi` itself. `MyApplication` is used in `WebData.java` but not here.

---

### A19-11 — MEDIUM: Inconsistent access modifier discipline on `WebData` methods

**File:** `WebData.java`

Several methods intended as internal implementation details have inconsistent visibility:

| Method | Declared visibility | Notes |
|--------|-------------------|-------|
| `isOffline()` | package-private | Correct — internal |
| `setGetTokenResult(...)` | package-private | Correct — internal |
| `isAppInitialized()` | package-private | Correct — internal |
| `setHttpHeaderForConnection(...)` | package-private | But `setHttpHeader(...)` is also package-private and duplicates purpose |
| `getAuthHeader()` | package-private | Called from `HttpClient.syncSendRequest` directly |
| `getTokenFormData()` | **`public`** | Returns the hardcoded credential string; should be package-private at most |
| `isValidMacAddress(...)` | **`public static`** | Utility method on `WebData` with no relation to `WebData` instance state; misplaced |

`getTokenFormData()` being `public` exposes credential-assembly logic to the entire application. `isValidMacAddress` is a static utility that belongs in a BLE or validation utility class, not on the network-layer singleton.

---

### A19-12 — LOW: Inline local variable declarations for string keys inside `getTokenFormData`

**File:** `WebData.java`, lines 59–77

String key constants (`KEY_GRANT_TYPE`, `KEY_CLIENT_ID`, etc.) are declared as local variables inside the method body rather than as class-level `private static final` constants. This is unusual — it creates the visual illusion of constants without compile-time deduplication across methods or classes, and the names (`KEY_GRANT_TYPE`) suggest they were originally intended as class-level constants.

---

### A19-13 — LOW: `saveSessionPreEnd` modifies the `SessionEndParameter` argument in-place before the offline short-circuit

**File:** `WebApi.java`, lines 286–297

```java
public void saveSessionPreEnd(SessionResult sessionResult,
                              SessionEndParameter parameter,
                              WebListener<SessionEndResult> resultListener) {
    parameter.prestart_required = sessionResult.prestart_required;
    SessionDb.setSessionPreFinish(sessionResult.id, parameter.finish_time);

    if (WebData.isSessionOffline(parameter.id) && !isSynchronous && resultListener != null) {
        resultListener.onSucceed(new SessionEndResult());
        return;
    }
    enqueueRequest(new GsonRequest<>(URLBuilder.urlSessionEnd(), parameter, ...));
}
```

The caller's `parameter` object is mutated before the method has finished deciding whether to proceed. If the caller holds a reference to `parameter` and inspects it after the call, it will observe the mutation regardless of whether an HTTP request was actually made. The same mutation also occurs in `saveSessionEnd` (line 303) for a different method, so there is duplication of this side-effect. The mutation is a hidden side-effect not signalled by the method signature.

---

### A19-14 — LOW: `WebListener` class file copyright/author comment predates the codebase name

**File:** `WebListener.java`, lines 2–6

```java
/**
 * ==================================
 * Created by michael.carr on 8/09/2014.
 * ==================================
 */
```

The comment is from 2014 (the product was formerly `FleetIQ360`). This is purely informational — it is not a code defect — but it is the only comment in the file and provides no useful API documentation. The two empty callback methods have no Javadoc explaining the contract (e.g., on which thread they are called, whether they can be called multiple times, whether `result` can be null in `onSucceed`).

---

## Summary Table

| ID | Severity | File | Issue |
|----|----------|------|-------|
| A19-1 | CRITICAL | WebData.java:59–77 | Hardcoded OAuth credentials (client_secret, username, password) in source |
| A19-2 | HIGH | WebApi.java:5 | Unused import of deprecated `android.os.AsyncTask` |
| A19-3 | HIGH | WebApi.java:71–82 | Null `urlItem` causes NPE when `frequency` argument is out of range 0–2 |
| A19-4 | HIGH | WebData.java:84–89 | Non-thread-safe singleton (no `volatile`, no `synchronized`) |
| A19-5 | HIGH | WebApi.java:18–19,191,209 | `@SuppressLint("StaticFieldLeak")` suppresses real static Context leak; redundant uses on instance methods |
| A19-6 | MEDIUM | WebListener.java:7–17 | Concrete class with empty bodies instead of interface/abstract class; silent failure on un-overridden `onFailed` |
| A19-7 | MEDIUM | WebListener.java:9 | `TAG` field declared but never used — dead code |
| A19-8 | MEDIUM | WebApi.java:96 / HttpClient.java:250 | Circular dependency: `HttpClient` calls back into `WebApi.authApp()` |
| A19-9 | MEDIUM | WebApi.java:112–185 | Triply-duplicated "ensure token then call" boilerplate in `login`, `resetPassword`, `register` |
| A19-10 | MEDIUM | WebApi.java:8,14 | Two unused imports: `SaveGPSLocationItem`, `MyApplication` |
| A19-11 | MEDIUM | WebData.java | Inconsistent access visibility; `getTokenFormData()` is `public`; `isValidMacAddress` misplaced |
| A19-12 | LOW | WebData.java:59–77 | String key constants declared as local variables instead of class-level `private static final` |
| A19-13 | LOW | WebApi.java:286–297 | `saveSessionPreEnd` mutates caller-owned `parameter` as a side-effect before the offline short-circuit |
| A19-14 | LOW | WebListener.java:2–6 | No Javadoc on public API; stale author comment is only documentation |
