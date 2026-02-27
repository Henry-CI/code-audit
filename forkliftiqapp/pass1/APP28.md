# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP28
**Date:** 2026-02-27
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist specifies `Branch: main`. The actual branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Checklist Reference

Full checklist read from `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`.
Sections reviewed: Signing and Keystores, Network Security, Data Storage, Input and Intent Handling, Authentication and Session, Third-Party Libraries, Google Play and Android Platform.

---

## Step 3 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/GetEquipmentResultArray.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/GetTokenResult.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/results/JoinCompanyResult.java`

Supporting files read for context (referenced by assigned files or their callers):
- `WebService/webserviceclasses/RefreshTokenItem.java`
- `WebService/webserviceclasses/WebServiceResultPacket.java`
- `WebService/webserviceclasses/WebServicePacket.java`
- `WebService/webserviceclasses/EquipmentItem.java`
- `WebService/WebData.java` (token storage caller)
- `WebService/WebApi.java` (token issuance caller)
- `autoupdate/util/TokenAuthenticator.java` (token refresh caller)
- `WebService/FakeX509TrustManager.java` (referenced by TokenAuthenticator)
- `model/ModelPrefs.java` (storage backend for token)

---

## Step 4 — Reading Evidence

### File 1: GetEquipmentResultArray.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.GetEquipmentResultArray`

**Extends / Implements:**
- Extends: `WebServiceResultPacket` → `WebServiceResultPacket` extends `WebServicePacket`
- Implements: `Serializable`

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `arrayList` | `ArrayList<EquipmentItem>` | `public` | 14 |

**Public methods:**
| Signature | Line |
|---|---|
| `GetEquipmentResultArray()` | 16 |
| `GetEquipmentResultArray(JSONArray jsonArray) throws JSONException` | 19 |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

**EquipmentItem fields (supporting file, relevant to data sensitivity assessment):**
`type_id`, `comp_id`, `fuel_type_id`, `impact_threshold`, `manu_id`, `id`, `name`, `type`, `manu`, `fuel_type`, `comp`, `serial_no`, `mac_address`, `url`, `active`, `alert_enabled`, `driver_based`, `hours`, `trained`

Note: `mac_address` and `serial_no` are hardware identifiers for forklift equipment.

---

### File 2: GetTokenResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.GetTokenResult`

**Extends / Implements:**
- Extends: `WebServiceResultPacket` → `WebServicePacket`
- Implements: `Serializable`

**Fields (all public):**
| Name | Type | Visibility | Line | Sensitivity |
|---|---|---|---|---|
| `value` | `String` | `public` | 14 | HIGH — bearer token value |
| `expiration` | `int` | `public` | 15 | Low |
| `tokenType` | `String` | `public` | 16 | Low |
| `expired` | `boolean` | `public` | 17 | Low |
| `refreshToken` | `RefreshTokenItem` | `public` | 18 | HIGH — refresh token object |

**RefreshTokenItem fields (supporting file):**
| Name | Type | Line | Sensitivity |
|---|---|---|---|
| `value` | `String` | 14 | HIGH — refresh token value (plaintext String) |
| `expiration` | `int` | 15 | Low |

**Public methods:**
| Signature | Line |
|---|---|
| `GetTokenResult()` | 20 |
| `GetTokenResult(JSONObject jsonObject) throws JSONException` | 23 |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

### File 3: JoinCompanyResult.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.JoinCompanyResult`

**Extends / Implements:**
- Extends: `WebServiceResultPacket` → `WebServicePacket`
- Implements: `Serializable`

**Fields (all public):**
| Name | Type | Visibility | Line | Sensitivity |
|---|---|---|---|---|
| `driver_id` | `int` | `public` | 14 | Medium — operator identifier |
| `comp_id` | `int` | `public` | 15 | Medium — company identifier |

**Public methods:**
| Signature | Line |
|---|---|
| `JoinCompanyResult()` | 17 |
| `JoinCompanyResult(JSONObject jsonObject) throws JSONException` | 20 |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared.**

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores

No findings directly applicable to the three assigned files. These are runtime data-transfer classes with no build configuration content.

**Result:** No issues found — Signing and Keystores (not applicable to assigned files).

---

### Section 2 — Network Security

**Finding NS-01 — Critical: TLS Certificate Validation Disabled Globally**

File: `TokenAuthenticator.java` (line 39) — called during token refresh for assigned class `GetTokenResult`.

```java
FakeX509TrustManager.allowAllSSL();
```

`FakeX509TrustManager.allowAllSSL()` (in `FakeX509TrustManager.java`) performs two globally destructive operations on `HttpsURLConnection`:

1. Sets `HttpsURLConnection.setDefaultHostnameVerifier()` to a lambda that unconditionally returns `true` for all hostnames (lines 68–75). This bypasses hostname verification entirely.
2. Sets `HttpsURLConnection.setDefaultSSLSocketFactory()` to an SSLContext backed by a custom `X509TrustManager` whose `checkServerTrusted()` and `checkClientTrusted()` methods are empty (no-ops), accepting every certificate regardless of validity, chain, or issuer (lines 26–33).

Because these are set as **default** values on `HttpsURLConnection`, they affect all HTTPS connections opened anywhere in the application process after this call is made, not just the token refresh connection. The call occurs in `TokenAuthenticator.getAccessToken()`, which executes on 401 responses during any authenticated request — meaning these defaults may be set early in a session and persist.

The result is that the application is fully susceptible to man-in-the-middle attacks. An attacker on the same network segment can present any certificate for any hostname, intercept all traffic including bearer tokens (the `value` field in `GetTokenResult`) and refresh tokens (`RefreshTokenItem.value`), and neither the hostname check nor certificate chain validation will raise an error.

For a forklift fleet management application transmitting operator credentials, session tokens, equipment assignments, and potentially incident data, this is a critical vulnerability.

**Affected assigned classes:** `GetTokenResult` and its `value` and `refreshToken` fields are transmitted over connections where TLS validation is disabled. All token material is exposed to interception.

---

### Section 3 — Data Storage

**Finding DS-01 — High: Authentication Token Stored in Unencrypted SharedPreferences**

`GetTokenResult` (the entire object, including `value` and `refreshToken`) is serialized via Gson and written to plain `SharedPreferences` under the key `"token_result"`.

Trace:
- `WebApi.authApp()` calls `WebData.instance().setGetTokenResult(result)` (`WebApi.java` line 101).
- `WebData.setGetTokenResult()` calls `ModelPrefs.saveObject(TOKEN_ITEM_KEY, result)` (`WebData.java` line 93).
- `ModelPrefs.saveObject()` calls `getPref().edit().putString(key, s).commit()` using `Context.MODE_PRIVATE` SharedPreferences (`ModelPrefs.java` lines 53–59).

`Context.MODE_PRIVATE` limits access to the same application UID at the OS level, but the data is written as plaintext JSON to the device's unencrypted SharedPreferences XML file. On a rooted device or via an ADB backup (if `android:allowBackup="true"` — not verified in this file set but noted for follow-up), this file is directly readable. The bearer token value and the refresh token value are both stored in this manner with no encryption.

The checklist requirement is `EncryptedSharedPreferences` from Jetpack Security for any sensitive values. This requirement is not met.

**Affected assigned class:** `GetTokenResult` — fields `value` (bearer token) and `refreshToken.value` (refresh token string, from `RefreshTokenItem`).

**Finding DS-02 — Low: All Result Classes Implement Serializable Without serialVersionUID**

`GetEquipmentResultArray`, `GetTokenResult`, and `JoinCompanyResult` all implement `Serializable` (directly and through the inheritance chain `WebServicePacket` → `WebServiceResultPacket`). None declare an explicit `serialVersionUID`. The JVM will generate one at compile time based on class structure. If the class structure changes, deserialization of previously serialized instances (e.g., from persistent storage or a cached Intent extra) will throw `InvalidClassException`. This is a robustness concern rather than a direct security finding, but for `GetTokenResult` specifically, serialization failure during token recovery could cause silent authentication failures rather than a proper re-authentication flow.

**Finding DS-03 — Informational: Token Fields Are Public with No Accessor Encapsulation**

In `GetTokenResult`, `value`, `expiration`, `tokenType`, `expired`, and `refreshToken` are all declared `public`. In `RefreshTokenItem`, `value` and `expiration` are also `public`. There is no encapsulation or defensive copying. Any code with a reference to the object can read or mutate the token value directly. This is a code quality observation. Combined with the plaintext storage finding (DS-01), it means token values are both broadly accessible in memory and stored without protection.

---

### Section 4 — Input and Intent Handling

**Finding IIH-01 — Informational: Serializable Result Objects Passed via Intent Risk**

`GetEquipmentResultArray`, `GetTokenResult`, and `JoinCompanyResult` all implement `java.io.Serializable`. Objects implementing `Serializable` are commonly passed as `Intent` extras via `putExtra(String, Serializable)`. If any of these result objects are passed in an implicit Intent or to an exported component (not determinable from these three files alone), their contents would be exposed. The presence of `Serializable` on `GetTokenResult` carrying a live bearer token is a latent risk if the object is ever used as an Intent extra in an exported or implicit context.

Specifically, `EquipmentItem` (contained in `GetEquipmentResultArray.arrayList`) carries `mac_address` and `serial_no` as plaintext string fields. If the list is serialized into an Intent passed to an exported activity, hardware identifiers for fleet equipment would be exposed.

Note: Whether these objects are actually passed via exported Intents requires review of the calling Activities, which are outside this assignment. This finding flags the structural risk arising from the data these classes hold combined with their Serializable implementation.

**Result:** No direct Intent handling is present in the three assigned files. The above is a conditional risk requiring cross-file confirmation.

---

### Section 5 — Authentication and Session

**Finding AS-01 — High: Token Stored in Plain SharedPreferences (cross-reference DS-01)**

As established in DS-01, `GetTokenResult` (containing `value` — the bearer token — and `refreshToken`) is persisted in unencrypted SharedPreferences. This finding applies under both Data Storage and Authentication and Session sections.

**Finding AS-02 — Informational: Token Expiry Field Present But Enforcement Not Verifiable in These Files**

`GetTokenResult` carries an `expiration` integer field and an `expired` boolean field. `RefreshTokenItem` carries an `expiration` field. Whether the application enforces token expiry (re-authenticating before or upon expiry) cannot be determined from the three assigned data classes alone. The data model supports expiry tracking. Enforcement must be verified in the calling layers (`WebData`, `WebApi`, `TokenAuthenticator`).

`TokenAuthenticator` is triggered on HTTP 401 responses and performs a new token fetch — this represents reactive re-authentication rather than proactive expiry-based refresh. If the server does not return a 401 on expiry (e.g., if the token window is large or server-side validation is lenient), the `expired` flag in `GetTokenResult` would never be acted upon by `TokenAuthenticator`.

**Finding AS-03 — Informational: No Evidence of Token Clearance on Logout in These Files**

The three assigned files are result packet/data-transfer objects. They do not contain logout logic. Whether the stored `token_result` key is deleted from SharedPreferences on logout must be confirmed in the logout flow (not part of this assignment). This is noted for completeness per the checklist requirement that logout clears all stored credentials and tokens.

---

### Section 6 — Third-Party Libraries

No dependency declarations are present in the three assigned files. The files import `org.json` (platform), `java.io`, `java.util`, `java.math` (platform), and wildcard imports for sibling packages within the project. No third-party library CVE assessment applicable to these files.

**Result:** No issues found — Third-Party Libraries (not applicable to assigned files).

---

### Section 7 — Google Play and Android Platform

**Finding GP-01 — Informational: Deprecated android.support.annotation Import in TokenAuthenticator**

While `TokenAuthenticator.java` is not one of the three assigned files, it directly uses `GetTokenResult` and was read as context. It imports `android.support.annotation.NonNull` (line 2 of `TokenAuthenticator.java`), which is the legacy Android Support Library namespace. The modern equivalent is `androidx.annotation.NonNull`. This indicates the codebase has not been fully migrated to AndroidX in this area. This is a maintenance and compatibility concern rather than a direct security finding.

The assigned files themselves (`GetEquipmentResultArray`, `GetTokenResult`, `JoinCompanyResult`) use only platform-standard imports (`org.json`, `java.io`, `java.util`, `java.math`) and make no platform API calls that could trigger deprecated API warnings.

**Result:** No API deprecation or platform compliance issues found directly within the three assigned files.

---

## Summary of Findings

| ID | Severity | Section | Description |
|---|---|---|---|
| NS-01 | Critical | Network Security | `FakeX509TrustManager.allowAllSSL()` disables TLS hostname verification and certificate chain validation globally; invoked during `GetTokenResult` refresh |
| DS-01 | High | Data Storage / Authentication | `GetTokenResult` (bearer token + refresh token) serialized to JSON and stored in unencrypted `SharedPreferences` via `ModelPrefs.saveObject()` |
| DS-02 | Low | Data Storage | `GetEquipmentResultArray`, `GetTokenResult`, `JoinCompanyResult` implement `Serializable` without `serialVersionUID`; deserialization brittleness for token recovery |
| DS-03 | Informational | Data Storage | All sensitive fields in `GetTokenResult` and `RefreshTokenItem` are `public` with no accessor encapsulation |
| IIH-01 | Informational | Input / Intent Handling | `Serializable` on `GetTokenResult` (with live token) and `GetEquipmentResultArray` (with hardware identifiers) creates latent risk if used as Intent extras with exported components |
| AS-02 | Informational | Authentication / Session | Token expiry fields present in data model; enforcement in calling layers not verifiable from assigned files |
| AS-03 | Informational | Authentication / Session | No logout token clearance logic in assigned files; must be verified in logout flow |
| GP-01 | Informational | Google Play / Platform | `android.support.annotation` (legacy) used in `TokenAuthenticator` which consumes `GetTokenResult` |

---

## Files Read

| File | Purpose |
|---|---|
| `...results/GetEquipmentResultArray.java` | Assigned file 1 |
| `...results/GetTokenResult.java` | Assigned file 2 |
| `...results/JoinCompanyResult.java` | Assigned file 3 |
| `...webserviceclasses/RefreshTokenItem.java` | Field detail for `GetTokenResult.refreshToken` |
| `...webserviceclasses/WebServiceResultPacket.java` | Superclass of all three assigned result classes |
| `...webserviceclasses/WebServicePacket.java` | Root superclass |
| `...webserviceclasses/EquipmentItem.java` | Element type of `GetEquipmentResultArray.arrayList` |
| `WebService/WebData.java` | Token storage call site |
| `WebService/WebApi.java` | Token issuance and storage trigger |
| `autoupdate/util/TokenAuthenticator.java` | Token refresh path; source of NS-01 |
| `WebService/FakeX509TrustManager.java` | TLS bypass implementation; evidence for NS-01 |
| `model/ModelPrefs.java` | SharedPreferences storage backend; evidence for DS-01 |
