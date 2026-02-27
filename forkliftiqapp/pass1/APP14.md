# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP14
**Date:** 2026-02-27
**Stack:** Android/Java
**Branch audited:** master

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`, but the actual branch in the repository is `master`. Audit proceeds on `master` as instructed.

---

## Reading Evidence

### File 1: RefreshTokenItem.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.RefreshTokenItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
- `public String value` — line 14. Token value stored as a plain `String`.
- `public int expiration` — line 15. Token expiration stored as an integer (presumably seconds or epoch offset).

**Public methods:**
- `RefreshTokenItem()` — default constructor, line 17.
- `RefreshTokenItem(JSONObject jsonObject) throws JSONException` — JSON-deserialising constructor, line 20. Populates `value` from `jsonObject.getString("value")` (line 27) and `expiration` from `jsonObject.getInt("expiration")` (line 31). Performs null-guard on the JSONObject parameter and uses `isNull()` checks before each field read.

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None. This is a plain data-model class.

**Imports noted:**
- `org.json.JSONException`, `org.json.JSONObject`, `java.io.Serializable`, `org.json.JSONArray`, `java.util.ArrayList`, `java.math.BigDecimal`
- Wildcard: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- Wildcard: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

### File 2: ReportItem.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.ReportItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
- `public int id` — line 14.
- `public String name` — line 15.

**Public methods:**
- `ReportItem()` — default constructor, line 17.
- `ReportItem(JSONObject jsonObject) throws JSONException` — JSON-deserialising constructor, line 20. Populates `id` from `jsonObject.getInt("id")` (line 27) and `name` from `jsonObject.getString("name")` (line 31). Performs null-guard on the JSONObject parameter and uses `isNull()` checks before each field read.

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None. Plain data-model class.

**Imports noted:** Same set as RefreshTokenItem.java.

---

### File 3: RoleItem.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.RoleItem`

**Implements:** `java.io.Serializable`

**Fields (all public):**
- `public int id` — line 14.
- `public String name` — line 15.
- `public String description` — line 16.

**Public methods:**
- `RoleItem()` — default constructor, line 18.
- `RoleItem(JSONObject jsonObject) throws JSONException` — JSON-deserialising constructor, line 21. Populates `id` (line 27), `name` (line 32), and `description` (line 37) with null-guard and `isNull()` checks before each field read.

**Activities / Fragments / Services / BroadcastReceivers / ContentProviders declared:** None. Plain data-model class.

**Imports noted:** Same set as RefreshTokenItem.java.

---

## Findings by Checklist Section

### Section 1 — Signing and Keystores

No findings applicable. These files are runtime data-model classes containing no signing configuration, keystore references, passwords, or build credentials.

No issues found — Section 1.

---

### Section 2 — Network Security

No findings applicable. These files contain no HTTP client code, no URL construction, no TrustManager overrides, and no hardcoded endpoint strings.

No issues found — Section 2.

---

### Section 3 — Data Storage

**Finding DS-01 — Severity: Medium**
**File:** `RefreshTokenItem.java`
**Lines:** 14–15

`RefreshTokenItem` holds two public fields:

```java
public String value;
public int expiration;
```

`value` carries the authentication refresh token received from the backend. The class implements `java.io.Serializable`. A serializable object with a plain `String` token field can be written to disk via Java object serialization, stored in a `Bundle` that gets persisted, or included in an `Intent` that may be logged or sniffed. The field carries no `transient` modifier to exclude it from serialization, and it is `public` with no accessor control. If callers persist this object (e.g., to `SharedPreferences` via serialization, to a file, or via `onSaveInstanceState`), the raw token string is exposed in whatever storage mechanism is used.

The immediate concern within this file is the absence of the `transient` keyword on `value`. The broader concern — how callers store this object — cannot be resolved from this file alone and should be traced in the wider codebase during a subsequent pass.

**Recommendation:** Mark `value` as `transient` to prevent automatic Java serialization of the token. Token persistence, if required, should be handled explicitly through `EncryptedSharedPreferences` or the Android Keystore, not through general-purpose object serialization.

---

**Finding DS-02 — Severity: Low / Observation**
**Files:** `RefreshTokenItem.java`, `ReportItem.java`, `RoleItem.java`
**All files**

All three classes declare every field `public` with no encapsulation (no getters/setters, no `private` modifiers). This violates the principle of least privilege. For `ReportItem` and `RoleItem` this is a code-quality issue with no direct security impact, since their fields (`id`, `name`, `description`) are not sensitive. For `RefreshTokenItem`, public field access on `value` means callers can read or overwrite the token without any interception point, making auditing or defensive coding (e.g., zeroing a token after use) impossible within the class.

---

**Wildcard import observation:**
All three files include:
```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```
These wildcard imports are unused within each file as no types from those packages are referenced in the class body. This is a code-hygiene issue. In itself it carries no security impact, but unused imports from a sensitive package (`webserviceclasses.results`) add unnecessary surface in the compiled class's constant pool and can obscure static analysis.

No further data-storage issues found — Section 3.

---

### Section 4 — Input and Intent Handling

No findings applicable. None of these classes are Activities, Services, BroadcastReceivers, or ContentProviders. They contain no WebView usage, no Intent construction, no deep-link handling. JSON parsing uses `JSONObject.isNull()` guards before each field access, which correctly avoids `JSONException` on missing keys.

No issues found — Section 4.

---

### Section 5 — Authentication and Session

**Finding AUTH-01 — Severity: Medium (cross-reference with DS-01)**
**File:** `RefreshTokenItem.java`
**Lines:** 14–15

`RefreshTokenItem` models the refresh token returned from the backend (field `value`) and its expiration (`expiration`). No token lifecycle management is present within this class (as expected for a data-model class). The audit note from DS-01 applies here: the token is held as a plain `String` in a serializable, fully public object. If the caller persists this object without encryption, the session token is stored in plaintext.

The `expiration` field is an `int`. Whether this represents seconds-until-expiry, an epoch timestamp, or another encoding cannot be determined from this file. The handling of expiry (checking before use, forcing re-authentication on expiry) must be verified in the caller chain in a later pass.

No issues found beyond what is already noted — Section 5.

---

### Section 6 — Third-Party Libraries

No findings applicable. These files import only `org.json.*` (bundled with the Android platform) and `java.*` standard library classes. No third-party library dependencies are introduced by these files.

No issues found — Section 6.

---

### Section 7 — Google Play and Android Platform

No findings applicable. These files contain no manifest declarations, no permission usage, no deprecated API calls, and no SDK-version-sensitive code paths.

No issues found — Section 7.

---

## Summary of Findings

| ID | Severity | File | Description |
|----|----------|------|-------------|
| DS-01 | Medium | RefreshTokenItem.java | `value` field (refresh token) is a plain `String` in a `Serializable` class with no `transient` modifier; token can be serialized to disk in plaintext by any caller that persists the object |
| DS-02 | Low | All three files | All fields are `public` with no accessor control; for `RefreshTokenItem.value` this prevents defensive zeroing or auditing of token access |
| AUTH-01 | Medium (cross-ref DS-01) | RefreshTokenItem.java | Refresh token stored as a plain `String`; token expiry encoding (`int expiration`) is opaque; full expiry-handling assessment requires caller-chain review |

**Files with no security findings:** `ReportItem.java`, `RoleItem.java` (contain only non-sensitive report and role metadata).

---

*Report generated by Agent APP14. Pass 1 scope only — findings are limited to the three assigned files. Caller-chain analysis of token persistence and expiry handling deferred to a subsequent pass.*
