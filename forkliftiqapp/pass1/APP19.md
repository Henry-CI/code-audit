# Pass 1 Security Audit — APP19
**App:** forkliftiqapp (Android/Java)
**Agent ID:** APP19
**Date:** 2026-02-27
**Output:** audit/2026-02-27-01/pass1/APP19.md

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist specifies `Branch: main`, but the actual branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Checklist Confirmed Read

All seven checklist sections were read in full:
1. Signing and Keystores
2. Network Security
3. Data Storage
4. Input and Intent Handling
5. Authentication and Session
6. Third-Party Libraries
7. Google Play and Android Platform

---

## Step 3 — Assigned Files Read in Full

All three files read completely:
1. `AddEquipmentParameter.java`
2. `GetTokenParameter.java`
3. `ImpactParameter.java`

---

## Step 4 — Reading Evidence

### File 1: AddEquipmentParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.AddEquipmentParameter`

**Superclass:** `WebServiceParameterPacket`
**Interfaces implemented:** `Serializable`

**Public fields (all public, no private/protected):**

| Line | Field | Type |
|------|-------|------|
| 14 | `name` | `String` |
| 15 | `manu_id` | `int` |
| 16 | `type_id` | `int` |
| 17 | `fuel_type_id` | `int` |
| 18 | `serial_no` | `String` |
| 19 | `mac_address` | `String` |
| 20 | `comp_id` | `int` |

**Public methods:**

| Line | Signature |
|------|-----------|
| 22–23 | `public AddEquipmentParameter()` — default constructor, empty body |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

### File 2: GetTokenParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.GetTokenParameter`

**Superclass:** `WebServiceParameterPacket`
**Interfaces implemented:** `Serializable`

**Public fields (all public, no private/protected):**

| Line | Field | Type |
|------|-------|------|
| 14 | `grant_type` | `String` |
| 15 | `client_id` | `String` |
| 16 | `client_secret` | `String` |
| 17 | `username` | `String` |
| 18 | `password` | `String` |

**Public methods:**

| Line | Signature |
|------|-----------|
| 20–21 | `public GetTokenParameter()` — default constructor, empty body |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

### File 3: ImpactParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.ImpactParameter`

**Superclass:** `WebServiceParameterPacket`
**Interfaces implemented:** `Serializable`

**Public fields (all public, no private/protected):**

| Line | Field | Type |
|------|-------|------|
| 14 | `injury_type` | `String` |
| 15 | `description` | `String` |
| 16 | `witness` | `String` |
| 17 | `report_time` | `String` |
| 18 | `event_time` | `String` |
| 19 | `injury` | `boolean` |
| 20 | `near_miss` | `boolean` |
| 21 | `incident` | `boolean` |
| 22 | `location` | `String` |
| 23 | `driver_id` | `int` |
| 24 | `unit_id` | `int` |

**Public methods:**

| Line | Signature |
|------|-----------|
| 26–27 | `public ImpactParameter()` — default constructor, empty body |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No signing configuration, keystore files, Gradle build scripts, or pipeline files are present in the assigned files. These files contain no signing-related content.

No issues found — Section 1 (Signing and Keystores)

---

### Section 2 — Network Security

No HTTP client configuration, URL strings, `TrustManager`, `HostnameVerifier`, or SSL-related code is present in the assigned files.

No issues found — Section 2 (Network Security)

---

### Section 3 — Data Storage

No `SharedPreferences` usage, file I/O, SQLite operations, or external storage access is present in the assigned files.

No issues found — Section 3 (Data Storage)

---

### Section 4 — Input and Intent Handling

No Intent construction, WebView usage, or deep link handlers are present in the assigned files.

No issues found — Section 4 (Input and Intent Handling)

---

### Section 5 — Authentication and Session

**FINDING — Medium: Public credential fields in GetTokenParameter (GetTokenParameter.java, lines 14–18)**

`GetTokenParameter` carries `client_id`, `client_secret`, `username`, and `password` as raw `public String` fields with no access control. All five authentication fields are fully public. This class implements `Serializable`, which means any code that can obtain a reference to an instance — including via `Intent` extras or inter-process mechanisms — can read these values directly without any accessor restriction. In isolation this is a design-level issue; the severity of exploitation depends on how callers populate and pass instances of this class.

Specific concerns:
- `client_secret` (line 16): OAuth client secret exposed as a public plain-text field. If an instance is serialised and passed across a process boundary or logged, the secret is fully exposed.
- `password` (line 18): Operator password carried as a public plain-text field. No indication of hashing or masking.
- `username` (line 17): Operator username carried as a public plain-text field.

**Recommendation:** Restrict all credential fields to `private`. Provide controlled accessors where necessary. Avoid holding the password in a String beyond the duration of the network call. Consider zeroing or clearing the field after use.

---

### Section 5 (continued) — Serializable credential object

**FINDING — Low/Informational: GetTokenParameter is Serializable and carries credentials**

Because `GetTokenParameter implements Serializable`, the JVM may serialise all non-transient fields to disk or across process boundaries (e.g., when passed in an `Intent` that is then received by another component). `client_secret`, `username`, and `password` are not marked `transient`. If the serialised form is written to an Intent's `Parcelable`/Serializable bundle and that bundle is written to disk (e.g., saved state), credentials land in plaintext storage.

**Recommendation:** Mark credential fields `transient` or migrate to `Parcelable` with explicit field control. Evaluate whether this object needs to be serialisable at all.

---

### Section 5 (continued) — ImpactParameter PII exposure

**FINDING — Low/Informational: ImpactParameter carries operator PII in public fields (ImpactParameter.java, lines 14–24)**

`ImpactParameter` holds incident/impact report data including `injury_type`, `description`, `witness`, `location`, `driver_id`, and `unit_id` as `public` fields, all serialisable. If an instance is logged, serialised to storage, or passed via an improperly secured Intent, operator PII and sensitive incident data are exposed without access control.

**Recommendation:** Restrict fields to `private`. Evaluate whether `Serializable` is required or whether field-level `transient` annotations are appropriate for sensitive string fields.

---

### Section 5 (continued) — AddEquipmentParameter MAC address exposure

**FINDING — Low/Informational: AddEquipmentParameter exposes mac_address as a public field (AddEquipmentParameter.java, line 19)**

`mac_address` is a device or equipment identifier held as a `public String`. MAC addresses are classified as device identifiers under privacy frameworks (GDPR, Australian Privacy Act). Exposure via serialisation, logging, or accessible public fields is a privacy risk.

**Recommendation:** Restrict to `private` with a controlled accessor.

---

### Section 6 — Third-Party Libraries

No `build.gradle` dependency declarations or library imports are present in the assigned files beyond standard `org.json` and `java.*` platform APIs.

No issues found — Section 6 (Third-Party Libraries)

---

### Section 7 — Google Play and Android Platform

No `targetSdkVersion`, `minSdkVersion`, permission declarations, or deprecated API usage is present in the assigned files.

No issues found — Section 7 (Google Play and Android Platform)

---

## Summary of Findings

| ID | File | Section | Severity | Title |
|----|------|---------|----------|-------|
| APP19-01 | GetTokenParameter.java:14–18 | 5 — Authentication and Session | Medium | Credential fields (`client_secret`, `password`, `username`) declared `public` with no access control |
| APP19-02 | GetTokenParameter.java:12 | 5 — Authentication and Session | Low | `GetTokenParameter` implements `Serializable` without marking credential fields `transient` |
| APP19-03 | ImpactParameter.java:14–24 | 5 — Authentication and Session / Data Storage | Low | Operator PII and incident data in public serialisable fields |
| APP19-04 | AddEquipmentParameter.java:19 | 3 — Data Storage | Low | `mac_address` device identifier exposed as `public` field in serialisable class |

---

## Notes for Subsequent Passes

- The parent class `WebServiceParameterPacket` (not in assigned files) should be reviewed. All three parameter classes extend it; if it defines serialisation hooks (`writeObject`/`readObject`) or logging, the credential exposure risk in APP19-01/APP19-02 may be elevated.
- Call sites that instantiate `GetTokenParameter` and assign `password` should be audited to confirm that field values are not logged or persisted beyond the network call lifetime.
- All three classes use broad wildcard imports (`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` and `.results.*`) but import symbols not visibly used in the files (e.g., `JSONObject`, `JSONArray`, `ArrayList`, `BigDecimal`). This may indicate template boilerplate or previously removed code; no direct security impact, but worth noting for code hygiene.
