# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP12
**Date:** 2026-02-27
**Stack:** Android/Java
**Branch audited:** master

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`. The actual repository default branch is `master`. Audit proceeded on `master` as instructed.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/FuelTypeItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/LoginItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/ManufactureItem.java`

---

## Reading Evidence

### File 1 — FuelTypeItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.FuelTypeItem`

**Implemented interfaces:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|-------|------|------|
| `id` | `int` | 14 |
| `name` | `String` | 15 |

**Constructors:**
| Signature | Line |
|-----------|------|
| `FuelTypeItem()` | 17 |
| `FuelTypeItem(JSONObject jsonObject) throws JSONException` | 20 |

**Public methods (non-constructor):** None declared beyond constructors.

**Activities / Services / BroadcastReceivers / ContentProviders:** None. This is a plain data model (POJO).

---

### File 2 — LoginItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.LoginItem`

**Implemented interfaces:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line | Sensitivity |
|-------|------|------|-------------|
| `id` | `int` | 15 | Low |
| `comp_id` | `int` | 16 | Low |
| `first_name` | `String` | 17 | PII |
| `last_name` | `String` | 18 | PII |
| `email` | `String` | 19 | PII |
| `password` | `String` | 20 | **CRITICAL — plaintext credential** |
| `phone` | `String` | 21 | PII |
| `licno` | `String` | 22 | PII — operator licence number |
| `expirydt` | `String` | 23 | PII — licence expiry date |
| `addr` | `String` | 24 | PII — address |
| `securityno` | `String` | 25 | PII — security number |
| `photo_url` | `String` | 26 | Low |
| `contactperson` | `boolean` | 27 | Low |
| `date_format` | `String` | 28 | Low |
| `max_session_length` | `int` | 29 | Low |
| `compliance_date` | `String` | 30 | Low |
| `gps_frequency` | `int` | 31 | Low |
| `drivers` | `List<LoginItem>` | 33 | High — nested operator records |
| `arrDriverTrainings` | `List<TrainingItem>` | 34 | Low |

**Constructors:**
| Signature | Line |
|-----------|------|
| `LoginItem(JSONObject jsonObject) throws JSONException` | 36 |

**Public methods (non-constructor):** None declared beyond the constructor.

**Activities / Services / BroadcastReceivers / ContentProviders:** None. This is a plain data model (POJO).

**Imports of note:**
- `android.util.Log` (line 3) — Log class imported; no `Log.*` call is visible in the constructor body, but the import's presence in a class carrying credential fields warrants noting.

---

### File 3 — ManufactureItem.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.ManufactureItem`

**Implemented interfaces:** `java.io.Serializable`

**Fields (all public):**
| Field | Type | Line |
|-------|------|------|
| `id` | `int` | 14 |
| `name` | `String` | 15 |

**Constructors:**
| Signature | Line |
|-----------|------|
| `ManufactureItem()` | 17 |
| `ManufactureItem(JSONObject jsonObject) throws JSONException` | 20 |

**Public methods (non-constructor):** None declared beyond constructors.

**Activities / Services / BroadcastReceivers / ContentProviders:** None. This is a plain data model (POJO).

---

## Findings by Checklist Section

### Section 1 — Signing and Keystores

No signing configuration, keystore references, or build credentials appear in the three assigned files. These are model classes with no build system interaction.

**Result:** No issues found in assigned files — Section 1.

---

### Section 2 — Network Security

No HTTP client code, URL construction, or network security configuration is present in FuelTypeItem.java or ManufactureItem.java.

**LoginItem.java** parses a JSON response that includes a `password` field. The class does not itself make network calls, but the presence of a plaintext password in the deserialized response payload is relevant to the transport layer: the server is sending credentials in API response bodies. If this response is received over HTTP (cleartext), the password is fully exposed in transit. This finding is addressed fully under Section 5 below; the network transport concern is flagged here for cross-reference.

**Result:** No direct network security issues found within the assigned files themselves — Section 2. Cross-reference: Section 5 finding regarding password in API response body has transport security implications.

---

### Section 3 — Data Storage

**FuelTypeItem.java:** No storage operations. No issues found.

**ManufactureItem.java:** No storage operations. No issues found.

**LoginItem.java:**

Finding 3-A (High): The class implements `java.io.Serializable`. Because `LoginItem` contains a `password` field (line 20, type `String`), any serialization of this object — including writing to a `Bundle`, passing via `Intent.putExtra()`, writing to a file, or saving to SharedPreferences — will include the plaintext password in the serialized byte stream. Java serialization provides no encryption. If a `LoginItem` instance is ever stored to disk (e.g. SharedPreferences, a file, SQLite as a blob), the password is stored in cleartext. The audit scope for this file does not include the call sites, but the structural risk is present and must be investigated at the call-site level.

Finding 3-B (Medium): The `drivers` field (line 33) is a `List<LoginItem>`. Each nested `LoginItem` also carries a `password` field. A single serialized `LoginItem` for a contact person therefore serializes the credentials of every driver under that contact person's account. The blast radius of any serialization or storage of a contact-person `LoginItem` is the credentials of the entire driver list.

**Result:** High finding (3-A) and Medium finding (3-B) identified — Section 3.

---

### Section 4 — Input and Intent Handling

No Activity, Service, BroadcastReceiver, or ContentProvider is declared in any of the three files. No WebView usage, no Intent construction, no deep link handling.

**Result:** No issues found in assigned files — Section 4.

---

### Section 5 — Authentication and Session

**FuelTypeItem.java:** No authentication or session logic. No issues found.

**ManufactureItem.java:** No authentication or session logic. No issues found.

**LoginItem.java:**

Finding 5-A (Critical): `LoginItem` contains a `public String password` field (line 20) populated directly from a server JSON response (`parser.getString("password")`, line 47). This means the backend API returns the user's password as a field in the authentication response payload. A correctly designed authentication system does not return passwords — it issues a token (session token, JWT, or similar). Receiving the raw password from the server indicates either:
  (a) the server is storing passwords in a recoverable (plaintext or reversibly encrypted) form, which is a critical backend vulnerability, or
  (b) the password field is repurposed for a PIN or operator code distinct from the login credential — this would require verification at call sites.
  Either interpretation represents a Critical or High risk. The field name `password` combined with field names `email` and `securityno` is consistent with a real password credential being returned.

Finding 5-B (High): All fields in `LoginItem` are `public` with no access modifier restriction. This means any code in the application that holds a reference to a `LoginItem` instance has direct, unrestricted read access to the `password` field. There is no encapsulation — no getter/setter pattern that could be instrumented to detect or restrict access. Combined with `Serializable`, the credential is structurally unprotected at the object level.

Finding 5-C (Low): `android.util.Log` is imported (line 3) into `LoginItem`. No `Log.*` call is visible in the constructor body as audited. However, the import creates a risk that a developer adding debug logging in future — or in a version not captured in this audit pass — could inadvertently log the `password` field. This should be verified across the full git history and any debug variants.

**Result:** Critical finding (5-A) and High finding (5-B) identified — Section 5.

---

### Section 6 — Third-Party Libraries

No dependency declarations, Gradle files, or library usage appear in the three assigned files (beyond standard Java and Android SDK imports: `org.json`, `java.io.Serializable`, `java.util`, `android.util.Log`).

**Result:** No issues found in assigned files — Section 6.

---

### Section 7 — Google Play and Android Platform

No `targetSdkVersion`, `minSdkVersion`, permissions, deprecated APIs, or runtime permission handling appear in the three assigned files. These are plain model classes.

One deprecated-pattern observation: `AsyncTask` and similar concerns are not present here. No issues arising from the assigned files.

**Result:** No issues found in assigned files — Section 7.

---

## Summary of Findings

| ID | Severity | File | Section | Description |
|----|----------|------|---------|-------------|
| APP12-001 | Critical | LoginItem.java | 5 | Server API response returns `password` as a plaintext JSON field. The backend either stores passwords in recoverable form or is transmitting real credentials in response bodies. Line 47: `password = parser.getString("password")`. |
| APP12-002 | High | LoginItem.java | 3, 5 | `LoginItem` implements `Serializable` while containing a plaintext `password` field. Any serialization of this object writes the credential to the serialized stream with no encryption. |
| APP12-003 | High | LoginItem.java | 5 | All fields including `password` are `public` with no encapsulation. Any holder of a `LoginItem` reference has unrestricted direct access to the credential. |
| APP12-004 | Medium | LoginItem.java | 3 | The `drivers` field (List<LoginItem>) causes a serialized contact-person `LoginItem` to embed all driver credentials recursively, amplifying the blast radius of any insecure storage or transmission. |
| APP12-005 | Low | LoginItem.java | 5 | `android.util.Log` is imported but not visibly used in the constructor. The import in a credential-bearing class creates risk of accidental credential logging in debug variants or future changes. |
| APP12-006 | Info | All files | Branch | Checklist specifies `Branch: main`; actual branch is `master`. Audit proceeded on `master`. |

---

## Files With No Findings

- `FuelTypeItem.java` — Simple two-field lookup model. No sensitive data, no storage, no network calls, no authentication logic. No issues found across all checklist sections.
- `ManufactureItem.java` — Simple two-field lookup model. Structurally identical to FuelTypeItem. No issues found across all checklist sections.
