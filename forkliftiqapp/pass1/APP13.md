# Pass 1 Security Audit — Agent APP13
**App:** forkliftiqapp (Android/Java)
**Date:** 2026-02-27
**Agent:** APP13

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

DISCREPANCY: Checklist specifies `Branch: main`; actual branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/PermissionItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/PreStartHelpItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/PreStartQuestionItem.java`

---

## Step 3 — Reading Evidence

### File 1: PermissionItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.PermissionItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**

| Line | Field | Type |
|------|-------|------|
| 14 | `id` | `int` |
| 15 | `driver_id` | `int` |
| 16 | `driver_name` | `String` |
| 17 | `comp_id` | `int` |
| 18 | `enabled` | `String` |
| 19 | `gsm_token` | `String` |

**Public methods:**

| Line | Signature |
|------|-----------|
| 21 | `PermissionItem()` — default constructor |
| 24 | `PermissionItem(JSONObject jsonObject) throws JSONException` — JSON-parsing constructor |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

### File 2: PreStartHelpItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.PreStartHelpItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**

| Line | Field | Type |
|------|-------|------|
| 14 | `id` | `int` |
| 15 | `input_order` | `int` |
| 16 | `input_type` | `String` |
| 17 | `input_label` | `String` |
| 18 | `input_value` | `String` |
| 19 | `input_image` | `String` |
| 20 | `expected_answer` | `String` |

**Public methods:**

| Line | Signature |
|------|-----------|
| 22 | `PreStartHelpItem()` — default constructor |
| 25 | `PreStartHelpItem(JSONObject jsonObject) throws JSONException` — JSON-parsing constructor |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

### File 3: PreStartQuestionItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.PreStartQuestionItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**

| Line | Field | Type |
|------|-------|------|
| 14 | `id` | `int` |
| 15 | `content` | `String` |
| 16 | `expectedanswer` | `String` |

**Public methods:**

| Line | Signature |
|------|-----------|
| 18 | `PreStartQuestionItem()` — default constructor |
| 21 | `PreStartQuestionItem(JSONObject jsonObject) throws JSONException` — JSON-parsing constructor |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

## Step 4 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found — Section 1. These are plain data-model (DTO) source files. No signing configuration, keystore references, build scripts, or credential values are present in any of the three files.

---

### Section 2 — Network Security

No issues found — Section 2. No HTTP client code, URL construction, TrustManager, HostnameVerifier, or endpoint strings appear in any of the three files. These classes only parse JSON objects received from elsewhere; they do not initiate or configure network connections.

---

### Section 3 — Data Storage

**Finding — Medium: All fields public with no access control across all three classes.**

All three DTOs expose every field as `public` with no getter/setter encapsulation. All three classes implement `java.io.Serializable`. The specific concern in scope of this section:

- `PermissionItem` (line 19): `public String gsm_token` — a GSM/push-notification token is a sensitive credential. It is held as a plain public `String` field on a `Serializable` class. Any code that can reach a `PermissionItem` instance can read or overwrite `gsm_token` without restriction. Because the class is `Serializable`, instances can be written to disk or sent across IPC boundaries (e.g. via Intent extras or object streams) without any custom serialization logic to redact the token. If the serialized form is written to unprotected storage or passed in an implicit Intent, the token is exposed.

- `PermissionItem` (line 15–16): `driver_id` and `driver_name` are PII and are similarly unprotected.

- `PreStartHelpItem` (line 20): `expected_answer` — depending on application context this may represent a safety-critical pre-start checklist expected answer. Exposure as a public field means any component holding this object can silently modify the expected answer in memory, potentially bypassing a pre-start safety check.

- `PreStartQuestionItem` (line 16): `expectedanswer` — same concern as above for the condensed question model.

These are data-model findings rather than storage-layer findings (the classes themselves do not write to disk), but the unguarded public fields and blanket `Serializable` implementation create conditions where sensitive data can leak through storage or IPC paths controlled by other parts of the application.

---

### Section 4 — Input and Intent Handling

No issues found — Section 4. None of the three files declare or handle Intents, deep links, WebViews, or exported components. The JSON-parsing constructors use `JSONObject.isNull()` guards before each field read, which prevents null-pointer exceptions on missing keys. No deserialization of untrusted input occurs within these files directly (the JSONObject is passed in from a calling layer not visible here).

Note for the broader audit: because all three classes implement `Serializable`, any code that deserialises instances of these classes from untrusted byte streams (e.g. from an Intent extra or a file) should be flagged when those call sites are reviewed. The classes themselves do not implement `readObject()`/`readResolve()` controls. This is recorded as an observation for later passes, not a finding against these files in isolation.

---

### Section 5 — Authentication and Session

**Observation — Informational: `gsm_token` field in `PermissionItem`.**

`PermissionItem.gsm_token` (line 19) appears to carry an authentication/push token for the driver. No issues with token storage or expiry can be assessed from this DTO alone; the risk is recorded under Section 3 above. No session management, login, or logout logic is present in any of these files.

No additional issues found — Section 5.

---

### Section 6 — Third-Party Libraries

No issues found — Section 6. The only imports across all three files are `org.json.*`, `java.io.Serializable`, `java.util.ArrayList`, and `java.math.BigDecimal` — all platform/standard library classes. No third-party library dependencies are introduced by these files.

---

### Section 7 — Google Play and Android Platform

No issues found — Section 7. No SDK version references, permissions declarations, deprecated API calls, or runtime permission requests appear in any of the three files. These are pure data-model classes with no Android framework dependencies beyond the standard Java serialization contract.

---

## Summary of Findings

| # | Severity | Section | File | Description |
|---|----------|---------|------|-------------|
| 1 | Medium | 3 — Data Storage | `PermissionItem.java` line 19 | `gsm_token` stored as an unguarded public field on a `Serializable` class; token can be read, overwritten, or serialised to disk/IPC without restriction. |
| 2 | Low | 3 — Data Storage | `PermissionItem.java` lines 15–16 | `driver_id` and `driver_name` (PII) exposed as public fields on a `Serializable` class with no access control. |
| 3 | Low | 3 — Data Storage | `PreStartHelpItem.java` line 20 | `expected_answer` exposed as a public field; in-memory tampering with safety-critical pre-start checklist data is not prevented. |
| 4 | Low | 3 — Data Storage | `PreStartQuestionItem.java` line 16 | `expectedanswer` exposed as a public field; same concern as Finding 3. |
| 5 | Informational | 4 — Input/Intent | All three files | All classes implement `Serializable` without `readObject()`/`readResolve()` guards; deserialisation call sites should be reviewed in later passes for untrusted-input risk. |

---

## Branch Discrepancy Record

Checklist header states `Branch: main`. The repository's active branch is `master`. This discrepancy is noted here for checklist maintenance. Audit was conducted on `master`.
