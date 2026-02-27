# Pass 1 Security Audit — Agent APP33

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** Checklist specifies `Branch: main`; actual branch is `master`. Audit proceeds on `master`.

---

## Reading Evidence

### File 1: SessionResult.java

**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/SessionResult.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SessionResult`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Public fields:**

| Field | Type | Line |
|---|---|---|
| `WARNING_MINUTES` | `static final int` | 15 |
| `id` | `int` | 17 |
| `driver_id` | `int` | 18 |
| `unit_id` | `int` | 19 |
| `prestart_required` | `boolean` | 20 |
| `start_time` | `String` | 21 |
| `finish_time` | `String` | 22 |

**Public methods:**

| Signature | Line |
|---|---|
| `SessionResult()` | 24 |
| `SessionResult(JSONObject jsonObject) throws JSONException` | 27 |
| `void preEnd()` | 40 |
| `void end()` | 48 |
| `boolean shouldShowWarning()` | 53 |
| `boolean isFinished()` | 60 |

No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.

---

### File 2: UserRegisterResult.java

**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/UserRegisterResult.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.UserRegisterResult`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Public fields:**

| Field | Type | Line |
|---|---|---|
| `id` | `int` | 14 |
| `first_name` | `String` | 15 |
| `last_name` | `String` | 16 |
| `email` | `String` | 17 |
| `password` | `String` | 18 |
| `phone` | `String` | 19 |
| `licno` | `String` | 20 |
| `expirydt` | `String` | 21 |
| `addr` | `String` | 22 |
| `securityno` | `String` | 23 |
| `photo` | `String` | 24 |
| `createdat` | `String` | 25 |
| `updatedat` | `String` | 26 |
| `active` | `String` | 27 |
| `contactperson` | `boolean` | 28 |
| `ranking` | `String` | 29 |

**Public methods:**

| Signature | Line |
|---|---|
| `UserRegisterResult()` | 31 |
| `UserRegisterResult(JSONObject jsonObject) throws JSONException` | 34 |

No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.

---

## Checklist Review

### 1. Signing and Keystores

No signing configuration, keystore files, Gradle build configuration, `gradle.properties`, `local.properties`, or `bitbucket-pipelines.yml` are present in the assigned files. These are plain data-model / result-packet classes.

No issues found — Signing and Keystores

---

### 2. Network Security

No HTTP client usage, URL construction, or network configuration is present in the assigned files. These classes are deserialized result packets; they receive already-parsed JSON data through `JSONObjectParser` and `JSONObject`. No hardcoded endpoints or IP addresses are present.

No issues found — Network Security

---

### 3. Data Storage

**Finding — HIGH: Password deserialized and held in a public plain-text field (UserRegisterResult.java, line 18)**

`UserRegisterResult` contains a `public String password` field (line 18). This field is populated directly from the server JSON response at line 62–64:

```java
if (!jsonObject.isNull("password"))
{
    password = jsonObject.getString("password");
}
```

The password value received from the server is stored as a plain `String` in a public, mutable instance field on a `Serializable` object. Issues arising from this pattern:

1. The field is `public` — any code in the application can read or write the credential without restriction.
2. The class implements `java.io.Serializable`. A `Serializable` object holding a password can be written to disk, passed in an `Intent` extra, or stored in a `Bundle` — all without any encryption. If this object is ever serialized (e.g., placed in a `SharedPreferences` store, written to a file, or passed between Activities as an `Intent` extra), the plaintext password persists on the device.
3. Java `String` objects are immutable and interned; the password value cannot be zeroed from memory after use, unlike a `char[]`. This extends the window during which the credential is available to a memory dump.
4. This likely indicates the server is returning a user password in a registration or profile API response. A server that transmits the user's password back to the client in API responses is a serious backend design deficiency — passwords should never leave the authentication boundary in this direction.

**Finding — MEDIUM: Session identifiers and operator data held in public fields (SessionResult.java)**

`SessionResult` exposes `id`, `driver_id`, `unit_id`, `start_time`, and `finish_time` as `public` fields on a `Serializable` class (lines 17–22). `driver_id` in particular identifies the operator. Because the class is `Serializable`, instances can be written to disk or passed through `Intent` extras without encryption. If calling code serializes and stores `SessionResult` objects in `SharedPreferences` or a file, operator session data will be stored in plaintext.

No issues found for `MODE_WORLD_READABLE`, `MODE_WORLD_WRITEABLE`, `getExternalStorageDirectory()`, or `allowBackup` (not applicable to these files).

---

### 4. Input and Intent Handling

No `Intent` construction, WebView usage, or deep-link handling is present in the assigned files.

No issues found — Input and Intent Handling

---

### 5. Authentication and Session

**Finding — HIGH: Password returned from server and stored in-memory as plaintext (UserRegisterResult.java, line 18)**

As described under Data Storage: the `password` field on `UserRegisterResult` indicates the backend API returns the user's password in a registration or profile API response. This is a server-side protocol deficiency with direct impact on authentication security. The client-side class materialises and retains this value in a publicly accessible, Serializable object. There is no evidence of zeroing or scoping the credential after use.

**Finding — LOW: No token expiry handling in SessionResult**

`SessionResult` tracks `finish_time` and provides `isFinished()` and `shouldShowWarning()` to detect session expiry. There is no evidence within this class of a mechanism to re-authenticate or clear credentials when the session expires — calling code is responsible for acting on the return value of `isFinished()`. This is a design observation; the risk depends on whether calling code handles the expired state correctly (outside scope of these two files).

No issues found — logout clearing, multi-operator shift handling (not present in these files).

---

### 6. Third-Party Libraries

The assigned files import only `org.json` (Android platform JSON), `java.io.Serializable`, `java.util.Calendar`, `java.util.Date`, `java.math.BigDecimal` (imported but unused in `UserRegisterResult`), and project-internal packages. No third-party library dependencies are declared or used in the assigned files.

**Observation — LOW: Unused import in UserRegisterResult.java (line 8)**

`import java.math.BigDecimal;` is present at line 8 but no `BigDecimal` symbol is referenced anywhere in the class body. This is dead code with no security impact but indicates the file may have been generated automatically without cleanup.

No issues found — Third-Party Libraries (security)

---

### 7. Google Play and Android Platform

No `build.gradle`, `AndroidManifest.xml`, permissions, `targetSdkVersion`, `minSdkVersion`, or deprecated API usage is present in the assigned files. `Calendar.getInstance()` and `Calendar.add()` are used in `SessionResult` — these APIs are not deprecated and carry no security implication.

No issues found — Google Play and Android Platform

---

## Summary of Findings

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| APP33-01 | High | `UserRegisterResult.java` | 18, 61–64 | Password received from server API and stored in a `public` plaintext `String` field on a `Serializable` object. Server is transmitting user password in API response — passwords must not leave the authentication boundary. |
| APP33-02 | High | `UserRegisterResult.java` | 12, 18 | `Serializable` class holding a password field can be serialized to disk or passed in `Intent` extras in plaintext, exposing the credential beyond its intended scope. |
| APP33-03 | Medium | `SessionResult.java` | 17–22 | Operator `driver_id`, session `id`, and session timestamps held as `public` fields on a `Serializable` class; if serialized and stored, operator session data persists in plaintext. |
| APP33-04 | Low | `UserRegisterResult.java` | 8 | Unused import `java.math.BigDecimal` — dead code, no security impact. |
| APP33-05 | Low | `SessionResult.java` | 60–63 | No in-class credential clearing upon session expiry; reliance on calling code to act on `isFinished()` result. |
