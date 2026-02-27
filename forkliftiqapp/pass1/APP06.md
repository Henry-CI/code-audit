# Pass 1 Security Audit — Agent APP06
**Date:** 2026-02-27
**Repo:** forkliftiqapp (Android/Java)
**Auditor:** APP06

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy:** The checklist specifies `Branch: main`. The actual default branch is `master`. Audit proceeds on `master`.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/HttpClient.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/ImagePostBackgroundTask.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/ImagePostRequest.java`

A fourth file, `FakeX509TrustManager.java`, is directly called from `HttpClient.java` at line 122 and was read in full because it is essential to evaluate the SSL/TLS security posture of this component.

---

## Reading Evidence

### File 1 — `HttpClient.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.HttpClient`

**Public fields and constants:**

| Name | Type | Value | Line |
|---|---|---|---|
| `isSynchronous` | `boolean` (instance) | `false` | 40 |
| `DEFAULT_TIMEOUT_MS` | `public static final int` | `30000` | 42 |
| `LOGIN_TIMEOUT_MS` | `public static final int` | `60000` | 43 |
| `TAG` | `public static final String` | `"Volley"` | 62 |

**Public methods:**

| Signature | Line |
|---|---|
| `HttpClient(Context context)` | 65 |
| `static void initRequestQueue(Context pContext)` | 72 |
| `RequestQueue getRequestQueue()` | 79 |
| `static void setCommonData(JSONObject jsonObject)` | 92 |
| `static JSONObject jsonFromWebParam(Object object)` | 104 |
| `void removeRequest(WebRequest request)` | 149 |
| `void enqueueRequest(GsonRequest webRequest)` | 154 |
| `void syncSendRequest(final GsonRequest gsonRequest)` | 162 |

**Package-private methods:**

| Signature | Line |
|---|---|
| `void retryOnAuthFail(final WebRequest msg)` | 248 |

**Key internal call of note:** `addRequest(WebRequest)` at line 120 calls `FakeX509TrustManager.allowAllSSL()` at line 122 before every Volley request is enqueued.

---

### File 2 — `ImagePostBackgroundTask.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.ImagePostBackgroundTask`

**Class hierarchy:** Extends `AsyncTask<ImageUploadParam, String, ImageUploadResult>`

**Inner/static classes:**

| Class | Type | Line |
|---|---|---|
| `ImageUploadParam` | `public static class` | 21 |
| `ImageUploadResult` | `public static class` | 30 |
| `ImageUploadCallBack` | `public static class` | 35 |

**Public fields on `ImageUploadParam`:**

| Name | Type | Line |
|---|---|---|
| `url` | `String` | 22 |
| `imagePath` | `String` | 23 |
| `multiPathArray` | `ArrayList<String>` | 24 |
| `fileNames` | `ArrayList<String>` | 25 |
| `bitmap` | `Bitmap` | 26 |
| `callback` | `ImageUploadCallBack` | 27 |

**Public fields on `ImageUploadResult`:**

| Name | Type | Line |
|---|---|---|
| `imageParam` | `ImageUploadParam` | 32 |
| `succeed` | `boolean` | 33 |

**Public methods:**

| Signature | Line |
|---|---|
| `static void uploadImage(String url, ArrayList<String> pathArray, ArrayList<String> fileNames, ImageUploadCallBack callback)` | 77 |
| `static void uploadImage(String url, String path, ImageUploadCallBack callback)` | 97 |
| `static void uploadImage(String url, Bitmap bitmap, ImageUploadCallBack callback)` | 114 |
| `void onUploadResult(ImageUploadResult result)` (on `ImageUploadCallBack`) | 36 |

**Overridden AsyncTask methods:**

| Signature | Line |
|---|---|
| `protected ImageUploadResult doInBackground(ImageUploadParam... params)` | 42 |
| `protected void onPostExecute(ImageUploadResult result)` | 65 |

---

### File 3 — `ImagePostRequest.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.ImagePostRequest`

**Public methods:**

| Signature | Line |
|---|---|
| `static boolean SendHttpImage(String urlServer, String pathToOurFile)` | 24 |
| `static boolean SendHttpImage(String urlServer, byte[] imageByte)` | 32 |
| `static boolean SendHttpImage(String urlServer, Bitmap bitmap)` | 100 |
| `static boolean SendMultipartHttpImage(String urlServer, ArrayList<String> filePaths, ArrayList<String> fileNames)` | 117 |

**Package-private methods:**

| Signature | Line |
|---|---|
| `static boolean isMultiPart(String urlServer)` | 107 |

**Notable implementation details:**
- All three `SendHttpImage` overloads and `SendMultipartHttpImage` open `HttpURLConnection` directly via `new URL(urlServer).openConnection()`. No TrustManager or HostnameVerifier is applied in this class.
- `isMultiPart` at line 107 performs substring matching on the URL string to select the multipart content type. The matched substrings are `"driveraccess"`, `"appuser/photo"`, and `"impactimage"`.
- `SendMultipartHttpImage` silently swallows exceptions at line 169–172 with an empty catch block.

---

### Supporting file read — `FakeX509TrustManager.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.FakeX509TrustManager`

**Public methods:**

| Signature | Line |
|---|---|
| `void checkClientTrusted(X509Certificate[], String)` | 26 |
| `void checkServerTrusted(X509Certificate[], String)` | 31 |
| `boolean isClientTrusted(X509Certificate[])` | 35 |
| `boolean isServerTrusted(X509Certificate[])` | 39 |
| `X509Certificate[] getAcceptedIssuers()` | 43 |
| `static SSLContext getUnsafeSSLContext()` | 48 |
| `static void allowAllSSL()` | 67 |

---

## Findings by Checklist Section

---

### Section 1 — Signing and Keystores

No signing configuration, keystore files, Gradle signing blocks, or pipeline YAML were within scope for these three files.

No issues found — Section 1 (out of scope for assigned files).

---

### Section 2 — Network Security

#### CRITICAL — SSL/TLS certificate validation completely disabled globally

**File:** `HttpClient.java` line 122, via `FakeX509TrustManager.java`

Every time a Volley `WebRequest` is dispatched through `addRequest()`, the app calls `FakeX509TrustManager.allowAllSSL()`. That method does two things:

1. **Hostname verification bypassed** (`FakeX509TrustManager.java` lines 67–75): Sets the default `HostnameVerifier` for all `HttpsURLConnection` instances on the JVM to an anonymous implementation that unconditionally returns `true` for every hostname, regardless of whether the server certificate matches the host being contacted.

2. **Certificate chain validation bypassed** (`FakeX509TrustManager.java` lines 48–65, 51–53): Installs a `TrustManager` array containing a single `FakeX509TrustManager` instance as the default SSL socket factory. Both `checkClientTrusted` (line 26) and `checkServerTrusted` (line 31) have empty bodies — they throw no `CertificateException` and perform no validation whatsoever. Any certificate, self-signed, expired, or belonging to an entirely different domain, is silently accepted.

Because `HttpsURLConnection.setDefaultHostnameVerifier` and `HttpsURLConnection.setDefaultSSLSocketFactory` set **process-wide** defaults, this affects every HTTPS connection opened anywhere in the application after the first Volley request is dispatched, including the `HttpURLConnection` calls in `ImagePostRequest.java` and `syncSendRequest()` in `HttpClient.java`.

The class name `FakeX509TrustManager` and the method name `allowAllSSL` make the intent explicit. The comment in the original `checkServerTrusted` body ("To change body of implemented methods use File | Settings | File Templates.") indicates this was generated as a stub and the validation logic was never implemented.

**Impact:** An attacker on any network path (Wi-Fi, mobile carrier, corporate proxy) can intercept and modify all HTTPS traffic between the application and the forkliftiqws backend. Operator credentials, authentication tokens, telemetry data, and forklift assignment data are all transmitted without effective transport-layer protection despite the use of the `https://` scheme.

**Severity: Critical**

---

#### HIGH — `HttpURLConnection` used for image upload with no SSL override applied in `ImagePostRequest`

**File:** `ImagePostRequest.java` lines 44–46, 126–128

Both `SendHttpImage(String, byte[])` and `SendMultipartHttpImage` call `new URL(urlServer).openConnection()` and cast the result to `HttpURLConnection`. The URL scheme is whatever the caller passes at runtime. There is no enforcement that the scheme is `https://`, and no SSL socket factory or hostname verifier is set on the individual connection object.

In practice, the process-wide override from `FakeX509TrustManager.allowAllSSL()` (applied via `HttpClient.addRequest`) will affect these connections once it has been called, but:

- If an image upload is the first network operation (before any Volley request has been dispatched), the unsafe SSL context has not yet been applied and the connection will use default validation — this is inconsistent behaviour depending on call order.
- If the URL passed by the caller uses `http://` rather than `https://`, no encryption is applied at all and the response code check at lines 93–97 and 173–178 simply returns `false` on non-200, with no error surfaced to the caller.
- There is no scheme validation anywhere in the image upload path.

**Severity: High**

---

#### MEDIUM — Silent exception swallowing in `SendMultipartHttpImage`

**File:** `ImagePostRequest.java` lines 169–172

The catch block for the multipart upload is empty. Any `IOException`, `MalformedURLException`, or SSL handshake exception is silently discarded. The method returns `false` (non-200 response code), which the caller in `ImagePostBackgroundTask.doInBackground` (line 54) treats as a failed upload. No error is logged, no exception is propagated, and there is no way to distinguish a network error from a deliberate server rejection. This also suppresses any SSL-related errors, making security issues invisible at runtime.

**Severity: Medium**

---

#### MEDIUM — `syncSendRequest` uses `HttpURLConnection` with no scheme enforcement

**File:** `HttpClient.java` lines 162–219

The synchronous request path casts `url.openConnection()` to `HttpURLConnection` (line 171). This path is used when `isSynchronous == true` (line 155). The URL is taken directly from `gsonRequest.mUrlItem.url` with no scheme validation. If a `http://` URL is passed, the connection is unencrypted. The process-wide SSL override from `FakeX509TrustManager.allowAllSSL()` does not affect `HttpURLConnection` opened over plain HTTP — it only matters for HTTPS connections.

**Severity: Medium**

---

#### INFO — `setCommonData` is a no-op

**File:** `HttpClient.java` lines 92–102

The `setCommonData` method has an empty `if (jsonObject != null)` block. Any common data fields (e.g., device ID, session correlation) that were intended to be injected into every outgoing request are not being set. This is a functional dead code finding with potential audit-trail implications.

**Severity: Informational**

---

### Section 3 — Data Storage

No SharedPreferences, file writes, SQLite operations, or backup configuration are present in these three files.

No issues found — Section 3 (out of scope for assigned files).

---

### Section 4 — Input and Intent Handling

No Activities, Services, BroadcastReceivers, or WebView usage are present in these three files. No Intent construction or deep link handling is present.

No issues found — Section 4 (out of scope for assigned files).

---

### Section 5 — Authentication and Session

#### LOW — Authorization header injected from `WebData.instance()` with no visibility into storage

**File:** `HttpClient.java` line 178, `ImagePostRequest.java` line 54

Both files call `WebData.instance().getAuthHeader()` (HttpClient) and `WebData.instance().setHttpHeaderForConnection(connection)` (ImagePostRequest) to inject authentication credentials into requests. The `WebData` singleton is outside the scope of these files; however, the pattern of a globally accessible singleton holding authentication state is noted. How and where `WebData` stores the token cannot be assessed from these files alone.

**Severity: Low / Refer to WebData.java review**

---

#### LOW — `retryOnAuthFail` triggers re-authentication silently

**File:** `HttpClient.java` lines 248–262

On authentication failure, the app silently re-authenticates via `WebApi.async().authApp(...)` and requeues the original request. There is no limit on how many times this retry can occur, and no user notification that credentials were rejected and re-sent. This behaviour is noted; the security impact depends on the credential storage and re-authentication mechanism.

**Severity: Low / Refer to WebApi.java review**

---

### Section 6 — Third-Party Libraries

**File:** `HttpClient.java` imports

- `com.android.volley` — Google Volley is used as the HTTP request queue. The specific version is not visible in these source files; it must be assessed in `build.gradle`.

No issues can be conclusively raised from source imports alone without version information from Gradle.

No issues found — Section 6 (version assessment deferred to build.gradle review).

---

### Section 7 — Google Play and Android Platform

#### MEDIUM — `AsyncTask` is deprecated

**File:** `ImagePostBackgroundTask.java` line 5 and 15

`ImagePostBackgroundTask` extends `android.os.AsyncTask`. `AsyncTask` was deprecated in API level 30 (Android 11). The checklist notes this as a deprecated API finding. Use of deprecated `AsyncTask` for network I/O also carries a subtle risk: if the `Activity` that triggered the upload is destroyed before `onPostExecute` runs, the callback reference in `ImageUploadCallBack` may reference a destroyed context, potentially causing a memory leak or a crash.

**Severity: Medium**

---

## Summary Table

| ID | Severity | File | Finding |
|---|---|---|---|
| APP06-01 | Critical | `HttpClient.java` / `FakeX509TrustManager.java` | Process-wide SSL certificate validation and hostname verification disabled for all HTTPS connections |
| APP06-02 | High | `ImagePostRequest.java` | No scheme enforcement on image upload URLs; SSL bypass is order-dependent; plain HTTP uploads possible |
| APP06-03 | Medium | `ImagePostRequest.java` | Empty catch block in `SendMultipartHttpImage` silently suppresses all errors including SSL failures |
| APP06-04 | Medium | `HttpClient.java` | `syncSendRequest` uses `HttpURLConnection` with no scheme enforcement |
| APP06-05 | Medium | `ImagePostBackgroundTask.java` | Use of deprecated `AsyncTask` (deprecated API 30); potential memory leak if Activity destroyed mid-upload |
| APP06-06 | Low | `HttpClient.java` / `ImagePostRequest.java` | Authentication credentials held in `WebData` singleton; storage mechanism not assessable from these files |
| APP06-07 | Low | `HttpClient.java` | `retryOnAuthFail` performs unlimited silent re-authentication with no user notification |
| APP06-08 | Info | `HttpClient.java` | `setCommonData` is a no-op; intended request decoration is never applied |

---

## Notes for Subsequent Passes

- `FakeX509TrustManager.java` was not in the assigned file list but is directly invoked by `HttpClient.java` at line 122. It was read to support accurate findings for APP06-01. The class should be assigned to an agent for its own entry in the reading evidence log if it has not been already.
- `WebData.java` must be reviewed to assess how authentication tokens are stored (Section 5).
- `WebApi.java` must be reviewed to assess re-authentication behaviour and credential source.
- The `build.gradle` (app module) must be reviewed for the Volley version and ProGuard configuration (Sections 6 and 7).
