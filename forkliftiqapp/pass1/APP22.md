# Pass 1 Security Audit — APP22
**Agent:** APP22
**Date:** 2026-02-27
**Repo:** forkliftiqapp (Android/Java)

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

The checklist header states `Branch: main`. The actual branch is `master`. This is a discrepancy between the checklist and the repository. Branch confirmed as `master` — audit proceeds.

---

## Reading Evidence

### File 1: SaveServiceDurationParameter.java

**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveServiceDurationParameter.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveServiceDurationParameter`

**Superclass chain:** `SaveServiceDurationParameter` extends `WebServiceParameterPacket` extends `WebServicePacket` implements `Serializable`

**Public fields (all public, no encapsulation):**
- Line 14: `public int unit_id`
- Line 15: `public double acc_hours`
- Line 16: `public int last_serv`
- Line 17: `public String service_type`
- Line 18: `public int serv_duration`
- Line 19: `public int driver_id`

**Public methods:**
- Line 21: `public SaveServiceDurationParameter()` — no-arg constructor, no body

**Android components declared:** None (plain parameter DTO class)

---

### File 2: SaveServiceHoursParameter.java

**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveServiceHoursParameter.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveServiceHoursParameter`

**Superclass chain:** `SaveServiceHoursParameter` extends `WebServiceParameterPacket` extends `WebServicePacket` implements `Serializable`

**Public fields (all public, no encapsulation):**
- Line 14: `public int unit_id`
- Line 15: `public double acc_hours`
- Line 16: `public int last_serv`
- Line 17: `public String service_type`
- Line 18: `public int next_serv`
- Line 19: `public int driver_id`

**Public methods:**
- Line 21: `public SaveServiceHoursParameter()` — no-arg constructor, no body

**Android components declared:** None (plain parameter DTO class)

---

### File 3: SaveSessionsParameter.java

**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveSessionsParameter.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveSessionsParameter`

**Superclass chain:** `SaveSessionsParameter` extends `WebServiceParameterPacket` extends `WebServicePacket` implements `Serializable`

**Public fields (all public, no encapsulation):**
- Line 14: `public SaveSessionItem sessions` — contains: `id`, `driver_id`, `unit_id`, `start_time`, `finish_time`, `prestart_required`
- Line 15: `public SavePreStartItem results` — contains: `start_time`, `finish_time`, `comment`, `session_id`, `arrAnswers` (ArrayList of `AnswerItem`)

**Public methods:**
- Line 17: `public SaveSessionsParameter()` — no-arg constructor, no body

**Android components declared:** None (plain parameter DTO class)

---

## Findings by Checklist Section

### 1. Signing and Keystores

No issues found — Section 1. These are pure DTO/parameter classes with no involvement in signing configuration, keystore references, build scripts, or credential storage. No `.jks`, `.keystore`, or `.p12` references. No `gradle.properties` or `local.properties` references. No pipeline configuration.

---

### 2. Network Security

No issues found — Section 2. These classes contain no HTTP client code, no URL construction, no SSL/TLS configuration, no `TrustManager` implementations, and no `HostnameVerifier` overrides. They are data transfer objects that package fields prior to transmission by other layers; the transport mechanism is not present in these files. No hardcoded API endpoints or IP addresses are present.

---

### 3. Data Storage

**Finding — Low — Broad Serializability of Operator-Linked Data**

All three classes implement `java.io.Serializable` and carry fields that can be linked to specific operators and operational events:

- `SaveServiceDurationParameter`: `driver_id` (operator identity), `unit_id` (forklift identity), `acc_hours`, `last_serv`, `serv_duration`, `service_type`
- `SaveServiceHoursParameter`: `driver_id`, `unit_id`, `acc_hours`, `last_serv`, `next_serv`, `service_type`
- `SaveSessionsParameter` (via `SaveSessionItem`): `driver_id`, `unit_id`, `start_time`, `finish_time`, `prestart_required`; (via `SavePreStartItem`): `comment`, `session_id`, answers

Implementing `Serializable` means instances of these classes can be written to persistent storage via `ObjectOutputStream`, included in `Intent` extras (`putExtra`), or written to files by any caller. The classes themselves do not implement this storage — however, if any caller serializes them to disk or passes them via `Intent` extras unprotected, operator-linked telemetry and pre-start inspection data is exposed. This cannot be fully assessed without examining callers, but the design choice to make all fields `public` with no access control compounds the risk.

No credentials (passwords, tokens) are present in these specific classes.

---

### 4. Input and Intent Handling

**Finding — Low — No Input Validation on Public Fields**

All fields across all three classes are `public` with no access modifiers, getters/setters, or validation. There is no range checking, null guarding at the field level, or type validation enforced by the class contract. Examples:

- `SaveServiceDurationParameter.serv_duration` (int) and `acc_hours` (double) accept any value including negative numbers, which would be semantically invalid for service duration and accumulated hours.
- `SaveServiceHoursParameter.next_serv` (int) and `last_serv` (int) accept any value with no bounds.
- `SaveSessionsParameter.sessions` and `results` are typed references that can be null with no null-safety enforced.
- `SavePreStartItem.comment` (String, reachable via `SaveSessionsParameter.results`) is an unvalidated free-text field that passes through to the backend; if the backend performs any dynamic query construction or template rendering without sanitisation, this is a potential injection vector. The risk cannot be fully characterised at the DTO layer alone but warrants review of how `comment` is used server-side.

These classes are parameter objects passed to a web service layer. If the serialised output is transmitted to `forkliftiqws` without server-side validation, malformed values could cause backend issues. Validation at the point of population (UI/controller layer) should be confirmed in a subsequent audit pass.

No issues found — Section 4 (Intent handling, WebView, deep links): these classes are not Android components, are not exported, and do not interact with intents, WebViews, or deep link handlers.

---

### 5. Authentication and Session

**Finding — Informational — `driver_id` Carried in Unprotected DTOs**

`driver_id` appears in `SaveServiceDurationParameter` (line 19), `SaveServiceHoursParameter` (line 19), and `SaveSessionItem` (line 15, referenced by `SaveSessionsParameter`). This field represents the operator identity associated with the web service call. It is a plain `public int` with no association to an authentication token or session credential within these classes.

Whether the web service layer enforces server-side validation that the authenticated session corresponds to the supplied `driver_id` cannot be determined from these files. If the backend trusts the `driver_id` value as sent by the client without cross-referencing against the authenticated session, an operator could potentially substitute another operator's `driver_id` and submit session or service records under a different identity. This is an architectural concern to carry forward to the backend audit.

No credentials or tokens are stored in these classes. No token expiry handling is present — not applicable at the DTO layer.

---

### 6. Third-Party Libraries

No issues found — Section 6. These files import only `org.json` (part of the Android platform) and `java.io`, `java.util`, `java.math` (Java standard library). No third-party library dependencies are introduced in these classes.

---

### 7. Google Play and Android Platform

No issues found — Section 7. These classes are plain Java data transfer objects with no Android framework usage, no API level dependencies, no permission usage, no deprecated API usage (`AsyncTask`, `startActivityForResult`, etc.), and no Android component lifecycle involvement.

---

## Summary Table

| # | Severity | Section | File(s) | Description |
|---|----------|---------|---------|-------------|
| 1 | Low | 3 — Data Storage | All three | All fields public; classes are `Serializable` carrying operator-linked telemetry (driver_id, unit_id, session times). Any caller can serialise to unprotected storage. |
| 2 | Low | 4 — Input Handling | All three | No input validation on any field. Negative/zero values accepted for duration and hours fields. `comment` (reachable via `SaveSessionsParameter`) is a free-text string with no sanitisation at DTO layer. |
| 3 | Informational | 5 — Authentication | All three | `driver_id` is a plain int in the DTO with no binding to the authenticated session. Backend must be verified to cross-check driver_id against the session credential. |
| — | Discrepancy | Branch | N/A | Checklist states `Branch: main`; actual branch is `master`. |

---

## Files Reviewed

1. `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveServiceDurationParameter.java`
2. `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveServiceHoursParameter.java`
3. `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveSessionsParameter.java`

**Supporting files read for context (not assigned):**
- `WebServiceParameterPacket.java` — superclass
- `SaveSessionItem.java` — field type in `SaveSessionsParameter`
- `SavePreStartItem.java` — field type in `SaveSessionsParameter`
