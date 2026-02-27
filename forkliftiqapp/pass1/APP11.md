# Pass 1 Security Audit — APP11
**Agent ID:** APP11
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

The checklist specifies branch `main`. The actual branch is `master`. This is a discrepancy between the checklist and the repository. Audit proceeds on `master` as confirmed.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EquipmentStatsItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EquipmentTypeItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EqupmentUsageItem.java`

---

## Step 3 — Reading Evidence

### File 1: EquipmentStatsItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.EquipmentStatsItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|-------|------|------|
| `unit_id` | `int` | 14 |
| `unit` | `String` | 15 |
| `total` | `double` | 16 |
| `usageList` | `ArrayList<EqupmentUsageItem>` | 17 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `EquipmentStatsItem()` | 19 |
| `EquipmentStatsItem(JSONObject jsonObject) throws JSONException` | 22 |

**Android components declared:** None (plain data class, no Activity/Fragment/Service/Receiver/Provider).

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal` (imported but unused)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

### File 2: EquipmentTypeItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.EquipmentTypeItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|-------|------|------|
| `id` | `int` | 14 |
| `name` | `String` | 15 |
| `url` | `String` | 16 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `EquipmentTypeItem()` | 18 |
| `EquipmentTypeItem(JSONObject jsonObject) throws JSONException` | 21 |

**Android components declared:** None (plain data class).

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray` (imported but unused)
- `java.util.ArrayList` (imported but unused)
- `java.math.BigDecimal` (imported but unused)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

### File 3: EqupmentUsageItem.java

**Note:** Class name contains a typo — `EqupmentUsageItem` (missing letter `i` in `Equipment`). This is a code quality observation.

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.EqupmentUsageItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|-------|------|------|
| `time` | `String` | 14 |
| `usage` | `double` | 15 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `EqupmentUsageItem()` | 17 |
| `EqupmentUsageItem(JSONObject jsonObject) throws JSONException` | 20 |

**Android components declared:** None (plain data class).

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray` (imported but unused)
- `java.util.ArrayList` (imported but unused)
- `java.math.BigDecimal` (imported but unused)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

## Step 4 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found — Section 1. These files are plain data model (DTO) classes. No keystore references, signing configurations, credentials, or build system interactions are present.

---

### Section 2 — Network Security

**Finding — Low — Unvalidated URL field in EquipmentTypeItem**

File: `EquipmentTypeItem.java`, line 16 and line 38.

The class contains a public field `url` of type `String` that is populated directly from a server-supplied JSON response without any validation or sanitisation. There is no check that the value is a valid URL, uses HTTPS, or belongs to an expected domain.

If this URL is subsequently loaded into a WebView, used as a redirect target, or passed to an HTTP client, a compromised or malicious backend response could supply an arbitrary URL — including one pointing to a different host, a non-HTTPS endpoint, or an internal network address. The risk is conditional on how callers consume this field, which is outside the scope of these three files, but the absence of any validation at the point of deserialisation is noteworthy.

No hardcoded API endpoints, server URLs, or IP addresses are present in any of the three files.

No issues found in the remaining areas of Section 2 within these files.

---

### Section 3 — Data Storage

**Finding — Low/Informational — Public fields on Serializable data classes**

All three classes implement `java.io.Serializable` and declare all fields as `public` with no access modifiers restricting visibility. The fields include:

- `EquipmentStatsItem`: `unit_id` (int), `unit` (String), `total` (double), `usageList` (ArrayList)
- `EquipmentTypeItem`: `id` (int), `name` (String), `url` (String)
- `EqupmentUsageItem`: `time` (String), `usage` (double)

Because these classes implement `Serializable`, any code with a reference to an instance can serialize the full object graph — including the nested `ArrayList<EqupmentUsageItem>` in `EquipmentStatsItem` — and write it to any `OutputStream`, including external storage or world-readable locations. There are no `transient` modifiers on any field to exclude sensitive values from serialization. In isolation the data is telemetry/usage data rather than credentials, but the pattern allows callers to inadvertently persist the full object without awareness.

No plain SharedPreferences writes, external storage writes, `MODE_WORLD_READABLE`, or `MODE_WORLD_WRITEABLE` calls are present in these files.

No issues found in the remaining areas of Section 3 within these files.

---

### Section 4 — Input and Intent Handling

**Finding — Low/Informational — No input validation on deserialized JSON fields**

All three constructors accept a `JSONObject` from an external source (the network response from forkliftiqws) and populate fields directly from it without any bounds checking, format validation, or length constraints:

- `EquipmentStatsItem`: `unit_id` is read as `int` (line 29), `unit` as `String` (line 34), `total` as `double` (line 39).
- `EquipmentTypeItem`: `id` as `int` (line 27), `name` as `String` (line 30), `url` as `String` (line 37).
- `EqupmentUsageItem`: `time` as `String` (line 26), `usage` as `double` (line 29).

A malicious or compromised backend could supply oversized strings (e.g. extremely long `unit`, `name`, `time`, or `url` values) or unexpected numeric values. The Android JSON library will not throw on large strings; they will be accepted and stored in memory. If these strings are subsequently rendered in UI components without truncation, they could cause layout issues or in edge cases contribute to denial-of-service through memory exhaustion in low-memory devices.

No exported Android components, implicit intents, WebView usage, or deep link handlers are present in these files.

No issues found in the remaining areas of Section 4 within these files.

---

### Section 5 — Authentication and Session

No issues found — Section 5. These files contain no authentication logic, credential storage, token handling, or session management. They are pure data transfer objects.

---

### Section 6 — Third-Party Libraries

**Finding — Informational — Unused imports across all three files**

Each file imports `java.math.BigDecimal` (all three files), `org.json.JSONArray` (EquipmentTypeItem and EqupmentUsageItem), and `java.util.ArrayList` (EquipmentTypeItem and EqupmentUsageItem) without using them. The wildcard imports `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` and `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` are also included in all three files regardless of whether types from those packages are actually used. While unused imports do not represent a direct security risk, they indicate the files were generated from a template without clean-up, which may mask intentional dependencies and complicates code review.

No third-party library dependencies are introduced by these files beyond the Android platform `org.json` package.

No ProGuard or R8 configuration is present in these files.

No issues found in the remaining areas of Section 6 within these files.

---

### Section 7 — Google Play and Android Platform

No issues found — Section 7. No `AndroidManifest.xml` entries, SDK version references, permissions, runtime permission requests, or deprecated API usages are present in these three files.

**Informational — Typo in class/file name:** `EqupmentUsageItem` (file: `EqupmentUsageItem.java`) is missing the letter `i` in `Equipment`. The misspelling is consistent across the file name, class declaration (line 12), and constructor names (lines 17, 20), and is referenced with the same misspelling in `EquipmentStatsItem.java` (lines 17, 45, 48–49). This is a code quality issue only and has no direct security impact.

---

## Summary Table

| # | Severity | Section | File | Description |
|---|----------|---------|------|-------------|
| 1 | Low | 2 — Network Security | EquipmentTypeItem.java (line 16, 38) | `url` field populated from JSON without validation; if consumed by WebView or HTTP client, arbitrary URLs accepted from backend |
| 2 | Low/Info | 3 — Data Storage | All three files | All fields public on Serializable classes; no `transient` modifiers; full object graph serializable without restriction |
| 3 | Low/Info | 4 — Input Handling | All three files | No bounds or format validation on JSON-deserialized String and numeric fields |
| 4 | Info | 6 — Third-Party Libraries | All three files | Multiple unused imports (`BigDecimal`, `JSONArray`, `ArrayList`, wildcard result imports) indicating templated generation without clean-up |
| 5 | Info | 7 — Platform | EqupmentUsageItem.java | Typo in class/file name (`EqupmentUsageItem` instead of `EquipmentUsageItem`) consistent throughout codebase |
| 6 | Info | Branch | N/A | Checklist specifies branch `main`; actual branch is `master` |
