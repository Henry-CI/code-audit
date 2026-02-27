# Pass 4 Code Quality Audit — Agent A44
**Audit run:** 2026-02-26-01
**Auditor:** A44
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/service/APKUpdateServiceFactory.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/util/OkHttpClientFactory.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/util/TokenAuthenticator.java`

---

## Step 1: Reading Evidence

### File 1 — APKUpdateServiceFactory.java

**Package:** `au.com.collectiveintelligence.fleetiq360.autoupdate.service`

**Class:** `APKUpdateServiceFactory` (public, no explicit superclass)

**Methods:**

| Method | Visibility | Return Type | Line |
|---|---|---|---|
| `getService()` | public static | `APKUpdateService` | 10 |

**Types/constants/interfaces defined:** None (all imports are external)

**Imports:**
- `au.com.collectiveintelligence.fleetiq360.BuildConfig` (line 3)
- `au.com.collectiveintelligence.fleetiq360.autoupdate.util.OkHttpClientFactory` (line 4)
- `okhttp3.OkHttpClient` (line 5)
- `retrofit2.Retrofit` (line 6)
- `retrofit2.converter.gson.GsonConverterFactory` (line 7)

**Notable annotations/comments:**
- Line 12: `//noinspection ConstantConditions depends on generated code` — suppression comment on the Retrofit builder block

---

### File 2 — OkHttpClientFactory.java

**Package:** `au.com.collectiveintelligence.fleetiq360.autoupdate.util`

**Class:** `OkHttpClientFactory` (public, no explicit superclass)

**Methods:**

| Method | Visibility | Return Type | Line |
|---|---|---|---|
| `getOkHttpClient()` | public static | `OkHttpClient` | 13 |

**Types/constants/interfaces defined:**
- Anonymous `HostnameVerifier` implementation (inline, line 18–24)

**Imports:**
- `javax.net.ssl.HostnameVerifier` (line 3)
- `javax.net.ssl.SSLContext` (line 4)
- `javax.net.ssl.SSLSession` (line 5)
- `android.annotation.SuppressLint` (line 7)
- `au.com.collectiveintelligence.fleetiq360.WebService.FakeX509TrustManager` (line 8)
- `okhttp3.Dispatcher` (line 9)
- `okhttp3.OkHttpClient` (line 10)

**Notable annotations/suppressions:**
- Line 19: `@SuppressLint("BadHostnameVerifier")` on the anonymous `HostnameVerifier.verify()` override

---

### File 3 — TokenAuthenticator.java

**Package:** `au.com.collectiveintelligence.fleetiq360.autoupdate.util`

**Class:** `TokenAuthenticator` (package-private, implements `okhttp3.Authenticator`)

**Methods:**

| Method | Visibility | Return Type | Line |
|---|---|---|---|
| `authenticate(Route, Response)` | public (override) | `Request` (nullable) | 27 |
| `getAccessToken()` | private | `GetTokenResult` (nullable) | 36 |

**Types/constants/interfaces defined:** None

**Imports:**
- `android.support.annotation.NonNull` (line 3)
- `com.google.gson.Gson` (line 4)
- `java.io.BufferedReader` (line 6)
- `java.io.DataOutputStream` (line 7)
- `java.io.IOException` (line 8)
- `java.io.InputStreamReader` (line 9)
- `java.net.URL` (line 10)
- `javax.annotation.Nullable` (line 12)
- `javax.net.ssl.HttpsURLConnection` (line 13)
- `au.com.collectiveintelligence.fleetiq360.BuildConfig` (line 15)
- `au.com.collectiveintelligence.fleetiq360.WebService.FakeX509TrustManager` (line 16)
- `au.com.collectiveintelligence.fleetiq360.WebService.WebData` (line 17)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.GetTokenResult` (line 18)
- `okhttp3.Authenticator` (line 19)
- `okhttp3.Request` (line 20)
- `okhttp3.Response` (line 21)
- `okhttp3.Route` (line 22)

**Notable annotations:**
- `@Nullable` on `authenticate()` return (line 25) — `javax.annotation.Nullable` rather than `android.support.annotation.Nullable`
- `@NonNull` on `response` parameter (line 27) — from `android.support.annotation`

---

## Step 2 & 3: Findings

---

### A44-1 — CRITICAL: SSL/TLS Validation Completely Disabled (OkHttpClientFactory.java + TokenAuthenticator.java)

**File:** `OkHttpClientFactory.java` lines 16–24; `TokenAuthenticator.java` line 39

**Detail:**

`OkHttpClientFactory.getOkHttpClient()` installs `FakeX509TrustManager` as the SSL trust manager and provides an anonymous `HostnameVerifier` that unconditionally returns `true`. This disables all certificate chain validation and all hostname verification for every request made through this OkHttpClient.

`TokenAuthenticator.getAccessToken()` independently calls `FakeX509TrustManager.allowAllSSL()` at line 39, which calls `HttpsURLConnection.setDefaultHostnameVerifier(...)` and `HttpsURLConnection.setDefaultSSLSocketFactory(...)`. This is a **JVM-global** mutation: it overrides the hostname verifier and SSL socket factory for every `HttpsURLConnection` opened anywhere in the process for the remainder of the process lifetime, not merely for the autoupdate connection. This is a process-wide side effect triggered from a per-request authentication callback.

Both mechanisms together mean the application accepts any certificate from any host, enabling trivial man-in-the-middle interception of all HTTPS traffic including user credentials and session tokens.

**Risk:** An attacker on the same network can intercept and tamper with all server communication, including authentication tokens and APK downloads (allowing installation of malicious APKs).

---

### A44-2 — CRITICAL: Hardcoded Credentials in Production-Accessible Code (TokenAuthenticator.java via WebData.java)

**File:** `TokenAuthenticator.java` line 49; `WebData.java` lines 63–77

**Detail:**

`TokenAuthenticator.getAccessToken()` calls `WebData.instance().getTokenFormData()`, which builds an OAuth password-grant payload with hardcoded values:

- `client_id`: `987654321`
- `client_secret`: `8752361E593A573E86CA558FFD39E`
- `username`: `gas`
- `password`: `ciiadmin`

These credentials are compiled into the release APK and are visible to anyone who decompiles it. Combined with the disabled SSL validation (A44-1), they are also trivially interceptable on the wire. Any party with these credentials can obtain OAuth tokens and authenticate to the backend as the service account.

---

### A44-3 — HIGH: Malicious/Unsafe APK Download Over Unauthenticated Channel with No Integrity Check (APKUpdateServiceFactory.java + OkHttpClientFactory.java)

**File:** `APKUpdateServiceFactory.java` lines 10–20; `OkHttpClientFactory.java` lines 13–34

**Detail:**

`APKUpdateServiceFactory.getService()` uses an `OkHttpClient` produced by `OkHttpClientFactory.getOkHttpClient()`, which has certificate validation disabled (see A44-1). The `APKUpdateService` interface (`downloadPackage`) downloads a full APK binary via this client. There is no evidence of any signature or hash verification of the downloaded APK before it is offered for installation. An on-path attacker can serve an arbitrary APK in place of a legitimate update, which the application will download and present for installation without any integrity guarantee.

---

### A44-4 — HIGH: Global JVM State Mutation from Within OkHttp Authenticator Callback (TokenAuthenticator.java)

**File:** `TokenAuthenticator.java` line 39

**Detail:**

`FakeX509TrustManager.allowAllSSL()` calls `HttpsURLConnection.setDefaultHostnameVerifier()` and `HttpsURLConnection.setDefaultSSLSocketFactory()`. These are static setters that mutate global state for the entire JVM process. Calling this from inside `authenticate()` — which OkHttp may invoke on a background thread from a connection pool thread — introduces a thread-safety hazard (no synchronization on the JVM-global state change) and an uncontrolled side effect on all other `HttpsURLConnection` usage in the application (e.g., Volley, any `URL.openConnection()` call). The scope of effect is unbounded and permanent for the process lifetime.

---

### A44-5 — HIGH: Mixed Annotation Libraries for Nullability (@Nullable and @NonNull) (TokenAuthenticator.java)

**File:** `TokenAuthenticator.java` lines 3, 12, 25, 27

**Detail:**

The file imports and uses two different nullability annotation libraries simultaneously:

- `android.support.annotation.NonNull` (line 3) — used for the `@NonNull Response response` parameter (line 27)
- `javax.annotation.Nullable` (line 12) — used for the `@Nullable` return annotation on `authenticate()` (line 25)

The `okhttp3.Authenticator` interface uses `@Nullable` from `javax.annotation` in its contract, but the `@NonNull` on the same method's parameter comes from the Android Support Library. These are two incompatible annotation systems. Tooling (lint, nullability analysers, annotation processors) that understands one set will not recognise the other, silently creating blind spots. Consistent use of a single library (either `javax.annotation` or `android.support.annotation` / AndroidX) is required.

---

### A44-6 — HIGH: Cross-Package Coupling — autoupdate Module Directly Depends on Core WebService Internals (OkHttpClientFactory.java, TokenAuthenticator.java)

**Files:**
- `OkHttpClientFactory.java` line 8: `import au.com.collectiveintelligence.fleetiq360.WebService.FakeX509TrustManager`
- `TokenAuthenticator.java` lines 16–18: imports of `FakeX509TrustManager`, `WebData`, and `GetTokenResult`

**Detail:**

The `autoupdate` module (package `au.com.collectiveintelligence.fleetiq360.autoupdate.*`) is tightly coupled to three classes in the unrelated core `WebService` package:

1. `FakeX509TrustManager` — an internal SSL-bypass utility from the main web service layer
2. `WebData` — a God Object singleton from the core web-service layer responsible for session management, authentication headers, BLE, and user management
3. `GetTokenResult` — a web service result DTO

`TokenAuthenticator` calls `WebData.instance().getTokenFormData()` to obtain OAuth credentials. This means the autoupdate subsystem cannot function without initialising the entire `WebData` singleton. The autoupdate module is not independently testable or deployable. Any change to `WebData` risks breaking autoupdate behaviour.

---

### A44-7 — MEDIUM: Exception Swallowing via RuntimeException Wrapping Without Logging (OkHttpClientFactory.java)

**File:** `OkHttpClientFactory.java` lines 31–33

**Detail:**

```java
} catch (Exception e) {
    throw new RuntimeException(e);
}
```

The caught exception is wrapped in a `RuntimeException` and re-thrown with no logging. At the call site in `APKUpdateServiceFactory.getService()` there is also no try-catch. If OkHttpClient construction fails (e.g., `SSLContext` initialisation failure in `FakeX509TrustManager.getUnsafeSSLContext()`), the application will crash with an unhandled `RuntimeException` and the developer will have no log entry identifying the root cause, only a wrapped stack trace. Given that `getUnsafeSSLContext()` can silently return `null` (it catches `NoSuchAlgorithmException` and `KeyManagementException` internally via `e.printStackTrace()` without rethrowing), calling `sslContext.getSocketFactory()` at line 17 would produce a `NullPointerException`, which would itself be caught here and re-thrown as a `RuntimeException` with no diagnostic context.

---

### A44-8 — MEDIUM: URL Construction Produces Double-Slash Path (TokenAuthenticator.java vs APKUpdateServiceFactory.java)

**File:** `TokenAuthenticator.java` line 37

**Detail:**

```java
URL refreshUrl = new URL(BuildConfig.BASE_URL + "/oauth/token");
```

`APKUpdateServiceFactory.getService()` (lines 13–14) carefully normalises `BASE_URL` to ensure it ends with a slash before passing it to `Retrofit`. `TokenAuthenticator.getAccessToken()` makes no such normalisation, concatenating `"/oauth/token"` directly onto `BASE_URL`. If `BASE_URL` already ends with a slash (as in the `local` flavour where it is constructed by the Gradle build script), this produces `https://host:port/fleetiq360ws//oauth/token` — a double-slash URL. While many servers tolerate this, it is an inconsistency that indicates the two callers have divergent assumptions about the format of `BASE_URL`. The defensive normalisation done in `APKUpdateServiceFactory` should be replicated everywhere `BASE_URL` is used raw.

---

### A44-9 — MEDIUM: New Gson Instance Allocated Per Authentication Retry (TokenAuthenticator.java)

**File:** `TokenAuthenticator.java` line 59

**Detail:**

```java
return new Gson().fromJson(response.toString(), GetTokenResult.class);
```

A fresh `Gson` instance is constructed on every call to `getAccessToken()`. `Gson` objects are thread-safe and intended to be reused. While not a correctness problem, constructing one per authentication call is unnecessary allocation. However, in the context of this file, this is the lowest-severity issue; it is noted because OkHttp may retry authentication multiple times (once per 401 response), and the pattern is inconsistent with idiomatic Gson usage elsewhere in the codebase (e.g., in `WebData`).

---

### A44-10 — MEDIUM: Dispatcher Concurrency Artificially Limited to 1 (OkHttpClientFactory.java)

**File:** `OkHttpClientFactory.java` lines 26–28

**Detail:**

```java
Dispatcher dispatcher = new Dispatcher();
dispatcher.setMaxRequests(1);
builder.dispatcher(dispatcher);
```

The dispatcher's `maxRequests` is set to 1, serialising all HTTP requests through a single thread. The default OkHttp value is 64 concurrent requests and 5 per host. Setting this to 1 means the APK download (which may be tens of megabytes) will block the authentication refresh, and vice versa, because they share the same dispatcher. This constraint is unexplained by any comment and conflicts with the fact that `APKUpdateService` declares two distinct endpoints (`getLatestAvailableUpdate` and `downloadPackage`). If both are called in sequence it functions correctly, but the constraint prevents any future parallelism and has no justification in this code.

---

### A44-11 — MEDIUM: `APKUpdateServiceFactory` and `OkHttpClientFactory` Are Utility Classes Without Private Constructors (APKUpdateServiceFactory.java, OkHttpClientFactory.java)

**Files:** `APKUpdateServiceFactory.java` line 9; `OkHttpClientFactory.java` line 12

**Detail:**

Both classes expose only `public static` methods and hold no state, making them pure utility classes. Neither defines a private constructor. This allows instantiation (e.g., `new APKUpdateServiceFactory()`) that is meaningless and misleading. Standard Java style for utility classes is to declare a `private` no-arg constructor to prevent instantiation and signal intent.

---

### A44-12 — LOW: `@SuppressLint("BadHostnameVerifier")` Applied to Anonymous Class Override Instead of Narrowest Scope (OkHttpClientFactory.java)

**File:** `OkHttpClientFactory.java` line 19

**Detail:**

```java
@SuppressLint("BadHostnameVerifier")
@Override
public boolean verify(String hostname, SSLSession session) {
    return true;
}
```

The `@SuppressLint` annotation is on the method, which is the correct minimal scope in this context. However, it suppresses an Android lint warning that exists specifically to flag security problems with hostname verification. Using `@SuppressLint` here documents the suppression but masks a genuine security defect (see A44-1) from automated scanning. The suppression is legitimate only if this code is intentionally temporary (e.g., for development/staging); in the present codebase it appears in the production code path shared by all product flavours.

---

### A44-13 — LOW: `//noinspection ConstantConditions` Comment Is Misleading (APKUpdateServiceFactory.java)

**File:** `APKUpdateServiceFactory.java` line 12

**Detail:**

```java
//noinspection ConstantConditions depends on generated code
Retrofit retrofit = new Retrofit.Builder()
        .baseUrl((BuildConfig.BASE_URL.endsWith("/") ? BuildConfig.BASE_URL : BuildConfig.BASE_URL + "/"))
```

The `noinspection` suppression comment is an IntelliJ-specific IDE hint, not a standard Java annotation. It suppresses the `ConstantConditions` inspection that would otherwise warn that `BuildConfig.BASE_URL` might be null (since it is a generated field). The comment does not explain *which* condition is constant or why, making it opaque to reviewers who are not familiar with the specific inspection. Using `@SuppressWarnings("ConstantConditions")` (a standard annotation) would be more portable, and the comment text "depends on generated code" does not sufficiently justify the suppression.

---

### A44-14 — LOW: Resource Leak Risk — `urlConnection` Never Explicitly Disconnected (TokenAuthenticator.java)

**File:** `TokenAuthenticator.java` lines 41–60

**Detail:**

`HttpsURLConnection urlConnection` is opened at line 41 but `urlConnection.disconnect()` is never called. The `InputStream` is closed via try-with-resources (line 55), but the underlying HTTP connection itself is not explicitly disconnected. While the JVM will eventually garbage-collect it, in Android environments persistent connections are pooled and the missing `disconnect()` can cause the connection to remain open longer than intended, holding a file descriptor. This should be wrapped in a `try/finally` block that calls `urlConnection.disconnect()`.

---

## Summary Table

| ID | Severity | File | Description |
|---|---|---|---|
| A44-1 | CRITICAL | OkHttpClientFactory.java, TokenAuthenticator.java | SSL/TLS validation completely disabled; global JVM SSL override |
| A44-2 | CRITICAL | TokenAuthenticator.java (via WebData.java) | Hardcoded OAuth credentials compiled into APK |
| A44-3 | HIGH | APKUpdateServiceFactory.java, OkHttpClientFactory.java | APK downloaded with no certificate validation or integrity check |
| A44-4 | HIGH | TokenAuthenticator.java | JVM-global static SSL state mutated inside OkHttp authenticator callback |
| A44-5 | HIGH | TokenAuthenticator.java | Mixed nullability annotation libraries in same method signature |
| A44-6 | HIGH | OkHttpClientFactory.java, TokenAuthenticator.java | autoupdate module tightly coupled to core WebService internals |
| A44-7 | MEDIUM | OkHttpClientFactory.java | Exception swallowed via RuntimeException wrap with no logging; upstream null risk from FakeX509TrustManager |
| A44-8 | MEDIUM | TokenAuthenticator.java | No BASE_URL normalisation; potential double-slash URL inconsistent with APKUpdateServiceFactory |
| A44-9 | MEDIUM | TokenAuthenticator.java | New Gson instance allocated per authentication retry |
| A44-10 | MEDIUM | OkHttpClientFactory.java | Dispatcher maxRequests set to 1 with no explanation; serialises all requests |
| A44-11 | MEDIUM | APKUpdateServiceFactory.java, OkHttpClientFactory.java | Utility classes missing private constructor; allow spurious instantiation |
| A44-12 | LOW | OkHttpClientFactory.java | @SuppressLint("BadHostnameVerifier") conceals security defect from lint in all flavours |
| A44-13 | LOW | APKUpdateServiceFactory.java | //noinspection IDE hint is opaque and not a standard annotation |
| A44-14 | LOW | TokenAuthenticator.java | HttpsURLConnection never disconnected; potential file descriptor leak |
