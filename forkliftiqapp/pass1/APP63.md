# Pass 1 Security Audit — APP63
**Agent ID:** APP63
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Files reviewed:**
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/util/ComplianceAccepter.java`
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/util/ServerDateFormatter.java`

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist header states `Branch: main`. The actual default branch is `master`. Audit proceeds on `master` as instructed.

---

## Reading Evidence

### File 1: `ComplianceAccepter.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.util.ComplianceAccepter`

**Fields:**
| Name | Type | Line |
|------|------|------|
| `context` | `Context` (private instance) | 20 |
| `user` | `User` (private instance) | 21 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `ComplianceAccepter(Context context)` (constructor) | 23 |
| `void askForCompliance()` | 28 |

**Android components declared:** None (utility class, no Activity/Fragment/Service/Receiver).

**Key behaviour of `askForCompliance()` (lines 28–52):**
- If `user.complianceIsValid()` returns `true`, the method returns immediately (line 29).
- Otherwise an `AlertDialog` is built with two buttons:
  - **Accept (line 34):** calls `user.updateCompliance(Calendar.getInstance().getTime())` then fires `WebApi.async().updateUser(...)` with a bare default `new WebListener<CommonResult>()` — i.e. the update call has no success or failure handler overrides; both `onSucceed` and `onFailed` are no-ops in the base `WebListener` class.
  - **Refuse (line 43):** calls `WebData.instance().logout()` and redirects to `LoginActivity`.

---

### File 2: `ServerDateFormatter.java`

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.util.ServerDateFormatter`

**Fields:**
| Name | Type | Line |
|------|------|------|
| `dateFormat` | `SimpleDateFormat` (private instance) | 10 |
| `dateTimeFormat` | `SimpleDateFormat` (private instance) | 11 |

**Public methods:**
| Signature | Line |
|-----------|------|
| `ServerDateFormatter()` (constructor) | 13 |
| `String formatDate(Date date)` | 21 |
| `String formatDateTime(Date date)` | 25 |
| `Date parseDate(String date)` | 29 |
| `Date parseDateTime(String date)` | 34 |

**Key behaviour:**
- Constructor (lines 14–19): creates two `SimpleDateFormat` instances anchored to `Locale.US` and `GMT` timezone. Formats: `yyyy-MM-dd` and `yyyy-MM-dd HH:mm:ss`.
- `parseDate` (line 29–31): guards against `null`/empty string, returns `null` in those cases; uses `ParsePosition(0)`.
- `parseDateTime` (line 34–36): no null guard; passes `null` string directly to `dateTimeFormat.parse()` — will throw `NullPointerException`.

**Android components declared:** None.

---

## Supporting Evidence (read to establish storage and credential context)

To fully evaluate the checklist items for `ComplianceAccepter`, the following supporting classes were read:

- **`User.java`** — `complianceIsValid()` (line 78) checks only `complianceDate != null`. `getPassword()` is public (line 135). `password` is stored as a plain `String` field. `updateCompliance()` calls `UserDb.save(this)` (line 107).
- **`CurrentUser.java`** — compliance date is populated from the login API response field `loginItem.compliance_date` (line 76). Static fields `loginEmail`, `loginPassword` hold credentials in memory (lines 22–23). `logout()` clears the `CURRENT_USER_ID_KEY` from SharedPreferences and nulls the static `user` field, but does **not** clear `loginEmail` or `loginPassword` static fields.
- **`UserDb.java`** — all persistence goes through Realm (unencrypted by default unless a Realm encryption key is configured separately). Passwords are queried in plaintext in `get(email, password)` (line 59).
- **`ModelPrefs.java`** — uses plain `SharedPreferences` (`MODE_PRIVATE`) without `EncryptedSharedPreferences`. The `current_user_id` integer is stored here.
- **`UserRealmObject.java`** — `password` is stored as a plain `String` field (line 15) in the Realm database.
- **`WebListener.java`** — `onSucceed` and `onFailed` are both empty no-ops in the base class (lines 11, 13).

---

## Section-by-Section Findings

### 1. Signing and Keystores
Not within scope of the two assigned files. No issues found in these files — Section 1.

### 2. Network Security
**Finding — Medium — No error handling on compliance server update (fire-and-forget).**
`ComplianceAccepter.java` line 40:
```java
WebApi.async().updateUser(user.getId(), parameter, new WebListener<CommonResult>());
```
The `WebListener` passed is a bare base-class instance. `onSucceed` and `onFailed` are both empty no-ops (confirmed in `WebListener.java` lines 11, 13). If the server-side `updateUser` call fails (network error, server error, HTTP 5xx), the failure is silently discarded. The local Realm record is already written (`UserDb.save` called inside `updateCompliance` at `User.java` line 107) before the API call, so the device considers compliance accepted even when the server did not record it. Conversely, if the app crashes or is killed between the local write and the API call completing, the server and device may be permanently out of sync. In either direction this undermines the integrity of GDPR compliance records.

**Finding — Low — `parseDateTime` in ServerDateFormatter lacks null guard.**
`ServerDateFormatter.java` line 34–36:
```java
public Date parseDateTime(String date) {
    return dateTimeFormat.parse(date, new ParsePosition(0));
}
```
`parseDate` (line 29) guards against `null` and empty string before calling `parse`. `parseDateTime` has no such guard. Passing `null` as `date` causes `SimpleDateFormat.parse(null, ...)` to throw a `NullPointerException` at runtime. This is an inconsistency that could cause an unhandled crash if the server returns a missing datetime field for any object that routes through `parseDateTime`. Not a direct security vulnerability, but it creates an availability risk (crash) and could potentially be reached by a malformed server response.

### 3. Data Storage
**Finding — High — User password stored in plaintext in Realm database.**
Established through the chain: `User.java` field `password` (line 17) → `UserRealmObject.java` field `password` (line 15) → `UserDb.save()` writes to Realm. `ComplianceAccepter.java` calls `user.updateCompliance()` → `UserDb.save(this)` which persists the full `User` object including `password`. Realm databases are stored in the app's data directory; without a Realm encryption key the database file is readable on rooted devices or via ADB backup (if `android:allowBackup` is `true`). This is a pre-existing storage vulnerability, and `ComplianceAccepter`'s persistence path confirms it is exercised during compliance acceptance.

**Finding — Medium — Compliance state is determined solely by a non-null local date value.**
`User.complianceIsValid()` (line 78 of `User.java`) returns `true` if `complianceDate != null`. This value is written locally by `ComplianceAccepter` upon the user tapping "Accept", with no server-side confirmation (see Section 2 finding above). An attacker or a developer with ADB access to the Realm database on a rooted device could write any non-null date value to `complianceDate`, causing `complianceIsValid()` to return `true` and bypassing the compliance prompt entirely. There is no server-side re-validation of the stored compliance date on subsequent logins against the live API response (the value comes from `loginItem.compliance_date` only on login, so a legitimate user who refuses compliance on device A and then logs in on device B where a manipulated record exists could bypass it). The compliance check is client-side only.

**Finding — Medium — `loginEmail` and `loginPassword` static fields not cleared on logout.**
`CurrentUser.logout()` (lines 125–128 of `CurrentUser.java`) calls `ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY)` and sets `user = null`, but does not null out the static `loginEmail` or `loginPassword` fields (lines 22–23). These persist in JVM memory for the lifetime of the process after logout. On a multi-operator device (shift changes), the previous operator's credentials remain accessible in static memory until the process is killed. This relates directly to the compliance flow because `ComplianceAccepter` is invoked post-login while these credentials are live.

**Finding — Informational — Plain SharedPreferences used for `current_user_id`.**
`ModelPrefs.getPref()` (line 17 of `ModelPrefs.java`) opens preferences with `Context.MODE_PRIVATE` (not `EncryptedSharedPreferences`). The value stored under `current_user_id` is only an integer ID, so the direct sensitivity is low; however the pattern is inconsistent with the checklist recommendation for `EncryptedSharedPreferences` and could become a risk if sensitive keys are added later.

### 4. Input and Intent Handling
`ComplianceAccepter` and `ServerDateFormatter` do not register or handle Intents, deep links, or WebViews. No issues found in these files — Section 4.

### 5. Authentication and Session
**Finding — see Section 3 above — `loginPassword` not cleared on logout.** The static credential fields in `CurrentUser` outlive the session.

**Finding — Medium — Compliance bypass possible via direct database manipulation.** `complianceIsValid()` is a purely local, client-side check against a stored date. There is no cryptographic proof of acceptance, no server-issued token, and no re-verification against the server response on subsequent sessions. A user with root access or ADB backup access can write a non-null date to the Realm record for `complianceDate` and bypass the GDPR acceptance dialog.

### 6. Third-Party Libraries
`ServerDateFormatter.java` uses only `java.text.SimpleDateFormat`, `java.util.Date`, `java.util.Locale`, and `java.util.TimeZone` from the Java standard library. No third-party library concerns for these two files. No issues found — Section 6.

### 7. Google Play and Android Platform
`ServerDateFormatter` uses `SimpleDateFormat` which is not thread-safe. The class creates new instances per object instantiation (not a static shared instance), so concurrent calls across multiple threads would each have their own instance — no thread-safety issue introduced by this pattern. No deprecated API or permission issues identified in the two assigned files. No issues found — Section 7.

---

## Summary of Findings

| # | Severity | File | Description |
|---|----------|------|-------------|
| 1 | High | `ComplianceAccepter.java` / `User.java` / `UserRealmObject.java` | User password stored in plaintext in unencrypted Realm database; exercised by `UserDb.save(this)` called from `updateCompliance()` |
| 2 | Medium | `ComplianceAccepter.java` | Compliance update to server is fire-and-forget (`new WebListener<CommonResult>()` with no-op callbacks); server failures silently discarded; local state and server state can diverge permanently |
| 3 | Medium | `ComplianceAccepter.java` / `User.java` | Compliance check is client-side only (`complianceDate != null`); no non-null date value is accepted; manipulating the local Realm record bypasses GDPR acceptance |
| 4 | Medium | `CurrentUser.java` | `logout()` does not clear static `loginEmail` / `loginPassword` fields; previous operator's credentials persist in memory across shift changes |
| 5 | Low | `ServerDateFormatter.java` | `parseDateTime()` lacks null guard present in `parseDate()`; null input causes `NullPointerException` at runtime |
| 6 | Informational | `ModelPrefs.java` | Plain `SharedPreferences` (not `EncryptedSharedPreferences`) used for `current_user_id`; low direct risk but inconsistent with security best practice |

---

## Branch Discrepancy Record

The checklist header specifies `Branch: main`. The repository default branch is `master`. Audit was performed on `master` as that is the branch present and confirmed by `git branch --show-current`. No other branch was checked out or examined.
