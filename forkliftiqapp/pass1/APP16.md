# Pass 1 Security Audit — APP16
**Agent ID:** APP16
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

DISCREPANCY: Checklist specifies `Branch: main`. Actual branch is `master`. Proceeding on `master` as instructed.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/SaveShockEventItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/ServiceRecordItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/ServiceSummaryItem.java`

---

## Step 3 — Reading Evidence

### File 1: SaveShockEventItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.SaveShockEventItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `impact_time` | `String` | 13 |
| `impact_value` | `long` | 14 |
| `mac_address` | `String` | 15 |

**Public methods / constructors:**
| Signature | Line |
|---|---|
| `SaveShockEventItem()` | 17 |
| `SaveShockEventItem(ShockEventsDb event)` | 20 |
| `SaveShockEventItem(JSONObject jsonObject) throws JSONException` | 26 |

**Android component type:** None (plain data/model class — no Activity, Fragment, Service, BroadcastReceiver, ContentProvider).

**Imports of note:**
- `au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventsDb`
- `au.com.collectiveintelligence.fleetiq360.WebService.JSONObjectParser`
- `au.com.collectiveintelligence.fleetiq360.util.ServerDateFormatter`
- `org.json.JSONObject`
- `java.io.Serializable`

---

### File 2: ServiceRecordItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.ServiceRecordItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `acc_hours` | `double` | 14 |
| `unit_name` | `String` | 15 |
| `service_due` | `double` | 16 |
| `last_serv` | `int` | 17 |
| `next_serv` | `int` | 18 |
| `serv_duration` | `int` | 19 |
| `service_type` | `String` | 20 |
| `unit_id` | `int` | 21 |

**Public methods / constructors:**
| Signature | Line |
|---|---|
| `ServiceRecordItem()` | 23 |
| `ServiceRecordItem(JSONObject jsonObject) throws JSONException` | 26 |

**Android component type:** None (plain data/model class).

**Imports of note:**
- `org.json.JSONObject`, `org.json.JSONArray`
- `java.util.ArrayList`, `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`
- `java.io.Serializable`

**Note:** `JSONArray`, `ArrayList`, and `BigDecimal` are imported but unused in this file.

---

### File 3: ServiceSummaryItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.ServiceSummaryItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|---|---|---|
| `unit_id` | `int` | 14 |
| `acc_hours` | `int` | 15 |
| `service_due` | `int` | 16 |
| `last_serv` | `int` | 17 |
| `next_serv` | `int` | 18 |
| `serv_duration` | `int` | 19 |
| `unit_name` | `String` | 20 |
| `service_type` | `String` | 21 |

**Public methods / constructors:**
| Signature | Line |
|---|---|
| `ServiceSummaryItem()` | 23 |
| `ServiceSummaryItem(JSONObject jsonObject) throws JSONException` | 26 |

**Android component type:** None (plain data/model class).

**Imports of note:**
- `org.json.JSONObject`, `org.json.JSONArray`
- `java.util.ArrayList`, `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`
- `java.io.Serializable`

**Note:** `JSONArray`, `ArrayList`, and `BigDecimal` are imported but unused in this file.

---

## Step 4 — Checklist Review (All Sections)

### Section 1 — Signing and Keystores

No signing configuration, keystore references, pipeline scripts, Gradle files, or properties files are present in the assigned files. These three files are pure data model classes with no build or signing relevance.

No issues found — Section 1 (Signing and Keystores). Out of scope for assigned files.

---

### Section 2 — Network Security

No HTTP client usage, no URL construction, no base URLs, no SSL/TLS configuration, no `TrustManager`, no `HostnameVerifier` overrides, and no hardcoded endpoints appear in any of the three files.

The classes receive pre-parsed `JSONObject` instances as constructor arguments; they do not initiate or configure network connections themselves.

No issues found — Section 2 (Network Security). Out of scope for assigned files.

---

### Section 3 — Data Storage

**Finding — Low: All fields public with no access control**

Severity: Low
Files affected:
- `SaveShockEventItem.java` (lines 13–15): `impact_time`, `impact_value`, `mac_address`
- `ServiceRecordItem.java` (lines 14–21): all eight fields
- `ServiceSummaryItem.java` (lines 14–21): all eight fields

All fields across all three classes are declared `public`. There are no private fields, no getters, no setters, and no validation on assignment. While these are DTO (Data Transfer Object) / model classes and the pattern is common in Android projects of this vintage, public fields mean any code with a reference to the object can freely mutate `mac_address`, `unit_name`, `unit_id`, or service scheduling data (e.g. `next_serv`, `service_due`) without any validation or audit trail.

`mac_address` in `SaveShockEventItem` identifies a specific BLE device and is sent to the backend. Unrestricted mutation of this field in-memory could cause telemetry to be attributed to the wrong asset.

No encrypted storage, external storage, or `SharedPreferences` usage is present in these files. The classes do not persist data themselves.

No issues found relating to external storage, `SharedPreferences`, or `allowBackup` — out of scope for assigned files.

---

### Section 4 — Input and Intent Handling

**Finding — Low: No input validation on JSON-parsed string fields**

Severity: Low
Files affected:
- `SaveShockEventItem.java` (lines 31, 33): `impact_time` and `mac_address` assigned directly from JSON strings with no format or length validation.
- `ServiceRecordItem.java` (lines 38, 62): `unit_name` and `service_type` assigned directly from JSON strings with no sanitisation.
- `ServiceSummaryItem.java` (lines 63, 68): `unit_name` and `service_type` assigned directly from JSON strings with no sanitisation.

`JSONObjectParser.getString()` (used in `SaveShockEventItem`) and `JSONObject.getString()` (used in `ServiceRecordItem` and `ServiceSummaryItem`) return raw server-supplied string values. If these values are subsequently rendered in UI components without escaping, they create a stored XSS equivalent in a native WebView context, or could produce display corruption. The risk is bounded by the fact that these fields originate from the backend rather than direct user input, but the backend is trusted implicitly and there is no defensive validation at the client boundary.

No WebView usage, exported components, deep link handlers, or implicit intents are present in the assigned files.

No issues found relating to WebView, exported components, or intent handling — out of scope for assigned files.

---

### Section 5 — Authentication and Session

No authentication logic, token handling, credential storage, logout logic, or session management is present in any of the three files. These are pure data model classes.

No issues found — Section 5 (Authentication and Session). Out of scope for assigned files.

---

### Section 6 — Third-Party Libraries

**Observation — Informational: Unused imports (dead imports)**

Files affected:
- `ServiceRecordItem.java` (lines 6–10): `JSONArray`, `ArrayList`, `BigDecimal`, and the wildcard imports `webserviceclasses.*` and `webserviceclasses.results.*` are imported but none of their types are referenced in the file body.
- `ServiceSummaryItem.java` (lines 6–10): same set of unused imports.

These are not a security finding in isolation, but wildcard imports (`import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`) increase the implicit surface area of the compilation unit and can mask unintended name resolution if new classes are introduced into those packages. This is a code quality observation rather than a vulnerability.

No third-party library CVEs or ProGuard configuration is assessable from these files.

No issues found — Section 6 (Third-Party Libraries). Out of scope for assigned files.

---

### Section 7 — Google Play and Android Platform

No `targetSdkVersion`, `minSdkVersion`, permissions, deprecated API usage, or runtime permission requests are present in the assigned files.

**Observation — Informational: `Serializable` without `serialVersionUID`**

All three classes implement `java.io.Serializable` without declaring a `serialVersionUID` field. The Java runtime will auto-generate one based on class structure, meaning that any field addition, removal, or reordering will change the auto-generated UID and cause deserialization to fail with `InvalidClassException` if objects serialized under one version of the app are read under another (e.g., across app updates where data is persisted to a file or passed via Intent extras). This is a robustness/correctness issue; it is not a security vulnerability in itself, but deserialization of `Serializable` objects from untrusted sources (Intent extras, IPC) without input validation can become a gadget chain attack surface in Android. The current files carry no sensitive credentials.

No issues found relating to SDK targeting, permissions, deprecated APIs, or runtime permissions — out of scope for assigned files.

---

## Summary of Findings

| ID | Severity | File | Section | Description |
|---|---|---|---|---|
| APP16-001 | Low | All three files | 3 — Data Storage | All fields are `public` with no access control. Fields can be mutated without validation, including `mac_address` used for asset identification. |
| APP16-002 | Low | `SaveShockEventItem.java`, `ServiceRecordItem.java`, `ServiceSummaryItem.java` | 4 — Input Handling | String fields populated from JSON without length or format validation. If rendered downstream without escaping, creates injection risk in UI or WebView contexts. |
| APP16-003 | Informational | `ServiceRecordItem.java`, `ServiceSummaryItem.java` | 6 — Libraries | Unused imports including wildcard imports. Code quality issue; no direct security impact. |
| APP16-004 | Informational | All three files | 7 — Platform | `Serializable` implemented without `serialVersionUID`. Robustness risk across app updates; not a direct security vulnerability in these files but increases deserialization attack surface if objects are ever passed via IPC. |

No Critical or High findings in the assigned files.
