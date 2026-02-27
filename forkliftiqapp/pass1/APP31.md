# Pass 1 Security Audit — APP31
**Agent ID:** APP31
**Date:** 2026-02-27
**Repo:** forkliftiqapp (Android/Java)

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Checklist specifies **Branch: main**, but the actual branch is **master**. This is a discrepancy between the checklist and the repository. Branch is `master` — audit proceeds.

---

## Step 2 — Reading Evidence

### File 1: SaveLicenseResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveLicenseResult`

**Superclass:** `WebServiceResultPacket`
**Interfaces implemented:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `id` | `int` | 14 |
| `licno` | `String` | 15 |
| `addr` | `String` | 16 |
| `expirydt` | `String` | 17 |
| `securityno` | `String` | 18 |

**Public methods:**
| Signature | Line |
|---|---|
| `SaveLicenseResult()` | 20 |
| `SaveLicenseResult(JSONObject jsonObject) throws JSONException` | 23 |

**Android component type:** None (plain Java data class / result packet, not an Activity, Fragment, Service, BroadcastReceiver, or ContentProvider).

---

### File 2: SaveMultipleGPSResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveMultipleGPSResult`

**Superclass:** `WebServiceResultPacket`
**Interfaces implemented:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `unit_id` | `int` | 11 |
| `longitude` | `Double` | 12 |
| `latitude` | `Double` | 13 |
| `gps_time` | `String` | 14 |

**Public methods:**
| Signature | Line |
|---|---|
| `SaveMultipleGPSResult()` | 16 |
| `SaveMultipleGPSResult(JSONObject jsonObject) throws JSONException` | 19 |

**Android component type:** None (plain Java data class / result packet).

---

### File 3: SaveSingleGPSResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.SaveSingleGPSResult`

**Superclass:** `WebServiceResultPacket`
**Interfaces implemented:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `unit_id` | `int` | 12 |
| `longitude` | `Double` | 13 |
| `latitude` | `Double` | 14 |
| `gps_time` | `String` | 15 |

**Public methods:**
| Signature | Line |
|---|---|
| `SaveSingleGPSResult()` | 17 |
| `SaveSingleGPSResult(JSONObject jsonObject) throws JSONException` | 20 |

**Android component type:** None (plain Java data class / result packet).

---

## Step 3 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found — Section 1. These are plain data-model result classes. They contain no signing configuration, keystore references, passwords, or credential material.

---

### Section 2 — Network Security

**Finding — Medium — All three files: All fields are public with no access control.**

All data fields across all three result classes are declared `public` rather than `private`. In `SaveLicenseResult` this includes fields that carry personally identifiable or security-relevant data:

- `SaveLicenseResult.java`, line 14-18:
  - `licno` (license number)
  - `addr` (address)
  - `expirydt` (expiry date)
  - `securityno` (security number)

These fields are populated directly from JSON parsed off a network response (via the `JSONObject` constructor at lines 23-55). Because they are `public`, any code anywhere in the application can read or overwrite them without restriction after deserialization. There are no getters, setters, or validation methods providing any control boundary. If the network layer delivers malformed or attacker-controlled data, there is no validation layer between the raw JSON value and the field.

For `SaveMultipleGPSResult` and `SaveSingleGPSResult`, the GPS coordinate fields (`latitude`, `longitude`, `gps_time`, `unit_id`) are similarly unrestricted. These represent telemetry data for tracked vehicles.

No hardcoded URLs, endpoints, or IP addresses are present in these files. Network communication itself is handled by the superclass `WebServiceResultPacket` and the calling layer — not reviewed here.

No issues found for cleartext traffic, TrustManager overrides, or certificate pinning bypass — these files contain no networking logic.

---

### Section 3 — Data Storage

**Finding — Low — SaveLicenseResult.java: Sensitive fields stored in a Serializable class without protection.**

`SaveLicenseResult` implements `java.io.Serializable` (line 12) and carries fields that may constitute PII or security-relevant data: `licno`, `addr`, `expirydt`, and `securityno`. Because the class is `Serializable`, instances can be written to disk (e.g., via `Intent` extras, `ObjectOutputStream`, or bundle state save/restore) without any encryption. If the calling code passes this object through an `Intent` or saves it to disk without additional protection, the license and security data would be written in plaintext.

`SaveMultipleGPSResult` and `SaveSingleGPSResult` also implement `Serializable` and carry GPS telemetry data, with the same risk profile at lower sensitivity.

No `SharedPreferences`, file I/O, SQLite, or external storage access is present in these files directly. The storage risk is indirect — it depends on how callers handle these objects.

No issues found for `MODE_WORLD_READABLE`, `MODE_WORLD_WRITEABLE`, or `Environment.getExternalStorageDirectory()` — these files contain no file I/O.

---

### Section 4 — Input and Intent Handling

**Finding — Low — All three files: No input validation on JSON-deserialized fields.**

All three constructors accept a `JSONObject` and assign values directly to public fields with no validation:

- `SaveLicenseResult.java` lines 30-53: `id`, `licno`, `addr`, `expirydt`, `securityno` are assigned from JSON without bounds checks, length limits, format validation, or sanitisation.
- `SaveMultipleGPSResult.java` lines 26-45: `unit_id`, `longitude`, `latitude`, `gps_time` are assigned without range validation. Longitude must be in [-180, 180] and latitude in [-90, 90]; no such checks are performed.
- `SaveSingleGPSResult.java` lines 26-45: Same pattern as `SaveMultipleGPSResult`.

If the backend were compromised or the app were subject to a man-in-the-middle attack on a non-validated connection, a malformed response could inject arbitrary string values or out-of-range numeric values into these fields with no client-side rejection.

No WebView, exported components, deep link handlers, or implicit intents are present in these files. No issues found for those sub-items.

---

### Section 5 — Authentication and Session

No issues found — Section 5. These classes carry no authentication tokens, session identifiers, or credentials. They are response deserialization containers. Authentication lifecycle is handled elsewhere.

---

### Section 6 — Third-Party Libraries

No issues found — Section 6. These files import only `org.json` (Android platform) and `java.io.Serializable` (Java standard library). No third-party dependencies are introduced here.

---

### Section 7 — Google Play and Android Platform

**Observation — SaveMultipleGPSResult.java and SaveSingleGPSResult.java: Near-identical classes.**

`SaveMultipleGPSResult` (lines 10-48) and `SaveSingleGPSResult` (lines 10-49) are structurally identical: same four fields (`unit_id`, `longitude`, `latitude`, `gps_time`), same field types, and same JSON parsing logic. The only difference is the class name. This duplication suggests either dead code or a design inconsistency. This is not a security vulnerability but is noted as a code quality observation relevant to maintainability — if one class is updated (e.g., to add validation), the other may not be, creating divergence.

No issues found for `targetSdkVersion`, permissions, deprecated APIs, or runtime permission handling — these are not addressed in result packet data classes.

---

## Summary Table

| Severity | File | Finding |
|---|---|---|
| Medium | SaveLicenseResult.java | All fields public — no access control on sensitive license/address/security data (lines 14-18) |
| Medium | SaveMultipleGPSResult.java | All fields public — no access control on GPS telemetry data (lines 11-14) |
| Medium | SaveSingleGPSResult.java | All fields public — no access control on GPS telemetry data (lines 12-15) |
| Low | SaveLicenseResult.java | Serializable class with PII-adjacent fields — no encryption if serialized to disk |
| Low | SaveMultipleGPSResult.java | Serializable class with telemetry fields — no encryption if serialized |
| Low | SaveSingleGPSResult.java | Serializable class with telemetry fields — no encryption if serialized |
| Low | SaveLicenseResult.java | No input validation on JSON-deserialized fields |
| Low | SaveMultipleGPSResult.java | No range validation on latitude/longitude values |
| Low | SaveSingleGPSResult.java | No range validation on latitude/longitude values |
| Observation | SaveMultipleGPSResult.java + SaveSingleGPSResult.java | Near-identical classes — code duplication risk |

---

## Branch Discrepancy Record

The checklist (`PASS1-CHECKLIST-forkliftiqapp.md`) specifies **Branch: main**. The repository's current branch is **master**. Audit was conducted on the `master` branch as instructed.
