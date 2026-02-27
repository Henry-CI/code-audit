# Pass 1 Security Audit — APP61
**Agent:** APP61
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android / Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

DISCREPANCY: The checklist states `Branch: main`. The actual branch is `master`. Proceeding — branch is `master` as expected per the task brief.

---

## Step 2 — Checklist Consulted

Full checklist read from:
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

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/CurrentUser.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/User.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/UserDb.java`

Supporting files read for context (not assigned, referenced only as evidence):
- `user/UserRealmObject.java`
- `util/CommonFunc.java`
- `model/ModelPrefs.java`
- `model/SafeRealm.java`
- `ui/application/MyApplication.java`
- `WebService/WebData.java`

---

## Step 4 — Reading Evidence

### CurrentUser.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.user.CurrentUser`

**Fields / constants:**
| Name | Type | Modifier | Line |
|---|---|---|---|
| `CURRENT_USER_ID_KEY` | `String` | `private static final` | 19 |
| `user` | `User` | `private static` | 21 |
| `loginEmail` | `String` | `private static` | 22 |
| `loginPassword` | `String` | `private static` | 23 |
| `training` | `List<TrainingItem>` | `private static` | 24 |

**Public methods:**
| Signature | Line |
|---|---|
| `public static User get()` | 26 |
| `public static void setUser(User newUser)` | 32 |
| `public static void setUser(LoginItem loginItem)` | 37 |
| `public static List<TrainingItem> getTrainingList()` | 53 |
| `public static void login(final LoginHandler handler)` | 80 |
| `public interface LoginHandler` (inner) | 114 |
| `public static void setTemporaryLoginInformation(String email, String password)` | 120 |
| `public static void logout()` | 125 |

**Private methods:**
| Signature | Line |
|---|---|
| `private static void setUserTraining(List<TrainingItem> newTraining)` | 48 |
| `private static User createUser(LoginItem loginItem)` | 58 |

---

### User.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.user.User`

**Fields:**
| Name | Type | Modifier |
|---|---|---|
| `id` | `int` | `private` |
| `companyId` | `int` | `private` |
| `firstName` | `String` | `private` |
| `lastName` | `String` | `private` |
| `email` | `String` | `private` |
| `password` | `String` | `private` |
| `phoneNumber` | `String` | `private` |
| `licenseNumber` | `String` | `private` |
| `expiryDate` | `Date` | `private` |
| `address` | `String` | `private` |
| `securityNumber` | `String` | `private` |
| `photoUrl` | `String` | `private` |
| `isContactPerson` | `boolean` | `private` |
| `dateFormat` | `String` | `private` |
| `maxSessionLength` | `int` | `private` |
| `complianceDate` | `Date` | `private` |
| `gps_frequency` | `int` | `private` |

**Constructor:**
`User(int id, int companyId, String firstName, String lastName, String email, String password, String phoneNumber, String licenseNumber, Date expiryDate, String address, String securityNumber, String photoUrl, boolean isContactPerson, String dateFormat, int maxSessionLength, Date complianceDate, int gpsFrequency)` — package-private, line 30.

**Public methods:**
| Signature | Line |
|---|---|
| `public String fullName()` | 66 |
| `public String definedName()` | 70 |
| `public boolean complianceIsValid()` | 78 |
| `public boolean hasAssociatedDrivers()` | 82 |
| `public List<User> associatedDrivers()` | 86 |
| `public void updateInformation(String firstName, String lastName, String complianceDate)` | 90 |
| `public void updateLicense(String licenseNumber, String securityNumber, String address, String expiryDate)` | 97 |
| `public void updateCompliance(Date complianceDate)` | 105 |
| `public int getId()` | 115 |
| `public int getCompanyId()` | 119 |
| `public String getFirstName()` | 123 |
| `public String getLastName()` | 127 |
| `public String getEmail()` | 131 |
| `public String getPassword()` | 135 |
| `public String getLicenseNumber()` | 143 |
| `public Date getExpiryDate()` | 147 |
| `public String getAddress()` | 151 |
| `public String getSecurityNumber()` | 155 |
| `public String getPhotoUrl()` | 159 |
| `public boolean isContactPerson()` | 163 |
| `public String getDateFormat()` | 167 |
| `public int getMaxSessionLength()` | 171 |
| `public int getGps_frequency()` | 175 |
| `public Date getComplianceDate()` | 179 |

**Package-private methods:**
| Signature | Line |
|---|---|
| `String getPhoneNumber()` | 139 |
| `void setPassword(String password)` | 110 |

---

### UserDb.java
**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.user.UserDb`

**Public methods:**
| Signature | Line |
|---|---|
| `public static void save(final User user)` | 13 |
| `public static ArrayList<String> userEmails()` | 32 |
| `public static User get(final int id)` | 45 |
| `public static User get(final String email, final String password)` | 55 |

**Package-private methods:**
| Signature | Line |
|---|---|
| `static List<User> driversOfCompany(final int companyId)` | 65 |

**Storage backend:** Realm (no-SQL embedded database). Uses `SafeRealm` wrapper. No encryption key passed to `RealmConfiguration` (confirmed via `MyApplication.java` lines 68–72).

---

## Step 5 — Findings by Checklist Section

### Section 1 — Signing and Keystores
These files contain no signing configuration, keystore references, or build configuration. No issues within scope of assigned files.

---

### Section 2 — Network Security
These files contain no HTTP client configuration, URL construction, or SSL handling. No issues within scope of assigned files.

**Out-of-scope observation (noted for completeness — found in `WebData.java` line 68, not an assigned file):** The method `getTokenFormData()` contains hardcoded OAuth `client_id`, `client_secret`, `username`, and `password` values in plaintext. This is a High finding but falls outside the three assigned files and is flagged only for cross-agent awareness.

---

### Section 3 — Data Storage

**FINDING 3-A — CRITICAL: Plaintext password stored in Realm without encryption**

`User.java` carries a `password` field (line 17). `UserDb.save()` (line 13) persists this object into Realm via `UserRealmObject`, which also has a `password` field (line 15 of `UserRealmObject.java`). The `RealmConfiguration` in `MyApplication.initDataBase()` (lines 68–72) does not set an encryption key:

```java
RealmConfiguration config = new RealmConfiguration.Builder()
        .schemaVersion(4)
        .deleteRealmIfMigrationNeeded()
        .build();
```

Realm stores its database as a `.realm` file in the app's data directory. Without `encryptionKey(byte[])` in `RealmConfiguration`, the entire database — including operator passwords — is written to disk in plaintext. Any attacker with physical access to the device and ADB or a rooted device can extract this file and read credentials directly.

Affected lines:
- `UserDb.java` line 13 (`save`), line 59 (password equality query)
- `User.java` line 17 (`password` field), line 110 (`setPassword`)
- `UserRealmObject.java` line 15 (`password` field)
- `MyApplication.java` lines 68–72 (no `encryptionKey`)

**FINDING 3-B — HIGH: Password used as a query predicate in Realm, stored as plaintext**

`UserDb.get(String email, String password)` at line 55–63 queries Realm with `equalTo("password", password)`. This means the password value stored in Realm must be in exactly the same form as the password passed in at query time. Tracing the call chain:

- `CurrentUser.login()` (line 90): after successful server login, calls `get().setPassword(loginPassword)` where `loginPassword` was set by `setTemporaryLoginInformation()` (line 122) as `CommonFunc.MD5_Hash(password)`. So the MD5 hash is stored.
- On offline fallback (line 103): `UserDb.get(loginEmail, loginPassword)` is called, where `loginEmail` is the plain email and `loginPassword` is the MD5 hash. This is consistent.

However, MD5 is a cryptographically broken hash function (collision attacks known since 2004; preimage resistance is insufficient for passwords). MD5 without a salt provides no meaningful protection against offline dictionary or rainbow-table attacks. The credential is effectively recoverable from the Realm file.

Affected lines:
- `CurrentUser.java` line 122 (`MD5_Hash` applied to password)
- `CurrentUser.java` lines 83, 90, 103 (MD5 hash used in login flow)
- `CommonFunc.java` line 68 (`MD5_Hash` implementation)
- `UserDb.java` line 59 (stored hash used as query filter)

**FINDING 3-C — HIGH: Operator credentials held in static fields that survive across operator sessions**

`CurrentUser` holds four `private static` fields that are process-lifetime singletons:
- `user` (line 21) — the full `User` object including password
- `loginEmail` (line 22)
- `loginPassword` (line 23) — the MD5 hash
- `training` (line 24)

`CurrentUser.logout()` (lines 125–128) clears only `user` and the `CURRENT_USER_ID_KEY` SharedPreferences entry:

```java
public static void logout() {
    ModelPrefs.deleteDataForKey(CURRENT_USER_ID_KEY);
    user = null;
}
```

`loginEmail` and `loginPassword` are NOT nulled on logout. In a shared-device scenario (shift changes between operators), the previous operator's MD5-hashed password and email remain in static memory until `setTemporaryLoginInformation()` is called again for the next login attempt. If the app process is not killed between operators, those values persist.

Additionally, `training` is never cleared on logout (line 24 initialised as an `ArrayList`, not nulled in `logout()`). Training data for the previous operator therefore persists in memory for the next operator's session.

Affected lines:
- `CurrentUser.java` lines 21–24 (static field declarations)
- `CurrentUser.java` lines 125–128 (`logout()` does not clear `loginEmail`, `loginPassword`, or `training`)

**FINDING 3-D — MEDIUM: Current user ID persisted in unencrypted SharedPreferences**

`CurrentUser.setUser(User)` at line 34 calls `ModelPrefs.saveInt(CURRENT_USER_ID_KEY, user.getId())`. `ModelPrefs.getPref()` (line 17 of `ModelPrefs.java`) uses `Context.MODE_PRIVATE` plain `SharedPreferences`. This is not `EncryptedSharedPreferences`. The stored user ID is not a secret credential, but it is used on next launch to reconstitute the current user from Realm without re-authentication (`CurrentUser.get()` line 28), meaning a persisted user ID could be manipulated on a rooted device to load a different user's profile. Severity is Medium given the ID is not a credential in isolation but enables session pre-loading without authentication.

Affected lines:
- `CurrentUser.java` lines 19, 28, 34, 126
- `ModelPrefs.java` line 17

---

### Section 4 — Input and Intent Handling
These files contain no Activity, Fragment, BroadcastReceiver, Intent, or WebView code. No issues within scope of assigned files.

---

### Section 5 — Authentication and Session

**FINDING 5-A — HIGH: Password stored and transmitted as unsalted MD5 hash**

Already detailed in Finding 3-B. From an authentication standpoint: `CurrentUser.setTemporaryLoginInformation()` (line 120–123) converts the user-typed password to an MD5 hash client-side before it is ever sent to the server:

```java
public static void setTemporaryLoginInformation(String email, String password) {
    loginEmail = email;
    loginPassword = CommonFunc.MD5_Hash(password);
}
```

At line 83, `loginParameter.password = loginPassword` (the MD5 hash) is sent to `forkliftiqws`. This means:
1. The server receives and validates an MD5 hash, not the raw password. The server is therefore treating the hash as the password equivalent, which means the hash is itself the authenticating credential.
2. Anyone who extracts the MD5 hash from the Realm database (Finding 3-A) can replay it directly to the server without cracking it — a pass-the-hash attack.

**FINDING 5-B — MEDIUM: Logout does not clear loginEmail and loginPassword static fields**

Already detailed in Finding 3-C. From an authentication/session perspective: the `logout()` method is insufficient for a full session teardown. An operator who logs out does not have their credential material removed from process memory. The `training` list also persists across sessions.

**FINDING 5-C — LOW: Offline fallback authentication uses locally stored MD5 hash with no lockout**

`CurrentUser.login()` lines 98–110: when the server is unreachable (or returns HTTP 502), the app falls back to `UserDb.get(loginEmail, loginPassword)` — matching against the locally stored MD5 hash. There is no evidence of failed-attempt counting, lockout, or rate limiting in this path. An attacker with device access could attempt offline brute-force or dictionary attacks against the local Realm without server-side controls applying.

**FINDING 5-D — INFORMATIONAL: loginItem.password passed from server response into User object**

`CurrentUser.createUser()` (lines 58–78) includes `loginItem.password` as a constructor argument to `User`. This means the server login response includes the password field in its JSON payload, and the client stores it. Whether this is a plaintext password or a hash depends on the server implementation (outside scope), but the client unconditionally stores whatever the server sends in the `password` field of the Realm record and in-memory `User` object. If the server returns the actual password, this compounds Finding 3-A significantly.

---

### Section 6 — Third-Party Libraries
These files import Realm (`io.realm`) and reference `WebApi`, `WebListener`, `WebResult`, and `ModelPrefs`. No direct dependency versions are declared in these source files. Version audit is a build.gradle concern and outside the scope of these three files.

No issues within scope of assigned files.

---

### Section 7 — Google Play and Android Platform
These files contain no manifest declarations, SDK version configuration, permission requests, or deprecated API usage directly. No issues within scope of assigned files.

---

## Summary of Findings

| ID | Severity | File(s) | Description |
|---|---|---|---|
| 3-A | CRITICAL | `UserDb.java`, `UserRealmObject.java`, `MyApplication.java` | Realm database has no encryption key — operator passwords written to disk in plaintext |
| 3-B / 5-A | HIGH | `CurrentUser.java`, `CommonFunc.java`, `UserDb.java` | Password hashed with unsalted MD5 — cryptographically broken; enables pass-the-hash replay |
| 3-C / 5-B | HIGH | `CurrentUser.java` | `logout()` does not null `loginEmail`, `loginPassword`, or `training` — credential material persists in static memory across operator sessions |
| 3-D | MEDIUM | `CurrentUser.java`, `ModelPrefs.java` | User ID persisted in plain `SharedPreferences`; used to restore session without re-authentication |
| 5-C | LOW | `CurrentUser.java`, `UserDb.java` | Offline authentication fallback has no failed-attempt limit or lockout |
| 5-D | INFORMATIONAL | `CurrentUser.java`, `User.java` | Server login response populates `password` field in `User` object; scope of what the server returns is unverified |
