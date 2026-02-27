# Pass 1 Security Audit — APP25
**Agent ID:** APP25
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Branch Verification

- Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
- Result: `master`
- Checklist specifies branch `main`; actual branch is `master`. Discrepancy recorded. Branch is `master` — audit proceeds.

---

## Assigned File

`/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/UserRegisterParameter.java`

---

## Reading Evidence

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.UserRegisterParameter`

**Superclass:** `WebServiceParameterPacket` (implements `Serializable`)

**Fields (all public):**

| Line | Type    | Name          |
|------|---------|---------------|
| 14   | String  | first_name    |
| 15   | String  | last_name     |
| 16   | String  | email         |
| 17   | String  | password      |
| 18   | String  | phone         |
| 19   | boolean | contactperson |

**Public methods:**

| Line | Signature                   |
|------|-----------------------------|
| 21   | `UserRegisterParameter()`   |

No other methods declared in this class. Methods inherited from `WebServiceParameterPacket` are not visible in this file.

**Activities / Services / Receivers / Providers:** None declared in this file.

**Permissions:** None declared in this file.

---

## Checklist Review

### 1. Signing and Keystores
No issues found — this file is a data parameter class with no signing configuration, keystore references, or credential properties.

### 2. Network Security
No issues found — this file contains no HTTP client configuration, URL construction, or network calls. No hardcoded endpoints or IP addresses.

### 3. Data Storage

**FINDING — High: Password stored as a plain, public `String` field**

- File: `UserRegisterParameter.java`, line 17
- Field: `public String password;`

The `password` field is:
1. Typed as `String`. In Java, `String` objects are immutable and interned; once created they remain in the heap until garbage collected and cannot be explicitly zeroed. The value may persist in memory longer than necessary and can appear in heap dumps.
2. Declared `public` with no access control. Any class that holds a reference to a `UserRegisterParameter` instance can read or assign the plain-text password directly without going through a getter or any protective logic.
3. The class implements `Serializable`. A serialized `UserRegisterParameter` object containing a non-null `password` will write the plain-text password to the serialization stream (file, parcel, or network) unless the field is marked `transient`. The field is not marked `transient`.

Recommended remediation (for developer reference): use a `char[]` instead of `String` for the password field so it can be explicitly zeroed after use; declare it `private`; mark it `transient` to exclude it from Java serialization; and ensure it is cleared from memory immediately after the network call completes.

### 4. Input and Intent Handling
No issues found — this file declares no Activities, BroadcastReceivers, Services, or intent filters. No WebView or deep link handling is present.

### 5. Authentication and Session

**FINDING — High: Password transmitted in a plain-text `String` field of a Serializable parameter object**

This relates to the finding in section 3. The class is used as a request parameter packet sent to `forkliftiqws` during user registration. If serialized or if the `WebServiceParameterPacket` superclass converts fields to JSON via reflection or field enumeration, the plain-text password will be present in the transmission payload without any indication that it was masked or hashed prior to transmission. Whether the password is hashed before being placed in this field cannot be determined from this file alone — this must be verified in the caller(s) that instantiate and populate `UserRegisterParameter`.

Note: The field `email` is also public and plain-text, constituting PII within the same object. If this object is logged, serialized to disk, or retained in memory, email address exposure is an additional concern.

### 6. Third-Party Libraries
No issues found — this file imports only `org.json`, `java.io.Serializable`, `java.util.ArrayList`, and `java.math.BigDecimal` from the standard libraries, plus intra-project imports. No third-party dependencies are introduced here.

### 7. Google Play and Android Platform
No issues found — this file uses no deprecated Android APIs, requests no permissions, and declares no Android platform components.

---

## Summary of Findings

| # | Severity | Section          | Description                                                                                      | File                         | Line |
|---|----------|------------------|--------------------------------------------------------------------------------------------------|------------------------------|------|
| 1 | High     | Data Storage / Authentication | `password` field is a public, non-transient, plain `String` in a `Serializable` class. Passwords stored as `String` cannot be zeroed from memory; `public` access removes encapsulation; `Serializable` without `transient` causes the plain-text password to be included in any serialization stream. | `UserRegisterParameter.java` | 17   |
| 2 | Informational | Authentication | Cannot confirm from this file alone whether the password is hashed by the caller before being assigned to this field. Caller code must be reviewed to determine whether the password travels in plain text to `forkliftiqws`. | `UserRegisterParameter.java` | 17   |
