# Pass 1 Security Audit — APP05
**Agent:** APP05
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android / Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist states `Branch: main`. The actual current branch is `master`. Branch is confirmed as `master`; audit proceeds.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/GPS/LocationProvider.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/GetDriverStatsResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/GsonRequest.java`

---

## Reading Evidence

### File 1: LocationProvider.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.GPS.LocationProvider`

**Public methods (with line numbers):**

| Line | Signature |
|------|-----------|
| 120 | `public void init(Context context, boolean requireFine, boolean passive, long interval, boolean requireNewLocation)` |
| 134 | `public static LocationProvider instance()` |
| 143 | `public LocationProvider()` (constructor) |
| 152 | `public void setListener(Listener listener)` |
| 161 | `public boolean hasLocationEnabled()` |
| 175 | `public void beginUpdates()` |
| 189 | `public void endUpdates()` |
| 234 | `public Point getPosition()` |
| 249 | `public double getLatitude()` |
| 264 | `public double getLongitude()` |
| 279 | `public long getTimestampInMilliseconds()` |
| 293 | `public long getElapsedTimeInNanoseconds()` |
| 312 | `public float getSpeed()` |
| 326 | `public double getAltitude()` |
| 340 | `public void setBlurRadius(int blurRadius)` |
| 462 | `public static void openSettings(Context context)` |
| 472 | `public static double latitudeToKilometer(double latitude)` |
| 481 | `public static double kilometerToLatitude(double kilometer)` |
| 491 | `public static double latitudeToMeter(double latitude)` |
| 500 | `public static double meterToLatitude(double meter)` |
| 511 | `public static double longitudeToKilometer(double longitude, double latitude)` |
| 521 | `public static double kilometerToLongitude(double kilometer, double latitude)` |
| 532 | `public static double longitudeToMeter(double longitude, double latitude)` |
| 542 | `public static double meterToLongitude(double meter, double latitude)` |
| 553 | `public static double calculateDistance(Point start, Point end)` |
| 566 | `public static double calculateDistance(double startLatitude, double startLongitude, double endLatitude, double endLongitude)` |

**Inner types:**

- `public static class Point implements Parcelable` (line 21) — public fields:
  - `public final double latitude` (line 24)
  - `public final double longitude` (line 26)
  - `public static final Parcelable.Creator<Point> CREATOR` (line 44)
- `public static interface Listener` (line 77) — method: `public void onPositionChanged()` (line 79)

**Public fields / constants on outer class:**

| Line | Declaration |
|------|-------------|
| 19 | `public static String TAG = "CI_GPS_" + LocationProvider.class.getSimpleName()` |

**Android component declarations:** None (not an Activity, Fragment, Service, BroadcastReceiver, or ContentProvider).

---

### File 2: GetDriverStatsResultArray.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.GetDriverStatsResultArray`

**Public methods (with line numbers):**

| Line | Signature |
|------|-----------|
| 16 | `public GetDriverStatsResultArray()` (default constructor) |
| 19 | `public GetDriverStatsResultArray(JSONArray jsonArray) throws JSONException` (constructor) |

**Public fields:**

| Line | Declaration |
|------|-------------|
| 14 | `public ArrayList<DriverStatsItem> arrayList` |

**Android component declarations:** None.

---

### File 3: GsonRequest.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.GsonRequest<T>`

**Public methods (with line numbers):**

| Line | Signature |
|------|-----------|
| 19 | `GsonRequest(UrlItem urlItem, Class<T> clazz, boolean authMessage, String requestBody, WebListener<T> listener)` (package-private constructor) |
| 24 | `GsonRequest(UrlItem urlItem, WebServiceParameterPacket param, Class<T> clazz, WebListener<T> listener)` (package-private constructor) |
| 29 | `public Map<String, String> getHeaders() throws AuthFailureError` (override) |
| 52 | `protected Response<T> parseNetworkResponse(NetworkResponse networkResponse)` (override) |
| 72 | `protected void deliverResponse(T response)` (override) |
| 79 | `void deliverResult(int statusCode, String response)` (package-private) |
| 111 | `public GsonRequest<T> update()` |

**Android component declarations:** None.

---

## Findings by Checklist Section

### 1. Signing and Keystores

No issues found in the three assigned files — `LocationProvider.java`, `GetDriverStatsResultArray.java`, and `GsonRequest.java` contain no keystore paths, signing credentials, or hardcoded passwords.

---

### 2. Network Security

#### CRITICAL — SSL Certificate Validation Disabled for All Requests

**File:** `GsonRequest.java` dispatches all network requests through `HttpClient.addRequest()` (confirmed by tracing the call chain: `HttpClient.enqueueRequest()` → `HttpClient.sendRequest(GsonRequest)` → `HttpClient.addRequest()`).

Inside `HttpClient.addRequest()` at **line 122**:

```java
FakeX509TrustManager.allowAllSSL();
```

`FakeX509TrustManager` (in the same WebService package, read as supporting context) implements `X509TrustManager` with empty `checkClientTrusted()` and `checkServerTrusted()` bodies — meaning neither client nor server certificates are ever validated. `allowAllSSL()` additionally installs a `HostnameVerifier` that unconditionally returns `true` for every hostname, then sets this as the process-wide default via `HttpsURLConnection.setDefaultHostnameVerifier()` and `HttpsURLConnection.setDefaultSSLSocketFactory()`.

This means every `GsonRequest` dispatched through `HttpClient` runs with:
- No TLS certificate chain validation
- No hostname verification

An attacker on the same network (LAN, Wi-Fi, or cellular MITM) can present any certificate for any hostname and the app will accept it, allowing complete interception and modification of all traffic to forkliftiqws, including authentication tokens, operator credentials, GPS telemetry, and driver stats.

**Severity:** Critical
**Location:** The vulnerability is invoked on every call to `HttpClient.addRequest()`. The `GsonRequest` class is the concrete request type routed through that path. `FakeX509TrustManager.allowAllSSL()` is also called independently in `au.com.collectiveintelligence.fleetiq360.autoupdate.util.TokenAuthenticator` (line 39) and `au.com.collectiveintelligence.fleetiq360.autoupdate.util.OkHttpClientFactory` (lines 16–17), confirming the pattern is application-wide.

**Related checklist item:** "Check for `TrustAllCertificates` implementations, `hostnameVerifier` overrides that return `true`, or `SSLContext` initialized with a permissive `TrustManager` — these disable certificate validation entirely."

---

#### MEDIUM — Synchronous Request Path Uses Plain `HttpURLConnection`

**File:** `HttpClient.java`, `syncSendRequest()` method (called from `HttpClient.enqueueRequest()` when `isSynchronous == true`).

The synchronous code path opens connections as `HttpURLConnection` (not `HttpsURLConnection`) and does not explicitly install the SSL factory or hostname verifier before connecting. However, because `allowAllSSL()` has already been called on `addRequest()` in the same session and sets **process-wide defaults** on `HttpsURLConnection`, the global defaults would propagate. The use of `HttpURLConnection` (the plain supertype) still supports HTTPS via the system's socket factory, which will now be the fake one. The net effect is the same: no certificate validation on synchronous calls. Noted here separately because the code structure obscures the coupling.

**Severity:** Medium (contributing factor to the Critical above; recorded separately for completeness).

---

#### No issues found — GsonRequest itself does not contain hardcoded URLs, IP addresses, or endpoint strings. URL construction is delegated to `UrlItem`.

---

### 3. Data Storage

#### LOW — `GetDriverStatsResultArray.arrayList` is a Public Non-Encapsulated Field

**File:** `GetDriverStatsResultArray.java`, line 14:

```java
public ArrayList<DriverStatsItem> arrayList;
```

Driver statistics data (operator performance data) is exposed via a public, mutable, non-encapsulated field with no access control. Any code holding a reference to a `GetDriverStatsResultArray` instance can replace or clear the list without going through any setter. While this is primarily an architecture issue, it means there is no enforcement point for clearing sensitive driver stats data when it should be discarded (e.g., on operator logout or shift change), which is relevant to the checklist requirement that operator data be fully cleared before another operator logs in.

**Severity:** Low (data-clearance risk; would be elevated if confirmed that instances are retained beyond a single request lifecycle).

---

#### No issues found — `LocationProvider.java` and `GsonRequest.java` contain no `SharedPreferences` writes, file I/O, SQLite operations, external storage access, `MODE_WORLD_READABLE`, or `MODE_WORLD_WRITEABLE` usage.

---

### 4. Input and Intent Handling

#### LOW — `LocationProvider.TAG` is a Mutable Public Static Field

**File:** `LocationProvider.java`, line 19:

```java
public static String TAG = "CI_GPS_" + LocationProvider.class.getSimpleName();
```

The `TAG` field is `public static` but not `final`. Any class in the application (or a component loaded into the same process) can reassign `TAG` at runtime. For a logging tag this is a low-severity issue, but it represents an unnecessary mutable global state surface. Declared `final` would eliminate the exposure.

**Severity:** Low / Informational.

---

#### No issues found — `LocationProvider.java` contains no WebView usage, no exported component declarations, no implicit intents carrying sensitive data, and no deep-link handlers. `GsonRequest.java` and `GetDriverStatsResultArray.java` similarly contain no intent handling.

---

### 5. Authentication and Session

#### MEDIUM — `GsonRequest` Silently Swallows Parse Failures, May Succeed with Null Data

**File:** `GsonRequest.java`, `getResult()` method, lines 97–109:

```java
private T getResult(String string) throws IllegalAccessException, InstantiationException {
    try {
        return createResultWithJsonArray(new JSONArray(string));
    } catch (JSONException ignored) {
    }

    try {
        return createResultWithJson(new JSONObject(string));
    } catch (JSONException ignored) {
    }

    return createResultWithJson(null);
}
```

If both JSON parse attempts fail (i.e., the server returns an unexpected response body — including an error page, an authentication challenge, or a redirection body), the method falls through to `createResultWithJson(null)`, which instantiates an empty result object and returns it as a success. `deliverResponse()` then calls `onSucceed()` with this empty object. A 401 Unauthorized or 403 Forbidden response with a non-JSON body would be silently treated as a successful, empty result rather than an authentication failure, potentially allowing the app to proceed in an unauthenticated state without the user or the calling code being aware.

This is compounded by the fact that the `deliverResult()` path (used for synchronous calls) does check `statusCode != HttpsURLConnection.HTTP_OK` before calling `getResult()`, but the Volley async path in `parseNetworkResponse()` does not check the HTTP status code at all before parsing — it relies entirely on Volley's error routing, which may not trigger for all non-200 responses depending on server configuration.

**Severity:** Medium

**Related checklist item:** "Check for token expiry handling: does the app refresh or re-authenticate when a token expires, or does it fail silently?"

---

#### No issues found — `LocationProvider.java` and `GetDriverStatsResultArray.java` contain no credential storage, token handling, or session management logic.

---

### 6. Third-Party Libraries

#### INFORMATIONAL — Volley Used as HTTP Client

**File:** `GsonRequest.java` imports `com.android.volley.*`. Volley is the HTTP client used for all async requests routed through `GsonRequest`. Specific version and CVE status of Volley are not determinable from this file alone (requires inspection of `build.gradle`). Recorded here as an observation for the library-review checklist item.

No issues found in these files that are attributable to third-party library misuse beyond the SSL bypass already recorded under Section 2.

---

### 7. Google Play and Android Platform

#### LOW — Deprecated API Usage in `LocationProvider.java`

**File:** `LocationProvider.java`, lines 363–369:

```java
@Override
public void onStatusChanged(String provider, int status, Bundle extras) { }

@Override
public void onProviderEnabled(String provider) { }

@Override
public void onProviderDisabled(String provider) { }
```

`LocationListener.onStatusChanged()` was deprecated in API level 29 (Android 10). `onProviderEnabled()` and `onProviderDisabled()` were also deprecated in API 29. The anonymous `LocationListener` created in `createLocationListener()` (line 349) overrides all three deprecated methods. While these stubs are empty and harmless today, they indicate the `LocationListener` implementation has not been updated for the modern `LocationListener` API and may require attention when `targetSdkVersion` is raised.

Additionally, `Build.VERSION.SDK_INT >= 17` at line 298 guards a code path for API 17 (Jelly Bean MR1, 2012). Given that `minSdkVersion` is expected to be well above 17 for a current Play Store app, this branch is dead code.

**Severity:** Low / Informational.

---

#### INFORMATIONAL — `java.util.Random` Used for Location Blur Offset

**File:** `LocationProvider.java`, line 98:

```java
private static final Random mRandom = new Random();
```

Used at line 226 in `calculateRandomOffset()` to generate blur offsets applied to GPS coordinates. `java.util.Random` is a pseudo-random number generator seeded from the system clock and is not cryptographically secure. For privacy-preserving location blurring in an operator-tracking context, `SecureRandom` is the appropriate choice. With `Random`, the blur offset sequence is predictable if the seed is known, which could allow an attacker to de-blur recorded locations and recover precise operator positions.

**Severity:** Low (context-dependent; elevated if location blur is relied upon as a privacy guarantee).

---

## Summary Table

| # | Severity | File | Description |
|---|----------|------|-------------|
| 1 | **Critical** | `GsonRequest.java` (via `HttpClient`) | All TLS certificate and hostname validation disabled process-wide via `FakeX509TrustManager.allowAllSSL()` called on every request dispatch |
| 2 | Medium | `HttpClient.java` (supporting context) | Synchronous request path also affected by global SSL bypass |
| 3 | Medium | `GsonRequest.java` | Silent fallthrough to empty success object on unparseable server responses; may mask authentication failures |
| 4 | Low | `GetDriverStatsResultArray.java` | Driver stats exposed via public mutable field with no enforcement point for data clearing on shift change |
| 5 | Low | `LocationProvider.java` | `java.util.Random` used for privacy-purpose location blur; predictable sequence |
| 6 | Low | `LocationProvider.java` | `public static String TAG` is mutable (not `final`) |
| 7 | Low / Info | `LocationProvider.java` | Deprecated `LocationListener` methods (`onStatusChanged`, `onProviderEnabled`, `onProviderDisabled`) and dead code for API < 17 |
| 8 | Info | `GsonRequest.java` | Volley version and CVE status not determinable from source alone; requires `build.gradle` review |
