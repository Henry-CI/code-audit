# Pass 1 Security Audit — Agent APP21

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`. The actual branch is `master`. Proceeding on `master` as instructed.

---

## Step 2 — Checklist Read

Full checklist read from `/c/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-forkliftiqapp.md`. Sections reviewed: Signing and Keystores, Network Security, Data Storage, Input and Intent Handling, Authentication and Session, Third-Party Libraries, Google Play and Android Platform.

---

## Step 3 — Assigned Files Read In Full

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveLicenseParameter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveMultipleGPSParameter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SavePreStartParameter.java`

Supporting files also read for full context:
- `WebServiceParameterPacket.java` (parent class)
- `SaveGPSLocationItem.java` (field type in SaveMultipleGPSParameter)
- `AnswerItem.java` (field type in SavePreStartParameter)
- `WebApi.java` (callers of all three parameter classes)
- `URLBuilder.java` (endpoint construction)
- `PreStartCheckListPresenter.java` (SavePreStartParameter population site)
- `CurrentUser.java` (SaveLicenseParameter field origin)
- `User.java` (field model for licence data)
- `UserDb.java` / `UserRealmObject.java` (persistence of licence/security fields)
- `ModelPrefs.java` (SharedPreferences wrapper)
- `SessionDb.java` (pre-start offline serialisation)
- `SyncService.java` (GPS sync caller)

---

## Step 4 — Reading Evidence

### File 1: `SaveLicenseParameter.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveLicenseParameter`

**Superclass:** `WebServiceParameterPacket` (which extends `WebServicePacket`) — implements `Serializable`

**Fields (all public):**
| Line | Field | Type |
|------|-------|------|
| 14 | `id` | `int` |
| 15 | `licno` | `String` |
| 16 | `addr` | `String` |
| 17 | `expirydt` | `String` |
| 18 | `securityno` | `String` |

**Public methods:**
| Line | Signature |
|------|-----------|
| 20 | `SaveLicenseParameter()` — default constructor |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders.**

**Caller in WebApi.java (line 333-335):**
```java
public void saveLicense(SaveLicenseParameter parameter, final WebListener<SaveLicenseResult> resultListener) {
    enqueueRequest(new GsonRequest<>(URLBuilder.urlSaveLicense(), parameter, SaveLicenseResult.class, resultListener));
}
```
Endpoint: `{BASE_URL}/rest/licence/save` — POST.

---

### File 2: `SaveMultipleGPSParameter.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SaveMultipleGPSParameter`

**Superclass:** `WebServiceParameterPacket` — implements `Serializable`

**Fields (all public):**
| Line | Field | Type |
|------|-------|------|
| 10 | `gpsList` | `ArrayList<SaveGPSLocationItem>` |

Each `SaveGPSLocationItem` carries: `unit_id` (int), `longitude` (Double), `latitude` (Double), `gps_time` (String).

**Public methods:**
| Line | Signature |
|------|-----------|
| 12 | `SaveMultipleGPSParameter()` — initialises `gpsList` as empty `ArrayList` |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders.**

**Caller in WebApi.java (line 345-347):**
```java
public void saveMultipleGPSLocation(SaveMultipleGPSParameter parameter, final WebListener<SaveMultipleGPSResult> resultListener) {
    enqueueRequest(new GsonRequest<>(URLBuilder.urlSaveMultipleGPSLocation(), parameter, SaveMultipleGPSResult.class, resultListener));
}
```
Endpoint: `{BASE_URL}/rest/gps/save/all` — POST.

Also referenced in `SyncService.java` and `LocationDb.java` for offline GPS sync.

---

### File 3: `SavePreStartParameter.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters.SavePreStartParameter`

**Superclass:** `WebServiceParameterPacket` — implements `Serializable`

**Fields (all public):**
| Line | Field | Type |
|------|-------|------|
| 14 | `start_time` | `String` |
| 15 | `finish_time` | `String` |
| 16 | `comment` | `String` |
| 17 | `session_id` | `int` |
| 18 | `arrAnswers` | `ArrayList<AnswerItem>` |

Each `AnswerItem` carries: `question_id` (int), `answer` (String).

**Public methods:**
| Line | Signature |
|------|-----------|
| 20 | `SavePreStartParameter()` — default constructor |

**No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders.**

**Callers:**
- `WebApi.java` (line 226-233): `savePreStartResult()` — POST to `{BASE_URL}/rest/result/save`; on success also calls `SessionDb.setSessionPreStartFinished()`.
- `PreStartCheckListPresenter.java` (line 61-66): populates all fields from `WebData` session result and user-supplied answers/comments.
- `SessionDb.java` (line 87, 408): serialises and deserialises the parameter object as a JSON string in the Realm database for offline deferral.

---

## Step 5 — Findings by Checklist Section

### 1. Signing and Keystores

These are pure parameter DTO (data-transfer object) classes with no signing or keystore logic. No `.jks`, `.keystore`, or `signingConfig` material is present in these files.

**No issues found — Signing and Keystores**

---

### 2. Network Security

**Finding N1 — Medium: `securityno` field transmitted without explicit transport-layer verification in scope of these files**

`SaveLicenseParameter.securityno` is a government-issued licence security number (a PII/credential-equivalent field). It is serialised by Gson and transmitted via `GsonRequest` to `{BASE_URL}/rest/licence/save` as a POST body. The base URL is resolved from `BuildConfig.BASE_URL` (confirmed in `URLBuilder.java` line 22), which is a build-config injection and not hardcoded here — this is correct practice. However, whether the resolved URL is HTTPS in all build variants is not determinable from these files alone and should be verified at the `build.gradle` / `BuildConfig` level.

The GPS coordinate payload (`SaveMultipleGPSParameter`) and pre-start checklist answers (`SavePreStartParameter`) are similarly transmitted via the same `GsonRequest` mechanism. The transport security of the base URL governs all three.

**Note:** A commented-out line in `URLBuilder.java` (line 171) references a private IP address `https://192.168.1.7/fleetiq360ws/rest` that was previously used for development. This comment is benign as a comment but is evidence of a prior development endpoint hardcode that was not fully removed. This is low severity in its current state (code comment only) but indicates the pattern of swapping endpoints exists.

**No other network security issues found within these three files specifically — the base URL mechanism is appropriately externalised to BuildConfig.**

---

### 3. Data Storage

**Finding D1 — High: `securityno` (government ID security number) and `licno` (licence number) persisted in unencrypted Realm database**

The field `SaveLicenseParameter.securityno` mirrors the `securityNumber` field in `User.java`. Tracing the data flow:

1. `LoginItem` (from server response) populates `securityno` into `User` via `CurrentUser.createUser()` (`CurrentUser.java` line 71).
2. `User` is persisted to Realm via `UserDb.save()` → `UserRealmObject` (`UserRealmObject.java` lines 42-43: fields `securityNumber` and `licenseNumber` stored in plain Realm).
3. When the operator edits their licence, `User.updateLicense()` (`User.java` line 97) updates these fields and calls `UserDb.save()` again.
4. The operator's `SaveLicenseParameter` (containing `securityno`, `licno`, `addr`, `expirydt`) is then assembled from these stored values and POSTed to the server.

Realm is not encrypted by default in this codebase. No Realm encryption key configuration was observed. The `securityNumber` (a government-issued credential-equivalent) and `licenseNumber` are therefore at rest in plaintext in the Realm database file on the device.

**Finding D2 — High: `password` stored in unencrypted Realm database**

`UserRealmObject.java` stores `password` as a plain `String` field in Realm (line 15). `UserDb.save()` persists it. `UserDb.get(email, password)` queries it for offline login (line 59). This is outside the strict scope of the three assigned files but is directly connected to the `SaveLicenseParameter` data flow (same `User` object stores both the password and the `securityno`/`licno` fields). Flagged here as contextual evidence that the unencrypted Realm database is the central risk.

**Finding D3 — Medium: `SavePreStartParameter` serialised as plaintext JSON in Realm for offline deferral**

`SessionDb.setSessionPreStartFinished()` (`SessionDb.java` line 408) serialises the entire `SavePreStartParameter` object — including `session_id`, `start_time`, `finish_time`, `comment`, and all `AnswerItem` answer strings — using `GsonHelper.stringFromObjectNoPolicy()` and stores the result as a plain string field (`preStartResults`) in the Realm database. This means pre-start check answers (which may include safety-relevant responses) are stored at rest in plaintext.

**No issues found — external storage (`Environment.getExternalStorageDirectory()`)**: Not present in these files.
**No issues found — `MODE_WORLD_READABLE` / `MODE_WORLD_WRITEABLE`**: Not present in these files.

---

### 4. Input and Intent Handling

These three files are pure data-transfer objects (parameter packets). They contain no Activity, Fragment, Service, BroadcastReceiver, or ContentProvider declarations. They handle no intents, deep links, or WebView operations. All field assignments observed at call sites (`PreStartCheckListPresenter.java`, `WebApi.java`) come from authenticated session state (`WebData.instance().getSessionResult()`) or UI-supplied values (comments, answers) without additional sanitisation at the DTO layer.

**Observation — No input sanitisation on `comment` or `answer` fields in `SavePreStartParameter`:** The `comment` field (populated from UI text in `PreStartCheckListPresenter.java` line 58) and each `AnswerItem.answer` string are passed directly into the parameter object without length limits, encoding validation, or sanitisation. Depending on server-side handling, this could be relevant for injection risk on the backend. Within the Android client these are string fields with no obvious client-side risk beyond this.

**No issues found — Exported components, WebView, deep links (not applicable to these files)**

---

### 5. Authentication and Session

**Finding A1 — Medium: `SaveLicenseParameter` fields are populated from `User` object which caches credentials beyond login session**

`User.getSecurityNumber()` and `User.getLicenseNumber()` return values that are cached in the in-memory `CurrentUser.user` static field (`CurrentUser.java` line 21) for the lifetime of the app process. Additionally these values are persisted to the unencrypted Realm database (see D1). The `securityno` field in `SaveLicenseParameter` originates from this static cache.

**Finding A2 — Medium: Logout does not clear Realm-persisted licence/security data**

`CurrentUser.logout()` (`CurrentUser.java` lines 125-128) clears only `ModelPrefs` key `current_user_id` and nulls the in-memory `user` reference. It does not call `UserDb` to delete or wipe the `UserRealmObject` record containing `licenseNumber`, `securityNumber`, and `password`. On a shared-device deployment (shift changes between operators), the previous operator's data remains in the Realm database and can be retrieved by querying by email/password.

**No issues found — Token expiry / re-authentication (not present in these files)**

---

### 6. Third-Party Libraries

These three files import only Java standard library (`java.io.Serializable`, `java.util.ArrayList`, `java.math.BigDecimal`) and Android's `org.json` package. No third-party library dependencies are declared or used within these files themselves.

**No issues found — Third-Party Libraries (within scope of these files)**

---

### 7. Google Play and Android Platform

These files are plain Java classes (DTOs). They declare no Android platform components and use no Android APIs directly. No deprecated API usage (`AsyncTask`, `startActivityForResult`, etc.) is present.

The `Serializable` interface is implemented on all three classes and their parent `WebServiceParameterPacket`. `Serializable` objects can be passed via `Intent` extras. If `SaveLicenseParameter` were ever passed via an Intent to an exported component, the `securityno` field would be exposed. No such Intent usage was observed in the current call sites reviewed.

**No issues found — Google Play and Android Platform (within scope of these files)**

---

## Summary of Findings

| ID | Severity | Section | Finding |
|----|----------|---------|---------|
| D1 | High | Data Storage | `securityno` (government ID security number) and `licno` (operator licence number) from `SaveLicenseParameter` are persisted at rest in the unencrypted Realm database via `UserRealmObject`. |
| D2 | High | Data Storage | Operator `password` is stored in the same unencrypted Realm database (directly connected to the licence data flow). |
| A2 | Medium | Authentication and Session | `CurrentUser.logout()` does not delete Realm-persisted `UserRealmObject` records. Licence number, security number, and password of a previous operator remain on-device after logout, creating a risk on shared devices. |
| D3 | Medium | Data Storage | `SavePreStartParameter` (pre-start check answers and timing) is serialised as a plaintext JSON string in Realm for offline deferral. |
| A1 | Medium | Authentication and Session | Licence/security fields are cached in a static `CurrentUser.user` field for the process lifetime and sourced from unencrypted Realm. |
| N1 | Low-Medium | Network Security | A commented-out private IP development endpoint remains in `URLBuilder.java` line 171. Not active, but indicates prior practice of endpoint hardcoding. Verify BUILD_URL value in all build variants resolves to HTTPS. |

---

*Report generated by Agent APP21 — 2026-02-27*
