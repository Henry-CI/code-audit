# Pass 1 Security Audit — Agent APP04
**Repository:** forkliftiqapp (Android/Java)
**Date:** 2026-02-27
**Agent:** APP04

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

DISCREPANCY: Checklist states `Branch: main`. Actual branch is `master`. Branch is confirmed present and correct for audit purposes. Proceeding.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/ShockEventsItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/DriverStatsItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/FakeX509TrustManager.java`

---

## Reading Evidence

### File 1 — ShockEventsItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventsItem`

**Public fields:**
- `public String mac_address` (line 8)
- `public Date time` (line 9)
- `public ImpactLevel level` (line 11)

**Package-private fields:**
- `long magnitude` (line 10) — no access modifier, package-private

**Private constants:**
- `private static final double GFORCE_COEFFICIENT = 0.00388` (line 6)

**Public methods:**
- `public double gForce()` — line 19
- `public enum ImpactLevel { RED, AMBER, BLUE }` — line 23

**Package-private methods:**
- `void calculateImpactLevel(int threshold)` — line 13

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None. Plain data model class.

---

### File 2 — DriverStatsItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.DriverStatsItem`

**Implemented interfaces:** `java.io.Serializable`

**Public fields:**
- `public String field` (line 10)
- `public String object` (line 11)
- `public String value` (line 12)

**Public methods:**
- `public DriverStatsItem()` — line 14 (no-arg constructor)
- `public DriverStatsItem(JSONObject jsonObject) throws JSONException` — line 17

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None. Plain serializable data model class.

---

### File 3 — FakeX509TrustManager.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.FakeX509TrustManager`

**Implemented interfaces:** `javax.net.ssl.X509TrustManager`

**Private static fields:**
- `private static TrustManager[] trustManagers` (line 21)
- `private static final X509Certificate[] _AcceptedIssuers = new X509Certificate[] {}` (line 22-23)

**Public methods:**
- `public void checkClientTrusted(X509Certificate[] x509Certificates, String s) throws CertificateException` — line 26 (OVERRIDE — body is EMPTY)
- `public void checkServerTrusted(X509Certificate[] x509Certificates, String s) throws CertificateException` — line 31 (OVERRIDE — body is EMPTY)
- `public boolean isClientTrusted(X509Certificate[] chain)` — line 35 (returns `true` unconditionally)
- `public boolean isServerTrusted(X509Certificate[] chain)` — line 39 (returns `true` unconditionally)
- `public X509Certificate[] getAcceptedIssuers()` — line 44 (OVERRIDE — returns empty array)
- `public static SSLContext getUnsafeSSLContext()` — line 48 (initializes TLS SSLContext with this permissive TrustManager)
- `public static void allowAllSSL()` — line 67 (sets JVM-wide default HostnameVerifier and SSLSocketFactory)

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None. SSL utility class.

---

## Checklist Section Findings

### 1. Signing and Keystores

No signing configuration, keystore files, Gradle signing blocks, or credential properties are present in any of the three assigned files. These are application-layer model and SSL utility classes; they contain no build or keystore material.

No issues found — Section 1 (Signing and Keystores) for assigned files.

---

### 2. Network Security

**CRITICAL — FakeX509TrustManager.java: Complete SSL Certificate Validation Bypass**

`FakeX509TrustManager` implements `X509TrustManager` with all validation logic deliberately removed. This is an active, production-present SSL bypass with two independent attack surfaces:

**Finding 2.1 — Severity: Critical**
`checkServerTrusted()` (line 31) has an empty body. The `X509TrustManager` contract requires this method to throw `CertificateException` if the server's certificate chain is not trusted. By doing nothing and returning normally, this implementation silently accepts every server certificate presented during a TLS handshake — including expired certificates, self-signed certificates, certificates signed by untrusted or attacker-controlled CAs, and certificates for entirely different hostnames. There is no validation whatsoever.

**Finding 2.2 — Severity: Critical**
`checkClientTrusted()` (line 26) similarly has an empty body. Client certificate validation is bypassed entirely.

**Finding 2.3 — Severity: Critical**
`allowAllSSL()` (line 67) calls `HttpsURLConnection.setDefaultHostnameVerifier(...)` with an anonymous `HostnameVerifier` whose `verify()` method returns `true` unconditionally (line 71). This means that even if a certificate were validated, the hostname on the certificate is never checked against the hostname of the server being contacted. An attacker can present any valid certificate for any domain and it will be accepted.

**Finding 2.4 — Severity: Critical**
`allowAllSSL()` (line 77) calls `HttpsURLConnection.setDefaultSSLSocketFactory(getUnsafeSSLContext().getSocketFactory())`. This sets the bypass as the **process-wide default** for all `HttpsURLConnection` instances. Every HTTPS connection made anywhere in the application after this call is made — including connections to the forkliftiqws backend — operates without certificate validation or hostname verification. A Man-in-the-Middle attacker on the same network as a forklift operator can intercept all traffic, including operator credentials, session tokens, telemetry data, and forklift assignments, with no TLS protection.

**Finding 2.5 — Severity: High**
`getAcceptedIssuers()` (line 44) returns an empty array. This signals to the TLS stack that no certificate issuers are trusted, which in a correctly functioning trust manager would reject all certificates. Combined with the empty `checkServerTrusted()`, the net effect is that the class signals it trusts no issuers but then silently accepts every certificate anyway — a combination that is internally contradictory and entirely bypasses the intended security contract of `X509TrustManager`.

**Finding 2.6 — Severity: Informational**
The file header comment reads `Created by steveyang on 7/6/17`. This class has existed in the codebase since at least 2017 and the class name `FakeX509TrustManager` makes the developer's intent explicit — this was knowingly written as a trust bypass. There is no indication this was intended as a development-only stub that was supposed to be removed before production builds.

Summary: `FakeX509TrustManager.allowAllSSL()` completely disables TLS security for the entire application process. Any operator credentials, session tokens, forklift telemetry, and assignment data transmitted to forkliftiqws are exposed to interception on any network the device connects to.

---

### 3. Data Storage

**DriverStatsItem.java:** Implements `Serializable`. The three public fields (`field`, `object`, `value`) are plain `String` types. If instances of this class are serialized to disk (e.g. via `ObjectOutputStream`, `Intent` extras written to persistent storage, or similar mechanisms), the data would be stored in plaintext. The class itself does not perform any storage operations, so no direct finding can be confirmed from this file alone; however, the use of `Serializable` rather than `Parcelable` and the fully public field exposure are design-level concerns that increase the risk surface if callers serialize sensitive values.

**ShockEventsItem.java:** Public fields `mac_address` and `time` are exposed without access control. The BLE MAC address of a forklift unit could be considered sensitive operational data (it uniquely identifies a physical device). No storage operations are performed in this file.

**FakeX509TrustManager.java:** No data storage operations present.

No direct storage-layer findings confirmed from assigned files — Section 3.

---

### 4. Input and Intent Handling

None of the three assigned files declare Activities, Services, BroadcastReceivers, ContentProviders, or intent filters. None use WebView. No deep link handlers are present.

No issues found — Section 4 (Input and Intent Handling) for assigned files.

---

### 5. Authentication and Session

`FakeX509TrustManager` directly undermines the transport-layer security on which all authentication mechanisms depend. Any token or credential transmitted over a connection using this trust manager is exposed. This amplifies the impact of any authentication weakness elsewhere in the codebase — even a correctly implemented authentication flow is negated if the channel carrying it is unprotected.

No session storage or token handling code is present in the three assigned files directly, but the SSL bypass in `FakeX509TrustManager` is categorised here as well as Section 2 due to its direct impact on credential security in transit.

No additional issues found beyond the SSL bypass already documented — Section 5.

---

### 6. Third-Party Libraries

None of the three assigned files import or reference third-party libraries. `ShockEventsItem.java` uses `java.util.Date`. `DriverStatsItem.java` uses `org.json.JSONObject` and `org.json.JSONException` (Android platform JSON API, not a third-party dependency). `FakeX509TrustManager.java` uses only `javax.net.ssl.*` and `java.security.*` (Java standard library).

No issues found — Section 6 (Third-Party Libraries) for assigned files.

---

### 7. Google Play and Android Platform

**ShockEventsItem.java:** Uses `java.util.Date` (line 9), which is not deprecated on Android but is considered legacy; `java.time.Instant` or `java.time.LocalDateTime` are preferred for new code. This is a low-severity code quality note, not a security finding.

**DriverStatsItem.java:** No deprecated API usage observed.

**FakeX509TrustManager.java:** No deprecated API usage observed within the file itself. The concern is not deprecation but active security harm.

No platform compliance issues found — Section 7 for assigned files.

---

## Finding Summary

| ID | File | Severity | Description |
|----|------|----------|-------------|
| APP04-01 | FakeX509TrustManager.java | **Critical** | `checkServerTrusted()` is empty — all server certificates accepted without validation (line 31) |
| APP04-02 | FakeX509TrustManager.java | **Critical** | `checkClientTrusted()` is empty — client certificate validation fully bypassed (line 26) |
| APP04-03 | FakeX509TrustManager.java | **Critical** | `allowAllSSL()` installs a hostname verifier that always returns `true` — hostname is never checked (line 67-75) |
| APP04-04 | FakeX509TrustManager.java | **Critical** | `allowAllSSL()` sets bypass as process-wide default via `HttpsURLConnection.setDefaultSSLSocketFactory()` — all HTTPS connections affected (line 77) |
| APP04-05 | FakeX509TrustManager.java | **High** | `getAcceptedIssuers()` returns empty array, contradicting the silent accept in `checkServerTrusted()` — entire trust model is incoherent (line 44) |
| APP04-06 | FakeX509TrustManager.java | **Informational** | Class has existed since 2017; name "Fake" indicates deliberate intent; no evidence of dev-only gating |

---

## Branch Discrepancy Record

The checklist header states `Branch: main`. The actual repository default branch is `master`. This is a documentation discrepancy in the checklist, not a repository integrity issue. Audit proceeded on `master`.
