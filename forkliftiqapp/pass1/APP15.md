# Pass 1 Security Audit — APP15
**Agent ID:** APP15
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`, but the actual current branch is `master`. Audit proceeds on `master` as instructed.

---

## Step 2 — Checklist Read

Full checklist read from `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`. Sections reviewed:
1. Signing and Keystores
2. Network Security
3. Data Storage
4. Input and Intent Handling
5. Authentication and Session
6. Third-Party Libraries
7. Google Play and Android Platform

---

## Step 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/SaveGPSLocationItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/SavePreStartItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/SaveSessionItem.java`

All three files read in full.

---

## Step 4 — Reading Evidence

### File 1: SaveGPSLocationItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveGPSLocationItem`

**Implements:** `java.io.Serializable`

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `au.com.collectiveintelligence.fleetiq360.WebService.JSONObjectParser`
- `au.com.collectiveintelligence.fleetiq360.model.LocationDb`

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `unit_id` | `int` | 13 |
| `longitude` | `Double` | 14 |
| `latitude` | `Double` | 15 |
| `gps_time` | `String` | 16 |

**Public methods:**
| Method | Signature | Line |
|---|---|---|
| Default constructor | `SaveGPSLocationItem()` | 19 |
| Parameterized constructor | `SaveGPSLocationItem(LocationDb gps)` | 22 |

**No Activities, Services, BroadcastReceivers, or ContentProviders.**

---

### File 2: SavePreStartItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SavePreStartItem`

**Implements:** `java.io.Serializable`

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (wildcard)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (wildcard)

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `start_time` | `String` | 14 |
| `finish_time` | `String` | 15 |
| `comment` | `String` | 16 |
| `session_id` | `int` | 17 |
| `arrAnswers` | `ArrayList<AnswerItem>` | 18 |

**Public methods:**
| Method | Signature | Line |
|---|---|---|
| Default constructor | `SavePreStartItem()` | 20 |
| JSON constructor | `SavePreStartItem(JSONObject jsonObject) throws JSONException` | 23 |

**No Activities, Services, BroadcastReceivers, or ContentProviders.**

---

### File 3: SaveSessionItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveSessionItem`

**Implements:** `java.io.Serializable`

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (wildcard)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (wildcard)

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `id` | `int` | 14 |
| `driver_id` | `int` | 15 |
| `unit_id` | `int` | 16 |
| `start_time` | `String` | 17 |
| `finish_time` | `String` | 18 |
| `prestart_required` | `boolean` | 19 |

**Public methods:**
| Method | Signature | Line |
|---|---|---|
| Default constructor | `SaveSessionItem()` | 21 |
| JSON constructor | `SaveSessionItem(JSONObject jsonObject) throws JSONException` | 24 |

**No Activities, Services, BroadcastReceivers, or ContentProviders.**

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found — Section 1. These are plain data-transfer object (DTO) classes. They contain no signing configuration, keystore references, credentials, or build logic.

---

### Section 2 — Network Security

No issues found — Section 2. These classes are data container/serialization DTOs. They do not instantiate any HTTP client, define any endpoint URL, configure TLS, or perform any network operation. There are no hardcoded server URLs or IP addresses in any of the three files.

---

### Section 3 — Data Storage

**Finding: Public fields exposing sensitive telemetry and operational data**

**Severity: Low-Medium (Code Quality / Defence in Depth)**

All three classes declare every field as `public` with no accessor encapsulation:

- `SaveGPSLocationItem` (lines 13–16): `unit_id`, `longitude`, `latitude`, `gps_time` — precise GPS coordinates of a forklift are operational security data.
- `SavePreStartItem` (lines 14–18): `start_time`, `finish_time`, `comment`, `session_id`, `arrAnswers` — includes free-text operator comments.
- `SaveSessionItem` (lines 14–19): `id`, `driver_id`, `unit_id`, `start_time`, `finish_time`, `prestart_required` — `driver_id` is a direct operator identifier.

Because all fields are `public`, any code in the application (including third-party library code) can read or overwrite these values without any validation or audit trail. For a warehouse/logistics context, `driver_id` combined with GPS coordinates constitutes PII. The fields are not `final`, meaning objects can be mutated after construction.

Additionally, all three classes implement `java.io.Serializable`. Java serialization of objects containing PII (`driver_id`, `latitude`, `longitude`) can expose data through serialized streams written to disk or passed via Intents. There is no `serialVersionUID` declared in any of the three classes, which can cause unpredictable `InvalidClassException` failures during deserialization after version changes, or silent data corruption if field layouts shift between builds. This is a reliability risk that compounds the data-exposure surface of serialization.

**Unused import — `BigDecimal` (SavePreStartItem.java line 8; SaveSessionItem.java line 8):** `java.math.BigDecimal` is imported but not referenced in either file. This is dead code; not a security finding but noted for completeness.

**Unused import — `JSONArray` (SaveGPSLocationItem.java):** `JSONArray` is not imported in this file but `JSONObjectParser` is imported and unused in the compiled class (no method uses it). Not a direct security finding.

No external or local file storage operations are present in these files. No `SharedPreferences`, SQLite, external storage, or `openFileOutput()` calls are present.

---

### Section 4 — Input and Intent Handling

**Finding: No input validation on JSON-deserialized fields**

**Severity: Low**

`SavePreStartItem` (lines 23–59) and `SaveSessionItem` (lines 24–59) both accept a `JSONObject` from an external source (the backend web service response) and assign values directly to public fields without any validation:

- `start_time` and `finish_time` are assigned as raw strings with no format or length validation (lines 30, 35 in `SavePreStartItem`; lines 44, 49 in `SaveSessionItem`).
- `comment` (SavePreStartItem line 40) is assigned as a raw string with no length cap or content sanitisation. If this value is subsequently rendered in a UI component or logged, excessively long or specially crafted values could cause display issues or log injection.
- `session_id` and `driver_id` are stored as `int` — truncation/overflow is possible if the server returns a value outside the 32-bit signed integer range, but this is low-probability in practice.

These classes themselves do not handle Intents, WebViews, deep links, or exported Android components. No issues found for those sub-items.

---

### Section 5 — Authentication and Session

No issues found — Section 5. None of the three files store, transmit, or reference authentication tokens, passwords, or session credentials. `session_id` and `driver_id` in `SaveSessionItem` are integer identifiers used for server-side record linkage, not authentication tokens. No logout logic, token refresh logic, or credential caching is present in these files.

---

### Section 6 — Third-Party Libraries

No issues found — Section 6. These files use only `org.json` (part of the Android SDK standard library) and `java.io.Serializable` (Java standard library). No third-party dependencies are introduced by these files.

---

### Section 7 — Google Play and Android Platform

**Finding: Use of Java Serializable on objects containing PII**

**Severity: Low (Platform Best Practice)**

All three classes implement `java.io.Serializable`. Android's recommended approach for passing data between components is `Parcelable`, which is explicit about what is serialized, does not use reflection, and avoids the deserialization gadget attack surface inherent to Java serialization. While the immediate risk depends on how these objects are passed (if via Intent extras using `putExtra(Serializable)`), the use of `Serializable` for objects containing `driver_id`, `latitude`, and `longitude` is not aligned with Android platform best practice.

`serialVersionUID` is absent from all three classes. The Android documentation and Java serialization specification both recommend declaring an explicit `serialVersionUID` to control version compatibility. Its absence means the JVM auto-generates one based on class structure; any field addition, removal, or reordering between app versions will change the UID and break deserialization of any persisted or transmitted serialized data silently or with an exception.

No `AsyncTask`, deprecated APIs, or missing runtime permission handling is present in these files (these are pure data classes with no UI or lifecycle components).

---

## Summary of Findings

| # | File | Severity | Section | Description |
|---|---|---|---|---|
| 1 | All three files | Low-Medium | 3 — Data Storage | All fields declared `public` with no encapsulation; PII fields (`driver_id`, `latitude`, `longitude`) directly mutable by any caller |
| 2 | All three files | Low | 7 — Platform | `Serializable` used without `serialVersionUID`; `Parcelable` preferred on Android |
| 3 | SavePreStartItem, SaveSessionItem | Low | 4 — Input Handling | No validation on JSON-deserialized string fields (`start_time`, `finish_time`, `comment`) |
| 4 | SavePreStartItem, SaveSessionItem | Informational | 3 — Data Storage | Unused imports (`BigDecimal`, wildcard imports) indicating dead code; not a direct security risk |

No Critical or High severity findings in the three assigned files.
