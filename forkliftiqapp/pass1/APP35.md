# Pass 1 Security Audit — APP35
**Agent ID:** APP35
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Branch confirmed as `master`. Proceeding.

**Discrepancy recorded:** The checklist header states `Branch: main`, but the actual repository default branch is `master`.

---

## Step 2 — Checklist Read

Full checklist read from `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`. Sections covered: Signing and Keystores, Network Security, Data Storage, Input and Intent Handling, Authentication and Session, Third-Party Libraries, Google Play and Android Platform.

---

## Step 3 — Files Read

All three assigned files read in full, plus two referenced classes read for complete evidence:

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/service/APKUpdateServiceFactory.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/util/OkHttpClientFactory.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/util/TokenAuthenticator.java`

Supporting classes read (referenced directly from assigned files):
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/FakeX509TrustManager.java`
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebData.java`

---

## Step 4 — Reading Evidence

### File 1: APKUpdateServiceFactory.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.autoupdate.service.APKUpdateServiceFactory`

**Public methods:**

| Line | Signature |
|------|-----------|
| 10 | `public static APKUpdateService getService()` |

**Fields/Constants:** None declared in this class.

**Summary:** Factory class. `getService()` builds a Retrofit instance using `BuildConfig.BASE_URL` as the base URL, `OkHttpClientFactory.getOkHttpClient()` as the HTTP client, and Gson for JSON conversion. Returns a `APKUpdateService` Retrofit interface proxy.

---

### File 2: OkHttpClientFactory.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.autoupdate.util.OkHttpClientFactory`

**Public methods:**

| Line | Signature |
|------|-----------|
| 13 | `public static OkHttpClient getOkHttpClient()` |

**Fields/Constants:** None declared in this class.

**Summary of construction in `getOkHttpClient()` (lines 13-34):**

- Line 16: Calls `FakeX509TrustManager.getUnsafeSSLContext()` — obtains an `SSLContext` initialized with a no-op `TrustManager` that accepts all certificates without validation.
- Line 17: Installs the unsafe SSL socket factory and `FakeX509TrustManager` as the trust manager on the OkHttp builder.
- Lines 18-24: Installs an anonymous `HostnameVerifier` that unconditionally returns `true` for every hostname. The Android lint suppression `@SuppressLint("BadHostnameVerifier")` is present, indicating the developer was aware this is dangerous.
- Line 29: Attaches a `TokenAuthenticator` for 401 challenge handling.
- `Dispatcher` is configured with `maxRequests(1)` — limits concurrency to one in-flight request.

**SSL/TLS validation is completely disabled on this client.**

---

### File 3: TokenAuthenticator.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.autoupdate.util.TokenAuthenticator`

**Access modifier:** Package-private (`class TokenAuthenticator`, no `public`).

**Implemented interface:** `okhttp3.Authenticator`

**Methods:**

| Line | Signature |
|------|-----------|
| 27 | `public Request authenticate(@Nullable Route route, @NonNull Response response) throws IOException` |
| 36 | `private GetTokenResult getAccessToken() throws IOException` |

**Fields/Constants:** None declared in this class.

**Summary of `authenticate()` (lines 27-34):**

- Calls `getAccessToken()` to obtain a fresh token.
- If null is returned (token fetch failed or non-200), returns null — OkHttp will propagate the 401 failure to the caller.
- Otherwise, rebuilds the original request with an `Authorization` header using `tokenType + " " + value` from the token result.

**Summary of `getAccessToken()` (lines 36-61):**

- Constructs the token endpoint URL as `BuildConfig.BASE_URL + "/oauth/token"` (line 37).
- Line 39: Calls `FakeX509TrustManager.allowAllSSL()` — this sets the JVM-wide default `HostnameVerifier` and `SSLSocketFactory` on `HttpsURLConnection` to accept all certificates and all hostnames for the entire process, not just this connection.
- POSTs to the token endpoint with `Content-Type: application/x-www-form-urlencoded`.
- Line 49: Calls `WebData.instance().getTokenFormData()` to obtain the POST body. **See critical finding below regarding hardcoded credentials found in WebData.**
- Returns a `GetTokenResult` deserialized from the JSON response. No expiry, no retry logic, no loop-detection — on 401, OkHttp will call `authenticate()` once per response. If the token endpoint itself returns 401, `getAccessToken()` returns null and the request fails, which is acceptable.

---

### Supporting class evidence (not assigned, read for context)

**FakeX509TrustManager** (`au.com.collectiveintelligence.fleetiq360.WebService.FakeX509TrustManager`):

- Implements `X509TrustManager`. Both `checkClientTrusted` and `checkServerTrusted` have empty bodies — they throw no exception and perform no validation. Every certificate is silently accepted.
- `getUnsafeSSLContext()` (line 48): Returns a `TrustManager[]` containing only this no-op manager, initializes `SSLContext("TLS")` with it.
- `allowAllSSL()` (line 67): Calls `HttpsURLConnection.setDefaultHostnameVerifier(...)` with a verifier returning `true` and `HttpsURLConnection.setDefaultSSLSocketFactory(...)` with the unsafe context. **This modifies process-wide static state.**

**WebData** (`au.com.collectiveintelligence.fleetiq360.WebService.WebData`) — `getTokenFormData()` method (lines 56-82):

Constructs an OAuth `password` grant body with the following hardcoded literal values:

| Parameter | Hardcoded Value |
|-----------|----------------|
| `grant_type` | `password` |
| `client_id` | `987654321` |
| `client_secret` | `8752361E593A573E86CA558FFD39E` |
| `username` | `gas` |
| `password` | `ciiadmin` |

These are embedded as string literals in the source file with no reference to build config, secrets management, or environment variables.

---

## Step 5 — Findings by Checklist Section

---

### Section 1 — Signing and Keystores

No signing configuration, keystore files, or Gradle signing blocks are present in the three assigned files. This section cannot be assessed from these files alone.

No issues found — Section 1 (from assigned files).

---

### Section 2 — Network Security

**CRITICAL — TLS Certificate Validation Disabled (CWE-295)**

**File:** `OkHttpClientFactory.java`, lines 16-17
**Also:** `FakeX509TrustManager.java`, lines 26-33

`FakeX509TrustManager` implements `X509TrustManager` with empty `checkClientTrusted` and `checkServerTrusted` methods. Both methods accept every certificate without any validation. This instance is supplied to `OkHttpClient.Builder.sslSocketFactory()` (line 17 of `OkHttpClientFactory.java`). Every HTTPS request made by this OkHttp client is vulnerable to interception by any attacker who can present any TLS certificate — including self-signed certificates issued by an attacker. This is an effective MITM sink for all API traffic routed through the autoupdate module.

The class name `FakeX509TrustManager` and the method name `getUnsafeSSLContext()` confirm developer awareness. This is not an accidental misconfiguration.

---

**CRITICAL — Hostname Verification Disabled (CWE-297)**

**File:** `OkHttpClientFactory.java`, lines 18-24

An anonymous `HostnameVerifier` is installed on the OkHttp builder. Its `verify()` method returns `true` unconditionally for every hostname. Combined with the disabled certificate trust validation above, no aspect of TLS is operative on this client. A connection to any host presenting any certificate will succeed and be treated as legitimate.

The `@SuppressLint("BadHostnameVerifier")` annotation (line 19) demonstrates the developer suppressed the Android lint warning explicitly rather than fixing the issue.

---

**CRITICAL — Process-Wide TLS Bypass via Static Setter (CWE-295, CWE-297)**

**File:** `TokenAuthenticator.java`, line 39
**Implemented in:** `FakeX509TrustManager.java`, lines 67-78

`FakeX509TrustManager.allowAllSSL()` is called unconditionally each time `getAccessToken()` is invoked (i.e., on every 401 response). This method calls:

- `HttpsURLConnection.setDefaultHostnameVerifier(...)` — overrides the JVM-wide default hostname verifier for all `HttpsURLConnection` instances in the process.
- `HttpsURLConnection.setDefaultSSLSocketFactory(...)` — overrides the JVM-wide default SSL socket factory for all `HttpsURLConnection` instances in the process.

These are static setters that affect every `HttpsURLConnection` opened anywhere in the application after this point, including connections opened by third-party libraries. The scope of the TLS bypass extends beyond the token endpoint to the entire application process.

---

**No issues found** — hardcoded base URL: `APKUpdateServiceFactory.java` correctly reads the base URL from `BuildConfig.BASE_URL` (line 14) rather than a string literal. However, the value of `BuildConfig.BASE_URL` in the generated build config must be verified separately to confirm it is not a development or staging endpoint.

---

### Section 3 — Data Storage

**CRITICAL — Hardcoded OAuth Client Secret in Source Code (CWE-798)**

**File:** `WebData.java` (supporting class), lines 63-68, called from `TokenAuthenticator.java` line 49

`WebData.getTokenFormData()` constructs an OAuth `password` grant body with five hardcoded string literals:

- `client_id`: `987654321`
- `client_secret`: `8752361E593A573E86CA558FFD39E`
- `username`: `gas`
- `password`: `ciiadmin`

These credentials are embedded in source code that is committed to version control. Any person with access to the repository has permanent access to these credentials. The OAuth `password` grant type combined with static credentials means that any party with network access to the token endpoint and knowledge of these values can obtain tokens independently of the application.

The credentials appear to be a service account (`gas` / `ciiadmin`) used by the app to obtain tokens on behalf of the device. Because they are hardcoded in Java source, they are also extractable from a compiled APK through decompilation with tools such as jadx or apktool.

**Severity: Critical** — hardcoded credentials for a live authentication endpoint in version-controlled source.

---

**No issues found** — data storage patterns for this section are not directly observable from the three assigned files. Token persistence is handled by `ModelPrefs` (via `WebData.setGetTokenResult()`), which is out of scope for this agent.

---

### Section 4 — Input and Intent Handling

No Activities, Services, BroadcastReceivers, ContentProviders, WebViews, deep link handlers, or Intent construction are present in the three assigned files.

No issues found — Section 4 (from assigned files).

---

### Section 5 — Authentication and Session

**HIGH — Token Refresh Uses Hardcoded Credentials (CWE-798, related to Section 3 finding)**

**File:** `TokenAuthenticator.java`, line 49

The `authenticate()` callback — called by OkHttp whenever the server returns a 401 — obtains a new token by calling `getAccessToken()`, which sends the hardcoded OAuth `password` grant. There is no user-specific credential involved in this token refresh path; the token is obtained using the static service-account credentials in `WebData.getTokenFormData()`. This means:

1. Token refresh is not bound to the authenticated user's session.
2. Compromise of the hardcoded credentials allows token issuance independent of the app.

**LOW — No Retry Loop Protection Confirmed at Class Level**

OkHttp's `Authenticator` contract limits retries per request internally. The `authenticate()` implementation returns `null` on non-200 from the token endpoint, which correctly stops OkHttp from retrying indefinitely. However, there is no count-based guard within the authenticator itself. If the token endpoint is unavailable or consistently returning errors other than 200, the behavior depends entirely on OkHttp's built-in retry limits.

No issues found — token expiry handling: OkHttp automatically calls `authenticate()` on 401, which is the correct mechanism for reactive token refresh. The app does respond to expired tokens rather than failing silently.

---

### Section 6 — Third-Party Libraries

Libraries used within the assigned files:
- OkHttp (version not determinable from these files alone — in `build.gradle`)
- Retrofit 2 with `GsonConverterFactory`
- Gson (used in `TokenAuthenticator.java` line 59)

Version numbers and CVE status require review of `build.gradle`, which is outside this agent's assigned scope.

No issues found — Section 6 (from assigned files; version audit deferred to build file agents).

---

### Section 7 — Google Play and Android Platform

No manifest declarations, `targetSdkVersion`, `minSdkVersion`, permissions, or deprecated API usage (`AsyncTask`, `startActivityForResult`) are present in the three assigned files.

No issues found — Section 7 (from assigned files).

---

## Summary of Findings

| ID | Severity | Section | File | Description |
|----|----------|---------|------|-------------|
| APP35-01 | Critical | 2 — Network Security | `OkHttpClientFactory.java` L16-17, `FakeX509TrustManager.java` L26-33 | TLS certificate validation completely disabled. `FakeX509TrustManager` accepts every certificate. All API traffic is vulnerable to MITM interception. |
| APP35-02 | Critical | 2 — Network Security | `OkHttpClientFactory.java` L18-24 | Hostname verification unconditionally returns `true`. No TLS hostname check is performed for any connection. |
| APP35-03 | Critical | 2 — Network Security | `TokenAuthenticator.java` L39, `FakeX509TrustManager.java` L67-78 | `allowAllSSL()` modifies process-wide static `HttpsURLConnection` defaults on every token refresh. TLS bypass extends to all `HttpsURLConnection` calls in the entire process. |
| APP35-04 | Critical | 3 — Data Storage / 5 — Authentication | `WebData.java` L63-68 (called from `TokenAuthenticator.java` L49) | Hardcoded OAuth credentials in source: `client_id=987654321`, `client_secret=8752361E593A573E86CA558FFD39E`, `username=gas`, `password=ciiadmin`. Committed to version control; extractable from compiled APK. |
| APP35-05 | Low | 5 — Authentication | `TokenAuthenticator.java` L27-34 | No explicit retry counter in authenticator. Relies solely on OkHttp's internal limit. |

**Branch discrepancy:** Checklist states `Branch: main`; actual branch is `master`.
