# Pass 1 Security Audit — APP29

**Agent ID:** APP29
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** Checklist specifies `Branch: main`; actual branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Reading Evidence

### File 1: LoginResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.LoginResultArray`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Fields:**
| Name | Type | Modifier | Line |
|------|------|----------|------|
| `arrayList` | `ArrayList<LoginItem>` | `public` | 14 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `LoginResultArray()` | 16 |
| `LoginResultArray(JSONArray jsonArray) throws JSONException` | 19 |

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

**Summary:** DTO/result array class that deserialises a `JSONArray` into an `ArrayList<LoginItem>`. No Android components declared. No permissions. No network calls.

---

### File 2: ManufactureResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.ManufactureResultArray`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Fields:**
| Name | Type | Modifier | Line |
|------|------|----------|------|
| `arrayList` | `ArrayList<ManufactureItem>` | `public` | 14 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `ManufactureResultArray()` | 16 |
| `ManufactureResultArray(JSONArray jsonArray) throws JSONException` | 19 |

**Imports:** (identical set to LoginResultArray.java)

**Summary:** DTO/result array class that deserialises a `JSONArray` into an `ArrayList<ManufactureItem>`. No Android components declared. No permissions. No network calls.

---

### File 3: PreStartHelpResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.PreStartHelpResultArray`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Fields:**
| Name | Type | Modifier | Line |
|------|------|----------|------|
| `arrayList` | `ArrayList<PreStartHelpItem>` | `public` | 14 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `PreStartHelpResultArray()` | 16 |
| `PreStartHelpResultArray(JSONArray jsonArray) throws JSONException` | 19 |

**Imports:** (identical set to LoginResultArray.java)

**Summary:** DTO/result array class that deserialises a `JSONArray` into an `ArrayList<PreStartHelpItem>`. No Android components declared. No permissions. No network calls.

---

## Step 3 — Checklist Review

All three files share an identical structural pattern: a thin DTO wrapper that holds a `public ArrayList<T>` and populates it from a `JSONArray` in its constructor. Findings are stated per checklist section.

---

### Section 1 — Signing and Keystores

No signing configuration, keystore references, credentials, or properties files are present in any of the three files.

**No issues found — Section 1.**

---

### Section 2 — Network Security

None of the three files contains network client code, URLs, IP addresses, API endpoint strings, TrustManager implementations, HostnameVerifier overrides, or SSLContext configuration. All three are pure data-model classes that consume already-parsed `JSONArray` input.

**No issues found — Section 2.**

---

### Section 3 — Data Storage

**Finding — Medium: Public field exposes login result data without access control**

- **File:** `LoginResultArray.java`, line 14
- **Field:** `public ArrayList<LoginItem> arrayList`
- **Detail:** The `arrayList` field is declared `public` with no accessor method or defensive copy. Any code holding a reference to a `LoginResultArray` instance can freely read, modify, or replace the entire list of `LoginItem` objects, which by class name are expected to contain authentication/session result data returned from the backend. If `LoginItem` stores credentials, session tokens, or operator identity data (which is likely given the class name and the app's forklift operator authentication domain), unrestricted public access to this field increases the blast radius of any code path that incorrectly passes a `LoginResultArray` reference beyond its intended consumer.
- **Note:** The same structural pattern (public `arrayList`) exists in `ManufactureResultArray` (line 14) and `PreStartHelpResultArray` (line 14). For those two classes the data involved (manufacturer reference data and pre-start help content) carries lower sensitivity. The concern is proportionally lower but the design inconsistency is noted.
- **Recommendation (informational):** Declare the field `private` and expose it via a getter returning an unmodifiable view or a defensive copy.

**Finding — Low: Serializable DTO with no serialVersionUID**

- **Files:** All three (`LoginResultArray.java`, `ManufactureResultArray.java`, `PreStartHelpResultArray.java`)
- **Detail:** Each class implements `java.io.Serializable` but declares no `private static final long serialVersionUID`. Java will compute a default UID at runtime based on class structure; any refactor that changes the class signature will silently break deserialisation of persisted or transmitted objects and can cause `InvalidClassException` in production. For `LoginResultArray` in particular, if session state containing this object is persisted (e.g. to a Bundle or file) across an app update, the mismatch could corrupt or drop login state.
- **Recommendation (informational):** Declare explicit `serialVersionUID` values in all three classes.

---

### Section 4 — Input and Intent Handling

None of the three files contain Activity, Service, BroadcastReceiver, or ContentProvider declarations, WebView usage, intent construction, deep link handling, or user-facing input processing. Input to these classes is a `JSONArray` object passed programmatically by the calling web service layer; no direct external input arrives here.

**No issues found — Section 4.**

---

### Section 5 — Authentication and Session

**Observation — related to Section 3 finding above:**

`LoginResultArray` is the container that holds backend login results. Its `public` field exposure (noted in Section 3) is directly relevant here: any component that obtains a reference to the populated `LoginResultArray` can inspect or mutate its contents without restriction. Whether the actual `LoginItem` fields contain tokens or passwords is determined by `LoginItem` itself (not in scope for this file set), but the container imposes no protection.

**No independent new issues found beyond the public-field concern already recorded — Section 5.**

---

### Section 6 — Third-Party Libraries

No third-party library dependencies are introduced in any of the three files. All imports are from `org.json` (Android SDK built-in), `java.io`, `java.util`, and `java.math` (standard library). The wildcard import of the internal `webserviceclasses` package is a minor code style issue but not a security concern.

**No issues found — Section 6.**

---

### Section 7 — Google Play and Android Platform

None of the three files reference deprecated APIs, Android permissions, SDK version guards, or Android platform APIs of any kind. They are plain Java classes with no Android framework dependency beyond what is inherited through `WebServiceResultPacket` (not in scope for this file set).

**No issues found — Section 7.**

---

## Summary of Findings

| ID | Severity | File | Line | Title |
|----|----------|------|------|-------|
| APP29-01 | Medium | `LoginResultArray.java` | 14 | Public field exposes login result list without access control |
| APP29-02 | Low | All three files | 14 (each) | `Serializable` classes lack explicit `serialVersionUID` |

**APP29-01** is the primary finding of note. The public `arrayList` field on the login result container means authentication response data has no encapsulation boundary. The remaining two files share the same structural pattern at lower risk due to data sensitivity.

**APP29-02** affects all three files equally and is a defensive robustness concern with indirect security relevance for `LoginResultArray`.

No Critical or High findings were identified in the assigned file set.
