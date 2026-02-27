# Pass 1 Security Audit — APP10
**Agent ID:** APP10
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist specifies `Branch: main`, but the actual branch is `master`. Branch is confirmed as `master`; audit proceeds.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/AnswerItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/CompanyItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/EquipmentItem.java`

---

## Step 3 — Reading Evidence

### File 1: AnswerItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.AnswerItem`

**Implemented interfaces:** `java.io.Serializable`

**Fields (all public):**
| Line | Type | Name |
|------|------|------|
| 14 | `int` | `question_id` |
| 15 | `String` | `answer` |

**Public methods:**
| Line | Signature |
|------|-----------|
| 17 | `public AnswerItem()` |
| 20 | `public AnswerItem(JSONObject jsonObject) throws JSONException` |

**Component type:** Plain data model (not an Activity, Fragment, Service, BroadcastReceiver, or ContentProvider).

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

Note: `JSONArray`, `ArrayList`, `BigDecimal`, and the wildcard imports are unused in this file.

---

### File 2: CompanyItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.CompanyItem`

**Implemented interfaces:** `java.io.Serializable`

**Fields (all public):**
| Line | Type | Name |
|------|------|------|
| 14 | `int` | `id` |
| 15 | `String` | `name` |
| 16 | `String` | `email` |
| 17 | `String` | `password` |
| 18 | `ArrayList<RoleItem>` | `arrRoles` |
| 19 | `PermissionItem` | `permission` |

**Public methods:**
| Line | Signature |
|------|-----------|
| 21 | `public CompanyItem()` |
| 24 | `public CompanyItem(JSONObject jsonObject) throws JSONException` |

**Component type:** Plain data model (not an Activity, Fragment, Service, BroadcastReceiver, or ContentProvider).

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

Note: `BigDecimal` is unused in this file.

---

### File 3: EquipmentItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.EquipmentItem`

**Implemented interfaces:** `java.io.Serializable`

**Fields (all public):**
| Line | Type | Name |
|------|------|------|
| 10 | `int` | `type_id` |
| 11 | `int` | `comp_id` |
| 12 | `int` | `fuel_type_id` |
| 13 | `int` | `impact_threshold` |
| 14 | `int` | `manu_id` |
| 15 | `int` | `id` |
| 16 | `String` | `name` |
| 17 | `String` | `type` |
| 18 | `String` | `manu` |
| 19 | `String` | `fuel_type` |
| 20 | `String` | `comp` |
| 21 | `String` | `serial_no` |
| 22 | `String` | `mac_address` |
| 23 | `String` | `url` |
| 24 | `boolean` | `active` |
| 25 | `boolean` | `alert_enabled` |
| 26 | `boolean` | `driver_based` |
| 27 | `int` | `hours` |
| 28 | `boolean` | `trained` |

**Public methods:**
| Line | Signature |
|------|-----------|
| 30 | `public EquipmentItem()` |
| 33 | `public EquipmentItem(JSONObject jsonObject) throws JSONException` |

**Component type:** Plain data model (not an Activity, Fragment, Service, BroadcastReceiver, or ContentProvider).

**Imports:**
- `au.com.collectiveintelligence.fleetiq360.WebService.JSONObjectParser`
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`

---

## Step 4 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found. These files are JSON-to-object mapping data model classes. They contain no signing configuration, keystore references, password values, or credential file paths.

---

### Section 2 — Network Security

No issues found. These files contain no HTTP client instantiation, no URL construction, and no SSL/TLS configuration. `EquipmentItem` contains a `url` field (line 23) that holds a URL string value deserialized from an API response; this is a data holder, not a network call site. No hardcoded endpoint strings are present in any of the three files.

---

### Section 3 — Data Storage

**FINDING — HIGH: Password deserialized into a public unprotected field (CompanyItem.java)**

- **File:** `CompanyItem.java`
- **Field:** `public String password` (line 17)
- **Location of population:** Constructor `CompanyItem(JSONObject)`, lines 44–47

The `password` field is declared `public`, has no access control, and is populated directly from the server JSON response. This means a plaintext password value received from the API is held in an unprotected in-memory object with public visibility. Any code that holds a reference to a `CompanyItem` instance can directly read the password string without any accessor restriction.

Because `CompanyItem` implements `java.io.Serializable`, instances can be passed between components via `Intent` extras or written to streams. If any calling code serializes this object to a file, `SharedPreferences`, or passes it in an `Intent` bundle, the password travels in plaintext through those channels. The `Serializable` interface combined with a public `password` field increases the attack surface.

Additionally, if `CompanyItem` instances are cached in memory (e.g., held in a static field, an Application-scoped singleton, or a list) beyond the immediate authentication transaction, the password persists in the JVM heap where it may be recoverable from a heap dump or via debugger attachment on a rooted/debug device.

**Recommendation (informational, not prescriptive):** The API should not return plaintext passwords in any response payload. The field should be removed. If an API contract change is not immediately possible, the field should at minimum have private access with no getter, and the value should be zeroed immediately after use. This finding may also indicate the backend is storing and transmitting passwords in plaintext, which is a separate and more severe backend concern.

---

**FINDING — MEDIUM: All fields across all three classes are public with no access control**

- **Files:** `AnswerItem.java` (lines 14–15), `CompanyItem.java` (lines 14–19), `EquipmentItem.java` (lines 10–28)

All fields in all three classes are declared `public`. This provides no encapsulation. While public fields are not inherently a security vulnerability for non-sensitive data types, they permit any code in the application to mutate these objects freely, which can lead to data integrity issues. For `CompanyItem` specifically, the combination of public fields and `Serializable` is the condition that makes the password field exposure more severe.

Fields of note with broader sensitivity beyond passwords:
- `CompanyItem.email` (line 16): PII — email address exposed publicly.
- `EquipmentItem.mac_address` (line 22): Device hardware identifier, potentially PII or sensitive operational data.
- `EquipmentItem.serial_no` (line 21): Equipment identifier that could be used for asset tracking or enumeration.

---

**FINDING — LOW: Unused imports (code quality / attack surface hygiene)**

- **Files:** `AnswerItem.java` and `CompanyItem.java`

Both files contain wildcard imports (`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` and `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`) and `java.math.BigDecimal` which are not used. Unused wildcard imports expand the set of names resolved at compile time and can obscure which types are actually in use, complicating security review.

---

### Section 4 — Input and Intent Handling

No Activity, Service, or BroadcastReceiver components are present in these files. However, a related observation is documented here:

**FINDING — LOW: No input validation on deserialized JSON values**

- **Files:** `AnswerItem.java` (lines 25–33), `CompanyItem.java` (lines 29–64), `EquipmentItem.java` (lines 38–56)

All three constructors accept a `JSONObject` from the network and map its values directly into fields without any validation of length, content, or character set. In `AnswerItem` and `CompanyItem`, string values are assigned from `jsonObject.getString()` without bounds checking. In `EquipmentItem`, the `JSONObjectParser` wrapper is used but no evidence of internal validation was inspected in these files.

If a malicious or corrupted API response provides unexpectedly large strings, specially crafted content, or values of the wrong type, these objects will hold that data and propagate it to any downstream UI or storage operations that consume these models.

---

### Section 5 — Authentication and Session

**FINDING — see Section 3 above (CompanyItem.password)**

The `password` field in `CompanyItem` is directly relevant to authentication. The concern regarding in-memory lifetime is repeated here for cross-reference: there is no mechanism in this class to clear the password after use. The string will remain on the heap until garbage collected, with no zeroing or nulling performed.

No token expiry logic, session management code, or logout clearing logic is present in these data model files. That scope is outside these three files.

---

### Section 6 — Third-Party Libraries

No dependency declarations are present in these files. These are pure Java source files. The libraries used (`org.json`) are Android platform-standard. No third-party library CVE concerns arise directly from these files.

---

### Section 7 — Google Play and Android Platform

No `targetSdkVersion`, `minSdkVersion`, permission declarations, or deprecated API usage is present in these three data model files. No `AsyncTask`, `startActivityForResult`, or similar deprecated patterns are used.

No issues found — Section 7.

---

## Summary of Findings

| ID | Severity | File | Description |
|----|----------|------|-------------|
| APP10-001 | High | `CompanyItem.java` line 17, 44–47 | Plaintext password deserialized from API response into a public field on a `Serializable` class. Password is exposed in-memory with no access restriction and no zeroing after use. |
| APP10-002 | Medium | All three files | All fields declared `public` with no encapsulation. PII fields (`email`, `mac_address`, `serial_no`) and the `password` field have no access control. `Serializable` combined with public fields allows uncontrolled serialization of sensitive data. |
| APP10-003 | Low | `AnswerItem.java`, `CompanyItem.java` | No input validation on JSON-deserialized string values. Unbounded strings accepted from network response. |
| APP10-004 | Low | `AnswerItem.java`, `CompanyItem.java` | Unused imports including wildcard imports that complicate security review and expand name resolution scope. |
