# Pass 1 Security Audit — APP20
**Agent ID:** APP20
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

DISCREPANCY: The checklist states `Branch: main`. The actual branch is `master`. Audit proceeds on `master`.

---

## Reading Evidence

### File 1: JoinCompanyParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.JoinCompanyParameter`

**Inheritance chain:**
`JoinCompanyParameter` → `WebServiceParameterPacket` → `WebServicePacket` → (implements `Serializable`)

**Fields:**
- `public int driver_id` (line 14)
- `public int comp_id` (line 15)

**Public methods:**
- `JoinCompanyParameter()` — default constructor, line 17 (no-op body)

**No activities, fragments, services, broadcast receivers, or content providers declared.**

---

### File 2: LoginParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.LoginParameter`

**Inheritance chain:**
`LoginParameter` → `WebServiceParameterPacket` → `WebServicePacket` → (implements `Serializable`)

**Fields:**
- `public String email` (line 14)
- `public String password` (line 15)

**Public methods:**
- `LoginParameter()` — default constructor, line 17 (no-op body)

**No activities, fragments, services, broadcast receivers, or content providers declared.**

---

### File 3: ResetPasswordParameter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.ResetPasswordParameter`

**Inheritance chain:**
`ResetPasswordParameter` → `WebServiceParameterPacket` → `WebServicePacket` → (implements `Serializable`)

**Fields:**
- `public String email` (line 14)

**Public methods:**
- `ResetPasswordParameter()` — default constructor, line 17 (no-op body)

**No activities, fragments, services, broadcast receivers, or content providers declared.**

---

### Supporting class evidence (read to assess scope of findings)

**WebServiceParameterPacket.java**
- Class: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServiceParameterPacket`
- Extends `WebServicePacket`, implements `Serializable`
- Constructor `WebServiceParameterPacket(JSONObject)` at line 18 — delegates to `super(jsonObject)`, then performs no additional field parsing (empty `if` block).

**WebServicePacket.java**
- Class: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.WebServicePacket`
- Implements `Serializable`
- Constructor `WebServicePacket(JSONObject)` at line 12 — null-guard only, no field parsing.

---

## Findings by Checklist Section

### 1. Signing and Keystores

No signing configuration, keystore files, gradle files, or pipeline files are within the assigned file set. No issues found in assigned files — Section 1.

---

### 2. Network Security

No network client code, URL construction, or HTTP configuration is present in any of the three assigned files. No issues found in assigned files — Section 2.

---

### 3. Data Storage

**FINDING — APP20-F01 — Medium**

**File:** `LoginParameter.java`, line 15
**Description:** The `password` field is declared as `public String password`. Java `String` objects are immutable and interned in the JVM string pool; once assigned, the value cannot be zeroed out by the application. The class implements `Serializable` through its full inheritance chain (`LoginParameter` → `WebServiceParameterPacket` → `WebServicePacket`). Because no `serialVersionUID` is declared and no `writeObject`/`readObject` override excludes the password field, a serialized `LoginParameter` instance will include the plaintext password in its byte stream. If this object is ever serialized to disk, passed via an Intent `Bundle` (which uses Java serialization internally for `Serializable` objects), written to a log, or cached as part of an activity saved-instance-state, the plaintext password is exposed.

**Specific risks:**
- The field is `public`, so any class in the process that holds a reference to a `LoginParameter` can read the password directly with no accessor indirection.
- Implementing `Serializable` without marking `password` as `transient` means any serialization path (file, Intent, ObjectOutputStream) will emit the plaintext credential.
- `String` cannot be wiped from memory; the value persists in the string pool until GC collects it, potentially surviving the authentication call lifetime.

**Recommendation (for record):** Use a `char[]` field for the password, mark it `transient`, and zero the array after use. The field should not be `public`. If serialization of the packet is required, implement `writeObject` to exclude the credential.

---

**FINDING — APP20-F02 — Low**

**File:** `LoginParameter.java`, line 14; `ResetPasswordParameter.java`, line 14
**Description:** The `email` field is `public String email` in both classes, and both classes are `Serializable` with no `transient` annotation on the field. Email address is PII. Serialization of either class will include the email in plaintext. The same `public` visibility concern applies — no access control on a PII-carrying field.

---

**FINDING — APP20-F03 — Low**

**File:** `JoinCompanyParameter.java`, lines 14–15
**Description:** Fields `public int driver_id` and `public int comp_id` are `public` with no accessor encapsulation. While integers carry lower sensitivity than strings, `driver_id` is an operator identifier. Combined with serialization, this value is emitted in any serialized byte stream without restriction. The `public` modifier means any code holding the object can mutate it freely, which could allow caller code to tamper with which driver or company is sent to the web service.

---

No issues found (in assigned files only) — credential caching in static fields, `MODE_WORLD_READABLE`, external storage writes, or `SharedPreferences` usage — Section 3 additional items.

---

### 4. Input and Intent Handling

No Activity, Service, BroadcastReceiver, ContentProvider, WebView, or Intent construction is present in any of the three files. These are plain data-transfer objects. No issues found in assigned files — Section 4.

---

### 5. Authentication and Session

**FINDING — APP20-F04 — Medium (linked to APP20-F01)**

**File:** `LoginParameter.java`
**Description:** `LoginParameter` is the credential carrier passed to the authentication web service. The password is held as a plain `String` with `public` visibility and no lifecycle management. There is no mechanism in the class to clear the credential after the authentication call completes. Depending on how callers use this object (e.g., retaining the instance as a field on an Activity or ViewModel after login), the plaintext password remains in memory and in the string pool for an indeterminate duration. This is a session/authentication hygiene issue: the credential object has no self-clearing capability, and the `Serializable` contract means it can escape into serialized state at any point while live.

No token expiry, logout clearing, or multi-operator session logic is present in the assigned files (those concerns belong to higher-level classes). No issues found for those sub-items in assigned files — Section 5 remaining items.

---

### 6. Third-Party Libraries

No Gradle build files, dependency declarations, or ProGuard configuration are in the assigned file set. The assigned files import only `org.json`, `java.io`, `java.util`, and `java.math` — standard Android/Java platform APIs, no third-party library risk from these files. No issues found in assigned files — Section 6.

---

### 7. Google Play and Android Platform

No `AndroidManifest.xml`, `build.gradle`, permission declarations, runtime permission requests, or deprecated API usage is present in any of the three files. These are pure data objects with no platform API surface. No issues found in assigned files — Section 7.

---

## Summary Table

| ID | File | Severity | Description |
|----|------|----------|-------------|
| APP20-F01 | LoginParameter.java:15 | Medium | Password stored as plain public String; Serializable with no transient — credential exposed in any serialization path; String cannot be zeroed |
| APP20-F02 | LoginParameter.java:14 / ResetPasswordParameter.java:14 | Low | Email (PII) stored as public String; Serializable with no transient annotation |
| APP20-F03 | JoinCompanyParameter.java:14–15 | Low | driver_id and comp_id are public fields — no access control; caller can freely read or mutate operator and company identifiers |
| APP20-F04 | LoginParameter.java | Medium | No credential lifecycle management — no clear/zero mechanism; object can persist with plaintext password beyond authentication call |

**Total findings: 4 (2 Medium, 2 Low)**
