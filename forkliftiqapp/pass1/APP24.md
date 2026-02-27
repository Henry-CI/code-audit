# Pass 1 Security Audit — APP24
**Agent ID:** APP24
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** Checklist specifies `Branch: main`. Actual branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SessionStartParameter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SetEmailsParameter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/UpdateUserParameter.java`

---

## Step 3 — Reading Evidence

### File 1: SessionStartParameter.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SessionStartParameter`

**Superclass chain:** `SessionStartParameter` extends `WebServiceParameterPacket` extends `WebServicePacket` (implements `Serializable` at each level)

**Public methods:**

| Line | Signature |
|------|-----------|
| 13 | `SessionStartParameter()` — default no-arg constructor |

**Public fields:**

| Line | Field |
|------|-------|
| 9 | `public int driver_id` |
| 10 | `public int unit_id` |
| 11 | `public String start_time` |

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None — this is a plain DTO class.

---

### File 2: SetEmailsParameter.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SetEmailsParameter`

**Superclass chain:** `SetEmailsParameter` extends `WebServiceParameterPacket` extends `WebServicePacket` (implements `Serializable` at each level)

**Public methods:**

| Line | Signature |
|------|-----------|
| 20 | `SetEmailsParameter()` — default no-arg constructor |

**Public fields:**

| Line | Field |
|------|-------|
| 14 | `public int driver_id` |
| 15 | `public String email_addr1` |
| 16 | `public String email_addr2` |
| 17 | `public String email_addr3` |
| 18 | `public String email_addr4` |

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None — this is a plain DTO class.

---

### File 3: UpdateUserParameter.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.UpdateUserParameter`

**Superclass chain:** `UpdateUserParameter` extends `WebServiceParameterPacket` extends `WebServicePacket` (implements `Serializable` at each level)

**Public methods:**

| Line | Signature |
|------|-----------|
| 13 | `UpdateUserParameter(int id, String firstName, String lastName, String complianceDate)` — parameterised constructor |

**Public fields:**

| Line | Field |
|------|-------|
| 8 | `public int id` |
| 9 | `public String first_name` |
| 10 | `public String last_name` |
| 11 | `public String compliance_date` |

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None — this is a plain DTO class.

---

### Supporting File Read: WebServiceParameterPacket.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServiceParameterPacket`

**Public methods:**

| Line | Signature |
|------|-----------|
| 15 | `WebServiceParameterPacket()` — default no-arg constructor |
| 18 | `WebServiceParameterPacket(JSONObject jsonObject) throws JSONException` — JSON deserialisation constructor; delegates to `super(jsonObject)`. The `if (jsonObject != null)` block is empty — no additional fields are parsed at this level. |

---

## Step 4 — Security Review by Checklist Section

### Section 1 — Signing and Keystores

No signing configurations, keystore references, passwords, or credential values are present in any of the three files. These are DTO/parameter-packet classes only.

**No issues found — Section 1.**

---

### Section 2 — Network Security

All three classes are data-transfer objects (DTOs) used to package parameters before dispatch to the backend (`forkliftiqws`). They contain no HTTP client code, no URLs, no IP addresses, no TrustManager implementations, and no SSL/TLS configuration.

**Finding — Section 2 (Low / Informational):** The fields in these DTOs reveal the shape of data transmitted over the network. All three classes implement `java.io.Serializable`. If the serialised form of these objects is ever transmitted directly (e.g. via Java object serialisation rather than JSON), that transport path must use HTTPS. The classes themselves do not control transport; the transport mechanism is determined by callers. Callers are out of scope for this file set but should be reviewed in a subsequent pass.

No hardcoded URLs, IP addresses, or plaintext-traffic settings found within these files.

**No additional issues found — Section 2.**

---

### Section 3 — Data Storage

None of the three files perform any storage operations (no SharedPreferences, no file I/O, no SQLite, no external storage access).

**Finding — Section 3 (Medium):** `SetEmailsParameter` carries up to four email addresses (`email_addr1` through `email_addr4`) associated with a `driver_id`. All four email fields are `public` with no access controls. PII (email addresses) in a publicly accessible field on a `Serializable` object can be inadvertently exposed if the object is written to a log, persisted to storage, or included in a crash report without sanitisation. The impact depends on how callers handle the populated object; callers are out of scope here but should be audited.

**Finding — Section 3 (Low):** `UpdateUserParameter` carries `first_name` and `last_name` (PII) as `public` fields with no access controls. Same exposure risk as noted above for `SetEmailsParameter`.

**Finding — Section 3 (Low):** `SessionStartParameter` carries `driver_id` and `unit_id` as `public int` fields and `start_time` as a `public String`. The combination of driver identity, unit identity, and session start timestamp constitutes operational data that, if exposed in logs or crash reports, could reveal forklift operator activity patterns.

**No issues found with storage operations directly in these files — Section 3.**

---

### Section 4 — Input and Intent Handling

None of the three files are Android components (no Activity, Service, BroadcastReceiver, ContentProvider, or WebView). No intent filters, deep link handlers, or exported component declarations are present.

There is no input validation in any of the three classes. All fields are bare `public` members; no type checking, length constraints, format validation, or null guards are applied at the DTO level. Validation responsibility falls entirely on callers. If callers do not validate before populating these objects, malformed data (e.g. excessively long strings in `email_addr1`–`email_addr4`, or malformed date strings in `compliance_date` and `start_time`) will be passed directly to the backend.

**Finding — Section 4 (Low):** No input validation is enforced at the DTO layer for any field across all three classes. Specifically:
- `SetEmailsParameter`: `email_addr1` through `email_addr4` are unbounded `String` fields with no format enforcement. A valid email address format is not checked.
- `UpdateUserParameter`: `compliance_date` is an unbounded `String` with no date format enforcement.
- `SessionStartParameter`: `start_time` is an unbounded `String` with no date/time format enforcement.

**No issues found — Section 4 (component export, intent, WebView).**

---

### Section 5 — Authentication and Session

`SessionStartParameter` is the most authentication-relevant file in this set. It carries `driver_id`, `unit_id`, and `start_time` — the parameters used to initiate an operator session. Observations:

- There is no authentication token or credential field within `SessionStartParameter`. The assumption is that authentication context (token/session) is managed at the `WebServicePacket` or `WebServiceParameterPacket` superclass level, or is injected by the HTTP client layer. The superclass `WebServiceParameterPacket` was read in full; its constructor delegates to `super(jsonObject)` with an empty body — no token or auth header is appended at that level either. This means authentication tokens, if any, are added outside the parameter packet hierarchy.
- There is no logout or session-clearing logic in any of the three files; they are inert DTOs.
- Token expiry handling is not present in these files.

**Finding — Section 5 (Informational):** `SessionStartParameter` does not include any authentication credential or token field. Whether authentication context is correctly appended at a higher layer (e.g. HTTP interceptor) cannot be determined from these files alone. The caller chain should be audited.

**No issues found — Section 5 (within scope of these files).**

---

### Section 6 — Third-Party Libraries

No third-party library dependencies are declared or used within these three files. The only imports present are:
- `java.io.Serializable` (JDK standard library)
- `org.json.JSONObject`, `org.json.JSONArray`, `java.math.BigDecimal`, `java.util.ArrayList` (JDK/Android SDK standard libraries, present in `SetEmailsParameter` as unused imports — see finding below)
- Internal package imports (`au.com.collectiveintelligence.fleetiq360.*`)

**Finding — Section 6 (Low / Code Quality):** `SetEmailsParameter.java` imports `org.json.JSONException`, `org.json.JSONObject`, `org.json.JSONArray`, `java.util.ArrayList`, and `java.math.BigDecimal` (lines 3–8) but uses none of them. These appear to be copy-paste residue from `WebServiceParameterPacket.java`. Unused imports are not a direct security issue but indicate copy-paste development patterns that can mask real dependencies or confuse future reviewers.

**No issues found — Section 6 (CVEs, abandoned libraries, ProGuard).**

---

### Section 7 — Google Play and Android Platform

No `build.gradle`, `AndroidManifest.xml`, or platform API calls are present in these files. No deprecated APIs (`AsyncTask`, `startActivityForResult`, etc.) are used. No permission declarations or runtime permission requests are made.

**No issues found — Section 7.**

---

## Step 5 — Summary of Findings

| ID | File | Section | Severity | Finding |
|----|------|---------|----------|---------|
| APP24-01 | `SetEmailsParameter.java` | 3 — Data Storage | Medium | PII (up to four email addresses) stored in `public` fields on a `Serializable` object. No access control. Risk of inadvertent exposure in logs or crash reports if callers do not sanitise. |
| APP24-02 | `UpdateUserParameter.java` | 3 — Data Storage | Low | PII (`first_name`, `last_name`) in `public` fields on a `Serializable` object. No access control. |
| APP24-03 | `SessionStartParameter.java` | 3 — Data Storage | Low | Operational data (`driver_id`, `unit_id`, `start_time`) in `public` fields. Combination constitutes operator activity data. |
| APP24-04 | All three files | 4 — Input Handling | Low | No input validation at DTO layer. String fields (`email_addr1`–`4`, `compliance_date`, `start_time`) are unbounded and unformatted. Validation must occur in callers. |
| APP24-05 | `SetEmailsParameter.java` | 6 — Libraries | Low / Code Quality | Five unused imports (lines 3–8) indicate copy-paste development pattern. Not a direct security issue. |
| APP24-06 | `SessionStartParameter.java` | 5 — Authentication | Informational | No authentication credential/token field present. Whether auth context is added upstream cannot be confirmed from these files; caller chain requires audit. |

---

## Step 6 — Discrepancy Log

| Item | Checklist Value | Actual Value |
|------|----------------|--------------|
| Branch | `main` | `master` |

---

*Report written by agent APP24. Scope limited to the three assigned parameter DTO files and their immediate superclass. Findings marked Informational and Low require cross-file context to assess full impact; caller-chain audit is recommended in a subsequent pass.*
