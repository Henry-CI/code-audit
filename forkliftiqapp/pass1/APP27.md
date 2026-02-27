# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP27
**Date:** 2026-02-27
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`, but the actual current branch is `master`. Audit proceeds on `master` as instructed.

---

## Step 2 — Checklist Referenced

`/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`

Sections reviewed:
1. Signing and Keystores
2. Network Security
3. Data Storage
4. Input and Intent Handling
5. Authentication and Session
6. Third-Party Libraries
7. Google Play and Android Platform

---

## Step 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/FuelTypeResultArray.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/GetCompanyResultArray.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/GetEmailResult.java`

---

## Step 4 — Reading Evidence

### File 1: FuelTypeResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.FuelTypeResultArray`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Fields:**
| Visibility | Type | Name | Line |
|---|---|---|---|
| public | `ArrayList<FuelTypeItem>` | `arrayList` | 14 |

**Public methods:**
| Signature | Line |
|---|---|
| `FuelTypeResultArray()` | 16 |
| `FuelTypeResultArray(JSONArray jsonArray) throws JSONException` | 19 |

**Android components declared:** None (plain Java class, not an Activity, Fragment, Service, Receiver, or Provider).

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

### File 2: GetCompanyResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.GetCompanyResultArray`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Fields:**
| Visibility | Type | Name | Line |
|---|---|---|---|
| public | `ArrayList<CompanyItem>` | `arrayList` | 14 |

**Public methods:**
| Signature | Line |
|---|---|
| `GetCompanyResultArray()` | 16 |
| `GetCompanyResultArray(JSONArray jsonArray) throws JSONException` | 19 |

**Android components declared:** None.

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

### File 3: GetEmailResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.GetEmailResult`

**Superclass:** `WebServiceResultPacket`

**Interfaces implemented:** `java.io.Serializable`

**Fields:**
| Visibility | Type | Name | Line |
|---|---|---|---|
| public | `int` | `id` | 14 |
| public | `int` | `driver_id` | 15 |
| public | `String` | `email_addr1` | 16 |
| public | `String` | `email_addr2` | 17 |
| public | `String` | `email_addr3` | 18 |
| public | `String` | `email_addr4` | 19 |

**Public methods:**
| Signature | Line |
|---|---|
| `GetEmailResult()` | 21 |
| `GetEmailResult(JSONObject jsonObject) throws JSONException` | 24 |

**Android components declared:** None.

**Imports:**
- `org.json.JSONException`
- `org.json.JSONObject`
- `java.io.Serializable`
- `org.json.JSONArray`
- `java.util.ArrayList`
- `java.math.BigDecimal`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*`

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No keystore files, `signingConfigs` blocks, `gradle.properties`, or `local.properties` are present in any of the three assigned files. These are plain data-transfer object (DTO) classes with no build configuration.

**Finding:** No issues found — Signing and Keystores.

---

### Section 2 — Network Security

None of the three files contain hardcoded URLs, IP addresses, API endpoints, or HTTP client configuration. No `TrustAllCertificates`, `hostnameVerifier`, or `SSLContext` usage is present. No `AndroidManifest.xml` attributes appear in these files.

**Finding:** No issues found — Network Security.

---

### Section 3 — Data Storage

**Finding (Low): Public fields expose PII and operator identity data without access control.**

All three classes declare their fields `public` with no encapsulation (no getters/setters, no `private` modifier).

Relevant fields in `GetEmailResult.java`:
- Line 14: `public int id`
- Line 15: `public int driver_id`
- Lines 16-19: `public String email_addr1`, `email_addr2`, `email_addr3`, `email_addr4`

The `email_addr1`–`email_addr4` fields hold email addresses (PII). The `driver_id` field identifies a specific operator. Because these are `public` fields on a `Serializable` class, any code that obtains a reference to a `GetEmailResult` object — including any class in any package — can read or overwrite these values directly. There is no defensive copying, nullability contract, or access control enforced.

The `Serializable` implementation without a defined `serialVersionUID` (absent in all three classes) is a minor robustness concern: if the class structure changes, deserialized objects from older data may throw `InvalidClassException` at runtime. This is not a direct security vulnerability but contributes to data-handling fragility for operator PII.

No direct `SharedPreferences` writes, file I/O, or database writes were found within these files. The storage risk is indirect: any caller of these DTOs may persist or log the unprotected public fields. That risk is assessed in the context of the broader codebase; within the scope of these three files the specific finding is the absence of field-level access control on PII-bearing data.

**Finding (Low): Unused import of `java.math.BigDecimal` in all three files.**

Lines 8 in all three files import `java.math.BigDecimal`, which is not referenced anywhere in any of the three files. This is dead code and, while not a security vulnerability in isolation, indicates the files were generated from a template without cleanup. Dead imports can obscure the actual data surface when reviewing code at scale.

---

### Section 4 — Input and Intent Handling

None of the three files are Android components (not Activities, Services, Receivers, or Providers). No `Intent` usage, no WebView, no deep-link handling, and no exported component attributes are present.

**Finding:** No issues found — Input and Intent Handling.

---

### Section 5 — Authentication and Session

`GetEmailResult.java` carries `driver_id` and up to four email addresses. These fields are populated directly from a `JSONObject` received from the network response (lines 31–59). There is no validation of the `driver_id` value (e.g., no bounds check, no cross-check against the currently authenticated session's user identity). A compromised or tampered server response could populate `driver_id` with an arbitrary value, and because the field is `public`, downstream code could silently use it.

This is a low-severity finding within these files alone; the actual session integrity depends on how callers consume this object.

**Finding (Low): No input validation on `driver_id` or email address fields in `GetEmailResult`.**

Fields are assigned directly from JSON with null checks only. No format validation is applied to email addresses before storage in the object. Downstream callers that trust these values without re-validating may process malformed data from a compromised API response.

No token storage, session management, or credential caching code is present in any of the three files.

---

### Section 6 — Third-Party Libraries

The three files use only standard Android SDK libraries (`org.json.*`) and Java standard library (`java.io.Serializable`, `java.util.ArrayList`, `java.math.BigDecimal`). No third-party library dependencies are introduced by these files.

**Finding:** No issues found — Third-Party Libraries.

---

### Section 7 — Google Play and Android Platform

No `targetSdkVersion`, `minSdkVersion`, permission declarations, or deprecated API usage (e.g., `AsyncTask`) appear in these three files.

**Finding:** No issues found — Google Play and Android Platform.

---

## Summary of Findings

| ID | File | Severity | Section | Description |
|---|---|---|---|---|
| APP27-01 | `GetEmailResult.java` | Low | 3 — Data Storage | PII fields (`email_addr1`–`email_addr4`, `driver_id`) are `public` with no access control; any caller can read or overwrite operator email addresses and identity. |
| APP27-02 | `FuelTypeResultArray.java`, `GetCompanyResultArray.java`, `GetEmailResult.java` | Low | 3 — Data Storage | No `serialVersionUID` defined on `Serializable` classes; structural changes will produce `InvalidClassException` on deserialized instances, contributing to data-handling fragility. |
| APP27-03 | `FuelTypeResultArray.java`, `GetCompanyResultArray.java`, `GetEmailResult.java` | Info | 3 — Data Storage | Unused import of `java.math.BigDecimal` in all three files; suggests template-generated code without cleanup, increasing audit surface noise. |
| APP27-04 | `GetEmailResult.java` | Low | 5 — Authentication and Session | No validation of `driver_id` or email address format on JSON deserialization; downstream callers receive unvalidated values from the network. |

**Branch discrepancy:** Checklist specifies `Branch: main`; actual branch is `master`. Audit was performed on `master` as instructed.
