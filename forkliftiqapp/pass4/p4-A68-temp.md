# Pass 4 – Code Quality Audit
**Agent:** A68
**Audit run:** 2026-02-26-01
**Date written:** 2026-02-27
**Files audited:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/UserPhotoFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/CurrentUser.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/User.java`

---

## Step 1: Reading Evidence

### File 1: `UserPhotoFragment.java`

**Class:** `UserPhotoFragment` (package-private, no modifier; not a Fragment subclass)
**Inner class:** `UserPhotoFragment.SSLCertificateHandler` (public static)

**Methods — exhaustive list:**

| Line | Visibility | Method |
|------|-----------|--------|
| 18 | (package-private) static | `showUserPhoto(ImageView imageView)` |
| 41 | public static | `SSLCertificateHandler.nuke()` |
| 44 | public | `SSLCertificateHandler.getAcceptedIssuers()` (anonymous X509TrustManager) |
| 49 | public | `SSLCertificateHandler.checkClientTrusted(X509Certificate[], String)` (anonymous) |
| 53 | public | `SSLCertificateHandler.checkServerTrusted(X509Certificate[], String)` (anonymous) |
| 63 | public | anonymous HostnameVerifier `verify(String, SSLSession)` |

**Constants/Fields:**

| Line | Scope | Name | Value |
|------|-------|------|-------|
| 38 | protected static final | `TAG` | `"NukeSSLCerts"` |

**Annotations used:** `@SuppressLint("TrustAllX509TrustManager")` (line 40), `@SuppressLint("BadHostnameVerifier")` (line 61)

**Imports:** `android.annotation.SuppressLint`, `android.widget.ImageView`, `R`, `CurrentUser`, `User`, `DisplayImageOptions`, `ImageLoader`, `SimpleBitmapDisplayer`, `javax.net.ssl.*`, `SecureRandom`, `X509Certificate`

---

### File 2: `CurrentUser.java`

**Class:** `CurrentUser` (public, effectively a static-only utility class — no private constructor)
**Interface:** `CurrentUser.LoginHandler` (public, lines 114–118)

**Methods — exhaustive list:**

| Line | Visibility | Method |
|------|-----------|--------|
| 26 | public static | `get()` |
| 32 | public static | `setUser(User newUser)` |
| 37 | public static | `setUser(LoginItem loginItem)` |
| 48 | private static | `setUserTraining(List<TrainingItem> newTraining)` |
| 53 | public static | `getTrainingList()` |
| 58 | private static | `createUser(LoginItem loginItem)` |
| 80 | public static | `login(LoginHandler handler)` |
| 120 | public static | `setTemporaryLoginInformation(String email, String password)` |
| 125 | public static | `logout()` |

**LoginHandler interface methods (lines 115–117):** `HandleSuccess()`, `HandleIncorrectCredentials()`

**Static fields:**

| Line | Modifier | Name | Type |
|------|---------|------|------|
| 19 | private final static String | `CURRENT_USER_ID_KEY` | `"current_user_id"` |
| 21 | private static | `user` | `User` |
| 22 | private static | `loginEmail` | `String` |
| 23 | private static | `loginPassword` | `String` |
| 24 | private static | `training` | `List<TrainingItem>` |

**Imports:** `WebApi`, `WebListener`, `WebResult`, `LoginItem`, `TrainingItem`, `LoginParameter`, `LoginResultArray`, `ModelPrefs`, `CommonFunc`, `ServerDateFormatter`, `HttpURLConnection`, `ArrayList`, `List`

---

### File 3: `User.java`

**Class:** `User` (public)

**Constructor:**

| Line | Visibility | Signature |
|------|-----------|-----------|
| 30 | (package-private) | `User(int id, int companyId, String firstName, String lastName, String email, String password, String phoneNumber, String licenseNumber, Date expiryDate, String address, String securityNumber, String photoUrl, boolean isContactPerson, String dateFormat, int maxSessionLength, Date complianceDate, int gpsFrequency)` |

**Methods — exhaustive list:**

| Line | Visibility | Method |
|------|-----------|--------|
| 66 | public | `fullName()` |
| 70 | public | `definedName()` |
| 78 | public | `complianceIsValid()` |
| 82 | public | `hasAssociatedDrivers()` |
| 86 | public | `associatedDrivers()` |
| 90 | public | `updateInformation(String firstName, String lastName, String complianceDate)` |
| 97 | public | `updateLicense(String licenseNumber, String securityNumber, String address, String expiryDate)` |
| 105 | public | `updateCompliance(Date complianceDate)` |
| 110 | (package-private) | `setPassword(String password)` |
| 115 | public | `getId()` |
| 119 | public | `getCompanyId()` |
| 123 | public | `getFirstName()` |
| 127 | public | `getLastName()` |
| 131 | public | `getEmail()` |
| 135 | public | `getPassword()` |
| 139 | (package-private) | `getPhoneNumber()` |
| 143 | public | `getLicenseNumber()` |
| 147 | public | `getExpiryDate()` |
| 151 | public | `getAddress()` |
| 155 | public | `getSecurityNumber()` |
| 159 | public | `getPhotoUrl()` |
| 163 | public | `isContactPerson()` |
| 167 | public | `getDateFormat()` |
| 171 | public | `getMaxSessionLength()` |
| 175 | public | `getGps_frequency()` |
| 179 | public | `getComplianceDate()` |

**Fields:**

| Line | Modifier | Name | Type |
|------|---------|------|------|
| 12 | private | `id` | `int` |
| 13 | private | `companyId` | `int` |
| 14 | private | `firstName` | `String` |
| 15 | private | `lastName` | `String` |
| 16 | private | `email` | `String` |
| 17 | private | `password` | `String` |
| 18 | private | `phoneNumber` | `String` |
| 19 | private | `licenseNumber` | `String` |
| 20 | private | `expiryDate` | `Date` |
| 21 | private | `address` | `String` |
| 22 | private | `securityNumber` | `String` |
| 23 | private | `photoUrl` | `String` |
| 24 | private | `isContactPerson` | `boolean` |
| 25 | private | `dateFormat` | `String` |
| 26 | private | `maxSessionLength` | `int` |
| 27 | private | `complianceDate` | `Date` |
| 28 | private | `gps_frequency` | `int` |

**Imports used:** `EquipmentItem` (line 3), `LoginItem` (line 4), `TrainingItem` (line 5), `ServerDateFormatter` (line 6), `Date` (line 8), `List` (line 9)

---

## Step 2 & 3: Findings

---

### A68-1 — CRITICAL: SSL validation completely disabled for image loading

**File:** `UserPhotoFragment.java`, lines 37–70
**Category:** Security / Build warnings (`@SuppressLint`)

`SSLCertificateHandler.nuke()` installs a process-global `TrustManager` that accepts every X.509 certificate without validation (`checkClientTrusted` and `checkServerTrusted` are empty), and a `HostnameVerifier` that returns `true` unconditionally. Both are applied via `HttpsURLConnection.setDefaultSSLSocketFactory` and `HttpsURLConnection.setDefaultHostnameVerifier`, which affect the entire JVM process — not just photo requests.

The developer suppressed the resulting lint warnings with `@SuppressLint("TrustAllX509TrustManager")` and `@SuppressLint("BadHostnameVerifier")` rather than addressing the root cause. This means:
- Any HTTPS connection made by any part of the application after `nuke()` is called is vulnerable to man-in-the-middle attack.
- `nuke()` is called every time a user photo URL is non-null — i.e., every time a screen with a user photo loads. Cross-referencing confirms it is also called directly from `SelectDriverPresenter` (line 39) and `EquipmentSelectForkPresenter` (line 71), widening the call surface.
- Exceptions in the `try` block are silently swallowed (`catch (Exception ignored) {}`), masking any failure to install the insecure handlers.

This is a production security defect. The `@SuppressLint` annotations are misused to silence the lint tooling instead of fixing the underlying problem.

---

### A68-2 — HIGH: `UserPhotoFragment` is not a Fragment — misleading class name and wrong package

**File:** `UserPhotoFragment.java`, lines 17–71
**Category:** Leaky abstraction / Style

`UserPhotoFragment` does not extend `Fragment` or any Android UI base class. It is a plain Java class containing two `static` utility methods. It:
- Lives in the `ui.fragment` package, implying a UI Fragment lifecycle component.
- Is named with the `Fragment` suffix, implying Fragment behaviour.
- Holds an inner `SSLCertificateHandler` class that is a pure networking utility with no UI relationship.

The class should be named `UserPhotoHelper` or `UserPhotoUtils`, placed in a `util` package, and `SSLCertificateHandler` should either be removed (see A68-1) or placed in a networking utility class. As written, the name and package actively mislead maintainers about the class's role and lifecycle.

---

### A68-3 — HIGH: `SSLCertificateHandler` is a public API exported from a UI fragment package

**File:** `UserPhotoFragment.java`, lines 37–70
**Category:** Leaky abstraction

`SSLCertificateHandler` is declared `public static`, and its `nuke()` method is `public static`. It is directly called from two unrelated presenter classes (`SelectDriverPresenter`, `EquipmentSelectForkPresenter`) that import the `ui.fragment` package solely to reach it. This creates coupling from the presenter/business layer into the UI fragment package for a networking concern. The SSL-disabling logic should not exist as a public utility at all (see A68-1), but if it were to be retained it should not be exposed through a UI package.

---

### A68-4 — HIGH: Password stored as MD5 hash in plaintext on-device database

**File:** `CurrentUser.java`, lines 120–123 and 103; `User.java`, line 135; `UserRealmObject.java`, lines 37, 80
**Category:** Security / Leaky abstraction

`setTemporaryLoginInformation` hashes the raw password with MD5 (line 122) and stores the result in the static `loginPassword` field. This MD5-hashed password is then:
1. Sent to the server as the `password` parameter in `LoginParameter` (line 83).
2. Stored in the local Realm database via `UserDb.save` and `User.setPassword` / `UserRealmObject.setValues` (lines 90, 112, 80 of `UserRealmObject`).
3. Used to look up the user in the local database in offline mode (line 103), meaning the hash is the credential stored and compared.

MD5 is a deprecated cryptographic hash with well-known collision and preimage vulnerabilities. It is not a password hashing function (it is not salted and is extremely fast to brute-force). Storing the MD5 hash in plaintext in a local Realm database means that compromise of the Realm file yields credential material directly usable against the server.

Additionally, `User.getPassword()` is declared `public` (line 135), exposing the stored credential to any caller that holds a `User` reference.

---

### A68-5 — HIGH: Double-hashing of email credential before network send

**File:** `CurrentUser.java`, lines 82, 121
**Category:** Style inconsistency / Security

`setTemporaryLoginInformation` stores the raw email string in `loginEmail` (line 121 stores `email` unchanged). Inside `login()`, line 82 applies `CommonFunc.MD5_Hash(loginEmail)` again at send time. However, `loginPassword` is already MD5-hashed at store time (line 122) and sent directly without re-hashing (line 83). This is an inconsistent pattern: the email is hashed at use-time while the password is hashed at storage-time. The asymmetry is confusing and makes it easy to introduce a double-hash bug on the password side or forget to hash the email.

---

### A68-6 — MEDIUM: `CurrentUser` has no private constructor — instantiable static utility class

**File:** `CurrentUser.java`, line 18
**Category:** Style / Dead code risk

`CurrentUser` is intended to be a static-only class (all fields and methods are static; the class tracks a single global user). It declares no constructor, so Java generates a public default no-argument constructor. Any code can instantiate `CurrentUser` via `new CurrentUser()`, which produces a meaningless object with no instance state. A `private CurrentUser() {}` constructor should be declared to prevent accidental instantiation, consistent with the static-utility pattern used elsewhere in the codebase.

---

### A68-7 — MEDIUM: Unused imports in `User.java`

**File:** `User.java`, lines 3–5
**Category:** Dead code / Build warnings

Three imports are present that are never referenced in the file body:
- Line 3: `import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.EquipmentItem;`
- Line 4: `import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.LoginItem;`
- Line 5: `import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.TrainingItem;`

`User` contains no fields, method parameters, or return types that reference `EquipmentItem`, `LoginItem`, or `TrainingItem`. These are dead imports, likely residue from a prior design where `User` directly consumed `LoginItem`. They generate IDE/lint warnings and create a false dependency from the domain model into the web-service layer.

---

### A68-8 — MEDIUM: Naming inconsistency — `gps_frequency` field uses snake_case; all other fields use camelCase

**File:** `User.java`, line 28; `UserRealmObject.java`, line 26
**Category:** Style inconsistency

Every other field in `User` and `UserRealmObject` is named in lowerCamelCase (`companyId`, `firstName`, `licenseNumber`, etc.), following the Java naming convention and the Google Java Style Guide. The field `gps_frequency` uses underscore (snake_case). The corresponding getter `getGps_frequency()` (line 175 of `User.java`) also violates the Java getter naming convention (`getGpsFrequency()` would be correct). The same snake_case field name appears in `UserRealmObject.java` (line 26, line 48, line 91), confirming this is not isolated to one file.

---

### A68-9 — MEDIUM: `definedName()` logic error — condition uses `||` (OR) instead of `&&` (AND)

**File:** `User.java`, lines 70–76
**Category:** Dead code / Logic bug

```java
public String definedName() {
    if (!firstName.isEmpty() || !lastName.isEmpty())
        return fullName();
    if (!email.isEmpty())
        return email;
    return "-";
}
```

The intent is clearly: "if the user has a name (either first or last is present), return the full name." The condition `!firstName.isEmpty() || !lastName.isEmpty()` returns `true` if *either* part is non-empty, which is semantically reasonable. However, `fullName()` is `String.format("%s %s", firstName, lastName)`, so if only `firstName` is non-empty (e.g., `"Alice"`, `""`), `fullName()` returns `"Alice "` — a trailing space. If only `lastName` is non-empty, it returns `" Smith"` — a leading space. The method delegates to `fullName()` without trimming, producing visually incorrect output. Additionally, `firstName` and `lastName` are never checked for `null`; if either is `null`, `isEmpty()` throws a `NullPointerException`.

---

### A68-10 — MEDIUM: `TAG` field in `SSLCertificateHandler` is declared but never used

**File:** `UserPhotoFragment.java`, line 38
**Category:** Dead code

```java
protected static final String TAG = "NukeSSLCerts";
```

`TAG` is never referenced anywhere in the file. There is no `Log.d(TAG, ...)` call or any other use within `SSLCertificateHandler` or `UserPhotoFragment`. The field is dead. The `protected` modifier on a `static final` field in a non-inherited `static` inner class is also unusual — `private` would be appropriate if the field were used at all.

---

### A68-11 — MEDIUM: `training` list not cleared on `logout()`

**File:** `CurrentUser.java`, lines 24, 125–128
**Category:** Style inconsistency / Leaky state

`logout()` sets `user = null` and deletes the `CURRENT_USER_ID_KEY` preference (lines 126–127), but it does not reset the `training` list. After logout, `getTrainingList()` still returns the previous user's training items. If a different user logs in subsequently without the app process restarting, the stale training data could be visible. The `login()` flow calls `setUserTraining` (via `setUser(LoginItem)`) only on successful server-side login; offline login via `UserDb.get(loginEmail, loginPassword)` (line 103–106) does not call `setUserTraining` at all, meaning training data is never refreshed in the offline path.

---

### A68-12 — LOW: `setUserTraining` is a private one-liner with unnecessary indirection

**File:** `CurrentUser.java`, lines 48–51
**Category:** Style inconsistency

```java
private static void setUserTraining(List<TrainingItem> newTraining) {
    training = newTraining;
}
```

This private method does nothing other than assign a field. It is called from exactly one place (line 41). The indirection adds no encapsulation value and is inconsistent with how other static fields (`user`, `loginEmail`, `loginPassword`) are set by direct assignment at their call sites. Either all field assignments should be wrapped in private setters, or none should be.

---

### A68-13 — LOW: `LoginHandler` interface method names use `PascalCase` instead of `camelCase`

**File:** `CurrentUser.java`, lines 114–118
**Category:** Style inconsistency

```java
public interface LoginHandler {
    void HandleSuccess();
    void HandleIncorrectCredentials();
}
```

Java interface method naming convention (JLS, Google Java Style Guide) requires method names to begin with a lowercase letter (`handleSuccess`, `handleIncorrectCredentials`). `HandleSuccess` and `HandleIncorrectCredentials` use PascalCase, which is the convention for class/type names. Every other method in the three audited files follows camelCase. This inconsistency is visible at every call site (lines 91, 93, 100, 106, 108).

---

### A68-14 — LOW: `showUserPhoto` is package-private but used across multiple fragments; access visibility is misleadingly narrow

**File:** `UserPhotoFragment.java`, line 18
**Category:** Style / Leaky abstraction

`showUserPhoto` is declared with no access modifier (package-private). Cross-reference shows it is called from `SetUserPhotoFragment`, `DashboardFragment`, `DriverStatsFragment1`, `DriverStatsFragment2`, `DriverStatsFragment3`, `EquipmentPrestartFragment`, and `JobsFragment` — all of which happen to be in the same `ui.fragment` package. Access is presently package-private by coincidence of package layout. If any caller were moved to a different package or sub-package, the build would break silently. The method should be declared `public static` to reflect its actual usage across multiple unrelated classes.

---

### A68-15 — INFO: `getExpiryDate()` has anomalous indentation

**File:** `User.java`, lines 147–149
**Category:** Style

```java
public Date getExpiryDate() {
        return expiryDate;
}
```

The `return` statement is indented with 8 spaces (two indent levels) rather than the 4-space single indent used by every other method in the file. This is a minor style inconsistency but deviates from the surrounding code.

---

## Summary Table

| ID | Severity | File | Issue |
|----|----------|------|-------|
| A68-1 | CRITICAL | UserPhotoFragment.java | TrustAll SSL handler nukes process-wide HTTPS certificate validation; suppressed with @SuppressLint |
| A68-2 | HIGH | UserPhotoFragment.java | Class is not a Fragment; wrong name and wrong package for a static utility |
| A68-3 | HIGH | UserPhotoFragment.java | SSLCertificateHandler is a public networking utility exposed through a UI fragment package, creating cross-layer coupling |
| A68-4 | HIGH | CurrentUser.java / User.java | Password stored as MD5 hash in local DB; `getPassword()` is public; MD5 not suitable as password hash |
| A68-5 | HIGH | CurrentUser.java | Asymmetric hashing: email hashed at use-time, password hashed at store-time |
| A68-6 | MEDIUM | CurrentUser.java | Static utility class has no private constructor; instantiable |
| A68-7 | MEDIUM | User.java | Three unused imports (EquipmentItem, LoginItem, TrainingItem) |
| A68-8 | MEDIUM | User.java / UserRealmObject.java | `gps_frequency` field and `getGps_frequency()` use snake_case; all other identifiers use camelCase |
| A68-9 | MEDIUM | User.java | `definedName()` produces leading/trailing spaces; no null-guard on firstName/lastName |
| A68-10 | MEDIUM | UserPhotoFragment.java | `TAG` field declared but never used; also marked `protected` without purpose |
| A68-11 | MEDIUM | CurrentUser.java | `logout()` does not clear `training` list; offline login path never refreshes training |
| A68-12 | LOW | CurrentUser.java | `setUserTraining` is a private one-liner called once; inconsistent with how other fields are assigned |
| A68-13 | LOW | CurrentUser.java | `LoginHandler` interface methods use PascalCase (`HandleSuccess`) instead of camelCase |
| A68-14 | LOW | UserPhotoFragment.java | `showUserPhoto` is package-private but relied on by 7 callers across the same package; should be `public` |
| A68-15 | INFO | User.java | `getExpiryDate()` return statement has double indentation |
