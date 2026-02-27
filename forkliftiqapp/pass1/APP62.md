# Pass 1 Security Audit — Agent APP62
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy:** Checklist specifies `Branch: main`; actual branch is `master`. Proceeding on `master` as confirmed.

---

## Reading Evidence

### File 1: `UserRealmObject.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.user.UserRealmObject`
**Extends:** `io.realm.RealmObject`

**Fields (all private, persisted to Realm):**

| Field | Type | Line |
|---|---|---|
| `id` | `int` | 10 |
| `companyId` | `int` | 11 |
| `firstName` | `String` | 12 |
| `lastName` | `String` | 13 |
| `email` | `String` | 14 |
| `password` | `String` | 15 |
| `phoneNumber` | `String` | 16 |
| `licenseNumber` | `String` | 17 |
| `expiryDate` | `Date` | 18 |
| `address` | `String` | 19 |
| `securityNumber` | `String` | 20 |
| `photoUrl` | `String` | 21 |
| `isContactPerson` | `boolean` | 22 |
| `dateFormat` | `String` | 23 |
| `maxSessionLength` | `int` | 24 |
| `complianceDate` | `Date` | 25 |
| `gps_frequency` | `int` | 26 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `UserRealmObject()` (no-arg constructor) | `public` | 28 |
| `UserRealmObject(User user)` (package-private constructor) | package-private | 31 |
| `makeUser()` | package-private | 51 |
| `getEmail()` | package-private | 71 |
| `setValues(User user)` | package-private | 75 |

No Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared in this file.

---

### File 2: `CommonFunc.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.util.CommonFunc`

**Fields:** None.

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `isCurrentDay(DateTime dateTime)` | `public static` | 16 |
| `isSameLocalDay(DateTime, DateTime)` | `private static` | 21 |
| `dateToLocalDayString(DateTime)` | `private static` | 32 |
| `getCurrentDateTimeZone()` | `private static` | 39 |
| `convertUTCDatetoLocalDate(Date utcDate)` | `public static` | 44 |
| `SHA1(String text)` | `public static` | 50 |
| `MD5_Hash(String s)` | `public static` | 68 |
| `isEmailInvalid(String email)` | `public static` | 85 |
| `isPasswordValid(String password)` | `public static` | 92 |

**Imports relevant to security:** `java.security.MessageDigest`, `java.security.NoSuchAlgorithmException`, `java.math.BigInteger`

No file I/O, network operations, Activities, Fragments, Services, BroadcastReceivers, or ContentProviders declared in this file.

---

### File 3: `CompanyDateFormatter.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.util.CompanyDateFormatter`

**Fields (all private instance):**

| Field | Type | Line |
|---|---|---|
| `timeFormat` | `SimpleDateFormat` | 10 |
| `dateFormat` | `SimpleDateFormat` | 11 |
| `dateTimeFormat` | `SimpleDateFormat` | 12 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `CompanyDateFormatter(String companyDateTimeFormatPattern)` | `public` | 14 |
| `formatTime(Date date)` | `public` | 24 |
| `formatDate(Date date)` | `public` | 28 |
| `formatDateTime(Date date)` | `public` | 32 |
| `parseDate(String date)` | `public` | 36 |

No security-relevant imports. No file I/O, network operations, Activities, Fragments, Services, BroadcastReceivers, or ContentProviders.

---

## Findings by Checklist Section

### Section 1 — Signing and Keystores

No issues found — Section 1. None of the three assigned files contain signing configuration, keystore references, passwords, or credentials related to build signing.

---

### Section 2 — Network Security

No issues found — Section 2. `CommonFunc.java` and `CompanyDateFormatter.java` contain no HTTP client usage, no URL construction, no SSL/TLS configuration, and no network operations. `UserRealmObject.java` is a pure data-layer class with no network interaction.

---

### Section 3 — Data Storage

**FINDING DS-01 — High: Password stored in plaintext in Realm database**

**File:** `UserRealmObject.java`, line 15
**Field:** `private String password;`

The `password` field is a direct member of a class extending `io.realm.RealmObject`. Realm persists all fields to its local database file on device storage. The password is written into Realm at line 37 (constructor) and updated at line 80 (`setValues`), unconditionally mapping `user.getPassword()` to this field. There is no hashing, encryption, or transformation applied to the value before persistence.

By default, Realm databases are stored unencrypted on the device filesystem. Even if the Realm instance is configured with an encryption key elsewhere in the codebase (not visible in this file), the `password` field value itself is passed in from the `User` object without any transformation, suggesting the raw credential is what is stored. If the caller supplies a plaintext password (confirmed as likely given the `SHA1` and `MD5_Hash` functions in `CommonFunc` are separate utilities rather than called here), the plaintext value reaches Realm.

This means any attacker with physical access to the device, a rooted device, or the ability to extract the Realm file (e.g., via ADB backup if `android:allowBackup` is enabled) can recover operator passwords directly.

**Fields of concern stored in Realm (PII and sensitive data):**
- `password` (line 15) — credential, plaintext as received
- `email` (line 14) — PII, operator identifier
- `securityNumber` (line 20) — PII, purpose unclear from name but likely a government or employment identifier (e.g., licence or national ID number), high sensitivity
- `licenseNumber` (line 17) — PII, forklift operator licence
- `address` (line 19) — PII
- `phoneNumber` (line 16) — PII
- `firstName`, `lastName` (lines 12–13) — PII

All of these are stored in Realm without any visible field-level encryption in this class. The Realm database at rest must be encrypted using a Realm encryption key stored in the Android Keystore to adequately protect this data. That configuration is external to this file and was not assessed here; however, the presence of an unencrypted `password` field in the schema is itself a design defect regardless of database-level encryption.

**Recommendation:** Remove the `password` field from the persisted Realm schema. Passwords should not be cached locally at all; if a local credential cache is required, store only a server-issued session token in `EncryptedSharedPreferences` or the Android Keystore, never the raw password.

---

**FINDING DS-02 — Medium: `securityNumber` field persisted to Realm**

**File:** `UserRealmObject.java`, line 20
**Field:** `private String securityNumber;`

The field name `securityNumber` suggests a government-issued or employment identification number (analogous to a national identification number or tax file number in an Australian context). This is high-sensitivity PII under the Australian Privacy Act 1988. It is persisted to Realm alongside the operator's full name, address, email, phone number, and licence number, creating a concentrated PII store on the device. The risk profile of a breach of this dataset is significant.

No issues found — Section 3 for `CommonFunc.java` and `CompanyDateFormatter.java`. Neither file performs storage operations.

---

### Section 4 — Input and Intent Handling

No issues found — Section 4. No Activities, Services, BroadcastReceivers, WebViews, or Intent handling are present in any of the three assigned files. `CompanyDateFormatter.parseDate` accepts an external string but uses `ParsePosition(0)` with `SimpleDateFormat.parse`, which returns `null` on failure rather than throwing; no injection vector is present.

---

### Section 5 — Authentication and Session

**FINDING AS-01 — High: Password persisted to Realm (cross-reference DS-01)**

**File:** `UserRealmObject.java`, lines 15, 37, 80

As detailed under DS-01, the `password` field is stored in Realm. From an authentication/session perspective, this means the plaintext (or at minimum unprocessed) password credential is retained on the device beyond the authentication event. There is no evidence in this file that the password is cleared from the Realm record after a successful login, nor that `setValues` (line 75) ever nulls this field out. Line 80 shows a null-guard (`if (user.getPassword() != null) password = user.getPassword()`) which prevents overwriting with null but does not clear the field on logout.

**FINDING AS-02 — Medium: Weak hashing functions available for credential processing**

**File:** `CommonFunc.java`, lines 50–83

Two cryptographic methods are present:

1. `SHA1(String text)` (line 50–66): Implements SHA-1 hashing via `MessageDigest`. SHA-1 is cryptographically broken — collision attacks are practical, and it is no longer considered suitable for any security-sensitive use including password hashing. It is not a password-hashing algorithm in any case (no salt, no iterations).

2. `MD5_Hash(String s)` (line 68–83): Implements MD5 hashing via `MessageDigest`. MD5 is cryptographically broken for all security uses. It is trivially reversible via rainbow tables and preimage attacks. It is completely unsuitable for password hashing.

Neither function accepts a salt parameter. Neither uses a key-stretching algorithm (bcrypt, scrypt, Argon2, PBKDF2). If either function is used to process passwords before transmission or storage, the hashing provides minimal security benefit.

The presence of these methods in the `util` package alongside `isPasswordValid` and `isEmailInvalid` strongly suggests they are used in the authentication flow. Their use for any security-sensitive purpose constitutes a vulnerability.

No issues found — Section 5 for `CompanyDateFormatter.java`. It contains no authentication or session logic.

---

### Section 6 — Third-Party Libraries

**FINDING TL-01 — Informational: Realm dependency in use**

**File:** `UserRealmObject.java`, lines 3–4

```java
import io.realm.RealmObject;
import io.realm.annotations.PrimaryKey;
```

Realm (Java SDK) is in use as the local database. Realm's Java SDK was deprecated by MongoDB in 2023. The Realm Java SDK receives no new features and only critical security fixes. Organisations are encouraged to migrate to a supported alternative. The security implication is a growing risk of unpatched vulnerabilities over time.

**FINDING TL-02 — Informational: Joda-Time in use**

**File:** `CommonFunc.java`, lines 3–6

```java
import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;
```

Joda-Time is the date/time library in use. Its author has recommended migrating to `java.time` (JSR-310, available on Android via desugaring or minSdk 26+). Joda-Time itself is no longer actively developed with new features. No direct CVE concern; informational only.

No issues found — Section 6 for `CompanyDateFormatter.java`. It uses only standard library `java.text.SimpleDateFormat`.

---

### Section 7 — Google Play and Android Platform

No issues found — Section 7. None of the three assigned files contain manifest declarations, SDK version references, permission declarations, or deprecated API usage that is assessable at this file scope. `AsyncTask` is not used. `SimpleDateFormat` with explicit `Locale.US` in `CompanyDateFormatter` is a positive practice (avoids locale-dependent parsing bugs).

---

## Summary of Findings

| ID | Severity | File | Description |
|---|---|---|---|
| DS-01 | High | `UserRealmObject.java` L15, L37, L80 | `password` field persisted to Realm database unencrypted at the field level |
| AS-01 | High | `UserRealmObject.java` L15, L80 | Password credential retained in Realm beyond authentication; no evidence of post-login clearing |
| AS-02 | Medium | `CommonFunc.java` L50–83 | SHA-1 and MD5 hashing utilities present; both are broken algorithms unsuitable for credential processing; no salting or key-stretching |
| DS-02 | Medium | `UserRealmObject.java` L20 | `securityNumber` (likely government-issued ID) persisted to Realm alongside comprehensive PII dataset |
| TL-01 | Informational | `UserRealmObject.java` | Realm Java SDK is deprecated; growing risk of unpatched vulnerabilities |
| TL-02 | Informational | `CommonFunc.java` | Joda-Time is unmaintained; recommend migration to `java.time` |
