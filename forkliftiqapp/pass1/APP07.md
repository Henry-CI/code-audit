# Pass 1 Security Audit — APP07
**Agent:** APP07
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Audit scope:** WebService layer — JSONObjectParser, URLBuilder, UrlItem

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Checklist states "Branch: main". Actual branch is "master". Discrepancy recorded. Branch is "master" — proceeding.

---

## Step 2 — Reading Evidence

### File 1: JSONObjectParser.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.JSONObjectParser`

**Public methods (signature — line number):**
- `JSONObjectParser(JSONObject object)` — constructor, line 10
- `public String getString(String propertyName) throws JSONException` — line 14
- `public int getInt(String propertyName) throws JSONException` — line 18
- `public long getLong(String propertyName) throws JSONException` — line 22
- `public Boolean getBoolean(String propertyName) throws JSONException` — line 26
- `public JSONArray getJSONArray(String propertyName) throws JSONException` — line 30

**Public fields/constants:** None.

**Android components declared:** None (not an Activity, Fragment, Service, Receiver, or Provider).

---

### File 2: URLBuilder.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.URLBuilder`

**Public fields/constants (with line numbers):**
- `public final static int EQUIPMENT_FRONT = 1` — line 17
- `public final static int EQUIPMENT_LEFT = 2` — line 18
- `public final static int EQUIPMENT_RIGHT = 3` — line 19
- `public final static int EQUIPMENT_BACK = 4` — line 20
- `final static String baseUrl = BuildConfig.BASE_URL` — line 22 (package-private)
- `final static String baseDataUrl = baseUrl + "/rest"` — line 24 (package-private)
- `final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora"` — line 26 (package-private, hardcoded literal)

**Public methods (signature — line number):**
- `public static UrlItem urlSaveSession()` — line 29
- `public static UrlItem urlAbortSession(int sessionId)` — line 36
- `public static UrlItem urlUploadImpactImage(int impactId)` — line 44
- `public static UrlItem urlUploadImpactSignature(int impactId)` — line 55
- `public static UrlItem urlResendReport(int uid, int rid)` — line 66
- `public static UrlItem urlSaveShockEvent()` — line 78
- `public static UrlItem urlUpdateUser(int uid)` — line 86
- `public static UrlItem urlDeleteCompany(int permissionId)` — line 95
- `public static UrlItem urlGetUserDetail(int uid)` — line 104
- `public static UrlItem urlAddEquipment()` — line 113
- `public static UrlItem urlGetEmails(int uid)` — line 122
- `public static UrlItem urlGetEquipmentStatsYearly(int uid)` — line 132
- `public static UrlItem urlGetEquipmentStatsMonthly(int uid)` — line 143
- `public static UrlItem urlGetEquipmentStatsWeekly(int uid)` — line 155
- `public static UrlItem urlSaveImpactPhoto(int impid)` — line 167
- `public static UrlItem urlGetReports(int uid)` — line 179
- `public static UrlItem urlGetDriverStats(int uid)` — line 189
- `public static UrlItem urlSaveService()` — line 199
- `public static UrlItem urlSaveImpact()` — line 208
- `public static UrlItem urlResetPassword()` — line 217
- `public static UrlItem urlGetServiceRecord(int uid)` — line 226
- `public static UrlItem urlGetDiagnosis(int eid)` — line 236
- `public static UrlItem urlGetUniversity(int eid)` — line 244
- `public static UrlItem urlGetFuelType(int mtype, int etype)` — line 253
- `public static UrlItem urlGetEquipmentType(int mtype)` — line 265
- `public static UrlItem urlGetManufacture()` — line 275
- `public static UrlItem urlSaveLicense()` — line 284
- `public static UrlItem urlUserRegister()` — line 294
- `public static UrlItem urlSaveSingleGPSLocation()` — line 303
- `public static UrlItem urlSaveMultipleGPSLocation()` — line 312
- `public static UrlItem urlLogin()` — line 322
- `public static UrlItem urlSetEmails()` — line 331
- `public static UrlItem urlUploadUserPhoto(int userId)` — line 340
- `public static UrlItem urlUploadEquipmentPhoto(int sid, int imageno)` — line 352
- `public static UrlItem urlJoinCompany()` — line 366
- `public static UrlItem urlSearchCompany(String search)` — line 376
- `public static UrlItem urlGetCompanyList(int userId)` — line 388
- `public static UrlItem urlGetEquipmentList(int userId)` — line 398
- `public static UrlItem urlGetCompanyDriversList(int userId)` — line 408
- `public static UrlItem urlGetPreStartQuestions(int equipmentId)` — line 419
- `public static UrlItem urlSavePreStartResult()` — line 429
- `public static UrlItem urlSessionStart()` — line 439
- `public static UrlItem urlSessionEnd()` — line 448
- `public static UrlItem urlGetToken()` — line 457
- `public static String getUrl()` — line 462

**All hardcoded URLs/endpoints/IPs:**

| Location | Value | Protocol |
|---|---|---|
| Line 26, `baseUrlForPreStartHelp` | `https://pandora.fleetiq360.com/pandora` | HTTPS |
| Line 171, commented-out | `https://192.168.1.7/fleetiq360ws/rest` | HTTPS (commented out) |
| Line 355, commented-out | `https://192.168.1.7/fleetiq360ws/rest` | HTTPS (commented out) |
| Line 459, `urlGetToken()` | `baseUrl + "/oauth/token"` | Inherits from `BuildConfig.BASE_URL` |

`baseUrl` itself is sourced from `BuildConfig.BASE_URL` — not a literal. All active (non-commented) URLs that do not inherit `baseUrl` use HTTPS. Commented-out IP references (`192.168.1.7`) are development/local addresses and are inert code.

**Android components declared:** None.

---

### File 3: UrlItem.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.UrlItem`

**Public fields:**
- `public int method` — line 9
- `public String url` — line 10

**Public methods:**
- `public UrlItem(int httpMethod, String webUrl)` — constructor, line 12

**Android components declared:** None.

---

## Step 3 — Security Findings by Checklist Section

### 1. Signing and Keystores

Not applicable to these three files. No keystore references, no `signingConfigs`, no `build.gradle` content, no `gradle.properties` content in scope.

No issues found — Signing and Keystores (out of scope for assigned files).

---

### 2. Network Security

**FINDING NET-01 — Hardcoded production hostname (Low/Informational)**
File: `URLBuilder.java`, line 26
```java
final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora";
```
The hostname `pandora.fleetiq360.com` is a hardcoded literal in source code. The primary base URL (`baseUrl`) correctly uses `BuildConfig.BASE_URL`, which allows per-flavor or per-environment configuration at build time. This secondary URL does not follow the same pattern and cannot be overridden at build time without a code change. If this endpoint changes environment (e.g., from a staging server to a different production server, or if it needs to be parameterised per tenant), it requires a code edit and a new release. This is a maintainability and minor information-disclosure concern (the production hostname is visible in the APK).

This endpoint is used by `urlGetDiagnosis()` (line 236) and `urlGetUniversity()` (line 244) and does use HTTPS — no cleartext transport issue.

**FINDING NET-02 — Commented-out private IP addresses remain in source (Informational)**
File: `URLBuilder.java`, lines 171 and 355
```java
// Uri.Builder builder = Uri.parse("https://192.168.1.7/fleetiq360ws/rest").buildUpon();
```
Two commented-out blocks reference a private LAN IP (`192.168.1.7`) that was clearly used during development. Although commented out and therefore inert at runtime, these indicate that developers previously bypassed the normal URL configuration mechanism by hardcoding a local IP directly. The comments should be removed. More importantly, if the surrounding code were accidentally uncommented (e.g., during a merge conflict resolution), requests would silently fail or redirect to an unintended host. Residual development artifacts of this kind also carry certificate validation risk: if the developer's local server used a self-signed certificate, any `TrustManager` permissiveness that was added to accommodate it may still be present elsewhere in the codebase (outside scope of these files).

**No HTTP (cleartext) URLs found** in active (non-commented) code within these files. All active endpoints inherit from `BuildConfig.BASE_URL` or use the hardcoded `https://` scheme.

**FINDING NET-03 — URL path component not sanitized in urlSearchCompany (Low)**
File: `URLBuilder.java`, line 376–384
```java
public static UrlItem urlSearchCompany(String search)
{
    Uri.Builder builder = Uri.parse(getUrl()).buildUpon();
    builder.appendPath("company");
    builder.appendPath("search");
    builder.appendPath(search);   // caller-supplied string appended directly
    builder.appendPath("");
    return new UrlItem(Request.Method.GET,builder.toString());
}
```
The `search` parameter is appended directly as a URL path segment without null-checking or character sanitization. `Uri.Builder.appendPath()` does perform percent-encoding for most special characters, which mitigates path traversal via the URL, but a null value for `search` will cause a `NullPointerException` at the `appendPath` call, potentially crashing the app. If the caller is a UI input field, there is also no evidence of length limiting in this layer. Input validation should be applied upstream before this method is called. This is a defensive coding concern; the Android `Uri` API encoding provides a degree of protection against URL injection.

No `TrustAllCertificates`, no `hostnameVerifier` overrides, and no `SSLContext` customization exist in any of these three files.

---

### 3. Data Storage

Not directly applicable. These files construct URLs and parse JSON; they do not write to SharedPreferences, SQLite, files, or external storage.

No issues found — Data Storage (out of scope for assigned files).

---

### 4. Input and Intent Handling

**FINDING IIH-01 — urlSearchCompany passes raw caller input into URL path (cross-reference to NET-03)**
As noted above, the `search` string in `urlSearchCompany()` is caller-supplied and receives no validation in this layer. No null guard is present. Assessed Low severity.

No WebView usage, no exported component declarations, and no intent filter definitions exist in these files.

No issues found beyond IIH-01 — Input and Intent Handling.

---

### 5. Authentication and Session

**Observation — Token endpoint construction**
File: `URLBuilder.java`, line 457–459
```java
public static UrlItem urlGetToken()
{
    return (new UrlItem(Request.Method.POST, baseUrl + "/oauth/token"));
}
```
The OAuth token endpoint uses `baseUrl` (from `BuildConfig.BASE_URL`) and POST — appropriate. The actual token handling (storage, expiry, clearing on logout) occurs in calling code outside these files and cannot be assessed here.

No credentials, tokens, or session data are stored or transmitted by any of these three files. These are URL-construction utilities.

No issues found — Authentication and Session (out of scope for assigned files).

---

### 6. Third-Party Libraries

**Observation — Volley usage**
File: `URLBuilder.java`, line 6
```java
import com.android.volley.Request;
```
The Volley library is used for HTTP method constants (`Request.Method.GET`, `Request.Method.POST`, `Request.Method.PUT`). No Volley version information is available in these files; version and CVE status must be assessed from `build.gradle`.

No issues found — Third-Party Libraries (version/CVE assessment out of scope for assigned files).

---

### 7. Google Play and Android Platform

Not applicable to these files. No `targetSdkVersion`, no manifest permissions, no deprecated API usage (e.g., `AsyncTask`) present in these three files.

No issues found — Google Play and Android Platform (out of scope for assigned files).

---

## Summary of Findings

| ID | File | Line(s) | Severity | Title |
|---|---|---|---|---|
| NET-01 | URLBuilder.java | 26 | Low / Informational | Hardcoded production hostname `pandora.fleetiq360.com` not externalised to BuildConfig |
| NET-02 | URLBuilder.java | 171, 355 | Informational | Commented-out development IP `192.168.1.7` left in source |
| NET-03 / IIH-01 | URLBuilder.java | 380 | Low | `urlSearchCompany` appends caller-supplied `search` parameter to URL path with no null-check or validation |

No Critical or High severity findings in these three files.

---

## Notes for Subsequent Passes

- The protocol of `BuildConfig.BASE_URL` (HTTP vs HTTPS) must be verified in `build.gradle` and any associated flavor configurations — this determines whether the primary API base URL is cleartext or encrypted.
- Any `TrustManager` / `HostnameVerifier` customization that may have been added to support the development IP (`192.168.1.7`) must be searched for in the broader network client code (Volley setup, OkHttp configuration) outside this file set.
- Volley library version and CVE status to be assessed from `build.gradle` (not in scope here).
- Token storage and session clearing behavior (AUTH sections 5) to be assessed from calling Activities and SharedPreferences usage outside this file set.
