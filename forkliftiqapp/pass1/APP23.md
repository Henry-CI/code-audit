# Pass 1 Security Audit — Agent APP23
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** Checklist specifies `Branch: main`; actual branch is `master`. Branch is `master` as expected for this repository. Proceeding.

---

## Step 2 — Checklist Reviewed

All sections read: Signing and Keystores, Network Security, Data Storage, Input and Intent Handling, Authentication and Session, Third-Party Libraries, Google Play and Android Platform.

---

## Step 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveShockEventParameter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveSingleGPSParameter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SessionEndParameter.java`

Supporting files read for inheritance chain and field context:
- `WebServiceParameterPacket.java`
- `WebServicePacket.java`
- `SaveShockEventItem.java`
- `SessionResult.java`

---

## Step 4 — Reading Evidence

### File 1: SaveShockEventParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveShockEventParameter`

**Inheritance chain:**
`SaveShockEventParameter` → `WebServiceParameterPacket` → `WebServicePacket` → `Object`

All three levels implement `java.io.Serializable`.

**Fields (declared in this class):**

| Visibility | Type | Name | Line |
|---|---|---|---|
| `public` | `ArrayList<SaveShockEventItem>` | `impactList` | 11 |

**Inherited fields from `WebServiceParameterPacket`:** None declared.
**Inherited fields from `WebServicePacket`:** None declared.

**Public methods:**

| Signature | Line |
|---|---|
| `SaveShockEventParameter()` (constructor) | 13 |

**Activity / Fragment / Service / BroadcastReceiver / ContentProvider:** None. This is a plain data transfer object (DTO).

---

### File 2: SaveSingleGPSParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveSingleGPSParameter`

**Inheritance chain:**
`SaveSingleGPSParameter` → `WebServiceParameterPacket` → `WebServicePacket` → `Object`

All levels implement `java.io.Serializable`.

**Fields (declared in this class):**

| Visibility | Type | Name | Line |
|---|---|---|---|
| `public` | `int` | `unit_id` | 9 |
| `public` | `Double` | `longitude` | 10 |
| `public` | `Double` | `latitude` | 11 |
| `public` | `String` | `gps_time` | 12 |

**Inherited fields from `WebServiceParameterPacket`:** None declared.
**Inherited fields from `WebServicePacket`:** None declared.

**Public methods:**

| Signature | Line |
|---|---|
| `SaveSingleGPSParameter()` (constructor) | 14 |

**Activity / Fragment / Service / BroadcastReceiver / ContentProvider:** None. Plain DTO.

---

### File 3: SessionEndParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SessionEndParameter`

**Inheritance chain:**
`SessionEndParameter` → `WebServiceParameterPacket` → `WebServicePacket` → `Object`

All levels implement `java.io.Serializable`.

**Fields (declared in this class):**

| Visibility | Type | Name | Line |
|---|---|---|---|
| `public` | `int` | `id` | 10 |
| `public` | `String` | `finish_time` | 11 |
| `public` | `boolean` | `prestart_required` | 12 |

**Inherited fields from `WebServiceParameterPacket`:** None declared.
**Inherited fields from `WebServicePacket`:** None declared.

**Public methods:**

| Signature | Line |
|---|---|
| `SessionEndParameter()` (no-arg constructor) | 14 |
| `SessionEndParameter(SessionResult result)` (constructor) | 17 |

**Activity / Fragment / Service / BroadcastReceiver / ContentProvider:** None. Plain DTO.

---

## Step 5 — Checklist Review

### Section 1 — Signing and Keystores

These three files are parameter DTOs with no involvement in signing, keystore configuration, Gradle build scripts, or pipeline definitions. They contain no credentials, passwords, or keystore references.

**No issues found — Signing and Keystores**

---

### Section 2 — Network Security

These files are parameter packet classes that model data sent to the forkliftiqws backend. Relevant observations:

- None of the three classes construct HTTP/HTTPS connections, configure SSL contexts, or set hostname verifiers.
- No API endpoint URLs or IP addresses are hardcoded in any of the three files.
- No `TrustAllCertificates`, `hostnameVerifier`, or `SSLContext` usage is present.
- The classes are serialised (`Serializable`) and passed to a higher-level web service layer (not audited in this assignment). The security of transport depends on that calling layer, which is outside scope for these files.

**No issues found — Network Security**

---

### Section 3 — Data Storage

**Finding — Medium: Public fields on Serializable DTOs carrying sensitive telemetry and session data**

All three parameter classes declare all fields as `public` with no access control. The data carried includes:

- `SaveSingleGPSParameter`: `latitude`, `longitude`, `unit_id`, `gps_time` — real-time GPS location of a forklift unit. This constitutes location PII tied to a physical asset and potentially to an operator on shift.
- `SessionEndParameter`: `id` (session ID), `finish_time`, `prestart_required` — operator session lifecycle data.
- `SaveShockEventParameter`: a list of `SaveShockEventItem` objects, each containing `impact_time`, `impact_value`, and `mac_address` of the BLE sensor device.

The `mac_address` field in `SaveShockEventItem` (the item type within `SaveShockEventParameter.impactList`) is a hardware identifier for a BLE sensor. MAC addresses are persistent hardware identifiers that can be used to track specific devices.

All three classes implement `java.io.Serializable`. Java serialization is a known attack surface: if these objects are serialised to disk (e.g., as intent extras written to SharedPreferences, files, or SQLite), the serialised bytes may be readable by other processes or exfiltrated via ADB backup if `android:allowBackup` is enabled. Whether these objects are persisted to storage cannot be confirmed from these files alone; the risk depends on calling code.

No direct calls to `openFileOutput`, `SharedPreferences`, `SQLite`, or `getExternalStorageDirectory` appear in these files.

**Finding — Low: No input validation on `gps_time` and `finish_time` string fields**

`SaveSingleGPSParameter.gps_time` and `SessionEndParameter.finish_time` are raw `String` fields with no validation or sanitisation in these classes. If these strings are constructed from user-controlled or device-controlled input before being passed to the web service, injection risks (e.g., malformed timestamps influencing server-side parsing) exist at the call site. This cannot be fully assessed from these files alone.

**No issues found regarding MODE_WORLD_READABLE, MODE_WORLD_WRITEABLE, external storage, or credential caching in static fields in these files.**

---

### Section 4 — Input and Intent Handling

These files are plain DTOs — they do not declare any Android components (Activity, Service, BroadcastReceiver, ContentProvider), have no `android:exported` attribute relevance, do not handle intents, do not configure WebViews, and do not process deep links.

**No issues found — Input and Intent Handling**

---

### Section 5 — Authentication and Session

`SessionEndParameter` carries `id` (session ID) and `finish_time`, which are session lifecycle fields. Within these files, there is no authentication credential (username, password, token) stored or transmitted. The session ID (`id`) is an `int` and provides no credential value on its own.

The constructor `SessionEndParameter(SessionResult result)` copies `id`, `finish_time`, and `prestart_required` from a `SessionResult` object. `SessionResult` also contains `driver_id` and `unit_id`, which are **not** copied into `SessionEndParameter` — this is consistent with the principle of minimal data inclusion, though it is incidental design rather than an enforced access control pattern.

No token storage, no credential caching, no logout logic present in these files (outside scope for DTOs).

**No issues found — Authentication and Session**

---

### Section 6 — Third-Party Libraries

These files import only:
- `java.io.Serializable` (JDK standard library)
- `java.util.ArrayList` (JDK standard library)
- Internal package classes (`WebServiceParameterPacket`, `SaveShockEventItem`, `SessionResult`)

No third-party library dependencies are introduced by these files.

**No issues found — Third-Party Libraries**

---

### Section 7 — Google Play and Android Platform

These files contain no Android API calls, no deprecated API usage, no permission declarations, and no SDK version dependencies. They are pure Java data classes.

**No issues found — Google Play and Android Platform**

---

## Summary of Findings

| ID | Severity | File | Description |
|---|---|---|---|
| APP23-01 | Medium | SaveShockEventParameter.java, SaveSingleGPSParameter.java, SessionEndParameter.java | All fields on all three DTOs are `public` with no access modifiers. Classes implement `java.io.Serializable`. If serialised to persistent storage, sensitive telemetry data (GPS coordinates, BLE MAC address, session IDs) may be exposed via ADB backup or filesystem access. Risk is contingent on calling layer behaviour. |
| APP23-02 | Low | SaveSingleGPSParameter.java, SessionEndParameter.java | `gps_time` and `finish_time` are raw unvalidated `String` fields. No sanitisation is enforced at the DTO level. Injection or parsing risk exists at the server if these strings are caller-controlled; full assessment requires review of call sites. |

---

## Branch Discrepancy Note

The checklist header states `Branch: main`. The repository's actual default branch is `master`. This is a documentation discrepancy in the checklist; no remediation action is required in the codebase for this audit.
