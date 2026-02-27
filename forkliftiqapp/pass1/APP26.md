# Pass 1 Security Audit — APP26
**Agent ID:** APP26
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

DISCREPANCY: The checklist specifies Branch: `main`. The actual branch is `master`. Proceeding on `master` as instructed.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/CommonResult.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/EquipmentStatsResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/EquipmentTypeResultArray.java`

---

## Reading Evidence

### File 1: CommonResult.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.CommonResult`

**Superclass:** `WebServiceResultPacket` (implements `Serializable`)

**Fields (all public):**
- `public String id` (line 14)
- `public String error` (line 15)

**Public methods:**
- `CommonResult()` — no-arg constructor (line 17)
- `CommonResult(JSONObject jsonObject) throws JSONException` — constructor parsing `id` and `error` from JSON (line 20)

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

### File 2: EquipmentStatsResultArray.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.EquipmentStatsResultArray`

**Superclass:** `WebServiceResultPacket` (implements `Serializable`)

**Fields (all public):**
- `public ArrayList<EquipmentStatsItem> arrayList` (line 14)

**Public methods:**
- `EquipmentStatsResultArray()` — no-arg constructor (line 16)
- `EquipmentStatsResultArray(JSONArray jsonArray) throws JSONException` — constructor that iterates a JSON array and populates `arrayList` with `EquipmentStatsItem` instances (line 19)

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

### File 3: EquipmentTypeResultArray.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.EquipmentTypeResultArray`

**Superclass:** `WebServiceResultPacket` (implements `Serializable`)

**Fields (all public):**
- `public ArrayList<EquipmentTypeItem> arrayList` (line 14)

**Public methods:**
- `EquipmentTypeResultArray()` — no-arg constructor (line 16)
- `EquipmentTypeResultArray(JSONArray jsonArray) throws JSONException` — constructor that iterates a JSON array and populates `arrayList` with `EquipmentTypeItem` instances (line 19)

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

## Security Findings by Checklist Section

### 1. Signing and Keystores

No signing configuration, keystore files, or build.gradle content present in these files.

No issues found — Signing and Keystores (out of scope for assigned files).

---

### 2. Network Security

No HTTP client calls, URL construction, endpoint definitions, or network configuration present in these files. These are pure data model / deserialization classes.

No issues found — Network Security (out of scope for assigned files).

---

### 3. Data Storage

**FINDING — Low/Informational: Overly broad public field visibility exposing deserialized data.**

All data-bearing fields in all three classes are declared `public` rather than `private` with accessors:

- `CommonResult.id` (line 14)
- `CommonResult.error` (line 15)
- `EquipmentStatsResultArray.arrayList` (line 14)
- `EquipmentTypeResultArray.arrayList` (line 14)

Any class holding a reference to these result objects can read and mutate the fields without restriction. For `CommonResult`, `id` and `error` may carry server-assigned identifiers or error detail strings originating from the backend. For the array types, callers can replace or mutate the `arrayList` reference directly. While none of these classes perform storage operations themselves, their public mutability increases the risk that consuming code stores, logs, or leaks field values without awareness of content sensitivity.

No explicit data storage, SharedPreferences access, file writes, external storage access, or database operations are present in these files.

No issues found — MODE_WORLD_READABLE, allowBackup, external storage, or credential caching (out of scope for assigned files).

---

### 4. Input and Intent Handling

**FINDING — Low/Informational: No input validation on deserialized JSON fields.**

`CommonResult` (lines 27–35) extracts `id` and `error` directly from the JSON response using `jsonObject.getString()` with no validation of content, length, or character set. If the backend is compromised or the response is intercepted and modified, an attacker could supply arbitrarily long strings or strings containing special characters into these fields. Downstream code that logs, displays, or processes these values without sanitization could be affected (log injection, UI injection, or storage of unexpected content).

Similarly, `EquipmentStatsResultArray` and `EquipmentTypeResultArray` perform no validation on the length or content of the incoming `JSONArray` before iterating it (lines 25–28 in both files). A malformed or unexpectedly large JSON array would cause unbounded object allocation.

No exported components, WebView usage, deep link handlers, or implicit intents are present in these files.

No issues found — exported components, WebView, deep links, implicit intents (out of scope for assigned files).

---

### 5. Authentication and Session

No authentication tokens, credentials, session identifiers, or token lifecycle logic are present in these files.

No issues found — Authentication and Session (out of scope for assigned files).

---

### 6. Third-Party Libraries

No third-party library dependencies are declared or invoked in these files. Imports are limited to `org.json` (Android platform), `java.io.Serializable`, `java.util.ArrayList`, and `java.math.BigDecimal` (standard Java), plus internal package wildcard imports.

Note: `java.math.BigDecimal` is imported in all three files but is not used in any of the three files. This is an unused import (dead code / minor code hygiene issue, not a security finding).

No issues found — Third-Party Libraries (out of scope for assigned files).

---

### 7. Google Play and Android Platform

No manifest entries, SDK version declarations, permission declarations, or deprecated API usage are present in these files.

**FINDING — Low/Informational: Serializable used on data model classes without serialVersionUID.**

All three classes implement `java.io.Serializable` but declare no `serialVersionUID`:

- `CommonResult` (line 12)
- `EquipmentStatsResultArray` (line 12)
- `EquipmentTypeResultArray` (line 12)

Without an explicit `serialVersionUID`, Java computes one at compile time based on class structure. Any change to a field or method signature will silently change the UID, causing `InvalidClassException` on deserialization of previously serialized instances. More significantly from a security perspective, if these objects are serialized and passed across trust boundaries (via Intents as `Serializable` extras, for example), the absence of a fixed UID and absence of `readObject`/`writeObject` controls means deserialization behavior is entirely platform-controlled with no application-level validation or integrity check.

No issues found — targetSdkVersion, permission declarations, deprecated APIs, runtime permissions (out of scope for assigned files).

---

## Summary of Findings

| ID | File | Severity | Section | Description |
|----|------|----------|---------|-------------|
| APP26-01 | CommonResult.java, EquipmentStatsResultArray.java, EquipmentTypeResultArray.java | Low/Informational | Data Storage | All data fields are public; no accessor encapsulation. Deserialized data is directly mutable by any holding reference. |
| APP26-02 | CommonResult.java | Low/Informational | Input and Intent Handling | No validation of length or content of `id` and `error` fields extracted from JSON. Susceptible to oversized or malformed server responses being propagated unchecked. |
| APP26-03 | EquipmentStatsResultArray.java, EquipmentTypeResultArray.java | Low/Informational | Input and Intent Handling | No bounds check on incoming JSONArray length before allocation; unbounded object allocation possible from malformed response. |
| APP26-04 | CommonResult.java, EquipmentStatsResultArray.java, EquipmentTypeResultArray.java | Low/Informational | Google Play / Android Platform | `Serializable` implemented without `serialVersionUID`; no custom `readObject`/`writeObject` controls on deserialization. |
| APP26-05 | CommonResult.java, EquipmentStatsResultArray.java, EquipmentTypeResultArray.java | Informational | Code Hygiene | `java.math.BigDecimal` imported but unused in all three files. |

No Critical, High, or Medium findings identified in the assigned files.
