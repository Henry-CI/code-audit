# Pass 1 Security Audit — APP17
**App:** forkliftiqapp (Android/Java)
**Agent ID:** APP17
**Date:** 2026-02-27
**Branch audited:** master

---

## STEP 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`, but the actual current branch is `master`. Audit proceeds on `master` as instructed.

---

## STEP 2 — Checklist

Checklist read in full from: `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`

Sections covered:
1. Signing and Keystores
2. Network Security
3. Data Storage
4. Input and Intent Handling
5. Authentication and Session
6. Third-Party Libraries
7. Google Play and Android Platform

---

## STEP 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/TrainingItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/WebServicePacket.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/WebServiceParameterPacket.java`

All three files read in full.

---

## STEP 4 — Reading Evidence

### File 1: TrainingItem.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.TrainingItem`

**Implements:** `java.io.Serializable`

**Fields (all public, no access modifiers):**

| Line | Type | Name |
|------|------|------|
| 10 | `int` | `manufacture_id` |
| 11 | `int` | `type_id` |
| 12 | `int` | `fuel_type_id` |
| 13 | `String` | `training_date` |
| 14 | `String` | `expiration_date` |

**Public methods:**

| Line | Signature |
|------|-----------|
| 16 | `public TrainingItem()` |
| 19 | `public TrainingItem(JSONObject jsonObject) throws JSONException` |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders.**

---

### File 2: WebServicePacket.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServicePacket`

**Implements:** `java.io.Serializable`

**Fields:** None.

**Public methods:**

| Line | Signature |
|------|-----------|
| 9 | `public WebServicePacket()` |
| 12 | `public WebServicePacket(JSONObject jsonObject) throws JSONException` |

**Notes:** The `JSONObject` constructor body (lines 13–17) receives a `jsonObject` parameter but the inner block is empty — the object is checked for null but no fields are parsed from it.

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders.**

---

### File 3: WebServiceParameterPacket.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServiceParameterPacket`

**Extends:** `WebServicePacket`
**Implements:** `java.io.Serializable`

**Imports (wildcard):**
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10)
- `org.json.JSONArray` (line 6)
- `java.util.ArrayList` (line 7)
- `java.math.BigDecimal` (line 8)

**Fields:** None.

**Public methods:**

| Line | Signature |
|------|-----------|
| 15 | `public WebServiceParameterPacket()` |
| 18 | `public WebServiceParameterPacket(JSONObject jsonObject) throws JSONException` |

**Notes:** Like `WebServicePacket`, the `JSONObject` constructor delegates to `super(jsonObject)` but the local block (lines 22–24) is empty — no fields are parsed.

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders.**

---

## STEP 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found — Section 1. These files are data model / packet classes with no signing, keystore, or credential references.

---

### Section 2 — Network Security

**Finding NS-01 — Severity: Low / Informational**

**File:** `TrainingItem.java`
**Lines:** 10–14

All five fields of `TrainingItem` are `public` with no access control. The class is deserialized directly from a `JSONObject` (i.e., from the network response of forkliftiqws). There is no input validation on any parsed value:

- `training_date` (line 41) and `expiration_date` (line 45) are assigned raw from `jsonObject.getString(...)` without any format validation. A malicious or malformed server response could supply arbitrary string content that is then stored and potentially rendered or processed downstream without sanitisation.
- `manufacture_id`, `type_id`, and `fuel_type_id` use `getInt()` which will throw a `JSONException` on non-integer input — this provides implicit type safety, but exceptions propagate to the caller with no observed sanitisation boundary in these files.

This is low severity in isolation, but contributes to a broader lack of defensive parsing from network data.

No hardcoded URLs, endpoints, or IP addresses are present in any of the three files.

---

### Section 3 — Data Storage

**Finding DS-01 — Severity: Low / Informational**

**File:** `TrainingItem.java`
**Lines:** 8, 10–14

`TrainingItem` implements `java.io.Serializable`. All five fields are `public` with no `transient` modifier. This means:

- If an instance of `TrainingItem` is serialized to disk (via `ObjectOutputStream`, intent extras, or Android's `Parcelable`-fallback mechanisms), all fields including `training_date` and `expiration_date` will be written in plaintext.
- Operator training record data (training and expiration dates tied to forklift type/manufacturer) is potentially sensitive compliance information. If serialized to unprotected storage, it is accessible to any app with appropriate storage permissions.

No credentials, session tokens, or explicit SharedPreferences usage are present in these files.

---

### Section 4 — Input and Intent Handling

**Finding IH-01 — Severity: Low / Informational**

**File:** `TrainingItem.java`
**Lines:** 39–47

The `training_date` and `expiration_date` string fields are deserialized from network JSON with no format or length validation. If these values are later passed in an Intent (e.g., as extras) or used to populate UI elements, unvalidated content from the network response flows through to downstream consumers. This is a data-flow concern that depends on how callers use the object, but the absence of any defensive parsing at the deserialization boundary is noted.

No exported components, WebView usage, or deep link handling are present in these files.

---

### Section 5 — Authentication and Session

No issues found — Section 5. None of the three files handle authentication tokens, credentials, session state, login, logout, or operator switching. These are pure data model/packet classes.

---

### Section 6 — Third-Party Libraries

**Finding TL-01 — Severity: Low / Informational**

**File:** `WebServiceParameterPacket.java`
**Lines:** 6–10

`WebServiceParameterPacket` imports `org.json.JSONArray`, `java.util.ArrayList`, and `java.math.BigDecimal`, plus two wildcard package imports (`webserviceclasses.*` and `webserviceclasses.results.*`), none of which are used anywhere in the class body. The wildcard imports in particular (`import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`) pull in all classes from those packages without specificity. This is a code hygiene issue and suggests this class may be a scaffold generated for future use, with unused imports never cleaned up. While not a direct security vulnerability, dead/unused wildcard imports obscure the class's actual dependencies and complicate static analysis.

No third-party dependency versions are declared in these files (versions are a build.gradle concern).

---

### Section 7 — Google Play and Android Platform

**Finding GP-01 — Severity: Low / Informational**

**File:** `WebServicePacket.java` (lines 12–17) and `WebServiceParameterPacket.java` (lines 18–25)

Both the base class `WebServicePacket` and its subclass `WebServiceParameterPacket` declare a `JSONObject`-accepting constructor that contains an empty implementation block. The constructors accept a `JSONObject` parameter (i.e., data from the network layer), check it for null, but perform no actual deserialization. This suggests dead or unfinished code — scaffolding that was never implemented. Incomplete code paths can mask errors at runtime: callers that pass a populated `JSONObject` expecting it to be parsed will silently receive a default-constructed object with no indication of failure (no exception, no error return). This is a code quality / correctness concern with indirect security implications (silent data loss from API responses could mask server-side errors or tampering).

No deprecated Android APIs, SDK version concerns, or permission declarations are present in these files.

---

## Summary Table

| ID | File | Line(s) | Severity | Section | Description |
|----|------|---------|----------|---------|-------------|
| NS-01 | TrainingItem.java | 39–47 | Low / Info | 2 — Network Security | No input validation on string fields parsed from network JSON |
| DS-01 | TrainingItem.java | 8, 10–14 | Low / Info | 3 — Data Storage | All fields public and non-transient on a Serializable class; training record data could be serialized to unprotected storage |
| IH-01 | TrainingItem.java | 39–47 | Low / Info | 4 — Input Handling | Unvalidated string fields from network response may flow to downstream consumers via Intent or UI |
| TL-01 | WebServiceParameterPacket.java | 6–10 | Low / Info | 6 — Third-Party Libraries | Unused wildcard imports and unused imports obscure actual dependencies |
| GP-01 | WebServicePacket.java, WebServiceParameterPacket.java | 12–17, 18–25 | Low / Info | 7 — Platform | Empty JSON constructor bodies — silent no-op deserialization; dead/unfinished scaffold code |

**No Critical or High severity findings in the assigned files.**
**No Medium severity findings in the assigned files.**

---

*End of report — Agent APP17*
