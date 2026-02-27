# Pass 1 Security Audit — Agent APP09
**App:** forkliftiqapp (Android/Java)
**Date:** 2026-02-27
**Agent:** APP09
**Files Reviewed:**
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebRequest.java`
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebResult.java`

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy:** The checklist specifies branch `main`. Actual branch is `master`. Audit proceeds on `master` as confirmed.

---

## Reading Evidence

### File 1: `WebRequest.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.WebRequest<T>`

Extends: `com.android.volley.Request<T>`

**Public constants and static fields:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `WEBREQUEST_TIMEOUT_MS` | `public static final int` | `30 * 1000` (30,000 ms) | 46 |

**Package-private / non-private fields (visible within package):**

| Name | Type | Line |
|------|------|-------|
| `mHttpClient` | `HttpClient` | 47 |
| `webClazz` | `final Class<T>` | 49 |
| `webHeaders` | `final Map<String, String>` | 50 |
| `msgId` | `String` | 51 |
| `mUrlItem` | `UrlItem` | 52 |
| `canceledByUser` | `boolean` | 53 |
| `mRequestBody` | `String` | 54 |
| `webListener` | `WebListener<T>` | 55 |
| `cTimer` | `CountDownTimer` | 56 |
| `isTimerRunning` | `boolean` | 57 |
| `PROTOCOL_CHARSET` | `static final String` (`"utf-8"`) | 60 |
| `PROTOCOL_CONTENT_TYPE` | `static final String` | 63 |
| `isAuthMessage` | `boolean` | 65 |

**Public methods (signature and line):**

| Method | Line |
|--------|------|
| `void cancel()` | 68 |
| `void setPriority(Priority priority)` | 75 |
| `Request.Priority getPriority()` | 79 |
| `void setHttpClient(HttpClient httpClient)` | 84 |
| `String getPostBodyContentType()` (deprecated) | 111 |
| `byte[] getPostBody()` (deprecated) | 119 |
| `String getBodyContentType()` | 124 |
| `byte[] getBody()` | 129 |
| `WebRequest(UrlItem, WebServiceParameterPacket, Class<T>, WebListener<T>)` | 143 |
| `String getMsgId()` | 192 |
| `void onSucceed(T response)` | 197 |
| `void onConnectFailed(VolleyError volleyError)` | 211 |
| `void onRequestFailed(WebResult webResult)` | 239 |
| `void deliverError(VolleyError error)` | 263 |
| `WebRequest<T> update()` | 274 |

**Second constructor (also public):**

| Method | Line |
|--------|------|
| `WebRequest(UrlItem, String requestBody, boolean authMessage, Class<T>, WebListener<T>)` | 176 |

**Protected methods:**

| Method | Line |
|--------|------|
| `Response<T> parseNetworkResponse(NetworkResponse networkResponse)` | 89 |
| `void deliverResponse(T response)` | 255 |

**Package-private methods:**

| Method | Line |
|--------|------|
| `String getMsgId(String url)` | 172 |
| `boolean ignoreResponse(T response)` | 246 |
| `void removeRequest()` | 227 |

---

### File 2: `WebResult.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.WebResult`

**Public fields:**

| Name | Type | Line |
|------|------|-------|
| `volleyError` | `public VolleyError` | 4 |

**Public methods (signature and line):**

| Method | Line |
|--------|------|
| `boolean isBadGateway()` | 14 |
| `int getStatusCode()` | 21 |

---

## Checklist Findings by Section

### 1. Signing and Keystores

No signing configuration, keystore files, Gradle signing blocks, `gradle.properties`, `local.properties`, or pipeline configuration are present in the two assigned files.

No issues found — Section 1 (not in scope for assigned files).

---

### 2. Network Security

**FINDING NET-1 — Medium: Request body logged or exposed via `mRequestBody` (plain String field, package-private)**

`WebRequest.java` line 54: `mRequestBody` is a package-private `String` field holding the serialised JSON request body. Any class in the same package can read the request body, which may include credentials (login payloads) or session parameters. There is no explicit clearing of this field after the request completes.

**FINDING NET-2 — Informational: Deprecated Volley POST methods retained**

`getPostBodyContentType()` (line 111) and `getPostBody()` (line 119) are overridden and explicitly marked `@deprecated` by the Volley library. They delegate to the correct replacements (`getBodyContentType()` / `getBody()`), so there is no functional defect, but their presence is dead code and should be removed.

**FINDING NET-3 — Informational: No SSL/TLS pinning or certificate validation in assigned files**

Neither `WebRequest.java` nor `WebResult.java` configures an `SSLContext`, `TrustManager`, or `HostnameVerifier`. SSL trust decisions are therefore delegated to Volley's default stack and the Android platform trust store. This is acceptable unless another file overrides trust at the `HttpStack` level. The `HttpClient` class (referenced at line 47) is not in scope for this pass and must be reviewed separately for `TrustAllCertificates` or permissive `HostnameVerifier` implementations.

**FINDING NET-4 — Informational: `WebResult.java` imports `javax.net.ssl.HttpsURLConnection` (line 5)**

The import is used only to reference the constant `HttpsURLConnection.HTTP_BAD_GATEWAY` (502). This is a benign usage — it reads a numeric constant from an HTTPS class rather than opening any connection. No issue, noted for completeness.

No issues found regarding cleartext traffic flags, hardcoded URLs, or permissive TrustManagers in the two assigned files.

---

### 3. Data Storage

**FINDING DS-1 — Low: `mRequestBody` not zeroed after use**

`WebRequest.java` line 54: `mRequestBody` holds the raw JSON string for the HTTP request body. If the request contains a login payload (username/password), the string remains in the object's memory for the lifetime of the `WebRequest` instance. There is no `onSucceed`/`onRequestFailed` cleanup that nulls this field. Combined with the field being package-private (readable without a getter), this increases the window during which credential data sits in heap memory.

No issues found regarding SharedPreferences, external storage, SQLite, ADB backup flag, or `MODE_WORLD_READABLE` in the two assigned files.

---

### 4. Input and Intent Handling

No Activity, Service, BroadcastReceiver, ContentProvider, WebView, or intent-filter declarations exist in either assigned file. Both files are pure network-layer helper classes.

No issues found — Section 4 (not in scope for assigned files).

---

### 5. Authentication and Session

**FINDING AUTH-1 — Medium: 401 Unauthorized triggers automatic retry without caller notification**

`WebRequest.java` lines 217–224: When a non-auth request receives an HTTP 401 response, `onConnectFailed()` calls `mHttpClient.retryOnAuthFail(this)` instead of surfacing the error to `webListener`. The calling code (via `WebListener.onFailed`) is never notified of the 401. If `retryOnAuthFail` itself silently fails, the user receives no feedback that their session has expired and re-authentication is required. This can mask session expiry events and delay operator lock-out when credentials are revoked.

**FINDING AUTH-2 — Informational: `isAuthMessage` flag controls header injection path**

`WebRequest.java` lines 150 and 184: `WebData.instance().setHttpHeader(isAuthMessage, webHeaders)` selects a different header set for authentication messages versus normal API calls. The exact headers set are in `WebData` (not in scope this pass) and must be reviewed to confirm that bearer tokens or session identifiers are not included in unauthenticated requests.

**FINDING AUTH-3 — Informational: `update()` method recreates request with same credentials**

`WebRequest.java` lines 274–283: The `update()` method constructs a new `WebRequest` using the stored `mRequestBody`, `isAuthMessage`, `webClazz`, and `webListener`. If `mRequestBody` contains credentials (e.g., login body), calling `update()` re-sends those credentials without any refresh or re-validation. This is likely intentional for token-refresh flows but should be confirmed that `update()` is never called with stale or revoked credentials.

No issues found regarding token storage or logout clearing in the two assigned files (those concerns are in storage and higher-level session management classes not assigned here).

---

### 6. Third-Party Libraries

The assigned files use **Volley** (`com.android.volley`) for HTTP request handling.

**FINDING LIB-1 — Informational: Volley version not determinable from assigned files**

The Volley dependency version is declared in `build.gradle` (not in scope for this pass). Volley has had no critical CVEs in its stable release history, but the version should be confirmed as current when `build.gradle` is reviewed. The deprecated `getPostBody()` / `getPostBodyContentType()` overrides (lines 119, 111) suggest the Volley version in use may be older than the current release.

No issues found in the two assigned files regarding `GsonHelper`, `WebServiceParameterPacket`, or other referenced classes beyond what is noted.

---

### 7. Google Play and Android Platform

**FINDING PLAT-1 — Low: Deprecated Volley POST API methods overridden**

`WebRequest.java` lines 107–122: The methods `getPostBodyContentType()` and `getPostBody()` are annotated `@deprecated` by the Volley framework (the `@deprecated` tags in the Javadoc at lines 108 and 116 are Volley's own deprecation notices). These overrides are harmless at runtime but constitute unnecessary dead code that should be removed. Their presence indicates this code was written against an older Volley API.

**FINDING PLAT-2 — Informational: `CountDownTimer` used for request timeout (lines 56, 158–167)**

`WebRequest.java`: A `CountDownTimer` with a 30-second total duration is started in the first constructor (lines 158–167). On `onFinish()`, it calls `onRequestFailed((VolleyError) null)` (line 165). This passes `null` to `onRequestFailed(VolleyError)` (line 233), which constructs a `WebResult` with `volleyError = null`. Any downstream code that calls `webResult.getStatusCode()` or `webResult.isBadGateway()` without null-checking `volleyError.networkResponse` is safe because `WebResult.getStatusCode()` guards for `null` (line 22–26), but callers expecting a non-null `VolleyError` for error typing could be misled into treating a timeout as an unknown error with status code 0. Using a `null` `VolleyError` to represent a timeout is semantically ambiguous. Additionally, the `CountDownTimer` is only started in the first constructor (line 158) but not in the second constructor (line 176), meaning requests created via the second constructor have no timeout mechanism at the `WebRequest` layer.

No issues found regarding `targetSdkVersion`, permissions, or runtime permission handling in the two assigned files.

---

## Summary Table

| ID | Severity | Section | File | Description |
|----|----------|---------|------|-------------|
| NET-1 | Medium | 2. Network Security | `WebRequest.java` | `mRequestBody` is package-private; may contain credentials; not cleared after use |
| NET-2 | Informational | 2. Network Security | `WebRequest.java` | Deprecated Volley POST methods retained as dead code |
| NET-3 | Informational | 2. Network Security | `WebRequest.java` | SSL/TLS trust configuration not present — defer to `HttpClient` review |
| NET-4 | Informational | 2. Network Security | `WebResult.java` | `HttpsURLConnection` imported for constant only — benign |
| DS-1 | Low | 3. Data Storage | `WebRequest.java` | `mRequestBody` not nulled after request completes |
| AUTH-1 | Medium | 5. Authentication and Session | `WebRequest.java` | 401 triggers silent retry; `WebListener` not notified of session expiry |
| AUTH-2 | Informational | 5. Authentication and Session | `WebRequest.java` | `isAuthMessage` header path requires `WebData` review |
| AUTH-3 | Informational | 5. Authentication and Session | `WebRequest.java` | `update()` resends stored request body without credential refresh check |
| LIB-1 | Informational | 6. Third-Party Libraries | `WebRequest.java` | Volley version unconfirmed — verify in `build.gradle` |
| PLAT-1 | Low | 7. Google Play and Platform | `WebRequest.java` | Deprecated Volley API overrides indicate outdated API usage |
| PLAT-2 | Informational | 7. Google Play and Platform | `WebRequest.java` | `null` VolleyError passed on timeout; second constructor has no timeout |

---

## Files Requiring Follow-Up (Out of Scope This Pass)

- `HttpClient.java` — must be reviewed for `TrustAllCertificates`, permissive `HostnameVerifier`, and the implementation of `retryOnAuthFail()` (AUTH-1 depends on this)
- `WebData.java` — must be reviewed for what headers are set per `isAuthMessage` flag (AUTH-2 depends on this)
- `app/build.gradle` — Volley version, `targetSdkVersion`, signing config (LIB-1 depends on this)
